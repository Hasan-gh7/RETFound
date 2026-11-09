# Project progress and handoff

## Source-only GitHub preparation — 2026-11-09

Authorized publication hygiene completed without Git initialization, staging,
commits, remote changes, uploads, installs, service restarts, or inference.

- Extended `.gitignore` to exclude weights/checkpoints and model binaries,
  dataset/benchmark assets, all `results/`, `aptos_zip_audit/`, upload demo assets,
  ZIPs/archives, historical source exports, large local cleanup inventories,
  Python environments, runtime/dependency trees, credentials and database backups.
  `.env.example` remains included. Original local data/assets are retained.
- Removed LFS filters from `.gitattributes`; small included images use ordinary
  Git. Evaluation/preparation scripts and the report template remain included.
- Replaced exactly one exposed OpenRouter credential in each of `docs/API.md`,
  root `RETFound-output.md`/`.txt`, and `archive/source-exports/RETFound-output.md`/
  `.txt` with a hidden-input prompt description. Byte replacement preserved all
  other file content. No secret value was printed or copied into a new artifact.
- Updated `README.md` with source-only distribution and fresh-clone requirements;
  recorded this limited scope in `docs/IMPLEMENTATION_PLAN.md`.

Verification used PowerShell and stdin-only Python scripts through
`C:\Users\jadgh\.conda\envs\ml-homework\python.exe -B -`, plus
`git check-ignore --no-index -z --stdin`, `git check-attr filter`, and read-only Git
inventory commands. All 18 actual/hypothetical exclusion checks passed; expected
source files and `.env.example` remained eligible. Publication candidates total
280 files, approximately 7.25 MiB; none is 5 MiB or larger (largest: `report.pdf`,
970,956 bytes). Scanning 250 eligible UTF-8 files found no matches for recognized
OpenRouter/OpenAI/GitHub/AWS token or private-key patterns; the five sanitized
files were also checked explicitly, including the now-ignored exports. This is
a bounded pattern scan, not proof that every possible secret format is absent.
Existing weights, checkpoint, dataset ZIP, benchmark inputs/reports, historical
snapshot, and both inspected local environment markers still exist.

No model/application tests were run for these publication-only changes. Existing
runtime readiness claims are unchanged. The folder still has no local `.git`;
fresh `git rev-parse --show-toplevel` resolves to `C:/Users/jadgh/Desktop/Dr 4`,
and the parent index lists no tracked files for this project, superseding the
historical gitlink observation. Parent Git metadata was not repaired or modified.
The owner must revoke/replace the exposed provider credential if active; this
preparation neither contacted the provider nor rewrote any previous publication.

## Phase3 two-defect corrections — 2026-11-07

Corrected cross-project image/person reviewer/adjudicator separation (both directions,
Phase3A, SQL and concurrency) and identity-based reviewer-pair kappa reporting.
Additive0005 changes guards only, tested on disposable PostgreSQL with115 passing
tests (previous103 +12;0 failures/errors/skips). Existing rows/triggers survived a
populated0004 upgrade. Live database/services and model files remain unchanged.
Browser automation is disabled; fresh browser/deployed acceptance remains pending
approved migration/restart. See [corrective report](../clinical_database/docs/PHASE3_DEFECT_FIXES.md).
Historical completion claims below are superseded by this deployment qualification.
No Phase4 work was authorized or performed.

## Phase3 acceptance recheck —2026-11-06

Fresh source audit corrected filter persistence, history/current-head pagination,
closed-state controls, account audit access, partial operational metrics and a
concurrent coordinator withdrawal race.103tests passed (all previous96 included),
with a fresh complete synthetic browser workflow and successful22-table backup
restore verification. Every pre-existing row/protected source hash matched; the
APTOS15pilot and prior Phase3 history remain unchanged. No schema change beyond
existing0004, no model/weight/inference/evaluation or Phase4 work. Only new synthetic
QA evidence added; QA identities retired/projectclosed. See
[current acceptance report](../clinical_database/docs/PHASE3_ACCEPTANCE.md) for the
15-criterion matrix, evidence, startup commands and remaining institutional gates.

## Clinical research Phase 3B–G — 2026-11-06

Completed the requested remaining research workflow in clinical_database and the
existing /review frontend: six local roles, database-backed named accounts,
projects/assignments, blind own drafts/finals, locked comparison, agreement metrics,
immutable adjudication and versioned research references with independent explicit
approval. Additive0004 now23tables; old migrations/guards preserved. Clinical
verification remains prohibited for synthetic assets/unverified local qualifications.
All previous67tests plus29newtests are exercised; browser end-to-end disagreement,
agreement/ungradable paths, Arabic/mobile/keyboard and explicit research approval
passed. Backup restore and all original-row/protected-source fingerprints matched.
The 15APTOS imports/memberships and prior synthetic history remain intact; only
three synthetic illustrations eligible, no GroundTruth created, no model work.
Five QA accounts retired/project closed. Existing reviewer account preserved.
Details/evidence/commands: [Phase3 report](../clinical_database/docs/PHASE3_IMPLEMENTATION_REPORT.md).
No Phase4 training or model integration was begun.

## Clinical review startup repair

Successful login with queue 503 traced to the stopped native clinical PostgreSQL
cluster. Started the existing loopback 55432 database without recreating data or
restarting API/model processes. Fresh health returned ready/0003; image/import counts
preserved. Added read-only health diagnostic and database startup instructions in
clinical_database/docs/CLINICAL_REVIEW.md. No model code or data changes.

## Independent clinical review Phase 3A — 2026-11-06

Completed `/review` on clinical API 8010 with the existing frontend's plain JS and
shared CSS: bilingual responsive queue/viewer, zoom/pan, quality/DR/separate DME,
confirmation, append-only personal history/revisions and session authentication.
Blind responses exclude source labels, predictions and other reviewers' labels.
Additive migration 0003 extends existing annotations and adds synthetic-only display
eligibility. Three project-created synthetic illustrations are eligible; original
15 APTOS/provenance records are unchanged and have no display grants. Two synthetic
QA annotations remain unverified with null grades; no Ground Truth created. QA
account disabled. All previous 50 tests plus 17 review tests passed (67 total), and
browser desktop/Arabic/mobile submission/revision checks passed. Only metadata API
was restarted; no model code, weights, requests or environment-file changes.
No claim of fresh model-service health. Development account setup and institutional
authentication limitations: [clinical review guide](../clinical_database/docs/CLINICAL_REVIEW.md).
Detailed evidence: [clinical progress](../clinical_database/docs/PROGRESS.md).
Phase 3A stops here; real-image grants, consensus and production use remain deferred.

## Independent clinical ingestion Phase 2A — 2026-11-06

Implemented bounded, auditable folder/ZIP public-dataset ingestion entirely inside
clinical_database/, with additive 0002 import provenance tables, explicit source
mapping, SELECT-only previews, duplicate/quarantine reports, original-byte storage,
idempotent execution, and authenticated configured-source API extensions. No
model/inference/frontend/weights/evaluation/source-image changes or requests.
Local APTOS ZIP exists (3,662 images, AutoMorph-preprocessed); dry-run checked 15
train images: all valid/mapped, no selected/catalog duplicates. Unknown patient/
laterality/consent/capture facts remain unknown; no clinical labels are fabricated.
All 50 synthetic PostgreSQL tests passed (31 original + 19 ingestion, 12.882s).
After explicit user approval, applied additive 0002 and imported exactly 15 train
images into 1 new draft version, with 0 duplicates/quarantines and no patients or
clinical annotations/adjudications. Repeated execution left all table counts
unchanged. Restarted ONLY clinical API 8010; model/UI listener owners stayed the
same. Fresh authenticated live listing/status/statistics passed, errors were zero,
unauthenticated reads returned 401 and both write routes now return 403. `.env`
and source ZIP are unchanged. Live source/import gates are disabled again.
Exact scope, commands, evidence, actual import count and limitations are maintained
in clinical_database/docs/PROGRESS.md and docs/DATASET_INGESTION.md there.

## Independent clinical database foundation Phase 1 — 2026-11-06

Implemented the user's pasted clinical database Phase 1 in `clinical_database/`,
as explicitly requested for isolation from the running server. All new code,
dependencies, configuration, migrations, tests, storage design and database docs
are inside that folder. Existing application/model/frontend/launcher sources,
working Conda environment, datasets, checkpoints and historical results were not
modified, imported for inference, restarted or used for model/provider requests.
Root documentation changes are limited to this entry and the plan scope pointer.

Schema: 12 requested tables, UUID/FK/grade/status/hash constraints, append-only
clinical and provenance history, exact truth-revision pins, false-only training
approval, serialized membership/patient split checks, derivative split checks,
frozen-version protection and database-triggered audits. Independent FastAPI
factory/reusable router supplies the five `/api/v1/data` endpoints; it is not
mounted into the existing app. Bearer protects all source/image access; source
POST is additionally opt-in development-only. No upload/review API or source
medical-image import. `ImageStorage` defines a future S3 adapter contract; only
the bounded, byte-preserving local backend is implemented.

Initial migration `0001_clinical` uses static SQL tables/guards, refuses nonempty
unmanaged databases, and disables destructive downgrade. Native PostgreSQL 16.14
was used in fresh random-port disposable loopback clusters, never an existing
database. Separate `.venv` is Python 3.10.19; isolated package installation needed
approved network access. Docker CLI exists but Compose runtime was not exercised.
Initial sandbox initdb stalled; the first unrestricted harness run exposed Windows
inherited pipe handles. Stopped only task-owned test processes/cluster and corrected
lifecycle logging to files. The next suite passed 23 tests, then an expanded suite
passed 29 tests in 6.909s. Final logged verification passed all 31 tests with zero
failures/errors/skips (8.800s unittest, 8.814s runner wall time); metadata/migration
parity, pip dependency check and Python/PowerShell syntax also passed. Final test
cluster shutdown was confirmed by its log and absent postmaster.pid. Full evidence
is in the independent progress document below. These are synthetic checks, not
model/clinical validation.

