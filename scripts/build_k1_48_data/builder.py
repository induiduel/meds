import json, os, sys

# Helper function to generate clean standard slides
def make_slide(slide_num, title, subtitle, clinical_focus, content_text, bullets, elements):
    return {
        "slideNumber": slide_num,
        "title": title,
        "subtitle": subtitle,
        "clinicalFocus": clinical_focus,
        "content": content_text,
        "synthesisNarrative": content_text,
        "bulletPoints": bullets,
        "relatedQuestions": [],
        "interactiveElements": elements
    }

print("Builder helper loaded.")
