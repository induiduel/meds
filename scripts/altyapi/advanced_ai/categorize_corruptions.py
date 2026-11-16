import json
import re

with open("meds/src/data/pastQuestions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

severe_issues = []
for q in questions:
    if not q:
        continue
    qid = q.get("id")
    opts = q.get("options") or []
    if isinstance(opts, list):
        opt_map = {o.get("key"): str(o.get("text") or "").strip() for o in opts}
    elif isinstance(opts, dict):
        opt_map = {k: str(v or "").strip() for k, v in opts.items()}
    else:
        continue

    issues = []
    # Check 1: Merged question stem or branch inside options
    for k, t in opt_map.items():
        if "?" in t:
            issues.append(f"{k} has ?")
        if re.search(r"(hangisi\s+(?:yanlıştır|doğrudur|değildir|olamaz|yer\s+almaz|kullanılmaz)|ne\s+için\s+kullanılır|aşağıdakilerden\s+hangisi)", t, re.IGNORECASE):
            issues.append(f"{k} has question stem")
        if re.search(r"\b[A-E]\)\s+", t):
            issues.append(f"{k} has embedded option label")
        if len(t) > 250:
            issues.append(f"{k} extremely long ({len(t)} chars)")
        if t in ("Bebek beslenmesi", "Beyin ve sinir cerrahisi", "Dahiliye", "Genel Cerrahi", "Tıbbi Patoloji", "FTR"):
            issues.append(f"{k} is a branch/topic name")
        if re.fullmatch(r"(?:şık\s*[A-E]|seçenek\s*[A-E]|option\s*[A-E]|-|\.)", t, re.IGNORECASE):
            issues.append(f"{k} is placeholder")

    # Check duplicate options (e.g. C: 1 3 and E: 1 3)
    vals = [v for v in opt_map.values() if v]
    if len(vals) > len(set(vals)):
        issues.append("duplicate options")

    if issues:
        severe_issues.append({
            "id": qid,
            "issues": issues,
            "stem": (q.get("stem") or "")[:100],
            "options": opt_map,
            "correctAnswer": q.get("correctAnswer")
        })

print(f"Total severe issue questions: {len(severe_issues)}")
cat_counts = {}
for s in severe_issues:
    for iss in s["issues"]:
        cat_counts[iss] = cat_counts.get(iss, 0) + 1

print("\nIssue breakdown:")
for k, v in sorted(cat_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  {k}: {v}")

with open("meds_database_v2/phase14_backup/severe_issues.json", "w", encoding="utf-8") as f:
    json.dump(severe_issues, f, ensure_ascii=False, indent=2)
print("Saved to meds_database_v2/phase14_backup/severe_issues.json")
