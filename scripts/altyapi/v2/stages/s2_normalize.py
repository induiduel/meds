"""s2 — Normalize: ham metni temizle, sorulara/parçalara böl, kimlik ata.

Deterministik: `core.textnorm` + `core.segment`. Bulut AI kullanılmaz.
"""
from __future__ import annotations

from .. import config
from ..core import ids, quality, segment, textnorm

CHUNK_TARGET = 900
CHUNK_OVERLAP = 120


def _looks_like_question(q: dict, strict: bool) -> bool:
    """`strict=True` (slayt/özet): yalnızca gerçek sorular — ≥3 şık veya açık cevap.
    `strict=False` (çıkmış soru dosyası): optionsuz/açık uçlu sorular da kabul edilir."""
    if len(q.get("options") or {}) >= 3:
        return True
    if q.get("answer"):
        return True
    return not strict


def build_questions(doc: dict, *, ders: str | None = None, konu: str | None = None) -> list[dict]:
    """Bir belgenin sayfalarından soru kayıtları üretir (status='raw', doğrulama s3'te)."""
    source = doc["source"]
    pages = doc["pages"]
    ders = ders or source.get("ders")
    konu = konu or source.get("konu")
    # Slayt/özet dosyalarında numaralı listeler soru değildir: yalnız gerçek soruları al.
    strict = source.get("doc_type") != "past_question"
    out: list[dict] = []
    for page in pages:
        for q in segment.parse_questions(page["text"]):
            # Gerçek soru kökü değilse (başlık/şık/ders içeriği/birleşik blok) KABUL ETME.
            if not q["stem"] or not quality.is_question_stem(q["stem"]) or not _looks_like_question(q, strict):
                continue
            rec = {
                "question_id": ids.question_id(q["stem"], q["options"]),
                "no": q.get("no"),
                "source_id": source["source_id"],
                "donem": source.get("donem", 3),
                "kurul": source.get("kurul"),
                "ders": ders,
                "konu": konu,
                "stem": q["stem"],
                "options": q["options"],
                "acik_uclu": len(q["options"]) < 4,
                "answer": q["answer"],
                "explanation": q["explanation"],
                "status": "raw",
                "issues": [],
                "evidence": [],
                "pipeline_generation": config.PIPELINE_GENERATION,
                "tags": [q["soru_tipi"]] if q.get("soru_tipi") == "negatif" else [],
                "provenance": {"kaynak_dosya": source["path"], "md5": source["md5"], "sayfa": page["page"], "kanal": "rule"},
            }
            out.append(rec)
    return out


def _split_page(text: str, target: int = CHUNK_TARGET, overlap: int = CHUNK_OVERLAP) -> list[str]:
    text = textnorm.normalize_ws(text)
    if len(text) <= target:
        return [text] if text else []
    paras = [p for p in text.split("\n") if p.strip()]
    chunks: list[str] = []
    cur = ""
    for para in paras:
        if cur and len(cur) + len(para) + 1 > target:
            chunks.append(cur.strip())
            cur = (cur[-overlap:] + " " + para) if overlap else para
        else:
            cur = f"{cur} {para}".strip()
    if cur.strip():
        chunks.append(cur.strip())
    return chunks


def build_chunks(doc: dict, *, ders: str | None = None, konu: str | None = None) -> list[dict]:
    """Bir belgenin sayfalarından ~900 karakterlik parçalar (chunk) üretir."""
    source = doc["source"]
    ders = ders or source.get("ders")
    konu = konu or source.get("konu")
    out: list[dict] = []
    for page in doc["pages"]:
        for n, text in enumerate(_split_page(page["text"])):
            out.append({
                "chunk_id": ids.chunk_id(source["source_id"], page["page"], n),
                "source_id": source["source_id"],
                "page": page["page"],
                "heading_path": [source.get("ders") or "", source["name"]],
                "text": text,
                "doc_type": source["doc_type"],
                "donem": source.get("donem", 3),
                "kurul": source.get("kurul"),
                "ders": ders,
                "konu": konu,
                "hash": ids.content_hash(text),
            })
    return out
