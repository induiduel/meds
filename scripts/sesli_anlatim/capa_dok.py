#!/usr/bin/env python3
"""Anlamsal çapa yazımı için slayt dökümü: her sayfa PNG'si üzerine pdf_isaret.Sayfa'nın gördüğü madde (M#, mavi)
ve resim (R#, kırmızı) kutuları numaralı çizilir + metin dökümü; cümle listesi (cumleler.md, sunucu bölmesiyle).
Çapa yazan (insan/ajan) cümlenin gerçekten anlattığı yeri görüntüden seçer → data/sesli_anlatim/capa/<key>.json
  {"mdSha1": sha1(metin/<key>.md), "p": [[{"ses": "<cümlenin başı>", "sayfa": n, "dosya": d (çok dosyalı),
     "madde": [M#...] | "resim": R# | "kutu": [x0,y0,x1,y1] (0–1),
     "yol": [{"k": "cümlede geçen ifade", "x": 0–1, "y": 0–1}, ...]  # hareketli imleç (resim anlatımı)
   }...] (paragraf başına, cümle sırasıyla)]}
Dosyalar: <çıktı>/d<dosya>_s<NN>.png/.txt (tek dosyalıda sNN.png/.txt), cumleler.md.
Kullanım: .venv-ocr/bin/python scripts/sesli_anlatim/capa_dok.py <key> <çıktı dizini>  (3000 açık olmalı)"""
import json, os, sys, urllib.request
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pymupdf
from pdf_isaret import Sayfa, INDIR, KOK, API, cumle_sonlari, pdf_indir

_op = urllib.request.build_opener(); _op.addheaders = [('User-Agent', 'medsor-capa/1')]; urllib.request.install_opener(_op)  # Oracle 403'ü önler
key, out = sys.argv[1], Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
hz = json.loads((KOK / "hizalama" / f"{key}.json").read_text())
cok = len(hz["dosyalar"]) > 1
for fi, f in enumerate(hz["dosyalar"]):
    yol = INDIR / f["path"]
    if not yol.exists():
        yol = pdf_indir(hz["deckId"], f, fi)
    if not yol or not Path(yol).exists():
        print("PDF YOK", fi, f["path"]); continue
    doc = pymupdf.open(yol)
    for i, pg in enumerate(doc, 1):
        sy = Sayfa(pg)
        satir = []
        for mi, m in enumerate(sy.maddeler):
            r = pymupdf.Rect(min(x[0] for x in m["satirlar"]), min(x[1] for x in m["satirlar"]), max(x[2] for x in m["satirlar"]), max(x[3] for x in m["satirlar"]))
            pg.draw_rect(r, color=(0, 0, 1), width=0.8)
            pg.insert_text((r.x0 - 2, r.y0 + 6), f"M{mi}", fontsize=7, color=(0, 0, 1))
            satir.append(f"M{mi}: {' '.join(m['metin'])}")
        for ri, b in enumerate(sy.resimler):
            r = pymupdf.Rect(b); pg.draw_rect(r, color=(1, 0, 0), width=1.2)
            pg.insert_text((r.x0 + 2, r.y0 + 10), f"R{ri}", fontsize=10, color=(1, 0, 0))
            satir.append(f"R{ri}: resim {sy.n(b)}")
        ad = f"d{fi}_s{i:02d}" if cok else f"s{i:02d}"
        pg.get_pixmap(dpi=80).save(str(out / f"{ad}.png"))
        (out / f"{ad}.txt").write_text("\n".join(satir))
    print(f"dosya {fi}: {len(doc)} sayfa ({yol})")
d = json.load(urllib.request.urlopen(f"{API}/api/canli-ders/{key}"))
satir = []; pi = 0
for b in d["bolumler"]:
    satir.append(f"\n### BÖLÜM: {b['baslik']}")
    for p in b["paragraflar"]:
        es = hz["paragraflar"][pi] if pi < len(hz["paragraflar"]) else None; pi += 1
        ip = f"eski tahmin: dosya {es.get('dosya', 0)} sayfa {es.get('sayfa')}" if es else "eski tahmin yok"
        satir.append(f"\n## P{p['i']} ({ip})")
        m = p["metin"]; a = 0
        for ci, e in enumerate(cumle_sonlari(m)):
            satir.append(f"P{p['i']}.C{ci}: {m[a:e].strip()}"); a = e
(out / "cumleler.md").write_text("\n".join(satir))
