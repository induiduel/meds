#!/usr/bin/env python3
"""
Crowdsource Question Reconstruction Benchmark & Evaluation Suite
================================================================
Yeniden inşa edilen tıp sorularını referans (orijinal) sorular ile karşılaştırıp
anlamsal (vektörel) ve morfolojik (token-düzeyi) başarı skorlarını hesaplar.

Metrikler:
- Anlamsal Vektör Benzerliği (Cosine Semantic Similarity, E5-small / BGE-M3)
- Token Düzeyi Bulanık Eşleme (RapidFuzz Token-Sort Ratio)
- Birleşik Doğruluk Skoru: 0.6 * Anlamsal + 0.4 * Token Eşleşmesi

Kısıtlar:
- GPU YASAK (AGENTS.md Kural 10).
- CPU mikroservisleri üzerinden vektörleme yapılır.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# GPU YASAK
os.environ["CUDA_VISIBLE_DEVICES"] = ""

import numpy as np
import requests
from rapidfuzz import fuzz

DEFAULT_E5_URL = os.environ.get("MEDS_EMBED_E5_URL", "http://127.0.0.1:8091/embed")
DEFAULT_BGE_URL = os.environ.get("MEDS_EMBED_BGE_URL", "http://127.0.0.1:8094/embed")


def get_embeddings(texts: List[str], url: str = DEFAULT_E5_URL) -> np.ndarray:
    """Mikroservisten L2 normalize edilmiş embedding vektörlerini çeker."""
    try:
        resp = requests.post(url, json={"texts": texts}, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        embeddings = data.get("vectors") or data.get("embeddings") or data.get("dense_embeddings") or data.get("data")
        arr = np.array(embeddings, dtype=np.float32)
        norms = np.linalg.norm(arr, axis=1, keepdims=True)
        return arr / np.maximum(norms, 1e-9)
    except Exception as e:
        print(f"[UYARI] Embedding servisine ulaşılamadı ({url}): {e}")
        return np.zeros((len(texts), 0), dtype=np.float32)


def evaluate_pairs(
    pairs: List[Dict[str, str]],
    embed_url: str = DEFAULT_E5_URL,
) -> Dict[str, Any]:
    """Her soru çifti için token ve vektör benzerliklerini hesaplar."""
    reconstructed_texts = [p["reconstructed"] for p in pairs]
    original_texts = [p["original"] for p in pairs]

    # Vektörleri al
    print(f"Toplam {len(pairs)} soru için anlamsal embedding'ler hesaplanıyor...")
    rec_vecs = get_embeddings(reconstructed_texts, url=embed_url)
    orig_vecs = get_embeddings(original_texts, url=embed_url)

    results = []
    semantic_scores = []
    token_scores = []
    combined_scores = []

    for idx, p in enumerate(pairs):
        rec = p["reconstructed"]
        orig = p["original"]

        # 1. Token-level fuzzy match
        token_sim = fuzz.token_sort_ratio(orig, rec)
        token_scores.append(token_sim)

        # 2. Semantic cosine similarity
        if rec_vecs.shape[1] > 0 and orig_vecs.shape[1] > 0:
            cos_sim = float(np.dot(rec_vecs[idx], orig_vecs[idx]))
            sem_sim = max(0.0, min(100.0, cos_sim * 100.0))
        else:
            sem_sim = token_sim
        semantic_scores.append(sem_sim)

        # 3. Combined score
        combined = 0.6 * sem_sim + 0.4 * token_sim
        combined_scores.append(combined)

        results.append({
            "id": p.get("id", idx + 1),
            "label": p.get("label", f"Soru {idx + 1}"),
            "original": orig,
            "reconstructed": rec,
            "token_similarity_pct": round(token_sim, 2),
            "semantic_similarity_pct": round(sem_sim, 2),
            "combined_similarity_pct": round(combined, 2),
        })

    summary = {
        "total_evaluated": len(pairs),
        "mean_semantic_similarity_pct": round(float(np.mean(semantic_scores)), 2),
        "mean_token_similarity_pct": round(float(np.mean(token_scores)), 2),
        "mean_combined_similarity_pct": round(float(np.mean(combined_scores)), 2),
        "min_combined_pct": round(float(np.min(combined_scores)), 2),
        "max_combined_pct": round(float(np.max(combined_scores)), 2),
        "detailed_results": results,
    }

    return summary


def main():
    parser = argparse.ArgumentParser(description="Evaluate Crowdsource Question Reconstruction")
    parser.add_argument("--results-file", type=Path, default=Path(__file__).parent / "results" / "benchmark_challenging_14q.json", help="Değerlendirilecek rekonstrüksiyon sonuç JSON dosyası")
    parser.add_argument("--embed-url", type=str, default=DEFAULT_E5_URL, help="Embedding mikroservis URL'i (varsayılan :8091)")
    parser.add_argument("--out", type=Path, default=None, help="Opsiyonel değerlendirme rapor çıktısı")
    args = parser.parse_args()

    if not args.results_file.exists():
        print(f"Hata: Dosya bulunamadı: {args.results_file}")
        sys.exit(1)

    with open(args.results_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Veri formatına göre soru çiftlerini hazırla
    pairs = []
    if isinstance(data, list):
        for item in data:
            orig = item.get("orijinal_soru_koku") or item.get("orijinal_soru", "")
            rec = item.get("distilbart_sorusu") or item.get("reconstructed_question", "")
            if orig and rec:
                pairs.append({
                    "id": item.get("soru_id"),
                    "label": item.get("klinik_konu", ""),
                    "original": orig,
                    "reconstructed": rec,
                })
    elif isinstance(data, dict) and "questions" in data:
        for q in data["questions"]:
            orig = q.get("orijinal_soru", "")
            rec = q.get("reconstructed_question", "")
            if orig and rec:
                pairs.append({
                    "id": q.get("cluster_id"),
                    "label": q.get("label", ""),
                    "original": orig,
                    "reconstructed": rec,
                })

    if not pairs:
        print("[Bilgi] Doğrudan karşılaştırılacak çift bulunamadı veya sonuç dosyasında zaten skorlar mevcut.")
        return

    eval_summary = evaluate_pairs(pairs, embed_url=args.embed_url)

    print("\n" + "=" * 70)
    print("DEĞERLENDİRME VE BENZETİM BAŞARI RAPORU")
    print("=" * 70)
    print(f"Toplam Değerlendirilen Soru: {eval_summary['total_evaluated']}")
    print(f"Ortalama Anlamsal Benzerlik (Cosine): %{eval_summary['mean_semantic_similarity_pct']}")
    print(f"Ortalama Token Eşleşmesi (RapidFuzz): %{eval_summary['mean_token_similarity_pct']}")
    print(f"Bileşik Başarı Skoru (Combined):      %{eval_summary['mean_combined_similarity_pct']}")
    print("=" * 70)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(eval_summary, f, ensure_ascii=False, indent=2)
        print(f"Rapor dosyası kaydedildi: {args.out}")


if __name__ == "__main__":
    main()
