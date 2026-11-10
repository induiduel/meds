#!/usr/bin/env python3
"""Ek modül "PDF ile dinle" kipi: sesli ders kliplerini ders kitapçığı PDF'ine bağlar.

Her ders klibi (d-<konu>-<n>: bölüm başlığı + `ses` cümleleri) için üç şey çıkarılır:
  1. Bölümün kitapçıktaki yeri: sayfa + bölüm kutusu + not satırlarının kutuları (PDF metninden; sayfa oranı 0–1).
  2. Cümle zamanı: klipteki her cümlenin başladığı saniye. Tahmin karakter oranıdır; sınır, tahminin çevresindeki en uzun
     duraklamaya oturtulur (scripts/sesli_anlatim/cumle_zaman.py ile aynı yöntem, yalnız CPU, LLM yok).
  3. Cümle → not maddesi: konuşma cümlesi, aynı bölümün ekran notundaki maddelerle sözcük köküyle eşlenir (not okunuşa
     çevrilip karşılaştırılır: "21 Mart" ↔ "yirmi bir Mart"). Eşiği geçmeyen cümleye madde UYDURULMAZ: o cümlede yalnız
     bölüm çerçevesi görünür.

Çıktı: src/data/ek_moduller/<modül>/pdf_esle.json
  { "pdf": "<index.json'daki ders kitapçığı>", "bayt": n,
    "klip": { "d-1a-1": { "s": sayfa, "k": [x0,y0,x1,y1], "l": [[kutu…] madde başına], "c": [[saniye, madde|-1], …] } } }
  c[0] başlığın okunduğu cümledir (madde 0 = başlık satırı). Kitapçık ya da ses yeniden üretilirse betik yeniden çalıştırılır;
  doğrulayıcı (dogrula.py) klip özetinin (`v`) eşleme anındakiyle aynı olduğunu denetler.

Kullanım (çalışma dizini meds/; PyMuPDF .venv-ocr'da):
  .venv-ocr/bin/python scripts/ek_modul/pdf_esle.py --modul yuruyus-kampcilik [--kuru]
"""
from __future__ import annotations
import json, math, re, sys
from collections import Counter
from pathlib import Path

import numpy as np

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "scripts/ek_modul"))
sys.path.insert(0, str(KOK / "scripts/sesli_anlatim"))
import ses as S  # noqa: E402  (oku, nokta: klip metni ses.py ile birebir aynı kurulur)
import cumle_zaman as Z  # noqa: E402

ESIK = 0.34  # cümle–madde benzerliği bunun altındaysa eşleme yazılmaz
DUR = set("ve ile bir bu da de için gibi daha çok en ise ama yani ya ki mi mı mu mü o şu ne her hem değil olan olarak "
          "sen senin seni sana onu ona bunu buna ile birlikte kadar göre sonra önce yalnız bile hiç evet".split())


def katla(s: str) -> str:
    return s.replace("I", "ı").replace("İ", "i").lower()


def duz(s: str) -> str:
    """Karşılaştırma için: harf/rakam dışı her şey atılır (PDF metninde boşluk ve tire yerleri değişebilir)."""
    return re.sub(r"[^0-9a-zçğıöşüâîû]", "", katla(s))


def kokler(s: str) -> list[str]:
    return [w[:5] for w in re.findall(r"[a-zçğıöşüâîû]+", katla(s)) if w not in DUR and len(w) > 1]


def ekran_maddeleri(ekran: str) -> list[str]:
    """Ekran notunun PDF'e basılan parçaları, sırayla: giriş cümlesi, maddeler, vurgu satırı (biçim imleri atılmış)."""
    out = []
    for s in (x.strip() for x in ekran.split("\n")):
        if not s:
            continue
        s = re.sub(r"^>\s*(\[!(IMPORTANT|NOTE)\])?\s*", "", s)
        s = re.sub(r"^-\s+", "", s).replace("**", "")
        out.append(s)
    return out


def pdf_satirlari(yol: Path):
    import pymupdf
    belge = pymupdf.open(yol)
    satir = []  # (sayfa, [x0,y0,x1,y1] oran, metin)
    for no, sayfa in enumerate(belge, 1):
        w, h = sayfa.rect.width, sayfa.rect.height
        for b in sayfa.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                t = "".join(sp["text"] for sp in l["spans"])
                if t.strip():
                    x0, y0, x1, y1 = l["bbox"]
                    satir.append((no, [round(x0 / w, 4), round(y0 / h, 4), round(x1 / w, 4), round(y1 / h, 4)], t))
    # PDF metni okuma sırasıyla gelmez (madde listeleri bloğun sonuna düşer): sayfa içinde yukarıdan aşağı, soldan sağa
    satir.sort(key=lambda s: (s[0], round((s[1][1] + s[1][3]) / 2, 3), s[1][0]))
    return satir


