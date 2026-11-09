# RETFound Evaluation Platform and Jev Retinal Image Screening

Technical implementation and evaluation report | 30 October 2026 | Prepared for the project team and a technical demonstration to the Syrian Ministry of Health

## 1 Purpose and main findings

We extended an existing RETFound research project into a reusable evaluation platform and local image prediction application. The work preserved the existing APTOS classifier, added validated dataset ingestion and deterministic sampling, evaluated 1,000 APTOS test images, and connected the model to a local API and browser interface. A separate Jev screening step now checks whether an upload is identifiable as a retinal fundus photograph before the DR classifier runs.

The saved evaluation contains 847 correct five-grade predictions out of 1,000 images, or 84.70% exact-grade accuracy. Any-DR accuracy is 98.30% under the rule predicted grade greater than zero. These are different tasks: detecting any DR is easier than assigning the correct severity grade. The five-label macro F1 is 0.666041, revealing weaker performance in less frequent grades that overall accuracy alone conceals.

The project owner confirmed in this chat that the Jev workflow works successfully after the fresh-key verification and startup changes. This is user-reported operational success, not a retained authenticated API transcript or a measured Jev accuracy study. The 1,000-image evaluation was completed before Jev integration and evaluated RETFound alone. No 1,000-image Jev or combined-pipeline evaluation is claimed.

This report uses current source files, saved run artifacts and dated development records. During report preparation we independently recomputed the saved confusion matrix, accuracy, macro F1, quadratic kappa and binary counts, and checked record ordering, unique hashes and score consistency. We did not rerun model inference or download data.

## 2 Starting point and work completed

The starting project already contained the RETFound ViT architecture, an APTOS-fine-tuned checkpoint, command-line prediction, a 100-image mixed-dataset benchmark, historical IDRiD results, notebooks and offline reports. Those artifacts provided a baseline rather than evidence that a platform already existed. The initial inspection documented environment differences, checkpoint locations, import-time inference in the legacy prediction script, dataset provenance gaps and the parent Git gitlink issue.

| Work area | Delivered behavior |
| --- | --- |
| Dataset validation | Explicit grade mapping, local folder and ZIP readers, bounded decoding, path and archive protections, duplicate and cross-split evidence. |
| Sampling | Stable candidate ordering, persisted selection, explicit seed, uniform sampling without replacement and explicit shortage errors. |
| Inference | Import-safe shared predictor, strict trusted checkpoint loading, original preprocessing and forward path, five finite scores and actual device provenance. |
| Evaluation | Versioned JSON and CSV, defined metric edge cases, new run directories, offline HTML viewer and saved selection/audit evidence. |
| Local API and UI | Raw or multipart image upload, bounded request handling, model loaded once, research results with five scores, JSON download and saved evaluation view. |
| Jev admission | Backend HTTP image classification with choices 0 and 1; failures and rejection prevent RETFound invocation; secure-key diagnostic and startup. |

No training, fine-tuning or checkpoint replacement was performed for platform development. The separate Nature CFP pretraining asset is not substituted for the existing APTOS classifier. Prior review/reference admission code remains historical and inactive in the current API; Jev is the current admission mechanism. Proposed notebook, durable evaluation jobs, broader deployment and clinical validation are not reported as completed.

## 3 Current system workflow

A browser or another application on the same computer sends one image to POST /api/predict. The backend enforces upload size, supported format, decoding, pixel and single-frame constraints. It prepares a separate image copy for Jev if its dimensions or format require conversion. The backend sends an authenticated HTTP request to OpenRouter. A valid Jev decision of 1 allows the original uploaded bytes to proceed to the shared RETFound predictor. The API returns the predicted grade, all five softmax scores, image hash, admission metadata, timing and model identity.

| Jev outcome | API behavior | RETFound action |
| --- | --- | --- |
| 0 | HTTP 422; not_retinal_fundus; prediction is null; decision 0 | Not invoked |
| 1 | Successful prediction with accepted input status and decision 1 | Run on original uploaded bytes |
| Timeout or provider failure | HTTP 503; fundus_check_unavailable; no DR scores | Not invoked |
| Malformed or non-binary answer | Service error; no DR prediction | Not invoked |

