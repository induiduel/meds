"""Sözlüksel indeks (TF-IDF) — tam korpus üzerinde kelime/ikili-gram benzerliği (CPU, ücretsiz).

Dense (FAISS/e5) getiriciyi tamamlar; ikisinin birleşimi top-1 isabetini belirgin artırır.
İndeks `data/lex.pkl` olarak önbelleklenir.
"""
from __future__ import annotations

import pickle

from . import config

_CACHE = None


def _path():
    return config.OUT / "lex.pkl"


def build(texts: list[str]) -> int:
    from sklearn.feature_extraction.text import TfidfVectorizer

    vec = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True, max_features=300000)
    mat = vec.fit_transform(texts)
    with open(_path(), "wb") as fh:
        pickle.dump({"vec": vec, "mat": mat}, fh, protocol=pickle.HIGHEST_PROTOCOL)
    return mat.shape[0]


def _load():
    global _CACHE
    if _CACHE is None:
        with open(_path(), "rb") as fh:
            _CACHE = pickle.load(fh)
    return _CACHE


def search(query: str, k: int = 100) -> list[tuple[int, float]]:
    """(indeks, kosinüs skoru) en iyi k sonuç."""
    import numpy as np

    data = _load()
    qv = data["vec"].transform([query])
    sims = (data["mat"] @ qv.T).toarray().ravel()
    if sims.size == 0:
        return []
    k = min(k, sims.size)
    idx = np.argpartition(-sims, k - 1)[:k]
    idx = idx[np.argsort(-sims[idx])]
    return [(int(i), float(sims[i])) for i in idx if sims[i] > 0]
