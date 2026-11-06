"""k2-07 / k2-15 / k2-37 ara resim Lottie planları için ortak yardımcı (yalnız bu üç dersin plan dosyaları kullanır).

SVG kaynağını okur; çizilmiş yapıları belge sırasıyla (= resmin anlattığı sıra) çıkarır ve üstlerine hizalı hareket
kurar: oklu yollar/çizgiler baştan sona çizilir (ana oklarda kayan işaretçi), eğriler (grafik, yolak) çizilir, kutular
ve yuvarlak yapılar sırayla nabızla vurgulanır. Metin eklemez; son kare sakin ve tam durumdur.
Yollar M/L/C mutlak biçime çevrilir (göreli komutlar, H/V, S, Q/T, A desteklenir), transform (translate/scale) uygulanır.
"""
from __future__ import annotations

import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from lottie_uret import yol, iz, isaretci, nabiz, kutu, halka, MAVI, GRI  # noqa: F401

KOK = Path(__file__).resolve().parents[3]
NS = '{http://www.w3.org/2000/svg}'
GENIS, YUKSEK = 1200, 800


def _tok(d):
    return re.findall(r'[A-Za-z]|[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?', d)


def mutlak(d):
    """SVG yolu → [(M,(x,y)) | (L,(x,y)) | (C,c1,c2,q) | (Z,)] mutlak."""
    t = _tok(d)
    i, cmd, out = 0, None, []
    x = y = sx = sy = 0.0
    pc = None  # son kontrol noktası (S/T)
    pq = None

    def n():
        nonlocal i
        v = float(t[i]); i += 1
        return v
    while i < len(t):
        if re.match(r'[A-Za-z]', t[i]):
            cmd = t[i]; i += 1
            if cmd in 'Zz':
                out.append(('Z',)); x, y = sx, sy; pc = pq = None
                continue
        if cmd is None:
            break
        rel = cmd.islower(); c = cmd.upper()
        ox, oy = (x, y) if rel else (0, 0)
        if c == 'M':
            x, y = n() + ox, n() + oy; sx, sy = x, y; out.append(('M', (x, y))); cmd = 'l' if rel else 'L'; pc = pq = None
        elif c == 'L':
            x, y = n() + ox, n() + oy; out.append(('L', (x, y))); pc = pq = None
        elif c == 'H':
            x = n() + (x if rel else 0); out.append(('L', (x, y))); pc = pq = None
        elif c == 'V':
            y = n() + (y if rel else 0); out.append(('L', (x, y))); pc = pq = None
        elif c == 'C':
            a = (n() + ox, n() + oy); b = (n() + ox, n() + oy); q = (n() + ox, n() + oy)
            out.append(('C', a, b, q)); x, y = q; pc = b; pq = None
        elif c == 'S':
            a = (2 * x - pc[0], 2 * y - pc[1]) if pc else (x, y)
            b = (n() + ox, n() + oy); q = (n() + ox, n() + oy)
            out.append(('C', a, b, q)); x, y = q; pc = b; pq = None
        elif c in 'QT':
            if c == 'Q':
                k = (n() + ox, n() + oy)
            else:
                k = (2 * x - pq[0], 2 * y - pq[1]) if pq else (x, y)
            q = (n() + ox, n() + oy)
            a = (x + 2 / 3 * (k[0] - x), y + 2 / 3 * (k[1] - y)); b = (q[0] + 2 / 3 * (k[0] - q[0]), q[1] + 2 / 3 * (k[1] - q[1]))
            out.append(('C', a, b, q)); x, y = q; pq = k; pc = None
        elif c == 'A':
            n(); n(); n(); n(); n()
            q = (n() + ox, n() + oy)
            out.append(('L', q)); x, y = q; pc = pq = None
        else:
            i += 1
    return out


def _uygula(seg, m):
    a, b, c, d, e, f = m
    T = lambda p: (round(a * p[0] + c * p[1] + e, 1), round(b * p[0] + d * p[1] + f, 1))
    r = []
    for s in seg:
        r.append((s[0],) + tuple(T(p) for p in s[1:]))
    return r


def yaz(seg):
    p = []
    for s in seg:
        if s[0] == 'Z':
            p.append('z')
        elif s[0] in 'ML':
            p.append(f'{s[0]}{s[1][0]:g} {s[1][1]:g}')
        else:
            p.append('C' + ' '.join(f'{q[0]:g} {q[1]:g}' for q in s[1:]))
    return ' '.join(p)


