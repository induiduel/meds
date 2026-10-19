#!/usr/bin/env python3
"""
metin_temizle.py — Sesli anlatım metinlerindeki fonetik okunuşları, yazıyla yazılmış yılları,
yüzdeleri ve sayıları temiz, okunaklı tıbbi standart metne dönüştürür.
Cümleleri paragraflar içinde yeni satırlara ayırır (okunaklılık için).
Vurgu (highlight) koordinatlarını karakter düzeyinde yeniden eşler.
"""
import difflib
import glob
import json
import re
import sys
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
METIN_DIR = MEDS / "data/sesli_anlatim/metin"
VURGU_DIR = MEDS / "data/sesli_anlatim/vurgu"

# 1. Sabit terim ve fonetik düzeltmeleri
TERIMLER = [
    (r"\bha te el ve bir\b", "HTLV-1"),
    (r"\bha te el ve iki\b", "HTLV-2"),
    (r"\bha te el ve\b", "HTLV"),
    (r"\bepştayn bar virüsü\b", "Epstein-Barr virüsü (EBV)"),
    (r"\bEpştayn Bar virüsü\b", "Epstein-Barr virüsü (EBV)"),
    (r"\bepştayn bar\b", "Epstein-Barr"),
    (r"\bEpştayn Bar\b", "Epstein-Barr"),
    (r"\bEpştayn-Bar\b", "Epstein-Barr"),
    (r"\bhepatit be virüsü\b", "Hepatit B virüsü (HBV)"),
    (r"\bhepatit ce virüsü\b", "Hepatit C virüsü (HCV)"),
    (r"\bhepatit de virüsü\b", "Hepatit D virüsü (HDV)"),
    (r"\bhepatit e virüsü\b", "Hepatit E virüsü (HEV)"),
    (r"\bhepatit a virüsü\b", "Hepatit A virüsü (HAV)"),
    (r"\bhepatit be\b", "Hepatit B"),
    (r"\bhepatit ce\b", "Hepatit C"),
    (r"\bhepatit de\b", "Hepatit D"),
    (r"\bhepatit e\b", "Hepatit E"),
    (r"\bhepatit a\b", "Hepatit A"),
    (r"\binsan papilloma virüsü\b", "İnsan papilloma virüsü (HPV)"),
    (r"\bİnsan papilloma virüsü\b", "İnsan papilloma virüsü (HPV)"),
    (r"\binsan immün yetmezlik virüsü\b", "İnsan immün yetmezlik virüsü (HIV)"),
    (r"\bvarisella zoster virüsü\b", "Varisella zoster virüsü (VZV)"),
    (r"\bVarisella zoster virüsü\b", "Varisella zoster virüsü (VZV)"),
    (r"\bvarisella zoster\b", "Varisella zoster"),
    (r"\bkaposi sarkomu herpes virüsü\b", "Kaposi sarkomu herpes virüsü (KSHV / HHV-8)"),
    (r"\bKaposi sarkomu herpes virüsü\b", "Kaposi sarkomu herpes virüsü (KSHV / HHV-8)"),
    (r"\binsan herpes virüsü sekiz\b", "İnsan herpes virüsü 8 (HHV-8)"),
    (r"\bİnsan herpes virüsü sekiz\b", "İnsan herpes virüsü 8 (HHV-8)"),
    (r"\bte ha bir\b", "Th1"),
    (r"\bte ha iki\b", "Th2"),
    (r"\bte ha on yedi\b", "Th17"),
    (r"\bte reg\b", "Treg"),
    (r"\bem ha ce\b", "MHC"),
    (r"\bpe ce er\b", "PCR"),
    (r"\bel de ha\b", "LDH"),
    (r"\ba se te ha\b", "ACTH"),
    (r"\bte se ha\b", "TSH"),
    (r"\bLaypzig\b", "Leipzig"),
    (r"\blaypzig\b", "Leipzig"),
    (r"\bCovanni Battista Morgani\b", "Giovanni Battista Morgagni"),
    (r"\bcovanni battista morgani\b", "Giovanni Battista Morgagni"),
    (r"\bİbni Sina\b", "İbn-i Sina"),
    (r"\bibni sina\b", "İbn-i Sina"),
    (r"\bYunisef\b", "UNICEF"),
    (r"\byunisef\b", "UNICEF"),
    (r"\bPapanikolau\b", "Papanicolaou"),
    (r"\bpapanikolau\b", "Papanicolaou"),
    (r"\bVirchow\b", "Rudolf Virchow"),
    (r"\bRudolf Rudolf Virchow\b", "Rudolf Virchow"),
    (r"\bTip 1 iki gün\b", "1-2 gün"),
    (r"\bgecikmiş Tip 1 iki gün\b", "gecikmiş tip 1-2 gün"),
    (r"\bgranülom tip dördün\b", "granülom Tip 4'ün"),
    (r"\bGranülom tip dördün\b", "Granülom Tip 4'ün"),
    (r"\btip bir\b", "Tip 1"),
    (r"\btip iki\b", "Tip 2"),
    (r"\btip üç\b", "Tip 3"),
    (r"\btip dört\b", "Tip 4"),
    (r"\bevre bir\b", "Evre 1"),
    (r"\bevre iki\b", "Evre 2"),
    (r"\bevre üç\b", "Evre 3"),
    (r"\bevre dört\b", "Evre 4"),
    (r"\bgrade bir\b", "Grade 1"),
    (r"\bgrade iki\b", "Grade 2"),
    (r"\bgrade üç\b", "Grade 3"),
]

