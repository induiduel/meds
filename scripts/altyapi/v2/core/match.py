"""Tek ortak retrieval kütüphanesi — BM25 (CPU, ücretsiz).

Eski sistemde BM25 en az 3-4 yerde ayrı ayrı yazılmıştı. Bu modül hepsinin yerine geçer:
soru↔kaynak eşleştirme, kaynak↔konu eşleştirme ve Öğren bağlantıları aynı skor uzayını kullanır.
Vektör/GPU yolu YOK (istenirse CPU e5 ileride buraya eklenir).
"""
from __future__ import annotations

import os
from typing import Iterable

from . import evidence, ids

__all__ = ["tokenize", "Bm25Index", "match_question", "guven_tier"]

# Kalibre eşikler (env ile ayarlanabilir).
TIER_HIGH = float(os.environ.get("MEDS_V2_TIER_HIGH", "0.6"))
TIER_MID = float(os.environ.get("MEDS_V2_TIER_MID", "0.35"))
MARGIN_MIN = float(os.environ.get("MEDS_V2_MARGIN_MIN", "0.15"))

_STOP = {
    "ve", "ile", "için", "bir", "bu", "şu", "o", "da", "de", "mi", "ki", "ne", "çok", "en",
    "gibi", "olarak", "olan", "veya", "ya", "ancak", "ama", "fakat", "ise", "her", "daha",
    "aşağıdakilerden", "hangisi", "hangisidir", "değildir", "yanlıştır", "hariç", "aşağıda",
    "verilen", "verilenlerden", "seçeneklerden", "doğru", "yanlış", "olduğuna", "göre",
}


def tokenize(text: str) -> list[str]:
    return [t for t in ids.norm_key(text).split() if len(t) > 1 and t not in _STOP]


class Bm25Index:
    """Küçük/orta boy koleksiyonlar için BM25.

    Kendi skorlayıcımız kullanılır: `rank_bm25`'in idf'i küçük koleksiyonlarda 0'a düşüp
    skoru sıfırlıyordu; burada idf = log(1 + (N-df+0.5)/(df+0.5)) daima pozitiftir.
    """

    def __init__(self, docs: Iterable[dict]):
        self.docs = list(docs)
        self.corpus = [tokenize(d.get("text") or "") for d in self.docs]
        self._df: dict[str, int] = {}
        for doc in self.corpus:
            for tok in set(doc):
                self._df[tok] = self._df.get(tok, 0) + 1
        self._avg_len = (sum(len(d) for d in self.corpus) / len(self.corpus)) if self.corpus else 0.0

    def _scores(self, query_tokens: list[str]) -> list[float]:
        import math

        n = len(self.corpus)
        qset = set(query_tokens)
        k1, b = 1.5, 0.75
        out: list[float] = []
        for doc in self.corpus:
            length = len(doc) or 1
            counts: dict[str, int] = {}
            for tok in doc:
                counts[tok] = counts.get(tok, 0) + 1
            score = 0.0
            for tok in qset:
                tf = counts.get(tok, 0)
                if not tf:
                    continue
                df = self._df.get(tok, 0)
                idf = math.log(1 + (n - df + 0.5) / (df + 0.5))
                score += idf * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * length / (self._avg_len or 1)))
            out.append(score)
        return out

    def search(self, query: str, k: int = 5) -> list[dict]:
        q = tokenize(query)
        if not q or not self.docs:
            return []
        raw = self._scores(q)
        order = sorted(range(len(raw)), key=lambda i: -raw[i])[:k]
        return [{"doc": self.docs[i], "skor": float(raw[i])} for i in order if raw[i] > 0]


def guven_tier(support: float | None, margin: float | None = None) -> str:
    """Kanıt desteği (ve varsa rakipten ayrım marjı) ile güven katmanı: yuksek/orta/dusuk."""
    s = support or 0.0
    if s >= TIER_HIGH:
        tier = "yuksek"
    elif s >= TIER_MID:
        tier = "orta"
    else:
        tier = "dusuk"
    if margin is not None and margin < MARGIN_MIN and tier == "yuksek":
        tier = "orta"
    return tier


def match_question(question: dict, index, k: int = 5) -> list[dict]:
    """Soruyu (kök + şıklar) kaynak parçalarıyla eşleştirir; her adaya kanıt + support_ratio + güven ekler."""
    options = question.get("options") or {}
    query = " ".join([question.get("stem") or "", *(
        str(v) for v in options.values())]) if isinstance(options, dict) else (question.get("stem") or "")
    hits = index.search(query, k=k)
    top = hits[0]["skor"] if hits else 0.0
    second = hits[1]["skor"] if len(hits) > 1 else 0.0
    margin = round((top - second) / top, 4) if top > 0 else 0.0
    for hit in hits:
        doc = hit["doc"]
        hit["chunk_id"] = doc.get("id")
        hit["kaynak"] = doc.get("source_id")
        hit["support_ratio"] = evidence.support_ratio(query, [doc.get("text") or ""])
    if hits:
        hits[0]["marj"] = margin
        hits[0]["guven"] = guven_tier(hits[0].get("support_ratio"), margin)
    return hits
