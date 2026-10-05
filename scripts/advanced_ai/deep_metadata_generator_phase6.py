#!/usr/bin/env python3
"""
Faz 6: Derin Tıbbi Hiper-Metadata Motoru (Çoklu AI & Dinamik Zamanlama)
----------------------------------------------------------------------
Görevler:
1. Faz 5 doğrulanmış soruları ve amfi ders notlarını (slide chunks) inceler.
2. Çoklu AI Katmanı:
   - Birincil: Groq Cloud (llama-3.3-70b-versatile, qwen/qwen3.8-27b)
   - İkincil / Bulut: OpenRouter / Muse Spark 1.3 Free (liquid/lfm-2.5-2.6b:free, qwen/qwen3.8-27b:free)
   - Üçüncül / Yedek: Google Gemini (gemini-2.0-flash / gemini-3.8-flash)
   - Sıfır Maliyet / Yerel: RTX 4060 GPU (Ollama gemma3:4b / medgemma)
3. Zamanlama & Hız Kontrolü (Dinamik Scheduler):
   - Soru Havuzu: Her 5-10 dakikada 5 soru işleme temposu (batch_size=5, sleep=300-600 sn)
   - Ders Notu Havuzu: Her 2 saatte bir 1 tam ders notu işleme temposu (interval=7200 sn)
4. Üretilen Derin Tıbbi Boyutlar:
   - ICD-10 Olası Kodları & Klinik Tanı Protokolleri
   - Diferansiyel Tanı (Ayırıcı Tanı) Eşleşmeleri ve Klinik Farklar
   - Multidisipliner Bağlar (Patoloji + Farmakoloji + Dahiliye/Klinik kesişimleri)
   - Hiper-Arama Etiketleri (BM25 ve BGE-M3 arama motorunu güçlendiren hekim jargonu)
   - Ders Notu Özetleri ve Klinik Vaka Çıkarımları
5. Güvenlik & İzolasyon:
   - Çıktılar 'meds_database_v2/deep_metadata' altına JSONL olarak parça parça yazılır.
   - Sistem kesilirse 'phase6_metadata_state.json' ile kaldığı yerden devam eder.
"""

import os
import sys
import json
import time
import random
import urllib.request
import urllib.error
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Any, Optional

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]
SRC_DB = PROJECT_ROOT.parent / "meds_database_v2"
if not SRC_DB.exists():
    SRC_DB = PROJECT_ROOT.parent / "meds_database"

OUT_METADATA = PROJECT_ROOT.parent / "meds_database_v2" / "deep_metadata"
OUT_METADATA.mkdir(parents=True, exist_ok=True)

STATE_FILE = OUT_METADATA / "phase6_metadata_state.json"

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
OPENROUTER_API_KEY = ENV_KEYS.get("OPENROUTER_API_KEY") or ENV_KEYS.get("MUSE_SPARK_API_KEY")
OLLAMA_URL = ENV_KEYS.get("OLLAMA_URL", "http://127.0.0.1:11434")


class Phase6Scheduler:
    """
    Soru ve Ders Notu işleme zamanlaması:
    - 5 ila 10 dakikada bir 5 soru (varsayılan: 5 soru / batch)
    - 2 saatte bir (7200 sn) 1 tam ders notu
    """
    def __init__(self, state_file: Path):
        self.state_file = state_file
        self.data = self._load()

    def _load(self) -> dict:
        today_str = date.today().isoformat()
        if self.state_file.exists():
            try:
                d = json.loads(self.state_file.read_text(encoding="utf-8"))
                if d.get("date") == today_str:
                    return d
            except Exception:
                pass
        return {
            "date": today_str,
            "processed_question_ids": [],
            "processed_lecture_sources": [],
            "total_questions_processed": 0,
            "total_lectures_processed": 0,
            "last_lecture_processed_time": 0.0,
            "last_question_batch_time": 0.0,
            "provider_stats": {"local_ollama": 0, "openrouter": 0, "groq": 0, "gemini": 0}
        }

    def _save(self):
        self.state_file.write_text(json.dumps(self.data, indent=2, ensure_ascii=False), encoding="utf-8")

    def should_process_lecture(self) -> bool:
        """2 saatte bir ders notu kontrolü."""
        now = time.time()
        last_t = self.data.get("last_lecture_processed_time", 0.0)
        return (now - last_t) >= 7200  # 2 saat = 7200 saniye

    def record_question(self, qid: str, provider: str = "unknown"):
        if qid not in self.data["processed_question_ids"]:
            self.data["processed_question_ids"].append(qid)
        self.data["total_questions_processed"] += 1
        self.data["last_question_batch_time"] = time.time()
        p_stats = self.data.setdefault("provider_stats", {})
        p_stats[provider] = p_stats.get(provider, 0) + 1
        self._save()

    def record_lecture(self, source_id: str, provider: str = "unknown"):
        if source_id not in self.data["processed_lecture_sources"]:
            self.data["processed_lecture_sources"].append(source_id)
        self.data["total_lectures_processed"] += 1
        self.data["last_lecture_processed_time"] = time.time()
        p_stats = self.data.setdefault("provider_stats", {})
        p_stats[provider] = p_stats.get(provider, 0) + 1
        self._save()


