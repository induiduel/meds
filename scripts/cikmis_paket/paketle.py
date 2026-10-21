#!/usr/bin/env python3
"""Çıkmış soru paketleri (Sınava hazırlan › Çıkmış çözücü).

Her kurul ve branş için, kurul sınavındaki o branşın soru sayısı (src/data/sinav_dagilimi.json) kadar sorudan oluşan
paketler kurar. Kaynak yalnız sesli soru çözücüdeki çıkmış sorulardır (src/data/<brans>_cozucu/<kod>.json, tur=cikmis):
bunlar yazar + bağımsız denetçi hattından geçmiş, slayt sayfasına (`sayfa`) bağlı ve EMA ile seslendirilmiştir. Sayfası
olmayan (kazanımı mevcut slaytlarda anlatılmayan) ya da sesi eksik soru alınmaz; aynı soru birden çok derste varsa bir kez.

Dağıtım: dersler sırayla tek tek dolaşılarak (round-robin) sorular paketlere dağıtılır; böylece her paket gerçek sınav
gibi branşın tüm derslerine yayılır. Paket içinde sıra ders sırasıdır. Son paket eksik kalırsa kısa paket olarak kalır.

Kısa not: her soruya sesli sınav asistanının (src/data/<brans>_asistan) bir noktası bağlanır — spot bilgisi, slayttan
yazılmış, denetlenmiş ve EMA ile seslendirilmiş (klip a-<id>). Önce asistanın o soruyu bağladığı nokta (kök eşleşmesi),
yoksa aynı dersin önem maddelerinden slayt sayfası soruyla en çok örtüşen (puanı yüksek) sesli asistan noktası. Sesli
asistanı olmayan derslerde (önem maddeleri şablon metin, kullanılmaz) not slayttan yazılır: scripts/cikmis_paket/notlar.json
(yazar + bağımsız denetçi, turkce_uslup kapısı), EMA sesi not_ses.py ile n-<no> klibi (tür y; metin + klip bu çıktıya gömülür).

Çıktı başvurudur ([ders kodu, soru no, not türü a, not dersi, not id] ya da [ders kodu, soru no, "y"] + branşın `notlar`ı): src/data/cikmis_paket/k<N>.json; metin ve sesler çözücü dosyalarından
çalışma anında okunur, böylece çözücüde yapılan düzeltme paketlere kendiliğinden yansır.

Kullanım: python3 scripts/cikmis_paket/paketle.py [--kurul 1]   (çözücü verisi değişince yeniden çalıştır)
"""
import argparse, hashlib, json, re, unicodedata
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
VERI = KOK / 'src' / 'data'


def anahtar(q):
    t = q['soru'] + '|' + '|'.join(q['secenekler'][h] for h in 'ABCDE')
    t = unicodedata.normalize('NFKD', t.lower())
    return re.sub(r'[^a-z0-9ğüşıöç]+', '', t)


def nkok(t):
    return re.sub(r'\W+', '', t.lower())[:90]


def asistan_dizini(brans):
    """kök → (asistan kodu, nokta id); ders kodu → {nokta id: nokta}"""
    kok, noktalar = {}, {}
    for f in sorted((VERI / f'{brans}_asistan').glob('*.json')):
        a = json.loads(f.read_text())
        if 'noktalar' not in a:
            continue
        noktalar[a['kod']] = {p['id']: p for p in a['noktalar'] if f"a-{p['id']}" in a.get('klip', {})}
        for p in a['noktalar']:
            if p['id'] not in noktalar[a['kod']]:
                continue
            for q in p.get('sorular') or []:
                if isinstance(q, dict) and q.get('kok'):
                    kok.setdefault(nkok(q['kok']), (a['kod'], p['id']))
    return kok, noktalar


def not_bul(brans, klasor, q, kok, noktalar):
    """→ ([tür, ders, id], yöntem); tür a = asistan noktası (EMA sesli), o = yalnız önem maddesi (sessiz, metin)"""
    h = kok.get(nkok(q['soru']))
    if h:
        return ['a', *h], 'soru'
    onem = VERI / f'{brans}_onem' / f'{klasor}.json'
    if not onem.exists():
        return None, None
    np = noktalar.get(klasor) or {}
    sayfa = set(q.get('sayfa') or [])
    en = None
    for m in json.loads(onem.read_text()).get('maddeler', []):
        ort = len(sayfa & {x.get('sayfa') for x in m.get('alinti') or []})
        if ort and (en is None or (ort, m['id'] in np, m.get('puan', 0)) > en[0]):
            en = ((ort, m['id'] in np, m.get('puan', 0)), m['id'])
    if not en or en[1] not in np:
        return None, None
    return (['a', klasor, en[1]], 'sayfa')


