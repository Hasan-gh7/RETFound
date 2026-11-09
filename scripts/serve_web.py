import argparse
import json
import socket
import threading
import time
import urllib.request
import webbrowser
import os

from web_runtime import configure


def running_model(url: str) -> dict | None:
    """Identify a ready local RETFound service, bypassing system HTTP proxies."""
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        def read(path):
            with opener.open(url + path, timeout=2) as response:
                return json.loads(response.read(65536))
        health, model = read('/api/health'), read('/api/model')
        if (health.get('status') == 'ready' and model.get('name') == 'RETFound MAE'
                and model.get('architecture') == 'ViT-Large'
                and len(model.get('grades', [])) == 5
                and len(model.get('checkpoint_sha256', '')) == 64):
            return model
    except (OSError, ValueError, TypeError, AttributeError):
        pass
    return None


def reserve_port(port: int) -> socket.socket:
    """Reserve before model loading so duplicate launches cannot allocate a model."""
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        if hasattr(socket, 'SO_EXCLUSIVEADDRUSE'):
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        listener.bind(('127.0.0.1', port))
        return listener
    except OSError:
        listener.close()
        raise


def main() -> None:
    configure()
    parser = argparse.ArgumentParser(description='RETFound local image prediction web application')
    parser.add_argument('--port', type=int, default=8000)
    parser.add_argument('--device', choices=['auto', 'cuda', 'cpu', 'mps'], default='auto')
    parser.add_argument('--allow-origin', action='append', default=[], help='Explicit browser origin for another local web app')
    parser.add_argument('--open-browser', action='store_true')
    parser.add_argument('--public-api', action='store_true', help='API-only mode protected by RETFOUND_API_KEY')
    parser.add_argument('--public-demo', action='store_true', help='Enable complete UI with authenticated external API')
    args = parser.parse_args()
    api_key = os.environ.get('RETFOUND_API_KEY', '') if args.public_api else ''
    if args.public_api and len(api_key) < 32:
        parser.error('Public API requires RETFOUND_API_KEY (at least 32 characters)')
    if not 1024 <= args.port <= 65535:
        parser.error('--port must be 1024..65535')
    url = f'http://127.0.0.1:{args.port}'
    try:
        listener = reserve_port(args.port)
    except OSError as exc:
        existing = None if args.public_api else running_model(url)
        if existing is not None:
            print(f'RETFound is already running: {url}\n'
                  f'Device: {existing["device"]}. Reusing the existing server; no second model was loaded.\n'
                  'Existing server settings remain in effect.', flush=True)
            if args.open_browser:
                webbrowser.open(url)
            return
        parser.exit(2, f'Cannot reserve {url}: {exc}\n'
                    'The port may belong to another application or a server that is still starting.\n'
                    'No process was stopped. Wait for startup, or use --port 8001.\n')
    try:
        import uvicorn
        from retfound_platform.api.app import Settings, create_app
    except ImportError as exc:
        listener.close()
        parser.exit(1, f'Web dependency missing: {exc}. Run setup_web.bat first.\n')
    print(f'RETFound web app: {url}\nLoading the classifier once; startup may take a moment.', flush=True)
    if args.open_browser:
        def open_when_ready():
            for _ in range(180):
                try:
                    with urllib.request.urlopen(url + '/api/health', timeout=1) as response:
                        if response.status == 200:
                            webbrowser.open(url)
                            return
                except OSError:
                    time.sleep(1)
        threading.Thread(target=open_when_ready, daemon=True).start()
    try:
        config = uvicorn.Config(create_app(Settings(device=args.device, allowed_origins=tuple(args.allow_origin),
                                                   public_api=args.public_api, api_key=api_key, public_demo=args.public_demo)),
                                host='127.0.0.1', port=args.port, workers=1, access_log=False)
        uvicorn.Server(config).run(sockets=[listener])
    finally:
        listener.close()


if __name__ == '__main__':
    main()
