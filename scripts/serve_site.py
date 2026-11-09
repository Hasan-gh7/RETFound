"""Local original RETFound website, forwarding to the external API with a private key."""
import argparse
import json
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import urllib.request
import urllib.error
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def make_handler(connection: dict):
    base = connection['base_url'].rstrip('/')
    parsed = urlsplit(base)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password or parsed.path or parsed.query or parsed.fragment:
        raise ValueError('Expected an HTTPS service origin')
    authorization = connection['authorization']
    if not authorization.startswith('Bearer ') or '\n' in authorization or '\r' in authorization:
        raise ValueError('Invalid access key')
    opener = urllib.request.build_opener(NoRedirect(), urllib.request.ProxyHandler({}))
    assets = {'/', '/index.html', '/app.js', '/styles.css', '/input-validation.css', '/favicon.svg', '/dataset-tests', '/dataset-tests.js', '/dataset-tests.css', '/openapi.json'}
    local_assets = {path: ('index.html' if path == '/' else 'dataset-tests.html' if path == '/dataset-tests' else path[1:]) for path in assets if path != '/openapi.json'}

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def reply(self, status, body, content_type='application/json'):
            try:
                self.write_reply(status, body, content_type)
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError, TimeoutError):
                # A disconnected browser must not trigger a second upstream call/response.
                self.close_connection = True

        def write_reply(self, status, body, content_type):
            self.send_response(status)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Referrer-Policy', 'no-referrer')
            self.send_header('Content-Security-Policy', "default-src 'self'; img-src 'self' blob: data:; style-src 'self'; script-src 'self'; connect-src 'self'; frame-ancestors 'none'")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            self.forward()

        def do_POST(self):
            self.forward()

        def forward(self):
            host = self.headers.get('Host', '')
            allowed_hosts = {f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}'}
            if host not in allowed_hosts:
                return self.reply(403, b'{"error":{"message":"Invalid host"}}')
            if self.command == 'POST' and self.headers.get('Origin') not in (None, f'http://{host}'):
                return self.reply(403, b'{"error":{"message":"Invalid origin"}}')
            if self.command == 'GET' and self.path == '/demo-auth.js':
                return self.reply(200, b'// Authentication is handled by the local site server.', 'text/javascript')
            if self.command == 'GET' and self.path in local_assets:
                asset = ROOT / 'frontend' / local_assets[self.path]
                mime = {'.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8', '.svg': 'image/svg+xml'}
                try:
                    body = asset.read_bytes()
                except OSError:
                    return self.reply(404, b'{"error":{"message":"UI asset unavailable"}}')
                return self.reply(200, body, mime.get(asset.suffix, 'application/octet-stream'))
            parts = self.path.split('/')
            sample = len(parts) == 5 and parts[1:3] == ['api', 'demo'] and parts[3] in {f'{d}-{g}' for d in ('IDRID', 'MESSIDOR2', 'DDR') for g in range(5)}
            permitted = (self.command == 'GET' and (self.path in assets | {'/api/health', '/api/model', '/api/demo', '/api/example', '/api/evaluation'} or sample and parts[4] in {'image', 'thumbnail'})) or (self.command == 'POST' and (self.path in {'/api/predict', '/api/predict/summary'} or sample and parts[4] == 'predict'))
            if not permitted:
                return self.reply(404, b'{"error":{"message":"Unknown route"}}')
            data = None
            self.connection.settimeout(30)
            if self.command == 'POST':
                length = self.headers.get('Content-Length', '')
                if self.headers.get('Transfer-Encoding') or not length.isdecimal() or int(length) > 20 * 1024 * 1024 + 65536:
                    return self.reply(413, b'{"error":{"message":"Invalid upload size"}}')
                data = self.rfile.read(int(length))
                if len(data) != int(length):
                    return self.reply(400, b'{"error":{"message":"Incomplete upload"}}')
            headers = {'Authorization': authorization}
            if data is not None:
                headers['Content-Type'] = self.headers.get('Content-Type', 'application/octet-stream')
            try:
                req = urllib.request.Request(base + self.path, data=data, headers=headers, method=self.command)
                try:
                    response = opener.open(req, timeout=150)
                except urllib.error.HTTPError as exc:
                    response = exc
                with response:
                    body = response.read(24 * 1024 * 1024 + 1)
                    if len(body) > 24 * 1024 * 1024:
                        raise ValueError('Response too large')
                    self.reply(response.code, body, response.headers.get('Content-Type', 'application/json'))
            except (OSError, ValueError):
                self.reply(502, b'{"error":{"message":"External API unavailable; no automatic retry."}}')
    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--connection-file', type=Path, default=ROOT / '.runtime/tunnel/connection.json')
    parser.add_argument('--port', type=int, default=8002)
    args = parser.parse_args()
    connection = json.loads(args.connection_file.read_text(encoding='utf-8'))
    with ThreadingHTTPServer(('127.0.0.1', args.port), make_handler(connection)) as server:
        print(f'RETFound website: http://127.0.0.1:{args.port}', flush=True)
        server.serve_forever()


if __name__ == '__main__':
    main()
