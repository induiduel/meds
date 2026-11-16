#!/usr/bin/env python3
"""Tıp Asistanı F0: tüm kaynakları tek belge şemasına çevirir (salt okur, LLM/GPU yok).

Çıktı: meds_temp/asistan/belgeler.jsonl  +  envanter_rapor.json
Belge: {id, tur, baslik, metin, ders, kurul, brans, url, kaynak, meta}
Çalıştır: python3 meds/scripts/asistan/kaynaklar.py
"""
import json, os, re, sys, hashlib, collections
# Konum-bağımsız kök: scripts/ kökünü sys.path'e ekler (deste_deposu için; HARITA.md kalıbı).
import sys as _sys
from pathlib import Path as _Path
_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import deste_deposu as dd  # noqa: E402
KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SD = os.path.join(KOK, 'src', 'data')
DD = os.path.join(KOK, 'data')
CIKTI = os.path.join(KOK, '..', 'meds_temp', 'asistan')
K1_SLUG = {'patoloji': 'patoloji', 'enfeksiyon': 'enfeksiyon', 'uroloji': 'uroloji', 'genetik': 'tbg',
           'halksagligi': 'halk-sagligi', 'kadindogum': 'kadin-dogum', 'farmakoloji': 'farmakoloji'}

def yukle(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)

def s(x):
    return x.strip() if isinstance(x, str) else ''

def birles(*parcalar):
    return '\n'.join(p for p in (s(x) for x in parcalar) if p)

def brans_adres(dizin):
    """patoloji_onem → (1,'patoloji'); k2noroloji_onem → (2,'noroloji')"""
    ad = re.sub(r'_(onem|asistan|cozucu|cozucu_alt)$', '', dizin)
    m = re.match(r'^k(\d)([a-z0-9]+)$', ad)
    if m:
        return int(m.group(1)), m.group(2)
    return 1, K1_SLUG.get(ad, ad)

def belge(tur, kimlik, baslik, metin, url, kaynak, ders='', kurul=None, brans='', **meta):
    metin = s(metin)
    if kurul is not None and not isinstance(kurul, int):
        meta['kurul_ham'] = kurul
        kurul = int(kurul) if isinstance(kurul, str) and kurul.isdigit() else None
    return {'id': f'{tur}:{kimlik}', 'tur': tur, 'baslik': s(baslik), 'metin': metin, 'ders': ders,
            'kurul': kurul, 'brans': brans, 'url': url, 'kaynak': kaynak, 'meta': meta}

def sik_metin(d):
    return '; '.join(f'{k}) {v}' for k, v in d.items()) if isinstance(d, dict) else ''

