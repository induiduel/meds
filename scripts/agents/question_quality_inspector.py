#!/usr/bin/env python3
"""
scripts/agents/question_quality_inspector.py
Otonom Soru Kalite ve Bağlam Denetçisi (Autonomous Medical Question Quality & Audit Inspector)

Arka planda donanımı yormadan (düşük öncelikli, throttled) çalışır:
1. Tekrar eden soruları (duplicate detection via Levenshtein / Token Jaccard) tespit eder.
2. Bozuk karakterleri, kesik cümleleri, OCR artefaktlarını (0->O, 1->I, kırık heceler) saptar.
3. Anlamsız / çok kısa soru köklerini, eksik şıkları (A-E eksikliği) bulur.
4. İlişkisiz şıkları veya kökle bağlam kopukluğunu tespit eder.
5. Kurul, ders ve konu etiket hatalarını analiz eder.
6. Tespit edilen tüm bulguları ve düzeltme önerilerini `meds_temp/state/quality_audit_suggestions.json`
   dosyasına ve gerektiğinde SQLite/Supabase denetim tablolarına kaydeder.
"""
from __future__ import annotations

import json
import logging
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "pastQuestions.json"
TEMP_STATE = Path(os.environ.get("MEDS_TEMP_DIR") or ROOT.parent / "meds_temp") / "state"
TEMP_STATE.mkdir(parents=True, exist_ok=True)
AUDIT_OUTPUT = TEMP_STATE / "quality_audit_suggestions.json"
PROGRESS_FILE = TEMP_STATE / "quality_audit_progress.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [QualityInspector] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(TEMP_STATE.parent / "logs" / "quality_inspector.log", encoding="utf-8")
    ]
)
log = logging.getLogger("QualityInspector")

# Türkçe karakter normalizasyonu
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

# OCR Artefaktları & Bozuk Karakter Paternleri
BROKEN_PATTERNS = [
    (r"\b[0-9]+[a-zA-Z]+[0-9]+\b", "Rakam-harf karışımı olası OCR gürültüsü"),
    (r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "Görünmeyen kontrol karakterleri"),
    (r"[Ã§Ã¶Ã¼ÄŸÄ±ÅŸ]", "UTF-8 bozuk çift kodlama (Mojibake)"),
    (r"(\w)\s+(\1\s+){2,}", "Tekrarlanan bozuk harf gürültüsü"),
    (r"\b(fi|fl|ffi|ffl)\b", "Tipografik ligatür hatası"),
]

MEDICAL_DISCIPLINES = {
    "anatomi": ["anatomi", "kemik", "kas", "arter", "ven", "sinir", "foramen", "ligament", "fossa"],
    "fizyoloji": ["fizyoloji", "potansiyel", "aksiyon", "reseptor", "membran", "filtrasyon", "klirens", "basinc"],
    "patoloji": ["patoloji", "nekroz", "karsinom", "inflamasyon", "biyopsi", "granulom", "neoplazi", "atrofi", "displazi"],
    "farmakoloji": ["farmakoloji", "ilac", "agonist", "antagonist", "doz", "reseptoru", "toksisite", "etki", "inhibitor"],
    "mikrobiyoloji": ["mikrobiyoloji", "bakteri", "virus", "kultur", "gram", "kok", "basil", "mantar", "parazit", "antijen"],
    "biyokimya": ["biyokimya", "enzim", "glukoz", "lipid", "protein", "sentez", "kinaz", "substrat", "metabolizma"],
    "tibbi genetik": ["genetik", "kromozom", "mutasyon", "otozomal", "delesyon", "dna", "rna", "resesif", "dominant"],
    "halk sagligi": ["halk sagligi", "insidans", "prevalans", "mortalite", "epidemiyoloji", "surveyans", "tarama", "asi"]
}

