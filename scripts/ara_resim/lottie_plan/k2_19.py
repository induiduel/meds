"""k2-19 Bipolar Bozukluk — ara resim Lottie hareket planı (koordinatlar SVG kaynağından)."""
import re
from pathlib import Path

from lottie_uret import *  # noqa: F401,F403  yapı taşları + renkler
from lottie_plan.k2_18 import q, ov  # Q→C çevirici, elips halkası

_SVG = Path(__file__).resolve().parents[3] / 'public' / 'ara_resim' / 'k2-19-bipolar-bozukluk'


def svg_yol(rid, bas):
    s = (_SVG / f'{rid}.svg').read_text()
    return re.search(r'd="(' + re.escape(bas) + r'[^"]*)"', s).group(1)


def r01():
    a = 'M300 222 C360 222 380 126 440 126 C500 126 520 222 580 222 C640 222 660 269 720 269 C780 269 800 222 860 222 L1158 222'
    b = 'M300 442 C340 442 350 394 400 394 C450 394 460 442 500 442 C560 442 580 508 660 508 C740 508 760 442 820 442 L900 442'
    b2 = 'M900 442 C930 442 940 354 980 354 C1020 354 1030 442 1070 442 L1158 442'
    c = q(svg_yol('r01', 'M300 662'))
    return [iz(a, TURUNCU, 10, 4, 50, 40), isaretci(a, TURUNCU, 4, 50, 8),
            nabiz(halka(440, 126, 14), KIRMIZI, 18, 20, 35),
            iz(b, MAVI, 10, 56, 100, 40), isaretci(b, MAVI, 56, 100, 8),
            nabiz(halka(400, 394, 13), TURUNCU, 64, 18, 30), nabiz(halka(660, 508, 13), MAVI, 82, 18, 30),
            iz(b2, KIRMIZI, 10, 104, 120, 40), nabiz(halka(980, 354, 14), KIRMIZI, 112, 20, 35),
            iz(c, MOR, 9, 124, 170, 40), isaretci(c, MOR, 124, 170, 8),
            iz('M300 572 L1140 572', MOR, 8, 124, 170, 35)]


def r02():
    k = [nabiz(rc(270, 310, 360, 90, 30), MOR, 2, 22, 0, 4)]
    for i, x in enumerate((200, 250, 300, 340)):
        k.append(gecis(x, 345, x + (i - 1.5) * 6, 408, TURUNCU, 20 + i * 5, 42 + i * 5, 7))
    k.append(nabiz(rc(270, 425, 400, 40, 14), YESIL, 46, 20, 25))
    # B: 1 = çok madde (çok nokta, normal reseptör), 2 = az madde ama reseptör parlıyor
    for i, x in enumerate((690, 705, 720, 735, 750, 712, 728)):
        k.append(gecis(x, 318, x, 360, TURUNCU, 70 + i * 4, 88 + i * 4, 5))
    k += [nabiz(rc(720, 372, 250, 26, 10), YESIL, 96, 18, 20)]
    for i, x in enumerate((1010, 1030)):
        k.append(gecis(x, 318, x, 360, TURUNCU, 110 + i * 6, 128 + i * 6, 5))
    k += [nabiz(rc(1020, 372, 250, 26, 10), KIRMIZI, 132, 22, 45, 7)]
    k += [nabiz(kutu(40, 600, 320, 110), TURUNCU, 140, 16, 20), nabiz(kutu(380, 600, 320, 110), KIRMIZI, 148, 16, 20),
          nabiz(kutu(800, 600, 360, 110), KIRMIZI, 158, 18, 35)]
    return k


