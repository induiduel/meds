#!/usr/bin/env python3
"""MedSoru Low-Latency Hybrid Serving API — FastAPI + DuckDB (cursor-per-request)."""
from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import os
import re
import time
from contextlib import asynccontextmanager, contextmanager
from dataclasses import dataclass
from pathlib import Path
from threading import RLock
from typing import Any, AsyncIterator, Iterator, Optional, Sequence

import duckdb
import numpy as np
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

LOG = logging.getLogger("medsoru.api")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
)

EMBEDDING_REGISTRY: dict[str, tuple[str, int, int]] = {
    "bge-m3":   ("BAAI/bge-m3",                    1024, 512),
    "e5-base":  ("intfloat/multilingual-e5-base",  768, 512),
    "e5-small": ("intfloat/multilingual-e5-small", 384, 512),
    "minilm":   ("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", 384, 256),
}

_TERM_CLEAN_RE = re.compile(r"[^\wçğıöşü\s\-]", re.UNICODE)


def sanitize_terms(terms: Sequence[str], max_terms: int = 6,
                   min_len: int = 3, max_len: int = 40) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for t in terms:
        if not isinstance(t, str):
            continue
        cleaned = _TERM_CLEAN_RE.sub("", t.strip().lower())
        if not (min_len <= len(cleaned) <= max_len):
            continue
        if cleaned in seen:
            continue
        seen.add(cleaned)
        out.append(cleaned)
        if len(out) >= max_terms:
            break
    return out


def build_sparse_score_sql(terms: Sequence[str]) -> tuple[str, list[Any]]:
    if not terms:
        return "0", []
    parts: list[str] = []
    params: list[Any] = []
    for t in terms:
        parts.append("CASE WHEN lower(content) LIKE ? THEN 1 ELSE 0 END")
        params.append(f"%{t}%")
    return " + ".join(parts), params


@dataclass(slots=True)
class ServerConfig:
    lake: Path
    embed_model: str = os.environ.get("MEDSORU_EMBED_MODEL", "bge-m3")
    embed_dim: int = 1024
    hnsw: bool = True
    default_top_k: int = 5
    rrf_k: int = 60
    query_cache_ttl: float = 300.0
    embed_cache_size: int = 512

    @classmethod
    def from_env(cls) -> "ServerConfig":
        model = os.environ.get("MEDSORU_EMBED_MODEL", "bge-m3").lower()
        if model not in EMBEDDING_REGISTRY:
            LOG.warning("Bilinmeyen MEDSORU_EMBED_MODEL=%s → bge-m3", model)
            model = "bge-m3"
        _, dim, _ = EMBEDDING_REGISTRY[model]
        return cls(
            lake=Path(os.environ.get("MEDSORU_LAKE", "./meds_lake")).resolve(),
            embed_model=model,
            embed_dim=int(os.environ.get("MEDSORU_EMBED_DIM", str(dim))),
            hnsw=os.environ.get("MEDSORU_HNSW", "1") not in {"0", "false", "False"},
            default_top_k=int(os.environ.get("MEDSORU_TOP_K", "5")),
            rrf_k=int(os.environ.get("MEDSORU_RRF_K", "60")),
            embed_cache_size=int(os.environ.get("MEDSORU_EMBED_CACHE", "512")),
        )


