"""KMB konu videoları — 2B düz çizgi film hattı, GRUP B: kadin-ilerleyis, erkek-jel, balon-sisme, yikama-testi, yanlis-balon.
Bölüm listeleri (ad, sayı, metin) eski hat (lottie_uret.py) ile birebir aynıdır (ses klibi l-<ad> bu bölümlere zamanlı);
anatomi/el/araç 2B sahnelerden (Sahne2B) gelir, burada yalnız koreografi yazılır. Alt kompozisyon olarak da çağrılır:
yalnız A.ekle / A.etiket / A.sayac / A.kamera / A.gor / A.T kullanılır (docs/KMB_2B_STIL.md, H462/H465).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ortak2b import *  # noqa: E402,F401,F403
from ortak2b import (IDRAR, JEL, KATETER, KIRMIZI, MAVI, YESIL, B, G, K, KD, S, Sahne2B, akis, anim, carpi, damla, el, fl, gf, halka,  # noqa: E402
                     ilerleyen_kateter, kateter_cizgi, ok, ornekle, rc, st, tik, tm, yol, zemin)

# erkek sahnesi: kateterin dış ucu (drenaj ucu, küvetin üstünde) → meatus; e-kateter / e-kivrim katmanlarıyla aynı yol
DIS_UC = 'M704 196 L702 140 C700 100 684 74 650 72 L524 70 C500 70 484 74 484 96 L482 140'
KIVRIM_E = DIS_UC + ' L486 262 L488 352 C490 372 470 388 458 374 C448 360 470 352 480 366'   # e-kivrim yolu (bulbar kıvrım)
PENIL_E = DIS_UC + ' L486 262'                                                                  # dış uç → penil üretra


def kesir(d, q):
    """q noktasının d yolundaki kesri (0–1)."""
    P = ornekle(d, 400)
    return min(range(len(P)), key=lambda i: (P[i][0] - q[0]) ** 2 + (P[i][1] - q[1]) ** 2) / 400


def pencere(A, n, b1, b2, f=8):
    """b1 cümlesinin başında belirir, b2'den sonraki cümle başlayınca kaybolur (sahneler arası boş kare kalmaz)."""
    T = A.T
    return A.gor(T(b1) if b1 > 0 else 0, T(b2 + 1) if b2 + 1 < n else None, f)


def _koseler(g):
    out = []
    for x in g.get('it', []):
        if x['ty'] == 'gr':
            out += _koseler(x)
        elif x['ty'] == 'sh':
            out += x['ks']['k']['v']
        elif x['ty'] in ('el', 'rc'):
            p, s = x['p']['k'], x['s']['k']
            out += [[p[0] - s[0] / 2, p[1] - s[1] / 2], [p[0] + s[0] / 2, p[1] + s[1] / 2]]
    return out


def _kutu(g):
    v = _koseler(g)
    xs, ys = [p[0] for p in v], [p[1] for p in v]
    return min(xs), min(ys), max(xs), max(ys)


def _deger(e, t):
    """Kareli (K/KD) ya da sabit değerin t anındaki değeri (sayı ya da liste)."""
    if not e.get('a'):
        return e['k']
    ks = e['k']
    if t <= ks[0]['t']:
        return ks[0]['s']
    for a, b in zip(ks, ks[1:]):
        if a['t'] <= t <= b['t']:
            f = 0 if b['t'] == a['t'] else (t - a['t']) / (b['t'] - a['t'])
            return [u + (v - u) * f for u, v in zip(a['s'], b['s'])]
    return ks[-1]['s']


def _carp(o1, o2):
    """İki opaklık eğrisini çarpar (örnekleyerek): sahne penceresi × öge görünürlüğü."""
    if o1 is None:
        return o2
    ts = sorted({k['t'] for o in (o1, o2) if o.get('a') for k in o['k']} | {0})
    d = lambda o, t: (lambda v: v[0] if isinstance(v, list) else v)(_deger(o, t))  # noqa: E731
    if len(ts) == 1:
        return S(d(o1, 0) * d(o2, 0) / 100)
    return KD(*[(t, round(d(o1, t) * d(o2, t) / 100, 1)) for t in ts])


