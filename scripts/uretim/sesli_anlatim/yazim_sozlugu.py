#!/usr/bin/env python3
"""Sesli ders ekran yazımı sözlüğü — konuşma metni okunuşla yazılır, ekranda doğru yazım gösterilir (kullanıcı, 2026-10-22).

  kisaltma: okunuş → yazım   "beta ha ce ge" → "β-hCG", "de ne a" → "DNA" (büyük/küçük harf ders kaynağındaki en sık biçim)
  acilim:   açılım → kısaltma "plazminojen aktivatörü" → "t-PA": ekranda açılımın ardına "(t-PA)" eklenir (kaynakta
            "… (t-PA)" biçiminde geçen ve konuşma metinlerinde kullanılan açılımlar)

Ses ve saklanan metin değişmez; dönüşüm ekranda (src/services/sayiYazim.ts → ekranYazimi) yapılır.
Kullanım: yazim_sozlugu.py   (src/data/sesli_anlatim/yazim_sozlugu.json üretir)
"""
from __future__ import annotations
# Konum-bağımsız kök (2026-11-16): sabit parents[N] yerine scripts/kok.py (dosya taşınsa da doğru).
import sys as _sys
from pathlib import Path as _Path
_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402

import collections
import glob
import json
import re
from pathlib import Path

import okunus as O

MEDS = _kok.MEDS
CIKTI = MEDS / "src/data/sesli_anlatim/yazim_sozlugu.json"
YUNAN = {"alfa": "α", "beta": "β", "gama": "γ", "gamma": "γ", "delta": "δ", "epsilon": "ε", "kappa": "κ", "lambda": "λ"}


# kaynakta "(…)" biçiminde geçmeyen ama yaygın açılımlar (kullanıcı örnekleri, 2026-10-22)
EL_ACILIM = {"doku plazminojen aktivatörü": "t-PA", "glikoprotein ib": "Gp Ib", "glikoprotein iib/iiia": "Gp IIb/IIIa",
             "von willebrand faktörü": "vWF", "insan koryonik gonadotropini": "hCG"}


# okunuşu kaynaktan türetilemeyen yazımlar (çok sözcüklü / sayı üslü; k1-51 V2, 2026-10-23)
EL_KISALTMA = {"ce re pe": "CRP", "pe ha": "pH", "ha ı ve": "HIV", "e koli": "E. coli", "hepatit be": "hepatit B",
               "pe fimbriya": "P fimbriya", "tamm horsfall": "Tamm-Horsfall",
               "on üzeri beş": "10⁵", "on üzeri dört": "10⁴", "on üzeri üç": "10³",
               # patoloji V2 okunuşları (2026-10-23)
               "anka": "ANCA", "pe i ka üç ce a": "PIK3CA", "ka ras": "KRAS", "i ge a": "IgA", "i ge ge": "IgG",
               "i ge e": "IgE", "i ge em": "IgM", "pe i üç ka": "PI3K", "pe i üç kinaz": "PI3 kinaz",
               "e er": "ER", "pe er": "PR", "a ef pe": "AFP", "pe de el bir": "PD-L1",
               "pe em el ra ra": "PML-RARA", "e em el dört alk": "EML4-ALK", "pe de ge ef": "PDGF", "be ce ar abl": "BCR-ABL",
               "be ce er abl": "BCR-ABL", "ef se epsilon": "Fcε", "se te el a": "CTLA", "en a pe ku i": "NAPQI", "e te es": "ETS",
               "be ka": "BK", "a le amiloid": "AL amiloid", "a a amiloid": "AA amiloid", "a le ve a a": "AL ve AA",
               "pe de bir": "PD-1", "se te el a dört": "CTLA-4", "se te el a dörde": "CTLA-4'e", "se te el a dörttür": "CTLA-4'tür",
               "ce te el a dört": "CTLA-4", "ge es": "Gs", "ge i": "Gi", "ge o": "Go", "ge ku": "Gq",
               "a er i de bir a": "ARID1A", "ve i em di ar": "EMDR", "i em di ar": "EMDR", "ce ce virüsü": "JC virüsü",
               "protein ce ve es": "protein C ve S", "te ve be hücreleri": "T ve B hücreleri", "be ve te hücre": "B ve T hücre",
               "de se me": "DSM", "dee see mee": "DSM", "de se em": "DSM", "tee ree": "TR", "te re": "TR",
               "es er te": "SERT", "de a te": "DAT", "te se ce bir": "TSC1", "te se ce iki": "TSC2", "ye a pe bir": "YAP1",
               "be a pe bir": "BAP1", "ef el te bir": "FLT1", "te i ef bir": "TIF1", "ce re es te": "CREST",
               "em te ha ef ar": "MTHFR", "ef ce": "Fc", "de em pe": "DMPP", "pe ce es": "PCS", "ge te paz": "GTPaz",
               "le me iks bir be": "LMX1B", "pee haa kuu": "PHQ", "pe ha ku": "PHQ", "pi 3 kaa ve a kaa te": "PI3K ve AKT", "es te yükselmesi": "ST yükselmesi", "ge on bir": "G11", "de se me dört": "DSM-IV", "de se me beş": "DSM-5", "de se em beş": "DSM-5", "dee see mee beş": "DSM-5", "dee se em beş": "DSM-5", "de se em üç": "DSM-III", "dsm beş": "DSM-5", "de se me üç": "DSM-III", "dsm üç": "DSM-III", "dsm dört": "DSM-IV", "dsm beş te re": "DSM-5-TR", "de se em beş te re": "DSM-5-TR", "dee se me beş te re": "DSM-5-TR", "dee see mee beş tee ree": "DSM-5-TR", "de se em dört": "DSM-IV", "fe ge fe": "FGF", "fe ge felerin": "FGF'lerin", "es e er te": "SERT", "pi üç kaa ve a kaa te": "PI3K ve AKT", "te-me-se": "TMS", "te-de-ce-se": "tDCS", "ce de kırka": "CD40'a", "ce a on dokuz dokuz": "CA 19-9", "te em pe ar es es iki": "TMPRSS2"}


