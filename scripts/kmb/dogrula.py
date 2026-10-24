#!/usr/bin/env python3
"""KMB görsel asistan içerik kapısı (docs/KMB_GORSEL_ASISTAN.md §2 A6). 0 HATA olmadan ses ve yayın yok.
Denetler: şema, hedef kapsamı (her öğrenim hedefi ≥1 adım), sahne/öge kimlikleri (sahneler.tsx SAHNE_OGELERI),
cümle başına eylem, senaryoda tek doğru şık + şık açıklama standardı, Türkçe üslup, bul görevinin hedefi.
Kullanım: python3 meds/scripts/kmb/dogrula.py [kod …]"""
import json, re, sys
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MEDS / 'scripts'))
import sik_aciklama as SA  # noqa: E402
import turkce_uslup as TU  # noqa: E402

VERI = MEDS / 'src/data/kmb'
SAHNE_TSX = MEDS / 'src/components/kmb/sahneler.tsx'
EYLEMLER = {'vurgula', 'ciz', 'renk', 'goster', 'gizle', 'etiket'}
RENKLER = {'yesil', 'kirmizi', 'mavi', 'sari'}


def sahne_ogeleri():
    t = SAHNE_TSX.read_text(encoding='utf-8')
    blok = t[t.index('SAHNE_OGELERI'):]
    blok = blok[:blok.index('\n};')] + '\n'
    s = {}
    for ad, ic in re.findall(r"\n\s+'?([\w-]+)'?: \[(.*?)\],?(?=\n)", blok):
        s[ad] = set(re.findall(r"'([a-z]{1,2}-[a-z0-9-]+)'", ic))
    # malzeme listesi MALZEMELER'den gelir
    s['malzeme'] = s.get('malzeme', set()) | set(re.findall(r"\['(m-[a-z-]+)', '", t))
    return s


