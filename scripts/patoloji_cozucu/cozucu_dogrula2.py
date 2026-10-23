"""Soru çözücü 2. tur doğrulayıcı: python3 dogrula2.py cikti2/<kod>.json [...] → HATA/UYARI (HATA varsa çıkış 1)."""
import json, os, re, sys, collections
# cümle sınırı: "8-10. haftalar" gibi sıra sayısı noktası cümle sonu sayılmaz (2026-10-24, H36)
CUMLE_SINIRI = re.compile(r'(?<=[.!?])(?<!\d\.)\s+|(?<=\d\.)\s+(?=[A-ZÇĞİÖŞÜ])')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from turkce_uslup import denetle as uslup_denetle  # noqa: E402  (meds/docs/TURKCE_USLUP_STANDARDI.md)
from sik_aciklama import denetle as sik_denetle  # noqa: E402  (meds/docs/SIK_ACIKLAMA_STANDARDI.md)
W = "/home/indu/medsor/meds_temp/patoloji_ornek26/cozucu"
YASAK_SES = re.compile(r'[0-9%/→←↑↓±≈~<>=+⁺⁻²³()\[\]*#_{}@&$€£^\\:;"“”‘’«»…–—]')
KISALTMA = re.compile(r'\b[A-ZÇĞİÖŞÜ]{2,}[0-9]*\b')
KARISIK = re.compile(r"\b\w*[a-zçğıöşü][A-ZÇĞİÖŞÜ]\w*\b")
# "kaynak": yalnız süreç dili biçimleri (kaynakta, kaynağa göre, kaynakça …). "kaynaklı", "kaynaklanır", "enfeksiyon
# kaynağı", "kaynak hasta" tıbbi Türkçedir — eski kalıp (kaynak\w*) bunları da yasaklıyordu (2026-10-23).
IC_DIL = re.compile(r"\b(pdf\w*|kaynak(ta|tan|ça|lara göre|a göre)|kaynağa göre|kaynak metin\w*|slayt\w*|ders not\w*|talimat\w*|"
                    r"ipucu(?!\s+hücre)\w*|çeldirici\w*|şık\w*|hoca\w*)\b", re.I)
HARF_AN = re.compile(r"\b[A-E] ?(şıkkı|seçeneği|şıkk)|\b(be|ce|de) şıkkı", re.I)
# birleşik okunan kısaltma (harf adları bitişik): denea, atepe, hapeve … ve kelime gibi okunan yasaklılar
BIRLESIK = re.compile(r"\b(denea|renea|atepe|hapeve|anka|cede\w*|pese\w*|acete\w*)\b", re.I)
kelime = lambda s: len(re.findall(r'\w+', s))
kok5 = lambda w: w.replace('İ', 'i').replace('I', 'ı').lower()[:5]
SAYI = re.compile(r'\d+(?:[.,]\d+)?')
DUR = set('aşağıdakilerden hangisi hangisidir değildir olan olarak için ile veya daha çok sıklıkla genellikle en sık olası doğru yanlış'.split())
kokler = lambda s: {kok5(w) for w in re.findall(r'\w{4,}', s) if w.lower() not in DUR}


def ses_denet(e, yer, s):
    t = s.replace('||', ' ').replace('|', ' ')
    m = YASAK_SES.search(t)
    if m: e.append(f'{yer}: ses yasak karakter {m.group()!r} — {s[:70]}')
    k = KISALTMA.findall(s)
    if k: e.append(f'{yer}: ses büyük harfli kısaltma (harfle yaz): {k[:3]}')
    if KARISIK.findall(s): e.append(f'{yer}: ses karışık harfli kısaltma: {KARISIK.findall(s)[:3]}')
    tek = [m.group(1) for m in re.finditer(r'(?<![.!?]\s)(?<!^)\b([A-ZÇĞİÖŞÜ])\b(?![\'’])', s.strip())]
    if tek: e.append(f'{yer}: seste cümle ortasında tek büyük harf {tek[:3]}')
    if BIRLESIK.search(s): e.append(f'{yer}: kısaltma birleşik/kelime gibi yazılmış: {BIRLESIK.search(s).group()!r} (harf harf, boşlukla)')
    if '**' in s: e.append(f'{yer}: seste ** var')
    if re.search(r'\b(tip|faktör|sınıf|evre|derece|kompleks)\s+(ı|ıı|ııı|ıv|v|vıı|vııı|ıx|xıı|i|ii|iii|iv|vii|viii|ix|xii)\b', s, re.I): e.append(f'{yer}: seste Roma rakamı harf gibi (sayıyla yaz: tip dört, faktör bir)')
    for cm in re.split(CUMLE_SINIRI, t):
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
        if HARF_AN.search(a): e.append(f'{yer}: harf anılmış')
    if '(' in m or ')' in m: e.append(f'{yer}: metin parantez içeriyor')
    e.extend(uslup_denetle(m, yer))
    if not enaz <= kelime(s) <= encok: e.append(f'{yer}: ses {kelime(s)} kelime ({enaz}–{encok})')
    nc = len([c for c in re.split(CUMLE_SINIRI, m) if c.strip()])
    if nc > cumle: e.append(f'{yer}: {nc} cümle (en çok {cumle})')
    r = kelime(s) / max(1, kelime(m.replace('**', '')))
    if not 0.7 <= r <= 2.6: e.append(f'{yer}: metin–ses uzunluk oranı {r:.2f}')
    return True