# 2. On 1. / On 2. / On 3. -> 11. / 12. / 13.
ONLU_ORDINAL = [
    (r"\b[Oo]n\s+1\.(?=\s|[,\)]|$)", "11."),
    (r"\b[Oo]n\s+2\.(?=\s|[,\)]|$)", "12."),
    (r"\b[Oo]n\s+3\.(?=\s|[,\)]|$)", "13."),
    (r"\b[Oo]n\s+4\.(?=\s|[,\)]|$)", "14."),
    (r"\b[Oo]n\s+5\.(?=\s|[,\)]|$)", "15."),
    (r"\b[Oo]n\s+6\.(?=\s|[,\)]|$)", "16."),
    (r"\b[Oo]n\s+7\.(?=\s|[,\)]|$)", "17."),
    (r"\b[Oo]n\s+8\.(?=\s|[,\)]|$)", "18."),
    (r"\b[Oo]n\s+9\.(?=\s|[,\)]|$)", "19."),
    (r"\b[Yy]irmi\s+1\.(?=\s|[,\)]|$)", "21."),
    (r"\b[Yy]irmi\s+2\.(?=\s|[,\)]|$)", "22."),
    (r"\b[Yy]irmi\s+3\.(?=\s|[,\)]|$)", "23."),
    (r"\b[Yy]irmi\s+4\.(?=\s|[,\)]|$)", "24."),
    (r"\b[Yy]irmi\s+5\.(?=\s|[,\)]|$)", "25."),
    (r"\b[Yy]irmi\s+6\.(?=\s|[,\)]|$)", "26."),
    (r"\b[Yy]irmi\s+7\.(?=\s|[,\)]|$)", "27."),
    (r"\b[Yy]irmi\s+8\.(?=\s|[,\)]|$)", "28."),
    (r"\b[Yy]irmi\s+9\.(?=\s|[,\)]|$)", "29."),
    (r"\b[Oo]tuz\s+([1-9])\.(?=\s|[,\)]|$)", r"3\1."),
    (r"\b[Kk]ırk\s+([1-9])\.(?=\s|[,\)]|$)", r"4\1."),
    (r"\b[Ee]lli\s+([1-9])\.(?=\s|[,\)]|$)", r"5\1."),
    (r"\b[Aa]ltmış\s+([1-9])\.(?=\s|[,\)]|$)", r"6\1."),
    (r"\b[Yy]etmiş\s+([1-9])\.(?=\s|[,\)]|$)", r"7\1."),
    (r"\b[Ss]eksen\s+([1-9])\.(?=\s|[,\)]|$)", r"8\1."),
    (r"\b[Dd]oksan\s+([1-9])\.(?=\s|[,\)]|$)", r"9\1."),
    (r"\b[Oo]n\s+1\.'si\b", "11.'si"),
    (r"\b[Oo]n\s+2\.'si\b", "12.'si"),
    (r"\b[Oo]n\s+3\.'sü\b", "13.'sü"),
    (r"\b[Oo]n\s+4\.'sü\b", "14.'sü"),
    (r"\b[Oo]n\s+5\.'si\b", "15.'si"),
]

