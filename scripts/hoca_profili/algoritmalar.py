#!/usr/bin/env python3
"""Satır sinyalleri ve birleşim algoritmaları (2026-27 sınaması). Çalıştırma: meds/.venv-ocr/bin/python (numpy gerekir).

Sinyaller (her biri ayrı algoritma olarak da ölçülür):
  fmt       biçim: ==vurgu==, kalın, tablo satırı, sayı/yüzde, eponim
  cue       sınav-kuran söz kalıpları (ISARET) sayısı
  tekrar    ders-içi geçmiş soru log-oranı (satir_model 'tekrar' modeli; sözcük düzeyi)
  emb_gec   bge-m3: satırın geçmiş çıkmışlara (tüm dersler) en yakın kosinüsü (anlamsal tekrar)
  emb_ders  aynı, yalnız aynı dersin çıkmışlarına
  emb_konu  aynı, yalnız dersin EN YAKIN 40 çıkmışına (konu-bazlı yerel profil; konu adı eşleşmesine bağlı değil)
  hedef     satırın dersin 'Öğrenim Hedefleri' satırlarına kosinüs yakınlığı (hocanın beyan ettiği hedef → soru)
  merkez    TextRank: satırın ders içi merkeziliği
  tur       konunun yerel bilgi-türü profili ile satırın bilgi-türü ipucu uyumu
Birleşim: sıra-ortalaması (ağırlıklı) ve L2'li lojistik regresyon (geliştirme dersleri üzerinde, bir-ders-dışarıda ile).
"""
from __future__ import annotations

import json
import math
import pickle
import re
import sys
import urllib.request
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ortak import BILGI_TURLERI, jetonlar, norm, soru_yukle  # noqa: E402
from sinama_ortak import SC, veri  # noqa: E402
from satir_model import ILAC_EK, ISARET_RX, modeli_yukle, lr_skor, BICIM_IDX, ISARET_IDX, STATIK_AD, TEKRAR_AD, ozellikler  # noqa: E402

URL = "http://127.0.0.1:8094/embed"


def embed(metinler: list[str]) -> np.ndarray:
    out = []
    for i in range(0, len(metinler), 48):
        req = urllib.request.Request(URL, data=json.dumps({"texts": metinler[i:i + 48], "kind": "raw"}).encode(), headers={"Content-Type": "application/json"})
        out += json.loads(urllib.request.urlopen(req, timeout=600).read())["vectors"]
    a = np.array(out, dtype=np.float32)
    return a / np.maximum(np.linalg.norm(a, axis=1, keepdims=True), 1e-9)


def gecmis_gom():
    """Geçmiş çıkmış gömmeleri (önbellekli). 2026-27 YOK (soru_yukle yalnız pastQuestions)."""
    f = SC / "gecmis_emb.pkl"
    Q = soru_yukle()
    if f.exists():
        d = pickle.loads(f.read_bytes())
        if len(d["ids"]) == len(Q):
            return Q, d["E"]
    E = embed([q["kok"] + " " + q["siklar"][q["dogru_i"]] for q in Q])
    f.write_bytes(pickle.dumps(dict(ids=[q["id"] for q in Q], E=E)))
    return Q, E


def ders_gom(dd):
    f = SC / f"satir_{dd['id']}.pkl"
    n = len(dd["satirlar"])
    if f.exists():
        d = pickle.loads(f.read_bytes())
        if d["n"] == n:
            return d["E"]
    E = embed([r["t"][:300] for r in dd["satirlar"]])
    f.write_bytes(pickle.dumps(dict(n=n, E=E)))
    return E


def textrank(E: np.ndarray, it=30) -> np.ndarray:
    S = np.maximum(E @ E.T, 0)
    np.fill_diagonal(S, 0)
    S = np.where(S > 0.45, S, 0)
    rs = S.sum(1, keepdims=True)
    P = S / np.maximum(rs, 1e-9)
    v = np.ones(len(E)) / len(E)
    for _ in range(it):
        v = 0.15 / len(E) + 0.85 * (P.T @ v)
    return v


def tur_ipucu(t: str) -> dict[str, float]:
    tl = norm(t)
    return {ad: float(len(re.findall(rx, tl)) > 0) for ad, rx in BILGI_TURLERI}