Exact verification command from `clinical_database/`:
`.\.venv\Scripts\python.exe -B scripts/test_postgres.py` (outside sandbox for native
PostgreSQL child processes). Runner upgrades twice, runs tests and stops its owned
cluster in finally. Test data/logs remain under ignored `.runtime/test-<uuid>/`.
See `clinical_database/docs/PROGRESS.md` for final evidence, changed paths and
limitations; `clinical_database/README.md` contains exact PowerShell/Anaconda setup,
native/Compose startup, migration and port-8010 metadata API commands.

Phase 1 only. No development database or API is left running. Production RBAC,
audit hardening, privacy/de-identification, approved hospital governance, storage
operations and integration into the running service remain future work. The
parent Git gitlink/no-local-metadata issue is preserved; no Git repair attempted.

## Clear Jev rejection message for Telegram - 2026-11-06

Changed shared not_retinal_fundus error.message to clear Arabic instructions
to submit a fundus image and state that no DR analysis ran. Retained HTTP 422,
stable error.code, prediction:null and gate decision metadata for both full and
summary endpoints. Extended summary test checks wording/code/no RETFound on
rejection. Added bot response formatter guidance distinguishing Jev rejection
from unreadable images, provider unavailability, busy and non-JSON tunnel errors.
Actual Telegram bot code is external and still must read the error JSON body;
no messages sent or provider/model inference requested by this change.
Verification: two focused synthetic API tests passed in ml-homework outside
sandbox (0.520s), covering rejection text and fail-closed gate behavior.

## Telegram summary and dataset preview optimization - 2026-11-06

User supplied successful Telegram prediction (request b0b29028cab0445f9143e0e9de6014f3,
server 9281.81ms) and requested clear classification/scores and faster dataset UI.
This is user-provided evidence, not fresh execution. Added POST /api/predict/summary
with existing auth/capacity/rate limit and single shared prediction; only grade,
label and five named percentage scores returned on success. Existing /api/predict
retained; errors remain blocking. Added full-response timing_ms for Jev/RETFound
and UI display. No claim that predicted class is verified ground truth.

Added hash-validated /api/demo/{id}/thumbnail and catalog thumbnail_url. Frontend
loads 320px quality-75 JPEG previews; originals remain unchanged and used for
prediction. Enabled routes in public allowlist and site proxy. Measured in-memory
rendering across actual 15 source files: original 8,188,943 bytes vs thumbnails
92,011 bytes (98.88% reduction). This is payload size, not measured network latency.
No image sent to a provider, no training or historical source/output mutation.

All 20 synthetic API tests passed (3.473s) including summary schema/percentages,
rejection, preview dimensions and no inference on preview. Dataset JS fixture
tests and Node syntax passed. Added docs/TELEGRAM_RESPONSE_AR.md with endpoint and
bot message formatter; colleague must change bot request/display code. Live
provider timings and browser latency remain unmeasured. Restart needed for new
routes. No cached/fake predictions or bypass of Jev introduced.

## Fix website startup depending on external HTML fetch - 2026-11-05

User supplied launcher failure on port 8002 after successful external health.
Read session 20261105-211616-6e3fc3 logs: site requests reached response writes
then raised WinError 10053 after client disconnect; Eye AI loaded successfully.
Launcher probes used two-second timeout while site root proxied via Cloudflare.
This unnecessarily made UI startup dependent on remote HTML latency and caused
whole-session teardown when its probes failed (then public 1033 was expected).

serve_site.py now serves exact-allowlisted original frontend files locally with
explicit MIME types; all API/data/schema requests still use configured external
HTTPS and server-side Bearer. Client disconnects no longer attempt a second
error response. Launcher checks UI child exit while waiting for startup.
Extended synthetic proxy test verifies root/JS/CSS/dataset page load within
two seconds without ANY upstream request, while health/prediction forwarding,
private headers and origin/path denial remain covered. Passed in ml-homework
outside sandbox (0.757s); both scripts passed AST syntax checks. No model/provider
requests or live combined restart executed. User's prior process already exited.

## Delayed DNS startup recovery - 2026-11-05

Screenshot showed ERR_NAME_NOT_RESOLVED for current mechanisms-stations-cgi-
evaluated.trycloudflare.com. Fresh approved checks found both local model and
external authenticated health 200 ready, but no listeners on 8001/8002. Session
20261105-204445-2464b7 had only model/tunnel logs. Launcher previously gave up UI
startup after its initial bounded public-readiness attempts, even if tunnel
became usable later. Replaced that with continued bounded individual GET checks,
periodic status and child-liveness checks until ready or Ctrl+C. Syntax passed;
new wait path not independently live-exercised yet.

Recovered current session without restarting model: launched Eye AI PID 12140
and site proxy PID 308 hidden. Logs are eye-ai.{stdout,stderr}.log and
site.{stdout,stderr}.log in that session. Fresh GET / and /api/health returned
200 on BOTH ports 8001 and 8002. Eye AI reported actual upstream cuda/float32
model identity. No image/prediction/provider request. These two recovery children
are independent of the already-running launcher; verify identity and stop them
before a later combined restart. User's model/tunnel left running. Browser DNS
failure not claimed to be independently resolved; local adapters avoid requiring
browser DNS for the remote hostname while using the external API server-side.

## Eye AI identity correction and two independent clients - 2026-11-05

User identified eye-ai-demo (existing nested project), not dataset-tests. Read
its plan/progress, launcher, adapter, dependencies and frontend. Existing adapter
already forwards original images but previously ignored connection.json base_url.
Now it reads URL+key together, prefers a demo-local connection.json when copied
to another machine, and retains explicit environment overrides. Added ignore
rule for private file, portable Python fallback in Windows launcher and help text.

Added scripts/serve_site.py: stdlib loopback-only original-site proxy on 8002,
fixed configured HTTPS upstream, server-only Bearer, explicit route/Host/Origin
checks, upload/response limits, redirects disabled and no retries. It serves an
empty demo-auth.js so browser needs no credential. Site API traffic uses public
upstream; no model or metric duplication. share_api.py starts Eye AI on 8001 and
site on 8002 after public health, opens both, checks port conflicts, cleans owned
children, and supports --api-only. OpenRouter not passed to UI children. See
docs/TWO_APPS_AR.md for host and colleague commands and connection-file handoff.

Synthetic proxy test passed (0.588s), including original bytes, hidden key and
cross-origin/unknown-route rejection. Existing Eye AI adapter 10 tests passed
(3.975s) and Node frontend checks passed. Syntax checks passed. Connection-file
selection check initially failed sandbox temp writes, then approved rerun passed.
Fresh external GET health returned 530; live combined startup cannot be claimed.
No inference/provider calls, model changes, installs or historical data changes.
User must launch new session with private OpenRouter input; remote colleague
must receive refreshed connection.json after URL/key rotation. No automatic
cross-device config sync or independent public hosting is implied.

## Stopped demo diagnosis and startup readiness - 2026-11-05

Fresh approved network checks: localhost:8000 refused all connections; current
public hostname returned 530. Session 20261105-124315-62741f tunnel log records
graceful shutdown from interrupt at 09:45:48 UTC. No active demo established.
Launcher now checks authenticated public health before opening browser (bounded
attempts); on failure leaves the processes running and prints troubleshooting
status. Added missing input-validation.css to public UI allowlist. Focused full
demo synthetic API test passed (2.189s); launcher AST passed. No model/provider
request or restart performed: private user OpenRouter input required. Public
readiness startup path not yet live-tested. No historical evidence changed.

## Complete original UI over external API - 2026-11-05

User clarified they need original pages, not only the simplified upload demo.
Added opt-in Settings.public_demo / serve_web.py --public-demo. share_api.py now
enables it and opens the external root URL. Public allowlisted UI assets contain
no credentials; API data, images, saved evaluation, schema and predictions stay
Bearer-protected. Public full-demo limit is 30/minute; API-only remains 10/minute.
Single executor, three slots, existing provider and model contracts remain.

Added frontend/demo-auth.js before original module scripts. Login collects the
RETFound key (not OpenRouter) into sessionStorage for this tab. Fetch adapter
attaches it only to same-origin /api/ calls and clears it on 401 without retries.
Initial GET timeouts that expire during login receive a fresh timeout. Dataset
previews use authenticated blob fetches. Both original pages retain local mode
through an empty authentication script response. Updated launcher, API tests,
dataset UI fixture, plan and temporary API documentation.

All 18 prior API tests passed in ml-homework outside sandbox (13.954s); new
complete-public-demo test passed (3.308s), covering assets, denial without key,
catalog/previews/evaluation/schema and synthetic demo prediction. Existing main
UI test and updated dataset UI test passed, including no automatic inference.
Initial dataset test assumed previews did not use fetch; updated to model image
GETs separately from prediction POSTs. Corrected incidental Windows encoding
conversion in dataset JS before final checks. Node syntax checks passed.
No live inference or restart performed; user's credential-bearing server must
restart via share_api.py to activate new mode. Browser rendering/integration
remain unverified. No weights, training, datasets or saved reports changed.

## External upload demo - 2026-11-05

Added frontend/external-demo.html and .js and explicit API routes for these
public static assets. User enters RETFound access key in memory; health and
multipart image calls use the same-origin external API with Bearer auth.
No automatic inference, key persistence or retry; uncertain outcomes block
further predictions. API remains protected, other demo/evaluation routes hidden.
Authenticated public mode accepts Origin headers despite localhost Host rewriting;
local origin checks and explicit CORS remain. Launcher prints /external-demo URL.
Updated plan and temporary API instructions. Original local UI unchanged.

