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


if __name__ == "__main__":
    import sys

    m, bilgi = pdf_metni(Path(sys.argv[1]))
    print(bilgi)
    print(m[:1500])
