import unittest

from retfound_platform.datasets.sampling import sample


class SamplingTests(unittest.TestCase):
    def fixture(self, n=981):
        return {'audit_id': 'fixture', 'dataset': 'synthetic', 'eligible': [
            {'path': f'test/{i % 5}/{i:04}.png', 'image_sha256': str(i), 'split': 'test', 'true_grade': i % 5}
            for i in range(n)]}

    def test_stable_without_replacement(self):
        source = self.fixture()
        first = sample(source, 100)
        source['eligible'].reverse()
        self.assertEqual(first, sample(source, 100))
        self.assertEqual(len({r['image_sha256'] for r in first['records']}), 100)
        self.assertNotEqual(first['records'], sample(source, 100, 42)['records'])

    def test_shortage_never_filled(self):
        with self.assertRaisesRegex(ValueError, 'only 981'):
            sample(self.fixture(), 1000)

    def test_invalid_count_or_split(self):
        for value in [0, -1, True, 1.5]:
            with self.assertRaises(ValueError):
                sample(self.fixture(), value)
        source = self.fixture(1)
        source['eligible'][0]['split'] = 'train'
        with self.assertRaises(ValueError):
            sample(source, 1)

    def test_reject_duplicate_selection_input(self):
        source = self.fixture(1)
        source['eligible'] *= 2
        with self.assertRaises(ValueError):
            sample(source, 1)
