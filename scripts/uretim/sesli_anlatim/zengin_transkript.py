#!/usr/bin/env python3
"""Zengin transkript modeli (v1) — sesli ders metnini türlü bloklara ayırır (kullanıcı kararı 2026-11-17).

LLM/ağ/GPU yok; yalnız kural tabanlı betik (token harcamaz). Girdi: data/sesli_anlatim/metin/<key>.md (+ varsa terim katmanı).
Çıktı: src/data/zengin_transkript/<key>.json — ön yüzde "Zengin" üslupla PDF/Word/Markdown'a dönüşür
(canliDersDisaAktar.ts → zenginBolumler). Eski "not"/"konuşma" üslupları bu dosyaya hiç dokunmaz.

Blok türleri (alan t):
  giris      bölümün açılış cümlesi (kavram/çerçeve)
  madde      bilgi maddesi; sv 1 = paragrafın ilk bilgi cümlesi (ana madde), sv 2 = aynı paragrafın sonraki cümleleri;
             anahtar = cümlenin tanımladığı kavram ("Enürezis, …" → Enürezis), varsa
  aciklama   önceki maddeyi açan/bağlayan cümle (Bu/Böylece/Çünkü…; 3. düzey)
  liste      sayım cümlesi: {bas, ogeler[]} → ana madde + alt maddeler
  sirali     sıra/basamak cümlesi: {bas, ogeler[]} → numaralı liste
  tablo      ≥3 "yüzde/oran" karşılaştırması: {basliklar, satirlar}
  sinav      "çıkmış sınavda …" cümlesi → Önemli kutusu
  ornek      "Örneğin …" cümlesi → İpucu kutusu
  alinti     tırnak içi ifade → alıntı
  terim      bölümde ilk geçen terim: {ad, tanim} (terim katmanından)
Her blokta p = metindeki boş olmayan paragrafın sırası (0'dan; ara resimleri doğru yere koymak için).

  python3 scripts/uretim/sesli_anlatim/zengin_transkript.py <key|k2-50> [...]  |  --kurul 2 [--yeni-gun 14]  |  --dogrula <key>
"""
from __future__ import annotations

import argparse
import ast
import datetime as dt
import json
import re
import sys
from pathlib import Path

_d = Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
sys.path.append(str(_d))
import kok as _kok  # noqa: E402

KOK = _kok.MEDS
METIN = KOK / "data" / "sesli_anlatim" / "metin"
TERIM = KOK / "data" / "sesli_anlatim" / "terim"
CIKTI = KOK / "src" / "data" / "zengin_transkript"
SURUM = 2  # v2: iç içe madde (sv 1–3: paragrafın ilk cümlesi ana madde, sonrakiler alt madde, açıklama 3. düzey) + anahtar
TURLER = {"giris", "madde", "aciklama", "liste", "sirali", "tablo", "sinav", "ornek", "alinti", "terim"}

CUMLE = re.compile(r"(?<=[.!?…])\s+(?=[A-ZÇĞİÖŞÜ0-9“\"(])")
SIRA = [r"\bönce\b", r"\bardından\b", r"\bsonra(sında)?\b", r"\ben sonunda\b", r"\bson olarak\b", r"\bilk sırada\b",
        r"\bikinci sırada\b", r"\büçüncü\b", r"\bbirinci\b", r"\bikinci\b", r"\bbasamak", r"\başama"]
BAGLAC = re.compile(r"^(Bu |Böylece|Dahası|Ayrıca|Bu nedenle|Bu yüzden|Yani|Başka deyişle|Bununla birlikte|Ancak|Oysa|Çünkü)")
SAYIM = re.compile(r"\b(sayılır|şunlardır|yer alır|gelir|eklenir|istenir|bulunur|içerir)\b")


def cumleler(p: str) -> list[str]:
    return [c.strip() for c in CUMLE.split(p.strip()) if c.strip()]


SAYI_AD = {"iki": 2, "üç": 3, "dört": 4, "beş": 5, "altı": 6, "yedi": 7, "sekiz": 8, "dokuz": 9, "on": 10}


def sayiyla_ayir(bas: str, govde: str) -> list[str] | None:
    """Başlık sayı söylüyorsa ("üç bulgu", "dördü") öğe sayısı tutmalı: önce son 've' bölünerek, tutmazsa bölünmeden denenir;
    ikisi de tutmazsa None (liste kurulmaz). Sayı yoksa normal bölme."""
    m = re.search(r"\b(iki|üç|dört|beş|altı|yedi|sekiz|dokuz|on)(?:\s|[ıiuü]|ü|sü|si|ü\b|$)", bas.lower())
    og = _ayir_oge(govde)
    if not m:
        return og
    n = SAYI_AD[m.group(1)]
    if len(og) == n:
        return og
    duz = [x.strip(" .;:") for x in re.split(r",\s*", govde) if 2 <= len(x.strip()) <= 140]
    return duz if len(duz) == n else None


