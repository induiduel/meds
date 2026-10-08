"""Vektör deposu — FAISS (CPU, ücretsiz). Kosinüs benzerliği (normalize + inner product)."""
from __future__ import annotations

import json

from . import config

_META_CACHE = None


class Store:
    def __init__(self):
        import faiss
        self.index = faiss.read_index(str(config.INDEX_PATH))
        self.metas = self._load_meta()
        self.idx_of = {m.get("chunk_id"): i for i, m in enumerate(self.metas)}

    def _load_meta(self) -> list[dict]:
        global _META_CACHE
        if _META_CACHE is not None:
            return _META_CACHE
        rows = []
        with open(config.META_PATH, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
        _META_CACHE = rows
        return rows

    def search(self, vector, k: int = 25) -> list[dict]:
        import numpy as np
        q = np.asarray([vector], dtype="float32")
        scores, idx = self.index.search(q, k)
        out = []
        for s, i in zip(scores[0], idx[0]):
            if i < 0:
                continue
            meta = dict(self.metas[int(i)])
            meta["skor"] = round(float(s), 4)
            out.append(meta)
        return out
