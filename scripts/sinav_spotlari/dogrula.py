#!/usr/bin/env python3
"""Sınav spotları doğrulayıcı (meds_temp/sinav_spotlari/spotlar/*.jsonl).

HATA: şema, kategori, alıntının ders notunda birebir bulunmaması, yinelenen id.
UYARI: ders başına spot sayısı 15–35 dışı, uzun spot, cevap spotta yok.
Kullanım: python3 meds/scripts/sinav_spotlari/dogrula.py [--dosya spotlar/10.jsonl]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
NOTLAR = ROOT / "meds_database_v2/ders_notlari_k1/notlar"
SPOT_DIR = ROOT / "meds_temp/sinav_spotlari/spotlar"
KATEGORI = {"en_sik", "karakteristik", "sayi", "eslesme", "tani_tedavi", "mekanizma", "tuzak", "siniflama"}


def norm_harf(s: str) -> str:
    return s.replace("İ", "i").replace("I", "ı").lower()


def duz(s: str) -> str:
    s = re.sub(r"(==|\*\*|`|~~|</?[a-zA-Z][^>\n]*>)", "", s or "")
    s = s.replace("’", "'").replace("–", "-").replace("—", "-").replace("|", " ")
    return " ".join(norm_harf(s).split())


def notlar() -> dict[int, tuple[str, str]]:
    out = {}
    for p in NOTLAR.glob("*.md"):
        m = re.match(r"(\d+)_", p.name)
        if m:
            out[int(m.group(1))] = (p.name, duz(p.read_text()))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dosya", action="append")
    a = ap.parse_args()
    files = [Path(f) for f in a.dosya] if a.dosya else sorted(SPOT_DIR.glob("*.jsonl"))
    nt = notlar()
    hatalar, uyarilar, seen, toplam = [], [], set(), 0
    for f in files:
        sayi = 0
        for no, ln in enumerate(f.read_text().splitlines(), 1):
            if not ln.strip():
                continue
            yer = f"{f.name}:{no}"
            try:
                s = json.loads(ln)
            except json.JSONDecodeError as e:
                hatalar.append(f"{yer} JSON: {e}")
                continue
            sayi += 1
            sid = s.get("id")
            if not sid or sid in seen:
                hatalar.append(f"{yer} id boş/yinelenen: {sid}")
            seen.add(sid)
            if s.get("kategori") not in KATEGORI:
                hatalar.append(f"{yer} kategori: {s.get('kategori')}")
            if s.get("onem") not in (1, 2, 3):
                hatalar.append(f"{yer} onem: {s.get('onem')}")
            for alan in ("baslik", "spot"):
                if not str(s.get(alan) or "").strip():
                    hatalar.append(f"{yer} {alan} boş")
            if s.get("kategori") == "tuzak" and not str(s.get("tuzak") or "").strip():
                hatalar.append(f"{yer} tuzak kategorisinde 'tuzak' boş")
            if not isinstance(s.get("maddeler", []), list):
                hatalar.append(f"{yer} maddeler liste değil")
            k = s.get("karsilastir")
            if k:
                bas = k.get("basliklar") or []
                for r in k.get("satirlar") or []:
                    if len(r) != len(bas) + 1:
                        hatalar.append(f"{yer} karsilastir satır uzunluğu")
            dn = s.get("ders_no")
            if dn not in nt:
                hatalar.append(f"{yer} ders_no yok: {dn}")
                continue
            kay = s.get("kaynak") or []
            if not kay:
                hatalar.append(f"{yer} kaynak yok")
            for q in kay:
                al = duz(q.get("alinti") or "")
                if len(al.split()) < 3:
                    hatalar.append(f"{yer} alıntı çok kısa: {q.get('alinti')}")
                elif al not in nt[dn][1]:
                    hatalar.append(f"{yer} alıntı notta yok: {q.get('alinti')}")
            if len((s.get("spot") or "").split()) > 60:
                uyarilar.append(f"{yer} spot uzun")
            c = duz(s.get("cevap") or "")
            if c and c not in duz(" ".join([s.get("spot") or ""] + [str(m) for m in s.get("maddeler") or []] + [s.get("baslik") or ""])):
                uyarilar.append(f"{yer} cevap spot/maddelerde birebir geçmiyor")
        toplam += sayi
        if not 15 <= sayi <= 40:
            uyarilar.append(f"{f.name}: {sayi} spot")
    print(f"{len(files)} dosya, {toplam} spot, {len(hatalar)} HATA, {len(uyarilar)} UYARI")
    for h in hatalar[:200]:
        print("HATA", h)
    for u in uyarilar[:60]:
        print("UYARI", u)
    return 1 if hatalar else 0


if __name__ == "__main__":
    sys.exit(main())
