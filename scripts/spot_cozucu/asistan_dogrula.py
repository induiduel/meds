"""Sesli sınav asistanı (branş geneli) doğrulayıcı — patoloji asistan v2 kurallarıyla aynı.
Kullanım: python3 asistan_dogrula.py meds_temp/spot_cozucu/<brans>/asistan/cikti/<kod>.json [...] → HATA sayısı (0 değilse çıkış 1).
Plan: aynı klasörün ../plan/<kod>.json; PDF metni: ../../pdf_metin/<kod>.md.
"""
import json, os, re, sys
# cümle sınırı: "8-10. haftalar" gibi sıra sayısı noktası cümle sonu sayılmaz (2026-10-24, H36)
CUMLE_SINIRI = re.compile(r'(?<=[.!?])(?<!\d\.)\s+|(?<=\d\.)\s+(?=[A-ZÇĞİÖŞÜ])')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from turkce_uslup import denetle as uslup_denetle  # noqa: E402  (meds/docs/TURKCE_USLUP_STANDARDI.md)
from sik_aciklama import denetle as sik_denetle  # noqa: E402  (meds/docs/SIK_ACIKLAMA_STANDARDI.md)
YASAK_SES = re.compile(r'[0-9%/→←↑↓±≈<>=+()\[\]*#_~{}@&$€£^\\]')
KISALTMA = re.compile(r'\b[A-ZÇĞİÖŞÜ]{2,}[0-9]*\b')
KARISIK = re.compile(r"\b\w*[a-zçğıöşü][A-ZÇĞİÖŞÜ]\w*\b")
IC_DIL = re.compile(r"\b(aday|adaylar|plan|talimat|ipucu|pdf'?te|kaynakta)\b", re.I)
kelime = lambda s: len(re.findall(r'\w+', s))


def cift(e, yer, x, enaz, encok):
    if not isinstance(x, dict) or not isinstance(x.get('metin'), str) or not isinstance(x.get('ses'), str):
        e.append(f'{yer}: {{metin, ses}} olmalı'); return
    m, s = x['metin'].strip(), x['ses'].strip()
    if not m or not s: e.append(f'{yer}: boş'); return
    sd = s.replace('||', ' ').replace('|', ' ')
    if YASAK_SES.search(sd): e.append(f'{yer}: ses yasak karakter {YASAK_SES.search(sd).group()!r} — {s[:60]}')
    if KISALTMA.findall(s): e.append(f'{yer}: ses kısaltma içeriyor (harfle yaz): {KISALTMA.findall(s)[:3]}')
    if KARISIK.findall(s): e.append(f'{yer}: ses karışık harfli kısaltma: {KARISIK.findall(s)[:3]}')
    tek = re.findall(r'(?<![\wçğıöşü])[BCÇDFGHJKLMNPRSŞTVYZ](?![\wçğıöşü])', s)
    if tek: e.append(f'{yer}: ses tek harf içeriyor (harf adıyla yaz: be, ce, te…): {tek[:3]}')
    if IC_DIL.search(m) or IC_DIL.search(s): e.append(f'{yer}: iç süreç dili: {(IC_DIL.search(m) or IC_DIL.search(s)).group()!r}')
    if '(' in m or ')' in m: e.append(f'{yer}: metin parantez içeriyor')
    e.extend(uslup_denetle(m, yer))
    if s.count('|') > 4: e.append(f'{yer}: durak işareti çok')
    if not enaz <= kelime(s) <= encok: e.append(f'{yer}: ses {kelime(s)} kelime ({enaz}–{encok})')
    for cm in re.split(CUMLE_SINIRI, sd):
        if kelime(cm) > 28: e.append(f'{yer}: ses cümlesi {kelime(cm)} kelime (en çok 25; böl)'); break
    r = kelime(s) / max(1, kelime(m.replace('**', '')))
    if not 0.6 <= r <= 2.6: e.append(f'{yer}: metin ile ses uzunluğu uyumsuz (oran {r:.2f})')


