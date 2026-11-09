"""Forward original bytes; validate and adapt the existing prediction/1 contract."""
from __future__ import annotations

import hashlib
import json
import math
import os
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlsplit

import httpx

LABELS = ["لا توجد علامات ظاهرة", "اعتلال خفيف", "اعتلال متوسط", "اعتلال شديد", "اعتلال تكاثري / متقدم"]
UNAVAILABLE = {"engine": "unavailable", "available": False, "detected": None,
               "probability": None, "confidence": None}


class ServiceError(Exception):
    def __init__(self, status: int, message: str):
        self.status, self.message = status, message
        super().__init__(message)


@dataclass(frozen=True)
class Connection:
    base_url: str = "http://127.0.0.1:8000"
    api_key: str = field(default="", repr=False)

    def __post_init__(self):
        parsed = urlsplit(self.base_url)
        if (parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username
                or parsed.password or parsed.query or parsed.fragment or parsed.path not in {"", "/"}):
            raise ValueError("RETFOUND_API_URL must be a service origin without credentials or path")
        if parsed.scheme == "http" and parsed.hostname not in {"localhost", "127.0.0.1", "::1", "host.docker.internal"}:
            raise ValueError("Remote RETFound connections require HTTPS")
        if self.api_key and (not self.api_key.isascii() or any(c.isspace() or ord(c) < 32 or ord(c) == 127 for c in self.api_key)):
            raise ValueError("Invalid RETFound API key")

    @classmethod
    def from_environment(cls):
        key = os.environ.get("RETFOUND_API_KEY", "")
        configured = os.environ.get("RETFOUND_CONNECTION_FILE")
        demo_file = Path(__file__).resolve().parents[2] / 'connection.json'
        path = Path(configured) if configured else (demo_file if demo_file.is_file() else Path(__file__).resolve().parents[3] / ".runtime/tunnel/connection.json")
        values = {}
        if configured and not path.is_file():
            raise ValueError("RETFOUND_CONNECTION_FILE does not exist")
        if path.is_file():
            values = json.loads(path.read_text(encoding="utf-8"))
            authorization = values.get("authorization", "")
            if not isinstance(authorization, str) or not authorization.startswith("Bearer "):
                raise ValueError("Connection file must contain Bearer authorization")
            key = key or authorization.removeprefix("Bearer ")
        return cls(os.environ.get("RETFOUND_API_URL", values.get('base_url', "http://127.0.0.1:8000")).rstrip("/"), key)


def adapt_prediction(payload: dict, data: bytes) -> dict:
    try:
        grade = payload["predicted_grade"]
        scores = payload["scores"]
        identity = payload["model"]
        validation = payload["input_validation"]
        if (payload["schema_version"] != "retfound-prediction/1"
                or type(grade) is not int or grade not in range(5)
                or not isinstance(scores, list) or len(scores) != 5
                or any(type(s) not in {int, float} or not math.isfinite(s) or not 0 <= s <= 1 for s in scores)
                or abs(sum(scores) - 1) > 1e-4 or max(range(5), key=lambda i: scores[i]) != grade
                or not math.isclose(payload["top_score"], scores[grade], abs_tol=1e-6)
                or payload["image_sha256"] != hashlib.sha256(data).hexdigest()
                or validation["status"] != "accepted" or validation["decision"] != 1
                or validation["image_sha256"] != payload["image_sha256"]
                or not all(isinstance(identity[k], str) and identity[k] for k in
                           ["checkpoint_sha256", "preprocessing_version", "device", "dtype"])
                or not isinstance(payload["request_id"], str) or not payload["request_id"]
                or not isinstance(payload["created_utc"], str) or not payload["created_utc"]):
            raise ValueError("Invalid prediction")
    except (KeyError, TypeError, ValueError, OverflowError) as exc:
        raise ServiceError(502, "استجابة RETFound غير متوافقة؛ لم تُعرض أي نتيجة بديلة.") from exc
    return {"analysis_id": payload["request_id"], "timestamp": payload["created_utc"],
            "mode": "retfound", "source_prediction": payload,
            "models": {"diabetic_retinopathy": {"engine": "retfound", "grade": grade,
                       "label_ar": LABELS[grade], "confidence": scores[grade], "probabilities": scores},
                       "amd": dict(UNAVAILABLE), "glaucoma": dict(UNAVAILABLE)}}


class RETFoundClient:
    def __init__(self, connection: Connection, http: httpx.AsyncClient):
        self.connection, self.http = connection, http

    async def request(self, method: str, route: str, **kwargs) -> dict:
        headers = {"Accept": "application/json", **kwargs.pop("headers", {})}
        if self.connection.api_key:
            headers["Authorization"] = "Bearer " + self.connection.api_key
        try:
            response = await self.http.request(method, self.connection.base_url.rstrip("/") + route,
                                               headers=headers, **kwargs)
        except httpx.TimeoutException as exc:
            raise ServiceError(504, "انتهت مهلة RETFound. قد يكون الطلب نُفّذ؛ لا توجد إعادة محاولة تلقائية.") from exc
        except httpx.RequestError as exc:
            raise ServiceError(503, "تعذر الاتصال بخادم RETFound؛ تحقق من تشغيله وإعداد الاتصال.") from exc
        if response.status_code != 200:
            messages = {401: "مفتاح اتصال RETFound غير صالح أو انتهت جلسته.",
                        422: "رفض الخادم الصورة أو لم يقبلها فحص Jev؛ لم يُنتج تصنيفًا.",
                        429: "الخادم مشغول أو تم تجاوز حد الطلبات.",
                        503: "خدمة RETFound أو Jev غير جاهزة.",
                        504: "انتهت مهلة الخادم؛ لا توجد إعادة محاولة تلقائية."}
            raise ServiceError(response.status_code if response.status_code in messages else 502,
                               messages.get(response.status_code, "فشل طلب RETFound؛ لم تُنتج نتيجة بديلة."))
        try:
            payload = response.json()
            if not isinstance(payload, dict):
                raise ValueError("Expected object")
            return payload
        except ValueError as exc:
            raise ServiceError(502, "استجابة الخادم غير صالحة.") from exc

    async def health(self) -> dict:
        health = await self.request("GET", "/api/health")
        if health.get("status") != "ready":
            raise ServiceError(503, "خادم RETFound لم يجهز بعد.")
        model = await self.request("GET", "/api/model")
        return {"status": "ready", "mode": "retfound", "model": model}

    async def predict(self, data: bytes, content_type: str) -> dict:
        payload = await self.request("POST", "/api/predict", content=data,
                                     headers={"Content-Type": content_type})
        return adapt_prediction(payload, data)
