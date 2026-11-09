# RETFound evaluation platform implementation plan

## Authorized source-only GitHub preparation — 2026-11-09

Scope is publication hygiene only: exclude weights/checkpoints, dataset archives,
benchmark data/results, generated exports, large historical inventories, and local
environments; remove the exposed provider credential from five text files; clarify
fresh-clone asset requirements. Preserve original data, model assets, source code,
running services, and historical reports. Do not initialize Git, stage, commit,
push, create a GitHub repository, or perform model/provider requests. Verification
is limited to ignore behavior, publication file sizes, and credential scanning.
This does not authorize any implementation phase or establish runtime readiness.

## Authorized Phase3 defect corrections — 2026-11-07

Scope is exactly image-wide stable-person separation and reviewer-pair agreement
statistics. Implemented additive0005 guards plus matching application checks,
audited existing exceptions, reverse/Phase3A protection and concurrency locks;
reports now identify/group reviewer pairs.115 tests pass on disposable databases.
Live migration/restart is explicitly excluded. Browser automation is disabled;
deployed acceptance remains pending. See [corrective report](../clinical_database/docs/PHASE3_DEFECT_FIXES.md).
No Phase4, model, inference, patient or imported-image changes.

## Phase3 acceptance fixes —2026-11-06

User reaffirmed full Phase3 completion and fresh verification. Closed identified
search/history/read-only/audit/reporting/concurrency gaps in the existing modules,
retaining schema0004 and all historical migrations.103tests and a fresh full browser
workflow passed, with original-record preservation and backup restoration verified.
See [acceptance matrix](../clinical_database/docs/PHASE3_ACCEPTANCE.md). Synthetic
research functionality is complete; clinical/real-image/production approval remains
explicitly unavailable. No Phase4 work is authorized or performed.

## Authorized full research Phase 3B–G — 2026-11-06

User explicitly expanded scope beyond3A to the full local research workflow.
Implemented incrementally in existing clinical_database and plain frontend: named
RBAC users, protocols/projects, independent assignments/drafts/finals, locking and
blindness, agreement/disagreement, adjudication, versioned synthetic research labels,
independent approval, authorized metadata export, dashboard and reporting. New
static additive0004 adds8tables; existing database/inference components preserved.
Live migration followed private backup, disposable migration/regression tests and
verified restoration. Clinical approvals, verified qualifications, real-image grants
and institutional production access stay closed; no authorization is fabricated.
Evidence: [Phase3 implementation report](../clinical_database/docs/PHASE3_IMPLEMENTATION_REPORT.md).
This completes Phase3 research functionality only. No Phase4 model integration,
training, retraining, dataset release or hospital imports are authorized or executed.

## Authorized independent review Phase 3A — completed 2026-11-06

Extend only the existing clinical service and frontend for blind independent review:
named local sessions, authorized synthetic image access, bilingual review queue and
viewer, append-only quality/DR/separate DME/notes, personal history and audit. Reuse
ClinicalAnnotation with additive 0003 and explicit synthetic display grants. Actual
frontend inspection found plain HTML/JS, so reused it instead of adding React/build
infrastructure. Preserve original 15 pilot records, imported labels, training gates,
all model/inference/evaluation code and existing UI entry points. Completed with
67 passing synthetic tests and live browser QA; see
[CLINICAL_REVIEW.md](../clinical_database/docs/CLINICAL_REVIEW.md).
No authorization for real-image display, adjudication/consensus, hospital imports,
production authentication, model changes or later phases is inferred.

## Authorized independent ingestion Phase 2A — 2026-11-06

Implement only the user's small public-dataset ingestion pilot in clinical_database/:
explicit local folder/ZIP source descriptors, JPEG/PNG/hash/label/split previews,
idempotent bounded execution, immutable import/source-label occurrence records,
additive migration 0002, authenticated configured-source-only API support, synthetic
regressions and ingestion documentation. Preserve all model/inference/frontend,
historical reports, original sources and Phase 1 protections. No hospital imports,
training approval, protected test imports or downloads. Actual pilot execution must
respect the existing disabled source-write gate and coordinate only the metadata
API deployment; model server operation is outside the changed scope.

## Authorized independent clinical database Phase 1 — 2026-11-06

User explicitly authorized the pasted clinical database foundation Phase 1 and
required a separate folder while the model server continues running. Implement
only `clinical_database/`: independent SQLAlchemy/PostgreSQL metadata, immutable
clinical/provenance history, versioned datasets and split guards, local storage
abstraction, Alembic, five minimal authenticated data routes, synthetic PostgreSQL
tests and setup/governance documentation. This is a separate Phase 1 scope from
the historical inspection-phase numbering below. No existing inference API,
frontend, model environment, launchers, weights, data or evaluation changes.
Root progress/plan receive documentation pointers only. Integration into the
running server, upload/review APIs, S3 implementation, hospital imports and any
training remain deferred. Details: `clinical_database/docs/DATABASE_ARCHITECTURE.md`.

## Telegram concise response and demo previews - 2026-11-06

Add authenticated POST /api/predict/summary using existing inference, returning
only predicted grade/label and five named percentage scores. Preserve full
prediction contract for current clients. Serve 320px JPEG demo thumbnails for
display only; original hashes/bytes and inference preprocessing unchanged.
Expose Jev/model timings in full responses/UI for diagnosis, without claims of
provider acceleration or bypassing screening. Bot formatting guidance is supplied;
the colleague's external Telegram bot source is not edited here.

