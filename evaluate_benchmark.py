"""Evaluate 100 official test images and create a local, self-contained HTML report."""
import base64
import csv
import gc
import hashlib
import io
import json
from collections import Counter
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import torch
from PIL import Image, ImageOps
from torchvision import transforms
from timm.data.constants import IMAGENET_DEFAULT_MEAN, IMAGENET_DEFAULT_STD
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, cohen_kappa_score
import models_vit

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'results' / 'benchmark100'
GRADES = ['No DR', 'Mild DR', 'Moderate DR', 'Severe DR', 'Proliferative DR']
COUNTS = {'APTOS2019': 34, 'IDRID': 33, 'MESSIDOR2': 33}

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def metrics(records):
    truth = [r['true_grade'] for r in records]
    pred = [r['predicted_grade'] for r in records]
    binary = confusion_matrix([v > 0 for v in truth], [v > 0 for v in pred], labels=[False, True])
    tn, fp, fn, tp = [int(v) for v in binary.ravel()]
    return {
        'n': len(records), 'correct': sum(r['correct'] for r in records),
        'accuracy': float(accuracy_score(truth, pred)),
        'macro_f1': float(f1_score(truth, pred, labels=list(range(5)), average='macro', zero_division=0)),
        'quadratic_kappa': float(cohen_kappa_score(truth, pred, labels=list(range(5)), weights='quadratic')),
        'confusion': confusion_matrix(truth, pred, labels=list(range(5))).tolist(),
        'true_counts': {str(i): truth.count(i) for i in range(5)},
        'binary': {'accuracy': (tn+tp)/len(records), 'tn': tn, 'fp': fp, 'fn': fn, 'tp': tp,
                   'sensitivity': tp/(tp+fn) if tp+fn else None,
                   'specificity': tn/(tn+fp) if tn+fp else None},
    }

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    manifests = []
    records = []
    for name, count in COUNTS.items():
        manifest = json.loads((ROOT / 'benchmark_data' / name / 'manifest.json').read_text())
        assert manifest['split'] == 'test'
        assert len(manifest['images']) == count
        manifests.append(manifest)
        records.extend(manifest['images'])
    assert len(records) == 100
    assert len({(r['dataset'], r['archive_path']) for r in records}) == 100
    checkpoint_path = ROOT / 'checkpoints' / 'APTOS2019' / 'checkpoint-best.pth'
    if not checkpoint_path.exists():
        checkpoint_path = ROOT / 'checkpoints' / 'checkpoints' / 'APTOS2019' / 'checkpoint-best.pth'
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    torch.manual_seed(20261023)
    print('Device:', device, flush=True)
    checkpoint = torch.load(checkpoint_path, map_location='cpu', mmap=True, weights_only=False)
    config = checkpoint['args']
    assert config.nb_classes == 5 and config.input_size == 224 and config.global_pool
    model = models_vit.RETFound_mae(img_size=224, num_classes=5, global_pool=True)
    model.load_state_dict(checkpoint['model'], strict=True)
    del checkpoint
    gc.collect()
    model.to(device).eval()
    preprocess = transforms.Compose([
        transforms.Resize(256, interpolation=transforms.InterpolationMode.BICUBIC),
        transforms.CenterCrop(224), transforms.ToTensor(),
        transforms.Normalize(IMAGENET_DEFAULT_MEAN, IMAGENET_DEFAULT_STD),
    ])
    for index, record in enumerate(records):
        path = ROOT / record['path']
        record['image_sha256'] = digest(path)
        with Image.open(path) as original:
            image = original.convert('RGB')
            x = preprocess(image).unsqueeze(0).to(device)
            with torch.inference_mode():
                features = model.forward_features(x)
                logits = model.head(features.reshape(1, -1))
                assert logits.shape == (1, 5) and torch.isfinite(logits).all()
                scores = torch.softmax(logits.float(), dim=1)[0].cpu().tolist()
            predicted = int(np.argmax(scores))
            record.update(predicted_grade=predicted, true_label=GRADES[record['true_grade']],
                          predicted_label=GRADES[predicted], correct=predicted == record['true_grade'],
                          scores=scores, top_score=scores[predicted])
            image.thumbnail((480, 360))
            buffer = io.BytesIO()
            image.save(buffer, format='JPEG', quality=83)
            record['thumbnail'] = 'data:image/jpeg;base64,' + base64.b64encode(buffer.getvalue()).decode('ascii')
        print(f"{index+1}/100 {record['dataset']} {Path(record['archive_path']).name}: true={record['true_grade']} predicted={predicted}", flush=True)
    hashes = Counter(r['image_sha256'] for r in records)
    duplicates = sum(v-1 for v in hashes.values() if v > 1)
    report = {
        'created_utc': datetime.now(timezone.utc).isoformat(), 'seed': 20261023,
        'model': 'RETFound MAE ViT-Large / APTOS2019 fine-tuned, five DR grades',
        'checkpoint': str(checkpoint_path.relative_to(ROOT)), 'checkpoint_sha256': digest(checkpoint_path),
        'device': str(device), 'torch': torch.__version__, 'grades': GRADES,
        'preprocessing': 'RGB; bicubic resize shorter edge to 256; center crop 224; ImageNet mean/std normalization (repository evaluation transform).',
        'sampling': 'Uniform random sampling without replacement from each official test folder; seed 20261023. Hidden files and notebook copies excluded.',
        'evaluation': 'APTOS is within-dataset testing; IDRiD and MESSIDOR2 test transfer of the same APTOS-trained model. No fine-tuning or threshold fitting on these samples.',
        'limitations': 'Small random subsets, not full benchmark scores. Class proportions may differ. Training overlap cannot be independently ruled out from checkpoint metadata. Softmax scores are not calibrated probabilities. PAPILA excluded because its labels assess glaucoma, not DR.',
        'duplicate_image_count': duplicates,
        'sources': [{k: v for k, v in m.items() if k != 'images'} for m in manifests],
        'metrics': {'All': metrics(records), **{name: metrics([r for r in records if r['dataset'] == name]) for name in COUNTS}},
        'records': records,
    }
    # Keep structured results compact; thumbnails live in the HTML only.
    structured = {**report, 'records': [{k: v for k, v in r.items() if k != 'thumbnail'} for r in records]}
    (OUT / 'predictions.json').write_text(json.dumps(structured, indent=2, allow_nan=False), encoding='utf-8')
    with (OUT / 'predictions.csv').open('w', newline='', encoding='utf-8') as stream:
        fields = ['dataset', 'archive_path', 'true_grade', 'true_label', 'predicted_grade', 'predicted_label', 'correct', 'top_score', 'image_sha256']
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows({k: r[k] for k in fields} for r in records)
    template = (ROOT / 'benchmark_report.html').read_text(encoding='utf-8')
    payload = json.dumps(report, allow_nan=False).replace('<', '\\u003c')
    (OUT / 'index.html').write_text(template.replace('__REPORT_DATA__', payload), encoding='utf-8')
    print(json.dumps(report['metrics'], indent=2), flush=True)
    print('Report:', OUT / 'index.html', flush=True)

if __name__ == '__main__':
    main()
