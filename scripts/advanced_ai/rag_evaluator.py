#!/usr/bin/env python3
"""
MedSoru RAG Değerlendirme (Evaluation) Test Scripti
Metrikler: Hit Rate@1, Hit Rate@3, Hit Rate@5, MRR (Mean Reciprocal Rank)
Ground Truth: Sorunun 'evidence.chunk_id' veya 'doc_source_id' / 'kaynak.source_id' bilgisi.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from pathlib import Path
import numpy as np

# Ajan kütüphanesini ve hibrit arama motorunu dahil et
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR / "scripts" / "agents"))
sys.path.insert(0, str(ROOT_DIR / "scripts" / "advanced_ai"))

import lib
from hybrid_search import HybridSearchEngine

log = lib.get_logger("rag_eval")

def load_eval_dataset(limit: int = 50) -> list[dict]:
    """Test için kanıtlanmış (evidence içeren) soruları toplar."""
    candidates = []
    
    # 1. Aşama 4 veritabanından veya temp3'ten oku
    q_paths = [
        lib.TEMP3 / "questions.jsonl",
        ROOT_DIR.parent / "meds_database" / "questions" / "verified.jsonl"
    ]
    
    for qp in q_paths:
        if qp.exists():
            for line in qp.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                try:
                    q = json.loads(line)
                    ev = q.get("evidence") or q.get("kaynak") or {}
                    target_chunk = ev.get("chunk_id") or q.get("matched_chunk_id")
                    target_src = ev.get("source_id") or q.get("doc_source_id") or q.get("source_id")
                    
                    if q.get("stem") and (target_chunk or target_src):
                        candidates.append({
                            "question_id": q.get("question_id") or q.get("no") or "q_unknown",
                            "stem": q["stem"],
                            "options": q.get("options", {}),
                            "target_chunk_id": target_chunk,
                            "target_source_id": target_src
                        })
                except Exception:
                    pass

    # Eğer temp3/questions.jsonl boşsa temp2'deki çıkmış soruları tara
    if not candidates:
        for f in (lib.TEMP2).rglob("*.json"):
            d = lib.read_json(f, {})
            if d.get("meta", {}).get("doc_type") == "past_question":
                sid, _ = lib.source_id_for(d["rel"])
                for q in d.get("questions", []):
                    if q.get("stem"):
                        candidates.append({
                            "question_id": q.get("no", "q_temp2"),
                            "stem": q["stem"],
                            "options": q.get("options", {}),
                            "target_chunk_id": None,
                            "target_source_id": sid
                        })

    if not candidates:
        return []

    random.seed(42)
    random.shuffle(candidates)
    return candidates[:limit]

def run_evaluation(num_samples: int = 30, use_hybrid: bool = True):
    print("=" * 65)
    print("🏥 MedSoru RAG Kalite & Erişim Doğrulama (Evaluation) Başlatılıyor...")
    print("=" * 65)

    # 1. Chunk'ları ve BGE-M3 Vektörlerini Yükle
    chunk_dir = lib.TEMP3 / "chunks"
    vec_dir = lib.TEMP3 / "vectors"
    
    chunks = []
    vec_list = []
    
    if not chunk_dir.exists():
        print(f"❌ Chunk dizini bulunamadı: {chunk_dir}")
        return

    print("📦 Chunk'lar ve BGE-M3 indeksleri yükleniyor...")
    for cf in sorted(chunk_dir.glob("*.jsonl")):
        vf = vec_dir / f"{cf.stem}.npy"
        if not vf.exists():
            continue
        c_rows = lib.read_jsonl(cf)
        v_mat = np.load(vf)
        if len(c_rows) == len(v_mat):
            chunks.extend(c_rows)
            vec_list.append(v_mat)

    if not chunks:
        print("❌ Sistemde yüklü chunk ve vektör bulunamadı. Lütfen önce Aşama 3'ü çalıştırın.")
        return

    all_vectors = np.vstack(vec_list)
    print(f"✅ Toplam {len(chunks)} chunk ve vektör hafızaya yüklendi.")

    # Hibrit motoru ayağa kaldır
    engine = HybridSearchEngine(chunks, all_vectors) if use_hybrid else None

    # 2. Değerlendirme Veri Kümesini Getir
    dataset = load_eval_dataset(limit=num_samples)
    print(f"🎯 Test için {len(dataset)} adet tıbbi soru belirlendi.\n")

    if not dataset:
        print("❌ Test edilecek soru bulunamadı.")
        return

    hit_1 = 0
    hit_3 = 0
    hit_5 = 0
    reciprocal_ranks = []
    
    faithfulness_scores = []
    
    t0 = time.time()

    for idx, item in enumerate(dataset, 1):
        query_text = item["stem"]
        target_chunk = item["target_chunk_id"]
        target_src = item["target_source_id"]

        # Soru vektörünü hesapla
        q_vec = lib.embed([query_text])[0]

        if use_hybrid:
            # Multi-Query Expansion & Top-25 RRF Arama
            multi_queries = HybridSearchEngine.expand_medical_queries(query_text)
            all_candidates = []
            seen_chunk_ids = set()
            
            for mq in multi_queries[:2]:
                mq_vec = lib.embed([mq])[0]
                cands = engine.search(query=mq, query_vec=mq_vec, top_k=25)
                for c in cands:
                    if c["chunk_id"] not in seen_chunk_ids:
                        seen_chunk_ids.add(c["chunk_id"])
                        all_candidates.append(c)
            
            # Cross-Encoder Reranker ile Top-25 -> Top-5
            ranked_results = HybridSearchEngine.rerank_bge(query_text, all_candidates, top_k=5)
        else:
            scores = all_vectors @ q_vec
            top_idx = np.argsort(-scores)[:5]
            ranked_results = [chunks[i] for i in top_idx]

        # Başarı tespiti
        found_rank = None
        best_match_chunk = None
        for r_idx, res in enumerate(ranked_results, 1):
            is_match = False
            if target_chunk and res.get("chunk_id") == target_chunk:
                is_match = True
            elif target_src and res.get("source_id") == target_src:
                is_match = True

            if is_match:
                found_rank = r_idx
                best_match_chunk = res
                break

        # Faithfulness (Sadakat Oranı / support_ratio) Hesaplama
        if ranked_results:
            top_content = ranked_results[0].get("text", "")
            q_tokens = set(lib.tokens(query_text))
            c_tokens = set(lib.tokens(top_content))
            faith = len(q_tokens & c_tokens) / max(1, len(q_tokens))
            faithfulness_scores.append(faith)

        if found_rank == 1:
            hit_1 += 1
        if found_rank and found_rank <= 3:
            hit_3 += 1
        if found_rank and found_rank <= 5:
            hit_5 += 1

        if found_rank:
            reciprocal_ranks.append(1.0 / found_rank)
        else:
            reciprocal_ranks.append(0.0)

        status_icon = f"✅ (Sıra: {found_rank})" if found_rank else "❌ (Bulunamadı)"
        print(f"[{idx:02d}/{len(dataset):02d}] Soru: {query_text[:60]}... -> {status_icon}")

    elapsed = time.time() - t0
    n = max(1, len(dataset))
    avg_faithfulness = (sum(faithfulness_scores) / len(faithfulness_scores)) if faithfulness_scores else 0.0

    print("\n" + "=" * 65)
    print("📊 RAG EVALUATION SONUÇ RAPORU (4 EKSEN)")
    print("=" * 65)
    print(f"• Toplam Test Sorusu         : {len(dataset)}")
    print(f"• Test Süresi                : {elapsed:.2f} sn (Soru başına ~{elapsed/n:.2f} sn)")
    print(f"• Hit Rate @ 1 (En tepede)   : %{(hit_1 / n) * 100:.2f} ({hit_1}/{n})")
    print(f"• Hit Rate @ 3 (Top-3'te)    : %{(hit_3 / n) * 100:.2f} ({hit_3}/{n})")
    print(f"• Hit Rate @ 5 (Top-5'te)    : %{(hit_5 / n) * 100:.2f} ({hit_5}/{n})")
    print(f"• MRR (Mean Reciprocal Rank) : {np.mean(reciprocal_ranks):.4f}")
    print(f"• Faithfulness (Sadakat)     : %{avg_faithfulness * 100:.2f}")
    print("=" * 65)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=20, help="Test edilecek soru adedi")
    parser.add_argument("--dense-only", action="store_true", help="Sadece dense embedding kullan")
    args = parser.parse_args()

    run_evaluation(num_samples=args.samples, use_hybrid=not args.dense_only)
