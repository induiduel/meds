"""s11 — Soru ↔ ders notu ilişkilendirme (kaynağın NERESİYLE eşleştiğini kaydeder).

Her soru için en iyi eşleşen ders notu parçalarını bulur ve kaydın içine yazar:
  `kaynak_baglari`: [{chunk_id, source_id, sayfa, skor, support_ratio, alinti}]
Böylece site, soruyu ilgili ders notu/slayt sayfasına yönlendirebilir. Deterministik (BM25).
"""
from __future__ import annotations

from ..core import match, store

MAX_LINKS = 3
MIN_LINK_SUPPORT = 0.35


def link_questions(records: list[dict], index=None, *, chunks_by_id: dict[str, dict] | None = None) -> dict:
    """Önce kanıt chunk'larından (hızlı, O(1)); kanıt yoksa ve index verilmişse BM25 ile arar."""
    by_id = chunks_by_id or {}
    counts = {"kayit": 0, "bagli": 0, "baglanti": 0}
    for rec in records:
        counts["kayit"] += 1
        links = []
        for cid in (rec.get("evidence") or []):
            chunk = by_id.get(cid)
            if not chunk:
                continue
            links.append({
                "chunk_id": cid,
                "source_id": chunk.get("source_id"),
                "sayfa": chunk.get("page"),
                "ders": chunk.get("ders"),
                "konu": chunk.get("konu"),
                "support_ratio": (rec.get("match") or {}).get("support_ratio"),
                "alinti": (chunk.get("text") or "")[:240],
            })
        if not links and index is not None:
            for hit in match.match_question(rec, index, k=MAX_LINKS):
                if (hit.get("support_ratio") or 0) < MIN_LINK_SUPPORT:
                    continue
                cid = hit.get("chunk_id")
                chunk = by_id.get(cid, {})
                links.append({
                    "chunk_id": cid, "source_id": hit.get("kaynak"), "sayfa": chunk.get("page"),
                    "ders": chunk.get("ders"), "konu": chunk.get("konu"),
                    "skor": hit.get("skor"), "support_ratio": hit.get("support_ratio"),
                    "alinti": (chunk.get("text") or "")[:240],
                })
        if links:
            rec["kaynak_baglari"] = links
            rec["kaynak_id"] = links[0]["source_id"]
            rec["kaynak_sayfa"] = links[0]["sayfa"]
            counts["bagli"] += 1
            counts["baglanti"] += len(links)
    return counts
