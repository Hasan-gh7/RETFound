"""Download exactly five labeled test examples per requested Hugging Face source.

Explicit network command only. No model inference or imports with side effects.
"""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import html
import io
import json
from pathlib import Path
import re
from urllib.parse import quote, urlparse

from PIL import Image
import requests

ROOT = Path(__file__).resolve().parents[1]
GRADES = ['No DR', 'Mild', 'Moderate', 'Severe', 'Proliferative']
ANSWER_MAP = {'A: No DR': 0, 'B: Mild DR': 1, 'C: Moderate DR': 2,
              'D: Severe DR': 3, 'E: Proliferative DR': 4}
IDRID_NAMES = ['a_noDR', 'b_mildDR', 'c_moderateDR', 'd_severeDR', 'e_proDR']


def fetch(session, url, limit=20 * 1024 * 1024):
    with session.get(url, stream=True, timeout=(15, 60)) as response:
        response.raise_for_status()
        result = bytearray()
        for chunk in response.iter_content(65536):
            result.extend(chunk)
            if len(result) > limit:
                raise ValueError('Download exceeds configured resource limit')
        return bytes(result)


def select_rows(rows, dataset):
    selected = {}
    for item in sorted(rows, key=lambda item: item['row_idx']):
        row = item['row']
        if item.get('truncated_cells'):
            raise ValueError('Truncated dataset viewer row')
        if dataset == 'IDRID':
            grade = row['label']
            if type(grade) is not int or grade not in range(5):
                raise ValueError('Unknown IDRiD label')
        else:
            if row['options'] != list(ANSWER_MAP) or row['answer'] not in ANSWER_MAP:
                raise ValueError('Unknown Messidor2 answer mapping')
            grade = ANSWER_MAP[row['answer']]
        selected.setdefault(grade, item)
    if set(selected) != set(range(5)):
        raise ValueError('Insufficient test examples for all five grades')
    return selected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'upload_test_images/huggingface15-20261030')
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    metadata = output / 'source_metadata'
    metadata.mkdir()
    session = requests.Session()
    session.headers['User-Agent'] = 'RETFound-labeled-upload-demo/1.0'
    records = []
    for dataset, repo in [('IDRID', 'amin-nejad/idrid-disease-grading'), ('MESSIDOR2', 'OctoMed/Messidor2')]:
        print(f'{dataset}: reading labeled test rows', flush=True)
        endpoint = 'https://datasets-server.huggingface.co/rows'
        url = requests.Request('GET', endpoint, params={'dataset': repo, 'config': 'default', 'split': 'test', 'offset': 0, 'length': 100}).prepare().url
        data = json.loads(fetch(session, url, 32 * 1024 * 1024))
        if dataset == 'IDRID':
            feature = next(f for f in data['features'] if f['name'] == 'label')
            if feature['type'].get('names') != IDRID_NAMES:
                raise ValueError('IDRiD feature mapping changed')
        chosen = select_rows(data['rows'], dataset)
        evidence = {'repo': repo, 'split': 'test', 'rows_endpoint': url,
                    'features': data['features'], 'test_rows': data['num_rows_total'], 'selected': []}
        for grade, item in sorted(chosen.items()):
            row = item['row']
            asset = row['image']['src']
            parsed = urlparse(asset)
            if parsed.scheme != 'https' or parsed.hostname != 'datasets-server.huggingface.co':
                raise ValueError('Unexpected viewer image host')
            revision = re.search(r'/--/([a-f0-9]{40})/--/', parsed.path)
            if revision is None:
                raise ValueError('Missing viewer asset revision')
            record = {'dataset': dataset, 'repo': repo, 'split': 'test', 'true_grade': grade,
                      'true_label': GRADES[grade], 'source_label': row.get('label', row.get('answer')),
                      'row_index': item['row_idx'], 'revision': revision.group(1),
                      'source': f'https://huggingface.co/datasets/{repo}/viewer/default/test?row={item["row_idx"]}',
                      'asset_path': parsed.path, 'representation': 'Hugging Face viewer-exported image; original embedded byte equivalence unverified',
                      'source_image_hash': row.get('image_hash')}
            save_image(output, record, fetch(session, asset), records)
            evidence['selected'].append({k: v for k, v in record.items() if k != 'sha256'})
        (metadata / f'{dataset}.json').write_text(json.dumps(evidence, indent=2), encoding='utf-8')

    repo = 'ctmedtech/DDR-dataset'
    info = json.loads(fetch(session, f'https://huggingface.co/api/datasets/{repo}', 8 * 1024 * 1024))
    revision = info['sha']
    base = f'https://huggingface.co/datasets/{repo}/resolve/{revision}/'
    label_bytes = fetch(session, base + 'DR_grading/test.txt', 2 * 1024 * 1024)
    (metadata / 'DDR_test_labels.txt').write_bytes(label_bytes)
    readme = fetch(session, base + 'README.md', 2 * 1024 * 1024)
    (metadata / 'DDR_source_README.md').write_bytes(readme)
    labels = {}
    for line in label_bytes.decode('utf-8-sig').splitlines():
        name, grade = line.split()
        if Path(name).name != name or re.fullmatch(r'[A-Za-z0-9_.-]+', name) is None:
            raise ValueError('Unsafe DDR image filename')
        if name in labels:
            raise ValueError('Duplicate DDR label filename')
        if grade not in {'0', '1', '2', '3', '4', '5'}:
            raise ValueError('Unknown DDR label')
        labels[name] = int(grade)
    # DDR may contain label 5 (ungradable). Never map it into five-grade DR.
    for grade in range(5):
        names = sorted(name for name, label in labels.items() if label == grade)
        if not names:
            raise ValueError('Insufficient DDR grade examples')
        name = names[0]
        member = 'DR_grading/test/' + name
        source = base + quote(member)
        record = {'dataset': 'DDR', 'repo': repo, 'split': 'test', 'true_grade': grade,
                  'true_label': GRADES[grade], 'source_label': grade, 'source_filename': name,
                  'source': source, 'revision': revision, 'representation': 'Repository image bytes',
                  'label_source': 'DR_grading/test.txt', 'label_file_sha256': hashlib.sha256(label_bytes).hexdigest()}
        save_image(output, record, fetch(session, source), records)
    if len(records) != 15 or len({r['sha256'] for r in records}) != 15:
        raise ValueError('Wrong image count or duplicate bytes across selected examples')
    manifest = {'schema_version': 'retfound-upload-demo/1', 'created_utc': datetime.now(timezone.utc).isoformat(),
        'purpose': 'Balanced manual upload demonstration; not a representative evaluation sample',
        'selection': 'IDRID and MESSIDOR2: lowest row index per grade in first 100 test rows; DDR: lexicographically first test-label filename per grade. No randomness or replacement.',
        'class_mapping': dict(enumerate(GRADES)), 'checks': {'selected_exact_byte_duplicates': 0,
        'decode': 'all 15 passed', 'train_val_test_overlap': 'unverified', 'patient_overlap': 'unverified',
        'near_duplicates': 'unverified', 'checkpoint_training_independence': 'unverified'},
        'label_note': 'Dataset-supplied reference labels, not predictions or independently reviewed clinical diagnoses. Messidor2 uses answer, not generated responses.',
        'inference_run': False, 'records': records}
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    fields = ['path', 'dataset', 'true_grade', 'true_label', 'predicted_grade', 'matches_true_grade', 'jev_decision', 'split', 'source', 'sha256']
    with (output / 'comparison.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(records)
    rows = ''.join('<tr><td>' + html.escape(r['dataset']) + '</td><td><a href="' + r['path'] + '">' + html.escape(Path(r['path']).name) + '</a></td><td>' + str(r['true_grade']) + ' ' + html.escape(r['true_label']) + '</td><td><img src="' + r['path'] + '" width="180" alt="Fundus example"></td></tr>' for r in records)
    (output / 'labels.html').write_text('<!doctype html><meta charset="utf-8"><title>Labeled fundus upload examples</title><style>body{font:16px Arial;margin:40px}td,th{border:1px solid #ccc;padding:12px}table{border-collapse:collapse}img{height:120px;object-fit:contain}</style><h1>15 labeled upload examples</h1><p>Five test images per dataset, one for each grade. Reference labels come from the source datasets. No inference has been run. This is a balanced demonstration, not an accuracy benchmark.</p><p>Upload image files from images. Record your model output in comparison.csv. Jev decision 0 is a rejection; DR grade 0 means No DR. They are different values.</p><table><tr><th>Dataset</th><th>Upload file</th><th>Reference label</th><th>Preview</th></tr>'+rows+'</table>', encoding='utf-8')
    (output / 'README.md').write_text('# Labeled upload demonstration\n\nOpen labels.html for thumbnails and reference labels. Upload files from images/IDRID, images/MESSIDOR2 and images/DDR. Each has exactly five images, one per grade 0..4. comparison.csv has empty prediction, agreement and Jev-decision columns for your results.\n\nLabels come from the supplied Hugging Face test data: IDRiD ClassLabel, Messidor2 answer field (never responses), DDR test.txt. See manifest.json for exact source/revision/hash and representation. Viewer-exported IDRiD/Messidor2 bytes may differ from original embedded images; dimensions and bytes are preserved as downloaded, with no local resizing/re-encoding. DDR uses pinned repository image bytes.\n\nSelection is deterministic first-per-grade, not a random or representative evaluation. No Jev or RETFound predictions were executed. Full split, patient, near-duplicate and checkpoint-training overlap checks remain unverified. Grade 5 DDR rows, if present, are excluded rather than mapped. Only selected-set exact-byte uniqueness and decoding are checked. Dataset labels are reference labels, not an independent clinical review.\n\nSources: https://huggingface.co/datasets/amin-nejad/idrid-disease-grading ; https://huggingface.co/datasets/OctoMed/Messidor2 ; https://huggingface.co/datasets/ctmedtech/DDR-dataset . Preserve source attribution and check the respective dataset terms for further use.\n', encoding='utf-8')
    (output / 'completed.json').write_text(json.dumps({'status': 'completed', 'images': 15, 'per_dataset': 5, 'inference_run': False}, indent=2), encoding='utf-8')
    print(f'Completed: {output}', flush=True)


def save_image(output, record, payload, records):
    with Image.open(io.BytesIO(payload)) as image:
        if image.width * image.height > 40_000_000 or getattr(image, 'n_frames', 1) != 1:
            raise ValueError('Unsupported image size/frame count')
        image.load()
        if image.format not in {'JPEG', 'PNG'}:
            raise ValueError('Unexpected source image encoding')
        suffix = '.jpg' if image.format == 'JPEG' else '.png'
        record.update(width=image.width, height=image.height, encoding=image.format)
    path = Path('images') / record['dataset'] / f'{record["dataset"]}_true{record["true_grade"]}_{record["true_label"].replace(" ", "_")}{suffix}'
    target = output / path
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('xb') as f:
        f.write(payload)
    record.update(path=path.as_posix(), sha256=hashlib.sha256(payload).hexdigest(), bytes=len(payload))
    records.append(record)
    print(f'Saved {path.as_posix()} | grade {record["true_grade"]} | {record["width"]}x{record["height"]}', flush=True)


if __name__ == '__main__':
    main()
