#!/usr/bin/env python3
"""
Ortak veri deposu + RAG parça deposu — tüm faz verileri tek klasörden listelenir ve erişilir.

$MEDS_DATABASE_DIR/ortak/
  KATALOG.json            — her veri kümesi: yol, kayıt sayısı, açıklama, güvenilirlik, üreten betik, güncelleme
  veri/<ad>               — dağınık faz çıktılarına sembolik bağlantılar (dosyalar TAŞINMAZ; betik yolları bozulmaz)
  rag/ders_materyali.jsonl— RAG parçaları: Faz 12 temiz metin (yoksa özgün), sınav dökümleri hariç; her parçada
                            kaynak, sayfa, kurul/ders/konu (Faz 8 kaynak→konu bağı) ve kavram kimlikleri (Faz 10)
Site (localRagEngine) "lecture_slide" türüyle bu dosyayı okur. Boş sonuç mevcut dosyanın üzerine yazılmaz.
"""
from __future__ import annotations

import collections
import json
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phase8_curriculum_graph as P8  # noqa: E402

PROJECT = P8.PROJECT
DB = P8.DB
V2 = PROJECT / "meds_database_v2"
TEMP = Path(os.environ.get("MEDS_TEMP_DIR") or PROJECT / "meds_temp")
OUT = DB / "ortak"

DATASETS = [
    # ad, yol, tür, açıklama, güvenilirlik, betik
    ("sorular_veritabani", DB / "questions", "jsonl_dizin", "Yeni hattın soru veritabanı", "kaynak", "pipeline aşama 2–4"),
    ("ders_kaynaklari", DB / "sources", "json_dizin", "Ders kaynakları (PDF/PPTX) üst verisi", "kaynak", "pipeline"),
    ("ders_parcalari", DB / "chunks", "jsonl_dizin", "Ders slaytı/sayfa parçaları (özgün OCR)", "kaynak", "pipeline"),
    ("temiz_ders_notlari", DB / "derived" / "clean_notes", "jsonl_dizin", "Faz 12 temizlenmiş ders metni", "yuksek", "phase12_clean_notes.py"),
    ("mufredat_baglantilari", DB / "derived" / "curriculum_links", "dizin", "Soru–kazanım (Faz 8 yüksek + hakem), soru–slayt (Faz 11), cevap anahtarı, kavramlar", "yuksek", "publish_to_database.py"),
    ("site_analizleri", DB / "derived" / "phase_insights", "dizin", "Site paneli için birleştirilmiş analiz", "yuksek", "export_phase_insights.py"),
    ("ogren_baglantilari", DB / "derived" / "learn_links.json", "json", "Soru → Öğren destesi slaytı", "orta_yuksek", "learn_links.py"),
    ("soru_karantinasi", DB / "derived" / "quarantine", "dizin", "Bozuk/birleşik soru karantinası ve onarımlar", "kural", "quarantine_questions.py"),
    ("yeniden_bolunmus_sorular", DB / "derived" / "resplit", "dizin", "Sınav çıktısının kuralla yeniden bölünmesi", "orta", "resplit_exam_printout.py"),
    ("tibbi_varliklar", DB / "derived" / "entities", "dizin", "Faz 13 GLiNER + terminoloji varlıkları", "orta", "phase13_entities.py"),
    ("kavram_kimlikleri", V2 / "concept_ids", "dizin", "Faz 10 Wikidata/UMLS kavramları", "yuksek", "phase10_concept_ids.py"),
    ("kanitli_sozluk", V2 / "evidence_thesaurus", "dizin", "Ders materyalinden kısaltma/yazım varyantı sözlüğü", "yuksek", "build_evidence_thesaurus.py"),
    ("icd10_referans", V2 / "reference", "dizin", "WHO ICD-10 (Wikidata P494, kısmi)", "referans", "wikidata"),
    ("faz5_soru_analizi", V2 / "questions", "jsonl_dizin", "Faz 5 konsensüs (AI; ders/slayt ipuçları)", "orta", "multi_ai_consensus_phase5.py"),
    ("faz6_dogrulanmis", V2 / "deep_metadata_validated", "dizin", "Faz 6 doğrulanmış ayırıcı tanılar", "orta", "validate_phase6_metadata.py"),
    ("faz8_agac", TEMP / "phase8", "dizin", "Müfredat ağacı (kurul→ders→konu→kazanım)", "yuksek_yalniz", "phase8_curriculum_graph.py"),
    ("faz10_agac", TEMP / "phase10", "dizin", "Kimlik destekli ağaç (Faz 8 öncelikli)", "yuksek_yalniz", "phase10_concept_ids.py"),
    ("faz11_soru_slayt", TEMP / "phase11", "dizin", "Soru–slayt eşleşmeleri (tüm güven düzeyleri)", "yuksek_orta", "phase11_question_slide.py"),
    ("hakem_kararlari", TEMP / "hakem", "dizin", "Hakem kuyruğu kararları (alıntı doğrulamalı)", "yuksek", "referee_queue.py"),
    ("site_cikmis_sorular", P8.ROOT / "data" / "pastQuestions.json", "json", "Sitenin çıkmış soru arşivi (özgün; okuma sırasında karantina/düzeltme uygulanır)", "kaynak", "—"),
]


