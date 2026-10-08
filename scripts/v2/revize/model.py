"""Revize v2 — girdi modeli: Faz 14 incelemelerinden mevcut soru sürümünü çıkarır (salt okunur)."""
from __future__ import annotations

import json

from ..core import store, textnorm
from . import config


def _clean_field(v) -> str:
    return textnorm.clean_text(v) if isinstance(v, str) else ("" if v is None else str(v))


def _normalize(obj: dict, fallback_id: str) -> dict:
    opts = obj.get("secenekler") or {}
    opts = {str(k): _clean_field(v) for k, v in opts.items() if str(v).strip()}
    return {
        "id": obj.get("id") or fallback_id,
        "soru_koku": _clean_field(obj.get("soru_koku")),
        "secenekler": opts,
        "dogru_secenek": (obj.get("dogru_secenek") or None),
        "aciklama": _clean_field(obj.get("aciklama")),
        "kurul_adi": obj.get("kurul_adi"),
        "ders_adi": obj.get("ders_adi"),
        "konu_adi": obj.get("konu_adi"),
    }


def load_inputs(limit: int | None = None) -> list[dict]:
    """Her inceleme kaydı için 'mevcut' soru sürümü: proposal öncelikli, yoksa source."""
    out: list[dict] = []
    seen: set[str] = set()
    for rec in store.iter_jsonl(config.REVIEWS):
        qid = str(rec.get("question_id") or "")
        if not qid or qid in seen:
            continue
        seen.add(qid)
        src = rec.get("source") or {}
        prop = rec.get("proposal") or {}
        # proposal daha zenginse onu kullan; soru_kökü boşsa source'a düş.
        base = prop if (prop.get("soru_koku") or "").strip() else src
        item = _normalize(base, qid)
        item["_source"] = _normalize(src, qid)
        item["_faz14_status"] = rec.get("status")
        item["_review_required"] = (prop.get("review_required") if isinstance(prop, dict) else None)
        item["_support_ratio"] = rec.get("support_ratio")
        item["_model"] = rec.get("model")
        out.append(item)
        if limit and len(out) >= limit:
            break
    return out
