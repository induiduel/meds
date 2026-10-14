#!/usr/bin/env python3
"""
Hastalıklar bilgi tabanı (şema 2) — birleştirme, denetim ve veri havuzu dışa aktarımı.

Kullanım:
  python3 scripts/diseases/hastalik_profilleri.py birlestir --girdi <out klasörü> --esler <alias_of.json> [--kaynak <özgün.json>] [--yaz]
      Yeniden yazılmış profilleri (her biri <id>.json) src/data/diseases.json'a şema 2 olarak birleştirir.
      Eski kaydın createdAt / relatedLectures bilgisi korunur; birleştirilen çift kayıtların kimliği `aliases`,
      adları `altNames` olur. Yazmadan önce eski dosya meds_temp/hastalik_yedek/<zaman>/ altına yedeklenir.
      --yaz verilmezse yalnız rapor üretir (deneme).
  python3 scripts/diseases/hastalik_profilleri.py denetle
      diseases.json'da şablon/dolgu cümle, eksik bölüm, geçersiz varlık türü arar (0 HATA beklenir).
  python3 scripts/diseases/hastalik_profilleri.py disa-aktar
      Veri havuzuna yazar: $MEDS_DATABASE_DIR/derived/hastaliklar/
        profiller.jsonl   — her satır bir profil modeli (şema 2)
        maddeler.jsonl    — her satır bir madde: profil + bölüm + etiket + metin + varlıklar (analiz/RAG için düz tablo)
        varlik_dizini.json — varlık → geçtiği profiller ve bölümler ("belirti:ateş" → [...])
        rapor.json        — sayımlar
      JSON Schema: $MEDS_DATABASE_DIR/schema/disease.schema.json

Varlık adları `varlik_esanlamlari.json` ile kanonik biçime getirilir ("yüksek ateş" → "ateş").
Yerel GPU/LLM kullanmaz.
"""
import argparse, datetime as dt, glob, json, os, re, shutil, sys
from collections import Counter, defaultdict

APP = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATA = os.path.join(APP, 'src', 'data', 'diseases.json')
DB = os.environ.get('MEDS_DATABASE_DIR') or os.path.abspath(os.path.join(APP, '..', 'meds_database'))
TEMP = os.environ.get('MEDS_TEMP_DIR') or os.path.abspath(os.path.join(APP, '..', 'meds_temp'))
SYN = os.path.join(os.path.dirname(__file__), 'varlik_esanlamlari.json')

SECTIONS = ['definition', 'etiology', 'physiology', 'pathology', 'symptoms', 'pathognomonic', 'diagnosis', 'imaging',
            'treatment', 'complications', 'epidemiology', 'lecture']
KINDS = {'hastalik', 'bulgu', 'patolojik_surec', 'mekanizma', 'molekul_hucre', 'ilac', 'kavram', 'yontem'}
ETYPES = {'belirti', 'bulgu', 'laboratuvar', 'goruntuleme', 'histopatoloji', 'patojen', 'gen_protein', 'ilac', 'tedavi',
          'test', 'hastalik', 'anatomi', 'risk_faktoru', 'hucre', 'mekanizma'}
PLACEHOLDER = [r'standart medikal protokol', r'laboratuvar incelemeleri ve klinik', r'radyolojik görüntüleme ve',
               r'tablosuna özgü akut veya kronik', r'altta yatan tetikleyici genetik', r'karakteristik histopatolojik doku',
               r'hücresel düzeyde fizyopatolojik', r'toplumda yaş ve cinsiyet', r'incelenmektedir', r'…']


STRICT_VERIFY = os.environ.get('HASTALIK_DOGRULAMA_ZORUNLU', '1') == '1'


def now_iso():
    return dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def load_syn():
    try:
        return json.load(open(SYN, encoding='utf-8'))
    except FileNotFoundError:
        return {}


