const $ = id => document.getElementById(id);
const labels = ['No DR', 'Mild DR', 'Moderate DR', 'Severe DR', 'Proliferative DR'];
const pageNames = {analysis: 'Image analysis', evaluation: 'Model evaluation', integration: 'API integration', about: 'About the model'};
let selectedFile = null;
let previewUrl = null;
let prediction = null;
let ready = false;
let busy = false;
let sampleLoading = false;
let evaluationLoaded = false;
let language = 'curl';
const limit = 20 * 1024 * 1024;

function make(tag, className, text) {
  const element = document.createElement(tag);
  if (className) element.className = className;
  if (text !== undefined) element.textContent = text;
  return element;
}

function updateControls() {
  $('analyze').disabled = !selectedFile || !ready || busy || sampleLoading;
  $('analyze-label').textContent = busy ? 'Analyzing image…' : !ready ? 'Waiting for model' : 'Analyze image';
  $('use-example').disabled = busy || sampleLoading;
  $('remove-image').disabled = busy || sampleLoading;
  $('file-input').disabled = busy || sampleLoading;
  $('dropzone').setAttribute('aria-disabled', String(busy || sampleLoading));
}

function showError(message) {
  $('upload-error').textContent = message;
  $('upload-error').hidden = !message;
}

function stage(number) {
  ['upload', 'analyze', 'results'].forEach((name, index) => {
    const element = $(`step-${name}`);
    element.classList.toggle('current', index === number);
    element.classList.toggle('done', index < number);
  });
}

function resetResult() {
  prediction = null;
  $('result-empty').hidden = false;
  $('result-loading').hidden = true;
  $('result-content').hidden = true;
  $('score-bars').replaceChildren();
  $('prediction-label').textContent = '';
  $('prediction-grade').textContent = '';
  $('top-score').textContent = '';
  $('result-panel').setAttribute('aria-busy', 'false');
}

function selectFile(file) {
  if (busy || sampleLoading || !file) return;
  if (!file.size) { showError('This file is empty. Choose a retinal image.'); return; }
  if (file.size > limit) { showError('This image is larger than 20 MB. Choose a smaller image.'); return; }
  if (!/\.(jpe?g|png|tiff?|bmp|webp)$/i.test(file.name) && !['image/jpeg', 'image/png', 'image/tiff', 'image/bmp', 'image/webp'].includes(file.type)) {
    showError('Choose a JPEG, PNG, TIFF, BMP or WebP image.'); return;
  }
  if (previewUrl) URL.revokeObjectURL(previewUrl);
  selectedFile = file;
  resetResult();
  showError('');
  $('dropzone').hidden = true;
  $('preview').hidden = false;
  $('preview-image').hidden = false;
  $('preview-fallback').hidden = true;
  $('filename').textContent = file.name;
  $('filename').title = file.name;
  $('filesize').textContent = file.size < 1024 * 1024 ? `${(file.size / 1024).toFixed(1)} KB` : `${(file.size / 1024 / 1024).toFixed(2)} MB`;
  previewUrl = URL.createObjectURL(file);
  $('preview-image').src = previewUrl;
  stage(1);
  updateControls();
}

$('preview-image').addEventListener('error', () => {
  $('preview-image').hidden = true;
  $('preview-fallback').hidden = false;
});
$('file-input').addEventListener('change', event => {
  selectFile(event.target.files[0]);
  event.target.value = '';
});
function browse() { if (!busy && !sampleLoading) $('file-input').click(); }
$('dropzone').addEventListener('click', browse);
$('dropzone').addEventListener('keydown', event => {
  if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); browse(); }
});
for (const name of ['dragenter', 'dragover']) $('dropzone').addEventListener(name, event => {
  event.preventDefault(); if (!busy && !sampleLoading) $('dropzone').classList.add('dragover');
});
for (const name of ['dragleave', 'drop']) $('dropzone').addEventListener(name, event => {
  event.preventDefault(); $('dropzone').classList.remove('dragover');
});
$('dropzone').addEventListener('drop', event => {
  if (event.dataTransfer.files.length !== 1) { showError('Choose one image at a time.'); return; }
  selectFile(event.dataTransfer.files[0]);
});
$('remove-image').addEventListener('click', () => {
  if (busy || sampleLoading) return;
  selectedFile = null;
  if (previewUrl) URL.revokeObjectURL(previewUrl);
  previewUrl = null;
  $('preview-image').removeAttribute('src');
  $('preview').hidden = true;
  $('dropzone').hidden = false;
  resetResult(); showError(''); stage(0); updateControls();
  $('dropzone').focus();
});

