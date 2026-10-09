"""Öğren desteleri için deste → kazanımlar dizini üretir (src/data/kazanimlar/byDeck.json).

Kazanım dosyalarındaki slayt bağlantılarını (deckId) kullanır; bağlantısı olmayan desteleri
ders adı ile kazanım konusu adının kelime örtüşmesine göre eşler. Kazanım verisi değiştiğinde yeniden çalıştırın:
    python3 scripts/build_kazanim_deck_index.py
"""
import glob, json, os, re, unicodedata

ROOT = os.path.join(os.path.dirname(__file__), '..', 'src', 'data')
cat = json.load(open(os.path.join(ROOT, 'decks', 'catalog.json')))
ids = {c['id']: c for c in cat}
safe = lambda s: re.sub(r'[^a-zA-Z0-9_-]+', '_', s)

def fold(s):
    s = unicodedata.normalize('NFKD', str(s).lower().replace('ı', 'i'))
    return ''.join(ch for ch in s if not unicodedata.combining(ch))

STOP = {'ve', 'ile', 'icin', 'bir', 'olan', 'ders', 'temel', 'genel'}
def toks(s):
    return {w[:6] for w in re.findall(r'[a-z0-9]+', fold(s)) if len(w) >= 4 and w not in STOP}

by_link, konular = {}, []
for f in sorted(glob.glob(os.path.join(ROOT, 'kazanimlar', 'k[0-9].json'))):
    d = json.load(open(f))
    for ders in d['dersler']:
        for k in ders.get('konular', []):
            items = [{'m': z['metin'], 'c': len(z.get('cikmisSorular', [])), 'p': sorted({s['sayfa'] for s in z.get('slaytlar', []) if s.get('sayfa')})} for z in k['kazanimlar']]
            konular.append((toks(k['konu']), items))
            for z, it in zip(k['kazanimlar'], items):
                for did in {s.get('deckId') for s in z.get('slaytlar', []) if s.get('deckId')}:
                    lst = by_link.setdefault(did, [])
                    if it['m'] not in [x['m'] for x in lst]:
                        lst.append(it)

out = {}
for did, v in by_link.items():
    for cand in (did, 'k1p-' + did, 'learn-' + did, 'deck-' + did):
        if cand in ids:
            out[cand] = v
            break
for cid, c in ids.items():
    if cid in out:
        continue
    item = json.load(open(os.path.join(ROOT, 'decks', 'items', safe(cid) + '.json')))
    if item.get('kazanimlar'):
        out[cid] = [{'m': m, 'c': 0, 'p': []} for m in item['kazanimlar']]
        continue
    t = toks(c.get('title', '')) | toks(c.get('shortTitle', ''))
    best, score = None, 0.0
    for kt, items in konular:
        if not kt or not t:
            continue
        if len(t & kt) < 2:
            continue
        s = len(t & kt) / len(t | kt)
        if s > score:
            best, score = items, s
    if best and score >= 0.35:
        out[cid] = [{**x, 'p': []} for x in best]

json.dump(out, open(os.path.join(ROOT, 'kazanimlar', 'byDeck.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
print(f'{len(out)}/{len(ids)} deste eşlendi; eşlenmeyen: {sorted(set(ids) - set(out))}')
