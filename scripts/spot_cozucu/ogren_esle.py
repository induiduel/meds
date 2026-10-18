#!/usr/bin/env python3
"""Sesli çözücü / asistan → Öğren slaytı eşlemesi.

Her çözücü sorusunu (ve sesli asistan noktasını) aynı ders PDF'inden üretilmiş yayımlanmış Öğren destelerinin
slaytlarına bağlar. Aday slaytlar `src/data/deckPdfSources.json`'daki (içerikle doğrulanmış) PDF eşlemesinden gelir;
sıralama = slayt metni ile soru metninin TF-IDF benzerliği + PDF sayfa örtüşmesi. Kanıt zayıfsa eşleme yazılmaz
(yanlış slayt göstermektense hiç göstermemek).

Çıktı: src/data/cozucu_ogren/<brans>.json
  {"surum", "desteler": [deckId...], "dersler": {<kod>: {"s": {<soruNo>: [[desteSıra, slaytNo, puan], ...]},
                                                       "n": {<noktaId>: [...]}}}}
Kullanım: python3 scripts/spot_cozucu/ogren_esle.py  (deste/çözücü/PDF eşlemesi değişince yeniden çalıştır)
"""
import json, math, re, unicodedata
from collections import Counter
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]          # meds/
DATA = KOK / 'src' / 'data'
TEMP = KOK.parent / 'meds_temp'
CIKTI = DATA / 'cozucu_ogren'

PDF_LISTE = {'patoloji': TEMP / 'patoloji_onem' / 'pdf_liste.json'}
for p in sorted((TEMP / 'spot_cozucu').glob('*/pdf_liste.json')):
    PDF_LISTE[p.parent.name] = p

# Eşikler: benzerlik (kosinüs) + sayfa katkısı
SAYFA_TAM, SAYFA_YAKIN = 0.25, 0.12
ESIK_TEK, ESIK_SAYFALI = 0.14, 0.07
GENIS_ARALIK = 0.4   # PDF'in %40'ından geniş aralık (özet/tekrar/oyun adımı) sayfa kanıtı sayılmaz
EN_COK = 3

DURAK = set('''ve ile bir bu için olan olarak daha çok en ya da de da mi mı mu mü ki gibi hangisi hangisidir aşağıdakilerden
değildir doğrudur yanlıştır olur olmaz eder ise iken kadar sonra önce her tüm bazı diğer şekilde nedeniyle sonucu durumda
bulunur görülür ilgili arasında üzere tarafından veya ancak fakat çünkü yani hem göre sık sıklıkla nedir olduğu olması'''.split())
CP = re.compile(r'^\s*\[(TEKRAR SAYFASI|OYUN SAYFASI)', re.I)


def nfc(s): return unicodedata.normalize('NFC', s or '')


def kucuk(s):
    return nfc(s).replace('İ', 'i').replace('I', 'ı').lower()


def jetonlar(s):
    s = re.sub(r'\*\*|__|[#>`|]', ' ', kucuk(s))
    out = []
    for w in re.findall(r'[0-9a-zçğıöşüâîû]+', s):
        if len(w) < 3 or w in DURAK:
            continue
        out.append(w[:6])
    return out


def dz(x):
    if isinstance(x, str): return x
    if isinstance(x, dict): return ' '.join(dz(v) for v in x.values())
    if isinstance(x, list): return ' '.join(dz(v) for v in x)
    return ''


def slayt_metni(s):
    cc = s.get('coreContent') if isinstance(s.get('coreContent'), dict) else {}
    parca = [s.get('title', ''), s.get('synthesisNarrative') or s.get('content') or cc.get('text') or '']
    parca += [f"{b.get('title', '')} {b.get('desc', '')}" for b in cc.get('keyBullets') or [] if isinstance(b, dict)]
    parca += [x for x in (s.get('spotPearls') or s.get('spots') or []) if isinstance(x, str)]
    if isinstance(cc.get('table'), dict):
        parca.append(dz(cc['table'].get('headers')) + ' ' + dz(cc['table'].get('rows')))
    parca += [t.get('term', '') for t in s.get('medicalTerms') or [] if isinstance(t, dict)]
    return ' '.join(parca)


def yayinda(d):
    return bool(d.get('isNew') or str(d.get('version', '')).startswith('2') or (d.get('slideCount') or 0) >= 50
                or (d.get('totalSlides') or 0) >= 50 or d.get('versionGroup'))


def ad_anahtari(ad):
    """'27)Mesane Hastalıkları.pdf' → 'mesane hastalıkları' (yeniden numaralanan PDF'ler için)."""
    return re.sub(r'\s+', ' ', re.sub(r'^\s*\d+\s*\)\s*', '', kucuk(ad)).replace('.pdf', '').replace("'", '')).strip()