def tr_sayi_eki(num: int, ek_turu: str) -> str:
    last_digit = num % 10
    last_ten = num % 100
    
    if last_digit == 0:
        if last_ten == 0 or num == 0:
            ses = 'u' if num == 0 else 'ü'
            sert = True if num != 0 else False
        elif last_ten == 10: ses, sert = 'o', False
        elif last_ten == 20: ses, sert = 'i', False
        elif last_ten == 30: ses, sert = 'u', False
        elif last_ten == 40: ses, sert = 'ı', True
        elif last_ten == 50: ses, sert = 'i', False
        elif last_ten == 60: ses, sert = 'ı', True
        elif last_ten == 70: ses, sert = 'i', False
        elif last_ten == 80: ses, sert = 'e', False
        elif last_ten == 90: ses, sert = 'a', False
    else:
        if last_digit == 1: ses, sert = 'i', False
        elif last_digit == 2: ses, sert = 'i', False
        elif last_digit == 3: ses, sert = 'ü', True
        elif last_digit == 4: ses, sert = 'ü', True
        elif last_digit == 5: ses, sert = 'e', True
        elif last_digit == 6: ses, sert = 'ı', False
        elif last_digit == 7: ses, sert = 'i', False
        elif last_digit == 8: ses, sert = 'e', False
        elif last_digit == 9: ses, sert = 'u', False

    ince = ses in ('e', 'i', 'ö', 'ü')
    e_a = 'e' if ince else 'a'
    i_ı_u_ü = 'i' if ses in ('i', 'e') else ('ü' if ses == 'ü' else ('u' if ses in ('u', 'o') else 'ı'))
    d_t = 't' if sert else 'd'

    if ek_turu == 'de':
        return f"'{d_t}{e_a}"
    elif ek_turu == 'den':
        return f"'{d_t}{e_a}n"
    elif ek_turu == 'e':
        y = 'y' if last_digit in (2, 6, 7) or (last_digit == 0 and last_ten in (20, 50)) else ''
        return f"'{y}{e_a}"
    elif ek_turu == 'i':
        y = 'y' if last_digit in (2, 6, 7) or (last_digit == 0 and last_ten in (20, 50)) else ''
        return f"'{y}{i_ı_u_ü}"
    elif ek_turu == 'si':
        s = 's' if last_digit in (2, 6, 7) or (last_digit == 0 and last_ten in (20, 50)) else ''
        return f"'{s}{i_ı_u_ü}"
    elif ek_turu == 'in':
        n = 'n' if last_digit in (2, 6, 7) or (last_digit == 0 and last_ten in (20, 50)) else ''
        return f"'{n}{i_ı_u_ü}n"
    elif ek_turu == 'dir':
        return f"'{d_t}{i_ı_u_ü}r"
    elif ek_turu == 'lik':
        return f"'l{i_ı_u_ü}k"
    elif ek_turu == 'le':
        y = 'y' if last_digit in (2, 6, 7) or (last_digit == 0 and last_ten in (20, 50)) else ''
        return f"'{y}l{e_a}"
    elif ek_turu == 'ler':
        return f"'l{e_a}r"
    elif ek_turu == 'li':
        return f"'l{i_ı_u_ü}"
    return ""

SAYI_PARSE = {
    'sıfır': 0, 'bir': 1, 'iki': 2, 'üç': 3, 'dört': 4, 'beş': 5, 'altı': 6, 'yedi': 7, 'sekiz': 8, 'dokuz': 9,
    'on': 10, 'yirmi': 20, 'otuz': 30, 'kırk': 40, 'elli': 50, 'altmış': 60, 'yetmiş': 70, 'seksen': 80, 'doksan': 90,
}

