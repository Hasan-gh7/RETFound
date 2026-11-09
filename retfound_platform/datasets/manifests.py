import hashlib
import json
import os
import uuid
from pathlib import Path


def fingerprint(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False,
                                     separators=(',', ':')).encode('utf-8')).hexdigest()


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            result.update(block)
    return result.hexdigest()


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, allow_nan=False))


def write_text(path: Path, value: str) -> None:
    """Publish a complete file without replacing an existing artifact."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    try:
        temporary.write_text(value, encoding='utf-8', newline='')
        # A hard link is atomic and fails if the destination already exists.
        os.link(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)
