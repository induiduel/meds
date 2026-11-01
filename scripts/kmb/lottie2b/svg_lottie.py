"""SVG (2B sahne dökümü) → Lottie şekil katmanları. Tek kaynak: components/kmb/sahneler*.tsx → svg_disa.mjs → svg/<sahne>.svg.

Çıktı `svg/<sahne>.lottie.json`:
  katmanlar: [{nm, id|None, it:[grup…]}]   belge sırasıyla (alttan üste); `data-id` taşıyan her grup kendi katmanı,
                                            aradaki parçalar `arka-N` katmanları
  bbox: {id: [x, y, w, h]}                  getBBox (svg_disa.mjs)
  cz:   {id: [{d, w, renk}]}                çizilebilir (class cz) yollar — ilerleme/çizim animasyonu için
  metin: [{x, y, metin}]                    atlanan <text> ögeleri (Lottie'ye yazı taşınmaz; etiket olarak eklenir)
Dönüşüm: tüm yol komutları (M L H V C S Q T A Z, göreli) → mutlak M/L/C/Z; dikdörtgen/daire/elips → yol; dönüşümler
koordinatlara işlenir (çizgi kalınlığı √|det| ile ölçeklenir); objectBoundingBox degradeler öge kutusuna oturtulur;
stop-opacity alfa durakları; fill-rule evenodd; pathLength'li dasharray gerçek uzunlukla ölçeklenir. Süzgeç/desen/işaret yok sayılır.
"""
from __future__ import annotations

import json
import math
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lottie_dsl import S, renk  # noqa: E402

KOK = Path(__file__).resolve().parent / 'svg'
KAPPA = 0.5522847498

# ———————————————————————— dönüşüm matrisi (a b c d e f)

def m_carp(m, n):
    a, b, c, d, e, f = m
    a2, b2, c2, d2, e2, f2 = n
    return (a * a2 + c * b2, b * a2 + d * b2, a * c2 + c * d2, b * c2 + d * d2, a * e2 + c * f2 + e, b * e2 + d * f2 + f)


def m_uygula(m, p):
    a, b, c, d, e, f = m
    return (a * p[0] + c * p[1] + e, b * p[0] + d * p[1] + f)


def transform_coz(t: str | None):
    m = (1, 0, 0, 1, 0, 0)
    if not t:
        return m
    for ad, arg in re.findall(r'(\w+)\s*\(([^)]*)\)', t):
        v = [float(x) for x in re.findall(r'-?\d*\.?\d+(?:e-?\d+)?', arg)]
        if ad == 'translate':
            n = (1, 0, 0, 1, v[0], v[1] if len(v) > 1 else 0)
        elif ad == 'scale':
            n = (v[0], 0, 0, v[1] if len(v) > 1 else v[0], 0, 0)
        elif ad == 'rotate':
            r = math.radians(v[0]); cs, sn = math.cos(r), math.sin(r)
            n = (cs, sn, -sn, cs, 0, 0)
            if len(v) > 2:
                n = m_carp(m_carp((1, 0, 0, 1, v[1], v[2]), n), (1, 0, 0, 1, -v[1], -v[2]))
        elif ad == 'matrix':
            n = tuple(v[:6])
        else:
            continue
        m = m_carp(m, n)
    return m


def m_olcek(m):
    return math.sqrt(abs(m[0] * m[3] - m[1] * m[2]))


# ———————————————————————— yol normalizasyonu

