#!/usr/bin/env python3
"""
RAG vektör hattı (tek, artımlı) — data/local_rag_chunks.json → e5 + bge-m3 vektörleri → meds-pg → (isteğe bağlı) Oracle.

Eski iki hattın (rag_vector_build.py: e5, rag_vector_build_bge_m3_test.py + rag_bge_m3_test_backfill.py: bge-m3) yerini alır:
* Donanım dostu: model süreç içine yüklenmez; zaten açık olan CPU servisleri kullanılır (meds-embed :8091 e5,
  meds-embed-bge :8094 bge-m3; scripts/agents/lib.py::embed). Servis kapalıysa o model atlanır, hat durmaz.
  Aynı anda tek kopya çalışır (kilit dosyası), süreç düşük önceliklidir (nice).
* Tekrar yok: vektörler içerik özetine (hash) göre önbellekte (derived/rag_vektor/); önbellek yetim satırlardan
  kendiliğinden arındırılır. Yalnız yeni/değişen parçalar vektörlenir.
* Veritabanı: PostgREST yerine doğrudan Postgres (psycopg COPY + tek INSERT … ON CONFLICT). Kaynakta artık olmayan
  satırlar silinir (dosya kesik/eksikse güvenlik eşiği silmeyi durdurur). İçerik değişip yeni vektör henüz yoksa eski
  vektör korunur, özet eşleşmediği için bir sonraki turda yenilenir.
* İnternet dostu Oracle eşitlemesi (--oracle): tam döküm yerine iki tarafın (id, özet) listesi karşılaştırılır; yalnız
  değişen satırlar gzip'li COPY akışıyla ssh üzerinden gönderilir, silinenler silinir. Tipik tur birkaç yüz KB.

Kullanım:
  rag_vektor_hatti.py                    # vektörle + yerel meds-pg
  rag_vektor_hatti.py --oracle           # + Oracle'a fark eşitlemesi
  rag_vektor_hatti.py --sadece-oracle    # yalnız yerel → Oracle farkı
  rag_vektor_hatti.py --kuru --oracle    # ne yapılacağını yaz, dokunma
  rag_vektor_hatti.py --model bge_m3 --limit 500
  rag_vektor_hatti.py --denetle --oracle # bozuk (yanlış parçaya ait) vektörleri bul, onar, canlıya taşı
Çıktı/günlük: $MEDS_DATABASE_DIR/derived/rag_vektor/hat_rapor.json, meds_temp/logs/rag_vektor_hatti.log
"""
from __future__ import annotations

import argparse
import fcntl
import gzip
import io
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")  # yerel GPU yasak (AGENTS.md kural 10)
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "agents"))
DB = Path(os.environ.get("MEDS_DATABASE_DIR") or ROOT.parent / "meds_database")
SRC = ROOT / "data" / "local_rag_chunks.json"
OUT = DB / "derived" / "rag_vektor"
REPORT = OUT / "hat_rapor.json"
LOCK = OUT / ".hat.lock"
LOG = ROOT.parent / "meds_temp" / "logs" / "rag_vektor_hatti.log"
CTRL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
SURR_RE = re.compile(r"[\ud800-\udfff]")

# Önbellek dosya adları eski hatlarla aynı: geçişte hiçbir vektör yeniden hesaplanmaz.
MODELS = {
    "e5": {"service_model": "e5", "dim": 384, "col": "embedding_e5", "hash_col": "content_hash",
           "idx": OUT / "vektor_onbellek.jsonl", "npy": OUT / "vektor_onbellek.npy"},
    "bge_m3": {"service_model": "bge-m3", "dim": 1024, "col": "embedding_bge_m3", "hash_col": "content_hash_bge_m3",
               "idx": OUT / "vektor_onbellek_bge_m3_test.jsonl", "npy": OUT / "vektor_onbellek_bge_m3_test.npy"},
}
COLS = ["id", "document_id", "document_type", "committee_id", "discipline", "title", "page_number", "content",
        "metadata", "embedding_e5", "content_hash", "embedding_bge_m3", "content_hash_bge_m3", "updated_at"]
