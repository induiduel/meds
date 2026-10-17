#!/usr/bin/env python3
"""Sesli soru çözücü (branş geneli) doğrulayıcısı — TALIMAT_COZUCU.md.
Kullanım: python3 meds/scripts/spot_cozucu/cozucu_dogrula.py meds_temp/spot_cozucu/<brans>/cozucu/<kod>.json [...]
Denetim: soru kümesi = onem/<kod>.json'daki örnekler + maddelere bağlı çıkmış temsilciler (eksik/fazla yok); örnekler onem ile, çıkmışlar
cikmis/<kod>.json ile birebir; ses/metin biçimi, ipucu sızıntısı, şık açıklamaları (patoloji çözücü denetimiyle aynı kurallar)."""
import json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'patoloji_cozucu'))
import cozucu_dogrula2 as D  # noqa: E402  (ses_denet, cift, soru_denet, kok5, DUR)

SAYI = re.compile(r'\d+(?:[.,]\d+)?')
kelime = lambda s: len(re.findall(r'\w+', str(s or '')))  # noqa: E731
st = lambda d: {k: str(v).strip() for k, v in (d or {}).items()}  # noqa: E731


def beklenen(W, kod):
    o = json.load(open(W / 'onem' / f'{kod}.json'))
    C = {c['id']: c for c in json.load(open(W / 'cikmis' / f'{kod}.json'))} if (W / 'cikmis' / f'{kod}.json').exists() else {}
    B = {}
    for m in o['maddeler']:
        for i, q in enumerate(m.get('ornek') or [], 1):
            B[f"o:{m['id']}:{i}"] = {'tur': 'ornek', 'onem_id': m['id'], 'soru': q['kok'], 'secenekler': q['secenekler'], 'dogru': q['dogru'], 'zorluk': q.get('zorluk')}
        for c in m.get('cikmis') or []:
            if f'c:{c}' not in B and c in C:
                B[f'c:{c}'] = {'tur': 'cikmis', 'onem_id': m['id'], 'soru': C[c]['kok'], 'secenekler': C[c]['secenekler'], 'dogru': C[c]['dogru'], 'sinav': C[c]['sinav']}
    return B


def check(p):
    e, u = [], []
    p = Path(p).resolve(); W = p.parent.parent
    o = json.load(open(p)); kod = o.get('kod') or p.stem
    pdf = (W / 'pdf_metin' / f'{kod}.md').read_text(encoding='utf-8')
    maxs = max(int(x) for x in re.findall(r'=== SAYFA (\d+) ===', pdf))
    pdf_sayilar = set(SAYI.findall(pdf))
    B = beklenen(W, kod)
    S = o.get('sorular') or []
    refs = [q.get('ref') for q in S]
    if len(set(refs)) < len(refs): e.append('aynı ref iki kez')
    eksik, fazla = set(B) - set(refs), set(refs) - set(B)
    if eksik: e.append(f'eksik soru: {sorted(eksik)[:6]}')
    if fazla: e.append(f'fazla/bilinmeyen soru: {sorted(fazla)[:6]}')
    for q in S:
        y = str(q.get('ref'))
        b = B.get(q.get('ref'))
        if not b: continue
        if q.get('tur') != b['tur']: e.append(f'{y}: tur {b["tur"]} olmalı')
        if q.get('onem_id') != b['onem_id'] and b['tur'] == 'ornek': e.append(f'{y}: onem_id {b["onem_id"]} olmalı')
        if str(q.get('soru', '')).strip() != str(b['soru']).strip() or st(q.get('secenekler')) != st(b['secenekler']) or q.get('dogru') != b['dogru']:
            e.append(f'{y}: soru/şık/anahtar ' + ('onem dosyasındaki örnekle aynı değil (düzeltmeyi iki dosyaya da yaz)' if b['tur'] == 'ornek' else 'çıkmış adaydan birebir değil'))
        if b['tur'] == 'cikmis' and q.get('sinav') != b['sinav']: e.append(f'{y}: sinav alanı farklı')
        if b['tur'] == 'ornek' and q.get('zorluk') != b['zorluk']: e.append(f'{y}: zorluk onem dosyasıyla aynı olmalı')
        kt = q.get('kontrol') or {}
        if kt.get('durum') not in ('tamam', 'duzeltildi'): e.append(f'{y}: kontrol.durum tamam|duzeltildi')
        if kt.get('durum') == 'duzeltildi':
            if len(str(kt.get('not') or '')) < 15: e.append(f'{y}: düzeltme notu yok')
            u.append(f"{y}: DÜZELTİLDİ — {kt.get('not')}")
        if kelime(q.get('soru')) > 90: e.append(f'{y}: kök çok uzun')
        D.soru_denet(e, u, y, q, pdf_sayilar, maxs, cikmis=True)
        # örnek sorularda ipucu sızıntısı HATA (çıkmışta D.soru_denet uyarır)
        if b['tur'] == 'ornek' and isinstance(q.get('ipucu'), dict) and q.get('dogru') in (q.get('secenekler') or {}):
            ip = str(q['ipucu'].get('metin', '')) + ' ' + str(q['ipucu'].get('ses', ''))
            ipk = {D.kok5(w) for w in re.findall(r'\w{4,}', ip)}
            dg = q['secenekler'][q['dogru']] + ' ' + (q.get('secenek_ses') or {}).get(q['dogru'], '')
            sizan = [w for w in re.findall(r'\w{4,}', dg) if D.kok5(w) in ipk and w.lower() not in D.DUR]
            if sizan: e.append(f'{y}.ipucu: cevabı sızdırıyor ({sizan[:3]})')
            for n in SAYI.findall(q['secenekler'][q['dogru']]):
                if re.search(rf'(?<!\d){re.escape(n)}(?!\d)', q['ipucu'].get('metin', '')): e.append(f'{y}.ipucu: cevaptaki sayı {n} geçiyor')
    return e, u, len(S)


if __name__ == '__main__':
    te = 0
    for p in sys.argv[1:]:
        e, u, n = check(p)
        for x in e: print('HATA', Path(p).stem, x)
        for x in u: print('UYARI', Path(p).stem, x)
        print(f'{Path(p).stem}: {n} soru · {len(e)} HATA · {len(u)} UYARI')
        te += len(e)
    print(f'TOPLAM {te} HATA')
    sys.exit(1 if te else 0)
