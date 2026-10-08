"""Denetçi (M1) — mevcut tüm veriyi kayıt kayıt denetler. SALT OKUNUR.

Eski (`meds_database/`) ve site (`meds/data/`) verisini okur, her kaydı şema + kural denetiminden
geçirir ve yalnızca izole `MEDS_CORE_DIR/reports/` altına rapor + inceleme kuyruğu yazar. Mevcut
veri dosyalarına hiçbir yazma yapılmaz.

Kullanım:
    python -m v2.audit                     # tüm veri kümeleri
    python -m v2.audit --only questions    # tek küme
    python -m v2.audit --limit 500         # küme başına ilk N kayıt (hızlı deneme)
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Iterator

from . import config
from .core import store, validate

# (ad, tür, do_schema) -> kayıt üreteci
Dataset = tuple[str, str, bool]


def _iter_jsonl(paths: list[Path]) -> Iterator[dict]:
    for path in sorted(paths):
        yield from store.iter_jsonl(path)


def _iter_json_array(paths: list[Path]) -> Iterator[dict]:
    """Her dosyayı okur: dizi ise öğelerini, nesne ise kendisini üretir."""
    for path in sorted(paths):
        data = store.read_json(path, [])
        if isinstance(data, list):
            yield from (r for r in data if isinstance(r, dict))
        elif isinstance(data, dict):
            yield data


def _adapt_site_past_question(rec: dict) -> dict:
    """Site modelini (id/discipline/reconstruction) denetlenebilir düz soruya çevirir."""
    recon = rec.get("reconstruction") or {}
    options: dict[str, str] = {}
    for opt in recon.get("options") or []:
        if isinstance(opt, dict):
            key = opt.get("key") or opt.get("label")
            if key:
                options[str(key)] = opt.get("text") or opt.get("value") or ""
        elif isinstance(opt, str):
            options.setdefault("ABCDE"[len(options)], opt)
    answer = recon.get("correctAnswer") or rec.get("answer")
    return {
        "question_id": rec.get("id"),
        "donem": 3,
        "kurul": rec.get("kurul"),
        "ders": rec.get("discipline"),
        "konu": rec.get("topic"),
        "stem": rec.get("stem"),
        "options": options,
        "answer": answer,
        "status": None,
        "issues": [],
        "evidence": rec.get("evidence") or [],
    }


def discover() -> list[tuple[str, str, bool, Iterator[dict]]]:
    db = config.DATABASE_DIR
    meds_data = config.MEDS_DIR / "data"
    sets: list[tuple[str, str, bool, Iterator[dict]]] = []

    q_files = list((db / "questions").glob("*.jsonl"))
    if q_files:
        sets.append(("questions", "question", True, _iter_jsonl(q_files)))

    c_files = list((db / "chunks").glob("*.jsonl"))
    if c_files:
        sets.append(("chunks", "chunk", True, _iter_jsonl(c_files)))

    s_files = list((db / "sources").glob("*.json"))
    if s_files:
        sets.append(("sources", "source", True, _iter_json_array(s_files)))

    site_past = meds_data / "pastQuestions.json"
    if site_past.exists():
        sets.append(("site_past_questions", "question", False,
                     (_adapt_site_past_question(r) for r in _iter_json_array([site_past]))))

    return sets


def run(only: set[str] | None = None, limit: int | None = None, verbose: bool = True) -> dict:
    config.ensure_core_dirs()
    started = time.time()
    report: dict = {"zaman": store.now_iso(), "kaynaklar": {}, "toplam": {}}
    review: list[dict] = []

    totals = {"kayit": 0, "blocking": 0, "review": 0, "ok": 0}

    for name, kind, do_schema, records in discover():
        if only and name not in only:
            continue
        counts = {"kayit": 0, "blocking": 0, "review": 0, "ok": 0}
        codes: dict[str, int] = {}
        for rec in records:
            if limit is not None and counts["kayit"] >= limit:
                break
            counts["kayit"] += 1
            result = validate.inspect(rec, kind, do_schema=do_schema)
            counts[result.severity] += 1
            for code in result.issues:
                base = code.split(":", 1)[0] if code.startswith("schema:") else code
                codes[base] = codes.get(base, 0) + 1
            if result.severity != validate.SEVERITY_OK:
                stem = (rec.get("stem") or rec.get("text") or rec.get("name") or "")[:120]
                review.append({
                    "kume": name, "tur": kind, "id": result.rid,
                    "severity": result.severity,
                    "blocking": result.blocking[:12], "review": result.review[:12],
                    "ozet": stem,
                })
        report["kaynaklar"][name] = {
            "tur": kind, "kayit": counts["kayit"],
            "blocking": counts["blocking"], "review": counts["review"], "ok": counts["ok"],
            "issue_kodlari": dict(sorted(codes.items(), key=lambda kv: -kv[1])),
        }
        for k in totals:
            totals[k] += counts[k]
        if verbose:
            print(f"[{name:22}] kayıt={counts['kayit']:6}  blocking={counts['blocking']:5}  "
                  f"review={counts['review']:5}  ok={counts['ok']:6}")

    report["toplam"] = {**totals, "sure_sn": round(time.time() - started, 1)}
    report["inceleme_kuyrugu"] = len(review)

    date = time.strftime("%Y-%m-%d_%H%M")
    report_path = config.REPORTS_DIR / f"audit_{date}.json"
    queue_path = config.REPORTS_DIR / "review_queue.jsonl"
    store.write_core_json(report_path, report)
    store.write_core_jsonl(queue_path, review, guard=False)

    if verbose:
        print("-" * 66)
        print(f"TOPLAM kayıt={totals['kayit']}  blocking={totals['blocking']}  "
              f"review={totals['review']}  ok={totals['ok']}  ({report['toplam']['sure_sn']} sn)")
        print(f"rapor      : {report_path}")
        print(f"inceleme   : {queue_path}  ({len(review)} kayıt)")
    return report


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="MedSoru Core v2 denetçisi (salt okunur)")
    ap.add_argument("--only", default="", help="virgülle ayrılmış küme adları (ör. questions,chunks)")
    ap.add_argument("--limit", type=int, default=None, help="küme başına en fazla N kayıt")
    args = ap.parse_args(argv)
    only = {s.strip() for s in args.only.split(",") if s.strip()} or None
    run(only=only, limit=args.limit, verbose=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
