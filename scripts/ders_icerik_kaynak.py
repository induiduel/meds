#!/usr/bin/env python3
"""Ders içerik paketinde PDF sayfası (`s`) olmayan terim/kısaltma/bilgi kayıtlarına kaynak sayfayı yazar.
Kullanım: python3 scripts/ders_icerik_kaynak.py [<key> ...]  (anahtarsız: tümü). Önce ders_icerik_adim.py çalışmış olmalı.
Sıra: adim → o slaytın pdfSayfalari[0]; adim yoksa terimin adı geçen ilk içerik slaytı. Kaynak dışı sayfa uydurulmaz:
bulunamazsa kayıt 'kaynaksız' sayılır, ders_icerik_dogrula.py HATA verir."""
import json, os, re, sys, glob
R = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
nz = lambda t: re.sub(r'\s+', ' ', re.sub(r'[^\wçğıöşü ]', ' ', (t or '').lower())).strip()
def metin(s): return nz(json.dumps(s, ensure_ascii=False))
def yaz(key):
    p = os.path.join(R, 'src/data/ders_icerik', key + '.json')
    dk = os.path.join(R, 'src/data/decks/items', f'k2p-{key}.json')
    if not (os.path.exists(p) and os.path.exists(dk)): return None
    d = json.load(open(p, encoding='utf-8')); sl = json.load(open(dk, encoding='utf-8'))['slides']
    ic = [s for s in sl if not s.get('isCheckpoint') and not s.get('isGameFinale')]
    sayfa = {s['slideNumber']: (s.get('pdfSayfalari') or [0])[0] for s in ic}
    n = eksik = 0
    for k, ad in (('terimler', 't'), ('bilgiler', 'b')):
        for x in d.get(k, []):
            if x.get('s'): continue
            a = x.get('adim') or next((s['slideNumber'] for s in ic if nz(x.get(ad)) and nz(x[ad]) in metin(s)), 0)
            pg = sayfa.get(a, 0)
            if pg: x['s'] = pg; x['adim'] = a; n += 1
            else: eksik += 1
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    return n, eksik
if __name__ == '__main__':
    keys = sys.argv[1:] or [os.path.basename(f)[:-5] for f in sorted(glob.glob(os.path.join(R, 'src/data/ders_icerik/*.json')))]
    for k in keys:
        r = yaz(k); print(k, 'deste yok/atlandı' if r is None else f'sayfa yazıldı {r[0]}, kaynaksız kalan {r[1]}')