## Authorized temporary external API trial - 2026-11-04

Website adapter serves original frontend assets locally; only API/data/schema
requests traverse the external tunnel. UI startup is independent of upstream
HTML latency, avoiding the previous two-second startup-probe failure.

2026-11-05 corrected application identity: user's demo is eye-ai-demo. Launch
its existing server adapter on 8001 using the external connection file URL/key,
and a separate loopback website adapter on 8002 for the original RETFound UI.
Both keep credentials server-side; neither browser asks for an API key. The
share launcher owns both UI child processes after external health succeeds.
Remote colleagues run eye-ai-demo with a private current connection.json.
No model/dependencies bundled or installed; no public hosting of the two adapters.

2026-11-05 expanded scope: share_api.py enables --public-demo, exposing the
original UI static assets with all data/inference routes authenticated. A shared
fetch adapter adds a tab-session RETFound key; sample previews use authenticated
blob fetches. Full demo permits 30 submissions/minute for the 15-image workflow.
Launcher opens the root external URL. API-only server mode remains available.

2026-11-05: authorize an external demo at /external-demo with a public static
page and script, and manually entered memory-only RETFound access key. API
requests remain Bearer-protected; authenticated public requests permit Origin
headers to support the Cloudflare Host rewrite. No wildcard CORS enabled.

The launcher also updates a stable .runtime/tunnel/connection.json on each new
session, per user request, while preserving session-specific originals.

User selected a temporary colleague/application/Telegram integration trial, not
continuous hosting. Add opt-in API-only Bearer authentication and a shared
10-submissions/minute limit around existing inference. Keep loopback binding,
local mode, checkpoint and preprocessing intact. Add scripts/share_api.py to
launch one real server and a portable Cloudflare Quick Tunnel with local Host
rewriting, unique connection details and cleanup on exit. Publish only health,
model and predict routes; do not publish frontend/datasets/reports. No Telegram
bot implementation or permanent deployment is authorized in this increment.
Live external success requires user-held OpenRouter credentials and a fresh
external test; synthetic tests cannot establish it. See docs/TEMPORARY_API.md
and PROGRESS.md for commands and verification boundaries.

## Authorized cleanup and organization increment - 2026-11-03

User requested determining unnecessary content and arranging the existing project.
Remove the incompatible copied macOS environment and selected generated artifacts;
preserve working Conda and `.runtime/web` dependencies. Organize historical ZIP
and generated source exports under `archive/`, with hash-verified moves. Preserve
baseline entry points, model assets, datasets, notebooks and historical reports in
place. Retain the separate Windows environment and alternate validation modules
where non-use is not established. Document the layout in `docs/FOLDER_GUIDE.md`
and record the fresh inventory, actions and verification under
`docs/cleanup-20261103/`. This is housekeeping, not a model or architecture change.

## Authorized sensitivity/specificity presentation increment

On 2026-11-03 the user requested sensitivity and specificity calculation/display.
Expose existing saved binary metrics on the main evaluation page with formulas,
counts and undefined-value reasons. The explanatory notebook recomputes the saved
run through the same shared metric function. Preserve grade > 0 as the any-DR
rule; no new probability threshold, model change or paid inference. Keep these
RETFound-only results distinct from Jev screening. Evidence is in PROGRESS.md.


## Authorized explained notebook increment

On 2026-10-30 the user requested a Jupyter notebook explaining image testing and
its pipeline. Added examples/RETFound_Jev_15_Image_Test_Pipeline.ipynb as a local
server API client, sharing existing inference/comparison contracts. Preview is
local; real single/batch requests are disabled by default. Optional JSON exports
use new unique files. This increment does not add model implementations, training,
new datasets or representative evaluation claims. Verification is in PROGRESS.md.


## Authorized local dataset testing increment

The user explicitly selected adding the 15-image labeled demonstration to the
existing local server on 2026-10-30. This extends the earlier manual-upload scope
with fixed server sample IDs, verified image reads, backend reference comparison
and a /dataset-tests page. UI actions invoke the existing Jev and RETFound path;
no separate model or browser metric implementation exists. The browser sequences
requests and downloads session results; durable jobs/history and remote hosting
are outside this increment. No actual batch inference was run during development.
The sample remains a balanced demonstration with unverified broader independence.
Acceptance checks and execution evidence are in PROGRESS.md.


## Authorized labeled upload demonstration increment

On 2026-10-30 the user requested five labeled test images from each of the three
explicit Hugging Face repositories IDRiD, OctoMed Messidor2 and DDR. This authorizes
selective download into a new upload_test_images folder and label/provenance
artifacts. The delivered 15-image set is balanced one per grade, intended for
manual uploads and comparison. It does not authorize or claim a new representative
evaluation, paid batch Jev inference, training or application changes. The source
adapter is an explicit preparation script, not a general remote ingestion service.
Completed paths, executed checks and source-representation limits are recorded
in PROGRESS.md and the download manifest.


## Empty HTTP 400 credential isolation and one-command startup - 2026-10-30

