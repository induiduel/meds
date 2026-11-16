"""Konu → ders özeti haritası: önceki eşleme (ozet_konu.json) + bağsız 115 konunun ajan kararı + mevcut bağ denetimi (varsa)."""
import json, os, collections
OK = json.load(open('/home/indu/medsor/meds_temp/kurul_ders_konu/v2/ozet_konu.json'))
P = json.load(open('/home/indu/medsor/meds_temp/kurul_ders_konu/program_konulari.json'))
prog = {f"{k['kurul']}|{d['ders']}|{c['konu']}" for k in P['kurullar'] for d in k['dersler'] for c in d['konular']}
H = collections.defaultdict(dict); kaynak = collections.Counter()
den = {x['ozet']: x for x in json.load(open('ozet_cevap/mevcut_bag_karar.json'))} if os.path.exists('ozet_cevap/mevcut_bag_karar.json') else {}
for oid, v in OK.items():
    if oid in den:
        for k in den[oid]['konular']:
            key = f"{k['konu'][0]}|{k['konu'][1]}|{k['konu'][2]}"
            H[key][oid] = k.get('kapsam', 'tam'); kaynak['denetim'] += 1
    elif v.get('konu'):
        key = f"{v['konu'][0]}|{v['konu'][1]}|{v['konu'][2]}"
        H[key][oid] = 'tam'; kaynak['onceki'] += 1
for x in json.load(open('ozet_cevap/eksik_konu_karar.json')):
    key = f"{x['konu'][0]}|{x['konu'][1]}|{x['konu'][2]}"
    for o in x['ozetler']:
        H[key].setdefault(o['id'], o.get('kapsam', 'tam')); kaynak['eksik_konu_ajan'] += 1
bad = [k for k in H if k not in prog]
out = {k: [{'id': i, 'kapsam': c} for i, c in sorted(v.items(), key=lambda x: x[1] != 'tam')] for k, v in H.items() if k in prog}
json.dump(out, open('ozet_cevap/konu_ozet_haritasi.json', 'w'), ensure_ascii=False, indent=1)
print(dict(kaynak), 'konu', len(out), '/', len(prog), 'programda olmayan anahtar', len(bad), bad[:5])
