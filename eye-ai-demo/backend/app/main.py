"""Same-origin demo adapter; RETFound remains the sole inference service."""
from __future__ import annotations

import io
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

import httpx
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image, UnidentifiedImageError

from .retfound_client import Connection, ServiceError, RETFoundClient

BASE_DIR = Path(__file__).resolve().parents[2]
MAX_UPLOAD_BYTES = 10 * 1024 * 1024


class FrontendFiles(StaticFiles):
    """Windows MIME registry may label .js text/plain; nosniff must stay enabled."""
    async def get_response(self, path, scope):
        response = await super().get_response(path, scope)
        content_type = {".js": "text/javascript; charset=utf-8", ".css": "text/css; charset=utf-8",
                        ".webmanifest": "application/manifest+json"}.get(Path(path).suffix)
        if response.status_code == 200 and content_type:
            response.headers["Content-Type"] = content_type
        return response


def create_app(connection: Connection | None = None, transport=None) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app):
        configured = connection or Connection.from_environment()
        async with httpx.AsyncClient(timeout=httpx.Timeout(150, connect=5),
                                     follow_redirects=False, trust_env=False,
                                     transport=transport) as http:
            app.state.client = RETFoundClient(configured, http)
            yield

    app = FastAPI(title="Eye AI · RETFound adapter", version="2.0.0", lifespan=lifespan)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["127.0.0.1", "localhost", "[::1]", "testserver"])

    @app.middleware("http")
    async def protect(request: Request, call_next):
        origin = request.headers.get("origin")
        if request.method == "POST" and origin and origin != f"{request.url.scheme}://{request.url.netloc}":
            return JSONResponse({"detail": "هذا المصدر غير مسموح."}, status_code=403)
        if request.method == "POST":
            length = request.headers.get("content-length", "")
            if not length.isdecimal() or int(length) > MAX_UPLOAD_BYTES + 65536:
                return JSONResponse({"detail": "حجم الطلب غير مقبول."}, status_code=413)
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Content-Security-Policy"] = "default-src 'self'; img-src 'self' blob: data:; style-src 'self' 'unsafe-inline'; script-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'"
        return response

    @app.exception_handler(ServiceError)
    async def service_error(request, exc):
        return JSONResponse({"detail": exc.message}, status_code=exc.status)

    @app.get("/api/health")
    async def health(request: Request):
        return await request.app.state.client.health()

    @app.post("/api/analyze")
    async def analyze(request: Request, file: Annotated[UploadFile, File()]):
        try:
            if file.content_type not in {"image/jpeg", "image/png", "image/webp"}:
                raise HTTPException(415, "استخدم JPEG أو PNG أو WEBP.")
            data = await file.read(MAX_UPLOAD_BYTES + 1)
            if not data:
                raise HTTPException(400, "الملف فارغ.")
            if len(data) > MAX_UPLOAD_BYTES:
                raise HTTPException(413, "الحد الأقصى للصورة 10 ميغابايت.")
            try:
                with Image.open(io.BytesIO(data)) as image:
                    if image.width * image.height > 40_000_000 or getattr(image, "n_frames", 1) != 1:
                        raise ValueError("Image limits")
                    if image.format not in {"JPEG", "PNG", "WEBP"}:
                        raise ValueError("Image format")
                    image.verify()
            except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError) as exc:
                raise HTTPException(400, "الصورة تالفة أو تتجاوز حدود الصور المدعومة.") from exc
            return await request.app.state.client.predict(data, file.content_type)
        finally:
            await file.close()

    app.mount("/", FrontendFiles(directory=BASE_DIR / "frontend", html=True), name="frontend")
    return app


app = create_app()
