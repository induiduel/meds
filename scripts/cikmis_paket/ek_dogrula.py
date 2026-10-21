#!/usr/bin/env python3
"""Çözücüde olmayan çıkmışların (ek modül) yazım kapısı: python3 ek_dogrula.py <parti.json> <cikti.json> → 0 HATA = geçer.
Çıktı kaydı: {"durum": "ekle"|"kopya"|"kapsam_disi", "gerekce", "ders", "sayfa", "soru", "secenek_ses", "ipucu", "siklar", "cozum", "not"}"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import sik_aciklama as SA
from turkce_uslup import denetle as TU

KALIP = re.compile(r'aranan özellik değil|doğru seçenektir ve klinik|fizyopatolojik mekanizma|temel gerekçesine göre|'
                   r'cevabı değil|cevap değil|olası hatalı|\[Dikkat|olarak geçmez', re.I)
DERS = json.load(open(Path(sys.argv[1]).parent / 'dersler.json'))
girdi = {q['id']: q for q in json.load(open(sys.argv[1]))}
c = json.load(open(sys.argv[2]))
e = []


def mv(k, yer, v, sik=False):
    m, s = (v or {}).get('metin', ''), (v or {}).get('ses', '')
    if not m or not s:
        e.append(f'{k} {yer}: metin/ses boş'); return
    if sik:
        e.extend(f'{k} {x}' for x in SA.denetle(m, yer))
    e.extend(f'{k} {x}' for x in TU(m, yer))
    if KALIP.search(m) or KALIP.search(s):
        e.append(f'{k} {yer}: kalıp ifade')
    if '**' in s or re.search(r'\d', s):
        e.append(f'{k} {yer}: ses metninde ** ya da rakam')


for k, q in girdi.items():
    o = c.get(k)
    if not o:
        e.append(f'{k}: çıktı yok'); continue
    d = o.get('durum')
    if d in ('kopya', 'kapsam_disi', 'sorun'):
        if not o.get('gerekce'):
            e.append(f'{k}: {d} için gerekce gerekli')
        continue
    if d != 'ekle':
        e.append(f'{k}: durum ekle/kopya/kapsam_disi/sorun olmalı'); continue
    if o.get('ders') not in {x['klasor'] for x in DERS[o.get('brans') or q['brans']]}:
        e.append(f'{k}: ders kodu geçersiz ({o.get("ders")})')
    if not o.get('sayfa') or not all(isinstance(x, int) for x in o['sayfa']):
        e.append(f'{k}: sayfa (slayt no listesi) gerekli')
    mv(k, 'soru', o.get('soru'))
    ss = o.get('secenek_ses') or {}
    if sorted(ss) != list('ABCDE') or any(re.search(r'\d|\*\*', v or '') for v in ss.values()):
        e.append(f'{k}: secenek_ses 5 şık, rakamsız')
    mv(k, 'ipucu', o.get('ipucu'))
    mv(k, 'cozum', o.get('cozum'))
    sk = o.get('siklar') or {}
    if sorted(sk) != list('ABCDE'):
        e.append(f'{k}: 5 şık gerekli'); continue
    for h in 'ABCDE':
        mv(k, f'sik {h}', sk[h], sik=True)
    dg = o.get('dogru') or q['dogru']
    if dg not in 'ABCDE' or len(dg) != 1:
        e.append(f'{k}: dogru geçersiz'); continue
    if o.get('dogru') and o['dogru'] != q['dogru'] and not o.get('anahtar_gerekce'):
        e.append(f'{k}: anahtar değiştiyse anahtar_gerekce gerekli')
    if 'doğru' not in sk[dg]['metin'].lower():
        e.append(f'{k}: doğru şık açıklaması doğru olduğunu söylemiyor')
    cev = re.sub(r'\W+', ' ', (q['secenekler'] or {}).get(dg, '').lower()).split()
    ip = (o.get('ipucu') or {}).get('metin', '').lower()
    if any(len(w) >= 5 and w[:5] in ip for w in cev):
        e.append(f'{k} ipucu: cevabın kelimesi/kökü geçiyor')
    nt = o.get('not') or {}
    cm = nt.get('cumleler') or []
    if not nt.get('baslik') or not 3 <= len(cm) <= 5:
        e.append(f'{k} not: başlık + 3–5 cümle gerekli')
    for i, x in enumerate(cm):
        mv(k, f'not {i}', x)
for x in e:
    print('HATA', x)
say = {d: sum(1 for v in c.values() if v.get('durum') == d) for d in ('ekle', 'kopya', 'kapsam_disi', 'sorun')}
print(f'{len(girdi)} soru {say}, {len(e)} HATA')
sys.exit(1 if e else 0)