Node syntax check passed; all 18 synthetic API tests passed in ml-homework
outside sandbox (15.609s). Focused updated test passed (2.486s), verifying public
assets contain no key, API rejects missing key, authenticated external Origin
works and rate limiting remains. No live provider/model calls or browser visual
test. Running server requires user restart with private OpenRouter input before
new routes are available. No checkpoint/dataset/historical run changes.

## Stable current connection file - 2026-11-04

User narrowed request to immediate connection.json updates only. share_api.py
now atomically replaces .runtime/tunnel/connection.json when a new URL/session
credential is generated, retaining per-session connection files. Populated the
stable file now from 20261104-220502-7a9129/connection.json and verified JSON
equality without printing credentials. Launcher AST syntax passed. No server
restart, network requests or collection changes; next launcher execution uses
the new automatic write. Already imported Postman copies are not synchronized.

## API-only colleague collection - 2026-11-04

Created private runtime RETFound_API_ONLY.postman_collection.json in session
20261104-183511-867c46 with only POST /api/predict and recovered URL/session key.
Instructions distinguish RETFound Bearer access from host OPENROUTER_API_KEY.
Current server does not accept caller-specific OpenRouter credentials. Using a
different provider account requires host configuration/restart and refreshed
connection details. JSON parse/single-request checks passed; no new network,
provider requests or server changes, and current tunnel liveness not rechecked.

## Temporary tunnel recovery - 2026-11-04

Postman screenshot showed ENOTFOUND. Approved external DNS check confirmed old
hostname does not exist; old tunnel log reports Unauthorized: Tunnel not found.
No cloudflared process remained, while model server PID 28432 still listened on
127.0.0.1:8000. Started replacement tunnel PID 16784 hidden, reusing that server
and its session key. New rocks-resulted-fisher-vampire.trycloudflare.com returned
authenticated health 200 ready. No inference/provider call. Recovery logs and
new connection-recovered.json / RETFound_Public_API_recovered.postman_collection.json
are in .runtime/tunnel/20261104-183511-867c46; original files preserved.
Replacement tunnel is independently launched: stopping it requires stopping
PID 16784 (verify process identity first); original launcher does not own it.
Existing model server remains user-owned. Full prediction not repeated.

## Private Postman collection - 2026-11-04

Created .runtime/tunnel/20261104-183511-867c46/RETFound_Public_API.postman_collection.json
at user request. Six requests cover health, model, multipart prediction, alternative
raw JPEG prediction, unauthenticated rejection and private-route rejection. Includes
current URL/session Bearer key from connection.json in ignored runtime only; no
OpenRouter credential. Instructions explain file selection, 120000 ms timeout,
individual requests, session lifetime and errors. Parsed JSON and checked request
count/auth-variable wiring/multipart headers with ml-homework. No new HTTP or paid
requests; Postman UI import was not executed. Existing local collection preserved.

## Public tunnel live verification - 2026-11-04

User launched share_api.py with their privately entered OpenRouter key. Verified
the supplied public HTTPS hostname via urllib using ml-homework outside the
network sandbox (initial sandbox DNS failed). Unauthenticated health returned
401; authenticated health returned 200 ready. One POST of existing
sample_images/idrid_test.jpg returned 200, Jev accepted, real CUDA float32
RETFound grade 0 and five scores. Client duration 55.99 seconds; server elapsed
21314.24 ms. These measure different scopes; no throughput claim. Evidence:
.runtime/tunnel/20261104-183511-867c46/external-verification.json (no access key).
Request ID 90b3d492bd28476f81e156da975da78e. Public routing was tested from this
machine through Cloudflare, not independently from the colleague's network.
No retry or shutdown test performed; user's session remains running. No weights,
training data or historical outputs modified. Colleague integration remains to
be exercised with the private session connection.json.

## Temporary external API trial preparation - 2026-11-04

User authorized a temporary external integration trial with a colleague's
application/Telegram bot, not continuous hosting. Inspected current progress,
plan, API, launcher, tests, dependency bootstrap and provider-key handling.
No listener on port 8000 or cloudflared executable was found; the agent's
ml-homework environment has no OPENROUTER_API_KEY. No existing server stopped.

Added opt-in public_api/api_key settings to retfound_platform/api/app.py and
--public-api to scripts/serve_web.py. Public mode requires a >=32-character
Bearer key, allows only health/model/predict, and bounds authenticated prediction
submissions to 10/minute before model/provider calls. Existing three admission
slots and single executor remain. Local mode stays unchanged. CORS permits the
Authorization header for explicitly configured origins; no new origin enabled.

Added scripts/share_api.py and docs/TEMPORARY_API.md. Launcher checks the tool,
refuses an occupied port, prompts invisibly for a missing OpenRouter key, passes
it only to the model child, waits for readiness, then starts a temporary HTTP/2
Cloudflare tunnel with localhost Host rewriting. Unique ignored runtime session
directories hold logs and connection.json containing only the fresh trial access
key/URL, never the OpenRouter key. Ctrl+C terminates owned children; no service,
firewall or environment installation. Connection file is private local plaintext.
No provider authentication/credits are inferred from key syntax or model health.

Verified Python executable C:/Users/jadgh/.conda/envs/ml-homework/python.exe.
AST syntax checks passed for API, both launchers and API tests. Initial sandbox
scripts/test_web.py hung without output and was interrupted. Approved outside-
sandbox rerun passed all 18 tests (8.767s), including new auth/no-model-on-denial,
route isolation, missing key and submission-limit checks. These use synthetic
predictor/provider fixtures. `node tests/verify_web_ui.cjs` passed existing UI
contract checks; `python -B scripts/share_api.py --help` passed. No real model,
Jev call, paid request or external prediction executed during preparation.

Official cloudflared portable Windows AMD64 download initially failed sandbox
DNS; authorized network retry downloads into .runtime/tunnel/cloudflared.exe.
Tool completion/version verification and actual live tunnel trial are tracked
below. User was asked to run share_api.py in their own PowerShell to supply the
missing provider key privately, and return only URL/error. External reachability,
prediction, timeout and shutdown verification remain pending. No checkpoint,
dataset, training or historical report changes. Folder still has no local .git;
parent gitlink was not repaired.

Download completed successfully. `cloudflared.exe --version` reports 2026.10.7
(built 2026-10-30T09:43 UTC); local SHA-256 is
2493dbc168923bb3e59e5e7716f71deced92992eea9acd6e9d74f84ac7751343.
This is a recorded local hash, not independent publisher-signature verification.
Final launcher AST syntax check passed after tool-version validation was added.
No public URL has been created yet; waiting for private user-terminal startup.

## Dataset source review - 2026-11-03

User requested verifying datasets in the first group of the supplied Downloads
HTML catalog for possible model improvement. Reviewed all 13 Tier A entries
(12 families at most because DDR appears twice), plus BRSET from Tier B.
Created docs/DATASET_REVIEW_20261103_AR.md with source links, per-source decisions,
access/license caveats, label-mapping requirements and a proposed evaluation-first
workflow. This is documentation/research only; no training phase authorized.

Read current progress/plan and relevant inference/label source and run-directory
names. Browsed original repositories, PhysioNet, Zenodo, ADCIS and RETFound Nature
paper. Corrected BRSET eligibility (DR_ICDR 0..4), DDR dataset-specific NC license
versus repository MIT badge, duplicate DDR counting, and EyePACS pretraining exposure.
Recommended DDR first, BRSET subject to credentialed access, then regular DeepDRiD;
retain existing external test evidence outside future training. Flagged FDR26 and
SRahimDR provenance/mapping uncertainties. Kaggle pages had no readable text; IDRiD
direct fetch returned 403, with official indexed page supplying limited evidence.

No image archives downloaded or audited, no package/environment changes, model
inference, checkpoint changes or tests executed. No improvement, patient independence,
near-duplicate clearance or Syrian clinical performance is established. Counts are
source/catalog counts, not freshly verified eligible-image counts. No architecture
or implementation-plan change; all training/development steps remain proposals.

## Project cleanup and organization - 2026-11-03

User authorized determining unnecessary content and arranging the project.
Read current progress/plan, earlier cleanup inventory, launchers, editor settings,
environment configuration, runtime selection and source references. Confirmed
`C:/Users/jadgh/.conda/envs/ml-homework/python.exe` using its own sys.executable.
Created a fresh recursive inventory and rejected reparse points before mutation.

Removed the incompatible copied macOS `.venv` (24,988 files), root `.DS_Store`,
four generated root bytecode files and their empty directory, generated runtime
QA contact sheet, and accidental empty `docs/API.md#jev-retinal-fundus-gate`.
Total logical bytes removed: 782,951,436 (746.68 MiB); physical recovery unmeasured.
Moved `frontend.zip` to `archive/snapshots/` and `RETFound-output.md/.txt` to
`archive/source-exports/`; SHA-256 before/after each move matched. Historical
snapshots contain differing sources and were preserved rather than discarded.

Added docs/FOLDER_GUIDE.md, archive/README.md and docs/cleanup-20261103 evidence:
fresh inventory, per-file decisions, action log, archive checks and retained-file
verification. Linked the guide from README, added macOS metadata ignore patterns,
and recorded this housekeeping scope in the implementation plan.

PowerShell existence/size/UTC-mtime verification matched all 6,194 retained files
outside explicitly changed/deleted/moved paths. This is metadata parity, not
cryptographic source/model parity. All three archive destination hashes matched,
and the original paths and macOS environment are absent. No application tests,
model inference, paid provider requests, downloads or package changes were run.

Preserved baseline source/launchers/notebooks, model/data trees and historical
results/reports. `.runtime/web` and working Conda remain; `.venv-win` is retained
because external use is unverified. Alternate validation modules still require
coordinated review before removal. Protected partial-download/macOS metadata in
weights/checkpoints was not touched. No local .git exists; parent gitlink history
was not repaired. Earlier inventories/exports describe their original dated paths.

