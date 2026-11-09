"""Explicit online diagnostic; sends one text fixture then one image, never runs DR."""
import argparse
import getpass
import os
import re
from pathlib import Path
import sys
import time
import urllib.request
import subprocess

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from retfound_platform.inference.fundus_gate import ENDPOINT, MODEL, FundusGate, GateUnavailable


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--image', type=Path, default=ROOT / 'sample_images/idrid_test.jpg')
    parser.add_argument('--timeout', type=float, default=90)
    parser.add_argument('--new-key', action='store_true', help='Prompt for a key instead of using the environment; never save it')
    parser.add_argument('--start-server', action='store_true', help='Start the web app with the tested key after all checks pass')
    args = parser.parse_args()
    key = '' if args.new_key else os.environ.get('OPENROUTER_API_KEY', '').strip()
    if not key:
        key = getpass.getpass('OpenRouter API key (hidden, not saved): ').strip()
    if not key:
        print('No API key supplied.')
        return 1
    if not re.fullmatch(r'sk-or-v1-[A-Za-z0-9_-]{32,256}', key):
        print('The supplied value does not match the expected OpenRouter inference key format.\n'
              'Run again with --new-key and paste only the raw sk-or-v1- key, without quotes or Bearer.\n'
              'No request was sent. The key was not printed or saved.')
        return 1
    gate = FundusGate(key, timeout=args.timeout)
    print(f'Model: {MODEL}\nEndpoint: {ENDPOINT}\nSocket timeout: {gate.timeout:g}s', flush=True)
    # Presence only: proxy URLs may contain credentials and must never be printed.
    proxies = urllib.request.getproxies()
    print(f'HTTPS proxy configured: {bool(proxies.get("https"))}', flush=True)
    print('0/2 Checking OpenRouter authentication (no model invocation)...', flush=True)
    try:
        gate.check_authentication()
    except GateUnavailable as exc:
        print(f'AUTHENTICATION CHECK FAILED: {exc}', flush=True)
        if exc.diagnostic:
            print(exc.diagnostic, flush=True)
        print('No Jev requests or images were sent. If this is an empty HTTP 400, the failure also affects\n'
              'the standard OpenRouter key endpoint; changing the classifier prompt will not fix it.', flush=True)
        return 1
    print('OpenRouter accepted the key. Account details and key are not displayed.', flush=True)
    print('This makes two online requests billed to your OpenRouter account. No RETFound inference.', flush=True)
    started = time.monotonic()
    print('1/2 Text-only connection check...', flush=True)
    body = {'model': MODEL, 'state': 'connection test', 'questions': {'retinal_fundus': {
        'type': 'choice', 'instructions': 'Does the supplied text equal connection test?',
        'criteria': {'0': 'No', '1': 'Yes'}}}}
    try:
        choice = gate._request_decision(body)
        print(f'Text request succeeded in {time.monotonic() - started:.1f}s (fixture choice {choice}).', flush=True)
    except GateUnavailable as exc:
        print(f'TEXT FAILED: {exc}', flush=True)
        if exc.diagnostic:
            print(exc.diagnostic, flush=True)
        print('Image request skipped. Failure also affects requests without images.', flush=True)
        return 1
    print(f'2/2 Image check: {args.image.name} (sent externally)...', flush=True)
    started = time.monotonic()
    try:
        choice = gate.classify(args.image.read_bytes())
        print(f'Image request succeeded in {time.monotonic() - started:.1f}s. Fundus decision: {choice}', flush=True)
    except GateUnavailable as exc:
        print(f'IMAGE FAILED: {exc}\nText succeeded; failure is specific to the image request or intermittent provider/network behavior.', flush=True)
        if exc.diagnostic:
            print(exc.diagnostic, flush=True)
        return 1
    except OSError:
        print('Cannot read the specified image file.')
        return 1
    if args.start_server:
        environment = os.environ.copy()
        environment['OPENROUTER_API_KEY'] = key
        environment['JEV_TIMEOUT_SECONDS'] = str(args.timeout)
        print('Checks passed. Starting the web server with the tested key; keep this terminal open.', flush=True)
        return subprocess.call([sys.executable, '-B', str(ROOT / 'scripts/serve_web.py'), '--open-browser'],
                               cwd=str(ROOT), env=environment)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
