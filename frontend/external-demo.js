'use strict';
const element = id => document.getElementById(id);
let uncertain = false;
async function callApi(predict) {
  const key = element('key').value.trim().replace(/^Bearer\s+/i, '');
  if (!key) { element('status').textContent = 'Enter your RETFound access key.'; return; }
  const file = element('image').files[0];
  if (predict && (!file || file.size > 20 * 1024 * 1024)) {
    element('status').textContent = 'Choose an image of at most 20 MiB.'; return;
  }
  if (predict && uncertain) return;
  element('check').disabled = element('predict').disabled = true;
  element('result').textContent = '';
  element('status').textContent = predict ? 'Checking image with Jev and running RETFound…' : 'Checking connection…';
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), predict ? 120000 : 15000);
  try {
    const options = {headers: {Authorization: `Bearer ${key}`}, signal: controller.signal};
    if (predict) { options.method = 'POST'; options.body = new FormData(); options.body.append('image', file); }
    const response = await fetch(predict ? '/api/predict' : '/api/health', options);
    const data = await response.json();
    if (!response.ok) throw new Error(data.error?.message || `HTTP ${response.status}`);
    element('status').textContent = predict ? `${data.predicted_label} (grade ${data.predicted_grade})` : `Server: ${data.status}`;
    element('result').textContent = JSON.stringify(data, null, 2);
  } catch (error) {
    uncertain = predict && (error.name === 'AbortError' || error instanceof TypeError || error instanceof SyntaxError);
    element('status').textContent = uncertain ? 'Connection interrupted. Outcome unknown; check the server before retrying.' : error.message;
  } finally {
    clearTimeout(timer);
    element('check').disabled = false;
    element('predict').disabled = uncertain;
  }
}
element('check').addEventListener('click', () => callApi(false));
element('predict').addEventListener('click', () => callApi(true));
