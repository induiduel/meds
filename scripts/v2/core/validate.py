"""Kayıt bazlı doğrulama — denetçinin kalbi.

Her soru/parça/kaynak için `issues[]` kodları ve bir önem derecesi üretir. İki katman:
  - `blocking`: yayına/veritabanına girmemesi gereken ciddi sorunlar (şema hatası, boş kök, mojibake...)
  - `review`  : insan/LLM incelemesi gerektiren şüpheli durumlar (cevap bilinmiyor, statü tutarsızlığı...)

Bu modül salt-okunur çalışır; kaydı DEĞİŞTİRMEZ, yalnızca inceler.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Iterator

from . import schema, textnorm

try:
    from . import quality
except Exception:  # noqa: BLE001
    quality = None

STEM_MIN = 15
_EMBEDDED_OPT = re.compile(r"(?:^|\s)[A-E]\)\s", re.M)
_UNKNOWN_ANSWER = {"cevap bilinmiyor", "cevap yok", "bilinmiyor"}
_VALID_OPTION_KEYS = ("A", "B", "C", "D", "E")

SEVERITY_OK = "ok"
SEVERITY_REVIEW = "review"
SEVERITY_BLOCKING = "blocking"


@dataclass
class AuditResult:
    kind: str
    rid: str
    blocking: list[str] = field(default_factory=list)
    review: list[str] = field(default_factory=list)

    @property
    def issues(self) -> list[str]:
        return self.blocking + self.review

    @property
    def severity(self) -> str:
        if self.blocking:
            return SEVERITY_BLOCKING
        if self.review:
            return SEVERITY_REVIEW
        return SEVERITY_OK

    def ok(self) -> bool:
        return not self.issues


def walk_strings(obj: Any, path: str = "") -> Iterator[tuple[str, str]]:
    """İç içe yapıdaki tüm metin alanlarını (yol, değer) olarak dolaşır (mojibake taraması için)."""
    if isinstance(obj, str):
        if obj.strip():
            yield path, obj
    elif isinstance(obj, dict):
        for key, val in obj.items():
            yield from walk_strings(val, f"{path}/{key}" if path else str(key))
    elif isinstance(obj, list):
        for i, val in enumerate(obj):
            yield from walk_strings(val, f"{path}/{i}")


def _mojibake_fields(rec: dict, ignore: tuple[str, ...] = ("question_id", "id", "source_id", "chunk_id")) -> list[str]:
    bad: list[str] = []
    for path, text in walk_strings(rec):
        top = path.split("/", 1)[0]
        if top in ignore:
            continue
        if textnorm.has_broken_turkish(text):
            bad.append(path)
    return bad


def inspect_question(rec: dict, *, do_schema: bool = True) -> AuditResult:
    rid = str(rec.get("question_id") or rec.get("id") or "")
    res = AuditResult("question", rid)

    if do_schema:
        for err in schema.validate(rec, "question"):
            res.blocking.append(f"schema:{err}")

    stem = (rec.get("stem") or "").strip()
    if not stem:
        res.blocking.append("stem_empty")
    elif len(stem) < STEM_MIN:
        res.blocking.append("stem_short")
    elif quality is not None and not quality.is_question_stem(stem):
        # Başlık/şık/ders içeriği/birleşik blok: gerçek soru kökü değil.
        res.blocking.append("not_a_question")

    options = rec.get("options") or {}
    if not isinstance(options, dict):
        res.blocking.append("options_not_object")
        options = {}
    acik = bool(rec.get("acik_uclu"))
    valid_keys = [k for k in _VALID_OPTION_KEYS if k in options]
    if len(valid_keys) < 4:
        if acik:
            # Açık uçlu sorular bilerek şıksızdır: engelleyici değil, bilgilendirici.
            res.review.append("acik_uclu")
        else:
            res.blocking.append("options_lt4")
    elif len(valid_keys) > 5:
        res.blocking.append("options_gt5")
    for key, val in options.items():
        if not (val or "").strip():
            res.blocking.append(f"option_empty:{key}")

    if stem and options and _EMBEDDED_OPT.search(stem) and len(valid_keys) <= 2:
        res.review.append("options_embedded_in_stem")

    answer = rec.get("answer")
    issues_text = " ".join(rec.get("issues") or []).lower()
    if answer is None:
        res.review.append("answer_null")
    elif isinstance(answer, str) and answer.strip().lower() in _UNKNOWN_ANSWER:
        res.review.append("answer_unknown")
    elif options and answer not in options:
        res.blocking.append("answer_mismatch")

    if issues_text and any(tok in issues_text for tok in _UNKNOWN_ANSWER):
        res.review.append("answer_unknown")

    if not rec.get("ders"):
        res.review.append("ders_missing")
    if not rec.get("evidence"):
        res.review.append("no_evidence")

    for path in _mojibake_fields(rec):
        res.blocking.append(f"mojibake:{path}")

    status = rec.get("status")
    if status in ("verified", "fixed") and res.blocking:
        res.review.append("status_inconsistent")
    return res


def inspect_chunk(rec: dict, *, do_schema: bool = True) -> AuditResult:
    rid = str(rec.get("chunk_id") or "")
    res = AuditResult("chunk", rid)
    if do_schema:
        for err in schema.validate(rec, "chunk"):
            res.blocking.append(f"schema:{err}")
    text = (rec.get("text") or "").strip()
    if not text:
        res.blocking.append("text_empty")
    try:
        if int(rec.get("page") or 0) < 1:
            res.blocking.append("page_invalid")
    except (TypeError, ValueError):
        res.blocking.append("page_invalid")
    for path in _mojibake_fields(rec):
        res.blocking.append(f"mojibake:{path}")
    return res


def inspect_source(rec: dict, *, do_schema: bool = True) -> AuditResult:
    rid = str(rec.get("source_id") or "")
    res = AuditResult("source", rid)
    if do_schema:
        for err in schema.validate(rec, "source"):
            res.blocking.append(f"schema:{err}")
    if not (rec.get("name") or "").strip():
        res.blocking.append("name_empty")
    if not (rec.get("md5") or "").strip():
        res.review.append("md5_missing")
    for path in _mojibake_fields(rec):
        res.blocking.append(f"mojibake:{path}")
    return res


_INSPECTORS = {
    "question": inspect_question,
    "chunk": inspect_chunk,
    "source": inspect_source,
}


def inspect(rec: dict, kind: str, *, do_schema: bool = True) -> AuditResult:
    try:
        fn = _INSPECTORS[kind]
    except KeyError as exc:
        raise ValueError(f"bilinmeyen kayıt türü: {kind!r}") from exc
    return fn(rec, do_schema=do_schema)