# harfleri tutsa da yanlış olan otomatik eşlemeler (H692): "a er i de bir a" = ARID1A, "ve i em di ar" = EMDR, "ce ce" = JC
ELE_KISALTMA = {"a er i", "ve i em", "ce ce", "ce ve es"}


ELE = {"germinal vezikül varlığı", "tetanoz bağışıklaması", "fingolimod hidroklorür", "nitrik oksit sentaz", "glatiramer asetat"}


SAYI_SOZ = {"sıfır", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz", "on", "yirmi", "otuz", "kırk", "elli",
            "altmış", "yetmiş", "seksen", "doksan", "yüz", "bin"}


KENAR = {"ile", "ise", "bu", "ya", "yani"}  # "ve"/"de" harf adı da olabilir (V, D): kesilmez


BAGLAC_HARF = {"a", "e", "o", "u", "ü", "ı", "i", "ve", "de", "en", "el", "ne", "ye", "se", "be", "ha", "he", "er", "es", "em", "ku"}


def _harf_adi(w: str) -> str | None:
    """Kısa ("de") ya da uzatılmış ("dee", "kuu", "aa") harf adı → büyük harf; değilse None."""
    if w in O.HARF:
        return O.HARF[w]
    if re.fullmatch(r"[ıi]+", w):  # "ıı", "ııı" Roma rakamıdır, uzatılmış I değil
        return None
    k = re.sub(r"([aeıioöuü])\1+$", r"\1", w)
    return O.HARF.get(k) if k != w else None


