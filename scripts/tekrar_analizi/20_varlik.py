"""Terim · hastalık · tedavi · semptom · bulgu ilişki grafiği (yerel, LLM'siz, tekrarlanabilir).

Düğümler: diseases.json profilleri (470) + profillerdeki tipli varlıklar + disease_entities.json + medical_glossary.json terimleri.
Kenarlar:
  profil  — hastalık profilinin bölüm + varlık tipinden (web kaynaklı, `refs`): semptomu, bulgusu, tedavisi, tani_yontemi, etkeni…
  soru    — görünen çıkmış sorularda: kökte hastalık + kök ipucu (tedavi/belirti/bulgu/tanı/etken) + doğru şıktaki varlık
            (olumsuz kökte "değildir/yer almaz": çeldiriciler ilişkili, doğru şık değil); kanıt = soru kimliği
  birlikte — aynı soruda (kök + doğru şık) birlikte geçen varlıklar (≥2 soru)
Ayrıca varlık ↔ konu (soru müfredatından) ve varlık ↔ ders özeti (özet metninde geçiş).
Çıktı: meds_database_v2/iliski/{varliklar.json, varlik_iliskileri.json, soru_varlik.json}
"""
import json, re, unicodedata, collections, math, os

ROOT = '/home/indu/medsor'
D = f'{ROOT}/meds/src/data'
OUT = f'{ROOT}/meds_database_v2/iliski'
os.makedirs(OUT, exist_ok=True)
FOLD = str.maketrans("çğıöşüâîû", "cgiosuaiu")
def fold(s):
    s = str(s or '').replace('İ', 'i').replace('I', 'ı').lower().translate(FOLD)
    s = unicodedata.normalize('NFKD', s); s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()
def toks(s): return fold(s).split()

# ---------------------------------------------------------------- düğümler
GRUP = {'hastalik': 'hastalik', 'patolojik_surec': 'hastalik', 'ilac': 'tedavi', 'tedavi': 'tedavi', 'belirti': 'semptom', 'bulgu': 'bulgu',
        'test': 'tani', 'laboratuvar': 'tani', 'goruntuleme': 'tani', 'tani': 'tani', 'patojen': 'etken', 'risk_faktoru': 'risk_faktoru',
        'gen_protein': 'gen_protein', 'genetik': 'gen_protein', 'protein': 'gen_protein', 'molekul_hucre': 'gen_protein',
        'histopatoloji': 'histopatoloji', 'patoloji': 'histopatoloji', 'mekanizma': 'mekanizma', 'anatomi': 'anatomi', 'hucre': 'anatomi',
        'fizyoloji': 'terim', 'terim': 'terim', 'kavram': 'terim', 'yontem': 'tani', 'halk-sagligi': 'terim', 'epidemiyoloji': 'terim'}
N = {}            # anahtar (fold ad) -> düğüm
alias_of = {}     # fold ad/eşad -> anahtar
ACR = {}          # büyük harf kısaltma (özgün yazım) -> anahtar; büyük/küçük harfe duyarlı eşlenir
ACR_RE = re.compile(r'^[A-ZÇĞİÖŞÜ0-9][A-ZÇĞİÖŞÜ0-9\-]{1,7}$')
def paren(ad):
    out = []
    for p in re.findall(r'\(([^)]{2,25})\)', ad or ''):
        p = p.strip()
        if ACR_RE.match(p) and sum(c.isalpha() for c in p) >= 2: out.append(p)
    return out
def temiz(ad): return re.sub(r'\s*\([^)]*\)\s*', ' ', ad or '').strip()
def dugum(ad, tur, kaynak, esadlar=(), **ek):
    k = fold(ad)
    if not k or len(k) < 2: return None
    key = alias_of.get(k, k)
    n = N.get(key)
    if not n:
        n = N[key] = {'id': key.replace(' ', '-'), 'ad': ad.strip(), 'turler': collections.Counter(), 'esAdlar': set(), 'kaynaklar': set()}
        alias_of[k] = key
    n['turler'][tur] += 1; n['kaynaklar'].add(kaynak)
    for e in list(esadlar) + [temiz(ad)] + paren(ad):
        e = (e or '').strip()
        if not e: continue
        if ACR_RE.match(e):
            ACR.setdefault(e, key); n['esAdlar'].add(e); continue
        fe = fold(e)
        if fe and fe != key and len(fe) >= 3:
            n['esAdlar'].add(e); alias_of.setdefault(fe, key)
    if len(temiz(ad)) < len(n['ad']) and temiz(ad): n['ad'] = n['ad']   # görünen ad: ilk (profil) adı korunur
    for a, b in ek.items(): n.setdefault(a, b)
    return key
