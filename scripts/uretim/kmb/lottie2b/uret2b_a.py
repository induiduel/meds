"""KMB konu videoları — 2B düz çizgi film hattı, GRUP A (uret2b.py bunları içe alır).
Videolar: mahremiyet, malzeme-hazirlik, glob-sistit, travma, idrar-akisi, kadin-temizlik.
Bölüm adları/metinleri eski hat (lottie_uret.py) ile BİREBİR aynıdır (ses klipleri l-<ad> bu bölümlere zamanlı).
Anatomi/el/araç/zemin 2B sahnelerden (Sahne2B) gelir; burada yalnız koreografi yazılır (docs/KMB_2B_STIL.md).
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ortak2b import *  # noqa: E402,F401,F403
from lottie_dsl import yumruk  # noqa: E402  (ortak eldivenli el, 2B palet)


def _son(A):
    """Video sonuna dek görünür kalan ögeler için `belir(..., son=_son(A))` değeri (T(i,1) = op-1)."""
    # alt kompozisyonda (lottie_dsl.Ic) bölüm listesi yok: harita uzunluğu
    return len(getattr(A, 'bolumler', None) or getattr(A, 'harita', [])) + 5


def _katmanlar(s: Sahne2B):
    """Sahne katmanları belge sırasıyla: (id | None, ad, şekiller) — arka (kimliksiz) parçalar dahil."""
    return [(k['id'], k['nm'], copy.deepcopy(k['it'])) for k in s.katmanlar]


# ———————————————————————— 1. İletişim ve mahremiyet (pozisyon sahnesi)

def mahremiyet(z):
    A = anim(z, 'mahremiyet', 'Kendini tanıt, onam al, mahremiyeti sağla', [
        B('Tanış', 'Kendini tanıtır, hastaya neden kateter takılması gerektiğini anlatır ve sözlü onamını alırsın.', 8),
        B('Paravan', 'Paravanı ya da perdeyi kapatarak mahremiyeti sağlarsın; kateter ortalık yerde takılmaz.', 7),
        B('Yardımcı', 'Yanına yardımcı bir sağlık personeli alırsın; karşı cinsten hastada karşı cinsten personel, çocukta ebeveyn bulunur.', 9),
    ])
    T = A.T
    s = Sahne2B('pozisyon')
    s.ekle(A, haric=['p-v', 'p-hekim'])  # iki yatak, erkek (supin), kadın (litotomi)
    # s0: hekim hastanın baş ucuna bir adım yaklaşır, konuşma balonu açılır, sözlü onam ✓
    A.ekle('hekim', *s.katman('p-hekim'), p=K((0, [0, 0, 0]), (T(0, .05), [0, 0, 0]), (T(0, .4), [6, 0, 0])))
    A.ekle('balon-konusma', G(yol('M140 12 L280 12 C292 12 292 68 280 68 L170 68 L128 96 L146 68 L140 68 C128 68 128 12 140 12 Z'), fl('#ffffff'), st(MAVI, 2.5)),
           *[G(el(186 + i * 24, 40, 10, 10), fl(MAVI)) for i in range(3)],
           o=K((0, 0), (T(0, .1), 0), (T(0, .2), 100), (T(0, .68), 100), (T(0, .72), 0)))
    A.ekle('balon-onam', G(yol('M140 12 L280 12 C292 12 292 68 280 68 L170 68 L128 96 L146 68 L140 68 C128 68 128 12 140 12 Z'), fl('#ffffff'), st(YESIL, 2.5)),
           o=K((0, 0), (T(0, .68), 0), (T(0, .72), 100), (T(0, 1), 100), (T(1, .05), 0)))
    tik(A, 210, 42, 0, .72)
    # s1: paravan sağdan kayarak yatakların başına gelir
    A.ekle('paravan', *s.katman('p-paravan'), p=K((0, [160, 0, 0]), (T(1, .05), [160, 0, 0]), (T(1, .55), [0, 0, 0])), o=belir(A, 1, .02))
    # s2: yardımcı personel sağdan gelir (kadın yatağının ayak ucunda, yatağın dışında)
    A.ekle('yardimci', *s.katman('p-yardimci'), p=K((0, [150, 0, 0]), (T(2, .05), [150, 0, 0]), (T(2, .45), [0, 0, 0])), o=belir(A, 2, .02))
    A.etiket(0, 0, 420, 40, 'Tanıt · anlat · onam', 'bilgi')
    A.etiket(1, 1, 705, 36, 'Paravan / perde', 'bilgi')
    A.etiket(1, 1, 700, 272, 'Ortalık yerde takılmaz', 'uyari')
    A.etiket(2, 2, 712, 290, 'Yardımcı personel', 'dogru')
    A.etiket(2, 2, 520, 230, 'Çocukta ebeveyn', 'bilgi')
    A.kamera(0, 230, 150, 150)
    A.kamera(1, 650, 160, 130)
    A.kamera(2, 600, 300, 120)
    return A


# ———————————————————————— 2. Malzeme hazırlığı (malzeme sahnesi: tepsi + 11 öge)

def malzeme_hazirlik(z):
    A = anim(z, 'malzeme-hazirlik', 'Malzemeyi hazırlamak ve steril alan', [
        B('Kateter', 'Önce uygun boyda üretral kateteri seçersin: erişkinde on iki ile yirmi dört French arası.', 7),
        B('Eldivenler', 'Temizlik için steril olmayan, yerleştirme için steril eldiven hazırlarsın.', 6),
        B('Jel ve balon', 'Kayganlaştırıcı jel, balon için steril izotonik ve enjektör tepsiye konur.', 6),
        B('Geniş uçlu enjektör', 'İdrar gelmezse kontrol için geniş uçlu kateter enjektörünü unutmazsın.', 6),
        B('Temizlik ve torba', 'Antiseptik, gazlı bez, delikli örtü ve idrar torbası da hazır olmalıdır.', 6),
        B('Steril alan', 'Steril malzemeyi yardımcın açar; sen steril eldivenle yalnız steril alana dokunursun.', 7),
    ])
    T = A.T
    s = Sahne2B('malzeme')
    s.ekle(A, haric=s.ids())  # yalnız tepsi + valf renk kutusu; ögeler cümle cümle tepsiye konur
    gruplar = [(0, ['m-lateks', 'm-silikon']), (1, ['m-nonsteril', 'm-steril']), (2, ['m-jel', 'm-izotonik', 'm-enjektor']),
               (3, ['m-genis']), (4, ['m-antiseptik', 'm-ortu', 'm-torba'])]
    for b, ids in gruplar:
        for j, i in enumerate(ids):
            x, y, w, h = s.bbox(i)
            k = T(b, .04 + .12 * j)
            A.ekle(i, *s.katman(i), p=K((0, [0, -26, 0]), (k, [0, -26, 0]), (k + 12, [0, 0, 0])), o=A.gor(k))  # tepsiye konur
            A.ekle(f'halka-{i}', G(el(x + w / 2, y + h / 2, w + 20, h + 20), st(SARI, 4, kesik=(10, 7))),
                   o=K((0, 0), (k + 10, 0), (k + 18, 100), (T(b, .95), 100), (T(b, 1), 0)))  # vurgu halkası öge yerleşince
    # s5: steril alan çerçevesi (yardımcı açar; sen yalnız buraya dokunursun)
    A.ekle('steril-alan', *s.katman('m-steril-alan'), o=belir(A, 5, .1))
    A.etiket(0, 0, 205, 14, 'Erişkin: 12–24 French', 'bilgi')
    A.etiket(1, 1, 500, 196, 'Steril olmayan: temizlik', 'bilgi')
    A.etiket(1, 1, 690, 196, 'Steril: yerleştirme', 'dogru')
    A.etiket(2, 2, 300, 186, 'Jel · izotonik · enjektör', 'bilgi')
    A.etiket(3, 3, 640, 160, 'İdrar gelmezse kontrol', 'uyari')
    A.etiket(3, 3, 640, 200, 'Geniş uçlu enjektör: 50 mL', 'bilgi')
    A.etiket(4, 4, 300, 345, 'Antiseptik · örtü · torba', 'bilgi')
    A.etiket(5, 5, 490, 42, 'Steril alan', 'dogru')
    A.etiket(5, 5, 490, 342, 'Yalnız steril eldivenle dokun', 'uyari')
    A.kamera(0, 210, 110, 170)
    A.kamera(1, 600, 100, 160)
    A.kamera(2, 300, 268, 140)
    A.kamera(3, 640, 270, 170)
    A.kamera(4, 300, 400, 130)
    A.kamera(5, 400, 250, 100)
    return A


# ———————————————————————— 3. Glob vezikale / sistit (mesane sahnesi, yan kesit)

def glob_sistit(z):
    A = anim(z, 'glob-sistit', 'Glob vezikale mi, sistit mi?', [
        B('Dolan mesane', 'İdrarını yapamayan hastada mesane dolar ve giderek büyür.', 6),
        B('Glob', 'Glob vezikalede mesane kubbesi pubisin üstüne çıkar; alt karında kabarıklık oluşur.', 7),
        B('Muayene', 'Muayenede suprapubik bölgede şişlik ve dolgunluk ararsın.', 6),
        B('Ultrason', 'Ultrason mesanenin ağzına kadar dolu olduğunu gösterirse kateter endikasyonu kesinleşir.', 7),
        B('Sistit', 'Sistitte ise mesanede yalnız on beş yirmi mililitre idrar vardır; hasta idrar yapamıyorum dese de kateter gerekmez.', 9),
    ])
    T = A.T
    s = Sahne2B('mesane')
    s.ekle(A, haric=['g-mesane-normal'])  # gövde kesiti, sakrum, rektum, simfiz, üretra, bağırsaklar
    # s0–s1: normal mesane → boyundan büyüyerek dolu mesane (kubbe umbilikusa doğru)
    A.ekle('mesane-normal', *s.katman('g-mesane-normal'), o=K((0, 100), (T(0, .25), 100), (T(0, .42), 0)))
    A.ekle('mesane-dolu', *s.katman('g-mesane-dolu'), a=(428, 318), p=S([428, 318, 0]),
           s=K((0, [42, 40, 100]), (T(0, .2), [42, 40, 100]), (T(1, .6), [100, 100, 100]), (T(4, .15), [100, 100, 100]), (T(4, .35), [30, 30, 100])),
           o=K((0, 0), (T(0, .2), 0), (T(0, .4), 100), (T(4, .15), 100), (T(4, .35), 0)))
    # s1: karın duvarı dolu mesanenin önünde öne bombeleşir
    A.ekle('sisme', *s.katman('g-sisme'), o=K((0, 0), (T(1, .3), 0), (T(1, .6), 100), (T(4, .15), 100), (T(4, .35), 0)))
    halka(A, 420, 112, 96, 56, 1, f1=.15, f2=.6, nm='halka-kubbe')
    halka(A, 500, 338, 24, 38, 1, f1=.55, f2=.98, nm='halka-pubis')
    # s2: palpasyon eli sağdan gelir, suprapubik deriye iki kez bastırır
    A.ekle('el', *s.katman('g-el'), p=K((0, [150, 0, 0]), (T(2), [150, 0, 0]), (T(2, .3), [0, 0, 0]), (T(2, .45), [-12, 3, 0]), (T(2, .6), [0, 0, 0]),
                                         (T(2, .75), [-12, 3, 0]), (T(2, .9), [0, 0, 0])), o=belir(A, 2, 0, 2))
    # s3: ultrason probu deride, ışın mesaneye: ağzına kadar dolu
    A.ekle('us', *s.katman('g-us'), o=belir(A, 3, .05, 3))
    A.ekle('us-dalga', *s.katman('g-us-dalga'), o=belir(A, 3, .25, 3))
    tik(A, 300, 150, 3, .6)
    # s4: sistit — büyük mesane gider, küçük ödemli duvarlı mesane (15–20 mL)
    A.ekle('mesane-kucuk', *s.katman('g-kucuk'), a=(430, 322), p=S([430, 322, 0]),
           s=K((0, [60, 60, 100]), (T(4, .3), [60, 60, 100]), (T(4, .55), [100, 100, 100])), o=belir(A, 4, .3))
    halka(A, 420, 294, 60, 52, 4, renk=KIRMIZI, f1=.6, f2=.98, nm='halka-sistit')
    A.etiket(0, 0, 600, 200, 'Retansiyon: mesane dolar', 'bilgi')
    A.etiket(1, 1, 660, 150, 'Suprapubik kabarıklık', 'bilgi')
    A.etiket(1, 1, 300, 60, 'Kubbe pubisin üstünde', 'bilgi')
    A.etiket(1, 1, 556, 296, 'Pubis', 'bilgi')
    A.etiket(2, 2, 660, 90, 'Suprapubik palpasyon', 'bilgi')
    A.etiket(2, 2, 660, 276, 'Şişlik + dolgunluk', 'bilgi')
    A.etiket(3, 3, 660, 100, 'USG: ağzına kadar dolu', 'dogru')
    A.etiket(3, 3, 660, 144, 'Kateter endikasyonu ✓', 'dogru')
    A.etiket(4, 4, 300, 200, 'Sistit: 15–20 mL', 'uyari')
    A.etiket(4, 4, 560, 200, '"Yapamıyorum" ≠ retansiyon', 'uyari')
    A.etiket(4, 4, 560, 350, 'Kateter gerekmez', 'uyari')
    A.kamera(0, 440, 250, 130)
    A.kamera(1, 470, 215, 130)
    A.kamera(2, 560, 200, 140)
    A.kamera(3, 520, 230, 130)
    A.kamera(4, 430, 290, 170)
    return A


# ———————————————————————— 4. Pelvis travması (travma sahnesi, önden)

def travma(z):
    A = anim(z, 'travma', 'Pelvis kırığı + meatusta kan: kateter yok', [
        B('Kuvvet', 'Yüksekten düşme ya da trafik kazası pelvise büyük bir kuvvet uygular.', 6),
        B('Kırık', 'Pubis kolunda kırık ve simfizde ayrılma oluşabilir.', 6),
        B('Kan', 'Buna erkekte meatusta taze kan eşlik ediyorsa üretra yaralanmış olabilir.', 6),
        B('Karar', 'Kısmi yırtıkta kateteri itmek yırtığı tamamlar; bu hastaya üretral kateter takılmaz.', 8),
    ])
    T = A.T
    s = Sahne2B('travma')
    titre = K((0, [0, 0, 0]), (T(0, .45), [0, 0, 0]), (T(0, .5), [10, 0, 0]), (T(0, .55), [-8, 0, 0]), (T(0, .6), [6, 0, 0]), (T(0, .66), [0, 0, 0]))
    for i, nm, it in _katmanlar(s):
        if i == 't-kirik':
            A.ekle(nm, *it, o=belir(A, 1, .1))              # s1: pubis kolunda kırık çizgileri
        elif i == 't-yirtik':
            A.ekle(nm, *it, o=belir(A, 3, .02))             # s3: membranöz/bulbar düzeyde kısmi yırtık
        elif i == 't-kan':                                   # s2: meatusta taze kan damlası belirir (büyüyerek)
            A.ekle(nm, *it, a=(400, 480), p=S([400, 480, 0]), s=K((0, [0, 0, 100]), (T(2, .2), [0, 0, 100]), (T(2, .55), [125, 125, 100]), (T(2, .75), [100, 100, 100])),
                   o=belir(A, 2, .2))
        elif i in ('t-pelvis', 't-simfiz'):
            A.ekle(nm, *it, p=titre)                         # s0: darbeyle sarsılır
        else:
            A.ekle(nm, *it)
    # s0: iki kuvvet oku (yandan çarpma, yüksekten düşme)
    ok(A, 'M40 262 L168 262', 0, renk=KIRMIZI, w=8, f1=.15, f2=.9, nm='ok-yan')
    ok(A, 'M400 -10 L400 46', 0, renk=KIRMIZI, w=8, f1=.15, f2=.9, nm='ok-ust')
    # s1: simfiz ayrılması vurgusu
    halka(A, 400, 265, 40, 54, 1, renk=KIRMIZI, f1=.5, f2=.95, nm='halka-simfiz')
    # s2: damla vurgusu
    halka(A, 400, 489, 24, 22, 2, renk=KIRMIZI, f1=.6, f2=.98, nm='halka-kan')
    # s3: meatustan itilen kateter yırtığa dayanır → yırtık tamamlanır → ÇARPI
    ilerleyen_kateter(A, 'M400 760 L400 480 L400 372', [(T(3, .05), (400, 480)), (T(3, .4), (400, 372))], w=5, o=A.gor(T(3, .05) - 2))
    halka(A, 400, 346, 34, 26, 3, renk=KIRMIZI, f1=.42, f2=.62, nm='halka-yirtik')
    carpi(A, 400, 420, 3, .62, r=38, son=_son(A))
    A.etiket(0, 0, 640, 60, 'Yüksekten düşme · kaza', 'uyari')
    A.etiket(0, 0, 130, 300, 'Darbe', 'uyari')
    A.etiket(1, 1, 250, 346, 'Pubis kolu kırığı', 'uyari')
    A.etiket(1, 1, 480, 200, 'Simfiz ayrılması', 'uyari')
    A.etiket(2, 2, 520, 400, 'Meatusta taze kan', 'uyari')
    A.etiket(2, 2, 540, 300, 'Üretra yaralanmış olabilir', 'uyari')
    A.etiket(3, 3, 540, 300, 'Kısmi yırtık', 'uyari')
    A.etiket(3, 3, 250, 346, 'Yırtık tamamlanır', 'uyari')
    A.etiket(3, 3, 560, 400, 'Üretral kateter YOK', 'uyari')
    A.kamera(0, 400, 250, 100)
    A.kamera(1, 330, 280, 160)
    A.kamera(2, 400, 400, 170)
    A.kamera(3, 400, 340, 150)
    return A


# ———————————————————————— 5. İdrarın torbaya akışı (foley sahnesi)

AKIS_F = 'M88 199 L200 200 C300 200 320 292 420 292 C500 292 520 200 596 200 L712 200 C778 200 792 254 756 284 C734 304 700 290 672 300'


def idrar_akisi(z):
    A = anim(z, 'idrar-akisi', 'İdrarın torbaya akışı ve ölçümü', [
        B('Delikler', 'İdrar kateterin ucundaki deliklerden girer.', 4),
        B('Drenaj kanalı', 'Kalın drenaj kanalından ve hortumdan torbaya akar.', 5),
        B('Ölçüm', 'Torbadaki çizgilerden saatlik ve yirmi dört saatlik idrar miktarı okunur.', 6),
        B('Sıvı dengesi', 'Bu miktara göre hastaya verilecek sıvıyı ayarlarsın; az verirsen böbrek, fazla verirsen akciğer ve kalp bozulur.', 8),
        B('Boşaltma', 'Torba dolunca altındaki musluktan boşaltılır.', 5),
    ])
    T = A.T
    s = Sahne2B('foley')
    for i, nm, it in _katmanlar(s):  # yerleşmiş kateter (balon şişkin) + torba; akış lümende: gövdenin üstünde, balon/uç/deliklerin altında
        if i == 'f-balon-sonuk' or i == 'f-enjektor':
            continue
        A.ekle(nm, *it)
        if i == 'f-govde':
            A.ekle('akis', G(yol(AKIS_F), st(IDRAR, 3, kesik=(10, 14), kesik_kayma=KD((0, 0), (A.op, -A.op * 3))),
                             tm(K((0, 0), (T(0, .3), 0), (T(0, 1), 16), (T(1, .9), 100)))), o=A.gor(T(0, .3)))
    # s0: deliklere dışarıdan giren idrar (ince çizgiler) + lümende akışın başlangıcı
    A.ekle('giris', *[G(yol(d), st(IDRAR, 2.2, kesik=(5, 6), kesik_kayma=KD((0, 0), (A.op, -A.op * 2)))) for d in
                      ('M64 176 L83 194', 'M98 178 L99 198', 'M118 214 L103 206', 'M78 222 L86 203')], o=belir(A, 0, .15, _son(A)))
    # s2: torbada idrar filmi yükselir (yatay yüzey; 800 mL çizgisi y 418) — s4'te musluktan boşalır
    A.ekle('torba-idrar', G(yol('M-84 -36 L84 -36 L84 -10 C84 -2 78 0 70 0 L-70 0 C-78 0 -84 -2 -84 -10 Z'), fl(IDRAR, o=80)),
           p=S([670, 453, 0]), s=K((0, [100, 0, 100]), (T(1, .9), [100, 0, 100]), (T(2, .9), [100, 100, 100]), (T(4, .3), [100, 100, 100]), (T(4, 1), [100, 12, 100])),
           o=A.gor(T(1, .9)))
    halka(A, 748, 390, 26, 72, 2, renk=MAVI, w=3, f1=.2, f2=.95, nm='halka-olcek')
    # s4: musluk açılır, idrar aşağı boşalır
    halka(A, 679, 475, 30, 28, 4, renk=MAVI, w=3, f1=.05, f2=.5, nm='halka-musluk')
    A.ekle('bosalt', G(yol('M680 490 L680 560'), st(IDRAR, 4, kesik=(8, 7), kesik_kayma=KD((0, 0), (A.op, -A.op * 3)))), o=belir(A, 4, .3, _son(A)))
    A.etiket(0, 0, 90, 150, 'Uçtaki delikler', 'bilgi')
    A.etiket(1, 1, 560, 250, 'Drenaj kanalı → hortum → torba', 'bilgi')
    A.etiket(2, 2, 540, 230, 'Saatlik / 24 saatlik miktar', 'bilgi')
    A.etiket(2, 2, 540, 380, 'Düzey: 800 mL', 'bilgi')
    A.etiket(3, 3, 400, 90, 'Sıvıyı miktara göre ayarla', 'bilgi')
    A.etiket(3, 3, 400, 340, 'Az: böbrek · çok: akciğer/kalp', 'uyari')
    A.etiket(4, 4, 560, 400, 'Musluktan boşalt', 'bilgi')
    A.kamera(0, 110, 200, 220)
    A.kamera(1, 520, 250, 120)
    A.kamera(2, 660, 380, 150)
    A.kamera(3, 400, 250, 100)
    A.kamera(4, 680, 420, 170)
    return A


# ———————————————————————— 6. Kadında alan temizliği (kadin sahnesi)

def _bez(renk):
    """Pens ucunda gazlı bez (yerel 0,0) + pens kolları + steril olmayan (mavi) eldivenli el (sağ-altta)."""
    return [G(yol('M6 4 L150 92 M10 -4 L156 80'), st('#7d8794', 4)), G(el(158, 92, 16, 16), st('#7d8794', 3)), G(el(164, 80, 16, 16), st('#7d8794', 3)),
            yumruk(178, 106, .8, 32, steril=False), G(el(0, 0, 38, 32), fl(renk), st('#5c2508', 1.5)), G(el(-6, -6, 14, 9), fl('#ffffff', o=35))]


def kadin_temizlik(z):
    A = anim(z, 'kadin-temizlik', 'Kadında alan temizliği', [
        B('Hazırlık', 'Ellerini yıkar, steril olmayan eldivenle antiseptikli gazlı bezi alırsın.', 6),
        B('Birinci silme', 'Labium minuslardan majuslara, merkezden dışa doğru dairesel hareketle silersin.', 6),
        B('İkinci silme', 'Dışa ulaşınca yeni bir bezle yeniden merkezden başlarsın.', 5),
        B('Üçüncü silme', 'Bu işlemi üç kez tekrarlarsın; dıştan içe silmek kirli alanı meatusa taşır.', 6),
        B('Steril örtü', 'Sonra steril eldiven giyer, delikli örtüyü meatus açıkta kalacak şekilde yerleştirirsin.', 6),
    ])
    T = A.T
    s = Sahne2B('kadin')
    s.ekle(A)  # uyluklar, mons, labia, vestibül, meatus, vajina, perine
    SP = s.cz('k-temizlik')[0]['d']  # merkezden (meatus altı) dışa spiral
    # s0: povidon kabı (sıvı yarı saydam film); beyaz bez kaba batar, kahverengi çıkar, merkeze gelir
    A.ekle('kap', G(yol('M590 110 C590 96 690 96 690 110 L684 172 C682 184 598 184 596 172 Z'), fl('#e8eef4'), st('#6b7a90', 2.5)),
           G(yol('M593 134 L687 134 L684 172 C682 184 598 184 596 172 Z'), fl('#9a4a18', o=55)), G(el(640, 112, 92, 16), fl('#7a3410', o=60)),
           o=K((0, 0), (T(0, .05), 0), (T(0, .15), 100), (T(0, 1), 100), (T(1, .1), 0)))
    A.ekle('bez-kuru', *_bez('#ffffff'), p=K((0, [560, 50, 0]), (T(0, .2), [560, 50, 0]), (T(0, .45), [640, 124, 0]), (T(0, .58), [640, 124, 0])),
           o=K((0, 0), (T(0, .15), 0), (T(0, .2), 100), (T(0, .57), 100), (T(0, .58), 0)))
    A.ekle('bez-islak', *_bez('#8a3a12'), p=K((0, [640, 124, 0]), (T(0, .58), [640, 124, 0]), (T(0, .95), [400, 214, 0])),
           o=K((0, 0), (T(0, .57), 0), (T(0, .58), 100), (T(0, 1) + 4, 100), (T(1), 0)))
    # s1–s3: üç silme, her biri yeni bezle merkezden dışa; antiseptik filmi (yarı saydam) iz bırakır
    renkler = ['#8a3a12', '#9a4a18', '#b5551d']
    for i in range(3):
        e = K((0, 0), (T(1 + i), 0), (T(1 + i, .9), 100))
        A.ekle(f'iz{i}', G(yol(SP), st(renkler[i], 13 - i * 2, o=38), tm(e)), o=A.gor(T(1 + i)))
        A.ekle(f'bez{i}', *_bez(renkler[i]), p=A.boyunca(SP, T(1 + i), T(1 + i, .9), 80),
               o=K((0, 0), (T(1 + i) - 3, 0), (T(1 + i), 100), (T(1 + i, .92), 100), (T(1 + i, 1), 0)))
    # s3: dıştan içe silme YASAK — içe dönük kırmızı ok + çarpı
    ok(A, 'M560 410 L452 296', 3, renk=KIRMIZI, w=6, f1=.45, f2=.98, nm='ok-icine')
    carpi(A, 506, 352, 3, .7, r=26)
    # s4: steril eldiven giyilir (krem eldivenli el sağdan girer), delikli örtü serilir (meatus açıkta)
    A.ekle('steril-el', yumruk(616, 300, .95, -12, steril=True), p=K((0, [180, 0, 0]), (T(4), [180, 0, 0]), (T(4, .2), [0, 0, 0]), (T(4, .5), [0, 0, 0]), (T(4, .62), [-40, 10, 0])),
           o=K((0, 0), (T(4), 0), (T(4, .04), 100), (T(4, .62), 100), (T(4, .72), 0)))
    A.ekle('ortu', *s.katman('k-ortu'), o=belir(A, 4, .5))
    A.etiket(0, 0, 640, 60, 'Steril olmayan eldiven', 'bilgi')
    A.etiket(0, 0, 640, 220, 'Antiseptikli gazlı bez', 'bilgi')
    for i in range(3):
        A.etiket(1 + i, 1 + i, 560, 110, f'{i + 1}. silme: merkezden dışa', 'bilgi')
    A.etiket(1, 1, 250, 110, 'Minuslardan majuslara', 'bilgi')
    A.etiket(2, 2, 250, 110, 'Yeni bez, yeniden merkez', 'bilgi')
    A.etiket(3, 3, 250, 110, 'Dıştan içe silme yok', 'uyari')
    A.etiket(4, 4, 660, 200, 'Steril eldiven', 'dogru')
    A.etiket(4, 4, 176, 90, 'Delikli örtü: meatus açıkta', 'dogru')
    A.kamera(0, 600, 170, 140)
    A.kamera(1, 400, 250, 140)
    A.kamera(2, 400, 250, 140)
    A.kamera(3, 400, 250, 140)
    A.kamera(4, 400, 250, 100)
    return A


URETICILER = [mahremiyet, malzeme_hazirlik, glob_sistit, travma, idrar_akisi, kadin_temizlik]
