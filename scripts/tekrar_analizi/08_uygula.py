"""Tekrar analizi sonuçlarını uygular (kuru çalıştırma varsayılan; yazmak için --yaz).

1) birlestirmeler.json: yeni/güncellenen gruplar + kurala aykırı eski otomatik gruplar "ayrildi" (silinmez).
2) pastQuestions.json (src/data + data):
   - sinavKimligi {yil, sinav, etiket, kesinlik, belge, gerekce} her soruya
   - examYear yalnız KESİN sınav kimliğiyle çelişiyorsa düzeltilir (eski değer examYearOnceki)
   - sourceNote kesin kimlikle çelişiyorsa standart nota çekilir (eski değer sourceNoteOnceki)
   - gerçek tekrarlar (farklı yıl / kurul+final): similarPastQuestions, examOccurrences, appearanceLabels, appearanceCount,
     'tekrarlayan_soru' etiketi; tekrar olmayanlardan eski (yanlış: aynı sınavın kitapçıklarını "başka yıl" sayan) alanlar kaldırılır
   - tekrarAnalizi {surum, grup, rol, sebep, belirsizKopyalar}
3) kazanım kataloğu (src/data/kazanimlar/k1-6.json) cikmisSorular: gizli kopyalar hariç yeniden kurulur.
Önce: systemctl --user stop meds-web
"""
import json, collections, datetime, re, shutil, sys, os

ROOT = '/home/indu/medsor'
PQ = f'{ROOT}/meds/src/data/pastQuestions.json'
MF = f'{ROOT}/meds_database_v2/soru_birlestirme/birlestirmeler.json'
YAZ = '--yaz' in sys.argv
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
TS = datetime.datetime.now().strftime('%Y%m%d%H%M')
SURUM = 'tekrar-analizi-v1'

G = json.load(open('gruplar_yeni.json'))
AYR = json.load(open('ayrilan_gruplar.json'))
AL = json.load(open('tekrar_alanlari.json'))
U = json.load(open('birim.json'))
RAP = json.load(open('rapor.json'))
mt0 = os.path.getmtime(PQ)
D = json.load(open(PQ)); Q = {q['id']: q for q in D}
ESKI = json.load(open(MF))

SINAV_AD = {'F': 'Final', 'B': 'Bütünleme', 'F?': 'Final (?)', 'D2K5': 'Dönem 2 Kurul 5'}
def etiket(u):
    s = u['sinav']
    ad = SINAV_AD.get(s) or (f'Kurul {s[1:]}' if s and s.startswith('K') else s)
    return f"{u['yil'] or 'Yılı belirsiz'} {ad or ''}".strip()

# ---------------------------------------------------------------- 1) birleştirme dosyası
yeni_ids = {g['id'] for g in G}
cikis = list(G)
for e in AYR:
    if e['id'] not in yeni_ids: cikis.append(e)
_cikan = {g['id'] for g in cikis}
for e in ESKI['gruplar']:
    if e['id'] not in _cikan: cikis.append(e); print('eski grup aynen korundu:', e['id'], e.get('durum'))
eski_ids = {g['id'] for g in ESKI['gruplar']}
kayip = eski_ids - {g['id'] for g in cikis}
assert not kayip, f'eski grup kayboluyor: {sorted(kayip)[:5]}'
uye_say = collections.Counter(u for g in cikis if g.get('durum') != 'ayrildi' for u in g['uyeler'])
assert all(v == 1 for v in uye_say.values()), 'bir soru iki etkin grupta'
gizli = {u: g for g in cikis if g.get('durum') != 'ayrildi' for u in g['uyeler'] if u != g['asil']}
asil_of = {g['asil']: g for g in cikis if g.get('durum') != 'ayrildi'}

# ---------------------------------------------------------------- 2) soru alanları
st = collections.Counter(); degisen = set(); gorunur = set()
GORUNUR = {'examYear', 'sourceNote', 'similarPastQuestions', 'examOccurrences', 'appearanceLabels', 'appearanceCount', 'tags'}
def set_(q, k, v):
    if json.dumps(q.get(k), sort_keys=True, ensure_ascii=False) != json.dumps(v, sort_keys=True, ensure_ascii=False):
        q[k] = v; degisen.add(q['id'])
        if k in GORUNUR: gorunur.add(q['id'])
        return True
    return False
