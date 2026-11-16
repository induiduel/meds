#!/usr/bin/env python3
"""Bağımsız yargıç protokolü. meds/.venv-ocr/bin/python ile çalışır.

  yargic.py hazirla <tur> [--set gelistirme|bekletilmis] [--grup N]  → <SC>/tur<N>/yargic/girdi_<g>.json (+ gizli eşleme)
  yargic.py puanla  <tur> [--set ...]                                  → karar dosyalarından tutturma oranı

Üç tahmin kümesi KÖR etiketle (X/Y/Z, derse göre karıştırılmış) yargıca verilir: LLM tahmini, algoritma ilk-8 satır, rastgele 8 satır.
Yargıç her soru için her kümede o soruyu sınayan bilgiyi içeren tahmini bulur: 2 = aynı bilgi (aynı olgu), 1 = aynı alt konu/komşu olgu, 0 = yok.
Sıkı skor = puan 2 oranı (asıl ölçüt). Geniş skor = puan ≥1.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from algoritmalar import hepsi, sira01  # noqa: E402
from sinama_ortak import SC, bekletilmis, gelistirme  # noqa: E402


def kume_hazirla(ders, sig, k, tur):
    dd = ders[k]
    f = SC / f"tur{tur}/cikti/{k}.json"
    llm = []
    if f.exists():
        try:
            llm = [t["olgu"] for t in json.loads(f.read_text())["tahminler"]]
        except Exception:
            pass
    ag = json.loads((SC / "agirlik.json").read_text())
    s = sum(a * sira01(sig[k][ad]) for ad, a in ag.items())
    Kn = max(8, len(llm))
    algo = [dd["satirlar"][int(i)]["t"][:300] for i in np.argsort(-s)[:Kn]]
    rnd = random.Random(hash(k) % 1000 + 7)
    rastgele = [dd["satirlar"][i]["t"][:300] for i in rnd.sample(range(len(dd["satirlar"])), min(Kn, len(dd["satirlar"])))]
    return dict(llm=llm, algo=algo, rastgele=rastgele)


def hazirla(tur, kume, grup_say=3):
    ders, sig = hepsi()
    sec = gelistirme(ders) if kume == "gelistirme" else bekletilmis(ders)
    ks = sorted(sec)
    d = SC / f"tur{tur}/yargic"
    d.mkdir(parents=True, exist_ok=True)
    gizli = {}
    gruplar = [ks[i::grup_say] for i in range(grup_say)]
    for g, kk in enumerate(gruplar):
        out = []
        for k in kk:
            kum = kume_hazirla(ders, sig, k, tur)
            etik = ["X", "Y", "Z"]
            random.Random(k).shuffle(etik)
            esle = dict(zip(["llm", "algo", "rastgele"], etik))
            gizli[k] = esle
            out.append(dict(ders_id=k, konu=ders[k]["konu"],
                            sorular=[dict(soru_id=str(q["sinav_no"]), kok=q["kok"], dogru=q["dogru"], siklar=q["siklar"]) for q in ders[k]["sorular"]],
                            kumeler={esle[a]: [dict(idx=i, metin=m) for i, m in enumerate(kum[a])] for a in kum}))
        (d / f"girdi_{kume}_{g}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    (d / f"gizli_{kume}.json").write_text(json.dumps(gizli))
    print(len(gruplar), "yargıç girdisi:", d)


def puanla(tur, kume):
    d = SC / f"tur{tur}/yargic"
    gizli = json.loads((d / f"gizli_{kume}.json").read_text())
    toplam = {a: [0, 0, 0] for a in ("llm", "algo", "rastgele")}  # [n, siki, genis]
    ders_sk = {}
    for f in sorted(d.glob(f"karar_{kume}_*.json")):
        for k in json.loads(f.read_text()).get("dersler", []):
            esle = gizli[k["ders_id"]]
            ters = {v: a for a, v in esle.items()}
            for s in k["kararlar"]:
                for et, a in ters.items():
                    p = int((s.get(et) or {}).get("puan", 0))
                    toplam[a][0] += 1; toplam[a][1] += p == 2; toplam[a][2] += p >= 1
                    if a == "llm":
                        ders_sk.setdefault(k["ders_id"], []).append(p)
    out = {a: dict(n=v[0], siki=round(v[1] / max(1, v[0]), 3), genis=round(v[2] / max(1, v[0]), 3)) for a, v in toplam.items()}
    (d / f"yargic_sonuc_{kume}.json").write_text(json.dumps(dict(ozet=out, llm_ders=ders_sk), ensure_ascii=False, indent=1))
    print(json.dumps(out, ensure_ascii=False))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("komut", choices=["hazirla", "puanla"])
    ap.add_argument("tur", type=int)
    ap.add_argument("--set", default="gelistirme")
    a = ap.parse_args()
    (hazirla if a.komut == "hazirla" else puanla)(a.tur, a.set)
