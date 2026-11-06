"""k2-18 Bazal Gangliyonlar ve Ekstrapiramidal Sistem — ara resim Lottie hareket planı (koordinatlar SVG kaynağından)."""
import re
from pathlib import Path

from lottie_uret import *  # noqa: F401,F403  yapı taşları + renkler

_SVG = Path(__file__).resolve().parents[3] / 'public' / 'ara_resim' / 'k2-18-bazal-gangliyonlar-ve-ekstrapiramidal-sistem'


def q(d):
    """Mutlak M/Q/L yolu → M/C/L (lottie_dsl Q bilmez)."""
    tok = re.findall(r'[MQLC]|-?\d*\.?\d+', d)
    out, i, cmd, P = [], 0, None, None
    while i < len(tok):
        t = tok[i]
        if t in 'MQLC':
            cmd = t; i += 1; continue
        if cmd == 'M':
            P = (float(tok[i]), float(tok[i + 1])); i += 2; out.append(f'M{P[0]} {P[1]}'); cmd = 'L'
        elif cmd == 'L':
            P = (float(tok[i]), float(tok[i + 1])); i += 2; out.append(f'L{P[0]} {P[1]}')
        elif cmd == 'C':
            out.append('C' + ' '.join(tok[i:i + 6])); P = (float(tok[i + 4]), float(tok[i + 5])); i += 6
        elif cmd == 'Q':
            c = (float(tok[i]), float(tok[i + 1])); e = (float(tok[i + 2]), float(tok[i + 3])); i += 4
            c1 = (P[0] + 2 / 3 * (c[0] - P[0]), P[1] + 2 / 3 * (c[1] - P[1]))
            c2 = (e[0] + 2 / 3 * (c[0] - e[0]), e[1] + 2 / 3 * (c[1] - e[1]))
            out.append(f'C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {e[0]} {e[1]}'); P = e
    return ' '.join(out)


def svg_yol(rid, bas):
    """SVG'deki uzun çizgi yolunu (ör. hareket izi) başlangıcından bulup getirir."""
    s = (_SVG / f'{rid}.svg').read_text()
    return re.search(r'd="(' + re.escape(bas) + r'[^"]*)"', s).group(1)


def ov(cx, cy, rx, ry, pay=6):
    return el(cx, cy, 2 * (rx + pay), 2 * (ry + pay))


def r01():
    k = []
    for i, d in enumerate(('M120,222 Q110,308 120,395', 'M280,222 Q267,331 280,440', 'M430,222 Q413,364 430,505')):
        p = q(d); t = 4 + i * 16
        k += [iz(p, KIRMIZI, 12, t, t + 22, 35), isaretci(p, KIRMIZI, t, t + 22, 8, False)]
    k += [nabiz(ov(120, 422, 60, 24), GRI, 26, 20, 25), nabiz(ov(280, 467, 72, 24), GRI, 42, 20, 25),
          nabiz(ov(430, 532, 72, 22), GRI, 58, 20, 25)]
    a = [q('M700,222 Q700,245 708,266'), q('M770,325 Q809,348 830,388'), q('M880,372 Q898,298 880,224')]
    b = [q('M1060,222 Q1059,249 1068,274'), q('M1020,345 Q983,364 962,400'), q('M880,372 Q898,298 880,224')]
    for j, (yollar, h, t0, dur) in enumerate(((a, MAVI, 78, (720, 300, 78, 32)), (b, MOR, 118, (1075, 315, 66, 38)))):
        k.append(iz(yollar[0], h, 12, t0, t0 + 8, 35))
        k.append(nabiz(ov(*dur), h, t0 + 6, 18, 25))
        k.append(iz(yollar[1], h, 12, t0 + 12, t0 + 22, 35))
        k.append(nabiz(ov(890, 410, 74, 36), YESIL, t0 + 20, 16, 20))
        k += [iz(yollar[2], YESIL if j == 0 else MOR, 12, t0 + 24, t0 + 34, 30)]
        for p, s in zip(yollar, (0, 12, 24)):
            k.append(isaretci(p, h, t0 + s, t0 + s + 10, 8, False))
    for i, x in enumerate((720, 890, 1060)):
        k.append(nabiz(halka(x, 775, 22), '#b45309', 150 + i * 8, 16, 30))
    return k


