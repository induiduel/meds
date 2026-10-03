import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = 'c:/Users/indui/Desktop/meds_database/kurul_ders_notlari_txt/Kurul 1/15)Genetik,pediatrik ve çevresel patoloji.txt'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

pages = re.split(r'--- \[SAYFA \d+\] ---', text)
print(f'Total pages in 15)Genetik,pediatrik ve çevresel patoloji.txt: {len(pages)}')

for i, p in enumerate(pages):
    lines = [l.strip() for l in p.strip().split('\n') if l.strip()]
    if lines:
        first_line = lines[0][:80]
        second_line = lines[1][:80] if len(lines) > 1 else ""
        print(f"P{i:02d}: {first_line} || {second_line}")
