#!/usr/bin/env python3
"""
PDF / PPTX okuma ajanı (downloads -> temp1).

PROJE_TANITIMI.md'deki 1. aşama: ham kaynaktan ilk veriyi çıkarır. Tamamen yerel çalışır
(PyMuPDF, python-pptx, Tesseract[tur]) ve taranmış sayfalar/slayt görselleri için bulut görsel model (Gemini,
ücretsiz anahtarlar; Tesseract'la kelime örtüşmesiyle doğrulanır). Yerel AI modeli kullanılmaz.

Her kaynak için temp1 altında iki dosya üretilir:
  <ad>.md    okunabilir ham metin ("## Sayfa N" / "## Slayt N" bölümleri)
  <ad>.json  sayfa sayfa metin + yöntem (metin/ocr/vision) + kaynak sha256 + meta

Kullanım:
  read_document.py DOSYA_VEYA_KLASÖR [...] [--out DİZİN] [--force] [--vision] [--docling] [--no-ocr]
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib  # noqa: E402  (OCR çöp tespiti, kalite puanı, hafif model) — eksikti: "name 'lib' is not defined"

PROJECT_ROOT = Path(__file__).resolve().parents[3]  # .../MedSoru Project
DEFAULT_DOWNLOADS = Path(os.environ.get("MEDS_DOWNLOADS_DIR") or PROJECT_ROOT / "meds_downloads")
DEFAULT_TEMP1 = Path(os.environ.get("MEDS_TEMP_DIR") or PROJECT_ROOT / "meds_temp") / "temp1"
OCR_LANG = os.environ.get("MEDS_OCR_LANG", "tur+eng")
OCR_DPI = int(os.environ.get("MEDS_OCR_DPI", "250"))
MIN_TEXT_CHARS = 40  # bunun altındaki sayfalar "metinsiz" sayılır ve OCR'a gider

SUPPORTED = {".pdf", ".pptx", ".ppt"}


# --------------------------------------------------------------------------- yardımcılar
def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def clean_raw(text: str) -> str:
    """temp1 için yalnızca güvenli temizlik: NUL/kontrol karakterleri. Asıl düzeltme temp2'de yapılır."""
    text = text.replace("\x00", "")
    text = re.sub(r"[\x01-\x08\x0b\x0c\x0e-\x1f]", "", text)
    return text.replace("\r\n", "\n").strip()


def preprocess_image_for_ocr(pil_img):
    """
    1. Görüntü Ön İşleme (Pre-Processing) Pipelini:
    - 2x Upscaling (LANCZOS)
    - Kontrast artırma ve binarizasyon
    """
    try:
        from PIL import ImageEnhance, ImageOps
        # Çözünürlük Büyütme (Upscaling)
        w, h = pil_img.size
        if w < 1200 or h < 900:
            pil_img = pil_img.resize((w * 2, h * 2), Image.Resampling.LANCZOS)
        # Gri tonlama & Kontrast artırma
        gray = ImageOps.grayscale(pil_img)
        enhancer = ImageEnhance.Contrast(gray)
        adjusted = enhancer.enhance(1.6)
        return adjusted
    except Exception:
        return pil_img


def ocr_image(img) -> str:
    """Tesseract (tur+eng). psm 3: otomatik sayfa bölütleme — iki sütunlu sınav sayfalarında sütunları karıştırmaz
    (psm 6 tüm sayfayı tek blok sanıp iki sütunun satırlarını iç içe geçiriyordu)."""
    import pytesseract
    try:
        return pytesseract.image_to_string(img, lang=OCR_LANG, config="--oem 1 --psm 3")
    except Exception:
        return ""


# Bulut görsel okuma (Gemini) varsayılan olarak açık: taranmış sayfalarda en yüksek doğruluk. Kapatmak: MEDS_OCR_CLOUD=0
# Aşama 1 varsayılan yerel (PyMuPDF + Tesseract). Bulut görsel OCR (yalnız ÜCRETSİZ Gemini anahtarları) panel ayarı
# (meds_temp/state/ingest_settings.json → "bulut_ocr") ya da MEDS_OCR_CLOUD=1 ile açılır.
INGEST_SETTINGS = Path(os.environ.get("MEDS_TEMP_DIR") or Path(__file__).resolve().parents[3] / "meds_temp") / "state" / "ingest_settings.json"


