#!/usr/bin/env python3
"""Sesli ders sesinin düşük bit hızlı kopyası (yavaş bağlantı alternatifi, H709, 2026-11-27).

Her `data/sesli_anlatim/ses/<key>/<vid>.mp3` için `data/sesli_anlatim/ses_dusuk/<key>/<vid>.mp3` (32 kbps, tek kanal,
kaynakla aynı örnekleme hızı → süre ve kelime zamanları birebir aynı) + `<vid>.json` {kaynakBayt, sure, kbps} yazar.
Sunucu (src/services/canliDers.ts) düşük kopyayı YALNIZ kaynak dosyanın bayt boyutu `kaynakBayt` ile aynıysa verir; ses
Oracle'da onarılmış/yeniden üretilmişse eski kopya çalınmaz, yüksek bit hızına düşülür.

LLM yok, GPU yok (CUDA_VISIBLE_DEVICES=""), ffmpeg `nice -n 19`. Kaynak ≤ 40 kbps ise kopya üretilmez (kazanç < %20).
Süre kaynaktan 0,3 sn'den fazla saparsa kopya silinir (zaman kayması işaretlemeyi bozar).

Kullanım:
  python3 scripts/uretim/sesli_anlatim/dusuk_bit.py [--is 4] [--ders <key>] [--kuru]
  sonra Oracle'a: bash deploy/oracle/ses_esitle.sh (ses_dusuk kökü dahil)
"""
import argparse
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path as _P

_s = _P(__file__).resolve()
while not (_s / 'kok.py').exists() and _s != _s.parent:
    _s = _s.parent
sys.path.insert(0, str(_s))
from kok import MEDS  # noqa: E402

HEDEF_KBPS = 32
ESIK_KBPS = 40
KOKLER = [MEDS / 'data/sesli_anlatim', MEDS / 'data/arsiv_25_26/sesli_anlatim']
ORTAM = {**os.environ, 'CUDA_VISIBLE_DEVICES': ''}


def bilgi(f: _P):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration,bit_rate', '-of', 'json', str(f)],
                         capture_output=True, text=True, env=ORTAM)
    fm = json.loads(out.stdout or '{}').get('format', {})
    return float(fm.get('duration') or 0), int(fm.get('bit_rate') or 0)


def isle(kaynak: _P, hedef: _P, kuru: bool) -> str:
    yan = hedef.with_suffix('.json')
    bayt = kaynak.stat().st_size
    try:
        if hedef.exists() and json.loads(yan.read_text()).get('kaynakBayt') == bayt:
            return 'güncel'
    except Exception:
        pass
    sure, br = bilgi(kaynak)
    if not sure or (br and br <= ESIK_KBPS * 1000):
        return 'atla'
    if kuru:
        return 'üretilecek'
    hedef.parent.mkdir(parents=True, exist_ok=True)
    gecici = hedef.with_suffix('.tmp.mp3')
    r = subprocess.run(['nice', '-n', '19', 'ffmpeg', '-v', 'error', '-y', '-threads', '1', '-i', str(kaynak),
                        '-map', '0:a', '-ac', '1', '-b:a', f'{HEDEF_KBPS}k', '-map_metadata', '-1', str(gecici)],
                       capture_output=True, text=True, env=ORTAM)
    if r.returncode != 0:
        gecici.unlink(missing_ok=True)
        return f'HATA ffmpeg: {r.stderr.strip()[:120]}'
    s2, _ = bilgi(gecici)
    if abs(s2 - sure) > 0.3:
        gecici.unlink(missing_ok=True)
        return f'HATA süre {sure:.2f} ≠ {s2:.2f}'
    gecici.replace(hedef)
    yan.write_text(json.dumps({'kaynakBayt': bayt, 'sure': round(sure, 3), 'kbps': HEDEF_KBPS,
                               'bayt': hedef.stat().st_size}, ensure_ascii=False))
    return 'üretildi'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--is', dest='isci', type=int, default=4)
    ap.add_argument('--ders')
    ap.add_argument('--kuru', action='store_true')
    a = ap.parse_args()
    isler = []
    for kok in KOKLER:
        for f in sorted((kok / 'ses').glob('*/*.mp3')):
            if a.ders and f.parent.name != a.ders:
                continue
            isler.append((f, kok / 'ses_dusuk' / f.parent.name / f.name))
    sayac: dict[str, int] = {}
    with ThreadPoolExecutor(max_workers=max(1, a.isci)) as ex:
        for (f, _), sonuc in zip(isler, ex.map(lambda x: isle(x[0], x[1], a.kuru), isler)):
            k = sonuc.split(' ')[0]
            sayac[k] = sayac.get(k, 0) + 1
            if k == 'HATA':
                print(f'  {f.parent.name}/{f.name}: {sonuc}', flush=True)
    print('özet:', sayac)
    return 1 if sayac.get('HATA') else 0


if __name__ == '__main__':
    sys.exit(main())