def kur(kurul: int):
    dag = json.loads((VERI / 'sinav_dagilimi.json').read_text())['kurullar'][str(kurul)]
    cikti = {'kurul': kurul, 'aciklama': 'scripts/cikmis_paket/paketle.py üretir; elle yazılmaz', 'branslar': []}
    for brans, n in dag['branslar'].items():
        klasor = VERI / f'{brans}_cozucu'
        if not (klasor / 'index.json').exists():
            print(f'  {brans}: çözücü verisi yok, atlandı')
            continue
        dizin = json.loads((klasor / 'index.json').read_text())
        gorulen, dersler, atlanan = set(), [], 0
        kok, noktalar = asistan_dizini(brans)
        yontem = {'soru': 0, 'sayfa': 0, 'yazili': 0, None: 0}
        yazili = json.loads((Path(__file__).parent / 'notlar.json').read_text())
        notlar = {}
        for d in dizin['dersler']:
            x = json.loads((klasor / f"{d['kod']}.json").read_text())
            l = []
            for q in x['sorular']:
                if q.get('tur') != 'cikmis':
                    continue
                if not q.get('sayfa') or f"q-{q['no']}" not in x.get('klip', {}):
                    atlanan += 1
                    continue
                a = anahtar(q)
                if a in gorulen:
                    continue
                gorulen.add(a)
                kl = x.get('klasor') or d['kod']
                nt, y = not_bul(brans, kl, q, kok, noktalar)
                yz = yazili.get(f"{brans}/{d['kod']}/{q['no']}")
                if not nt and yz:
                    kay = json.loads((KOK / 'data' / f'{brans}_cozucu' / 'ses' / kl / 'kayit.json').read_text()).get(f"n-{q['no']}")
                    notlar[f"{d['kod']}/{q['no']}"] = {'baslik': yz['baslik'], 'cumleler': yz['cumleler'], 'sayfa': yz.get('kaynak_sayfa', []),
                                                      **({'klip': {'v': kay['h'], 'sure': kay['sure'], 'zaman': kay['zaman']}} if kay else {})}
                    nt, y = ['y'], 'yazili'
                yontem[y] += 1
                l.append([d['kod'], q['no'], *(nt or [])])  # [kod, no, tür, ders, id]
            if l:
                dersler.append(l)
        toplam = sum(len(l) for l in dersler)
        if not toplam:
            continue
        sira = []  # round-robin
        while any(dersler):
            for l in dersler:
                if l:
                    sira.append(l.pop(0))
        paket_say = -(-toplam // n)
        kovalar = [[] for _ in range(paket_say)]
        for i, r in enumerate(sira):
            kovalar[i // n].append(r)
        # paket içinde ders sırası
        ders_sira = {d['kod']: i for i, d in enumerate(dizin['dersler'])}
        paketler = []
        for i, k in enumerate(kovalar, 1):
            k.sort(key=lambda r: (ders_sira[r[0]], r[1]))
            paketler.append({'no': i, 'sorular': k, 'ders': len({r[0] for r in k})})
        cikti['branslar'].append({'brans': brans, 'sinavSoru': n, 'soru': toplam, 'paketler': paketler, 'notlar': notlar})
        print(f'  {brans}: {toplam} çıkmış → {paket_say} paket × {n} (son {len(kovalar[-1])}); atlanan {atlanan}; not: soru {yontem['soru']}, sayfa {yontem['sayfa']}, yazılı {yontem['yazili']}, yok {yontem[None]}')
    ham = json.dumps(cikti, ensure_ascii=False, separators=(',', ':'))
    cikti['surum'] = hashlib.sha1(ham.encode()).hexdigest()[:10]
    yol = VERI / 'cikmis_paket' / f'k{kurul}.json'
    yol.parent.mkdir(exist_ok=True)
    yol.write_text(json.dumps(cikti, ensure_ascii=False, separators=(',', ':')) + '\n')
    print(f'→ {yol.relative_to(KOK)}')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--kurul', type=int, default=None)
    a = ap.parse_args()
    kurullar = [a.kurul] if a.kurul else [int(k) for k in json.loads((VERI / 'sinav_dagilimi.json').read_text())['kurullar']]
    for k in kurullar:
        print(f'Kurul {k}')
        kur(k)
