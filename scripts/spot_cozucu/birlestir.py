#!/usr/bin/env python3
"""Spot bilgiler + sesli soru çözücü (branş geneli) birleştirici.

Girdi (meds_temp/spot_cozucu/<brans>/): girdi/, cikmis/, onem/<kod>.json (onem_dogrula 0 HATA), cozucu/<kod>.json (cozucu_dogrula 0 HATA),
ses kayıtları meds/data/<brans>_cozucu/ses[_<id>]/<kod>/kayit.json.
Çıktı:
  meds/src/data/<brans>_onem/{index,<kod>}.json   — önem listesi (örnek sorular `ornek26` alanında, zorluklu; çıkmışlar tekrar yıllarıyla)
  meds/src/data/<brans>_cozucu/{index,<set>}.json — çözücü; 40'tan çok sorulu ders ders akışına göre ardışık setlere bölünür
                                                    (set kodu "<kod>-1", ses klasörü `klasor` = ders kodu)
  meds_temp/spot_cozucu/<brans>/cikti_tam/<kod>.json — seslendirme girdisi (ses.py)
Soru numaraları kalıcıdır (numara.json, yalnız eklenir): ilerleme ve klip adları buna bağlı.
Kullanım: python3 meds/scripts/spot_cozucu/birlestir.py <brans> [--taslak]   (--taslak: hatalı dersi atla, durma)
"""
import json, math, os, re, shutil, subprocess, sys
from pathlib import Path

B = Path(__file__).resolve().parent
MEDS = B.parents[1]
DERS_AD = {
    'enfeksiyon': 'Enfeksiyon Hastalıkları', 'uroloji': 'Üroloji',
    'genetik': 'Tıbbi Genetik', 'halksagligi': 'Halk Sağlığı',
    'kadindogum': 'Kadın Hastalıkları ve Doğum', 'farmakoloji': 'Tıbbi Farmakoloji',
}
SES_AD = {'ema': 'EMA'}  # ses.py SESLER ile aynı kimlikler; varsayılan ilk
MAKS_SET = 40


def gecer(betik, f):
    r = subprocess.run([sys.executable, str(B / betik), str(f)], capture_output=True, text=True)
    return r.returncode == 0, r.stdout[-600:]


