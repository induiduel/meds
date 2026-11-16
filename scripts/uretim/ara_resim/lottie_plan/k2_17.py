"""k2-17 Periferik Nöropati — ara resim Lottie hareket planı (koordinatlar SVG kaynağından)."""
from lottie_uret import *  # noqa: F401,F403
from lottie_plan.k2_16 import yol, iz, isaretci, _serit  # göreli/Q/A/S yolu çeviren sarmalayıcılar

SERIT4 = [(30, 640, 260, 74), (324, 640, 260, 74), (617, 640, 260, 74), (910, 640, 260, 74)]
OK4 = ['M292 677 L320 677', 'M586 677 L614 677', 'M880 677 L908 677']
SERIT3 = [(30, 640, 357, 74), (421, 640, 357, 74), (813, 640, 357, 74)]
OK3 = ['M390 677 L418 677', 'M782 677 L810 677']
GOVDE = 'M{x} {y} q-6 -30 18 -38 q22 -10 34 8 q16 22 -4 42 q-18 16 -38 4 q-14 -6 -10 -16 z'


def r01():
    d = 'M700 430 C 680 380 640 340 560 322'
    m = 'M500 330 C 560 350 590 400 585 470'
    return [nabiz(halka(690, 452, 12), MAVI, 2, 20, 35, 4),
            iz(d, MAVI, 11, 10, 40, 40), isaretci(d, MAVI, 10, 40, 7, False),
            nabiz(halka(400, 238, 30), MAVI, 38, 22, 35),
            iz('M420 245 C 380 225 330 230 260 260', MAVI, 9, 46, 62, 45),
            nabiz(halka(244, 330, 20), KIRMIZI, 64, 20, 35, 4),
            iz('M250 345 C 320 370 380 360 430 330', KIRMIZI, 9, 72, 88, 45),
            iz(m, KIRMIZI, 11, 88, 112, 40), isaretci(m, KIRMIZI, 88, 112, 7, False),
            nabiz(yol('M560 488 q30 -14 60 0 q10 24 0 46 q-30 12 -60 0 q-10 -24 0 -46 z'), KIRMIZI, 108, 20, 30),
            nabiz(halka(470, 300, 14), MOR, 118, 20, 40, 4),
            nabiz(halka(970, 270, 114), MOR, 124, 24, 20, 4),
            *_serit(SERIT4, (MAVI, MAVI, KIRMIZI, MOR), 132, 10, OK4)]


def r02():
    k = []
    for i, (x, sx) in enumerate(((110, 80), (470, 440), (720, 690), (970, 940))):
        y0 = 190 if i == 0 else 230
        t = 6 + i * 36
        h = (GRI, KIRMIZI, TURUNCU, MOR)[i]
        k.append(iz(f'M{x} {y0 + 14} L{x} {520 if i == 0 else 480}', MAVI if i == 0 else h, 8, t, t + 18, 40))
        if i:
            k.append(nabiz(halka(x + 2, (228, 390, 384)[i - 1], 28), h, t + 14, 20, 40, 5))
            k.append(iz(f'M{x + 40} 300 C {x + 70} 340 {x + 70} 400 {x + 42} 450', h, 8, t + 22, t + 34, 55))
    k.append(nabiz(yol(GOVDE.format(x=80, y=190)), MAVI, 2, 20, 25, 4))
    return k + _serit(SERIT4, (MAVI, KIRMIZI, TURUNCU, MOR), 150, 6, OK4)


def r03():
    na = 'M290 330 C 280 280 270 240 268 210'
    kk = 'M348 230 C 352 280 352 330 350 452'
    ap = 'M730 460 L900 460 C 930 460 935 200 960 200'
    return [nabiz(halka(318, 340, 36), MOR, 2, 22, 35),
            iz(na, TURUNCU, 9, 14, 34, 50), isaretci(na, TURUNCU, 14, 34, 7, False),
            iz(kk, MOR, 9, 24, 48, 50), isaretci(kk, MOR, 24, 48, 7, False),
            iz(ap, KIRMIZI, 10, 56, 108, 40), isaretci(ap, KIRMIZI, 56, 108, 8),
            iz('M960 270 C 1000 330 1050 330 1100 320', KIRMIZI, 8, 110, 128, 50),
            *_serit(SERIT4, (MOR, MOR, MAVI, KIRMIZI), 130, 10, OK4)]


def r04():
    k = [nabiz(rc(475, 225, 100, 88, 8), KIRMIZI, 4, 20, 35),
         iz('M520 214 C 545 196 575 196 600 214', KIRMIZI, 7, 18, 34, 55),
         iz('M430 214 C 405 196 375 196 350 214', KIRMIZI, 7, 18, 34, 55)]
    for i, x in enumerate((255, 430, 605, 780)):
        t = 46 + i * 20
        k.append(nabiz(halka(x, 470, 10), YESIL, t, 16, 35, 4))
        if i < 3:
            d = f'M{x} 444 C {x + 50} 400 {x + 125} 400 {x + 171} 440'
            k += [iz(d, YESIL, 8, t + 4, t + 18, 50), isaretci(d, YESIL, t + 4, t + 18, 7, False)]
    k.append(iz('M605 500 C 565 530 470 530 434 500', GRI, 6, 120, 134, 45))
    return k + _serit([(30, 645, 357, 80), (421, 645, 357, 80), (813, 645, 357, 80)], (KIRMIZI, YESIL, YESIL), 136, 12,
                      ['M390 685 L418 685', 'M782 685 L810 685'])