class DuckEngine:
    _instance: Optional["DuckEngine"] = None
    _lock = RLock()

    def __init__(self, cfg: ServerConfig) -> None:
        self.cfg = cfg
        self._master = duckdb.connect(":memory:")
        self._master.execute("SET threads TO 4;")
        self._master.execute("PRAGMA memory_limit='2GB';")
        self._views_ready = False
        self._question_cache: dict[str, Any] = {}
        self._question_cache_ts: float = 0.0

    @classmethod
    def instance(cls, cfg: ServerConfig) -> "DuckEngine":
        with cls._lock:
            if cls._instance is None:
                cls._instance = DuckEngine(cfg)
            return cls._instance

    @contextmanager
    def connect(self) -> Iterator[duckdb.DuckDBPyConnection]:
        cur = self._master.cursor()
        try:
            yield cur
        finally:
            cur.close()

    @contextmanager
    def write_connect(self) -> Iterator[duckdb.DuckDBPyConnection]:
        with self._lock:
            yield self._master

    def ensure_views(self) -> None:
        if self._views_ready:
            return
        chunks = str(self.cfg.lake / "chunks" / "**" / "*.parquet")
        questions = str(self.cfg.lake / "questions" / "**" / "*.parquet")
        with self.write_connect() as con:
            con.execute(f"CREATE OR REPLACE VIEW chunks AS SELECT * FROM read_parquet('{chunks}', hive_partitioning=true);")
            con.execute(f"CREATE OR REPLACE VIEW questions AS SELECT * FROM read_parquet('{questions}', hive_partitioning=true);")
            if self.cfg.hnsw:
                try:
                    con.execute("INSTALL vss; LOAD vss;")
                    con.execute("SET hnsw_enable_experimental_persistence = true;")
                    con.execute("""
                        CREATE OR REPLACE TABLE chunks_mat AS
                        SELECT chunk_id, donem, komite, ders, content, embedding
                        FROM chunks;
                    """)
                    con.execute(
                        "CREATE INDEX IF NOT EXISTS idx_chunks_hnsw "
                        "ON chunks_mat USING HNSW (embedding) WITH (metric='cosine');"
                    )
                    LOG.info("HNSW indeks hazır.")
                except Exception as exc:  # noqa: BLE001
                    LOG.warning("HNSW kurulamadı: %s", exc)
            self._views_ready = True
            LOG.info("DuckDB view'leri hazır: %s", self.cfg.lake)

    def load_question_cache(self) -> None:
        now = time.monotonic()
        if self._question_cache and (now - self._question_cache_ts) < self.cfg.query_cache_ttl:
            return
        with self.connect() as con:
            tbl = con.execute(
                "SELECT * FROM questions WHERE status IN ('verified', 'fixed')"
            ).fetch_arrow_table()
        rows = tbl.to_pylist()
        buckets: dict[tuple[int, int, str], list[dict[str, Any]]] = {}
        for row in rows:
            key = (row.get("donem", 0), row.get("komite", 0), row.get("ders") or "Genel")
            buckets.setdefault(key, []).append(row)
        self._question_cache = {"rows": rows, "buckets": buckets}
        self._question_cache_ts = now
        LOG.info("Question cache: %d soru, %d bucket", len(rows), len(buckets))


