"""s5 — Eşleştirme: soruları kaynak parçalarıyla (BM25 [+ opsiyonel CPU e5]) ilişkilendirir.

Kanıt yalnızca yeterli destek varsa bağlanır; güven katmanı (yuksek/orta/dusuk) kayda işlenir.
Hibrit vektör araması `MEDS_V2_VECTOR=1` ile açılır; kapalıysa yalnız BM25 (GPU yok).
"""
from __future__ import annotations

from .. import config
from ..core import match, store, vector

MIN_SUPPORT_FOR_EVIDENCE = 0.5


def build_index(chunks: list[dict]):
    docs = [{"id": c.get("chunk_id"), "text": c.get("text") or "", "source_id": c.get("source_id")} for c in chunks]
    return vector.build_index(docs)


def load_existing_chunks() -> list[dict]:
    """Mevcut parçaları (varsa CORE, yoksa eski meds_database) SALT OKUNUR yükler."""
    chunks: list[dict] = []
    for d in (config.CHUNKS_DIR, config.DATABASE_DIR / "chunks"):
        if d.exists():
            for path in sorted(d.glob("*.jsonl")):
                chunks.extend(store.read_jsonl(path))
            break
    return chunks


def match_records(records: list[dict], index, *, k: int = 5) -> dict:
    counts = {"eslesen": 0, "kanit_bagli": 0, "aday": 0, "yuksek": 0, "orta": 0, "dusuk": 0}
    for rec in records:
        hits = match.match_question(rec, index, k=k)
        if not hits:
            continue
        best = hits[0]
        guven = best.get("guven") or match.guven_tier(best.get("support_ratio"))
        counts[guven] = counts.get(guven, 0) + 1
        rec["match"] = {
            "durum": "aday",
            "guven": guven,
            "kaynak": best.get("kaynak"),
            "kanit_chunk": best.get("chunk_id"),
            "skor": round(best.get("skor", 0.0), 4),
            "marj": best.get("marj"),
            "support_ratio": best.get("support_ratio"),
            "adaylar": [{"chunk_id": h.get("chunk_id"), "skor": round(h.get("skor", 0.0), 4),
                         "support_ratio": h.get("support_ratio")} for h in hits],
        }
        counts["eslesen"] += 1
        if (best.get("support_ratio") or 0) >= MIN_SUPPORT_FOR_EVIDENCE and best.get("chunk_id"):
            rec["match"]["durum"] = "kanitli"
            if not rec.get("evidence"):
                rec["evidence"] = [best["chunk_id"]]
            rec["support_ratio"] = best.get("support_ratio")
            counts["kanit_bagli"] += 1
        else:
            counts["aday"] += 1
    return counts
