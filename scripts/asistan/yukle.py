#!/usr/bin/env python3
"""Tıp Asistanı F1: belgeler.jsonl + vektör önbelleği → meds-pg asistan_belge (artımlı, tek COPY + ON CONFLICT).
Çalıştır: meds/.venv-ocr/bin/python scripts/asistan/yukle.py [--kuru]
Kaynakta olmayan satırlar silinir; kaynak %50'den fazla küçülmüşse silme yapılmaz (güvenlik eşiği)."""
import argparse, glob, hashlib, io, json, os, sys
import numpy as np, psycopg
sys.path.insert(0, os.path.dirname(__file__))
from metin import fold, kokler
KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
GIRDI = os.path.join(KOK, '..', 'meds_temp', 'asistan', 'belgeler.jsonl')
DIZIN = os.path.join(KOK, '..', 'meds_temp', 'asistan', 'vektor')


def env_url():
    for l in open(os.path.join(KOK, '.env'), encoding='utf-8'):
        if l.startswith('DATABASE_URL='): return l.split('=', 1)[1].strip().strip('"\'')
    return 'postgres://meds@127.0.0.1:54330/meds'


def temiz(s):
    """Postgres NUL ve denetim karakterlerini reddeder."""
    return ''.join(c for c in (s or '') if c in '\n\t' or ord(c) >= 32)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--kuru', action='store_true'); a = ap.parse_args()
    belgeler = [json.loads(l) for l in open(GIRDI, encoding='utf-8')]
    vek = {}
    for p in sorted(glob.glob(os.path.join(DIZIN, 'parca_*.npz'))):
        z = np.load(p, allow_pickle=False)
        for i, o, v in zip(z['id'].tolist(), z['ozet'].tolist(), z['vec']):
            vek[(i, o)] = v
    con = psycopg.connect(env_url()); cur = con.cursor()
    cur.execute('select id, ozet, embedding is not null from asistan_belge')
    mevcut = {r[0]: (r[1], r[2]) for r in cur.fetchall()}
    yeni = []
    for b in belgeler:
        oz = hashlib.md5((b['baslik'] + '|' + b['metin']).encode()).hexdigest()
        if mevcut.get(b['id']) == (oz, True): continue
        v = vek.get((b['id'], oz))
        yeni.append((b, oz, v))
    silinecek = [i for i in mevcut if i not in {b['id'] for b in belgeler}]
    vektorsuz = sum(1 for _, _, v in yeni if v is None)
    print(f'kaynak {len(belgeler)}, DB {len(mevcut)}, yazılacak {len(yeni)} (vektörsüz {vektorsuz}), silinecek {len(silinecek)}')
    if a.kuru: return
    if mevcut and len(belgeler) < 0.5 * len(mevcut): sys.exit('Kaynak yarıdan fazla küçülmüş: durdum')
    for i in range(0, len(yeni), 500):
        parca = yeni[i:i + 500]
        cur.execute('create temp table _y (id text, tur text, baslik text, metin text, ders text, kurul int, brans text, url text, kaynak text, meta text, ozet text, baslik_f text, arama text, embedding text) on commit drop')
        with cur.copy('copy _y from stdin') as cp:
            for b, oz, v in parca:
                f = fold(b['baslik'] + ' ' + b['metin'])
                emb = None if v is None else '[' + ','.join(f'{x:.6f}' for x in v.astype('float32')) + ']'
                cp.write_row([b['id'], b['tur'], temiz(b['baslik']).replace('\n', ' '), temiz(b['metin']), b['ders'], b['kurul'], b['brans'], b['url'], b['kaynak'],
                              json.dumps(b['meta'], ensure_ascii=False, default=str), oz, fold(b['baslik']), kokler(f), emb])
        cur.execute('''insert into asistan_belge (id,tur,baslik,metin,ders,kurul,brans,url,kaynak,meta,ozet,baslik_f,arama,embedding)
            select id,tur,baslik,metin,ders,kurul,brans,url,kaynak,meta::jsonb,ozet,baslik_f,arama,embedding::vector from _y
            on conflict (id) do update set tur=excluded.tur,baslik=excluded.baslik,metin=excluded.metin,ders=excluded.ders,kurul=excluded.kurul,
              brans=excluded.brans,url=excluded.url,kaynak=excluded.kaynak,meta=excluded.meta,ozet=excluded.ozet,baslik_f=excluded.baslik_f,
              arama=excluded.arama,embedding=coalesce(excluded.embedding, case when asistan_belge.ozet=excluded.ozet then asistan_belge.embedding end),guncel=now()''')
        con.commit(); print(f'  {min(i + 500, len(yeni))}/{len(yeni)}', flush=True)
    if silinecek:
        cur.execute('delete from asistan_belge where id = any(%s)', (silinecek,)); con.commit()
    cur.execute('select count(*), count(embedding) from asistan_belge'); print('DB:', cur.fetchone())


if __name__ == '__main__':
    main()
