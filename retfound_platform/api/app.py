"""Local HTTP service; create_app is import safe and the model loads in lifespan."""
import asyncio
import io
import logging
import time
import uuid
import secrets
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, Response
from PIL import Image
from starlette.exceptions import HTTPException
from starlette.requests import ClientDisconnect
from starlette.staticfiles import StaticFiles
from starlette.middleware.trustedhost import TrustedHostMiddleware

from retfound_platform.config import ROOT, MAX_IMAGE_PIXELS
from retfound_platform.datasets.labels import GRADES
from retfound_platform.inference.fundus_gate import FundusGate, GateUnavailable, POLICY
from .demo_samples import DemoSamples
from .schemas import ModelIdentity, PredictionResponse
from .uploads import MAX_REQUEST_BYTES, MAX_UPLOAD_BYTES, UploadError, extract_image

LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class Settings:
    device: str = 'auto'
    capacity: int = 3
    upload_timeout_seconds: float = 30.0
    allowed_origins: tuple[str, ...] = ()
    frontend: Path = ROOT / 'frontend'
    demo_root: Path = ROOT / 'upload_test_images/huggingface15-20261030'
    api_key: str = ''
    public_api: bool = False
    public_demo: bool = False


def make_predictor(device: str):
    from retfound_platform.inference.predictor import Predictor
    return Predictor(device=device)


def error(status: int, code: str, message: str, request_id: str = '', headers=None) -> JSONResponse:
    return JSONResponse({'error': {'code': code, 'message': message}, 'request_id': request_id},
                        status_code=status, headers=headers)


