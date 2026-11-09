"""Select workspace-only API dependencies without modifying the Conda environment."""
import sys
from pathlib import Path


def configure() -> Path:
    root = Path(__file__).resolve().parents[1]
    dependencies = root / '.runtime/web'
    sys.path.insert(0, str(root))
    if dependencies.is_dir():
        sys.path.insert(0, str(dependencies))
    return root
