#!/usr/bin/env python3
"""KMB görsel asistan EMA sesleri (GPU; AGENTS.md kural 10, EMA daima GPU):
  bash meds/scripts/patoloji_cozucu/cozucu_ses_gpu.sh meds/scripts/kmb/ses.py 02
Klipler data/kmb_cozucu/ses/<kod>/<klip>.mp3 (→ /api/cozucu-ses/kmb/ema/<kod>/…), zamanlama src/data/kmb/ses_<kod>.json.
Klip adları: l-<lottie> video anlatımı (bölüm = cümle; sonra lottie_uret.py yeniden) · a-<akış>-<basamak> basamak açıklaması · o-<adım> öğretim · s-<vaka> soru · s-<vaka>-<şık> geri bildirim · b-<görev> yönerge · b-<görev>-d doğru."""
import json, re, subprocess, sys
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
if subprocess.run([sys.executable, str(MEDS / 'scripts/kmb/dogrula.py'), *sys.argv[1:]]).returncode:
    sys.exit('dogrula.py HATA verdi — ses üretilmedi')
sys.path.insert(0, str(MEDS / 'scripts/patoloji_cozucu'))
import cozucu_ses as C  # noqa: E402  (EMA modeli, seslendir, klasör önbelleği)

C.CIKTI = MEDS / 'data/kmb_cozucu/ses'
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
    lidx = VERI / 'lottie/index.json'
    if lidx.exists() and d['kod'] == '02':
        for v in json.loads(lidx.read_text(encoding='utf-8')):
            K[f'l-{v["ad"]}'] = [oku(b['metin']) for b in v['bolumler']]
    for b in d['sinav']['bul']:
        K[f'b-{b["id"]}'] = [oku(b['yonerge'])]
        K[f'b-{b["id"]}-d'] = ['Doğru.'] + [oku(x) for x in C.cumlele(b['aciklama'])]
    return K


def main(kodlar):
    m = C.Model()
    for kod in kodlar:
        d = json.loads((VERI / f'{kod}.json').read_text(encoding='utf-8'))
        C.klasor(m, kod, klipler(d))
        kayit = json.loads((C.CIKTI / kod / 'kayit.json').read_text(encoding='utf-8'))
        (VERI / f'ses_{kod}.json').write_text(json.dumps({k: {'h': v['h'], 'sure': v['sure'], 'zaman': v['zaman']}
                                                          for k, v in kayit.items()}, ensure_ascii=False) + '\n', encoding='utf-8')


if __name__ == '__main__':
    idx = json.loads((VERI / 'index.json').read_text(encoding='utf-8'))
    main(sys.argv[1:] or [b['kod'] for b in idx['beceriler'] if b['durum'] == 'hazir'])
