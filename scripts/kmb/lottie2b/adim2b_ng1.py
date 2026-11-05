"""KMB 01 Nazogastrik sonda — adım videoları, GRUP NG1 (adim2b.py bunları toplar; `--kod=01`).
Adımlar: ng-giris, ng-endikasyon, ng-kontrendikasyon-travma / -koroziv / -bilinc / -varis, ng-anatomi.
Sahneler: ng-kesit (baş-boyun sagital kesit), ng-mide (mide kesiti). Yalnız koreografi; stil docs/KMB_2B_STIL.md.
Kontrendikasyon videoları (hoca sınavda soruyor) nedeni görsel gösterir ve sondayı kırmızı çarpıyla "takılmaz" diye kapatır.
Not: svg/bbox.json ng-kesit için eski koordinatlı; kutular burada Lottie katman koordinatlarından elle verildi.
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ortak2b import *  # noqa: E402,F401,F403
from lottie_dsl import renk as _rgb  # noqa: E402

NG = ('#e9eef3', '#6b7a90')          # NG sonda: açık plastik gövde, kontur
NG_K = ('#f6d0d0', '#c62828')        # yanlış/takılmaz sonda (kırmızı ton)
YESIL_A = '#2e9e5b'
KUSMUK = '#b9b65a'

# ng-kesit cz yolları (Lottie koordinatı)
_KZ = Sahne2B('ng-kesit')
SONDA = _KZ.cz('nk-sonda')[0]['d']            # burun → sert damağa paralel → farinks → özofagus (kadraj altına)
SONDA_TR = _KZ.cz('nk-sonda-trakea')[0]['d']  # yanlış yol: larinks → trakea
D_BURUN, D_DAMAK, D_FARINKS, D_OZ = (152, 141), (405, 119), (516, 182), (520, 505)
D_TR = (492, 505)


# ———————————————————————— yardımcılar

def _boya(it, h, o=60, cizgi=None):
    """Öge parçalarını tek renge boyar (renk eylemi): dolgu/degrade → düz renk (o opak), çizgi → cizgi rengi."""
    it = copy.deepcopy(it)
    c = _rgb(h)
    cc = _rgb(cizgi or h)

    def gez(x):
        if isinstance(x, dict):
            if x.get('ty') in ('fl', 'gf'):
                for k in [k for k in x if k not in ('ty', 'r', 'nm')]:
                    del x[k]
                x['ty'], x['c'], x['o'] = 'fl', S(c), S(o)
                return
            if x.get('ty') == 'st':
                x['c'] = S(cc)
            for v in x.values():
                gez(v)
        elif isinstance(x, list):
            for v in x:
                gez(v)
    gez(it)
    return it


def boya(A, s, id_, h, b, fr=.1, son=None, o=60, cizgi=None, nm=None):
    A.ekle(nm or f'boya-{id_}-{b}', *_boya(s.katman(id_), h, o, cizgi), o=belir(A, b, fr, son))


def sonda(A, b, f1, f2, d=SONDA, duraklar=None, renk=NG, nm='sonda', son=None, son_f=1.0, bas_f=None):
    """Sonda burundan ilerler (b cümlesinde f1→f2); son cümlesinin son_f kesirinde söner."""
    T = A.T
    if duraklar is None:
        duraklar = [(0, D_BURUN), (.45, D_DAMAK), (.62, D_FARINKS), (1, D_OZ if d == SONDA else D_TR)]
    k = [(T(b, f1 + (f2 - f1) * q), xy) for q, xy in duraklar]
    o = A.gor(T(b, bas_f if bas_f is not None else max(0, f1 - .04)), T(son, son_f) if son is not None else None)
    ilerleyen_kateter(A, d, k, w=7, renk=renk, nm=nm, o=o, uc=False)
    A.ekle(nm + '-agiz', G(rc(130, 271, 18, 22, 3), fl('#2e9e5b'), st('#1d6b3d', 1.5)), o=o)  # renkli bağlantı ağzı


def sonda_sabit(A, b, fr, son=None, d=SONDA, renk=NG, nm='sonda-s', son_f=1.0):
    o = A.gor(A.T(b, fr), A.T(son, son_f) if son is not None else None)
    A.ekle(nm, *kateter_cizgi(d, 7, renk), G(rc(130, 271, 18, 22, 3), fl('#2e9e5b'), st('#1d6b3d', 1.5)), o=o)


def takilmaz(A, b, x, y, fr=.45, r=40, d=SONDA, et_xy=None, metin='Sonda takılmaz'):
    """Kontrendikasyon kapanışı: sonda kırmızı tonla belirir + büyük kırmızı çarpı + 'takılmaz' etiketi."""
    sonda_sabit(A, b, fr, b, d=d, renk=NG_K, nm=f'sonda-takilmaz-{b}')
    carpi(A, x, y, b, fr + .08, r=r)
    ex, ey = et_xy or (x, y - r - 40)
    et(A, b, ex, ey, metin, 'uyari', fr + .1)


def kivilcim(A, x, y, b, fr, son_f=.95, nm=None):
    """Sürtünme/yeniden yanık işareti: küçük kırmızı yıldız çizgileri yanıp söner."""
    T = A.T
    seg = [(-9, 0, 9, 0), (0, -9, 0, 9), (-6, -6, 6, 6), (6, -6, -6, 6)]
    parca = [G(yol(f'M{x + a} {y + b} L{x + c} {y + e}'), st(KIRMIZI, 3)) for a, b, c, e in seg]
    A.ekle(nm or f'kiv-{b}-{x}-{y}', *parca, a=(x, y), p=S([x, y, 0]),
           s=K((0, [40, 40, 100]), (T(b, fr), [40, 40, 100]), (T(b, fr + .08), [130, 130, 100]), (T(b, fr + .16), [80, 80, 100]),
               (T(b, fr + .24), [130, 130, 100]), (T(b, son_f), [100, 100, 100])),
           o=belir(A, b, fr, b))


def carpi(A, x, y, b, fr=0.3, r=36, son=None):
    """Kırmızı çarpı (iki ayrı çizgi; tek yolda çoklu M birleşiyordu)."""
    A.ekle(f'carpi-{b}-{x}', G(yol(f'M{x - r} {y - r} L{x + r} {y + r}'), st(KIRMIZI, 9)), G(yol(f'M{x + r} {y - r} L{x - r} {y + r}'), st(KIRMIZI, 9)),
           o=belir(A, b, fr, son if son is not None else b))


def kart(cx, cy, w, h, kenar, *ic, o=96):
    return [G(rc(cx, cy, w, h, 14), fl('#ffffff', o=o), st(kenar, 2.5)), *ic]


def kesit(A, o=None, dahil=(), haric=()):
    s = Sahne2B('ng-kesit')
    s.ekle(A, dahil=list(dahil), haric=list(haric), o=o)
    return s


# ———————————————————————— 1. Giriş: sonda nedir, neden sen takacaksın

def a_giris(A):
    s = kesit(A)
    # s0: sonda burundan girer, damağa paralel arkaya, farinkste aşağı, özofagusa
    sonda(A, 0, .08, .8)
    et(A, 0, 175, 70, 'Burun deliğinden girer', 'bilgi', .04)
    ok(A, 'M575 230L575 302', 0, renk=YESIL_A, f1=.78, f2=1)
    et(A, 0, 640, 190, 'Özofagustan mideye', 'dogru', .8)
    A.kamera_sabit(0, 0, 400, 250, 100)
    # s1: işi kim yapar — baş vurgusu; hemşire / hekim
    halka(A, 330, 150, 250, 190, 1, renk=SARI, nm='halka-bas')
    et(A, 1, 300, 40, 'Çoğu zaman: hemşire', 'bilgi', .05)
    et(A, 1, 300, 260, 'Bilinçsiz, çocuk: hekim', 'uyari', .45)
    # s2: tekniği tek başına — sonda boyunca yeşil vurgu
    A.ekle('sonda-vurgu', G(yol(SONDA), st(YESIL_A, 15, o=35)), o=belir(A, 2, .1, 2))
    et(A, 2, 300, 50, 'Tek başına uygulayabil', 'dogru', .2)
    # s3: üç soru; yanlış yol trakea kırmızı, doğru yol özofagus yeşil
    A.kamera(3, 495, 372, 190, f=.0)
    boya(A, s, 'nk-trakea', KIRMIZI, 3, .2, o=65)
    boya(A, s, 'nk-ozofagus', YESIL_A, 3, .2, o=55)
    carpi(A, 455, 350, 3, .3, r=13)
    tik(A, 575, 335, 3, .35)
    et(A, 3, 420, 310, 'Trakea: yanlış yol', 'uyari', .25)
    et(A, 3, 600, 290, 'Özofagus: doğru yol', 'dogru', .3)
    et(A, 3, 495, 220, 'Kime? Kime değil? Nasıl?', 'bilgi', .05)


# ———————————————————————— 2. Endikasyonlar (ng-mide)

AKIS_IC = 'M443 0 L443 122 C444 170 446 230 448 292'
AKIS_DIS = 'M448 292 C446 230 444 170 443 122 L443 0'


def _alt_yollar(d):
    """Çoklu M'li yolu alt yollara böler (yol() alt yolları çizgiyle birleştiriyordu)."""
    return ['M' + x.strip() for x in d.split('M') if x.strip()]


