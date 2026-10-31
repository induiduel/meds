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


def fl_cift(h, o=100):
    """Çift-tek dolgu: aynı gruptaki ikinci yol delik açar (delikli örtü gibi)."""
    return {'ty': 'fl', 'c': S(renk(h)), 'o': S(o), 'r': 2}


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
    """Şekil grubu. Lottie'de grupta önce gelen öge üstte çizilir; burada yazım sırası alttan üste olsun diye iç gruplar
    ve ardışık şekil/boya blokları ters sıralanır (bloğun kendi içi — şekil, dolgu, çizgi, kırpma — korunur)."""
    bloklar, cari = [], []
    for x in it:
        if x.get('ty') == 'gr':
            if cari:
                bloklar.append(cari); cari = []
            bloklar.append([x])
        else:
            cari.append(x)
    if cari:
        bloklar.append(cari)
    if len(bloklar) > 1 and any(b[0].get('ty') == 'gr' for b in bloklar):
        it = [x for b in reversed(bloklar) for x in b]
    return {'ty': 'gr', 'it': [*it, tr(p, a, s, r, o)]}


def kamera_ekle(k, t0, sure, cx, cy, z):
    """Kamera hareketi ekle: t0'dan başlayıp `sure` sn'de (cx, cy, z)'ye. Hareketler bir liste olarak tutulur ve
    `kamera_coz` ile ZAMAN SIRASIYLA çözülür: her hareket, kendinden önceki hareketin t0 anındaki gerçek konumundan başlar.
    (Eski sürüm başlangıç anahtarını ekleme anındaki son konumdan kopyalıyordu; araya sonradan eklenen bir hareket — ör.
    zemin_kat'ın kamera sıfırlaması — sonraki hareketi bozmuyor, kamera cümle boyunca kayıyordu.) Aynı ana (≤1 kare) düşen
    eski hareketin yerine yenisi geçer."""
    # kadraj sahne dışına taşmasın: yakınlaşmada merkez sınırlanır
    if z >= 100:
        rx, ry = 400 * 100 / z, 250 * 100 / z
        cx, cy = min(800 - rx, max(rx, cx)), min(500 - ry, max(ry, cy))
    k[:] = [x for x in k if abs(x[0] - t0) >= 1 / FR]
    k.append((round(t0, 3), sure, cx, cy, z))


def _yumusak(f):
    return f * f * (3 - 2 * f)


def kamera_coz(hareketler):
    """Hareket listesi → kamera anahtarları [(t, cx, cy, z)] (oynatıcıdaki kameraAn ile aynı biçim)."""
    keys = [(0.0, 400, 250, 100)]
    for t0, sure, cx, cy, z in sorted(hareketler, key=lambda x: x[0]):
        son = keys[-1]
        if t0 < son[0] and len(keys) > 1:  # önceki geçiş bitmeden yeni hareket: geçiş t0'da kesilir
            onc = keys[-2]
            e = _yumusak((t0 - onc[0]) / max(1e-6, son[0] - onc[0]))
            keys[-1] = (t0, *[a + (b - a) * e for a, b in zip(onc[1:], son[1:])])
        elif t0 > son[0]:
            keys.append((t0, *son[1:]))
        keys.append((round(t0 + sure, 3), cx, cy, z))
    out = []
    for x in keys:
        x = (round(x[0], 3), *[round(v, 2) for v in x[1:]])
        if out and x[0] - out[-1][0] < 1 / FR:
            out[-1] = x
        else:
            out.append(x)
    return out


def kamera_an(keys, t):
    """kamera_coz anahtarlarında t anındaki (cx, cy, z) — LottieVideo.tsx kameraAn ile aynı (smoothstep)."""
    if not keys or t <= keys[0][0]:
        return keys[0][1:] if keys else (400, 250, 100)
    for a, b in zip(keys, keys[1:]):
        if t <= b[0]:
            e = _yumusak(1 if b[0] == a[0] else (t - a[0]) / (b[0] - a[0]))
            return tuple(p + (q - p) * e for p, q in zip(a[1:], b[1:]))
    return keys[-1][1:]


