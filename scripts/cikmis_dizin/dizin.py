#!/usr/bin/env python3
"""Çıkmış dizini — her tekil çıkmış BİR KEZ işlenir, PDF'ler yalnız kendi adaylarını tarar (ICERIK_MOTORU_V3.md §15.1, §15.3).

Kaynak: `meds/data/pastQuestions.json` (yalnız Dönem 3; karantina ve şüpheli dışı). Her soru için:
  {id, aile, kurul (int | None: final/bütünleme), tur, brans, konu, yil, kok, secenekler, dogru, dogru_metin, varliklar,
   karma, v (vektör satırı)}
Aile: katlanmış kök + doğru şık metni aynı olan kopyalar tek aile (`kez` = farklı sınav yılı sayısı).
Vektör: bge-m3 (CPU :8094), metin = kök + doğru şık; önbellekli (değişmeyen soru yeniden vektörlenmez).
Ters dizinler: varlik → [id], brans → [id], kurul → [id].
Artımlı: önceki dizinle karma karşılaştırılır; yeni/değişen sorular `meds_temp/cikmis_dizin/degisen.json`'a, bunların
etkileyebileceği dersler (L0 varlık kesişimi + branş) `etkilenen.json`'a yazılır → yalnız o derslerin planı yeniden kurulur.

Çıktı: meds_database_v2/cikmis_dizin/{dizin.json, vektor.npy (float16), ters.json}
Kullanım (.venv-ocr): dizin.py [--zorla]     |     dizin.py --etkilenen     (son değişikliklerin etkilediği dersler)
"""
from __future__ import annotations

import argparse
import re
import sys
import time
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "kroki"))
import numpy as np  # noqa: E402

import varlik  # noqa: E402
from ortak import DB2, DEPO, KOK, TEMP, katla, oku, sha, sha_dosya, vektorle, yaz  # noqa: E402

SURUM = 1
HEDEF = DB2 / "cikmis_dizin"
KAYNAK = KOK / "data" / "pastQuestions.json"
DURUM_TEMP = TEMP / "cikmis_dizin"


def _tur_kurul(cid: str) -> tuple[str, int | None]:
    m = re.fullmatch(r"donem3-kurul(\d)", cid or "")
    if m:
        return "kurul", int(m.group(1))
    return (cid or "").replace("donem3-", "") or "bilinmiyor", None


def satir(q: dict) -> dict | None:
    cid = q.get("committeeId") or ""
    if not cid.startswith("donem3") or q.get("status") == "quarantined" or q.get("isSuspect"):
        return None
    rec = q.get("reconstruction") if isinstance(q.get("reconstruction"), dict) else {}
    kok = (q.get("stem") or rec.get("stem") or "").strip()
    sec = {(o.get("key") or o.get("label") or "").strip().upper()[:1]: (o.get("text") or "").strip() for o in q.get("options") or []}
    dogru = (q.get("correctAnswer") or "").strip().upper()[:1]
    if len(kok) < 15 or dogru not in sec:
        return None
    tur, kurul = _tur_kurul(cid)
    metin = kok + " " + " ".join(sec.values())
    return {"id": q["id"], "tur": tur, "kurul": kurul, "brans": q.get("discipline") or "", "konu": q.get("topic") or "",
            "yil": q.get("examYear") or "", "kok": kok, "secenekler": sec, "dogru": dogru, "dogru_metin": sec[dogru],
            "varliklar": sorted(varlik.cikar(metin)),
            "karma": sha(kok + "|" + "|".join(f"{k}:{v}" for k, v in sorted(sec.items())) + "|" + dogru, 12)}


def aile_anahtari(r: dict) -> str:
    return sha(" ".join(re.findall(r"[0-9a-z]+", katla(r["kok"]))) + "|" + katla(r["dogru_metin"]).strip(), 12)


