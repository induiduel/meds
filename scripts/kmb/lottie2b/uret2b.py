"""KMB konu videoları — 2B düz çizgi film hattı (eski lottie_uret.py korunur; bu dosya src/data/kmb/lottie2b/ üretir).
  python3 meds/scripts/kmb/lottie2b/uret2b.py [ad…]   → lottie2b/<ad>.json + lottie2b/index.json
Üreticiler: burada `erkek_ilerleyis` (referans uygulama) + uret2b_a.py / uret2b_b.py (kalan 11). Her üretici
`anim(z, ad, baslik, bolumler)` ile başlar (alt kompozisyon olarak da çağrılabilir), sahneyi `Sahne2B` ile kurar,
koreografiyi ortak2b yardımcılarıyla yazar. Bölüm metinleri ve adları ESKİ hat ile aynı kalır (ses klipleri l-<ad>).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ortak2b import (CIKTI, SES, B, G, K, Sahne2B, akis, anim, balon, el, et, fl, halka, ilerleyen_kateter, st, yol)  # noqa: E402

# ———————————————————————— 1. Erkekte kateter ilerleyişi (referans uygulama)

# Erkek sahnesi (sahneler.tsx): meatus (482,140) → penil (486,262) → bulbar kıvrım → sfinkter (445,362) → prostatik → boyun (408,326) → mesane
URETRA_E = 'M482 140 L486 262 L488 352 C488 382 456 384 448 368 L442 356 C432 344 420 334 408 326 L378 312 L356 300'
# ilerleme yolu: kateter yukarıdan (kadraj dışı, hekimin elinden) beslenir
KATETER_YOL = 'M482 -420 L482 140 L486 262 L488 352 C488 382 456 384 448 368 L442 356 C432 344 420 334 408 326 L378 312 L356 300'


def erkek_ilerleyis(z):
    A = anim(z, 'erkek-ilerleyis', 'Erkekte kateterin üretrada ilerleyişi', [
        B('Anatomi', 'Erkek alt üriner sistemini yandan görüyoruz: mesane, prostat, eksternal sfinkter, bulbar ve penil üretra.', 7),
        B('Tutuş', 'Kateteri avucunda toplar, penisi dik ve gergin tutarsın; böylece üretranın kıvrımı düzleşir.', 6),
        B('Penil üretra', 'Kateter meatustan girer ve düz penil üretrada kolayca ilerler.', 5),
        B('Bulbar kıvrım', 'Bulbar üretranın kıvrımında hafif direnç olabilir; zorlamadan, sabit ve yavaş bir basınçla devam edersin.', 7),
        B('Sfinkter', 'Eksternal sfinkterin bulunduğu membranöz üretra en dar bölümdür.', 5),
        B('Prostatik üretra', 'Prostatik üretrayı geçen kateter mesane boynundan mesaneye ulaşır.', 5),
        B('İdrar geldi', 'İdrar geldi; ama erkekte kateteri yine de çatal kısmına kadar, sonuna kadar ilerletirsin.', 7),
        B('Balon mesanede', 'Böylece balon kesinlikle mesanede olur ve güvenle şişirilebilir.', 5),
    ])
    T = A.T
    s = Sahne2B('erkek')
    s.ekle(A)  # gövde, kesit, mesane, prostat, sfinkter, üretra, el, penis, skrotum, örtü, küvet (gizli ögeler hariç)
    # s1: düzleştirme kılavuzu (dik penis boyunca üretra hattı)
    A.ekle('kilavuz', G(yol('M482 120 L486 262 L488 352'), st('#2f6fd6', 3, kesik=(10, 8))), o=A.gor(T(1), T(2, .5)))
    # s2–s6: uç meatus → penil → bulbar → sfinkter → prostatik → boyun → mesane içi
    ilerleyen_kateter(A, KATETER_YOL, [(T(2), (482, 140)), (T(2, 1), (486, 262)), (T(3, 1), (448, 368)), (T(4, 1), (438, 350)),
                                       (T(5, .7), (408, 326)), (T(5, 1), (384, 315)), (T(6, .8), (356, 300))], o=A.gor(T(2) - 2))
    halka(A, 462, 372, 44, 34, 3)
    halka(A, 445, 362, 30, 30, 4, renk='#d23b3b')
    # s6: idrar lümenden dışa (yukarı, kadraj dışına)
    akis(A, 'M360 302 L378 312 L408 326 C420 334 432 344 442 356 L448 368 C456 384 488 382 488 352 L486 262 L482 140 L482 -40', T(6, .1))
    # s7: balon mesanede
    balon(A, 378, 312, 17, T(7), T(7, .6), o=A.gor(T(7)))
    A.ekle('balon-halka', G(el(378, 312, 70, 60), st('#2e9e5b', 3, kesik=(6, 6))), o=A.gor(T(7, .5)))
    for x, y, m in [(344, 224, 'Mesane'), (540, 352, 'Prostat'), (520, 404, 'Eksternal sfinkter'), (570, 300, 'Bulbar üretra'), (590, 196, 'Penil üretra'), (590, 106, 'Meatus')]:
        A.etiket(0, 0, x, y, m)
    A.etiket(1, 1, 596, 180, 'Penis dik ve gergin', 'bilgi')
    A.etiket(3, 3, 560, 420, 'Kıvrım: zorlama yok', 'uyari')
    A.etiket(4, 4, 540, 420, 'En dar bölüm', 'uyari')
    A.etiket(6, 6, 620, 90, 'İdrar geldi: yine sonuna kadar', 'bilgi')
    A.etiket(7, 7, 330, 378, 'Balon mesanede ✓', 'dogru')
    A.kamera(1, 486, 230, 150)
    A.kamera(2, 486, 220, 170)
    A.kamera(3, 462, 350, 200)
    A.kamera(4, 445, 350, 220)
    A.kamera(5, 410, 330, 200)
    A.kamera(6, 440, 240, 130)
    A.kamera(7, 378, 300, 200)
    return A


def ureticiler():
    out = [erkek_ilerleyis]
    for mod in ('uret2b_a', 'uret2b_b'):
        try:
            m = __import__(mod)
            out += list(m.URETICILER)
        except ImportError:
            pass
    return out


def uret(secili=None):
    ses = json.loads(SES.read_text(encoding='utf-8')) if SES.exists() else {}
    CIKTI.mkdir(parents=True, exist_ok=True)
    idx_yol = CIKTI / 'index.json'
    idx = {x['ad']: x for x in json.loads(idx_yol.read_text(encoding='utf-8'))} if idx_yol.exists() else {}
    for f in ureticiler():
        on = f(None)
        if secili and on.ad not in secili:
            continue
        k = ses.get(f'l-{on.ad}')
        z = k['zaman'] if k and len(k['zaman']) == len(on.bolumler) else None
        A = f(z) if z else on
        (CIKTI / f'{A.ad}.json').write_text(json.dumps(A.json(), ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
        bilgi = A.bilgi(); bilgi['sesli'] = bool(z)
        idx[A.ad] = bilgi
        print(f'{A.ad}: {A.sure:.1f} sn, {len(A.bolumler)} bölüm, {len(A.katmanlar)} katman{" (ses zamanlı)" if z else ""}')
    sira = ['mahremiyet', 'malzeme-hazirlik', 'glob-sistit', 'travma', 'idrar-akisi', 'kadin-temizlik', 'kadin-ilerleyis', 'erkek-jel', 'erkek-ilerleyis', 'balon-sisme', 'yikama-testi', 'yanlis-balon']
    idx_yol.write_text(json.dumps([idx[a] for a in sira if a in idx] + [v for a, v in idx.items() if a not in sira], ensure_ascii=False, indent=1) + '\n', encoding='utf-8')


if __name__ == '__main__':
    uret([a for a in sys.argv[1:] if not a.startswith('--')] or None)
