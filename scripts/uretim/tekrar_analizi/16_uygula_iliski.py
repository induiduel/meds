"""İlişki + cevap–özet kanıtı alanlarını pastQuestions.json'a yazar (kuru varsayılan; --yaz). Önce: systemctl --user stop meds-web.

- iliski {ozet[], deste[], dersNotu[], pdf[], surum}: soru_iliskileri.json'dan (12_soru_iliski.py)
- ozetKaniti: YALNIZ sözcüksel benzerlik ≥ 0,60 VE anlamsal bütünlük ≥ 90 (alt ajan yargısı) olan sorulara
  {ozetId, ozetBaslik, satir, metin, benzerlik, anlamsal, konuDisi, surum}. Gizli kopyalar asılınkini devralır.
  Pasaj işaretli cevapla çelişiyorsa (anlamsal < 90 olsa da) `ozetCelisiyor` notu düşülür (cevap anahtarı şüphesi).
"""
import json, glob, os, sys, shutil, datetime, collections, re
RX = re.compile(r'(?m)(^|\s)[A-E]\s*[\)\.]\s+\S.*\n?.*(^|\s)[B-E]\s*[\)\.]\s|çıkmış|ÇIKMIŞ|Doğru Cevap|Doğru cevap|Çözüm|Sınav sorusu|Soru \d', re.S)
ROOT = '/home/indu/medsor'
PQ = f'{ROOT}/meds/src/data/pastQuestions.json'
YAZ = '--yaz' in sys.argv
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
SURUM = 'ozet-kanit-v1'
mt0 = os.path.getmtime(PQ)
Q = json.load(open(PQ)); by = {q['id']: q for q in Q}
S = json.load(open(f'{ROOT}/meds_database_v2/iliski/soru_iliskileri.json'))
MG = json.load(open(f'{ROOT}/meds_database_v2/soru_birlestirme/birlestirmeler.json'))['gruplar']
kopyalar = collections.defaultdict(list)
for g in MG:
    if g.get('durum') == 'ayrildi': continue
    for u in g['uyeler']:
        if u != g['asil']: kopyalar[g['asil']].append(u)
parti = {}
for f in glob.glob('ozet_cevap/parti/a*.json'):
    for s in json.load(open(f))['sorular']: parti[s['id']] = s
sonuc = {}
for f in glob.glob('ozet_cevap/sonuc/a*.json'):
    for x in json.load(open(f)): sonuc[x['id']] = x
st = collections.Counter(); kanit = {}; celiski = {}
for i, s in parti.items():
    x = sonuc.get(i)
    if not x: st['sonucsuz'] += 1; continue
    p = s['pasajlar'][x['pasaj']]
    if x.get('celisiyor'): celiski[i] = {'ozetId': p['ozet'], 'satir': p['satir'], 'not': x.get('not', ''), 'surum': SURUM}
    if p['benzerlik'] >= 0.60 and x['anlamsal'] >= 90:
        kanit[i] = {'ozetId': p['ozet'], 'ozetBaslik': p['ozet_baslik'], 'satir': p['satir'], 'metin': p['metin'][:600],
                    'benzerlik': round(p['benzerlik'], 3), 'anlamsal': x['anlamsal'], 'konuDisi': bool(p['konu_disi']), 'pasajTuru': 'cikmis_soru_blogu' if RX.search(p['metin']) else 'anlatim', 'surum': SURUM}
        st['kanitli_' + kanit[i]['pasajTuru']] += 1; st['konu_disi'] += bool(p['konu_disi'])
    else:
        st['esik_alti'] += 1
st['celisiyor'] = len(celiski)
degisen = 0
for q in Q:
    r = S.get(q['id'])
    if r:
        q['iliski'] = {'ozet': [o['id'] for o in r['ozetler']], 'deste': [d['id'] for d in r['desteler']][:3],
                       'dersNotu': [d['id'] for d in r['dersNotlari']], 'pdf': [p['ad'] for p in r['pdf']][:3], 'surum': 'iliski-v1'}
    q.pop('ozetKaniti', None); q.pop('ozetCelisiyor', None)
for a, k in kanit.items():
    for i in [a] + kopyalar.get(a, []):
        if i in by: by[i]['ozetKaniti'] = dict(k, kaynakSoru=a) if i != a else k; degisen += 1
for a, c in celiski.items():
    for i in [a] + kopyalar.get(a, []):
        if i in by: by[i]['ozetCelisiyor'] = c
st['kanit_yazilan_kayit'] = degisen
print(dict(st), 'görünen soru (anlamsal incelenen):', len(parti))
json.dump({'kanit': kanit, 'celiski': celiski, 'ozet': dict(st)}, open('ozet_cevap/sonuc_ozeti.json', 'w'), ensure_ascii=False, indent=1)
if not YAZ: print('kuru çalıştırma (--yaz)'); sys.exit(0)
assert os.path.getmtime(PQ) == mt0, 'pastQuestions.json değişti — yeniden çalıştır'
Y = f'{ROOT}/yedek/ozet_kanit_{datetime.datetime.now().strftime("%Y%m%d%H%M")}'; os.makedirs(Y, exist_ok=True)
shutil.copy(PQ, f'{Y}/pastQuestions.json')
json.dump(Q, open(PQ + '.tmp', 'w'), ensure_ascii=False); os.replace(PQ + '.tmp', PQ)
shutil.copy(PQ, f'{ROOT}/meds/data/pastQuestions.json')
print('YAZILDI; yedek:', Y)