def enjektor(A, m, id_, nm, dolu_k, bos_k, o, p=(0, 0), r=0, a=(0, 0), sivi=JEL, kay=None):
    """malzeme sahnesinin enjektörünü (m-enjektor 10 mL / m-genis 50 mL) taşır: gövde sabit; piston (tıpa + çubuk + baş)
    dolu_k'ya dek dışarıda (dolu), bos_k'da sonuna dek itilmiş; silindirdeki sıvı filmi aynı oranda kısalır.
    p: taşıma (dx, dy); r/a: döndürme (a: yerel dayanak, ör. uç); kay: [(kare, dx, dy), …] katmanın ek kayması (gelme).
    Sol uç = kateter ucu, piston sağa doğru çıkar. Üç katman: nm, nm-sivi, nm-piston."""
    kutular = [(_kutu(g), g) for g in m.katman(id_)]
    gx1, gy1, gx2, gy2 = max(kutular, key=lambda kg: kg[0][2] - kg[0][0])[0]     # silindir (en uzun parça)
    yc = (gy1 + gy2) / 2
    tipa = [g for (x1, y1, x2, y2), g in kutular if gx1 < x1 < gx2 and x2 - x1 < 10 and y2 - y1 >= 12 and all(it['ty'] != 'st' for it in g['it'])]
    bas = [g for (x1, _, _, _), g in kutular if x1 >= gx2 - 1]
    sabit = [g for (_, g) in kutular if g not in tipa and g not in bas]
    tx1 = _kutu(tipa[0])[0] if tipa else gx1 + 8
    D = (gx2 - tx1) - 14                                                            # dolu: piston bu kadar dışarıda
    bas_x1 = min(_kutu(g)[0] for g in bas) if bas else gx2 + 20
    cubuk = G(rc((tx1 + 7 + bas_x1) / 2, yc, bas_x1 - tx1 - 7, 5), fl('#6b7a90'))
    P = lambda dx, dy: [p[0] + a[0] + dx, p[1] + a[1] + dy, 0]  # noqa: E731
    konum = K(*[(k, P(dx, dy)) for k, dx, dy in kay]) if kay else S(P(0, 0))
    tr = dict(r=S(r), a=a, o=o)
    A.ekle(nm, *sabit, p=konum, **tr)
    W0 = (tx1 - gx1 - 3) + D
    sx = K((0, [100, 100, 100]), (dolu_k, [100, 100, 100]), (bos_k, [max(2, round((tx1 - gx1 - 3) / W0 * 100, 1)), 100, 100]))
    A.ekle(nm + '-sivi', G(rc(W0 / 2, 0, W0, (gy2 - gy1) - 8), fl(sivi, .55), s=sx, p=(gx1 + 3, yc)), p=konum, **tr)
    A.ekle(nm + '-piston', G(*tipa, cubuk, *bas, p=K((0, [D, 0]), (dolu_k, [D, 0]), (bos_k, [0, 0]))), p=konum, **tr)


# ———————————————————————— 1. Kadında kateterin mesaneye ilerleyişi

V_KATETER = 'M800 70 C690 86 540 130 408 168'      # yakin-kadin: kateter dıştan meatusa (v-kateter yolu)
V_IDRAR = 'M408 168 C540 130 690 86 800 70'        # idrar: meatustan dışa (v-idrar yolu)
Y_IDRAR = ['M280 110 C340 124 376 182 392 206', 'M230 170 C315 184 376 206 392 206', 'M520 120 C460 134 424 182 408 182', 'M560 180 C480 194 424 206 408 182']


