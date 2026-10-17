#!/usr/bin/env python3
"""Spot bilgiler (önem listesi) + örnek sorular + çıkmış seçimi doğrulayıcısı (TALIMAT_ONEM.md).
Kullanım: python3 meds/scripts/spot_cozucu/onem_dogrula.py meds_temp/spot_cozucu/<brans>/onem/<kod>.json [...]
Denetim: şema, puan/bant dağılımı, alıntının PDF sayfasında birebir geçmesi, sayıların PDF'te geçmesi, her çıkmış temsilcisinin kararı,
örnek soru sayısı/biçimi/zorluk dağılımı/harf dengesi, örnek–örnek ve örnek–çıkmış benzerliği (tekrar soru)."""
import collections, json, os, re, sys, unicodedata
from pathlib import Path

TUR = {'tanim', 'en_sik', 'karakteristik', 'sayi', 'eslesme', 'mekanizma', 'siniflama', 'tuzak', 'tani_tedavi'}
ELEN = re.compile(r'^(pdf_disi|anahtar_celiskili|gorsel|belirsiz|tekrar:\S+)$')
IC_DIL = re.compile(r"\b(aday\w*|bağlan\w*|eşlen\w*|pdf'?te yok|talimat\w*|ajan\w*)\b", re.I)
DUR = set('aşağıdakilerden aşağıdaki hangisi hangisidir hangileri değildir olan olarak için ile veya daha çok sıklıkla genellikle '
          'en sık olası doğru yanlış hastada hasta yaşında hangisinde bulunur görülür yer almaz almaz'.split())