def bolum_bul(satir, i0: int, baslik: str, maddeler: list[str]):
    """i0'dan başlayarak bölüm başlığını ve altındaki madde satırlarını bulur → (sonraki dizin, sayfa, [başlık kutuları, madde kutuları…])."""
    hedef = duz(baslik)
    for i in range(i0, len(satir)):
        # başlık satırı "<sıra><başlık>"; uzun başlık iki satıra bölünebilir
        t, j = duz(satir[i][2]), i
        if not (t and t[0].isdigit() and hedef.startswith(t[1:]) and len(t) > 1):
            continue
        t = t[1:]
        while t != hedef and j + 1 < len(satir) and hedef.startswith(t + duz(satir[j + 1][2])):
            j += 1
            t += duz(satir[j][2])
        if t != hedef:
            continue
        sayfa = satir[i][0]
        kutular = [[s[1] for s in satir[i:j + 1]]]
        j += 1
        for m in maddeler:
            h, t, bas = duz(m), "", j
            while j < len(satir) and satir[j][0] == sayfa and t != h and h.startswith(t + duz(satir[j][2])):
                t += duz(satir[j][2])
                j += 1
            if t != h:
                raise SystemExit(f"HATA: PDF'te madde bulunamadı (s. {sayfa}, «{baslik}»): {m[:70]}")
            kutular.append([s[1] for s in satir[bas:j]])
        return j, sayfa, kutular
    raise SystemExit(f"HATA: PDF'te bölüm başlığı bulunamadı: {baslik}")


def cumle_zamanlari(mp3: Path, cumleler: list[str]) -> tuple[list[float], float, int]:
    """Her cümlenin başladığı saniye ([0, t1, …]), klip süresi, duraklamaya oturan sınır sayısı."""
    en = Z.enerji(Z.coz(mp3))
    sure = len(en) / 100.0
    dolu = en[en > 0]
    # EMA paragraf içindeki cümle sonunda yalnız 0,2–0,3 sn durur ve taban tam sessiz değildir: eşik cumle_zaman'dakinden
    # yüksek tutulur (konuşma düzeyinin ~-24 dB altı), yoksa paragraf içi sınırlar duraklama olarak görülmez
    esik = max(float(np.percentile(dolu, 90)) * 0.06, 1.0)
    sess = Z.sessizlikler(en, esik)
    orta = np.array([(a + b) / 2 for a, b in sess]) / 100.0
    uzun = np.array([(b - a) for a, b in sess]) / 100.0
    # Tahmin KONUŞULAN süre üzerinden (duraklamalar sayılmaz): klip paragraf aralarında uzun nefes payı taşır, düz karakter
    # oranı bu yüzden kayıyordu. Sonra bütün sınırlar BİRLİKTE yerleştirilir (sıra korunur): en uzun duraklamalar + tahmine
    # yakınlık. Tek tek seçimde bir sınır komşusunun duraklamasını kapıp iki cümleyi üst üste bindiriyordu.
    sesli = np.cumsum(en >= esik) / 100.0
    L = sum(len(c) for c in cumleler)
    tahmin, konum = [], 0
    for c in cumleler[:-1]:
        konum += len(c)
        tahmin.append(float(np.searchsorted(sesli, sesli[-1] * konum / L)) / 100.0)
    # baştaki ve sondaki sessizlik cümle sınırı değildir (klip sonunda uzun nefes payı var: son sınırı kapıyordu)
    aday = [k for k, (x, y) in enumerate(sess) if uzun[k] >= 0.12 and x > 5 and y < len(en) - 5]
    n = len(tahmin)
    from functools import lru_cache
    sys.setrecursionlimit(10000)

    @lru_cache(maxsize=None)
    def en_iyi(j: int, a: int) -> tuple[float, tuple[int, ...]]:
        """j. sınırdan itibaren, a. adaydan başlayarak en yüksek puan ve seçilen adaylar (-1: duraklama bulunamadı)."""
        if j == n:
            return 0.0, ()
        p, sec = en_iyi(j + 1, a)
        en_p, en_sec = p - 1.0, (-1, *sec)
        for x in range(a, len(aday)):
            k = aday[x]
            if abs(orta[k] - tahmin[j]) > 6:
                continue
            p, sec = en_iyi(j + 1, x + 1)
            p += min(uzun[k], 0.6) - abs(orta[k] - tahmin[j]) * 0.8
            if p > en_p:
                en_p, en_sec = p, (k, *sec)
        return en_p, en_sec

    t, oturan = [0.0], 0
    for j, k in enumerate(en_iyi(0, 0)[1]):
        if k >= 0:
            oturan += 1
            t.append(round(sess[k][1] / 100.0 - 0.05, 2))  # duraklamanın bittiği an: cümle konuşmayla birlikte yanar
        else:
            t.append(round(max(tahmin[j], t[-1] + 0.2), 2))
    for j in range(1, len(t)):  # duraklaması bulunamayan sınır komşusunu geçmesin
        t[j] = max(t[j], round(t[j - 1] + 0.2, 2))
    return t, round(sure, 2), oturan


