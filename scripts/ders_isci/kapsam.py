"""Bir PDF'in ders programındaki HANGİ KONULARI kapsadığını ve sayfa aralıklarını bulur (bir sunu birden çok konu içerebilir).

Yöntem:
  1. Ana konu: isle.program_eslesmesi (ad + kapak + içerik anlamı; tarih kullanılmaz).
  2. Ek konular: aynı kurulun her konusu için, sayfaların BAŞLIK BÖLGESİNDE (ilk 3 anlamlı satır) konu başlığı geçiyor mu?
     Metin içinde geçen anma sayılmaz (yanlış bölme olmasın). Bulunan başlık sayfası = o konunun başlangıcı.
  3. Başlangıçlara göre sayfa aralıkları: [başlangıç, sonraki başlangıç − 1].
"""
from __future__ import annotations

import difflib
import re

UNVAN = re.compile(r"^\s*(prof|doç|doc|dr|uzm|öğr|ogr)\.?\s", re.I)   # isim satırı unvanla BAŞLAR


def _baslik_gibi(x: str) -> bool:
    k = x.split()
    if not 2 <= len(k) <= 8 or re.search(r"[().:;]$|\(|\)|\d{4}|tıp fakültesi|üniversite|şekil|izniyle", x, re.I):
        return False
    return x.isupper() or sum(w[:1].isupper() for w in k) / len(k) >= 0.6

from ayarlar import DATABASE, oku

_FOLD = str.maketrans("çğıöşüâîûÇĞİÖŞÜÂÎÛ", "cgiosuaiucgiosuaiu")


def fold(s: str) -> str:
    s = str(s).replace("İ", "i").replace("I", "ı").lower().translate(_FOLD)
    return " ".join(re.sub(r"[^a-z0-9]+", " ", s).split())


def sayfalar(metin: str) -> list[tuple[int, list[str]]]:
    out = []
    for blok in metin.split("=== SAYFA ")[1:]:
        bas, _, govde = blok.partition(" ===")
        try:
            n = int(bas.strip())
        except ValueError:
            continue
        satir = [x.strip() for x in govde.split("\n") if len(x.strip()) >= 3]
        out.append((n, satir))
    return out


def _kokler(s: str) -> set[str]:
    return {w[:5] for w in fold(s).split() if len(w) >= 3 and w not in {"ve", "ile", "icin", "bir", "veya"}}


def _baslik_eslesir(konu_f: str, satir: str) -> bool:
    """Başlık satırı konuyu gösteriyor mu? Konunun anlamlı kelimelerinin (5 harf kök) HEPSİ satırda olmalı;
    yalnız harf benzerliği yetmez ("Cinsel yolla bulaşan enfeksiyonlar" ≠ "... enfeksiyonlarda TEDAVİ")."""
    s = fold(satir)
    if not s or len(s) > len(konu_f) + 25:
        return False
    k, t = _kokler(konu_f), _kokler(s)
    if not k or not k <= t:
        return False
    return s == konu_f or difflib.SequenceMatcher(None, konu_f, s).ratio() >= 0.75 or konu_f in s


