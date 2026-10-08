"""JSON-Schema doğrulaması — tek nokta.

Sözleşme `meds_database/schema/*.json` dosyalarıdır (question/chunk/source). Bu modül hem
denetçinin hem ingest'in kayıt doğrulamasını yapar; jsonschema varsa onu, yoksa küçük bir
yedek doğrulayıcıyı kullanır.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from .. import config

try:  # jsonschema çoğu ortamda var; yoksa yedek doğrulayıcı devreye girer
    import jsonschema as _jsonschema  # type: ignore
except Exception:  # noqa: BLE001
    _jsonschema = None

KINDS = ("question", "chunk", "source")
_FILES = {
    "question": "question.schema.json",
    "chunk": "chunk.schema.json",
    "source": "source.schema.json",
}


@lru_cache(maxsize=None)
def load_schema(kind: str) -> dict:
    if kind not in _FILES:
        raise ValueError(f"bilinmeyen şema türü: {kind!r} (beklenen: {KINDS})")
    path = Path(config.SCHEMA_DIR) / _FILES[kind]
    return json.loads(path.read_text(encoding="utf-8"))


def validate(record: Any, kind: str) -> list[str]:
    """Geçerliyse boş liste döner; aksi halde okunur hata mesajları."""
    schema = load_schema(kind)
    if _jsonschema is not None:
        validator = _jsonschema.Draft202012Validator(schema)
        errors = sorted(validator.iter_errors(record), key=lambda e: list(e.path))
        out = []
        for e in errors:
            loc = "/".join(str(p) for p in e.path) or "(kök)"
            out.append(f"{loc}: {e.message}")
        return out
    return _mini_validate(record, schema)


def is_valid(record: Any, kind: str) -> bool:
    return not validate(record, kind)


# ---- jsonschema yoksa kullanılan asgari doğrulayıcı -----------------------------------------

def _type_ok(value: Any, t: Any) -> bool:
    if isinstance(t, list):
        return any(_type_ok(value, x) for x in t)
    if t == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if t == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if t == "boolean":
        return isinstance(value, bool)
    if t == "null":
        return value is None
    py = {"object": dict, "array": list, "string": str}.get(t)
    return py is not None and isinstance(value, py)


def _mini_validate(value: Any, schema: dict, path: str = "") -> list[str]:
    errors: list[str] = []
    label = path or "(kök)"
    t = schema.get("type")
    if t is not None and not _type_ok(value, t):
        return [f"{label}: tip {t!r} bekleniyor"]
    if isinstance(value, dict):
        for req in schema.get("required", []):
            if req not in value:
                errors.append(f"{label}: zorunlu alan eksik: {req}")
        props = schema.get("properties", {})
        for key, sub in value.items():
            if key in props:
                errors += _mini_validate(sub, props[key], f"{path}/{key}")
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}/{key}: izin verilmeyen alan")
    if isinstance(value, list) and "items" in schema:
        for i, item in enumerate(value):
            errors += _mini_validate(item, schema["items"], f"{path}/{i}")
    enum = schema.get("enum")
    if enum is not None and value not in enum:
        errors.append(f"{label}: {value!r} izin verilen değerlerde değil {enum}")
    return errors
