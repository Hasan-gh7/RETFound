import hashlib
import io
import warnings
import zipfile
import zlib
from collections import Counter, defaultdict
from pathlib import Path

from PIL import Image

from retfound_platform.config import MAX_IMAGE_PIXELS
from retfound_platform.contracts import ImageRecord, SCHEMA_VERSION
from .labels import CLASS_MAP, identity
from .manifests import fingerprint, digest
from .sources import LocalSource


def decode(payload: bytes) -> Image.Image:
    with warnings.catch_warnings():
        warnings.simplefilter('error', Image.DecompressionBombWarning)
        with Image.open(io.BytesIO(payload)) as image:
            if image.width * image.height > MAX_IMAGE_PIXELS:
                raise ValueError('Image exceeds pixel limit')
            if getattr(image, 'n_frames', 1) != 1:
                raise ValueError('Multi-frame images are unsupported')
            image.load()
            return image.convert('RGB')


def audit(root: Path, dataset: str = 'APTOS2019') -> dict:
    records, issues = [], []
    hashes: dict[str, list] = defaultdict(list)
    seen_splits: set[str] = set()
    with LocalSource(root) as source:
        issues.extend(source.issues)
        for name in sorted(source.entries):
            try:
                split, grade = identity(name)
                seen_splits.add(split)
                payload = source.read(name)
                image_hash = hashlib.sha256(payload).hexdigest()
                # Keep byte-hash evidence even if decoding subsequently fails.
                evidence = {'path': name, 'split': split, 'true_grade': grade,
                            'image_sha256': image_hash}
                hashes[image_hash].append(evidence)
                with decode(payload) as image:
                    records.append(ImageRecord(name, split, grade, image_hash,
                                               image.width, image.height).to_dict())
            except (ValueError, OSError, RuntimeError, EOFError, KeyError,
                    zipfile.BadZipFile, zlib.error,
                    Image.DecompressionBombError, Image.DecompressionBombWarning) as exc:
                issues.append({'path': name, 'reason': f'{type(exc).__name__}: {exc}'})
        kind = source.kind
        source_path = str(source.root)
        archive_hash = digest(source.root) if source.archive else None
    excluded: dict[str, list[str]] = defaultdict(list)
    duplicates, overlap = [], []
    for image_hash, rows in sorted(hashes.items()):
        if len(rows) > 1:
            duplicates.append({'sha256': image_hash, 'paths': [r['path'] for r in rows]})
        if len({r['true_grade'] for r in rows}) > 1:
            for row in rows:
                excluded[row['path']].append('conflicting_labels')
        if len({r['split'] for r in rows}) > 1:
            overlap.append({'sha256': image_hash, 'paths': [r['path'] for r in rows]})
            for row in rows:
                if row['split'] == 'test':
                    excluded[row['path']].append('cross_split_exact_overlap')
    # Deduplicate only decoded, otherwise-eligible test images in stable path order.
    seen_test = set()
    for row in records:
        if row['split'] == 'test' and not excluded.get(row['path']):
            if row['image_sha256'] in seen_test:
                excluded[row['path']].append('same_label_exact_duplicate')
            else:
                seen_test.add(row['image_sha256'])
    eligible = [r for r in records if r['split'] == 'test' and not excluded.get(r['path'])]
    # Any unreadable/ambiguous evidence means a complete overlap check is unverified.
    complete = seen_splits == {'train', 'val', 'test'} and not issues
    result = {
        'schema_version': SCHEMA_VERSION, 'dataset': dataset,
        'source': {'kind': kind, 'archive_sha256': archive_hash},
        'class_mapping': CLASS_MAP, 'records': records, 'issues': issues,
        'duplicate_groups': duplicates, 'cross_split_groups': overlap,
        'exclusions': dict(excluded), 'eligible': eligible,
        'counts': {'decoded': dict(Counter(r['split'] for r in records)),
                   'eligible_test': len(eligible), 'issues': len(issues)},
        'checks': {'exact_overlap': 'complete' if complete else 'unverified',
                   'exact_overlap_detail': 'All readable recognized splits compared; unreadable or missing evidence prevents completeness.',
                   'splits_seen': sorted(seen_splits), 'patient_overlap': 'unverified',
                   'near_duplicates': 'unverified', 'checkpoint_split_identity': 'unverified'},
    }
    result['audit_id'] = fingerprint(result)
    result['local_source_path'] = source_path
    return result