DIS = json.load(open(f'{D}/diseases.json'))
for p in DIS:     # önce profiller: eş adlar kanonik düğüme bağlanır
    dugum(p['name'], {'hastalik': 'hastalik', 'patolojik_surec': 'hastalik'}.get(p.get('kind'), p.get('kind') or 'hastalik'), 'hastalik_profili',
          [p.get('latinName') or ''] + list(p.get('aliases') or []) + list(p.get('altNames') or []), profil=p['id'], kategori=p.get('category'))
for e in json.load(open(f'{D}/disease_entities.json')):
    dugum(e['name'], 'hastalik', 'hastalik_varligi', [e.get('latinName') or ''])
GL = json.load(open(f'{D}/medical_glossary.json'))
for k, v in GL.items():
    dugum(v.get('term') or k, v.get('category') or 'terim', 'sozluk', [], sozluk=True)
SEC_REL = {'symptoms': {'belirti': 'semptomu', 'bulgu': 'bulgusu'}, 'pathognomonic': {'*': 'patognomonik_bulgusu'},
           'treatment': {'ilac': 'tedavisi', 'tedavi': 'tedavisi'}, 'diagnosis': {'test': 'tani_yontemi', 'laboratuvar': 'tani_yontemi', 'goruntuleme': 'tani_yontemi', 'hastalik': 'ayirici_tanisi'},
           'imaging': {'goruntuleme': 'goruntuleme_bulgusu'}, 'etiology': {'patojen': 'etkeni', 'risk_faktoru': 'risk_faktoru', 'gen_protein': 'genetik_nedeni', 'hastalik': 'zemin_hastaligi'},
           'complications': {'hastalik': 'komplikasyonu', 'bulgu': 'komplikasyonu'}, 'pathology': {'histopatoloji': 'histopatolojisi'},
           'physiology': {'mekanizma': 'mekanizmasi'}}
E = collections.defaultdict(lambda: {'agirlik': 0, 'kanit': []})
def kenar(a, b, iliski, kanit, w=1):
    if not a or not b or a == b: return
    e = E[(a, b, iliski)]; e['agirlik'] += w
    if len(e['kanit']) < 6: e['kanit'].append(kanit)
for p in DIS:
    src = alias_of.get(fold(p['name']))
    items = [('hallmarks', it) for it in p.get('hallmarks') or []] + [(sec, it) for sec, L in (p.get('sections') or {}).items() for it in (L if isinstance(L, list) else [])]
    for sec, it in items:
        for en in it.get('entities') or []:
            t = en.get('type') or 'terim'
            dst = dugum(en['name'], t, 'hastalik_profili')
            rmap = SEC_REL.get(sec, {})
            rel = rmap.get(t) or rmap.get('*') or ('ayirt_edici_ozelligi' if sec == 'hallmarks' else
                  {'belirti': 'semptomu', 'bulgu': 'bulgusu', 'ilac': 'ilgili_ilac', 'tedavi': 'tedavisi', 'patojen': 'etkeni',
                   'gen_protein': 'gen_protein', 'histopatoloji': 'histopatolojisi', 'risk_faktoru': 'risk_faktoru'}.get(t, 'iliskili'))
            kenar(src, dst, rel, {'tur': 'profil', 'profil': p['id'], 'bolum': sec, 'metin': re.sub(r'==', '', it.get('text', ''))[:180], 'refs': len(it.get('refs') or [])})

# ---------------------------------------------------------------- metin eşleyici (ek toleranslı)
GENEL = set('hasta hastalik tedavi tani kan idrar doku hucre organ sendrom enfeksiyon tumor kanser agri ates yas kadin erkek cocuk '
            'risk faktor bulgu belirti test ilac doz etki yan etki neden tip evre derece akut kronik primer sekonder normal '
            'patoloji patogenez kontrol gelisme oyku kitle dogum tani tedavisi semptom morfoloji etiyoloji klinik lezyon '
            'fizik muayene laboratuvar goruntuleme alt ust sol sag orta'.split())
