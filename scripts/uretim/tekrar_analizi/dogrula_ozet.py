import json, sys, os
# Konum-bağımsız kök (2026-11-16): kod git'te, çalışma verisi meds_temp/tekrar_analizi (TEKRAR_KOK ile değişir).
import sys as _sys
from pathlib import Path as _Path
_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402
D = os.environ.get("TEKRAR_KOK") or str(_kok.PROJE / "meds_temp" / "tekrar_analizi"); h = 0
for pid in sys.argv[1:]:
    p = json.load(open(f'{D}/parti/{pid}.json'))
    try: s = {x['id']: x for x in json.load(open(f'{D}/sonuc/{pid}.json'))}
    except Exception as e: print(pid, 'HATA okunamadı', e); h += 1; continue
    for q in p['sorular']:
        x = s.get(q['id'])
        if not x: print(pid, q['id'], 'HATA eksik'); h += 1; continue
        if not isinstance(x.get('anlamsal'), (int, float)) or not 0 <= x['anlamsal'] <= 100: print(pid, q['id'], 'HATA anlamsal'); h += 1
        if x.get('pasaj') not in range(len(q['pasajlar'])): print(pid, q['id'], 'HATA pasaj'); h += 1
    print(pid, len(p['sorular']), len(s))
print(f'{h} HATA')