def _ayir_oge(govde: str) -> list[str]:
    """'a, b, c ve d' → [a, b, c, d]: yalnız virgüller ve SON 've/ya da' bölünür ("uyku ile uyanıklık düzeni" bütün kalır)."""
    parca = [x.strip() for x in re.split(r",\s*", govde) if x.strip()]
    # öğeler zaten "X ve Y" çiftiyse son 've' de çiftin parçasıdır, bölünmez
    if parca and not any(re.search(r"\s(?:ve|ya da|veya)\s", x) for x in parca[:-1]):
        son = re.split(r"\s+(?:ve|ya da|veya)\s+(?!.*\s(?:ve|ya da|veya)\s)", parca[-1], maxsplit=1)
        parca = parca[:-1] + [x for x in son if x.strip()]
    return [x.strip(" .;:") for x in parca if 2 <= len(x.strip()) <= 140]


BAG_SOZ = {"ve", "ile", "ya", "da", "de", "önce", "öncelikle", "ardından", "sonra", "sonrasında", "daha", "en", "sonunda", "sonda",
           "son", "olarak", "ilk", "birincisi", "ilki", "ise", "gelir", "gelişir", "görülür", "izlenir", "ikincisi", "üçüncüsü", "dördüncüsü", "beşincisi", "altıncısı", "sonuncusu",
           "sayılır", "şunlardır", "yer", "alır", "gelir", "eklenir", "istenir", "bulunur", "içerir", "gelişir", "başlar"}


YUKLEM = re.compile(r"(?:[dt][ıiuü]r|[ıiuü]yor|m[ae]z|[^l\s][ae]r|[ıiuü]r|abilir|ebilir|m[ıiuü]ş)$")


def ogeler_ad_mi(og: list[str]) -> bool:
    """Liste öğeleri ad öbeği mi? Yüklemle biten öğe ("kişiye konur", "öndedir") cümle parçasıdır, liste kurulmaz."""
    return all((not YUKLEM.search(x.split()[-1].lower()) or len(x.split()[-1]) <= 3) and not re.match(r"^(ve|ya da|veya|yani|ise)\b", x)
               for x in og if x.split())


def kapsar(c: str, parcalar: list[str]) -> bool:
    """Yapı cümlenin bilgi sözcüklerini kaybetmiyor mu (≥ %95)? Kaybediyorsa yapı kurulmaz, cümle madde kalır."""
    sz = lambda t: [w for w in re.findall(r"[\wçğıöşüÇĞİÖŞÜ]+", t.lower()) if len(w) > 2 and w not in BAG_SOZ]
    asil, yeni = sz(c), set(sz(" ".join(parcalar)))
    return not asil or sum(w in yeni for w in asil) / len(asil) >= 0.95


ZAMAN_IS = r"(?:\b[Öö]nce(?:likle)?\b|\bilk olarak\b|\bardından\b|\bdaha sonra\b|\bsonra(?:sında)?\b|\ben sonunda\b|\ben sonda\b|\ben son\b|\bson olarak\b|\bsonunda\b)"
SIRA_SOZ = re.compile(r"\b(basamak|aşama|evre|adım|sıra|sırasıyla|sırayla|kademe)", re.I)