def _cloud_ocr_enabled() -> bool:
    try:
        return bool(json.loads(INGEST_SETTINGS.read_text(encoding="utf-8")).get("bulut_ocr"))
    except Exception:
        return os.environ.get("MEDS_OCR_CLOUD", "0") == "1"


CLOUD_OCR = _cloud_ocr_enabled()
_WORD = re.compile(r"[0-9A-Za-zÇĞİÖŞÜçğıöşüÂâÎîÛû]{4,}")


def _fold(w: str) -> str:
    return w.translate(str.maketrans("ÇĞİIÖŞÜçğıöşüâîû", "cgiiosucgiosuaiu")).lower()


def ocr_support(cloud_text: str, tess_text: str) -> float:
    """Bulut metnindeki kelimelerin Tesseract çıktısında da geçme oranı (5 harflik kök eşleşmesi).
    Görsel modelin metin uydurmasını/yeniden yazmasını yakalar; Tesseract hataları kısmi eşleşmeyle tolere edilir."""
    cw = [_fold(w) for w in _WORD.findall(cloud_text)]
    if not cw:
        return 0.0
    tw = {_fold(w)[:5] for w in _WORD.findall(tess_text)}
    return sum(1 for w in cw if w[:5] in tw) / len(cw)


def vision_ocr(png_bytes: bytes, pil_img=None) -> str:
    """Bulut görsel model (Gemini) ile birebir metin çıkarımı. Yanıt yoksa boş."""
    import cloud_llm
    out = cloud_llm.vision_ocr(png_bytes)
    return out or ""


def online_web_ocr(png_bytes: bytes) -> str:
    """Son çare: ücretsiz web OCR (bulut görsel ve Tesseract ikisi de yetersizse)."""
    import requests
    try:
        r = requests.post(
            "https://api.ocr.space/parse/image",
            files={"file": ("image.png", png_bytes, "image/png")},
            data={"apikey": "helloworld", "language": "tur", "OCREngine": "2"},
            timeout=20,
        )
        if r.status_code == 200:
            return "\n".join(i.get("ParsedText", "").strip() for i in r.json().get("ParsedResults", []) if i.get("ParsedText")).strip()
    except Exception as e:
        print(f"  [uyarı] Web OCR hatası: {e}", file=sys.stderr)
    return ""


def read_image_text(pil_img, use_ocr: bool, use_vision: bool, cloud_needs_text: bool = False) -> tuple[str, str]:
    """Görüntüden metin. Sıra: Tesseract (her zaman, doğrulama tabanı) + bulut görsel model (Gemini).
    Seçim — metin hiçbir modelle yeniden yazılmaz:
      * bulut metni Tesseract'la ≥%35 kelime örtüşüyorsa → bulut_ocr (doğrulandı)
      * Tesseract okuyamadıysa (çok kısa/çöp) → bulut_ocr_dogrulanamadi (yine de en iyi kaynak)
      * örtüşme düşük ve Tesseract okunabilirse → Tesseract (bulut metni şüpheli)
    """
    use_cloud = _cloud_ocr_enabled()   # panel ayarı her sayfada okunur (izleyici yeniden başlatılmadan geçerli)
    if not use_ocr and not use_cloud:
        return "", "yok"
    proc_img = preprocess_image_for_ocr(pil_img)
    tess = ""
    if use_ocr:
        raw = clean_raw(ocr_image(proc_img))
        tess = "" if lib.is_ocr_garbage(raw) else raw

    cloud = ""
    # Küçük slayt görselleri (simge, logo): Tesseract hiç yazı görmediyse bulut kotası harcanmaz.
    # Büyük görseller (taranmış slayt, şema, tablo resmi) her zaman bulutta okunur.
    if cloud_needs_text and pil_img.width * pil_img.height < 500 * 350 and len(_WORD.findall(tess)) < 3:
        use_cloud = False
    if use_cloud:
        buf = io.BytesIO()
        img = pil_img.convert("RGB")
        if max(img.size) > 2400:                       # gereksiz büyük görüntüyü küçült (hız + kota)
            img.thumbnail((2400, 2400))
        img.save(buf, format="PNG")
        try:
            raw = clean_raw(vision_ocr(buf.getvalue()))
            cloud = "" if (not raw or lib.is_ocr_garbage(raw)) else raw
        except Exception as e:
            print(f"  [uyarı] bulut görsel okuma başarısız: {e}", file=sys.stderr)

    if cloud:
        tess_words = len(_WORD.findall(tess))
        if tess_words < 15:
            return cloud, "bulut_ocr_dogrulanamadi"
        sup = ocr_support(cloud, tess)
        if sup >= 0.35:
            return cloud, "bulut_ocr"
        print(f"  [uyarı] bulut metni Tesseract'la az örtüşüyor (%{sup * 100:.0f}); Tesseract kullanıldı", file=sys.stderr)
    if tess:
        return tess, "ocr"
    # ikisi de yoksa son çare web OCR (dış servis: yalnız bulut açıkken)
    if not _cloud_ocr_enabled():
        return "", "noise_dropped"
    buf = io.BytesIO()
    pil_img.save(buf, format="PNG")
    web = clean_raw(online_web_ocr(buf.getvalue()))
    if web and not lib.is_ocr_garbage(web):
        return web, "web_ocr"
    return "", "noise_dropped"


