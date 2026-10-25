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
        self.gri = gri
        # sayfanın alt kenar rengi (panel için sayfa altına eklenen alan aynı zeminle boyanır, slaytın parçası gibi)
        alt = img[int(self.h * 0.985):, :, :3].reshape(-1, 3)
        self.alt_renk = "#%02x%02x%02x" % tuple(int(v) for v in np.median(alt, axis=0))
        kenar = cv2.Canny(gri, 50, 150)
        self.kenar = cv2.dilate(kenar, np.ones((11, 11), np.uint8)) > 0
        arka = np.median(gri)
        murekkep = (np.abs(gri.astype(int) - int(arka)) > 40).astype(np.uint8)
        self.murekkep = cv2.dilate(murekkep, np.ones((31, 31), np.uint8)) > 0
        # yerleşim için ince mürekkep haritası (yazı/resim pikselleri + 3 px pay): ok rotası, etiket ve şema paneli
        # bunun üstünden en az geçecek şekilde seçilir (içeriğin önü kapanmasın)
        self.ince = cv2.dilate(murekkep, np.ones((7, 7), np.uint8)) > 0
        self.ii = cv2.integral(self.ince.astype(np.uint8))

    def kutu_doluluk(self, x0, y0, x1, y1) -> float:
        """[x0,y0,x1,y1] (0–1) kutusunun mürekkepli oranı (integral görüntü)."""
        a, b = self._px(max(0, x0), max(0, y0))
        c, d = self._px(min(1, x1), min(1, y1))
        if c <= a or d <= b:
            return 1.0
        S = self.ii
        dolu = S[d, c] - S[b, c] - S[d, a] + S[b, a]
        return float(dolu) / ((c - a) * (d - b))

    def yol_doluluk(self, nokta: list) -> float:
        hit = sum(1 for x, y in nokta if self.ince[self._px(x, y)[1], self._px(x, y)[0]])
        return hit / max(1, len(nokta))

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
        if k.get("odak"):
            od = k.get("odak")
            if not (isinstance(od, (list, tuple)) and len(od) == 4 and all(isinstance(v, (int, float)) and 0 <= v <= 1 for v in od)):
                return "odak kutusu geçersiz"
            if od[2] <= od[0] or od[3] <= od[1]:
                return "odak kutusu boyutları geçersiz"
            return None
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
    if tur == "sema" and k.get("sablon"):
        # şablonlu panel (sablon.py coz() düzeni doğrular): görünen her metin o cümleye kadar anlatılanlardan
        from sablon import hucreler
        bilinen = _kok(onceki_metin)
        for c in hucreler(k):
            kk = _kok(c)
            if kk and len(kk - bilinen) > (1 if len(kk) >= 3 else 0):
                return f"panel metni '{c[:30]}' henüz anlatılmamış terim içeriyor (ileri sızıntı)"
        return None
    if tur == "sema":
        dg, kn = k.get("dugum") or [], k.get("kenar") or []
        ids = {d.get("id") for d in dg}
        if not 2 <= len(dg) <= 8 or len(ids) != len(dg):
            return "düğüm sayısı 2–8 ve kimlikler tekil olmalı"
        if not kn or any(e.get("a") not in ids or e.get("b") not in ids or e.get("tur") not in ("aktive", "inhibe", "donusur", "maske", "karsit") for e in kn):
            return "kenar geçersiz"
        bilinen = _kok(onceki_metin)
        for d in dg:
            kk = _kok(str(d.get("metin") or ""))
            if not kk or len(kk - bilinen) > (1 if len(kk) >= 3 else 0):
                return f"düğüm '{d.get('metin')}' henüz anlatılmamış terim içeriyor (ileri sızıntı)"
        return None
    return f"tür '{tur}' tanımsız"


if __name__ == "__main__":
    import argparse
    import json
    import sys
    from pathlib import Path

    ap = argparse.ArgumentParser(description="Canlı çizim komutlarını ve adaylarını denetler")
    ap.add_argument("yol", nargs="?", default=".", help="Taslak dizini ya da cizim_aday.json yolu")
    args = ap.parse_args()

    p = Path(args.yol)
    if p.is_dir():
        aday_yol = p / "cizim_aday.json"
        v2_yol = p / "konusma_v2.json"
    else:
        aday_yol = p
        v2_yol = p.parent / "konusma_v2.json"

    if not aday_yol.exists():
        print(f"HATA: {aday_yol} bulunamadı")
        sys.exit(1)

    data = json.loads(aday_yol.read_text(encoding="utf-8"))
    komutlar = data.get("komutlar", [])
    cizimler = data.get("cizimler", [])

    # load transcript if exists
    sentences = []
    if v2_yol.exists():
        v2 = json.loads(v2_yol.read_text(encoding="utf-8"))
        for b in v2.get("bolumler", []):
            for pr in b.get("paragraflar", []):
                for c in pr.get("cumleler", []):
                    sentences.append(c)
    sent_map = {c["id"]: c for c in sentences}

    def _cum_text(cid):
        txt = []
        for c in sentences:
            txt.append(c.get("ses", ""))
            if c.get("id") == cid:
                break
        return " ".join(txt)

    from sablon import coz as sb_coz, kutuphane as sb_kut
    kut = sb_kut()
    hatalar = []

    for i, k in enumerate(komutlar):
        cid = k.get("cumle")
        c_obj = sent_map.get(cid, {})
        s_words = len(c_obj.get("ses", "").split()) if c_obj else 20
        k_coz, err_s = sb_coz(k, kut) if k.get("sablon") else (k, None)
        if err_s:
            hatalar.append(f"Komut {i} ({cid}): şablon hatası - {err_s}")
            continue
        onceki = _cum_text(cid) if cid in sent_map else ""
        err_d = denetle(k_coz, s_words, [], None, onceki)
        if err_d:
            hatalar.append(f"Komut {i} ({cid}): denetim hatası - {err_d}")

    for h in hatalar[:30]:
        print("HATA:", h)

    print(f"{len(komutlar)} komut · {len(cizimler)} çizim · {len(hatalar)} HATA")
    sys.exit(1 if hatalar else 0)

