"""Exercise the running real-model API from a separate local HTTP client."""
import argparse
import concurrent.futures
import json
import io
import math
import time
from pathlib import Path
from web_runtime import configure


def main() -> None:
    root = configure()
    import httpx
    from retfound_platform.datasets.manifests import write_json
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', default='http://127.0.0.1:8000')
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    payload = (root / 'sample_images/idrid_test.jpg').read_bytes()
    reference = json.loads((root / 'results/runs/aptos-audit-20261029/inference-verification.json').read_text(encoding='utf-8'))['cuda_prediction']
    with httpx.Client(base_url=args.url, timeout=120, trust_env=False) as client:
        for _ in range(90):
            try:
                health = client.get('/api/health')
                if health.status_code == 200:
                    break
            except httpx.ConnectError:
                pass
            time.sleep(1)
        else:
            raise RuntimeError('API did not become ready')
        model = client.get('/api/model')
        model.raise_for_status()
        raw = client.post('/api/predict', content=payload, headers={'Content-Type': 'image/jpeg'})
        raw.raise_for_status()
        multipart = client.post('/api/predict', files={'image': ('retina.jpg', payload, 'image/jpeg')})
        multipart.raise_for_status()
        prediction = multipart.json()
        if prediction['input_validation']['status'] != 'accepted':
            raise ValueError('Jev admission contract was not returned')
        delta = max(abs(a-b) for a, b in zip(prediction['scores'], reference['scores']))
        if delta > 1e-6 or prediction['predicted_grade'] != reference['predicted_grade']:
            raise ValueError('API result does not match verified inference')
        if prediction['scores'] != raw.json()['scores']:
            raise ValueError('Raw and multipart results differ')
        if not all(math.isfinite(value) for value in prediction['scores']):
            raise ValueError('Non-finite scores')
        corrupt = client.post('/api/predict', content=b'invalid-image', headers={'Content-Type': 'image/png'})
        if corrupt.status_code != 422:
            raise ValueError('Invalid image was not rejected')
        # New encoding: test a new input, not a change to model preprocessing.
        from PIL import Image
        import hashlib
        buffer = io.BytesIO()
        with Image.open(io.BytesIO(payload)) as image:
            image.convert('RGB').save(buffer, format='PNG')
        new_payload = buffer.getvalue()
        new_response = client.post('/api/predict', files={'image': ('new-retina.png', new_payload, 'image/png')})
        new_response.raise_for_status()
        new_prediction = new_response.json()
        if (new_prediction['input_validation']['status'] != 'accepted'
                or new_prediction['image_sha256'] != hashlib.sha256(new_payload).hexdigest()
                or len(new_prediction['scores']) != 5):
            raise ValueError('New image failed Jev admission')
        responses = {path: client.get(path) for path in ['/', '/app.js', '/styles.css', '/input-validation.css', '/favicon.svg', '/openapi.json', '/api/evaluation']}
        if any(response.status_code != 200 for response in responses.values()):
            raise ValueError('A web asset or metadata endpoint failed')
        expected_types = {'/': 'text/html', '/app.js': 'text/javascript', '/styles.css': 'text/css',
                          '/input-validation.css': 'text/css',
                          '/favicon.svg': 'image/svg+xml', '/openapi.json': 'application/json',
                          '/api/evaluation': 'application/json'}
        for path, expected in expected_types.items():
            if responses[path].headers['content-type'].split(';')[0] != expected:
                raise ValueError(f'Incorrect browser content type for {path}')
        def concurrent_predict(index):
            result = client.post('/api/predict', content=payload, headers={'Content-Type': 'image/jpeg'})
            result.raise_for_status()
            return result.json()
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            parallel = list(executor.map(concurrent_predict, range(3)))
        if any(row['scores'] != prediction['scores'] for row in parallel):
            raise ValueError('Concurrent predictions differ')
        if client.get('/api/health').json()['active_requests'] != 0:
            raise ValueError('Inference slot was not released')
        result = {'status': 'passed', 'url': args.url, 'model': model.json(),
                  'real_prediction': prediction, 'baseline_max_score_delta': delta,
                  'raw_and_multipart_match': True, 'concurrent_successes': len(parallel),
                  'corrupt_image_status': corrupt.status_code,
                  'new_image_prediction': new_prediction,
                  'new_image_requires_approval': False,
                  'asset_statuses': {path: response.status_code for path, response in responses.items()},
                  'asset_content_types': {path: response.headers['content-type'] for path, response in responses.items()},
                  'browser_visual_verification': 'unavailable: browser access host and native pipe absent'}
        write_json(args.output, result)
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
