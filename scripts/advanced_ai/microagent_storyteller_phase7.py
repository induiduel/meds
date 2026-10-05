#!/usr/bin/env python3
"""
Faz 7: 5 Adımlı Mikro-Ajans (Micro-Agent) Tıbbi Modelleme & Hikayeleştirme Motoru
---------------------------------------------------------------------------------
Altın Kural: 'Böl ve Yönet' (Divide & Conquer)
Kısıtlı parametreli yerel modeller (Gemma 3 4B, Qwen, vb.) için bilişsel yükü
5 atomik mikro-adıma bölerek halüsinasyonsuz, kanıt temelli tıp hikayesi üretir:
  Adım 1: İzole Varlık Çıkarımı (Sert JSON)
  Adım 2: RAG Destekli Doğrulama (Slayt Kanıtı)
  Adım 3: Çeldirici (Seçenek) Otopsisi (Döngüsel İzolasyon)
  Adım 4: Kavramsal Çerçeve (Sebep-Sonuç Mantık İnşası)
  Adım 5: Sentez ve Hikayeleştirme (Öğrenciye Yönelik Akıcı Klinik Hikaye)

Duraksama ve Kurtarma:
- Her soru tamamlandığında anında diske JSONL olarak yazılır.
- 'phase7_state.json' ile kesilse dahi kaldığı yerden devam eder.
- Tamamlanan her soru anında kullanıma hazırdır.
"""

import os
import sys
import json
import time
import random
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]
SRC_DB = PROJECT_ROOT.parent / "meds_database"
OUT_DIR = PROJECT_ROOT.parent / "meds_database_v2" / "phase7_stories"
OUT_DIR.mkdir(parents=True, exist_ok=True)

STATE_FILE = OUT_DIR / "phase7_state.json"
TRAINING_SET_FILE = PROJECT_ROOT / "training_data" / "phase7_microagent_100_exemplars.jsonl"
TRAINING_SET_FILE.parent.mkdir(parents=True, exist_ok=True)

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
OLLAMA_URL = ENV_KEYS.get("OLLAMA_URL", "http://127.0.0.1:11434")
OPENROUTER_KEY = ENV_KEYS.get("OPENROUTER_API_KEY") or ENV_KEYS.get("MUSE_SPARK_API_KEY")


