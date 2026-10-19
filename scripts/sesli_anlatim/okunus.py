#!/usr/bin/env python3
"""Kısaltma okunuşu düzeltmesi — YALNIZ seslendirme motoruna giden metne uygulanır (EMA Lightning).

Konuşma metinlerinde kısaltmalar harf adlarıyla ayrık yazılı ("de ne a", "ha e er iki", "pe ce er"). Edge/Gemini bunu
doğal okur; EMA ise her heceyi ayrı sözcük gibi (duraklı, sözcük vurgulu) okuyor. Düzeltme: dizi gerçek bir kısaltmaysa
heceler bitişik yazılır → "denea", "haeer iki", "pecer" (Türkçede kısaltma okunuşu: bitişik, son hece vurgulu).

Gerçek kısaltma kararı: hecelerin harfleri (de ne a → DNA) ders kaynaklarında (meds_temp/temp2/drive_root/**/*.md)
büyük harfli bir kısaltma olarak geçmeli ve küçük harfli hâli kaynakta yaygın bir Türkçe sözcük olmamalı ("VE", "DE"
başlık kalıntıları elenir). Böylece "ve de ne a" → "ve denea" (VDNA yok), "ne ... ne de" dokunulmaz.

Metin dosyaları, paragraf sayısı, zamanlama ve PDF hizalaması DEĞİŞMEZ: düzeltme paragraf içinde, sentez anında yapılır.

Kullanım:
  okunus.py --kur            # kisaltmalar.json'u kaynaklardan yeniden üretir
  okunus.py --rapor [N]      # 69 metinde kaç dizi birleşir + örnekler
  okunus.py "metin"          # tek metni düzeltip yazdırır
"""
from __future__ import annotations

import collections
import glob
import json
import re
import sys
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
SOZLUK = MEDS / "data/sesli_anlatim/okunus/kisaltmalar.json"
KAYNAK = MEDS.parent / "meds_temp/temp2/drive_root"

# Türkçe harf adı → harf (konuşma metni yazımı: TALIMAT okunuşla kısaltma)
HARF = {
    "a": "A", "be": "B", "ce": "C", "çe": "Ç", "de": "D", "e": "E", "fe": "F", "ef": "F", "ge": "G", "ha": "H", "he": "H",
    "ı": "I", "i": "I", "i̇": "I", "je": "J", "ka": "K", "ke": "K", "le": "L", "el": "L", "me": "M", "em": "M", "ne": "N",
    "en": "N", "o": "O", "ö": "Ö", "pe": "P", "re": "R", "er": "R", "se": "S", "es": "S", "şe": "Ş", "te": "T", "u": "U",
    "ü": "Ü", "ve": "V", "ye": "Y", "ze": "Z", "iks": "X", "ku": "Q", "kü": "Q",
}
EN_UZUN = 8  # bir kısaltmada en çok hece
SOZ = re.compile(r"[A-Za-zÇĞİÖŞÜçğıöşüİ̇]+(?:['’][A-Za-zçğıöşü]+)?")


def tr_lower(s: str) -> str:
    return s.replace("İ", "i").replace("I", "ı").lower()


def kur() -> set[str]:
    buyuk, kucuk = collections.Counter(), collections.Counter()
    for f in glob.glob(str(KAYNAK / "**/*.md"), recursive=True):
        t = open(f, encoding="utf-8", errors="ignore").read()
        for w in re.findall(r"[A-Za-zÇĞİÖŞÜçğıöşü]+", t):
            if 2 <= len(w) <= 8 and sum(c.isupper() for c in w) >= 2:
                buyuk[w.upper().replace("İ", "I")] += 1
            if w.islower():
                kucuk[w] += 1
    # küçük harfli hâli kaynakta sözcük olarak geçiyorsa (ve, de, ne, en, el, on…) kısaltma sayılmaz
    # iki harfli kısaltmanın küçük harfli hâli kaynakta sözcük olarak geçiyorsa (ve, de, ne, en, el, on…) kısaltma sayılmaz;
    # daha uzunlarda hece dizisi zaten sözcükle karışmaz (ANA ≠ "a en a")
    kume = sorted(k for k in buyuk if len(k) > 2 or (kucuk[tr_lower(k)] < 3 and kucuk[k.lower()] < 3))
    SOZLUK.parent.mkdir(parents=True, exist_ok=True)
    SOZLUK.write_text(json.dumps(kume, ensure_ascii=False, indent=0), encoding="utf-8")
    return set(kume)


