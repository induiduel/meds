#!/usr/bin/env python3
"""Alternatif soru çözücü — ön yüz paketi.

Girdi : meds/data/patoloji_cozucu_alt/{metin,ses} + meds/data/patoloji_cozucu/ses
Çıktı : meds/src/data/patoloji_cozucu_alt/index.json ve <kod>.json
        (uygulama bunları import.meta.glob ile paketler; ses /api/patoloji-cozucu-alt/ses/<kod>/<no>.mp3)
"""
from __future__ import annotations

import json
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
KOK = MEDS / "data/patoloji_cozucu_alt"
STD_SES = MEDS / "data/patoloji_cozucu/ses"
HEDEF = MEDS / "src/data/patoloji_cozucu_alt"
KAYNAK_INDEX = MEDS / "src/data/patoloji_cozucu/index.json"
HARF = "ABCDE"


def bolum_zamanlari(sure: float, no: int, std_kayit: dict) -> list[float]:
    """MP3 içindeki 14 bölümün (kök, A..E şık, giriş, A..E açıklama, cevap, özet) kümülatif bitiş saniyeleri (ilk 13 sınır)."""
    if sure <= 0:
        return []
    ad = str(no)
    q_rec = std_kayit.get(f"q-{ad}", {})
    q_z = q_rec.get("zaman", [])
    if len(q_z) == 6:
        d_q = [max(0.5, (z[1] - z[0]) + 0.45) for z in q_z]
    else:
        d_q = [5.0, 1.2, 1.2, 1.2, 1.2, 1.2]

    d_giris = 1.8
    d_acik = [max(1.5, std_kayit.get(f"s-{ad}-{h}", {}).get("sure", 4.5) - 0.12) for h in HARF]
    c_rec = std_kayit.get(f"c-{ad}", {})
    c_z = c_rec.get("zaman", [])
    d_cevap = max(1.2, (c_z[0][1] - c_z[0][0]) + 0.45) if c_z else 2.2
    d_ozet = max(2.0, (c_rec.get("sure", 8.0) - 0.12) - d_cevap)

    parcalar = [*d_q, d_giris, *d_acik, d_cevap, d_ozet]
    toplam = sum(parcalar)
    oran = sure / toplam if toplam > 0 else 1.0
    kum = 0.0
    sinirlar: list[float] = []
    for p in parcalar[:-1]:
        kum += p * oran
        sinirlar.append(round(kum, 1))
    return sinirlar


def main() -> None:
    HEDEF.mkdir(parents=True, exist_ok=True)
    no_by_kod = {
        d["kod"]: d.get("no")
        for d in json.loads(KAYNAK_INDEX.read_text(encoding="utf-8"))["dersler"]
    }
    dersler = []
    for p in sorted((KOK / "metin").glob("*.json")):
        if p.name.startswith("tum_"):
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        kod = d["kod"]
        ders_no = d.get("no") or no_by_kod.get(kod) or int("".join(c for c in kod if c.isdigit()) or 0)
        kayit_p = KOK / "ses" / kod / "kayit.json"
        kayit = json.loads(kayit_p.read_text(encoding="utf-8")) if kayit_p.exists() else {}
        std_kayit_p = STD_SES / kod / "kayit.json"
        std_kayit = json.loads(std_kayit_p.read_text(encoding="utf-8")) if std_kayit_p.exists() else {}

        sorular = []
        for s in d["sorular"]:
            k = kayit.get(str(s["no"]), {})
            sure = k.get("sure", 0)
            zaman = bolum_zamanlari(sure, s["no"], std_kayit)
            sorular.append({
                "no": s["no"],
                "tur": s["tur"],
                **({"zorluk": s["zorluk"]} if s.get("zorluk") else {}),
                **({"sinav": s["sinav"]} if s.get("sinav") else {}),
                "soru": s["soru"],
                "secenekler": s["secenekler"],
                "dogru": s["dogru"],
                **({"ipucu": s["ipucu"]} if s.get("ipucu") else {}),
                "giris": s["giris"],
                "aciklamalar": s["aciklamalar"],
                "ozet": s["ozet"],
                **({"sayfa": s["sayfa"]} if s.get("sayfa") else {}),
                "mp3": f"{s['no']}.mp3",
                "h": k.get("h", ""),
                "sure": sure,
                **({"zaman": zaman} if zaman else {}),
            })
        ders = {
            "kod": kod,
            "no": ders_no,
            "baslik": d["baslik"],
            "sorular": sorular,
        }
        (HEDEF / f"{kod}.json").write_text(json.dumps(ders, ensure_ascii=False), encoding="utf-8")
        dersler.append({
            "kod": kod,
            "no": ders_no,
            "baslik": d["baslik"],
            "soru": len(sorular),
            "ornek": sum(1 for s in sorular if s["tur"] == "ornek"),
            "cikmis": sum(1 for s in sorular if s["tur"] == "cikmis"),
            "sure": round(sum(s["sure"] for s in sorular)),
        })

    dersler.sort(key=lambda x: (x["no"], x["kod"]))
    index = {"surum": "patoloji-cozucu-alt-2", "dersler": dersler}
    (HEDEF / "index.json").write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8")
    print(f"{len(dersler)} ders, {sum(d['soru'] for d in dersler)} soru → {HEDEF}")


if __name__ == "__main__":
    main()