def soru_denet(e, u, y, q, pdf_sayilar, maxs, cikmis=False):
    sec = q.get('secenekler') or {}
    if sorted(sec) != list('ABCDE'): e.append(f'{y}: şıklar A–E değil'); return
    if len({v.strip().lower() for v in sec.values()}) < 5: e.append(f'{y}: yinelenen şık')
    d = q.get('dogru')
    if d not in sec: e.append(f'{y}: dogru harfi geçersiz'); return
    if not cikmis:
        for h, v in sec.items():
            if kelime(v) > 7: e.append(f'{y}: şık {h} uzun ({kelime(v)} kelime; en çok 6)')
        if kelime(q.get('soru', '')) > 40: e.append(f'{y}: kök uzun')
    ks = q.get('kok_ses')
    if not isinstance(ks, str) or kelime(ks) < 3: e.append(f'{y}: kok_ses yok')
    else:
        ses_denet(e, f'{y}.kok_ses', ks)
        r = kelime(ks) / max(1, kelime(q['soru']))
        if not 0.7 <= r <= 2.8: e.append(f'{y}.kok_ses: kökle uzunluk uyumsuz ({r:.2f})')
    ss = q.get('secenek_ses') or {}
    if sorted(ss) != list('ABCDE'): e.append(f'{y}: secenek_ses A–E değil')
    for h, v in ss.items():
        if not isinstance(v, str) or not v.strip(): e.append(f'{y}.secenek_ses.{h}: boş'); continue
        ses_denet(e, f'{y}.secenek_ses.{h}', v)
        if kelime(v) > max(12, kelime(sec.get(h, '')) * 3): e.append(f'{y}.secenek_ses.{h}: şıktan çok uzun')
    if cift(e, f'{y}.ipucu', q.get('ipucu'), 6, 26, 1):
        ip = q['ipucu']['metin'] + ' ' + q['ipucu']['ses']
        ipk = {kok5(w) for w in re.findall(r'\w{4,}', ip)}
        sizan = [w for w in re.findall(r'\w{4,}', sec[d] + ' ' + ss.get(d, '')) if kok5(w) in ipk and w.lower() not in DUR]
        if sizan and not cikmis: e.append(f'{y}.ipucu: cevabı sızdırıyor ({sizan[:3]})')
        elif sizan: u.append(f'{y}.ipucu: doğru şıkla ortak sözcük ({sizan[:3]}) — sızıntı değil mi kontrol et')
    Sk = q.get('siklar') or {}
    if sorted(Sk) != list('ABCDE'): e.append(f'{y}: siklar A–E değil')
    bas = []
    for h, v in Sk.items():
        if not cift(e, f'{y}.siklar.{h}', v, 18, 80, 3): continue
        e.extend(sik_denetle(v['metin'], f'{y}.siklar.{h}', enaz=18, encok=60, cumle=(2, 3)))
        mm = v['metin'].lower()
        if h == d and 'doğru' not in mm: e.append(f'{y}.siklar.{h}: doğru şık açıklamasında "doğru" yok')
        if h != d and re.match(r'\W*doğru\b', mm): e.append(f'{y}.siklar.{h}: yanlış şık "doğru" ile başlıyor')
        bas.append(re.sub(r'\W+', ' ', mm)[:45])
        for n in SAYI.findall(v['metin']):
            if n not in pdf_sayilar and n not in json.dumps(sec, ensure_ascii=False): u.append(f'{y}.siklar.{h}: sayı {n} PDF metninde yok')
    if len(set(bas)) < len(bas): e.append(f'{y}: şık açıklamaları birbirinin tekrarı')
    if cift(e, f'{y}.cozum', q.get('cozum'), 10, 44):
        if re.match(r'\W*doğru (cevap|yanıt)', q['cozum']['metin'].lower()): e.append(f'{y}.cozum: "Doğru cevap" ile başlamamalı')
        for n in SAYI.findall(q['cozum']['metin']):
            if n not in pdf_sayilar: u.append(f'{y}.cozum: sayı {n} PDF metninde yok')
    sy = q.get('sayfa')
    if not isinstance(sy, list) or not sy or not all(isinstance(x, int) and 1 <= x <= maxs for x in sy): e.append(f'{y}: sayfa listesi geçersiz (1–{maxs})')


