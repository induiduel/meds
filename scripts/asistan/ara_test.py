#!/usr/bin/env python3
"""F1 sınama: karma aramanın ilk-5 isabeti. Çalıştır: meds/.venv-ocr/bin/python scripts/asistan/ara_test.py
Her satır: (soru, ilk 5 içinde başlık/ders/metin/url'de aranacak kök sözcükler [biri yeter], beklenen tür [isteğe bağlı])"""
import json, os, sys, urllib.request
sys.path.insert(0, os.path.dirname(__file__))
import psycopg
from metin import sorgu
from yukle import env_url
SORULAR = [
 ("anamnez nedir", ["anamnez"], None), ("patolojide rutin fiksatif hangisi", ["formalin"], None),
 ("parkinson hastalığı belirtileri", ["parkinson"], None), ("MS multipl skleroz", ["skleroz"], None),
 ("nistatin hangi gruptan ilaç", ["nistatin"], None), ("hipertansiyon tedavisi", ["hipertansiyon"], None),
 ("aşı takvimi", ["asi"], None), ("sesli soru çözücüye nasıl giderim", ["cozucu"], "sayfa"),
 ("en önemli konular nerede", ["onemli"], "sayfa"), ("kurul takvimi", ["takvim"], "sayfa"),
 ("renal hücreli karsinom", ["renal"], None), ("gogus agrisi", ["agri"], None),
 ("kronik enflamasyon granülom", ["granulom"], None), ("ADH ne demek", ["adh","antidiy","alkol"], None),
 ("inme serebrovasküler", ["inme","serebro"], None), ("nörolojik muayene", ["noroloji","muayene"], None),
]
def emb(t):
    r = urllib.request.Request('http://127.0.0.1:8094/embed', json.dumps({'texts': [t], 'kind': 'raw'}).encode(), {'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(r, timeout=60))['vectors'][0]
con = psycopg.connect(env_url()); cur = con.cursor(); ok = 0
for q, anah, tur in SORULAR:
    f, k = sorgu(q); v = emb(q)
    cur.execute("select a.id,a.tur,a.baslik,a.url,a.ders||' '||b.metin,a.skor from asistan_ara(%s::vector,%s,%s,5) a join asistan_belge b using (id)", ('[' + ','.join(map(str, v)) + ']', f, k))
    rows = cur.fetchall()
    metin = ' '.join(r[2] + ' ' + r[3] + ' ' + r[4] for r in rows)
    from metin import fold
    isabet = any(a in fold(metin) for a in anah) and (tur is None or any(r[1] == tur for r in rows))
    ok += isabet
    print(('OK  ' if isabet else 'YOK '), q, '→', rows[0][1], '|', rows[0][2][:50] if rows else '-')
print(f'{ok}/{len(SORULAR)} isabet')