def norm(s):
    s = unicodedata.normalize('NFKC', str(s or '')).replace('İ', 'i').replace('I', 'ı').lower()
    s = re.sub(r'[•●▪–—\-►➢✓*_`"“”‘’\'()\[\]{}:;,.!?/]', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def words(s): return len(re.findall(r'\w+', str(s or '')))
def nums(s): return set(re.findall(r'\d+(?:[.,]\d+)?', re.sub(r'\*\*', '', str(s or ''))))
def kok5(w): return w.replace('İ', 'i').replace('I', 'ı').lower()[:5]
def kokler(s): return {kok5(w) for w in re.findall(r'\w{4,}', str(s or '')) if w.lower() not in DUR}


def benzer(a, b):
    return len(a & b) / max(1, min(len(a), len(b))) if a and b else 0


def soru_imza(kok, sec, dogru):
    return kokler(kok + ' ' + (sec or {}).get(dogru, ''))


def check(path):
    e, w = [], []
    path = Path(path).resolve()
    W = path.parent.parent
    d = json.load(open(path)); kod = d.get('kod') or path.stem
    pm = W / 'pdf_metin' / f'{kod}.md'
    if not pm.exists(): return [f'{kod}: pdf_metin yok'], [], {}
    t = pm.read_text(encoding='utf-8')
    parts = re.split(r'\n=== SAYFA (\d+) ===\n', t)
    P = {int(parts[i]): norm(parts[i + 1]) for i in range(1, len(parts) - 1, 2)}
    ALL = norm(t); allraw = re.sub(r'\s+', ' ', t); maxs = max(P)
    g = json.load(open(W / 'girdi' / f'{kod}.json'))
    C = {c['id']: c for c in json.load(open(W / 'cikmis' / f'{kod}.json'))} if (W / 'cikmis' / f'{kod}.json').exists() else {}
    tum_cikmis = dict(C)
    for c in list(C.values()):
        for r in c.get('tekrar') or []: tum_cikmis.setdefault(r['id'], c)
    for k in ('baslik', 'pdf', 'ozet', 'neden_onemli'):
        if words(d.get(k)) < (1 if k in ('baslik', 'pdf') else 8): e.append(f'{kod}: {k} eksik/kısa')
    for k in ('ozet', 'neden_onemli'):
        if IC_DIL.search(str(d.get(k) or '')): e.append(f'{kod}: {k} iç süreç dili: {IC_DIL.search(d[k]).group()!r}')
    M = d.get('maddeler') or []
    if not 20 <= len(M) <= 45: e.append(f'{kod}: madde sayısı {len(M)} (20–45)')
    bant, ids, kullanilan, ornekler = {}, set(), collections.Counter(), []
    for m in M:
        tt = f"{kod}/{m.get('id')}"
        if not re.match(rf'^{re.escape(kod)}-\d{{2}}$', str(m.get('id'))): e.append(f'{tt}: id "<kod>-NN" biçiminde olmalı')
        if m.get('id') in ids: e.append(f'{tt}: id tekrar')
        ids.add(m.get('id'))
        p = m.get('puan')
        if not isinstance(p, int) or not 0 <= p <= 100: e.append(f'{tt}: puan 0–100 tamsayı olmalı'); continue
        b = min(p // 10, 9); bant[b] = bant.get(b, 0) + 1
        if m.get('tur') not in TUR: e.append(f'{tt}: tur geçersiz {m.get("tur")!r}')
        if not 1 <= words(m.get('baslik')) <= 10: e.append(f'{tt}: baslik 1–10 kelime')
        bw = words(m.get('bilgi'))
        if bw < 4 or bw > 30: e.append(f'{tt}: bilgi {bw} kelime (4–30, tek cümle)')
        alt = m.get('alt') or []
        if not isinstance(alt, list) or len(alt) > 4 or any(words(x) > 20 for x in alt): e.append(f'{tt}: alt en çok 4 madde, her biri ≤20 kelime')
        for n in nums(m.get('bilgi')) | set().union(*[nums(x) for x in alt] or [set()]):
            if n not in allraw and n.replace(',', '.') not in allraw and n.replace('.', ',') not in allraw: e.append(f'{tt}: "{n}" sayısı PDF metninde yok')
        for n in nums(m.get('detay')):
            if n not in allraw and n.replace(',', '.') not in allraw and n.replace('.', ',') not in allraw: w.append(f'{tt}: detayda "{n}" sayısı PDF metninde yok')
        al = m.get('alinti') or []
        if not 1 <= len(al) <= 3: e.append(f'{tt}: alinti 1–3 öge')
        for a in al:
            s, mt = a.get('sayfa'), norm(a.get('metin'))
            if words(a.get('metin')) < 3: e.append(f'{tt}: alıntı çok kısa'); continue
            if not any(mt in P.get(x, '') for x in (s, (s or 0) - 1, (s or 0) + 1)):
                if mt in ALL: w.append(f"{tt}: alıntı PDF'te var ama sayfa {s} yanlış")
                else: e.append(f"{tt}: alıntı PDF'te birebir yok: {str(a.get('metin'))[:70]!r}")
        if words(m.get('neden')) < 4: e.append(f'{tt}: neden eksik')
        for k in ('bilgi', 'neden', 'detay'):
            if IC_DIL.search(str(m.get(k) or '')): e.append(f'{tt}: {k} iç süreç dili: {IC_DIL.search(m[k]).group()!r}')
        dw = words(m.get('detay'))
        if dw < 40 or dw > 260: e.append(f'{tt}: detay {dw} kelime (60–250)')
        for c in m.get('cikmis') or []:
            if c not in C: e.append(f'{tt}: cikmis {c} temsilci listesinde yok' + (' (tekrar kopyası — temsilci kimliğini yaz)' if c in tum_cikmis else ''))
            kullanilan[c] += 1
        for i, q in enumerate(m.get('ornek') or [], 1):
            y = f'{tt}.ornek{i}'
            sec = q.get('secenekler') or {}
            if sorted(sec) != list('ABCDE') or len({norm(v) for v in sec.values()}) < 5: e.append(f'{y}: 5 farklı şık (A–E)'); continue
            if q.get('dogru') not in sec: e.append(f'{y}: dogru geçersiz'); continue
            if not str(q.get('kok', '')).strip().endswith('?'): e.append(f'{y}: kök ? ile bitmeli')
            if q.get('zorluk') not in ('kolay', 'orta', 'zor'): e.append(f'{y}: zorluk kolay|orta|zor')
            if words(q.get('aciklama')) < 8: e.append(f'{y}: aciklama kısa')
            sy = q.get('sayfa')
            if not isinstance(sy, list) or not sy or not all(isinstance(x, int) and 1 <= x <= maxs for x in sy): e.append(f'{y}: sayfa listesi geçersiz (1–{maxs})')
            if any(words(v) > 14 for v in sec.values()): w.append(f'{y}: şık uzun (>14 kelime)')
            for n in nums(sec[q['dogru']]):
                if n not in allraw and n.replace(',', '.') not in allraw: e.append(f'{y}: doğru şıktaki "{n}" PDF metninde yok')
            ornekler.append((y, q))
        if len(m.get('ornek') or []) > 2: e.append(f'{tt}: bir maddede en çok 2 örnek soru')
    # bantlar
    if not 4 <= bant.get(9, 0) <= 8: e.append(f'{kod}: 90–100 bandında {bant.get(9, 0)} madde (4–8)')
    for b in (8, 7, 6, 5):
        if bant.get(b, 0) < 2: e.append(f'{kod}: {b*10}–{b*10+9} bandında {bant.get(b, 0)} madde (en az 2)')
    # çıkmış kararları
    el = {}
    for x in d.get('elenen_cikmis') or []:
        if x.get('id') not in C: e.append(f"elenen {x.get('id')}: temsilci listesinde yok"); continue
        if not ELEN.match(str(x.get('neden'))): e.append(f"elenen {x['id']}: neden geçersiz {x.get('neden')!r}")
        if str(x.get('neden')).startswith('tekrar:') and x['neden'][7:] not in C: e.append(f"elenen {x['id']}: tekrar edilen {x['neden'][7:]} temsilci değil")
        if words(x.get('not')) < 3 and x.get('neden') != 'gorsel': e.append(f"elenen {x['id']}: not (gerekçe) eksik")
        el[x['id']] = x
    for c in C:
        if c in el and kullanilan[c]: e.append(f'çıkmış {c}: hem kullanılmış hem elenmiş')
        if c not in el and not kullanilan[c]: e.append(f'çıkmış {c}: karar yok (bir maddeye bağla ya da elenen_cikmis\'e yaz)')
        if kullanilan[c] > 2: e.append(f'çıkmış {c}: {kullanilan[c]} maddeye bağlı (en çok 2)')
    nk = sum(1 for c in C if kullanilan[c])
    # örnek sayısı, zorluk, harf
    no = len(ornekler)
    alt_s, ust_s = max(g['ornek_hedef'], 20 - nk), g['ornek_hedef'] + 6
    if not alt_s <= no <= ust_s: e.append(f'{kod}: örnek soru {no} (beklenen {alt_s}–{ust_s}; kullanılan çıkmış {nk})')
    if no:
        z = collections.Counter(q.get('zorluk') for _, q in ornekler)
        for ad, a, b in (('kolay', .15, .25), ('orta', .50, .65), ('zor', .15, .25)):
            r = z.get(ad, 0) / no
            if r < a - 0.06 or r > b + 0.06: e.append(f'{kod}: zorluk {ad} %{r*100:.0f} (hedef %{a*100:.0f}–{b*100:.0f}) {dict(z)}')
            elif not a <= r <= b: w.append(f'{kod}: zorluk {ad} %{r*100:.0f} sınırda (hedef %{a*100:.0f}–{b*100:.0f})')
        h = collections.Counter(q['dogru'] for _, q in ornekler)
        if max(h.values()) > max(2, no * 0.35): e.append(f'{kod}: örnek sorularda doğru harf dağılımı dengesiz {dict(h)}')
    # tekrar soru: örnek–örnek ve örnek–çıkmış (tüm çıkmış kopyaları dahil)
    cimza = [(cid, soru_imza(c['kok'], c['secenekler'], c['dogru'])) for cid, c in C.items()]
    gor = []
    for y, q in ornekler:
        im = soru_imza(q['kok'], q['secenekler'], q['dogru'])
        for y2, im2 in gor:
            s = benzer(im, im2)
            if s >= 0.8: e.append(f'{y}: {y2} ile aynı soru gibi (benzerlik {s:.2f})')
            elif s >= 0.6: w.append(f'{y}: {y2} ile benzer (benzerlik {s:.2f}) — aynı bilgiyi mi soruyor?')
        for cid, im2 in cimza:
            s = benzer(im, im2)
            if s >= 0.8: e.append(f'{y}: çıkmış {cid} ile aynı soru gibi (benzerlik {s:.2f})')
            elif s >= 0.6: w.append(f'{y}: çıkmış {cid} ile benzer (benzerlik {s:.2f}) — aynı bilgiyi mi soruyor?')
        gor.append((y, im))
    return e, w, {'madde': len(M), 'ornek': no, 'cikmis': nk, 'elenen': len(el)}


if __name__ == '__main__':
    te = tw = 0
    for p in sys.argv[1:]:
        e, w, s = check(p); te += len(e); tw += len(w)
        for x in e: print('HATA ', x)
        for x in w: print('UYARI', x)
        print(f'{Path(p).stem}: {s} · {len(e)} HATA · {len(w)} UYARI')
    print(f'TOPLAM {te} HATA · {tw} UYARI'); sys.exit(1 if te else 0)