def esle(cumleler: list[str], maddeler: list[str], idf: dict[str, float]) -> list[int]:
    """Her konuşma cümlesi için en benzeyen not maddesinin sırası (1 tabanlı; 0 başlık satırıdır) ya da -1."""
    mk = [Counter(kokler(S.oku(m))) for m in maddeler]
    out = []
    for c in cumleler:
        ck = set(kokler(c))
        top = sum(idf.get(k, 1.0) for k in ck) or 1.0
        puan = [sum(idf.get(k, 1.0) for k in ck if k in m) / top for m in mk]
        en = int(np.argmax(puan)) if puan else -1
        out.append(en + 1 if en >= 0 and puan[en] >= ESIK else -1)
    return out


def main() -> int:
    a = sys.argv[1:]
    modul = a[a.index("--modul") + 1]
    veri = KOK / "src/data/ek_moduller" / modul
    ozet = next(m for m in json.loads((veri.parent / "index.json").read_text())["moduller"] if m["id"] == modul)
    pdf = next((p["dosya"] for p in ozet["pdf"] if p["id"] == "ders"), None)
    if not pdf:
        raise SystemExit("HATA: index.json'da ders kitapçığı (pdf id 'ders') yok")
    pdf_yol = KOK / "public/ek_moduller" / modul / pdf
    klip = json.loads((veri / "klip.json").read_text())
    ses_kok = KOK / "data/ek_moduller/ses" / modul
    satir = pdf_satirlari(pdf_yol)
    konular = [k for f in sorted(veri.glob("b*.json"), key=lambda f: int(f.stem[1:])) for k in json.loads(f.read_text())["konular"]]
    # kök ağırlığı: modülün bütün not maddelerinde seyrek geçen kök daha ayırt edicidir
    tum = [ekran_maddeleri(b["ekran"]) for k in konular for b in k["bolumler"]]
    df = Counter(kk for ms in tum for m in ms for kk in set(kokler(S.oku(m))))
    n = sum(len(ms) for ms in tum)
    idf = {k: math.log(1 + n / v) for k, v in df.items()}

    out, i, cumle_n, esli, oturan_n, sinir_n, eksik = {}, 0, 0, 0, 0, 0, []
    for k in konular:
        for bi, b in enumerate(k["bolumler"], 1):
            ad = f"d-{k['id']}-{bi}"
            maddeler = ekran_maddeleri(b["ekran"])
            i, sayfa, kutular = bolum_bul(satir, i, b["baslik"], maddeler)
            duz_k = [x for ks in kutular for x in ks]
            kutu = [min(x[0] for x in duz_k), min(x[1] for x in duz_k), max(x[2] for x in duz_k), max(x[3] for x in duz_k)]
            mp3 = ses_kok / f"{ad}.mp3"
            if ad not in klip or not mp3.exists():
                eksik.append(ad)
                continue
            cumleler = [S.nokta(S.oku(b["baslik"]))] + b["ses"]
            t, sure, oturan = cumle_zamanlari(mp3, cumleler)
            m = [0] + esle(b["ses"], maddeler, idf)
            cumle_n += len(b["ses"])
            esli += sum(1 for x in m[1:] if x > 0)
            oturan_n += oturan
            sinir_n += len(cumleler) - 1
            out[ad] = {"v": klip[ad]["v"], "s": sayfa, "k": kutu, "l": kutular, "c": [[tj, mj] for tj, mj in zip(t, m)]}
            if "--goster" in a:
                for cj, (tj, mj) in zip(cumleler, zip(t, m)):
                    print(f"  {ad} {tj:6.2f} → {'—' if mj < 0 else ('başlık' if mj == 0 else maddeler[mj - 1][:48])} | {cj[:60]}")
    print(f"{modul}: {len(out)} klip eşlendi, {cumle_n} cümlenin {esli}'i ({esli * 100 // max(1, cumle_n)}%) not maddesine bağlandı, "
          f"{oturan_n}/{sinir_n} cümle sınırı duraklamaya oturdu" + (f"; sesi olmayan {len(eksik)} klip atlandı: {eksik[:5]}" if eksik else ""))
    if "--kuru" not in a:
        (veri / "pdf_esle.json").write_text(json.dumps({"pdf": pdf, "bayt": pdf_yol.stat().st_size, "klip": out}, ensure_ascii=False, separators=(",", ":")))
        print(f"yazıldı: {veri / 'pdf_esle.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
