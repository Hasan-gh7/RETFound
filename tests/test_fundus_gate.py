import io
import base64
import json
import unittest
import urllib.error
import os
from unittest.mock import Mock, MagicMock, patch

from PIL import Image
from retfound_platform.inference.fundus_gate import FundusGate, GateUnavailable, ENDPOINT, _validation_detail


class FundusGateTests(unittest.TestCase):
    def test_key_check_uses_get_without_model_or_image(self):
        with patch('urllib.request.build_opener') as build:
            response = build.return_value.open.return_value.__enter__.return_value
            response.read.return_value = b'{"data":{"is_management_key":false}}'
            FundusGate('secret').check_authentication()
            request = build.return_value.open.call_args.args[0]
            self.assertEqual(request.full_url, 'https://openrouter.ai/api/v1/key')
            self.assertEqual(request.get_method(), 'GET')
            self.assertIsNone(request.data)
            response.read.return_value = b'{"data":{"is_management_key":true}}'
            with self.assertRaisesRegex(GateUnavailable, 'management'):
                FundusGate('secret').check_authentication()

    def test_control_characters_in_key_block_network(self):
        with patch('urllib.request.build_opener') as build:
            with self.assertRaisesRegex(GateUnavailable, 'control characters'):
                FundusGate('secret\x00').classify(self.image())
            build.assert_not_called()

    def test_validation_error_shapes_and_html_do_not_hide_details(self):
        for value in [
            {'error': {'message': 'Invalid model'}},
            {'error': 'Invalid model'},
            {'message': 'Invalid model'},
            {'detail': [{'msg': 'Invalid model'}]},
        ]:
            with self.subTest(value=value):
                self.assertEqual(_validation_detail(json.dumps(value).encode(), 'secret'), 'Invalid model')
        self.assertEqual(_validation_detail(b'<title>Bad Request</title><body>secret</body>', 'secret'), 'Bad Request')
        self.assertEqual(_validation_detail(b'{"metadata":{"raw":"private"}}', 'secret'), '')

    def test_http_error_has_safe_diagnostic_when_message_is_missing(self):
        with patch('urllib.request.build_opener') as build:
            build.return_value.open.side_effect = urllib.error.HTTPError(
                ENDPOINT, 400, '', {'Content-Type': 'text/html'}, io.BytesIO(b'<title>Bad Request</title>'))
            with self.assertRaises(GateUnavailable) as caught:
                FundusGate('secret').classify(self.image())
            self.assertIn('Bad Request', str(caught.exception))
            self.assertIn('text/html', caught.exception.diagnostic)

    def test_configured_timeout_is_validated_and_sent(self):
        with patch.dict(os.environ, {'OPENROUTER_API_KEY': 'secret', 'JEV_TIMEOUT_SECONDS': '75'}):
            gate = FundusGate.from_environment()
        with patch('urllib.request.build_opener') as build:
            build.return_value.open.side_effect = TimeoutError('private')
            with self.assertRaises(GateUnavailable) as caught:
                gate.classify(self.image())
            self.assertEqual(build.return_value.open.call_args.kwargs['timeout'], 75)
            self.assertIn('response headers', str(caught.exception))
            self.assertNotIn('private', str(caught.exception))
        for value in (0, 91, float('nan'), float('inf')):
            with self.assertRaises(ValueError):
                FundusGate('secret', value)

    def test_response_body_timeout_is_distinguished(self):
        with patch('urllib.request.build_opener') as build:
            response = build.return_value.open.return_value.__enter__.return_value
            response.read.side_effect = TimeoutError('private')
            with self.assertRaises(GateUnavailable) as caught:
                FundusGate('secret').classify(self.image())
            self.assertIn('reading the response body', str(caught.exception))

    def image(self, fmt='PNG'):
        out = io.BytesIO()
        Image.new('RGB', (12, 12)).save(out, format=fmt)
        return out.getvalue()

    def test_missing_key_blocks_without_network(self):
        with patch('urllib.request.build_opener') as opener:
            with self.assertRaises(GateUnavailable):
                FundusGate('').classify(self.image())
            opener.assert_not_called()

    def test_http_contract_and_strict_binary(self):
        for choice in ['0', '1', 'yes', 1, None]:
            with self.subTest(choice=choice), patch('urllib.request.build_opener', new_callable=MagicMock) as build:
                response = Mock()
                response.read.return_value = json.dumps({'answers': {'retinal_fundus': {'type': 'choice', 'choice': choice}}}).encode()
                build.return_value.open.return_value.__enter__.return_value = response
                gate = FundusGate('test-secret')
                if choice in ('0', '1'):
                    self.assertEqual(gate.classify(self.image('BMP')), int(choice))
                else:
                    with self.assertRaises(GateUnavailable):
                        gate.classify(self.image())
                request = build.return_value.open.call_args.args[0]
                self.assertEqual(request.full_url, ENDPOINT)
                self.assertEqual(request.get_header('Authorization'), 'Bearer test-secret')
                body = json.loads(request.data)
                self.assertTrue(body['state'][0]['image_url']['url'].startswith('data:image/'))

    def test_network_and_malformed_response_are_redacted(self):
        for failure in [TimeoutError('private'), ValueError('private')]:
            with patch('urllib.request.build_opener', new_callable=MagicMock) as build:
                build.return_value.open.side_effect = failure
                with self.assertRaises(GateUnavailable) as caught:
                    FundusGate('secret').classify(self.image())
                self.assertNotIn('private', str(caught.exception))

    def test_provider_errors_identify_cause_without_leaking_body(self):
        for status in (400, 401, 402, 403, 404, 413, 422, 429, 503):
            with self.subTest(status=status), patch('urllib.request.build_opener') as build:
                build.return_value.open.side_effect = urllib.error.HTTPError(
                    ENDPOINT, status, 'private-secret', {}, io.BytesIO(b'private-secret'))
                with self.assertRaises(GateUnavailable) as caught:
                    FundusGate('private-secret').classify(self.image())
                self.assertIn(str(status), str(caught.exception))
                self.assertNotIn('private-secret', str(caught.exception))

    def test_network_failure_has_actionable_message(self):
        with patch('urllib.request.build_opener') as build:
            build.return_value.open.side_effect = urllib.error.URLError('private-details')
            with self.assertRaises(GateUnavailable) as caught:
                FundusGate('secret').classify(self.image())
            self.assertIn('could not connect', str(caught.exception))
            self.assertNotIn('private-details', str(caught.exception))

    def test_remote_copy_meets_jev_dimensions(self):
        for size in [(4288, 2848), (12, 12), (256, 256), (256, 1568)]:
            with self.subTest(size=size), patch('urllib.request.build_opener') as build:
                image = io.BytesIO()
                Image.new('RGB', size).save(image, 'JPEG')
                response = Mock()
                response.read.return_value = b'{"answers":{"retinal_fundus":{"type":"choice","choice":"1"}}}'
                build.return_value.open.return_value.__enter__.return_value = response
                self.assertEqual(FundusGate('secret').classify(image.getvalue()), 1)
                body = json.loads(build.return_value.open.call_args.args[0].data)
                data = body['state'][0]['image_url']['url'].split(',', 1)[1]
                with Image.open(io.BytesIO(base64.b64decode(data))) as remote:
                    self.assertTrue(all(256 <= side <= 1568 for side in remote.size))
                    self.assertGreaterEqual(remote.width * remote.height, 78400)

    def test_validation_detail_redacts_key_and_image(self):
        with patch('urllib.request.build_opener') as build:
            body = json.dumps({'error': {'message': 'Bad dimensions secret data:image/jpeg;base64,' + 'A' * 100}}).encode()
            build.return_value.open.side_effect = urllib.error.HTTPError(ENDPOINT, 400, '', {}, io.BytesIO(body))
            with self.assertRaises(GateUnavailable) as caught:
                FundusGate('secret').classify(self.image())
            self.assertIn('Bad dimensions', str(caught.exception))
            self.assertNotIn('secret', str(caught.exception))
            self.assertNotIn('A' * 100, str(caught.exception))
