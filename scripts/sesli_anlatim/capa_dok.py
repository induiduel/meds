#!/usr/bin/env python3
"""Anlamsal çapa yazımı için slayt dökümü: her sayfa PNG'si üzerine pdf_isaret.Sayfa'nın gördüğü madde (M#, mavi)
ve resim (R#, kırmızı) kutuları numaralı çizilir + sayfa_<n>.txt madde metinleri. Çapa yazan (insan/ajan) cümlenin
gerçekten anlattığı yeri görüntüden seçer: data/sesli_anlatim/capa/<key>.json
  {"mdSha1": sha1(metin/<key>.md), "p": [[{"ses": "<cümlenin ilk ≥40 harfi>", "sayfa": n,
                                           "madde": [M#...] | "resim": R# | "kutu": [x0,y0,x1,y1] (0–1) | null,
                                           "sekil": "<kısa not>"}...] (paragraf başına, cümle sırasıyla)]}
Kullanım: .venv-ocr/bin/python scripts/sesli_anlatim/capa_dok.py <key> <çıktı dizini>"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pymupdf
from pdf_isaret import Sayfa, INDIR, KOK

key, out = sys.argv[1], Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
hz = json.loads((KOK / "hizalama" / f"{key}.json").read_text())
doc = pymupdf.open(INDIR / hz["dosyalar"][0]["path"])
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
    pg.get_pixmap(dpi=80).save(str(out / f"s{i:02d}.png"))
    (out / f"s{i:02d}.txt").write_text("\n".join(satir))
print(len(doc), "sayfa")
