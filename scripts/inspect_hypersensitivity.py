import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('c:/Users/indui/Desktop/meds_database/kurul_ders_notlari_txt/Kurul 1/14)Aşırı duyarlılık ve otoimmünite.txt', encoding='utf-8') as f:
    text = f.read()

pages = re.split(r'--- \[SAYFA \d+\] ---', text)
print(f'Total pages: {len(pages)}')
for i, p in enumerate(pages):
    lines = [l.strip() for l in p.strip().split('\n') if l.strip()]
    if lines:
        first_line = lines[0][:80]
        second_line = lines[1][:80] if len(lines) > 1 else ""
        print(f"P{i:02d}: {first_line} || {second_line}")