cands = collections.defaultdict(list)    # ilk token -> [(token tuple, anahtar)]
for fa, key in alias_of.items():
    t = tuple(fa.split())
    if len(t) == 1 and (len(t[0]) < 3 or t[0] in GENEL or t[0].isdigit()): continue
    cands[t[0]].append((t, key))
def eslesir(w, p, son):
    if w == p: return True
    return son and len(p) >= 4 and w.startswith(p) and len(w) - len(p) <= 5
ACR_PAT = re.compile(r'(?<![A-Za-zÇĞİÖŞÜçğıöşü0-9])(' + '|'.join(sorted(map(re.escape, ACR), key=len, reverse=True)) + r')(?![A-Za-zÇĞİÖŞÜçğıöşü0-9])') if ACR else None
def bul(metin):
    metin = str(metin or '')
    out = set()
    harf = [c for c in metin if c.isalpha()]
    if ACR_PAT and harf and sum(c.isupper() for c in harf) / len(harf) < 0.5:
        for m in ACR_PAT.finditer(metin): out.add(ACR[m.group(1)])
    w = toks(metin); i = 0
    while i < len(w):
        best = None
        heads = {w[i]} | {w[i][:L] for L in range(max(3, len(w[i]) - 5), len(w[i]))}
        for h in heads:
            for t, key in cands.get(h, ()):
                n = len(t)
                if i + n > len(w): continue
                if all(eslesir(w[i + j], t[j], j == n - 1) for j in range(n)):
                    if not best or n > best[0]: best = (n, key)
        if best: out.add(best[1]); i += best[0]
        else: i += 1
    return out

# ---------------------------------------------------------------- sorular
PQ = json.load(open(f'{D}/pastQuestions.json'))
MG = json.load(open(f'{ROOT}/meds_database_v2/soru_birlestirme/birlestirmeler.json'))['gruplar']
gizli = {u for g in MG if g.get('durum') != 'ayrildi' for u in g['uyeler'] if u != g['asil']}
OLUMSUZ = re.compile(r'\b(degildir|degil|yer almaz|almaz|beklenmez|gorulmez|olmaz|yanlistir|bulunmaz|kullanilmaz|icermez|yoktur|gozlenmez)\b')
IPUCU = [('tedavisi', r'tedavi|ilac|kullanil|verilir|uygulan|endike'), ('semptomu', r'semptom|belirti|yakinma|sikayet'),
         ('bulgusu', r'bulgu|muayene|gorunum|izlenir|saptan'), ('tani_yontemi', r'tani|test|tetkik|laboratuvar|inceleme|goruntuleme'),
         ('etkeni', r'etken|etiyoloj|neden ol|sebep ol|mikroorganizma'), ('komplikasyonu', r'komplikasyon'),
         ('histopatolojisi', r'histopatoloj|mikroskop|morfoloj|boya')]
SV = {}; konu_of = collections.defaultdict(collections.Counter); soru_say = collections.Counter(); bir = collections.Counter()
def turu(k):
    n = N[k]; return GRUP.get(n['turler'].most_common(1)[0][0], 'terim')
for q in PQ:
    rec = q.get('reconstruction') if isinstance(q.get('reconstruction'), dict) else {}
    stem = rec.get('stem') or q.get('stem') or ''
    opts = rec.get('options') or q.get('options') or []
    ans = str(rec.get('correctAnswer') or q.get('correctAnswer') or '').upper()
    dogru = [o.get('text', '') for o in opts if isinstance(o, dict) and str(o.get('key', '')).upper() == ans]
    celd = [o.get('text', '') for o in opts if isinstance(o, dict) and str(o.get('key', '')).upper() != ans]
    k_ = bul(stem); d_ = bul(' '.join(dogru)); c_ = bul(' '.join(celd)); a_ = bul(str(rec.get('explanation') or q.get('explanation') or '')[:3000])
    SV[q['id']] = {'kok': sorted(k_), 'dogru_sik': sorted(d_), 'celdirici': sorted(c_ - d_), 'aciklama': sorted(a_ - k_ - d_ - c_)[:40]}
    if q['id'] in gizli: continue
    m = (q.get('checkSolve') or {}).get('mufredat') or {}
    konu = (m.get('kurul'), m.get('ders'), m.get('konu')) if m.get('konu') else None
    for k in k_ | d_:
        soru_say[k] += 1
        if konu: konu_of[k][konu] += 1
    fs = fold(stem); olumsuz = bool(OLUMSUZ.search(fs))
    hast = [k for k in k_ if turu(k) == 'hastalik' and fold(N[k]['ad']) not in GENEL]
    if len(hast) != 1: hast = []
    for rel, rx in IPUCU:
        if not re.search(rx, fs): continue
        hedef = c_ - d_ if olumsuz else d_
        for h in hast:
            for t in hedef:
                if t in k_: continue
                tt = turu(t)
                if (rel == 'tedavisi' and tt == 'tedavi') or (rel == 'semptomu' and tt in ('semptom', 'bulgu')) or (rel == 'bulgusu' and tt in ('bulgu', 'semptom', 'histopatoloji', 'tani')) \
                   or (rel == 'tani_yontemi' and tt == 'tani') or (rel == 'etkeni' and tt in ('etken', 'risk_faktoru', 'gen_protein')) or (rel == 'komplikasyonu' and tt == 'hastalik') \
                   or (rel == 'histopatolojisi' and tt == 'histopatoloji'):
                    kenar(h, t, rel, {'tur': 'soru', 'id': q['id'], 'olumsuz_kok': olumsuz})
        break
    L = sorted(k_ | d_)
    for i in range(len(L)):
        for j in range(i + 1, len(L)): bir[(L[i], L[j])] += 1
