#!/usr/bin/env python3
"""Öğrenci notu → L1 kırmızı işaret, HİZALI fark (ICERIK_MOTORU_V3.md §12.1; H — k1-51 kayık not tuzağı).

`scripts/sesli_anlatim/ogrenci_not_isaret.py`'nin mürekkep ve "işaretli kelime" kuralları AYNEN kullanılır (tek kaynak);
eklenenler:
  1. Sayfa eşleme sayfa iziyle (iz.py): öğrenci PDF'inin sayfa sayısı/sırası farklı olabilir (çıkarılmış, eklenmiş sayfa).
  2. Görüntü hizalama: öğrenci sayfası asıl sayfaya `cv2.findTransformECC` (afin) ile oturtulur, fark ondan sonra alınır.
  3. Hizalama kapısı: asıl sayfanın yazı piksellerinin ≥ %85'i hizalı öğrenci sayfasında da yazı olmalı; tutmazsa sayfa
     YAZILMAZ ("hizalanamadı" raporu) — kayık nottan yanlış satır üretilmez.
Çıktı biçimi mevcut okuyucuyla aynı ({surum, kaynak, s: {sayfa: {l, y, b}}}) + `hizalama` raporu:
  meds_database_v2/ders_bilgi/<ders>/l1/ogrenci_not/<not_sha>.json   (sesli ders katmanına yayın ayrı karar)

Kullanım (.venv-ocr):
  ogrenci_not.py --ders k1-51 --not NOT.pdf [--asil ASIL.pdf] [--cikis DOSYA] [--onizle DİZİN]
  ogrenci_not.py --kiyas      mevcut 6 dersin eski çıktısıyla kelime düzeyi uyum + yapay kaydırma sınaması
"""
from __future__ import annotations

import argparse
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "sesli_anlatim"))
import cv2  # noqa: E402
import numpy as np  # noqa: E402
import pymupdf  # noqa: E402

import iz  # noqa: E402
import ogrenci_not_isaret as ONI  # noqa: E402  (mürekkep kuralları tek kaynak)
from ortak import DEPO, KOK, oku, sha_dosya, yaz  # noqa: E402

SURUM = 2
YAZI_UYUM_ESIK = 0.85