def main():
    kaynak = json.loads((DATA / 'deckPdfSources.json').read_text())['decks']
    katalog = {d['id']: d for d in json.loads((DATA / 'decks' / 'catalog.json').read_text())}
    ada = {}
    for did, v in kaynak.items():
        if did not in katalog or not yayinda(katalog[did]):
            continue
        for fi, f in enumerate(v['files']):
            ada.setdefault(nfc(f['name']), []).append((did, fi, f.get('pages') or 0))
    baslik_ada = {}
    for ad, l in ada.items():
        baslik_ada.setdefault(ad_anahtari(ad), []).extend(l)

    deste_bellek = {}

    def deste(did):
        if did not in deste_bellek:
            ham = json.loads((DATA / 'decks' / 'items' / f'{did}.json').read_text())
            sl = ham.get('slides') or ham.get('steps') or []
            deste_bellek[did] = [(s.get('slideNumber') or i + 1, s) for i, s in enumerate(sl)
                                 if not CP.match(str(s.get('title', ''))) and not s.get('isGameFinale') and not s.get('isCheckpoint')]
        return deste_bellek[did]

    CIKTI.mkdir(exist_ok=True)
    genel = Counter()
    for brans, liste_yolu in PDF_LISTE.items():
        cdizin = DATA / f'{brans}_cozucu'
        if not cdizin.exists():
            continue
        pdfler = {x['kod']: x for x in json.loads(liste_yolu.read_text())}
        desteler, dersler, say, asistan_bitti = [], {}, Counter(), set()

        for dosya in sorted(cdizin.glob('*.json')):
            if dosya.stem == 'index':
                continue
            ders = json.loads(dosya.read_text())
            temel = ders.get('klasor') or dosya.stem.split('-')[0]
            pdf = pdfler.get(temel)
            if not pdf:
                say['pdf_yok'] += len(ders['sorular']); continue
            adaylar = ada.get(nfc(pdf['ad'])) or [x for x in baslik_ada.get(ad_anahtari(pdf['ad']), []) if x[2] == pdf.get('sayfa')]
            if not adaylar:
                say['deste_yok'] += len(ders['sorular']); continue

            # aday slaytlar: (did, slaytNo, aralık|None, jeton sayacı)
            slaytlar = []
            for did, fi, sayfa_sayisi in adaylar:
                aralik = kaynak[did]['slides']
                for no, s in deste(did):
                    r = aralik.get(str(no))
                    if r and (len(r) > 2 and r[2] != fi or len(r) == 2 and fi != 0):
                        r = None
                    if r and sayfa_sayisi and (r[1] - r[0] + 1) > GENIS_ARALIK * sayfa_sayisi:
                        r = None
                    slaytlar.append((did, no, r, Counter(jetonlar(slayt_metni(s)))))
            df = Counter()
            for *_, c in slaytlar:
                df.update(c.keys())
            N = len(slaytlar)
            idf = {w: math.log((N + 1) / (n + 0.5)) for w, n in df.items()}

            def vek(c):
                v = {w: (1 + math.log(n)) * idf.get(w, math.log(N + 1)) for w, n in c.items()}
                norm = math.sqrt(sum(x * x for x in v.values())) or 1
                return {w: x / norm for w, x in v.items()}
            svek = [vek(c) for *_, c in slaytlar]

            def esle(metin, sayfalar):
                q = vek(Counter(jetonlar(metin)))
                adaylar_ = []
                for (did, no, r, _), sv in zip(slaytlar, svek):
                    cos = sum(x * sv.get(w, 0) for w, x in q.items())
                    sp = 0.0
                    if r and sayfalar:
                        if any(r[0] <= p <= r[1] for p in sayfalar): sp = SAYFA_TAM
                        elif any(r[0] - 2 <= p <= r[1] + 2 for p in sayfalar): sp = SAYFA_YAKIN
                    if cos >= ESIK_TEK or (sp == SAYFA_TAM and cos >= ESIK_SAYFALI):
                        adaylar_.append((cos + sp, did, no))
                en_iyi = {}
                for puan, did, no in sorted(adaylar_, reverse=True):
                    en_iyi.setdefault(did, (puan, no))
                sira = sorted(((p, did, no) for did, (p, no) in en_iyi.items()), reverse=True)[:EN_COK]
                out = []
                for p, did, no in sira:
                    if did not in desteler: desteler.append(did)
                    out.append([desteler.index(did), no, round(min(p, 1) * 100)])
                return out

            kayit = {'s': {}, 'n': {}}
            for q in ders['sorular']:
                metin = ' '.join([q['soru'], q['secenekler'].get(q['dogru'], ''), q.get('cozum', ''), q.get('siklar', {}).get(q['dogru'], '')])
                e = esle(metin, q.get('sayfa') or [])
                if e: kayit['s'][str(q['no'])] = e; say['soru_eslendi'] += 1
                else: say['soru_eslenmedi'] += 1

            # sesli asistan noktaları (ders kodu = set öneki, ör. u04-1 → u04; sayfa önem maddesinin alıntılarından)
            if temel not in asistan_bitti:
                asistan_bitti.add(temel)
                ay = DATA / f'{brans}_asistan' / f'{temel}.json'
                oy = DATA / f'{brans}_onem' / f'{temel}.json'
                if ay.exists():
                    onem = {m['id']: m for m in json.loads(oy.read_text())['maddeler']} if oy.exists() else {}
                    for n in json.loads(ay.read_text()).get('noktalar', []):
                        m = onem.get(n['id'], {})
                        sayfalar = sorted({a.get('sayfa') for a in m.get('alinti') or [] if isinstance(a, dict) and a.get('sayfa')})
                        metin = ' '.join([n.get('baslik', ''), n.get('bilgi', ''), ' '.join(n.get('cumleler') or [])])
                        e = esle(metin, sayfalar)
                        if e: kayit['n'][n['id']] = e; say['nokta_eslendi'] += 1
                        else: say['nokta_eslenmedi'] += 1
            if kayit['s']:
                dersler.setdefault(dosya.stem, {})['s'] = kayit['s']
            if kayit['n']:
                dersler.setdefault(temel, {})['n'] = kayit['n']

        (CIKTI / f'{brans}.json').write_text(json.dumps(
            {'surum': 'cozucu-ogren-v1', 'desteler': desteler, 'dersler': dersler}, ensure_ascii=False, separators=(',', ':')))
        print(f'{brans:12} {dict(say)}')
        genel.update(say)
    print('TOPLAM', dict(genel))


if __name__ == '__main__':
    main()
