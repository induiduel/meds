#!/usr/bin/env python3
"""
Faz 11 — Soru ↔ ders slaytı (kaynak + sayfa) eşleştirmesi ve metadatası

Tüm güvenilir verileri birleştirir; hedef: elle denetimde ilk slayt ≥ %60–70 doğru.

Adaylar (sınav/soru dökümleri hiçbir aşamada kanıt sayılmaz):
  a) BM25 — Türkçe katlama + 5 harf kök + kavram belirteçleri (Faz 10 Wikidata/UMLS kavramları, kanıtlı sözlük,
     eski sözlüğün doğrulanmış kısmı): "glikojenoliz" sorusu "glycogenolysis" yazan slaytı bulur.
  b) Vektör — intfloat/multilingual-e5-small (CPU, çok dilli; all-MiniLM-L6-v2 yalnız İngilizce olduğu için seçilmedi).
  c) Güvenilir önceki eşleşmeler — Faz 5 ders slaytı eşleşmeleri, Faz 8/10 kazanım kanıtı, Faz 6.5 çapası.
  → Reciprocal Rank Fusion ile birleştirilir, ilk 30 aday yeniden sıralanır.
Yeniden sıralama: cross-encoder/mmarco-mMiniLMv2-L12-H384-v1 (çok dilli cross-encoder, CPU) — sorgu = soru kökü +
  doğru cevap metni (cevabı bilinen sorularda).
Son puan = cross-encoder + konu önseli (güvenilir müfredat konusunun kaynağı) + slayt doğru cevabı içeriyor +
  Faz 5 ile örtüşme.
Güven: yuksek (net fark + cevap/konu kanıtı) | orta | dusuk → düşük olanlar hakem kuyruğuna.

Çıktı (ana veritabanına yazmaz): meds_temp/phase11/
  soru_slayt.jsonl  — soru başına en iyi 3 slayt (kaynak, sayfa, chunk, puanlar, alıntı, gerekçe), güven, konu
  hakem_kuyrugu.jsonl, rapor.json, elle_kontrol_ornegi.json
  emb_*.npy         — vektör önbelleği (chunk sayısı değişince yenilenir)
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import random
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phase8_curriculum_graph as P8  # noqa: E402
import phase9_thesaurus_graph as P9  # noqa: E402

PROJECT = P8.PROJECT
V2 = PROJECT / "meds_database_v2"
TEMP = Path(os.environ.get("MEDS_TEMP_DIR") or PROJECT / "meds_temp")
OUT = TEMP / "phase11"
TREE = [TEMP / "phase10" / "soru_kazanim.jsonl", TEMP / "phase9" / "soru_kazanim.jsonl", TEMP / "phase8" / "soru_kazanim.jsonl"]
KONULAR = TEMP / "phase8" / "konular.jsonl"
EMB_MODEL = "intfloat/multilingual-e5-small"
CE_MODEL = "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1"
K_CAND = 30


def log(m):
    print(f"[{time.strftime('%H:%M:%S')}] [faz11] {m}", flush=True)


def clip(s, n):
    s = " ".join(str(s or "").split())
    return s if len(s) <= n else s[: n - 1] + "…"


# --------------------------------------------------------------------------- veri
def load_material():
    sources = P8.load_sources()
    chunks_by_src = P8.load_chunks()
    dumps = {s for s, src in sources.items() if P8.is_exam_dump(src, chunks_by_src)}
    # ada göre de: "Kurul III Sınavı" gibi belgeler içerik ölçütünden kaçabiliyor
    name_pat = re.compile(r"(s[ıi]nav|[çc][ıi]km[ıi][şs]|soru bankas|deneme s|final|b[üu]t[üu]nleme|\bb[üu]t\b|cevap anahtar)", re.I)
    dumps |= {s for s, src in sources.items() if name_pat.search((src.get("name") or "") + " " + (src.get("path") or ""))}
    chunks = []
    for sid, cs in chunks_by_src.items():
        if sid in dumps:
            continue
        for c in cs:
            t = (c.get("text") or "").strip()
            if len(t) >= 40:
                chunks.append({"chunk_id": c.get("chunk_id"), "source_id": sid, "sayfa": c.get("page"), "text": t})
    names = {s: (src.get("name") or src.get("title") or s) for s, src in sources.items()}
    return chunks, names, dumps


def load_concepts(report):
    """Faz 9'un sözlük kavramları + kanıtlı sözlük + Faz 10 Wikidata kavramları → P8.stems'e kavram belirteci."""
    concepts = {}
    try:
        concepts.update(P9.load_evidence_concepts(report))
    except Exception as e:  # noqa: BLE001
        log(f"kanıtlı sözlük yüklenemedi: {e}")
    k10 = V2 / "concept_ids" / "kavramlar.json"
    if k10.exists():
        extra = json.load(open(k10, encoding="utf-8"))
        concepts.update({cid: c for cid, c in extra.items() if len(c.get("uyeler") or []) >= 2})
    P9.install_concept_stems(concepts)
    report["kavram"] = len(concepts)
    return concepts


def load_tree():
    """Soru → güvenilir konu (yayınlanan: Faz 8 yüksek öncelikli) + kazanım kanıt chunk'ı."""
    for p in TREE:
        if p.exists():
            out = {}
            for r in P8.read_jsonl(p):
                if not r.get("kazanimlar"):
                    continue
                k = r["kazanimlar"][0]
                reliable = r.get("karar") in ("faz8_faz9_ayni", "faz8_onceligi") or (p.parent.name == "phase8" and r.get("guven") == "yuksek")
                out[r["soru_id"]] = {"konu_id": k.get("konu_id"), "konu": k.get("konu"), "ders": k.get("ders"),
                                     "kurul": k.get("kurul"), "guvenilir": reliable, "guven": r.get("guven"),
                                     "kanit_chunk": (k.get("kanit") or {}).get("chunk_id")}
            return out, p.parent.name
    return {}, None