User supplied live text-only HTTP 400 with no Content-Type and zero response
bytes, and requested a solution. Do not interpret this as a confirmed Jev schema
error. Approved unauthenticated probes from the agent process used urllib and
http.client against GET /api/v1/key and POST /api/alpha/decisions. All four returned
HTTP 401 with application/json and a nonempty auth error, establishing reachability
from this diagnostic context. No key was available in the agent environment, and
no images or actual credentials were sent by these probes. This does not prove
connectivity or authentication in the user's terminal.

Added FundusGate.check_authentication using the official GET /api/v1/key endpoint
(no model invocation), management/provisioning-key rejection, and rejection of
control/whitespace/non-ASCII header credentials before transport. The diagnostic
now checks the expected sk-or-v1- key syntax before network I/O, then checks auth
before text/image requests. Syntax failure does not assert server key validity;
only the auth response can establish acceptance. No secret is printed or saved.

Added --new-key for a hidden prompt bypassing a stale environment key, and
--start-server to launch serve_web.py with the tested credential in the child
environment only after all checks pass. The key is absent from process arguments
and source files. Existing servers still must be stopped to avoid launcher reuse.
Failures still block DR inference; no retries, model substitutions or bypasses.

Verification: `python -B -m unittest tests.test_fundus_gate tests.test_jev_diagnostic`
passed all 18 tests in ml-homework. Mock tests cover auth GET (no body), management
key handling, bad credentials blocking network, auth failure skipping billed
requests, hidden prompt and tested-key handoff without secret argv exposure.
No live authenticated Jev classification is claimed. Actual empty-400 root cause
remains unconfirmed pending the user's credential-bearing run. No weights,
RETFound preprocessing, source images or historical results were modified.


## Text-only HTTP 400 investigation - 2026-10-30

The user's live diagnostic returned HTTP 400 even for the small text fixture;
the image was correctly skipped. This establishes that the observed failure
also affects text-only requests, not that image processing is its cause. HTTP
400 alone does not establish which server/intermediary rejected the request.

The earlier error parser accepted only error.message; missing/unreadable details
were silently discarded. Updated inference/fundus_gate.py to extract common
error/message/detail/issues JSON shapes, an HTML title, or bounded plain text,
with existing credential/data redaction. Request echoes and metadata are not
traversed. GateUnavailable now has separate safe diagnostic text (content type,
bytes inspected, empty/unreadable body) used by the diagnostic CLI only. HTTP
400 wording no longer asserts a request-format cause without evidence. Added
explicit JSON accept/identity encoding and an application User-Agent. Diagnostic
prints HTTPS proxy presence only, never proxy URLs/credentials. Payload and model
are unchanged pending actual validation evidence.

Executed in ml-homework: `python -B -m unittest tests.test_fundus_gate tests.test_jev_diagnostic`.
All 13 tests passed, with mocked provider responses. Tests cover alternative
JSON error shapes, HTML title extraction, suppressed metadata, safe response
diagnostics, binary admission, image sizes, timeouts and diagnostic skip behavior.
The real text/image request remains unresolved; no authenticated live request or
server restart was possible from this process. Next evidence needed: rerun the
updated diagnostic in the user's terminal with its existing key. No key should be
shared in chat. No DR weights, preprocessing or saved evidence changed.


## Jev timeout handling and connection diagnostic - 2026-10-30

The user reported a Jev timeout after the size repair. This does not prove that
the request was accepted or that the earlier HTTP 400 is fully resolved.
The transport used a 30-second socket timeout. Changed its default to 90 seconds,
with JEV_TIMEOUT_SECONDS configurable in 1..90 (finite values only). Timeout
messages now include elapsed time and whether failure occurred before response
headers or while reading the response body. No automatic retries are performed.
The image admission contract remains binary, with service failures blocking DR.

Added scripts/diagnose_jev.py: explicitly sends a small text fixture using the
same model/transport, then the existing sample image if text succeeds, reporting
separate timings. It never runs RETFound or saves credentials. It reads the key
from the launching environment, or prompts invisibly if absent. It can be run
without loading the DR model; requests may be billed by OpenRouter. A successful
text fixture is not an image classification or accuracy result.

Added timeout configuration/phase tests and diagnostic success/skip tests.
All 11 gate and diagnostic tests passed with mocked transport in ml-homework
using `python -B -m unittest tests.test_fundus_gate tests.test_jev_diagnostic`.
The combined gate/API suite stalled after the nine gate tests and was interrupted;
no completed API-suite pass is claimed for this increment. The diagnostic CLI
help was verified separately. No authenticated
live call or service restart was performed; the underlying timeout cause is not
confirmed. User must run the diagnostic in their credential-bearing terminal.


## Jev image size compatibility repair - 2026-10-30

User retry returned HTTP 400. Checked the current official multimodal guide:
https://openrouter.ai/docs/guides/community/multimodal-decisions
Jev requires 256..1568 pixels per side and 78,400..2,458,624 total pixels.
The actual sample_images/idrid_test.jpg is 4288x2848, outside these limits.
This is a verified incompatibility; the exact reason for the user's 400 remains
unconfirmed because the provider validation body was previously discarded.

Updated inference/fundus_gate.py to prepare a dimension-compliant remote copy,
using bicubic resizing and RGB JPEG where necessary. Original uploaded bytes
continue unchanged to RETFound. Extreme aspect ratios block admission explicitly.
Bounded HTTP 400/422 validation messages are now exposed after redacting the key,
data URLs and long encoded strings; provider metadata is not displayed.
Added dimension-boundary and validation-redaction tests. All seven gate tests
passed in ml-homework via unittest discovery of test_fundus_gate.py. Provider
responses were mocked. No authenticated call, accuracy validation or server
restart was performed. The user must restart their credential-bearing server.


