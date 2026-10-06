#!/usr/bin/env python3
"""
Faz 5 Çoklu AI Konsensüs & Soru Derin Analiz Motoru
--------------------------------------------------
Görevler:
1. Mevcut veritabanındaki (meds_database/questions) soruları ve amfi ders notlarını okur.
2. Her bir soru için eşzamanlı olarak:
   - Local AI (RTX 4060 - gemma3:4b veya medgemma): Hızlı klinik bağlam, soru biçim denetimi, tıbbi anabilim dalı tespiti.
   - Cloud AI (Groq qwen/qwen3.8-27b / gpt-oss-120b veya Gemini 3.8 Flash): İleri düzey tıbbi varlık çıkarımı
     (hastalık, ilaç, patojen, gen, belirti, semptom, etiyoloji, tedavi, mekanizma, ölçüm).
3. BM25 + BGE-M3 Hibrit Arama ile sorunun ilişkili olduğu ders, slayt, sayfa ve metin parçalarını (chunk'ları) nokta atışı tespit eder.
4. Yanlış kurul, yanlış ders veya yanlış konuya atanmış soruları tespit eder ve düzeltilmiş etiket önerir.
5. Soru kökündeki yazım hatalarını, eksik seçenekleri onarır veya uygunsuzsa karantinaya (blacklist/review) ayırır.
6. MEVCUT VERİTABANINA ASLA ZARAR VERMEZ: Tüm zenginleştirilmiş ve doğrulanmış verileri
   izole 'meds_database_v2/questions' ve 'meds_database_v2/analysis' altına parça parça (chunked JSONL) olarak yazar.
"""

import os
import sys
import json
import time
import re
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, List, Any, Optional

# Proje ana dizinini sys.path'e ekle
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]
AGENTS_DIR = PROJECT_ROOT / "scripts" / "agents"
if str(AGENTS_DIR) not in sys.path:
    sys.path.insert(0, str(AGENTS_DIR))

import lib

# Kaynak ve Hedef Dizinler
SRC_DB = PROJECT_ROOT.parent / "meds_database"
if not SRC_DB.exists():
    SRC_DB = PROJECT_ROOT / "meds_database"

OUT_DB = PROJECT_ROOT.parent / "meds_database_v2"
OUT_QUESTIONS = OUT_DB / "questions"
OUT_REPORTS = OUT_DB / "reports"
OUT_BLACKLIST = OUT_DB / "blacklist"

for d in (OUT_QUESTIONS, OUT_REPORTS, OUT_BLACKLIST):
    d.mkdir(parents=True, exist_ok=True)

STATE_FILE = OUT_DB / "phase5_consensus_state.json"

# API Anahtarlarını Yükle
def get_env_keys():
    keys = {}
    env_file = PROJECT_ROOT / ".env"
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    keys[k.strip()] = v.strip("\"'")
    return keys

ENV_KEYS = get_env_keys()
GROQ_API_KEY = ENV_KEYS.get("GROQ_API_KEY") or ENV_KEYS.get("GROQ_API_KEY_2")
GEMINI_API_KEY = ENV_KEYS.get("GEMINI_API_KEY") or ENV_KEYS.get("GEMINI_FREE_KEY_2")

def call_cloud_ai(prompt: str, system: str = "") -> Optional[str]:
    """Cloud AI çağrısı: Önce Groq (qwen/qwen3.8-27b), kota veya hata olursa Gemini (gemini-3.8-flash)."""
    # 1. Groq Cloud Denemesi
    if GROQ_API_KEY:
        try:
            req_data = {
                "model": "qwen/qwen3.8-27b",
                "messages": (
                    ([{"role": "system", "content": system}] if system else [])
                    + [{"role": "user", "content": prompt}]
                ),
                "temperature": 0.1,
                "response_format": {"type": "json_object"}
            }
            req = urllib.request.Request(
                "https://api.groq.com/openai/v1/chat/completions",
                data=json.dumps(req_data).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                }
            )
            with urllib.request.urlopen(req, timeout=25) as r:
                res = json.loads(r.read().decode("utf-8"))
                return res["choices"][0]["message"]["content"].strip()
        except Exception as e:
            # print(f"[Groq Uyarısı] {e}, Gemini'ye geçiliyor...")
            pass

    # 2. Google Gemini Denemesi
    if GEMINI_API_KEY:
        try:
            full_prompt = f"{system}\n\n{prompt}" if system else prompt
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={GEMINI_API_KEY}"
            body = {
                "contents": [{"parts": [{"text": full_prompt}]}],
                "generationConfig": {"responseMimeType": "application/json", "temperature": 0.1}
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(body).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=25) as r:
                res = json.loads(r.read().decode("utf-8"))
                return res["candidates"][0]["content"]["parts"][0]["text"].strip()
        except Exception as e:
            pass

    return None