Fundus decision 0 and DR grade 0 have different meanings. Fundus decision 0 rejects an image that was not identified as a fundus photograph. DR grade 0 means the accepted retinal image was classified as No DR. A failed external request is a service failure and is not converted into a non-fundus classification.

The API is bound to loopback for use on this computer, with explicit browser origin and Host controls. One inference executor and three admitted slots bound work; a cancelled request retains its slot until its worker finishes. Uploads are handled in memory and are not saved as a server prediction history. The interface displays backend results rather than implementing its own model or metrics. Images sent to Jev leave the computer for OpenRouter and its provider; local memory handling is not a statement about external provider retention.

## 4 RETFound inference contract

The architecture is models_vit.RETFound_mae with img_size 224, num_classes 5 and global_pool True. The loader resolves the explicit checkpoint first, then the supported local layouts. The actual baseline checkpoint is checkpoints/checkpoints/APTOS2019/checkpoint-best.pth. It is loaded on CPU using the compatible mmap and weights_only settings, validates the model configuration and loads checkpoint model weights strictly. Remote or uploaded checkpoint files are not accepted.

Preprocessing is unchanged: Pillow decode, RGB conversion, bicubic resize of the shorter edge to 256, center crop 224, tensor conversion, and ImageNet normalization with mean 0.485, 0.456, 0.406 and standard deviation 0.229, 0.224, 0.225. No EXIF rotation, retinal crop, enhancement, augmentation or replacement normalization is silently introduced. The shared predictor uses eval mode and torch.inference_mode, calls forward_features, flattens features per batch and applies model.head. It requires finite logits of shape batch by 5.

| Grade | Meaning |
| --- | --- |
| 0 | No DR |
| 1 | Mild |
| 2 | Moderate |
| 3 | Severe |
| 4 | Proliferative |

The result is the argmax of five softmax scores. These are uncalibrated model scores, not validated clinical probabilities. The baseline uses float32. CUDA, CPU and MPS selection are supported by code; historical parity checks exercised CUDA and CPU, while MPS was not exercised. Shared modules do not load the model or allocate a GPU during import.

## 5 Dataset audit and selection for the 1000 image evaluation

The evaluated source is the locally supplied APTOS2019 ZIP identified by its exact archive SHA-256. Its recognized folders supplied 2,048 train, 514 validation and 1,100 test images. The current audit recorded zero structure/read issues and identified 1,036 eligible test images. Sixty-four test paths were excluded. Overlapping reason counts include 56 cross-split matches, 12 conflicting-label records and four redundant same-label test copies; these counters cannot be added to infer the number excluded.

The older audit reporting 981 eligible images is a separate historical artifact. It is not the source of the completed 1,000-image run, and its discrepancy was not resolved by duplicating images or borrowing training data. The later run used a fresh audit of the available archive. Explicit numeric and documented named class folders are mapped to grades; labels are not assigned by incidental directory sorting.

Selection used uniform sampling without replacement from the 1,036 eligible test candidates, seed 20261023, with stable ordering and a persisted selection manifest. This is a uniform image sample, not a class-balanced demonstration. It contains 1,000 distinct exact-byte image hashes. Exact overlap checks cover the supplied train, validation and test splits. This does not establish patient independence, absence of near duplicates, or independence from the original checkpoint training data.

## 6 Results of the saved 1000 image run

Run ID aptos1000-20261029 was saved on 29 October 2026 at 20:46:51 UTC, equivalent to 23:46:51 in Damascus. The recorded device was CUDA and dtype float32. Recorded elapsed time was 84.98 seconds from audit start through prediction and metric creation, excluding Python startup and final serialization. It is a single laptop measurement and contains no Jev request time.

| Metric | Result |
| --- | --- |
| Images / correct / incorrect | 1000 / 847 / 153 |
| Exact five-grade accuracy | 84.70% |
| Five-label macro F1 | 0.666041 |
| Quadratic weighted kappa | 0.913479 |
| Any-DR accuracy | 98.30% |
| Any-DR sensitivity | 98.9474% |
| Any-DR specificity | 97.7143% |
| True negatives / false positives | 513 / 12 |
| True positives / false negatives | 470 / 5 |