## Sensitivity and specificity display - 2026-11-03

User requested calculating and showing sensitivity and specificity to explain
their difference. The shared evaluation metrics function already calculates
both using any-DR = argmax grade > 0. Added two main evaluation cards plus
formulas, TP/FN/TN/FP counts, reference-class definitions and RETFound-only scope
in frontend/app.js and index.html. The existing /api/evaluation contract supplies
the saved metrics unchanged; no metric calculations were duplicated in JavaScript.
Undefined denominators display N/A with the backend reason.

Added section 9 to examples/RETFound_Jev_15_Image_Test_Pipeline.ipynb. It reads
the saved 1,000-image predictions and calls the existing shared metrics function,
showing accuracy, sensitivity, specificity and counts independently of the small
live demo session. No new model/provider requests or saved run changes. Values:
TP 470, FN 5, TN 513, FP 12; sensitivity 98.95%, specificity 97.71%.
This measures DR detection, not Jev fundus screening or combined-pipeline accuracy.

Verification: six tests in tests.test_metrics_reports passed in ml-homework,
including new asymmetric grade-vs-binary interpretation and absent-class behavior
checks; existing legacy metric parity and report export checks also passed.
The initial sandbox run passed metric cases but report export failed with WinError
5 on os.link for temporary fixture output. Approved rerun outside sandbox passed
all six. Node verify_web_ui.cjs and syntax check passed, including both displayed
percentages, formula counts and null-to-N/A behavior. Notebook nbformat validation
and direct execution of its new metrics cell passed against saved records.
Browser visual rendering and a full Jupyter-kernel execution were not performed.
No training, checkpoint, source data or historical report modifications.


## Cleanup inspection only - 2026-10-31

User requested identifying unnecessary files before deletion. Completed a static
inventory of 31,111 files, with no skipped entries/reparse points or scan errors.
Created docs/cleanup-review-20261031/{CLEANUP_REVIEW.md,file-review.csv,
inventory.json,summary.json,archive-review.json,small-file-duplicates.json}.
Every scanned file has a category and reason; input inventory excludes the new
review artifacts themselves and subsequent progress edits. No files deleted,
moved, installed or downloaded; no model inference or environment changes.

Seven low-risk generated/empty-file candidates total 106,873 bytes. Large
conditional candidates: copied macOS .venv (746.58 MiB), separate Windows
.venv-win (104.55 MiB), historical frontend.zip snapshot (576.30 MiB).
Current launchers use Conda; external use of these environments is unverified.
ZIP member inspection and size/CRC comparisons found old differing source/report
versions; it is not a verified redundant archive. No extraction was performed.
Small-file SHA-256 comparisons also identified referenced duplicate sample paths;
these remain preserved. Duplicate checks were scoped, not a full dataset audit.

Confirmed .runtime/web supplies active server dependencies. A 603,807,740-byte
partial download and macOS metadata exist inside protected weights/checkpoint
trees; flagged for separate review, not included in routine cleanup. Alternative
jev_gate.py and older human-review policy files need coordinated reference/test
review before removal. Source datasets, checkpoints, weights, historical results,
legacy scripts/notebooks and reports remain protected. Running/open-file use and
backup adequacy are not established. Await a concrete cleanup scope before any
deletion; revalidate paths/file changes then. No plan architecture change needed.


## Explained Jupyter testing notebook - 2026-10-30

Added examples/RETFound_Jev_15_Image_Test_Pipeline.ipynb at the user's request.
The 18-cell notebook explains the existing server pipeline, binary Jev decisions,
error blocking, unchanged RETFound preprocessing, five DR grades, reference-label
sources and demonstration limitations. It displays an HTML pipeline and three
local image galleries covering all 15 hash-verified images. Startup commands and
kernel guidance use the existing ml-homework environment. No packages installed.

Single-image and sequential batch testing use the existing fixed-sample API;
both switches default off. Readiness/catalog checks use GET only. The backend
continues to compute predictions and grade agreement. Repeated session requests
are skipped, errors stop batches, and uncertain/interrupted outcomes block further
requests. Optional export creates unique new results/notebook_demo JSON files
only after requests, preserving complete server responses and untested states.
No key is stored in the notebook; no model is loaded by the notebook.

Verified with the existing ml-homework Python: nbformat schema validation and
execution of every default code cell with HTTP transport mocked offline. All
15 local files decoded and matched hashes; three HTML image galleries generated;
only a GET readiness attempt occurred, no POST or results file. Synthetic checks
passed for accepted, repeat-skipped, rejected, provider-error, interrupted and
retry-blocked states. Initial verification harness assertions were corrected for
plain-Python display capture and mock namespace restoration; final checks passed.
This was direct code-cell execution, not a Jupyter kernel/browser rendering test.
No live Jev/RETFound inference, downloads, checkpoint changes or historical output
changes occurred. The notebook ships with empty execution outputs.


## Local server dataset test feature - 2026-10-30

User requested testing the downloaded images on a server and explicitly selected
adding testing to the existing local server. Added /dataset-tests, linked from
the existing navigation. The page lists the 15 images with dataset reference
grades, offers per-image testing and sequential Test all 15, stops after the
current image on request, and stops batches on provider/server failure. Opening
or previewing does not invoke a model. Network-uncertain outcomes stop further
requests without automatic retry. New tests clear stale scores; rejection, error
and untested states remain explicit. Results JSON can be downloaded; no server
history is written and no browser aggregate metrics are calculated.

Added api/demo_samples.py to validate the fixed trusted local manifest and enforce
15 distinct IDs/hashes, dataset/grade/split mapping, root containment, bounded
reads and image hash agreement. Added GET /api/demo, GET /api/demo/{id}/image and
POST /api/demo/{id}/predict. The prediction handler shares the existing capacity,
executor, cancellation behavior, decode validation, Jev gate and real predictor
with uploads. The backend joins the reference label only after inference and
computes matches_true_grade. Caller-supplied labels do not change the comparison.
Unknown/changed files are blocked before model calls. Existing upload response
schema and original image preprocessing are unchanged.

Changed/added paths: retfound_platform/api/{app,demo_samples}.py;
frontend/{dataset-tests.html,dataset-tests.js,dataset-tests.css,index.html};
tests/{test_api.py,test_demo_samples.py,verify_dataset_tests_ui.cjs};
docs/API.md, README.md, this record and implementation plan. Removed stale
local-only/direct-upload wording in existing frontend text to reflect Jev.
No downloads, checkpoint changes or paid inference were executed in this phase.

Verification in ml-homework with existing isolated web dependencies:
34 API/gate/diagnostic tests passed, including new accepted-image comparison,
reference-label override resistance, exact bytes passed to the gate, dataset
asset MIME types, rejection, provider failure, unknown IDs and changed files.
Two additional manifest/path/label/hash tests passed. Node tests for the new
page and existing application passed: no prediction on page load, 15 cards,
per-image endpoint, score rendering, stale-result clearing, batch stop on provider
failure and JSON export distinguishing failed/untested records. These use
synthetic model/provider responses; no real Jev or DR result is claimed.

The initial sandbox API run hung creating Windows asyncio's local socketpair;
a faulthandler trace identified socket.accept in _fallback_socketpair before test
execution. It was interrupted; the approved run outside the sandbox passed in
2.53 seconds. This diagnosis applies to the observed test attempt, not to all
historical stalls. Browser visual rendering and fresh authenticated end-to-end
inference remain unverified. No running credential-bearing server was stopped;
restart using diagnose_jev.py --new-key --start-server and visit /dataset-tests.


## Fifteen labeled Hugging Face upload examples - 2026-10-30

The user explicitly requested downloading five images each from
amin-nejad/idrid-disease-grading, OctoMed/Messidor2 and ctmedtech/DDR-dataset,
with reference labels and a folder for manual upload. Added
scripts/prepare_upload_demo.py and tests/test_upload_demo.py. The script is
import-safe and downloads only on explicit CLI execution; existing outputs are
not overwritten. No packages, model/checkpoint, inference API or frontend changed.

Completed new output: upload_test_images/huggingface15-20261030/.
Its images/IDRID, images/MESSIDOR2 and images/DDR folders each contain exactly
five image files, one per DR grade 0..4. The set is a balanced demonstration,
selected deterministically (first test row per grade among the first 100 viewer
rows for IDRiD/Messidor2, first sorted labeled test filename per grade for DDR).
It is not a random or representative evaluation sample.

Verified IDRiD ClassLabel names against source features; Messidor2 uses the
explicit answer mapping A..E, never its generated responses. DDR images are
joined to DR_grading/test.txt at a pinned repository revision; extra grade 5
rows, if present, are not mapped into the five-grade classifier. IDRiD and
Messidor2 images are Hugging Face viewer-exported assets with cached revision
and row identity preserved; byte equivalence to embedded originals is unverified.
DDR uses original repository bytes at a pinned revision. No local resize or
re-encoding was applied to the upload files. Metadata, label-source snapshots,
source identities, SHA-256 hashes and dimensions are outside the image folders.

Deliverables: manifest.json; comparison.csv with blank predicted grade,
agreement and Jev-decision columns; labels.html preview; README.md;
source_metadata/; completed.json and verification.json. Filename true0 denotes
reference grade 0, not a predicted grade. Three synthetic selection tests passed
via ml-homework `python -B -m unittest tests.test_upload_demo`.

The initial sandbox metadata access failed on DNS. Approved network commands
verified source labels and downloaded the authorized 15 images using
`python -B scripts/prepare_upload_demo.py` (exit 0). Reopened/decoded every saved
image, recomputed hashes and dimensions against the manifest, verified 15 distinct
hashes and one example per grade/dataset, and confirmed comparison output fields
are empty. A 15-image contact sheet was visually inspected for preview integrity;
this is not independent clinical review of reference labels. All checks passed.
No Jev calls or RETFound inference were performed. Full split, patient,
near-duplicate and checkpoint-training independence remain unverified. No
historical datasets/results were overwritten.


