"""k2-16 Nörolojik Rehabilitasyona Giriş — ara resim Lottie hareket planı (koordinatlar SVG kaynağından)."""
from lottie_uret import *  # noqa: F401,F403
from lottie_uret import yol as _yol_ham, iz as _iz_ham, isaretci as _isr_ham, nabiz as _nb_ham  # noqa: E402
import math as _m
import re as _re


def mutlak(d):
    """Her SVG yolunu (göreli, Q, A, H, V) yalnız M/L/C/Z mutlak biçime çevirir (DSL yalnız bunları okur)."""
    tok = _re.findall(r'[MLHVCSQAZmlhvcsqaz]|-?\d*\.?\d+(?:e-?\d+)?', d)
    i, cmd, x, y, sx, sy, out = 0, None, 0.0, 0.0, 0.0, 0.0, []
    f = lambda: float(tok[i])
    while i < len(tok):
        t = tok[i]
        if t.isalpha():
            cmd = t; i += 1
            if cmd in 'Zz':
                out.append('Z'); x, y = sx, sy
            continue
        r = cmd.islower(); C = cmd.upper(); bx, by = (x, y) if r else (0, 0)
        n = lambda k: float(tok[i + k])
        if C == 'M':
            x, y = bx + n(0), by + n(1); i += 2; sx, sy = x, y; out.append(f'M{x:.1f} {y:.1f}'); cmd = 'l' if r else 'L'
        elif C == 'L':
            x, y = bx + n(0), by + n(1); i += 2; out.append(f'L{x:.1f} {y:.1f}')
        elif C == 'H':
            x = (x if r else 0) + n(0); i += 1; out.append(f'L{x:.1f} {y:.1f}')
        elif C == 'V':
            y = (y if r else 0) + n(0); i += 1; out.append(f'L{x:.1f} {y:.1f}')
        elif C == 'C':
            p = [n(k) + (bx if k % 2 == 0 else by) for k in range(6)]; i += 6
            out.append('C' + ' '.join(f'{v:.1f}' for v in p)); x, y = p[4], p[5]; lc = (p[2], p[3])
        elif C == 'S':
            px, py = (2 * x - lc[0], 2 * y - lc[1]) if out and out[-1][0] == 'C' else (x, y)
            p = [px, py] + [n(k) + (bx if k % 2 == 0 else by) for k in range(4)]; i += 4
            out.append('C' + ' '.join(f'{v:.1f}' for v in p)); x, y = p[4], p[5]; lc = (p[2], p[3])
        elif C == 'Q':
            qx, qy, ex, ey = bx + n(0), by + n(1), bx + n(2), by + n(3); i += 4
            c = [x + 2 / 3 * (qx - x), y + 2 / 3 * (qy - y), ex + 2 / 3 * (qx - ex), ey + 2 / 3 * (qy - ey), ex, ey]
            out.append('C' + ' '.join(f'{v:.1f}' for v in c)); x, y = ex, ey
        elif C == 'A':
            rx, ry, _, la, sw = n(0), n(1), n(2), int(n(3)), int(n(4)); ex, ey = bx + n(5), by + n(6); i += 7
            # yalnız döndürmesiz yay: merkez parametrelemesi
            dx, dy = (x - ex) / 2, (y - ey) / 2
            lam = (dx / rx) ** 2 + (dy / ry) ** 2
            if lam > 1: rx, ry = rx * _m.sqrt(lam), ry * _m.sqrt(lam)
            num = max(0, rx * rx * ry * ry - rx * rx * dy * dy - ry * ry * dx * dx)
            k = _m.sqrt(num / (rx * rx * dy * dy + ry * ry * dx * dx)) * (-1 if la == sw else 1)
            cx, cy = k * rx * dy / ry + (x + ex) / 2, -k * ry * dx / rx + (y + ey) / 2
            a0 = _m.atan2((y - cy) / ry, (x - cx) / rx); a1 = _m.atan2((ey - cy) / ry, (ex - cx) / rx)
            da = a1 - a0
            if sw and da < 0: da += 2 * _m.pi
            if not sw and da > 0: da -= 2 * _m.pi
            for j in range(1, 13):
                a = a0 + da * j / 12; out.append(f'L{cx + rx * _m.cos(a):.1f} {cy + ry * _m.sin(a):.1f}')
            x, y = ex, ey
    return ' '.join(out)


def yol(d):
    return _yol_ham(mutlak(d))


def iz(d, *a, **k):
    return _iz_ham(mutlak(d), *a, **k)


def isaretci(d, *a, **k):
    return _isr_ham(mutlak(d), *a, **k)