Confusion matrix: rows are true grades and columns are predicted grades, in fixed order 0 through 4. Diagonal entries are correct severity predictions.

| True grade | Pred 0 | Pred 1 | Pred 2 | Pred 3 | Pred 4 |
| --- | --- | --- | --- | --- | --- |
| 0 | 513 | 7 | 5 | 0 | 0 |
| 1 | 2 | 36 | 47 | 0 | 1 |
| 2 | 2 | 10 | 241 | 6 | 2 |
| 3 | 0 | 1 | 27 | 19 | 7 |
| 4 | 1 | 0 | 21 | 14 | 38 |

| Grade | True count | Precision | Recall | F1 |
| --- | --- | --- | --- | --- |
| 0 | 525 | 99.03% | 97.71% | 0.9837 |
| 1 | 86 | 66.67% | 41.86% | 0.5143 |
| 2 | 261 | 70.67% | 92.34% | 0.8007 |
| 3 | 54 | 48.72% | 35.19% | 0.4086 |
| 4 | 74 | 79.17% | 51.35% | 0.6230 |

Per-grade precision, recall and F1 in this table were derived during report preparation from the saved confusion matrix; they are not a new inference run. Recall is 97.71% for grade 0, 41.86% for grade 1, 92.34% for grade 2, 35.19% for grade 3 and 51.35% for grade 4. The sample has 525 grade-0 images, so overall accuracy is strongly influenced by that class.

Important errors include 47 of 86 mild images predicted as moderate, 27 of 54 severe images predicted as moderate, and 21 of 74 proliferative images predicted as moderate. Binary any-DR accuracy hides these severity errors because predictions above grade 0 all count as DR. The five false negatives are labeled DR images predicted as No DR; the 12 false positives are labeled No DR images predicted as a DR grade. No referral policy or clinical operating threshold was validated.

Accuracy is correct divided by total. Macro F1 averages the five class F1 values with absent-class behavior retained from the legacy five-label definition. Quadratic kappa weights grade disagreement by squared severity distance. Any-DR metrics collapse grades 1 to 4 into positive and use argmax grade greater than zero, not a probability threshold. Undefined metrics in the shared evaluation contract are JSON null with reasons, not NaN or Infinity.

## 7 Other historical evaluation evidence

| Saved dataset evaluation | Images | Correct | Accuracy |
| --- | --- | --- | --- |
| APTOS subset in mixed benchmark | 34 | 31 | 91.18% |
| IDRiD transfer subset | 33 | 14 | 42.42% |
| MESSIDOR2 transfer subset | 33 | 20 | 60.61% |
| Combined mixed benchmark | 100 | 65 | 65.00% |
| Separate historical IDRiD test | 103 | 42 | 40.78% |

These are historical saved results summarized in the progress record, not rerun for this report. IDRiD and MESSIDOR2 evaluate transfer of the APTOS classifier and must remain separate from APTOS within-dataset performance. Different source datasets, sample sizes and class mixtures prevent treating these figures as direct like-for-like comparisons or evidence of improvement over time.

## 8 Jev implementation and troubleshooting

Jev is called through ordinary backend HTTP requests, without an OpenRouter workflow node or a new SDK dependency. The configured model ID is typesafe/jev-1.14 and the endpoint is https://openrouter.ai/api/alpha/decisions. Authentication uses Authorization Bearer with the server-held OpenRouter inference key. It remains an OpenRouter-routed request, rather than a direct TypeSafe-provider request. The choice question asks for one of the predefined strings 0 and 1, then the backend strictly validates and converts that value into its binary contract.

Choice 1 describes an identifiable retinal fundus photograph showing the interior retinal surface and anatomy. Choice 0 covers unrelated scenes, external eye photographs, OCT images, diagrams and images not identifiable as fundus photographs. Instructions tell Jev to judge visual content and ignore instructions written in the image. These criteria define the requested behavior; they do not prove detection accuracy or resistance to misleading inputs.

