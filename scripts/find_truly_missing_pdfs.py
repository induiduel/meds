# -*- coding: utf-8 -*-
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/missing_drive_pdfs.json', encoding='utf-8') as f:
    missing_drive = json.load(f)

print(f"Total candidates in missing_drive_pdfs.json: {len(missing_drive)}")

# Check against all files in meds_database
all_existing = set()
for root, dirs, files in os.walk(r'c:\Users\indui\Desktop\meds_database'):
    for f in files:
        all_existing.add(f.lower().strip())
        base = os.path.splitext(f)[0].lower().strip()
        all_existing.add(base)

truly_missing = []
already_there = 0
for item in missing_drive:
    name = item.get('name', '').lower().strip()
    base = os.path.splitext(name)[0].lower().strip()
    if name in all_existing or base in all_existing:
        already_there += 1
    else:
        truly_missing.append(item)

print(f"Already in meds_database (any folder): {already_there}")
print(f"Truly missing from meds_database: {len(truly_missing)}")

for i, tm in enumerate(truly_missing[:30]):
    print(f"{i+1}. {tm.get('name')} -> {tm.get('fullPath')}")

with open('data/truly_missing_drive_pdfs.json', 'w', encoding='utf-8') as f:
    json.dump(truly_missing, f, ensure_ascii=False, indent=2)
