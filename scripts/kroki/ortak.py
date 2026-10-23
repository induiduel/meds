"""Kroki (L0/L1) betiklerinin ortak yardımcıları — ICERIK_MOTORU_V3.md §2, §12, §15, §16.

Çalışma ortamı: `meds/.venv-ocr/bin/python` (PyMuPDF, OpenCV, SciPy, NumPy). Yerel GPU yok (`CUDA_VISIBLE_DEVICES=""`).
Ders bilgi deposu: `meds_database_v2/ders_bilgi/<ders>/` (manifest.json) — L0 `l0/`, L1 `l1/` alt klasörleri.
Vektörler: bge-m3 CPU servisi (:8094, `MEDS_EMBED_BGE_URL`); metin karmasıyla önbellek (aynı metin bir kez vektörlenir).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import urllib.request
from pathlib import Path

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")

KOK = Path(__file__).resolve().parents[2]                   # meds/
UST = KOK.parent
DB2 = Path(os.environ.get("MEDS_DB2_DIR") or UST / "meds_database_v2")
TEMP = Path(os.environ.get("MEDS_TEMP_DIR") or UST / "meds_temp")
INDIR = Path(os.environ.get("MEDS_DOWNLOADS_DIR") or UST / "meds_downloads")
DEPO = DB2 / "ders_bilgi"
EMBED_URL = os.environ.get("MEDS_EMBED_BGE_URL", "http://127.0.0.1:8094/embed")
VEKTOR_ONBELLEK = TEMP / "kroki" / "vektor_onbellek"


def oku(p, varsayilan=None):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return varsayilan


def yaz(p, veri, girinti: int | None = None):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    g = p.with_suffix(p.suffix + ".tmp")
    g.write_text(json.dumps(veri, ensure_ascii=False, indent=girinti, separators=None if girinti else (",", ":")) + "\n",
                 encoding="utf-8")
    g.replace(p)


def sha_dosya(p, n: int = 16) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for parca in iter(lambda: f.read(1 << 20), b""):
            h.update(parca)
    return h.hexdigest()[:n]


def sha(s: str, n: int = 16) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:n]


# ── Türkçe metin ──────────────────────────────────────────────────────────────────────────────────────────────────
_KATLA = str.maketrans("çğıöşüâîûÇĞİÖŞÜÂÎÛ", "cgiosuaiucgiosuaiu")
BAGLAC = set("ve ile veya ya da de da ki bu şu o bir için gibi olan olarak daha en çok az ise hem ne mi mı mu mü "
             "aşağıdaki aşağıdakilerden hangisi hangisidir değildir yalnız".split())


def katla(s: str) -> str:
    return (s or "").replace("İ", "i").replace("I", "ı").lower().translate(_KATLA)


def sozcukler(s: str) -> list[str]:
    return re.findall(r"[0-9a-zçğıöşüâîû]+", (s or "").replace("İ", "i").replace("I", "ı").lower())


def kokler(s: str, en_az: int = 3) -> set[str]:
    """5 harf kök kümesi (katlanmış; bağlaç ve tek başına sayı dışı)."""
    return {katla(w)[:5] for w in sozcukler(s) if len(w) >= en_az and not w.isdigit() and w not in BAGLAC}


def sayilar(s: str) -> set[str]:
    return {x.replace(",", ".") for x in re.findall(r"\d+(?:[.,]\d+)?", s or "")}


# ── ders deposu ───────────────────────────────────────────────────────────────────────────────────────────────────
def manifest(ders_id: str) -> dict:
    m = oku(DEPO / ders_id / "manifest.json")
    if not m:
        raise SystemExit(f"ders bilgi deposu yok: {DEPO / ders_id} (scripts/dersler/bilgi_deposu.py)")
    return m


def pdf_bul(ders_id: str) -> Path:
    """Dersin PDF'i: manifest `pdf_yolu` (Kurul 2+ ders işçisi), yoksa ad ile `meds_downloads/**/Kurul N/` altında."""
    m = manifest(ders_id)
    for anahtar in ("pdf_yolu", "pdf_tam"):
        if m.get(anahtar) and Path(m[anahtar]).exists():
            return Path(m[anahtar])
    ad = m.get("pdf")
    if not ad:
        raise SystemExit(f"{ders_id}: manifestte pdf adı yok")
    kurul = m.get("kurul")
    kok_dizin = INDIR / "drive_root" / f"Kurul {kurul}"
    adaylar = sorted(kok_dizin.rglob(ad)) or sorted(INDIR.rglob(ad))
    if adaylar:
        return adaylar[0]
    # Ad değişmiş olabilir (Drive'da numara/sözcük değişti): ad benzerliği adayı, İÇERİKLE doğrulanır (hata kabul edilmez)
    import difflib
    import unicodedata

    def sade_ad(x: str) -> str:
        x = unicodedata.normalize("NFC", x)
        return katla(re.sub(r"^\s*\d+\s*[).-]\s*", "", Path(x).stem))

    hedef = sade_ad(ad)
    tum = [p for p in kok_dizin.rglob("*.pdf")]
    puanli = sorted(((difflib.SequenceMatcher(None, hedef, sade_ad(p.name)).ratio(), p) for p in tum), reverse=True)[:3]
    kaynak = (m.get("yollar") or {}).get("kaynak_md")
    ref = set(sozcukler(Path(kaynak).read_text(encoding="utf-8")[:20000])) if kaynak and Path(kaynak).exists() else set()
    for oran, p in puanli:
        if oran < 0.6:
            break
        if ref:
            import pymupdf
            b = pymupdf.open(str(p))
            aday = set(sozcukler(" ".join(b[i].get_text() for i in range(min(len(b), 8)))))
            ortak = len(ref & aday) / max(min(len(ref), len(aday)), 1)
            if ortak >= 0.6:
                return p
        elif oran >= 0.85 and sum(1 for o, _ in puanli if o >= 0.85) == 1:
            return p
    raise SystemExit(f"{ders_id}: PDF bulunamadı ya da içerikle doğrulanamadı: {ad}")


