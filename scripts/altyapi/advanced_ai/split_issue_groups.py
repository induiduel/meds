import json
import re

with open("meds_database_v2/phase14_backup/severe_issues.json", "r", encoding="utf-8") as f:
    issues = json.load(f)

# Group 1: Merged stems or branch names in options
merged_stem = [i for i in issues if any("has question stem" in iss or "branch/topic name" in iss for iss in i["issues"])]
# Group 2: Duplicate options
duplicates = [i for i in issues if "duplicate options" in i["issues"] and i not in merged_stem]
# Group 3: Placeholder options (Seçenek A)
placeholders = [i for i in issues if "A is placeholder" in i["issues"]]
# Group 4: Other merged / question marks / extremely long
others = [i for i in issues if i not in merged_stem and i not in duplicates and i not in placeholders]

print(f"Group 1 (Merged stems/branch in options): {len(merged_stem)}")
print(f"Group 2 (Duplicates): {len(duplicates)}")
print(f"Group 3 (Placeholders): {len(placeholders)}")
print(f"Group 4 (Other merged/corrupted): {len(others)}")

print("\n--- Group 1: Merged Stems/Branch Details (Sample) ---")
for m in merged_stem[:10]:
    print(f"ID: {m['id']} | Stem: {m['stem']}")
    print(f"Options: {m['options']}")
    print("-" * 40)

print("\n--- Group 4: Other Merged/Corrupted (Sample) ---")
for o in others[:10]:
    print(f"ID: {o['id']} | Issues: {o['issues']}")
    print(f"Stem: {o['stem']}")
    print(f"Options: {o['options']}")
    print("-" * 40)
