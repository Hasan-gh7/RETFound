# Demo-only RETFound integration — 2026-11-04

## External connection file - 2026-11-05

User explicitly identified this application as the demo to run on another device.
Connection now consumes base_url and authorization together; prefers local
connection.json then parent stable file, with environment overrides preserved.
Key stays in backend. Updated ignore rule, launcher help and Python fallback.
Parent share launcher can start this adapter on 8001 alongside original site
proxy on 8002. Existing 10 adapter tests and frontend Node checks passed; isolated
connection-file selection check passed. Current external service returned 530,
so live startup/prediction remains pending. See parent docs/TWO_APPS_AR.md.

Scope: user authorized changes inside eye-ai-demo only. All source edits, new tests,
documentation and local runtime evidence remain in this folder. No parent platform,
checkpoint, data, reports, environment or running RETFound service changes. No Git
initialization: parent project is a gitlink without local repository metadata.

Implemented:
- backend/app/main.py: lifespan-managed async HTTP adapter, loopback browser origin
  checks, upload validation and explicit Windows JS/CSS MIME types with nosniff.
- backend/app/retfound_client.py: original-byte forwarding to existing /api/predict;
  server-only Bearer from stable private connection or environment; finite five-score,
  argmax, input hash, admission and provenance checks; no redirects/retries/fallback.
- Former model_runtime is a compatibility re-export, with no ONNX/synthetic engine.
- frontend: genuine RETFound contract; five scores and model provenance; errors clear
  stale results; AMD/glaucoma unavailable; browser and report summaries DR-only.
  Separate v2 local history excludes old simulated records without deleting them.
- run_demo.py and launchers: port 8001, existing ml-homework plus read-only reuse of
  parent .runtime/web. No venv creation, downloads or package installations/upgrades.
- README files, model-folder notice, security notes and optional Docker config updated.

Executed with C:/Users/jadgh/.conda/envs/ml-homework/python.exe, verified earlier by
sys.executable; Node used for frontend logic. Commands from RETFound root:

    python -B eye-ai-demo/tests/test_adapter.py
    node eye-ai-demo/tests/verify_frontend.cjs
    node --check eye-ai-demo/frontend/app.js
    python -B eye-ai-demo/run_demo.py --help

Final Python result: 10 tests passed in 7.700 seconds outside sandbox. Tests cover
exact upstream bytes/auth, provenance preservation, missing/NaN/wrong scores/hash,
upstream denial/failure/timeout with no retry/fallback, invalid/oversized uploads,
cross-origin denial, static serving and Windows MIME regression. Test models and
provider responses are synthetic. Earlier suite before MIME fix: 9 tests passed.
Frontend Node checks passed: health-only initialization, valid synthetic-response rendering,
unavailable disease cards, saved provenance, offline error clears prior result,
no automatic retry/fallback, file:// blocked and HTML element references present.
Two initial additions to the Node harness needed missing style/dataset/append mock
members; after fixing the harness, final tests passed. No production bug was hidden.

Read-only real health verification: existing RETFound /api/health returned 200 ready.
Demo /api/health returned 200 ready with cuda, float32 and preprocessing version
retfound-rgb-resize256-crop224-imagenet-v1. Browser displayed the same connected
state. No inference was needed for these GETs. Windows MIME registry maps .js to
text/plain; fixed serving within this demo only. The browser history dialog opened
and closed successfully. Desktop and narrow layouts visually inspected; actual
image prediction, print/PDF rendering and camera capture were not exercised.

Demo server launched hidden and only its own first process PID 18796 was stopped
(after exact command-line identity check) for the MIME fix. Current demo process
PID 33592 listens at http://127.0.0.1:8001. Logs:
.runtime/session-20261104-232818/{stdout.log,stderr.log,server.json}.
Preview: .runtime/connected-preview.png. Existing RETFound service not restarted.

Pending: one actual image through the new adapter. An attempted execution of
`tests/live_smoke.py --image sample_images/idrid_test.jpg` was rejected by automatic
approval review before launch because it would send a medical image onward to
external Jev without specific user authorization for that data/destination. No
image/provider request was sent and no fresh prediction is claimed. The script
is opt-in, one request, no retries, saves uniquely named local evidence on success.
Await specific authorization before this end-to-end check. No clinical-readiness,
accuracy, parity, throughput or reproducible-environment claim follows from tests.