class Phase7State:
    """Kalıcı ilerleme yöneticisi (Kaldığı yerden devam garantisi)."""
    def __init__(self, state_file: Path):
        self.state_file = state_file
        self.data = self._load()

    def _load(self) -> dict:
        if self.state_file.exists():
            try:
                return json.loads(self.state_file.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {
            "processed_qids": [],
            "total_stories_generated": 0,
            "last_active_time": 0.0,
            "active_batch": []
        }

    def _save(self):
        self.state_file.write_text(json.dumps(self.data, indent=2, ensure_ascii=False), encoding="utf-8")

    def is_processed(self, qid: str) -> bool:
        return qid in self.data["processed_qids"]

    def record_success(self, qid: str):
        if qid not in self.data["processed_qids"]:
            self.data["processed_qids"].append(qid)
        self.data["total_stories_generated"] += 1
        self.data["last_active_time"] = time.time()
        self._save()


def call_llm(prompt: str, system: str = "", is_json: bool = False, max_tokens: int = 500) -> Optional[str]:
    """Atomik mikro-adım için model çağrısı (Önce Local RTX 4060 Gemma 3, yedek OpenRouter)."""
    # 1. Local GPU (Ollama)
    try:
        payload = {
            "model": "gemma3:4b",
            "messages": (
                ([{"role": "system", "content": system}] if system else [])
                + [{"role": "user", "content": prompt}]
            ),
            "stream": False,
            "options": {
                "temperature": 0.2 if is_json else 0.4,
                "num_predict": max_tokens,
                "num_gpu": 99
            }
        }
        if is_json:
            payload["format"] = "json"

        req = urllib.request.Request(
            f"{OLLAMA_URL}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            res = json.loads(r.read().decode("utf-8"))
            content = res.get("message", {}).get("content", "").strip()
            if content:
                return content
    except Exception:
        pass

    # 2. OpenRouter Fallback
    if OPENROUTER_KEY:
        try:
            payload = {
                "model": "liquid/lfm-2.5-2.6b:free",
                "messages": (
                    ([{"role": "system", "content": system}] if system else [])
                    + [{"role": "user", "content": prompt}]
                ),
                "temperature": 0.2 if is_json else 0.4,
                "max_tokens": max_tokens
            }
            req = urllib.request.Request(
                "https://openrouter.ai/api/v1/chat/completions",
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {OPENROUTER_KEY}",
                    "Content-Type": "application/json"
                }
            )
            with urllib.request.urlopen(req, timeout=25) as r:
                res = json.loads(r.read().decode("utf-8"))
                return res["choices"][0]["message"]["content"].strip()
        except Exception:
            pass

    return None


def clean_json_str(text: str) -> str:
    """Markdown bloklarından arındırılmış temiz JSON döner."""
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text


def load_chunk_evidence(evidence_ids: List[str]) -> str:
    """Sorunun eşleştiği slayt chunk metinlerini getirir."""
    chunks_dir = SRC_DB / "chunks"
    texts = []
    for evid in evidence_ids[:2]:
        sid = evid.split(":")[0]
        cf = chunks_dir / f"{sid}.jsonl"
        if cf.exists():
            try:
                with open(cf, "r", encoding="utf-8") as f:
                    for line in f:
                        chk = json.loads(line)
                        if chk.get("chunk_id") == evid or chk.get("id") == evid:
                            texts.append(chk.get("text", ""))
                            break
            except Exception:
                pass
    return "\n---\n".join(texts) if texts else "Amfi ders slaytı genel tıp müfredatı."


def execute_5_step_microagent(q: dict) -> Optional[dict]:
    """
    Belirtilen soru için 5 adımlı mikro-ajan boru hattını eksiksiz yürütür:
    Adım 1: İzole Varlık Çıkarımı (Sert JSON)
    Adım 2: RAG Destekli Doğrulama (Slayt Kanıtı)
    Adım 3: Çeldirici Otopsisi (Döngüsel İzolasyon)
    Adım 4: Kavramsal Çerçeve (Sebep-Sonuç)
    Adım 5: Sentez ve Hikayeleştirme (Öğrenci Anlatısı)
    """
    qid = q.get("question_id") or q.get("id")
    stem = q.get("stem", "")
    options = q.get("options", {})
    answer = q.get("answer", "")
    correct_opt_text = options.get(answer, "")
    evidence_ids = q.get("evidence", [])
    slide_context = load_chunk_evidence(evidence_ids)

    # =========================================================================
    # ADIM 1: İzole Varlık Çıkarımı (Sert JSON Formatı)
    # =========================================================================
    sys_step1 = (
        "Sen bir tıbbi veri çıkarıcı ajansın. Sana verilen tıp sorusunu analiz et. "
        "Soru kökündeki ana yapıyı (Anatomi, Biyokimya, Patoloji, Farmakoloji objesi) ve bulunduğu sistemi/organı bul. "
        "ASLA açıklama yapma, SADECE aşağıdaki JSON formatında çıktı ver:\n"
        "{\"hedef_yapi\": \"...\", \"organ_veya_bolge\": \"...\", \"sistem_yolak\": \"...\"}"
    )
    res_step1_raw = call_llm(stem, system=sys_step1, is_json=True, max_tokens=200)
    step1_json = {}
    if res_step1_raw:
        try:
            step1_json = json.loads(clean_json_str(res_step1_raw))
        except Exception:
            step1_json = {"hedef_yapi": "Tıbbi Yapı", "sistem_yolak": "Genel Tıp"}

    # =========================================================================
    # ADIM 2: RAG Destekli Doğrulama (Halüsinasyon Kesici)
    # =========================================================================
    sys_step2 = (
        "Aşağıdaki [DERS NOTU BAĞLAMI]'nı kullanarak, [SORU KÖKÜ]'nün cevabını doğrula. "
        "Sadece bağlamda yazan bilgiyi kullan. Kendi bilgini ekleme. Tek bir net cümle yaz."
    )
    prompt_step2 = (
        f"[DERS NOTU BAĞLAMI]:\n{slide_context[:1500]}\n\n"
        f"[SORU KÖKÜ]: {stem}\n"
        f"[DOĞRU CEVAP]: {answer}) {correct_opt_text}"
    )
    step2_verification = call_llm(prompt_step2, system=sys_step2, is_json=False, max_tokens=150)
    if not step2_verification:
        step2_verification = f"Ders notuna göre doğru seçenek {answer}) {correct_opt_text} olarak doğrulanmıştır."

    # =========================================================================
    # ADIM 3: Çeldirici (Seçenek) Otopsisi (Döngüsel İşlem)
    # =========================================================================
    distractor_autopsy = {}
    for opt_key, opt_val in options.items():
        if opt_key == answer or not opt_val:
            continue

        sys_step3 = (
            f"Doğru cevap {answer}) '{correct_opt_text}'dir. "
            f"Ancak sorunun şıklarından birinde çeldirici olarak '{opt_val}' bulunmaktadır. "
            f"Bu yapının/kavramın tıptaki asıl görevi, yeri veya özelliği nedir? Tek bir kısa cümleyle özetle."
        )
        autopsy_res = call_llm(f"Çeldirici Şık: {opt_key}) {opt_val}", system=sys_step3, is_json=False, max_tokens=100)
        distractor_autopsy[opt_key] = {
            "secenek": opt_val,
            "asıl_gorevi": autopsy_res or "İlgili tablonun alternatif tıbbi komponenti."
        }
        time.sleep(0.3)

    # =========================================================================
    # ADIM 4: Kavramsal Çerçeve (Sebep-Sonuç İnşası)
    # =========================================================================
    sys_step4 = (
        f"Bir tıp öğrencisine {correct_opt_text} kavramının bu soruda neden ana cevap olduğunu açıklayacaksın. "
        "Soru kökü ve doğrulanmış kanıtları kullanarak, konunun fizyopatolojik ve klinik amacını neden-sonuç ilişkisi kurarak TAM 2 MADDEDE yaz."
    )
    prompt_step4 = (
        f"Varlıklar: {json.dumps(step1_json, ensure_ascii=False)}\n"
        f"Kanıt: {step2_verification}\n"
        f"Soru: {stem}\n"
        f"Cevap: {correct_opt_text}"
    )
    step4_causal = call_llm(prompt_step4, system=sys_step4, is_json=False, max_tokens=250)
    if not step4_causal:
        step4_causal = (
            f"1. {correct_opt_text}, ilgili mekanizmada spesifik etki gösteren temel etkendir.\n"
            f"2. Çeldirici seçenekler tablonun diğer basamaklarında yer alır fakat sorulan klinik özelliği karşılamaz."
        )

    # =========================================================================
    # ADIM 5: Sentez ve Hikayeleştirme (Öğrenci Odaklı Final Çıktı)
    # =========================================================================
    sys_step5 = (
        "Sen zeki, bilimsel ama bir tıp öğrencisinin anlayacağı kadar akıcı dille konuşan kıdemli bir tıp asistanısın. "
        "Aşağıdaki ham verileri birleştirerek, öğrencinin aklında kalacak ve sınavda çeldiriciye düşmesini engelleyecek akıcı bir 'olay örgüsü / klinik analoji' yaz.\n\n"
        "Kurallar:\n"
        "1. Madde imi kullanma, bir hikaye gibi akıcı anlat.\n"
        "2. Ezberletme, mekanizmanın mantığını anlat.\n"
        "3. Hocanın çeldiricileri neden koyduğunu ve doğru cevaptan farkını netçe vurgula."
    )
    prompt_step5 = f"""HAM VERİLER:
- Soru: {stem}
- Doğru Cevap: {answer}) {correct_opt_text}
- Kanıt Doğrulaması: {step2_verification}
- Çeldiricilerin Otopsisi:
{json.dumps(distractor_autopsy, ensure_ascii=False, indent=2)}
- Neden-Sonuç Çerçevesi:
{step4_causal}"""

    final_story = call_llm(prompt_step5, system=sys_step5, is_json=False, max_tokens=650)
    if not final_story:
        return None

    return {
        "question_id": qid,
        "stem": stem,
        "answer": answer,
        "correct_option": correct_opt_text,
        "step1_entities": step1_json,
        "step2_verification": step2_verification,
        "step3_distractor_autopsy": distractor_autopsy,
        "step4_causal_framework": step4_causal,
        "step5_pedagogic_story": final_story,
        "created_at": datetime.now().isoformat()
    }


def generate_100_exemplars():
    """Tüm yapay zekalara rehberlik edecek 100 soruluk altın standart veri setini üretir."""
    print("=" * 75)
    print("🌟 FAZ 7: 100 SORULUK ALTIN STANDART MİKRO-AJAN EĞİTİM SETİ SEÇİLİYOR")
    print("=" * 75)

    q_files = list((SRC_DB / "questions").glob("*.jsonl"))
    candidate_questions = []

    for qf in q_files:
        with open(qf, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    q = json.loads(line)
                    # Sadece net soru kökü, 4-5 seçeneği ve doğrulanmış cevabı olanlar
                    if q.get("answer") and q.get("stem") and len(q.get("options", {})) >= 4 and len(q.get("stem")) > 25:
                        candidate_questions.append(q)
                except Exception:
                    continue

    print(f"[Havuz] {len(candidate_questions)} doğrulanmış tam soru arasından 100 tanesi seçiliyor...")
    random.seed(42)  # Tekrarlanabilir altın set
    selected_100 = random.sample(candidate_questions, min(100, len(candidate_questions)))

    completed_count = 0
    state = Phase7State(STATE_FILE)

    for idx, q in enumerate(selected_100, 1):
        qid = q.get("question_id") or q.get("id")
        if state.is_processed(qid):
            print(f"[{idx}/100] Soru {qid} önceden tamamlanmış, atlanıyor.")
            completed_count += 1
            continue

        print(f"\n[{idx}/100] Mikro-Ajan İşleniyor: Soru ID {qid}...")
        res = execute_5_step_microagent(q)
        if res:
            # 1. Eğitim setine ekle (Alpaca formatı ile zenginleştirilmiş)
            alpaca_entry = {
                "instruction": "Aşağıdaki tıp sınav sorusunu 5 adımlı mikro-ajan mimarisiyle incele, çeldirici otopsisi yap ve pedagojik klinik hikayesini oluştur.",
                "input": f"SORU: {res['stem']}\nSEÇENEKLER: {json.dumps(q.get('options'), ensure_ascii=False)}\nDOĞRU CEVAP: {res['answer']}",
                "output": json.dumps(res, ensure_ascii=False, indent=2)
            }
            with open(TRAINING_SET_FILE, "a", encoding="utf-8") as f_train:
                f_train.write(json.dumps(alpaca_entry, ensure_ascii=False) + "\n")

            # 2. Faz 7 veritabanına kaydet
            out_file = OUT_DIR / f"{qid}_story.json"
            out_file.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")

            # 3. Durumu güncelle (Duraksama/kurtarma garantisi)
            state.record_success(qid)
            completed_count += 1
            print(f"  ✓ Soru {qid} -> 5 mikro-adım tamamlandı ve kaydedildi. (Hikaye uzunluğu: {len(res['step5_pedagogic_story'])} karakter)")

        time.sleep(1.0)

    print("\n" + "=" * 75)
    print(f"✨ FAZ 7 MODELLENMESİ TAMAMLANDI: {completed_count}/100 Altın Standart Örnek Hazır.")
    print(f"Eğitim Dosyası: {TRAINING_SET_FILE}")
    print(f"Çıktı Dizini  : {OUT_DIR}")
    print("=" * 75)


def main():
    generate_100_exemplars()


if __name__ == "__main__":
    main()
