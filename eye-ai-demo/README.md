> Updated 2026-11-05: connection.json now supplies BOTH base_url and the RETFound access key. Put a private current copy beside run_demo.py on another computer, then run `python run_demo.py --connection-file connection.json` using Python with backend/requirements.txt installed. No OpenRouter key or model weights are needed on the demo computer. Earlier loopback-only defaults below are historical. Host two-app instructions: ../docs/TWO_APPS_AR.md.

# Eye AI · RETFound frontend

See [Arabic setup and behavior](README_AR.md) and [verification record](docs/PROGRESS.md).

This demo now delegates image admission and DR inference to the existing RETFound
HTTP service. It does not load ONNX models, transform inference inputs, or generate
synthetic predictions. AMD and glaucoma are unavailable. The original model service,
weights, datasets and Python environment are unchanged.

Run `start_windows.bat` using the existing ml-homework interpreter. Demo: port 8001;
RETFound: port 8000. No automatic dependency installation. Remote service origins
require HTTPS. Trial credentials stay server-side. Read README_AR.md before use.
