"""Değerlendirme: 1000 soruda semantik anlama başarısı.

Metrik (şeffaf): Bir soru için anlamsal arama, sorunun gerçekten geldiği ders notu parçasını
(kaynağını) bulabiliyor mu?  - top-1 kaynak isabeti ve top-5 kaynak isabeti ölçülür; ayrıca top-1
parçanın soruyu destekleme oranı (token örtüşmesi) raporlanır. Hedef: top-5 ≥ %80.
"""
from __future__ import annotations

import json
import random

from . import config, nlp, pipeline


def _load_questions(limit: int, seed: int) -> list[dict]:
    rows = []
    if config.CORE_QUESTIONS.exists():
        for p in config.CORE_QUESTIONS.glob("*.jsonl"):
            with open(p, "r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        r = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if r.get("stem") and r.get("evidence"):
                        rows.append(r)
    random.Random(seed).shuffle(rows)
    return rows[:limit]


def _support(chunk_text: str, question: str) -> float:
    q = set(nlp.tokens(question))
    if not q:
        return 0.0
    ev = set(nlp.tokens(chunk_text))
    return len(q & ev) / len(q)


def _load_sources() -> dict[str, dict]:
    out = {}
    if config.CORE_SOURCES.exists():
        for p in config.CORE_SOURCES.glob("*.json"):
            try:
                s = json.loads(p.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001
                continue
            if s.get("source_id"):
                out[s["source_id"]] = s
    return out


def evaluate(n: int = 1000, seed: int = 42, topk: int = 5) -> dict:
    eng = pipeline.Engine()
    sources = _load_sources()
    try:
        groups = json.loads((config.OUT / "source_groups.json").read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        groups = {}
    questions = _load_questions(n, seed)
    total = len(questions)
    top1 = topk_hit = support_ok = ders_ok = 0
    for q in questions:
        opts = q.get("options") or {}
        qtext = " ".join([q.get("stem") or "", *(str(v) for v in opts.values())])
        ev = (q.get("evidence") or [""])[0]
        ev_src = ev.split(":")[0]
        true_ders = (sources.get(ev_src) or {}).get("ders")
        ev_group = groups.get(ev_src, ev_src)
        hits = eng.retrieve(qtext, k=topk)
        srcs = [h.get("source_id") for h in hits]
        sup = _support(hits[0].get("text") or "", qtext) if hits else 0.0
        s1 = bool(hits) and hits[0].get("source_id") == ev_src
        grp = bool(hits) and groups.get(hits[0].get("source_id"), hits[0].get("source_id")) == ev_group
        dok = bool(true_ders) and bool(hits) and hits[0].get("ders") == true_ders
        if s1:
            top1 += 1
        if ev_src in srcs:
            topk_hit += 1
        if sup >= 0.35:
            support_ok += 1
        if dok:
            ders_ok += 1

    report = {
        "soru": total,
        "top1_kaynak_isabeti": round(top1 / total, 4) if total else 0.0,
        "top5_kaynak_isabeti": round(topk_hit / total, 4) if total else 0.0,
        "top1_destek_orani": round(support_ok / total, 4) if total else 0.0,
        "top1_ders_uyumu": round(ders_ok / total, 4) if total else 0.0,
        "hedef": 0.90,
    }
    config.REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    return report


if __name__ == "__main__":
    print(json.dumps(evaluate(), ensure_ascii=False))
