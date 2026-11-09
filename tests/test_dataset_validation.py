import io
import tempfile
import unittest
import warnings
import zipfile
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from retfound_platform.datasets.labels import CLASS_MAP, identity
from retfound_platform.datasets.sources import LocalSource, safe_path
from retfound_platform.datasets.validation import audit, decode
from retfound_platform.datasets.manifests import write_json
from tests.fixtures import fixture_directory


def png(color: int) -> bytes:
    stream = io.BytesIO()
    Image.new('RGB', (12, 10), (color, 5, 10)).save(stream, format='PNG')
    return stream.getvalue()


class DatasetTests(unittest.TestCase):
    def setUp(self):
        self.temp = fixture_directory()
        self.root = self.temp.__enter__()
        self.addCleanup(self.temp.__exit__, None, None, None)

    def archive(self, members):
        path = self.root / 'source.zip'
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', UserWarning)
            with zipfile.ZipFile(path, 'w') as archive:
                for name, payload in members:
                    archive.writestr(name, payload)
        return path

    def test_aliases_and_invalid_labels(self):
        for name, grade in CLASS_MAP.items():
            self.assertEqual(identity(f'APTOS/test/{name}/a.png'), ('test', grade))
        for name in ['test/unknown/a.png', 'test/1/nested/a.png', '1/a.png', 'train/test/0/a.png']:
            with self.assertRaises(ValueError):
                identity(name)

    def test_overlap_conflicts_duplicates_corruption(self):
        source = self.archive([
            ('data/train/0/train.png', png(1)), ('data/val/0/val.png', png(2)),
            ('data/test/0/overlap.png', png(1)),
            ('data/test/1/conflict_a.png', png(3)), ('data/test/2/conflict_b.png', png(3)),
            ('data/test/0/keep.png', png(4)), ('data/test/0/duplicate.png', png(4)),
            ('data/test/0/broken.png', b'invalid'),
            ('data/test/.ipynb_checkpoints/hidden.png', b'ignored'),
            ('__MACOSX/test/0/a.png', b'ignored'),
        ])
        result = audit(source)
        self.assertEqual(len(result['eligible']), 1)
        self.assertEqual(result['eligible'][0]['path'], 'data/test/0/duplicate.png')
        self.assertIn('cross_split_exact_overlap', result['exclusions']['data/test/0/overlap.png'])
        self.assertIn('conflicting_labels', result['exclusions']['data/test/1/conflict_a.png'])
        self.assertEqual(len(result['issues']), 1)
        self.assertEqual(result['checks']['exact_overlap'], 'unverified')

    def test_complete_vs_test_only(self):
        path = self.archive([(f'{s}/0/a.png', png(i)) for i, s in enumerate(['train', 'val', 'test'])])
        self.assertEqual(audit(path)['checks']['exact_overlap'], 'complete')
        path = self.archive([('test/0/a.png', png(1))])
        self.assertEqual(audit(path)['checks']['exact_overlap'], 'unverified')

    def test_unsafe_duplicate_and_symlink_members(self):
        path = self.archive([('../test/0/a.png', png(0)), ('test/0/b.png', png(1)), ('test/0/b.png', png(2))])
        with zipfile.ZipFile(path, 'a') as archive:
            link = zipfile.ZipInfo('test/0/link.png')
            link.create_system = 3
            link.external_attr = 0o120777 << 16
            archive.writestr(link, 'outside.png')
        result = audit(path)
        self.assertFalse(result['eligible'])
        self.assertEqual(len(result['issues']), 4)
        for name in ['/a.png', 'C:/a.png', 'a\\b.png', 'a/../b.png', 'a//b.png']:
            with self.assertRaises(ValueError):
                safe_path(name)

    def test_crc_error_recorded(self):
        path = self.archive([('test/0/a.png', png(2))])
        with patch.object(LocalSource, 'read', side_effect=zipfile.BadZipFile('Bad CRC')):
            result = audit(path)
        self.assertFalse(result['eligible'])
        self.assertIn('Bad CRC', result['issues'][0]['reason'])

    def test_folder_and_zip_match(self):
        folder = self.root / 'folder'
        path = folder / 'test/2/image.png'
        path.parent.mkdir(parents=True)
        path.write_bytes(png(20))
        archive = self.archive([('test/2/image.png', png(20))])
        self.assertEqual(audit(folder)['eligible'], audit(archive)['eligible'])

    def test_limits_and_invalid_image(self):
        with self.assertRaises(OSError):
            decode(b'not an image')
        with patch('retfound_platform.datasets.validation.MAX_IMAGE_PIXELS', 10):
            with self.assertRaisesRegex(ValueError, 'pixel limit'):
                decode(png(1))
        path = self.archive([('test/0/a.png', png(1))])
        with patch('retfound_platform.datasets.sources.MAX_IMAGE_BYTES', 10):
            self.assertFalse(audit(path)['eligible'])

    def test_no_output_overwrite(self):
        path = self.root / 'audit.json'
        write_json(path, {'first': 1})
        with self.assertRaises(FileExistsError):
            write_json(path, {'second': 2})
        self.assertIn('first', path.read_text())
