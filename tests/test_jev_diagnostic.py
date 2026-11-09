import contextlib
import importlib.util
import io
from pathlib import Path
import unittest
from unittest.mock import patch

from retfound_platform.inference.fundus_gate import GateUnavailable

spec = importlib.util.spec_from_file_location('diagnose_jev', Path(__file__).resolve().parents[1] / 'scripts/diagnose_jev.py')
diagnostic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(diagnostic)


class DiagnosticTests(unittest.TestCase):
    def test_bad_key_is_rejected_before_network(self):
        with patch.object(diagnostic.sys, 'argv', ['diagnose_jev']), patch.dict(
                diagnostic.os.environ, {'OPENROUTER_API_KEY': 'Bearer bad-key'}), patch.object(
                diagnostic, 'FundusGate') as factory, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(diagnostic.main(), 1)
            factory.assert_not_called()

    def test_auth_failure_prevents_billed_requests(self):
        with patch.object(diagnostic.sys, 'argv', ['diagnose_jev']), patch.dict(
                diagnostic.os.environ, {'OPENROUTER_API_KEY': 'sk-or-v1-' + '0' * 64}), patch.object(
                diagnostic, 'FundusGate') as factory, contextlib.redirect_stdout(io.StringIO()):
            factory.return_value.timeout = 90
            factory.return_value.check_authentication.side_effect = GateUnavailable('HTTP 400')
            self.assertEqual(diagnostic.main(), 1)
            factory.return_value._request_decision.assert_not_called()
            factory.return_value.classify.assert_not_called()

    def test_new_key_starts_server_with_tested_secret_only_in_environment(self):
        key = 'sk-or-v1-' + '0' * 64
        with patch.object(diagnostic.sys, 'argv', ['diagnose_jev', '--new-key', '--start-server']), patch.object(
                diagnostic.getpass, 'getpass', return_value=key), patch.object(
                diagnostic, 'FundusGate') as factory, patch.object(
                diagnostic.subprocess, 'call', return_value=0) as launch, contextlib.redirect_stdout(io.StringIO()):
            factory.return_value.timeout = 90
            factory.return_value._request_decision.return_value = 1
            factory.return_value.classify.return_value = 1
            self.assertEqual(diagnostic.main(), 0)
            self.assertEqual(factory.call_args.args[0], key)
            self.assertEqual(launch.call_args.kwargs['env']['OPENROUTER_API_KEY'], key)
            self.assertNotIn(key, ' '.join(launch.call_args.args[0]))

    def test_text_failure_skips_image_and_redacts_key(self):
        output = io.StringIO()
        with patch.object(diagnostic.sys, 'argv', ['diagnose_jev']), patch.dict(
                diagnostic.os.environ, {'OPENROUTER_API_KEY': ('sk-or-v1-' + '0' * 64)}), patch.object(
                diagnostic, 'FundusGate') as factory, contextlib.redirect_stdout(output):
            factory.return_value.timeout = 90
            factory.return_value._request_decision.side_effect = GateUnavailable('Timed out')
            self.assertEqual(diagnostic.main(), 1)
            factory.return_value.classify.assert_not_called()
        self.assertIn('TEXT FAILED', output.getvalue())
        self.assertNotIn(('sk-or-v1-' + '0' * 64), output.getvalue())

    def test_text_and_image_success_are_reported_separately(self):
        output = io.StringIO()
        with patch.object(diagnostic.sys, 'argv', ['diagnose_jev']), patch.dict(
                diagnostic.os.environ, {'OPENROUTER_API_KEY': ('sk-or-v1-' + '0' * 64)}), patch.object(
                diagnostic, 'FundusGate') as factory, contextlib.redirect_stdout(output):
            factory.return_value.timeout = 90
            factory.return_value._request_decision.return_value = 1
            factory.return_value.classify.return_value = 0
            self.assertEqual(diagnostic.main(), 0)
            factory.return_value.classify.assert_called_once()
        self.assertIn('Fundus decision: 0', output.getvalue())
        self.assertNotIn(('sk-or-v1-' + '0' * 64), output.getvalue())
