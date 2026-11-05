"""KMB Lottie 2B hattı — ortak yardımcılar (düz çizgi film dili, docs/KMB_2B_STIL.md).

Tek kaynak: 2B SVG sahneleri (`Sahne2B`) — anatomi, el, araç, zemin buradan gelir; üreticiler yalnız koreografi yazar:
kateter ilerleyişi, balon, idrar akışı, vurgu halkası, etiket, kamera. Eski (gerçekçi) hat `lottie_uret.py`/`adim_lottie.py`
ve `src/data/kmb/lottie/` DOKUNULMADAN durur; bu hat `src/data/kmb/lottie2b/` üretir.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lottie_dsl import FR, Anim, G, K, KD, S, el, fl, gf, ornekle, rc, st, tm, yol  # noqa: E402,F401
from sahne2b import Sahne2B  # noqa: E402,F401

MEDS = Path(__file__).resolve().parents[3]
CIKTI = MEDS / 'src/data/kmb/lottie2b'
SES = MEDS / 'src/data/kmb/ses_02.json'
VERI = MEDS / 'src/data/kmb'

# 2B palet (sahneOrtak.tsx kmb-2b-* ile aynı tonlar)
KATETER = ('#f0c050', '#b47a1a')        # gövde, kontur
SILIKON = ('#f2f5f8', '#8a96a6')
IDRAR = '#efc53f'
JEL = '#8fc7ff'
MAVI, YESIL, KIRMIZI, SARI = '#2f6fd6', '#2e9e5b', '#d23b3b', '#e1a92e'
DERI = [(0, '#f3c8a3'), (1, '#e2a37c')]
MESANE = [(0, '#c9655a'), (1, '#a8433a')]
IDRAR_G = [(0, '#fbe58a'), (1, '#efc53f')]
KEMIK = [(0, '#f7efdd'), (1, '#e6d7b4')]

_IC = None  # lottie_dsl.ic_ekle(modul=ortak2b) ayarlar: üretici alt kompozisyon olarak çalışır


def anim(z, ad, baslik, bolumler, bekle=2.0):
    return _IC if _IC is not None else Anim(ad, baslik, bolumler, z, bekle=bekle)


def B(baslik, metin, sure):
    return {'baslik': baslik, 'metin': metin, 'sure': sure}


def zemin(A, renk='#ffffff', nm='zemin'):
    A.ekle(nm, G(rc(400, 250, 800, 500), fl(renk)))


def gorun(A, b1, b2, f=8):
    """b1 cümlesinin başında belirir, b2 cümlesinin sonunda kaybolur."""
    return A.gor(A.T(b1), A.T(b2, 1), f)


def belir(A, b, fr=0.0, son=None, f=8):
    """b cümlesinin fr kesirinde belirir; son verilirse o cümlenin sonunda kaybolur."""
    return A.gor(A.T(b, fr), A.T(son, 1) if son is not None else None, f)


def kateter_cizgi(d, w=6.5, renk=KATETER, e=None, s=None, o=None):
    """Düz stil silindir: koyu kontur + açık gövde (+ ince beyaz parlama). e/s: kırpma anahtarları (çizim/ilerleme)."""
    k = tm(e, s) if e is not None else None
    parca = [G(yol(d), st(renk[1], w + 2.5), *([k] if k else [])), G(yol(d), st(renk[0], w), *([k] if k else []))]
    return parca


def ilerleyen_kateter(A, d, duraklar, w=6.5, renk=KATETER, nm='kateter', o=None, uc=True, catal_son=None):
    """Sabit boylu kateter: uç `duraklar` [(kare, (x, y)), …] boyunca `d` yolunda ilerler; dışta kalan kısım kısalır.
    `d` dış uçtan (kadraj dışından) başlayıp hedefte biter. catal_son: tam itildiğinde dış ucun (Y bağlantı) noktası;
    verilmezse yol başı dışarıda kalır (kateter kadraj dışından beslenir)."""
    P = ornekle(d, 400)
    kes = lambda q: min(range(len(P)), key=lambda i: (P[i][0] - q[0]) ** 2 + (P[i][1] - q[1]) ** 2) / 400  # noqa: E731
    fr = [(k, kes(q)) for k, q in duraklar]
    L = (fr[-1][1] - kes(catal_son)) if catal_son else 10.0
    ornek = []
    for (k1, f1), (k2, f2) in zip(fr, fr[1:]):
        for j in range(12):
            ornek.append((k1 + (k2 - k1) * j / 12, f1 + (f2 - f1) * j / 12))
    ornek.append(fr[-1])
    nokta = lambda f: P[max(0, min(400, round(f * 400)))]  # noqa: E731
    e = KD(*[(k, f * 100) for k, f in ornek])
    s = KD(*[(k, max(0, f - L) * 100) for k, f in ornek])
    A.ekle(nm, *kateter_cizgi(d, w, renk, e, s), o=o)
    if uc:
        A.ekle(nm + '-uc', G(el(0, 0, w + 3, w + 3), fl(renk[0]), st(renk[1], 1.6)), G(el(w * .35, w * .3, 2.6, 2.6), fl('#5a3a10')),
               p=KD(*[(k, [*nokta(f), 0]) for k, f in ornek]), o=o)
    return nokta, ornek


def balon(A, cx, cy, r, k1, k2, nm='balon', o=None, dogru=True):
    """Balon k1→k2 arasında 0→tam şişer (2B: beyaz-gri yuvarlak, yeşil kontur; yanlışsa kırmızı)."""
    kon = YESIL if dogru else '#8d1f1f'
    A.ekle(nm, G(el(0, 0, 2 * r, 2 * r), gf([(0, '#ffffff'), (1, '#d7dee6')], (-r * .3, -r * .3), (r * .7, r * .7), radyal=True), st(kon, 3)),
           G(el(-r * .3, -r * .35, r * .55, r * .3), fl('#ffffff')),
           a=(0, 0), p=S([cx, cy, 0]), s=K((0, [8, 8, 100]), (k1, [8, 8, 100]), (k2, [100, 100, 100])), o=o)


def halka(A, cx, cy, rx, ry, b, renk=SARI, w=4, f1=.1, f2=.9, nm=None):
    """Vurgu halkası: b cümlesinde belirir ve söner."""
    T = A.T
    A.ekle(nm or f'halka-{b}', G(el(cx, cy, rx * 2, ry * 2), st(renk, w, kesik=(10, 7))),
           o=K((0, 0), (T(b), 0), (T(b, f1), 100), (T(b, f2), 100), (T(b, 1), 0)))


def akis(A, d, k1, k2=None, renk=IDRAR, w=3, nm='akis', o=None, hiz=3):
    """Akan sıvı: kesikli çizgi kayar (k1'den itibaren; o verilmezse k1'de belirir)."""
    son = k2 if k2 is not None else A.op
    A.ekle(nm, G(yol(d), st(renk, w, kesik=(10, 14), kesik_kayma=KD((k1, 0), (son, -(son - k1) * hiz)))), o=o or A.gor(k1))


def damla(x, y, s=1.0, renk=IDRAR):
    return G(yol(f'M{x} {y - 14 * s} C{x - 4 * s} {y - 6 * s} {x - 9 * s} {y} {x - 9 * s} {y + 5 * s} C{x - 9 * s} {y + 11 * s} {x - 4 * s} {y + 14 * s} {x} {y + 14 * s} C{x + 4 * s} {y + 14 * s} {x + 9 * s} {y + 11 * s} {x + 9 * s} {y + 5 * s} C{x + 9 * s} {y} {x + 4 * s} {y - 6 * s} {x} {y - 14 * s} Z'), fl(renk))


def carpi(A, x, y, b, fr=0.3, r=36, son=None):
    # iki ayrı kol: lottie_dsl.yol tek alt yol üretir; tek yolda ikinci M birleşip "Z" çiziyordu (2026-11-05)
    A.ekle(f'carpi-{b}', G(yol(f'M{x - r} {y - r} L{x + r} {y + r}'), st(KIRMIZI, 9)), G(yol(f'M{x + r} {y - r} L{x - r} {y + r}'), st(KIRMIZI, 9)),
           o=belir(A, b, fr, son if son is not None else b))


def tik(A, x, y, b, fr=0.3, son=None):
    A.ekle(f'tik-{b}', G(yol(f'M{x - 30} {y} L{x - 8} {y + 24} L{x + 36} {y - 26}'), st(YESIL, 10)), o=belir(A, b, fr, son if son is not None else b))


def ok(A, d, b, renk=MAVI, w=5, f1=.1, f2=.9, nm=None):
    """Çizilen ok: b cümlesinde uzar (kırpma) ve söner; uçta üçgen."""
    T = A.T
    P = ornekle(d, 40)
    import math
    ang = math.atan2(P[-1][1] - P[-2][1], P[-1][0] - P[-2][0])
    cs, sn = math.cos(ang), math.sin(ang)
    L = w * 3.2
    x, y = P[-1]
    uc = f'M{x - L * cs - L * .6 * sn} {y - L * sn + L * .6 * cs} L{x} {y} L{x - L * cs + L * .6 * sn} {y - L * sn - L * .6 * cs} Z'
    A.ekle(nm or f'ok-{b}', G(yol(d), st(renk, w), tm(K((0, 0), (T(b, f1), 0), (T(b, f1 + .25), 100)))),
           G(yol(uc), fl(renk)), o=K((0, 0), (T(b), 0), (T(b, f1), 100), (T(b, f2), 100), (T(b, 1), 0)))


def et(A, b, x, y, metin, tur='bilgi', f1=0.0, f2=1.0):
    A.etiketler.append({'bas': round(A.T(b, f1) / FR, 2), 'son': round(A.T(b, f2) / FR, 2), 'x': x, 'y': y, 'metin': metin, 'tur': tur})


def sahne_etiket(A, s: Sahne2B, b1, b2, ids, tur='etiket', kaydir=(0, -24)):
    """Sahnedeki ögelerin bbox merkezine (kaydırılmış) etiket."""
    for i, (id_, metin) in enumerate(ids):
        cx, cy = s.merkez(id_)
        A.etiket(b1, b2, round(cx + kaydir[0]), round(cy + kaydir[1]), metin, tur)


def ic_ekle2b(ust, uretici, harita, gorunur, nm='ic'):
    """2B konu üreticisini (uret2b*.py) adım videosuna alt kompozisyon olarak ekler; lottie_dsl.ic_ekle'nin 2B sarmalayıcısı.
    harita: konu videosunun her bölümü → adım cümlesi (int) | None | 'once'; gorunur: [(ilk cümle, son cümle), …]."""
    import ortak2b
    from lottie_dsl import ic_ekle
    ic_ekle(ust, uretici, harita, gorunur, nm=nm, modul=ortak2b)


def adim(ad, cumleler, zaman, bekle=0.9):
    """Adım videosu: her cümle bir bölüm (eski adim_lottie.adim ile aynı süre kuralı: max(3, uzunluk/14))."""
    return Anim(f'adim-{ad}', ad, [{'baslik': ' '.join(c.split()[:4]).rstrip(',;:'), 'metin': c, 'sure': max(3, len(c) / 14)} for c in cumleler], zaman, bekle=bekle)
