import json, sys, os
D = os.path.dirname(os.path.abspath(__file__))
hata = 0
for pid in sys.argv[1:]:
    p = json.load(open(f'{D}/parti/{pid}.json'))
    try: s = json.load(open(f'{D}/sonuc/{pid}.json'))
    except Exception as e: print(pid, 'HATA: sonuç okunamadı', e); hata += 1; continue
    by = {x.get('cift'): x for x in s}
    for c in p['ciftler']:
        x = by.get(c['cift'])
        if not x: print(pid, c['cift'], 'HATA: eksik'); hata += 1; continue
        if x.get('a') != c['A']['id'] or x.get('b') != c['B']['id']: print(pid, c['cift'], 'HATA: kimlik uyuşmuyor'); hata += 1
        if x.get('karar') not in ('AYNI', 'VARYANT', 'FARKLI'): print(pid, c['cift'], 'HATA: karar'); hata += 1
    print(pid, 'çift', len(p['ciftler']), 'sonuç', len(s))
print(f'{hata} HATA')
