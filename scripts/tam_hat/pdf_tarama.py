#!/usr/bin/env python3
"""Ders PDF'i otomatik tasarım taraması (kullanıcı kararı 2026-10-28; H-PDF, H106, H108 sınıfı hatalar). LLM yok.

  .venv-ocr/bin/python -I scripts/tam_hat/pdf_tarama.py <ders.pdf> [--json rapor.json]
  (PDF: npx tsx scripts/ders_pdf.mts <key>)

Sayfa başına HATA:
  bos_sayfa       : mürekkep < %0,3 (taşan kart, yükseklik eşitliği — H-PDF)
  kenar_ihlali    : yazı kutusu sayfa kenarına 8 pt'den yakın ya da sayfa dışına taşıyor
  ust_uste        : farklı bloklardaki iki yazı satırının kesişimi küçük olanın alanının %30'undan fazla
  dikey_harf      : tek harfli satırların alt alta dizildiği sütun (dar kutuda harf harf kırılma — H108)
UYARI:
  seyrek_sayfa    : son sayfa dışında, doluluk < %3 (özet/başlık sonraki sayfaya itilmiş olabilir)
Çıkış 0 = HATA yok. Rapor sayfa numarasıyla verilir; yalnız o sayfanın kaynağı (kart/tablo) düzeltilir.
"""
from __future__ import annotations

import argparse
import json
import sys

import numpy as np
import pymupdf

KENAR = 8.0  # belge kendi 18 pt boşluğunu kullanır; başlıklar o çizgiye oturur (k2-01 sınaması)


def tara(yol: str) -> tuple[list[str], list[str]]:
    hata, uyari = [], []
    doc = pymupdf.open(yol)
    for i, sayfa in enumerate(doc, 1):
        W, H = sayfa.rect.width, sayfa.rect.height
        pix = sayfa.get_pixmap(dpi=40, colorspace=pymupdf.csGRAY)
        g = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w)
        murekkep = float((g < 235).mean())
        if murekkep < 0.003:
            hata.append(f"s.{i}: bos_sayfa")
            continue
        satirlar = []
        for b in sayfa.get_text("dict")["blocks"]:
            for ln in b.get("lines", []):
                metin = "".join(s["text"] for s in ln["spans"]).strip()
                if metin:
                    satirlar.append((b["number"], pymupdf.Rect(ln["bbox"]), metin))
        for _, r, m in satirlar:
            if r.x0 < KENAR or r.y0 < KENAR or r.x1 > W - KENAR or r.y1 > H - KENAR:
                hata.append(f"s.{i}: kenar_ihlali «{m[:40]}»")
                break
        bulundu = False
        for a in range(len(satirlar)):
            for b in range(a + 1, len(satirlar)):
                (ba, ra, ma), (bb, rb, mb) = satirlar[a], satirlar[b]
                if ba == bb:
                    continue
                k = ra & rb
                if k.is_empty:
                    continue
                kucuk = min(ra.get_area(), rb.get_area()) or 1
                if k.get_area() / kucuk > 0.30:
                    hata.append(f"s.{i}: ust_uste «{ma[:30]}» × «{mb[:30]}»")
                    bulundu = True
                    break
            if bulundu:
                break
        # Şık harfleri (A–E) alt alta durur, kırılma değildir; yalnız başka harflerin ≤14 pt arayla dizilmesi sayılır
        tek = sorted((round(r.x0 / 4), r.y0) for _, r, m in satirlar if len(m) == 1 and m.isalpha() and m not in "ABCDE")
        en_uzun, dizi = 0, 1
        for (xa, ya), (xb, yb) in zip(tek, tek[1:]):
            dizi = dizi + 1 if xa == xb and 0 < yb - ya <= 14 else 1
            en_uzun = max(en_uzun, dizi)
        if en_uzun >= 4:
            hata.append(f"s.{i}: dikey_harf (dar kutuda harf harf kırılma)")
        if murekkep < 0.03 and i < len(doc):
            uyari.append(f"s.{i}: seyrek_sayfa (doluluk %{murekkep * 100:.1f})")
    return hata, uyari


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("--json")
    a = ap.parse_args()
    hata, uyari = tara(a.pdf)
    for h in hata:
        print("HATA", h)
    for w in uyari:
        print("UYARI", w)
    print(f"{len(hata)} HATA · {len(uyari)} UYARI")
    if a.json:
        open(a.json, "w").write(json.dumps({"hata": hata, "uyari": uyari}, ensure_ascii=False, indent=1))
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main())
