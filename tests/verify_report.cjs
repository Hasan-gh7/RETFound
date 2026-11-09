/* Pure JavaScript contract checks with a minimal document stub; not a browser test. */
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const html = fs.readFileSync(process.argv[2], 'utf8');
const payload = html.match(/<script id="report-data" type="application\/json">([\s\S]*?)<\/script>/)[1];
const data = JSON.parse(payload);
const source = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)][0][1];
const elements = new Map();
for (const match of html.matchAll(/id="([^"]+)"/g)) {
  elements.set(match[1], {innerHTML: '', textContent: '', value: '', handlers: {},
    addEventListener(type, handler) { this.handlers[type] = handler; },
    showModal() { this.open = true; }, close() { this.open = false; }});
}
elements.get('report-data').textContent = payload;
elements.get('outcome').value = 'all';
elements.get('grade').value = 'all';
let exportedBlob, anchor;
const context = vm.createContext({document: {
  getElementById: id => elements.get(id), querySelectorAll: () => [],
  createElement: () => (anchor = {click() { this.clicked = true; }})},
  Blob, URL: {createObjectURL(blob) { exportedBlob = blob; return 'blob:test'; }, revokeObjectURL() {}},
  setTimeout: fn => fn()});
vm.runInContext(source, context);
const gallery = () => (elements.get('gallery').innerHTML.match(/<article /g) || []).length;
assert.equal(gallery(), data.records.length);
for (const outcome of ['wrong', 'ok', 'fn', 'fp']) {
  elements.get('outcome').value = outcome;
  elements.get('outcome').handlers.input();
  const expected = data.records.filter(r => outcome === 'wrong' ? !r.correct : outcome === 'ok' ? r.correct : outcome === 'fn' ? r.true_grade > 0 && r.predicted_grade === 0 : r.true_grade === 0 && r.predicted_grade > 0).length;
  assert.equal(gallery(), expected, outcome);
}
elements.get('outcome').value = 'all';
elements.get('grade').value = '3';
elements.get('grade').handlers.input();
assert.equal(gallery(), data.records.filter(r => r.true_grade === 3).length);
elements.get('grade').value = 'all';
elements.get('search').value = 'no-such-image-test';
elements.get('search').handlers.input();
assert.equal(gallery(), 0);
assert.match(elements.get('gallery').innerHTML, /No images match/);
elements.get('gallery').handlers.click({target: {closest: () => ({dataset: {index: '0'}})}});
assert.equal(elements.get('detail').open, true);
assert.equal((elements.get('detail-content').innerHTML.match(/class="prob"/g) || []).length, 5);
elements.get('close').onclick();
assert.equal(elements.get('detail').open, false);
elements.get('download').onclick();
assert.equal(anchor.clicked, true);
exportedBlob.text().then(csv => {
  assert.equal(csv.split('\r\n').length, data.records.length + 1);
  assert.match(csv.split('\r\n')[0], /score_4/);
  console.log(JSON.stringify({records: data.records.length, filters: 'passed', detail_scores: 5, csv_rows: data.records.length, browser_rendering: 'not tested'}));
});
