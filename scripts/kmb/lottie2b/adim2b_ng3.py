"""KMB 01 Nazogastrik sonda — adım videoları, 2B düz çizgi film hattı, GRUP NG3 (adim2b.py bunları toplar).
Adımlar: ng-yutkunma, ng-oksuruk, ng-yer-kontrol, ng-lavaj (+ ng-ilerletme, ng-sabitleme: ng-burun sahnesi hazır olunca).
Sahneler: ng-kesit, ng-mide, ng-govde (svg/<sahne>.lottie.json). Yalnız koreografi; sonda sahnedeki `cz` yolu boyunca
ilerler (ilerleyen_kateter, NG açık plastik renk). Not: ng-kesit bbox değerleri farinks bölgesinde çizimle örtüşmüyor
(x ≈ 50–80 px kayık); bu yüzden farinks çevresinde koordinatlar cz yollarından ve kare ölçümünden alındı.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ortak2b import *  # noqa: E402,F401,F403
from lottie_dsl import yumruk  # noqa: E402

NG = ('#e9eef3', '#6b7a90')          # NG sonda: açık plastik gövde, kontur
NG_YANLIS = ('#f8dada', '#d23b3b')   # trakeaya giden yanlış sonda
SU = '#2f6fd6'
ICERIK = '#d6a840'
# ng-mide: sondanın midedeki ucundan kadraj içinde kıvrılıp bağlantı ağzına (680,146) inen kesintisiz dış seyri
DIS = 'M448 292 C446 230 444 170 443 122 L443 46 C443 16 466 12 500 12 L630 12 C664 12 680 28 680 56 L680 146'
DIS_TERS = 'M680 146 L680 56 C680 28 664 12 630 12 L500 12 C466 12 443 16 443 46 L443 122 C444 170 446 230 448 292'
TORBA_HORTUM = 'M680 150 L680 176 C680 214 748 214 748 256 L748 342'
STET_DX = 34                         # gövde sahnesinde stetoskop diyaframı epigastriuma oturur                   # mide içeriği (sarı akış)


def _kesit_sonda_d(s, id_='nk-sonda'):
    return s.cz(id_)[0]['d']


def _baglanti(A, o, nm='ng-agiz'):
    """Sondanın dış ucundaki renkli bağlantı ağzı (kesit sahnesinde yol başı 130,260)."""
    A.ekle(nm, G(yol('M121 260 L139 260 L141 282 L119 282 Z'), fl(YESIL), st('#1f6b3e', 2)), o=o)


def _sahne_gecis(A, b_bitis, b_bas, f=8):
    """Çapraz solma yerine ardışık solma: önceki sahne b_bas başında söner, yeni sahne hemen ardından belirir."""
    k = A.T(b_bas)
    eski = K((0, 100), (k - f, 100), (k, 0))
    yeni = K((0, 0), (k, 0), (k + f, 100))
    return eski, yeni


def _gor_aralik(A, k1, k2, f=6):
    return K((0, 0), (k1, 0), (k1 + f, 100), (k2, 100), (k2 + f, 0))


def _darbeler(A, araliklar, f=4):
    """Birden çok görünme aralığı [(k1, k2), …] → opaklık anahtarları."""
    ks = [(0, 0)]
    for k1, k2 in araliklar:
        ks += [(k1, 0), (k1 + f, 100), (k2, 100), (k2 + f, 0)]
    return K(*ks)


def _kabarciklar(A, x, y1, y2, k0, k1, nm, n=6):
    """Sıvıda yükselen hava kabarcıkları: k0..k1 arasında n kabarcık uçtan (x, y1) sıvı yüzeyine (y2) çıkar."""
    for i in range(n):
        a = k0 + (k1 - k0) * i / n
        b = a + (k1 - k0) * .55
        dx = (-6, 5, -2, 8, -8, 3)[i % 6]
        r = (7, 5, 9, 6, 5, 8)[i % 6]
        A.ekle(f'{nm}-{i}', G(el(0, 0, r, r), fl('#ffffff', o=90), st('#5b6676', 1.4)),
               p=KD((a, [x, y1, 0]), (b, [x + dx, y2, 0])), o=K((0, 0), (a, 0), (a + 2, 100), (b - 3, 100), (b, 0)))


def _ses_yaylari(A, cx, cy, araliklar, nm, yon=-1):
    """Fokurdama ses yayları (yeşil, iç içe 3 yay) — her aralıkta yanıp söner."""
    for j, r in enumerate((16, 28, 40)):
        d = f'M{cx + yon * r * .2} {cy - r} C{cx + yon * r * 1.1} {cy - r * .6} {cx + yon * r * 1.1} {cy + r * .6} {cx + yon * r * .2} {cy + r}'
        ar = [(k1 + j * 3, k2) for k1, k2 in araliklar]
        A.ekle(f'{nm}-{j}', G(yol(d), st(YESIL, 3.5)), o=_darbeler(A, ar))


def _enjektor(A, x, ust, o, piston, nm='enj', su=None):
    """Çan uçlu 50 mL enjektör, ucu yukarıda (x, ust). piston: konum kareleri (0 = çekili, -70 = itilmiş).
    su: (k1, k2) verilirse gövde suyla dolu, piston itildikçe su azalır."""
    y0 = ust
    A.ekle(nm + '-govde',
           G(yol(f'M{x - 6} {y0} L{x + 6} {y0} L{x + 10} {y0 + 28} L{x - 10} {y0 + 28} Z'), fl('#dfe6ee'), st(NG[1], 2)),
           G(rc(x, y0 + 81, 40, 106, 4), fl('#f3f7fb'), st(NG[1], 2.2)),
           *[G(yol(f'M{x + 8} {y0 + 50 + i * 18} L{x + 20} {y0 + 50 + i * 18}'), st(NG[1], 1.4)) for i in range(5)],
           G(rc(x, y0 + 136, 62, 7, 2), fl('#dfe6ee'), st(NG[1], 2)), o=o)
    if su:
        k1, k2 = su
        A.ekle(nm + '-su', G(rc(x, y0 + 75, 36, 82), fl('#8fc7ff', o=75)), a=(x, y0 + 34), p=S([x, y0 + 34, 0]),
               s=K((0, [100, 100, 100]), (k1, [100, 100, 100]), (k2, [100, 18, 100])), o=o)
    A.ekle(nm + '-piston',
           G(rc(x, y0 + 159, 10, 72), fl('#c9d3de'), st(NG[1], 1.6)),
           G(rc(x, y0 + 196, 46, 7, 2), fl('#c9d3de'), st(NG[1], 1.8)),
           G(rc(x, y0 + 118, 36, 10, 2), fl('#3e4a58')), p=piston, o=o)


# ———————————————————————— 1. Orofarinks: yutkunma telkini ve su (ng-kesit)

def a_yutkunma(A):
    T = A.T
    s = Sahne2B('ng-kesit')
    s.ekle(A, haric=['nk-epiglot'])
    # epiglot: yutkunmada (s2 ve s3'teki üç itişte) gizlenir, kapalı konum görünür
    itis = [(T(3, .08), T(3, .3)), (T(3, .4), T(3, .62)), (T(3, .72), T(3, .94))]
    kapali = [(T(2, .25), T(2, 1))] + itis
    acik_ks = [(0, 100)]
    for k1, k2 in kapali:
        acik_ks += [(k1, 100), (k1 + 4, 0), (k2, 0), (k2 + 4, 100)]
    A.ekle('epiglot', *s.katman('nk-epiglot'), o=K(*acik_ks))
    A.ekle('epiglot-kapali', *s.katman('nk-epiglot-kapali'), o=_darbeler(A, kapali))
    # sonda: burun deliğinden damağa paralel, nazofarinkste aşağı → orofarinks (s0); her yutkunmada biraz daha (s3)
    d = _kesit_sonda_d(s)
    _baglanti(A, None)
    ilerleyen_kateter(A, d, [(T(0), (152, 140)), (T(0, .25), (300, 128)), (T(0, .4), (405, 119)), (T(0, .6), (518, 222)),
                             (itis[0][0], (518, 222)), (itis[0][1], (520, 275)), (itis[1][0], (520, 275)), (itis[1][1], (520, 330)),
                             (itis[2][0], (520, 330)), (itis[2][1], (520, 390)), (T(5, 1), (520, 390))],
                      w=4.4, renk=NG, nm='sonda')
    # s0: orofarinks vurgusu + hekimin sözü
    A.kamera(0, 440, 275, 125, f=.55)
    halka(A, 508, 242, 34, 50, 0, f1=.6, f2=.98, nm='halka-orofarinks')
    et(A, 0, 590, 230, 'Orofarinks', 'etiket', .6)
    et(A, 0, 330, 70, '"Ben söyleyince yutkunun"', 'bilgi', .65)
    # s1: dil — "ekmek yutar gibi"
    halka(A, 340, 230, 110, 50, 1, nm='halka-dil')
    et(A, 1, 330, 160, '"Ekmek yutar gibi yutkunun"', 'bilgi', .1)
    # s2: epiglot larinksi kapatır, lokma/sonda özofagusa: yeşil ok + yeşil özofagus vurgusu, trakeaya çarpı
    ok(A, 'M508 230 C512 270 518 310 520 380', 2, renk=YESIL, w=5, f1=.35, f2=.98, nm='ok-ozofagus')
    A.ekle('ozofagus-yesil', G(rc(522, 340, 30, 80, 12), fl(YESIL, o=22), st(YESIL, 3)), o=belir(A, 2, .45, 2))
    halka(A, 488, 282, 26, 22, 2, renk=YESIL, f1=.25, f2=.98, nm='halka-epiglot')
    et(A, 2, 600, 230, 'Epiglot larinksi kapatır', 'dogru', .28)
    et(A, 2, 600, 110, 'Sonda özofagusa gider', 'dogru', .5)
    # s3: her yutkunmada biraz it — "yutkun" işaretleri
    et(A, 3, 330, 80, 'Her yutkunmada biraz it', 'bilgi', .05)
    et(A, 3, 600, 230, 'İşarete kadar ilerlet', 'dogru', .5)
    # s4: su yudumu (enjektörle 0,5 mL)
    A.ekle('su', *s.katman('nk-su'), o=belir(A, 4, .15, 4))
    et(A, 4, 340, 100, 'Enjektörle 0,5 mL su', 'bilgi', .15)
    tik(A, 250, 180, 4, .4)
    et(A, 4, 600, 230, 'Bilinci açık hasta', 'dogru', .45)
    # s5: güvenle yutamayan hastaya su yok — trakea kırmızı (aspirasyon), su çarpı
    A.ekle('su-yanlis', *s.katman('nk-su'), o=K((0, 0), (T(5), 0), (T(5, .05), 60), (T(5, .5), 60), (T(5, .6), 0)))
    carpi(A, 340, 192, 5, .15, r=26)
    A.ekle('trakea-kirmizi', G(rc(492, 375, 26, 110, 10), fl(KIRMIZI, o=22), st(KIRMIZI, 3)), o=belir(A, 5, .2, 5))
    et(A, 5, 330, 90, 'Yutamayana su verilmez', 'uyari', .1)
    et(A, 5, 600, 230, 'Aspirasyon riski', 'uyari', .3)
    A.kamera(5, 420, 260, 120, f=.0)


# ———————————————————————— 2. Öksürük ve hava yolu irritasyonu: geri çek (ng-kesit)

def a_oksuruk(A):
    T = A.T
    s = Sahne2B('ng-kesit')
    s.ekle(A)
    _baglanti(A, K((0, 100), (T(1, .6), 100), (T(1, .7), 0), (T(3), 0), (T(3, .03), 100)))
    # s0: yanlış yol — sonda larinksten trakeaya (kırmızı), öksürük çizgileri; s1: hemen geri çekilir
    dy = _kesit_sonda_d(s, 'nk-sonda-trakea')
    ilerleyen_kateter(A, dy, [(T(0), (152, 140)), (T(0, .2), (405, 119)), (T(0, .35), (516, 200)), (T(0, .55), (492, 350)),
                              (T(1, .05), (492, 350)), (T(1, .45), (405, 119)), (T(1, .6), (300, 128))],
                      w=4.4, renk=NG_YANLIS, nm='sonda-yanlis', o=K((0, 100), (T(1, .6), 100), (T(1, .7), 0)))
    oks = [(T(0, .55) + i * 9, T(0, .55) + i * 9 + 6) for i in range(6)]
    for j, d in enumerate(('M105 198 L80 188', 'M104 210 L76 212', 'M106 222 L82 234')):
        A.ekle(f'oksuruk-{j}', G(yol(d), st(KIRMIZI, 3.5)), o=_darbeler(A, oks + [(T(0, .85), T(0, 1))], f=2))
    carpi(A, 560, 310, 0, .6, r=22)
    et(A, 0, 300, 50, 'Öksürük: sonda larinkste', 'uyari', .55)
    # s1: geri çekme oku, larinks vurgusu
    ok(A, 'M470 260 C460 180 430 135 380 126', 1, renk=KIRMIZI, w=5, f1=.05, f2=.6, nm='ok-geri')
    halka(A, 486, 330, 32, 36, 1, renk=KIRMIZI, f1=.5, f2=.98, nm='halka-larinks')
    et(A, 1, 300, 50, 'Hemen geri çek', 'uyari', .05)
    # s2: yer kontrolünde ses yok → yanlış yer: trakea vurgusu + kulaklık/çarpı simgesi
    A.ekle('trakea-kirmizi', G(rc(492, 375, 26, 110, 10), fl(KIRMIZI, o=22), st(KIRMIZI, 3)), o=belir(A, 2, .1, 2))
    A.ekle('ses-yok', G(el(640, 80, 64, 64), fl('#ffffff'), st(NG[1], 2.5)),
           G(yol('M626 68 L634 68 L646 58 L646 102 L634 92 L626 92 Z'), fl('#5b6676')),
           G(yol('M654 68 L672 92 M672 68 L654 92'), st(KIRMIZI, 4)), o=belir(A, 2, .1, 2))
    et(A, 2, 330, 140, 'Midede ses yok: yanlış yer', 'uyari', .15)
    et(A, 2, 600, 230, 'Geri çek, yeniden dene', 'uyari', .5)
    # s3: doğru yol — sonda özofagusa; boğulma belirtisine güvenme, yer kontrolü şart
    d = _kesit_sonda_d(s)
    ilerleyen_kateter(A, d, [(T(3), (152, 140)), (T(3, .2), (405, 119)), (T(3, .35), (518, 222)), (T(3, .6), (520, 400))],
                      w=4.4, renk=NG, nm='sonda', o=belir(A, 3, 0, f=4))
    A.ekle('ozofagus-yesil', G(rc(522, 340, 30, 80, 12), fl(YESIL, o=22), st(YESIL, 3)), o=belir(A, 3, .6))
    tik(A, 590, 280, 3, .65, son=3)
    et(A, 3, 300, 50, 'Boğulmama ≠ doğru yer', 'uyari', .1)
    et(A, 3, 600, 190, 'Yer kontrolü mutlaka', 'dogru', .65)


# ———————————————————————— 3. Yer kontrolü: hava ver, epigastriumu dinle (ng-mide → ng-govde → ng-mide)

def a_yer_kontrol(A):
    T = A.T
    m = Sahne2B('ng-mide')
    g = Sahne2B('ng-govde')
    k4, k6 = T(4), T(6)
    om = K((0, 100), (k4 - 8, 100), (k4, 0), (k6, 0), (k6 + 8, 100))     # mide: s0–s3 ve s6–s7
    og = K((0, 0), (k4, 0), (k4 + 8, 100), (k6 - 8, 100), (k6, 0))       # gövde: s4–s5
    m.ekle(A, o=om)
    # sonda: midedeki uçtan özofagus boyunca yukarı, kadraj içinde kıvrılıp enjektör hizasına iner (kesintisiz dış uç)
    A.ekle('sonda', *kateter_cizgi(DIS, 4.4, NG), o=om)
    A.ekle('sonda-agiz', G(rc(680, 140, 16, 14, 2), fl(YESIL), st('#1f6b3e', 2)), o=om)
    # s0: piston geri çekilip hava alınır (enjektör ayrık, 60 px aşağıda) → enjektör yukarı kayıp ağza oturur → aniden itilir
    P = lambda off, v: [0, off + v, 0]  # noqa: E731
    a1, a2 = T(0, .36), T(0, .55)
    pis = KD((0, P(60, -70)), (T(0, .08), P(60, -70)), (T(0, .3), P(60, 0)), (a1, P(60, 0)), (a2, P(0, 0)),
             (T(0, .72), P(0, 0)), (T(0, .78), P(0, -70)),
             (T(1, .05), P(0, -70)), (T(1, .2), P(0, 0)), (T(1, .3), P(0, 0)), (T(1, .35), P(0, -70)),
             (T(3, .05), P(0, -70)), (T(3, .12), P(0, 0)), (T(3, .15), P(0, 0)), (T(3, .5), P(0, -70)),
             (T(3, .55), P(0, -70)), (T(3, .62), P(0, 0)), (T(3, .66), P(0, 0)), (T(3, .71), P(0, -70)),
             (T(6, .05), P(0, -70)), (T(6, .2), P(0, -30)), (T(7, 1), P(0, -30)))
    eo = K((0, 0), (T(0), 0), (T(0, .05), 100), (k4 - 8, 100), (k4, 0), (k6, 0), (k6 + 8, 100))
    _enjektor(A, 680, 150, eo, pis, nm='enj')
    A.katmanlar[-2]['ks']['p'] = K((0, [0, 60, 0]), (a1, [0, 60, 0]), (a2, [0, 0, 0]))  # gövde
    ok(A, 'M720 260 L720 200', 0, renk=MAVI, w=4, f1=.36, f2=.6, nm='ok-tak')
    et(A, 0, 560, 200, 'Sondanın ucuna tak', 'bilgi', .36, .7)
    et(A, 0, 560, 90, 'Çan uçlu enjektöre hava', 'bilgi', .05)
    et(A, 0, 560, 140, 'Havayı aniden ver', 'dogru', .72)
    # ani itişlerde kabarcıklar + ses yayları
    patla = [(T(0, .78), T(0, 1)), (T(1, .35), T(2, 1)), (T(3, .71), T(3, 1))]
    _kabarciklar(A, 448, 292, 240, T(0, .78), T(0, 1), 'kab0')
    _kabarciklar(A, 448, 292, 240, T(1, .35), T(1, 1), 'kab1')
    _kabarciklar(A, 448, 292, 240, T(2), T(2, .9), 'kab2')
    _kabarciklar(A, 448, 292, 240, T(3, .71), T(3, 1), 'kab3')
    # s1: stetoskop epigastriumda, fokurdama
    A.ekle('stetoskop', *m.katman('nd-stetoskop'), o=K((0, 0), (T(1), 0), (T(1, .1), 100), (k4 - 8, 100), (k4, 0)))
    _ses_yaylari(A, 360, 150, [(T(1, .38), T(1, .9)), (T(2, .05), T(2, .5)), (T(3, .74), T(3, .98))], 'ses', yon=-1)
    A.kamera(1, 470, 220, 125, f=.0)
    et(A, 1, 300, 250, 'Epigastrium', 'etiket', .1)
    et(A, 1, 330, 60, 'Fokurdama sesi', 'dogru', .4)
    # s2: sıvı dolu mide → hava girince ses; trakeada (hava dolu) ses yok
    halka(A, 440, 290, 150, 44, 2, nm='halka-sivi')
    et(A, 2, 600, 330, 'Sıvı dolu mide: ses olur', 'dogru', .1)
    et(A, 2, 250, 330, 'Trakeada ses olmaz', 'uyari', .55)
    # s3: yavaş verilen hava → ses yok (çarpı), ani → ses (tik)
    carpi(A, 300, 150, 3, .3, r=22, son=3)
    A.katmanlar[-1]['ks']['o'] = K((0, 0), (T(3, .3), 0), (T(3, .34), 100), (T(3, .5), 100), (T(3, .54), 0))
    et(A, 3, 560, 90, 'Yavaş verirsen ses yok', 'uyari', .15, .55)
    tik(A, 300, 150, 3, .74)
    et(A, 3, 560, 90, 'Aniden ver: fokurdama', 'dogru', .72)
    # s4–s5: gövde sahnesi — bir el sondayı tutar, öbür el hava verir; stetoskop boyunda; dinleyen sondayı takan
    g.ekle(A, dahil=['nb-sonda', 'nb-enjektor', 'nb-ozofagus'], o=og)
    A.ekle('stetoskop-govde', *g.katman('nb-stetoskop'), p=S([STET_DX, 0, 0]), o=og)
    A.kamera_sabit(4, 5, 400, 250, 100)
    A.ekle('el-sonda', yumruk(0, 0, .3, 152, steril=False), p=S([236, 170, 0]), o=K((0, 0), (T(4, .1), 0), (T(4, .2), 100), (k6 - 8, 100), (k6, 0)))
    A.ekle('el-enj', yumruk(0, 0, .3, 270, steril=False), p=S([172, 428, 0]), o=K((0, 0), (T(4, .35), 0), (T(4, .45), 100), (k6 - 8, 100), (k6, 0)))
    et(A, 4, 220, 90, 'Bir el sondayı tutar', 'bilgi', .15)
    et(A, 4, 150, 200, 'Öbür el hava verir', 'bilgi', .4)
    et(A, 4, 600, 230, 'Stetoskop önceden boyunda', 'bilgi', .6)
    A.ekle('ses-govde', *g.katman('nb-ses'), o=_darbeler(A, [(T(5, .1), T(5, .3)), (T(5, .45), T(5, .65)), (T(5, .8), T(5, .98))]))
    halka(A, 402, 366, 34, 34, 5, renk=YESIL, f1=.08, nm='halka-epigastr')
    et(A, 5, 620, 300, 'Dinleyen: sondayı takan sen', 'dogru', .1)
    et(A, 5, 200, 90, 'Enjektör yardımcıya', 'bilgi', .45)
    # s6: güvenilmeyen yöntemler ✗; mide içeriği aspirasyonu ✓ (piston geri çekilir, sarı içerik gelir)
    A.kamera_sabit(6, 7, 400, 250, 100)
    halka(A, 445, 210, 26, 100, 6, f1=.05, f2=.5, nm='halka-sonda')
    et(A, 6, 240, 80, 'Boğaza dokunmak: güvenilmez', 'uyari', .05, .55)
    akis(A, DIS, T(6, .1), T(7, 1), renk=ICERIK, w=3, nm='aspirat',
         o=K((0, 0), (T(6, .1), 0), (T(6, .15), 100), (T(7, 1), 100)))
    et(A, 6, 240, 80, 'Mide içeriği gelir: kullanılır', 'dogru', .55)
    et(A, 6, 600, 330, 'USG: kritik değil', 'bilgi', .7)
    # s7: sınavda dinleme; klinikte aspirat + akciğer grafisi
    halka(A, 440, 290, 150, 44, 7, nm='halka-sivi7')
    et(A, 7, 240, 80, 'Sınavda: dinleme yöntemi', 'dogru', .05)
    et(A, 7, 600, 330, 'Klinikte: aspirat + grafi', 'bilgi', .45)


# ———————————————————————— 4. Mide lavajı, ilaç verme ve ucu kapatma (ng-mide)

def a_lavaj(A):
    T = A.T
    m = Sahne2B('ng-mide')
    m.ekle(A)  # sondasız; sonda + ağız + torba aşağıda (kesintisiz)
    A.ekle('sonda', *kateter_cizgi(DIS, 4.4, NG))
    A.ekle('sonda-agiz', G(rc(680, 140, 16, 14, 2), fl(YESIL), st('#1f6b3e', 2)))
    # s0: suyla dolu enjektör ağza takılı; piston itildikçe mavi akış sonda boyunca mideye
    eo = K((0, 0), (T(0), 0), (T(0, .05), 100), (T(0, 1), 100), (T(1, .05), 0))
    _enjektor(A, 680, 150, eo, K((0, [0, 0, 0]), (T(0, .15), [0, 0, 0]), (T(0, .85), [0, -70, 0])), nm='enj', su=(T(0, .15), T(0, .85)))
    akis(A, DIS_TERS, T(0, .12), T(0, 1), renk=SU, w=3, nm='su-akis',
         o=K((0, 0), (T(0, .1), 0), (T(0, .15), 100), (T(0, .9), 100), (T(0, 1), 0)))
    A.ekle('su-film', G(el(440, 292, 230, 46), fl('#3d8ff0', o=55)), a=(440, 292), p=S([440, 292, 0]),
           s=K((0, [10, 10, 100]), (T(0, .3), [10, 10, 100]), (T(0, .9), [100, 100, 100]), (T(2, .1), [100, 100, 100]), (T(2, .9), [20, 20, 100])),
           o=K((0, 0), (T(0, .3), 0), (T(0, .35), 100), (T(2, .9), 100), (T(2, 1), 0)))
    et(A, 0, 560, 70, 'Lavaj: 300–500 mL su', 'bilgi', .1)
    et(A, 0, 250, 330, 'Föyde: 300 mL', 'bilgi', .5)
    # s1: torba aynı ağza takılır, mide hizasının altında asılır
    to = K((0, 0), (T(1, .1), 0), (T(1, .2), 100), (T(2, 1), 100), (T(3, .05), 0), (T(4), 0), (T(4, .08), 100))
    A.ekle('torba', *kateter_cizgi(TORBA_HORTUM, 4.4, NG),
           G(rc(748, 406, 86, 130, 10), fl('#f3f7fb'), st(NG[1], 2.2)),
           *[G(yol(f'M{772} {370 + i * 22} L{788} {370 + i * 22}'), st(NG[1], 1.4)) for i in range(4)],
           G(rc(748, 461, 80, 16, 6), fl(ICERIK, o=70)), o=to)
    A.ekle('hiza', G(yol('M300 330 L792 330'), st('#5b6676', 2, kesik=(8, 8))), o=belir(A, 1, .3, 1))
    et(A, 1, 560, 160, 'Torba mide hizasının altında', 'dogru', .25)
    # s2: sifonla sarı akış mideden sonda boyunca torbaya; torbada içerik yükselir
    AKIS = DIS + ' ' + TORBA_HORTUM.replace('M680 150', 'L680 150')
    akis(A, AKIS, T(2, .05), T(2, 1), renk=ICERIK, w=3, nm='akis1',
         o=K((0, 0), (T(2, .05), 0), (T(2, .1), 100), (T(2, .95), 100), (T(3), 0)))
    A.ekle('torba-dolum', G(rc(748, 418, 80, 70, 6), fl(ICERIK, o=55)), a=(748, 453), p=S([748, 453, 0]),
           s=K((0, [100, 0, 100]), (T(2, .1), [100, 0, 100]), (T(2, .95), [100, 100, 100])),
           o=K((0, 0), (T(2, .1), 0), (T(2, .15), 100), (T(2, 1), 100), (T(3, .05), 0), (T(4, .05), 0), (T(4, .1), 100)))
    halka(A, 440, 290, 150, 44, 2, nm='halka-sivi')
    et(A, 2, 560, 160, 'Sifon: içerik torbaya', 'dogru', .1)
    # s3: ilaç sonrası ağız tıpayla kapatılır (yoksa kıvrılır)
    A.ekle('tipa', G(rc(680, 154, 18, 12, 3), fl('#2f6fd6'), st('#1f4e79', 2)), G(yol('M689 154 C700 150 702 138 692 132'), st('#1f4e79', 2)),
           o=K((0, 0), (T(3, .15), 0), (T(3, .22), 100), (T(3, 1), 100), (T(4, .05), 0)))
    halka(A, 682, 148, 30, 26, 3, renk=YESIL, f1=.2, nm='halka-tipa')
    et(A, 3, 560, 90, 'İlaçtan sonra: tıpayla kapat', 'dogru', .2)
    et(A, 3, 560, 260, 'Tıpa yoksa ucu kıvır', 'bilgi', .55)
    # s4: boşaltma isteniyorsa kapatılmaz, torbaya bağlanır
    akis(A, AKIS, T(4, .1), T(4, 1), renk=ICERIK, w=3, nm='akis2', o=belir(A, 4, .1))
    et(A, 4, 560, 90, 'Boşaltma: torbaya bağla', 'dogru', .1)


# ———————————————————————— 5. İlerletme: damağa paralel düz, farinkste aşağı (ng-burun → ng-kesit → ng-burun)

def a_ilerletme(A):
    T = A.T
    b = Sahne2B('ng-burun')
    k = Sahne2B('ng-kesit')
    k1, k5 = T(1), T(5)
    ob = K((0, 100), (k1 - 8, 100), (k1, 0), (k5, 0), (k5 + 8, 100))
    ok_ = K((0, 0), (k1, 0), (k1 + 8, 100), (k5 - 8, 100), (k5, 0))
    # s0: burun deliği aşağı bakan hastada parmak burun ucunu hafifçe yukarı kaldırır
    b.ekle(A, o=ob)
    A.ekle('parmak', *b.katman('nr-parmak'), p=K((0, [0, 40, 0]), (T(0, .15), [0, 40, 0]), (T(0, .45), [0, 0, 0])),
           o=K((0, 0), (T(0, .1), 0), (T(0, .18), 100), (k1 - 8, 100), (k1, 0)))
    ok(A, b.cz('nr-ok-yukari')[0]['d'], 0, renk=MAVI, w=5, f1=.45, f2=.98, nm='ok-yukari')
    et(A, 0, 600, 200, 'Burun ucunu hafifçe kaldır', 'bilgi', .4)
    # s1–s4: kesit — sonda damağa paralel düz arkaya, kulak memesi hizasına dek, sonra farinkste aşağı
    k.ekle(A, o=ok_)
    _baglanti(A, K((0, 0), (k1, 0), (k1 + 8, 100), (k5 - 8, 100), (k5, 0)))
    d = _kesit_sonda_d(k)
    ilerleyen_kateter(A, d, [(T(1, .1), (152, 140)), (T(1, .9), (300, 128)), (T(2, .05), (300, 128)), (T(2, .8), (405, 119)),
                             (T(3, .1), (405, 119)), (T(3, .7), (520, 260))],
                      w=4.4, renk=NG, nm='sonda', o=K((0, 0), (k1, 0), (k1 + 8, 100), (T(4, .2), 100), (T(4, .28), 0)))
    ok(A, k.cz('nk-ok-duz')[0]['d'], 1, renk=YESIL, w=5, f1=.2, f2=.98, nm='ok-duz')
    A.ekle('ok-yukari-yanlis', G(yol('M200 120 L240 82'), st(KIRMIZI, 4, kesik=(8, 6))), o=belir(A, 1, .55, 1))
    carpi(A, 244, 78, 1, .6, r=14)
    et(A, 1, 600, 150, 'Sert damağa paralel, düz', 'dogru', .2)
    et(A, 1, 340, 40, 'Yukarı doğru değil', 'uyari', .6)
    A.ekle('hiza-kulak', G(yol('M405 50 L405 190'), st('#5b6676', 2, kesik=(8, 8))), o=belir(A, 2, .3, 2))
    et(A, 2, 560, 60, 'Kulak memesi hizasına dek', 'bilgi', .3)
    et(A, 2, 600, 180, 'Nazofarinks', 'etiket', .5)
    ok(A, k.cz('nk-ok-asagi')[0]['d'], 3, renk=YESIL, w=5, f1=.3, f2=.98, nm='ok-asagi')
    et(A, 3, 600, 230, 'Farinkste aşağı ilerlet', 'dogru', .3)
    # s4: dilini arkaya çeken hastada sonda dilin çevresinde kıvrılır → dilini dışarı çıkarmasını iste
    ilerleyen_kateter(A, k.cz('nk-dil-kivrim')[0]['d'], [(T(4, .2), (405, 119)), (T(4, .6), (276, 172))],
                      w=4.4, renk=NG_YANLIS, nm='sonda-kivrim', o=K((0, 0), (T(4, .2), 0), (T(4, .25), 100), (T(4, 1), 100), (k5 - 8, 0)))
    carpi(A, 330, 230, 4, .6, r=22)
    et(A, 4, 260, 50, 'Sonda dilde kıvrıldı', 'uyari', .45)
    et(A, 4, 600, 230, '"Dilinizi çıkarın"', 'bilgi', .7)
    # s5: septum deviasyonu — zorlamadan öbür burun deliği
    A.ekle('sapma', *b.katman('nr-sapma'), o=belir(A, 5, .1))
    carpi(A, 362, 308, 5, .3, r=18)
    halka(A, 437, 308, 34, 22, 5, renk=YESIL, f1=.5, nm='halka-sol')
    et(A, 5, 400, 120, 'Septum deviasyonu: zorlama', 'uyari', .1)
    et(A, 5, 600, 240, 'Öbür burun deliğini dene', 'dogru', .5)


# ———————————————————————— 6. Sabitleme: flasterle buruna (ng-burun)

def a_sabitleme(A):
    T = A.T
    b = Sahne2B('ng-burun')
    b.ekle(A)
    A.ekle('sonda', *b.katman('nr-sonda'))
    halka(A, 300, 380, 90, 70, 0, f1=.2, nm='halka-sonda')
    et(A, 0, 560, 120, 'Yer doğrulandı: sabitle', 'dogru', .1)
    et(A, 0, 560, 200, 'Kayarsa akciğere kaçabilir', 'uyari', .55)
    A.ekle('flaster', *b.katman('nr-flaster-burun'), p=K((0, [0, -40, 0]), (T(1, .2), [0, -40, 0]), (T(1, .5), [0, 0, 0])), o=belir(A, 1, .2))
    et(A, 1, 560, 120, 'İnce şerit flaster', 'dogru', .2)
    et(A, 1, 200, 120, 'Kalın parça gereksiz', 'bilgi', .6)
    A.ekle('sarim', *b.katman('nr-flaster-sarim'), o=belir(A, 2, .3))
    halka(A, 366, 318, 40, 40, 2, renk=YESIL, f1=.3, nm='halka-sarim')
    et(A, 2, 560, 120, 'Bir uç burna, öbürü sondaya', 'dogru', .3)
    halka(A, 437, 308, 34, 22, 3, renk=YESIL, f1=.1, nm='halka-sol')
    tik(A, 520, 300, 3, .4)
    et(A, 3, 560, 120, 'Öbür delik açık kalır', 'dogru', .1)
    A.ekle('ek-bant', *b.katman('nr-ek-bant'), o=belir(A, 4, .4))
    et(A, 4, 560, 120, 'Terli, yağlı cilt, ajite hasta', 'uyari', .05)
    et(A, 4, 200, 280, 'Ek ince bant', 'dogru', .45)


ADIMLAR = {
    'ng-yutkunma': a_yutkunma,
    'ng-oksuruk': a_oksuruk,
    'ng-yer-kontrol': a_yer_kontrol,
    'ng-lavaj': a_lavaj,
    'ng-ilerletme': a_ilerletme,
    'ng-sabitleme': a_sabitleme,
}