def _arc_bezier(p0, rx, ry, phi, fa, fs, p1):
    """SVG yayı → kübik Bezier parçaları (her biri ≤ 90°)."""
    if rx == 0 or ry == 0 or p0 == p1:
        return [('L', p1)]
    phi = math.radians(phi); cp, sp = math.cos(phi), math.sin(phi)
    dx, dy = (p0[0] - p1[0]) / 2, (p0[1] - p1[1]) / 2
    x1 = cp * dx + sp * dy; y1 = -sp * dx + cp * dy
    rx, ry = abs(rx), abs(ry)
    lam = (x1 / rx) ** 2 + (y1 / ry) ** 2
    if lam > 1:
        rx *= math.sqrt(lam); ry *= math.sqrt(lam)
    num = rx * rx * ry * ry - rx * rx * y1 * y1 - ry * ry * x1 * x1
    den = rx * rx * y1 * y1 + ry * ry * x1 * x1
    k = math.sqrt(max(0, num / den)) if den else 0
    if fa == fs:
        k = -k
    cx1 = k * rx * y1 / ry; cy1 = -k * ry * x1 / rx
    cx = cp * cx1 - sp * cy1 + (p0[0] + p1[0]) / 2
    cy = sp * cx1 + cp * cy1 + (p0[1] + p1[1]) / 2
    def ang(u, v):
        a = math.atan2(u[0] * v[1] - u[1] * v[0], u[0] * v[0] + u[1] * v[1])
        return a
    t1 = ang((1, 0), ((x1 - cx1) / rx, (y1 - cy1) / ry))
    dt = ang(((x1 - cx1) / rx, (y1 - cy1) / ry), ((-x1 - cx1) / rx, (-y1 - cy1) / ry))
    if not fs and dt > 0:
        dt -= 2 * math.pi
    elif fs and dt < 0:
        dt += 2 * math.pi
    n = max(1, math.ceil(abs(dt) / (math.pi / 2)))
    out = []
    for i in range(n):
        a0 = t1 + dt * i / n; a1 = t1 + dt * (i + 1) / n
        al = 4 / 3 * math.tan((a1 - a0) / 4)
        def pt(a):
            x, y = rx * math.cos(a), ry * math.sin(a)
            return (cp * x - sp * y + cx, sp * x + cp * y + cy)
        def dv(a):
            x, y = -rx * math.sin(a), ry * math.cos(a)
            return (cp * x - sp * y, sp * x + cp * y)
        P0, P1 = pt(a0), pt(a1); D0, D1 = dv(a0), dv(a1)
        out.append(('C', (P0[0] + al * D0[0], P0[1] + al * D0[1]), (P1[0] - al * D1[0], P1[1] - al * D1[1]), P1))
    return out


