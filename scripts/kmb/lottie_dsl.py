"""KMB Lottie DSL — bölüm (chapter) zaman çizelgeli, bağımlılıksız Lottie üretimi.

Her animasyon bölümlerden oluşur; her bölümün bir anlatım cümlesi vardır. EMA sesi üretildiyse bölüm sınırları
sesteki cümle zamanlarına oturur (ses_02.json → `l-<ad>`), yoksa planlanan süreler kullanılır. Böylece video, sesle
kare kare eşzamanlıdır. Şekiller SVG yol söz dizimiyle (M L C Z, mutlak) yazılır.

Katman sırası: `A.ekle()` çağrı sırası alttan üste (sonra eklenen üstte çizilir).
"""
from __future__ import annotations

import math
import re

FR = 30


def renk(h: str, a: float = 1.0):
    h = h.lstrip('#')
    return [round(int(h[i:i + 2], 16) / 255, 4) for i in (0, 2, 4)] + [a]


def S(v):
    return {'a': 0, 'k': v}


def _yumusat(k, son):
    if not son:
        k['i'] = {'x': [0.42], 'y': [1]}
        k['o'] = {'x': [0.58], 'y': [0]}
    return k


def K(*ks):
    """Kare listesi: (kare, değer) çiftleri. Değer sayı ya da liste."""
    ks = sorted(ks, key=lambda x: x[0])
    if len(ks) == 1:
        v = ks[0][1]
        return S(v)
    out = []
    for i, (t, v) in enumerate(ks):
        out.append(_yumusat({'t': round(t, 2), 's': v if isinstance(v, list) else [v]}, i == len(ks) - 1))
    return {'a': 1, 'k': out}


def KD(*ks):
    """Doğrusal (sabit hızlı) kareler."""
    ks = sorted(ks, key=lambda x: x[0])
    out = []
    for i, (t, v) in enumerate(ks):
        k = {'t': round(t, 2), 's': v if isinstance(v, list) else [v]}
        if i < len(ks) - 1:
            k['i'] = {'x': [1], 'y': [1]}
            k['o'] = {'x': [0], 'y': [0]}
        out.append(k)
    return {'a': 1, 'k': out}


# ———————————————————————— SVG yolu → Lottie yolu + örnekleme

def _parca(d: str):
    tok = re.findall(r'[MLCZmlcz]|-?\d*\.?\d+(?:e-?\d+)?', d)
    i, cmd, P, out = 0, None, None, []
    alt = []
    while i < len(tok):
        t = tok[i]
        if t in 'MLCZmlcz':
            cmd = t.upper()
            i += 1
            if cmd == 'Z':
                out.append(('Z',))
            continue
        if cmd == 'M':
            P = (float(tok[i]), float(tok[i + 1])); i += 2
            out.append(('M', P)); cmd = 'L'
        elif cmd == 'L':
            Q = (float(tok[i]), float(tok[i + 1])); i += 2
            out.append(('L', P, Q)); P = Q
        elif cmd == 'C':
            c1 = (float(tok[i]), float(tok[i + 1])); c2 = (float(tok[i + 2]), float(tok[i + 3])); Q = (float(tok[i + 4]), float(tok[i + 5])); i += 6
            out.append(('C', P, c1, c2, Q)); P = Q
    return out


def yol(d: str):
    """SVG yolu → Lottie 'sh' (tek alt yol)."""
    v, ii, oo, kapali = [], [], [], False
    for s in _parca(d):
        if s[0] == 'M':
            v.append(list(s[1])); ii.append([0, 0]); oo.append([0, 0])
        elif s[0] == 'L':
            v.append(list(s[2])); ii.append([0, 0]); oo.append([0, 0])
        elif s[0] == 'C':
            _, p0, c1, c2, q = s
            oo[-1] = [c1[0] - p0[0], c1[1] - p0[1]]
            v.append(list(q)); ii.append([c2[0] - q[0], c2[1] - q[1]]); oo.append([0, 0])
        elif s[0] == 'Z':
            kapali = True
    if kapali and len(v) > 1 and abs(v[0][0] - v[-1][0]) < .01 and abs(v[0][1] - v[-1][1]) < .01:
        ii[0] = ii[-1]; v.pop(); ii.pop(); oo.pop()
    return {'ty': 'sh', 'ks': S({'c': kapali, 'v': v, 'i': ii, 'o': oo})}


def _nokta(s, t):
    if s[0] == 'L':
        _, a, b = s
        return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
    _, a, c1, c2, b = s
    m = 1 - t
    return tuple(m ** 3 * a[k] + 3 * m * m * t * c1[k] + 3 * m * t * t * c2[k] + t ** 3 * b[k] for k in (0, 1))