def pop_(q, k):
    if k in q:
        q.pop(k); degisen.add(q['id'])
        if k in GORUNUR: gorunur.add(q['id'])
        return True
    return False
YIL_RE = re.compile(r'(20\d\d)-(20\d\d)')
temsil = lambda i: (gizli[i]['asil'] if i in gizli else i)
belirsiz = RAP['belirsiz_kopya']
for i, q in Q.items():
    u = U.get(i)
    if not u: st['birimsiz'] += 1; continue
    sk = {'yil': u['yil'], 'sinav': u['sinav'], 'etiket': etiket(u), 'kesinlik': u['kesinlik'], 'belge': u['belge'], 'gerekce': u['gerekce'], 'surum': SURUM}
    set_(q, 'sinavKimligi', sk)
    if u['kesinlik'] == 'kesin' and u['yil']:
        ey = str(q.get('examYear') or '')
        if ey != u['yil']:
            if 'examYearOnceki' not in q: q['examYearOnceki'] = q.get('examYear')
            set_(q, 'examYear', u['yil']); st['examYear_duzeltildi'] += 1
        sn = str(q.get('sourceNote') or '')
        m = YIL_RE.search(sn); km = re.search(r'Kurul (\d)', sn)
        celisik = (m and m.group(0) != u['yil']) or (km and u['sinav'] and u['sinav'].startswith('K') and km.group(1) != u['sinav'][1:]) \
                  or (u['sinav'] in ('F', 'B') and km and 'Final' not in sn and 'Büt' not in sn)
        if celisik or not sn:
            yeni = f"{u['yil']} Dönem 3 {etiket(u).split(' ', 1)[1]} Sınavı"
            if u['belge'].startswith('combinepdf:') or 'karne' in u['gerekce']: yeni += ' (sinav.karabuk.edu.tr öğrenci çıktısı)'
            if 'sourceNoteOnceki' not in q: q['sourceNoteOnceki'] = q.get('sourceNote')
            set_(q, 'sourceNote', yeni); st['sourceNote_duzeltildi'] += 1
    # tekrar alanları: temsilcinin (görünen asıl) değerleri gruptaki tüm kopyalara
    t = temsil(i)
    al = AL.get(t)
    tags = list(q.get('tags') or [])
    # başka oturumun "olası aynı soru" bağlantıları (olasi/benzerlik alanlı) korunur
    olasi_eski = [x for x in (q.get('similarPastQuestions') or []) if isinstance(x, dict) and (x.get('olasi') or x.get('benzerlik') is not None)]
    if olasi_eski:
        al = dict(al) if al else {'similarPastQuestions': [], 'sebepler': []}
        ids_ = {x['id'] for x in al['similarPastQuestions']}
        al['similarPastQuestions'] = al['similarPastQuestions'] + [x for x in olasi_eski if x['id'] not in ids_]
        own = {'id': i, 'examYear': u['yil'] or q.get('examYear'), 'label': etiket(u) + (f" · Soru {q['questionNumber']}" if q.get('questionNumber') else ''), 'questionNumber': q.get('questionNumber')}
        al['examOccurrences'] = [own] + al['similarPastQuestions']
        al['appearanceLabels'] = [o.get('label') or str(o.get('examYear')) for o in al['examOccurrences']]
        al['appearanceCount'] = len(al['examOccurrences'])
        st['olasi_baglanti_korundu'] += 1
    if al:
        set_(q, 'similarPastQuestions', al['similarPastQuestions']); set_(q, 'examOccurrences', al['examOccurrences'])
        set_(q, 'appearanceLabels', al['appearanceLabels']); set_(q, 'appearanceCount', al['appearanceCount'])
        if 'tekrarlayan_soru' not in tags: tags.append('tekrarlayan_soru')
        st['tekrar_isaretli'] += 1
    else:
        eski = bool(q.get('similarPastQuestions') or q.get('examOccurrences') or (q.get('appearanceCount') or 1) > 1 or 'tekrarlayan_soru' in tags)
        for k in ('similarPastQuestions', 'examOccurrences', 'appearanceLabels'): pop_(q, k)
        if (q.get('appearanceCount') or 1) > 1: set_(q, 'appearanceCount', 1)
        if 'tekrarlayan_soru' in tags: tags.remove('tekrarlayan_soru')
        if eski: st['yanlis_tekrar_kaldirildi'] += 1
    if tags != list(q.get('tags') or []): set_(q, 'tags', tags)
    ta = {'surum': SURUM}
    g = gizli.get(i) or asil_of.get(i)
    if g:
        ta.update({'grup': g['id'], 'rol': 'kopya' if i in gizli else 'asil', 'sebep': g.get('sebep'), 'sinav': g.get('sinav')})
    if al and al.get('sebepler'): ta['tekrar'] = al['sebepler']
    if belirsiz.get(t): ta['belirsizKopyalar'] = belirsiz[t][:12]
    if len(ta) > 1: set_(q, 'tekrarAnalizi', ta)
    elif 'tekrarAnalizi' in q: pop_(q, 'tekrarAnalizi')
