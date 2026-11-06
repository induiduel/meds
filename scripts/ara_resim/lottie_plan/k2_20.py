"""k2-20 Psikiyatrik Bozukluklarda Uygulanan Tedaviler — ara resim Lottie hareket planı (koordinatlar SVG kaynağından)."""
import re
from pathlib import Path

from lottie_uret import *  # noqa: F401,F403  yapı taşları + renkler
from lottie_plan.k2_18 import q, ov  # Q→C çevirici, elips halkası

_SVG = Path(__file__).resolve().parents[3] / 'public' / 'ara_resim' / 'k2-20-psikiyatrik-bozukluklarda-uygulanan-tedaviler'


def svg_yol(rid, bas):
    s = (_SVG / f'{rid}.svg').read_text()
    return re.search(r'd="(' + re.escape(bas) + r'[^"]*)"', s).group(1)


def yay(cx, cy, rx, ry):
    """Soldan sağa üst yarım elips (SVG A yayının kübik karşılığı)."""
    k = .5523
    return (f'M{cx - rx} {cy} C{cx - rx} {cy - ry * k} {cx - rx * k} {cy - ry} {cx} {cy - ry} '
            f'C{cx + rx * k} {cy - ry} {cx + rx} {cy - ry * k} {cx + rx} {cy}')


def r01():
    k = [nabiz(ov(80, 250, 16, 11), TURUNCU, 2, 16, 30), nabiz(ov(340, 250, 16, 11), TURUNCU, 2, 16, 30)]
    for i, (rx, ry) in enumerate(((40, 32), (75, 60), (110, 88))):
        k.append(iz(yay(210, 330, rx, ry), '#c2410c', 7, 12 + i * 10, 26 + i * 10, 55))
    k.append(nabiz(yol('M84 362 C63 288 126 225 210 225 C304 220 357 278 346 340 C344 382 304 404 252 395 C220 414 178 409 147 393 C105 404 79 388 84 362 z'), '#be123c', 44, 22, 25))
    k.append(nabiz(yol('M450 170 C450 140 560 140 560 170 L560 250 C560 280 450 280 450 250 z'), MAVI, 64, 18, 25))
    k.append(gecis(505, 272, 505, 306, '#c2410c', 70, 84, 6))
    k.append(iz('M440 330 C480 300 530 300 570 330', MAVI, 10, 80, 96, 40))
    for i, x in enumerate((465, 505, 545)):
        k.append(nabiz(rc(x, 320 if x != 505 else 314, 24, 26, 5), '#c2410c', 90 + i * 4, 14, 30, 4))
    for i, d in enumerate(('M940 302 C910 270 880 250 850 240', 'M980 300 C1000 260 1030 240 1060 230',
                           'M940 340 C905 370 880 395 860 420', 'M985 335 C1020 360 1045 385 1080 400')):
        k.append(iz(d, MOR, 8, 110 + i * 5, 126 + i * 5, 40))
    k += [nabiz(halka(960, 320, 32), MOR, 106, 18, 30),
          iz('M1060 230 C1090 215 1110 230 1120 250', YESIL, 7, 134, 146, 60)]
    k += [iz('M70 640 C250 610 450 670 640 640', KIRMIZI, 12, 146, 166, 35), iz('M70 680 C250 650 450 710 640 680', KIRMIZI, 12, 146, 166, 35)]
    for i, x in enumerate((240, 330, 420)):
        k.append(gecis(x, 650, x, 712, '#c2410c', 150 + i * 6, 172 + i * 2, 6))
    return k


def r02():
    k = [nabiz(yol('M245 140 C300 140 330 180 330 225 C330 275 300 300 245 300 C190 300 160 275 160 225 C160 180 190 140 245 140 z'), KIRMIZI, 4, 22, 25),
         nabiz(rc(245, 395, 250, 90, 20), KIRMIZI, 18, 22, 15, 4), nabiz(rc(245, 550, 260, 110, 20), KIRMIZI, 30, 22, 15, 4)]
    for i, (x1, y1, y2) in enumerate(((245, 215, 160), (330, 400, 360), (330, 560, 520))):
        k.append(iz(f'M{x1} {y1} L{x1} {y2}', '#b91c1c', 8, 4 + i * 12, 16 + i * 12, 55))
    kalp = 'M228 420 C210 395 180 405 185 430 C190 455 228 475 228 475 C228 475 266 455 271 430 C276 405 246 395 228 420 z'
    kp = [(0, 0)]
    for b in range(3):
        t0 = 50 + b * 14
        kp += [(t0, 0), (t0 + 5, 95), (t0 + 12, 20)]
    k.append(katman('kalp', [G(yol(kalp), st(KIRMIZI, 6, 100))], o=K(*kp)))
    for i in range(7):
        k.append(nabiz(halka(515, 164 + 68 * i, 21), '#c2410c', 96 + i * 9, 14, 30))
    k += [iz('M1080 505 C1080 470 1120 455 1135 480 C1150 505 1125 535 1100 530', KIRMIZI, 8, 150, 166, 50)]
    return k


