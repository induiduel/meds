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
from lottie_dsl import FR, Anim, G, K, KD, S, el, fl, gf, ic_ekle, rc, st, tm, yol, yol_morph  # noqa: E402

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


def kisi(x, y, renk='#8fc1c9', olcek=1.0, beyaz=False):
    """Basit insan figürü (önden): baş, saç, gövde, kollar."""
    s = olcek
    return [G(yol(f'M{x - 30 * s} {y + 70 * s} C{x - 30 * s} {y + 30 * s} {x + 30 * s} {y + 30 * s} {x + 30 * s} {y + 70 * s} L{x + 36 * s} {y + 150 * s} L{x - 36 * s} {y + 150 * s} Z'),
              fl('#ffffff' if beyaz else renk), st('#7d8aa0', 1.5)),
            G(el(x, y, 44 * s, 46 * s), gf(DERI, (x - 6, y - 6), (x + 10, y + 14), radyal=True), st('#b9805a', 1.2)),
            G(yol(f'M{x - 22 * s} {y - 4 * s} C{x - 20 * s} {y - 30 * s} {x + 20 * s} {y - 30 * s} {x + 22 * s} {y - 4 * s} C{x + 12 * s} {y - 14 * s} {x - 12 * s} {y - 14 * s} {x - 22 * s} {y - 4 * s} Z'), fl('#3b2a1e'))]


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
           s=K((0, [100, 100, 100]), (T(b, .1), [100, 100, 100]), (T(b, .35), [100, 82, 100])), a=(700, 80), p=S([700, 80, 0]), o=gorun(A, b, b))
    A.ekle('damla', G(el(0, 0, 26, 30), fl('#cfe9ff', o=90), st('#8fb8e6', 1.5)), G(el(-5, -6, 7, 5), fl('#ffffff')),
           p=K((0, [612, 208, 0]), (T(b, .3), [612, 208, 0]), (T(b, .5), [606, 312, 0])), s=K((0, [20, 20, 100]), (T(b, .15), [20, 20, 100]), (T(b, .3), [100, 100, 100])),
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
            A.etiketler.append({'bas': round(A.T(b, f) / FR, 2), 'son': round(A.T(b, 1) / FR, 2), 'x': x, 'y': y + 95, 'metin': et, 'tur': tur})


def ikon_kutu(x, y, renk, ic):
    return [G(rc(x, y, 150, 130, 22), fl('#ffffff'), st(renk, 3)), *ic]


# ———————————————————————— adımlar

def adim(ad, cumleler, zaman):
    return Anim(f'adim-{ad}', ad, [{'baslik': ' '.join(c.split()[:4]).rstrip(',;:'), 'metin': c, 'sure': max(3, len(c) / 14)} for i, c in enumerate(cumleler)], zaman, bekle=0.9)


def a_giris(A):
    ic_ekle(A, LU.idrar_akisi, [0, 0, None, None, None], [(0, 0)])
    kavram_ikonlar(A, 1, [(180, 180, kisi(180, 140, '#ffffff', 1, True), 'Hekim', 'bilgi'), (400, 180, kisi(400, 140, '#8fc1c9'), 'Hemşire', 'bilgi'),
                          (620, 180, kisi(620, 140, '#a3b9d9'), 'Sağlık çalışanı', 'bilgi')], 'ekip')
    kavram_ikonlar(A, 2, [(220, 200, ikon_kutu(220, 200, '#2e9e5b', [G(yol('M190 200 L212 222 L252 178'), st('#2e9e5b', 12))]), 'Kime takılır?', 'dogru'),
                          (400, 200, ikon_kutu(400, 200, '#d23b3b', [G(yol('M372 172 L428 228 M428 172 L372 228'), st('#d23b3b', 12))]), 'Kime asla?', 'uyari'),
                          (580, 200, ikon_kutu(580, 200, '#2f6fd6', [G(el(580, 200, 70, 70), st('#2f6fd6', 6)), G(yol('M580 200 L580 172'), st('#2f6fd6', 6))]), 'Hangi endikasyon?', 'bilgi')], 'karar')
    yolh = [(130, 'Endikasyon'), (300, 'Kontrendikasyon'), (470, 'Malzeme'), (640, 'Uygulama')]
    kavram_ikonlar(A, 3, [(x, 220, ikon_kutu(x, 220, '#2f6fd6', [G(el(x, 220, 54, 54), fl('#2f6fd6')), ]), m, 'bilgi') for x, m in yolh], 'yol')
    A.ekle('yol-ok', G(yol('M130 220 L640 220'), st('#2f6fd6', 4, kesik=(10, 8)), tm(K((0, 0), (A.T(3, .1), 0), (A.T(3, .9), 100)))), o=gorun(A, 3, 3))
    A.kamera(0, 260, 220, 140)
    A.kamera(1, 400, 250, 100)


def monitor(A, b1, b2):
    o = gorun(A, b1, b2)
    A.ekle('monitor', G(rc(250, 190, 360, 240, 16), fl('#11161d'), st('#5b6676', 4)), G(rc(250, 330, 80, 30, 4), fl('#5b6676')),
           G(yol('M90 160 L150 160 L162 120 L176 200 L190 140 L200 160 L260 160 L272 120 L286 200 L300 140 L310 160 L400 160'), st('#3ad17a', 3, kesik=(18, 8), kesik_kayma=KD((0, 0), (A.op, -A.op * 3)))),
           G(yol('M90 250 C120 230 150 270 180 250 C210 230 240 270 270 250 C300 230 330 270 360 250'), st('#5ab6ff', 3, kesik=(14, 6), kesik_kayma=KD((0, 0), (A.op, -A.op * 2)))), o=o)
    A.ekle('torba', G(rc(640, 260, 150, 220, 14), fl('#f4f7fa', o=90), st('#9aa6b4', 3)), G(rc(640, 330, 134, 80, 10), gf([(0, '#f8dd6c'), (1, '#e7b82e')], (640, 290), (640, 370))),
           *[G(yol(f'M690 {180 + i * 30} L712 {180 + i * 30}'), st('#5b6676', 2)) for i in range(6)], o=o)


def a_takip(A):
    T = A.T
    zemin_kat(A, 0, 4)
    monitor(A, 0, 1)
    for i, (x, m) in enumerate([(150, 'Tansiyon'), (250, 'Nabız'), (350, 'Solunum'), (150, 'Satürasyon'), (250, 'Ateş')]):
        A.etiketler.append({'bas': round(T(0, .1 + i * .12) / FR, 2), 'son': round(T(0, 1) / FR, 2), 'x': x, 'y': 100 + (i // 3) * 220 + 0, 'metin': m, 'tur': 'bilgi'})
    A.etiket(0, 0, 640, 410, 'Saatlik / 24 saatlik idrar', 'dogru')
    # s1: serum (giren) ↔ idrar (çıkan)
    A.ekle('serum', G(rc(150, 300, 90, 130, 14), fl('#e9f3fb', o=95), st('#6b7a90', 2)), G(rc(150, 320, 76, 80, 8), fl('#9fc4ef')),
           G(yol('M150 365 L150 420 C150 450 250 450 300 430'), st('#cfd8e2', 6)), G(el(150, 380, 10, 14), fl('#5b8fc9')), o=belir(A, 1, .1, 1))
    A.etiket(1, 1, 150, 210, 'Giren sıvı', 'bilgi'); A.etiket(1, 1, 640, 410, 'Çıkan idrar', 'bilgi')
    # s2–s3: kavanozlar + organlar
    zemin_kat(A, 2, 3, 'zemin-denge')
    for b, cik, gir, organ in ((2, 2000, 1000, 'bobrek'), (3, 1000, 5000, 'akciger')):
        o = gorun(A, b, b)
        for x, v, nm, r in ((180, cik, 'Çıkan', '#e7b82e'), (360, gir, 'Giren', '#5b8fc9')):
            h = v / 5000 * 260
            A.ekle(f'kavanoz{b}{nm}', G(rc(x, 270, 120, 280, 12), fl('#f4f7fa'), st('#9aa6b4', 3)), o=o)
            A.ekle(f'sivi{b}{nm}', G(rc(x, 0, 104, h, 6), fl(r)), p=K((0, [0, 404, 0]), (T(b, .1), [0, 404, 0]), (T(b, .5), [0, 404 - h / 2, 0])),
                   s=K((0, [100, 1, 100]), (T(b, .1), [100, 1, 100]), (T(b, .5), [100, 100, 100])), a=(0, 0), o=o)
            A.etiketler.append({'bas': round(T(b, .5) / FR, 2), 'son': round(T(b, 1) / FR, 2), 'x': x, 'y': 110, 'metin': f'{nm} {v} mL', 'tur': 'bilgi'})
        if organ == 'bobrek':
            for x in (560, 680):
                A.ekle(f'bobrek{x}', G(yol(f'M{x} 180 C{x - 60} 180 {x - 60} 340 {x} 340 C{x + 40} 340 {x + 50} 300 {x + 20} 260 C{x + 50} 220 {x + 40} 180 {x} 180 Z'),
                                        fl('#b5524a'), st('#7d2f2a', 2)), o=o)
                A.ekle(f'bobrek-k{x}', G(yol(f'M{x} 180 C{x - 60} 180 {x - 60} 340 {x} 340 C{x + 40} 340 {x + 50} 300 {x + 20} 260 C{x + 50} 220 {x + 40} 180 {x} 180 Z'),
                                          fl('#5c1f1d')), o=K((0, 0), (T(b, .55), 0), (T(b, .85), 70), (T(b, 1) + 8, 70), (T(b, 1) + 16, 0)))
            A.etiket(b, b, 620, 380, 'Dehidratasyon · böbrek bozulur', 'uyari')
        else:
            for x in (560, 680):
                A.ekle(f'akc{x}', G(yol(f'M{x} 160 C{x - 50} 170 {x - 60} 300 {x - 40} 350 C{x - 10} 360 {x + 20} 350 {x + 24} 330 L{x + 24} 170 Z' if x == 560 else f'M{x} 160 C{x + 50} 170 {x + 60} 300 {x + 40} 350 C{x + 10} 360 {x - 20} 350 {x - 24} 330 L{x - 24} 170 Z'),
                                     fl('#f2b8b2'), st('#a8554e', 2)), o=o)
            A.ekle('odem', G(rc(620, 0, 230, 190, 30), fl('#5b8fc9', o=70)), p=K((0, [0, 350, 0]), (T(b, .5), [0, 350, 0]), (T(b, .9), [0, 280, 0])),
                   s=K((0, [100, 1, 100]), (T(b, .5), [100, 1, 100]), (T(b, .9), [100, 100, 100])), o=o)
            A.etiket(b, b, 620, 400, 'Akciğer ödemi · periferik ödem · KKY', 'uyari')
    kavram_ikonlar(A, 4, [(130, 200, ikon_kutu(130, 200, '#2f6fd6', [G(rc(130, 210, 100, 40, 8), fl('#9aa6b4')), G(el(100, 190, 26, 26), fl('#e9b896'))]), 'Yoğun bakım', 'bilgi'),
                          (300, 200, ikon_kutu(300, 200, '#2f6fd6', [G(yol('M260 230 L340 170'), st('#6b7a90', 8)), G(el(300, 200, 40, 40), st('#d23b3b', 5))]), 'Uzun / kanamalı ameliyat', 'bilgi'),
                          (470, 200, ikon_kutu(470, 200, '#d23b3b', [G(yol('M440 230 L470 170 L500 230 Z'), fl('#d23b3b'))]), 'Septik · hipovolemik · hemorajik şok', 'uyari'),
                          (640, 200, ikon_kutu(640, 200, '#2f6fd6', [G(el(640, 200, 60, 60), gf(DERI, (630, 190), (650, 215), radyal=True)), G(yol('M622 196 L636 196 M644 196 L658 196'), st('#3b2a1e', 3))]), 'Bilinci kapalı (inme, DKA)', 'bilgi')], 'grup')


def a_retansiyon(A):
    ic_ekle(A, LU.glob, [0, 1, None, None, None], [(0, 1)])
    ic_ekle(A, LU.idrar_akisi, [2, 2, None, None, None], [(2, 2)], 'bosalt')
    A.etiket(2, 2, 250, 440, 'Mesane boşalır, hasta rahatlar', 'dogru')
    kavram_ikonlar(A, 3, [(250, 210, ikon_kutu(250, 210, '#2f6fd6', [G(rc(250, 220, 120, 40, 8), fl('#9aa6b4')), G(el(210, 200, 30, 30), fl('#e9b896')), G(rc(290, 250, 26, 34, 5), fl('#f2cf55'))]), 'Yatağa bağımlı hasta', 'bilgi'),
                          (550, 210, ikon_kutu(550, 210, '#d23b3b', [G(rc(550, 220, 120, 40, 8), fl('#9aa6b4')), G(el(510, 200, 30, 30), fl('#e9b896')), G(yol('M570 180 L600 180 M585 165 L585 195'), st('#d23b3b', 7))]), 'Hareket ettirilemeyen travma hastası', 'uyari')], 'yatak')


def a_diger(A):
    T = A.T
    zemin_kat(A, 0, 2)
    A.ekle('mesane', G(el(320, 230, 260, 200), gf(MESANE, (280, 180), (340, 300), radyal=True), st('#a8554e', 6)), G(el(320, 230, 222, 166), gf(IDRAR, (300, 200), (330, 280), radyal=True)), o=gorun(A, 0, 2))
    A.ekle('opak', G(el(320, 230, 222, 166), fl('#ffffff', o=90)), o=K((0, 0), (T(2, .2), 0), (T(2, .6), 100), (T(2, 1) + 8, 100), (T(2, 1) + 16, 0)))
    A.ekle('kateter', G(yol('M320 250 L320 420 C320 460 400 470 470 450'), st('#8a96a6', 11)), G(yol('M320 250 L320 420 C320 460 400 470 470 450'), st('#eef2f6', 8)), o=gorun(A, 0, 2))
    A.ekle('kultur', G(rc(560, 400, 70, 90, 10), fl('#eef3f8', o=95), st('#7d8aa0', 2)), G(rc(560, 420, 60, 50, 6), fl('#f2cf55')), G(rc(560, 350, 84, 18, 4), fl('#c0392b')),
           G(yol('M470 450 C520 440 540 400 556 380'), st('#e1b300', 4, kesik=(8, 8), kesik_kayma=KD((0, 0), (A.op, -A.op * 2)))), o=gorun(A, 0, 0))
    A.etiket(0, 0, 560, 300, 'Steril kültür örneği', 'bilgi'); A.etiket(0, 0, 160, 80, 'Küçük çocuk / yaşlı', 'bilgi')
    A.ekle('enjektor', G(rc(620, 440, 150, 40, 5), fl('#eef3f8', o=95), st('#6b7a90', 2)), G(rc(600, 440, 90, 30), fl('#b48ae0')),
           o=gorun(A, 1, 1), p=K((0, [80, 0, 0]), (T(1, .1), [80, 0, 0]), (T(1, .4), [0, 0, 0])))
    A.ekle('ilac', G(yol('M545 445 L470 450 C400 470 320 460 320 420 L320 250'), st('#8e44ad', 5, kesik=(10, 10), kesik_kayma=KD((T(1, .3), 0), (T(1, 1), -300)))), o=gorun(A, 1, 1))
    A.ekle('ilac-mesane', G(el(320, 230, 222, 166), fl('#b48ae0', o=55)), o=K((0, 0), (T(1, .5), 0), (T(1, .9), 100), (T(1, 1) + 8, 100), (T(1, 1) + 16, 0)))
    A.etiket(1, 1, 620, 380, 'Kemoterapötik ilaç', 'bilgi')
    A.ekle('rontgen', G(rc(320, 230, 360, 300, 10), st('#2f6fd6', 4, kesik=(14, 8))), o=gorun(A, 2, 2))
    A.etiket(2, 2, 600, 220, 'Sistografi: opak madde', 'bilgi')
    kavram_ikonlar(A, 3, [(150, 220, ikon_kutu(150, 220, '#2e9e5b', [G(el(150, 220, 70, 70), fl('#2e9e5b'))]), '1 · İdrar yapamama', 'dogru'),
                          (400, 220, ikon_kutu(400, 220, '#2e9e5b', [G(el(400, 220, 60, 60), fl('#5aa874'))]), '2 · İdrar takibi', 'dogru'),
                          (650, 220, ikon_kutu(650, 220, '#9aa6b4', [G(el(650, 220, 46, 46), fl('#9aa6b4'))]), '3 · Kültür, ilaç, sistografi', 'bilgi')], 'sira')


def konusma(A, b, metin_x, x=520, y=120, renk='#d23b3b'):
    A.ekle('balon', G(yol(f'M{x - 150} {y - 40} L{x + 150} {y - 40} C{x + 166} {y - 40} {x + 166} {y + 40} {x + 150} {y + 40} L{x - 90} {y + 40} L{x - 130} {y + 70} L{x - 120} {y + 40} L{x - 150} {y + 40} C{x - 166} {y + 40} {x - 166} {y - 40} {x - 150} {y - 40} Z'),
                       fl('#ffffff'), st(renk, 3)), o=belir(A, b, .05, b))


def a_sistit(A):
    T = A.T
    zemin_kat(A, 0, 0)
    A.ekle('hasta0', *kisi(240, 200, '#8fc1c9', 1.3), o=gorun(A, 0, 0))
    konusma(A, 0, 0, 520, 140)
    A.etiket(0, 0, 520, 140, '"İdrar yapamıyorum"', 'uyari')
    A.ekle('tepsi', G(rc(560, 380, 220, 80, 10), fl('#c7d1da'), st('#8b96a3', 2)), G(yol('M480 380 C520 350 580 410 640 370'), st('#e3b544', 8)), o=belir(A, 0, .4, 0))
    carpi(A, 560, 380, 0, .6)
    A.etiket(0, 0, 560, 460, 'Hemen sonda takma!', 'uyari')
    ic_ekle(A, LU.glob, [None, None, None, None, 1], [(1, 2)], 'sistit')
    A.etiket(1, 1, 640, 80, 'Suprapubik ağrı · sık idrar · yanma', 'bilgi')
    A.etiket(2, 2, 640, 80, 'Retansiyon değil → değerlendir', 'uyari')
    ic_ekle(A, LU.glob, [3, 3, 3, 4, None], [(3, 4)], 'glob')
    A.etiket(3, 3, 640, 420, 'Altı aylık gebe karnı gibi kabarık', 'bilgi')
    kavram_ikonlar(A, 5, [(160, 210, ikon_kutu(160, 210, '#d23b3b', [*[G(el(130 + i * 22, 200 + (i % 2) * 22, 18, 12), fl('#5aa874'), st('#2e6e46', 1)) for i in range(4)]]), 'Enfeksiyon riski', 'uyari'),
                          (400, 210, ikon_kutu(400, 210, '#d23b3b', [G(yol('M390 160 L370 215 L400 215 L380 260 L430 195 L400 195 L420 160 Z'), fl('#e1a92e'))]), 'Günlerce ağrı', 'uyari'),
                          (640, 210, ikon_kutu(640, 210, '#d23b3b', [G(yol('M580 210 L620 210 C630 210 630 205 640 205 C650 205 650 210 660 210 L700 210'), st('#f0b8b2', 14)), G(yol('M632 196 L648 196 M632 224 L648 224'), st('#d23b3b', 4))]), 'Erkekte üretra darlığı', 'uyari')], 'sonuc')


def a_enf(A):
    T = A.T
    zemin_kat(A, 0, 0)
    A.ekle('dur', G(yol('M400 90 L470 120 L500 190 L470 260 L400 290 L330 260 L300 190 L330 120 Z'), fl('#d23b3b'), st('#8d1f1f', 4)), G(rc(400, 190, 140, 30, 6), fl('#ffffff')), o=belir(A, 0, .1, 0))
    A.etiket(0, 0, 400, 350, 'Kesin kontrendikasyon: takarsan malpraktis', 'uyari')

    def anatomi(_z):
        I = LU._IC
        LU.erkek_anatomi(I)
        return I
    ic_ekle(A, anatomi, [1], [(1, 3)], 'anatomi')
    A.ekle('prostat-ilt', G(el(300, 262, 92, 72), fl('#d23b3b', o=55), st('#8d1f1f', 3)), o=K((0, 0), (T(1, .2), 0), (T(1, .35), 100), (T(1, 1) + 8, 100), (T(1, 1) + 16, 0)),
           s=KD(*[(T(1, .2) + k * 10, [100 + (k % 2) * 8, 100 + (k % 2) * 8, 100]) for k in range(int((T(1, 1) - T(1, .2)) / 10))]), a=(300, 262), p=S([300, 262, 0]))
    A.ekle('bakteri', *[G(el(300 + dx, 262 + dy, 9, 6), fl('#2e6e46')) for dx, dy in [(-50, -20), (40, -30), (60, 10), (-60, 30), (0, -60), (20, 50)]],
           s=K((0, [40, 40, 100]), (T(1, .4), [40, 40, 100]), (T(1, .9), [260, 260, 100])), a=(300, 262), p=S([300, 262, 0]), o=gorun(A, 1, 1))
    A.etiket(1, 1, 200, 400, 'Akut prostatit / abse: bakteriyemi, sepsis', 'uyari')
    A.ekle('testis-ilt', G(el(505, 395, 90, 72), fl('#d23b3b', o=55), st('#8d1f1f', 3)), o=gorun(A, 2, 2))
    A.etiket(2, 2, 600, 470, 'Orşit · epididimit · Fournier · abse', 'uyari')
    A.ekle('mesane-kanama', *[G(el(300 + dx, 150 + dy, 8, 8), fl('#b3201f')) for dx, dy in [(-30, -10), (20, -30), (40, 20), (-40, 30), (0, 40)]], o=gorun(A, 3, 3))
    A.etiket(3, 3, 380, 40, 'Hızlı boşaltma → mukozal kanama', 'bilgi')
    tik(A, 600, 120, 3, .5)
    A.etiket(3, 3, 600, 190, 'Kontrendikasyon değil', 'dogru')
    A.kamera(1, 300, 262, 200)
    A.kamera(2, 505, 395, 190)
    A.kamera(3, 320, 170, 150)


def a_travma(A):
    ic_ekle(A, LU.travma, [0, 1, 2, 4], [(0, 2), (4, 4)])
    ic_ekle(A, LU.travma, [3, 3, None, None], [(3, 3)], 'yalniz-kirik')
    tik(A, 620, 400, 3, .5)
    A.etiket(3, 3, 600, 470, 'Meatusta kan yok → kateter takılabilir', 'dogru')
    A.etiket(4, 4, 250, 440, 'Kısmi yırtık: zorlama yırtığı tamamlar', 'uyari')


def a_malzeme(A):
    ic_ekle(A, LU.malzeme, [0, 0, 1, 2, 3, 4], [(0, 4)])
    A.ekle('uzatan-el', G(yol('M800 330 C720 320 660 300 620 280 L600 300 C640 340 720 370 800 380 Z'), fl(ELDIVEN), st('#7d8aa0', 2)),
           G(rc(600, 280, 60, 40, 6), fl('#fbfaf6'), st('#c9b48a', 1.5)), p=K((0, [200, 0, 0]), (A.T(4, .2), [200, 0, 0]), (A.T(4, .5), [0, 0, 0])), o=belir(A, 4, .2, 4))


def foley_detay(A):
    """Kateter yapısı: 7 cümlenin her biri ayrı eylem."""
    T = A.T
    zemin_kat(A, 0, 6)
    # s0: lateks ve silikon yan yana
    for y, r, k, ad in ((170, '#e3b544', '#8a6a1e', 'Lateks · kısa süreli'), (300, '#f2f5f8', '#8a96a6', 'Silikon · uzun süreli')):
        A.ekle(f'kat{y}', G(yol(f'M80 {y} L640 {y}'), st(k, 22, o=40)), G(yol(f'M80 {y} L640 {y}'), st(r, 18)), G(yol(f'M80 {y - 5} L640 {y - 5}'), st('#ffffff', 4, o=60)),
               G(el(78, y, 20, 18), fl(r), st(k, 1.5)), o=gorun(A, 0, 0), p=K((0, [-700, 0, 0]), (T(0, .05 if y == 170 else .3), [-700, 0, 0]), (T(0, .05 if y == 170 else .3) + 16, [0, 0, 0])))
        A.etiketler.append({'bas': round(T(0, .2 if y == 170 else .45) / FR, 2), 'son': round(T(0, 1) / FR, 2), 'x': 360, 'y': y - 40, 'metin': ad, 'tur': 'bilgi'})
    # s1–s5: tek kateter büyük
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
    A.etiket(1, 1, 90, 190, 'Uçtaki delikler', 'bilgi'); A.etiket(1, 1, 150, 310, 'Sabitleme balonu', 'bilgi')
    A.etiket(2, 2, 670, 330, 'Kalın drenaj kanalı → torba', 'dogru'); A.etiket(2, 2, 650, 90, 'İnce valfli balon kanalı', 'bilgi')
    # s3: torba hortumu önce balon kanalına → kırmızı çarpı, sonra drenaja
    A.ekle('hortum', G(yol('M800 420 C760 420 740 400 730 380'), st('#cfd8e2', 14)), G(rc(730, 372, 26, 30, 6), fl('#9aa6b4')),
           p=K((0, [0, 0, 0]), (T(3), [0, 0, 0]), (T(3, .25), [-60, -240, 0]), (T(3, .5), [-60, -240, 0]), (T(3, .8), [16, -120, 0])), o=gorun(A, 3, 3))
    carpi(A, 650, 140, 3, .25)
    tik(A, 760, 250, 3, .8)
    A.etiket(3, 3, 400, 420, 'Torba her zaman drenaj kanalına', 'dogru')
    # s4: enjektör balon kanalına, balon şişer, çekme oku
    A.ekle('enjektor', G(rc(0, 0, 130, 34, 4), fl('#eef3f8', o=95), st('#6b7a90', 2)), G(rc(-10, 0, 90, 26), fl('#9fc4ef')),
           p=K((0, [780, 60, 0]), (T(4, .05), [780, 60, 0]), (T(4, .25), [700, 100, 0])), r=S(-40), o=gorun(A, 4, 4))
    A.ekle('cek', G(yol('M400 330 L240 330'), st('#2f6fd6', 6)), G(yol('M262 314 L236 330 L262 346'), st('#2f6fd6', 6)), o=belir(A, 4, .75, 4))
    A.etiket(4, 4, 330, 380, 'Basit çekiştirmeyle çıkmaz', 'bilgi')
    # s5: torba + musluk
    A.ekle('torba', G(rc(560, 360, 200, 200, 14), fl('#f4f7fa', o=92), st('#9aa6b4', 3)), G(rc(560, 410, 184, 90, 10), gf([(0, '#f8dd6c'), (1, '#e7b82e')], (560, 370), (560, 450))),
           G(rc(560, 466, 30, 16, 4), fl('#6b7a90')), G(yol('M560 474 L560 500'), st('#e1b300', 6, kesik=(8, 6), kesik_kayma=KD((T(5, .4), 0), (A.op, -80)))),
           o=gorun(A, 5, 5), p=K((0, [0, 200, 0]), (T(5), [0, 200, 0]), (T(5, .2), [0, 0, 0])))
    A.etiket(5, 5, 640, 480, 'Musluktan boşaltılır', 'bilgi')
    # s6: boy ve çap
    zemin_kat(A, 6, 6, 'zemin-boy')
    for i, f in enumerate([12, 16, 20, 24]):
        A.ekle(f'eriskin{f}', G(yol(f'M120 {100 + i * 50} L680 {100 + i * 50}'), st('#8a96a6', f * 0.9 + 2)), G(yol(f'M120 {100 + i * 50} L680 {100 + i * 50}'), st('#eef2f6', f * 0.9)), o=belir(A, 6, .05 + i * .06, 6))
    for i, f in enumerate([6, 8, 10]):
        A.ekle(f'cocuk{f}', G(yol(f'M120 {330 + i * 40} L480 {330 + i * 40}'), st('#8a96a6', f + 2)), G(yol(f'M120 {330 + i * 40} L480 {330 + i * 40}'), st('#dfeaf6', f)), o=belir(A, 6, .5 + i * .06, 6))
    A.etiket(6, 6, 720, 170, 'Erişkin 12–24 Fr · boy aynı', 'bilgi'); A.etiket(6, 6, 600, 370, 'Çocuk 6–8–10 Fr · daha kısa', 'bilgi')
    A.kamera(1, 140, 250, 190)
    A.kamera(2, 640, 220, 160)
    A.kamera(3, 620, 250, 120)
    A.kamera(4, 360, 220, 110)
    A.kamera(5, 560, 330, 130)
    A.kamera(6, 400, 250, 100)


def a_iletisim(A):
    ic_ekle(A, LU.mahremiyet, [0, 2, 3], [(0, 3)])
    zemin_kat(A, 1, 1, 'zemin-onam')
    A.ekle('hekim1', *kisi(200, 170, '#ffffff', 1.3, True), o=gorun(A, 1, 1))
    konusma(A, 1, 0, 520, 130)
    A.etiketler.append({'bas': round(A.T(1, .05) / FR, 2), 'son': round(A.T(1, .5) / FR, 2), 'x': 520, 'y': 130, 'metin': '"Yatın, sonda takacağım"', 'tur': 'uyari'})
    carpi(A, 520, 130, 1, .3)
    A.etiketler.append({'bas': round(A.T(1, .55) / FR, 2), 'son': round(A.T(1, 1) / FR, 2), 'x': 520, 'y': 300, 'metin': 'Anlat + sözlü onam al', 'tur': 'dogru'})
    tik(A, 520, 380, 1, .6)
    kavram_ikonlar(A, 4, [(260, 220, ikon_kutu(260, 220, '#2e9e5b', [G(el(260, 220, 70, 70), gf(DERI, (250, 210), (270, 230), radyal=True)), G(yol('M240 230 C250 244 270 244 280 230'), st('#3b2a1e', 4))]), 'Hasta rahat', 'dogru'),
                          (540, 220, ikon_kutu(540, 220, '#2f6fd6', [G(yol('M540 170 L590 190 L586 236 C580 262 560 274 540 282 C520 274 500 262 494 236 L490 190 Z'), fl('#2f6fd6'))]), 'Medikolegal koruma', 'bilgi')], 'koruma')


def a_pozisyon(A):
    T = A.T
    zemin_kat(A, 0, 2)
    # s0: erkek, yandan sırtüstü; iç çamaşırı iner
    A.ekle('yatak0', G(rc(400, 330, 640, 60, 12), gf([(0, '#f4f7fa'), (1, '#d6dee7')], (400, 300), (400, 360)), st('#9aa6b4', 2)), G(rc(140, 290, 90, 30, 12), fl('#ffffff')), o=gorun(A, 0, 0))
    A.ekle('erkek', G(el(140, 260, 60, 56), gf(DERI, (130, 250), (150, 272), radyal=True)), G(yol('M170 270 L420 262 L640 280 L640 300 L170 300 Z'), fl('#8fc1c9'), st('#4c8590', 1.5)),
           G(yol('M420 262 L640 280 L640 300 L420 300 Z'), gf(DERI, (500, 270), (500, 300))), o=gorun(A, 0, 0))
    A.ekle('camasir', G(rc(0, 0, 70, 40, 6), fl('#5b6676')), p=K((0, [430, 282, 0]), (T(0, .4), [430, 282, 0]), (T(0, .8), [520, 288, 0])), o=gorun(A, 0, 0))
    A.etiket(0, 0, 400, 200, 'Supin: sırtüstü', 'bilgi')
    # s1–s2: kadın, üstten; dizler bükülür, topuklar yatakta, bacaklar V
    A.ekle('yatak1', G(rc(400, 260, 620, 300, 16), gf([(0, '#f4f7fa'), (1, '#d6dee7')], (400, 120), (400, 400)), st('#9aa6b4', 2)), o=gorun(A, 1, 2))
    A.ekle('kadin', G(el(160, 260, 60, 56), gf(DERI, (150, 250), (170, 270), radyal=True)), G(yol('M190 220 L400 216 C412 216 416 304 400 304 L190 300 Z'), fl('#8fc1c9'), st('#4c8590', 1.5)), o=gorun(A, 1, 2))
    for s, (d1, d2) in enumerate([('M400 236 L520 236 L640 236', 'M400 236 L500 170 L620 150'), ('M400 284 L520 284 L640 284', 'M400 284 L500 350 L620 370')]):
        A.ekle(f'bacak{s}', G(yol_morph(d1, d2, T(2, .1), T(2, .6)), st('#b9805a', 30)), G(yol_morph(d1, d2, T(2, .1), T(2, .6)), st('#e9b896', 26)), o=gorun(A, 1, 2))
    A.ekle('diz', G(el(0, 0, 30, 30), fl('#d9a07c')), p=K((0, [520, 236, 0]), (T(2, .1), [520, 236, 0]), (T(2, .6), [500, 170, 0])), o=belir(A, 2, .3, 2))
    A.ekle('diz2', G(el(0, 0, 30, 30), fl('#d9a07c')), p=K((0, [520, 284, 0]), (T(2, .1), [520, 284, 0]), (T(2, .6), [500, 350, 0])), o=belir(A, 2, .3, 2))
    A.ekle('V', G(yol('M640 150 L420 260 L640 370'), st('#2f6fd6', 4, kesik=(12, 8))), o=belir(A, 2, .65, 2))
    A.etiket(1, 1, 400, 80, 'Modifiye litotomi', 'bilgi'); A.etiket(2, 2, 680, 260, 'Dizler bükük · topuklar yatakta · V', 'dogru')


def a_kadin_anatomi(A):
    T = A.T
    vulva(A, 0, 4, ayir=(T(1, 0), T(1, .5)), parmak=(T(4, .1), T(4, .6)))
    A.etiket(0, 0, 160, 130, 'Labium majus', 'bilgi'); A.etiket(0, 0, 230, 240, 'Labium minus', 'bilgi')
    A.etiket(1, 1, 520, 118, 'Klitoris', 'bilgi'); A.etiket(1, 1, 560, 205, 'Meatus (≈1 cm altında)', 'dogru')
    A.etiket(2, 2, 560, 310, 'Vajina', 'bilgi')
    A.etiket(3, 3, 400, 470, 'Kız bebek, çocuk: anatomiyi kesin bil', 'uyari')
    A.etiket(4, 4, 400, 470, 'Gerçek dokuda yumuşak açılır', 'bilgi')
    A.ekle('meatus-vurgu', G(el(400, 208, 46, 38), st('#2e9e5b', 4)), o=belir(A, 1, .4, 1))
    A.kamera(1, 400, 200, 170)
    A.kamera(2, 400, 280, 150)
    A.kamera(3, 400, 250, 100)


def a_kadin_temizlik(A):
    ic_ekle(A, LU.kadin_temizlik, [0, 1, 1, 2, 3], [(0, 3)])
    zemin_kat(A, 4, 4, 'zemin-uzat')
    A.ekle('ortu4', G(rc(400, 380, 800, 240), fl('#3b7bb8', o=75)), o=gorun(A, 4, 4))
    A.ekle('paket', G(rc(0, 0, 160, 110, 8), fl('#fbfaf6'), st('#c9b48a', 2)), G(yol('M-70 -10 C-30 -40 30 20 70 -10'), st('#e3b544', 7)),
           p=K((0, [760, 200, 0]), (A.T(4, .1), [760, 200, 0]), (A.T(4, .45), [420, 300, 0])), o=gorun(A, 4, 4))
    A.ekle('yardimci-eli', G(yol('M800 160 C700 170 620 180 560 200 L560 230 C640 240 720 250 800 250 Z'), fl(ELDIVEN), st('#7d8aa0', 2)),
           p=K((0, [260, 0, 0]), (A.T(4, .1), [260, 0, 0]), (A.T(4, .45), [-60, 100, 0])), o=gorun(A, 4, 4))
    A.etiket(4, 4, 420, 420, 'Yardımcı steril paketi uzatır', 'bilgi')


def a_kadin_yerlestirme(A):
    T = A.T
    jel_ucuna(A, 0)
    avuc_kateter(A, 1)
    A.etiket(1, 1, 400, 460, 'Avuçta halka: uç hiçbir yere değmez', 'dogru')
    vulva(A, 2, 2, ayir=(T(2, .05), T(2, .35)), parmak=(T(2, .05), T(2, .35)))
    A.ekle('giren-kateter', G(yol('M640 520 C560 400 460 270 404 212'), st('#8a6a1e', 12, o=45), tm(K((0, 0), (T(2, .45), 0), (T(2, .9), 100)))),
           G(yol('M640 520 C560 400 460 270 404 212'), st('#e3b544', 9), tm(K((0, 0), (T(2, .45), 0), (T(2, .9), 100)))), o=gorun(A, 2, 2))
    A.etiket(2, 2, 600, 160, 'Sol el ayırır · sağ el iter', 'bilgi')
    ic_ekle(A, LU.kadin_ilerleyis, [3, 3, 3, 3, 4, 4], [(3, 4)], 'ilerle')


def a_erkek_temizlik(A):
    ic_ekle(A, LU.erkek_jel, [0, 1, 3, 3, 4], [(0, 1), (3, 4)])
    zemin_kat(A, 2, 2, 'zemin-kiyas')
    T = A.T
    A.ekle('kadin-u', G(yol('M140 160 L300 160'), st('#f0b8b2', 16)), G(el(300, 160, 26, 26), fl('#e3b544')), G(el(300, 160, 40, 26), fl('#cfe9ff', o=70)), o=gorun(A, 2, 2))
    A.ekle('erkek-u', G(yol('M140 330 L700 330'), st('#f0b8b2', 16)), G(yol('M140 330 L700 330'), st('#8fc7ff', 14, o=70), tm(K((0, 0), (T(2, .4), 0), (T(2, .9), 100)))), o=gorun(A, 2, 2))
    A.etiket(2, 2, 220, 110, 'Kadın: kısa üretra · uca jel', 'bilgi'); A.etiket(2, 2, 420, 400, 'Erkek: uzun üretra · jelin tamamı', 'dogru')


def a_erkek_yerlestirme(A):
    avuc_kateter(A, 0, renk='#f2f5f8', kenar='#8a96a6', steril=True)
    A.etiket(0, 0, 400, 460, 'Avuca dola · uçtan gevşek tutma', 'uyari')
    ic_ekle(A, LU.erkek_ilerleyis, [1, 1, 1, 2, 2, 2, 3, 4], [(1, 4)])
    A.etiket(2, 2, 400, 470, 'Makette takılabilir · gerçek hastada daha kolay', 'bilgi')


def a_idrar_gelmezse(A):
    ic_ekle(A, LU.yikama, [0, 2, 2, 3, 4, 4], [(0, 0), (2, 4)])
    ic_ekle(A, LU.yanlis_balon, [1, None, None, None, None], [(1, 1)], 'kivrim')
    A.etiket(1, 1, 200, 60, '1) Mesane boş  ·  2) Kateter kıvrıldı', 'bilgi')
    ic_ekle(A, LU.yanlis_balon, [None, 5, 5, 6, 6], [(5, 6)], 'yanlis')


def a_sabitleme(A):
    ic_ekle(A, LU.balon, [0, 0, 0, 0, 1, 1], [(0, 1)])
    ic_ekle(A, LU.idrar_akisi, [2, 2, 2, None, None], [(2, 2)], 'torba')
    A.ekle('kultur', G(rc(470, 300, 60, 80, 8), fl('#eef3f8', o=95), st('#7d8aa0', 2)), G(rc(470, 320, 50, 40, 6), fl('#f2cf55')), G(rc(470, 256, 70, 16, 4), fl('#c0392b')),
           o=belir(A, 2, .6, 2))
    A.etiket(2, 2, 470, 380, 'Gerekirse kültür örneği', 'bilgi')
    zemin_kat(A, 3, 4, 'zemin-kayit')
    T = A.T
    A.ekle('form', G(rc(330, 250, 300, 380, 12), fl('#ffffff'), st('#9aa6b4', 2)), G(rc(330, 70, 120, 24, 6), fl('#9aa6b4')),
           *[G(yol(f'M210 {130 + i * 50} L450 {130 + i * 50}'), st('#2f6fd6', 4), tm(K((0, 0), (T(3, .1 + i * .18), 0), (T(3, .25 + i * .18), 100)))) for i in range(5)], o=gorun(A, 3, 3))
    for i, m in enumerate(['Kateter türü · boyu', 'Balon hacmi', 'İdrar miktarı · görünümü', 'Güçlük', 'Komplikasyon']):
        A.etiketler.append({'bas': round(T(3, .1 + i * .18) / FR, 2), 'son': round(T(3, 1) / FR, 2), 'x': 600, 'y': 130 + i * 50, 'metin': m, 'tur': 'bilgi'})
    A.ekle('hasta', *kisi(260, 200, '#8fc1c9', 1.3), o=gorun(A, 4, 4))
    A.ekle('yanma', G(yol('M300 360 C290 340 300 320 310 300 C320 320 334 330 330 350 C326 366 306 372 300 360 Z'), fl('#e1a92e')), o=belir(A, 4, .2, 4))
    A.ekle('hekim', *kisi(560, 200, '#ffffff', 1.3, True), o=gorun(A, 4, 4))
    A.etiket(4, 4, 420, 120, 'Birkaç gün yanma olabilir — önceden anlat', 'bilgi')


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
