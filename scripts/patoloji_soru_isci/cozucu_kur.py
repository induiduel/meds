#!/usr/bin/env python3
"""Hoca üslubu soruların SESLİ ÇÖZÜCÜ hattı (branş k2patolojihoca; ders kodu 2h01, 2h02 …).

  python3 scripts/patoloji_soru_isci/cozucu_kur.py iskele <ders-id>     # k2-03 → çalışma klasörü + yazar iskeleti
  python3 scripts/patoloji_soru_isci/cozucu_kur.py dogrula <ders-id>    # spot_cozucu/cozucu_dogrula.py (0 HATA şart)
  python3 scripts/patoloji_soru_isci/cozucu_kur.py birlestir            # cikti_tam + src/data/k2patolojihoca_cozucu (ses varsa klipler)
  (ses)  bash meds/scripts/patoloji_cozucu/cozucu_ses_gpu.sh meds/scripts/spot_cozucu/ses.py --brans k2patolojihoca 2h01 2h02   # EMA, GPU (AGENTS.md kural 10)

Çalışma klasörü meds_temp/spot_cozucu/k2patolojihoca/ (onem/, cozucu/, pdf_metin/); format TALIMAT_COZUCU.md ile aynıdır.
Kaynak: src/data/hoca_uslubu_sorular/k2/<ders>.json + ders dökümü meds_temp/patoloji_analiz/k2/<ders-id>.txt.
"""
from __future__ import annotations
import json, math, re, sys
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
BRANS = 'k2patolojihoca'
W = MEDS.parent / 'meds_temp/spot_cozucu' / BRANS
KODLAR = {'k2-03': '2h01', 'k2-04': '2h02'}   # yeni derste buraya eklenir (kod: <kurul><h><sıra>)
KAYNAK = MEDS / 'src/data/hoca_uslubu_sorular/k2'
DOKUM = MEDS.parent / 'meds_temp/patoloji_analiz/k2'


def kaynak(ders):
    f = next(KAYNAK.glob(f'{ders}-*.json'))
    return json.load(open(f, encoding='utf-8'))


