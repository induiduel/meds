#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Faz 14: Bulut Tabanlı (Gemini Flash) Çıkmış Soru İyileştirme ve İnceleme Pipeline'ı.

Kullanıcının ilettiği Chunk/Batch mimarisine göre çalışır:
- /v1 üzerinden soruları ve müfredatı çeker.
- Google Gemini (gemini-2.5-flash / gemini-3.8-flash) ile soruyu analiz eder,
  tıbbi literatüre (Robbins, Guyton, Harrison vb.) göre eksik/hatalı kökleri ve açıklamaları düzeltir,
  müfredat ve YZV (Yapay Zeka Verisi) bloğunu üretir.
- Üretilen verileri 'meds_database_v2/phase14_past_question_editor/reviews.jsonl'
  inceleme katmanına ve nofrostlife.com.tr/test/cikmis arayüzüne sunar.
- Opsiyonel --direct-apply bayrağı verilirse X-API-Password ile /api uç noktasına canlı uygular.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path
import urllib.request
import urllib.error

# Dizin tanımları
ROOT = Path(__file__).resolve().parents[2]
AGENTS = ROOT / "scripts" / "agents"
sys.path.insert(0, str(AGENTS))

try:
    import lib
except ImportError:
    lib = None

# .env yükleme
ENV_FILE = ROOT / ".env"
if ENV_FILE.exists():
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        v = v.strip().strip("'\"")
        os.environ.setdefault(k.strip(), v)

# Ayarlar
BASE_URL = os.environ.get("BASE_URL", "http://localhost:3000")
V1_CATALOG_URL = f"{BASE_URL}/v1"
API_WRITE_URL = f"{BASE_URL}/api"
API_PASSWORD = os.environ.get("MEDSORU_API_PASSWORD", "12345678")

# Gemini API Anahtarları (GEMINI_API_KEY, GEMINI_FREE_KEY_2, GEMINI_BACKUP_KEY)
GEMINI_KEYS = [
    os.environ.get("GEMINI_API_KEY", "").strip(),
    os.environ.get("GEMINI_FREE_KEY_2", "").strip(),
    os.environ.get("GEMINI_BACKUP_KEY", "").strip(),
    os.environ.get("GEMINI_FALLBACK_KEY", "").strip(),
]
GEMINI_KEYS = [k for k in list(dict.fromkeys(GEMINI_KEYS)) if k and not k.startswith("BURAYA_") and not k.startswith("MY_")]


def _paid_key() -> str:
    """ÜCRETLİ anahtar — YALNIZ bu betik (Faz 14) kullanır; ücretsiz anahtarlar tükenince devreye girer.
    Aylık bütçe tavanı (record_cost_and_check_budget) bu anahtar için de geçerlidir."""
    v = os.environ.get("PHASE14_PAID_GEMINI_KEY", "").strip()
    if not v:
        try:
            for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
                if line.startswith("PHASE14_PAID_GEMINI_KEY="):
                    v = line.split("=", 1)[1].strip().strip('"')
        except OSError:
            pass
    return v


if _paid_key() and _paid_key() not in GEMINI_KEYS:
    GEMINI_KEYS.append(_paid_key())

OUT_DIR = ROOT.parent / "meds_database_v2" / "phase14_past_question_editor"
REVIEWS_FILE = OUT_DIR / "reviews.jsonl"
CHECKPOINT_FILE = OUT_DIR / "checkpoint_cloud.json"
REPORT_FILE = OUT_DIR / "report.json"
CURRICULUM_FILE = ROOT / "curriculum" / "kbu_tip_donem3_curriculum.json"

HEADERS_READ = {"Accept": "application/json"}
HEADERS_WRITE = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-API-Password": API_PASSWORD,
}

# Aylık Bütçe ve Maliyet Denetimi (Maksimum 1000 TL / Ay)
# Google GenAI Fiyatları:
# gemini-flash-lite: Girdi $0.075 / 1M token, Çıktı $0.30 / 1M token
# gemini-flash:      Girdi $0.15 / 1M token,  Çıktı $0.60 / 1M token
USD_TO_TRY = 42.0  # Güvenli tavan kur oranı
MAX_MONTHLY_BUDGET_TL = 1000.0
COST_TRACKING_FILE = OUT_DIR / "cost_tracking.json"