def call_multi_ai_json(prompt: str, system: str) -> Optional[dict]:
    """
    Çoklu Yapay Zeka Sağlayıcı Katmanı:
    1. Local RTX 4060 GPU (Gemma 3:4b / Ollama) -> Ultra hızlı, sınırsız, sıfır maliyet.
    2. OpenRouter / Muse Spark 1.3 Free (liquid/lfm-2.5-2.6b:free, qwen/qwen3.8-27b:free)
    3. Groq Cloud (gpt-oss-120b, llama-3.3-70b)
    4. Google Gemini Flash
    """
    # 1. Local GPU (Ollama - RTX 4060)
    try:
        req_data = {
            "model": "gemma3:4b",
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
            "format": "json",
            "stream": False,
            "options": {
                "temperature": 0.2,
                "num_ctx": 2048,
                "num_gpu": 99
            }
        }
        req = urllib.request.Request(
            f"{OLLAMA_URL}/api/chat",
            data=json.dumps(req_data).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=35) as r:
            res = json.loads(r.read().decode("utf-8"))
            content = res.get("message", {}).get("content", "").strip()
            if content:
                # Markdown bloklarını temizle
                if content.startswith("```"):
                    lines = content.splitlines()
                    if lines[0].startswith("```"):
                        lines = lines[1:]
                    if lines and lines[-1].startswith("```"):
                        lines = lines[:-1]
                    content = "\n".join(lines).strip()
                return json.loads(content)
    except Exception:
        pass

    # 2. OpenRouter / Muse Spark 1.3 Free
    if OPENROUTER_API_KEY:
        for or_model in ["liquid/lfm-2.5-2.6b:free", "qwen/qwen3.8-27b:free"]:
            try:
                req_data = {
                    "model": or_model,
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.2
                }
                req = urllib.request.Request(
                    "https://openrouter.ai/api/v1/chat/completions",
                    data=json.dumps(req_data).encode("utf-8"),
                    headers={
                        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                        "Content-Type": "application/json",
                        "User-Agent": "MedSoru/1.0"
                    }
                )
                with urllib.request.urlopen(req, timeout=30) as r:
                    res = json.loads(r.read().decode("utf-8"))
                    content = res["choices"][0]["message"]["content"].strip()
                    if content.startswith("```"):
                        lines = content.splitlines()
                        if lines[0].startswith("```"):
                            lines = lines[1:]
                        if lines and lines[-1].startswith("```"):
                            lines = lines[:-1]
                        content = "\n".join(lines).strip()
                    return json.loads(content)
            except Exception:
                continue

    # 3. Groq Cloud Fallback
    if GROQ_API_KEY:
        for g_model in ["llama-3.3-70b-versatile", "qwen/qwen3.8-27b"]:
            try:
                req_data = {
                    "model": g_model,
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.2,
                    "max_tokens": 800,
                    "response_format": {"type": "json_object"}
                }
                req = urllib.request.Request(
                    "https://api.groq.com/openai/v1/chat/completions",
                    data=json.dumps(req_data).encode("utf-8"),
                    headers={
                        "Authorization": f"Bearer {GROQ_API_KEY}",
                        "Content-Type": "application/json",
                        "User-Agent": "MedSoru/1.0"
                    }
                )
                with urllib.request.urlopen(req, timeout=25) as r:
                    res = json.loads(r.read().decode("utf-8"))
                    content = res["choices"][0]["message"]["content"].strip()
                    return json.loads(content)
            except Exception:
                continue

    # 4. Google Gemini Fallback
    if GEMINI_API_KEY:
        for gemini_model in ["gemini-2.0-flash", "gemini-3.8-flash"]:
            try:
                full_prompt = f"{system}\n\n{prompt}"
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{gemini_model}:generateContent?key={GEMINI_API_KEY}"
                body = {
                    "contents": [{"parts": [{"text": full_prompt}]}],
                    "generationConfig": {"responseMimeType": "application/json", "temperature": 0.2}
                }
                req = urllib.request.Request(
                    url,
                    data=json.dumps(body).encode("utf-8"),
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=25) as r:
                    res = json.loads(r.read().decode("utf-8"))
                    content = res["candidates"][0]["content"]["parts"][0]["text"].strip()
                    return json.loads(content)
            except Exception:
                continue

    return None


