#!/usr/bin/env python3
"""Sesli derste ÇIKMIŞ ara soru hattı (kullanıcı kararı 2026-11-25).

Dersin sesli çözücüsündeki (src/data/k<N><branş>_cozucu) `tur: cikmis` soruları, sorunun dayandığı en ileri slaytın son
paragrafı bitince derste açılır; ara soru sayfasıyla aynı akış: EMA soruyu okur, (otomatik çöz açıksa) düşünme payından sonra
çözer. Yeni ses ÜRETİLMEZ: çözücünün mevcut EMA klipleri (q/c/d/s-*) kullanılır, LLM/GPU yok (kural 10/20 dışı).
Sıfır ileriye sızıntı (kural 7): soru dayanak sayfalarının EN BÜYÜĞÜNÜN son paragrafından sonra açılır.

  python3 meds/scripts/uretim/cikmis_ara/kur.py birlestir [<kurul>]   # → src/data/k<N>cikmisara/{index,<ders-key>}.json
  python3 meds/scripts/uretim/cikmis_ara/kur.py dogrula [<kurul>]     # kapı: 0 HATA şart

Girdi: data/sesli_anlatim/hizalama/<key>.json (paragraf → slayt), src/data/dersler/k<N>.json (ders → çözücü kodu),
çözücü ders dosyası + klip özetleri. Ön yüz: src/components/canliDers/CdHocaAra.tsx (hocaAraYukle).
"""
from __future__ import annotations
import sys as _sys
from pathlib import Path as _Path
_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402
import json, sys

MEDS = _kok.MEDS
HIZ = MEDS / 'data/sesli_anlatim/hizalama'
DATA = MEDS / 'src/data'
GEREK = lambda n: [f'q-{n}', f'c-{n}', f'd-{n}'] + [f's-{n}-{h}' for h in 'ABCDE']  # noqa: E731


def son_paragraf(hz: dict, sayfa: int):
    son = None
    for i, e in enumerate(hz.get('paragraflar') or []):
        if e and (e.get('dosya') or 0) == 0 and sayfa in [e.get('sayfa'), *(e.get('sayfalar') or [])]: son = i
    return son


def cozucu_setleri(kurul: str, kod: str):
    """Ders kodunun çözücü setleri (bölünmüşse 2f06-1, 2f06-2 …); hoca/ara çözücüleri hariç."""
    for idx in sorted(DATA.glob(f'k{kurul}*_cozucu/index.json')):
        brans = idx.parent.name[:-len('_cozucu')]
        if brans.endswith('hoca') or brans.endswith('hocaara'): continue
        for x in json.load(open(idx, encoding='utf-8')).get('dersler', []):
            if x['kod'] == kod or x['kod'].startswith(f'{kod}-'):
                f = idx.parent / f"{x['kod']}.json"
                if f.exists(): yield brans, json.load(open(f, encoding='utf-8'))


def kayit_oku(brans, klasor):
    p = MEDS / 'data' / f'{brans}_cozucu' / 'ses' / klasor / 'kayit.json'
    return json.load(open(p)) if p.exists() else None


