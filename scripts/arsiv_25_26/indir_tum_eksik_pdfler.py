#!/usr/bin/env python3
"""2025-2026 Kurul 2 arşivinde eksik olan tüm PDF'leri Google Drive'dan indirir ve PPTX olanları PDF'e dönüştürür."""
import os
import sys
import subprocess
import urllib.request
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
ROOT = MEDS.parent
DB_25_26 = ROOT / "meds_database_25_26"
PDF_DIR = DB_25_26 / "pdf" / "kurul2"
PDF_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(MEDS / "scripts" / "arsiv_25_26"))
from paralel_arsiv_isci import KURUL2_ARSIV_LISTESI


def drive_indir(file_id: str, hedef: Path) -> Path:
    if hedef.exists() and hedef.stat().st_size > 1024:
        print(f"  [ATLANDI] Zaten mevcut: {hedef.name} ({hedef.stat().st_size} bayt)")
        return hedef
    url = f"https://drive.usercontent.google.com/download?id={file_id}&export=download&authuser=0&confirm=t"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (medsor-arsiv-25-26)"})
    tmp = hedef.with_suffix(hedef.suffix + ".tmp")
    print(f"  [İNDİRİLİYOR] {hedef.name} (file_id: {file_id})...")
    with urllib.request.urlopen(req, timeout=180) as r:
        data = r.read()
    if len(data) < 512 or data[:15].lower().startswith(b"<!doctype html"):
        raise RuntimeError(f"Drive indirme başarısız ({file_id}): {len(data)} bayt")
    tmp.write_bytes(data)
    tmp.replace(hedef)
    print(f"  [TAMAM] {hedef.name} ({len(data)} bayt)")
    return hedef


def pptx_to_pdf(pptx: Path, pdf_hedef: Path) -> Path:
    if pdf_hedef.exists() and pdf_hedef.stat().st_size > 1024:
        return pdf_hedef
    print(f"  [DÖNÜŞTÜRÜLÜYOR] {pptx.name} -> {pdf_hedef.name}...")
    r = subprocess.run(
        ["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", str(pdf_hedef.parent), str(pptx)],
        capture_output=True, text=True, timeout=300
    )
    uretilen = pdf_hedef.parent / (pptx.stem + ".pdf")
    if r.returncode != 0 or not uretilen.exists():
        raise RuntimeError(f"PPTX → PDF dönüşümü başarısız: {r.stderr}")
    if uretilen != pdf_hedef:
        uretilen.replace(pdf_hedef)
    return pdf_hedef


def main():
    import json
    dl_path = ROOT / "meds_downloads" / "_downloads.json"
    dl = json.loads(dl_path.read_text(encoding="utf-8")) if dl_path.exists() else {}

    print(f"Eksik PDF kontrolü ve indirme başlıyor (Hedef: {PDF_DIR})...")
    indirilen = 0
    hatalar = []

    for item in KURUL2_ARSIV_LISTESI:
        key = item["key"]
        pdf_yol = PDF_DIR / f"{key}.pdf"
        if pdf_yol.exists() and pdf_yol.stat().st_size > 1024:
            continue

        fid = item["file_id"]
        info = dl.get(fid, {})
        orijinal_path = info.get("path", "")
        is_pptx = orijinal_path.lower().endswith(".pptx") or orijinal_path.lower().endswith(".ppt")

        print(f"\n=> {item['kurul_no']:02d}) {key} | {item['baslik']}")
        try:
            if is_pptx:
                pptx_yol = PDF_DIR / f"{key}.pptx"
                drive_indir(fid, pptx_yol)
                pptx_to_pdf(pptx_yol, pdf_yol)
            else:
                drive_indir(fid, pdf_yol)
            indirilen += 1
        except Exception as e:
            print(f"  [HATA] {key}: {e}", file=sys.stderr)
            hatalar.append((key, str(e)))

    print(f"\nİşlem tamamlandı! İndirilen/Dönüştürülen yeni PDF sayısı: {indirilen}")
    if hatalar:
        print(f"{len(hatalar)} derste hata oluştu:")
        for k, err in hatalar:
            print(f"  - {k}: {err}")
    return 1 if hatalar else 0


if __name__ == "__main__":
    sys.exit(main())
