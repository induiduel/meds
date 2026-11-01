"""KMB adım videoları — 2B düz çizgi film hattı, GRUP C3 (adim2b.py bunları toplar).
Adımlar: kadin-temizlik, kadin-yerlestirme, erkek-temizlik, erkek-yerlestirme, idrar-gelmezse, sabitleme.
Her cümle bir bölümdür (ses `o-<adım>`); anatomi/el/araç 2B sahnelerden (Sahne2B: kadin, yakin-el, yakin-uretra, foley),
konu videoları alt kompozisyon (ic_ekle2b: uret2b_a.kadin_temizlik / idrar_akisi, uret2b_b.kadin_ilerleyis / erkek_jel /
yikama_testi / yanlis_balon / balon_sisme, uret2b.erkek_ilerleyis). Burada yalnız koreografi yazılır (docs/KMB_2B_STIL.md);
sahne yazıları Lottie'ye geçmediğinden ölçek/ad bilgisi etiketle verilir. Eski hat (adim_lottie.py) dokunulmadan durur.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ortak2b import *  # noqa: E402,F401,F403
from lottie_dsl import kisi, yumruk  # noqa: E402  (2B paletli eldivenli el, insan figürü)
import uret2b as U0  # noqa: E402
import uret2b_a as UA  # noqa: E402
import uret2b_b as UB  # noqa: E402

MUKOZA = [(0, '#f2b7b0'), (1, '#d98f88')]
MUKOZA_K = '#a85f5a'


def _kart(cx, cy, w, h, kenar, *ic, o=94):
    """Düz stil bilgi kartı: beyaz yuvarlak dikdörtgen + renkli kontur, içinde ikon."""
    return [G(rc(cx, cy, w, h, 14), fl('#ffffff', o=o), st(kenar, 2.5)), *ic]


def _balon_konusma(x, y, w, h, renk, kuyruk='alt'):
    """Konuşma balonu; kuyruk alt-ortada (konuşana doğru)."""
    L, R, T_, B_ = x - w / 2, x + w / 2, y - h / 2, y + h / 2
    d = (f'M{L + 14} {T_} L{R - 14} {T_} C{R} {T_} {R} {T_ + 14} {R} {T_ + 14} L{R} {B_ - 14} C{R} {B_} {R - 14} {B_} {R - 14} {B_} '
         f'L{x + 16} {B_} L{x} {B_ + 22} L{x - 16} {B_} L{L + 14} {B_} C{L} {B_} {L} {B_ - 14} {L} {B_ - 14} L{L} {T_ + 14} C{L} {T_} {L + 14} {T_} {L + 14} {T_} Z')
    return G(yol(d), fl('#ffffff'), st(renk, 3))


def _paket(x, y):
    """Açılmış steril paket (yerel 0,0 merkez): tepsi + açık kapak + içinde halka kateter ve jel tüpü."""
    return [G(rc(0, 0, 150, 92, 8), fl('#fbfaf6'), st('#c9b48a', 2)),
            G(yol('M-75 -46 L75 -46 L56 -96 L-56 -96 Z'), fl('#e8e0cc'), st('#c9b48a', 1.5)),
            G(el(-28, 4, 62, 62), st(KATETER[1], 9)), G(el(-28, 4, 62, 62), st(KATETER[0], 6)),
            G(el(-28, 4, 34, 34), st(KATETER[1], 9)), G(el(-28, 4, 34, 34), st(KATETER[0], 6)),
            G(yol('M-28 -27 C-10 -34 20 -34 44 -28'), st(KATETER[1], 9)), G(yol('M-28 -27 C-10 -34 20 -34 44 -28'), st(KATETER[0], 6)),
            G(rc(42, 14, 48, 22, 6), fl('#eef3f8'), st('#6b7a90', 1.5)), G(rc(70, 14, 10, 12, 2), fl('#6b7a90')), G(yol('M24 14 L54 14'), st(MAVI, 4))]


def _jel_tup(A, k1, k2, nm='tup'):
    """Jel tüpü sağ üstten kateter ucuna eğik gelir, k1→k2 arasında sıkılır (yerel: ağız 0,0; gövde yukarı-sağa)."""
    return [G(yol('M-14 -160 L54 -184 L74 -128 L8 -104 Z'), fl('#eef3f8'), st('#6b7a90', 2)),
            G(yol('M8 -104 L74 -128 L80 -112 L14 -88 Z'), fl('#dfe6ee'), st('#6b7a90', 1.5)),
            G(yol('M20 -166 L50 -176'), st(MAVI, 5)),
            G(yol('M14 -88 L6 -60 L-6 -60 L-10 -84 Z'), fl('#c9d3de'), st('#6b7a90', 1.5))]


# ———————————————————————— 1. Kadında alan temizliği ve steril örtü (kadin_temizlik konu videosu + kadin sahnesi)

def a_kadin_temizlik(A):
    T = A.T
    # konu: s0 hazırlık → 0; s1+s2 birinci/ikinci silme → 1; s3 üçüncü silme (dıştan içe yok) → 2; s4 steril eldiven + örtü → 3
    ic_ekle2b(A, UA.kadin_temizlik, [0, 1, 1, 2, 3], [(0, 3)])
    et(A, 0, 640, 110, 'Eller yıkanır', 'bilgi', .05, .45)
    et(A, 2, 560, 60, '3 kez: alan temizlendi', 'dogru', .05)
    tik(A, 180, 260, 2, .25)
    # s4: delikli örtü serili; yardımcının mavi (steril olmayan) eli sağdan paketi açık uzatır, steril (krem) el soldan alır
    g4 = gorun(A, 4, 4)
    k = Sahne2B('kadin')
    k.ekle(A, dahil=['k-ortu'], o=g4)
    A.ekle('paket', *_paket(0, 0), p=K((0, [900, 230, 0]), (T(4, .06), [900, 230, 0]), (T(4, .36), [640, 230, 0])), o=belir(A, 4, .06, 4))
    A.ekle('yardimci-el', yumruk(0, 0, .75, 0, steril=False), p=K((0, [1040, 242, 0]), (T(4, .06), [1040, 242, 0]), (T(4, .36), [780, 242, 0])), o=belir(A, 4, .06, 4))
    A.ekle('steril-el', yumruk(0, 0, .75, 90, steril=True), p=K((0, [600, 760, 0]), (T(4, .42), [600, 760, 0]), (T(4, .72), [640, 352, 0])), o=belir(A, 4, .42, 4))
    halka(A, 640, 330, 110, 80, 4, renk=YESIL, f1=.75, f2=.98, nm='halka-steril-el')
    et(A, 4, 640, 60, 'Yardımcı: paketi açar, uzatır', 'bilgi', .1)
    et(A, 4, 640, 110, 'Steril el: yalnız sterile', 'dogru', .45)
    A.kamera_sabit(4, 4, 400, 250, 100)


# ———————————————————————— 2. Kadında kateteri ilerletmek (yakin-el sahnesi + kadin_ilerleyis konu videosu)

def a_kadin_yerlestirme(A):
    T = A.T
    h = Sahne2B('yakin-el')
    g01 = gorun(A, 0, 1)
    h.ekle(A, o=g01)  # avuçta halka kateter + dışarıda uç (h-el, h-halka, h-uc); h-jel/h-yanlis gizli
    # s0: jel tüpü sağ üstten ucun üstüne eğilir, sıkılır; damla uca düşer, uçta jel filmi (h-jel) belirir
    A.ekle('tup', *_jel_tup(A, T(0, .25), T(0, .5)), a=(0, -160), p=S([652, 216, 0]),
           s=K((0, [100, 100, 100]), (T(0, .25), [100, 100, 100]), (T(0, .5), [100, 84, 100])), o=belir(A, 0, .04, 0))
    A.ekle('damla', G(el(0, 0, 18, 22), fl(JEL, .75)), G(el(-3, -4, 6, 4), fl('#ffffff', .8)),
           p=K((0, [652, 230, 0]), (T(0, .42), [652, 230, 0]), (T(0, .58), [652, 268, 0])),
           s=K((0, [30, 30, 100]), (T(0, .3), [30, 30, 100]), (T(0, .42), [100, 100, 100])),
           o=K((0, 0), (T(0, .3), 0), (T(0, .34), 100), (T(0, .58), 100), (T(0, .62), 0)))
    A.ekle('jel-uc', *h.katman('h-jel'), a=(626, 280), p=S([626, 280, 0]),
           s=K((0, [20, 60, 100]), (T(0, .58), [20, 60, 100]), (T(0, .85), [100, 100, 100])), o=A.gor(T(0, .58), T(1, 1)))
    et(A, 0, 560, 150, 'Uca ≈2 mL jel yeter', 'bilgi', .1)
    A.kamera(0, 520, 250, 125)
    # s1: avuçtaki halkalar vurgulanır; sarkan uç uyluğa/önlüğe değerse sterilite bozulur (h-yanlis: sarkan parça + çarpı)
    halka(A, 330, 322, 170, 170, 1, f1=.05, f2=.5)
    A.ekle('sarkan', *h.katman('h-yanlis'), o=belir(A, 1, .5, 1))
    et(A, 1, 330, 190, 'Avuçta halka: uç sallanmaz', 'dogru', .05)
    et(A, 1, 250, 370, 'Uç değdi: steril değil', 'uyari', .55)
    A.kamera(1, 400, 370, 100)
    # s2–s4: yakın plan vestibül — parmaklar labiaları ayırır, kateter meatustan girer (konu s1+s2 → 2), 3–4 cm'de idrar (s3 → 3),
    # birkaç santim daha + balon (s4+s5 → 4); konu s0 (anatomi) olmuş bitmiş
    ic_ekle2b(A, UB.kadin_ilerleyis, [None, 2, 2, 3, 4, 4], [(2, 4)], 'ilerle')
    et(A, 2, 200, 110, 'Bir el ayırır, diğeri iter', 'bilgi', .05)
    et(A, 3, 620, 290, 'Büyük kısmı dışarıda kalır', 'bilgi', .5)
    et(A, 4, 200, 330, 'Sonra balonu şişir', 'dogru', .55)


# ———————————————————————— 3. Erkekte temizlik ve lidokainli jel (erkek_jel konu videosu)

def a_erkek_temizlik(A):
    T = A.T
    # konu: s0 prepisyum → 0; s1 temizlik → 1; s2 jel ucu + s3 jeli ver → 3; s4 bekle → 4 (2. cümle kıyas sahnesi)
    ic_ekle2b(A, UB.erkek_jel, [0, 1, 3, 3, 4], [(0, 1), (3, 4)])
    # s1 sonu: temizlik eldiveni (mavi) çıkarılır → steril eldiven (krem) giyilir — kart
    A.kamera_sabit(1, 1, 430, 250, 105)
    A.ekle('eldiven-degis', *_kart(620, 120, 280, 120, MAVI,
                                   yumruk(548, 122, .36, 0, steril=False),
                                   G(yol('M522 96 L574 148 M574 96 L522 148'), st(KIRMIZI, 6)),
                                   G(yol('M600 122 L636 122'), st(MAVI, 5)), G(yol('M624 110 L638 122 L624 134'), st(MAVI, 5)),
                                   yumruk(700, 122, .36, 0, steril=True)),
           o=belir(A, 1, .74, 1))
    et(A, 1, 620, 200, 'Mavi çıkar → steril eldiven', 'dogru', .78)
    # s2: kıyas — kadında kısa üretra, yalnız uca jel; erkekte uzun üretra, tüpün tamamı (daha ağrılı)
    g2 = gorun(A, 2, 2)
    A.kamera_sabit(2, 2, 400, 250, 100)
    zemin(A, nm='zemin-kiyas')
    A.katmanlar[-1]['ks']['o'] = g2
    A.ekle('kadin-u', G(yol('M200 170 L420 170'), st(MUKOZA_K, 40)), G(yol('M200 170 L420 170'), st('#f2b7b0', 34)),
           G(yol('M200 170 L420 170'), st('#f6cfc9', 14)), o=g2)
    A.ekle('kadin-kat', *kateter_cizgi('M60 170 L404 170', 7), G(el(404, 170, 44, 24), fl(JEL, .55)), G(el(398, 166, 14, 6), fl('#ffffff', .8)), o=g2)
    A.ekle('erkek-u', G(yol('M120 330 L700 330'), st(MUKOZA_K, 40)), G(yol('M120 330 L700 330'), st('#f2b7b0', 34)),
           G(yol('M120 330 L700 330'), st('#f6cfc9', 14)),
           G(yol('M700 330 L120 330'), st(JEL, 26, o=55), tm(K((0, 0), (T(2, .35), 0), (T(2, .9), 100)))), o=g2)
    A.ekle('agri', G(yol('M730 280 L716 310 L730 310 L718 342 L752 300 L736 300 L748 280 Z'), fl(SARI), st('#b47a1a', 1.5)), o=belir(A, 2, .3, 2))
    et(A, 2, 300, 110, 'Kadın: kısa üretra · uca jel', 'bilgi', .02)
    et(A, 2, 380, 262, 'Erkek: uzun üretra · tüm jel', 'dogru', .35)
    et(A, 2, 700, 400, 'Daha ağrılı', 'uyari', .3)
    # s3–s4 konu videosundan (jel ucu meatusa, tüp boşalır; parmaklar ucu sıkar, 2–3 dk sayaç)
    et(A, 4, 250, 110, 'Lidokain: anestezi', 'dogru', .55)


# ———————————————————————— 4. Erkekte kateteri sonuna kadar ilerletmek (yakin-el sahnesi + erkek_ilerleyis konu videosu)

SPIRAL = ('M392 300 C392 236 268 236 268 322 C268 386 392 386 392 322 C392 272 290 272 290 322 C290 364 372 364 372 322 '
          'C372 290 312 290 312 322 C312 346 352 346 352 322')
UC_S = 'M392 300 C440 290 560 270 650 282'


def a_erkek_yerlestirme(A):
    T = A.T
    h = Sahne2B('yakin-el')
    g0 = A.gor(0, T(0, .6))
    h.ekle(A, haric=['h-halka', 'h-uc'], o=g0)  # avuç (eldivenli el); silikon kateter burada çizilir
    # s0a: beyaz silikon kateter avuca dolanır (spiral çizilir), uç baş-işaret parmağı arasından dışarı
    A.ekle('silikon-halka', *kateter_cizgi(SPIRAL, 11, SILIKON, e=K((0, 0), (T(0, .04), 0), (T(0, .42), 100))), o=g0)
    A.ekle('silikon-uc', *kateter_cizgi(UC_S, 11, SILIKON), G(el(652, 282, 15, 15), fl(SILIKON[0]), st(SILIKON[1], 1.5)), G(el(654, 281, 4, 4), fl('#4a4a4a')),
           o=A.gor(T(0, .4), T(0, .6)))
    et(A, 0, 330, 190, 'Silikon kateter avuca dolanır', 'dogru', .05, .6)
    # s0b: yanlış tutuş — uçtan gevşek tutulan kateter sarkar, uzun üretrada itilemez (çarpı)
    z0 = A.gor(T(0, .6), T(0, 1))
    zemin(A, nm='zemin-gevsek')
    A.katmanlar[-1]['ks']['o'] = z0
    A.ekle('gevsek-el', yumruk(600, 150, .8, 0, steril=True), o=z0)
    A.ekle('gevsek-kat', *kateter_cizgi('M556 150 C500 170 420 230 360 330', 8, SILIKON), G(el(556, 150, 12, 12), fl(SILIKON[0]), st(SILIKON[1], 1.5)), o=z0)
    A.ekle('gevsek-salinim', G(yol('M380 300 C372 330 356 350 340 360'), st('#8a96a6', 2, kesik=(5, 5))), G(yol('M398 316 C402 338 396 352 386 366'), st('#8a96a6', 2, kesik=(5, 5))), o=z0)
    carpi(A, 430, 240, 0, .7, r=34)
    et(A, 0, 600, 70, 'Uçtan gevşek: ilerlemez', 'uyari', .62)
    A.kamera_sabit(0, 0, 400, 250, 100)
    # s1–s4: erkek kesiti — tutuş + penil üretra → 1; bulbar, sfinkter, prostatik → 2; idrar geldi, yine sonuna kadar → 3; balon → 4
    ic_ekle2b(A, U0.erkek_ilerleyis, ['once', 1, 1, 2, 2, 2, 3, 4], [(1, 4)])
    et(A, 1, 580, 60, 'Meatustan içeri it', 'bilgi', .55)
    et(A, 2, 330, 290, 'Makette takılabilir', 'bilgi', .3)
    et(A, 2, 330, 250, 'Hastada daha kolay', 'dogru', .7)
    et(A, 3, 600, 160, 'Çatal kısmına kadar it', 'dogru', .5)
    et(A, 4, 330, 240, 'Mesane boynunun ötesinde', 'dogru', .4)


# ———————————————————————— 5. Sonuna kadar ittin ama idrar gelmiyor (yikama_testi + yanlis_balon konu videoları)

def a_idrar_gelmezse(A):
    T = A.T
    e = Sahne2B('erkek')
    u = Sahne2B('yakin-uretra')
    # konu yikama_testi: s0 dur → 0; s1 enjektör + s2 ver → 2; s3 mesanede → 3; s4 kıvrım + s5 geri çek → 4
    ic_ekle2b(A, UB.yikama_testi, [0, 2, 2, 3, 4, 4], [(0, 0), (2, 4)])
    # s0: hata — balon kanalına enjektör takılıp şişirilmek istenir → çarpı
    A.ekle('yanlis-enjektor', *e.katman('e-enjektor'), o=belir(A, 0, .4, 0))
    carpi(A, 645, 36, 0, .55, r=26)
    et(A, 0, 560, 160, 'Balonu şişirmek: büyük hata', 'uyari', .45)
    A.kamera_sabit(0, 0, 460, 255, 100)
    # s1: iki neden yan yana — solda gerçekten boş mesane, sağda üretrada takılıp kıvrılmış kateter
    g1 = gorun(A, 1, 1)
    A.kamera_sabit(1, 1, 400, 250, 100)
    zemin(A, nm='zemin-nedenler')
    A.katmanlar[-1]['ks']['o'] = g1
    A.ekle('kart-bos', *_kart(195, 250, 300, 230, MAVI,
                              G(yol('M195 420 L195 262'), st(KATETER[1], 9)), G(yol('M195 420 L195 262'), st(KATETER[0], 6.5)),
                              G(yol('M120 250 C120 190 270 190 270 250 C270 276 240 290 195 292 C150 290 120 276 120 250 Z'), gf(MESANE, (150, 200), (230, 280)), st('#7a2e26', 3)),
                              G(yol('M150 250 C150 222 240 222 240 250 C240 266 220 274 195 276 C170 274 150 266 150 250 Z'), fl('#f3d9d4', .9)),
                              G(yol('M195 292 L195 268'), st(KATETER[1], 9)), G(yol('M195 292 L195 268'), st(KATETER[0], 6.5)),
                              G(el(195, 266, 10, 10), fl(KATETER[0]), st(KATETER[1], 1.5))),
           o=belir(A, 1, .04, 1))
    et(A, 1, 195, 100, '1) Mesane gerçekten boş', 'bilgi', .06)
    A.ekle('kart-kivrim', *_kart(600, 250, 320, 230, KIRMIZI), o=belir(A, 1, .4, 1))
    A.ekle('kivrim-kesit', *u.katman('z-mukoza'), *u.katman('z-kivrim'), a=(400, 250), p=S([600, 250, 0]), s=S([40, 40, 100]), o=belir(A, 1, .4, 1))
    halka(A, 505, 250, 150, 70, 1, renk=KIRMIZI, f1=.55, f2=.98, nm='halka-kivrim')
    et(A, 1, 600, 100, '2) Üretrada takıldı, kıvrıldı', 'uyari', .42)
    # s2–s4 konu videosundan (geniş uçlu enjektör, 30–40 mL, gidip geliyor ✓ / geri gelmiyor ✗ → şişirmeden geri çek)
    # s5–s6: üretrada şişirilen balon — konu yanlis_balon: s0 kıvrılma + s1 soru olmuş bitmiş; s2 gerilme → 5; s3 yırtık + s4 darlık → 6
    ic_ekle2b(A, UB.yanlis_balon, [None, None, 5, 6, 6], [(5, 6)], 'yanlis')
    A.etiketler[:] = [x for x in A.etiketler if x['metin'] != 'Üretra ≈ 1 cm çap']
    A.ekle('kart-genis', *_kart(170, 100, 240, 130, YESIL,
                                G(yol('M80 104 C80 44 260 44 260 104 C260 134 220 150 170 152 C120 150 80 134 80 104 Z'), gf(MESANE, (120, 50), (220, 140)), st('#7a2e26', 3)),
                                G(yol('M100 104 C100 62 240 62 240 104 C240 126 210 138 170 140 C130 138 100 126 100 104 Z'), gf(IDRAR_G, (170, 70), (170, 140)), st('#b47a1a', 1.5)),
                                G(yol('M170 170 L170 130'), st(KATETER[1], 8)), G(yol('M170 170 L170 130'), st(KATETER[0], 5.5)),
                                G(el(170, 118, 26, 22), gf([(0, '#ffffff'), (1, '#d7dee6')], (160, 108), (178, 128), radyal=True), st(YESIL, 2.5))),
           o=K((0, 0), (T(5, .02), 0), (T(5, .06), 100), (T(5, .54), 100), (T(5, .6), 0)))
    tik(A, 262, 60, 5, .2, son=5)
    A.katmanlar[-1]['ks']['o'] = K((0, 0), (T(5, .2), 0), (T(5, .25), 100), (T(5, .54), 100), (T(5, .6), 0))
    et(A, 5, 240, 190, 'Mesanede balon fark edilmez', 'dogru', .04, .56)
    et(A, 5, 180, 110, 'Üretra ≈1 cm: perfore olur', 'uyari', .6)
    A.ekle('inkontinans', damla(700, 170, .9), p=KD(*[(T(6, .12) + k * 14, [0, (k % 3) * 16, 0]) for k in range(max(2, int((T(6, 1) - T(6, .12)) / 14)))]),
           o=belir(A, 6, .12, 6))
    et(A, 6, 640, 60, 'Kalıcı idrar kaçırma', 'uyari', .15, .55)
    et(A, 6, 640, 60, 'Kanama · üretra darlığı', 'uyari', .55)


# ———————————————————————— 6. Balonu şişirmek, torbayı bağlamak ve kayıt (balon_sisme konu videosu + foley sahnesi)

def a_sabitleme(A):
    T = A.T
    # konu balon_sisme: s0 kateter mesanede, s1 enjektör, s2 sıvı, s3 şişme → 0; s4 geri çekme, s5 oturdu → 1
    ic_ekle2b(A, UB.balon_sisme, [0, 0, 0, 0, 1, 1], [(0, 1)])
    et(A, 0, 600, 300, 'Kateter mesanede: emin ol', 'bilgi', .02, .25)
    # s2: foley — torba alttan gelir, hortum kalın drenaj kanalına bağlanır (bağ belirir), idrar torbaya akar; kültür örneği
    g2 = gorun(A, 2, 2)
    f = Sahne2B('foley')
    for k in f.katmanlar:
        i = k['id']
        if i in ('f-balon-sonuk', 'f-enjektor'):
            continue
        import copy
        it = copy.deepcopy(k['it'])
        if i in ('f-torba', 'f-musluk'):
            A.ekle(k['nm'], *it, p=K((0, [0, 180, 0]), (T(2, .04), [0, 180, 0]), (T(2, .28), [0, 0, 0])), o=g2)
        elif i == 'f-torba-bag':
            A.ekle(k['nm'], *it, o=belir(A, 2, .3, 2))
        else:
            A.ekle(k['nm'], *it, o=g2)
            if i == 'f-govde':
                A.ekle('akis-torba', G(yol(UA.AKIS_F), st(IDRAR, 3, kesik=(10, 14), kesik_kayma=KD((T(2, .36), 0), (A.op, -(A.op - T(2, .36)) * 3))),
                                      tm(K((0, 0), (T(2, .36), 0), (T(2, .7), 100)))), o=belir(A, 2, .36, 2))
    halka(A, 660, 200, 120, 40, 2, renk=YESIL, f1=.3, f2=.6, nm='halka-drenaj')
    tik(A, 560, 120, 2, .4, son=2)
    A.ekle('torba-idrar', G(yol('M-84 -36 L84 -36 L84 -10 C84 -2 78 0 70 0 L-70 0 C-78 0 -84 -2 -84 -10 Z'), fl(IDRAR, o=80)),
           p=S([670, 453, 0]), s=K((0, [100, 0, 100]), (T(2, .66), [100, 0, 100]), (T(2, 1), [100, 60, 100])), o=belir(A, 2, .66, 2))
    # kültür: küçük enjektör hortumun örnek alma yerine iner, piston çekilince içine sarı film dolar
    A.ekle('kultur', G(rc(744, 168, 22, 64, 4), fl('#eef3f8', .9), st('#6b7a90', 2)), G(yol('M744 200 L744 228'), st('#5b6676', 3)),
           G(rc(744, 186, 14, 26), fl(IDRAR, .75), s=K((0, [100, 8, 100]), (T(2, .72), [100, 8, 100]), (T(2, .9), [100, 100, 100])), a=(744, 199), p=(744, 199)),
           G(rc(744, 128, 6, 26), fl('#6b7a90'), p=K((0, [0, 10]), (T(2, .72), [0, 10]), (T(2, .9), [0, -14]))),
           G(rc(744, 114, 24, 8, 2), fl('#5b6676'), p=K((0, [0, 10]), (T(2, .72), [0, 10]), (T(2, .9), [0, -14]))),
           p=K((0, [0, -140, 0]), (T(2, .58), [0, -140, 0]), (T(2, .7), [0, 0, 0])), o=belir(A, 2, .58, 2))
    et(A, 2, 520, 250, 'Torba: kalın drenaj kanalına', 'bilgi', .05)
    et(A, 2, 640, 80, 'Gerekirse kültür örneği', 'bilgi', .6)
    A.kamera_sabit(2, 2, 600, 290, 100)
    # s3: kayıt formu — satırlar yazılır, kalem ilerler; maddeler etiketle
    g3 = gorun(A, 3, 3)
    A.kamera_sabit(3, 3, 400, 250, 100)
    zemin(A, nm='zemin-kayit')
    A.katmanlar[-1]['ks']['o'] = g3
    A.ekle('form', G(rc(330, 250, 300, 380, 12), fl('#ffffff'), st('#9aa6b4', 2)), G(rc(330, 86, 120, 22, 6), fl('#9aa6b4')),
           *[G(yol(f'M210 {130 + i * 50} L450 {130 + i * 50}'), st(MAVI, 4), tm(K((0, 0), (T(3, .08 + i * .17), 0), (T(3, .22 + i * .17), 100)))) for i in range(5)], o=g3)
    A.ekle('kalem', G(yol('M0 0 L-56 38'), st('#2b2f36', 8)), G(yol('M-56 38 L-66 44'), st(SARI, 6)),
           p=KD(*[(T(3, .08 + i * .17 + j * .14 / 6), [210 + 240 * j / 6 + 56, 130 + i * 50 - 38, 0]) for i in range(5) for j in range(7)]), o=g3)
    for i, m in enumerate(['Yapılan işlem · kateter', 'Boy · balon hacmi', 'İdrar miktarı · rengi', 'Güçlük yaşandı mı', 'Komplikasyon']):
        et(A, 3, 600, 130 + i * 50, m, 'bilgi', .08 + i * .17)
    # s4: hekim hastaya anlatır — konuşma balonu; hastada (pelvis düzeyinde) yanma simgesi
    g4 = gorun(A, 4, 4)
    A.kamera_sabit(4, 4, 400, 250, 100)
    zemin(A, nm='zemin-anlat')
    A.katmanlar[-1]['ks']['o'] = g4
    A.ekle('hasta', *kisi(250, 130, '#8fc1c9', 1.2), o=g4)
    A.ekle('hekim', *kisi(560, 130, '#ffffff', 1.2, True), o=g4)
    A.ekle('balon-anlat', _balon_konusma(560, 44, 270, 50, MAVI), o=belir(A, 4, .25, 4))
    A.ekle('yanma', G(yol('M250 318 C238 298 246 280 256 266 C262 284 278 290 274 308 C270 322 254 328 250 318 Z'), fl(SARI), st('#b47a1a', 1.5)),
           s=K((0, [60, 60, 100]), (T(4, .5), [60, 60, 100]), (T(4, .62), [110, 110, 100]), (T(4, .74), [100, 100, 100])), a=(256, 300), p=S([256, 300, 0]), o=belir(A, 4, .5, 4))
    et(A, 4, 560, 44, 'Birkaç gün yanma olabilir', 'bilgi', .25)
    et(A, 4, 250, 350, 'Kateter çıkınca: yanma, ağrı', 'uyari', .55)
    et(A, 4, 560, 350, 'Önceden anlat', 'dogru', .8)


ADIMLAR = {'kadin-temizlik': a_kadin_temizlik, 'kadin-yerlestirme': a_kadin_yerlestirme, 'erkek-temizlik': a_erkek_temizlik,
           'erkek-yerlestirme': a_erkek_yerlestirme, 'idrar-gelmezse': a_idrar_gelmezse, 'sabitleme': a_sabitleme}