# ———————————————————————— etiket yerleşimi (oynatıcının HTML katmanı: LottieVideo.tsx › Katman + kmb.css)
# Oynatıcı etiketi sahne koordinatından kamerayla ekrana taşır, merkezini yatayda %12–88, dikeyde %8–72'ye sıkıştırır, yatayda
# %26 / dikeyde %8'den yakın etiketi aşağı-yukarı iter, 46cqi'den uzun yazıyı "…" ile keser; alt %24 altyazınındır.
# Telefonda (sahne ≈ 400 px) yazı 10 px tabana oturur: harf ≈ 11, iç boşluk 30 birim (800'lük sahne biriminde).
ETIKET_AZAMI = 30          # harf; daha uzunu telefonda kesilir
ET_Y = (40, 356)           # etiket merkezi ekranda (800×500 birim): üst %8 – altyazı bölgesinin (alt %24) üstü
ET_ITME = (208, 41)        # oynatıcının itme eşiği (%26 yatay, %8 dikey) + pay


def etiket_gen(metin):
    return min(368, len(metin) * 11 + 30)


def _x_aralik(metin):
    w = etiket_gen(metin)
    return max(96, w / 2 + 6), min(704, 794 - w / 2)


def etiket_durumlari(keys, bas, son):
    """Etiketin ömrü boyunca kameranın durduğu konumlar (geçiş sonları) + bas anı."""
    d = [kamera_an(keys, bas)]
    for t, *v in keys:
        if bas < t <= son:
            d.append(tuple(v))
    t = bas + .25
    while t < son:  # geçiş ortaları da (kamera sürekli kayarken etiket kadrajdan çıkmasın)
        d.append(kamera_an(keys, t))
        t += .25
    return d


def etiket_yerlestir(etiketler, keys, sure):
    """Etiketleri kadraja ve altyazı bölgesinin üstüne oturtur, aynı anda görünenleri oynatıcının itme eşiğinin dışına
    ayırır; kamera geçişi sırasında başlayan etiket geçiş bitince belirir. Sahne koordinatı (x, y) değiştirilir."""
    yerlesen = []
    for e in sorted(etiketler, key=lambda e: e['bas']):
        # kamera geçişinin ortasında belirme: geçiş bitince belir (etiket kaymasın)
        for a, b in zip(keys, keys[1:]):
            if a[0] <= e['bas'] < b[0] and a[1:] != b[1:] and b[0] < e['son'] - .6:
                e['bas'] = round(b[0], 2)
        dur = etiket_durumlari(keys, e['bas'], e['son'])
        xl, xh = _x_aralik(e['metin'])

        def aralik(dd):
            lo_x = max(cx + (xl - 400) * 100 / z for cx, cy, z in dd); hi_x = min(cx + (xh - 400) * 100 / z for cx, cy, z in dd)
            lo_y = max(cy + (ET_Y[0] - 250) * 100 / z for cx, cy, z in dd); hi_y = min(cy + (ET_Y[1] - 250) * 100 / z for cx, cy, z in dd)
            return lo_x, hi_x, lo_y, hi_y
        lo_x, hi_x, lo_y, hi_y = aralik(dur)
        if lo_x > hi_x or lo_y > hi_y:  # kamera etiketi kadrajdan atıyor: etiket ilk kamera hareketinde biter
            sonraki = [t for t, *v in keys if e['bas'] < t <= e['son']]
            if sonraki:
                e['son'] = round(max(e['bas'] + .5, sonraki[0]), 2)  # sonraki = kayan hareketin başladığı an
            dur = dur[:1]
            lo_x, hi_x, lo_y, hi_y = aralik(dur)
        e['x'] = round(min(hi_x, max(lo_x, e['x'])), 1)
        e['y'] = round(min(hi_y, max(lo_y, e['y'])), 1)
        cx, cy, z = dur[0]
        ekr = lambda x, y: (400 + (x - cx) * z / 100, 250 + (y - cy) * z / 100)  # noqa: E731
        diger = [o for o in yerlesen if o['bas'] < e['son'] and e['bas'] < o['son']]
        def carpisir(y):
            sx, sy = ekr(e['x'], y)
            for o in diger:
                ox, oy = ekr(o['x'], o['y'])
                if abs(ox - sx) < ET_ITME[0] and abs(oy - sy) < ET_ITME[1]:
                    return True
            return False
        if carpisir(e['y']):
            for d in (44, -44, 88, -88, 132, -132, 176, -176):
                y = e['y'] + d * 100 / z
                if lo_y <= y <= hi_y and not carpisir(y):
                    e['y'] = round(y, 1)
                    break
        yerlesen.append(e)


