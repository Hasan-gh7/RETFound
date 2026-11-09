import hashlib
import io
import json
import unittest

from PIL import Image

from retfound_platform.config import ROOT
from retfound_platform.datasets.manifests import write_json
from retfound_platform.inference.input_validation import RetinalInputPolicy, review_record
from tests.fixtures import fixture_directory


class InputPolicyTests(unittest.TestCase):
    def test_only_exact_reference_bytes_are_accepted(self):
        original = (ROOT / 'sample_images/idrid_test.jpg').read_bytes()
        policy = RetinalInputPolicy.load()
        self.assertEqual(policy.assess(original).status, 'trusted_reference')
        with Image.open(io.BytesIO(original)) as image:
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
        self.assertFalse(policy.assess(buffer.getvalue()).accepted)

    def test_user_reported_window_is_not_a_reference(self):
        policy = RetinalInputPolicy.load()
        self.assertNotIn('291671d62e36123d6894df9f6ed1f3f0fcc395b69f04204eb585c48ebecb8399', policy.references)

    def test_human_review_applies_to_exact_bytes_and_can_be_revoked(self):
        # This uses a real fundus sample with an empty reference list, so it exercises
        # the human-review branch without pretending the test performs modality review.
        payload = (ROOT / 'sample_images/idrid_test.jpg').read_bytes()
        with fixture_directory() as directory:
            policy = RetinalInputPolicy({}, directory)
            self.assertFalse(policy.assess(payload).accepted)
            record = review_record(payload, 'Fixture reviewer', 'Fixture only: known local fundus sample')
            path = directory / (record['image_sha256'] + '.json')
            write_json(path, record)
            self.assertEqual(policy.assess(payload).status, 'human_reviewed')
            self.assertFalse(policy.assess(payload + b'changed').accepted)
            path.unlink()
            self.assertFalse(policy.assess(payload).accepted)

    def test_invalid_review_fails_closed(self):
        payload = b'fixture'
        with fixture_directory() as directory:
            write_json(directory / (hashlib.sha256(payload).hexdigest() + '.json'), {'reviewed_as_color_fundus': True})
            with self.assertRaises(ValueError):
                RetinalInputPolicy({}, directory).assess(payload)

    def test_review_requires_decode_reviewer_and_note(self):
        with self.assertRaises(OSError):
            review_record(b'not-image', 'Reviewer', 'Reviewed')
        with self.assertRaises(ValueError):
            review_record(b'', '', 'Reviewed')

    def test_missing_or_malformed_reference_registry_does_not_allow_inputs(self):
        with fixture_directory() as directory:
            with self.assertRaises(FileNotFoundError):
                RetinalInputPolicy.load(directory / 'absent.json')
            path = directory / 'bad.json'
            write_json(path, {'schema_version': 'unsupported', 'references': {}})
            with self.assertRaises(ValueError):
                RetinalInputPolicy.load(path)