def main():
    brans = sys.argv[1]
    taslak = '--taslak' in sys.argv
    W = MEDS.parent / 'meds_temp/spot_cozucu' / brans
    OD, CD = MEDS / 'src/data' / f'{brans}_onem', MEDS / 'src/data' / f'{brans}_cozucu'
    SES = MEDS / 'data' / f'{brans}_cozucu'
    (W / 'cikti_tam').mkdir(exist_ok=True)
    nump = W / 'numara.json'
    numara = json.load(open(nump)) if nump.exists() else {}
    G = sorted((json.load(open(p)) for p in (W / 'girdi').glob('*.json')), key=lambda g: g['no'])
    onem_d, cozucu_d, hatali = [], [], []
    for g in G:
        kod = g['kod']
        fo, fc = W / 'onem' / f'{kod}.json', W / 'cozucu' / f'{kod}.json'
        if not fo.exists(): hatali.append(f'{kod}(yok)'); continue
        ok, cikti = gecer('onem_dogrula.py', fo)
        if not ok:
            if taslak: hatali.append(f'{kod}(önem hata)'); continue
            sys.exit(f'{kod}: onem_dogrula HATA — birleştirilmez\n{cikti}')
        o = json.load(open(fo))
        C = {c['id']: c for c in json.load(open(W / 'cikmis' / f'{kod}.json'))} if (W / 'cikmis' / f'{kod}.json').exists() else {}
        # ---- önem listesi
        maddeler, cik = [], {}
        for m in o['maddeler']:
            m = dict(m)
            ornek = m.pop('ornek', None) or []
            m.pop('ornek_soru', None)
            if ornek:
                m['ornek26'] = [{k: q[k] for k in ('kok', 'secenekler', 'dogru', 'aciklama', 'zorluk') if k in q} for q in ornek]
            for i in m.get('cikmis') or []:
                c = C[i]
                cik[i] = {'sinav': c['sinav'], 'kok': c['kok'], 'secenekler': c['secenekler'], 'dogru': c['dogru'],
                          **({'tekrar': [t['sinav'] for t in c['tekrar']]} if c.get('tekrar') else {})}
            maddeler.append(m)
        maddeler.sort(key=lambda m: -m['puan'])
        onem_d.append({'kod': kod, 'no': g['no'], 'baslik': o['baslik'], 'pdf': g['ad'], 'ozet': o['ozet'],
                       'neden_onemli': o['neden_onemli'], 'maddeler': maddeler, 'cikmis': dict(sorted(cik.items()))})
        # ---- çözücü
        if not fc.exists(): hatali.append(f'{kod}(çözücü yok)'); continue
        ok, cikti = gecer('cozucu_dogrula.py', fc)
        if not ok:
            if taslak: hatali.append(f'{kod}(çözücü hata)'); continue
            sys.exit(f'{kod}: cozucu_dogrula HATA — birleştirilmez\n{cikti}')
        S = json.load(open(fc))['sorular']
        f3 = W / 'cozucu3' / f'{kod}.json'  # 3. tur: canlı ders konularından örnek sorular (cozucu_dogrula3.py)
        if f3.exists():
            ok3, c3 = gecer('cozucu_dogrula3.py', f3)
            if not ok3: sys.exit(f'{kod}: cozucu_dogrula3 HATA — birleştirilmez\n{c3}')
            S = S + [dict(q, ref=f'k:{i}', tur='ornek') for i, q in enumerate(json.load(open(f3)).get('yeni') or [], 1)]
        nm = numara.setdefault(kod, {})
        for q in sorted(S, key=lambda q: (q['tur'] != 'ornek', q['ref'])):
            if q['ref'] not in nm: nm[q['ref']] = max(nm.values(), default=0) + 1
        tam = [dict(q, no=nm[q['ref']]) for q in S]
        json.dump({'kod': kod, 'sorular': sorted(tam, key=lambda q: q['no'])}, open(W / 'cikti_tam' / f'{kod}.json', 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
        kayit = {}
        for sid in SES_AD:
            p = SES / ('ses' if sid == 'ema' else f'ses_{sid}') / kod / 'kayit.json'
            kayit[sid] = json.load(open(p)) if p.exists() else {}
        sira = sorted(tam, key=lambda q: (min(q['sayfa']), q['tur'] != 'cikmis', q['no']))
        k = max(1, math.ceil(len(sira) / MAKS_SET))
        boy = math.ceil(len(sira) / k)
        for si in range(k):
            parca = sira[si * boy:(si + 1) * boy]
            skod = kod if k == 1 else f'{kod}-{si + 1}'
            sorular, gerek = [], []
            for q in parca:
                no = q['no']
                gerek += [f'q-{no}', f'i-{no}', f'c-{no}', f'd-{no}'] + [f's-{no}-{h}' for h in 'ABCDE']
                sorular.append({'no': no, 'tur': q['tur'], **({'sinav': q['sinav']} if q.get('sinav') else {}),
                                **({'zorluk': q['zorluk']} if q.get('zorluk') else {}),
                                'soru': q['soru'], 'secenekler': q['secenekler'], 'dogru': q['dogru'],
                                'ipucu': q['ipucu']['metin'], 'siklar': {h: q['siklar'][h]['metin'] for h in 'ABCDE'},
                                'cozum': q['cozum']['metin'], 'sayfa': q['sayfa']})
            klipler = {sid: {x: {'v': kay[x]['h'], 'sure': kay[x]['sure'], 'zaman': kay[x]['zaman']} for x in gerek if x in kay}
                       for sid, kay in kayit.items()}
            v = next(iter(SES_AD))
            d = {'kod': skod, 'no': g['no'], 'baslik': o['baslik'], 'klasor': kod, **({'set': si + 1, 'setSay': k} if k > 1 else {}),
                 'sorular': sorular, 'klip': klipler[v]}
            diger = {sid: kl for sid, kl in klipler.items() if sid != v and kl}
            if diger: d['klipSes'] = diger
            sayfalar = [x for q in parca for x in q['sayfa']]
            cozucu_d.append((d, {'kod': skod, 'no': g['no'], 'baslik': o['baslik'], 'soru': len(sorular),
                                 'ornek': sum(q['tur'] == 'ornek' for q in sorular), 'cikmis': sum(q['tur'] == 'cikmis' for q in sorular),
                                 'ses': len(klipler[v]) == len(gerek), **({'set': si + 1, 'setSay': k} if k > 1 else {}),
                                 'sayfa': [min(sayfalar), max(sayfalar)]}))
    json.dump(numara, open(nump, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    # ---- yaz (önce tümü hazır; sonra klasörler yenilenir)
    if OD.exists(): shutil.rmtree(OD)
    OD.mkdir(parents=True)
    for d in onem_d:
        json.dump(d, open(OD / f"{d['kod']}.json", 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    json.dump({'surum': f'{brans}-onem-v1', 'kaynak': f"Kurul 1 {DERS_AD.get(brans, brans)} ders PDF'leri (2026-27 Drive)",
               'dersler': [{'kod': d['kod'], 'no': d['no'], 'baslik': d['baslik'], 'madde': len(d['maddeler']),
                            'bant': {str(b): sum(1 for m in d['maddeler'] if min(max(m['puan'] // 10, 4), 9) == b) for b in range(4, 10)}}
                           for d in onem_d]}, open(OD / 'index.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    if CD.exists(): shutil.rmtree(CD)
    CD.mkdir(parents=True)
    for d, _ in cozucu_d:
        json.dump(d, open(CD / f"{d['kod']}.json", 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    ortak = {}
    for sid in SES_AD:
        p = SES / ('ses' if sid == 'ema' else f'ses_{sid}') / 'ortak' / 'kayit.json'
        if p.exists(): ortak[sid] = {k: {'v': v['h'], 'sure': v['sure']} for k, v in json.load(open(p)).items()}
    v = next(iter(SES_AD))
    sesler = [{'id': sid, 'ad': SES_AD[sid], **({'varsayilan': True} if sid == v else {})} for sid in SES_AD if sid == v or ortak.get(sid)]
    json.dump({'surum': f'{brans}-cozucu-v1', 'ses': SES_AD[v], 'sesler': sesler, 'ortak': ortak.get(v, {}),
               **({'ortakSes': {s: o for s, o in ortak.items() if s != v}} if len(ortak) > 1 else {}),
               'dersler': [x for _, x in cozucu_d]}, open(CD / 'index.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    D = [x for _, x in cozucu_d]
    print(f'{brans}: önem {len(onem_d)} ders · {sum(len(d["maddeler"]) for d in onem_d)} madde | çözücü {len(D)} set · '
          f'{sum(x["soru"] for x in D)} soru (örnek {sum(x["ornek"] for x in D)} · çıkmış {sum(x["cikmis"] for x in D)}) · '
          f'sesli {sum(x["ses"] for x in D)}/{len(D)} | atlanan {hatali}')


if __name__ == '__main__':
    main()
