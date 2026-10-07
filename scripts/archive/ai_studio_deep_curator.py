#!/usr/bin/env python3
"""MedSoru Gemini Shadow Judge — bozuk tıp sorularını AI Studio ile onarır."""
from __future__ import annotations

import argparse
import json
import logging
import os
import random
import re
import shutil
import sys
import tempfile
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator, Optional, Sequence

import duckdb
import pyarrow as pa
import pyarrow.dataset as ds
from pydantic import BaseModel, Field, ValidationError, field_validator

LOG = logging.getLogger("medsoru.curator")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
)

_TERM_CLEAN_RE = re.compile(r"[^\wçğıöşü\s\-]", re.UNICODE)


def sanitize_terms(terms: Sequence[str], max_terms: int = 8,
                   min_len: int = 4, max_len: int = 40) -> list[str]:
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


class DetectedEntities(BaseModel):
    diseases: list[str] = Field(default_factory=list)
    drugs: list[str] = Field(default_factory=list)
    symptoms: list[str] = Field(default_factory=list)


class CuratedQuestion(BaseModel):
    is_valid_medical_question: bool
    cleaned_stem: str
    options: dict[str, str]
    correct_answer: Optional[str] = None
    slide_evidence_exact_quote: str = ""
    clinical_reasoning: str = ""
    support_ratio: float = Field(ge=0.0, le=1.0)
    status: str
    detected_entities: DetectedEntities = Field(default_factory=DetectedEntities)

    @field_validator("options")
    @classmethod
    def _validate_options(cls, v: dict[str, str]) -> dict[str, str]:
        if not v:
            raise ValueError("options boş olamaz")
        for k in v:
            if k.upper() not in {"A", "B", "C", "D", "E"}:
                raise ValueError(f"Geçersiz şık harfi: {k}")
        return {k.upper(): (val or "").strip() for k, val in v.items()}

    @field_validator("correct_answer")
    @classmethod
    def _validate_correct(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        v = v.strip().upper()[:1]
        if v and v not in {"A", "B", "C", "D", "E"}:
            raise ValueError(f"Geçersiz doğru cevap: {v}")
        return v or None

    @field_validator("status")
    @classmethod
    def _validate_status(cls, v: str) -> str:
        if v not in {"verified", "fixed", "needs_fix", "rejected"}:
            raise ValueError(f"Geçersiz status: {v}")
        return v


@dataclass(slots=True)
class CuratorConfig:
    lake: Path
    model: str = "gemini-1.5-pro"
    api_key_env: str = "GEMINI_API_KEY"
    max_retries: int = 5
    base_backoff: float = 2.0
    max_backoff: float = 90.0
    batch_size: int = 25
    top_k_evidence: int = 6
    min_support: float = 0.85
    dry_run: bool = False

    @property
    def chunks_glob(self) -> str:
        return str(self.lake / "chunks" / "**" / "*.parquet")

    @property
    def questions_glob(self) -> str:
        return str(self.lake / "questions" / "**" / "*.parquet")

    @property
    def questions_dir(self) -> Path:
        return self.lake / "questions"


class LakeReader:
    def __init__(self, cfg: CuratorConfig) -> None:
        self.cfg = cfg
        self._master = duckdb.connect(":memory:")
        self._master.execute("SET threads TO 4;")
        self._master.execute("PRAGMA memory_limit='2GB';")

    @contextmanager
    def connect(self) -> Iterator[duckdb.DuckDBPyConnection]:
        cur = self._master.cursor()
        try:
            yield cur
        finally:
            cur.close()

    def fetch_repair_queue(self, limit: int = 100) -> list[dict[str, Any]]:
        with self.connect() as con:
            q = f"""
                SELECT *
                FROM read_parquet('{self.cfg.questions_glob}', hive_partitioning=true)
                WHERE status = 'needs_fix'
                    OR support_ratio < {float(self.cfg.min_support)}
                    OR array_length(map_keys(options)) < 5
                    OR correct_answer IS NULL
                LIMIT {int(limit)};
            """
            rows = con.execute(q).fetchall()
            cols = [d[0] for d in con.description]
            return [dict(zip(cols, r)) for r in rows]

    def fetch_evidence(self, donem: int, komite: int, ders: str, keywords: Sequence[str], top_k: int):
        with self.connect() as con:
            terms = sanitize_terms(keywords, max_terms=8, min_len=4)
            score_expr, score_params = build_sparse_score_sql(terms)
            q = f"""
                SELECT chunk_id, donem, komite, ders,
                       source_file, page_num, heading_path, content,
                       medical_entities,
                       ({score_expr}) AS kw_score
                FROM read_parquet('{self.cfg.chunks_glob}', hive_partitioning=true)
                WHERE donem = ? AND komite = ?
                  AND (? = 'Genel' OR ders = ?)
                ORDER BY kw_score DESC, token_count DESC
                LIMIT {int(top_k)};
            """
            params: list[Any] = [*score_params, donem, komite, ders, ders]
            rows = con.execute(q, params).fetchall()
            cols = [d[0] for d in con.description]
            return [dict(zip(cols, r)) for r in rows]

    def close(self) -> None:
        try:
            self._master.close()
        except Exception:  # noqa: BLE001
            pass


class GeminiClient:
    SYSTEM_PROMPT = (
        "Sen Tıp Fakültesi Sınav Değerlendirme Kurul Başkanısın. "
        "Sana verilen amfi ders slaytlarını TEK HAKİKAT kabul edeceksin. "
        "Dışarıdan tıbbi bilgi UYDURMAYACAKSIN (Sıfır Halüsinasyon). "
        "Soru kökünü, A-B-C-D-E şıklarını ayrıştıracak, doğru cevabı "
        "yalnızca slayt referansıyla gerekçelendireceksin. "
        "Slaytta kanıtı bulunmayan hiçbir soruyu 'verified' veya 'fixed' "
        "olarak işaretlemeyeceksin; support_ratio < 0.85 ise 'needs_fix' "
        "veya 'rejected' döneceksin. Yanıtını yalnızca istenen JSON şemasıyla vereceksin."
    )

    def __init__(self, cfg: CuratorConfig) -> None:
        api_key = os.environ.get(cfg.api_key_env)
        if not api_key:
            raise RuntimeError(f"{cfg.api_key_env} ortam değişkeni ayarlı değil.")
        try:
            from google import genai  # type: ignore
            from google.genai import types as genai_types  # type: ignore
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError("google-genai SDK yüklü değil.") from exc
        self._types = genai_types
        self._client = genai.Client(api_key=api_key)
        self.cfg = cfg

    def _sleep_backoff(self, attempt: int) -> None:
        delay = min(self.cfg.base_backoff * (2 ** attempt), self.cfg.max_backoff)
        jitter = random.uniform(0, delay * 0.25)
        total = delay + jitter
        LOG.warning("Backoff %.1fs (attempt=%d)", total, attempt + 1)
        time.sleep(total)

    def curate(self, raw_question: dict[str, Any], evidence_chunks: list[dict[str, Any]]) -> Optional[CuratedQuestion]:
        user_payload = self._build_user_payload(raw_question, evidence_chunks)
        response_schema = {
            "type": "object",
            "properties": {
                "is_valid_medical_question": {"type": "boolean"},
                "cleaned_stem": {"type": "string"},
                "options": {
                    "type": "object",
                    "properties": {k: {"type": "string"} for k in "ABCDE"},
                    "required": list("ABCDE"),
                },
                "correct_answer": {"type": "string", "nullable": True},
                "slide_evidence_exact_quote": {"type": "string"},
                "clinical_reasoning": {"type": "string"},
                "support_ratio": {"type": "number"},
                "status": {"type": "string",
                           "enum": ["verified", "fixed", "needs_fix", "rejected"]},
                "detected_entities": {
                    "type": "object",
                    "properties": {
                        "diseases": {"type": "array", "items": {"type": "string"}},
                        "drugs": {"type": "array", "items": {"type": "string"}},
                        "symptoms": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["diseases", "drugs", "symptoms"],
                },
            },
            "required": [
                "is_valid_medical_question", "cleaned_stem", "options",
                "slide_evidence_exact_quote", "clinical_reasoning",
                "support_ratio", "status", "detected_entities",
            ],
        }
        last_exc: Optional[Exception] = None
        for attempt in range(self.cfg.max_retries):
            try:
                resp = self._client.models.generate_content(
                    model=self.cfg.model,
                    contents=user_payload,
                    config=self._types.GenerateContentConfig(
                        system_instruction=self.SYSTEM_PROMPT,
                        temperature=0.0, top_p=0.1,
                        response_mime_type="application/json",
                        response_schema=response_schema,
                    ),
                )
                raw_text = (resp.text or "").strip()
                if not raw_text:
                    raise RuntimeError("Gemini boş yanıt döndü.")
                parsed = json.loads(raw_text)
                return CuratedQuestion.model_validate(parsed)
            except ValidationError as exc:
                LOG.error("Schema validation hatası: %s", exc)
                last_exc = exc
                if attempt >= 1:
                    break
            except Exception as exc:  # noqa: BLE001
                msg = str(exc).lower()
                last_exc = exc
                if any(k in msg for k in ("429", "rate", "quota", "resource_exhausted")):
                    self._sleep_backoff(attempt)
                    continue
                if any(k in msg for k in ("500", "503", "unavailable")):
                    self._sleep_backoff(attempt)
                    continue
                LOG.error("Gemini hatası: %s", exc)
                self._sleep_backoff(attempt)
        LOG.error("Curate başarısız. Son hata: %s", last_exc)
        return None

    @staticmethod
    def _build_user_payload(raw_question: dict[str, Any], evidence_chunks: list[dict[str, Any]]) -> str:
        raw_view = {
            "question_id": raw_question.get("question_id"),
            "ders": raw_question.get("ders"),
            "donem": raw_question.get("donem"),
            "komite": raw_question.get("komite"),
            "stem": raw_question.get("stem"),
            "options": raw_question.get("options"),
            "correct_answer": raw_question.get("correct_answer"),
            "explanation": raw_question.get("explanation"),
            "status": raw_question.get("status"),
        }
        blocks: list[str] = []
        for i, chunk in enumerate(evidence_chunks, start=1):
            blocks.append(
                f"[EVIDENCE {i}]\n"
                f"chunk_id: {chunk.get('chunk_id')}\n"
                f"source: {chunk.get('source_file')} p.{chunk.get('page_num')}\n"
                f"heading: {' > '.join(chunk.get('heading_path') or [])}\n"
                f"content:\n{chunk.get('content')}\n"
            )
        evidence_text = "\n".join(blocks) if blocks else "(KANIT BULUNAMADI)"
        return (
            "Aşağıdaki bozuk sınav sorusunu, yalnızca kanıt bloklarına dayanarak "
            "yeniden inşa et. Kanıt yoksa status='rejected' döndür.\n\n"
            f"### HAM SORU\n{json.dumps(raw_view, ensure_ascii=False, indent=2)}\n\n"
            f"### AMFİ SLAYT KANITLARI\n{evidence_text}\n"
        )


class QuestionStore:
    def __init__(self, cfg: CuratorConfig) -> None:
        self.cfg = cfg
        self.questions_dir = cfg.questions_dir

    def write_fixes(self, fixes: Sequence[dict[str, Any]]) -> int:
        if not fixes:
            return 0
        if self.cfg.dry_run:
            LOG.info("[DRY-RUN] %d düzeltme yazılmayacak.", len(fixes))
            return 0
        tmp_root = Path(tempfile.mkdtemp(prefix="curator_stage_", dir=str(self.cfg.lake)))
        try:
            fixed_ids = [f["question_id"] for f in fixes]
            new_tbl = _rows_to_arrow(fixes)
            ds.write_dataset(new_tbl, base_dir=str(tmp_root / "_new"), format="parquet")
            staging_glob = str(tmp_root / "_new" / "**" / "*.parquet")
            con = duckdb.connect(":memory:")
            try:
                con.execute("SET threads TO 4;")
                placeholders = ",".join(["?"] * len(fixed_ids))
                merge_sql = f"""
                    COPY (
                        SELECT * FROM read_parquet('{self.cfg.questions_glob}',
                                                   hive_partitioning=true)
                        WHERE question_id NOT IN ({placeholders})
                        UNION ALL
                        SELECT * FROM read_parquet('{staging_glob}')
                    )
                    TO '{tmp_root / "merged"}' (
                        FORMAT PARQUET, COMPRESSION ZSTD, COMPRESSION_LEVEL 9,
                        PARTITION_BY (donem, komite, ders), OVERWRITE_OR_IGNORE
                    );
                """
                con.execute(merge_sql, fixed_ids)
            finally:
                con.close()
            backup = self.questions_dir.with_suffix(".bak")
            if backup.exists():
                shutil.rmtree(backup, ignore_errors=True)
            self.questions_dir.rename(backup)
            (tmp_root / "merged").rename(self.questions_dir)
            shutil.rmtree(backup, ignore_errors=True)
            LOG.info("Yazıldı: %d onarılmış soru (swap tamam).", len(fixes))
            return len(fixes)
        finally:
            shutil.rmtree(tmp_root, ignore_errors=True)


def _rows_to_arrow(rows: Sequence[dict[str, Any]]) -> pa.Table:
    fields = [
        ("question_id", pa.string()), ("donem", pa.int16()),
        ("komite", pa.int16()), ("ders", pa.string()),
        ("academic_year", pa.string()), ("exam_type", pa.string()),
        ("stem", pa.string()), ("options", pa.map_(pa.string(), pa.string())),
        ("correct_answer", pa.string()), ("explanation", pa.string()),
        ("evidence_chunk_ids", pa.list_(pa.string())),
        ("support_ratio", pa.float32()), ("status", pa.string()),
        ("difficulty", pa.string()), ("clinical_tags", pa.list_(pa.string())),
    ]
    schema = pa.schema(fields)
    cols: dict[str, list[Any]] = {f[0]: [] for f in fields}
    for r in rows:
        for k, _ in fields:
            cols[k].append(r.get(k))
    arrays = {
        "question_id": pa.array(cols["question_id"], type=pa.string()),
        "donem": pa.array(cols["donem"], type=pa.int16()),
        "komite": pa.array(cols["komite"], type=pa.int16()),
        "ders": pa.array(cols["ders"], type=pa.string()),
        "academic_year": pa.array(cols["academic_year"], type=pa.string()),
        "exam_type": pa.array(cols["exam_type"], type=pa.string()),
        "stem": pa.array(cols["stem"], type=pa.string()),
        "options": pa.array(
            [list((o or {}).items()) for o in cols["options"]],
            type=pa.map_(pa.string(), pa.string()),
        ),
        "correct_answer": pa.array(cols["correct_answer"], type=pa.string()),
        "explanation": pa.array(cols["explanation"], type=pa.string()),
        "evidence_chunk_ids": pa.array(cols["evidence_chunk_ids"],
                                       type=pa.list_(pa.string())),
        "support_ratio": pa.array(cols["support_ratio"], type=pa.float32()),
        "status": pa.array(cols["status"], type=pa.string()),
        "difficulty": pa.array(cols["difficulty"], type=pa.string()),
        "clinical_tags": pa.array(cols["clinical_tags"], type=pa.list_(pa.string())),
    }
    return pa.table(arrays, schema=schema)


class DeepCurator:
    def __init__(self, cfg: CuratorConfig) -> None:
        self.cfg = cfg
        self.reader = LakeReader(cfg)
        self.store = QuestionStore(cfg)
        self.client = GeminiClient(cfg)

    @staticmethod
    def _keywords(question: dict[str, Any]) -> list[str]:
        text = " ".join([
            str(question.get("stem") or ""),
            " ".join((question.get("options") or {}).values()
                     if isinstance(question.get("options"), dict) else []),
        ]).lower()
        tokens = re.findall(r"[a-zçğıöşü]{4,}", text)
        stop = {"hangi", "aşağıdaki", "değildir", "olan", "veya", "çünkü",
                "olarak", "ile", "için", "bir", "the", "with", "patient"}
        return [t for t in tokens if t not in stop][:16]

    def _to_row(self, q_raw: dict[str, Any], curated: CuratedQuestion) -> dict[str, Any]:
        status = curated.status
        if curated.support_ratio < self.cfg.min_support and status in {"verified", "fixed"}:
            status = "needs_fix"
        if not curated.is_valid_medical_question and status != "rejected":
            status = "rejected"
        entities = curated.detected_entities
        tags = list(dict.fromkeys(
            entities.diseases + entities.drugs + entities.symptoms
        ))[:20]
        return {
            "question_id": q_raw.get("question_id"),
            "donem": int(q_raw.get("donem") or 0),
            "komite": int(q_raw.get("komite") or 0),
            "ders": q_raw.get("ders") or "Genel",
            "academic_year": q_raw.get("academic_year"),
            "exam_type": q_raw.get("exam_type"),
            "stem": curated.cleaned_stem.strip(),
            "options": curated.options,
            "correct_answer": curated.correct_answer,
            "explanation": curated.clinical_reasoning.strip(),
            "evidence_chunk_ids": [
                c.get("chunk_id") for c in (q_raw.get("_evidence") or [])
                if c.get("chunk_id")
            ],
            "support_ratio": float(curated.support_ratio),
            "status": status,
            "difficulty": q_raw.get("difficulty"),
            "clinical_tags": tags,
        }

    def run(self, max_questions: int = 200) -> dict[str, int]:
        queue = self.reader.fetch_repair_queue(limit=max_questions)
        LOG.info("Onarım kuyruğu: %d soru", len(queue))
        stats = {"processed": 0, "fixed": 0, "rejected": 0, "failed": 0}
        fixes_buffer: list[dict[str, Any]] = []
        try:
            for idx, q in enumerate(queue, start=1):
                kw = self._keywords(q)
                evidence = self.reader.fetch_evidence(
                    donem=int(q.get("donem") or 0),
                    komite=int(q.get("komite") or 0),
                    ders=q.get("ders") or "Genel",
                    keywords=kw, top_k=self.cfg.top_k_evidence,
                )
                q["_evidence"] = evidence
                curated = self.client.curate(q, evidence)
                stats["processed"] += 1
                if curated is None:
                    stats["failed"] += 1
                else:
                    row = self._to_row(q, curated)
                    fixes_buffer.append(row)
                    if row["status"] in {"verified", "fixed"}:
                        stats["fixed"] += 1
                    elif row["status"] == "rejected":
                        stats["rejected"] += 1
                if len(fixes_buffer) >= self.cfg.batch_size:
                    self.store.write_fixes(fixes_buffer)
                    fixes_buffer.clear()
                if idx % 10 == 0:
                    LOG.info("İlerleme: %d/%d | %s", idx, len(queue), stats)
            if fixes_buffer:
                self.store.write_fixes(fixes_buffer)
        finally:
            self.reader.close()
        LOG.info("Curator tamamlandı: %s", stats)
        return stats


def _parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="MedSoru Gemini Shadow Judge")
    p.add_argument("--lake", default="./meds_lake")
    p.add_argument("--model", default="gemini-1.5-pro",
                   choices=["gemini-1.5-pro", "gemini-1.5-flash",
                            "gemini-2.0-flash-exp"])
    p.add_argument("--max", type=int, default=200)
    p.add_argument("--batch-size", type=int, default=25)
    p.add_argument("--min-support", type=float, default=0.85)
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = _parse_args(argv)
    cfg = CuratorConfig(
        lake=Path(args.lake).resolve(), model=args.model,
        batch_size=args.batch_size, min_support=args.min_support,
        dry_run=args.dry_run,
    )
    if not cfg.lake.exists():
        LOG.error("Göl dizini bulunamadı: %s", cfg.lake)
        return 2
    curator = DeepCurator(cfg)
    curator.run(max_questions=args.max)
    return 0


if __name__ == "__main__":
    sys.exit(main())
