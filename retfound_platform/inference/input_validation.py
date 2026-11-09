"""Fail-closed input provenance gate, NOT an automatic retina detector.

Only exact bytes from trusted retinal references or a local human review may
reach DR grading. Unknown inputs abstain, including genuine unseen fundus images.
"""
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

from retfound_platform.config import ROOT

POLICY_VERSION = 'retfound-reviewed-input-v1'
REGISTRY_SCHEMA = 'retfound-retinal-references/1'
REVIEW_SCHEMA = 'retfound-retinal-review/1'
REFERENCES = Path(__file__).with_name('retinal_references.json')
REVIEWS = ROOT / '.runtime' / 'retinal_reviews'
LIMITATION = 'Exact reference match or human review only; no automatic retina or image-quality detector.'


@dataclass(frozen=True)
class InputDecision:
    status: str
    image_sha256: str
    basis: str | None = None
    policy_version: str = POLICY_VERSION
    limitation: str = LIMITATION

    @property
    def accepted(self) -> bool:
        return self.status in ('trusted_reference', 'human_reviewed')

    def to_dict(self) -> dict:
        return asdict(self)


class RetinalInputPolicy:
    def __init__(self, references: dict[str, str], review_directory: Path = REVIEWS):
        if any(not re.fullmatch('[0-9a-f]{64}', key) or not value for key, value in references.items()):
            raise ValueError('Invalid retinal reference registry')
        self.references = dict(references)
        self.review_directory = review_directory

    @classmethod
    def load(cls, path: Path = REFERENCES, review_directory: Path = REVIEWS):
        registry = json.loads(path.read_text(encoding='utf-8'))
        if registry.get('schema_version') != REGISTRY_SCHEMA:
            raise ValueError('Unsupported retinal reference registry')
        return cls(registry['references'], review_directory)

    def assess(self, payload: bytes) -> InputDecision:
        image_hash = hashlib.sha256(payload).hexdigest()
        if image_hash in self.references:
            return InputDecision('trusted_reference', image_hash, self.references[image_hash])
        approval = self.review_directory / f'{image_hash}.json'
        if approval.is_file():
            review = json.loads(approval.read_text(encoding='utf-8'))
            if (review.get('schema_version') == REVIEW_SCHEMA
                    and review.get('image_sha256') == image_hash
                    and review.get('reviewed_as_color_fundus') is True
                    and isinstance(review.get('reviewer'), str) and review['reviewer'].strip()
                    and isinstance(review.get('note'), str) and review['note'].strip()):
                return InputDecision('human_reviewed', image_hash, 'local-human-review')
            raise ValueError('Invalid local retinal review record')
        return InputDecision('unverified', image_hash)


def review_record(payload: bytes, reviewer: str, note: str) -> dict:
    from datetime import datetime, timezone
    from retfound_platform.datasets.validation import decode
    if not reviewer.strip() or not note.strip():
        raise ValueError('A named reviewer and review note are required')
    # This only checks decoding. The person making this record supplies modality review.
    with decode(payload):
        pass
    return {'schema_version': REVIEW_SCHEMA, 'image_sha256': hashlib.sha256(payload).hexdigest(),
            'reviewed_as_color_fundus': True, 'reviewer': reviewer.strip(), 'note': note.strip(),
            'created_utc': datetime.now(timezone.utc).isoformat(),
            'limitation': 'Human modality review; not clinical validation or image-quality certification.'}