NQ = sum(1 for q in PQ if q['id'] not in gizli)
genel = {k for k, c in soru_say.items() if c / NQ > 0.012} | {k for k in N if k in GENEL}
for (a, b), c in bir.items():
    if c >= 2 and a not in genel and b not in genel:
        pmi = math.log((c * NQ) / (soru_say[a] * soru_say[b]))
        if pmi > 1.0: kenar(a, b, 'birlikte_sorulur', {'tur': 'birlikte', 'soru_sayisi': c, 'pmi': round(pmi, 2)}, w=c)

# ---------------------------------------------------------------- özetler
ozet_of = collections.defaultdict(collections.Counter)
for o in json.load(open(f'{D}/lectureSummariesCatalog.json')):
    for line in o['content'].split('\n'):
        for k in bul(line): ozet_of[k][o['id']] += 1

# ---------------------------------------------------------------- yaz
kullanilan = set(a for a, _, _ in E) | set(b for _, b, _ in E) | set(soru_say) | set(ozet_of)
V = []
for key in kullanilan:
    n = N[key]
    V.append({'id': n['id'], 'ad': n['ad'], 'tur': turu(key), 'altTurler': dict(n['turler']), 'esAdlar': sorted(n['esAdlar'])[:12],
              'kaynaklar': sorted(n['kaynaklar']), 'profil': n.get('profil'), 'sozluk': bool(n.get('sozluk')),
              'soruSayisi': soru_say.get(key, 0), 'genel': key in genel,
              'konular': [{'kurul': k[0], 'ders': k[1], 'konu': k[2], 'soru': c} for k, c in konu_of[key].most_common(5)],
              'ozetler': [{'id': i, 'gecis': c} for i, c in ozet_of[key].most_common(5)]})
idmap = {k: N[k]['id'] for k in N}
K = [{'kaynak': idmap[a], 'hedef': idmap[b], 'iliski': r, 'agirlik': e['agirlik'], 'kanit': e['kanit'],
      'kanit_turu': sorted({x['tur'] for x in e['kanit']})} for (a, b, r), e in E.items()]
SVo = {i: {r: [idmap[k] for k in v] for r, v in d.items() if v} for i, d in SV.items()}
json.dump(sorted(V, key=lambda x: (-x['soruSayisi'], x['ad'])), open(f'{OUT}/varliklar.json', 'w'), ensure_ascii=False, indent=0)
json.dump(K, open(f'{OUT}/varlik_iliskileri.json', 'w'), ensure_ascii=False, indent=0)
json.dump(SVo, open(f'{OUT}/soru_varlik.json', 'w'), ensure_ascii=False)
c = collections.Counter(v['tur'] for v in V)
print('düğüm', len(V), dict(c.most_common()))
print('kenar', len(K), dict(collections.Counter(k['iliski'] for k in K).most_common(25)))
print('kanıt türü', dict(collections.Counter('+'.join(k['kanit_turu']) for k in K)))
print('varlıklı soru', sum(1 for v in SVo.values() if v), '/', len(SVo), 'genel varlık', len(genel))
