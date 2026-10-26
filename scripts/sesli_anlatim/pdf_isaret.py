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
  cümle işareti: { d: dosya, s: sayfa, t: "metin"|"tablo"|"kelime"|"resim"|"sayfa",
                   l: [[x0,y0,x1,y1], …]          # ≥%80'i okunan madde satırları / resim kutusu (sayfa oranı 0–1)
                   w: [[b, e, x0,y0,x1,y1], …] }   # kelime kutuları; [b, e) = konuşulan kelimenin cümle içi karakter aralığı
Sunucu yalnız metinHash tutarsa gönderir (metin değişince eski işaret kendiliğinden yok sayılır).

Kullanım (PyMuPDF .venv-ocr'da):
  .venv-ocr/bin/python scripts/sesli_anlatim/pdf_isaret.py --hepsi | --key <key> [--kuru] [--zorla]
  Değişmemiş ders (aynı metinHash + hizalama + SURUM) atlanır; zamanlayıcıda (cihaz ve Oracle) ~saniyeler.
  Yerelde PDF yoksa sunucunun /api/lecture-pdf/deck/<id>/<i> ucundan .pdf_onbellek'e indirilir.
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
import urllib.parse
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
# Üretim sunucusunun bot koruması urllib'in varsayılan kimliğini 403 ile reddediyor: açık kimlik gönderilir.
UA = {"User-Agent": "medsor-sesli-anlatim/1"}


def api_iste(url: str, timeout: int = 30) -> "urllib.request.Request":
    return urllib.request.Request(url, headers=UA)
KELIME = re.compile(r"[\wçğıöşüâîû]+", re.I)
MADDE_IMI = re.compile(r"^(?:[•●▪■◦○➢➤►▶✓✔\-–—*]|\d{1,2}[.)]|[a-zA-Z][.)])$")
GORSEL = re.compile(r"\b(görsel|görüntü|şekil|resim|fotoğraf|grafik|şema|tablo|çizim|mikrograf|kesit|plak|görürsünüz|görüyoruz|görülüyor|görülen|bakın|bakalım)", re.I)
SURUM = 7  # eşleme kuralı değişince artır: tüm dersler yeniden üretilir
MADDE_ORAN = 0.80  # slayt maddesinin en az bu kadarı okunan cümlede geçmeli (kullanıcı kuralı)
CUMLE_RE = re.compile(r"[.!?…]+[\"'”’)\]]*(?:\s+|$)")
BULLET_PREFIX = re.compile(r"^[^\wçğıöşüâîû]+", re.I)


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
    w = BULLET_PREFIX.sub("", w)
    k = katla(w)
    if not k:
        return None
    if k.isdigit():
        return "#" + k
    if len(k) <= 2 or k in STOP:
        return None
    return k[:5]


def tokenler(metin: str) -> list[tuple[str, int, int]]:
    """(kök, başlangıç, bitiş) — anlamsız parçalar atılır."""
    return [(k, m.start(), m.end()) for m in KELIME.finditer(metin) if (k := kok(m.group(0)))]


def ocr_kelimeler(pg: pymupdf.Page, anahtar: str) -> list:
    """Taranmış (metin katmanı olmayan) slayt: Tesseract (tur) ile kelime kutuları; sonuç önbelleğe yazılır.
    Tesseract yoksa boş döner (sayfa yalnız sayfa vurgusu alır)."""
    yol = Path(os.environ.get("PDF_ONBELLEK", str(KOK / ".pdf_onbellek"))) / "ocr" / f"{anahtar}.json"
    if yol.exists():
        return json.loads(yol.read_text())
    import shutil
    import subprocess
    import tempfile
    if not shutil.which("tesseract") or pg.rotation:  # döndürülmüş sayfada kırpma koordinatı ayrı tutulmaz
        return []
    # Tam sayfa değil resim kutusu kırpılır: geniş boş kenarlı sayfada Tesseract bölütleme yapamayıp boş döner
    dpi = 300
    k = 72 / dpi
    W, H = pg.rect.width, pg.rect.height
    kutular = []
    for im in pg.get_image_info():
        r = pymupdf.Rect(im["bbox"]) & pg.rect
        if r.width * r.height >= 0.04 * W * H:
            kutular.append(r)
    ws = []
    with tempfile.TemporaryDirectory() as td:
        for bi, r in enumerate(kutular[:6]):
            png = Path(td) / f"r{bi}.png"
            pg.get_pixmap(dpi=dpi, clip=r, colorspace=pymupdf.csGRAY).save(str(png))
            try:
                tsv = subprocess.run(["nice", "-n", "15", "tesseract", str(png), "-", "-l", "tur", "--psm", "3", "tsv"],
                                     capture_output=True, text=True, timeout=180,
                                     env={**os.environ, "OMP_THREAD_LIMIT": "1"}).stdout
            except Exception:
                continue
            for ln in tsv.splitlines()[1:]:
                c = ln.split("\t")
                if len(c) < 12 or c[0] != "5" or not c[11].strip() or float(c[10]) < 40:
                    continue
                x, y, w, h = (int(v) * k for v in c[6:10])
                # (x0, y0, x1, y1, kelime, blok, satır, sıra): blok = resim×10⁶ + blok×10³ + paragraf
                ws.append([r.x0 + x, r.y0 + y, r.x0 + x + w, r.y0 + y + h, c[11],
                           bi * 1_000_000 + int(c[2]) * 1000 + int(c[3]), int(c[4]), int(c[5])])
    yol.parent.mkdir(parents=True, exist_ok=True)
    yol.write_text(json.dumps(ws, ensure_ascii=False))
    return ws


class Sayfa:
    def __init__(self, pg: pymupdf.Page, ocr_anahtar: str | None = None):
        W, H = pg.rect.width, pg.rect.height
        self.W, self.H = W, H
        M = pg.rotation_matrix  # sayfa kendi içinde döndürülmüşse kutular görünen yöne çevrilir (pdf.js de öyle çizer)

        def n(r):
            r = pymupdf.Rect(r) * M if pg.rotation else pymupdf.Rect(r)
            return [round(r.x0 / W, 4), round(r.y0 / H, 4), round(r.x1 / W, 4), round(r.y1 / H, 4)]
        self.n = n
        # Madde: madde imiyle (•, –, 1. …) başlayan satır + aynı bloktaki devam satırları; imsiz blokta her satır
        # cümle sonuyla biter. Kelimeler (kök, madde no, kutu); madde → satır kutuları ve içerik kökü sayısı.
        self.kelimeler = []
        self.maddeler: list[dict] = []
        satirlar: dict[tuple, list] = {}
        kelimeler = pg.get_text("words")
        self.ocr = False
        if ocr_anahtar and sum(1 for w in kelimeler if kok(w[4])) < 5 and pg.get_images():
            kelimeler = ocr_kelimeler(pg, ocr_anahtar) or kelimeler
            self.ocr = kelimeler is not None and len(kelimeler) > 0
        for x0, y0, x1, y1, w, b, l, _ in kelimeler:
            satirlar.setdefault((b, l), []).append((w, (x0, y0, x1, y1)))
        onceki_blok, acik = None, None
        for (b, l), ws in sorted(satirlar.items()):
            ilk = ws[0][0]
            clean_ilk = BULLET_PREFIX.sub("", ilk)
            im = bool(MADDE_IMI.match(ilk)) or ilk != clean_ilk or bool(re.match(r"^[•●▪■◦○➢➤►▶✓✔\-–—*]\s*", ilk))
            if b != onceki_blok or im or acik is None or acik["bitti"]:
                acik = {"satirlar": [], "kok": 0, "bitti": False, "metin": [], "koks": set()}
                self.maddeler.append(acik)
            onceki_blok = b
            r = (min(x[1][0] for x in ws), min(x[1][1] for x in ws), max(x[1][2] for x in ws), max(x[1][3] for x in ws))
            acik["satirlar"].append(r)
            mi = len(self.maddeler) - 1
            for w, box in ws:
                acik["metin"].append(w)
                k = kok(w)
                if k:
                    self.kelimeler.append((k, mi, box))
                    acik["kok"] += 1
                    acik["koks"].add(k)
            acik["bitti"] = bool(re.search(r"[.!?:]$", ws[-1][0])) or im
        self.tablolar = []
        try:
            for t in pg.find_tables().tables:
                # slayt çerçevesi/tek kutu tablo sayılmaz: en az 2 satır × 2 sütun, dolu hücreler
                if t.row_count >= 2 and t.col_count >= 2 and sum(1 for r in t.extract() for c in r if c and c.strip()) >= 4:
                    self.tablolar.append(t.bbox)
        except Exception:
            pass
        # R# dizini kalıcıdır (yazılmış çapalar ona bakar): aynı yere üst üste konmuş görsel (maske, yinelenen yerleşim)
        # listede kalır ama tekil_resim'e girmez; dökümde ve otomatik seçimde yalnız tekiller görünür (2026-10-25).
        self.resimler = []
        self.tekil_resim: list[int] = []
        self.zemin = None  # sayfanın %85'inden büyük görsel (taranmış slayt/arka plan): yalnız şekil çapasında yedek
        alan = W * H
        for im in pg.get_image_info():
            x0, y0, x1, y1 = im["bbox"]
            x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
            a = max(0, x1 - x0) * max(0, y1 - y0)
            if 0.04 * alan <= a <= 0.85 * alan:
                b = (x0, y0, x1, y1)
                if not any(kesisim_orani(b, self.resimler[i]) >= 0.9 for i in self.tekil_resim):
                    self.tekil_resim.append(len(self.resimler))
                self.resimler.append(b)
            elif a > 0.85 * alan:
                self.zemin = (round(W * 0.04, 2), round(H * 0.04, 2), round(W * 0.96, 2), round(H * 0.96, 2))
        # Yazının arkasındaki şablon/kart zemini resim değildir (H59: yazı slaytı bütünüyle "resim" diye işaretleniyordu):
        # içinde ≥8 metin kelimesi olan görsel kutusu tekil resim listesinden çıkar (dizin kalıcı, yalnız seçilmez).
        def _yazi_say(b):
            return sum(1 for _, _, w in self.kelimeler if b[0] <= (w[0] + w[2]) / 2 <= b[2] and b[1] <= (w[1] + w[3]) / 2 <= b[3])
        if not self.ocr:
            self.tekil_resim = [i for i in self.tekil_resim if _yazi_say(self.resimler[i]) < 8]
        # tam sayfa görsel ancak slaytın kendisiyse (taranmış, metin katmanı az ya da OCR) zemin yedeğidir; yazılı slaytın
        # arkasındaki şablon görseli değil
        if self.zemin and len(self.kelimeler) >= 15 and not self.ocr:
            self.zemin = None
        # Metinsiz/az metinli tam slayt görseli ya da diyagramı (şema, anatomi, radyoloji)
        if not self.resimler and (not self.kelimeler or len(self.kelimeler) < 15) and pg.get_image_info():
            self.resimler.append((round(W * 0.04, 2), round(H * 0.04, 2), round(W * 0.96, 2), round(H * 0.96, 2)))
            self.tekil_resim = [0]

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


def c_oran(c: int, n: int) -> float:
    return c / n if n else 0.0


def eslestir(cumle: str, sy: Sayfa):
    """Kelime eşlemesi: önce sıra korumalı (LCS), sonra madde içinde sırasız ortak kökler (anlatım slaytı başka sırayla
    anlatabilir). Madde zemini yalnız maddenin farklı köklerinin ≥%80'i cümlede geçiyorsa; kelime işareti yalnız
    gerçekten anlatılan maddede (≥2 farklı ortak kök ve maddenin en az %30'u, ya da ≥3 ortak kök)."""
    tk = tokenler(cumle)
    if not tk or not sy.kelimeler:
        return 0, None
    S = {k for k, _, _ in tk}
    ilk3 = {k for k, _, _ in tk[:3]}
    anlatilan, tam = set(), set()
    for m, md in enumerate(sy.maddeler):
        ks = md["koks"]
        if not ks:
            continue
        d = len(ks & S)
        oran = d / len(ks)
        # tek kelimelik madde (başlık: "Patoloji:") ancak cümle o kelimeyle açılıyorsa
        if d >= 3 or (d >= 2 and oran >= 0.3) or (len(ks) == 1 and ks <= ilk3):
            anlatilan.add(m)
            if oran >= MADDE_ORAN:
                tam.add(m)
    if not anlatilan:
        return 0, None
    # konuşulan kelime → slayt kelimesi: LCS çiftleri öncelikli, kalanlar ilk boş eşiyle (her iki taraf tekil)
    es = [(i, j) for i, j in lcs([k for k, _, _ in tk], [k for k, _, _ in sy.kelimeler]) if sy.kelimeler[j][1] in anlatilan]
    kul_i, kul_j = {i for i, _ in es}, {j for _, j in es}
    for j, (k, m, _) in enumerate(sy.kelimeler):
        if m not in anlatilan or j in kul_j:
            continue
        i = next((i for i, (kk, _, _) in enumerate(tk) if kk == k and i not in kul_i), None)
        if i is not None:
            es.append((i, j)); kul_i.add(i); kul_j.add(j)
    es.sort()
    w = [[tk[i][1], tk[i][2], *sy.n(sy.kelimeler[j][2])] for i, j in es]
    l, tablo = [], 0
    for m in sorted(tam):
        for r in sy.maddeler[m]["satirlar"]:
            tablo += sy.tabloda(r)
            l.append(sy.n(r))
    tur = "tablo" if l and tablo * 2 >= len(l) else "metin" if l else "kelime"
    return len(es), {"t": tur, "l": l, "w": w}


def madde_kokleri(sy: Sayfa, m: int) -> list[str]:
    return [k for k, mi, _ in sy.kelimeler if mi == m]


def capa_maddeleri(sy: Sayfa, satirlar: list[str]) -> set[int]:
    """Yazarın kaynak.md'den birebir kopyaladığı satır(lar) → PDF maddeleri. kaynak.md ile PDF metni küçük farklar
    taşıyabilir (OCR, bölünmüş satır): satırın köklerinin ≥%80'ini ardışık maddelerde toplayan en kısa aralık seçilir."""
    out: set[int] = set()
    for st in satirlar:
        hedef = [k for k, _, _ in tokenler(st)]
        if not hedef:
            continue
        en = None
        for a in range(len(sy.maddeler)):
            kok_say: list[str] = []
            for b in range(a, min(a + 4, len(sy.maddeler))):
                kok_say += madde_kokleri(sy, b)
                ort = len(lcs(hedef, kok_say))
                if ort / len(hedef) >= MADDE_ORAN and ort / max(1, len(kok_say)) >= 0.5:
                    if en is None or (b - a, -ort) < (en[1] - en[0], -en[2]):
                        en = (a, b, ort)
                    break
        if en:
            out.update(range(en[0], en[1] + 1))
    return out


def eslestir_capa(cumle: str, sy: Sayfa, ms: set[int]):
    """Çapalı cümle: madde zemini yazarın gösterdiği maddeler; kelimeler yalnız bu maddelerde aranır."""
    tk = tokenler(cumle)
    idx = [j for j, (_, mi, _) in enumerate(sy.kelimeler) if mi in ms]
    es = lcs([k for k, _, _ in tk], [sy.kelimeler[j][0] for j in idx]) if tk else []
    w = [[tk[i][1], tk[i][2], *sy.n(sy.kelimeler[idx[j]][2])] for i, j in es]
    l, tablo = [], 0
    for m in sorted(ms):
        for r in sy.maddeler[m]["satirlar"]:
            tablo += sy.tabloda(r)
            l.append(sy.n(r))
    return {"t": "tablo" if tablo * 2 >= len(l) else "metin", "l": l, "w": w}


def kesisim_orani(a, b) -> float:
    """İki kutunun kesişim / birleşim oranı (IoU)."""
    ix = max(0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    k = ix * iy
    u = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - k
    return k / u if u > 0 else 0.0


def resim_kutusu(sy: Sayfa, zemin: bool = False):
    """Sayfanın en büyük tekil resim kutusu; yoksa ve zemin istenirse tam sayfa görselin kutusu."""
    tekil = [sy.resimler[i] for i in sy.tekil_resim]
    if tekil:
        return max(tekil, key=lambda b: (b[2] - b[0]) * (b[3] - b[1]))
    return sy.zemin if zemin else None


TABLO_SOZ = re.compile(r"\b(tablo|table|çizelge|sınıflama|karşılaştırma)", re.I)


def sekil_isareti(sy: Sayfa, sayfa: int, capalar: list[dict]) -> dict | None:
    """Şekil/tablo çapalı cümle: yazarın gösterdiği tablo (T#) ya da resim (R#), yoksa sayfadaki tablo/en büyük resim.
    Tablo anlatılıyorsa (çapada tablo, ya da şekil tarifinde "tablo") tür "tablo" olur; tablo PDF'te resimse kutusu R'dir."""
    tablo_mu = any(c.get("tablo") is not None and c.get("tablo") is not False for c in capalar) or \
        any(TABLO_SOZ.search(str(c.get("sekil") or "")) for c in capalar)
    for c in capalar:
        t = c.get("tablo")
        if isinstance(t, int) and not isinstance(t, bool) and 0 <= t < len(sy.tablolar):
            return {"s": sayfa, "t": "tablo", "l": [sy.n(sy.tablolar[t])], "w": []}
    tur = "tablo" if tablo_mu else "resim"
    for c in capalar:
        if c.get("kutu"):
            return {"s": sayfa, "t": tur, "l": [[round(float(v), 4) for v in c["kutu"]]], "w": []}
        if c.get("resim") is not None and 0 <= int(c["resim"]) < len(sy.resimler):
            return {"s": sayfa, "t": tur, "l": [sy.n(sy.resimler[int(c["resim"])])], "w": []}
    if tablo_mu and sy.tablolar:
        return {"s": sayfa, "t": "tablo", "l": [sy.n(t) for t in sy.tablolar], "w": []}
    rb = resim_kutusu(sy, zemin=True)
    return {"s": sayfa, "t": tur, "l": [sy.n(rb)], "w": []} if rb else None


def cumle_capalari(metin: str, sinir: list[int], capa: list[dict]) -> list[list[dict]]:
    """v2 cümleleri (ses metni) paragraf içinde sırayla bulunur; her istemci cümlesine başlangıcı içine düşen
    çapalar verilir (iki bölme farklı olabilir: v2 cümlesi istemcide ikiye bölünebilir ya da tersi)."""
    out: list[list[dict]] = [[] for _ in sinir]
    konum = 0
    for c in capa:
        i = metin.find(c.get("ses", "")[:40], konum)
        if i < 0:
            continue
        konum = i + 1
        ci = next((k for k, e in enumerate(sinir) if i < e), len(sinir) - 1)
        out[ci].append(c)
    return out


class Pdf:
    def __init__(self, yol: Path):
        self.doc = pymupdf.open(yol)
        self.kimlik = hashlib.sha1(f"{Path(yol).name}:{Path(yol).stat().st_size}".encode()).hexdigest()[:16]
        self.cache: dict[int, Sayfa] = {}

    def sayfa(self, s: int) -> Sayfa | None:
        if not 1 <= s <= self.doc.page_count:
            return None
        if s not in self.cache:
            self.cache[s] = Sayfa(self.doc[s - 1], f"{self.kimlik}_{s}")
        return self.cache[s]


def pdf_indir(deck_id: str, f: dict, fi: int) -> Path | None:
    """Yerelde olmayan PDF (Oracle): sunucunun ders PDF ucundan önbelleğe indirilir (Drive kimliği/adıyla eşlenir)."""
    ON = Path(os.environ.get("PDF_ONBELLEK", str(KOK / ".pdf_onbellek")))
    ON.mkdir(parents=True, exist_ok=True)
    try:
        with urllib.request.urlopen(api_iste(f"{API}/api/lecture-pdf/deck/{urllib.parse.quote(deck_id)}"), timeout=30) as r:
            dosyalar = json.load(r).get("files") or []
    except Exception:
        return None
    i = next((k for k, x in enumerate(dosyalar) if (f.get("fileId") and x.get("fileId") == f["fileId"]) or x.get("name") == f.get("name")), fi)
    if i >= len(dosyalar) or not dosyalar[i].get("available", True):
        return None
    hedef = ON / f"{deck_id}_{i}_{dosyalar[i].get('size') or 0}.pdf"
    if not hedef.exists():
        try:
            with urllib.request.urlopen(api_iste(f"{API}/api/lecture-pdf/deck/{urllib.parse.quote(deck_id)}/{i}"), timeout=180) as r:
                tmp = hedef.with_suffix(".tmp")
                tmp.write_bytes(r.read())
                os.replace(tmp, hedef)
        except Exception:
            return None
    return hedef


def imlec_yolu(cumle: str, capalar: list[dict]) -> list[list[float]]:
    """Hareketli imleç: çapadaki "yol" = [{"k": cümledeki ifade, "x":, "y": (sayfa oranı)}] → [[karakter, x, y]]
    (ifadenin cümledeki başlangıcı; ses o kelimeye gelince imleç o noktaya kayar)."""
    trk = lambda t: t.replace("İ", "i").replace("I", "ı").lower()  # uzunluk korunur (İ.lower() iki karakter olur)
    out, kucuk, konum = [], trk(cumle), 0
    for c in capalar:
        for n in c.get("yol") or []:
            k = trk(str(n.get("k") or "")).strip()
            i = kucuk.find(k, konum) if k else -1
            if i < 0 and k:
                i = kucuk.find(k)
            if i < 0:
                i = 0 if not out else -1
            if i < 0:
                continue
            konum = max(konum, i)
            v = [i, round(float(n["x"]), 4), round(float(n["y"]), 4)]
            if isinstance(n.get("r"), list) and len(n["r"]) == 4:  # o an anlatılan bölge (ince çerçeve)
                v += [round(float(z), 4) for z in n["r"]]
            out.append(v)
    out.sort(key=lambda v: v[0])
    return out


def bolge_sikilastir(yol: list[list[float]], sy: "Sayfa | None") -> list[list[float]]:
    """Yazı içeren bölgeyi (r) içindeki gerçek kelime kutularına oturtur: çizim tam anlatılan satır/hücreyi çevreler,
    komşu yapıları kapatmaz. İmleç noktası bölgenin dışındaysa bölgenin sol-ortasına çekilir."""
    if not sy:
        return yol
    for v in yol:
        if len(v) < 7:
            continue
        x0, y0, x1, y1 = v[3:7]
        ws = []
        for _, _, b in sy.kelimeler:
            n = sy.n(b)
            cx, cy = (n[0] + n[2]) / 2, (n[1] + n[3]) / 2
            if x0 <= cx <= x1 and y0 <= cy <= y1:
                ws.append(n)
        if ws:
            ux0, uy0 = min(w[0] for w in ws), min(w[1] for w in ws)
            ux1, uy1 = max(w[2] for w in ws), max(w[3] for w in ws)
            # yalnız yazı bölgesi (resim değil): kelimeler bölgenin anlamlı kısmını kaplıyorsa sıkılaştır
            if (ux1 - ux0) * (uy1 - uy0) >= 0.25 * max(1e-6, (x1 - x0) * (y1 - y0)):
                v[3:7] = [round(ux0 - 0.004, 4), round(uy0 - 0.004, 4), round(ux1 + 0.004, 4), round(uy1 + 0.004, 4)]
                x0, y0, x1, y1 = v[3:7]
        if not (x0 <= v[1] <= x1 and y0 <= v[2] <= y1):
            v[1], v[2] = round(x0 + 0.01, 4), round((y0 + y1) / 2, 4)
    return yol


def capali(cumle: str, capalar: list[dict], pdf: "Pdf | None") -> dict | None:
    isr = capali_ic(cumle, capalar, pdf)
    if isr:
        yol = imlec_yolu(cumle, capalar)
        if yol:
            isr["y"] = bolge_sikilastir(yol, pdf.sayfa(int(isr["s"])) if pdf else None)
    return isr


def capali_ic(cumle: str, capalar: list[dict], pdf: "Pdf | None") -> dict | None:
    """Yazar çapasından işaret: sayfa ve madde tahminsiz; şekil anlatılıyorsa resim + lazer."""
    if not pdf:
        return None
    sayfa = next((c.get("sayfa") for c in capalar if c.get("sayfa")), None)
    sy = pdf.sayfa(int(sayfa)) if sayfa else None
    if not sy:
        return None
    # Anlamsal çapa (2026-10-21): "madde" = Sayfa.maddeler dizinleri (capa_dok.py'nin numaraladığı M kutuları),
    # "resim" = Sayfa.resimler dizini (R kutuları), "tablo" = Sayfa.tablolar dizini (T kutuları) ya da true,
    # "kutu" = elle sayfa oranı kutu; kelime eşlemesi yalnız madde içinde.
    # Şekil/tablo anlatılıyorsa görsel önce gelir (2026-10-25): madde ya da tek ortak kelime onu ezemez.
    if any(c.get("sekil") or c.get("tablo") not in (None, False) for c in capalar):
        isr = sekil_isareti(sy, int(sayfa), capalar)
        if isr:
            return isr
        # çapanın sayfasında görsel yok: hizalama kayması (±1) — komşu sayfadaki görsel (R# dizini o sayfaya ait değil)
        yalin = [{k: v for k, v in c.items() if k not in ("resim", "kutu")} for c in capalar]
        for s2 in (int(sayfa) + 1, int(sayfa) - 1):
            sy2 = pdf.sayfa(s2)
            if sy2 and (sy2.tekil_resim or sy2.tablolar):
                isr = sekil_isareti(sy2, s2, yalin)
                if isr:
                    return isr
    if any(c.get("madde") for c in capalar):
        ms = {int(i) for c in capalar for i in (c.get("madde") or []) if 0 <= int(i) < len(sy.maddeler)}
        if ms:
            return {"s": int(sayfa), **eslestir_capa(cumle, sy, ms)}
    for c in capalar:
        if c.get("kutu"):
            return {"s": int(sayfa), "t": "resim", "l": [[round(float(v), 4) for v in c["kutu"]]], "w": []}
        if c.get("resim") is not None and 0 <= int(c["resim"]) < len(sy.resimler):
            return {"s": int(sayfa), "t": "resim", "l": [sy.n(sy.resimler[int(c["resim"])])], "w": []}
    # satir tek dize de yazılmış olabilir (arşiv çapaları): harf harf gezilmesin
    satirlar = [x for c in capalar for x in ([c["satir"]] if isinstance(c.get("satir"), str) else (c.get("satir") or [])) if x]
    ms = capa_maddeleri(sy, satirlar) if satirlar else set()
    if ms:
        return {"s": int(sayfa), **eslestir_capa(cumle, sy, ms)}
    # Çapalı satır eşleşemezse veya madde bulunamazsa doğrudan hedef sayfada tam metin/kelime eşlemesi yap (kurtarma)
    n, r = eslestir(cumle, sy)
    if r and n >= 1:
        return {"s": int(sayfa), **r}
    # şekil çapası yazılmamış ama cümle görseli anlatıyor ya da slayt resimden ibaret: resme git
    if sy.tekil_resim and (GORSEL.search(cumle) or (len(sy.kelimeler) < 15 and not sy.ocr)):
        isr = sekil_isareti(sy, int(sayfa), [{"sekil": cumle}] if TABLO_SOZ.search(cumle) else [{}])
        if isr:
            return isr
    return {"s": int(sayfa), "t": "sayfa", "l": [], "w": []}


def ders_isle(key: str, kuru: bool, zorla: bool = False) -> dict | None:
    hz_yol = KOK / "hizalama" / f"{key}.json"
    if not hz_yol.exists():
        return None
    hz = json.loads(hz_yol.read_text(encoding="utf-8"))
    with urllib.request.urlopen(api_iste(f"{API}/api/canli-ders/{key}"), timeout=30) as r:
        d = json.load(r)
    paras = [p for b in d["bolumler"] for p in b["paragraflar"]]
    if len(paras) != len(hz["paragraflar"]):
        return None
    metin_hash = hashlib.sha1("\n".join(p["metin"] for p in paras).encode("utf-8")).hexdigest()
    capa_yol = KOK / "capa" / f"{key}.json"
    capa_p = None
    if capa_yol.exists():
        cj = json.loads(capa_yol.read_text(encoding="utf-8"))
        md = KOK / "metin" / f"{key}.md"
        if md.exists() and cj.get("mdSha1") == hashlib.sha1(md.read_bytes()).hexdigest() and len(cj.get("p") or []) == len(paras):
            capa_p = cj["p"]
    hiz_hash = hashlib.sha1(hz_yol.read_bytes() + (capa_yol.read_bytes() if capa_p else b"")).hexdigest()
    hedef = CIKTI / f"{key}.json"
    if not zorla and hedef.exists():
        try:
            e = json.loads(hedef.read_text(encoding="utf-8"))
            if e.get("metinHash") == metin_hash and e.get("hizHash") == hiz_hash and e.get("surum") == SURUM:
                return {"guncel": True}
        except ValueError:
            pass
    pdfler: list[Pdf | None] = []
    for fi, f in enumerate(hz["dosyalar"]):
        yol = INDIR / f["path"]
        if str(f.get("path", "")).startswith("Son Prova/"):  # Son Prova özet PDF'i (scripts/son_prova/pdf_kirp.mjs)
            yol = MEDS / "data" / "son_prova" / "pdf" / Path(f["path"]).name
        if not yol.exists() and os.environ.get("HIZALA_PDF_DIZIN"):
            ek = f"_{fi}" if fi else ""
            yol = Path(os.environ["HIZALA_PDF_DIZIN"]) / f"{hz['deckId']}{ek}.pdf"
        if not yol.exists():
            yol = pdf_indir(hz["deckId"], f, fi)
        pdfler.append(Pdf(yol) if yol and yol.exists() else None)
    if not any(pdfler):
        return None
    say = {"metin": 0, "tablo": 0, "kelime": 0, "resim": 0, "sayfa": 0, "yok": 0, "capa": 0}
    c_out: dict[str, list] = {}
    for pn, (p, es) in enumerate(zip(paras, hz["paragraflar"])):
        m = p["metin"]
        sinir = cumle_sonlari(m)
        cc = cumle_capalari(m, sinir, capa_p[pn]) if capa_p else None
        liste = []
        for ci, e in enumerate(sinir):
            cumle = m[(sinir[ci - 1] if ci else 0):e]
            if cc and cc[ci] and es:
                cd = next((int(c["dosya"]) for c in cc[ci] if c.get("dosya") is not None), es.get("dosya", 0))
                isr = capali(cumle, cc[ci], pdfler[cd] if cd < len(pdfler) else None)
                if isr:
                    isr["d"] = cd
                    say[isr["t"]] += 1
                    say["capa"] += 1
                    liste.append(isr)
                    continue
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
            # komşu slaytlar: uzaklaştıkça daha güçlü kanıt (±1: 3 kelime, ±2–3: 4 kelime ve atanan sayfanın 1,5 katı)
            for s in (s0, s0 - 1, s0 + 1, s0 + 2, s0 - 2, s0 + 3, s0 - 3):
                sy = pdf.sayfa(s)
                if not sy:
                    continue
                n, r = eslestir(cumle, sy)
                uz = abs(s - s0)
                esik = 0 if not uz else max(3 if uz == 1 else 4, en[0] * 1.5)
                if r and n >= max(1, esik) and (en[1] is None or n > en[0]):
                    en = (n, r, s)
            n, r, s = en
            if r:
                isr = {"d": d0, "s": s, **r}
            else:
                sy = pdf.sayfa(s0)
                # Lazer yalnız görsel anlatılırken: cümle görselden söz ediyor ya da slayt neredeyse yalnız resim.
                # Bağlam/geçiş cümlesinde resme lazer yanıltır → yalnız sayfa vurgusu.
                if sy and sy.resimler and (GORSEL.search(cumle) or (len(sy.kelimeler) < 15 and not sy.ocr)):
                    rb = max(sy.resimler, key=lambda b: (b[2] - b[0]) * (b[3] - b[1]))
                    isr = {"d": d0, "s": s0, "t": "resim", "l": [sy.n(rb)], "w": []}
                else:
                    isr = {"d": d0, "s": s0, "t": "sayfa", "l": [], "w": []}
            say[isr["t"]] += 1
            liste.append(isr)
        c_out[str(p["i"])] = liste
    toplam = sum(v for k, v in say.items() if k != "capa") or 1
    say.pop("capa") if not say["capa"] else None
    kapsama = (say["metin"] + say["tablo"] + say["kelime"] + say["resim"]) / toplam
    sonuc = {"surum": SURUM, "metinHash": metin_hash, "hizHash": hiz_hash, "c": c_out}
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
    ap.add_argument("--zorla", action="store_true", help="güncel olanları da yeniden üret")
    a = ap.parse_args()
    keys = a.key or sorted(p.stem for p in (KOK / "hizalama").glob("*.json"))
    kotu = 0
    for key in keys:
        try:
            r = ders_isle(key, a.kuru, a.zorla)
        except Exception as e:  # tek ders hatası diğerlerini durdurmasın
            print(f"{key}: HATA {e}")
            kotu += 1
            continue
        if r and r.get("guncel"):
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
