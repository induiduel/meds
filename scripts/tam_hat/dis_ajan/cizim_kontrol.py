#!/usr/bin/env python3
"""Çizim kapısı sarmalayıcısı (dış ajan protokolü §12). `cizim_dogrula.denetle` (gerçek kapı) + ek kurallar. LLM yok.
Çalıştır:  .venv-ocr/bin/python -I scripts/tam_hat/dis_ajan/cizim_kontrol.py <cizim.json> <sayfalar.md> <orijinal.pdf> <sayfa> <dok/sNN.txt>

  sayfalar.md : satırlar `P11.C2: [0]Kelime [1]kelime …` (cümle kimliği + numaralı kelimeler; çizim bas/son bu numaralardır)
  dok/sNN.txt : `M#:` madde satırları ve `R#: resim [x0,y0,x1,y1]` kutu satırları
Denetler: komut başına cizim_dogrula.denetle (kontur resim kutusu içinde ve gerçek kenar üstünde, akış uçları mürekkepte, sema ileri sızıntı yok,
şablon panelleri), cümle başına ≤2, sayfa başına ≤8, akış `kaynak_metin/hedef_metin` slaytta YAZILI ifade (M satırlarında birebir), cümle kimliği var.
`karar.json` (cizim.json'un yanında) ZORUNLU: sayfadaki her cümle için ilişki kararı —
  [{"cumle":"P11.C2","iliski":"siniflama|neden_sonuc|karsilastirma|deger|sekil|yok","cizim":true|false,"neden_yok":"çizim yoksa tıbbi gerekçe"}]
  iliski≠yok ve cizim=false ise neden_yok ≥40 karakter olmalı; iliski≠yok ama hiç komut yoksa, gerekçeler o cümleleri tek tek açıklamak zorundadır.
  Anatomik kontur/akış için «emin değilsen çizme» geçerlidir; metin ağırlıklı sayfada sınıflama/neden-sonuç/karşılaştırma/değer anlatan cümleye
  şablonlu panel (sema) çizilir. Çıkış 0 = HATA yok.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(KOK / "scripts" / "cizim"))
import cizim_dogrula as CD  # noqa: E402


def main() -> int:
    if len(sys.argv) != 6:
        print(__doc__)
        return 2
    cizim_y, sayfalar_md, pdf_y, sayfa, dok_txt = sys.argv[1], Path(sys.argv[2]), sys.argv[3], int(sys.argv[4]), Path(sys.argv[5])
    komutlar = json.loads(Path(cizim_y).read_text("utf8")).get("komutlar", [])
    cum: dict[str, list[str]] = {}
    sira: list[str] = []
    for ln in sayfalar_md.read_text("utf8").splitlines():
        m = re.match(r"(P\d+\.C\d+):\s*(.*)", ln)
        if m:
            cum[m.group(1)] = re.findall(r"\[\d+\]([^\[]+)", m.group(2)) or m.group(2).split()
            sira.append(m.group(1))
    txt = dok_txt.read_text("utf8")
    kutular, etiket_sira = [], []
    for ln in txt.splitlines():
        m = re.match(r"R(\d+):", ln)
        if m:
            kutular.append(json.loads(re.search(r"\[.*\]", ln).group(0)))
            etiket_sira.append(m.group(1))
    mlines = " ".join(ln.split(":", 1)[1] for ln in txt.splitlines() if re.match(r"M\d+:", ln))
    import fitz

    raster = CD.SayfaRaster(fitz.open(pdf_y)[sayfa - 1])
    hata: list[str] = []
    if len(komutlar) > 8:
        hata.append(f"[CIZIM-01] sayfa başına {len(komutlar)} komut (en çok 8).")
    sayac: dict[str, int] = {}
    for i, k in enumerate(komutlar):
        kim = f"komut{i}({k.get('cumle')},{k.get('tur')})"
        cid = k.get("cumle")
        if cid not in cum:
            hata.append(f"[CIZIM-02] {kim}: cümle kimliği sayfalar.md'de yok.")
            continue
        sayac[cid] = sayac.get(cid, 0) + 1
        if sayac[cid] > 2:
            hata.append(f"[CIZIM-03] {kim}: bir cümlede en çok 2 çizim.")
        onceki = " ".join(" ".join(cum[c]) for c in sira[: sira.index(cid) + 1])
        if k.get("tur") == "akis":
            for alan in ("kaynak_metin", "hedef_metin"):
                v = k.get(alan)
                if v and re.sub(r"\s+", " ", v.lower()) not in re.sub(r"\s+", " ", mlines.lower()):
                    hata.append(f"[CIZIM-04] {kim}: {alan}='{v}' slaytta YAZILI ifade değil (M satırlarında birebir yok).")
        kd_ = dict(k)
        if kd_.get("resim") is not None:  # sNN.txt etiketi (kalıcı dizin, R0 olabilir) → doğrulayıcının 1'den sıra sayısı
            m = re.fullmatch(r"R(\d+)", str(kd_["resim"]))
            if not m or m.group(1) not in etiket_sira:
                hata.append(f"[CIZIM-13] {kim}: resim='{k['resim']}' sNN.txt'de yok (var olanlar: {', '.join('R' + e for e in etiket_sira)}). Yapılacak: txt'deki etiketi AYNEN yaz.")
                continue
            kd_["resim"] = f"R{etiket_sira.index(m.group(1)) + 1}"
        try:
            ret = CD.denetle(kd_, len(cum[cid]), kutular, raster, onceki)
        except Exception as e:  # noqa: BLE001
            ret = f"kapı çalıştırılamadı: {type(e).__name__}: {e}"
        if ret:
            hata.append(f"[CIZIM-05] {kim}: {ret}. Yapılacak: bu komutu düzelt ya da SİL (emin değilsen çizme).")
    karar_y = Path(cizim_y).with_name("karar.json")
    if not karar_y.exists():
        hata.append("[CIZIM-06] karar.json yok. Yapılacak: her cümle için ilişki türünü ve çizim kararını yaz (başlık dokümanına bak).")
    else:
        kr = json.loads(karar_y.read_text("utf8"))
        kd = {x.get("cumle"): x for x in kr}
        for cid in cum:
            if cid not in kd:
                hata.append(f"[CIZIM-07] {cid}: karar.json'da yok. Yapılacak: her cümleye iliski ve cizim kararı yaz.")
        cizilen = {k.get("cumle") for k in komutlar}
        for cid, x in kd.items():
            if x.get("iliski") not in ("siniflama", "neden_sonuc", "karsilastirma", "deger", "sekil", "yok"):
                hata.append(f"[CIZIM-08] {cid}: iliski değeri geçersiz ({x.get('iliski')}).")
            elif x.get("iliski") != "yok" and x.get("cizim") is False and len(str(x.get("neden_yok", ""))) < 40:
                hata.append(f"[CIZIM-09] {cid}: ilişki ({x['iliski']}) var, çizim yok; neden_yok ≥40 karakterlik TIBBİ gerekçe olmalı (örn. kural numarası + o cümlede neden uygun değil).")
            if x.get("cizim") is True and cid not in cizilen:
                hata.append(f"[CIZIM-10] {cid}: karar 'cizim' ama cizim.json'da komut yok.")
            if cid in cizilen and x.get("cizim") is not True:
                hata.append(f"[CIZIM-11] {cid}: komut var ama karar.json 'cizim: true' demiyor.")
        if not komutlar and any(x.get("iliski") not in ("yok", None) for x in kr):
            hata.append("[CIZIM-12] sayfada ilişki anlatan cümle var ama hiç çizim yok. Yapılacak: en güçlü ilişkiyi şablonlu paneli (sema) ile çiz; yalnız anatomik kontur/akış için «emin değilsen çizme» geçerlidir.")
    for h in hata:
        print("HATA", h)
    print(f"{'BAŞARISIZ' if hata else 'GEÇTİ'}: {len(komutlar)} komut, {len(hata)} hata")
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main())
