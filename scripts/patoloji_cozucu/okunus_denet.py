#!/usr/bin/env python3
"""Ekrandaki metinde geçen kısaltma seste harf harf (harf adlarıyla) yazılmış mı? python3 okunus_denet.py <cikti.json> [...]
Her {metin, ses} çiftinde (kök/şık dahil) metindeki kısaltmanın harfleri seste bir harf-adı dizisi olarak bulunmalı; bulunmayanlar
listelenir (yerleşik okunuşlar ve Türkçe açılımla okunanlar elle kontrol edilir). Çıkış kodu her zaman 0 (yalnız rapor)."""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import kisaltma_ses as KS
O = KS.O
SERBEST = {"HER", "HELLP", "AIDS", "TORCH", "RAS", "MYC", "KIT", "MET", "BRAF", "PARP", "NOTCH", "WNT", "SMAD"}


def dizileri(ses, K):
    es = list(O.SOZ.finditer(ses)); bul, i = set(), 0
    while i < len(es):
        b = O._en_iyi(ses, es, i, K)
        if b: bul.add("".join(O.HARF[h] for h in b[1])); i = b[0]
        else: i += 1
    return bul


def ciftler(q):
    yield 'kok', q['soru'], q['kok_ses']
    for h in 'ABCDE': yield f'secenek.{h}', q['secenekler'][h], q['secenek_ses'][h]
    yield 'ipucu', q['ipucu']['metin'], q['ipucu']['ses']
    for h in 'ABCDE': yield f'siklar.{h}', q['siklar'][h]['metin'], q['siklar'][h]['ses']
    yield 'cozum', q['cozum']['metin'], q['cozum']['ses']


def denetle(q, etiket):
    out = []
    for yer, m, s in ciftler(q):
        ab = {a for a in KS.metin_kisaltmalari(m) - SERBEST if not re.fullmatch(r'[IVX]+[AB]?', a)}  # Roma rakamı: tip dört
        if not ab: continue
        bul = dizileri(s, O.kume() | ab)
        eksik = sorted(a for a in ab if a not in bul)
        if eksik: out.append(f'{etiket}.{yer}: {eksik} seste harf harf değil → ses: {s[:90]}')
    return out


if __name__ == '__main__':
    n = 0
    for p in sys.argv[1:]:
        o = json.load(open(p))
        Q = [(f's{q["no"]}', q) for q in o.get('sorular') or []] + [(f'yeni{i}', q) for i, q in enumerate(o.get('yeni') or [], 1)] \
            + [(f'cikmis:{q.get("id")}', q) for q in o.get('cikmis') or []]
        for et, q in Q:
            for x in denetle(q, f'{o["kod"]} {et}'): print('OKUNUŞ', x); n += 1
    print(f'{n} okunuş uyarısı')
