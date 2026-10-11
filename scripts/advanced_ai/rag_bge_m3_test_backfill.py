#!/usr/bin/env python3
"""BGE-M3 TEST backfill: test önbelleğindeki vektörleri yerel Supabase rag_chunks.embedding_bge_m3'e yazar.
Güvenlik: yalnız UPSERT (id), DELETE YOK, yalnız content_hash_bge_m3 değişenler. Prod embedding_e5'e dokunmaz."""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DB = Path(os.environ.get("MEDS_DATABASE_DIR") or ROOT.parent / "meds_database")
SRC = ROOT / "data" / "local_rag_chunks.json"
OUT = DB / "derived" / "rag_vektor"
CACHE_IDX = OUT / "vektor_onbellek_bge_m3_test.jsonl"
CACHE_NPY = OUT / "vektor_onbellek_bge_m3_test.npy"
SYNC = OUT / "esitleme_durumu_bge_m3_test.json"
LOG = ROOT.parent / "meds_temp" / "logs" / "rag_bge_m3_backfill.log"
CTRL_RE = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]')
SURR_RE = re.compile(r'[\ud800-\udfff]')


def log(m: str):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [backfill] {m}"
    print(line, flush=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def env() -> dict:
    e = {}
    try:
        for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                e[k.strip()] = v.split(" #")[0].strip().strip('"').strip("'")
    except OSError:
        pass
    e.update({k: v for k, v in os.environ.items() if v})
    return e


def rest(url: str, key: str, method: str, path: str, body=None) -> tuple[int, str]:
    data = json.dumps(body).encode() if body is not None else None
    h = {"apikey": key, "Authorization": f"Bearer {key}", "Content-Type": "application/json",
         "Prefer": "resolution=merge-duplicates,return=minimal"}
    req = urllib.request.Request(url.rstrip("/") + "/rest/v1/" + path, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return r.status, r.read().decode("utf-8", "replace")[:200]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")[:200]


def main() -> int:
    import argparse

    import numpy as np

    ap = argparse.ArgumentParser()
    ap.add_argument("--hedef", default="yerel", choices=["yerel", "bulut"])
    a = ap.parse_args()
    sync_path = OUT / ("esitleme_durumu_bge_m3_cloud.json" if a.hedef == "bulut" else SYNC.name)
    e = env()
    if a.hedef == "bulut":
        url, key = e.get("CLOUD_SUPABASE_URL"), e.get("CLOUD_SUPABASE_SECRET_KEY")
    else:
        url = e.get("LOCAL_SUPABASE_URL") or e.get("SUPABASE_URL") or "http://127.0.0.1:8000"
        key = e.get("LOCAL_SUPABASE_KEY") or e.get("SUPABASE_SECRET_KEY")
    if not url or not key:
        log(f"[{a.hedef}] adres/anahtar yok")
        return 1
    log(f"hedef: {a.hedef}")
    raw = json.loads(SRC.read_text(encoding="utf-8").replace("\\u0000", ""))
    lst = raw if isinstance(raw, list) else raw.get("chunks", [])
    chunks = {c.get("id"): c for c in lst if c.get("id")}
    idx: dict[str, int] = {}
    for line in CACHE_IDX.read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        idx[r["hash"]] = r["row"]
    vecs = np.load(CACHE_NPY)
    log(f"test önbellek: {vecs.shape}, chunk: {len(chunks)}")
    # hash -> chunk id eşleşmesi
    rows = []
    for cid, c in chunks.items():
        h = str(c.get("hash") or "")
        if h in idx:
            txt = SURR_RE.sub('', CTRL_RE.sub('', (c.get("content") or ""))).strip()
            if len(txt) < 20:
                continue
            rows.append({"id": str(cid), "document_id": str(c.get("documentId") or cid),
                         "document_type": c.get("documentType") or "unknown",
                         "committee_id": c.get("committeeId"), "discipline": c.get("discipline"),
                         "title": (c.get("title") or "")[:500],
                         "page_number": c.get("pageNumber") if isinstance(c.get("pageNumber"), int) else None,
                         "content": txt, "metadata": c.get("metadata") or {},
                         "content_hash_bge_m3": h,
                         "embedding_bge_m3": "[" + ",".join(f"{x:.6f}" for x in vecs[idx[h]]) + "]"})
    log(f"yazılacak: {len(rows)} (DELETE YOK)")
    # Artımlı: yalnız hash'i değişenler (cron no-op koşsun)
    synced: dict = {}
    if sync_path.exists():
        try:
            synced = json.loads(sync_path.read_text(encoding="utf-8")).get(a.hedef, {})
        except Exception:
            synced = {}
    rows = [r for r in rows if synced.get(r["id"]) != r["content_hash_bge_m3"]]
    log(f"değişen: {len(rows)} · güncel: {len(synced) - 0}")
    ok = fail = 0
    B = 100
    failed_rows: list = []
    hmap = {r["id"]: r["content_hash_bge_m3"] for r in rows}
    done_ids: set = set()
    for i in range(0, len(rows), B):
        part = rows[i:i + B]
        code, txt = rest(url, key, "POST", "rag_chunks?on_conflict=id", part)
        if code in (200, 201, 204):
            ok += len(part)
            done_ids.update(r["id"] for r in part)
        else:
            # Bulut ücretsiz katman: 57014/500 zaman aşımı → küçük parça + bekleyip yeniden dene
            time.sleep(15)
            recovered = 0
            for j in range(0, len(part), 25):
                sub = part[j:j + 25]
                for _d in range(3):
                    code2, txt2 = rest(url, key, "POST", "rag_chunks?on_conflict=id", sub)
                    if code2 in (200, 201, 204):
                        recovered += len(sub)
                        break
                    time.sleep(10 * (_d + 1))
                else:
                    failed_rows += sub
                    log(f"yazma hatası HTTP {code2}: {txt2} (id={sub[0]['id']}...)")
            ok += recovered
            fail += len(part) - recovered
            done_ids.update(r["id"] for r in part if r["id"] not in {x["id"] for x in failed_rows})
            if code in (401, 403, 404):
                break
        if (i // B) % 20 == 0:
            for rid in done_ids:
                synced[rid] = hmap[rid]
            done_ids.clear()
            sync_path.write_text(json.dumps({a.hedef: synced}), encoding="utf-8")
            log(f"  ilerleme {i + len(part)}/{len(rows)} (ara kayıt)")
    log(f"bitti: yazıldı {ok}, hata {fail}")
    if ok:
        for rid in ({r["id"] for r in rows} - {r["id"] for r in failed_rows}):
            synced[rid] = hmap[rid]
        sync_path.write_text(json.dumps({a.hedef: synced}), encoding="utf-8")
    return 0 if fail == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