Jev requires a separate supported image representation. The sample file is 4288 by 2848 pixels, beyond the documented maximum of 1568 per side. Screening copies are resized within 256 to 1568 pixels per side and at least 78,400 total pixels, with extreme aspect ratios rejected. Supported compatible PNG/JPEG bytes can be retained; otherwise RGB JPEG is generated for Jev only. RETFound receives the original payload through its unchanged preprocessing. Changes to this screening copy have not been evaluated for their effect on Jev accuracy.

Integration exposed HTTP 400 and timeout failures. Early messages were too generic and did not establish a cause. The client now distinguishes authentication, credits, permissions, request/model errors, rate limits, network/TLS failures, timeouts and malformed responses. It uses a 90-second socket timeout, configurable from 1 to 90 seconds, bounded response reads and disabled redirects. It does not automatically retry paid model requests. Sanitized validation details and response-type diagnostics exclude the key and encoded image blobs.

The diagnostic now validates expected key syntax locally and calls GET https://openrouter.ai/api/v1/key before any model request. This checks authentication without invoking Jev and rejects management/provisioning keys. It then tests a text fixture and the sample image separately. A hidden fresh-key prompt avoids reusing a stale terminal value. The optional startup step passes the tested key to the child server environment without saving it or putting it in process arguments.

The user subsequently reported successful operation. We do not have a retained successful authenticated trace, measured Jev latency, confusion matrix or confirmed root cause for the earlier empty HTTP 400. Successful startup confirms an operational workflow as reported by the user; it does not validate fundus screening sensitivity, specificity or the combined system on 1,000 images.

## 9 Verification and evidence boundaries

| Evidence | What it supports | Boundary |
| --- | --- | --- |
| Saved 1000-image predictions and completion marker | Completed RETFound evaluation and recorded metrics | Predates Jev; no fresh inference for this report |
| Fresh report consistency checks | Record count, score consistency, selection order and recomputed metrics | Does not revalidate original diagnoses or rerun the checkpoint |
| Historical inference parity | 34 APTOS images matched saved scores exactly; one CPU/CUDA delta about 1.79e-7 | Recorded development evidence; MPS untested |
| Historical API/UI verification | Real CUDA HTTP parity, raw/multipart behavior, concurrency and asset MIME checks | Earlier direct-input workflow, before Jev |
| 18 gate and diagnostic tests | Binary parsing, blocked inference paths, key handling, errors, dimensions and startup handoff | Mock provider responses; not a Jev accuracy study |
| User confirmation on 30 October | Jev workflow reported to work after startup changes | No retained authenticated transcript or quantified accuracy |

Earlier development records include successful full-suite runs of 46 Python tests and UI contract checks at that stage. A later combined gate/API run stalled after gate tests and was interrupted; it must not be represented as a completed current full-suite pass. The most recent gate/diagnostic suite had 18 passing tests. Browser contract tests use stubs and do not replace visual testing in a real browser. This report does not invent an updated aggregate test count.

## 10 Startup and demonstration procedure

Use the existing ml-homework interpreter. From the project directory, stop an old server with Ctrl+C before launching so that the launcher does not reuse stale configuration. Run the command below, paste the raw key at the hidden prompt and keep the terminal open. The text and image requests may be billed by OpenRouter.

```powershell
& "$env:USERPROFILE\.conda\envs\ml-homework\python.exe" -B scripts/diagnose_jev.py --new-key --start-server
```

After successful checks the server opens http://127.0.0.1:8000. Select a fundus image, run analysis and inspect all five scores. Use a non-fundus image to demonstrate rejection only as an actual live observation, not as a guaranteed model outcome. Verify that rejection or service failure clears earlier results and does not show a disease grade. Review the saved evaluation in the interface or the offline results/runs/aptos1000-20261029/index.html viewer. Download JSON only for the intended case.

The original evaluation command is recorded below for reproducibility. It was executed for the saved run, not again during report preparation. If rerunning is separately authorized, choose a new output directory and confirm the explicit dataset source. Do not overwrite historical evidence or interpret an existing report as a new run.

```powershell
& "$env:USERPROFILE\.conda\envs\ml-homework\python.exe" -B scripts/evaluate_aptos.py APTOS2019.zip --count 1000 --device cuda --output results/runs/NEW_RUN_ID
```

