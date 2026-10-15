#!/usr/bin/env python3
"""Sesli anlatım: her ders için kaynak kiti (slayt metni + Öğren destesi + çıkmış + spot) ve sıra listesi.

Çıktı: meds_temp/sesli_anlatim/kitler/<key>.md, meds_temp/sesli_anlatim/liste.json
Kaynak önceliği: güncel slayt (temp2) > V2 deste > V1 deste. Model yok, yalnız yerel okuma.
"""
import json, os, re, glob, unicodedata
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
ROOT = MEDS.parent
TEMP2 = ROOT / 'meds_temp' / 'temp2' / 'drive_root'
OUT = ROOT / 'meds_temp' / 'sesli_anlatim'

# Kullanıcının verdiği sıra (Tıbbi Patoloji dosya no → Kurul 1 ders no); hepsi Microsoft Emel.
EMEL_SIRA = [28, 29, 30, 32, 33, 37, 38, 41, 42, 44, 45, 46, 48, 49, 53, 55, 67, 56, 9, 12, 13, 15, 16, 20, 24, 25, 26]

decks = json.load(open(MEDS / 'src/data/interactive_learning_decks.json'))
byid = {d['id']: d for d in decks}
pdfsrc = json.load(open(MEDS / 'src/data/deckPdfSources.json'))['decks']
past = json.load(open(MEDS / 'src/data/pastQuestions.json'))

dersler = {}
for d in decks:
    m = re.match(r'^k1p-(k1-(\d+)-.+?)(-v2)?$', d['id'])
    if not m: continue
    key, no = m.group(1), int(m.group(2))
    e = dersler.setdefault(key, {'key': key, 'no': no, 'v1': None, 'v2': None})
    e['v2' if m.group(3) else 'v1'] = d['id']

def _nfc(x):
    return unicodedata.normalize('NFC', x).casefold()

_MD = {}
for _p in TEMP2.rglob('*.md'):
    _MD[_nfc(str(_p.relative_to(TEMP2)))] = _p

def md_bul(rel):
    """Ad (NFC/NFD farkı gözetmeden) temp2 .md dosyası; temp2 adı ilk noktada kesilmişse önek eşleşmesi."""
    hit = _MD.get(_nfc(rel.rsplit('.', 1)[0] + '.md'))
    if hit: return hit
    hedef = _nfc(rel.rsplit('.', 1)[0])
    aday = [(k, v) for k, v in _MD.items() if hedef.startswith(k[:-3]) and len(k[:-3]) >= len(hedef) * 0.6]
    return max(aday, key=lambda kv: len(kv[0]))[1] if aday else None

def pdf_metin(rel):
    """temp2'de yoksa ham PDF'ten (pdftotext, sayfa sayfa)."""
    import subprocess
    pdf = ROOT / 'meds_downloads' / 'drive_root' / rel
    if not pdf.exists():
        cands = [q for q in pdf.parent.glob('*.pdf') if _nfc(q.name) == _nfc(pdf.name)] if pdf.parent.exists() else []
        if not cands: return None
        pdf = cands[0]
    try:
        t = subprocess.run(['pdftotext', '-layout', str(pdf), '-'], capture_output=True, text=True, timeout=120).stdout
    except Exception:
        return None
    return '\n'.join(f'## Sayfa {i}\n\n{x.strip()}' for i, x in enumerate(t.split('\f'), 1) if x.strip())

def deck_md(did, full=True):
    d = byid[did]
    out = [f"### Deste `{did}` — {d.get('title')}", '']
    for i, s in enumerate(d.get('slides') or [], 1):
        out.append(f"#### Adım {i}: {s.get('title','')}" + (f" — {s['subtitle']}" if s.get('subtitle') else ''))
        nar = (s.get('synthesisNarrative') or s.get('content') or '').strip()
        if nar: out.append(nar)
        for p in s.get('spotPearls') or []: out.append(f"- {p}")
        if full:
            for t in s.get('medicalTerms') or []:
                out.append(f"- Terim: **{t.get('term')}** — {t.get('explanation','')}")
            for el in s.get('interactiveElements') or []:
                if el.get('type') == 'interactive_table' and el.get('tableRows'):
                    out.append(f"- Tablo: {el.get('tableTitle','')} | " + ' / '.join(el.get('tableHeaders') or []))
                    for r in el['tableRows']:
                        out.append('  - ' + ' | '.join(c.get('text', '') for c in r.get('cells', [])))
        out.append('')
    return '\n'.join(out)