def _carp(m1, m2):
    a, b, c, d, e, f = m1
    A, B, C, D, E, F = m2
    return (a * A + c * B, b * A + d * B, a * C + c * D, b * C + d * D, a * E + c * F + e, b * E + d * F + f)


def _matris(tr):
    m = (1, 0, 0, 1, 0, 0)
    for ad, arg in re.findall(r'(\w+)\s*\(([^)]*)\)', tr or ''):
        v = [float(z) for z in re.findall(r'[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?', arg)]
        if ad == 'translate':
            k = (1, 0, 0, 1, v[0], v[1] if len(v) > 1 else 0)
        elif ad == 'scale':
            k = (v[0], 0, 0, v[1] if len(v) > 1 else v[0], 0, 0)
        elif ad == 'matrix':
            k = tuple(v)
        elif ad == 'rotate':
            r = math.radians(v[0]); cx, cy = (v[1], v[2]) if len(v) > 2 else (0, 0)
            k = _carp(_carp((1, 0, 0, 1, cx, cy), (math.cos(r), math.sin(r), -math.sin(r), math.cos(r), 0, 0)), (1, 0, 0, 1, -cx, -cy))
        else:
            continue
        m = _carp(m, k)
    return m


def _uzunluk(seg):
    L, P = 0.0, None
    for s in seg:
        if s[0] == 'M':
            P = s[1]
        elif s[0] in 'LC':
            q = s[-1]
            if P:
                L += math.dist(P, q)
            P = q
    return L


def ogeler(key, rid):
    """Belge sırasıyla [(tür, veri, renk)] — tür: 'ok' (oklu yol), 'egri' (oksuz uzun eğri), 'kutu', 'halka'."""
    kok = ET.parse(KOK / 'public' / 'ara_resim' / key / f'{rid}.svg').getroot()
    out = []

    def gez(e, m, defs):
        tag = e.tag.replace(NS, '')
        if tag in ('defs', 'marker', 'text', 'clipPath', 'mask', 'linearGradient', 'radialGradient', 'symbol', 'use'):
            return
        m = _carp(m, _matris(e.get('transform')))
        renk = e.get('stroke')
        renk = renk if renk and renk.startswith('#') else None
        sw = float(re.sub(r'[^\d.]', '', e.get('stroke-width', '1')) or 1)
        if tag in ('path', 'line', 'polyline'):
            if tag == 'path':
                seg = mutlak(e.get('d', ''))
            elif tag == 'line':
                seg = [('M', (float(e.get('x1', 0)), float(e.get('y1', 0)))), ('L', (float(e.get('x2', 0)), float(e.get('y2', 0))))]
            else:
                pts = re.findall(r'[-+]?\d*\.?\d+', e.get('points', ''))
                pp = [(float(pts[j]), float(pts[j + 1])) for j in range(0, len(pts) - 1, 2)]
                seg = [('M', pp[0])] + [('L', p) for p in pp[1:]] if pp else []
            if seg and sum(1 for s in seg if s[0] == 'M') == 1:
                seg = _uygula(seg, m)
                L = _uzunluk(seg)
                kapali = any(s[0] == 'Z' for s in seg)
                acik = e.get('fill', 'black') == 'none' and not kapali
                if e.get('marker-end') or e.get('marker-start'):
                    if L > 25:
                        out.append(('ok', yaz(seg), renk or GRI, L))
                elif kapali and renk and sw >= 2 and L > 180 and e.get('stroke-dasharray') is None:
                    out.append(('yapi', yaz(seg), renk, L))
                elif acik and renk and L > 160 and sw >= 2.5 and not e.get('stroke-dasharray'):
                    out.append(('egri', yaz(seg), renk, L))
        elif tag == 'rect':
            x, y = float(e.get('x', 0)), float(e.get('y', 0))
            w, h = float(e.get('width', 0)), float(e.get('height', 0))
            sx, sy = math.hypot(m[0], m[1]), math.hypot(m[2], m[3])
            X, Y, W, H = m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5], w * sx, h * sy
            if 40 <= W and 26 <= H and W * H < 0.16 * GENIS * YUKSEK and W < 1000 and (renk or e.get('fill', '#').startswith('#')):
                r = float(e.get('rx', 8) or 8) * sx
                out.append(('kutu', (X, Y, W, H, r), renk or GRI, W * H))
        elif tag in ('circle', 'ellipse'):
            cx, cy = float(e.get('cx', 0)), float(e.get('cy', 0))
            r = float(e.get('r', 0) or max(float(e.get('rx', 0)), float(e.get('ry', 0))))
            s = math.hypot(m[0], m[1])
            R = r * s
            if R >= 14 and renk:
                out.append(('halka', (m[0] * cx + m[2] * cy + m[4], m[1] * cx + m[3] * cy + m[5], R), renk, R))
        for c in e:
            gez(c, m, defs)
    gez(kok, (1, 0, 0, 1, 0, 0), None)
    tek, gor = [], set()  # aynı yere üst üste çizilmiş yapılar (gölge/dolgu katmanı) tek vurgu alır
    for x in out:
        a = (x[0], str(x[1]) if x[0] in ('ok', 'egri', 'yapi') else tuple(round(v / 4) for v in x[1][:3]))
        if a not in gor:
            gor.add(a); tek.append(x)
    return tek