def ders_icerik():
    d = os.path.join(SD, 'ders_icerik')
    for fn in sorted(os.listdir(d)):
        if not fn.endswith('.json'): continue
        n = yukle(os.path.join(d, fn)); key = n.get('key') or fn[:-5]
        m = re.match(r'^k(\d)-', key); kurul = int(m.group(1)) if m else None
        url = f'/dersler/ders/kurul{kurul}/{key}'; kay = f'src/data/ders_icerik/{fn}'
        ortak = dict(ders=n.get('baslik', ''), kurul=kurul, url=url, kaynak=kay)
        yield belge('ders_ozet', key, n.get('baslik'), n.get('ozet'), **ortak)
        for i, t in enumerate(n.get('terimler', [])):
            yield belge('terim', f'{key}:{i}', t.get('t'), birles(t.get('a'), t.get('i'), ', '.join(t.get('e') or [])), sayfa=t.get('s'), adim=t.get('adim'), **ortak)
        for i, t in enumerate(n.get('kisaltmalar', [])):
            yield belge('kisaltma', f'{key}:{i}', t.get('k'), t.get('acilim'), adim=t.get('adim'), **ortak)
        for i, t in enumerate(n.get('bilgiler', [])):
            yield belge('bilgi', f'{key}:{i}', t.get('b'), t.get('m'), sayfa=t.get('s'), alt=t.get('tur'), adim=t.get('adim'), **ortak)
        for i, h in enumerate(n.get('hastaliklar', [])):
            govde = []
            for b in h.get('bolumler', []):
                govde.append(s(b.get('b')) + ': ' + ' '.join(s(x.get('m')) for x in b.get('m', []) if isinstance(x, dict)))
            yield belge('hastalik_karti', f"{key}:{h.get('id', i)}", birles(h.get('ad'), h.get('latin')), '\n'.join(govde), sayfa=h.get('s'), adim=h.get('adim'), latin=h.get('latin'), **ortak)
        for i, t in enumerate(n.get('onemli', [])):
            yield belge('onemli', f'{key}:{i}', t.get('b'), birles(t.get('m'), *(t.get('alt') or []), t.get('n')), puan=t.get('p'), sayfa=t.get('s'), adim=t.get('adim'), **ortak)
        for i, t in enumerate(n.get('spotlar', [])):
            yield belge('spot', f'{key}:{i}', t.get('bolum'), t.get('m'), adim=t.get('adim'), **ortak)
        for i, t in enumerate(n.get('tablolar', [])):
            satir = [' | '.join(map(str, t.get('h', [])))] + [' | '.join(map(str, r)) for r in t.get('r', [])]
            yield belge('tablo', f'{key}:{i}', t.get('t'), '\n'.join(satir), adim=t.get('adim'), **ortak)
        for i, t in enumerate(n.get('listeler', [])):
            yield belge('liste', f'{key}:{i}', t.get('t'), '\n'.join(s(x.get('m')) if isinstance(x, dict) else s(x) for x in t.get('m', [])), sira=t.get('sira'), adim=t.get('adim'), **ortak)
        for i, t in enumerate(n.get('kartlar', [])):
            yield belge('kart', f'{key}:{i}', t.get('o'), birles(t.get('a'), t.get('c')), adim=t.get('adim'), **ortak)
        for i, t in enumerate(n.get('quiz', [])):
            dogru = [o for o in t.get('o', []) if o.get('d')]
            yield belge('mini_soru', f'{key}:{i}', t.get('q'), birles(*(f"{o.get('k')}) {o.get('t')}" for o in t.get('o', [])), 'Doğru: ' + ', '.join(f"{o.get('k')}) {o.get('t')}" for o in dogru), *(o.get('a') for o in dogru)), adim=t.get('adim'), **ortak)

def onem():
    for dizin in sorted(os.listdir(SD)):
        if not dizin.endswith('_onem'): continue
        kurul, slug = brans_adres(dizin)
        for fn in sorted(os.listdir(os.path.join(SD, dizin))):
            if not re.match(r'^\w+\.json$', fn) or fn == 'index.json': continue
            n = yukle(os.path.join(SD, dizin, fn))
            if not isinstance(n, dict) or 'maddeler' not in n: continue
            url = f'/kamplar/kurul{kurul}/en-onemliler/{slug}'; kay = f'src/data/{dizin}/{fn}'
            ders = n.get('baslik', ''); kod = f"{dizin}/{n.get('kod', fn[:-5])}"
            yield belge('onem_ozet', kod, ders, birles(n.get('ozet'), n.get('neden_onemli')), url, kay, ders, kurul, slug)
            for md in n['maddeler']:
                cik = md.get('cikmis') or []
                yield belge('onem_maddesi', f"{kod}:{md.get('id')}", md.get('baslik'),
                            birles(md.get('bilgi'), *(md.get('alt') or []), md.get('detay'), md.get('neden')),
                            url, kay, ders, kurul, slug, puan=md.get('puan'), cikmis_sayisi=len(cik), tur_=md.get('tur'))
                oq = md.get('ornek_soru')
                if isinstance(oq, dict) and oq:
                    yield belge('onem_ornek_soru', f"{kod}:{md.get('id')}", oq.get('kok') or oq.get('soru') or md.get('baslik'),
                                birles(oq.get('kok') or oq.get('soru'), sik_metin(oq.get('secenekler')), 'Doğru: ' + s(oq.get('dogru')), oq.get('aciklama') or oq.get('cozum')),
                                url, kay, ders, kurul, slug)

