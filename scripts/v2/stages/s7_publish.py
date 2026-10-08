"""s7 — Yayına alma: yalnızca şema-geçerli kayıtları izole CORE_DIR'e yazar (idempotent).

- Her kayıt şemaya karşı doğrulanır; geçersizler atlanır (sessizce yazılmaz).
- Aynı `question_id`/`chunk_id`/`source_id` ile ikinci kez gelirse ÜZERİNE YAZAR (güncelleme),
  yeni kopya üretmez → tekrar yok.
- Boş sonuçla dolu dosya ezilmez (store guard).
"""
from __future__ import annotations

from .. import config
from ..core import schema, store


# Yeniden işleme sırasında KORUNACAK zenginleştirme alanları (yeni kayıt boşsa eskiden alınır).
_PRESERVE = (
    "answer", "explanation", "answer_kaynak", "konu", "kazanim", "terimler", "mufredat",
    "kaynak_baglari", "kaynak_id", "kaynak_sayfa", "tibbi_dogrulama", "enrichment",
    "support_ratio", "match", "seen_in",
)


def _merge_jsonl(path, new_records: list[dict], key: str, preserve: bool = True) -> dict:
    existing = {r.get(key): r for r in store.read_jsonl(path) if r.get(key)}
    added = updated = 0
    for rec in new_records:
        rec.setdefault("pipeline_generation", config.PIPELINE_GENERATION)
        rec.setdefault("created_at", store.now_iso())
        k = rec.get(key)
        old = existing.get(k)
        if old:
            updated += 1
            if preserve:
                # Yeni kayıt zenginleştirme alanını taşımıyorsa eskisini koru (cevap/kazanım/link kaybolmasın).
                for field_name in _PRESERVE:
                    if not rec.get(field_name) and old.get(field_name):
                        rec[field_name] = old[field_name]
        else:
            added += 1
        existing[k] = rec
    store.write_core_jsonl(path, list(existing.values()), guard=True)
    return {"added": added, "updated": updated, "total": len(existing)}


def publish_questions(records: list[dict], dataset: str = "ingest", preserve: bool = True) -> dict:
    config.ensure_core_dirs()
    valid, invalid = [], 0
    for rec in records:
        if schema.is_valid(rec, "question"):
            valid.append(rec)
        else:
            invalid += 1
    if not valid:
        return {"added": 0, "updated": 0, "total": 0, "invalid": invalid, "yazildi": False}
    stats = _merge_jsonl(config.QUESTIONS_DIR / f"{dataset}.jsonl", valid, "question_id", preserve=preserve)
    stats["invalid"] = invalid
    stats["yazildi"] = True
    return stats


def publish_chunks(chunks: list[dict]) -> dict:
    config.ensure_core_dirs()
    by_source: dict[str, list[dict]] = {}
    for c in chunks:
        if schema.is_valid(c, "chunk"):
            by_source.setdefault(c["source_id"], []).append(c)
    total = 0
    for sid, recs in by_source.items():
        stats = _merge_jsonl(config.CHUNKS_DIR / f"{sid}.jsonl", recs, "chunk_id")
        total += stats["added"]
    return {"kaynak": len(by_source), "eklenen": total}


def publish_sources(sources: list[dict]) -> dict:
    config.ensure_core_dirs()
    written = 0
    for src in sources:
        if not schema.is_valid(src, "source"):
            continue
        src.setdefault("created_at", store.now_iso())
        store.write_core_json(config.SOURCES_DIR / f"{src['source_id']}.json", src)
        written += 1
    return {"yazilan": written}


def update_katalog(question_count: int, chunk_count: int, source_count: int, dataset: str = "ingest") -> None:
    for entry in (
        {"ad": f"v2_sorular_{dataset}", "yol": str(config.QUESTIONS_DIR / f'{dataset}.jsonl'),
         "tur": "jsonl", "aciklama": "Core v2 ingest soruları", "guvenilirlik": "aday",
         "uretici": config.PIPELINE_GENERATION, "kayit": question_count, "var": True},
        {"ad": "v2_ders_parcalari", "yol": str(config.CHUNKS_DIR), "tur": "jsonl_dizin",
         "aciklama": "Core v2 ingest parçaları", "guvenilirlik": "kaynak",
         "uretici": config.PIPELINE_GENERATION, "kayit": chunk_count, "var": True},
        {"ad": "v2_ders_kaynaklari", "yol": str(config.SOURCES_DIR), "tur": "json_dizin",
         "aciklama": "Core v2 ingest kaynakları", "guvenilirlik": "kaynak",
         "uretici": config.PIPELINE_GENERATION, "kayit": source_count, "var": True},
    ):
        store.update_katalog(entry)
