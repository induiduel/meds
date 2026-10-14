#!/usr/bin/env python3
"""
Sağlık Bakanlığı sekmesi — resmî veri araştırma çıktısını uygulamaya taşır ve denetler (yerel, modelsiz).

Girdi (varsayılan: --kaynak klasörü): asi.json, anne_yenidogan.json, karabuk.json, turkiye.json — her biri
`kaynaklar` listesi + bölüm verisi (şema: docs/SAGLIK_BAKANLIGI_PLANI.md, bileşen türleri: src/components/saglik/saglikVeri.ts).

Yapılanlar:
  1. Kaynak URL'si devlet alan adında mı (.gov.tr, .edu.tr, .bel.tr, .tsk.tr) — değilse kaynak ve ona dayanan ögeler atılır.
  2. Aynı kimlik farklı dosyalarda farklı URL'yle geçiyorsa dosya önekiyle yeniden adlandırılır, başvurular güncellenir.
  3. `kaynak` alanı kaynak listesinde olmayan liste ögeleri atılır (kaynaksız sayı gösterilmez).
  4. src/data/saglik/kaynaklar.json (birleşik) + bölüm dosyaları yazılır; rapor stdout'a.

Kullanım: python3 scripts/saglik/birlestir.py --kaynak <araştırma klasörü> [--deneme]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

MEDS = Path(__file__).resolve().parents[2]
OUT = MEDS / "src" / "data" / "saglik"
DOSYALAR = {"asi": "asi.json", "anne_yenidogan": "anne_yenidogan.json", "karabuk": "karabuk.json", "turkiye": "turkiye.json"}
DEVLET = re.compile(r"(\.gov\.tr|\.edu\.tr|\.bel\.tr|\.tsk\.tr|\.pol\.tr|\.k12\.tr)$", re.I)


def devlet_mi(url: str) -> bool:
    try:
        h = urlparse(url).hostname or ""
    except ValueError:
        return False
    return bool(DEVLET.search(h))


def yeniden_adlandir(x, harita: dict[str, str]):
    if isinstance(x, dict):
        return {k: (harita.get(v, v) if k == "kaynak" and isinstance(v, str) else yeniden_adlandir(v, harita)) for k, v in x.items()}
    if isinstance(x, list):
        return [yeniden_adlandir(v, harita) for v in x]
    return x


def kaynak_ayir(x, gecerli: set[str]):
    """'a; b, c' gibi birleşik kaynak alanını ilk geçerli kimlik + ek_kaynaklar'a ayırır; kimlik olmayan sözcükler düşer."""
    if isinstance(x, list):
        return [kaynak_ayir(v, gecerli) for v in x]
    if not isinstance(x, dict):
        return x
    d = {k: kaynak_ayir(v, gecerli) for k, v in x.items()}
    k = d.get("kaynak")
    if isinstance(k, str) and k not in gecerli and re.search(r"[;,]", k):
        parcalar = [t.strip() for t in re.split(r"[;,]", k) if t.strip() in gecerli]
        if parcalar:
            d["kaynak"] = parcalar[0]
            ek = [e for e in (d.get("ek_kaynaklar") or []) if e in gecerli]
            d["ek_kaynaklar"] = list(dict.fromkeys(parcalar[1:] + ek))
            if not d["ek_kaynaklar"]:
                del d["ek_kaynaklar"]
    return d


def temizle(x, gecerli: set[str], atilan: list[str], yol: str = ""):
    """Listelerde kaynağı geçersiz olan sözlük ögelerini atar; tekil sözlükte geçersiz kaynağı siler."""
    if isinstance(x, list):
        out = []
        for i, v in enumerate(x):
            if isinstance(v, dict) and isinstance(v.get("kaynak"), str) and v["kaynak"] not in gecerli:
                atilan.append(f"{yol}[{i}] kaynak={v['kaynak']}")
                continue
            out.append(temizle(v, gecerli, atilan, f"{yol}[{i}]"))
        return out
    if isinstance(x, dict):
        d = {}
        for k, v in x.items():
            if k == "kaynak" and isinstance(v, str) and v not in gecerli:
                atilan.append(f"{yol}.kaynak={v} (alan silindi)")
                continue
            d[k] = temizle(v, gecerli, atilan, f"{yol}.{k}")
        return d
    return x


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kaynak", required=True, type=Path)
    ap.add_argument("--deneme", action="store_true", help="yazmadan rapor ver")
    a = ap.parse_args()

    tum_kaynak: dict[str, dict] = {}
    veriler: dict[str, dict] = {}
    for ad, dosya in DOSYALAR.items():
        p = a.kaynak / dosya
        if not p.exists():
            print(f"[yok] {dosya} — boş yazılacak")
            veriler[ad] = {}
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        harita: dict[str, str] = {}
        for k in d.get("kaynaklar", []):
            kid = k.get("id")
            if not kid or not k.get("url"):
                continue
            # Aynı belge (aynı URL) başka dosyada başka kimlikle varsa o kimliğe bağlanır
            ayni = next((x for x in tum_kaynak.values() if x.get("url") == k.get("url") and x["id"] != kid), None)
            if ayni:
                harita[kid] = ayni["id"]
                continue
            if kid in tum_kaynak and tum_kaynak[kid].get("url") != k.get("url"):
                yeni = f"{ad}-{kid}"
                harita[kid] = yeni
                k = {**k, "id": yeni}
            tum_kaynak[k["id"]] = k
        d = yeniden_adlandir(d, harita)
        d.pop("kaynaklar", None)
        veriler[ad] = d

    gecersiz = {kid for kid, k in tum_kaynak.items() if not devlet_mi(k["url"])}
    for kid in sorted(gecersiz):
        print(f"[devlet dışı kaynak atıldı] {kid}: {tum_kaynak[kid]['url']}")
        del tum_kaynak[kid]
    gecerli = set(tum_kaynak)

    kullanilan: set[str] = set()

    def topla(x):
        if isinstance(x, dict):
            if isinstance(x.get("kaynak"), str):
                kullanilan.add(x["kaynak"])
            for v in x.values():
                topla(v)
        elif isinstance(x, list):
            for v in x:
                topla(v)

    for ad, d in veriler.items():
        atilan: list[str] = []
        dogrulanamayan = d.pop("dogrulanamayan", [])
        d = kaynak_ayir(d, gecerli)
        d = temizle(d, gecerli, atilan, ad)
        if dogrulanamayan:
            d["dogrulanamayan"] = dogrulanamayan
        veriler[ad] = d
        topla(d)
        for x in atilan:
            print(f"[kaynaksız öge atıldı] {x}")

    kullanilmayan = sorted(gecerli - kullanilan)
    if kullanilmayan:
        print(f"[bilgi] başvurulmayan {len(kullanilmayan)} kaynak: {', '.join(kullanilmayan[:12])}{'…' if len(kullanilmayan) > 12 else ''}")

    print(f"kaynak: {len(tum_kaynak)} · " + " · ".join(f"{k}: {len(json.dumps(v))//1024} KB" for k, v in veriler.items()))
    if a.deneme:
        return 0
    OUT.mkdir(parents=True, exist_ok=True)
    kaynaklar = sorted(tum_kaynak.values(), key=lambda k: k["id"])
    (OUT / "kaynaklar.json").write_text(json.dumps({"guncelleme": date.today().isoformat(), "kaynaklar": kaynaklar}, ensure_ascii=False, indent=1), encoding="utf-8")
    for ad, dosya in DOSYALAR.items():
        (OUT / dosya).write_text(json.dumps(veriler[ad], ensure_ascii=False, indent=1), encoding="utf-8")
    print("yazıldı:", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
