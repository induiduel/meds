#!/usr/bin/env python3
"""Modül dersleri (TBG Sınav Kampı) için kısaltma/gen adı okunuşu — YALNIZ EMA'ya giden metne uygulanır.

Modül metni ekranda standart yazımla durur (BRCA1, FGFR3, PAPP-A, kırk altı XY); Kurul 1 okunuş düzeltmesi (okunus.py)
yalnız ayrık yazılmış harf dizilerini tanıdığından bu yazımı okuyamaz. Burada her büyük harfli kısaltma ünlüsü uzatılmış
harf adlarına (Kurul 2 standardı, kisaltma_ses.py: "vee haa lee"), içindeki rakamlar Türkçe sayıya çevrilir; kelime gibi
okunanlar (PARP, FISH, ICSI, HIF…) sözlükten gelir. Paragraf/cümle sayısı değişmez (nokta eklenmez/silinmez).
Kullanım: modul_okunus.py "metin"  |  from modul_okunus import donustur
"""
from __future__ import annotations

import re
import sys

MODUL_ANAHTARLAR = {"k1-70-tbg-sinav-kampi", "k1-59-immunofarmakoloji-v2"}  # V2: yazımla yazılmış metin (CD2, IL-2), okunuş burada
SON_PROVA = re.compile(r"^k\d+-\d+-son-prova-")  # Son Prova partları da modül yazımıyla (BRCA1, IL-6) yazılır


def modul_mu(anahtar: str) -> bool:
    return anahtar in MODUL_ANAHTARLAR or bool(SON_PROVA.match(anahtar))

UZUN = {"A": "aa", "B": "bee", "C": "cee", "Ç": "çee", "D": "dee", "E": "ee", "F": "fee", "G": "gee", "H": "haa", "I": "ıı",
        "İ": "ii", "J": "jee", "K": "kaa", "L": "lee", "M": "mee", "N": "nee", "O": "oo", "Ö": "öö", "P": "pee", "R": "ree",
        "S": "see", "Ş": "şee", "T": "tee", "U": "uu", "Ü": "üü", "V": "vee", "W": "vee", "Y": "yee", "Z": "zee", "Q": "kuu",
        "X": "iks"}
# kelime gibi okunan ya da yerleşik okunuşu olan adlar (rakamsız kök; rakam ayrıca okunur)
KELIME = {
    "PARP": "parp", "FISH": "fiş", "ICSI": "iksi", "HIF": "hif", "MET": "met", "RET": "ret", "RAS": "ras", "RAF": "raf",
    "MEK": "mek", "ERK": "erk", "KIT": "kit", "MYC": "mik", "POLE": "pol e", "PTEN": "pe ten", "BRCA": "bercea",
    "SOX": "soks", "FOXL": "foks el", "DAX": "daks", "WNT": "vint", "RSPO": "ar spo", "PAX": "paks", "EMX": "e em iks",
    "LHX": "el ha iks", "CHEK": "çek", "PALB": "pal bee", "HOXB": "hoks bee", "EPCAM": "ep kam", "VACTERL": "vakterl",
    "MURCS": "murks", "SERKAL": "serkal", "WAGR": "vagr", "StAR": "star", "PAPP": "pap", "TBG": "tee bee gee",
    "mTOR": "em tor", "PIK": "pik", "VUS": "vee uu see", "NTRK": "en te er ka", "POR": "por", "AXL": "aa iks el", "ERBB": "er bee bee",
    "CTLA": "cee tee lee aa", "TP": "tee pee", "DNA": "dee nee aa", "mRNA": "mee ree nee aa", "hCG": "haa cee gee",
    "RhD": "ree haa dee", "pRB": "pee ree bee", "EGFR": "ee gee fee ree", "FGFR": "fee gee fee ree",
    # Son Prova (2026-10-21): kelime gibi okunan kısaltmalar
    "AIDS": "eyds", "ELISA": "eliza", "SOFA": "sofa", "SIRS": "sirs", "TORCH": "torç", "TORCHS": "torçs", "ANCA": "anka",
    "UNICEF": "yunisef", "MERS": "mers", "CREST": "krest", "PUMA": "puma", "SNAIL": "sneyl", "TWIST": "tvist",
    "HELLP": "help", "NICE": "nays", "KRAS": "kaa ras", "HRAS": "haa ras", "BRAF": "bee raf", "MALT": "malt", "JAK": "jak",
    "SMAD": "smad", "RANKL": "rank el", "AmpC": "amp cee", "CAR": "kar", "NAPQI": "nee aa pee kiyu ıı", "KETEM": "ketem",
    "SARS": "sars", "CoV": "kov", "SCID": "skid", "GLUT": "glut", "AIRE": "eyr", "CART": "kart", "OXA": "oksa",
    "VISA": "vize", "MRSA": "mee ree see aa", "Scl": "skl", "Sm": "smit",
}
# İmmünofarmakoloji V2 (2026-10-22): I harfi "ıı" değil; IL = interlökin
KELIME.update({"IL": "interlökin", "IVIG": "ii vee ii gee", "KIR": "kaa ii ree", "HAMA": "hama", "IgE": "immünoglobulin ee",
               "IgG": "immünoglobulin gee", "IgM": "immünoglobulin mee", "Rh": "ree haa", "pH": "pee haa"})
