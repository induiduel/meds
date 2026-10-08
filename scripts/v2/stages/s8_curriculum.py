"""s8 — Müfredat/kazanım eşleme aşaması.

Her soruya Ders → Konu → Kazanım bağlar, metadata ve tıbbi terimleri yazar. Daha önce ders/konu
atanmamışsa doldurur; mevcut değeri (varsa) koruyarak yalnız boşlukları tamamlar.
"""
from __future__ import annotations

from ..core import curriculum


def apply_curriculum(records: list[dict]) -> dict:
    counts = {"kayit": 0, "eslesen": 0, "konu": 0, "kazanim": 0, "ders_dolduruldu": 0, "terimli": 0}
    for rec in records:
        counts["kayit"] += 1
        if rec.get("ders"):
            rec["ders"] = curriculum.normalize_ders(rec["ders"])
        m = curriculum.map_question(rec) or {}
        rec["mufredat"] = m
        if m:
            counts["eslesen"] += 1
        # ders yalnız boşsa doldurulur (yoldan gelen ders güvenilir kabul edilir)
        if not rec.get("ders") and m.get("ders"):
            rec["ders"] = m["ders"]
            counts["ders_dolduruldu"] += 1
        # konu/kazanım her turda yeniden hesaplanır (eski/yanlış değeri temizler)
        rec["konu"] = m.get("konu")
        rec["kazanim"] = m.get("kazanim")
        if m.get("terimler"):
            rec["terimler"] = m["terimler"]
        if m.get("konu"):
            counts["konu"] += 1
        if m.get("kazanim"):
            counts["kazanim"] += 1
        if m.get("terimler"):
            counts["terimli"] += 1
    return counts