def _serit(kutular, renkler, t0=100, ara=20, oklar=()):
    """C paneli: alt kutular soldan sağa sırayla, aradaki oklar çizilerek."""
    k = []
    for i, (x, y, w, h) in enumerate(kutular):
        k.append(nabiz(kutu(x, y, w, h), renkler[i % len(renkler)], t0 + i * ara, 20, 25))
        if i < len(oklar):
            k.append(iz(oklar[i], GRI, 8, t0 + i * ara + 12, t0 + i * ara + 20, 55))
    return k


def r01():
    k = [nabiz(halka(171, 248, 24), KIRMIZI, 4, 24, 35),  # kopan distal falanks
         iz('M204 226 L150 180', KIRMIZI, 6, 10, 22, 60)]
    for i, y in enumerate((280, 370, 460)):
        t = 30 + i * 22
        k += [nabiz(halka(820, y, 17), (MAVI, MAVI, KIRMIZI)[i] if i < 2 else KIRMIZI, t, 20, 30),
              nabiz(halka(1050, y, 17), YESIL if i == 2 else MAVI, t + 6, 20, 30)]
    k.append(nabiz(halka(1050, 460, 17), YESIL, 100, 26, 45))  # piyanistte engellilik
    k += _serit([(60, 600, 320, 92), (440, 600, 320, 92), (820, 600, 320, 92)], (MAVI, TURUNCU, KIRMIZI), 120, 16,
                ['M384 646 L434 646', 'M764 646 L814 646'])
    return k


def r02():
    k = [nabiz(yol('M160 228 m-20 0 a20 52 0 1 0 40 0 a20 52 0 1 0 -40 0'), KIRMIZI, 4, 22, 30),
         iz('M236 420 A90 90 0 0 0 262 330', MAVI, 9, 20, 40, 50),
         iz('M300 300 L300 372', GRI, 8, 34, 46, 50),
         iz('M352 196 L336 246', KIRMIZI, 8, 44, 56, 50)]
    for i in range(6):
        y = 220 + i * 50
        t = 56 + i * 16
        k.append(nabiz(halka(530, y, 18), MAVI, t, 18, 30, 4))
        for j in range(min(i, 4)):
            x = 856 + j * 80
            k.append(iz(f'M{x} {y} L{x + 48} {y}', MAVI if (i, j) != (4, 3) else '#a5b4fc', 9, t + 3 + j * 3, t + 9 + j * 3, 45))
    return k


def r03():
    k = [nabiz(halka(160, 170, 40), MOR, 2, 20, 0, 3), nabiz(halka(310, 170, 34), MOR, 8, 20, 0, 3),
         nabiz(halka(460, 170, 40), MOR, 14, 20, 0, 3),
         iz('M310 198 C310 240 300 280 300 312', MOR, 10, 20, 40, 45)]
    a = 'M90 320 C130 290 190 290 240 344'
    b = 'M238 450 C180 480 130 470 90 430'
    k += [iz(a, MAVI, 10, 40, 60, 40), isaretci(a, MAVI, 40, 60, 7, False),
          iz(b, KIRMIZI, 10, 60, 80, 40), isaretci(b, KIRMIZI, 60, 80, 7, False)]
    for i, (x, y) in enumerate([(248, 434), (196, 304), (72, 408), (64, 348)]):
        k.append(nabiz(halka(x, y, 14), TURUNCU, 84 + i * 8, 18, 35, 4))
    k += [nabiz(yol('M928 190 m-12 0 a12 40 0 1 0 24 0 a12 40 0 1 0 -24 0 M970 190 m0 0 a12 40 0 1 0 24 0 a12 40 0 1 0 -24 0'), MAVI, 112, 18, 25, 3),
          nabiz(halka(940, 305, 30), TURUNCU, 124, 18, 35, 4),
          nabiz(yol('M918 420 a22 40 0 1 0 44 0 a22 40 0 1 0 -44 0 M960 420 a22 40 0 1 0 44 0 a22 40 0 1 0 -44 0'), KIRMIZI, 136, 18, 35, 4)]
    k += _serit([(60, 600, 340, 110), (430, 600, 340, 110), (800, 600, 340, 110)], (TURUNCU, KIRMIZI, MAVI), 148, 8)
    return k


