"""Güvenli G/Ç katmanı: atomik yazım, checkpoint, kilit ve "boş sonuçla ezme" koruması.

Güvenlik kuralı: v2 yalnızca izole CORE_DIR ağacına YAZAR. Genel amaçlı yazıcılar (`atomic_*`)
testler/ara dosyalar için serbesttir; üretim çıktısı için `write_core_*` kullanılır ve bunlar
`assert_under_core` ile korunur.
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any, Iterable, Iterator

from .. import config

try:
    import fcntl  # POSIX
except Exception:  # noqa: BLE001 - POSIX olmayan ortamda kilit devre dışı
    fcntl = None

__all__ = [
    "EmptyOverwriteError", "LockTimeout",
    "atomic_write_bytes", "atomic_write_text", "atomic_write_json",
    "read_text", "read_json", "iter_jsonl", "read_jsonl", "write_jsonl", "append_jsonl",
    "assert_under_core", "write_core_json", "write_core_jsonl",
    "FileLock", "State", "sha1_file", "now_iso", "update_katalog",
]


class EmptyOverwriteError(RuntimeError):
    """Dolu bir dosyanın üzerine boş içerik yazılmak istendi."""


class LockTimeout(RuntimeError):
    """Kilit zaman aşımına uğradı."""


def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S")


# ---- atomik yazım ---------------------------------------------------------------------------

def atomic_write_bytes(path: str | Path, data: bytes) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp-{os.getpid()}-{time.time_ns()}")
    with open(tmp, "wb") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)
    return path


def atomic_write_text(path: str | Path, text: str, encoding: str = "utf-8") -> Path:
    return atomic_write_bytes(path, text.encode(encoding))


def atomic_write_json(path: str | Path, obj: Any, indent: int = 1) -> Path:
    return atomic_write_text(path, json.dumps(obj, ensure_ascii=False, indent=indent))


# ---- okuma ----------------------------------------------------------------------------------

def read_text(path: str | Path) -> str | None:
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError:
        return None


def read_json(path: str | Path, default: Any = None) -> Any:
    txt = read_text(path)
    if txt is None:
        return default
    try:
        return json.loads(txt)
    except json.JSONDecodeError:
        return default


def iter_jsonl(path: str | Path) -> Iterator[dict]:
    try:
        fh = open(path, "r", encoding="utf-8")
    except OSError:
        return
    with fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def read_jsonl(path: str | Path) -> list[dict]:
    return list(iter_jsonl(path))


# ---- yazım (guard'lı) -----------------------------------------------------------------------

def _nonempty(path: Path) -> bool:
    try:
        return path.exists() and path.stat().st_size > 0
    except OSError:
        return False


def write_jsonl(path: str | Path, records: Iterable[dict], guard: bool = True) -> Path:
    """JSONL yazar. `guard` açıkken dolu dosyanın üzerine boş içerik yazılmaz."""
    path = Path(path)
    items = list(records)
    if guard and not items and _nonempty(path):
        raise EmptyOverwriteError(f"boş sonuç dolu dosyanın üzerine yazılamaz: {path}")
    body = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in items)
    return atomic_write_text(path, body)


def append_jsonl(path: str | Path, record: dict) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        fh.flush()
        os.fsync(fh.fileno())
    return path


# ---- CORE_DIR sınırı ------------------------------------------------------------------------

def assert_under_core(path: str | Path) -> Path:
    """Yol CORE_DIR dışındaysa hata verir (eski verinin yanlışlıkla ezilmesini engeller)."""
    p = Path(path)
    if not config.is_under_core(p):
        raise PermissionError(
            f"CORE_DIR dışına yazım reddedildi: {p} (izinli kök: {config.CORE_DIR})"
        )
    return p


def write_core_json(path: str | Path, obj: Any) -> Path:
    return atomic_write_json(assert_under_core(path), obj)


def write_core_jsonl(path: str | Path, records: Iterable[dict], guard: bool = True) -> Path:
    return write_jsonl(assert_under_core(path), records, guard=guard)


# ---- kilit ----------------------------------------------------------------------------------

class FileLock:
    """Süreçler arası özel kilit (fcntl). POSIX yoksa sessizce no-op olur."""

    def __init__(self, path: str | Path, timeout: float = 30.0, poll: float = 0.2):
        self.path = Path(path)
        self.timeout = timeout
        self.poll = poll
        self._fh = None

    def __enter__(self) -> "FileLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._fh = open(self.path, "w")
        if fcntl is None:
            return self
        deadline = time.monotonic() + self.timeout
        while True:
            try:
                fcntl.flock(self._fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                return self
            except OSError:
                if time.monotonic() > deadline:
                    self._fh.close()
                    self._fh = None
                    raise LockTimeout(f"kilit alınamadı: {self.path}")
                time.sleep(self.poll)

    def __exit__(self, *exc) -> None:
        if self._fh is not None:
            if fcntl is not None:
                try:
                    fcntl.flock(self._fh.fileno(), fcntl.LOCK_UN)
                except OSError:
                    pass
            self._fh.close()
            self._fh = None


# ---- checkpoint / durum ---------------------------------------------------------------------

class State:
    """Adım ilerlemesini `CORE_DIR/_state/<name>.json` içinde tutar (kaldığı yerden devam)."""

    def __init__(self, name: str, state_dir: str | Path | None = None):
        base = Path(state_dir) if state_dir else config.STATE_DIR
        self.path = base / f"{name}.json"
        data = read_json(self.path, {}) or {}
        self.data: dict = data
        self.data.setdefault("tamamlanan", [])

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.data[key] = value
        self.save()

    def is_done(self, item: str) -> bool:
        return item in set(self.data.get("tamamlanan", []))

    def mark_done(self, item: str) -> None:
        done = self.data.setdefault("tamamlanan", [])
        if item not in done:
            done.append(item)
            self.save()

    def save(self) -> None:
        self.data["guncelleme"] = now_iso()
        atomic_write_json(self.path, self.data)


# ---- yardımcılar ----------------------------------------------------------------------------

def sha1_file(path: str | Path, chunk: int = 1 << 20) -> str:
    import hashlib

    h = hashlib.sha1()
    with open(path, "rb") as fh:
        while True:
            block = fh.read(chunk)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def update_katalog(entry: dict) -> Path:
    """CORE_DIR/KATALOG.json içine veri kümesi girdisini ekler/günceller (ad'a göre tekil)."""
    config.ensure_core_dirs()
    kat = read_json(config.KATALOG_PATH, {}) or {}
    kumeler = [k for k in kat.get("veri_kumeleri", []) if k.get("ad") != entry.get("ad")]
    kumeler.append(entry)
    kat["zaman"] = now_iso()
    kat["veri_kumeleri"] = sorted(kumeler, key=lambda k: str(k.get("ad", "")))
    return write_core_json(config.KATALOG_PATH, kat)
