#!/usr/bin/env python3
"""Gemini varyantında her parçanın sonundaki kısa "kapanış" patlamasını sessizlikle değiştirir (zamanlama değişmez).

Kullanım: kapanis_temizle.py <key> <vid> [--kuru]
Parça sonu = parçanın son paragrafının zamanlama sonu. [son-1.6 sn, son] içinde, konuşmadan ≥0,12 sn boşlukla ayrılmış
ve 0,35 sn'den kısa son ses parçası bulunursa sıfırlanır (10 ms yumuşatmayla). Dosya tek seferde yeniden kodlanır;
eskisi <vid>.kapanis-oncesi.mp3 olarak saklanır.
"""
import json, os, struct, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import yonerge_kes as y

PEN = 480  # 20 ms


def sesli(pcm, i, esik=600):
    w = pcm[i:i + PEN]
    return bool(w) and max(abs(x) for x in w) > esik


def main():
    key, vid = sys.argv[1], sys.argv[2]
    kuru = '--kuru' in sys.argv
    SR = y.SR
    kayit = json.load(open(y.KOK / 'kayit.json'))
    v = next(x for x in kayit[key] if x['id'] == vid)
    zam = v['zamanlama']
    ch = y.parcalar(y.paragraflar(open(y.KOK / 'metin' / f'{key}.md', encoding='utf-8').read()))
    mp3 = y.KOK / 'ses' / key / f'{vid}.mp3'
    pcm = y.coz(mp3)
    n = 0
    for ci, c in enumerate(ch):
        son = min(len(pcm), int(zam[c['idx'][-1]][1] * SR))
        bas = max(0, son - int(3.2 * SR))
        k = son
        while k > bas and not sesli(pcm, k - PEN): k -= PEN          # son sesli pencerenin bitişi
        kb = k
        while kb > bas and sesli(pcm, kb - PEN): kb -= PEN           # son ses parçasının başı
        bos = kb
        while bos > bas and not sesli(pcm, bos - PEN): bos -= PEN    # önceki boşluğun başı
        if 0 < k - kb < 0.35 * SR and kb - bos >= 0.12 * SR and bos > bas:
            f = 240
            for i in range(kb - f, k + f):
                if 0 <= i < len(pcm): pcm[i] = 0
            n += 1
            print(f'  parça {ci + 1:2d}: {(k - kb) / SR:.2f} sn kapanış sesi silindi ({kb / SR:.1f}–{k / SR:.1f} sn)')
        else:
            print(f'  parça {ci + 1:2d}: kapanış sesi bulunmadı')
    print(f'{n}/{len(ch)} parçada temizlendi')
    if kuru or n == 0: return
    yedek = mp3.with_name(f'{vid}.kapanis-oncesi.mp3')
    if not yedek.exists(): os.rename(mp3, yedek)
    raw = struct.pack('<%dh' % len(pcm), *pcm)
    subprocess.run([y.FF, '-v', 'error', '-y', '-f', 's16le', '-ar', str(SR), '-ac', '1', '-i', '-', '-b:a', '64k', str(mp3)], input=raw, check=True)
    kayit = json.load(open(y.KOK / 'kayit.json'))
    v = next(x for x in kayit[key] if x['id'] == vid)
    v['bayt'] = mp3.stat().st_size
    v['onarim'] = (v.get('onarim') or '') + '; kapanış sesleri silindi'
    tmp = y.KOK / 'kayit.json.tmp'; json.dump(kayit, open(tmp, 'w'), ensure_ascii=False, indent=1); os.replace(tmp, y.KOK / 'kayit.json')
    print('yazıldı:', mp3)


if __name__ == '__main__':
    main()
