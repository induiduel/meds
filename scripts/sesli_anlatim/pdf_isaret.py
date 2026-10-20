#!/usr/bin/env python3
"""Sesli derste okunan cümlenin PDF slaytındaki KARŞILIĞI: satır, kelime, tablo hücresi ya da resim kutusu.

pdf_hizala.py her cümleye sayfa verir; bu betik o sayfanın içine iner. PDF'in kendi kelime kutuları
(PyMuPDF get_text("words"), tablo için find_tables, resim için get_image_info) okunur ve konuşmadaki her
kelime sırası korunarak slayttaki kelimeye bağlanır. Ön yüz tahmin yürütmez; bu dosyadaki kutuları çizer.

Eşleme (cümle × sayfa kelimeleri):
  - Türkçe katlama + 5 harf kök; sayılar birebir; ≤2 harfli ve bağlaç parçaları sayılmaz.
  - Sıra korumalı en uzun ortak alt dizi (LCS): konuşma kelimesi j → slayt kelimesi k, j ve k artan.
    Tek başına geçen yaygın kelime (ör. "hücre") başka satıra sıçramaz; satır başına en az 2 eşleşme ya da
    satırın yarısı aranır (kısa satırda 1 yeter).
  - Komşu sayfalar (±1) da denenir; belirgin üstünse (1,5×) o sayfa seçilir.
  - Metin karşılığı yoksa sayfada belirgin bir resim (sayfanın %4–85'i) varsa "resim" kutusu verilir;
    o da yoksa "sayfa" (yalnız sayfa vurgusu).

Çıktı: data/sesli_anlatim/isaret/<key>.json
  { surum:1, metinHash, c: { "<paragraf i>": [ <cümle işareti> | null, … ] } }
  cümle işareti: { d: dosya, s: sayfa, t: "metin"|"tablo"|"resim"|"sayfa",
                   l: [[x0,y0,x1,y1], …]          # satır/hücre/resim kutuları (sayfa oranı 0–1)
                   w: [[o, x0,y0,x1,y1], …] }      # kelime kutuları; o = kelimenin cümledeki karakter oranı (0–1)
Sunucu yalnız metinHash tutarsa gönderir (metin değişince eski işaret kendiliğinden yok sayılır).

Kullanım (PyMuPDF .venv-ocr'da):
  .venv-ocr/bin/python scripts/sesli_anlatim/pdf_isaret.py --hepsi | --key <key> [--rapor] [--kuru]
  --esik X : kapsama (metin+tablo+resim işaretli cümle oranı) bunun altındaysa çıkış kodu 1 (Kurul 2 kapısı)
3000 açık olmalı (paragraf/cümle bölmesi istemciyle birebir: GET /api/canli-ders/<key>). Yalnız CPU.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.request
import warnings
from pathlib import Path

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")
warnings.filterwarnings("ignore")
import pymupdf  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pdf_hizala import INDIR, STOP, katla  # noqa: E402

MEDS = Path(__file__).resolve().parents[2]
KOK = MEDS / "data" / "sesli_anlatim"
CIKTI = KOK / "isaret"
API = os.environ.get("MEDS_API", "http://127.0.0.1:3000")
KELIME = re.compile(r"[\wçğıöşüâîû]+", re.I)
CUMLE_RE = re.compile(r"[.!?…]+[\"'”’)\]]*(?:\s+|$)")


def cumle_sonlari(m: str) -> list[int]:
    """canliDersStore.ts::cumleSinirlari ile birebir."""
    out: list[int] = []
    for x in CUMLE_RE.finditer(m):
        if not x.group(0):
            continue
        e = x.end()
        s = m[e:e + 1]
        if s and s != s.upper() and s == s.lower():
            continue
        if e > (out[-1] if out else 0):
            out.append(e)
        if e >= len(m):
            break
    if not out or out[-1] < len(m):
        out.append(len(m))
    return out


def kok(w: str) -> str | None:
    k = katla(w)
    if not k:
        return None
    if k.isdigit():
        return "#" + k
    if len(k) <= 2 or k in STOP:
        return None
    return k[:5]


def tokenler(metin: str) -> list[tuple[str, int]]:
    """(kök, karakter konumu) — anlamsız parçalar atılır."""
    return [(k, m.start()) for m in KELIME.finditer(metin) if (k := kok(m.group(0)))]


class Sayfa:
    def __init__(self, pg: pymupdf.Page):
        W, H = pg.rect.width, pg.rect.height
        self.W, self.H = W, H
        M = pg.rotation_matrix  # sayfa kendi içinde döndürülmüşse kutular görünen yöne çevrilir (pdf.js de öyle çizer)

        def n(r):
            r = pymupdf.Rect(r) * M if pg.rotation else pymupdf.Rect(r)
            return [round(r.x0 / W, 4), round(r.y0 / H, 4), round(r.x1 / W, 4), round(r.y1 / H, 4)]
        self.n = n
        self.kelimeler = []  # (kök, satır anahtarı, kutu)
        self.satirlar: dict[tuple, list] = {}
        for x0, y0, x1, y1, w, b, l, _ in pg.get_text("words"):
            k = kok(w)
            if not k:
                continue
            key = (b, l)
            self.kelimeler.append((k, key, (x0, y0, x1, y1)))
            self.satirlar.setdefault(key, []).append((x0, y0, x1, y1))
        self.tablolar = []
        try:
            for t in pg.find_tables().tables:
                # slayt çerçevesi/tek kutu tablo sayılmaz: en az 2 satır × 2 sütun, dolu hücreler
                if t.row_count >= 2 and t.col_count >= 2 and sum(1 for r in t.extract() for c in r if c and c.strip()) >= 4:
                    self.tablolar.append(t.bbox)
        except Exception:
            pass
        self.resimler = []
        alan = W * H
        for im in pg.get_image_info():
            x0, y0, x1, y1 = im["bbox"]
            x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
            a = max(0, x1 - x0) * max(0, y1 - y0)
            if 0.04 * alan <= a <= 0.85 * alan:
                self.resimler.append((x0, y0, x1, y1))

    def tabloda(self, r) -> bool:
        cx, cy = (r[0] + r[2]) / 2, (r[1] + r[3]) / 2
        return any(t[0] <= cx <= t[2] and t[1] <= cy <= t[3] for t in self.tablolar)


def lcs(a: list[str], b: list[str]) -> list[tuple[int, int]]:
    n, m = len(a), len(b)
    if not n or not m:
        return []
    D = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        ai, Di, Dn = a[i], D[i], D[i + 1]
        for j in range(m - 1, -1, -1):
            Di[j] = Dn[j + 1] + 1 if ai == b[j] else max(Dn[j], Di[j + 1])
    out, i, j = [], 0, 0
    while i < n and j < m:
        if a[i] == b[j]:
            out.append((i, j))
            i += 1
            j += 1
        elif D[i + 1][j] >= D[i][j + 1]:
            i += 1
        else:
            j += 1
    return out


def eslestir(cumle: str, sy: Sayfa):
    tk = tokenler(cumle)
    if not tk or not sy.kelimeler:
        return 0, None
    es = lcs([k for k, _ in tk], [k for k, _, _ in sy.kelimeler])
    satir_say: dict[tuple, int] = {}
    for _, j in es:
        satir_say[sy.kelimeler[j][1]] = satir_say.get(sy.kelimeler[j][1], 0) + 1
    gecerli = set()
    for key, c in satir_say.items():
        uz = len(sy.satirlar[key])
        if c >= 2 or c / uz >= 0.5:
            gecerli.add(key)
    es = [(i, j) for i, j in es if sy.kelimeler[j][1] in gecerli]
    if not es:
        return 0, None
    L = len(cumle) or 1
    w = [[round(tk[i][1] / L, 3), *sy.n(sy.kelimeler[j][2])] for i, j in es]
    l, tablo = [], 0
    for key in sorted(gecerli, key=lambda k: min(r[1] for r in sy.satirlar[k])):
        rs = sy.satirlar[key]
        r = (min(x[0] for x in rs), min(x[1] for x in rs), max(x[2] for x in rs), max(x[3] for x in rs))
        tablo += sy.tabloda(r)
        l.append(sy.n(r))
    return len(es), {"t": "tablo" if tablo * 2 >= len(l) else "metin", "l": l, "w": w}


class Pdf:
    def __init__(self, yol: Path):
        self.doc = pymupdf.open(yol)
        self.cache: dict[int, Sayfa] = {}

    def sayfa(self, s: int) -> Sayfa | None:
        if not 1 <= s <= self.doc.page_count:
            return None
        if s not in self.cache:
            self.cache[s] = Sayfa(self.doc[s - 1])
        return self.cache[s]


def ders_isle(key: str, kuru: bool) -> dict | None:
    hz_yol = KOK / "hizalama" / f"{key}.json"
    if not hz_yol.exists():
        return None
    hz = json.loads(hz_yol.read_text(encoding="utf-8"))
    with urllib.request.urlopen(f"{API}/api/canli-ders/{key}", timeout=30) as r:
        d = json.load(r)
    paras = [p for b in d["bolumler"] for p in b["paragraflar"]]
    if len(paras) != len(hz["paragraflar"]):
        return None
    pdfler: list[Pdf | None] = []
    for f in hz["dosyalar"]:
        yol = INDIR / f["path"]
        if not yol.exists() and os.environ.get("HIZALA_PDF_DIZIN"):
            ek = f"_{len(pdfler)}" if pdfler else ""
            yol = Path(os.environ["HIZALA_PDF_DIZIN"]) / f"{hz['deckId']}{ek}.pdf"
        pdfler.append(Pdf(yol) if yol.exists() else None)
    if not any(pdfler):
        return None
    metin_hash = hashlib.sha1("\n".join(p["metin"] for p in paras).encode("utf-8")).hexdigest()
    say = {"metin": 0, "tablo": 0, "resim": 0, "sayfa": 0, "yok": 0}
    c_out: dict[str, list] = {}
    for p, es in zip(paras, hz["paragraflar"]):
        m = p["metin"]
        sinir = cumle_sonlari(m)
        liste = []
        for ci, e in enumerate(sinir):
            cumle = m[(sinir[ci - 1] if ci else 0):e]
            if not es:
                liste.append(None)
                say["yok"] += 1
                continue
            s0 = (es.get("sayfalar") or [])[ci] if ci < len(es.get("sayfalar") or []) else es["sayfa"]
            d0 = (es.get("dosyalar") or [])[ci] if ci < len(es.get("dosyalar") or []) else es.get("dosya", 0)
            pdf = pdfler[d0] if d0 < len(pdfler) else None
            if not pdf:
                liste.append(None)
                say["yok"] += 1
                continue
            en = (0, None, s0)
            for s in (s0, s0 - 1, s0 + 1):
                sy = pdf.sayfa(s)
                if not sy:
                    continue
                n, r = eslestir(cumle, sy)
                esik = en[0] * 1.5 if s != s0 else 0
                if r and n > esik and (s == s0 or n >= 3):
                    if en[1] is None or n > en[0]:
                        en = (n, r, s)
            n, r, s = en
            if r:
                isr = {"d": d0, "s": s, **r}
            else:
                sy = pdf.sayfa(s0)
                if sy and sy.resimler:
                    rb = max(sy.resimler, key=lambda b: (b[2] - b[0]) * (b[3] - b[1]))
                    isr = {"d": d0, "s": s0, "t": "resim", "l": [sy.n(rb)], "w": []}
                else:
                    isr = {"d": d0, "s": s0, "t": "sayfa", "l": [], "w": []}
            say[isr["t"]] += 1
            liste.append(isr)
        c_out[str(p["i"])] = liste
    toplam = sum(say.values()) or 1
    kapsama = (say["metin"] + say["tablo"] + say["resim"]) / toplam
    sonuc = {"surum": 1, "metinHash": metin_hash, "c": c_out}
    if not kuru:
        CIKTI.mkdir(parents=True, exist_ok=True)
        out = CIKTI / f"{key}.json"
        tmp = out.with_suffix(".tmp")
        tmp.write_text(json.dumps(sonuc, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        os.replace(tmp, out)
    return {"say": say, "kapsama": kapsama}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--key", action="append")
    g.add_argument("--hepsi", action="store_true")
    ap.add_argument("--kuru", action="store_true")
    ap.add_argument("--esik", type=float, default=0.0)
    a = ap.parse_args()
    keys = a.key or sorted(p.stem for p in (KOK / "hizalama").glob("*.json"))
    kotu = 0
    for key in keys:
        try:
            r = ders_isle(key, a.kuru)
        except Exception as e:  # tek ders hatası diğerlerini durdurmasın
            print(f"{key}: HATA {e}")
            kotu += 1
            continue
        if not r:
            print(f"{key}: atlandı (hizalama/PDF/metin uyuşmuyor)")
            continue
        durum = "" if r["kapsama"] >= a.esik else "  << EŞİK ALTI"
        kotu += bool(durum)
        print(f"{key}: kapsama {r['kapsama']:.0%} {r['say']}{durum}")
    return 1 if kotu and a.esik else 0


if __name__ == "__main__":
    sys.exit(main())
