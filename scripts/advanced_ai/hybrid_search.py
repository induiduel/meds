"""
BM25 + Dense Retrieval (bge-m3) Hibrit Arama & Reranker Motoru
"""
import numpy as np
from rank_bm25 import BM25Okapi
import re
from typing import List, Dict, Any

class HybridSearchEngine:
    def __init__(self, chunks: List[Dict[str, Any]], vectors: np.ndarray):
        """
        chunks: [{'chunk_id': ..., 'text': ..., 'heading_path': ..., ...}]
        vectors: (N, 1024) bge-m3 normalize edilmiş dense vektör matrisi
        """
        self.chunks = chunks
        self.vectors = vectors
        self.tokenized_corpus = [self._tokenize(c["text"]) for c in chunks]
        self.bm25 = BM25Okapi(self.tokenized_corpus)

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        text = text.lower()
        # Türkçe karakter sadeleştirme ve harf/sayı ayırma
        tr_map = str.maketrans("çğıöşüâîû", "cgiosuaiu")
        text = text.translate(tr_map)
        return re.findall(r"\w+", text)

    def search(self, query: str, query_vec: np.ndarray, top_k: int = 10, alpha: float = 0.5) -> List[Dict[str, Any]]:
        """
        alpha: 0.0 -> Sadece BM25 (anahtar kelime), 1.0 -> Sadece Dense (anlamsal)
        0.5 -> Hibrit (Reciprocal Rank Fusion veya Score Blend)
        """
        if not self.chunks:
            return []

        # 1. BM25 Skorları
        q_tokens = self._tokenize(query)
        bm25_scores = np.array(self.bm25.get_scores(q_tokens), dtype=np.float32)
        if bm25_scores.max() > 0:
            bm25_norm = bm25_scores / (bm25_scores.max() + 1e-9)
        else:
            bm25_norm = bm25_scores

        # 2. Dense Cosine Benzerlikleri
        if query_vec.ndim == 1:
            query_vec = query_vec.reshape(1, -1)
        # vectors zaten L2 normalize edilmiş olduğundan dot product = kosinüs benzerliğidir
        dense_scores = (self.vectors @ query_vec.T).squeeze(-1)
        # -1..1 aralığını 0..1 aralığına çek
        dense_norm = np.clip((dense_scores + 1.0) / 2.0, 0.0, 1.0)

        # 3. Hibrit Harmanlama (Hybrid Fusion)
        hybrid_scores = (1 - alpha) * bm25_norm + alpha * dense_norm

        top_indices = np.argsort(hybrid_scores)[::-1][:top_k]

        results = []
        for idx in top_indices:
            res = dict(self.chunks[idx])
            res["score_hybrid"] = float(hybrid_scores[idx])
            res["score_dense"] = float(dense_scores[idx])
            res["score_bm25"] = float(bm25_norm[idx])
            results.append(res)
        return results

    @staticmethod
    def rerank_bge(query: str, candidates: List[Dict[str, Any]], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Çapraz Dikkat (Cross-Encoder / Rerank) Benzetimi & Terim Ağırlıklı Sıralama
        Tıbbi terminoloji örtüşmesi, soru kökü eşleşmesi ve slayt başlığı uyumu
        """
        q_toks = set(HybridSearchEngine._tokenize(query))
        for cand in candidates:
            c_toks = set(HybridSearchEngine._tokenize(cand.get("text", "")))
            heading_toks = set(HybridSearchEngine._tokenize(" ".join(cand.get("heading_path", []))))
            
            overlap_text = len(q_toks & c_toks) / max(1, len(q_toks))
            overlap_heading = len(q_toks & heading_toks) / max(1, len(q_toks))
            
            # Yeniden sıralama skoru: Hibrit skor + Slayt başlığı örtüşmesi + Tıbbi terim örtüşmesi
            rerank_score = cand.get("score_hybrid", 0.5) * 0.6 + overlap_heading * 0.25 + overlap_text * 0.15
            cand["rerank_score"] = float(round(rerank_score, 4))

        candidates.sort(key=lambda x: x["rerank_score"], reverse=True)
        return candidates[:top_k]
