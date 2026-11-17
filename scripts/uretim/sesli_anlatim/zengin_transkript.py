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


BAG_SOZ = {"ve", "ile", "ya", "da", "de", "önce", "ardından", "sonra", "sonrasında", "en", "sonunda", "son", "olarak",
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


def sirali_mi(c: str) -> list[str] | None:
    """'Önce A, ardından B, sonra C ve en sonunda D gelişir.' → [A, B, C, D]. Açık başlangıç (önce/ilk) ve bitiş
    (en son/son olarak) ister; her adım ≥ 2 sözcük; cümle sözcükleri korunmalı (kapsar)."""
    if not (re.search(r"\b(önce|ilk olarak|ilk sırada)\b", c, re.I) and re.search(r"\b(en sonunda|en son|son olarak|en sonda)\b", c, re.I)):
        return None
    bas = re.match(r"^(.{0,120}?:)\s*", c)  # "Sıra şöyledir:" gibi giriş
    govde = c[bas.end():] if bas else c
    parca = re.split(r",?\s*(?:\b[Öö]nce\b|\bilk olarak\b|\bardından\b|\bsonra(?:sında)?\b|\ben sonunda\b|\ben sonda\b|\ben son\b|\bson olarak\b)\s*,?\s*", govde)
    og = [re.sub(r"\s+(ve|ile)$", "", x.strip(" ,.;")) for x in parca if x.strip(" ,.;")]
    if og:  # son öğedeki yüklem (gelişir, gelir…) madde metnine girmez
        og[-1] = re.sub(r"\s+(gelişir|gelir|yapılır|uygulanır|başlar|izlenir|kazanılır)$", "", og[-1])
    if len(og) < 3 or any(len(x.split()) < 2 for x in og) or any(";" in x for x in og):
        return None
    return og if kapsar(c, og) else None


def liste_mi(c: str) -> tuple[str, list[str]] | None:
    """Sayım cümlesi: 'X'in başında A, B ve C gelir.' / 'Nedenler arasında A, B ve C sayılır.' /
    'Üç aile tanımlanmıştır: A, B ve C.' (iki noktadan sonra yalnız kısa öğeler, her biri ≤ 6 sözcük)"""
    ik = re.match(r"^([^:;]{8,160}):\s+([^:;]+?)[.!]?$", c)
    if ik:
        og = sayiyla_ayir(ik.group(1), ik.group(2)) or []
        if len(og) >= 3 and all(len(x.split()) <= 6 for x in og) and ogeler_ad_mi(og) and kapsar(c, [ik.group(1), *og]):
            return ik.group(1).strip(), og
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
            elif (s := sirali_mi(c)):
                gb = re.match(r"^(.{0,120}?:)\s*", c)
                B.append({"t": "sirali", "bas": gb.group(1) if gb else "", "ogeler": s, "p": p})
            elif (tb := tablo_mi(c)):
                B.append({"t": "tablo", **tb, "x": c, "p": p})
            elif (ls := liste_mi(c)):
                B.append({"t": "liste", "bas": ls[0], "ogeler": ls[1], "p": p})
            elif (q := re.search(r"[“\"]([^”\"]{8,200})[”\"]", c)):
                B.append({"t": "alinti", "x": q.group(1), "kaynak": c, "p": p})
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
        if b["t"] in ("liste", "sirali") and len(b.get("ogeler", [])) < 3:
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
