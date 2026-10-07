#!/usr/bin/env python3
"""
RAG vektör yapısı — tüm veritabanı parçalarını (sitenin arama motorunun ürettiği data/local_rag_chunks.json:
çıkmış sorular, ders notları/slaytlar, özetler, Faz 14 önerileri, AI kayıtları…) çok dilli e5-small ile vektörleştirir ve
yerel + bulut Supabase'deki public.rag_chunks tablosuna yazar (embedding_e5 vector(384), match_rag_chunks_e5 ile aranır).

* Ücretsiz ve yerel: intfloat/multilingual-e5-small, CPU (sohbet modeli değil; GPU/Ollama gerekmez).
* Tekrar yok: her parçanın vektörü içerik özetine (hash) göre önbellekte; yalnız yeni/değişen parçalar vektörlenir.
  Her hedef için yazılmış (id → hash) kaydı tutulur; yalnız değişenler yazılır, kaynakta artık olmayanlar silinir.
* Hedefler: yerel (SUPABASE_URL + SUPABASE_SECRET_KEY) ve bulut (CLOUD_SUPABASE_URL + CLOUD_SUPABASE_SECRET_KEY;
  anahtar yoksa atlanır). Bulutta önce supabase/migrations/20261007_rag_e5_384.sql çalıştırılmalıdır.
Kullanım: rag_vector_build.py [--hedef yerel,bulut] [--limit N] [--sadece-vektor]
Çıktı: $MEDS_DATABASE_DIR/derived/rag_vektor/ (vektör önbelleği, eşitleme durumu, rapor)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")            # CPU (GPU yalnız Ollama'ya ayrılmıştı)
ROOT = Path(__file__).resolve().parents[2]
DB = Path(os.environ.get("MEDS_DATABASE_DIR") or ROOT.parent / "meds_database")
SRC = ROOT / "data" / "local_rag_chunks.json"
OUT = DB / "derived" / "rag_vektor"
CACHE_IDX = OUT / "vektor_onbellek.jsonl"                    # {"hash": ..., "row": n}
CACHE_NPY = OUT / "vektor_onbellek.npy"
SYNC = OUT / "esitleme_durumu.json"                          # {hedef: {id: hash}}
REPORT = OUT / "rapor.json"
LOG = ROOT.parent / "meds_temp" / "logs" / "rag_vektor.log"
MODEL = "intfloat/multilingual-e5-small"
DIM = 384


def log(m: str):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [rag_vektor] {m}"
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


def load_chunks() -> list[dict]:
    # Postgres text/jsonb NUL (\u0000) kabul etmez (HTTP 400 22P05) → OCR artığı NUL'lar atılır
    d = json.loads(SRC.read_text(encoding="utf-8").replace("\\u0000", ""))
    rows = d if isinstance(d, list) else d.get("chunks", [])
    out = []
    for c in rows:
        txt = (c.get("content") or "").replace("\x00", "").strip()
        if len(txt) < 20 or not c.get("id"):
            continue
        out.append({"id": str(c["id"]), "hash": str(c.get("hash") or hash(txt)), "content": txt,
                    "document_id": str(c.get("documentId") or c["id"]), "document_type": c.get("documentType") or "unknown",
                    "committee_id": c.get("committeeId"), "discipline": c.get("discipline"), "title": c.get("title"),
                    "page_number": c.get("pageNumber") if isinstance(c.get("pageNumber"), int) else None,
                    "metadata": c.get("metadata") or {}})
    return out


# ---------------------------------------------------------------- vektör önbelleği
def embed_all(chunks: list[dict], limit: int = 0):
    import numpy as np
    OUT.mkdir(parents=True, exist_ok=True)
    idx: dict[str, int] = {}
    vecs = np.zeros((0, DIM), dtype=np.float32)
    if CACHE_IDX.exists() and CACHE_NPY.exists():
        vecs = np.load(CACHE_NPY)
        for line in CACHE_IDX.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            idx[r["hash"]] = r["row"]
    todo = [c for c in chunks if c["hash"] not in idx]
    if limit:
        todo = todo[:limit]
    log(f"parça: {len(chunks)} · önbellekte: {len(chunks) - len([c for c in chunks if c['hash'] not in idx])} · vektörlenecek: {len(todo)}")
    if todo:
        from sentence_transformers import SentenceTransformer
        import torch
        torch.set_num_threads(max(1, (os.cpu_count() or 4) - 2))
        model = SentenceTransformer(MODEL, device="cpu")
        model.max_seq_length = 256           # parça başı ~256 token yeterli; 512’ye göre ~3 kat hızlı
        t0 = time.time()
        B = 2048
        new_rows = []
        for i in range(0, len(todo), B):
            part = todo[i:i + B]
            v = model.encode(["passage: " + c["content"][:1500] for c in part], batch_size=64, normalize_embeddings=True,
                             show_progress_bar=False).astype(np.float32)
            new_rows.append(v)
            done = i + len(part)
            rate = done / max(1e-6, time.time() - t0)
            log(f"  vektörlendi {done}/{len(todo)} · {rate:.0f} parça/sn · kalan ~{(len(todo) - done) / max(rate, 1e-6) / 60:.1f} dk")
            # ara kayıt (kesilirse kaldığı yerden)
            base = len(vecs)
            vecs = np.vstack([vecs, v])
            with open(CACHE_IDX, "a", encoding="utf-8") as f:
                for j, c in enumerate(part):
                    idx[c["hash"]] = base + j
                    f.write(json.dumps({"hash": c["hash"], "row": base + j}) + "\n")
            np.save(CACHE_NPY, vecs)
    return idx, vecs


# ---------------------------------------------------------------- Supabase
def rest(url: str, key: str, method: str, path: str, body=None, prefer: str = "") -> tuple[int, str]:
    data = json.dumps(body).encode() if body is not None else None
    h = {"apikey": key, "Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    if prefer:
        h["Prefer"] = prefer
    req = urllib.request.Request(url.rstrip("/") + "/rest/v1/" + path, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, r.read().decode("utf-8", "replace")[:300]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")[:300]


def sync_target(name: str, url: str, key: str, chunks: list[dict], idx: dict, vecs) -> dict:
    st_all = json.loads(SYNC.read_text(encoding="utf-8")) if SYNC.exists() else {}
    synced: dict = st_all.get(name, {})
    want = {c["id"]: c for c in chunks if c["hash"] in idx}
    changed = [c for c in want.values() if synced.get(c["id"]) != c["hash"]]
    removed = [i for i in synced if i not in want]
    log(f"[{name}] yazılacak: {len(changed)} · silinecek: {len(removed)} · güncel: {len(want) - len(changed)}")
    ok = fail = 0
    B = 100 if name == "bulut" else 300                         # bulut (ücretsiz katman): HNSW yazımı yavaş, küçük paket
    for i in range(0, len(changed), B):
        part = changed[i:i + B]
        rows = [{"id": c["id"], "document_id": c["document_id"], "document_type": c["document_type"],
                 "committee_id": c["committee_id"], "discipline": c["discipline"], "title": (c["title"] or "")[:500],
                 "page_number": c["page_number"], "content": c["content"], "metadata": c["metadata"],
                 "content_hash": c["hash"], "embedding_e5": "[" + ",".join(f"{x:.6f}" for x in vecs[idx[c["hash"]]]) + "]"}
                for c in part]
        for _d in range(3):                                         # zaman aşımı (57014/500) → bekleyip yeniden dene
            code, txt = rest(url, key, "POST", "rag_chunks?on_conflict=id", rows, "resolution=merge-duplicates,return=minimal")
            if code not in (500, 502, 503, 504):
                break
            time.sleep(10 * (_d + 1))
        if code in (200, 201, 204):
            ok += len(part)
            for c in part:
                synced[c["id"]] = c["hash"]
        else:
            fail += len(part)
            log(f"[{name}] yazma hatası HTTP {code}: {txt}")
            if code in (401, 403, 404):
                break
        if (i // B) % 20 == 0:
            st_all[name] = synced
            SYNC.write_text(json.dumps(st_all), encoding="utf-8")
    for i in range(0, len(removed), 200):
        part = removed[i:i + 200]
        ids = ",".join('"' + x.replace('"', '') + '"' for x in part)
        code, txt = rest(url, key, "DELETE", f"rag_chunks?id=in.({urllib.request.quote(ids, safe=',()')})", prefer="return=minimal")
        if code in (200, 204):
            for x in part:
                synced.pop(x, None)
    st_all[name] = synced
    SYNC.write_text(json.dumps(st_all), encoding="utf-8")
    log(f"[{name}] yazıldı {ok}, hata {fail}, silindi {len(removed)}")
    return {"yazilan": ok, "hata": fail, "silinen": len(removed), "toplam_esit": len(synced)}


def main() -> int:
    ap = argparse.ArgumentParser()
    # Bulut Supabase ücretsiz katmanı doldu (2026-10-07) → varsayılan yalnız yerel. Bulut için: --hedef yerel,bulut
    # ya da .env'de MEDS_RAG_TARGETS=yerel,bulut
    ap.add_argument("--hedef", default=env().get("MEDS_RAG_TARGETS") or "yerel")
    ap.add_argument("--limit", type=int, default=0, help="test: en fazla N yeni parça vektörle")
    ap.add_argument("--sadece-vektor", action="store_true")
    a = ap.parse_args()
    if not SRC.exists():
        log(f"kaynak yok: {SRC} (site sunucusu açılışta üretir)")
        return 1
    t0 = time.time()
    chunks = load_chunks()
    idx, vecs = embed_all(chunks, a.limit)
    rep = {"zaman": time.strftime("%Y-%m-%dT%H:%M:%S"), "parca": len(chunks), "vektorlu": sum(1 for c in chunks if c["hash"] in idx),
           "model": MODEL, "boyut": DIM, "hedefler": {}}
    if not a.sadece_vektor:
        e = env()
        targets = {"yerel": (e.get("LOCAL_SUPABASE_URL") or e.get("SUPABASE_URL") or "http://127.0.0.1:8000", e.get("LOCAL_SUPABASE_KEY") or e.get("SUPABASE_SECRET_KEY")),
                   "bulut": (e.get("CLOUD_SUPABASE_URL"), e.get("CLOUD_SUPABASE_SECRET_KEY"))}
        for name in [x.strip() for x in a.hedef.split(",") if x.strip()]:
            url, key = targets.get(name, (None, None))
            if not url or not key:
                log(f"[{name}] atlandı: adres/gizli anahtar yok ({'CLOUD_SUPABASE_SECRET_KEY' if name == 'bulut' else 'SUPABASE_SECRET_KEY'})")
                rep["hedefler"][name] = "anahtar yok"
                continue
            rep["hedefler"][name] = sync_target(name, url, key, chunks, idx, vecs)
    rep["sure_sn"] = round(time.time() - t0)
    REPORT.write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    log(f"bitti: {json.dumps(rep, ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