def r05():
    k = [iz('M100 350 L180 344', KIRMIZI, 8, 4, 12, 70),
         katman('waller', [G(rc(140, 438, 40, 160, 8), st(KIRMIZI, 4, 70))], o=K((0, 0), (14, 0), (26, 85), (50, 30))),
         nabiz(halka(180, 440, 14), TURUNCU, 30, 18, 35, 4), nabiz(halka(176, 500, 14), TURUNCU, 40, 18, 35, 4),
         nabiz(rc(520, 302, 30, 30, 6), TURUNCU, 56, 18, 35, 4),
         iz('M564 302 L538 302', YESIL, 7, 70, 82, 60), iz('M564 406 L538 406', YESIL, 7, 76, 88, 60),
         iz('M900 214 L900 400', MAVI, 7, 96, 110, 35),
         katman('distal', [G(rc(900, 458, 34, 116, 8), st(KIRMIZI, 4, 70))], o=K((0, 0), (110, 0), (120, 85), (140, 30))),
         iz('M940 510 C 960 470 960 430 940 380', KIRMIZI, 8, 120, 140, 55),
         nabiz(kutu(30, 640, 1140, 64), GRI, 150, 20, 20)]
    return k


def r06():
    k = [nabiz(halka(160, 290, 48), MAVI, 2, 18, 0, 3), nabiz(halka(265, 300, 42), MAVI, 8, 18, 0, 3),
         nabiz(halka(210, 390, 50), MAVI, 14, 18, 0, 3),
         nabiz(yol('M80 330 C 80 180 340 180 340 330 C 340 480 80 480 80 330 Z'), MOR, 22, 20, 25, 4),
         iz('M440 205 L1140 205', MAVI, 6, 36, 60, 30),
         nabiz(halka(750, 196, 24), TURUNCU, 50, 20, 40, 4),
         iz('M440 380 L790 380', MAVI, 6, 70, 86, 30),
         nabiz(halka(801, 380, 16), KIRMIZI, 84, 18, 40, 4),
         katman('glob', [G(rc(955, 380, 290, 34, 10), st(TURUNCU, 4, 70))], o=K((0, 0), (92, 0), (100, 80), (118, 25))),
         nabiz(rc(805, 555, 96, 72, 10), KIRMIZI, 120, 20, 40),
         iz('M795 555 L770 555', KIRMIZI, 7, 128, 138, 60), iz('M815 555 L840 555', KIRMIZI, 7, 128, 138, 60)]
    return k + _serit([(30, 640, 357, 64), (421, 640, 357, 64), (813, 640, 357, 64)], (TURUNCU, KIRMIZI, '#991b1b'), 144, 10,
                      ['M390 672 L418 672', 'M782 672 L810 672'])


def r07():
    hucre = [(470, 292, 460, 165, MAVI), (470, 512, 460, 165, TURUNCU), (945, 292, 450, 165, MAVI), (945, 512, 450, 165, TURUNCU)]
    k = [nabiz(halka(120, 290, 54), MAVI, 2, 18, 30, 4), nabiz(halka(120, 520, 30), TURUNCU, 10, 18, 30, 4),
         iz('M410 160 L540 160', GRI, 8, 20, 32, 55)]
    for i, (x, y, w, h, c) in enumerate(hucre):
        t = 30 + i * 22
        if i == 2:
            k.append(iz('M720 160 l10 -14 l10 24 l10 -30 l10 30 l10 -18 l10 12 l10 -20 l10 26 l10 -10 l10 0', KIRMIZI, 8, 70, 84, 55))
        k.append(nabiz(rc(x, y, w, h - 10, 12), c, t, 20, 25, 4))
    return k + _serit([(30, 640, 357, 70), (421, 640, 357, 70), (813, 640, 357, 70)], (GRI, GRI, GRI), 130, 12,
                      ['M390 675 L418 675', 'M782 675 L810 675'])