## Consolidated project report and user confirmation of Jev success - 2026-10-30

The project owner stated that Jev now works successfully, then requested a report
covering all work, Jev and the 1,000-image evaluation. This is user-reported live
success; no authenticated trace, latency measurement or root-cause proof was
provided. Earlier records of unverified live operation are historical. No Jev
accuracy or 1,000-image combined-pipeline evaluation is established.

Created docs/reports/retfound-jev-20261030/RETFound_Jev_Technical_Report.html and
an editable Markdown copy, plus report_verification.json. Added the import-safe
scripts/build_project_report.py, which creates a new output directory and refuses
to overwrite it. The 12-section English technical report covers the original
baseline, modular implementation, audit/sampling, inference contract, the saved
1,000-image results and per-class/confusion analysis, historical transfer results,
API/UI, Jev gate and troubleshooting, verification boundaries, startup, limitations
and artifact provenance. The saved evaluation predates Jev and is labeled RETFound
only. Proposed combined validation is explicitly future work.

Executed with the existing ml-homework interpreter:
`python -B scripts/build_project_report.py`.
Read all 1,000 saved records; independently recomputed confusion, accuracy, macro
F1, quadratic kappa and binary counts; checked score finiteness/normalization,
argmax, distinct hashes and selection hash ordering. All nine checks passed.
No fresh inference, dataset download, training or paid API request was made.
Historical run files were read only. Structural HTML checks passed for all 12
sections, UTF-8 and absence of executable/external asset elements. The standalone
report is printable from a browser. Visual browser/print rendering is unverified.

The workspace dependency loader reported no configured bundled document runtime;
Word/PDF authoring and render tools were not available. Delivered HTML and Markdown
instead of claiming a rendered DOCX/PDF. No packages or environment configuration
were changed. The implementation plan needs no architecture/scope change for this
documentation-only deliverable.


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
`python -B scripts/test_web.py`. Full discovery passed all 46 Python tests using the same interpreter and
isolated web dependencies; `node tests/verify_web_ui.cjs` passed. Browser visual
rendering was not tested. HTTP provider responses in unit tests are mocked,
not real predictions. No authenticated Jev call or fundus accuracy evaluation was
performed. The previously running service has not been restarted; it retains the
old behavior until the user stops it and launches with OPENROUTER_API_KEY as
documented in docs/API.md. No key was requested through chat or written to disk.


## Direct image inference restored at user request - 2026-10-30

The user clarified that they do not want the approval/reference workflow now and
want their photo sent directly into the model. This supersedes the restriction
documented below. `api/app.py` no longer loads or consults the retinal registry or
review files. After format, decoding and resource checks, every supported upload
calls the existing real predictor. Raw and multipart requests share this behavior.
Weights and preprocessing are unchanged. The retained review utility/registry and
their tests are inactive in the API; they do not control uploads.

Updated `api/schemas.py` to report `input_validation.status: decoded` and
`model.input_policy: retfound-direct-input-v1`. Decoding is not modality review.
Updated `frontend/{app.js,index.html,input-validation.css}` to remove review-required
UI and render direct predictions, with an explicit explanation that non-retinal
photos can also receive meaningless DR outputs. Updated README, API instructions,
Postman collection, and implementation plan to remove the approval requirement.

Verification in the existing ml-homework interpreter with isolated web dependencies:

```powershell
& $retfoundPython -B -c "import sys; sys.path.insert(0, 'scripts'); from web_runtime import configure; configure(); import unittest; result=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.discover('tests')); sys.exit(not result.wasSuccessful())"
node tests/verify_web_ui.cjs
& $retfoundPython -B scripts/verify_web.py --output results/runs/direct-input-20261030/verification.json
```

All **42 Python tests passed**. The previous three active-gate API tests were
replaced with a direct-inference regression proving unregistered raw/multipart
uploads call the predictor without registry lookup. Corrupt images still bypass
inference and return errors. UI contract checks passed, including result rendering,
download, and clearing stale results after errors. Postman JSON and test scripts
were syntax checked; Postman UI and browser visual rendering were not exercised.

Restarted only verified RETFound PID 32472; replacement PID **20468** remains running
at http://127.0.0.1:8000. Logs:
`.runtime/web-server-6f3fbb17351349338529759e463b1b73.{out,err}.log`.
The fresh real-CUDA HTTP verification above passed: baseline maximum score delta
**0.0**, raw/multipart parity, three concurrent successes, corrupt-image rejection,
and correct asset MIME types. A newly encoded PNG of the fundus sample (new SHA-256
`eae21551d35b29c649c0064f9d82caea70e1fb3c5669870aff5d8bae4fe0d695`)
received a real prediction without any registration/review. This was a new test
input, not the user's unavailable `test.jpeg` or a change to model preprocessing.
No previous results were overwritten; no evaluation rerun or training occurred.

## Unverified-image prediction repair - 2026-10-30

The user uploaded a house/window photograph and received grade 2. The five-class
DR model has no non-retinal class, and the prior API decoded arbitrary images then
passed them directly to the classifier. No validated retina/non-retina detector
was found. The user explicitly selected **block unverified images**.

Implemented the selected restriction in `inference/input_validation.py`: before
DR inference, require an exact trusted-reference SHA-256 or a trusted local human
modality review. Unknown inputs receive HTTP 422, `unverified_retinal_input`,
`prediction: null`, and no disease grade or scores. A new genuine retinal image is
also unknown until reviewed. This is provenance admission, not automatic retina
recognition, clinical validation or image-quality assessment.

Changed/added paths:

- `retfound_platform/inference/{input_validation.py,retinal_references.json}`:
  versioned policy and 1,106 distinct reference hashes. The registry combines the
  1,036 eligible APTOS test hashes from the existing audit, the 100 benchmark
  references (deduplicated), and the visually inspected local fundus sample.
  The current ZIP hash was checked against the audit; benchmark image bytes were
  checked against their saved hashes. Dataset provenance supports the dataset
  entries; this was not a visual review of every dataset image. No ground-truth
  grades are used in admission or live inference.
- `scripts/review_retinal_image.py`: records a trusted person's completed visual
  modality review with reviewer, note, UTC time and exact hash. No remote approval
  endpoint or client-header override exists. Records apply immediately and are
  revocable locally; edited/re-encoded files need a new review.
- `retfound_platform/api/{app,schemas}.py`: shared gate before predictor invocation,
  accepted-input metadata, explicit rejection contract, model policy metadata.
- `frontend/{index.html,app.js,input-validation.css}`: review-required result state,
  clear all earlier scores/grades on rejection, accepted-input basis, API guidance.
- `tests/{test_api.py,test_input_validation.py,verify_web_ui.cjs}` and
  `scripts/verify_web.py`: reference/review/rejection tests and live regression.
- `docs/API.md`, `docs/RETFound.postman_collection.json`, `README.md`, and
  `docs/IMPLEMENTATION_PLAN.md`: accepted/rejected workflows and review limitations.

Verification executed with
`C:\Users\jadgh\.conda\envs\ml-homework\python.exe` and isolated `.runtime/web`
API dependencies (no package or environment changes):

```powershell
& $retfoundPython -B -c "import sys; sys.path.insert(0, 'scripts'); from web_runtime import configure; configure(); import unittest; result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('tests')); sys.exit(not result.wasSuccessful())"
node tests/verify_web_ui.cjs
& $retfoundPython -B scripts/verify_web.py --output results/runs/input-gate-20261030/verification.json
```

All **44 Python tests passed**. They include zero predictor invocations for unknown
inputs, misleading filenames and client verification claims; invalid policy records
fail closed; exact human review and revocation; existing preprocessing parity and
dataset/metric/launcher regressions. Frontend contract checks passed, including
rejection after an earlier successful prediction clearing scores and preventing
old JSON download. Postman collection JSON and response-script syntax checked;
Postman itself was not operated. Visual browser rendering remains unverified.

Restarted only the identity-checked `serve_web.py` process on port 8000. Replacement
PID **32472**, still running locally for the user. Logs:
`.runtime/web-server-b29663f633724d1a823d8f9ae0243734.{out,err}.log`.
The fresh HTTP verification above passed against the real CUDA service:
known sample accepted, **maximum score difference 0.0** from the verified baseline,
raw/multipart parity, three concurrent predictions, corrupt-input rejection, and
all asset MIME types correct. A synthetic window illustration uploaded as
`retina.jpg` received 422 with no grade/scores. This was a test fixture, not the
user's original photo. That photo was not retained; its reported SHA-256
`291671d62e36123d6894df9f6ed1f3f0fcc395b69f04204eb585c48ebecb8399`
is absent from the reference registry. No live human-review records were created.

No weights, preprocessing, legacy scripts, datasets or prior reports changed. The
1,000-image evaluation was not rerun. Automatic modality detection remains future
work requiring a separately validated detector and suitable evaluation data.

## Repeated web launch fix — 2026-10-30

The user encountered Windows error 10048 after running `run_web.bat`. Port inspection
confirmed that the previously started RETFound process (PID 16756) was still serving
healthy CUDA inference on 127.0.0.1:8000. The new invocation unnecessarily loaded a
second model before Uvicorn tried to bind the same port.

Updated `scripts/serve_web.py` to reserve its loopback socket before importing the
API/loading weights and pass that socket to Uvicorn. If binding fails and the port
serves a ready RETFound health/model response, it reuses that service and opens its
page when requested. Unknown port owners are left untouched, with an actionable
message. Existing server configuration is explicitly retained on reuse.

