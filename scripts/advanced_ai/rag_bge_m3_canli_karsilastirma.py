#!/usr/bin/env python3
"""Canlı karşılaştırma: aynı sorgu -> e5(384)+match_rag_chunks_e5 vs bge-m3(1024)+match_rag_chunks_bge_m3.
Sadece OKUMA (rpc SELECT); yazma/silme yok."""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QUERIES = [
    "hiperkalsemi lityum hiperparatiroidi",
    "göğüs ağrısı ST elevasyonu troponin",
    "mikrositik anemi demir eksikliği",
]


def env() -> dict:
    e = {}
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            e[k.strip()] = v.split(" #")[0].strip().strip('"').strip("'")
    e.update({k: v for k, v in os.environ.items() if v})
    return e


def post(url: str, key: str, path: str, body: dict):
    data = json.dumps(body).encode()
    h = {"apikey": key, "Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    req = urllib.request.Request(url.rstrip("/") + path, data=data, method="POST", headers=h)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def main() -> int:
    e = env()
    url = (e.get("LOCAL_SUPABASE_URL") or e.get("SUPABASE_URL") or "http://127.0.0.1:8000").rstrip("/")
    key = e.get("LOCAL_SUPABASE_KEY") or e.get("SUPABASE_SECRET_KEY")
    # e5 sorgu vektörü (meds-embed, 384)
    for q in QUERIES:
        er = urllib.request.Request("http://127.0.0.1:8091/embed",
                                    data=json.dumps({"texts": [q], "kind": "query"}).encode(),
                                    method="POST", headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(er, timeout=30) as r:
            e5vec = json.load(r)["vectors"][0]
        # bge-m3 sorgu vektörü (Ollama, 1024)
        sys.path.insert(0, str(ROOT / "scripts" / "agents"))
        import lib as meds_lib
        bgevec = [round(float(x), 6) for x in meds_lib.embed(["query: " + q]).astype(float)[0]]
        rows_e5 = post(url, key, "/rest/v1/rpc/match_rag_chunks_e5",
                       {"query_embedding": "[" + ",".join(map(str, e5vec)) + "]", "match_count": 5})
        rows_bge = post(url, key, "/rest/v1/rpc/match_rag_chunks_bge_m3",
                        {"query_embedding": "[" + ",".join(map(str, bgevec)) + "]", "match_count": 5})
        print(f"\n=== SORGU: {q} ===")
        print("-- e5-small (384):")
        for r in rows_e5:
            print(f"  sim={r['similarity']:.4f} {r['id']} [{r.get('discipline')}] {(r.get('title') or '')[:60]}")
        print("-- bge-m3 (1024):")
        for r in rows_bge:
            print(f"  sim={r['similarity']:.4f} {r['id']} [{r.get('discipline')}] {(r.get('title') or '')[:60]}")
        ids_e5 = {r["id"] for r in rows_e5}
        ids_bge = {r["id"] for r in rows_bge}
        print(f"-- kesişim: {len(ids_e5 & ids_bge)}/5")
    return 0


if __name__ == "__main__":
    sys.exit(main())