def r02():
    k = []
    for i, (x, h) in enumerate(((140, KIRMIZI), (365, YESIL), (590, '#d97706'), (815, MAVI), (1040, MOR))):
        t = 4 + i * 26
        k.append(nabiz(yol(f'M{x - 14} 178 L{x - 14} 200 C{x - 62} 205 {x - 62} 295 {x} 305 C{x + 62} 295 {x + 62} 205 {x + 14} 200 L{x + 14} 178 Z'), h, t, 22, 20))
        for dx in (-18, 0, 18):
            k.append(gecis(x + dx, 322, x + dx, 342, h, t + 8, t + 20, 5))
        if x == 590:
            k += [nabiz(halka(548, 425, 27), YESIL, t + 18, 18, 35), nabiz(halka(632, 425, 27), KIRMIZI, t + 22, 18, 35)]
        elif x != 1040:
            k.append(nabiz(halka(x, 410, 27), h, t + 18, 18, 35))
    k += [nabiz(halka(106, 700, 34), '#d97706', 140, 20, 30), nabiz(halka(548, 425, 31), YESIL, 150, 16, 0),
          nabiz(halka(632, 425, 31), KIRMIZI, 158, 16, 0)]
    return k


def r03():
    D, I, C = MAVI, '#d97706', YESIL
    k = [nabiz(ov(970, 180, 63, 24), '#b45309', 2, 18, 20), iz(q('M970,206 Q970,225 970,244'), GRI, 8, 10, 18, 50),
         nabiz(ov(970, 270, 111, 24), D, 16, 20, 30),
         nabiz(ov(300, 370, 44, 78), D, 18, 20, 30), nabiz(ov(478, 262, 28, 40), D, 22, 20, 30)]
    pd = q('M905,294 Q883,371 915,444')
    k += [iz(pd, D, 12, 44, 66, 35), isaretci(pd, D, 44, 66, 8, False),
          nabiz(ov(970, 470, 116, 24), KIRMIZI, 64, 20, 30), nabiz(ov(392, 392, 16, 44), KIRMIZI, 66, 20, 35),
          nabiz(ov(458, 532, 46, 12), KIRMIZI, 70, 20, 35)]
    p1, p2 = q('M1000,294 Q1025,315 1040,344'), q('M1040,396 Q1030,424 1010,446')
    k += [iz(p1, I, 12, 86, 96, 35), isaretci(p1, I, 86, 96, 8, False),
          nabiz(ov(1050, 370, 74, 24), I, 94, 18, 30), nabiz(ov(358, 382, 20, 56), I, 96, 18, 35),
          nabiz(ov(482, 496, 24, 12), I, 100, 18, 35),
          iz(p2, I, 12, 106, 116, 35), isaretci(p2, I, 106, 116, 8, False)]
    po = q('M970,494 Q970,519 970,544')
    ret = 'M1032 565 C1185 520 1185 210 1040 182'
    k += [iz(po, GRI, 8, 124, 132, 50), nabiz(ov(970, 570, 63, 24), C, 130, 18, 30), nabiz(ov(520, 405, 62, 56), C, 132, 18, 30),
          iz(ret, C, 10, 138, 166, 35), isaretci(ret, C, 138, 166, 8)]
    return k


def r04():
    R, Y = KIRMIZI, YESIL
    k = []
    a = q('M195,494 Q193,513 195,532')
    k += [nabiz(ov(195, 470, 74, 22), R, 2, 20, 30), iz(a, R, 14, 8, 22, 35), isaretci(a, R, 8, 22, 8, False),
          nabiz(ov(195, 560, 63, 22), Y, 20, 20, 25)]
    # B · direkt
    s = [(q('M580,192 Q580,209 580,226'), GRI, 6), (q('M580,274 Q572,358 580,442'), R, 14), (q('M580,494 Q578,514 580,534'), R, 4)]
    t = 44
    for p, h, w in s:
        dur = 10 if w > 6 else 6
        k += [iz(p, h, w + 6, t, t + dur, 35), isaretci(p, h, t, t + dur, 7, False)]
        t += dur + 2
    k += [nabiz(ov(580, 560, 63, 22), Y, t, 18, 35)]
    ret = 'M642 554 C745 520 745 230 660 188'
    k += [iz(ret, Y, 12, t + 6, t + 26, 35), isaretci(ret, Y, t + 6, t + 26, 8)]
    # C · indirekt
    s = [(q('M1040,192 Q1040,209 1040,226'), GRI, 6), (q('M1040,274 Q1039,285 1040,296'), R, 12),
         (q('M1040,344 Q1039,358 1040,371'), R, 4), (q('M1040,419 Q1039,432 1040,446'), Y, 12), (q('M1040,494 Q1038,513 1040,532'), R, 16)]
    t = 104
    for i, (p, h, w) in enumerate(s):
        k += [iz(p, h, w + 6, t, t + 6, 35), isaretci(p, h, t, t + 6, 7, False)]
        if i == 1: k.append(nabiz(ov(1040, 320, 42, 22), '#d97706', t + 4, 14, 20))
        if i == 3: k.append(nabiz(ov(1040, 395, 42, 22), '#d97706', t - 2, 14, 30))
        t += 9
    k += [nabiz(ov(1040, 470, 74, 22), R, t - 6, 18, 35), nabiz(ov(1040, 560, 63, 22), R, t + 4, 18, 30)]
    return k


