#!/usr/bin/env python3
"""Aşama 4: temp3 -> meds_database. Yalnızca verified/fixed + kanıtlı sorular yazılır."""
import json, shutil, sys, time
from pathlib import Path
import lib

DB = Path(lib.TEMP1).parent.parent / "meds_database"
OK_STATUS = {"verified", "fixed"}


def jl(path, items):
    Path(path).write_text("\n".join(json.dumps(i, ensure_ascii=False) for i in items) + "\n", encoding="utf-8")


def load_schema(name):
    p = DB / "schema" / f"{name}.schema.json"
    return json.loads(p.read_text()) if p.exists() else None


def valid(obj, schema):
    if not schema:
        return True
    try:
        import jsonschema
        jsonschema.validate(obj, schema)
        return True
    except Exception:
        return False


def main():
    t3 = Path(lib.TEMP3)
    qs = load_schema("question")
    stats = {"questions": 0, "rejected": 0, "sources": 0, "chunks": 0}
    for d in ("questions", "chunks", "index", "sources", "taxonomy", "reports"):
        (DB / d).mkdir(parents=True, exist_ok=True)

    now_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ")
    PIPELINE_GEN = "v2_local_pipeline_2026"
    PIPELINE_TAGS = ["new_pipeline", "v2_verified", "local_ai_extracted"]

    groups, rejected = {}, []
    qf = t3 / "questions.jsonl"
    if qf.exists():
        for line in qf.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            q = json.loads(line)
            # Yeni nesil ayırt edici etiketleri enjekte et
            q["pipeline_generation"] = PIPELINE_GEN
            q["tags"] = sorted(list(set(q.get("tags", []) + PIPELINE_TAGS)))
            q["created_at"] = q.get("created_at") or now_iso

            if q.get("status") in OK_STATUS and q.get("evidence") and valid(q, qs):
                groups.setdefault(str(q.get("kurul") or q.get("donem") or "genel"), []).append(q)
                stats["questions"] += 1
            else:
                rejected.append(q)
                stats["rejected"] += 1
    for k, items in groups.items():
        jl(DB / "questions" / f"{lib.fold(k).replace(' ', '_')}.jsonl", items)
    if rejected:
        Path(lib.REVIEW_DIR).mkdir(parents=True, exist_ok=True)
        jl(Path(lib.REVIEW_DIR) / "db_rejected.jsonl", rejected)

    # Kaynakları ve Chunk'ları etiketleyerek DB'ye kopyala
    for sub, key in (("sources", "sources"), ("chunks", "chunks")):
        if (t3 / sub).exists():
            for f in (t3 / sub).glob("*.json*"):
                if f.suffix == ".json":
                    try:
                        content = json.loads(f.read_text(encoding="utf-8"))
                        content["pipeline_generation"] = PIPELINE_GEN
                        content["tags"] = sorted(list(set(content.get("tags", []) + PIPELINE_TAGS)))
                        content["created_at"] = content.get("created_at") or now_iso
                        (DB / sub / f.name).write_text(json.dumps(content, ensure_ascii=False, indent=1), encoding="utf-8")
                        stats[key] += 1
                        continue
                    except Exception:
                        pass
                shutil.copy2(f, DB / sub / f.name)
                stats[key] += 1
    if (t3 / "vectors").exists():
        for f in (t3 / "vectors").glob("*.npy"):
            shutil.copy2(f, DB / "index" / f.name)

    dp = t3 / "ders_programi_taslak.json"
    if dp.exists():
        d = json.loads(dp.read_text(encoding="utf-8"))
        d["sapma_notu"] = "Saat sapmaları kaynak PDF tutarsızlığından olabilir; düşük öncelik."
        (DB / "taxonomy" / "donem3_ders_programi.json").write_text(
            json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    (DB / "reports" / "stage4.json").write_text(json.dumps(stats, indent=1))
    print(stats)


if __name__ == "__main__":
    sys.exit(main())