def asistan():
    for dizin in sorted(os.listdir(SD)):
        if not dizin.endswith('_asistan'): continue
        kurul, slug = brans_adres(dizin)
        for fn in sorted(os.listdir(os.path.join(SD, dizin))):
            if not re.match(r'^\w+\.json$', fn) or fn == 'index.json': continue
            n = yukle(os.path.join(SD, dizin, fn))
            if not isinstance(n, dict) or 'noktalar' not in n: continue
            url = f'/kamplar/kurul{kurul}/en-onemliler/{slug}'; kod = f"{dizin}/{n.get('kod', fn[:-5])}"
            for nk in n['noktalar']:
                yield belge('asistan_nokta', f"{kod}:{nk.get('id')}", nk.get('baslik'), birles(nk.get('bilgi'), *(nk.get('cumleler') or [])), url, f'src/data/{dizin}/{fn}', n.get('baslik', ''), kurul, slug, kategori=nk.get('kategori'), ses=bool(n.get('klip')))

def cozucu():
    for dizin in sorted(os.listdir(SD)):
        if not re.search(r'_cozucu(_alt)?$', dizin): continue
        kurul, slug = brans_adres(dizin)
        for fn in sorted(os.listdir(os.path.join(SD, dizin))):
            if not re.match(r'^\w+\.json$', fn) or fn == 'index.json': continue
            n = yukle(os.path.join(SD, dizin, fn))
            if not isinstance(n, dict) or 'sorular' not in n: continue
            kod = n.get('kod', fn[:-5])
            url = f'/sorular/soru-cozucu/kurul{kurul}/{slug}?ders={kod}'
            for q in n['sorular']:
                sk = q.get('siklar') if isinstance(q.get('siklar'), dict) else {}
                yield belge('cozucu_sorusu', f"{dizin}/{kod}:{q.get('no')}", q.get('soru'),
                            birles(q.get('soru'), sik_metin(q.get('secenekler')), 'Doğru: ' + s(q.get('dogru')), q.get('cozum'), *(f'{k}: {v}' for k, v in sk.items())),
                            f"{url}&coz={q.get('no')}", f'src/data/{dizin}/{fn}', n.get('baslik', ''), kurul, slug, zorluk=q.get('zorluk'), sayfa=q.get('sayfa'), ses=f"q-{q.get('no')}" in (n.get('klip') or {}))

def cikmis():
    for q in yukle(os.path.join(SD, 'pastQuestions.json')):
        r = q.get('reconstruction') or {}
        sk = q.get('options') or r.get('options') or []
        sk = '; '.join(f"{o.get('label', chr(65+i))}) {o.get('text', o)}" if isinstance(o, dict) else f'{chr(65+i)}) {o}' for i, o in enumerate(sk))
        yield belge('cikmis_soru', q['id'], q.get('topic'), birles(q.get('stem') or r.get('stem'), sk, 'Doğru: ' + s(q.get('correctAnswer')), q.get('explanation') or r.get('explanation')),
                    f"/sorular/cikmis/{q['id']}", 'src/data/pastQuestions.json', q.get('discipline', ''), q.get('kurul'), '', yil=q.get('examYear'), committee=q.get('committeeId'))

def ornek_sorular():
    for k in ('k1', 'k2'):
        d = os.path.join(SD, 'ornek_sorular', k)
        if not os.path.isdir(d): continue
        for fn in sorted(os.listdir(d)):
            if fn == 'index.json' or not fn.endswith('.json'): continue
            n = yukle(os.path.join(d, fn))
            for kz in n.get('kazanimlar', []):
                for q in kz.get('sorular', []):
                    yield belge('ornek_soru', q.get('id'), q.get('soru'),
                                birles(q.get('soru'), sik_metin(q.get('secenekler')), 'Doğru: ' + s(q.get('dogru')), q.get('aciklama') or q.get('cozum'), 'Kazanım: ' + s(kz.get('metin'))),
                                '/sorular/ornek', f'src/data/ornek_sorular/{k}/{fn}', n.get('konu', ''), int(k[1]), n.get('ders', ''), zorluk=q.get('zorluk'))