def r03():
    d = 'M720 340 C760 220 800 220 840 340 C880 460 920 460 960 340 C1000 220 1040 220 1080 340 C1100 400 1120 430 1140 440'
    return [iz('M88 268 L110 242 L120 260 L142 236', KIRMIZI, 9, 4, 18, 45),
            iz(q('M505,285 Q535,303 569,287'), MAVI, 9, 14, 28, 45),
            iz('M200 300 L288 384', KIRMIZI, 9, 30, 50, 40), isaretci('M200 300 L288 384', KIRMIZI, 30, 50, 7, False),
            iz('M480 310 L394 384', MAVI, 9, 30, 50, 40), isaretci('M480 310 L394 384', MAVI, 30, 50, 7, False),
            nabiz(kutu(290, 370, 100, 54, 6), MOR, 52, 22, 35),
            iz(d, MOR, 11, 80, 150, 35), isaretci(d, MOR, 80, 150, 9),
            nabiz(halka(780, 250, 22), TURUNCU, 96, 18, 25), nabiz(halka(900, 430, 22), MAVI, 118, 18, 25),
            nabiz(halka(1020, 250, 22), TURUNCU, 138, 18, 25)]


def r04():
    soru = 'M175 355 C250 320 330 320 400 355'
    k = [iz(soru, MAVI, 8, 4, 30, 35), isaretci(soru, MAVI, 4, 30, 7, False)]
    for i, (d, sek) in enumerate((('M600 230 C540 270 500 320 470 380', kutu(596, 140, 92, 70)),
                                  ('M555 320 C520 340 500 360 478 388', kutu(552, 286, 140, 82)),
                                  ('M330 200 C380 230 405 300 422 375', halka(305, 190, 22)))):
        t = 36 + i * 24
        k += [nabiz(sek, TURUNCU, t, 16, 25), iz(d, TURUNCU, 9, t + 4, t + 18, 45), isaretci(d, TURUNCU, t + 4, t + 18, 7, False)]
    k += [nabiz(kutu(800, 420, 110, 80, 10), MAVI, 110, 18, 30),
          nabiz(kutu(1010, 230, 110, 270, 10), TURUNCU, 120, 18, 30)]
    for i, x in enumerate((40, 340, 650, 940)):
        w = (250, 270, 250, 225)[i]
        k.append(nabiz(kutu(x, 625, w, 100), (TURUNCU, TURUNCU, MAVI, KIRMIZI)[i], 140 + i * 9, 14, 20))
    return k


def r05():
    k = [iz('M110 185 L366 185', TURUNCU, 26, 4, 22, 35), iz('M110 229 L558 229', '#c2410c', 26, 22, 46, 35),
         iz('M110 251 L1070 251', MAVI, 6, 46, 90, 70), iz('M110 289 L1070 289', MAVI, 6, 46, 90, 70)]
    for i in range(3):
        k.append(nabiz(halka(64, 418 + 34 * i, 15), TURUNCU, 96 + i * 8, 14, 35))
    for i in range(5):
        k.append(nabiz(halka(644, (414, 444, 474, 504, 564)[i], 15), MAVI, 124 + i * 7, 14, 35))
    return k


def r07():
    k = [iz('M260 200 C380 140 520 140 660 200 L1130 200', TURUNCU, 9, 4, 50, 40), isaretci('M260 200 C380 140 520 140 660 200 L1130 200', TURUNCU, 4, 50, 8),
         iz('M260 250 L1120 250', YESIL, 22, 54, 110, 35),
         iz('M260 320 L740 320', MOR, 22, 60, 96, 35), iz('M260 380 L760 380', '#0ea5e9', 22, 66, 100, 35),
         iz('M260 440 L640 440', KIRMIZI, 8, 72, 100, 45), nabiz(halka(450, 440, 18), KIRMIZI, 100, 20, 40)]
    k += [nabiz(kutu(40, 520, 360, 200), KIRMIZI, 120, 18, 20), nabiz(kutu(420, 520, 360, 200), YESIL, 134, 18, 30),
          nabiz(kutu(800, 520, 360, 200), MOR, 148, 18, 20)]
    return k


