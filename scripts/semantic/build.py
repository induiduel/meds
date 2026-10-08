"""Derleme (build): bilgi tabanını üretir.

Adımlar:
  1. Hiyerarşik taksonomi (Ders→Kurul→Konu→Kazanım) — `taxonomy.build()`
  2. Tıbbi sözlük/ICD — `medical.build_lexicon()`
  3. CORE parçalarını yükle ve zenginleştir (ders + konu/kazanım)
  4. FAISS vektör indeksi (mevcut e5 vektörleriyle; yoksa üretir)
Tümü CPU/ücretsiz; eski veriye dokunmaz.
"""
from __future__ import annotations

import json

from . import config, medical, taxonomy


def _read_jsonl(path):
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue


def _load_sources() -> dict[str, dict]:
    out = {}
    if config.CORE_SOURCES.exists():
        for p in config.CORE_SOURCES.glob("*.json"):
            try:
                s = json.loads(p.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001
                continue
            if s.get("source_id"):
                out[s["source_id"]] = {"ders": s.get("ders"), "kurul": s.get("kurul")}
    return out


def _load_chunk_map() -> dict[str, dict]:
    out = {}
    if config.CORE_CHUNKS.exists():
        for p in config.CORE_CHUNKS.glob("*.jsonl"):
            for c in _read_jsonl(p):
                if c.get("chunk_id"):
                    out[c["chunk_id"]] = c
    return out


def source_groups(metas: list[dict], vecs, threshold: float = 0.90) -> dict[str, str]:
    """Aynı dersin tekrar yüklenmiş (kopya) kaynaklarını gruplar. source_id → grup_id."""
    import numpy as np

    src_rows: dict[str, list[int]] = {}
    for i, m in enumerate(metas):
        sid = m.get("source_id")
        if sid:
            src_rows.setdefault(sid, []).append(i)
    sids = list(src_rows)
    cents = {}
    for sid in sids:
        v = vecs[src_rows[sid]]
        c = v.mean(axis=0)
        n = np.linalg.norm(c) or 1.0
        cents[sid] = c / n
    parent = {s: s for s in sids}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a in range(len(sids)):
        for b in range(a + 1, len(sids)):
            if float(cents[sids[a]] @ cents[sids[b]]) >= threshold:
                ra, rb = find(sids[a]), find(sids[b])
                if ra != rb:
                    parent[rb] = ra
    return {s: find(s) for s in sids}


def main() -> int:
    print("[1/4] taksonomi...")
    tax_data = taxonomy.build()
    tax = taxonomy.Taxonomy(tax_data)
    print(f"      konu={len(tax.konular)} kurul={len(tax.kurul_ad)}")

    print("[2/4] tıbbi sözlük/ICD...")
    lex = medical.build_lexicon()
    config.LEXICON_PATH.write_text(json.dumps(lex, ensure_ascii=False), encoding="utf-8")
    print(f"      terim={len(lex)}")

    print("[3/4] CORE parçaları...")
    sources = _load_sources()
    chunk_map = _load_chunk_map()
    ids = list(_read_jsonl(config.CORE_VECTOR_IDS))
    if not ids:
        print("HATA: CORE vektör kimlikleri yok:", config.CORE_VECTOR_IDS)
        return 1

    import numpy as np
    vecs = np.load(config.CORE_VECTORS).astype("float32") if config.CORE_VECTORS.exists() else None

    texts, metas = [], []
    for row in ids:
        cid = row.get("chunk_id")
        ch = chunk_map.get(cid) or {}
        text = ch.get("text") or ""
        sid = row.get("source_id") or ch.get("source_id")
        src = sources.get(sid, {})
        texts.append(text)
        metas.append({"chunk_id": cid, "source_id": sid, "page": row.get("page") or ch.get("page"),
                      "ders": src.get("ders"), "kurul": src.get("kurul"),
                      "text": (text or "")[:1200]})

    print("      konu/kazanım eşleme (toplu)...")
    matches = tax.match_many(texts, min_score=0.15)
    for meta, m in zip(metas, matches):
        for key in ("konu", "kazanim", "konu_skor", "kazanim_skor"):
            if m.get(key) is not None:
                meta[key] = m[key]

    with open(config.META_PATH, "w", encoding="utf-8") as fh:
        for meta in metas:
            fh.write(json.dumps(meta, ensure_ascii=False) + "\n")

    print("[4/4] FAISS indeksi...")
    if vecs is None or vecs.shape[0] != len(ids):
        print("      e5 vektörleri yok/uyumsuz → yeniden üretiliyor (yavaş, CPU)")
        from . import embeddings
        vecs = embeddings.embed_passages(texts)
    import faiss
    index = faiss.IndexFlatIP(vecs.shape[1])
    index.add(vecs)
    faiss.write_index(index, str(config.INDEX_PATH))

    print("      sözlüksel indeks (TF-IDF)...")
    from . import lexindex
    lexindex.build(texts)

    print("      kopya kaynak gruplama...")
    groups = source_groups(metas, vecs)
    (config.OUT / "source_groups.json").write_text(json.dumps(groups, ensure_ascii=False), encoding="utf-8")
    print(f"      kaynak kümesi: {len(set(groups.values()))} (kaynak {len(groups)})")

    print(json.dumps({"parca": len(ids), "boyut": int(vecs.shape[1]), "terim": len(lex),
                      "konu": len(tax.konular)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