def r05():
    c = 'M150 212 C140 330 130 420 135 492'
    kop = 'M142 350 C220 350 270 380 312 402'
    pr = 'M590 212 C590 300 560 370 506 398'
    dz = 'M474 580 C640 570 690 330 330 206'
    ist = 'M930 280 C990 250 1050 270 1100 330'
    return [iz(c, '#0f172a', 10, 4, 30, 30), isaretci(c, GRI, 4, 30, 8, False),
            iz(kop, MAVI, 10, 22, 44, 35), isaretci(kop, MAVI, 22, 44, 8, False),
            iz(pr, MOR, 10, 40, 62, 35), isaretci(pr, MOR, 40, 62, 8, False),
            nabiz(ov(410, 410, 96, 40), MAVI, 62, 22, 30),
            iz(q('M410,502 Q410,527 410,552'), GRI, 8, 80, 88, 50), nabiz(ov(410, 580, 64, 26), YESIL, 86, 18, 30),
            iz(dz, YESIL, 12, 94, 126, 35), isaretci(dz, YESIL, 94, 126, 8),
            iz(ist, YESIL, 13, 132, 156, 35), isaretci(ist, YESIL, 132, 156, 8),
            nabiz(kutu(958, 428, 84, 46), KIRMIZI, 152, 20, 30)]


def r06():
    j1, j2 = 'M121 312 C70 230 110 170 160 166', 'M178 176 C260 250 240 380 160 432'
    k = [nabiz(halka(121, 312, 14), KIRMIZI, 2, 14, 20), iz(j1, KIRMIZI, 7, 4, 14, 45), isaretci(j1, KIRMIZI, 4, 14, 7, False),
         nabiz(halka(170, 168, 14), KIRMIZI, 14, 14, 20), iz(j2, KIRMIZI, 7, 18, 28, 45), isaretci(j2, KIRMIZI, 18, 28, 7, False),
         nabiz(halka(150, 440, 14), KIRMIZI, 28, 14, 20), nabiz(halka(200, 205, 14), KIRMIZI, 34, 14, 20)]
    kore = svg_yol('r06', 'M62.0,580.0')
    k += [iz(kore, KIRMIZI, 9, 40, 70, 40), isaretci(kore, KIRMIZI, 40, 70, 8)]
    for i, d in enumerate(('M775 335 C735 300 780 270 755 240', 'M795 335 C767 300 812 270 787 240',
                           'M815 335 C801 300 846 270 821 240', 'M835 335 C833 300 878 270 853 240')):
        k.append(iz(d, MOR, 18, 80 + i * 8, 100 + i * 8, 25))
    k += [iz('M720 250 C700 300 720 350 700 400', MOR, 7, 84, 120, 45), iz('M920 260 C950 300 925 350 950 400', MOR, 7, 90, 126, 45)]
    at = svg_yol('r06', 'M642.0,580.0')
    k += [iz(at, MOR, 9, 110, 170, 40), isaretci(at, MOR, 110, 170, 8)]
    return k


def r07():
    t = 'M80 250 L1120 250'
    k = [nabiz(halka(90, 250, 16), KIRMIZI, 2, 20, 35), iz(t, GRI, 10, 6, 110, 30), isaretci(t, GRI, 6, 110, 9),
         nabiz(halka(1040, 250, 16), MOR, 100, 20, 35)]
    for i, (x, y) in enumerate(((244, 500), (236, 535), (272, 566), (190, 612))):
        k.append(nabiz(halka(x, y, 12), KIRMIZI, 24 + i * 12, 18, 35))
    k += [iz(q('M866,560 Q876,568 866,576 Q856,584 866,592'), MOR, 8, 116, 136, 45),
          iz('M880 548 C910 540 920 560 900 572', MOR, 7, 124, 140, 45), iz('M880 590 C915 596 920 616 896 620', MOR, 7, 132, 148, 45),
          nabiz(halka(866, 576, 30), MOR, 146, 20, 25)]
    return k


