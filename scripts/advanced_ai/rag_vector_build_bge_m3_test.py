#!/usr/bin/env python3
"""
BGE-M3 TEST hattı (prod'a dokunmaz).

Farklar (test güvenliği):
- Ayrı önbellek dosyaları: vektor_onbellek_bge_m3_test.npy/.jsonl (mevcut 384'lük önbellek ASLA okunmaz/yazılmaz).
- Ayrı sync/rapor: esitleme_durumu_bge_m3_test.json, rapor_bge_m3_test.json
- ASLA DELETE yok: Supabase'e silme isteği gönderilmez (--hedef verilse bile test tablosuna upsert + silme kapalı).
- Varsayılan: yalnız yerel vektör + FTS5+dense RRF sanity (0.4 FTS5 + 0.6 BGE-M3 iskeleti mevcut hybrid_search.HybridSearchEngine ile).
- Embedding: AGENTS.md uyarınca scripts/agents/lib.py :: lib.embed (Ollama bge-m3, GPU güvenlik frenli, normalize).

Kullanım:
  .venv-ocr aktifken:
  python3 scripts/advanced_ai/rag_vector_build_bge_m3_test.py --limit 200
  python3 scripts/advanced_ai/rag_vector_build_bge_m3_test.py --limit 200 --sorgu "hiperkalsemi lityum"
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "agents"))
DB = Path(__import__("os").environ.get("MEDS_DATABASE_DIR") or ROOT.parent / "meds_database")
SRC = ROOT / "data" / "local_rag_chunks.json"
OUT = DB / "derived" / "rag_vektor"
CACHE_IDX = OUT / "vektor_onbellek_bge_m3_test.jsonl"
CACHE_NPY = OUT / "vektor_onbellek_bge_m3_test.npy"
SYNC = OUT / "esitleme_durumu_bge_m3_test.json"
REPORT = OUT / "rapor_bge_m3_test.json"
LOG = ROOT.parent / "meds_temp" / "logs" / "rag_bge_m3_test.log"
MODEL = "bge-m3"
DIM = 1024


def log(m: str):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [bge_m3_test] {m}"
    print(line, flush=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def load_chunks() -> list[dict]:
    d = json.loads(SRC.read_text(encoding="utf-8").replace("\\u0000", ""))
    rows = d if isinstance(d, list) else d.get("chunks", [])
    out = []
    for c in rows:
        txt = (c.get("content") or "").replace("\x00", "").strip()
        if len(txt) < 20 or not c.get("id"):
            continue
        out.append({"id": str(c["id"]), "hash": str(c.get("hash") or hash(txt)), "content": txt,
                    "document_id": str(c.get("documentId") or c["id"]),
                    "document_type": c.get("documentType") or "unknown",
                    "committee_id": c.get("committeeId"), "discipline": c.get("discipline"),
                    "title": c.get("title")})
    return out


def embed_all(chunks: list[dict], limit: int = 0):
    import numpy as np
    import lib as meds_lib

    OUT.mkdir(parents=True, exist_ok=True)
    idx: dict[str, int] = {}
    vecs = np.zeros((0, DIM), dtype=np.float32)
    if CACHE_IDX.exists() and CACHE_NPY.exists():
        vecs = np.load(CACHE_NPY)
        if vecs.ndim != 2 or vecs.shape[1] != DIM:
            raise SystemExit(f"HATA: test önbellek boyutu {vecs.shape} != (*, {DIM}); dosyayı silip temiz başlayın: {CACHE_NPY}")
        for line in CACHE_IDX.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            idx[r["hash"]] = r["row"]
    # Prod 384'lük önbellek bilerek okunmaz (karışma engeli).
    todo = [c for c in chunks if c["hash"] not in idx]
    if limit:
        todo = todo[:limit]
    log(f"parça: {len(chunks)} · test-önbellekte: {len(chunks) - len([c for c in chunks if c['hash'] not in idx])} · vektörlenecek: {len(todo)} (model={MODEL})")
    t0 = time.time()
    B = 512  # Ollama /api/embed için güvenli blok
    for i in range(0, len(todo), B):
        part = todo[i:i + B]
        v = meds_lib.embed(["passage: " + c["content"][:1500] for c in part], model=MODEL).astype(np.float32)
        assert v.shape[1] == DIM, f"beklenmeyen dim {v.shape}"
        base = len(vecs)
        vecs = np.vstack([vecs, v])
        with open(CACHE_IDX, "a", encoding="utf-8") as f:
            for j, c in enumerate(part):
                idx[c["hash"]] = base + j
                f.write(json.dumps({"hash": c["hash"], "row": base + j}) + "\n")
        np.save(CACHE_NPY, vecs)
        done = i + len(part)
        rate = done / max(1e-6, time.time() - t0)
        log(f"  vektörlendi {done}/{len(todo)} · {rate:.1f} parça/sn")
    return idx, vecs


def sanity_search(chunks: list[dict], idx: dict, vecs, query: str, k: int = 5):
    """FTS5 (sqlite, kelime) + BGE-M3 (dense) RRF sanity: Skor=0.4*FTS5+0.6*BGE-M3 iskeleti.
    hybrid_search.HybridSearchEngine RRF kullanır (alpha=0.6 dense ağırlığı)."""
    import sqlite3

    import numpy as np
    import lib as meds_lib
    from hybrid_search import HybridSearchEngine

    have = [c for c in chunks if c["hash"] in idx]
    sub = have[:2000]  # test altkümesi (hız)
    mat = np.array([vecs[idx[c["hash"]]] for c in sub], dtype=np.float32)
    eng_chunks = [{"chunk_id": c["id"], "text": c["content"][:1500],
                   "heading_path": [str(c.get("discipline") or ""), str(c.get("title") or "")]} for c in sub]
    eng = HybridSearchEngine(eng_chunks, mat)
    qv = meds_lib.embed(["query: " + query], model=MODEL).astype(np.float32)[0]
    res = eng.search(query, qv, top_k=k, alpha=0.6)
    # FTS5 kelime kontrolü (gen/ilaç adı kaçmasın)
    con = sqlite3.connect(":memory:")
    con.execute("CREATE VIRTUAL TABLE t USING fts5(id UNINDEXED, x)")
    con.executemany("INSERT INTO t(id,x) VALUES(?,?)", [(c["chunk_id"], c["text"]) for c in eng_chunks])
    try:
        fts = [r[0] for r in con.execute("SELECT id FROM t WHERE t MATCH ? LIMIT 5", (" OR ".join(query.split()[:6]),)).fetchall()]
    except Exception:
        fts = []
    return res, fts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=200)
    ap.add_argument("--sorgu", default="hiperkalsemi lityum hiperparatiroidi")
    a = ap.parse_args()
    if not SRC.exists():
        log(f"kaynak yok: {SRC}")
        return 1
    chunks = load_chunks()
    idx, vecs = embed_all(chunks, a.limit)
    res, fts = sanity_search(chunks, idx, vecs, a.sorgu)
    log(f"sanity sorgu: {a.sorgu}")
    for r in res:
        log(f"  RRF={r['score_rrf']} dense_rank={r['rank_dense']} bm25_rank={r['rank_bm25']} id={r['chunk_id']} txt={r['text'][:110]}...")
    log(f"  FTS5 ilk 5: {fts[:5]}")
    rep = {"zaman": time.strftime("%Y-%m-%dT%H:%M:%S"), "model": MODEL, "boyut": DIM,
           "test_parca": a.limit, "vektorlu_test": int(vecs.shape[0]), "sorgu": a.sorgu,
           "rrf_top5": [r["chunk_id"] for r in res], "fts5_top5": fts[:5],
           "not": "prod önbellek/Supabase'e dokunulmadı; DELETE yok"}
    REPORT.write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    log(f"bitti: {json.dumps(rep, ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
