# -*- coding: utf-8 -*-
import pypdf
import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

catalog = json.load(open('data/user_drive_catalog.json', encoding='utf-8'))
pdf_dir = ((__import__('os').environ.get('MEDS_DATABASE_DIR') or __import__('os').path.expanduser('~/meds_database')) + '/ders_notlari_pdf')

print(f"{'No':2s} | {'Sayfa':5s} | {'Karakter':8s} | {'Drive Dosya Adı'}")
print("-" * 80)

for i, p in enumerate(catalog.get('pdfs', [])):
    fname = p['name']
    fpath = os.path.join(pdf_dir, fname)
    if not os.path.exists(fpath):
        # try matching
        matches = [f for f in os.listdir(pdf_dir) if f.replace("'", "").lower() == fname.replace("'", "").lower()]
        if matches:
            fpath = os.path.join(pdf_dir, matches[0])
            
    if os.path.exists(fpath):
        try:
            reader = pypdf.PdfReader(fpath)
            num_pages = len(reader.pages)
            char_count = sum(len(pg.extract_text() or '') for pg in reader.pages)
            print(f"{i+1:2d} | {num_pages:5d} | {char_count:8d} | {fname}")
        except Exception as e:
            print(f"{i+1:2d} | HATA  | {str(e)[:8]} | {fname}")
    else:
        print(f"{i+1:2d} | YOK   |          | {fname}")
