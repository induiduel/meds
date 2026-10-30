#!/usr/bin/env python3
"""Öğrenci önem notunun çıkmış soruları ne kadar yakaladığı (isabet / başarı oranı).

  python3 scripts/ogrenci_onem/basari.py --hazirla <klasör>   # yargıç partileri (soru + aday birimler + arşiv slayt sayfası)
  python3 scripts/ogrenci_onem/basari.py --hesapla <klasör>   # yargı_*.json → src/data/ogrenci_onem/basari.json + özet

Neden yargıç: vektör benzerliği "aynı konu"yu yakalar ama "sorunun ölçtüğü bilgi notta var mı" sorusunu yanıtlayamaz
(k2-05'te nöroanatomi soruları muayene birimlerine 0,5 benzerlikle düşüyor). Her soru için bağımsız yargıç
(alt ajan, LLM) karar verir: tam | kismi | yok, ve sorunun bilgisi 2025-26 ders slaytında var mı (`slaytta`).
Ölçüler (ders, branş, genel):
  - isabet_tam      = tam / slaytta olan sorular         (öğrenci notu sorunun bilgisini birebir içeriyor)
  - isabet_genis    = (tam + kismi) / slaytta olan sorular
  - yapistirilmamis = notta yapıştırılmamış sorularda isabet (gerçek öngörü gücü; yapıştırılan soru zaten kapsanır)
  - secicilik       = notta yer alan arşiv slayt sayfası / dersin toplam sayfası
  - kaldirac        = isabet_tam(yapıştırılmamış) / secicilik   (>1: not rastgele sayfa seçiminden iyi)
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agents"))
from ortak import CIKTI, PAST, Y25_PDF, oku_json  # noqa: E402

PARTI = 30


def y25_sayfa_sayisi(key: str) -> int:
    p = Y25_PDF / f"{key}.pdf"
    if not p.exists():
        return 0
    o = subprocess.run(["pdfinfo", str(p)], capture_output=True, text=True).stdout
    return int(next((l.split()[-1] for l in o.splitlines() if l.startswith("Pages:")), 0))


def y25_sayfalar(key: str) -> dict[int, str]:
    p = Y25_PDF / f"{key}.pdf"
    if not p.exists():
        return {}
    t = subprocess.run(["pdftotext", "-layout", str(p), "-"], capture_output=True, text=True).stdout
    return {i + 1: " ".join(s.split()) for i, s in enumerate(t.split("\f")) if i < y25_sayfa_sayisi(key)}


def hazirla(klasor: Path) -> None:
    from lib import embed  # noqa: E402
    past = {q["id"]: q for q in json.loads(PAST.read_text())}
    klasor.mkdir(parents=True, exist_ok=True)
    isler = []
    for f in sorted(CIKTI.glob("k2-*.json")):
        d = json.loads(f.read_text())
        if not d["banka"]:
            continue
        birim_txt = {b["id"]: (b["baslik"] + " | " + b["metin"] + " | el: " + "; ".join(e["metin"] for e in b["el_yazisi"]))[:900]
                     for b in d["birimler"]}
        ids = list(birim_txt)
        BV = embed([birim_txt[i] for i in ids], model="bge-m3")
        key = d["y25"]["key"]
        sayfa = y25_sayfalar(key) if key else {}
        sn = [k for k, v in sayfa.items() if v.strip()]
        SV = embed([sayfa[k][:1500] for k in sn], model="bge-m3") if sn else []
        QV = embed([r["kok"] + " " + r["dogru"] for r in d["banka"]], model="bge-m3")
        for r, qv in zip(d["banka"], QV):
            q = past.get(r["id"], {})
            sk = sorted(((float(BV[j] @ qv), ids[j]) for j in range(len(ids))), reverse=True)[:4]
            sp = sorted(((float(SV[j] @ qv), sn[j]) for j in range(len(sn))), reverse=True)[:2] if sn else []
            isler.append(dict(
                id=r["id"], ders=d["ders"], konu=d["konu"], yillar=r["yillar"], notta_yapistirilmis=r["notta_yapistirilmis"],
                kok=q.get("stem", r["kok"]), siklar=[f"{o.get('key')}) {o.get('text')}" for o in q.get("options") or []], dogru=r["dogru"],
                aday_birimler=[dict(id=i, benzerlik=round(s, 3), metin=birim_txt[i]) for s, i in sk],
                arsiv_sayfalari=[dict(key=key, sayfa=p, metin=sayfa[p][:900]) for s, p in sp]))
    for n in range(0, len(isler), PARTI):
        (klasor / f"parti_{n // PARTI + 1:02d}.json").write_text(json.dumps(isler[n:n + PARTI], ensure_ascii=False, indent=1))
    print(f"{len(isler)} soru, {(len(isler) + PARTI - 1) // PARTI} parti → {klasor}")


def oran(a: int, b: int):
    return round(a / b, 3) if b else None


def hesapla(klasor: Path) -> None:
    yargi = {}
    for f in sorted(klasor.glob("yargi_*.json")):
        for y in json.loads(f.read_text()):
            yargi[y["id"]] = y
    satir = []
    for f in sorted(CIKTI.glob("k2-*.json")):
        d = json.loads(f.read_text())
        key = d["y25"]["key"]
        top = y25_sayfa_sayisi(key) if key else 0
        sec = oran(len(d["y25"]["sayfalar"]), top)
        for r in d["banka"]:
            y = yargi.get(r["id"])
            if not y:
                continue
            satir.append(dict(ders=d["ders"], brans=d["brans"], konu=d["konu"], secicilik=sec, yapis=r["notta_yapistirilmis"],
                              karar=y["karar"], slaytta=y.get("slaytta", True), yillar=r["yillar"], id=r["id"], birim=y.get("birim")))

    def ozet(rs: list[dict]) -> dict:
        def olc(ss: list[dict]) -> dict:
            ya = [r for r in ss if not r["yapis"]]
            tam = sum(r["karar"] == "tam" for r in ss); gen = sum(r["karar"] in ("tam", "kismi") for r in ss)
            ytam = sum(r["karar"] == "tam" for r in ya); ygen = sum(r["karar"] in ("tam", "kismi") for r in ya)
            return dict(n=len(ss), yapistirilan=len(ss) - len(ya), isabet_tam=oran(tam, len(ss)), isabet_genis=oran(gen, len(ss)),
                        yapistirilmamis_n=len(ya), yapistirilmamis_tam=oran(ytam, len(ya)), yapistirilmamis_genis=oran(ygen, len(ya)))
        secs = [r["secicilik"] for r in rs if r["secicilik"]]
        sec = round(sum(secs) / len(secs), 3) if secs else None
        # Ana ölçü: tüm sorular (yargıcın "slaytta" kararı gürültülü: bilgi slayt metninde değil hocanın sözünde/el notunda
        # olabilir — ör. rijiditenin tanımı). İkinci ölçü: yalnız bilgisi 2025-26 slayt metninde bulunan sorular.
        t, sl = olc(rs), olc([r for r in rs if r["slaytta"]])
        ya = t["yapistirilmamis_tam"]
        ys = sl["yapistirilmamis_tam"]
        return dict(soru=len(rs), **t, slaytta=sl, secicilik=sec,
                    kaldirac=round(ya / sec, 2) if ya is not None and sec else None,
                    kaldirac_slaytta=round(ys / sec, 2) if ys is not None and sec else None)

    ders, brans = defaultdict(list), defaultdict(list)
    for r in satir:
        ders[r["ders"]].append(r); brans[r["brans"]].append(r)
    son = [r for r in satir if any(y in ("2025-2026",) for y in r["yillar"])]
    out = dict(surum=1, yontem="docs/OGRENCI_ONEM_YONTEMI.md §4", genel=ozet(satir),
               son_sinav_2025_26=ozet(son), brans={k: ozet(v) for k, v in sorted(brans.items())},
               ders={k: dict(konu=v[0]["konu"], **ozet(v)) for k, v in sorted(ders.items())},
               kacan=[dict(id=r["id"], ders=r["ders"], yillar=r["yillar"], slaytta=r["slaytta"]) for r in satir if r["karar"] == "yok"])
    (CIKTI / "basari.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(json.dumps(dict(genel=out["genel"], son=out["son_sinav_2025_26"], brans=out["brans"]), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--hazirla"); g.add_argument("--hesapla")
    a = ap.parse_args()
    hazirla(Path(a.hazirla)) if a.hazirla else hesapla(Path(a.hesapla))