def canon_entity(e, syn):
    """Varlığı kanonik biçime getirir. syn: {"tür:ad": {"name":..,"type":..,"qualifier":..}} ya da {"ad": "kanonik ad"}"""
    name = re.sub(r'\s+', ' ', str(e.get('name') or '')).strip()
    typ = e.get('type')
    q = (e.get('qualifier') or '').strip()
    key = f'{typ}:{name.lower()}'
    rule = syn.get(key) or syn.get(name.lower())
    if isinstance(rule, str):
        name = rule
    elif isinstance(rule, dict):
        if rule.get('qualifier') and not q:
            q = rule['qualifier']
        name, typ = rule.get('name', name), rule.get('type', typ)
    out = {'name': name, 'type': typ}
    if q:
        out['qualifier'] = q
    return out


def clean_fact(f, syn, nref=0):
    o = {'text': re.sub(r'\s+', ' ', str(f.get('text') or '')).strip()}
    its = [re.sub(r'\s+', ' ', str(x)).strip() for x in f.get('items') or [] if str(x).strip()]
    if its:
        o['items'] = its
    if f.get('label'):
        o['label'] = str(f['label']).strip()
    if f.get('key'):
        o['key'] = True
    ents, seen = [], set()
    for e in f.get('entities') or []:
        c = canon_entity(e, syn)
        k = (c['type'], c['name'].lower())
        if c['name'] and k not in seen:
            seen.add(k)
            ents.append(c)
    if ents:
        o['entities'] = ents
    if f.get('source'):
        o['source'] = str(f['source']).strip()
    refs = sorted({int(x) for x in f.get('refs') or [] if isinstance(x, int) and 0 <= x < nref})
    if refs:
        o['refs'] = refs
    return o


def cmd_birlestir(a):
    # Kaynak: özgün (şema 1, çift kayıtlı) liste — birleştirme tekrar çalıştırılabilsin diye yedekten okunabilir
    old = json.load(open(a.kaynak or DATA, encoding='utf-8'))
    byid = {d['id']: d for d in old}
    alias_of = json.load(open(a.esler, encoding='utf-8'))
    syn = load_syn()
    files = {os.path.basename(p)[:-5]: p for p in glob.glob(os.path.join(a.girdi, '*.json'))}
    canon_ids = [d['id'] for d in old if d['id'] not in alias_of]
    missing = [i for i in canon_ids if i not in files]
    if missing and not a.eksige_izin:
        print(f'EKSİK {len(missing)} profil (ör. {missing[:8]}); --eksige-izin ile eskileri koruyarak devam edilebilir.')
        sys.exit(1)
    ts = now_iso()
    out = []
    for cid in canon_ids:
        o = byid[cid]
        if cid not in files:
            out.append(o)  # yeniden yazılmamış: eski kayıt olduğu gibi (arayüz şema 1'i dönüştürür)
            continue
        n = json.load(open(files[cid], encoding='utf-8'))
        aliases = [x for x, c in alias_of.items() if c == cid]
        nref = len(n.get('references') or [])
        alt = []
        for x in [cid] + aliases:
            nm = byid[x]['name']
            if nm and nm != n['name'] and nm not in alt:
                alt.append(nm)
        lectures = []
        for x in [cid] + aliases:
            for l in byid[x].get('relatedLectures') or []:
                if l not in lectures:
                    lectures.append(l)
        rec = {
            'id': cid,
            'name': n['name'].strip(),
            'latinName': (n.get('latinName') or '').strip() or None,
            'icd_code': n.get('icd_code') or None,
            'kind': n['kind'],
            'category': n['category'],
            'aliases': aliases,
            'altNames': alt,
            'hallmarks': [clean_fact(f, syn, nref) for f in n.get('hallmarks') or []],
            'sections': {s: [clean_fact(f, syn, nref) for f in (n.get('sections') or {}).get(s) or []] for s in SECTIONS},
            # Kaynak sırası korunur: maddelerdeki refs bu dizinin sıralarına işaret eder
            'references': [{k: v for k, v in r.items() if k in ('label', 'url') and v} for r in n.get('references') or []],
            **({'verification': n['verification']} if isinstance(n.get('verification'), dict) else {}),
            'relatedLectures': lectures,
            'schemaVersion': 2,
            'curation': {'method': 'ders notu + ders kitabı (Robbins/Harrison/Katzung) + resmi kılavuz doğrulaması; madde/varlık modeli', 'at': ts},
            'isCustom': False,
            'createdAt': o.get('createdAt') or ts,
            'updatedAt': ts,
        }
        rec['sections'] = {s: v for s, v in rec['sections'].items() if v}
        out.append(rec)
    errs = denetle(out)
    kinds = Counter(d.get('kind', 'eski') for d in out)
    print(f'{len(out)} profil ({len(old)} eski kayıttan, {len(alias_of)} çift birleşti) · tür: {dict(kinds)} · denetim: {len(errs)} hata')
    for e in errs[:40]:
        print('  ✗', e)
    if not a.yaz:
        print('Deneme: yazılmadı (--yaz ile yaz).')
        return
    if errs and not a.eksige_izin:
        print('Hata varken yazılmaz.')
        sys.exit(1)
    bdir = os.path.join(TEMP, 'hastalik_yedek', dt.datetime.now().strftime('%Y%m%d-%H%M%S'))
    os.makedirs(bdir, exist_ok=True)
    shutil.copy2(DATA, os.path.join(bdir, 'diseases.json'))
    tmp = DATA + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    os.replace(tmp, DATA)
    print(f'Yazıldı: {DATA}\nYedek: {bdir}/diseases.json')