def r08():
    k = [iz('M90 320 L1140 320', GRI, 8, 4, 40, 30), nabiz(kutu(240, 214, 270, 60, 10), TURUNCU, 30, 20, 35),
         iz('M510 240 C570 180 710 180 770 236', MAVI, 9, 50, 84, 40), isaretci('M510 240 C570 180 710 180 770 236', MAVI, 50, 84, 8, False),
         nabiz(halka(780, 244, 18), MAVI, 84, 18, 35)]
    for i, y in enumerate((494, 572, 650)):
        k.append(nabiz(halka(74, y, 26), MAVI, 100 + i * 12, 16, 30))
    k += [iz('M640 610 C800 602 960 602 1150 610', KIRMIZI, 6, 140, 166, 45)]
    return k


def r09():
    k = [nabiz(halka(200, 310, 116), TURUNCU, 4, 24, 30),
         iz('M330 300 C360 260 410 260 440 300', GRI, 8, 34, 54, 40), isaretci('M330 300 C360 260 410 260 440 300', GRI, 34, 54, 7, False),
         nabiz(halka(560, 310, 116), TURUNCU, 56, 24, 30),
         iz('M830 360 L1130 360', GRI, 6, 86, 110, 40), iz('M880 360 C900 300 960 300 990 360', '#c2410c', 8, 90, 110, 45)]
    for i, (x, w, h) in enumerate(((40, 340, MOR), (440, 340, TURUNCU), (840, 320, YESIL))):
        k.append(nabiz(kutu(x, 600, w, 120), h, 120 + i * 14, 18, 25 if i < 2 else 35))
    return k


def r10():
    k = [nabiz(halka(525, 434, 14), MOR, 4, 16, 35), nabiz(halka(525, 470, 14), '#c2410c', 14, 16, 35),
         nabiz(halka(525, 506, 14), '#0369a1', 24, 16, 35),
         nabiz(yol('M260 300 C300 260 380 260 420 300 C450 330 440 370 400 380 C360 390 290 390 260 360 C240 340 240 320 260 300 z'), MOR, 44, 22, 30),
         nabiz(yol('M200 200 C230 160 300 150 340 170 C380 140 470 150 480 200 C520 220 500 260 460 250 C430 270 380 260 360 250 C320 270 240 260 220 240 C180 240 170 220 200 200 z'), MOR, 64, 26, 35, 6)]
    ekg = 'M960 270 L980 270 L990 240 L1004 300 L1016 260 L1024 270 L1064 270'
    k += [nabiz(yol('M790 260 C790 220 840 210 860 240 C880 210 930 220 930 260 C930 300 860 340 860 340 C860 340 790 300 790 260 z'), KIRMIZI, 96, 20, 30),
          iz(ekg, KIRMIZI, 7, 104, 126, 50), isaretci(ekg, KIRMIZI, 104, 126, 6, False),
          nabiz(kutu(40, 600, 520, 125), '#ca8a04', 136, 18, 25), nabiz(kutu(620, 600, 540, 125), YESIL, 152, 18, 35)]
    return k


def r11():
    c = 'M70 180 C130 180 190 330 270 340 L590 340'
    return [iz(c, TURUNCU, 10, 4, 50, 40), isaretci(c, TURUNCU, 4, 50, 8),
            nabiz(rc(345, 285, 160, 180, 6), KIRMIZI, 46, 22, 30),
            iz('M800 395 L800 211', KIRMIZI, 64, 70, 100, 30), iz('M1000 395 L1000 321', YESIL, 64, 100, 118, 30)] + \
        [nabiz(halka(64, 510 + 42 * i, 15), (TURUNCU, MOR, '#0ea5e9', KIRMIZI, GRI)[i], 126 + i * 9, 14, 30) for i in range(5)]


PLAN = {'r01': r01, 'r02': r02, 'r03': r03, 'r04': r04, 'r05': r05, 'r07': r07, 'r08': r08, 'r09': r09, 'r10': r10, 'r11': r11}
