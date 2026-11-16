"""Kopya kararları + sınav birimi kuralı → birleştirme grupları, tekrar aileleri, soru alanları.

Kural (kullanıcı, 2026-10-14):
  - Aynı yıl + aynı kurul olduğu KESİN olan kopyalar birleştirilir (silinmez; birlestirmeler.json grubu → sitede tek görünür).
  - Aynı yıl kurul + final/bütünleme → dokunulmaz (ayrı sınav, gerçek tekrar).
  - Farklı yıllarda sorulmuş → dokunulmaz (gerçek tekrar; "Diğer yıllardaki çıkmış örnekleri" bandında gösterilir).
  - Emin olunamayanlar (yıl/sınav belirsiz) → birleştirilmez, raporlanır.

Çıktılar (kuru çalıştırmada yalnız rapor): gruplar_yeni.json, aileler.json, rapor.json
`--yaz`: birlestirmeler.json + pastQuestions.json (src/data + data) güncellenir (önce yedek). Önce `systemctl --user stop meds-web`.
"""
import json, glob, collections, datetime, re, shutil, sys, unicodedata

ROOT = '/home/indu/medsor'
PQ = f'{ROOT}/meds/src/data/pastQuestions.json'
MF = f'{ROOT}/meds_database_v2/soru_birlestirme/birlestirmeler.json'
YAZ = '--yaz' in sys.argv
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
TS = datetime.datetime.now().strftime('%Y%m%d%H%M')

exec(open('05_cift_sinifla.py').read().split("out = open('cift_karar.jsonl'")[0])   # R, U, P, iliski(), benzerlik()
P = [json.loads(l) for l in open('cift_karar.jsonl')]
Q = {q['id']: q for q in json.load(open(PQ))}
SILINEN = set(json.load(open(f'{ROOT}/meds/data/deleted_past_questions.json')))
ESKI = json.load(open(MF))

# ---------------------------------------------------------------- çift kararları
REV = {}
for f in sorted(glob.glob('inceleme/sonuc/p*.json')):
    for x in json.load(open(f)):
        REV[frozenset((x['a'], x['b']))] = x
ZAYIF = {frozenset((p['a'], p['b'])) for p in json.load(open('inceleme/zayif_ayni.json'))}
ayni, olamaz, guc = set(), set(), {}
yanlis_cevap = collections.Counter()      # inceleme: çelişkide yanlış taraf
celiski_belirsiz = []
for p in P:
    k = frozenset((p['a'], p['b']))
    rv = REV.get(k)
    if rv:
        if rv['karar'] == 'AYNI':
            ayni.add(k); guc[k] = {'yuksek': 2, 'orta': 1, 'dusuk': 0}.get(rv.get('guven'), 1)
            if rv.get('cevap_celiskisi'):
                d = rv.get('dogru_olan')
                if d in ('A', 'B'): yanlis_cevap[rv['b'] if d == 'A' else rv['a']] += 1
                else: celiski_belirsiz.append((rv['a'], rv['b'], rv.get('not', '')))
        else:
            olamaz.add(k)
    elif p['benzerlik'] == 'ayni' and k not in ZAYIF:
        ayni.add(k); guc[k] = 3

def iliski_k(a, b):
    return iliski(a, b)[0]

def gecersiz(i):
    q = Q.get(i)
    return (q is None or i in SILINEN or (q.get('checkSolve') or {}).get('status') == 'kaldirildi')

# ---------------------------------------------------------------- kısıtlı kümeleme
uyesi = {}            # id -> küme no
kume = {}             # no -> set
sabit = {}            # no -> onaylı grup (asıl sabit)
_sayac = [0]
def yeni(ids, g=None):
    n = _sayac[0]; _sayac[0] += 1; kume[n] = set(ids)
    for i in ids: uyesi[i] = n
    if g: sabit[n] = g
    return n
DONUK = set()      # başka oturumun bugünkü grupları (olası üye kuralı): olduğu gibi korunur, eklenmez/ayrılmaz
def baska_oturum(g):
    return ('olasilik' in g or 'olasiUyeler' in g or str(g.get('olusturma', '')) >= '2026-10-14T03:30'
            or str(g.get('karar_zamani', '')) >= '2026-10-14T03:30') and g.get('kaynak') != 'tekrar-analizi-v1'