## Jev connection diagnostics repair - 2026-10-30

The user supplied a screenshot showing a failed Jev request with the generic
unavailable message. Updated inference/fundus_gate.py to distinguish HTTP status
(authentication, credits, permissions, request/model errors, size, rate limit,
provider outage), timeout, TLS certificate failure, connection failure and invalid
response. Messages never include provider bodies, credentials or uploaded bytes.
The gate still blocks RETFound on all failures. Added status/redaction and
connection-message tests in tests/test_fundus_gate.py.

Executed with the existing ml-homework interpreter:
`python -B -c "import unittest; r=unittest.TextTestRunner().run(unittest.defaultTestLoader.discover('tests', pattern='test_fundus_gate.py')); raise SystemExit(not r.wasSuccessful())"`
All five gate tests passed (mock provider responses). An approved network probe,
without credentials or images, reached the fixed endpoint and received HTTP 401.
This proves reachability from that diagnostic process, not the user's key validity
or image classification. The local service could not be reached from the tool
process; no service was stopped/restarted and no credentials inspected. The
screenshot's underlying failure remains unknown until retry with the new messages.


## Jev fundus admission increment - 2026-10-30

Authorized by the user: implement an HTTP Jev image classifier before RETFound.
Added `inference/fundus_gate.py`: fixed OpenRouter Decisions endpoint, model
`typesafe/jev-1.14`, backend environment key, binary choice, 30-second timeout,
bounded response, disabled redirects and redacted provider errors. No SDK/install.
The API now requires decision 1 before predictor invocation; decision 0 returns
422 with null prediction; missing key/provider/invalid result returns 503.
Both raw and multipart requests share the gate. No direct-input fallback exists.
Jev-only format conversion does not alter original bytes sent to RETFound.

Updated API schemas, frontend admission text/contract, README, API setup docs,
verification script and UI fixtures. Added client tests and API rejection/failure
regressions. Model weights, preprocessing and historical results are preserved.
The old direct-input notes below describe superseded behavior.

Verification: 14 API tests passed using the ml-homework interpreter via
`python -B scripts/test_web.py`. Full suite and Node UI checks run subsequently;
see completion evidence below. HTTP provider responses in unit tests are mocked,
not real predictions. No authenticated Jev call or fundus accuracy evaluation was
performed. The previously running service has not been restarted; it retains the
old behavior until the user stops it and launches with OPENROUTER_API_KEY as
documented in docs/API.md. No key was requested through chat or written to disk.


## Authorized direct image inference - 2026-10-30

The user subsequently rejected the approval workflow and requested sending their
uploaded photo into the model directly. This supersedes the restricted-input
increment below. The API now validates decoding, format and resource limits, then
calls the existing predictor without consulting reference hashes or review files.
The page and Postman use that same path. `input_validation.status` is `decoded`;
`model.input_policy` is `retfound-direct-input-v1`. Neither implies retinal modality
verification. The interface explains that this five-class model can assign a DR
grade to non-retinal photos. No detector, training or preprocessing changes are
part of this increment. Prior policy utilities remain inactive historical code.

Acceptance: new unregistered images invoke inference, corrupt inputs remain
rejected, uploaded-byte hashes agree, known-sample scores retain parity, and no
UI approval prompt blocks results. Fresh evidence is recorded in PROGRESS.md.

## Authorized unverified-input repair - 2026-10-30

After a house/window upload received a DR grade, the user explicitly selected
**block unverified images**. Implement a fail-closed admission check before the
existing DR predictor: exact trusted retinal reference bytes or a trusted local
human modality-review record are required. Unknown inputs return HTTP 422 with
`prediction: null`; UI clears earlier scores and displays a review-required state.
Both raw and multipart API clients follow the same policy.

The policy lives in `inference/input_validation.py`, with a versioned reference
registry and local-only `scripts/review_retinal_image.py`. API schemas expose the
admission basis and limitation. No automatic modality/quality detector is claimed,
and no DR model, checkpoint or preprocessing change is authorized. A separately
validated retina/non-retina detector remains future work. This increment does not
rerun or change the saved evaluation.

Acceptance: unknown and misleadingly named images never invoke the predictor;
trusted/reviewed exact bytes are accepted; modified bytes require new review;
malformed policy records fail closed; accepted real-model scores retain parity;
UI rejection clears previous results; Postman examples explain both outcomes.

## Authorized local web/API increment

After the evaluation increment, the user requested an image-receiving web API and
a polished prediction interface, and specified that the calling application is
**another app on this computer**. This authorizes local single-image API/frontend
work from phases 6–7. It does not require remote hosting or evaluation jobs.

Implemented architecture: `retfound_platform/api/{app,schemas,uploads}.py` wraps
the existing `Predictor` in FastAPI lifespan with one inference executor and three
admitted request slots. It accepts bounded multipart or raw-image bodies entirely
in memory and serves an additive `frontend/` of HTML/CSS/JavaScript from the same
origin. API clients and UI share the same response contract; no prediction or metric
logic is duplicated in the frontend. The existing saved evaluation is a read-only
reference page. Model code and historical artifacts are preserved.

