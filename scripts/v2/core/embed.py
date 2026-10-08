"""Vektörleştirme (CPU e5) — site RAG'i için parça embedding'leri.

GPU YOK. `intfloat/multilingual-e5-small` CPU'da çalışır. Çıktı `MEDS_CORE_DIR/vectors/`:
  - `e5.npy`         : (N, d) normalize edilmiş embedding matrisi
  - `e5_ids.jsonl`   : satır sırasıyla {chunk_id, source_id, page}
  - `e5_manifest.json`: model, boyut, sayı, zaman
Site bu dosyaları hızlı benzerlik araması için kullanabilir; yeniden çalıştırma idempotenttir.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from .. import config
from . import store

DEFAULT_MODEL = os.environ.get("MEDS_V2_EMBED_MODEL", "intfloat/multilingual-e5-small")


def build(chunks: list[dict], *, batch_size: int = 64, log=print) -> dict:
    """Parçaları CPU e5 ile vektörleştirir ve diske yazar. Model yoksa yapılmaz (rapor döner).
    Aynı anda yalnız bir vektörleştirme çalışır (kilit); ikinci çağrı atlanır."""
    if not chunks:
        return {"vektor": 0, "yazildi": False, "neden": "parça yok"}
    try:
        from sentence_transformers import SentenceTransformer
    except Exception as exc:  # noqa: BLE001
        return {"vektor": 0, "yazildi": False, "neden": f"sentence_transformers yok: {exc}"}

    config.ensure_core_dirs()
    try:
        # işlemci çekirdeklerini kullan (CPU-only)
        import torch  # type: ignore

        torch.set_num_threads(os.cpu_count() or 4)
    except Exception:  # noqa: BLE001
        pass

    lock = store.FileLock(config.VECTORS_DIR / "embed.lock", timeout=2)
    try:
        lock.__enter__()
    except Exception:  # noqa: BLE001
        return {"vektor": 0, "yazildi": False, "neden": "başka vektörleştirme çalışıyor"}

    try:
        model = SentenceTransformer(DEFAULT_MODEL, device="cpu")
        texts = ["passage: " + (c.get("text") or "") for c in chunks]
        log(f"vektörleştirme: {len(texts)} parça, model={DEFAULT_MODEL}")
        emb = model.encode(texts, normalize_embeddings=True, batch_size=batch_size,
                           show_progress_bar=False, convert_to_numpy=True)

        import numpy as np

        vec_dir: Path = config.VECTORS_DIR
        np.save(vec_dir / "e5.npy", np.asarray(emb, dtype="float32"))
        store.write_jsonl(vec_dir / "e5_ids.jsonl", [
            {"chunk_id": c.get("chunk_id"), "source_id": c.get("source_id"), "page": c.get("page")}
            for c in chunks
        ], guard=False)
        store.atomic_write_json(vec_dir / "e5_manifest.json", {
            "model": DEFAULT_MODEL, "boyut": int(np.asarray(emb).shape[1]),
            "sayi": len(chunks), "zaman": store.now_iso(), "pipeline_generation": config.PIPELINE_GENERATION,
        })
        return {"vektor": len(chunks), "boyut": int(np.asarray(emb).shape[1]), "yazildi": True}
    finally:
        lock.__exit__(None, None, None)


_CACHE: dict = {"model": None, "mat": None, "rows": None, "key": None}


def _load_cache():
    """Model + vektörleri bir kez yükler (kalıcı süreçte tekrar yüklememek için)."""
    npy = config.VECTORS_DIR / "e5.npy"
    ids = config.VECTORS_DIR / "e5_ids.jsonl"
    man = config.VECTORS_DIR / "e5_manifest.json"
    if not npy.exists() or not ids.exists():
        return None
    key = (str(npy.stat().st_mtime_ns), str(ids.stat().st_mtime_ns))
    if _CACHE["mat"] is not None and _CACHE["key"] == key:
        return _CACHE
    try:
        import numpy as np
        from sentence_transformers import SentenceTransformer
    except Exception:  # noqa: BLE001
        return None
    _CACHE["model"] = SentenceTransformer((store.read_json(man, {}) or {}).get("model", DEFAULT_MODEL), device="cpu")
    _CACHE["mat"] = np.load(npy)
    _CACHE["rows"] = list(store.iter_jsonl(ids))
    _CACHE["key"] = key
    return _CACHE


def search(query: str, k: int = 5) -> list[dict]:
    """Kaydedilmiş vektörler üzerinde anlamsal arama (CPU). Model bir kez yüklenir."""
    cache = _load_cache()
    if not cache or not query.strip():
        return []
    model, mat, rows = cache["model"], cache["mat"], cache["rows"]
    q = model.encode(["query: " + query], normalize_embeddings=True)[0]
    sims = mat @ q
    order = sims.argsort()[::-1][:k]
    out = []
    for i in order:
        if sims[int(i)] <= 0:
            continue
        row = dict(rows[int(i)])
        row["skor"] = float(sims[int(i)])
        out.append(row)
    return out


def load_all_chunks() -> list[dict]:
    chunks: list[dict] = []
    if config.CHUNKS_DIR.exists():
        for path in sorted(config.CHUNKS_DIR.glob("*.jsonl")):
            chunks.extend(store.read_jsonl(path))
    return chunks


def manifest() -> dict:
    return store.read_json(config.VECTORS_DIR / "e5_manifest.json", {}) or {}
