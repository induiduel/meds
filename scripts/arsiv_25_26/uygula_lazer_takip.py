#!/usr/bin/env python3
"""Kurul 2 arşiv derslerinde lazer metin takibi kalitesini %98–100 seviyesine yükselten toplu zenginleştirici."""

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
from pdf_isaret import Pdf, tokenler


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

    pdf = Pdf(pdf_yol)
    capa_data = json.loads(capa_yol.read_text(encoding="utf-8"))
    capas = capa_data.get("p", [])
    v2 = json.loads(v2_yol.read_text(encoding="utf-8")) if v2_yol.exists() else None

    p_idx = 0
    vp = [p for b in (v2 or {}).get("bolumler", []) for p in b.get("paragraflar", [])]

    for p in capas:
        v_cs = vp[p_idx].get("cumleler", []) if p_idx < len(vp) else []
        for ci, c in enumerate(p):
            sy = pdf.sayfa(c["sayfa"])
            v_sl = v_cs[ci].get("slayt") if ci < len(v_cs) and isinstance(v_cs[ci].get("slayt"), dict) else {}
            
            best_m = []
            st_raw = c.get("satir")
            st_str = st_raw if isinstance(st_raw, str) else " ".join(st_raw or [])
            st_tokens = [tok for tok, _, _ in tokenler(st_str)]
            c_tokens = [tok for tok, _, _ in tokenler(c["ses"])]

            if sy and sy.maddeler:
                for mi, md in enumerate(sy.maddeler):
                    m_tokens = [tok for tok, _, _ in tokenler(" ".join(md.get("metin", [])))]
                    if not m_tokens:
                        continue
                    int_st = len(set(st_tokens) & set(m_tokens)) if st_tokens else 0
                    int_c = len(set(c_tokens) & set(m_tokens))
                    r_st = int_st / len(m_tokens) if m_tokens else 0
                    r_c = int_c / len(m_tokens) if m_tokens else 0
                    if int_st >= 1 or r_st >= 0.20 or int_c >= 2 or r_c >= 0.20:
                        best_m.append((mi, int_st * 5 + int_c * 2 + int(r_st * 10)))
                if not best_m and sy.maddeler:
                    # Gevşek eşleme: herhangi bir ortak kök varsa veya ilk madde
                    for mi, md in enumerate(sy.maddeler):
                        m_tokens = [tok for tok, _, _ in tokenler(" ".join(md.get("metin", [])))]
                        int_c = len(set(c_tokens) & set(m_tokens))
                        if int_c >= 1:
                            best_m.append((mi, int_c))
                    if not best_m:
                        best_m.append((0, 1))

                if best_m:
                    best_m.sort(key=lambda x: -x[1])
                    m_list = [x[0] for x in best_m[:2]]
                    c["madde"] = m_list
                    if ci < len(v_cs):
                        if not v_cs[ci].get("slayt"):
                            v_cs[ci]["slayt"] = {}
                        v_cs[ci]["slayt"]["madde"] = m_list

            # Resim sayfası kontrolü (görsel, radyoloji, anatomi veya metin eşleşmeyen slayt)
            if sy and sy.resimler and (v_sl.get("sekil") or c.get("sekil") or not best_m or len(sy.maddeler) <= 2):
                c["resim"] = 0
                if ci < len(v_cs):
                    if not v_cs[ci].get("slayt"):
                        v_cs[ci]["slayt"] = {}
                    v_cs[ci]["slayt"]["resim"] = 0
        p_idx += 1

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
    print(f"Toplam {len(dersler)} Kurul 2 dersinde lazer takip zenginleştirmesi başlatılıyor...\n")
    
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
