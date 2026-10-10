import json, os, sys

# Helper functions to build slides cleanly
def make_slide(slide_num, title, subtitle, clinical_focus, narrative, bullets, elements):
    # Sanity checks
    assert len(narrative.split()) >= 60, f"Slide {slide_num} narrative too short: {len(narrative.split())} words"
    assert 4 <= len(elements) <= 6, f"Slide {slide_num} has {len(elements)} elements (must be 4-6)"
    for el in elements:
        assert el['type'] != 'feature_bidding', f"Slide {slide_num} has forbidden feature_bidding"
    return {
        "slideNumber": slide_num,
        "title": title,
        "subtitle": subtitle,
        "clinicalFocus": clinical_focus,
        "content": narrative,
        "synthesisNarrative": narrative,
        "bulletPoints": bullets,
        "relatedQuestions": [],
        "interactiveElements": elements
    }

print("Generator framework loaded.")
