#!/usr/bin/env python3
"""Metin takipçisi kapısı (KURUL2_DERS_STANDARDI §5, kullanıcı kararı 2026-10-27: "metin takipçisinin doğru çalıştığından
daha garanti yollarla emin ol"). Yayından önce 0 HATA; LLM yok, yalnız veri tutarlılığı.

  T1  Kelime zamanı: paragraf başına zaman sayısı = ekrandaki kelime sayısı (istemci \\S+ ile böler); zamanlar artan.
  T2  Paragraflar arası: her paragrafın ilk kelimesi bir öncekinin son kelimesinden sonra; son zaman ses süresinin içinde.
  T3  Cümle zamanı: paragraf başına iç sınır sayısı = cümle sayısı − 1 (pdf_isaret.cumle_sonlari); sınırlar artan.
  T4  Kelime zamanı yoksa: cümle sınırları kelime akışıyla uyumlu (±0,6 sn). Kelime zamanı geçerliyse istemci cümle
      başlarını ondan türetir (canliDersStore.ts), cumle_zaman kullanılmaz.
  T6  --api verilirse: canlı /api/canli-ders/<key> varsayılan sesi için kelimeZaman'ı paragraf başına eksiksiz sunuyor.
  T5  PDF işareti: her cümlenin işareti var; çapa varsa işaretin sayfası çapadaki sayfa; "sayfa"/boş işaret oranı ≤ %5.
Kullanım: .venv-ocr/bin/python scripts/sesli_anlatim/takip_kapisi.py <key> [--kok data/sesli_anlatim] [--varyant ID]
Çıkış: 0 geçti, 1 HATA.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "arsiv_25_26"))
from pdf_isaret import cumle_sonlari  # noqa: E402
from arsiv_yayinla import metin_paragraflari  # noqa: E402

PAY = 0.6


def oku(p: Path):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("key")
    ap.add_argument("--kok", default=str(Path(__file__).resolve().parents[2] / "data" / "sesli_anlatim"))
    ap.add_argument("--varyant")
    ap.add_argument("--sure", type=float, help="ses süresi (sn); verilmezse kayit.json'dan")
    ap.add_argument("--api", help="canlı API kökü (ör. http://127.0.0.1:3310) — T6")
    a = ap.parse_args()
    K, k = Path(a.kok), a.key
    H: list[str] = []
    md = K / "metin" / f"{k}.md"
    if not md.exists():
        print(f"{k}: metin yok"); return 1
    pars = [p["t"] for p in metin_paragraflari(md.read_text(encoding="utf-8"))]
    kz, cz, isr, capa = (oku(K / d / f"{k}.json") for d in ("kelime_zaman", "cumle_zaman", "isaret", "capa"))
    for ad, v in (("kelime_zaman", kz), ("cumle_zaman", cz), ("isaret", isr)):
        if not v:
            H.append(f"{ad} dosyası yok")
    if H:
        print("\n".join("HATA " + h for h in H)); return 1
    vid = a.varyant or next(iter(kz["varyantlar"]))
    if vid not in kz["varyantlar"] or vid not in cz["varyantlar"]:
        H.append(f"varyant {vid} kelime/cümle zamanında yok")
        print("\n".join("HATA " + h for h in H)); return 1
    KP, CP, CK = kz["varyantlar"][vid]["p"], cz["varyantlar"][vid]["p"], cz["varyantlar"][vid].get("k") or {}
    sure = a.sure
    if sure is None:
        kay = oku(K / "kayit.json") or {}
        sure = next((v.get("sureSn") for v in (kay.get(k) or []) if v.get("id") == vid), None)
    onceki_son = -1.0
    for pi, t in enumerate(pars):
        kel = re.findall(r"\S+", t)
        zt = KP.get(str(pi)) or []
        if len(zt) != len(kel):
            H.append(f"T1 P{pi}: {len(zt)} kelime zamanı ≠ {len(kel)} kelime")
        if any(b < a_ for a_, b in zip(zt, zt[1:])):
            H.append(f"T1 P{pi}: kelime zamanları artan değil")
        if zt:
            if zt[0] < onceki_son:
                H.append(f"T2 P{pi}: paragraf önceki paragrafın bitişinden önce başlıyor ({zt[0]} < {onceki_son})")
            onceki_son = zt[-1]
        sonlar = cumle_sonlari(t)
        cs = CP.get(str(pi)) or []
        if len(cs) != len(sonlar) - 1:
            H.append(f"T3 P{pi}: {len(cs)} cümle sınırı ≠ {len(sonlar)} cümle − 1")
        if any(b < a_ for a_, b in zip(cs, cs[1:])):
            H.append(f"T3 P{pi}: cümle sınırları artan değil")
        # T4: cümlenin ilk kelimesinin zamanı cümle aralığında
        if not zt and cs:  # kelime zamanı yoksa istemci cümle sınırlarına dayanır
            bas = [0] + sonlar[:-1]
            konum = [m.start() for m in re.finditer(r"\S+", t)]
            for ci, b in enumerate(bas):
                wi = next((j for j, c in enumerate(konum) if c >= b), None)
                if wi is None:
                    continue
                alt = cs[ci - 1] if ci else zt[0]
                ust = cs[ci] if ci < len(cs) else zt[-1]
                if not (alt - PAY <= zt[wi] <= ust + PAY):
                    H.append(f"T4 P{pi}.C{ci}: ilk kelime {zt[wi]} sn, cümle aralığı {round(alt, 2)}–{round(ust, 2)}")
        # T5: işaret
        il = (isr.get("c") or {}).get(str(pi)) or []
        cl = (capa or {}).get("p", [])[pi] if capa and pi < len(capa.get("p", [])) else None
        for ci in range(len(sonlar)):
            i = il[ci] if ci < len(il) else None
            if not i:
                H.append(f"T5 P{pi}.C{ci}: PDF işareti yok"); continue
            if cl and ci < len(cl) and cl[ci].get("sayfa") and i.get("s") != cl[ci]["sayfa"] and i.get("t") != "sayfa":
                H.append(f"T5 P{pi}.C{ci}: işaret s.{i.get('s')} ≠ çapa s.{cl[ci]['sayfa']}")
    if a.api:
        import urllib.request
        d = json.load(urllib.request.urlopen(f"{a.api}/api/canli-ders/{k}", timeout=30))
        v = next((x for x in d.get("varyantlar") or [] if x.get("id") == vid), None)
        kzc = (v or {}).get("kelimeZaman") or {}
        eksik = [pi for pi, t in enumerate(pars) if len(kzc.get(str(pi)) or []) != len(re.findall(r"\S+", t))]
        if not v:
            H.append(f"T6 canlı API'de {vid} sesi yok")
        elif eksik:
            H.append(f"T6 canlı API kelimeZaman eksik/uyumsuz paragraflar: {eksik[:8]}")
        sure = sure or v and v.get("sureSn")
    if sure and onceki_son > sure + 1:
        H.append(f"T2 son kelime {onceki_son} sn ses süresini ({sure} sn) aşıyor")
    tum = [x for v in (isr.get("c") or {}).values() for x in v]
    bos = sum(1 for x in tum if not x or x.get("t") == "sayfa")
    if tum and bos / len(tum) > 0.05:
        H.append(f"T5 işaretlerin %{round(100 * bos / len(tum))}'i yalnız sayfa/boş (üst %5)")
    for h in H:
        print("HATA", h)
    print(f"{k} [{vid}]: {len(pars)} paragraf · {sum(len(cumle_sonlari(t)) for t in pars)} cümle · {len(H)} HATA")
    return 1 if H else 0


if __name__ == "__main__":
    sys.exit(main())
