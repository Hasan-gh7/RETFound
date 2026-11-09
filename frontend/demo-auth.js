'use strict';
// Installed before the existing module scripts; credentials only go to this origin.
const originalFetch = window.fetch.bind(window);
let access = sessionStorage.getItem('retfound-demo-key') || '';
let resolveLogin;
const loginReady = access ? Promise.resolve() : new Promise(resolve => { resolveLogin = resolve; });
window.fetch = async (input, options = {}) => {
  const url = new URL(typeof input === 'string' ? input : input.url, location.href);
  if (url.origin !== location.origin || !url.pathname.startsWith('/api/')) return originalFetch(input, options);
  await loginReady;
  if (options.signal?.aborted && (!options.method || options.method === 'GET')) options = {...options, signal: AbortSignal.timeout(15000)};
  const headers = new Headers(options.headers || (input instanceof Request ? input.headers : undefined));
  headers.set('Authorization', `Bearer ${access}`);
  const response = await originalFetch(input, {...options, headers});
  if (response.status === 401) {
    sessionStorage.removeItem('retfound-demo-key');
    alert('Access key rejected. Reload this page and enter the current RETFound key.');
  }
  return response;
};
document.addEventListener('DOMContentLoaded', () => {
  if (access) return;
  const dialog = document.createElement('dialog');
  const title = document.createElement('h2'); title.textContent = 'Connect to RETFound';
  const note = document.createElement('p'); note.textContent = 'Enter the RETFound key from connection.json, not your OpenRouter key. Kept in this browser tab until it closes.';
  const input = document.createElement('input'); input.type = 'password'; input.autocomplete = 'off'; input.setAttribute('aria-label', 'RETFound access key');
  const button = document.createElement('button'); button.textContent = 'Open demo';
  button.onclick = () => {
    access = input.value.trim().replace(/^Bearer\s+/i, '');
    if (!access) return;
    sessionStorage.setItem('retfound-demo-key', access); input.value = ''; dialog.close(); dialog.remove(); resolveLogin();
  };
  dialog.addEventListener('cancel', event => event.preventDefault());
  dialog.append(title, note, input, button); document.body.append(dialog); dialog.showModal();
});
