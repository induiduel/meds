#!/usr/bin/env python3
"""L0 kroki — ders PDF'inin değişmez, koordinatlı haritası (ICERIK_MOTORU_V3.md §2.1, §2.2, §19).

PDF bir kez okunur; her sayfa için (koordinatlar sayfa oranı 0–1, 4 ondalık):
  kimlik `kN-NN-pNN`, boyut, iz {metin SimHash, gorsel pHash}, metin, satirlar [{bbox, metin, kelime:[ilk, son], zemin?}],
  kelimeler [[x0,y0,x1,y1,"metin",satir]], vurgulu (kalın/renkli ifadeler), resimler [{id -gN, bbox, metinsiz, ocr?}],
  tablolar [{id -tN, bbox, hucreler}], cizgi_sayisi, zemin {L, sinif}, varliklar (tıbbi varlık listesi).
Ders düzeyi: `tekrar_satirlar` (sayfaların ≥%40'ında yinelenen başlık/altbilgi; kapsam ve kanıt hesabında sayılmaz).
OCR yalnız METİNSİZ resim bölgesine (gömülü metni olan sayfa OCR'a girmez; hibrit atlatma §19).
Önceki L0 varsa sayfa izleriyle eşlenir; "aynı" sayfanın pahalı alanları (resim OCR, roi, egri, ok) TAŞINIR, yeniden
hesaplanmaz → `l0/sayfa_eslesme.json` + özet.

Kullanım (meds/.venv-ocr/bin/python):
  l0.py --ders k1-03 [--pdf YOL] [--zorla] [--ocr-yok]      → meds_database_v2/ders_bilgi/k1-03/l0/sayfalar.json
  l0.py --kurul 1                                            → bilgi deposundaki tüm dersler (değişmeyen PDF atlanır)
  l0.py --ders k1-03 --pdf YENI.pdf --cikis DİZİN            → sınama: eski L0'la eşle, başka yere yaz
"""
from __future__ import annotations

import argparse
import re
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np  # noqa: E402

import iz  # noqa: E402
import varlik  # noqa: E402
from ortak import DEPO, dersler, katla, manifest, oku, pdf_bul, sha_dosya, yaz  # noqa: E402

SURUM = 2   # 2: satırlara PDF blok numarası (şema etiketleri blok düzeyinde bağlanır)
TASINAN = ("roi", "egri", "ok")          # sayfa düzeyi pahalı alanlar (R1b betikleri yazar)


def _y(v: float) -> float:
    return round(float(v), 4)


def _kutu(r, w, h) -> list[float]:
    return [_y(r[0] / w), _y(r[1] / h), _y(r[2] / w), _y(r[3] / h)]


def _dogrusal(c: np.ndarray) -> np.ndarray:
    c = c / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def bagil_isiklilik(rgb: np.ndarray) -> float:
    """WCAG bağıl ışıklılık (doğrusallaştırılmış sRGB ortalaması)."""
    if rgb.size == 0:
        return 1.0
    lin = _dogrusal(rgb.reshape(-1, 3).astype("float64"))
    return float((0.2126 * lin[:, 0] + 0.7152 * lin[:, 1] + 0.0722 * lin[:, 2]).mean())


def zemin_sinifi(rgb: np.ndarray) -> dict:
    L = bagil_isiklilik(rgb)
    doy = 0.0
    if rgb.size:
        a = rgb.reshape(-1, 3).astype("float64")
        doy = float(((a.max(1) - a.min(1)) / np.maximum(a.max(1), 1)).mean())
    return {"L": round(L, 3), "sinif": "koyu" if L < 0.18 else ("renkli" if doy > 0.35 else "acik")}


def _render(sayfa, genislik: int = 600) -> np.ndarray:
    import pymupdf
    olcek = genislik / max(sayfa.rect.width, 1)
    pm = sayfa.get_pixmap(matrix=pymupdf.Matrix(olcek, olcek), colorspace=pymupdf.csRGB, alpha=False)
    return np.frombuffer(pm.samples, dtype=np.uint8).reshape(pm.height, pm.width, 3)


