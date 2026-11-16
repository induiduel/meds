# Complete builder for Deck 49 using native dicts and json dumping
import json, os, sys, re

DECK_ID = 'k1p-k1-49-invaziv-serviks-kanseri-ve-endometriyozis'

def fold(s):
    return str(s or '').lower().replace('ı', 'i').replace('İ', 'i')

def leaks(hint, answer):
    h = fold(hint)
    return any((w[:5] if len(w) > 5 else w) in h for w in re.findall(r'[\wçğıöşü%.,-]+', fold(answer)) if len(w) >= 3 or re.search(r'\d', w))

print('Generator 49 JSON engine loaded.')
