"""Legacy five-label macro F1 and argmax any-DR definitions, with finite JSON."""
import math
import warnings

from sklearn.metrics import cohen_kappa_score, confusion_matrix, f1_score


def metrics(records: list[dict]) -> dict:
    truth = [r['true_grade'] for r in records]
    predicted = [r['predicted_grade'] for r in records]
    if any(type(v) is not int or v not in range(5) for v in truth + predicted):
        raise ValueError('Grades must be integers in 0..4')
    n = len(records)
    correct = sum(t == p for t, p in zip(truth, predicted))
    tn, fp, fn, tp = [int(v) for v in confusion_matrix(
        [v > 0 for v in truth], [v > 0 for v in predicted], labels=[False, True]).ravel()]
    reasons = {}
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', RuntimeWarning)
        kappa = float(cohen_kappa_score(truth, predicted, labels=list(range(5)), weights='quadratic')) if n else None
    if kappa is None or not math.isfinite(kappa):
        kappa = None
        reasons['quadratic_kappa'] = 'Empty input or zero expected disagreement'
    if not n:
        reasons.update(accuracy='No evaluated images', macro_f1='No evaluated images', binary_accuracy='No evaluated images')
    if not tp + fn:
        reasons['sensitivity'] = 'No positive ground-truth images'
    if not tn + fp:
        reasons['specificity'] = 'No negative ground-truth images'
    return {'n': n, 'correct': correct, 'accuracy': correct / n if n else None,
            'macro_f1': float(f1_score(truth, predicted, labels=list(range(5)), average='macro', zero_division=0)) if n else None,
            'quadratic_kappa': kappa, 'confusion': confusion_matrix(truth, predicted, labels=list(range(5))).tolist(),
            'true_counts': {str(i): truth.count(i) for i in range(5)},
            'binary': {'accuracy': (tn + tp) / n if n else None, 'tn': tn, 'fp': fp, 'fn': fn, 'tp': tp,
                       'sensitivity': tp / (tp + fn) if tp + fn else None,
                       'specificity': tn / (tn + fp) if tn + fp else None}, 'undefined_reasons': reasons}
