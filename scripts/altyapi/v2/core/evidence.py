"""Kanıt (evidence) ve provenance yardımcıları.

Kural: yayına girecek her soru en az bir kanıt (chunk_id) taşımalı ve türetilmiş metinler
kanıt metniyle `support_ratio` ile ölçülmelidir. Alıntısız (desteklenmeyen) türetilmiş içerik
`needs_review` sayılır. Bu, hallucination'a karşı temel kapıdır.
"""
from __future__ import annotations

from typing import Iterable

from . import ids

__all__ = ["tokens", "support_ratio", "make_source_ref", "attach_provenance", "has_evidence"]

_MIN_TOKEN = 3


def tokens(text: str) -> list[str]:
    return [t for t in ids.norm_key(text).split() if len(t) >= _MIN_TOKEN]


def support_ratio(text: str, evidence_texts: Iterable[str]) -> float:
    """`text` token'larının ne kadarı kanıt metinlerinde geçiyor (0..1). Kısa metinde 1.0 döner."""
    toks = set(tokens(text))
    if not toks:
        return 1.0
    ev: set[str] = set()
    for e in evidence_texts:
        ev.update(tokens(e))
    if not ev:
        return 0.0
    return round(len(toks & ev) / len(toks), 4)


def make_source_ref(chunk_id: str, *, quote: str | None = None) -> dict:
    """Kaynak referansı (siteye gösterilebilir) üretir: [Kaynak: chunk_id]."""
    ref = {"chunk_id": chunk_id}
    if quote:
        ref["alinti"] = quote.strip()[:500]
    return ref


def attach_provenance(rec: dict, *, kaynak_dosya: str, md5: str | None = None,
                      sayfa: int | None = None, kanal: str | None = None) -> dict:
    """Kaydın nereden geldiğini izlenebilir kılar (provenance)."""
    prov = rec.setdefault("provenance", {})
    prov["kaynak_dosya"] = kaynak_dosya
    if md5:
        prov["md5"] = md5
    if sayfa is not None:
        prov["sayfa"] = sayfa
    if kanal:
        prov["kanal"] = kanal
    return rec


def has_evidence(rec: dict) -> bool:
    ev = rec.get("evidence") or []
    if isinstance(ev, (list, tuple)):
        return any(str(x).strip() for x in ev)
    return bool(ev)
