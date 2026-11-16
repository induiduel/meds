"""Hibrit arama (opsiyonel) — BM25 + CPU e5 vektörleri, RRF ile birleştirme.

GPU YOK: `intfloat/multilingual-e5-small` CPU'da çalışır. Model yoksa/indirilemezse veya
`MEDS_V2_VECTOR` kapalıysa sessizce yalnız BM25'e düşülür (zararsız).
"""
from __future__ import annotations

import os
from typing import Iterable

from . import match

DEFAULT_MODEL = os.environ.get("MEDS_V2_EMBED_MODEL", "intfloat/multilingual-e5-small")
_MAX_DOCS = int(os.environ.get("MEDS_V2_VECTOR_MAX", "60000"))


def vector_enabled() -> bool:
    return os.environ.get("MEDS_V2_VECTOR", "0").lower() in {"1", "true", "yes", "on"}


class VectorIndex:
    """CPU e5 ile anlamsal arama. Model yoksa `available()` False döner."""

    def __init__(self, docs: Iterable[dict], model_name: str = DEFAULT_MODEL):
        self.docs = list(docs)
        self._model = None
        self._emb = None
        if not self.docs or len(self.docs) > _MAX_DOCS:
            return
        try:
            from sentence_transformers import SentenceTransformer  # CPU

            self._model = SentenceTransformer(model_name, device="cpu")
            texts = ["passage: " + (d.get("text") or "") for d in self.docs]
            self._emb = self._model.encode(
                texts, normalize_embeddings=True, batch_size=32, show_progress_bar=False
            )
        except Exception:  # noqa: BLE001
            self._model = None
            self._emb = None

    def available(self) -> bool:
        return self._emb is not None and self._model is not None

    def search(self, query: str, k: int = 5) -> list[dict]:
        if not self.available() or not query.strip():
            return []
        import numpy as np

        q = self._model.encode(["query: " + query], normalize_embeddings=True)[0]
        sims = np.asarray(self._emb) @ np.asarray(q)
        order = sims.argsort()[::-1][:k]
        return [{"doc": self.docs[int(i)], "skor": float(sims[int(i)])} for i in order if sims[int(i)] > 0]


class HybridIndex:
    """BM25 + (varsa) vektör aramasını Reciprocal Rank Fusion ile birleştirir."""

    def __init__(self, docs: Iterable[dict], *, use_vector: bool | None = None, rrf_k: int = 60):
        self.docs = list(docs)
        self.bm25 = match.Bm25Index(self.docs)
        self.vector = None
        if use_vector is None:
            use_vector = vector_enabled()
        if use_vector:
            self.vector = VectorIndex(self.docs)
            if not self.vector.available():
                self.vector = None
        self.rrf_k = rrf_k

    @property
    def vector_active(self) -> bool:
        return self.vector is not None

    def search(self, query: str, k: int = 5) -> list[dict]:
        bm_hits = self.bm25.search(query, k=k * 2)
        vec_hits = self.vector.search(query, k=k * 2) if self.vector else []
        if not vec_hits:
            return bm_hits[:k]
        scores: dict[str, float] = {}
        doc_of: dict[str, dict] = {}
        for rank, hit in enumerate(bm_hits):
            key = str(hit["doc"].get("id"))
            doc_of[key] = hit["doc"]
            scores[key] = scores.get(key, 0.0) + 1.0 / (self.rrf_k + rank + 1)
        for rank, hit in enumerate(vec_hits):
            key = str(hit["doc"].get("id"))
            doc_of[key] = hit["doc"]
            scores[key] = scores.get(key, 0.0) + 1.0 / (self.rrf_k + rank + 1)
        ranked = sorted(scores.items(), key=lambda kv: -kv[1])[:k]
        return [{"doc": doc_of[key], "skor": score, "rrf": score} for key, score in ranked]


def build_index(docs: Iterable[dict], *, use_vector: bool | None = None):
    """Vektör açıksa HybridIndex, değilse Bm25Index döndürür."""
    docs = list(docs)
    if use_vector is None:
        use_vector = vector_enabled()
    return HybridIndex(docs, use_vector=use_vector) if use_vector else match.Bm25Index(docs)
