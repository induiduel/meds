"""k2-38 Travma ve Stres Bağlantılı Bozukluklar — ara resim Lottie hareket planı (koordinatlar SVG kaynağından)."""
from lottie_uret import *  # noqa: F401,F403
from lottie_plan.k2_16 import yol, iz, isaretci  # göreli/Q/A/S yolu çeviren sarmalayıcılar


def elips(cx, cy, rx, ry, pay=6):
    return el(cx, cy, 2 * (rx + pay), 2 * (ry + pay))


def maddeler(x, ys, h, t0, ara=8):
    return [nabiz(halka(x, y, 9), h, t0 + i * ara, 14, 40, 3) for i, y in enumerate(ys)]


Y5 = (458.35, 488.35, 518.35, 548.35, 578.35)


def r01():
    eks = 'M90 300 L1130 300'
    k = [iz(eks, GRI, 6, 0, 120, 35), isaretci(eks, KIRMIZI, 0, 120, 8)]
    for i, (d, h, t) in enumerate((('M95,270 Q170,210 245,270', YESIL, 6), ('M255,270 Q407,150 555,270', TURUNCU, 30),
                                   ('M565,270 Q710,150 855,270', KIRMIZI, 64), ('M865,270 Q1000,150 1120,270', '#991b1b', 94))):
        k.append(iz(d, h, 12, t, t + 24, 40))
    k += maddeler(80, Y5, MOR, 124) + maddeler(640, Y5, MAVI, 128)
    return k


def r02():
    kos = 'M420,290 Q320,250 200,262'
    yolu = 'M660,330 C760,250 900,380 1120,260'
    k = [nabiz(halka(530, 272, 18), KIRMIZI, 2, 18, 30, 4),
         iz(kos, KIRMIZI, 10, 8, 30, 45), isaretci(kos, KIRMIZI, 8, 30, 7, False),
         nabiz(yol('M140,398 C110,376 126,354 140,370 C154,354 170,376 140,398 Z'), KIRMIZI, 30, 16, 40, 5),
         katman('kalp', [G(yol('M140,398 C110,376 126,354 140,370 C154,354 170,376 140,398 Z'), st(KIRMIZI, 4, 90))],
                o=K((0, 0), (46, 0), (50, 90), (54, 0), (58, 90), (62, 0))),
         iz(yolu, TURUNCU, 12, 66, 100, 35), isaretci(yolu, MOR, 66, 100, 8),
         nabiz(yol('M860,248.1 C846.5,238.2 853.7,228.3 860,235.5 C866.3,228.3 873.5,238.2 860,248.1 Z'), KIRMIZI, 86, 16, 40, 5)]
    for i, cx in enumerate((180, 445, 715, 1005)):
        k.append(nabiz(elips(cx, 610, 120, 36), (MOR, TURUNCU, TURUNCU, KIRMIZI)[i], 110 + i * 14, 18, 30, 4))
        if i < 3:
            k.append(iz(('M302,610 L321,610', 'M567,610 L591,610', 'M837,610 L881,610')[i], GRI, 7, 120 + i * 14, 126 + i * 14, 60))
    return k


def r03():
    k = [nabiz(halka(600, 330, 101), MOR, 2, 22, 30, 5)]
    for i, (d, cx, cy) in enumerate((('M515,290 Q420,250 375,215', 200, 170), ('M685,290 Q780,250 825,215', 1000, 170),
                                     ('M600,425 Q600,445 600,462', 600, 560))):
        t = 22 + i * 26
        k += [iz(d, MOR, 9, t, t + 12, 55), nabiz(elips(cx, cy, 190, 95), (MAVI, TURUNCU, KIRMIZI)[i], t + 10, 20, 30, 4)]
    ys = (384.05, 414.05, 444.05, 474.05, 504.05)
    k += maddeler(56, ys, GRI, 110, 7) + maddeler(846, ys[:4], KIRMIZI, 116, 7)
    k.append(nabiz(halka(846, 414.05, 12), KIRMIZI, 150, 20, 50, 4))  # intihar riski
    return k


