#!/usr/bin/env python3
"""Arşiv 25-26 (Kurul 2 ve 3) sesli ders işaretlerini YERİNDE anlam eşlemesiyle onarır (H655, 2026-11-25).

Kök neden: anlatım slaytı birebir okumaz; arşiv üreteci (arsiv_yayinla.pdf_isaret_yerel) yalnız ortak köke baktığı için
cümle "yalnız sayfa"ya ya da tek kelimelik zayıf "kelime" işaretine düşüyordu. Arşiv işaretleri yayından sonra çizim/lazer
adımlarıyla işlendiği için baştan üretilmez; yalnız şu işaretlere dokunulur:
  - t ∈ {"sayfa", "kelime"} ve lazer yolu (y) / çizim (z) YOK.
  - Sayfa DEĞİŞMEZ (çapa sayfası kesin, T5): anlam eşlemesi yalnız işaretin kendi sayfasında (komsu=False).
  - Eşleşme yoksa ve sayfada ≥2 gerçek madde varsa "sayfa" → "ek" (hocanın slaytta olmayan ek açıklaması); "kelime" kalır.
Kurul 1'e DOKUNULMAZ (kullanıcı kararı 2026-11-25): yalnız y25-k2-* ve y25-k3-*.
Kullanım: anlam_onar.py --hepsi | --key <key> [--kuru]
"""
from __future__ import annotations

import sys as _sys
from pathlib import Path as _Path
_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402

import argparse
import json
import re
import sys
from collections import Counter

sys.path.insert(0, str(_kok.SCRIPTS / "uretim" / "sesli_anlatim"))
sys.path.insert(0, str(_Path(__file__).resolve().parent))
import pdf_isaret as PI  # noqa: E402
from arsiv_yayinla import metin_paragraflari  # noqa: E402

SA = _kok.MEDS / "data" / "arsiv_25_26" / "sesli_anlatim"
IZINLI = re.compile(r"^y25-k[23]-")


def pdf_yolu(hz: dict) -> _Path | None:
    f = (hz.get("dosyalar") or [{}])[0]
    for y in (_kok.PROJE / f.get("path", ""), _Path(f.get("path", ""))):
        if y.is_file():
            return y
    return None


def ders_onar(key: str, kuru: bool) -> Counter | None:
    if not IZINLI.match(key):
        return None
    yi, yh, ym = SA / "isaret" / f"{key}.json", SA / "hizalama" / f"{key}.json", SA / "metin" / f"{key}.md"
    if not (yi.exists() and yh.exists() and ym.exists()):
        return None
    hz = json.loads(yh.read_text(encoding="utf-8"))
    yol = pdf_yolu(hz)
    if not yol:
        return None
    pdf = PI.Pdf(yol)
    isr = json.loads(yi.read_text(encoding="utf-8"))
    pars = metin_paragraflari(ym.read_text(encoding="utf-8"))
    yc = SA / "capa" / f"{key}.json"
    capa_p = json.loads(yc.read_text(encoding="utf-8")).get("p") if yc.exists() else None
    say = Counter()
    for pn, liste in isr["c"].items():
        pn = int(pn)
        if pn >= len(pars):
            continue
        m = pars[pn]["t"]
        sinir = PI.cumle_sonlari(m)
        cc = PI.cumle_capalari(m, sinir, capa_p[pn]) if capa_p and pn < len(capa_p) else None
        for ci, x in enumerate(liste):
            # T5: işaret çapanın sayfasından başka sayfadaysa (komşu sayfadan ödünç) çapa sayfasına geri alınır
            cs = next((int(c["sayfa"]) for c in (cc[ci] if cc and ci < len(cc) and cc[ci] else []) if c.get("sayfa")), None)
            if x and cs and int(x.get("s") or 0) != cs and not x.get("z"):
                sy = pdf.sayfa(cs)
                if sy:
                    cumle = m[(sinir[ci - 1] if ci else 0):sinir[ci]]
                    n, r = PI.eslestir(cumle, sy)
                    r = r if r and n >= 1 else {"t": "sayfa", "l": [], "w": []}
                    for k in ("t", "l", "w", "y"):
                        x.pop(k, None)
                    x["s"] = cs
                    x.update({k: v for k, v in r.items() if k in ("t", "l", "w")})
                    say["sayfa_duzeltme"] += 1
            if not x or x.get("t") not in ("sayfa", "kelime") or x.get("y") or x.get("z") or ci >= len(sinir):
                continue
            cumle = m[(sinir[ci - 1] if ci else 0):sinir[ci]]
            s = int(x.get("s") or 0)
            ar = PI.anlam_isaret(cumle, pdf, s, komsu=False, esik=0.72 if x["t"] == "kelime" else None) if PI.ANLAM else None
            if ar and ar[1] == s:
                yeni = ar[0]
                say[f"{x['t']}→{yeni['t']}"] += 1
            elif x["t"] == "sayfa":
                sy = pdf.sayfa(s)
                if not (sy and sum(1 for i in range(len(sy.maddeler)) if len(PI.madde_kokleri(sy, i)) >= 2) >= 2):
                    continue
                yeni = {"t": "ek", "l": [], "w": []}
                say["sayfa→ek"] += 1
            else:
                continue
            for k in ("t", "l", "w"):
                x.pop(k, None)
            x.update({k: v for k, v in yeni.items() if k in ("t", "l", "w")})
    if not PI.ANLAM:
        raise RuntimeError("anlam servisi (bge-m3 :8094) yanıt vermiyor")
    if say and not kuru:
        yi.write_text(json.dumps(isr, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return say


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--key", action="append")
    g.add_argument("--hepsi", action="store_true")
    ap.add_argument("--kuru", action="store_true")
    a = ap.parse_args()
    keys = a.key or sorted(p.stem for p in (SA / "isaret").glob("y25-k[23]-*.json"))
    top = Counter()
    for k in keys:
        try:
            r = ders_onar(k, a.kuru)
        except Exception as e:
            print(f"{k}: HATA {e}")
            continue
        if r is None:
            print(f"{k}: atlandı (Kurul 1 / dosya ya da PDF yok)")
            continue
        top.update(r)
        print(f"{k}: {dict(r)}", flush=True)
    print("TOPLAM", dict(top))
    return 0


if __name__ == "__main__":
    sys.exit(main())
