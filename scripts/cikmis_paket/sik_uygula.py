#!/usr/bin/env python3
"""Denetlenmiş çıkmış şık açıklamalarını uygular (meds_temp/cikmis_paket/sik/cikti*.json, sik_dogrula.py 0 HATA):

1. Hat kaynağı (seslendirme girdisi) güncellenir: patoloji meds_temp/patoloji_ornek26/cozucu/cikti_tam/<klasör>.json,
   diğerleri meds_temp/spot_cozucu/<brans>/cikti_tam/<klasör>.json — sonraki tam üretim düzeltmeyi geri almaz.
2. Yalnız değişen klipler EMA ile seslendirilir (s-n-H; ipucu değiştiyse i-n; çözüm değiştiyse c-n, d-n), silme yok.
3. Yayın dosyası src/data/<brans>_cozucu/<kod>.json metni + klip özetleri yazılır (birlestir.py K1'de K2 kapısına takıldığı için).

Kullanım (EMA venv, CPU tavanlı): bash meds/scripts/cikmis_paket/sik_uygula.sh  [--kuru: yalnız metin, ses yok]
"""
import glob, json, sys
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
T = MEDS.parent / 'meds_temp'
KURU = '--kuru' in sys.argv

cikti = {}
for f in sorted(glob.glob(str(T / 'cikmis_paket/sik/cikti*.json'))):
    cikti.update(json.load(open(f)))
cikti = {k: v for k, v in cikti.items() if not v.get('sorun')}
print(len(cikti), 'soru uygulanacak')

if not KURU:
    sys.path.insert(0, str(MEDS / 'scripts/spot_cozucu'))
    import ses as SES
    S = SES.SESLER['ema']['sinif']()


def tam_yol(b, kl):
    return T / ('patoloji_ornek26/cozucu/cikti_tam' if b == 'patoloji' else f'spot_cozucu/{b}/cikti_tam') / f'{kl}.json'


gruplar = {}
for key, o in cikti.items():
    b, kod, no = key.split('/')
    gruplar.setdefault((b, kod), {})[int(no)] = o

tamlar, klipler = {}, {}
for (b, kod), sorular in sorted(gruplar.items()):
    yp = MEDS / 'src/data' / f'{b}_cozucu' / f'{kod}.json'
    yay = json.loads(yp.read_text())
    kl = yay.get('klasor') or kod
    tp = tam_yol(b, kl)
    tam = tamlar.setdefault(tp, json.loads(tp.read_text()))
    for no, o in sorular.items():
        tq = next(x for x in tam['sorular'] if x['no'] == no)
        yq = next(x for x in yay['sorular'] if x['no'] == no)
        degisen = []
        for h, v in o['siklar'].items():
            tq['siklar'][h] = v; yq['siklar'][h] = v['metin']; degisen.append(f's-{no}-{h}')
        if o.get('ipucu'):
            tq['ipucu'] = o['ipucu']; yq['ipucu'] = o['ipucu']['metin']; degisen.append(f'i-{no}')
        if o.get('cozum'):
            tq['cozum'] = o['cozum']; yq['cozum'] = o['cozum']['metin']; degisen += [f'c-{no}', f'd-{no}']
        if KURU:
            continue
        ekk = SES.kisaltmalar(tq['soru'], *tq['secenekler'].values(), tq['ipucu']['metin'], tq['cozum']['metin'],
                              *(v['metin'] for v in tq['siklar'].values()))
        cz = SES.cumlele(tq['cozum']['ses'])
        d = tq['dogru']
        tanim = {f's-{no}-{h}': SES.cumlele(tq['siklar'][h]['ses']) for h in 'ABCDE'}
        tanim[f'i-{no}'] = SES.cumlele(tq['ipucu']['ses'])
        tanim[f'c-{no}'] = [f"Doğru cevap {SES.HARF_AD[d]}, {SES.nokta(tq['secenek_ses'][d])}"] + cz
        tanim[f'd-{no}'] = ['Doğru!'] + cz
        K = klipler.setdefault((b, kl), {})
        for ad in degisen:
            K[ad] = [S.ses_metni(c, ekk) for c in tanim[ad]]
    if KURU:
        yp.write_text(json.dumps(yay, ensure_ascii=False, separators=(',', ':')))
for tp, tam in tamlar.items():
    tp.write_text(json.dumps(tam, ensure_ascii=False, indent=1))

if not KURU:
    for (b, kl), K in sorted(klipler.items()):
        SES.klasor(S, SES.ses_klasoru(b, 'ema'), kl, K, SES.SESLER['ema']['kbps'], silinsin=False)
    # yayın dosyalarına metin + yeni klip özetleri
    for (b, kod), sorular in sorted(gruplar.items()):
        yp = MEDS / 'src/data' / f'{b}_cozucu' / f'{kod}.json'
        yay = json.loads(yp.read_text())
        kl = yay.get('klasor') or kod
        tam = tamlar[tam_yol(b, kl)]
        kay = json.loads((SES.ses_klasoru(b, 'ema') / kl / 'kayit.json').read_text())
        for no in sorular:
            tq = next(x for x in tam['sorular'] if x['no'] == no)
            yq = next(x for x in yay['sorular'] if x['no'] == no)
            yq['siklar'] = {h: v['metin'] for h, v in tq['siklar'].items()}
            yq['ipucu'] = tq['ipucu']['metin']; yq['cozum'] = tq['cozum']['metin']
            for ad in [f's-{no}-{h}' for h in 'ABCDE'] + [f'i-{no}', f'c-{no}', f'd-{no}']:
                if ad in kay and ad in yay['klip']:
                    yay['klip'][ad] = {'v': kay[ad]['h'], 'sure': kay[ad]['sure'], 'zaman': kay[ad]['zaman']}
        yp.write_text(json.dumps(yay, ensure_ascii=False, separators=(',', ':')))
print('bitti')
