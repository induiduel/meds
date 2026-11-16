#!/usr/bin/env python3
"""Gemini varyantının paragraf zamanlamasını sesteki gerçek duraklamalara oturtur (yeniden ses üretmeden).

Kullanım: zaman_oturt.py <key> <vid> [--kuru]
Parça sınırları korunur (parçanın ilk paragraf başı / son paragraf sonu); yalnız parça içi paragraf sınırları,
karakter oranı tahmininin ±pay çevresindeki en uzun duraklamaya kaydırılır (sunucudaki sessizligeOturt ile aynı kural).
"""
import json, os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import yonerge_kes as y


def main():
    key, vid = sys.argv[1], sys.argv[2]
    kuru = '--kuru' in sys.argv
    kayit = json.load(open(y.KOK / 'kayit.json'))
    v = next(x for x in kayit[key] if x['id'] == vid)
    zam = [list(t) for t in v['zamanlama']]
    pars = y.paragraflar(open(y.KOK / 'metin' / f'{key}.md', encoding='utf-8').read())
    ch = y.parcalar(pars)
    pcm = y.coz(y.KOK / 'ses' / key / f'{vid}.mp3')
    SR = y.SR
    sessiz = [(a / SR, b / SR) for a, b in y.sessizlikler(pcm, 0, len(pcm), esik=400, min_sn=0.22)]
    oynayan = 0
    for c in ch:
        idx = c['idx']
        for j in range(1, len(idx)):
            i = idx[j]
            tahmin = zam[i][0]
            pay = max(1.5, 0.3 * min(zam[i - 1][1] - zam[i - 1][0], zam[i][1] - zam[i][0]))
            en, enp = None, -1e9
            for g in sessiz:
                orta = (g[0] + g[1]) / 2
                if abs(orta - tahmin) > pay or g[1] <= zam[i - 1][0] + 0.5 or g[0] >= zam[i][1] - 0.5:
                    continue
                p = (g[1] - g[0]) * 2 - abs(orta - tahmin) / pay
                if p > enp: en, enp = g, p
            if en:
                sinir = round(max(en[0], en[1] - 0.1), 2)
                oynayan += abs(sinir - tahmin) > 0.3
                zam[i - 1][1] = sinir; zam[i][0] = sinir
    print(f'{len(zam)} paragraf, {oynayan} sınır 0,3 sn\'den fazla düzeltildi')
    if kuru: return
    kayit = json.load(open(y.KOK / 'kayit.json'))
    v = next(x for x in kayit[key] if x['id'] == vid)
    v['zamanlama'] = zam; v['zamanlamaKaynak'] = 'sessizlik'
    tmp = y.KOK / 'kayit.json.tmp'; json.dump(kayit, open(tmp, 'w'), ensure_ascii=False, indent=1); os.replace(tmp, y.KOK / 'kayit.json')
    print('yazıldı')


if __name__ == '__main__':
    main()
