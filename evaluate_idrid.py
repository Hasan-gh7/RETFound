import argparse
import csv
import gc
from collections import Counter
from math import ceil
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Save figures without requiring a display window
import matplotlib.pyplot as plt
import numpy as np
import torch
from datasets import load_dataset
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from timm.data.constants import IMAGENET_DEFAULT_MEAN, IMAGENET_DEFAULT_STD
from torchvision import transforms

import models_vit

GRADES = ["No DR", "Mild", "Moderate", "Severe", "Proliferative"]
CHECKPOINT = Path("checkpoints/APTOS2019/checkpoint-best.pth")
OUT_DIR = Path("results/idrid")


def make_model(device):
    if not CHECKPOINT.is_file():
        raise FileNotFoundError(f"Checkpoint not found: {CHECKPOINT}")

    if hasattr(models_vit, "RETFound_mae"):
        model = models_vit.RETFound_mae(img_size=224, num_classes=5, global_pool=True)
    elif hasattr(models_vit, "vit_large_patch16"):
        model = models_vit.vit_large_patch16(num_classes=5, global_pool=True)
    else:
        raise RuntimeError("Cannot find RETFound MAE ViT-Large model in models_vit.py")

    # Only use trusted, official checkpoint files.
    checkpoint = torch.load(CHECKPOINT, map_location="cpu", mmap=True, weights_only=False)
    model.load_state_dict(checkpoint["model"], strict=True)
    del checkpoint
    gc.collect()
    return model.to(device).eval()


def save_gallery(records, page_size=20):
    """Each gallery shows fundus images with true and predicted grades."""
    for page_start in range(0, len(records), page_size):
        subset = records[page_start: page_start + page_size]
        columns = 4
        rows = ceil(len(subset) / columns)
        fig, axs = plt.subplots(rows, columns, figsize=(15, rows * 3.9))
        axs = np.asarray(axs).ravel()
        for ax in axs:
            ax.axis("off")
        for ax, result in zip(axs, subset):
            ax.imshow(result["preview"])
            correctness = "CORRECT" if result["correct"] else "INCORRECT"
            ax.set_title(
                f"IDRiD test row {result['row']}\n"
                f"True: {result['true']} ({GRADES[result['true']]})\n"
                f"Pred: {result['pred']} ({GRADES[result['pred']]}) - {correctness}",
                fontsize=9,
                color="green" if result["correct"] else "firebrick",
            )
            ax.axis("off")
        fig.tight_layout()
        gallery_path = OUT_DIR / f"gallery_{1 + page_start // page_size:02d}.png"
        fig.savefig(gallery_path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print("Saved gallery:", gallery_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="Evaluate all IDRiD test images")
    parser.add_argument("--per-grade", type=int, default=4,
                        help="For a quick demo, show this many images from each true grade")
    parser.add_argument("--cpu", action="store_true", help="Use CPU instead of Apple MPS")
    args = parser.parse_args()

    if args.per_grade < 1:
        parser.error("--per-grade must be at least 1")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    device = torch.device("mps" if torch.backends.mps.is_available() and not args.cpu else "cpu")
    print("Device:", device)
    print("Loading model once...")
    model = make_model(device)
    print("Model weights loaded (strict=True).")

    preproc = transforms.Compose([
        transforms.Resize(256, interpolation=transforms.InterpolationMode.BICUBIC),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(IMAGENET_DEFAULT_MEAN, IMAGENET_DEFAULT_STD),
    ])

    print("Streaming IDRiD test split...")
    ds = load_dataset("amin-nejad/idrid-disease-grading", split="test", streaming=True)
    print("Dataset label names:", getattr(ds.features["label"], "names", "not available"))
    per_grade_counts = Counter()
    results = []

    for index, item in enumerate(ds):
        true_grade = int(item["label"])
        if not 0 <= true_grade <= 4:
            raise ValueError(f"Unexpected label at row {index}: {true_grade}")
        if not args.all and per_grade_counts[true_grade] >= args.per_grade:
            continue

        pil_image = item["image"].convert("RGB")
        image_tensor = preproc(pil_image).unsqueeze(0).to(device)
        with torch.inference_mode():
            features = model.forward_features(image_tensor)
            logits = model.head(features.reshape(features.shape[0], -1))
            if logits.shape != (1, 5) or not torch.isfinite(logits).all():
                raise RuntimeError(f"Invalid model output for row {index}")
            scores = torch.softmax(logits.float(), dim=1)[0].cpu()

        predicted_grade = int(scores.argmax().item())
        top_score = float(scores[predicted_grade].item())
        thumb = pil_image.copy()
        thumb.thumbnail((340, 340))
        results.append({
            "row": index,
            "true": true_grade,
            "pred": predicted_grade,
            "correct": true_grade == predicted_grade,
            "score": top_score,
            "preview": thumb,
        })
        per_grade_counts[true_grade] += 1
        status = "CORRECT" if predicted_grade == true_grade else "INCORRECT"
        print(f"Row {index:3d}: true={true_grade}, predicted={predicted_grade}, "
              f"score={100*top_score:5.1f}% -> {status}")

        if not args.all and all(per_grade_counts[g] >= args.per_grade for g in range(5)):
            break

    if not results:
        raise RuntimeError("No test images were evaluated.")

    csv_path = OUT_DIR / "predictions.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["test_row", "true_grade", "true_name", "predicted_grade",
                         "predicted_name", "predicted_softmax", "correct"])
        for result in results:
            writer.writerow([
                result["row"], result["true"], GRADES[result["true"]],
                result["pred"], GRADES[result["pred"]],
                f"{result['score']:.5f}", result["correct"],
            ])

    y_true = [r["true"] for r in results]
    y_pred = [r["pred"] for r in results]
    accuracy = accuracy_score(y_true, y_pred)
    macro_f1 = f1_score(y_true, y_pred, labels=list(range(5)),
                        average="macro", zero_division=0)
    correct = sum(r["correct"] for r in results)
    sample_desc = "all streamed test images" if args.all else "selected balanced example subset"
    summary = (
        f"Evaluation: {sample_desc}\n"
        f"Evaluated: {len(results)}\n"
        f"Correct: {correct}\n"
        f"Incorrect: {len(results)-correct}\n"
        f"Accuracy: {accuracy*100:.2f}%\n"
        f"Macro F1: {macro_f1:.4f}\n"
        f"True class counts: {dict(sorted(Counter(y_true).items()))}\n"
        "Scores are not calibrated medical probabilities.\n"
    )
    (OUT_DIR / "summary.txt").write_text(summary, encoding="utf-8")
    print("\n" + summary)
    print("Saved CSV:", csv_path)

    cm = confusion_matrix(y_true, y_pred, labels=list(range(5)))
    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(cm, cmap="Blues")
    fig.colorbar(im, ax=ax)
    ax.set_xticks(range(5), labels=range(5))
    ax.set_yticks(range(5), labels=range(5))
    ax.set_xlabel("RETFound prediction")
    ax.set_ylabel("True IDRiD grade")
    ax.set_title("Confusion matrix - IDRiD test")
    for i in range(5):
        for j in range(5):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "confusion_matrix.png", dpi=150)
    plt.close(fig)

    save_gallery(results)
    print("Done. Open results/idrid/gallery_01.png to view images and grades.")


if __name__ == "__main__":
    main()