def a_endikasyon(A):
    T = A.T
    m = Sahne2B('ng-mide')
    m.ekle(A)
    # sonda (s0'da yukarıdan iner; s1 boyunca söner, s2'de geri gelir)
    o_s = K((0, 0), (T(0, .04), 0), (T(0, .1), 100), (T(1, .02), 100), (T(1, .1), 0), (T(2, 0), 0), (T(2, .08), 100))
    A.ekle('nd-sonda', *m.katman('nd-sonda'), o=o_s)
    A.ekle('sonda-in', *kateter_cizgi(AKIS_IC, 7, NG), o=K((0, 0), (T(0, .04), 0), (T(0, .1), 100), (T(0, .4), 100), (T(0, .41), 0)))
    # s0: lavaj suyu sondadan mideye (zehirlenme)
    A.ekle('sonda-ilerle', *kateter_cizgi(AKIS_IC, 7, NG, e=K((0, 0), (T(0, .05), 0), (T(0, .38), 100))), o=belir(A, 0, .0, 0))
    akis(A, AKIS_IC, T(0, .42), T(0, 1), renk=MAVI, w=3, nm='lavaj', o=belir(A, 0, .42, 0))
    A.ekle('lavaj-yayil', G(el(452, 300, 70, 26), fl(JEL, o=55)), a=(452, 300), p=S([452, 300, 0]),
           s=K((0, [20, 20, 100]), (T(0, .55), [20, 20, 100]), (T(0, .9), [160, 120, 100])), o=belir(A, 0, .55, 0))
    et(A, 0, 640, 120, 'Mide lavajı: zehirlenme', 'dogru', .45)
    et(A, 0, 470, 230, 'Mide', 'etiket', .1)
    A.kamera_sabit(0, 0, 400, 250, 100)
    # s1: beslenme sondası (kılavuz telli), ucu duodenum başlangıcında
    bes = m.cz('nd-beslenme')[0]['d']
    A.ekle('beslenme', *kateter_cizgi(bes, 4.5, NG, e=K((0, 0), (T(1, .08), 0), (T(1, .5), 100))), o=belir(A, 1, .06, 1))
    A.ekle('besin', G(yol(bes), st('#e1a92e', 2.5, kesik=(8, 12), kesik_kayma=KD((T(1, .55), 0), (T(1, 1), -120)))), o=belir(A, 1, .55, 1))
    et(A, 1, 560, 60, 'Beslenme sondası', 'bilgi', .1)
    et(A, 1, 230, 230, 'Duodenum', 'etiket', .4)
    et(A, 1, 560, 330, 'PEG takılana kadar', 'dogru', .6)
    # s2: mide içeriğini boşaltma — torba mide hizasının altında, içerik sondadan torbaya
    A.ekle('torba', *m.katman('nd-torba'), o=belir(A, 2, .02, 3))
    for j, d in enumerate(_alt_yollar(m.cz('nd-akis')[0]['d'])):
        akis(A, d, T(2, .25), T(3, 1), renk='#b08a3e', w=3, nm=f'bosalt-{j}', o=belir(A, 2, .25, 2))
    et(A, 2, 700, 110, 'Drenaj torbası', 'bilgi', .1)
    et(A, 2, 470, 330, 'Mide içeriği boşaltılır', 'dogru', .35)
    # s3: üst GİS kanaması şüphesi — mide içeriği kırmızı, torbaya kanlı içerik
    A.ekle('kanli-sivi', G(yol('M298 242 L556 240 C562 282 540 318 470 324 C410 328 340 290 298 242 Z'), fl('#b3261e', o=55)), o=belir(A, 3, .1, 3))
    for j, d in enumerate(_alt_yollar(m.cz('nd-akis')[0]['d'])):
        akis(A, d, T(3, .2), T(3, 1), renk='#b3261e', w=3, nm=f'kanli-{j}', o=belir(A, 3, .2, 3))
    halka(A, 440, 291, 175, 64, 3, renk=KIRMIZI, nm='halka-sivi')
    et(A, 3, 420, 120, 'Kanlı içerik: üst GİS kanama', 'uyari', .2)
    # s4: ilaç — ezilmiş tablet sıvıya karışır, enjektörle sondadan verilir
    A.ekle('enjektor', *m.katman('nd-enjektor'), o=belir(A, 4, .02, 4))
    A.ekle('tablet', G(yol('M580 70 C580 60 590 54 600 56 L596 76 Z'), fl('#ffffff'), st('#8a96a6', 2)),
           G(yol('M604 58 C614 62 618 78 612 86 L598 78 Z'), fl('#ffffff'), st('#8a96a6', 2)),
           G(el(625, 92, 5, 5), fl('#c9d3de')), G(el(615, 100, 4, 4), fl('#c9d3de')), G(el(630, 80, 4, 4), fl('#c9d3de')),
           o=K((0, 0), (T(4, .05), 0), (T(4, .12), 100), (T(4, .4), 100), (T(4, .5), 0)))
    for j, d in enumerate(_alt_yollar(m.cz('nd-su')[0]['d'])):
        akis(A, d, T(4, .45), T(4, 1), renk='#8e5bd0', w=3, nm=f'ilac-{j}', o=belir(A, 4, .45, 4))
    halka(A, 445, 150, 30, 140, 4, renk=SARI, nm='halka-sonda')
    et(A, 4, 560, 50, 'Ezilmiş ilaç + sıvı', 'bilgi', .08)
    et(A, 4, 300, 160, 'Nazogastrik sonda', 'etiket', .4)
    # s5: hepsi bir arada — endikasyon özeti
    halka(A, 427, 209, 150, 105, 5, renk=YESIL_A, nm='halka-mide')
    tik(A, 427, 200, 5, .3)
    et(A, 5, 560, 60, 'Lavaj · beslenme · boşaltma', 'dogru', .05)
    et(A, 5, 560, 330, 'Kontrendikasyonla birlikte', 'uyari', .45)