def _ocr(sayfa, bbox_pdf) -> str:
    import pymupdf
    import pytesseract
    from PIL import Image
    pm = sayfa.get_pixmap(matrix=pymupdf.Matrix(2.5, 2.5), clip=pymupdf.Rect(*bbox_pdf), alpha=False)
    img = Image.frombytes("RGB", (pm.width, pm.height), pm.samples)
    try:
        d = pytesseract.image_to_data(img, lang="tur+eng", config="--psm 11", output_type=pytesseract.Output.DICT)
    except Exception:  # noqa: BLE001
        return ""
    sozler = [t for t, c in zip(d["text"], d["conf"]) if t.strip() and float(c) >= 60 and len(t.strip()) >= 2]
    metin = " ".join(sozler)
    return metin if ocr_anlamli(metin) else ""


def metin_izi(sayfa, sozler=None) -> str | None:
    """Sayfa metin izi her yerde AYNI girdiden: PyMuPDF sözcükleri okuma sırasıyla (sort=True)."""
    sozler = sozler if sozler is not None else sayfa.get_text("words", sort=True)
    return iz.simhash(" ".join(w[4] for w in sozler))


def gercek_tablo(hucre: list[list[str]]) -> bool:
    """Ders işçisiyle aynı ölçüt (cikar.py): ≥2 satırda 2+ dolu hücre, ≥30 karakter, boş hücre ≤ %50; ek olarak
    tek hücrede ≤30 sözcük (şekil altı yazısı / serbest metin bloğu tablo sayılmaz)."""
    dolu = [r for r in hucre if sum(1 for h in r if len(h) >= 2) >= 2]
    tum = [h for r in hucre for h in r]
    bos = sum(1 for h in tum if not h) / max(1, len(tum))
    return (len(dolu) >= 2 and sum(len(h) for r in dolu for h in r) >= 30 and bos <= 0.5
            and max((len(h.split()) for h in tum), default=0) <= 30)


def ocr_anlamli(metin: str) -> bool:
    """Fotoğraf/histoloji OCR'ı harf yığını üretir: ≥3 sözcük ve sözcüklerin ≥%70'i harf, ≥3 harf, ünlülü olmalı."""
    t = metin.split()
    iyi = [w for w in t if len(w) >= 3 and w.strip(".,:;()").isalpha() and re.search(r"[aeıioöuüAEIİOÖUÜ]", w)]
    return len(iyi) >= 3 and len(iyi) / max(len(t), 1) >= 0.7