def etiket_denetle(v):
    """Kapı (dogrula.py): bilgi() çıktısındaki etiketler kesilmeden, kadrajda, altyazının üstünde ve çakışmadan görünür mü."""
    H = []
    keys = [tuple(k) for k in v.get('kamera') or []] or [(0.0, 400, 250, 100)]
    for e in v['etiketler']:
        if len(e['metin']) > ETIKET_AZAMI:
            H.append(f'etiket {ETIKET_AZAMI} harften uzun (telefonda kesilir): "{e["metin"]}"')
        xl, xh = _x_aralik(e['metin'])
        for cx, cy, z in etiket_durumlari(keys, e['bas'], e['son']):
            sx, sy = 400 + (e['x'] - cx) * z / 100, 250 + (e['y'] - cy) * z / 100
            if not (xl - 2 <= sx <= xh + 2 and ET_Y[0] - 2 <= sy <= ET_Y[1] + 2):
                H.append(f'etiket kadraj/altyazı bölgesi dışında ({sx:.0f},{sy:.0f}) @{e["bas"]}: "{e["metin"]}"')
                break
    es = v['etiketler']
    for i, a in enumerate(es):
        for b in es[:i]:
            t = max(a['bas'], b['bas'])
            if t < min(a['son'], b['son']) - .05:
                cx, cy, z = kamera_an(keys, t)
                if abs(a['x'] - b['x']) * z / 100 < ET_ITME[0] - 2 and abs(a['y'] - b['y']) * z / 100 < ET_ITME[1] - 3:
                    H.append(f'etiketler üst üste @{t}: "{a["metin"]}" ↔ "{b["metin"]}"')
    if v.get('sayaclar') and any(s.get('gizle') for s in v['sayaclar']):
        H.append('gizlenmesi gereken sayaç etikete çevrilmemiş')
    return [f'{v["ad"]}: {h}' for h in H]