def yol_normalize(d: str):
    """→ [[('M',p),('L',p),('C',c1,c2,p),('Z',)], …] alt yollar, mutlak."""
    tok = re.findall(r'[MLHVCSQTAZmlhvcsqtaz]|-?\d*\.?\d+(?:e-?\d+)?', d)
    i, cmd = 0, None
    P = (0.0, 0.0); bas = P; onceki_c = None; onceki_q = None
    altlar, cur = [], []
    def num(k):
        return float(tok[i + k])
    while i < len(tok):
        t = tok[i]
        if re.match(r'[A-Za-z]', t):
            cmd = t; i += 1
            if cmd in 'Zz':
                if cur:
                    cur.append(('Z',)); altlar.append(cur); cur = []
                P = bas; onceki_c = onceki_q = None
            continue
        rel = cmd.islower(); c = cmd.upper()
        if c == 'M':
            Q = (num(0), num(1)); i += 2
            if rel:
                Q = (P[0] + Q[0], P[1] + Q[1])
            if cur:
                altlar.append(cur)
            cur = [('M', Q)]; P = bas = Q; cmd = 'l' if rel else 'L'; onceki_c = onceki_q = None
        elif c == 'L':
            Q = (num(0), num(1)); i += 2
            if rel:
                Q = (P[0] + Q[0], P[1] + Q[1])
            cur.append(('L', Q)); P = Q; onceki_c = onceki_q = None
        elif c == 'H':
            x = num(0); i += 1
            Q = (P[0] + x if rel else x, P[1]); cur.append(('L', Q)); P = Q; onceki_c = onceki_q = None
        elif c == 'V':
            y = num(0); i += 1
            Q = (P[0], P[1] + y if rel else y); cur.append(('L', Q)); P = Q; onceki_c = onceki_q = None
        elif c == 'C':
            c1 = (num(0), num(1)); c2 = (num(2), num(3)); Q = (num(4), num(5)); i += 6
            if rel:
                c1 = (P[0] + c1[0], P[1] + c1[1]); c2 = (P[0] + c2[0], P[1] + c2[1]); Q = (P[0] + Q[0], P[1] + Q[1])
            cur.append(('C', c1, c2, Q)); P = Q; onceki_c = c2; onceki_q = None
        elif c == 'S':
            c2 = (num(0), num(1)); Q = (num(2), num(3)); i += 4
            if rel:
                c2 = (P[0] + c2[0], P[1] + c2[1]); Q = (P[0] + Q[0], P[1] + Q[1])
            c1 = (2 * P[0] - onceki_c[0], 2 * P[1] - onceki_c[1]) if onceki_c else P
            cur.append(('C', c1, c2, Q)); P = Q; onceki_c = c2; onceki_q = None
        elif c == 'Q':
            q = (num(0), num(1)); Q = (num(2), num(3)); i += 4
            if rel:
                q = (P[0] + q[0], P[1] + q[1]); Q = (P[0] + Q[0], P[1] + Q[1])
            c1 = (P[0] + 2 / 3 * (q[0] - P[0]), P[1] + 2 / 3 * (q[1] - P[1])); c2 = (Q[0] + 2 / 3 * (q[0] - Q[0]), Q[1] + 2 / 3 * (q[1] - Q[1]))
            cur.append(('C', c1, c2, Q)); P = Q; onceki_q = q; onceki_c = None
        elif c == 'T':
            Q = (num(0), num(1)); i += 2
            if rel:
                Q = (P[0] + Q[0], P[1] + Q[1])
            q = (2 * P[0] - onceki_q[0], 2 * P[1] - onceki_q[1]) if onceki_q else P
            c1 = (P[0] + 2 / 3 * (q[0] - P[0]), P[1] + 2 / 3 * (q[1] - P[1])); c2 = (Q[0] + 2 / 3 * (q[0] - Q[0]), Q[1] + 2 / 3 * (q[1] - Q[1]))
            cur.append(('C', c1, c2, Q)); P = Q; onceki_q = q; onceki_c = None
        elif c == 'A':
            rx, ry, phi, fa, fs = num(0), num(1), num(2), int(num(3)), int(num(4)); Q = (num(5), num(6)); i += 7
            if rel:
                Q = (P[0] + Q[0], P[1] + Q[1])
            for seg in _arc_bezier(P, rx, ry, phi, fa, fs, Q):
                cur.append(seg if seg[0] == 'L' else ('C', seg[1], seg[2], seg[3]))
            P = Q; onceki_c = onceki_q = None
        else:
            i += 1
    if cur:
        altlar.append(cur)
    return altlar


def alt_donustur(alt, m):
    out = []
    for s in alt:
        if s[0] in ('M', 'L'):
            out.append((s[0], m_uygula(m, s[1])))
        elif s[0] == 'C':
            out.append(('C', m_uygula(m, s[1]), m_uygula(m, s[2]), m_uygula(m, s[3])))
        else:
            out.append(s)
    return out


def alt_sh(alt):
    v, ii, oo, kapali = [], [], [], False
    for s in alt:
        if s[0] == 'M' or s[0] == 'L':
            v.append([round(s[1][0], 2), round(s[1][1], 2)]); ii.append([0, 0]); oo.append([0, 0])
        elif s[0] == 'C':
            p0 = v[-1]
            oo[-1] = [round(s[1][0] - p0[0], 2), round(s[1][1] - p0[1], 2)]
            v.append([round(s[3][0], 2), round(s[3][1], 2)]); ii.append([round(s[2][0] - s[3][0], 2), round(s[2][1] - s[3][1], 2)]); oo.append([0, 0])
        elif s[0] == 'Z':
            kapali = True
    if kapali and len(v) > 1 and abs(v[0][0] - v[-1][0]) < .01 and abs(v[0][1] - v[-1][1]) < .01:
        ii[0] = ii[-1]; v.pop(); ii.pop(); oo.pop()
    return {'ty': 'sh', 'ks': S({'c': kapali, 'v': v, 'i': ii, 'o': oo})}


