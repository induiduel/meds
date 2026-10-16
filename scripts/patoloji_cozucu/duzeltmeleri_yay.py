#!/usr/bin/env python3
"""Soru çözücü denetiminde düzeltilen örnek soruları (kontrol.durum == duzeltildi) öteki kopyalara yayar:
  1) meds_temp/patoloji_ornek26/cikti/<kod>.json  (örnek soru kaynağı; ardından derle.py → MD/HTML/PDF)
  2) meds/src/data/patoloji_onem/<kod>.json        (önem listesi maddelerindeki ornek26 kopyaları)
  3) meds_temp/patoloji_onem/asistan2/{plan,cikti}  (sesli asistan v2: kök/şık + kok_ses, değişen şıkların yanlis/yardim metni)
Değişen şıkların asistan metinleri aşağıdaki ASISTAN_SIK sözlüğünde (asistan2 biçimi: "Doğrusu:" kalıbı, yardım tek cümle).
Sonra: asistan2/dogrula.py → asistan_ses.py <kodlar> → asistan_birlestir.py.
"""
import json, os
T = '/home/indu/medsor/meds_temp'
SRC = '/home/indu/medsor/meds/src/data/patoloji_onem'
A2 = f'{T}/patoloji_onem/asistan2'
ASISTAN_SIK = {
    ('13', 15, 'B'): {
        'yanlis': {'metin': 'Kronik evre şokun evreleri arasında sayılmaz; şokun üç evresi kompanse, ilerleyici ve geri dönüşümsüzdür. Doğrusu: ilerleyici evre.',
                   'ses': 'Kronik evre şokun evreleri arasında sayılmaz. Şokun üç evresi kompanse, ilerleyici ve geri dönüşümsüzdür. Doğrusu: ilerleyici evre.'},
        'yardim': {'metin': 'Kronik evre üç şok evresi arasında yok.', 'ses': 'Kronik evre üç şok evresi arasında yok.'}},
    ('14', 3, 'E'): {
        'yanlis': {'metin': 'Greft-versus-host hastalığı bir aşırı duyarlılık tipi değildir; donör T hücreleri alıcı dokusunu alloantijen olarak tanır. Doğrusu: miyastenia antikor aracılı Tip II hastalığıdır.',
                   'ses': 'Greft versus host hastalığı bir aşırı duyarlılık tipi değildir. Donör te hücreleri alıcı dokusunu alloantijen olarak tanır. Doğrusu: miyastenia antikor aracılı tip iki hastalığıdır.'},
        'yardim': {'metin': 'Greft-versus-host bir aşırı duyarlılık tipi değil.', 'ses': 'Greft versus host bir aşırı duyarlılık tipi değil.'}},
    ('14', 7, 'D'): {
        'yanlis': {'metin': 'Hiperakut red, alıcıda önceden oluşmuş antikorlarla dakikalar ile saatler içinde gelişir; tüberkülin testinde antikor değil T hücresi çalışır. Doğrusu: Tip IV.',
                   'ses': 'Hiperakut red, alıcıda önceden oluşmuş antikorlarla dakikalar ile saatler içinde gelişir. Tüberkülin testinde antikor değil te hücresi çalışır. Doğrusu: tip dört.'},
        'yardim': {'metin': 'Hiperakut red hazır antikorla olur, T hücresiyle değil.', 'ses': 'Hiperakut red hazır antikorla olur, te hücresiyle değil.'}},
    ('26', 4, 'A'): {
        'yanlis': {'metin': 'Retinoblastom bu sorunun cevabı değildir; VHL hastalığında retinada gelişen tümör hemanjiyoblastomdur. Doğrusu: serebellar hemanjiyoblastom.',
                   'ses': 'Retinoblastom bu sorunun cevabı değildir. Ve ha le hastalığında retinada gelişen tümör hemanjiyoblastomdur. Doğrusu: serebellar hemanjiyoblastom.'},
        'yardim': {'metin': 'Retinoblastom değil; retinada hemanjiyoblastom görülür.', 'ses': 'Retinoblastom değil, retinada hemanjiyoblastom görülür.'}},
}
yaz = lambda p, d, **k: json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, **k)
rapor = []
for f in sorted(os.listdir(f'{T}/patoloji_ornek26/cozucu/cikti')):
    kod = f[:-5]
    coz = json.load(open(f'{T}/patoloji_ornek26/cozucu/cikti/{f}'))
    duz = [q for q in coz['sorular'] if q['kontrol']['durum'] == 'duzeltildi']
    if not duz: continue
    # 1) örnek soru kaynağı
    kp = f'{T}/patoloji_ornek26/cikti/{kod}.json'; k = json.load(open(kp))
    eski = {}
    for q in duz:
        s = next(x for x in k['sorular'] if x['no'] == q['no'])
        eski[q['no']] = s['soru']
        if (s['soru'], s['secenekler'], s['dogru']) == (q['soru'], q['secenekler'], q['dogru']): continue
        s.update(soru=q['soru'], secenekler=q['secenekler'], dogru=q['dogru'])
        rapor.append(f'ornek26 {kod} s{q["no"]}')
    yaz(kp, k, separators=(',', ':'))
    # 2) önem listesi
    op = f'{SRC}/{kod}.json'; o = json.load(open(op)); n = 0
    for m in o['maddeler']:
        for s in m.get('ornek26') or []:
            q = next((q for q in duz if eski[q['no']] == s['kok'] or q['soru'] == s['kok']), None)
            if q and (s['kok'], s['secenekler'], s['dogru']) != (q['soru'], q['secenekler'], q['dogru']):
                s.update(kok=q['soru'], secenekler=q['secenekler'], dogru=q['dogru']); n += 1
    if n: yaz(op, o, separators=(',', ':')); rapor.append(f'onem {kod} {n}')
    # 3) asistan v2
    pp, cp = f'{A2}/plan/{kod}.json', f'{A2}/cikti/{kod}.json'
    p, c = json.load(open(pp)), json.load(open(cp))
    CS = {s['anahtar']: s for b in c['bolumler'] for nn in b['noktalar'] for s in nn.get('sorular') or []}
    for nn in p['noktalar']:
        for s in nn['sorular']:
            q = next((q for q in duz if s.get('tur') == 'ornek26' and s['kok'] in (eski[q['no']], q['soru'])), None)
            if not q: continue
            cs = CS[s['anahtar']]
            degisen = [h for h in q['secenekler'] if s['secenekler'].get(h) != q['secenekler'][h]]
            s.update(kok=q['soru'], secenekler=q['secenekler'], dogru=q['dogru'])
            cs['kok_ses'] = q['kok_ses']
            for h in degisen:
                yeni = ASISTAN_SIK[(kod, q['no'], h)]
                cs['yanlis'][h] = yeni['yanlis']; cs['yardim'][h] = yeni['yardim']
            rapor.append(f'asistan {kod} {s["anahtar"]} şık {degisen}')
    yaz(pp, p, indent=1); yaz(cp, c, indent=1)
print('\n'.join(rapor))
