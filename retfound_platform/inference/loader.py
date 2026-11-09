import gc
from pathlib import Path

import torch

from retfound_platform.config import ROOT


def checkpoint_path(explicit: Path | None = None) -> Path:
    candidates = [explicit] if explicit is not None else [
        ROOT / 'checkpoints/APTOS2019/checkpoint-best.pth',
        ROOT / 'checkpoints/checkpoints/APTOS2019/checkpoint-best.pth',
    ]
    for path in candidates:
        if path.is_file():
            return path.resolve()
    raise FileNotFoundError(f'Classifier checkpoint not found: {candidates}')


def select_device(requested: str) -> torch.device:
    if requested == 'auto':
        requested = 'cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu'
    if requested not in ('cpu', 'cuda', 'mps'):
        raise ValueError('Device must be auto, cpu, cuda or mps')
    if requested == 'cuda' and not torch.cuda.is_available():
        raise ValueError('CUDA requested but unavailable')
    if requested == 'mps' and not torch.backends.mps.is_available():
        raise ValueError('MPS requested but unavailable')
    return torch.device(requested)


def validate_config(config: object) -> None:
    if (getattr(config, 'nb_classes', None) != 5
            or getattr(config, 'input_size', None) != 224
            or getattr(config, 'global_pool', None) is not True):
        raise ValueError('Checkpoint must specify five classes, input_size=224 and global_pool=True')


def load_model(path: Path, device: torch.device):
    import models_vit
    checkpoint = torch.load(path, map_location='cpu', mmap=True, weights_only=False)
    validate_config(checkpoint.get('args'))
    model = models_vit.RETFound_mae(img_size=224, num_classes=5, global_pool=True)
    model.load_state_dict(checkpoint['model'], strict=True)
    del checkpoint
    gc.collect()
    return model.float().to(device).eval()
