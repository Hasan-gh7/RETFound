# RETFound local web application and image API

Start `run_web.bat` from the project folder. It uses the verified `ml-homework`
Python interpreter, loads the existing classifier once, and opens
<http://127.0.0.1:8000> when the model is ready. Keep the launch window open while
using the application; press Ctrl+C there to stop it.

If RETFound is already running on the selected port, the launcher reuses it and
opens the page without loading another model. Existing device/CORS settings remain
in effect; changing those settings requires stopping and restarting that server.
If another application owns the port, the launcher exits before loading weights
and suggests another port. It never automatically stops the port owner.

The workspace contains image analysis, a saved evaluation summary, integration
examples, and the model identity. Uploading a new image does not supply a true label.
The sample-image button selects a real local sample; clicking Analyze runs fresh
inference on it. New uploads must pass the Jev fundus check after file validation. The evaluation page explicitly displays the earlier saved
1,000-image run rather than a new evaluation.

## Installation and runtime

The API dependencies have been installed and tested in `.runtime/web`. They are
isolated from the existing Conda environment. On a fresh checkout, run
`setup_web.bat` once using the working model environment. `requirements-web.txt`
pins the API dependency set; it is not a lock for the full model environment.
The existing model packages and `uvicorn` are still supplied by `ml-homework`.

Direct launch from PowerShell:

```powershell
$retfoundPython = Join-Path $env:USERPROFILE '.conda\envs\ml-homework\python.exe'
& $retfoundPython -B scripts/serve_web.py --device cuda --open-browser
```

Optional flags: `--port 8001`, `--device cpu`, `--device auto`, and repeatable
`--allow-origin http://localhost:3000`. The launcher always binds to loopback,
uses one server worker, and does not change firewall or network configuration.
Do not run multiple workers against this GPU model.

## Prediction request

### Postman

Import `docs/RETFound.postman_collection.json` into Postman Desktop. It contains
Health, Model identity and Predict image requests plus response checks.

1. Open **1. Health** and click **Send**. Expect `200 OK` and `"status": "ready"`.
2. Open **3. Predict image**. Its URL is `http://127.0.0.1:8000/api/predict` and method is POST.
3. In **Body → form-data**, the key must be **image** and its type must be **File**.
4. Select a local image, for example `sample_images/idrid_test.jpg` in this project.
5. Click **Send**. Expect a JSON prediction with five scores and `200 OK`.

No registration or reviewer approval is required for a new retinal image.
The model does not identify non-retinal photographs; it can assign them a DR grade.

