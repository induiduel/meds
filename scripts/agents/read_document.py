#!/usr/bin/env python3
"""
PDF / PPTX okuma ajanı (downloads -> temp1).

PROJE_TANITIMI.md'deki 1. aşama: ham kaynaktan ilk veriyi çıkarır. Tamamen yerel çalışır
(PyMuPDF, python-pptx, Tesseract[tur]; isteğe bağlı Ollama görsel model) ve token harcamaz.

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

PROJECT_ROOT = Path(__file__).resolve().parents[3]  # .../MedSoru Project
DEFAULT_DOWNLOADS = Path(os.environ.get("MEDS_DOWNLOADS_DIR") or PROJECT_ROOT / "meds_downloads")
DEFAULT_TEMP1 = Path(os.environ.get("MEDS_TEMP_DIR") or PROJECT_ROOT / "meds_temp") / "temp1"
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
VISION_MODEL = os.environ.get("MEDS_VISION_MODEL", "qwen3-vl:8b")
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


def slice_image_quadrants(pil_img) -> list:
    """
    2. Görüntü Dilimleme (Image Tiling / Slicing):
    Büyük ve çok yazılı slaytları 2x2 4 kadrana bölerek Qwen-VL downsampling kaybını engeller.
    """
    w, h = pil_img.size
    if w < 1000 or h < 800:
        return [pil_img]
    mid_x, mid_y = w // 2, h // 2
    quadrants = [
        pil_img.crop((0, 0, mid_x, mid_y)),          # Sol üst
        pil_img.crop((mid_x, 0, w, mid_y)),          # Sağ üst
        pil_img.crop((0, mid_y, mid_x, h)),          # Sol alt
        pil_img.crop((mid_x, mid_y, w, h)),          # Sağ alt
    ]
    return quadrants


def ocr_image(img) -> str:
    """
    4. Hibrit OCR Mimarisi:
    Önce EasyOCR (varsa) veya Tesseract çalıştırılır.
    """
    # EasyOCR kontrolü
    try:
        import easyocr
        reader = easyocr.Reader(['tr', 'en'], gpu=True)
        results = reader.readtext(np.array(img), detail=0)
        easy_text = " ".join(results).strip()
        if easy_text and not lib.is_ocr_garbage(easy_text):
            return easy_text
    except Exception:
        pass

    # Tesseract OCR
    import pytesseract
    try:
        return pytesseract.image_to_string(img, lang=OCR_LANG, config="--oem 1 --psm 6")
    except Exception:
        return ""


def vision_ocr_single(png_bytes: bytes) -> str:
    """Tekil parça için Qwen3-VL ile katı promptlu OCR."""
    import requests

    # 3. VLM İçin Katı OCR Promptu (Strict Prompting)
    prompt = (
        "Sen yüksek hassasiyetli bir tıbbi OCR motorusun. "
        "Sana verilen görseldeki metni BİREBİR çıkaracaksın. Hiçbir yorum ekleme, özetleme yapma ve metni değiştirme. "
        "Türkçe karakterleri (ç ğ ı İ ö ş ü) ve tıbbi Latince terimleri koru. "
        "Eğer tıbbi bir tablo varsa bunu Markdown tablosu formatında ver. "
        "Eğer görselde okunmayan bir yer varsa oraya [OKUNAMIYOR] yaz. "
        "Okunabilir hiçbir metin yoksa sadece BOŞ yaz."
    )
    r = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": VISION_MODEL,
            "stream": False,
            "think": False,
            "messages": [{"role": "user", "content": prompt, "images": [base64.b64encode(png_bytes).decode()]}],
            "options": {"temperature": 0},
        },
        timeout=600,
    )
    r.raise_for_status()
    out = r.json()["message"]["content"].strip()
    if out.upper() in {"BOŞ", "BOS", "BOŞTUR", "YOK"}:
        return ""
    return out


def vision_ocr(png_bytes: bytes, pil_img=None) -> str:
    """Yerel Ollama görsel modeliyle (qwen3-vl:8b) sayfayı dilimleyerek (slicing) okur."""
    if pil_img is None:
        from PIL import Image
        pil_img = Image.open(io.BytesIO(png_bytes))

    # Geniş/yoğun görsellerde dilimleme (slicing) uygula
    w, h = pil_img.size
    if w >= 1200 and h >= 900:
        quads = slice_image_quadrants(pil_img)
        texts = []
        for q in quads:
            buf = io.BytesIO()
            q.save(buf, format="PNG")
            t = vision_ocr_single(buf.getvalue())
            if t:
                texts.append(t)
        if texts:
            return "\n\n".join(texts)

    return vision_ocr_single(png_bytes)


def online_web_ocr(png_bytes: bytes) -> str:
    """Yerel OCR yetersiz kaldığında ücretsiz internet tabanlı OCR motorundan destek alır."""
    import requests
    try:
        r = requests.post(
            "https://api.ocr.space/parse/image",
            files={"file": ("image.png", png_bytes, "image/png")},
            data={"apikey": "helloworld", "language": "tur", "OCREngine": "2"},
            timeout=20,
        )
        if r.status_code == 200:
            res = r.json()
            lines = []
            for item in res.get("ParsedResults", []):
                t = item.get("ParsedText", "").strip()
                if t:
                    lines.append(t)
            return "\n".join(lines).strip()
    except Exception as e:
        print(f"  [uyarı] Web OCR fallback hatası: {e}", file=sys.stderr)
    return ""


def consolidate_ocr_texts(tess_text: str, vision_text: str, web_text: str = "") -> str:
    """Birden fazla OCR motorunun çıktısını ultra hızlı hafif modelle (qwen3:1.7b) tek ve doğru metne birleştirir."""
    sources = []
    if tess_text:
        sources.append(f"--- Tesseract OCR Çıktısı ---\n{tess_text}")
    if vision_text:
        sources.append(f"--- Vision Model Çıktısı ---\n{vision_text}")
    if web_text:
        sources.append(f"--- Web OCR Çıktısı ---\n{web_text}")

    if not sources:
        return ""
    if len(sources) == 1:
        # Tek bir kaynak varsa ve çöp değilse doğrudan döndür
        raw = tess_text or vision_text or web_text
        return raw if not lib.is_ocr_garbage(raw) else ""

    prompt = (
        "Aşağıda aynı tıp slaytına/sayfasına ait farklı OCR motorlarının okuduğu metinler verilmiştir.\n"
        "GÖREV: Bu çıktılardaki yazım/karakter hatalarını tıp terminolojisine ve Türkçe imlaya göre düzelterek "
        "tek bir temiz ve eksiksiz metin oluştur. Eğer içerik sadece anlamsız çizgi/şekil çöpü ise hiçbir şey yazma.\n"
        "Yalnızca nihai metni yaz, açıklama yapma.\n\n" + "\n\n".join(sources)
    )
    try:
        merged = lib.chat(lib.MODEL_FAST, prompt, system="Sen uzman bir tıp metni editörüsün.", num_predict=1500)
        if merged and not lib.is_ocr_garbage(merged):
            return clean_raw(merged)
    except Exception as e:
        print(f"  [uyarı] Hafif model OCR birleştirme hatası: {e}", file=sys.stderr)

    # Birleştirme başarısız olursa en kaliteli olanı seç
    candidates = [t for t in [vision_text, tess_text, web_text] if t and not lib.is_ocr_garbage(t)]
    return clean_raw(max(candidates, key=lib.quality_of)) if candidates else ""


def read_image_text(pil_img, use_ocr: bool, use_vision: bool) -> tuple[str, str]:
    """Multi-Engine OCR: Tesseract + Vision Model + Hızlı Konsolidasyon + Web OCR Fallback."""
    if not use_ocr and not use_vision:
        return "", "yok"

    tess_text = ""
    vision_text = ""
    web_text = ""
    method = "ocr"

    # 1. Görüntü Ön İşleme (Upscaling + Kontrast)
    proc_img = preprocess_image_for_ocr(pil_img)

    # 1. Motor: Tesseract / EasyOCR
    if use_ocr:
        raw_tess = clean_raw(ocr_image(proc_img))
        if not lib.is_ocr_garbage(raw_tess):
            tess_text = raw_tess

    buf = None
    # 2. Motor: Yerel Görsel Yapay Zeka (Qwen3-VL ile Dilimleme/Slicing)
    # Tesseract yetersiz kaldıysa, kısa ise veya şüpheliyse devreye girer
    if use_vision:
        buf = io.BytesIO()
        proc_img.save(buf, format="PNG")
        png_bytes = buf.getvalue()
        try:
            raw_vis = clean_raw(vision_ocr(png_bytes, pil_img=proc_img))
            if not lib.is_ocr_garbage(raw_vis):
                vision_text = raw_vis
                method = "vision"
        except Exception as e:
            print(f"  [uyarı] görsel model başarısız: {e}", file=sys.stderr)

    # 3. Konsolidasyon & Hızlı Model Düzeltmesi (qwen3:1.7b)
    final_text = consolidate_ocr_texts(tess_text, vision_text)

    # 4. Kalite Yetersizse İnternet Tabanlı Ücretsiz Web OCR Fallback
    if len(final_text) < MIN_TEXT_CHARS or lib.quality_of(final_text) < 0.60:
        if buf is None:
            buf = io.BytesIO()
            pil_img.save(buf, format="PNG")
        web_text = online_web_ocr(buf.getvalue())
        if web_text and not lib.is_ocr_garbage(web_text):
            # Web OCR çıktısı ile tekrar konsolide et
            re_merged = consolidate_ocr_texts(tess_text, vision_text, web_text)
            if re_merged and lib.quality_of(re_merged) > lib.quality_of(final_text):
                final_text = re_merged
                method = "multi_ocr+web"

    # Son çöp kontrolü: Anlamsız karakter/çizim çorbasıysa boşalt
    if lib.is_ocr_garbage(final_text):
        return "", "noise_dropped"

    return final_text, method


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
            if len(text) < MIN_TEXT_CHARS and (has_images or not text):
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
                    t, m = read_image_text(img, use_ocr, use_vision)
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
    digest = sha256_of(src)
    if json_path.exists() and not force:
        try:
            if json.loads(json_path.read_text(encoding="utf-8")).get("source_sha256") == digest:
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


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", type=Path, help=f"dosya/klasör (varsayılan: {DEFAULT_DOWNLOADS})")
    ap.add_argument("--out", type=Path, default=DEFAULT_TEMP1, help="çıktı kökü (varsayılan temp1)")
    ap.add_argument("--rel-root", type=Path, default=DEFAULT_DOWNLOADS, help="alt klasör yapısını korumak için kök")
    ap.add_argument("--force", action="store_true", help="değişmemiş dosyaları da yeniden oku")
    ap.add_argument("--no-ocr", action="store_true", help="Tesseract OCR kullanma")
    ap.add_argument("--docling", action="store_true", help="Docling kullan (tablo/başlık yapısını korur; ağır ama daha düzenli)")
    ap.add_argument("--vision", action="store_true", help="OCR yetersizse Ollama görsel modeli kullan")
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
