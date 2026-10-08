"""s4 — Tekilleştirme: içerik-adresli id + yakın-kopya gruplama."""

from __future__ import annotations

from ..core import dedupe


def dedupe_records(records: list[dict], near_threshold: float = 0.9) -> dedupe.DedupeResult:
    return dedupe.deduplicate(records, near_threshold=near_threshold)
