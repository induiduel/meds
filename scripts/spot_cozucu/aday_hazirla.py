#!/usr/bin/env python3
"""Branş ders listesi + çıkmış soru adayları (Kurul 1) → meds_temp/spot_cozucu/<brans>/cikmis/<kod>.json

Aday = sitede görünen çıkmış soru: birleştirme kopyası (birlestirmeler.json), karantina, çöp, iptal değil. Müfredat eşlemesi
check-solve'un `mufredat.{kurul,ders,konu}` alanından. Aynı bilgiyi soran farklı yıl tekrarları `tekrar` grubunda toplanır
(similarPastQuestions bağı ya da kök+doğru şık benzerliği); grubun temsilcisi en yeni yıl. Ajan yalnız temsilcileri seçer,
gruptaki yıllar "kaç kez soruldu" bilgisidir.
Kullanım: python3 meds/scripts/spot_cozucu/aday_hazirla.py
"""
import json, os, re, unicodedata
from collections import defaultdict
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
W = MEDS.parent / 'meds_temp/spot_cozucu'
# branş → (müfredat ders adı, {kod: [check-solve konu adları]})
BRANS = {
    'enfeksiyon': ('Enfeksiyon Hastalıkları', {
        'e01': ['Cinsel Yolla Bulaşan Enfeksiyonlarda Tedavi'], 'e02': ['Genital Enfeksiyonlar'], 'e03': ['İzolasyon Yöntemleri'],
        'e04': ['Enfeksiyon Hastalıklarında Genel Kavramlar ve Temel Özellikler'], 'e05': ['Üriner Sistem Enfeksiyonları'],
        'e06': ['Cinsel yolla bulaşan hastalıklarda profilaksi ve korunma'], 'e07': ['Sifilis'], 'e08': ['Üretral Akıntı'],
        'e10': ['Mikroorganizmalarda Direnç Sorunu ve Antimikrobiyal Yönetim']}),
    'uroloji': ('Üroloji', {
        'u01': ['Üriner Obstrüksiyonun Fizyopatolojisi'], 'u02': ['Üriner Sistem Taş Hastalıkları Fizyopatolojisi'],
        'u03': ['Üriner Sistem Enfeksiyonları Lab. Bulguları ve Tedavi'],
        'u04': ['Üriner Sistem Enfeksiyonlarının Epidemiyoloji, Etiyoloji ve Semptomatolojisi'],
        'u05': ['Üriner Sistemin Spesifik Enfeksiyonları'], 'u06': ['Enürezis Nokturna']}),
}


def norm(s):
    s = unicodedata.normalize('NFKC', str(s or '')).lower().replace('i̇', 'i')
    return re.sub(r'[^0-9a-zçğıöşü]+', ' ', s).strip()


def kelimeler(s):
    return {w for w in norm(s).split() if len(w) > 2}


def jacc(a, b):
    return len(a & b) / max(1, len(a | b))