def ornekle(d: str, n: int = 60):
    """Yol üzerinde eşit aralıklı n+1 nokta."""
    seg = [s for s in _parca(d) if s[0] in 'LC']
    ince = []
    for s in seg:
        for j in range(40):
            ince.append(_nokta(s, j / 40))
    ince.append(_nokta(seg[-1], 1))
    uz = [0.0]
    for a, b in zip(ince, ince[1:]):
        uz.append(uz[-1] + math.dist(a, b))
    L = uz[-1]
    out, j = [], 0
    for k in range(n + 1):
        h = L * k / n
        while j < len(uz) - 2 and uz[j + 1] < h:
            j += 1
        a, b = ince[j], ince[j + 1]
        f = 0 if uz[j + 1] == uz[j] else (h - uz[j]) / (uz[j + 1] - uz[j])
        out.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))
    return out


# ———————————————————————— şekiller

def tr(p=(0, 0), a=(0, 0), s=(100, 100), r=0, o=100):
    return {'ty': 'tr', 'p': p if isinstance(p, dict) else S(list(p)), 'a': S(list(a)), 's': s if isinstance(s, dict) else S(list(s)),
            'r': r if isinstance(r, dict) else S(r), 'o': o if isinstance(o, dict) else S(o), 'sk': S(0), 'sa': S(0)}


def fl(h, a=1.0, o=100):
    # Lottie dolguda rengin alfası yok sayılır; saydamlık opaklık (o) ile verilir
    if not isinstance(o, dict):
        o = S(round(o * a, 1))
    return {'ty': 'fl', 'c': S(renk(h)), 'o': o, 'r': 1}


def gf(duraklar, bas, son, radyal=False, o=100):
    """Degrade dolgu. duraklar: [(konum 0–1, '#rrggbb'), …]"""
    k = []
    for p, h in duraklar:
        k += [p] + renk(h)[:3]
    return {'ty': 'gf', 'o': S(o), 'r': 1, 'g': {'p': len(duraklar), 'k': S(k)}, 's': S(list(bas)), 'e': S(list(son)), 't': 2 if radyal else 1}


def st(h, w=1.5, o=100, kesik=None, kesik_kayma=None):
    x = {'ty': 'st', 'c': S(renk(h)), 'o': o if isinstance(o, dict) else S(o), 'w': w if isinstance(w, dict) else S(w), 'lc': 2, 'lj': 2}
    if kesik:
        x['d'] = [{'n': 'd', 'nm': 'tire', 'v': S(kesik[0])}, {'n': 'g', 'nm': 'boşluk', 'v': S(kesik[1])},
                  {'n': 'o', 'nm': 'kayma', 'v': kesik_kayma or S(0)}]
    return x


def el(cx, cy, w, h):
    return {'ty': 'el', 'p': S([cx, cy]), 's': S([w, h]), 'd': 1}


def rc(cx, cy, w, h, r=0):
    return {'ty': 'rc', 'p': S([cx, cy]), 's': S([w, h]), 'r': S(r), 'd': 1}


def tm(e, s=None):
    """Kırpma: e (son) 0–100, kareli olabilir."""
    return {'ty': 'tm', 's': s if s is not None else S(0), 'e': e if isinstance(e, dict) else S(e), 'o': S(0), 'm': 1}


def G(*it, p=(0, 0), a=(0, 0), s=(100, 100), r=0, o=100):
    return {'ty': 'gr', 'it': [*it, tr(p, a, s, r, o)]}


def kamera_ekle(k, t0, sure, cx, cy, z):
    """Kamera karesi ekle: t0'dan önceki en son konumdan (zamanca) sure sn'de yeni konuma; sonraki karelerle çakışan
    eski kareler korunur (sıralama json'da)."""
    once = max((x for x in k if x[0] <= t0), key=lambda x: x[0], default=(0.0, 400, 250, 100))
    k[:] = [x for x in k if not (t0 < x[0] <= t0 + sure)]
    if t0 > once[0]:
        k.append((round(t0, 3), *once[1:]))
    k.append((round(t0 + sure, 3), cx, cy, z))