def mesane_balon(A, s, k_sis1, k_sis2, k_cek1, k_cek2, o, idrar_k=0, kadin=False):
    """yakin-mesane: kateter ucu mesanede, delikler, idrar akışı; balon k_sis1→k_sis2 şişer, k_cek1→k_cek2 kateter 24 px geri
    çekilir (balon mesane boynuna oturur). Kadında prostat yoktur: yerine kısa üretra duvarı çizilir. Dönüş: geri çekme eğrisi."""
    if kadin:  # kadın: prostat yok; klinik zemin yerine mesane çevresi doku, altında kısa üretra duvarı
        import copy
        A.ekle('doku-kadin', G(rc(400, 250, 800, 500), fl('#efc3ae')), o=o)
        for k in s.katmanlar:
            if k['nm'] == 'arka-0' or k['id'] == 'y-prostat' or k['id'] in s.gizli:
                continue
            A.ekle(k['nm'], *copy.deepcopy(k['it']), o=o)
        A.ekle('uretra-kadin', G(rc(400, 430, 62, 190, 14), gf([(0, '#f2b7b0'), (1, '#d98f88')], (369, 430), (431, 430)), st('#a85f5a', 2.5)),
               G(rc(400, 430, 30, 190), fl('#f6cfc9', .9)), o=o)
    else:
        s.ekle(A, o=o)
    geri = K((0, [0, 0, 0]), (k_cek1, [0, 0, 0]), (k_cek2, [0, 24, 0]))
    for i, d in enumerate(Y_IDRAR):
        A.ekle(f'idrar{i}', G(yol(d), st(IDRAR, 3, kesik=(10, 14), kesik_kayma=KD((idrar_k, 0), (A.op, -(A.op - idrar_k) * 3)))), o=o, p=geri)
    A.ekle('kateter', *s.katman('y-kateter'), o=o, p=geri)
    A.ekle('delik', *s.katman('y-delik'), o=o, p=geri)
    A.ekle('balon-sonuk', *s.katman('y-balon-sonuk'), o=_carp(o, K((0, 100), (k_sis1, 100), (k_sis1 + 6, 0))), p=geri)
    A.ekle('balon', *s.katman('y-balon'), a=(400, 262), p=K((0, [400, 262, 0]), (k_cek1, [400, 262, 0]), (k_cek2, [400, 286, 0])),
           s=K((0, [8, 8, 100]), (k_sis1, [8, 8, 100]), (k_sis2, [100, 100, 100])), o=_carp(o, A.gor(k_sis1)))
    A.ekle('cekme', *s.katman('y-cekme'), o=_carp(o, A.gor(k_cek1 - 6, k_cek2 + 10)))
    return geri


def kadin_ilerleyis(z):
    A = anim(z, 'kadin-ilerleyis', 'Kadında kateterin mesaneye ilerleyişi', [
        B('Anatomi', 'Kadın üretrası kısadır; mesane boynundan öne ve aşağıya, vestibüle uzanır. Arkasında vajina vardır.', 7),
        B('Meatus', 'Labiaları ayırınca meatusu görürsün: klitorisin altında, vajinanın üstündeki küçük açıklık.', 6),
        B('Giriş', 'Ucuna jel sürülmüş kateteri meatustan nazikçe ilerletirsin.', 5),
        B('İdrar', 'Birkaç santimetre sonra uçtaki delikler mesaneye girer ve idrar gelir.', 5),
        B('Birkaç santim daha', 'Balonun da mesaneye girmesi için kateteri birkaç santimetre daha ilerletirsin.', 5),
        B('Balon', 'Balonu şişirip hafifçe geri çektiğinde balon mesane boynuna oturur.', 6),
    ])
    T, n = A.T, 6
    zemin(A)
    # s0: önden litotomi (steril örtü serili); kısa üretra kılavuzu meatustan yukarı (≈ 4 cm = 48 px), mesane boynu, arkada vajina
    k = Sahne2B('kadin')
    k.ekle(A, dahil=['k-ortu'], o=pencere(A, n, 0, 0))
    A.ekle('uretra-kilavuz', G(yol('M400 210 L400 164'), st(MAVI, 3, kesik=(8, 6)), tm(K((0, 0), (T(0, .15), 0), (T(0, .5), 100)))),
           G(yol('M392 172 L400 162 L408 172'), st(MAVI, 3)), o=pencere(A, n, 0, 0))
    halka(A, 400, 314, 44, 70, 0, renk='#a85f5a', f1=.55, f2=.95)
    A.etiket(0, 0, 560, 186, 'Kısa üretra ≈ 4 cm, içeri', 'bilgi')
    A.etiket(0, 0, 560, 314, 'Arkada vajina')
    # s1–s4: yakın plan vestibül; parmaklar labiaları ayırır, meatus halkası
    v = Sahne2B('yakin-kadin')
    v.ekle(A, dahil=['v-parmak'], o=pencere(A, n, 1, 4))
    halka(A, 400, 170, 54, 42, 1, renk=YESIL)
    A.etiket(1, 1, 400, 44, 'Klitoris')
    A.etiket(1, 1, 600, 170, 'Meatus: küçük açıklık', 'dogru')
    A.etiket(1, 1, 400, 320, 'Vajina')
    # s2: jelli uç meatusa girer (uç yolu boyunca ilerler; içeri giren kısım görünmez)
    o_kat = A.gor(T(2) - 2, T(5))
    nokta, ornek = ilerleyen_kateter(A, V_KATETER, [(T(2), (690, 86)), (T(2, .9), (408, 168))], w=12.6, nm='v-kat', o=o_kat, uc=False)
    A.ekle('v-jel', G(el(0, 0, 34, 20), fl(JEL, .5)), G(el(-4, -3, 12, 6), fl('#ffffff', .7)),
           p=KD(*[(kk, [*nokta(f), 0]) for kk, f in ornek]), o=A.gor(T(2) - 2, T(2, .82)))
    # s3–s4: gövde içeri kayar (cm işaretleri meatusa doğru akar: 1 cm ≈ 24 px bu ölçekte)
    isaret = st('#8a5a1a', 12.6, o=55, kesik=(2.5, 45.5), kesik_kayma=KD((T(3), 0), (T(3, 1), -84), (T(4), -84), (T(4, 1), -144)))
    isaret['lc'] = 1  # düz uç: cm işareti ince çizgi kalsın (yuvarlak uç her işareti topağa çevirir)
    A.ekle('v-isaret', G(yol(V_KATETER), isaret), o=A.gor(T(3), T(5)))
    akis(A, V_IDRAR, T(3, .45), renk='#b8860b', w=4, nm='v-idrar', o=A.gor(T(3, .45), T(5)))
    A.etiket(2, 2, 620, 220, 'Jelli uç meatusa', 'bilgi')
    A.etiket(3, 3, 620, 220, '3–4 cm: idrar geldi', 'bilgi')
    ok(A, 'M660 44 L540 80', 4, renk=MAVI)
    A.etiket(4, 4, 620, 220, 'Birkaç santim daha', 'uyari')
    # s5: yakın plan mesane boynu (kadın: prostat yok, kısa üretra duvarı) — balon şişer, hafif geri çekilince boyna oturur
    y = Sahne2B('yakin-mesane')
    o5 = pencere(A, n, 5, 5)
    mesane_balon(A, y, T(5, .05), T(5, .45), T(5, .55), T(5, .8), o5, idrar_k=T(5), kadin=True)
    A.ekle('boyun-halka', G(el(400, 318, 150, 70), st(YESIL, 3, kesik=(6, 6))), o=A.gor(T(5, .8)))
    A.etiket(5, 5, 200, 150, 'Balon mesanede ✓', 'dogru')
    A.etiket(5, 5, 600, 330, 'Hafifçe geri çek: boyna oturur', 'bilgi')
    A.kamera(0, 400, 250, 150)
    A.kamera(1, 400, 210, 115)
    A.kamera(2, 520, 150, 130)
    A.kamera(5, 400, 280, 130)
    return A


