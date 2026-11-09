"""Synthetic label-selection checks; no network or clinical predictions."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('prepare_upload_demo', Path(__file__).resolve().parents[1] / 'scripts/prepare_upload_demo.py')
demo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(demo)


class UploadDemoTests(unittest.TestCase):
    def test_idrid_selects_each_grade_in_stable_order(self):
        rows = [{'row_idx': i, 'row': {'label': i}, 'truncated_cells': []} for i in range(5)]
        rows.append({'row_idx': 20, 'row': {'label': 0}})
        chosen = demo.select_rows(list(reversed(rows)), 'IDRID')
        self.assertEqual([chosen[i]['row_idx'] for i in range(5)], list(range(5)))

    def test_missing_or_unknown_label_blocks_selection(self):
        for labels in ([0, 1, 2, 3], [0, 1, 2, 3, 5], [False, 1, 2, 3, 4]):
            with self.assertRaises(ValueError):
                demo.select_rows([{'row_idx': i, 'row': {'label': label}} for i, label in enumerate(labels)], 'IDRID')

    def test_messidor_uses_reference_answer_not_generated_response(self):
        rows = [{'row_idx': i, 'row': {'answer': label, 'options': list(demo.ANSWER_MAP),
                                     'responses': ['Wrong answer A: No DR']}} for i, label in enumerate(demo.ANSWER_MAP)]
        chosen = demo.select_rows(rows, 'MESSIDOR2')
        self.assertEqual(chosen[4]['row']['answer'], 'E: Proliferative DR')
        rows[0]['row']['answer'] = 'Unknown'
        with self.assertRaises(ValueError):
            demo.select_rows(rows, 'MESSIDOR2')
