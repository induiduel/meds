"""k2-15 Şizofrenik Bozukluklar — ara resim Lottie hareket planı.

Varsayılan: SVG yapıları belge sırasıyla (_oto_ara). Zayıf kalan resimler (r09, r10, r11, r14) adimlar sırasıyla elle
yazılmıştır; koordinatlar SVG kaynağından, nöron/kişi <use> simgeleri çözülmüş konumlarıyla.
"""
from lottie_uret import *  # noqa: F401,F403
from ._oto_ara import plan, bul, kullanimlar

KEY = 'k2-15-sizofrenik-bozukluklar'
PLAN = plan(KEY)


def r09():
    # 1 süre: 1 ay / 6 ay sınırları; 4 gidiş: üç işlevsellik eğrisi; 2–3 belirti tablosu sütun sütun, negatif satırı
    k = [iz('M470 140 L470 430', KIRMIZI, 7, 2, 18, 45), iz('M800 140 L800 430', KIRMIZI, 7, 10, 26, 45)]
    for i, (bas, h) in enumerate([('M330 190 C360', YESIL), ('M330 290 C360', TURUNCU), ('M330 390 C360', MOR)]):
        d = bul(KEY, 'r09', bas)
        t = 22 + i * 22
        k += [iz(d, h, 11, t, t + 30, 40), isaretci(d, h, t, t + 30, r=7)]
    k.append(iz(bul(KEY, 'r09', 'M780 300 C860'), TURUNCU, 9, 92, 112, 45))
    for j, x in enumerate((561, 791, 1021)):
        for i, y in enumerate((559, 593, 627, 661)):
            k.append(nabiz(halka(x, y, 17), YESIL, 108 + j * 10 + i * 2, 18, 22, 3))
    k += [nabiz(halka(560, 696, 18), KIRMIZI, 142, 24, 40), nabiz(halka(791, 695, 17), YESIL, 148, 22, 30, 3),
          nabiz(halka(1021, 695, 17), YESIL, 150, 22, 30, 3)]
    return k


def r10():
    # A: çubuklar sırayla dolar (risk akrabalıkla artar); adım 1 (%10), 2 (%17, %47), 3 (ikizler) vurgulanır; B: ikizler, antisipasyon
    sonlar = [338, 370, 402, 431, 452, 452, 661, 668]
    k = []
    for i, x2 in enumerate(sonlar):
        y = 172 + i * 50
        k.append(iz(f'M332 {y} L{x2 - 4} {y}', MAVI, 18, 4 + i * 6, 16 + i * 6, 35))
    for t, i, h in [(64, 2, MAVI), (80, 4, TURUNCU), (86, 5, TURUNCU), (92, 7, KIRMIZI), (108, 6, MOR), (114, 3, MOR)]:
        y = 172 + i * 50
        k.append(nabiz(rc(330 + (sonlar[i] - 330) / 2, y, sonlar[i] - 330 + 20, 36, 10), h, t, 22, 28, 4))
    kisi = kullanimlar(KEY, 'r10', 'kisi')
    for j, (x, y, s) in enumerate(kisi):
        k.append(nabiz(halka(x, y - 58 * s, 18 * s + 6), MOR, 108 + j * 6, 22, 30, 4))
    k.append(iz(bul(KEY, 'r10', 'M880 290 C900'), MOR, 8, 116, 130, 45))
    k += [nabiz(kutu(830, 430, 36, 36, 2, 5), MAVI, 134, 20, 30, 4),
          gecis(848, 468, 848, 524, '#c7d2fe', 140, 156, 7),
          nabiz(halka(848, 548, 24), KIRMIZI, 154, 22, 35, 4)]
    return k


def r11():
    # 1: sağlıklı → şizofreni kesiti: korteks, genişlemiş sulkus ve ventriküller; 2: ilişkili özellikler; 3: arkadan öne olgunlaşma
    k = [nabiz(yol(bul(KEY, 'r11', 'M347.9 320.0')), GRI, 2, 22, 20, 3)]
    k.append(nabiz(yol(bul(KEY, 'r11', 'M727.9 320.0')), '#be185d', 18, 22, 30, 4))
    for i, bas in enumerate(['M457 280', 'M509 224', 'M671 224', 'M723 280', 'M723 360', 'M457 360']):
        k.append(iz(bul(KEY, 'r11', bas), '#be185d', 12, 30 + i * 3, 40 + i * 3, 45))
    for i, bas in enumerate(['M576 283', 'M604 283']):
        k.append(nabiz(yol(bul(KEY, 'r11', bas)), MAVI, 52 + i * 4, 24, 40, 4))
    for i, y in enumerate((193, 221.1, 249.2, 277.3, 357.4, 385.5, 413.6, 441.7)):
        k.append(nabiz(halka(839, y, 9), MAVI if i < 4 else '#be185d', 80 + i * 6 + (8 if i >= 4 else 0), 16, 30, 3))
    k.append(nabiz(yol(bul(KEY, 'r11', 'M135.6 710.4')), '#be185d', 136, 20, 25, 3))
    d = bul(KEY, 'r11', 'M262 652 C230')
    k += [iz(d, KIRMIZI, 9, 140, 165, 45), isaretci(d, KIRMIZI, 140, 165, r=7)]
    return k


def r14():
    # 1: sağlıklı ve şizofreni nöronları (küçük); 2: sinaps sayısı; 3: gliozis yok; C: kuram dayanakları gelişim kusuruna akar
    k = []
    nor = kullanimlar(KEY, 'r14', 'noron')
    for i, (x, y, s) in enumerate(nor):
        sag = x > 420
        k.append(nabiz(halka(x, y, 16 * s + 5), KIRMIZI if sag else GRI, (24 if sag else 2) + (i % 5) * 4, 18, 30 if sag else 18, 3))
    for i, (x, y, s) in enumerate(kullanimlar(KEY, 'r14', 'sinaps')):
        sag = x > 420
        k.append(nabiz(halka(x, y, 8), TURUNCU, (66 if sag else 50) + (i % 6) * 2, 16, 35 if sag else 15, 3))
    k.append(nabiz(yol(bul(KEY, 'r14', 'M860 230 C860')), YESIL, 92, 22, 25, 4))
    for i, (bas) in enumerate(['M940 230', 'M955 249', 'M928 243', 'M909 260', 'M907 238', 'M882 230', 'M908 222', 'M910 200', 'M928 217', 'M955 212']):
        k.append(iz(bul(KEY, 'r14', bas), YESIL, 6, 98 + i * 1.5, 104 + i * 1.5, 50))
    for i, x in enumerate((60, 290, 520, 750)):
        t = 116 + i * 9
        k.append(nabiz(kutu(x, 612, 214, 64, 12, 4), '#4338ca', t, 18, 28, 3))
        cx = x + 107
        k.append(iz(f'M{cx} 678 C{cx} 694 1000 686 1010 652', '#4338ca', 5, t + 4, t + 22, 45))
        k.append(gecis(cx, 680, 1010, 652, '#a5b4fc', t + 4, t + 24, 6))
    k.append(nabiz(rc(1070, 652, 104, 64, 16), KIRMIZI, 160, 16, 35, 4))
    return k


PLAN.update(r09=r09, r10=r10, r11=r11, r14=r14)