Leave the Content-Type header unset: Postman creates the multipart boundary.
Do not send a file path as a text field or JSON. If you use Postman in a browser,
select its **Desktop Agent**; the Cloud Agent cannot reach this computer's loopback
address. See [Postman file uploads](https://learning.postman.com/docs/use/send-requests/create-requests/parameters)
and [Postman agents](https://learning.postman.com/docs/getting-started/basics/about-postman-agent).

### Direct HTTP clients

`POST http://127.0.0.1:8000/api/predict`

Send exactly one file in the multipart field `image`:

```powershell
curl.exe -X POST "http://127.0.0.1:8000/api/predict" -F "image=@C:/images/retina.jpg"
```

Or send the raw file body:

```powershell
curl.exe -X POST "http://127.0.0.1:8000/api/predict" -H "Content-Type: image/jpeg" --data-binary "@C:/images/retina.jpg"
```

Python client:

```python
import requests

with open("retina.jpg", "rb") as image:
    response = requests.post(
        "http://127.0.0.1:8000/api/predict",
        files={"image": image},
        timeout=120,
    )
response.raise_for_status()
result = response.json()
print(result["predicted_grade"], result["predicted_label"])
print(result["scores"])
```

Supported decoded formats: JPEG, PNG, TIFF, BMP and WebP; single-frame images only.
Maximum image size is 20 MiB and 40 million pixels. Body size is bounded even
without Content-Length. Multipart overhead is limited to 64 KiB beyond the image
limit. A complete upload must arrive within 30 seconds.

The backend checks decoded content. Filename and MIME type alone do not establish
validity. Files are parsed in memory; no uploads, patient identifiers, or prediction
history are persisted by the server. The JSON download is an explicit browser action.
## Jev retinal fundus gate

Every upload is decoded, then sent by backend HTTP POST to
`https://openrouter.ai/api/alpha/decisions` using `typesafe/jev-1.14`.
Only choice `1` proceeds to RETFound; choice `0` returns HTTP 422,
`not_retinal_fundus`, `prediction: null` and `input_validation.decision: 0`.
Missing credentials, invalid answers, timeout or provider errors return HTTP 503
`fundus_check_unavailable` with no DR prediction. There is no bypass.

Set the key in the PowerShell session that launches the server (never in frontend
code or source files). Stop the existing server with Ctrl+C in its window first;
the launcher reuses an existing server and cannot update its environment.

```powershell
$jevKey = Read-Host 'OpenRouter API key (input hidden)' -AsSecureString
$env:OPENROUTER_API_KEY = [System.Net.NetworkCredential]::new('', $jevKey).Password
& "$env:USERPROFILE\.conda\envs\ml-homework\python.exe" -B scripts/serve_web.py --open-browser
```

Images leave this computer for OpenRouter/TypeSafe. Uploads are not saved locally.
A separate Jev copy is resized as needed to meet its dimension and total-pixel
limits (256..1568 per side, at least 78,400 total pixels). Images needing resizing
or format conversion are encoded as RGB JPEG solely for Jev. Compliant PNG/JPEG
bytes are preserved when within its 16 MiB file limit. RETFound receives the original bytes and its preprocessing is unchanged.
Successful responses report `status: accepted`, `decision: 1`, policy
`jev-fundus-choice-v1`; automatic modality screening is enabled. This is not a
validated image-quality or clinical gate. No live Jev accuracy claim is made.

API contract source: https://openrouter.ai/blog/insights/what-is-jev/

## Response contract

The successful response contains:

| Field | Meaning |
| --- | --- |
| `schema_version` | `retfound-prediction/1` |
| `request_id`, `created_utc` | Unique request identity and UTC completion time |
| `predicted_grade`, `predicted_label` | Argmax grade and canonical name |
| `scores` | Exactly five softmax scores in fixed grade order 0..4 |
| `top_score` | Score for the predicted class |
| `image_sha256` | SHA-256 of the uploaded bytes |
| `elapsed_ms` | Time from request admission through upload/inference completion; includes queue wait |
| `model` | Checkpoint SHA-256, preprocessing version, actual device, dtype and grade order |
| `input_validation` | `accepted` status, binary decision 1, exact image hash, Jev admission basis, policy version and limitations |
| `interpretation` | Uncalibrated scores; research use, not clinical diagnosis |

Grade order: 0 No DR, 1 Mild DR, 2 Moderate DR, 3 Severe DR, 4 Proliferative DR.
Scores are uncalibrated model outputs. There is no inferred ground-truth label,
tuned diagnostic threshold, treatment recommendation, or retinal-image quality check.

`GET /api/health` reports readiness, admitted requests and capacity.
`GET /api/model` returns model identity without local checkpoint paths.
`GET /openapi.json` provides the machine-readable API specification.

Errors use this shape:

```json
{
  "error": {"code": "invalid_image", "message": "A readable explanation"},
  "request_id": "request identifier when assigned"
}
```

| HTTP status | Meaning |
| --- | --- |
| 400 | Malformed/interrupted upload |
| 403 | Browser origin not allowed |
| 408 | Upload timeout |
| 413 | Image/body too large |
| 415 | Unsupported request media type |
| 422 | Missing image field, multiple files, incomplete or unreadable image |
| 429 | Capacity reached; retry after the `Retry-After: 2` interval |
| 500 | Inference failure; private error details remain in the server log |
| 503 | Model unavailable |

There are three admitted request slots and a single inference executor. Slots
include upload time and queue wait. If a client disconnects during inference,
its slot stays occupied until the work finishes. Health checks remain responsive
while inference is running. This is a bounded synchronous prediction API, not a
persistent evaluation-job service.

## Browser integration

Backend applications on this computer can call the loopback endpoint directly.
A browser application on another port must be explicitly allowed:

```powershell
.\run_web.bat --allow-origin http://localhost:3000
```

Use the exact scheme, host and port of that application. Wildcard origins are
rejected. The bundled interface uses the same origin and needs no extra CORS
configuration. Host validation allows loopback hostnames only. Public/LAN hosting,
authentication, TLS, and reverse-proxy deployment are outside this local build.

## Verification

```powershell
& $retfoundPython -B scripts/test_web.py
node tests/verify_web_ui.cjs
# With the real server running, choose a new output filename:
& $retfoundPython -B scripts/verify_web.py --output results/runs/my-web-check/verification.json
```

The API unit tests use a clearly labeled test predictor. The separate HTTP
verification uses the real checkpoint, compares its result with earlier
verified CUDA scores, and submits a new encoding of a fundus image without approval.
Unit tests verify new images reach the predictor and corrupt images do not. Frontend contract tests use a minimal DOM stub and recorded
responses; they are not visual browser tests. The actual browser-access host was
unavailable during implementation, so desktop/mobile rendering, the native file
picker and browser download behavior remain visually unverified.

Implementation references: [FastAPI lifespan model loading](https://fastapi.tiangolo.com/advanced/events/)
and [Python-Multipart](https://pypi.org/project/python-multipart/). Local launch
instructions and measured results take precedence over upstream examples.

### Jev connection troubleshooting

Restart after updating the code to see specific failure messages. HTTP 401 means
key rejected; 402 insufficient credits; 403 access denied; 429 rate limited.
HTTP 400/422 indicates a rejected request; 404 an unavailable endpoint/model.
Connection, TLS, timeout and invalid-response errors have separate messages.
All failures block RETFound; none count as a binary non-fundus classification.
Never paste keys into chat or browser code.

HTTP 400/422 now includes a bounded, sanitized provider validation message.
The sample image exceeds Jev dimensions and is resized only for screening.

### Jev timeouts and direct connection test

The Jev socket timeout defaults to 90 seconds (previously 30). Set
`JEV_TIMEOUT_SECONDS` to a finite value from 1 to 90 before starting the server.
This is a socket-operation timeout, not a guaranteed total request deadline.
The browser waits 120 seconds; concurrent queued requests can take longer.
No automatic retries or fallback admission are performed.

Stop the server with Ctrl+C, then use the same terminal (with the API key set):

```powershell
& "$env:USERPROFILE\.conda\envs\ml-homework\python.exe" -B scripts/diagnose_jev.py
```

The diagnostic makes a text request then a sample-image request to OpenRouter;
both may incur charges. If no key exists in this terminal it prompts invisibly,
without saving it. Text failure skips the image. Separate timing and sanitized
error output help distinguish general connection/provider failure from
image-specific or intermittent behavior. No DR model is loaded or run.
Use `--image "C:/images/retina.jpg"` to choose an explicit image. Do not paste keys
into chat. Share only the diagnostic output. Then restart serve_web.py normally.

The diagnostic now prints error response content type and inspected byte count
for HTTP 400/422, and whether an HTTPS proxy is configured (no proxy URL). Error
messages support alternative JSON shapes and HTML titles. HTTP 400 does not by
itself prove which field is invalid; use these details before changing payloads.

### Fresh-key verification and startup

Stop the existing server first with Ctrl+C. From the project directory run:

```powershell
& "$env:USERPROFILE\.conda\envs\ml-homework\python.exe" -B scripts/diagnose_jev.py --new-key --start-server
```

Paste only the raw OpenRouter inference key into the hidden prompt, without
quotes or the word Bearer. This command checks key syntax locally, checks
GET https://openrouter.ai/api/v1/key (no model invocation), then tests text and
sample-image Jev requests. Failed authentication skips billed model requests.
If successful it launches the web server using the same tested key in its child
environment. The key is never saved or put in process arguments. The parent
PowerShell environment is not changed. Keep the terminal open while serving.
Do not use a management/provisioning key. An empty HTTP 400 from the key endpoint
means the failure is outside the classifier payload; preserve the stage output
for troubleshooting. No live success is guaranteed by the unit tests.

## Labeled dataset tests on the local server

After restarting with the working key, open http://127.0.0.1:8000/dataset-tests
or click Dataset tests in the main navigation. The page shows the existing 15
examples, five each from IDRiD, MESSIDOR2 and DDR, covering grades 0..4.
Test one image or click Test all 15 images. Each test sends one image to Jev
through OpenRouter (potential charges); accepted images proceed to RETFound.
Opening the page or reading previews does not invoke inference. The page compares
backend predictions with dataset-supplied reference labels, displays all five
scores, and exports session JSON. It does not compute representative accuracy.
Reference labels never enter the model inputs. Jev rejection is not a DR grade.

| Route | Purpose |
| --- | --- |
| GET /api/demo | Validated catalog with sample IDs and reference labels |
| GET /api/demo/{sample_id}/image | Hash-verified image bytes |
| POST /api/demo/{sample_id}/predict | Same gated predictor as uploads, plus trusted reference and match flag |

Example IDs: IDRID-0, MESSIDOR2-2, DDR-4. POST needs no image body or label.
The server loads the fixed registered image, rejects changed bytes and computes
`matches_true_grade`. Success uses schema `retfound-demo-result/1`, with
`reference` and the full ordinary `prediction` response. Errors have no match
flag or disease prediction. The manifest and downloaded source files are read
only. Arbitrary paths or URLs cannot be supplied. Regular /api/predict is unchanged.

All-15 runs sequentially. Stop after current image finishes does not cancel paid
work already started. Server failures/rate limits stop the batch. Disconnection or
client timeout records outcome unknown and prevents retry until the user checks
the server and reloads. No automatic retries. Session results are lost on reload
unless downloaded, and errors/untested records remain visible in exported JSON.
The existing reference-only saved 1,000-image evaluation is unaffected.