# ———————————————————————— 3. Kontrendikasyon 1–2: yüz travması, kafa tabanı kırığı

YUZ_KIRIK = 'M130 260C128 220 134 174 152 140C164 126 186 132 196 122C202 110 192 86 184 64'  # burun deliğinden girer, boşluk içinde kırık hattına sapar
KAFA_KIRIK = 'M130 260C128 220 134 174 152 140C164 126 186 136 210 135C246 130 278 80 297 26'


def a_travma(A):
    s = kesit(A)
    # s0: yüz kemikleri vurgusu (travma iki kontrendikasyon)
    halka(A, 178, 136, 50, 118, 0, renk=SARI, nm='halka-yuz')
    et(A, 0, 300, 20, 'Yüz kemikleri', 'etiket', .1)
    et(A, 0, 330, 260, 'Kime takılmaz? Travma', 'uyari', .4)
    A.kamera_sabit(0, 0, 400, 250, 100)
    # s1: sonda burun → sert damak boyunca ilerler (bu bölgeden geçer)
    sonda(A, 1, .05, .75, son=1)
    halka(A, 292, 142, 125, 26, 1, renk=SARI, f1=.4, nm='halka-damak')
    et(A, 1, 290, 220, 'Sert damak boyunca', 'bilgi', .4)
    et(A, 1, 175, 70, 'Burun', 'etiket', .05)
    # s2: yüzde deprese kırık — sonda kırık hattına sapar → zarar
    A.kamera(2, 230, 120, 170, f=.0)
    A.ekle('kirik', *s.katman('nk-kirik'), o=belir(A, 2, .08, 3))
    boya(A, s, 'nk-yuz-kemik', KIRMIZI, 2, .15, son=2, o=55)
    A.ekle('sonda-yuz', *kateter_cizgi(YUZ_KIRIK, 7, NG_K, e=K((0, 0), (A.T(2, .35), 0), (A.T(2, .65), 100))), o=belir(A, 2, .33, 2))
    kivilcim(A, 184, 66, 2, .66)
    carpi(A, 230, 80, 2, .75, r=24)
    et(A, 2, 290, 160, 'Kırık hattı: zarar verir', 'uyari', .2)
    # s3: kafa tabanı kırığı — kafa tabanı burun boşluğunun hemen üstünde; sonda kırıktan kafa içine
    A.kamera(3, 400, 250, 100, f=.0)
    boya(A, s, 'nk-kafa-tabani', KIRMIZI, 3, .05, o=55)
    halka(A, 374, 74, 200, 66, 3, renk=KIRMIZI, f2=.4, nm='halka-kafa')
    A.ekle('sonda-kafa', *kateter_cizgi(KAFA_KIRIK, 7, NG_K, e=K((0, 0), (A.T(3, .2), 0), (A.T(3, .45), 100))), o=belir(A, 3, .18, 3))
    ok(A, 'M298 34L310 4', 3, renk=KIRMIZI, w=4, f1=.45, f2=1)
    et(A, 3, 420, 40, 'Kırıktan kafa içine', 'uyari', .45)
    et(A, 3, 600, 90, 'Kafa tabanı', 'etiket', .05)
    takilmaz(A, 3, 250, 200, fr=.62, r=40, et_xy=(250, 280))