def sirali_mi(c: str) -> tuple[str, list[str], str] | None:
    """Tek cümlede sıralama → (başlık, adımlar, kalan). Kalan (';' sonrası) metin kaybolmasın diye açıklama olarak eklenir.
      · zaman işaretli: 'Sıra şöyle: önce A, sonra B, sonra C, en sonda D.' (başlangıç işareti + ≥ 2 sonraki işaret)
      · sıra sayılı: 'Birincisi A, ikincisi B, üçüncüsü C.' / 'İlki A, ikincisi B'
      · basamak sayımı: 'Üç aşamada ilerler: A, B ve C.' / 'Basamaklar sırasıyla A, B ve C'dir.'
    Her yapıda cümle sözcüklerinin ≥ %95'i korunur (kapsar), yoksa None."""
    ana, _, kalan = c.partition(";")
    kalan = kalan.strip()
    # 1) sıra sayılı tek cümle
    if re.search(r"\b(birincisi|ilki)\b", ana, re.I) and re.search(r"\bikincisi\b", ana, re.I):
        bol = re.split(r",?\s*\b(?:[Bb]irincisi|[İi]lki|ikincisi|üçüncüsü|dördüncüsü|beşincisi|altıncısı|sonuncusu)\b\s*,?\s*", ana)
        bas, og = bol[0].strip(" ,:"), [x.strip(" ,.;") for x in bol[1:] if x.strip(" ,.;")]
        if len(og) >= 2 and kapsar(ana, [bas, *og]):
            return bas, _sira_temiz(og), kalan
    # 1b) tek cümlede "Birinci aşama A, ikinci aşama B …" — sıra sözcüğü adımın içinde kalır (metin kaybı yok)
    tam = c.replace("İ", "i").replace("I", "ı")
    if re.match(r"^(birinci|ilk)\s+\w+", tam, re.I) and re.search(r"[,;]\s*ikinci\s+\w+", tam, re.I):
        bol = re.split(r"[,;]\s*(?=(?:ikinci|üçüncü|dördüncü|beşinci|altıncı)\s)", c.replace("İkinci", "ikinci"))
        og = [x.strip(" .") for x in bol if x.strip(" .")]
        if len(og) >= 2 and all(len(x.split()) <= 25 for x in og):
            return "", og, ""
    # 2) zaman işaretli
    isaret = re.findall(ZAMAN_IS, ana, re.I)
    if len(isaret) >= 3 and re.search(r"\b(önce|öncelikle|ilk olarak)\b", ana, re.I):
        gb = re.match(r"^(.{0,120}?:)\s*", ana)
        govde = ana[gb.end():] if gb else ana
        bol = re.split(r",?\s*" + ZAMAN_IS + r"\s*,?\s*", govde)
        bas = ((gb.group(1) if gb else "") + " " + bol[0]).strip(" ,") if bol[0].strip() and len(bol[0].split()) <= 8 else (gb.group(1) if gb else "")
        govde_og = bol[1:] if bol[0].strip() and len(bol[0].split()) <= 8 else bol
        og = [re.sub(r"\s+(ve|ile)$", "", x.strip(" ,.;")) for x in govde_og if x.strip(" ,.;")]
        if len(og) >= 3 and kapsar(ana, [bas, *og]):
            return bas, _sira_temiz(og), kalan
    # 3) basamak sayımı (iki nokta ya da 'sırasıyla')
    m = re.match(r"^([^:]{6,140}?)(?::\s+|\s+sırasıyla\s+)(.+?)[.!]?$", ana)
    # başlık sıra bildirmeli: sayılı basamak ("üç basamakta", "dört evre") ya da sıra/sırasıyla/sırayla;
    # "İkinci basamak fizik muayenedir: …" bir basamağın İÇERİĞİDİR, sıralama değildir
    sayili = re.search(r"\b(iki|üç|dört|beş|altı|yedi|sekiz)\s+(basamak|aşama|evre|adım|kademe)", m.group(1), re.I) if m else None
    sira = re.search(r"\b(sıra|sırasıyla|sırayla)\b", m.group(1) + (" sırasıyla" if m and "sırasıyla" in ana else ""), re.I) if m else None
    if m and (sayili or sira) and not re.match(r"^(İkinci|Üçüncü|Dördüncü|Beşinci|Birinci|İlk)\b", m.group(1)):
        og = sayiyla_ayir(m.group(1), re.sub(r"(?:'?[dt][ıiuü]r)$", "", m.group(2))) or []
        if len(og) >= 3 and all(len(x.split()) <= 12 for x in og) and ogeler_ad_mi(og[:-1]) and kapsar(ana, [m.group(1), *og]):
            return m.group(1).strip() + ("" if ":" in ana else " (sırasıyla)"), _sira_temiz(og), kalan
    return None


def _sira_temiz(og: list[str]) -> list[str]:
    """Adımın başındaki bağlaç (da/de/ise/ve) ve son adımın sonundaki genel yüklem (gelir, gelişir, görülür…) atılır."""
    og = [re.sub(r"^(?:da|de|ise|ve|ve de)\s+", "", x).strip() for x in og]
    if og:
        og[-1] = re.sub(r"\s+(gelir|gelişir|görülür|izlenir|başlar|kazanılır|yapılır|uygulanır)$", "", og[-1])
    return [x for x in og if x]


def sira_dizileri(B: list[dict]) -> list[dict]:
    """Art arda 'Birinci… / İkinci… / Üçüncü…' ile başlayan madde cümlelerini (aynı bölüm, ≥ 2, birinciden başlayan)
    tek sıralama bloğuna toplar; adımlar cümlenin tamamıdır (metin kaybı yok)."""
    SIRA = ["birinci", "ilk", "ikinci", "üçüncü", "dördüncü", "beşinci", "altıncı", "yedinci", "sekizinci", "dokuzuncu", "onuncu"]
    def no(b: dict) -> int:
        if b.get("t") != "madde":
            return -1
        # Türkçe büyük İ: str.lower() "i̇" (birleşik nokta) üretir, "ikinci" ile eşleşmez → önce İ→i, I→ı
        w = re.match(r"^(\w+)", (b.get("x") or "").replace("İ", "i").replace("I", "ı").lower())
        w = w.group(1) if w else ""
        for i, k in enumerate(SIRA):
            if w.startswith(k):
                return 1 if i <= 1 else i
        return -1
    out, i = [], 0
    while i < len(B):
        if no(B[i]) == 1:
            j, beklenen = i + 1, 2
            while j < len(B) and (no(B[j]) == beklenen or B[j]["t"] in ("terim", "aciklama")):
                if no(B[j]) == beklenen:
                    beklenen += 1
                j += 1
            adim = [b for b in B[i:j] if b["t"] == "madde"]
            if len(adim) >= 2:
                out.append({"t": "sirali", "bas": "", "ogeler": [b["x"] for b in adim], "p": B[i]["p"]})
                out += [b for b in B[i:j] if b["t"] != "madde"]  # terim/açıklama kaybolmaz, dizinin ardına
                i = j
                continue
        # önceki sıralamanın devamı: n. sıra sözcüğüyle başlayan cümle, n−1 adımlı sıralamanın ardından gelir
        n = no(B[i])
        onceki = next((b for b in reversed(out) if b["t"] not in ("terim", "aciklama")), None)
        if n > 1 and onceki is not None and onceki["t"] == "sirali" and len(onceki["ogeler"]) == n - 1:
            # devam cümlesi kendi içinde sonraki sırayı da taşıyabilir ("Üçüncü aşama …; dördüncü aşama …")
            onceki["ogeler"] += [x.strip(" .") for x in re.split(r"[,;]\s*(?=(?:dördüncü|beşinci|altıncı|yedinci)\s)", B[i]["x"]) if x.strip(" .")]
            i += 1
            continue
        out.append(B[i])
        i += 1
    return out


