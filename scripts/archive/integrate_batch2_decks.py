# -*- coding: utf-8 -*-
"""
Integrate Batch 2 Rebuilt Decks into src/data/interactive_learning_decks.json
Decks:
1. learn-enflamasyon-kimyasal-mediyatorleri
2. learn-enfeksiyon-temel-kavramlar
3. learn-sistemik-hastaliklar-bobrek-hasari
4. learn-urogenital-tumorlerde-genetik
5. learn-donem3-kurul1-mufredat-rehberi
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECKS_PATH = 'src/data/interactive_learning_decks.json'
SCRATCH_DIR = (__import__('tempfile').gettempdir())

with open(DECKS_PATH, 'r', encoding='utf-8') as f:
    decks = json.load(f)

# Normalize decks
clean_decks = []
seen = set()
for d in decks:
    did = d.get('id') or d.get('deckId')
    if did:
        d['id'] = did
        if 'deckId' in d:
            del d['deckId']
        if did not in seen:
            seen.add(did)
            clean_decks.append(d)

decks = clean_decks
decks_by_id = {d['id']: d for d in decks}

batch2_files = {
    'learn-enflamasyon-kimyasal-mediyatorleri': os.path.join(SCRATCH_DIR, 'deck_kimyasal_mediyatorler.json'),
    'learn-enfeksiyon-temel-kavramlar': os.path.join(SCRATCH_DIR, 'deck_enfeksiyon_temel_kavramlar.json'),
    'learn-sistemik-hastaliklar-bobrek-hasari': os.path.join(SCRATCH_DIR, 'deck_sistemik_bobrek.json'),
    'learn-urogenital-tumorlerde-genetik': os.path.join(SCRATCH_DIR, 'deck_urogenital_genetik.json'),
    'learn-donem3-kurul1-mufredat-rehberi': os.path.join(SCRATCH_DIR, 'deck_kurul1_mufredat.json'),
}

updated_decks = []
for deck_id, filepath in batch2_files.items():
    if not os.path.exists(filepath):
        print(f"HATA: {filepath} bulunamadı!")
        continue
    with open(filepath, 'r', encoding='utf-8') as sf:
        new_data = json.load(sf)
    
    new_slides = new_data.get('slides', [])
    new_title = new_data.get('title')
    
    if deck_id in decks_by_id:
        target = decks_by_id[deck_id]
        if new_title:
            target['title'] = new_title
        target['slides'] = new_slides
        target['totalSlides'] = len(new_slides)
        updated_decks.append((deck_id, len(new_slides)))
        print(f"✓ Güncellendi: {deck_id} ({len(new_slides)} slayt)")
    else:
        new_deck_entry = {
            "id": deck_id,
            "title": new_title or deck_id,
            "discipline": "Kurul 1",
            "committee": "Kurul 1",
            "slides": new_slides,
            "totalSlides": len(new_slides)
        }
        decks.append(new_deck_entry)
        updated_decks.append((deck_id, len(new_slides)))
        print(f"✓ Yeni eklendi: {deck_id} ({len(new_slides)} slayt)")

with open(DECKS_PATH, 'w', encoding='utf-8') as f:
    json.dump(decks, f, ensure_ascii=False, indent=2)

print("\n--- BATCH 2 ENTEGRASYON RAPORU ---")
for did, scnt in updated_decks:
    print(f"• {did}: {scnt} slayt başarıyla işlendi.")
