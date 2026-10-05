# -*- coding: utf-8 -*-
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/drive_check_result.json', encoding='utf-8') as f:
    check_res = json.load(f)

new_files = check_res.get('newFiles', [])
print(f"Total files in drive_check_result: {len(new_files)}")

base_dir = ((__import__('os').environ.get('MEDS_DATABASE_DIR') or __import__('os').path.expanduser('~/meds_database')))
all_local = {}
for root, dirs, files in os.walk(base_dir):
    for f in files:
        all_local[f.lower().strip()] = os.path.join(root, f)

for item in new_files:
    fname = item.get('name', '').lower().strip()
    found_path = all_local.get(fname)
    print(f"File: {item.get('name')}")
    print(f"  Local status: {'FOUND at ' + found_path if found_path else 'NOT FOUND'}")