_KUME: set[str] | None = None


def kume() -> set[str]:
    global _KUME
    if _KUME is None:
        _KUME = set(json.loads(SOZLUK.read_text(encoding="utf-8"))) if SOZLUK.exists() else set()
    return _KUME


# Kesme işaretsiz çekim ekleri (son hecede): "a ce te haya", "ha pe vedir", "a pe ceyi"
EKLER = sorted({"ya", "ye", "yı", "yi", "yu", "yü", "nın", "nin", "nun", "nün", "da", "de", "ta", "te", "dan", "den", "tan",
                "ten", "dır", "dir", "dur", "dür", "tır", "tir", "lar", "ler", "yla", "yle", "sı", "si", "ları", "leri", "nda",
                "nde", "ndan", "nden", "yı", "yi", "nı", "ni", "ydı", "ydi"}, key=len, reverse=True)
SAYI = {"bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz", "on", "yirmi", "otuz", "kırk", "elli", "altmış",
        "yetmiş", "seksen", "doksan", "yüz", "bin"}  # sayı sözcükleri hece+ek diye ayrıştırılmaz ("pe elli üç")
BAGLAC = {"ve", "de", "ne"}  # dizinin başında gerçek bağlaç olabilir


def _hece_ek(w: str, son: bool):
    """Sözcük → (hece, ek) ya da None. Ek yalnız dizinin son sözcüğünde (kesmeli ya da kesmesiz) kabul edilir."""
    h = tr_lower(w)
    ek = ""
    if "'" in h or "’" in h:
        if not son:
            return None
        h, e = re.split(r"['’]", h, maxsplit=1)
        ek = "'" + e
    if h in HARF:
        return h, ek
    if son and not ek and h not in SAYI:
        for e in EKLER:
            if h.endswith(e) and h[: -len(e)] in HARF:
                return h[: -len(e)], e
    return None


def _en_iyi(metin: str, eslesme: list, i: int, K: set):
    """i'den başlayan en uzun geçerli kısaltma dizisi: (j, heceler, ek) ya da None."""
    for j in range(min(len(eslesme), i + EN_UZUN), i + 1, -1):
        parca = eslesme[i:j]
        if any(metin[parca[k].end():parca[k + 1].start()].strip() for k in range(len(parca) - 1)):
            continue
        cozum = [_hece_ek(m.group(0), k == len(parca) - 1) for k, m in enumerate(parca)]
        if any(c is None for c in cozum):
            continue
        heceler = [c[0] for c in cozum]
        if "ve" in heceler[1:-1]:  # ortada "ve" = bağlaç (PI3K ve AKT)
            continue
        if len(heceler) == 2 and heceler[-1] == "ve":  # "ge ve ig em", "te ve be"
            continue
        if "".join(HARF[h] for h in heceler) in K:
            return j, heceler, cozum[-1][1]
    return None


