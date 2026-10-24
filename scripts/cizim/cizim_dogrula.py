#!/usr/bin/env python3
"""Canlı çizim kapısı (R6, ICERIK_MOTORU_V3.md §4.3). Komut başına denetim; geçmeyen komut ATILIR (ders yayından kalmaz,
imleç/halka yedek olarak kalır).

  kontur / egri_faz : noktalar 0–1, bir resim kutusunun (R#) içinde; temiz basılmış sayfanın kenar haritasında
                      (Canny + 5 px genişletme) noktaların ve ara noktaların ≥%70'i çizgi üstünde (uydurma koordinat elenir);
                      egri_faz x'e göre sıralı, fazlar geçerli aralık
  akis              : a/b sayfa içinde, ≥0,04 uzak, ikisi de mürekkebe 15 px yakın; ilişki aktive|inhibe|donusur
  sema              : 2–8 düğüm, kenarlar var olan düğümlere; her düğüm metni o cümleye KADAR anlatılan terimlerden
                      (ileri sızıntı yok, Kural 7)
  hepsi             : bas ≤ son < kelime sayısı; cümle başına ≤2, sayfa başına ≤8 komut
"""
from __future__ import annotations

import re

import numpy as np

CV = None


def _cv():
    global CV
    if CV is None:
        import cv2
        CV = cv2
    return CV


class SayfaRaster:
    """Bir PDF sayfasının temiz görüntüsünden kenar ve mürekkep haritası (önbellekli)."""

    def __init__(self, sayfa, dpi: int = 110):
        cv2 = _cv()
        pix = sayfa.get_pixmap(dpi=dpi)
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
        gri = cv2.cvtColor(img[:, :, :3], cv2.COLOR_RGB2GRAY)
        self.h, self.w = gri.shape
        kenar = cv2.Canny(gri, 50, 150)
        self.kenar = cv2.dilate(kenar, np.ones((11, 11), np.uint8)) > 0
        arka = np.median(gri)
        murekkep = (np.abs(gri.astype(int) - int(arka)) > 40).astype(np.uint8)
        self.murekkep = cv2.dilate(murekkep, np.ones((31, 31), np.uint8)) > 0

    def _px(self, x, y):
        return min(self.w - 1, max(0, int(x * self.w))), min(self.h - 1, max(0, int(y * self.h)))

    def kenar_orani(self, nokta: list) -> float:
        orn = []
        for (x0, y0), (x1, y1) in zip(nokta, nokta[1:]):
            for t in (0, 0.5):
                orn.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t))
        orn.append(tuple(nokta[-1]))
        hit = sum(1 for x, y in orn if self.kenar[self._px(x, y)[1], self._px(x, y)[0]])
        return hit / max(1, len(orn))

    def murekkepte(self, p) -> bool:
        x, y = self._px(*p)
        return bool(self.murekkep[y, x])


def _ic(p, kutu, tol=0.02) -> bool:
    return kutu[0] - tol <= p[0] <= kutu[2] + tol and kutu[1] - tol <= p[1] <= kutu[3] + tol


def _gecerli_nokta(n) -> bool:
    return isinstance(n, (list, tuple)) and len(n) == 2 and all(isinstance(v, (int, float)) and 0 <= v <= 1 for v in n)


def _kok(s: str) -> set[str]:
    s = s.replace("İ", "i").replace("I", "ı").lower()
    return {w[:5] for w in re.findall(r"[a-zçğıöşü0-9]{4,}", s)}


def denetle(k: dict, kelime_sayisi: int, kutular: list, raster: SayfaRaster | None, onceki_metin: str) -> str | None:
    """→ None (geçti) ya da ret nedeni."""
    if not (isinstance(k.get("bas"), int) and isinstance(k.get("son"), int) and 0 <= k["bas"] <= k["son"] < kelime_sayisi):
        return f"kelime aralığı geçersiz ({k.get('bas')}–{k.get('son')}, cümle {kelime_sayisi} kelime)"
    tur = k.get("tur")
    if tur in ("kontur", "egri_faz"):
        nk = k.get("nokta") or []
        if not (4 if tur == "egri_faz" else 5) <= len(nk) <= (30 if tur == "egri_faz" else 20) or not all(_gecerli_nokta(n) for n in nk):
            return "nokta sayısı/biçimi geçersiz"
        if not kutular:
            return "sayfada resim kutusu yok (kontur/eğri yalnız resim üstünde)"
        if not any(all(_ic(n, b) for n in nk) for b in kutular):
            return "noktalar tek bir resim kutusunun içinde değil"
        if raster is None:
            return "sayfa görüntüsü yok"
        oran = raster.kenar_orani(nk)
        if oran < 0.7:
            return f"noktaların %{round(oran * 100)}'i çizgi üstünde (en az %70)"
        if tur == "egri_faz":
            xs = [n[0] for n in nk]
            if xs != sorted(xs):
                return "eğri noktaları soldan sağa sıralı değil"
            for f in k.get("fazlar") or []:
                a = f.get("aralik") or []
                if f.get("faz") not in ("yukselis", "inis", "plato") or len(a) != 2 or not 0 <= a[0] < a[1] < len(nk):
                    return "faz aralığı/türü geçersiz"
        return None
    if tur == "akis":
        a, b = k.get("a"), k.get("b")
        if not (_gecerli_nokta(a) and _gecerli_nokta(b)):
            return "a/b noktası geçersiz"
        if ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5 < 0.04:
            return "a ile b çok yakın"
        if k.get("iliski") not in ("aktive", "inhibe", "donusur"):
            return "ilişki aktive|inhibe|donusur olmalı"
        if raster is not None and not (raster.murekkepte(a) and raster.murekkepte(b)):
            return "ok uçlarından biri boş alanda (yazı/çizim yok)"
        return None
    if tur == "sema":
        dg, kn = k.get("dugum") or [], k.get("kenar") or []
        ids = {d.get("id") for d in dg}
        if not 2 <= len(dg) <= 8 or len(ids) != len(dg):
            return "düğüm sayısı 2–8 ve kimlikler tekil olmalı"
        if not kn or any(e.get("a") not in ids or e.get("b") not in ids or e.get("tur") not in ("aktive", "inhibe", "donusur") for e in kn):
            return "kenar geçersiz"
        bilinen = _kok(onceki_metin)
        for d in dg:
            kk = _kok(str(d.get("metin") or ""))
            if not kk or len(kk - bilinen) > (1 if len(kk) >= 3 else 0):
                return f"düğüm '{d.get('metin')}' henüz anlatılmamış terim içeriyor (ileri sızıntı)"
        return None
    return f"tür '{tur}' tanımsız"
