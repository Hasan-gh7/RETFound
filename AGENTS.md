# RETFound project instructions

## Scope and first steps

This is an existing RETFound research evaluation project being prepared for a technical demonstration to the Syrian Ministry of Health. Extend it incrementally; do not rebuild it.

Read `docs/PROGRESS.md` and `docs/IMPLEMENTATION_PLAN.md`, then inspect the actual files relevant to the current request. The filesystem and observed executions take precedence over old reports, project exports, and previous conversation snapshots. Distinguish existing functionality, historical artifacts, verified behavior, and proposed work.

The inspection/documentation phase completed on 2026-10-29. The implementation phases in the plan are proposals, not authorization to execute them automatically. Stop at the phase requested by the user.

## Preserve the baseline

- Do not train, fine-tune, update weights, replace the classifier, or modify checkpoints as part of platform development.
- Preserve `predict_aptos.py`, `prepare_benchmark.py`, `evaluate_benchmark.py`, `evaluate_idrid.py`, both batch launchers, existing notebooks, and saved reports. Refactor only when the requested phase calls for it, retaining command-line behavior and checking parity.
- Treat `checkpoints/`, `weights/`, source datasets, and historical `results/` and `aptos_zip_audit/` artifacts as read-only inputs. New runs should use new output directories and must not silently overwrite historical evidence.
- Do not execute `train.sh` or notebook training cells. `main_finetune.py` is a training-oriented entry point; use the dedicated inference path for the platform.
- Do not download datasets, install/upgrade packages, initialize Git, or alter environment configuration merely to inspect the project.
- Do not claim successful tests, reproducibility, dataset independence, or clinical readiness without evidence. A saved report is not a fresh execution.

## Windows and environment conventions

- Workspace: `C:\Users\jadgh\Desktop\Dr 4\Dr\RETFound`. Quote paths containing spaces and use `pathlib.Path` in Python.
- Known working interpreter: `%USERPROFILE%\.conda\envs\ml-homework\python.exe` (Python 3.10.19 at inspection). In PowerShell invoke it with `&`.
- The copied `.venv` is a macOS environment. `.venv-win` is a separate Python 3.13 environment and has not been validated for this model. Do not infer the active environment from the prompt alone; check `sys.executable`.
- The current installed packages differ from `requirements.txt`. Preserve the working environment until a separate reproducible dependency specification has been validated.
- Resolve project defaults relative to the package/script, not the caller's working directory. Permit explicit configured dataset and output roots; never substitute a guessed location for a missing dataset.
- Store portable relative image paths with `/` in manifests; keep machine-specific absolute paths in local configuration/provenance only.
- Use UTF-8 for documents and artifacts. Console output on Windows may require `sys.stdout.reconfigure(encoding='utf-8')`.
- Parent Git currently records `RETFound` as a gitlink, but this folder has no `.git` metadata. Parent `git status` does not prove changes here are tracked. Report this rather than repairing history automatically; preserve unrelated parent changes.

## Inference contract

