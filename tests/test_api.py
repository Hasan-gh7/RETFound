"""Synthetic API contract tests. FakePredictor is never used by the application."""
import asyncio
import hashlib
import io
import threading
import unittest
from unittest.mock import Mock
from retfound_platform.inference.fundus_gate import GateUnavailable
from unittest.mock import patch

try:
    import fastapi
except ImportError as exc:
    raise unittest.SkipTest('Run scripts/test_web.py with the isolated API dependencies') from exc

import httpx
from PIL import Image

from retfound_platform.api.app import Settings, create_app
from retfound_platform.api.uploads import MAX_REQUEST_BYTES, UploadError, extract_image


def image_bytes(fmt='PNG'):
    payload = io.BytesIO()
    Image.new('RGB', (18, 20), (40, 90, 80)).save(payload, format=fmt)
    return payload.getvalue()


class FakePredictor:
    def __init__(self):
        self.metadata = {'device': 'cpu', 'dtype': 'float32', 'checkpoint_sha256': 'synthetic-test-only',
                         'preprocessing_version': 'synthetic-test-only'}
        self.calls = 0
        self.started = threading.Event()
        self.block = None
        self.fail = False

    def predict(self, payload):
        self.calls += 1
        self.started.set()
        if self.block:
            self.block.wait(5)
        if self.fail:
            raise RuntimeError('Synthetic failure with private server details')
        return {'predicted_grade': 0, 'predicted_label': 'No DR', 'scores': [.6, .1, .1, .1, .1],
                'top_score': .6, 'image_sha256': hashlib.sha256(payload).hexdigest()}


