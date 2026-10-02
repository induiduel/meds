import re
import json

with open(r'C:\Users\indui\Desktop\meds_database\meds_sorular_txt\butunleme_clean_extracted.txt', 'r', encoding='utf-8') as f:
    text = f.read()

lines = [l.strip() for l in text.split('\n') if l.strip()]

questions = []
cur_q = {'stem': [], 'opts': {}, 'discipline': 'Genel Tıp'}
current_discipline = 'Genel Tıp'

i = 0
while i < len(lines):
    line = lines[i]
    if line.startswith('2022-2023 DÖNEM 3'):
        i += 1
        continue
    
    lower = line.lower()
    if lower in ['acil tip', 'aile hekim', 'aile hekimliği', 'anestezi', 'adli tip']:
        if lower == 'acil tip': current_discipline = 'Acil Tıp'
        elif 'aile' in lower: current_discipline = 'Aile Hekimliği'
        elif lower == 'anestezi': current_discipline = 'Anesteziyoloji ve Reanimasyon'
        elif lower == 'adli tip': current_discipline = 'Adli Tıp'
        i += 1
        continue

    opt_match = re.match(r'^([A-E])\)\s*(.*)$', line)
    if opt_match:
        opt_key = opt_match.group(1).upper()
        opt_text = opt_match.group(2)
        if not opt_text and i + 1 < len(lines) and not re.match(r'^[A-E]\)', lines[i+1]):
            i += 1
            opt_text = lines[i]
        cur_q['opts'][opt_key] = opt_text
        
        if opt_key == 'E':
            stem_text = ' '.join(cur_q['stem']).strip()
            cur_q['stem'] = stem_text
            cur_q['discipline'] = current_discipline
            questions.append(cur_q)
            cur_q = {'stem': [], 'opts': {}, 'discipline': current_discipline}
        i += 1
        continue

    keys = list(cur_q['opts'].keys())
    if len(keys) > 0 and len(keys) < 5:
        cur_q['opts'][keys[-1]] += ' ' + line
    else:
        cur_q['stem'].append(line)
    i += 1

print('Total Bütünleme questions parsed:', len(questions))
with open(r'C:\Users\indui\Desktop\meds_database\meds_sorular_txt\parsed_butunleme_raw.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)
print('Saved to parsed_butunleme_raw.json')