`tests/test_web_launcher.py` covers exclusive reservation, reuse before model/API
import, unknown owners and actual Uvicorn HTTP serving on the reserved socket.
The live `scripts/serve_web.py` command now exits successfully with
“RETFound is already running … no second model was loaded.” The existing service
was not stopped or replaced. Documentation updated in `docs/API.md`.

## Web responsiveness fix and Postman — 2026-10-30

The user reported that the web page did not respond and requested Postman testing.
Live inspection found `/api/health` ready on port 8000 and the CUDA model loaded.
However, `/app.js` returned `Content-Type: text/plain; charset=utf-8`. Windows MIME
mapping caused `StaticFiles` to serve a module script with the wrong type, preventing
browser JavaScript execution. Earlier HTTP-200 and DOM-stub checks missed this.

Fixed `retfound_platform/api/app.py` with explicit FileResponse routes for JavaScript,
CSS and SVG MIME types before the general static mount. Added a regression test
that simulates `mimetypes.guess_type` returning text/plain; all **12 API tests passed**.
`scripts/verify_web.py` now checks live content types as well as asset status codes.
Created `docs/RETFound.postman_collection.json` with health, model and multipart image
requests, response assertions and a configurable local base URL; documented its use
in `docs/API.md`. No model or preprocessing changes were made.

Restarted only the verified Python `serve_web.py` process owning port 8000 and left
the replacement running for the user's web/Postman tests. Replacement PID: 16756;
logs: `.runtime/web-server-35585fa5c9a640da8ce093cce5c81906.{out,err}.log`.
No other Python process was stopped. The service remains bound to 127.0.0.1:8000.
Live verification passed and is recorded in the new
`results/runs/web-mime-fix-20261030/verification.json`: JavaScript now returns
`text/javascript; charset=utf-8`; all assets have correct content types; raw and
multipart real CUDA predictions match the baseline exactly; three concurrent
predictions succeeded. The sample returned grade 0 with top score 0.7967534661.
Postman collection JSON and its response-script syntax validated (three requests).
The requests were verified by HTTP client, not executed inside the Postman UI.

## Local web application and image API — completed

Authorized scope: the user requested a web application that receives an image
through an API and returns a nicely presented prediction. They clarified that the
calling client is **another application on this computer**. This section supersedes
the API-deferred status in the earlier evaluation record below.

Delivered:

- `retfound_platform/api/{__init__,app,schemas,uploads}.py`: import-safe FastAPI
  factory, one real model loaded in lifespan, one inference thread, three admitted
  requests, bounded in-memory raw/multipart upload handling, structured errors,
  response schemas, explicit browser origins, loopback Host validation, readiness
  and model metadata. A cancelled client retains its slot until actual work ends.
- `frontend/{index.html,styles.css,app.js,favicon.svg}`: responsive local research
  workspace with drag-and-drop/file selection, preview, real sample selection,
  processing/error/offline states, predicted grade, five score bars, JSON download,
  saved evaluation/confusion matrix, model information and API request examples.
  The frontend displays API results and backend-computed metrics only.
- `scripts/{web_runtime,serve_web,test_web,verify_web}.py`, `run_web.bat` and
  `setup_web.bat`; pinned `requirements-web.txt`; `.runtime/` ignore entry.
- `tests/test_api.py` and `tests/verify_web_ui.cjs`; `docs/API.md`, README and plan
  updates. The earlier evaluation package, original model, scripts, checkpoints,
  notebooks, datasets and historical run outputs were not modified for this phase.

Dependencies were installed with the working Python 3.10.19 interpreter into
`.runtime/web`, not the Conda environment. Tested versions include FastAPI 0.162.0,
Starlette 1.7.0, Pydantic 2.14.2, python-multipart 0.0.32 and the transitive versions
pinned in `requirements-web.txt`; existing uvicorn 0.49.0 remains in `ml-homework`.
This is a web-dependency lock, not a newly reproduced full model environment.
The first download attempt could not access the index in the sandbox. A scoped
approved download succeeded. Installed files inherited restrictive temporary-file
permissions; restoring inherited permissions solely under `.runtime/web` made
them readable. The working model packages were not upgraded or replaced.

Commands and evidence (using `%USERPROFILE%\.conda\envs\ml-homework\python.exe`):

```powershell
& $retfoundPython -B -m pip install --index-url https://pypi.org/simple --only-binary=:all: --no-cache-dir --target .runtime/web -r requirements-web.txt
& $retfoundPython -B scripts/test_web.py
& $retfoundPython -B scripts/serve_web.py --device cuda
& $retfoundPython -B scripts/verify_web.py --output results/runs/web-api-20261029/verification.json
node tests/verify_web_ui.cjs
```

- 11 API tests passed: model lifespan/loading count, raw/multipart contract parity,
  corruption/unsupported content/missing/multiple fields, limits with and without
  Content-Length, bounded concurrency and responsive health, cancellation handling,
  inference failure/error redaction, explicit CORS/Host rules, schema/static files
  and blocked filesystem traversal.
- Full combined suite passed: **30 tests** (API plus 19 existing tests) using the
  isolated dependency path. Model-independent API fixtures are explicitly labeled;
  they are not used by the application. Ordinary core discovery skips API tests
  if optional API dependencies have not been configured.
- The live server at `http://127.0.0.1:8000` strictly loaded the real CUDA model.
  A separate HTTP process uploaded `sample_images/idrid_test.jpg` as multipart and
  raw bytes. Both returned grade 0 and five scores matching the previously verified
  CUDA prediction with **maximum difference 0.0**. One recorded request took
  495.59 ms including admission/upload/queue/inference/response construction;
  this is a single observation, not a throughput guarantee.
- Three simultaneous real HTTP predictions succeeded with identical scores and
  released all slots; a corrupt image returned 422. The page, JavaScript, CSS,
  favicon, OpenAPI schema and saved evaluation endpoints all returned HTTP 200.
  The evidence is `results/runs/web-api-20261029/verification.json` (UTC response
  timestamp `2026-10-29T21:12:52.115039+00:00`).
- Frontend contract tests passed: sample selection, multipart request, five-score
  result, download contents, failure clearing stale output, remove/reset, client
  size rejection, navigation, evaluation data, copied request example and offline
  state. These execute JavaScript with a minimal DOM stub and recorded real-model
  responses, not in an actual browser. JavaScript syntax validation passed.

Verification limits: browser automation returned both “browser access host is
unavailable” and “native pipe is unavailable”; visual desktop/mobile QA, native file
picker and browser download behavior remain unverified. The API tests and real HTTP
requests do not establish those visual behaviors. No hosted Site was registered or
published because this is the requested loopback-only application.

The temporary verification server was stopped after checks. Run `run_web.bat`
to start the app and open the browser after model startup. Stop
it with Ctrl+C in its window. Requests are ephemeral; no uploaded images or request
history are retained. The frontend's JSON download is explicit. API evaluation
jobs, notebook work, React migration, LAN/public hosting/authentication and clinical
deployment remain outside this increment. The Git gitlink limitation is unchanged.

## Evaluation implementation — 2026-10-29 (Asia/Damascus)

User-authorized scope: build the 1,000-image APTOS evaluation workflow from
`APTOS2019.zip`; **evaluation first, API later**. This section supersedes the
earlier inspection-only status below. No API, React application, notebook,
training, checkpoint modification, installation or dataset download was performed.

Implemented additively:

- `retfound_platform/config.py`, `contracts.py`, package initializers and
  `datasets/{labels,sources,validation,manifests,sampling}.py`: safe local ZIP/folder
  readers, bounded decoding, explicit grades/splits, SHA-256 evidence, conflicting
  labels/overlap/duplicate exclusions, versioned atomic manifests and seeded sampling.
- `inference/{preprocessing,loader,predictor}.py`: shared float32 inference,
  strict trusted-local checkpoint loading and configuration validation, explicit
  auto/CUDA/CPU/MPS selection, serialized access, no model creation on import.
- `evaluation/{metrics,runner,reports}.py`: finite metrics with undefined reasons,
  fresh audit before inference, immutable selection/new run directories, image-hash
  rechecks, provenance, offline APTOS viewer and five-score CSV/JSON exports.
- `scripts/{validate_dataset,sample_dataset,evaluate_aptos,verify_inference}.py`,
  `run_aptos_evaluation.bat`, Python tests and a pure-JavaScript report contract check.
- Updated README and implementation plan. Legacy Python scripts, model definitions,
  launchers, notebooks and historical reports were not edited by this implementation.

Fresh data evidence (`results/runs/aptos-audit-20261029/audit.json`):

- The ZIP is now present: 288,557,206 bytes; SHA-256
  `fd04f48ee1889f64e5c7f4edad4a16b4468fed2d709a21e1107ddc1ff6eb1dff`.
- Decoded 2,048 train, 514 validation, 1,100 test images; zero read/structure issues.
- 1,036 eligible test images. Sixty-four test paths excluded; overlapping reasons
  include 56 cross-split matches, 12 conflicting-label records and 4 redundant
  same-label test copies. Reason counters must not be summed to infer exclusions.
- Exact-byte comparisons cover all three supplied splits. Patient, near-duplicate
  and checkpoint-training-split independence remain unverified. The old 981-image
  audit is historical and cannot explain the current archive's different behavior.

Commands executed using `C:\Users\jadgh\.conda\envs\ml-homework\python.exe`
(Python 3.10.19; installed packages preserved):

```powershell
$retfoundPython = Join-Path $env:USERPROFILE '.conda\envs\ml-homework\python.exe'
& $retfoundPython -B scripts/validate_dataset.py APTOS2019.zip --output results/runs/aptos-audit-20261029/audit.json
& $retfoundPython -B predict_aptos.py sample_images/idrid_test.jpg
& $retfoundPython -B -m unittest discover -s tests -v
& $retfoundPython -B scripts/verify_inference.py --output results/runs/aptos-audit-20261029/inference-verification.json
& $retfoundPython -B scripts/evaluate_aptos.py APTOS2019.zip --count 1000 --device cuda --output results/runs/aptos1000-20261029
```

