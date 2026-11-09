import base64
import hashlib
import io
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from retfound_platform.contracts import SCHEMA_VERSION
from retfound_platform.datasets.labels import GRADES
from retfound_platform.datasets.manifests import write_json, digest
from retfound_platform.datasets.sampling import sample
from retfound_platform.datasets.sources import LocalSource
from retfound_platform.datasets.validation import audit, decode
from retfound_platform.inference.predictor import Predictor
from .metrics import metrics
from .reports import write_reports


def evaluate(source_path: Path, output: Path, count: int = 1000,
             seed: int = 20261023, device: str = 'auto', checkpoint: Path | None = None) -> dict:
    """Fresh audit then immutable selection and real model predictions."""
    output.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    try:
        print('Validating all source splits...', flush=True)
        evidence = audit(source_path)
        write_json(output / 'audit.json', evidence)
        selection = sample(evidence, count, seed)
        write_json(output / 'selection.json', selection)
        print(f'Loading model for {count} selected test images...', flush=True)
        predictor = Predictor(device, checkpoint)
        records = []
        with LocalSource(source_path) as source:
            if source.archive and digest(source.root) != evidence['source']['archive_sha256']:
                raise ValueError('Archive changed after audit')
            for index, selected in enumerate(selection['records']):
                payload = source.read(selected['path'])
                if hashlib.sha256(payload).hexdigest() != selected['image_sha256']:
                    raise ValueError(f'Source changed after audit: {selected["path"]}')
                prediction = predictor.predict(payload)
                with decode(payload) as image:
                    image.thumbnail((480, 360))
                    buffer = io.BytesIO()
                    image.save(buffer, format='JPEG', quality=83)
                row = {**selected, **prediction, 'dataset': evidence['dataset'],
                       'archive_path': selected['path'], 'true_label': GRADES[selected['true_grade']],
                       'correct': selected['true_grade'] == prediction['predicted_grade'],
                       'thumbnail': 'data:image/jpeg;base64,' + base64.b64encode(buffer.getvalue()).decode('ascii')}
                records.append(row)
                print(f'{index + 1}/{count} true={row["true_grade"]} predicted={row["predicted_grade"]} {row["path"]}', flush=True)
        summary = metrics(records)
        report = {
            'schema_version': SCHEMA_VERSION, 'run_id': output.name,
            'created_utc': datetime.now(timezone.utc).isoformat(),
            'seed': seed, 'audit_id': evidence['audit_id'], 'selection_id': selection['selection_id'],
            'model': 'RETFound MAE ViT-Large / APTOS2019 fine-tuned, five DR grades',
            **predictor.metadata, 'torch': predictor.metadata['packages']['torch'],
            'interpreter': sys.executable, 'grades': GRADES,
            'elapsed_seconds': time.perf_counter() - started,
            'preprocessing': 'RGB; bicubic shorter-edge resize 256; center crop 224; ImageNet normalization.',
            'sampling': f'Uniform without replacement from {len(evidence["eligible"])} eligible test images; seed {seed}. See audit.json and selection.json.',
            'evaluation': 'APTOS within-dataset evaluation. True labels come from supplied class folders. Any DR = predicted grade > 0.',
            'limitations': f'Research evaluation, not clinical diagnosis. Uncalibrated model scores. Exact-overlap completeness: {evidence["checks"]["exact_overlap"]}; known overlaps excluded. Patient/near-duplicate and checkpoint training-split independence unverified. Source issues: {len(evidence["issues"])}.',
            'checks': evidence['checks'], 'duplicate_image_count': 0,
            'sources': [{'dataset': 'APTOS2019', 'source': '#method', 'test_pool_size': len(evidence['eligible'])}],
            'source_identity': evidence['source'], 'local_source_path': evidence['local_source_path'],
            'metrics': {'All': summary, 'APTOS2019': summary}, 'records': records,
        }
        write_reports(output, report)
        write_json(output / 'completed.json', {'status': 'completed', 'count': count, 'accuracy': summary['accuracy']})
        return report
    except Exception as exc:
        write_json(output / 'failed.json', {'status': 'failed', 'type': type(exc).__name__, 'message': str(exc)})
        raise
