"""Niyet Tespiti (Intent Classification) — kural tabanlı, deterministik, ücretsiz.

Soru kökünün hangi klinik/temel bilim niyetini taşıdığını sınıflar (tanı, tedavi, mekanizma,
patogenez, etyoloji, komplikasyon, semptom, laboratuvar, sıklık, ayırıcı tanı, önleme, prognoz,
karşılaştırma, negatif sorgu).
"""
from __future__ import annotations

from . import nlp

_INTENT = [
    ("tedavi", ["tedavi", "ilaç", "mg", "doz", "antibiyotik", "reçete", "kaç mg", "uygulama", "yönetim", "management", "treatment"]),
    ("tanı", ["tanı", "tanısı", "teşhis", "diagnos", "ile uyumlu", "düşündürür", "en olası"]),
    ("ayırıcı_tanı", ["ayırt", "ayırıcı", "farkı", "hangisiyle karışır", "differential"]),
    ("mekanizma", ["mekanizma", "etki", "reseptör", "kanal", "enzim", "inhibe", "aktive", "yol", "pathway", "mechanism"]),
    ("patogenez", ["patogenez", "patofizyoloji", "oluş", "neden olur", "gelişir", "mekanizması"]),
    ("etiyoloji", ["etken", "etiyoloji", "sebep", "neden", "cause", "patojen", "mikroorganizma"]),
    ("komplikasyon", ["komplikasyon", "sekonder", "sonucu", "bağlı gelişen", "complication"]),
    ("semptom", ["semptom", "belirti", "bulgu", "klinik", "symptom", "presentation"]),
    ("laboratuvar", ["laboratuvar", "değer", "test", "kültür", "enzim", "seviye", "düzey", "marker", "lab"]),
    ("sıklık", ["en sık", "en nadir", "insidans", "prevalans", "oran", "most common", "frequency"]),
    ("önleme", ["önleme", "korunma", "profilaksi", "aşı", "prevention", "vaccine"]),
    ("prognoz", ["prognoz", "seyir", "mortalite", "yaşam", "outcome", "prognosis"]),
    ("karşılaştırma", ["karşılaştır", "farkı nedir", "hangisi daha", "benzer", "difference"]),
    ("anatomi", ["anatom", "seyir", "komşu", "bölge", "lokalizasyon", "anatomic"]),
    ("fizyoloji", ["fizyoloji", "fonksiyon", "işlev", "faz", "potansiyel", "physiology"]),
]


def classify(text: str) -> dict:
    toks = set(nlp.fold(text).split())
    stems = set(nlp.stems(text))
    low = nlp.fold(text)
    scores = []
    for name, keys in _INTENT:
        s = 0
        for k in keys:
            fk = nlp.fold(k)
            if " " in fk:
                if fk in low:  # çok kelimeli kalıp
                    s += 1
            elif fk in toks or fk in stems or (len(fk) >= 4 and any(t.startswith(fk) for t in toks)):
                s += 1
        if s:
            scores.append((s, name))
    scores.sort(reverse=True)
    neg = any(k in toks for k in ("değildir", "yanlıştır", "hariç", "olmayan")) or "değildir" in low
    return {"niyet": scores[0][1] if scores else "genel",
            "alt_niyetler": [n for _, n in scores[:3]],
            "negatif_sorgu": neg}