EK_SESLERI = {
    'de': 'de', 'da': 'de', 'te': 'de', 'ta': 'de',
    'den': 'den', 'dan': 'den', 'ten': 'den', 'tan': 'den',
    'ye': 'e', 'ya': 'e', 'e': 'e', 'a': 'e',
    'yi': 'i', 'yı': 'i', 'yu': 'i', 'yü': 'i', 'i': 'i', 'ı': 'i', 'u': 'i', 'ü': 'i',
    'dir': 'dir', 'dır': 'dir', 'tir': 'dir', 'tır': 'dir', 'tür': 'dir', 'dür': 'dir',
    'nin': 'in', 'nın': 'in', 'nun': 'in', 'nün': 'in', 'in': 'in', 'ın': 'in', 'un': 'in', 'ün': 'in',
    'si': 'si', 'sı': 'si', 'su': 'si', 'sü': 'si',
    'lik': 'lik', 'lık': 'lik', 'luk': 'lik', 'lük': 'lik',
    'le': 'le', 'la': 'le', 'yle': 'le', 'yla': 'le',
    'ler': 'ler', 'lar': 'ler', 'lerde': 'ler', 'larda': 'ler',
    'li': 'li', 'lı': 'li', 'lu': 'li', 'lü': 'li',
}

SUFFIX_MAP = {
    # 1
    'bir': ('', 1), 'biri': ("'i", 1), 'birin': ("'in", 1), 'birine': ("'ine", 1), 'birini': ("'ini", 1),
    'birinde': ("'inde", 1), 'birinden': ("'inden", 1), 'birdir': ("'dir", 1), 'birden': ("'den", 1), 'birlik': ("'lik", 1),
    # 2
    'iki': ('', 2), 'ikisi': ("'si", 2), 'ikisinin': ("'sinin", 2), 'ikisine': ("'sine", 2), 'ikisini': ("'sini", 2),
    'ikisinde': ("'sinde", 2), 'ikisinden': ("'sinden", 2), 'ikidir': ("'dir", 2), 'ikiden': ("'den", 2), 'ikilik': ("'lik", 2), 'ikiye': ("'ye", 2),
    # 3
    'üç': ('', 3), 'üçü': ("'ü", 3), 'üçün': ("'ün", 3), 'üçüne': ("'üne", 3), 'üçünü': ("'ünü", 3),
    'üçünde': ("'ünde", 3), 'üçünden': ("'ünden", 3), 'üçtür': ("'tür", 3), 'üçten': ("'ten", 3), 'üçlük': ("'lük", 3), 'üçe': ("'e", 3),
    # 4
    'dört': ('', 4), 'dördü': ("'ü", 4), 'dördün': ("'ün", 4), 'dördüne': ("'üne", 4), 'dördünü': ("'ünü", 4),
    'dördünde': ("'ünde", 4), 'dördünden': ("'ünden", 4), 'dörttür': ("'tür", 4), 'dörtten': ("'ten", 4), 'dörtlük': ("'lük", 4), 'dörde': ("'e", 4),
    # 5
    'beş': ('', 5), 'beşi': ("'i", 5), 'beşin': ("'in", 5), 'beşine': ("'ine", 5), 'beşini': ("'ini", 5),
    'beşinde': ("'inde", 5), 'beşinden': ("'inden", 5), 'beştir': ("'tir", 5), 'beşten': ("'ten", 5), 'beşlik': ("'lik", 5), 'beşle': ("'le", 5), 'beşe': ("'e", 5),
    # 6
    'altı': ('', 6), 'altısı': ("'sı", 6), 'altısının': ("'sının", 6), 'altısına': ("'sına", 6), 'altısını': ("'sını", 6),
    'altısında': ("'sında", 6), 'altısından': ("'sından", 6), 'altıdır': ("'dır", 6), 'altıdan': ("'dan", 6), 'altılık': ("'lık", 6), 'altıya': ("'ya", 6),
    # 7
    'yedi': ('', 7), 'yedisi': ("'si", 7), 'yedisinin': ("'sinin", 7), 'yedisine': ("'sine", 7), 'yedisini': ("'sini", 7),
    'yedisinde': ("'sinde", 7), 'yedisinden': ("'sinden", 7), 'yedidir': ("'dir", 7), 'yediden': ("'den", 7), 'yedilik': ("'lik", 7), 'yediye': ("'ye", 7),
    # 8
    'sekiz': ('', 8), 'sekizi': ("'i", 8), 'sekizinin': ("'inin", 8), 'sekizine': ("'ine", 8), 'sekizini': ("'ini", 8),
    'sekizinde': ("'inde", 8), 'sekizinden': ("'inden", 8), 'sekizdir': ("'dir", 8), 'sekizden': ("'den", 8), 'sekizlik': ("'lik", 8), 'sekize': ("'e", 8),
    # 9
    'dokuz': ('', 9), 'dokuzu': ("'u", 9), 'dokuzunun': ("'unun", 9), 'dokuzuna': ("'una", 9), 'dokuzunu': ("'unu", 9),
    'dokuzunda': ("'unda", 9), 'dokuzundan': ("'undan", 9), 'dokuzdur': ("'dur", 9), 'dokuzdan': ("'dan", 9), 'dokuzluk': ("'luk", 9), 'dokuza': ("'a", 9),
}

