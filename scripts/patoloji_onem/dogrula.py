"""Patoloji önem listesi çıktı doğrulayıcısı. Kullanım: python3 araclar/dogrula.py cikti/07.json [...]
Denetim: şema, puan/bant dağılımı, alıntının PDF sayfasında birebir geçmesi, sayıların PDF'te geçmesi, örnek soru biçimi, çıkmış id'leri."""
import json, os, re, sys, unicodedata
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from turkce_uslup import denetle_yapi as uslup_yapi  # noqa: E402  (meds/docs/TURKCE_USLUP_STANDARDI.md)
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CIK = json.load(open(f'{W}/cikmis_pdf.json'))
TUR = {'tanim', 'en_sik', 'karakteristik', 'sayi', 'eslesme', 'mekanizma', 'siniflama', 'tuzak', 'tani_tedavi'}
def norm(s):
    s = unicodedata.normalize('NFKC', str(s or '')).replace('İ', 'i').replace('I', 'ı').lower()
    s = re.sub(r'[•●▪–—\-•▪►➢✓*_`"“”‘’\'()\[\]{}:;,.!?/]', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()
def pages(kod):
    t = open(f'{W}/pdf_metin/{kod}.md', encoding='utf-8').read()
    parts = re.split(r'\n=== SAYFA (\d+) ===\n', t)
    return {int(parts[i]): norm(parts[i + 1]) for i in range(1, len(parts) - 1, 2)}, norm(t)
def words(s): return len(re.findall(r'\w+', str(s or '')))
def nums(s): return set(re.findall(r'\d+(?:[.,]\d+)?', re.sub(r'\*\*', '', str(s or ''))))
def check(path):
    e, w = [], []
    d = json.load(open(path)); kod = d.get('kod') or os.path.basename(path)[:-5]
    if not os.path.exists(f'{W}/pdf_metin/{kod}.md'): return [f'{kod}: pdf_metin yok'], []
    P, ALL = pages(kod)
    allraw = re.sub(r'\s+', ' ', open(f'{W}/pdf_metin/{kod}.md', encoding='utf-8').read())
    cand = {c['id'] for c in CIK.get(kod, [])}
    for k in ('baslik', 'pdf', 'ozet', 'neden_onemli'):
        if words(d.get(k)) < (2 if k in ('baslik', 'pdf') else 8): e.append(f'{kod}: {k} eksik/kısa')
    e.extend(uslup_yapi({k: v for k, v in d.items() if k != 'maddeler'}, kod))
    M = d.get('maddeler') or []
    if not 20 <= len(M) <= 45: e.append(f'{kod}: madde sayısı {len(M)} (20–45)')
    bant = {}
    ids = set()
    for m in M:
        t = f"{kod}/{m.get('id')}"
        e.extend(uslup_yapi(m, t))
        if m.get('id') in ids: e.append(f'{t}: id tekrar')
        ids.add(m.get('id'))
        p = m.get('puan')
        if not isinstance(p, int) or not 0 <= p <= 100: e.append(f'{t}: puan 0–100 tamsayı olmalı'); continue
        b = min(p // 10, 9); bant[b] = bant.get(b, 0) + 1
        if m.get('tur') not in TUR: e.append(f'{t}: tur geçersiz {m.get("tur")!r}')
        if words(m.get('baslik')) < 1 or words(m.get('baslik')) > 10: e.append(f'{t}: baslik 1–10 kelime')
        bw = words(m.get('bilgi'))
        if bw < 4 or bw > 30: e.append(f'{t}: bilgi {bw} kelime (4–30, tek cümle)')
        alt = m.get('alt') or []
        if not isinstance(alt, list) or len(alt) > 4 or any(words(x) > 20 for x in alt): e.append(f'{t}: alt en çok 4 madde, her biri ≤20 kelime')
        for n in nums(m.get('bilgi')) | set().union(*[nums(x) for x in alt] or [set()]):
            if n not in allraw and n.replace(',', '.') not in allraw and n.replace('.', ',') not in allraw: e.append(f'{t}: "{n}" sayısı PDF metninde yok')
        al = m.get('alinti') or []
        if not 1 <= len(al) <= 3: e.append(f'{t}: alinti 1–3 öge')
        for a in al:
            s, mt = a.get('sayfa'), norm(a.get('metin'))
            if words(a.get('metin')) < 3: e.append(f'{t}: alıntı çok kısa'); continue
            ok = any(mt in P.get(x, '') for x in (s, (s or 0) - 1, (s or 0) + 1))
            if not ok:
                if mt in ALL: w.append(f'{t}: alıntı PDF\'te var ama sayfa {s} yanlış')
                else: e.append(f'{t}: alıntı PDF\'te birebir yok: {a.get("metin")[:70]!r}')
        if words(m.get('neden')) < 4: e.append(f'{t}: neden eksik')
        dw = words(m.get('detay'))
        if dw < 40 or dw > 220: e.append(f'{t}: detay {dw} kelime (40–220)')
        os_ = m.get('ornek_soru')
        if p >= 70 and not os_: e.append(f'{t}: puan ≥70 → ornek_soru zorunlu')
        if os_:
            sec = os_.get('secenekler') or {}
            if sorted(sec) != list('ABCDE') or len({norm(v) for v in sec.values()}) < 5: e.append(f'{t}: ornek_soru 5 farklı şık (A–E)')
            if os_.get('dogru') not in sec: e.append(f'{t}: ornek_soru dogru geçersiz')
            if not str(os_.get('kok', '')).strip().endswith('?'): e.append(f'{t}: ornek_soru kökü ? ile bitmeli')
            if words(os_.get('aciklama')) < 5: e.append(f'{t}: ornek_soru aciklama kısa')
        for c in m.get('cikmis') or []:
            if c not in cand: e.append(f'{t}: cikmis {c} aday listesinde yok')
    if bant.get(9, 0) < 4 or bant.get(9, 0) > 8: e.append(f'{kod}: 90–100 bandında {bant.get(9, 0)} madde (4–8)')
    for b in (8, 7, 6, 5):
        if bant.get(b, 0) < 2: e.append(f'{kod}: {b*10}–{b*10+9} bandında {bant.get(b, 0)} madde (en az 2)')
    return e, w
if __name__ == '__main__':
    te = tw = 0
    for p in sys.argv[1:]:
        e, w = check(p); te += len(e); tw += len(w)
        for x in e: print('HATA ', x)
        for x in w: print('UYARI', x)
    print(f'{te} HATA · {tw} UYARI'); sys.exit(1 if te else 0)
