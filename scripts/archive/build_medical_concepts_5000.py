# -*- coding: utf-8 -*-
"""
Master 5,000 Medical Concepts Knowledge Base Generator
Gathers, synthesizes, enriches and standardizes 5,000+ medical concepts for MedSoru.
"""

import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

OUTPUT_PATH = 'src/data/medicalConcepts5000.json'

def normalize_text(text: str) -> str:
    if not text:
        return ''
    text = text.replace('İ', 'i').replace('I', 'ı').lower()
    tr_map = str.maketrans('ığüşöç', 'igusoc')
    text = text.translate(tr_map)
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def make_slug(name: str) -> str:
    norm = normalize_text(name)
    slug = re.sub(r'\s+', '_', norm)
    slug = re.sub(r'[^a-z0-9_]', '', slug)
    return slug[:70].strip('_')

STOP_WORDS = {
    'bir', 've', 'ile', 'bu', 'icin', 'olan', 'olarak', 'gibi', 'en', 'daha',
    'cok', 'kadar', 'sonra', 'once', 'hangisi', 'hangisidir', 'asagidakilerden',
    'asagidaki', 'nedir', 'verilmistir', 'gorulur', 'gorulmez', 'degildir',
    'yanlistir', 'dogrudur', 'sorusu', 'hoca', 'slaytta', 'sinavda', 'cikmis',
    'soruldu', 'geldi', 'vardi', 'hasta', 'hastada', 'yasta', 'erkek', 'kadin',
    'ben', 'bence', 'sanki', 'diye', 'kismini', 'hatirliyorum', 'soruyordu',
    'tibbi', 'hatirlanan', 'soru', 'dersi', 'kurul', 'bolum', 'anabilim', 'dali',
    'the', 'of', 'and', 'in', 'to', 'a', 'is', 'for', 'from', 'with', 'by',
    'neden', 'olur', 'hangisinde', 'hakkinda', 'asagida', 'belirtilen', 'durumda'
}

def clean_term(term: str) -> str:
    norm = normalize_text(term)
    if len(norm) < 2 or norm in STOP_WORDS:
        return ''
    return norm

CONCEPTS = {}

def add_concept(cid: str, name: str, disciplines: list, terms: list):
    if not name or len(name.strip()) < 3:
        return
    slug = make_slug(cid or name)
    if not slug or len(slug) < 3:
        return
    
    cleaned_terms = set()
    name_norm = clean_term(name)
    if name_norm:
        cleaned_terms.add(name_norm)
        for w in name_norm.split(' '):
            w_c = clean_term(w)
            if w_c and len(w_c) >= 3:
                cleaned_terms.add(w_c)
                
    for t in terms:
        t_c = clean_term(t)
        if t_c:
            cleaned_terms.add(t_c)
            parts = t_c.split(' ')
            if len(parts) > 1:
                cleaned_terms.add(t_c)
                for p in parts:
                    p_c = clean_term(p)
                    if p_c and len(p_c) >= 4:
                        cleaned_terms.add(p_c)
                        
    valid_discs = []
    for d in disciplines:
        d_clean = d.strip()
        if d_clean and d_clean not in valid_discs:
            valid_discs.append(d_clean)
    if not valid_discs:
        valid_discs = ['Genel Tıp']
        
    if slug in CONCEPTS:
        existing = CONCEPTS[slug]
        for d in valid_discs:
            if d not in existing['disciplines']:
                existing['disciplines'].append(d)
        for ct in cleaned_terms:
            if ct not in existing['terms']:
                existing['terms'].append(ct)
    else:
        CONCEPTS[slug] = {
            'id': slug,
            'name': name.strip(),
            'disciplines': valid_discs,
            'terms': list(cleaned_terms)
        }

# Ensure script directory and cwd are in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

print("1. Loading curated modules...")
try:
    from medical_data_genetics import GENETICS_CONCEPTS
    for name, discs, terms in GENETICS_CONCEPTS: add_concept(name, name, discs, terms)
    from medical_data_builder import get_pharmacology_concepts
    for name, discs, terms in get_pharmacology_concepts(): add_concept(name, name, discs, terms)
    from medical_data_micro import MICROBIOLOGY_CONCEPTS
    for name, discs, terms in MICROBIOLOGY_CONCEPTS: add_concept(name, name, discs, terms)
    from medical_data_patho import PATHOLOGY_CONCEPTS
    for name, discs, terms in PATHOLOGY_CONCEPTS: add_concept(name, name, discs, terms)
    from medical_data_clinical import CLINICAL_CONCEPTS
    for name, discs, terms in CLINICAL_CONCEPTS: add_concept(name, name, discs, terms)
    from medical_data_master_taxonomy import generate_master_taxonomy
    for name, discs, terms in generate_master_taxonomy(): add_concept(name, name, discs, terms)
    from medical_taxonomy_pharm import PHARM_LIST
    for name, discs, terms in PHARM_LIST: add_concept(name, name, discs, terms)
    from medical_master_expansion import EXPANSION_CONCEPTS
    for name, discs, terms in EXPANSION_CONCEPTS: add_concept(name, name, discs, terms)
except Exception as e:
    print("Curated import error:", e)

print(f"Count after curated modules: {len(CONCEPTS)}")