def _harf_tutar(okun: str, yazim: str) -> bool:
    """Okunuşun harfleri yazımın harfleriyle birebir mi? ("o ka be"↔OKB, "ve ne te"↔WNT, "ka o em te"↔KOMT; sayı/Yunan
    sözcüğü atlanır). Tek sözcüklü okunuş yalnız kısaltmanın kendisi olabilir ("komt"↔COMT, "vip"↔VIP); "ve"→OD, "alan"→CST,
    "e ka ge de es te"→ST gibi v2 hizalama artıkları elenir (H692)."""
    ws = okun.split()
    hy = re.sub(r"[^A-Z]", "", yazim.replace("İ", "I").upper())
    norm = lambda x: x.upper().replace("W", "V").replace("C", "K").replace("Ç", "K").replace("Ş", "S").replace("Ö", "O").replace("Ü", "U").replace("KS", "X")
    if len(ws) == 1:
        return norm(O.tr_lower(ws[0])) == norm(hy)
    # yazımda rakam varsa okunuşta sayı sözcüğü olmalı ("a ge" → A3243G olmaz)
    if re.search(r"\d", yazim) and not set(ws) & SAYI_SOZ:
        return False
    kalan = norm(hy)
    for w in ws:
        if w in SAYI_SOZ or w in YUNAN:
            continue
        h = _harf_adi(w)
        if h is not None and kalan.startswith(norm(h)):
            kalan = kalan[len(norm(h)):]
            continue
        # sözcük gibi okunan parça ("hoks" → HOX, "paks" → PAX, "lis" → LIS)
        p = norm(O.tr_lower(w))
        if len(p) >= 3 and kalan.startswith(p):
            kalan = kalan[len(p):]
            continue
        return False
    return kalan == ""


def bilinen_kisaltmalar(kaynak: str, metinler: list[str]) -> dict[str, str]:
    """Anahtar (yalnız harf, büyük, İ→I) → en sık yazım. Kaynak: kısaltma sözlüğü (seçilmiş) + kaynak md + ders metinleri."""
    say: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    def ekle(t: str, n: int = 1):
        if sum(c.isupper() for c in t) >= 2 and not re.search(r"[a-zçğıöşü]{3}", t):
            say[re.sub(r"[^A-Za-zİÇŞĞÖÜ]", "", t).replace("İ", "I").upper()][t] += n
    for t in json.loads((MEDS / "src/data/kisaltma_sozluk.json").read_text(encoding="utf-8")):
        ekle(t, 5)
    for metin in [kaynak, *metinler]:
        for t in re.findall(r"[A-Za-zÇĞİÖŞÜ][A-Za-zÇĞİÖŞÜ0-9\-]*", metin):
            ekle(re.sub(r"[\-0-9]+$", "", t))
    return {k: c.most_common(1)[0][0] for k, c in say.items() if len(k) >= 2}


def _dizide(sozler: list[str], ws: list, j: int, n: int) -> bool:
    """ws[j:j+n] boşlukla bitişik başka bir harf adıyla devam ediyor/başlıyor mu ("te se" ← "te se se be")?"""
    for k in (j - 1, j + n):
        if 0 <= k < len(ws):
            a, b = sorted((ws[k][0], ws[j if k < j else j + n - 1][0]))
            if all(x == " " for x in sozler[a + 1:b]) and _harf_adi(ws[k][1]) is not None:
                return True
    return False


def dizi_kisaltmalari(metinler: list[str], bilinen: dict[str, str]) -> dict[str, str]:
    """Harf adı dizisi ("o ka be", "te se se be", "dee see mee", "a ce te ha") → bilinen kısaltma (OKB, TSSB, DSM, ACTH).
    Her konumda en uzun eşleşme; 2 sözcüklük dizide ikisi de bağlaç olabilen harf adı değilse ("ve te" = VT sayılmaz)."""
    out: dict[str, str] = {}
    for m in metinler:
        sozler = re.findall(r"[A-Za-zÇĞİÖŞÜçğıöşü]+|[^A-Za-zÇĞİÖŞÜçğıöşü]+", m)
        ws = [(i, O.tr_lower(x)) for i, x in enumerate(sozler) if x[0].isalpha()]
        j = 0
        while j < len(ws):
            bul = None
            for n in range(min(8, len(ws) - j), 1, -1):
                parca = ws[j:j + n]
                # aradaki ayraç yalnız boşluk olmalı (cümle/virgül sınırı aşılmaz)
                if any(sozler[a + 1] != " " for (a, _), _b in zip(parca, parca[1:])):
                    continue
                harfler = [_harf_adi(w) for _, w in parca]
                if None in harfler:
                    continue
                if n == 2 and (all(w in BAGLAC_HARF for _, w in parca) or _dizide(sozler, ws, j, n)):
                    continue
                y = bilinen.get("".join(harfler).replace("Ç", "C").replace("Ş", "S").replace("Ö", "O").replace("Ü", "U"))
                if y and not re.search(r"[a-zçğıöşü]{2}", y):
                    bul = (n, " ".join(w for _, w in parca), y)
                    break
            if bul:
                out.setdefault(bul[1], bul[2])
                j += bul[0]
            else:
                j += 1
    return out


