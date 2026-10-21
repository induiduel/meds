#!/usr/bin/env python3
"""YZ yargılarını doğrular ve analiz.py'ye bağlar.

Girdi: meds_temp/oncelikli/yz/<key>.json (Claude ajanları; talimat meds_temp/oncelikli/TALIMAT.md).
Çıktı:
  scripts/oncelikli_dersler/yz/k<N>.json   ders başına puan + tür + gerekçe + ezber çekirdeği + konu türleri
  turkce_sozcukler.txt / ek_terimler.txt   YZ'nin terim çıkarıcıda bulduğu hatalar (yanlış pozitif / kaçan terim)
  --rapor: düzeltmeden sonra kalan hataları ders ders sayar (analiz.py --dok çıktısıyla karşılaştırır).

Kullanım:
  python3 scripts/oncelikli_dersler/yz_birlestir.py [--kurul 1]
  python3 scripts/oncelikli_dersler/analiz.py --dok meds_temp/oncelikli/terimler
  python3 scripts/oncelikli_dersler/yz_birlestir.py --rapor
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analiz import METIN, kok, vocab_kur  # noqa: E402

BURADA = Path(__file__).resolve().parent
TEMP = BURADA.parents[2] / 'meds_temp' / 'oncelikli'
TURLER = {'mantik', 'karma', 'ezber'}


def hata(key: str, y: dict) -> list[str]:
    h = []
    for k in ('azEzber', 'mantik'):
        if not isinstance(y.get(k), (int, float)) or not 0 <= y[k] <= 100:
            h.append(f'{k} 0–100 olmalı')
    if y.get('kolayCikmis') is not None and not (isinstance(y['kolayCikmis'], (int, float)) and 0 <= y['kolayCikmis'] <= 100):
        h.append('kolayCikmis 0–100 ya da null olmalı')
    if y.get('tur') not in TURLER:
        h.append('tur geçersiz')
    if not isinstance(y.get('gerekce'), str) or len(y['gerekce']) < 40:
        h.append('gerekce eksik')
    for k in ('ezberCekirdegi', 'konular', 'yanlisTerim', 'kacanTerim'):
        if not isinstance(y.get(k), list):
            h.append(f'{k} liste olmalı')
    for k in y.get('konular') or []:
        if not isinstance(k, dict) or k.get('tur') not in TURLER or not k.get('baslik'):
            h.append('konular ögesi geçersiz')
            break
    if y.get('key') != key:
        h.append('key dosya adıyla aynı değil')
    return h


def liste_yaz(ad: str, ogeler: set[str], baslik: str) -> None:
    f = BURADA / ad
    eski = {x.split('#')[0].strip() for x in f.read_text().splitlines()} if f.exists() else set()
    hepsi = sorted((eski | ogeler) - {''})
    f.write_text(f'# {baslik}\n# yz_birlestir.py üretir; elle ekleme serbest (satır başına bir kök)\n' + '\n'.join(hepsi) + '\n')


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--kurul', type=int, default=1)
    ap.add_argument('--rapor', action='store_true')
    a = ap.parse_args()
    vocab_kur(p.read_text() for p in METIN.glob(f'k{a.kurul}-*.md'))
    dosyalar = sorted((TEMP / 'yz').glob(f'k{a.kurul}-*.json'))

    if a.rapor:
        top_y = top_k = top_t = 0
        for f in dosyalar:
            y = json.loads(f.read_text())
            d = TEMP / 'terimler' / f.name
            if not d.exists():
                continue
            terim = set(json.loads(d.read_text())['terimler'])
            kalan_y = sorted(terim & {kok(t) for t in y['yanlisTerim']})
            kalan_k = sorted({kok(t) for t in y['kacanTerim']} - terim)
            top_y += len(kalan_y); top_k += len(kalan_k); top_t += len(terim)
            if kalan_y or kalan_k:
                print(f'{f.stem[:44]:44} yanlış {len(kalan_y):2} {kalan_y[:4]}  kaçan {len(kalan_k):2} {kalan_k[:4]}')
        print(f'TOPLAM: {top_t} terim · kalan yanlış pozitif {top_y} · kalan kaçan {top_k}')
        return

    cikti, yanlis, kacan, hatalar = {}, set(), set(), 0
    for f in dosyalar:
        try:
            y = json.loads(f.read_text())
        except json.JSONDecodeError as e:
            print(f'HATA {f.name}: JSON bozuk ({e})'); hatalar += 1; continue
        h = hata(f.stem, y)
        if h:
            print(f'HATA {f.name}: {", ".join(h)}'); hatalar += 1; continue
        yanlis |= {kok(t) for t in y['yanlisTerim'] if isinstance(t, str)}
        kacan |= {kok(t) for t in y['kacanTerim'] if isinstance(t, str)}
        cikti[f.stem] = {k: y.get(k) for k in ('azEzber', 'mantik', 'kolayCikmis', 'tur', 'gerekce', 'ezberCekirdegi', 'konular', 'cikmisNot')}
    celiski = yanlis & kacan  # bir ajan "Türkçe", öteki "terim" dedi: terim sayılır (ezber yükü tarafında kal)
    yanlis -= celiski
    hedef = BURADA / 'yz' / f'k{a.kurul}.json'
    hedef.parent.mkdir(exist_ok=True)
    hedef.write_text(json.dumps(cikti, ensure_ascii=False, indent=1) + '\n')
    liste_yaz('turkce_sozcukler.txt', {t for t in yanlis if len(t) >= 4}, 'Terim sanılan Türkçe / genel sözcükler')
    liste_yaz('ek_terimler.txt', {t for t in kacan if len(t) >= 2}, 'Terim çıkarıcının kaçırdığı yabancı terimler')
    print(f'{len(cikti)} ders · {hatalar} HATA · yanlış pozitif {len(yanlis)} · kaçan {len(kacan)} · çelişki {len(celiski)} → {hedef.name}')
    sys.exit(1 if hatalar else 0)


if __name__ == '__main__':
    main()