def alt_noktalar(altlar):
    for alt in altlar:
        for s in alt:
            if s[0] in ('M', 'L'):
                yield s[1]
            elif s[0] == 'C':
                yield s[1]; yield s[2]; yield s[3]


def alt_uzunluk(altlar):
    L = 0.0
    for alt in altlar:
        P = None
        for s in alt:
            if s[0] == 'M':
                P = s[1]
            elif s[0] == 'L':
                L += math.dist(P, s[1]); P = s[1]
            elif s[0] == 'C':
                q = P
                for j in range(1, 17):
                    t = j / 16; mt = 1 - t
                    pt = tuple(mt ** 3 * P[k] + 3 * mt * mt * t * s[1][k] + 3 * mt * t * t * s[2][k] + t ** 3 * s[3][k] for k in (0, 1))
                    L += math.dist(q, pt); q = pt
                P = s[3]
    return L


def elips_yol(cx, cy, rx, ry):
    k = KAPPA
    return [[('M', (cx + rx, cy)),
             ('C', (cx + rx, cy + ry * k), (cx + rx * k, cy + ry), (cx, cy + ry)),
             ('C', (cx - rx * k, cy + ry), (cx - rx, cy + ry * k), (cx - rx, cy)),
             ('C', (cx - rx, cy - ry * k), (cx - rx * k, cy - ry), (cx, cy - ry)),
             ('C', (cx + rx * k, cy - ry), (cx + rx, cy - ry * k), (cx + rx, cy)), ('Z',)]]


def dikdortgen_yol(x, y, w, h, rx, ry):
    rx = min(rx, w / 2); ry = min(ry, h / 2)
    if rx <= 0 or ry <= 0:
        return [[('M', (x, y)), ('L', (x + w, y)), ('L', (x + w, y + h)), ('L', (x, y + h)), ('Z',)]]
    k = KAPPA
    return [[('M', (x + rx, y)), ('L', (x + w - rx, y)),
             ('C', (x + w - rx + rx * k, y), (x + w, y + ry - ry * k), (x + w, y + ry)),
             ('L', (x + w, y + h - ry)),
             ('C', (x + w, y + h - ry + ry * k), (x + w - rx + rx * k, y + h), (x + w - rx, y + h)),
             ('L', (x + rx, y + h)),
             ('C', (x + rx - rx * k, y + h), (x, y + h - ry + ry * k), (x, y + h - ry)),
             ('L', (x, y + ry)),
             ('C', (x, y + ry - ry * k), (x + rx - rx * k, y), (x + rx, y)), ('Z',)]]


# ———————————————————————— stil

def f_(v, vars=1.0):
    if v is None:
        return None
    v = v.strip()
    if v.endswith('%'):
        return float(v[:-1]) / 100
    return float(v)


def degradeler(root):
    out = {}
    for el in root.iter():
        tag = el.tag.split('}')[-1]
        if tag not in ('linearGradient', 'radialGradient'):
            continue
        st = []
        for s in el:
            if s.tag.split('}')[-1] != 'stop':
                continue
            st.append((f_(s.get('offset') or '0'), s.get('stop-color') or '#000000', float(s.get('stop-opacity') or 1)))
        g = {'tip': 'r' if tag == 'radialGradient' else 'l', 'stops': st, 'units': el.get('gradientUnits') or 'objectBoundingBox',
             'tr': el.get('gradientTransform')}
        if g['tip'] == 'l':
            g['k'] = [f_(el.get('x1') or '0'), f_(el.get('y1') or '0'), f_(el.get('x2') or '1'), f_(el.get('y2') or '0')]
        else:
            g['k'] = [f_(el.get('cx') or '0.5'), f_(el.get('cy') or '0.5'), f_(el.get('r') or '0.5')]
        out[el.get('id')] = g
    return out


