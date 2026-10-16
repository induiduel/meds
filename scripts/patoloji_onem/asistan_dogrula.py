"""Sesli sınav asistanı çıktısı doğrulayıcı: python3 dogrula.py cikti/<kod>.json [...] → HATA sayısı (0 değilse çıkış 1)."""
import json, os, re, sys
W = os.path.dirname(os.path.abspath(__file__))
YASAK_SES = re.compile(r'[0-9%/→←↑↓±≈<>=+()\[\]*#_~{}@&$€£^\\]')
KISALTMA = re.compile(r'\b[A-ZÇĞİÖŞÜ]{2,}[0-9]*\b')
IC_DIL = re.compile(r"\b(aday|adaylar|plan|talimat|ipucu|pdf'?te|kaynakta)\b", re.I)
KARISIK = re.compile(r"\b\w*[a-zçğıöşü][A-ZÇĞİÖŞÜ]\w*\b")  # IgG, mRNA gibi karışık harfli kısaltma
kelime = lambda s: len(re.findall(r'\w+', s))


def cift(e, yer, x, enaz=1, encok=40):
    if not isinstance(x, dict) or not isinstance(x.get('metin'), str) or not isinstance(x.get('ses'), str):
        e.append(f'{yer}: {{metin, ses}} olmalı'); return
    m, s = x['metin'].strip(), x['ses'].strip()
    if not m or not s: e.append(f'{yer}: boş'); return
    if YASAK_SES.search(s.replace('||', '').replace('|', '')): e.append(f'{yer}: ses yasak karakter içeriyor: {YASAK_SES.search(s.replace("|", "")).group()!r} — {s[:60]}')
    k = [w for w in KISALTMA.findall(s) if w not in ('I',)]
    if k: e.append(f'{yer}: ses büyük harfli kısaltma içeriyor (harfle yaz): {k[:3]}')
    if KARISIK.findall(s): e.append(f'{yer}: ses karışık harfli kısaltma içeriyor (harfle yaz): {KARISIK.findall(s)[:3]}')
    for cm in re.split(r'(?<=[.!?])\s+', s.replace('||', ' ').replace('|', ' ')):
        if kelime(cm) > 28: e.append(f'{yer}: ses cümlesi {kelime(cm)} kelime (en çok 25; ikiye böl)'); break
    if IC_DIL.search(m) or IC_DIL.search(s): e.append(f'{yer}: iç süreç dili: {(IC_DIL.search(m) or IC_DIL.search(s)).group()!r}')
    if '(' in m or ')' in m: e.append(f'{yer}: metin parantez içeriyor')
    if s.count('|') > 4: e.append(f'{yer}: durak işareti çok')
    if not enaz <= kelime(s) <= encok: e.append(f'{yer}: ses {kelime(s)} kelime ({enaz}–{encok})')
    r = kelime(s) / max(1, kelime(m.replace('**', '')))
    if not 0.6 <= r <= 2.6: e.append(f'{yer}: metin ile ses uzunluğu uyumsuz (oran {r:.2f}) — aynı içerik olmalı')


te = tu = 0
for p in sys.argv[1:]:
    e, u = [], []
    o = json.load(open(p)); kod = o.get('kod')
    pp = f'{W}/plan/{kod}.json'
    if not os.path.exists(pp): print('HATA', p, 'plan yok'); te += 1; continue
    plan = json.load(open(pp))
    pdf = open(f'{W}/../pdf_metin/{kod}.md', encoding='utf-8').read()
    pdf_sayilar = set(re.findall(r'\d+(?:[.,]\d+)?', pdf))
    plan_metin = json.dumps(plan, ensure_ascii=False)
    for i, x in enumerate(o.get('giris') or []): cift(e, f'giris[{i}]', x, 4, 45)
    if not 1 <= len(o.get('giris') or []) <= 2: e.append('giris 1–2 cümle olmalı')
    for i, x in enumerate(o.get('kapanis') or []): cift(e, f'kapanis[{i}]', x, 4, 45)
    if not 2 <= len(o.get('kapanis') or []) <= 3: e.append('kapanis 2–3 cümle olmalı')
    A = o.get('adimlar') or []
    if [a.get('id') for a in A] != [a['id'] for a in plan['adimlar']]: e.append('adimlar plandaki id/sıra ile aynı olmalı')
    for a, pa in zip(A, plan['adimlar']):
        y = a.get('id')
        if not a.get('baslik') or kelime(a['baslik']) > 8: e.append(f'{y}: baslik 1–8 kelime')
        C = a.get('cumleler') or []
        if not 2 <= len(C) <= 5: e.append(f'{y}: cumleler 2–5 ({len(C)})')
        for j, c in enumerate(C): cift(e, f'{y}.cumle[{j}]', c, 3, 40)
        top = sum(kelime(c.get('ses', '')) for c in C if isinstance(c, dict))
        if not 25 <= top <= 92: e.append(f'{y}: anlatım {top} kelime (25–90)')
        for c in C:
            for n in re.findall(r'\d+(?:[.,]\d+)?', c.get('metin', '') if isinstance(c, dict) else ''):
                if n not in pdf_sayilar and n not in plan_metin: e.append(f'{y}: sayı {n} PDF/planda yok')
        ps, s = pa.get('soru'), a.get('soru')
        if ps and not s: e.append(f'{y}: planda soru var, çıktıda yok')
        if s and not ps: e.append(f'{y}: planda soru yok')
        if ps and s:
            if not isinstance(s.get('kok_ses'), str) or not s['kok_ses'].strip(): e.append(f'{y}: kok_ses yok')
            else:
                ks = s['kok_ses']
                if YASAK_SES.search(ks.replace('|', '')): e.append(f'{y}: kok_ses yasak karakter: {YASAK_SES.search(ks.replace("|", "")).group()!r}')
                if KISALTMA.findall(ks): e.append(f'{y}: kok_ses kısaltma: {KISALTMA.findall(ks)[:3]}')
            cift(e, f'{y}.dogru', s.get('dogru'), 3, 32)
            if isinstance(s.get('dogru'), dict) and not str(s['dogru'].get('metin', '')).startswith('Doğru'): e.append(f'{y}.dogru: "Doğru" ile başlamalı')
            beklenen = sorted(k for k in ps['secenekler'] if k != ps['dogru'])
            Y = s.get('yanlis') or {}
            if sorted(Y) != beklenen: e.append(f'{y}: yanlis şıkları {sorted(Y)} ≠ {beklenen}')
            for k, v in Y.items():
                cift(e, f'{y}.yanlis.{k}', v, 12, 72)
                if isinstance(v, dict) and 'Doğrusu' not in v.get('metin', '') and 'doğrusu' not in v.get('metin', ''): e.append(f'{y}.yanlis.{k}: "Doğrusu:" kalıbı yok')
                for n in re.findall(r'\d+(?:[.,]\d+)?', v.get('metin', '') if isinstance(v, dict) else ''):
                    if n not in pdf_sayilar and n not in plan_metin: u.append(f'{y}.yanlis.{k}: sayı {n} PDF/planda yok')
            metinler = [v.get('metin', '') for v in Y.values() if isinstance(v, dict)]
            if len(set(m[:40] for m in metinler)) < len(metinler): e.append(f'{y}: yanlış açıklamaları birbirinin tekrarı')
    for x in e: print('HATA', kod, x)
    for x in u[:8]: print('UYARI', kod, x)
    te += len(e); tu += len(u)
print(te, 'HATA', tu, 'UYARI'); sys.exit(1 if te else 0)
