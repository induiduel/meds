import json, os, sys, re

# Deck 49: İnvaziv Serviks Kanseri ve Endometriyozis (Servisit, Endoservikal Polip, HPV/CIN, İnvaziv Serviks Kanseri)
DECK_ID = "k1p-k1-49-invaziv-serviks-kanseri-ve-endometriyozis"

def leaks(hint, answer):
    def fold(s):
        return str(s or '').lower().replace('ı', 'i').replace('İ', 'i')
    h = fold(hint)
    return any((w[:5] if len(w) > 5 else w) in h for w in re.findall(r'[\wçğıöşü%.,-]+', fold(answer)) if len(w) >= 3 or re.search(r'\d', w))

def sanitize_deck(deck):
    for s in deck.get("slides", []):
        for e in s.get("interactiveElements", []):
            etype = e.get("type")
            if etype == "cloze_masking":
                if e.get("hint") and leaks(e["hint"], e.get("maskedTerm", "")):
                    e["hint"] = "Klinik ve patolojik anahtar terim"
            elif etype == "interactive_table":
                for r in e.get("tableRows", []):
                    cells = r.get("cells") if isinstance(r, dict) else r
                    for c in cells or []:
                        if isinstance(c, dict) and c.get("isMasked") and c.get("hint") and leaks(c["hint"], c.get("text", "")):
                            c["hint"] = "Ayırıcı tanı kriteri"
    return deck

print("Loaded gen_deck_49 generator template")
