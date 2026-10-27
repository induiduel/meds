#!/usr/bin/env python3
"""Ders değerlendirme paketini girdilerden kurar (KURUL2_DERS_STANDARDI §2 aşama 5; LLM yok, yalnız birleştirme).

Girdiler (oturumda/alt ajanlarla hazırlanmış, her biri kendi doğrulamasından geçmiş):
  --notlar   öğrenci notu JSON listesi  [{s, tur, hedef, not?}]
  --hoca     hoca vurguları JSON (ders anahtarlı sözlük ya da liste)  [{t, s, tur, alinti, konu, guven, slayt_disi}]
  --cikmis   çıkmış eşleme JSON (ders anahtarlı)  [{id, s, seviye, kanit, kaynak, yil}]
  --taslak   ders işçisi taslağı (bilgi_havuzu.jsonl → atomik bilgi envanteri)
Çıktı: meds_database_v2/ders_bilgi/<ders>/degerlendirme/paket.json (+ cikmis_taslak.json: p/c metin bitince eklenir)
Bilgi paketleri: notu, çıkmışı ya da hoca vurgusu olan her sayfa; önem = dayanak çeşitliliği (1–3).
  .venv-ocr/bin/python scripts/ogrenci_drive/paket_kur.py --ders k2-03 --key <key> --konu "…" --brans "…" --hoca-adi "…" \\
      --pdf ORIJINAL.pdf --notlar … --hoca … --cikmis … --taslak …
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

import pymupdf

DEPO = Path(__file__).resolve().parents[3] / "meds_database_v2" / "ders_bilgi"
KATEGORI = {"spot": "clinical_note", "mekanizma": "pharmacodynamics", "tanim": "clinical_note", "hastalik": "disease",
            "bulgu": "symptom", "ilac": "drug", "tedavi": "drug", "yan_etki": "side_effect"}


def oku(p, ders=None):
    d = json.loads(Path(p).read_text(encoding="utf-8"))
    return d.get(ders, []) if isinstance(d, dict) and ders else d


def baslik(metin: str) -> str:
    satir = [x.strip() for x in metin.splitlines() if x.strip() and not re.match(r"^[-•\-–]+$", x.strip())]
    return re.sub(r"^Slayt \d+ – ", "", satir[0])[:80] if satir else ""


def main() -> int:
    ap = argparse.ArgumentParser()
    for a in ("ders", "key", "konu", "brans", "hoca-adi", "pdf", "notlar", "hoca", "cikmis", "taslak"):
        ap.add_argument(f"--{a}", required=a not in ("hoca",))
    a = ap.parse_args()
    doc = pymupdf.open(a.pdf)
    notlar = oku(a.notlar)
    for n in notlar:  # resim sayfasında metin yoksa hedef sayfa başlığı (doğrulayıcı resim ögesini böyle tanır)
        if not n.get("hedef"):
            n["hedef"], n["resim"] = baslik(doc[n["s"] - 1].get_text()) or "", True
    hoca = oku(a.hoca, a.ders) if a.hoca else []
    cik = oku(a.cikmis, a.ders)
    sayfa = defaultdict(lambda: {"not": [], "hoca": [], "cikmis": []})
    for n in notlar:
        sayfa[n["s"]]["not"].append(n)
    for h in hoca:
        sayfa[h["s"]]["hoca"].append(h)
    for c in cik:
        sayfa[c["s"]]["cikmis"].append(c)
    paketler = []
    for s in sorted(sayfa):
        v = sayfa[s]
        maddeler = []
        for n in v["not"]:
            m = n["hedef"] + (f" — öğrenci notu: {n['not']}" if n.get("not") else "")
            if m not in maddeler:
                maddeler.append(m)
        maddeler += [f"Hoca: {h['konu']}" for h in v["hoca"] if h.get("tur") == "vurgu"]
        maddeler += [f"Çıkmış ({c['seviye']}): {c['kanit']}" for c in v["cikmis"]]
        dayanak = [k for k, x in (("ogrenci_not", v["not"]), ("hoca", [h for h in v["hoca"] if h.get("tur") == "vurgu"]),
                                  ("cikmis", v["cikmis"])) if x]
        if not maddeler:
            continue
        paketler.append({"id": f"bp{len(paketler) + 1}", "s": [s], "baslik": baslik(doc[s - 1].get_text()) or f"Sayfa {s}",
                         "onem": min(3, len(dayanak) + (1 if len(v["not"]) >= 3 else 0)), "dayanak": dayanak, "maddeler": maddeler[:8]})
    atomlar = []
    for i, satir in enumerate((Path(a.taslak) / "bilgi_havuzu.jsonl").read_text(encoding="utf-8").splitlines()):
        if not satir.strip():
            continue
        b = json.loads(satir)
        k = b.get("kanit") or {}
        atomlar.append({"id": f"{a.ders}-a{i + 1:02d}", "kategori": KATEGORI.get(b.get("tur"), "clinical_note"),
                        "baslik": b.get("varlik") or "", "ifade": b.get("bilgi") or "", "s": k.get("sayfa"),
                        "kanit": k.get("alinti") or "", "iliski": b.get("iliski"), "hedef": b.get("hedef"),
                        "cikmis": [c["id"] for c in cik if c["s"] == k.get("sayfa")],
                        **({"gorsel": True} if k.get("sayfa") and len(doc[k["sayfa"] - 1].get_text().strip()) < 60 else {})})
    paket = {"surum": 1, "ders": a.ders, "key": a.key, "konu": a.konu, "brans": a.brans, "ogretim_uyesi": a.hoca_adi,
             "kaynaklar": {"orijinal_pdf": str(a.pdf), "sayfa": doc.page_count},
             "ogrenci_notlari": notlar, "hoca_vurgulari": hoca,
             "cikmis": {"kaynak": f"data/sesli_anlatim/cikmis_konum/{a.key}.json",
                        "not": "Ham sınav belgesinde bulunan sorular, slayt kanıtıyla elle doğrulandı (H83)."},
             "bilgi_paketleri": paketler,
             "atomik_bilgi_envanteri": {"not": "Her derste çıkarılır; quiz soruları yalnız Farmakoloji (kural 19).", "atomlar": atomlar}}
    hedef = DEPO / a.ders / "degerlendirme"
    hedef.mkdir(parents=True, exist_ok=True)
    (hedef / "paket.json").write_text(json.dumps(paket, ensure_ascii=False, indent=1), encoding="utf-8")
    (hedef / "cikmis_taslak.json").write_text(json.dumps(cik, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{a.ders}: {len(notlar)} not · {len(hoca)} hoca · {len(cik)} çıkmış · {len(paketler)} bilgi paketi · {len(atomlar)} atom")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