def liste_mi(c: str) -> tuple[str, list[str]] | None:
    """Sayım cümlesi: 'X'in başında A, B ve C gelir.' / 'Nedenler arasında A, B ve C sayılır.' /
    'Üç aile tanımlanmıştır: A, B ve C.' (iki noktadan sonra yalnız kısa öğeler, her biri ≤ 6 sözcük)"""
    ik = re.match(r"^([^:;]{8,160}):\s+([^:;]+?)[.!]?$", c)
    if ik:
        og = sayiyla_ayir(ik.group(1), ik.group(2)) or []
        if len(og) >= 3 and all(len(x.split()) <= 14 for x in og) and ogeler_ad_mi(og) and kapsar(c, [ik.group(1), *og]):
            return ik.group(1).strip(), og
    # Özne + sayım + koşaç: "Nontravmatik nedenler enfeksiyon, transvers miyelit, tümör ve nörodejeneratif hastalıklardır."
    # Özne bir grup adı (çoğul: nedenler, bulgular, etmenler…) ya da "X açısından/için/arasında" çerçevesi olmalı.
    GRUP = (r"(?:neden|bulgu|belirti|etmen|faktör|örnek|tip|grup|endikasyon|komplikasyon|özellik|bileşen|etki|kontrendikasyon|"
            r"seçenek|yöntem|ölçüt|kriter|evre|sınıf|tür|çeşit|kaynak|amaç|hedef|ilke|basamak|risk|sonuç|türev|üye)")
    oz = re.match(rf"^(?P<bas>(?:[^\s,]+\s+){{0,3}}?[^\s,]*{GRUP}(?:ler|lar)?(?:i|ı|si|sı|leri|ları)?)\s+(?P<govde>[^:;]+?)[.!]?$", c, re.I)
    if oz and (re.search(r"(?:lerin|ların|nin|nın)$", oz.group("bas")) or re.search(r"\bise\b", oz.group("bas"))
               or not re.search(r"(?:ler|lar|leri|ları|i|ı|si|sı)$", oz.group("bas"))):
        oz = None  # ilgi eki (tamlayan), "ise" ya da yalın tekil özne grup adı değildir
    if oz and oz.group("govde").count(",") >= 1 and re.search(r"\s(?:ve|ya da|veya)\s", oz.group("govde")):
        og = sayiyla_ayir(oz.group("bas"), oz.group("govde")) or []
        son = re.sub(r"(?:'?[dt][ıiuü]r)$", "", og[-1]) if og else ""  # koşaç ("hastalıklardır") ad öbeğini bozmaz
        if len(og) >= 3 and all(len(x.split()) <= 8 for x in og) and ogeler_ad_mi([*og[:-1], son]) and kapsar(c, [oz.group("bas"), *og]):
            return oz.group("bas").strip(), og
    if c.count(",") + len(re.findall(r"\s(?:ve|ile|ya da)\s", c)) < 2 or not SAYIM.search(c):
        return None
    m = re.match(r"^(.{8,90}?(?:başında|arasında|amacıyla|için|olarak|Bunlara|Bu amaçla))\s+(.*)$", c)
    if not m:
        return None
    if re.search(r"[;:]", m.group(2)) or re.search(r"\b(yüz|bin|on|yirmi|otuz|kırk|elli)\s+ile\b", m.group(1)):
        return None  # ikinci cümle parçası ya da sayı aralığı ("üç yüz ile dört yüz arasında") liste değildir
    og = sayiyla_ayir(m.group(1), SAYIM.split(m.group(2))[0]) or []
    return (m.group(1).strip(), og) if len(og) >= 3 and ogeler_ad_mi(og) and kapsar(c, [m.group(1), *og]) else None


SAYI = r"(?:sıfır|bir|iki|üç|dört|beş|altı|yedi|sekiz|dokuz|on|yirmi|otuz|kırk|elli|altmış|yetmiş|seksen|doksan|yüz)"
YUZDE = re.compile(rf"\byüzde\s+((?:{SAYI}\s+)*{SAYI})(?:[a-zçğıöşü']*)\b", re.I)
KOSUL = re.compile(r"((?:[\wçğıöşü]+\s+){0,2}[\wçğıöşü]*yaş[\wçğıöşü]*)", re.I)