ORACLE_SSH = os.environ.get("MEDS_ORACLE_SSH", "medsor-oracle")
# Vektör parmak izi: özet aynı kalıp vektör düzeltildiğinde (--denetle) de fark yakalansın (iki makinede aynı float4 → aynı metin)
VEC_FP = ("coalesce(round(((embedding_bge_m3::real[])[1] + 3 * (embedding_bge_m3::real[])[7] "
          "+ 7 * (embedding_e5::real[])[1])::numeric, 6)::text, '')")
REMOTE_PSQL = "docker exec -i meds-pg psql -U meds -d meds -v ON_ERROR_STOP=1 -q"


def log(m: str):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [rag_hat] {m}"
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
    # Postgres text/jsonb NUL (\u0000) kabul etmez → OCR artığı NUL'lar atılır
    d = json.loads(SRC.read_text(encoding="utf-8").replace("\\u0000", ""))
    rows = d if isinstance(d, list) else d.get("chunks", [])
    out = []
    for c in rows:
        txt = SURR_RE.sub("", CTRL_RE.sub("", (c.get("content") or ""))).strip()
        if len(txt) < 20 or not c.get("id"):
            continue
        meta = json.loads(SURR_RE.sub("", json.dumps(c.get("metadata") or {}, ensure_ascii=False)).replace("\\u0000", ""))
        out.append({"id": str(c["id"]), "hash": str(c.get("hash") or hash(txt)), "content": txt,
                    "document_id": str(c.get("documentId") or c["id"]), "document_type": c.get("documentType") or "unknown",
                    "committee_id": c.get("committeeId"), "discipline": c.get("discipline"),
                    "title": SURR_RE.sub("", c.get("title") or "")[:500],
                    "page_number": c.get("pageNumber") if isinstance(c.get("pageNumber"), int) else None,
                    "metadata": meta})
    return out