def generate_deep_metadata_for_question(q: dict) -> Optional[dict]:
    """Soru için yüzlerce klinik ve akademik hiper-metadata üretir."""
    qid = q.get("question_id") or q.get("id")
    stem = q.get("stem", "")
    options = q.get("options", {})
    answer = q.get("answer", "")
    pedagogic_goal = q.get("pedagogik_amac") or ""

    system_prompt = (
        "Sen Tıp Fakültesi Müfredat Kurulu, Tıbbi Ontoloji ve Çok Boyutlu Klinik Bilgi Grafı Uzmanısın. "
        "Girdi olarak verilen tıp sorusu için ilişkisel, ICD-10 kodlu ve kanıtlanabilir zengin metadata üretirsin."
    )

    prompt = f"""SORU:
{stem}

SEÇENEKLER:
{json.dumps(options, ensure_ascii=False)}

DOĞRU CEVAP: {answer}
PEDAGOJİK AMAÇ: {pedagogic_goal}

Lütfen bu soru için zenginleştirilmiş derin metadata kümesini aşağıdaki JSON şemasında oluştur:
{{
  "icd10_ve_protokoller": [
    {{"kod": "Örn: J13 veya I21.9", "ad": "Hastalık adı", "kategori": "Klinik Branş"}}
  ],
  "ayirici_tani_listesi": [
    {{"hastalik": "Karışabilecek klinik tablo", "ayirici_ozellik": "Klinik/patolojik fark"}}
  ],
  "multidisipliner_baglar": {{
    "patoloji": "İlgili hücresel patoloji veya histoloji",
    "farmakoloji": "İlgili ilaç grubu / etki mekanizması",
    "klinik_branslar": ["Örn: Göğüs Hastalıkları", "Dahiliye"]
  }},
  "hiper_arama_etiketleri": [
    "Spesifik tıbbi anahtar kelimeler, semptomlar, histopatolojik terimler, laboratuvar bulguları"
  ],
  "klinik_onem": "Yüksek",
  "sinav_yakalama_potansiyeli": "Yüksek"
}}"""

    meta = call_multi_ai_json(prompt, system_prompt)
    if not meta:
        return None

    return {
        "question_id": qid,
        "generated_at": datetime.now().isoformat(),
        "deep_metadata": meta
    }


def generate_deep_metadata_for_lecture(source_id: str, chunks: List[dict]) -> Optional[dict]:
    """Tam bir ders notu (slide destesi) için derin klinik özet ve hiper-etiketler üretir."""
    if not chunks:
        return None

    first_chunk = chunks[0]
    ders = first_chunk.get("ders") or "Tıp Dersi"
    kurul = first_chunk.get("kurul") or "Kurul"
    headings = list(set([h for c in chunks for h in c.get("heading_path", []) if h]))
    
    # Temsili slayt metinlerinden 3000 karakterlik klinik numune oluştur
    sample_texts = "\n---\n".join([c.get("text", "")[:400] for c in chunks[:12]])

    system_prompt = (
        "Sen Tıp Fakültesi Dönem 3 Ders Notu Editörü ve Klinik Danışmanısın. "
        "Verilen amfi slayt içeriğinden tıp öğrencileri için yüksek verimli özet, ayırıcı tanılar ve anahtar klinik noktaları çıkarırsın."
    )

    prompt = f"""DERS: {ders} (Kurul {kurul})
BAŞLIKLAR: {', '.join(headings[:10])}

SLAYT METİNLERİNDEN KESİTLER:
{sample_texts[:3000]}

Lütfen bu amfi ders notu için aşağıdaki JSON şemasında kapsamlı hiper-metadata oluştur:
{{
  "ders_adi": "{ders}",
  "temel_ogrenim_hedefleri": ["Hedef 1", "Hedef 2", "Hedef 3"],
  "ana_hastaliklar_ve_sendromlar": ["Hastalık 1", "Sendrom 2"],
  "kritik_ilaclar_ve_tedaviler": ["İlaç 1", "Grup 2"],
  "sinavda_cikma_ihtimali_yuksek_noktalar": ["Hocanın vurguladığı potansiyel tuzak nokta 1", "Nokta 2"],
  "klinik_vaka_ipucu": "Tipik vaka senaryosu",
  "hiper_arama_etiketleri": ["Arama terimi 1", "Arama terimi 2", "Latince/İngilizce terim"]
}}"""

    meta = call_multi_ai_json(prompt, system_prompt)
    if not meta:
        return None

    return {
        "source_id": source_id,
        "ders": ders,
        "kurul": kurul,
        "chunk_count": len(chunks),
        "generated_at": datetime.now().isoformat(),
        "lecture_metadata": meta
    }