def oto(key, rid, sec=None, en_cok=18, isaretci_sayi=3, bas=4, son=162):
    """Belge sırasıyla zamanlanmış katmanlar. sec: tür süzgeci ya da (ogeler)→ogeler işlevi."""
    o = ogeler(key, rid)
    if callable(sec):
        o = sec(o)
    # çok kalabalıksa önce halkalar, sonra küçük kutular azaltılır (oklar/eğriler korunur)
    while len(o) > en_cok:
        aday = [i for i, x in enumerate(o) if x[0] == 'halka'] or [i for i, x in enumerate(o) if x[0] == 'yapi'] or [i for i, x in enumerate(o) if x[0] == 'kutu']
        if not aday:
            o = o[:en_cok]; break
        j = min(aday, key=lambda i: o[i][3])
        o.pop(j)
    if not o:
        return []
    adim = (son - bas) / len(o)
    oklar = sorted([x for x in o if x[0] in ('ok', 'egri')], key=lambda x: -x[3])[:isaretci_sayi]
    k = []
    for i, (tur, v, h, _) in enumerate(o):
        t = bas + i * adim
        if tur in ('ok', 'egri'):
            t1 = t + max(10, min(40, adim * 1.6))
            k.append(iz(v, h, 9 if tur == 'ok' else 11, round(t), round(t1), 40))
            if (tur, v, h, _) in oklar:
                k.append(isaretci(v, h, round(t), round(t1), r=7))
        elif tur == 'kutu':
            X, Y, W, H, r = v
            k.append(nabiz(kutu(X, Y, W, H, min(r, 18), 5), h, round(t), 24, 28, 4))
        elif tur == 'yapi':
            k.append(nabiz(yol(v), h, round(t), 24, 28, 4))
        else:
            cx, cy, R = v
            k.append(nabiz(halka(cx, cy, R + 5), h, round(t), 24, 28, 4))
    return k


def plan(key, ozel=None):
    """Dersin tüm resimleri için PLAN sözlüğü; ozel = {rid: dict(oto parametreleri)}."""
    ozel = ozel or {}
    d = KOK / 'public' / 'ara_resim' / key
    return {p.stem: (lambda r=p.stem: oto(key, r, **ozel.get(r, {}))) for p in sorted(d.glob('r*.svg'))}


def bul(key, rid, bas):
    """SVG'de d'si `bas` ile başlayan <path>'in mutlak (M/L/C) biçimi — elle planlarda kaynakla birebir hizalama için."""
    kok = ET.parse(KOK / 'public' / 'ara_resim' / key / f'{rid}.svg').getroot()
    for e in kok.iter(NS + 'path'):
        if e.get('d', '').startswith(bas):
            return yaz(mutlak(e.get('d')))
    raise KeyError(f'{rid}: yol yok: {bas}')


def kullanimlar(key, rid, ref):
    """<use href="#ref"> ögelerinin çözülmüş konumları [(x, y, ölçek)] (x/y öznitelikleri + translate/scale)."""
    kok = ET.parse(KOK / 'public' / 'ara_resim' / key / f'{rid}.svg').getroot()
    out = []
    for e in kok.iter(NS + 'use'):
        h = e.get('href') or e.get('{http://www.w3.org/1999/xlink}href')
        if h != '#' + ref:
            continue
        m = _carp(_matris(e.get('transform')), (1, 0, 0, 1, float(e.get('x', 0)), float(e.get('y', 0))))
        out.append((m[4], m[5], math.hypot(m[0], m[1])))
    return out
