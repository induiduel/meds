"""k2-37 OKB ve İlişkili Bozukluklar — ara resim Lottie hareket planı.

Varsayılan: SVG yapıları belge sırasıyla (_oto_ara). r04 ve r07 adimlar sırasıyla elle yazılmıştır (koordinatlar SVG
kaynağından, <use> simgeleri çözülmüş konumlarıyla).
"""
from lottie_uret import *  # noqa: F401,F403
from ._oto_ara import plan, bul, kullanimlar

KEY = 'k2-37-okb-ve-iliskili-bozukluklar'
PLAN = plan(KEY)


def r04():
    # 1 streptokok enfeksiyonu → 2 antikor yanıtı → 3 kaudat, putamen, globus pallidus → 4 klinik: ani başlangıç → kan → tedavi
    k = [nabiz(yol(bul(KEY, 'r04', 'M110 200 C110')), '#9f1239', 0, 22, 25, 4)]
    kok = kullanimlar(KEY, 'r04', 'kok')
    for i, (x, y, _) in enumerate(kok):
        k.append(nabiz(halka(x, y, 13), KIRMIZI, 8 + i * 4, 18, 30, 3))
    for i, (x, y, _) in enumerate(kullanimlar(KEY, 'r04', 'ab')):
        x0, y0, _ = kok[-1 - (i % len(kok))]
        k.append(gecis(x0, y0, x, y, '#93c5fd', 34 + i * 6, 54 + i * 6, 6))
        k.append(nabiz(halka(x, y - 2, 18), MAVI, 52 + i * 6, 18, 30, 3))
    k.append(nabiz(yol(bul(KEY, 'r04', 'M480 300 C470')), '#9f1239', 76, 20, 20, 3))
    for i, (bas, h) in enumerate([('M600 250', MOR), ('M640 250', MOR), ('M545 275', MAVI), ('M695 275', MAVI),
                                  ('M560 300', YESIL), ('M680 300', YESIL)]):
        k.append(nabiz(yol(bul(KEY, 'r04', bas)), h, 86 + (i // 2) * 12 + (i % 2) * 3, 22, 40, 4))
    for i, (y1, y2) in enumerate([(260, 300), (370, 410)]):
        d = f'M1010 {y1} L1010 {y2}'
        k += [iz(d, GRI, 8, 128 + i * 16, 140 + i * 16, 50), isaretci(d, GRI, 128 + i * 16, 140 + i * 16, r=6)]
    return k


def r07():
    # 1 OKB: obsesyon → yıkama (nötrleme); 2 trikotilomani: öncesinde obsesyon yok; 3 saç yolma, seyrelmiş alan; 4 ayırıcı tanı şeridi
    d = bul(KEY, 'r07', 'M330 245 C340')
    k = [nabiz(yol(bul(KEY, 'r07', 'M230 212 C210')), MOR, 2, 24, 35, 4),
         iz(d, MOR, 9, 18, 40, 50), isaretci(d, MOR, 18, 40, r=7),
         nabiz(yol(bul(KEY, 'r07', 'M404 436 C399')), '#0369a1', 40, 22, 35, 4)]
    for i, (x, y, _) in enumerate(kullanimlar(KEY, 'r07', 'damla')):
        k.append(gecis(x, y, x, y + 40, '#7dd3fc', 46 + i * 6, 62 + i * 6, 6))
    k.append(nabiz(yol(bul(KEY, 'r07', 'M880 254 C860')), GRI, 72, 24, 25, 4))
    d2 = bul(KEY, 'r07', 'M800 285 C800')
    k += [nabiz(yol(bul(KEY, 'r07', 'M774 336 C769')), TURUNCU, 96, 22, 30, 4),
          iz(d2, TURUNCU, 8, 104, 118, 50), isaretci(d2, TURUNCU, 104, 118, r=6),
          nabiz(halka(755, 250, 24), TURUNCU, 116, 24, 40, 4),
          nabiz(kutu(30, 640, 1140, 130, 16, 4), '#ea580c', 140, 24, 25, 4)]
    return k


PLAN.update(r04=r04, r07=r07)
