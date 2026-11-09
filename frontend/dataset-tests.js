const byId = id => document.getElementById(id);
const states = new Map();
let samples = [], running = false, stopping = false, uncertain = false;
const views = new Map();
function node(tag, text = '', className = '') {
  const item = document.createElement(tag); item.textContent = text; item.className = className; return item;
}
function controls() {
  byId('run-all').disabled = running || uncertain || samples.length !== 15;
  byId('stop').disabled = !running || stopping;
  byId('download').disabled = running || states.size === 0;
  for (const view of views.values()) view.button.disabled = running || uncertain;
}
function clearResult(sample) {
  states.delete(sample.id);
  const view = views.get(sample.id); view.result.textContent = 'Not tested'; view.result.dataset.state = ''; view.scores.textContent = '';
}
async function testOne(sample) {
  clearResult(sample);
  const view = views.get(sample.id); view.result.textContent = 'Checking with Jev, then RETFound…';
  const controller = new AbortController(), timer = setTimeout(() => controller.abort(), 180000);
  try {
    const response = await fetch(`/api/demo/${sample.id}/predict`, {method: 'POST', signal: controller.signal});
    const result = await response.json();
    if (!response.ok) {
      const status = result.error?.code === 'not_retinal_fundus' ? 'rejected' : 'error';
      states.set(sample.id, {sample_id: sample.id, reference: sample, status, http_status: response.status, response: result});
      view.result.dataset.state = status;
      view.result.textContent = `${status === 'rejected' ? 'Rejected by Jev — no DR prediction' : 'Test failed'}\n${result.error?.message || 'Request failed'}`;
      // Stop a batch on service failure rather than repeating paid failing requests.
      if (response.status >= 500 || response.status === 429) stopping = true;
      return;
    }
    const prediction = result.prediction;
    if (result.schema_version !== 'retfound-demo-result/1' || result.reference?.id !== sample.id ||
        prediction?.image_sha256 !== sample.sha256 || prediction.input_validation?.decision !== 1 ||
        !Number.isInteger(prediction.predicted_grade) || typeof result.matches_true_grade !== 'boolean' ||
        !Array.isArray(prediction.scores) || prediction.scores.length !== 5) throw new Error('Invalid server result');
    states.set(sample.id, {sample_id: sample.id, status: 'predicted', response: result});
    view.result.dataset.state = result.matches_true_grade ? 'match' : 'mismatch';
    view.result.textContent = `Jev: accepted (1)\nPredicted: ${prediction.predicted_grade} ${prediction.predicted_label}\n${result.matches_true_grade ? 'Matches reference grade' : 'Does not match reference grade'}`;
    view.scores.textContent = prediction.scores.map((score, grade) => `Grade ${grade}: ${(score * 100).toFixed(2)}%`).join('\n') + '\nUncalibrated model scores';
    if (prediction.timing_ms) view.scores.textContent += `\nJev: ${(prediction.timing_ms.jev / 1000).toFixed(1)}s · RETFound: ${(prediction.timing_ms.retfound / 1000).toFixed(1)}s · Server total: ${(prediction.elapsed_ms / 1000).toFixed(1)}s`;
  } catch (error) {
    // A disconnected client cannot know whether the server finished. No automatic retry.
    uncertain = true; stopping = true;
    const message = error.name === 'AbortError' ? 'Request timed out; the server may still be working.' : error.message;
    states.set(sample.id, {sample_id: sample.id, reference: sample, status: 'unknown', error: message});
    view.result.dataset.state = 'error'; view.result.textContent = `${message}\nOutcome unknown. Check server status before reloading and retrying.`;
  } finally { clearTimeout(timer); }
}
async function run(selected, reset = false) {
  if (running || uncertain) return;
  running = true; stopping = false;
  if (reset) { for (const sample of samples) clearResult(sample); }
  controls(); let processed = 0;
  for (const sample of selected) {
    if (stopping) break;
    byId('status').textContent = `Testing ${sample.dataset}, reference grade ${sample.true_grade} (${processed + 1} of ${selected.length})…`;
    await testOne(sample); processed++;
  }
  running = false;
  byId('status').textContent = uncertain ? 'Stopped: request outcome is unknown. Check the server before retrying.' :
    `${stopping ? 'Stopped' : 'Finished'}: ${processed} requested image(s) processed. Review each result; untested images have no prediction.`;
  controls();
}
byId('run-all').addEventListener('click', () => run(samples, true));
byId('stop').addEventListener('click', () => { stopping = true; controls(); byId('status').textContent = 'Stopping after the current request finishes…'; });
byId('download').addEventListener('click', () => {
  const data = {schema_version: 'retfound-demo-session/1', downloaded_utc: new Date().toISOString(),
    description: 'Balanced demonstration, not a representative evaluation. No aggregate accuracy is computed.',
    results: samples.map(sample => states.get(sample.id) || {sample_id: sample.id, reference: sample, status: 'not_tested'})};
  const url = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'}));
  const link = node('a'); link.href = url; link.download = 'retfound-dataset-tests.json'; link.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
});
async function load() {
  try {
    const response = await fetch('/api/demo'); const data = await response.json();
    if (!response.ok) throw new Error(data.error?.message || 'Demo samples unavailable');
    if (!Array.isArray(data.samples) || data.samples.length !== 15) throw new Error('Unexpected sample catalog');
    samples = data.samples;
    for (const dataset of ['IDRID', 'MESSIDOR2', 'DDR']) {
      byId('samples').append(node('h2', dataset)); const grid = node('div', '', 'grid'); byId('samples').append(grid);
      for (const sample of samples.filter(item => item.dataset === dataset)) {
        const card = node('article', '', 'sample'), image = node('img'); fetch(sample.thumbnail_url || sample.image_url).then(r => { if (!r.ok) throw new Error('Preview unavailable'); return r.blob(); }).then(blob => { image.src = URL.createObjectURL(blob); }).catch(() => { image.alt = 'Preview unavailable'; }); image.alt = `${dataset} test image`; image.loading = 'lazy';
        const button = node('button', 'Test this image'), result = node('p', 'Not tested', 'result'), scores = node('div', '', 'scores');
        button.addEventListener('click', () => run([sample]));
        card.append(image, node('h3', `Reference grade ${sample.true_grade} — ${sample.true_label}`), button, result, scores); grid.append(card); views.set(sample.id, {button, result, scores});
      }
    }
    byId('status').textContent = 'Ready. No tests have been run. Choose an image or test all 15.';
  } catch (error) { byId('status').textContent = error.message; }
  controls();
}
load();
