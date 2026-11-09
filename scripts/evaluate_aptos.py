"""Audit, sample, evaluate and export an offline ground-truth/prediction viewer."""
import argparse
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from retfound_platform.config import DEFAULT_RUNS


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path, help='Explicit local ZIP or split/grade/image folder root')
    parser.add_argument('--count', type=int, default=1000)
    parser.add_argument('--seed', type=int, default=20261023)
    parser.add_argument('--device', choices=['auto', 'cuda', 'cpu', 'mps'], default='auto')
    parser.add_argument('--checkpoint', type=Path, help='Trusted local classifier checkpoint only')
    parser.add_argument('--output', type=Path, help='New directory; existing outputs are never replaced')
    parser.add_argument('--open-report', action='store_true', help='Open completed report in the default browser')
    args = parser.parse_args()
    if args.count < 1:
        parser.error('--count must be positive')
    output = args.output or DEFAULT_RUNS / ('aptos-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:8])
    from retfound_platform.evaluation.runner import evaluate
    try:
        report = evaluate(args.source, output, args.count, args.seed, args.device, args.checkpoint)
    except (ValueError, OSError) as exc:
        parser.exit(2, f'Evaluation stopped: {exc}\nRun directory: {output}\n')
    result = report['metrics']['All']
    print(f'Completed: {result["correct"]}/{result["n"]} correct ({result["accuracy"]:.2%})')
    print(f'Open report: {(output / "index.html").resolve()}')
    if args.open_report:
        import webbrowser
        webbrowser.open((output / 'index.html').resolve().as_uri())


if __name__ == '__main__':
    main()