def slide_text(did):
    src = pdfsrc.get(did) or {}
    parts = []
    for f in src.get('files') or []:
        p = md_bul(f['path'])
        if p:
            parts.append(f"### PDF: {f['path']} ({f.get('pages')} sayfa)\n\n" + p.read_text(encoding='utf-8'))
        elif (pm := pdf_metin(f['path'])):
            parts.append(f"### PDF: {f['path']} ({f.get('pages')} sayfa, ham PDF metni)\n\n" + pm)
        else:
            parts.append(f"### PDF: {f['path']} — slayt metni YOK")
    return '\n\n'.join(parts), [f['path'] for f in src.get('files') or []], sum(int(f.get('pages') or 0) for f in src.get('files') or [])

def past_md(ids):
    out = []
    for q in past:
        dl = ((q.get('iliski') or {}).get('deste')) or []
        if not set(dl) & ids: continue
        cs = q.get('checkSolve') or {}
        if cs.get('status') in ('kaldirildi', 'karantina') or q.get('status') in ('deleted', 'rejected'): continue
        opts = q.get('options') or []
        o = '\n'.join(f"  {'✔' if x.get('isCorrect') else '-'} {x.get('key')}) {x.get('text','')}" for x in opts)
        out.append(f"- [{q.get('examYear') or '?'}] {q.get('stem','').strip()}\n{o}")
    return out

def spots_md(no):
    p = ROOT / 'meds_temp' / 'sinav_spotlari' / 'spotlar' / f'{no:02d}.jsonl'
    if not p.exists(): return []
    out = []
    for line in p.read_text(encoding='utf-8').splitlines():
        if not line.strip(): continue
        s = json.loads(line)
        out.append(f"- ({s.get('kategori')}, önem {s.get('onem')}) **{s.get('baslik')}**: {s.get('spot')}" + (f" Tuzak: {s['tuzak']}" if s.get('tuzak') else ''))
    return out

def note_path(no):
    hits = glob.glob(str(ROOT / 'meds_database_v2' / 'ders_notlari_k1' / 'notlar' / f'{no:02d}_*.md'))
    return hits[0] if hits else None

liste = []
emel = set(EMEL_SIRA)
sira = EMEL_SIRA + sorted(n for n in {e['no'] for e in dersler.values()} if n not in emel)
for no in sira:
    cands = [e for e in dersler.values() if e['no'] == no]
    if not cands: print('YOK', no); continue
    e = cands[0]
    main = e['v2'] or e['v1']
    stext, pdfs, pages = slide_text(main)
    if not pdfs and e['v1']: stext, pdfs, pages = slide_text(e['v1'])
    ids = {x for x in (e['v1'], e['v2']) if x}
    pq = past_md(ids); sp = spots_md(no)
    title = byid[main].get('title')
    kit = [f"# Sesli anlatım kiti — {e['key']}", f"Başlık: {title}", f"PDF: {', '.join(pdfs) or 'yok'} · toplam {pages} sayfa", f"Ders notu (müfredat özeti): {note_path(no) or 'yok'}", '',
           '## 1. GÜNCEL AMFİ SLAYTI (birincil kaynak)', '', stext or '_slayt metni yok_', '',
           '## 2. ÖĞREN DESTESİ V2 (güncel)', '', deck_md(e['v2']) if e['v2'] else '_yok_', '',
           f'## 3. ÇIKMIŞ SORULAR ({len(pq)}) — bu bilgilere anlatımda "burası önemli" de', '', '\n'.join(pq) or '_bağlı çıkmış soru yok_', '',
           f'## 4. SINAV SPOTLARI ({len(sp)})', '', '\n'.join(sp) or '_yok_', '',
           '## 5. ÖĞREN DESTESİ V1 (eski; yalnız slaytla çelişmeyen ek bilgi için)', '', deck_md(e['v1'], full=False) if e['v1'] else '_yok_']
    (OUT / 'kitler' / f"{e['key']}.md").write_text('\n'.join(kit), encoding='utf-8')
    liste.append({'key': e['key'], 'no': no, 'baslik': title, 'v1': e['v1'], 'v2': e['v2'], 'pdf': pdfs, 'sayfa': pages,
                  'cikmis': len(pq), 'spot': len(sp), 'ses': 'emel', 'sira': len(liste) + 1})
json.dump(liste, open(OUT / 'liste.json', 'w'), ensure_ascii=False, indent=1)
for x in liste: print(x['sira'], x['ses'], x['key'], x['sayfa'], 'syf', x['cikmis'], 'çıkmış', x['spot'], 'spot', '|', '; '.join(p.split('/')[-1] for p in x['pdf']))
