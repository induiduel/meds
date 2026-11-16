#!/usr/bin/env python3
"""Create additive, provenance-tagged RAG chunks for the Gemini v3 export.

No existing question, lecture, or local RAG file is modified. Output is one
append-only JSONL artifact consumed by the optional v3 RAG loader.
"""
import argparse, json, hashlib, re
from pathlib import Path
from datetime import datetime, timezone

TAG = 'aistudio_curated_20261005'

def fold(s):
    return str(s or '').replace('\r', '').strip()

def split_text(text, target=900, overlap=120):
    text = fold(text)
    if not text: return []
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
    out, current = [], ''
    for paragraph in paragraphs:
        if current and len(current) + len(paragraph) + 2 > target:
            out.append(current)
            tail = current[-overlap:]
            current = (tail + '\n' + paragraph).strip()
        else:
            current = (current + '\n\n' + paragraph).strip()
    if current: out.append(current)
    return out

def chunk_id(kind, doc, index):
    return f'gemini_v3:{kind}:{doc}:c{index}'

def base(kind, doc, content, index, **meta):
    return {
      'chunk_id': chunk_id(kind, doc, index), 'document_id': doc,
      'document_type': f'gemini_v3_{kind}', 'content': content,
      'hash': hashlib.sha256(content.encode('utf-8')).hexdigest()[:16],
      'source_tag': TAG, 'source_label': 'Gemini v3 · AI Studio küratörlü',
      'created_at': datetime.now(timezone.utc).isoformat(), 'metadata': meta
    }

def read_jsonl(path):
    for line in path.read_text(encoding='utf-8', errors='replace').splitlines():
        if not line.strip(): continue
        try:
            value = json.loads(line)
            if isinstance(value, dict): yield value
        except Exception: pass

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--root', type=Path, default=Path('/home/indu/medsor/meds_database_v3_export')); ap.add_argument('--output', type=Path)
    a = ap.parse_args(); root = a.root; output = a.output or root / 'gemini_v3_rag_chunks.jsonl'; rows = []
    for q in read_jsonl(root / 'questions_curated.jsonl'):
        if q.get('curation_provenance', {}).get('tag') != TAG: continue
        body = '\n'.join([f"Soru: {q.get('stem','')}", *(f"{k}) {v}" for k,v in (q.get('options') or {}).items()), f"Açıklama: {q.get('explanation','')}", f"Ders: {q.get('ders','')} | Konu: {q.get('konu','')}", f"Kanıt chunkları: {', '.join(q.get('evidence_chunks') or [])}"])
        rows.append(base('question', q.get('question_id',''), body, 0, committee=q.get('kurul'), discipline=q.get('ders'), topic=q.get('konu'), status=q.get('status'), evidence_chunks=q.get('evidence_chunks', []), medical_accuracy_score=q.get('medical_accuracy_score')))
    lectures = {x.get('source_id'): x for x in read_jsonl(root / 'lecture_notes_master_curated.jsonl') if x.get('curation_tag') == TAG}
    for sid, note in lectures.items():
        md = root / note.get('markdown_path','')
        if not md.exists(): continue
        for index, content in enumerate(split_text(md.read_text(encoding='utf-8', errors='replace'))):
            page = None
            match = re.search(r'Slayt Sayfa\s+(\d+)', content, re.I)
            if match: page = int(match.group(1))
            rows.append(base('lecture', sid, content, index, title=note.get('title'), page=page, committee=note.get('kurul'), discipline=note.get('ders'), markdown_path=note.get('markdown_path')))
    thesaurus_path = root / 'medical_thesaurus_expanded.json'
    if thesaurus_path.exists():
        data = json.loads(thesaurus_path.read_text(encoding='utf-8'))
        for key, value in data.items():
            content = '\n'.join([f"Terim: {key}", str(value.get('turkce','')), f"Latince: {value.get('latin','')}", f"Eş anlamlılar: {', '.join(value.get('esanlamlilar', []))}", f"Anahtar bileşenler: {', '.join(value.get('anahtar_bilesenler', []))}"])
            rows.append(base('term', key, content, 0, provenance='file_manifest_verified', category=value.get('anahtar_bilesenler', [])[-1] if value.get('anahtar_bilesenler') else None))
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('w', encoding='utf-8') as f:
        for row in rows: f.write(json.dumps(row, ensure_ascii=False, separators=(',', ':')) + '\n')
    summary = {'generated_at': datetime.now(timezone.utc).isoformat(), 'output': str(output), 'chunks': len(rows), 'questions': sum(x['document_type']=='gemini_v3_question' for x in rows), 'lecture_chunks': sum(x['document_type']=='gemini_v3_lecture' for x in rows), 'terms': sum(x['document_type']=='gemini_v3_term' for x in rows), 'target_chars': 900, 'overlap_chars': 120, 'immutable_existing_data': True, 'source_tag': TAG}
    output.with_suffix('.manifest.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8'); print(json.dumps(summary, ensure_ascii=False))

if __name__ == '__main__': main()