def sayac_etiketle(s, adim=8):
    """Oynatıcı sayacı bas'tan videonun sonuna dek gösterir (bitiş yok). Bir sahneye ait sayaç (gizle zamanı olan) adım adım
    değişen etiketlere çevrilir; son değer sahne kaybolunca kalkar."""
    n = max(1, min(adim, int(abs(s['v2'] - s['v1'])) or 1))
    out = []
    for i in range(n + 1):
        t1 = s['bas'] + (s['son'] - s['bas']) * i / n
        t2 = s['bas'] + (s['son'] - s['bas']) * (i + 1) / n if i < n else s['gizle']
        v = s['v1'] + (s['v2'] - s['v1']) * i / n
        if t1 >= s['gizle'] - .2:
            break
        out.append({'bas': round(t1, 2), 'son': round(min(t2, s['gizle']), 2), 'x': s['x'], 'y': s['y'],
                    'metin': f'{v:.{s["ondalik"]}f} {s["birim"]}'.replace('.', ','), 'tur': 'sayac'})
    return out


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
        self.kamera_k = []  # kamera hareketleri (t0, süre, cx, cy, z); kamera_coz ile çözülür
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
                               'shapes': list(reversed(shapes))})  # Lottie'de önce gelen grup üstte: çağrı sırası alttan üste

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

    def kamera_temiz(self):
        return kamera_coz(self.kamera_k)

    def kamera_sabit(self, b1, b2, cx=400, cy=250, z=100):
        """b1..b2 cümleleri boyunca kamerayı sabitle (alt kompozisyonların yakınlaşmasını ezer)."""
        t1, t2 = self.T(b1) / FR, self.T(b2, 1) / FR
        self.kamera_k[:] = [x for x in self.kamera_k if not (t1 - .01 <= x[0] <= t2 + .01)]
        kamera_ekle(self.kamera_k, t1, 0.5, cx, cy, z)

    @staticmethod
    def etkin_aralik(katmanlar, op):
        """Başarım: her katman yalnız görünür olduğu aralıkta etkin (ip/op). Gizli katmanlar oynatıcıda hiç işlenmez."""
        for L in katmanlar:
            o = L['ks']['o']
            if not o.get('a'):
                if o.get('k') == 0:
                    L['ip'], L['op'] = 0, 1
                continue
            ks = o['k']
            deg = lambda k: (k['s'][0] if isinstance(k.get('s'), list) else k.get('s', 0))  # noqa: E731
            bas, bit = None, None
            for i, k in enumerate(ks):
                v = deg(k)
                sonraki = ks[i + 1] if i + 1 < len(ks) else None
                if v > 0 or (sonraki and deg(sonraki) > 0):
                    if bas is None:
                        bas = k['t'] if v > 0 else k['t']
                    bit = sonraki['t'] if (sonraki and not (v > 0 and deg(sonraki) > 0 and False)) else op
                    if v > 0 and sonraki is None:
                        bit = op
            if bas is None:
                L['ip'], L['op'] = 0, 1
            else:
                if deg(ks[0]) > 0:
                    bas = 0
                if deg(ks[-1]) > 0:
                    bit = op
                L['ip'], L['op'] = max(0, int(bas) - 1), min(op, int(bit) + 2)

    def json(self):
        Anim.etkin_aralik(self.katmanlar, self.op)
        for a in self.varliklar:
            Anim.etkin_aralik(a['layers'], self.op)
        L = list(reversed(self.katmanlar))
        if self.kamera_k:
            k = self.kamera_temiz()
            for x in L:
                x['parent'] = 999  # precomp katmanları da kameraya bağlı
            L.append({'ddd': 0, 'ind': 999, 'ty': 3, 'nm': 'kamera', 'sr': 1, 'ip': 0, 'op': self.op, 'st': 0, 'bm': 0, 'ao': 0,
                      'ks': {'o': S(100), 'r': S(0), 'p': S([400, 250, 0]),
                             'a': K(*[(t * FR, [cx, cy, 0]) for t, cx, cy, z in k]),
                             's': K(*[(t * FR, [z, z, 100]) for t, cx, cy, z in k])}})
        return {'v': '5.7.4', 'fr': FR, 'ip': 0, 'op': self.op, 'w': 800, 'h': 500, 'nm': self.ad, 'ddd': 0, 'assets': self.varliklar, 'layers': L}

    def bilgi(self):
        kam = self.kamera_temiz() if self.kamera_k else []
        sayac, etiket = [], [dict(e) for e in self.etiketler]
        for x in self.sayaclar:
            if x.get('gizle') is not None and x['gizle'] < self.sure - .3:
                etiket += sayac_etiketle(x)
            else:
                sayac.append({k: v for k, v in x.items() if k != 'gizle'})
        # sürekli sayaç (sahnenin sonuna dek görünen) da kadraja oturtulur; kamera onu kadrajdan atıyorsa etikete çevrilir
        sanal = [{'bas': x['bas'], 'son': self.sure, 'x': x['x'], 'y': x['y'], 'metin': f'{max(abs(x["v1"]), abs(x["v2"])):.{x["ondalik"]}f} {x["birim"]}'}
                 for x in sayac]
        etiket_yerlestir(sanal, kam or [(0.0, 400, 250, 100)], self.sure)
        kalan = []
        for x, e in zip(sayac, sanal):
            x['x'], x['y'] = e['x'], e['y']
            if e['son'] < self.sure - .3:
                etiket += sayac_etiketle({**x, 'gizle': e['son']})
            else:
                kalan.append(x)
        sayac = kalan
        etiket_yerlestir(etiket, kam or [(0.0, 400, 250, 100)], self.sure)
        return {'ad': self.ad, 'baslik': self.baslik, 'sure': round(self.sure, 2),
                'bolumler': [{'baslik': b['baslik'], 'metin': b['metin'], 'bas': round(a, 2), 'son': round(c, 2),
                              **({'ses_bas': round(self.ses_sinir[i][0], 3)} if self.ses_sinir else {})}
                             for i, (b, (a, c)) in enumerate(zip(self.bolumler, self.sinir))],
                'kamera': [[round(t, 3), cx, cy, z] for t, cx, cy, z in kam],
                'etiketler': sorted(etiket, key=lambda e: e['bas']), 'sayaclar': sayac}


def yol_morph(d1: str, d2: str, k1: float, k2: float):
    """İki SVG yolu arasında şekil değiştirme (aynı komut dizisi, aynı nokta sayısı)."""
    a, b = yol(d1)['ks']['k'], yol(d2)['ks']['k']
    assert len(a['v']) == len(b['v']), (len(a['v']), len(b['v']))
    return {'ty': 'sh', 'ks': {'a': 1, 'k': [
        {'t': round(k1, 2), 's': [a], 'i': {'x': .42, 'y': 1}, 'o': {'x': .58, 'y': 0}},
        {'t': round(k2, 2), 's': [b]}]}}


