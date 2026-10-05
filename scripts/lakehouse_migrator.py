#!/usr/bin/env python3
"""MedSoru Medical Lakehouse Builder — JSON/JSONL/SQLite → Parquet gölü."""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import re
import sqlite3
import sys
import time
import unicodedata
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator, Optional, Protocol, Sequence

import duckdb
import numpy as np
import pyarrow as pa
import pyarrow.dataset as ds

LOG = logging.getLogger("medsoru.lakehouse")
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
# MedSoru standart mimarisi: bge-m3 (1024d)
DEFAULT_EMBED_MODEL = os.environ.get("MEDSORU_EMBED_MODEL", "bge-m3")

DEFAULT_CHUNK_CHARS = 900
DEFAULT_CHUNK_OVERLAP = 120
VALID_STATUS = {"verified", "fixed", "needs_fix", "rejected"}
VALID_DIFFICULTY = {"Kolay", "Orta", "Zor", "Vaka"}

_DRUG_SUFFIXES = ("mab", "nib", "pril", "sartan", "olol", "statyn", "statin",
                  "mycin", "cillin", "cycline", "prazole", "azepam", "azolam")
_ENTITY_REGEX = re.compile(
    r"\b([A-ZÇĞİÖŞÜ][a-zçğıöşü]{2,}(?:\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]{2,}){0,3})\b"
)


def resolve_embed_spec(model_name: Optional[str] = None) -> tuple[str, int, int]:
    name = (model_name or DEFAULT_EMBED_MODEL).lower()
    if name not in EMBEDDING_REGISTRY:
        raise ValueError(
            f"Bilinmeyen embedding modeli: {name}. Geçerli: {list(EMBEDDING_REGISTRY)}"
        )
    return EMBEDDING_REGISTRY[name]


def chunks_schema(embed_dim: int) -> pa.Schema:
    return pa.schema([
        pa.field("chunk_id", pa.string(), nullable=False),
        pa.field("donem", pa.int16(), nullable=False),
        pa.field("komite", pa.int16(), nullable=False),
        pa.field("ders", pa.string(), nullable=False),
        pa.field("source_file", pa.string()),
        pa.field("page_num", pa.int32()),
        pa.field("heading_path", pa.list_(pa.string())),
        pa.field("content", pa.string()),
        pa.field("medical_entities", pa.list_(pa.string())),
        pa.field("embedding", pa.list_(pa.float32(), embed_dim)),
        pa.field("token_count", pa.int32()),
        pa.field("created_at", pa.timestamp("us", tz="UTC")),
    ])


def questions_schema() -> pa.Schema:
    return pa.schema([
        pa.field("question_id", pa.string(), nullable=False),
        pa.field("donem", pa.int16(), nullable=False),
        pa.field("komite", pa.int16(), nullable=False),
        pa.field("ders", pa.string(), nullable=False),
        pa.field("academic_year", pa.string()),
        pa.field("exam_type", pa.string()),
        pa.field("stem", pa.string()),
        pa.field("options", pa.map_(pa.string(), pa.string())),
        pa.field("correct_answer", pa.string()),
        pa.field("explanation", pa.string()),
        pa.field("evidence_chunk_ids", pa.list_(pa.string())),
        pa.field("support_ratio", pa.float32()),
        pa.field("status", pa.string()),
        pa.field("difficulty", pa.string()),
        pa.field("clinical_tags", pa.list_(pa.string())),
    ])


CHUNK_PARTITIONS = pa.schema([("donem", pa.int16()),
                              ("komite", pa.int16()),
                              ("ders", pa.string())])
QUESTION_PARTITIONS = CHUNK_PARTITIONS


