"""Explicit one-request real integration check; no automatic retries."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import time
import urllib.request

parser = argparse.ArgumentParser()
parser.add_argument("--image", type=Path, required=True, help="Trusted local sample; sends it to RETFound and Jev")
args = parser.parse_args()
data = args.image.read_bytes()
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
with opener.open("http://127.0.0.1:8001/api/health", timeout=20) as response:
    health = json.load(response)
if health.get("status") != "ready":
    raise RuntimeError("Demo upstream not ready; no prediction sent")
started = time.perf_counter()
request = urllib.request.Request("http://127.0.0.1:8001/api/analyze", data=(
    b'--eye-demo-check\r\nContent-Disposition: form-data; name="file"; filename="sample.jpg"\r\n'
    b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n--eye-demo-check--\r\n'),
    headers={"Content-Type": "multipart/form-data; boundary=eye-demo-check"}, method="POST")
with opener.open(request, timeout=165) as response:
    result = json.load(response)
elapsed = time.perf_counter() - started
source = result["source_prediction"]
if result["mode"] != "retfound" or source["image_sha256"] != hashlib.sha256(data).hexdigest():
    raise RuntimeError("Unexpected result identity")
if result["models"]["diabetic_retinopathy"]["probabilities"] != source["scores"]:
    raise RuntimeError("Scores changed")
evidence = {"checked_utc": datetime.now(timezone.utc).isoformat(), "duration_seconds": round(elapsed, 3),
            "image": args.image.name, "health": health, "result": result}
destination = Path(__file__).resolve().parents[1] / ".runtime" / ("live-check-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + ".json")
destination.parent.mkdir(parents=True, exist_ok=True)
with destination.open("x", encoding="utf-8") as handle:
    json.dump(evidence, handle, ensure_ascii=False, indent=2, allow_nan=False)
print("Real integration PASS:", "grade", source["predicted_grade"], "device", source["model"]["device"],
      "scores", len(source["scores"]), "elapsed", round(elapsed, 3), "seconds")
print("Evidence:", destination)
