"""Build a portable project report from saved evaluation evidence; no inference."""
import hashlib
import html
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / 'results/runs/aptos1000-20261029'
OUT = ROOT / 'docs/reports/retfound-jev-20261030'


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    p = json.loads((RUN / 'predictions.json').read_text(encoding='utf-8'))
    selection = json.loads((RUN / 'selection.json').read_text(encoding='utf-8'))
    records = p['records']
    cm = [[0] * 5 for _ in range(5)]
    for record in records:
        cm[record['true_grade']][record['predicted_grade']] += 1
        scores = record['scores']
        if len(scores) != 5 or not all(math.isfinite(v) for v in scores) or abs(sum(scores) - 1) > 1e-5:
            raise ValueError('Invalid saved scores')
        if max(range(5), key=scores.__getitem__) != record['predicted_grade']:
            raise ValueError('Saved argmax mismatch')
    n = len(records)
    correct = sum(cm[i][i] for i in range(5))
    truth = [sum(row) for row in cm]
    predicted = [sum(row[i] for row in cm) for i in range(5)]
    f1 = [2 * cm[i][i] / (truth[i] + predicted[i]) for i in range(5)]
    qwk = 1 - sum((i-j)**2 * cm[i][j] for i in range(5) for j in range(5)) / sum(
        (i-j)**2 * truth[i] * predicted[j] / n for i in range(5) for j in range(5))
    binary = {'tn': cm[0][0], 'fp': sum(cm[0][1:]), 'fn': sum(cm[i][0] for i in range(1,5)),
              'tp': sum(cm[i][j] for i in range(1,5) for j in range(1,5))}
    saved = p['metrics']['All']
    checks = {
        'record_count_1000': n == 1000,
        'unique_image_hashes_1000': len({r['image_sha256'] for r in records}) == 1000,
        'selection_hash_order_matches': [r['image_sha256'] for r in records] == [r['image_sha256'] for r in selection['records']],
        'confusion_matches_saved': cm == saved['confusion'],
        'accuracy_matches_saved': correct / n == saved['accuracy'],
        'macro_f1_matches_saved': abs(sum(f1)/5 - saved['macro_f1']) < 1e-12,
        'quadratic_kappa_matches_saved': abs(qwk - saved['quadratic_kappa']) < 1e-12,
        'binary_counts_match_saved': all(binary[k] == saved['binary'][k] for k in binary),
        'finite_normalized_scores_and_argmax': True,
    }
    if not all(checks.values()):
        raise ValueError(checks)
    md, body = [], []
    def title(text):
        md.append('# ' + text)
        body.append('<h1>' + html.escape(text) + '</h1>')
    def heading(text):
        md.append('\n## ' + text)
        body.append('<h2>' + html.escape(text) + '</h2>')
    def para(text):
        md.append('\n' + text)
        body.append('<p>' + html.escape(text) + '</p>')
    def table(headers, rows):
        rows = [[str(x) for x in row] for row in rows]
        md.extend(['\n| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join('---' for _ in headers) + ' |'])
        md.extend('| ' + ' | '.join(row) + ' |' for row in rows)
        body.append('<table><thead><tr>' + ''.join('<th>' + html.escape(x) + '</th>' for x in headers) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join('<td>' + html.escape(x) + '</td>' for x in row) + '</tr>' for row in rows) + '</tbody></table>')
    def code(text):
        md.append('\n```powershell\n' + text + '\n```')
        body.append('<pre>' + html.escape(text) + '</pre>')

    title('RETFound Evaluation Platform and Jev Retinal Image Screening')
    para('Technical implementation and evaluation report | 30 October 2026 | Prepared for the project team and a technical demonstration to the Syrian Ministry of Health')
    heading('1 Purpose and main findings')
    para('We extended an existing RETFound research project into a reusable evaluation platform and local image prediction application. The work preserved the existing APTOS classifier, added validated dataset ingestion and deterministic sampling, evaluated 1,000 APTOS test images, and connected the model to a local API and browser interface. A separate Jev screening step now checks whether an upload is identifiable as a retinal fundus photograph before the DR classifier runs.')
    para('The saved evaluation contains 847 correct five-grade predictions out of 1,000 images, or 84.70% exact-grade accuracy. Any-DR accuracy is 98.30% under the rule predicted grade greater than zero. These are different tasks: detecting any DR is easier than assigning the correct severity grade. The five-label macro F1 is 0.666041, revealing weaker performance in less frequent grades that overall accuracy alone conceals.')
    para('The project owner confirmed in this chat that the Jev workflow works successfully after the fresh-key verification and startup changes. This is user-reported operational success, not a retained authenticated API transcript or a measured Jev accuracy study. The 1,000-image evaluation was completed before Jev integration and evaluated RETFound alone. No 1,000-image Jev or combined-pipeline evaluation is claimed.')
    para('This report uses current source files, saved run artifacts and dated development records. During report preparation we independently recomputed the saved confusion matrix, accuracy, macro F1, quadratic kappa and binary counts, and checked record ordering, unique hashes and score consistency. We did not rerun model inference or download data.')

    heading('2 Starting point and work completed')
    para('The starting project already contained the RETFound ViT architecture, an APTOS-fine-tuned checkpoint, command-line prediction, a 100-image mixed-dataset benchmark, historical IDRiD results, notebooks and offline reports. Those artifacts provided a baseline rather than evidence that a platform already existed. The initial inspection documented environment differences, checkpoint locations, import-time inference in the legacy prediction script, dataset provenance gaps and the parent Git gitlink issue.')
    table(['Work area', 'Delivered behavior'], [
        ['Dataset validation', 'Explicit grade mapping, local folder and ZIP readers, bounded decoding, path and archive protections, duplicate and cross-split evidence.'],
        ['Sampling', 'Stable candidate ordering, persisted selection, explicit seed, uniform sampling without replacement and explicit shortage errors.'],
        ['Inference', 'Import-safe shared predictor, strict trusted checkpoint loading, original preprocessing and forward path, five finite scores and actual device provenance.'],
        ['Evaluation', 'Versioned JSON and CSV, defined metric edge cases, new run directories, offline HTML viewer and saved selection/audit evidence.'],
        ['Local API and UI', 'Raw or multipart image upload, bounded request handling, model loaded once, research results with five scores, JSON download and saved evaluation view.'],
        ['Jev admission', 'Backend HTTP image classification with choices 0 and 1; failures and rejection prevent RETFound invocation; secure-key diagnostic and startup.']])
    para('No training, fine-tuning or checkpoint replacement was performed for platform development. The separate Nature CFP pretraining asset is not substituted for the existing APTOS classifier. Prior review/reference admission code remains historical and inactive in the current API; Jev is the current admission mechanism. Proposed notebook, durable evaluation jobs, broader deployment and clinical validation are not reported as completed.')

    heading('3 Current system workflow')
    para('A browser or another application on the same computer sends one image to POST /api/predict. The backend enforces upload size, supported format, decoding, pixel and single-frame constraints. It prepares a separate image copy for Jev if its dimensions or format require conversion. The backend sends an authenticated HTTP request to OpenRouter. A valid Jev decision of 1 allows the original uploaded bytes to proceed to the shared RETFound predictor. The API returns the predicted grade, all five softmax scores, image hash, admission metadata, timing and model identity.')
    table(['Jev outcome', 'API behavior', 'RETFound action'], [
        ['0', 'HTTP 422; not_retinal_fundus; prediction is null; decision 0', 'Not invoked'],
        ['1', 'Successful prediction with accepted input status and decision 1', 'Run on original uploaded bytes'],
        ['Timeout or provider failure', 'HTTP 503; fundus_check_unavailable; no DR scores', 'Not invoked'],
        ['Malformed or non-binary answer', 'Service error; no DR prediction', 'Not invoked']])
    para('Fundus decision 0 and DR grade 0 have different meanings. Fundus decision 0 rejects an image that was not identified as a fundus photograph. DR grade 0 means the accepted retinal image was classified as No DR. A failed external request is a service failure and is not converted into a non-fundus classification.')
    para('The API is bound to loopback for use on this computer, with explicit browser origin and Host controls. One inference executor and three admitted slots bound work; a cancelled request retains its slot until its worker finishes. Uploads are handled in memory and are not saved as a server prediction history. The interface displays backend results rather than implementing its own model or metrics. Images sent to Jev leave the computer for OpenRouter and its provider; local memory handling is not a statement about external provider retention.')

    heading('4 RETFound inference contract')
    para('The architecture is models_vit.RETFound_mae with img_size 224, num_classes 5 and global_pool True. The loader resolves the explicit checkpoint first, then the supported local layouts. The actual baseline checkpoint is checkpoints/checkpoints/APTOS2019/checkpoint-best.pth. It is loaded on CPU using the compatible mmap and weights_only settings, validates the model configuration and loads checkpoint model weights strictly. Remote or uploaded checkpoint files are not accepted.')
    para('Preprocessing is unchanged: Pillow decode, RGB conversion, bicubic resize of the shorter edge to 256, center crop 224, tensor conversion, and ImageNet normalization with mean 0.485, 0.456, 0.406 and standard deviation 0.229, 0.224, 0.225. No EXIF rotation, retinal crop, enhancement, augmentation or replacement normalization is silently introduced. The shared predictor uses eval mode and torch.inference_mode, calls forward_features, flattens features per batch and applies model.head. It requires finite logits of shape batch by 5.')
    table(['Grade', 'Meaning'], [[i, label] for i,label in enumerate(['No DR','Mild','Moderate','Severe','Proliferative'])])
    para('The result is the argmax of five softmax scores. These are uncalibrated model scores, not validated clinical probabilities. The baseline uses float32. CUDA, CPU and MPS selection are supported by code; historical parity checks exercised CUDA and CPU, while MPS was not exercised. Shared modules do not load the model or allocate a GPU during import.')

    heading('5 Dataset audit and selection for the 1000 image evaluation')
    para('The evaluated source is the locally supplied APTOS2019 ZIP identified by its exact archive SHA-256. Its recognized folders supplied 2,048 train, 514 validation and 1,100 test images. The current audit recorded zero structure/read issues and identified 1,036 eligible test images. Sixty-four test paths were excluded. Overlapping reason counts include 56 cross-split matches, 12 conflicting-label records and four redundant same-label test copies; these counters cannot be added to infer the number excluded.')
    para('The older audit reporting 981 eligible images is a separate historical artifact. It is not the source of the completed 1,000-image run, and its discrepancy was not resolved by duplicating images or borrowing training data. The later run used a fresh audit of the available archive. Explicit numeric and documented named class folders are mapped to grades; labels are not assigned by incidental directory sorting.')
    para('Selection used uniform sampling without replacement from the 1,036 eligible test candidates, seed 20261023, with stable ordering and a persisted selection manifest. This is a uniform image sample, not a class-balanced demonstration. It contains 1,000 distinct exact-byte image hashes. Exact overlap checks cover the supplied train, validation and test splits. This does not establish patient independence, absence of near duplicates, or independence from the original checkpoint training data.')

    heading('6 Results of the saved 1000 image run')
    para('Run ID aptos1000-20261029 was saved on 29 October 2026 at 20:46:51 UTC, equivalent to 23:46:51 in Damascus. The recorded device was CUDA and dtype float32. Recorded elapsed time was 84.98 seconds from audit start through prediction and metric creation, excluding Python startup and final serialization. It is a single laptop measurement and contains no Jev request time.')
    table(['Metric', 'Result'], [
        ['Images / correct / incorrect', f'{n} / {correct} / {n-correct}'],
        ['Exact five-grade accuracy', '84.70%'], ['Five-label macro F1', f'{sum(f1)/5:.6f}'],
        ['Quadratic weighted kappa', f'{qwk:.6f}'], ['Any-DR accuracy', '98.30%'],
        ['Any-DR sensitivity', '98.9474%'], ['Any-DR specificity', '97.7143%'],
        ['True negatives / false positives', '513 / 12'], ['True positives / false negatives', '470 / 5']])
    para('Confusion matrix: rows are true grades and columns are predicted grades, in fixed order 0 through 4. Diagonal entries are correct severity predictions.')
    table(['True grade', 'Pred 0', 'Pred 1', 'Pred 2', 'Pred 3', 'Pred 4'], [[i,*row] for i,row in enumerate(cm)])
    table(['Grade', 'True count', 'Precision', 'Recall', 'F1'], [
        [i, truth[i], f'{cm[i][i]/predicted[i]:.2%}', f'{cm[i][i]/truth[i]:.2%}', f'{f1[i]:.4f}'] for i in range(5)])
    para('Per-grade precision, recall and F1 in this table were derived during report preparation from the saved confusion matrix; they are not a new inference run. Recall is 97.71% for grade 0, 41.86% for grade 1, 92.34% for grade 2, 35.19% for grade 3 and 51.35% for grade 4. The sample has 525 grade-0 images, so overall accuracy is strongly influenced by that class.')
    para('Important errors include 47 of 86 mild images predicted as moderate, 27 of 54 severe images predicted as moderate, and 21 of 74 proliferative images predicted as moderate. Binary any-DR accuracy hides these severity errors because predictions above grade 0 all count as DR. The five false negatives are labeled DR images predicted as No DR; the 12 false positives are labeled No DR images predicted as a DR grade. No referral policy or clinical operating threshold was validated.')
    para('Accuracy is correct divided by total. Macro F1 averages the five class F1 values with absent-class behavior retained from the legacy five-label definition. Quadratic kappa weights grade disagreement by squared severity distance. Any-DR metrics collapse grades 1 to 4 into positive and use argmax grade greater than zero, not a probability threshold. Undefined metrics in the shared evaluation contract are JSON null with reasons, not NaN or Infinity.')

    heading('7 Other historical evaluation evidence')
    table(['Saved dataset evaluation', 'Images', 'Correct', 'Accuracy'], [
        ['APTOS subset in mixed benchmark',34,31,'91.18%'], ['IDRiD transfer subset',33,14,'42.42%'],
        ['MESSIDOR2 transfer subset',33,20,'60.61%'], ['Combined mixed benchmark',100,65,'65.00%'],
        ['Separate historical IDRiD test',103,42,'40.78%']])
    para('These are historical saved results summarized in the progress record, not rerun for this report. IDRiD and MESSIDOR2 evaluate transfer of the APTOS classifier and must remain separate from APTOS within-dataset performance. Different source datasets, sample sizes and class mixtures prevent treating these figures as direct like-for-like comparisons or evidence of improvement over time.')

    heading('8 Jev implementation and troubleshooting')
    para('Jev is called through ordinary backend HTTP requests, without an OpenRouter workflow node or a new SDK dependency. The configured model ID is typesafe/jev-1.14 and the endpoint is https://openrouter.ai/api/alpha/decisions. Authentication uses Authorization Bearer with the server-held OpenRouter inference key. It remains an OpenRouter-routed request, rather than a direct TypeSafe-provider request. The choice question asks for one of the predefined strings 0 and 1, then the backend strictly validates and converts that value into its binary contract.')
    para('Choice 1 describes an identifiable retinal fundus photograph showing the interior retinal surface and anatomy. Choice 0 covers unrelated scenes, external eye photographs, OCT images, diagrams and images not identifiable as fundus photographs. Instructions tell Jev to judge visual content and ignore instructions written in the image. These criteria define the requested behavior; they do not prove detection accuracy or resistance to misleading inputs.')
    para('Jev requires a separate supported image representation. The sample file is 4288 by 2848 pixels, beyond the documented maximum of 1568 per side. Screening copies are resized within 256 to 1568 pixels per side and at least 78,400 total pixels, with extreme aspect ratios rejected. Supported compatible PNG/JPEG bytes can be retained; otherwise RGB JPEG is generated for Jev only. RETFound receives the original payload through its unchanged preprocessing. Changes to this screening copy have not been evaluated for their effect on Jev accuracy.')
    para('Integration exposed HTTP 400 and timeout failures. Early messages were too generic and did not establish a cause. The client now distinguishes authentication, credits, permissions, request/model errors, rate limits, network/TLS failures, timeouts and malformed responses. It uses a 90-second socket timeout, configurable from 1 to 90 seconds, bounded response reads and disabled redirects. It does not automatically retry paid model requests. Sanitized validation details and response-type diagnostics exclude the key and encoded image blobs.')
    para('The diagnostic now validates expected key syntax locally and calls GET https://openrouter.ai/api/v1/key before any model request. This checks authentication without invoking Jev and rejects management/provisioning keys. It then tests a text fixture and the sample image separately. A hidden fresh-key prompt avoids reusing a stale terminal value. The optional startup step passes the tested key to the child server environment without saving it or putting it in process arguments.')
    para('The user subsequently reported successful operation. We do not have a retained successful authenticated trace, measured Jev latency, confusion matrix or confirmed root cause for the earlier empty HTTP 400. Successful startup confirms an operational workflow as reported by the user; it does not validate fundus screening sensitivity, specificity or the combined system on 1,000 images.')

    heading('9 Verification and evidence boundaries')
    table(['Evidence', 'What it supports', 'Boundary'], [
        ['Saved 1000-image predictions and completion marker', 'Completed RETFound evaluation and recorded metrics', 'Predates Jev; no fresh inference for this report'],
        ['Fresh report consistency checks', 'Record count, score consistency, selection order and recomputed metrics', 'Does not revalidate original diagnoses or rerun the checkpoint'],
        ['Historical inference parity', '34 APTOS images matched saved scores exactly; one CPU/CUDA delta about 1.79e-7', 'Recorded development evidence; MPS untested'],
        ['Historical API/UI verification', 'Real CUDA HTTP parity, raw/multipart behavior, concurrency and asset MIME checks', 'Earlier direct-input workflow, before Jev'],
        ['18 gate and diagnostic tests', 'Binary parsing, blocked inference paths, key handling, errors, dimensions and startup handoff', 'Mock provider responses; not a Jev accuracy study'],
        ['User confirmation on 30 October', 'Jev workflow reported to work after startup changes', 'No retained authenticated transcript or quantified accuracy']])
    para('Earlier development records include successful full-suite runs of 46 Python tests and UI contract checks at that stage. A later combined gate/API run stalled after gate tests and was interrupted; it must not be represented as a completed current full-suite pass. The most recent gate/diagnostic suite had 18 passing tests. Browser contract tests use stubs and do not replace visual testing in a real browser. This report does not invent an updated aggregate test count.')

    heading('10 Startup and demonstration procedure')
    para('Use the existing ml-homework interpreter. From the project directory, stop an old server with Ctrl+C before launching so that the launcher does not reuse stale configuration. Run the command below, paste the raw key at the hidden prompt and keep the terminal open. The text and image requests may be billed by OpenRouter.')
    code('& "$env:USERPROFILE\\.conda\\envs\\ml-homework\\python.exe" -B scripts/diagnose_jev.py --new-key --start-server')
    para('After successful checks the server opens http://127.0.0.1:8000. Select a fundus image, run analysis and inspect all five scores. Use a non-fundus image to demonstrate rejection only as an actual live observation, not as a guaranteed model outcome. Verify that rejection or service failure clears earlier results and does not show a disease grade. Review the saved evaluation in the interface or the offline results/runs/aptos1000-20261029/index.html viewer. Download JSON only for the intended case.')
    para('The original evaluation command is recorded below for reproducibility. It was executed for the saved run, not again during report preparation. If rerunning is separately authorized, choose a new output directory and confirm the explicit dataset source. Do not overwrite historical evidence or interpret an existing report as a new run.')
    code('& "$env:USERPROFILE\\.conda\\envs\\ml-homework\\python.exe" -B scripts/evaluate_aptos.py APTOS2019.zip --count 1000 --device cuda --output results/runs/NEW_RUN_ID')

    heading('11 Limitations and proposed next work')
    para('The deliverable is a research demonstration, not a clinically validated screening service. Ground truth comes from the supplied folder labels. Patient identities, near-duplicate methods and checkpoint-matched training split provenance were unavailable, so those independence claims remain unverified. Exact-byte exclusions address only the overlaps detectable by that method. Scores are uncalibrated and no confidence intervals or prospective clinical study were produced.')
    para('Jev introduces external connectivity, provider availability, billing and data-handling dependencies. Its binary output can be wrong. Neither modality screening nor image-quality acceptance has been validated on a labeled positive-and-negative corpus. The original 1,000 retinal images cannot by themselves quantify specificity against non-fundus uploads. A real fundus image falsely rejected by Jev never reaches RETFound, so combined-system performance requires separate measurement.')
    para('Proposed next work is to assemble an explicitly labeled fundus/non-fundus and poor-quality set, record Jev outcomes and provider/model versions, measure false acceptance, false rejection, failures and latency, then evaluate the combined pipeline. Include genuine fundus, external-eye photos, OCT, scans, diagrams and unrelated photographs. Preserve all exclusions and failure accounting rather than reporting only accepted cases. These are proposals, not completed experiments or authorization to run a paid 1,000-image Jev batch.')
    para('Other pending work includes a validated complete dependency specification, fuller browser visual verification, source-control ownership repair as a separate authorized task, and any requested notebook, deployment or bilingual preparation. The parent Git repository records this folder as a gitlink while the folder lacks its own Git metadata; normal parent status is not proof that these source edits are tracked.')

    heading('12 Provenance and source register')
    table(['Recorded runtime component', 'Value'], [[k,v] for k,v in p['packages'].items()] + [['Python',p['python']],['Device / dtype',p['device']+' / '+p['dtype']],['GPU in inspection record','NVIDIA GeForce RTX 3070 Laptop GPU']])
    para('Checkpoint SHA-256: ' + p['checkpoint_sha256'])
    para('Dataset archive SHA-256: ' + p['source_identity']['archive_sha256'])
    para('Audit ID: ' + p['audit_id'])
    para('Selection ID: ' + p['selection_id'])
    para('Preprocessing version: ' + p['preprocessing_version'] + '. Evaluation schema: ' + p['schema_version'] + '. Jev admission policy: jev-fundus-choice-v1.')
    for path, purpose in [
        ('results/runs/aptos1000-20261029/predictions.json','Authoritative saved per-image scores, provenance and metrics'),
        ('results/runs/aptos1000-20261029/audit.json','Split validation, duplicate and exclusion evidence'),
        ('results/runs/aptos1000-20261029/selection.json','Ordered seeded sample manifest'),
        ('results/runs/aptos1000-20261029/completed.json','Completion marker'),
        ('docs/PROGRESS.md','Dated implementation and verification record'),
        ('docs/IMPLEMENTATION_PLAN.md','Authorized scope and remaining proposals'),
        ('docs/API.md','Local API contracts, startup and troubleshooting'),
        ('retfound_platform/inference/fundus_gate.py','Current Jev request and rejection behavior'),
        ('retfound_platform/inference/predictor.py','Current RETFound forward path'),
        ('retfound_platform/evaluation/metrics.py','Metric definitions'),
    ]:
        para(path + ' — ' + purpose + '.')
    para('External API references used during implementation: https://openrouter.ai/docs/guides/community/multimodal-decisions ; https://openrouter.ai/docs/api/api-reference/alphadecisions/submit-a-decisions-request ; https://openrouter.ai/docs/api/api-reference/api-keys/get-current-key . The local source describes the implemented contract; provider capabilities and limits can change.')
    para('Reader guidance: use the run artifacts for detailed numerical evidence, the source code for current behavior and the progress log for the chronology. Later dated changes supersede older descriptions. User confirmation is explicitly attributed. No performance figure from RETFound is attributed to Jev.')

    css = '''body{font:16px/1.6 Segoe UI,Arial,sans-serif;color:#17232c;background:#edf1f4;margin:0}main{max-width:980px;margin:30px auto;padding:55px 65px;background:white}h1{font-size:34px;line-height:1.2;color:#000;margin:0 0 22px}h2{font-size:23px;line-height:1.3;color:#000;margin-top:38px;break-after:avoid}p{margin:13px 0;overflow-wrap:anywhere}table{width:100%;border-collapse:collapse;margin:20px 0;font-size:14px;break-inside:auto}th,td{border:1px solid #d9d9d9;padding:10px 12px;text-align:left;vertical-align:middle}th{background:#173b50;color:white}tr:nth-child(even){background:#f4f7f9}tr{break-inside:avoid}thead{display:table-header-group}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:13px/1.6 Consolas,monospace;padding:15px;background:#f2f5f7}footer{margin-top:35px;border-top:1px solid #ddd;padding-top:15px;font-size:13px;color:#50616f}@page{size:A4;margin:18mm}@media print{body{background:white;font-size:10.5pt;line-height:1.45}main{margin:0;padding:0;max-width:none}h1{font-size:25pt}h2{font-size:16pt;margin-top:20pt}table{font-size:9pt}th,td{padding:6px 8px}pre{font-size:9pt}th{background:#e6edf2;color:black}}'''
    (OUT / 'RETFound_Jev_Technical_Report.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>RETFound and Jev technical report</title><style>'+css+'</style><main>'+''.join(body)+'<footer>Prepared 30 October 2026 · Research demonstration · Evidence source and limits stated within the report</footer></main></html>', encoding='utf-8')
    (OUT / 'RETFound_Jev_Technical_Report.md').write_text('\n'.join(md), encoding='utf-8')
    (OUT / 'report_verification.json').write_text(json.dumps({'report_date':'2026-10-30','inference_rerun':False,'checks':checks,'source_hashes':{name:hashlib.sha256((RUN/name).read_bytes()).hexdigest() for name in ['predictions.json','selection.json','audit.json','completed.json']}},indent=2), encoding='utf-8')
    print(json.dumps({'output':str(OUT),'checks':checks,'sections':12,'records':n},indent=2))


if __name__ == '__main__':
    main()
