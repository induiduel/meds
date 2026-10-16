"""Sesli sınav asistanı planı: her ders için anlatılacak adımlar ve sorulacak sorular (deterministik).
Kaynak: meds/src/data/patoloji_onem/<kod>.json (birlestir.py çıktısı). Çıktı: meds_temp/patoloji_onem/asistan/plan/<kod>.json.

Seçim: sınava uygun (kaynak metin, klinik değil) maddelerden puanı ≥80 olanlar + tüm sınav adayları; en az 8 adım (puan
sırasıyla tamamlanır), en çok 22 (adaylar korunur, düşük puanlılar düşer). Anlatım sırası slayt (alıntı sayfası) sırası.
Soru: aday ya da puanı ≥90 olan adımda; önce bağlı çıkmış soru (ilki), yoksa örnek soru.
"""
import json, os, re, sys
SRC = '/home/indu/medsor/meds/src/data/patoloji_onem'
OUT = '/home/indu/medsor/meds_temp/patoloji_onem/asistan/plan'
ilk = lambda m: min([a['sayfa'] for a in m.get('alinti') or []] or [9999])
kodlar = sys.argv[1:] or [d['kod'] for d in json.load(open(f'{SRC}/index.json'))['dersler']]
top_a = top_s = 0
for kod in kodlar:
    d = json.load(open(f'{SRC}/{kod}.json'))
    aday = {a['id']: a for a in d.get('sinavAdaylari') or []}
    uygun = [m for m in d['maddeler'] if m.get('sinavUygun') is not False]
    sec = [m for m in uygun if m['puan'] >= 80 or m['id'] in aday]
    if len(sec) < 8:
        sec += [m for m in sorted(uygun, key=lambda m: -m['puan']) if m not in sec][:8 - len(sec)]
    if len(sec) > 22:
        sec = sorted(sec, key=lambda m: (m['id'] not in aday, -m['puan']))[:22]
    sec.sort(key=lambda m: (ilk(m), -m['puan']))
    adimlar = []
    for m in sec:
        a = aday.get(m['id'])
        s = None
        if a or m['puan'] >= 90:
            cid = next((i for i in m.get('cikmis') or [] if i in (d.get('cikmis') or {})), None)
            if cid:
                c = d['cikmis'][cid]; s = {'anahtar': f'c-{cid}', 'tur': 'cikmis', 'sinav': c['sinav'], 'kok': c['kok'], 'secenekler': c['secenekler'], 'dogru': c['dogru']}
            elif m.get('ornek_soru'):
                o = m['ornek_soru']; s = {'anahtar': f'o-{m["id"]}', 'tur': 'ornek', 'kok': o['kok'], 'secenekler': o['secenekler'], 'dogru': o['dogru'], 'aciklama': o.get('aciklama', '')}
        adimlar.append({'id': m['id'], 'puan': m['puan'], 'aday': a['sira'] if a else None, 'baslik': m['baslik'], 'bilgi': m['bilgi'], 'alt': m.get('alt') or [],
                        'detay': m.get('detay', ''), 'neden': m.get('neden', ''), 'sayfalar': sorted({x['sayfa'] for x in m.get('alinti') or []}),
                        'kategori': m.get('kategori', 'patoloji'), 'soru': s})
    top_a += len(adimlar); top_s += sum(1 for x in adimlar if x['soru'])
    json.dump({'kod': kod, 'no': d['no'], 'baslik': d['baslik'], 'pdf': d['pdf'], 'pdf_metin': f'pdf_metin/{kod}.md', 'ozet': d['ozet'],
               'soruSayisi': d.get('soruSayisi', 1), 'adimlar': adimlar}, open(f'{OUT}/{kod}.json', 'w'), ensure_ascii=False, indent=1)
    print(kod, len(adimlar), 'adım', sum(1 for x in adimlar if x['soru']), 'soru')
print('TOPLAM', top_a, 'adım', top_s, 'soru')
