#!/usr/bin/env python3
"""Ders içerik paketindeki her kayda `adim` (ait olduğu Öğren slayt numarası) anahtarını yazar; PDF üretici (scripts/ders_pdf.mjs,
src/components/v15/dersPdfAkis.ts) yapay zekasız, yalnız bu anahtarla "anlatım → özet" akışı kurar. Yinelenebilir (idempotent).
Kullanım: python3 scripts/ders_icerik_adim.py [<key> ...]   (anahtar verilmezse tüm paketler)
Eşleme: n taşıyan kayıtta adim = n; PDF sayfası (s) taşıyanlarda sayfayı kapsayan ilk içerik slaytı (checkpoint hariç),
kapsayan yoksa başlangıcı sayfadan önce gelen en yakın slayt; kısaltma → adı ilk geçtiği slayt. Eşlenemeyen kayıt `adim: 0` (PDF sonu 'Ek')."""
import json, os, re, sys, glob
R = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
J = lambda p: json.load(open(p, encoding='utf-8'))

def metin(s):
    return ' '.join([s.get('title', ''), s.get('synthesisNarrative') or s.get('content') or ''] + [m.get('term', '') for m in s.get('medicalTerms', [])])

def adim_yaz(key):
    p = os.path.join(R, 'src/data/ders_icerik', key + '.json')
    dk = os.path.join(R, 'src/data/decks/items', f'k2p-{key}.json')
    if not (os.path.exists(p) and os.path.exists(dk)): return None
    d, deck = J(p), J(dk)
    sl = deck['slides']
    icerik = [s for s in sl if not s.get('isCheckpoint') and not s.get('isGameFinale')]
    def sayfa_adim(pg):
        if not pg: return 0
        for s in icerik:
            a, b = (s.get('pdfSayfalari') or [0, 0])[:2]
            if a <= pg <= b: return s['slideNumber']
        onceki = [s for s in icerik if (s.get('pdfSayfalari') or [999])[0] <= pg]
        return onceki[-1]['slideNumber'] if onceki else (icerik[0]['slideNumber'] if icerik else 0)
    sayilar = lambda x: sorted(v for v in (x if isinstance(x, list) else [x]) if isinstance(v, int))
    ilk = lambda x: (sayilar(x) or [0])[0]
    for x in d.get('bilgiler', []): x['adim'] = sayfa_adim(x.get('s'))
    nz = lambda t: re.sub(r'\s+', ' ', re.sub(r'[^\wçğıöşü ]', ' ', (t or '').lower())).strip()
    for x in d.get('terimler', []):
        a = sayfa_adim(x.get('s'))
        if not a:  # sayfası olmayan terim: destede terim olarak işaretlendiği, yoksa adı geçtiği ilk slayt
            ad = {nz(x['t'])} | {nz(e) for e in x.get('e', [])}
            a = next((s['slideNumber'] for s in icerik if any(nz(m.get('term')) in ad for m in s.get('medicalTerms', []))), 0) \
                or next((s['slideNumber'] for s in icerik if nz(x['t']) and nz(x['t']) in nz(metin(s))), 0)
        x['adim'] = a
    for x in d.get('hastaliklar', []): x['adim'] = sayfa_adim(ilk(x.get('s', [])))
    for x in d.get('onemli', []): x['adim'] = sayfa_adim(ilk(x.get('s', [])))
    for k in ('spotlar', 'tablolar', 'listeler', 'kartlar', 'quiz'):
        for x in d.get(k, []): x['adim'] = x.get('n') or 0
    for x in d.get('kisaltmalar', []):
        re_k = re.compile(r'(?<![\wçğıöşüÇĞİÖŞÜ])' + re.escape(x['k']) + r'(?![\wçğıöşüÇĞİÖŞÜ])')
        x['adim'] = next((s['slideNumber'] for s in icerik if re_k.search(metin(s))), 0)
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    eksik = sum(1 for k, v in d.items() if isinstance(v, list) for x in v if isinstance(x, dict) and x.get('adim') == 0)
    return eksik

if __name__ == '__main__':
    keys = sys.argv[1:] or sorted(os.path.basename(f)[:-5] for f in glob.glob(os.path.join(R, 'src/data/ders_icerik/*.json')))
    for k in keys:
        e = adim_yaz(k)
        print(k, 'deste yok/atlandı' if e is None else f'adim yazıldı, eşlenemeyen {e}')