if __name__ == '__main__':
    te = 0
    for p in sys.argv[1:]:
        e, u = [], []
        o = json.load(open(p)); kod = o.get('kod')
        g = json.load(open(f'{W}/girdi2/{kod}.json'))
        pdf = open(f'/home/indu/medsor/meds_temp/patoloji_onem/pdf_metin/{kod}.md', encoding='utf-8').read()
        maxs = max(int(x) for x in re.findall(r'=== SAYFA (\d+) ===', pdf))
        pdf_sayilar = set(SAYI.findall(pdf))
        Y, C = o.get('yeni') or [], o.get('cikmis') or []
        if len(Y) != g['yeni_soru_sayisi']: e.append(f'yeni soru sayısı {len(Y)} ≠ {g["yeni_soru_sayisi"]}')
        if len(C) > 5: e.append(f'çıkmış {len(C)} (en çok 5)')
        onem_ids = {m['id'] for m in g['onem']}
        mevcut = [kokler(m['soru'] + ' ' + m['dogru']) for m in g['mevcut']]
        gorulen = []
        for i, q in enumerate(Y, 1):
            y = f'yeni{i}'
            soru_denet(e, u, y, q, pdf_sayilar, maxs)
            if q.get('onem_id') not in onem_ids: u.append(f'{y}: onem_id {q.get("onem_id")} girdide yok')
            if q.get('zorluk') not in ('orta', 'zor'): e.append(f'{y}: zorluk orta|zor')
            kk = kokler(q.get('soru', '') + ' ' + (q.get('secenekler') or {}).get(q.get('dogru'), ''))
            for j, mk in enumerate(mevcut + gorulen):
                if kk and len(kk & mk) / max(1, min(len(kk), len(mk))) >= 0.8:
                    (e if j >= len(mevcut) else u).append(f'{y}: {"başka yeni soruya" if j >= len(mevcut) else "mevcut " + str(g["mevcut"][j]["no"]) + ". soruya"} çok benziyor')
            gorulen.append(kk)
        if Y:
            c = collections.Counter(q.get('dogru') for q in Y)
            if max(c.values()) > max(2, len(Y) * 0.35): e.append(f'yeni sorularda harf dağılımı dengesiz {dict(c)}')
            if sum(q.get('zorluk') == 'zor' for q in Y) < len(Y) / 2 - 0.5: u.append('zor soru yarıdan az')
        aday = {a['id']: a for a in g['cikmis_adaylari']}
        ids = [q.get('id') for q in C]
        if len(set(ids)) < len(ids): e.append('aynı çıkmış iki kez')
        for q in C:
            y = f'cikmis:{q.get("id")}'
            a = aday.get(q.get('id'))
            if not a: e.append(f'{y}: aday listesinde yok'); continue
            if q.get('soru', '').strip() != a['kok'].strip() or {k: v.strip() for k, v in (q.get('secenekler') or {}).items()} != {k: v.strip() for k, v in a['secenekler'].items()} or q.get('dogru') != a['dogru']:
                e.append(f'{y}: kök/şık/anahtar adaydan birebir kopyalanmamış')
            if q.get('sinav') != a['sinav']: e.append(f'{y}: sinav alanı farklı')
            soru_denet(e, u, y, q, pdf_sayilar, maxs, cikmis=True)
        if len(C) < min(5, len(aday)) and not o.get('elenen_cikmis'): u.append(f'çıkmış {len(C)} < {min(5, len(aday))} ve elenen gerekçesi yok')
        for x in e: print('HATA', kod, x)
        for x in u: print('UYARI', kod, x)
        print(f'{kod}: yeni {len(Y)} · çıkmış {len(C)} · {len(e)} HATA · {len(u)} UYARI')
        te += len(e)
    print(f'TOPLAM {te} HATA')
    sys.exit(1 if te else 0)