NW = r"(?:sıfır|bir|iki|üç|dört|beş|altı|yedi|sekiz|dokuz|on|yirmi|otuz|kırk|elli|altmış|yetmiş|seksen|doksan)[a-zçğıöşü]*"

def parse_turkce_sayi_ve_ek(kelime_dizisi: str):
    parcalar = kelime_dizisi.strip().split()
    if not parcalar:
        return None, ""
    toplam = 0
    ek = ""
    for i, p in enumerate(parcalar):
        kok = None
        bulunan_ek = ""
        for s, val in sorted(SAYI_PARSE.items(), key=lambda x: len(x[0]), reverse=True):
            if p == s:
                kok = s
                break
            elif p.startswith(s):
                kalan = p[len(s):]
                if kalan in EK_SESLERI:
                    kok = s
                    bulunan_ek = EK_SESLERI[kalan]
                    break
        if kok is None:
            return None, ""
        toplam += SAYI_PARSE[kok]
        if bulunan_ek:
            ek = bulunan_ek
    return toplam, ek

ABBRS = {'dr', 'prof', 'vb', 'vs', 'bkz', 'ör', 'örn', 'no', 'mr', 'mrs', 'ms', 'st'}

def cumleleri_satirlara_bol(para: str) -> str:
    tokens = re.split(r'(?<=[.!?…])\s+', para)
    merged = []
    for t in tokens:
        if not merged:
            merged.append(t)
            continue
        prev = merged[-1]
        last_word = prev.split()[-1].lower().rstrip('.!?…') if prev.split() else ''
        if last_word in ABBRS or (len(last_word) == 1 and last_word.isalpha()) or re.search(r'\b\d+\.$', prev):
            merged[-1] = prev + ' ' + t
        else:
            merged.append(t)
    return '\n'.join(merged)