Verification already completed:

- 19 unittest checks passed. Synthetic cases cover aliases, invalid labels/splits,
  decoding/CRC failure, paths, duplicate ZIP members, symlinks, byte/pixel limits,
  overlap/conflicting labels, stable selection, no replacement, insufficient samples,
  preprocessing tensor parity, checkpoint configuration, invalid logits, undefined
  metrics, saved metric parity and export consistency/escaping.
- The initial tests failed on Python temporary-directory permissions (including
  mode-0700 workspace temp directories) under this Windows sandbox. Fixtures now
  use unique workspace directories with normal inherited permissions. A path-audit
  test also caught traversal being classified as hidden; safe-path validation was
  moved before hidden-entry exclusion, then the full suite passed.
- After atomic CSV/HTML publication was added, the five relevant persistence and
  report/metric tests passed again.
- The unchanged baseline CLI ran successfully on CUDA, predicting grade 0 for
  `sample_images/idrid_test.jpg`. Shared inference matches its printed scores.
- All 34 historical APTOS images were freshly inferred with **zero maximum score
  difference** from saved predictions. CPU versus CUDA on one image had maximum
  score difference `1.7881393432617188e-07` and the same predicted grade. MPS untested.
- Checkpoint hash remains
  `a96b9dbcb78eff373912fb0a48d316dc35ffb0715bb2a1b9128b096d780edbbf`.

The fresh 1,000-image CUDA run completed with exit code 0. Artifacts are in
`results/runs/aptos1000-20261029/`; `index.html` is the offline viewer.
The run recorded 84.98 seconds from audit start through prediction/metric creation
(excluding Python startup and final artifact serialization). This is one measured
run on this laptop, not a general throughput claim.

| Metric | Fresh result |
| --- | --- |
| Exact grade agreement | 847/1,000 (84.70%) |
| Five-label macro F1 | 0.666041 |
| Quadratic weighted kappa | 0.913479 |
| Any-DR accuracy (argmax > 0) | 98.30% |
| Any-DR sensitivity / specificity | 98.9474% / 97.7143% |
| False negatives / false positives | 5 / 12 |
| True grade counts 0..4 | 525 / 86 / 261 / 54 / 74 |

Post-run checks: recomputed the seeded selection and metrics; verified 1,000 distinct
image hashes, identical record ordering across selection/JSON/HTML, finite five-score
vectors summing to one, argmax grades, all five CSV scores and true/predicted labels;
decoded all 1,000 embedded thumbnails. All checks passed. `node tests/verify_report.cjs
results/runs/aptos1000-20261029/index.html` passed report initialization, correct/incorrect
and false-positive/negative filters, grade filtering, empty search, image detail with
five scores, dialog closure and a 1,000-row CSV export using a minimal document stub.
This tests JavaScript behavior, not browser rendering. All 27 new Python files parsed.

Remaining scope/limitations: API and image-upload workflow deferred by the user.
Only uniform test sampling and labeled split/grade folder or ZIP input are supported.
The browser-access host and native UI pipe were unavailable, so interactive visual
browser QA could not run. The offline report is an adapter of the established viewer;
its contract checks are distinct from actual browser rendering. Dependency locking,
legacy CLI refactors, IDRiD fixes, notebook, API/jobs and React remain future work.
The parent Git gitlink/no-local-`.git` limitation remains; no Git repair was attempted.

## Historical phase 1 inspection

Last inspected: 2026-10-29, Asia/Damascus.

Status: **Phase 1 complete; stop after inspection and documentation.** No API/frontend implementation, training, checkpoint modification, package installation, dataset download or full benchmark rerun was performed.

## Completed in this phase

- Inventoried the application source tree, data/manifests, checkpoints, environments, notebooks, report assets and parent Git state. Read README, benchmark source references, launchers, relevant Python modules and notebook sources. Inventoried PDFs without rendering them; dependencies/caches were not reviewed line-by-line.
- Traced strict model loading, exact preprocessing, prediction, dataset sampling and evaluation/report generation.
- Identified reusable components and documented known gaps and the staged architecture in `IMPLEMENTATION_PLAN.md`.
- Created `AGENTS.md`, `docs/IMPLEMENTATION_PLAN.md`, and this progress file. These are the only intended source/document changes for this phase.
- Verified the current Conda interpreter, installed package versions and CUDA availability without changing the environment.
- Ran the existing single-image prediction CLI successfully on CUDA. It loaded all weights strictly and returned finite logits of shape `(1, 5)`.
- Parsed all 13 application Python files in the root and `util/` with `ast.parse`; all parsed successfully. This is a syntax check, not an automated behavioral test suite.
- Decoded all 100 local benchmark images and recomputed their SHA-256 hashes; all matched the saved JSON. Checked finite five-score vectors, score sums and argmax grades.
- Reproduced the saved 34/33/33 seeded selections from each cached archive entry listing using the existing selection algorithm. This verifies local selection reproducibility, not current remote archive contents.
- Recomputed the fine-tuned checkpoint SHA-256; it matches the saved benchmark provenance.
- Parsed the generated HTML's embedded JSON: its 100 records and metrics match `predictions.json` after excluding embedded thumbnails. Browser rendering, filters and downloads were not interactively tested.
- Compared SHA-256 snapshots of 25 pre-existing source/document/report-template files. Twenty-two were unchanged; `evaluate_idrid.py`, `RETFound-output.md`, and `RETFound-output.txt` changed outside this session's writes during inspection. The IDRiD file's initial module docstring was absent on reread; the checkpoint/device findings remained unchanged. The two exports were regenerated with a 2026-10-29 timestamp. These concurrent changes were left intact; a blanket claim that every original file is byte-identical would be incorrect. This session wrote only the three requested documentation files.

## Current workspace map

All relative paths below are relative to `C:\Users\jadgh\Desktop\Dr 4\Dr\RETFound`.

| Path | State / purpose |
| --- | --- |
| `README.md`, `BENCHMARK.md`, `LICENSE` | Existing instructions, source links and license text. README mixes current Windows prediction instructions with upstream training instructions. |
| `predict_aptos.py`, `models_vit.py` | Verified classifier CLI and architecture. |
| `prepare_benchmark.py`, `evaluate_benchmark.py` | Existing 100-image preparation/inference/report workflow. |
| `evaluate_idrid.py` | Legacy streaming evaluation; not currently runnable unchanged in the inspected environment. |
| `main_finetune.py`, `engine_finetune.py`, `train.sh`, `util/` | Upstream training/evaluation code; preserve, do not train. |
| `run_prediction.bat`, `run_benchmark.bat` | Windows launchers selecting `ml-homework`. |
| `checkpoints/checkpoints/APTOS2019/checkpoint-best.pth` | Actual classifier checkpoint, 3,639,988,647 bytes. |
| `weights/weights/RETFound_mae_natureCFP/RETFound_mae_natureCFP.pth` | Separate pretraining weights, 3,952,489,221 bytes; not used in the verified prediction command. |
| `benchmark_data/APTOS2019/` | 34 images plus `manifest.json` and `archive_entries.json`. |
| `benchmark_data/IDRID/` | 33 images plus corresponding manifest/entry listing. |
| `benchmark_data/MESSIDOR2/` | 33 images plus corresponding manifest/entry listing. |
| `sample_images/` | `idrid_test.jpg`, `test.jpeg`, `test1.jpeg`. |
| `benchmark_report.html` | Source template with `__REPORT_DATA__` placeholder. |
| `results/benchmark100/` | Existing `predictions.json`, `predictions.csv`, `index.html`. |
| `results/idrid/` | Existing summary, CSV, confusion matrix and six gallery PNGs. |
| `aptos_zip_audit/` | Existing `audit_summary.json`, `audit_issues.json`, `test_manifest.csv`. The 981-row CSV is an eligible subset manifest, not a complete per-file audit. |
| `latent_feature.ipynb`, `examples/RETFound_MESSIDOR2_demo.ipynb` | Existing feature/training examples; not the planned platform notebook. |
| `work_report.html`, `report.pdf`, `Report_Arabic.pdf` | Historical presentation artifacts. HTML inspected as source, PDFs inventoried only. |
| `RETFound-output.md`, `RETFound-output.txt` | Generated source exports, initially dated 2026-10-23 and regenerated externally during this inspection with a 2026-10-29 timestamp; inspect actual source files instead. |
| `.venv/`, `.venv-win/`, `.vscode/`, `__pycache__/` | Copied macOS environment, separate Windows 3.13 environment, editor settings and generated cache. |

`APTOS2019.zip` and `audit_aptos_1000 (1).py` are **absent from the current project**. Do not reuse earlier chat commands as if those inputs still existed. No `retfound_platform/`, `scripts/`, `tests/`, `notebooks/` or `frontend/` platform scaffold was created in this phase.

## Verified runtime

Interpreter: `C:\Users\jadgh\.conda\envs\ml-homework\python.exe`, Python 3.10.19.

| Component | Observed version/state |
| --- | --- |
| PyTorch / torchvision | `2.5.1+cu121` / `0.20.1+cu121` |
| timm | `0.9.16` |
| CUDA | Available; PyTorch CUDA build 12.1 |
| GPU | NVIDIA GeForce RTX 3070 Laptop GPU |
| Pillow / NumPy | `12.0.0` / `2.2.6` |
| scikit-learn / matplotlib | `1.7.2` / `3.10.7` |
| requests / gdown | `2.32.5` / `6.4.2` |
| ipykernel / nbformat | `7.3.0` / `5.11.1` |
| uvicorn | `0.49.0` installed; this does not establish an API exists |
| datasets / fastapi / pytest | Not installed in `ml-homework` |

