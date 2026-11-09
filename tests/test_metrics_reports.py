import csv
import json
import tempfile
import unittest
from pathlib import Path

from retfound_platform.config import ROOT
from retfound_platform.evaluation.metrics import metrics
from retfound_platform.evaluation.reports import write_reports
from tests.fixtures import fixture_directory


class MetricsTests(unittest.TestCase):
    def test_any_dr_sensitivity_specificity_use_argmax_grade(self):
        # DR grade errors still count as binary true positives when both exceed 0.
        rows = [{'true_grade': t, 'predicted_grade': p}
                for t, p in [(0, 0), (0, 0), (0, 1), (1, 2), (4, 3), (2, 0)]]
        result = metrics(rows)
        self.assertEqual(result['binary']['tp'], 2)
        self.assertEqual(result['binary']['fn'], 1)
        self.assertEqual(result['binary']['tn'], 2)
        self.assertEqual(result['binary']['fp'], 1)
        self.assertAlmostEqual(result['binary']['sensitivity'], 2 / 3)
        self.assertAlmostEqual(result['binary']['specificity'], 2 / 3)
        self.assertNotEqual(result['accuracy'], result['binary']['sensitivity'])

    def test_absent_reference_classes_are_undefined(self):
        positives = metrics([{'true_grade': 2, 'predicted_grade': 0}])
        self.assertEqual(positives['binary']['sensitivity'], 0)
        self.assertIsNone(positives['binary']['specificity'])
        self.assertIn('specificity', positives['undefined_reasons'])
        empty = metrics([])
        self.assertIsNone(empty['binary']['sensitivity'])
        self.assertIsNone(empty['binary']['specificity'])
        json.dumps([positives, empty], allow_nan=False)

    def test_empty_and_single_class(self):
        empty = metrics([])
        self.assertIsNone(empty['accuracy'])
        self.assertEqual(empty['confusion'], [[0] * 5 for _ in range(5)])
        single = metrics([{'true_grade': 0, 'predicted_grade': 0}])
        self.assertEqual(single['macro_f1'], .2)
        self.assertIsNone(single['quadratic_kappa'])
        self.assertIsNone(single['binary']['sensitivity'])
        json.dumps([empty, single], allow_nan=False)

    def test_saved_legacy_metric_parity(self):
        saved = json.loads((ROOT / 'results/benchmark100/predictions.json').read_text(encoding='utf-8'))
        for name, expected in saved['metrics'].items():
            records = saved['records'] if name == 'All' else [r for r in saved['records'] if r['dataset'] == name]
            actual = metrics(records)
            for key, value in expected.items():
                self.assertEqual(actual[key], value, (name, key))

    def test_invalid_grade(self):
        with self.assertRaises(ValueError):
            metrics([{'true_grade': -1, 'predicted_grade': 0}])

    def test_report_export_counts_and_escaping(self):
        # Artifact-format fixture only; these are historical predictions, not a new run.
        saved = json.loads((ROOT / 'results/benchmark100/predictions.json').read_text(encoding='utf-8'))
        saved['records'] = [r for r in saved['records'] if r['dataset'] == 'APTOS2019']
        saved['records'][0]['archive_path'] = '</script><script>alert(1)</script>'
        saved['metrics'] = {'All': metrics(saved['records']), 'APTOS2019': metrics(saved['records'])}
        with fixture_directory() as folder:
            output = Path(folder)
            write_reports(output, saved)
            html = (output / 'index.html').read_text(encoding='utf-8')
            payload = html.split('<script id="report-data" type="application/json">')[1].split('</script>')[0]
            self.assertEqual(len(json.loads(payload)['records']), 34)
            self.assertNotIn('</script><script>alert', html)
            self.assertNotIn("IDRID:'IDRiD'", html)
            with (output / 'predictions.csv').open(encoding='utf-8', newline='') as stream:
                rows = list(csv.DictReader(stream))
            self.assertEqual(len(rows), 34)
            self.assertIn('score_4', rows[0])