# ———————————————————————— 2. Erkekte temizlik ve lidokainli jel

J_TEMIZ = ['M556 236 C520 180 460 140 380 128', 'M552 248 C500 218 420 206 330 212', 'M556 264 C520 320 460 360 380 372']


def erkek_jel(z):
    A = anim(z, 'erkek-jel', 'Erkekte temizlik ve lidokainli jel', [
        B('Prepisyum', 'Sünnetsiz hastada önce prepisyumu geriye çekersin.', 5),
        B('Temizlik', 'Meatustan başlayıp glans boyunca dışa doğru silersin ve bunu üç kez yaparsın.', 8),
        B('Jel ucu', 'Lidokainli jelin ucunu meatusa yerleştirirsin.', 5),
        B('Jeli ver', 'Çok sert basmadan tüpün tamamını üretraya verirsin.', 6),
        B('Bekle', 'Penisin ucunu sıkıca tutarak iki üç dakika beklersin; jeldeki lidokain anestezi sağlar.', 8),
    ])
    T = A.T
    zemin(A)
    j = Sahne2B('yakin-erkek-jel')
    j.ekle(A, haric=['j-prepisyum'])
    # s0: prepisyum glansı örten konumdan (sağda) geriye, koronanın gerisine kayar
    A.ekle('prepisyum', *j.katman('j-prepisyum'), p=K((0, [190, 0, 0]), (T(0, .15), [190, 0, 0]), (T(0, .85), [0, 0, 0])))
    ok(A, 'M470 92 L330 92', 0, renk=MAVI, f1=.15, f2=.95)
    A.etiket(0, 0, 250, 60, 'Prepisyum geriye', 'bilgi')
    # s1: üç silme: meatustan dışa doğru yay; gazlı bez yayı izler
    for i, d in enumerate(J_TEMIZ):
        k1, k2 = T(1, (i + .05) / 3), T(1, (i + .9) / 3)
        A.ekle(f'temiz{i}', G(yol(d), st(YESIL, 3.5, kesik=(8, 6)), tm(K((0, 0), (k1, 0), (k2, 100)))), o=A.gor(k1 - 2, T(2)))
        A.ekle(f'bez{i}', G(el(0, 0, 30, 30), fl('#f6ead8'), st('#9a4a18', 2.5)), G(el(-4, -4, 12, 8), fl('#ffffff', .8)),
               p=A.boyunca(d, k1, k2, 40), o=A.gor(k1 - 2, k2 + 2))
    A.etiket(1, 1, 400, 60, 'Meatustan dışa · 3 kez', 'bilgi')
    # s2: jel tüpü sağdan gelir, ucu meatusa oturur. Parçalar: uç, silindir, dolgu, tıpa (704–710), flanş (744–752), çubuk (752+), baş
    sir = j.katman('j-siringa')
    piston = [g for g in sir if _kutu(g)[0] >= 752 or 703 < _kutu(g)[0] < 706]
    govde = [g for g in sir if g not in piston]
    gel = K((0, [250, 0, 0]), (T(2), [250, 0, 0]), (T(2, .7), [0, 0, 0]), (T(4), [0, 0, 0]), (T(4, .3), [250, 0, 0]))
    A.ekle('siringa', *govde, p=gel)
    A.ekle('siringa-sivi-ortu', G(rc(-46, 0, 92, 24), fl('#eef3f8'), s=K((0, [0, 100, 100]), (T(3), [0, 100, 100]), (T(3, .95), [100, 100, 100])), p=(704, 250)),
           o=A.gor(T(3), T(4, .1)))
    A.ekle('siringa-piston', G(*piston, p=K((0, [0, 0]), (T(3), [0, 0]), (T(3, .95), [-88, 0]))), p=gel)
    halka(A, 566, 250, 30, 40, 2, renk=YESIL, f1=.6)
    A.etiket(2, 2, 660, 150, 'Jel ucu meatusta', 'bilgi')
    # s3: jel üretraya dolar (yarı saydam film, meatustan içeri)
    A.ekle('dolum', G(yol('M556 250 L0 250'), st(JEL, 22, o=60), tm(K((0, 0), (T(3), 0), (T(3, .95), 100)))))
    A.etiket(3, 3, 250, 60, 'Jelin tamamı üretraya', 'bilgi')
    # s4: tüp çekilir; üstten ve alttan parmak uçları glansı sıkar; süre sayacı
    A.ekle('parmak', *j.katman('j-parmak'), a=(515, 250), p=S([515, 250, 0]),
           s=K((0, [100, 114, 100]), (T(4, .25), [100, 114, 100]), (T(4, .5), [100, 100, 100])), o=A.gor(T(4, .15)))
    A.sayac(4, .3, 4, 1, 0, 3, 'dk', 680, 120, 1)
    A.etiket(4, 4, 250, 60, 'Ucu tut · 2–3 dk bekle', 'dogru')
    A.kamera(0, 330, 250, 130)
    A.kamera(1, 450, 250, 120)
    A.kamera(2, 600, 250, 140)
    A.kamera(3, 400, 250, 110)
    A.kamera(4, 480, 250, 120)
    return A


