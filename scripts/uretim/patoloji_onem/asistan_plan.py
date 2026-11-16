"""Sesli sınav asistanı planı v2: her ders için anlatılacak noktalar (zorunlu + seçmeli) ve sorulacak TÜM sorular.

Kaynaklar: meds/src/data/patoloji_onem/<kod>.json (önem listesi), meds_temp/patoloji_ornek26/cikti/<kod>.json (2026-27 örnek
soruları, PDF'e dayalı) + ornek26_esleme.json (soru → madde). Çıktı: meds_temp/patoloji_onem/asistan2/plan/<kod>.json.

Zorunlu nokta: sınava uygun ve puanı ≥80 · çıkmış sorusu olan · sınav adayı · 2026-27 örnek sorusunun hedefi.
Seçmeli nokta: sınava uygun, puanı 70–79 (ajan değer katanları seçer). Sıra: slayt (alıntı sayfası).
Sorular: dersteki her çıkmış soru bir kez (bağlı maddelerden puanı en yükseğine), her 2026-27 örnek sorusu, ve başka sorusu
olmayan ≥90 noktada önem listesinin örnek sorusu. Anahtar s1…sN (klip adı için kısa ve kararlı).
"""
import json, os, sys
SRC = '/home/indu/medsor/meds/src/data/patoloji_onem'
Y = '/home/indu/medsor/meds_temp/patoloji_ornek26/cikti'
ES = json.load(open('/home/indu/medsor/meds_temp/patoloji_onem/ornek26_esleme.json'))
OUT = '/home/indu/medsor/meds_temp/patoloji_onem/asistan2/plan'
os.makedirs(OUT, exist_ok=True)
ilk = lambda m: min([a['sayfa'] for a in m.get('alinti') or []] or [9999])
kodlar = sys.argv[1:] or [d['kod'] for d in json.load(open(f'{SRC}/index.json'))['dersler']]
T = {'zorunlu': 0, 'secmeli': 0, 'soru': 0}
for kod in kodlar:
    d = json.load(open(f'{SRC}/{kod}.json'))
    M = {m['id']: m for m in d['maddeler']}
    aday = {a['id']: a['sira'] for a in d.get('sinavAdaylari') or []}
    # çıkmış → en yüksek puanlı bağlı madde
    cik_hedef = {}
    for m in sorted(d['maddeler'], key=lambda m: -m['puan']):
        for i in m.get('cikmis') or []:
            if i in (d.get('cikmis') or {}) and i not in cik_hedef: cik_hedef[i] = m['id']
    yeni = json.load(open(f'{Y}/{kod}.json'))['sorular'] if os.path.exists(f'{Y}/{kod}.json') else []
    yeni_hedef = {str(q['no']): ES.get(kod, {}).get(str(q['no'])) for q in yeni}
    soru_m = {}
    for i, mid in cik_hedef.items():
        c = d['cikmis'][i]
        soru_m.setdefault(mid, []).append({'tur': 'cikmis', 'kaynak': i, 'sinav': c['sinav'], 'kok': c['kok'], 'secenekler': c['secenekler'], 'dogru': c['dogru']})
    for q in yeni:
        mid = yeni_hedef.get(str(q['no']))
        if mid in M:
            soru_m.setdefault(mid, []).append({'tur': 'ornek26', 'kaynak': f'ornek26-{q["no"]}', 'kok': q['soru'], 'secenekler': q['secenekler'],
                                                'dogru': q['dogru'], 'aciklama': q.get('aciklama', ''), 'sayfa': q.get('sayfa')})
    uygun = lambda m: m.get('sinavUygun') is not False
    zorunlu = {m['id'] for m in d['maddeler'] if (uygun(m) and m['puan'] >= 80) or m['id'] in aday or m['id'] in soru_m}
    for mid in zorunlu:
        m = M[mid]
        if not soru_m.get(mid) and m['puan'] >= 90 and m.get('ornek_soru'):
            o = m['ornek_soru']
            soru_m[mid] = [{'tur': 'ornek', 'kaynak': f'ornek-{mid}', 'kok': o['kok'], 'secenekler': o['secenekler'], 'dogru': o['dogru'], 'aciklama': o.get('aciklama', '')}]
    secmeli = {m['id'] for m in d['maddeler'] if uygun(m) and 70 <= m['puan'] < 80 and m['id'] not in zorunlu}
    sec = sorted(zorunlu | secmeli, key=lambda i: (ilk(M[i]), -M[i]['puan']))
    n = 0; noktalar = []
    for i in sec:
        m = M[i]; sorular = []
        for s in sorted(soru_m.get(i, []), key=lambda s: ({'cikmis': 0, 'ornek26': 1, 'ornek': 2}[s['tur']], s['kaynak'])):
            n += 1; sorular.append({'anahtar': f's{n}', **s})
        noktalar.append({'id': i, 'zorunlu': i in zorunlu, 'puan': m['puan'], 'aday': aday.get(i), 'tur': m['tur'], 'kategori': m.get('kategori', 'patoloji'),
                         'kaynak': m.get('kaynak', 'metin'), 'baslik': m['baslik'], 'bilgi': m['bilgi'], 'alt': m.get('alt') or [], 'detay': m.get('detay', ''),
                         'neden': m.get('neden', ''), 'sayfalar': sorted({x['sayfa'] for x in m.get('alinti') or []}), 'sorular': sorular})
    T['zorunlu'] += len(zorunlu); T['secmeli'] += len(secmeli); T['soru'] += n
    json.dump({'kod': kod, 'no': d['no'], 'baslik': d['baslik'], 'pdf': d['pdf'], 'pdf_metin': f'pdf_metin/{kod}.md', 'ozet': d['ozet'],
               'neden_onemli': d.get('neden_onemli', ''), 'soruSayisi': d.get('soruSayisi', 1), 'noktalar': noktalar},
              open(f'{OUT}/{kod}.json', 'w'), ensure_ascii=False, indent=1)
    print(kod, len(zorunlu), 'zorunlu', len(secmeli), 'seçmeli', n, 'soru')
print('TOPLAM', T)
