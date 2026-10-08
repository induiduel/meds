"""s10 — Ders notları ve özetlerini düzeltilmiş biçimde CORE'a alır.

Kaynaklar (salt okunur): `meds_database/derived/clean_notes/*.jsonl` (parça metinleri) ve
`meds/src/data/summaries/kurul*.json` (ders özetleri). `core.textnorm.clean_text` uygulanır;
düzeltilmiş sürüm `MEDS_CORE_DIR/notes/` ve `MEDS_CORE_DIR/summaries/` altına yazılır.
Eski veri DEĞİŞTİRİLMEZ.
"""
from __future__ import annotations

from pathlib import Path

from .. import config
from ..core import store, textnorm


def _clean_notes_sources() -> list[Path]:
    base = config.DATABASE_DIR / "derived" / "clean_notes"
    return sorted(base.glob("*.jsonl")) if base.exists() else []


def ingest_notes(log=print) -> dict:
    """Temiz ders notu parçalarını yeniden düzeltip CORE/notes altına yazar."""
    config.ensure_core_dirs()
    files = _clean_notes_sources()
    total = 0
    for path in files:
        out: list[dict] = []
        for rec in store.iter_jsonl(path):
            raw = rec.get("metin") or rec.get("text") or ""
            clean = textnorm.clean_text(raw)
            out.append({
                "chunk_id": rec.get("chunk_id"),
                "source_id": rec.get("source_id"),
                "sayfa": rec.get("sayfa") or rec.get("page"),
                "metin": clean,
                "ozgun_hash": rec.get("ozgun_hash"),
                "duzeltildi": clean != raw,
                "pipeline_generation": config.PIPELINE_GENERATION,
            })
        if out:
            store.write_core_jsonl(config.NOTES_DIR / path.name, out, guard=True)
            total += len(out)
    log(f"ders notları: {len(files)} dosya, {total} parça düzeltildi → {config.NOTES_DIR}")
    return {"dosya": len(files), "parca": total}


def ingest_summaries(log=print) -> dict:
    """Ders özetlerini (kurul1..6.json) düzeltip CORE/summaries altına yazar."""
    config.ensure_core_dirs()
    base = config.MEDS_DIR / "src" / "data" / "summaries"
    files = sorted(base.glob("kurul*.json")) if base.exists() else []
    total = 0
    for path in files:
        data = store.read_json(path, []) or []
        out = []
        for item in data:
            if not isinstance(item, dict):
                continue
            content = item.get("content") or ""
            out.append({
                "id": item.get("id"),
                "kurul": item.get("kurul"),
                "committeeId": item.get("committeeId"),
                "discipline": item.get("discipline"),
                "title": textnorm.clean_text(item.get("title") or ""),
                "fileName": item.get("fileName"),
                "keyPoints": [textnorm.clean_text(k) for k in (item.get("keyPoints") or [])],
                "content": textnorm.clean_text(content),
                "charCount": len(content),
                "pipeline_generation": config.PIPELINE_GENERATION,
            })
        if out:
            store.write_core_json(config.SUMMARIES_DIR / path.name, out)
            total += len(out)
    log(f"ders özetleri: {len(files)} dosya, {total} özet düzeltildi → {config.SUMMARIES_DIR}")
    return {"dosya": len(files), "ozet": total}
