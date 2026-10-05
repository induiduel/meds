#!/usr/bin/env python3
"""Build evidence-first curriculum/question/lecture links under meds_database.

This pass is deliberately deterministic. It never labels a weak lexical match as
confirmed; uncertain records are emitted to review_queue.jsonl for a later human
or Gemini review pass.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from datetime import datetime, timezone

TR = str.maketrans("İIĞÜŞÖÇıığüşöç", "iig usociig üsoc".replace(" ", ""))
STOP = set("ve veya ile bir bu şu için olan olanın olarak da de daha çok gibi hangi hangisi nedir mi mı mu mü ile olanlar ilgili ait göre en son olanların".split())


def fold(value: object) -> str:
    s = str(value or "").translate(TR).lower()
    return re.sub(r"[^a-z0-9çğıöşü]+", " ", s)


def tokens(value: object) -> list[str]:
    out = []
    for raw in fold(value).split():
        if len(raw) < 3 or raw in STOP or raw.isdigit():
            continue
        out.append(raw if len(raw) <= 8 else raw[:8])
    return out


def read_jsonl(path: Path):
    """Yield valid JSON lines and parse diagnostics without aborting the run."""
    with path.open(encoding="utf-8", errors="replace") as handle:
        for line_no, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                item = json.loads(line)
                if isinstance(item, dict):
                    yield item, None
                else:
                    yield None, {"line": line_no, "error": "json_object_required"}
            except Exception as exc:
                yield None, {"line": line_no, "error": type(exc).__name__}


def stable_id(prefix: str, value: str) -> str:
    return f"{prefix}_{hashlib.sha1(value.encode('utf-8')).hexdigest()[:12]}"


def committee_number(value):
    m = re.search(r"\d+", str(value or ""))
    return int(m.group()) if m else None


def score(query_tokens: list[str], target_tokens: list[str]) -> float:
    q, t = set(query_tokens), set(target_tokens)
    if not q or not t:
        return 0.0
    overlap = len(q & t)
    return (overlap / len(q)) * (overlap / len(t)) ** 0.35


def write_jsonl(path: Path, rows):
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    ap.add_argument("--database", type=Path)
    ap.add_argument("--curriculum", type=Path)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    root = args.root
    database = args.database or root / "meds_database"
    curriculum_path = args.curriculum or root / "meds" / "curriculum" / "kbu_tip_donem3_curriculum.json"
    out = args.output or database / "deepseek_meta_data"
    out.mkdir(parents=True, exist_ok=True)

    curriculum = json.loads(curriculum_path.read_text(encoding="utf-8"))
    topics = []
    for code, committee in curriculum.get("committees", {}).items():
        for idx, topic in enumerate(committee.get("core_topics", []), 1):
            topic_id = f"{code}.K{idx:03d}"
            topics.append({
                "outcome_id": topic_id,
                "committee_code": code,
                "committee_name": committee.get("name"),
                "departments": committee.get("departments", []),
                "topic": topic,
                "topic_tokens": tokens(topic),
                "evidence_basis": "curriculum.core_topics",
            })
    write_jsonl(out / "curriculum_outcomes.jsonl", topics)

    question_rows, parse_issues = [], []
    question_dir = database / "questions"
    for path in sorted(question_dir.glob("*.jsonl")):
        for item, issue in read_jsonl(path):
            if issue:
                parse_issues.append({"path": str(path), **issue})
            elif item:
                question_rows.append((path, item))

    # Topic candidates are constrained by the question's committee whenever possible.
    links, review = [], []
    for path, q in question_rows:
        stem = q.get("stem") or ""
        options = q.get("options") or {}
        query = tokens(" ".join([stem, *[str(v) for v in options.values()], str(q.get("ders")), str(q.get("konu"))]))
        kurul = committee_number(q.get("kurul"))
        code = f"TIP{300 + kurul * 10}" if q.get("donem") in (3, "3") and kurul in range(1, 7) else None
        candidates = [t for t in topics if code and t["committee_code"] == code]
        ranked = sorted(((score(query, t["topic_tokens"]), t) for t in candidates), reverse=True, key=lambda x: x[0])
        top = ranked[:3]
        best = top[0][0] if top else 0.0
        margin = best - (top[1][0] if len(top) > 1 else 0.0)
        issues = []
        if len(stem.strip()) < 15:
            issues.append("incomplete_or_too_short_stem")
        if not options or len([v for v in options.values() if str(v).strip()]) < 4:
            issues.append("malformed_options")
        if not stem.strip() and not options:
            issues.append("not_a_question")
        if not top or best < 0.12:
            issues.append("unmatched_curriculum")
        elif margin < 0.03 and len(top) > 1:
            issues.append("ambiguous_curriculum")
        elif len(top) > 1 and top[1][0] >= best * 0.82:
            issues.append("multi_topic_same_committee_review")
        confidence = "confirmed_candidate" if best >= 0.28 and margin >= 0.04 and not issues else ("review" if top else "unmatched")
        row = {
            "question_id": q.get("question_id") or stable_id("question", f"{path}:{stem}"),
            "source_file": str(path),
            "committee_code": code,
            "question_course": q.get("ders"),
            "question_topic": q.get("konu"),
            "candidate_outcomes": [{"outcome_id": t["outcome_id"], "topic": t["topic"], "score": round(s, 4), "evidence": ["stem", "options", "existing_course_topic"]} for s, t in top],
            "selected_outcome_ids": [top[0][1]["outcome_id"]] if confidence == "confirmed_candidate" else [],
            "confidence": confidence,
            "review_flags": issues,
        }
        links.append(row)
        if issues or confidence != "confirmed_candidate":
            review.append({"record_type": "question", **row})
    write_jsonl(out / "question_curriculum_links.jsonl", links)

    # Read chunks as lecture evidence and classify them against curriculum topics.
    chunks = []
    chunk_errors = []
    for path in sorted((database / "chunks").glob("*.jsonl")):
        for item, issue in read_jsonl(path):
            if issue:
                chunk_errors.append({"path": str(path), **issue})
            elif item:
                chunks.append((path, item))

    note_links, chunk_index = [], defaultdict(list)
    for path, c in chunks:
        text = " ".join([str(c.get(k) or "") for k in ("text", "raw_text", "heading_path", "ders", "konu")])
        ct = tokens(text)
        for tok in set(ct):
            chunk_index[tok].append((path, c, ct))
        kurul = committee_number(c.get("kurul"))
        code = f"TIP{300 + kurul * 10}" if c.get("donem") in (3, "3") and kurul in range(1, 7) else None
        cand = [t for t in topics if code and t["committee_code"] == code]
        ranked = sorted(((score(ct, t["topic_tokens"]), t) for t in cand), reverse=True, key=lambda x: x[0])[:3]
        best = ranked[0][0] if ranked else 0
        confidence = "confirmed_candidate" if best >= 0.24 else ("review" if best >= 0.12 else "unmatched")
        row = {"chunk_id": c.get("chunk_id"), "source_id": c.get("source_id"), "page": c.get("page"), "source_file": str(path), "committee_code": code, "course": c.get("ders"), "heading_path": c.get("heading_path"), "candidate_outcomes": [{"outcome_id": t["outcome_id"], "topic": t["topic"], "score": round(s, 4)} for s, t in ranked], "selected_outcome_ids": [ranked[0][1]["outcome_id"]] if confidence == "confirmed_candidate" else [], "confidence": confidence}
        note_links.append(row)
    write_jsonl(out / "lecture_chunk_curriculum_links.jsonl", note_links)

    # Link questions to evidence chunks through inverted lexical retrieval, same committee/course preferred.
    q_evidence = []
    chunk_by_id = {c.get("chunk_id"): c for _, c in chunks}
    for qrow in links:
        qtokens = tokens(" ".join([qrow.get("question_course") or "", qrow.get("question_topic") or "", " ".join(x["topic"] for x in qrow.get("candidate_outcomes", []))]))
        pool = Counter()
        for tok in set(qtokens):
            for _, c, ct in chunk_index.get(tok, []):
                if qrow.get("committee_code") and c.get("kurul") and committee_number(c.get("kurul")) != committee_number(qrow.get("committee_code")):
                    continue
                pool[c.get("chunk_id")] += 1
        ranked = sorted(pool.items(), key=lambda x: x[1], reverse=True)[:5]
        q_evidence.append({"question_id": qrow["question_id"], "evidence_chunks": [{"chunk_id": cid, "shared_token_count": n, "page": chunk_by_id.get(cid, {}).get("page"), "source_id": chunk_by_id.get(cid, {}).get("source_id")} for cid, n in ranked], "evidence_status": "candidate_only" if ranked else "missing"})
    write_jsonl(out / "question_lecture_evidence_links.jsonl", q_evidence)

    # Inventory all source documents without reading binary payloads.
    source_rows = []
    skip = {".git", "node_modules", ".venv-ocr", ".venv_train", "dist"}
    for path in root.rglob("*"):
        if not path.is_file() or any(part in skip for part in path.parts):
            continue
        if path.suffix.lower() in {".pdf", ".md", ".json", ".jsonl"}:
            try: size = path.stat().st_size
            except OSError: continue
            source_rows.append({"path": str(path), "format": path.suffix.lower()[1:], "bytes": size})
    write_jsonl(out / "source_manifest.jsonl", source_rows)
    write_jsonl(out / "review_queue.jsonl", review)
    write_jsonl(out / "parse_issues.jsonl", parse_issues + chunk_errors)
    summary = {"generated_at": datetime.now(timezone.utc).isoformat(), "questions_read": len(question_rows), "question_links": len(links), "question_review": len(review), "chunks_read": len(chunks), "chunk_links": len(note_links), "source_files": len(source_rows), "parse_issues": len(parse_issues) + len(chunk_errors), "method": "curriculum-constrained lexical evidence retrieval; no weak match marked confirmed"}
    (out / "run_manifest.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