def pdf_kapsami(yol: str, metin: str, ana: dict) -> list[dict]:
    kurul = ana.get("kurul")
    prog = oku(DATABASE / "taxonomy" / "donem3_ders_programi.json", {})
    konular = [x for k in prog.get("kurullar") or [] if k.get("kurul") == kurul
               for x in k.get("konular") or [] if x.get("tur", "ders") == "ders" and x.get("konu")]
    sp = sayfalar(metin)
    son = max((n for n, _ in sp), default=1)
    ders_f = fold(ana.get("ders") or ana.get("ders_klasoru") or "")
    baslangic: dict[str, tuple[int, dict]] = {}
    ilgili: list[dict] = []          # başka dersin konusu bu PDF'te bölüm olarak geçiyor (kapsam SAYILMAZ)
    for n, satirlar in sp:
        # Yalnız KAPAK benzeri sayfa yeni ders başlangıcı olabilir: başlık ilk 2 satırda VE (sayfa seyrek ≤6 satır ya da
        # hoca unvanı içeriyor). Ders içi bölüm başlıkları ve tablo sütunları böylece elenir.
        kapak = len(satirlar) <= 6 or any(UNVAN.match(x) for x in satirlar[:6])
        if not kapak:
            continue
        ust = satirlar[:2]
        bulunan = [t for t in konular if len(fold(t["konu"])) >= 6 and any(_baslik_eslesir(fold(t["konu"]), x) for x in ust)]
        # Programda OLMAYAN bir dersin kapağı: hoca unvanı + başlık satırı, ana dersin başlığından farklı (1. sayfa hariç)
        if not bulunan and n > 2 and len(satirlar) <= 6 and any(UNVAN.match(x) for x in satirlar):
            baslik = next((x for x in satirlar if not UNVAN.match(x) and _baslik_gibi(x)), None)
            ana_f = fold(ana.get("konu") or ana.get("pdf_basligi") or "")
            if baslik and difflib.SequenceMatcher(None, fold(baslik), ana_f).ratio() < 0.7 and baslik not in baslangic:
                baslangic[baslik] = (n, {"konu": baslik.title() if baslik.isupper() else baslik, "ders": ana.get("ders"),
                                         "programda_degil": True})
                continue
        if len({t["konu"] for t in bulunan}) >= 2:      # içindekiler / akış sayfası: bölme noktası değil
            continue
        for t in bulunan:
            if t["konu"] in baslangic or t["konu"] == ana.get("konu"):
                continue
            if ders_f and fold(t.get("ders") or "") != ders_f:
                if t["konu"] not in {x["konu"] for x in ilgili}:
                    ilgili.append({"konu": t["konu"], "ders": t.get("ders"), "sayfa": n})
                continue
            baslangic[t["konu"]] = (n, t)
    ana_t = next((x for x in konular if x["konu"] == ana.get("konu")), {"konu": ana.get("konu"), "ders": ana.get("ders")})
    if not ana.get("programda") and not baslangic:  # programda karşılığı yok: PDF'in kendi adıyla tek konu
        return [{"konu": ana.get("pdf_basligi") or ana.get("konu"), "kurul": kurul, "ders": ana.get("ders"),
                 "sayfa_bas": 1, "sayfa_bit": son, "yontem": "pdf_adi", "programda": False, "guven": "dusuk",
                 "ilgili": ilgili}]
    bolumler = sorted(baslangic.values(), key=lambda x: x[0])
    if ana.get("programda"):
        bolumler.insert(0, (1, ana_t))                # ana konu her zaman baştan başlar (kapak sayfaları dahil)
    out = []
    for i, (bas, t) in enumerate(bolumler):
        bit = (bolumler[i + 1][0] - 1) if i + 1 < len(bolumler) else son
        out.append({"konu": t["konu"], "kurul": kurul, "ders": t.get("ders"), "tarih": t.get("tarih"),
                    "ogretim_uyesi": t.get("ogretim_uyesi"), "sayfa_bas": bas, "sayfa_bit": bit,
                    "yontem": "program" if i == 0 and ana.get("programda") else ("pdf_kapagi" if t.get("programda_degil") else "baslik_sayfasi"),
                    "programda": not t.get("programda_degil"),
                    "guven": ana.get("guven") if i == 0 else "orta"})
    # 4 sayfadan kısa ek bölüm ayrı konu sayılmaz: bir önceki bölüme katılır
    birlesik: list[dict] = []
    for x in out:
        if birlesik and x["yontem"] in ("baslik_sayfasi", "pdf_kapagi") and x["sayfa_bit"] - x["sayfa_bas"] + 1 < 4:
            birlesik[-1]["sayfa_bit"] = x["sayfa_bit"]
            continue
        birlesik.append(x)
    if birlesik:
        birlesik[0]["ilgili"] = ilgili
    return birlesik