MODEL_PRICING = {
    "gemini-flash-lite-latest": {"input": 0.075 / 1_000_000, "output": 0.30 / 1_000_000},
    "gemini-3.5-flash-lite":    {"input": 0.075 / 1_000_000, "output": 0.30 / 1_000_000},
    "gemini-3.1-flash-lite":    {"input": 0.075 / 1_000_000, "output": 0.30 / 1_000_000},
    "gemini-3.8-flash":         {"input": 0.150 / 1_000_000, "output": 0.60 / 1_000_000},
    "gemini-flash-latest":      {"input": 0.150 / 1_000_000, "output": 0.60 / 1_000_000},
}


def load_monthly_cost() -> dict:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    current_month = datetime.utcnow().strftime("%Y-%m")
    if COST_TRACKING_FILE.exists():
        try:
            data = json.loads(COST_TRACKING_FILE.read_text(encoding="utf-8"))
            if data.get("month") == current_month:
                return data
        except Exception:
            pass
    return {
        "month": current_month,
        "total_requests": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "cost_usd": 0.0,
        "cost_tl": 0.0,
        "max_budget_tl": MAX_MONTHLY_BUDGET_TL,
        "last_updated": datetime.utcnow().isoformat() + "Z"
    }


def record_cost_and_check_budget(model_name: str, in_tokens: int, out_tokens: int) -> bool:
    """Maliyeti kaydeder ve 1000 TL bütçe aşımını denetler."""
    pricing = MODEL_PRICING.get(model_name, {"input": 0.15 / 1_000_000, "output": 0.60 / 1_000_000})
    cost_usd = (in_tokens * pricing["input"]) + (out_tokens * pricing["output"])
    cost_tl = cost_usd * USD_TO_TRY

    state = load_monthly_cost()
    state["total_requests"] += 1
    state["input_tokens"] += in_tokens
    state["output_tokens"] += out_tokens
    state["cost_usd"] = round(state["cost_usd"] + cost_usd, 5)
    state["cost_tl"] = round(state["cost_tl"] + cost_tl, 3)
    state["last_updated"] = datetime.utcnow().isoformat() + "Z"

    COST_TRACKING_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    logging.info(f"[Bütçe Takibi] İstek Maliyeti: ~{cost_tl:.4f} TL | Aylık Toplam: {state['cost_tl']:.2f} TL / {MAX_MONTHLY_BUDGET_TL} TL")

    if state["cost_tl"] >= MAX_MONTHLY_BUDGET_TL:
        logging.error(f"[BÜTÇE LİMİTİ AŞILDI] Aylık harcama tavanına ({MAX_MONTHLY_BUDGET_TL} TL) ulaşıldı! Bulut çağrıları durduruluyor.")
        return False
    return True


LOG_FILE = ROOT.parent / "meds_temp" / "logs" / "phase14.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stderr),
        logging.FileHandler(str(LOG_FILE), encoding="utf-8")
    ]
)


def load_checkpoints() -> set[str]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if CHECKPOINT_FILE.exists():
        try:
            return set(json.loads(CHECKPOINT_FILE.read_text(encoding="utf-8")).get("done_ids", []))
        except Exception:
            pass
    return set()


def save_checkpoint(islenmis_set: set[str], soru_id: str):
    islenmis_set.add(soru_id)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {"done_ids": sorted(islenmis_set), "updated_at": datetime.utcnow().isoformat() + "Z"}
    CHECKPOINT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def load_curriculum_summary() -> str:
    if not CURRICULUM_FILE.exists():
        return ""
    try:
        data = json.loads(CURRICULUM_FILE.read_text(encoding="utf-8"))
        comms = data.get("committees", {})
        lines = []
        for code, info in comms.items():
            name = info.get("name", "")
            deps = ", ".join(info.get("departments", [])[:5])
            lines.append(f"- {code} ({name}): Branşlar: {deps}")
        return "\n".join(lines)
    except Exception:
        return ""