def denetle(p: Path, S):
    H, U = [], []
    d = json.loads(p.read_text(encoding='utf-8'))
    for k in ('kod', 'slug', 'ad', 'belgeKodu', 'amac', 'hedefler', 'adimlar', 'sinav'):
        if k not in d: H.append(f'{k} alanı yok')
    if H: return H, U
    ids = [a['id'] for a in d['adimlar']]
    if len(set(ids)) != len(ids): H.append('yinelenen adım kimliği')
    for h in d['hedefler']:
        if not h.get('adimlar'): H.append(f'hedef {h["no"]}: bağlı adım yok')
        for a in h.get('adimlar', []):
            if a not in ids: H.append(f'hedef {h["no"]}: bilinmeyen adım {a}')

    def eylem_denetle(ey, sahne, yer):
        for e in ey or []:
            if e.get('t') not in EYLEMLER: H.append(f'{yer}: bilinmeyen eylem {e.get("t")}')
            if e.get('id') not in S.get(sahne, set()): H.append(f'{yer}: {sahne} sahnesinde öge yok: {e.get("id")}')
            if e.get('t') == 'renk' and e.get('renk') not in RENKLER: H.append(f'{yer}: renk {e.get("renk")}')

    for a in d['adimlar']:
        y = f'adım {a["id"]}'
        if a.get('sahne') not in S: H.append(f'{y}: sahne yok {a.get("sahne")}'); continue
        lotti = {v['ad'] for v in json.loads((VERI / 'lottie/index.json').read_text(encoding='utf-8'))} if (VERI / 'lottie/index.json').exists() else set()
        for e in [e for e in a.get('ek', []) if e.startswith('lottie:')]:
            if e[7:] not in lotti: H.append(f'{y}: Lottie videosu yok {e}')
        ekler = [e for e in a.get('ek', []) if not e.startswith('lottie:')]
        for e in ekler:
            if e not in S: H.append(f'{y}: ek sahne yok {e}')
        S[f'_{a["id"]}'] = set().union(*(S.get(x, set()) for x in [a['sahne'], *ekler]))
        if not 3 <= len(a['cumleler']) <= 8: H.append(f'{y}: {len(a["cumleler"])} cümle (3–8)')
        kel = sum(len(c['metin'].split()) for c in a['cumleler'])
        if kel < 35: H.append(f'{y}: {kel} kelime — çok yüzeysel')
        for i, c in enumerate(a['cumleler']):
            if not c.get('metin', '').strip(): H.append(f'{y}[{i}]: boş cümle')
            if not c.get('eylem'): U.append(f'{y}[{i}]: görsel eylemsiz cümle')
            eylem_denetle(c.get('eylem'), f'_{a["id"]}', f'{y}[{i}]')
    sn = d['sinav']
    if not sn.get('akislar'): H.append('akış (OSCE sıralama) yok')

    def basamak_denetle(L, yer, gorulen):
        for b in L:
            y = f'{yer}/{b.get("id")}'
            if b.get('id') in gorulen: H.append(f'{y}: yinelenen basamak kimliği')
            gorulen.add(b.get('id'))
            if not b.get('metin'): H.append(f'{y}: metin yok')
            if len(SA.cumleler(b.get('aciklama', ''))) < 2: H.append(f'{y}: ayrıntılı açıklama en az 2 cümle')
            dal = b.get('dal')
            if dal:
                if b is not L[-1]: H.append(f'{y}: dal yalnız listenin son basamağında olabilir')
                if len(dal.get('yollar', [])) < 2: H.append(f'{y}: dalda en az 2 yol')
                for yol in dal.get('yollar', []):
                    if not yol.get('basamaklar'): H.append(f'{y}: {yol.get("id")} yolu boş')
                    basamak_denetle(yol.get('basamaklar', []), f'{y}>{yol.get("id")}', gorulen)

    for ak in sn.get('akislar', []):
        if len(ak['basamaklar']) < 6: H.append(f'akış {ak["id"]}: en az 6 basamak')
        basamak_denetle(ak['basamaklar'], f'akış {ak["id"]}', set())
    if len(sn['senaryolar']) < 5: H.append('senaryo: en az 5 vaka')
    for s in sn['senaryolar']:
        y = f'senaryo {s["id"]}'
        if s.get('sahne') not in S: H.append(f'{y}: sahne yok')
        eylem_denetle(s.get('eylem'), s.get('sahne'), y)
        if sum(1 for c in s['secenekler'] if c['dogru']) != 1: H.append(f'{y}: tam 1 doğru şık olmalı')
        if len(s['secenekler']) < 3: H.append(f'{y}: en az 3 şık')
        for i, c in enumerate(s['secenekler']):
            H += SA.denetle(c['aciklama'], f'{y} şık {i + 1}', enaz=18)
    for b in sn['bul']:
        if b['hedef'] not in S.get(b['sahne'], set()): H.append(f'bul {b["id"]}: hedef öge yok {b["hedef"]}')
    hc = d.get('hedefCalisma', [])
    if sorted(x['no'] for x in hc) != sorted(h['no'] for h in d['hedefler']): H.append('hedefCalisma: her öğrenim hedefi için tam bir kart olmalı')
    for x in hc:
        y = f'hedef kartı {x["no"]}'
        if x['sahne'] not in S: H.append(f'{y}: sahne yok')
        eylem_denetle(x.get('eylem'), x['sahne'], y)
        for k in ('ne', 'neden', 'hata', 'hoca'):
            if not x.get(k): H.append(f'{y}: {k} boş')
        if len(x.get('nasil', [])) < 2: H.append(f'{y}: nasıl en az 2 cümle')
        if x.get('lottie') and (VERI / f'lottie/{x["lottie"]}.json').exists() is False: H.append(f'{y}: Lottie yok')
        if x.get('dogrulanacak'): U.append(f'{y}: doğrulanacak — {x["dogrulanacak"]}')
    H += TU.denetle_yapi(d, p.stem)
    ai = VERI / 'lottie/adimlar.json'
    av = {v['adim']: v for v in json.loads(ai.read_text(encoding='utf-8'))} if ai.exists() else {}
    for a in d['adimlar']:
        v = av.get(a['id'])
        if not v: H.append(f'adım {a["id"]}: adım videosu yok (adim_lottie.py) — her cümle videoda olmalı')
        elif len(v['bolumler']) != len(a['cumleler']): H.append(f'adım {a["id"]}: video bölümü {len(v["bolumler"])} ≠ cümle {len(a["cumleler"])}')
        elif [b['metin'] for b in v['bolumler']] != [c['metin'] for c in a['cumleler']]: H.append(f'adım {a["id"]}: video metni ders metniyle aynı değil (adim_lottie.py yeniden)')
        elif not v.get('sesli'): U.append(f'adım {a["id"]}: adım videosu ses zamanlı değil')
    li = VERI / 'lottie/index.json'
    if li.exists():
        for v in json.loads(li.read_text(encoding='utf-8')):
            if not 15 <= v['sure'] <= 90: H.append(f'lottie {v["ad"]}: süre {v["sure"]} sn (15–90)')
            for b in v['bolumler']: H += TU.denetle(b['metin'], f'lottie {v["ad"]}')
    for a in d['adimlar']:
        for x in a.get('dogrulanacak', []): U.append(f'adım {a["id"]}: doğrulanacak — {x}')
    return H, U


def main(kodlar):
    S = sahne_ogeleri()
    idx = json.loads((VERI / 'index.json').read_text(encoding='utf-8'))
    hazir = [b['kod'] for b in idx['beceriler'] if b['durum'] == 'hazir']
    top = 0
    for kod in kodlar or hazir:
        H, U = denetle(VERI / f'{kod}.json', S)
        for u in U: print(f'  UYARI {kod}: {u}')
        for h in H: print(f'  HATA  {kod}: {h}')
        print(f'{kod}: {len(H)} HATA, {len(U)} uyarı')
        top += len(H)
    print(f'TOPLAM {top} HATA')
    sys.exit(1 if top else 0)


if __name__ == '__main__':
    main(sys.argv[1:])
