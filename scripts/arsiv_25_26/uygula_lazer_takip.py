#!/usr/bin/env python3
"""Kurul 2 arşiv derslerinde uydurma madde/resim çapalarını temizleyip PDF işaretini yeniden üretir (H59).

Kullanım: .venv-ocr/bin/python scripts/arsiv_25_26/uygula_lazer_takip.py [key ...]  (anahtarsız: dersler.json)"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")

MEDS = Path(__file__).resolve().parents[2]
ROOT = MEDS.parent
SA_KOK = MEDS / "data" / "arsiv_25_26" / "sesli_anlatim"
DB_25_26 = ROOT / "meds_database_25_26"

sys.path.insert(0, str(MEDS / "scripts" / "sesli_anlatim"))
sys.path.insert(0, str(MEDS / "scripts" / "arsiv_25_26"))

import arsiv_yayinla as AY



def zenginlestir_ders(key: str) -> tuple[int, int, float, float]:
    pdf_yol = DB_25_26 / "pdf" / "kurul2" / f"{key}.pdf"
    if not pdf_yol.exists():
        # Aday pdf kontrolü
        adaylar = list((DB_25_26 / "pdf" / "kurul2").glob(f"*{key}*.pdf"))
        if not adaylar:
            print(f"[{key}] PDF bulunamadı: {pdf_yol}")
            return (0, 0, 0.0, 0.0)
        pdf_yol = adaylar[0]

    capa_yol = SA_KOK / "capa" / f"{key}.json"
    hz_yol = SA_KOK / "hizalama" / f"{key}.json"
    metin_yol = SA_KOK / "metin" / f"{key}.md"
    v2_yol = SA_KOK / "v2" / f"{key}.json"

    if not capa_yol.exists() or not hz_yol.exists() or not metin_yol.exists():
        print(f"[{key}] Gerekli dosyalar eksik")
        return (0, 0, 0.0, 0.0)

    capa_data = json.loads(capa_yol.read_text(encoding="utf-8"))
    capas = capa_data.get("p", [])
    v2 = json.loads(v2_yol.read_text(encoding="utf-8")) if v2_yol.exists() else None

    # H59 (2026-10-25): bu betik eskiden her cümleye en yakın maddeyi (yoksa M0) ve görselli sayfada "resim: 0" basıp
    # kapsamayı şişiriyordu; lazer şekil/tablo yerine yazıya gidiyordu. Artık yalnız o uydurma dizinleri SİLER; yazarın
    # satir/sekil/tablo çapası korunur, işaret pdf_isaret (şekil önceliği) ile yeniden üretilir.
    vp = [p for b in (v2 or {}).get("bolumler", []) for p in b.get("paragraflar", [])]
    # "el": görüntüye bakılarak yazılmış çapa (sekil_capa_uygula.py) — korunur
    for p in capas:
        for c in p:
            if not c.get("el"):
                c.pop("madde", None)
                c.pop("resim", None)
    for p in vp:
        for c in p.get("cumleler", []):
            if isinstance(c.get("slayt"), dict) and not c["slayt"].get("el"):
                c["slayt"].pop("madde", None)
                c["slayt"].pop("resim", None)

    # Kaydet capa ve v2
    capa_data["p"] = capas
    capa_yol.write_text(json.dumps(capa_data, ensure_ascii=False, indent=1), encoding="utf-8")
    taslak_capa = DB_25_26 / "taslak" / key / "konusma_capalari.json"
    if taslak_capa.exists():
        taslak_capa.write_text(json.dumps(capas, ensure_ascii=False, indent=1), encoding="utf-8")

    if v2 and v2_yol.exists():
        v2_yol.write_text(json.dumps(v2, ensure_ascii=False, indent=1), encoding="utf-8")
        taslak_v2 = DB_25_26 / "taslak" / key / "konusma_v2.json"
        if taslak_v2.exists():
            taslak_v2.write_text(json.dumps(v2, ensure_ascii=False, indent=1), encoding="utf-8")

    pars = AY.metin_paragraflari(metin_yol.read_text(encoding="utf-8"))
    hz = json.loads(hz_yol.read_text(encoding="utf-8"))
    metin_sha1 = hashlib.sha1("\n".join(p["t"] for p in pars).encode("utf-8")).hexdigest()

    isr = AY.pdf_isaret_yerel(key, pars, pdf_yol, hz, capas, metin_sha1, v2)
    l_cnt = sum(1 for cs in isr["c"].values() for c in cs if c and c.get("l"))
    w_cnt = sum(1 for cs in isr["c"].values() for c in cs if c and c.get("w"))
    tot_cnt = sum(len(cs) for cs in isr["c"].values())

    pct_l = round(l_cnt / tot_cnt * 100, 1) if tot_cnt else 0
    pct_w = round(w_cnt / tot_cnt * 100, 1) if tot_cnt else 0
    return (l_cnt, tot_cnt, pct_l, pct_w)


def main():
    dersler_yol = SA_KOK / "dersler.json"
    dersler = json.loads(dersler_yol.read_text(encoding="utf-8"))
    if len(sys.argv) > 1:
        dersler = [d for d in dersler if d["key"] in sys.argv[1:]]
    print(f"Toplam {len(dersler)} Kurul 2 dersinde çapa temizliği ve işaret yeniden üretimi başlatılıyor...\n")
    
    ozet = []
    for d in dersler:
        k = d["key"]
        l_cnt, tot_cnt, pct_l, pct_w = zenginlestir_ders(k)
        print(f"[{k:<38}] {l_cnt:3d}/{tot_cnt:3d} ({pct_l:5.1f}%) satır vurgusu | {pct_w:5.1f}% kelime")
        ozet.append((k, d["baslik"], l_cnt, tot_cnt, pct_l, pct_w))
        
    print("\n" + "=" * 70)
    print("TAMAMLANDI. En düşük 5 ders:")
    for x in sorted(ozet, key=lambda it: it[4])[:5]:
        print(f"  {x[0]}: {x[2]}/{x[3]} ({x[4]}%)")


if __name__ == "__main__":
    main()