# --------------------------------------------------------------------------- PDF
def read_pdf(path: Path, use_ocr: bool, use_vision: bool) -> list[dict]:
    import pymupdf as fitz
    from PIL import Image

    pages = []
    with fitz.open(path) as doc:
        for i, page in enumerate(doc, start=1):
            text = clean_raw(page.get_text("text"))
            method = "metin"
            has_images = bool(page.get_images(full=True))
            garbled = len(text) >= MIN_TEXT_CHARS and (lib.is_ocr_garbage(text) or lib.quality_of(text) < 0.45)
            if (len(text) < MIN_TEXT_CHARS and (has_images or not text)) or garbled:
                pix = page.get_pixmap(dpi=OCR_DPI)
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                ocr_text, m = read_image_text(img, use_ocr, use_vision)
                if len(ocr_text) > len(text):
                    text, method = ocr_text, m
            pages.append({"n": i, "text": text, "method": method})
    return pages


# --------------------------------------------------------------------------- PPTX
def _shape_texts(shape, out: list[str], images: list):
    from pptx.enum.shapes import MSO_SHAPE_TYPE

    if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
        for s in shape.shapes:
            _shape_texts(s, out, images)
        return
    if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
        images.append(shape)
        return
    if getattr(shape, "has_table", False) and shape.has_table:
        for row in shape.table.rows:
            out.append(" | ".join(c.text.strip().replace("\n", " ") for c in row.cells))
        return
    if getattr(shape, "has_text_frame", False) and shape.has_text_frame:
        for para in shape.text_frame.paragraphs:
            line = "".join(r.text for r in para.runs).strip() or para.text.strip()
            if line:
                indent = "  " * (para.level or 0)
                out.append(f"{indent}{line}")


def read_pptx(path: Path, use_ocr: bool, use_vision: bool) -> list[dict]:
    from PIL import Image
    from pptx import Presentation

    prs = Presentation(str(path))
    pages = []
    for i, slide in enumerate(prs.slides, start=1):
        lines: list[str] = []
        pictures: list = []
        for shape in slide.shapes:
            _shape_texts(shape, lines, pictures)
        text = clean_raw("\n".join(lines))
        method = "metin"

        # Slayttaki görsellerin içindeki yazılar (şema, tablo resmi vb.)
        img_texts = []
        if use_ocr or use_vision:
            for pic in pictures:
                try:
                    img = Image.open(io.BytesIO(pic.image.blob)).convert("RGB")
                    if img.width < 200 or img.height < 80:
                        continue
                    t, m = read_image_text(img, use_ocr, use_vision, cloud_needs_text=True)
                    if len(t) >= 15:
                        img_texts.append(t)
                        method = "metin+" + m
                except Exception:
                    continue
        if img_texts:
            text = (text + "\n\n[Görsel içi metin]\n" + "\n---\n".join(img_texts)).strip()

        notes = ""
        if slide.has_notes_slide:
            notes = clean_raw(slide.notes_slide.notes_text_frame.text)
        pages.append({"n": i, "text": text, "method": method, **({"notes": notes} if notes else {})})
    return pages