class Anim:
    def __init__(self, ad: str, baslik: str, bolumler: list[dict], zaman: list[list[float]] | None = None, bekle: float = 2.0):
        self.ad, self.baslik, self.bolumler = ad, baslik, bolumler
        # Bölüm sınırları video saatinde (sn). Her bölümden sonra `bekle` sn sessiz pay (bölümde 'bekle' ile değişir):
        # animasyon sesi bitince de sürer, öğrenci görüntüyü sindirir. Ses saati (ses_sinir) ayrı tutulur; oynatıcı
        # bölüm başında sesi ses_sinir'den başlatır, payda sesi durdurur.
        self.ses_sinir = [(a, b) for a, b in zaman] if zaman and len(zaman) == len(bolumler) else None
        t, self.sinir = 0.8, []
        for i, b in enumerate(bolumler):
            uz = (self.ses_sinir[i][1] - self.ses_sinir[i][0]) if self.ses_sinir else b['sure']
            self.sinir.append((t, t + uz))
            t += uz + b.get('bekle', bekle)
        self.sure = t + 0.4
        self.kamera_k = [(0.0, 400, 250, 100)]
        self.varliklar = []
        self.op = round(self.sure * FR)
        self.katmanlar = []
        self.etiketler = []
        self.sayaclar = []

    def T(self, i: int, f: float = 0.0) -> float:
        """i. bölümün f kesirindeki kare (f 0..1; 1 = bölüm sonu; i = len → video sonu)."""
        if i >= len(self.sinir):
            return self.op - 1
        a, b = self.sinir[i]
        return (a + (b - a) * f) * FR

    def ekle(self, nm, *shapes, p=None, s=None, o=None, r=None, a=(0, 0)):
        self.katmanlar.append({'ddd': 0, 'ind': len(self.katmanlar) + 1, 'ty': 4, 'nm': nm, 'sr': 1, 'ip': 0, 'op': self.op, 'st': 0, 'bm': 0, 'ao': 0,
                               'ks': {'o': o or S(100), 'r': r or S(0), 'p': p or S([0, 0, 0]), 'a': S([a[0], a[1], 0]), 's': s or S([100, 100, 100])},
                               'shapes': list(shapes)})

    def gor(self, bas, son=None, f=8, deger=100):
        """Görünürlük: bas karesinde belirir, son karesinde kaybolur."""
        ks = [(0, 0), (max(0, bas), 0), (bas + f, deger)] if bas > 0 else [(0, deger)]
        if son is not None:
            ks += [(son, deger), (son + f, 0)]
        return K(*ks)

    def etiket(self, b1, b2, x, y, metin, tur='etiket'):
        """HTML katmanı (oynatıcı çizer): b1..b2 bölümleri arasında (x, y)'de etiket."""
        self.etiketler.append({'bas': round(self.T(b1) / FR, 2), 'son': round(self.T(b2, 1) / FR, 2), 'x': x, 'y': y, 'metin': metin, 'tur': tur})

    def sayac(self, b1, f1, b2, f2, v1, v2, birim, x, y, ondalik=0):
        self.sayaclar.append({'bas': round(self.T(b1, f1) / FR, 2), 'son': round(self.T(b2, f2) / FR, 2), 'v1': v1, 'v2': v2,
                              'birim': birim, 'x': x, 'y': y, 'ondalik': ondalik})

    def boyunca(self, d, k1, k2, n=50, ofset=(0, 0)):
        """Yol boyunca konum kareleri (sabit hız)."""
        P = ornekle(d, n)
        return KD(*[(k1 + (k2 - k1) * i / n, [x + ofset[0], y + ofset[1], 0]) for i, (x, y) in enumerate(P)])

    def kamera(self, b: int, cx: float, cy: float, z: float = 100, f: float = 0.0, sure: float = 1.4):
        """Kamera: b. bölümün f kesirinden başlayıp `sure` sn'de (cx, cy) merkezine z% yakınlaşır (100 = tüm sahne)."""
        t0 = self.T(b, f) / FR
        kamera_ekle(self.kamera_k, t0, sure, cx, cy, z)

    def json(self):
        L = list(reversed(self.katmanlar))
        if len(self.kamera_k) > 1:
            k = sorted(self.kamera_k)
            for x in L:
                x['parent'] = 999  # precomp katmanları da kameraya bağlı
            L.append({'ddd': 0, 'ind': 999, 'ty': 3, 'nm': 'kamera', 'sr': 1, 'ip': 0, 'op': self.op, 'st': 0, 'bm': 0, 'ao': 0,
                      'ks': {'o': S(100), 'r': S(0), 'p': S([400, 250, 0]),
                             'a': K(*[(t * FR, [cx, cy, 0]) for t, cx, cy, z in k]),
                             's': K(*[(t * FR, [z, z, 100]) for t, cx, cy, z in k])}})
        return {'v': '5.7.4', 'fr': FR, 'ip': 0, 'op': self.op, 'w': 800, 'h': 500, 'nm': self.ad, 'ddd': 0, 'assets': self.varliklar, 'layers': L}

    def bilgi(self):
        return {'ad': self.ad, 'baslik': self.baslik, 'sure': round(self.sure, 2),
                'bolumler': [{'baslik': b['baslik'], 'metin': b['metin'], 'bas': round(a, 2), 'son': round(c, 2),
                              **({'ses_bas': round(self.ses_sinir[i][0], 3)} if self.ses_sinir else {})}
                             for i, (b, (a, c)) in enumerate(zip(self.bolumler, self.sinir))],
                'kamera': [[round(t, 3), cx, cy, z] for t, cx, cy, z in sorted(self.kamera_k)] if len(self.kamera_k) > 1 else [],
                'etiketler': self.etiketler, 'sayaclar': self.sayaclar}