for g in ESKI['gruplar']:
    if g.get('durum') == 'onayli' or (baska_oturum(g) and g.get('durum') != 'ayrildi'):
        ids = [u for u in g['uyeler'] if u in Q]
        if any(u in uyesi for u in ids): continue
        n = yeni(ids, g)
        if baska_oturum(g): DONUK.add(n)
def birlestirilebilir(c1, c2):
    if c1 in DONUK or c2 in DONUK: return False
    if c1 in sabit and c2 in sabit: return False
    for x in kume[c1]:
        for y in kume[c2]:
            if frozenset((x, y)) in olamaz: return False
            if iliski_k(x, y) == 'KORU': return False
    return True
kenarlar = []
for k in ayni:
    a, b = tuple(k)
    if gecersiz(a) or gecersiz(b): continue
    karar, neden, _ = iliski(a, b)
    if karar == 'BIRLESTIR': kenarlar.append((-guc[k], a, b, neden))
kenarlar.sort()
reddedilen = collections.Counter()
for _, a, b, neden in kenarlar:
    ca = uyesi.get(a); cb = uyesi.get(b)
    if ca is None: ca = yeni([a])
    if cb is None: cb = yeni([b])
    if ca == cb: continue
    if not birlestirilebilir(ca, cb): reddedilen[neden] += 1; continue
    if cb in sabit: ca, cb = cb, ca
    for i in kume[cb]: uyesi[i] = ca
    kume[ca] |= kume.pop(cb)

# ---------------------------------------------------------------- asıl seçimi
def n_etkilesim(q):
    o = q.get('options') or []
    oy = sum(int(x.get('upvotes') or 0) for x in o if isinstance(x, dict))
    return len(q.get('comments') or []) + int(q.get('upvotes') or 0) + oy + len(q.get('reports') or [])
def puan(i, eski_asil):
    q = Q[i]; cs = q.get('checkSolve') or {}
    temiz = q.get('status') != 'quarantined' and cs.get('status') not in ('karantina', 'kaldirildi')
    return (temiz, -yanlis_cevap[i], i == eski_asil, bool(q.get('denetleyiciOnayi')), int(q.get('qualityScore') or 0),
            bool(q.get('explanation')), n_etkilesim(q), U[i]['kesinlik'] == 'kesin', -len(i))
eski_grup_of = {}
for g in ESKI['gruplar']:
    for u in g['uyeler']: eski_grup_of.setdefault(u, []).append(g)

def norm(t):
    t = unicodedata.normalize('NFKD', str(t or '').lower().replace('ı', 'i'))
    return re.sub(r'[^a-z0-9]+', ' ', ''.join(c for c in t if not unicodedata.combining(c))).strip()
def gorunen(q):
    rec = q.get('reconstruction') if isinstance(q.get('reconstruction'), dict) else {}
    o = rec.get('options') or q.get('options') or []
    return norm(rec.get('stem') or q.get('stem')), sorted(norm(x.get('text') if isinstance(x, dict) else x) for x in o)
SINAV_AD = {'F': 'Final', 'B': 'Bütünleme', 'F?': 'Final (?)', 'D2K5': 'Dönem 2 Kurul 5'}
def etiket(u):
    s = u['sinav']
    ad = SINAV_AD.get(s) or (f'Kurul {s[1:]}' if s and s.startswith('K') else s)
    return f"{u['yil'] or 'Yılı belirsiz'} {ad or ''}".strip()