FONETIK_TTS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"\bBCG(['’][a-zçğıöşü]+)?\b", re.IGNORECASE), "becege"),
    (re.compile(r"\bDNA(['’][a-zçğıöşü]+)?\b"), "denea"),
    (re.compile(r"\bmRNA(['’][a-zçğıöşü]+)?\b"), "me renea"),
    (re.compile(r"\btRNA(['’][a-zçğıöşü]+)?\b"), "te renea"),
    (re.compile(r"\bRNA(['’][a-zçğıöşü]+)?\b"), "renea"),
    (re.compile(r"\bHPV(['’][a-zçğıöşü]+)?\b"), "hapeve"),
    (re.compile(r"\bHIV(['’][a-zçğıöşü]+)?\b"), "haive"),
    (re.compile(r"\bHSV(['’][a-zçğıöşü]+)?\b"), "haseve"),
    (re.compile(r"\bEBV(['’][a-zçğıöşü]+)?\b"), "ebeve"),
    (re.compile(r"\bATP(['’][a-zçğıöşü]+)?\b"), "atepe"),
    (re.compile(r"\bAFP(['’][a-zçğıöşü]+)?\b"), "afepe"),
    (re.compile(r"\b(?:hCG|HCG)(['’][a-zçğıöşü]+)?\b"), "hacege"),
    (re.compile(r"\bCDK([0-9/]+)?\b"), "cedeka"),
    (re.compile(r"\bCIN\b"), "ceine"),
    (re.compile(r"\bTP53\b"), "tepe elli üç"),
    (re.compile(r"\bBRCA1\b"), "bercea bir"),
    (re.compile(r"\bBRCA2\b"), "bercea iki"),
    (re.compile(r"\bCD4\b"), "cede dört"),
    (re.compile(r"\bCD8\b"), "cede sekiz"),
    (re.compile(r"\bCD10\b"), "cede on"),
    (re.compile(r"\bCD20\b"), "cede yirmi"),
    (re.compile(r"\bCD30\b"), "cede otuz"),
    (re.compile(r"\bCD80\b"), "cede seksen"),
    (re.compile(r"\bCharles\b"), "Çarls"),
    (re.compile(r"\bWinslow\b"), "Vinslo"),
    (re.compile(r"\bJenner\b"), "Cenır"),
    (re.compile(r"\bVon Behring\b", re.IGNORECASE), "Fon Bering"),
    (re.compile(r"\bCalmette\b"), "Kalmet"),
    (re.compile(r"\bGuérin\b"), "Geren"),
    (re.compile(r"\bVirchow\b"), "Virşov"),
    (re.compile(r"\bLouis Pasteur\b"), "Lui Pastör"),
    (re.compile(r"\bJames Lind\b"), "Ceyms Lind"),
    (re.compile(r"\bNeisseria gonorrhoeae\b", re.IGNORECASE), "Nayseria gonorea"),
    (re.compile(r"\bChlamydia trachomatis\b", re.IGNORECASE), "Klamidya trakomatis"),
    (re.compile(r"\bHelicobacter pylori\b", re.IGNORECASE), "Helikobakter pilori"),
    # Sıra sayıları ve yüzdeler (TTS telaffuzu)
    (re.compile(r"\b1\.(?=\s|[,\)]|$)"), "birinci"),
    (re.compile(r"\b2\.(?=\s|[,\)]|$)"), "ikinci"),
    (re.compile(r"\b3\.(?=\s|[,\)]|$)"), "üçüncü"),
    (re.compile(r"\b4\.(?=\s|[,\)]|$)"), "dördüncü"),
    (re.compile(r"\b5\.(?=\s|[,\)]|$)"), "beşinci"),
    (re.compile(r"\b6\.(?=\s|[,\)]|$)"), "altıncı"),
    (re.compile(r"\b7\.(?=\s|[,\)]|$)"), "yedinci"),
    (re.compile(r"\b8\.(?=\s|[,\)]|$)"), "sekizinci"),
    (re.compile(r"\b9\.(?=\s|[,\)]|$)"), "dokuzuncu"),
    (re.compile(r"\b10\.(?=\s|[,\)]|$)"), "onuncu"),
    (re.compile(r"\b11\.(?=\s|[,\)]|$)"), "on birinci"),
    (re.compile(r"\b12\.(?=\s|[,\)]|$)"), "on ikinci"),
    (re.compile(r"\b13\.(?=\s|[,\)]|$)"), "on üçüncü"),
    (re.compile(r"\b14\.(?=\s|[,\)]|$)"), "on dördüncü"),
    (re.compile(r"\b15\.(?=\s|[,\)]|$)"), "on beşinci"),
    (re.compile(r"\b16\.(?=\s|[,\)]|$)"), "on altıncı"),
    (re.compile(r"\b17\.(?=\s|[,\)]|$)"), "on yedinci"),
    (re.compile(r"\b18\.(?=\s|[,\)]|$)"), "on sekizinci"),
    (re.compile(r"\b19\.(?=\s|[,\)]|$)"), "on dokuzuncu"),
    (re.compile(r"\b20\.(?=\s|[,\)]|$)"), "yirminci"),
    (re.compile(r"\b21\.(?=\s|[,\)]|$)"), "yirmi birinci"),
    (re.compile(r"\b22\.(?=\s|[,\)]|$)"), "yirmi ikinci"),
    (re.compile(r"\b23\.(?=\s|[,\)]|$)"), "yirmi üçüncü"),
    (re.compile(r"\b1\.'si\b"), "birincisi"),
    (re.compile(r"\b2\.'si\b"), "ikincisi"),
    (re.compile(r"\b3\.'sü\b"), "üçüncüsü"),
    (re.compile(r"\b4\.'sü\b"), "dördüncüsü"),
    (re.compile(r"\b5\.'si\b"), "beşincisi"),
    (re.compile(r"%([0-9]+)"), r"yüzde \1"),
]


