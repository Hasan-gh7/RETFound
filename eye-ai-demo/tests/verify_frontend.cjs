const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { normalize } = require('../frontend/result-contract.js');
const source = {schema_version: 'retfound-prediction/1', predicted_grade: 2,
  scores: [.1,.1,.6,.1,.1], request_id: 'fixture', created_utc: '2026-11-04T20:00:00Z',
  input_validation: {status: 'accepted', decision: 1},
  model: {checkpoint_sha256: 'fixture', preprocessing_version: 'fixture', device: 'fixture', dtype: 'float32'}};
const unavailable = {engine: 'unavailable', available: false, detected: null, probability: null};
const result = {mode: 'retfound', analysis_id: 'fixture', timestamp: source.created_utc,
  source_prediction: source, models: {diabetic_retinopathy: {engine: 'retfound', grade: 2,
  confidence: .6, probabilities: source.scores}, amd: unavailable, glaucoma: unavailable}};
assert.equal(normalize(result, null).models.diabetic_retinopathy.grade, 2);
for (const bad of [{}, {...result, mode: 'demo'}, {...result, source_prediction: {}},
                   {...result, models: {...result.models, diabetic_retinopathy: {engine:'retfound',grade:0}}}]) {
  assert.throws(() => normalize(bad, null));
}
const frontend = path.join(__dirname, '../frontend');
const elements = new Map();
function element(id) {
  if (!elements.has(id)) elements.set(id, {id, checked:false, hidden:true, value:'', style:{}, dataset:{},
    classList:{add(){},remove(){},toggle(){}}, handlers:{}, addEventListener(type, fn){this.handlers[type]=fn;}, replaceChildren(){},
    querySelectorAll(){return[];}, querySelector(){return element('child');},
    closest(){return element('frame');}, scrollIntoView(){}, appendChild(){}, append(){}});
  return elements.get(id);
}
let calls = 0;
let fail = false;
const context = { window: {EyeAIContract: {normalize}},
  document: {getElementById:element, querySelectorAll:()=>[],createElement:()=>element('new')},
  localStorage:{getItem:()=> '[]',setItem(){}}, location:{protocol:'http:'},
  AbortController, AbortSignal, FormData, setTimeout, clearTimeout, console,
  fetch: async url => {calls++; if (fail) throw new TypeError('offline');
    return {ok:true,json:async()=>url==='/api/health'?{status:'ready',mode:'retfound',model:source.model}:result};}
};
vm.createContext(context);
vm.runInContext(fs.readFileSync(path.join(frontend,'app.js'),'utf8'),context);
(async()=>{
  await new Promise(resolve=>setImmediate(resolve));
  assert.equal(calls,1,'only health on initialization');
  const file = new Blob(['fixture'], {type:'image/png'});
  const good = await context.window.eyeAiDemo.requestAnalysis(file);
  assert.equal(good.mode,'retfound');
  context.window.eyeAiDemo.state.selectedFile=file;
  context.window.eyeAiDemo.state.imageDataUrl='data:image/jpeg;base64,fixture';
  element('consentCheck').checked=true;
  await element('analyzeBtn').handlers.click();
  assert.equal(element('drGrade').textContent,'2');
  assert.equal(element('resultsSection').hidden,false);
  assert.equal(element('amdProbability').textContent,'غير متاح');
  assert.ok(element('modelIdentity').textContent.includes('fixture'));
  await element('saveBtn').handlers.click();
  assert.equal(context.window.eyeAiDemo.state.cases.length,1);
  assert.equal(context.window.eyeAiDemo.state.cases[0].result.source_prediction.request_id,'fixture');
  fail = true;
  await assert.rejects(context.window.eyeAiDemo.requestAnalysis(file));
  await element('analyzeBtn').handlers.click();
  assert.equal(element('resultsSection').hidden,true,'no stale result after error');
  assert.equal(context.window.eyeAiDemo.state.result,null);
  assert.equal(element('analysisError').hidden,false);
  assert.equal(calls,5,'no automatic retry or demo fallback');
  context.location.protocol='file:';
  await assert.rejects(context.window.eyeAiDemo.requestAnalysis(file));
  const html=fs.readFileSync(path.join(frontend,'index.html'),'utf8');
  for(const id of elements.keys()) {
    if(!['child','frame','new'].includes(id)) assert.ok(html.includes(`id="${id}"`),`missing ${id}`);
  }
  console.log('Frontend contract, initialization, fixture rendering/save, stale-result clearing, offline failure, no retry and DOM references: PASS');
})().catch(error=>{console.error(error);process.exitCode=1;});
