import sys, os, json, re

# Quick slide structure helper to reduce boilerplate in data files
def make_subtopic(
    title, subtitle, focus, lead, bullets, alert, summaries,
    cloze, table, chain, recall, spot, quiz
):
    return {
        "title": title,
        "subtitle": subtitle,
        "focus": focus,
        "lead": lead,
        "bullets": bullets,
        "alert": alert,
        "summaries": summaries,
        "cloze": cloze,
        "table": table,
        "chain": chain,
        "recall": recall,
        "spot": spot,
        "quiz": quiz
    }

print("builder_helpers loaded.")