The frontend is buildless for this focused local workflow rather than the earlier
proposed React scaffold. API packages are pinned in `requirements-web.txt` and
installed in workspace-only `.runtime/web`; the working Conda model environment
is unchanged. New launch/setup scripts and `docs/API.md` document the supported path.
No Sites registration/publication is performed because the user specified a local
application and the real GPU model remains on this computer.

Acceptance: API lifecycle/upload/error/concurrency tests, UI interaction contract
checks, and real-model HTTP verification from a separate client process. Browser
visual QA is pending because the browser host/native pipe were unavailable.
Notebook, API evaluation jobs, persisted request history, authentication, network
deployment and React remain separate future work.

## Authorized evaluation increment — 2026-10-29

The user requested software to evaluate 1,000 images from the local APTOS2019 ZIP,
then clarified **evaluation first; API later**. This authorizes the dataset,
shared inference and evaluation/report pieces needed for that workflow (parts of
phases 2–4), not API, React, notebook, training, or deployment work.

The current ZIP is present and a fresh audit supersedes the earlier availability
finding: 2,048 train, 514 validation, and 1,100 test images decode; 1,036 test images
remain eligible under the new exact-hash/conflicting-label rules. The historical
981-image audit is preserved and is not reused as current evidence.

Architecture refinement: introduce the proposed package boundaries additively;
leave legacy Python entry points unchanged. `evaluation/reports.py` adapts the
existing HTML template in memory for an APTOS-only report. `scripts/evaluate_aptos.py`
and `run_aptos_evaluation.bat` provide a local launch path. `scripts/verify_inference.py`
is an opt-in real-checkpoint check. Tests use unittest and synthetic fixtures.
Only uniform deterministic sampling is implemented now. Proportional/balanced
sampling, legacy CLI refactoring, IDRiD fixes, dependency locking, notebook, API,
jobs and React remain deferred. Existing environment packages are used unchanged.

The initial plan below is retained as historical planning context. Its statements
that the ZIP/package are absent and that implementation must stop after inspection
describe the earlier inspection, not the newly authorized evaluation increment.

Inspection date: 2026-10-29 (Asia/Damascus). Phase 1 is complete. All other phases and paths marked proposed below are future work, not implemented functionality.

## 1. Existing project and reuse assessment

The project already has a functioning APTOS classifier and a reproducible small benchmark workflow. Extend those implementations behind shared contracts, preserving their entry points and historical artifacts.

| Existing path | Implementation and reuse decision |
| --- | --- |
| `README.md`, `BENCHMARK.md` | Windows launch instructions, upstream training/evaluation instructions, dataset/checkpoint source references. Keep; add platform instructions incrementally. Remote links were not revalidated in this phase. |
| `models_vit.py` | MAE ViT-Large with 16-pixel patches, 1024-dimensional embeddings, 24 blocks, 16 attention heads, global average pooling excluding the class token, then `fc_norm`. Reuse directly. Also contains DINOv2/v3 factories, outside the current APTOS platform scope. |
| `predict_aptos.py` | Trusted checkpoint CPU load with mmap, checkpoint-argument checks, strict state loading, CUDA/MPS/CPU selection, single-image and zero-input smoke modes. Best baseline for the shared inference service. Currently executes at import, so cannot be used as a service module unchanged. |
| `prepare_benchmark.py` | `RemoteZip` reads Google Drive ZIPs using HTTP ranges; maps named/numeric grades; excludes hidden entries; seeded uniform sampling; generated safe filenames; ZIP CRC checks; `.part` then rename; manifests; parallel downloads. Reuse source mapping and selection semantics, isolate network adapter later. |
| `evaluate_benchmark.py` | Loads the classifier once; evaluates 100 images sequentially; hashes images/checkpoint; computes metrics; writes CSV/JSON and fills HTML template. Reuse `digest`, metric definitions, provenance fields, and report generation after extraction into import-safe modules. |
| `evaluate_idrid.py` | Hugging Face streaming; first up-to-four images per grade by default or all rows with `--all`; strict loading; summary/CSV/confusion matrix/galleries. Preserve as legacy workflow, then align checkpoint/device handling in a later phase. Its subset is first-encountered per grade, not random sampling. |
| `util/datasets.py` | `ImageFolder` split loading and matching evaluation transform; optional uniform or proportional stratified **training** subsampling by ratio. Reuse transform behavior and sampling ideas; not a complete dataset validator or exact-size test sampler. |
| `main_finetune.py`, `engine_finetune.py` | Training/evaluation orchestration and broader metrics. Keep intact. Even `--eval` constructs all three datasets and training-related objects; the engine calls `model(images)` with CUDA autocast. It is not the verified platform inference path. |
| `util/misc.py`, `lr_decay.py`, `lr_sched.py`, `pos_embed.py` | Training/distributed utilities, checkpoint save/resume, scheduling, positional embeddings. Preserve; do not couple the platform service to optimizer or training state. |
| `benchmark_report.html` | Offline vanilla HTML/CSS/JS template; embedded JSON placeholder, dataset/outcome/grade/search filters, image dialog, five scores, confusion matrix, metrics and CSV export. Reuse report concepts and existing exporter; React can be additive. |
| `results/benchmark100/` | Saved 100-image JSON/CSV and generated standalone HTML. Preserve as historical evidence and parity inputs. |
| `results/idrid/`, `work_report.html` | Historical 103-image IDRiD evaluation, six galleries and matrix; narrative HTML summary with print support. Preserve; narrative claims do not supersede current inspection. |
| `latent_feature.ipynb` | Feature extraction example with direct resize and per-image channel normalization, non-strict loading and unresolved `dinov2_large` factory name. Not the classifier preprocessing or a ready evaluation notebook. |
| `examples/RETFound_MESSIDOR2_demo.ipynb` | Training/evaluation example for DINOv2/MESSIDOR2, with training cells and its own paths/kernel. Preserve; create a separate inference-only demonstration notebook later. |
| `aptos_zip_audit/` | Saved audit summary/issues and 981-row eligible manifest. Useful historical evidence; producing script and referenced ZIP are absent. Must not treat this as a reproducible current audit. |
| `run_prediction.bat`, `run_benchmark.bat` | Windows launchers use the `ml-homework` interpreter directly. Preserve. Benchmark launcher reruns evaluation and overwrites its fixed report directory. |
| `checkpoints/`, `weights/` | Existing fine-tuned classifier and separate pretraining weights. Keep immutable and distinct. |
| `.venv/`, `.venv-win/`, `.vscode/`, `__pycache__/` | Local environments, editor settings and generated cache, not application modules. Dependencies were inventoried, not audited line-by-line. |
| `report.pdf`, `Report_Arabic.pdf`, `RETFound-output.md`, `RETFound-output.txt` | Existing presentation/export artifacts. Inventoried and preserved; PDFs were not rendered or validated, and old source exports were not used instead of current code. |

