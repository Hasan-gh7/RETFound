import random

from retfound_platform.contracts import SCHEMA_VERSION
from .manifests import fingerprint


def sample(audit: dict, count: int, seed: int = 20261023) -> dict:
    if isinstance(count, bool) or not isinstance(count, int) or count < 1:
        raise ValueError('Requested count must be a positive integer')
    candidates = sorted(audit['eligible'], key=lambda row: row['path'])
    if len({r['path'] for r in candidates}) != len(candidates) or len({r['image_sha256'] for r in candidates}) != len(candidates):
        raise ValueError('Eligible manifest contains duplicate paths or image hashes')
    if any(r['split'] != 'test' or type(r['true_grade']) is not int or r['true_grade'] not in range(5) for r in candidates):
        raise ValueError('Only labeled test images may be sampled')
    if count > len(candidates):
        raise ValueError(f'Requested {count} test images, but only {len(candidates)} are eligible. '
                         'No duplicates or train/validation images will be used to fill the shortage.')
    selected = sorted(random.Random(seed).sample(candidates, count), key=lambda row: row['path'])
    result = {'schema_version': SCHEMA_VERSION, 'audit_id': audit['audit_id'],
              'dataset': audit['dataset'], 'method': 'uniform_without_replacement',
              'seed': seed, 'requested_count': count, 'selected_count': len(selected),
              'records': selected}
    result['selection_id'] = fingerprint(result)
    return result
