import ast
import io
import threading
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import torch
import numpy as np
from PIL import Image
from torchvision import transforms
from timm.data.constants import IMAGENET_DEFAULT_MEAN, IMAGENET_DEFAULT_STD

from retfound_platform.config import ROOT
from retfound_platform.inference.loader import validate_config, checkpoint_path
from retfound_platform.inference.predictor import Predictor
from retfound_platform.inference.preprocessing import build_transform


class InferenceTests(unittest.TestCase):
    def test_exact_preprocessing_from_baseline_source(self):
        # Execute only the transform expression parsed from the legacy CLI, never import it.
        tree = ast.parse((ROOT / 'predict_aptos.py').read_text(encoding='utf-8'))
        expression = next(n.value for n in tree.body if isinstance(n, ast.Assign)
                          and any(isinstance(t, ast.Name) and t.id == 'transform' for t in n.targets))
        baseline = eval(compile(ast.Expression(expression), '<baseline-transform>', 'eval'),
                        {'transforms': transforms, 'IMAGENET_DEFAULT_MEAN': IMAGENET_DEFAULT_MEAN,
                         'IMAGENET_DEFAULT_STD': IMAGENET_DEFAULT_STD})
        for size, mode in [((320, 511), 'RGB'), ((511, 320), 'L'), ((224, 224), 'RGBA')]:
            values = np.random.default_rng(42).integers(0, 256, (size[1], size[0], 3), dtype=np.uint8)
            image = Image.fromarray(values).convert(mode).convert('RGB')
            self.assertTrue(torch.equal(baseline(image), build_transform()(image)))

    def test_invalid_config_and_explicit_checkpoint(self):
        validate_config(SimpleNamespace(nb_classes=5, input_size=224, global_pool=True))
        for config in [None, SimpleNamespace(nb_classes=4, input_size=224, global_pool=True),
                       SimpleNamespace(nb_classes=5, input_size=256, global_pool=True)]:
            with self.assertRaises(ValueError):
                validate_config(config)
        with self.assertRaises(FileNotFoundError):
            checkpoint_path(ROOT / 'does-not-exist.pth')

    def test_invalid_logits(self):
        predictor = Predictor.__new__(Predictor)
        predictor.device = torch.device('cpu')
        predictor.lock = threading.Lock()
        predictor.transform = build_transform()
        payload = io.BytesIO()
        Image.new('RGB', (20, 30)).save(payload, format='PNG')
        for logits in [torch.zeros(1, 4), torch.full((1, 5), float('nan'))]:
            predictor.model = SimpleNamespace(forward_features=lambda x: x, head=lambda x: logits)
            with self.assertRaises(ValueError):
                predictor.predict(payload.getvalue())