# ———————————————————————— 4. Kontrendikasyon 3: koroziv madde

KUSMA_YOL = 'M522 450L522 330C522 300 520 270 520 230L518 192'


def a_koroziv(A):
    T = A.T
    s = kesit(A)
    # s0: koroziv madde → farinks-özofagus mukozasında yanık
    A.ekle('sise', G(rc(70, 230, 40, 64, 6), fl('#f6f2dc'), st('#8a7a3a', 2)), G(rc(70, 192, 18, 16, 3), fl('#c62828'), st('#7a1a1a', 1.5)),
           G(yol('M70 214L86 242L54 242Z'), fl('#ffffff'), st(KIRMIZI, 2.5)), G(yol('M70 222L70 232'), st(KIRMIZI, 3)),
           o=belir(A, 0, .02, 0))
    A.ekle('yanik', *s.katman('nk-yanik'), o=belir(A, 0, .2))
    halka(A, 505, 302, 46, 112, 0, renk=KIRMIZI, f1=.3, nm='halka-yanik0')
    et(A, 0, 120, 140, 'Yakıcı madde', 'uyari', .05)
    et(A, 0, 610, 230, 'Koroziv yanık', 'uyari', .3)
    A.kamera_sabit(0, 0, 400, 250, 100)
    # s1: sonda yanmış mukozaya değer → yeniden zarar
    A.kamera(1, 490, 330, 170, f=.0)
    boya(A, s, 'nk-ozofagus', KIRMIZI, 1, .1, o=45)
    boya(A, s, 'nk-orofarinks', KIRMIZI, 1, .1, o=30)
    A.ekle('yanik-vurgu', *_boya(s.katman('nk-yanik'), '#7a1a10', 100), o=belir(A, 1, .1, 3))
    sonda(A, 1, .12, .62, renk=NG_K, son=1, son_f=1)
    for i, (x, y) in enumerate([(528, 220), (481, 246), (528, 268)]):
        kivilcim(A, x, y, 1, .66 + i * .06, nm=f'kiv1-{i}')
    et(A, 1, 400, 200, 'Yanmış mukozaya sürtünür', 'uyari', .6)
    # s2: kusma — içerik özofagustan yukarı çıkar, aynı dokuyu yeniden yakar
    A.ekle('kusma', G(yol(KUSMA_YOL), st(KUSMUK, 14, o=80), tm(K((0, 0), (T(2, .12), 0), (T(2, .6), 100)))), o=belir(A, 2, .1, 2))
    ok(A, 'M556 350L556 220', 2, renk='#8a7a20', w=5, f1=.15, f2=1)
    for i, (x, y) in enumerate([(528, 354), (528, 268), (528, 220)]):
        kivilcim(A, x, y, 2, .45 + i * .08, nm=f'kiv2-{i}')
    et(A, 2, 620, 180, 'Kusma: yeniden yakar', 'uyari', .2)
    # s3: lavaj endikasyonu olsa bile takılmaz
    A.kamera(3, 400, 250, 100, f=.0)
    et(A, 3, 330, 10, 'Lavaj gerekse bile', 'bilgi', .05)
    takilmaz(A, 3, 330, 180, fr=.35, r=44, et_xy=(330, 80), metin='Koroziv: sonda takılmaz')


