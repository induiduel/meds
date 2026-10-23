"""Sesli sınav asistanı görevlerinin ortak katmanı (asistan_iskelet + asistan_nokta).

W = ders zinciri çalışma klasörü; plan W/asistan/plan/<kod>.json (scripts/spot_cozucu/asistan_plan.py üretir), çıktı
W/asistan/cikti/<kod>.json (resmî `asistan_dogrula.py` 0 HATA). Görev ara çıktıları W/gorev/<kod>/asistan_*.json.
"""
from __future__ import annotations

import sys
from pathlib import Path

from .. import cekirdek as c

NOKTA_PARTI, SORU_PARTI = 2, 2   # 2026-10-23: 4 soruluk partide açıklamalar kısalıyordu (36 açıklama tek çıktıda)


def ad():
    """Resmî asistan doğrulayıcısı (cift, check) — 2026-10-23'te işleve ayrıldı, CLI çıktısı birebir aynı."""
    sys.path.insert(0, str(c.KOK / "scripts" / "spot_cozucu"))
    import asistan_dogrula
    return asistan_dogrula


def plan(W: Path, kod: str) -> dict:
    p = W / "asistan" / "plan" / f"{kod}.json"
    d = c.oku(p)
    if not d:
        raise SystemExit(f"asistan planı yok: {p} (scripts/spot_cozucu/asistan_plan.py)")
    return d


def iskelet(W: Path, kod: str) -> dict:
    d = c.oku(W / "gorev" / kod / "asistan_iskelet.json")
    if not d:
        raise SystemExit(f"{kod}: önce asistan_iskelet görevi")
    return d


def son_noktalar(W: Path, kod: str) -> list[dict]:
    """İskeletin son düzeni: [{id, bolum, sorular:[anahtar…]}] (taşınan sorular hedef noktada)."""
    P = plan(W, kod)
    PN = {n["id"]: n for n in P["noktalar"]}
    ik = iskelet(W, kod)
    out = []
    for bi, b in enumerate(ik["bolumler"]):
        for nid in b["noktalar"]:
            out.append({"id": nid, "bolum": bi, "sorular": [s["anahtar"] for s in PN[nid]["sorular"]
                                                            if s["anahtar"] not in ik["soru_tasima"]]})
    yer = {n["id"]: n for n in out}
    for k, hedef in ik["soru_tasima"].items():
        yer[hedef]["sorular"].append(k)
    return out


def yapilan(W: Path, kod: str) -> set[str]:
    out = set()
    for p in sorted((W / "gorev" / kod).glob("asistan_nokta_*.json")):
        out |= {n["id"] for n in (c.oku(p) or {}).get("noktalar", [])}
    return out


def bekleyen_parti(W: Path, kod: str) -> list[dict]:
    """Henüz kabul edilmemiş noktalardan belirlenimci ilk parti: ≤3 nokta ve ≤4 soru (çok sorulu nokta tek başına)."""
    bitti = yapilan(W, kod)
    parti, soru = [], 0
    for n in son_noktalar(W, kod):
        if n["id"] in bitti:
            continue
        if parti and (len(parti) >= NOKTA_PARTI or soru + len(n["sorular"]) > SORU_PARTI):
            break
        parti.append(n); soru += len(n["sorular"])
    return parti