# Roma rakamı (tip II, faktör XIII, sınıf IV): sayıyla. XX, XXX, XY gibi kromozom formülleri DEĞİL (X tek başına da değil)
ROMEN = {"II": 2, "III": 3, "IV": 4, "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "XI": 11, "XII": 12, "XIII": 13}
ROMEN_RE = re.compile(r"^(II|III|IV|VI|VII|VIII|IX|XI|XII|XIII)([abAB]?)$")
BIR = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
ON = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]


def sayi_oku(n: int) -> str:
    if n == 0:
        return "sıfır"
    if n >= 100:
        return " ".join(x for x in [("" if n // 100 == 1 else BIR[n // 100]) + " yüz", sayi_oku(n % 100) if n % 100 else ""] if x).strip()
    return " ".join(x for x in (ON[n // 10], BIR[n % 10]) if x)


def harfler(s: str) -> str:
    return " ".join(UZUN.get(c.upper(), c.lower()) for c in s if c.isalpha())


def parca_oku(p: str) -> str:
    """Tire ile ayrılmamış tek parça: harf kökü + rakam + harf kuyruğu (PIK3CA, CD80, CYP21A2)."""
    out = []
    for m in re.finditer(r"[A-Za-zÇĞİÖŞÜçğıöşü]+|\d+", p):
        x = m.group()
        if x.isdigit():
            out.append(sayi_oku(int(x)))
        elif ROMEN_RE.match(x):
            r = ROMEN_RE.match(x)
            out.append(sayi_oku(ROMEN[r.group(1)]) + (" " + UZUN[r.group(2).upper()] if r.group(2) else ""))
        elif re.fullmatch(r"Gp(II|III|IV|I)([ab]?)", x):
            r = re.fullmatch(r"Gp(II|III|IV|I)([ab]?)", x)
            out.append("gee pee " + sayi_oku({"I": 1, **ROMEN}[r.group(1)]) + (" " + UZUN[r.group(2).upper()] if r.group(2) else ""))
        elif x in KELIME:
            out.append(KELIME[x])
        elif sum(c.isupper() for c in x) >= 2 or (len(x) == 1 and x.isupper()) or (len(x) <= 2 and x[:1].isupper()):
            out.append(harfler(x))
        elif len(x) == 1 and out and x.lower() in "abcdefghijklmnoprstuvyz":
            out.append(UZUN[x.upper()])  # C3b, C5a: rakamdan sonraki tek küçük harf de harf adıyla
        else:
            out.append(x)
    return " ".join(out)


# büyük harfli kısaltma (≥2 büyük harf ya da büyük harf + rakam), tireli birleşikleri ve Türkçe eki ile
TOKEN = re.compile(r"(?<![\wÇĞİÖŞÜçğıöşü-])((?:[A-Za-zÇĞİÖŞÜçğıöşü]*[A-ZÇĞİÖŞÜ][A-Za-z0-9ÇĞİÖŞÜçğıöşü]*)(?:-[A-Za-z0-9]+)*)(['’][a-zçğıöşü]+)?(?![\wÇĞİÖŞÜçğıöşü])")


def _kisaltma_mi(w: str) -> bool:
    if w in KELIME or w.split("-")[0] in KELIME:
        return True
    govde = w.replace("-", "")
    buyuk = sum(c.isupper() for c in govde)
    # Prader-Willi, DiGeorge, McCune gibi özel adlar kısaltma değil
    if re.fullmatch(r"(?:[A-ZÇĞİÖŞÜ][a-zçğıöşüé]+)+(?:-(?:[A-ZÇĞİÖŞÜ][a-zçğıöşüé]+)+)*", w):
        return False
    if re.fullmatch(r"[XY][pq]", w):
        return True
    if buyuk >= 2:
        return True
    return bool(re.search(r"[A-Z].*\d|\d.*[A-Z]", govde))


def donustur(metin: str) -> str:
    # c-MYC, a-CGH (küçük harf önekli) ve p53, p11 (küçük p + rakam)
    metin = re.sub(r"(?<![\wçğıöşü])([a-z])-([A-Z][A-Za-z0-9]+)", lambda m: UZUN[m.group(1).upper()] + " " + parca_oku(m.group(2)), metin)
    metin = re.sub(r"(?<![\wçğıöşü])([pq])(\d+)(['’]([a-zçğıöşü]+))?(?![\w])", lambda m: f"{UZUN[m.group(1).upper()]} {sayi_oku(int(m.group(2)))}" + (f" {m.group(4)}" if m.group(4) else ""), metin)

    def f(m):
        w, ek = m.group(1), (m.group(2) or "")
        if (re.fullmatch(r"[A-ZÇĞİÖŞÜ][a-zçğıöşü]+", w) and not re.fullmatch(r"[XY][pq]", w)) or not _kisaltma_mi(w):
            # tek büyük harf (X, Y kromozomu; vitamin B; hepatit B) harf adıyla
            if len(w) == 1 and w in UZUN:
                return UZUN[w] + (" " + ek.lstrip("'’") if ek else "")
            return m.group(0)
        s = " ".join(parca_oku(p) for p in w.split("-"))
        return s + (" " + ek.lstrip("'’") if ek else "")
    return TOKEN.sub(f, metin)


if __name__ == "__main__":
    print(donustur(" ".join(sys.argv[1:]) or sys.stdin.read()))
