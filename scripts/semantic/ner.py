"""Varlık Çıkarımı (NER) — sözlük tabanlı, deterministik, ücretsiz, GPU yok.

Sözlükteki (ICD/sözlük/kavram) terimleri metinde çok-kelimeli ifade olarak yakalar ve kodlar
(ICD, UMLS, QID) döndürür. Model indirmesi yok.
"""
from __future__ import annotations

from . import nlp

MAX_NGRAM = 5


def _word_positions(text: str):
    import re

    words = []
    for m in re.finditer(r"[A-Za-zÇĞİÖŞÜçğıöşü0-9]+", nlp.normalize(text)):
        words.append((nlp.fold(m.group(0)), m.start(), m.end()))
    return words


def extract(text: str, lexicon: dict[str, dict]) -> list[dict]:
    words = _word_positions(text)
    forms = list(words)
    found: list[dict] = []
    i = 0
    n = len(forms)
    while i < n:
        matched = None
        for size in range(min(MAX_NGRAM, n - i), 0, -1):
            phrase = " ".join(w[0] for w in forms[i:i + size])
            if phrase in lexicon:
                matched = (phrase, size)
                break
        if matched:
            phrase, size = matched
            info = dict(lexicon[phrase])
            info["terim"] = phrase
            info["konum"] = [forms[i][1], forms[i + size - 1][2]]
            found.append(info)
            i += size
        else:
            i += 1
    return found


def summarize(entities: list[dict]) -> dict:
    icd = sorted({e["icd"] for e in entities if e.get("icd")})
    umls = sorted({e["umls"] for e in entities if e.get("umls")})
    return {"terimler": [e["terim"] for e in entities], "icd": icd, "umls": umls}
