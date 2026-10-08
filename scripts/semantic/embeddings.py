"""Embedding (CPU, ücretsiz) — multilingual-e5-small. GPU yok."""
from __future__ import annotations

from . import config

_MODEL = None


def model():
    global _MODEL
    if _MODEL is None:
        from sentence_transformers import SentenceTransformer
        try:
            import torch
            torch.set_num_threads(int(__import__("os").cpu_count() or 4))
        except Exception:  # noqa: BLE001
            pass
        _MODEL = SentenceTransformer(config.EMBED_MODEL, device="cpu")
    return _MODEL


def embed_passages(texts: list[str], batch: int = 64):
    return model().encode(["passage: " + (t or "") for t in texts],
                          normalize_embeddings=True, batch_size=batch, show_progress_bar=False,
                          convert_to_numpy=True)


def embed_query(text: str):
    return model().encode(["query: " + (text or "")], normalize_embeddings=True,
                          show_progress_bar=False)[0]
