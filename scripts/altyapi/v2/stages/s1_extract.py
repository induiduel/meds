"""s1 — Ham kaynaktan metin çıkarma (PDF/PPTX/DOCX/TXT).

CPU-only: PyMuPDF metin katmanı, yoksa Tesseract (tur) OCR. GPU vision YOK. Doğrulanamayan
dış OCR kabul edilmez; gerekirse `core.llm.vision_ocr` yalnızca açıkça istendiğinde kullanılır.
"""
from __future__ import annotations

import re
from pathlib import Path

from .. import config
from ..core import ids, store

TEXT_EXTS = {".txt", ".md"}
SUPPORTED = {".pdf", ".pptx", ".docx"} | TEXT_EXTS
_MIN_PAGE_CHARS = 40

# Arşiv yolu "kurul N / ders / dosya" düzenindedir. Ders adlarını yoldan çıkarırız.
_DISCIPLINES = [
    "Tıbbi Patoloji", "Patoloji", "Tıbbi Farmakoloji", "Farmakoloji", "İç Hastalıkları", "Dahiliye",
    "Kardiyoloji", "Kalp Damar Cerrahisi", "Göğüs Hastalıkları", "Göğüs Cerrahisi", "Çocuk Hastalıkları",
    "Çocuk Sağlığı", "Pediatri", "Kadın Hastalıkları", "Kadın Doğum", "Enfeksiyon Hastalıkları",
    "Enfeksiyon", "Klinik Mikrobiyoloji", "Nöroloji", "Psikiyatri", "Beyin ve Sinir Cerrahisi",
    "Beyin Cerrahisi", "Fiziksel Tıp ve Rehabilitasyon", "FTR", "Ortopedi", "Travmatoloji",
    "Acil Tıp", "Halk Sağlığı", "Üroloji", "Anestezi", "Tıbbi Biyoloji", "Tıbbi Genetik", "Genetik",
    "Dermatoloji", "Radyoloji", "Nükleer Tıp", "Biyoistatistik", "Tıbbi Mikrobiyoloji",
    "Göğüs", "KVC", "KBB", "Göz",
]
_KURUL = re.compile(r"kurul[\s_\-]*(\d)")
_DONEM = re.compile(r"d[oö]nem[\s_\-]*(\d)")


def infer_path_meta(path: str | Path) -> dict:
    """Dosya yolundan kurul/ders/dönem çıkarır (heuristic). Bulunamayan alan yazılmaz."""
    folded = ids.fold_tr(str(path))
    out: dict = {}
    m = _KURUL.search(folded)
    if m:
        out["kurul"] = int(m.group(1))
    m = _DONEM.search(folded)
    if m:
        out["donem"] = int(m.group(1))
    ders, best = None, 0
    for d in _DISCIPLINES:
        fd = ids.fold_tr(d)
        if fd in folded and len(fd) > best:
            ders, best = d, len(fd)
    if ders:
        out["ders"] = ders
    return out


def _doc_type(path: Path) -> str:
    name = str(path).lower()
    if any(k in name for k in ("çıkmış", "cikmis", "çıkmış", "cikmislar", "soru", "final", "büt", "butunleme")):
        return "past_question"
    if path.suffix.lower() in TEXT_EXTS:
        return "summary"
    return "lecture_slide"


def _pdf_pages(path: Path, ocr: bool) -> tuple[list[str], str]:
    try:
        import pymupdf as fitz  # yeni ad
    except Exception:  # noqa: BLE001
        import fitz  # eski ad

    pages: list[str] = []
    used = "text"
    doc = fitz.open(path)
    try:
        for page in doc:
            text = page.get_text("text") or ""
            if ocr and len(text.strip()) < _MIN_PAGE_CHARS:
                try:
                    import pytesseract
                    from PIL import Image
                    import io

                    pix = page.get_pixmap(dpi=200)
                    img = Image.open(io.BytesIO(pix.tobytes("png")))
                    ocr_text = pytesseract.image_to_string(img, lang="tur")
                    if ocr_text.strip():
                        text = ocr_text
                        used = "ocr" if used != "mixed" else "mixed"
                except Exception:  # noqa: BLE001
                    pass
            pages.append(text)
    finally:
        doc.close()
    return pages, used


def _pptx_pages(path: Path) -> tuple[list[str], str]:
    from pptx import Presentation

    prs = Presentation(str(path))
    pages = []
    for slide in prs.slides:
        parts = []
        for shape in slide.shapes:
            if getattr(shape, "has_text_frame", False):
                parts.append(shape.text_frame.text)
            if getattr(shape, "has_table", False):
                for row in shape.table.rows:
                    parts.append(" | ".join(cell.text for cell in row.cells))
        pages.append("\n".join(p for p in parts if p))
    return pages, "text"


def _docx_pages(path: Path) -> tuple[list[str], str]:
    import docx

    d = docx.Document(str(path))
    text = "\n".join(p.text for p in d.paragraphs)
    return [text], "text"


def extract_document(path: str | Path, *, ocr: bool = False, donem: int = 3) -> dict | None:
    """Bir dosyayı okur; {source, pages:[{page,text}]} döndürür. Desteklenmeyen/boşsa None."""
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED or not path.exists():
        return None

    if suffix == ".pdf":
        raw_pages, extraction = _pdf_pages(path, ocr)
    elif suffix == ".pptx":
        raw_pages, extraction = _pptx_pages(path)
    elif suffix == ".docx":
        raw_pages, extraction = _docx_pages(path)
    else:
        raw_pages, extraction = [path.read_text(encoding="utf-8", errors="replace")], "text"

    md5 = store.sha1_file(path)
    meta = infer_path_meta(path)
    source = {
        "source_id": ids.source_id(md5),
        "drive_id": md5,  # yerel ingest'te Drive yok; md5 kararlı kimlik işlevi görür
        "name": path.stem,
        "path": str(path),
        "md5": md5,
        "version": 1,
        "doc_type": _doc_type(path),
        "donem": meta.get("donem", donem),
        "kurul": meta.get("kurul"),
        "ders": meta.get("ders"),
        "pages": len(raw_pages),
        "extraction": extraction,
        "pipeline_generation": config.PIPELINE_GENERATION,
    }
    pages = [{"page": i + 1, "text": t} for i, t in enumerate(raw_pages) if t and t.strip()]
    source["bos_sayfa"] = sum(1 for t in raw_pages if not t.strip())
    return {"source": source, "pages": pages}


def extract_path(target: str | Path, *, recursive: bool = True, ocr: bool = False) -> list[dict]:
    """Dosya ya da klasörü tarar; her desteklenen dosya için extract_document sonucunu toplar."""
    target = Path(target)
    files: list[Path] = []
    if target.is_file():
        files = [target]
    elif target.is_dir():
        files = sorted(p for p in target.rglob("*") if p.is_file() and p.suffix.lower() in SUPPORTED) \
            if recursive else sorted(p for p in target.glob("*") if p.is_file() and p.suffix.lower() in SUPPORTED)
    out = []
    for f in files:
        doc = extract_document(f, ocr=ocr)
        if doc and doc["pages"]:
            out.append(doc)
    return out