def sozlukler():
    for ad, kay in (('medical_glossary.json', 'sozluk'), ('terim_yardimcisi_sozluk.json', 'terim_yardimcisi'), ('kisaltma_sozluk.json', 'sozluk_kisaltma')):
        for anahtar, v in yukle(os.path.join(SD, ad)).items():
            yield belge(kay, anahtar, v.get('term'), birles(v.get('definition'), v.get('description') if v.get('description') != v.get('definition') else '', v.get('clinicalPearl'), ', '.join(v.get('aliases') or [])), '/sozluk?id=' + anahtar, f'src/data/{ad}', v.get('discipline') or v.get('ders') or '', kategori=v.get('category'))
    for h in yukle(os.path.join(SD, 'disease_entities.json')):
        yield belge('hastalik', h['id'], birles(h.get('name'), h.get('latinName')),
                    birles(h.get('definition'), h.get('morphologyOrMechanism'), h.get('differentialDiagnosis'), h.get('examSpotPearls'), h.get('pitfallsAndWarnings')),
                    f"/hastaliklar?id={h['id']}", 'src/data/disease_entities.json', h.get('discipline', ''), kategori=h.get('category'))
    for c in yukle(os.path.join(SD, 'question_cards.json')):
        yield belge('soru_karti', c['id'], c.get('front'), birles(c.get('front'), sik_metin(c.get('options')), c.get('back'), c.get('note')), '/dersler/kartlar', 'src/data/question_cards.json', c.get('group', ''), c.get('kurul'))

def dersler():
    br = {b['ad']: b for b in yukle(os.path.join(SD, 'dersler', 'branslar.json'))['branslar']}
    for k in (1, 2, 3, 4):
        p = os.path.join(SD, 'dersler', f'k{k}.json')
        if not os.path.exists(p): continue
        for d in yukle(p).get('dersler', []):
            yield belge('ders', d['id'], d.get('konu'), birles(d.get('konu'), d.get('brans'), d.get('ogretim_uyesi'), d.get('tarih')), f"/dersler/ders/kurul{d.get('kurul', k)}/{d['id']}", f'src/data/dersler/k{k}.json', d.get('konu', ''), d.get('kurul', k), d.get('brans', ''), tarih=d.get('tarih'), saat=d.get('saat'), hoca=d.get('ogretim_uyesi'))

def desteler():
    for dk in dd.hepsi():
        yield belge('deste', dk['id'], dk.get('title'), birles(dk.get('overview')), f"/dersler/interaktif/{dk['id']}", 'src/data/interactive_learning_decks.json', dk.get('discipline', ''), committee=dk.get('committee'), slayt=len(dk.get('slides') or dk.get('steps') or []))

def saglik():
    d = os.path.join(SD, 'saglik')
    for fn in sorted(os.listdir(d)):
        if not fn.endswith('.json') or fn in ('baglantilar.json', 'ders_eslesme.json'): continue
        n = yukle(os.path.join(d, fn))
        def duz(o, d=0):
            if isinstance(o, str): return [o]
            if isinstance(o, dict): return [x for v in o.values() for x in duz(v, d + 1)]
            if isinstance(o, list): return [x for v in o for x in duz(v, d + 1)]
            return []
        if isinstance(n, dict):
            for anahtar, v in n.items():
                if anahtar in ('kaynaklar', 'ek_kaynaklar', 'dogrulanamayan'): continue  # künye listeleri: cevap değil
                if isinstance(v, list) and v and isinstance(v[0], dict):
                    for i, it in enumerate(v):
                        bas = it.get('ad') or it.get('baslik') or it.get('etiket') or it.get('madde') or it.get('olay') or it.get('konu')
                        if not bas:  # başlık alanı yoksa ilk anlamlı metin
                            bas = next((x for x in duz(it) if len(x) >= 8), '')
                            bas = bas[:80]
                        if not bas: continue
                        yield belge('saglik', f'{fn[:-5]}:{anahtar}:{i}', bas, '\n'.join(x for x in duz(it) if len(x) > 1), f'/saglik/{fn[:-5]}', f'src/data/saglik/{fn}', 'Sağlık Bakanlığı', anahtar=anahtar)

