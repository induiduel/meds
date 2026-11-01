"""2B sahne kitaplığının Lottie tarafı: svg_lottie.py çıktısını (svg/<sahne>.lottie.json) üreticilere sunar.

    from sahne2b import Sahne2B
    s = Sahne2B('erkek')
    s.ekle(A)                                  # görünür katmanları (gizli ögeler hariç) belge sırasıyla A'ya ekler
    s.ekle(A, dahil=['e-kateter'], o=...)      # gizli bir ögeyi de (kendi opaklık anahtarıyla) ekler
    A.ekle('kateter', *s.katman('e-kateter'), o=K(...))   # tek ögeyi ayrıca, animasyonlu
    s.bbox('e-mesane') → (x, y, w, h); s.merkez('e-mesane') → (cx, cy); s.cz('e-kateter') → [{d, w, renk}]
Katman `it` listeleri belge sırasındadır (alttan üste); Anim.ekle Lottie için ters çevirir. Her çağrı derin kopya verir.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

KOK = Path(__file__).resolve().parent / 'svg'


class Sahne2B:
    def __init__(self, ad: str):
        self.ad = ad
        d = json.loads((KOK / f'{ad}.lottie.json').read_text(encoding='utf-8'))
        self.katmanlar = d['katmanlar']
        self._bbox = d['bbox']
        self.gizli = set(d['gizli'])
        self._cz = d['cz']
        self.metin = d['metin']

    def ids(self):
        return [k['id'] for k in self.katmanlar if k['id']]

    def katman(self, id_: str):
        it = [copy.deepcopy(k['it']) for k in self.katmanlar if k['id'] == id_]
        if not it:
            raise KeyError(f'{self.ad}: öge yok {id_}')
        return [g for parca in it for g in parca]

    def bbox(self, id_: str):
        return tuple(self._bbox[id_])

    def merkez(self, id_: str):
        x, y, w, h = self.bbox(id_)
        return (x + w / 2, y + h / 2)

    def cz(self, id_: str):
        return copy.deepcopy(self._cz.get(id_, []))

    def ekle(self, A, dahil=(), haric=(), o=None, on_ek=''):
        """Katmanları sırayla A'ya ekler. Gizli ögeler yalnız `dahil` ile; `haric` atlanır; `o` tüm katmanlara uygulanır.
        Dönüş: {id: katman adı}."""
        adlar = {}
        for k in self.katmanlar:
            i = k['id']
            if i and (i in haric or (i in self.gizli and i not in dahil)):
                continue
            if not i and 'arka' in haric:
                continue
            nm = on_ek + k['nm']
            A.ekle(nm, *copy.deepcopy(k['it']), o=o)
            if i:
                adlar[i] = nm
        return adlar