def gf_yap(g, bbox, o, m):
    x, y, w, h = bbox
    def obb(px, py):
        return (x + px * w, y + py * h)
    k = []
    for p, hx, _ in g['stops']:
        k += [round(p, 3)] + renk(hx)[:3]
    alfa = [v for v in g['stops'] if v[2] < 1]
    if alfa:
        for p, _, a in g['stops']:
            k += [round(p, 3), round(a, 3)]
    if g['tip'] == 'l':
        x1, y1, x2, y2 = g['k']
        s, e = (obb(x1, y1), obb(x2, y2)) if g['units'] == 'objectBoundingBox' else ((x1, y1), (x2, y2))
        t = 1
    else:
        cx, cy, r = g['k']
        if g['units'] == 'objectBoundingBox':
            s = obb(cx, cy); e = (s[0] + r * max(w, h) * (w / max(w, h) if w >= h else 1), s[1])
            e = (s[0] + r * max(w, h), s[1])
        else:
            s = (cx, cy); e = (cx + r, cy)
        t = 2
    if g['units'] != 'objectBoundingBox':
        s = m_uygula(m, s); e = m_uygula(m, e)
    return {'ty': 'gf', 'o': S(o), 'r': 1, 'g': {'p': len(g['stops']), 'k': S([round(v, 4) for v in k])}, 's': S([round(s[0], 1), round(s[1], 1)]), 'e': S([round(e[0], 1), round(e[1], 1)]), 't': t}


# ———————————————————————— eleman → grup

