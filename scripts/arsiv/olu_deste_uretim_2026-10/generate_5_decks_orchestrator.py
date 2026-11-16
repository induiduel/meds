import json, os, sys, re

def fold(s):
    return str(s or '').lower().replace('ı', 'i').replace('İ', 'i')

def leaks(hint, answer):
    h = fold(hint)
    return any((w[:5] if len(w) > 5 else w) in h for w in re.findall(r'[\wçğıöşü%.,-]+', fold(answer)) if len(w) >= 3 or re.search(r'\d', w))

def check_slide(s):
    items = s.get("interactiveElements", [])
    if len(items) < 4 or len(items) > 6:
        raise ValueError(f"Slide {s.get('slideNumber')} has {len(items)} items; expected 4-6.")
    for e in items:
        t = e.get("type")
        if t == "feature_bidding":
            raise ValueError(f"Slide {s.get('slideNumber')} has forbidden feature_bidding!")
        if t == "cloze_masking":
            sen = e.get("sentence", "")
            term = e.get("maskedTerm", "")
            hint = e.get("hint", "")
            if not term or fold(term) not in fold(sen):
                raise ValueError(f"Slide {s.get('slideNumber')} cloze term {term!r} not in sentence {sen!r}")
            if hint and leaks(hint, term):
                raise ValueError(f"Slide {s.get('slideNumber')} cloze hint leak: {hint!r} -> {term!r}")
        elif t == "interactive_table":
            headers = e.get("tableHeaders", [])
            for row in e.get("tableRows", []):
                cells = row.get("cells", [])
                if len(cells) != len(headers):
                    raise ValueError(f"Slide {s.get('slideNumber')} table row length mismatch")
                for c in cells:
                    if c.get("isMasked") and c.get("hint") and leaks(c.get("hint"), c.get("text")):
                        raise ValueError(f"Slide {s.get('slideNumber')} table hint leak: {c.get('hint')!r} -> {c.get('text')!r}")
        elif t == "spot_the_lie":
            topic = e.get("topic", "")
            if not topic:
                raise ValueError(f"Slide {s.get('slideNumber')} spot_the_lie missing topic")
            its = e.get("items", [])
            lies = [i for i in its if i.get("isLie")]
            if len(lies) != 1:
                raise ValueError(f"Slide {s.get('slideNumber')} spot_the_lie must have exactly 1 lie")
            for it in its:
                if not it.get("explanation"):
                    raise ValueError(f"Slide {s.get('slideNumber')} spot_the_lie item missing explanation")
        elif t == "micro_quiz":
            opts = e.get("microQuizOptions", [])
            corr = [o for o in opts if o.get("isCorrect")]
            if len(corr) != 1:
                raise ValueError(f"Slide {s.get('slideNumber')} micro_quiz must have exactly 1 correct option")
            for o in opts:
                if not o.get("explanation"):
                    raise ValueError(f"Slide {s.get('slideNumber')} micro_quiz option missing explanation")

print("Validation engine ready.")
