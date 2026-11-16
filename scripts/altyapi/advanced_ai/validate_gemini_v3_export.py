#!/usr/bin/env python3
"""Validate the external Gemini v3 export without mutating the existing database."""
import argparse, json, hashlib
from pathlib import Path
from datetime import datetime, timezone

TAG = "aistudio_curated_20261005"

def jsonl(path):
    rows, errors = [], []
    if not path.exists(): return rows, errors
    for line_no, line in enumerate(path.read_text(encoding='utf-8', errors='replace').splitlines(), 1):
        if not line.strip(): continue
        try:
            value = json.loads(line)
            if isinstance(value, dict): rows.append(value)
            else: errors.append({"line": line_no, "reason": "object_required"})
        except Exception as exc: errors.append({"line": line_no, "reason": type(exc).__name__})
    return rows, errors

def tagged(row):
    return row.get('curation_provenance', {}).get('tag') == TAG or row.get('curation_tag') == TAG or row.get('source_tag') == TAG

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--root', type=Path, default=Path('/home/indu/medsor/meds_database_v3_export')); ap.add_argument('--report', type=Path)
    a = ap.parse_args(); root = a.root; report = a.report or root / 'integration_report.json'
    q, qe = jsonl(root / 'questions_curated.jsonl'); l, le = jsonl(root / 'lecture_notes_master_curated.jsonl'); rej, re = jsonl(root / 'audit_rejected_questions.jsonl')
    thesaurus_path = root / 'medical_thesaurus_expanded.json'
    try: thesaurus = json.loads(thesaurus_path.read_text(encoding='utf-8')) if thesaurus_path.exists() else {}
    except Exception as exc: thesaurus = {}; le.append({'file': str(thesaurus_path), 'reason': type(exc).__name__})
    accepted_q = [x for x in q if tagged(x)]; accepted_l = [x for x in l if tagged(x)]
    rejected_tagged = [x for x in rej if tagged(x)]
    missing_q = len(q) - len(accepted_q); missing_l = len(l) - len(accepted_l)
    payload = {
      'generated_at': datetime.now(timezone.utc).isoformat(), 'source_root': str(root), 'source_tag': TAG,
      'immutable_existing_database': True,
      'files': {name: {'exists': (root/name).exists(), 'bytes': (root/name).stat().st_size if (root/name).exists() else 0} for name in ['questions_curated.jsonl','lecture_notes_master_curated.jsonl','medical_thesaurus_expanded.json','audit_rejected_questions.jsonl']},
      'accepted': {'questions': len(accepted_q), 'lecture_notes': len(accepted_l), 'thesaurus_terms': len(thesaurus) if isinstance(thesaurus, dict) else 0},
      'excluded': {'untagged_questions': missing_q, 'untagged_lecture_notes': missing_l, 'rejected_questions': len(rej), 'rejected_with_tag': len(rejected_tagged), 'parse_errors': len(qe)+len(le)+len(re)},
      'exclusion_reasons': {'untagged': 'Zorunlu Gemini provenance tag yok.', 'rejected': 'Audit tarafından reddedilmiş; uygulamaya dahil edilmez.', 'parse_error': 'Geçerli JSON/JSONL kaydı değil.'},
      'checks': {'question_ids_unique': len({x.get('question_id') for x in accepted_q}) == len(accepted_q), 'question_tags_present': all(tagged(x) for x in accepted_q), 'lecture_tags_present': all(tagged(x) for x in accepted_l), 'thesaurus_file_readable': isinstance(thesaurus, dict)},
      'fingerprint': hashlib.sha256((''.join(str(x.get('question_id','')) for x in accepted_q) + ''.join(str(x.get('source_id','')) for x in accepted_l)).encode()).hexdigest(),
      'parse_errors': qe + le + re,
    }
    report.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8'); print(json.dumps(payload, ensure_ascii=False))

if __name__ == '__main__': main()
