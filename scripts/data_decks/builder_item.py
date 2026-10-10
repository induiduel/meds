def mi(title, subtitle, lead, bullets, alert, summaries,
       cloze, table, chain, recall, spot, quiz, focus=None):
    it = {
        "title": title,
        "subtitle": subtitle,
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
    if focus:
        it["focus"] = focus
    return it
