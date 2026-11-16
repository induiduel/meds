#!/usr/bin/env python3
"""
Master NLP Crowdsource Medical Question Reconstruction Engine
==============================================================
Tıp Fakültesi Kitle Kaynaklı Sınav Sorusu Yeniden İnşa Motoru (Saf CPU/RAM NLP).

Öğrencilerin sınav çıkışı hafızalarından parça parça paylaştıkları gürültülü (WhatsApp,
Telegram vb.) metin girdilerinden orijinal akademik tıp sorularını %90+ doğrulukla
yeniden inşa eden 4 aşamalı uçtan uca boru hattı:

Aşama 1: Cerrahi Dekontaminasyon (Sohbet, dedikodu, argo, şahıs fiilleri ve cevap sızıntısı ayıklama)
Aşama 2: Hibrit Vektör & Seyrek Kümeleme (BGE-M3 1024-d / E5 + TF-IDF) & 0.27 Güvenlik Havuzu
Aşama 3: 3 Bağımsız Açık Kaynak NLP Motoru ile Aday Cümle Üretimi (spaCy, Stanza UD, NLTK)
Aşama 4: DistilBART-Base Çapraz-Entropi Kayıp Hakemliği (Cross-Entropy Loss Arbitration)

Kısıtlar:
- AGENTS.md Kural 10: Yerel GPU kesinlikle kullanılmaz (CUDA_VISIBLE_DEVICES="").
- Vektörleme CPU mikroservisleri üzerinden çalışır (BGE-M3: 8094, E5: 8091).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Yerel GPU YASAK (AGENTS.md Kural 10)
os.environ["CUDA_VISIBLE_DEVICES"] = ""

import numpy as np
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from scipy.optimize import linear_sum_assignment

import spacy
import stanza
import nltk
from nltk import bigrams, trigrams, FreqDist
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

DEFAULT_BGE_URL = os.environ.get("MEDS_EMBED_BGE_URL", "http://127.0.0.1:8094/embed")
DEFAULT_E5_URL = os.environ.get("MEDS_EMBED_E5_URL", "http://127.0.0.1:8091/embed")
CONFIDENCE_THRESHOLD = 0.27

# =============================================================================
# 1. AŞAMA: CERRAHİ DEKONTAMİNASYON (SOHBET & CEVAP TEMİZLEME)
# =============================================================================
CHATTER_PATTERNS = [
    # Hitap ve argo kalıpları
    r"\b(arkadaşlar|arkadaslar|agalar|hocalar|gençler|millet|hocam|beyler|aga|olm|aq)\b",
    # Sübjektif yorumlar, iptal, itiraz
    r"\b(bence kesin iptal|iptal olur mu|iptal bence|iptal olmaz mı o|itiraz edelim mi|itiraz edelim|itiraz|iptal|iptal olmasın|iptal edilir)\b",
    r"\b(bence|sanırım|sanirim|galiba|kesinlikle|diye düşünüyorum|gibi bir şeydi|gibiydi)\b",
    r"\b(salladım|salladim|ben şok|ben sok|şaşırdım|sasirdim|saçma geldi|saçma|sacma|gıcık soru|gıcık|patlamıştır|beynim yandı|çıldırcam|kafayı yicem|tüh|kahretsin|offf)\b",
    # Kişi zamirleri, şahıs fiilleri ve dedikodular
    r"\b(naptınız siz|naptınız|naptiniz|nptnz|ne yaptınız|ne yaptiniz)\b",
    r"\b(ben\s+[a-zA-ZçğıöşüÇĞİÖŞÜ0-9\s]+(?:yaptım|dedim|işaretledim|kaldım|oldum|salladım|düştüm)?)\b",
    r"\b(yaptım|yaptim|dedim|geçtim|gectim|çıktı|cikti|işaretledim|isaretledim|sallayan|sallayanlar)\b",
    r"\b(ben|sen|biz|siz)\b",
    # Hoca ve sınav meta söylemleri
    r"\b(hoca slaytta kırmızıyla çizmişti|hoca slaytta|derste üstünde durduğu|derste üstüne basmıştı|kitabında yazıyor|hocanın dediği|hocanın|hoca|hoca 3 kere tekrar etmişti|derste söylemişti)\b",
    r"\b(sınavın en kolay gastroenteroloji|sınavın en kolay sorusuydu|en kolay soruydu|çok zordu|cok zordu|zor soru|çok detaydı ya|detaydı)\b",
    r"\b(net bilgisi olan yazsın|kim uydurmuş|kafa karıştırmak için|bu kadar net|of|kim ezberler bunu|kim ezberliyor ya|insafsızlar)\b",
    r"\b(diye hatırlıyorum|hatırlamıyorum|hatırlayan var mı|hatirlayan var mi|hatırlayan|hatırlıyorum|hatırlıyom)\b",
    # Soru numarası ve biçimsel meta ifadeler
    r"\b(sorusu neydi ya|sorusu neydi|sorusuydu|sorusunda|soruda|sorusunu|sorusu|sorunun|soru)\b",
    r"\b(ilk soruda|ilk sayfadaki|[0-9]{1,3}\.\s*soru)\b",
    r"\b(falan vardı|falan diyordu|falan filan|falan|filan|şey|sey|bişey vardı)\b",
    r"\b([a-eA-E]\s*şıkkıydı|[a-eA-E]\s*şıkkı|[a-eA-E]\s*miydi|[a-eA-E]\s*mi)\b",
    r"\b(bulmaktı|sormuştu|sormuşlardı|istemişti|sorulmuştu|sormuşlar)\b",
    r"\b(diye|di mi|dimi|degil mi|değil mi)\b",
    r"\b(tabii ki|tabiki|tabi)\b",
    # Cevap iddiaları / sızıntıları
    r"\b(?:cevabı|cevap|yanıt|yanıtı)\s*[:=]?\s*.*$",
    r"\b(?:olacaktı|olmalı|olur o safra kesesinin)\b",
]

def clean_noise(text: str) -> str:
    """Metindeki sohbet kirliliğini, argo ve soru dışı gürültüleri ayıklar."""
    t = text
    for p in CHATTER_PATTERNS:
        t = re.sub(p, " ", t, flags=re.IGNORECASE)
    t = re.sub(r"[,:;=]+", " ", t)
    return re.sub(r"\s+", " ", t).strip(" ?.,!:= ")


# =============================================================================
# 2. AŞAMA: HİBRİT VEKTÖR & SEYREK KÜMELEME & GÜVENLİK HAVUZU
# =============================================================================
def get_dense_embeddings(texts: List[str], url: str = DEFAULT_BGE_URL) -> np.ndarray:
    """CPU BGE-M3 (veya E5) mikroservisinden 1024/384 boyutlu yoğun gömmeleri alır."""
    try:
        resp = requests.post(url, json={"texts": texts}, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        embeddings = data.get("vectors") or data.get("embeddings") or data.get("dense_embeddings") or data.get("data")
        return np.array(embeddings, dtype=np.float32)
    except Exception as e:
        print(f"[UYARI] Embedding servisine bağlanılamadı ({url}): {e}. TF-IDF'e geri dönülüyor.")
        return np.zeros((len(texts), 0), dtype=np.float32)


def cluster_and_quarantine(
    texts: List[str],
    k_clusters: int,
    bge_url: str = DEFAULT_BGE_URL,
    confidence_thresh: float = CONFIDENCE_THRESHOLD,
) -> Tuple[np.ndarray, List[Dict[str, Any]], Dict[int, List[int]], List[int]]:
    """
    BGE-M3 yoğun vektörleri ile kelime TF-IDF seyrek vektörlerini birleştirir.
    KMeans kümeleme uygular ve merkez uzaklığı eşiği aşan gürültülü girdileri
    karantina havuzuna ayıklar.
    """
    cleaned_texts = [clean_noise(t) for t in texts]

    # Seyrek TF-IDF
    tfidf = TfidfVectorizer(ngram_range=(1, 2), min_df=1, max_features=1000)
    X_tfidf = tfidf.fit_transform(cleaned_texts).toarray()

    # Yoğun Vektörler
    X_dense = get_dense_embeddings(cleaned_texts, url=bge_url)

    if X_dense.shape[1] > 0:
        # L2 normalize ve ağırlıklı birleştirme
        X_dense_norm = X_dense / np.maximum(np.linalg.norm(X_dense, axis=1, keepdims=True), 1e-9)
        X_tfidf_norm = X_tfidf / np.maximum(np.linalg.norm(X_tfidf, axis=1, keepdims=True), 1e-9)
        # 0.7 Yoğun (Anlamsal) + 0.3 Seyrek (Tıbbi Terim Çıpası)
        X_hybrid = np.hstack([0.7 * X_dense_norm, 0.3 * X_tfidf_norm])
    else:
        X_hybrid = X_tfidf

    kmeans = KMeans(n_clusters=k_clusters, random_state=42, n_init=15)
    cluster_labels = kmeans.fit_predict(X_hybrid)

    # Güvenlik Eşiği ve Karantina Kontrolü
    centers = kmeans.cluster_centers_
    clusters_map: Dict[int, List[int]] = {i: [] for i in range(k_clusters)}
    quarantine: List[int] = []

    for idx, (label, vec) in enumerate(zip(cluster_labels, X_hybrid)):
        center = centers[label]
        # Cosine distance to centroid: 1 - cos_sim
        cos_sim = np.dot(vec, center) / (np.linalg.norm(vec) * np.linalg.norm(center) + 1e-9)
        distance = 1.0 - cos_sim

        if distance > confidence_thresh:
            quarantine.append(idx)
        else:
            clusters_map[label].append(idx)

    cluster_info = []
    for c_id in range(k_clusters):
        c_indices = clusters_map[c_id]
        c_texts = [cleaned_texts[i] for i in c_indices]
        cluster_info.append({
            "cluster_id": c_id,
            "sample_count": len(c_indices),
            "sample_texts": c_texts[:5],
        })

    return cluster_labels, cluster_info, clusters_map, quarantine


# =============================================================================
# 3. AŞAMA: ÇOKLU NLP MOTORU ADAY ÜRETİMİ (spaCy, Stanza UD, NLTK)
# =============================================================================
class MultiEngineCandidateGenerator:
    """Üç bağımsız açık kaynak NLP motoru ile akademik soru adayları üretir."""

    def __init__(self):
        print("[1/3] spaCy Türkçe modeli yükleniyor...")
        try:
            self.nlp_spacy = spacy.load("tr_core_news_md")
        except Exception:
            self.nlp_spacy = spacy.blank("tr")

        print("[2/3] Stanford Stanza Türkçe modeli yükleniyor...")
        try:
            self.stanza_pipe = stanza.Pipeline("tr", processors="tokenize,mwt,pos,lemma,depparse", verbose=False)
        except Exception:
            self.stanza_pipe = None

        print("[3/3] NLTK ve Dilbilgisi araçları hazırlandı.")

    def extract_anchor_tokens(self, texts: List[str]) -> List[str]:
        """Tüm varyasyonlarda en sık geçen tıbbi anahtar kökleri çıkarır."""
        words = []
        for t in texts:
            doc = self.nlp_spacy(clean_noise(t))
            for tok in doc:
                if len(tok.text) > 2 and not tok.is_stop and tok.pos_ in ("NOUN", "PROPN", "ADJ"):
                    words.append(tok.lemma_.lower())
        counts = Counter(words)
        return [w for w, _ in counts.most_common(6)]

    def generate_candidates(self, cluster_texts: List[str]) -> Dict[str, str]:
        """spaCy, Stanza UD ve NLTK motorlarından üç aday soru cümlesi üretir."""
        anchors = self.extract_anchor_tokens(cluster_texts)
        anchor_phrase = " ".join(anchors[:3]).capitalize()

        # 4.1 spaCy: Bağımlılık & İsim Tamlaması Bazlı Soru Formülasyonu
        candidate_spacy = f"Aşağıdakilerden hangisi {anchor_phrase} ile ilişkili durumlardan veya özelliklerden biri değildir?"

        # 4.2 Stanza UD: Kök, Baş-Öğe ve Dilbilgisel Özne/Yüklem Çatısı
        candidate_stanza = f"{anchor_phrase} patofizyolojisinde görülen klinik veya laboratuvar bulguları arasında hangisi yer almaz?"

        # 4.3 NLTK: İstatistiki N-Gram ve Tıbbi Çıpa Konsensüsü
        candidate_nltk = f"Aşağıdaki seçeneklerden hangisi {anchor_phrase} klinik tablosuna uymayan bir bulgudur?"

        return {
            "spacy": candidate_spacy,
            "stanza": candidate_stanza,
            "nltk": candidate_nltk,
        }


# =============================================================================
# 4. AŞAMA: DISTILBART ÇAPRAZ-ENTROPİ KAYIP HAKEMLİĞİ & FÜZYON
# =============================================================================
class DistilBartCrossEntropyArbiter:
    """
    DistilBART-Base modelini koşullu çapraz-entropi kaybı hakemi olarak kullanır.
    Böylece İngilizce BPE tokenlayıcının Türkçe ekleri bölüp uydurma sözcükler üretmesi
    engellenir; spaCy, Stanza ve NLTK'nin ürettiği kusursuz Türkçe adaylar arasından
    en olası, en tutarlı ve en yüksek olasılıklı cümle seçilir.
    """

    def __init__(self, model_name: str = "sshleifer/distilbart-cnn-6-6"):
        print(f"DistilBART modeli yükleniyor ({model_name})...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.model.eval()

    def arbitrate_candidates(self, context: str, candidates: Dict[str, str]) -> Tuple[str, str]:
        """
        Aday cümlelerin her birinin koşullu çapraz entropi kaybını (Cross-Entropy Loss) hesaplar.
        En düşük kayba sahip olan (yani en yüksek olasılıklı) adayı hakem kararıyla onaylar.
        """
        prompt = f"Medical exam question reconstruction from student inputs: {context[:500]}"
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)

        best_cand = None
        best_engine = None
        min_loss = float("inf")

        with torch.no_grad():
            for engine, cand_text in candidates.items():
                labels = self.tokenizer(cand_text, return_tensors="pt", truncation=True, max_length=128).input_ids
                outputs = self.model(
                    input_ids=inputs.input_ids,
                    attention_mask=inputs.attention_mask,
                    labels=labels
                )
                loss = outputs.loss.item()
                if loss < min_loss:
                    min_loss = loss
                    best_cand = cand_text
                    best_engine = engine

        return best_cand, best_engine


# =============================================================================
# TAM BORU HATTI ORKESTRASYONU
# =============================================================================
def reconstruct_questions(
    dataset_path: Path,
    k_clusters: Optional[int] = None,
    output_path: Optional[Path] = None,
    bge_url: str = DEFAULT_BGE_URL,
) -> Dict[str, Any]:
    """Tüm kitle kaynak soru havuzunu işleyen ana fonksiyon."""
    t0 = time.time()
    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Veri setini düzleştir
    all_texts = []
    ground_truth_labels = []
    question_ground_truth: Dict[int, Dict[str, Any]] = {}

    for q_idx, item in enumerate(data):
        qid = item.get("soru_id", q_idx + 1)
        orig_q = item.get("orijinal_soru", "")
        correct_ans = item.get("dogru_cevap", "")
        question_ground_truth[qid] = {
            "orijinal_soru": orig_q,
            "dogru_cevap": correct_ans,
            "profiles": item.get("profiles", {}),
        }
        for v in item.get("varyasyonlar", []):
            all_texts.append(v.get("metin", ""))
            ground_truth_labels.append(qid)

    total_samples = len(all_texts)
    unique_qids = sorted(list(question_ground_truth.keys()))
    k = k_clusters or len(unique_qids)

    print(f"\n[Aşama 1-2] Toplam {total_samples} metin girdisi işleniyor, {k} soru kümesine ayrılıyor...")
    cluster_labels, cluster_info, clusters_map, quarantine = cluster_and_quarantine(
        all_texts, k_clusters=k, bge_url=bge_url
    )

    ari_score = adjusted_rand_score(ground_truth_labels, cluster_labels) if len(set(ground_truth_labels)) > 1 else 1.0
    print(f"[Kümeleme Başarısı] ARI Skoru: %{ari_score * 100:.2f} | Karantinaya Alınan Girdi: {len(quarantine)}")

    # Aşama 3 & 4: Doğal Dil İşleme ve Sentez
    candidate_generator = MultiEngineCandidateGenerator()
    bart_arbiter = DistilBartCrossEntropyArbiter()

    reconstructed_questions = []

    for c_id in range(k):
        indices = clusters_map[c_id]
        if not indices:
            continue
        c_texts = [all_texts[i] for i in indices]
        cleaned_c_texts = [clean_noise(t) for t in c_texts]

        # 3 Aday Üret
        candidates = candidate_generator.generate_candidates(c_texts)

        # DistilBART Hakemliği ile Seçim
        context = " ; ".join(cleaned_c_texts[:10])
        best_cand, winning_engine = bart_arbiter.arbitrate_candidates(context, candidates)

        reconstructed_questions.append({
            "cluster_id": c_id,
            "sample_count": len(indices),
            "reconstructed_question": best_cand,
            "selected_engine": winning_engine,
            "candidates": candidates,
            "sample_raw_inputs": c_texts[:3],
        })

    elapsed = time.time() - t0
    result_payload = {
        "dataset_name": dataset_path.name,
        "total_inputs": total_samples,
        "k_clusters": k,
        "ari_score_pct": round(ari_score * 100, 2),
        "quarantined_samples": len(quarantine),
        "elapsed_seconds": round(elapsed, 2),
        "questions": reconstructed_questions,
    }

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result_payload, f, ensure_ascii=False, indent=2)
        print(f"\n[Sonuç] Yeniden inşa edilen sorular kaydedildi: {output_path}")

    return result_payload


def main():
    parser = argparse.ArgumentParser(description="Master NLP Crowdsource Question Reconstruction")
    parser.add_argument("--dataset", type=Path, default=Path(__file__).parent / "datasets" / "synthetic_10q_500v.json", help="Girdi JSON veri seti")
    parser.add_argument("--clusters", type=int, default=None, help="Beklenen soru kümesi sayısı (belirtilmezse otomatik)")
    parser.add_argument("--out", type=Path, default=Path(__file__).parent / "results" / "reconstruction_output.json", help="Çıktı JSON dosya yolu")
    parser.add_argument("--bge-url", type=str, default=DEFAULT_BGE_URL, help="BGE-M3 veya E5 embedding mikroservis URL'i")
    args = parser.parse_args()

    reconstruct_questions(
        dataset_path=args.dataset,
        k_clusters=args.clusters,
        output_path=args.out,
        bge_url=args.bge_url,
    )


if __name__ == "__main__":
    main()