These are observed versions, not a newly generated dependency lock or recommended upgrade set. `requirements.txt` requests different Pillow/NumPy/scikit-learn versions and omits some workflow dependencies. No installation was attempted.

## Commands and actual verification evidence

Run from the project folder. A direct interpreter path avoids relying on Conda initialization:

```powershell
$retfoundPython = Join-Path $env:USERPROFILE '.conda\envs\ml-homework\python.exe'
& $retfoundPython -B predict_aptos.py sample_images/idrid_test.jpg
```

Executed in this phase, exit code 0: device `cuda`; all model weights loaded successfully; output shape `(1, 5)`; predicted grade 0. Printed scores were approximately `[79.68, 9.80, 6.66, 1.79, 2.08]` percent. This verifies execution, not ground-truth accuracy for the sample. The displayed percentages are rounded and uncalibrated. CPU and MPS inference were not exercised in this phase.

Equivalent existing launcher (not separately rerun):

```powershell
.\run_prediction.bat
```

If Conda is not recognized in PowerShell, the previously verified session hook is:

```powershell
(& 'C:\ProgramData\anaconda3\Scripts\conda.exe' 'shell.powershell' 'hook') | Out-String | Invoke-Expression
conda activate ml-homework
```

Useful inspection commands:

```powershell
& $retfoundPython -B -c "import sys,torch; print(sys.executable); print(torch.__version__); print(torch.cuda.is_available())"
Get-FileHash -Algorithm SHA256 '.\checkpoints\checkpoints\APTOS2019\checkpoint-best.pth'
```

Computed classifier SHA-256: `a96b9dbcb78eff373912fb0a48d316dc35ffb0715bb2a1b9128b096d780edbbf`.

Existing benchmark commands below are documented for later use, **not executed in this phase**. They may access the network and overwrite fixed historical outputs:

```powershell
& $retfoundPython prepare_benchmark.py
& $retfoundPython evaluate_benchmark.py
# Equivalent sequence:
.\run_benchmark.bat
```

Existing IDRiD entry point: `python evaluate_idrid.py --all`; blocked in this environment by missing `datasets` and the hardcoded flat checkpoint path. No successful rerun is claimed.

The read-only checks were executed as temporary inline Python, not added as test files: `ast.parse` for the 13 application modules; Pillow `load()` plus SHA-256 over all 100 images; seeded selection reconstruction from cached entry lists; score/argmax assertions; and comparison of HTML embedded data with JSON. One initial report-inspection command encountered a Windows console `UnicodeEncodeError`; rerunning with UTF-8 stdout succeeded. This was an inspection-output encoding issue, not a model failure.

## Historical results, not fresh benchmark inference

`results/benchmark100/predictions.json` records creation at `2026-10-23T12:09:34.020599+00:00`, CUDA and PyTorch `2.5.1+cu121`. Its artifact/image/checkpoint consistency was checked today; all 100 predictions were not recomputed.

| Saved evaluation | N | Correct grades | Grade accuracy |
| --- | --- | --- | --- |
| APTOS2019 subset | 34 | 31 | 91.18% |
| IDRID subset | 33 | 14 | 42.42% |
| MESSIDOR2 subset | 33 | 20 | 60.61% |
| Combined subset | 100 | 65 | 65.00% |
| Separate historical IDRiD full test | 103 | 42 | 40.78% |

The saved mixed benchmark reports zero duplicate hashes within its selected sample. This is not evidence of no training overlap. IDRID/MESSIDOR2 use the APTOS-trained model and represent transfer evaluation; these small subsets are not full benchmark or clinical performance claims. Grade 3 is absent from the APTOS subset; grades 3 and 4 are absent from the MESSIDOR2 subset.

## Known issues and unresolved evidence

1. **Full APTOS source unavailable here.** Saved audit references a missing ZIP. It reports 981 eligible test files for a target of 1,000, with 58 read/structure errors, six duplicate groups and 49 overlapping test hashes. The producing script is absent, and its exclusions cannot currently be rerun. Some duplicate groups span labels. Obtain a source location/identity and rerun validation before declaring eligibility; do not duplicate images or mix train/validation samples to reach the target.
2. **No reusable platform core yet.** Loading/preprocessing are repeated across scripts. `predict_aptos.py` parses arguments and runs the model at import. Inference, audit and metric logic need import-safe contracts before API reuse.
3. **Legacy IDRiD portability.** Uses a flat checkpoint path relative to CWD, while only the nested path exists; selects MPS/CPU but not CUDA; imports missing Hugging Face `datasets`. Historical artifacts do not prove it runs now.
4. **Dependency drift.** README upstream install uses Python 3.11, runtime is 3.10, `.venv-win` is 3.13, `.venv` is macOS. Runtime package versions differ from requirements; no validated platform environment specification exists. Do not blindly reinstall requirements.
5. **Limited validation/cache integrity.** Preparation cache checks only counts/existence; downloader depends on HTTP range support and gdown confirmation parsing. Complete source overlap checks are not part of the 100-image pipeline. Live remote downloads were not tested.
6. **Metric/generalization gaps.** Fixed 100-image counts, no generic run IDs, no durable job orchestration, no comprehensive empty/single-class behavior, and no confidence intervals. Undefined kappa can conflict with strict JSON serialization. Preserve metric meanings when extracting code.
7. **Notebook divergence.** Feature notebook uses different normalization/non-strict weights and references `dinov2_large`, absent from the current factories. MESSIDOR2 notebook includes training and is not a ready ministry demonstration notebook. Neither was executed.
8. **Training-path concerns remain outside scope.** `main_finetune.py` defaults do not match the verified APTOS CLI; eval still builds train/val datasets. The engine's generic forward/autocast path was not validated against the dedicated compatibility path. `util/pos_embed.py` contains `np.float`, incompatible with current NumPy if that helper is called. No training code was changed or exercised.
9. **Git ownership is unresolved.** `git rev-parse --show-toplevel` resolves to parent `...\Dr`. Parent index records `RETFound` as mode `160000` gitlink at `ae9a9ecf37857cf47b8aa9f87cd6f710d75db287`, but this folder has no `.git`. Parent status already contains unrelated changes. Git does not currently provide a normal file-level diff for these project changes. Do not initialize/reset/reconstruct repositories without a separate task.
10. **Application layers absent.** No FastAPI app, React app, common API schema, platform notebook or automated platform tests exist. Existing offline report UI source/data were inspected, but browser interactions were not exercised.

## Pending work and exact next scope

- Phase 2: implement dataset validation and reproducible sampling; use synthetic fixtures while full source data is unavailable. Modify existing `README.md`, `docs/IMPLEMENTATION_PLAN.md` and `docs/PROGRESS.md` only. Create the 14 package/CLI/test files listed in the plan's "Exact next-phase file scope" section. Existing Python scripts remain untouched in that phase.
- Phase 3: add shared inference and preserve prediction CLI behavior with parity evidence.
- Phase 4: shared evaluation/report adapters, improved provenance, IDRiD compatibility.
- Phase 5: inference-only notebook using shared modules.
- Phase 6: FastAPI lifecycle, prediction/evaluation jobs and contracts.
- Phase 7: API-driven React frontend and bilingual/RTL preparation.
- Phase 8: local integration and demonstration rehearsal.

No later phase has started. Resume only within the next user-authorized scope, consulting `AGENTS.md` and the implementation plan first.

## Arabic Ministry presentation - 2026-11-03

Authorized creation of a simple Arabic presentation after content and architecture
review in chat. Created docs/presentations/ministry-20261103/output/
RETFound_Syria_Ministry_AR.pptx (25 editable slides) and دليل_المتحدث.md.
Covers existing evidence vs proposed clinical workflow, four specialist questions,
Syrian data requirements, dataset independence, data/inference/review paths,
feedback, responsibilities, resources, risks and source references in slide notes.
No training, checkpoint changes, downloads of datasets or new inference.

Built with bundled @oai/artifact-tool using build/build.mjs; build/rtl.py adds
native paragraph RTL to the exported package. Finalization via build/finalize.mjs
passed integrity, geometry, Arial policy and Artifact Tool import, with zero
findings. Initial font property corrected from fontFamily to typeface. Initial
sandbox finalization failed on Windows hard-link EPERM; approved rerun succeeded.
Native PowerPoint opened final file read-only and exported all 25 slides; all
native PNG previews were visually reviewed for readability and overflow. Artifact
renderer had incorrect Arabic word order, so native PowerPoint previews were used
for final QA. No claim of live clinical validation or Syrian performance.

Public references include RETFound Nature 2023, asymmetric retinopathy PMID
3377038, NHS image quality/grading pathways, multiethnic GWAS and cross-camera
validation. Existing saved APTOS JSON supplies results; no fresh model execution.
Architecture remains a proposal, with no implementation phase newly executed.

## Concise English clinical discussion deck - 2026-11-03

User requested an English redesign focused on specialist questions and requirements,
removing unnecessary detail. Created a separate 13-slide editable deck and English
speaker guide under docs/presentations/ministry-20261103/english/output/.
Four question slides pair clinician decisions with concrete data/workflow needs.
Other slides cover minimum data, workflow, resources, key risks, feedback and
meeting decisions. Technical implementation and saved benchmark numbers were
removed from the main slides; material limitations remain explicit in notes.
Original Arabic deliverables preserved. Sources reused from prior verified research.

Builder: docs/presentations/ministry-20261103/build/english.mjs, bundled Artifact
Tool. All 13 rendered slide PNGs visually reviewed; no clipping or overlap seen.
Final package integrity, geometry, Arial policy and Artifact Tool import passed.
Sandbox hard-link EPERM required an approved rerun to finalize. This English deck
was not opened in native PowerPoint; visual checks used Artifact Tool rendering.
No new inference, model modification, dataset download or clinical implementation.