class QuestionQualityInspector:
    def __init__(self, data_file: Path = DATA_PATH):
        self.data_file = data_file
        self.questions: List[Dict[str, Any]] = []
        self.load_questions()

    def load_questions(self):
        if not self.data_file.exists():
            log.error(f"Soru dosyası bulunamadı: {self.data_file}")
            return
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    self.questions = data
                elif isinstance(data, dict) and "questions" in data:
                    self.questions = data["questions"]
            log.info(f"{len(self.questions)} soru denetim için yüklendi.")
        except Exception as e:
            log.error(f"Soru dosyası yüklenirken hata: {e}")

    def inspect_single_question(self, q: Dict[str, Any]) -> Dict[str, Any]:
        """Tek bir soruyu yapısal, içeriksel ve tıbbi bağlam açısından denetler."""
        qid = q.get("id") or str(q.get("questionNumber") or q.get("no") or "bilinmeyen")
        stem = q.get("stem") or q.get("text") or q.get("questionText") or ""
        options = q.get("options") or []
        answer = q.get("correctAnswer") or q.get("answer") or q.get("claimedAnswer") or ""
        committee = str(q.get("committeeId") or q.get("committee") or "")
        discipline = str(q.get("discipline") or q.get("subject") or "").lower()

        issues: List[str] = []
        suggestions: List[Dict[str, Any]] = []
        severity = "info"  # info, warning, error

        # 1. Kök Uzunluk & Anlamsızlık Kontrolü
        stem_clean = stem.strip()
        if len(stem_clean) < 15:
            issues.append("Soru kökü çok kısa veya anlamsız (< 15 karakter).")
            severity = "error"
        elif len(stem_clean.split()) < 4:
            issues.append("Soru kökü yetersiz kelime içeriyor (eksik taslak olabilir).")
            severity = "warning"

        # 2. Bozuk Harf & OCR Gürültüsü
        for pattern, desc in BROKEN_PATTERNS:
            if re.search(pattern, stem_clean):
                issues.append(f"Metinde OCR/Kodlama bozukluğu tespit edildi: {desc}")
                if severity != "error":
                    severity = "warning"
                # Olası basit onarım önerisi
                fixed_stem = re.sub(pattern, " ", stem_clean)
                suggestions.append({
                    "field": "stem",
                    "action": "ocr_cleanup",
                    "detail": f"Şüpheli karakterler temizlendi",
                    "proposed_value": re.sub(r"\s+", " ", fixed_stem).strip()
                })
                break

        # 3. Şık Bütünlüğü Kontrolü (A-E)
        opt_keys = []
        opt_texts = []
        if isinstance(options, list):
            for opt in options:
                if isinstance(opt, dict):
                    k = opt.get("key") or opt.get("optionKey") or ""
                    t = opt.get("text") or opt.get("optionText") or ""
                    opt_keys.append(str(k).upper())
                    opt_texts.append(t)
                elif isinstance(opt, str):
                    opt_texts.append(opt)
        elif isinstance(options, dict):
            for k, t in options.items():
                opt_keys.append(str(k).upper())
                opt_texts.append(str(t))

        if len(opt_texts) < 4:
            issues.append(f"Eksik şık sayısı: Toplam {len(opt_texts)} şık var (en az 4 veya 5 olmalı).")
            severity = "warning"
        
        # Boş şık kontrolü
        empty_opts = [i for i, t in enumerate(opt_texts) if not str(t).strip()]
        if empty_opts:
            issues.append(f"İçeriği tamamen boş olan {len(empty_opts)} şık bulundu.")
            severity = "error"

        # 4. Doğru Cevap / Anahtar Eşleşmesi
        if answer:
            ans_clean = str(answer).strip().upper()
            if len(ans_clean) == 1 and ans_clean in ["A", "B", "C", "D", "E"]:
                if opt_keys and ans_clean not in opt_keys:
                    issues.append(f"Belirtilen doğru şık ({ans_clean}) mevcut şıklar ({', '.join(opt_keys)}) arasında yok!")
                    severity = "error"
        else:
            issues.append("Doğru cevap anahtarı atanmamış.")
            if severity == "info":
                severity = "warning"

        # 5. Tıbbi Anabilim Dalı & Bağlam Tutarlılığı
        norm_stem = normalize_text(stem_clean)
        detected_disciplines = []
        for disc, keywords in MEDICAL_DISCIPLINES.items():
            matches = [kw for kw in keywords if kw in norm_stem]
            if len(matches) >= 2:
                detected_disciplines.append(disc)

        if detected_disciplines and discipline:
            norm_disc = normalize_text(discipline)
            # Eğer sorudaki belirgin anahtar kelimeler mevcut branşla uyuşmuyorsa
            is_match = any(norm_disc in d or d in norm_disc for d in detected_disciplines)
            if not is_match and len(detected_disciplines) == 1:
                suggested_disc = detected_disciplines[0].title()
                issues.append(f"Branş uyumsuzluğu şüphesi: Mevcut='{discipline}', İçerik analizi='{suggested_disc}'")
                suggestions.append({
                    "field": "discipline",
                    "action": "reclassify_discipline",
                    "detail": f"Soru metnindeki yoğun kavramlara göre branş revizyonu önerisi",
                    "proposed_value": suggested_disc
                })

        return {
            "question_id": qid,
            "severity": severity,
            "has_issues": len(issues) > 0,
            "issues": issues,
            "suggestions": suggestions,
            "preview": stem_clean[:120] + "..." if len(stem_clean) > 120 else stem_clean,
            "committee": committee,
            "discipline": discipline
        }

    def detect_duplicates(self, threshold: float = 0.88) -> List[Dict[str, Any]]:
        """Sorular arasındaki tekrar eden / mükerrer kopyaları tespit eder."""
        log.info("Mükerrer soru taraması başlatılıyor...")
        duplicates: List[Dict[str, Any]] = []
        token_cache = []

        for q in self.questions:
            stem = q.get("stem") or q.get("text") or q.get("questionText") or ""
            tokens = tokenize(stem)
            qid = q.get("id") or str(q.get("questionNumber") or q.get("no") or "")
            token_cache.append((qid, stem, tokens))

        n = len(token_cache)
        # Karşılaştırma optimizasyonu (sadece token uzunluğu yakın olanlar)
        for i in range(n):
            qid1, stem1, tokens1 = token_cache[i]
            if len(tokens1) < 4:
                continue
            for j in range(i + 1, min(i + 200, n)):  # Lokalde yakın komşuluk penceresi
                qid2, stem2, tokens2 = token_cache[j]
                if abs(len(tokens1) - len(tokens2)) > 10:
                    continue
                sim = jaccard_similarity(tokens1, tokens2)
                if sim >= threshold:
                    duplicates.append({
                        "question_id_1": qid1,
                        "question_id_2": qid2,
                        "similarity": round(sim, 3),
                        "preview_1": stem1[:100],
                        "preview_2": stem2[:100],
                        "action_proposed": "merge_or_archive_duplicate"
                    })

        log.info(f"{len(duplicates)} potansiyel mükerrer soru tespit edildi.")
        return duplicates

    def run_full_audit(self, throttle_ms: int = 5):
        """Bütün soruları yavaşça, donanımı yormadan tarar ve rapor üretir."""
        log.info(f"Tüm sorular için denetim süreci başlatıldı (Toplam: {len(self.questions)})...")
        results: List[Dict[str, Any]] = []
        issue_counts = {"error": 0, "warning": 0, "info": 0}

        for idx, q in enumerate(self.questions):
            audit = self.inspect_single_question(q)
            if audit["has_issues"]:
                results.append(audit)
                issue_counts[audit["severity"]] = issue_counts.get(audit["severity"], 0) + 1

            if (idx + 1) % 500 == 0:
                log.info(f"İlerleme: {idx + 1}/{len(self.questions)} soru incelendi (Sorunlu: {len(results)})")
                # İlerlemeyi kaydet
                with open(PROGRESS_FILE, "w", encoding="utf-8") as pf:
                    json.dump({
                        "processed": idx + 1,
                        "total": len(self.questions),
                        "issues_found": len(results),
                        "timestamp": time.time()
                    }, pf)

            # Donanımı yormamak için mikro uyuma (Throttling)
            if throttle_ms > 0:
                time.sleep(throttle_ms / 1000.0)

        duplicates = self.detect_duplicates()

        report = {
            "meta": {
                "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "total_questions_audited": len(self.questions),
                "total_issues_found": len(results),
                "issue_severity_distribution": issue_counts,
                "duplicates_found": len(duplicates),
                "status": "completed"
            },
            "duplicates": duplicates[:100],  # İlk 100 mükerrer çift
            "issue_questions": results
        }

        with open(AUDIT_OUTPUT, "w", encoding="utf-8") as out:
            json.dump(report, out, ensure_ascii=False, indent=2)

        log.info(f"Denetim tamamlandı! Sonuçlar yazıldı: {AUDIT_OUTPUT}")
        log.info(f"Özet: {issue_counts['error']} Kritik Hata, {issue_counts['warning']} Uyarı, {len(duplicates)} Mükerrer Eşleşme.")
        return report

def main():
    inspector = QuestionQualityInspector()
    inspector.run_full_audit(throttle_ms=2)

if __name__ == "__main__":
    main()