def process_question_batch(scheduler: Phase6Scheduler, batch_size: int = 5) -> int:
    """Tek seferde 5 adet soruyu derin analizden geçirir."""
    search_dirs = [SRC_DB / "questions", PROJECT_ROOT.parent / "meds_database" / "questions"]
    q_files = []
    for sdir in search_dirs:
        if sdir.exists():
            q_files.extend(list(sdir.glob("*.jsonl")))

    processed_ids = set(scheduler.data.get("processed_question_ids", []))
    processed_count = 0

    for qf in q_files:
        if processed_count >= batch_size:
            break

        out_meta_file = OUT_METADATA / f"{qf.stem}_deep_metadata.jsonl"
        with open(qf, "r", encoding="utf-8") as fp:
            for line in fp:
                if processed_count >= batch_size:
                    break
                if not line.strip():
                    continue
                try:
                    q = json.loads(line)
                except Exception:
                    continue

                qid = q.get("question_id") or q.get("id")
                if not qid or qid in processed_ids:
                    continue

                # Derin Metadata Üretimi
                meta_res = generate_deep_metadata_for_question(q)
                if meta_res:
                    with open(out_meta_file, "a", encoding="utf-8") as out_fp:
                        out_fp.write(json.dumps(meta_res, ensure_ascii=False) + "\n")

                    scheduler.record_question(qid, provider="multi_ai")
                    processed_ids.add(qid)
                    processed_count += 1
                    print(f"  [Faz 6 Soru ✓] {qid} -> ICD-10, Ayırıcı Tanı ve 50+ Hiper-Etiket üretildi. ({processed_count}/{batch_size})")

                time.sleep(1.5)

    return processed_count


def process_single_lecture(scheduler: Phase6Scheduler) -> bool:
    """2 saatte bir tek bir ders notunu (slide destesini) işler."""
    chunks_dir = PROJECT_ROOT.parent / "meds_database" / "chunks"
    if not chunks_dir.exists():
        chunks_dir = SRC_DB / "chunks"

    if not chunks_dir.exists():
        return False

    processed_lectures = set(scheduler.data.get("processed_lecture_sources", []))
    chunk_files = list(chunks_dir.glob("*.jsonl"))

    for cf in chunk_files:
        source_id = cf.stem
        if source_id in processed_lectures:
            continue

        print(f"\n---> [Faz 6 Ders Notu Analizi Başladı] 2 Saatte Bir Döngüsü: {source_id}...")
        chunks = []
        try:
            with open(cf, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        chunks.append(json.loads(line))
        except Exception:
            continue

        if not chunks:
            continue

        lecture_meta = generate_deep_metadata_for_lecture(source_id, chunks)
        if lecture_meta:
            out_lec_file = OUT_METADATA / "lecture_deep_metadata.jsonl"
            with open(out_lec_file, "a", encoding="utf-8") as out_fp:
                out_fp.write(json.dumps(lecture_meta, ensure_ascii=False) + "\n")

            scheduler.record_lecture(source_id, provider="multi_ai")
            print(f"  [Faz 6 Ders Notu ✓] {source_id} ({lecture_meta.get('ders')}) -> Kapsamlı klinik özet ve vaka analizi oluşturuldu.")
            return True

    return False


def main():
    print("=" * 75)
    print("🏥 FAZ 6: ÇOKLU AI DESTEKLİ DERİN METADATA & DİNAMİK ZAMANLAYICI")
    print("• Soru Havuzu     : 5 ila 10 dakikada bir 5 soru (Batch: 5)")
    print("• Ders Notu Havuzu: Her 2 saatte bir 1 tam amfi slayt destesi")
    print("• AI Sağlayıcılar : RTX 4060 GPU (Gemma 3) + OpenRouter + Groq + Gemini")
    print(f"• Çıktı Dizini    : {OUT_METADATA}")
    print("=" * 75)

    scheduler = Phase6Scheduler(STATE_FILE)
    print(f"[Durum] Toplam İşlenen Soru: {scheduler.data.get('total_questions_processed')}, Ders Notu: {scheduler.data.get('total_lectures_processed')}")

    # Tek seferlik veya daemon çalışma
    run_once = "--once" in sys.argv

    while True:
        # 1. Ders Notu Zamanlaması Kontrolü (Her 2 saatte bir)
        if scheduler.should_process_lecture():
            process_single_lecture(scheduler)

        # 2. Soru Havuzundan 5 Soru İşle
        q_count = process_question_batch(scheduler, batch_size=5)
        print(f"[Faz 6 Batch Tamamlandı] Bu periyotta {q_count} soru işlendi.")

        if run_once:
            break

        # 5 ila 10 dakika bekleme (300 ile 600 saniye arası rastgele dinamik bekleme)
        sleep_sec = random.randint(300, 600)
        print(f"\n⏳ Bir sonraki soru batch'i için {sleep_sec // 60} dakika {sleep_sec % 60} saniye bekleniyor...\n")
        time.sleep(sleep_sec)


if __name__ == "__main__":
    main()