def v2_kisaltmalari() -> dict[str, str]:
    """Kurul 2+ v2 metinleri (ses ↔ ekran cümle çifti) → okunuş → yazım ("hoks" → "HOX", "paks altı" → "PAX6").
    Kaynak md'den türetilemeyen gen sembolleri ekranda okunuşla görünüyordu (H124, k2-08, 2026-10-28)."""
    import difflib
    oy: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    soz = re.compile(r"[A-Za-zÇĞİÖŞÜçğıöşüÂâ0-9]+(?:-[A-Za-z0-9]+)*")
    for f in sorted(glob.glob(str(MEDS / "data/sesli_anlatim/v2/*.json"))):
        try:
            v = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        for b in v.get("bolumler") or []:
            for p in b.get("paragraflar") or []:
                for c in p.get("cumleler") or []:
                    ses, ekr = soz.findall(c.get("ses") or ""), soz.findall(c.get("ekran") or "")
                    sl, el = [O.tr_lower(x) for x in ses], [O.tr_lower(x) for x in ekr]
                    for op, a1, a2, b1, b2 in difflib.SequenceMatcher(None, sl, el, autojunk=False).get_opcodes():
                        if op != "replace" or b2 - b1 != 1 or not 1 <= a2 - a1 <= 6:
                            continue
                        y = ekr[b1]
                        # yalnız sembol yazımı (HOX, PAX6, COL1A1); Roma rakamı ve "Bölüm" gibi sözcükler değil
                        if not re.fullmatch(r"[A-Z][A-Z0-9]+", y) or re.fullmatch(r"[IVXLC]+", y) or sum(ch.isupper() for ch in y) < 2:
                            continue
                        okun = sl[a1:a2]
                        while okun and okun[0] in KENAR:
                            okun = okun[1:]
                        while okun and okun[-1] in KENAR:
                            okun = okun[:-1]
                        # okunuş hece dizisidir: gerçek sözcük ya da salt sayı dizisi eşlenmez
                        if not okun or any(len(w) > 4 and w not in SAYI_SOZ for w in okun) or all(w in SAYI_SOZ for w in okun):
                            continue
                        oy[" ".join(okun)][y] += 1
    return {k: c.most_common(1)[0][0] for k, c in oy.items()}


def kaynak_metni() -> str:
    return "\n".join(open(f, encoding="utf-8", errors="ignore").read()
                     for f in glob.glob(str(O.KAYNAK / "**/*.md"), recursive=True))


