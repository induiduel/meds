import sys
import pypdf
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r'C:/Users/indui/.gemini/antigravity/brain/7e11da8f-18e8-4852-9b94-365630abe361/.user_uploaded/media_1790889746559.pdf'
reader = pypdf.PdfReader(pdf_path)

curriculum = {
    'kurullar': {},
    'all_topics': [],
    'departments': set(),
    'raw_lecture_lines': []
}

current_kurul = "Kurul 1"
curriculum['kurullar'][current_kurul] = {
    'title': 'TIP 310-ÜROGENİTAL VE OBSTETRİK KURULU',
    'lectures': []
}

known_departments = [
    'Tıbbi Patoloji', 'Patoloji',
    'Tıbbi Farmakoloji', 'Farmakoloji',
    'Tıbbi Genetik', 'Genetik',
    'Enfeksiyon Hastalıkları', 'Enfeksiyon',
    'İç Hastalıkları', 'Dahiliye',
    'Kardiyoloji',
    'Göğüs Hastalıkları',
    'Üroloji',
    'Kadın Hastalıkları ve Doğum', 'Kadın Doğum',
    'Acil Tıp',
    'Ortopedi ve Travmatoloji', 'Ortopedi',
    'FTR', 'Fiziksel Tıp ve Rehabilitasyon',
    'Halk Sağlığı',
    'Nöroloji',
    'Psikiyatri',
    'Aile Hekimliği',
    'Anesteziyoloji ve Reanimasyon', 'Anestezi',
    'Çocuk Sağlığı ve Hastalıkları', 'Pediatri',
    'Kalp ve Damar Cerrahisi', 'KVC',
    'Tıbbi Biyokimya', 'Biyokimya',
    'Beyin ve Sinir Cerrahisi', 'Nöroşirürji',
    'Göz Hastalıkları', 'Kulak Burun Boğaz'
]

dept_pattern = '|'.join([re.escape(d) for d in known_departments])

for page_num in range(len(reader.pages)):
    text = reader.pages[page_num].extract_text() or ''
    
    # Check for kurul headers
    km = re.search(r'DÖNEM 3 KURUL (\d)\s*(TIP \d+-[^\n]+)?', text, re.IGNORECASE)
    if km:
        k_num = km.group(1)
        k_title = km.group(2).strip() if km.group(2) else f'Kurul {k_num}'
        current_kurul = f'Kurul {k_num}'
        if current_kurul not in curriculum['kurullar']:
            curriculum['kurullar'][current_kurul] = {
                'title': k_title,
                'lectures': []
            }

    lines = [l.strip() for l in text.split('\n') if l.strip()]
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check if current line is or starts with a department name
        matched_dept = None
        for d in sorted(known_departments, key=lambda x: -len(x)):
            if re.match(rf'^{re.escape(d)}\b', line, re.IGNORECASE):
                matched_dept = d
                break
        
        if matched_dept:
            # Check if topic is on same line or next line
            same_line_rest = line[len(matched_dept):].strip(' :-')
            topic_str = ""
            if len(same_line_rest) > 3 and not re.search(r'^(PROF|DOÇ|DR|ÖĞR)', same_line_rest, re.I):
                topic_str = same_line_rest
            elif i + 1 < len(lines):
                # Next line could be topic
                next_line = lines[i + 1]
                # If next line is not an instructor, department, or time
                if not re.match(r'^(?:0\d|1\d|2\d):', next_line) and not any(re.match(rf'^{re.escape(kd)}\b', next_line, re.I) for kd in known_departments):
                    topic_str = next_line
                    i += 1
            
            # Clean instructor titles if any attached
            cleaned_topic = re.sub(r'(?:PROF|DOÇ|DR|ÖĞR|ÜYESİ|UZM|UZ)\.?\s*.*$', '', topic_str, flags=re.IGNORECASE).strip(' :-')
            if len(cleaned_topic) >= 3 and not re.match(r'^(?:Pazartesi|Salı|Çarşamba|Perşembe|Cuma|Saatler|Bağımsız|Alan Dışı)', cleaned_topic, re.I):
                curriculum['departments'].add(matched_dept.title())
                entry = {
                    'kurul': current_kurul,
                    'department': matched_dept.title(),
                    'topic': cleaned_topic,
                    'page': page_num + 1
                }
                curriculum['kurullar'][current_kurul]['lectures'].append(entry)
                curriculum['all_topics'].append(entry)
        i += 1

curriculum['departments'] = sorted(list(curriculum['departments']))
print(f"Total extracted topics: {len(curriculum['all_topics'])}")
print(f"Unique departments found: {curriculum['departments']}")

for k_id, k_data in curriculum['kurullar'].items():
    print(f"{k_id} ({k_data['title']}): {len(k_data['lectures'])} topics")

with open('data/donem3_curriculum.json', 'w', encoding='utf-8') as f:
    json.dump(curriculum, f, ensure_ascii=False, indent=2)

print("Saved to data/donem3_curriculum.json successfully.")