def sayfa_cikar(sayfa, no: int, ders_id: str, ocr: bool) -> dict:
    W, H = sayfa.rect.width, sayfa.rect.height
    sozler = sayfa.get_text("words", sort=True)
    satir_anahtar: dict[tuple, int] = {}
    satirlar, kelimeler = [], []
    for x0, y0, x1, y1, t, b, l, _ in sozler:
        k = (b, l)
        if k not in satir_anahtar:
            satir_anahtar[k] = len(satirlar)
            satirlar.append({"bbox": [x0, y0, x1, y1], "sozler": [], "blok": b})
        s = satirlar[satir_anahtar[k]]
        s["bbox"] = [min(s["bbox"][0], x0), min(s["bbox"][1], y0), max(s["bbox"][2], x1), max(s["bbox"][3], y1)]
        s["sozler"].append(len(kelimeler))
        kelimeler.append([*_kutu((x0, y0, x1, y1), W, H), t, satir_anahtar[k]])
    gor = _render(sayfa)
    gh, gw = gor.shape[:2]
    sayfa_zemin = zemin_sinifi(gor)
    satir_cikti = []
    for s in satirlar:
        bx = _kutu(s["bbox"], W, H)
        x0, y0 = max(int((bx[0] - 0.01) * gw), 0), max(int((bx[1] - 0.01) * gh), 0)
        x1, y1 = min(int((bx[2] + 0.01) * gw) + 1, gw), min(int((bx[3] + 0.01) * gh) + 1, gh)
        z = zemin_sinifi(gor[y0:y1, x0:x1])
        kayit = {"bbox": bx, "metin": " ".join(kelimeler[i][4] for i in s["sozler"]),
                 "kelime": [s["sozler"][0], s["sozler"][-1]], "blok": s["blok"]}
        if z["sinif"] != sayfa_zemin["sinif"]:
            kayit["zemin"] = z["sinif"]
        satir_cikti.append(kayit)
    # hocanın vurgusu: kalın ya da siyah olmayan renkli ifadeler
    vurgulu = []
    for blok in sayfa.get_text("dict").get("blocks", []):
        for ln in blok.get("lines", []):
            for sp in ln.get("spans", []):
                t = sp.get("text", "").strip()
                if len(t) < 3:
                    continue
                renk = sp.get("color", 0)
                r, g, b = (renk >> 16) & 255, (renk >> 8) & 255, renk & 255
                renkli = max(r, g, b) - min(r, g, b) > 60 and max(r, g, b) > 90
                if (sp.get("flags", 0) & 16) or renkli:
                    vurgulu.append({"metin": t, "bbox": _kutu(sp["bbox"], W, H),
                                    "tur": "renkli" if renkli else "kalin"})
    resimler = []
    for bilgi in sayfa.get_image_info():
        bb = bilgi.get("bbox")
        if not bb:
            continue
        alan = (bb[2] - bb[0]) * (bb[3] - bb[1]) / max(W * H, 1)
        if alan < 0.01 or alan > 0.92:
            continue                                  # süs ya da tüm sayfa zemini
        kutu = _kutu(bb, W, H)
        icinde = sum(1 for k in kelimeler if k[0] >= kutu[0] - 0.005 and k[2] <= kutu[2] + 0.005
                     and k[1] >= kutu[1] - 0.005 and k[3] <= kutu[3] + 0.005)
        r = {"id": f"{ders_id}-p{no:02d}-g{len(resimler) + 1}", "bbox": kutu, "alan": round(alan, 3),
             "metinsiz": icinde < 3}
        if ocr and r["metinsiz"] and alan >= 0.04:
            r["ocr"] = _ocr(sayfa, bb)
        resimler.append(r)
    tablolar = []
    try:
        for ti, tb in enumerate(sayfa.find_tables().tables, 1):
            hucre = [[(x or "").strip() for x in satir] for satir in tb.extract()]
            if gercek_tablo(hucre):
                tablolar.append({"id": f"{ders_id}-p{no:02d}-t{ti}", "bbox": _kutu(tb.bbox, W, H), "hucreler": hucre})
    except Exception:  # noqa: BLE001
        pass
    metin = " ".join(s["metin"] for s in satir_cikti)
    ocr_metin = " ".join(r.get("ocr", "") for r in resimler)
    return {
        "kimlik": f"{ders_id}-p{no:02d}", "sayfa": no, "boyut": [round(W, 1), round(H, 1)],
        "iz": {"metin": metin_izi(sayfa, sozler), "gorsel": iz.phash(iz.sayfa_gri32(sayfa))},
        "metin": metin, "satirlar": satir_cikti, "kelimeler": kelimeler, "vurgulu": vurgulu,
        "resimler": resimler, "tablolar": tablolar, "cizgi_sayisi": len(sayfa.get_drawings()),
        "zemin": sayfa_zemin, "varliklar": sorted(varlik.cikar(metin + " " + ocr_metin)),
    }


def tekrar_satirlari(sayfalar: list[dict]) -> list[str]:
    say = Counter()
    for s in sayfalar:
        gorulen = set()
        for st in s["satirlar"]:
            y = st["bbox"][1]
            t = katla(st["metin"]).strip()
            if len(t) >= 3 and (y < 0.14 or y > 0.86) and t not in gorulen:
                gorulen.add(t)
                say[t] += 1
    n = max(len(sayfalar), 1)
    return sorted(t for t, k in say.items() if k >= max(3, 0.4 * n))