def count(p: Path, kind: str) -> int:
    try:
        if kind == "jsonl_dizin":
            return sum(sum(1 for _ in open(f, encoding="utf-8")) for f in p.glob("*.jsonl"))
        if kind in ("json_dizin",):
            return len(list(p.glob("*.json")))
        if kind == "dizin":
            return len([f for f in p.iterdir() if f.is_file()])
        if kind == "json":
            d = json.load(open(p, encoding="utf-8"))
            if isinstance(d, dict):
                for k in ("baglantilar", "items", "sorular"):
                    if isinstance(d.get(k), dict):
                        return len(d[k])
            return len(d) if isinstance(d, (list, dict)) else 0
    except Exception:
        return 0
    return 0


def build_rag(report) -> int:
    sources = P8.load_sources()
    chunks_by_src = P8.load_chunks()
    dumps = {s for s, src in sources.items() if P8.is_exam_dump(src, chunks_by_src)}
    clean = {}
    for f in (DB / "derived" / "clean_notes").glob("*.jsonl"):
        for r in P8.read_jsonl(f):
            if r.get("durum") == "temiz":
                clean[r["chunk_id"]] = r.get("metin") or ""
    konu_of = {}
    kk = TEMP / "phase8" / "kaynak_konu.jsonl"
    konular = {k["konu_id"]: k for k in P8.read_jsonl(TEMP / "phase8" / "konular.jsonl")} if (TEMP / "phase8" / "konular.jsonl").exists() else {}
    if kk.exists():
        for r in P8.read_jsonl(kk):
            if r.get("konu_id") and r["konu_id"] in konular:
                k = konular[r["konu_id"]]
                konu_of[r["kaynak_id"]] = {"kurul": k.get("kurul"), "ders": k.get("ders"), "konu": k.get("ad")}
    concepts = {}
    k10 = V2 / "concept_ids" / "kavramlar.json"
    if k10.exists():
        for cid, c in json.load(open(k10, encoding="utf-8")).items():
            for m in c.get("uyeler") or []:
                if len(m) >= 4:
                    concepts[m] = (cid, (c.get("kimlik") or {}).get("umls_cui", [None])[0])
    pat = re.compile(r"(?<![a-z0-9])(" + "|".join(re.escape(m) for m in sorted(concepts, key=len, reverse=True)) + r")(?![a-z0-9])") if concepts else None
    rows, st = [], collections.Counter()
    for sid, cs in chunks_by_src.items():
        if sid in dumps:
            st["sinav_dokumu_atlandi"] += len(cs)
            continue
        src = sources.get(sid, {})
        meta = konu_of.get(sid, {})
        for c in cs:
            text = clean.get(c.get("chunk_id")) or (c.get("text") or "")
            if len(text.strip()) < 40:
                st["kisa_atlandi"] += 1
                continue
            cids = []
            if pat:
                seen = set()
                for m in pat.finditer(P8.fold(text)):
                    cid, cui = concepts[m.group(1)]
                    if cid not in seen:
                        seen.add(cid)
                        cids.append({"kavram": cid, "cui": cui})
            rows.append({"id": c.get("chunk_id"), "doc_type": "lecture_slide", "kaynak_id": sid,
                         "kaynak": src.get("name") or sid, "sayfa": c.get("page"), "kurul": meta.get("kurul"),
                         "ders": meta.get("ders"), "konu": meta.get("konu"), "metin": text,
                         "temiz": c.get("chunk_id") in clean, "kavramlar": cids[:20]})
            st["parca"] += 1
            st["temiz_metin"] += c.get("chunk_id") in clean
            st["konulu"] += bool(meta)
    if not rows:
        return 0
    (OUT / "rag").mkdir(parents=True, exist_ok=True)
    tmp = OUT / "rag" / "ders_materyali.jsonl.tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(tmp, OUT / "rag" / "ders_materyali.jsonl")
    report["rag"] = dict(st)
    return len(rows)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "veri").mkdir(exist_ok=True)
    rep = {"zaman": time.strftime("%Y-%m-%dT%H:%M:%S")}
    n = build_rag(rep)
    cat = []
    for name, path, kind, desc, rel, script in DATASETS + [("rag_ders_materyali", OUT / "rag" / "ders_materyali.jsonl", "jsonl",
                                                           "Ortak RAG parça deposu (site arama motoru okur)", "yuksek", "build_unified_store.py")]:
        link = OUT / "veri" / name
        if path.exists() and not link.exists() and name != "rag_ders_materyali":
            try:
                link.symlink_to(path)
            except OSError:
                pass
        cnt = count(path, kind) if kind != "jsonl" else (sum(1 for _ in open(path, encoding="utf-8")) if path.exists() else 0)
        cat.append({"ad": name, "yol": str(path), "ortak_yol": str(link if name != "rag_ders_materyali" else path),
                    "tur": kind, "aciklama": desc, "guvenilirlik": rel, "uretici": script, "kayit": cnt,
                    "guncelleme": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(path.stat().st_mtime)) if path.exists() else None,
                    "var": path.exists()})
    tmp = OUT / "KATALOG.json.tmp"
    json.dump({"zaman": rep["zaman"], "veri_kumeleri": cat, "rag": rep.get("rag")}, open(tmp, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    os.replace(tmp, OUT / "KATALOG.json")
    print(json.dumps({"rag_parca": n, "rag": rep.get("rag"), "katalog": len(cat)}, ensure_ascii=False, indent=1))
    return 0 if n else 1


if __name__ == "__main__":
    sys.exit(main())
