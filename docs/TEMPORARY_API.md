# Temporary external API trial

## Complete original demo (2026-11-05)

share_api.py now starts --public-demo and opens the external root URL automatically.
Enter the RETFound key from .runtime/tunnel/connection.json in the login dialog.
It is kept in sessionStorage for the current browser tab until closed. Jev's
OpenRouter key remains server-side. Original analysis, dataset tests and saved
evaluation pages share the authenticated API. Public static HTML/JS contain no
key; data and prediction endpoints require it. Full demo limit is 30 submissions
per minute; single-worker and three-slot constraints remain. Earlier API-only
restrictions below apply to serve_web.py --public-api without --public-demo.
Restart the current server to activate new server routes. No model duplication.

External browser demo: after restarting the updated launcher, open the printed
HTTPS URL with /external-demo appended. Enter the RETFound access key from the
stable connection.json (not OpenRouter), check connection, select an image and
analyze. The static page/script are public; all API requests still require the
key. The page does not persist keys or auto-run predictions. This upload demo
does not expose dataset tests, saved evaluations or the original local UI.

This opt-in mode keeps RETFound on the existing machine. It exposes only
GET /api/health, GET /api/model and POST /api/predict, all requiring the same
session Bearer key. It does not expose the frontend, dataset examples, saved
evaluation or OpenAPI. Ordinary local launch behavior is unchanged.

## Start from PowerShell in any directory

```powershell
& "$env:USERPROFILE\.conda\envs\ml-homework\python.exe" -B "C:/Users/jadgh/Desktop/Dr 4/Dr/RETFound/scripts/share_api.py"
```

Stop any existing RETFound server in its terminal first. The script refuses to
replace a process on its selected port. It prompts invisibly for the OpenRouter
inference key if unavailable in the current environment. That key is passed to
the model server environment, never saved or given to cloudflared. Syntax is
checked, but live provider authentication and credit availability are only
established by actual provider requests.

The script waits for the real model, then runs a temporary Quick Tunnel with
HTTP/2 and local Host rewriting. No firewall changes, service installation,
account or domain are required. Cloudflare connectivity is still required.
The classifier and its preprocessing remain unchanged.

A unique `.runtime/tunnel/<session>/connection.json` contains the URL and the
new session API key. Share this file privately with the colleague, never publish
it. It is local plaintext inside the ignored runtime directory. Logs sit next to
it; OpenRouter credentials are not intentionally logged. Keep the terminal open.
Ctrl+C stops both child processes; another start creates a different access key
and URL. No automatic retries, restart or persistent hosting are configured.

Limits: 10 prediction submissions per minute across this session key, three
admitted requests, one executor, original 20 MiB / 40 megapixel image limits.
Failed authenticated submissions count toward the minute limit. Health and model
checks do not. These are trial controls, not per-user billing or quotas.

## Colleague integration

```python
import requests

# Supply these through the colleague's backend environment/configuration.
base_url = "https://REPLACE.trycloudflare.com"
access_key = "REPLACE_WITH_SESSION_ACCESS_KEY"
headers = {"Authorization": "Bearer " + access_key}
print(requests.get(base_url + "/api/health", headers=headers, timeout=15).json())
with open("retina.jpg", "rb") as image:
    response = requests.post(base_url + "/api/predict", headers=headers,
                             files={"image": image}, timeout=120)
response.raise_for_status()
print(response.json())
```

The Telegram bot backend can use this same call after downloading a user file.
Ask users to send Document files to preserve original bytes. Do not place the
session key or OpenRouter key in a public browser frontend. This trial is aimed
at backend-to-backend calls; additional browser origins are not enabled.

401 means missing/incorrect access key; 429 means rate limit or full capacity;
422 may mean corrupt image or Jev non-fundus rejection; 503 may mean Jev unavailable.
An ambiguous timeout must not trigger an automatic prediction retry: paid work
can continue after the client disconnects. Send requests sequentially in the trial.

Images pass through Cloudflare and the current Jev/OpenRouter screening path;
Telegram also handles files submitted through its bot. No local prediction/upload
history is added. Scores remain uncalibrated research outputs.

## Tool download and independent verification

Official portable Windows AMD64 tool (no installer):
https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe

Save it as `.runtime/tunnel/cloudflared.exe`. Download source documentation:
https://developers.cloudflare.com/tunnel/downloads/

After launch, from a different network verify unauthenticated requests get 401,
authenticated health returns ready, and a trusted fundus image returns five scores.
Then stop the session and confirm the URL no longer serves the API. Creating a
URL or passing synthetic tests alone does not establish external model success.