class Ic:
    """Alt kompozisyon bağdaştırıcısı: bir sahne üreticisi (lottie_uret.py) kendi bölümleriyle yazılmıştır; `harita` her
    bölümünü adım videosunun bir cümlesine eşler (aynı cümleye düşen bölümler o cümlenin süresini eşit paylaşır).
    Eşlenmeyen bölüm:
      · None, eşlenmiş bir bölümden ÖNCE ya da 'once' → "olmuş bitmiş": bölüm, sahne görünmeden hemen önceki sessiz
        payda (bir sonraki eşlenmiş bölümün cümlesinden ~0,3–0,9 sn önce) sıkıştırılarak oynar; sonraki bölümler doğru
        durumdan başlar (ör. dolu mesane → küçülen mesane). Etiket/sayaç/kamera hareketi taşımaz.
      · None, son eşlenmiş bölümden SONRA → hiç oynamaz (video sonrasına atılır).
    (Eski sürümde her None bölüm video sonrasına atılıyordu; önceki bölümün anahtarları geleceğe gidince Lottie anahtarları
    zamanca yeniden sıralanıyor, eşlenen bölüm yanlış durumdan başlıyordu — sistitte mesane cümle boyunca şişip küçülüyordu.)
    Katmanlar ayrı bir precomp'a gider; etiket/sayaç/kamera adım videosuna aktarılır."""

    def __init__(self, ust: 'Anim', harita, bas=None):
        self.ust, self.harita, self.katmanlar = ust, list(harita), []
        self.op = ust.op
        self.ad = ust.ad
        self.bas = bas  # sahnenin görünmeye başladığı cümle ('once' bölümlerin dayanağı)
        n = len(self.harita)
        self.sikis = {}  # bölüm → (dayanak cümle, sıra, adet)
        i = 0
        while i < n:
            if not isinstance(self.harita[i], int):
                j = i
                while j < n and not isinstance(self.harita[j], int):
                    j += 1
                dayanak = self.harita[j] if j < n else None
                for r, k in enumerate(range(i, j)):
                    d = dayanak if (dayanak is not None or self.harita[k] == 'once') else None
                    if self.harita[k] == 'once' and d is None:
                        d = bas
                    if d is not None:
                        self.sikis[k] = (d, r, j - i)
                i = j
            else:
                i += 1

    def esli(self, i):
        return i < len(self.harita) and isinstance(self.harita[i], int)

    def T(self, i, f=0.0):
        if i >= len(self.harita):
            return self.ust.op + 2000 + i * 100
        if i in self.sikis:
            d, r, adet = self.sikis[i]
            a1 = max(3.0, self.ust.T(d) - 10)
            a0 = max(1.0, min(a1 - 2, self.ust.T(d) - 26))
            return a0 + (a1 - a0) * (r + f) / adet
        if not self.esli(i):
            return self.ust.op + 2000 + i * 100
        j = self.harita[i]
        ayni = [k for k, h in enumerate(self.harita) if h == j]
        r = ayni.index(i)
        return self.ust.T(j, (r + f) / len(ayni))

    def ekle(self, nm, *shapes, p=None, s=None, o=None, r=None, a=(0, 0)):
        self.katmanlar.append({'ddd': 0, 'ind': len(self.katmanlar) + 1, 'ty': 4, 'nm': nm, 'sr': 1, 'ip': 0, 'op': self.ust.op, 'st': 0, 'bm': 0, 'ao': 0,
                               'ks': {'o': o or S(100), 'r': r or S(0), 'p': p or S([0, 0, 0]), 'a': S([a[0], a[1], 0]), 's': s or S([100, 100, 100])},
                               'shapes': list(reversed(shapes))})  # Lottie'de önce gelen grup üstte: çağrı sırası alttan üste

    gor = Anim.gor
    boyunca = Anim.boyunca

    def etiket(self, b1, b2, x, y, metin, tur='etiket'):
        if not (self.esli(b1) and self.esli(b2)):
            return
        self.ust.etiketler.append({'bas': round(self.T(b1) / FR, 2), 'son': round(self.T(b2, 1) / FR, 2), 'x': x, 'y': y, 'metin': metin, 'tur': tur})

    def sayac(self, b1, f1, b2, f2, v1, v2, birim, x, y, ondalik=0):
        if not (self.esli(b1) and self.esli(b2)):
            return
        self.ust.sayaclar.append({'bas': round(self.T(b1, f1) / FR, 2), 'son': round(self.T(b2, f2) / FR, 2), 'v1': v1, 'v2': v2,
                                  'birim': birim, 'x': x, 'y': y, 'ondalik': ondalik})

    def kamera(self, b, cx, cy, z=100, f=0.0, sure=1.4):
        if not self.esli(b):
            return
        t0 = self.T(b, f) / FR
        kamera_ekle(self.ust.kamera_k, t0, sure, cx, cy, z)