def tablo_mi(c: str) -> dict | None:
    """≥3 'yüzde …' karşılaştırması → iki sütunlu tablo (koşul | oran). Her parçada hem koşul (yaş ifadesi) hem tam sayı
    sözcüğü bulunmalı; biri eksikse tablo kurulmaz (kesik sayı tablo olarak basılmaz — H609)."""
    parcalar = [x for x in re.split(r",\s*|;\s*", c) if "yüzde" in x]
    if len(parcalar) < 3:
        return None
    satir = []
    for x in parcalar:
        y, k = YUZDE.search(x), KOSUL.search(x)
        if not (y and k):
            return None
        satir.append([re.sub(r"^(?:bu\s+)?oran\s+", "", k.group(1).strip(), flags=re.I), "yüzde " + y.group(1).strip()])
    return {"basliklar": ["Durum", "Oran"], "satirlar": satir}


SAYI_KOS = re.compile(rf"(?:\byüzde\s+)?(?:\b(?:{SAYI}|\d+(?:[.,]\d+)?)\b\s*)+(?:[\wçğıöşü']*)", re.I)


def _deger_ayir(seg: str, deger_once: bool) -> tuple[str, str] | None:
    """Parçayı (koşul, değer) ikilisine ayırır. deger_once: "yüzde altmışı serebral tromboza" → (serebral tromboza, yüzde altmışı)."""
    seg = seg.strip(" .")
    if deger_once:
        m = re.match(rf"^(yüzde\s+(?:{SAYI}\s+)*{SAYI}[\wçğıöşü']*)\s+(.+)$", seg, re.I)
        return (m.group(2), m.group(1)) if m else None
    m = re.search(r"\byüzde\s", seg, re.I) or SAYI_KOS.search(seg)
    if not m or m.start() == 0:
        return None
    # sözcük silinmez (kapsar): koşul sonundaki "ise/yalnızca/ancak" değerin önüne geçer, "ise" bağlaç olarak düşer
    kosul, deger = seg[:m.start()].strip(), seg[m.start():].strip()
    ek = re.search(r"(?:\s+(?:ise|yalnızca|ancak|sadece))+$", kosul)
    if ek:
        kosul, deger = kosul[:ek.start()].strip(" ,"), (" ".join(w for w in ek.group(0).split() if w != "ise") + " " + deger).strip()
    return (kosul, deger) if kosul and len(kosul.split()) <= 8 else None


def deger_tablosu(c: str) -> dict | None:
    """Sayısal değer serisi (≥ 3 satır): 'üç yaş altında yüzde altmış altı, bir ila yirmi yaşta yüzde kırk, …' →
    Durum | Değer. Her satırda sayı olmalı; cümle sözcükleri korunmalı (kapsar)."""
    bas, _, govde = c.rpartition(": ") if re.search(r":\s", c) else ("", "", c)
    seg = [x for x in re.split(r",\s*|;\s*", govde.rstrip(" .")) if x.strip()]
    if len(seg) < 3:
        return None
    deger_once = sum(1 for x in seg[1:] if re.match(r"^yüzde\s", x.strip(), re.I)) >= 2
    if deger_once:  # ilk parçanın öznesi başlığa: "İnmelerin yüzde altmışı …" → başlık "İnmelerin"
        m = re.match(r"^(.*?)\s+(yüzde\s.+)$", seg[0], re.I)
        if not m:
            return None
        bas, seg[0] = (bas + " " + m.group(1)).strip(), m.group(2)
    ham = [_deger_ayir(x, deger_once) for x in seg]
    satir: list[tuple[str, str]] = [r for r in ham if r is not None]
    if len(satir) != len(ham) or len(satir) < 3:
        return None
    # değer gerçek nicelik olmalı: yüzde, birimli sayı ya da yalnız sayı sözcükleri ("bir şekilde", "üç yönelimin" değildir)
    BIRIM = r"(miligram|mikrogram|gram|mg|kilogram|mikrometre|milimetre|santimetre|metre|mmhg|ünite|saniye|dakika|saat|gün|hafta|ay|aylarda|ayda|yıl|yaş|kat|doz|derece)"
    def nicel(v: str) -> bool:
        v = v.lower()
        return "yüzde" in v or bool(re.search(r"\d", v)) or bool(re.search(BIRIM, v)) or \
            bool(re.fullmatch(rf"(?:(?:{SAYI}|virgül)[\wçğıöşü']*\s*)+", v.strip()))
    if not all(nicel(r[1]) for r in satir) or any(re.match(r"^(ile|ila|ve|ya)\b", r[0], re.I) for r in satir):
        return None
    if not kapsar(c, [bas, *[h for r in satir for h in r]]):
        return None
    oran = any("yüzde" in r[1].lower() for r in satir)
    return {"bas": bas.strip(), "basliklar": ["Durum", "Oran" if oran else "Değer"], "satirlar": [list(r) for r in satir]}