def denetle(lst):
    errs = []
    ids = Counter(d['id'] for d in lst)
    for i, n in ids.items():
        if n > 1:
            errs.append(f'{i}: kimlik tekrarı')
    for d in lst:
        if d.get('schemaVersion') != 2:
            continue
        p = d['id']
        if d.get('kind') not in KINDS:
            errs.append(f'{p}: kind geçersiz')
        if not d.get('hallmarks'):
            errs.append(f'{p}: karakteristik özellik yok')
        facts = list(d.get('hallmarks') or []) + [f for s in SECTIONS for f in (d.get('sections') or {}).get(s) or []]
        if len(facts) < 10:
            errs.append(f'{p}: az madde ({len(facts)})')
        for f in facts:
            t = f.get('text', '').lower()
            for pat in PLACEHOLDER:
                if re.search(pat, t):
                    errs.append(f'{p}: şablon/dolgu «{f["text"][:60]}»')
            for e in f.get('entities') or []:
                if e.get('type') not in ETYPES:
                    errs.append(f'{p}: varlık türü {e.get("type")}')
        if d.get('verification'):
            refs = d.get('references') or []
            urls = {i for i, r in enumerate(refs) if str(r.get('url') or '').startswith('https://')}
            for f in facts:
                if not set(f.get('refs') or []) & urls:
                    errs.append(f'{p}: web kaynağına bağlanmamış madde «{f["text"][:50]}»')
        elif STRICT_VERIFY:
            # Amfi slaytı veya ders notu kaynaklı akademik profiller ders işçisi/amfi kanıtıyla onaylıdır
            is_lecture_backed = bool(d.get('relatedLectures')) or (d.get('curation') or {}).get('source') == 'ders_isci' or any(
                r.get('title') or r.get('source') or 'ders' in str(r.get('label', '')).lower() for r in (d.get('references') or [])
            )
            if not is_lecture_backed:
                errs.append(f'{p}: web doğrulaması yok')
        if d.get('kind') == 'hastalik':
            for s in ('definition', 'symptoms', 'treatment'):
                if not (d.get('sections') or {}).get(s):
                    errs.append(f'{p}: {s} boş')
    return errs


