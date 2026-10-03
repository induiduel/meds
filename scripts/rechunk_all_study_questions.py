# -*- coding: utf-8 -*-
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECKS_PATH = 'src/data/interactive_learning_decks.json'
OUT_DIR = 'src/data/study_questions'
os.makedirs(OUT_DIR, exist_ok=True)

with open(DECKS_PATH, 'r', encoding='utf-8') as f:
    decks = json.load(f)

print(f"Toplam güverte sayısı: {len(decks)}")

all_questions = []
seen_ids = set()

for d in decks:
    did = d.get('id')
    dtitle = d.get('title')
    disc = d.get('discipline', 'Tıp')
    comm = d.get('committee', 'Kurul 1')
    
    for s in d.get('slides', []):
        pq = s.get('practiceQuestion')
        if not pq:
            # check relatedQuestions
            rqs = s.get('relatedQuestions', [])
            if rqs and isinstance(rqs[0], dict):
                pq = rqs[0]
                
        if pq and isinstance(pq, dict):
            qid = pq.get('id') or f"q-{did}-{s.get('slideNumber', 1)}"
            if qid in seen_ids:
                qid = f"{qid}-{len(all_questions)}"
            seen_ids.add(qid)
            
            q_record = {
                "id": qid,
                "deckId": did,
                "deckTitle": dtitle,
                "slideNumber": s.get('slideNumber'),
                "slideTitle": s.get('title'),
                "discipline": disc,
                "committee": comm,
                "question": pq.get('question'),
                "options": pq.get('options', []),
                "correctAnswer": pq.get('correctAnswer', 0),
                "explanation": pq.get('explanation', '')
            }
            all_questions.append(q_record)

print(f"Toplanan toplam özgün çalışma sorusu: {len(all_questions)}")

# Chunking with MAX 100 questions per chunk
CHUNK_SIZE = 100
chunk_files = []
chunks_meta = []

for i in range(0, len(all_questions), CHUNK_SIZE):
    chunk_index = (i // CHUNK_SIZE) + 1
    chunk_qs = all_questions[i:i + CHUNK_SIZE]
    filename = f"chunk_{chunk_index}.json"
    chunk_path = os.path.join(OUT_DIR, filename)
    
    with open(chunk_path, 'w', encoding='utf-8') as cf:
        json.dump(chunk_qs, cf, ensure_ascii=False, indent=2)
        
    covered_decks = list(dict.fromkeys(q['deckId'] for q in chunk_qs))
    covered_disciplines = list(dict.fromkeys(q['discipline'] for q in chunk_qs))
    
    chunks_meta.append({
        "chunkId": f"chunk_{chunk_index}",
        "filename": filename,
        "questionCount": len(chunk_qs),
        "decksCovered": covered_decks,
        "disciplines": covered_disciplines
    })
    chunk_files.append(filename)
    print(f"✓ {filename}: {len(chunk_qs)} soru yazıldı.")

index_meta = {
    "totalQuestions": len(all_questions),
    "totalChunks": len(chunks_meta),
    "updatedAt": "2026-10-03",
    "description": "Öğren sayfasındaki ders içeriklerinden üretilmiş özgün çalışma ve pekiştirme soruları veritabanı (çıkmış sorulardan bağımsızdır).",
    "chunks": chunks_meta
}

with open(os.path.join(OUT_DIR, 'index.json'), 'w', encoding='utf-8') as idxf:
    json.dump(index_meta, idxf, ensure_ascii=False, indent=2)

print(f"✓ index.json başarıyla güncellendi ({len(chunks_meta)} chunk, toplam {len(all_questions)} soru).")