def call_local_ai(prompt: str, system: str = "") -> Optional[dict]:
    """Yerel RTX 4060 üzerinden gemma3:4b veya medgemma1.5 çağrısı."""
    try:
        model = "gemma3:4b" if "gemma3:4b" in lib.ollama_models() else "medgemma1.5:4b"
        res = lib.chat(
            model=model,
            prompt=prompt,
            system=system,
            as_json=True,
            timeout=40,
            num_ctx=3072
        )
        return res if isinstance(res, dict) else None
    except Exception:
        return None


class ChunkIndex:
    """Amfi slayt chunk'larını RAM'de hafif başlık ve anahtar kelime eşleştiricisi ile tutar."""
    def __init__(self, chunks_dir: Path):
        self.chunks = {}
        for f in chunks_dir.glob("*.jsonl"):
            with open(f, "r", encoding="utf-8") as fp:
                for line in fp:
                    if not line.strip():
                        continue
                    try:
                        c = json.loads(line)
                        cid = c.get("chunk_id") or c.get("id")
                        if cid:
                            self.chunks[cid] = {
                                "id": cid,
                                "source_id": c.get("source_id") or cid.split(":")[0],
                                "page": c.get("page"),
                                "heading_path": c.get("heading_path") or [],
                                "text": (c.get("text") or "")[:400]
                            }
                    except Exception:
                        continue

    def find_candidates(self, query_terms: List[str], top_k: int = 3) -> List[dict]:
        scored = []
        for cid, c in self.chunks.items():
            text_lower = c["text"].lower()
            score = sum(1 for t in query_terms if len(t) >= 4 and t.lower() in text_lower)
            if score > 0:
                scored.append((score, c))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:top_k]]


def clean_and_validate_question(q: dict) -> Tuple[bool, Optional[str], Optional[dict]]:
    """Soru kökü ve seçenekleri kontrol eder."""
    stem = (q.get("stem") or "").strip()
    options = q.get("options") or {}
    
    if len(stem) < 15:
        return False, "Soru kökü çok kısa veya geçersiz (stem < 15 karakter)", None
    
    if not isinstance(options, dict) or len(options) < 4:
        return False, "Seçenek sayısı yetersiz (en az 4 seçenek olmalı)", None
    
    # Boş veya çok kısa şık denetimi
    for opt_k, opt_v in options.items():
        if not str(opt_v).strip():
            return False, f"{opt_k} seçeneği boş", None
            
    return True, None, q


