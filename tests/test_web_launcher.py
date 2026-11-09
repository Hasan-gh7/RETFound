import contextlib
import io
import sys
import threading
import time
import unittest
import urllib.request
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from serve_web import main, reserve_port, running_model


class LauncherTests(unittest.TestCase):
    def test_uvicorn_serves_using_reserved_socket(self):
        import uvicorn
        async def tiny_app(scope, receive, send):
            await send({'type': 'http.response.start', 'status': 200, 'headers': []})
            await send({'type': 'http.response.body', 'body': b'reserved socket ready'})
        with reserve_port(0) as listener:
            port = listener.getsockname()[1]
            server = uvicorn.Server(uvicorn.Config(tiny_app, lifespan='off', log_level='critical'))
            worker = threading.Thread(target=server.run, kwargs={'sockets': [listener]}, daemon=True)
            worker.start()
            try:
                for _ in range(100):
                    if server.started:
                        break
                    time.sleep(.01)
                self.assertTrue(server.started)
                opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
                with opener.open(f'http://127.0.0.1:{port}', timeout=2) as response:
                    self.assertEqual(response.read(), b'reserved socket ready')
            finally:
                server.should_exit = True
                worker.join(timeout=5)
            self.assertFalse(worker.is_alive())

    def test_reserved_port_rejects_second_launch_before_listening(self):
        with reserve_port(0) as first:
            port = first.getsockname()[1]
            with self.assertRaises(OSError):
                reserve_port(port)

    def test_ready_server_is_reused_before_model_import(self):
        with patch('sys.argv', ['serve_web.py', '--open-browser']), \
             patch('serve_web.reserve_port', side_effect=OSError('in use')), \
             patch('serve_web.running_model', return_value={'device': 'cuda'}), \
             patch('serve_web.webbrowser.open') as browser, \
             patch.dict(sys.modules, {'uvicorn': None}), \
             contextlib.redirect_stdout(io.StringIO()) as output:
            main()
        browser.assert_called_once_with('http://127.0.0.1:8000')
        self.assertIn('no second model was loaded', output.getvalue())

    def test_unknown_port_owner_is_not_reused(self):
        with patch('sys.argv', ['serve_web.py']), \
             patch('serve_web.reserve_port', side_effect=OSError('in use')), \
             patch('serve_web.running_model', return_value=None), \
             patch('serve_web.webbrowser.open') as browser, \
             contextlib.redirect_stderr(io.StringIO()) as output:
            with self.assertRaises(SystemExit) as raised:
                main()
        self.assertEqual(raised.exception.code, 2)
        browser.assert_not_called()
        self.assertIn('No process was stopped', output.getvalue())
