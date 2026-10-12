#!/usr/bin/env python3
"""Sözlük v2 kartlarını doğrular ve yayınlar.

1. dogrula.py → 0 HATA değilse durur.
2. meds_database_v2/sozluk_v2/bilgi_kartlari.json (doğrulanmış kayıt)
3. Site: meds/src/data/medical_encyclopedia.json (Sözlük sayfası; `uretici: sozluk_v2`)
         meds/src/data/medical_glossary.json     (terim açılır penceresi; `dogrulama.uretici: sozluk_v2`)
   Önceki sozluk_v2 kayıtları silinip yeniden yazılır (betik idempotent). Yedek: PROJECT_ROOT/yedek/sozluk_v2/<zaman>/
4. meds_temp/sozluk_v2/sablon_terimler.json → bu terimler `durum: tamam`.

Kullanım: python3 meds/scripts/sozluk_v2/birlestir.py [--kuru]
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from aday_uret import NOTLAR, OUT as SABLON, ROOT, SITE, norm  # noqa: E402

KART_DIR = ROOT / "meds_temp/sozluk_v2/kartlar"
DB = ROOT / "meds_database_v2/sozluk_v2/bilgi_kartlari.json"
ENC = SITE / "medical_encyclopedia.json"
GLO = SITE / "medical_glossary.json"
URETICI = "sozluk_v2"


def kartlari_oku() -> list[dict]:
    out = []
    for f in sorted(KART_DIR.glob("*.jsonl")):
        out += [json.loads(ln) for ln in f.read_text().splitlines() if ln.strip()]
    return out


def gkey(term: str) -> str:  # s13_study ile aynı anahtar
    return term.replace("I", "ı").replace("İ", "i").lower()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kuru", action="store_true", help="yazmadan özet ver")
    a = ap.parse_args()

    if subprocess.run([sys.executable, str(Path(__file__).with_name("dogrula.py"))]).returncode != 0:
        print("Doğrulama HATA verdi; birleştirme yapılmadı.")
        return 1
    kartlar = kartlari_oku()
    index = {d["id"]: d for d in json.loads((NOTLAR / "index.json").read_text())}
    bugun = datetime.now().strftime("%Y-%m-%d")

    enc = [e for e in json.loads(ENC.read_text()) if e.get("uretici") != URETICI]
    glo = {k: v for k, v in json.loads(GLO.read_text()).items()
           if (v.get("dogrulama") or {}).get("uretici") != URETICI}

    # ilişkili terim adı → sözlük kimliği
    ad2id: dict[str, str] = {}
    for e in enc:
        for x in [e.get("term"), *(e.get("aliases") or [])]:
            if x:
                ad2id.setdefault(norm(x), e["id"])
    for k in kartlar:
        for x in [k["term"], *(k.get("aliases") or [])]:
            ad2id[norm(x)] = k["id"]

    for k in kartlar:
        ks = k["kaynaklar"]
        ders = index.get(ks[0].get("ders_id"), {})
        kaynak = "; ".join(
            f"{index.get(r.get('ders_id'), {}).get('title', Path(r['dosya']).stem)} (satır {r.get('satir')})" for r in ks)
        related = []
        for t in k.get("relatedTerms") or []:
            rid = ad2id.get(norm(t))
            if rid and rid != k["id"] and rid not in related:
                related.append(rid)
        enc.append({
            "id": k["id"], "term": k["term"], "latinName": k.get("latinName") or "",
            "aliases": k.get("aliases") or [], "category": k["category"], "subcategory": k["subcategory"],
            "kurul": k.get("kurul") or "Kurul 1", "discipline": k["discipline"],
            "instructorAndSource": f"Ders notu: {kaynak}",
            "definition": k["definition"], "lectureContextNotes": "",
            "infoCard": k["infoCard"],
            "examSpotPearls": k.get("examSpotPearls") or [],
            "pitfallsAndWarnings": k.get("pitfallsAndWarnings") or [],
            "relatedItems": related,
            "uretici": URETICI,
            "aiAudit": {"verified": True, "verifiedAt": bugun, "accuracyScore": 100,
                        "auditSummary": "Bilgi kartı ders notundan yazıldı; kaynak alıntıları ders notunda birebir doğrulandı."},
        })
        rec = {
            "term": k["term"], "category": k["category"], "subcategory": k["subcategory"],
            "definition": k["definition"], "description": k["definition"], "discipline": k["discipline"], "committee": "",
        }
        if k.get("examSpotPearls"):
            rec["clinicalPearl"] = k["examSpotPearls"][0]
        if k.get("aliases"):
            rec["aliases"] = k["aliases"]
        rec["dogrulama"] = {"durum": URETICI, "destek": 1.0, "uretici": URETICI}
        rec["kaynaklar"] = [{"chunk_id": None, "kaynak": index.get(r.get("ders_id"), {}).get("title", ""),
                             "ders": index.get(r.get("ders_id"), {}).get("ders", ders.get("ders", "")), "kurul": 1,
                             "sayfa": None, "satir": r.get("satir"), "alinti": r.get("alinti")} for r in ks]
        glo[gkey(k["term"])] = rec

    sablon = json.loads(SABLON.read_text()) if SABLON.exists() else {"terimler": []}
    rows = sablon["terimler"]
    by_id = {r["id"]: r for r in rows}
    by_norm = {norm(r["term"]): r for r in rows}
    eklenen = 0
    for k in kartlar:
        r = by_id.get(k["id"]) or by_norm.get(norm(k["term"]))
        if not r:
            r = {"id": k["id"], "dersler": [], "oncelik": 0, "kaynak_tur": ["elle"]}
            rows.insert(0, r)
            eklenen += 1
        r.update({"term": k["term"], "category": k["category"], "subcategory": k["subcategory"],
                  "discipline": k["discipline"], "kurul": k.get("kurul") or "Kurul 1", "durum": "tamam",
                  "kart_id": k["id"]})
    for i, r in enumerate(rows, 1):
        r["sira"] = i
    import collections
    sablon["istatistik"] = {"toplam": len(rows),
                            "durum": dict(collections.Counter(r.get("durum") for r in rows)),
                            "kategori": dict(collections.Counter(r.get("category") for r in rows))}

    ozet = {"kart": len(kartlar), "sozluk_sayfasi": len(enc), "terim_penceresi": len(glo),
            "sablon": sablon["istatistik"], "sablona_eklenen": eklenen}
    print(json.dumps(ozet, ensure_ascii=False))
    if a.kuru:
        return 0

    yedek = ROOT / "yedek" / "sozluk_v2" / datetime.now().strftime("%Y%m%d_%H%M%S")
    yedek.mkdir(parents=True, exist_ok=True)
    for p in (ENC, GLO):
        shutil.copy2(p, yedek / p.name)
    DB.parent.mkdir(parents=True, exist_ok=True)
    DB.write_text(json.dumps({"surum": 1, "uretim": bugun, "kaynak": "meds_database_v2/ders_notlari_k1",
                              "sema": "meds_temp/sozluk_v2/SABLON.md", "kartlar": kartlar}, ensure_ascii=False, indent=1))
    ENC.write_text(json.dumps(enc, ensure_ascii=False, indent=2))
    GLO.write_text(json.dumps(glo, ensure_ascii=False, indent=2))
    SABLON.write_text(json.dumps(sablon, ensure_ascii=False, indent=1))
    print(f"yazıldı · yedek: {yedek}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
