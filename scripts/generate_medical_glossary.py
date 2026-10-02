#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/generate_medical_glossary.py
Medical glossary generator and synchronizer for Dönem 3 Kurul 1.
Ensures medical_glossary.json remains valid, properly formatted, and sorted.
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

GLOSSARY_PATH = os.path.join('src', 'data', 'medical_glossary.json')

def main():
    if not os.path.exists(GLOSSARY_PATH):
        print(f"Error: {GLOSSARY_PATH} not found!")
        return

    with open(GLOSSARY_PATH, 'r', encoding='utf-8') as f:
        terms = json.load(f)

    # Sort alphabetically by term name
    terms.sort(key=lambda x: x.get('term', '').lower())

    with open(GLOSSARY_PATH, 'w', encoding='utf-8') as f:
        json.dump(terms, f, ensure_ascii=False, indent=2)

    print(f"Verified and formatted {len(terms)} terms in {GLOSSARY_PATH}.")

if __name__ == '__main__':
    main()
