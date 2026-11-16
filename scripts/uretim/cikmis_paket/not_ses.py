#!/usr/bin/env python3
"""Çıkmış çözücü kısa notlarını EMA ile seslendirir (yalnız CPU).

Kaynak: scripts/uretim/cikmis_paket/notlar.json — sesli asistanı olmayan derslerdeki çıkmışlar için slayttan yazılmış ve bağımsız
denetçiden geçmiş notlar ({"<brans>/<çözücü ders kodu>/<soru no>": {baslik, cumleler, kaynak_sayfa, kaynak}}).
Klip: meds/data/<brans>_cozucu/ses/<ses klasörü>/n-<soru no>.mp3 (+ o klasörün kayit.json'u; ses.py n-* kliplerini silmez),
yani /api/cozucu-ses/<brans>/ema/<klasör>/n-<no>.mp3. Metni değişmeyen klip yeniden üretilmez. Sonra paketle.py çalıştırılır.

Kullanım: bash meds/scripts/uretim/cikmis_paket/not_ses.sh   (ses_kuyruk.sh ile aynı kilit ve kaynak tavanı)
"""
# Konum-bağımsız kök (2026-11-16): sabit parents[N] yerine scripts/kok.py (dosya taşınsa da doğru).
import sys as _sys
from pathlib import Path as _Path
_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402
import json, re, sys
from pathlib import Path

MEDS = _kok.MEDS
sys.path.insert(0, str(MEDS / 'scripts/uretim/spot_cozucu'))
import ses as SES  # noqa: E402

notlar = json.loads((Path(__file__).parent / 'notlar.json').read_text())
S = SES.SESLER['ema']['sinif']()
gruplar: dict[tuple[str, str], dict[str, list[str]]] = {}
for anahtar, v in notlar.items():
    brans, kod, no = anahtar.split('/')
    d = json.loads((MEDS / 'src/data' / f'{brans}_cozucu' / f'{kod}.json').read_text())
    klasor = d.get('klasor') or d['kod']
    duz = [SES.nokta(re.sub(r'\*\*', '', c)) for c in v['cumleler']]
    ekk = SES.kisaltmalar(*duz)
    gruplar.setdefault((brans, klasor), {})[f'n-{no}'] = [S.ses_metni(c, ekk) for c in duz]
for (brans, klasor), K in sorted(gruplar.items()):
    SES.klasor(S, SES.ses_klasoru(brans, 'ema'), klasor, K, SES.SESLER['ema']['kbps'], silinsin=False)
