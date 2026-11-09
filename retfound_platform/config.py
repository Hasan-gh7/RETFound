from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUNS = ROOT / 'results' / 'runs'
MAX_IMAGE_BYTES = 64 * 1024 * 1024
MAX_IMAGE_PIXELS = 40_000_000
MAX_SOURCE_FILES = 100_000
MAX_SOURCE_BYTES = 50 * 1024**3
