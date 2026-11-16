"""Soru çözücü 3. tur doğrulayıcı (canlı ders soruları): python3 dogrula3.py cikti3/<kod>.json [...] → HATA/UYARI."""
import json, os, re, sys, collections
W = "/home/indu/medsor/meds_temp/patoloji_ornek26/cozucu"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cozucu_dogrula2 import soru_denet, kokler

if __name__ == '__main__':
    te = 0
    for p in sys.argv[1:]:
        e, u = [], []
        o = json.load(open(p)); kod = o.get('kod')
        g = json.load(open(f'{W}/girdi3/{kod}.json'))
        pdf = open(f'/home/indu/medsor/meds_temp/patoloji_onem/pdf_metin/{kod}.md', encoding='utf-8').read()
        maxs = max(int(x) for x in re.findall(r'=== SAYFA (\d+) ===', pdf))
        pdf_sayilar = set(re.findall(r'\d+(?:[.,]\d+)?', pdf))
        bolumler = set()
        for y in g['canli_metin']:
            bolumler |= {l[2:].strip() for l in open(y, encoding='utf-8') if l.startswith('@@')}
        Y = o.get('yeni') or []
        if not 5 <= len(Y) <= 30: e.append(f'yeni soru sayısı {len(Y)} (5–30)')
        elif abs(len(Y) - g['yeni_soru_sayisi']) > 3: u.append(f'yeni soru sayısı {len(Y)}, hedef {g["yeni_soru_sayisi"]} (gerekçe yaz)')
        mevcut = [kokler(m['soru'] + ' ' + m['dogru']) for m in g['mevcut']]
        gorulen = []
        for i, q in enumerate(Y, 1):
            y = f'yeni{i}'
            soru_denet(e, u, y, q, pdf_sayilar, maxs)
            if q.get('canli_bolum') not in bolumler: e.append(f'{y}: canli_bolum canlı ders bölüm başlığıyla birebir değil: {q.get("canli_bolum")!r}')
            if q.get('zorluk') not in ('kolay', 'orta', 'zor'): e.append(f'{y}: zorluk kolay|orta|zor')
            kk = kokler(q.get('soru', '') + ' ' + (q.get('secenekler') or {}).get(q.get('dogru'), ''))
            for j, mk in enumerate(mevcut + gorulen):
                if kk and len(kk & mk) / max(1, min(len(kk), len(mk))) >= 0.8:
                    e.append(f'{y}: {"başka yeni soruya" if j >= len(mevcut) else "mevcut " + str(g["mevcut"][j]["no"]) + ". soruya"} çok benziyor')
            gorulen.append(kk)
        if Y:
            c = collections.Counter(q.get('dogru') for q in Y)
            if max(c.values()) > max(2, len(Y) * 0.35): e.append(f'harf dağılımı dengesiz {dict(c)}')
            if sum(q.get('zorluk') == 'kolay' for q in Y) > len(Y) * 0.2: u.append('kolay soru %20 üstü')
        for x in e: print('HATA', kod, x)
        for x in u: print('UYARI', kod, x)
        print(f'{kod}: yeni {len(Y)} · {len(e)} HATA · {len(u)} UYARI')
        te += len(e)
    print(f'TOPLAM {te} HATA')
    sys.exit(1 if te else 0)
