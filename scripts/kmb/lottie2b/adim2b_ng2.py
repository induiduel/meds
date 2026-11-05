"""KMB 01 Nazogastrik sonda — adım videoları, 2B düz çizgi film hattı, GRUP NG2 (adim2b.py bunları toplar).
Adımlar: ng-malzeme, ng-malzeme-kontrol, ng-hazirlik, ng-olcum, ng-cikarma, ng-kayganlastirma.
Sahneler: ng-malzeme, ng-pozisyon, ng-govde, ng-mide (+ ng-burun). Yalnız koreografi (docs/KMB_2B_STIL.md); her cümle bir
bölümdür (A.T(i, kesir)), cümlede anlatılan şey görüntüde bir eylemle karşılanır.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ortak2b import *  # noqa: E402,F401,F403
from lottie_dsl import kisi, yumruk  # noqa: E402

NG = ('#e9eef3', '#6b7a90')  # NG sonda: açık plastik gövde, kontur


def vurgu(A, s, id_, b, renk=SARI, f1=.05, f2=.95, pad=12, nm=None):
    """Sahne ögesinin kutusunu çevreleyen kesikli vurgu halkası (b cümlesinde belirir, söner)."""
    x, y, w, h = s.bbox(id_)
    halka(A, x + w / 2, y + h / 2, w / 2 + pad, h / 2 + pad, b, renk=renk, f1=f1, f2=f2, nm=nm or f'v-{id_}-{b}')


def balon_konusma(x, y, w, h, renk):
    L, R, T_, B_ = x - w / 2, x + w / 2, y - h / 2, y + h / 2
    d = (f'M{L + 14} {T_} L{R - 14} {T_} C{R} {T_} {R} {T_ + 14} {R} {T_ + 14} L{R} {B_ - 14} C{R} {B_} {R - 14} {B_} {R - 14} {B_} '
         f'L{x + 16} {B_} L{x} {B_ + 22} L{x - 16} {B_} L{L + 14} {B_} C{L} {B_} {L} {B_ - 14} {L} {B_ - 14} L{L} {T_ + 14} C{L} {T_} {L + 14} {T_} {L + 14} {T_} Z')
    return G(yol(d), fl('#ffffff'), st(renk, 3))


def kayit_formu(A, b, maddeler):
    """Kayıt formu: zemin + form, satırlar sırayla yazılır, kalem ilerler; her madde etiketle."""
    T = A.T
    g = gorun(A, b, b)
    zemin(A, nm=f'zemin-kayit-{b}')
    A.katmanlar[-1]['ks']['o'] = g
    n = len(maddeler)
    A.ekle(f'form-{b}', G(rc(300, 250, 300, 380, 12), fl('#ffffff'), st('#9aa6b4', 2)), G(rc(300, 86, 120, 22, 6), fl('#9aa6b4')),
           *[G(yol(f'M180 {140 + i * 56} L420 {140 + i * 56}'), st(MAVI, 4), tm(K((0, 0), (T(b, .08 + i * .2), 0), (T(b, .24 + i * .2), 100)))) for i in range(n)], o=g)
    A.ekle(f'kalem-{b}', G(yol('M0 0 L-56 38'), st('#2b2f36', 8)), G(yol('M-56 38 L-66 44'), st(SARI, 6)),
           p=KD(*[(T(b, .08 + i * .2 + j * .16 / 6), [180 + 240 * j / 6 + 56, 140 + i * 56 - 38, 0]) for i in range(n) for j in range(7)]), o=g)
    for i, m in enumerate(maddeler):
        et(A, b, 610, 140 + i * 56, m, 'bilgi', .08 + i * .2)
    A.kamera_sabit(b, b, 400, 250, 100)


# ———————————————————————— 1. Malzeme: sonda, kayganlaştırıcı, beslenme sondası (ng-malzeme; son cümle ng-mide)

def a_ng_malzeme(A):
    T = A.T
    s = Sahne2B('ng-malzeme')
    s.ekle(A, o=A.gor(0, T(7, .02)))
    # s0: renkli uçlar = kalınlık
    vurgu(A, s, 'nm-kalinlik', 0, f1=.05, f2=.5)
    halka(A, 452, 103, 26, 46, 0, renk=MAVI, f1=.45, f2=.98, nm='halka-uclar')
    et(A, 0, 300, 40, 'Renkli uç: kalınlık', 'bilgi', .05)
    A.kamera(0, 340, 110, 170)
    # s1: boylar aynı (üstte çift yönlü ölçü oku), kalınlık farklı (uç sütunu)
    ok(A, 'M222 52 L462 52', 1, renk=YESIL, w=4, f1=.05, f2=.98, nm='ok-boy-sag')
    ok(A, 'M462 52 L222 52', 1, renk=YESIL, w=4, f1=.05, f2=.98, nm='ok-boy-sol')
    halka(A, 452, 103, 26, 46, 1, renk=MAVI, f1=.45, f2=.98, nm='halka-kalinlik')
    et(A, 1, 300, 40, 'Boyları benzer', 'dogru', .05)
    et(A, 1, 300, 170, 'Kalınlıkları farklı', 'bilgi', .45)
    # s2: uzunluk işaretleri (kıvrık sondadaki çizgiler + 50/60 sayıları)
    vurgu(A, s, 'nm-sonda', 2, f1=.05, f2=.6)
    halka(A, 318, 70, 34, 14, 2, renk=MAVI, f1=.4, f2=.98, nm='halka-50-60')
    et(A, 2, 120, 180, 'Uzunluk işareti: çizgi', 'bilgi', .05)
    et(A, 2, 320, 40, '50, 60: ilerlemeyi izle', 'bilgi', .4)
    A.kamera(2, 230, 110, 160)
    # s3: kapalı paket işlemden hemen önce açılır; eldivenle, steril olmayan işlem
    A.ekle('paket', G(rc(111, 101, 166, 124, 10), fl('#dfe8f1', .82), st('#8a96a6', 2)),
           G(yol('M28 39 L194 163'), st('#ffffff', 2, o=60)),
           o=K((0, 0), (T(3), 0), (T(3, .04), 100), (T(3, .3), 100), (T(3, .4), 0)),
           s=K((0, [100, 100, 100]), (T(3, .3), [100, 100, 100]), (T(3, .4), [100, 6, 100])), a=(111, 39), p=S([111, 39, 0]))
    et(A, 3, 260, 200, 'Paket hemen önce açılır', 'bilgi', .04)
    vurgu(A, s, 'nm-eldiven', 3, renk=MAVI, f1=.45, f2=.98)
    et(A, 3, 324, 300, 'Temiz + eldiven, steril değil', 'bilgi', .45)
    A.kamera(3, 300, 250, 100)
    # s4: su bazlı jel (doğru)
    vurgu(A, s, 'nm-jel', 4, renk=YESIL, f1=.05)
    tik(A, 500, 200, 4, .3)
    et(A, 4, 470, 140, 'Su bazlı jel', 'dogru', .05)
    et(A, 4, 470, 320, 'Üretral kateter jeli uygun', 'bilgi', .45)
    A.kamera(4, 520, 250, 160)
    # s5: vazelin (petrol ürünü, ilk tercih değil)
    vurgu(A, s, 'nm-vazelin', 5, renk=KIRMIZI, f1=.05)
    carpi(A, 600, 243, 5, .25, r=30)
    et(A, 5, 600, 150, 'Vazelin: petrol ürünü', 'uyari', .05)
    et(A, 5, 600, 320, 'Yalnız çaresizsen, çok az', 'uyari', .5)
    A.kamera(5, 560, 250, 150)
    # s6: standart sonda telsiz; beslenme sondası ince, yumuşak, kılavuz telli
    vurgu(A, s, 'nm-sonda', 6, f1=.05, f2=.45)
    et(A, 6, 120, 200, 'Standart: tel yok', 'bilgi', .05)
    vurgu(A, s, 'nm-beslenme', 6, renk=MAVI, f1=.45, f2=.98)
    halka(A, 768, 101, 18, 18, 6, renk=MAVI, f1=.6, f2=.98, nm='halka-tel')
    et(A, 6, 640, 160, 'Beslenme: ince, telli', 'bilgi', .45)
    A.kamera(6, 400, 250, 100)
    # s7: sahne ng-mide'ye geçer — beslenme sondasının ucu mide–duodenum başında; tel çıkar, yer kontrolü, sabitleme
    m = Sahne2B('ng-mide')
    gm = A.gor(T(7), None)
    m.ekle(A, dahil=['nd-beslenme'], o=gm, on_ek='m-')
    halka(A, 268, 280, 40, 40, 7, renk=YESIL, f1=.15, f2=.98, nm='halka-uc-duo')
    et(A, 7, 200, 200, 'Uç: mide–duodenum başı', 'dogru', .15)
    ok(A, 'M444 90 L444 10', 7, renk=MAVI, w=5, f1=.45, f2=.98, nm='ok-tel')
    et(A, 7, 600, 60, 'Tel çıkarılır', 'bilgi', .45)
    et(A, 7, 600, 110, 'Yer kontrolü, sabitleme', 'dogru', .7)
    A.kamera(7, 400, 250, 100)


# ———————————————————————— 2. Malzeme: yer kontrolü, sabitleme, korunma (ng-malzeme)

def a_ng_malzeme_kontrol(A):
    s = Sahne2B('ng-malzeme')
    s.ekle(A)
    # s0: çan uçlu 50 mL enjektör (doğru)
    vurgu(A, s, 'nm-enjektor-can', 0, renk=YESIL)
    tik(A, 150, 190, 0, .3)
    et(A, 0, 150, 140, 'Çan uçlu 50 mL: tam oturur', 'dogru', .05)
    A.kamera(0, 200, 240, 170)
    # s1: normal (luer) enjektör oturmaz, hava kenardan kaçar
    vurgu(A, s, 'nm-enjektor-normal', 1, renk=KIRMIZI)
    carpi(A, 324, 240, 1, .3, r=26)
    A.ekle('hava-kacar', G(yol('M372 232 C384 224 392 226 398 218'), st('#9aa6b4', 2.5, kesik=(5, 5))),
           G(yol('M374 248 C386 256 394 254 400 262'), st('#9aa6b4', 2.5, kesik=(5, 5))), o=belir(A, 1, .45, 1))
    et(A, 1, 320, 160, 'Normal uç oturmaz', 'uyari', .05)
    et(A, 1, 330, 320, 'Hava kenardan kaçar', 'uyari', .45)
    A.kamera(1, 320, 240, 170)
    # s2: stetoskop (dinleme) + flaster (sabitleme)
    vurgu(A, s, 'nm-stetoskop', 2, f1=.05)
    vurgu(A, s, 'nm-flaster', 2, renk=MAVI, f1=.4)
    et(A, 2, 120, 260, 'Stetoskop: mideyi dinle', 'bilgi', .05)
    et(A, 2, 250, 300, 'Flaster: burna sabitle', 'bilgi', .4)
    A.kamera(2, 160, 340, 160)
    # s3: kirli işlem → emici örtü + kusma poşeti
    et(A, 3, 460, 250, 'İşlem kirli: öğürme, öksürük', 'uyari', .02, .4)
    vurgu(A, s, 'nm-ortu', 3, f1=.3)
    vurgu(A, s, 'nm-poset', 3, renk=MAVI, f1=.55)
    et(A, 3, 400, 300, 'Emici örtü: göğse', 'bilgi', .3)
    et(A, 3, 580, 250, 'Kusma poşeti', 'bilgi', .55)
    A.kamera(3, 480, 340, 150)
    # s4: lavaj suyu + boşaltma torbası
    vurgu(A, s, 'nm-su', 4, renk=MAVI, f1=.05)
    vurgu(A, s, 'nm-torba', 4, f1=.4)
    et(A, 4, 710, 160, 'Su: lavaj', 'bilgi', .05)
    et(A, 4, 640, 310, 'Torba: boşaltma', 'bilgi', .4)
    A.kamera(4, 640, 320, 150)


# ———————————————————————— 3. El yıkama, kendini tanıtma, onam, örtü (ng-pozisyon)

def a_ng_hazirlik(A):
    T = A.T
    s = Sahne2B('ng-pozisyon')
    s.ekle(A)
    # s0: lavabo — musluktan su akar, köpük; dezenfektan yerini tutmaz
    vurgu(A, s, 'np-lavabo', 0, renk=MAVI, f2=.98)
    A.ekle('su', G(yol('M74 222 L74 262'), st(JEL, 4, kesik=(8, 8), kesik_kayma=KD((T(0, .1), 0), (T(0, 1), -(T(0, 1) - T(0, .1)) * 2)))),
           o=K((0, 0), (T(0, .1), 0), (T(0, .14), 100), (T(0, .96), 100), (T(0, 1), 0)))
    A.ekle('kopuk', *[G(el(56 + i * 12, 262 - (i % 2) * 6, 10, 10), fl('#ffffff'), st('#9aa6b4', 1.2)) for i in range(4)],
           o=belir(A, 0, .35, 0))
    et(A, 0, 160, 120, 'Su ve sabunla yıka', 'dogru', .05)
    et(A, 0, 210, 330, 'Dezenfektan yerini tutmaz', 'uyari', .5)
    A.kamera(0, 160, 280, 170)
    # s1: sağlık çalışanının elleri enfeksiyon taşır — elde mikrop noktaları
    vurgu(A, s, 'np-hekim', 1, renk=KIRMIZI)
    A.ekle('mikrop', *[G(el(x, y, 9, 9), fl('#8bbf3f'), st('#4f7a1c', 1.2)) for x, y in ((548, 236), (566, 244), (556, 262), (574, 270), (590, 228))],
           o=belir(A, 1, .25, 1))
    et(A, 1, 440, 60, 'Eller enfeksiyon taşır', 'uyari', .1)
    A.kamera(1, 400, 250, 100)
    # s2: eldiven giyilir (kalıcı)
    A.ekle('eldiven', *s.katman('np-eldiven'), o=belir(A, 2, .15))
    A.ekle('eldiven-el', *s.katman('np-el-bas'), o=K((0, 0), (T(2, .15), 0), (T(2, .2), 0)))  # el-bas bu adımda görünmez
    vurgu(A, s, 'np-eldiven', 2, renk=MAVI, f1=.2, pad=16)
    et(A, 2, 540, 170, 'Eldiven giyilir', 'bilgi', .2)
    A.kamera(2, 520, 250, 160)
    # s3: kendini tanıtır — konuşma balonu
    vurgu(A, s, 'np-hekim', 3, f1=.05, f2=.4)
    A.ekle('balon-tanit', balon_konusma(470, 70, 230, 50, MAVI), o=belir(A, 3, .4, 3))
    et(A, 3, 470, 70, 'Ben Doktor Büşra', 'bilgi', .42)
    et(A, 3, 250, 180, 'Kendini tanıt', 'dogru', .3)
    A.kamera(3, 400, 250, 100)
    # s4: işlemi anlatır — olası yakınmalar hastaya
    vurgu(A, s, 'np-hasta', 4, f1=.05, f2=.98, pad=6)
    A.ekle('balon-anlat', balon_konusma(470, 70, 230, 50, MAVI), o=belir(A, 4, .02, 4))
    et(A, 4, 470, 70, 'İşlemi anlat', 'bilgi', .05)
    et(A, 4, 200, 150, 'Bulantı olabilir', 'bilgi', .25)
    et(A, 4, 200, 200, 'Burunda tahriş, kanama', 'bilgi', .45)
    et(A, 4, 200, 250, 'Kusarsa poşet tutulur', 'bilgi', .65)
    # s5: onam; örtü göğse, kusma poşeti hastaya
    tik(A, 380, 120, 5, .05, son=5)
    et(A, 5, 250, 70, 'Sorular cevaplanır, onam', 'dogru', .05)
    A.ekle('ortu', *s.katman('np-ortu'), o=belir(A, 5, .3))
    A.ekle('poset', *s.katman('np-poset'), o=belir(A, 5, .5))
    vurgu(A, s, 'np-ortu', 5, renk=YESIL, f1=.3, pad=8)
    vurgu(A, s, 'np-poset', 5, renk=MAVI, f1=.5, pad=8)
    et(A, 5, 560, 200, 'Örtü: peçete gibi göğse', 'bilgi', .3)
    et(A, 5, 300, 320, 'Kusma poşeti verilir', 'bilgi', .5)
    A.kamera(5, 400, 250, 120)


# ———————————————————————— 4. Ölçüm: burun deliği → kulak memesi → ksifoid (ng-govde)

def a_ng_olcum(A):
    T = A.T
    s = Sahne2B('ng-govde')
    s.ekle(A)
    d = s.cz('nb-sonda-olcu')[0]['d']  # burun → kulak → ksifoid → aşağı (gövdenin DIŞINDA tutulan sonda)
    P = ornekle(d, 400)
    yak = lambda q: min(range(len(P)), key=lambda i: (P[i][0] - q[0]) ** 2 + (P[i][1] - q[1]) ** 2) / 4  # noqa: E731
    f_kulak, f_ksi = yak((444, 132)), yak((388, 338))
    # s0: iki farklı beden — mesafe kişiye özeldir
    A.ekle('uzun', *kisi(150, 120, '#8fc1c9', 1.4), o=belir(A, 0, .1, 0))
    A.ekle('kisa', *kisi(690, 220, '#c9b48f', .95), o=belir(A, 0, .3, 0))
    et(A, 0, 150, 60, '2 m · 120 kg', 'bilgi', .1)
    et(A, 0, 690, 150, '1,40 m · 40 kg', 'bilgi', .3)
    et(A, 0, 420, 330, 'Mesafe kişiye özel: ölç', 'dogru', .55)
    A.kamera(0, 400, 250, 100)
    # sonda: ucu burunda sabit, gövde cümle cümle uzar (s1 uç → s2 kulak → s3 ksifoid → s4 kalan)
    e = K((0, 0), (T(1, .1), 0), (T(1, .4), 2), (T(2, .1), 2), (T(2, .7), f_kulak), (T(3, .1), f_kulak), (T(3, .75), f_ksi),
          (T(4, .55), f_ksi), (T(4, .85), 100))
    A.ekle('sonda-olcu', *kateter_cizgi(d, 5, NG, e=e), o=belir(A, 1, .1))
    A.ekle('sonda-uc', G(el(330, 119, 9, 9), fl(NG[0]), st(NG[1], 1.6)), o=belir(A, 1, .1))
    # s1: uç burun deliğinde
    halka(A, 337, 123, 18, 16, 1, renk=MAVI, f1=.15, f2=.98, nm='h-burun')
    et(A, 1, 250, 80, '1) Burun deliği', 'bilgi', .15)
    A.kamera(1, 380, 150, 200)
    # s2: burun → kulak memesi (ölçü çizgisi çizilir)
    A.ekle('olcu-1', G(yol(s.cz('nb-olcu-1')[0]['d']), st(MAVI, 2.5, kesik=(8, 6)), tm(K((0, 0), (T(2, .1), 0), (T(2, .7), 100)))), o=belir(A, 2, .1))
    halka(A, 445, 112, 18, 26, 2, renk=MAVI, f1=.6, f2=.98, nm='h-kulak')
    et(A, 2, 520, 70, '2) Kulak memesi', 'bilgi', .6)
    A.kamera(2, 410, 150, 200)
    # s3: kulak memesi → ksifoid (epigastriumun üst sınırı)
    A.ekle('olcu-2', G(yol(s.cz('nb-olcu-2')[0]['d']), st(MAVI, 2.5, kesik=(8, 6)), tm(K((0, 0), (T(3, .1), 0), (T(3, .75), 100)))), o=belir(A, 3, .1))
    halka(A, 389, 336, 20, 20, 3, renk=MAVI, f1=.7, f2=.98, nm='h-ksifoid')
    et(A, 3, 250, 310, '3) Ksifoid', 'bilgi', .7)
    A.kamera(3, 400, 260, 140)
    # s4: ksifoide denk gelen nokta sondada işaretlenir; sonda kalan boyuyla görünür
    A.ekle('isaret', *s.katman('nb-isaret'), o=belir(A, 4, .1))
    halka(A, 388, 338, 24, 24, 4, renk=SARI, f1=.1, f2=.98, nm='h-isaret')
    et(A, 4, 250, 300, 'Sondada işaretle', 'dogru', .1)
    et(A, 4, 250, 200, 'Kaç cm? Kaçıncı çizgi?', 'bilgi', .45)
    A.kamera(4, 380, 280, 170)
    # s5: sınavın en sık hatası — sıra: burun → kulak → ksifoid (noktalar sırayla yanar), işaret yeşil + tik
    for i, (x, y, rx, ry) in enumerate(((337, 123, 18, 16), (445, 112, 18, 26), (389, 336, 20, 20))):
        halka(A, x, y, rx, ry, 5, renk=YESIL, f1=.1 + i * .2, f2=.98, nm=f'h-sira-{i}')
    et(A, 5, 220, 100, '1) Burun deliği', 'dogru', .1)
    et(A, 5, 600, 100, '2) Kulak memesi', 'dogru', .3)
    et(A, 5, 220, 330, '3) Ksifoid', 'dogru', .5)
    tik(A, 440, 320, 5, .65)
    et(A, 5, 600, 200, 'En sık sınav hatası', 'uyari', .02)
    A.kamera(5, 400, 230, 125)


# ———————————————————————— 5. Sondayı çıkarma ve kayıt (ng-pozisyon; son cümle kayıt formu)

def a_ng_cikarma(A):
    T = A.T
    s = Sahne2B('ng-pozisyon')
    gp = K((0, 100), (T(2), 100), (T(2) + 8, 0), (T(3), 0), (T(3) + 8, 100), (T(3, 1), 100), (T(3, 1) + 8, 0))
    s.ekle(A, o=gp)
    # s0: takılı sonda; hekim kendini tanıtır, anlatır
    A.ekle('sonda', *s.katman('np-sonda'), o=K((0, 100), (T(2), 100), (T(2) + 8, 0)))
    vurgu(A, s, 'np-sonda', 0, f1=.05, f2=.45, pad=8)
    et(A, 0, 300, 160, 'Takılı sonda', 'bilgi', .05)
    A.ekle('balon-c0', balon_konusma(470, 70, 230, 50, MAVI), o=belir(A, 0, .4, 0))
    et(A, 0, 470, 70, 'Tanıt ve anlat', 'bilgi', .42)
    vurgu(A, s, 'np-hekim', 0, renk=MAVI, f1=.4, f2=.98)
    A.kamera(0, 400, 250, 100)
    # s1: yine örtü + kusma poşeti
    A.ekle('poset', *s.katman('np-poset'), o=K((0, 0), (T(1, .35), 0), (T(1, .35) + 8, 100), (T(2), 100), (T(2) + 8, 0), (T(3), 0), (T(3) + 8, 100), (T(3, 1), 100), (T(3, 1) + 8, 0)))
    A.ekle('ortu-1', *s.katman('np-ortu'), o=K((0, 0), (T(1, .15), 0), (T(1, .2), 100), (T(2), 100), (T(2) + 8, 0)))
    et(A, 1, 300, 110, 'Çıkarmak da bulandırır', 'uyari', .05)
    et(A, 1, 560, 200, 'Örtü serilir', 'bilgi', .2)
    et(A, 1, 300, 320, 'Kusma poşeti verilir', 'bilgi', .35)
    A.kamera(1, 420, 250, 130)
    # s2a: yakın plan burun — bantlar kalkıp solar, eldivenli el sondayı kavrar
    b = Sahne2B('ng-burun')
    gb = K((0, 0), (T(2), 0), (T(2) + 8, 100), (T(2, .45), 100), (T(2, .45) + 8, 0))
    b.ekle(A, dahil=['nr-sonda'], o=gb, on_ek='b-')
    for i, fid in enumerate(('nr-flaster-burun', 'nr-flaster-sarim')):
        A.ekle(f'bant-{i}', *b.katman(fid), p=K((0, [0, 0, 0]), (T(2, .1 + i * .08), [0, 0, 0]), (T(2, .3 + i * .05), [40, -50, 0])),
               o=K((0, 0), (T(2), 0), (T(2) + 8, 100), (T(2, .12 + i * .08), 100), (T(2, .3 + i * .05), 0)))
    et(A, 2, 560, 120, 'Bantları sök', 'bilgi', .05, .45)
    A.ekle('el-b', yumruk(0, 0, .5, 0, steril=False), p=K((0, [262, 452, 0]), (T(2, .3), [262, 452, 0]), (T(2, .42), [236, 470, 0])),
           o=K((0, 0), (T(2, .3), 0), (T(2, .3) + 6, 100), (T(2, .45), 100), (T(2, .45) + 8, 0)))
    # s2b: kesit — sondanın içerideki kısmı tersine kısalır, dışarı çıkan kısım örtüye toplanır
    k = Sahne2B('ng-kesit')
    gk = K((0, 0), (T(2, .45), 0), (T(2, .45) + 8, 100), (T(2, 1), 100), (T(2, 1) + 8, 0))
    k.ekle(A, o=gk, on_ek='k-')
    d = k.cz('nk-sonda')[0]['d']
    P = ornekle(d, 400)
    f_delik = min(range(len(P)), key=lambda i: (P[i][0] - 152) ** 2 + (P[i][1] - 140) ** 2) / 4
    A.ekle('k-ortu', G(rc(110, 352, 200, 34, 8), fl('#2f6f5f', o=85), st('#1f4e44', 2)), o=gk)
    A.ekle('k-sonda', *kateter_cizgi(d, 5, NG, e=K((0, 100), (T(2, .55), 100), (T(2, .95), f_delik + 1))), o=gk)
    dis = 'M130 260 C128 290 118 316 100 330 C84 342 120 348 150 340'
    A.ekle('k-dis', *kateter_cizgi(dis, 5, NG, e=K((0, 0), (T(2, .55), 0), (T(2, .95), 100))), o=gk)
    A.ekle('el-k', yumruk(0, 0, .4, 0, steril=False), p=K((0, [128, 302, 0]), (T(2, .55), [128, 302, 0]), (T(2, .95), [104, 318, 0])), o=gk)
    et(A, 2, 330, 110, 'Sonda geri çekilir', 'bilgi', .55)
    et(A, 2, 330, 340, 'Dışarı çıkan örtüye', 'dogru', .7)
    A.kamera(2, 400, 250, 100)
    # s3: örtü sondayla katlanıp toplanır, hekim çöpe atar
    A.ekle('eldiven', *s.katman('np-eldiven'), o=K((0, 0), (T(3), 0), (T(3) + 8, 100), (T(3, 1), 100), (T(3, 1) + 8, 0)))
    A.ekle('cop', G(yol('M666 400 L714 400 L708 456 L672 456 Z'), fl('#9aa6b4'), st('#5b6676', 2)), G(rc(690, 398, 56, 8, 3), fl('#5b6676')), o=gorun(A, 3, 3))
    A.ekle('ortu-2', *s.katman('np-ortu'), a=(453, 261),
           p=K((0, [453, 261, 0]), (T(3, .1), [453, 261, 0]), (T(3, .4), [520, 265, 0]), (T(3, .5), [540, 265, 0]), (T(3, .78), [690, 390, 0])),
           s=K((0, [100, 100, 100]), (T(3, .1), [100, 100, 100]), (T(3, .4), [60, 30, 100]), (T(3, .78), [40, 20, 100])),
           o=K((0, 0), (T(3), 0), (T(3) + 8, 100), (T(3, .78), 100), (T(3, .86), 0)))
    et(A, 3, 300, 110, 'Partikül saçılmaz', 'dogru', .05)
    et(A, 3, 300, 170, 'Örtü katlanıp toplanır', 'bilgi', .1)
    et(A, 3, 560, 330, 'Çöpe atılır', 'bilgi', .6)
    A.kamera(3, 440, 260, 130)
    # s4: kayıt
    kayit_formu(A, 4, ['Yapılan işlem', 'Ölçülen uzunluk', 'Yer kontrolü sonucu', 'Kanama, öksürük, kusma'])


# ———————————————————————— 6. Kayganlaştırma ve baş pozisyonu (ng-burun; s3–s4 ng-pozisyon)

def a_ng_kayganlastirma(A):
    T = A.T
    b = Sahne2B('ng-burun')
    g01 = A.gor(0, T(2, 1))
    b.ekle(A, o=g01)
    A.ekle('sonda', *b.katman('nr-sonda'), o=K((0, 0), (T(0, .05), 0), (T(0, .1), 100), (T(2, 1), 100), (T(2, 1) + 8, 0)))
    A.ekle('jel', *b.katman('nr-jel'), o=K((0, 0), (T(0, .4), 0), (T(0, .5), 100), (T(2, 1), 100), (T(2, 1) + 8, 0)))
    x, y, w, h = b.bbox('nr-jel')
    halka(A, x + w / 2, y + h / 2, w / 2 + 14, h / 2 + 14, 0, renk=MAVI, f1=.45, f2=.98, nm='h-jel')
    et(A, 0, x + w / 2, max(60, y - 30), 'Uçtan ≈5 cm jelle', 'dogru', .45)
    et(A, 0, 400, 60, 'Önce yan delikli uç girer', 'bilgi', .1)
    halka(A, x + w / 2, y + h / 2, w / 2 + 14, h / 2 + 14, 1, renk=MAVI, f1=.05, f2=.98, nm='h-jel-1')
    et(A, 1, 400, 60, 'Sondaya sık ya da eldivene koy', 'bilgi', .05)
    xs, ys, ws, hs = b.bbox('nr-jel')  # sondanın burun deliğindeki jelli ucu (nr-sonda kutusu dış uzantıyı da kapsar)
    halka(A, xs + ws / 2, ys + hs / 2, ws / 2 + 12, hs / 2 + 12, 2, f1=.05, f2=.98, nm='h-sonda')
    et(A, 2, 400, 60, 'Jelli uç burnu da kayganlatır', 'dogru', .1)
    # s3–s4: ng-pozisyon — çene göğse; başın arkasında el
    p = Sahne2B('ng-pozisyon')
    g34 = A.gor(T(3), None)
    p.ekle(A, o=g34, on_ek='p-')
    A.ekle('ok-egim', G(yol(p.cz('np-ok-egim')[0]['d']), st(MAVI, 3), tm(K((0, 0), (T(3, .15), 0), (T(3, .6), 100)))), o=belir(A, 3, .1))
    et(A, 3, 300, 120, 'Başı hafifçe öne eğ', 'dogru', .15)
    A.kamera(3, 420, 200, 160)
    A.ekle('el-bas', *p.katman('np-el-bas'), o=belir(A, 4, .4))
    et(A, 4, 300, 120, 'İçgüdü: baş geri atılır', 'uyari', .05)
    et(A, 4, 560, 110, 'El başın arkasında', 'dogru', .4)


ADIMLAR = {'ng-malzeme': a_ng_malzeme, 'ng-malzeme-kontrol': a_ng_malzeme_kontrol, 'ng-hazirlik': a_ng_hazirlik,
           'ng-olcum': a_ng_olcum, 'ng-cikarma': a_ng_cikarma}
if (Path(__file__).resolve().parent / 'svg' / 'ng-burun.lottie.json').exists():
    ADIMLAR['ng-kayganlastirma'] = a_ng_kayganlastirma
