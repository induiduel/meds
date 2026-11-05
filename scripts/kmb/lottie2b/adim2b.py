"""KMB adım videoları — 2B düz çizgi film hattı (eski adim_lottie.py korunur; bu dosya src/data/kmb/lottie2b/ üretir).
  python3 meds/scripts/kmb/lottie2b/adim2b.py [adım-id…] [--kod=01]   → lottie2b/adim-<adım>.json + lottie2b/adimlar.json
Üreticiler adim2b_a.py / adim2b_b.py / adim2b_c.py içinde `ADIMLAR = {'<adım id>': fonksiyon}`; fonksiyon `A` (Anim) alır,
cümleler 02.json `adimlar[].cumleler` metinleridir (ses `o-<adım>`), koreografi ortak2b + Sahne2B + ic_ekle2b (konu videoları).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ortak2b import CIKTI, VERI, adim  # noqa: E402


def ureticiler():
    out = {}
    for mod in ('adim2b_a', 'adim2b_b', 'adim2b_c', 'adim2b_ng1', 'adim2b_ng2', 'adim2b_ng3'):
        try:
            m = __import__(mod)
            out.update(m.ADIMLAR)
        except ImportError:
            pass
    return out


def uret(secili=None, kod='02'):
    ders = json.loads((VERI / f'{kod}.json').read_text(encoding='utf-8'))
    sy = VERI / f'ses_{kod}.json'
    ses = json.loads(sy.read_text(encoding='utf-8')) if sy.exists() else {}
    CIKTI.mkdir(parents=True, exist_ok=True)
    idx_yol = CIKTI / 'adimlar.json'
    idx = {x['adim']: x for x in json.loads(idx_yol.read_text(encoding='utf-8'))} if idx_yol.exists() else {}
    U = ureticiler()
    for a in ders['adimlar']:
        if secili and a['id'] not in secili:
            continue
        f = U.get(a['id'])
        if not f:
            if not secili:
                continue
            print(f'UYARI: {a["id"]} için 2B adım videosu yok'); continue
        k = ses.get(f'o-{a["id"]}')
        z = k['zaman'] if k and len(k['zaman']) == len(a['cumleler']) else None
        A = adim(a['id'], [c['metin'] for c in a['cumleler']], z)
        A.baslik = a['baslik']
        f(A)
        (CIKTI / f'adim-{a["id"]}.json').write_text(json.dumps(A.json(), ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
        b = A.bilgi(); b['adim'] = a['id']; b['sesli'] = bool(z)
        idx[a['id']] = b
        print(f'adim-{a["id"]}: {A.sure:.1f} sn, {len(a["cumleler"])} cümle, {len(A.katmanlar)} katman, {len(A.varliklar)} alt kompozisyon')
    sira = [a['id'] for a in ders['adimlar']]  # bu dersin sırası; öteki derslerin videoları korunur
    idx_yol.write_text(json.dumps([v for i, v in idx.items() if i not in sira] + [idx[i] for i in sira if i in idx], ensure_ascii=False, indent=1) + '\n', encoding='utf-8')


if __name__ == '__main__':
    kod = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--kod=')), '02')
    uret([a for a in sys.argv[1:] if not a.startswith('--')] or None, kod)
