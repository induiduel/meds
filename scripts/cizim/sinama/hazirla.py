"""panel_sinama.mjs için: dersin çizimlerinden panel/etiketli komutlar + sayfa görüntüleri (dizine)."""
import glob
import json
import sys
from pathlib import Path

import pymupdf

KOK = Path(__file__).resolve().parents[3] / "data" / "sesli_anlatim"
key, hedef = sys.argv[1], Path(sys.argv[2])
hedef.mkdir(parents=True, exist_ok=True)
cz = json.loads((KOK / "cizim" / f"{key}.json").read_text())
hz = json.loads((KOK / "hizalama" / f"{key}.json").read_text())
pdf = sorted(glob.glob(str(KOK / ".pdf_onbellek" / f"{hz['deckId']}_0_*.pdf")))[-1]
doc = pymupdf.open(pdf)
komut, oran = {}, {}
for cs in cz["p"].values():
    for v in cs.values():
        for k in v:
            if k["tur"] == "sema" or k.get("etiket_konum"):
                komut.setdefault(str(k["s"]), []).append(k)
for s in komut:
    pg = doc[int(s) - 1]
    oran[s] = pg.rect.width / pg.rect.height
    pg.get_pixmap(dpi=72).save(str(hedef / f"s{s}.png"))
(hedef / "veri.json").write_text(json.dumps({"oran": oran, "komut": komut}, ensure_ascii=False))
(hedef / "index.html").write_text('<!doctype html><meta charset=utf-8><link rel=stylesheet href=giris.css>'
                                  '<style>*{animation:none!important;transition:none!important}</style>'
                                  '<body style="margin:0;background:#333"><div id=r></div><script src=giris.js></script>')
print(sum(len(v) for v in komut.values()))