@dataclass(slots=True)
class LakehouseConfig:
    root: Path
    lake: Path
    embed_model: str = DEFAULT_EMBED_MODEL
    embed_dim: int = 1024
    chunk_chars: int = DEFAULT_CHUNK_CHARS
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP
    zstd_level: int = 9
    max_rows_per_file: int = 200_000
    max_rows_per_group: int = 50_000
    flush_every: int = 20_000
    source_dirs: tuple[Path, ...] = field(default_factory=tuple)

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> "LakehouseConfig":
        root = Path(args.root).resolve()
        lake = Path(args.lake).resolve()
        dirs = (
            root / "meds_temp" / "temp3",
            root / "meds_database",
            root / "meds_temp" / "state",
        )
        return cls(
            root=root, lake=lake,
            embed_model=args.embed_model,
            embed_dim=args.embed_dim,
            chunk_chars=args.chunk_chars,
            chunk_overlap=args.chunk_overlap,
            source_dirs=dirs,
        )


class Embedder(Protocol):
    dim: int
    def encode(self, texts: Sequence[str]) -> np.ndarray: ...


class HashEmbedder:
    def __init__(self, dim: int) -> None:
        self.dim = dim

    def _vec(self, text: str) -> np.ndarray:
        h = hashlib.blake2b(text.encode("utf-8"), digest_size=64).digest()
        seed = int.from_bytes(h[:8], "little", signed=False)
        rng = np.random.default_rng(seed)
        v = rng.standard_normal(self.dim, dtype=np.float32)
        n = float(np.linalg.norm(v))
        return v / (n if n > 0 else 1.0)

    def encode(self, texts: Sequence[str]) -> np.ndarray:
        if not texts:
            return np.zeros((0, self.dim), dtype=np.float32)
        return np.stack([self._vec(t) for t in texts], axis=0)


class SentenceTransformerEmbedder:
    def __init__(self, hf_id: str, dim: int, max_len: int, prefix: str = "") -> None:
        try:
            from sentence_transformers import SentenceTransformer  # type: ignore
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError("sentence-transformers yüklü değil.") from exc
        LOG.info("Embedding modeli yükleniyor: %s (dim=%d)", hf_id, dim)
        self._model = SentenceTransformer(hf_id, device="cpu")
        self._model.max_seq_length = max_len
        self._prefix = prefix
        try:
            actual = int(self._model.get_sentence_embedding_dimension())
            self.dim = actual
            if actual != dim:
                LOG.warning("Model dim=%d, beklenen=%d", actual, dim)
        except Exception:  # noqa: BLE001
            self.dim = dim

    def encode(self, texts: Sequence[str]) -> np.ndarray:
        if not texts:
            return np.zeros((0, self.dim), dtype=np.float32)
        prefixed = [self._prefix + t for t in texts]
        vecs = self._model.encode(
            prefixed, batch_size=32, normalize_embeddings=True,
            convert_to_numpy=True, show_progress_bar=False,
        )
        return vecs.astype(np.float32, copy=False)


def build_embedder(model_name: str) -> Embedder:
    name = (model_name or DEFAULT_EMBED_MODEL).lower()
    try:
        hf_id, dim, max_len = resolve_embed_spec(name)
    except ValueError as exc:
        LOG.error("%s → HashEmbedder fallback", exc)
        return HashEmbedder(dim=1024)
    prefix = "passage: " if name.startswith("e5") else ""
    try:
        return SentenceTransformerEmbedder(hf_id, dim, max_len, prefix=prefix)
    except Exception as exc:  # noqa: BLE001
        LOG.warning("%s yüklenemedi (%s). HashEmbedder fallback (dim=%d).", name, exc, dim)
        return HashEmbedder(dim=dim)


_WS_RE = re.compile(r"[ \t]+")
_NL_RE = re.compile(r"\n{3,}")


def normalize_text(text: str) -> str:
    if not text:
        return ""
    t = unicodedata.normalize("NFKC", text)
    t = t.replace("\u00ad", "").replace("\ufeff", "")
    t = _WS_RE.sub(" ", t)
    t = _NL_RE.sub("\n\n", t)
    return t.strip()


def token_count(text: str) -> int:
    return len(re.findall(r"\S+", text))


