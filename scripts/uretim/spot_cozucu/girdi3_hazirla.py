#!/usr/bin/env python3
"""Branş çözücü 3. tur girdisi: canlı ders konularından yeni örnek sorular.
Kullanım: python3 girdi3_hazirla.py <brans>  →  meds_temp/spot_cozucu/<brans>/girdi3/<kod>.json"""
import json, sys
from pathlib import Path
M = Path('/home/indu/medsor/meds/data/sesli_anlatim/metin')
CANLI = {
 'enfeksiyon': {'e01': 'k1-17-cinsel-yolla-bulasan-enfeksiyonlarda-tedavi', 'e02': 'k1-34-genital-enfeksiyonlar', 'e03': 'k1-36-izolasyon-yontemleri',
   'e04': 'k1-21-enfeksiyon-hastaliklarinda-genel-kavramlar-ve-teme', 'e05': 'k1-52-uriner-sistem-enfeksiyonlari',
   'e06': 'k1-40-cinsel-yolla-bulasan-hastaliklarda-profilaksi-ve-k', 'e07': 'k1-50-sifilis', 'e08': 'k1-62-uretral-akinti',
   'e10': 'k1-69-mikroorganizmalarda-direnc-sorunu-ve-antimikrobiya'},
 'uroloji': {'u01': 'k1-11-uriner-obstruksiyonun-fizyopatolojisi', 'u02': 'k1-27-uriner-sistem-tas-hastaliklari-fizyopatolojisi',
   'u03': 'k1-51-uriner-sistem-enfeksiyonlari-laboratuvar-bulgulari', 'u04': 'k1-39-uriner-sistem-enfeksiyonlarinin-epidemiyoloji-etiy',
   'u05': 'k1-43-uriner-sistemin-spesifik-enfeksiyonlari', 'u06': 'k1-58-enurezis-nokturna'},
 'genetik': {'g01': 'k1-01-dismorfolojide-genetik-terminoloji', 'g02': 'k1-10-kromozomal-hastaliklar-ve-genetik-danisma',
   'g03': 'k1-19-dogumsal-kadin-erkek-genital-gelisim-anomalileri', 'g04': 'k1-31-urogenital-sistem-tumorlerinde-genetik-belirtecler',
   'g05': 'k1-35-prenatal-tani-yontemleri', 'g06': 'k1-60-preimplantasyon-genetik-tani-pgt'},
 'halksagligi': {'h01': 'k1-18-halk-sagligi-tarihcesi', 'h02': 'k1-23-ana-cocuk-sagligi-duzeyinin-izlenmesi', 'h03': 'k1-22-bebek-beslenmesi',
   'h04': 'k1-14-salgin-hastaliklarda-kontrol-ve-korunma-yontemleri', 'h05': 'k1-68-enfeksiyon-hastaliklarinin-epidemiyolojisi'},
 'kadindogum': {'k01': 'k1-61-abortus'},
 'farmakoloji': {'f01': 'k1-59-immunofarmakoloji'},
}
brans = sys.argv[1]
W = Path('/home/indu/medsor/meds_temp/spot_cozucu') / brans
(W / 'girdi3').mkdir(exist_ok=True); (W / 'cozucu3').mkdir(exist_ok=True)
for kod, key in CANLI[brans].items():
    S = json.load(open(W / 'cozucu' / f'{kod}.json'))['sorular']
    o = json.load(open(W / 'onem' / f'{kod}.json'))
    yol = M / f'{key}.md'
    hedef = max(8, min(25, round(len(yol.read_text().split()) / 230)))
    json.dump({'kod': kod, 'baslik': o['baslik'], 'canli_metin': [str(yol)], 'yeni_soru_sayisi': hedef,
               'pdf_metin': str(W / 'pdf_metin' / f'{kod}.md'),
               'mevcut': [{'ref': q['ref'], 'tur': q['tur'], 'soru': q['soru'], 'dogru': q['secenekler'][q['dogru']]} for q in S],
               'onem': [{'id': m['id'], 'puan': m['puan'], 'baslik': m['baslik'], 'bilgi': m['bilgi']} for m in o['maddeler']]},
              open(W / 'girdi3' / f'{kod}.json', 'w'), ensure_ascii=False, indent=1)
    print(kod, len(S), hedef)
