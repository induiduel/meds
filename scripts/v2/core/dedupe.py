"""Tekilleştirme — içerik-adresli id + yakın-kopya gruplama.

Seviyeler:
  1. Tam id eşitliği (aynı kök + aynı şıklar) → kesin tekrar.
  2. Normalize token Jaccard ≥ eşik → yakın kopya (insan/LLM incelemesine aday).
Hiçbir kayıt otomatik SİLİNMEZ; yalnızca kanonik seçilir ve gruplar raporlanır.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from . import ids


def _tokens(q: dict) -> set[str]:
    parts = [q.get("stem") or ""]
    options = q.get("options") or {}
    if isinstance(options, dict):
        parts.extend(str(v) for v in options.values())
    text = " ".join(parts)
    return {t for t in ids.norm_key(text).split() if len(t) > 2}


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


@dataclass
class DuplicateGroup:
    canonical_id: str
    ids: list[str] = field(default_factory=list)
    reason: str = "exact"


@dataclass
class DedupeResult:
    unique: list[dict]
    groups: list[DuplicateGroup]

    @property
    def duplicate_count(self) -> int:
        return sum(len(g.ids) - 1 for g in self.groups)


def deduplicate(records: Iterable[dict], near_threshold: float = 0.9, store_id: bool = True) -> DedupeResult:
    """Kayıtları tekilleştirir. `store_id=True` iken her kayda 'question_id' yazılır."""
    items = list(records)
    unique: list[dict] = []
    groups: list[DuplicateGroup] = []
    by_id: dict[str, dict] = {}
    near: list[tuple[set[str], str]] = []

    for rec in items:
        qid = rec.get("question_id") or ids.question_id(rec.get("stem") or "", rec.get("options") or {})
        if store_id:
            rec["question_id"] = qid
        if qid in by_id:
            g = next((g for g in groups if g.canonical_id == qid and g.reason == "exact"), None)
            if g is None:
                g = DuplicateGroup(canonical_id=qid, ids=[qid], reason="exact")
                groups.append(g)
            g.ids.append(qid)
            continue

        toks = _tokens(rec)
        dup_of = None
        for other_toks, other_id in near:
            if jaccard(toks, other_toks) >= near_threshold:
                dup_of = other_id
                break
        if dup_of is not None:
            g = next((g for g in groups if g.canonical_id == dup_of and g.reason == "near"), None)
            if g is None:
                g = DuplicateGroup(canonical_id=dup_of, ids=[dup_of], reason="near")
                groups.append(g)
            g.ids.append(qid)
            continue

        by_id[qid] = rec
        near.append((toks, qid))
        unique.append(rec)

    return DedupeResult(unique=unique, groups=groups)