class Donusturucu:
    def __init__(self, root):
        self.grad = degradeler(root)
        self.metin = []
        self.cz = {}
        self.atlanan = {}

    def stil(self, el, kalit):
        s = dict(kalit)
        for k in ('fill', 'stroke', 'stroke-width', 'opacity', 'fill-opacity', 'stroke-opacity', 'stroke-dasharray', 'fill-rule', 'stroke-linecap', 'stroke-linejoin'):
            v = el.get(k)
            if v is not None:
                s[k] = v
        st = el.get('style')
        if st:
            for kv in st.split(';'):
                if ':' in kv:
                    k, v = kv.split(':', 1); s[k.strip()] = v.strip()
        # opacity gruplardan çarpılarak iner
        if el.get('opacity') is not None:
            s['_o'] = kalit.get('_o', 1.0) * float(el.get('opacity'))
        else:
            s['_o'] = kalit.get('_o', 1.0)
        s.pop('opacity', None)
        return s

    def sekil(self, el, m, stil, oge):
        tag = el.tag.split('}')[-1]
        if tag == 'path':
            altlar = yol_normalize(el.get('d') or '')
        elif tag == 'rect':
            x, y, w, h = (float(el.get(k) or 0) for k in ('x', 'y', 'width', 'height'))
            rx = float(el.get('rx') or el.get('ry') or 0); ry = float(el.get('ry') or el.get('rx') or 0)
            altlar = dikdortgen_yol(x, y, w, h, rx, ry)
        elif tag == 'circle':
            r = float(el.get('r') or 0); altlar = elips_yol(float(el.get('cx') or 0), float(el.get('cy') or 0), r, r)
        elif tag == 'ellipse':
            altlar = elips_yol(float(el.get('cx') or 0), float(el.get('cy') or 0), float(el.get('rx') or 0), float(el.get('ry') or 0))
        elif tag in ('line', 'polyline', 'polygon'):
            if tag == 'line':
                altlar = [[('M', (float(el.get('x1') or 0), float(el.get('y1') or 0))), ('L', (float(el.get('x2') or 0), float(el.get('y2') or 0)))]]
            else:
                pts = [float(v) for v in re.findall(r'-?\d*\.?\d+', el.get('points') or '')]
                P = list(zip(pts[::2], pts[1::2]))
                altlar = [[('M', P[0])] + [('L', p) for p in P[1:]] + ([('Z',)] if tag == 'polygon' else [])]
        else:
            return None
        if not altlar:
            return None
        m2 = m_carp(m, transform_coz(el.get('transform')))
        altlar = [alt_donustur(a, m2) for a in altlar]
        pts = list(alt_noktalar(altlar))
        if not pts:
            return None
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        bbox = (min(xs), min(ys), max(1e-6, max(xs) - min(xs)), max(1e-6, max(ys) - min(ys)))
        it = [alt_sh(a) for a in altlar]
        o = stil.get('_o', 1.0)
        fill = stil.get('fill', '#000000')
        fo = float(stil.get('fill-opacity', 1)) * o
        if fill and fill != 'none':
            mm = re.match(r'url\(#([^)]+)\)', fill)
            if mm:
                g = self.grad.get(mm.group(1))
                if g:
                    it.append(gf_yap(g, bbox, round(fo * 100, 1), m2))
            elif fill.startswith('#') or fill in ('white', 'black'):
                h = {'white': '#ffffff', 'black': '#000000'}.get(fill, fill)
                if len(h) == 4:
                    h = '#' + ''.join(c * 2 for c in h[1:])
                it.append({'ty': 'fl', 'c': S(renk(h)), 'o': S(round(fo * 100, 1)), 'r': 2 if stil.get('fill-rule') == 'evenodd' else 1})
        stroke = stil.get('stroke')
        mm = re.match(r'url\(#([^)]+)\)', stroke or '')
        if mm and self.grad.get(mm.group(1)):
            # degrade çizgi (gs): dolgu degradesiyle aynı geometri
            w = float(stil.get('stroke-width', 1)) * m_olcek(m2)
            so = float(stil.get('stroke-opacity', 1)) * o
            g = gf_yap(self.grad[mm.group(1)], bbox, round(so * 100, 1), m2)
            it.append({'ty': 'gs', 'o': g['o'], 'w': S(round(w, 2)), 'g': g['g'], 's': g['s'], 'e': g['e'], 't': g['t'], 'lc': 2, 'lj': 2})
            stroke = None
        if stroke and stroke != 'none' and stroke.startswith('#'):
            if len(stroke) == 4:
                stroke = '#' + ''.join(c * 2 for c in stroke[1:])
            w = float(stil.get('stroke-width', 1)) * m_olcek(m2)
            so = float(stil.get('stroke-opacity', 1)) * o
            x = {'ty': 'st', 'c': S(renk(stroke)), 'o': S(round(so * 100, 1)), 'w': S(round(w, 2)),
                 'lc': {'butt': 1, 'round': 2, 'square': 3}.get(stil.get('stroke-linecap', 'round'), 2), 'lj': {'miter': 1, 'round': 2, 'bevel': 3}.get(stil.get('stroke-linejoin', 'round'), 2)}
            da = stil.get('stroke-dasharray')
            if da and da != 'none':
                vals = [float(v) for v in re.findall(r'-?\d*\.?\d+', da)]
                if el.get('pathLength'):
                    L = alt_uzunluk(altlar) / float(el.get('pathLength'))
                    vals = [v * L for v in vals]
                if len(vals) >= 1 and sum(vals) > 0:
                    d1 = vals[0]; d2 = vals[1] if len(vals) > 1 else vals[0]
                    x['d'] = [{'n': 'd', 'nm': 'tire', 'v': S(round(d1, 2))}, {'n': 'g', 'nm': 'boşluk', 'v': S(round(d2, 2))}, {'n': 'o', 'nm': 'kayma', 'v': S(0)}]
            it.append(x)
            if 'cz' in (el.get('class') or '').split() and oge:
                self.cz.setdefault(oge, []).append({'d': yol_d(altlar), 'w': round(w, 2), 'renk': stroke, 'o': round(so, 2)})
        it.append({'ty': 'tr', 'p': S([0, 0]), 'a': S([0, 0]), 's': S([100, 100]), 'r': S(0), 'o': S(100), 'sk': S(0), 'sa': S(0)})
        gr = {'ty': 'gr', 'it': it, 'nm': tag}
        if el.get('marker-end') and altlar:
            # kmb-ok işareti: yolun sonunda, son parçanın yönünde 6×çizgi kalınlığı üçgen (#2f6fd6 ya da çizgi rengi)
            son = altlar[-1]
            uc = [x for x in son if x[0] in ('L', 'C')]
            if uc:
                p1 = uc[-1][-1]; p0 = uc[-1][2] if uc[-1][0] == 'C' else (uc[-2][-1] if len(uc) > 1 else son[0][1])
                ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
                w = float(stil.get('stroke-width', 1)) * m_olcek(m2) * 6
                pts = [(0, -w / 2), (w, 0), (0, w / 2)]
                cs, sn = math.cos(ang), math.sin(ang)
                P = [(p1[0] + (x - w * 0.8) * cs - y * sn, p1[1] + (x - w * 0.8) * sn + y * cs) for x, y in pts]
                ok = alt_sh([('M', P[0]), ('L', P[1]), ('L', P[2]), ('Z',)])
                col = stroke if (stroke and stroke.startswith('#')) else '#2f6fd6'
                okg = {'ty': 'gr', 'nm': 'ok', 'it': [ok, {'ty': 'fl', 'c': S(renk(col)), 'o': S(100), 'r': 1}, _tr()]}
                return {'ty': 'gr', 'it': [okg, gr, _tr()], 'nm': tag + '+ok'}
        return gr

    def grup(self, el, m, kalit, oge):
        """<g> → grup; data-id taşıyan alt gruplar ayrı katman olarak döner (katman akışı)."""
        stil = self.stil(el, kalit)
        m2 = m_carp(m, transform_coz(el.get('transform')))
        parcalar = []  # ('sekil', gr) | ('katman', nm, id, items)
        for c in el:
            tag = c.tag.split('}')[-1]
            if tag in ('defs', 'title', 'desc', 'metadata'):
                continue
            if tag == 'text':
                self.metin.append({'x': float(c.get('x') or 0), 'y': float(c.get('y') or 0), 'metin': ''.join(c.itertext()).strip()})
                continue
            if tag == 'g':
                cid = c.get('data-id')
                alt = self.grup(c, m2, stil, cid or oge)
                if cid:
                    parcalar.append(('katman', cid, cid, alt))
                else:
                    for p in alt:
                        parcalar.append(p)
                continue
            s = self.sekil(c, m2, self.stil(c, stil), oge)
            if s:
                parcalar.append(('sekil', s))
            else:
                self.atlanan[tag] = self.atlanan.get(tag, 0) + 1
        return parcalar


