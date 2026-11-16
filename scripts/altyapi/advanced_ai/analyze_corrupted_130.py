import json
import re

with open("meds_database_v2/phase14_backup/corrupted_group1_4.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

print(f"Total to examine: {len(questions)}")

clean_cuts = []
replacements_needed = []
debris_to_quarantine = []

for q in questions:
    qid = q["id"]
    stem = q["stem"]
    opts = q["options"]
    issues = q["issues"]
    
    # Check if options have huge concatenated text that can be cleanly sliced
    # e.g., "Ksenon I I. Aşağıdaki genel anesteziklerden hangisi..." -> slice at "I I."
    has_cut = False
    for k, v in opts.items():
        if "?" in v and len(v) > 60:
            has_cut = True
    
    # Check if question is completely unrecoverable debris (e.g. 3 different questions in 1 stem/options)
    if "Bebek beslenmesi" in str(opts) and "gebe kadının" in str(opts):
        debris_to_quarantine.append((qid, "Çoklu sınav sorusu ve konu başlığı birbirine girmiş enkaz"))
    elif any("Tıbbi Patoloji" in v for v in opts.values()) and sum(1 for v in opts.values() if "Tıbbi Patoloji" in v) >= 3:
        # e.g. 50edcb644012 where B, C, D, E are all 'Tıbbi Patoloji'
        replacements_needed.append((qid, "Patoloji ders başlığı şıkların yerine basılmış"))
    elif any("has question stem" in iss for iss in issues):
        replacements_needed.append((qid, "Soru kökü şıkka kopyalanmış"))
    elif "duplicate options" in issues:
        replacements_needed.append((qid, "Mükerrer şık"))
    elif has_cut:
        clean_cuts.append((qid, "Şık ucunda ikinci soru birleşmesi"))
    else:
        replacements_needed.append((qid, "Diğer şık bozukluğu"))

print(f"Clean cuts: {len(clean_cuts)}")
print(f"Replacements/reconstruction needed: {len(replacements_needed)}")
print(f"Debris to quarantine: {len(debris_to_quarantine)}")
