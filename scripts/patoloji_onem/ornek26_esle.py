"""2026-27 örnek sorularını (meds_temp/patoloji_ornek26/cikti/<kod>.json, ders PDF'ine dayalı, sayfa numaralı) önem
listesi maddelerine eşler → meds_temp/patoloji_onem/ornek26_esleme.json {kod: {"<no>": "<madde id>"}}.

Puan: soru (kök + doğru şık + açıklama) ile madde (başlık, bilgi, alt, detay, alıntı) arasındaki ortak sözcük kökleri
(ders içi IDF ağırlıklı) + sayfa yakınlığı (alıntı sayfası ±1: +2,5; ±3: +1). Kurul/ders dışı eşleşme yapılmaz.
"""
import glob, json, math, re, collections
SRC = '/home/indu/medsor/meds/src/data/patoloji_onem'
Y = '/home/indu/medsor/meds_temp/patoloji_ornek26/cikti'
OUT = '/home/indu/medsor/meds_temp/patoloji_onem/ornek26_esleme.json'
DUR = set('aşağıdakilerden hangisi hangisidir değildir olan olarak için ile veya daha çok sıklıkla genellikle durum bulgu doğru yanlış en sık olası'.split())


def kokler(s):
    s = s.replace('İ', 'i').replace('I', 'ı').lower()
    return [w[:5] for w in re.findall(r'[a-zçğıöşü0-9]{4,}', s) if w not in DUR]


out, rapor = {}, collections.Counter()
for f in sorted(glob.glob(f'{Y}/*.json')):
    y = json.load(open(f)); kod = y['kod']
    d = json.load(open(f'{SRC}/{kod}.json'))
    M = d['maddeler']
    mt = {m['id']: kokler(' '.join([m['baslik'], m['bilgi'], ' '.join(m.get('alt') or []), m.get('detay', ''), ' '.join(a['metin'] for a in m['alinti'])])) for m in M}
    df = collections.Counter(t for v in mt.values() for t in set(v))
    idf = {t: math.log((len(M) + 1) / (c + 0.5)) for t, c in df.items()}
    ms = {i: set(v) for i, v in mt.items()}
    sayfa = {m['id']: [a['sayfa'] for a in m['alinti']] for m in M}
    out[kod] = {}
    for q in y['sorular']:
        qt = set(kokler(' '.join([q['soru'], q['secenekler'].get(q['dogru'], ''), q.get('aciklama', ''), q.get('konu', '')])))
        en, en_p = None, -1
        for m in M:
            p = sum(idf.get(t, 0) for t in qt & ms[m['id']])
            yak = min([abs(s - q.get('sayfa', -99)) for s in sayfa[m['id']]] or [99])
            p += 2.5 if yak <= 1 else 1 if yak <= 3 else 0
            p += m['puan'] / 200  # eşitlikte önemli madde
            if p > en_p: en, en_p = m['id'], p
        out[kod][str(q['no'])] = en
        rapor['zayif' if en_p < 4 else 'iyi'] += 1
json.dump(out, open(OUT, 'w'), ensure_ascii=False, indent=1)
print(sum(len(v) for v in out.values()), 'soru eşlendi', dict(rapor))
