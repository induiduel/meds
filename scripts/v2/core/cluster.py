"""Toplu soru tamamlama motoru — deterministik, AI/GPU YOK.

Öğrenciler bir kurulda hatırladıkları soru parçalarını ayrı ayrı girer. Bu modül, aynı soruya ait
parçaları **benzerlik + tıbbi varlık örtüşmesi + yapı** ile kümeleyip tek tam soruya birleştirir.
Hiçbir model yüklemez; saf string/token algoritmaları kullanır:

  - token Jaccard (içerik örtüşmesi)
  - karakter shingle Jaccard (yazım/yakınlık toleransı)
  - tıbbi varlık (terim) örtüşmesi (müfredat sözlüğünden)
  - yapı işaretleri: soru tipi (negatif/pozitif), şık kümesi

Bloklama ile O(n²) önlenir (ilk anlamlı token grubu).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from . import ids

__all__ = ["similarity", "cluster_and_merge", "ClusterResult"]

# Ağırlıklar (toplam 1.0)
W_TOKEN = 0.55
W_SHINGLE = 0.30
W_ENTITY = 0.15
DEFAULT_THRESHOLD = 0.55
SHINGLE_N = 4


def _tokens(text: str) -> set[str]:
    return {t for t in ids.norm_key(text).split() if len(t) > 2}


def _shingles(text: str, n: int = SHINGLE_N) -> set[str]:
    s = ids.norm_key(text).replace(" ", "")
    return {s[i:i + n] for i in range(max(0, len(s) - n + 1))}


def _jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _entities(rec: dict) -> set[str]:
    ents = set(rec.get("terimler") or [])
    ents |= {t for t in _tokens(rec.get("stem") or "") if len(t) >= 5}
    return ents


def similarity(a: dict, b: dict) -> float:
    """İki soru parçası arasındaki 0..1 benzerlik."""
    ta, tb = _tokens(a.get("stem") or ""), _tokens(b.get("stem") or "")
    sa, sb = _shingles(a.get("stem") or ""), _shingles(b.get("stem") or "")
    ea, eb = _entities(a), _entities(b)
    score = W_TOKEN * _jaccard(ta, tb) + W_SHINGLE * _jaccard(sa, sb) + W_ENTITY * _jaccard(ea, eb)
    # Aynı şık metinleri varsa ek kanıt
    oa = {ids.norm_key(str(v)) for v in (a.get("options") or {}).values()}
    ob = {ids.norm_key(str(v)) for v in (b.get("options") or {}).values()}
    if oa and ob and _jaccard(oa, ob) >= 0.5:
        score = min(1.0, score + 0.1)
    return round(score, 4)


@dataclass
class ClusterResult:
    groups: list[list[dict]] = field(default_factory=list)
    merged: list[dict] = field(default_factory=list)


def _block_key(rec: dict) -> str:
    toks = sorted(_tokens(rec.get("stem") or "")) or [str(rec.get("question_id") or "?")]
    return toks[0][:4]


def _merge_group(group: list[dict]) -> dict:
    """Bir gruptaki parçaları tek tam soruya birleştirir (kök en uzun, şıklar birleşik)."""
    group = sorted(group, key=lambda r: (-len(r.get("stem") or ""), -len(r.get("options") or {})))
    canon = dict(group[0])
    options: dict[str, str] = {}
    for rec in group:
        for k, v in (rec.get("options") or {}).items():
            if v and (k not in options or len(str(v)) > len(str(options[k]))):
                options[k] = v
    if options:
        canon["options"] = options
    # cevap: parçalardan çoğunluk
    answers = [r.get("answer") for r in group if r.get("answer")]
    if answers:
        canon["answer"] = max(set(answers), key=answers.count)
    # görülme kayıtları + kanıt birleşik
    seen = []
    for rec in group:
        for s in (rec.get("seen_in") or []):
            if s not in seen:
                seen.append(s)
    if seen:
        canon["seen_in"] = seen
    evidence = []
    for rec in group:
        for e in (rec.get("evidence") or []):
            if e not in evidence:
                evidence.append(e)
    if evidence:
        canon["evidence"] = evidence
    canon["birlesik_parca_sayisi"] = len(group)
    canon["birlesik_kaynak_idler"] = sorted({str(r.get("question_id")) for r in group})
    canon["acik_uclu"] = len(options) < 4 if options else bool(group[0].get("acik_uclu"))
    return canon


def cluster_and_merge(records: list[dict], *, threshold: float = DEFAULT_THRESHOLD) -> ClusterResult:
    """Kayıtları bloklayıp kümelere ayırır ve her kümeyi birleştirir. O(n·blok)."""
    blocks: dict[str, list[dict]] = {}
    for rec in records:
        blocks.setdefault(_block_key(rec), []).append(rec)

    groups: list[list[dict]] = []
    for recs in blocks.values():
        parent = list(range(len(recs)))

        def find(i: int) -> int:
            while parent[i] != i:
                parent[i] = parent[parent[i]]
                i = parent[i]
            return i

        for i in range(len(recs)):
            for j in range(i + 1, len(recs)):
                if similarity(recs[i], recs[j]) >= threshold:
                    ri, rj = find(i), find(j)
                    if ri != rj:
                        parent[rj] = ri
        buckets: dict[int, list[dict]] = {}
        for i, rec in enumerate(recs):
            buckets.setdefault(find(i), []).append(rec)
        groups.extend(buckets.values())

    merged = [_merge_group(g) for g in groups]
    return ClusterResult(groups=[g for g in groups if len(g) > 1], merged=merged)