# ———————————————————————— 5. Kontrendikasyon 4: bilinç kapalı, hava yolu korunmuyor

ASPIRASYON = 'M526 302C526 282 500 280 494 310L492 400'


def a_bilinc(A):
    T = A.T
    s = kesit(A)
    # s0: larinks (hava yolu) vurgusu
    A.kamera(0, 490, 360, 175, f=.0)
    halka(A, 484, 338, 40, 46, 0, renk=SARI, nm='halka-larinks')
    et(A, 0, 400, 230, 'Larinks: hava yolu', 'etiket', .1)
    et(A, 0, 560, 220, 'Bilinç kapalı', 'uyari', .45)
    # s1: sonda bulantı → kusma → içerik trakeaya kaçar
    sonda(A, 1, .02, .3, son=3, son_f=.3)
    kus = s.katman('nk-kusmuk')
    A.ekle('kusmuk', kus[0], kus[1], o=belir(A, 1, .4, 2))
    ok(A, ASPIRASYON, 1, renk=KIRMIZI, w=4, f1=.55, f2=1)
    ok(A, ASPIRASYON, 2, renk=KIRMIZI, w=4, f1=.0, f2=1, nm='ok-asp2')
    et(A, 1, 560, 230, 'Kusma', 'uyari', .4)
    et(A, 1, 410, 260, 'Trakeaya kaçar', 'uyari', .6)
    # s2: aspirasyon — trakea kırmızı
    boya(A, s, 'nk-trakea', KIRMIZI, 2, .1, o=65)
    halka(A, 486, 400, 32, 44, 2, renk=KIRMIZI, nm='halka-trakea')
    et(A, 2, 470, 210, 'Aspirasyon: yaşamı tehdit', 'uyari', .2)
    # s3: önce hava yolu güvence; korunmuyorsa sonda takılmaz
    A.kamera(3, 400, 250, 100, f=.0)
    halka(A, 489, 275, 22, 40, 3, renk=YESIL_A, f2=.5, nm='halka-epiglot')
    et(A, 3, 600, 230, 'Önce hava yolu güvencesi', 'dogru', .05)
    takilmaz(A, 3, 330, 180, fr=.35, r=44, et_xy=(330, 80), metin='Korunmuyorsa takılmaz')


