import pypdf
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_dir = r'c:\Users\indui\Desktop\meds_database\ders_notlari_pdf'
out_dir = 'data/extracted_lectures'
os.makedirs(out_dir, exist_ok=True)

files = os.listdir(pdf_dir)

missing_keywords = [
    'kronik',
    'terminoloji',
    'karsino',
    'metabolizma',
    'metastaz',
    'evreleme',
    'sistemik',
    'bebek',
    'urogenital',
    'ürogenital'
]

extracted_count = 0
for fname in files:
    if not fname.lower().endswith('.pdf'):
        continue
    lower_f = fname.lower()
    if any(k in lower_f for k in missing_keywords):
        fpath = os.path.join(pdf_dir, fname)
        safe_name = fname.replace('.pdf', '').replace(')', '_').replace("'", '').replace(' ', '_').lower() + '.txt'
        out_path = os.path.join(out_dir, safe_name)
        try:
            reader = pypdf.PdfReader(fpath)
            txt = '\n'.join([p.extract_text() or '' for p in reader.pages])
            with open(out_path, 'w', encoding='utf-8') as out:
                out.write(txt)
            print(f"Extracted: {fname} -> {safe_name} ({len(reader.pages)} pages, {len(txt)} chars)")
            extracted_count += 1
        except Exception as e:
            print(f"Error on {fname}: {e}")

print(f"\nTotal extracted pending lectures: {extracted_count}")
