/* Synthetic UI behavior checks; no browser rendering or real predictions. */
const fs = require('node:fs'), vm = require('node:vm'), assert = require('node:assert/strict');
class Element {
  constructor(tag) { this.tagName = tag; this.children = []; this.events = {}; this.dataset = {}; this.textContent = ''; }
  append(...nodes) { this.children.push(...nodes); }
  addEventListener(name, callback) { this.events[name] = callback; }
  async click() { return this.events.click?.(); }
}
async function main() {
  const elements = new Map(['run-all','stop','download','status','samples'].map(id => [id, new Element('div')]));
  const manifest = JSON.parse(fs.readFileSync('upload_test_images/huggingface15-20261030/manifest.json'));
  const samples = manifest.records.map(r => ({...r, id: `${r.dataset}-${r.true_grade}`, image_url: `/api/demo/${r.dataset}-${r.true_grade}/image`}));
  const calls = [], blobs = []; let mode = 'success';
  const context = vm.createContext({console, AbortController, Blob, setTimeout: () => 1, clearTimeout() {},
    URL: {createObjectURL(blob) { blobs.push(blob); return 'blob:test'; }, revokeObjectURL() {}},
    document: {getElementById: id => elements.get(id), createElement: tag => new Element(tag)},
    async fetch(path, options) {
      calls.push(path);
      if (path === '/api/demo') return {ok: true, json: async () => ({samples})};
      if (path.endsWith('/image')) return {ok: true, blob: async () => new Blob(['synthetic image'])};
      assert.equal(options.method, 'POST');
      if (mode === 'rejected') return {ok: false, status: 422, json: async () => ({error: {code: 'not_retinal_fundus', message: 'Rejected'}})};
      if (mode === 'failed') return {ok: false, status: 503, json: async () => ({error: {code: 'fundus_check_unavailable', message: 'Unavailable'}})};
      const sample = samples.find(s => path === `/api/demo/${s.id}/predict`);
      return {ok: true, json: async () => ({schema_version: 'retfound-demo-result/1', reference: sample,
        matches_true_grade: sample.true_grade === 0, prediction: {predicted_grade: 0, predicted_label: 'No DR',
          image_sha256: sample.sha256, input_validation: {decision: 1}, scores: [.6,.1,.1,.1,.1]}})};
    }});
  vm.runInContext(fs.readFileSync('frontend/dataset-tests.js','utf8'), context);
  await new Promise(resolve => setImmediate(resolve));
  assert.equal(calls.filter(path => path.endsWith('/predict')).length, 0, 'Opening page must not run predictions');
  assert.equal(calls.filter(path => path.endsWith('/image')).length, 15);
  const cards = elements.get('samples').children.filter(el => el.className === 'grid').flatMap(grid => grid.children);
  assert.equal(cards.length, 15);
  await cards[0].children[2].click();
  assert.match(cards[0].children[3].textContent, /Matches reference/);
  assert.match(cards[0].children[4].textContent, /Grade 4/);
  mode = 'rejected'; await cards[0].children[2].click();
  assert.equal(cards[0].children[4].textContent, '', 'Rejection must clear old scores');
  assert.match(cards[0].children[3].textContent, /Rejected by Jev/);
  mode = 'failed'; const before = calls.length; await elements.get('run-all').click();
  assert.equal(calls.length, before + 1, 'Provider failure stops batch');
  assert.equal(cards[1].children[3].textContent, 'Not tested', 'New batch clears previous outcomes');
  await elements.get('download').click();
  const exported = JSON.parse(await blobs[blobs.length - 1].text());
  assert.equal(exported.results.length, 15);
  assert.equal(exported.results[0].status, 'error');
  assert.equal(exported.results[1].status, 'not_tested');
  console.log(JSON.stringify({status:'passed', cards:15, tested:['no auto inference','real endpoint request','comparison display','scores cleared on rejection','batch stops on service failure','honest JSON export'],browser_rendering:'not tested'}));
}
main().catch(error => { console.error(error); process.exitCode = 1; });
