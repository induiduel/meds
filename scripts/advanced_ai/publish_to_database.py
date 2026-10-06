#!/usr/bin/env python3
"""
Güvenilir faz çıktılarını veritabanına yükler (faz zincirinde Faz 11'den sonra, site yayınından önce).

Hedef: $MEDS_DATABASE_DIR/derived/curriculum_links/   (kaynak sorular ve chunk'lar DEĞİŞTİRİLMEZ)
  soru_kazanim.jsonl   — yalnızca Faz 8 yüksek güven (Faz 9/10 birleşik çıktısından, karar faz8_*)
  soru_slayt.jsonl     — Faz 11 yüksek/orta güven (elle denetim ~%89)
  kavramlar.json       — Faz 10 Wikidata/UMLS kavramları
  kanitli_sozluk.json  — kanıtlı sözlükten yalnız kısaltma + yazım varyantı (yüksek/orta)
  agac.json            — müfredat ağacı (Faz 8)
  hakem_kabul.jsonl    — hakem kuyruğunda alıntısı doğrulanmış kararlar
  manifest.json        — sayılar, kaynak dosyalar, zaman, denetim notları
Güvenlik:
  * Boş ya da öncekine göre %30'dan fazla küçülen çıktı YÜKLENMEZ (önceki sürüm korunur).
  * Yazım geçici klasöre yapılır, sonra atomik değiştirilir; önceki sürüm curriculum_links.prev olarak kalır.
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT.parent
DB = Path(os.environ.get("MEDS_DATABASE_DIR") or PROJECT / "meds_database")
V2 = PROJECT / "meds_database_v2"
TEMP = Path(os.environ.get("MEDS_TEMP_DIR") or PROJECT / "meds_temp")
OUT = DB / "derived" / "curriculum_links"


def jsonl(p: Path):
    if not p.exists():
        return
    with open(p, encoding="utf-8") as f:
        for line in f:
            try:
                yield json.loads(line)
            except Exception:
                continue


def main():
    tree = next((p for p in (TEMP / "phase10" / "soru_kazanim.jsonl", TEMP / "phase9" / "soru_kazanim.jsonl") if p.exists()), None)
    kaz = [r for r in jsonl(tree)] if tree else []
    kaz = [r for r in kaz if r.get("karar") in ("faz8_faz9_ayni", "faz8_onceligi")]
    sl = [r for r in jsonl(TEMP / "phase11" / "soru_slayt.jsonl") if r.get("guven") in ("yuksek", "orta")]
    hk = [r for r in jsonl(TEMP / "hakem" / "kararlar.jsonl") if r.get("karar") == "kabul"]
    # Hakem kararlarını uygula: yalnızca sürüm 2, "emin" ve alıntısı doğrulanmış ("uygulanir") kararlar
    apply = {}
    for r in hk:
        if r.get("surum") == 2 and r.get("uygulanir"):
            apply[(r["tur"], r["soru_id"])] = r
    sl_by = {r["soru_id"]: r for r in sl}
    n_sl = n_kz = 0
    for (tur, qid), r in apply.items():
        h = r.get("hedef") or {}
        if tur == "slayt" and h.get("chunk_id"):
            base = sl_by.get(qid) or {"soru_id": qid, "slaytlar": []}
            chosen = {"source_id": h.get("source_id"), "kaynak": (r.get("secilen") or "").rsplit(" s.", 1)[0],
                      "sayfa": h.get("sayfa"), "chunk_id": h.get("chunk_id"), "alinti": r.get("alinti"),
                      "gerekce": ["hakem"], "hakem_modeli": r.get("model")}
            rest = [x for x in base.get("slaytlar", []) if x.get("chunk_id") != h.get("chunk_id")]
            sl_by[qid] = {**base, "guven": "hakem", "slaytlar": [chosen] + rest[:2]}
            n_sl += 1
        elif tur == "konu" and h.get("konu_id"):
            kaz.append({"soru_id": qid, "guven": "hakem", "karar": "hakem",
                        "kazanimlar": [{**h, "kazanim": (r.get("secilen") or "").split("kazanım:")[-1].strip(),
                                        "kanit": {"metin": r.get("alinti")}}], "hakem_modeli": r.get("model")})
            n_kz += 1
    sl = list(sl_by.values())
    known = {}
    for r in kaz:          # aynı soruda Faz 8 yüksek varsa o önceliklidir
        if r["soru_id"] not in known or known[r["soru_id"]].get("karar") == "hakem":
            known[r["soru_id"]] = r
    kaz = list(known.values())
    kav = json.load(open(V2 / "concept_ids" / "kavramlar.json", encoding="utf-8")) if (V2 / "concept_ids" / "kavramlar.json").exists() else {}
    sz = {}
    ep = V2 / "evidence_thesaurus" / "kanitli_sozluk.json"
    if ep.exists():
        for k, e in json.load(open(ep, encoding="utf-8")).items():
            keep = [s for s in e.get("esanlamlilar") or [] if (e.get("guven") or {}).get(s) in ("yuksek", "orta")
                    and ((e.get("kanit") or {}).get(s) or {}).get("tur") in ("kisaltma", "yazim_varyanti")]
            if keep:
                sz[k] = {**e, "esanlamlilar": keep, "kanit": {s: e["kanit"][s] for s in keep}, "guven": {s: e["guven"][s] for s in keep}}
    agac = TEMP / "phase8" / "agac.json"
    counts = {"hakem_uygulanan_slayt": n_sl, "hakem_uygulanan_konu": n_kz, "soru_kazanim": len(kaz), "soru_slayt": len(sl), "kavramlar": len(kav), "kanitli_sozluk": len(sz), "hakem_kabul": len(hk)}

    prev = json.load(open(OUT / "manifest.json", encoding="utf-8")).get("sayilar", {}) if (OUT / "manifest.json").exists() else {}
    for k in ("soru_kazanim", "soru_slayt", "kavramlar"):
        if counts[k] == 0:
            print(f"YÜKLENMEDİ: {k} boş — önceki sürüm korunuyor"); return 1
        if prev.get(k) and counts[k] < 0.7 * prev[k]:
            print(f"YÜKLENMEDİ: {k} {prev[k]} → {counts[k]} (%30'dan fazla düşüş) — önceki sürüm korunuyor"); return 1

    tmp = OUT.with_name("curriculum_links.tmp")
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    for name, rows in (("soru_kazanim.jsonl", kaz), ("soru_slayt.jsonl", sl), ("hakem_kabul.jsonl", hk)):
        with open(tmp / name, "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    json.dump(kav, open(tmp / "kavramlar.json", "w", encoding="utf-8"), ensure_ascii=False)
    json.dump(sz, open(tmp / "kanitli_sozluk.json", "w", encoding="utf-8"), ensure_ascii=False)
    if agac.exists():
        shutil.copy2(agac, tmp / "agac.json")
    json.dump({"zaman": time.strftime("%Y-%m-%dT%H:%M:%S"), "sayilar": counts,
               "kaynaklar": {"agac": str(tree), "slayt": str(TEMP / "phase11" / "soru_slayt.jsonl")},
               "denetim": {"soru_kazanim": "Faz 8 yüksek güven, elle 20/20 doğru/kısmen",
                           "soru_slayt": "Faz 11 yüksek/orta, elle ~%89",
                           "kanitli_sozluk": "kısaltma ~%96, yazım varyantı ~%93",
                           "kavramlar": "Wikidata birebir ad eşleşmesi + filtre, ~26/30"}},
              open(tmp / "manifest.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    old = OUT.with_name("curriculum_links.prev")
    shutil.rmtree(old, ignore_errors=True)
    if OUT.exists():
        OUT.rename(old)
    tmp.rename(OUT)
    print(json.dumps({"yuklendi": str(OUT), **counts}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
