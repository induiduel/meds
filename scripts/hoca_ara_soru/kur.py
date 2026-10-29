#!/usr/bin/env python3
"""Sesli ders ARA SORU hattı — hocanın sorabileceği sorular (kullanıcı kararı 2026-10-29; AGENTS.md kural 27).

Hoca üslubuna göre soru çıkabilecek bir slayttan hemen sonra derste yapay bir soru sayfası açılır; EMA soruyu okur, çözer ve
çözümü önceki slaytlara dayanarak anlatır (`a-N` klibi). Aynı sorular ders dışında sesli çözücüde (branş k<N>hocaara) çözülür.

  python3 meds/scripts/hoca_ara_soru/kur.py iskele <ders-key>         # kaynak/<kod>.json → onem + cozucu iskeleti
  python3 meds/scripts/hoca_ara_soru/kur.py dogrula <ders-key> [--ses] # çözücü kapısı + ara kapıları (0 HATA şart; --ses klipleri de)
  python3 meds/scripts/hoca_ara_soru/kur.py birlestir [<kurul>]        # cikti_tam + src/data/k<N>hocaara_cozucu/{index,<kod>}.json
  (ses)  bash meds/scripts/patoloji_cozucu/cozucu_ses_gpu.sh meds/scripts/spot_cozucu/ses.py --brans k2hocaara 2a07   # EMA, GPU

<ders-key> sesli ders anahtarıdır (k2-07-genel-anestezik-ilaclar); branş k<kurul>hocaara, kod <kurul>a<sıra> (k2-07 → 2a07).
Çalışma klasörü meds_temp/spot_cozucu/k<N>hocaara/ (kaynak/, onem/, cozucu/, cikti_tam/). Yazım kuralları: TALIMAT.md.
"""
from __future__ import annotations
import json, re, subprocess, sys
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MEDS / 'scripts'))
HIZ = MEDS / 'data/sesli_anlatim/hizalama'
kelime = lambda s: len(re.findall(r'\w+', str(s or '')))  # noqa: E731
cumleler = lambda s: [c for c in re.split(r'(?<=[.!?])(?<!\d\.)\s+', str(s or '').strip()) if c.strip()]  # noqa: E731
GEREK_KLIP = lambda n: [f'q-{n}', f'i-{n}', f'c-{n}', f'd-{n}', f'a-{n}'] + [f's-{n}-{h}' for h in 'ABCDE']  # noqa: E731


def kimlik(key: str):
    m = re.match(r'^k([2-6])-(\d{2})', key)
    if not m: sys.exit(f'ders anahtarı k<N>-<sıra>-… olmalı: {key}')
    brans = f'k{m[1]}hocaara'
    return brans, f'{m[1]}a{m[2]}', MEDS.parent / 'meds_temp/spot_cozucu' / brans


def hizalama(key: str) -> dict:
    p = HIZ / f'{key}.json'
    if not p.exists(): sys.exit(f'hizalama yok: {p} (önce ders-ekle + hizalama)')
    return json.load(open(p, encoding='utf-8'))


def son_paragraf(hz: dict, dosya: int, sayfa: int):
    """(dosya, sayfa) slaytına eşlenen SON paragrafın dizini — soru bu paragraf bitince açılır."""
    son = None
    for i, e in enumerate(hz.get('paragraflar') or []):
        if e and (e.get('dosya') or 0) == dosya and sayfa in [e.get('sayfa'), *(e.get('sayfalar') or [])]: son = i
    return son