gruplar = []
for n, ids in kume.items():
    ids = [i for i in ids if not gecersiz(i)]
    if len(ids) < 2: continue
    g0 = sabit.get(n)
    if n in DONUK:
        gruplar.append(dict(g0)); continue
    eskiler = [g for i in ids for g in eski_grup_of.get(i, []) if g.get('durum') == 'otomatik']
    eski_asil = g0['asil'] if g0 else (collections.Counter(g['asil'] for g in eskiler).most_common(1)[0][0] if eskiler else None)
    asil = g0['asil'] if g0 and g0['asil'] in ids else max(ids, key=lambda i: puan(i, eski_asil))
    uyeler = [asil] + sorted((i for i in ids if i != asil), key=lambda i: puan(i, eski_asil), reverse=True)
    nedenler = collections.Counter()
    for i in range(len(uyeler)):
        for j in range(i + 1, len(uyeler)):
            if frozenset((uyeler[i], uyeler[j])) in ayni: nedenler[iliski(uyeler[i], uyeler[j])[1]] += 1
    bz = [p['stem'] / 100 for p in P if p['a'] in ids and p['b'] in ids]
    birebir = all(gorunen(Q[asil]) == gorunen(Q[u]) for u in uyeler[1:])
    cel = sorted({f'{a}|{b}' for a, b, _ in celiski_belirsiz if a in ids and b in ids})
    yanlis = sorted(i for i in ids if yanlis_cevap[i])
    birimler = collections.Counter(etiket(U[i]) for i in ids)
    g = {
        'id': g0['id'] if g0 else None, 'asil': asil, 'uyeler': uyeler, 'birebir_ayni': birebir,
        'benzerlik': round(min(bz), 3) if bz else 1.0, 'durum': g0['durum'] if g0 else 'otomatik',
        'olusturma': g0.get('olusturma') if g0 else NOW, 'sebep': (nedenler.most_common(1)[0][0] if nedenler else 'onayli_grup'),
        'sinav': birimler.most_common(1)[0][0], 'kaynak': 'tekrar-analizi-v1',
        'not': {'ayni_sinav_ayni_cikti': 'Aynı sınavın aynı öğrenci çıktısında/bölümünde birden çok kez çıkarılmış.',
                'ayni_yil_ayni_kurul': 'Aynı yıl, aynı kurul sınavının farklı öğrenci çıktıları/dökümlerinden gelen kopya.',
                'ayni_belge_tek_sinav': 'Aynı sınav belgesinin farklı dökümleri (txt/pdf/OCR) ya da yinelenen çıkarım.',
                'ayni_belge_ayni_sira': 'Aynı belgenin farklı dökümleri, aynı soru sırası.'}.get(nedenler.most_common(1)[0][0] if nedenler else '', 'Önceden onaylanmış grup.'),
    }
    if g0:
        for k, v in g0.items():
            if k not in ('uyeler', 'asil'): g.setdefault(k, v)
            if k in ('karar_zamani', 'not'): g[k] = v
        if set(uyeler) != set(g0['uyeler']): g['ek_uyeler'] = sorted(set(uyeler) - set(g0['uyeler']))
    if cel: g['cevap_celiskisi'] = cel
    if yanlis: g['yanlis_cevapli_kopyalar'] = yanlis
    gruplar.append(g)

# eski otomatik grupların kimliğini koru (asıl aynı kümede ise), diğerleri "ayrildi"
kullanilan = set(g['id'] for g in gruplar if g['id'])
for g in gruplar:
    if g['id']: continue
    aday = [e for i in g['uyeler'] for e in eski_grup_of.get(i, []) if e.get('durum') == 'otomatik' and e['id'] not in kullanilan and e['asil'] in g['uyeler']]
    if aday:
        e = max(aday, key=lambda e: len(set(e['uyeler']) & set(g['uyeler'])))
        g['id'] = e['id']; g['olusturma'] = e.get('olusturma', NOW); kullanilan.add(e['id'])
        g['onceki_uyeler'] = e['uyeler'] if set(e['uyeler']) != set(g['uyeler']) else None
        if g['onceki_uyeler'] is None: g.pop('onceki_uyeler')
    else:
        g['id'] = 'g-t-' + g['asil']
ayrilan = []
for e in ESKI['gruplar']:
    if e['id'] in kullanilan or e.get('durum') == 'onayli': continue
    if e.get('durum') == 'ayrildi': ayrilan.append(e); continue
    e2 = dict(e); e2['durum'] = 'ayrildi'; e2['karar_zamani'] = NOW
    rel = collections.Counter(iliski(a, b)[1] for a in e['uyeler'] for b in e['uyeler'] if a < b and a in R and b in R)
    e2['ayrilma_nedeni'] = ('tekrar-analizi-v1: kurala aykırı ya da kanıtsız birleştirme (' +
                           ', '.join(f'{k}:{v}' for k, v in rel.most_common()) + '); geçerli üyeler yeni gruplarda')
    ayrilan.append(e2)

# ---------------------------------------------------------------- tekrar aileleri (farklı sınavlar)
gizli = {u: g['asil'] for g in gruplar if g['durum'] != 'ayrildi' for u in g['uyeler'] if u != g['asil']}
temsil = lambda i: gizli.get(i, i)
par = {}
def f(x):
    while par.get(x, x) != x: x = par[x]
    return x
