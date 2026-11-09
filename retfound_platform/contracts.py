"""Framework-independent persisted contracts."""
from dataclasses import asdict, dataclass

SCHEMA_VERSION = 'retfound-evaluation/1'


@dataclass
class ImageRecord:
    path: str
    split: str
    true_grade: int
    image_sha256: str
    width: int
    height: int

    def to_dict(self) -> dict:
        return asdict(self)