# --------------------------------------------------------------------------- Docling
_DOCLING_CONVERTER = None


def _docling_converter():
    """Docling dönüştürücüsünü (tablo yapısı + Tesseract[tur] OCR) bir kez oluşturur."""
    global _DOCLING_CONVERTER
    if _DOCLING_CONVERTER is None:
        from docling.datamodel.base_models import InputFormat
        from docling.datamodel.pipeline_options import PdfPipelineOptions, TesseractCliOcrOptions
        from docling.document_converter import DocumentConverter, PdfFormatOption

        opts = PdfPipelineOptions()
        opts.do_ocr = True
        opts.do_table_structure = True
        opts.ocr_options = TesseractCliOcrOptions(lang=["tur", "eng"])
        _DOCLING_CONVERTER = DocumentConverter(
            format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=opts)}
        )
    return _DOCLING_CONVERTER


def read_docling(path: Path) -> list[dict]:
    """Docling ile sayfa/slayt bazlı Markdown (başlık, tablo, liste yapısı korunur)."""
    doc = _docling_converter().convert(str(path)).document
    nums = sorted(doc.pages.keys()) if getattr(doc, "pages", None) else [1]
    pages = []
    for n in nums:
        md = doc.export_to_markdown(page_no=n) if len(nums) > 1 or n != 1 else doc.export_to_markdown()
        pages.append({"n": n, "text": clean_raw(md), "method": "docling"})
    return pages


def ppt_to_pptx(path: Path, tmpdir: Path) -> Path:
    exe = shutil.which("libreoffice") or shutil.which("soffice")
    if not exe:
        raise RuntimeError("Eski .ppt için libreoffice gerekli")
    subprocess.run(
        [exe, "--headless", "--convert-to", "pptx", "--outdir", str(tmpdir), str(path)],
        check=True, capture_output=True, timeout=300,
    )
    return tmpdir / (path.stem + ".pptx")


# --------------------------------------------------------------------------- ana akış
def out_base(src: Path, out_root: Path, rel_root: Path | None) -> Path:
    if rel_root and src.is_relative_to(rel_root):
        rel = src.relative_to(rel_root).parent
    else:
        rel = Path()
    return out_root / rel / src.stem