def kur(zorla: bool = False, log=print) -> dict:
    t0 = time.time()
    ham = oku(KAYNAK, [])
    if not ham:
        raise SystemExit(f"çıkmış kaynağı okunamadı: {KAYNAK}")
    satirlar = [r for q in ham if (r := satir(q))]
    eski = oku(HEDEF / "dizin.json") or {}
    eski_karma = {r["id"]: r["karma"] for r in eski.get("sorular", [])}
    aileler = defaultdict(list)
    for r in satirlar:
        aileler[aile_anahtari(r)].append(r)
    for uyeler in aileler.values():
        aid = min(u["id"] for u in uyeler)
        yillar = sorted({u["yil"] for u in uyeler if u["yil"]})
        for u in uyeler:
            u["aile"], u["kez"], u["yillar"] = aid, max(len(yillar), 1), yillar
    vek = vektorle([f"{r['kok']} Cevap: {r['dogru_metin']}" for r in satirlar])
    for i, r in enumerate(satirlar):
        r["v"] = i
    ters = {"varlik": defaultdict(list), "brans": defaultdict(list), "kurul": defaultdict(list)}
    for r in satirlar:
        for v in r["varliklar"]:
            ters["varlik"][v].append(r["id"])
        ters["brans"][r["brans"]].append(r["id"])
        ters["kurul"][str(r["kurul"] or r["tur"])].append(r["id"])
    degisen = [r["id"] for r in satirlar if eski_karma.get(r["id"]) != r["karma"]]
    silinen = sorted(set(eski_karma) - {r["id"] for r in satirlar})
    HEDEF.mkdir(parents=True, exist_ok=True)
    np.save(HEDEF / "vektor.npy", vek.astype("float16"))
    d = {"surum": SURUM, "olusturuldu": time.strftime("%Y-%m-%dT%H:%M:%S"), "kaynak": str(KAYNAK),
         "kaynak_sha": sha_dosya(KAYNAK), "soru_sayisi": len(satirlar), "aile_sayisi": len(aileler), "sorular": satirlar}
    d["dizin_sha"] = sha("|".join(r["karma"] for r in satirlar), 16)
    yaz(HEDEF / "dizin.json", d)
    yaz(HEDEF / "ters.json", {k: dict(v) for k, v in ters.items()})
    if eski and (degisen or silinen):
        yaz(DURUM_TEMP / "degisen.json", {"zaman": d["olusturuldu"], "degisen": degisen, "silinen": silinen,
                                          "etkilenen": etkilenen_dersler([r for r in satirlar if r["id"] in set(degisen)])}, 1)
    log(f"çıkmış dizini: {len(satirlar)} soru, {len(aileler)} aile, {len(ters['varlik'])} varlık, "
        f"{len(degisen) if eski else 'ilk kurulum'} değişen, {len(silinen)} silinen, {time.time() - t0:.0f} sn")
    return d


def ders_varliklari(ders: str) -> set[str]:
    l0 = oku(DEPO / ders / "l0" / "sayfalar.json") or {}
    return {v for s in l0.get("sayfalar", []) for v in s.get("varliklar", [])}


def etkilenen_dersler(sorular: list[dict]) -> dict[str, list[str]]:
    """Yeni/değişen çıkmışın planını etkileyebileceği dersler: ≥1 sözlük terimi ya da ≥2 varlık ortak (yalnız L0'ı olanlar)."""
    out: dict[str, list[str]] = {}
    dv = {p.parent.parent.name: ders_varliklari(p.parent.parent.name) for p in DEPO.glob("k*-*/l0/sayfalar.json")}
    for q in sorular:
        qv = set(q["varliklar"])
        for ders, v in dv.items():
            ortak = qv & v
            if any(x.startswith("t:") for x in ortak) or len(ortak) >= 2:
                out.setdefault(ders, []).append(q["id"])
    return out


def yukle() -> tuple[dict, np.ndarray]:
    d = oku(HEDEF / "dizin.json")
    if not d:
        raise SystemExit("çıkmış dizini yok — scripts/cikmis_dizin/dizin.py")
    return d, np.load(HEDEF / "vektor.npy").astype("float32")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--zorla", action="store_true")
    ap.add_argument("--etkilenen", action="store_true")
    a = ap.parse_args()
    if a.etkilenen:
        print(oku(DURUM_TEMP / "degisen.json", {}))
        return 0
    kur(a.zorla)
    return 0


if __name__ == "__main__":
    sys.exit(main())
