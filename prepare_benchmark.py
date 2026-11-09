"""Fetch a reproducible sample from the official RETFound Google Drive ZIPs.

HTTP range reads avoid downloading the training images. No archive is extracted
wholesale: only selected test images are saved, under generated safe filenames.
"""
import argparse
import io
import json
import random
import re
import zipfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

import requests
from gdown.download import get_url_from_gdrive_confirmation

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'benchmark_data'
SOURCES = {
    'APTOS2019': ('162YPf4OhMVxj9TrQH0GnJv0n7z7gJWpj', 34),
    'IDRID': ('1c6zexA705z-ANEBNXJOBsk6uCvRnzmr3', 33),
    'MESSIDOR2': ('1vOLBUK9xdzNV8eVkRjVdNrRwhPfaOmda', 33),
}
CLASS_MAP = {
    'anodr': 0, 'bmilddr': 1, 'cmoderatedr': 2,
    'dseveredr': 3, 'eproliferativedr': 4, 'eprodr': 4,
    **{str(i): i for i in range(5)},
}

class RemoteZip(io.RawIOBase):
    def __init__(self, file_id):
        self.session = requests.Session()
        self.url = f'https://drive.google.com/uc?export=download&id={file_id}'
        for _ in range(5):
            r = self.session.get(self.url, stream=True, timeout=60)
            r.raise_for_status()
            if 'text/html' not in r.headers.get('Content-Type', ''):
                self.url = r.url
                r.close()
                break
            html = r.text
            r.close()
            self.url = get_url_from_gdrive_confirmation(html)
        r = self.session.get(self.url, headers={'Range': 'bytes=0-0'}, timeout=60, stream=True)
        if r.status_code != 206 or not r.headers.get('Content-Range'):
            status = r.status_code
            r.close()
            raise RuntimeError(f'Server does not support range reads: HTTP {status}')
        self.length = int(r.headers['Content-Range'].split('/')[-1])
        r.close()
        self.pos = 0
        print(f'Archive size: {self.length / 1e6:.1f} MB', flush=True)

    def seekable(self):
        return True

    def readable(self):
        return True

    def tell(self):
        return self.pos

    def seek(self, offset, whence=0):
        self.pos = offset if whence == 0 else self.pos + offset if whence == 1 else self.length + offset
        if self.pos < 0:
            raise ValueError('Negative seek')
        return self.pos

    def read(self, size=-1):
        end = self.length if size < 0 else min(self.length, self.pos + size)
        if end <= self.pos:
            return b''
        for attempt in range(3):
            try:
                r = self.session.get(self.url, headers={'Range': f'bytes={self.pos}-{end-1}'}, timeout=90)
                r.raise_for_status()
                if r.status_code != 206 or len(r.content) != end - self.pos:
                    raise RuntimeError('Invalid ranged response')
                result = r.content
                self.pos = end
                return result
            except requests.RequestException:
                if attempt == 2:
                    raise

    def close(self):
        self.session.close()
        super().close()

def prepare(name, inspect_only=False):
    file_id, count = SOURCES[name]
    folder = DATA / name
    folder.mkdir(parents=True, exist_ok=True)
    manifest_path = folder / 'manifest.json'
    if manifest_path.exists() and not inspect_only:
        manifest = json.loads(manifest_path.read_text())
        if len(manifest['images']) == count and all((ROOT / x['path']).is_file() for x in manifest['images']):
            print(name, 'already prepared', flush=True)
            return
    with RemoteZip(file_id) as remote, zipfile.ZipFile(remote) as archive:
        entries = archive.namelist()
        (folder / 'archive_entries.json').write_text(json.dumps(entries, indent=2), encoding='utf-8')
        images = [p for p in entries if Path(p).suffix.lower() in ('.jpg', '.jpeg', '.png', '.tif', '.tiff') and '__MACOSX' not in p and not any(part.startswith('.') for part in Path(p).parts)]
        groups = {}
        for p in images:
            parent = str(Path(p).parent).replace('\\', '/')
            groups[parent] = groups.get(parent, 0) + 1
        print(name, 'image folders:', json.dumps(groups), flush=True)
        if inspect_only:
            return
        test = sorted(p for p in images if 'test' in [x.lower() for x in Path(p).parts])
        if len(test) < count:
            raise RuntimeError(f'{name}: only {len(test)} test images, need {count}')
        chosen = sorted(random.Random(20261023).sample(test, count))
        records = []
        pending = []
        for i, member in enumerate(chosen):
            label = Path(member).parent.name.lower()
            if label not in CLASS_MAP:
                raise ValueError(f'Unrecognized DR class folder: {member}')
            output = folder / f'{i:03d}{Path(member).suffix.lower()}'
            if not output.exists():
                pending.append((i, member, output))
            records.append({'dataset': name, 'archive_path': member, 'path': output.relative_to(ROOT).as_posix(), 'true_grade': CLASS_MAP[label]})
        def fetch_group(group):
            if not group:
                return
            # Separate seek cursors and sessions for each worker.
            with RemoteZip(file_id) as source, zipfile.ZipFile(source) as source_zip:
                for i, member, output in group:
                    payload = source_zip.read(member)  # Checks the ZIP CRC.
                    temporary = output.with_suffix(output.suffix + '.part')
                    temporary.write_bytes(payload)
                    temporary.replace(output)
                    print(f'{name} image {i+1}/{count}: {member}', flush=True)
        print(f'{name}: reusing {count-len(pending)} images; downloading {len(pending)} with 4 workers', flush=True)
        with ThreadPoolExecutor(max_workers=4) as workers:
            list(workers.map(fetch_group, [pending[i::4] for i in range(4)]))
        manifest = {'dataset': name, 'source': f'https://drive.google.com/file/d/{file_id}/view', 'split': 'test', 'seed': 20261023, 'sampling': 'Uniform random sample without replacement from sorted test paths; hidden notebook copies excluded', 'class_mapping': CLASS_MAP, 'test_pool_size': len(test), 'images': records}
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--inspect', action='store_true')
    parser.add_argument('--dataset', choices=list(SOURCES))
    args = parser.parse_args()
    names = [args.dataset] if args.dataset else list(SOURCES)
    with ThreadPoolExecutor(max_workers=3) as pool:
        list(pool.map(lambda name: prepare(name, args.inspect), names))
