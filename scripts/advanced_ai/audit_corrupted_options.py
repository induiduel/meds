import json
import re

with open("meds/src/data/pastQuestions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

corrupted_options = []
for q in questions:
    if not q or q.get("status") == "quarantined":
        continue
    qid = q.get("id")
    opts = q.get("options") or []
    if isinstance(opts, list):
        opt_map = {o.get("key"): str(o.get("text") or "") for o in opts}
    elif isinstance(opts, dict):
        opt_map = {k: str(v or "") for k, v in opts.items()}
    else:
        continue

    corrupt_reasons = []
    for k, text in opt_map.items():
        t = text.strip()
        # 1. OCR typos ($ without math, "ç"n, hang"s", oto$mmun)
        if "$" in t and not re.search(r"\$[A-Za-z0-9\^\{\}\+\-_/]+\$", t):
            corrupt_reasons.append(f"{k}: unescaped OCR dollar")
        if re.search(r'["\']ç["\']n|hang["\']s["\']|oto\$mmun|tans\$yon', t, re.IGNORECASE):
            corrupt_reasons.append(f"{k}: OCR typo")
        if re.search(r'(?:^\s*\(?[A-E]\)[\s.-]+|\s+\(?[A-E]\)[\s.-]+)', t) and not t.startswith("A)") and not t.startswith("B)") and not t.startswith("C)") and not t.startswith("D)") and not t.startswith("E)"):
            corrupt_reasons.append(f"{k}: option label inside text")
        # 2. Merged question inside option: contains "?" or question stem phrases
        if "?" in t:
            corrupt_reasons.append(f"{k}: question mark in option")
        if re.search(r'(hangisi\s+(?:yanlıştır|doğrudur|değildir|olamaz|yer\s+almaz|kullanılmaz)|ne\s+için\s+kullanılır|aşağıdakilerden\s+hangisi)', t, re.IGNORECASE):
            corrupt_reasons.append(f"{k}: merged question stem")
        # 3. Invalid placeholder options like "ŞIK A", "Seçenek B", empty, "-"
        if re.fullmatch(r'(?:şık\s*[A-E]|seçenek\s*[A-E]|option\s*[A-E]|-|\.)', t, re.IGNORECASE):
            corrupt_reasons.append(f"{k}: placeholder option")

    if corrupt_reasons:
        corrupted_options.append({
            "id": qid,
            "stem": (q.get("stem") or "")[:100],
            "discipline": q.get("discipline"),
            "topic": q.get("topic"),
            "correctAnswer": q.get("correctAnswer"),
            "reasons": corrupt_reasons,
            "options": opt_map
        })

print(f"Total truly corrupted questions found: {len(corrupted_options)}")
for c in corrupted_options:
    print(f"ID: {c['id']} | Discipline: {c['discipline']} | Reasons: {c['reasons']}")
    print(f"Stem: {c['stem']}")
    for k, v in c["options"].items():
        print(f"   {k}: {v}")
    print("-" * 50)

# Save to scratch file for inspection
with open("meds_database_v2/phase14_backup/corrupted_options_audit.json", "w", encoding="utf-8") as f:
    json.dump(corrupted_options, f, ensure_ascii=False, indent=2)
