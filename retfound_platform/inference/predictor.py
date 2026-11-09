import hashlib
import platform
import threading
from importlib.metadata import version
from pathlib import Path

import torch

from retfound_platform.datasets.labels import GRADES
from retfound_platform.datasets.manifests import digest
from retfound_platform.datasets.validation import decode
from .loader import checkpoint_path, load_model, select_device
from .preprocessing import PREPROCESSING_VERSION, build_transform


class Predictor:
    """One explicitly loaded model, serialized inference, no import-time I/O."""
    def __init__(self, device: str = 'auto', checkpoint: Path | None = None):
        self.device = select_device(device)
        path = checkpoint_path(checkpoint)
        self.metadata = {
            'checkpoint': str(path), 'checkpoint_sha256': digest(path),
            'device': str(self.device), 'dtype': 'float32',
            'preprocessing_version': PREPROCESSING_VERSION,
            'python': platform.python_version(),
            'packages': {name: version(name) for name in ['torch', 'torchvision', 'timm', 'Pillow', 'numpy', 'scikit-learn']},
        }
        self.model = load_model(path, self.device)
        self.transform = build_transform()
        self.lock = threading.Lock()

    def predict(self, payload: bytes) -> dict:
        with decode(payload) as image:
            x = self.transform(image).unsqueeze(0)
        with self.lock, torch.inference_mode():
            x = x.to(self.device)
            features = self.model.forward_features(x)
            logits = self.model.head(features.reshape(features.shape[0], -1))
            if tuple(logits.shape) != (1, 5) or not bool(torch.isfinite(logits).all()):
                raise ValueError('Model returned invalid logits; expected finite (1, 5)')
            scores = torch.softmax(logits.float(), dim=1)[0].cpu().tolist()
        grade = max(range(5), key=scores.__getitem__)
        return {'image_sha256': hashlib.sha256(payload).hexdigest(),
                'predicted_grade': grade, 'predicted_label': GRADES[grade],
                'scores': scores, 'top_score': scores[grade]}
