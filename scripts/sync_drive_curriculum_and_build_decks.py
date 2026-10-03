# -*- coding: utf-8 -*-
import json
import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

CATALOG_PATH = 'data/user_drive_catalog.json'
DECKS_PATH = 'src/data/interactive_learning_decks.json'
REGISTRY_PATH = 'data/interactive_decks_registry.json'

with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

with open(DECKS_PATH, 'r', encoding='utf-8') as f:
    decks = json.load(f)

pdfs = catalog.get('pdfs', [])

# Normalize title helper
def norm_text(t):
    if not t: return ''
    t = t.lower()
    t = t.replace('ı', 'i').replace('ğ', 'g').replace('ü', 'u').replace('ş', 's').replace('ö', 'o').replace('ç', 'c')
    t = re.sub(r'[^a-z0-9]', '', t)
    return t

# Collect existing deck normalized titles and ids
deck_map = {}
for d in decks:
    nid = norm_text(d.get('id', ''))
    ntitle = norm_text(d.get('title', ''))
    nshort = norm_text(d.get('shortTitle', ''))
    deck_map[nid] = d
    deck_map[ntitle] = d
    if nshort:
        deck_map[nshort] = d

# Compare with Drive PDFs
matched_list = []
missing_decks = []

for p in pdfs:
    fname = p.get('name', '').replace('.pdf', '')
    # Strip leading numbers like "1) ", "2) ", "'", etc.
    clean_name = re.sub(r'^\d+\s*[\)\.\-]\s*', '', fname).strip("'\" ")
    norm_fname = norm_text(clean_name)

    found_deck = None
    for k, d in deck_map.items():
        if norm_fname in k or k in norm_fname or (len(norm_fname) > 6 and norm_fname[:10] in k):
            found_deck = d
            break

    if found_deck:
        matched_list.append({
            'pdf': p,
            'cleanName': clean_name,
            'deckId': found_deck.get('id'),
            'deckTitle': found_deck.get('title'),
            'slideCount': len(found_deck.get('slides', []))
        })
    else:
        missing_decks.append({
            'pdf': p,
            'cleanName': clean_name,
            'normName': norm_fname,
            'fullPath': p.get('fullPath')
        })

print('=' * 70)
print(f'Drive Toplam PDF Sayısı: {len(pdfs)}')
print(f'Eşleşen (Zaten Güvertesi Hazır) PDF Sayısı: {len(matched_list)}')
print(f'Eksik (İnteraktif Notu Hazırlanacak) PDF Sayısı: {len(missing_decks)}')
print('=' * 70)

# Save registry of all Drive PDFs with status
registry = {
    'updatedAt': catalog.get('updatedAt'),
    'totalDrivePdfs': len(pdfs),
    'readyCount': len(matched_list),
    'pendingCount': len(missing_decks),
    'readyDecks': matched_list,
    'pendingPdfs': missing_decks
}

with open(REGISTRY_PATH, 'w', encoding='utf-8') as f:
    json.dump(registry, f, ensure_ascii=False, indent=2)

print(f'\nKayıtlar {REGISTRY_PATH} dosyasına kaydedildi.')

print('\n--- EKSİK VE İŞLENECEK PDFLER LİSTESİ ---')
for i, m in enumerate(missing_decks):
    print(f"{i+1:2d}. [{m['pdf']['id']}] {m['cleanName']} ({m['pdf']['fullPath']})")
