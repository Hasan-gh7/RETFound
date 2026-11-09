"""Trusted local demonstration manifest, with no model or network activity."""
import hashlib
import json
from pathlib import Path
import re

from .uploads import MAX_UPLOAD_BYTES, UploadError

LABELS = ['No DR', 'Mild', 'Moderate', 'Severe', 'Proliferative']


class DemoSamples:
    def __init__(self, root: Path):
        self.root = root.resolve()

    def catalog(self) -> list[dict]:
        try:
            manifest = self.root / 'manifest.json'
            if manifest.stat().st_size > 128 * 1024:
                raise ValueError('Manifest too large')
            data = json.loads(manifest.read_text(encoding='utf-8'))
            if data['schema_version'] != 'retfound-upload-demo/1' or len(data['records']) != 15:
                raise ValueError('Unexpected demo schema or count')
            rows = []
            ids, hashes = set(), set()
            for record in data['records']:
                dataset, grade = record['dataset'], record['true_grade']
                if dataset not in {'IDRID', 'MESSIDOR2', 'DDR'} or type(grade) is not int or grade not in range(5):
                    raise ValueError('Invalid dataset or label')
                if record['split'] != 'test' or record['true_label'] != LABELS[grade]:
                    raise ValueError('Invalid reference mapping')
                path = Path(record['path'])
                resolved = (self.root / path).resolve()
                image_root = (self.root / 'images').resolve()
                if path.is_absolute() or not resolved.is_relative_to(image_root) or not image_root.is_relative_to(self.root):
                    raise ValueError('Unsafe image path')
                sample_id = f'{dataset}-{grade}'
                digest = record['sha256']
                if sample_id in ids or digest in hashes or not re.fullmatch('[a-f0-9]{64}', digest):
                    raise ValueError('Duplicate or invalid manifest identity')
                ids.add(sample_id)
                hashes.add(digest)
                rows.append({'id': sample_id, 'dataset': dataset, 'true_grade': grade,
                             'true_label': LABELS[grade], 'sha256': digest, 'split': 'test',
                             'source': record['source'], 'representation': record['representation'],
                             'path': path.as_posix(), 'image_url': f'/api/demo/{sample_id}/image',
                             'thumbnail_url': f'/api/demo/{sample_id}/thumbnail'})
            return sorted(rows, key=lambda row: (row['dataset'], row['true_grade']))
        except (OSError, ValueError, KeyError, TypeError):
            raise UploadError(503, 'demo_unavailable', 'The labeled demo manifest is missing or invalid.') from None

    def load(self, sample_id: str) -> tuple[dict, bytes]:
        row = next((row for row in self.catalog() if row['id'] == sample_id), None)
        if row is None:
            raise UploadError(404, 'demo_sample_not_found', 'Unknown demonstration sample.')
        try:
            with (self.root / row['path']).open('rb') as file:
                payload = file.read(MAX_UPLOAD_BYTES + 1)
        except OSError:
            raise UploadError(503, 'demo_unavailable', 'The demonstration image is unavailable.') from None
        if len(payload) > MAX_UPLOAD_BYTES or hashlib.sha256(payload).hexdigest() != row['sha256']:
            raise UploadError(409, 'demo_image_changed', 'The demo image differs from its recorded hash. No inference was run.')
        return row, payload