def ic_ekle(ust: 'Anim', uretici, harita, gorunur, nm='ic'):
    """Üreticiyi alt kompozisyon olarak ekler. gorunur: [(ilk cümle, son cümle), …] görünür olduğu aralıklar.
    Sahnenin sayaçları görünürlük bitince kalkar (bilgi() onları etikete çevirir: oynatıcı sayacı hiç kaldırmaz)."""
    import lottie_uret as LU
    I = Ic(ust, harita, bas=min(b1 for b1, _ in gorunur))
    n_say = len(ust.sayaclar)
    LU._IC = I
    try:
        uretici(None)
    finally:
        LU._IC = None
    for x in ust.sayaclar[n_say:]:
        bitis = [ust.T(b2, 1) / FR + .3 for b1, b2 in gorunur if ust.T(b1) / FR - .5 <= x['bas'] <= ust.T(b2, 1) / FR + .5]
        x['gizle'] = round(bitis[0], 2) if bitis else x['son']
    rid = f'p{len(ust.varliklar)}'
    ust.varliklar.append({'id': rid, 'layers': list(reversed(I.katmanlar))})
    ks = [(0, 0)]
    for b1, b2 in gorunur:
        ks += [(max(1, ust.T(b1) - 8), 0), (ust.T(b1), 100), (ust.T(b2, 1) + 10, 100), (ust.T(b2, 1) + 18, 0)]
    ust.katmanlar.append({'ddd': 0, 'ind': len(ust.katmanlar) + 1, 'ty': 0, 'nm': nm, 'refId': rid, 'sr': 1, 'ao': 0, 'w': 800, 'h': 500,
                          'ip': 0, 'op': ust.op, 'st': 0, 'bm': 0,
                          'ks': {'o': K(*ks), 'r': S(0), 'p': S([0, 0, 0]), 'a': S([0, 0, 0]), 's': S([100, 100, 100])}})


# ———————————————————————— ortak eller (eldivenli). Yerel eksen: nesne yumruğun içinden soldan sağa (y=0) geçer.

ELDIVEN_STERIL = [(0, '#fbf3e6'), (1, '#e7d3b3')]  # 2B palet (docs/KMB_2B_STIL.md)
ELDIVEN_MAVI = [(0, '#dcedf9'), (1, '#b3d4ec')]


def yumruk(cx, cy, s=1.0, r=0, steril=True):
    """Yandan görülen, bir şeyi kavrayan eldivenli el: bilek sağda, dört parmak boğumu solda, başparmak üstte kapanır."""
    g = ELDIVEN_STERIL if steril else ELDIVEN_MAVI
    k = '#b59c72' if steril else '#6f8bb3'
    parcalar = [
        G(yol('M20 -42 C70 -50 130 -44 180 -34 L180 36 C130 46 70 50 20 44 Z'), gf(g, (20, -40), (180, 40)), st(k, 2)),
        G(yol('M-54 -40 C-54 -52 30 -54 34 -40 L36 40 C32 54 -52 54 -54 40 Z'), gf(g, (-50, -50), (30, 50)), st(k, 2)),
        *[G(el(-46, y, 34, 24), gf(g, (-60, y - 10), (-30, y + 12)), st(k, 1.6)) for y in (-30, -10, 10, 30)],
        *[G(yol(f'M-30 {y - 9} C-24 {y - 4} -24 {y + 4} -30 {y + 9}'), st(k, 1.2, o=70)) for y in (-30, -10, 10, 30)],
        G(yol('M24 -40 C0 -62 -40 -58 -60 -30 C-66 -20 -56 -12 -46 -18 C-30 -34 -6 -38 14 -24 Z'), gf(g, (-50, -60), (20, -20)), st(k, 2)),
        G(yol('M-20 -50 C-8 -54 6 -52 14 -46'), st('#ffffff', 2.5, o=60)),
    ]
    return G(*parcalar, p=(cx, cy), s=(100 * s, 100 * s), r=r)