def load_konu_sources():
    out = {}
    if KONULAR.exists():
        for k in P8.read_jsonl(KONULAR):
            out[k["konu_id"]] = {x.get("kaynak_id") for x in k.get("kaynaklar") or []}
    return out


def load_prior_slides(dumps):
    import ast
    p5, p65 = collections.defaultdict(list), collections.defaultdict(list)
    for p in (V2 / "questions").glob("*.jsonl"):
        for q in P8.read_jsonl(p):
            sm = q.get("slide_matches")
            if isinstance(sm, str):
                try:
                    sm = ast.literal_eval(sm)
                except Exception:
                    sm = []
            for m in sm or []:
                if m.get("source_id") not in dumps and m.get("chunk_id"):
                    p5[q["question_id"]].append(m["chunk_id"])
    ap = V2 / "medical_thesaurus" / "phase6_5_question_slide_anchors.jsonl"
    if ap.exists():
        for r in P8.read_jsonl(ap):
            g = r.get("gold_slide") or {}
            if g.get("chunk_id") and g.get("source_id") not in dumps:
                p65[r["question_id"]].append(g["chunk_id"])
    return p5, p65


def load_questions():
    qs = []
    for p in sorted((P8.DB / "questions").glob("*.jsonl")):
        for q in P8.read_jsonl(p):
            opts = q.get("options") or {}
            if not isinstance(opts, dict):
                opts = {}
            ans = (q.get("answer") or "").strip().upper()
            qs.append({"id": q["question_id"], "stem": q.get("stem") or "", "options": opts,
                       "answer": ans, "answer_text": opts.get(ans) or ""})
    return qs


NEG = re.compile(r"(yanl[ıi]şt[ıi]r|yanl[ıi]ş\s*olan|de[ğg]ildir|de[ğg]il\b|hari[çc]|olamaz|beklenmez|g[öo]r[üu]lmez|"
                 r"yoktur|d[ıi]ş[ıi]nda|bulunmaz|kullan[ıi]lmaz|s[öo]ylenemez)", re.I)