# ---------------------------------------------------------------- vektör önbelleği
class VectorCache:
    """Özet → satır dizini (.jsonl) + vektörler (.npy). Yeni satırlar bellekte birikir; save() önce .npy'yi atomik
    yazar, sonra dizin satırlarını ekler — kesinti dizini hiçbir zaman yazılmamış satıra işaret ettirmez."""

    def __init__(self, name: str, spec: dict):
        import numpy as np
        self.np = np
        self.name, self.spec = name, spec
        self.idx: dict[str, int] = {}
        self.vecs = np.zeros((0, spec["dim"]), dtype=np.float32)
        if spec["idx"].exists() and spec["npy"].exists():
            self.vecs = np.load(spec["npy"], mmap_mode="r")
            for line in spec["idx"].read_text(encoding="utf-8").splitlines():
                r = json.loads(line)
                if r["row"] < len(self.vecs):
                    self.idx[r["hash"]] = r["row"]
        self.new_hashes: list[str] = []
        self.new_vecs: list = []

    def has(self, h: str) -> bool:
        return h in self.idx

    def get(self, h: str):
        r = self.idx[h]
        n = len(self.vecs)
        return self.vecs[r] if r < n else self.new_vecs[r - n]

    def add(self, hashes: list[str], v):
        base = len(self.vecs) + len(self.new_vecs)
        for j, h in enumerate(hashes):
            self.idx[h] = base + j
            self.new_hashes.append(h)
            self.new_vecs.append(v[j])

    def save(self):
        if not self.new_vecs:
            return
        base = len(self.vecs)
        arr = self.np.concatenate([self.np.asarray(self.vecs), self.np.stack(self.new_vecs)]) if base else self.np.stack(self.new_vecs)
        self._atomic_save(arr)
        with open(self.spec["idx"], "a", encoding="utf-8") as f:
            for j, h in enumerate(self.new_hashes):
                f.write(json.dumps({"hash": h, "row": base + j}) + "\n")
        self.new_hashes, self.new_vecs = [], []

    def _atomic_save(self, arr):
        tmp = self.spec["npy"].with_suffix(".tmp.npy")
        self.np.save(tmp, self.np.ascontiguousarray(arr, dtype=self.np.float32))
        os.replace(tmp, self.spec["npy"])
        self.vecs = self.np.load(self.spec["npy"], mmap_mode="r")

    def compact(self, live: set[str]) -> int:
        """Kaynakta artık olmayan özetlerin satırlarını atar (önbellek yarıdan fazlası yetim olabiliyordu)."""
        self.save()
        keep = [(h, r) for h, r in self.idx.items() if h in live]
        dropped = len(self.vecs) - len(keep)
        if dropped < max(1000, len(self.vecs) // 5):
            return 0
        keep.sort(key=lambda x: x[1])
        rows = self.np.array([r for _, r in keep], dtype=self.np.int64)
        arr = self.np.asarray(self.vecs)[rows] if len(rows) else self.np.zeros((0, self.spec["dim"]), self.np.float32)
        self._atomic_save(arr)
        self.idx = {h: i for i, (h, _) in enumerate(keep)}
        tmp = self.spec["idx"].with_suffix(".tmp")
        tmp.write_text("".join(json.dumps({"hash": h, "row": i}) + "\n" for i, (h, _) in enumerate(keep)), encoding="utf-8")
        os.replace(tmp, self.spec["idx"])
        return dropped


def embed_missing(cache: VectorCache, chunks: list[dict], limit: int) -> dict:
    import lib  # scripts/agents/lib.py
    todo, seen = [], set()
    for c in chunks:
        if not cache.has(c["hash"]) and c["hash"] not in seen:
            seen.add(c["hash"])
            todo.append(c)
    if limit:
        todo = todo[:limit]
    log(f"[{cache.name}] parça {len(chunks)} · önbellekte {len(chunks) - len(seen)} · vektörlenecek {len(todo)}")
    if not todo:
        return {"vektorlenen": 0}
    t0, done, B = time.time(), 0, 256
    try:
        for i in range(0, len(todo), B):
            part = todo[i:i + B]
            v = lib.embed(["passage: " + c["content"][:1500] for c in part], model=cache.spec["service_model"])
            if v.shape[1] != cache.spec["dim"]:
                raise RuntimeError(f"boyut {v.shape[1]} ≠ {cache.spec['dim']} (servis yanlış model?)")
            cache.add([c["hash"] for c in part], v.astype("float32"))
            done += len(part)
            if (i // B) % 8 == 7 or done == len(todo):
                cache.save()  # ara kayıt: kesilirse kaldığı yerden
                rate = done / max(1e-6, time.time() - t0)
                log(f"[{cache.name}]   {done}/{len(todo)} · {rate:.1f} parça/sn · kalan ~{(len(todo) - done) / max(rate, 1e-6) / 60:.1f} dk")
    except Exception as err:  # servis kapalı/yanıtsız: bu model atlanır, eldeki vektörler yazılır
        if done:
            cache.save()
        log(f"[{cache.name}] vektörleme durdu ({type(err).__name__}: {str(err)[:160]}) — {done} parça kaydedildi")
        return {"vektorlenen": done, "hata": str(err)[:200]}
    return {"vektorlenen": done}


# ---------------------------------------------------------------- vektör denetimi
def audit_vectors(chunks: list[dict], caches: dict[str, VectorCache], dry: bool) -> tuple[set[str], dict]:
    """Önbellekte yanlış parçaya ait vektör (eski bge test betiğinin kesinti hatası) arar ve onarır.
    Ölçüt: bge-m3'te en yakın komşusuyla "neredeyse aynı" (> 0.96) görünüp e5'te açıkça farklı (< 0.93) olan parçalar
    şüphelidir; servisle taze vektörlenir, saklananla benzerliği < 0.98 ise değiştirilir. e5 doğruluğu ayrıca örneklenir."""
    import numpy as np
    import lib
    B, E = caches.get("bge_m3"), caches.get("e5")
    if not B or not E:
        return set(), {"atlandi": "iki model de gerekli"}
    by_hash = {}
    for c in chunks:
        if B.has(c["hash"]) and E.has(c["hash"]):
            by_hash.setdefault(c["hash"], c)
    hs = list(by_hash)
    Bv = np.stack([np.asarray(B.get(h)) for h in hs]).astype(np.float32)
    Ev = np.stack([np.asarray(E.get(h)) for h in hs]).astype(np.float32)
    nn = np.zeros(len(hs), dtype=np.int64)
    nns = np.zeros(len(hs), dtype=np.float32)
    for i in range(0, len(hs), 1024):
        sims = Bv[i:i + 1024] @ Bv.T
        sims[np.arange(sims.shape[0]), np.arange(i, i + sims.shape[0])] = -1
        nn[i:i + 1024] = sims.argmax(1)
        nns[i:i + 1024] = sims.max(1)
    e = np.einsum("ij,ij->i", Ev, Ev[nn])
    suspects = [hs[i] for i in np.where((nns > 0.96) & (e < 0.93))[0]]
    log(f"[denetim] {len(hs)} özet tarandı · şüpheli {len(suspects)}")
    del Bv, Ev
    if dry or not suspects:
        return set(), {"supheli": len(suspects)}
    fixed: set[str] = set()
    for i in range(0, len(suspects), 128):
        part = suspects[i:i + 128]
        fresh = lib.embed(["passage: " + by_hash[h]["content"][:1500] for h in part], model="bge-m3").astype("float32")
        bad = [(h, fresh[k]) for k, h in enumerate(part) if float(fresh[k] @ np.asarray(B.get(h))) < 0.98]
        if bad:
            B.add([h for h, _ in bad], np.stack([v for _, v in bad]))
            fixed.update(h for h, _ in bad)
        log(f"[denetim]   {min(i + 128, len(suspects))}/{len(suspects)} · bozuk bulunan {len(fixed)}")
    B.save()
    return fixed, {"supheli": len(suspects), "onarilan": len(fixed)}


# ---------------------------------------------------------------- yerel meds-pg
def vec_text(v) -> str:
    return "[" + ",".join(f"{x:.6f}" for x in v) + "]"


def copy_escape(s) -> str:
    if s is None:
        return "\\N"
    return str(s).replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n").replace("\r", "\\r")


def sync_local(conn, chunks: list[dict], caches: dict[str, VectorCache], dry: bool, force: set[str] | None = None) -> dict:
    cur = conn.cursor()
    cur.execute("SELECT id, content_hash, content_hash_bge_m3, embedding_e5 IS NOT NULL, embedding_bge_m3 IS NOT NULL FROM rag_chunks")
    have = {r[0]: r[1:] for r in cur.fetchall()}
    want = {c["id"]: c for c in chunks}
    e5, bge = caches.get("e5"), caches.get("bge_m3")
    changed = []
    for c in want.values():
        h = have.get(c["id"])
        if h is None or h[0] != c["hash"] or (force and c["hash"] in force):
            changed.append(c)
            continue
        if (e5 and e5.has(c["hash"]) and not h[2]) or (bge and bge.has(c["hash"]) and (h[1] != c["hash"] or not h[3])):
            changed.append(c)
    removed = [i for i in have if i not in want]
    log(f"[yerel] satır {len(have)} · yazılacak {len(changed)} · silinecek {len(removed)}")
    if len(removed) > max(5000, len(have) // 2) and len(want) < len(have) // 2:
        log("[yerel] GÜVENLİK: kaynak parça sayısı tablonun yarısından az — silme atlandı (dosya kesik olabilir)")
        removed = []
    if dry:
        return {"yazilacak": len(changed), "silinecek": len(removed)}
    B = 2000
    for i in range(0, len(changed), B):
        part = changed[i:i + B]
        buf = io.StringIO()
        for c in part:
            ve5 = vec_text(e5.get(c["hash"])) if e5 and e5.has(c["hash"]) else None
            vbg = vec_text(bge.get(c["hash"])) if bge and bge.has(c["hash"]) else None
            buf.write("\t".join(copy_escape(x) for x in [
                c["id"], c["document_id"], c["document_type"], c["committee_id"], c["discipline"], c["title"],
                c["page_number"], c["content"], json.dumps(c["metadata"], ensure_ascii=False), ve5, c["hash"],
                vbg, c["hash"] if vbg else None]) + "\n")
        cur.execute("CREATE TEMP TABLE IF NOT EXISTS _rag_in (LIKE rag_chunks INCLUDING DEFAULTS) ON COMMIT DELETE ROWS")
        cols = COLS[:-1]
        with cur.copy(f"COPY _rag_in ({','.join(cols)}) FROM STDIN") as cp:
            cp.write(buf.getvalue())
        # Yeni vektör yoksa eskisi korunur; özeti eski kalır → sonraki tur yeniler
        cur.execute(f"""
            INSERT INTO rag_chunks ({','.join(cols)}, updated_at)
            SELECT {','.join(cols)}, now() FROM _rag_in
            ON CONFLICT (id) DO UPDATE SET
              document_id = EXCLUDED.document_id, document_type = EXCLUDED.document_type,
              committee_id = EXCLUDED.committee_id, discipline = EXCLUDED.discipline, title = EXCLUDED.title,
              page_number = EXCLUDED.page_number, content = EXCLUDED.content, metadata = EXCLUDED.metadata,
              content_hash = EXCLUDED.content_hash,
              embedding_e5 = COALESCE(EXCLUDED.embedding_e5, rag_chunks.embedding_e5),
              embedding_bge_m3 = COALESCE(EXCLUDED.embedding_bge_m3, rag_chunks.embedding_bge_m3),
              content_hash_bge_m3 = COALESCE(EXCLUDED.content_hash_bge_m3, rag_chunks.content_hash_bge_m3),
              updated_at = now()""")
        conn.commit()
    for i in range(0, len(removed), 5000):
        cur.execute("DELETE FROM rag_chunks WHERE id = ANY(%s)", (removed[i:i + 5000],))
        conn.commit()
    log(f"[yerel] yazıldı {len(changed)} · silindi {len(removed)}")
    return {"yazilan": len(changed), "silinen": len(removed)}


# ---------------------------------------------------------------- Oracle fark eşitlemesi
def remote_state() -> dict[str, tuple]:
    q = ("COPY (SELECT id, coalesce(content_hash,''), coalesce(content_hash_bge_m3,''), "
         f"(embedding_e5 IS NOT NULL)::int, (embedding_bge_m3 IS NOT NULL)::int, {VEC_FP} FROM rag_chunks) TO STDOUT")
    p = subprocess.run(["ssh", "-o", "ConnectTimeout=15", ORACLE_SSH,
                        f"docker exec meds-pg psql -U meds -d meds -c \"{q}\" | gzip -6"],
                       capture_output=True, timeout=300)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.decode("utf-8", "replace")[-300:])
    st = {}
    for line in gzip.decompress(p.stdout).decode("utf-8").splitlines():
        a = line.split("\t")
        st[a[0]] = (a[1], a[2], a[3] == "1", a[4] == "1", a[5])
    log(f"[oracle] durum alındı: {len(st)} satır ({len(p.stdout) / 1024:.0f} KB sıkıştırılmış)")
    return st


def sync_oracle(conn, dry: bool) -> dict:
    cur = conn.cursor()
    cur.execute("SELECT id, coalesce(content_hash,''), coalesce(content_hash_bge_m3,''), embedding_e5 IS NOT NULL, "
                f"embedding_bge_m3 IS NOT NULL, {VEC_FP} FROM rag_chunks")
    local = {r[0]: r[1:] for r in cur.fetchall()}
    remote = remote_state()
    changed = [i for i, s in local.items() if remote.get(i) != tuple(s)]
    removed = [i for i in remote if i not in local]
    log(f"[oracle] gönderilecek {len(changed)} · silinecek {len(removed)} · aynı {len(local) - len(changed)}")
    if dry or (not changed and not removed):
        return {"gonderilecek": len(changed), "silinecek": len(removed), "bayt": 0}
    sent = 0
    B = 3000
    batches = [changed[i:i + B] for i in range(0, len(changed), B)] or [[]]
    for bi, part in enumerate(batches):
        raw = io.BytesIO()
        with gzip.GzipFile(fileobj=raw, mode="wb", compresslevel=6) as gz:
            w = lambda s: gz.write(s.encode("utf-8"))
            w("BEGIN;\nCREATE TEMP TABLE _rag_in (LIKE rag_chunks INCLUDING DEFAULTS);\n")
            if part:
                w(f"COPY _rag_in ({','.join(COLS)}) FROM STDIN;\n")
                with cur.copy(f"COPY (SELECT {','.join(COLS)} FROM rag_chunks WHERE id = ANY(%s)) TO STDOUT", (part,)) as cp:
                    for block in cp:
                        gz.write(bytes(block))
                w("\\.\n")
                upd = ",".join(f"{c} = EXCLUDED.{c}" for c in COLS[1:])
                w(f"INSERT INTO rag_chunks ({','.join(COLS)}) SELECT {','.join(COLS)} FROM _rag_in ON CONFLICT (id) DO UPDATE SET {upd};\n")
            if bi == len(batches) - 1 and removed:
                for i in range(0, len(removed), 5000):
                    arr = ",".join("'" + x.replace("'", "''") + "'" for x in removed[i:i + 5000])
                    w(f"DELETE FROM rag_chunks WHERE id IN ({arr});\n")
            w("COMMIT;\n")
        payload = raw.getvalue()
        p = subprocess.run(["ssh", "-o", "ConnectTimeout=15", ORACLE_SSH, f"gunzip | {REMOTE_PSQL}"],
                           input=payload, capture_output=True, timeout=1800)
        if p.returncode != 0:
            raise RuntimeError(f"Oracle yazımı başarısız (parti {bi + 1}): {p.stderr.decode('utf-8', 'replace')[-400:]}")
        sent += len(payload)
        log(f"[oracle]   parti {bi + 1}/{len(batches)}: {len(part)} satır · {len(payload) / 1048576:.2f} MB")
    log(f"[oracle] bitti: {len(changed)} yazıldı, {len(removed)} silindi, {sent / 1048576:.2f} MB gönderildi")
    return {"gonderilen": len(changed), "silinen": len(removed), "bayt": sent}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="e5,bge_m3", help="e5,bge_m3 (virgüllü)")
    ap.add_argument("--limit", type=int, default=0, help="model başına en fazla N yeni parça vektörle")
    ap.add_argument("--oracle", action="store_true", help="yerel meds-pg → Oracle fark eşitlemesi")
    ap.add_argument("--sadece-oracle", action="store_true", help="vektörleme/yerel yazım yok, yalnız Oracle farkı")
    ap.add_argument("--kuru", action="store_true", help="yazmadan say")
    ap.add_argument("--denetle", action="store_true", help="yanlış parçaya ait bge-m3 vektörlerini bul ve onar")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    lock = open(LOCK, "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        log("başka bir hat turu sürüyor — çıkılıyor")
        return 0
    try:
        os.nice(10)
    except OSError:
        pass
    import psycopg
    t0 = time.time()
    rep: dict = {"zaman": time.strftime("%Y-%m-%dT%H:%M:%S")}
    conn = psycopg.connect(env().get("DATABASE_URL") or "postgres://meds@127.0.0.1:54330/meds")
    if not a.sadece_oracle:
        if not SRC.exists():
            log(f"kaynak yok: {SRC} (site sunucusu açılışta üretir)")
            return 1
        chunks = load_chunks()
        live = {c["hash"] for c in chunks}
        rep["parca"] = len(chunks)
        caches: dict[str, VectorCache] = {}
        for name in [m.strip() for m in a.model.split(",") if m.strip() in MODELS]:
            cache = VectorCache(name, MODELS[name])
            if not a.kuru:
                rep[name] = embed_missing(cache, chunks, a.limit)
                dropped = cache.compact(live)
                if dropped:
                    log(f"[{name}] önbellekten {dropped} yetim satır atıldı")
                    rep[name]["onbellek_atilan"] = dropped
            rep.setdefault(name, {})["vektorlu"] = sum(1 for c in chunks if cache.has(c["hash"]))
            caches[name] = cache
        force: set[str] = set()
        if a.denetle:
            force, rep["denetim"] = audit_vectors(chunks, caches, a.kuru)
        rep["yerel"] = sync_local(conn, chunks, caches, a.kuru, force)
    if a.oracle or a.sadece_oracle:
        try:
            rep["oracle"] = sync_oracle(conn, a.kuru)
        except Exception as err:
            log(f"[oracle] HATA: {err}")
            rep["oracle"] = {"hata": str(err)[:300]}
    rep["sure_sn"] = round(time.time() - t0)
    REPORT.write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    log(f"bitti: {json.dumps(rep, ensure_ascii=False)}")
    return 0 if "hata" not in json.dumps(rep.get("oracle", {})) else 2


if __name__ == "__main__":
    sys.exit(main())