def yol_d(altlar):
    out = []
    for alt in altlar:
        for s in alt:
            if s[0] == 'M':
                out.append(f'M{s[1][0]:.1f} {s[1][1]:.1f}')
            elif s[0] == 'L':
                out.append(f'L{s[1][0]:.1f} {s[1][1]:.1f}')
            elif s[0] == 'C':
                out.append(f'C{s[1][0]:.1f} {s[1][1]:.1f} {s[2][0]:.1f} {s[2][1]:.1f} {s[3][0]:.1f} {s[3][1]:.1f}')
            else:
                out.append('Z')
    return ' '.join(out)


def _tr():
    return {'ty': 'tr', 'p': S([0, 0]), 'a': S([0, 0]), 's': S([100, 100]), 'r': S(0), 'o': S(100), 'sk': S(0), 'sa': S(0)}


def katmanla(parcalar, ad_on='arka'):
    """Parçalar → katman listesi. Ardışık şekiller tek 'arka' katmanında. `it` BELGE SIRASIYLA (alttan üste) tutulur;
    Anim.ekle(nm, *it) Lottie için ters çevirir (lottie_dsl sözleşmesi)."""
    out, cari, n = [], [], 0
    def bosalt():
        nonlocal cari, n
        if cari:
            out.append({'nm': f'{ad_on}-{n}', 'id': None, 'it': list(cari)}); n += 1; cari = []
    for p in parcalar:
        if p[0] == 'sekil':
            cari.append(p[1])
        else:
            bosalt()
            _, nm, cid, alt = p
            # öge içi: alt parçalar düz şekillerse tek katman; içinde başka öge varsa yine ayrı katman (nadir)
            ic = []
            for q in alt:
                if q[0] == 'sekil':
                    ic.append(q[1])
                else:
                    if ic:
                        out.append({'nm': nm, 'id': cid, 'it': list(ic)}); ic = []
                    out.append({'nm': q[1], 'id': q[2], 'it': [x[1] for x in q[3] if x[0] == 'sekil']})
            out.append({'nm': nm, 'id': cid, 'it': list(ic)})
    bosalt()
    return out


