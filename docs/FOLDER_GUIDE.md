# Project folder guide

## Start here

- `run_web.bat`: start the local application.
- `run_aptos_evaluation.bat`: create a new APTOS evaluation run.
- `README.md`: usage; `docs/API.md`: API and Jev setup.
- `docs/PROGRESS.md`: actual execution evidence and remaining limitations.
- `docs/IMPLEMENTATION_PLAN.md`: architecture and authorized increments.

## Folder responsibilities

| Location | Purpose / cleanup decision |
| --- | --- |
| `retfound_platform/` | Shared dataset validation, inference, evaluation and API code. Keep. |
| `frontend/` | Current web interface. Keep. |
| `scripts/` | Launch, diagnostics, preparation and verification tools. Keep. |
| `tests/` | Synthetic fixtures and regression checks. Keep. |
| `examples/` | Demonstration notebooks, including the explained Jev pipeline. Keep. |
| `util/`, root model/training/evaluation Python files | Original research baseline and dependencies. Keep their existing paths. Training is not part of cleanup. |
| `checkpoints/`, `weights/` | Protected model assets. Keep, including metadata and incomplete downloads pending a specific exception. |
| `APTOS2019.zip`, `benchmark_data/` | Dataset inputs and sampled source evidence. Keep. |
| `sample_images/`, `upload_test_images/`, `idrid2.jpg` | Referenced examples, labeled demonstration and an additional sample. Keep; similar appearance does not establish redundancy. |
| `results/`, `aptos_zip_audit/` | Saved outputs and provenance. Keep. New runs use new output directories. |
| `docs/`, root PDFs and `work_report.html` | Documentation and historical reports. Keep. Reports retain their original locations. |
| `benchmark_report.html` | Active HTML report template. Keep at the root. |
| `.runtime/web/` | Active isolated API dependencies. Keep. Other runtime logs remain for diagnostic history. |
| `.venv-win/` | Separate Windows Python 3.13 environment. Not selected by inspected launchers; external use remains unknown. Retained. |
| `.vscode/` | Editor settings selecting Conda management. Keep. |
| `archive/snapshots/` | Historical project ZIP, preserved rather than treated as redundant code. |
| `archive/source-exports/` | Historical generated source exports; inspect actual source for current behavior. |
| `docs/cleanup-review-20261031/` | Earlier read-only inspection. Its paths and sizes describe that date. |
| `docs/cleanup-20261103/` | Fresh pre-cleanup file inventory, action log and verification. |

The copied macOS `.venv` and selected generated artifacts were removed on
2026-11-03. The working interpreter remains
`%USERPROFILE%\.conda\envs\ml-homework\python.exe`.

## Organization rules

Keep entry points and baseline files at their existing locations: imports,
launchers, notebooks and report generation depend on this layout. Store future
historical snapshots under `archive/snapshots/`, generated source exports under
`archive/source-exports/`, and new reports under `docs/reports/`. Never copy local
environments or credentials into future snapshots. Do not delete alternate
validation modules independently of their CLI/test references.

This directory has no `.git` metadata. The parent gitlink does not provide a
recoverable file history for this project; cleanup records are evidence, not a
backup of deleted files.
