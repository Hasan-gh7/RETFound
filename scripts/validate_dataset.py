"""Validate a local labeled ZIP/folder without modifying the source."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from retfound_platform.datasets.validation import audit
from retfound_platform.datasets.manifests import write_json


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    result = audit(args.source)
    write_json(args.output, result)
    print(json.dumps({'counts': result['counts'], 'checks': result['checks'],
                      'audit': str(args.output)}, indent=2))


if __name__ == '__main__':
    main()
