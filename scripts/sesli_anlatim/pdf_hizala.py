#!/usr/bin/env python3
"""Sesli anlatım paragraflarını ders PDF sayfalarına hizalar (Canlı ders sayfası için).

Kaynaklar:
  - konuşma metni   data/sesli_anlatim/metin/<key>.md (paragraflar sesliAnlatim.ts::metinParagraflari ile aynı)
  - PDF listesi     src/data/deckPdfSources.json → decks[k1p-<key>-v2 | k1p-<key>].files (v2 dosyaları varsa onlar)
  - sayfa metni     ../meds_temp/temp2/drive_root/<path .md> (## Sayfa N); yoksa pdftotext (meds_downloads)

Yöntem: Türkçe katlama + 5 harf kök + TF-IDF kosinüs (sayı ve ≤3 harfli parçalar atılır: konuşmada kısaltmalar
okunuşla yazılı). Sıra korumalı dinamik programlama: ileri atlama ucuz, aynı sayfada kalma serbest, geri dönüş
cezalı (küçük geri dönüş az, büyük çok). Benzerliği düşük paragraf bir önceki paragrafın sayfasını devralır.

Çıktı: data/sesli_anlatim/hizalama/<key>.json
  { deckId, dosyalar:[{path,name,fileId,pages}], paragraflar:[{dosya,sayfa,guven}] }   (dizin = global paragraf sırası)
PDF'i olmayan derste dosya yazılmaz (eskisi varsa silinmez).

Kullanım: pdf_hizala.py --hepsi | --key <key> [--goster N]   (--goster: N örnek paragrafı sayfa metniyle yazdırır)
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import subprocess
import sys
import unicodedata
from collections import Counter
from pathlib import Path

import numpy as np

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")

MEDS = Path(__file__).resolve().parents[2]
ROOT = MEDS.parent
KOK = MEDS / "data" / "sesli_anlatim"
CIKTI = KOK / "hizalama"
TEMP2 = ROOT / "meds_temp" / "temp2" / "drive_root"
INDIR = ROOT / "meds_downloads" / "drive_root"

DUSUK_GUVEN = 0.05  # bu kosinüsün altı: önceki sayfayı devral
GUVEN_TAVAN = 0.30  # guven = min(1, kosinüs / GUVEN_TAVAN)
GERI_CEZA = 0.06  # geri dönüş sabit cezası
GERI_SAYFA = 0.015  # geri dönülen her sayfa için ek ceza
ILERI_SAYFA = 0.0015  # ileri atlanan her sayfa için çok küçük ceza (uzak sıçramaları hafifçe caydırır)
DOSYA_GECIS = 0.02  # dosyalar arası geçiş (çok dosyalı derste)
# Cümle düzeyi (dp_cumle)
C_ILERI = 0.05  # bir sonraki slayta geçiş için gereken en az kanıt
C_ILERI_SAYFA = 0.02  # atlanan her ek slayt
C_GERI = 0.16  # önceki slayta dönüş
C_GERI_SAYFA = 0.03
CUMLE_ILERI = 4  # paragrafın sayfasından en çok kaç slayt ileri cümle kayabilir (çapa dışı cezalı)
CAPA_CEZA = 0.08

STOP = set(
    """
    için gibi daha olan olarak veya ancak hem kadar sonra önce ise yani ayrıca çünkü bunun şunu bunu buna şimdi
    burada şöyle böyle diye değil değildir olur olup olduğu olduğunu oluşur olması olan olabilir birlikte arasında
    üzerinde içinde dikkat edin edelim bakalım geçelim sınavda klasik tuzak önemli özellikle genellikle bazen
    birinci ikinci üçüncü dördüncü beşinci altıncı yedinci sekizinci dokuzuncu onuncu özetle kısaca bağlı ilgili
    """.split()
)


def katla(t: str) -> str:
    t = t.replace("İ", "i").replace("I", "ı").lower().replace("ı", "i")
    t = unicodedata.normalize("NFKD", t)
    return "".join(c for c in t if not unicodedata.combining(c))


STOP_K = {katla(w) for w in STOP}


def kokler(t: str) -> list[str]:
    out = []
    t = unicodedata.normalize("NFKC", t)  # slayttaki alt simgeler: LTB₄ → LTB4
    # Kısaltmalar (DNA, HER2, CD4) ve en az iki haneli sayılar (1960, 46) slaytta da aynı yazılır: bütün hâliyle tutulur
    for m in re.finditer(r"\b(?:[A-ZÇĞİÖŞÜ][A-ZÇĞİÖŞÜa-z]?[A-ZÇĞİÖŞÜ0-9]{1,5}|\d{2,4})\b", t):
        w = m.group(0)
        if sum(c.isupper() or c.isdigit() for c in w) >= 2:
            out.append("#" + katla(w))
    for w in re.findall(r"[a-z]+", katla(t)):
        if len(w) < 4 or w in STOP_K:
            continue
        out.append(w[:5])
    return out


def cumle_sinirlari(p: str) -> list[int]:
    """Cümle bitiş konumları — canliDersStore.ts::cumleSinirlari ile BİREBİR aynı kural.
    Sınır: [.!?…]+ (+ kapanan tırnak/parantez) ardından boşluk ya da metin sonu; sonraki karakter küçük harfse
    sınır sayılmaz ("2. basamak", "1.'si", "3,5" bölünmez)."""
    out: list[int] = []
    for m in re.finditer(r"[.!?…]+[\"'”’)\]]*(?:\s+|$)", p):
        e = m.end()
        if e < len(p) and p[e].islower():
            continue
        if e > (out[-1] if out else 0):
            out.append(e)
    if not out or out[-1] < len(p):
        out.append(len(p))
    return out


def cumleler(p: str) -> list[str]:
    s = cumle_sinirlari(p)
    return [p[(s[k - 1] if k else 0):s[k]] for k in range(len(s))]


def _nfc(x: str) -> str:
    return unicodedata.normalize("NFC", x).casefold()


_MD: dict[str, Path] = {}
if TEMP2.exists():
    for _p in TEMP2.rglob("*.md"):
        _MD[_nfc(str(_p.relative_to(TEMP2)))] = _p


def md_bul(rel: str) -> Path | None:
    """kit_hazirla.py::md_bul — NFC/NFD farkı gözetmeden; temp2 adı noktada kesilmişse önek eşleşmesi."""
    hit = _MD.get(_nfc(rel.rsplit(".", 1)[0] + ".md"))
    if hit:
        return hit
    hedef = _nfc(rel.rsplit(".", 1)[0])
    aday = [(k, v) for k, v in _MD.items() if hedef.startswith(k[:-3]) and len(k[:-3]) >= len(hedef) * 0.6]
    return max(aday, key=lambda kv: len(kv[0]))[1] if aday else None


def sayfalar_md(p: Path) -> dict[int, str]:
    out: dict[int, str] = {}
    cur = None
    buf: list[str] = []
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.match(r"^##\s+Sayfa\s+(\d+)", line)
        if m:
            if cur is not None:
                out[cur] = "\n".join(buf)
            cur, buf = int(m.group(1)), []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        out[cur] = "\n".join(buf)
    return out


def sayfalar_pdf(rel: str) -> dict[int, str] | None:
    pdf = INDIR / rel
    if not pdf.exists():
        cands = [q for q in pdf.parent.glob("*.pdf") if _nfc(q.name) == _nfc(pdf.name)] if pdf.parent.exists() else []
        if not cands:
            return None
        pdf = cands[0]
    try:
        t = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True, timeout=180).stdout
    except Exception:
        return None
    return {i: x for i, x in enumerate(t.split("\f"), 1) if x.strip()}


def metin_paragraflari(md: str) -> list[str]:
    """sesliAnlatim.ts::metinParagraflari ile aynı paragraf ayrımı (yalnız metin)."""
    out: list[str] = []
    tampon: list[str] = []

    def bitir():
        nonlocal tampon
        t = re.sub(r"\s+", " ", " ".join(tampon)).strip()
        if t:
            out.append(t)
        tampon = []

    for s in re.split(r"\r?\n", md):
        if s.startswith("# "):
            continue
        if s.startswith("@@"):
            bitir()
            continue
        if not s.strip():
            bitir()
        else:
            tampon.append(s.strip())
    bitir()
    return out


def tfidf(belgeler: list[list[str]], idf_kaynak: list[list[str]]) -> tuple[np.ndarray, dict[str, int]]:
    df = Counter()
    for b in idf_kaynak:
        df.update(set(b))
    sozluk = {w: i for i, w in enumerate(sorted(df))}
    n = len(idf_kaynak)
    idf = np.zeros(len(sozluk))
    for w, i in sozluk.items():
        idf[i] = math.log((1 + n) / (1 + df[w])) + 1
    M = np.zeros((len(belgeler), len(sozluk)))
    for r, b in enumerate(belgeler):
        for w, c in Counter(b).items():
            j = sozluk.get(w)
            if j is not None:
                M[r, j] = (1 + math.log(c)) * idf[j]
    nr = np.linalg.norm(M, axis=1, keepdims=True)
    nr[nr == 0] = 1
    return M / nr, sozluk


def dp_hizala(S: np.ndarray, dosya_of: np.ndarray, sira_of: np.ndarray) -> list[int]:
    """S[i, j]: paragraf i ↔ sayfa j kosinüsü. Sıra korumalı en iyi yol (Viterbi)."""
    n, m = S.shape
    # geçiş cezası T[j_prev, j]
    jp = np.arange(m)[:, None]
    jn = np.arange(m)[None, :]
    fark = (sira_of[jn] - sira_of[jp]).astype(float)
    ayni_dosya = dosya_of[jp] == dosya_of[jn]
    T = np.where(fark >= 0, fark * ILERI_SAYFA, GERI_CEZA + (-fark) * GERI_SAYFA)
    T = np.where(ayni_dosya, T, DOSYA_GECIS + np.abs(fark) * ILERI_SAYFA)
    np.fill_diagonal(T, 0.0)
    skor = S[0].copy()
    geri = np.zeros((n, m), dtype=np.int32)
    for i in range(1, n):
        aday = skor[:, None] - T  # [prev, cur]
        geri[i] = aday.argmax(axis=0)
        skor = aday.max(axis=0) + S[i]
    yol = [int(skor.argmax())]
    for i in range(n - 1, 0, -1):
        yol.append(int(geri[i, yol[-1]]))
    return yol[::-1]


def dp_cumle(S: np.ndarray, dosya_of: np.ndarray, sira_of: np.ndarray) -> list[int]:
    """Cümle düzeyi Viterbi: sayfada kalmak bedava; ileri geçiş için kanıt gerekir (sabit + sayfa başına ceza);
    geri dönüş pahalı (anlatıcı nadiren önceki slayta döner)."""
    n, m = S.shape
    jp = np.arange(m)[:, None]
    jn = np.arange(m)[None, :]
    fark = (sira_of[jn] - sira_of[jp]).astype(float)
    T = np.where(fark > 0, C_ILERI + (fark - 1) * C_ILERI_SAYFA, C_GERI + (-fark) * C_GERI_SAYFA)
    T = np.where(dosya_of[jp] == dosya_of[jn], T, T + DOSYA_GECIS)
    np.fill_diagonal(T, 0.0)
    skor = S[0].copy()
    geri = np.zeros((n, m), dtype=np.int32)
    for i in range(1, n):
        aday = skor[:, None] - T
        geri[i] = aday.argmax(axis=0)
        skor = aday.max(axis=0) + S[i]
    yol = [int(skor.argmax())]
    for i in range(n - 1, 0, -1):
        yol.append(int(geri[i, yol[-1]]))
    return yol[::-1]


def deste_sec(pdfsrc: dict, key: str) -> tuple[str, list[dict]] | None:
    for did in (f"k1p-{key}-v2", f"k1p-{key}"):
        files = (pdfsrc.get(did) or {}).get("files") or []
        if files:
            return did, files
    return None


def hizala(key: str, pdfsrc: dict, goster: int = 0) -> dict | None:
    mdp = KOK / "metin" / f"{key}.md"
    if not mdp.exists():
        return None
    sec = deste_sec(pdfsrc, key)
    if not sec:
        # deckPdfSources'ta dosya listesi yoksa (ders işçisinin yazdığı hizalama) mevcut dosyadaki PDF yolları kullanılır
        try:
            eski = json.loads((CIKTI / f"{key}.json").read_text(encoding="utf-8"))
            sec = (eski["deckId"], [d for d in eski.get("dosyalar") or [] if d.get("path")]) if eski.get("dosyalar") else None
        except Exception:
            sec = None
    if not sec:
        return None
    did, files = sec
    paragraflar = metin_paragraflari(mdp.read_text(encoding="utf-8"))
    sayfa_list: list[tuple[int, int, str]] = []  # (dosya, sayfa, metin)
    dosyalar = []
    for fi, f in enumerate(files):
        md = md_bul(f["path"])
        sy = sayfalar_md(md) if md else None
        if not sy:
            sy = sayfalar_pdf(f["path"]) or {}
        if not sy and os.environ.get("HIZALA_PDF_DIZIN"):
            # yerelde olmayan PDF (ör. Oracle'dan indirilmiş): <dizin>/<deckId>[_<sıra>].pdf
            ek = f"_{fi}" if fi else ""
            yerel = Path(os.environ["HIZALA_PDF_DIZIN"]) / f"{did}{ek}.pdf"
            if yerel.exists():
                t = subprocess.run(["pdftotext", "-layout", str(yerel), "-"], capture_output=True, text=True, timeout=180).stdout
                sy = {i: x for i, x in enumerate(t.split("\f"), 1) if x.strip()}
        dosyalar.append({"path": f["path"], "name": f.get("name"), "fileId": f.get("fileId"), "pages": f.get("pages")})
        for no in sorted(sy):
            sayfa_list.append((fi, no, sy[no]))
    if not sayfa_list:
        return None
    sayfa_kok = [kokler(t) for _, _, t in sayfa_list]
    par_kok = [kokler(t) for t in paragraflar]
    # IDF sayfalar + paragraflardan: konuşma metninde her yerde geçen ders adı vb. ağırlık kaybeder
    X, _ = tfidf(sayfa_kok + par_kok, sayfa_kok + par_kok)
    Pm, Sm = X[len(sayfa_kok):], X[: len(sayfa_kok)]
    S = Pm @ Sm.T
    dosya_of = np.array([d for d, _, _ in sayfa_list])
    sira_of = np.arange(len(sayfa_list))
    yol = dp_hizala(S, dosya_of, sira_of)
    sonuc = []
    onceki = None
    for i, j in enumerate(yol):
        if S[i, j] < DUSUK_GUVEN and onceki is not None:
            j = onceki
        onceki = j
        sonuc.append(j)

    # ---- Cümle düzeyi: tüm ders boyunca cümle × sayfa sıra korumalı yol ----
    # Bir paragrafın anlattığı içerik art arda 2-4 slayta yayılabilir; cümleler kendi kanıtıyla sayfa seçer.
    # Kanıt: cümle (+ komşu cümleler yarım ağırlık) ve paragrafın kendisi; paragraf hizası bölge çapası olur.
    cum_par: list[int] = []
    cum_txt: list[str] = []
    for i, p in enumerate(paragraflar):
        for c in cumleler(p):
            cum_par.append(i)
            cum_txt.append(c)
    cum_kok = [kokler(c) for c in cum_txt]
    Xc, _ = tfidf(cum_kok, sayfa_kok + par_kok)
    Sc_tek = Xc @ Sm.T
    n_c = len(cum_txt)
    Sc_kom = Sc_tek.copy()
    for k in range(n_c):
        for d, w in ((-1, 0.5), (1, 0.5), (-2, 0.2), (2, 0.2)):
            q = k + d
            if 0 <= q < n_c and cum_par[q] == cum_par[k]:
                Sc_kom[k] += w * Sc_tek[q]
    # paragraf çapası: paragrafın DP sayfası ve yakın komşuları dışındaki sayfalar hafif cezalı
    capa = np.zeros((n_c, len(sayfa_list)))
    sira = np.arange(len(sayfa_list))
    for k in range(n_c):
        i = cum_par[k]
        j0 = sonuc[i]
        j1 = sonuc[i + 1] if i + 1 < len(sonuc) else j0
        lo, hi = min(j0, j1) - 1, max(j0, j1) + CUMLE_ILERI
        capa[k] = np.where((sira >= lo) & (sira <= hi), 0.0, CAPA_CEZA)
    Sc = 0.55 * Sc_tek + 0.25 * Sc_kom / 1.4 + 0.20 * S[np.array(cum_par)] - capa
    yol_c = dp_cumle(Sc, dosya_of, sira_of)

    paragraflar_out = []
    k = 0
    for i, j in enumerate(sonuc):
        idx = []
        while k < n_c and cum_par[k] == i:
            idx.append(yol_c[k])
            k += 1
        if not idx:
            idx = [j]
        j_ilk = idx[0]
        p_obj = {
            "dosya": int(dosya_of[j_ilk]),
            "sayfa": int(sayfa_list[j_ilk][1]),
            "guven": round(float(min(1.0, S[i, j] / GUVEN_TAVAN)), 2),
            "sayfalar": [int(sayfa_list[x][1]) for x in idx],
        }
        c_dosyalar = [int(dosya_of[x]) for x in idx]
        if any(d != c_dosyalar[0] for d in c_dosyalar) or c_dosyalar[0] != p_obj["dosya"]:
            p_obj["dosyalar"] = c_dosyalar
        paragraflar_out.append(p_obj)
    if goster:
        adim = max(1, len(paragraflar) // goster)
        for i in range(0, len(paragraflar), adim):
            j = sonuc[i]
            top = int(S[i].argmax())
            print(f"\n[{i}] g={S[i, j]:.2f} → dosya {dosya_of[j]} s.{sayfa_list[j][1]} (en iyi tekil: s.{sayfa_list[top][1]} {S[i, top]:.2f})")
            print("   P:", paragraflar[i][:160])
            print("   S:", re.sub(r"\s+", " ", sayfa_list[j][2])[:160])
    return {"deckId": did, "dosyalar": dosyalar, "paragraflar": paragraflar_out, "_S": S, "_yol": sonuc}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--key", action="append")
    g.add_argument("--hepsi", action="store_true")
    ap.add_argument("--goster", type=int, default=0, help="her ders için N örnek paragraf ↔ sayfa yazdır")
    ap.add_argument("--kuru", action="store_true", help="dosya yazma")
    a = ap.parse_args()
    pdfsrc = json.load(open(MEDS / "src/data/deckPdfSources.json", encoding="utf-8"))["decks"]
    keys = a.key or sorted(p.stem for p in (KOK / "metin").glob("k1-*.md"))
    CIKTI.mkdir(parents=True, exist_ok=True)
    yazilan = 0
    pdfsiz = []
    for key in keys:
        if not re.fullmatch(r"k1-\d+-[a-z0-9-]+", key):
            continue
        r = hizala(key, pdfsrc, a.goster)
        if not r:
            pdfsiz.append(key)
            continue
        ps = r["paragraflar"]
        dusuk = sum(1 for p in ps if p["guven"] < DUSUK_GUVEN / GUVEN_TAVAN)
        S, yol = r.pop("_S"), r.pop("_yol")
        tekil = sum(1 for i, j in enumerate(yol) if int(S[i].argmax()) == j)
        geri = sum(1 for i in range(1, len(yol)) if yol[i] < yol[i - 1])
        ort = sum(p["guven"] for p in ps) / len(ps)
        print(
            f"{key}: {r['deckId']} dosya {len(r['dosyalar'])}, paragraf {len(ps)}, ort.güven {ort:.2f}, "
            f"düşük {dusuk}, en-iyi-tekil ile aynı {tekil}/{len(ps)}, geri dönüş {geri}"
        )
        if not a.kuru:
            out = CIKTI / f"{key}.json"
            tmp = out.with_suffix(".json.tmp")
            tmp.write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
            os.replace(tmp, out)
            yazilan += 1
    print(f"ÖZET: yazılan {yazilan}, PDF'siz {len(pdfsiz)}: {', '.join(pdfsiz)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
