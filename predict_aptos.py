from pathlib import Path
import argparse
import gc

import torch
import models_vit
from PIL import Image
from torchvision import transforms
from timm.data.constants import (
    IMAGENET_DEFAULT_MEAN,
    IMAGENET_DEFAULT_STD,
)

ROOT = Path(__file__).resolve().parent
CHECKPOINT = ROOT / "checkpoints/APTOS2019/checkpoint-best.pth"
if not CHECKPOINT.is_file():
    CHECKPOINT = ROOT / "checkpoints/checkpoints/APTOS2019/checkpoint-best.pth"

CLASSES = [
    "0 - No DR",
    "1 - Mild DR",
    "2 - Moderate DR",
    "3 - Severe DR",
    "4 - Proliferative DR",
]

parser = argparse.ArgumentParser()
parser.add_argument("image", nargs="?", default=None)
parser.add_argument("--cpu", action="store_true")
args = parser.parse_args()

device = torch.device(
    "cpu" if args.cpu else
    "cuda" if torch.cuda.is_available() else
    "mps" if torch.backends.mps.is_available() else "cpu"
)
print("Device:", device)

if not CHECKPOINT.is_file():
    raise FileNotFoundError(CHECKPOINT)

print("Loading checkpoint...")

# Only load checkpoints from trusted sources.
checkpoint = torch.load(
    CHECKPOINT,
    map_location="cpu",
    mmap=True,
    weights_only=False,
)

config = checkpoint["args"]

assert config.nb_classes == 5
assert config.input_size == 224
assert config.global_pool is True

# Support old and current RETFound repository names.
if hasattr(models_vit, "RETFound_mae"):
    model = models_vit.RETFound_mae(
        img_size=224,
        num_classes=5,
        global_pool=True,
    )
elif hasattr(models_vit, "vit_large_patch16"):
    model = models_vit.vit_large_patch16(
        num_classes=5,
        global_pool=True,
    )
else:
    raise RuntimeError(
        "Compatible RETFound model definition not found."
    )

# Strict loading: no missing or unexpected weights.
model.load_state_dict(checkpoint["model"], strict=True)
print("All model weights loaded successfully!")

del checkpoint
gc.collect()

model = model.to(device)
model.eval()

transform = transforms.Compose([
    transforms.Resize(
        256,
        interpolation=transforms.InterpolationMode.BICUBIC,
    ),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        IMAGENET_DEFAULT_MEAN,
        IMAGENET_DEFAULT_STD,
    ),
])

if args.image:
    image_path = Path(args.image)
    image = Image.open(image_path).convert("RGB")
    x = transform(image).unsqueeze(0).to(device)
else:
    print("No image supplied: running a technical smoke test.")
    x = torch.zeros(1, 3, 224, 224, device=device)

with torch.inference_mode():
    # RETFound's forward_features includes global pooling
    # and fc_norm. Call head directly for compatibility
    # with different timm versions.
    features = model.forward_features(x)
    features = features.reshape(features.shape[0], -1)
    logits = model.head(features)

    assert logits.shape == (1, 5), logits.shape
    assert torch.isfinite(logits).all()

print("Output shape:", tuple(logits.shape))
print("Inference successful!")

if args.image:
    scores = torch.softmax(logits.float(), dim=1)[0].cpu()
    predicted = int(scores.argmax())

    print("\nPrediction:", CLASSES[predicted])
    print("\nSoftmax scores (not calibrated probabilities):")
    for label, score in zip(CLASSES, scores.tolist()):
        print(f"{label}: {score * 100:.2f}%")
