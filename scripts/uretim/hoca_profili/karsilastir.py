#!/usr/bin/env python3
"""Algoritma karşılaştırması: 2026-27 K1 (kaynak satır isabeti). meds/.venv-ocr/bin/python ile çalışır.

  karsilastir.py            → tek tek sinyaller + sıra birleşimleri + LOO lojistik; geliştirme ve bekletilmiş ayrı
Ayar yalnız GELİŞTİRME derslerinde yapılır; bekletilmiş kümeye yalnız rapor için bakılır.
"""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from algoritmalar import hepsi, lr, sira01  # noqa: E402
from sinama_ortak import bekletilmis, gelistirme, puanla  # noqa: E402

TEK = ["fmt", "cue", "tekrar", "bicim_eski", "emb_gec", "emb_ders", "emb_ders_max", "emb_konu", "hedef", "merkez", "tur", "uzun"]
LR_OZ = ["fmt", "cue", "tekrar", "emb_gec", "emb_ders", "emb_ders_max", "emb_konu", "hedef", "merkez", "tur", "uzun", "poz", "giris"]


def tek_skor(sig, ad, isaret=1):
    return {k: list(isaret * v[ad]) for k, v in sig.items()}


def birlesim(sig, agirlik):
    return {k: list(sum(a * sira01(v[ad]) for ad, a in agirlik.items())) for k, v in sig.items()}


def lr_skorlari(ders, sig, egitim_anahtar, test_anahtar, ozellik=LR_OZ, l2=30.0, poz_agirlik=8.0):
    X, y, w = [], [], []
    for k in egitim_anahtar:
        M = np.stack([sig[k][a] for a in ozellik], 1)
        pos = {i for q in ders[k]["sorular"] for i in q["altin"]}
        for i in range(len(M)):
            X.append(M[i]); y.append(1.0 if i in pos else 0.0); w.append(poz_agirlik if i in pos else 1.0)
    mu, sd, wt, b = lr(np.array(X), np.array(y), np.array(w), l2=l2)
    out = {}
    for k in test_anahtar:
        M = np.stack([sig[k][a] for a in ozellik], 1)
        out[k] = list(((M - mu) / sd) @ wt + b)
    return out, dict(zip(ozellik, np.round(wt, 2)))


def loo_dev(ders, sig, **kw):
    dev = [k for k, v in ders.items() if not v["bekletilmis"]]
    out = {}
    for k in dev:
        o, _ = lr_skorlari(ders, sig, [x for x in dev if x != k], [k], **kw)
        out.update(o)
    return out


def main():
    ders, sig = hepsi()
    dev, hold = gelistirme(ders), bekletilmis(ders)
    rnd = random.Random(1)
    sat = {k: len(v["satirlar"]) for k, v in ders.items()}
    rows = {}
    rows["rastgele"] = {k: [rnd.random() for _ in range(sat[k])] for k in ders}
    for ad in TEK:
        rows[ad] = tek_skor(sig, ad)
    rows["sira:emb_ders+emb_konu+hedef"] = birlesim(sig, dict(emb_ders=1, emb_konu=1, hedef=1))
    rows["sira:emb(3)+hedef+fmt+cue"] = birlesim(sig, dict(emb_ders=1, emb_konu=1, emb_gec=0.5, hedef=1, fmt=0.7, cue=0.5))
    rows["sira:hepsi_esit"] = birlesim(sig, {a: 1 for a in ["fmt", "cue", "tekrar", "emb_ders", "emb_konu", "hedef", "merkez", "tur"]})
    loo = loo_dev(ders, sig)
    lr_hold, agirlik = lr_skorlari(ders, sig, list(dev), list(hold))
    print("LR ağırlıkları (geliştirme):", agirlik)
    print(f"{'algoritma':34s} | GELİŞTİRME ilk5/ilk10/ilk%10/yüzdelik | BEKLETİLMİŞ ilk5/ilk10/ilk%10/yüzdelik")
    for ad, sk in list(rows.items()) + [("lojistik(LOO dev | dev→bekl.)", {**loo, **lr_hold})]:
        a = puanla({k: sk[k] for k in dev}, dev)
        b = puanla({k: sk[k] for k in hold}, hold)
        print(f"{ad:34s} | {a['ilk5']:.2f} {a['ilk10']:.2f} {a['ilk10yuzde']:.2f} {a['yuzdelik']:.2f} (n={a['n_soru']}) | {b['ilk5']:.2f} {b['ilk10']:.2f} {b['ilk10yuzde']:.2f} {b['yuzdelik']:.2f} (n={b['n_soru']})")


if __name__ == "__main__":
    main()