- Use `models_vit.RETFound_mae(img_size=224, num_classes=5, global_pool=True)` for the present APTOS classifier. Reuse the existing architecture.
- Resolve the explicit checkpoint first, then the existing supported layouts: `checkpoints/APTOS2019/checkpoint-best.pth` and `checkpoints/checkpoints/APTOS2019/checkpoint-best.pth`. The latter exists at inspection.
- The separate `weights/weights/RETFound_mae_natureCFP/RETFound_mae_natureCFP.pth` is a pretraining asset, not a replacement for the APTOS classifier.
- Load the trusted local checkpoint on CPU with the existing compatible loading options (`mmap=True`, `weights_only=False`), validate its configuration, and load `checkpoint['model']` with `strict=True`. Never accept uploaded checkpoint files or arbitrary remote checkpoint URLs.
- Require five classes, input size 224, and global pooling. Use explicit exceptions for new validation code, not assertions that disappear under `python -O`.
- Preserve this preprocessing exactly: decode with Pillow, convert to RGB, bicubic resize of the shorter edge to 256, center crop 224, `ToTensor`, normalize with ImageNet mean `(0.485, 0.456, 0.406)` and standard deviation `(0.229, 0.224, 0.225)`.
- Do not silently add EXIF rotation, contrast enhancement, retinal cropping, augmentation, or alternative normalization. Any proposed change requires a separately named preprocessing version and a parity/effect check.
- Use `model.eval()` and `torch.inference_mode()`. The compatible forward path is `forward_features(x)`, reshape to `(batch, -1)`, then `model.head(features)`. Validate finite `(batch, 5)` logits.
- Grade order is fixed: 0 No DR, 1 Mild, 2 Moderate, 3 Severe, 4 Proliferative. Return all five softmax scores and the argmax grade. Scores are uncalibrated model scores.
- Support explicit device selection and report the actual device. Preserve existing CUDA/MPS/CPU behavior where already supported. Baseline parity uses float32; optimization or mixed precision is a later measured change.
- Shared modules must not parse CLI arguments, load weights, allocate a GPU model, download data, or write outputs during import. Load the model once per inference service/process.

## Data and evaluation rules

- Validate source format, split identity, explicit label mapping, paths, decoding, and duplicate/overlap evidence before sampling for evaluation.
- Support documented numeric grade folders and the named folders in `prepare_benchmark.CLASS_MAP`. Reject unknown labels; do not depend on incidental directory sorting.
- Exclude hidden entries, `__MACOSX`, and notebook checkpoint copies. Resolve paths within configured roots; guard archive paths, symlinks, resource limits, and duplicate archive members in new ingestion code.
- Full overlap checks require train, validation, and test evidence. A test-only manifest must say overlap is unverified, never imply the check passed.
- Record exact-byte SHA-256 checks separately from patient-level and near-duplicate checks. Do not claim the latter without suitable metadata/methods. Exclude conflicting-label duplicate groups pending review.
- Use deterministic sampling with an explicit seed, stable candidate ordering, no replacement, and a persisted selection manifest. Never fill a shortage by duplicating images or borrowing train/validation images.
- Preserve the historical benchmark's seed `20261023` and counts 34 APTOS2019 / 33 IDRID / 33 MESSIDOR2 for legacy parity. Label balanced demonstrations separately from proportional or uniform evaluation samples.
- Keep APTOS within-dataset results separate from IDRiD/MESSIDOR2 transfer results. Any-DR means argmax grade > 0 in the existing benchmark; do not silently replace that rule with a probability threshold.
- Fix confusion-matrix label order to 0..4. Define empty/single-class/absent-class behavior; serialize undefined metrics as JSON `null` with a reason, never NaN/Infinity. Preserve legacy five-label macro-F1 semantics when comparing old results.
- Record source identity, sample seed/method, exclusions, checkpoint hash, preprocessing version, package/device information, and output schema version for new runs.

## Code and verification conventions

- Follow the proposed `retfound_platform` package boundaries in the implementation plan. Use typed functions and small data contracts; keep framework schemas and UI code outside the core model/data logic.
- API, notebook, and frontend must consume the same inference/evaluation contracts. No duplicated model implementations or metric calculations in the browser.
- Add meaningful tests for data corruption, leakage, label mapping, deterministic selection, insufficient samples, preprocessing parity, and metric edge cases as those components are implemented. Use small synthetic fixtures; real checkpoints are optional integration inputs, not unit-test dependencies.
- Do not import `predict_aptos.py` as a library in its present form: it executes inference at module import. Run its CLI for baseline checks.
- Do not present mocks or fixture predictions as real model results. Report the command, environment, outcome, and limitations of checks actually run.
- Update `docs/PROGRESS.md` after each authorized phase with completed/pending work, changed paths, commands, evidence, and unresolved issues. Update the plan when scope or architecture changes.
