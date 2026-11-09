"""Opt-in real-checkpoint verification; no training and no source modification."""
import argparse
import gc
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import torch
from retfound_platform.config import ROOT
from retfound_platform.inference.predictor import Predictor
from retfound_platform.datasets.manifests import write_json


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    service = Predictor('cuda')
    sample = (ROOT / 'sample_images/idrid_test.jpg').read_bytes()
    cuda = service.predict(sample)
    # Values printed by the unchanged baseline CLI, independently run on this image.
    if [f'{s * 100:.2f}' for s in cuda['scores']] != ['79.68', '9.80', '6.66', '1.79', '2.08']:
        raise ValueError('Prediction differs from baseline CLI rounded scores')
    saved = json.loads((ROOT / 'results/benchmark100/predictions.json').read_text(encoding='utf-8'))
    differences = []
    for row in saved['records']:
        if row['dataset'] != 'APTOS2019':
            continue
        actual = service.predict((ROOT / row['path']).read_bytes())
        if actual['predicted_grade'] != row['predicted_grade']:
            raise ValueError('Historical prediction grade mismatch')
        differences.append(max(abs(a-b) for a, b in zip(actual['scores'], row['scores'])))
    if max(differences) > 1e-5:
        raise ValueError('Historical five-score parity exceeded 1e-5 tolerance')
    metadata = service.metadata
    del service
    gc.collect()
    torch.cuda.empty_cache()
    print('CUDA parity passed; checking CPU on one real image...', flush=True)
    cpu = Predictor('cpu').predict(sample)
    delta = max(abs(a-b) for a, b in zip(cpu['scores'], cuda['scores']))
    if cpu['predicted_grade'] != cuda['predicted_grade'] or delta > 1e-4:
        raise ValueError('CPU/CUDA score difference exceeded 1e-4 tolerance')
    result = {'metadata': metadata, 'baseline_cli_rounded_scores_match': True,
              'historical_aptos_count': len(differences), 'historical_max_score_delta': max(differences),
              'cpu_cuda_max_score_delta': delta, 'cuda_prediction': cuda, 'cpu_prediction': cpu}
    write_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