def check(p):
    """Bir asistan çıktısının (e, u) hata/uyarı listeleri — CLI ile birebir aynı kurallar."""
    e, u = [], []
    o = json.load(open(p)); kod = o.get('kod')
    W = os.path.dirname(os.path.dirname(os.path.abspath(p)))
    pp = f'{W}/plan/{kod}.json'
    if not os.path.exists(pp): return ['plan yok'], [], kod
    plan = json.load(open(pp))
    pdf = open(f'{W}/../pdf_metin/{kod}.md', encoding='utf-8').read()
    pdf_sayilar = set(re.findall(r'\d+(?:[.,]\d+)?', pdf)); plan_metin = json.dumps(plan, ensure_ascii=False)
    PN = {n['id']: n for n in plan['noktalar']}
    PS = {s['anahtar']: s for n in plan['noktalar'] for s in n['sorular']}
    G = o.get('giris') or []
    if not 1 <= len(G) <= 2: e.append('giris 1–2 cümle')
    for i, x in enumerate(G): cift(e, f'giris[{i}]', x, 4, 45)
    K = o.get('kapanis') or []
    if not 2 <= len(K) <= 4: e.append('kapanis 2–4 cümle')
    for i, x in enumerate(K): cift(e, f'kapanis[{i}]', x, 4, 45)
    B = o.get('bolumler') or []
    if not 3 <= len(B) <= 8: e.append(f'bolumler 3–8 ({len(B)})')
    gorulen_n, gorulen_s, sira = [], [], []
    dikkat = 0
    for bi, b in enumerate(B):
        if not b.get('baslik') or kelime(b['baslik']) > 9: e.append(f'bolum[{bi}]: baslik 1–9 kelime')
        cift(e, f'bolum[{bi}].neden', b.get('neden'), 6, 48)
        N = b.get('noktalar') or []
        ust = 11 if os.path.basename(p) == 'g07.json' else 10  # TBG kampı (g07) çıkmış PDF'i: bölüm 4'e g07-4f eklendi (2026-10-21)
        if not 1 <= len(N) <= ust: e.append(f'bolum[{bi}]: nokta 1–{ust} ({len(N)})')
        for n in N:
            y = n.get('id'); gorulen_n.append(y)
            if y not in PN: e.append(f'{y}: planda yok'); continue
            sira.append(y)
            if not n.get('baslik') or kelime(n['baslik']) > 8: e.append(f'{y}: baslik 1–8 kelime')
            C = n.get('cumleler') or []
            if not 3 <= len(C) <= 7: e.append(f'{y}: cumleler 3–7 ({len(C)})')
            for j, c in enumerate(C): cift(e, f'{y}.cumle[{j}]', c, 3, 40)
            top = sum(kelime(c.get('ses', '')) for c in C if isinstance(c, dict))
            if not 45 <= top <= 145: e.append(f'{y}: anlatım {top} kelime (45–140)')
            dikkat += sum(1 for c in C if isinstance(c, dict) and 'Dikkat' in c.get('metin', ''))
            for c in C:
                for x in re.findall(r'\d+(?:[.,]\d+)?', c.get('metin', '') if isinstance(c, dict) else ''):
                    if x not in pdf_sayilar and x not in plan_metin: e.append(f'{y}: sayı {x} PDF/planda yok')
            for s in n.get('sorular') or []:
                k = s.get('anahtar'); gorulen_s.append(k)
                ps = PS.get(k)
                if not ps: e.append(f'{y}: soru {k} planda yok'); continue
                ks = s.get('kok_ses') or ''
                if not ks.strip(): e.append(f'{k}: kok_ses yok')
                elif YASAK_SES.search(ks.replace('|', '')) or KISALTMA.findall(ks) or KARISIK.findall(ks): e.append(f'{k}: kok_ses yasak karakter/kısaltma')
                cift(e, f'{k}.dogru', s.get('dogru'), 3, 32)
                if isinstance(s.get('dogru'), dict) and not str(s['dogru'].get('metin', '')).startswith('Doğru'): e.append(f'{k}.dogru: "Doğru" ile başlamalı')
                beklenen = sorted(h for h in ps['secenekler'] if h != ps['dogru'])
                Y = s.get('yanlis') or {}
                if sorted(Y) != beklenen: e.append(f'{k}: yanlis şıkları {sorted(Y)} ≠ {beklenen}')
                for h, v in Y.items():
                    cift(e, f'{k}.yanlis.{h}', v, 12, 62)
                    if isinstance(v, dict) and 'oğrusu' not in v.get('metin', ''): e.append(f'{k}.yanlis.{h}: "Doğrusu:" yok')
                    if isinstance(v, dict): e.extend(sik_denetle(v.get('metin', ''), f'{k}.yanlis.{h}', enaz=15, encok=65, cumle=(2, 4)))
                if len({v.get('metin', '')[:40] for v in Y.values() if isinstance(v, dict)}) < len(Y): e.append(f'{k}: yanlış açıklamaları tekrar')
                H = s.get('yardim') or {}
                if sorted(H) != sorted(ps['secenekler']): e.append(f'{k}: yardim tüm şıklar için olmalı {sorted(H)} ≠ {sorted(ps["secenekler"])}')
                for h, v in H.items():
                    cift(e, f'{k}.yardim.{h}', v, 18, 75)
                    if isinstance(v, dict): e.extend(sik_denetle(v.get('metin', ''), f'{k}.yardim.{h}'))
                    if isinstance(v, dict) and re.match(r'^[A-E]\s*(şıkkı|\)|:)', v.get('ses', '')): e.append(f'{k}.yardim.{h}: harfi okuma')
    zor = [n['id'] for n in plan['noktalar'] if n['zorunlu']]
    eksik = [i for i in zor if i not in gorulen_n]
    if eksik: e.append(f'zorunlu nokta eksik: {eksik}')
    if len(gorulen_n) != len(set(gorulen_n)): e.append('nokta tekrar')
    if sorted(gorulen_s) != sorted(PS): e.append(f'soru eksik/fazla: eksik {sorted(set(PS) - set(gorulen_s))[:6]} fazla {sorted(set(gorulen_s) - set(PS))[:6]}')
    if len(gorulen_s) != len(set(gorulen_s)): e.append('soru tekrar')
    if dikkat > 5: u.append(f'"Dikkat" {dikkat} kez (en çok 5)')
    return e, u, kod


if __name__ == '__main__':
    te = tu = 0
    for p in sys.argv[1:]:
        e, u, kod = check(p)
        if e == ['plan yok']:
            print('HATA', p, 'plan yok'); te += 1; continue
        for x in e: print('HATA', kod, x)
        for x in u: print('UYARI', kod, x)
        te += len(e); tu += len(u)
    print(te, 'HATA', tu, 'UYARI'); sys.exit(1 if te else 0)