class QueryEmbedder:
    def __init__(self, model: str, expected_dim: int, cache_size: int) -> None:
        self.model_name = model
        self.dim = expected_dim
        self._model = None
        self._onnx = None
        self._tokenizer = None
        self._prefix = "query: " if model.startswith("e5") else ""
        self._cache: dict[str, list[float]] = {}
        self._cache_size = cache_size
        self._mode = "hash"

        onnx_dir = os.environ.get("MEDSORU_ONNX_DIR")
        if onnx_dir and Path(onnx_dir).exists():
            try:
                self._init_onnx(onnx_dir)
                self._mode = "onnx"
                return
            except Exception as exc:  # noqa: BLE001
                LOG.warning("ONNX yüklenemedi: %s", exc)

        if model in EMBEDDING_REGISTRY:
            hf_id, dim, max_len = EMBEDDING_REGISTRY[model]
            try:
                from sentence_transformers import SentenceTransformer  # type: ignore
                self._model = SentenceTransformer(hf_id, device="cpu")
                self._model.max_seq_length = max_len
                self.dim = int(self._model.get_sentence_embedding_dimension())
                self._mode = "st"
                LOG.info("Query embedder: ST %s (dim=%d)", model, self.dim)
                return
            except Exception as exc:  # noqa: BLE001
                LOG.warning("%s yüklenemedi: %s", model, exc)

        self._mode = "hash"
        LOG.warning("HashEmbedder aktif (dim=%d)", self.dim)

    def _init_onnx(self, model_dir: str) -> None:
        import onnxruntime as ort  # type: ignore
        from transformers import AutoTokenizer  # type: ignore
        self._tokenizer = AutoTokenizer.from_pretrained(model_dir)
        so = ort.SessionOptions()
        so.intra_op_num_threads = 2
        so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        self._onnx = ort.InferenceSession(
            f"{model_dir}/model.onnx", sess_options=so,
            providers=["CPUExecutionProvider"],
        )
        self.dim = int(self._onnx.get_outputs()[0].shape[-1])
        LOG.info("ONNX embedder hazır (dim=%d)", self.dim)

    def encode(self, text: str) -> list[float]:
        key = hashlib.blake2b(text.strip().lower().encode(), digest_size=16).hexdigest()
        cached = self._cache.get(key)
        if cached is not None:
            return cached
        if self._onnx is not None:
            vec = self._encode_onnx(text).tolist()
        elif self._model is not None:
            v = self._model.encode(
                [self._prefix + text], normalize_embeddings=True,
                convert_to_numpy=True, show_progress_bar=False,
            )[0]
            vec = v.astype(np.float32).tolist()
        else:
            seed = int.from_bytes(hashlib.blake2b(text.encode(), digest_size=8).digest(), "little")
            rng = np.random.default_rng(seed)
            v = rng.standard_normal(self.dim, dtype=np.float32)
            v /= (np.linalg.norm(v) or 1.0)
            vec = v.tolist()
        if len(self._cache) >= self._cache_size:
            self._cache.pop(next(iter(self._cache)))
        self._cache[key] = vec
        return vec

    def _encode_onnx(self, text: str) -> np.ndarray:
        enc = self._tokenizer(
            self._prefix + text, return_tensors="np",
            truncation=True, max_length=256, padding=True,
        )
        feeds = {i.name: enc[i.name] for i in self._onnx.get_inputs() if i.name in enc}
        out = self._onnx.run(None, feeds)[0]
        mask = enc["attention_mask"].astype(np.float32)
        masked = out * mask[..., None]
        summed = masked.sum(axis=1)
        counts = np.clip(mask.sum(axis=1, keepdims=True), 1e-9, None)
        vec = (summed / counts)[0]
        return (vec / (np.linalg.norm(vec) or 1.0)).astype(np.float32)


class HybridSearchRequest(BaseModel):
    query: str = Field(min_length=2, max_length=1000)
    donem: Optional[int] = None
    komite: Optional[int] = None
    ders: Optional[str] = None
    top_k: int = Field(default=5, ge=1, le=50)


class SearchHit(BaseModel):
    chunk_id: str
    donem: int
    komite: int
    ders: str
    source_file: Optional[str] = None
    page_num: Optional[int] = None
    heading_path: list[str] = Field(default_factory=list)
    content: str
    score: float
    dense_score: float = 0.0
    sparse_score: float = 0.0


class HybridSearchResponse(BaseModel):
    query: str
    latency_ms: float
    partitions_scanned: int
    hits: list[SearchHit]


class QuizResponse(BaseModel):
    latency_ms: float
    questions: list[dict[str, Any]]


class SolveRequest(BaseModel):
    question_id: Optional[str] = None
    stem: Optional[str] = None
    options: Optional[dict[str, str]] = None
    donem: Optional[int] = None
    komite: Optional[int] = None
    ders: Optional[str] = None
    top_k: int = Field(default=6, ge=1, le=20)


def _partition_filter(req: HybridSearchRequest) -> tuple[str, list[Any], int]:
    clauses: list[str] = []
    params: list[Any] = []
    n = 0
    if req.donem is not None:
        clauses.append("donem = ?"); params.append(req.donem); n += 1
    if req.komite is not None:
        clauses.append("komite = ?"); params.append(req.komite); n += 1
    if req.ders:
        clauses.append("ders = ?"); params.append(req.ders); n += 1
    where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
    partitions_scanned = max(1, 3 - n) * 4
    return where, params, partitions_scanned


