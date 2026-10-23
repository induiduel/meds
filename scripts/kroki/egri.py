#!/usr/bin/env python3
"""Grafik eğrisi vektörleştirme — EKG, aksiyon potansiyeli, spirometri, büyüme eğrisi (ICERIK_MOTORU_V3.md §12.1).

Model yok, koordinat uydurma yok. Yöntem: resim bölgesi yüksek çözünürlükte çizilir → sinyal pikselleri (koyu, az doygun;
`--renkli` ile doygun renkli iz) → uzun düz eksen/ızgara çizgileri morfolojik açmayla atılır → her x sütununda bir y
(önceki y'ye en yakın koşu; kısa boşluk doğrusal doldurulur) → ortanca süzgeç → `scipy.signal.find_peaks` tepe/çukur →
türev işaretine göre `yukselis` / `inis` dilimleri.
Kapı: sütun kapsaması ≥ %60, noktaların ≥ %90'ı gerçek sinyal pikseli (1 px komşuluk) ve sinyal piksellerinin ≥ %60'ı izin
±3 px çevresinde (tekillik: yazı/şema bloğu eğri sanılmasın) — tutmazsa eğri YAZILMAZ.
Çıktı: L0 sayfasına `egri: [{id: <resim>-e1, nokta: [[x,y]…] (sayfa oranı, ≤200), fazlar: [{bas, son, faz}], tepe, cukur,
kapsama, isabet}]`.

Kullanım (.venv-ocr):
  egri.py --ders k1-22 --sayfa 14 [--resim g1] [--renkli] [--yaz]
  egri.py --sinama            yapay EKG benzeri eğri (pembe ızgara + eksen) — hata < 2 px ve fazlar doğru olmalı
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cv2  # noqa: E402
import numpy as np  # noqa: E402
from scipy.signal import find_peaks, medfilt  # noqa: E402

import l0kayit  # noqa: E402

KAPSAMA_ESIK, ISABET_ESIK, TEKILLIK_ESIK = 0.60, 0.90, 0.60


def sinyal_maskesi(bgr: np.ndarray, renkli: bool = False) -> np.ndarray:
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    if renkli:
        m = (hsv[:, :, 1] > 120) & (hsv[:, :, 2] > 60)
    else:
        m = (hsv[:, :, 2] < 110) & (hsv[:, :, 1] < 100)
    m = m.astype(np.uint8)
    h, w = m.shape
    # uzun düz çizgiler (eksen, ızgara kalın çizgisi) eğri değildir
    yatay = cv2.morphologyEx(m, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (max(w // 3, 15), 1)))
    dikey = cv2.morphologyEx(m, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (1, max(h // 3, 15))))
    return (m & ~(yatay | dikey)).astype(bool)


def egri_cikar(bgr: np.ndarray, renkli: bool = False) -> dict | None:
    m = sinyal_maskesi(bgr, renkli)
    h, w = m.shape
    ys = np.full(w, np.nan)
    onceki = None
    for x in range(w):
        satir = np.flatnonzero(m[:, x])
        if satir.size == 0:
            continue
        kosu = np.split(satir, np.flatnonzero(np.diff(satir) > 2) + 1)
        merkez = [float(k.mean()) for k in kosu]
        y = min(merkez, key=lambda c: abs(c - onceki)) if onceki is not None else float(np.median(merkez))
        ys[x] = y
        onceki = y
    gecerli = ~np.isnan(ys)
    if gecerli.sum() < max(20, w * 0.2):
        return None
    xs = np.arange(w)
    bas, son = int(np.flatnonzero(gecerli)[0]), int(np.flatnonzero(gecerli)[-1])
    kapsama = float(gecerli[bas:son + 1].mean())
    y = np.interp(xs[bas:son + 1], xs[gecerli], ys[gecerli])
    y = medfilt(y, 5)
    yd = cv2.dilate(m.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    isabet = float(np.mean([yd[int(round(yy)), bas + i] for i, yy in enumerate(y) if 0 <= int(round(yy)) < h]))
    # tekillik: sinyal piksellerinin ne kadarı bulunan izin ±3 px çevresinde (yazı/şema bloğunda düşük kalır)
    yol = np.zeros_like(m)
    for i, yy in enumerate(y):
        r = int(round(yy))
        yol[max(r - 3, 0):min(r + 4, h), bas + i] = True
    tekillik = float((m & yol).sum() / max(m[:, bas:son + 1].sum(), 1))
    yukari = -y                                                     # görüntüde y aşağı artar
    pr = max(h * 0.05, 2)
    tepe, _ = find_peaks(yukari, prominence=pr)
    cukur, _ = find_peaks(-yukari, prominence=pr)
    dy = np.gradient(medfilt(yukari, 7))
    esik = max(h * 0.002, 0.05)
    isaret = np.where(dy > esik, 1, np.where(dy < -esik, -1, 0))
    fazlar, i = [], 0
    while i < len(isaret):
        j = i
        while j + 1 < len(isaret) and isaret[j + 1] == isaret[i]:
            j += 1
        if isaret[i] != 0 and j - i >= 2:
            fazlar.append({"bas": bas + i, "son": bas + j, "faz": "yukselis" if isaret[i] > 0 else "inis"})
        i = j + 1
    adim = max(1, len(y) // 200)
    return {"xs": [bas + k for k in range(0, len(y), adim)], "ys": [float(y[k]) for k in range(0, len(y), adim)],
            "fazlar": fazlar, "tepe": [int(bas + t) for t in tepe], "cukur": [int(bas + c) for c in cukur],
            "kapsama": round(kapsama, 3), "isabet": round(isabet, 3), "tekillik": round(tekillik, 3), "w": w, "h": h, "_y": y, "_bas": bas}


def kapidan_gecer(e: dict | None) -> bool:
    return bool(e) and e["kapsama"] >= KAPSAMA_ESIK and e["isabet"] >= ISABET_ESIK and e["tekillik"] >= TEKILLIK_ESIK


def sayfa_egrisi(ders: str, sayfa: int, resim: str | None, renkli: bool) -> list[dict]:
    import pymupdf
    l0, s = l0kayit.sayfa(ders, sayfa)
    from ortak import pdf_bul
    p = pymupdf.open(pdf_bul(ders))[sayfa - 1]
    W, H = p.rect.width, p.rect.height
    # logo/süs gibi küçük resimler (sayfanın < %3'ü) grafik değildir; açıkça istenirse denenir
    hedefler = [r for r in s["resimler"] if (r["id"].endswith(f"-{resim}") if resim else r.get("alan", 0) >= 0.03)]
    out = []
    for r in hedefler:
        x0, y0, x1, y1 = r["bbox"]
        olcek = 3.0
        pm = p.get_pixmap(matrix=pymupdf.Matrix(olcek, olcek), clip=pymupdf.Rect(x0 * W, y0 * H, x1 * W, y1 * H), alpha=False)
        rgb = np.frombuffer(pm.samples, np.uint8).reshape(pm.height, pm.width, pm.n)[:, :, :3]
        e = egri_cikar(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR), renkli)
        if not kapidan_gecer(e):
            print(f"  {r['id']}: eğri kapıdan geçmedi ({None if not e else (e['kapsama'], e['isabet'])})")
            continue
        sx, sy = (x1 - x0) / e["w"], (y1 - y0) / e["h"]
        out.append({"id": f"{r['id']}-e1", "nokta": [[round(x0 + x * sx, 4), round(y0 + yy * sy, 4)] for x, yy in zip(e["xs"], e["ys"])],
                    "fazlar": [{"bas": round(x0 + f["bas"] * sx, 4), "son": round(x0 + f["son"] * sx, 4), "faz": f["faz"]}
                               for f in e["fazlar"]],
                    "tepe": [round(x0 + t * sx, 4) for t in e["tepe"]], "cukur": [round(x0 + c * sx, 4) for c in e["cukur"]],
                    "kapsama": e["kapsama"], "isabet": e["isabet"]})
    return out


def sinama() -> int:
    """Yapay grafik: pembe ızgara, siyah eksen, EKG benzeri iz (P–QRS–T). Gerçek y bilinir."""
    h, w = 300, 900
    img = np.full((h, w, 3), (230, 225, 250), np.uint8)               # açık pembe zemin (BGR)
    for x in range(0, w, 15):
        cv2.line(img, (x, 0), (x, h), (190, 170, 240), 1)
    for y_ in range(0, h, 15):
        cv2.line(img, (0, y_), (w, y_), (190, 170, 240), 1)
    cv2.line(img, (20, 280), (880, 280), (0, 0, 0), 2)                # x ekseni
    cv2.line(img, (20, 10), (20, 280), (0, 0, 0), 2)                  # y ekseni
    xs = np.arange(40, 860)
    taban = 200.0
    def g(c, s, a): return a * np.exp(-((xs - c) ** 2) / (2 * s ** 2))
    gercek = taban - g(150, 18, 25) + g(260, 6, 30) - g(280, 5, 150) + g(300, 6, 40) - g(420, 30, 45) \
        - g(600, 18, 25) - g(730, 5, 150) - g(870, 30, 45)
    pts = np.stack([xs, gercek], 1).astype(np.int32)
    cv2.polylines(img, [pts], False, (20, 20, 20), 2)
    e = egri_cikar(img)
    if not e:
        print("eğri bulunamadı"); return 1
    y = e["_y"]
    ortak = [(x, y[x - e["_bas"]]) for x in xs if 0 <= x - e["_bas"] < len(y)]
    hata = float(np.mean([abs(yy - gercek[x - 40]) for x, yy in ortak]))
    r_tepe = [t for t in e["tepe"] if abs(t - 280) < 8 or abs(t - 730) < 8]
    yuks = [f for f in e["fazlar"] if f["faz"] == "yukselis" and 260 <= f["son"] <= 290]
    inis = [f for f in e["fazlar"] if f["faz"] == "inis" and 275 <= f["bas"] <= 300]
    print(f"ortalama hata {hata:.2f} px, kapsama {e['kapsama']}, isabet {e['isabet']}, R tepesi {len(r_tepe)}/2, "
          f"tekillik {e['tekillik']}, QRS yükseliş {len(yuks)}, iniş {len(inis)}, kapı {'GEÇER' if kapidan_gecer(e) else 'KALIR'}")
    ok = hata < 2.0 and len(r_tepe) == 2 and yuks and inis and kapidan_gecer(e)
    # olumsuz sınama: düz yazı bloğu eğri sanılmasın
    yazi = np.full((h, w, 3), 255, np.uint8)
    for k in range(8):
        cv2.putText(yazi, "Hucre adaptasyonu ve hasar", (30, 30 + k * 34), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)
    ey = egri_cikar(yazi)
    print(f"yazı bloğu: tekillik {ey and ey['tekillik']}, kapı {'GEÇER (HATA)' if kapidan_gecer(ey) else 'KALIR (doğru)'}")
    return 0 if ok and not kapidan_gecer(ey) else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ders"); ap.add_argument("--sayfa", type=int); ap.add_argument("--resim")
    ap.add_argument("--renkli", action="store_true"); ap.add_argument("--yaz", action="store_true")
    ap.add_argument("--sinama", action="store_true")
    a = ap.parse_args()
    if a.sinama:
        return sinama()
    if not (a.ders and a.sayfa):
        ap.error("--ders ve --sayfa (ya da --sinama)")
    out = sayfa_egrisi(a.ders, a.sayfa, a.resim, a.renkli)
    for e in out:
        print(f"{e['id']}: {len(e['nokta'])} nokta, {len(e['fazlar'])} faz, tepe {len(e['tepe'])}, kapsama {e['kapsama']}")
    if a.yaz and out:
        l0kayit.sayfa_yaz(a.ders, a.sayfa, "egri", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