def parmak_ucu(cx, cy, r=0, s=1.0, steril=True):
    """Tek parmak (uç solda): sıkıştırma, ayırma gibi işlerde. Uç (cx, cy)'dedir."""
    g = ELDIVEN_STERIL if steril else ELDIVEN_MAVI
    k = '#b59c72' if steril else '#6f8bb3'
    return G(G(yol('M0 -17 C-14 -17 -20 -8 -20 0 C-20 8 -14 17 0 17 L150 20 L150 -20 Z'), gf(g, (0, -20), (0, 20)), st(k, 2)),
             G(yol('M34 -15 C38 -6 38 6 34 15'), st(k, 1.3, o=70)), G(yol('M84 -17 C88 -6 88 6 84 17'), st(k, 1.3, o=70)),
             G(yol('M-8 -10 C0 -14 16 -14 28 -12'), st('#ffffff', 2.5, o=60)), p=(cx, cy), s=(100 * s, 100 * s), r=r)


DERI = [(0, '#f3c8a3'), (1, '#e2a37c')]  # 2B palet


def kisi(x, y, renk='#8fc1c9', olcek=1.0, beyaz=False, sac='#3b2a1e'):
    """İnsan figürü (önden, bele kadar): omuzlu gövde, boyun, kulaklı baş, yüz, saç, kollar ve eller.
    beyaz=True: beyaz önlüklü hekim (yaka, cep, steteskop); değilse renkli forma (V yaka)."""
    s = olcek
    P = lambda dx, dy: f'{x + dx * s:.1f} {y + dy * s:.1f}'  # noqa: E731
    koyu = '#7d8aa0' if beyaz else '#4c8590'
    giysi = [(0, '#ffffff'), (1, '#dbe3ec')] if beyaz else [(0, renk), (1, renk)]
    parca = [
        # kollar (gövdenin arkasında)
        G(yol(f'M{P(-44, 60)} C{P(-58, 80)} {P(-60, 120)} {P(-56, 146)} L{P(-40, 148)} C{P(-40, 120)} {P(-38, 96)} {P(-30, 76)} Z'), gf(giysi, (x - 50 * s, y + 60 * s), (x - 40 * s, y + 150 * s)), st(koyu, 1.2)),
        G(yol(f'M{P(44, 60)} C{P(58, 80)} {P(60, 120)} {P(56, 146)} L{P(40, 148)} C{P(40, 120)} {P(38, 96)} {P(30, 76)} Z'), gf(giysi, (x + 50 * s, y + 60 * s), (x + 40 * s, y + 150 * s)), st(koyu, 1.2)),
        G(el(x - 48 * s, y + 152 * s, 16 * s, 16 * s), fl('#e9b896')), G(el(x + 48 * s, y + 152 * s, 16 * s, 16 * s), fl('#e9b896')),
        # boyun
        G(rc(x, y + 30 * s, 18 * s, 26 * s, 6 * s), fl('#e2a983')),
        # gövde (omuzlar)
        G(yol(f'M{P(-46, 156)} C{P(-50, 80)} {P(-42, 50)} {P(-14, 40)} L{P(14, 40)} C{P(42, 50)} {P(50, 80)} {P(46, 156)} Z'), gf(giysi, (x, y + 40 * s), (x, y + 156 * s)), st(koyu, 1.5)),
    ]
    if beyaz:
        parca += [G(yol(f'M{P(-14, 40)} L{P(0, 74)} L{P(14, 40)}'), fl('#8fc1c9')),
                  G(yol(f'M{P(-14, 40)} L{P(-4, 92)} M{P(14, 40)} L{P(4, 92)}'), st('#b9c4d0', 1.5)),
                  G(rc(x + 26 * s, y + 104 * s, 16 * s, 14 * s, 2), st('#b9c4d0', 1.2)),
                  G(yol(f'M{P(-12, 44)} C{P(-26, 70)} {P(-18, 100)} {P(-8, 106)} M{P(12, 44)} C{P(22, 70)} {P(14, 96)} {P(4, 104)}'), st('#3e4a58', 2.2)),
                  G(el(x - 6 * s, y + 108 * s, 10 * s, 10 * s), fl('#9aa6b4'), st('#3e4a58', 1.5))]
    else:
        parca += [G(yol(f'M{P(-14, 40)} L{P(0, 62)} L{P(14, 40)} Z'), fl('#e2a983')), G(rc(x - 22 * s, y + 100 * s, 16 * s, 12 * s, 2), st(koyu, 1.2))]
    parca += [
        G(el(x - 23 * s, y + 2 * s, 8 * s, 12 * s), fl('#e2a983')), G(el(x + 23 * s, y + 2 * s, 8 * s, 12 * s), fl('#e2a983')),
        G(el(x, y, 44 * s, 50 * s), gf(DERI, (x - 6 * s, y - 8 * s), (x + 10 * s, y + 18 * s), radyal=True), st('#b9805a', 1)),
        G(el(x - 8 * s, y + 2 * s, 4 * s, 4 * s), fl('#3b2a1e')), G(el(x + 8 * s, y + 2 * s, 4 * s, 4 * s), fl('#3b2a1e')),
        G(yol(f'M{P(-7, 13)} C{P(-3, 16)} {P(3, 16)} {P(7, 13)}'), st('#a8705f', 1.4)),
        G(yol(f'M{P(-23, -2)} C{P(-26, -30)} {P(26, -30)} {P(23, -2)} C{P(18, -14)} {P(6, -18)} {P(-4, -16)} C{P(-12, -14)} {P(-18, -10)} {P(-23, -2)} Z'), fl(sac)),
    ]
    return parca


