#!/usr/bin/env python3
"""Sözlük v2 kart doğrulayıcı (meds_temp/sozluk_v2/kartlar/*.jsonl).

HATA (birleştirmeyi durdurur): şema, kategori, alıntının ders notunda birebir bulunmaması,
yinelenen id/terim, sözlükte zaten var olan terim, iç içe derinlik > 3.
UYARI: kelime/madde sayısı sınır dışı.

Kullanım: python3 meds/scripts/sozluk_v2/dogrula.py [--dosya kartlar/x.jsonl]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from aday_uret import NOTLAR, ROOT, norm, sozlukte_olan  # noqa: E402

KART_DIR = ROOT / "meds_temp/sozluk_v2/kartlar"
RAPOR = ROOT / "meds_temp/sozluk_v2/dogrulama_raporu.json"
KATEGORI = {"hastalik", "ilac", "patojen", "patoloji", "genetik", "protein", "tani", "halk-sagligi", "terim"}


def duz(s: str) -> str:
    """Alıntı karşılaştırması: biçim işaretleri, boşluk ve büyük/küçük harf farkı yok sayılır."""
    s = re.sub(r"(==|\*\*|`|~~|</?[a-zA-Z][^>\n]*>)", "", s or "")
    s = s.replace("’", "'").replace("–", "-").replace("—", "-")
    return " ".join(norm_harf(s).split())


def norm_harf(s: str) -> str:
    return s.replace("İ", "i").replace("I", "ı").lower()


def kelime(s: str) -> int:
    return len(re.findall(r"[\wçğıöşüÇĞİÖŞÜ]+", s or ""))


def maddeler(items, derinlik=1):
    """(metin, derinlik) üretir."""
    for it in items or []:
        if isinstance(it, str):
            yield it, derinlik
        elif isinstance(it, dict):
            yield str(it.get("text") or ""), derinlik
            yield from maddeler(it.get("sub"), derinlik + 1)
        else:
            yield None, derinlik


def kart_metni(k: dict) -> str:
    parca = [k.get("definition") or ""]
    for s in (k.get("infoCard") or {}).get("sections") or []:
        parca += [s.get("title") or "", s.get("intro") or ""]
        parca += [t or "" for t, _ in maddeler(s.get("items"))]
    parca += list(k.get("examSpotPearls") or []) + list(k.get("pitfallsAndWarnings") or [])
    return " ".join(parca)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dosya", action="append")
    a = ap.parse_args()
    files = [Path(f) for f in a.dosya] if a.dosya else sorted(KART_DIR.glob("*.jsonl"))
    notlar = {p.name: duz(p.read_text()) for p in (NOTLAR / "notlar").glob("*.md")}
    have = sozlukte_olan(haric_v2=True)
    arsiv = ROOT / "meds_database_v2/sozluk_v2/bilgi_kartlari.json"
    birlesik = {c.get("id") for c in json.loads(arsiv.read_text()).get("kartlar", [])} if arsiv.exists() else set()
    seen_id, seen_term = {}, {}
    hatalar, uyarilar, kartlar = [], [], 0

    for f in files:
        for no, ln in enumerate(f.read_text().splitlines(), 1):
            if not ln.strip():
                continue
            yer = f"{f.name}:{no}"
            try:
                k = json.loads(ln)
            except json.JSONDecodeError as e:
                hatalar.append(f"{yer} JSON: {e}")
                continue
            kartlar += 1
            ad = k.get("term") or "?"
            yer = f"{yer} [{ad}]"
            H = lambda m: hatalar.append(f"{yer} {m}")  # noqa: E731
            U = lambda m: uyarilar.append(f"{yer} {m}")  # noqa: E731
            for alan in ("id", "term", "category", "subcategory", "discipline", "definition", "infoCard", "kaynaklar"):
                if not k.get(alan):
                    H(f"eksik alan: {alan}")
            if not str(k.get("id", "")).startswith("s2-"):
                H("id 's2-' ile başlamalı")
            if k.get("category") not in KATEGORI:
                H(f"geçersiz kategori: {k.get('category')}")
            if "›" not in str(k.get("subcategory", "")):
                U("alt sınıf '›' ile yol olarak yazılmalı")
            if k.get("id") in seen_id:
                H(f"yinelenen id ({seen_id[k['id']]})")
            seen_id[k.get("id")] = yer
            nt = norm(ad)
            if nt in seen_term:
                H(f"yinelenen terim ({seen_term[nt]})")
            seen_term[nt] = yer
            if k.get("id") not in birlesik and (nt in have or any(norm(x) in have for x in k.get("aliases") or [])):
                H("sözlükte zaten var (ad ya da eşanlamlı)")  # önceden birleştirilmiş kart kendini/başka kaynağı saymaz
            # bilgi kartı
            secs = (k.get("infoCard") or {}).get("sections") or []
            if not 1 <= len(secs) <= 3:
                H(f"bilgi kartı 1–3 bölüm olmalı ({len(secs)})")
            n_madde = 0
            for s in secs:
                for t, d in maddeler(s.get("items")):
                    if t is None or not str(t).strip():
                        H("boş/geçersiz madde")
                    if d > 3:
                        H("iç içe derinlik 3'ü aşıyor")
                    n_madde += 1
            if not 4 <= n_madde <= 22:
                U(f"madde sayısı {n_madde} (öneri 4–20, alt maddeler dahil)")
            w_def = kelime(k.get("definition"))
            if not 10 <= w_def <= 55:
                U(f"tanım {w_def} kelime (öneri 15–45)")
            w = kelime(kart_metni(k))
            if not 45 <= w <= 300:
                U(f"kart metni {w} kelime (öneri 50–260)")
            if len(k.get("examSpotPearls") or []) > 3 or len(k.get("pitfallsAndWarnings") or []) > 2:
                U("spot ≤3, uyarı ≤2 olmalı")
            # kaynak alıntıları
            ks = k.get("kaynaklar") or []
            if not 1 <= len(ks) <= 3:
                H(f"kaynak 1–3 olmalı ({len(ks)})")
            for r in ks:
                dosya = Path(str(r.get("dosya") or "")).name
                if dosya not in notlar:
                    H(f"kaynak dosyası yok: {r.get('dosya')}")
                    continue
                al = duz(r.get("alinti") or "")
                if kelime(al) < 4:
                    H("alıntı çok kısa")
                elif al not in notlar[dosya]:
                    H(f"alıntı ders notunda birebir yok: {r.get('alinti')[:80]!r}")

    rapor = {"kart": kartlar, "hata": len(hatalar), "uyari": len(uyarilar), "hatalar": hatalar, "uyarilar": uyarilar}
    RAPOR.write_text(json.dumps(rapor, ensure_ascii=False, indent=1))
    for m in hatalar:
        print("HATA ", m)
    for m in uyarilar:
        print("UYARI", m)
    print(f"{kartlar} kart · {len(hatalar)} HATA · {len(uyarilar)} UYARI")
    return 1 if hatalar else 0


if __name__ == "__main__":
    sys.exit(main())
