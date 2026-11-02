#!/usr/bin/env python3
"""Hocanın vurguladıkları — ayrı kategori (kullanıcı kararı 2026-11-02; LLM yok).

Hocanın ders kaydında "sınavda sorarım / çıkmıştı / önemli / bilin / dikkat edin" dediği yerler (Faz A1:
meds_temp/ogrenci_ders/<ders>/hoca_vurgulari.json, şema GOREV_ORTAK_K2_B2.md) öğrenciye ayrı listede sunulur
(ders sayfası › Hocanın vurguladıkları; components/v15/HocaVurguV15.tsx) ve sesli derste/önem listesinde rozet olur.

  python3 scripts/hoca_vurgu/yayinla.py kimlik <klasör> --ders k2-10        # kalıcı kimlik (hv-k2-10-NN) ekler, anlatımdan ÖNCE
  python3 scripts/hoca_vurgu/yayinla.py yaz <klasör> --ders k2-10 --key <sesli ders anahtarı> [--deste deck.json]
  python3 scripts/hoca_vurgu/yayinla.py dogrula --ders k2-10 --key <key>

yaz: yalnız tur=sinav, guven yuksek|orta, slayt sayfalı kayıtlar → src/data/hoca_vurgu/<ders>.json.
     p (sesli ders paragrafı): v2 cümlesindeki hoca.id; yoksa hizalamada aynı sayfayı anlatan ilk paragraf.
     adim (Öğren slaytı): destedeki pdfSayfalari aralığı s'yi içeren ilk içerik slaytı.
dogrula (HATA): kimliksiz/çift kimlik, kategori dışı tür, boş konu/alıntı, alıntıda bozuk Whisper terimi ihtimali
     (konu sözcüklerinin hiçbiri alıntıda/slaytta yok), v2'de geçen hoca.id'nin listede olmaması, p'nin metin dışı olması.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
SA = KOK / "data" / "sesli_anlatim"
CIKTI = KOK / "src" / "data" / "hoca_vurgu"
KATEGORI = ("sorulur", "cikmis", "onemli", "bilin", "dikkat")


def dk(t) -> str:
    t = int(float(t or 0))
    return f"{t // 60}:{t % 60:02d}"


def oku(p: Path, vars=None):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else vars


def sesli_dosya(alt: str, key: str) -> Path | None:
    L = sorted((SA / alt).glob(f"{key}*.json"))
    tam = [x for x in L if x.stem == key]
    return (tam or L or [None])[0]


def kimlik(a) -> int:
    f = Path(a.klasor) / "hoca_vurgulari.json"
    L = oku(f, [])
    if isinstance(L, dict):
        L = L.get(a.ders, [])
    var = {x.get("id") for x in L if x.get("id")}
    n = max([int(i.rsplit("-", 1)[1]) for i in var if re.search(r"-\d+$", i)] or [0])
    for x in sorted(L, key=lambda x: float(x.get("t") or 0)):
        if not x.get("id"):
            n += 1
            x["id"] = f"hv-{a.ders}-{n:02d}"
    f.write_text(json.dumps(L, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(L)} kayıt, {n} kimlik → {f}")
    return 0


def sade(t: str) -> str:
    """Öğrenciye gösterilen metinden iç not parantezlerini atar ("(öykü kavramı slaytta yok)", "(döküm bozuk)")."""
    t = re.sub(r"\s*\([^)]*(?:slayt|döküm|dokum|kayıt|okunak|anlaşılm)[^)]*\)", "", t or "", flags=re.I)
    return re.sub(r"\((?:im|ım|um|üm)\)", "", t).strip()


def secilen(L: list) -> list:
    # slayt dışı vurgu (hocanın slaytta yazmayan bir konuya "çok önemli" demesi) da gerçek sözdür; slayt sayfası taşıdığı sürece listelenir
    return [x for x in L if x.get("tur") == "sinav" and x.get("guven") in ("yuksek", "orta") and x.get("s")]


def v2_haritasi(key: str) -> dict[str, int]:
    f = sesli_dosya("v2", key)
    v = oku(f, {}) if f else {}
    out, p = {}, -1
    for b in v.get("bolumler", []):
        for par in b.get("paragraflar", []):
            p += 1
            for c in par.get("cumleler", []):
                h = c.get("hoca") or {}
                if h.get("id") and h["id"] not in out:
                    out[h["id"]] = p
    return out


def yaz(a) -> int:
    L = oku(Path(a.klasor) / "hoca_vurgulari.json", [])
    if isinstance(L, dict):
        L = L.get(a.ders, [])
    S = secilen(L)
    if any(not x.get("id") for x in S):
        print("HATA: kimliksiz kayıt var — önce `yayinla.py kimlik`", file=sys.stderr)
        return 1
    v2 = v2_haritasi(a.key) if a.key else {}
    hz = sesli_dosya("hizalama", a.key) if a.key else None
    hp = (oku(hz, {}) or {}).get("paragraflar", []) if hz else []
    deste = oku(Path(a.deste), {}) if a.deste else {}
    slaytlar = [s for s in (deste.get("slides") or []) if s.get("pdfSayfalari") and not s.get("isCheckpoint") and not s.get("isGameFinale")]
    out = []
    for x in sorted(S, key=lambda x: float(x.get("t") or 0)):
        s = x.get("s")
        p = v2.get(x["id"])
        if p is None and s is not None:
            p = next((i for i, h in enumerate(hp) if h.get("sayfa") == s), None)
        adim = next((sl.get("slideNumber") for sl in slaytlar if sl["pdfSayfalari"][0] <= (s or -1) <= sl["pdfSayfalari"][-1]), None)
        out.append({"id": x["id"], "kategori": x.get("kategori"), "ifade": sade(x.get("ifade", "")),
                    "alinti": sade(x.get("alinti_duzgun") or x.get("alinti", "")), "konu": sade(x.get("konu_ozet") or x.get("konu", "")), "s": s,
                    "dk": dk(x.get("t")), "p": p, "adim": adim})
    CIKTI.mkdir(parents=True, exist_ok=True)
    f = CIKTI / f"{a.ders}.json"
    f.write_text(json.dumps({"ders": a.ders, "key": a.key or "", "vurgular": out}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(out)} vurgu ({sum(1 for o in out if o['p'] is not None)} paragraflı, {len(v2)} v2 bağı) → {f}")
    return dogrula(a)


def dogrula(a) -> int:
    f = CIKTI / f"{a.ders}.json"
    d = oku(f, None)
    if not d:
        print(f"HATA: {f} yok")
        return 1
    hata = []
    ids = [v.get("id") for v in d["vurgular"]]
    if len(ids) != len(set(ids)) or not all(ids):
        hata.append("kimlik boş ya da çift")
    for v in d["vurgular"]:
        if v.get("kategori") not in KATEGORI:
            hata.append(f"{v['id']}: kategori '{v.get('kategori')}'")
        if len(str(v.get("konu", "")).split()) < 2 or len(str(v.get("alinti", "")).split()) < 3:
            hata.append(f"{v['id']}: konu/alıntı boş ya da çok kısa")
        if v.get("s") is None:
            hata.append(f"{v['id']}: slayt sayfası yok")
    if a.key:
        v2 = v2_haritasi(a.key)
        for i in v2:
            if i not in ids:
                hata.append(f"v2 cümlesindeki hoca.id listede yok: {i}")
        met = sesli_dosya("metin", a.key)
        if met:
            n = sum(1 for s in met.read_text(encoding="utf-8").split("\n\n") if s.strip() and not s.lstrip().startswith(("#", "@@")))
            for v in d["vurgular"]:
                if v.get("p") is not None and not (0 <= v["p"] < n + 5):
                    hata.append(f"{v['id']}: p={v['p']} metin dışında")
    for h in hata:
        print("HATA", h)
    print(f"{len(hata)} HATA · {len(d['vurgular'])} vurgu")
    return 1 if hata else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("is_", choices=("kimlik", "yaz", "dogrula"))
    ap.add_argument("klasor", nargs="?")
    ap.add_argument("--ders", required=True)
    ap.add_argument("--key", default="")
    ap.add_argument("--deste", default="")
    a = ap.parse_args()
    return {"kimlik": kimlik, "yaz": yaz, "dogrula": dogrula}[a.is_](a)


if __name__ == "__main__":
    sys.exit(main())