def temizle(metin: str) -> str:
    # 1. Sabit terimler
    for pat, rep in TERIMLER:
        metin = re.sub(pat, rep, metin)

    # 2. On 1. / On 2. / On 3. -> 11. / 12. / 13.
    for pat, rep in ONLU_ORDINAL:
        metin = re.sub(pat, rep, metin)

    # 3. Yıllar (1700 - 2035)
    metin = re.sub(r"\bbin\s+dokuz\s+yüz\s+ellili\b", "1950'li", metin, flags=re.IGNORECASE)
    metin = re.sub(r"\bbin\s+dokuz\s+yüz\s+ellilerde\b", "1950'lerde", metin, flags=re.IGNORECASE)
    metin = re.sub(r"\bbin\s+dokuz\s+yüz\s+kırklarda\b", "1940'larda", metin, flags=re.IGNORECASE)
    metin = re.sub(r"\bbin\s+dokuz\s+yüz\s+altmışlarda\b", "1960'larda", metin, flags=re.IGNORECASE)
    metin = re.sub(r"\bbin\s+dokuz\s+yüz\s+yetmişlerde\b", "1970'lerde", metin, flags=re.IGNORECASE)
    metin = re.sub(r"\bbin\s+dokuz\s+yüz\s+seksenlerde\b", "1980'lerde", metin, flags=re.IGNORECASE)
    metin = re.sub(r"\bbin\s+dokuz\s+yüz\s+doksanlarda\b", "1990'larda", metin, flags=re.IGNORECASE)

    def yil_rep(m):
        base = m.group(1).lower()
        rest = m.group(2)
        if 'sekiz' in base: yil_taban = 1800
        elif 'dokuz' in base: yil_taban = 1900
        elif 'yedi' in base: yil_taban = 1700
        elif 'iki' in base: yil_taban = 2000
        else: return m.group(0)
        
        if not rest:
            m_ek = re.search(r"(de|da|te|ta|den|dan|ten|tan|e|a)$", base)
            ek = EK_SESLERI.get(m_ek.group(1), '') if m_ek else ''
            suf = tr_sayi_eki(yil_taban, ek) if ek else ""
            return f"{yil_taban}{suf}"

        val, ek = parse_turkce_sayi_ve_ek(rest.lower())
        if val is not None:
            tam_yil = yil_taban + val
            suf = tr_sayi_eki(tam_yil, ek) if ek else ""
            return f"{tam_yil}{suf}"
        return m.group(0)

    pat_yil = rf"\b(bin\s+dokuz\s+yüz|bin\s+sekiz\s+yüz|bin\s+yedi\s+yüz|iki\s+bin)(?:\s+({NW}(?:\s+{NW})?))?\b"
    metin = re.sub(pat_yil, yil_rep, metin, flags=re.IGNORECASE)

    # 4. Yüzde birleştirmeleri:
    def pct_comp_rep(m):
        base = int(m.group(1))
        w = m.group(2).lower()
        if w in SUFFIX_MAP and SUFFIX_MAP[w] is not None:
            suf, d = SUFFIX_MAP[w]
            return f"%{base + d}{suf}"
        return m.group(0)
    metin = re.sub(r"%([1-9]0)\s+([a-zçğıöşü]+)", pct_comp_rep, metin)

    # %2 virgül altısı -> %2,6'sı
    metin = re.sub(r"%(\d+)\s+virgül\s+([a-zçğıöşü0-9]+)", lambda m: f"%{m.group(1)},{SUFFIX_MAP.get(m.group(2).lower(), (m.group(2), 0))[1] or m.group(2)}", metin)

    # 5. Kalan 'yüzde <sayı>' ifadeleri:
    def yuzde_word_rep(m):
        rest = m.group(1).lower().strip()
        if rest in ('kelebek', 'kabarık', 'kıllanma', 'yaygın', 'akciğer', 'beyin', 'ödem', 'lezyon', 'döküntü'):
            return m.group(0)
        
        m_virgul = re.match(r"^sıfır\s+virgül\s+([a-zçğıöşü0-9]+)", rest)
        if m_virgul:
            kalan = m_virgul.group(1)
            v = SUFFIX_MAP.get(kalan, ('', SAYI_PARSE.get(kalan, kalan)))[1]
            return f"%0,{v}"

        val, ek = parse_turkce_sayi_ve_ek(rest)
        if val is not None and val <= 100:
            suf = tr_sayi_eki(val, ek) if ek else ""
            return f"%{val}{suf}"
        return m.group(0)

    pat_yuzde = rf"\byüzde\s+({NW}(?:\s+{NW})?)\b"
    metin = re.sub(pat_yuzde, yuzde_word_rep, metin, flags=re.IGNORECASE)

    # 6. Sayı + zaman / ölçü / kromozom birimleri:
    def sayi_birim_rep(m):
        sayi_metin = m.group(1).lower()
        birim = m.group(2)
        val, ek = parse_turkce_sayi_ve_ek(sayi_metin)
        if val is not None:
            suf = tr_sayi_eki(val, ek) if ek else ""
            return f"{val}{suf} {birim}"
        return m.group(0)

    BIRIMLER = r"(?:saat|saatte|saatlik|saatteki|saatin|dakika|dakikada|dakikalık|hafta|haftada|haftalık|haftaya|gün|günde|günlük|günden|yıl|yılda|yıllık|yıldan|ay|ayda|aylık|kromozom|kromozomlu|kromozomun|kromozomda|derece|derecelik|miligram|mililitre|santimetre|milimetre|yaş|yaşında|yaşındaki|kat|katı|katına|katından|kez|defa|sefer)"
    pat_birim = rf"\b({NW}(?:\s+{NW})?)\s+({BIRIMLER})\b"
    metin = re.sub(pat_birim, sayi_birim_rep, metin, flags=re.IGNORECASE)

    # 7. Belirli tarihler ve sayılar
    metin = re.sub(r"\bdokuz\s+yüz\s+seksen\b", "980", metin, flags=re.IGNORECASE)
    metin = re.sub(r"\bbin\s+otuz\s+yedi\b", "1037", metin, flags=re.IGNORECASE)
    metin = re.sub(r"\bbir\s+buçuk\b", "1,5", metin, flags=re.IGNORECASE)
    metin = re.sub(r"\büç\s+buçuk\b", "3,5", metin, flags=re.IGNORECASE)
    metin = re.sub(r"\byedi\s+buçuk\b", "7,5", metin, flags=re.IGNORECASE)

    # 8. Sıra sayıları: '1.'si .. 10.'su'
    metin = re.sub(r"\bbirincisi\b", "1.'si", metin, flags=re.IGNORECASE)
    metin = re.sub(r"\bikincisi\b", "2.'si", metin, flags=re.IGNORECASE)
    metin = re.sub(r"\büçüncüsü\b", "3.'sü", metin, flags=re.IGNORECASE)
    metin = re.sub(r"\bdördüncüsü\b", "4.'sü", metin, flags=re.IGNORECASE)
    metin = re.sub(r"\bbeşincisi\b", "5.'si", metin, flags=re.IGNORECASE)

    # 9. Paragraf içindeki cümleleri yeni satırlara ayırma
    paragraflar = metin.split('\n\n')
    yeni_paragraflar = []
    for p in paragraflar:
        p_strip = p.strip()
        if not p_strip or p_strip.startswith('@@') or p_strip.startswith('#'):
            yeni_paragraflar.append(p)
            continue
        yeni_p = cumleleri_satirlara_bol(p_strip)
        yeni_paragraflar.append(yeni_p)

    return '\n\n'.join(yeni_paragraflar)