# Koşul cümle başında (ya da iki noktadan hemen sonra) olmalı: "A'da P, B'de ise Q". Ortadaki ilk -de/-da'yı koşul saymak
# yanlış eşleme üretiyordu ("Örnekte | … difüzyon görüntüde …").
KARSIT = re.compile(r"^(?P<on>)(?P<k1>(?:\S+\s+){0,3}?\S+(?:[dt][ae]|n[dt][ae]))\s+(?P<v1>[^;]+?),\s+"
                    r"(?P<k2>(?:\S+\s+){0,3}?\S+(?:[dt][ae]|n[dt][ae]))\s+ise\s+(?P<v2>[^;]+?)[.!]?$")


def karsitlik_tablosu(c: str) -> dict | None:
    """'X'te P, Y'de ise Q' → iki satırlı karşılaştırma tablosu (Durum | Bulgu). Ön ek ≤ 8 sözcük başlık olur."""
    ana, _, kalan = c.partition("; ")
    on_ek = ""
    if ": " in ana:  # "Ayrımı şöyle yapabilirsiniz: A'da P, B'de ise Q" → başlık iki noktadan önce
        on_ek, _, ana = ana.rpartition(": ")
    m = KARSIT.match(ana.strip())
    # "yüzde", "önce" gibi -de/-te ile biten bulunma eki olmayan sözcükler koşul değildir
    YANLIS = r"(?:yüzde|önce|sonra|halde|ayrıca|zaten|bile|hatta|şimdi|ilkönce|kadar|beri|neden|orta|örnekte|tanıda|pratikte|klinikte|genelde|aslında|sonuçta|özünde|burada|şurada|olarak\s+\S+)$"
    if not m or re.search(YANLIS, m.group("k1").lower()) or re.search(YANLIS, m.group("k2").lower()) \
            or len(m.group("v1").split()) > 20 or len(m.group("v2").split()) > 20 \
            or any(YUKLEM.search(w) for w in m.group("k2").lower().split()[:-1]) or "," in m.group("k1") + m.group("k2") \
            or re.search(r"\S+(?:[dt][ae]|n[dt][ae])\b", " ".join(m.group("v1").split()[:3])):  # çerçeve koşulu: v1 başında yeni koşul var
        return None
    satir = [[m.group("k1").strip(), m.group("v1").strip()], [m.group("k2").strip(), m.group("v2").strip()]]
    if satir[0][0].lower() == satir[1][0].lower() or ":" in satir[0][0] or not kapsar(ana, [m.group("on"), *satir[0], *satir[1]]):
        return None
    return {"bas": (on_ek + " " + m.group("on")).strip(" ,:"), "basliklar": ["Durum", "Bulgu"], "satirlar": satir, "kalan": kalan.strip()}


def kavram_tablolari(B: list[dict]) -> list[dict]:
    """Bölümde art arda tanımlanan ≥ 3 kavram (anahtarlı ana madde; arada yalnız alt madde/açıklama/terim) → Kavram | Açıklama
    tablosu. Alt madde ve açıklama cümleleri ilgili satırın hücresine eklenir; terim kartları tablonun ardına taşınır."""
    out, i = [], 0
    while i < len(B):
        if B[i]["t"] == "madde" and B[i].get("anahtar") and B[i].get("sv") == 1:
            j, satirlar, ek = i, [], []
            while j < len(B):
                b = B[j]
                if b["t"] == "madde" and b.get("anahtar") and b.get("sv") == 1:
                    a = b["anahtar"]
                    ac = b["x"][len(a):].lstrip(" ,;:").strip() if b["x"].startswith(a) else b["x"]
                    ac = re.sub(r"^ise\s+", "", ac)
                    satirlar.append([a, ac[:1].upper() + ac[1:]])
                elif b["t"] in ("aciklama",) or (b["t"] == "madde" and b.get("sv") == 2):
                    satirlar[-1][1] += " " + b["x"]
                elif b["t"] == "terim":
                    ek.append(b)
                else:
                    break
                j += 1
            if len(satirlar) >= 3 and len({r[0].lower() for r in satirlar}) == len(satirlar):
                out.append({"t": "tablo", "bas": "", "basliklar": ["Kavram", "Açıklama"], "satirlar": satirlar, "p": B[i]["p"], "x": ""})
                out += ek
                i = j
                continue
        out.append(B[i])
        i += 1
    return out


ANAHTAR = re.compile(r"^([A-ZÇĞİÖŞÜ][\wçğıöşüÇĞİÖŞÜ\-]*(?:\s+[\wçğıöşüÇĞİÖŞÜ\-]+){0,3}?)(?:,\s|\s+ise\s|;\s|:\s)")


TANIM = re.compile(r"(demektir|denir|tanımlanır|anlamına gelir|adı verilir|terimdir|olarak bilinir|olarak adlandırılır)[.!]?$")