def pick_device() -> str:
    """Varsayılan CPU: küçük modeller CPU'da yeterince hızlı; GPU'yu Ollama ve GPU koruyucunun duraklatmaları paylaşınca
    "CUDA launch failure" görüldü. MEDS_FAZ11_DEVICE=auto ile GPU (yeterli boş bellek varsa) denenebilir."""
    if os.environ.get("MEDS_FAZ11_DEVICE", "cpu") != "auto":
        return "cpu"
    try:
        import torch
        if torch.cuda.is_available():
            free, _ = torch.cuda.mem_get_info()
            if free > 1.5 * 1024 ** 3:
                return "cuda"
        if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
            return "mps"
    except Exception:
        pass
    return "cpu"


# --------------------------------------------------------------------------- vektörler
def chunk_embeddings(chunks, device="cpu"):
    import numpy as np
    from sentence_transformers import SentenceTransformer
    OUT.mkdir(parents=True, exist_ok=True)
    key = f"{len(chunks)}_{abs(hash(chunks[0]['chunk_id'] + chunks[-1]['chunk_id'])) % 10**8}"
    f = OUT / f"emb_{key}.npy"
    model = SentenceTransformer(EMB_MODEL, device=device)
    if f.exists():
        return model, np.load(f)
    for old in OUT.glob("emb_*.npy"):
        old.unlink()
    log(f"slayt vektörleri hesaplanıyor ({len(chunks)} chunk, {device})…")
    t = time.time()
    emb = model.encode(["passage: " + c["text"][:1200] for c in chunks], batch_size=64, normalize_embeddings=True,
                       show_progress_bar=False, convert_to_numpy=True).astype("float16")  # bellek: yarım
    np.save(f, emb)
    log(f"  {round(time.time() - t)} sn")
    return model, emb


