"""Read local sources without extracting ZIP members or following links."""
import os
import stat
import zipfile
from collections import Counter
from pathlib import Path, PurePosixPath

from retfound_platform.config import MAX_IMAGE_BYTES, MAX_SOURCE_BYTES, MAX_SOURCE_FILES

EXTENSIONS = {'.png', '.jpg', '.jpeg', '.tif', '.tiff', '.bmp'}


def safe_path(name: str) -> PurePosixPath:
    parts = name.split('/')
    if (not name or '\\' in name or ':' in name or name.startswith('/')
            or any(p in ('', '.', '..') for p in parts)):
        raise ValueError('Unsafe source path')
    return PurePosixPath(name)


def ignored(name: str) -> bool:
    return any(p.startswith('.') or p == '__MACOSX' for p in name.split('/'))


class LocalSource:
    def __init__(self, root: Path):
        self.root = root.expanduser().resolve(strict=True)
        self.archive = zipfile.ZipFile(self.root) if self.root.is_file() else None
        self.kind = 'zip' if self.archive else 'folder'
        self.entries: dict = {}
        self.issues: list[dict] = []
        self.split_evidence: set[str] = set()
        self.total = 0

    def __enter__(self):
        try:
            self._inventory()
        except BaseException:
            self.__exit__(None, None, None)
            raise
        return self

    def __exit__(self, *args):
        if self.archive:
            self.archive.close()

    def _add(self, name: str, size: int, entry: object, link: bool = False) -> None:
        try:
            path = safe_path(name)
            if ignored(name):
                return
            if link:
                raise ValueError('Symlinks/reparse points are not allowed')
            if path.suffix.lower() not in EXTENSIONS:
                return
            if size > MAX_IMAGE_BYTES:
                raise ValueError('Image exceeds byte limit')
            self.total += size
            if self.total > MAX_SOURCE_BYTES or len(self.entries) >= MAX_SOURCE_FILES:
                raise RuntimeError('Source exceeds resource limits')
            self.entries[name] = entry
        except ValueError as exc:
            self.issues.append({'path': name, 'reason': str(exc)})

    def _inventory(self) -> None:
        if self.archive:
            members = self.archive.infolist()
            if len(members) > MAX_SOURCE_FILES:
                raise ValueError('Archive contains too many members')
            counts = Counter(m.filename for m in members)
            normalized = Counter(m.filename.casefold() for m in members)
            for member in members:
                name = member.filename
                try:
                    safe_path(name[:-1] if member.is_dir() else name)
                except ValueError as exc:
                    self.issues.append({'path': name, 'reason': str(exc)})
                    continue
                if ignored(name):
                    continue
                if counts[name] > 1 or normalized[name.casefold()] > 1:
                    self.issues.append({'path': name, 'reason': 'Duplicate archive member/name collision'})
                    continue
                if member.is_dir():
                    continue
                if member.flag_bits & 1:
                    self.issues.append({'path': name, 'reason': 'Encrypted archive member'})
                    continue
                if member.file_size > max(1, member.compress_size) * 1000:
                    self.issues.append({'path': name, 'reason': 'Archive expansion ratio exceeds limit'})
                    continue
                self._add(name, member.file_size, member,
                          stat.S_ISLNK(member.external_attr >> 16))
        else:
            visited = 0
            for directory, dirs, files in os.walk(self.root, followlinks=False):
                for child in list(dirs):
                    path = Path(directory) / child
                    attrs = getattr(path.lstat(), 'st_file_attributes', 0)
                    if ignored(child) or path.is_symlink() or attrs & 0x400:
                        dirs.remove(child)
                        if not ignored(child):
                            self.issues.append({'path': path.relative_to(self.root).as_posix(),
                                                'reason': 'Linked directory excluded'})
                for child in files:
                    visited += 1
                    if visited > MAX_SOURCE_FILES:
                        raise ValueError('Source contains too many files')
                    path = Path(directory) / child
                    info = path.lstat()
                    self._add(path.relative_to(self.root).as_posix(), info.st_size, path,
                              path.is_symlink() or bool(getattr(info, 'st_file_attributes', 0) & 0x400))

    def read(self, name: str) -> bytes:
        safe_path(name)
        entry = self.entries[name]
        if self.archive:
            with self.archive.open(entry) as stream:
                payload = stream.read(MAX_IMAGE_BYTES + 1)
        else:
            path = Path(entry)
            if not path.resolve(strict=True).is_relative_to(self.root):
                raise ValueError('Path escapes source root')
            for part in (path, *path.parents):
                if part == self.root:
                    break
                if part.is_symlink() or getattr(part.lstat(), 'st_file_attributes', 0) & 0x400:
                    raise ValueError('Linked source path')
            with path.open('rb') as stream:
                payload = stream.read(MAX_IMAGE_BYTES + 1)
        if len(payload) > MAX_IMAGE_BYTES:
            raise ValueError('Image exceeds byte limit')
        return payload
