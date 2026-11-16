"""KMB adım videoları — 2B düz çizgi film hattı, GRUP C1 (adim2b.py bunları içe alır).
Adımlar: giris, endikasyon-takip, endikasyon-retansiyon, endikasyon-diger, tuzak-sistit, kontrendikasyon-enfeksiyon.
Cümleler 02.json `adimlar[].cumleler` (ses o-<adım>); anatomi/el/araç 2B sahnelerden (Sahne2B) ve 2B konu videolarından
(uret2b*.py, `ic_ekle2b`) gelir; kavram sahneleri (kartlar, kavanozlar, monitör, organlar) burada düz renk + 2–3 px
konturla çizilir (docs/KMB_2B_STIL.md). Eski hat (adim_lottie.py) dokunulmadan durur.
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ortak2b import *  # noqa: E402,F401,F403
import uret2b_a as U  # noqa: E402
import uret2b as U0  # noqa: E402  (erkek_ilerleyis, KATETER_YOL, URETRA_E)

SON = 99          # T(SON, 1) = videonun sonu (son cümlede kalan ögeler için)
KOYU = '#3e4a58'  # tek yazı/kontur rengi (stil belgesi)
GRI = ('#f4f7fa', '#6b7a90')
MOR = '#8e44ad'
KAN = '#b3201f'


# ———————————————————————— yardımcılar (2B kavram ögeleri)

def _katmanlar(s: Sahne2B):
    return [(k['id'], k['nm'], copy.deepcopy(k['it'])) for k in s.katmanlar]


def arka_parca(s: Sahne2B, nm: str, idx):
    """Kimliksiz arka katmanın (ör. pozisyon `arka-0`: beyaz zemin, üst yatak, üst yastık, alt yatak, alt yastık) seçili parçaları."""
    for k in s.katmanlar:
        if k['nm'] == nm:
            return [copy.deepcopy(k['it'][i]) for i in idx]
    raise KeyError(nm)


def kart(x, y, renk, *ic, w=150, h=130):
    return [G(rc(x, y, w, h, 22), fl('#ffffff'), st(renk, 3)), *ic]


def kartlar(A, b, ogeler, nm='kart', zemin_koy=True, satir=(300, 345)):
    """Kavram kartları sırayla belirir; etiketler iki satıra dağılır (itme eşiği 208 px'in altındaki komşular çakışmasın).
    ogeler: [(x, y, şekiller, etiket, tür)]"""
    T = A.T
    if zemin_koy:
        zemin(A, nm=f'zemin-{nm}')
        A.katmanlar[-1]['ks']['o'] = gorun(A, b, b) if b < len(A.bolumler) - 1 else A.gor(T(b))
    n = len(ogeler)
    for i, (x, y, sh, et_, tur) in enumerate(ogeler):
        f = 0.04 + 0.7 * i / max(1, n)
        son = b if b < len(A.bolumler) - 1 else SON
        A.ekle(f'{nm}{i}', *sh, o=belir(A, b, f, son), a=(x, y), p=S([x, y, 0]),
               s=K((0, [70, 70, 100]), (T(b, f), [70, 70, 100]), (T(b, f) + 10, [100, 100, 100])))
        if et_:
            A.etiketler.append({'bas': round(T(b, f) / FR, 2), 'son': round(T(son, 1) / FR, 2), 'x': x, 'y': satir[i % 2] if n >= 3 else satir[0], 'metin': et_, 'tur': tur})


def figur(x, y, s=1.0, forma='#8fc1c9', sac='#3b2a1e', baston=False):
    """Küçük düz insan figürü (önden): baş, saç, gövde, kollar, bacaklar. (x, y) gövde merkezi."""
    p = [
        G(rc(-12, 52, 14, 40, 6), fl('#3e4a58'), st(KOYU, 1.5)), G(rc(12, 52, 14, 40, 6), fl('#3e4a58'), st(KOYU, 1.5)),
        G(rc(0, 12, 56, 70, 16), gf([(0, forma), (1, forma)], (0, -20), (0, 40)), st(KOYU, 2)),
        G(rc(-34, 10, 14, 54, 7), fl(forma), st(KOYU, 1.8)), G(rc(34, 10, 14, 54, 7), fl(forma), st(KOYU, 1.8)),
        G(el(-34, 40, 14, 14), gf(DERI, (-40, 34), (-28, 46))), G(el(34, 40, 14, 14), gf(DERI, (28, 34), (40, 46))),
        G(el(0, -38, 40, 44), gf(DERI, (-10, -56), (10, -20)), st('#b9805a', 2)),
        G(yol('M-20 -44 C-16 -64 16 -64 20 -44 C14 -50 -14 -50 -20 -44 Z'), fl(sac)),
    ]
    if baston:
        p.append(G(yol('M48 44 L54 92'), st('#7a5a3a', 4)))
    return G(*p, p=(x, y), s=(100 * s, 100 * s))


def kavanoz(A, b, x, v, renk, nm, tavan=5000, yuk=200, son=None):
    """Ölçekli kavanoz (y 130–350) ve içinde yükselen yarı saydam sıvı (v/tavan oranında)."""
    T = A.T
    o = gorun(A, b, son if son is not None else b)
    h = max(8, v / tavan * yuk)
    A.ekle(f'kavanoz-{nm}', G(rc(x, 240, 120, 220, 12), fl(GRI[0]), st(GRI[1], 2.5)),
           *[G(yol(f'M{x + 44} {y} L{x + 56} {y}'), st(GRI[1], 2)) for y in range(150, 350, 40)], o=o)
    A.ekle(f'sivi-{nm}', G(rc(x, 346 - h / 2, 104, h, 4), fl(renk, o=78)), G(yol(f'M{x - 52} {346 - h} L{x + 52} {346 - h}'), st(renk, 2)),
           a=(x, 346), p=S([x, 346, 0]), s=K((0, [100, 0, 100]), (T(b, .08), [100, 0, 100]), (T(b, .5), [100, 100, 100])), o=o)


def bobrek(x):
    d = f'M{x} 150 C{x - 60} 150 {x - 60} 310 {x} 310 C{x + 40} 310 {x + 50} 270 {x + 20} 230 C{x + 50} 190 {x + 40} 150 {x} 150 Z'
    return d


def akciger(x, sag):
    return (f'M{x} 140 C{x + 50} 150 {x + 60} 280 {x + 40} 330 C{x + 10} 340 {x - 20} 330 {x - 24} 310 L{x - 24} 150 Z' if sag else
            f'M{x} 140 C{x - 50} 150 {x - 60} 280 {x - 40} 330 C{x - 10} 340 {x + 20} 330 {x + 24} 310 L{x + 24} 150 Z')


def yatak_hasta(s: Sahne2B):
    """pozisyon sahnesinin üst yatağı + yastığı + sırtüstü erkek hasta (belge sırasıyla)."""
    return [*arka_parca(s, 'arka-0', [1, 2]), *s.katman('p-erkek')]


def idrar_torbasi(x, y, w=90, h=110):
    """Küçük düz idrar torbası (x, y merkez) — sıvı ayrı katman (torba_sivi)."""
    return [G(rc(x, y, w, h, 10), fl(GRI[0]), st(GRI[1], 2.5)), G(rc(x, y - h / 2 + 8, 18, 12, 3), fl('#b9c2cc'), st(GRI[1], 1.5)),
            *[G(yol(f'M{x + w / 2 - 14} {yy} L{x + w / 2 - 4} {yy}'), st(GRI[1], 1.6)) for yy in range(int(y - h / 2 + 24), int(y + h / 2 - 10), 16)]]


def torba_sivi(x, y, w, h, k1, k2, oran=.55):
    """Torbada yükselen yarı saydam idrar filmi (alt kenardan)."""
    hh = h * oran
    return dict(shapes=[G(rc(x, y + h / 2 - 4 - hh / 2, w - 10, hh, 6), fl(IDRAR, o=80))], a=(x, y + h / 2 - 4), p=S([x, y + h / 2 - 4, 0]),
                s=K((0, [100, 0, 100]), (k1, [100, 0, 100]), (k2, [100, 100, 100])))


def konusma_balonu(x, y, renk=KIRMIZI, w=300, h=80):
    """Konuşma balonu (x, y merkez); kuyruk sol-altta."""
    return G(yol(f'M{x - w / 2 + 14} {y - h / 2} L{x + w / 2 - 14} {y - h / 2} C{x + w / 2} {y - h / 2} {x + w / 2} {y + h / 2} {x + w / 2 - 14} {y + h / 2} '
                 f'L{x - w / 2 + 70} {y + h / 2} L{x - w / 2 + 30} {y + h / 2 + 34} L{x - w / 2 + 44} {y + h / 2} L{x - w / 2 + 14} {y + h / 2} '
                 f'C{x - w / 2} {y + h / 2} {x - w / 2} {y - h / 2} {x - w / 2 + 14} {y - h / 2} Z'), fl('#ffffff'), st(renk, 3))


def simsek(x, y, s=1.0, renk=SARI):
    return G(yol(f'M{x + 8 * s} {y - 36 * s} L{x - 14 * s} {y + 4 * s} L{x + 2 * s} {y + 4 * s} L{x - 10 * s} {y + 40 * s} L{x + 22 * s} {y - 10 * s} L{x + 4 * s} {y - 10 * s} L{x + 18 * s} {y - 36 * s} Z'),
             fl(renk), st('#a8741a', 2))


def bakteri(x, y, r=0):
    return G(el(0, 0, 18, 11), fl('#5aa874'), st('#2e6e46', 1.6), G(yol('M-9 0 L-15 -3 M9 0 L15 3'), st('#2e6e46', 1.6)), p=(x, y), r=r)


def soru_isareti(x, y, renk=SARI):
    return [G(el(x, y, 100, 100), fl('#ffffff'), st(renk, 5)),
            G(yol(f'M{x - 16} {y - 14} C{x - 16} {y - 34} {x + 16} {y - 34} {x + 16} {y - 14} C{x + 16} {y} {x} {y} {x} {y + 16}'), st(renk, 8)),
            G(el(x, y + 32, 9, 9), fl(renk))]


# ———————————————————————— 1. giris (4 cümle)

def a_giris(A):
    T = A.T
    # s0: erkek sahnesi — kateter meatustan mesaneye ilerler, idrar dışarı akar
    s = Sahne2B('erkek')
    s.ekle(A, o=gorun(A, 0, 0))
    ilerleyen_kateter(A, U0.KATETER_YOL, [(T(0, .1), (482, 140)), (T(0, .28), (486, 262)), (T(0, .42), (448, 368)), (T(0, .52), (408, 326)), (T(0, .6), (356, 300))],
                      o=A.gor(T(0, .1) - 2, T(0, 1)))
    akis(A, 'M360 302 L378 312 L408 326 C420 334 432 344 442 356 L448 368 C456 384 488 382 488 352 L486 262 L482 140 L482 -40', T(0, .64),
         nm='akis0', o=A.gor(T(0, .64), T(0, 1)))
    halka(A, 350, 296, 86, 78, 0, f1=.6, f2=.95, nm='halka-mesane0')
    A.etiket(0, 0, 330, 196, 'Mesane')
    et(A, 0, 600, 100, 'Meatus: üretra ağzı', 'bilgi', .02, .58)
    et(A, 0, 600, 100, 'İdrarı dışarı alır', 'dogru', .64, 1)
    et(A, 0, 600, 160, 'Sonda = üretral kateter', 'bilgi', .2, 1)
    A.kamera(0, 440, 240, 112)
    # s1: kolay teknik — hekim + sağlık çalışanı (pozisyon figürleri), tik
    zemin(A, nm='zemin-ekip')
    A.katmanlar[-1]['ks']['o'] = gorun(A, 1, 3)
    p = Sahne2B('pozisyon')
    A.ekle('hekim', *p.katman('p-hekim'), p=S([200, -10, 0]), o=belir(A, 1, .04, 1))
    A.ekle('calisan', *p.katman('p-yardimci'), p=S([-211, -206, 0]), o=belir(A, 1, .28, 1))
    tik(A, 620, 190, 1, .5)
    et(A, 1, 400, 60, 'Kolay: birkaç küçük incelik', 'bilgi', .04)
    et(A, 1, 290, 330, 'Hekim', 'bilgi', .1)
    et(A, 1, 500, 330, 'Sağlık çalışanı', 'bilgi', .32)
    et(A, 1, 620, 262, 'Eğitim almış herkes yapabilir', 'dogru', .52)
    A.kamera(1, 400, 250, 100)
    # s2: hekimi ayıran üç soru — tik / çarpı / soru kartları
    A.ekle('karar-cerceve', *[G(rc(x, 200, 150, 130, 22), fl(r, o=14), st(r, 3)) for x, r in ((180, YESIL), (400, KIRMIZI), (620, MAVI))], o=belir(A, 2, .02, 2))
    kartlar(A, 2, [(180, 200, [G(yol('M150 200 L172 222 L212 178'), st(YESIL, 12))], 'Kime takılır?', 'dogru'),
                   (400, 200, [G(yol('M372 172 L428 228 M428 172 L372 228'), st(KIRMIZI, 12))], 'Kime asla?', 'uyari'),
                   (620, 200, soru_isareti(620, 200, MAVI), 'Hangi endikasyonla?', 'bilgi')], 'karar', zemin_koy=False, satir=(300, 300))
    et(A, 2, 400, 60, 'Hekimi ayıran bilgi', 'bilgi', .02)
    # s3: yol haritası — 4 durak, kesikli ok soldan sağa uzar
    A.ekle('yol-ok', G(yol('M130 200 L670 200'), st(MAVI, 4, kesik=(10, 8)), tm(K((0, 0), (T(3, .05), 0), (T(3, .8), 100)))), o=A.gor(T(3)))
    yatak = [G(rc(670, 212, 70, 24, 8), fl('#9fd0d6'), st('#4f9aa0', 2)), G(el(650, 206, 20, 20), gf(DERI, (642, 198), (658, 214)), st('#b9805a', 1.5))]
    tepsi = [G(rc(490, 214, 76, 30, 6), fl('#c7d1da'), st(GRI[1], 2)), G(yol('M460 210 C476 190 500 226 520 204'), st(KATETER[1], 7)), G(yol('M460 210 C476 190 500 226 520 204'), st(KATETER[0], 4.5))]
    kartlar(A, 3, [(130, 200, kart(130, 200, YESIL, G(yol('M104 200 L124 220 L158 182'), st(YESIL, 10)), w=120, h=110), '1 · Endikasyon', 'bilgi'),
                   (310, 200, kart(310, 200, KIRMIZI, G(yol('M288 178 L332 222 M332 178 L288 222'), st(KIRMIZI, 10)), w=120, h=110), '2 · Kontrendikasyon', 'bilgi'),
                   (490, 200, kart(490, 200, MAVI, *tepsi, w=120, h=110), '3 · Malzeme', 'bilgi'),
                   (670, 200, kart(670, 200, MAVI, *yatak, w=120, h=110), '4 · Uygulama', 'bilgi')], 'yol', zemin_koy=False)
    A.kamera(2, 400, 250, 100)
    A.kamera(3, 400, 250, 100)


# ———————————————————————— 2. endikasyon-takip (5 cümle)

def a_takip(A):
    T = A.T
    zemin(A)
    # s0: vital monitörü + idrar torbası (foley sahnesi) — en önemli gösterge saatlik idrar
    o0 = gorun(A, 0, 0)
    A.ekle('monitor', G(rc(230, 318, 90, 26, 4), fl('#5b6676')), G(rc(230, 195, 340, 220, 16), fl('#1b2330'), st('#5b6676', 3)),
           G(yol('M80 160 L140 160 L152 120 L166 200 L180 140 L190 160 L250 160 L262 120 L276 200 L290 140 L300 160 L380 160'),
             st('#3ad17a', 3, kesik=(18, 8), kesik_kayma=KD((0, 0), (A.op, -A.op * 3)))),
           G(yol('M80 240 C110 220 140 260 170 240 C200 220 230 260 260 240 C290 220 320 260 350 240 L380 240'),
             st('#5ab6ff', 3, kesik=(14, 6), kesik_kayma=KD((0, 0), (A.op, -A.op * 2)))), o=o0)
    f = Sahne2B('foley')
    A.ekle('torba0', *f.katman('f-torba'), *f.katman('f-musluk'), p=S([0, -110, 0]), o=o0)
    A.ekle('torba0-idrar', G(yol('M-84 -36 L84 -36 L84 -10 C84 -2 78 0 70 0 L-70 0 C-78 0 -84 -2 -84 -10 Z'), fl(IDRAR, o=80)),
           p=S([670, 343, 0]), s=K((0, [100, 0, 100]), (T(0, .3), [100, 0, 100]), (T(0, .95), [100, 100, 100])), o=o0)
    halka(A, 670, 300, 112, 110, 0, renk=YESIL, f1=.55, f2=.98, nm='halka-torba0')
    for i, (x, y, m) in enumerate([(120, 60, 'TA 120/80'), (250, 60, 'Nabız 84'), (360, 60, 'SS 16'), (150, 345, 'SpO₂ %98'), (310, 345, 'Ateş 36,8 °C')]):
        et(A, 0, x, y, m, 'bilgi', .04 + i * .07)
    et(A, 0, 640, 110, 'En önemli: saatlik idrar', 'dogru', .5)
    A.kamera(0, 400, 250, 100)
    # s1: ağızdan alamayan yoğun bakım hastası — serum (giren) + idrar torbası (çıkan)
    o1 = gorun(A, 1, 1)
    p = Sahne2B('pozisyon')
    A.ekle('hasta1', *yatak_hasta(p), p=S([0, 60, 0]), o=o1)
    A.ekle('serum', G(yol('M110 50 L110 330'), st('#9aa6b4', 5)), G(yol('M60 330 L160 330'), st('#9aa6b4', 5)),
           G(rc(110, 105, 62, 92, 10), fl('#eef3f8'), st(GRI[1], 2.2)), G(rc(110, 118, 52, 60, 6), fl('#9fc4ef', o=80)),
           G(yol('M110 152 L110 190 C110 236 190 246 262 224'), st('#cfd8e2', 4.5)), G(el(110, 172, 10, 14), fl('#5b8fc9')), o=o1)
    A.ekle('serum-damla', damla(110, 165, .45, '#5b8fc9'), p=KD(*[(T(1) + k * 12, [0, (k % 2) * 10, 0]) for k in range(max(2, int((T(1, 1) - T(1)) / 12)))]), o=o1)
    A.ekle('torba1', G(yol('M520 256 C540 270 560 280 560 292'), st('#cfd8e2', 4.5)), *idrar_torbasi(560, 340, 84, 96), o=o1)
    ts = torba_sivi(560, 340, 84, 96, T(1, .2), T(1, .9))
    A.ekle('torba1-idrar', *ts['shapes'], a=ts['a'], p=ts['p'], s=ts['s'], o=o1)
    A.ekle('yemek-yok', G(rc(690, 118, 54, 14, 4), fl('#e9eef5'), st(GRI[1], 2)), G(yol('M650 100 L690 100 L684 128 L656 128 Z'), fl('#dbe8f3'), st(GRI[1], 2)),
           G(yol('M650 80 L690 80 L680 100 L660 100 Z'), fl('#bcd3ea', o=80)), G(yol('M708 86 L730 86 L724 128 L714 128 Z'), fl('#dbe8f3'), st(GRI[1], 2)),
           G(yol('M700 110 L740 110'), st(GRI[1], 2)), G(yol('M652 60 L738 146 M738 60 L652 146'), st(KIRMIZI, 7)), o=belir(A, 1, .1, 1))
    et(A, 1, 170, 60, 'Giren sıvı: serum', 'bilgi', .04)
    et(A, 1, 695, 180, 'Yiyemiyor, içemiyor', 'uyari', .14)
    et(A, 1, 650, 300, 'Çıkan idrar → sıvı kararı', 'dogru', .45)
    A.kamera(1, 400, 250, 100)
    # s2: çıkan 2000 / giren 1000 → dehidratasyon, böbrek bozulur
    kavanoz(A, 2, 150, 2000, SARI, 'cik2')
    kavanoz(A, 2, 390, 1000, '#5b8fc9', 'gir2')
    for x in (580, 700):
        A.ekle(f'bobrek{x}', G(yol(bobrek(x)), gf(MESANE, (x - 30, 160), (x + 20, 300)), st('#7a2e26', 2.5)), o=gorun(A, 2, 2))
        A.ekle(f'bobrek-k{x}', G(yol(bobrek(x)), fl('#4a1715', o=65)), o=K((0, 0), (T(2, .55), 0), (T(2, .85), 100), (T(2, 1) + 8, 100), (T(2, 1) + 16, 0)))
    A.ekle('kuru', damla(640, 110, 1.5, '#5b8fc9'), G(yol('M622 92 L658 128 M658 92 L622 128'), st(KIRMIZI, 6)), o=belir(A, 2, .55, 2))
    et(A, 2, 150, 60, 'Çıkan idrar 2000 mL', 'bilgi', .1)
    et(A, 2, 390, 60, 'Giren sıvı 1000 mL', 'bilgi', .3)
    et(A, 2, 600, 345, 'Dehidrate: böbrek bozulur', 'uyari', .58)
    A.kamera(2, 400, 250, 100)
    # s3: çıkan 1000 / giren 5000 → akciğer ödemi, periferik ödem, KKY
    kavanoz(A, 3, 150, 1000, SARI, 'cik3')
    kavanoz(A, 3, 390, 5000, '#5b8fc9', 'gir3')
    for x, sag in ((580, False), (700, True)):
        A.ekle(f'akc{x}', G(yol(akciger(x, sag)), fl('#f2b8b2'), st('#a8554e', 2.5)), o=gorun(A, 3, 3))
        A.ekle(f'odem{x}', G(yol(akciger(x, sag)), fl('#5b8fc9', o=70)), a=(x, 334), p=S([x, 334, 0]),
               s=K((0, [100, 0, 100]), (T(3, .45), [100, 0, 100]), (T(3, .85), [100, 62, 100])), o=gorun(A, 3, 3))
    A.ekle('kalp', G(yol('M640 232 C620 212 606 232 624 252 L640 268 L656 252 C674 232 660 212 640 232 Z'), fl('#c0392b'), st('#8d1f1f', 2)),
           s=KD(*[(T(3, .6) + k * 8, [100 + (k % 2) * 14, 100 + (k % 2) * 14, 100]) for k in range(max(2, int((T(3, 1) - T(3, .6)) / 8)))]),
           a=(640, 240), p=S([640, 240, 0]), o=belir(A, 3, .6, 3))
    A.ekle('bacak', G(yol('M726 300 L722 372 L748 372 L750 300 Z'), gf(DERI, (730, 300), (740, 370)), st('#b9805a', 1.8)),
           G(yol('M766 300 L756 372 L800 372 L794 300 Z'), gf(DERI, (770, 300), (790, 370)), st(KIRMIZI, 2.5)), o=belir(A, 3, .75, 3))
    et(A, 3, 150, 60, 'Çıkan idrar 1000 mL', 'bilgi', .1)
    et(A, 3, 390, 60, 'Giren sıvı 5000 mL', 'bilgi', .3)
    et(A, 3, 600, 345, 'Akciğer ödemi · ödem · KKY', 'uyari', .5)
    A.kamera(3, 400, 250, 100)
    # s4: kateterlenen hasta grupları — 4 kart
    kartlar(A, 4, [(110, 200, kart(110, 200, MAVI, G(rc(110, 214, 110, 30, 8), fl('#9fd0d6'), st('#4f9aa0', 2)), G(el(80, 192, 28, 28), gf(DERI, (70, 182), (90, 206)), st('#b9805a', 1.5)),
                                                 G(rc(152, 240, 18, 24, 4), fl(IDRAR, o=80), st(GRI[1], 1.5))), 'Yoğun bakım', 'bilgi'),
                   (300, 200, kart(300, 200, MAVI, G(yol('M262 232 L320 176 L332 186 L276 242 Z'), fl('#c9d3de'), st(GRI[1], 2)), damla(318, 222, 1.1, '#c0392b')), 'Uzun / kanamalı ameliyat', 'bilgi'),
                   (490, 200, kart(490, 200, KIRMIZI, G(yol('M450 170 L490 220 L530 250'), st(KIRMIZI, 7)), G(yol('M516 242 L532 252 L522 234'), st(KIRMIZI, 6))), 'Şok', 'uyari'),
                   (660, 200, kart(660, 200, MAVI, G(el(660, 200, 64, 64), gf(DERI, (650, 190), (670, 215), radyal=True), st('#b9805a', 2)),
                                   G(yol('M640 196 C646 202 654 202 660 196 M660 196 C666 202 674 202 680 196'), st('#3b2a1e', 3))), 'Bilinci kapalı (inme, DKA)', 'bilgi')], 'grup')
    A.kamera(4, 400, 250, 100)


# ———————————————————————— 3. endikasyon-retansiyon (4 cümle)

KAT_TORBA = 'M666 470 C666 484 656 492 638 492 L500 492 C456 492 436 478 438 446 C442 404 440 362 436 326 L428 306'
AKIS_TORBA = 'M428 306 L436 326 C440 362 442 404 438 446 C436 478 456 492 500 492 L638 492 C656 492 666 484 666 470'


def a_retansiyon(A):
    T = A.T
    # s0–s1: glob-sistit konu videosu — mesane dolar (s0), glob: kubbe pubis üstünde, kabarıklık (s1)
    ic_ekle2b(A, U.glob_sistit, [0, 1, None, None, None], [(0, 1)], 'glob')
    et(A, 0, 600, 120, 'Acilde en sık neden', 'uyari', .1)
    et(A, 1, 660, 230, 'Glob vezikale', 'uyari', .35)
    # s2: dolu mesane + kateter torbaya, idrar akar, mesane küçülür, torba dolar
    s = Sahne2B('mesane')
    o2 = A.gor(T(1, 1) + 8, T(2, 1) + 10)
    s.ekle(A, haric=['g-mesane-normal'], o=o2)
    A.ekle('sisme2', *s.katman('g-sisme'), o=K((0, 0), (T(1, 1) + 8, 0), (T(1, 1) + 16, 100), (T(2, .5), 100), (T(2, .85), 0)))
    A.ekle('mesane-dolu2', *s.katman('g-mesane-dolu'), a=(428, 318), p=S([428, 318, 0]),
           s=K((0, [100, 100, 100]), (T(2, .45), [100, 100, 100]), (T(2, .95), [42, 40, 100])), o=o2)
    ilerleyen_kateter(A, KAT_TORBA, [(T(2, .05), (438, 446)), (T(2, .4), (428, 306))], o=A.gor(T(2, .05) - 2, T(2, 1) + 10), nm='kateter2')
    akis(A, AKIS_TORBA, T(2, .45), nm='akis2', o=A.gor(T(2, .45), T(2, 1) + 10))
    A.ekle('torba2', *idrar_torbasi(710, 404, 116, 136), o=o2)
    ts = torba_sivi(710, 404, 116, 136, T(2, .5), T(2, 1), .6)
    A.ekle('torba2-idrar', *ts['shapes'], a=ts['a'], p=ts['p'], s=ts['s'], o=o2)
    et(A, 2, 620, 250, 'Üretral kateter takılır', 'bilgi', .05, .5)
    et(A, 2, 620, 250, 'Mesane boşalır', 'dogru', .55, 1)
    et(A, 2, 620, 310, 'Hasta rahatlar', 'dogru', .72, 1)
    A.kamera(2, 500, 330, 115)
    # s3: göreceli endikasyon — yatağa bağımlı hasta (torbalı) + hareket ettirilemeyen travma hastası
    zemin(A, nm='zemin-yatak')
    A.katmanlar[-1]['ks']['o'] = A.gor(T(3))
    p = Sahne2B('pozisyon')
    for i, (x, f1) in enumerate(((200, .04), (600, .45))):
        A.ekle(f'yatak{i}', *yatak_hasta(p), a=(390, 130), p=S([x, 200, 0]), s=S([60, 60, 100]), o=belir(A, 3, f1, SON))
    A.ekle('torba3', G(yol('M250 236 C270 250 290 256 290 268'), st('#cfd8e2', 3.5)), *idrar_torbasi(290, 296, 48, 56), o=belir(A, 3, .12, SON))
    ts = torba_sivi(290, 296, 48, 56, T(3, .15), T(3, .4))
    A.ekle('torba3-idrar', *ts['shapes'], a=ts['a'], p=ts['p'], s=ts['s'], o=belir(A, 3, .12, SON))
    A.ekle('travma-isaret', G(el(690, 140, 56, 56), fl('#ffffff'), st(KIRMIZI, 3)), G(yol('M690 122 L690 158 M672 140 L708 140'), st(KIRMIZI, 9)),
           G(yol('M636 224 L744 224'), st('#8a96a6', 9)), G(yol('M636 224 L744 224'), st('#dfe6ee', 5)), o=belir(A, 3, .5, SON))
    et(A, 3, 200, 330, 'Yatağa bağımlı hasta', 'bilgi', .1)
    et(A, 3, 600, 330, 'Hareket ettirilemeyen travma', 'uyari', .52)
    et(A, 3, 400, 60, 'Göreceli endikasyon', 'bilgi', .6)
    A.kamera(3, 400, 250, 100)


# ———————————————————————— 4. endikasyon-diger (4 cümle)

KAT_KULTUR = 'M560 398 C590 392 600 404 600 430 L600 476 C600 490 592 492 576 492 L500 492 C456 492 436 478 438 446 C442 404 440 362 436 326 L428 306'
AKIS_KULTUR = 'M428 306 L436 326 C440 362 442 404 438 446 C436 478 456 492 500 492 L576 492 C592 492 600 490 600 476 L600 430 C600 404 590 392 560 398'


def a_diger(A):
    T = A.T
    s = Sahne2B('mesane')
    s.ekle(A, o=gorun(A, 0, 2))  # gövde kesiti + normal mesane
    # s0: kültür — kateter mesanede, idrar steril kaba; küçük çocuk + yaşlı
    A.ekle('kultur', *s.katman('g-kultur'), o=belir(A, 0, .04, 0))
    A.ekle('kap-bos', G(rc(556, 452, 46, 40, 3), fl('#f2f5f8')), o=K((0, 0), (T(0, .04), 0), (T(0, .04) + 6, 100), (T(0, .62), 100), (T(0, .85), 0)))
    ilerleyen_kateter(A, KAT_KULTUR, [(T(0, .08), (438, 446)), (T(0, .4), (428, 306))], o=A.gor(T(0, .08) - 2, T(0, 1)), nm='kateter-k')
    akis(A, AKIS_KULTUR, T(0, .45), nm='akis-k', o=A.gor(T(0, .45), T(0, 1)))
    A.ekle('damla-k', damla(556, 412, .6), p=KD(*[(T(0, .6) + k * 10, [0, (k % 2) * 10, 0]) for k in range(max(2, int((T(0, 1) - T(0, .6)) / 10)))]), o=belir(A, 0, .6, 0))
    A.ekle('cocuk', figur(660, 150, .62, '#f2b8d0'), o=belir(A, 0, .12, 0))
    A.ekle('yasli', figur(740, 140, .8, '#c9d3de', sac='#cfd3d8', baston=True), o=belir(A, 0, .22, 0))
    et(A, 0, 660, 245, 'Temiz örnek veremiyor', 'uyari', .25)
    et(A, 0, 660, 345, 'Steril kültür örneği', 'dogru', .5)
    A.kamera(0, 520, 300, 110)
    # s1: mesaneye ilaç (kemoterapötik) — enjektör + kateterden mor sıvı, mesane morarır
    A.ekle('ilac', *s.katman('g-ilac'), o=belir(A, 1, .04, 1))
    for i, c in enumerate(s.cz('g-ilac')):
        A.ekle(f'ilac-akis{i}', G(yol(c['d']), st(MOR, c['w'] + 1, kesik=(10, 10), kesik_kayma=KD((0, 0), (A.op, -A.op * 3))),
                                   tm(K((0, 0), (T(1, .3), 0), (T(1, .75), 100)))), o=belir(A, 1, .3, 1))
    A.ekle('ilac-mesane', G(el(420, 288, 94, 84), fl('#b48ae0', o=55)), o=K((0, 0), (T(1, .55), 0), (T(1, .9), 100), (T(1, 1) + 8, 100), (T(1, 1) + 16, 0)))
    et(A, 1, 650, 250, 'Kemoterapötik ilaç', 'bilgi', .1)
    et(A, 1, 650, 330, 'Kateterden mesaneye', 'bilgi', .4)
    A.kamera(1, 520, 330, 115)
    # s2: travmada sistografi — kateterden opak madde, röntgen penceresinde beyaz mesane
    A.ekle('opak-mesane', G(el(420, 288, 94, 84), fl('#ffffff', o=92), st('#9aa6b4', 2)), o=K((0, 0), (T(2, .2), 0), (T(2, .6), 100), (T(2, 1) + 8, 100), (T(2, 1) + 16, 0)))
    A.ekle('rontgen', G(rc(680, 190, 200, 240, 14), fl('#1b2330'), st('#5b6676', 3)),
           G(yol('M600 150 C630 110 680 110 700 150 M760 150 C740 110 700 110 680 150'), st('#e9eef5', 4, o=55)),
           G(yol('M610 290 C640 270 680 270 700 294 C720 270 750 270 760 290'), st('#e9eef5', 5, o=65)),
           G(yol('M680 236 L680 300'), st('#cfd8e2', 5)), o=belir(A, 2, .05, 2))
    A.ekle('rontgen-mesane', G(el(680, 196, 106, 86), fl('#ffffff', o=95)), a=(680, 196), p=S([680, 196, 0]),
           s=K((0, [20, 20, 100]), (T(2, .25), [20, 20, 100]), (T(2, .65), [100, 100, 100])), o=belir(A, 2, .25, 2))
    et(A, 2, 300, 110, 'Travmada sistografi', 'bilgi', .05)
    et(A, 2, 630, 345, 'Opak madde kateterden', 'bilgi', .3)
    A.kamera(2, 540, 280, 108)
    # s3: sınav sırası — 1 idrar yapamama, 2 idrar takibi, 3 seyrek endikasyonlar
    kartlar(A, 3, [(160, 200, kart(160, 200, YESIL, G(el(160, 196, 80, 80), gf(MESANE, (140, 176), (180, 220), radyal=True), st('#7a2e26', 2.5)), G(el(160, 196, 62, 62), fl(IDRAR, o=85))), '1 · İdrar yapamama', 'dogru'),
                   (400, 200, kart(400, 200, YESIL, *idrar_torbasi(400, 200, 70, 86), G(rc(400, 222, 60, 34, 6), fl(IDRAR, o=80))), '2 · İdrar takibi', 'dogru'),
                   (640, 200, kart(640, 200, MAVI, G(rc(640, 208, 44, 56, 8), fl('#eef3f8'), st('#7d8aa0', 2)), G(rc(640, 220, 36, 24, 4), fl(IDRAR, o=80)), G(rc(640, 176, 54, 12, 3), fl('#c0392b'), st('#8d1f1f', 1.5))), '3 · Kültür, ilaç, sistografi', 'bilgi')], 'sira')
    et(A, 3, 400, 60, 'Sınavda önce 1 ve 2', 'bilgi', .05)
    A.kamera(3, 400, 250, 100)


# ———————————————————————— 5. tuzak-sistit (6 cümle)

def a_sistit(A):
    T = A.T
    zemin(A)
    # s0: hekim + yatan hasta: "idrar yapamıyorum" balonu; tepsideki sondaya ÇARPI
    o0 = gorun(A, 0, 0)
    p = Sahne2B('pozisyon')
    A.ekle('hasta0', *yatak_hasta(p), p=S([0, 80, 0]), o=o0)
    A.ekle('hekim0', *p.katman('p-hekim'), p=S([0, 10, 0]), o=o0)
    A.ekle('balon0', konusma_balonu(380, 86, KIRMIZI, 300, 70), o=belir(A, 0, .05, 0))
    f = Sahne2B('foley')
    A.ekle('tepsi0', G(rc(560, 345, 210, 58, 8), fl('#c7d1da'), st('#8b96a3', 2)), o=belir(A, 0, .4, 0))
    A.ekle('sonda0', *f.katman('f-govde'), *f.katman('f-uc'), *f.katman('f-delik'), *f.katman('f-balon-sonuk'), *f.katman('f-drenaj'),
           a=(335, 245), p=S([560, 342, 0]), s=S([34, 34, 100]), o=belir(A, 0, .4, 0))
    carpi(A, 560, 345, 0, .62, r=30)
    et(A, 0, 380, 86, '"İdrar yapamıyorum"', 'uyari', .08)
    et(A, 0, 640, 292, 'Hemen sonda takma!', 'uyari', .64)
    A.kamera(0, 400, 250, 100)
    # s1–s2: sistit — glob videosunun SON durumu (küçük, ödemli mesane) baştan görünür; ağrı, sık idrar, yanma
    ic_ekle2b(A, U.glob_sistit, ['once'] * 5, [(1, 2)], 'sistit')
    A.kamera(1, 430, 285, 150)
    halka(A, 420, 298, 56, 50, 1, renk=KIRMIZI, f1=.45, f2=.98, nm='halka-kucuk')
    A.ekle('agri', simsek(556, 262, 1.0), o=belir(A, 1, .08, 2))
    A.ekle('az-idrar', damla(446, 404, .7), p=KD(*[(T(1, .35) + k * 16, [0, (k % 2) * 18, 0]) for k in range(max(2, int((T(1, 1) - T(1, .35)) / 16)))]), o=belir(A, 1, .35, 1))
    et(A, 1, 600, 170, 'Ağrı · sık idrar · yanma', 'uyari', .08)
    et(A, 1, 300, 330, 'Sistit: 15–20 mL', 'uyari', .5)
    A.ekle('soru', *soru_isareti(600, 232, SARI), o=belir(A, 2, .08, 2))
    et(A, 2, 310, 180, '"Yapamıyorum" ≠ retansiyon', 'uyari', .05)
    et(A, 2, 600, 310, 'Önce sen değerlendir', 'uyari', .3)
    # s3: yatır, suprapubik şişlik/dolgunluk (glob 0–2) — s4: ultrason (glob 3)
    ic_ekle2b(A, U.glob_sistit, [3, 3, 3, 4, None], [(3, 4)], 'glob')
    et(A, 3, 300, 120, '6 aylık gebe karnı gibi', 'bilgi', .36, .9)
    # s5: gereksiz kateterin zararları — 3 kart
    kartlar(A, 5, [(160, 200, kart(160, 200, KIRMIZI, bakteri(136, 190, -20), bakteri(176, 182, 15), bakteri(150, 218, 40), bakteri(186, 214, -30)), 'Enfeksiyon riski', 'uyari'),
                   (400, 200, kart(400, 200, KIRMIZI, simsek(400, 200, 1.1)), 'Birkaç gün ağrı', 'uyari'),
                   (640, 200, kart(640, 200, KIRMIZI, G(yol('M580 186 L620 186 C632 186 632 194 640 194 C648 194 648 186 660 186 L700 186 L700 214 L660 214 C648 214 648 206 640 206 C632 206 632 214 620 214 L580 214 Z'),
                                                      fl('#f0b8b2'), st('#a8554e', 2)), G(yol('M600 200 L680 200'), st(IDRAR, 3, kesik=(6, 6)))), 'Erkekte üretra darlığı', 'uyari')], 'zarar', satir=(300, 300))
    et(A, 5, 400, 60, 'Gereksiz kateter zarar verir', 'bilgi', .04)
    A.kamera(5, 400, 250, 100)


# ———————————————————————— 6. kontrendikasyon-enfeksiyon (4 cümle)

AKIS_E = 'M356 300 L378 312 L408 326 C420 334 432 344 442 356 L448 368 C456 384 488 382 488 352 L486 262 L482 140 L482 -40'


def a_enf(A):
    T = A.T
    zemin(A)
    # s0: DUR işareti + tepsideki kateterde çarpı — malpraktis
    o0 = gorun(A, 0, 0)
    A.ekle('dur', G(yol('M400 100 L470 130 L500 200 L470 270 L400 300 L330 270 L300 200 L330 130 Z'), fl(KIRMIZI), st('#8d1f1f', 4)),
           G(rc(400, 200, 130, 28, 6), fl('#ffffff')), a=(400, 200), p=S([400, 200, 0]),
           s=K((0, [40, 40, 100]), (T(0, .05), [40, 40, 100]), (T(0, .2), [100, 100, 100])), o=belir(A, 0, .05, 0))
    f = Sahne2B('foley')
    A.ekle('sonda-e', *f.katman('f-govde'), *f.katman('f-uc'), *f.katman('f-delik'), *f.katman('f-balon-sonuk'), *f.katman('f-drenaj'),
           a=(335, 245), p=S([640, 200, 0]), s=S([36, 36, 100]), o=belir(A, 0, .35, 0))
    carpi(A, 640, 200, 0, .55, r=34)
    et(A, 0, 400, 335, 'Kesin kontrendikasyon', 'uyari', .1)
    et(A, 0, 640, 250, 'Takarsan malpraktis', 'uyari', .6)
    A.kamera(0, 400, 250, 100)
    # s1–s3: erkek sahnesi
    s = Sahne2B('erkek')
    o13 = A.gor(T(1), T(3, 1) + 10)
    s.ekle(A, o=o13)
    # s1: akut prostatit — prostat kızarık ve zonklar, bakteriler kana yayılır; rektal tuşe de yasak
    A.ekle('prostat-ilt', G(el(427, 341, 62, 60), fl(KIRMIZI, o=50), st('#8d1f1f', 2.5)), a=(427, 341), p=S([427, 341, 0]),
           s=KD(*[(T(1, .1) + k * 10, [100 + (k % 2) * 10, 100 + (k % 2) * 10, 100]) for k in range(max(2, int((T(1, 1) - T(1, .1)) / 10)))]),
           o=K((0, 0), (T(1, .1), 0), (T(1, .25), 100), (T(1, 1) + 8, 100), (T(1, 1) + 16, 0)))
    A.ekle('bakteri', *[bakteri(427 + dx, 341 + dy, r) for dx, dy, r in [(-40, -16, 20), (34, -26, -15), (48, 8, 40), (-48, 22, -30), (0, -48, 10), (18, 42, 60)]],
           a=(427, 341), p=S([427, 341, 0]), s=K((0, [40, 40, 100]), (T(1, .4), [40, 40, 100]), (T(1, .9), [240, 240, 100])), o=belir(A, 1, .4, 1))
    A.ekle('tuse', G(rc(650, 300, 92, 72, 12), fl('#ffffff'), st(GRI[1], 2.5)),
           G(yol('M612 318 L664 318 C676 318 684 310 684 300 C684 290 676 282 664 282 L612 282 Z'), fl('#dcedf9'), st('#3f6f9c', 2)),
           G(yol('M640 284 C644 290 644 310 640 316'), st('#3f6f9c', 1.4, o=70)), G(yol('M616 290 L628 288'), st('#ffffff', 2.5, o=70)),
           o=K((0, 0), (T(1, .05), 0), (T(1, .12), 100), (T(1, 1) + 8, 100), (T(1, 1) + 16, 0)))
    carpi(A, 650, 300, 1, .2, r=26)
    et(A, 1, 560, 160, 'Akut prostatit: sepsis riski', 'uyari', .3)
    et(A, 1, 560, 230, 'Rektal tuşe de yapılmaz', 'uyari', .08)
    A.etiket(1, 1, 340, 358, 'Prostat')
    A.kamera(1, 450, 290, 135)
    # s2: aktif genital enfeksiyon — testis/epididim kızarık, bakteriler
    A.ekle('testis-ilt', G(el(546, 240, 112, 52), fl(KIRMIZI, o=50), st('#8d1f1f', 2.5)), a=(546, 240), p=S([546, 240, 0]),
           s=KD(*[(T(2, .05) + k * 10, [100 + (k % 2) * 8, 100 + (k % 2) * 8, 100]) for k in range(max(2, int((T(2, 1) - T(2, .05)) / 10)))]),
           o=K((0, 0), (T(2, .05), 0), (T(2, .2), 100), (T(2, 1) + 8, 100), (T(2, 1) + 16, 0)))
    A.ekle('bakteri2', *[bakteri(546 + dx, 240 + dy, r) for dx, dy, r in [(-50, -24, 20), (40, -30, -15), (60, 10, 40), (-60, 20, -30)]],
           a=(546, 240), p=S([546, 240, 0]), s=K((0, [40, 40, 100]), (T(2, .45), [40, 40, 100]), (T(2, .9), [180, 180, 100])), o=belir(A, 2, .45, 2))
    et(A, 2, 560, 140, 'Orşit · epididimit · Fournier', 'uyari', .1)
    et(A, 2, 560, 300, 'Enfeksiyonu yayar: takılmaz', 'uyari', .5)
    A.kamera(2, 520, 250, 150)
    # s3: çok dolu mesane hızla boşalır → mukozada kanama; ama kontrendikasyon değil
    A.ekle('kateter-e', *s.katman('e-kateter'), *s.katman('e-balon-dogru'), o=belir(A, 3, .04, SON))
    akis(A, AKIS_E, T(3, .12), nm='akis-e', hiz=7, w=3.5, o=belir(A, 3, .12, SON))
    for i, (dx, dy) in enumerate([(-52, -20), (20, -50), (56, 10), (-40, 36), (34, 44), (-8, -58)]):
        A.ekle(f'kanama{i}', G(el(350 + dx, 295 + dy, 10, 10), fl(KAN)), o=belir(A, 3, .3 + i * .07, SON))
    tik(A, 600, 190, 3, .6, son=SON)
    et(A, 3, 560, 110, 'Hızlı boşaltma: kanama', 'bilgi', .3)
    et(A, 3, 560, 250, 'Kontrendikasyon değil', 'dogru', .62)
    et(A, 3, 560, 300, 'Endikasyon varsa yine takılır', 'dogru', .75)
    A.kamera(3, 420, 250, 125)


ADIMLAR = {'giris': a_giris, 'endikasyon-takip': a_takip, 'endikasyon-retansiyon': a_retansiyon, 'endikasyon-diger': a_diger,
           'tuzak-sistit': a_sistit, 'kontrendikasyon-enfeksiyon': a_enf}
