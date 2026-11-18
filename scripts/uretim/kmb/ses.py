#!/usr/bin/env python3
"""KMB görsel asistan EMA sesleri (GPU; AGENTS.md kural 10, EMA daima GPU):
  bash meds/scripts/uretim/patoloji_cozucu/cozucu_ses_gpu.sh meds/scripts/uretim/kmb/ses.py 02
Klipler data/kmb_cozucu/ses/<kod>/<klip>.mp3 (→ /api/cozucu-ses/kmb/ema/<kod>/…), zamanlama src/data/kmb/ses_<kod>.json.
Klip adları: l-<lottie> video anlatımı (bölüm = cümle; sonra lottie_uret.py yeniden) · a-<akış>-<basamak> basamak açıklaması · o-<adım> öğretim · s-<vaka> soru · s-<vaka>-<şık> geri bildirim · b-<görev> yönerge · b-<görev>-d doğru."""
# Konum-bağımsız kök (2026-11-16): sabit parents[N] yerine scripts/kok.py (dosya taşınsa da doğru).
import sys as _sys
from pathlib import Path as _Path
_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402
import json, re, subprocess, sys
from pathlib import Path

MEDS = _kok.MEDS
if subprocess.run([sys.executable, str(MEDS / 'scripts/uretim/kmb/dogrula.py'), *sys.argv[1:]]).returncode:
    sys.exit('dogrula.py HATA verdi — ses üretilmedi')
sys.path.insert(0, str(MEDS / 'scripts/uretim/patoloji_cozucu'))
import cozucu_ses as C  # noqa: E402  (EMA modeli, SURUM/KBPS, cumlele/nokta)
sys.path.insert(0, str(MEDS / 'scripts/uretim/ses_ortak'))
import ses_klip as SK  # noqa: E402  (2026-11-16: C.CIKTI genel durumunu ezmek yerine ortak klasör üretimi)
import ses_metin  # noqa: E402

CIKTI = MEDS / 'data/kmb_cozucu/ses'
VERI = MEDS / 'src/data/kmb'
OKUNUS = [(r'(\d+)\s*[–-]\s*(\d+)\s*mL', r'\1 ile \2 mililitre'), (r'\bmL\b', 'mililitre'), (r'(\d+)\s*cm\b', r'\1 santimetre'),
          (r'(\d+)\s*[–-]\s*(\d+)\s*dakika', r'\1 ile \2 dakika'), (r'\bFr\b', 'French'), (r'→', ', '), (r'≠', ' değildir, '),
          (r'\+', ' ve '), (r'✓|✗', '')]


def oku(s: str) -> str:
    for a, b in OKUNUS:
        s = re.sub(a, b, s)
    return C.nokta(re.sub(r'\s+', ' ', s).strip())


def klipler(d: dict) -> dict[str, list[str]]:
    K = {f'o-{a["id"]}': [oku(c['metin']) for c in a['cumleler']] for a in d['adimlar']}
    for s in d['sinav']['senaryolar']:
        K[f's-{s["id"]}'] = [oku(s['soru'])]
        for i, c in enumerate(s['secenekler']):
            K[f's-{s["id"]}-{i}'] = ['Doğru.' if c['dogru'] else 'Yanlış.'] + [oku(x) for x in C.cumlele(c['aciklama'])]
    def gez(L, ak):
        for b in L:
            K[f'a-{ak}-{b["id"]}'] = [oku(b['metin'])] + [oku(x) for x in C.cumlele(b['aciklama'])]
            for yol in (b.get('dal') or {}).get('yollar', []):
                gez(yol['basamaklar'], ak)
    for ak in d['sinav']['akislar']:
        gez(ak['basamaklar'], ak['id'])
    for x in d.get('hedefCalisma', []):
        K[f'h-{x["no"]}'] = [oku(f'Hedef {x["no"]}. {x["ne"]}'), *[oku(c) for c in x['nasil']], oku(x['neden']), 'Sınavda sık yapılan bir hata var.', oku(x['hata'])]
        K[f'h-{x["no"]}-s'] = [oku(f'Hedef {x["no"]}. {x["hoca"]}'), 'Önce kendin sesli anlat, sonra cevabı aç.']
    for x in d.get('rehberBasamaklari', []):  # Basamak filmi (KMB Eğitim Rehberi sırası)
        K[f'p-{x["no"]}'] = [oku(f'Basamak {x["no"]}. {x["ne"]}'), *[oku(c) for c in x['nasil']], oku(x['neden']), 'Sınavda sık yapılan bir hata var.', oku(x['hata'])]
        K[f'p-{x["no"]}-s'] = [oku(f'Basamak {x["no"]}. {x["hoca"]}'), 'Önce kendin sesli anlat, sonra cevabı aç.']
    lidx = VERI / ('lottie/index.json' if d['kod'] == '02' else 'lottie2b/index.json')  # 01: yalnız 2B, ad öneki ng-
    if lidx.exists() and d['kod'] in ('02', '01'):
        for v in json.loads(lidx.read_text(encoding='utf-8')):
            if d['kod'] == '01' and not v['ad'].startswith('ng-'): continue
            K[f'l-{v["ad"]}'] = [oku(b['metin']) for b in v['bolumler']]
    for b in d['sinav']['bul']:
        K[f'b-{b["id"]}'] = [oku(b['yonerge'])]
        K[f'b-{b["id"]}-d'] = ['Doğru.'] + [oku(x) for x in C.cumlele(b['aciklama'])]
    return K


def main(kodlar):
    m = C.Model()
    for kod in kodlar:
        d = json.loads((VERI / f'{kod}.json').read_text(encoding='utf-8'))
        ok = ses_metin.okuyucu(yol='uzun', modul='kmb_cozucu')  # çözücü klipleri tasarım gereği uzun yol (eski C.klasor ile aynı)
        SK.klasor(CIKTI / kod, klipler(d), surum=f'{C.SURUM}|{C.E.HIZ}',
                  uret=lambda c: SK.seslendir(m(), c, okunus=ok, kbps=C.KBPS, E=C.E), log=C.E.log)
        kayit = json.loads((CIKTI / kod / 'kayit.json').read_text(encoding='utf-8'))
        (VERI / f'ses_{kod}.json').write_text(json.dumps({k: {'h': v['h'], 'sure': v['sure'], 'zaman': v['zaman']}
                                                          for k, v in kayit.items()}, ensure_ascii=False) + '\n', encoding='utf-8')


if __name__ == '__main__':
    idx = json.loads((VERI / 'index.json').read_text(encoding='utf-8'))
    main(sys.argv[1:] or [b['kod'] for b in idx['beceriler'] if b['durum'] == 'hazir'])