No platform package, FastAPI application, React package, dedicated platform evaluation notebook, automated test suite, or reproducible environment lock was found in the application tree at inspection.

## 2. Exact current inference contract

The selected classifier is `checkpoints/checkpoints/APTOS2019/checkpoint-best.pth` (3,639,988,647 bytes). Both prediction and benchmark scripts also support the flatter `checkpoints/APTOS2019/checkpoint-best.pth` layout. The checked SHA-256 is `a96b9dbcb78eff373912fb0a48d316dc35ffb0715bb2a1b9128b096d780edbbf`, matching the saved benchmark report.

Both scripts read `checkpoint['args']`, require five classes, 224 input size and global pooling, create `RETFound_mae`, and load `checkpoint['model']` with `strict=True`. `torch.load(..., map_location='cpu', mmap=True, weights_only=False)` is used for this trusted local checkpoint. A future API must not expose arbitrary checkpoint deserialization.

The image pipeline is Pillow RGB conversion -> bicubic shorter-edge resize to 256 -> center crop 224 -> tensor in [0, 1] -> ImageNet normalization. Means are `(0.485, 0.456, 0.406)` and standard deviations `(0.229, 0.224, 0.225)`. There is no current EXIF transpose or fundus-specific enhancement. `util.datasets.build_transform` reproduces this evaluation transform at input size 224.

Inference runs under `eval()` and `inference_mode()`: `forward_features` returns pooled features, then flatten all non-batch dimensions and call the classifier head. The required output is finite `(N, 5)` logits. Softmax produces five uncalibrated scores; argmax maps to grades 0..4. Keep this path during extraction because generic `model(x)` is not the compatibility path verified by the dedicated scripts.

## 3. Dataset and evaluation findings

- Current local benchmark: 34 APTOS2019, 33 IDRID and 33 MESSIDOR2 images, with manifests and archive entry listings. Recorded source test pools contain 1,100 / 103 / 526 images. Selection is `random.Random(20261023).sample(sorted_test_paths, count)` without replacement, followed by sorting the selection.
- Cache reuse checks image count and file existence, not hashes, decoding, seed/source compatibility, or semantic equivalence of a changed manifest. New validation must address those gaps without changing historical files.
- The benchmark verifies 100 distinct dataset/archive paths, hashes selected images and reports duplicate counts. It does not perform complete train/validation overlap exclusion before selecting images.
- The stored ZIP audit reports 2,048 train, 514 validation, 1,100 test entries; 1,042 valid test files, 58 read/structure errors, six test duplicate hash groups and 49 test hashes shared with train/validation. It reports **981 eligible test images**, so its 1,000 target is not met. Some duplicate groups have conflicting grade folders. Preserve the report's exclusion accounting; do not derive eligibility by subtracting overlapping counters.
- The audit's `APTOS2019.zip` is absent now, as is `audit_aptos_1000 (1).py` previously discussed in chat. No full extracted train/val/test dataset was found inside this project. The old eligible manifest alone cannot prove source availability or a clean current dataset.
- Exact-byte checks cannot establish patient independence, near-duplicate absence or checkpoint-matched split provenance. New reports must represent these as separate verification states.
- Existing benchmark metrics: accuracy, fixed-five-label macro F1 (`zero_division=0`), quadratic weighted kappa, 5x5 confusion matrix, class counts, and any-DR accuracy/sensitivity/specificity with counts TN/FP/FN/TP. Any-DR uses argmax grade > 0. Broader engine metrics are separate and use unweighted kappa plus ROC/PR-related calculations.
- Empty input and degenerate kappa/AUC require defined handling before metrics are generalized. Current benchmark JSON forbids NaN, so a degenerate kappa can prevent output. Mixed-dataset totals must not obscure per-dataset transfer performance.

