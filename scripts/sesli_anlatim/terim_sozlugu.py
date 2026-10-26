#!/usr/bin/env python3
"""Sesli ders PDF yardımcısı — slayt başına terim sözlüğü (kullanıcı isteği 2026-10-26).

Her slayttaki tıbbi terim, karıştırılabilecek terim, unutulabilecek terim, Latince/yabancı sözcük ve kısaltma için
1–2 cümlelik basit, net açıklama. Ön yüz (CanliDersDers.tsx · CdTerimKatman):
  - "Terim yardımcısı" (ⓘ) açıkken açıklamalar slaytın altındaki boşlukta panel olarak; boşluk yetmezse sayfa
    yalnız gerektiği kadar uzatılır,
  - kapalıyken terimlerin altı ince kesikli çizilir, dokununca açılır kartta açıklama gösterilir.

Akış (ders zinciri `terim` adımı, otomasyon/ders_zinciri.py):
  1. dok      KEY DIR          → DIR/sayfalar.md (sayfa metinleri), DIR/terimler.json (sözlük adaylarıyla taslak)
  2. Claude   TALIMAT_TERIM.md → DIR/terimler.json'u yazar
  3. dogrula  KEY DIR/terimler.json [--yaz] → kapı 0 HATA; --yaz: data/sesli_anlatim/terim/<key>.json (kutularla)
  Claude'suz yol: otomatik KEY|--hepsi [--yaz] — yalnız doğrulanmış sözlükten (src/data/medical_glossary.json).

terimler.json (yazar biçimi):
  { "key": "...", "s": { "<dosya>:<sayfa>": [ { "t": "Metaplazi", "a": "1–2 cümle.", "k": "terim|latince|karisan|kisaltma",
                                               "f": "karıştırılan terim (yalnız karisan)" } ] } }
Çıktı (sunucu → ön yüz, canliDers.ts `terim`):
  { surum, key, d: { "<dosya>": { "<sayfa>": { bos: alt boş oran, t: [ { t, a, k, f?, b: [[x0,y0,x1,y1], …] } ] } } } }
Kutular sayfa oranıdır (0–1). Yalnız CPU. PDF yerelde yoksa sunucunun ders PDF ucundan indirilir (pdf_isaret.pdf_indir).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")
import pymupdf  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pdf_hizala import INDIR, STOP, katla  # noqa: E402
from pdf_isaret import pdf_indir  # noqa: E402

MEDS = Path(__file__).resolve().parents[2]
KOK = MEDS / "data" / "sesli_anlatim"
ARSIV_KOK = MEDS / "data" / "arsiv_25_26" / "sesli_anlatim"
API = os.environ.get("MEDS_API", "http://127.0.0.1:3000")
SURUM = 1
TURLER = {"terim", "latince", "karisan", "kisaltma"}
EN_COK = 8          # sayfa başına terim
A_ENAZ, A_ENCOK = 25, 280
TOK = re.compile(r"[\wçğıöşüâîû]+(?:[-'’][\wçğıöşüâîû]+)*", re.I)
ARSIV = re.compile(r"^y25-k\d+-\d+-[a-z0-9-]+$")


def kok_sec(key: str) -> Path:
    return ARSIV_KOK if ARSIV.match(key) else KOK


def fold(w: str) -> str:
    return katla(w.replace("’", "'").split("'")[0])


def ders(key: str) -> dict:
    with urllib.request.urlopen(f"{API}/api/canli-ders/{urllib.parse.quote(key)}", timeout=30) as r:
        return json.load(r)


def pdfler(d: dict) -> list[pymupdf.Document | None]:
    pdf = d.get("pdf") or {}
    out = []
    for fi, f in enumerate(pdf.get("dosyalar") or []):
        yol = INDIR / f.get("path", "")
        if not yol.is_file():
            yol = pdf_indir(pdf.get("deckId", ""), f, fi)
        out.append(pymupdf.open(yol) if yol and Path(yol).is_file() else None)
    return out


class Sayfa:
    """Sayfa kelimeleri (oran kutularıyla) ve alt boşluk."""

    def __init__(self, pg: pymupdf.Page):
        W, H = pg.rect.width or 1, pg.rect.height or 1
        self.kel: list[tuple[str, list[float], tuple[int, int]]] = []  # (katlanmış, kutu, (blok, satır))
        self.metin_satir: list[str] = []
        son = None
        satir: list[str] = []
        alt = 0.0
        for x0, y0, x1, y1, w, b, ln, _ in pg.get_text("words"):
            kutu = [max(0, x0 / W), max(0, y0 / H), min(1, x1 / W), min(1, y1 / H)]
            alt = max(alt, kutu[3])
            if (b, ln) != son and satir:
                self.metin_satir.append(" ".join(satir)); satir = []
            son = (b, ln); satir.append(w)
            for m in TOK.finditer(w):
                # parça kutusu: kelime içindeki konuma göre orantılı
                n = max(1, len(w))
                bx = [kutu[0] + (kutu[2] - kutu[0]) * m.start() / n, kutu[1], kutu[0] + (kutu[2] - kutu[0]) * m.end() / n, kutu[3]]
                self.kel.append((fold(m.group()), bx, (b, ln)))
        if satir:
            self.metin_satir.append(" ".join(satir))
        for im in pg.get_image_info():
            r = im.get("bbox")
            if r and (r[2] - r[0]) * (r[3] - r[1]) < 0.9 * W * H:  # zemin resmi sayılmaz
                alt = max(alt, min(1, r[3] / H))
        self.bos = round(max(0.0, 1 - alt - 0.01), 4)

    def bul(self, terim: str, en_cok: int = 3) -> list[list[float]]:
        """Terimin sayfadaki geçişleri (Türkçe ek payı: her parça önek eşleşmesi); satır başına birleşik kutu."""
        par = [fold(m.group()) for m in TOK.finditer(terim)]
        par = [p for p in par if p]
        if not par:
            return []
        kutular: list[list[float]] = []
        k = self.kel
        for i in range(len(k) - len(par) + 1):
            ok = True
            for j, p in enumerate(par):
                w = k[i + j][0]
                if not (w == p or (len(p) >= 3 and w.startswith(p) and len(w) - len(p) <= 6)):
                    ok = False; break
            if not ok:
                continue
            satirlar: dict = {}
            for j in range(len(par)):
                _, bx, sl = k[i + j]
                s = satirlar.setdefault(sl, list(bx))
                s[0], s[1], s[2], s[3] = min(s[0], bx[0]), min(s[1], bx[1]), max(s[2], bx[2]), max(s[3], bx[3])
            kutular.extend([round(v, 4) for v in s] for s in satirlar.values())
            if len(kutular) >= en_cok:
                break
        return kutular[:en_cok * 2]


def sayfalar(d: dict) -> dict[str, Sayfa]:
    out = {}
    for di, doc in enumerate(pdfler(d)):
        if doc is None:
            continue
        for si in range(doc.page_count):
            out[f"{di}:{si + 1}"] = Sayfa(doc[si])
    return out


# ── doğrulanmış sözlük (otomatik yol ve aday listesi) ─────────────────────────────────────────────────────────────
def sozluk() -> dict[tuple[str, ...], dict]:
    g = json.loads((MEDS / "src/data/medical_glossary.json").read_text(encoding="utf-8"))
    out: dict[tuple[str, ...], dict] = {}
    for v in g.values():
        if not isinstance(v, dict):
            continue
        tanim = kisa_tanim(str(v.get("definition") or v.get("description") or ""))
        if not tanim:
            continue
        for ad in [v.get("term", "")] + list(v.get("aliases") or []):
            par = tuple(fold(m.group()) for m in TOK.finditer(re.sub(r"\(.*?\)", " ", str(ad))))
            if not par or (len(par) == 1 and (len(par[0]) < 5 or par[0] in STOP)):
                continue
            out.setdefault(par, {"t": re.sub(r"\s*\(.*?\)", "", str(ad)).strip(), "a": tanim,
                                 "k": "kisaltma" if str(ad).isupper() and len(str(ad)) <= 6 else "terim"})
    return out


def kisa_tanim(t: str) -> str:
    t = re.sub(r"\s+", " ", t).strip()
    cumleler = re.split(r"(?<=[.!?])\s+(?=[A-ZÇĞİÖŞÜ])", t)
    a = cumleler[0] if cumleler else ""
    if len(cumleler) > 1 and len(a) + len(cumleler[1]) + 1 <= A_ENCOK:
        a = f"{a} {cumleler[1]}"
    return a if A_ENAZ <= len(a) <= A_ENCOK and a.endswith(".") else ""


def adaylar(sy: Sayfa, sz: dict) -> list[dict]:
    seq = [w for w, _, _ in sy.kel]
    bulunan: dict[str, dict] = {}
    for n in range(5, 0, -1):
        for i in range(len(seq) - n + 1):
            e = sz.get(tuple(seq[i:i + n]))
            if e and e["t"].lower() not in bulunan:
                bulunan[e["t"].lower()] = e
    # uzun (çok sözcüklü) terimler önce; aynı tanımı ya da seçilmiş terimin içinde kalanı tekrar etme
    secilen: list[dict] = []
    for e in sorted(bulunan.values(), key=lambda e: -len(e["t"])):
        if any(e["a"] == s["a"] or fold(e["t"]) in fold(s["t"]) for s in secilen):
            continue
        secilen.append(e)
    return secilen[:EN_COK]


# ── kapı ──────────────────────────────────────────────────────────────────────────────────────────────────────────
def denetle(key: str, yazar: dict, sy: dict[str, Sayfa]) -> tuple[list[str], dict]:
    try:
        from turkce_uslup import denetle as uslup
    except Exception:  # noqa: BLE001
        uslup = lambda m, y: []  # noqa: E731
    hata: list[str] = []
    cikti: dict = {}
    for yer, liste in (yazar.get("s") or {}).items():
        if yer not in sy:
            hata.append(f"{yer}: böyle bir sayfa yok"); continue
        if not isinstance(liste, list):
            hata.append(f"{yer}: liste olmalı"); continue
        if len(liste) > EN_COK:
            hata.append(f"{yer}: {len(liste)} terim (en çok {EN_COK})")
        gor = set()
        for i, x in enumerate(liste):
            y = f"{yer}#{i + 1}"
            t, a, k = str(x.get("t") or "").strip(), str(x.get("a") or "").strip(), x.get("k")
            if not t:
                hata.append(f"{y}: terim boş"); continue
            if t.lower() in gor:
                hata.append(f"{y}: '{t}' sayfada iki kez"); continue
            gor.add(t.lower())
            if k not in TURLER:
                hata.append(f"{y}: tür '{k}' geçersiz ({', '.join(sorted(TURLER))})")
            if not (A_ENAZ <= len(a) <= A_ENCOK):
                hata.append(f"{y}: açıklama {len(a)} karakter ({A_ENAZ}–{A_ENCOK})")
            if "…" in a or "..." in a or not a.endswith((".", "!", "?")):
                hata.append(f"{y}: açıklama tam cümleyle bitmeli (kesme yok)")
            if len(re.findall(r"[.!?](?:\s|$)", a)) > 2:
                hata.append(f"{y}: açıklama en çok 2 cümle")
            if k == "karisan" and not str(x.get("f") or "").strip():
                hata.append(f"{y}: karisan türünde karıştırılan terim (f) zorunlu")
            hata.extend(uslup(a, y))
            b = sy[yer].bul(t)
            if not b:
                hata.append(f"{y}: '{t}' bu sayfanın metninde bulunamadı (slayttaki yazımı kullan)"); continue
            d, s = yer.split(":")
            sayfa = cikti.setdefault(d, {}).setdefault(s, {"bos": sy[yer].bos, "t": []})
            o = {"t": t, "a": a, "k": k, "b": b}
            if x.get("f"):
                o["f"] = str(x["f"]).strip()
            sayfa["t"].append(o)
    return hata, {"surum": SURUM, "key": key, "d": cikti}


def yaz(key: str, cikti: dict) -> Path:
    hedef = kok_sec(key) / "terim" / f"{key}.json"
    hedef.parent.mkdir(parents=True, exist_ok=True)
    tmp = hedef.with_suffix(".tmp")
    tmp.write_text(json.dumps(cikti, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    os.replace(tmp, hedef)
    return hedef


# ── komutlar ──────────────────────────────────────────────────────────────────────────────────────────────────────
def k_dok(key: str, dizin: Path) -> int:
    d = ders(key)
    sy = sayfalar(d)
    if not sy:
        print(f"{key}: PDF yok"); return 2
    dizin.mkdir(parents=True, exist_ok=True)
    sz = sozluk()
    md, taslak = [f"# {d.get('baslik', key)} — slayt metinleri\n"], {"key": key, "s": {}}
    for yer, s in sy.items():
        md.append(f"\n## {yer}\n" + ("\n".join(s.metin_satir) or "(metin yok — görsel slayt)"))
        ad = adaylar(s, sz)
        if ad:
            taslak["s"][yer] = ad
    (dizin / "sayfalar.md").write_text("\n".join(md), encoding="utf-8")
    hedef = dizin / "terimler.json"
    if not hedef.exists():
        hedef.write_text(json.dumps(taslak, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{key}: {len(sy)} sayfa → {dizin}")
    return 0


def k_dogrula(key: str, dosya: Path, yazilsin: bool) -> int:
    yazar = json.loads(dosya.read_text(encoding="utf-8"))
    hata, cikti = denetle(key, yazar, sayfalar(ders(key)))
    for h in hata:
        print("HATA", h)
    n = sum(len(s["t"]) for d in cikti["d"].values() for s in d.values())
    print(f"{key}: {n} terim · {len(hata)} HATA")
    if hata:
        return 1
    if yazilsin:
        print("yazıldı:", yaz(key, cikti))
    return 0


def k_otomatik(key: str, yazilsin: bool, sz: dict) -> int:
    sy = sayfalar(ders(key))
    if not sy:
        print(f"{key}: PDF yok"); return 0
    yazar = {"key": key, "s": {yer: ad for yer, s in sy.items() if (ad := adaylar(s, sz))}}
    hata, cikti = denetle(key, yazar, sy)
    # sözlük tanımı kapıdan geçmediyse o terim düşer (otomatik yolda hata durdurmaz)
    n = sum(len(s["t"]) for d in cikti["d"].values() for s in d.values())
    print(f"{key}: {n} terim (sözlükten) · {len(hata)} düşen")
    if yazilsin and n:
        yaz(key, cikti)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    alt = ap.add_subparsers(dest="komut", required=True)
    a1 = alt.add_parser("dok"); a1.add_argument("key"); a1.add_argument("dizin", type=Path)
    a2 = alt.add_parser("dogrula"); a2.add_argument("key"); a2.add_argument("dosya", type=Path); a2.add_argument("--yaz", action="store_true")
    a3 = alt.add_parser("otomatik"); a3.add_argument("key", nargs="?"); a3.add_argument("--hepsi", action="store_true")
    a3.add_argument("--yaz", action="store_true")
    a = ap.parse_args()
    if a.komut == "dok":
        return k_dok(a.key, a.dizin)
    if a.komut == "dogrula":
        return k_dogrula(a.key, a.dosya, a.yaz)
    sz = sozluk()
    keys = [a.key] if a.key else sorted({p.stem for k in (KOK, ARSIV_KOK) for p in (k / "hizalama").glob("*.json")}) if a.hepsi else []
    for key in keys:
        try:
            k_otomatik(key, a.yaz, sz)
        except Exception as e:  # noqa: BLE001
            print(f"{key}: HATA {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