def r03():
    ekt = 'M100 470 C150 470 170 290 210 285 C250 280 260 470 300 470'
    k = [iz(ekt, '#c2410c', 10, 4, 40, 40), isaretci(ekt, '#c2410c', 4, 40, 8),
         nabiz(halka(174, 330, 13), YESIL, 18, 18, 40), nabiz(halka(246, 330, 13), YESIL, 30, 18, 40),
         iz('M80 230 L560 230', MOR, 8, 48, 74, 55)]
    n1, n2 = q(svg_yol('r03', 'M630 230')), q(svg_yol('r03', 'M630 360'))
    k += [iz(n1, '#c2410c', 8, 84, 110, 40), isaretci(n1, '#c2410c', 84, 110, 7, False),
          iz(n2, KIRMIZI, 8, 112, 158, 40), isaretci(n2, KIRMIZI, 112, 158, 7),
          nabiz(yol('M95 640 C77 615 47 625 52 650 C57 675 95 695 95 695 C95 695 133 675 138 650 C143 625 113 615 95 640 z'), KIRMIZI, 160, 18, 35)]
    return k


def r04():
    k = [nabiz(halka(278, 190, 34), MAVI, 4, 18, 30), nabiz(halka(342, 190, 34), MAVI, 4, 18, 30),
         nabiz(yol(q('M240,262 Q310,330 380,262') + ' Z'), MAVI, 22, 22, 40),
         iz('M460 255 L460 320', '#0f172a', 6, 30, 44, 60),
         nabiz(ov(265, 500, 30, 22), GRI, 50, 18, 25), nabiz(ov(355, 500, 30, 22), GRI, 50, 18, 25)]
    h = 'M675 470 C655 290 765 195 890 195 C1015 195 1125 290 1105 470'
    k += [iz(h, MAVI, 12, 80, 110, 35), isaretci(h, MAVI, 80, 110, 8, False),
          nabiz(yol('M715 440 C700 330 780 255 890 255 C1000 255 1080 330 1065 440 L1000 440 C1005 375 960 390 890 390 C820 390 775 375 780 440 Z'), MAVI, 110, 24, 40),
          iz('M890 255 L890 390', '#0f172a', 6, 120, 136, 60),
          nabiz(ov(845, 500, 30, 22), MAVI, 140, 18, 30), nabiz(ov(935, 500, 30, 22), MAVI, 140, 18, 30)]
    return k


def r05():
    an, ka = 'M155 272 C140 400 190 470 215 510', 'M325 272 C340 400 290 470 265 510'
    k = [nabiz(kutu(200, 510, 80, 80, 10), GRI, 2, 16, 25),
         iz(an, KIRMIZI, 7, 8, 28, 50), isaretci('M215 510 C190 470 140 400 155 272', KIRMIZI, 8, 28, 6, False),
         nabiz(ov(155, 250, 34, 22), KIRMIZI, 26, 18, 35),
         iz(ka, MAVI, 7, 30, 50, 50), isaretci(ka, MAVI, 30, 50, 6, False),
         nabiz(ov(325, 250, 34, 22), MAVI, 48, 18, 35)]
    a = 'M560 400 L700 400 C730 400 740 300 780 300 L1100 300'
    b = 'M560 400 L700 400 C730 400 740 490 780 490 L1100 490'
    k += [iz(a, KIRMIZI, 10, 70, 120, 40), isaretci(a, KIRMIZI, 70, 120, 8),
          iz(b, MAVI, 10, 100, 150, 40), isaretci(b, MAVI, 100, 150, 8),
          iz('M520 230 L1130 230', '#0f172a', 5, 150, 172, 45)]
    return k


def r06():
    yaz = 'M70 450 C170 250 260 200 330 200 C400 200 470 260 560 450'
    kis = 'M110 450 C190 340 250 310 310 310 C370 310 430 340 510 450'
    mel = 'M650 430 C720 430 760 250 840 230 C900 215 930 380 990 425 C1030 432 1100 430 1130 430'
    return [iz(yaz, '#f59e0b', 10, 4, 40, 40), isaretci(yaz, '#f59e0b', 4, 40, 9, False),
            iz(kis, GRI, 10, 44, 76, 40), isaretci(kis, '#f59e0b', 44, 76, 9),
            iz(mel, MOR, 10, 86, 126, 40), isaretci(mel, MOR, 86, 126, 8),
            nabiz(halka(960, 330, 42), '#ca8a04', 126, 22, 40),
            iz('M925 330 L880 300', '#a16207', 7, 136, 146, 60)]


def r07():
    k = [nabiz(halka(120, 470, 18), '#0e7490', 2, 16, 30),
         iz('M300 470 L300 250', '#0e7490', 76, 14, 44, 30), iz('M460 470 L460 420', '#0e7490', 76, 48, 62, 30),
         iz('M520 330 C560 330 575 390 605 445', KIRMIZI, 8, 66, 84, 55)]
    k += [nabiz(yol('M816 328 C797 262 854 205 930 205 C1016 200 1063 252 1054 310 C1052 348 1016 366 968 359 C940 376 902 371 873 357 C835 366 811 352 816 328 z'), '#0e7490', 92, 22, 25),
          nabiz(halka(840, 250, 14), '#0e7490', 100, 16, 30),
          iz('M890 330 C900 300 950 295 965 320 C975 340 950 355 925 350', MOR, 7, 108, 124, 55)]
    for i, x in enumerate((90, 175, 260, 345, 430, 515)):
        k.append(nabiz(halka(x, 620, 22), MOR if x in (90, 345, 515) else '#ca8a04', 130 + i * 7, 14, 30))
    return k


PLAN = {'r01': r01, 'r02': r02, 'r03': r03, 'r04': r04, 'r05': r05, 'r06': r06, 'r07': r07}
