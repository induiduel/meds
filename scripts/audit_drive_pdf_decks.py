# -*- coding: utf-8 -*-
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

catalog = json.load(open('data/user_drive_catalog.json', encoding='utf-8'))
decks = json.load(open('src/data/interactive_learning_decks.json', encoding='utf-8'))

def norm(t):
    if not t: return ''
    t = t.lower().replace('ı','i').replace('ğ','g').replace('ü','u').replace('ş','s').replace('ö','o').replace('ç','c')
    return re.sub(r'[^a-z0-9]', '', t)

deck_map = {}
for d in decks:
    deck_map[norm(d.get('id', ''))] = d
    deck_map[norm(d.get('title', ''))] = d
    deck_map[norm(d.get('shortTitle', ''))] = d

pdfs = catalog.get('pdfs', [])
print(f"Toplam Drive PDF: {len(pdfs)}")

import difflib

# Accurate matcher
report = []
for p in pdfs:
    fn = p['name'].replace('.pdf', '')
    clean = re.sub(r'^\d+\s*[\)\.\-]\s*', '', fn).strip('\'" ')
    nfn = norm(clean)
    
    best_deck = None
    best_score = 0.0
    
    for d in decks:
        did = norm(d.get('id', ''))
        dtitle = norm(d.get('title', ''))
        dshort = norm(d.get('shortTitle', ''))
        
        # Exact / strong substring checks
        score = 0.0
        if nfn == dtitle or nfn == did or nfn == dshort:
            score = 1.0
        elif len(nfn) > 6 and (nfn in dtitle or dtitle in nfn):
            score = 0.85
        elif len(nfn) > 6 and (nfn in did or did in nfn):
            score = 0.85
        else:
            # difflib similarity
            s1 = difflib.SequenceMatcher(None, nfn, dtitle).ratio()
            s2 = difflib.SequenceMatcher(None, nfn, did).ratio()
            score = max(s1, s2)
            
        if score > best_score:
            best_score = score
            best_deck = d
            
    matched = best_deck if best_score >= 0.55 else None
    report.append({
        'name': fn,
        'clean': clean,
        'path': p['fullPath'],
        'match_id': matched.get('id') if matched else None,
        'match_title': matched.get('title') if matched else None,
        'score': best_score,
        'slides': len(matched.get('slides', [])) if matched else 0
    })

print(f"{len(report)} PDF incelendi.\n")
ready_count = 0
for i, r in enumerate(report):
    if r['match_id']:
        ready_count += 1
        status = f"HAZIR ({r['slides']} slayt)"
    else:
        status = "EKSIK"
    print(f"{i+1:2d}. [{status:15s}] {r['name']} -> {r['match_title'] or 'YOK'}")

print(f"\nÖzet: {ready_count} Hazır, {len(report) - ready_count} Eksik")