def hybrid_search(engine: DuckEngine, embedder: QueryEmbedder,
                  req: HybridSearchRequest) -> HybridSearchResponse:
    t0 = time.perf_counter()
    engine.ensure_views()
    where, filter_params, partitions_scanned = _partition_filter(req)
    qvec = embedder.encode(req.query)
    fetch_k = max(int(req.top_k) * 4, 20)

    raw_terms = [t for t in req.query.lower().split() if len(t) >= 3]
    terms = sanitize_terms(raw_terms, max_terms=6, min_len=3)
    score_expr, score_params = build_sparse_score_sql(terms)

    with engine.connect() as con:
        dense_sql = f"""
            SELECT chunk_id, donem, komite, ders,
                   source_file, page_num, heading_path, content,
                   array_cosine_similarity(embedding, ?::FLOAT[{embedder.dim}]) AS dscore
            FROM chunks
            {where}
            ORDER BY dscore DESC
            LIMIT {fetch_k};
        """
        dense_rows = con.execute(dense_sql, [qvec, *filter_params]).fetchall()
        dense_cols = [d[0] for d in con.description]

        if terms:
            sparse_sql = f"""
                SELECT chunk_id, donem, komite, ders,
                       source_file, page_num, heading_path, content,
                       ({score_expr}) AS sscore
                FROM chunks
                {where}
                ORDER BY sscore DESC, token_count DESC
                LIMIT {fetch_k};
            """
            sparse_rows = con.execute(sparse_sql, [*score_params, *filter_params]).fetchall()
            sparse_cols = [d[0] for d in con.description]
        else:
            sparse_rows, sparse_cols = [], dense_cols

    dense = [dict(zip(dense_cols, r)) for r in dense_rows]
    sparse = [dict(zip(sparse_cols, r)) for r in sparse_rows]

    k = engine.cfg.rrf_k
    rrf: dict[str, dict[str, Any]] = {}
    dense_rank = {row["chunk_id"]: i for i, row in enumerate(dense)}
    sparse_rank = {row["chunk_id"]: i for i, row in enumerate(sparse)}
    for row in dense:
        cid = row["chunk_id"]
        rrf.setdefault(cid, {"row": row, "dense_score": 0.0, "sparse_score": 0.0})
        rrf[cid]["dense_score"] = float(row.get("dscore") or 0.0)
        rrf[cid]["rrf"] = rrf[cid].get("rrf", 0.0) + 1.0 / (k + dense_rank[cid] + 1)
    for row in sparse:
        cid = row["chunk_id"]
        rrf.setdefault(cid, {"row": row, "dense_score": 0.0, "sparse_score": 0.0})
        rrf[cid]["sparse_score"] = float(row.get("sscore") or 0.0)
        rrf[cid]["rrf"] = rrf[cid].get("rrf", 0.0) + 1.0 / (k + sparse_rank[cid] + 1)

    merged = sorted(rrf.items(), key=lambda kv: kv[1].get("rrf", 0.0), reverse=True)
    hits: list[SearchHit] = []
    for cid, payload in merged[:req.top_k]:
        row = payload["row"]
        hits.append(SearchHit(
            chunk_id=cid, donem=int(row.get("donem") or 0),
            komite=int(row.get("komite") or 0),
            ders=row.get("ders") or "Genel",
            source_file=row.get("source_file"), page_num=row.get("page_num"),
            heading_path=list(row.get("heading_path") or []),
            content=row.get("content") or "",
            score=float(payload.get("rrf", 0.0)),
            dense_score=payload.get("dense_score", 0.0),
            sparse_score=payload.get("sparse_score", 0.0),
        ))

    latency_ms = (time.perf_counter() - t0) * 1000.0
    return HybridSearchResponse(
        query=req.query, latency_ms=round(latency_ms, 3),
        partitions_scanned=partitions_scanned, hits=hits,
    )


_cfg = ServerConfig.from_env()
_engine = DuckEngine.instance(_cfg)
_embedder = QueryEmbedder(_cfg.embed_model, _cfg.embed_dim, _cfg.embed_cache_size)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    LOG.info("MedSoru API başlıyor: lake=%s embed=%s (dim=%d)",
             _cfg.lake, _cfg.embed_model, _embedder.dim)
    _cfg.embed_dim = _embedder.dim
    _engine.ensure_views()
    _engine.load_question_cache()
    yield
    LOG.info("MedSoru API kapanıyor.")


