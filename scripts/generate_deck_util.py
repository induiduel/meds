import sys, os, json, re

# Utility to create high-quality, zero-leakage, middle-density slides and flashcards
def make_slide(
    slide_num,
    title,
    subtitle,
    clinical_focus,
    lead_paragraph,
    bullet_tuples,  # [("Başlık", "Açıklama"), ...]
    alert_type,     # "NOTE" or "IMPORTANT"
    alert_text,
    bullet_summaries, # 3 short strings
    interactive_items # list of interactive dicts
):
    body_lines = [lead_paragraph, ""]
    for header, desc in bullet_tuples:
        body_lines.append(f"- **{header}:** {desc}")
    body_lines.append("")
    body_lines.append(f"> [!{alert_type}]")
    body_lines.append(f"> {alert_text}")
    
    narrative = "\n".join(body_lines)
    
    return {
        "slideNumber": slide_num,
        "title": title,
        "subtitle": subtitle,
        "clinicalFocus": clinical_focus,
        "content": narrative,
        "synthesisNarrative": narrative,
        "bulletPoints": bullet_summaries,
        "relatedQuestions": [],
        "interactiveElements": interactive_items
    }

print("make_slide utility defined.")