class APITests(unittest.IsolatedAsyncioTestCase):
    async def test_summary_and_thumbnail_contract(self):
        response = await self.client.post('/api/predict/summary', content=image_bytes(), headers={'Content-Type': 'image/png'})
        self.assertEqual(response.status_code, 200, response.text)
        result = response.json()
        self.assertEqual(set(result), {'predicted_grade', 'predicted_label', 'class_scores_percent'})
        self.assertEqual([row['score'] for row in result['class_scores_percent']], [60, 10, 10, 10, 10])
        self.assertEqual([row['grade'] for row in result['class_scores_percent']], list(range(5)))
        self.gate.classify.return_value = 0
        rejected = await self.client.post('/api/predict/summary', content=image_bytes(), headers={'Content-Type': 'image/png'})
        self.assertEqual(rejected.status_code, 422)
        self.assertIsNone(rejected.json()['prediction'])
        self.assertEqual(rejected.json()['error']['code'], 'not_retinal_fundus')
        self.assertIn('قاع العين', rejected.json()['error']['message'])
        self.assertEqual(self.fake.calls, 1, 'Jev rejection must not run RETFound')
        count = self.fake.calls
        preview = await self.client.get('/api/demo/DDR-0/thumbnail')
        self.assertEqual(preview.status_code, 200)
        with Image.open(io.BytesIO(preview.content)) as image:
            self.assertLessEqual(max(image.size), 320)
        self.assertEqual(self.fake.calls, count)
        self.assertEqual((await self.client.get('/api/demo/unknown/thumbnail')).status_code, 404)

    async def test_complete_public_demo(self):
        key = 'x' * 40
        app = create_app(Settings(public_api=True, public_demo=True, api_key=key), lambda device: self.fake, gate=self.gate)
        async with app.router.lifespan_context(app):
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://localhost') as client:
                for path in ('/', '/app.js', '/styles.css', '/input-validation.css', '/demo-auth.js', '/dataset-tests', '/dataset-tests.js'):
                    response = await client.get(path)
                    self.assertEqual(response.status_code, 200)
                    self.assertNotIn(key, response.text)
                self.assertEqual((await client.get('/api/demo')).status_code, 401)
                client.headers.update({'Authorization': 'Bearer ' + key, 'Origin': 'https://demo.trycloudflare.com'})
                for path in ('/api/demo', '/api/demo/DDR-0/image', '/api/example', '/api/evaluation', '/openapi.json'):
                    self.assertEqual((await client.get(path)).status_code, 200, path)
                response = await client.post('/api/demo/DDR-0/predict')
                self.assertEqual(response.status_code, 200, response.text)
                self.assertEqual(self.fake.calls, 1)
                self.assertEqual((await client.get('/api/unknown')).status_code, 404)

    async def test_public_api_authentication_routes_and_rate_limit(self):
        key = 'synthetic-access-key-' + 'x' * 32
        app = create_app(Settings(public_api=True, api_key=key), lambda device: self.fake, gate=self.gate)
        async with app.router.lifespan_context(app):
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://localhost') as client:
                for path in ('/api/health', '/api/model', '/', '/openapi.json'):
                    response = await client.get(path)
                    self.assertEqual(response.status_code, 401)
                for path in ('/external-demo', '/external-demo.js'):
                    response = await client.get(path)
                    self.assertEqual(response.status_code, 200)
                    self.assertNotIn(key, response.text)
                denied = await client.post('/api/predict', content=image_bytes(), headers={'Authorization': 'Bearer wrong'})
                self.assertEqual(denied.status_code, 401)
                self.gate.classify.assert_not_called()
                self.assertEqual(self.fake.calls, 0)
                client.headers['Authorization'] = 'Bearer ' + key
                client.headers['Origin'] = 'https://trial.trycloudflare.com'
                self.assertEqual((await client.get('/api/health')).status_code, 200)
                self.assertEqual((await client.get('/api/model')).status_code, 200)
                for path in ('/', '/openapi.json', '/api/demo', '/api/evaluation'):
                    self.assertEqual((await client.get(path)).status_code, 404)
                blocked = await client.post('/api/demo/DDR-4/predict')
                self.assertEqual(blocked.status_code, 404)
                for index in range(10):
                    response = await client.post('/api/predict/summary' if index == 0 else '/api/predict', content=image_bytes(), headers={'Content-Type': 'image/png'})
                    self.assertEqual(response.status_code, 200, response.text)
                response = await client.post('/api/predict', content=image_bytes(), headers={'Content-Type': 'image/png'})
                self.assertEqual(response.status_code, 429)
                self.assertEqual(self.fake.calls, 10)
                self.assertEqual(self.gate.classify.call_count, 10)
                self.assertEqual(response.headers['Retry-After'], '60')

    async def test_public_api_rejects_missing_key(self):
        with self.assertRaises(ValueError):
            create_app(Settings(public_api=True), lambda device: self.fake, gate=self.gate)

    async def asyncSetUp(self):
        self.fake = FakePredictor()
        self.loads = 0
        def factory(device):
            self.loads += 1
            return self.fake
        self.gate = Mock()
        self.gate.classify.return_value = 1
        self.app = create_app(Settings(capacity=1, allowed_origins=('http://localhost:3000',)), factory, gate=self.gate)
        self.assertEqual(self.loads, 0)
        self.lifespan = self.app.router.lifespan_context(self.app)
        await self.lifespan.__aenter__()
        self.client = httpx.AsyncClient(transport=httpx.ASGITransport(app=self.app), base_url='http://127.0.0.1')

    async def asyncTearDown(self):
        if self.fake.block:
            self.fake.block.set()
        await self.client.aclose()
        await self.lifespan.__aexit__(None, None, None)

    async def test_raw_and_multipart_share_contract_and_model(self):
        payload = image_bytes()
        first = await self.client.post('/api/predict', content=payload, headers={'Content-Type': 'image/png'})
        second = await self.client.post('/api/predict', files={'image': ('../../outside.png', payload, 'image/png')})
        self.assertEqual(first.status_code, 200, first.text)
        self.assertEqual(second.status_code, 200, second.text)
        result = second.json()
        self.assertEqual(result['scores'], first.json()['scores'])
        self.assertEqual(result['image_sha256'], hashlib.sha256(payload).hexdigest())
        self.assertEqual(result['schema_version'], 'retfound-prediction/1')
        self.assertEqual(len(result['scores']), 5)
        self.assertEqual(self.loads, 1)
        self.assertEqual(self.fake.calls, 2)
        self.assertNotIn('checkpoint', result['model'])
        self.assertEqual(self.app.state.active, 0)

    async def test_demo_catalog_images_and_reference_comparison(self):
        catalog = await self.client.get('/api/demo')
        self.assertEqual(catalog.status_code, 200)
        self.assertEqual(len(catalog.json()['samples']), 15)
        self.assertEqual(self.fake.calls, 0)
        self.gate.classify.assert_not_called()
        image = await self.client.get('/api/demo/DDR-4/image')
        self.assertEqual(image.status_code, 200)
        response = await self.client.post('/api/demo/DDR-4/predict', json={'true_grade': 0})
        self.assertEqual(response.status_code, 200, response.text)
        result = response.json()
        self.assertEqual(result['reference']['true_grade'], 4)
        self.assertFalse(result['matches_true_grade'])
        self.assertEqual(result['prediction']['predicted_grade'], 0)
        self.assertEqual(result['prediction']['image_sha256'], hashlib.sha256(image.content).hexdigest())
        self.gate.classify.assert_called_once_with(image.content)
        for path, mime in [('/dataset-tests', 'text/html'), ('/dataset-tests.js', 'text/javascript'), ('/dataset-tests.css', 'text/css')]:
            asset = await self.client.get(path)
            self.assertEqual(asset.status_code, 200)
            self.assertTrue(asset.headers['content-type'].startswith(mime))

    async def test_demo_rejections_failures_and_unknown_id_block_prediction(self):
        for decision, status in [(0, 422), (GateUnavailable('Unavailable'), 503)]:
            self.gate.classify.side_effect = decision if isinstance(decision, Exception) else None
            self.gate.classify.return_value = decision
            response = await self.client.post('/api/demo/IDRID-0/predict')
            self.assertEqual(response.status_code, status, response.text)
            self.assertNotIn('matches_true_grade', response.json())
        response = await self.client.post('/api/demo/unknown/predict')
        self.assertEqual(response.status_code, 404)
        with patch('retfound_platform.api.app.DemoSamples.load', side_effect=UploadError(409, 'demo_image_changed', 'Changed')):
            response = await self.client.post('/api/demo/DDR-0/predict')
            self.assertEqual(response.status_code, 409)
        self.assertEqual(self.fake.calls, 0)
        self.assertEqual(self.app.state.active, 0)

    async def test_new_images_pass_gate_without_registry(self):
        # Synthetic fixtures test invocation, not real model accuracy.
        payload = image_bytes('JPEG')
        with patch('retfound_platform.inference.input_validation.RetinalInputPolicy.load',
                   side_effect=RuntimeError('Registry must not be used')):
            for kwargs in [
                {'content': payload, 'headers': {'Content-Type': 'image/jpeg'}},
                {'files': {'image': ('new-image.jpg', payload, 'image/jpeg')}},
            ]:
                response = await self.client.post('/api/predict', **kwargs)
                self.assertEqual(response.status_code, 200, response.text)
                result = response.json()
                self.assertEqual(result['input_validation']['status'], 'accepted')
                self.assertEqual(result['image_sha256'], hashlib.sha256(payload).hexdigest())
                self.assertEqual(result['model']['input_policy'], 'jev-fundus-choice-v1')
                self.assertTrue(result['model']['automatic_retina_detection'])
                self.assertEqual(len(result['scores']), 5)
        self.assertEqual(self.fake.calls, 2)
        self.assertEqual(self.app.state.active, 0)

    async def test_gate_rejection_and_failure_never_call_retFound(self):
        for multipart in (False, True):
            for outcome, status in [(0, 422), (GateUnavailable('Unavailable'), 503), ('1', 503)]:
                self.gate.classify.side_effect = outcome if isinstance(outcome, Exception) else None
                self.gate.classify.return_value = outcome
                kwargs = {'files': {'image': ('retina.png', image_bytes(), 'image/png')}} if multipart else {'content': image_bytes(), 'headers': {'Content-Type': 'image/png'}}
                response = await self.client.post('/api/predict', **kwargs)
                self.assertEqual(response.status_code, status, response.text)
                self.assertNotIn('scores', response.json())
                if status == 422:
                    self.assertEqual(response.json()['input_validation']['decision'], 0)
        self.assertEqual(self.fake.calls, 0)

    async def test_bad_images_rejected_before_model(self):
        for payload, media, status in [(b'bad', 'image/png', 422), (b'', 'image/png', 422),
                                       (b'{}', 'application/json', 415), (image_bytes('GIF'), 'image/png', 422)]:
            response = await self.client.post('/api/predict', content=payload, headers={'Content-Type': media})
            self.assertEqual(response.status_code, status, response.text)
            self.assertIn('message', response.json()['error'])
        self.assertEqual(self.fake.calls, 0)

    async def test_multipart_requires_one_named_image(self):
        payload = image_bytes()
        wrong = await self.client.post('/api/predict', files={'file': ('a.png', payload)})
        many = await self.client.post('/api/predict', files=[('image', ('a.png', payload)), ('image', ('b.png', payload))])
        broken = await self.client.post('/api/predict', content=b'--abc', headers={'Content-Type': 'multipart/form-data; boundary=abc'})
        for response in [wrong, many, broken]:
            self.assertIn(response.status_code, [400, 422])
        self.assertEqual(self.fake.calls, 0)

    async def test_size_limit_with_header_and_chunked_body(self):
        response = await self.client.post('/api/predict', content=b'x', headers={'Content-Type': 'image/png', 'Content-Length': str(MAX_REQUEST_BYTES + 1)})
        self.assertEqual(response.status_code, 413)
        async def chunks():
            for _ in range(22):
                yield b'x' * 1024 * 1024
        response = await self.client.post('/api/predict', content=chunks(), headers={'Content-Type': 'image/png'})
        self.assertEqual(response.status_code, 413)
        self.assertEqual(self.fake.calls, 0)

    async def test_busy_capacity_and_health_remain_responsive(self):
        self.fake.block = threading.Event()
        pending = asyncio.create_task(self.client.post('/api/predict', content=image_bytes(), headers={'Content-Type': 'image/png'}))
        await asyncio.to_thread(self.fake.started.wait, 3)
        try:
            health = await asyncio.wait_for(self.client.get('/api/health'), 1)
            self.assertEqual(health.status_code, 200)
            self.assertEqual(health.json()['active_requests'], 1)
            busy = await self.client.post('/api/predict', content=image_bytes(), headers={'Content-Type': 'image/png'})
            self.assertEqual(busy.status_code, 429)
            self.assertEqual(busy.headers['retry-after'], '2')
        finally:
            self.fake.block.set()
            self.assertEqual((await pending).status_code, 200)
        self.assertEqual(self.app.state.active, 0)

    async def test_cancelled_client_reserves_slot_until_model_finishes(self):
        self.fake.block = threading.Event()
        pending = asyncio.create_task(self.client.post('/api/predict', content=image_bytes(), headers={'Content-Type': 'image/png'}))
        await asyncio.to_thread(self.fake.started.wait, 3)
        pending.cancel()
        try:
            await pending
        except asyncio.CancelledError:
            pass
        self.assertEqual(self.app.state.active, 1)
        self.fake.block.set()
        for _ in range(100):
            if self.app.state.active == 0:
                break
            await asyncio.sleep(.01)
        self.assertEqual(self.app.state.active, 0)

    async def test_inference_failure_does_not_leak_details_or_hold_slot(self):
        self.fake.fail = True
        with self.assertLogs('retfound_platform.api.app', level='ERROR'):
            response = await self.client.post('/api/predict', content=image_bytes(), headers={'Content-Type': 'image/png'})
        self.assertEqual(response.status_code, 500)
        self.assertNotIn('private server details', response.text)
        self.assertEqual(self.app.state.active, 0)

    async def test_explicit_cors_and_local_host(self):
        denied = await self.client.post('/api/predict', content=image_bytes(), headers={'Content-Type': 'image/png', 'Origin': 'https://untrusted.example'})
        self.assertEqual(denied.status_code, 403)
        allowed = await self.client.post('/api/predict', content=image_bytes(), headers={'Content-Type': 'image/png', 'Origin': 'http://localhost:3000'})
        self.assertEqual(allowed.status_code, 200)
        self.assertEqual(allowed.headers['access-control-allow-origin'], 'http://localhost:3000')
        host = await self.client.get('/api/health', headers={'Host': 'untrusted.example'})
        self.assertEqual(host.status_code, 400)

    async def test_ui_and_schema_and_no_filesystem_escape(self):
        page = await self.client.get('/')
        self.assertEqual(page.status_code, 200)
        self.assertIn('Every image tells a story.', page.text)
        self.assertIn("default-src 'self'", page.headers['content-security-policy'])
        schema = (await self.client.get('/openapi.json')).json()
        self.assertIn('multipart/form-data', schema['paths']['/api/predict']['post']['requestBody']['content'])
        for path in ['/AGENTS.md', '/checkpoints/checkpoints/APTOS2019/checkpoint-best.pth', '/%2e%2e/AGENTS.md']:
            self.assertEqual((await self.client.get(path)).status_code, 404)

    async def test_asset_mime_types_ignore_windows_registry(self):
        # Reproduce the observed Windows mapping that blocked browser modules.
        with patch('mimetypes.guess_type', return_value=('text/plain', None)):
            for path, expected in [('/app.js', 'text/javascript'), ('/styles.css', 'text/css'),
                                   ('/favicon.svg', 'image/svg+xml')]:
                response = await self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.headers['content-type'].split(';')[0], expected)
                self.assertEqual(response.headers['x-content-type-options'], 'nosniff')


class UploadTests(unittest.TestCase):
    def test_missing_or_incomplete_boundary(self):
        for media, body in [('multipart/form-data', b'x'), ('multipart/form-data; boundary=abc', b'--abc\r\n')]:
            with self.assertRaises(UploadError):
                extract_image(body, media)

    def test_explicit_settings_validation(self):
        for settings in [Settings(capacity=0), Settings(allowed_origins=('*',))]:
            with self.assertRaises(ValueError):
                create_app(settings)