def uret(ders_id: str, pdf: Path | None = None, cikis: Path | None = None, zorla: bool = False, ocr: bool = True,
         log=print) -> dict:
    import pymupdf
    pdf = Path(pdf) if pdf else pdf_bul(ders_id)
    hedef = Path(cikis) if cikis else DEPO / ders_id / "l0"
    eski = oku(DEPO / ders_id / "l0" / "sayfalar.json")
    psha = sha_dosya(pdf)
    if eski and eski.get("pdf_sha") == psha and eski.get("surum") == SURUM and not zorla and cikis is None:
        log(f"{ders_id}: L0 güncel (PDF değişmedi) — atlandı")
        return eski
    t0 = time.time()
    belge = pymupdf.open(str(pdf))
    # önce yalnız izler (ucuz): eski L0 ile eşle, aynı sayfaların pahalı işini taşı
    yeni_iz = []
    for i, sayfa in enumerate(belge, 1):
        sw = sayfa.get_text("words", sort=True)
        yeni_iz.append({"sayfa": i, "iz": {"metin": metin_izi(sayfa, sw), "gorsel": iz.phash(iz.sayfa_gri32(sayfa))},
                        "kume": iz.kume(w[4] for w in sw)})
    eski_iz = [{"sayfa": s["sayfa"], "iz": s["iz"], "kume": iz.kume(k[4] for k in s["kelimeler"])}
               for s in (eski or {}).get("sayfalar", [])]
    eslesme = iz.eslestir(eski_iz, yeni_iz) if eski else {}
    eski_sayfa = {s["sayfa"]: s for s in (eski or {}).get("sayfalar", [])}
    sayfalar, ocr_yapilan, tasinan = [], 0, 0
    for i, sayfa in enumerate(belge, 1):
        e = eslesme.get(i)
        es = eski_sayfa.get(e["eski"]) if e and e["tur"] == "ayni" else None
        s = sayfa_cikar(sayfa, i, ders_id, ocr=ocr and es is None)
        if es:
            # aynı sayfa: resim OCR'ı ve sayfa düzeyi pahalı alanlar taşınır (kimlik yeni numarayla)
            eski_ocr = [r.get("ocr") for r in es.get("resimler", [])]
            for r, o in zip(s["resimler"], eski_ocr):
                if o is not None:
                    r["ocr"] = o
            for alan in TASINAN:
                if alan in es:
                    s[alan] = es[alan]
            s["tasindi"] = es["kimlik"]
            tasinan += 1
        else:
            ocr_yapilan += sum(1 for r in s["resimler"] if "ocr" in r)
        sayfalar.append(s)
    tekrar = tekrar_satirlari(sayfalar)
    m = manifest(ders_id)
    l0 = {"surum": SURUM, "ders_id": ders_id, "kurul": m.get("kurul"), "pdf": pdf.name, "pdf_sha": psha,
          "sayfa_sayisi": len(sayfalar), "olusturuldu": time.strftime("%Y-%m-%dT%H:%M:%S"),
          "tekrar_satirlar": tekrar, "sayfalar": sayfalar}
    yaz(hedef / "sayfalar.json", l0)
    if eski:
        ozet = Counter(v["tur"] for v in eslesme.values())
        yaz(hedef / "sayfa_eslesme.json", {"onceki_pdf_sha": eski.get("pdf_sha"), "yeni_pdf_sha": psha,
                                           "ozet": dict(ozet), "esleme": {str(k): v for k, v in eslesme.items()},
                                           "takma_ad": {eski_sayfa[v["eski"]]["kimlik"]: f"{ders_id}-p{k:02d}"
                                                        for k, v in eslesme.items() if v["eski"] and v["eski"] != k}}, 1)
    log(f"{ders_id}: {len(sayfalar)} sayfa, {tasinan} taşındı, {ocr_yapilan} resim OCR, "
        f"{sum(len(s['resimler']) for s in sayfalar)} resim, {sum(len(s['tablolar']) for s in sayfalar)} tablo, "
        f"{len(tekrar)} tekrar satırı, {time.time() - t0:.1f} sn")
    return l0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ders")
    ap.add_argument("--kurul", type=int)
    ap.add_argument("--pdf")
    ap.add_argument("--cikis")
    ap.add_argument("--zorla", action="store_true")
    ap.add_argument("--ocr-yok", action="store_true")
    a = ap.parse_args()
    liste = [a.ders] if a.ders else dersler(a.kurul)
    if not liste:
        ap.error("--ders ya da --kurul")
    hata = 0
    for d in liste:
        try:
            uret(d, a.pdf, a.cikis, a.zorla, not a.ocr_yok)
        except SystemExit as e:
            print(f"{d}: {e}")
            hata += 1
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main())
