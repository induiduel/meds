#!/usr/bin/env python3
"""KMB Lottie videoları (A8) — 02 Üretral kateter.
  python3 meds/scripts/kmb/lottie_uret.py        → src/data/kmb/lottie/<ad>.json + lottie/index.json
Bölüm anlatımları EMA ile `l-<ad>` klibine okunur (scripts/kmb/ses.py); ses üretildiyse bu betik yeniden çalıştırılınca
bölüm sınırları ses zamanlarına oturur. Ön yüz: src/components/kmb/LottieVideo.tsx. DSL: lottie_dsl.py.
İçerik kuralı: anlatım yalnız hocanın kaydı + KMB belgesindeki bilgiyi kullanır (docs/KMB_GORSEL_ASISTAN.md §1)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lottie_dsl import FR, Anim, G, K, KD, S, el, fl, fl_cift, gf, kisi, yatan_hasta, parmak_ucu, rc, st, tm, yol, yol_morph, yumruk  # noqa: E402

MEDS = Path(__file__).resolve().parents[2]
CIKTI = MEDS / 'src/data/kmb/lottie'
SES = MEDS / 'src/data/kmb/ses_02.json'

# ortak renkler
DERI = [(0, '#f6d6bd'), (.7, '#e9b896'), (1, '#d49a76')]
MESANE = [(0, '#f6c2bb'), (.7, '#e39a92'), (1, '#c8746c')]
IDRAR = [(0, '#fff3b8'), (1, '#f2cf55')]
KEMIK = [(0, '#fbf6e9'), (.75, '#eadfc4'), (1, '#cdbd98')]
ZEMIN = [(0, '#fbfcfd'), (1, '#e1e7ee')]
URETRA_E = 'M300 236 L300 305 C300 345 330 362 372 352 L470 320 L700 302'
KATETER_Y = 'M730 302 L700 302 L470 320 L372 352 C330 362 300 345 300 305 L300 138'
KATETER_E = 'M790 302 L700 302 L470 320 L372 352 C330 362 300 345 300 305 L300 138'


_IC = None  # lottie_dsl.ic_ekle ayarlar: üretici alt kompozisyon olarak çalışır


def _anim(z, ad, baslik, bolumler, _z=None):
    return _IC if _IC is not None else Anim(ad, baslik, bolumler, z)


def B(baslik, metin, sure):
    return {'baslik': baslik, 'metin': metin, 'sure': sure}


def zemin(A):
    A.ekle('zemin', G(rc(400, 250, 800, 500), gf(ZEMIN, (400, 150), (400, 650), radyal=True)))


BAGIRSAK = [(170, 70, 96, 60), (255, 58, 104, 64), (345, 70, 100, 60), (215, 118, 92, 52), (310, 115, 88, 52)]


def pelvis_zemin(A, kadin=False):
    """Ortak pelvis yan kesiti: boşluk, bağırsak kıvrımları + mezenter çizgisi, periton, sakrum (vertebra çizgili), koksiks,
    rektum (mukoza kıvrımlı), levator ani, karın duvarı (deri / yağ / rektus kası), simfiz pubis (kortikal + ilik)."""
    zemin(A)
    A.ekle('bosluk', G(yol('M60 20 L470 20 C470 120 468 190 452 250 C440 300 420 340 390 380 L340 430 L240 440 C170 440 120 400 95 330 C70 260 60 140 60 20 Z'), fl('#f4e4dc')))
    A.ekle('bagirsak', *[G(el(x, y, w, h), gf([(0, '#f3d0c3'), (1, '#d9a594')], (x - w / 4, y - h / 4), (x + w / 2, y + h / 2), radyal=True), st('#c58b7a', 1.5),
                           ) for x, y, w, h in BAGIRSAK],
           *[G(yol(f'M{x - w * .3} {y} C{x - w * .1} {y - h * .3} {x + w * .1} {y - h * .3} {x + w * .3} {y}'), st('#c58b7a', 1.2, o=60)) for x, y, w, h in BAGIRSAK])
    A.ekle('periton', G(yol('M100 150 C180 160 240 150 300 150 C360 150 420 140 455 150'), st('#b48a7a', 1.5, kesik=(5, 4), o=80)))
    A.ekle('sakrum', G(yol('M60 30 C95 40 118 70 128 120 C138 175 138 230 130 280 C124 315 112 340 100 355 L82 350 C92 320 100 290 104 250 C108 200 104 140 92 100 C84 74 72 54 60 46 Z'),
                       gf(KEMIK, (80, 100), (140, 300)), st('#a8946b', 2)),
           *[G(yol(f'M{96 + (y - 85) * .1} {y} L{122 + (y - 85) * .1} {y + 6}'), st('#b9a479', 1.5)) for y in (85, 125, 165, 205, 245)],
           G(yol('M100 355 C104 372 112 384 124 392'), st('#a8946b', 7)))
    rek = 'M128 70 C160 110 168 170 170 220 C172 270 180 320 205 360 L238 410' if not kadin else 'M128 70 C160 110 168 170 170 220 C172 270 190 330 230 380 L262 430'
    A.ekle('rektum', G(yol(rek), st('#ad7c69', 36)), G(yol(rek), st('#d6a995', 28)), G(yol(rek), st('#8f5f4f', 2, kesik=(3, 7), o=60)))
    A.ekle('levator', G(yol('M150 395 C200 360 260 330 330 322 C370 318 400 330 420 345'), st('#b65a50', 9, o=80)), G(yol('M150 395 C200 360 260 330 330 322 C370 318 400 330 420 345'), st('#e08f85', 3, o=70)))
    A.ekle('karin', G(yol('M470 20 C470 120 468 190 452 250 C447 270 440 285 432 298 L452 304 C462 290 472 270 478 248 C494 190 496 120 496 20 Z'), gf([(0, '#b5524a'), (.5, '#cf6b5f'), (1, '#a8463f')], (470, 0), (496, 0))),
           *[G(yol(f'M{470 + i * 6} 30 C{470 + i * 6} 120 {468 + i * 6} 190 {452 + i * 6} 250'), st('#9a3d36', 1, o=50)) for i in range(4)],
           G(yol('M496 20 C496 120 494 190 478 248 C472 270 462 290 452 304 L478 312 C490 296 500 276 506 252 C522 194 526 120 526 20 Z'), gf([(0, '#f6e3a6'), (1, '#efd283')], (496, 0), (526, 0))),
           *[G(el(504 + (i % 3) * 7, 50 + i * 24, 7, 6), fl('#e8c46e', o=60)) for i in range(10)],
           G(yol('M526 20 C526 120 522 194 506 252 C500 276 490 296 478 312 L490 316 C503 299 512 280 518 255 C534 196 538 120 538 20 Z'), gf([(0, '#e8b493'), (1, '#f3cdb1')], (526, 0), (538, 0))))


def simfiz(A, x, y, r):
    A.ekle('simfiz', G(el(0, 0, 44, 88), gf(KEMIK, (-10, -30), (20, 40), radyal=True), st('#a8946b', 2.5)), G(el(0, 0, 26, 64), fl('#e2c49a', o=55)),
           G(yol('M-4 -40 L-4 40'), st('#d8cbb0', 3, o=80)), p=S([x, y, 0]), r=S(r))


def erkek_anatomi(A, kateter_sonu=True):
    """Erkek pelvis yan kesiti (sahneler.tsx Erkek ile aynı geometri) + üreter, vas deferens, seminal vezikül, verumontanum,
    Cowper bezleri, korpus kavernozum septumu, derin dorsal ven, fossa navikularis, mesane rugaları."""
    pelvis_zemin(A)
    A.ekle('ureter', G(yol('M170 20 C190 60 210 100 238 132'), st('#d9a08f', 9)), G(yol('M170 20 C190 60 210 100 238 132'), st('#f2c9bb', 4)))
    A.ekle('vas', G(yol('M520 380 C560 330 540 250 500 200 C470 160 420 150 380 160 C330 172 280 200 262 222'), st('#d8b48f', 5)), G(yol('M520 380 C560 330 540 250 500 200 C470 160 420 150 380 160 C330 172 280 200 262 222'), st('#f3dcc0', 2)))
    A.ekle('seminal', G(yol('M240 235 C222 222 222 205 238 200 C252 196 262 212 266 228 Z'), gf([(0, '#f0d2b8'), (1, '#c9a07e')], (235, 205), (260, 232), radyal=True), st('#b58b6a', 1.5)),
           G(yol('M232 222 C238 214 246 214 252 222 M236 210 C242 204 250 206 254 214'), st('#b58b6a', 1, o=70)))
    simfiz(A, 412, 236, -20)
    A.ekle('diyafram', G(yol('M250 300 L360 300'), st('#b65a50', 10)), G(yol('M250 300 L360 300'), st('#d9786d', 3, kesik=(4, 4))))
    A.ekle('mesane', G(yol('M228 160 C222 100 270 70 320 72 C372 74 400 110 392 160 C386 200 352 228 306 236 C266 228 232 200 228 160 Z'), gf(MESANE, (280, 100), (330, 260), radyal=True), st('#a8554e', 7)),
           *[G(yol(f'M{236 + i * 18} {110 + (i % 2) * 8} C{240 + i * 18} 140 {232 + i * 18} 170 {240 + i * 18} 200'), st('#b5605a', 2, o=50)) for i in range(8)],
           G(yol('M242 160 C238 110 278 88 320 90 C362 92 382 120 376 160 C371 192 345 212 306 220 C272 213 246 192 242 160 Z'), gf(IDRAR, (300, 120), (330, 240), radyal=True), o=S(85)),
           G(yol('M282 214 L306 236 L330 214'), st('#b85f58', 2, o=70)), G(el(240, 134, 10, 6), fl('#8f3c3a')),
           G(yol('M270 100 C292 90 320 88 345 94'), st('#ffffff', 4, o=40)))
    A.ekle('prostat', G(yol('M262 262 C258 240 280 232 300 232 C322 232 342 242 338 264 C334 284 318 292 300 292 C280 292 266 282 262 262 Z'), gf([(0, '#e7b3a0'), (1, '#b97a66')], (285, 245), (320, 290), radyal=True), st('#94594a', 2)),
           *[G(yol(d), st('#9a604f', 1.2, o=60)) for d in ['M272 254 C278 248 288 246 294 250', 'M310 252 C318 252 326 256 328 262', 'M276 276 C286 282 296 282 302 276']])
    A.ekle('sfinkter', G(rc(300, 303, 36, 18, 7), fl('#c5534a'), st('#8d2f28', 1.5)), *[G(yol(f'M{288 + i * 8} 296 L{288 + i * 8} 310'), st('#8d2f28', 1, o=60)) for i in range(4)])
    A.ekle('cowper', G(el(326, 318, 9, 9), fl('#e9c5a8'), st('#b58b6a', 1)), G(el(336, 326, 8, 8), fl('#e9c5a8'), st('#b58b6a', 1)))
    A.ekle('penis', G(yol('M392 300 C420 278 460 270 500 270 L640 270 C650 270 650 334 640 334 L500 334 C450 336 412 336 380 352 Z'), gf(DERI, (500, 270), (500, 340)), st('#b9805a', 2)),
           G(yol('M420 288 C450 280 480 280 500 280 L636 280 L636 302 L500 302 C470 302 440 304 420 308 Z'), gf([(0, '#c9787a'), (.5, '#e0999a'), (1, '#b9686b')], (500, 280), (500, 302))),
           G(yol('M440 294 L630 291'), st('#a85558', 1, o=60)), G(yol('M430 276 L636 274'), st('#6d79b8', 2.2, o=80)),
           G(yol('M460 312 L636 304 L636 324 L460 330 Z'), gf([(0, '#e8a9a6'), (1, '#cf8784')], (500, 304), (500, 330))))
    A.ekle('bulbus', G(el(0, 0, 68, 36), gf([(0, '#e8a9a6'), (1, '#cf8784')], (-20, -10), (20, 18), radyal=True), st('#b56c69', 1), p=(392, 352), r=-18))
    A.ekle('skrotum', G(yol('M440 336 C420 360 420 430 470 450 C520 468 572 440 570 392 C568 356 540 336 510 334 Z'), gf(DERI, (480, 360), (520, 450)), st('#b9805a', 2)),
           G(yol('M470 352 C460 370 462 420 495 430'), st('#c28a66', 1.2, o=60)),
           G(el(505, 395, 72, 56), gf([(0, '#f3e0dc'), (1, '#cfa7a1')], (495, 385), (520, 420), radyal=True), st('#a77d76', 2)),
           G(yol('M535 372 C552 380 552 412 532 420'), st('#b9746d', 8, o=85)))
    A.ekle('uretra', G(yol(URETRA_E), st('#a8554e', 13, o=50)), G(yol(URETRA_E), st('#f0b8b2', 8)), G(el(301, 262, 7, 10), fl('#c97c77')),
           G(el(690, 302, 26, 12), fl('#f0b8b2')))
    A.ekle('glans', G(yol('M630 268 C680 262 712 282 712 302 C712 322 680 342 630 336 C622 320 622 284 630 268 Z'), gf([(0, '#f2b4ae'), (1, '#c97c77')], (660, 285), (700, 320), radyal=True), st('#a85f5a', 2)),
           G(yol('M626 266 C640 262 648 268 652 276 M626 338 C640 342 648 336 652 328'), st('#c28a66', 5)),
           G(yol('M650 278 C672 276 690 284 698 294'), st('#ffffff', 2.5, o=50)), G(el(710, 302, 8, 16), fl('#7d2f2a')))


def kateter_katmani(A, k1, k2, nm='kateter', d=KATETER_E, renk='#eef2f6', trim_ks=None, o=None):
    """Kateter yol boyunca ilerler (kırpma sonu 0→100). trim_ks verilirse onu kullanır."""
    e = trim_ks or K((0, 0), (k1, 0), (k2, 100))
    A.ekle(nm + '-golge', G(yol(d), st('#5b6676', 9, o=35), tm(e)), o=o)
    A.ekle(nm, G(yol(d), st(renk, 7), tm(e)), G(yol(d), st('#ffffff', 2, o=70), tm(e), p=(0, -2)), o=o)


def itilen_kateter(A, d, duraklar, catal_son, renk='#eef2f6', kenar='#5b6676', w=7, nm='kateter', o=None, catal=True):
    """Sabit boylu kateter: uç `duraklar` [(kare, (x, y)), …] boyunca ilerler, boy sabit kaldığı için dışta kalan kısım
    kısalır ve çatal (dış uç) meatusa yaklaşır. Kateter tam itildiğinde çatal `catal_son` noktasındadır.
    Kırpma başı/sonu ve uç/çatal konumları aynı doğrusal sık örneklemle üretilir (birbirinden kaymaz)."""
    from lottie_dsl import ornekle
    P = ornekle(d, 400)
    kes = lambda q: min(range(len(P)), key=lambda i: (P[i][0] - q[0]) ** 2 + (P[i][1] - q[1]) ** 2) / 400  # noqa: E731
    fr = [(k, kes(q)) for k, q in duraklar]
    L = fr[-1][1] - kes(catal_son)
    ornek = []
    for (k1, f1), (k2, f2) in zip(fr, fr[1:]):
        for j in range(12):
            ornek.append((k1 + (k2 - k1) * j / 12, f1 + (f2 - f1) * j / 12))
    ornek.append(fr[-1])
    nokta = lambda f: P[max(0, min(400, round(f * 400)))]  # noqa: E731
    e = KD(*[(k, f * 100) for k, f in ornek])
    s = KD(*[(k, max(0, f - L) * 100) for k, f in ornek])
    A.ekle(nm + '-golge', G(yol(d), st(kenar, w + 2, o=40), tm(e, s)), o=o)
    A.ekle(nm, G(yol(d), st(renk, w), tm(e, s)), G(yol(d), st('#ffffff', 2, o=70), tm(e, s), p=(0, -w / 3)), o=o)
    # uç: yuvarlak kör uç + idrar deliği
    A.ekle(nm + '-uc', G(el(0, 0, w + 3, w + 3), fl(renk), st(kenar, 1.2)), G(el(0, 0, 3.4, 3.4), fl('#2e3540')),
           p=KD(*[(k, [*nokta(f), 0]) for k, f in ornek]), o=o)
    if catal:
        A.ekle(nm + '-catal', G(rc(10, 0, 30, 20, 5), fl('#e3e8ee'), st('#6b7a90', 1.5)), G(rc(14, -14, 8, 12, 2), fl('#ef7d22')),
               G(yol('M24 6 L44 14'), st('#e3e8ee', 7)),
               p=KD(*[(k, [*nokta(max(0, f - L)), 0]) for k, f in ornek]), o=o)


# ———————————————————————— 1. Erkekte kateter ilerleyişi

def erkek_ilerleyis(z):
    A = _anim(z, 'erkek-ilerleyis', 'Erkekte kateterin üretrada ilerleyişi', [
        B('Anatomi', 'Erkek alt üriner sistemini yandan görüyoruz: mesane, prostat, eksternal sfinkter, bulbar ve penil üretra.', 7),
        B('Tutuş', 'Kateteri avucunda toplar, penisi dik ve gergin tutarsın; böylece üretranın kıvrımı düzleşir.', 6),
        B('Penil üretra', 'Kateter meatustan girer ve düz penil üretrada kolayca ilerler.', 5),
        B('Bulbar kıvrım', 'Bulbar üretranın kıvrımında hafif direnç olabilir; zorlamadan, sabit ve yavaş bir basınçla devam edersin.', 7),
        B('Sfinkter', 'Eksternal sfinkterin bulunduğu membranöz üretra en dar bölümdür.', 5),
        B('Prostatik üretra', 'Prostatik üretrayı geçen kateter mesane boynundan mesaneye ulaşır.', 5),
        B('İdrar geldi', 'İdrar geldi; ama erkekte kateteri yine de çatal kısmına kadar, sonuna kadar ilerletirsin.', 7),
        B('Balon mesanede', 'Böylece balon kesinlikle mesanede olur ve güvenle şişirilebilir.', 5),
    ], z)
    erkek_anatomi(A)
    T = A.T
    # düzleştirme kılavuzu
    A.ekle('kilavuz', G(yol('M300 305 C300 345 330 362 372 352 L700 302'), st('#2f6fd6', 3, kesik=(10, 8))), o=A.gor(T(1), T(2, .5)))
    # uç: meatus → penil → bulbar kıvrım → sfinkter → prostatik üretra → mesane boynu → mesane; çatal sonunda meatusun dışında
    itilen_kateter(A, 'M1200 302 L700 302 L470 320 L372 352 C330 362 300 345 300 305 L300 138',
                   [(T(2), (712, 302)), (T(2, 1), (470, 320)), (T(3, 1), (340, 352)), (T(4, 1), (300, 300)), (T(5, .6), (300, 236)),
                    (T(5, 1), (300, 200)), (T(6, .8), (300, 138))], catal_son=(728, 302), o=A.gor(T(2) - 2))
    # bölge vurguları
    A.ekle('vurgu-bulbar', G(el(372, 352, 60, 60), st('#e1a92e', 4)), o=K((0, 0), (T(3), 0), (T(3, .15), 100), (T(3, .85), 100), (T(3, 1), 0)))
    A.ekle('vurgu-sfinkter', G(rc(300, 303, 52, 30, 10), st('#d23b3b', 4)), o=K((0, 0), (T(4), 0), (T(4, .15), 100), (T(4, .85), 100), (T(4, 1), 0)))
    # idrar geri akışı (kateter boyunca dışa)
    A.ekle('idrar-akis', G(yol('M300 150 L300 305 C300 345 330 362 372 352 L470 320 L700 302 L790 302'),
                           st('#e1b300', 3, kesik=(10, 14), kesik_kayma=KD((T(6), 0), (A.op, -(A.op - T(6)) * 3)))), o=A.gor(T(6, .1)))
    # balon mesanede
    A.ekle('balon', G(el(300, 166, 44, 34), fl('#ffffff', .75), st('#2e9e5b', 3)), a=(300, 166), p=S([300, 166, 0]), s=K((0, [10, 10, 100]), (T(7), [10, 10, 100]), (T(7, .6), [100, 100, 100])),
           o=A.gor(T(7)))
    A.ekle('balon-halka', G(el(300, 166, 80, 70), st('#2e9e5b', 3, kesik=(6, 6))), o=A.gor(T(7, .5)))
    for i, (x, y, m) in enumerate([(230, 60, 'Mesane'), (210, 262, 'Prostat'), (215, 315, 'Eksternal sfinkter'), (440, 380, 'Bulbar üretra'), (560, 250, 'Penil üretra'), (720, 340, 'Meatus')]):
        A.etiket(0, 0, x, y, m)
    A.etiket(1, 1, 560, 230, 'Penis dik ve gergin', 'bilgi')
    A.etiket(3, 3, 330, 410, 'Kıvrım: zorlama yok', 'uyari')
    A.etiket(4, 4, 215, 330, 'En dar bölüm', 'uyari')
    A.etiket(6, 6, 600, 360, 'İdrar geldi → yine de sonuna kadar', 'bilgi')
    A.etiket(7, 7, 380, 150, 'Balon mesanede ✓', 'dogru')
    # kamera: bölüm başında ilgili bölgeye yumuşak yakınlaşma
    A.kamera(1, 560, 300, 130)
    A.kamera(2, 600, 300, 190)
    A.kamera(3, 380, 335, 230)
    A.kamera(4, 300, 300, 250)
    A.kamera(5, 300, 250, 210)
    A.kamera(6, 450, 250, 105)
    A.kamera(7, 300, 160, 210)
    return A


# ———————————————————————— 2. Kadında kateter ilerleyişi

KADIN_URETRA = 'M330 250 C350 290 372 330 392 372'


def kadin_ilerleyis(z):
    A = _anim(z, 'kadin-ilerleyis', 'Kadında kateterin mesaneye ilerleyişi', [
        B('Anatomi', 'Kadın üretrası kısadır; mesane boynundan öne ve aşağıya, vestibüle uzanır. Arkasında vajina vardır.', 7),
        B('Meatus', 'Labiaları ayırınca meatusu görürsün: klitorisin altında, vajinanın üstündeki küçük açıklık.', 6),
        B('Giriş', 'Ucuna jel sürülmüş kateteri meatustan nazikçe ilerletirsin.', 5),
        B('İdrar', 'Birkaç santimetre sonra uçtaki delikler mesaneye girer ve idrar gelir.', 5),
        B('Birkaç santim daha', 'Balonun da mesaneye girmesi için kateteri birkaç santimetre daha ilerletirsin.', 5),
        B('Balon', 'Balonu şişirip hafifçe geri çektiğinde balon mesane boynuna oturur.', 6),
    ], z)
    T = A.T
    pelvis_zemin(A, kadin=True)
    # uterus (endometrium + miyometrium), serviks, tuba + over, vezikouterin ve rektouterin çukur
    A.ekle('uterus', G(yol('M200 120 C190 70 260 50 300 80 C330 100 320 150 290 170 L250 180 C220 170 205 150 200 120 Z'), gf([(0, '#f1b9b0'), (1, '#c97f76')], (240, 90), (280, 170), radyal=True), st('#a8554e', 2)),
           G(yol('M228 120 C226 98 262 88 282 104 C296 116 290 140 274 150 L254 154 C238 148 230 136 228 120 Z'), fl('#e88f88', o=80)),
           G(yol('M250 178 C252 190 258 196 266 198'), st('#c97f76', 14)),
           G(yol('M300 82 C330 60 360 60 380 70'), st('#e0a99c', 4)), G(el(390, 76, 26, 18), gf([(0, '#f6e0cf'), (1, '#d9b49a')], (385, 70), (398, 84), radyal=True), st('#b58b6a', 1)))
    A.ekle('cukurlar', G(yol('M300 170 C318 180 330 190 340 200'), st('#b48a7a', 1.5, kesik=(4, 4))), G(yol('M200 180 C196 200 198 220 210 236'), st('#b48a7a', 1.5, kesik=(4, 4))))
    A.ekle('vajina', G(yol('M262 190 C280 260 300 330 330 410'), st('#c97f7a', 22)), G(yol('M262 190 C280 260 300 330 330 410'), st('#8f3c3a', 6)),
           *[G(yol(f'M{262 + i * 7} {200 + i * 26} L{276 + i * 7} {196 + i * 26}'), st('#a64c48', 1.5, o=70)) for i in range(8)])
    simfiz(A, 420, 290, -18)
    A.ekle('mesane', G(yol('M250 230 C240 180 290 150 340 156 C390 162 410 200 400 235 C392 262 360 270 330 266 C295 262 255 258 250 230 Z'), gf(MESANE, (300, 170), (340, 270), radyal=True), st('#a8554e', 6)),
           G(yol('M262 228 C256 190 296 170 338 174 C380 178 392 205 384 230 C378 248 356 253 330 250 C300 248 266 246 262 228 Z'), gf(IDRAR, (310, 190), (340, 250), radyal=True), o=88))
    A.ekle('uretra', G(yol(KADIN_URETRA), st('#a8554e', 11, o=50)), G(yol(KADIN_URETRA), st('#f0b8b2', 7)))
    A.ekle('vulva', G(yol('M372 372 C384 380 400 392 412 410 L392 430 C380 410 370 396 360 386 Z'), gf(DERI, (380, 380), (400, 430))),
           G(el(392, 374, 10, 10), fl('#7d2f2a')))
    A.ekle('meatus-isik', G(el(392, 374, 34, 34), st('#2e9e5b', 4)), o=K((0, 0), (T(1), 0), (T(1, .2), 100), (T(1, .9), 100), (T(2), 0)))
    itilen_kateter(A, 'M700 610 L520 470 C470 440 420 400 392 372 C372 330 350 290 330 250 L318 205',
                   [(T(2), (394, 374)), (T(2, 1), (372, 330)), (T(3, .6), (338, 262)), (T(4, .8), (320, 212))], catal_son=(560, 500),
                   renk='#e3b544', kenar='#8a6a1e', o=A.gor(T(2) - 2), catal=False)
    A.ekle('jel', G(el(392, 374, 22, 14), fl('#cfe9ff', .8)), o=K((0, 0), (T(2), 0), (T(2, .2), 100), (T(3), 0)))
    A.ekle('idrar', G(yol('M320 210 C350 290 380 360 400 390 L470 450 L530 480'), st('#e1b300', 3, kesik=(8, 10), kesik_kayma=KD((T(3, .5), 0), (A.op, -(A.op - T(3, .5)) * 3)))), o=A.gor(T(3, .5)))
    A.ekle('balon', G(el(318, 212, 42, 34), fl('#ffffff', .75), st('#2e9e5b', 3)),
           p=K((0, [0, 0, 0]), (T(5, .55), [0, 0, 0]), (T(5, .85), [4, 18, 0])), s=K((0, [10, 10, 100]), (T(5), [10, 10, 100]), (T(5, .5), [100, 100, 100])), o=A.gor(T(5)))
    A.etiket(0, 0, 330, 140, 'Mesane'); A.etiket(0, 0, 210, 300, 'Vajina'); A.etiket(0, 0, 440, 330, 'Simfiz'); A.etiket(0, 0, 410, 300, 'Kısa üretra', 'bilgi')
    A.etiket(1, 1, 470, 380, 'Meatus', 'dogru')
    A.etiket(3, 3, 470, 420, 'İdrar geldi', 'bilgi')
    A.etiket(4, 4, 250, 195, 'Birkaç santim daha', 'uyari')
    A.etiket(5, 5, 400, 190, 'Balon boyunda ✓', 'dogru')
    # kamera: bölüm başında ilgili bölgeye yumuşak yakınlaşma
    A.kamera(0, 320, 260, 120)
    A.kamera(1, 392, 374, 260)
    A.kamera(2, 400, 340, 170)
    A.kamera(3, 340, 280, 160)
    A.kamera(4, 320, 240, 200)
    A.kamera(5, 330, 230, 190)
    return A


# ———————————————————————— 3. Balonun şişirilmesi

def balon(z):
    A = _anim(z, 'balon-sisme', 'Balonun şişirilmesi ve mesane boynuna oturtulması', [
        B('Kateter mesanede', 'Kateterin ucu mesanede; uçtaki deliklerden idrar geliyor.', 5),
        B('Enjektör', 'İnce, valfli balon kanalına steril izotonikle dolu enjektörü takarsın.', 6),
        B('Sıvı', 'Pistonu yavaşça ittiğinde sıvı balon kanalında ilerler.', 5),
        B('Şişme', 'Balon şişer; hasta ağrı tarif ederse durur, balonu indirip kateterin yerini yeniden değerlendirirsin.', 8),
        B('Geri çekme', 'Kateteri hafifçe geri çektiğinde direnç hissedersin.', 5),
        B('Oturdu', 'Balon artık mesane boynuna oturmuştur; kateter basit çekiştirmeyle çıkmaz.', 6),
    ], z)
    T = A.T
    geri = K((0, [0, 0, 0]), (T(4), [0, 0, 0]), (T(4, .7), [0, 34, 0]))
    A.ekle('mesane', G(rc(400, 250, 800, 500), gf(MESANE, (400, 120), (400, 600), radyal=True)))
    for i in range(9):
        A.ekle(f'ruga{i}', G(yol(f'M{40 + i * 85} 40 C{60 + i * 85} 120 {20 + i * 85} 200 {50 + i * 85} 300'), st('#c06a63', 6, o=35)))
    A.ekle('lumen', G(yol('M60 50 L740 50 L740 300 C650 300 540 305 455 335 L345 335 C260 305 150 300 60 300 Z'), gf(IDRAR, (400, 120), (400, 330), radyal=True), o=S(78)))
    A.ekle('trigon', G(yol('M220 220 L580 220 L400 330 Z'), fl('#f3b3ac', .85), st('#c06a63', 2)), G(el(222, 222, 28, 14), fl('#8f3c3a')), G(el(578, 222, 28, 14), fl('#8f3c3a')))
    A.ekle('prostat', G(yol('M200 360 C240 345 300 345 345 360 L345 500 L180 500 C170 450 175 390 200 360 Z'), fl('#c98f7c')),
           G(yol('M600 360 C560 345 500 345 455 360 L455 500 L620 500 C630 450 625 390 600 360 Z'), fl('#c98f7c')),
           G(yol('M345 356 L345 500 L455 500 L455 356 C430 366 370 366 345 356 Z'), fl('#e8a7a2')))
    A.ekle('idrar-giris', *[G(yol(f'M{x} {y} C{(x + 400) / 2} {y + 10} {400 + (-16 if x < 400 else 16)} 170 400 172'),
                             st('#d9a400', 3, kesik=(8, 10), kesik_kayma=KD((0, 0), (A.op, -A.op * 2)))) for x, y in [(300, 110), (250, 160), (500, 120), (540, 170)]],
           o=K((0, 100), (T(3), 100), (T(3, .3), 0)))
    A.ekle('kateter', G(rc(400, 325, 44, 350, 6), gf([(0, '#9aa6b4'), (.35, '#ffffff'), (.65, '#e6ebf1'), (1, '#9aa6b4')], (378, 0), (422, 0)), st('#8a96a6', 1.5)),
           G(el(400, 150, 44, 56), fl('#eef2f6'), st('#8a96a6', 1.5)),
           G(el(400, 168, 26, 16), fl('#3e4a58')), G(el(400, 196, 22, 14), fl('#3e4a58', .8)),
           G(rc(392, 380, 10, 260), fl('#c9d3de', .7)), p=geri)
    A.ekle('kanal-sivi', G(yol('M413 500 L413 280'), st('#5b8fc9', 5), tm(K((0, 0), (T(2), 0), (T(2, 1), 100)))), p=geri)
    A.ekle('balon', G(el(0, 0, 160, 96), fl('#e6f1fc', .88), st('#5b8fc9', 3)), G(el(0, 10, 130, 56), fl('#b9d8f7', .7)), G(el(-30, -18, 36, 14), fl('#ffffff', .85)),
           p=K((0, [400, 280, 0]), (T(4), [400, 280, 0]), (T(4, .7), [400, 314, 0])),
           s=K((0, [30, 42, 100]), (T(3), [30, 42, 100]), (T(3, .8), [100, 100, 100])))
    A.ekle('boyun', G(yol('M330 335 C360 352 380 358 400 358 C420 358 440 352 470 335'), st('#a8554e', 9)))
    A.ekle('oturdu', G(el(400, 330, 210, 120), st('#2e9e5b', 4, kesik=(10, 8))), o=A.gor(T(5)))
    A.ekle('cekme-ok', G(yol('M560 360 L560 450'), st('#2f6fd6', 6)), G(yol('M546 432 L560 456 L574 432'), st('#2f6fd6', 6)), o=K((0, 0), (T(4), 0), (T(4, .15), 100), (T(5, .2), 100), (T(5, .4), 0)))
    # enjektör (sağdan gelir)
    A.ekle('hortum', G(yol('M640 440 C560 440 470 470 418 470'), st('#cfd8e2', 10)), o=A.gor(T(1)))
    enj_p = K((0, [260, 0, 0]), (T(1), [260, 0, 0]), (T(1, .6), [0, 0, 0]))
    A.ekle('enjektor', G(rc(720, 440, 150, 60, 6), fl('#eef3f8', .92), st('#6b7a90', 2)),
           *[G(yol(f'M{660 + i * 14} 410 L{660 + i * 14} {418 if i % 2 else 424}'), st('#3e4a58', 1.5)) for i in range(9)],
           G(rc(640, 440, 20, 14, 2), fl('#9aa6b4')), p=enj_p)
    A.ekle('enj-sivi', G(rc(0, 0, 110, 46, 2), fl('#9fc4ef', .9)),
           p=K((0, [990, 440, 0]), (T(1), [990, 440, 0]), (T(1, .6), [730, 440, 0]), (T(2), [730, 440, 0]), (T(3, .8), [780, 440, 0])),
           s=K((0, [100, 100, 100]), (T(2), [100, 100, 100]), (T(3, .8), [10, 100, 100])))
    A.ekle('piston', G(rc(0, 0, 14, 56, 3), fl('#2b2f36')), G(rc(60, 0, 110, 12, 2), fl('#c9d3de'), st('#6b7a90', 1.5)), G(rc(118, 0, 10, 70, 3), fl('#6b7a90')),
           p=K((0, [928, 440, 0]), (T(1), [928, 440, 0]), (T(1, .6), [668, 440, 0]), (T(2), [668, 440, 0]), (T(3, .8), [720, 440, 0])))
    A.sayac(2, 0, 3, .8, 0, 10, 'mL', 640, 380)
    A.etiket(0, 0, 400, 90, 'Uçtaki delikler: idrar girer', 'bilgi')
    A.etiket(1, 1, 700, 380, 'Balon kanalı + enjektör', 'bilgi')
    A.etiket(3, 3, 260, 400, 'Ağrı olursa dur', 'uyari')
    A.etiket(4, 4, 640, 470, 'Hafifçe çek', 'bilgi')
    A.etiket(5, 5, 400, 430, 'Balon mesane boynunda ✓', 'dogru')
    # kamera: bölüm başında ilgili bölgeye yumuşak yakınlaşma
    A.kamera(0, 400, 180, 150)
    A.kamera(1, 640, 420, 140)
    A.kamera(2, 520, 380, 120)
    A.kamera(3, 400, 290, 150)
    A.kamera(4, 400, 330, 130)
    A.kamera(5, 400, 330, 110)
    return A


# ———————————————————————— 4. İdrar akışı ve torba

def idrar_akisi(z):
    A = _anim(z, 'idrar-akisi', 'İdrarın torbaya akışı ve ölçümü', [
        B('Delikler', 'İdrar kateterin ucundaki deliklerden girer.', 4),
        B('Drenaj kanalı', 'Kalın drenaj kanalından ve hortumdan torbaya akar.', 5),
        B('Ölçüm', 'Torbadaki çizgilerden saatlik ve yirmi dört saatlik idrar miktarı okunur.', 6),
        B('Sıvı dengesi', 'Bu miktara göre hastaya verilecek sıvıyı ayarlarsın; az verirsen böbrek, fazla verirsen akciğer ve kalp bozulur.', 8),
        B('Boşaltma', 'Torba dolunca altındaki musluktan boşaltılır.', 5),
    ], z)
    T = A.T
    zemin(A)
    A.ekle('mesane', G(yol('M40 150 C40 80 120 40 200 44 C280 48 320 100 310 170 C300 240 250 270 190 272 C120 274 40 240 40 150 Z'), gf(MESANE, (150, 100), (200, 260), radyal=True), st('#a8554e', 6)),
           G(yol('M56 150 C56 94 126 60 200 62 C270 66 298 108 290 168 C282 226 240 252 190 254 C128 256 56 226 56 150 Z'), gf(IDRAR, (160, 110), (200, 240), radyal=True)))
    hat = 'M200 160 L200 330 C200 380 260 390 340 390 L560 390 C600 390 620 360 620 330 L620 250'
    A.ekle('kateter', G(yol(hat), st('#8a96a6', 14)), G(yol(hat), st('#eef2f6', 11)), G(yol(hat), st('#ffffff', 3, o=70), p=(0, -3)))
    A.ekle('uc', G(el(200, 150, 18, 26), fl('#eef2f6'), st('#8a96a6', 1.5)), G(el(200, 162, 8, 6), fl('#3e4a58')))
    A.ekle('akis', G(yol(hat), st('#e1b300', 5, kesik=(10, 14), kesik_kayma=KD((T(1), 0), (A.op, -(A.op - T(1)) * 3)))), o=A.gor(T(1)))
    A.ekle('giris', *[G(yol(f'M{x} {y} L200 160'), st('#d9a400', 3, kesik=(6, 8), kesik_kayma=KD((0, 0), (A.op, -A.op * 2)))) for x, y in [(120, 110), (270, 120), (150, 210), (250, 210)]])
    # torba
    A.ekle('torba', G(rc(640, 360, 220, 250, 18), fl('#f4f7fa', .9), st('#9aa6b4', 3)), G(yol('M560 236 C560 220 720 220 720 236'), st('#9aa6b4', 4)),
           G(rc(620, 262, 26, 40, 6), fl('#eef3f8'), st('#9aa6b4', 1.5)))
    A.ekle('torba-idrar', G(rc(640, 0, 204, 230, 14), gf([(0, '#f8dd6c'), (1, '#e7b82e')], (640, -100), (640, 100))),
           p=K((0, [0, 704, 0]), (T(1, .5), [0, 704, 0]), (T(4, .2), [0, 560, 0]), (T(4, .4), [0, 560, 0]), (T(4, 1), [0, 640, 0])))
    A.ekle('cizgi', *[G(yol(f'M712 {290 + i * 36} L748 {290 + i * 36}'), st('#5b6676', 2)) for i in range(6)])
    A.ekle('damla', G(el(620, 270, 8, 12), fl('#e1b300')), p=KD(*[(T(1) + k * 12, [0, (k % 2) * 20, 0]) for k in range(int((A.op - T(1)) / 12))]), o=A.gor(T(1)))
    A.ekle('musluk', G(rc(640, 492, 30, 16, 4), fl('#6b7a90')), G(rc(662, 492, 20, 10, 3), fl('#c0392b')))
    A.ekle('bosalt', G(yol('M640 500 L640 540'), st('#e1b300', 6, kesik=(8, 6), kesik_kayma=KD((T(4), 0), (A.op, -60)))), o=K((0, 0), (T(4, .4), 0), (T(4, .5), 100)))
    A.sayac(1, .5, 3, 1, 0, 600, 'mL', 470, 240)
    A.etiket(0, 0, 200, 300, 'Uçtaki delikler', 'bilgi'); A.etiket(1, 1, 420, 420, 'Drenaj kanalı → torba', 'bilgi')
    A.etiket(2, 2, 560, 200, 'Saatlik / 24 saatlik miktar', 'bilgi')
    A.etiket(3, 3, 300, 470, 'Az sıvı → böbrek · fazla sıvı → akciğer, kalp', 'uyari')
    A.etiket(4, 4, 520, 470, 'Musluktan boşalt', 'bilgi')
    # kamera: bölüm başında ilgili bölgeye yumuşak yakınlaşma
    A.kamera(0, 200, 160, 190)
    A.kamera(1, 400, 380, 120)
    A.kamera(2, 640, 360, 170)
    A.kamera(3, 400, 250, 100)
    A.kamera(4, 640, 470, 180)
    return A


# ———————————————————————— 5. Üretrada şişirilen balon

def yanlis_balon(z):
    A = _anim(z, 'yanlis-balon', 'Üretrada şişirilen balon: ne olur?', [
        B('Kıvrılma', 'Kateter bulbar üretrada bir yere takıldı ve kıvrıldı; idrar gelmiyor.', 6),
        B('Soru', 'Bu durumda balon şişirilirse ne olacağını görelim.', 4),
        B('Gerilme', 'Yaklaşık bir santimetre çapındaki üretra balonla zorla genişler.', 6),
        B('Yırtık', 'Mukoza yırtılır ve kanama başlar; balon sfinkter düzeyindeyse hasta kalıcı inkontinans olur.', 8),
        B('Darlık', 'Uzun dönemde bu bölgede üretra darlığı gelişir. Kural basit: idrar yoksa şişirme yok.', 7),
    ], z)
    T = A.T
    zemin(A)
    gen = K((0, [100, 100, 100]), (T(2), [100, 100, 100]), (T(2, 1), [100, 175, 100]), (T(4, .3), [100, 175, 100]), (T(4, .8), [100, 70, 100]))
    A.ekle('spongiozum', G(rc(400, 250, 800, 320, 40), gf([(0, '#e8a9a6'), (1, '#cf8784')], (400, 90), (400, 410))))
    A.ekle('sfinkter', G(rc(400, 250, 120, 320, 18), fl('#c5534a', .85)), *[G(yol(f'M{348 + i * 11} 100 L{348 + i * 11} 400'), st('#8d2f28', 1.5, o=60)) for i in range(10)])
    A.ekle('mukoza', G(rc(0, 0, 800, 100), gf([(0, '#f2a9a6'), (1, '#c86e6c')], (0, -50), (0, 50))), G(rc(0, 0, 800, 50), fl('#f6cfc9')), p=S([400, 250, 0]), s=gen)
    A.ekle('kivrim', G(yol('M0 250 L520 250 C600 250 640 230 640 200 C640 160 560 160 560 210 C560 260 620 280 680 260'), st('#8a96a6', 24), tm(K((0, 0), (T(0, .1), 0), (T(0, .9), 100)))),
           G(yol('M0 250 L520 250 C600 250 640 230 640 200 C640 160 560 160 560 210 C560 260 620 280 680 260'), st('#eef2f6', 20), tm(K((0, 0), (T(0, .1), 0), (T(0, .9), 100)))))
    A.ekle('soru', G(el(400, 120, 70, 70), fl('#e1a92e')), o=K((0, 0), (T(1), 0), (T(1, .2), 100), (T(1, .9), 100), (T(2), 0)))
    A.ekle('balon', G(el(0, 0, 220, 190), fl('#d23b3b', .55), st('#8d1f1f', 4)), G(el(-30, -40, 60, 28), fl('#ffffff', .5)),
           p=S([400, 250, 0]), s=K((0, [8, 8, 100]), (T(2), [8, 8, 100]), (T(2, 1), [100, 100, 100]), (T(4, .3), [100, 100, 100]), (T(4, .6), [0, 0, 100])))
    A.ekle('yirtik', *[G(yol(d), st('#5c0f0f', 4), tm(K((0, 0), (T(3), 0), (T(3, .4), 100)))) for d in ['M300 160 L320 190 L306 204 L324 230', 'M500 340 L482 314 L496 300 L476 270', 'M410 150 L404 176 L414 188']])
    A.ekle('kan', *[G(yol(f'M{x} {y} C{x - 8} {y + 12} {x - 6} {y + 20} {x} {y + 20} C{x + 6} {y + 20} {x + 8} {y + 12} {x} {y} Z'), fl('#b3201f')) for x, y in [(280, 300), (520, 210), (470, 320), (320, 190)]],
           o=A.gor(T(3, .3)), s=K((0, [100, 100, 100]), (T(3, .3), [100, 100, 100]), (T(4), [100, 115, 100])))
    A.ekle('kan-akis', G(yol('M200 250 L0 250'), st('#b3201f', 6, kesik=(10, 10), kesik_kayma=KD((T(3, .4), 0), (A.op, -(A.op - T(3, .4)) * 2)))), o=A.gor(T(3, .4)))
    A.ekle('carpi', G(yol('M640 90 L720 170 M720 90 L640 170'), st('#d23b3b', 12)), o=A.gor(T(4, .6)))
    A.etiket(0, 0, 610, 120, 'Takıldı, kıvrıldı', 'uyari'); A.etiket(1, 1, 400, 60, 'Şişirirsek?', 'bilgi')
    A.etiket(2, 2, 400, 450, 'Üretra zorla genişliyor', 'uyari'); A.etiket(3, 3, 400, 450, 'Yırtık + kanama · sfinkter → inkontinans', 'uyari')
    A.etiket(4, 4, 400, 450, 'Darlık · idrar yoksa şişirme yok', 'uyari')
    # kamera: bölüm başında ilgili bölgeye yumuşak yakınlaşma
    A.kamera(0, 560, 230, 140)
    A.kamera(1, 400, 250, 100)
    A.kamera(2, 400, 250, 140)
    A.kamera(3, 400, 250, 170)
    A.kamera(4, 400, 250, 110)
    return A


# ———————————————————————— 6. Yıkama testi (idrar gelmedi)

def yikama(z):
    A = _anim(z, 'yikama-testi', 'İdrar gelmedi: izotonik yıkama testi', [
        B('Dur', 'Kateteri sonuna kadar ittin ama idrar gelmiyor; balonu şişirmeden durursun.', 6),
        B('Enjektör', 'Geniş uçlu kateter enjektörünü kateterin drenaj ucuna takarsın.', 5),
        B('Ver', 'Otuz kırk mililitre steril izotonik verirsin.', 5),
        B('Birinci olasılık', 'Sıvı rahatça gidip rahatça geri çekiliyorsa kateter mesanededir; balonu şişirebilirsin.', 8),
        B('İkinci olasılık', 'Sıvı zor gidiyor ve hiç geri gelmiyorsa kateter üretrada kıvrılmıştır.', 7),
        B('Geri çek', 'Bu durumda balonu şişirmeden kateteri geri çekersin.', 5),
    ], z)
    T = A.T
    erkek_anatomi(A)
    tam = K((0, 100))
    A.ekle('kateter-mesane', G(yol(KATETER_Y), st('#5b6676', 9, o=35)), G(yol(KATETER_Y), st('#eef2f6', 7)), G(el(300, 138, 10, 10), fl('#eef2f6'), st('#5b6676', 1.2)), G(el(300, 138, 3.4, 3.4), fl('#2e3540')), o=K((0, 100), (T(4), 100), (T(4, .1), 0)))
    kiv = 'M730 302 L700 302 L470 320 L405 340 C350 362 332 318 375 316 C418 314 408 362 352 358'
    A.ekle('kateter-kivrim', G(yol(kiv), st('#5b6676', 9, o=35)), G(yol(kiv), st('#eef2f6', 7)), o=K((0, 0), (T(4), 0), (T(4, .1), 100), (T(5, .3), 100), (T(5, .9), 0)))
    A.ekle('kivrim-geri', G(yol('M730 302 L700 302 L560 312'), st('#eef2f6', 7)), o=A.gor(T(5, .8)))
    A.ekle('catal', G(rc(742, 302, 26, 20, 5), fl('#e3e8ee'), st('#6b7a90', 1.5)), G(rc(746, 288, 8, 12, 2), fl('#ef7d22')))
    A.ekle('enjektor', G(rc(0, 0, 96, 40, 5), fl('#eef3f8', .92), st('#6b7a90', 2)), G(rc(-58, 0, 22, 12, 2), fl('#9aa6b4')),
           G(rc(6, 0, 70, 30), fl('#9fc4ef', .9)),
           p=K((0, [960, 302, 0]), (T(1), [960, 302, 0]), (T(1, .7), [812, 302, 0])))
    giden = 'M760 302 L700 302 L470 320 L372 352 C330 362 300 345 300 305 L300 150'
    A.ekle('sivi-git', G(yol(giden), st('#2f6fd6', 4, kesik=(10, 10), kesik_kayma=KD((T(2), 0), (T(3, .5), -260)))), o=K((0, 0), (T(2), 0), (T(2, .1), 100), (T(3, .5), 100), (T(3, .6), 0)))
    A.ekle('sivi-don', G(yol(giden), st('#2e9e5b', 4, kesik=(10, 10), kesik_kayma=KD((T(3, .5), 0), (T(4), 260)))), o=K((0, 0), (T(3, .5), 0), (T(3, .6), 100), (T(4), 100), (T(4, .05), 0)))
    A.ekle('mesane-sivi', G(el(300, 160, 70, 50), fl('#9fc4ef', .6)), o=K((0, 0), (T(2, .8), 0), (T(3, .2), 100), (T(3, .8), 100), (T(4), 0)))
    A.ekle('tikali', G(el(370, 335, 60, 50), fl('#d23b3b', .3), st('#d23b3b', 3)), o=K((0, 0), (T(4, .3), 0), (T(4, .4), 100), (T(5, .6), 100), (T(5, .8), 0)))
    A.ekle('balon-ok', G(el(300, 152, 48, 40), fl('#ffffff', .75), st('#2e9e5b', 3)), o=K((0, 0), (T(3, .7), 0), (T(3, .8), 100), (T(4), 100), (T(4, .05), 0)))
    A.sayac(2, 0, 2, 1, 0, 40, 'mL', 640, 220)
    A.etiket(0, 0, 600, 380, 'İdrar yok → şişirme!', 'uyari'); A.etiket(1, 1, 700, 250, 'Geniş uçlu enjektör', 'bilgi')
    A.etiket(3, 3, 380, 120, 'Rahat gidip geliyor → mesanede ✓', 'dogru')
    A.etiket(4, 4, 320, 420, 'Geri gelmiyor → üretrada kıvrım', 'uyari'); A.etiket(5, 5, 600, 380, 'Şişirmeden geri çek', 'uyari')
    # kamera: bölüm başında ilgili bölgeye yumuşak yakınlaşma
    A.kamera(0, 300, 200, 140)
    A.kamera(1, 720, 302, 190)
    A.kamera(2, 500, 300, 120)
    A.kamera(3, 300, 180, 190)
    A.kamera(4, 380, 340, 220)
    A.kamera(5, 560, 310, 130)
    return A


# ———————————————————————— 7. Kadında temizlik

VULVA_DIS = 'M400 62 C300 66 252 170 262 300 C270 390 320 452 400 456 C480 452 530 390 538 300 C548 170 500 66 400 62 Z'
SPIRAL = 'M400 208 C422 208 428 234 400 242 C360 251 350 188 400 180 C464 171 478 288 400 306 C318 320 300 152 400 130 C500 112 528 338 400 366'


def kadin_temizlik(z):
    A = _anim(z, 'kadin-temizlik', 'Kadında alan temizliği', [
        B('Hazırlık', 'Ellerini yıkar, steril olmayan eldivenle antiseptikli gazlı bezi alırsın.', 6),
        B('Birinci silme', 'Labium minuslardan majuslara, merkezden dışa doğru dairesel hareketle silersin.', 6),
        B('İkinci silme', 'Dışa ulaşınca yeni bir bezle yeniden merkezden başlarsın.', 5),
        B('Üçüncü silme', 'Bu işlemi üç kez tekrarlarsın; dıştan içe silmek kirli alanı meatusa taşır.', 6),
        B('Steril örtü', 'Sonra steril eldiven giyer, delikli örtüyü meatus açıkta kalacak şekilde yerleştirirsin.', 6),
    ], z)
    T = A.T
    zemin(A)
    A.ekle('uyluk', G(yol('M0 60 C120 70 220 150 260 300 C280 380 270 460 250 500 L0 500 Z'), gf(DERI, (100, 200), (250, 450))),
           G(yol('M800 60 C680 70 580 150 540 300 C520 380 530 460 550 500 L800 500 Z'), gf(DERI, (700, 200), (550, 450))))
    A.ekle('majus', G(yol(VULVA_DIS), gf(DERI, (400, 150), (400, 460), radyal=True), st('#b9805a', 2)))
    A.ekle('vestibul', G(yol('M400 112 C350 120 334 220 346 320 C352 370 376 400 400 402 C424 400 448 370 454 320 C466 220 450 120 400 112 Z'), gf([(0, '#f2a9a6'), (1, '#c86e6c')], (400, 200), (400, 400), radyal=True)))
    A.ekle('minus', G(yol('M400 112 C356 118 330 200 336 300 C340 360 366 400 392 404 C366 380 356 330 358 280 C360 210 372 150 400 130 Z'), fl('#d9928c'), st('#a85f5a', 1.8)),
           G(yol('M400 112 C444 118 470 200 464 300 C460 360 434 400 408 404 C434 380 444 330 442 280 C440 210 428 150 400 130 Z'), fl('#d9928c'), st('#a85f5a', 1.8)))
    A.ekle('klitoris', G(el(400, 142, 16, 18), fl('#e3958f')), G(el(400, 208, 8, 14), fl('#7d2f2a')),
           G(yol('M400 252 C374 256 368 300 372 330 C376 356 390 370 400 370 C410 370 424 356 428 330 C432 300 426 256 400 252 Z'), fl('#8f3c3a'), st('#c9827c', 5)))
    renkler = ['#7a3410', '#9a4a18', '#b5551d']

    def pens(bez='#8a3a12'):
        """Gazlı bez (pens ucunda, antiseptikli) + pens kolları + mavi (steril olmayan) eldivenli el."""
        return [G(yol('M8 4 L150 92 M12 -4 L156 80'), st('#7d8794', 4)), G(el(158, 92, 16, 16), st('#7d8794', 3)), G(el(164, 80, 16, 16), st('#7d8794', 3)),
                yumruk(178, 106, .8, 32, steril=False), G(el(0, 0, 40, 34), fl(bez), st('#5c2508', 1.5)), G(el(-6, -6, 14, 9), fl('#c46a2c', o=70))]
    for i in range(3):
        e = K((0, 0), (T(1 + i), 0), (T(1 + i, .9), 100))
        A.ekle(f'iz{i}', G(yol(SPIRAL), st(renkler[i], 6 - i, o=70), tm(e)), o=K((0, 100), (T(4), 100), (T(4, .3), 0)))
        A.ekle(f'bez{i}', *pens(renkler[i]), p=A.boyunca(SPIRAL, T(1 + i), T(1 + i, .9), 60), o=K((0, 0), (T(1 + i) - 3, 0), (T(1 + i), 100), (T(1 + i, .92), 100), (T(1 + i, 1), 0)))
    # hazırlık: povidon kabı, beyaz gazlı bez kaba batırılıp kahverengi çıkar
    A.ekle('kap', G(yol('M600 330 C600 300 720 300 720 330 L712 400 C708 420 612 420 608 400 Z'), fl('#dfe6ee'), st('#7d8aa0', 2)), G(el(660, 330, 116, 26), fl('#7a3410')),
           o=K((0, 0), (T(0, .05), 0), (T(0, .15), 100), (T(0, 1), 100), (T(1, .05), 0)))
    A.ekle('bez-hazir', *pens('#ffffff'), p=K((0, [560, 180, 0]), (T(0, .2), [560, 180, 0]), (T(0, .45), [650, 330, 0]), (T(0, .7), [650, 330, 0]), (T(0, .95), [520, 220, 0])),
           o=K((0, 0), (T(0, .15), 0), (T(0, .2), 100), (T(0, .55), 100), (T(0, .56), 0)))
    A.ekle('bez-islak', *pens('#8a3a12'), p=K((0, [650, 330, 0]), (T(0, .55), [650, 330, 0]), (T(0, .95), [520, 220, 0])),
           o=K((0, 0), (T(0, .55), 0), (T(0, .56), 100), (T(0, 1) + 4, 100), (T(1), 0)))
    A.ekle('ortu', G(yol('M140 30 L660 30 L660 490 L140 490 Z'), yol('M400 100 C330 104 320 360 400 380 C480 360 470 104 400 100 Z'), fl_cift('#3b7bb8', o=100)),
           G(yol('M400 100 C330 104 320 360 400 380 C480 360 470 104 400 100 Z'), st('#2c5f91', 2)), o=A.gor(T(4, .45)))
    A.ekle('steril-eldiven', yumruk(690, 180, .7, -20, steril=True), o=K((0, 0), (T(4), 0), (T(4, .1), 100), (T(4, .45), 100), (T(4, .55), 0)))
    A.etiket(4, 4, 680, 100, 'Steril eldiven', 'dogru')
    A.etiket(0, 0, 660, 440, 'Antiseptiğe batırılan gazlı bez · steril olmayan eldiven', 'bilgi')
    for i in range(3):
        A.etiket(1 + i, 1 + i, 640, 80, f'{i + 1}. silme · merkezden dışa', 'bilgi')
    A.etiket(3, 3, 160, 80, 'Dıştan içe silme yok', 'uyari'); A.etiket(4, 4, 400, 470, 'Delikli örtü · steril alan', 'dogru')
    # kamera: bölüm başında ilgili bölgeye yumuşak yakınlaşma
    A.kamera(0, 640, 330, 130)
    A.kamera(1, 400, 250, 150)
    A.kamera(2, 400, 250, 150)
    A.kamera(3, 400, 250, 120)
    A.kamera(4, 400, 250, 100)
    return A


# ———————————————————————— 8. Erkekte temizlik ve lidokainli jel

def erkek_jel(z):
    A = _anim(z, 'erkek-jel', 'Erkekte temizlik ve lidokainli jel', [
        B('Prepisyum', 'Sünnetsiz hastada önce prepisyumu geriye çekersin.', 5),
        B('Temizlik', 'Meatustan başlayıp glans boyunca dışa doğru silersin ve bunu üç kez yaparsın.', 8),
        B('Jel ucu', 'Lidokainli jelin ucunu meatusa yerleştirirsin.', 5),
        B('Jeli ver', 'Çok sert basmadan tüpün tamamını üretraya verirsin.', 6),
        B('Bekle', 'Penisin ucunu sıkıca tutarak iki üç dakika beklersin; jeldeki lidokain anestezi sağlar.', 8),
    ], z)
    T = A.T
    zemin(A)
    A.ekle('saft', G(yol('M0 150 L260 140 L260 360 L0 350 Z'), gf(DERI, (100, 150), (100, 350)), st('#b9805a', 2)))
    A.ekle('uretra', G(yol('M566 250 L0 252'), st('#f0b8b2', 14)))
    A.ekle('glans', G(yol('M270 120 C420 90 560 160 570 250 C560 340 420 410 270 380 C250 330 250 170 270 120 Z'), gf([(0, '#f2b4ae'), (1, '#c97c77')], (380, 180), (500, 340), radyal=True), st('#a85f5a', 2.5)),
           G(yol('M300 140 C400 120 500 160 540 210'), st('#ffffff', 5, o=40)))
    A.ekle('dolum', G(yol('M566 250 L0 252'), st('#8fc7ff', 22, o=70), tm(K((0, 0), (T(3), 0), (T(3, .95), 100)))))
    A.ekle('meatus', G(yol('M566 222 C556 236 556 264 566 278 C574 264 574 236 566 222 Z'), fl('#6e2420')))
    # prepisyum: glansı örten deri kılıfı, şekil değiştirerek koronanın gerisine sıyrılır; geride kıvrımlar toplanır
    ort = 'M200 132 C300 120 470 110 556 204 C566 216 574 230 578 242 L578 258 C574 270 566 284 556 296 C470 390 300 380 200 368 Z'
    sir = 'M200 132 C224 128 248 126 262 128 C272 140 278 156 280 172 L280 328 C278 344 272 360 262 372 C248 374 224 372 200 368 Z'
    A.ekle('prepisyum', G(yol_morph(ort, sir, T(0, .15), T(0, .85)), gf(DERI, (300, 150), (300, 360)), st('#b9805a', 2)),
           G(yol_morph('M540 212 C556 226 562 240 566 250', 'M268 160 C276 200 278 240 278 250', T(0, .15), T(0, .85)), st('#c28a66', 2)))
    A.ekle('prepisyum-kivrim', *[G(yol(f'M{246 + i * 7} {150 + i * 4} C{258 + i * 7} 200 {258 + i * 7} 300 {246 + i * 7} {350 - i * 4}'), st('#b9805a', 1.6, o=70)) for i in range(3)],
           o=A.gor(T(0, .8)))
    A.ekle('cekme-ok', G(yol('M470 110 L330 110'), st('#2f6fd6', 5)), G(yol('M350 96 L326 110 L350 124'), st('#2f6fd6', 5)), o=K((0, 0), (T(0, .1), 0), (T(0, .2), 100), (T(0, .9), 100), (T(1), 0)))
    spr = 'M566 250 C546 250 536 220 556 200 C596 160 496 120 436 160 C356 210 376 360 466 370 C546 380 596 330 586 260'
    for i in range(3):
        A.ekle(f'temiz{i}', G(yol(spr), st(['#7a3410', '#9a4a18', '#b5551d'][i], 5, o=70), tm(K((0, 0), (T(1, i / 3), 0), (T(1, (i + .9) / 3), 100)))),
               o=K((0, 100), (T(2), 100), (T(2, .2), 0)))
        A.ekle(f'bez{i}', G(yol('M8 4 L150 92 M12 -4 L156 80'), st('#7d8794', 4)), yumruk(178, 106, .8, 32, steril=False),
               G(el(0, 0, 36, 30), fl(['#7a3410', '#9a4a18', '#b5551d'][i]), st('#5c2508', 1.5)),
               p=A.boyunca(spr, T(1, i / 3), T(1, (i + .9) / 3), 50), o=K((0, 0), (T(1, i / 3) - 2, 0), (T(1, i / 3), 100), (T(1, (i + .9) / 3), 100), (T(1, (i + .95) / 3), 0)))
    A.ekle('jel', G(rc(680, 250, 150, 36, 6), fl('#eef3f8', .92), st('#6b7a90', 2)), G(rc(670, 250, 110, 24), fl('#cfe6ff', .9)), G(rc(590, 250, 40, 10, 2), fl('#9aa6b4')),
           G(rc(760, 250, 14, 48, 3), fl('#6b7a90')),
           p=K((0, [300, 0, 0]), (T(2), [300, 0, 0]), (T(2, .8), [0, 0, 0]), (T(4, .2), [0, 0, 0]), (T(4, .5), [300, 0, 0])))
    # başparmak üstten, işaret parmağı alttan glansı sıkıştırır (jel üretrada kalsın, lidokain etki etsin)
    A.ekle('parmak', parmak_ucu(470, 138, -90, 1.7), parmak_ucu(470, 362, 90, 1.7), o=A.gor(T(4, .3)),
           p=K((0, [0, 0, 0]), (T(4, .3), [0, 0, 0]), (T(4, .45), [0, 0, 0])))
    A.sayac(4, .3, 4, 1, 0, 3, 'dk', 680, 120, 1)
    A.etiket(0, 0, 160, 100, 'Prepisyum geri', 'bilgi'); A.etiket(1, 1, 640, 420, 'Meatustan dışa · 3 kez', 'bilgi')
    A.etiket(3, 3, 200, 300, 'Jelin tamamı üretraya', 'bilgi'); A.etiket(4, 4, 400, 470, 'Ucu tut · 2–3 dk bekle', 'dogru')
    # kamera: bölüm başında ilgili bölgeye yumuşak yakınlaşma
    A.kamera(0, 260, 250, 150)
    A.kamera(1, 480, 250, 140)
    A.kamera(2, 600, 250, 200)
    A.kamera(3, 300, 250, 120)
    A.kamera(4, 400, 250, 110)
    return A


# ———————————————————————— 9. Glob vezikale ve sistit

def glob(z):
    A = _anim(z, 'glob-sistit', 'Glob vezikale mi, sistit mi?', [
        B('Dolan mesane', 'İdrarını yapamayan hastada mesane dolar ve giderek büyür.', 6),
        B('Glob', 'Glob vezikalede mesane kubbesi pubisin üstüne çıkar; alt karında kabarıklık oluşur.', 7),
        B('Muayene', 'Muayenede suprapubik bölgede şişlik ve dolgunluk ararsın.', 6),
        B('Ultrason', 'Ultrason mesanenin ağzına kadar dolu olduğunu gösterirse kateter endikasyonu kesinleşir.', 7),
        B('Sistit', 'Sistitte ise mesanede yalnız on beş yirmi mililitre idrar vardır; hasta idrar yapamıyorum dese de kateter gerekmez.', 9),
    ], z)
    T = A.T
    pelvis_zemin(A)
    A.ekle('uretra', G(yol('M330 268 C340 300 352 330 360 360 L368 440'), st('#d68c86', 9)))
    A.ekle('sisme', G(yol('M538 70 C600 110 612 220 560 300 C548 316 532 326 520 330 L506 252 C522 194 526 120 526 20 Z'), fl('#eec2a3')), o=K((0, 0), (T(1), 0), (T(1, .6), 100), (T(4), 100), (T(4, .4), 0)))
    A.ekle('simfiz', G(el(0, 0, 44, 88), gf(KEMIK, (-10, -30), (20, 40), radyal=True), st('#a8946b', 2.5), p=(420, 300), r=-18))
    A.ekle('mesane', G(el(0, 0, 150, 100), gf(MESANE, (-30, -30), (40, 50), radyal=True), st('#a8554e', 5)), G(el(0, 0, 126, 80), gf(IDRAR, (-20, -20), (30, 40), radyal=True)),
           p=K((0, [330, 245, 0]), (T(0), [330, 245, 0]), (T(1, .8), [345, 185, 0]), (T(4), [345, 185, 0]), (T(4, .4), [330, 250, 0])),
           s=K((0, [100, 100, 100]), (T(0), [100, 100, 100]), (T(1, .8), [150, 220, 100]), (T(4), [150, 220, 100]), (T(4, .4), [50, 50, 100])))
    A.ekle('iltihap', *[G(el(330 + dx, 250 + dy, 6, 6), fl('#9f1f1c')) for dx, dy in [(-20, -8), (14, 6), (20, -12), (-10, 12), (0, -16)]], o=A.gor(T(4, .4)))
    A.ekle('el', G(yol('M560 175 C590 150 650 140 700 150 L780 160 L780 230 L700 236 C660 240 610 232 586 220 C570 212 556 196 560 175 Z'), gf(DERI, (650, 160), (650, 236)), st('#b9805a', 2)),
           p=K((0, [80, 0, 0]), (T(2), [80, 0, 0]), (T(2, .4), [0, 0, 0]), (T(2, .6), [-10, 4, 0]), (T(2, .8), [0, 0, 0]), (T(3), [80, 0, 0])), o=K((0, 0), (T(2), 0), (T(2, .2), 100), (T(2, .95), 100), (T(3), 0)))
    # ultrason: probdan çıkan ince, saydam yelpaze + ekran penceresi (mesane siyah, ağzına kadar dolu)
    A.ekle('isin', G(yol('M583 153 L430 120 C420 160 420 200 432 236 Z'), fl('#cfe3f7', o=30)), G(yol('M583 153 L430 120 C420 160 420 200 432 236 Z'), st('#7fa8d6', 1.5, kesik=(6, 5))),
           o=K((0, 0), (T(3, .3), 0), (T(3, .5), 100), (T(4), 100), (T(4, .1), 0)))
    A.ekle('us-ekran', G(G(rc(150, 110, 230, 170, 14), fl('#0e1218'), st('#5b6676', 3)), G(yol('M150 40 L70 170 C120 190 180 190 230 170 Z'), fl('#3a4350')),
           G(el(150, 128, 96, 62), fl('#000000')), G(yol('M104 128 C110 100 190 100 196 128'), st('#8a96a6', 2, o=70)), p=(100, 0)),
           o=K((0, 0), (T(3, .45), 0), (T(3, .6), 100), (T(4), 100), (T(4, .1), 0)))
    A.ekle('prob', G(yol('M570 60 L630 60 L636 130 C636 146 564 146 564 130 Z'), fl('#e8edf2'), st('#5b6676', 2)), G(yol('M600 60 C620 30 660 20 700 10'), st('#3e4a58', 6)),
           p=S([560, 120, 0]), r=S(-35), a=(600, 100), o=K((0, 0), (T(3), 0), (T(3, .3), 100), (T(4), 100), (T(4, .1), 0)))
    A.etiket(1, 1, 640, 130, 'Suprapubik kabarıklık', 'bilgi'); A.etiket(2, 2, 680, 260, 'Palpasyon', 'bilgi')
    A.etiket(3, 3, 250, 215, 'Ultrasonda mesane ağzına kadar dolu', 'dogru'); A.etiket(4, 4, 330, 330, 'Sistit: 15–20 mL', 'uyari')
    A.etiket(4, 4, 400, 470, '"İdrar yapamıyorum" ≠ retansiyon', 'uyari')
    # kamera: bölüm başında ilgili bölgeye yumuşak yakınlaşma
    A.kamera(0, 330, 230, 140)
    A.kamera(1, 450, 180, 130)
    A.kamera(2, 600, 200, 150)
    A.kamera(3, 450, 160, 120)
    A.kamera(4, 330, 250, 180)
    return A


# ———————————————————————— 10. Pelvis travması

def travma(z):
    A = _anim(z, 'travma', 'Pelvis kırığı + meatusta kan: kateter yok', [
        B('Kuvvet', 'Yüksekten düşme ya da trafik kazası pelvise büyük bir kuvvet uygular.', 6),
        B('Kırık', 'Pubis kolunda kırık ve simfizde ayrılma oluşabilir.', 6),
        B('Kan', 'Buna erkekte meatusta taze kan eşlik ediyorsa üretra yaralanmış olabilir.', 6),
        B('Karar', 'Kısmi yırtıkta kateteri itmek yırtığı tamamlar; bu hastaya üretral kateter takılmaz.', 8),
    ], z)
    T = A.T
    zemin(A)
    titre = K((0, [0, 0, 0]), (T(0, .5), [0, 0, 0]), (T(0, .55), [10, 0, 0]), (T(0, .6), [-8, 0, 0]), (T(0, .65), [6, 0, 0]), (T(0, .7), [0, 0, 0]))
    def ayna(d):
        import re
        out, k = [], 0
        for s in re.findall(r'[MLCZ]|-?\d*\.?\d+', d):
            if s in 'MLCZ':
                out.append(s); k = 0
            else:
                out.append(str(round(800 - float(s), 2)) if k % 2 == 0 else s); k += 1
        return ' '.join(out)
    ILIUM = 'M360 70 C320 40 220 30 150 60 C110 78 96 120 108 160 C120 196 150 218 190 232 L240 236 C280 220 320 196 352 168 Z'
    HALKA = 'M244 248 C300 236 360 236 388 232 L388 304 C360 330 320 350 286 340 C250 330 236 290 244 248 Z'
    DELIK = 'M318 268 C344 268 356 280 356 292 C356 306 340 314 318 314 C296 314 282 304 282 292 C282 280 294 268 318 268 Z'
    for taraf, f, isaret in (('sol', lambda d: d, -1), ('sag', ayna, 1)):
        x = (lambda v: v) if taraf == 'sol' else (lambda v: 800 - v)
        A.ekle(taraf, G(yol(f('M200 262 L172 300 L160 480')), st('#a8946b', 44)), G(yol(f('M200 262 L172 300 L160 480')), st('#ece2c8', 40)),
               G(el(x(166), 300, 46, 40), gf(KEMIK, (x(150), 290), (x(180), 316), radyal=True), st('#a8946b', 1.5)),
               G(yol(f(ILIUM)), gf(KEMIK, (x(200), 60), (x(300), 230)), st('#a8946b', 2)), G(yol(f('M150 64 C210 40 300 44 352 74')), st('#ffffff', 3, o=60)),
               G(yol(f(HALKA)), yol(f(DELIK)), fl_cift('#efe4c9'), st('#a8946b', 2)), G(yol(f(DELIK)), st('#a8946b', 1.5)),
               G(el(x(215), 262, 70, 70), fl('#d9cba9'), st('#a8946b', 2)), G(el(x(215), 262, 54, 54), gf(KEMIK, (x(205), 252), (x(225), 272), radyal=True), st('#a8946b', 1.5)),
               p=K((0, [0, 0, 0]), (T(0, .5), [0, 0, 0]), (T(0, .55), [10, 0, 0]), (T(0, .6), [-8, 0, 0]), (T(0, .7), [0, 0, 0]), (T(1, .3), [0, 0, 0]), (T(1, .8), [14 * isaret, 0, 0])))
    A.ekle('sakrum', G(yol('M350 60 L450 60 C452 100 446 140 432 170 L410 196 L390 196 L368 170 C354 140 348 100 350 60 Z'), gf(KEMIK, (380, 80), (420, 190)), st('#a8946b', 2)),
           *[G(el(x, y, 10, 10), fl('#cdbd98')) for x in (378, 422) for y in (85, 115, 145)], p=titre)
    A.ekle('ok', G(yol('M60 260 L190 260'), st('#d23b3b', 10)), G(yol('M170 238 L196 260 L170 282'), st('#d23b3b', 10)),
           p=K((0, [-120, 0, 0]), (T(0, .1), [-120, 0, 0]), (T(0, .5), [0, 0, 0])), o=K((0, 0), (T(0, .1), 0), (T(0, .2), 100), (T(1), 100), (T(1, .2), 0)))
    A.ekle('kirik', G(yol('M292 248 L304 266 L296 280 L312 300 L304 318'), st('#d23b3b', 5), tm(K((0, 0), (T(1), 0), (T(1, .5), 100)))))
    A.ekle('penis', G(yol('M368 400 C368 390 432 390 432 400 L428 470 C424 490 376 490 372 470 Z'), gf(DERI, (380, 400), (420, 490)), st('#b9805a', 2)),
           G(yol('M400 304 L400 480'), st('#f0b8b2', 9)))
    A.ekle('kan', G(yol('M400 478 C396 486 392 492 392 497 C392 502 396 505 400 505 C404 505 408 502 408 497 C408 492 404 486 400 478 Z'), fl('#b3201f')), G(el(397, 495, 3, 5), fl('#ffffff', o=70)),
           s=K((0, [0, 0, 100]), (T(2), [0, 0, 100]), (T(2, .6), [130, 130, 100])), a=(400, 478), p=S([400, 474, 0]))
    A.ekle('kateter', G(yol('M400 620 L400 500'), st('#eef2f6', 8)), p=K((0, [0, 80, 0]), (T(3), [0, 80, 0]), (T(3, .3), [0, 0, 0])), o=A.gor(T(3)))
    A.ekle('carpi', G(yol('M340 380 L460 500 M460 380 L340 500'), st('#d23b3b', 14)), o=A.gor(T(3, .4)))
    A.etiket(0, 0, 130, 220, 'Darbe', 'uyari'); A.etiket(1, 1, 250, 345, 'Pubis kırığı', 'uyari'); A.etiket(1, 1, 400, 210, 'Simfiz ayrılması', 'uyari')
    A.etiket(2, 2, 520, 470, 'Meatusta taze kan', 'uyari'); A.etiket(3, 3, 620, 420, 'Üretral kateter YOK', 'uyari')
    # kamera: bölüm başında ilgili bölgeye yumuşak yakınlaşma
    A.kamera(0, 300, 250, 110)
    A.kamera(1, 330, 270, 170)
    A.kamera(2, 400, 400, 170)
    A.kamera(3, 400, 420, 140)
    return A


# ———————————————————————— 11. Malzeme hazırlığı

def malzeme(z):
    A = _anim(z, 'malzeme-hazirlik', 'Malzemeyi hazırlamak ve steril alan', [
        B('Kateter', 'Önce uygun boyda üretral kateteri seçersin: erişkinde on iki ile yirmi dört French arası.', 7),
        B('Eldivenler', 'Temizlik için steril olmayan, yerleştirme için steril eldiven hazırlarsın.', 6),
        B('Jel ve balon', 'Kayganlaştırıcı jel, balon için steril izotonik ve enjektör tepsiye konur.', 6),
        B('Geniş uçlu enjektör', 'İdrar gelmezse kontrol için geniş uçlu kateter enjektörünü unutmazsın.', 6),
        B('Temizlik ve torba', 'Antiseptik, gazlı bez, delikli örtü ve idrar torbası da hazır olmalıdır.', 6),
        B('Steril alan', 'Steril malzemeyi yardımcın açar; sen steril eldivenle yalnız steril alana dokunursun.', 7),
    ], z)
    T = A.T
    zemin(A)
    A.ekle('tepsi', G(rc(400, 250, 780, 470, 24), gf([(0, '#8b96a3'), (.4, '#eef2f6'), (1, '#6d7884')], (400, 10), (400, 490))), G(rc(400, 250, 756, 446, 18), gf([(0, '#dfe6ec'), (1, '#c7d1da')], (400, 30), (400, 470))))
    ogeler = [
        (0, 140, 110, [G(yol('M60 140 C90 110 130 170 170 120 C190 100 210 104 220 110'), st('#e3b544', 10)), G(rc(64, 150, 14, 12, 3), fl('#ef7d22'))]),
        (1, 330, 110, [G(rc(330, 110, 120, 80, 8), fl('#eaf1f8'), st('#8a9bb0', 1.5)), G(rc(330, 110, 60, 50, 6), fl('#cfe0f5'))]),
        (1, 500, 110, [G(rc(500, 110, 120, 80, 8), fl('#fbfaf6'), st('#c9b48a', 1.5)), G(rc(500, 110, 60, 50, 6), fl('#efe2c8'))]),
        (2, 140, 260, [G(rc(140, 260, 130, 26, 6), fl('#eef3f8'), st('#6b7a90', 1.5)), G(rc(130, 260, 90, 16), fl('#cfe6ff'))]),
        (2, 330, 260, [G(rc(320, 260, 24, 60, 6), fl('#eef3f8'), st('#6b7a90', 1.5)), G(rc(350, 260, 24, 60, 6), fl('#eef3f8'), st('#6b7a90', 1.5))]),
        (2, 500, 260, [G(rc(500, 260, 100, 22, 3), fl('#eef3f8'), st('#6b7a90', 1.5)), G(rc(560, 260, 24, 6), fl('#9aa6b4'))]),
        (3, 670, 260, [G(rc(660, 260, 130, 36, 4), fl('#eef3f8'), st('#6b7a90', 1.5)), G(rc(740, 260, 34, 10), fl('#9aa6b4'))]),
        (4, 140, 410, [G(rc(120, 410, 40, 74, 9), fl('#9a4518')), G(el(190, 420, 90, 50), fl('#c5cdd6'), st('#5b6676', 1.5))]),
        (4, 330, 410, [G(rc(330, 410, 150, 100), fl('#3b7bb8')), G(el(330, 410, 36, 36), fl('#dfe6ec'))]),
        (4, 500, 410, [G(rc(500, 410, 100, 110, 10), fl('#f4f7fa'), st('#9aa6b4', 2)), G(rc(500, 445, 90, 40, 6), fl('#f2cf55'))]),
    ]
    for j, (b, x, y, sh) in enumerate(ogeler):
        k = T(b, .2 + .1 * (j % 3))
        A.ekle(f'oge{j}', *sh, p=K((0, [0, -520, 0]), (k, [0, -520, 0]), (k + 18, [0, 0, 0])), o=A.gor(k))
    A.ekle('steril', G(rc(450, 185, 560, 330, 14), fl('#cfe7d8', .35), st('#2e9e5b', 4, kesik=(14, 8))), o=A.gor(T(5, .2)))
    A.etiket(0, 0, 140, 170, '12–24 Fr', 'bilgi'); A.etiket(1, 1, 330, 170, 'Steril olmayan', 'bilgi'); A.etiket(1, 1, 500, 170, 'Steril', 'bilgi')
    A.etiket(2, 2, 330, 320, 'Jel · izotonik · enjektör', 'bilgi'); A.etiket(3, 3, 670, 320, 'Geniş uçlu enjektör', 'uyari')
    A.etiket(4, 4, 330, 475, 'Antiseptik · örtü · torba', 'bilgi'); A.etiket(5, 5, 450, 30, 'Steril alan', 'dogru')
    # kamera: bölüm başında ilgili bölgeye yumuşak yakınlaşma
    A.kamera(0, 140, 110, 200)
    A.kamera(1, 415, 110, 170)
    A.kamera(2, 330, 260, 140)
    A.kamera(3, 670, 260, 200)
    A.kamera(4, 330, 410, 130)
    A.kamera(5, 400, 250, 100)
    return A


# ———————————————————————— 12. İletişim ve mahremiyet

def mahremiyet(z):
    A = _anim(z, 'mahremiyet', 'Kendini tanıt, onam al, mahremiyeti sağla', [
        B('Tanış', 'Kendini tanıtır, hastaya neden kateter takılması gerektiğini anlatır ve sözlü onamını alırsın.', 8),
        B('Paravan', 'Paravanı ya da perdeyi kapatarak mahremiyeti sağlarsın; kateter ortalık yerde takılmaz.', 7),
        B('Yardımcı', 'Yanına yardımcı bir sağlık personeli alırsın; karşı cinsten hastada karşı cinsten personel, çocukta ebeveyn bulunur.', 9),
    ], z)
    T = A.T
    zemin(A)
    A.ekle('hasta', *yatan_hasta(220, 290, .95))
    A.ekle('hekim', *kisi(90, 110, olcek=1.0, beyaz=True))
    A.ekle('balon', G(yol('M140 60 L330 60 C344 60 344 110 330 110 L190 110 L160 130 L168 110 L140 110 C126 110 126 60 140 60 Z'), fl('#ffffff'), st('#2f6fd6', 2)),
           o=K((0, 0), (T(0, .1), 0), (T(0, .2), 100), (T(1), 100), (T(1, .1), 0)))
    for i in range(3):
        A.ekle(f'paravan{i}', G(rc(0, 0, 32, 400, 4), fl('#e6eef7', .9), st('#7d8aa0', 2)),
               p=K((0, [880, 250, 0]), (T(1, .1 + i * .1), [880, 250, 0]), (T(1, .5 + i * .1), [680 + i * 34, 250, 0])))
    A.ekle('yardimci', *kisi(670, 330, '#8fc1c9', .9, sac='#5a3a24'), p=K((0, [200, 0, 0]), (T(2), [200, 0, 0]), (T(2, .4), [0, 0, 0])))
    A.etiket(0, 0, 235, 85, 'Tanıt · anlat · onam', 'bilgi'); A.etiket(1, 1, 700, 30, 'Paravan', 'bilgi')
    A.etiket(2, 2, 660, 488, 'Yardımcı personel', 'dogru')
    # kamera: bölüm başında ilgili bölgeye yumuşak yakınlaşma
    A.kamera(0, 160, 150, 150)
    A.kamera(1, 700, 250, 130)
    A.kamera(2, 560, 330, 130)
    return A


URETICILER = [mahremiyet, malzeme, glob, travma, idrar_akisi, kadin_temizlik, kadin_ilerleyis, erkek_jel, erkek_ilerleyis, balon, yikama, yanlis_balon]


def uret():
    ses = json.loads(SES.read_text(encoding='utf-8')) if SES.exists() else {}
    CIKTI.mkdir(parents=True, exist_ok=True)
    idx = []
    for f in URETICILER:
        on = f(None)
        k = ses.get(f'l-{on.ad}')
        z = k['zaman'] if k and len(k['zaman']) == len(on.bolumler) else None
        A = f(z) if z else on
        (CIKTI / f'{A.ad}.json').write_text(json.dumps(A.json(), ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
        bilgi = A.bilgi()
        bilgi['sesli'] = bool(z)
        idx.append(bilgi)
        print(f'{A.ad}: {A.sure:.1f} sn, {len(A.bolumler)} bölüm, {len(A.katmanlar)} katman{" (ses zamanlı)" if z else ""}')
    (CIKTI / 'index.json').write_text(json.dumps(idx, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    (CIKTI / 'balon.json').unlink(missing_ok=True)


if __name__ == '__main__':
    uret()