app = FastAPI(title="MedSoru Hybrid API", version="1.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000",
                   "http://localhost:5173", "*"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)


@app.middleware("http")
async def telemetry(request: Request, call_next):
    t0 = time.perf_counter()
    response = await call_next(request)
    dt_ms = (time.perf_counter() - t0) * 1000.0
    response.headers["X-Latency-Ms"] = f"{dt_ms:.2f}"
    LOG.info("%s %s -> %d (%.1f ms)", request.method,
             request.url.path, response.status_code, dt_ms)
    return response


@app.get("/healthz")
def healthz() -> dict[str, Any]:
    _engine.ensure_views()
    with _engine.connect() as con:
        n_chunks = con.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
        n_q = con.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
    return {
        "status": "ok", "lake": str(_cfg.lake),
        "embed_model": _cfg.embed_model, "embed_dim": _embedder.dim,
        "chunks": n_chunks, "questions": n_q, "hnsw": _cfg.hnsw,
    }


@app.post("/api/search/hybrid", response_model=HybridSearchResponse)
async def api_hybrid(req: HybridSearchRequest) -> HybridSearchResponse:
    try:
        return await asyncio.to_thread(hybrid_search, _engine, _embedder, req)
    except Exception as exc:  # noqa: BLE001
        LOG.exception("Hybrid search hatası")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/api/questions/quiz", response_model=QuizResponse)
async def api_quiz(
    donem: Optional[int] = None, komite: Optional[int] = None,
    ders: Optional[str] = None, adet: int = 10, zorluk: Optional[str] = None,
) -> QuizResponse:
    t0 = time.perf_counter()
    _engine.load_question_cache()
    buckets: dict[tuple[int, int, str], list[dict[str, Any]]] = \
        _engine._question_cache.get("buckets", {})  # noqa: SLF001
    pool: list[dict[str, Any]] = []
    for (d, k, c), rows in buckets.items():
        if donem is not None and d != donem:
            continue
        if komite is not None and k != komite:
            continue
        if ders and c != ders:
            continue
        for r in rows:
            if zorluk and r.get("difficulty") != zorluk:
                continue
            pool.append(r)
    if not pool:
        raise HTTPException(status_code=404, detail="Kriterlere uyan soru bulunamadı.")
    import random
    random.shuffle(pool)
    selected = pool[: max(1, min(adet, 50))]
    latency_ms = (time.perf_counter() - t0) * 1000.0
    return QuizResponse(latency_ms=round(latency_ms, 3), questions=selected)


async def _solve_stream(req: SolveRequest) -> AsyncIterator[bytes]:
    t0 = time.perf_counter()
    engine = _engine
    engine.ensure_views()
    stem = req.stem
    options = req.options or {}
    if req.question_id and not stem:
        with engine.connect() as con:
            row = con.execute(
                "SELECT stem, options, ders, donem, komite FROM questions "
                "WHERE question_id = ?", [req.question_id],
            ).fetchone()
        if row is None:
            yield _sse("error", {"message": f"Soru bulunamadı: {req.question_id}"})
            return
        stem = row[0]
        options = dict(row[1] or {})
        req.ders = req.ders or row[2]
        req.donem = req.donem if req.donem is not None else row[3]
        req.komite = req.komite if req.komite is not None else row[4]
    if not stem:
        yield _sse("error", {"message": "stem veya question_id zorunlu."})
        return
    search_req = HybridSearchRequest(
        query=stem[:400], donem=req.donem, komite=req.komite,
        ders=req.ders, top_k=req.top_k,
    )
    result = await asyncio.to_thread(hybrid_search, engine, _embedder, search_req)
    yield _sse("meta", {"question_id": req.question_id,
                        "evidence_count": len(result.hits),
                        "retrieval_ms": result.latency_ms})
    for hit in result.hits:
        yield _sse("evidence", hit.model_dump())
    api_key = os.environ.get("GEMINI_API_KEY")
    context = "\n\n".join(
        f"[{h.chunk_id}] ({h.source_file} p.{h.page_num})\n{h.content}"
        for h in result.hits
    )
    if api_key:
        try:
            async for token in _gemini_stream(api_key, stem, options, context):
                yield _sse("token", {"text": token})
        except Exception as exc:  # noqa: BLE001
            LOG.exception("Gemini stream hatası")
            yield _sse("error", {"message": f"LLM hatası: {exc}"})
    else:
        fallback = _fallback_explanation(stem, options, result.hits)
        for tok in _pseudo_tokens(fallback):
            yield _sse("token", {"text": tok})
            await asyncio.sleep(0.01)
    yield _sse("done", {"total_ms": round((time.perf_counter() - t0) * 1000.0, 2)})