def cmd_denetle(a):
    lst = json.load(open(DATA, encoding='utf-8'))
    errs = denetle(lst)
    v2 = sum(1 for d in lst if d.get('schemaVersion') == 2)
    print(f'{len(lst)} profil · şema 2: {v2} · {len(errs)} HATA')
    for e in errs[:80]:
        print('  ✗', e)
    hepsi_zorunlu = getattr(a, 'hepsi_sema2', False) or os.environ.get('HASTALIK_HEPSI_SEMA2') == '1'
    sys.exit(1 if errs or (hepsi_zorunlu and v2 < len(lst)) else 0)


def cmd_disa_aktar(_a):
    lst = [d for d in json.load(open(DATA, encoding='utf-8')) if d.get('schemaVersion') == 2]
    outd = os.path.join(DB, 'derived', 'hastaliklar')
    os.makedirs(outd, exist_ok=True)
    idx = defaultdict(lambda: {'hits': []})
    nfacts = 0
    with open(os.path.join(outd, 'profiller.jsonl'), 'w', encoding='utf-8') as fp, \
         open(os.path.join(outd, 'maddeler.jsonl'), 'w', encoding='utf-8') as fm:
        for d in lst:
            fp.write(json.dumps(d, ensure_ascii=False) + '\n')
            rows = [('hallmarks', i, f) for i, f in enumerate(d.get('hallmarks') or [])]
            rows += [(s, i, f) for s in SECTIONS for i, f in enumerate((d.get('sections') or {}).get(s) or [])]
            for sec, i, f in rows:
                nfacts += 1
                fm.write(json.dumps({
                    'madde_id': f'{d["id"]}#{sec}-{i}', 'profil_id': d['id'], 'profil': d['name'], 'tur': d['kind'],
                    'uzmanlik': d['category'], 'bolum': sec, 'etiket': f.get('label'), 'metin': ' '.join([f['text']] + [f'- {x}' for x in f.get('items') or []]).strip(), 'alt_maddeler': f.get('items') or [],
                    'sinav': bool(f.get('key')), 'varliklar': f.get('entities') or [], 'ders_kaynagi': f.get('source'),
                    'dogrulayan_kaynaklar': [(d.get('references') or [])[i] for i in f.get('refs') or [] if i < len(d.get('references') or [])],
                }, ensure_ascii=False) + '\n')
                for e in f.get('entities') or []:
                    k = f'{e["type"]}:{e["name"].lower()}'
                    row = idx[k]
                    row.setdefault('ad', e['name'])
                    row.setdefault('tur', e['type'])
                    hit = {'profil_id': d['id'], 'bolum': sec}
                    if e.get('qualifier'):
                        hit['nitelik'] = e['qualifier']
                    if not any(h['profil_id'] == d['id'] and h['bolum'] == sec for h in row['hits']):
                        row['hits'].append(hit)
    index = {k: {'ad': v['ad'], 'tur': v['tur'], 'profil_sayisi': len({h['profil_id'] for h in v['hits']}), 'gecisler': v['hits']}
             for k, v in sorted(idx.items(), key=lambda kv: (-len({h['profil_id'] for h in kv[1]['hits']}), kv[0]))}
    json.dump(index, open(os.path.join(outd, 'varlik_dizini.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    by_type = Counter(v['tur'] for v in index.values())
    rapor = {
        'zaman': now_iso(), 'profil': len(lst), 'madde': nfacts, 'varlik': len(index), 'varlik_turleri': dict(by_type),
        'profil_turleri': dict(Counter(d['kind'] for d in lst)), 'kaynak': 'meds/src/data/diseases.json (şema 2)',
        'en_yaygin': [{k: v['profil_sayisi']} for k, v in list(index.items())[:25]],
    }
    json.dump(rapor, open(os.path.join(outd, 'rapor.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    os.makedirs(os.path.join(DB, 'schema'), exist_ok=True)
    json.dump(SCHEMA, open(os.path.join(DB, 'schema', 'disease.schema.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{outd}: {len(lst)} profil · {nfacts} madde · {len(index)} varlık')


FACT = {'type': 'object', 'required': ['text'], 'additionalProperties': False, 'properties': {
    'text': {'type': 'string', 'description': 'Tek bilgi; ==terim== vurgu'},
    'items': {'type': 'array', 'items': {'type': 'string'}, 'description': 'Sıralamada her öge ayrı satır'},
    'label': {'type': 'string'}, 'key': {'type': 'boolean', 'description': 'Sınavda sorulan kritik bilgi'},
    'source': {'type': 'string', 'description': 'Ders notu kaynağı'},
    'refs': {'type': 'array', 'items': {'type': 'integer', 'minimum': 0}, 'description': 'Doğrulayan kaynakların references sırası'},
    'entities': {'type': 'array', 'items': {'type': 'object', 'required': ['name', 'type'], 'additionalProperties': False, 'properties': {
        'name': {'type': 'string', 'description': 'Kanonik ad (Türkçe, küçük harf, yalın)'},
        'type': {'enum': sorted(ETYPES)}, 'qualifier': {'type': 'string'}}}}}}
SCHEMA = {
    '$schema': 'https://json-schema.org/draft/2020-12/schema', 'title': 'DiseaseProfile (şema 2)',
    'description': 'MeDSor Hastalıklar bilgi tabanı profili. Her bilgi sorgulanabilir bir madde (fact) nesnesidir.',
    'type': 'object', 'required': ['id', 'name', 'kind', 'category', 'hallmarks', 'sections', 'schemaVersion'],
    'properties': {
        'id': {'type': 'string'}, 'name': {'type': 'string'}, 'latinName': {'type': ['string', 'null']},
        'icd_code': {'type': ['string', 'null']}, 'kind': {'enum': sorted(KINDS)}, 'category': {'type': 'string'},
        'aliases': {'type': 'array', 'items': {'type': 'string'}}, 'altNames': {'type': 'array', 'items': {'type': 'string'}},
        'hallmarks': {'type': 'array', 'items': FACT},
        'sections': {'type': 'object', 'additionalProperties': False, 'properties': {s: {'type': 'array', 'items': FACT} for s in SECTIONS}},
        'references': {'type': 'array', 'items': {'type': 'object', 'required': ['label'], 'properties': {'label': {'type': 'string'}, 'url': {'type': 'string'}}}},
        'verification': {'type': 'object', 'required': ['at', 'method', 'checked'], 'properties': {
            'at': {'type': 'string'}, 'method': {'const': 'web'}, 'checked': {'type': 'integer'}, 'ok': {'type': 'integer'},
            'fixed': {'type': 'integer'}, 'conflict': {'type': 'integer'}, 'removed': {'type': 'integer'}}},
        'relatedLectures': {'type': 'array', 'items': {'type': 'string'}}, 'schemaVersion': {'const': 2},
        'curation': {'type': 'object'}, 'createdAt': {'type': 'string'}, 'updatedAt': {'type': 'string'},
    },
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest='cmd', required=True)
    b = sp.add_parser('birlestir')
    b.add_argument('--girdi', required=True)
    b.add_argument('--esler', required=True)
    b.add_argument('--yaz', action='store_true')
    b.add_argument('--eksige-izin', action='store_true')
    b.add_argument('--kaynak', help='özgün diseases.json (varsayılan: src/data/diseases.json)')
    p_den = sp.add_parser('denetle')
    p_den.add_argument('--hepsi-sema2', action='store_true', help='Tüm profillerin şema 2 olmasını şart koşar')
    sp.add_parser('disa-aktar')
    a = ap.parse_args()
    {'birlestir': cmd_birlestir, 'denetle': cmd_denetle, 'disa-aktar': cmd_disa_aktar}[a.cmd](a)


if __name__ == '__main__':
    main()
