#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/integrate_deepseek_jsonl.py
-----------------------------------
Entegrates DeepSeek-verified Dönem 3 questions (meds_donem3_sorulari_duzeltilmis.jsonl)
directly into:
  1. src/data/pastQuestions.json
  2. data/pastQuestions.json
  3. data/deepseek_contributions.json
  4. data/local_rag_chunks.json (RAG indexing)
  5. meds_database/database_json/donem3k* (committee databases)
"""

import os
import sys
import json
import hashlib
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = (__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))))
MEDS_DB_DIR = ((__import__('os').environ.get('MEDS_DATABASE_DIR') or __import__('os').path.expanduser('~/meds_database')))
JSONL_FILE = os.path.join(MEDS_DB_DIR, "deepseek_data", "meds_donem3_sorulari_duzeltilmis.jsonl")
SRC_QUESTIONS_FILE = os.path.join(ROOT_DIR, "src", "data", "pastQuestions.json")
DATA_QUESTIONS_FILE = os.path.join(ROOT_DIR, "data", "pastQuestions.json")
DEEPSEEK_CONTRIB_FILE = os.path.join(ROOT_DIR, "data", "deepseek_contributions.json")
LOCAL_RAG_FILE = os.path.join(ROOT_DIR, "data", "local_rag_chunks.json")
DATABASE_JSON_DIR = os.path.join(MEDS_DB_DIR, "database_json")

def hash_text(text: str) -> str:
    return hashlib.md5(text.strip().encode('utf-8')).hexdigest()

def run_integration():
    print("=" * 80)
    print("🚀 [DeepSeek JSONL] Entegrasyon Motoru Başlatılıyor...")
    print("=" * 80)

    if not os.path.exists(JSONL_FILE):
        print(f"❌ HATA: JSONL dosyası bulunamadı: {JSONL_FILE}")
        return False

    # 1. JSONL dosyasını yükle
    print(f"📂 Okunuyor: {JSONL_FILE}")
    jsonl_items = []
    with open(JSONL_FILE, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
                jsonl_items.append(item)
            except Exception as e:
                print(f"⚠️ Satır {idx} ayrıştırma hatası: {e}")

    print(f"✓ Toplam {len(jsonl_items)} adet DeepSeek doğrulanmış soru okundu.")

    # 2. pastQuestions.json dosyalarını oku
    for target_path in [SRC_QUESTIONS_FILE, DATA_QUESTIONS_FILE]:
        if not os.path.exists(target_path):
            continue

        with open(target_path, 'r', encoding='utf-8') as f:
            existing_questions = json.load(f)

        q_dict = {q['id']: q for q in existing_questions if 'id' in q}
        updated_count = 0
        added_count = 0

        now_iso = datetime.now().isoformat()

        for j_item in jsonl_items:
            qid = j_item.get('id')
            if not qid:
                continue

            if qid in q_dict:
                # Güncelle
                target = q_dict[qid]
                target['stem'] = j_item.get('stem', target.get('stem'))
                target['options'] = j_item.get('options', target.get('options'))
                target['correctAnswer'] = j_item.get('correctAnswer', target.get('correctAnswer'))
                target['claimedAnswer'] = j_item.get('correctAnswer', target.get('claimedAnswer'))
                target['explanation'] = j_item.get('explanation', target.get('explanation'))
                target['evidenceText'] = j_item.get('evidenceText', target.get('evidenceText'))
                target['lectureMatches'] = j_item.get('lectureMatches', target.get('lectureMatches'))
                target['verification'] = j_item.get('verification', target.get('verification'))
                target['embeddingText'] = j_item.get('embeddingText', target.get('embeddingText'))
                target['discipline'] = j_item.get('discipline', target.get('discipline'))
                target['topic'] = j_item.get('topic', target.get('topic'))
                target['donem'] = "Dönem 3"
                target['status'] = "onaylandi"
                target['updatedAt'] = now_iso
                
                # Reconstruction nesnesini de zenginleştir
                if not isinstance(target.get('reconstruction'), dict):
                    target['reconstruction'] = {}
                target['reconstruction']['stem'] = target['stem']
                target['reconstruction']['options'] = target['options']
                target['reconstruction']['correctAnswer'] = target['correctAnswer']
                target['reconstruction']['explanation'] = target['explanation']
                target['reconstruction']['evidenceText'] = target['evidenceText']
                target['reconstruction']['isAiRefined'] = True
                target['reconstruction']['reconstructionQuality'] = 'deepseek_verified'
                
                updated_count += 1
            else:
                # Yeni soru olarak ekle
                new_q = {
                    'id': qid,
                    'committeeId': j_item.get('committeeId', 'donem3-kurul1'),
                    'donem': "Dönem 3",
                    'kurul': j_item.get('kurul', 1),
                    'questionNumber': j_item.get('questionNumber', 0),
                    'discipline': j_item.get('discipline', 'Tıp Bilimleri'),
                    'topic': j_item.get('topic', 'Klinik Tıp'),
                    'stem': j_item.get('stem', ''),
                    'options': j_item.get('options', []),
                    'correctAnswer': j_item.get('correctAnswer', 'A'),
                    'claimedAnswer': j_item.get('correctAnswer', 'A'),
                    'explanation': j_item.get('explanation', ''),
                    'evidenceText': j_item.get('evidenceText', ''),
                    'lectureMatches': j_item.get('lectureMatches', []),
                    'verification': j_item.get('verification', {}),
                    'embeddingText': j_item.get('embeddingText', ''),
                    'examYear': j_item.get('examYear', 'Dönem 3 Çıkmış'),
                    'sourceFile': 'deepseek_data/meds_donem3_sorulari_duzeltilmis.jsonl',
                    'status': 'onaylandi',
                    'isPastExam': True,
                    'tags': ['deepseek_verified', 'donem3'],
                    'reconstruction': {
                        'stem': j_item.get('stem', ''),
                        'options': j_item.get('options', []),
                        'correctAnswer': j_item.get('correctAnswer', 'A'),
                        'explanation': j_item.get('explanation', ''),
                        'evidenceText': j_item.get('evidenceText', ''),
                        'isAiRefined': True,
                        'reconstructionQuality': 'deepseek_verified'
                    },
                    'createdAt': now_iso,
                    'updatedAt': now_iso
                }
                existing_questions.append(new_q)
                q_dict[qid] = new_q
                added_count += 1

        with open(target_path, 'w', encoding='utf-8') as f:
            json.dump(existing_questions, f, ensure_ascii=False, indent=2)

        print(f"✓ {target_path} güncellendi: {updated_count} soru zenginleştirildi, {added_count} yeni soru eklendi (Toplam: {len(existing_questions)}).")

    # 3. deepseek_contributions.json Güncellemesi
    deepseek_contributions = []
    now_iso = datetime.now().isoformat()
    for item in jsonl_items:
        stem = item.get('stem', '')
        opts = item.get('options', [])
        opt_lines = "\n".join([f"{o.get('key')}) {o.get('text')}" for o in opts if isinstance(o, dict)])
        correct = item.get('correctAnswer', '')
        expl = item.get('explanation', '')
        ev = item.get('evidenceText', '')
        disc = item.get('discipline', 'Tıp Bilimleri')
        comm = item.get('committeeId', 'donem3-kurul1')
        top = item.get('topic', 'Tıp')

        content = f"""[DEEPSEEK DOĞRULANMIŞ TIP SORUSU]
