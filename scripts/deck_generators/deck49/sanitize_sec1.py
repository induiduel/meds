import re
from meds.scripts.validate_learning_decks import leaks
import meds.scripts.deck_generators.deck49.sec1 as s1

def sanitize_elements(slides):
    for s in slides:
        for el in s.get('interactiveElements', []):
            if el['type'] == 'cloze_masking':
                if el.get('hint') and leaks(el['hint'], el.get('maskedTerm', '')):
                    el['hint'] = ''
            elif el['type'] == 'interactive_table':
                for r in el.get('tableRows', []):
                    for c in r.get('cells', []):
                        if c.get('isMasked') and c.get('hint'):
                            if leaks(c['hint'], c.get('text', '')):
                                c['hint'] = ''
    return slides

if __name__ == '__main__':
    slides = sanitize_elements(s1.get_sec1())
    print("Sec1 sanitized.")