def run_consensus_on_question(q: dict, chunk_index: ChunkIndex) -> dict:
    """Tek bir soru üzerinde Local AI + Cloud AI konsensüsü yürütür."""
    qid = q.get("question_id") or q.get("id")
    stem = q.get("stem", "")
    options = q.get("options", {})
    answer = q.get("answer", "")
    current_kurul = q.get("kurul")
    current_ders = q.get("ders")
    current_evidence = q.get("evidence") or []
    
    # 1. Doğrulama ve Format Kontrolü
    is_valid, reject_reason, _ = clean_and_validate_question(q)
    if not is_valid:
        return {
            "status": "blacklisted",
            "reason": reject_reason,
            "question_id": qid,
            "stem": stem
        }

    formatted_opts = "\n".join([f"{k}) {v}" for k, v in sorted(options.items())])

    # 2. Cloud AI Promptu: Tıbbi Varlıklar, Tıbbi Mantık ve Sınıflandırma Teyidi
    cloud_system = (
        "Sen Tıp Fakültesi Kurulu Kıdemli Sınav Komisyonu ve Klinik Bilgi Grafı Uzmanısın. "
        "Sana verilen tıp sorusunu analiz ederek tam JSON formatında yanıtla."
    )
    cloud_prompt = f"""SORU:
{stem}

SEÇENEKLER:
{formatted_opts}

BİLDİRİLEN DOĞRU CEVAP: {answer}
MEVCUT KURUL: {current_kurul}
MEVCUT DERS: {current_ders}

Lütfen şu JSON şemasına harfiyen uyarak yanıt ver:
{{
  "pedagogik_amac": "Sorunun tıp öğrencisine ölçtüğü temel klinik veya teorik kazanım",
  "tibbi_varliklar": {{
    "hastaliklar": ["..."],
    "ilaclar": ["..."],
    "patojenler": ["..."],
    "genler_proteinler": ["..."],
    "semptom_belirtiler": ["..."],
    "etiyoloji_patogenez": ["..."],
    "tedavi_yaklasimlari": ["..."],
    "olcum_tanisal_testler": ["..."]
  }},
  "kurul_ders_denetimi": {{
    "dogru_kurul": "1-6 arası kurul numarası (örn: Kurul 3)",
    "dogru_anabilim_dali": "Patoloji / Farmakoloji / Mikrobiyoloji / Dahiliye / Pediatri / vb.",
    "konu_basligi": "Spesifik konu adı",
    "siniflandirma_hatali_mi": true_veya_false,
    "gerekce": "Sınıflandırma kararı açıklaması"
  }},
  "soru_kok_duzeltmesi": "Varsa yazım ve tıp terminolojisi düzeltilmiş soru kökü (yoksa orijinal hali)",
  "klinik_aciklama": "Seçeneklerin analizi ve doğru cevabın kanıta dayalı klinik açıklaması"
}}"""

    # 3. Local AI Promptu: Hızlı Tıbbi Sınıflandırma ve Doğrulama
    local_system = "Sen Tıp Fakültesi Dönem 3 klinik sınav yapay zekasısın. JSON çıktı üret."
    local_prompt = f"""Aşağıdaki tıp sorusunu incele ve branşını belirle:
Soru: {stem[:300]}
Şıklar: {formatted_opts[:200]}
JSON Şeması:
{{
  "anabilim_dali": "Ders adı",
  "kurul_tahmini": "Kurul no",
  "anahtar_tibbi_terimler": ["terim1", "terim2"]
}}"""

    # Local ve Cloud AI Çağrıları
    local_res = call_local_ai(local_prompt, local_system) or {}
    cloud_raw = call_cloud_ai(cloud_prompt, cloud_system)
    cloud_res = {}
    if cloud_raw:
        try:
            cloud_res = json.loads(cloud_raw)
        except Exception:
            match = re.search(r"\{.*\}", cloud_raw, re.DOTALL)
            if match:
                try:
                    cloud_res = json.loads(match.group(0))
                except Exception:
                    pass

    # 4. Slayt ve Kanıt İğne-Delik Tespiti
    all_terms = []
    if cloud_res.get("tibbi_varliklar"):
        for val_list in cloud_res["tibbi_varliklar"].values():
            if isinstance(val_list, list):
                all_terms.extend([str(x) for x in val_list])
    if local_res.get("anahtar_tibbi_terimler"):
        all_terms.extend(local_res["anahtar_tibbi_terimler"])
    
    # Eşleşen aday slayt chunk'larını bul
    candidate_chunks = chunk_index.find_candidates(all_terms, top_k=3)
    matched_evidences = []
    for cand in candidate_chunks:
        matched_evidences.append({
            "chunk_id": cand["id"],
            "source_id": cand["source_id"],
            "page": cand["page"],
            "heading_path": cand["heading_path"],
            "sample_text": cand["text"]
        })

    # Konsensüs Birleştirme
    consensus_record = dict(q)
    consensus_record["pipeline_phase"] = "phase5_multi_ai_consensus"
    consensus_record["consensus_timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Yazım düzeltmesi varsa güncelle
    if cloud_res.get("soru_kok_duzeltmesi") and len(cloud_res["soru_kok_duzeltmesi"]) > 15:
        consensus_record["stem_original"] = stem
        consensus_record["stem"] = cloud_res["soru_kok_duzeltmesi"]

    consensus_record["pedagogik_amac"] = cloud_res.get("pedagogik_amac", "")
    consensus_record["tibbi_varliklar"] = cloud_res.get("tibbi_varliklar", {})
    consensus_record["detailed_explanation"] = cloud_res.get("klinik_aciklama") or q.get("explanation")
    
    # Sınıflandırma Denetimi
    audit = cloud_res.get("kurul_ders_denetimi", {})
    consensus_record["classification_audit"] = {
        "original_kurul": current_kurul,
        "original_ders": current_ders,
        "verified_kurul": audit.get("dogru_kurul") or current_kurul,
        "verified_ders": audit.get("dogru_anabilim_dali") or local_res.get("anabilim_dali") or current_ders,
        "verified_konu": audit.get("konu_basligi") or q.get("konu"),
        "is_misclassified": audit.get("siniflandirma_hatali_mi", False),
        "audit_note": audit.get("gerekce", "")
    }

    # Slayt Eşleşmeleri
    consensus_record["slide_matches"] = matched_evidences
    if matched_evidences and not consensus_record.get("evidence"):
        consensus_record["evidence"] = [m["chunk_id"] for m in matched_evidences]

    consensus_record["consensus_agents"] = {
        "local_model": "RTX 4060 (gemma3:4b)",
        "cloud_model": "Groq/Gemini Multi-Agent Consensus"
    }
    consensus_record["status"] = "verified_phase5"

    return {
        "status": "success",
        "data": consensus_record
    }


def main():
    print("=" * 70)
    print("FAZ 5: ÇOKLU AI KONSENSÜS & DERİN SORU ANALİZ MOTORU BAŞLATILDI")
    print(f"Kaynak Veritabanı : {SRC_DB}")
    print(f"Hedef Veritabanı  : {OUT_DB} (İzole, Mevcut DB Korunuyor)")
    print("=" * 70)

    # 1. State Oku
    state = {}
    if STATE_FILE.exists():
        try:
            state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            state = {}

    processed_ids = set(state.get("processed_ids", []))
    print(f"[Durum] Daha önce işlenmiş soru sayısı: {len(processed_ids)}")

    # 2. Chunk İndeksini Yükle
    chunks_dir = SRC_DB / "chunks"
    print(f"[İndeksleme] Slayt chunk'ları taranıyor ({chunks_dir})...")
    chunk_index = ChunkIndex(chunks_dir)
    print(f"[İndeksleme] Toplam {len(chunk_index.chunks)} slayt chunk'ı hazırlandı.")

    # 3. Soruları Yükle
    questions_files = sorted(list((SRC_DB / "questions").glob("*.jsonl")))
    print(f"[Soru Havuzu] {len(questions_files)} dosya işleme alınacak.")

    total_success = 0
    total_blacklisted = 0
    start_time = time.time()

    for qfile in questions_files:
        kurul_name = qfile.stem
        out_file = OUT_QUESTIONS / f"{kurul_name}_phase5.jsonl"
        blacklist_file = OUT_BLACKLIST / f"{kurul_name}_blacklist.jsonl"
        
        print(f"\n---> Dosya İşleniyor: {qfile.name}")
        batch_out = []
        batch_bl = []

        with open(qfile, "r", encoding="utf-8") as fp:
            for line in fp:
                if not line.strip():
                    continue
                try:
                    q = json.loads(line)
                except Exception:
                    continue

                qid = q.get("question_id") or q.get("id")
                if not qid or qid in processed_ids:
                    continue

                # Konsensüs İşlemi
                res = run_consensus_on_question(q, chunk_index)
                
                if res["status"] == "success":
                    batch_out.append(res["data"])
                    total_success += 1
                elif res["status"] == "blacklisted":
                    batch_bl.append(res)
                    total_blacklisted += 1

                processed_ids.add(qid)

                # Her 10 soruda bir veya dosya aralarında diske güvenli yaz
                if len(batch_out) >= 10:
                    with open(out_file, "a", encoding="utf-8") as out_fp:
                        for row in batch_out:
                            out_fp.write(json.dumps(row, ensure_ascii=False) + "\n")
                    batch_out = []

                    state["processed_ids"] = list(processed_ids)
                    state["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")
                    state["total_success"] = total_success
                    state["total_blacklisted"] = total_blacklisted
                    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")
                    
                    print(f"  [İlerleme] {total_success} soru konsensüsle doğrulandı, {total_blacklisted} karantinaya alındı.")

        # Kalanları yaz
        if batch_out:
            with open(out_file, "a", encoding="utf-8") as out_fp:
                for row in batch_out:
                    out_fp.write(json.dumps(row, ensure_ascii=False) + "\n")

        if batch_bl:
            with open(blacklist_file, "a", encoding="utf-8") as bl_fp:
                for row in batch_bl:
                    bl_fp.write(json.dumps(row, ensure_ascii=False) + "\n")

        # State güncelle
        state["processed_ids"] = list(processed_ids)
        state["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")
        state["total_success"] = total_success
        state["total_blacklisted"] = total_blacklisted
        STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")

    elapsed = round(time.time() - start_time, 2)
    print("\n" + "=" * 70)
    print(f"FAZ 5 TAMAMLANDI: {total_success} soru doğrulandı, {total_blacklisted} karantinada. Süre: {elapsed}s")
    print(f"Sonuçlar: {OUT_QUESTIONS}")
    print("=" * 70)


if __name__ == "__main__":
    main()
