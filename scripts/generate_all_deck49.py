import json, os, sys, re

# Deck 49: TIP 310 - İnvaziv Serviks Kanseri ve Endometriyozis
# 100 slides, 30 flashcards, 16 learning outcomes

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
                    e["hint"] = "Klinik anahtar kavram"
            elif etype == "interactive_table":
                for r in e.get("tableRows", []):
                    cells = r.get("cells") if isinstance(r, dict) else r
                    for c in cells or []:
                        if isinstance(c, dict) and c.get("isMasked") and c.get("hint") and leaks(c["hint"], c.get("text", "")):
                            c["hint"] = "Ayırıcı tanı kriteri"
    return deck

print("Helper functions ready.")
