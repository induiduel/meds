#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/bulletize_all_decks.py
Converts all slides across all 17 interactive learning decks into structured,
hierarchical markdown with clear bullet points, spot callouts, and curriculum synthesis.
"""

import json
import os
import re
import sys
import shutil

sys.stdout.reconfigure(encoding='utf-8')

DECKS_PATH = os.path.join('src', 'data', 'interactive_learning_decks.json')
BACKUP_PATH = os.path.join('src', 'data', 'interactive_learning_decks.backup.json')

def clean_bullet_text(text: str) -> str:
    t = text.strip()
    # Remove leading bullet characters
    t = re.sub(r'^[•\-\*]\s*', '', t)
    return t.strip()

def format_slide_synthesis(slide: dict, deck: dict) -> str:
    existing = slide.get('synthesisNarrative', '').strip()
    # If the slide already has rich hierarchical formatting with multiple bullet points (like deck 16), keep it
    if existing.count('\n• ') >= 2 and '### ' in existing:
        return existing

    title = slide.get('title', '').strip()
    subtitle = slide.get('subtitle', '').strip() or 'Müfredat ve Klinik Patofizyoloji Analizi'
    core = slide.get('coreContent', {}) or {}
    key_bullets = core.get('keyBullets', []) or []
    spot_pearls = slide.get('spotPearls', []) or []
    discipline = deck.get('discipline', 'Tıp')
    
    # Clean discipline name for section header
    disc_clean = discipline.split('/')[0].strip() if '/' in discipline else discipline.strip()

    lines = []
    lines.append(f'### {title}')
    lines.append(f'#### {subtitle}')
    lines.append('')

    # 1. Lead definition or core concept
    if existing and not any(junk in existing for junk in [
        'öğretim üyemiz dalgalı',
        'öğretim üyemiz değişiklikler',
        'öğretim üyemiz konuşacağız',
        'öğretim üyemiz'
    ]):
        sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', existing) if s.strip()]
        if sents:
            lines.append(sents[0])
            lines.append('')

    # 2. Spot pearls callout card
    if spot_pearls:
        lines.append('💡 **Klinik ve Sınav Odaklı Spot İpuçları:**')
        for p in spot_pearls:
            p_clean = clean_bullet_text(p)
            if p_clean:
                lines.append(f'• {p_clean}')
        lines.append('')

    # 3. Detailed curriculum points with distinct bullet points
    lines.append(f'#### Detaylı Müfredat Maddeleri ve {disc_clean} Sentezi')
    if key_bullets:
        for b in key_bullets:
            bt = clean_bullet_text(b.get('title', ''))
            bd = clean_bullet_text(b.get('desc', ''))
            if bt and bd:
                lines.append(f'• **{bt}:** {bd}')
            elif bd:
                lines.append(f'• {bd}')
    else:
        # Fallback if key_bullets is empty: split existing narrative into bullets
        if existing:
            sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+|;\s+(?=\*\*)', existing) if s.strip()]
            for s in sents[1:]:  # skip first sentence used as intro
                s_clean = clean_bullet_text(s)
                m = re.match(r'^\*\*([^*]+)\*\*[:,-]?\s*(.*)$', s_clean)
                if m:
                    lines.append(f'• **{m.group(1).strip()}:** {m.group(2).strip()}')
                else:
                    lines.append(f'• {s_clean}')

    return '\n'.join(lines).strip()

def main():
    if not os.path.exists(DECKS_PATH):
        print(f"Error: {DECKS_PATH} not found.")
        sys.exit(1)

    # Backup original file
    if not os.path.exists(BACKUP_PATH):
        shutil.copy2(DECKS_PATH, BACKUP_PATH)
        print(f"Backup created at: {BACKUP_PATH}")

    with open(DECKS_PATH, 'r', encoding='utf-8') as f:
        decks = json.load(f)

    total_decks = len(decks)
    total_slides = 0
    updated_slides = 0

    # Fix deck 3 spot pearls (which were mistakenly FMF pearls in early prototype)
    if len(decks) > 3 and decks[3].get('id') == 'learn-odem-hiperemi-konjesyon':
        d3 = decks[3]
        if len(d3.get('slides', [])) >= 2:
            d3['slides'][0]['spotPearls'] = [
                'Ödem patogenezinde Starling kuvvetlerini bozan 4 ana faktör: Hidrostatik basınç artışı, onkotik basınç düşüşü, lenfatik obstrüksiyon ve vasküler permeabilite artışıdır.',
                'Kalp yetmezliğinde venöz göllenme ile hidrostatik basınç artarken; nefrotik sendrom ve sirozda hipoalbüminemi sonucu onkotik basınç düşer.',
                'İnflamatuvar ödem eksüda (yüksek protein/dansite) vasfındayken, hemodinamik dengesizlik ödemi transüda (düşük protein) vasfındadır.'
            ]
            d3['slides'][1]['spotPearls'] = [
                'Sol kalp yetmezliğinde pulmoner konjesyona bağlı alveollere sızan eritrositleri yutan makrofajlar "Kalp Yetmezliği Hücreleri" (Hemosiderofajlar) adını alır.',
                'Sağ kalp yetmezliğinde karaciğer santral venlerinde göllenme ve santrilobüler nekroz "Muskat Cevizi Karaciğer" (Nutmeg liver) tablosuna yol açar.',
                'Aktif hiperemi arteriyoler vazodilatasyonla (sıcak, kırmızı), pasif konjesyon ise venöz dönüş bozukluğuyla (soğuk, siyanotik) karakterizedir.'
            ]

    for d in decks:
        slides = d.get('slides', [])
        for s in slides:
            total_slides += 1
            original = s.get('synthesisNarrative', '')
            formatted = format_slide_synthesis(s, d)
            if formatted != original:
                s['synthesisNarrative'] = formatted
                updated_slides += 1

    with open(DECKS_PATH, 'w', encoding='utf-8') as f:
        json.dump(decks, f, ensure_ascii=False, indent=2)

    print(f"Successfully processed {total_decks} decks.")
    print(f"Total slides: {total_slides}, Updated with structured bullets: {updated_slides}")

    # Verification: check how many slides now have bullets
    with open(DECKS_PATH, 'r', encoding='utf-8') as f:
        reloaded = json.load(f)

    bullet_count = 0
    for d in reloaded:
        for s in d.get('slides', []):
            if '• ' in s.get('synthesisNarrative', ''):
                bullet_count += 1

    print(f"Verification: {bullet_count}/{total_slides} slides now have markdown bullet points ('• ')!")

if __name__ == '__main__':
    main()