async def _gemini_stream(api_key: str, stem: str,
                         options: dict[str, str], context: str) -> AsyncIterator[str]:
    from google import genai  # type: ignore
    client = genai.Client(api_key=api_key)
    prompt = (
        "Sen Tıp Fakültesi Dönem 3 öğrencisine klinik akıl yürütmeyle açıklama yapan "
        "kıdemli bir öğretim üyesisin. YALNIZCA aşağıdaki kanıt bloklarına dayanarak "
        "soruyu çöz. Kanıt yoksa 'bu konuda slaytta kanıt yok' de, uydurma.\n\n"
        f"### SORU\n{stem}\n\n"
        f"### ŞIKLAR\n{json.dumps(options, ensure_ascii=False, indent=2)}\n\n"
        f"### KANIT\n{context}\n\n"
        "Adım adım: (1) soru kökünü özetle, (2) her şıkkı kanıtla çürüt/doğrula, "
        "(3) doğru cevabı ve chunk_id referansını ver."
    )
    loop = asyncio.get_running_loop()
    queue: asyncio.Queue[Optional[str]] = asyncio.Queue()

    def _produce() -> None:
        try:
            stream = client.models.generate_content_stream(
                model=os.environ.get("MEDSORU_LLM_MODEL", "gemini-1.5-flash"),
                contents=prompt,
            )
            for chunk in stream:
                txt = getattr(chunk, "text", None)
                if txt:
                    loop.call_soon_threadsafe(queue.put_nowait, txt)
        except Exception as exc:  # noqa: BLE001
            loop.call_soon_threadsafe(queue.put_nowait, f"\n[hata: {exc}]")
        finally:
            loop.call_soon_threadsafe(queue.put_nowait, None)

    loop.run_in_executor(None, _produce)
    while True:
        tok = await queue.get()
        if tok is None:
            break
        yield tok


def _fallback_explanation(stem, options, hits) -> str:
    if not hits:
        return "Bu soru için slaytta doğrudan kanıt bulunamadı."
    ev = "\n".join(f"- {h.chunk_id}: {h.content[:220]}..." for h in hits[:3])
    return (f"Soru: {stem[:180]}\n\nSlayt kanıtları:\n{ev}\n\n"
            "Bu açıklama kanıt modunda (LLM devre dışı) üretildi.")


def _pseudo_tokens(text: str) -> Iterator[str]:
    buf = ""
    for ch in text:
        buf += ch
        if ch in " \n.,;:!?" or len(buf) >= 12:
            yield buf
            buf = ""
    if buf:
        yield buf


def _sse(event: str, data: dict[str, Any]) -> bytes:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n".encode("utf-8")


@app.post("/api/solve/stream")
async def api_solve_stream(req: SolveRequest) -> StreamingResponse:
    return StreamingResponse(
        _solve_stream(req), media_type="text/event-stream",
        headers={"Cache-Control": "no-cache",
                 "X-Accel-Buffering": "no",
                 "Connection": "keep-alive"},
    )


def _run_uvicorn() -> None:
    import uvicorn
    uvicorn.run(
        "scripts.fast_hybrid_server:app",
        host=os.environ.get("HOST", "0.0.0.0"),
        port=int(os.environ.get("PORT", "8000")),
        reload=False, log_level="info",
    )


if __name__ == "__main__":
    _run_uvicorn()
