#!/usr/bin/env python3
"""KMB adım videoları — dersin HER cümlesi bir animasyon bölümüdür (kullanıcı kuralı: metinde anlatılan her şey videoda).
  python3 meds/scripts/kmb/adim_lottie.py   → src/data/kmb/lottie/adim-<adım>.json + lottie/adimlar.json
Bölüm = adımın cümlesi; zamanlama adımın EMA klibinden (`o-<adım>`, ses_02.json). Sahne parçaları:
  · lottie_uret.py üreticileri alt kompozisyon olarak (ic_ekle + harita: üretici bölümü → cümle)
  · bu dosyadaki gerçekçi eylem parçaları (labia ayırma, avuçta kateter, uca jel, kavram sahneleri …)
Doğrulayıcı (dogrula.py) her adımda bölüm sayısı = cümle sayısı ve her cümlenin bir parçaya bağlı olduğunu denetler."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lottie_uret as LU  # noqa: E402
from lottie_dsl import FR, Anim, G, K, KD, S, el, fl, fl_cift, gf, ic_ekle, kisi, yatan_hasta, parmak_ucu, rc, st, tm, yol, yol_morph, yumruk  # noqa: E402

MEDS = Path(__file__).resolve().parents[2]
VERI = MEDS / 'src/data/kmb'
DERI, KEMIK, MESANE, IDRAR = LU.DERI, LU.KEMIK, LU.MESANE, LU.IDRAR
ELDIVEN = '#cfe0f5'
STERIL = '#f3e5cf'


def zemin_kat(A, b1, b2, nm='zemin'):
    """Bölüm aralığında görünen tam zemin (yeni parça öncekini örtsün)."""
    A.ekle(nm, G(rc(400, 250, 800, 500), gf(LU.ZEMIN, (400, 150), (400, 650), radyal=True)), o=gorun(A, b1, b2))
    A.kamera(b1, 400, 250, 100, sure=0.3)  # kendi sahnemiz: kamera sıfırlanır


def gorun(A, b1, b2, f=8):
    return K((0, 0), (max(1, A.T(b1) - f), 0), (A.T(b1), 100), (A.T(b2, 1) + f, 100), (A.T(b2, 1) + 2 * f, 0))


def belir(A, b, fr=0.0, son=None):
    """b. cümlenin fr kesirinde belirir; son verilirse o cümlenin sonunda kaybolur."""
    t = A.T(b, fr)
    ks = [(0, 0), (max(1, t - 6), 0), (t + 6, 100)]
    if son is not None:
        ks += [(A.T(son, 1) + 4, 100), (A.T(son, 1) + 12, 0)]
    return K(*ks)


def carpi(A, x, y, b, fr=0.3, r=36):
    A.ekle('carpi', G(yol(f'M{x - r} {y - r} L{x + r} {y + r} M{x + r} {y - r} L{x - r} {y + r}'), st('#d23b3b', 11)), o=belir(A, b, fr, b))


def tik(A, x, y, b, fr=0.3, son=None):
    A.ekle('tik', G(yol(f'M{x - 26} {y} L{x - 6} {y + 22} L{x + 30} {y - 24}'), st('#2e9e5b', 12)), o=belir(A, b, fr, son if son is not None else b))


# ———————————————————————— gerçekçi eylem parçaları

VULVA_DIS = LU.VULVA_DIS
MINUS_SOL_KAPALI = 'M400 112 C356 118 330 200 336 300 C340 360 366 400 392 404 C380 380 384 330 388 280 C392 210 394 150 400 130 Z'
MINUS_SOL_ACIK = 'M400 112 C320 116 272 200 276 300 C278 362 306 410 360 418 C330 384 320 330 326 280 C334 206 356 150 400 130 Z'


def ayna(d):
    import re
    out, sayilar = [], re.findall(r'[MLCZ]|-?\d*\.?\d+', d)
    k = 0
    for s in sayilar:
        if s in 'MLCZ':
            out.append(s); k = 0
        else:
            out.append(str(round(800 - float(s), 2)) if k % 2 == 0 else s); k += 1
    return ' '.join(out)


def vulva(A, b1, b2, ayir=None, parmak=None):
    """Önden kadın dış genitalyası; ayir=(k1, k2) labia minuslar şekil değiştirerek ayrılır; parmak=(k1, k2) sol elin
    eldivenli işaret ve orta parmağı V biçiminde labiaların iç yüzüne oturur ve ayırır (labia parmakla birlikte açılır)."""
    o = gorun(A, b1, b2)
    A.kamera(b1, 400, 250, 100, sure=0.3)
    A.ekle('uyluk', G(yol('M0 60 C120 70 220 150 260 300 C280 380 270 460 250 500 L0 500 Z'), gf(DERI, (100, 200), (250, 450))),
           G(yol('M800 60 C680 70 580 150 540 300 C520 380 530 460 550 500 L800 500 Z'), gf(DERI, (700, 200), (550, 450))), o=o)
    A.ekle('mons', G(yol('M260 20 C320 0 480 0 540 20 C560 50 540 80 520 90 L280 90 C260 80 240 50 260 20 Z'), gf(DERI, (400, 10), (400, 90))),
           *[G(yol(f'M{280 + i * 18} {30 + (i % 3) * 14} C{284 + i * 18} {22 + (i % 3) * 14} {290 + i * 18} {20 + (i % 3) * 14} {294 + i * 18} {24 + (i % 3) * 14}'), st('#6b4a33', 1.2, o=50)) for i in range(14)], o=o)
    A.ekle('majus', G(yol(VULVA_DIS), gf(DERI, (400, 150), (400, 460), radyal=True), st('#b9805a', 2)),
           G(yol('M320 110 C290 170 288 290 318 380'), st('#c28a66', 3, o=50)), G(yol('M480 110 C510 170 512 290 482 380'), st('#c28a66', 3, o=50)), o=o)
    A.ekle('vestibul', G(yol('M400 112 C340 120 314 220 326 320 C332 370 366 406 400 408 C434 406 468 370 474 320 C486 220 460 120 400 112 Z'),
                         gf([(0, '#f2a9a6'), (1, '#c86e6c')], (400, 220), (400, 400), radyal=True)), o=o)
    A.ekle('klitoris', G(yol('M372 128 C380 112 420 112 428 128 C420 140 380 140 372 128 Z'), fl('#d49a8e'), st('#a8705f', 1.2)),
           G(el(400, 142, 16, 18), gf([(0, '#f2b4ae'), (1, '#c97c77')], (396, 136), (404, 150), radyal=True)), o=o)
    A.ekle('meatus', G(el(400, 208, 22, 16), fl('#e8a7a2')), G(yol('M400 201 C396 204 396 212 400 215 C404 212 404 204 400 201 Z'), fl('#6e2420')), o=o)
    A.ekle('vajina', G(yol('M400 252 C374 256 368 300 372 330 C376 356 390 370 400 370 C410 370 424 356 428 330 C432 300 426 256 400 252 Z'), fl('#8f3c3a'), st('#c9827c', 5)),
           *[G(el(x, y, 7, 7), fl('#d9928c')) for x, y in [(376, 300), (424, 300), (384, 350), (416, 350)]], o=o)
    k1, k2 = ayir if ayir else (A.op + 10, A.op + 20)
    sol = yol_morph(MINUS_SOL_KAPALI, MINUS_SOL_ACIK, k1, k2)
    sag = yol_morph(ayna(MINUS_SOL_KAPALI), ayna(MINUS_SOL_ACIK), k1, k2)
    A.ekle('minus', G(sol, fl('#d9928c'), st('#a85f5a', 1.8)), G(sag, fl('#d9928c'), st('#a85f5a', 1.8)), o=o)
    A.ekle('anus', G(el(400, 470, 24, 24), fl('#9a5f48')), o=o)
    if parmak:
        p1, p2 = parmak
        # sol el yukarıdan gelir: eldivenli işaret (solda) ve orta parmak (sağda) V açar; uçlar labia minusların iç yüzüne,
        # meatus hizasına oturur ve labialar açılırken onlarla birlikte yanlara kayar
        import math

        def parmak_yolu(kx, ky, ux, uy, w):
            dx, dy = ux - kx, uy - ky
            L = math.hypot(dx, dy); nx, ny = -dy / L * w / 2, dx / L * w / 2
            ex, ey = dx / L * w * .55, dy / L * w * .55
            return (f'M{kx + nx:.1f} {ky + ny:.1f} L{ux + nx * .8:.1f} {uy + ny * .8:.1f} C{ux + nx * .8 + ex:.1f} {uy + ny * .8 + ey:.1f} '
                    f'{ux - nx * .8 + ex:.1f} {uy - ny * .8 + ey:.1f} {ux - nx * .8:.1f} {uy - ny * .8:.1f} L{kx - nx:.1f} {ky - ny:.1f} Z')
        for kx, ux0, ux1, nm in ((250, 372, 330, 'isaret'), (550, 428, 470, 'orta')):
            d1, d2 = parmak_yolu(kx, -30, ux0, 214, 40), parmak_yolu(kx, -30, ux1, 222, 40)
            A.ekle(f'parmak-{nm}', G(yol_morph(d1, d2, p1, p2), gf([(0, '#fdf6ea'), (1, '#e7d3b3')], (kx, 0), (ux0, 214)), st('#b59c72', 2)),
                   G(yol_morph(f'M{(kx + ux0) / 2 - 10} 100 C{(kx + ux0) / 2 - 4} 106 {(kx + ux0) / 2 + 4} 106 {(kx + ux0) / 2 + 10} 100',
                               f'M{(kx + ux1) / 2 - 10} 104 C{(kx + ux1) / 2 - 4} 110 {(kx + ux1) / 2 + 4} 110 {(kx + ux1) / 2 + 10} 104', p1, p2), st('#b59c72', 1.4)),
                   p=K((0, [0, -300, 0]), (p1 - 16, [0, -300, 0]), (p1, [0, 0, 0])), o=K((0, 0), (p1 - 16, 0), (p1 - 10, 100), (A.T(b2, 1) + 8, 100), (A.T(b2, 1) + 16, 0)))
        A.ekle('el-sirti', G(yol('M200 -120 L600 -120 L580 -20 C520 0 280 0 220 -20 Z'), gf([(0, '#fdf6ea'), (1, '#e7d3b3')], (400, -120), (400, 0)), st('#b59c72', 1.5)),
               p=K((0, [0, -300, 0]), (p1 - 16, [0, -300, 0]), (p1, [0, 0, 0])), o=K((0, 0), (p1 - 16, 0), (p1 - 10, 100), (A.T(b2, 1) + 8, 100), (A.T(b2, 1) + 16, 0)))
        A.ekle('meatus-acik', G(el(400, 208, 40, 32), st('#2e9e5b', 3, kesik=(5, 4))), o=K((0, 0), (p2, 0), (p2 + 8, 100), (A.T(b2, 1) + 8, 100), (A.T(b2, 1) + 16, 0)))


def avuc_kateter(A, b, renk='#e3b544', kenar='#8a6a1e', steril=True, gevsek=False):
    """Eldivenli sağ avucun üstten görünümü: kateter avuca halka halinde yerleşir (kırpma ile sarılır), parmaklar kıvrılıp
    halkaların üstüne kapanır; yalnız uç baş ve işaret parmağı arasından birkaç santim dışarıda kalır. gevsek=True: yanlış
    tutuş — kateter uçtan tutulur, gövde sallanır."""
    T = A.T
    ren = STERIL if steril else ELDIVEN
    zemin_kat(A, b, b, 'zemin-avuc')
    A.ekle('ortu', G(rc(400, 420, 800, 180), fl('#3b7bb8', o=75)), o=gorun(A, b, b))
    if gevsek:
        A.ekle('el', G(yol('M500 120 C540 100 600 110 620 150 C640 190 610 230 570 236 C530 240 500 210 490 180 Z'), fl(ren), st('#b59c72', 2)), o=gorun(A, b, b))
        A.ekle('sarkan', G(yol_morph('M500 170 C440 220 380 300 330 420', 'M500 170 C420 200 330 260 250 330', T(b, .2), T(b, .6)), st(kenar, 10)),
               G(yol_morph('M500 170 C440 220 380 300 330 420', 'M500 170 C420 200 330 260 250 330', T(b, .2), T(b, .6)), st(renk, 7)), o=gorun(A, b, b))
        A.ekle('dokunma', G(el(250, 330, 60, 60), st('#d23b3b', 5)), o=belir(A, b, .6, b))
        return
    # bilek + eldiven manşeti
    A.ekle('bilek', G(yol('M330 500 L330 380 C330 360 470 360 470 380 L470 500 Z'), fl(ren), st('#b59c72', 2)),
           G(yol('M326 430 C360 440 440 440 474 430'), st('#b59c72', 2, o=80)), o=gorun(A, b, b))
    # avuç içi: tenar (başparmak kökü) ve hipotenar kabarıklıkları, avuç çizgileri
    A.ekle('avuc', G(yol('M300 160 C296 120 330 104 400 104 C470 104 506 120 502 168 C512 230 506 300 470 350 C440 382 360 382 330 350 C300 316 292 230 300 160 Z'),
                     gf([(0, '#fdf6ea'), (1, '#ead7b8')], (400, 150), (400, 380), radyal=True), st('#b59c72', 2.5)),
           G(yol('M440 340 C480 320 500 280 500 240 C470 260 446 300 440 340 Z'), fl('#ecdcc0', o=80)),
           G(yol('M320 200 C360 220 420 226 486 206'), st('#c9b08a', 1.8, o=70)), G(yol('M330 260 C380 280 440 280 490 256'), st('#c9b08a', 1.8, o=70)),
           G(yol('M360 330 C380 300 410 270 430 200'), st('#c9b08a', 1.6, o=60)), o=gorun(A, b, b))
    # kateter halkaları avuçta: dıştan içe üç tur, sonra uç
    halka = 'M412 140 C480 140 494 214 470 262 C446 310 360 314 336 262 C312 212 346 170 404 170 C456 172 466 228 446 252 C424 278 372 276 360 246 C350 220 372 202 404 204 C432 206 438 232 424 244'
    e = K((0, 0), (T(b, .05), 0), (T(b, .5), 100))
    A.ekle('kateter-golge', G(yol(halka), st(kenar, 11, o=45), tm(e)), o=gorun(A, b, b))
    A.ekle('kateter', G(yol(halka), st(renk, 8), tm(e)), G(yol(halka), st('#ffffff', 2, o=60), tm(e), p=(0, -2)), o=gorun(A, b, b))
    # dışarıda kalan uç: başparmak ile işaret parmağı arasından birkaç santim
    A.ekle('uc', G(yol('M412 140 C450 118 520 96 590 82'), st(kenar, 11, o=45)), G(yol('M412 140 C450 118 520 96 590 82'), st(renk, 8)),
           G(el(592, 82, 12, 12), fl(renk), st(kenar, 1.2)), G(el(594, 81, 4, 4), fl('#2e3540')), o=belir(A, b, .45, b))
    # parmaklar (serçe → işaret): yelpaze açık, sivri, yuvarlak uçlu; kıvrılınca kısalır, halkaların üstüne kapanır
    def parmak(x0, x1, uz, gen, kv):
        """x0 kök orta, x1 uç orta (açık), uz uzunluk, gen genişlik, kv kıvrık boy"""
        w, u = gen / 2, gen * .4
        acik = f'M{x0 - w} 150 C{x0 - w} 110 {x1 - u} {150 - uz + 30} {x1 - u} {150 - uz + 12} C{x1 - u} {150 - uz - 6} {x1 + u} {150 - uz - 6} {x1 + u} {150 - uz + 12} C{x1 + u} {150 - uz + 30} {x0 + w} 110 {x0 + w} 150 Z'
        kiv = f'M{x0 - w} 150 C{x0 - w} 170 {x0 - u} {150 + kv - 18} {x0 - u} {150 + kv} C{x0 - u} {150 + kv + 18} {x0 + u} {150 + kv + 18} {x0 + u} {150 + kv} C{x0 + u} {150 + kv - 18} {x0 + w} 170 {x0 + w} 150 Z'
        return acik, kiv
    for i, (x0, x1, uz, gen, kv) in enumerate([(322, 290, 110, 34, 60), (360, 346, 150, 38, 84), (404, 404, 162, 40, 92), (448, 462, 146, 38, 84)]):
        d1, d2 = parmak(x0, x1, uz, gen, kv)
        A.ekle(f'parmak{i}', G(yol_morph(d1, d2, T(b, .55), T(b, .8)), gf([(0, '#fdf6ea'), (1, '#e7d3b3')], (x0 - 20, 60), (x0 + 20, 200)), st('#b59c72', 2)), o=gorun(A, b, b))
        A.ekle(f'bogum{i}', G(yol(f'M{x0 - 12} {150 + kv * .45} C{x0 - 4} {150 + kv * .5} {x0 + 4} {150 + kv * .5} {x0 + 12} {150 + kv * .45}'), st('#b59c72', 1.6)),
               G(yol(f'M{x0 - 10} {150 + kv * .8} C{x0 - 3} {150 + kv * .85} {x0 + 3} {150 + kv * .85} {x0 + 10} {150 + kv * .8}'), st('#b59c72', 1.4)), o=belir(A, b, .8, b))
    # başparmak: yandan gelir, kıvrılınca halkaların dış kenarını bastırır
    A.ekle('basparmak', G(yol_morph('M500 250 C540 240 590 210 630 176 C646 164 664 182 652 198 C620 236 570 280 506 300 Z',
                                    'M500 250 C520 236 540 214 552 192 C560 178 580 188 574 204 C562 240 536 276 506 300 Z', T(b, .55), T(b, .8)),
                          gf([(0, '#fdf6ea'), (1, '#e7d3b3')], (520, 200), (600, 280)), st('#b59c72', 2)), o=gorun(A, b, b))


def jel_ucuna(A, b, ml='~2 mL'):
    """Kadında kateter ucuna jel: tüp sıkılır, jel damlası uca düşer ve uç boyunca yayılır."""
    T = A.T
    zemin_kat(A, b, b, 'zemin-jel')
    A.ekle('ortu', G(rc(400, 400, 800, 200), fl('#3b7bb8', o=70)), o=gorun(A, b, b))
    A.ekle('kateter', G(yol('M60 330 L600 330'), st('#8a6a1e', 22, o=45)), G(yol('M60 330 L600 330'), st('#e3b544', 18)), G(yol('M60 324 L600 324'), st('#fff6d6', 4)),
           G(yol('M600 320 C626 320 634 326 634 330 C634 334 626 340 600 340 Z'), fl('#e3b544'), st('#8a6a1e', 1.5)), G(el(592, 326, 12, 7), fl('#4a3510')),
           G(rc(520, 330, 70, 24, 10), fl('#e8c25c'), st('#8a6a1e', 1.2)), o=gorun(A, b, b))
    A.ekle('tup', G(yol('M640 110 L760 70 L780 130 L668 178 Z'), fl('#eef3f8'), st('#6b7a90', 2)), G(yol('M640 110 L668 178 L620 210 L606 200 Z'), fl('#dfe6ee'), st('#6b7a90', 1.5)),
           G(yol('M700 110 L746 94'), st('#2f6fd6', 6)),
           s=K((0, [100, 100, 100]), (T(b, .1), [100, 100, 100]), (T(b, .35), [100, 82, 100])), a=(700, 80), p=S([700, 172, 0]), o=gorun(A, b, b))
    A.ekle('damla', G(el(0, 0, 26, 30), fl('#cfe9ff', o=90), st('#8fb8e6', 1.5)), G(el(-5, -6, 7, 5), fl('#ffffff')),
           p=K((0, [612, 300, 0]), (T(b, .3), [612, 300, 0]), (T(b, .5), [606, 318, 0])), s=K((0, [20, 20, 100]), (T(b, .15), [20, 20, 100]), (T(b, .3), [100, 100, 100])),
           o=K((0, 0), (T(b, .15), 0), (T(b, .2), 100), (T(b, .55), 100), (T(b, .6), 0)))
    A.ekle('jel-yayilma', G(el(0, 0, 90, 30), fl('#cfe9ff', o=80)), G(el(-10, -6, 40, 8), fl('#ffffff', o=90)),
           p=S([590, 326, 0]), s=K((0, [10, 40, 100]), (T(b, .55), [10, 40, 100]), (T(b, .8), [100, 100, 100])), o=belir(A, b, .55, b))
    A.etiket(b, b, 560, 260, f'Uca {ml} jel', 'bilgi')


def kavram_ikonlar(A, b, ogeler, nm='kavram'):
    """Kavram sahnesi: ikonlar sırayla belirir. ogeler: [(x, y, şekiller, etiket, tür)]"""
    zemin_kat(A, b, b, f'zemin-{nm}')
    n = len(ogeler)
    for i, (x, y, sh, et, tur) in enumerate(ogeler):
        f = 0.08 + 0.75 * i / max(1, n)
        A.ekle(f'{nm}{i}', *sh, o=belir(A, b, f, b), s=K((0, [70, 70, 100]), (A.T(b, f), [70, 70, 100]), (A.T(b, f) + 10, [100, 100, 100])), a=(x, y), p=S([x, y, 0]))
        if et:
            dy = 95 + (28 if n >= 4 and i % 2 else 0)  # dörtlü sırada etiketler iki satıra dağılır, çakışmaz
            A.etiketler.append({'bas': round(A.T(b, f) / FR, 2), 'son': round(A.T(b, 1) / FR, 2), 'x': x, 'y': y + dy, 'metin': et, 'tur': tur})


def ikon_kutu(x, y, renk, ic):
    return [G(rc(x, y, 150, 130, 22), fl('#ffffff'), st(renk, 3)), *ic]


# ———————————————————————— adımlar

def adim(ad, cumleler, zaman):
    return Anim(f'adim-{ad}', ad, [{'baslik': ' '.join(c.split()[:4]).rstrip(',;:'), 'metin': c, 'sure': max(3, len(c) / 14)} for i, c in enumerate(cumleler)], zaman, bekle=0.9)


def et(A, b, x, y, metin, tur='bilgi', f1=0.0, f2=1.0):
    A.etiketler.append({'bas': round(A.T(b, f1) / FR, 2), 'son': round(A.T(b, f2) / FR, 2), 'x': x, 'y': y, 'metin': metin, 'tur': tur})


def panel(A, b, f1, f2, x, y, w, h, nm, *shapes, kenar='#2f6fd6'):
    """Ana sahnenin üstünde iç pencere (cümlenin bir kısmını göstermek için)."""
    A.ekle(nm, G(rc(x, y, w, h, 14), fl('#f7f9fb'), st(kenar, 3)), *shapes,
           o=K((0, 0), (A.T(b, f1), 0), (A.T(b, f1) + 8, 100), (A.T(b, f2), 100), (A.T(b, f2) + 8, 0)))


def damla(x, y, s=1.0, renk='#e1b300'):
    return G(yol(f'M{x} {y - 14 * s} C{x - 4 * s} {y - 6 * s} {x - 9 * s} {y} {x - 9 * s} {y + 5 * s} C{x - 9 * s} {y + 11 * s} {x - 4 * s} {y + 14 * s} {x} {y + 14 * s} C{x + 4 * s} {y + 14 * s} {x + 9 * s} {y + 11 * s} {x + 9 * s} {y + 5 * s} C{x + 9 * s} {y} {x + 4 * s} {y - 6 * s} {x} {y - 14 * s} Z'), fl(renk))


def a_giris(A):
    ic_ekle(A, LU.erkek_ilerleyis, [0] * 8, [(0, 0)])
    A.kamera_sabit(0, 0, 420, 250, 100)
    et(A, 0, 400, 440, 'Üretral kateter: meatustan mesaneye, idrarı dışarı alır', 'dogru', .3)
    kavram_ikonlar(A, 1, [(180, 180, kisi(180, 140, '#ffffff', 1, True), 'Hekim', 'bilgi'), (400, 180, kisi(400, 140, '#8fc1c9'), 'Hemşire', 'bilgi'),
                          (620, 180, kisi(620, 140, '#a3b9d9'), 'Sağlık çalışanı', 'bilgi')], 'ekip')
    et(A, 1, 400, 420, 'Teknik kolay: birkaç küçük incelik', 'bilgi', .5)
    kavram_ikonlar(A, 2, [(220, 200, ikon_kutu(220, 200, '#2e9e5b', [G(yol('M190 200 L212 222 L252 178'), st('#2e9e5b', 12))]), 'Kime takılır?', 'dogru'),
                          (400, 200, ikon_kutu(400, 200, '#d23b3b', [G(yol('M372 172 L428 228 M428 172 L372 228'), st('#d23b3b', 12))]), 'Kime asla?', 'uyari'),
                          (580, 200, ikon_kutu(580, 200, '#2f6fd6', [G(el(580, 200, 70, 70), st('#2f6fd6', 6)), G(yol('M580 200 L580 172'), st('#2f6fd6', 6))]), 'Hangi endikasyon?', 'bilgi')], 'karar')
    yolh = [(130, 'Endikasyon'), (300, 'Kontrendikasyon'), (470, 'Malzeme'), (640, 'Kadında / erkekte uygulama')]
    A.ekle('yol-ok', G(yol('M130 220 L640 220'), st('#2f6fd6', 4, kesik=(10, 8)), tm(K((0, 0), (A.T(3, .1), 0), (A.T(3, .9), 100)))), o=gorun(A, 3, 3))
    kavram_ikonlar(A, 3, [(x, 220, ikon_kutu(x, 220, '#2f6fd6', [G(el(x, 220, 54, 54), fl('#2f6fd6'))]), f'{i + 1} · {m}', 'bilgi') for i, (x, m) in enumerate(yolh)], 'yol')


def monitor(A, b1, b2):
    o = gorun(A, b1, b2)
    A.ekle('monitor', G(rc(250, 330, 80, 30, 4), fl('#5b6676')), G(rc(250, 190, 360, 240, 16), fl('#11161d'), st('#5b6676', 4)),
           G(yol('M90 150 L150 150 L162 110 L176 190 L190 130 L200 150 L260 150 L272 110 L286 190 L300 130 L310 150 L400 150'), st('#3ad17a', 3, kesik=(18, 8), kesik_kayma=KD((0, 0), (A.op, -A.op * 3)))),
           G(yol('M90 230 C120 210 150 250 180 230 C210 210 240 250 270 230 C300 210 330 250 360 230'), st('#5ab6ff', 3, kesik=(14, 6), kesik_kayma=KD((0, 0), (A.op, -A.op * 2)))), o=o)
    A.ekle('torba', G(rc(640, 260, 150, 220, 14), fl('#f4f7fa', o=90), st('#9aa6b4', 3)), G(rc(640, 330, 134, 80, 10), gf([(0, '#f8dd6c'), (1, '#e7b82e')], (640, 290), (640, 370))),
           *[G(yol(f'M690 {180 + i * 30} L712 {180 + i * 30}'), st('#5b6676', 2)) for i in range(6)], o=o)


def a_takip(A):
    T = A.T
    zemin_kat(A, 0, 4)
    monitor(A, 0, 0)
    for i, (x, y, m) in enumerate([(130, 100, 'TA 120/80'), (250, 100, 'Nabız 84'), (370, 100, 'SS 16'), (170, 280, 'SpO₂ %98'), (330, 280, 'Ateş 36,8 °C')]):
        et(A, 0, x, y, m, 'bilgi', .05 + i * .08)
    et(A, 0, 640, 410, 'Saatlik / 24 saatlik idrar: vital bulgu kadar önemli', 'dogru', .5)
    # s1: yatakta, ağızdan beslenemeyen hasta: serum kola, kateter torbaya
    o1 = gorun(A, 1, 1)
    A.ekle('hasta', *yatan_hasta(180, 300, 1.0, torba=True), o=o1)
    A.ekle('serum', G(yol('M120 40 L120 320'), st('#9aa6b4', 5)), G(rc(120, 90, 70, 100, 12), fl('#e9f3fb', o=95), st('#6b7a90', 2)), G(rc(120, 110, 58, 60, 8), fl('#9fc4ef')),
           G(yol('M120 140 L120 170 C120 230 260 250 392 290'), st('#cfd8e2', 5)), G(el(120, 160, 10, 14), fl('#5b8fc9')), o=o1)
    A.ekle('serum-damla', damla(120, 150, .5, '#5b8fc9'), p=KD(*[(T(1) + k * 12, [0, (k % 2) * 12, 0]) for k in range(max(1, int((T(1, 1) - T(1)) / 12)))]), o=o1)
    et(A, 1, 140, 30, 'Ağızdan alamıyor: giren sıvı', 'bilgi'); et(A, 1, 560, 470, 'Çıkan idrar → ne kadar sıvı?', 'dogru', .4)
    # s2–s3: kavanozlar + organlar
    zemin_kat(A, 2, 3, 'zemin-denge')
    for b, cik, gir, organ in ((2, 2000, 1000, 'bobrek'), (3, 1000, 5000, 'akciger')):
        o = gorun(A, b, b)
        for x, v, nm, r in ((180, cik, 'Çıkan', '#e7b82e'), (360, gir, 'Giren', '#5b8fc9')):
            h = v / 5000 * 260
            A.ekle(f'kavanoz{b}{nm}', G(rc(x, 270, 120, 280, 12), fl('#f4f7fa'), st('#9aa6b4', 3)), o=o)
            A.ekle(f'sivi{b}{nm}', G(rc(x, 0, 104, h, 6), fl(r)), p=K((0, [0, 404, 0]), (T(b, .1), [0, 404, 0]), (T(b, .5), [0, 404 - h / 2, 0])),
                   s=K((0, [100, 1, 100]), (T(b, .1), [100, 1, 100]), (T(b, .5), [100, 100, 100])), o=o)
            et(A, b, x, 110, f'{nm} {v} mL', 'bilgi', .5)
        if organ == 'bobrek':
            for x in (560, 680):
                d = f'M{x} 180 C{x - 60} 180 {x - 60} 340 {x} 340 C{x + 40} 340 {x + 50} 300 {x + 20} 260 C{x + 50} 220 {x + 40} 180 {x} 180 Z'
                A.ekle(f'bobrek{x}', G(yol(d), gf([(0, '#c9605a'), (1, '#8f3c3a')], (x - 30, 190), (x + 20, 330)), st('#7d2f2a', 2)), o=o)
                A.ekle(f'bobrek-k{x}', G(yol(d), fl('#4a1715')), o=K((0, 0), (T(b, .55), 0), (T(b, .85), 70), (T(b, 1) + 8, 70), (T(b, 1) + 16, 0)))
            A.ekle('kuru', damla(620, 120, 1.6, '#5b8fc9'), G(yol('M600 100 L640 140 M640 100 L600 140'), st('#d23b3b', 6)), o=belir(A, 2, .55, 2))
            et(A, 2, 620, 380, 'Dehidratasyon · böbrek fonksiyonu bozulur', 'uyari', .55)
        else:
            for x, sag in ((560, False), (680, True)):
                d = (f'M{x} 160 C{x + 50} 170 {x + 60} 300 {x + 40} 350 C{x + 10} 360 {x - 20} 350 {x - 24} 330 L{x - 24} 170 Z' if sag else
                     f'M{x} 160 C{x - 50} 170 {x - 60} 300 {x - 40} 350 C{x - 10} 360 {x + 20} 350 {x + 24} 330 L{x + 24} 170 Z')
                A.ekle(f'akc{x}', G(yol(d), fl('#f2b8b2'), st('#a8554e', 2)), o=o)
                A.ekle(f'odem{x}', G(yol(d), fl('#5b8fc9', o=75)), a=(x, 356), p=S([x, 356, 0]),
                       s=K((0, [100, 0, 100]), (T(b, .5), [100, 0, 100]), (T(b, .9), [100, 60, 100])), o=o)
            A.ekle('kalp', G(yol('M620 300 C600 280 590 300 606 318 L620 334 L634 318 C650 300 640 280 620 300 Z'), fl('#c0392b')), o=belir(A, 3, .7, 3))
            A.ekle('bacak', G(yol('M720 400 L716 470 L740 470 L742 400 Z'), fl('#e9b896'), st('#b9805a', 1.5)), G(yol('M760 400 L752 470 L792 470 L786 400 Z'), fl('#e9b896'), st('#d23b3b', 2)),
                   o=belir(A, 3, .8, 3))
            et(A, 3, 560, 440, 'Akciğer ödemi · periferik ödem · KKY', 'uyari', .6)
    kavram_ikonlar(A, 4, [(110, 190, ikon_kutu(110, 190, '#2f6fd6', [G(rc(110, 205, 110, 30, 8), fl('#9aa6b4')), G(el(80, 185, 28, 28), fl('#e9b896')), G(rc(150, 230, 18, 24, 4), fl('#f2cf55'))]), 'Yoğun bakım', 'bilgi'),
                          (300, 190, ikon_kutu(300, 190, '#2f6fd6', [G(yol('M262 222 L320 166 L332 176 L276 232 Z'), fl('#c9d3de'), st('#6b7a90', 2)), damla(318, 212, 1.1, '#c0392b')]), 'Uzun / kanamalı ameliyat', 'bilgi'),
                          (490, 190, ikon_kutu(490, 190, '#d23b3b', [G(yol('M450 160 L490 210 L530 240'), st('#d23b3b', 7)), G(yol('M516 232 L532 242 L522 224'), st('#d23b3b', 6))]), 'Şok (septik · hipovolemik · hemorajik)', 'uyari'),
                          (680, 190, ikon_kutu(680, 190, '#2f6fd6', [G(el(680, 190, 64, 64), gf(DERI, (670, 180), (690, 205), radyal=True)), G(yol('M660 186 C666 192 674 192 680 186 M680 186 C686 192 694 192 700 186'), st('#3b2a1e', 3))]), 'Bilinci kapalı (inme, DKA)', 'bilgi')], 'grup')


def bosalma(_z):
    """Retansiyonda kateter: üretradan mesaneye girer, idrar torbaya akar, mesane küçülür."""
    I = LU._IC
    T = I.T
    LU.pelvis_zemin(I)
    LU.simfiz(I, 420, 300, -18)
    I.ekle('uretra', G(yol('M330 268 C340 300 352 330 360 360 L368 440'), st('#d68c86', 9)))
    I.ekle('mesane', G(el(0, 0, 190, 220), gf(MESANE, (-40, -60), (40, 70), radyal=True), st('#a8554e', 5)), G(el(0, 0, 166, 196), gf(IDRAR, (-30, -40), (30, 60), radyal=True)),
           a=(0, 90), p=K((0, [340, 270, 0]), (T(0, .4), [340, 270, 0]), (T(0, 1), [334, 276, 0])), s=K((0, [100, 100, 100]), (T(0, .4), [100, 100, 100]), (T(0, 1), [62, 52, 100])))
    kd = 'M380 520 L368 440 L360 360 C352 330 340 300 330 268 L326 240'
    I.ekle('kateter', G(yol(kd), st('#8a96a6', 9)), G(yol(kd), st('#eef2f6', 7)), G(el(326, 240, 9, 9), fl('#eef2f6'), st('#5b6676', 1)), tm(K((0, 0), (T(0, .05), 0), (T(0, .35), 100))))
    I.ekle('akis', G(yol('M326 240 C330 268 340 300 352 330 L368 440 L380 520'), st('#e1b300', 4, kesik=(8, 10), kesik_kayma=KD((T(0, .35), 0), (I.ust.op, -(I.ust.op - T(0, .35)) * 3)))),
           o=K((0, 0), (T(0, .35), 0), (T(0, .4), 100)))
    I.ekle('torba', G(rc(620, 420, 140, 130, 12), fl('#f4f7fa', o=92), st('#9aa6b4', 2)), G(yol('M380 520 C420 520 520 470 560 440'), st('#cfd8e2', 6)))
    I.ekle('torba-dolu', G(rc(620, 0, 124, 110, 8), fl('#f2cf55')), a=(0, 55), p=S([0, 480, 0]),
           s=K((0, [100, 5, 100]), (T(0, .4), [100, 5, 100]), (T(0, 1), [100, 90, 100])))


def a_retansiyon(A):
    ic_ekle(A, LU.glob, [0, 1, None, None, None], [(0, 1)])
    et(A, 0, 600, 420, 'Hasta idrar yapamıyor', 'uyari', .2)
    ic_ekle(A, bosalma, [2], [(2, 2)], 'bosalma')
    A.kamera_sabit(2, 2, 420, 300, 100)
    et(A, 2, 250, 440, 'Mesane boşalır, hasta rahatlar', 'dogru', .6)
    zemin_kat(A, 3, 3, 'zemin-yatak')
    A.ekle('yatak-hasta', *yatan_hasta(40, 200, .8, torba=True), o=belir(A, 3, .05, 3))
    A.ekle('travma-hasta', *yatan_hasta(430, 200, .8, battaniye='#c9a8a3', torba=True), G(yol('M560 150 L600 150 M580 130 L580 170'), st('#d23b3b', 8)), o=belir(A, 3, .45, 3))
    et(A, 3, 210, 330, 'Kendi başına tuvalete gidemeyen, yatağa bağımlı', 'bilgi', .1); et(A, 3, 600, 330, 'Hareket ettirilemeyen travma hastası', 'uyari', .5)


def a_diger(A):
    T = A.T
    zemin_kat(A, 0, 2)
    A.ekle('rontgen', G(rc(330, 250, 440, 340, 12), fl('#1a1f26')), G(yol('M180 140 C220 100 300 100 330 140 M480 140 C440 100 360 100 330 140'), st('#e9eef5', 4, o=60)),
           G(yol('M200 320 C240 300 300 300 330 330 C360 300 420 300 460 320'), st('#e9eef5', 6, o=70)), o=gorun(A, 2, 2))
    A.ekle('mesane', G(el(320, 230, 260, 200), gf(MESANE, (280, 180), (340, 300), radyal=True), st('#a8554e', 6)), G(el(320, 230, 222, 166), gf(IDRAR, (300, 200), (330, 280), radyal=True)), o=gorun(A, 0, 2))
    A.ekle('opak', G(el(320, 230, 230, 174), fl('#ffffff', o=95)), o=K((0, 0), (T(2, .2), 0), (T(2, .6), 100), (T(2, 1) + 8, 100), (T(2, 1) + 16, 0)))
    A.ekle('kateter', G(yol('M320 250 L320 420 C320 460 400 470 470 450'), st('#8a96a6', 11)), G(yol('M320 250 L320 420 C320 460 400 470 470 450'), st('#eef2f6', 8)), o=gorun(A, 0, 2))
    A.ekle('kultur', G(rc(560, 400, 70, 90, 10), fl('#eef3f8', o=95), st('#7d8aa0', 2)), G(rc(560, 420, 60, 50, 6), fl('#f2cf55')), G(rc(560, 350, 84, 18, 4), fl('#c0392b')),
           G(yol('M470 450 C520 440 540 400 556 380'), st('#e1b300', 4, kesik=(8, 8), kesik_kayma=KD((0, 0), (A.op, -A.op * 2)))), o=gorun(A, 0, 0))
    A.ekle('cocuk', *kisi(640, 120, '#f2b8d0', .7), o=belir(A, 0, .1, 0))
    A.ekle('yasli', *kisi(730, 110, '#c9d3de', .85), G(yol('M760 160 L770 240'), st('#7a5a3a', 4)), o=belir(A, 0, .2, 0))
    et(A, 0, 690, 260, 'Küçük çocuk · yaşlı: temiz örnek veremiyor', 'bilgi', .25); et(A, 0, 560, 300, 'Steril kültür örneği', 'dogru', .5)
    A.ekle('enjektor', G(rc(560, 450, 150, 40, 5), fl('#eef3f8', o=95), st('#6b7a90', 2)), G(rc(540, 450, 90, 30), fl('#b48ae0')), G(rc(478, 450, 20, 12, 2), fl('#9aa6b4')),
           G(rc(642, 450, 10, 50, 3), fl('#6b7a90')), o=gorun(A, 1, 1), p=K((0, [80, 0, 0]), (T(1, .1), [80, 0, 0]), (T(1, .35), [0, 0, 0])))
    A.ekle('ilac', G(yol('M470 450 C400 470 320 460 320 420 L320 250'), st('#8e44ad', 5, kesik=(10, 10), kesik_kayma=KD((T(1, .35), 0), (T(1, 1), -300)))), o=gorun(A, 1, 1))
    A.ekle('ilac-mesane', G(el(320, 230, 222, 166), fl('#b48ae0', o=55)), o=K((0, 0), (T(1, .5), 0), (T(1, .9), 100), (T(1, 1) + 8, 100), (T(1, 1) + 16, 0)))
    et(A, 1, 600, 390, 'Kemoterapötik ilaç', 'bilgi', .2)
    et(A, 2, 600, 220, 'Travma · sistografi: opak madde', 'bilgi', .2)
    kavram_ikonlar(A, 3, [(150, 210, ikon_kutu(150, 210, '#2e9e5b', [G(el(150, 205, 80, 80), gf(MESANE, (130, 185), (170, 230), radyal=True)), G(el(150, 205, 62, 62), fl('#f2cf55'))]), '1 · İdrar yapamama', 'dogru'),
                          (400, 210, ikon_kutu(400, 210, '#2e9e5b', [G(rc(400, 210, 70, 84, 10), fl('#f4f7fa'), st('#9aa6b4', 2)), G(rc(400, 228, 60, 40, 6), fl('#f2cf55'))]), '2 · İdrar takibi', 'dogru'),
                          (650, 210, ikon_kutu(650, 210, '#9aa6b4', [G(rc(650, 216, 44, 56, 8), fl('#eef3f8'), st('#7d8aa0', 2)), G(rc(650, 184, 54, 12, 3), fl('#c0392b'))]), '3 · Kültür, ilaç, sistografi', 'bilgi')], 'sira')


def konusma(A, b, metin_x, x=520, y=120, renk='#d23b3b', f1=.05, f2=None):
    A.ekle('balon', G(yol(f'M{x - 150} {y - 40} L{x + 150} {y - 40} C{x + 166} {y - 40} {x + 166} {y + 40} {x + 150} {y + 40} L{x - 90} {y + 40} L{x - 130} {y + 70} L{x - 120} {y + 40} L{x - 150} {y + 40} C{x - 166} {y + 40} {x - 166} {y - 40} {x - 150} {y - 40} Z'),
                       fl('#ffffff'), st(renk, 3)), o=belir(A, b, f1, b) if f2 is None else K((0, 0), (A.T(b, f1), 0), (A.T(b, f1) + 6, 100), (A.T(b, f2), 100), (A.T(b, f2) + 6, 0)))


def a_sistit(A):
    T = A.T
    zemin_kat(A, 0, 0)
    A.ekle('hasta0', *kisi(240, 200, '#8fc1c9', 1.3), o=gorun(A, 0, 0))
    konusma(A, 0, 0, 520, 140)
    et(A, 0, 520, 140, '"İdrar yapamıyorum"', 'uyari')
    A.ekle('tepsi', G(rc(560, 380, 220, 80, 10), fl('#c7d1da'), st('#8b96a3', 2)), G(yol('M480 380 C520 350 580 410 640 370'), st('#e3b544', 8)), o=belir(A, 0, .4, 0))
    carpi(A, 560, 380, 0, .6)
    et(A, 0, 560, 460, 'Hemen sonda takma!', 'uyari', .6)
    ic_ekle(A, LU.glob, [None, None, None, None, 1], [(1, 2)], 'sistit')
    A.kamera_sabit(1, 2, 400, 260, 112)
    A.ekle('agri', G(yol('M470 230 L452 268 L470 268 L456 306 L494 256 L474 256 L488 230 Z'), fl('#e1a92e'), st('#a8741a', 1.5)), o=belir(A, 1, .1, 2))
    A.ekle('az-idrar', damla(370, 470, .8), p=KD(*[(T(1, .4) + k * 18, [0, (k % 2) * 16, 0]) for k in range(max(1, int((T(1, 1) - T(1, .4)) / 18)))]), o=belir(A, 1, .4, 1))
    et(A, 1, 560, 200, 'Suprapubik ağrı · sık idrar · yanma', 'uyari', .1)
    A.ekle('soru', G(el(600, 200, 100, 100), fl('#ffffff'), st('#e1a92e', 5)), G(yol('M584 186 C584 166 616 166 616 186 C616 200 600 200 600 216'), st('#e1a92e', 8)), G(el(600, 232, 9, 9), fl('#e1a92e')),
           o=belir(A, 2, .1, 2))
    et(A, 2, 600, 300, 'Retansiyon değil · önce değerlendir', 'uyari', .2)
    ic_ekle(A, LU.glob, [3, 3, 3, 4, None], [(3, 4)], 'glob')
    et(A, 3, 600, 440, 'Altı aylık gebe karnı gibi kabarık', 'bilgi', .5)
    kavram_ikonlar(A, 5, [(160, 210, ikon_kutu(160, 210, '#d23b3b', [*[G(el(130 + i * 22, 200 + (i % 2) * 22, 18, 12), fl('#5aa874'), st('#2e6e46', 1)) for i in range(4)]]), 'Enfeksiyon riski', 'uyari'),
                          (400, 210, ikon_kutu(400, 210, '#d23b3b', [G(yol('M390 160 L370 215 L400 215 L380 260 L430 195 L400 195 L420 160 Z'), fl('#e1a92e'))]), 'Günlerce ağrı', 'uyari'),
                          (640, 210, ikon_kutu(640, 210, '#d23b3b', [G(yol('M580 196 L620 196 C632 196 632 204 640 204 C648 204 648 196 660 196 L700 196 L700 224 L660 224 C648 224 648 216 640 216 C632 216 632 224 620 224 L580 224 Z'), fl('#f0b8b2'), st('#a8554e', 1.5))]), 'Tek kateter bile: erkekte darlık', 'uyari')], 'sonuc')


def a_enf(A):
    T = A.T
    zemin_kat(A, 0, 0)
    A.ekle('dur', G(yol('M400 90 L470 120 L500 190 L470 260 L400 290 L330 260 L300 190 L330 120 Z'), fl('#d23b3b'), st('#8d1f1f', 4)), G(rc(400, 190, 140, 30, 6), fl('#ffffff')), o=belir(A, 0, .1, 0))
    et(A, 0, 400, 350, 'Kesin kontrendikasyon: takarsan malpraktis', 'uyari', .3)

    def anatomi(_z):
        LU.erkek_anatomi(LU._IC)
    ic_ekle(A, anatomi, [1], [(1, 3)], 'anatomi')
    A.ekle('prostat-ilt', G(el(300, 262, 92, 72), fl('#d23b3b', o=55), st('#8d1f1f', 3)), o=K((0, 0), (T(1, .2), 0), (T(1, .35), 100), (T(1, 1) + 8, 100), (T(1, 1) + 16, 0)),
           s=KD(*[(T(1, .2) + k * 10, [100 + (k % 2) * 8, 100 + (k % 2) * 8, 100]) for k in range(max(1, int((T(1, 1) - T(1, .2)) / 10)))]), a=(300, 262), p=S([300, 262, 0]))
    A.ekle('bakteri', *[G(el(300 + dx, 262 + dy, 9, 6), fl('#2e6e46')) for dx, dy in [(-50, -20), (40, -30), (60, 10), (-60, 30), (0, -60), (20, 50)]],
           s=K((0, [40, 40, 100]), (T(1, .4), [40, 40, 100]), (T(1, .9), [260, 260, 100])), a=(300, 262), p=S([300, 262, 0]), o=gorun(A, 1, 1))
    # rektal tuşe: eldivenli parmak anüsten rektuma (prostata) uzanır → çarpı
    A.ekle('tuse', parmak_ucu(232, 404, 140, 1.0, steril=False), o=K((0, 0), (T(1, .05), 0), (T(1, .1), 100), (T(1, .5), 100), (T(1, .55), 0)),
           p=K((0, [-40, 34, 0]), (T(1, .05), [-40, 34, 0]), (T(1, .2), [0, 0, 0])))
    A.ekle('tuse-x', G(yol('M200 360 L260 420 M260 360 L200 420'), st('#d23b3b', 9)), o=K((0, 0), (T(1, .22), 0), (T(1, .26), 100), (T(1, .5), 100), (T(1, .55), 0)))
    et(A, 1, 150, 460, 'Rektal tuşe de yapılmaz', 'uyari', .2, .55)
    et(A, 1, 200, 60, 'Akut prostatit / abse: bakteriyemi, sepsis', 'uyari', .4)
    A.kamera_sabit(1, 1, 300, 280, 140)
    A.ekle('testis-ilt', G(el(505, 395, 90, 72), fl('#d23b3b', o=55), st('#8d1f1f', 3)), G(el(540, 396, 26, 50), fl('#d23b3b', o=55)), o=gorun(A, 2, 2))
    et(A, 2, 600, 470, 'Orşit · epididimit · Fournier · abse', 'uyari', .2)
    A.ekle('hizli-kateter', G(yol(LU.KATETER_Y), st('#5b6676', 9, o=35)), G(yol(LU.KATETER_Y), st('#eef2f6', 7)), o=gorun(A, 3, 3))
    A.ekle('hizli-akis', G(yol('M300 150 L300 305 C300 345 330 362 372 352 L470 320 L700 302 L760 302'), st('#e1b300', 5, kesik=(14, 8), kesik_kayma=KD((T(3), 0), (A.op, -(A.op - T(3)) * 8)))), o=gorun(A, 3, 3))
    for i, (dx, dy) in enumerate([(-30, -10), (20, -30), (40, 20), (-40, 30), (0, 40)]):
        A.ekle(f'kanama{i}', G(el(300 + dx, 150 + dy, 9, 9), fl('#b3201f')), o=belir(A, 3, .3 + i * .08, 3))
    et(A, 3, 380, 40, 'Hızlı boşaltma → mukozal kanama', 'bilgi', .3)
    tik(A, 600, 140, 3, .6)
    et(A, 3, 600, 210, 'Yine de kontrendikasyon değil', 'dogru', .6)
    A.kamera_sabit(2, 2, 505, 380, 170)
    A.kamera_sabit(3, 3, 400, 220, 105)


def a_travma(A):
    T = A.T
    ic_ekle(A, LU.travma, [0, 1, 2, 4], [(0, 2), (4, 4)])
    for i, (x, sh, m) in enumerate([(160, [G(yol('M130 60 L130 160 M150 60 L150 160'), st('#7a5a3a', 4)), *[G(yol(f'M130 {70 + j * 22} L150 {70 + j * 22}'), st('#7a5a3a', 3)) for j in range(5)], G(yol('M190 70 L190 150'), st('#d23b3b', 5)), G(yol('M180 136 L190 154 L200 136'), st('#d23b3b', 5))], 'Yüksekten düşme'),
                                    (400, [G(rc(400, 110, 120, 40, 14), fl('#2f6fd6')), G(rc(390, 86, 70, 26, 8), fl('#9cc6ff')), G(el(365, 132, 26, 26), fl('#2b2f36')), G(el(435, 132, 26, 26), fl('#2b2f36'))], 'Trafik kazası'),
                                    (640, [G(yol('M590 110 L690 110'), st('#7a5a3a', 8)), G(yol('M640 60 L640 104 M640 104 L616 150 M640 104 L664 150'), st('#3e4a58', 6)), G(el(640, 50, 20, 20), fl('#e9b896'))], 'Ata biner gibi düşme')]):
        A.ekle(f'neden{i}', G(rc(x, 110, 170, 130, 16), fl('#ffffff', o=92), st('#d23b3b', 2)), *sh, o=belir(A, 1, .1 + i * .15, 1))
        et(A, 1, x, 190, m, 'uyari', .1 + i * .15)
    A.kamera_sabit(1, 1, 400, 250, 100)
    ic_ekle(A, LU.travma, [3, 3, None, None], [(3, 3)], 'yalniz-kirik')
    A.kamera_sabit(3, 3, 400, 280, 100)
    A.ekle('kan-yok', G(el(400, 470, 50, 40), st('#2e9e5b', 4)), o=belir(A, 3, .3, 3))
    tik(A, 620, 400, 3, .5)
    et(A, 3, 600, 460, 'Pelvis kırığı var, meatusta kan yok → takılabilir', 'dogru', .5)
    # kısmi yırtık: kateter itilince yırtık tamamlanır
    A.ekle('yirtik', G(yol('M392 354 L408 350'), st('#b3201f', 6)), s=K((0, [100, 100, 100]), (T(4, .3), [100, 100, 100]), (T(4, .6), [300, 260, 100])), a=(400, 352), p=S([400, 352, 0]), o=gorun(A, 4, 4))
    A.ekle('itilen', G(yol('M400 640 L400 520'), st('#8a96a6', 10)), G(yol('M400 640 L400 520'), st('#eef2f6', 8)), p=K((0, [0, 120, 0]), (T(4, .1), [0, 120, 0]), (T(4, .55), [0, -150, 0])), o=gorun(A, 4, 4))
    et(A, 4, 250, 440, 'Kısmi yırtık: zorlama yırtığı tamamlar', 'uyari', .3); et(A, 4, 600, 300, 'Başka yöntemle yaklaşılır', 'bilgi', .7)


def paket(x, y, lateks):
    r, k = ('#e3b544', '#8a6a1e') if lateks else ('#f4f7fa', '#8a96a6')
    return [G(yol(f'M{x - 82} {y - 46} L{x + 74} {y - 46} L{x + 86} {y - 34} L{x + 86} {y + 46} L{x - 82} {y + 46} Z'), fl('#f4f1ea'), st('#b9b1a0', 1.2)),
            G(yol(f'M{x - 60} {y + 26} C{x - 30} {y + 26} {x - 20} {y - 30} {x + 20} {y - 30} C{x + 50} {y - 30} {x + 60} {y - 6} {x + 40} {y + 6}'), st(k, 10, o=35)),
            G(yol(f'M{x - 60} {y + 26} C{x - 30} {y + 26} {x - 20} {y - 30} {x + 20} {y - 30} C{x + 50} {y - 30} {x + 60} {y - 6} {x + 40} {y + 6}'), st(r, 8)),
            G(rc(x - 76, y + 10, 10, 9, 2), fl('#ef7d22')), G(rc(x + 56, y + 30, 50, 20, 3), fl('#ffffff'), st('#c9d3de', 1)), G(rc(x + 34, y + 30, 6, 20), fl('#ef7d22'))]


def enjektor(x, y, L, H, sivi='#e9f3fb', genis=False):
    sh = [G(rc(x, y, L, H, 3), fl('#eef3f8', o=95), st('#6b7a90', 1.5)), G(rc(x - 4, y, L - 20, H - 6), fl(sivi, o=90)),
          *[G(yol(f'M{x - L / 2 + 8 + i * (L - 16) / 9} {y - H / 2} L{x - L / 2 + 8 + i * (L - 16) / 9} {y - H / 2 + (5 if i % 2 else 8)}'), st('#3e4a58', 1)) for i in range(10)],
          G(rc(x - L / 2 - 20, y, 40, H * .35), fl('#cfd8e2')), G(rc(x - L / 2 - 42, y, 8, H + 10, 2), fl('#6b7a90')), G(rc(x - L / 2 + 6, y, 8, H - 4, 1.5), fl('#2b2f36'))]
    sh.append(G(yol(f'M{x + L / 2} {y - 9} L{x + L / 2 + 34} {y - 3} L{x + L / 2 + 34} {y + 3} L{x + L / 2} {y + 9} Z' if genis else f'M{x + L / 2} {y - 4} L{x + L / 2 + 12} {y - 3} L{x + L / 2 + 12} {y + 3} L{x + L / 2} {y + 4} Z'), fl('#dfe6ee'), st('#6b7a90', 1.2)))
    return sh


def a_malzeme(A):
    """Tepsiye malzemeler cümle sırasıyla iner (ürün fotoğraflarına göre çizim)."""
    T = A.T
    zemin_kat(A, 0, 4)
    A.ekle('tepsi', G(rc(400, 250, 780, 470, 24), gf([(0, '#8b96a3'), (.4, '#eef2f6'), (1, '#6d7884')], (400, 10), (400, 490))),
           G(rc(400, 250, 756, 446, 18), gf([(0, '#dfe6ec'), (1, '#c7d1da')], (400, 30), (400, 470))), o=gorun(A, 0, 4))
    O = [
        (0, .05, [*paket(120, 100, True)], (120, 160, 'Lateks Foley · 16 Fr')),
        (0, .15, [*paket(320, 100, False)], (320, 160, 'Silikon Foley')),
        (0, .45, [G(rc(510, 110, 140, 60, 4), fl('#eaf1f8'), st('#8a9bb0', 1.2)), G(rc(510, 76, 140, 12, 2), fl('#f6f9fc'), st('#8a9bb0', 1)), G(rc(480, 118, 70, 14, 3), fl('#2f6fd6')),
                  G(yol('M520 76 C516 50 530 36 540 40 L548 74'), fl('#cfe0f5'), st('#6f8bb3', 1.2))], (510, 160, 'Steril olmayan eldiven')),
        (0, .65, [G(rc(690, 100, 160, 90, 4), fl('#fbfaf6'), st('#c9b48a', 1.2)), G(yol('M690 56 L690 144'), st('#e5dcc8', 1.5)),
                  yumruk(650, 100, .32, 90), yumruk(730, 100, .32, 90)], (690, 160, 'Steril eldiven')),
        (1, .1, [G(rc(150, 260, 130, 26, 6), fl('#eef3f8'), st('#6b7a90', 1.2)), G(rc(140, 260, 90, 16), fl('#cfe6ff')), G(yol('M215 252 L250 257 L250 263 L215 268 Z'), fl('#dfe6ee'), st('#6b7a90', 1)),
                  G(rc(80, 260, 12, 36, 3), fl('#6b7a90'))], (150, 310, 'Jel (lidokainli)')),
        (2, .05, [*[G(rc(320 + dx, 262, 22, 64, 6), fl('#eef3f8', o=95), st('#6b7a90', 1.2)) for dx in (-26, 0, 26)], *[G(rc(320 + dx, 226, 14, 10, 2), fl('#e9eef3'), st('#6b7a90', 1)) for dx in (-26, 0, 26)]], (320, 310, 'Steril izotonik')),
        (2, .25, enjektor(500, 262, 92, 20), (500, 310, '10 mL enjektör · balon')),
        (2, .6, enjektor(680, 262, 120, 34, genis=True), (680, 310, 'Geniş uçlu 50 mL enjektör')),
        (3, .05, [G(rc(110, 410, 40, 74, 9), gf([(0, '#7a3410'), (.5, '#b5551d'), (1, '#6d2c0c')], (90, 0), (130, 0))), G(rc(110, 366, 22, 12, 2), fl('#e9eef3')),
                  G(yol('M150 420 C150 396 250 396 250 420 C250 450 222 460 200 446 C178 460 150 450 150 420 Z'), gf([(0, '#8b96a3'), (.4, '#eef2f6'), (1, '#6d7884')], (0, 400), (0, 460))),
                  *[G(el(x, 418, 18, 18), fl('#ffffff'), st('#d6dde5', 1)) for x in (176, 198, 220)]], (170, 470, 'Antiseptik · gazlı bez')),
        (3, .4, [G(rc(400, 410, 170, 100), yol('M400 392 C390 392 384 400 384 410 C384 420 390 428 400 428 C410 428 416 420 416 410 C416 400 410 392 400 392 Z'), fl_cift('#3b7bb8'))], (400, 470, 'Steril delikli örtü')),
        (3, .7, [G(rc(600, 410, 110, 110, 10), fl('#f4f7fa', o=92), st('#9aa6b4', 2)), G(rc(600, 440, 96, 40, 6), fl('#f2cf55')), G(yol('M600 356 C600 330 650 326 680 334'), st('#cfd8e2', 6)),
                  G(rc(600, 470, 20, 10, 2), fl('#6b7a90'))], (600, 470, 'İdrar torbası')),
    ]
    for j, (b, f, sh, (lx, ly, m)) in enumerate(O):
        k = T(b, f)
        A.ekle(f'oge{j}', *sh, p=K((0, [0, -560, 0]), (k, [0, -560, 0]), (k + 16, [0, 0, 0])), o=K((0, 0), (k, 0), (k + 4, 100), (T(4, 1) + 8, 100), (T(4, 1) + 16, 0)))
        et(A, b, lx, ly + (26 if j % 2 else 0), m, 'bilgi', f + .05)
    et(A, 1, 300, 330, 'Lidokain: kayganlaştırır + anestezi', 'dogru', .5)
    # kamera: her cümlede ilgili rafa yaklaş
    A.kamera(0, 400, 140, 128); A.kamera(1, 220, 270, 170); A.kamera(2, 500, 280, 135); A.kamera(3, 400, 420, 128); A.kamera(4, 400, 250, 100)
    A.ekle('steril-alan', G(rc(400, 180, 760, 330, 14), fl('#cfe7d8', o=30), st('#2e9e5b', 4, kesik=(14, 8))), o=belir(A, 4, .05, 4))
    A.ekle('yardimci', yumruk(760, 220, .7, 180, steril=False), p=K((0, [120, 0, 0]), (T(4, .1), [120, 0, 0]), (T(4, .35), [0, 0, 0])), o=belir(A, 4, .1, 4))
    A.ekle('alan-el', yumruk(560, 240, .7, 0, steril=True), p=K((0, [-60, 120, 0]), (T(4, .4), [-60, 120, 0]), (T(4, .65), [0, 0, 0])), o=belir(A, 4, .4, 4))
    et(A, 4, 660, 330, 'Yardımcı açar, uzatır', 'bilgi', .2); et(A, 4, 520, 330, 'Steril el yalnız steril alana', 'dogru', .6)


def foley_detay(A):
    """Kateter yapısı: 7 cümlenin her biri ayrı eylem."""
    T = A.T
    zemin_kat(A, 0, 6)
    for y, r, k, ad in ((170, '#e3b544', '#8a6a1e', 'Lateks · kısa süreli'), (300, '#f2f5f8', '#8a96a6', 'Silikon · uzun süreli')):
        A.ekle(f'kat{y}', G(yol(f'M80 {y} L640 {y}'), st(k, 22, o=40)), G(yol(f'M80 {y} L640 {y}'), st(r, 18)), G(yol(f'M80 {y - 5} L640 {y - 5}'), st('#ffffff', 4, o=60)),
               G(el(78, y, 20, 18), fl(r), st(k, 1.5)), o=gorun(A, 0, 0), p=K((0, [-700, 0, 0]), (T(0, .05 if y == 170 else .3), [-700, 0, 0]), (T(0, .05 if y == 170 else .3) + 16, [0, 0, 0])))
        et(A, 0, 360, y - 40, ad, 'bilgi', .2 if y == 170 else .45)
    gov = 'M60 250 L560 250'
    A.ekle('govde', G(yol(gov), st('#8a6a1e', 26, o=40)), G(yol(gov), st('#e3b544', 22)), G(yol('M60 244 L560 244'), st('#fff6d6', 5)),
           G(yol('M60 238 C34 238 28 246 28 250 C28 254 34 262 60 262 Z'), fl('#e3b544'), st('#8a6a1e', 1.5)), o=gorun(A, 1, 5))
    A.ekle('delik', G(el(72, 246, 16, 9), fl('#4a3510')), G(el(96, 254, 13, 8), fl('#4a3510', o=80)), o=gorun(A, 1, 5))
    A.ekle('balon-sonuk', G(rc(140, 250, 64, 30, 13), fl('#e8c25c'), st('#8a6a1e', 1.5)), o=K((0, 0), (T(1) - 8, 0), (T(1), 100), (T(4, .3), 100), (T(4, .4), 0)))
    A.ekle('balon', G(el(0, 0, 130, 110), fl('#f6e3a2', o=60), st('#c9a03a', 2.5)), G(el(0, 12, 100, 60), fl('#e8f2fb', o=60)), G(el(-24, -26, 30, 14), fl('#ffffff', o=85)),
           p=S([140, 250, 0]), s=K((0, [30, 30, 100]), (T(4, .3), [30, 30, 100]), (T(4, .7), [100, 100, 100])), o=K((0, 0), (T(4, .3), 0), (T(4, .35), 100), (T(5, 1) + 8, 100), (T(5, 1) + 16, 0)))
    A.ekle('catal', G(yol('M540 236 C566 234 584 228 604 222 L608 280 C588 274 566 268 540 266 Z'), fl('#e3b544'), st('#8a6a1e', 1.5)),
           G(yol('M604 220 L700 214 C712 214 716 222 716 228 L716 274 C716 280 712 288 700 288 L604 282 Z'), fl('#e3b544'), st('#8a6a1e', 1.8)),
           G(el(716, 251, 14, 60), fl('#d9a83a'), st('#8a6a1e', 1.5)), G(el(716, 251, 8, 36), fl('#4a3510')),
           G(yol('M560 240 C590 200 610 170 636 140'), st('#8a6a1e', 14, o=40)), G(yol('M560 240 C590 200 610 170 636 140'), st('#e3b544', 11)),
           G(rc(648, 126, 40, 30, 6), fl('#ef7d22'), st('#9a4a0e', 1.5)), o=gorun(A, 1, 5))
    A.ekle('vurgu-drenaj', G(el(670, 251, 120, 100), st('#2e9e5b', 5)), o=belir(A, 2, .3, 2))
    A.ekle('vurgu-balon-k', G(el(650, 140, 80, 60), st('#2f6fd6', 5)), o=belir(A, 2, .6, 2))
    et(A, 1, 90, 190, 'Uçtaki delikler', 'bilgi'); et(A, 1, 150, 310, 'Sabitleme balonu', 'bilgi', .4)
    et(A, 2, 670, 330, 'Kalın drenaj kanalı → torba', 'dogru', .3); et(A, 2, 650, 90, 'İnce valfli balon kanalı', 'bilgi', .6)
    A.ekle('hortum', G(yol('M800 420 C760 420 740 400 730 380'), st('#cfd8e2', 14)), G(rc(730, 372, 26, 30, 6), fl('#9aa6b4')),
           p=K((0, [0, 0, 0]), (T(3), [0, 0, 0]), (T(3, .25), [-60, -240, 0]), (T(3, .5), [-60, -240, 0]), (T(3, .8), [16, -120, 0])), o=gorun(A, 3, 3))
    carpi(A, 650, 140, 3, .25)
    tik(A, 760, 250, 3, .8)
    et(A, 3, 400, 420, 'Torba her zaman drenaj kanalına', 'dogru', .7)
    A.ekle('enjektor', G(rc(0, 0, 130, 34, 4), fl('#eef3f8', o=95), st('#6b7a90', 2)), G(rc(-10, 0, 90, 26), fl('#9fc4ef')),
           p=K((0, [780, 60, 0]), (T(4, .05), [780, 60, 0]), (T(4, .25), [700, 100, 0])), r=S(-40), o=gorun(A, 4, 4))
    A.ekle('cek', G(yol('M400 330 L240 330'), st('#2f6fd6', 6)), G(yol('M262 314 L236 330 L262 346'), st('#2f6fd6', 6)), o=belir(A, 4, .75, 4))
    et(A, 4, 330, 380, 'Basit çekiştirmeyle çıkmaz', 'bilgi', .75)
    # s5: torba sağ altta, hortumla drenaj kanalına bağlı; musluk açılır
    A.ekle('torba-hortum', G(yol('M724 251 C790 260 790 330 700 350'), st('#cfd8e2', 10)), o=gorun(A, 5, 5))
    A.ekle('torba', G(rc(640, 410, 170, 150, 14), fl('#f4f7fa', o=92), st('#9aa6b4', 3)), G(rc(640, 450, 154, 66, 10), gf([(0, '#f8dd6c'), (1, '#e7b82e')], (640, 420), (640, 480))),
           G(rc(640, 490, 28, 14, 4), fl('#6b7a90')), G(rc(660, 490, 14, 8, 2), fl('#c0392b')),
           o=gorun(A, 5, 5), p=K((0, [0, 160, 0]), (T(5), [0, 160, 0]), (T(5, .2), [0, 0, 0])))
    A.ekle('bosalt', G(yol('M640 498 L640 540'), st('#e1b300', 6, kesik=(8, 6), kesik_kayma=KD((T(5, .5), 0), (A.op, -80)))), o=belir(A, 5, .5, 5))
    et(A, 5, 520, 470, 'Musluktan boşaltılır', 'bilgi', .5)
    zemin_kat(A, 6, 6, 'zemin-boy')
    for i, f in enumerate([12, 16, 20, 24]):
        A.ekle(f'eriskin{f}', G(yol(f'M120 {100 + i * 50} L680 {100 + i * 50}'), st('#8a96a6', f * 0.9 + 2)), G(yol(f'M120 {100 + i * 50} L680 {100 + i * 50}'), st('#eef2f6', f * 0.9)), o=belir(A, 6, .05 + i * .06, 6))
    for i, f in enumerate([6, 8, 10]):
        A.ekle(f'cocuk{f}', G(yol(f'M120 {330 + i * 40} L480 {330 + i * 40}'), st('#8a96a6', f + 2)), G(yol(f'M120 {330 + i * 40} L480 {330 + i * 40}'), st('#dfeaf6', f)), o=belir(A, 6, .5 + i * .06, 6))
    et(A, 6, 720, 170, 'Erişkin 12–24 Fr · boy aynı', 'bilgi', .2); et(A, 6, 600, 370, 'Çocuk 6–8–10 Fr · daha kısa', 'bilgi', .6)
    A.kamera(1, 140, 250, 190)
    A.kamera(2, 640, 220, 160)
    A.kamera(3, 620, 250, 120)
    A.kamera(4, 360, 220, 110)
    A.kamera(5, 600, 350, 115)
    A.kamera(6, 400, 250, 100)


def a_iletisim(A):
    ic_ekle(A, LU.mahremiyet, [0, 2, 3], [(0, 3)])
    zemin_kat(A, 1, 1, 'zemin-onam')
    A.kamera_sabit(1, 1, 400, 250, 100)
    A.ekle('hekim1', *kisi(200, 170, '#ffffff', 1.3, True), o=gorun(A, 1, 1))
    konusma(A, 1, 0, 520, 130, f2=.5)
    et(A, 1, 520, 130, '"Yatın, sonda takacağım"', 'uyari', .05, .5)
    A.ekle('carpi1', G(yol('M484 94 L556 166 M556 94 L484 166'), st('#d23b3b', 11)), o=K((0, 0), (A.T(1, .25), 0), (A.T(1, .28), 100), (A.T(1, .5), 100), (A.T(1, .53), 0)))
    konusma(A, 1, 0, 520, 300, renk='#2e9e5b', f1=.55, f2=1)
    et(A, 1, 520, 300, 'Neden gerektiğini anlatır, onam alır', 'dogru', .55)
    A.ekle('cocuk-ebeveyn', G(rc(150, 110, 220, 150, 14), fl('#ffffff', o=95), st('#2f6fd6', 2)), *kisi(110, 80, '#a3b9d9', .65), *kisi(185, 100, '#f2b8d0', .45),
           o=belir(A, 3, .5, 3))
    et(A, 3, 150, 200, 'Çocukta ebeveyn · karşı cinste karşı cins personel', 'bilgi', .5)
    A.kamera_sabit(3, 3, 400, 250, 100)
    kavram_ikonlar(A, 4, [(260, 220, ikon_kutu(260, 220, '#2e9e5b', [G(el(260, 220, 70, 70), gf(DERI, (250, 210), (270, 230), radyal=True)), G(yol('M240 230 C250 244 270 244 280 230'), st('#3b2a1e', 4))]), 'Hasta rahat', 'dogru'),
                          (540, 220, ikon_kutu(540, 220, '#2f6fd6', [G(yol('M540 170 L590 190 L586 236 C580 262 560 274 540 282 C520 274 500 262 494 236 L490 190 Z'), fl('#2f6fd6'))]), 'Medikolegal koruma', 'bilgi')], 'koruma')


def a_pozisyon(A):
    T = A.T
    zemin_kat(A, 0, 2)
    A.ekle('yatak0', G(rc(400, 330, 640, 60, 12), gf([(0, '#f4f7fa'), (1, '#d6dee7')], (400, 300), (400, 360)), st('#9aa6b4', 2)), G(rc(140, 290, 90, 30, 12), fl('#ffffff')), o=gorun(A, 0, 0))
    A.ekle('erkek', G(el(140, 260, 60, 56), gf(DERI, (130, 250), (150, 272), radyal=True)), G(yol('M170 270 L420 262 L640 280 L640 300 L170 300 Z'), fl('#8fc1c9'), st('#4c8590', 1.5)),
           G(yol('M420 262 L640 280 L640 300 L420 300 Z'), gf(DERI, (500, 270), (500, 300))), o=gorun(A, 0, 0))
    A.ekle('camasir', G(rc(0, 0, 70, 40, 6), fl('#5b6676')), p=K((0, [430, 282, 0]), (T(0, .4), [430, 282, 0]), (T(0, .8), [520, 288, 0])), o=gorun(A, 0, 0))
    et(A, 0, 400, 200, 'Supin: sırtüstü · iç çamaşırı indirilir', 'bilgi', .2)
    A.ekle('yatak1', G(rc(400, 260, 620, 300, 16), gf([(0, '#f4f7fa'), (1, '#d6dee7')], (400, 120), (400, 400)), st('#9aa6b4', 2)), o=gorun(A, 1, 2))
    A.ekle('kadin', G(el(160, 260, 60, 56), gf(DERI, (150, 250), (170, 270), radyal=True)), G(yol('M190 220 L400 216 C412 216 416 304 400 304 L190 300 Z'), fl('#8fc1c9'), st('#4c8590', 1.5)), o=gorun(A, 1, 2))
    for s, (d1, d2) in enumerate([('M400 236 L520 236 L640 236', 'M400 236 L500 170 L620 150'), ('M400 284 L520 284 L640 284', 'M400 284 L500 350 L620 370')]):
        A.ekle(f'bacak{s}', G(yol_morph(d1, d2, T(2, .1), T(2, .6)), st('#b9805a', 30)), G(yol_morph(d1, d2, T(2, .1), T(2, .6)), st('#e9b896', 26)), o=gorun(A, 1, 2))
    A.ekle('V', G(yol('M640 150 L420 260 L640 370'), st('#2f6fd6', 4, kesik=(12, 8))), o=belir(A, 2, .65, 2))
    # yandan görünüm: dizler bükük, topuklar yatakta
    panel(A, 2, .05, 1, 640, 90, 300, 150, 'yan', G(yol('M500 140 L780 140'), st('#9aa6b4', 6)), G(yol('M510 128 L640 128'), st('#8fc1c9', 22)),
          G(yol_morph('M640 128 L700 128 L760 128', 'M640 128 L690 70 L740 132', T(2, .1), T(2, .6)), st('#e9b896', 18)), G(el(510, 120, 22, 22), fl('#e9b896')),
          kenar='#2f6fd6')
    et(A, 2, 640, 30, 'Yandan: diz bükük, topuk yatakta', 'bilgi', .1)
    et(A, 1, 400, 80, 'Modifiye litotomi', 'bilgi'); et(A, 2, 680, 300, 'Bacaklar V şeklinde açılır', 'dogru', .65)


def a_kadin_anatomi(A):
    T = A.T
    vulva(A, 0, 4, ayir=(T(1, 0), T(1, .5)), parmak=(T(4, .1), T(4, .6)))
    et(A, 0, 250, 150, 'Labium majus', 'bilgi', .1); et(A, 0, 330, 260, 'Labium minus', 'bilgi', .4)
    et(A, 1, 520, 118, 'Klitoris', 'bilgi'); et(A, 1, 560, 205, 'Meatus (≈1 cm altında)', 'dogru', .4)
    et(A, 2, 560, 310, 'Vajina', 'bilgi')
    A.ekle('meatus-vurgu', G(el(400, 208, 46, 38), st('#2e9e5b', 4)), o=belir(A, 1, .4, 1))
    A.ekle('vajina-vurgu', G(el(400, 312, 80, 136), st('#e1a92e', 4)), o=belir(A, 2, .2, 2))
    panel(A, 3, .05, 1, 160, 110, 260, 170, 'fark', *kisi(100, 80, '#f2b8d0', .6), *kisi(210, 70, '#8fc1c9', .7), kenar='#d23b3b')
    et(A, 3, 100, 190, 'Kız çocuk ⚠', 'uyari', .1); et(A, 3, 210, 190, 'Doğum yapmış ✓', 'dogru', .1)
    et(A, 3, 400, 470, 'Kız bebek, çocuk, cinsel aktif olmayan: anatomiyi kesin bil', 'uyari', .3)
    et(A, 4, 400, 470, 'Gerçek dokuda yumuşak açılır', 'bilgi', .3)
    A.kamera(1, 400, 200, 170)
    A.kamera(2, 400, 280, 150)
    A.kamera(3, 400, 250, 100)


def a_kadin_temizlik(A):
    ic_ekle(A, LU.kadin_temizlik, [0, 1, 1, 2, 3], [(0, 3)])
    zemin_kat(A, 4, 4, 'zemin-uzat')
    T = A.T
    A.ekle('ortu4', G(rc(400, 380, 800, 240), fl('#3b7bb8', o=75)), o=gorun(A, 4, 4))
    # yardımcı (mavi eldiven) steril paketi soyar; steril el kateteri ve jeli alır
    A.ekle('paket', G(rc(0, 0, 170, 110, 8), fl('#fbfaf6'), st('#c9b48a', 2)), G(yol('M-70 -10 C-30 -40 30 20 70 -10'), st('#e3b544', 7)),
           G(yol_morph('M-85 -55 L85 -55 L85 -50 L-85 -50 Z', 'M-85 -55 L85 -55 L60 -120 L-60 -120 Z', T(4, .1), T(4, .35)), fl('#e8e0cc'), st('#c9b48a', 1.5)),
           p=K((0, [720, 220, 0]), (T(4, .05), [720, 220, 0]), (T(4, .4), [400, 300, 0])), o=gorun(A, 4, 4))
    A.ekle('yardimci-sol', yumruk(0, 0, .55, 180, steril=False), p=K((0, [800, 200, 0]), (T(4, .05), [800, 200, 0]), (T(4, .4), [560, 230, 0])), o=gorun(A, 4, 4))
    A.ekle('yardimci-sag', yumruk(0, 0, .55, 180, steril=False), p=K((0, [800, 400, 0]), (T(4, .05), [800, 400, 0]), (T(4, .4), [560, 370, 0])), o=gorun(A, 4, 4))
    A.ekle('steril-el', yumruk(0, 0, .65, 0, steril=True), p=K((0, [-80, 300, 0]), (T(4, .45), [-80, 300, 0]), (T(4, .75), [240, 300, 0])), o=belir(A, 4, .45, 4))
    et(A, 4, 560, 120, 'Yardımcı paketi açar, steril uzatır', 'bilgi', .1); et(A, 4, 300, 430, 'Steril el yalnız steril malzemeye', 'dogru', .6)


def a_kadin_yerlestirme(A):
    T = A.T
    jel_ucuna(A, 0)
    A.kamera_sabit(0, 0, 560, 300, 150)
    avuc_kateter(A, 1)
    et(A, 1, 400, 460, 'Avuçta halka: uç hiçbir yere değmez', 'dogru', .5)
    panel(A, 1, .72, 1, 640, 380, 280, 170, 'sarkan', G(yol('M500 460 C540 380 620 360 780 380 L780 465 L500 465 Z'), gf(DERI, (640, 380), (640, 460))),
          G(yol('M560 300 C560 340 600 380 640 400'), st('#e3b544', 6)), G(el(640, 400, 40, 40), st('#d23b3b', 4)),
          G(yol('M610 320 L670 380 M670 320 L610 380'), st('#d23b3b', 7)), kenar='#d23b3b')
    et(A, 1, 640, 310, 'Sallanan uç uyluğa değdi → steril değil', 'uyari', .72)
    vulva(A, 2, 2, ayir=(T(2, .05), T(2, .35)), parmak=(T(2, .05), T(2, .35)))
    kd = 'M640 520 C560 400 460 270 404 212'
    A.ekle('giren-kateter', G(yol(kd), st('#8a6a1e', 12, o=45), tm(K((0, 0), (T(2, .45), 0), (T(2, .9), 100)))),
           G(yol(kd), st('#e3b544', 9), tm(K((0, 0), (T(2, .45), 0), (T(2, .9), 100)))), o=gorun(A, 2, 2))
    A.ekle('sag-el', yumruk(0, 0, .6, -125, steril=True), p=K((0, [640, 520, 0]), (T(2, .45), [640, 520, 0]), (T(2, .9), [560, 410, 0])), o=belir(A, 2, .4, 2))
    et(A, 2, 600, 160, 'Sol el ayırır · sağ el iter', 'bilgi', .3)
    ic_ekle(A, LU.kadin_ilerleyis, [3, 3, 3, 3, 4, 4], [(3, 4)], 'ilerle')


def a_erkek_temizlik(A):
    ic_ekle(A, LU.erkek_jel, [0, 1, 3, 3, 4], [(0, 1), (3, 4)])
    zemin_kat(A, 2, 2, 'zemin-kiyas')
    T = A.T
    A.ekle('kadin-u', G(yol('M140 160 L300 160'), st('#f0b8b2', 16)), G(el(300, 160, 26, 26), fl('#e3b544')), G(el(300, 160, 40, 26), fl('#cfe9ff', o=70)), o=gorun(A, 2, 2))
    A.ekle('erkek-u', G(yol('M140 330 L700 330'), st('#f0b8b2', 16)), G(yol('M140 330 L700 330'), st('#8fc7ff', 14, o=70), tm(K((0, 0), (T(2, .4), 0), (T(2, .9), 100)))), o=gorun(A, 2, 2))
    A.ekle('agri2', G(yol('M720 290 L706 320 L720 320 L708 350 L740 310 L724 310 L736 290 Z'), fl('#e1a92e')), o=belir(A, 2, .3, 2))
    et(A, 2, 220, 110, 'Kadın: kısa üretra · uca jel', 'bilgi'); et(A, 2, 420, 400, 'Erkek: uzun üretra, daha ağrılı · jelin tamamı', 'dogru', .4)


def a_erkek_yerlestirme(A):
    T = A.T
    avuc_kateter(A, 0, renk='#f2f5f8', kenar='#8a96a6', steril=True)
    et(A, 0, 400, 460, 'Avuca dola', 'dogru', .4)
    panel(A, 0, .7, 1, 640, 360, 280, 200, 'gevsek',
          yumruk(560, 300, .42, 0, steril=True),
          G(yol('M590 300 C630 320 650 370 640 440'), st('#8a96a6', 10)), G(yol('M590 300 C630 320 650 370 640 440'), st('#f2f5f8', 7)),
          G(yol('M690 330 L750 390 M750 330 L690 390'), st('#d23b3b', 7)), kenar='#d23b3b')
    et(A, 0, 640, 280, 'Uçtan gevşek tutarsan ilerletemezsin', 'uyari', .7)
    ic_ekle(A, LU.erkek_ilerleyis, [1, 1, 1, 2, 2, 2, 3, 4], [(1, 4)])
    # penisi dik ve gergin tutan sol el + çekme oku
    A.ekle('tutan-el', yumruk(545, 300, .72, 180, steril=False), o=gorun(A, 1, 1))
    A.ekle('gergin', G(yol('M620 240 L720 240'), st('#2f6fd6', 5)), G(yol('M700 226 L722 240 L700 254'), st('#2f6fd6', 5)), o=belir(A, 1, .1, 1))
    et(A, 1, 620, 200, 'Penis dik ve gergin', 'bilgi', .1)
    et(A, 2, 400, 470, 'Makette takılabilir · gerçek hastada daha kolay', 'bilgi', .5)


def a_idrar_gelmezse(A):
    T = A.T
    ic_ekle(A, LU.yikama, [0, 2, 2, 3, 4, 4], [(0, 0), (2, 4)])
    A.ekle('yanlis-sisirme', *enjektor(640, 120, 110, 30), G(yol('M590 70 L690 170 M690 70 L590 170'), st('#d23b3b', 9)), o=belir(A, 0, .45, 0))
    A.kamera_sabit(0, 0, 450, 240, 108)
    ic_ekle(A, LU.yanlis_balon, [1, None, None, None, None], [(1, 1)], 'kivrim')
    panel(A, 1, .02, .5, 200, 250, 300, 260, 'bos', G(el(200, 230, 120, 60), gf(MESANE, (180, 210), (220, 250), radyal=True), st('#a8554e', 4)),
          G(yol('M200 260 L200 360'), st('#eef2f6', 7)), G(el(200, 236, 10, 10), fl('#eef2f6'), st('#5b6676', 1)), kenar='#2f6fd6')
    et(A, 1, 200, 140, '1) Mesane gerçekten boş', 'bilgi', .02, .5); et(A, 1, 600, 60, '2) Kateter takıldı, kıvrıldı', 'uyari', .5)
    ic_ekle(A, LU.yanlis_balon, [None, 5, 5, 6, 6], [(5, 6)], 'yanlis')
    panel(A, 5, .02, .45, 200, 130, 300, 200, 'genis', G(el(200, 130, 220, 140), gf(MESANE, (170, 100), (230, 170), radyal=True), st('#a8554e', 4)),
          G(el(200, 150, 30, 22), fl('#ffffff', o=80), st('#2e9e5b', 2)), kenar='#2e9e5b')
    et(A, 5, 200, 250, 'Mesanede balon fark edilmez', 'dogru', .02, .45); et(A, 5, 600, 470, 'Üretra ≈ 1 cm: şişirirsen perfore', 'uyari', .45)
    A.ekle('inkontinans', damla(720, 300, .9), p=KD(*[(T(6, .2) + k * 14, [0, (k % 3) * 14, 0]) for k in range(max(1, int((T(6, 1) - T(6, .2)) / 14)))]), o=belir(A, 6, .2, 6))
    et(A, 6, 600, 60, 'Sfinkterde şişirme → kalıcı inkontinans', 'uyari', .1)


def a_sabitleme(A):
    T = A.T
    ic_ekle(A, LU.balon, [0, 0, 0, 0, 1, 1], [(0, 1)])
    ic_ekle(A, LU.idrar_akisi, [2, 2, 2, None, None], [(2, 2)], 'torba')
    A.ekle('kultur', G(rc(470, 300, 60, 80, 8), fl('#eef3f8', o=95), st('#7d8aa0', 2)), G(rc(470, 320, 50, 40, 6), fl('#f2cf55')), G(rc(470, 256, 70, 16, 4), fl('#c0392b')),
           G(yol('M420 390 C440 370 460 350 470 340'), st('#e1b300', 4, kesik=(6, 6), kesik_kayma=KD((T(2, .6), 0), (A.op, -A.op)))), o=belir(A, 2, .6, 2))
    et(A, 2, 470, 220, 'Gerekirse kültür örneği', 'bilgi', .6)
    zemin_kat(A, 3, 4, 'zemin-kayit')
    A.ekle('form', G(rc(330, 250, 300, 380, 12), fl('#ffffff'), st('#9aa6b4', 2)), G(rc(330, 70, 120, 24, 6), fl('#9aa6b4')),
           *[G(yol(f'M210 {130 + i * 50} L450 {130 + i * 50}'), st('#2f6fd6', 4), tm(K((0, 0), (T(3, .1 + i * .18), 0), (T(3, .25 + i * .18), 100)))) for i in range(5)], o=gorun(A, 3, 3))
    A.ekle('kalem', G(yol('M0 0 L-60 40'), st('#2b2f36', 8)), G(yol('M-60 40 L-68 46'), st('#e1a92e', 6)),
           p=KD(*[(T(3, .1 + i * .18 + j * .15 / 6), [210 + 240 * j / 6 + 60, 130 + i * 50 - 40, 0]) for i in range(5) for j in range(7)]), o=gorun(A, 3, 3))
    for i, m in enumerate(['Kateter türü · boyu', 'Balon hacmi', 'İdrar miktarı · görünümü', 'Güçlük', 'Komplikasyon']):
        et(A, 3, 600, 130 + i * 50, m, 'bilgi', .1 + i * .18)
    A.ekle('hasta', *kisi(260, 200, '#8fc1c9', 1.3), o=gorun(A, 4, 4))
    A.ekle('yanma', G(yol('M300 360 C290 340 300 320 310 300 C320 320 334 330 330 350 C326 366 306 372 300 360 Z'), fl('#e1a92e')), o=belir(A, 4, .2, 4))
    A.ekle('hekim', *kisi(560, 200, '#ffffff', 1.3, True), o=gorun(A, 4, 4))
    konusma(A, 4, 0, 460, 110, renk='#2f6fd6', f1=.3, f2=1)
    et(A, 4, 460, 110, 'Birkaç gün yanma olabilir', 'bilgi', .3)
    et(A, 4, 400, 470, 'Önceden anlatmak uyumu artırır', 'dogru', .6)


ADIMLAR = {'giris': a_giris, 'endikasyon-takip': a_takip, 'endikasyon-retansiyon': a_retansiyon, 'endikasyon-diger': a_diger, 'tuzak-sistit': a_sistit,
           'kontrendikasyon-enfeksiyon': a_enf, 'kontrendikasyon-travma': a_travma, 'malzeme': a_malzeme, 'kateter-yapisi': foley_detay,
           'iletisim': a_iletisim, 'pozisyon': a_pozisyon, 'kadin-anatomi': a_kadin_anatomi, 'kadin-temizlik': a_kadin_temizlik,
           'kadin-yerlestirme': a_kadin_yerlestirme, 'erkek-temizlik': a_erkek_temizlik, 'erkek-yerlestirme': a_erkek_yerlestirme,
           'idrar-gelmezse': a_idrar_gelmezse, 'sabitleme': a_sabitleme}


def main():
    ders = json.loads((VERI / '02.json').read_text(encoding='utf-8'))
    ses = json.loads((VERI / 'ses_02.json').read_text(encoding='utf-8'))
    idx = []
    for a in ders['adimlar']:
        f = ADIMLAR.get(a['id'])
        if not f:
            print(f'UYARI: {a["id"]} için adım videosu yok'); continue
        k = ses.get(f'o-{a["id"]}')
        z = k['zaman'] if k and len(k['zaman']) == len(a['cumleler']) else None
        A = adim(a['id'], [c['metin'] for c in a['cumleler']], z)
        A.baslik = a['baslik']
        f(A)
        (VERI / f'lottie/adim-{a["id"]}.json').write_text(json.dumps(A.json(), ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
        b = A.bilgi(); b['adim'] = a['id']; b['sesli'] = bool(z)
        idx.append(b)
        print(f'adim-{a["id"]}: {A.sure:.1f} sn, {len(a["cumleler"])} cümle, {len(A.katmanlar)} katman, {len(A.varliklar)} alt kompozisyon')
    (VERI / 'lottie/adimlar.json').write_text(json.dumps(idx, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
