"""panel_sinama.mjs için: dersin çizimlerinden panel/etiketli komutlar + sayfa görüntüleri (dizine)."""
import glob
import json
import sys
from pathlib import Path

import pymupdf

MEDS_KOK = Path(__file__).resolve().parents[3]
key, hedef = sys.argv[1].removesuffix(".json"), Path(sys.argv[2])
if "/" in key:
    key = Path(key).stem
arsiv_mi = key.startswith("y25-")
KOK = MEDS_KOK / "data" / ("arsiv_25_26/sesli_anlatim" if arsiv_mi else "sesli_anlatim")
hedef.mkdir(parents=True, exist_ok=True)
cz = json.loads((KOK / "cizim" / f"{key}.json").read_text())
hz = json.loads((KOK / "hizalama" / f"{key}.json").read_text())
if arsiv_mi:
    kurul = key.split("-")[1].replace("k", "kurul")
    pdf = str(MEDS_KOK.parent / "meds_database_25_26" / "pdf" / kurul / f"{key}.pdf")
else:
    pdfler = sorted(glob.glob(str(KOK / ".pdf_onbellek" / f"{hz['deckId']}_0_*.pdf")))
    if not pdfler:  # H91: önbellek boşsa capa_dok/cizim_uret ile aynı yol (indirme klasörü → ders PDF ucu)
        sys.path.insert(0, str(MEDS_KOK / "scripts" / "sesli_anlatim"))
        from pdf_isaret import INDIR, pdf_indir
        y = INDIR / hz["dosyalar"][0]["path"]
        pdfler = [str(y if y.exists() else pdf_indir(hz["deckId"], hz["dosyalar"][0], 0))]
    pdf = pdfler[-1]
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