# --------------------------------------------------------------------------- ana akış
def best_sentence(text, qstems, ans_stems):
    """En ilgili satır + bir öncesi/sonrası (slaytlar madde işaretli olduğu için bağlam penceresi)."""
    sents = [x for x in re.split(r"(?<=[.!?•])\s+|\n+", text) if x.strip()]
    best_i, bs = -1, -1
    for i, s in enumerate(sents):
        st = set(P8.stems(s))
        sc = len(st & qstems) + (5 if ans_stems and ans_stems <= st else 0)
        if sc > bs and len(s) > 15:
            best_i, bs = i, sc
    if best_i < 0:
        return ""
    return clip(" … ".join(sents[max(0, best_i - 1): best_i + 2]), 380)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="yalnızca ilk N soru (deneme)")
    ap.add_argument("--sample", type=int, default=40)
    a = ap.parse_args()
    import numpy as np
    from sentence_transformers import CrossEncoder
    t0 = time.time()
    rep = {"zaman": time.strftime("%Y-%m-%dT%H:%M:%S"), "modeller": {"vektor": EMB_MODEL, "yeniden_siralama": CE_MODEL}}
    chunks, names, dumps = load_material()
    rep["materyal_chunk"], rep["sinav_dokumu_kaynak"] = len(chunks), len(dumps)
    load_concepts(rep)
    log(f"materyal {len(chunks)} chunk, kavram {rep['kavram']}")
    idx_of = {c["chunk_id"]: i for i, c in enumerate(chunks)}
    bm = P8.BM25([P8.stems(c["text"]) for c in chunks], b=0.6)
    device = pick_device()
    rep["cihaz"] = device
    emb_model, emb = chunk_embeddings(chunks, device)
    ce = CrossEncoder(CE_MODEL, device=device, max_length=384)
    tree, tree_src = load_tree()
    rep["agac_kaynagi"] = tree_src
    konu_src = load_konu_sources()
    p5, p65 = load_prior_slides(dumps)
    qs = load_questions()
    if a.limit:
        qs = qs[: a.limit]
    log(f"{len(qs)} soru işlenecek (ağaç: {tree_src})")

    OUT.mkdir(parents=True, exist_ok=True)
    tmp = OUT / "soru_slayt.jsonl.tmp"
    review = []
    stats = collections.Counter()
    qv_all = emb_model.encode(["query: " + (q["stem"] + " " + q["answer_text"]).strip()[:600] for q in qs], batch_size=64,
                              normalize_embeddings=True, show_progress_bar=False, convert_to_numpy=True)
    emb32 = emb.astype("float32")
    BLOCK = 256
    sims_block, block_start = None, -1
    with open(tmp, "w", encoding="utf-8") as out:
        for n, q in enumerate(qs):
            if n and n % 250 == 0:
                log(f"  {n}/{len(qs)}")
            if n // BLOCK != block_start:                      # soru blokları hâlinde toplu matris çarpımı
                block_start = n // BLOCK
                sims_block = qv_all[block_start * BLOCK:(block_start + 1) * BLOCK].astype("float32") @ emb32.T
            neg = bool(NEG.search(q["stem"]))
            ans_stems = set(P8.stems(q["answer_text"])) if q["answer_text"] else set()
            opt_text = " ".join(v for k, v in q["options"].items() if k != q["answer"])
            qc = collections.Counter()
            for w in P8.stems(q["stem"]):
                qc[w] += 2.0
            for w in P8.stems(q["answer_text"]):
                qc[w] += 1.0 if neg else 3.0          # olumsuz kökte doğru cevap genelde slaytta OLMAYAN bilgidir
            for w in P8.stems(opt_text):
                qc[w] += 0.4
            if not qc:
                stats["bos_soru"] += 1
                continue
            ranks = {}
            bs = bm.scores(qc)
            for r, i in enumerate(sorted(bs, key=bs.get, reverse=True)[:K_CAND]):
                ranks.setdefault(i, []).append(r)
            sims = sims_block[n - block_start * BLOCK]
            top_idx = np.argpartition(-sims, K_CAND)[:K_CAND]
            for r, i in enumerate(top_idx[np.argsort(-sims[top_idx])]):
                ranks.setdefault(int(i), []).append(r)
            tq = tree.get(q["id"]) or {}
            prior_ids = set(p5.get(q["id"], [])) | set(p65.get(q["id"], []))
            if tq.get("kanit_chunk"):
                prior_ids.add(tq["kanit_chunk"])
            for cid in prior_ids:
                if cid in idx_of:
                    ranks.setdefault(idx_of[cid], []).append(0)
            rrf = {i: sum(1 / (60 + r) for r in rs) for i, rs in ranks.items()}
            cand = sorted(rrf, key=rrf.get, reverse=True)[:K_CAND]
            if neg:   # olumsuz kök: konu = kök + şıklar (doğru cevap slaytta yanlış/eksik bilgi olabilir)
                query = (q["stem"] + " " + " ".join(q["options"].values())).strip()[:500]
            elif q["answer_text"]:
                query = (q["stem"] + " Cevap: " + q["answer_text"]).strip()[:500]
            else:     # cevabı bilinmeyen / iptal soru
                query = q["stem"].strip()[:500]
            ces = ce.predict([(query, chunks[i]["text"][:900]) for i in cand], batch_size=32, show_progress_bar=False)
            kon_sources = konu_src.get(tq.get("konu_id"), set()) if tq else set()
            use_ans = bool(ans_stems) and not neg
            scored = []
            for i, c in zip(cand, ces):
                ch = chunks[i]
                # kök toleranslı: "glukagon" ↔ "glukagonun / glukagondur"
                has_ans = use_ans and ans_stems <= set(P8.stems(ch["text"]))
                in_konu = ch["source_id"] in kon_sources
                prior = ch["chunk_id"] in prior_ids
                b_konu = 1.5 if in_konu and tq.get("guvenilir") else 0.6 if in_konu else 0.0
                b_ans = 1.0 if has_ans else 0.0
                b_prior = 0.5 if prior else 0.0
                final = float(c) + b_konu + b_ans + b_prior
                scored.append((final, float(c), i, has_ans, in_konu, prior, (b_konu, b_ans, b_prior)))
            scored.sort(reverse=True)
            top = scored[0]
            other_src = next((s for s in scored[1:] if chunks[s[2]]["source_id"] != chunks[top[2]]["source_id"]), None)
            # başka kaynak aday yoksa fark ölçülemez → 0 (güven yapay olarak yükselmesin)
            margin = top[0] - other_src[0] if other_src else 0.0
            # Kalibrasyon (2026-10-06, 30 örnek elle denetim): yanlışların hepsinde başka kaynakla fark ≤ 0,74 ve
            # (biri hariç) konu kaynağı desteği yoktu; doğruların çoğunda fark ≥ 1 ya da güvenilir konu kaynağı vardı.
            in_konu = top[4]
            if (top[1] >= 3 and margin >= 1.0) or (in_konu and margin >= 1.0 and top[1] >= 0):
                conf = "yuksek"
            elif margin >= 1.0 or (in_konu and margin >= 0.5) or top[1] >= 3:
                conf = "orta"
            else:
                conf = "dusuk"
            stats["guven_" + conf] += 1
            qst = set(P8.stems(q["stem"] + " " + q["answer_text"]))
            stats["olumsuz_kok"] += neg
            slides, seen = [], set()
            for s in scored:
                ch = chunks[s[2]]
                key = (ch["source_id"], ch["sayfa"])
                if key in seen:
                    continue
                seen.add(key)
                why = [w for w, f in (("cevap_slaytta", s[3]), ("konu_kaynagi", s[4]), ("onceki_eslesme", s[5])) if f]
                slides.append({"source_id": ch["source_id"], "kaynak": names.get(ch["source_id"], ch["source_id"]),
                               "sayfa": ch["sayfa"], "chunk_id": ch["chunk_id"], "skor": round(s[0], 2),
                               "ce": round(s[1], 2),
                               "puan_ayrimi": {"cross_encoder": round(s[1], 2), "konu": s[6][0], "cevap": s[6][1], "onceki": s[6][2]},
                               "gerekce": why, "alinti": best_sentence(ch["text"], qst, ans_stems if use_ans else set())})
                if len(slides) >= 3:
                    break
            rec = {"soru_id": q["id"], "guven": conf, "fark": round(margin, 2), "soru_tipi": "olumsuz" if neg else "olumlu",
                   "slaytlar": slides,
                   "konu": {k: tq.get(k) for k in ("kurul", "ders", "konu", "konu_id", "guvenilir")} if tq else None}
            out.write(json.dumps(rec, ensure_ascii=False) + "\n")
            if conf == "dusuk":
                review.append({**rec, "stem": clip(q["stem"], 200), "neden": "düşük güven: net slayt kanıtı yok"})
            stats["cevap_slaytta"] += top[3]
            stats["konu_kaynagi"] += top[4]
    if not stats.get("guven_yuksek") and not stats.get("guven_orta"):
        log("anlamlı sonuç yok; önceki çıktı korunuyor")
        tmp.unlink()
        return 1
    os.replace(tmp, OUT / "soru_slayt.jsonl")
    with open(OUT / "hakem_kuyrugu.jsonl", "w", encoding="utf-8") as f:
        for r in review:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    rep["sorular"] = dict(stats)
    rep["sure_sn"] = round(time.time() - t0, 1)
    if a.sample:
        recs = [json.loads(l) for l in open(OUT / "soru_slayt.jsonl", encoding="utf-8")]
        random.seed(11)
        qmap = {q["id"]: q for q in qs}
        pick = random.sample(recs, min(a.sample, len(recs)))
        json.dump([{"soru": clip(qmap[r["soru_id"]]["stem"], 220), "cevap": qmap[r["soru_id"]]["answer_text"],
                    "guven": r["guven"], "slayt": r["slaytlar"][0]["kaynak"] if r["slaytlar"] else None,
                    "sayfa": r["slaytlar"][0]["sayfa"] if r["slaytlar"] else None,
                    "alinti": r["slaytlar"][0]["alinti"] if r["slaytlar"] else None} for r in pick],
                  open(OUT / "elle_kontrol_ornegi.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(rep, open(OUT / "rapor.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(rep, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
