"""Adapt the established offline gallery without changing historical templates."""
import csv
import io
import json
from pathlib import Path

from retfound_platform.config import ROOT
from retfound_platform.datasets.manifests import write_json, write_text


def write_reports(output: Path, report: dict) -> None:
    structured = {**report, 'records': [{k: v for k, v in r.items() if k != 'thumbnail'} for r in report['records']]}
    write_json(output / 'predictions.json', structured)
    fields = ['dataset', 'archive_path', 'true_grade', 'true_label', 'predicted_grade',
              'predicted_label', 'correct', 'top_score', 'image_sha256', *[f'score_{i}' for i in range(5)]]
    buffer = io.StringIO(newline='')
    writer = csv.DictWriter(buffer, fieldnames=fields)
    writer.writeheader()
    for record in report['records']:
        row = {key: record.get(key) for key in fields}
        row.update({f'score_{i}': value for i, value in enumerate(record['scores'])})
        # Prevent spreadsheet formulas from source-controlled filenames.
        row['archive_path'] = "'" + row['archive_path'] if row['archive_path'].startswith(('=', '+', '-', '@')) else row['archive_path']
        writer.writerow(row)
    write_text(output / 'predictions.csv', buffer.getvalue())
    template = (ROOT / 'benchmark_report.html').read_text(encoding='utf-8')
    n = len(report['records'])
    template = template.replace('100-image DR evaluation', f'{n}-image APTOS evaluation')
    template = template.replace('One model. Three DR datasets.', 'APTOS 2019 · Evaluation results')
    template = template.replace('100 test images', f'{n} test images')
    template = template.replace('34 APTOS · 33 IDRiD · 33 MESSIDOR2', f'{n} APTOS test images')
    template = template.replace('Official RETFound test splits', 'Locally audited test split')
    template = template.replace('Official test split samples', 'Audited test selection')
    template = template.replace("const names={All:'All datasets',APTOS2019:'APTOS 2019',IDRID:'IDRiD',MESSIDOR2:'MESSIDOR2'};", "const names={All:'All images',APTOS2019:'APTOS 2019'};")
    template = template.replace('m.macro_f1.toFixed(3)', "(m.macro_f1==null?'N/A':m.macro_f1.toFixed(3))")
    template = template.replace('retfound-100-predictions.csv', f'retfound-{n}-predictions.csv')
    template = template.replace('Ground truth is taken from the official test class folder.', 'Ground truth is taken from the supplied test class folder.')
    # Export all five scores from the browser as well as from the Python exporter.
    template = template.replace("'top_score','image_sha256'];", "'top_score','image_sha256','score_0','score_1','score_2','score_3','score_4'];")
    template = template.replace('fields.map(k=>r[k])', "fields.map(k=>k.startsWith('score_')?r.scores[Number(k.slice(6))]:r[k])")
    payload = json.dumps(report, allow_nan=False).replace('<', '\\u003c')
    write_text(output / 'index.html', template.replace('__REPORT_DATA__', payload))