def r08():
    a = 'M520 424 C 480 300 340 200 236 222'
    m = 'M206 286 C 280 380 360 420 420 430'
    g = 'M180 290 C 250 470 420 470 500 444'
    k = [katman('cekic', [G(rc(691, 531, 40, 24, 4), st(GRI, 4, 80))], o=K((0, 0), (2, 0), (6, 90), (16, 0))),
         nabiz(yol('M470 432 C 500 420 540 420 570 432 C 540 444 500 444 470 432 Z'), MAVI, 8, 20, 35, 5),
         iz(a, MAVI, 10, 18, 46, 40), isaretci(a, MAVI, 18, 46, 7, False),
         nabiz(halka(196, 274, 18), KIRMIZI, 46, 18, 35, 4),
         iz(m, KIRMIZI, 10, 52, 76, 40), isaretci(m, KIRMIZI, 52, 76, 7, False),
         nabiz(yol('M360 440 C 420 380 600 380 680 430 C 640 490 430 500 360 440 Z'), KIRMIZI, 76, 20, 25, 4),
         iz(g, MOR, 9, 92, 116, 40), isaretci(g, MOR, 92, 116, 7, False)]
    for i, y in enumerate((186, 256, 326, 396)):
        k.append(nabiz(rc(957, y + 35, 395, 66, 8), YESIL, 120 + i * 12, 16, 20, 3))
    return k + _serit(SERIT3, (MAVI, KIRMIZI, MOR), 150, 6, OK3)


def r09():
    k = [nabiz(halka(230, 245, 72), MAVI, 2, 20, 30, 5), nabiz(halka(600, 245, 36), MOR, 16, 20, 30, 4),
         nabiz(halka(960, 245, 16), TURUNCU, 30, 20, 30, 4),
         iz('M200 600 L1120 600', GRI, 5, 44, 60, 40),
         iz('M260 506 L1060 506', MAVI, 12, 60, 80, 35), isaretci('M260 506 L1060 506', MAVI, 60, 80, 7),
         iz('M210 536 C 230 530 250 542 260 536', MOR, 10, 60, 100, 45),
         iz('M200 580 L222 580', TURUNCU, 12, 60, 130, 45)]
    return k + _serit([(30, 650, 260, 74), (324, 650, 260, 74), (617, 650, 260, 74), (910, 650, 260, 74)],
                      (MAVI, MOR, TURUNCU, GRI), 134, 10, ['M292 687 L320 687', 'M586 687 L614 687', 'M880 687 L908 687'])


def r10():
    k = [nabiz(halka(100, 292, 34), KIRMIZI, 4, 20, 35, 5),
         iz('M134 296 C 300 290 450 300 600 296', MAVI, 8, 20, 50, 35),
         nabiz(halka(330, 292, 18), TURUNCU, 46, 20, 40, 4),
         nabiz(rc(470, 296, 50, 30, 10), MOR, 66, 20, 40, 4),
         nabiz(rc(935, 300, 82, 40, 6), KIRMIZI, 92, 20, 40, 4),
         nabiz(halka(935, 326, 18), '#991b1b', 108, 20, 40, 4)]
    return k + _serit(SERIT4, (KIRMIZI, TURUNCU, MOR, '#991b1b'), 128, 10, OK4)


def r11():
    k = [nabiz(halka(110, 210, 42), MAVI, 2, 18, 30, 4)]
    for i, y in enumerate((222, 252, 282, 312)):
        k.append(nabiz(halka(182, y, 9), MAVI, 12 + i * 8, 14, 40, 4))
    k += [nabiz(halka(540, 440, 12), MAVI, 40, 18, 35, 4),
          nabiz(halka(110, 420, 18), TURUNCU, 54, 18, 30, 4),
          nabiz(halka(182, 442, 9), TURUNCU, 62, 14, 40, 4), nabiz(halka(182, 472, 9), TURUNCU, 70, 14, 40, 4)]
    for i, (x, y) in enumerate(((824, 400), (1026, 400), (887, 546), (963, 546))):
        k.append(nabiz(halka(x, y, 20), MOR, 88 + i * 8, 20, 40, 4))
    return k + _serit(SERIT3, (MAVI, TURUNCU, MOR), 130, 12, OK3)


def r12():
    d = 'M1130 360 C 1090 340 1070 280 1060 220'
    return [nabiz(halka(190, 210, 32), MAVI, 4, 20, 25, 4),
            nabiz(rc(190, 548, 100, 14, 6), MAVI, 10, 20, 25, 3),
            nabiz(halka(532, 214, 32), KIRMIZI, 34, 20, 35, 4),
            iz('M560 230 C 600 260 600 320 570 360', KIRMIZI, 9, 44, 64, 55),
            iz(d, MAVI, 10, 74, 96, 40), isaretci(d, MAVI, 74, 96, 7, False),
            nabiz(halka(1030, 214, 28), KIRMIZI, 94, 20, 40, 4),
            iz('M940 260 C 980 220 1020 210 1060 220', MAVI, 8, 100, 112, 45),
            nabiz(yol('M872 238 C 856 260 904 260 888 238 C 892 270 868 270 872 238 Z'), KIRMIZI, 110, 20, 40, 4),
            *_serit(SERIT4, (MAVI, KIRMIZI, KIRMIZI, MOR), 128, 10, OK4)]


PLAN = {f'r{i:02d}': globals()[f'r{i:02d}'] for i in range(1, 13)}
