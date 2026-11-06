#!/usr/bin/env python3
"""Ara resim → Lottie: özgün SVG alt katmanda (base64 data URI görsel), üstte mekanizmayı oynatan yarı saydam şekiller.

Kullanım: python3 scripts/ara_resim/lottie_uret.py k2-21-sedatif-ve-hipnotik-ilaclar [r01 r03 …]
Resim başına hareket planı aşağıdaki PLAN sözlüğündedir (koordinatlar SVG kaynağından). Metin eklenmez, yeni tıbbi
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


def r01():
    a = 'M160 545 L640 180'
    b = 'M160 545 C260 470 330 425 400 412 C480 400 580 395 680 390'
    return [iz(a, KIRMIZI, 14, 10, 70, 30), isaretci(a, KIRMIZI, 10, 70),
            iz(b, MAVI, 14, 80, 140, 30), isaretci(b, MAVI, 80, 140),
            nabiz(halka(400, 412, 16), MAVI, 140, 30, 0)]


def r02():
    k = [nabiz(yol('M70 230 C80 160 200 140 300 160 C360 170 380 200 360 250 C340 320 200 360 120 330 C80 315 65 280 70 230 z'), '#991b1b', 0),
         iz('M360 210 C380 205 390 205 398 205', '#991b1b', 8, 14, 22, 60),
         nabiz(kutu(400, 150, 210, 110), MAVI, 20),
         iz('M612 205 C650 205 660 205 690 205', GRI, 8, 36, 46, 60),
         nabiz(kutu(700, 150, 210, 110), '#b45309', 44),
         iz('M912 205 C940 205 950 205 975 205', GRI, 8, 60, 70, 60),
         nabiz(kutu(985, 150, 170, 110), YESIL, 68),
         iz('M805 262 L790 288', TURUNCU, 8, 76, 84, 60),
         nabiz(kutu(560, 290, 400, 110), TURUNCU, 82)]
    tur = 'M110 645 C130 580 150 590 200 615 C220 560 245 565 300 595 C320 540 345 545 400 578 C420 525 445 530 500 565 C520 515 545 520 600 555 C620 510 645 515 700 548'
    yes = 'M110 645 C130 600 150 610 200 640 C220 600 245 605 300 640 C320 600 345 605 400 640 C420 600 445 605 500 640'
    return k + [iz(yes, YESIL, 10, 100, 150, 30), iz(tur, TURUNCU, 12, 100, 165, 30), isaretci(tur, TURUNCU, 100, 165)]


def r03():
    k = []
    for i, (cx, cy) in enumerate([(340, 230), (473, 327), (422, 483), (258, 483), (207, 327)]):
        k.append(nabiz(halka(cx, cy, 66), GRI, 4 + i * 8, 20, 0, 3))
    for t, s in [(50, halka(407, 278, 17)), (58, halka(340, 483, 17)), (78, rc(273, 278, 30, 30, 6)), (100, halka(228, 531, 19))]:
        h = MOR if t < 70 else (MAVI if t < 90 else TURUNCU)
        k.append(nabiz(s, h, t, 26, 40))
    k.append(nabiz(halka(340, 370, 42), YESIL, 122, 30, 35))
    return k


def r04():
    k = [nabiz(halka(200, 160, 16), MOR, 0, 20, 30), nabiz(rc(422, 162, 30, 30, 6), MAVI, 12, 20, 30),
         nabiz(halka(780, 160, 16), MOR, 0, 20, 30), nabiz(halka(1002, 162, 19), TURUNCU, 12, 20, 30)]
    # sol: kısa iyon geçişleri; sağ: aynı kanal daha uzun süre açık, akış kesintisiz
    for t in (40, 80, 120):
        k.append(gecis(310, 188, 310, 292, '#bbf7d0', t, t + 22))
    for t in range(40, 150, 11):
        k.append(gecis(890, 188, 890, 292, '#bbf7d0', t, t + 22))
    return k


def r05():
    k = []
    for i, x in enumerate((215, 600, 985)):
        h = (MAVI, GRI, KIRMIZI)[i]
        t = 6 + i * 44
        k += [nabiz(rc(x, 251, 42, 34, 7), h, t, 24, 40),
              iz(f'M{x} 420 L{x} 460', h, 9, t + 16, t + 26, 55),
              nabiz(kutu(x - 165, 470, 330, 80), h, t + 24, 20, 25)]
    return k


def r06():
    k = []
    for i, y in enumerate((160, 222, 284, 346)):
        k.append(nabiz(rc(515, y + 23, 390, 64, 10), ('#64748b', MAVI, '#1e40af', MOR)[i], 6 + i * 26, 24, 0, 3))
    k += [iz('M880 355 C895 330 910 382 925 355 C940 330 955 382 970 355 C985 332 1000 378 1015 355', '#1d4ed8', 9, 115, 140, 35),
          iz('M880 388 C910 340 940 436 970 388 C1000 342 1030 434 1060 388', '#1e40af', 10, 130, 160, 35)]
    return k


def r07():
    c = 'M70 190 C140 200 200 240 250 265 C290 282 310 288 340 290'
    k = [iz(c, MAVI, 14, 6, 56, 30), isaretci(c, MAVI, 6, 56)]
    for i, x in enumerate((80, 118, 156, 194, 232)):
        if i >= 2:  # aşağı regülasyon bölümü: sağdaki reseptörler sırayla kırmızı halkayla işaretlenir, sonra söner
            k.append(katman('azal', [G(halka(x, 366, 12), st(KIRMIZI, 3, 100))], o=K((0, 0), (58 + i * 3, 0), (66 + i * 3, 90), (90, 0))))
    k += [nabiz(kutu(640, 150, 500, 64), MOR, 92, 20, 25), nabiz(kutu(640, 252, 500, 50), '#64748b', 108, 20, 25),
          nabiz(kutu(640, 340, 500, 96), KIRMIZI, 124, 20, 25),
          iz('M610 610 C640 540 660 540 690 610 C720 540 740 540 770 610 C800 540 820 540 850 610', KIRMIZI, 11, 130, 170, 35)]
    return k


def r08():
    m = 'M570 220 L660 225 C690 230 700 470 740 480 C800 490 830 480 860 420 C900 340 930 290 1120 262'
    return [nabiz(rc(250, 337, 40, 36, 6), GRI, 0, 22, 30),
            iz('M340 405 C320 385 295 372 275 360', GRI, 9, 10, 30, 55),
            nabiz(rc(350, 425, 42, 38, 6), GRI, 8, 22, 30),
            iz('M165 410 C190 390 210 375 228 360', MAVI, 9, 32, 50, 45),
            iz('M570 220 L1120 260', MAVI, 9, 60, 110, 25),
            iz(m, MOR, 14, 70, 160, 30), isaretci(m, MOR, 70, 160)]


PLAN = {'r01': r01, 'r02': r02, 'r03': r03, 'r04': r04, 'r05': r05, 'r06': r06, 'r07': r07, 'r08': r08}


def uret(key: str, rid: str, svg: Path) -> dict:
    kaynak = svg.read_text(encoding='utf-8')
    w, h = [int(float(x)) for x in re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', kaynak).groups()]
    veri = 'data:image/svg+xml;base64,' + base64.b64encode(kaynak.encode()).decode()
    alt = {'ddd': 0, 'ty': 2, 'nm': 'ozgun_svg', 'refId': 'bg', 'sr': 1, 'ao': 0, 'ip': 0, 'op': SURE, 'st': 0, 'bm': 0,
           'ks': {'o': S(100), 'r': S(0), 'p': S([0, 0, 0]), 'a': S([0, 0, 0]), 's': S([100, 100, 100])}}
    ust = PLAN[rid]()
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
        if rid not in PLAN or (secim and rid not in secim):
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
