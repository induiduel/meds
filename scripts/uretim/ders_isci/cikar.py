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
                    # gerçek tablo: en az 2 satırda 2+ dolu hücre ve anlamlı metin (görsel yerleşimi tablo sanılmasın)
                    dolu = [r for r in satir if sum(1 for h in r if len(h) >= 2) >= 2]
                    hucre = [h for r in satir for h in r]
                    bos = sum(1 for h in hucre if not h) / max(1, len(hucre))
                    if len(dolu) >= 2 and sum(len(h) for r in dolu for h in r) >= 30 and bos <= 0.5:
                        tablolar.append(satir)
            except Exception:  # noqa: BLE001
                pass
            vurgulu = hoca_vurgusu(sayfa)
            goruntu = None
            if oran >= gorsel_esik or cizim >= 25:
                goruntu = f"sayfa_goruntu/{i}.png"
                sayfa.get_pixmap(dpi=dpi).save(hedef / goruntu)
            out.append({"sayfa": i, "tablolar": tablolar, "gorsel_orani": oran, "cizim": cizim, "goruntu": goruntu,
                        "vurgulu": vurgulu})
    import json
    (hedef / "sayfalar.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    return {"tablo_sayfa": sum(1 for x in out if x["tablolar"]), "tablo": sum(len(x["tablolar"]) for x in out),
            "goruntu_sayfa": sum(1 for x in out if x["goruntu"]), "vurgulu_ifade": sum(len(x["vurgulu"]) for x in out)}


def hoca_vurgusu(sayfa) -> list[dict]:
    """Hocanın slaytta öne çıkardığı ifadeler: renkli yazı (siyah/gri/beyaz dışı) ve kalın yazı; büyük punto satırlar
    `baslik`. Sarı vurgulayıcı kutuları kullanılmaz: slayt PDF'lerinde üst üste binen gizli metin katmanları kutu içi
    okumayı bozuyor (2026-10-20 sınandı). Döner: [{"metin", "tur": "renk"|"kalin"|"baslik"}] (tekrarsız, ≤40)."""
    def renkli(c: int) -> bool:
        r, g, b = (c >> 16) & 255, (c >> 8) & 255, c & 255
        return max(r, g, b) - min(r, g, b) > 60  # gri tonlar (siyah, beyaz dahil) değil
    gor, out = set(), []
    boyut = [sp["size"] for bl in sayfa.get_text("dict")["blocks"] for ln in bl.get("lines", []) for sp in ln["spans"]
             if sp["text"].strip()]
    govde = sorted(boyut)[len(boyut) // 2] if boyut else 0
    for bl in sayfa.get_text("dict")["blocks"]:
        for ln in bl.get("lines", []):
            for sp in ln["spans"]:
                t = " ".join(sp["text"].split())
                if len(t) < 3 or t.casefold() in gor:
                    continue
                import pymupdf as fitz
                tur = ("baslik" if govde and sp["size"] >= govde * 1.35 else
                       "renk" if renkli(sp["color"]) else "kalin" if sp["flags"] & 16 else None)
                if tur:
                    gor.add(t.casefold()); out.append({"metin": t, "tur": tur})
    return out[:40]


if __name__ == "__main__":
    import sys

    m, bilgi = pdf_metni(Path(sys.argv[1]))
    print(bilgi)
    print(m[:1500])
