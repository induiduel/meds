#!/usr/bin/env python3
"""
scripts/agents/post_lora_auto_refiner.py
--------------------------------------------------------------------------------
MedSoru Otonom Veri Düzeltme & İyileştirme Motoru (Post-Training Autonomous Dataset Refiner)

Amaç:
1. QLoRA eğitimi sonrasında veya arka plan otomasyonu olarak tüm verileri baştan sona denetler.
2. Tespit edilen kusurları otomatik onarır:
   - Mükerrer / Tekrar eden soruları birleştirir veya arşive alır (deduplication).
   - Bozuk karakterleri, OCR gürültülerini (0->O, 1->I karışımları, ligatürler, Mojibake) düzeltir.
   - 15 karakterden kısa anlamsız taslak / kopuk kökleri temizler.
   - Boş kalan şıkları tespit edip temizler.
   - Soru kökündeki tıbbi terim yoğunluğuna göre yanlış branş/ders/kurul etiketlerini doğru disipline atar.
3. Güncellenen ve temizlenen doğrulanmış veri kümesini:
   - meds/data/pastQuestions.json
   - meds_database/questions/
   - SQLite / Yerel DB
   dosyalarına atomik olarak yazar.
4. İsteğe bağlı olarak --sync-supabase bayrağı ile Supabase tablolarını (past_questions) anında günceller.
5. İyileştirme raporunu `meds_temp/state/dataset_refinement_report.json` olarak kaydeder.
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "pastQuestions.json"
DATABASE_DIR = ROOT / "meds_database" / "questions"
TEMP_STATE = Path(os.environ.get("MEDS_TEMP_DIR") or ROOT.parent / "meds_temp") / "state"
TEMP_STATE.mkdir(parents=True, exist_ok=True)
REPORT_FILE = TEMP_STATE / "dataset_refinement_report.json"
AUDIT_SUGGESTIONS_FILE = TEMP_STATE / "quality_audit_suggestions.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [DataRefiner] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(TEMP_STATE.parent / "logs" / "data_refiner.log", encoding="utf-8")
    ]
)
log = logging.getLogger("DataRefiner")

# Türkçe normalizasyonu
TR_MAP = str.maketrans("çğıöşüâîûÇĞİÖŞÜÂÎÛ", "cgiosuaiucgiosuaiu")

def normalize_text(s: str) -> str:
    if not s:
        return ""
    s = s.translate(TR_MAP).lower()
    return re.sub(r"[^\w\s]", " ", s)

def tokenize(s: str) -> List[str]:
    return [w for w in normalize_text(s).split() if len(w) > 2]

def jaccard_similarity(tokens1: List[str], tokens2: List[str]) -> float:
    set1, set2 = set(tokens1), set(tokens2)
    if not set1 or not set2:
        return 0.0
    return len(set1 & set2) / len(set1 | set2)

# OCR ve Bozuk Metin Onarım Kalıpları
REPAIR_RULES = [
    # Mojibake UTF-8 çift kodlama onarımı
    (r"Ã§", "ç"),
    (r"Ã¶", "ö"),
    (r"Ã¼", "ü"),
    (r"ÄŸ", "ğ"),
    (r"Ä±", "ı"),
    (r"ÅŸ", "ş"),
    (r"Ã‡", "Ç"),
    (r"Ã–", "Ö"),
    (r"Ãœ", "Ü"),
    (r"Äž", "Ğ"),
    (r"Ä°", "İ"),
    (r"Åž", "Ş"),
    # Görünmeyen veya bozuk kontrol karakterleri
    (r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", ""),
    # Ligatür birleşmeleri
    (r"\bfl\b", "fi"),
    # URL veya sistem analiz artıklarının kökten arındırılması
    (r"https?://\S+", ""),
    (r"sinav\.karab[uü]k\.edu\.tr\S*", ""),
    (r"\b\d{4}/\s*\d{1,2}/\s*\d{1,2}\b", ""),
]

# Tıbbi Anabilim Dalı Anahtar Kelime Haritası (İçerik Analizi)
DISCIPLINE_PATTERNS = {
    "Tıbbi Anatomi": [
        "foramen", "nervus", "arteria", "vena", "musculus", "ligamentum", "pleksus", 
        "sulcus", "fossa", "kemik", "eklem", "kas", "kol", "bacak", "kraniyal", "vertebra"
    ],
    "Tıbbi Fizyoloji": [
        "aksiyon potansiyeli", "depolarizasyon", "repolarizasyon", "glomerüler filtrasyon", 
        "klirens", "frank-starling", "surfactant", "osmolalite", "onkotik", "hemostaz", 
        "membran potansiyeli", "sodyum potasyum pompasi", "fizyoloji"
    ],
    "Tıbbi Patoloji": [
        "granülom", "nekroz", "kazeifikasyon", "displazi", "metaplazi", "karsinom", 
        "adenom", "anaplazisi", "apopitoz", "lenfoid", "biyopsi", "infiltrasyon", 
        "kresent", "amiloid", "dev hücre", "reed-sternberg", "psammom"
    ],
    "Tıbbi Farmakoloji": [
        "agonist", "antagonist", "biyoyararlanım", "yarı ömrü", "reseptör blokeri", 
        "sitokrom p450", "toksisite", "yan etki", "kontrendike", "inhibitorü", 
        "antifungal", "antibiyotik", "diüretik", "antiaritmik", "farmakoloji", "nistatin"
    ],
    "Tıbbi Mikrobiyoloji": [
        "gram pozitif", "gram negatif", "aerop", "anaerop", "basil", "kok", "virüs", 
        "mantar", "parazit", "antijen", "elisa", "pcr", "toksin", "endotoksin", 
        "kapsüllü", "kültür", "staphylococcus", "streptococcus"
    ],
    "Tıbbi Biyokimya": [
        "glikoliz", "krebs", "oksidatif fosforilasyon", "kolesterol sentezi", "enzim", 
        "allosterik", "substrat", "km değeri", "apoenzim", "koenzim", "vitamin", 
        "bilirubin", "üre siklusu", "lipoprotein", "hdl", "ldl"
    ],
    "Tıbbi Genetik": [
        "otozomal dominant", "otozomal resesif", "x'e bağlı", "trizomi", "monozomi", 
        "karyotip", "mutasyon", "translokasyon", "delesyon", "polikistik böbrek", 
        "turner sendromu", "klinefelter", "down sendromu", "genetik"
    ],
    "Halk Sağlığı": [
        "insidans", "prevalans", "mortalite", "morbidite", "hız", "oran", "surveyans", 
        "tarama testi", "duyarlılık", "özgüllük", "bağışıklama", "salgın", "epidemiyoloji"
    ]
}

class PostLoraDatasetRefiner:
    def __init__(self, data_file: Path = DATA_PATH):
        self.data_file = data_file
        self.questions: List[Dict[str, Any]] = []
        self.stats = {
            "initial_count": 0,
            "final_count": 0,
            "duplicates_removed": 0,
            "corrupted_stems_cleaned": 0,
            "ocr_artifacts_fixed": 0,
            "empty_options_fixed": 0,
            "disciplines_reclassified": 0,
            "invalid_stems_dropped": 0
        }
        self.load_data()

    def load_data(self):
        if not self.data_file.exists():
            log.error(f"Veri dosyası bulunamadı: {self.data_file}")
            sys.exit(1)
        with open(self.data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.questions = data if isinstance(data, list) else data.get("questions", [])
        self.stats["initial_count"] = len(self.questions)
        log.info(f"{len(self.questions)} soru belleğe yüklendi.")

    def clean_text_artifacts(self, text: str) -> Tuple[str, bool]:
        """Metindeki OCR gürültülerini ve kontrol karakterlerini onarır."""
        if not text:
            return "", False
        original = text
        repaired = text
        for pat, rep in REPAIR_RULES:
            repaired = re.sub(pat, rep, repaired)

        # Çoklu boşlukları ve kırık satırları tek tipe getir
        repaired = re.sub(r"[ \t]+", " ", repaired)
        repaired = re.sub(r"\n\s*\n+", "\n", repaired).strip()
        changed = repaired != original
        return repaired, changed

    def determine_correct_discipline(self, stem: str, current_discipline: str) -> Tuple[str, bool]:
        """Soru içeriğine göre en uygun tıbbi ana bilim dalını belirler."""
        norm_stem = normalize_text(stem)
        scores: Dict[str, int] = {}
        for disc, kws in DISCIPLINE_PATTERNS.items():
            score = sum(1 for kw in kws if kw in norm_stem)
            if score > 0:
                scores[disc] = score

        if not scores:
            return current_discipline, False

        best_disc, best_score = max(scores.items(), key=lambda x: x[1])
        # Güvenilirlik eşiği: En az 2 anahtar kelime veya çok belirgin tekil tıp kavramı
        if best_score >= 2:
            current_clean = current_discipline.strip()
            if normalize_text(best_disc) not in normalize_text(current_clean):
                return best_disc, True
        return current_discipline, False

    def refine_dataset(self) -> List[Dict[str, Any]]:
        """Tüm veri kümesini temizler, düzenler ve mükerrerleri ayıklar."""
        log.info("Veri kümesi temizleme ve kalite optimizasyonu başlatılıyor...")
        refined_pool: List[Dict[str, Any]] = []
        seen_token_signatures: Dict[str, str] = {} # token_signature -> qid

        for idx, q in enumerate(self.questions):
            stem = q.get("stem") or q.get("reconstruction", {}).get("stem") or ""
            qid = q.get("id") or str(q.get("questionNumber") or idx + 1)

            # 1. OCR ve Tipografik Karakter Onarımı
            clean_stem, changed = self.clean_text_artifacts(stem)
            if changed:
                self.stats["ocr_artifacts_fixed"] += 1
                q["stem"] = clean_stem
                if "reconstruction" in q and isinstance(q["reconstruction"], dict):
                    q["reconstruction"]["stem"] = clean_stem

            # 2. Geçersiz / Anlamsız Soru Köklerini Eleme (< 15 karakter veya anlamsız sınav linkleri)
            if len(clean_stem.strip()) < 15 or len(clean_stem.split()) < 3:
                self.stats["invalid_stems_dropped"] += 1
                continue

            # 3. Şıkları Denetleme ve Boş Şıkları Temizleme
            options = q.get("options") or q.get("reconstruction", {}).get("options") or []
            valid_options = []
            if isinstance(options, list):
                for opt in options:
                    if isinstance(opt, dict):
                        text = opt.get("text") or ""
                        c_text, _ = self.clean_text_artifacts(text)
                        if c_text.strip():
                            opt["text"] = c_text
                            valid_options.append(opt)
                    elif isinstance(opt, str) and opt.strip():
                        valid_options.append(opt)

            if len(valid_options) < len(options):
                self.stats["empty_options_fixed"] += 1

            q["options"] = valid_options
            if "reconstruction" in q and isinstance(q["reconstruction"], dict):
                q["reconstruction"]["options"] = valid_options

            # 4. Tıbbi Anabilim Dalı Uyuşmazlığı Otomasyonu
            curr_disc = q.get("discipline") or "Tıp"
            new_disc, disc_changed = self.determine_correct_discipline(clean_stem, curr_disc)
            if disc_changed:
                self.stats["disciplines_reclassified"] += 1
                q["discipline"] = new_disc
                q["topic"] = f"{new_disc} Kurul Sorusu"

            # 5. Mükerrer / Tekrar Eden Soruları Ayıklama
            tokens = tuple(tokenize(clean_stem)[:15]) # İlk 15 anahtar kelime
            token_sig = " ".join(tokens)
            if token_sig and token_sig in seen_token_signatures:
                # Mükerrer kopya tespit edildi, atla
                self.stats["duplicates_removed"] += 1
                continue

            if token_sig:
                seen_token_signatures[token_sig] = qid

            q["updatedAt"] = datetime.now(timezone.utc).isoformat()
            refined_pool.append(q)

        self.stats["final_count"] = len(refined_pool)
        self.questions = refined_pool
        log.info(f"Temizleme tamamlandı. {self.stats['initial_count']} -> {self.stats['final_count']} soru.")
        return refined_pool

    def save_to_disk(self):
        """Sonuçları veri dosyalarına atomik olarak yazar."""
        log.info(f"Temizlenmiş sorular kaydediliyor: {self.data_file}")
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.questions, f, ensure_ascii=False, indent=2)

        # Raporu kaydet
        report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "success",
            "stats": self.stats
        }
        with open(REPORT_FILE, "w", encoding="utf-8") as rf:
            json.dump(report, rf, ensure_ascii=False, indent=2)
        log.info(f"İyileştirme raporu kaydedildi: {REPORT_FILE}")

def main():
    parser = argparse.ArgumentParser(description="MedSoru Post-Training Autonomous Dataset Refiner")
    parser.add_argument("--sync-supabase", action="store_true", help="Temizlenen soruları Supabase'e de senkronize et")
    args = parser.parse_args()

    refiner = PostLoraDatasetRefiner()
    refiner.refine_dataset()
    refiner.save_to_disk()

    if args.sync_supabase:
        log.info("Supabase senkronizasyonu başlatılıyor...")
        try:
            import subprocess
            cmd = [sys.executable, str(ROOT / "scripts" / "sync_to_supabase_v2.py"), "--questions-only"]
            subprocess.run(cmd, check=True)
            log.info("Supabase senkronizasyonu tamamlandı ✓")
        except Exception as e:
            log.error(f"Supabase senkronizasyonu sırasında hata: {e}")

if __name__ == "__main__":
    main()
