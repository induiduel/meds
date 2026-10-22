#!/usr/bin/env python3
"""Öğrenci notu PDF'indeki işaretli (önemli) yerler → sesli dersteki asıl PDF'te kırmızı marker + sayfa başına 1 yıldız.

Öğrenci notu, amfi slaytının aynısının üzerine alınmış el işaretleridir (altı çizili, fosforlu, daire, yıldız, el yazısı).
Her sayfa asıl ders PDF'iyle aynı çözünürlükte çizilir; fark pikselleri = mürekkep. Asıl PDF'in metin satırlarından
mürekkebe değenler (üstünü boyayan, altını çizen ya da çevreleyen) "önemli satır" olur. Köşe karalamaları ve metne
değmeyen el yazısı satır sayılmaz. Sayfada önemli yer varsa sağ üst köşeye tek yıldız konur.

Çıktı: data/sesli_anlatim/ogrenci_not/<Drive fileId>.json
  { surum, kaynak, s: { "<sayfa>": { l: [[x0,y0,x1,y1], …], y: [x, y], b: [[x, y], …] }  (b: işaretli pasaj başları) } }   (sayfa oranı 0–1)
Sunucu (canliDers.ts) bu dosyayı dersin hizalamasındaki dosya kimliğiyle bulur; aynı PDF'i kullanan V1 ve V2 ikisi de gösterir.

Kullanım (.venv-ocr): python scripts/sesli_anlatim/ogrenci_not_isaret.py [--onizle DIZIN]
Yalnız CPU.
"""
from __future__ import annotations

import argparse
import json
import unicodedata
import os
from pathlib import Path

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")
import numpy as np  # noqa: E402
import pymupdf  # noqa: E402

MEDS = Path(__file__).resolve().parents[2]
ASIL = MEDS.parent / "meds_downloads" / "drive_root" / "Kurul 1"
NOT = Path(os.environ.get("OGRENCI_NOT_DIZIN", str(Path.home() / "İndirilenler")))
CIKTI = MEDS / "data" / "sesli_anlatim" / "ogrenci_not"
SURUM = 1
DPI = 72  # 960×540 sayfa → 960×540 piksel

# (öğrenci notu dosyası, asıl ders PDF'i, Drive fileId)
DERSLER = [
    ("Üriner Obstrüksiyonders pptx_260918_144127.pdf", "Üroloji/1)Üriner Obstrüksiyon; Patofizyoloji, Klinik ve Tedavi.pdf", "1dIUpRGGlkJsuyK4rrTqUBw3V82cQazvv"),
    ("22-23 Ürolitiyazis Patofizyolojisi_260923_135832.pdf", "Üroloji/2)Ürolitiyazis Patofizyolojisi.pdf", "1bvyIs3jM82_zu3HwqDr6t_wfMNTI9_eD"),
    ("4)'Üriner Sistem Enfeksiyonlarının Epidemiyoloji, _260930_103812.pdf", "Üroloji/4)'Üriner Sistem Enfeksiyonlarının Epidemiyoloji, Etyoloji ve Semptomatolojisi'.pdf", "1wsnQe7-lUuwTTyAhBWZbQbFm4-DzcciE"),
    ("yeni spesifik_261001_105814.pdf", "Üroloji/5) Üriner Sistemin Spesifik Enfeksiyonları.pdf", "1HJWgSxlk0an9wqpLHU2z319wEOi26D_L"),
    ("enürezis_261012_113028.pdf", "Üroloji/6)Enürezis.pdf", "1HxaHEJLrssKterb0N8BlH_ePCZ4FqOfV"),
    ("55 İmmunofarmakoloji.pdf", "Tıbbi Farmakoloji/1)İmmunofarmakoloji.pdf", "1xbAdOVfCOECQYYRkaL3lOqZSN-5pXGJj"),
]


def ciz(p: pymupdf.Page) -> np.ndarray:
    pm = p.get_pixmap(dpi=DPI, alpha=False)
    return np.frombuffer(pm.samples, np.uint8).reshape(pm.h, pm.w, pm.n)[:, :, :3].astype(np.int16)