# ———————————————————————— 3. Balonun şişirilmesi

def balon_sisme(z):
    A = anim(z, 'balon-sisme', 'Balonun şişirilmesi ve mesane boynuna oturtulması', [
        B('Kateter mesanede', 'Kateterin ucu mesanede; uçtaki deliklerden idrar geliyor.', 5),
        B('Enjektör', 'İnce, valfli balon kanalına steril izotonikle dolu enjektörü takarsın.', 6),
        B('Sıvı', 'Pistonu yavaşça ittiğinde sıvı balon kanalında ilerler.', 5),
        B('Şişme', 'Balon şişer; hasta ağrı tarif ederse durur, balonu indirip kateterin yerini yeniden değerlendirirsin.', 8),
        B('Geri çekme', 'Kateteri hafifçe geri çektiğinde direnç hissedersin.', 5),
        B('Oturdu', 'Balon artık mesane boynuna oturmuştur; kateter basit çekiştirmeyle çıkmaz.', 6),
    ])
    T = A.T
    zemin(A)
    y = Sahne2B('yakin-mesane')
    m = Sahne2B('malzeme')
    geri = mesane_balon(A, y, T(3), T(3, .75), T(4, .15), T(4, .7), None, idrar_k=0)
    halka(A, 400, 194, 34, 40, 0, renk=YESIL)
    A.etiket(0, 0, 200, 130, 'Uçtaki delikler: idrar girer', 'bilgi')
    # s1: balon kanalı (kateter içindeki ince hat) vurgulanır; izotonikle dolu 10 mL enjektör sağ üstte pano içinde gelir
    A.ekle('kanal-vurgu', G(yol('M395 500 L395 262'), st(MAVI, 3, kesik=(6, 6))), o=A.gor(T(1, .1), T(2)), p=geri)
    o_enj = A.gor(T(1) - 2, T(4))
    gel = [(0, 260, 0), (T(1), 260, 0), (T(1, .6), 0, 0)]
    A.ekle('enj-pano', G(rc(680, 66, 232, 72, 12), fl('#ffffff', .96), st('#6b7a90', 2)), p=K(*[(k, [dx, dy, 0]) for k, dx, dy in gel]), o=o_enj)
    enjektor(A, m, 'm-enjektor', 'enj', T(2), T(3, .75), o_enj, p=(140, -188), kay=gel)
    A.etiket(1, 1, 560, 150, 'Balon kanalı + enjektör', 'bilgi')
    # s2: piston itilir, sıvı kanalda ilerler (mavi ince film), sayaç 0→10 mL
    A.ekle('kanal-sivi', G(yol('M395 500 L395 262'), st(MAVI, 2.6), tm(K((0, 0), (T(2), 0), (T(2, 1), 100)))), o=A.gor(T(2)), p=geri)
    A.sayac(2, 0, 3, .75, 0, 10, 'mL', 560, 140)
    A.etiket(2, 2, 560, 300, 'Sıvı kanalda ilerliyor', 'bilgi')
    # s3: balon şişer (mesane_balon); ağrı uyarısı
    A.etiket(3, 3, 200, 300, 'Ağrı olursa dur', 'uyari')
    # s4: hafif geri çekme (ok sahneden), direnç
    A.etiket(4, 4, 600, 330, 'Hafifçe çek: direnç', 'bilgi')
    # s5: boyunda oturdu
    A.ekle('boyun-halka', G(el(400, 318, 150, 70), st(YESIL, 3, kesik=(6, 6))), o=A.gor(T(5)))
    A.etiket(5, 5, 250, 330, 'Balon mesane boynunda ✓', 'dogru')
    A.kamera(0, 400, 200, 150)
    A.kamera(1, 520, 150, 125)
    A.kamera(2, 500, 220, 120)
    A.kamera(3, 400, 260, 150)
    A.kamera(4, 400, 290, 140)
    A.kamera(5, 400, 290, 130)
    return A