Ders / Branş: {disc}
Kurul: {comm}
Konu: {top}
Soru Kökü:
{stem}

Seçenekler:
{opt_lines}

Doğru Cevap: {correct}
{f'DeepSeek Tıbbi Analizi & Çözümü:\n{expl}' if expl else ''}
{f'Ders Notu Kanıtı:\n{ev}' if ev else ''}""".strip()

        h = hash_text(content)
        deepseek_contributions.append({
            'id': item.get('id', f"deepseek-d3-{h[:8]}"),
            'source': 'deepseek',
            'contributor': 'DeepSeek AI',
            'isContribution': True,
            'attributionBadge': 'DeepSeek Doğrulanmış Soru',
            'itemType': 'question',
            'committeeId': comm,
            'discipline': disc,
            'topic': top,
            'title': top or (stem[:60] + '...'),
            'content': content,
            'rawPayload': item,
            'metadata': {
                'sourceFile': 'meds_donem3_sorulari_duzeltilmis.jsonl',
                'fileFormat': 'jsonl',
                'importedAt': now_iso,
                'stem': stem,
                'options': opts,
                'correctAnswer': correct,
                'explanation': expl,
                'evidenceText': ev,
                'verification': item.get('verification'),
                'lectureMatches': item.get('lectureMatches'),
                'tags': ['deepseek', 'donem3', 'dogrulanmis_soru', disc]
            },
            'hash': h,
            'createdAt': now_iso,
            'updatedAt': now_iso
        })

    with open(DEEPSEEK_CONTRIB_FILE, 'w', encoding='utf-8') as f:
        json.dump(deepseek_contributions, f, ensure_ascii=False, indent=2)
    print(f"✓ {DEEPSEEK_CONTRIB_FILE} kaydedildi ({len(deepseek_contributions)} DeepSeek katkısı hazır).")

    # 4. local_rag_chunks.json İndeksleme ve Senkronizasyon
    if os.path.exists(LOCAL_RAG_FILE):
        with open(LOCAL_RAG_FILE, 'r', encoding='utf-8') as f:
            existing_chunks = json.load(f)

        # Mevcut chunklardan deepseek veya past_question olanları güncelle
        chunk_map = {c.get('documentId', c.get('id')): c for c in existing_chunks}
        updated_rag_count = 0
        added_rag_count = 0

        for contrib in deepseek_contributions:
            doc_id = contrib['id']
            rag_content = contrib['content']
            h = contrib['hash']

            chunk_obj = {
                'id': f"chunk-ds-{doc_id}",
                'documentId': doc_id,
                'documentType': 'deepseek_contribution',
                'committeeId': contrib.get('committeeId'),
                'discipline': contrib.get('discipline'),
                'title': f"Dönem 3 Doğrulanmış Soru: {contrib.get('discipline')} - {contrib.get('topic')}",
                'pageNumber': contrib.get('rawPayload', {}).get('questionNumber', 1),
                'content': rag_content,
                'metadata': {
                    'donem': 'Dönem 3',
                    'committeeId': contrib.get('committeeId'),
                    'discipline': contrib.get('discipline'),
                    'topic': contrib.get('topic'),
                    'correctAnswer': contrib['metadata'].get('correctAnswer'),
                    'verification': contrib['metadata'].get('verification'),
                    'sourceFile': 'meds_donem3_sorulari_duzeltilmis.jsonl'
                },
                'hash': h,
                'createdAt': now_iso,
                'updatedAt': now_iso
            }

            if doc_id in chunk_map:
                existing_entry = chunk_map[doc_id]
                existing_entry['content'] = rag_content
                existing_entry['metadata'].update(chunk_obj['metadata'])
                existing_entry['hash'] = h
                existing_entry['updatedAt'] = now_iso
                updated_rag_count += 1
            else:
                existing_chunks.append(chunk_obj)
                chunk_map[doc_id] = chunk_obj
                added_rag_count += 1

        with open(LOCAL_RAG_FILE, 'w', encoding='utf-8') as f:
            json.dump(existing_chunks, f, ensure_ascii=False, indent=2)

        print(f"✓ {LOCAL_RAG_FILE} güncellendi: {updated_rag_count} chunk yenilendi, {added_rag_count} yeni RAG chunk eklendi (Toplam: {len(existing_chunks)} chunk).")

    # 5. meds_database/database_json Güncellemesi
    if os.path.exists(DATABASE_JSON_DIR):
        db_updated = 0
        for root, _, files in os.walk(DATABASE_JSON_DIR):
            for fname in files:
                if fname.endswith('.json') and not fname.startswith('manifest') and not fname.startswith('index'):
                    fpath = os.path.join(root, fname)
                    try:
                        with open(fpath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        modified = False
                        if isinstance(data, list):
                            for item in data:
                                qid = item.get('id')
                                if qid and qid in q_dict:
                                    # Update verification & explanation
                                    match = q_dict[qid]
                                    item['correctAnswer'] = match['correctAnswer']
                                    item['explanation'] = match['explanation']
                                    item['evidenceText'] = match.get('evidenceText')
                                    item['verification'] = match.get('verification')
                                    modified = True
                        if modified:
                            with open(fpath, 'w', encoding='utf-8') as f:
                                json.dump(data, f, ensure_ascii=False, indent=2)
                            db_updated += 1
                    except Exception:
                        pass
        print(f"✓ meds_database/database_json içinde {db_updated} dosya güncellendi.")

    print("\n" + "=" * 80)
    print("🎉 DEEPSEEK JSONL VERİLERİ SİSTEME VE RAG KATMANINA BAŞARIYLA ENTEGRE EDİLDİ!")
    print("=" * 80)
    return True

if __name__ == '__main__':
    run_integration()
