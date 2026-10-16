"""cikti/<kod>.json (dogrula 0 HATA) → meds/src/data/patoloji_onem_k1.json (dersler PDF sırasıyla + bağlanan çıkmış sorular)."""
import glob, json, os, re, subprocess, sys
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = '/home/indu/medsor/meds/src/data/patoloji_onem_k1.json'
L = {x['kod']: x for x in json.load(open(f'{W}/pdf_liste.json'))}
C = json.load(open(f'{W}/cikmis_pdf.json'))
cik_by = {c['id']: c for v in C.values() for c in v}
dersler, cik, eksik = [], {}, []
NEDEN = json.load(open(f'{W}/neden/cikti.json')) if os.path.exists(f'{W}/neden/cikti.json') else {}
for kod in sorted(L, key=lambda k: (int(re.match(r'\d+', k).group()), k)):
    p = f'{W}/cikti/{kod}.json'
    if not os.path.exists(p): eksik.append(kod); continue
    r = subprocess.run([sys.executable, f'{W}/araclar/dogrula.py', p], capture_output=True, text=True)
    if r.returncode:
        if '--taslak' in sys.argv: eksik.append(kod + '(hata)'); continue
        sys.exit(f'{kod}: doğrulama HATA — birleştirilmez\n{r.stdout[-800:]}')
    d = json.load(open(p))
    d['no'] = int(re.match(r'\d+', L[kod]['ad']).group()); d['pdf'] = L[kod]['ad']; d['kod'] = kod
    if kod in NEDEN: d['neden_onemli'] = NEDEN[kod]
    sp = f'{W}/sinav/cikti/{kod}.json'
    if os.path.exists(sp):
        sv = json.load(open(sp))
        for m in d['maddeler']:
            v = sv['maddeler'].get(m['id']) or {}
            m['kaynak'] = v.get('kaynak', 'metin'); m['klinik'] = bool(v.get('klinik')); m['sinavUygun'] = m['kaynak'] == 'metin' and not m['klinik']
        d['sinavAdaylari'] = sv['adaylar']; d['soruSayisi'] = 2 if kod == '15' else 1
    elif '--taslak' not in sys.argv: sys.exit(f'{kod}: sınav ayrımı yok')
    d['maddeler'].sort(key=lambda m: -m['puan'])
    for m in d['maddeler']:
        for i in m.get('cikmis') or []:
            c = cik_by[i]; cik[i] = {'sinav': c['sinav'], 'kok': c['kok'], 'secenekler': c['secenekler'], 'dogru': c['dogru']}
    dersler.append({k: d[k] for k in ('kod', 'no', 'baslik', 'pdf', 'ozet', 'neden_onemli', 'maddeler', 'sinavAdaylari', 'soruSayisi') if k in d})
# ders başına dosya (görünüm yalnız seçilen dersi indirir) + küçük dizin
import shutil
OD = '/home/indu/medsor/meds/src/data/patoloji_onem'
if os.path.isdir(OD): shutil.rmtree(OD)
os.makedirs(OD)
for d in dersler:
    ids = {i for m in d['maddeler'] for i in (m.get('cikmis') or [])}
    json.dump({**d, 'cikmis': {i: cik[i] for i in sorted(ids)}}, open(f'{OD}/{d["kod"]}.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
idx = {'surum': 'patoloji-onem-v1', 'kaynak': "Kurul 1 Tıbbi Patoloji ders PDF'leri (2026-27 Drive)",
       'dersler': [{'kod': d['kod'], 'no': d['no'], 'baslik': d['baslik'], 'madde': len(d['maddeler']),
                    'bant': {str(b): sum(1 for m in d['maddeler'] if min(max(m['puan'] // 10, 4), 9) == b) for b in range(4, 10)}} for d in dersler]}
json.dump(idx, open(f'{OD}/index.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
if os.path.exists(OUT): os.remove(OUT)
print(len(dersler), 'ders ·', sum(len(d['maddeler']) for d in dersler), 'madde ·', len(cik), 'çıkmış · eksik', eksik)
