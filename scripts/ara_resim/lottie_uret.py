#!/usr/bin/env python3
"""Ara resim → Lottie: özgün SVG alt katmanda (base64 data URI görsel), üstte mekanizmayı oynatan yarı saydam şekiller.

Kullanım: python3 scripts/ara_resim/lottie_uret.py k2-21-sedatif-ve-hipnotik-ilaclar [r01 r03 …]
Resim başına hareket planı lottie_plan/<k2_NN>.py içindeki PLAN sözlüğündedir (koordinatlar SVG kaynağından). Metin eklenmez, yeni tıbbi
bilgi eklenmez; son kare = tam ve sakin durum (hareketi azalt açıkken son kare gösterilir). LLM/GPU yok.
"""
from __future__ import annotations

import base64
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / 'scripts' / 'kmb'))
from lottie_dsl import K, S, G, yol, st, fl, el, rc, tm, ornekle  # noqa: E402

FR = 30
SURE = 180  # 6 sn döngü


# ———————————————————————— yapı taşları

def katman(ad, sekiller, o=None):
    ks = {'o': o or S(100), 'r': S(0), 'p': S([0, 0, 0]), 'a': S([0, 0, 0]), 's': S([100, 100, 100])}
    return {'ddd': 0, 'ty': 4, 'nm': ad, 'sr': 1, 'ks': ks, 'ao': 0, 'shapes': sekiller, 'ip': 0, 'op': SURE, 'st': 0, 'bm': 0}


def iz(d, h, w, t0, t1, o=45):
    """Yolu parlak yarı saydam çizgiyle t0→t1 arasında baştan sona çizer; sonra kalır."""
    return katman('iz', [G(yol(d), tm(K((t0, 0), (t1, 100))), st(h, w, o))])


def isaretci(d, h, t0, t1, r=9, kalsin=True):
    """Yol boyunca kayan nokta; kalsin=True ise sonda yolun ucunda durur, değilse kaybolur."""
    nk = ornekle(d, 24)
    adim = (t1 - t0) / 24
    kp = [(t0 + i * adim, [round(x, 1), round(y, 1)]) for i, (x, y) in enumerate(nk)]
    p = {'a': 1, 'k': [{'t': round(t, 2), 's': v, **({'i': {'x': 1, 'y': 1}, 'o': {'x': 0, 'y': 0}} if j < len(kp) - 1 else {})}
                       for j, (t, v) in enumerate(kp)]}
    son = 100 if kalsin else 0
    o = K((0, 0), (t0, 0), (t0 + 4, 100), (t1, 100), (t1 + 8, son))
    g = G(el(0, 0, 2 * r, 2 * r), fl(h, o=100), st('#ffffff', 2.5))
    g['it'][-1]['p'] = p
    return katman('isaretci', [g], o=o)


def nabiz(sekil, h, t0, sure=24, son=30, w=5):
    """Şekli çevreleyen halka: t0'da belirir, parlayıp söner, son opaklıkta kalır (sakin vurgu)."""
    o = K((0, 0), (t0, 0), (t0 + sure * .4, 95), (t0 + sure, son))
    gw = K((t0, w + 6), (t0 + sure, w))
    return katman('nabiz', [G(sekil, st(h, gw, 100))], o=o)


def gecis(x, y, x2, y2, h, t0, t1, r=9):
    """Nokta (iyon) x,y → x2,y2 yürür ve söner (son karede görünmez)."""
    g = G(el(0, 0, 2 * r, 2 * r), fl(h, o=100), st('#15803d', 1.5))
    g['it'][-1]['p'] = K((t0, [x, y]), (t1, [x2, y2]))
    o = K((0, 0), (t0, 0), (t0 + 3, 100), (t1 - 4, 100), (t1, 0))
    return katman('iyon', [g], o=o)


def kutu(x, y, w, h, r=12, pay=6):
    return rc(x + w / 2, y + h / 2, w + 2 * pay, h + 2 * pay, r + 4)


def halka(cx, cy, r):
    return el(cx, cy, 2 * r, 2 * r)


# ———————————————————————— resim başına plan (alttan üste katmanlar)

MAVI, KIRMIZI, YESIL, TURUNCU, MOR, GRI = '#2563eb', '#dc2626', '#15803d', '#ea580c', '#7c3aed', '#475569'


def plan_yukle(key: str) -> dict:
    """Dersin hareket planı: lottie_plan/k2_NN.py → PLAN (yoksa boş)"""
    import importlib
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    ad = re.match(r'^k\d-\d{2}', key).group(0).replace('-', '_')
    try:
        return importlib.import_module(f'lottie_plan.{ad}').PLAN
    except ModuleNotFoundError:
        return {}


def uret(key: str, rid: str, svg: Path) -> dict:
    kaynak = svg.read_text(encoding='utf-8')
    w, h = [int(float(x)) for x in re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', kaynak).groups()]
    veri = 'data:image/svg+xml;base64,' + base64.b64encode(kaynak.encode()).decode()
    alt = {'ddd': 0, 'ty': 2, 'nm': 'ozgun_svg', 'refId': 'bg', 'sr': 1, 'ao': 0, 'ip': 0, 'op': SURE, 'st': 0, 'bm': 0,
           'ks': {'o': S(100), 'r': S(0), 'p': S([0, 0, 0]), 'a': S([0, 0, 0]), 's': S([100, 100, 100])}}
    ust = plan_yukle(key)[rid]()
    for i, l in enumerate(ust):
        l['ind'] = i + 2
        l['nm'] = f"{l['nm']}_{i}"
    alt['ind'] = 1
    # Lottie'de katman listesi üstten alta: üst katmanlar önce (son eklenen en üstte), özgün SVG en sonda
    return {'v': '5.7.4', 'fr': FR, 'ip': 0, 'op': SURE, 'w': w, 'h': h, 'nm': f'{key}-{rid}', 'ddd': 0,
            'assets': [{'id': 'bg', 'w': w, 'h': h, 'u': '', 'p': veri, 'e': 1}], 'layers': [*reversed(ust), alt]}


def main():
    if len(sys.argv) < 2:
        sys.exit('kullanım: lottie_uret.py <key> [rNN …]')
    key = sys.argv[1]
    veri_yol = KOK / 'src' / 'data' / 'ara_resim' / f'{key}.json'
    d = json.loads(veri_yol.read_text(encoding='utf-8'))
    secim = set(sys.argv[2:])
    for r in d['resimler']:
        rid = r['id']
        if rid not in plan_yukle(key) or (secim and rid not in secim):
            continue
        klasor = KOK / 'public' / 'ara_resim' / key
        lj = uret(key, rid, klasor / r['svg'])
        hedef = klasor / f'{rid}.json'
        hedef.write_text(json.dumps(lj, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
        r['lottie'] = hedef.name
        print(f'{rid}: {hedef.stat().st_size // 1024} KB, {len(lj["layers"]) - 1} hareket katmanı')
    veri_yol.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