def dersler(kurul: int | None = None) -> list[str]:
    out = []
    for p in sorted(DEPO.glob("k*-*/manifest.json")):
        m = oku(p, {})
        if kurul is None or m.get("kurul") == kurul:
            out.append(p.parent.name)
    return out


# ── vektörler (bge-m3, önbellekli) ────────────────────────────────────────────────────────────────────────────────
def _onbellek():
    import sqlite3
    VEKTOR_ONBELLEK.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(str(VEKTOR_ONBELLEK) + ".sqlite", timeout=60)
    db.execute("CREATE TABLE IF NOT EXISTS v (k TEXT PRIMARY KEY, a BLOB)")
    return db


def vektorle(metinler: list[str]):
    """Normalleştirilmiş float32 matris (n × 1024). Metin karmasıyla tek dosyalık SQLite önbellek
    (meds_temp/kroki/vektor_onbellek.sqlite): aynı metin servise bir kez gider."""
    import numpy as np
    db = _onbellek()
    anahtar = [sha(t, 24) for t in metinler]
    var = {}
    for b in range(0, len(anahtar), 500):
        parca = anahtar[b:b + 500]
        for k, a in db.execute(f"SELECT k, a FROM v WHERE k IN ({','.join('?' * len(parca))})", parca):
            var[k] = np.frombuffer(a, dtype="float32")
    eksik = sorted({i for i, k in enumerate(anahtar) if k not in var}, key=lambda i: anahtar[i])
    tekil = list(dict.fromkeys(anahtar[i] for i in eksik))
    ilk = {anahtar[i]: i for i in eksik}
    for b in range(0, len(tekil), 32):
        grup = [ilk[k] for k in tekil[b:b + 32]]
        govde = json.dumps({"texts": [metinler[i][:2000] for i in grup], "kind": "raw"}).encode()
        req = urllib.request.Request(EMBED_URL, govde, {"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=600) as r:
            vek = json.loads(r.read())["vectors"]
        if len(vek) != len(grup):
            raise RuntimeError("vektör servisi eksik yanıt verdi")
        satir = []
        for i, v in zip(grup, vek):
            a = np.asarray(v, dtype="float32")
            a = a / max(float(np.linalg.norm(a)), 1e-9)
            var[anahtar[i]] = a
            satir.append((anahtar[i], a.tobytes()))
        db.executemany("INSERT OR REPLACE INTO v VALUES (?, ?)", satir)
        db.commit()
    db.close()
    if not metinler:
        return np.zeros((0, 1024), dtype="float32")
    return np.vstack([var[k] for k in anahtar])