for i in gorunur: Q[i]['updatedAt'] = NOW
st['degisen_soru'] = len(degisen); st['gorunur_degisen'] = len(gorunur)

# ---------------------------------------------------------------- 3) kazanım kataloğu
def fq(q): return {"id": q.get("id"), "questionNumber": q.get("questionNumber"), "stem": q.get("stem", ""), "correctAnswer": q.get("correctAnswer", ""),
                   "options": [{"key": o.get("key", o.get("label", "")), "text": o.get("text", "")} for o in q.get("options", [])],
                   "year": q.get("year") or q.get("examYear") or "", "discipline": q.get("discipline", ""), "topic": q.get("topic", ""), "explanation": q.get("explanation", "")}
byk = collections.defaultdict(list)
for q in D:
    cs = q.get('checkSolve') or {}
    if cs.get('status') != 'onayli' or q['id'] in gizli: continue
    z = (cs.get('mufredat') or {}).get('kazanimId')
    if z: byk[z].append(q)
kat = {}; tot = 0
for k in range(1, 7):
    fp = f'{ROOT}/meds/src/data/kazanimlar/k{k}.json'; c = json.load(open(fp))
    for de in c['dersler']:
        for ko in de['konular']:
            for z in ko['kazanimlar']:
                z['cikmisSorular'] = [fq(q) for q in sorted(byk.get(z['id'], []), key=lambda q: (str(q.get('examYear')), q.get('questionNumber') or 0))]
                tot += len(z['cikmisSorular'])
    kat[fp] = c
st['katalog_cikmis'] = tot
print(dict(st))
print('etkin grup', sum(1 for g in cikis if g.get('durum') != 'ayrildi'), 'gizli kopya', len(gizli), 'toplam grup kaydı', len(cikis))
if not YAZ:
    print('kuru çalıştırma (yazmak için --yaz)'); sys.exit(0)
assert os.path.getmtime(PQ) == mt0, 'pastQuestions.json okuma sonrası değişti — yeniden çalıştır'
Y = f'{ROOT}/yedek/tekrar_analizi_{TS}'; os.makedirs(Y, exist_ok=True)
shutil.copy(PQ, f'{Y}/pastQuestions.json'); shutil.copy(MF, f'{Y}/birlestirmeler.json')
for fp in kat: shutil.copy(fp, f'{Y}/' + os.path.basename(fp))
json.dump({'guncelleme': NOW, 'gruplar': cikis}, open(MF + '.tmp', 'w'), ensure_ascii=False, indent=1); os.replace(MF + '.tmp', MF)
json.dump(D, open(PQ + '.tmp', 'w'), ensure_ascii=False); os.replace(PQ + '.tmp', PQ)
shutil.copy(PQ, f'{ROOT}/meds/data/pastQuestions.json')
for fp, c in kat.items(): json.dump(c, open(fp, 'w'), ensure_ascii=False, indent=1)
print('YAZILDI; yedek:', Y)
