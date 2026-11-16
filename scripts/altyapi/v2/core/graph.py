"""Kavram grafı — deterministik veri zenginleştirme (AI/GPU YOK).

Sorulardan ve müfredattan düğüm/kenar grafı üretir: ders, konu, kazanım ve tıbbi terimler.
Kenarlar birlikte geçme (co-occurrence) sayısına göre ağırlıklıdır. Site ve analiz araçları bu
grafiği gezinme/ilişki kurma için kullanabilir. NetworkX gerekmez; saf dict ile üretilir.
"""
from __future__ import annotations

from collections import Counter

__all__ = ["build", "summary"]


def _node_id(kind: str, name: str) -> str:
    return f"{kind}:{name}"


def build(records: list[dict], *, min_edge: int = 2) -> dict:
    """Soru listesinden düğüm/kenar grafı üretir."""
    nodes: dict[str, dict] = {}
    edge_counts: Counter = Counter()

    def add_node(kind: str, name: str) -> str | None:
        name = (name or "").strip()
        if not name:
            return None
        nid = _node_id(kind, name)
        nodes[nid] = {"id": nid, "tur": kind, "ad": name}
        return nid

    for rec in records:
        ids_here = []
        for kind, val in (("ders", rec.get("ders")), ("konu", rec.get("konu")), ("kazanim", rec.get("kazanim"))):
            nid = add_node(kind, val) if val else None
            if nid:
                ids_here.append(nid)
        for term in (rec.get("terimler") or [])[:12]:
            nid = add_node("terim", term)
            if nid:
                ids_here.append(nid)
        ids_here = sorted(set(ids_here))
        for i in range(len(ids_here)):
            for j in range(i + 1, len(ids_here)):
                edge_counts[(ids_here[i], ids_here[j])] += 1

    edges = [
        {"kaynak": a, "hedef": b, "agirlik": w}
        for (a, b), w in edge_counts.items() if w >= min_edge
    ]
    edges.sort(key=lambda e: -e["agirlik"])
    return {"dugumler": list(nodes.values()), "kenarlar": edges}


def summary(graph: dict) -> dict:
    tur = Counter(n["tur"] for n in graph.get("dugumler", []))
    return {"dugum": len(graph.get("dugumler", [])), "kenar": len(graph.get("kenarlar", [])),
            "tur_dagilimi": dict(tur)}