def gizli_listesi(sahne):
    kok = Path(__file__).resolve().parents[3] / 'src/components/kmb'
    for p in sorted(kok.glob('sahneler*.tsx')):
        t = p.read_text(encoding='utf-8')
        for blok in re.split(r'\nconst \w+: Sahne = \{', t)[1:]:
            ad = re.search(r"\n\s+ad: '([^']*)'", blok)
            g = re.search(r"gizli: \[([^\]]*)\]", blok)
            ids = re.findall(r"'([^']+)'", g.group(1)) if g else []
            if ids and any(i.split('-')[0] == ON_EK.get(sahne) for i in ids):
                return ids
            if not ids and g and ON_EK.get(sahne) == 'c':
                return []
    return []


ON_EK = {'foley': 'f', 'mesane': 'g', 'erkek': 'e', 'travma': 't', 'malzeme': 'm', 'pozisyon': 'p', 'kadin': 'k', 'yakin-mesane': 'y',
         'yakin-uretra': 'z', 'yakin-kadin': 'v', 'yakin-el': 'h', 'yakin-erkek-jel': 'j', 'foley-kesit': 'c', 'maket': 'mk'}


def donustur(sahne: str):
    svg = (KOK / f'{sahne}.svg').read_text(encoding='utf-8')
    svg = re.sub(r'\sxmlns(:\w+)?="[^"]*"', '', svg)
    root = ET.fromstring(svg)
    D = Donusturucu(root)
    parcalar = D.grup(root, (1, 0, 0, 1, 0, 0), {}, None)
    katmanlar = katmanla(parcalar)
    bbox = json.loads((KOK / 'bbox.json').read_text(encoding='utf-8')).get(sahne, {})
    gizli = [g for g in gizli_listesi(sahne) if g in bbox]
    out = {'sahne': sahne, 'katmanlar': katmanlar, 'bbox': bbox, 'gizli': gizli, 'cz': D.cz, 'metin': D.metin, 'atlanan': D.atlanan}
    (KOK / f'{sahne}.lottie.json').write_text(json.dumps(out, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
    return out


if __name__ == '__main__':
    secili = [a for a in sys.argv[1:] if not a.startswith('--')] or sorted(p.stem for p in KOK.glob('*.svg'))
    for s in secili:
        o = donustur(s)
        print(f'{s}: {len(o["katmanlar"])} katman ({sum(1 for k in o["katmanlar"] if k["id"])} öge), gizli {len(o["gizli"])}, cz {sum(len(v) for v in o["cz"].values())}, metin {len(o["metin"])}, atlanan {o["atlanan"] or "-"}')