$('use-example').addEventListener('click', async () => {
  if (busy || sampleLoading) return;
  sampleLoading = true; updateControls(); showError('');
  try {
    const response = await fetch('/api/example');
    if (!response.ok) throw new Error('The sample image is unavailable. Please upload your own image.');
    const blob = await response.blob();
    sampleLoading = false;
    selectFile(new File([blob], 'idrid_test.jpg', {type: 'image/jpeg'}));
  } catch (error) { showError(error.message || 'The sample could not be loaded.'); }
  finally { sampleLoading = false; updateControls(); }
});

function validPrediction(result) {
  return result.schema_version === 'retfound-prediction/1' && Number.isInteger(result.predicted_grade)
    && result.input_validation?.status === 'accepted'
    && result.predicted_grade >= 0 && result.predicted_grade <= 4
    && Array.isArray(result.scores) && result.scores.length === 5
    && result.scores.every(value => Number.isFinite(value) && value >= 0 && value <= 1)
    && typeof result.model?.device === 'string' && Number.isFinite(result.elapsed_ms);
}

function renderPrediction(result) {
  $('input-note').textContent = 'Jev accepted the retinal fundus image; automated screening can be wrong';
  $('prediction-label').textContent = result.predicted_label;
  $('prediction-grade').textContent = `Grade ${result.predicted_grade} of 4`;
  $('top-score').textContent = `${(result.top_score * 100).toFixed(1)}%`;
  $('score-bars').replaceChildren(...result.scores.map((score, index) => {
    const row = make('div', `score-row${index === result.predicted_grade ? ' winner' : ''}`);
    const heading = make('div', 'score-label');
    const name = make('span', 'score-name');
    name.append(make('span', 'grade-number', index), document.createTextNode(result.model.grades[index]));
    heading.append(name, make('span', '', `${(score * 100).toFixed(1)}%`));
    const track = make('div', 'score-track');
    const progress = make('progress');
    progress.max = 1; progress.value = score;
    progress.setAttribute('aria-label', `${result.model.grades[index]} model score`);
    track.append(progress); row.append(heading, track); return row;
  }));
  $('inference-time').textContent = `${(result.elapsed_ms / 1000).toFixed(2)} s · request ${result.request_id.slice(0, 8)}`;
  $('result-device').textContent = `${result.model.device.toUpperCase()} · ${result.model.dtype}`;
  $('result-empty').hidden = true;
  $('result-loading').hidden = true;
  $('result-content').hidden = false;
  stage(2);
}

$('analyze').addEventListener('click', async () => {
  if (!selectedFile || !ready || busy) return;
  busy = true; resetResult(); updateControls(); showError('');
  $('result-empty').hidden = true;
  $('result-content').hidden = true;
  $('result-loading').hidden = false;
  $('scan-line').hidden = false;
  $('result-panel').setAttribute('aria-busy', 'true');
  stage(1);
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 120000);
  try {
    const form = new FormData(); form.append('image', selectedFile);
    const response = await fetch('/api/predict', {method: 'POST', body: form, signal: controller.signal});
    const result = await response.json();
    if (!response.ok) throw new Error(result.error?.message || `The request failed (HTTP ${response.status}).`);
    if (!validPrediction(result)) throw new Error('The server returned an unexpected result. Please try again.');
    prediction = result;
    renderPrediction(result);
  } catch (error) {
    resetResult();
    showError(error.name === 'AbortError' ? 'The request took too long. The server may still be finishing it; try again shortly.' : error.message === 'Failed to fetch' ? 'The server could not be reached. Keep run_web.bat open and try again.' : error.message);
  } finally {
    clearTimeout(timeout); busy = false;
    $('scan-line').hidden = true;
    $('result-panel').setAttribute('aria-busy', 'false'); updateControls();
  }
});

