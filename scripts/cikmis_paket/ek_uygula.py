#!/usr/bin/env python3
"""Çıkmış çözücü ek modülü: çözücüde olmayan, denetlenmiş Kurul 1 çıkmışlarını yayına ve EMA sesine alır.

Girdi : meds_temp/cikmis_paket/ek/cikti*.json (yazar + bağımsız denetçi, ek_dogrula.py 0 HATA); yalnız "durum": "ekle".
Çıktı : src/data/cikmis_paket/ek/<brans>/<klasör>.json — çözücü ders biçimi (sorular no ≥ 1001, kendi klipleri; kısa not
        soruda `notYazili`). Numara defteri scripts/cikmis_paket/ek_numara.json (veritabanı id → no, kalıcı).
Ses   : meds/data/<brans>_cozucu/ses/<klasör>/{q,i,c,d}-<no>, s-<no>-<H>, n-<no> (çözücü klasörü; ses.py ≥1001 ve n-* silmez).
Sonra paketle.py paketleri yeniden kurar. Kullanım: bash meds/scripts/cikmis_paket/ek_uygula.sh  [--kuru: ses yok]
"""
import glob, json, re, sys
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
T = MEDS.parent / 'meds_temp'
KURU = '--kuru' in sys.argv
NP = Path(__file__).parent / 'ek_numara.json'
numara = json.loads(NP.read_text()) if NP.exists() else {}

girdi, cikti = {}, {}
for f in sorted(glob.glob(str(T / 'cikmis_paket/ek/parti*.json'))):
    girdi.update({q['id']: q for q in json.load(open(f))})
for f in sorted(glob.glob(str(T / 'cikmis_paket/ek/cikti*.json'))):
    cikti.update({k: v for k, v in json.load(open(f)).items() if v.get('durum') == 'ekle'})
dersler = json.load(open(T / 'cikmis_paket/ek/dersler.json'))

# partiler arası tekrar: aynı kök (ilk 90 harf) + aynı doğru cevap metni bir kez alınır
_n = lambda t: re.sub(r'\W+', '', (t or '').lower())
_gor, _tekrar = set(), 0
for k in sorted(cikti):
    o, q = cikti[k], girdi[k]
    an = (_n(o['soru']['metin'])[:90], _n((q['secenekler'] or {}).get(o.get('dogru') or q['dogru'])))
    if an in _gor:
        del cikti[k]; _tekrar += 1
    else:
        _gor.add(an)
print('partiler arası tekrar atlandı:', _tekrar)

gruplar = {}
for k, o in cikti.items():
    q = girdi[k]
    gruplar.setdefault((o.get('brans') or q['brans'], o['ders']), []).append((k, q, o))

if not KURU:
    sys.path.insert(0, str(MEDS / 'scripts/spot_cozucu'))
    import ses as SES
    S = SES.SESLER['ema']['sinif']()

for (b, kl), l in sorted(gruplar.items()):
    l.sort(key=lambda x: x[0])
    # numara defteri: anahtar "<brans>/<klasör>/<db id>" → no
    sorular, K = [], {}
    ders = next(d for d in dersler[b] if d['klasor'] == kl)
    for k, q, o in l:
        an = f'{b}/{kl}/{k}'
        if an not in numara:
            numara[an] = 1001 + sum(1 for v in numara if v.startswith(f'{b}/{kl}/'))
        no = numara[an]
        sk = o['siklar']
        sorular.append({
            'no': no, 'tur': 'cikmis', **({'sinav': f"{q['sinav']} Kurul 1"} if q.get('sinav') else {}), 'dbId': k,
            'soru': o['soru']['metin'], 'secenekler': q['secenekler'], 'dogru': o.get('dogru') or q['dogru'],
            'ipucu': o['ipucu']['metin'], 'siklar': {h: sk[h]['metin'] for h in 'ABCDE'}, 'cozum': o['cozum']['metin'],
            'sayfa': o['sayfa'],
            'notYazili': {'baslik': o['not']['baslik'], 'cumleler': [c['metin'] for c in o['not']['cumleler']], 'sayfa': o['sayfa']},
        })
        if not KURU:
            tum = [o['soru']['metin'], *q['secenekler'].values(), o['ipucu']['metin'], o['cozum']['metin'], *(v['metin'] for v in sk.values())]
            ekk = SES.kisaltmalar(*tum)
            cz = SES.cumlele(o['cozum']['ses'])
            d = o.get('dogru') or q['dogru']
            tanim = {f'q-{no}': [SES.nokta(o['soru']['ses'])] + [f"{SES.HARF_AD[h]}, {SES.nokta(o['secenek_ses'][h])}" for h in 'ABCDE'],
                     f'i-{no}': SES.cumlele(o['ipucu']['ses']),
                     f'c-{no}': [f"Doğru cevap {SES.HARF_AD[d]}, {SES.nokta(o['secenek_ses'][d])}"] + cz,
                     f'd-{no}': ['Doğru!'] + cz,
                     f'n-{no}': [SES.nokta(c['ses']) for c in o['not']['cumleler']]}
            for h in 'ABCDE':
                tanim[f's-{no}-{h}'] = SES.cumlele(sk[h]['ses'])
            for ad, cl in tanim.items():
                K[ad] = [S.ses_metni(c, ekk) for c in cl]
    klip = {}
    if not KURU:
        kok = SES.ses_klasoru(b, 'ema')
        SES.klasor(S, kok, kl, K, SES.SESLER['ema']['kbps'], silinsin=False)
        kay = json.loads((kok / kl / 'kayit.json').read_text())
        klip = {ad: {'v': kay[ad]['h'], 'sure': kay[ad]['sure'], 'zaman': kay[ad]['zaman']} for ad in K if ad in kay}
    out = MEDS / 'src/data/cikmis_paket/ek' / b / f'{kl}.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    eski = json.loads(out.read_text()) if out.exists() else {}
    if KURU:
        klip = eski.get('klip', {})
    out.write_text(json.dumps({'kod': kl, 'no': ders['no'], 'baslik': ders['baslik'], 'klasor': kl,
                               'sorular': sorular, 'klip': klip}, ensure_ascii=False, separators=(',', ':')))
    print(b, kl, len(sorular), 'soru', '' if KURU else f'{len(klip)} klip', flush=True)

NP.write_text(json.dumps(numara, ensure_ascii=False, indent=1, sort_keys=True))
print('bitti')
