"""Disposable fixtures with normal inherited workspace permissions on Windows."""
import shutil
import uuid
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def fixture_directory():
    root = Path(__file__).resolve().parent
    path = root / ('fixture-' + uuid.uuid4().hex)
    path.mkdir()
    try:
        yield path
    finally:
        resolved = path.resolve()
        if resolved.parent != root or not resolved.name.startswith('fixture-'):
            raise ValueError('Fixture cleanup escaped the tests directory')
        shutil.rmtree(resolved)
