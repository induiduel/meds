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

    def search(self, query: str, query_vec: np.ndarray, top_k: int = 10, rrf_k: int = 60, alpha: float = 0.5) -> List[Dict[str, Any]]:
        """
        RRF (Reciprocal Rank Fusion):
        RRF_Score(d) = (1 - alpha) * (1 / (rrf_k + rank_bm25(d))) + alpha * (1 / (rrf_k + rank_dense(d)))
        Standart RRF için alpha=0.5 alınır.
        """
        if not self.chunks:
            return []

        # 1. BM25 Skorları & Sıralaması
        q_tokens = self._tokenize(query)
        bm25_scores = np.array(self.bm25.get_scores(q_tokens), dtype=np.float32)
        # BM25 rank sırası (0: en yüksek skorlu)
        bm25_order = np.argsort(-bm25_scores)
        bm25_ranks = np.empty_like(bm25_order)
        bm25_ranks[bm25_order] = np.arange(len(bm25_scores)) + 1

        # 2. Dense Cosine Benzerlikleri & Sıralaması
        if query_vec.ndim == 1:
            query_vec = query_vec.reshape(1, -1)
        # vectors zaten L2 normalize edilmiş olduğundan dot product = kosinüs benzerliğidir
        dense_scores = (self.vectors @ query_vec.T).squeeze(-1)
        dense_order = np.argsort(-dense_scores)
        dense_ranks = np.empty_like(dense_order)
        dense_ranks[dense_order] = np.arange(len(dense_scores)) + 1

        # 3. Reciprocal Rank Fusion (RRF)
        # RRF_Score(d) = 1/(k + rank_dense) + 1/(k + rank_bm25)
        rrf_bm25 = 1.0 / (rrf_k + bm25_ranks)
        rrf_dense = 1.0 / (rrf_k + dense_ranks)
        rrf_scores = (1.0 - alpha) * rrf_bm25 + alpha * rrf_dense

        # En yüksek RRF skorlu adaylar
        top_indices = np.argsort(-rrf_scores)[:top_k]

        results = []
        for idx in top_indices:
            res = dict(self.chunks[idx])
            res["score_rrf"] = float(round(rrf_scores[idx], 6))
            res["score_dense"] = float(round(dense_scores[idx], 4))
            res["score_bm25"] = float(round(bm25_scores[idx], 4))
            res["rank_dense"] = int(dense_ranks[idx])
            res["rank_bm25"] = int(bm25_ranks[idx])
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
            
            # Yeniden sıralama skoru: RRF skoru (veya dense benzerlik) + Slayt başlığı örtüşmesi + Tıbbi terim örtüşmesi
            base_score = cand.get("score_rrf", cand.get("score_dense", 0.5))
            rerank_score = base_score * 0.6 + overlap_heading * 0.25 + overlap_text * 0.15
            cand["rerank_score"] = float(round(rerank_score, 4))

        candidates.sort(key=lambda x: x["rerank_score"], reverse=True)
        return candidates[:top_k]
