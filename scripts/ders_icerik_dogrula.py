#!/usr/bin/env python3
"""Ders içerik paketi kapısı: python3 scripts/ders_icerik_dogrula.py <key> ... → 0 HATA olmadan ders 'tamamlandı' sayılmaz.
Kaynak dışı veri yazılmaz: her kayıt slayt/sayfa kaynağı taşır, boş/yarım kayıt yok, tablo/sıra biçimi tutarlı."""
import json, os, sys, glob, re
R = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
# quiz (mini soru) ZORUNLU değil: kullanıcı kararı 2026-11-17 mini soru/quiz varsayılan kapalı, ders_icerik_uret.py quiz=[] yazar.
ZORUNLU = ['terimler', 'hastaliklar', 'bilgiler', 'spotlar', 'tablolar', 'listeler', 'kartlar']
h = 0
for key in sys.argv[1:]:
    p = os.path.join(R, 'src/data/ders_icerik', key + '.json')
    if not os.path.exists(p): print(f'HATA {key}: paket yok'); h += 1; continue
    d = json.load(open(p, encoding='utf-8')); e = []
    for k in ZORUNLU:
        # Gerekçeli muafiyet (H581 ilkesi, 2026-11-17): yalnız tablolar, yalnız kaynakta tablo yoksa ve gerekçe ≥ 12 kelimeyse
        if k == 'tablolar' and not d.get(k) and len((d.get('tablolarYok') or '').split()) >= 12:
            print(f"UYARI {key}: tablolar boş — gerekçe: {d['tablolarYok']}"); continue
        if not d.get(k): e.append(f'{k} boş (kaynakta yoksa gerekçeyle rapora yaz)')
    for t in d.get('terimler', []):
        if not t['a'].strip(): e.append(f"terim tanımsız: {t['t']}")
    for t in d.get('tablolar', []):
        if any(len(r) != len(t['h']) for r in t['r']): e.append(f"tablo satır/sütun uyumsuz: {t['t']}")
        if not t.get('n'): e.append(f"tablo kaynak adımı yok: {t['t']}")
    for l in d.get('listeler', []):
        if l['sira'] not in ('numara', 'alfa', 'azalan', 'madde'): e.append(f"liste sıra türü geçersiz: {l['t']}")
        if len(l['m']) < 2: e.append(f"liste tek maddeli: {l['t']}")
    for x in d.get('hastaliklar', []):
        if not x['bolumler']: e.append(f"hastalık/kavram bölümsüz: {x['ad']}")
        for b in x['bolumler']:
            if not b['m']: e.append(f"boş bölüm: {x['ad']}/{b['b']}")
    for q in d.get('quiz', []):
        if sum(o['d'] for o in q['o']) != 1: e.append(f"quiz tek doğru değil: {q['q'][:40]}")
    # kaynak bilgisi: her terim/bilgi/hastalık/önemli kaydı PDF sayfası (s) taşır; 'Checkpoint' gibi slayt iskeleti terim olamaz
    for k, ad in (('terimler', 't'), ('bilgiler', 'b'), ('hastaliklar', 'ad'), ('onemli', 'b')):
        ks = [x.get(ad) for x in d.get(k, []) if not x.get('s')]
        if ks: e.append(f'{len(ks)} {k} kaydında kaynak sayfa (s) yok: python3 scripts/ders_icerik_kaynak.py {key} ({ks[:3]})')
    for t in d.get('terimler', []):
        if re.match(r'(?i)^(checkpoint|oyun sayfası|tekrar sayfası)', t['t'].strip()): e.append(f"slayt iskeleti terim olamaz: {t['t']}")
    # PDF akışı: her kayıt `adim` (Öğren slayt no) taşır; eşlenemeyen (0) payı yüksekse üretim eksiktir
    kay = [x for k, v in d.items() if isinstance(v, list) for x in v if isinstance(x, dict)]
    ya = [x for x in kay if 'adim' not in x]
    if ya: e.append(f'{len(ya)} kayıtta adim yok: python3 scripts/ders_icerik_adim.py {key}')
    s0 = sum(1 for x in kay if x.get('adim') == 0)
    if kay and s0 / len(kay) > 0.05: e.append(f'adim eşlenemeyen kayıt %{100 * s0 // len(kay)} (>%5): slayt/sayfa kaynağı eksik')
    # sesli örnek soru çözücü (kaynak gösteren, şık şık açıklamalı) zorunlu
    # eşleme önce ders defteri koduyla (H608: program başlığı ≠ çözücü başlığı), sonra başlıkla
    nz = lambda t: re.sub(r'\W+', ' ', (t or '').lower()).strip()
    bas = nz(d.get('baslik'))
    kod = None
    for df in glob.glob(os.path.join(R, 'src/data/dersler/k*.json')):
        for x in json.load(open(df, encoding='utf-8')).get('dersler', []):
            if x.get('id') == key[:5]: kod = x.get('kod')
    var = False
    for ix in glob.glob(os.path.join(R, 'src/data/k[0-9]*_cozucu/index.json')):
        if 'hoca' in os.path.basename(os.path.dirname(ix)): continue
        for x in json.load(open(ix, encoding='utf-8')).get('dersler', []):
            esit = (kod and (x['kod'] == kod or x['kod'].startswith(kod + '-'))) or nz(x['baslik']) == bas
            if esit and (x.get('soru') or x.get('madde')): var = True
    if not var: e.append('sesli örnek soru çözücü yok (src/data/k2*_cozucu): üretilmeden ders tamamlanmaz')
    for e1 in e: print(f'HATA {key}: {e1}')
    h += len(e)
    print(f'{key}: {"0 HATA" if not e else str(len(e)) + " HATA"}')
sys.exit(1 if h else 0)