# ———————————————————————— 4. Yıkama testi (idrar gelmedi)

def yikama_testi(z):
    A = anim(z, 'yikama-testi', 'İdrar gelmedi: izotonik yıkama testi', [
        B('Dur', 'Kateteri sonuna kadar ittin ama idrar gelmiyor; balonu şişirmeden durursun.', 6),
        B('Enjektör', 'Geniş uçlu kateter enjektörünü kateterin drenaj ucuna takarsın.', 5),
        B('Ver', 'Otuz kırk mililitre steril izotonik verirsin.', 5),
        B('Birinci olasılık', 'Sıvı rahatça gidip rahatça geri çekiliyorsa kateter mesanededir; balonu şişirebilirsin.', 8),
        B('İkinci olasılık', 'Sıvı zor gidiyor ve hiç geri gelmiyorsa kateter üretrada kıvrılmıştır.', 7),
        B('Geri çek', 'Bu durumda balonu şişirmeden kateteri geri çekersin.', 5),
    ])
    T, n = A.T, 6
    zemin(A)
    e = Sahne2B('erkek')
    u = Sahne2B('yakin-uretra')
    m = Sahne2B('malzeme')
    o_e = K((0, 100), (T(3) - 8, 100), (T(3), 0), (T(5) - 8, 0), (T(5), 100))
    e.ekle(A, o=o_e)
    # s0: kateter sonuna dek itilmiş, idrar yok (drenaj ucunda çarpı), balon şişirilmez
    A.ekle('kateter', *e.katman('e-kateter'), o=A.gor(0, T(3) - 8))
    carpi(A, 668, 178, 0, fr=.25, r=18)
    A.etiket(0, 0, 560, 100, 'İdrar yok → şişirme!', 'uyari')
    # s1: 50 mL kateter uçlu enjektör drenaj ucuna (704,196) takılır: ucu yukarı (75° döndürülmüş), gövde aşağı-sağa
    o_enj = A.gor(T(1) - 2, T(3) - 8)
    enjektor(A, m, 'm-genis', 'genis', T(2), T(2, .95), o_enj, p=(704 - 618, 206 - 248), r=75, a=(618, 248),
             kay=[(0, 60, 160), (T(1), 60, 160), (T(1, .7), 0, 0)])
    A.etiket(1, 1, 560, 110, 'Geniş uçlu enjektör', 'bilgi')
    # s2: piston itilir; izotonik kateter içinde penil üretraya dek ilerler; sayaç 0→40 mL
    akis(A, PENIL_E, T(2), T(2, 1), renk=MAVI, w=3, nm='sivi-ver', o=A.gor(T(2), T(3) - 8))
    A.sayac(2, 0, 2, 1, 0, 40, 'mL', 520, 300)
    A.etiket(2, 2, 560, 110, '30–40 mL izotonik', 'bilgi')
    # s3: yakın plan üretra — düz kateter, sıvı rahat gidiyor (sağa, mesaneye) ve rahat geri geliyor (sola): mesanede ✓
    o_u = pencere(A, n, 3, 4)
    u.ekle(A, o=o_u)
    A.ekle('duz', *u.katman('z-dogru'), o=pencere(A, n, 3, 3))
    akis(A, 'M0 250 L800 250', T(3), T(3, .5), renk=MAVI, w=5, nm='git', o=A.gor(T(3), T(3, .5)), hiz=5)
    akis(A, 'M800 250 L0 250', T(3, .5), T(3, 1), renk=YESIL, w=5, nm='gel', o=A.gor(T(3, .5), T(4)), hiz=5)
    tik(A, 700, 330, 3, fr=.6)
    A.etiket(3, 3, 400, 330, 'Gidip geliyor: mesanede ✓', 'dogru')
    # s4: kıvrılmış kateter — sıvı zor gidiyor, kıvrımda duruyor, geri gelmiyor ✗
    A.ekle('kivrim', *u.katman('z-kivrim'), o=pencere(A, n, 4, 4))
    akis(A, 'M0 250 L232 250', T(4), T(4, .7), renk=MAVI, w=5, nm='git-zor', o=A.gor(T(4), T(4, .7)), hiz=1.2)
    carpi(A, 285, 140, 4, fr=.45, r=26)
    A.etiket(4, 4, 560, 330, 'Geri gelmiyor: kıvrım', 'uyari')
    # s5: erkek sahnesi — kıvrımlı kateter balon şişirilmeden geri çekilir (uç kıvrımdan penil üretraya döner)
    f_kiv = kesir(KIVRIM_E, (486, 262))
    A.ekle('kivrim-geri', *kateter_cizgi(KIVRIM_E, 6.5, KATETER, e=K((0, 100), (T(5, .1), 100), (T(5, .9), round(f_kiv * 100, 1)))), o=A.gor(T(5) - 2))
    ok(A, 'M530 330 L530 190', 5, renk=MAVI, f1=.15, f2=.95)
    A.etiket(5, 5, 600, 110, 'Şişirmeden geri çek', 'uyari')
    A.kamera(0, 470, 250, 140)
    A.kamera(1, 620, 260, 150)
    A.kamera(2, 560, 220, 130)
    A.kamera(3, 400, 250, 100)
    A.kamera(4, 320, 250, 130)
    A.kamera(5, 480, 260, 140)
    return A