tekrar_kenar = collections.defaultdict(set); belirsiz_kopya = collections.defaultdict(set)
for k in ayni:
    a, b = tuple(k)
    if gecersiz(a) or gecersiz(b): continue
    ta, tb = temsil(a), temsil(b)
    if ta == tb: continue
    karar, neden, _ = iliski(a, b)
    if karar == 'KORU':
        par[f(ta)] = f(tb); tekrar_kenar[ta].add((tb, neden)); tekrar_kenar[tb].add((ta, neden))
    elif karar == 'BEKLET':
        belirsiz_kopya[ta].add(tb); belirsiz_kopya[tb].add(ta)
aile = collections.defaultdict(set)
for x in list(par):
    aile[f(x)].add(x)
grup_of = {g['asil']: g for g in gruplar}
def olay(i):
    q = Q[i]; u = U[i]
    lab = etiket(u) + (f" · Soru {q['questionNumber']}" if q.get('questionNumber') else '')
    return {'id': i, 'examYear': u['yil'] or q.get('examYear'), 'label': lab, 'questionNumber': q.get('questionNumber'), 'sinav': u['sinav']}
aileler = []
alanlar = {}         # id -> yeni tekrar alanları
for kok, uyeler in aile.items():
    uy = sorted(uyeler)
    # aynı sınav birimindeki (yıl+sınav) temsilciler tek olay sayılmaz: ayrı soru ama aynı sınavda — nadir, raporla
    birim = collections.defaultdict(list)
    for i in uy: birim[(U[i]['yil'], U[i]['sinav'])].append(i)
    if len(birim) < 2: continue
    aileler.append({'aile': 'a-' + uy[0], 'uyeler': uy, 'sinavlar': sorted(etiket(U[v[0]]) for v in birim.values())})
    for i in uy:
        digerleri = [olay(j) for j in uy if j != i and (U[j]['yil'], U[j]['sinav']) != (U[i]['yil'], U[i]['sinav']) and U[j]['yil']]
        if not digerleri: continue
        hepsi = [olay(i)] + digerleri
        alanlar[i] = {'similarPastQuestions': digerleri, 'examOccurrences': hepsi,
                      'appearanceLabels': [o['label'] for o in hepsi], 'appearanceCount': len({(o['examYear'], o['sinav']) for o in hepsi}),
                      'sebepler': sorted({n for _, n in tekrar_kenar.get(i, [])})}

# ---------------------------------------------------------------- rapor
ozet = {
    'kopya_cifti_aday': len(P), 'ayni_soru_cifti': len(ayni), 'inceleme_ile_ayni_degil': len(olamaz),
    'grup': len(gruplar), 'gizlenen_kopya': sum(len(g['uyeler']) - 1 for g in gruplar if g['durum'] != 'ayrildi'),
    'grup_sebep': collections.Counter(g.get('sebep', 'baska_oturum_grubu') for g in gruplar), 'grup_sinav': collections.Counter(g.get('sinav', '?') for g in gruplar).most_common(30),
    'onayli_korunan': sum(1 for g in gruplar if g['durum'] == 'onayli'), 'eski_otomatik_yeniden_kullanilan': sum(1 for g in gruplar if g['id'] in kullanilan and g['durum'] == 'otomatik'),
    'eski_otomatik_ayrilan': sum(1 for e in ayrilan if e.get('ayrilma_nedeni')), 'kisit_ile_reddedilen_kenar': reddedilen,
    'tekrar_ailesi': len(aileler), 'tekrar_isaretli_soru': len(alanlar),
    'tekrar_sebep': collections.Counter(n for v in alanlar.values() for n in v['sebepler']),
    'belirsiz_kopyali_soru': len(belirsiz_kopya), 'cevap_celiskili_grup': sum(1 for g in gruplar if g.get('cevap_celiskisi') or g.get('yanlis_cevapli_kopyalar')),
}
print(json.dumps(ozet, ensure_ascii=False, indent=1, default=str))
json.dump(gruplar, open('gruplar_yeni.json', 'w'), ensure_ascii=False, indent=1)
json.dump(aileler, open('aileler.json', 'w'), ensure_ascii=False, indent=1)
json.dump({'ozet': ozet, 'belirsiz_kopya': {k: sorted(v) for k, v in belirsiz_kopya.items()}, 'celiski_belirsiz': celiski_belirsiz},
          open('rapor.json', 'w'), ensure_ascii=False, indent=1, default=str)
json.dump(alanlar, open('tekrar_alanlari.json', 'w'), ensure_ascii=False)
json.dump(ayrilan, open('ayrilan_gruplar.json', 'w'), ensure_ascii=False, indent=1)
if not YAZ:
    print('kuru çalıştırma (yazmak için --yaz)'); sys.exit(0)