## 11 Limitations and proposed next work

The deliverable is a research demonstration, not a clinically validated screening service. Ground truth comes from the supplied folder labels. Patient identities, near-duplicate methods and checkpoint-matched training split provenance were unavailable, so those independence claims remain unverified. Exact-byte exclusions address only the overlaps detectable by that method. Scores are uncalibrated and no confidence intervals or prospective clinical study were produced.

Jev introduces external connectivity, provider availability, billing and data-handling dependencies. Its binary output can be wrong. Neither modality screening nor image-quality acceptance has been validated on a labeled positive-and-negative corpus. The original 1,000 retinal images cannot by themselves quantify specificity against non-fundus uploads. A real fundus image falsely rejected by Jev never reaches RETFound, so combined-system performance requires separate measurement.

Proposed next work is to assemble an explicitly labeled fundus/non-fundus and poor-quality set, record Jev outcomes and provider/model versions, measure false acceptance, false rejection, failures and latency, then evaluate the combined pipeline. Include genuine fundus, external-eye photos, OCT, scans, diagrams and unrelated photographs. Preserve all exclusions and failure accounting rather than reporting only accepted cases. These are proposals, not completed experiments or authorization to run a paid 1,000-image Jev batch.

Other pending work includes a validated complete dependency specification, fuller browser visual verification, source-control ownership repair as a separate authorized task, and any requested notebook, deployment or bilingual preparation. The parent Git repository records this folder as a gitlink while the folder lacks its own Git metadata; normal parent status is not proof that these source edits are tracked.

## 12 Provenance and source register

| Recorded runtime component | Value |
| --- | --- |
| torch | 2.5.1+cu121 |
| torchvision | 0.20.1+cu121 |
| timm | 0.9.16 |
| Pillow | 12.0.0 |
| numpy | 2.2.6 |
| scikit-learn | 1.7.2 |
| Python | 3.10.19 |
| Device / dtype | cuda / float32 |
| GPU in inspection record | NVIDIA GeForce RTX 3070 Laptop GPU |

Checkpoint SHA-256: a96b9dbcb78eff373912fb0a48d316dc35ffb0715bb2a1b9128b096d780edbbf

Dataset archive SHA-256: fd04f48ee1889f64e5c7f4edad4a16b4468fed2d709a21e1107ddc1ff6eb1dff

Audit ID: 35d2d28e58b78cbe99f9f08359bc68e2163ab73f071668a529937c839267a33c

Selection ID: 71a743c14dc83254dc54177ae533a84ab5a7923f50d0af365b90df381ac44349

Preprocessing version: retfound-rgb-resize256-crop224-imagenet-v1. Evaluation schema: retfound-evaluation/1. Jev admission policy: jev-fundus-choice-v1.

results/runs/aptos1000-20261029/predictions.json — Authoritative saved per-image scores, provenance and metrics.

results/runs/aptos1000-20261029/audit.json — Split validation, duplicate and exclusion evidence.

results/runs/aptos1000-20261029/selection.json — Ordered seeded sample manifest.

results/runs/aptos1000-20261029/completed.json — Completion marker.

docs/PROGRESS.md — Dated implementation and verification record.

docs/IMPLEMENTATION_PLAN.md — Authorized scope and remaining proposals.

docs/API.md — Local API contracts, startup and troubleshooting.

retfound_platform/inference/fundus_gate.py — Current Jev request and rejection behavior.

retfound_platform/inference/predictor.py — Current RETFound forward path.

retfound_platform/evaluation/metrics.py — Metric definitions.

External API references used during implementation: https://openrouter.ai/docs/guides/community/multimodal-decisions ; https://openrouter.ai/docs/api/api-reference/alphadecisions/submit-a-decisions-request ; https://openrouter.ai/docs/api/api-reference/api-keys/get-current-key . The local source describes the implemented contract; provider capabilities and limits can change.

Reader guidance: use the run artifacts for detailed numerical evidence, the source code for current behavior and the progress log for the chronology. Later dated changes supersede older descriptions. User confirmation is explicitly attributed. No performance figure from RETFound is attributed to Jev.