def main():
    Q = json.load(open(MEDS / 'data/pastQuestions.json'))
    gizli = set()
    for g in json.load(open(MEDS.parent / 'meds_database_v2/soru_birlestirme/birlestirmeler.json')).get('gruplar', []):
        if g.get('durum') != 'ayrildi':
            gizli |= {u for u in g['uyeler'] if u != g['asil']}
    try:
        silinen = {str(x.get('id') if isinstance(x, dict) else x) for x in json.load(open(MEDS / 'data/deleted_past_questions.json'))}
    except Exception:
        silinen = set()
    for brans, (ders, KONU) in BRANS.items():
        konu_kod = {k: kod for kod, ks in KONU.items() for k in ks}
        by = defaultdict(list)
        for q in Q:
            cs = q.get('checkSolve') or {}
            m = cs.get('mufredat') or {}
            if m.get('kurul') != 1 or m.get('ders') != ders or m.get('konu') not in konu_kod: continue
            if q['id'] in gizli or q['id'] in silinen or q.get('hidden') or q.get('iptal'): continue
            if cs.get('status') in ('karantina', 'kaldirildi') or q.get('status') == 'quarantined': continue
            opts = {o['key']: str(o.get('text') or '').strip() for o in q.get('options') or [] if o.get('key') in 'ABCDE'}
            if len(opts) < 4 or not q.get('stem') or q.get('correctAnswer') not in opts: continue
            sk = q.get('sinavKimligi') or {}
            yil = sk.get('yil') or (q.get('examYear') if re.match(r'^\d{4}-\d{4}$', str(q.get('examYear'))) else None)
            by[konu_kod[m['konu']]].append({
                'id': q['id'], 'yil': yil, 'sinav': sk.get('etiket') or str(q.get('examYear') or 'Yılı belirsiz'),
                'kok': q['stem'].strip(), 'secenekler': opts, 'dogru': q['correctAnswer'],
                'benzer_id': [s.get('id') for s in q.get('similarPastQuestions') or [] if s.get('id')],
                **({'dikkat': True} if q.get('olasiHataliKayit') else {})})
        for kod, L in by.items():
            # tekrar grupları: bağlı kimlik ya da (kök benzer + doğru şık metni aynı) ya da kök çok benzer
            ust = {c['id']: c['id'] for c in L}
            def bul(x):
                while ust[x] != x: ust[x] = ust[ust[x]]; x = ust[x]
                return x
            def bag(a, b): ust[bul(a)] = bul(b)
            kw = {c['id']: kelimeler(c['kok'] + ' ' + ' '.join(sorted(c['secenekler'].values()))) for c in L}
            dg = {c['id']: norm(c['secenekler'][c['dogru']]) for c in L}
            ids = {c['id'] for c in L}
            for i, a in enumerate(L):
                for b in a['benzer_id']:
                    if b in ids: bag(a['id'], b)
                for b in L[i + 1:]:
                    j = jacc(kw[a['id']], kw[b['id']])
                    if j >= 0.8 or (j >= 0.55 and dg[a['id']] == dg[b['id']]): bag(a['id'], b['id'])
            G = defaultdict(list)
            for c in L: G[bul(c['id'])].append(c)
            out = []
            for uy in G.values():
                uy.sort(key=lambda c: (c['yil'] or '0000', c['id']), reverse=True)
                t = dict(uy[0]); t.pop('benzer_id')
                t['tekrar'] = [{'id': c['id'], 'sinav': c['sinav']} for c in uy[1:]]
                t['yillar'] = sorted({c['yil'] for c in uy if c['yil']})
                out.append(t)
            out.sort(key=lambda c: (-len(c['tekrar']), c['yil'] or ''))
            (W / brans / 'cikmis').mkdir(parents=True, exist_ok=True)
            json.dump(out, open(W / brans / 'cikmis' / f'{kod}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            print(brans, kod, 'aday', len(L), '→ tekil', len(out), '· tekrarlı', sum(1 for c in out if c['tekrar']))
        # ajan girdisi: ders bilgisi + örnek soru hedefi (çözücü seti 20–40 soru: tekil çıkmış + örnek; uzun PDF'te daha çok örnek)
        (W / brans / 'girdi').mkdir(parents=True, exist_ok=True)
        for x in json.load(open(W / brans / 'pdf_liste.json')):
            c = len(by.get(x['kod']) and json.load(open(W / brans / 'cikmis' / f"{x['kod']}.json")) or [])
            hedef = max(14, min(30, round(0.5 * c + 0.15 * x['sayfa'])))
            json.dump({**x, 'brans': brans, 'cikmis_tekil': c, 'ornek_hedef': hedef}, open(W / brans / 'girdi' / f"{x['kod']}.json", 'w', encoding='utf-8'),
                      ensure_ascii=False, indent=1)
            print('  girdi', x['kod'], 'çıkmış', c, 'örnek hedefi', hedef)


if __name__ == '__main__':
    main()
