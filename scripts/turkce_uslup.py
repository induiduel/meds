"""Türkçe üslup kapısı — meds/docs/TURKCE_USLUP_STANDARDI.md (kullanıcı kararı 2026-10-18).

Öğrenciye okunan/gösterilen metin doğal, eksiksiz ve anlaşılır Türkçe olmalı: İngilizceden çeviri kokan mecazlar
("imzası", "motoru", "çapası") ve iç yazım etiketleri ("Ayrım cümlesi:", "Kısa formül:", "Akılda tut:") HATA'dır.
Kullanım: from turkce_uslup import denetle; e.extend(denetle(metin, yer))
"""
import re

# (kalıp, önerilen doğal karşılık)
YASAK = [
    (r"\bimza(sı|si|ları|ları|dır|sıdır)?\b", "en belirgin/ayırt edici özelliği, tipik bulgusu"),
    (r"\bmotor(u|udur|larıdır|ları)\b", "temel nedeni, itici gücü yerine: …e yol açan temel olay"),
    (r"\bçapa(sı|dır)?\b", "bağlayıcı yapı, tutunma noktası"),
    (r"\bfren(i|idir|ler)?\b", "baskılayıcı, düzenleyici"),
    (r"\bgaz pedalı\w*", "uyarıcı, hızlandırıcı"),
    (r"\banahtar oyuncu\w*", "temel rol oynayan"),
    (r"\boyun değiştirici\w*", "belirleyici"),
    (r"\b(ayrım|ayırt|anahtar|sınav|özet|hap) cümle(si)?\s*:", "etiketi kaldır; cümleyi doğrudan kur"),
    (r"\b(kısa|tek) formül\s*:", "etiketi kaldır; \"Özetle, …\" ya da doğrudan cümle"),
    (r"\bakılda tut\s*:", "etiketi kaldır; \"Unutmayın, …\" ya da doğrudan cümle"),
    (r"\b(mekanizma|mantığı|mantık) şudur\s*:", "doğrudan anlat: \"… çünkü …\""),
    (r"\bayırt et\s*:", "\"… ile … şöyle ayrılır: …\""),
    (r"\bayrım\s*:", "\"… ile … şöyle ayrılır: …\""),
]
YASAK_RE = [(re.compile(k, re.I), o) for k, o in YASAK]


def denetle(metin, yer):
    e = []
    m = (metin or '').replace('**', '')
    for r, oneri in YASAK_RE:
        g = r.search(m)
        if g: e.append(f'{yer}: Türkçe üslup — {g.group()!r} doğal değil ({oneri})')
    return e