def call_gemini_json(prompt_text: str) -> tuple[dict | None, str]:
    """Doğrudan HTTP REST API ile en düşük maliyetli ve aktif Gemini Flash-Lite/Flash modellerini çağırır."""
    cost_data = load_monthly_cost()
    if cost_data["cost_tl"] >= MAX_MONTHLY_BUDGET_TL:
        logging.warning(f"Aylık bütçe kotası ({MAX_MONTHLY_BUDGET_TL} TL) dolduğu için bulut API çağrısı engellendi.")
        if lib:
            logging.info("Sıfır maliyetli yerel model (RTX 4060 - Gemma 3) fallback devreye giriyor...")
            res = lib.chat(lib.MODEL_TEXT, prompt_text, as_json=True, timeout=120)
            if isinstance(res, dict):
                return res, f"local-{lib.MODEL_TEXT}"
        return None, "budget_exceeded"

    # En düşük maliyetli, yüksek kotalı ve aktif resmi modeller sırasıyla denenir
    models = [
        "gemini-flash-lite-latest",
        "gemini-3.5-flash-lite",
        "gemini-3.1-flash-lite",
        "gemini-3.8-flash",
        "gemini-flash-latest",
    ]
    payload = {
        "contents": [{"parts": [{"text": prompt_text}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.1,
        },
    }
    data_bytes = json.dumps(payload).encode("utf-8")

    for key in GEMINI_KEYS:
        for model in models:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
            req = urllib.request.Request(
                url,
                data=data_bytes,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    res_body = json.loads(resp.read().decode("utf-8"))
                    text = (
                        res_body.get("candidates", [{}])[0]
                        .get("content", {})
                        .get("parts", [{}])[0]
                        .get("text", "")
                        .strip()
                    )
                    usage = res_body.get("usageMetadata", {})
                    in_tokens = usage.get("promptTokenCount", len(prompt_text) // 4)
                    out_tokens = usage.get("candidatesTokenCount", len(text) // 4)
                    record_cost_and_check_budget(model, in_tokens, out_tokens)

                    if text.startswith("```"):
                        lines = text.splitlines()
                        if lines[0].startswith("```"):
                            lines = lines[1:]
                        if lines and lines[-1].startswith("```"):
                            lines = lines[:-1]
                        text = "\n".join(lines).strip()
                    return json.loads(text), model
            except urllib.error.HTTPError as e:
                err_text = e.read().decode("utf-8", errors="ignore")
                if e.code == 429:
                    logging.warning(f"Gemini {model} rate limit (429), sonraki düşük maliyetli modele geçiliyor...")
                    time.sleep(1)
                    continue
                elif e.code in (404, 503):
                    logging.warning(f"Gemini {model} kullanılamıyor ({e.code}), alternatif model deneniyor...")
                    continue
                logging.error(f"Gemini HTTP {e.code} hatası ({model}): {err_text[:200]}")
            except Exception as e:
                logging.warning(f"Gemini çağrı hatası ({model}): {e}")
                continue

    # Bulut anahtarları veya kotaları yetersizse yerel sıfır maliyetli model fallback
    if lib:
        try:
            logging.info("Gemini kotaları nedeniyle yerel model fallback devreye giriyor (Gemma 3)...")
            res = lib.chat(lib.MODEL_TEXT, prompt_text, as_json=True, timeout=120)
            if isinstance(res, dict):
                return res, f"local-{lib.MODEL_TEXT}"
        except Exception as e:
            logging.error(f"Yerel model fallback hatası: {e}")

    return None, "none"


def canonical_options(question: dict) -> dict[str, str]:
    raw = question.get("options") or (question.get("reconstruction") or {}).get("options") or {}
    if isinstance(raw, dict):
        return {str(k).upper(): str(v) for k, v in raw.items() if str(k).upper() in "ABCDE"}
    if isinstance(raw, list):
        result = {}
        for i, item in enumerate(raw[:5]):
            key = "ABCDE"[i]
            result[key] = str(item.get("text", "")) if isinstance(item, dict) else str(item)
        return result
    return {}


def source_view(question: dict) -> dict:
    rec = question.get("reconstruction") or {}
    return {
        "id": question.get("id"),
        "soru_koku": question.get("stem") or question.get("rawQuestion", {}).get("stem") or rec.get("stem") or "",
        "secenekler": canonical_options(question),
        "dogru_secenek": question.get("correctAnswer") or question.get("claimedAnswer") or rec.get("answer") or "",
        "aciklama": question.get("explanation") or rec.get("explanation") or "",
        "kurul_adi": question.get("committeeId") or "",
        "ders_adi": question.get("discipline") or "",
        "konu_adi": question.get("topic") or "",
    }


def ai_ile_soruyu_duzelt(soru: dict, mufredat_ozeti: str = "") -> tuple[dict | None, str]:
    """Soru verisini Gemini Bulut Modeline gönderir ve tıbbi literatüre göre YZV bloğuyla düzenletir."""
    prompt = f"""Sen uzman bir tıp doktoru, akademisyen ve tıp fakültesi kurul/USMLE/TUS sınav soru hazırlama komisyonu başkanısın.
Aşağıda verilen tıp fakültesi çıkmış sınav sorusunu tıbbi literatüre (Robbins & Cotran Patoloji, Guyton & Hall Tıbbi Fizyoloji, Harrison İç Hastalıkları, Goodman & Gilman Farmakoloji vb.) ve resmi tıp müfredatına göre titizlikle incele.

KESİN TALİMATLAR VE GÖREVLER (ZORUNLU KURALLAR):
1. SORU KÖKÜ VE MANTIĞI KESİNLİKLE KÖKLÜ DEĞİŞTİRİLEMEZ (ZORUNLU KORUMA):
   - Soru kökündeki imla hatalarını, harf düşmelerini (örn: 'patloji' -> 'patoloji', 'etkisiyle' -> 'etkisi ile'), fazla/tekrarlanan harfleri ve OCR karakter bozukluklarını (0/O, 1/I, bozuk Türkçe karakterler) düzelt.
   - DİKKAT: Soru kökünün yönünü, mantığını ve hedefini KÖKLÜ BİÇİMDE DEĞİŞTİRMEK KESİNLİKLE YASAKTIR!
     * Örneğin: 'Hangisi doğrudur?' sorusu ASLA 'Hangisi yanlıştır / doğru değildir?' diye değiştirilemez!
     * Soru olumlu sorulmuşsa ('...etkendir', '...görülür', '...en olasıdır') olumsuz yapılamaz; olumsuz sorulmuşsa ('...değildir', '...beklenmez') olumlu yapılamaz!
     * Sorunun doğru cevabını ve doğru şıkkını değiştirecek hiçbir köklü manipülasyon yapılamaz!

2. ESKİ, GEREKSİZ VE ANLAMSIZ AÇIKLAMALARIN YENİDEN YAZILMASI:
   - Eski, yetersiz, kopyala-yapıştır veya soruyla alakasız açıklamaları tamamen temizle.
   - Soruya ve doğru cevaba doğrudan odaklanan, klinik ve fizyopatolojik/farmakolojik mekanizmayı açıklayan, doğru şıkkın neden doğru olduğunu ve diğer önemli çeldiricilerin neden elendiğini net olarak anlatan öğretici, kaliteli bir açıklama yaz.

3. ŞIKLARIN KONTROLÜ, EKSİK ŞIKLARI TAMAMLAMA VE CEVAP DOĞRULAMA:
   - 5 seçeneğin (A, B, C, D, E) tamamı mevcut olmalıdır. Eğer soru kaynağında eksik şık varsa (örneğin yalnızca 3 veya 4 şık hatırlanmışsa ya da şık boşsa):
     * Klinik mekanizmaya, komite müfredatına ve soru köküne uygun güçlü, mantıklı tıbbi çeldiriciler üreterek 5 şıkkı (A, B, C, D, E) eksiksiz tamamla!
     * Sonradan yapay zekâ tarafından üretilen/tamamlanan şıkların harflerini "yapay_zeka_tamamlanan_siklar" listesine ekle (örn: ["D", "E"] veya ["E"]).
   - Şıklar içindeki metinleri denetle: Bazen cümleler birleşik basılmış ('hastanıntetkikinde'), kelimeler yapışık ('akutapandisit'), eksik veya karakter bazlı bozukluklar taşıyor olabilir. Birleşik kelimeleri ayır, imla ve Latince terminoloji hatalarını düzelt.
   - Kaynak doğru cevap anahtarına saygı duy; sadece açıkça kanıtlanabilir bariz bir tıp/dizgi hatası varsa gerekçesini belirterek düzelt, keyfi cevap kaydırması yapma.

4. MÜFREDAT VE JSON ŞEMA UYUMLULUĞU:
   - Bu sorunun hangi Kurul (örn: TIP310, TIP320, TIP340, TIP350, TIP360), hangi Ders (Anatomi, Fizyoloji, Patoloji, Farmakoloji, Mikrobiyoloji, Dahiliye, Cerrahi vb.) ve hangi Konu başlığına ait olduğunu resmi müfredata göre tespit et ve JSON içine yaz.
   - Yapılan her müdahaleyi şeffaf biçimde 'YZV' (Yapay Zeka Verisi) altında listele.

MEVCUT SORU VERİSİ:
{json.dumps(soru, ensure_ascii=False, indent=2)}

MÜFREDAT BİLGİSİ / İPUCU:
{mufredat_ozeti}

LÜTFEN YALNIZCA AŞAĞIDAKİ JSON ŞEMASINDA YANIT VER:
{{
  "soru_koku": "Yazım hataları, fazla veya eksik harfleri düzeltilmiş, anlam bütünlüğü tam soru kökü",
  "secenekler": {{
     "A": "...",
     "B": "...",
     "C": "...",
     "D": "...",
     "E": "..."
  }},
  "dogru_secenek": "A/B/C/D/E",
  "yapay_zeka_tamamlanan_siklar": ["E"],
  "aciklama": "Soru ve şıklarla doğrudan ilişkili, tıbbi literatüre dayalı yeni ve detaylı açıklama",
  "kurul_adi": "Belirlenen Kurul Adı veya Kodu (örn: TIP310)",
  "ders_adi": "Belirlenen Ders Adı (örn: Patoloji)",
  "konu_adi": "Belirlenen Konu Adı (örn: Kronik Enflamasyon)",
  "degisen_alanlar": ["soru_koku", "aciklama", "kurul_adi", "ders_adi", "konu_adi"],
  "degisiklik_ozeti": "Yapılan düzeltmelerin kısa ve somut özeti (harf hataları, açıklama yenilemesi, AI şık tamamlama vb.)",
  "review_required": true,
  "YZV": {{
     "islem_zamani": "{datetime.utcnow().isoformat()}Z",
     "degisiklik_yapildi_mi": true,
     "degisen_alanlar": ["soru_koku", "aciklama", "kurul_adi"],
     "degisiklik_ozeti": {{
        "soru_koku_duzeltmesi": "Soru kökündeki harf/imla/anlam düzeltmelerinin detayı",
        "aciklama_duzeltmesi": "Açıklamanın tıbbi literatüre göre nasıl yenilendiği",
        "sik_duzeltmesi_ve_tamamlama": "Şıklardaki birleşik kelimelerin ayrılması ve eksik şıkların AI ile tamamlanması",
        "mufredat_atamasi": "Atanan ders, kurul ve konu gerekçesi",
        "cevap_dogrulamasi": "Doğru şıkkın tıbbi gerekçesi"
     }},
     "referans_literatur": "İlgili standart kaynak (örn. Robbins Patoloji 10. Baskı, Bl. 3)"
  }}
}}"""
    return call_gemini_json(prompt)


def support_ratio(original: dict, proposal: dict) -> float:
    def get_tokens(text: str) -> set[str]:
        return set(text.lower().split())

    before = " ".join([original.get("soru_koku", ""), original.get("aciklama", ""), *original.get("secenekler", {}).values()])
    after = " ".join([str(proposal.get("soru_koku") or ""), str(proposal.get("aciklama") or ""),
                      *[str(v) for v in (proposal.get("secenekler") or {}).values()]])
    tok_after = get_tokens(after)
    if not tok_after:
        return 1.0
    new_tokens = tok_after - get_tokens(before)
    return round(max(0.0, 1.0 - (len(new_tokens) / len(tok_after))), 3)


def main() -> int:
    parser = argparse.ArgumentParser(description="Faz 14 Bulut Tabanlı Çıkmış Soru İyileştirme")
    parser.add_argument("--limit", type=int, default=10, help="Bu çalıştırmada incelenecek soru sayısı")
    parser.add_argument("--chunk-size", type=int, default=30, help="API'den bir seferde çekilecek soru sayısı")
    parser.add_argument("--direct-apply", action="store_true", help="İnceleme katmanına yazmanın yanı sıra /api üzerinden de doğrudan uygula")
    args = parser.parse_args()

    islenmisler = load_checkpoints()
    curriculum_summary = load_curriculum_summary()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Soruları çek: Önce yerel veritabanı dosyasından veya /v1/past-exams endpointinden
    questions = []
    local_past = ROOT / "data" / "pastQuestions.json"
    if local_past.exists():
        try:
            raw = json.loads(local_past.read_text(encoding="utf-8"))
            questions = raw if isinstance(raw, list) else raw.get("questions", [])
            logging.info(f"Yerel çıkmış soru deposundan {len(questions)} soru yüklendi.")
        except Exception as e:
            logging.warning(f"Yerel dosya okunamadı: {e}")

    if not questions:
        try:
            req = urllib.request.Request(f"{V1_CATALOG_URL}/past-exams", headers=HEADERS_READ)
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read().decode("utf-8"))
                questions = data.get("questions", [])
                logging.info(f"/v1/past-exams üzerinden {len(questions)} soru çekildi.")
        except Exception as e:
            logging.error(f"Soru çekme hatası: {e}")
            return 1

    stats = {"aday": len(questions), "islenen": 0, "degisiklik_onerisi": 0, "inceleme_gerekli": 0, "hata": 0}

    with REVIEWS_FILE.open("a", encoding="utf-8") as out_reviews:
        for q in questions:
            s_id = str(q.get("id") or "")
            if not s_id or s_id in islenmisler:
                continue
            if stats["islenen"] >= args.limit:
                break

            src = source_view(q)
            if len(src["soru_koku"].strip()) < 15 or len(src["secenekler"]) < 4:
                continue

            logging.info(f"Soru #{s_id} Google Gemini ile inceleniyor...")
            ai_sonuc, model_used = ai_ile_soruyu_duzelt(src, curriculum_summary)

            if not ai_sonuc or not isinstance(ai_sonuc, dict):
                logging.warning(f"Soru #{s_id} için AI yanıtı alınamadı.")
                stats["hata"] += 1
                continue

            ratio = support_ratio(src, ai_sonuc)
            changed = ai_sonuc.get("degisen_alanlar") or []
            if not changed and ai_sonuc.get("YZV", {}).get("degisiklik_yapildi_mi"):
                changed = ["soru_koku", "aciklama"]

            # İnceleme katmanı kaydı
            record = {
                "question_id": s_id,
                "source_hash": hashlib.sha256(json.dumps(src, ensure_ascii=False, sort_keys=True).encode()).hexdigest(),
                "processed_at": datetime.utcnow().isoformat() + "Z",
                "model": model_used or "gemini-flash-lite-latest",
                "source": src,
                "proposal": ai_sonuc,
                "support_ratio": ratio,
                "status": "review_required" if (ratio < 0.85 or ai_sonuc.get("review_required", True)) else "unchanged",
            }

            out_reviews.write(json.dumps(record, ensure_ascii=False) + "\n")
            out_reviews.flush()

            stats["islenen"] += 1
            stats["degisiklik_onerisi"] += int(bool(changed))
            stats["inceleme_gerekli"] += int(record["status"] == "review_required")

            save_checkpoint(islenmisler, s_id)
            logging.info(f"✓ Soru #{s_id} inceleme katmanına yazıldı ({record['status']}, kanıt {ratio}).")

            # Eğer --direct-apply verilmişse canlı API'ye yaz
            if args.direct_apply:
                try:
                    update_body = dict(q)
                    update_body.update(ai_sonuc)
                    up_req = urllib.request.Request(
                        f"{API_WRITE_URL}/questions/{s_id}",
                        data=json.dumps(update_body).encode("utf-8"),
                        headers=HEADERS_WRITE,
                        method="PUT",
                    )
                    with urllib.request.urlopen(up_req, timeout=10) as up_res:
                        if up_res.status in [200, 204]:
                            logging.info(f"✓ Soru #{s_id} /api/questions üzerinden güncellendi.")
                except Exception as up_err:
                    logging.warning(f"Doğrudan güncelleme hatası (#{s_id}): {up_err}")

            time.sleep(1)

    REPORT_FILE.write_text(json.dumps({
        "zaman": datetime.utcnow().isoformat() + "Z",
        "motor": "Google Gemini Flash (Bulut)",
        **stats,
        "cikti": str(REVIEWS_FILE),
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    logging.info(f"Faz 14 Bulut İşlemi Tamamlandı: {stats}")
    print(json.dumps(stats, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