def main():
    kaynak = kaynak_metni()
    biçim: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    for t in re.findall(r"[α-ωA-Za-zÇĞİÖŞÜçğıöşü0-9]+(?:-[A-Za-z0-9]+)*", kaynak):
        if sum(c.isupper() for c in t) >= 1 and re.search(r"[A-Za-z]", t):
            biçim[re.sub(r"[^A-Za-z]", "", t).upper()][t] += 1
    metinler = [open(f, encoding="utf-8").read() for f in sorted(glob.glob(str(MEDS / "data/sesli_anlatim/metin/*.md")))]

    kisa: dict[str, str] = {}
    for m in metinler:
        kayit: list = []
        # FONETIK_TTS'siz yalnız hece dizisi: okunus.duzelt FONETIK uyguladığı için _en_iyi'yi doğrudan yürüt
        K = O.kume()
        es = list(O.SOZ.finditer(m))
        i = 0
        while i < len(es):
            bul = O._en_iyi(m, es, i, K)
            if bul:
                sonraki = O._en_iyi(m, es, i + 1, K) if i + 1 < len(es) else None
                if sonraki and (sonraki[0] > bul[0] or (sonraki[0] == bul[0] and bul[1][0] in O.BAGLAC and (bul[1][0] != "ve" or len(bul[1]) < 4))):
                    bul = None
            if not bul:
                i += 1
                continue
            j, heceler, ek = bul
            anahtar = "".join(O.HARF[h] for h in heceler)
            adaylar = biçim.get(anahtar)
            if adaylar and len(heceler) >= 2 and not (len(heceler) == 2 and set(heceler) & {"o", "e", "a", "de"}):
                # rakamlı biçim ("TP53") okunuşun ardındaki sayıyı da içerir: harf kısmı alınır, rakam sayı geçişinden gelir
                # ve ekranda "bitisik" listesiyle birleşir ("te pe elli üç" → "TP 53" → "TP53"; eskiden "TP53 53")
                yazim = adaylar.most_common(1)[0][0]
                if re.search(r"\d$", yazim):
                    alt = [t for t, _ in adaylar.most_common() if re.fullmatch(r"[A-Za-z]+", t) and sum(c.isupper() for c in t) >= 2]
                    yazim = alt[0] if alt else re.sub(r"-?\d+$", "", yazim)
                okun = " ".join(heceler)
                # önceki sözcük Yunan harfiyse ("beta ha ce ge") ve kaynakta "β-hCG" geçiyorsa birlikte
                once = O.tr_lower(es[i - 1].group(0)) if i else ""
                if once in YUNAN:
                    yb = [t for t in adaylar if t.startswith(YUNAN[once])]
                    if not yb and f"{YUNAN[once]}-{yazim}" in kaynak:
                        yb = [f"{YUNAN[once]}-{yazim}"]
                    if yb:
                        kisa[f"{once} {okun}"] = yb[0] if "-" in yb[0] or yb[0][1:2] == "-" else yb[0]
                kisa.setdefault(okun, yazim)
            i = j

    # açılım (KISALTMA)
    toplam = O.tr_lower("\n".join(metinler))
    acilim: dict[str, str] = {}
    for m in re.finditer(r"((?:[A-Za-zÇĞİÖŞÜçğıöşü\-]+ ){1,6}?[A-Za-zÇĞİÖŞÜçğıöşü\-]+)\s*\(([A-Za-zα-ω][A-Za-z0-9α-ω\-]{1,11})\)", kaynak):
        ab = m.group(2)
        buyuk = [c for c in ab if c.isupper()]
        if len(buyuk) < 2 and not (len(buyuk) == 1 and len(ab) <= 3):
            continue
        sozler = m.group(1).split()
        for n in range(min(6, len(sozler)), 0, -1):
            ifade = O.tr_lower(" ".join(sozler[-n:]))
            ilk = {w[0].upper() for w in ifade.split()}
            harf = {O.tr_lower(c) for c in ab if c.isalpha()} | {"ç" if c == "C" else c for c in []}
            bas = ifade.split()[0]
            # baştaki sözcük kısaltmanın bir harfiyle başlamalı ("kısmında dikkat …", "ya da germinal …" elenir)
            if bas[0] not in harf and not (bas[0] in "çşğıöü" and {"ç": "c", "ş": "s", "ğ": "g", "ı": "i", "ö": "o", "ü": "u"}[bas[0]] in harf):
                continue
            if bas in {"ve", "ya", "da", "de", "en", "ile", "veya"}:
                continue
            eksik = len(set(buyuk)) - sum(c in ilk for c in set(buyuk))
            if len(ifade) < 8 or eksik > (1 if len(set(buyuk)) >= 4 else 0) or ifade.split()[0][0].upper() != buyuk[0].replace("İ", "I"):
                continue
            if re.search(rf"(?<![a-zçğıöşü]){re.escape(ifade)}", toplam):
                acilim.setdefault(ifade, ab)
                break

    for k in [k for k, v in acilim.items() if re.search(r"\d", v) or k in ELE]:
        del acilim[k]
    acilim.update(EL_ACILIM)
    for k, y in v2_kisaltmalari().items():
        kisa.setdefault(k, y)
    # Türkçe sözcük yazım sayılmaz ("be el em" → "Bölüm", "be a ka" → "Bakış"; kaynak md'deki büyük harfli başlıklar)
    kisa = {k: y for k, y in kisa.items() if not re.search(r"[ÇĞİÖŞÜçğıöşü]", y)
            and (len(y) <= 2 or sum(ch.isupper() for ch in y) >= 2)
            # rakamlı/Yunan harfli yazım okunuşta sayı/harf adı yoksa eksik eşlemedir ("te i ef" → "TIF1γ")
            and not (re.search(r"[\dα-ω]", y) and not set(k.split()) & (SAYI_SOZ | set(YUNAN)))}
    # Kurul 2+ kısaltmaları kaynak md'de az/hiç geçmiyor, hece bölme ("o ka be") eşleşmiyordu (H692)
    for k, y in dizi_kisaltmalari(metinler, bilinen_kisaltmalar(kaynak, metinler)).items():
        kisa.setdefault(k, y)
    # iki sözcüklük yeni eşleme çoğunlukla uzun kısaltmanın parçasıdır ("te se" ← TSSB, "se me" ← DSM): yalnız önceden
    # yayındaysa ya da metinde tek başına geçiyorsa (dizi geçişi) alınır
    try:
        onceki = {k for k, _ in json.loads(CIKTI.read_text(encoding="utf-8")).get("kisaltma", [])}
    except (OSError, ValueError):
        onceki = set()
    tek = dizi_kisaltmalari(metinler, bilinen_kisaltmalar(kaynak, metinler))
    kisa = {k: y for k, y in kisa.items() if _harf_tutar(k, y)
            and (len(k.split()) != 2 or k in onceki or k in tek or k in EL_KISALTMA)}
    for k, y in tek.items():
        if _harf_tutar(k, y):
            kisa.setdefault(k, y)
    # yeni eşleme güvenliği (H692): sayı sözcüğü içeren ("ce de yirmi" → CD20, "ce de yirmi sekiz"i bozar), metinde sayıdan
    # ya da başka harf adından hemen önce/sonra geçen ("pe ı" ← "pe ı te iks üç" = PITX3, "ce de" ← CD138) ve "ve"+kısaltma
    # ile karışan ("ve te" ← "ve Th2", "ve aa" ← "ve AA") eşleme alınmaz; bu biçimleri ekranYazim'in harf+sayı geçişi kurar.
    birlesik = O.tr_lower("\n".join(metinler))
    def guvenli(k: str) -> bool:
        if k in onceki or k in EL_KISALTMA:
            return True
        ws = k.split()
        if set(ws) & SAYI_SOZ:
            return False
        if ws[0] == "ve" and (len(ws) == 2 or " ".join(ws[1:]) in kisa):
            return False
        harf_ad = "|".join(sorted({*O.HARF, *SAYI_SOZ} - BAGLAC_HARF, key=len, reverse=True))
        ek = re.escape(k).replace("\\ ", "\\s+")
        if re.search(rf"(?:(?<![\wçğıöşü])(?:{harf_ad})\s+{ek}(?![\wçğıöşü])|(?<![\wçğıöşü]){ek}\s+(?:{harf_ad}|\d)(?![\wçğıöşü]))", birlesik):
            return False
        return True
    kisa = {k: y for k, y in kisa.items() if guvenli(k) and k not in ELE_KISALTMA}
    kisa.update(EL_KISALTMA)
    CIKTI.parent.mkdir(parents=True, exist_ok=True)
    # rakamla bitişik yazılan kısaltmalar (TP53, HER2, BRCA1, C3, CD4, Ki-67): ekranda "TP 53" → "TP53"
    # aynı kısaltmanın en sık biçimi seçilir ("BCL-2" mi "BCL2" mi kaynaktaki sıklığa göre)
    bsay = collections.Counter(t for t in re.findall(r"(?<![A-Za-z0-9])[A-Za-z]{1,6}-?\d{1,3}[a-z]?(?![A-Za-z0-9])", kaynak)
                               if sum(c.isupper() for c in t) >= 1)
    enc: dict[str, str] = {}
    for t, _ in bsay.most_common():
        enc.setdefault(t.replace("-", "").upper(), t)
    bitisik = sorted(enc.values())
    veri = {"yunan": YUNAN, "harf": O.HARF, "bitisik": bitisik,
            "kisaltma": sorted(kisa.items(), key=lambda x: -len(x[0])),
            "acilim": sorted(acilim.items(), key=lambda x: -len(x[0]))}
    CIKTI.write_text(json.dumps(veri, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(len(kisa), "kısaltma,", len(acilim), "açılım →", CIKTI)


if __name__ == "__main__":
    main()