def extract_medical_entities(text: str, limit: int = 32) -> list[str]:
    if not text:
        return []
    found: dict[str, None] = {}
    for m in _ENTITY_REGEX.finditer(text):
        cand = m.group(1).strip()
        if len(cand) < 3 or cand.lower() in {"the", "and", "bir", "ile", "ve"}:
            continue
        found.setdefault(cand, None)
        if len(found) >= limit * 2:
            break
    for word in re.findall(r"\b[a-zçğıöşü]{4,}\b", text.lower()):
        if word.endswith(_DRUG_SUFFIXES):
            found.setdefault(word.capitalize(), None)
    return list(found.keys())[:limit]


def _split_with_overlap(text: str, size: int, overlap: int) -> list[str]:
    if len(text) <= size:
        return [text.strip()] if text.strip() else []
    chunks: list[str] = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + size, n)
        if end < n:
            window = text[start:end]
            for sep in ("\n\n", ". ", ".\n", "\n"):
                idx = window.rfind(sep)
                if idx > size * 0.6:
                    end = start + idx + len(sep)
                    break
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= n:
            break
        start = max(end - overlap, start + 1)
    return chunks


def _safe_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, (dict, list)):
        try:
            return json.dumps(value, ensure_ascii=False)
        except Exception:  # noqa: BLE001
            return str(value)
    return str(value)


