"""Onay kapısı ekleri → ders işçisi bağlamı (2026-10-24).

Yönetici onay ekranından öğrenci notu ve/veya ders ses kaydı yükleyip "Notlarla başlat" derse (api.py `_onay`, mod "ekli"),
iş kaydında `ekler = {not: [{ad, yol, boyut}], ses: [...]}` bulunur. Bu modül taslak klasörüne yazar:
  ogrenci_notu.md   — not dosyalarının metni (PDF: PyMuPDF, görüntü sayfa → Tesseract; görsel: Tesseract; txt/md: aynen;
                      docx: python-docx varsa)
  ders_kaydi.md     — ses kaydının dökümü (faster-whisper, CPU int8; GPU yasak — AGENTS.md madde 10)
  ekler.json        — ne hazırlandı, ne hazırlanamadı (uyarılar rapora/bağlama geçer)
Notlar içerik KAYNAĞI değildir (kaynak yine kaynak.md): hoca vurgusunun ve "Burası önemli" cümlesinin dayanağıdır (H22).
"""
from __future__ import annotations

import os
import shutil
import subprocess
import time
from pathlib import Path

from ayarlar import log, yaz

WHISPER_MODEL = os.environ.get("MEDS_ISCI_WHISPER_MODEL", "small")


def _ocr(goruntu: Path) -> str:
    tess = shutil.which("tesseract")
    if not tess:
        return ""
    r = subprocess.run([tess, str(goruntu), "-", "-l", "tur+eng"], capture_output=True, text=True, timeout=300)
    return r.stdout.strip()


def not_metni(f: Path) -> tuple[str, str]:
    """→ (metin, uyarı)."""
    uz = f.suffix.lower()
    if uz in (".txt", ".md"):
        return f.read_text(encoding="utf-8", errors="replace"), ""
    if uz == ".pdf":
        import pymupdf
        out, ocr = [], 0
        with pymupdf.open(f) as doc:
            for i, s in enumerate(doc, 1):
                t = s.get_text().strip()
                if len(t) < 40:                     # el yazısı / taranmış not sayfası → OCR
                    p = f.with_name(f".{f.stem}_s{i}.png")
                    s.get_pixmap(dpi=200).save(p)
                    t = _ocr(p); p.unlink(missing_ok=True); ocr += 1
                out.append(f"=== NOT SAYFASI {i} ===\n{t}")
        return "\n\n".join(out), (f"{ocr} sayfa OCR ile okundu (el yazısında hata olabilir)" if ocr else "")
    if uz in (".png", ".jpg", ".jpeg", ".webp", ".heic"):
        t = _ocr(f)
        return t, "" if t else "görselden metin çıkmadı (tesseract yok ya da okunaksız)"
    if uz in (".docx", ".doc"):
        try:
            import docx  # python-docx
            return "\n".join(p.text for p in docx.Document(str(f)).paragraphs), ""
        except Exception as e:  # noqa: BLE001
            return "", f"Word dosyası okunamadı ({e.__class__.__name__}); PDF olarak yükleyin"
    return "", f"desteklenmeyen not türü: {uz}"


def ses_dokumu(f: Path) -> tuple[str, str]:
    """faster-whisper (CPU, int8). Yoksa ("", uyarı): iş durmaz, döküm bekliyor olarak raporlanır."""
    try:
        os.environ["CUDA_VISIBLE_DEVICES"] = ""
        from faster_whisper import WhisperModel
    except Exception:  # noqa: BLE001
        return "", "ses dökümü yapılamadı: işçide faster-whisper yok (Dockerfile.isci yeniden kurulmalı)"
    t0 = time.time()
    m = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8", cpu_threads=max(1, (os.cpu_count() or 2) - 1))
    parcalar, bilgi = m.transcribe(str(f), language="tr", vad_filter=True, beam_size=1)
    satirlar = []
    for p in parcalar:
        dk, sn = divmod(int(p.start), 60)
        satirlar.append(f"[{dk:02d}:{sn:02d}] {p.text.strip()}")
    log(f"ses dökümü: {f.name} · {round(bilgi.duration / 60, 1)} dk ses · {round((time.time() - t0) / 60, 1)} dk sürdü")
    return "\n".join(satirlar), ""


def hazirla(j: dict, d: Path) -> dict:
    """İşin eklerini taslak klasörüne metin olarak yazar; bir kez (ekler.json varsa yeniden yapılmaz)."""
    if (d / "ekler.json").exists():
        from ayarlar import oku
        return oku(d / "ekler.json", {})
    ek = j.get("ekler") or {}
    if not (ek.get("not") or ek.get("ses")):
        return {}
    sonuc = {"not": [], "ses": [], "uyarilar": []}
    notlar = []
    for x in ek.get("not") or []:
        f = Path(x["yol"])
        if not f.is_file():
            sonuc["uyarilar"].append(f"not dosyası bulunamadı: {x['ad']}"); continue
        try:
            t, u = not_metni(f)
        except Exception as e:  # noqa: BLE001  (okuyucu eksik/bozuk dosya: iş durmaz, uyarı rapora)
            t, u = "", f"okunamadı ({e.__class__.__name__}: {str(e)[:80]})"
        if u:
            sonuc["uyarilar"].append(f"{x['ad']}: {u}")
        if t.strip():
            notlar.append(f"## {x['ad']}\n\n{t.strip()}")
            sonuc["not"].append({"ad": x["ad"], "karakter": len(t)})
    if notlar:
        (d / "ogrenci_notu.md").write_text("# Öğrenci notu (yöneticinin yüklediği)\n\n" + "\n\n".join(notlar) + "\n",
                                          encoding="utf-8")
    dokum = []
    for x in ek.get("ses") or []:
        f = Path(x["yol"])
        if not f.is_file():
            sonuc["uyarilar"].append(f"ses dosyası bulunamadı: {x['ad']}"); continue
        try:
            t, u = ses_dokumu(f)
        except Exception as e:  # noqa: BLE001
            t, u = "", f"ses dökümü yapılamadı ({e.__class__.__name__}: {str(e)[:80]})"
        if u:
            sonuc["uyarilar"].append(f"{x['ad']}: {u}")
        if t.strip():
            dokum.append(f"## {x['ad']}\n\n{t}")
            sonuc["ses"].append({"ad": x["ad"], "karakter": len(t)})
    if dokum:
        (d / "ders_kaydi.md").write_text("# Ders ses kaydı dökümü (otomatik, hatalı kelime olabilir)\n\n" + "\n\n".join(dokum)
                                         + "\n", encoding="utf-8")
    yaz(d / "ekler.json", sonuc)
    return sonuc


def istem_eki(d: Path) -> str:
    """Yazar istemine eklenecek açıklama (dosyalar varsa)."""
    var = [a for a in ("ogrenci_notu.md", "ders_kaydi.md") if (d / a).exists()]
    if not var:
        return ""
    return (f" Çalışma dizininde yöneticinin yüklediği {' ve '.join(var)} var: bunlar İÇERİK KAYNAĞI DEĞİLDİR (kaynak yine "
            "kaynak.md); hocanın derste vurguladığı noktaların ve sesli metindeki 'Burası önemli' cümlesinin dayanağıdır. "
            "Notta ya da kayıtta vurgulanan ve kaynak.md'de bulunan bilgileri önem/vurgu olarak işaretle; kaynak.md'de olmayan "
            "bilgiyi ekleme, rapor.md'de 'notta var, slaytta yok' diye listele.")
