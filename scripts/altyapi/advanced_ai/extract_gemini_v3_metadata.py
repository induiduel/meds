#!/usr/bin/env python3
"""Extract only Gemini v3 metadata that is approved for application access."""
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

TAG = 'aistudio_curated_20261005'

def norm(value):
    return ' '.join(str(value or '').lower().replace('ı','i').replace('ş','s').replace('ğ','g').replace('ü','u').replace('ö','o').replace('ç','c').split())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--export-root', default='/home/indu/medsor/meds_database_v3_export')
    ap.add_argument('--curriculum', default='/home/indu/medsor/meds/curriculum/kbu_tip_donem3_curriculum.json')
    ap.add_argument('--output-dir', default='/home/indu/medsor/meds_database/deepseek_meta_data')
    args = ap.parse_args()
    root, out = Path(args.export_root), Path(args.output_dir); out.mkdir(parents=True, exist_ok=True)
    curriculum = json.loads(Path(args.curriculum).read_text())
    committees = curriculum.get('committees', {})
    relations, synonym_map = [], {}
    for line in (root/'questions_curated.jsonl').open():
        if not line.strip(): continue
        q = json.loads(line); p = q.get('curation_provenance', {})
        if p.get('tag') != TAG: continue
        kurul = q.get('kurul'); key = f'TIP{310 + (int(kurul)-1)*10}' if str(kurul).isdigit() else None
        c = committees.get(key, {}) if key else {}
        topic = norm(q.get('konu')); candidates = []
        for core in c.get('core_topics', []):
            words = [w for w in norm(core).split() if len(w) > 3]
            score = sum(w in topic for w in words) / max(1, len(words))
            if score >= .2: candidates.append({'topic': core, 'score': round(score, 4)})
        candidates.sort(key=lambda x: x['score'], reverse=True)
        relations.append({'question_id': q.get('question_id'), 'committee': {'id': key, 'kurul': kurul, 'name': c.get('name')}, 'course': q.get('ders'), 'topic': q.get('konu'), 'curriculum_core_topic_candidates': candidates[:5], 'learning_outcomes': [], 'learning_outcome_status': 'not_present_in_gemini_source', 'evidence_chunks': q.get('evidence_chunks', []), 'taxonomy_metadata': q.get('taxonomy_metadata', {}), 'provenance': {'source': 'gemini_v3', 'tag': TAG, 'curated_by': p.get('curated_by'), 'curation_date': p.get('curation_date'), 'pipeline_version': p.get('pipeline_version'), 'extraction': 'metadata_only'}})
    thes = json.loads((root/'medical_thesaurus_expanded.json').read_text())
    for canonical, value in thes.items():
        synonym_map[canonical] = {'canonical': canonical, 'turkish': value.get('turkce'), 'latin': value.get('latin'), 'synonyms': value.get('esanlamlilar', []), 'abbreviations': value.get('kisaltmalar', []), 'key_components': value.get('anahtar_bilesenler', []), 'provenance': {'source': 'gemini_v3', 'tag': TAG, 'source_file': 'medical_thesaurus_expanded.json'}}
    meta = {'schema_version': '1.0', 'source': 'gemini_v3', 'source_tag': TAG, 'generated_at': datetime.now(timezone.utc).isoformat(), 'immutable_existing_database': True, 'learning_outcomes_note': 'Gemini exportunda kazanım alanı bulunmadığı için kazanımlar uydurulmamış, alan boş bırakılmıştır.', 'counts': {'question_relations': len(relations), 'synonym_terms': len(synonym_map)}}
    (out/'gemini_v3_question_curriculum_relations.json').write_text(json.dumps({'metadata': meta, 'items': relations}, ensure_ascii=False, indent=2))
    (out/'gemini_v3_medical_synonyms.json').write_text(json.dumps({'metadata': meta, 'items': synonym_map}, ensure_ascii=False, indent=2))
    digest = hashlib.sha256((json.dumps(relations, sort_keys=True)+json.dumps(synonym_map, sort_keys=True)).encode()).hexdigest()
    (out/'gemini_v3_metadata_manifest.json').write_text(json.dumps({**meta, 'sha256': digest, 'approved_public_files': ['gemini_v3_question_curriculum_relations.json','gemini_v3_medical_synonyms.json'], 'blocked_source_files': ['questions_curated.jsonl','lecture_notes_master_curated.jsonl','medical_thesaurus_expanded.json','audit_rejected_questions.jsonl']}, ensure_ascii=False, indent=2))
    print(json.dumps({**meta, 'sha256': digest}, ensure_ascii=False))
if __name__ == '__main__': main()