def yatan_hasta(x, y, s=1.0, battaniye='#8fc1c9', sac='#3b2a1e', torba=False):
    """Yandan yatan hasta (baş solda): başlıklı ve ayaklı yatak, şilte, yastık, baş + saç, kıvrımlı battaniye, battaniye
    üstünde kol; torba=True: yatak kenarında idrar torbası. (x, y) şiltenin sol üst köşesi; genişlik 420·s."""
    P = lambda dx, dy: f'{x + dx * s:.1f} {y + dy * s:.1f}'  # noqa: E731
    W = 420
    p = [
        G(yol(f'M{P(-14, -60)} L{P(-14, 120)}'), st('#7d8aa0', 7 * s)), G(yol(f'M{P(W + 14, -10)} L{P(W + 14, 120)}'), st('#7d8aa0', 7 * s)),
        G(yol(f'M{P(-14, -60)} C{P(-14, -76)} {P(10, -76)} {P(10, -60)} L{P(10, 30)}'), st('#9aa6b4', 6 * s)),
        G(rc(x + W / 2 * s, y + 52 * s, (W + 20) * s, 12 * s, 3), fl('#9aa6b4')),
        G(rc(x + W / 2 * s, y + 22 * s, W * s, 44 * s, 10 * s), gf([(0, '#f7f9fb'), (1, '#d6dee7')], (x, y), (x, y + 44 * s)), st('#b9c4d0', 1.5)),
        G(yol(f'M{P(8, 2)} C{P(8, -16)} {P(80, -18)} {P(84, 0)} Z'), fl('#ffffff'), st('#c9d3de', 1.5)),
        G(el(x + 52 * s, y - 16 * s, 46 * s, 42 * s), gf([(0, '#f6d6bd'), (.7, '#e9b896'), (1, '#d49a76')], (x + 44 * s, y - 24 * s), (x + 60 * s, y - 4 * s), radyal=True), st('#b9805a', 1)),
        G(yol(f'M{P(30, -16)} C{P(30, -40)} {P(70, -44)} {P(76, -22)} C{P(64, -30)} {P(44, -30)} {P(30, -16)} Z'), fl(sac)),
        G(el(x + 66 * s, y - 18 * s, 4 * s, 3 * s), fl('#3b2a1e')),
        G(yol(f'M{P(78, -8)} C{P(140, -34)} {P(260, -36)} {P(330, -22)} C{P(370, -16)} {P(400, -10)} {P(410, 6)} L{P(410, 20)} L{P(78, 20)} Z'),
          gf([(0, battaniye), (1, battaniye)], (x, y - 30 * s), (x, y + 20 * s)), st('#4c8590', 1.5)),
        *[G(yol(f'M{P(120 + i * 70, -18)} C{P(130 + i * 70, -6)} {P(126 + i * 70, 6)} {P(134 + i * 70, 16)}'), st('#4c8590', 1.2, o=60)) for i in range(4)],
        G(yol(f'M{P(100, -14)} C{P(140, -20)} {P(190, -18)} {P(214, -12)}'), st('#e2a983', 9 * s)),
        G(el(x + 218 * s, y - 12 * s, 14 * s, 12 * s), fl('#e2a983')),
    ]
    if torba:
        p += [G(yol(f'M{P(300, 20)} C{P(320, 60)} {P(340, 70)} {P(350, 76)}'), st('#cfd8e2', 5 * s)),
              G(rc(x + 362 * s, y + 100 * s, 50 * s, 64 * s, 8 * s), fl('#f4f7fa', o=94), st('#9aa6b4', 1.5)),
              G(rc(x + 362 * s, y + 116 * s, 42 * s, 28 * s, 6 * s), fl('#f2cf55'))]
    return p
