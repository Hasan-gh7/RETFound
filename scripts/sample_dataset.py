import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from retfound_platform.datasets.sampling import sample
from retfound_platform.datasets.manifests import write_json


def main() -> None:
    parser = argparse.ArgumentParser(description='Select reproducible test images from an audit.')
    parser.add_argument('audit', type=Path)
    parser.add_argument('--count', type=int, default=1000)
    parser.add_argument('--seed', type=int, default=20261023)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        result = sample(json.loads(args.audit.read_text(encoding='utf-8')), args.count, args.seed)
    except ValueError as exc:
        parser.exit(2, f'{exc}\n')
    write_json(args.output, result)
    print(f'Selected {result["selected_count"]} images: {args.output}')


if __name__ == '__main__':
    main()