## 4. Proposed modular architecture

The following paths do not exist yet. Introduce them in the phases below; keep upstream modules and command-line entry points at their current locations.

```text
retfound_platform/
  __init__.py
  config.py                 # explicit roots, device/model settings; no I/O on import
  contracts.py              # framework-independent records, schema versions
  datasets/
    __init__.py
    labels.py               # canonical grades and explicit source aliases
    sources.py              # local folder/ZIP adapters; remote adapter later
    validation.py           # structure, decode, duplicates, split overlap
    manifests.py            # validated manifest serialization and identities
    sampling.py             # deterministic uniform/stratified/balanced selection
  inference/
    __init__.py
    preprocessing.py        # single versioned evaluation transform
    loader.py               # path/config/hash checks and strict model loading
    predictor.py            # reusable single/batch inference service
  evaluation/
    __init__.py
    metrics.py              # pure metrics with explicit edge-case policy
    runner.py               # joins labeled manifests to predictions
    reports.py              # JSON/CSV and existing HTML template adapter
  api/
    __init__.py
    app.py                  # FastAPI lifecycle and routes
    schemas.py              # request/response schemas around core contracts
    jobs.py                 # bounded evaluation queue and persisted job states
scripts/
  validate_dataset.py
  sample_dataset.py
notebooks/
  RETFound_Evaluation_Demo.ipynb
frontend/                   # future React + TypeScript application
tests/                      # fast synthetic-fixture tests + opt-in integration
requirements-platform.txt  # independently validated runtime dependencies
requirements-dev.txt
```

Dependency direction: CLI/notebook/API -> shared dataset, inference and evaluation modules -> existing `models_vit.py` and installed libraries. React communicates with the API; it never loads checkpoints or computes authoritative metrics. The domain modules do not depend on FastAPI or React. Keep the existing offline HTML export available independently of the frontend.

### Contracts and persistence

| Proposed contract | Required information |
| --- | --- |
| Dataset record | Dataset/source ID, source-relative path or ZIP member, stable sample ID, split, integer grade, image hash, dimensions, validation outcome and exclusion reasons; optional patient ID only when supplied by the source. |
| Audit result | Source fingerprint, schema version, class map, split/grade counts, corrupt files, duplicates, conflicting labels, cross-split overlaps, eligible rows; status of exact, patient and near-duplicate checks separately. |
| Sample manifest | Audit/source identity, method, seed, requested/selected count, per-grade allocation, ordered sample IDs/hashes and exclusions. No image mutation. |
| Prediction | Sample ID/hash, predicted grade, five ordered scores, checkpoint hash, preprocessing version and actual device; timing/error information where applicable. Ground truth is joined by evaluation, not guessed by inference. |
| Evaluation run | Run ID, source/sample manifest identity, model/runtime identity, success/failure counts, per-dataset metrics, aggregate metrics with interpretation, artifact paths and UTC timestamp. |

Use JSON manifests and CSV exports initially, with new outputs under a configurable run directory such as `results/runs/<run_id>/`. Write completed artifacts atomically. Persist job metadata/status separately from immutable completed results; a small local SQLite job store is sufficient for a later single-host API. Carry manifest/schema versions so existing benchmark JSON can be adapted rather than silently rewritten.

### Dataset validation and sampling

Validate before selecting. Local folders and ZIPs should feed a common record iterator. Reject unknown grades, unsafe paths and unreadable images with explicit records. Check actual decoding and ZIP CRC where applicable. Hash all required splits for exact overlap detection; test-only inputs must record that train/val evidence is unavailable. Quarantine all conflicting-label duplicate groups and use a documented representative rule for same-label duplicates. Avoid full extraction when a safe stream suffices, and bound archive expansion/image dimensions.

Support uniform sampling first, preserving the legacy algorithm. Add proportional stratification with deterministic remainder allocation and an explicitly named balanced demonstration mode. For an oversized request, fail with eligible counts and reasons; do not silently reduce the target. The user can then select a smaller target or provide a repaired source for a new audit. Never alter source splits to manufacture 1,000 eligible test images.

### RETFound inference and evaluation

Create one import-safe loader and transform; start with single-image and modest batch float32 inference. Keep CUDA selection explicit, allow CPU fallback by policy, report failures rather than hiding them, and serialize access to one GPU model initially. Batch size must be bounded and tuned on the actual laptop; no throughput claim exists yet.

Extract metrics without changing legacy definitions. New metrics may include per-class precision/recall/F1 and score-based AUC only when their inputs are defined. Return `null` and a reason for undefined quantities. Include class support in every report. Do not fit thresholds or choose preprocessing on the evaluation test set. Preserve the HTML template interface via an adapter and validate saved-result parity before altering legacy entry points.

### FastAPI (later phase only)

Load the model during application lifespan, not import and not per request. Start with one application worker owning one GPU model and a bounded work queue; do not block async request handling with an inline long-running GPU job. Persist evaluation job status and mark interrupted jobs explicitly after restart.

Proposed routes: `GET /health`, `GET /model`, `POST /predict`, `POST /datasets/validate`, `POST /samples`, `POST /evaluations`, `GET /evaluations/{run_id}`, and `GET /evaluations/{run_id}/artifacts/{name}`. Long validation/evaluation requests return a job ID/status; define exact schemas in that phase. Use configured dataset IDs and safe artifact identifiers rather than arbitrary client filesystem paths. Validate decoded upload content, size/pixel limits and filename handling. Configure CORS explicitly for the local frontend. Keep local demo binding as the default; wider deployment/authentication is a separate decision.

