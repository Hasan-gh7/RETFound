# Eye AI demo integration scope

2026-11-05: user now requests this application as an independent external API
client on another device. Read both URL/key from private connection.json and
keep credentials in the adapter. Parent orchestrator may start it on port 8001.
Previous demo-only scope below describes the earlier phase, not this expansion.

Authorized scope: only eye-ai-demo. Connect to the existing RETFound HTTP contract;
no changes to the parent service, model, checkpoint, preprocessing or environment.

Completed: same-origin adapter, server-side trial authentication, strict response
mapping, original-byte forwarding, error blocking, DR-only UI/report/history,
no synthetic predictions, nonconflicting launcher, synthetic protocol/UI tests,
real health/model read and browser connection verification.

Pending user authorization: one real public sample through RETFound and external
Jev; opt-in tests/live_smoke.py records a unique evidence file after success.
Camera, PDF layout, Docker deployment and clinical evaluation remain unverified.
No training, ONNX export, new disease models or public demo hosting is planned.
