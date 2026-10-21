#!/usr/bin/env python3
"""Çıkmış şık açıklaması yeniden yazımının kapısı: python3 sik_dogrula.py <parti.json> <cikti.json> → HATA listesi, 0 = geçer.
Çıktı: {"<brans>/<kod>/<no>": {"siklar": {"A": {"metin","ses"}, …5}, "ipucu"?: {metin,ses}, "cozum"?: {metin,ses}}}"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import sik_aciklama as SA
from turkce_uslup import denetle as TU

KALIP = re.compile(r'aranan özellik değil|doğru seçenektir ve klinik|fizyopatolojik mekanizma|temel gerekçesine göre|'
                   r'cevabı değil|cevap değil|olası hatalı|\[Dikkat|olarak geçmez|bu nedenle elenir$', re.I)
girdi = {q['id']: q for q in json.load(open(sys.argv[1]))}
c = json.load(open(sys.argv[2]))
e = []
for k, q in girdi.items():
    o = c.get(k)
    if not o:
        e.append(f'{k}: çıktı yok'); continue
    sk = o.get('siklar') or {}
    if sorted(sk) != list('ABCDE'):
        e.append(f'{k}: 5 şık gerekli'); continue
    parca = [(f'sik {h}', sk[h]) for h in 'ABCDE'] + [(a, o[a]) for a in ('ipucu', 'cozum') if a in o]
    for yer, v in parca:
        m, s = (v or {}).get('metin', ''), (v or {}).get('ses', '')
        if not m or not s:
            e.append(f'{k} {yer}: metin/ses boş'); continue
        if yer.startswith('sik'):
            e += [f'{k} {x}' for x in SA.denetle(m, yer)]
        e += [f'{k} {x}' for x in TU(m, yer)]
        if KALIP.search(m) or KALIP.search(s):
            e.append(f'{k} {yer}: kalıp ifade')
        if '**' in s or re.search(r'\d', s):
            e.append(f'{k} {yer}: ses metninde ** ya da rakam (sayıyı yazıyla yaz)')
    if 'doğru' not in sk[q['dogru']]['metin'].lower():
        e.append(f'{k}: doğru şık ({q["dogru"]}) açıklaması doğru olduğunu söylemiyor')
for x in e: print('HATA', x)
print(f'{len(girdi)} soru, {len(e)} HATA')
sys.exit(1 if e else 0)