### Notebook and React (later phases only)

The new notebook should show environment identity, validated dataset evidence, deterministic sample selection, shared inference, per-dataset metrics and error review. It must use the same package as the API, contain no training commands or automatic downloads, and run from a fresh `ml-homework` kernel with explicit paths.

React + TypeScript should provide dataset/audit status, sample configuration, image prediction, evaluation progress, dataset-specific results, confusion matrices, searchable galleries, five-score detail and exports. Reuse the existing report's information design. Include empty/error/loading states, keyboard support and clearly separated ground truth/prediction. Plan Arabic/English strings and RTL support for the demonstration, with wording reviewed before presentation. Derive API types from the eventual schema; do not hardcode demonstration results as live predictions.

## 5. Implementation phases and acceptance criteria

| Phase | Scope | Acceptance evidence |
| --- | --- | --- |
| 1 - Inspection and documentation | Current phase: inventory, trace source/data/report flows, read-only verification, three requested documents. | Actual commands and results in `PROGRESS.md`; original application sources preserved. Stop here. |
| 2 - Dataset foundation and reproducible sampling | New contracts/configuration, local folder/ZIP validation, manifest persistence, seeded sampling CLIs, synthetic-fixture tests. Reconcile missing full dataset and audit provenance when source becomes available. | Known corrupt/duplicate/conflicting-label/overlap fixtures excluded correctly; aliases map to 0..4; path escapes rejected; identical source+seed gives identical sample; 1,000-from-981 request fails clearly. Real-data validation remains pending if source is unavailable. |
| 3 - Shared inference extraction | Add loader/preprocessor/predictor around existing MAE; then make prediction CLI a thin guarded entry point preserving behavior. Add validated dependency specs without upgrading the working environment blindly. | Strict load, verified checkpoint identity, preprocessing tensor parity and same-device prediction parity against baseline; invalid images/configs and batch shapes tested. CPU path checked separately; CUDA performance measured rather than assumed. |
| 4 - Shared evaluation and legacy adapters | Add metrics/runner/reports, versioned run outputs; then adapt benchmark/preparation and IDRiD scripts. Fix IDRiD nested path/CUDA handling while retaining defaults/output semantics. | Saved JSON metric parity, defined edge cases, CSV/HTML consistency, no overwrite of baseline artifacts; new real run only on an explicitly validated manifest. |
| 5 - Reproducible notebook | Add inference-only notebook using shared modules. | Fresh-kernel execution on a declared dataset; same sample IDs/predictions/metrics as CLI; no training or downloads. |
| 6 - FastAPI | Lifecycle, schemas, bounded inference/jobs, errors, artifacts and local configuration. | Contract/lifecycle/upload/path tests, one model per worker, concurrent request behavior and restart semantics; optional real-model integration test clearly identified. |
| 7 - React frontend | Add API-driven UI preserving report capabilities, bilingual/RTL preparation and error/progress states. | Browser workflow checks against API; filters/export counts agree with backend; no frontend-derived authoritative metrics or fabricated results. |
| 8 - Demonstration integration | End-to-end local launch, reproducibility instructions, report export and rehearsal. | Documented startup from a clean session, traceable dataset/model/run IDs, measured timing, verified offline behavior for the agreed workflow and honest limitations. No training. |

Dependencies: phase 2 precedes trustworthy new dataset evaluation; phase 3 precedes phases 4-6; phase 7 depends on phase 6 contracts. Do not implement later phases merely because they appear in this plan.

## 6. Exact next-phase file scope

**Phase 2 modifies existing `README.md`, `docs/IMPLEMENTATION_PLAN.md`, and `docs/PROGRESS.md` only**, to document the new validation/sampling commands and evidence. Amend `AGENTS.md` only if an established convention changes. No existing Python script needs modification in phase 2.

Create these proposed files in phase 2:

```text
retfound_platform/__init__.py
retfound_platform/config.py
retfound_platform/contracts.py
retfound_platform/datasets/__init__.py
retfound_platform/datasets/labels.py
retfound_platform/datasets/sources.py
retfound_platform/datasets/validation.py
retfound_platform/datasets/manifests.py
retfound_platform/datasets/sampling.py
scripts/validate_dataset.py
scripts/sample_dataset.py
tests/__init__.py
tests/test_dataset_validation.py
tests/test_sampling.py
```

Use standard-library `unittest` plus the already installed Pillow for phase 2 fixtures unless a later dependency decision requires otherwise. No FastAPI, React, checkpoint edits, training, network downloader rewrite, or notebook rewrite belongs in that phase. The missing real dataset does not prevent implementation/testing against synthetic fixtures, but it prevents claiming a completed real APTOS audit.

Later modifications are explicitly deferred: `predict_aptos.py` in phase 3; `prepare_benchmark.py`, `evaluate_benchmark.py`, `evaluate_idrid.py` and, only as needed for report compatibility, `benchmark_report.html` in phase 4. Keep `models_vit.py`, checkpoint files, training code and original notebooks unchanged unless a separately justified issue requires a narrowly reviewed change.