def sinyaller(dd, Q, QE, Qders_idx):
    sat = dd["satirlar"]
    n = len(sat)
    E = ders_gom(dd)
    S = E @ QE.T  # n × nq
    top = lambda M, k: np.sort(M, axis=1)[:, -k:].mean(1) if M.shape[1] >= k else (M.max(1) if M.shape[1] else np.zeros(n))
    ders_i = Qders_idx.get(dd["ders"], [])
    emb_gec = top(S, 3)
    emb_ders = top(S[:, ders_i], 3) if len(ders_i) >= 3 else emb_gec
    # konu-bazlı yerel profil: dersin satırlarının ortalama vektörüne en yakın 40 soru (aynı ders içinde)
    c = E.mean(0)
    yakin = np.argsort(-(QE[ders_i] @ c))[:40] if len(ders_i) >= 40 else np.arange(len(ders_i))
    yi = [ders_i[j] for j in yakin]
    emb_konu = top(S[:, yi], 2) if yi else emb_gec
    # yerel bilgi türü profili
    yp = Counter(Q[j]["tur"] for j in yi)
    toplam = max(1, sum(yp.values()))
    # hedef yakınlığı
    hed = [i for i, r in enumerate(sat) if re.search(r"öğrenim hedef", norm(r["baslik"]))]
    if hed:
        H = E[hed] @ E.T
        hedef = H.max(0)
        hedef[hed] = 0
    else:
        hedef = np.zeros(n)
    merkez = textrank(E)
    fmt, cue, tur = np.zeros(n), np.zeros(n), np.zeros(n)
    for i, r in enumerate(sat):
        t = r["t"]
        fmt[i] = 1.0 * r["vurgu"] + 0.6 * r["kalin"] + 0.4 * r["tablo"] + 0.3 * bool(re.search(r"\d", t)) + 0.3 * bool(re.search(r"%|oran", norm(t))) + 0.2 * bool(ILAC_EK.search(norm(t)))
        cue[i] = sum(1 for k, rx in ISARET_RX.items() if (r["tablo"] if k == "tablo_satiri" else rx.search(norm(t))))
        ip = tur_ipucu(t)
        tur[i] = sum(ip[a] * yp.get(a, 0) / toplam for a in ip)
    # tekrar (sözcük düzeyi) — eski özet verisiyle eğitilmiş model
    d, st = modeli_yukle()
    fe = ozellikler(sat, st)
    nS = len(STATIK_AD)
    tekrar = np.array([lr_skor(d["model_tekrar"], x[nS:]) for x in fe])
    bic = np.array([lr_skor(d["model_bicim"], [x[j] for j in BICIM_IDX + ISARET_IDX]) for x in fe])
    uz = np.array([math.log1p(r["uzun"]) for r in sat])
    poz = np.array([r["pos"] for r in sat])
    gir = np.array([1.0 if re.search(r"öğrenim hedef|kaynak|özet|giriş", norm(r["baslik"])) else 0.0 for r in sat])
    return dict(fmt=fmt, cue=cue, tekrar=tekrar, bicim_eski=bic, emb_gec=emb_gec, emb_ders=emb_ders, emb_konu=emb_konu, hedef=hedef, merkez=merkez, tur=tur,
                uzun=uz, poz=poz, giris=gir, emb_ders_max=S[:, ders_i].max(1) if ders_i else emb_gec)


def hepsi():
    f = SC / "sinyaller.pkl"
    ders = veri()
    if f.exists():
        d = pickle.loads(f.read_bytes())
        if set(d) == set(ders):
            return ders, d
    Q, QE = gecmis_gom()
    idx = {}
    for j, q in enumerate(Q):
        idx.setdefault(q["ders"], []).append(j)
    sig = {k: sinyaller(dd, Q, QE, idx) for k, dd in ders.items()}
    f.write_bytes(pickle.dumps(sig))
    return ders, sig


def sira01(x):
    o = np.argsort(np.argsort(x))
    return o / max(1, len(x) - 1)


def lr(X, y, w, l2=1.0, it=300, lr_=0.1):
    mu, sd = X.mean(0), X.std(0) + 1e-6
    Z = (X - mu) / sd
    wt = np.zeros(X.shape[1]); b = 0.0
    for _ in range(it):
        p = 1 / (1 + np.exp(-(Z @ wt + b)))
        g = (p - y) * w
        wt -= lr_ * ((Z.T @ g) / len(y) + l2 * wt / len(y))
        b -= lr_ * g.mean()
    return mu, sd, wt, b


if __name__ == "__main__":
    ders, sig = hepsi()
    print(len(sig), "ders sinyali hazır")


def ekstra(dd) -> dict:
    """Ders notunun kendi yapısından sinyaller (ders notu biçimi: SPOT BİLGİLER + Çıkmış Sorular bölümleri)."""
    sat = dd["satirlar"]
    n = len(sat)
    E = ders_gom(dd)
    spot = np.array([1.0 if re.search(r"spot", norm(r["baslik"])) else 0.0 for r in sat])
    cik = np.array([1.0 if re.search(r"çıkmış|soru \d+", norm(r["baslik"])) else 0.0 for r in sat])
    def yak(maske):
        idx = [i for i in range(n) if maske[i]]
        if not idx:
            return np.zeros(n)
        S = E @ E[idx].T
        for j, i in enumerate(idx):
            S[i, j] = 0
        return S.max(1)
    return dict(spot=spot, cikmis_bolum=cik, ozcik_sim=yak(cik), spot_sim=yak(spot),
                govde=1.0 - np.maximum(spot, cik))


def hepsi2():
    ders, sig = hepsi()
    f = SC / "ekstra.pkl"
    if f.exists():
        ex = pickle.loads(f.read_bytes())
        if set(ex) == set(ders):
            for k in ders:
                sig[k].update(ex[k])
            return ders, sig
    ex = {k: ekstra(dd) for k, dd in ders.items()}
    f.write_bytes(pickle.dumps(ex))
    for k in ders:
        sig[k].update(ex[k])
    return ders, sig
