"""Temporary authenticated Cloudflare API session. No service installation."""
import argparse
import getpass
import json
import os
from pathlib import Path
import re
import secrets
import socket
import subprocess
import sys
import time
import webbrowser
import urllib.error
import urllib.request
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8000)
    parser.add_argument('--device', choices=['auto', 'cuda', 'cpu', 'mps'], default='auto')
    parser.add_argument('--api-only', action='store_true', help='Do not launch the two local websites')
    args = parser.parse_args()
    if not 1024 <= args.port <= 65535:
        parser.error('Port must be 1024..65535')
    executable = ROOT / '.runtime/tunnel/cloudflared.exe'
    if not executable.is_file():
        parser.error('Missing .runtime/tunnel/cloudflared.exe; see docs/TEMPORARY_API.md')
    try:
        version = subprocess.run([str(executable), '--version'], capture_output=True, text=True, timeout=10, check=True)
        print(version.stdout.strip(), flush=True)
    except (OSError, subprocess.SubprocessError):
        parser.error('cloudflared cannot run. Its download may still be incomplete; finish downloading it first.')
    with socket.socket() as probe:
        if probe.connect_ex(('127.0.0.1', args.port)) == 0:
            parser.error('Port already in use. Stop the existing RETFound server in its terminal first; no process was stopped.')
    environment = os.environ.copy()
    if not args.api_only:
        for ui_port in (8001, 8002):
            with socket.socket() as probe:
                if probe.connect_ex(('127.0.0.1', ui_port)) == 0:
                    parser.error(f'Port {ui_port} is occupied. Stop that UI first, or use --api-only.')
    key = environment.get('OPENROUTER_API_KEY', '').strip()
    if not key:
        key = getpass.getpass('OpenRouter key (hidden; never saved): ').strip()
    if not re.fullmatch(r'sk-or-v1-[A-Za-z0-9_-]{32,256}', key):
        parser.error('Expected an OpenRouter inference key. No key was saved or sent.')
    environment['OPENROUTER_API_KEY'] = key
    environment['RETFOUND_API_KEY'] = secrets.token_urlsafe(32)
    session = ROOT / '.runtime/tunnel' / (datetime.now().strftime('%Y%m%d-%H%M%S-') + secrets.token_hex(3))
    session.mkdir()
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    server = None
    tunnel = None
    interfaces = []
    interface_logs = []
    try:
        with (session / 'server.log').open('w', encoding='utf-8') as server_log, (session / 'tunnel.log').open('w', encoding='utf-8') as tunnel_log:
            server = subprocess.Popen([sys.executable, '-B', str(ROOT / 'scripts/serve_web.py'), '--public-api',
                                       '--public-demo', '--port', str(args.port), '--device', args.device],
                                      cwd=ROOT, env=environment, stdout=server_log, stderr=subprocess.STDOUT)
            print('Loading RETFound once. Ctrl+C stops this complete temporary session.', flush=True)
            deadline = time.monotonic() + 300
            while time.monotonic() < deadline:
                if server.poll() is not None:
                    raise RuntimeError(f'Server exited. Inspect {session / "server.log"}')
                request = urllib.request.Request(f'http://127.0.0.1:{args.port}/api/health',
                    headers={'Authorization': 'Bearer ' + environment['RETFOUND_API_KEY']})
                try:
                    with opener.open(request, timeout=2) as response:
                        if json.load(response).get('status') == 'ready':
                            break
                except (OSError, ValueError):
                    pass
                time.sleep(1)
            else:
                raise RuntimeError('Model readiness exceeded five minutes; tunnel was not opened.')
            tunnel_environment = os.environ.copy()
            for name in ('OPENROUTER_API_KEY', 'RETFOUND_API_KEY'):
                tunnel_environment.pop(name, None)
            tunnel = subprocess.Popen([str(executable), 'tunnel', '--no-autoupdate', '--url',
                                       f'http://127.0.0.1:{args.port}', '--http-host-header', 'localhost',
                                       '--protocol', 'http2'], cwd=ROOT, env=tunnel_environment,
                                      stdout=tunnel_log, stderr=subprocess.STDOUT)
            deadline = time.monotonic() + 90
            url = None
            while time.monotonic() < deadline:
                if tunnel.poll() is not None:
                    raise RuntimeError(f'Tunnel exited. Inspect {session / "tunnel.log"}')
                match = re.search(r'https://[a-z0-9-]+\.trycloudflare\.com', (session / 'tunnel.log').read_text(encoding='utf-8', errors='replace'))
                if match:
                    url = match.group()
                    break
                time.sleep(1)
            if not url:
                raise RuntimeError('No temporary URL received within 90 seconds.')
            # Persist only the new session access key, never the OpenRouter credential.
            details = {'base_url': url, 'predict_url': url + '/api/predict',
                       'authorization': 'Bearer ' + environment['RETFOUND_API_KEY'],
                       'limit': '30 submissions/minute; 3 admitted; one inference executor'}
            (session / 'connection.json').write_text(json.dumps(details, indent=2), encoding='utf-8')
            # Stable current-session file; retain each session's original evidence.
            current_connection = ROOT / '.runtime/tunnel/connection.json'
            staged_connection = session / 'current-connection.tmp'
            staged_connection.write_text(json.dumps(details, indent=2), encoding='utf-8')
            staged_connection.replace(current_connection)
            print(f'\nTemporary URL: {url}\nPrivate colleague connection details: {session / "connection.json"}\n'
                  f'Complete demo: {url}\nDataset tests: {url}/dataset-tests\n'
                  f'Automatically updated connection file: {current_connection}\n'
                  'Share that file privately. Keep this terminal open. Ctrl+C stops server and tunnel.\n'
                  'This URL is not yet an independently verified external prediction.', flush=True)
            print('Waiting for the public connection before opening the demo...', flush=True)
            public_ready = False
            attempt = 0
            while not public_ready:
                if server.poll() is not None or tunnel.poll() is not None:
                    raise RuntimeError('Server or tunnel exited while waiting for public readiness.')
                attempt += 1
                try:
                    check = urllib.request.Request(url + '/api/health', headers={
                        'Authorization': 'Bearer ' + environment['RETFOUND_API_KEY']})
                    with opener.open(check, timeout=5) as response:
                        public_ready = response.status == 200 and json.load(response).get('status') == 'ready'
                except (OSError, ValueError):
                    pass
                if public_ready:
                    break
                if attempt % 6 == 0:
                    print('Still waiting for external DNS/API readiness. The two apps will start automatically; Ctrl+C stops.', flush=True)
                time.sleep(2)
            if public_ready:
                print('External API is reachable. Keep this window OPEN while using it.', flush=True)
                if not args.api_only:
                    ui_environment = tunnel_environment.copy()
                    ui_environment['EYE_AI_HOST'] = '127.0.0.1'
                    ui_environment['RETFOUND_API_URL'] = url
                    ui_environment['RETFOUND_CONNECTION_FILE'] = str(current_connection)
                    for name, command in (
                        ('eye-ai', [sys.executable, '-B', str(ROOT / 'eye-ai-demo/run_demo.py'), '--no-browser', '--port', '8001']),
                        ('retfound-site', [sys.executable, '-B', str(ROOT / 'scripts/serve_site.py'), '--port', '8002']),
                    ):
                        log = (session / (name + '.log')).open('w', encoding='utf-8')
                        interface_logs.append(log)
                        interfaces.append(subprocess.Popen(command, cwd=ROOT, env=ui_environment, stdout=log, stderr=subprocess.STDOUT))
                    for ui_url in ('http://127.0.0.1:8001', 'http://127.0.0.1:8002'):
                        for _ in range(30):
                            if any(p.poll() is not None for p in interfaces):
                                raise RuntimeError(f'A UI process exited; inspect {session} for eye-ai.log and retfound-site.log')
                            try:
                                with opener.open(ui_url, timeout=2) as response:
                                    if response.status == 200:
                                        break
                            except OSError:
                                pass
                            time.sleep(1)
                        else:
                            raise RuntimeError(f'UI failed to start: {ui_url}; inspect session logs.')
                        webbrowser.open(ui_url)
                    print('Eye AI demo: http://127.0.0.1:8001\nRETFound website: http://127.0.0.1:8002\n'
                          'Both use the external API; access keys stay in their servers.', flush=True)
            else:
                print('Public connection is not ready yet. Server stays running; check tunnel.log.\n'
                      'Do not close this window. Opening the URL now may show a Cloudflare error.', flush=True)
            while server.poll() is None and tunnel.poll() is None and all(p.poll() is None for p in interfaces):
                time.sleep(1)
            raise RuntimeError('A child process exited; session stopped. Inspect session logs.')
    except KeyboardInterrupt:
        print('\nStopping temporary session.', flush=True)
        return 0
    except (OSError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    finally:
        for process in (*interfaces, tunnel, server):
            if process is not None and process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
        for log in interface_logs:
            log.close()


if __name__ == '__main__':
    raise SystemExit(main())
