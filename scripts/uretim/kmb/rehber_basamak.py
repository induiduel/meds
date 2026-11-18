#!/usr/bin/env python3
"""KMB Basamak filmi verisi (2026-11-18, kullanıcı kararı): KMB Eğitim Rehberi'ndeki (okulun resmi beceri rehberi PDF'i)
uygulama basamakları, rehberdeki sıra ve sayıyla birebir, her KMB dersine `rehberBasamaklari` olarak yazılır.
Kart metni (ne/nasıl/neden/hata/hoca) rehber + hoca ses dökümünden elle yazılır (LLM otomasyonu yok, kural 20);
`harita` = görsel koreografisi (sahne/eylem/film) alınacak hedef kartının no'su. HedefFilmi.tsx `tur="basamak"` oynatır,
ses klipleri `p-<no>` / `p-<no>-s` (ses.py), kapı dogrula.py.

  python3 meds/scripts/uretim/kmb/rehber_basamak.py <kod> <kartlar.json> --kaynak "<rehber adı, sayfa>"
"""
import sys as _sys
from pathlib import Path as _Path
_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402
import copy, json, sys
from pathlib import Path

VERI = _kok.MEDS / 'src/data/kmb'


def main():
    kod, kart_yol = sys.argv[1], Path(sys.argv[2])
    kaynak = sys.argv[sys.argv.index('--kaynak') + 1] if '--kaynak' in sys.argv else ''
    yol = VERI / f'{kod}.json'
    d = json.loads(yol.read_text(encoding='utf-8'))
    hc = {x['no']: x for x in d.get('hedefCalisma', [])}
    out = []
    for i, k in enumerate(json.loads(kart_yol.read_text(encoding='utf-8')), 1):
        if k['no'] != i: sys.exit(f'basamak sırası bozuk: {k["no"]} (beklenen {i})')
        h = hc.get(k.pop('harita'))
        if not h: sys.exit(f'basamak {i}: harita hedef kartı yok')
        k.update({'sahne': h['sahne'], 'eylem': copy.deepcopy(h.get('eylem', [])), 'film': copy.deepcopy(h['film'])})
        out.append(k)
    d['rehber'] = {'kaynak': kaynak, 'basamakSayisi': len(out)}
    d['rehberBasamaklari'] = out
    yol.write_text(json.dumps(d, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'{kod}: {len(out)} rehber basamağı yazıldı')


if __name__ == '__main__':
    main()
