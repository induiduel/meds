# -*- coding: utf-8 -*-
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/drive_crawler_results.json', encoding='utf-8') as f:
    drive_items = json.load(f)

print(f"Total drive crawler items: {len(drive_items)}")

pdf_items = [item for item in drive_items if not item.get('isFolder') and item.get('name', '').lower().endswith('.pdf')]
print(f"Total PDF items in Drive crawler: {len(pdf_items)}")

local_dirs = [
    r'c:\Users\indui\Desktop\meds_database\ders_notlari_pdf',
    r'c:\Users\indui\Desktop\meds_database\kurul_ders_notlari',
    r'c:\Users\indui\Desktop\Dönem 3 Notlar',
    r'c:\Users\indui\Desktop\meds_database\cikmis_sorular_pdf'
]

local_files = set()
for ldir in local_dirs:
    if os.path.exists(ldir):
        for root, dirs, files in os.walk(ldir):
            for file in files:
                local_files.add(file.lower().strip())

missing_pdfs = []
for p in pdf_items:
    pname = p.get('name', '').lower().strip()
    if pname not in local_files:
        missing_pdfs.append(p)

print(f"Missing PDFs count: {len(missing_pdfs)}")
for i, m in enumerate(missing_pdfs[:40]):
    print(f"{i+1}. {m.get('name')} | Path: {m.get('fullPath')} | ID: {m.get('id')}")

# Save missing list to json
with open('data/missing_drive_pdfs.json', 'w', encoding='utf-8') as f:
    json.dump(missing_pdfs, f, ensure_ascii=False, indent=2)

print("Saved missing PDFs to data/missing_drive_pdfs.json")
