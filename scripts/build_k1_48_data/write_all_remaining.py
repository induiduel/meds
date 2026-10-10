import json, os, sys

def make_element_cloze(sentence, masked_term, hint):
    return {
        "type": "cloze_masking",
        "sentence": sentence,
        "maskedTerm": masked_term,
        "hint": hint
    }

def make_element_table(title, headers, rows):
    return {
        "type": "interactive_table",
        "tableTitle": title,
        "tableHeaders": headers,
        "tableRows": rows
    }

def make_element_chain(title, steps):
    return {
        "type": "causal_chain",
        "chainTitle": title,
        "steps": steps
    }

def make_element_recall(question, answer):
    return {
        "type": "active_recall",
        "question": question,
        "answer": answer
    }

def make_element_spot_lie(topic, items):
    return {
        "type": "spot_the_lie",
        "topic": topic,
        "items": items
    }

def make_element_quiz(question, options):
    return {
        "type": "micro_quiz",
        "question": question,
        "microQuizOptions": options
    }

print("Helper elements defined.")
