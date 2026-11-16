#!/usr/bin/env python3
"""v15 Soru haritası dizini: data/pastQuestions.json (96 MB) → src/data/soru_haritasi.json (küçük).
Kurul × ders × sınav yılı soru sayıları. Yalnız sayım; LLM yok. Çıkmış verisi değişince yeniden çalıştırılır:
    python3 scripts/altyapi/v15/soru_haritasi.py
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
import json, collections, pathlib, datetime, re
kok = _kok.MEDS
qs = json.load(open(_kok.CIKMIS))
say = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
yillar = set()
for q in qs:
    # H391: isPastExam alanı hiç olmayan çıkmışlar (178 soru, kaynakları çıkmış sınav PDF'leri) atlanıyordu; çıkmış sayfası
    # onları gösteriyor. Yalnız açıkça false olan ve gizli sorular dışarıda kalır (çıkmış sayfasıyla aynı ölçüt)
    if q.get('isPastExam') in (False, 'false', 'False', 0, '0') or q.get('hidden'):
        continue
    y = q.get('examYear') or ''
    if not y or y in ('Kategorisiz', 'Çıkmış Soru'):
        continue
    m = re.fullmatch(r'(\d{4})-(\d{4})', y.strip())
    # Yalnız ardışık öğretim yılı (2023-2024) sütun olur; "2021-2026", "(Geçen Sene)", "Arşiv", "belirsiz" tek sütunda
    y = y.strip() if m and int(m.group(2)) - int(m.group(1)) == 1 else 'Yılı belirsiz'
    k = str(q.get('kurul') or '').strip()
    d = (q.get('discipline') or '').strip()
    if not k.isdigit() or not d:
        continue
    say[k][d][y] += 1
    yillar.add(y)
cikti = {
    'uretildi': datetime.date.today().isoformat(),
    'yillar': sorted(yillar - {'Yılı belirsiz'}) + (['Yılı belirsiz'] if 'Yılı belirsiz' in yillar else []),
    'kurullar': {k: {d: dict(c) for d, c in sorted(v.items(), key=lambda x: -sum(x[1].values()))} for k, v in sorted(say.items(), key=lambda x: int(x[0]))},
}
(kok / 'src/data/soru_haritasi.json').write_text(json.dumps(cikti, ensure_ascii=False, separators=(',', ':')))
print('yıllar', cikti['yillar'], 'kurullar', list(cikti['kurullar']), 'boyut', (kok / 'src/data/soru_haritasi.json').stat().st_size)