def iskele(ders):
    kod = KODLAR[ders]; d = kaynak(ders)
    for k in ('pdf_metin', 'onem', 'cozucu'): (W / k).mkdir(parents=True, exist_ok=True)
    # pdf_metin: biçim işaretlerinden arındırılmış sayfa metni (=== SAYFA n ===)
    ham = (DOKUM / f'{ders}.txt').read_text(encoding='utf-8')
    ham = re.sub(r'=== SAYFA (\d+) \(g\d+\) ===', r'=== SAYFA \1 ===', ham)
    ham = re.sub(r'[⟦⟧‹›]', '', ham); ham = re.sub(r'^(Y\|)?(# )?', '', ham, flags=re.M)
    (W / 'pdf_metin' / f'{kod}.md').write_text(ham, encoding='utf-8')
    per, maddeler, sor = {}, {}, []
    for q in d['sorular']: per.setdefault(q['onem_id'], []).append(q)
    vurgu = {v['id']: v for v in d.get('vurgu', [])}
    for oid, qs in per.items():
        ornek = [{'kok': q['kok'], 'secenekler': {h: q['siklar'][i] for i, h in enumerate('ABCDE')}, 'dogru': q['cevap'], 'zorluk': 'zor'} for q in qs]
        maddeler[oid] = {'id': oid, 'puan': int((vurgu.get(oid) or {}).get('puan', 70)), 'baslik': (vurgu.get(oid) or {}).get('baslik', oid), 'ornek': ornek, 'cikmis': []}
        for i, q in enumerate(qs, 1):
            sor.append({'ref': f'o:{oid}:{i}', 'tur': 'ornek', 'onem_id': oid, 'zorluk': 'zor', 'kontrol': {'durum': 'tamam'},
                        'soru': q['kok'], 'secenekler': {h: q['siklar'][j] for j, h in enumerate('ABCDE')}, 'dogru': q['cevap'],
                        'sayfa': sorted({q['kaynak']['sayfa']}), 'taslak_aciklama': q['aciklama']})
    (W / 'onem' / f'{kod}.json').write_text(json.dumps({'kod': kod, 'baslik': d['konu'], 'ozet': d['konu'], 'neden_onemli': d['konu'],
                                                       'maddeler': list(maddeler.values())}, ensure_ascii=False, indent=1), encoding='utf-8')
    (W / 'cozucu' / f'{kod}_iskelet.json').write_text(json.dumps({'kod': kod, 'sorular': sor}, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'{ders} → {kod}: {len(sor)} soru iskeleti, {len(maddeler)} önem noktası → {W}')


def dogrula(ders):
    import subprocess
    kod = KODLAR[ders]
    r = subprocess.run([sys.executable, str(MEDS / 'scripts/spot_cozucu/cozucu_dogrula.py'), str(W / 'cozucu' / f'{kod}.json')])
    return r.returncode


def birlestir():
    """cikti_tam (ses.py girdisi) + src/data/k2patolojihoca_cozucu/{index,<kod>}.json (birlestir.py'nin çözücü bölümüyle aynı biçim)."""
    (W / 'cikti_tam').mkdir(exist_ok=True)
    CD = MEDS / 'src/data' / f'{BRANS}_cozucu'; SES = MEDS / 'data' / f'{BRANS}_cozucu'
    CD.mkdir(parents=True, exist_ok=True)
    nump = W / 'numara.json'; numara = json.load(open(nump)) if nump.exists() else {}
    dersler = []
    for ders, kod in KODLAR.items():
        fc = W / 'cozucu' / f'{kod}.json'
        if not fc.exists(): continue
        S = json.load(open(fc, encoding='utf-8'))['sorular']
        nm = numara.setdefault(kod, {})
        for q in S:
            if q['ref'] not in nm: nm[q['ref']] = max(nm.values(), default=0) + 1
        tam = sorted((dict(q, no=nm[q['ref']]) for q in S), key=lambda q: q['no'])
        json.dump({'kod': kod, 'sorular': tam}, open(W / 'cikti_tam' / f'{kod}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        p = SES / 'ses' / kod / 'kayit.json'; kay = json.load(open(p)) if p.exists() else {}
        gerek, sorular = [], []
        for q in tam:
            no = q['no']; gerek += [f'q-{no}', f'i-{no}', f'c-{no}', f'd-{no}'] + [f's-{no}-{h}' for h in 'ABCDE']
            sorular.append({'no': no, 'tur': q['tur'], 'zorluk': q.get('zorluk', 'zor'), 'soru': q['soru'], 'secenekler': q['secenekler'], 'dogru': q['dogru'],
                            'ipucu': q['ipucu']['metin'], 'siklar': {h: q['siklar'][h]['metin'] for h in 'ABCDE'}, 'cozum': q['cozum']['metin'], 'sayfa': q['sayfa']})
        klip = {x: {'v': kay[x]['h'], 'sure': kay[x]['sure'], 'zaman': kay[x]['zaman']} for x in gerek if x in kay}
        baslik = json.load(open(W / 'onem' / f'{kod}.json'))['baslik']
        json.dump({'kod': kod, 'no': int(ders.split('-')[1]), 'baslik': baslik, 'klasor': kod, 'sorular': sorular, 'klip': klip},
                  open(CD / f'{kod}.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
        sy = [x for q in tam for x in q['sayfa']]
        dersler.append({'kod': kod, 'no': int(ders.split('-')[1]), 'baslik': baslik, 'soru': len(sorular), 'ornek': len(sorular), 'cikmis': 0,
                        'ses': len(klip) == len(gerek), 'sayfa': [min(sy), max(sy)]})
    json.dump(numara, open(nump, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    ortak = {}; p = SES / 'ses' / 'ortak' / 'kayit.json'
    if p.exists(): ortak = {k: {'v': v['h'], 'sure': v['sure']} for k, v in json.load(open(p)).items()}
    json.dump({'surum': f'{BRANS}-cozucu-v1', 'ses': 'EMA', 'sesler': [{'id': 'ema', 'ad': 'EMA', 'varsayilan': True}], 'ortak': ortak, 'dersler': dersler},
              open(CD / 'index.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{BRANS}: {len(dersler)} ders · {sum(x["soru"] for x in dersler)} soru · sesli {sum(x["ses"] for x in dersler)}/{len(dersler)}')


if __name__ == '__main__':
    kom = sys.argv[1] if len(sys.argv) > 1 else ''
    if kom == 'iskele': iskele(sys.argv[2])
    elif kom == 'dogrula': sys.exit(dogrula(sys.argv[2]))
    elif kom == 'birlestir': birlestir()
    else: print(__doc__)
