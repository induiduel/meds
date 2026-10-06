#!/usr/bin/env python3
"""
Faz 13 — Tıbbi varlık tanıma ve terminoloji eşleme (GLiNER + spaCy PhraseMatcher)

1. Terminoloji (resmî kimlikli): Faz 10 Wikidata kavramları (UMLS CUI / MeSH / ICD-10 / DO), WHO ICD-10 Türkçe adları
   (Wikidata P494, meds_database_v2/reference/icd10.tsv), kanıtlı sözlük (kısaltma + yazım varyantı).
   spaCy PhraseMatcher (Türkçe katlanmış metin üzerinde) ile tamlama bazlı eşleme → kavram kimliği.
2. GLiNER (urchade/gliner_multi-v2.1, çok dilli, sıfır atış): önceden tanımlı sözlükte olmayan tamlamalar da bulunur.
   Etiketler: hastalık, ilaç, patojen, anatomik yapı, laboratuvar testi, belirti, gen veya protein, tedavi yöntemi.
3. Birleştirme: GLiNER varlığı sözlükte varsa kavram kimliği alır ("kimlikli"); yoksa "kimliksiz" (yalnız arama ipucu,
   kanıt değildir). PhraseMatcher eşleşmeleri GLiNER kaçırsa da eklenir.
BERTurk BIO NER: hazır Türkçe biyomedikal NER kontrol noktası yok → GLiNER sıfır atış kullanılır.
CPU'da çalışır (GPU Ollama'ya ayrılmıştır). Artımlı: işlenen soru tekrar işlenmez (--full: hepsi).
Çıktı: $MEDS_DATABASE_DIR/derived/entities/soru_varliklar.jsonl, terminoloji.json, rapor.json
"""
from __future__ import annotations

import collections
import json
import os
import re
import sys
import time
from pathlib import Path

if os.environ.get("MEDS_GPU_OK") != "1":          # zincir GPU'yu boşaltmadıysa CPU (Ollama ile yan yana CUDA yok)
    os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")
sys.path.insert(0, str(Path(__file__).resolve().parent))
import phase8_curriculum_graph as P8  # noqa: E402

V2 = P8.PROJECT / "meds_database_v2"
OUT = P8.DB / "derived" / "entities"
LABELS = {"hastalık": "hastalik", "ilaç": "ilac", "patojen": "patojen", "anatomik yapı": "anatomi",
          "laboratuvar testi": "test", "belirti": "belirti", "gen veya protein": "gen_protein", "tedavi yöntemi": "tedavi"}
GLINER_MODEL = os.environ.get("MEDS_GLINER_MODEL", "urchade/gliner_multi-v2.1")


def build_terminology() -> dict:
    """katlanmış ifade → {kavram, ad, kimlik, kaynak}"""
    term = {}
    k10 = V2 / "concept_ids" / "kavramlar.json"
    if k10.exists():
        for cid, c in json.load(open(k10, encoding="utf-8")).items():
            for m in c.get("uyeler") or []:
                if len(m) >= 3:
                    term[m] = {"kavram": cid, "ad": c.get("tr") or c.get("en"), "kimlik": c.get("kimlik") or {}, "kaynak": "wikidata"}
    icd = V2 / "reference" / "icd10.tsv"
    if icd.exists():
        for line in open(icd, encoding="utf-8"):
            if line.startswith("#") or "\t" not in line:
                continue
            code, names = line.rstrip("\n").split("\t", 1)
            for nm in names.split(" | "):
                f = P8.fold(nm)
                if len(f) >= 5 and f not in term:
                    term[f] = {"kavram": f"icd:{code}", "ad": nm, "kimlik": {"icd10": [code]}, "kaynak": "icd10_who"}
    ev = V2 / "evidence_thesaurus" / "kanitli_sozluk.json"
    if ev.exists():
        for k, e in json.load(open(ev, encoding="utf-8")).items():
            base = P8.fold(e.get("turkce") or k)
            syns = [s for s in e.get("esanlamlilar") or [] if (e.get("guven") or {}).get(s) in ("yuksek", "orta")
                    and ((e.get("kanit") or {}).get(s) or {}).get("tur") in ("kisaltma", "yazim_varyanti")]
            if not syns:
                continue
            cid = (term.get(base) or {}).get("kavram") or f"sozluk:{base}"
            for f in [base] + [P8.fold(s) for s in syns]:
                if len(f.replace(" ", "")) >= 3 and f not in term:
                    term[f] = {"kavram": cid, "ad": e.get("turkce") or k, "kimlik": {}, "kaynak": "kanitli_sozluk"}
    return term


