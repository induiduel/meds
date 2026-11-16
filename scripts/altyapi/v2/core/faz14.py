"""Faz 14 (eski sistem) entegrasyonu.

Eski sistem, soruları bulut AI ile tek tek inceleyip `phase14_past_question_editor/reviews.jsonl`
içine yazıyor. Bu modül, hangi soruların zaten incelendiğini **içerik anahtarıyla** (id şemasından
bağımsız) tespit eder; böylece v2 aynı soruyu tekrar incelemez (çakışma/tekrar yok).
"""
from __future__ import annotations

from functools import lru_cache

from .. import config
from . import ids, store


def content_key(stem: str, options) -> str:
    parts = [ids.norm_key(stem or "")]
    if isinstance(options, dict):
        for k in sorted(options):
            parts.append(f"{k}:{ids.norm_key(str(options[k]))}")
    elif options:
        parts.extend(sorted(ids.norm_key(str(x)) for x in options))
    return "|".join(parts)


@lru_cache(maxsize=1)
def reviewed_keys() -> frozenset[str]:
    """Faz 14'ün incelediği soruların içerik anahtarları."""
    keys: set[str] = set()
    for rec in store.iter_jsonl(config.FAZ14_REVIEWS):
        src = rec.get("source") or {}
        stem = src.get("soru_koku") or src.get("stem") or rec.get("soru_koku")
        opts = src.get("secenekler") or src.get("options") or rec.get("secenekler")
        if stem:
            keys.add(content_key(stem, opts))
    return frozenset(keys)


def is_reviewed(rec: dict) -> bool:
    return content_key(rec.get("stem") or "", rec.get("options") or {}) in reviewed_keys()


def stats() -> dict:
    return {"incelenen": len(reviewed_keys())}
