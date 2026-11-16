import json, re, sys
from pathlib import Path

TASLAK = Path("meds_database_25_26/taslak/y25-k2-64-omurga-tumorleri")
kaynak_txt = (TASLAK / "kaynak.md").read_text(encoding="utf-8")

pages_lines = {}
for p in re.split(r'=== SAYFA (\d+) ===', kaynak_txt)[1:]:
    if p.isdigit():
        curr_p = int(p)
    else:
        ll = []
        for line in p.strip().splitlines():
            cl = line.strip(' ✓\t').strip()
            cl = re.sub(r'^[✓\s\-*•o❑➢]+', '', cl).strip()
            if len(cl) > 3 and not cl.isdigit() and not cl.startswith('==='):
                ll.append(cl)
        pages_lines[curr_p] = ll

print(f"Total parsed pages: {len(pages_lines)}")
for p in range(1, 21):
    lines = pages_lines.get(p, [])
    print(f"Page {p:2d}: {len(lines)} lines -> first: {lines[0][:50] if lines else 'NONE'}")
