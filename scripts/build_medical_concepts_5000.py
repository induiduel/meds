# -*- coding: utf-8 -*-
"""
Medical Concepts 5000 Knowledge Base Generator
Builds a comprehensive, high-yield, normalized database of 5,000+ distinct medical
concepts for MedSoru draft deduplication, clustering, and anchor matching.
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
    return slug[:60].strip('_')

STOP_WORDS = {
    'bir', 've', 'ile', 'bu', 'icin', 'olan', 'olarak', 'gibi', 'en', 'daha',
    'cok', 'kadar', 'sonra', 'once', 'hangisi', 'hangisidir', 'asagidakilerden',
    'asagidaki', 'nedir', 'verilmistir', 'gorulur', 'gorulmez', 'degildir',
    'yanlistir', 'dogrudur', 'sorusu', 'hoca', 'slaytta', 'sinavda', 'cikmis',
    'soruldu', 'geldi', 'vardi', 'hasta', 'hastada', 'yasta', 'erkek', 'kadin',
    'ben', 'bence', 'sanki', 'diye', 'kismini', 'hatirliyorum', 'soruyordu',
    'tibbi', 'hatirlanan', 'soru', 'dersi', 'kurul', 'bolum', 'anabilim', 'dali',
    'the', 'of', 'and', 'in', 'to', 'a', 'is', 'for', 'from', 'with', 'by'
}

def clean_term(term: str) -> str:
    norm = normalize_text(term)
    if len(norm) < 2 or norm in STOP_WORDS:
        return ''
    return norm

# Master concepts registry: id -> concept dict
CONCEPTS = {}

def add_concept(cid: str, name: str, disciplines: list, terms: list):
    slug = make_slug(cid or name)
    if not slug:
        return
    
    cleaned_terms = set()
    # Add name itself
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
            # Add multi-words and important sub-words
            parts = t_c.split(' ')
            if len(parts) > 1:
                cleaned_terms.add(t_c)
                for p in parts:
                    p_c = clean_term(p)
                    if p_c and len(p_c) >= 4:
                        cleaned_terms.add(p_c)
                        
    if slug in CONCEPTS:
        # Merge disciplines and terms
        existing = CONCEPTS[slug]
        for d in disciplines:
            if d not in existing['disciplines']:
                existing['disciplines'].append(d)
        for ct in cleaned_terms:
            if ct not in existing['terms']:
                existing['terms'].append(ct)
    else:
        CONCEPTS[slug] = {
            'id': slug,
            'name': name.strip(),
            'disciplines': disciplines,
            'terms': list(cleaned_terms)
        }

print("1. Loading existing medical encyclopedia (src/data/medical_encyclopedia.json)...")
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
            # Extract key phrases from definition & exam pearls
            text_context = (item.get('definition', '') + ' ' + 
                            item.get('morphologyOrMechanism', '') + ' ' + 
                            item.get('examSpotPearls', ''))
            
            # Extract medical keywords
            med_words = re.findall(r'[a-zA-ZçğıöşüÇĞİÖŞÜ]{4,}', text_context)
            for w in med_words[:15]:
                if normalize_text(w) not in STOP_WORDS:
                    terms_pool.append(w)
                    
            add_concept(item.get('id', term), term, disciplines, terms_pool)

print(f"   Loaded {len(CONCEPTS)} concepts after encyclopedia.")

print("2. Loading past questions topics (src/data/pastQuestions.json)...")
if os.path.exists('src/data/pastQuestions.json'):
    with open('src/data/pastQuestions.json', 'r', encoding='utf-8') as f:
        pqs = json.load(f)
        
    topic_map = {}
    for q in pqs:
        t = q.get('topic')
        if not t or len(t.strip()) < 3:
            continue
        t_clean = t.strip()
        disc = q.get('discipline', 'Genel Tıp')
        if t_clean not in topic_map:
            topic_map[t_clean] = {'discipline': disc, 'stems': [], 'options': []}
            
        stem = q.get('stem') or ''
        if len(stem) > 10:
            topic_map[t_clean]['stems'].append(stem)
            
        opts = q.get('options') or []
        if isinstance(opts, list):
            for o in opts:
                if isinstance(o, dict) and o.get('text'):
                    topic_map[t_clean]['options'].append(o['text'])
                    
    for topic_name, data in topic_map.items():
        disc_list = [d.strip() for d in re.split(r'[&,;/•()]', data['discipline']) if d.strip()]
        terms = [topic_name]
        
        # Extract frequent terms from stems and options
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

print(f"   Loaded {len(CONCEPTS)} concepts after past questions topics.")