def r05():
    c = 'M120 326 C180 326 190 280 230 260 S290 180 340 180 S410 200 450 210 S520 270 560 270 S630 300 670 300'
    k = [iz(c, KIRMIZI, 12, 6, 90, 35), isaretci(c, KIRMIZI, 6, 90, 8)]
    for i, (x, y) in enumerate([(230, 260), (340, 180), (560, 270)]):
        k.append(nabiz(halka(x, y, 12), KIRMIZI, [27, 46, 72][i], 18, 35, 4))
    k += [iz('M80 410 L160 410', GRI, 10, 8, 20, 50), iz('M180 410 L390 410', TURUNCU, 10, 26, 50, 50),
          iz('M400 410 L710 410', YESIL, 10, 56, 92, 50),
          iz('M450 488 L450 426', YESIL, 8, 60, 70, 60)]
    for i, x in enumerate((820, 940, 1060)):
        k.append(nabiz(halka(x, 230, 52), (GRI, KIRMIZI, YESIL)[i], 96 + i * 14, 20, 0, 3))
    k += _serit([(60, 598, 340, 112), (430, 598, 340, 112), (800, 598, 340, 112)], (MAVI, MAVI, MAVI), 140, 10)
    return k


def r06():
    k = [nabiz(halka(330, 320, 72), KIRMIZI, 2, 24, 25, 4)]
    p1 = 'M120 240 C200 260 260 280 280 300'
    p2 = 'M380 300 C420 280 480 250 520 230'
    p3 = 'M140 380 C220 420 400 420 470 340'
    k += [iz(p1, MAVI, 9, 14, 30, 50), isaretci(p1, MAVI, 14, 30, 7, False), nabiz(halka(200, 262, 13), MAVI, 26, 16, 35, 4),
          iz('M470 330 L600 372', YESIL, 9, 34, 50, 50), nabiz(halka(540, 350, 13), YESIL, 46, 16, 35, 4),
          iz(p3, TURUNCU, 9, 52, 76, 50), isaretci(p3, TURUNCU, 52, 76, 7, False), nabiz(halka(300, 438, 13), TURUNCU, 70, 16, 35, 4),
          nabiz(halka(600, 260, 70), MOR, 80, 20, 0, 3),
          katman('genis', [G(el(600, 260, 200, 120), st(MOR, 5, 60))], o=K((0, 0), (90, 0), (100, 80), (120, 35))),
          nabiz(halka(690, 220, 13), MOR, 96, 16, 35, 4),
          iz(p2, MAVI, 6, 104, 120, 30), nabiz(halka(450, 190, 13), MAVI, 116, 16, 35, 4),
          iz('M812 330 L1140 330', YESIL, 10, 118, 140, 45), iz('M960 380 L1140 380', MOR, 10, 132, 154, 45)]
    k += _serit([(60, 598, 320, 96), (440, 598, 320, 96), (820, 598, 320, 96)], (YESIL, YESIL, YESIL), 140, 10,
                ['M384 646 L434 646', 'M764 646 L814 646'])
    k.append(iz('M980 696 C980 740 220 740 220 700', YESIL, 7, 166, 178, 45))
    return k


def r07():
    k = [katman('terazi', [G(yol('M120 220 L480 160'), st(GRI, 10, 45))], o=K((0, 0), (4, 0), (12, 90), (40, 0))),
         nabiz(yol('M70 300 Q120 340 170 300 Z'), KIRMIZI, 14, 22, 35),
         nabiz(yol('M430 240 Q480 280 530 240 Z'), YESIL, 34, 22, 35),
         nabiz(yol('M650 300 C640 250 660 210 700 206 C740 204 760 230 758 270 C756 300 730 320 700 318 C676 316 660 312 650 300 Z'), KIRMIZI, 58, 20, 30),
         iz('M830 300 L862 300', KIRMIZI, 7, 76, 86, 60), iz('M910 300 L878 300', KIRMIZI, 7, 76, 86, 60),
         nabiz(halka(1052, 320, 12), YESIL, 94, 20, 35, 4)]
    k += _serit([(60, 598, 320, 92), (440, 598, 320, 92), (820, 598, 320, 92)], (MAVI, MOR, TURUNCU), 116, 20,
                ['M384 644 L434 644', 'M764 644 L814 644'])
    return k


