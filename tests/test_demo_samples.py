import copy
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from retfound_platform.api.demo_samples import DemoSamples
from retfound_platform.api.uploads import UploadError

ROOT = Path(__file__).resolve().parents[1] / 'upload_test_images/huggingface15-20261030'


class DemoSamplesTests(unittest.TestCase):
    def test_label_and_path_tampering_is_rejected(self):
        original = json.loads((ROOT / 'manifest.json').read_text())
        for key, value in [('true_grade', 5), ('true_label', 'Wrong'), ('path', '../../README.md'), ('split', 'train')]:
            data = copy.deepcopy(original)
            data['records'][0][key] = value
            with patch.object(Path, 'read_text', return_value=json.dumps(data)):
                with self.assertRaises(UploadError):
                    DemoSamples(ROOT).catalog()

    def test_changed_image_bytes_are_blocked(self):
        samples = DemoSamples(ROOT)
        row = samples.catalog()[0]
        with patch.object(samples, 'catalog', return_value=[row]), patch.object(Path, 'open', return_value=io.BytesIO(b'changed')):
            with self.assertRaises(UploadError) as caught:
                samples.load(row['id'])
            self.assertEqual(caught.exception.status, 409)
