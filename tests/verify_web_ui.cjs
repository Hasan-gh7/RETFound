/* App interaction contract tests in a minimal DOM. This does not test browser rendering. */
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const {File} = require('node:buffer');
class Element {
  constructor(tag = 'div') { this.tagName = tag; this.children = []; this.dataset = {}; this.events = {}; this.attributes = {}; this.hidden = false; this.className = ''; this.textContent = ''; this.value = ''; this.innerHTML = ''; this.selectors = new Map(); }
  get classList() { const self = this; return {
    add(name) { self.className = [...new Set([...self.className.split(' '), name])].join(' ').trim(); },
    remove(name) { self.className = self.className.split(' ').filter(v => v !== name).join(' '); },
    toggle(name, active) { if (active) this.add(name); else this.remove(name); },
  }; }
  setAttribute(key, value) { this.attributes[key] = value; }
  removeAttribute(key) { delete this.attributes[key]; }
  addEventListener(name, callback) { (this.events[name] ||= []).push(callback); }
  append(...children) { this.children.push(...children); }
  replaceChildren(...children) { this.children = children; }
  querySelector(selector) { if (!this.selectors.has(selector)) this.selectors.set(selector, new Element()); return this.selectors.get(selector); }
  focus() { this.focused = true; }
  click() { this.clicked = true; }
  async emit(name, event = {}) { for (const callback of this.events[name] || []) await callback(event); }
}
async function main() {
  const html = fs.readFileSync('frontend/index.html', 'utf8');
  const elements = new Map();
  for (const match of html.matchAll(/<([a-z0-9]+)\b[^>]*\bid="([^"]+)"[^>]*>/g)) {
    const element = new Element(match[1]); element.hidden = /\bhidden\b/.test(match[0]); elements.set(match[2], element);
  }
  const nav = [...html.matchAll(/data-page="([^"]+)"/g)].map(m => { const e = new Element('a'); e.dataset.page = m[1]; return e; });
  const languages = [...html.matchAll(/data-language="([^"]+)"/g)].map(m => { const e = new Element('button'); e.dataset.language = m[1]; return e; });
  const recorded = JSON.parse(fs.readFileSync('results/runs/web-api-20261029/verification.json', 'utf8'));
  // Adapt the historical response explicitly to the current direct-input contract.
  recorded.real_prediction.input_validation = {status: 'accepted', decision: 1};
  const saved = JSON.parse(fs.readFileSync('results/runs/aptos1000-20261029/predictions.json', 'utf8'));
  const uploads = [], blobs = [], anchors = [], requests = [];
  let nextResponse = null, offline = false, copied = '';
  const win = new Element();
  const location = {hash: '', origin: 'http://127.0.0.1:8000'};
  const context = vm.createContext({console, Blob, File, FormData, AbortController,
    AbortSignal: {timeout: () => undefined}, location, window: win,
    URL: {createObjectURL(blob) { blobs.push(blob); return 'blob:fixture'; }, revokeObjectURL() {}},
    navigator: {clipboard: {async writeText(text) { copied = text; }}},
    document: {getElementById: id => { assert.ok(elements.has(id), `Missing element ${id}`); return elements.get(id); },
      createElement(tag) { const e = new Element(tag); if (tag === 'a') anchors.push(e); return e; },
      createTextNode: text => ({textContent: text}),
      querySelectorAll: selector => selector === '[data-page]' ? nav : languages},
    setTimeout: () => 1, clearTimeout() {}, setInterval() {},
    async fetch(path, options) {
      requests.push(path);
      if (offline) throw new Error('Failed to fetch');
      if (path === '/api/health') return {ok: true, json: async () => ({status: 'ready'})};
      if (path === '/api/model') return {ok: true, json: async () => recorded.model};
      if (path === '/api/example') return {ok: true, blob: async () => new Blob([fs.readFileSync('sample_images/idrid_test.jpg')], {type: 'image/jpeg'})};
      if (path === '/api/evaluation') return {ok: true, json: async () => ({run_id: saved.run_id, created_utc: saved.created_utc, metrics: saved.metrics.All})};
      if (path === '/api/predict') {
        assert.equal(options.method, 'POST'); uploads.push(options.body.get('image'));
        if (nextResponse) return nextResponse;
        return {ok: true, json: async () => recorded.real_prediction};
      }
      throw new Error(`Unexpected request ${path}`);
    },
  });
  vm.runInContext(fs.readFileSync('frontend/app.js', 'utf8'), context);
  await new Promise(resolve => setImmediate(resolve));
  const $ = id => elements.get(id);
  assert.equal($('analyze').disabled, true);
  await $('use-example').emit('click');
  assert.equal($('preview').hidden, false);
  assert.equal($('filename').textContent, 'idrid_test.jpg');
  assert.equal($('analyze').disabled, false);
  await $('analyze').emit('click');
  assert.equal(uploads.length, 1);
  assert.equal(uploads[0].name, 'idrid_test.jpg');
  assert.equal($('result-content').hidden, false);
  assert.equal($('score-bars').children.length, 5);
  assert.equal($('prediction-label').textContent, 'No DR');
  assert.equal($('top-score').textContent, '79.7%');
  await $('download-result').emit('click');
  assert.equal(anchors.at(-1).clicked, true);
  assert.equal(JSON.parse(await blobs.at(-1).text()).request_id, recorded.real_prediction.request_id);
  nextResponse = {ok: false, status: 422, json: async () => ({
    error: {code: 'invalid_image', message: 'Cannot decode image'}
  })};
  await $('analyze').emit('click');
  assert.equal($('upload-error').textContent, 'Cannot decode image');
  assert.equal($('result-content').hidden, true);
  assert.equal($('score-bars').children.length, 0);
  assert.equal($('prediction-label').textContent, '');
  const downloadsBefore = anchors.length;
  await $('download-result').emit('click');
  assert.equal(anchors.length, downloadsBefore);
  nextResponse = {ok: false, status: 422, json: async () => ({error: {message: 'Invalid image fixture'}})};
  await $('analyze').emit('click');
  assert.equal($('result-content').hidden, true);
  assert.equal($('upload-error').textContent, 'Invalid image fixture');
  await $('remove-image').emit('click');
  assert.equal($('preview').hidden, true);
  assert.equal($('analyze').disabled, true);
  await $('file-input').emit('change', {target: {files: [{name: 'huge.png', size: 21 * 1024 * 1024, type: 'image/png'}]}});
  assert.match($('upload-error').textContent, /larger than 20 MB/);
  assert.equal(uploads.length, 3);
  location.hash = '#evaluation'; await win.emit('hashchange');
  await new Promise(resolve => setImmediate(resolve));
  assert.equal($('evaluation-content').hidden, false);
  assert.equal($('evaluation-metrics').children.length, 6);
  const metricsCards = $('evaluation-metrics').children;
  assert.equal(metricsCards[4].children[0].textContent, 'Any-DR sensitivity');
  assert.equal(metricsCards[4].children[1].textContent, '98.95%');
  assert.equal(metricsCards[5].children[1].textContent, '97.71%');
  assert.match($('sensitivity-detail').textContent, /470 \/ \(470 \+ 5\)/);
  assert.match($('specificity-detail').textContent, /513 \/ \(513 \+ 12\)/);
  assert.match($('binary-counts').textContent, /False negatives \(DR missed\): 5/);
  // Undefined denominators must render N/A, never zero or a misleading percentage.
  const original = saved.metrics.All;
  saved.metrics.All = {...original, binary: {...original.binary, sensitivity: null, specificity: null},
    undefined_reasons: {sensitivity: 'No positive ground-truth images', specificity: 'No negative ground-truth images'}};
  await vm.runInContext('evaluationLoaded = false; loadEvaluation()', context);
  assert.equal($('evaluation-metrics').children[4].children[1].textContent, 'N/A');
  assert.equal($('evaluation-metrics').children[5].children[1].textContent, 'N/A');
  assert.match($('sensitivity-detail').textContent, /No positive ground-truth images/);
  assert.match($('specificity-detail').textContent, /No negative ground-truth images/);
  saved.metrics.All = original;
  location.hash = '#integration'; await win.emit('hashchange');
  await $('copy-code').emit('click');
  assert.ok(copied.includes('http://127.0.0.1:8000/api/predict'));
  assert.ok(!copied.includes('\\n'));
  offline = true;
  await vm.runInContext('checkConnection()', context);
  assert.equal($('connection-text').textContent, 'Server offline');
  assert.equal($('analyze').disabled, true);
  console.log(JSON.stringify({status: 'passed', tested: ['sample selection', 'multipart request', 'five scores', 'JSON download', 'error clears stale result', 'remove image', 'size limit', 'navigation', 'saved evaluation', 'copy API example', 'offline state'], browser_rendering: 'not tested'}));
}
main().catch(error => { console.error(error); process.exitCode = 1; });