def _gri(rgb: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(rgb.astype(np.uint8), cv2.COLOR_RGB2GRAY)


def hizala(not_rgb: np.ndarray, asil_rgb: np.ndarray) -> tuple[np.ndarray, dict]:
    """Öğrenci sayfasını asıl sayfaya afin hizalar. Dönen: hizalı görüntü (int16, asıl boyutunda) + rapor."""
    H, W = asil_rgb.shape[:2]
    a = cv2.resize(not_rgb.astype(np.uint8), (W, H), interpolation=cv2.INTER_AREA) if not_rgb.shape[:2] != (H, W) \
        else not_rgb.astype(np.uint8)
    ga, gb = _gri(a).astype(np.float32) / 255, _gri(asil_rgb).astype(np.float32) / 255
    # mürekkep ECC'yi şaşırtmasın: yalnız asıl sayfanın yazı/çizgi çevresi ağırlıklı (koyu pikseller + komşuluk)
    maske = cv2.dilate((gb < 0.6).astype(np.uint8), np.ones((5, 5), np.uint8))
    warp = np.eye(2, 3, dtype=np.float32)
    cc = None
    try:
        kucuk = 0.5
        ga2, gb2 = cv2.resize(ga, None, fx=kucuk, fy=kucuk), cv2.resize(gb, None, fx=kucuk, fy=kucuk)
        m2 = cv2.resize(maske, (gb2.shape[1], gb2.shape[0]), interpolation=cv2.INTER_NEAREST)
        cc, warp = cv2.findTransformECC(gb2, ga2, warp, cv2.MOTION_AFFINE,
                                        (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 80, 1e-5), m2, 5)
        warp[:, 2] /= kucuk
    except cv2.error:
        warp = np.eye(2, 3, dtype=np.float32)
    hizali = cv2.warpAffine(a, warp, (W, H), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP,
                            borderMode=cv2.BORDER_REPLICATE)
    yazi_b = gb < 0.45
    yazi_a = cv2.dilate((_gri(hizali).astype(np.float32) / 255 < 0.55).astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    uyum = float((yazi_b & yazi_a).sum() / max(yazi_b.sum(), 1))
    kayma = float(np.hypot(warp[0, 2], warp[1, 2]))
    return hizali.astype(np.int16), {"cc": None if cc is None else round(float(cc), 3), "kayma_px": round(kayma, 1),
                                     "olcek": round(float(np.hypot(warp[0, 0], warp[1, 0])), 4), "yazi_uyum": round(uyum, 3)}


def sayfa_eslesmesi(not_belge, asil_belge) -> dict[int, int]:
    """asıl sayfa no → öğrenci sayfa no. Sayfa sayısı eşitse ve görüntüler yakınsa birebir; değilse iz eşlemesi."""
    if len(not_belge) == len(asil_belge):
        uzak = [iz.hamming(iz.phash(iz.sayfa_gri32(a)), iz.phash(iz.sayfa_gri32(b))) for a, b in zip(not_belge, asil_belge)]
        if np.median(uzak) <= 14:
            return {i + 1: i + 1 for i in range(len(asil_belge))}
    def girdi(belge):
        return [{"sayfa": i + 1, "iz": {"metin": None, "gorsel": iz.phash(iz.sayfa_gri32(p))}} for i, p in enumerate(belge)]
    # öğrenci notu çoğu kez taranmış/mürekkepli: yalnız görsel izle (metin katmanına güvenilmez)
    e = iz.eslestir(girdi(not_belge), girdi(asil_belge))
    return {k: v["eski"] for k, v in e.items() if v["eski"]}


def isle(not_pdf: Path, asil_pdf: Path, onizle: Path | None = None, hizalama: bool = True, log=print) -> dict:
    a, b = pymupdf.open(not_pdf), pymupdf.open(asil_pdf)
    es = sayfa_eslesmesi(a, b)
    sayfalar, rapor = {}, {}
    for i in range(len(b)):
        no = i + 1
        if no not in es:
            rapor[str(no)] = {"durum": "eslesmedi"}
            continue
        pa, pb = a[es[no] - 1], b[i]
        W, H = pb.rect.width, pb.rect.height
        asil = ONI.ciz(pb)
        ogr = ONI.ciz(pa)
        if hizalama:
            ogr, r = hizala(ogr, asil)
        else:
            r = {"kayma_px": 0.0, "yazi_uyum": None}
        if hizalama and r["yazi_uyum"] < YAZI_UYUM_ESIK:
            rapor[str(no)] = {"durum": "hizalanamadi", **r}
            continue
        ink = ONI.murekkep(ogr, asil)
        if ink.mean() > 0.25:
            rapor[str(no)] = {"durum": "sayfa_bütünüyle_farkli", **r}
            continue
        lis = ONI.parcalar(ONI.kelimeler(pb), ink)
        rapor[str(no)] = {"durum": "tamam", "not_sayfa": es[no], "parca": len(lis), **r}
        if not lis:
            continue
        lis.sort(key=lambda s: (s[1], s[0]))
        bas, son = [], None
        for q in lis:
            if not (son and q[1] - son[3] < (son[3] - son[1]) * 0.8):
                bas.append([round(q[0] / W, 4), round((q[1] + q[3]) / 2 / H, 4)])
            son = q
        sayfalar[str(no)] = {"l": [[round(s[0] / W, 4), round(s[1] / H, 4), round(s[2] / W, 4), round(s[3] / H, 4)]
                                   for s in lis], "y": [0.965, 0.06], "b": bas}
        if onizle:
            for s in lis:
                pb.draw_rect(pymupdf.Rect(s), color=(1, 0, 0), fill=(1, 0, 0), fill_opacity=0.25, width=0)
    if onizle:
        onizle.mkdir(parents=True, exist_ok=True)
        for k in sayfalar:
            b[int(k) - 1].get_pixmap(dpi=50).save(onizle / f"{asil_pdf.stem[:20]}_{int(k):02d}.png")
    reddedilen = [k for k, v in rapor.items() if v["durum"] != "tamam"]
    if reddedilen:
        log(f"  yazılmayan sayfa: {len(reddedilen)} ({', '.join(k + ':' + rapor[k]['durum'] for k in reddedilen[:6])})")
    return {"surum": SURUM, "kaynak": not_pdf.name, "not_sha": sha_dosya(not_pdf), "asil_sha": sha_dosya(asil_pdf),
            "s": sayfalar, "hizalama": rapor}


# ── kıyas: mevcut çıktılarla uyum + yapay kaydırma ────────────────────────────────────────────────────────────────
def _isaretli_kelimeler(belge, s: dict) -> set[tuple]:
    out = set()
    for k, v in s.items():
        p = belge[int(k) - 1]
        W, H = p.rect.width, p.rect.height
        for w in p.get_text("words"):
            cx, cy = (w[0] + w[2]) / 2 / W, (w[1] + w[3]) / 2 / H
            if any(r[0] - 0.003 <= cx <= r[2] + 0.003 and r[1] - 0.003 <= cy <= r[3] + 0.003 for r in v["l"]):
                out.add((int(k), round(w[0], 1), round(w[1], 1)))
    return out


def kiyas() -> int:
    eski_dizin = KOK / "data" / "sesli_anlatim" / "ogrenci_not"
    for notf, asilf, fid in ONI.DERSLER:
        nf = next((x for x in ONI.NOT.glob("*.pdf")
                   if unicodedata.normalize("NFC", x.name) == unicodedata.normalize("NFC", notf)), ONI.NOT / notf)
        asil = ONI.ASIL / asilf
        eski = (oku(eski_dizin / f"{fid}.json") or {}).get("s", {})
        yeni = isle(nf, asil, log=lambda *_: None)
        b = pymupdf.open(asil)
        E, Y = _isaretli_kelimeler(b, eski), _isaretli_kelimeler(b, yeni["s"])
        kay = [v.get("kayma_px", 0) for v in yeni["hizalama"].values() if v.get("durum") == "tamam"]
        red = sum(1 for v in yeni["hizalama"].values() if v["durum"] != "tamam")
        print(f"{asilf[:42]:42} eski {len(E):4} yeni {len(Y):4} ortak {len(E & Y):4} "
              f"(uyum {2 * len(E & Y) / max(len(E) + len(Y), 1):.2f}) kayma ort {np.mean(kay) if kay else 0:.1f}px  ret {red}")
    # yapay kayma: öğrenci sayfasını 7 px kaydır + %1,5 büyüt → hizasız yöntem yanlış satır üretir, hizalı yöntem üretmez
    notf, asilf, fid = ONI.DERSLER[0]
    nf = next((x for x in ONI.NOT.glob("*.pdf")
               if unicodedata.normalize("NFC", x.name) == unicodedata.normalize("NFC", notf)), ONI.NOT / notf)
    a, b = pymupdf.open(nf), pymupdf.open(ONI.ASIL / asilf)
    toplam = {"hizasiz_fazla": 0, "hizali_fazla": 0, "dogru": 0}
    for i in range(min(len(a), len(b), 12)):
        asil, ogr = ONI.ciz(b[i]), ONI.ciz(a[i])
        dogru = ONI.parcalar(ONI.kelimeler(b[i]), ONI.murekkep(ogr, asil))
        M = np.float32([[1.015, 0, 7], [0, 1.015, 5]])
        kaymis = cv2.warpAffine(ogr.astype(np.uint8), M, (ogr.shape[1], ogr.shape[0]), borderMode=cv2.BORDER_REPLICATE).astype(np.int16)
        hizasiz = ONI.parcalar(ONI.kelimeler(b[i]), ONI.murekkep(kaymis, asil))
        hz, r = hizala(kaymis, asil)
        hizali = ONI.parcalar(ONI.kelimeler(b[i]), ONI.murekkep(hz, asil)) if r["yazi_uyum"] >= YAZI_UYUM_ESIK else []
        def kume(x): return {(round(q[0]), round(q[1])) for q in x}
        D = kume(dogru)
        toplam["dogru"] += len(D)
        toplam["hizasiz_fazla"] += len(kume(hizasiz) - D)
        toplam["hizali_fazla"] += len(kume(hizali) - D)
    print(f"yapay kayma (7,5 px, ×1,015; 12 sayfa): doğru parça {toplam['dogru']}, hizasız yanlış parça {toplam['hizasiz_fazla']},"
          f" hizalı yanlış parça {toplam['hizali_fazla']}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ders")
    ap.add_argument("--not", dest="not_pdf")
    ap.add_argument("--asil")
    ap.add_argument("--cikis")
    ap.add_argument("--onizle", type=Path)
    ap.add_argument("--kiyas", action="store_true")
    a = ap.parse_args()
    if a.kiyas:
        return kiyas()
    if not (a.ders and a.not_pdf):
        ap.error("--ders ve --not gerekli (ya da --kiyas)")
    from ortak import pdf_bul
    asil = Path(a.asil) if a.asil else pdf_bul(a.ders)
    sonuc = isle(Path(a.not_pdf), asil, a.onizle)
    hedef = Path(a.cikis) if a.cikis else DEPO / a.ders / "l1" / "ogrenci_not" / f"{sonuc['not_sha']}.json"
    yaz(hedef, sonuc)
    print(f"{a.ders}: işaretli sayfa {len(sonuc['s'])}, parça {sum(len(v['l']) for v in sonuc['s'].values())} → {hedef}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