# 2. Encyclopedia
if os.path.exists('src/data/medical_encyclopedia.json'):
    with open('src/data/medical_encyclopedia.json', 'r', encoding='utf-8') as f:
        enc_data = json.load(f)
        for item in enc_data:
            term = item.get('term', '')
            latin = item.get('latinName', '')
            aliases = item.get('aliases', [])
            disc = item.get('discipline', 'Genel Tıp')
            disciplines = [d.strip() for d in re.split(r'[&,;/•]', disc) if d.strip()]
            terms_pool = [term, latin] + aliases
            text_context = (item.get('definition', '') + ' ' + 
                            item.get('morphologyOrMechanism', '') + ' ' + 
                            item.get('examSpotPearls', ''))
            med_words = re.findall(r'[a-zA-ZçğıöşüÇĞİÖŞÜ]{4,}', text_context)
            for w in med_words[:15]:
                if normalize_text(w) not in STOP_WORDS:
                    terms_pool.append(w)
            add_concept(item.get('id', term), term, disciplines, terms_pool)

print(f"Count after encyclopedia: {len(CONCEPTS)}")

# 3. Past questions topics and high-yield options
if os.path.exists('src/data/pastQuestions.json'):
    with open('src/data/pastQuestions.json', 'r', encoding='utf-8') as f:
        pqs = json.load(f)
        
    topic_map = {}
    for q in pqs:
        disc = q.get('discipline', 'Genel Tıp')
        t = q.get('topic')
        if t and len(t.strip()) >= 3:
            t_clean = t.strip()
            if t_clean not in topic_map:
                topic_map[t_clean] = {'discipline': disc, 'stems': [], 'options': []}
            stem = q.get('stem') or ''
            if len(stem) > 10: topic_map[t_clean]['stems'].append(stem)
            for o in q.get('options') or []:
                if isinstance(o, dict) and o.get('text'):
                    topic_map[t_clean]['options'].append(o['text'])
                    
        # Extract high-yield distinct medical options
        for opt in q.get('options', []):
            if isinstance(opt, dict) and opt.get('text'):
                txt = opt['text'].strip()
                if 4 < len(txt) < 45 and not re.search(r'(hepsi|hicbiri|yalniz|yalnizca|dogrudur|yanlistir|secenek|sik)', txt, re.I):
                    if re.search(r'(sendrom|hastalik|karsinom|anemi|arter|ven|sinir|kas|ligament|virus|bakteri|enfarkt|nekroz|stenoz|refl|kist|tiroid|renal|hepat|gast|kard|pulmon|pleks|fosfat|asit|protein|lipid|kolest|gluk|reseptor|faktor|tedavi|ilac|doz|inhib|agon|antag)', txt, re.I):
                        add_concept('opt_' + txt, txt, [disc], [txt, t or ''])

    for topic_name, data in topic_map.items():
        disc_list = [d.strip() for d in re.split(r'[&,;/•()]', data['discipline']) if d.strip()]
        terms = [topic_name]
        combined_text = ' '.join(data['stems'][:5] + data['options'][:10])
        words = re.findall(r'[a-zA-ZçğıöşüÇĞİÖŞÜ]{4,}', combined_text)
        word_freq = {}
        for w in words:
            wn = normalize_text(w)
            if wn and wn not in STOP_WORDS and len(wn) >= 4:
                word_freq[wn] = word_freq.get(wn, 0) + 1
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        for w, freq in sorted_words[:12]:
            terms.append(w)
        add_concept('pq_' + topic_name, topic_name, disc_list, terms)

print(f"Count after past questions & options: {len(CONCEPTS)}")

# 4. Lecture notes titles
if os.path.exists('src/data/lecture_notes.json'):
    with open('src/data/lecture_notes.json', 'r', encoding='utf-8') as f:
        notes = json.load(f)
    for n in notes:
        t = n.get('title')
        if t and len(t.strip()) > 3:
            disc = n.get('discipline') or 'Genel Tıp'
            add_concept('note_' + t, t, [disc], [t])

print(f"Count after lecture notes: {len(CONCEPTS)}")

# 5. Lecture summaries catalog
if os.path.exists('src/data/lectureSummariesCatalog.json'):
    with open('src/data/lectureSummariesCatalog.json', 'r', encoding='utf-8') as f:
        cats = json.load(f)
    for c in cats:
        t = c.get('title')
        if t and len(t.strip()) > 3:
            disc = c.get('discipline') or 'Genel Tıp'
            key_pts = c.get('keyPoints') or []
            terms = [t]
            for kp in key_pts[:5]:
                words = re.findall(r'[a-zA-ZçğıöşüÇĞİÖŞÜ]{4,}', kp)
                terms.extend(words[:3])
            add_concept('cat_' + t, t, [disc], terms)

print(f"Count after lecture summaries: {len(CONCEPTS)}")

# 6. Comprehensive Medical Expansion
from medical_master_expansion import EXPANSION_CONCEPTS
for name, discs, terms in EXPANSION_CONCEPTS:
    add_concept(name, name, discs, terms)

print(f"Final Total Concepts Count: {len(CONCEPTS)}")

# Write to JSON
concepts_list = list(CONCEPTS.values())
concepts_list.sort(key=lambda x: x['name'])

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(concepts_list, f, ensure_ascii=False, indent=2)

print(f"Successfully generated {len(concepts_list)} medical concepts into {OUTPUT_PATH}")
