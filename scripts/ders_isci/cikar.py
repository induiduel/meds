"""PDF → sayfa işaretli düz metin (CPU; yerel GPU yok). Önce PyMuPDF metin katmanı; sayfada metin yoksa Tesseract (tur+eng).

Çıktı biçimi (Claude'un alıntıyı sayfasıyla göstermesi için):
    === SAYFA 3 ===
    ...metin...
"""
from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path


def pdf_metni(pdf: Path, ocr_esik: int = 40) -> tuple[str, dict]:
    import pymupdf as fitz  # PyMuPDF

    parcalar, ocr_sayfa = [], []
    tess = shutil.which("tesseract")
    with fitz.open(pdf) as doc:
        for i, sayfa in enumerate(doc, 1):
            t = sayfa.get_text("text").strip()
            if len(t) < ocr_esik and tess:
                with tempfile.TemporaryDirectory() as td:
                    png = Path(td) / "s.png"
                    sayfa.get_pixmap(dpi=200).save(png)
                    r = subprocess.run([tess, str(png), "-", "-l", "tur+eng", "--psm", "3"],
                                       capture_output=True, text=True, timeout=180)
                    if r.returncode == 0 and len(r.stdout.strip()) > len(t):
                        t = r.stdout.strip()
                        ocr_sayfa.append(i)
            parcalar.append(f"=== SAYFA {i} ===\n{t}")
        n = doc.page_count
    metin = "\n\n".join(parcalar)
    return metin, {"sayfa": n, "ocr_sayfalar": ocr_sayfa, "karakter": len(metin)}


def sayfa_varliklari(pdf: Path, hedef: Path, gorsel_esik: float = 0.18, dpi: int = 110) -> dict:
    """Her sayfanın tabloları ve görselleri (GELECEK_PLANLAMASI P2.1). kaynak.md'ye dokunmaz (alıntı denetimi ona bağlı).
    Çıktı: hedef/sayfalar.json + hedef/sayfa_goruntu/<n>.png (görsel ağırlıklı ya da çizim/şema içeren sayfalar).
      sayfalar.json: [{"sayfa", "tablolar": [[[hücre…]…]…], "gorsel_orani", "cizim", "goruntu": "sayfa_goruntu/n.png"|null}]
    Görsel oranı = sayfadaki resim kutularının alanı / sayfa alanı; çizim = vektör yol sayısı (şema, grafik, akış)."""
    import pymupdf as fitz

    (hedef / "sayfa_goruntu").mkdir(parents=True, exist_ok=True)
    out = []
    with fitz.open(pdf) as doc:
        for i, sayfa in enumerate(doc, 1):
            alan = abs(sayfa.rect) or 1.0
            resim = 0.0
            for b in sayfa.get_image_info():
                r = fitz.Rect(b["bbox"]) & sayfa.rect
                resim += abs(r)
            oran = round(min(1.0, resim / alan), 3)
            try:
                cizim = len(sayfa.get_drawings())
            except Exception:  # noqa: BLE001
                cizim = 0
            tablolar = []
            try:
                for t in sayfa.find_tables().tables:
                    satir = [[(h or "").strip() for h in r] for r in t.extract()]
                    if len(satir) >= 2 and max(len(r) for r in satir) >= 2:
                        tablolar.append(satir)
            except Exception:  # noqa: BLE001
                pass
            goruntu = None
            if oran >= gorsel_esik or cizim >= 25:
                goruntu = f"sayfa_goruntu/{i}.png"
                sayfa.get_pixmap(dpi=dpi).save(hedef / goruntu)
            out.append({"sayfa": i, "tablolar": tablolar, "gorsel_orani": oran, "cizim": cizim, "goruntu": goruntu})
    import json
    (hedef / "sayfalar.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    return {"tablo_sayfa": sum(1 for x in out if x["tablolar"]), "tablo": sum(len(x["tablolar"]) for x in out),
            "goruntu_sayfa": sum(1 for x in out if x["goruntu"])}


if __name__ == "__main__":
    import sys

    m, bilgi = pdf_metni(Path(sys.argv[1]))
    print(bilgi)
    print(m[:1500])
