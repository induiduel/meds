#!/usr/bin/env python3
"""Sesli çözücü — dersin TÜM örnek soruları (kullanıcı kararı 2026-11-18, H623).

Kural "her örnek soru sesli çözücüde" der; `cozucu_dogrula.py` ise yalnız önem kümesini (önem örnekleri + çıkmış temsilciler) kabul
eder. Dersin `src/data/ornek_sorular/k<N>/<ders>.json` dosyasındaki sorular bu ayrı dosyada çözücüye girer:

  meds_temp/spot_cozucu/<brans>/cozucu_ders/<kod>.json = {"kod": "2p05", "ders": "<tam ders anahtarı>", "sorular": [...]}

Soru kümesi = örnek soru dosyasındaki her soru (önem örnekleriyle kökü aynı olanlar hariç; onlar zaten `cozucu/`'da),
`ref` = `"d:<soru id>"`, `tur: "ornek"`, `zorluk` kaynakla aynı; `soru`/`secenekler`/`dogru` örnek soru dosyasıyla BİREBİR (düzeltme
gerekiyorsa iki dosyaya da yazılır, `kontrol.durum: duzeltildi`). Alan biçimi ve dil kuralları TALIMAT_COZUCU.md ile aynı
(`kok_ses`, `secenek_ses`, `ipucu`, `siklar`, `cozum`, `sayfa`).

Kullanım: python3 cozucu_ders_dogrula.py meds_temp/spot_cozucu/<brans>/cozucu_ders/<kod>.json [...]
"""
import sys as _sys
from pathlib import Path as _Path
_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402
import json, re, sys  # noqa: E402
from pathlib import Path  # noqa: E402

sys.path.insert(0, str(_kok.SCRIPTS / 'uretim' / 'patoloji_cozucu'))
import cozucu_dogrula2 as D  # noqa: E402

SAYI = re.compile(r'\d+(?:[.,]\d+)?')
st = lambda d: {k: str(v).strip() for k, v in (d or {}).items()}  # noqa: E731


def ornek_dosyasi(ders):
    for p in sorted((_kok.MEDS / 'src' / 'data' / 'ornek_sorular').glob(f'k*/{ders}.json')):
        return p
    return None


def beklenen(W, kod, ders):
    p = ornek_dosyasi(ders)
    if not p:
        return None
    onem = W / 'onem' / f'{kod}.json'
    ok = set()
    if onem.exists():
        ok = {q['kok'].strip() for m in json.load(open(onem))['maddeler'] for q in m.get('ornek') or []}
    B = {}
    for k in json.load(open(p))['kazanimlar']:
        for q in k.get('sorular') or []:
            if q['soru'].strip() in ok:
                continue
            B[f"d:{q['id']}"] = q
    return B


def check(p):
    e, u = [], []
    p = Path(p).resolve(); W = p.parent.parent
    o = json.load(open(p)); kod = o.get('kod') or p.stem; ders = o.get('ders')
    if not ders:
        return ['"ders" alanı (tam ders anahtarı) yok'], u, 0
    B = beklenen(W, kod, ders)
    if B is None:
        return [f'örnek soru dosyası yok: src/data/ornek_sorular/k*/{ders}.json'], u, 0
    pdf = (W / 'pdf_metin' / f'{kod}.md').read_text(encoding='utf-8')
    maxs = max(int(x) for x in re.findall(r'=== SAYFA (\d+) ===', pdf))
    pdf_sayilar = set(SAYI.findall(pdf))
    S = o.get('sorular') or []
    refs = [q.get('ref') for q in S]
    if len(set(refs)) < len(refs): e.append('aynı ref iki kez')
    eksik, fazla = set(B) - set(refs), set(refs) - set(B)
    if eksik: e.append(f'eksik soru ({len(eksik)}): {sorted(eksik)[:6]}')
    if fazla: e.append(f'fazla/bilinmeyen soru: {sorted(fazla)[:6]}')
    for q in S:
        y = str(q.get('ref'))
        b = B.get(q.get('ref'))
        if not b: continue
        if q.get('tur') != 'ornek': e.append(f'{y}: tur ornek olmalı')
        if str(q.get('soru', '')).strip() != b['soru'].strip() or st(q.get('secenekler')) != st(b['secenekler']) or q.get('dogru') != b['dogru']:
            e.append(f'{y}: soru/şık/anahtar örnek soru dosyasıyla aynı değil (düzeltmeyi iki dosyaya da yaz)')
        if q.get('zorluk') != b.get('zorluk'): e.append(f'{y}: zorluk örnek soru dosyasıyla aynı olmalı')
        kt = q.get('kontrol') or {}
        if kt.get('durum') not in ('tamam', 'duzeltildi'): e.append(f'{y}: kontrol.durum tamam|duzeltildi')
        if kt.get('durum') == 'duzeltildi':
            if len(str(kt.get('not') or '')) < 15: e.append(f'{y}: düzeltme notu yok')
            u.append(f"{y}: DÜZELTİLDİ — {kt.get('not')}")
        if len(re.findall(r'\w+', str(q.get('soru') or ''))) > 90: e.append(f'{y}: kök çok uzun')
        D.soru_denet(e, u, y, q, pdf_sayilar, maxs, cikmis=True)
        if isinstance(q.get('ipucu'), dict) and q.get('dogru') in (q.get('secenekler') or {}):
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