def duzelt(metin: str, kayit: list | None = None) -> str:
    """Paragraf içindeki kısaltma hece dizilerini ve tıbbi terimleri seslendirme için fonetik hâle getirir."""
    for pat, fon in FONETIK_TTS:
        metin = pat.sub(fon, metin)
    K = kume()
    if not K:
        return metin
    eslesme = list(SOZ.finditer(metin))
    out, son, i = [], 0, 0
    while i < len(eslesme):
        bul = _en_iyi(metin, eslesme, i, K)
        if bul:
            # bir sonraki sözcükten başlayan dizi daha ileri uzanıyorsa (ya da baştaki bağlaçsa aynı yere) ilk sözcük dışarıda
            sonraki = _en_iyi(metin, eslesme, i + 1, K) if i + 1 < len(eslesme) else None
            # (4+ heceli kısaltma baştaki "ve"yi korur: ve e ge ef = VEGF)
            if sonraki and (sonraki[0] > bul[0] or (sonraki[0] == bul[0] and bul[1][0] in BAGLAC and (bul[1][0] != "ve" or len(bul[1]) < 4))):
                bul = None
        if bul:
            j, heceler, ek = bul
            bitisik = "".join(heceler)
            if eslesme[i].group(0)[:1].isupper():
                bitisik = bitisik[:1].upper() + bitisik[1:]
            bas, bit = eslesme[i].start(), eslesme[j - 1].end()
            out.append(metin[son:bas] + bitisik + ek)
            if kayit is not None:
                kayit.append((metin[bas:bit], bitisik + ek))
            son, i = bit, j
        else:
            i += 1
    out.append(metin[son:])
    return "".join(out)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["--kur"]:
        print(len(kur()), "kısaltma →", SOZLUK)
    elif a[:1] == ["--rapor"]:
        n = int(a[1]) if len(a) > 1 else 60
        say = collections.Counter()
        for f in sorted(glob.glob(str(MEDS / "data/sesli_anlatim/metin/*.md"))):
            k: list = []
            duzelt(open(f, encoding="utf-8").read(), k)
            say.update(f"{x} → {y}" for x, y in k)
        print(sum(say.values()), "değişiklik,", len(say), "farklı")
        for s, c in say.most_common(n):
            print(f"{c:5} {s}")
    elif a:
        print(duzelt(" ".join(a)))
    else:
        print(__doc__)
