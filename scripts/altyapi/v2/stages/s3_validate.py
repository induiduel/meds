"""s3 — Doğrulama: kayıt bazlı issues/severity uygula ve durum ataması yap.

Bloğlayıcı sorun varsa durum `needs_fix`; aksi halde `raw` (doğrulanmamış). Hiçbir kayıt SİLİNMEZ.
"""
from __future__ import annotations

from ..core import validate


def validate_records(records: list[dict]) -> dict:
    """Her kayda 'issues' ve 'status' yazar; özet sayımları döndürür."""
    counts = {"kayit": 0, "blocking": 0, "review": 0, "ok": 0}
    for rec in records:
        result = validate.inspect_question(rec)
        rec["issues"] = result.issues
        if result.blocking:
            rec["status"] = "needs_fix"
            counts["blocking"] += 1
        else:
            if rec.get("status") in (None, "raw", "needs_fix"):
                rec["status"] = "raw"
            counts["review" if result.review else "ok"] += 1
        counts["kayit"] += 1
    return counts