def yol_morph(d1: str, d2: str, k1: float, k2: float):
    """İki SVG yolu arasında şekil değiştirme (aynı komut dizisi, aynı nokta sayısı)."""
    a, b = yol(d1)['ks']['k'], yol(d2)['ks']['k']
    assert len(a['v']) == len(b['v']), (len(a['v']), len(b['v']))
    return {'ty': 'sh', 'ks': {'a': 1, 'k': [
        {'t': round(k1, 2), 's': [a], 'i': {'x': .42, 'y': 1}, 'o': {'x': .58, 'y': 0}},
        {'t': round(k2, 2), 's': [b]}]}}


class Ic:
    """Alt kompozisyon bağdaştırıcısı: bir sahne üreticisi (lottie_uret.py) kendi bölümleriyle yazılmıştır; `harita` her
    bölümünü adım videosunun bir cümlesine eşler (aynı cümleye düşen bölümler o cümlenin süresini eşit paylaşır; None = hiç
    oynamaz). Katmanlar ayrı bir precomp'a gider; etiket/sayaç/kamera adım videosuna aktarılır."""

    def __init__(self, ust: 'Anim', harita):
        self.ust, self.harita, self.katmanlar = ust, harita, []
        self.op = ust.op
        self.ad = ust.ad

    def T(self, i, f=0.0):
        if i >= len(self.harita) or self.harita[i] is None:
            return self.ust.op + 2000 + i * 100
        j = self.harita[i]
        ayni = [k for k, h in enumerate(self.harita) if h == j]
        r = ayni.index(i)
        return self.ust.T(j, (r + f) / len(ayni))

    def ekle(self, nm, *shapes, p=None, s=None, o=None, r=None, a=(0, 0)):
        self.katmanlar.append({'ddd': 0, 'ind': len(self.katmanlar) + 1, 'ty': 4, 'nm': nm, 'sr': 1, 'ip': 0, 'op': self.ust.op, 'st': 0, 'bm': 0, 'ao': 0,
                               'ks': {'o': o or S(100), 'r': r or S(0), 'p': p or S([0, 0, 0]), 'a': S([a[0], a[1], 0]), 's': s or S([100, 100, 100])},
                               'shapes': list(shapes)})

    gor = Anim.gor
    boyunca = Anim.boyunca

    def etiket(self, b1, b2, x, y, metin, tur='etiket'):
        if self.harita[b1] is None or self.harita[b2] is None:
            return
        self.ust.etiketler.append({'bas': round(self.T(b1) / FR, 2), 'son': round(self.T(b2, 1) / FR, 2), 'x': x, 'y': y, 'metin': metin, 'tur': tur})

    def sayac(self, b1, f1, b2, f2, v1, v2, birim, x, y, ondalik=0):
        if self.harita[b1] is None or self.harita[b2] is None:
            return
        self.ust.sayaclar.append({'bas': round(self.T(b1, f1) / FR, 2), 'son': round(self.T(b2, f2) / FR, 2), 'v1': v1, 'v2': v2,
                                  'birim': birim, 'x': x, 'y': y, 'ondalik': ondalik})

    def kamera(self, b, cx, cy, z=100, f=0.0, sure=1.4):
        if b >= len(self.harita) or self.harita[b] is None:
            return
        t0 = self.T(b, f) / FR
        kamera_ekle(self.ust.kamera_k, t0, sure, cx, cy, z)


def ic_ekle(ust: 'Anim', uretici, harita, gorunur, nm='ic'):
    """Üreticiyi alt kompozisyon olarak ekler. gorunur: [(ilk cümle, son cümle), …] görünür olduğu aralıklar."""
    import lottie_uret as LU
    I = Ic(ust, harita)
    LU._IC = I
    try:
        uretici(None)
    finally:
        LU._IC = None
    rid = f'p{len(ust.varliklar)}'
    ust.varliklar.append({'id': rid, 'layers': list(reversed(I.katmanlar))})
    ks = [(0, 0)]
    for b1, b2 in gorunur:
        ks += [(max(1, ust.T(b1) - 8), 0), (ust.T(b1), 100), (ust.T(b2, 1) + 10, 100), (ust.T(b2, 1) + 18, 0)]
    ust.katmanlar.append({'ddd': 0, 'ind': len(ust.katmanlar) + 1, 'ty': 0, 'nm': nm, 'refId': rid, 'sr': 1, 'ao': 0, 'w': 800, 'h': 500,
                          'ip': 0, 'op': ust.op, 'st': 0, 'bm': 0,
                          'ks': {'o': K(*ks), 'r': S(0), 'p': S([0, 0, 0]), 'a': S([0, 0, 0]), 's': S([100, 100, 100])}})