def kur(kurul: str):
    """(key → ders verisi, hatalar)"""
    defter = json.load(open(DATA / 'dersler' / f'k{kurul}.json', encoding='utf-8'))
    KOD = {x['id']: x['kod'] for x in defter.get('dersler', []) if x.get('kod')}
    out, hata, kayitlar = {}, [], {}
    for fh in sorted(HIZ.glob(f'k{kurul}-*.json')):
        key = fh.stem
        kod = KOD.get(key[:5])
        if not kod: continue
        hz = json.load(open(fh, encoding='utf-8'))
        sorular = []
        for brans, d in cozucu_setleri(kurul, kod):
            klip = d.get('klip') or {}
            for q in d.get('sorular', []):
                if q.get('tur') != 'cikmis': continue
                y = f"{key} {d['kod']}#{q['no']}"
                day = [int(p) for p in q.get('sayfa') or [] if str(p).isdigit()]
                if not day: hata.append(f'{y}: dayanak sayfası yok'); continue
                par = son_paragraf(hz, max(day))
                if par is None: hata.append(f'{y}: {max(day)}. slayt sesli derste hiçbir paragrafa eşlenmemiş — atlandı'); continue
                eks = [k for k in GEREK(q['no']) if k not in klip]
                if eks: hata.append(f'{y}: EMA klibi eksik {eks} — atlandı'); continue
                ky = kayitlar.setdefault((brans, d.get('klasor') or d['kod']), kayit_oku(brans, d.get('klasor') or d['kod']))
                bayat = [k for k in GEREK(q['no']) if ky is not None and (k not in ky or ky[k].get('h') != klip[k].get('v'))]
                if bayat: hata.append(f'{y}: çözücü yayını ses kaydıyla uyuşmuyor {bayat} (çözücü birleştirmesi bayat) — atlandı'); continue
                if q.get('dogru') not in 'ABCDE' or set(q.get('secenekler') or {}) != set('ABCDE'):
                    hata.append(f'{y}: şık/doğru cevap eksik — atlandı'); continue
                sorular.append({'no': len(sorular) + 1, 'tur': 'cikmis', 'sinav': q.get('sinav'), 'soru': q['soru'],
                                'secenekler': q['secenekler'], 'dogru': q['dogru'], 'siklar': q['siklar'], 'cozum': q['cozum'],
                                'sayfa': day, 'anlatim': '',
                                'ara': {'dosya': 0, 'sayfa': max(day), 'paragraf': par},
                                'kaynak': {'brans': brans, 'klasor': d.get('klasor') or d['kod'], 'no': q['no'],
                                           'klip': {k: klip[k] for k in GEREK(q['no'])}}})
        if sorular:
            sorular.sort(key=lambda q: (q['ara']['paragraf'], q['kaynak']['no']))
            for i, q in enumerate(sorular, 1): q['no'] = i
            out[key] = {'kod': kod, 'key': key, 'baslik': kod, 'sorular': sorular, 'klip': {}}
    return out, hata


def birlestir(kurul='2'):
    out, hata = kur(kurul)
    D = DATA / f'k{kurul}cikmisara'
    D.mkdir(parents=True, exist_ok=True)
    for f in D.glob('*.json'): f.unlink()
    for key, v in out.items():
        json.dump(v, open(D / f'{key}.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    json.dump({'surum': f'k{kurul}cikmisara-v1', 'dersler': [{'key': k, 'soru': len(v['sorular'])} for k, v in out.items()]},
              open(D / 'index.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for x in hata: print('UYARI', x)
    print(f'k{kurul}cikmisara: {len(out)} ders · {sum(len(v["sorular"]) for v in out.values())} çıkmış ara soru · {len(hata)} atlanan')
    return 0


def dogrula(kurul='2'):
    D = DATA / f'k{kurul}cikmisara'
    e = []
    for f in sorted(D.glob('k*.json')):
        v = json.load(open(f, encoding='utf-8'))
        hz = json.load(open(HIZ / f'{v["key"]}.json', encoding='utf-8'))
        n = len(hz.get('paragraflar') or [])
        for q in v['sorular']:
            y = f"{v['key']} #{q['no']}"
            a = q['ara']
            if not 0 <= a['paragraf'] < n: e.append(f'{y}: paragraf {a["paragraf"]} derste yok')
            if a['sayfa'] != max(q['sayfa']): e.append(f'{y}: ara slaytı dayanağın en ilerisi değil — ileriye sızıntı')
            if son_paragraf(hz, a['sayfa']) != a['paragraf']: e.append(f'{y}: paragraf hizalamayla uyuşmuyor (bayat veri, birlestir yeniden)')
            eks = [k for k in GEREK(q['kaynak']['no']) if k not in q['kaynak']['klip']]
            if eks: e.append(f'{y}: klip eksik {eks}')
            kayit = MEDS / 'data' / f"{q['kaynak']['brans']}_cozucu" / 'ses' / q['kaynak']['klasor'] / 'kayit.json'
            if kayit.exists():
                ky = json.load(open(kayit))
                for k, m in q['kaynak']['klip'].items():
                    if k not in ky or ky[k].get('h') != m.get('v'): e.append(f'{y}: {k} klip sürümü ses kaydıyla uyuşmuyor')
    for x in e: print('HATA', x)
    print(f'çıkmış ara kapısı: {len(e)} HATA')
    return 1 if e else 0


if __name__ == '__main__':
    a = sys.argv[1:]
    kom = a[0] if a else ''
    if kom == 'birlestir': sys.exit(birlestir(a[1] if len(a) > 1 else '2'))
    elif kom == 'dogrula': sys.exit(dogrula(a[1] if len(a) > 1 else '2'))
    else: print(__doc__)