$('download-result').addEventListener('click', () => {
  if (!prediction) return;
  const url = URL.createObjectURL(new Blob([JSON.stringify(prediction, null, 2)], {type: 'application/json'}));
  const anchor = document.createElement('a'); anchor.href = url;
  anchor.download = `retfound-${prediction.request_id.slice(0, 8)}.json`;
  anchor.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
});

function renderModel(model) {
  const rows = [
    ['Architecture', model.architecture], ['Classifier', 'APTOS2019 · 5 grades'],
    ['Device', `${model.device.toUpperCase()} · ${model.dtype}`],
    ['Grade order', model.grades.map((grade, index) => `${index} ${grade}`).join(' / ')],
    ['Preprocessing', 'RGB → bicubic shorter-edge resize 256 → center crop 224 → ImageNet normalization'],
    ['Version', model.preprocessing_version], ['Checkpoint SHA-256', model.checkpoint_sha256],
    ['Input handling', 'Direct inference after decoding. Automatic retina detection is not implemented.'],
  ];
  $('model-details').replaceChildren(...rows.flatMap(([key, value]) => [make('dt', '', key), make('dd', '', value)]));
}

async function checkConnection() {
  try {
    const response = await fetch('/api/health', {signal: AbortSignal.timeout(5000)});
    const health = await response.json();
    ready = response.ok && health.status === 'ready';
    const device = $('connection').dataset.device;
    $('connection-text').textContent = ready ? `Model ready${device ? ` · ${device}` : ''}` : 'Model loading';
    $('connection').querySelector('.status-dot').className = `status-dot${ready ? '' : ' waiting'}`;
    if (ready && !$('model-details').dataset.loaded) {
      const modelResponse = await fetch('/api/model');
      if (modelResponse.ok) {
        const model = await modelResponse.json(); renderModel(model);
        $('model-details').dataset.loaded = 'true';
        $('connection').dataset.device = model.device.toUpperCase();
        $('connection-text').textContent = `Model ready · ${model.device.toUpperCase()}`;
      }
    }
  } catch {
    ready = false;
    delete $('model-details').dataset.loaded;
    $('connection-text').textContent = 'Server offline';
    $('connection').querySelector('.status-dot').className = 'status-dot offline';
  }
  updateControls();
}

