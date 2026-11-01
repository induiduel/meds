"""KMB adım videoları — 2B düz çizgi film hattı, GRUP C2 (adim2b.py bunları toplar).
Adımlar: kontrendikasyon-travma, malzeme, kateter-yapisi, iletisim, pozisyon, kadin-anatomi.
Her cümle bir bölümdür (ses `o-<adım>`); anatomi/araç/figür 2B sahnelerden (Sahne2B: travma, malzeme, foley, foley-kesit,
pozisyon, kadin, yakin-kadin), konu videoları alt kompozisyon (ic_ekle2b: uret2b_a.travma / mahremiyet). Burada yalnız
koreografi yazılır (docs/KMB_2B_STIL.md); sahne yazıları Lottie'ye geçmediğinden ölçek/ad bilgisi etiketle verilir.
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ortak2b import *  # noqa: E402,F401,F403
from lottie_dsl import yumruk  # noqa: E402  (eldivenli el, 2B palet)
import uret2b_a as U  # noqa: E402

# uret2b_a._son(A) yalnız Anim'i tanır (A.bolumler); alt kompozisyonda (lottie_dsl.Ic) harita uzunluğu kullanılır —
# Ic.T(i ≥ len(harita)) zaten "video sonuna dek" demektir. uret2b_a.py'ye dokunulmadan burada genişletilir.


def _katmanlar(s: Sahne2B):
    return [(k['id'], k['nm'], copy.deepcopy(k['it'])) for k in s.katmanlar]


def _kart(cx, cy, w, h, kenar, *ic, o=92):
    """Düz stil bilgi kartı: beyaz yuvarlak dikdörtgen + renkli kontur, içinde ikon."""
    return [G(rc(cx, cy, w, h, 14), fl('#ffffff', o=o), st(kenar, 2.5)), *ic]


def _konusma(x, y, w, h, renk):
    """Konuşma balonu (kuyruk sol-altta): (x, y) merkez."""
    L, R, T_, B_ = x - w / 2, x + w / 2, y - h / 2, y + h / 2
    d = (f'M{L + 14} {T_} L{R - 14} {T_} C{R} {T_} {R} {T_ + 14} {R} {T_ + 14} L{R} {B_ - 14} C{R} {B_} {R - 14} {B_} {R - 14} {B_} '
         f'L{L + 40} {B_} L{L + 10} {B_ + 26} L{L + 24} {B_} L{L + 14} {B_} C{L} {B_} {L} {B_ - 14} {L} {B_ - 14} L{L} {T_ + 14} C{L} {T_} {L + 14} {T_} {L + 14} {T_} Z')
    return G(yol(d), fl('#ffffff'), st(renk, 3))


# ———————————————————————— 1. Kontrendikasyon: üretra travması (travma sahnesi + travma konu videosu)

def a_travma(A):
    T = A.T
    # s0 darbe (Kuvvet), s1 kırık, s2 meatusta kan → kontrendike, s4 kısmi yırtık + kateter itilir (Karar)
    ic_ekle2b(A, U.travma, [0, 1, 2, 4], [(0, 2), (4, 4)])
    A.etiketler[:] = [e for e in A.etiketler if e['metin'] != 'Yüksekten düşme · kaza']  # nedenler 1. cümlede
    et(A, 0, 560, 60, 'Künt ya da penetran darbe', 'uyari', .1)
    # s1: üç neden kartı (yüksekten düşme, trafik kazası, ata biner gibi düşme) — pelvisin üstünde, kırık belirirken
    kartlar = [
        (150, [G(yol('M120 62 L120 140 M146 62 L146 140'), st('#8a6a3a', 4)), *[G(yol(f'M120 {72 + j * 17} L146 {72 + j * 17}'), st('#8a6a3a', 3)) for j in range(5)],
               G(el(186, 74, 16, 16), fl('#e9b896'), st('#b9805a', 1.5)), G(yol('M186 82 L186 110 M186 92 L172 104 M186 92 L200 104 M186 110 L176 130 M186 110 L198 130'), st('#3e4a58', 4)),
               G(yol('M212 70 L212 132'), st(KIRMIZI, 4)), G(yol('M202 120 L212 136 L222 120 Z'), fl(KIRMIZI))], 'Yüksekten düşme'),
        (400, [G(rc(400, 112, 118, 36, 12), fl(MAVI), st('#1f4e9c', 2)), G(rc(392, 88, 66, 26, 8), fl('#9cc6ff'), st('#1f4e9c', 2)),
               G(el(366, 132, 24, 24), fl('#2b2f36')), G(el(434, 132, 24, 24), fl('#2b2f36')), G(el(366, 132, 10, 10), fl('#9aa6b4')), G(el(434, 132, 10, 10), fl('#9aa6b4')),
               G(yol('M330 70 L352 92 M352 70 L330 92'), st(KIRMIZI, 4))], 'Trafik kazası'),
        (650, [G(yol('M590 118 L710 118'), st('#8a6a3a', 10)), G(el(650, 62, 18, 18), fl('#e9b896'), st('#b9805a', 1.5)),
               G(yol('M650 71 L650 104 M650 104 L622 134 M650 104 L678 134 M650 80 L630 96 M650 80 L670 96'), st('#3e4a58', 5)),
               G(yol('M650 40 L650 56'), st(KIRMIZI, 4)), G(yol('M642 52 L650 64 L658 52 Z'), fl(KIRMIZI))], 'Ata biner gibi düşme'),
    ]
    for i, (x, ic, m) in enumerate(kartlar):
        A.ekle(f'neden{i}', *_kart(x, 100, 170, 112, KIRMIZI, *ic), o=belir(A, 1, .06 + i * .14, 1), p=S([0, 0, 0]))
        et(A, 1, x, 172, m, 'uyari', .08 + i * .14)
    A.kamera_sabit(1, 1, 400, 250, 100)
    # s3: yalnız kırık (darbe + kırık olmuş bitmiş), meatusta kan YOK → kateter takılır
    ic_ekle2b(A, U.travma, ['once', 'once', None, None], [(3, 3)], 'yalniz-kirik')
    A.kamera_sabit(3, 3, 400, 273, 110)
    A.ekle('kan-yok', G(el(400, 486, 52, 40), st(YESIL, 4, kesik=(8, 6))), o=belir(A, 3, .3, 3))
    tik(A, 600, 300, 3, .55)
    et(A, 3, 250, 346, 'Pelvis kırığı var', 'bilgi', .05)
    et(A, 3, 560, 440, 'Meatusta kan yok', 'dogru', .3)
    et(A, 3, 600, 240, 'Kateter rahatlıkla takılır', 'dogru', .55)
    # s4: Karar bölümü (kateter yırtığa dayanır → ÇARPI) + başka yöntem notu
    et(A, 4, 560, 440, 'Başka yöntemle yaklaşılır', 'bilgi', .7)


# ———————————————————————— 2. Malzemeler ve steril alan (malzeme sahnesi)

def a_malzeme(A):
    T = A.T
    s = Sahne2B('malzeme')
    s.ekle(A, haric=s.ids())  # yalnız tepsi + valf renk kutusu; ögeler cümle cümle tepsiye iner
    gruplar = [(0, ['m-lateks', 'm-silikon', 'm-nonsteril', 'm-steril']), (1, ['m-jel']), (2, ['m-izotonik', 'm-enjektor', 'm-genis']),
               (3, ['m-antiseptik', 'm-ortu', 'm-torba'])]
    for b, ids in gruplar:
        for j, i in enumerate(ids):
            x, y, w, h = s.bbox(i)
            k = T(b, .04 + .14 * j)
            A.ekle(i, *s.katman(i), p=K((0, [0, -28, 0]), (k, [0, -28, 0]), (k + 12, [0, 0, 0])), o=A.gor(k))
            A.ekle(f'halka-{i}', G(el(x + w / 2, y + h / 2, w + 18, h + 18), st(SARI, 4, kesik=(10, 7))),
                   o=K((0, 0), (k + 10, 0), (k + 18, 100), (T(b, .95), 100), (T(b, 1), 0)))
    # s0: kateter boyu + eldivenler
    et(A, 0, 205, 14, 'Uygun boy: erişkin 12–24 Fr', 'bilgi', .05)
    et(A, 0, 500, 196, 'Steril olmayan: temizlik', 'bilgi', .35)
    et(A, 0, 690, 196, 'Steril: yerleştirme', 'dogru', .5)
    # s1: jel — kayganlık + lidokain anestezisi
    et(A, 1, 102, 214, 'Tek kullanımlık lidokainli jel', 'bilgi', .1)
    et(A, 1, 300, 290, 'Kayganlaştırır + anestezi', 'dogru', .45)
    # s2: izotonik + enjektör (balon), geniş uçlu enjektör (yer sınaması)
    et(A, 2, 300, 186, 'Balon: izotonik + enjektör', 'bilgi', .1)
    et(A, 2, 640, 200, 'İdrar gelmezse: geniş uçlu', 'uyari', .5)
    # s3: antiseptik + gazlı bez, delikli örtü, torba
    et(A, 3, 90, 345, 'Antiseptik + gazlı bez', 'bilgi', .1)
    et(A, 3, 330, 300, 'Steril delikli örtü', 'bilgi', .3)
    et(A, 3, 560, 345, 'İdrar torbası', 'bilgi', .5)
    # s4: steril alan çerçevesi; yardımcının mavi (steril olmayan) eli alanın DIŞINDA paketi uzatır, steril el alanın içinde
    A.ekle('steril-alan', *s.katman('m-steril-alan'), o=belir(A, 4, .05))
    A.ekle('paket', G(rc(0, 0, 120, 70, 6), fl('#fbfaf6'), st('#c9b48a', 2)), G(yol('M-44 -20 L44 -20 L44 -14 L-44 -14 Z'), fl('#e8e0cc'), st('#c9b48a', 1.5)),
           G(yol('M-40 14 C-10 -20 10 30 40 6'), st(KATETER[0], 7)), G(yol('M-40 14 C-10 -20 10 30 40 6'), st(KATETER[1], 9, o=35)),
           p=K((0, [860, 250, 0]), (T(4, .08), [860, 250, 0]), (T(4, .38), [700, 250, 0])), o=belir(A, 4, .08, 4))
    A.ekle('yardimci-el', yumruk(0, 0, .7, 180, steril=False), p=K((0, [920, 250, 0]), (T(4, .08), [920, 250, 0]), (T(4, .38), [772, 250, 0])), o=belir(A, 4, .08, 4))
    A.ekle('steril-el', yumruk(0, 0, .7, 0, steril=True), p=K((0, [420, 560, 0]), (T(4, .42), [420, 560, 0]), (T(4, .7), [470, 200, 0])), o=belir(A, 4, .42, 4))
    et(A, 4, 560, 42, 'Yardımcı paketi açar, uzatır', 'bilgi', .15)
    et(A, 4, 440, 342, 'Steril el: yalnız steril alan', 'dogru', .55)
    A.kamera(0, 400, 120, 140)
    A.kamera(1, 210, 272, 180)
    A.kamera(2, 520, 272, 140)
    A.kamera(3, 300, 292, 120)
    A.kamera(4, 400, 250, 100)


# ———————————————————————— 3. Kateterin yapısı, boyu, kalış süresi (foley + foley-kesit sahneleri)

def a_kateter_yapisi(A):
    T = A.T
    s = Sahne2B('foley')
    son6 = gorun(A, 0, 5)  # foley sahnesi 0–5; 6. cümlede Fr ölçeği (foley-kesit)
    for i, nm, it in _katmanlar(s):
        if i == 'f-balon':
            A.ekle(nm, *it, a=(134, 200), p=S([134, 200, 0]), s=K((0, [30, 30, 100]), (T(4, .45), [30, 30, 100]), (T(4, .75), [100, 100, 100])),
                   o=K((0, 0), (T(4, .45), 0), (T(4, .5), 100), (T(5, 1), 100), (T(5, 1) + 8, 0)))
        elif i == 'f-balon-sonuk':
            A.ekle(nm, *it, o=K((0, 100), (T(4, .45), 100), (T(4, .55), 0)))
        elif i == 'f-enjektor':
            A.ekle(nm, *it, p=K((0, [120, -120, 0]), (T(4, .05), [120, -120, 0]), (T(4, .3), [0, 0, 0])), o=belir(A, 4, .05, 5))
        elif i in ('f-torba', 'f-musluk'):
            A.ekle(nm, *it, p=K((0, [0, 160, 0]), (T(3, .02), [0, 160, 0]), (T(3, .22), [0, 0, 0])), o=belir(A, 3, .02, 5))
        elif i == 'f-torba-bag':
            A.ekle(nm, *it, o=belir(A, 3, .78, 5))
        else:
            A.ekle(nm, *it, o=son6)
    # s0: sarı lateks (sahnedeki kateter) + beyaz silikon kateter (altta, aynı boy)
    A.ekle('silikon', *kateter_cizgi('M80 330 L560 330', 8, SILIKON), G(yol('M80 320 C58 320 52 326 52 330 C52 334 58 340 80 340 Z'), fl(SILIKON[0]), st(SILIKON[1], 2)),
           G(el(92, 326, 12, 7), fl('#4a4a4a', o=70)), o=belir(A, 0, .3, 0))
    halka(A, 330, 200, 300, 40, 0, f1=.05, f2=.5)
    et(A, 0, 330, 140, 'Sarı: lateks, kısa süreli', 'bilgi', .08)
    et(A, 0, 330, 380, 'Beyaz: silikon, uzun süreli', 'bilgi', .4)
    # s1: uçtaki delikler + sönük sabitleme balonu
    halka(A, 93, 200, 44, 30, 1, renk=MAVI, f1=.05, f2=.6, nm='halka-delik')
    halka(A, 134, 200, 60, 32, 1, f1=.45, f2=.98, nm='halka-balon')
    et(A, 1, 110, 150, 'Uçtaki idrar delikleri', 'bilgi', .05)
    et(A, 1, 200, 244, 'Sabitleme balonu (sönük)', 'bilgi', .45)
    # s2: arka uçta iki kanal — kalın drenaj (yeşil), ince valfli balon kanalı (mavi)
    halka(A, 663, 200, 70, 24, 2, renk=YESIL, f1=.05, f2=.98, nm='halka-drenaj')
    halka(A, 649, 153, 56, 54, 2, renk=MAVI, f1=.45, f2=.98, nm='halka-bkanal')
    et(A, 2, 560, 260, 'Kalın drenaj kanalı → torba', 'dogru', .1)
    et(A, 2, 540, 90, 'İnce valfli balon kanalı', 'bilgi', .5)
    # s3: torba hortumu önce balon kanalına yönelir (ÇARPI), sonra drenaj kanalına takılır (bağ belirir, TİK)
    A.ekle('hortum-ucu', G(yol('M0 0 L0 40'), st('#cfd8e2', 10)), G(rc(0, -8, 22, 22, 4), fl('#9aa6b4'), st('#5b6676', 1.5)),
           p=K((0, [690, 300, 0]), (T(3, .22), [690, 300, 0]), (T(3, .38), [700, 112, 0]), (T(3, .55), [700, 112, 0]), (T(3, .72), [724, 206, 0])),
           o=K((0, 0), (T(3, .22), 0), (T(3, .26), 100), (T(3, .74), 100), (T(3, .78), 0)))
    A.ekle('carpi-bkanal', G(yol('M674 86 L726 138 M726 86 L674 138'), st(KIRMIZI, 8)),
           o=K((0, 0), (T(3, .4), 0), (T(3, .44), 100), (T(3, .56), 100), (T(3, .6), 0)))
    tik(A, 760, 260, 3, .8)
    et(A, 3, 560, 90, 'Balon kanalına DEĞİL', 'uyari', .35)
    et(A, 3, 560, 260, 'Torba drenaj kanalına', 'dogru', .78)
    # s4: enjektörden balon kanalına izotonik (mavi akış) → balon şişer → çekiştirme oku
    akis(A, 'M706 100 L646 180 L560 200 L136 200', T(4, .12), T(4, .6), renk=MAVI, w=2.5, nm='izotonik', o=A.gor(T(4, .12), T(4, .62)))
    ok(A, 'M330 250 L230 250', 4, renk=MAVI, w=5, f1=.78, f2=.98, nm='ok-cek')
    et(A, 4, 560, 90, 'Balon kanalı → izotonik', 'bilgi', .1)
    et(A, 4, 150, 150, 'Balon şişti', 'dogru', .55)
    et(A, 4, 300, 300, 'Çekiştirmeyle çıkmaz', 'dogru', .8)
    # s5: torbanın altında musluk; hemşire boşaltır
    halka(A, 679, 475, 44, 34, 5, renk=MAVI, f1=.05, f2=.6, nm='halka-musluk')
    A.ekle('bosalt', G(yol('M680 490 L680 540'), st(IDRAR, 4, kesik=(8, 7), kesik_kayma=KD((0, 0), (A.op, -A.op * 3)))), o=belir(A, 5, .45, 5))
    et(A, 5, 560, 340, 'Altta boşaltma musluğu', 'bilgi', .05)
    et(A, 5, 560, 385, 'Hemşire torbayı boşaltır', 'bilgi', .5)
    # s6: Fr ölçeği (foley-kesit: erişkin 12–24 aynı boy, çocuk 6–8–10 daha kısa); lümen kesiti hariç, ölçek sola kaydırılır
    k = Sahne2B('foley-kesit')
    g6 = gorun(A, 6, 6)
    A.ekle('olcek-eriskin', *k.katman('c-olcek-eriskin'), p=S([-180, 0, 0]), o=g6)
    A.ekle('olcek-cocuk', *k.katman('c-olcek-cocuk'), p=S([-180, 0, 0]), o=g6)
    for i, (y, x1, x2, w) in enumerate([(112, 250, 580, 7), (378, 314, 450, 4.5)]):
        A.ekle(f'boy{i}', *kateter_cizgi(f'M{x1} {y} L{x2} {y}', w, KATETER if i == 0 else SILIKON),
               G(yol(f'M{x1} {y - w} C{x1 - 16} {y - w} {x1 - 20} {y} {x1 - 20} {y} C{x1 - 20} {y} {x1 - 16} {y + w} {x1 + 0} {y + w} Z'),
                 fl((KATETER if i == 0 else SILIKON)[0]), st((KATETER if i == 0 else SILIKON)[1], 1.5)),
               o=belir(A, 6, .1 + i * .45, 6))
    et(A, 6, 420, 60, 'Erişkin 12–24 Fr: boy aynı', 'bilgi', .1)
    et(A, 6, 420, 330, 'Çocuk 6–8–10 Fr: daha kısa', 'bilgi', .55)
    A.kamera(0, 330, 250, 120)
    A.kamera(1, 182, 200, 220)
    A.kamera(2, 533, 170, 150)
    A.kamera(3, 560, 273, 110)
    A.kamera(4, 400, 220, 110)
    A.kamera(5, 560, 308, 130)
    A.kamera(6, 400, 250, 100)


# ———————————————————————— 4. İletişim, onam, mahremiyet (mahremiyet konu videosu + pozisyon sahnesi)

def a_iletisim(A):
    T = A.T
    # s0 tanış/onam, s2 paravan, s3 yardımcı personel (mahremiyet bölümleri)
    ic_ekle2b(A, U.mahremiyet, [0, 2, 3], [(0, 0), (2, 3)])
    et(A, 0, 420, 92, 'Anlayacağı dille anlat', 'bilgi', .45)
    # s1: hekim (pozisyon sahnesi) + kötü örnek balonu (ÇARPI) → iyi örnek balonu (onam ✓)
    s = Sahne2B('pozisyon')
    A.ekle('yatak1', *[g for k in s.katmanlar if not k['id'] for g in copy.deepcopy(k['it'])], o=gorun(A, 1, 1))
    A.ekle('erkek1', *s.katman('p-erkek'), o=gorun(A, 1, 1))
    A.ekle('hekim1', *s.katman('p-hekim'), o=gorun(A, 1, 1))
    A.ekle('balon-kotu', _konusma(290, 70, 290, 64, KIRMIZI), o=K((0, 0), (T(1, .04), 0), (T(1, .1), 100), (T(1, .5), 100), (T(1, .54), 0)))
    et(A, 1, 290, 70, '"Yatın, sonda takacağım"', 'uyari', .08, .5)
    carpi(A, 290, 70, 1, .3, r=26, son=None)
    A.ekle('balon-iyi', _konusma(290, 70, 290, 64, YESIL), o=K((0, 0), (T(1, .56), 0), (T(1, .62), 100), (T(1, 1), 100), (T(1, 1) + 6, 0)))
    et(A, 1, 290, 70, 'Güzelce anlat · sözlü onam', 'dogru', .6)
    tik(A, 450, 70, 1, .75)
    A.kamera_sabit(1, 1, 267, 180, 150)
    # s3: ek not — erkek hekim kadın/çocuk hastaya takarken kadın personel
    et(A, 3, 520, 120, 'Erkek hekim: kadın personel', 'bilgi', .5)
    # s4: iki kavram kartı — hasta rahat (yüz), medikolegal koruma (kalkan)
    A.ekle('kart-rahat', *_kart(220, 220, 170, 150, YESIL, G(el(220, 212, 72, 72), gf(DERI, (210, 200), (230, 224), radyal=True), st('#b9805a', 2)),
                                G(el(206, 204, 6, 6), fl('#3b2a1e')), G(el(234, 204, 6, 6), fl('#3b2a1e')), G(yol('M202 226 C210 240 230 240 238 226'), st('#a8705f', 3.5))),
           o=belir(A, 4, .08, 4))
    A.ekle('kart-koruma', *_kart(580, 220, 170, 150, MAVI, G(yol('M580 164 L630 184 L626 230 C620 256 600 268 580 276 C560 268 540 256 534 230 L530 184 Z'), fl(MAVI), st('#1f4e9c', 2)),
                                 G(yol('M560 222 L574 236 L602 206'), st('#ffffff', 6))), o=belir(A, 4, .4, 4))
    et(A, 4, 220, 320, 'Hasta rahat hisseder', 'dogru', .12)
    et(A, 4, 580, 320, 'Medikolegal koruma', 'bilgi', .45)
    A.kamera_sabit(4, 4, 400, 250, 100)


# ———————————————————————— 5. Pozisyon: erkekte supin, kadında modifiye litotomi (pozisyon sahnesi)

def a_pozisyon(A):
    T = A.T
    s = Sahne2B('pozisyon')
    A.ekle('yataklar', *[g for k in s.katmanlar if not k['id'] for g in copy.deepcopy(k['it'])])
    A.ekle('erkek', *s.katman('p-erkek'))
    # s0: iç çamaşırı işlem alanını açacak kadar indirilir (kalçadan uyluğa kayar)
    A.ekle('camasir', G(rc(0, 0, 54, 44, 8), fl('#5b6676'), st('#3e4a58', 2)), G(yol('M-27 -8 L27 -8'), st('#8a96a6', 2)),
           p=K((0, [418, 150, 0]), (T(0, .4), [418, 150, 0]), (T(0, .8), [500, 152, 0])), o=gorun(A, 0, 0))
    halka(A, 406, 152, 236, 64, 0, renk=MAVI, f1=.05, f2=.4, nm='halka-supin')
    et(A, 0, 300, 60, 'Supin: sırtüstü', 'bilgi', .05)
    et(A, 0, 560, 230, 'İç çamaşırı indirilir', 'bilgi', .45)
    # s1: kadın hasta belirir — sırtüstü, modifiye litotomi
    A.ekle('kadin', *s.katman('p-kadin'), o=belir(A, 1, .02))
    halka(A, 398, 370, 236, 110, 1, renk=MAVI, f1=.15, f2=.5, nm='halka-kadin')
    et(A, 1, 300, 240, 'Sırtüstü yatar', 'bilgi', .1)
    et(A, 1, 400, 470, 'Modifiye litotomi', 'dogru', .5)
    # s2: dizler bükülü (halkalar), topuklar yatakta, bacaklar V (çizilir)
    A.ekle('v', *s.katman('p-v'), o=belir(A, 2, .55))
    halka(A, 528, 322, 44, 40, 2, f1=.05, f2=.5, nm='halka-diz1')
    halka(A, 522, 438, 44, 40, 2, f1=.05, f2=.5, nm='halka-diz2')
    halka(A, 604, 334, 36, 32, 2, renk=YESIL, f1=.3, f2=.7, nm='halka-topuk1')
    halka(A, 600, 446, 36, 32, 2, renk=YESIL, f1=.3, f2=.7, nm='halka-topuk2')
    et(A, 2, 430, 250, 'Dizler bükülür', 'bilgi', .05)
    et(A, 2, 630, 250, 'Topuklar yatağa basar', 'bilgi', .3)
    et(A, 2, 300, 300, 'Bacaklar V şeklinde açılır', 'dogru', .6)
    A.kamera(0, 406, 160, 160)
    A.kamera(1, 400, 292, 120)
    A.kamera(2, 480, 322, 140)


# ———————————————————————— 6. Kadında meatusu bulmak (kadin + yakin-kadin sahneleri)

def a_kadin_anatomi(A):
    T = A.T
    k = Sahne2B('kadin')
    k.ekle(A, o=gorun(A, 0, 0))  # s0: dış görünüm — labium majus / minus
    halka(A, 400, 270, 128, 196, 0, f1=.05, f2=.5, nm='halka-majus')
    halka(A, 400, 266, 70, 150, 0, renk=MAVI, f1=.45, f2=.98, nm='halka-minus')
    et(A, 0, 230, 180, 'Dışta: labium majus', 'bilgi', .05)
    et(A, 0, 580, 300, 'İçte: labium minus', 'bilgi', .45)
    v = Sahne2B('yakin-kadin')
    v.ekle(A, o=gorun(A, 1, 4))  # s1–s4: yakın plan — klitoris, meatus (üstte), vajina (altta)
    # s1: klitoris → ≈1 cm aşağıda, minusların arasında üstteki küçük açıklık = meatus
    halka(A, 400, 40, 90, 60, 1, renk=MAVI, f1=.05, f2=.45, nm='halka-klitoris')
    ok(A, 'M470 70 L470 150', 1, renk=MAVI, w=4, f1=.3, f2=.98, nm='ok-1cm')
    halka(A, 400, 170, 70, 50, 1, renk=YESIL, f1=.5, f2=.98, nm='halka-meatus')
    et(A, 1, 560, 50, 'Klitoris', 'bilgi', .05)
    et(A, 1, 620, 110, '≈1 cm aşağısı', 'bilgi', .3)
    et(A, 1, 600, 180, 'Üstteki açıklık: meatus', 'dogru', .5)
    # s2: alttaki geniş açıklık vajina
    halka(A, 400, 366, 110, 150, 2, f1=.05, f2=.98, nm='halka-vajina')
    et(A, 2, 620, 310, 'Alttaki geniş açıklık: vajina', 'bilgi', .1)
    # s3: yanlışlıkla vajinaya giren kateter (doğum yapmışta ciddi sorun yok) — kız bebek/çocukta anatomiyi kesin bil
    ilerleyen_kateter(A, 'M1000 250 L600 330 L400 366', [(T(3, .08), (600, 330)), (T(3, .4), (400, 366))], w=7,
                      o=K((0, 0), (T(3, .06), 0), (T(3, .1), 100), (T(3, .62), 100), (T(3, .7), 0)))
    halka(A, 400, 366, 110, 150, 3, f1=.4, f2=.68, nm='halka-vajina-hata')
    halka(A, 400, 170, 70, 50, 3, renk=YESIL, f1=.7, f2=.98, nm='halka-meatus-dogru')
    et(A, 3, 620, 310, 'Vajinaya girdi: hata, sorun az', 'uyari', .1, .66)
    et(A, 3, 600, 180, 'Doğru yer: meatus', 'dogru', .7)
    et(A, 3, 200, 120, 'Kız bebek/çocuk: kesin bil', 'uyari', .45)
    # s4: gerçek dokuda labialar yumuşak açılır — başparmak + işaret parmağı
    A.ekle('parmak', *v.katman('v-parmak'), p=K((0, [0, 200, 0]), (T(4, .05), [0, 200, 0]), (T(4, .4), [0, 0, 0])), o=belir(A, 4, .05))
    et(A, 4, 400, 110, 'Gerçek doku: yumuşak açılır', 'bilgi', .1)
    et(A, 4, 200, 300, 'Maket: daha sert', 'bilgi', .45)
    A.kamera(0, 400, 250, 100)
    A.kamera(1, 400, 200, 130)
    A.kamera(2, 400, 292, 120)
    A.kamera(3, 400, 292, 120)
    A.kamera(4, 400, 250, 100)


ADIMLAR = {'kontrendikasyon-travma': a_travma, 'malzeme': a_malzeme, 'kateter-yapisi': a_kateter_yapisi,
           'iletisim': a_iletisim, 'pozisyon': a_pozisyon, 'kadin-anatomi': a_kadin_anatomi}
