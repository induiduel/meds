#!/usr/bin/env python3
"""Ders programı sırası → src/data/deckSchedule.json (Öğren kitaplığı "Ders programı" sıralaması).

Kaynak: ders işçisinin checklist.json'u (kurul, tarih, program sırası, hoca). Çıktı: {deste_id: {s, t, k, h}}
  s = programdaki sıra (kurul → tarih → listedeki yer), t = ders tarihi (YYYY-AA-GG), k = kurul, h = hoca.
build_deck_pdf_sources.py her çalıştığında bunu da çalıştırır.
"""
import json, os, sys

APP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ISCI = os.environ.get('MEDS_ISCI_DIR') or os.path.join(os.path.dirname(APP), 'ders_isci')
CIKTI = os.path.join(APP, 'src', 'data', 'deckSchedule.json')


def main():
    src = os.path.join(ISCI, 'checklist.json')
    if not os.path.exists(src):
        print('checklist.json yok, atlandı:', src)
        return 0
    konular = json.load(open(src, encoding='utf-8')).get('konular', [])
    rows = [(k.get('kurul') or 99, k.get('tarih') or '9999', i, k) for i, k in enumerate(konular) if k.get('deste_id')]
    rows.sort(key=lambda r: r[:3])
    out = {}
    for n, (_, _, _, k) in enumerate(rows, 1):
        e = {'s': n, 'k': k.get('kurul')}
        if k.get('tarih'):
            e['t'] = k['tarih']
        if k.get('hoca'):
            e['h'] = k['hoca']
        out[k['deste_id']] = e
    if not out:
        print('Program sırası boş; mevcut dosya korunur.')
        return 0
    tmp = CIKTI + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, ensure_ascii=False, indent=0, sort_keys=True)
    os.replace(tmp, CIKTI)
    print(f'Ders programı sırası: {len(out)} deste → {CIKTI}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