def sayfalar():
    L = [('Ders çalış', '/dersler', 'ders çalış merkezi kurul seçici'), ('Etkileşimli ders (Öğren)', '/dersler/interaktif', 'öğren etkileşimli ders deste'),
         ('Sesli ders', '/dersler/canliders', 'sesli ders canlı ders dinle'), ('Ders özetleri', '/dersler/ozetler', 'özet ders özeti'),
         ('Kartlar', '/dersler/kartlar', 'flashcard kart ezber'), ('KMB görsel asistan', '/dersler/kmb', 'kmb beceri görsel asistan'),
         ('Soru çöz', '/sorular', 'soru çöz merkezi'), ('Sesli soru çözücü', '/sorular/soru-cozucu', 'soru çözücü sesli yardım al'),
         ('Çıkmış sorular', '/sorular/cikmis', 'çıkmış soru geçmiş sınav'), ('Soru havuzu', '/sorular/havuz', 'soru havuzu'),
         ('Deneme', '/sorular/deneme', 'deneme sınavı'), ('Örnek sorular', '/sorular/ornek', 'örnek soru'),
         ('Olası sorular', '/sorular/olasi', 'olası soru'), ('Soru haritası', '/sorular/soru-haritasi', 'soru haritası'),
         ('Sınava hazırlan', '/kamplar', 'sınav hazırlık kamp merkezi'), ('Son Prova', '/kamplar/kurul1/son-prova', 'son prova son tekrar'),
         ('Çıkmış çözücü', '/kamplar/kurul1/cikmis-cozucu', 'çıkmış çözücü'), ('Kurul kampı', '/kamplar/kurul1/kamp', 'kamp hoca tüyoları'),
         ('Patoloji Check Up', '/kamplar/kurul1/checkup/patoloji', 'patoloji check up tablolar'), ('TBG Sınav Kampı', '/kamplar/kurul1/checkup/tbg/v1', 'tbg genetik kamp'),
         ('En önemliler', '/kamplar/en-onemliler', 'en önemli önem listesi'), ('Spotlar', '/kamplar/spotlar', 'sınav spotları'),
         ('Sınav planı', '/kamplar/sinav-plani', 'sınav planı 60'), ('Takvim', '/kamplar/takvim', 'kurul takvimi'),
         ('Kaynaklar', '/kaynaklar', 'kaynak başvuru sözlük hastalık'), ('Sağlık Bakanlığı', '/saglik', 'sağlık bakanlığı resmi veri aşı')]
    for i, (ad, url, anah) in enumerate(L):
        yield belge('sayfa', str(i), ad, ad + ' — ' + anah, url, 'docs/SITE_HARITASI_KURALLARI.md')

KAYNAKLAR = [ders_icerik, onem, asistan, cozucu, cikmis, ornek_sorular, sozlukler, dersler, desteler, saglik, sayfalar]

def main():
    os.makedirs(CIKTI, exist_ok=True)
    sayac = collections.Counter(); bos = collections.Counter(); tekrar = []; gorulen = set(); kisa = collections.Counter(); hata = {}
    with open(os.path.join(CIKTI, 'belgeler.jsonl'), 'w', encoding='utf-8') as out:
        for fn in KAYNAKLAR:
            try:
                for b in fn():
                    if b['id'] in gorulen: tekrar.append(b['id']); continue
                    gorulen.add(b['id'])
                    sayac[b['tur']] += 1
                    if not b['metin']: bos[b['tur']] += 1; continue
                    if not b['url']: bos['url_yok:' + b['tur']] += 1
                    if len(b['metin']) < 25: kisa[b['tur']] += 1
                    out.write(json.dumps(b, ensure_ascii=False) + '\n')
            except Exception as e:
                hata[fn.__name__] = repr(e)
    rag = collections.Counter(c.get('documentType') for c in yukle(os.path.join(DD, 'local_rag_chunks.json')))
    rapor = {'belge_sayisi': dict(sayac), 'toplam': sum(sayac.values()), 'bos_metin_atlandi': dict(bos), 'cok_kisa_metin': dict(kisa),
             'tekrar_kimlik': len(tekrar), 'tekrar_ornek': tekrar[:10], 'rag_chunk_turleri': dict(rag), 'hatalar': hata}
    json.dump(rapor, open(os.path.join(CIKTI, 'envanter_rapor.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(json.dumps(rapor, ensure_ascii=False, indent=1))

if __name__ == '__main__':
    main()
