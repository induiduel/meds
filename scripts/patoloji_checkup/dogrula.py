"""Patoloji Hızlı Check Up içerik doğrulayıcı.

src/data/patoloji_checkup/*.json: her tablo satırı sütun sayısına eşit, boş hücre yok, her tablo/not kaynaklı;
kaynak "kod:slayt" biçiminde ve slayt ders PDF metninde (meds_temp/patoloji_onem/pdf_metin) var; Türkçe üslup kapısı.
Ayrıca src/data/patoloji_checkup/dersler.json (kod → ders adı) üretir.
Kullanım: python3 scripts/patoloji_checkup/dogrula.py [--kurul N]
  --kurul N (2+): veri src/data/patoloji_checkup/k<N>/, kaynak PDF metni meds_temp/spot_cozucu/k<N>patoloji/pdf_metin,
  kaynak kodu ders defteri kodu ("2p03:12"); dersler.json yazılmaz (adlar src/data/dersler/k<N>.json'dan).
"""
import glob, json, os, re, sys
KOK = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(KOK, 'scripts'))
from turkce_uslup import denetle_yapi

KURUL = int(sys.argv[sys.argv.index('--kurul') + 1]) if '--kurul' in sys.argv else 1
if KURUL == 1:
    VERI = os.path.join(KOK, 'src/data/patoloji_checkup')
    PDF = os.path.join(os.path.dirname(KOK), 'meds_temp/patoloji_onem/pdf_metin')
    KOD_RE = r'([0-9]+b?):(\d+)'
else:
    VERI = os.path.join(KOK, f'src/data/patoloji_checkup/k{KURUL}')
    PDF = os.path.join(os.path.dirname(KOK), f'meds_temp/spot_cozucu/k{KURUL}patoloji/pdf_metin')
    KOD_RE = rf'({KURUL}p\d{{2}}):(\d+)'
    if not glob.glob(os.path.join(VERI, '[0-9][0-9]-*.json')):
        print(f'Kurul {KURUL}: Check Up verisi yok — 0 tablo, 0 HATA'); sys.exit(0)

sayfalar, adlar = {}, {}
for f in glob.glob(os.path.join(PDF, '*.md')):
    kod = os.path.basename(f)[:-3]
    t = open(f, encoding='utf-8').read()
    adlar[kod] = re.sub(r'\.pdf$', '', t.split('\n', 1)[0].lstrip('# ').strip()).strip()
    sayfalar[kod] = {int(n) for n in re.findall(r'=== SAYFA (\d+) ===', t)}

H, tablo_say, satir_say, not_say = [], 0, 0, 0
idler = set()
def kaynak(k, yer):
    m = re.fullmatch(KOD_RE, k or '')
    if not m: H.append(f'{yer}: kaynak biçimi bozuk {k!r}'); return
    kod, s = m.group(1), int(m.group(2))
    if kod not in sayfalar: H.append(f'{yer}: ders kodu yok {kod}')
    elif s not in sayfalar[kod]: H.append(f'{yer}: {kod} dersinde slayt {s} yok')

for f in sorted(glob.glob(os.path.join(VERI, '[0-9][0-9]-*.json'))):
    ad = os.path.basename(f)
    d = json.load(open(f, encoding='utf-8'))
    for alan in ('id', 'ad', 'kisa', 'tablolar', 'notlar'):
        if not d.get(alan): H.append(f'{ad}: {alan} eksik')
    for t in d.get('tablolar', []):
        yer = f"{ad}#{t.get('id')}"
        tablo_say += 1
        if t.get('id') in idler: H.append(f'{yer}: tekrar eden id')
        idler.add(t.get('id'))
        if not t.get('baslik'): H.append(f'{yer}: başlık yok')
        if not t.get('k'): H.append(f'{yer}: kaynak yok')
        for k in t.get('k', []): kaynak(k, yer)
        n = len(t.get('sutun', []))
        if n < 2: H.append(f'{yer}: en az 2 sütun gerekir')
        for i, r in enumerate(t.get('satir', [])):
            satir_say += 1
            if len(r) != n: H.append(f'{yer} satır {i+1}: {len(r)} hücre, {n} sütun')
            for c in r:
                if not isinstance(c, str) or not c.strip(): H.append(f'{yer} satır {i+1}: boş hücre')
    for i, nt in enumerate(d.get('notlar', [])):
        not_say += 1
        if not nt.get('m'): H.append(f'{ad} not {i+1}: metin yok')
        kaynak(nt.get('k'), f'{ad} not {i+1}')
    H.extend(denetle_yapi({x: d[x] for x in ('ad', 'kisa', 'tablolar', 'notlar') if x in d}, ad))

if KURUL == 1:
    json.dump(dict(sorted(adlar.items())), open(os.path.join(VERI, 'dersler.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for h in H: print('HATA', h)
print(f'{tablo_say} tablo, {satir_say} satır, {not_say} not — {len(H)} HATA')
sys.exit(1 if H else 0)