def _to_int16(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:  # noqa: BLE001
        return default


def _parse_page(value: Any) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    m = re.search(r"\d+", str(value))
    return int(m.group()) if m else None


@dataclass(slots=True)
class ChunkRow:
    chunk_id: str
    donem: int
    komite: int
    ders: str
    source_file: str
    page_num: Optional[int]
    heading_path: list[str]
    content: str
    medical_entities: list[str]
    token_count: int
    created_at: datetime
    existing_embedding: Optional[list[float]] = None

    def to_arrow_dict(self, embedding: np.ndarray) -> dict[str, Any]:
        return {
            "chunk_id": self.chunk_id, "donem": self.donem, "komite": self.komite,
            "ders": self.ders, "source_file": self.source_file,
            "page_num": self.page_num, "heading_path": self.heading_path,
            "content": self.content, "medical_entities": self.medical_entities,
            "embedding": embedding.astype(np.float32).tolist(),
            "token_count": self.token_count, "created_at": self.created_at,
        }


@dataclass(slots=True)
class QuestionRow:
    question_id: str
    donem: int
    komite: int
    ders: str
    academic_year: Optional[str]
    exam_type: Optional[str]
    stem: str
    options: dict[str, str]
    correct_answer: Optional[str]
    explanation: Optional[str]
    evidence_chunk_ids: list[str]
    support_ratio: float
    status: str
    difficulty: Optional[str]
    clinical_tags: list[str]

    def to_arrow_dict(self) -> dict[str, Any]:
        return {
            "question_id": self.question_id, "donem": self.donem,
            "komite": self.komite, "ders": self.ders,
            "academic_year": self.academic_year, "exam_type": self.exam_type,
            "stem": self.stem,
            "options": list(self.options.items()) if self.options else [],
            "correct_answer": self.correct_answer,
            "explanation": self.explanation,
            "evidence_chunk_ids": self.evidence_chunk_ids,
            "support_ratio": float(self.support_ratio),
            "status": self.status, "difficulty": self.difficulty,
            "clinical_tags": self.clinical_tags,
        }


class SourceScanner:
    def __init__(self, dirs: Sequence[Path]) -> None:
        self.dirs = [Path(d) for d in dirs]

    def _iter_json(self, path: Path) -> Iterator[dict[str, Any]]:
        try:
            with path.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception as exc:  # noqa: BLE001
            LOG.warning("JSON okunamadı %s: %s", path, exc)
            return
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    yield item
        elif isinstance(data, dict):
            yielded = False
            for v in data.values():
                if isinstance(v, list):
                    for item in v:
                        if isinstance(item, dict):
                            yield item
                            yielded = True
            if not yielded:
                yield data

    def _iter_jsonl(self, path: Path) -> Iterator[dict[str, Any]]:
        try:
            with path.open("r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if isinstance(obj, dict):
                        yield obj
        except Exception as exc:  # noqa: BLE001
            LOG.warning("JSONL okunamadı %s: %s", path, exc)

    def _iter_sqlite(self, path: Path) -> Iterator[dict[str, Any]]:
        try:
            conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        except Exception as exc:  # noqa: BLE001
            LOG.warning("SQLite açılamadı %s: %s", path, exc)
            return
        try:
            cur = conn.cursor()
            tables = [
                r[0] for r in cur.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
            ]
            for table in tables:
                try:
                    cur.execute(f'SELECT * FROM "{table}"')  # noqa: S608
                    cols = [d[0] for d in cur.description]
                    for row in cur.fetchall():
                        yield dict(zip(cols, row))
                except sqlite3.DatabaseError as exc:
                    LOG.warning("Tablo okunamadı %s.%s: %s", path.name, table, exc)
        finally:
            conn.close()

    def iter_all(self) -> Iterator[tuple[Path, dict[str, Any]]]:
        for base in self.dirs:
            if not base.exists():
                LOG.info("Kaynak dizin yok: %s", base)
                continue
            for path in sorted(base.rglob("*")):
                if not path.is_file():
                    continue
                suffix = path.suffix.lower()
                if suffix == ".json":
                    for rec in self._iter_json(path):
                        yield path, rec
                elif suffix in {".jsonl", ".ndjson"}:
                    for rec in self._iter_jsonl(path):
                        yield path, rec
                elif suffix in {".sqlite", ".db", ".sqlite3"}:
                    for rec in self._iter_sqlite(path):
                        yield path, rec


class RecordMapper:
    _CHUNK_HINTS = ("content", "text", "chunk", "paragraph", "passage")
    _QUESTION_HINTS = ("stem", "question", "soru", "options", "şıklar")

    @classmethod
    def classify(cls, rec: dict[str, Any]) -> str:
        keys = {str(k).lower() for k in rec.keys()}
        if any(h in keys for h in cls._QUESTION_HINTS):
            if any(k in keys for k in ("options", "şıklar", "choices")):
                return "question"
        if any(h in keys for h in cls._CHUNK_HINTS):
            return "chunk"
        return "unknown"

    @staticmethod
    def _norm_options(value: Any) -> dict[str, str]:
        if value is None:
            return {}
        if isinstance(value, dict):
            return {str(k).upper(): _safe_str(v) or "" for k, v in value.items()}
        if isinstance(value, list):
            letters = "ABCDEFGH"
            return {letters[i]: _safe_str(v) or "" for i, v in enumerate(value[:8])}
        if isinstance(value, str):
            parts = re.split(r"(?m)^\s*([A-E])[\).:\-]\s*", value)
            out: dict[str, str] = {}
            i = 1
            while i + 1 < len(parts):
                out[parts[i].upper()] = parts[i + 1].strip()
                i += 2
            return out
        return {}

    @classmethod
    def to_chunk(cls, raw, source_path, cfg, part_index) -> Optional[ChunkRow]:
        content = ""
        for key in ("content", "text", "chunk", "paragraph", "passage", "body"):
            v = raw.get(key)
            if v:
                content = _safe_str(v) or ""
                break
        content = normalize_text(content)
        if len(content) < 40:
            return None
        source_id = _safe_str(
            raw.get("source_id") or raw.get("source")
            or raw.get("file") or source_path.stem
        ) or source_path.stem
        page = _parse_page(raw.get("page_num") or raw.get("page") or raw.get("sayfa"))
        donem = _to_int16(raw.get("donem") or raw.get("semester"), 0)
        komite = _to_int16(raw.get("komite") or raw.get("committee"), 0)
        ders = _safe_str(raw.get("ders") or raw.get("course") or raw.get("lesson")) or "Genel"
        heading_path = raw.get("heading_path") or raw.get("headings") or []
        if isinstance(heading_path, str):
            heading_path = [h.strip() for h in heading_path.split(">") if h.strip()]
        if not isinstance(heading_path, list):
            heading_path = []
        chunk_id = f"{source_id}:p{page if page is not None else 0}:c{part_index}"
        
        # Önceden hesaplanmış embedding var mı kontrol et (BGE-M3 1024d)
        existing_emb = raw.get("embedding")
        if isinstance(existing_emb, list) and len(existing_emb) == cfg.embed_dim:
            clean_emb = existing_emb
        else:
            clean_emb = None

        return ChunkRow(
            chunk_id=chunk_id, donem=donem, komite=komite, ders=ders,
            source_file=source_path.name, page_num=page,
            heading_path=[_safe_str(h) or "" for h in heading_path],
            content=content, medical_entities=extract_medical_entities(content),
            token_count=token_count(content),
            created_at=datetime.now(tz=timezone.utc),
            existing_embedding=clean_emb,
        )

    @classmethod
    def to_question(cls, raw, source_path) -> Optional[QuestionRow]:
        stem = ""
        for key in ("stem", "question", "soru", "text"):
            v = raw.get(key)
            if v:
                stem = _safe_str(v) or ""
                break
        stem = normalize_text(stem)
        if len(stem) < 10:
            return None
        options = cls._norm_options(
            raw.get("options") or raw.get("şıklar") or raw.get("choices")
        )
        correct = raw.get("correct_answer") or raw.get("answer") or raw.get("doğru_cevap")
        correct = _safe_str(correct)
        if correct:
            correct = correct.strip().upper()[:1] or None
        evidence = raw.get("evidence_chunk_ids") or raw.get("evidence") or []
        if isinstance(evidence, str):
            evidence = [e.strip() for e in evidence.split(",") if e.strip()]
        if not isinstance(evidence, list):
            evidence = []
        try:
            support = float(raw.get("support_ratio") or raw.get("support") or 0.0)
        except Exception:  # noqa: BLE001
            support = 0.0
        status = _safe_str(raw.get("status") or "needs_fix") or "needs_fix"
        if status not in VALID_STATUS:
            status = "needs_fix"
        difficulty = _safe_str(raw.get("difficulty") or raw.get("zorluk"))
        if difficulty and difficulty not in VALID_DIFFICULTY:
            difficulty = None
        qid = _safe_str(
            raw.get("question_id") or raw.get("id")
            or f"q-{hashlib.blake2b(stem.encode(), digest_size=8).hexdigest()}"
        ) or "q-unknown"
        return QuestionRow(
            question_id=qid,
            donem=_to_int16(raw.get("donem") or raw.get("semester"), 0),
            komite=_to_int16(raw.get("komite") or raw.get("committee"), 0),
            ders=_safe_str(raw.get("ders") or raw.get("course")) or "Genel",
            academic_year=_safe_str(raw.get("academic_year") or raw.get("yil")),
            exam_type=_safe_str(raw.get("exam_type") or raw.get("sinav_turu")),
            stem=stem, options=options, correct_answer=correct,
            explanation=_safe_str(raw.get("explanation") or raw.get("aciklama")),
            evidence_chunk_ids=[_safe_str(e) or "" for e in evidence],
            support_ratio=support, status=status, difficulty=difficulty,
            clinical_tags=[_safe_str(t) or "" for t in (raw.get("clinical_tags") or [])],
        )


def _arrow_chunks(rows: list[ChunkRow], embeddings: np.ndarray, schema: pa.Schema) -> pa.Table:
    data = [r.to_arrow_dict(emb) for r, emb in zip(rows, embeddings)]
    emb_type = schema.field("embedding").type
    arrays = {
        "chunk_id": pa.array([r["chunk_id"] for r in data], type=pa.string()),
        "donem": pa.array([r["donem"] for r in data], type=pa.int16()),
        "komite": pa.array([r["komite"] for r in data], type=pa.int16()),
        "ders": pa.array([r["ders"] for r in data], type=pa.string()),
        "source_file": pa.array([r["source_file"] for r in data], type=pa.string()),
        "page_num": pa.array([r["page_num"] for r in data], type=pa.int32()),
        "heading_path": pa.array([r["heading_path"] for r in data], type=pa.list_(pa.string())),
        "content": pa.array([r["content"] for r in data], type=pa.string()),
        "medical_entities": pa.array([r["medical_entities"] for r in data], type=pa.list_(pa.string())),
        "embedding": pa.array([r["embedding"] for r in data], type=emb_type),
        "token_count": pa.array([r["token_count"] for r in data], type=pa.int32()),
        "created_at": pa.array([r["created_at"] for r in data], type=pa.timestamp("us", tz="UTC")),
    }
    return pa.table(arrays, schema=schema)


def _arrow_questions(rows: list[QuestionRow], schema: pa.Schema) -> pa.Table:
    data = [r.to_arrow_dict() for r in rows]
    arrays = {
        "question_id": pa.array([r["question_id"] for r in data], type=pa.string()),
        "donem": pa.array([r["donem"] for r in data], type=pa.int16()),
        "komite": pa.array([r["komite"] for r in data], type=pa.int16()),
        "ders": pa.array([r["ders"] for r in data], type=pa.string()),
        "academic_year": pa.array([r["academic_year"] for r in data], type=pa.string()),
        "exam_type": pa.array([r["exam_type"] for r in data], type=pa.string()),
        "stem": pa.array([r["stem"] for r in data], type=pa.string()),
        "options": pa.array([r["options"] for r in data], type=pa.map_(pa.string(), pa.string())),
        "correct_answer": pa.array([r["correct_answer"] for r in data], type=pa.string()),
        "explanation": pa.array([r["explanation"] for r in data], type=pa.string()),
        "evidence_chunk_ids": pa.array([r["evidence_chunk_ids"] for r in data], type=pa.list_(pa.string())),
        "support_ratio": pa.array([r["support_ratio"] for r in data], type=pa.float32()),
        "status": pa.array([r["status"] for r in data], type=pa.string()),
        "difficulty": pa.array([r["difficulty"] for r in data], type=pa.string()),
        "clinical_tags": pa.array([r["clinical_tags"] for r in data], type=pa.list_(pa.string())),
    }
    return pa.table(arrays, schema=schema)


class LakehouseBuilder:
    def __init__(self, cfg: LakehouseConfig, embedder: Optional[Embedder] = None) -> None:
        self.cfg = cfg
        self.embedder: Embedder = embedder or build_embedder(cfg.embed_model)
        self.cfg.embed_dim = self.embedder.dim
        self.chunks_dir = cfg.lake / "chunks"
        self.questions_dir = cfg.lake / "questions"
        self.rejects_dir = cfg.lake / "_rejects"
        for d in (self.chunks_dir, self.questions_dir, self.rejects_dir):
            d.mkdir(parents=True, exist_ok=True)
        self.chunks_schema = chunks_schema(self.embedder.dim)
        self.questions_schema = questions_schema()
        self._buf_chunks: list[ChunkRow] = []
        self._buf_questions: list[QuestionRow] = []
        self._rejects: list[dict[str, Any]] = []
        self._stats = {"scanned": 0, "chunk_written": 0,
                       "question_written": 0, "rejected": 0}

    def _flush_chunks(self) -> None:
        if not self._buf_chunks:
            return
        
        # Mevcut embedding'i olanları tespit et, olmayanları encode et
        missing_indices: list[int] = []
        texts_to_encode: list[str] = []
        for i, r in enumerate(self._buf_chunks):
            if r.existing_embedding is None or len(r.existing_embedding) != self.embedder.dim:
                missing_indices.append(i)
                texts_to_encode.append(r.content)

        embeddings = np.zeros((len(self._buf_chunks), self.embedder.dim), dtype=np.float32)
        for i, r in enumerate(self._buf_chunks):
            if r.existing_embedding is not None and len(r.existing_embedding) == self.embedder.dim:
                embeddings[i] = np.array(r.existing_embedding, dtype=np.float32)

        if texts_to_encode:
            encoded_vecs = self.embedder.encode(texts_to_encode)
            for local_idx, orig_idx in enumerate(missing_indices):
                embeddings[orig_idx] = encoded_vecs[local_idx]

        table = _arrow_chunks(self._buf_chunks, embeddings, self.chunks_schema)
        ds.write_dataset(
            table, base_dir=str(self.chunks_dir), format="parquet",
            partitioning=ds.partitioning(CHUNK_PARTITIONS, flavor="hive"),
            partitioning_flavor="hive",
            file_options=ds.ParquetFileFormat().make_write_options(
                compression="zstd", compression_level=self.cfg.zstd_level
            ),
            existing_data_behavior="overwrite_or_ignore",
            max_rows_per_file=self.cfg.max_rows_per_file,
            max_rows_per_group=self.cfg.max_rows_per_group,
        )
        self._stats["chunk_written"] += len(self._buf_chunks)
        LOG.info("chunk flush: +%d (total=%d)", len(self._buf_chunks),
                 self._stats["chunk_written"])
        self._buf_chunks.clear()

    def _flush_questions(self) -> None:
        if not self._buf_questions:
            return
        table = _arrow_questions(self._buf_questions, self.questions_schema)
        ds.write_dataset(
            table, base_dir=str(self.questions_dir), format="parquet",
            partitioning=ds.partitioning(QUESTION_PARTITIONS, flavor="hive"),
            partitioning_flavor="hive",
            file_options=ds.ParquetFileFormat().make_write_options(
                compression="zstd", compression_level=self.cfg.zstd_level
            ),
            existing_data_behavior="overwrite_or_ignore",
            max_rows_per_file=self.cfg.max_rows_per_file,
            max_rows_per_group=self.cfg.max_rows_per_group,
        )
        self._stats["question_written"] += len(self._buf_questions)
        LOG.info("question flush: +%d (total=%d)", len(self._buf_questions),
                 self._stats["question_written"])
        self._buf_questions.clear()

    def _flush_rejects(self) -> None:
        if not self._rejects:
            return
        path = self.rejects_dir / f"rejected_{int(time.time())}.jsonl"
        with path.open("w", encoding="utf-8") as fh:
            for r in self._rejects:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        LOG.warning("rejected: %s (%d)", path, len(self._rejects))
        self._stats["rejected"] += len(self._rejects)
        self._rejects.clear()

    def _add_reject(self, path: Path, reason: str, raw: dict[str, Any]) -> None:
        self._rejects.append({
            "source": str(path), "reason": reason,
            "raw_keys": list(raw.keys()),
            "raw_preview": {k: _safe_str(v) for k, v in list(raw.items())[:8]},
        })

    def ingest(self) -> dict[str, int]:
        scanner = SourceScanner(self.cfg.source_dirs)
        for path, raw in scanner.iter_all():
            self._stats["scanned"] += 1
            kind = RecordMapper.classify(raw)
            if kind == "chunk":
                content = ""
                for key in ("content", "text", "chunk", "paragraph", "passage", "body"):
                    v = raw.get(key)
                    if v:
                        content = _safe_str(v) or ""
                        break
                content = normalize_text(content)
                if not content:
                    self._add_reject(path, "empty_content", raw)
                    continue
                pieces = _split_with_overlap(
                    content, self.cfg.chunk_chars, self.cfg.chunk_overlap
                )
                for idx, piece in enumerate(pieces):
                    sub = dict(raw)
                    sub["content"] = piece
                    row = RecordMapper.to_chunk(sub, path, self.cfg, idx)
                    if row is not None:
                        self._buf_chunks.append(row)
            elif kind == "question":
                row = RecordMapper.to_question(raw, path)
                if row is None:
                    self._add_reject(path, "invalid_question", raw)
                    continue
                self._buf_questions.append(row)
            else:
                self._add_reject(path, "unknown_schema", raw)

            if len(self._buf_chunks) >= self.cfg.flush_every:
                self._flush_chunks()
            if len(self._buf_questions) >= self.cfg.flush_every:
                self._flush_questions()

        self._flush_chunks()
        self._flush_questions()
        self._flush_rejects()
        LOG.info("Ingest tamamlandı: %s", self._stats)
        return dict(self._stats)


def verify_lake(cfg: LakehouseConfig) -> None:
    con = duckdb.connect(":memory:")
    try:
        con.execute(f"SET threads TO {max(2, (os.cpu_count() or 4))};")
        chunks_glob = str(cfg.lake / "chunks" / "**" / "*.parquet")
        questions_glob = str(cfg.lake / "questions" / "**" / "*.parquet")
        con.execute(f"CREATE OR REPLACE VIEW chunks AS SELECT * FROM read_parquet('{chunks_glob}', hive_partitioning=true);")
        con.execute(f"CREATE OR REPLACE VIEW questions AS SELECT * FROM read_parquet('{questions_glob}', hive_partitioning=true);")
        total_chunks = con.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
        total_q = con.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
        null_chunk_ids = con.execute(
            "SELECT COUNT(*) FROM chunks WHERE chunk_id IS NULL OR content IS NULL"
        ).fetchone()[0]
        null_q_ids = con.execute(
            "SELECT COUNT(*) FROM questions WHERE question_id IS NULL OR stem IS NULL"
        ).fetchone()[0]
        distinct_embed_dim = con.execute(
            "SELECT DISTINCT array_length(embedding) FROM chunks LIMIT 5"
        ).fetchall()
        LOG.info("── DOĞRULAMA ──")
        LOG.info("embed model  : %s (dim=%d)", cfg.embed_model, cfg.embed_dim)
        LOG.info("chunks       : %d", total_chunks)
        LOG.info("questions    : %d", total_q)
        LOG.info("null chunk_id: %d", null_chunk_ids)
        LOG.info("null q_id    : %d", null_q_ids)
        LOG.info("embed dims   : %s", distinct_embed_dim)
        if total_chunks == 0:
            LOG.warning("chunks tablosu boş.")
        if null_chunk_ids or null_q_ids:
            LOG.error("NULL birincil anahtar!")
        if distinct_embed_dim and any(d[0] != cfg.embed_dim for d in distinct_embed_dim):
            LOG.error("Embedding boyutu tutarsız.")
    finally:
        con.close()


def _parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="MedSoru Medical Lakehouse Builder")
    p.add_argument("--root", default=".")
    p.add_argument("--lake", default="./meds_lake")
    p.add_argument("--embed-model", default=DEFAULT_EMBED_MODEL,
                   choices=list(EMBEDDING_REGISTRY.keys()))
    p.add_argument("--embed-dim", type=int, default=1024)
    p.add_argument("--chunk-chars", type=int, default=DEFAULT_CHUNK_CHARS)
    p.add_argument("--chunk-overlap", type=int, default=DEFAULT_CHUNK_OVERLAP)
    p.add_argument("--verify-only", action="store_true")
    return p.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = _parse_args(argv)
    cfg = LakehouseConfig.from_args(args)
    if args.embed_dim > 0:
        cfg.embed_dim = args.embed_dim
    else:
        _, dim, _ = resolve_embed_spec(cfg.embed_model)
        cfg.embed_dim = dim
    LOG.info("root=%s lake=%s embed_model=%s dim=%d",
             cfg.root, cfg.lake, cfg.embed_model, cfg.embed_dim)
    if not args.verify_only:
        builder = LakehouseBuilder(cfg)
        stats = builder.ingest()
        if stats["chunk_written"] == 0 and stats["question_written"] == 0:
            LOG.warning("Hiçbir kayıt yazılmadı. Kaynaklar: %s", cfg.source_dirs)
    verify_lake(cfg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