def r04():
    k = [nabiz(kutu(40, 80, 360, 200, 14), YESIL, 4, 22, 25),
         iz('M402,180 Q436,150 466,180', GRI, 8, 26, 36, 60),
         nabiz(kutu(470, 80, 360, 200, 14), MAVI, 34, 22, 25),
         nabiz(kutu(880, 80, 280, 200, 14), TURUNCU, 58, 22, 25),
         iz('M1020,284 Q1020,320 960,330', TURUNCU, 7, 72, 82, 60)]
    for i, (x, y, h) in enumerate(((250, 470, YESIL), (680, 505, MAVI), (1080, 540, MOR))):
        t = 90 + i * 20
        k += [iz(f'M80,{y} H{x}', h, 12, t, t + 12 + i * 10, 40)]
    k.append(isaretci('M80 590 L1080 590', MOR, 90, 150, 7))
    return k


def r05():
    k = [iz('M420,250 C480,210 540,290 600,250 C660,210 720,290 780,250', MAVI, 9, 2, 30, 50),
         nabiz(halka(690, 205, 30), MAVI, 26, 20, 30, 4),
         iz('M470,330 Q350,380 300,420', TURUNCU, 9, 46, 62, 55),
         nabiz(kutu(40, 420, 520, 250, 14), TURUNCU, 58, 22, 25)]
    ys = (473.35, 507.35, 541.35, 575.35, 609.35)
    k += maddeler(60, ys, TURUNCU, 70, 6)
    k += [iz('M730,330 Q850,380 900,420', KIRMIZI, 9, 104, 120, 55), nabiz(kutu(640, 420, 520, 250, 14), KIRMIZI, 116, 22, 25)]
    k += maddeler(660, ys, KIRMIZI, 128, 6)
    return k


def r06():
    k = [iz('M110,140 Q110,220 112,300', MOR, 9, 2, 20, 55),
         nabiz(halka(110, 330, 16), MOR, 16, 18, 40, 4),
         iz('M110,326 C250,326 330,160 430,160', TURUNCU, 12, 26, 56, 40),
         nabiz(halka(430, 330, 16), TURUNCU, 50, 18, 40, 4),
         iz('M430,160 L700,160', TURUNCU, 12, 56, 80, 40),
         nabiz(halka(700, 330, 16), YESIL, 78, 18, 40, 4),
         iz('M700,160 C820,160 900,326 1020,326', YESIL, 12, 84, 114, 40),
         nabiz(halka(1020, 330, 16), YESIL, 110, 18, 40, 4)]
    ys = (483.35, 517.35, 551.35, 585.35, 619.35)
    return k + maddeler(60, ys, MOR, 124, 6) + maddeler(640, ys, KIRMIZI, 132, 6)


def r07():
    k = [nabiz(yol('M150,95 L1050,95 Q860,300 720,470 L480,470 Q340,300 150,95 Z'), GRI, 0, 20, 20, 4)]
    elipsler = [(360, 140), (600, 140), (840, 140), (450, 215), (750, 215), (480, 290), (720, 290), (600, 370)]
    for i, (cx, cy) in enumerate(elipsler):
        t = 16 + i * 12
        h = (MAVI, MAVI, MAVI, MAVI, KIRMIZI, MOR, KIRMIZI, MOR)[i]
        k.append(nabiz(elips(cx, cy, 108, 27, 4), h, t, 16, 0, 4))
        if i == 4:
            k.append(iz('M1010,280 Q930,230 862,220', KIRMIZI, 7, t, t + 10, 60))
        if i == 6:
            k.append(iz('M1000,410 Q900,360 830,300', KIRMIZI, 7, t, t + 10, 60))
    k += [iz('M600,500 L600,560', YESIL, 9, 120, 134, 60), isaretci('M600 420 L600 560', YESIL, 110, 134, 8, False),
          nabiz(elips(600, 610, 250, 45), YESIL, 132, 26, 40, 5)]
    return k


PLAN = {f'r{i:02d}': globals()[f'r{i:02d}'] for i in range(1, 8)}
