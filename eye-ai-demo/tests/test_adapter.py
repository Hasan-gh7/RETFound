"""Synthetic protocol tests; these never call a real model or provider."""
import copy
import hashlib
import io
import sys
import unittest
from pathlib import Path

DEMO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(DEMO))
sys.path.insert(0, str(DEMO.parent / ".runtime/web"))

import httpx
from PIL import Image
from backend.app.main import create_app
from backend.app.retfound_client import Connection, ServiceError, adapt_prediction


def prediction(data):
    digest = hashlib.sha256(data).hexdigest()
    return {"schema_version": "retfound-prediction/1", "request_id": "fixture-request",
            "created_utc": "2026-11-04T20:00:00Z", "predicted_grade": 2,
            "predicted_label": "Moderate", "scores": [.1, .1, .6, .1, .1], "top_score": .6,
            "image_sha256": digest,
            "model": {"checkpoint_sha256": "a" * 64, "preprocessing_version": "fixture-transform",
                      "device": "fixture-cpu", "dtype": "float32"},
            "input_validation": {"status": "accepted", "decision": 1, "image_sha256": digest}}


class ContractTests(unittest.TestCase):
    def test_maps_only_dr_and_preserves_provenance(self):
        original = prediction(b"bytes")
        result = adapt_prediction(original, b"bytes")
        self.assertEqual(result["source_prediction"], original)
        self.assertEqual(result["models"]["diabetic_retinopathy"]["probabilities"], original["scores"])
        for name in ["amd", "glaucoma"]:
            self.assertIsNone(result["models"][name]["detected"])
            self.assertFalse(result["models"][name]["available"])

    def test_rejects_invalid_scores_grades_hashes_and_admission(self):
        changes = [("scores", [float("nan")] * 5), ("scores", [.2] * 6),
                   ("scores", [.2] * 4), ("scores", [0] * 5),
                   ("predicted_grade", 0), ("predicted_grade", True),
                   ("top_score", .9), ("image_sha256", "wrong"),
                   ("input_validation", {"status": "rejected", "decision": 0}),
                   ("model", {}), ("schema_version", "different")]
        for key, value in changes:
            with self.subTest(key=key, value=value):
                payload = prediction(b"bytes")
                payload[key] = value
                with self.assertRaises(ServiceError):
                    adapt_prediction(payload, b"bytes")

    def test_rejects_unsafe_origins_and_hides_key(self):
        for url in ["http://example.com", "https://user:secret@example.com", "https://example.com/path"]:
            with self.assertRaises(ValueError):
                Connection(url)
        self.assertNotIn("secret", repr(Connection(api_key="secret")))


class APITests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.calls = []
        self.failure = None
        self.bad_payload = False
        stream = io.BytesIO()
        Image.new("RGB", (700, 700), (130, 48, 34)).save(stream, format="PNG")
        self.image = stream.getvalue()

        async def upstream(request):
            self.calls.append(request)
            if self.failure == "timeout":
                raise httpx.ReadTimeout("private transport details", request=request)
            if self.failure:
                return httpx.Response(self.failure, json={"error": "private provider details"})
            if request.url.path == "/api/health":
                return httpx.Response(200, json={"status": "ready"})
            if request.url.path == "/api/model":
                return httpx.Response(200, json=prediction(b"")["model"])
            if self.bad_payload:
                return httpx.Response(200, json={"predicted_grade": 0})
            return httpx.Response(200, json=prediction(request.content))

        self.app = create_app(Connection(api_key="fixture-secret"), httpx.MockTransport(upstream))
        self.lifespan = self.app.router.lifespan_context(self.app)
        await self.lifespan.__aenter__()
        self.client = httpx.AsyncClient(transport=httpx.ASGITransport(app=self.app), base_url="http://testserver")

    async def asyncTearDown(self):
        await self.client.aclose()
        await self.lifespan.__aexit__(None, None, None)

    async def upload(self, data=None, mime="image/png", headers=None):
        return await self.client.post("/api/analyze", files={"file": ("image.png", self.image if data is None else data, mime)}, headers=headers)

    async def test_health_never_predicts(self):
        response = await self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([r.url.path for r in self.calls], ["/api/health", "/api/model"])
        self.assertNotIn("fixture-secret", response.text)

    async def test_exact_bytes_auth_and_real_response_mapping(self):
        response = await self.upload()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.calls), 1)
        request = self.calls[0]
        self.assertEqual(request.url.path, "/api/predict")
        self.assertEqual(request.content, self.image)
        self.assertEqual(request.headers["authorization"], "Bearer fixture-secret")
        self.assertEqual(response.json()["mode"], "retfound")
        self.assertEqual(response.json()["models"]["diabetic_retinopathy"]["grade"], 2)
        self.assertIsNone(response.json()["models"]["amd"]["probability"])
        self.assertNotIn("fixture-secret", response.text)

    async def test_failures_never_produce_predictions_or_retry(self):
        for failure in [401, 422, 429, 503, 504, 500, "timeout"]:
            with self.subTest(failure=failure):
                self.failure = failure
                self.calls.clear()
                response = await self.upload()
                self.assertEqual(response.status_code, 504 if failure == "timeout" else 502 if failure == 500 else failure)
                self.assertNotIn("models", response.json())
                self.assertNotIn("private", response.text)
                self.assertEqual(len(self.calls), 1)

    async def test_bad_contract_blocked(self):
        self.bad_payload = True
        response = await self.upload()
        self.assertEqual(response.status_code, 502)
        self.assertNotIn("models", response.json())

    async def test_invalid_uploads_and_cross_origin_do_not_call_upstream(self):
        for data, mime, expected in [(b"", "image/png", 400), (b"bad", "image/png", 400),
                                     (b"text", "text/plain", 415), (b"x" * (10 * 1024 * 1024 + 1), "image/png", 413)]:
            response = await self.upload(data, mime)
            self.assertEqual(response.status_code, expected)
        response = await self.upload(headers={"Origin": "http://another-origin"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.calls, [])

    async def test_static_page_has_contract_and_no_secret(self):
        response = await self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("result-contract.js", response.text)
        self.assertNotIn("fixture-secret", response.text)

    async def test_script_mime_types_ignore_windows_registry(self):
        for name in ["app.js", "config.js", "result-contract.js"]:
            response = await self.client.get("/" + name)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.headers["content-type"], "text/javascript; charset=utf-8")
            self.assertEqual(response.headers["x-content-type-options"], "nosniff")


if __name__ == "__main__":
    unittest.main(verbosity=2)
