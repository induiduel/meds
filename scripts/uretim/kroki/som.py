#!/usr/bin/env python3
"""Set-of-Mark (SoM) bölgeleri — resim içindeki yapıların betikle bulunan poligonları + numaralı kopya (§12.1, §17.1).

Görsel modele ham görüntü gönderilmez: bu betik resim kutusu içindeki belirgin yapıları (Canny kenar → genişletme →
dış konturlar; alan %0,4–%50; IoU > 0,6 çakışanlardan büyüğü; en çok 15) bulur, her birine numara basar. Model
(R4 `som_sec` görevi) yalnız NUMARA seçer; koordinat ve poligon buradan gelir (sapma yok).
Çıktı:
  L0 sayfasına `roi: [{id: <resim>-rN, no, bbox, poligon (≤40 nokta), alan, etiket}]` (etiket = bölgeye düşen L0 sözcükleri)
  meds_temp/kroki/<ders>/som/pNN.webp (numaralı kopya) + pNN.json (numara → roi kimliği)

Kullanım (.venv-ocr): som.py --ders k1-03 [--sayfa 13] [--yaz]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cv2  # noqa: E402
import numpy as np  # noqa: E402
import pymupdf  # noqa: E402

import l0kayit  # noqa: E402
from ortak import TEMP, pdf_bul, yaz  # noqa: E402

EN_COK = 15


def _iou(a, b) -> float:
    x0, y0, x1, y1 = max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])
    k = max(0, x1 - x0) * max(0, y1 - y0)
    return k / max((a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - k, 1e-9)


def bolgeler(bgr: np.ndarray) -> list[dict]:
    h, w = bgr.shape[:2]
    gri = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    kenar = cv2.Canny(cv2.GaussianBlur(gri, (3, 3), 0), 50, 150)
    kenar = cv2.dilate(kenar, np.ones((3, 3), np.uint8), iterations=2)
    kont, _ = cv2.findContours(kenar, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    aday = []
    for c in kont:
        x, y, cw, ch = cv2.boundingRect(c)
        alan = cw * ch / (w * h)
        if 0.004 <= alan <= 0.5 and min(cw, ch) >= 8:
            cevre = cv2.arcLength(c, True)
            p = cv2.approxPolyDP(c, 0.01 * cevre, True).reshape(-1, 2)
            if len(p) > 40:
                p = p[np.linspace(0, len(p) - 1, 40).astype(int)]
            aday.append({"kutu": (x / w, y / h, (x + cw) / w, (y + ch) / h), "poligon": p / [w, h], "alan": alan})
    aday.sort(key=lambda r: -r["alan"])
    secilen: list[dict] = []
    for r in aday:
        if all(_iou(r["kutu"], s["kutu"]) <= 0.6 for s in secilen):
            secilen.append(r)
        if len(secilen) >= EN_COK:
            break
    return secilen


def sayfa_som(belge, l0_sayfa: dict, ders: str) -> tuple[list[dict], np.ndarray | None]:
    p = belge[l0_sayfa["sayfa"] - 1]
    W, H = p.rect.width, p.rect.height
    olcek = 1400 / max(W, 1)
    pm = p.get_pixmap(matrix=pymupdf.Matrix(olcek, olcek), alpha=False)
    tum = cv2.cvtColor(np.frombuffer(pm.samples, np.uint8).reshape(pm.height, pm.width, pm.n)[:, :, :3], cv2.COLOR_RGB2BGR)
    roi, no = [], 0
    for r in l0_sayfa["resimler"]:
        if r.get("alan", 0) < 0.04:
            continue
        x0, y0, x1, y1 = r["bbox"]
        X0, Y0, X1, Y1 = int(x0 * pm.width), int(y0 * pm.height), int(x1 * pm.width), int(y1 * pm.height)
        kes = tum[Y0:Y1, X0:X1]
        if kes.size == 0:
            continue
        for b in bolgeler(kes):
            no += 1
            bx = [x0 + b["kutu"][0] * (x1 - x0), y0 + b["kutu"][1] * (y1 - y0),
                  x0 + b["kutu"][2] * (x1 - x0), y0 + b["kutu"][3] * (y1 - y0)]
            etiket = " ".join(k[4] for k in l0_sayfa["kelimeler"]
                              if k[0] >= bx[0] - 0.003 and k[2] <= bx[2] + 0.003 and k[1] >= bx[1] - 0.003 and k[3] <= bx[3] + 0.003)
            roi.append({"id": f"{r['id']}-r{no}", "no": no, "bbox": [round(v, 4) for v in bx],
                        "poligon": [[round(x0 + px * (x1 - x0), 4), round(y0 + py * (y1 - y0), 4)] for px, py in b["poligon"]],
                        "alan": round(b["alan"], 4), "etiket": etiket[:120]})
    if not roi:
        return [], None
    kat = tum.copy()
    for r in roi:
        poly = (np.array(r["poligon"]) * [pm.width, pm.height]).astype(np.int32)
        cv2.polylines(kat, [poly], True, (0, 140, 255), 2)
    tum = cv2.addWeighted(kat, 0.6, tum, 0.4, 0)
    for r in roi:
        cx, cy = int(r["bbox"][0] * pm.width) + 4, int(r["bbox"][1] * pm.height) + 4
        cv2.circle(tum, (cx + 11, cy + 11), 13, (255, 255, 255), -1)
        cv2.circle(tum, (cx + 11, cy + 11), 13, (0, 90, 220), 2)
        cv2.putText(tum, str(r["no"]), (cx + (5 if r["no"] < 10 else 1), cy + 17), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    return roi, tum


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ders", required=True); ap.add_argument("--sayfa", type=int); ap.add_argument("--yaz", action="store_true")
    a = ap.parse_args()
    l0 = l0kayit.yukle(a.ders)
    belge = pymupdf.open(pdf_bul(a.ders))
    hedef = TEMP / "kroki" / a.ders / "som"
    hedef.mkdir(parents=True, exist_ok=True)
    yazilacak, toplam = {}, 0
    for s in l0["sayfalar"]:
        if a.sayfa and s["sayfa"] != a.sayfa:
            continue
        roi, goruntu = sayfa_som(belge, s, a.ders)
        if not roi:
            continue
        toplam += len(roi)
        cv2.imwrite(str(hedef / f"p{s['sayfa']:02d}.webp"), goruntu, [cv2.IMWRITE_WEBP_QUALITY, 70])
        yaz(hedef / f"p{s['sayfa']:02d}.json", {str(r["no"]): r["id"] for r in roi}, 1)
        yazilacak[s["sayfa"]] = {"roi": roi}
        print(f"  s{s['sayfa']}: {len(roi)} bölge")
    if a.yaz and yazilacak:
        l0kayit.yaz_toplu(a.ders, yazilacak)
    print(f"{a.ders}: {toplam} bölge, {len(yazilacak)} sayfa → {hedef}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