def process_file(src: Path, out_root: Path = DEFAULT_TEMP1, rel_root: Path | None = DEFAULT_DOWNLOADS,
                 force: bool = False, use_ocr: bool = True, use_vision: bool = False,
                 use_docling: bool = False) -> Path | None:
    src = src.resolve()
    ext = src.suffix.lower()
    if ext not in SUPPORTED:
        return None
    base = out_base(src, out_root, rel_root.resolve() if rel_root else None)
    md_path, json_path = base.with_suffix(".md"), base.with_suffix(".json")
    st_src = src.stat()
    if json_path.exists() and not force:
        # Hızlı yol: boyut + değişiklik zamanı aynıysa özet hesaplanmadan atlanır (yeniden işleme yok)
        try:
            prev = json.loads(json_path.read_text(encoding="utf-8"))
            if prev.get("source_size") == st_src.st_size and prev.get("source_mtime") == int(st_src.st_mtime):
                return json_path
        except Exception:
            pass
    digest = sha256_of(src)
    if json_path.exists() and not force:
        try:
            prev = json.loads(json_path.read_text(encoding="utf-8"))
            if prev.get("source_sha256") == digest:
                # boyut/zaman kaydedilir: sonraki çalıştırmalar özet hesaplamadan atlar
                prev["source_size"], prev["source_mtime"] = st_src.st_size, int(st_src.st_mtime)
                json_path.write_text(json.dumps(prev, ensure_ascii=False, indent=1), encoding="utf-8")
                print(f"= atlandı (değişmemiş): {src.name}")
                return json_path
        except Exception:
            pass

    t0 = time.time()
    print(f"> okunuyor: {src.name}")
    kind = "pdf" if ext == ".pdf" else "pptx"
    pages = None
    with tempfile.TemporaryDirectory() as td:
        work = ppt_to_pptx(src, Path(td)) if ext == ".ppt" else src
        if use_docling:
            try:
                pages = read_docling(work)
                if not any(p["text"] for p in pages):
                    pages = None  # Docling boş döndürdü, klasik okuyucuya düş
            except Exception as e:
                print(f"  [uyarı] Docling başarısız ({e}); klasik okuyucuya geçiliyor", file=sys.stderr)
        if pages is None:
            pages = read_pdf(work, use_ocr, use_vision) if kind == "pdf" else read_pptx(work, use_ocr, use_vision)

    label = "Sayfa" if kind == "pdf" else "Slayt"
    md_parts = [f"# {src.stem}\n", f"> Kaynak: `{src}`  \n> Tür: {kind}, {len(pages)} {label.lower()}\n"]
    for p in pages:
        md_parts.append(f"\n## {label} {p['n']}\n")
        md_parts.append(p["text"] if p["text"] else "_(boş / okunamadı)_")
        if p.get("notes"):
            md_parts.append(f"\n\n**Konuşmacı notu:** {p['notes']}")
        md_parts.append("\n")

    base.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text("\n".join(md_parts), encoding="utf-8")
    empty = sum(1 for p in pages if not p["text"])
    json_path.write_text(
        json.dumps(
            {
                "stage": "temp1",
                "source": str(src),
                "source_sha256": digest,
                "source_size": st_src.st_size,
                "source_mtime": int(st_src.st_mtime),
                "type": kind,
                "page_count": len(pages),
                "empty_pages": empty,
                "ocr_lang": OCR_LANG,
                "reader": "docling" if use_docling and pages and pages[0].get("method") == "docling" else "klasik",
                "extracted_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                "pages": pages,
            },
            ensure_ascii=False,
            indent=1,
        ),
        encoding="utf-8",
    )
    print(f"  ✓ {len(pages)} {label.lower()}, {empty} boş, {time.time() - t0:.1f}s -> {md_path}")
    return json_path


def iter_sources(paths: list[Path]):
    for p in paths:
        if p.is_dir():
            for f in sorted(p.rglob("*")):
                if f.is_file() and f.suffix.lower() in SUPPORTED and not f.name.startswith(("~$", ".")):
                    yield f
        elif p.is_file():
            yield p
        else:
            print(f"  [uyarı] bulunamadı: {p}", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", type=Path, help=f"dosya/klasör (varsayılan: {DEFAULT_DOWNLOADS})")
    ap.add_argument("--out", type=Path, default=DEFAULT_TEMP1, help="çıktı kökü (varsayılan temp1)")
    ap.add_argument("--rel-root", type=Path, default=DEFAULT_DOWNLOADS, help="alt klasör yapısını korumak için kök")
    ap.add_argument("--force", action="store_true", help="değişmemiş dosyaları da yeniden oku")
    ap.add_argument("--no-ocr", action="store_true", help="Tesseract OCR kullanma")
    ap.add_argument("--docling", action="store_true", help="Docling kullan (tablo/başlık yapısını korur; ağır ama daha düzenli)")
    ap.add_argument("--vision", action="store_true", help="bulut görsel okumayı zorla aç (varsayılan zaten açık; kapatmak: MEDS_OCR_CLOUD=0)")
    a = ap.parse_args()

    paths = a.paths or [DEFAULT_DOWNLOADS]
    n = fail = 0
    for f in iter_sources(paths):
        try:
            if process_file(f, a.out, a.rel_root, a.force, not a.no_ocr, a.vision, a.docling):
                n += 1
        except Exception as e:
            fail += 1
            print(f"  ✗ HATA {f.name}: {e}", file=sys.stderr)
    print(f"Bitti: {n} dosya işlendi, {fail} hata.")
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