def anahtar_bul(c: str, terim_adlari: set[str] | None = None) -> str:
    """Cümlenin başında tanımlanan kavram: en çok 4 sözcük, ardından virgül/ise/;/: ("Primer enürezis, …")."""
    m = ANAHTAR.match(c)
    if not m:
        return ""
    a = m.group(1).strip()
    # bağlaç/zamirle başlayan ya da tek harfli başlangıç kavram değildir
    if re.match(r"^(Bu|Şu|O|Bunlar|Ancak|Ayrıca|Örneğin|Yani|Böylece|Dahası|Son olarak|Ardından|Önce|Sonra|Tanı|Tedavi|İlk)\b", a):
        return ""
    # yüklem içeren başlangıç ("Yaş ölçütü önemlidir") kavram adı değildir
    if re.search(r"(?:[dt][ıiuü]r|m[ae]z|[ıiuü]yor|abilir|ebilir|[ıiuü]r|[ae]r)$", a.split()[-1]) and len(a.split()) > 1:
        return ""
    # çekimli ad (bulunma/ilgi eki: "Sekonder enüreziste", "Hastanın") kavram adı değildir
    if re.search(r"(?:[dt][ae]|n[dt][ae]|[ıiuü]n|n[ıiuü]n)$", a.split()[-1]) and len(a.split()[-1]) > 4:
        return ""
    if not 2 < len(a) <= 40:
        return ""
    # yalnız güvenilir durumlar: dersin terim katmanındaki bir terim ya da açık tanım cümlesi ("X ise …", "… demektir")
    terim = bool(terim_adlari) and a.lower() in terim_adlari
    tanim = bool(TANIM.search(c)) or bool(re.match(rf"^{re.escape(a)}\s+ise\s", c))
    return a if terim or tanim else ""


def terimler(key: str) -> dict[str, str]:
    f = TERIM / f"{key}.json"
    if not f.exists():
        return {}
    try:
        d = json.loads(f.read_text(encoding="utf-8"))
        ic = d.get("d")
        ic = ast.literal_eval(ic) if isinstance(ic, str) else ic
        out: dict[str, str] = {}
        for sayfalar in (ic or {}).values():
            for kayit in (sayfalar or {}).values():
                for t in kayit.get("t", []) if isinstance(kayit, dict) else []:
                    if t.get("t") and t.get("a") and len(t["t"]) >= 4:
                        out.setdefault(t["t"], t["a"])
        return out
    except Exception:  # noqa: BLE001 — terim katmanı isteğe bağlı
        return {}


def modelle(key: str) -> dict:
    md = (METIN / f"{key}.md").read_text(encoding="utf-8")
    trm = terimler(key)
    kullanildi: set[str] = set()
    bolumler: list[dict] = []
    baslik = ""
    p = -1
    for blok in re.split(r"\n\s*\n", md):
        satirlar = [s for s in blok.strip().splitlines() if s.strip()]
        if not satirlar:
            continue
        if satirlar[0].startswith("# ") and not baslik:
            baslik = satirlar.pop(0)[2:].strip()
        if satirlar and satirlar[0].startswith("@@"):
            bolumler.append({"baslik": satirlar.pop(0)[2:].strip(), "bloklar": []})
        if not satirlar:
            continue
        if not bolumler:
            bolumler.append({"baslik": baslik or key, "bloklar": []})
        B = bolumler[-1]["bloklar"]
        p += 1
        for c in cumleler(" ".join(satirlar)):
            ilk = not B
            if ilk:
                B.append({"t": "giris", "x": c, "p": p})
            elif re.search(r"çıkmış sınav|sınavda (doğrudan )?soru", c, re.I):
                B.append({"t": "sinav", "x": c, "p": p})
            elif re.match(r"^(Örneğin|Mesela|Sözgelimi)\b", c):
                B.append({"t": "ornek", "x": c, "p": p})
            elif (sr := sirali_mi(c)):
                B.append({"t": "sirali", "bas": sr[0], "ogeler": sr[1], "p": p})
                if sr[2]:  # ';' sonrası kalan cümle parçası açıklama olarak korunur
                    B.append({"t": "aciklama", "x": sr[2][:1].upper() + sr[2][1:], "p": p})
            elif (tb := deger_tablosu(c)):  # eski tablo_mi koşul/sayı kesiyordu (kapsamsız), kullanılmıyor
                B.append({"t": "tablo", **tb, "x": c, "p": p})
            elif (kt := karsitlik_tablosu(c)):
                kalan = kt.pop("kalan")
                B.append({"t": "tablo", **kt, "x": c, "p": p})
                if kalan:
                    B.append({"t": "aciklama", "x": kalan[:1].upper() + kalan[1:], "p": p})
            elif (ls := liste_mi(c)):
                B.append({"t": "liste", "bas": ls[0], "ogeler": ls[1], "p": p})
            elif (q := re.search(r"[“\"]([^”\"]{8,200})[”\"]", c)):
                B.append({"t": "alinti", "x": c, "alinti": q.group(1), "p": p})  # x = cümlenin tamamı (metin kaybı yok)
            elif BAGLAC.match(c) and B and B[-1]["t"] in ("madde", "liste", "sirali", "giris"):
                B.append({"t": "aciklama", "x": c, "p": p})
            else:
                # paragrafın ilk bilgi maddesi ana madde (sv 1), sonrakiler onun altında (sv 2)
                ana_var = any(b["t"] == "madde" and b["p"] == p and b["sv"] == 1 for b in B)
                m = {"t": "madde", "sv": 2 if ana_var else 1, "x": c, "p": p}
                if (a := anahtar_bul(c, {t.lower() for t in trm})):  # yeni kavram tanımı kendi ana maddesini açar (Primer / Sekonder kardeştir)
                    m["anahtar"], m["sv"] = a, 1
                B.append(m)
            # bölümde ilk geçen terim (en çok 3/bölüm), cümlenin hemen ardından
            if B[-1]["t"] != "giris" and sum(1 for b in B if b["t"] == "terim") < 3:  # giriş cümlesine terim kartı eklenmez
                for ad, tanim in trm.items():
                    # tek sözcüklü terim yalnız ekiyle değil tam sözcük olarak eşleşir ("Gelişim" ≠ "gelişiminde")
                    bitis = r"(?!\w)" if " " not in ad else ""
                    if ad not in kullanildi and re.search(rf"(?<!\w){re.escape(ad)}{bitis}", c, re.I):
                        kullanildi.add(ad)
                        B.append({"t": "terim", "ad": ad, "tanim": tanim, "p": p})
                        break
    buyuk = lambda t: ({"i": "İ", "ı": "I"}.get(t[:1], t[:1].upper()) + t[1:]) if t else t
    for bl in bolumler:
        bl["bloklar"] = kavram_tablolari(sira_dizileri(bl["bloklar"]))
        for b in bl["bloklar"]:
            if b["t"] == "sirali":  # adım başı büyük harf (Türkçe i/İ)
                b["ogeler"] = [buyuk(x) for x in b["ogeler"]]
    return {"surum": SURUM, "key": key, "baslik": baslik, "uretildi": dt.date.today().isoformat(),
            "kaynak_mtime": int((METIN / f"{key}.md").stat().st_mtime), "bolumler": bolumler}