def main():
    full = "--full" in sys.argv
    t0 = time.time()
    import spacy
    from spacy.matcher import PhraseMatcher
    term = build_terminology()
    nlp = spacy.blank("xx")
    matcher = PhraseMatcher(nlp.vocab)
    keys = list(term)
    for i in range(0, len(keys), 5000):
        matcher.add("TERM", [nlp.make_doc(k) for k in keys[i:i + 5000]])
    OUT.mkdir(parents=True, exist_ok=True)
    json.dump({"ifade": len(term), "kaynak": dict(collections.Counter(v["kaynak"] for v in term.values()))},
              open(OUT / "terminoloji.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    from gliner import GLiNER
    model = GLiNER.from_pretrained(GLINER_MODEL)
    pq = json.load(open(P8.ROOT / "data" / "pastQuestions.json", encoding="utf-8"))
    pq = pq if isinstance(pq, list) else pq.get("questions", [])
    outp = OUT / "soru_varliklar.jsonl"
    done = set()
    if outp.exists() and not full:
        for r in P8.read_jsonl(outp):
            done.add(r["soru_id"])
    st = collections.Counter()
    mode = "w" if full else "a"
    with open(outp, mode, encoding="utf-8") as f:
        for n, q in enumerate(pq):
            qid = str(q.get("id"))
            if qid in done:
                continue
            stem = q.get("stem") or (q.get("reconstruction") or {}).get("stem") or ""
            opts = " ; ".join(o.get("text", "") for o in (q.get("options") or []) if isinstance(o, dict))
            text = re.sub(r"\s+", " ", f"{stem} ; {opts}").strip()[:1200]
            if len(text) < 15:
                continue
            ents = {}
            # 1) terminoloji (tamlama bazlı, kimlikli)
            doc = nlp.make_doc(P8.fold(text))
            for _, s, e in matcher(doc):
                span = doc[s:e].text
                t = term[span]
                k = t["kavram"]
                if k not in ents or len(span) > len(ents[k]["metin"]):
                    ents[k] = {"metin": span, "tur": None, "kavram": k, "ad": t["ad"], "kimlik": t["kimlik"], "kaynak": t["kaynak"]}
            # 2) GLiNER (sıfır atış)
            try:
                preds = model.predict_entities(text, list(LABELS), threshold=0.45)
            except Exception:
                preds = []
            for p in preds:
                f = P8.fold(p["text"])
                tur = LABELS.get(p["label"])
                t = term.get(f)
                if t:
                    k = t["kavram"]
                    ents.setdefault(k, {"metin": p["text"], "kavram": k, "ad": t["ad"], "kimlik": t["kimlik"], "kaynak": t["kaynak"]})
                    ents[k]["tur"] = tur
                    ents[k]["gliner_skor"] = round(p["score"], 3)
                    st["gliner_kimlikli"] += 1
                elif len(f) >= 3:
                    ents[f"g:{f}"] = {"metin": p["text"], "tur": tur, "kavram": None, "kaynak": "gliner",
                                      "gliner_skor": round(p["score"], 3)}
                    st["gliner_kimliksiz"] += 1
            st["soru"] += 1
            st["kimlikli_varlik"] += sum(1 for v in ents.values() if v.get("kavram"))
            f.write(json.dumps({"soru_id": qid, "varliklar": list(ents.values())}, ensure_ascii=False) + "\n")
            if st["soru"] % 250 == 0:
                print(f"[{time.strftime('%H:%M:%S')}] [faz13] {st['soru']} soru", flush=True)
                f.flush()
    rep = {"zaman": time.strftime("%Y-%m-%dT%H:%M:%S"), "terminoloji_ifade": len(term), **dict(st),
           "model": GLINER_MODEL, "sure_sn": round(time.time() - t0)}
    json.dump(rep, open(OUT / "rapor.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(rep, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
