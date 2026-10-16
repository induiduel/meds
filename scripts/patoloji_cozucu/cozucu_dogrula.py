"""Soru çözücü çıktısı doğrulayıcı: python3 dogrula.py cikti/<kod>.json [...] → HATA/UYARI (HATA varsa çıkış 1)."""
import json, os, re, sys
W = "/home/indu/medsor/meds_temp/patoloji_ornek26/cozucu"
YASAK_SES = re.compile(r'[0-9%/→←↑↓±≈~<>=+⁺⁻²³()\[\]*#_{}@&$€£^\\:;"“”‘’«»…–—]')
KISALTMA = re.compile(r'\b[A-ZÇĞİÖŞÜ]{2,}[0-9]*\b')
KARISIK = re.compile(r"\b\w*[a-zçğıöşü][A-ZÇĞİÖŞÜ]\w*\b")
IC_DIL = re.compile(r"\b(pdf\w*|kaynak\w*|slayt\w*|ders not\w*|talimat\w*|ipucu(?!\s+hücre)\w*|çeldirici\w*|şık\w*|hoca\w*)\b", re.I)
HARF_AN = re.compile(r"\b[A-E] ?(şıkkı|seçeneği|şıkk)|\b(be|ce|de) şıkkı", re.I)
kelime = lambda s: len(re.findall(r'\w+', s))
kok5 = lambda w: w.replace('İ', 'i').replace('I', 'ı').lower()[:5]
SAYI = re.compile(r'\d+(?:[.,]\d+)?')


def ses_denet(e, yer, s):
    t = s.replace('||', ' ').replace('|', ' ')
    m = YASAK_SES.search(t)
    if m: e.append(f'{yer}: ses yasak karakter {m.group()!r} — {s[:70]}')
    k = KISALTMA.findall(s)
    if k: e.append(f'{yer}: ses büyük harfli kısaltma (harfle yaz): {k[:3]}')
    if KARISIK.findall(s): e.append(f'{yer}: ses karışık harfli kısaltma: {KARISIK.findall(s)[:3]}')
    if '**' in s: e.append(f'{yer}: seste ** var')
    tek = [m.group(1) for m in re.finditer(r'(?<![.!?]\s)(?<!^)\b([A-ZÇĞİÖŞÜ])\b(?![\'’])', s.strip())]
    if tek: e.append(f'{yer}: seste cümle ortasında tek büyük harf {tek[:3]} (okunuşla yaz)')
    for cm in re.split(r'(?<=[.!?])\s+', t):
        if kelime(cm) > 27: e.append(f'{yer}: ses cümlesi {kelime(cm)} kelime (en çok 25)'); break
    if s.count('|') > 2: e.append(f'{yer}: durak işareti çok')


def cift(e, yer, x, enaz, encok, cumle=2):
    if not isinstance(x, dict) or not isinstance(x.get('metin'), str) or not isinstance(x.get('ses'), str):
        e.append(f'{yer}: {{metin, ses}} olmalı'); return False
    m, s = x['metin'].strip(), x['ses'].strip()
    if not m or not s: e.append(f'{yer}: boş'); return False
    ses_denet(e, yer, s)
    for a in (m, s):
        g = IC_DIL.search(a)
        if g: e.append(f'{yer}: öğrenciye dönük olmayan sözcük {g.group()!r}')
        if HARF_AN.search(a): e.append(f'{yer}: harf anılmış: {HARF_AN.search(a).group()!r}')
    if '(' in m or ')' in m: e.append(f'{yer}: metin parantez içeriyor')
    if not enaz <= kelime(s) <= encok: e.append(f'{yer}: ses {kelime(s)} kelime ({enaz}–{encok})')
    if not enaz - 2 <= kelime(m.replace('**', '')) <= encok + 4: e.append(f'{yer}: metin {kelime(m)} kelime ({enaz}–{encok})')
    nc = len([c for c in re.split(r'(?<=[.!?])\s+', m) if c.strip()])
    if nc > cumle: e.append(f'{yer}: {nc} cümle (en çok {cumle})')
    r = kelime(s) / max(1, kelime(m.replace('**', '')))
    if not 0.7 <= r <= 2.4: e.append(f'{yer}: metin–ses uzunluk oranı {r:.2f} (aynı içerik olmalı)')
    return True