def r08():
    k = [iz('M372 352 A212 212 0 0 0 318 228', MAVI, 9, 4, 26, 50),
         nabiz(yol('M146 280 m-20 0 a20 50 0 1 0 40 0 a20 50 0 1 0 -40 0'), KIRMIZI, 22, 22, 30)]
    bit = [1150, 1150, 1150, 1150, 1150, 1150]
    renk = [YESIL, '#65a30d', '#ca8a04', TURUNCU, KIRMIZI, '#991b1b']
    bas = [640, 640, 956, 742, 640, 640]
    for i in range(6):
        y = 194 + i * 56
        t = 40 + i * 18
        k.append(nabiz(halka(530, y + 6, 18), renk[i], t, 18, 30, 4))
        if i:
            k.append(iz(f'M{bas[i]} {y} L{bit[i]} {y}', renk[i], 8 + i, t + 2, t + 16, 45))
    k.append(iz('M640 524 L1150 524', GRI, 6, 40, 150, 45))
    k += _serit([(60, 598, 340, 100), (430, 598, 340, 100), (800, 598, 340, 100)], (MAVI, KIRMIZI, MOR), 150, 8)
    return k


def r09():
    k = [nabiz(halka(275, 250, 34), KIRMIZI, 4, 24, 35, 5),
         iz('M296 236 L330 160', KIRMIZI, 6, 10, 20, 60),
         iz('M470 396 C470 420 500 436 544 446', KIRMIZI, 9, 24, 44, 50)]
    n = 'M650 380 C760 300 950 280 1106 280'
    t = 'M650 470 C760 420 880 380 960 360 q10 -14 20 0 q10 14 20 0 q12 -22 24 0 q12 26 24 0 q14 -34 28 2'
    k += [iz(n, YESIL, 10, 48, 80, 35), isaretci(n, YESIL, 48, 80, 8),
          iz(t, KIRMIZI, 10, 84, 124, 35), isaretci(t, KIRMIZI, 84, 124, 8),
          nabiz(halka(1112, 280, 12), YESIL, 78, 16, 30, 4)]
    k += _serit([(60, 598, 250, 112), (345, 598, 250, 112), (630, 598, 250, 112), (915, 598, 230, 112)],
                (YESIL, KIRMIZI, KIRMIZI, KIRMIZI), 128, 12,
                ['M313 654 L340 654', 'M598 654 L625 654', 'M883 654 L910 654'])
    return k


def r10():
    k = [nabiz(halka(230, 260, 48), KIRMIZI, 4, 24, 30, 5),
         iz('M272 262 L430 292', KIRMIZI, 6, 12, 24, 60),
         nabiz(yol('M70 456 h160 a12 12 0 0 1 12 12 v34 a12 12 0 0 1 -12 12 h-110 l-20 16 l4 -16 h-34 a12 12 0 0 1 -12 -12 v-34 a12 12 0 0 1 12 -12 z'), MAVI, 30, 20, 30),
         nabiz(yol('M330 456 h200 a12 12 0 0 1 12 12 v34 a12 12 0 0 1 -12 12 h-150 l-20 16 l4 -16 h-34 a12 12 0 0 1 -12 -12 v-34 a12 12 0 0 1 12 -12 z'), MAVI, 44, 20, 30),
         nabiz(yol('M836 344 C850 330 870 330 884 340 M856 352 Q880 346 896 356'), TURUNCU, 66, 20, 35, 6),
         iz('M884 336 L960 250', TURUNCU, 6, 74, 86, 60),
         iz('M930 330 q10 -12 20 0 M960 330 q10 -12 20 0 M1000 324 q10 -24 20 0 M1030 324 l0 10 M1050 330 q10 -12 20 0', TURUNCU, 9, 86, 116, 50)]
    k += _serit([(60, 598, 340, 116), (430, 598, 340, 116), (800, 598, 340, 116)], (MAVI, TURUNCU, GRI), 124, 16)
    return k


def r11():
    k = [iz('M190 220 A50 30 0 1 1 280 240', MAVI, 9, 4, 26, 50),
         nabiz(halka(160, 314, 12), KIRMIZI, 22, 20, 35, 4),
         iz('M486 268 A40 40 0 0 1 540 300', YESIL, 8, 34, 48, 55), iz('M540 310 A40 40 0 0 1 480 262', YESIL, 8, 48, 62, 55)]
    for i, (x, y) in enumerate([(662, 488), (782, 428), (902, 368), (1022, 308)]):
        k.append(nabiz(halka(x, y, 14), YESIL, 70 + i * 16, 18, 35, 4))
    s = 'M660 520 C760 520 960 470 1110 300'
    k += [iz(s, YESIL, 9, 70, 130, 35), isaretci(s, YESIL, 70, 130, 7)]
    k += _serit([(60, 598, 250, 112), (325, 598, 250, 112), (590, 598, 250, 112), (855, 598, 290, 112)],
                (MAVI, MAVI, MAVI, MOR), 134, 10)
    return k


PLAN = {f'r{i:02d}': globals()[f'r{i:02d}'] for i in (1, 2, 3, 5, 6, 7, 8, 9, 10, 11)}