def dogrula(d: dict) -> list[str]:
    """Yapı kapısı: tür, zorunlu alan, boş metin, p artan. Kaynak cümle kaybı yok (her cümle bir blokta)."""
    h = []
    if d.get("surum") != SURUM:
        h.append("surum uyumsuz")
    son = -1
    for b in (x for bl in d.get("bolumler", []) for x in bl["bloklar"]):
        if b["t"] not in TURLER:
            h.append(f"bilinmeyen tür {b['t']}")
        if b["p"] < son:
            h.append(f"p geriye gidiyor ({b['p']} < {son})")
        son = b["p"]
        if len(b.get("ogeler", [])) < (3 if b["t"] == "liste" else 2) and b["t"] in ("liste", "sirali"):
            h.append(f"{b['t']} < 3 öğe")
        if b["t"] not in ("liste", "sirali", "tablo", "terim") and not (b.get("x") or "").strip():
            h.append(f"boş {b['t']}")
    return h


def anahtar(k: str) -> str:
    if (METIN / f"{k}.md").exists():
        return k
    c = sorted(f.stem for f in METIN.glob(f"{k}-*.md") if not re.search(r"-v\d+$|-ag-", f.stem))
    if not c:
        raise SystemExit(f"HATA: {k} metni yok")
    return c[0]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("keys", nargs="*")
    ap.add_argument("--kurul", type=int)
    ap.add_argument("--yeni-gun", type=int, help="yalnız son N günde değişen metinler")
    ap.add_argument("--dogrula", action="store_true")
    a = ap.parse_args()
    keys = [anahtar(k) for k in a.keys]
    if a.kurul:
        sinir = dt.datetime.now().timestamp() - (a.yeni_gun or 10_000) * 86400
        keys += [f.stem for f in sorted(METIN.glob(f"k{a.kurul}-*.md"))
                 if not re.search(r"-v\d+$|-ag-", f.stem) and f.stat().st_mtime >= sinir]
    if not keys:
        ap.print_help()
        return 2
    CIKTI.mkdir(parents=True, exist_ok=True)
    toplam = 0
    for k in keys:
        if a.dogrula:
            f = CIKTI / f"{k}.json"
            hata = dogrula(json.loads(f.read_text(encoding="utf-8"))) if f.exists() else ["dosya yok"]
        else:
            d = modelle(k)
            hata = dogrula(d)
            if not hata:
                (CIKTI / f"{k}.json").write_text(json.dumps(d, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
            say: dict[str, int] = {}
            for b in (x for bl in d["bolumler"] for x in bl["bloklar"]):
                say[b["t"]] = say.get(b["t"], 0) + 1
            print(f"{k}: " + " · ".join(f"{t} {n}" for t, n in sorted(say.items())))
        for x in hata:
            print(f"HATA {k}: {x}")
        toplam += len(hata)
    print(f"{toplam} HATA")
    return 1 if toplam else 0


if __name__ == "__main__":
    sys.exit(main())
