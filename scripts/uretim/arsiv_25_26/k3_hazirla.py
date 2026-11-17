#!/usr/bin/env python3
"""2025-2026 Kurul 3 (GİS) arşiv hazırlığı: Drive klasörü envanteri → indirme → PDF metin önizlemesi → ders eşlemesi.

Kurul 2 hattıyla (indir_ve_cikar.py / arsiv_yayinla.py) aynı veri yerleşimi; 2026-2027 veritabanına DOKUNMAZ.

  k3_hazirla.py envanter            → meds_database_25_26/kurul3_kaynak.json  (klasör + dosya listesi, id/ad/mime)
  k3_hazirla.py indir               → pdf/kurul3/_ham/<dosya_id>.<uzantı>  (pptx ise PDF'e çevrilir)
  k3_hazirla.py onizleme            → kurul3_metin.json  {dosya_id: {ad, sayfa, ilk_sayfa_metni, ...}}  (eşleme için)
  k3_hazirla.py listele             → eşleşme tablosunun durumu (hangi ders PDF'siz)
"""
from __future__ import annotations
import sys as _sys
from pathlib import Path as _Path
_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402

import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

MEDS = _kok.MEDS
ROOT = MEDS.parent
DB = ROOT / "meds_database_25_26"
PDF_DIR = DB / "pdf" / "kurul3"
HAM = PDF_DIR / "_ham"
KAYNAK = DB / "kurul3_kaynak.json"
METIN = DB / "kurul3_metin.json"
ESLESME = DB / "kurul3_eslesme.json"

KOK_ID = "14kdfK-kz_Tt3A_SAWCXJD1TzOIjmUBv8"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/122 Safari/537.36"

sys.path.insert(0, str(MEDS / "scripts" / "uretim" / "ders_isci"))


def klasor(fid: str):
    import hizli_bakis as H
    return H.klasor_listesi(fid) or []


def envanter() -> dict:
    if KAYNAK.exists():
        eski = json.loads(KAYNAK.read_text(encoding="utf-8"))
        if eski.get("kok") == KOK_ID and eski.get("dosyalar"):
            return eski
    dosyalar = []

    def gez(fid: str, klasor_adi: str):
        for (i, ad, mime) in klasor(fid):
            if mime.endswith("folder"):
                gez(i, f"{klasor_adi}/{ad}".strip("/"))
            else:
                dosyalar.append({"id": i, "ad": ad, "mime": mime, "klasor": klasor_adi})
    gez(KOK_ID, "")
    out = {"kok": KOK_ID, "dosyalar": dosyalar}
    KAYNAK.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    return out


def drive_indir(file_id: str, hedef: Path) -> Path:
    hedef.parent.mkdir(parents=True, exist_ok=True)
    if hedef.exists() and hedef.stat().st_size > 1024:
        return hedef
    url = f"https://drive.usercontent.google.com/download?id={file_id}&export=download&authuser=0&confirm=t"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    tmp = hedef.with_suffix(hedef.suffix + ".tmp")
    with urllib.request.urlopen(req, timeout=300) as r:
        veri = r.read()
    if len(veri) < 512 or veri[:15].lower().startswith(b"<!doctype html"):
        raise RuntimeError(f"Drive indirme başarısız ({file_id}): {len(veri)} bayt")
    tmp.write_bytes(veri)
    tmp.replace(hedef)
    return hedef


def pdf_yap(ham: Path) -> Path:
    """PPTX → PDF (libreoffice). PDF ise kendisi."""
    if ham.suffix.lower() == ".pdf":
        return ham
    pdf = ham.with_suffix(".pdf")
    if pdf.exists() and pdf.stat().st_size > 1024:
        return pdf
    r = subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", str(ham.parent), str(ham)],
                       capture_output=True, text=True, timeout=300)
    if r.returncode != 0 or not pdf.exists():
        raise RuntimeError(f"PPTX→PDF başarısız: {ham.name}: {r.stderr[-300:]}")
    return pdf


def indir():
    env = envanter()
    for d in env["dosyalar"]:
        uzanti = Path(d["ad"]).suffix.lower() or ".pdf"
        ham = HAM / f"{d['id']}{uzanti}"
        try:
            drive_indir(d["id"], ham)
            pdf = pdf_yap(ham)
            print(f"[OK] {d['klasor']}/{d['ad']} → {pdf.name} ({pdf.stat().st_size // 1024} KB)")
        except Exception as e:  # noqa: BLE001
            print(f"[HATA] {d['ad']}: {e}", file=sys.stderr)


def onizleme():
    """Her PDF'in ilk 2 sayfası + sayfa sayısı → ders eşlemesi için (ucuz, LLM yok)."""
    import pymupdf as fitz
    env = envanter()
    out = json.loads(METIN.read_text(encoding="utf-8")) if METIN.exists() else {}
    for d in env["dosyalar"]:
        ham = HAM / f"{d['id']}{Path(d['ad']).suffix.lower()}"
        pdf = ham.with_suffix(".pdf")
        if not pdf.exists() or pdf.stat().st_size < 1024:
            continue
        if d["id"] in out and out[d["id"]].get("sayfa"):
            continue
        try:
            doc = fitz.open(pdf)
            ilk = "\n".join(doc[i].get_text("text") for i in range(min(2, doc.page_count)))
            out[d["id"]] = {
                "ad": d["ad"], "klasor": d["klasor"], "sayfa": doc.page_count,
                "ilk": re.sub(r"\n{2,}", "\n", ilk.strip())[:1200],
            }
            doc.close()
        except Exception as e:  # noqa: BLE001
            print(f"[HATA] {d['ad']}: {e}", file=sys.stderr)
    METIN.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(out)} PDF önizlemesi → {METIN}")


def listele():
    dersler = json.loads((MEDS / "src/data/dersler/k3.json").read_text(encoding="utf-8"))["dersler"]
    esles = json.loads(ESLESME.read_text(encoding="utf-8")) if ESLESME.exists() else {}
    ters = {v["id"]: k for k, v in esles.items()}
    for d in dersler:
        e = esles.get(d["id"])
        print(f"{d['id']} {d['brans'][:18]:18} {d['konu'][:44]:44} {'✔ ' + e['dosya'] if e else '— PDF yok'}")
    print(f"\nEşleşen: {len(esles)} / {len(dersler)}")
    return 0


def main() -> int:
    a = sys.argv[1] if len(sys.argv) > 1 else "listele"
    {"envanter": envanter, "indir": indir, "onizleme": onizleme, "listele": listele}[a]()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
