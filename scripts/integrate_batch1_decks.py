# -*- coding: utf-8 -*-
"""
Integrate Batch 1 Rebuilt Decks into src/data/interactive_learning_decks.json
Decks:
1. learn-uriner-sistem-enfeksiyonlari-epidemiyoloji
2. learn-uriner-sistemin-spesifik-enfeksiyonlari
3. learn-enfeksiyon-epidemiyoloji
4. learn-halk-sagligi-tarihcesi-ve
5. learn-bebek-beslenmesi
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECKS_PATH = 'src/data/interactive_learning_decks.json'
SCRATCH_DIR = r'C:\Users\indui\.gemini\antigravity\brain\386176b3-c821-4f99-a837-6f25ae2aca35\scratch'

with open(DECKS_PATH, 'r', encoding='utf-8') as f:
    decks = json.load(f)

# Batch 1 mappings
batch1_files = {
    'learn-uriner-sistem-enfeksiyonlari-epidemiyoloji': os.path.join(SCRATCH_DIR, 'deck_uriner_epidemiyoloji.json'),
    'learn-uriner-sistemin-spesifik-enfeksiyonlari': os.path.join(SCRATCH_DIR, 'deck_uriner_spesifik.json'),
    'learn-enfeksiyon-epidemiyoloji': os.path.join(SCRATCH_DIR, 'deck_enfeksiyon_epidemiyoloji.json'),
    'learn-halk-sagligi-tarihcesi-ve': os.path.join(SCRATCH_DIR, 'deck_halk_sagligi_tarihcesi.json'),
    'learn-bebek-beslenmesi': os.path.join(SCRATCH_DIR, 'deck_bebek_beslenmesi.json'),
}

# Clean up any malformed deck entries first
clean_decks = []
seen = set()
for d in decks:
    did = d.get('id') or d.get('deckId')
    if did:
        d['id'] = did
        if 'deckId' in d and 'id' in d:
            del d['deckId']
        if did not in seen:
            seen.add(did)
            clean_decks.append(d)

decks = clean_decks
decks_by_id = {d['id']: d for d in decks}

updated_decks = []
for deck_id, filepath in batch1_files.items():
    if not os.path.exists(filepath):
        print(f"HATA: {filepath} bulunamadı!")
        continue
    with open(filepath, 'r', encoding='utf-8') as sf:
        new_data = json.load(sf)
    
    # new_data might have 'slides' or be a deck object
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
        # If it doesn't exist, create it
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

print("\n--- BATCH 1 ENTEGRASYON RAPORU ---")
for did, scnt in updated_decks:
    print(f"• {did}: {scnt} slayt başarıyla işlendi.")
