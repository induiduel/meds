#!/usr/bin/env python3
"""Ders değerlendirme paketi kapısı (orijinal PDF + öğrenci notu + hoca sesi, kural 21; 2026-10-27).

  .venv-ocr/bin/python scripts/ogrenci_drive/degerlendirme_dogrula.py <ders> --pdf ORIJINAL.pdf

HATA:  öğrenci notu / bilgi atomu kanıtı slaytta birebir yok · çıkmış soru bankada yok ya da elle doğrulanmamış ·
       çıkmış kanıtı slaytta yok · slaytta geçen kısaltmanın sözlükte açılımı yok · hoca vurgusunda zaman/sayfa eksik
UYARI: sayfasında hiç bilgi paketi olmayan slayt (kapak hariç)
LLM yok; yalnız metin karşılaştırması.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "sesli_anlatim"))
import kisaltma_sozlugu as KS  # noqa: E402  (kısaltma adayı kuralı tek kaynak)

MEDS = Path(__file__).resolve().parents[2]
DEPO = MEDS.parent / "meds_database_v2" / "ders_bilgi"


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s).replace("İ", "i").replace("I", "ı").lower()
    s = re.sub(r"[«»“”\"'’→]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("ders")
    ap.add_argument("--pdf", required=True)
    a = ap.parse_args()
    paket = json.loads((DEPO / a.ders / "degerlendirme" / "paket.json").read_text(encoding="utf-8"))
    sayfa = {i + 1: norm(p.get_text()) for i, p in enumerate(pymupdf.open(a.pdf))}
    hata, uyari = [], []

    def slaytta(s: int, metin: str) -> bool:
        return norm(metin) in sayfa.get(s, "")

    for n in paket["ogrenci_notlari"]:
        if not slaytta(n["s"], n["hedef"]):
            hata.append(f"öğrenci notu s{n['s']}: hedef slaytta yok → {n['hedef'][:60]}")
    for at in paket["atomik_bilgi_envanteri"]["atomlar"]:
        if not slaytta(at["s"], at["kanit"]):
            hata.append(f"atom {at['id']}: kanıt s{at['s']}'de yok → {at['kanit'][:60]}")

    banka = json.loads((MEDS / "src/data/pastQuestions.json").read_text(encoding="utf-8"))
    banka = {q["id"] for q in (banka if isinstance(banka, list) else banka["questions"])}
    ck = json.loads((MEDS / paket["cikmis"]["kaynak"]).read_text(encoding="utf-8"))
    for q in ck["q"]:
        if q["id"] not in banka:
            hata.append(f"çıkmış {q['id']}: bankada yok")
        if not q.get("dogrulandi") or not q.get("s"):
            hata.append(f"çıkmış {q['id']}: elle doğrulanmamış / slayt yok")
        elif not slaytta(q["s"], q["kanit"].split(" (")[0].split(" → ")[0]):
            hata.append(f"çıkmış {q['id']}: kanıt s{q['s']}'de yok")
    for at in paket["atomik_bilgi_envanteri"]["atomlar"]:
        for i in at.get("cikmis", []):
            if i not in banka:
                hata.append(f"atom {at['id']}: çıkmış {i} bankada yok")

    kis = json.loads((MEDS / "src/data/kisaltma_sozluk.json").read_text(encoding="utf-8"))
    for s, m in sayfa.items():
        for k in set(re.findall(r"(?<![\wçğıöşü])([A-ZÇĞİÖŞÜ]{2,5})(?![\wçğıöşü])", pymupdf.open(a.pdf)[s - 1].get_text())):
            if k not in kis and KS.kisaltma_mi(k):
                hata.append(f"s{s}: kısaltma '{k}' sözlükte yok")
    for v in paket.get("hoca_vurgulari", []):
        if not (v.get("t") is not None and v.get("s") and v.get("alinti")):
            hata.append(f"hoca vurgusu eksik alan: {v}")
    kapsanan = {s for b in paket["bilgi_paketleri"] for s in b["s"]}
    for s in sayfa:
        if s > 1 and s not in kapsanan:
            uyari.append(f"s{s}: bilgi paketi yok")

    for x in hata:
        print("HATA ", x)
    for x in uyari:
        print("UYARI", x)
    print(f"{a.ders}: {len(hata)} HATA · {len(uyari)} UYARI")
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main())
