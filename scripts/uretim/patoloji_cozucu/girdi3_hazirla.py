"""3. tur girdisi: canlı ders metninden yeni sorular. girdi3/<kod>.json"""
import json, os
A = os.path.dirname(os.path.abspath(__file__))
M = '/home/indu/medsor/meds/data/sesli_anlatim/metin'
CANLI = {'01':'k1-02-patolojiye-giris','02':'k1-04-hucre-hasari-ve-nekroz-i','03':'k1-05-hucre-hasari-ve-nekroz-ii','04':'k1-03-hucresel-adaptasyonlar',
'05':'k1-07-hucre-ici-birikimler-ve-kalsifikasyonlar','06':'k1-08-hucresel-yaslanma','07':'k1-09-akut-enflamasyon-vaskuler-degisiklikler-ve-hucrese',
'08':'k1-12-enflamasyonun-kimyasal-mediyatorleri','09':'k1-13-kronik-ve-granulomatoz-enflamasyon','10':'k1-15-doku-onarimi-ve-yara-iyilesmesi',
'11':'k1-16-odem-hiperemi-konjesyon-ve-kanama','12':'k1-20-tromboz-patofizyolojisi','13':'k1-24-emboli-enfarktus-ve-sok','14':'k1-25-asiri-duyarlilik-ve-otoimmunite',
'15':'k1-26-genetik-pediatrik-ve-cevresel-patoloji','16':'k1-28-tumor-biyolojisi-ve-terminolojisi','17':'k1-29-karsinojenezin-molekuler-temeli',
'18':'k1-30-ileri-tumor-genetigi-ve-metabolizmasi','19':'k1-32-tumor-immunolojisi-ve-metastaz-mekanizmalari','20':'k1-33-tumor-evrelemesi-derecelendirme-ve-laboratuvar-tan',
'21':'k1-37-glomeruler-hastaliklar-nefrotik-sendrom','22':'k1-38-glomeruler-hastaliklar-nefritik-sendrom','23':'k1-41-sistemik-hastaliklarda-bobrek-hasari',
'24':'k1-42-tubulointerstisyel-hastaliklar','25':'k1-44-vaskuler-ve-kistik-bobrek-hastaliklari','26':'k1-45-bobrek-tumorleri','26b':'k1-46-mesane-hastaliklari-ve-tumorleri',
'28':'k1-48-vulva-vajen-ve-serviks-hastaliklari','39':'k1-49-invaziv-serviks-kanseri-ve-endometriyozis','30':'k1-53-endometriyal-hiperplazi-ve-kanserleri k1-54-uterus-duz-kas-ve-trofoblastik-tumorleri',
'31':'k1-55-over-tumorleri','32':'k1-67-gebelik-hastaliklari','33':'k1-56-memenin-benign-hastaliklari','34':'k1-66-erkek-genital-sistem-ve-prostat-hastaliklari','35':'k1-65-meme-kanseri-ve-molekuler-tipleri'}
for kod, keys in CANLI.items():
    g2 = json.load(open(f'{A}/girdi2/{kod}.json'))
    tam = json.load(open(f'{A}/cikti_tam/{kod}.json'))['sorular']
    yol = [f'{M}/{k}.md' for k in keys.split()]
    kel = len(open(yol[0]).read().split())
    hedef = max(10, min(25, round(kel / 230)))
    json.dump({'kod': kod, 'no': g2['no'], 'baslik': g2['baslik'], 'canli_metin': yol, 'yeni_soru_sayisi': hedef,
               'mevcut': [{'no': q['no'], 'tur': q['tur'], 'soru': q['soru'], 'dogru': q['secenekler'][q['dogru']]} for q in tam],
               'onem': g2['onem']}, open(f'{A}/girdi3/{kod}.json', 'w'), ensure_ascii=False, indent=1)
    print(kod, len(tam), hedef)
