# -*- coding: utf-8 -*-
import pypdf
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_dir = ((__import__('os').environ.get('MEDS_DATABASE_DIR') or __import__('os').path.expanduser('~/meds_database')) + '/ders_notlari_pdf')
out_dir = 'data/extracted_lectures'
os.makedirs(out_dir, exist_ok=True)

target_keywords = [
    'temel kavramlar',
    'epidemiyolojik',
    'tarihçesi',
    'tarihcesi',
    'epidemiyoloji, etyoloji',
    'spesifik enfeksiyon',
    'ders programı',
    'ders programi'
]

files = os.listdir(pdf_dir)
print(f"PDF dizininde {len(files)} dosya mevcut.")

for fname in files:
    if not fname.lower().endswith('.pdf'):
        continue
    lower_f = fname.lower().replace('ı','i').replace('ğ','g').replace('ü','u').replace('ş','s').replace('ö','o').replace('ç','c')
    if any(k in lower_f for k in target_keywords):
        fpath = os.path.join(pdf_dir, fname)
        safe_name = fname.replace('.pdf', '').replace(')', '_').replace("'", '').replace(' ', '_').lower() + '.txt'
        safe_name = safe_name.replace('__', '_')
        out_path = os.path.join(out_dir, safe_name)
        try:
            reader = pypdf.PdfReader(fpath)
            txt = '\n'.join([p.extract_text() or '' for p in reader.pages])
            with open(out_path, 'w', encoding='utf-8') as out:
                out.write(txt)
            print(f"✓ Çıkarıldı: {fname} -> {safe_name} ({len(reader.pages)} sayfa, {len(txt)} karakter)")
        except Exception as e:
            print(f"✗ Hata ({fname}): {e}")

print("\nMetin çıkarım işlemi tamamlandı.")
