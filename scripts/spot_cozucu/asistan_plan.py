"""Sesli sınav asistanı (branş geneli) — ders planı: anlatılacak noktalar (zorunlu + seçmeli) ve sorulacak TÜM sorular.

Patolojideki asistan v2'nin (scripts/patoloji_onem/asistan_plan.py) Enfeksiyon/Üroloji karşılığı.
Kaynak: meds/src/data/<brans>_onem/<kod>.json (önem listesi; maddelerde çıkmış bağları ve `ornek26` örnek soruları, PDF'e dayalı).
Çıktı: meds_temp/spot_cozucu/<brans>/asistan/plan/<kod>.json.

Zorunlu nokta: puanı ≥80 · çıkmış ya da örnek sorusu olan. Seçmeli: 70–79 (ajan değer katanları seçer). Sıra: slayt (alıntı sayfası).
Sorular: dersteki her çıkmış bir kez (bağlı maddelerden puanı en yükseğine) + her örnek soru bir kez (kök tekrarı elenir). Anahtar s1…sN.
Kullanım: python3 meds/scripts/spot_cozucu/asistan_plan.py <brans> [kod ...]
"""
import json, os, sys
MEDS = '/home/indu/medsor/meds'
brans = sys.argv[1]
SRC = f'{MEDS}/src/data/{brans}_onem'
OUT = f'/home/indu/medsor/meds_temp/spot_cozucu/{brans}/asistan/plan'
os.makedirs(OUT, exist_ok=True)
ilk = lambda m: min([a['sayfa'] for a in m.get('alinti') or []] or [9999])
P = lambda m: int(m['puan'])
kodlar = sys.argv[2:] or [d['kod'] for d in json.load(open(f'{SRC}/index.json'))['dersler']]
T = {'zorunlu': 0, 'secmeli': 0, 'soru': 0}
for kod in kodlar:
    d = json.load(open(f'{SRC}/{kod}.json'))
    M = {m['id']: m for m in d['maddeler']}
    C = d.get('cikmis') or {}
    soru_m, gor = {}, set()
    for m in sorted(d['maddeler'], key=lambda m: -P(m)):
        for i in m.get('cikmis') or []:
            if i in C and i not in gor:
                gor.add(i); c = C[i]
                soru_m.setdefault(m['id'], []).append({'tur': 'cikmis', 'kaynak': i, 'sinav': c.get('sinav', ''), 'kok': c['kok'],
                                                       'secenekler': c['secenekler'], 'dogru': c['dogru']})
    kokler = set()
    for m in d['maddeler']:
        for j, q in enumerate(m.get('ornek26') or []):
            if q['kok'] in kokler: continue
            kokler.add(q['kok'])
            soru_m.setdefault(m['id'], []).append({'tur': 'ornek', 'kaynak': f'ornek-{m["id"]}-{j}', 'kok': q['kok'], 'secenekler': q['secenekler'],
                                                   'dogru': q['dogru'], 'aciklama': q.get('aciklama', ''), **({'zorluk': q['zorluk']} if q.get('zorluk') else {})})
    zorunlu = {m['id'] for m in d['maddeler'] if P(m) >= 80 or m['id'] in soru_m}
    secmeli = {m['id'] for m in d['maddeler'] if 70 <= P(m) < 80 and m['id'] not in zorunlu}
    sec = sorted(zorunlu | secmeli, key=lambda i: (ilk(M[i]), -P(M[i])))
    n = 0; noktalar = []
    for i in sec:
        m = M[i]; sorular = []
        for s in sorted(soru_m.get(i, []), key=lambda s: ({'cikmis': 0, 'ornek': 1}[s['tur']], s['kaynak'])):
            n += 1; sorular.append({'anahtar': f's{n}', **s})
        noktalar.append({'id': i, 'zorunlu': i in zorunlu, 'puan': P(m), 'aday': None, 'tur': m.get('tur', ''), 'kategori': brans,
                         'kaynak': 'metin', 'baslik': m['baslik'], 'bilgi': m['bilgi'], 'alt': m.get('alt') or [], 'detay': m.get('detay', ''),
                         'neden': m.get('neden', ''), 'sayfalar': sorted({x['sayfa'] for x in m.get('alinti') or []}), 'sorular': sorular})
    T['zorunlu'] += len(zorunlu); T['secmeli'] += len(secmeli); T['soru'] += n
    json.dump({'kod': kod, 'brans': brans, 'no': d['no'], 'baslik': d['baslik'], 'pdf': d['pdf'], 'pdf_metin': f'pdf_metin/{kod}.md', 'ozet': d['ozet'],
               'neden_onemli': d.get('neden_onemli', ''), 'noktalar': noktalar},
              open(f'{OUT}/{kod}.json', 'w'), ensure_ascii=False, indent=1)
    print(kod, len(zorunlu), 'zorunlu', len(secmeli), 'seçmeli', n, 'soru')
print('TOPLAM', T)