te = tu = 0
for p in sys.argv[1:]:
    e, u = [], []
    o = json.load(open(p)); kod = o.get('kod')
    kaynak = json.load(open(f'{W}/../cikti/{kod}.json'))
    pdf = open(f'/home/indu/medsor/meds_temp/patoloji_onem/pdf_metin/{kod}.md', encoding='utf-8').read()
    maxs = max(int(x) for x in re.findall(r'=== SAYFA (\d+) ===', pdf))
    pdf_sayilar = set(SAYI.findall(pdf))
    S = o.get('sorular') or []
    K = {q['no']: q for q in kaynak['sorular']}
    if [q.get('no') for q in S] != [q['no'] for q in kaynak['sorular']]: e.append('sorular kaynakla aynı no/sırada ve eksiksiz olmalı')
    for q in S:
        y = f"s{q.get('no')}"
        kq = K.get(q.get('no'))
        if not kq: continue
        kt = q.get('kontrol') or {}
        if kt.get('durum') not in ('tamam', 'duzeltildi'): e.append(f'{y}: kontrol.durum tamam|duzeltildi')
        ayni = q.get('soru') == kq['soru'] and q.get('secenekler') == kq['secenekler'] and q.get('dogru') == kq['dogru']
        if kt.get('durum') == 'tamam' and not ayni: e.append(f'{y}: kontrol tamam ama soru/şık/anahtar kaynaktan farklı')
        if kt.get('durum') == 'duzeltildi':
            if ayni: e.append(f'{y}: düzeltildi denmiş ama değişiklik yok')
            if not kt.get('not') or len(kt['not']) < 15: e.append(f'{y}: düzeltme notu yok')
            u.append(f"{y}: DÜZELTİLDİ — {kt.get('not')}")
        sec = q.get('secenekler') or {}
        if sorted(sec) != list('ABCDE'): e.append(f'{y}: şıklar A–E değil'); continue
        if len({v.strip().lower() for v in sec.values()}) < 5: e.append(f'{y}: yinelenen şık')
        d = q.get('dogru')
        if d not in sec: e.append(f'{y}: dogru harfi geçersiz'); continue
        ks = q.get('kok_ses')
        if not isinstance(ks, str) or kelime(ks) < 3: e.append(f'{y}: kok_ses yok')
        else:
            ses_denet(e, f'{y}.kok_ses', ks)
            r = kelime(ks) / max(1, kelime(q['soru']))
            if not 0.7 <= r <= 2.6: e.append(f'{y}.kok_ses: kökle uzunluk uyumsuz ({r:.2f})')
        ss = q.get('secenek_ses') or {}
        if sorted(ss) != list('ABCDE'): e.append(f'{y}: secenek_ses A–E değil')
        for h, v in ss.items():
            if not isinstance(v, str) or not v.strip(): e.append(f'{y}.secenek_ses.{h}: boş'); continue
            ses_denet(e, f'{y}.secenek_ses.{h}', v)
            if kelime(v) > max(12, kelime(sec.get(h, '')) * 3): e.append(f'{y}.secenek_ses.{h}: şıktan çok uzun')
        if cift(e, f'{y}.ipucu', q.get('ipucu'), 6, 26, 1):
            ip = (q['ipucu']['metin'] + ' ' + q['ipucu']['ses'])
            ipk = {kok5(w) for w in re.findall(r'\w{4,}', ip)}
            sizan = [w for w in re.findall(r'\w{4,}', sec[d] + ' ' + ss.get(d, '')) if kok5(w) in ipk]
            if sizan: e.append(f'{y}.ipucu: cevabı sızdırıyor ({sizan[:3]})')
            for n in SAYI.findall(sec[d]):
                if re.search(rf'(?<!\d){re.escape(n)}(?!\d)', q['ipucu']['metin']): e.append(f'{y}.ipucu: cevaptaki sayı {n} geçiyor')
        Sk = q.get('siklar') or {}
        if sorted(Sk) != list('ABCDE'): e.append(f'{y}: siklar A–E değil')
        bas = []
        for h, v in Sk.items():
            if not cift(e, f'{y}.siklar.{h}', v, 6, 36): continue
            mm = v['metin'].lower()
            if h == d and 'doğru' not in mm: e.append(f'{y}.siklar.{h}: doğru şık açıklamasında "doğru" yok')
            if h != d and re.match(r'\W*doğru\b', mm): e.append(f'{y}.siklar.{h}: yanlış şık "doğru" ile başlıyor')
            bas.append(re.sub(r'\W+', ' ', mm)[:45])
            for n in SAYI.findall(v['metin']):
                if n not in pdf_sayilar and n not in json.dumps(sec, ensure_ascii=False): u.append(f'{y}.siklar.{h}: sayı {n} PDF metninde yok')
        if len(set(bas)) < len(bas): e.append(f'{y}: şık açıklamaları birbirinin tekrarı')
        if cift(e, f'{y}.cozum', q.get('cozum'), 10, 42):
            if re.match(r'\W*doğru (cevap|yanıt)', q['cozum']['metin'].lower()): e.append(f'{y}.cozum: "Doğru cevap" ile başlamamalı')
            for n in SAYI.findall(q['cozum']['metin']):
                if n not in pdf_sayilar: u.append(f'{y}.cozum: sayı {n} PDF metninde yok')
        sy = q.get('sayfa')
        if not isinstance(sy, list) or not sy or not all(isinstance(x, int) and 1 <= x <= maxs for x in sy): e.append(f'{y}: sayfa listesi geçersiz (1–{maxs})')
    for x in e: print('HATA', kod, x)
    for x in u: print('UYARI', kod, x)
    print(f'{kod}: {len(S)} soru · {len(e)} HATA · {len(u)} UYARI')
    te += len(e); tu += len(u)
print(f'TOPLAM {te} HATA, {tu} UYARI')
sys.exit(1 if te else 0)
