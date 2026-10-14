import json, sys, os
D = os.path.dirname(os.path.abspath(__file__)); h = 0
for pid in sys.argv[1:]:
    p = json.load(open(f'{D}/parti/{pid}.json'))
    try: s = {x['id']: x for x in json.load(open(f'{D}/sonuc/{pid}.json'))}
    except Exception as e: print(pid, 'HATA okunamadı', e); h += 1; continue
    for q in p['sorular']:
        x = s.get(q['id'])
        if not x: print(pid, q['id'], 'HATA eksik'); h += 1; continue
        if not isinstance(x.get('anlamsal'), (int, float)) or not 0 <= x['anlamsal'] <= 100: print(pid, q['id'], 'HATA anlamsal'); h += 1
        if x.get('pasaj') not in range(len(q['pasajlar'])): print(pid, q['id'], 'HATA pasaj'); h += 1
    print(pid, len(p['sorular']), len(s))
print(f'{h} HATA')