# ———————————————————————— 5. Üretrada şişirilen balon

def yanlis_balon(z):
    A = anim(z, 'yanlis-balon', 'Üretrada şişirilen balon: ne olur?', [
        B('Kıvrılma', 'Kateter bulbar üretrada bir yere takıldı ve kıvrıldı; idrar gelmiyor.', 6),
        B('Soru', 'Bu durumda balon şişirilirse ne olacağını görelim.', 4),
        B('Gerilme', 'Yaklaşık bir santimetre çapındaki üretra balonla zorla genişler.', 6),
        B('Yırtık', 'Mukoza yırtılır ve kanama başlar; balon sfinkter düzeyindeyse hasta kalıcı inkontinans olur.', 8),
        B('Darlık', 'Uzun dönemde bu bölgede üretra darlığı gelişir. Kural basit: idrar yoksa şişirme yok.', 7),
    ])
    T, n = A.T, 5
    zemin(A)
    e = Sahne2B('erkek')
    u = Sahne2B('yakin-uretra')
    # s0: kateter bulbar üretrada kıvrılmış, idrar yok
    o_e = pencere(A, n, 0, 1)
    e.ekle(A, o=o_e)
    A.ekle('kivrim', *e.katman('e-kivrim'), o=o_e)
    halka(A, 470, 372, 42, 32, 0, renk=KIRMIZI)
    carpi(A, 668, 178, 0, fr=.3, r=18)
    A.etiket(0, 0, 600, 110, 'Takıldı, kıvrıldı', 'uyari')
    A.etiket(0, 0, 540, 200, 'İdrar gelmiyor')
    # s1: balon kanalına enjektör takılı; küçük kırmızı balon kıvrımda belirmeye başlar
    A.ekle('enjektor', *e.katman('e-enjektor'), o=A.gor(T(1, .1), T(2)))
    A.ekle('balon-y', *e.katman('e-balon-yanlis'), a=(470, 372), p=S([470, 372, 0]),
           s=K((0, [10, 10, 100]), (T(1, .55), [10, 10, 100]), (T(1, 1), [100, 100, 100])), o=A.gor(T(1, .55), T(2)))
    A.etiket(1, 1, 560, 110, 'Şişirirsek?', 'bilgi')
    # s2–s4: yakın plan üretra kesiti; mukoza 1 cm çap; balon şişer, duvar zorla gerilir
    o_u = pencere(A, n, 2, 4)
    u.ekle(A, haric=['z-mukoza'], o=o_u)
    A.ekle('mukoza', *u.katman('z-mukoza'), a=(400, 250), p=S([400, 250, 0]),
           s=K((0, [100, 100, 100]), (T(2, .1), [100, 100, 100]), (T(2, .9), [100, 200, 100]), (T(4, .15), [100, 200, 100]), (T(4, .7), [100, 55, 100])), o=o_u)
    A.ekle('kateter-duz', *kateter_cizgi('M0 250 L800 250', 20, KATETER), o=A.gor(T(2) - 2, T(4, .3)))
    A.ekle('balon', *u.katman('z-balon'), a=(560, 250), p=S([560, 250, 0]),
           s=K((0, [8, 8, 100]), (T(2, .1), [8, 8, 100]), (T(2, .9), [100, 100, 100]), (T(4, .15), [100, 100, 100]), (T(4, .6), [0, 0, 100])), o=o_u)
    A.etiket(2, 2, 180, 110, 'Üretra ≈ 1 cm çap', 'bilgi')
    A.etiket(2, 2, 560, 110, 'Zorla genişliyor', 'uyari')
    # s3: mukoza yırtılır, kan meatusa doğru akar (sola); sfinkter düzeyi uyarısı
    A.ekle('yirtik', *u.katman('z-yirtik'), o=A.gor(T(3, .1), T(4, .6)))
    akis(A, 'M470 266 L0 266', T(3, .3), renk='#b3201f', w=4, nm='kan', o=A.gor(T(3, .3), T(4, .4)))
    A.ekle('kan-damla', damla(500, 318, .8, '#b3201f'), damla(620, 322, .7, '#b3201f'), o=A.gor(T(3, .45), T(4, .5)))
    A.etiket(3, 3, 150, 110, 'Yırtık + kanama', 'uyari')
    A.etiket(3, 3, 400, 110, 'Sfinkter: inkontinans', 'uyari')
    # s4: balon ve kateter gider; mukoza daralır (darlık); kural
    carpi(A, 400, 250, 4, fr=.6, r=46)
    A.etiket(4, 4, 400, 110, 'Darlık gelişir', 'uyari')
    A.etiket(4, 4, 400, 330, 'İdrar yoksa şişirme yok', 'uyari')
    A.kamera(0, 500, 290, 150)
    A.kamera(1, 540, 200, 125)
    A.kamera(2, 400, 250, 100)
    A.kamera(3, 420, 250, 120)
    A.kamera(4, 400, 250, 100)
    return A


URETICILER = [kadin_ilerleyis, erkek_jel, balon_sisme, yikama_testi, yanlis_balon]