def murekkep(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Öğrenci sayfasında asıl sayfada olmayan belirgin renk/koyuluk farkı; tek piksellik kenar gürültüsü atılır."""
    # yalnız renkli mürekkep (kalem/fosforlu): kayan siyah yazı kenarı gri kalır, işaret sayılmaz
    renk = (a.max(axis=2) - a.min(axis=2)) >= 60
    f = (np.abs(a - b).max(axis=2) > 70) & renk
    # kenar yumuşatma farkı: en az 2 komşusu da farklı olan pikseller
    k = f.astype(np.int8)
    n = k[:-2, 1:-1] + k[2:, 1:-1] + k[1:-1, :-2] + k[1:-1, 2:]
    out = np.zeros_like(f)
    out[1:-1, 1:-1] = f[1:-1, 1:-1] & (n >= 2)
    return out


def kelimeler(p: pymupdf.Page) -> list[tuple]:
    """(x0, y0, x1, y1, blok, satır) — madde imleri ve tek harfler sayılmaz."""
    return [w[:4] + (w[5], w[6]) for w in p.get_text("words") if len(w[4].strip("•–-·▪➢")) >= 2]


def _yatay(ink: np.ndarray, ya: int, yb: int, xa: int, xb: int) -> float:
    """Bant içindeki en iyi İNCE yatay çizginin (3 piksel) kelime genişliğini kaplama oranı. Komşu satırın fosforlusu
    (üstünde ya da altında 5 piksel ötede de dolu) çizgi sayılmaz."""
    ya, yb = max(0, ya), min(ink.shape[0], yb)
    if yb - ya < 1:
        return 0.0
    kol = ink[:, xa:xb]
    kap = lambda r: kol[max(0, r - 1):r + 2].any(axis=0).mean() if 0 <= r < kol.shape[0] else 0.0
    en = 0.0
    for r in range(ya, yb):
        c = kap(r)
        if c > en and max(kap(r - 5), kap(r + 5)) < 0.3:
            en = c
    return en


def isaretli(ink: np.ndarray, b) -> bool:
    """Kelime gerçekten işaretli mi (sayfayı çapraz geçen kalem çizgisi sayılmaz):
    fosforlu = kelime kutusunun ≥%30'u mürekkep; altı çizili = altında kelimenin ≥%60'ını geçen yatay çizgi;
    daire = üstte ve altta ≥%50'lik yay."""
    x0, y0, x1, y1 = (int(round(v)) for v in b[:4])
    h = max(4, y1 - y0)
    xa, xb = max(0, x0), min(ink.shape[1], x1)
    if xb - xa < 4:
        return False
    ic = ink[max(0, y0):min(ink.shape[0], y1), xa:xb]
    if ic.size and ic.mean() >= 0.30:
        return True
    alt = _yatay(ink, y1 - h // 5, y1 + int(h * 0.6), xa, xb)
    if alt >= 0.6:
        return True
    ust = _yatay(ink, y0 - h // 2, y0 + h // 5, xa, xb)
    return alt >= 0.5 and ust >= 0.5


def parcalar(ws: list[tuple], ink: np.ndarray) -> list[list[float]]:
    """Aynı satırda art arda işaretli kelimeler tek marker parçası olur."""
    out: list[list[float]] = []
    onceki = None
    for w in ws:
        if not isaretli(ink, w):
            onceki = None
            continue
        anahtar = (w[4], w[5])
        if onceki == anahtar and out and w[0] - out[-1][2] < (w[3] - w[1]) * 1.2:
            r = out[-1]
            r[1], r[2], r[3] = min(r[1], w[1]), w[2], max(r[3], w[3])
        else:
            out.append(list(w[:4]))
        onceki = anahtar
    return out


def isle(not_pdf: Path, asil_pdf: Path, onizle: Path | None, ad: str) -> dict:
    a, b = pymupdf.open(not_pdf), pymupdf.open(asil_pdf)
    if len(a) != len(b):
        raise SystemExit(f"{ad}: sayfa sayısı farklı ({len(a)} ≠ {len(b)})")
    sayfalar = {}
    for i in range(len(b)):
        pa, pb = a[i], b[i]
        W, H = pb.rect.width, pb.rect.height
        ink = murekkep(ciz(pa), ciz(pb))
        if ink.mean() > 0.25:  # sayfa bütünüyle farklı (yeniden dizilmiş slayt): güvenilmez
            continue
        lis = parcalar(kelimeler(pb), ink)
        if not lis:
            continue
        lis.sort(key=lambda s: (s[1], s[0]))
        yildiz = [0.965, 0.06]  # sayfa başına bir yıldız: sağ üst köşe (metni örtmez)
        # işaretli metnin başına küçük yıldız: art arda satırlardaki parçalar tek pasaj sayılır, yıldız pasajın başına
        bas, son = [], None
        for r in lis:
            if not (son and r[1] - son[3] < (son[3] - son[1]) * 0.8):
                bas.append([round(r[0] / W, 4), round((r[1] + r[3]) / 2 / H, 4)])
            son = r
        sayfalar[str(i + 1)] = {
            "l": [[round(s[0] / W, 4), round(s[1] / H, 4), round(s[2] / W, 4), round(s[3] / H, 4)] for s in lis],
            "y": [round(yildiz[0], 4), round(yildiz[1], 4)],
            "b": bas,
        }
        if onizle:
            for s in lis:
                pb.draw_rect(pymupdf.Rect(s), color=(1, 0, 0), fill=(1, 0, 0), fill_opacity=0.25, width=0)
            pb.draw_circle((yildiz[0] * W, yildiz[1] * H), 7, color=(1, 0.6, 0), fill=(1, 0.6, 0))
    if onizle:
        onizle.mkdir(parents=True, exist_ok=True)
        for k in sayfalar:
            b[int(k) - 1].get_pixmap(dpi=50).save(onizle / f"{ad}_{int(k):02d}.png")
    return sayfalar


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--onizle", type=Path)
    ar = ap.parse_args()
    CIKTI.mkdir(parents=True, exist_ok=True)
    for notf, asilf, fid in DERSLER:
        nf = next((x for x in NOT.glob('*.pdf') if unicodedata.normalize('NFC', x.name) == unicodedata.normalize('NFC', notf)), NOT / notf)
        s = isle(nf, ASIL / asilf, ar.onizle, fid[:6])
        (CIKTI / f"{fid}.json").write_text(json.dumps({"surum": SURUM, "kaynak": notf, "s": s}, ensure_ascii=False))
        print(f"{asilf[:40]:40} işaretli sayfa {len(s):3}  satır {sum(len(v['l']) for v in s.values())}")


if __name__ == "__main__":
    main()