# ———————————————————————— 6. Kontrendikasyon 5: özofagus varisi (büyüteç kartı)

KX, KY = 660, 190   # kart merkezi (kafatası arkası boş alan üstünde)


def _kart_ozofagus():
    """Büyüteç kartı: özofagus duvarı (iki yan), içi lümen."""
    return [*kart(KX, KY, 220, 250, '#3e4a58'),
            G(rc(KX, KY + 6, 120, 210, 10), fl('#fbeee9'), st('#a85f5a', 2.5)),
            G(yol(f'M{KX - 60} {KY - 99} L{KX - 60} {KY + 111}'), st('#d98f88', 10, o=70)),
            G(yol(f'M{KX + 60} {KY - 99} L{KX + 60} {KY + 111}'), st('#d98f88', 10, o=70))]


def _varis_yol(x, y0, y1, gen=9):
    d, y, sag = f'M{x} {y0}', y0, 1
    while y < y1:
        d += f' C{x + gen * sag} {y + 8} {x + gen * sag} {y + 22} {x} {y + 30}'
        y += 30; sag = -sag
    return d


def a_varis(A):
    T = A.T
    s = kesit(A)
    # s0: alt özofagusta varis; büyüteç kartında genişlemiş venler
    A.ekle('varis', *s.katman('nk-varis'), o=belir(A, 0, .1))
    A.ekle('kart', *_kart_ozofagus(), o=belir(A, 0, .15))
    A.ekle('kart-bag', G(yol(f'M{KX - 110} {KY + 110} L536 360'), st('#3e4a58', 2, kesik=(6, 5))), G(el(522, 370, 34, 34), st('#3e4a58', 2, kesik=(6, 5))),
           o=belir(A, 0, .15))
    vy = [_varis_yol(KX - 48, KY - 90, KY + 100), _varis_yol(KX + 48, KY - 80, KY + 100)]
    A.ekle('kart-varis', *[G(yol(d), st('#4b3f9e', 9), tm(K((0, 0), (T(0, .25), 0), (T(0, .6), 100)))) for d in vy],
           *[G(yol(d), st('#7d6fd0', 5), tm(K((0, 0), (T(0, .25), 0), (T(0, .6), 100)))) for d in vy], o=belir(A, 0, .25))
    et(A, 0, KX, 45, 'Genişlemiş venler', 'bilgi', .3)
    et(A, 0, 400, 260, 'Özofagus varisi', 'uyari', .5)
    A.kamera_sabit(0, 0, 400, 250, 100)
    # s1: kanamaya yatkın — varis kırmızı, damla
    boya(A, s, 'nk-varis', KIRMIZI, 1, .1, o=80)
    A.ekle('kart-varis-k', *[G(yol(d), st('#b3261e', 9)) for d in vy], o=belir(A, 1, .1))
    for i, (x, y) in enumerate([(KX - 30, KY - 10), (KX + 32, KY + 40)]):
        A.ekle(f'kan-{i}', damla(0, 0, .8, '#b3261e'), p=K((0, [x, y, 0]), (T(1, .3 + i * .1), [x, y, 0]), (T(1, .8 + i * .1), [x, y + 50, 0])),
               o=K((0, 0), (T(1, .3 + i * .1), 0), (T(1, .36 + i * .1), 100), (T(1, .8 + i * .1), 100), (T(1, .9 + i * .1), 0)))
    et(A, 1, 400, 230, 'Kanamaya yatkın', 'uyari', .15)
    et(A, 1, 400, 50, 'Üst GİS kanamasıyla gelir', 'bilgi', .5)
    # s2: kanama normalde endikasyon — ama varis biliniyorsa takılmaz; sonda iner
    sonda(A, 2, .05, .45, son=3)
    A.ekle('kart-sonda', *kateter_cizgi(f'M{KX} {KY - 112} L{KX} {KY + 112}', 14, NG,
                                        e=K((0, 0), (T(2, .4), 0), (T(2, .7), 100))), o=belir(A, 2, .38, 2))
    et(A, 2, 330, 30, 'Kanama: normalde endikasyon', 'bilgi', .05)
    et(A, 2, 330, 230, 'Varis biliniyorsa: takma', 'uyari', .6)
    # s3: sonda genişlemiş venlere sürtünür → kanama artar
    A.ekle('kart-sonda-sur', *kateter_cizgi(f'M{KX} {KY - 112} L{KX} {KY + 112}', 14, NG_K),
           p=K((0, [0, 0, 0]), (T(3, .05), [0, 0, 0]), (T(3, .15), [-30, 0, 0]), (T(3, .25), [30, 0, 0]), (T(3, .35), [-30, 0, 0]),
               (T(3, .45), [30, 0, 0]), (T(3, .55), [0, 0, 0])), o=belir(A, 3, .0))
    for i, (x, y) in enumerate([(KX - 40, KY - 30), (KX + 40, KY + 10), (KX - 40, KY + 60), (KX + 40, KY - 60)]):
        kivilcim(A, x, y, 3, .15 + i * .1, nm=f'kiv3-{i}')
    A.ekle('kart-kan', G(yol(f'M{KX - 54} {KY + 70} C{KX - 54} {KY + 90} {KX - 44} {KY + 108} {KX - 30} {KY + 110} L{KX + 30} {KY + 110} '
                            f'C{KX + 44} {KY + 108} {KX + 54} {KY + 90} {KX + 54} {KY + 70} Z'), fl('#b3261e', o=75)),
           o=belir(A, 3, .5))
    et(A, 3, 620, 45, 'Sürtünme kanamayı artırır', 'uyari', .2)
    takilmaz(A, 3, 300, 180, fr=.55, r=44, et_xy=(300, 80), metin='Varis bilinen: takılmaz')