def r08():
    ust = 'M110 296 C170 270 280 270 340 292 C280 302 170 302 110 296 Z'
    alt = 'M110 344 C170 360 280 360 340 346 C280 334 170 334 110 344 Z'
    k = []
    for ad, d, faz in (('kas1', ust, 0), ('kas2', alt, 12)):
        kp = [(0, 0)]
        for b in range(4):
            t0 = 4 + faz + b * 24
            kp += [(t0, 0), (t0 + 6, 90), (t0 + 12, 0)]
        kp.append((110, 0))
        k.append(katman(ad, [G(yol(d), st(KIRMIZI, 5, 100))], o=K(*kp)))
    k.append(nabiz(kutu(462, 266, 52, 110), GRI, 8, 90, 20, 3))
    s1, s2 = svg_yol('r08', 'M602.0,250.0'), svg_yol('r08', 'M602.0,430.0')
    k += [iz(s1, MAVI, 8, 30, 80, 40), isaretci(s1, MAVI, 30, 80, 7),
          iz(s2, MOR, 8, 84, 134, 40), isaretci(s2, MOR, 84, 134, 7),
          nabiz(halka(1130, 430, 18), MOR, 130, 18, 30),
          nabiz(halka(252, 640, 16), '#b45309', 140, 18, 35), nabiz(kutu(540, 636, 54, 104), '#b45309', 152, 18, 25)]
    return k


def r09():
    f = 'M330 400 C470 380 520 300 470 190'
    g = 'M330 430 C430 470 520 430 560 330'
    return [nabiz(halka(292, 238, 18), KIRMIZI, 2, 22, 40),
            nabiz(rc(290, 395, 92, 512, 10), KIRMIZI, 10, 22, 15, 3),
            iz(f, KIRMIZI, 10, 30, 46, 40), isaretci(f, KIRMIZI, 30, 46, 9, False),
            iz(g, KIRMIZI, 9, 50, 66, 40), isaretci(g, KIRMIZI, 50, 66, 9, False),
            nabiz(halka(560, 250, 26), '#b45309', 62, 20, 30),
            iz('M860 250 C820 230 780 240 732 250', KIRMIZI, 10, 90, 106, 40), nabiz(rc(720, 255, 26, 168, 6), GRI, 104, 18, 30),
            iz(q('M780,420 Q810,400 840,420 Q870,400 900,420 Q930,400 960,420'), KIRMIZI, 9, 124, 150, 40),
            nabiz(kutu(720, 430, 420, 30, 6), GRI, 146, 18, 25)]


def r10():
    k = []
    for i, y in enumerate((460, 380, 300)):
        on = f'M150 {y} C160 {y + 26} 240 {y + 26} 250 {y}'
        ark = f'M250 {y} C240 {y - 18} 160 {y - 18} 150 {y}'
        t = 4 + i * 22
        k += [iz(on, MOR, 10, t, t + 10, 40), iz(ark, MOR, 6, t + 10, t + 18, 35), isaretci(on + ' ' + ark[ark.index('C'):], MOR, t, t + 18, 7, False)]
    k.append(nabiz(rc(200, 380, 300, 300, 30), MOR, 72, 20, 0, 3))
    scm = 'M772 318 C780 360 795 400 812 436'
    don = 'M800 170 C850 140 900 160 910 210'
    k += [iz(scm, KIRMIZI, 16, 92, 112, 40), nabiz(halka(788, 380, 12), KIRMIZI, 108, 16, 30),
          iz(don, '#0f172a', 9, 116, 136, 35), isaretci(don, GRI, 116, 136, 8),
          iz('M1100 470 C1110 440 1100 410 1080 395', '#0f172a', 8, 144, 162, 35), isaretci('M1100 470 C1110 440 1100 410 1080 395', GRI, 144, 162, 7)]
    return k


PLAN = {f'r{i:02d}': fn for i, fn in enumerate((r01, r02, r03, r04, r05, r06, r07, r08, r09, r10), 1)}