def create_app(settings: Settings | None = None, predictor_factory: Callable | None = None, gate=None) -> FastAPI:
    settings = settings or Settings()
    if settings.public_api and len(settings.api_key) < 32:
        raise ValueError('Public API requires an access key of at least 32 characters')
    if not 1 <= settings.capacity <= 8 or settings.upload_timeout_seconds <= 0:
        raise ValueError('Capacity must be 1..8 and upload timeout must be positive')
    if '*' in settings.allowed_origins:
        raise ValueError('Configure explicit browser origins; wildcard origins are unsupported')
    demos = DemoSamples(settings.demo_root)
    factory = predictor_factory or make_predictor
    fundus_gate = gate if gate is not None else FundusGate.from_environment()

    @asynccontextmanager
    async def lifespan(app):
        app.state.ready = False
        app.state.active = 0
        executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix='retfound-inference')
        app.state.executor = executor
        try:
            loop = asyncio.get_running_loop()
            predictor = await loop.run_in_executor(executor, factory, settings.device)
            app.state.predictor = predictor
            meta = predictor.metadata
            app.state.model = ModelIdentity(
                checkpoint_sha256=meta['checkpoint_sha256'],
                preprocessing_version=meta['preprocessing_version'],
                device=meta['device'], dtype=meta['dtype'], grades=GRADES,
            )
            app.state.ready = True
            yield
        finally:
            app.state.ready = False
            executor.shutdown(wait=True, cancel_futures=True)
            app.state.predictor = None

    app = FastAPI(title='RETFound image prediction API', version='1.0.0', lifespan=lifespan,
                  description='Image bytes or one multipart image upload. Five ordered, uncalibrated model scores.',
                  docs_url=None, redoc_url=None)
    app.state.ready = False
    app.state.active = 0
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=['127.0.0.1', 'localhost', '[::1]'])
    if settings.allowed_origins:
        app.add_middleware(CORSMiddleware, allow_origins=list(settings.allowed_origins),
                           allow_methods=['GET', 'POST'], allow_headers=['Content-Type', 'Authorization'], max_age=600)

    admissions = deque()

    @app.middleware('http')
    async def response_headers(request: Request, call_next):
        ui_paths = {'/', '/index.html', '/app.js', '/styles.css', '/input-validation.css', '/favicon.svg', '/dataset-tests', '/dataset-tests.js', '/dataset-tests.css', '/demo-auth.js'}
        public_demo_asset = request.method == 'GET' and (request.url.path in {'/external-demo', '/external-demo.js', '/demo-auth.js'} or (settings.public_demo and request.url.path in ui_paths))
        if settings.public_api and not public_demo_asset:
            allowed = {('/api/health', 'GET'), ('/api/model', 'GET'), ('/api/predict', 'POST'), ('/api/predict/summary', 'POST')}
            if settings.public_demo:
                allowed.update({('/api/demo', 'GET'), ('/api/example', 'GET'), ('/api/evaluation', 'GET'), ('/openapi.json', 'GET')})
                parts = request.url.path.split('/')
                if len(parts) == 5 and parts[1:3] == ['api', 'demo'] and parts[4] in {'image', 'thumbnail', 'predict'}:
                    allowed.add((request.url.path, 'POST' if parts[4] == 'predict' else 'GET'))
            if request.method != 'OPTIONS':
                supplied = request.headers.get('authorization', '')
                if not secrets.compare_digest(supplied.encode('utf-8'), ('Bearer ' + settings.api_key).encode('utf-8')):
                    return error(401, 'unauthorized', 'A valid Bearer access key is required.', headers={'WWW-Authenticate': 'Bearer', 'Cache-Control': 'no-store'})
                if (request.url.path, request.method) not in allowed:
                    return error(404, 'not_found', 'This route is not available on the temporary API.')
                if request.method == 'POST':
                    now = time.monotonic()
                    while admissions and now - admissions[0] >= 60:
                        admissions.popleft()
                    maximum = 30 if settings.public_demo else 10
                    if len(admissions) >= maximum:
                        return error(429, 'rate_limited', f'Temporary API allows {maximum} submissions per minute.', headers={'Retry-After': '60', 'Cache-Control': 'no-store'})
                    admissions.append(now)
        # A browser from another origin must opt in even though localhost has no credentials.
        origin = request.headers.get('origin')
        same_origin = f'{request.url.scheme}://{request.url.netloc}'
        if not settings.public_api and request.method == 'POST' and origin and origin != same_origin and origin not in settings.allowed_origins:
            return error(403, 'origin_not_allowed', 'This browser origin is not enabled for the API.')
        response = await call_next(request)
        response.headers['Cache-Control'] = 'no-store'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Referrer-Policy'] = 'no-referrer'
        response.headers['Content-Security-Policy'] = "default-src 'self'; img-src 'self' blob: data:; style-src 'self'; script-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'"
        return response

    @app.exception_handler(HTTPException)
    async def http_error(request, exc):
        return error(exc.status_code, 'http_error', str(exc.detail))

    @app.exception_handler(RequestValidationError)
    async def validation_error(request, exc):
        return error(422, 'invalid_request', 'The request does not match the API contract.')

    @app.get('/external-demo', include_in_schema=False)
    async def external_demo():
        return FileResponse(settings.frontend / 'external-demo.html', media_type='text/html')

    @app.get('/demo-auth.js', include_in_schema=False)
    async def demo_auth_script():
        if settings.public_api and settings.public_demo:
            return FileResponse(settings.frontend / 'demo-auth.js', media_type='text/javascript')
        return Response('', media_type='text/javascript')

    @app.get('/external-demo.js', include_in_schema=False)
    async def external_demo_script():
        return FileResponse(settings.frontend / 'external-demo.js', media_type='text/javascript')

    @app.get('/api/health')
    async def health():
        return JSONResponse({'status': 'ready' if app.state.ready else 'loading',
                             'active_requests': app.state.active, 'capacity': settings.capacity},
                            status_code=200 if app.state.ready else 503)

    @app.get('/api/model', response_model=ModelIdentity)
    async def model():
        if not app.state.ready:
            return error(503, 'model_unavailable', 'The model is still loading. Try again shortly.')
        return app.state.model

    def infer(payload: bytes):
        # Inspect content, not the filename or the supplied MIME type.
        try:
            with Image.open(io.BytesIO(payload)) as image:
                if image.format not in {'JPEG', 'PNG', 'TIFF', 'BMP', 'WEBP'}:
                    raise ValueError('Unsupported image format')
                if image.width * image.height > MAX_IMAGE_PIXELS or getattr(image, 'n_frames', 1) != 1:
                    raise ValueError('Invalid image dimensions or multiple frames')
                image.load()
        except (ValueError, OSError, Image.DecompressionBombError, Image.DecompressionBombWarning) as exc:
            raise UploadError(422, 'invalid_image', 'This image could not be decoded. Use a valid, single-frame JPEG, PNG, TIFF, BMP or WebP of at most 40 megapixels.') from exc
        try:
            gate_started = time.monotonic()
            decision = fundus_gate.classify(payload)
            gate_ms = (time.monotonic() - gate_started) * 1000
        except GateUnavailable as exc:
            raise UploadError(503, 'fundus_check_unavailable', str(exc)) from None
        if type(decision) is not int or decision not in (0, 1):
            raise UploadError(503, 'fundus_check_unavailable', 'Invalid response from retinal image check.')
        if decision == 0:
            raise UploadError(422, 'not_retinal_fundus', 'Please submit a retinal fundus image')
        model_started = time.monotonic()
        result = app.state.predictor.predict(payload)
        model_ms = (time.monotonic() - model_started) * 1000
        return {**result, 'timing_ms': {'jev': round(gate_ms, 2), 'retfound': round(model_ms, 2)}, 'input_validation': {
            'status': 'accepted', 'decision': 1, 'image_sha256': result['image_sha256'],
            'basis': 'Jev identified a retinal fundus photograph',
            'policy_version': POLICY,
            'limitation': 'Automated modality screening can be wrong; fundus accuracy and image quality are not validated.',
        }}

    @app.post('/api/predict', response_model=PredictionResponse, responses={
        400: {'description': 'Malformed image upload'}, 413: {'description': 'Upload exceeds limit'},
        415: {'description': 'Unsupported content type'}, 422: {'description': 'Missing or unreadable image'},
        429: {'description': 'All inference slots are occupied'}, 503: {'description': 'Model unavailable'},
    }, openapi_extra={'requestBody': {'required': True, 'content': {
        'multipart/form-data': {'schema': {'type': 'object', 'required': ['image'],
            'properties': {'image': {'type': 'string', 'format': 'binary'}}}},
        'image/jpeg': {'schema': {'type': 'string', 'format': 'binary'}},
        'image/png': {'schema': {'type': 'string', 'format': 'binary'}},
        'application/octet-stream': {'schema': {'type': 'string', 'format': 'binary'}},
    }}})
    async def predict(request: Request):
        return await perform_prediction(request)

    @app.post('/api/predict/summary')
    async def predict_summary(request: Request):
        result = await perform_prediction(request)
        if not isinstance(result, PredictionResponse):
            return result
        return {'predicted_grade': result.predicted_grade, 'predicted_label': result.predicted_label,
                'class_scores_percent': [
                    {'grade': grade, 'label': label, 'score': round(result.scores[grade] * 100, 2)}
                    for grade, label in enumerate(GRADES)]}

    async def perform_prediction(request: Request, sample_id: str | None = None):
        request_id = uuid.uuid4().hex
        if not app.state.ready:
            return error(503, 'model_unavailable', 'The model is still loading. Try again shortly.', request_id)
        if app.state.active >= settings.capacity:
            return error(429, 'server_busy', 'The model is busy. Please try again in a moment.', request_id, {'Retry-After': '2'})
        # No await between admission check and increment: bounded across concurrent requests.
        app.state.active += 1
        future = None
        started = time.perf_counter()
        try:
            reference = None
            if sample_id is not None:
                def infer_demo():
                    row, payload = demos.load(sample_id)
                    return row, infer(payload)
                future = asyncio.get_running_loop().run_in_executor(app.state.executor, infer_demo)
            else:
                size = request.headers.get('content-length')
                if size and (not size.isdecimal() or int(size) > MAX_REQUEST_BYTES):
                    raise UploadError(413, 'upload_too_large', 'The image must be 20 MB or smaller.')
    
                async def read_body():
                    body = bytearray()
                    async for chunk in request.stream():
                        if len(body) + len(chunk) > MAX_REQUEST_BYTES:
                            raise UploadError(413, 'upload_too_large', 'The image must be 20 MB or smaller.')
                        body.extend(chunk)
                    return bytes(body)
    
                body = await asyncio.wait_for(read_body(), timeout=settings.upload_timeout_seconds)
                payload = extract_image(body, request.headers.get('content-type', ''))
                del body
                future = asyncio.get_running_loop().run_in_executor(app.state.executor, infer, payload)
            # Keep the slot reserved until the actual GPU task finishes, even on cancellation.
            result = await asyncio.shield(future)
            if sample_id is not None:
                reference, result = result
            prediction = PredictionResponse(**result, request_id=request_id,
                created_utc=datetime.now(timezone.utc).isoformat(),
                elapsed_ms=round((time.perf_counter() - started) * 1000, 2), model=app.state.model)
            if reference is not None:
                return {'schema_version': 'retfound-demo-result/1', 'reference': reference,
                        'matches_true_grade': prediction.predicted_grade == reference['true_grade'],
                        'prediction': prediction.model_dump()}
            return prediction
        except UploadError as exc:
            response = error(exc.status, exc.code, str(exc), request_id)
            if exc.code == 'not_retinal_fundus':
                return JSONResponse({'error': {'code': exc.code, 'message': str(exc)}, 'request_id': request_id, 'prediction': None, 'input_validation': {'status': 'rejected', 'decision': 0, 'policy_version': POLICY}}, status_code=422)
            return response
        except asyncio.TimeoutError:
            return error(408, 'upload_timeout', 'The upload took too long. Please try again.', request_id)
        except ClientDisconnect:
            return error(400, 'upload_interrupted', 'The upload was interrupted.', request_id)
        except Exception:
            LOG.exception('Inference failed: request_id=%s', request_id)
            return error(500, 'prediction_failed', 'Prediction failed. Please try again or check the server log.', request_id)
        finally:
            if future is not None and not future.done():
                def release(completed):
                    app.state.active -= 1
                    if not completed.cancelled():
                        completed.exception()  # consume errors after client cancellation
                future.add_done_callback(release)
            else:
                app.state.active -= 1

    @app.get('/api/demo')
    async def demo_catalog():
        try:
            return {'samples': demos.catalog(), 'description': 'Balanced demonstration with one test image per grade per dataset. Not a representative accuracy benchmark.'}
        except UploadError as exc:
            return error(exc.status, exc.code, str(exc))

    @app.get('/api/demo/{sample_id}/image')
    async def demo_image(sample_id: str):
        try:
            _, payload = await asyncio.to_thread(demos.load, sample_id)
            return Response(payload, media_type='image/png' if payload.startswith(b'\x89PNG') else 'image/jpeg')
        except UploadError as exc:
            return error(exc.status, exc.code, str(exc))

    @app.get('/api/demo/{sample_id}/thumbnail')
    async def demo_thumbnail(sample_id: str):
        def render():
            _, payload = demos.load(sample_id)
            with Image.open(io.BytesIO(payload)) as original:
                preview = original.convert('RGB')
                preview.thumbnail((320, 320))
                output = io.BytesIO()
                preview.save(output, format='JPEG', quality=75)
                return output.getvalue()
        try:
            return Response(await asyncio.to_thread(render), media_type='image/jpeg')
        except UploadError as exc:
            return error(exc.status, exc.code, str(exc))

    @app.post('/api/demo/{sample_id}/predict')
    async def demo_predict(sample_id: str, request: Request):
        return await perform_prediction(request, sample_id)

    @app.get('/dataset-tests', include_in_schema=False)
    async def demo_page():
        return FileResponse(settings.frontend / 'dataset-tests.html', media_type='text/html')

    @app.get('/dataset-tests.js', include_in_schema=False)
    async def demo_script():
        return FileResponse(settings.frontend / 'dataset-tests.js', media_type='text/javascript')

    @app.get('/dataset-tests.css', include_in_schema=False)
    async def demo_style():
        return FileResponse(settings.frontend / 'dataset-tests.css', media_type='text/css')

    @app.get('/api/example', include_in_schema=False)
    async def example():
        return FileResponse(ROOT / 'sample_images/idrid_test.jpg', media_type='image/jpeg')

    @app.get('/api/evaluation', include_in_schema=False)
    async def evaluation():
        # Read-only reference to a completed run; never substitute example predictions.
        import json
        path = ROOT / 'results/runs/aptos1000-20261029/predictions.json'
        if not path.is_file():
            return error(404, 'evaluation_unavailable', 'The saved evaluation is not available.')
        report = json.loads(path.read_text(encoding='utf-8'))
        return {'run_id': report['run_id'], 'created_utc': report['created_utc'],
                'metrics': report['metrics']['All'], 'limitations': report['limitations']}

    # Windows registry MIME mappings can classify .js as text/plain. Module
    # scripts require a JavaScript MIME type, so pin our known assets explicitly.
    @app.get('/app.js', include_in_schema=False)
    async def javascript():
        return FileResponse(settings.frontend / 'app.js', media_type='text/javascript')

    @app.get('/styles.css', include_in_schema=False)
    async def stylesheet():
        return FileResponse(settings.frontend / 'styles.css', media_type='text/css')

    @app.get('/favicon.svg', include_in_schema=False)
    async def favicon():
        return FileResponse(settings.frontend / 'favicon.svg', media_type='image/svg+xml')

    app.mount('/', StaticFiles(directory=settings.frontend, html=True, check_dir=False), name='web')
    return app