def iskele(key):
    brans, kod, W = kimlik(key)
    k = json.load(open(W / 'kaynak' / f'{kod}.json', encoding='utf-8'))
    for d in ('onem', 'cozucu'): (W / d).mkdir(parents=True, exist_ok=True)
    maddeler, sor = [], []
    for i, q in enumerate(k['sorular'], 1):
        mid = f'{kod}-a{i:02d}'
        maddeler.append({'id': mid, 'puan': 80, 'baslik': q.get('baslik') or q['gerekce'][:80],
                         'ornek': [{'kok': q['kok'], 'secenekler': q['secenekler'], 'dogru': q['dogru'], 'zorluk': q.get('zorluk', 'orta')}], 'cikmis': []})
        sor.append({'ref': f'o:{mid}:1', 'tur': 'ornek', 'onem_id': mid, 'zorluk': q.get('zorluk', 'orta'), 'kontrol': {'durum': 'tamam'},
                    'soru': q['kok'], 'secenekler': q['secenekler'], 'dogru': q['dogru'], 'sayfa': sorted(set(q['dayanak'])),
                    'ara': q['ara'], 'gerekce': q['gerekce'], 'kanit': q['kanit'],
                    'kok_ses': '', 'secenek_ses': {}, 'ipucu': {'metin': '', 'ses': ''}, 'siklar': {}, 'cozum': {'metin': '', 'ses': ''},
                    'anlatim': {'metin': '', 'ses': ''}})
    json.dump({'kod': kod, 'key': key, 'baslik': k['baslik'], 'ozet': k['baslik'], 'neden_onemli': 'hocanın sorabileceği yerler',
               'maddeler': maddeler}, open(W / 'onem' / f'{kod}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump({'kod': kod, 'sorular': sor}, open(W / 'cozucu' / f'{kod}_iskelet.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{key} → {brans}/{kod}: {len(sor)} ara soru iskeleti → {W / "cozucu"}')


def ara_denetle(key, S, kaynak, ses_kayit=None):
    """Ara soruya özgü kapılar. Hata listesi döndürür."""
    from sik_aciklama import denetle as sik_den
    from turkce_uslup import denetle as uslup_den
    hz = hizalama(key)
    e, slayt = [], {}
    for q in S:
        y = q.get('ref', '?')
        a = q.get('ara') or {}
        ds, sy = a.get('dosya', 0), a.get('sayfa')
        if not isinstance(sy, int) or sy < 1: e.append(f'{y}: ara.sayfa yok'); continue
        if son_paragraf(hz, ds, sy) is None: e.append(f'{y}: ara slaytı ({ds}/{sy}) sesli derste hiçbir paragrafa eşlenmemiş')
        slayt[(ds, sy)] = slayt.get((ds, sy), 0) + 1
        day = q.get('sayfa') or []
        if not day: e.append(f'{y}: dayanak sayfası yok')
        # Sıfır ileriye sızıntı (kural 7): soru yalnız o slayta kadar anlatılanla kurulur
        if any(p > sy for p in day): e.append(f'{y}: dayanak {day} ara slaytından ({sy}) ileride — ileriye sızıntı')
        if sy not in day: e.append(f'{y}: ara slaytı {sy} dayanakta yok')
        if kaynak:
            for p in day:
                if not (kaynak.get(str(p)) or '').strip(): e.append(f'{y}: dayanak sayfa {p} metni kaynak dökümünde yok')
        if q.get('kanit') not in ('profil', 'cikmis'): e.append(f'{y}: kanit "profil" ya da "cikmis" olmalı (kanıtsız önem damgası yasak)')
        if kelime(q.get('gerekce')) < 8: e.append(f'{y}: gerekce (neden hoca sorar) en az 8 kelime')
        an = (q.get('anlatim') or {}).get('metin', '')
        if not 3 <= len(cumleler(an)) <= 6 or not 35 <= kelime(an) <= 130:
            e.append(f'{y}: anlatim 3–6 cümle, 35–130 kelime olmalı ({len(cumleler(an))} cümle, {kelime(an)} kelime)')
        if not (q.get('anlatim') or {}).get('ses', '').strip(): e.append(f'{y}: anlatim.ses boş')
        atif = {int(x) for x in re.findall(r'(\d+)\.\s*(?:slayt|sayfa)', an)}
        if not atif: e.append(f'{y}: anlatim önceki slaytlara numarayla dayanmalı ("4. slaytta gördüğümüz gibi …")')
        elif not atif <= set(day): e.append(f'{y}: anlatim {sorted(atif - set(day))}. slayta atıf yapıyor, dayanakta yok')
        e += [f'{y}: {x}' for x in uslup_den(an, 'anlatim')]
        for h, v in (q.get('siklar') or {}).items():
            e += [f'{y}: {x}' for x in sik_den(v.get('metin', ''), f'şık {h}')]
        if ses_kayit is not None:
            eks = [k for k in GEREK_KLIP(q['no']) if k not in ses_kayit]
            if eks: e.append(f'{y}: ses klibi eksik {eks}')
    e += [f'slayt {k}: {n} soru (en çok 2)' for k, n in slayt.items() if n > 2]
    return e


def dogrula(key, ses=False):
    brans, kod, W = kimlik(key)
    f = W / 'cozucu' / f'{kod}.json'
    r = subprocess.run([sys.executable, str(MEDS / 'scripts/spot_cozucu/cozucu_dogrula.py'), str(f)])
    S = json.load(open(f, encoding='utf-8'))['sorular']
    k = json.load(open(W / 'kaynak' / f'{kod}.json', encoding='utf-8'))
    kayit = None
    if ses:
        tam = {q['ref']: q['no'] for q in json.load(open(W / 'cikti_tam' / f'{kod}.json'))['sorular']}
        for q in S: q['no'] = tam.get(q['ref'], -1)
        p = MEDS / 'data' / f'{brans}_cozucu' / 'ses' / kod / 'kayit.json'
        kayit = json.load(open(p)) if p.exists() else {}
    e = ara_denetle(key, S, k.get('sayfa_metin'), kayit)
    # Hoca profili (kural 26): set düzeyinde üslup sapması
    tmp = W / 'cozucu' / f'{kod}_profil.json'
    json.dump([{'soru': q['soru'], 'secenekler': q['secenekler'], 'dogru': q['dogru']} for q in S], open(tmp, 'w', encoding='utf-8'), ensure_ascii=False)
    rp = subprocess.run([sys.executable, str(MEDS / 'scripts/hoca_profili/profil_kapisi.py'), str(tmp), '--ders', k['ders_adi']])
    for x in e: print('HATA', x)
    print(f'ara kapıları: {len(e)} HATA · çözücü kapısı çıkış {r.returncode} · profil kapısı çıkış {rp.returncode}')
    return 1 if (e or r.returncode or rp.returncode) else 0


def birlestir(kurul='2'):
    brans = f'k{kurul}hocaara'
    W = MEDS.parent / 'meds_temp/spot_cozucu' / brans
    (W / 'cikti_tam').mkdir(parents=True, exist_ok=True)
    CD = MEDS / 'src/data' / f'{brans}_cozucu'; SES = MEDS / 'data' / f'{brans}_cozucu'
    CD.mkdir(parents=True, exist_ok=True)
    dersler = []
    for fo in sorted((W / 'onem').glob('*.json')):
        o = json.load(open(fo, encoding='utf-8')); kod, key = o['kod'], o['key']
        fc = W / 'cozucu' / f'{kod}.json'
        if not fc.exists(): continue
        hz = hizalama(key)
        # numara: ara slaytı sırasına göre (ders akışıyla aynı); klip adları no'ya bağlı
        S = sorted(json.load(open(fc, encoding='utf-8'))['sorular'], key=lambda q: (q['ara'].get('dosya', 0), q['ara']['sayfa'], q['ref']))
        tam = [dict(q, no=i) for i, q in enumerate(S, 1)]
        json.dump({'kod': kod, 'sorular': tam}, open(W / 'cikti_tam' / f'{kod}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        p = SES / 'ses' / kod / 'kayit.json'; kay = json.load(open(p)) if p.exists() else {}
        gerek, sorular = [], []
        for q in tam:
            no = q['no']; gerek += GEREK_KLIP(no)
            ds, sy = q['ara'].get('dosya', 0), q['ara']['sayfa']
            sorular.append({'no': no, 'tur': 'ornek', 'zorluk': q.get('zorluk', 'orta'), 'soru': q['soru'], 'secenekler': q['secenekler'], 'dogru': q['dogru'],
                            'ipucu': q['ipucu']['metin'], 'siklar': {h: q['siklar'][h]['metin'] for h in 'ABCDE'}, 'cozum': q['cozum']['metin'],
                            'sayfa': q['sayfa'], 'ara': {'dosya': ds, 'sayfa': sy, 'paragraf': son_paragraf(hz, ds, sy)}, 'anlatim': q['anlatim']['metin']})
        klip = {x: {'v': kay[x]['h'], 'sure': kay[x]['sure'], 'zaman': kay[x]['zaman']} for x in gerek if x in kay}
        no = int(re.match(r'k\d-(\d+)', key)[1])
        json.dump({'kod': kod, 'key': key, 'no': no, 'baslik': o['baslik'], 'klasor': kod, 'sorular': sorular, 'klip': klip},
                  open(CD / f'{kod}.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
        sy = [x for q in tam for x in q['sayfa']]
        dersler.append({'kod': kod, 'key': key, 'no': no, 'baslik': o['baslik'], 'soru': len(sorular), 'ornek': len(sorular), 'cikmis': 0,
                        'ses': len(klip) == len(gerek), 'sayfa': [min(sy), max(sy)]})
    ortak = {}; p = SES / 'ses' / 'ortak' / 'kayit.json'
    if p.exists(): ortak = {k: {'v': v['h'], 'sure': v['sure']} for k, v in json.load(open(p)).items()}
    json.dump({'surum': f'{brans}-v1', 'ses': 'EMA', 'sesler': [{'id': 'ema', 'ad': 'EMA', 'varsayilan': True}], 'ortak': ortak, 'dersler': dersler},
              open(CD / 'index.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{brans}: {len(dersler)} ders · {sum(x["soru"] for x in dersler)} ara soru · sesli {sum(x["ses"] for x in dersler)}/{len(dersler)}')
    return 0 if all(x['ses'] for x in dersler) else 2


if __name__ == '__main__':
    a = sys.argv[1:]
    kom = a[0] if a else ''
    if kom == 'iskele': iskele(a[1])
    elif kom == 'dogrula': sys.exit(dogrula(a[1], '--ses' in a))
    elif kom == 'birlestir': sys.exit(birlestir(a[1] if len(a) > 1 else '2'))
    else: print(__doc__)