async function loadEvaluation() {
  if (evaluationLoaded) return;
  try {
    const response = await fetch('/api/evaluation');
    if (!response.ok) throw new Error('The saved evaluation is not available on this server.');
    const report = await response.json(); const m = report.metrics;
    const percent = value => Number.isFinite(value) ? `${(100 * value).toFixed(2)}%` : 'N/A';
    const binary = m.binary;
    const rows = [['Images evaluated', m.n.toLocaleString(), 'Seeded APTOS test selection'],
      ['Exact grade accuracy', `${(100 * m.accuracy).toFixed(1)}%`, `${m.correct} correct predictions`],
      ['Macro F1', m.macro_f1.toFixed(3), 'Fixed five-grade average'],
      ['Quadratic kappa', m.quadratic_kappa.toFixed(3), 'Weighted grade agreement'],
      ['Any-DR sensitivity', percent(binary.sensitivity), 'Proportion of reference DR cases detected'],
      ['Any-DR specificity', percent(binary.specificity), 'Proportion of reference No DR cases correctly excluded']];
    $('evaluation-metrics').replaceChildren(...rows.map(([label, value, hint]) => {
      const card = make('div', 'metric-card'); card.append(make('span', '', label), make('strong', '', value), make('small', '', hint)); return card;
    }));
    $('sensitivity-detail').textContent = binary.sensitivity == null
      ? `Sensitivity: N/A. ${m.undefined_reasons?.sensitivity || 'No positive reference images.'}`
      : `Sensitivity = TP / (TP + FN): ${binary.tp} / (${binary.tp} + ${binary.fn}) = ${percent(binary.sensitivity)}. Detects DR among reference DR cases.`;
    $('specificity-detail').textContent = binary.specificity == null
      ? `Specificity: N/A. ${m.undefined_reasons?.specificity || 'No negative reference images.'}`
      : `Specificity = TN / (TN + FP): ${binary.tn} / (${binary.tn} + ${binary.fp}) = ${percent(binary.specificity)}. Correctly excludes DR among reference No DR cases.`;
    $('binary-counts').textContent = `True positives (DR detected): ${binary.tp}. False negatives (DR missed): ${binary.fn}. True negatives (No DR correctly classified): ${binary.tn}. False positives (false alarms): ${binary.fp}.`;
    const thead = make('thead'), header = make('tr');
    header.append(make('th', '', 'True / Pred'));
    labels.forEach((label, index) => { const th = make('th', '', index); th.title = label; header.append(th); });
    thead.append(header);
    const tbody = make('tbody');
    m.confusion.forEach((values, index) => {
      const row = make('tr'); const th = make('th', '', index); th.title = labels[index]; row.append(th);
      values.forEach((value, column) => row.append(make('td', index === column ? 'diagonal' : '', value)));
      tbody.append(row);
    });
    $('confusion').append(thead, tbody);
    $('evaluation-run').textContent = `Run ${report.run_id} · ${new Date(report.created_utc).toLocaleDateString()}`;
    $('evaluation-status').hidden = true; $('evaluation-content').hidden = false;
    evaluationLoaded = true;
  } catch (error) { $('evaluation-status').textContent = error.message; }
}

function codeExample() {
  const endpoint = `${location.origin}/api/predict`;
  const examples = {
    curl: `curl.exe -X POST "${endpoint}" -F "image=@C:/images/retina.jpg"`,
    python: `import requests\n\nwith open("retina.jpg", "rb") as image:\n    response = requests.post(\n        "${endpoint}",\n        files={"image": image},\n        timeout=120,\n    )\nresponse.raise_for_status()\nresult = response.json()\nprint(result["predicted_label"])\nprint(result["scores"])`,
    javascript: `const form = new FormData();\nform.append("image", fileInput.files[0]);\n\nconst response = await fetch(\n  "${endpoint}",\n  { method: "POST", body: form }\n);\nconst result = await response.json();\nif (!response.ok) {\n  throw new Error(result.error.message);\n}\nconsole.log(result.predicted_label);`,
  };
  return examples[language];
}
function renderCode() {
  $('request-code').textContent = codeExample();
  $('api-base').textContent = location.origin;
  document.querySelectorAll('[data-language]').forEach(button => button.setAttribute('aria-selected', String(button.dataset.language === language)));
}
document.querySelectorAll('[data-language]').forEach(button => button.addEventListener('click', () => {
  language = button.dataset.language; renderCode();
}));
$('copy-code').addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText(codeExample());
    $('copy-code').querySelector('span').textContent = 'Copied';
  } catch { $('copy-code').querySelector('span').textContent = 'Select text to copy'; }
  setTimeout(() => { $('copy-code').querySelector('span').textContent = 'Copy'; }, 2000);
});

function navigate() {
  const page = location.hash.slice(1) in pageNames ? location.hash.slice(1) : 'analysis';
  Object.keys(pageNames).forEach(name => { $(`page-${name}`).hidden = name !== page; });
  document.querySelectorAll('[data-page]').forEach(link => {
    link.classList.toggle('active', link.dataset.page === page);
    if (link.dataset.page === page) link.setAttribute('aria-current', 'page');
    else link.removeAttribute('aria-current');
  });
  $('breadcrumb').textContent = pageNames[page];
  document.title = `RETFound · ${pageNames[page]}`;
  if (page === 'evaluation') loadEvaluation();
}
window.addEventListener('hashchange', navigate);
window.addEventListener('beforeunload', () => { if (previewUrl) URL.revokeObjectURL(previewUrl); });
renderCode(); navigate(); checkConnection();
setInterval(checkConnection, 15000);
