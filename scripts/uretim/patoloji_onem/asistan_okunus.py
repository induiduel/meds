"""Asistan v2 çıktılarında ders arası okunuş birliği (ses alanı): HER2 → "her tu"; src → "sark"; komplemanda Faktör I →
"faktör ı" (harf, Romen rakamı değil). Yalnız `ses` değişir; `metin` aynı kalır. Kullanım: asistan_okunus.py cikti/*.json"""
import json, re, sys


def duzelt(metin, ses):
    if re.search(r'HER-?2', metin):
        ses = re.sub(r'\b(her iki|ha e re iki|ha e er iki|insan epidermal büyüme faktörü reseptörü iki)\b', 'her tu', ses)
    ses = re.sub(r'\bsrc\b', 'sark', ses)
    if re.search(r'[Ff]aktör I\b', metin) and re.search(r'[Ff]aktör H|kompleman|MCP|CD46', metin + ses):
        ses = re.sub(r'\b([Ff]aktör) (bir|i)\b', r'\1 ı', ses)
    return ses


def gez(x, say):
    if isinstance(x, dict):
        if isinstance(x.get('metin'), str) and isinstance(x.get('ses'), str):
            yeni = duzelt(x['metin'], x['ses'])
            if yeni != x['ses']: x['ses'] = yeni; say[0] += 1
        for v in x.values(): gez(v, say)
    elif isinstance(x, list):
        for v in x: gez(v, say)


for p in sys.argv[1:]:
    o = json.load(open(p)); say = [0]; gez(o, say)
    if say[0]: json.dump(o, open(p, 'w'), ensure_ascii=False, indent=1)
    print(p, say[0], 'düzeltme')