def remap_range(matcher, s: int, e: int, new_len: int):
    def map_pos(pos):
        for a, b, size in matcher.get_matching_blocks():
            if a <= pos < a + size:
                return b + (pos - a)
            elif pos < a:
                return b
        last_block = matcher.get_matching_blocks()[-1]
        return last_block.b
    ns, ne = map_pos(s), map_pos(e)
    return max(0, min(new_len, ns)), max(0, min(new_len, ne))

def remap_vurgu(orig_md: str, yeni_md: str, vurgu_obj: dict) -> dict:
    o_paras = [p for p in orig_md.split('\n\n') if p.strip() and not p.strip().startswith('@@')]
    y_paras = [p for p in yeni_md.split('\n\n') if p.strip() and not p.strip().startswith('@@')]
    
    yeni_vurgu = {'surum': vurgu_obj.get('surum', 1), 'p': {}}
    
    for pi in range(min(len(o_paras), len(y_paras))):
        o_p = o_paras[pi]
        y_p = y_paras[pi]
        sm = difflib.SequenceMatcher(None, o_p, y_p)
        items = vurgu_obj.get('p', {}).get(str(pi), [])
        yeni_items = []
        for it in items:
            ns, ne = remap_range(sm, it[0], it[1], len(y_p))
            if ne > ns:
                yeni_items.append([ns, ne] + it[2:])
        if yeni_items:
            yeni_vurgu['p'][str(pi)] = yeni_items
            
    return yeni_vurgu

if __name__ == "__main__":
    files = sorted(glob.glob(str(METIN_DIR / "*.md")))
    toplam_degisiklik = 0
    apply_changes = "--apply" in sys.argv

    for f in files:
        key = Path(f).stem
        orig = open(f, encoding="utf-8").read()
        yeni = temizle(orig)
        if orig != yeni:
            toplam_degisiklik += 1
            if apply_changes:
                open(f, "w", encoding="utf-8").write(yeni)
                # Vurgu dosyasını yeniden eşle
                v_path = VURGU_DIR / f"{key}.json"
                if v_path.exists():
                    try:
                        v_obj = json.load(open(v_path, encoding="utf-8"))
                        yeni_v = remap_vurgu(orig, yeni, v_obj)
                        json.dump(yeni_v, open(v_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
                    except Exception as e:
                        print(f"Hata vurgu eşleme {key}: {e}")

    print(f"Bitti. Toplam dosya: {len(files)}, güncellenen dosya: {toplam_degisiklik} (apply={apply_changes})")