# ———————————————————————— 7. Anatomi: iki delik ve başın öne eğilmesi

def _mini_bas(cx, cy, aci, iyi):
    """Küçük profil baş ikonu (yüz sola): boyun sabit, baş boyun üstünde aci kadar döner (+ = arkaya düşmüş)."""
    bas = G(G(el(0, -30, 54, 58), fl('#f3c8a3'), st('#b9805a', 2.5)), G(yol('M-26 -32L-40 -18L-24 -14Z'), fl('#f3c8a3'), st('#b9805a', 2)),
            G(el(-10, -36, 5, 5), fl('#3e4a58')), p=(cx, cy), r=aci)
    return [G(rc(cx + 2, cy + 18, 22, 40, 6), fl('#f3c8a3'), st('#b9805a', 2.5)), bas]


def a_anatomi(A):
    T = A.T
    s = kesit(A)
    # s0: iki giriş — önde trakea (mavi), arkada özofagus (yeşil)
    A.kamera(0, 495, 372, 190, f=.0)
    boya(A, s, 'nk-trakea', MAVI, 0, .1, son=1, o=55)
    boya(A, s, 'nk-larinks', MAVI, 0, .1, son=1, o=40)
    boya(A, s, 'nk-ozofagus', YESIL_A, 0, .3, son=1, o=55)
    et(A, 0, 420, 325, 'Önde: trakea', 'bilgi', .1)
    et(A, 0, 610, 310, 'Arkada: özofagus', 'dogru', .3)
    # s1: larinksten geçerse trakeaya (kırmızı, çarpı); özofagustan geçerse mideye
    sonda(A, 1, .05, .55, d=SONDA_TR, renk=NG_K, nm='sonda-tr', son=1, son_f=1)
    carpi(A, 452, 350, 1, .6, r=13)
    ok(A, 'M560 322L560 370', 1, renk=YESIL_A, w=4, f1=.75, f2=1)
    et(A, 1, 400, 230, 'Larinksten: trakeaya', 'uyari', .45)
    et(A, 1, 610, 260, 'Özofagustan: mideye', 'dogru', .75)
    # s2: baş öne eğik — yol özofagusa açılır, sonda rahat ilerler
    A.kamera(2, 400, 250, 100, f=.0)
    sonda(A, 2, .1, .75, son=3)
    A.ekle('ok-duz', *s.katman('nk-ok-duz'), o=belir(A, 2, .15, 2))
    A.ekle('ok-asagi', *s.katman('nk-ok-asagi'), o=belir(A, 2, .45, 2))
    ok(A, 'M112 230C118 266 150 286 196 286', 2, renk=YESIL_A, w=5, f1=.1, f2=1, nm='ok-egim')
    et(A, 2, 330, 320, 'Çene göğse: baş öne', 'dogru', .1)
    et(A, 2, 620, 130, 'Yol özofagusa açılır', 'dogru', .5)
    # s3: maket başı arkaya düşmüş gibi; gerçek hastada baş öne
    halka(A, 360, 180, 260, 200, 3, renk=SARI, f2=.35, nm='halka-bas')
    A.ekle('kart-bas', *kart(660, 145, 250, 190, '#3e4a58'), *_mini_bas(605, 125, 40, False), *_mini_bas(715, 125, -25, True),
           o=belir(A, 3, .3))
    carpi(A, 605, 200, 3, .42, r=13)
    tik(A, 718, 196, 3, .5)
    et(A, 3, 330, 290, 'Maket: baş arkada', 'uyari', .35)
    et(A, 3, 330, 336, 'Hasta: başı öne eğdir', 'dogru', .55)


ADIMLAR = {
    'ng-giris': a_giris,
    'ng-endikasyon': a_endikasyon,
    'ng-kontrendikasyon-travma': a_travma,
    'ng-kontrendikasyon-koroziv': a_koroziv,
    'ng-kontrendikasyon-bilinc': a_bilinc,
    'ng-kontrendikasyon-varis': a_varis,
    'ng-anatomi': a_anatomi,
}
