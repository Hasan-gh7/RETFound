import io
import json
import threading
import unittest
import urllib.request
import urllib.error
from http.server import ThreadingHTTPServer
from unittest.mock import patch
from scripts.serve_site import make_handler


class ProxyTests(unittest.TestCase):
    def test_private_forwarding_and_browser_boundaries(self):
        calls = []
        class Reply(io.BytesIO):
            code = 200
            headers = {'Content-Type': 'application/json'}
        class Upstream:
            def open(self, req, timeout):
                calls.append(req)
                return Reply(b'{"status":"ready"}')
        with patch('scripts.serve_site.urllib.request.build_opener', return_value=Upstream()):
            handler = make_handler({'base_url': 'https://fixture.trycloudflare.com', 'authorization': 'Bearer private-test-key'})
        server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
        worker = threading.Thread(target=server.serve_forever, daemon=True); worker.start()
        base = f'http://127.0.0.1:{server.server_port}'
        client = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        try:
            with client.open(base + '/demo-auth.js') as response:
                self.assertNotIn(b'private-test-key', response.read())
            self.assertEqual(calls, [])
            for path, content_type in [('/', 'text/html'), ('/app.js', 'text/javascript'), ('/styles.css', 'text/css'), ('/dataset-tests', 'text/html')]:
                with client.open(base + path, timeout=2) as response:
                    self.assertEqual(response.status, 200)
                    self.assertTrue(response.headers['Content-Type'].startswith(content_type))
                    self.assertNotIn(b'private-test-key', response.read())
            self.assertEqual(calls, [], 'UI startup must not wait for external API or DNS')
            with client.open(base + '/api/health') as response:
                self.assertEqual(json.load(response)['status'], 'ready')
            self.assertEqual(calls[-1].get_header('Authorization'), 'Bearer private-test-key')
            self.assertEqual(calls[-1].full_url, 'https://fixture.trycloudflare.com/api/health')
            req = urllib.request.Request(base + '/api/predict', data=b'original-image', headers={'Content-Type': 'image/jpeg', 'Origin': base})
            with client.open(req) as response:
                self.assertEqual(response.status, 200)
            self.assertEqual(calls[-1].data, b'original-image')
            before = len(calls)
            for path, headers in [('/api/predict', {'Origin':'https://untrusted.example'}), ('/api/unknown', {})]:
                with self.assertRaises(urllib.error.HTTPError):
                    client.open(urllib.request.Request(base + path, data=b'x', headers=headers))
            self.assertEqual(len(calls), before)
        finally:
            server.shutdown(); server.server_close(); worker.join()


if __name__ == '__main__':
    unittest.main()
