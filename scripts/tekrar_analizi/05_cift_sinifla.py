"""Kopya çiftlerini (kesin + gri) sınav birimi kuralına göre sınıflandır → cift_karar.jsonl"""
import json, re, collections
R = {json.loads(l)['id']: json.loads(l) for l in open('sorular_ozet.jsonl')}
U = json.load(open('birim.json'))
P = [json.loads(l) for l in open('ciftler.jsonl')]
num = lambda s: tuple(sorted(re.findall(r'\d+(?:[.,]\d+)?', re.sub(r'^\s*\d{1,3}\s*[\).\-]', '', s or ''))))
def vstem(r, v):
    for x in r['variants']:
        if x['v'] == v: return x['stem']
    return ''
def benzerlik(p):
    a, b = R[p['a']], R[p['b']]
    s, o, pt, ans = p['stem'], p['opt'], p['part'], p['ans']
    ne = num(vstem(a, p['va'])) == num(vstem(b, p['vb']))
    if (s >= 90 and (o is None or o >= 0.8) and ne) or (s >= 80 and o is not None and o >= 0.8 and (ans or 0) >= 90 and ne) \
       or (pt >= 95 and o is not None and o >= 0.8 and ne): return 'ayni'
    if s >= 85 and o is not None and o < 0.5: return 'farkli_siklar'
    if s < 70 and pt < 85 and (o or 0) < 0.8: return 'farkli'
    return 'gri'
# bölüm örtüşmesi (03'ten)
OV = {}
for l in open('bolum_ortusme.tsv'):
    ov, sa, _, _, sb, _, _ = l.rstrip('\n').split('\t'); OV[(sa, sb)] = OV[(sb, sa)] = float(ov)
# belge düzeyi örtüşme (metin 'aynı' çiftleri): yılı kesin olmayan iki belge çok örtüşüyorsa "farklı yıl" denemez
_bs = collections.Counter(v['bolum'] if v['belge'].startswith('combinepdf') else v['belge'] for v in U.values())
_bl = collections.defaultdict(set)
def _bk(i): return U[i]['bolum'] if U[i]['belge'].startswith('combinepdf') else U[i]['belge']
for _p in P:
    if benzerlik(_p) == 'ayni':
        _bl[(_bk(_p['a']), _bk(_p['b']))].add(_p['a']); _bl[(_bk(_p['b']), _bk(_p['a']))].add(_p['b'])
def belge_ortusme(a, b):
    ba, bb = _bk(a), _bk(b)
    return max(len(_bl[(ba, bb)]) / _bs[ba], len(_bl[(bb, ba)]) / _bs[bb])
TEK_SINAV_BELIRSIZ = set()   # yılı bilinmeyen ama tek sınav olduğu kesin belge yok (ihtiyatlı)
def iliski(a, b):
    ua, ub = U[a], U[b]
    ra, rb = R[a], R[b]
    if ua['belge'] == ub['belge']:
        if ua['belge'].startswith(('combinepdf:', 'D3K1pdf:')) and ua['yil']:
            return 'BIRLESTIR', 'ayni_sinav_ayni_cikti', f"aynı sınav çıktısı/bölümü ({ua['belge'].split(':')[1]})"
        if (ua['yil'] and ua['kesinlik'] in ('kesin', 'olasi')) or ua['kesinlik'] == 'tek_sinav':
            return 'BIRLESTIR', 'ayni_belge_tek_sinav', f"aynı sınav belgesi ({ua['gerekce']})"
        qa, qb = ra.get('questionNumber'), rb.get('questionNumber')
        if qa and qb and qa == qb:
            return 'BIRLESTIR', 'ayni_belge_ayni_sira', 'aynı belgenin farklı dökümleri (txt/pdf), aynı soru sırası'
        return 'BEKLET', 'belirsiz_ayni_belge', 'aynı derleme belgesinde iki kez; yıl/sınav ayrımı yapılamıyor'
    if ua['yil'] and ub['yil']:
        if ua['yil'] != ub['yil']:
            if not (ua['kesinlik'] == 'kesin' and ub['kesinlik'] == 'kesin') and belge_ortusme(a, b) >= 0.35:
                return 'BEKLET', 'yil_celiskili_ortusme', f"{ua['yil']} ↔ {ub['yil']} (yıl kesin değil, belgeler %{round(belge_ortusme(a, b)*100)} örtüşüyor)"
            return 'KORU', 'farkli_yil', f"{ua['yil']} {ua['sinav']} ↔ {ub['yil']} {ub['sinav']}"
        if ua['sinav'] != ub['sinav']:
            kf = {ua['sinav'][0], ub['sinav'][0]}
            if 'F' in kf or 'B' in kf:
                return 'KORU', 'kurul_final_ayni_yil', f"{ua['yil']}: {ua['sinav']} ↔ {ub['sinav']}"
            return 'KORU', 'ayni_yil_farkli_kurul', f"{ua['yil']}: {ua['sinav']} ↔ {ub['sinav']}"
        ka, kb = ua['kesinlik'], ub['kesinlik']
        ov = OV.get((ua['bolum'], ub['bolum']), 0)
        if ka == 'kesin' and kb == 'kesin':
            return 'BIRLESTIR', 'ayni_yil_ayni_kurul', f"{ua['yil']} {ua['sinav']} (iki kesin kaynak)"
        if ov >= 0.6:
            return 'BIRLESTIR', 'ayni_yil_ayni_kurul', f"{ua['yil']} {ua['sinav']} (kaynaklar %{round(ov*100)} örtüşüyor)"
        return 'BEKLET', 'olasi_ayni_sinav', f"{ua['yil']} {ua['sinav']} ({ka}/{kb}; kesin değil)"
    return 'BEKLET', 'yil_belirsiz', f"{ua['yil'] or '?'} {ua['sinav'] or ''} ↔ {ub['yil'] or '?'} {ub['sinav'] or ''}"
out = open('cift_karar.jsonl', 'w'); C = collections.Counter()
for p in P:
    bz = benzerlik(p)
    if bz == 'farkli': continue
    k, neden, acik = iliski(p['a'], p['b'])
    p.update({'benzerlik': bz, 'karar': k, 'neden': neden, 'aciklama': acik})
    out.write(json.dumps(p, ensure_ascii=False) + '\n'); C[(bz, k, neden)] += 1
for k, v in sorted(C.items()): print(v, k)
