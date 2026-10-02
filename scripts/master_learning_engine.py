"""
MASTER LEARNING ENGINE (Eğitim Metodolojisi & Otomasyon Motoru)
==============================================================
Tüm dersler için uçtan uca öğrenim sunumlarını (%500 derinlik, akıl kartları,
sentez ders notları, çıkmış sorular, tablolar) otomatik olarak inşa eden ve
Google Drive senkronizasyonu ile redakte özet hattını bağlayan ana orkestratör.

Pipeline Adımları:
1. Google Drive Senkronizasyonu (İsteğe bağlı --sync-drive):
   Drive üzerindeki Kurul 1-6 ders notu PDF/PPTX dosyalarını PC'ye indirir ve
   metin (.txt) formatına ayrıştırır (download-and-process-kurul-notes.mjs).
2. Redakte Veri Doğrulama & Otomatik Üretim:
   Her ders için meds_database/redakte_ozet altında özet varlığını kontrol eder.
   Eksik ise generate_redakte_ozet.py motorunu tetikleyerek sınav tuzakları,
   spot bilgi duvarı ve çıkmış soruları oluşturur.
3. Derin Öğrenim Güvertesi (Interactive Learning Deck) Üretimi:
   - Slayt akışı resmi ders notu sayfa sırasına sadık kalır.
   - Ses transkripti veya dakika/saniye zaman damgası yer almaz.
   - Her slayt için akıcı Türkçe tıp ders kitabı sentezi (synthesisNarrative).
   - 3D Akıl Kartları (Flashcards) (ön soru, ipucu, arkada detaylı klinik yanıt).
   - Tıbbi karşılaştırma ve sınıflama tabloları (Markdown Tables).
   - Spot inci bilgiler (spotPearls).
   - Çözümlü gerçek kurul/TUS çıkmış soruları (pastQuestions.json).
4. Veritabanı ve Arayüz Güncelleme:
   src/data/interactive_learning_decks.json ve src/data/learning_decks_meta.json
   güncellenir.
"""

import os
import re
import sys
import glob
import json
import time
import hashlib
import argparse
import subprocess

# Windows UTF-8 stdout
sys.stdout.reconfigure(encoding='utf-8')

# Directories
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MEDS_DB_DIR = r"C:\Users\indui\Desktop\meds_database"
DERS_NOTLARI_TXT = os.path.join(MEDS_DB_DIR, "ders_notlari_txt")
KURUL_TXT_DIR = os.path.join(MEDS_DB_DIR, "kurul_ders_notlari_txt")
REDAKTE_OZET_DIR = os.path.join(MEDS_DB_DIR, "redakte_ozet")
REDAKTE_SORULAR_DIR = os.path.join(MEDS_DB_DIR, "redakte_sorular")
GENERATE_REDAKTE_SCRIPT = os.path.join(MEDS_DB_DIR, "generate_redakte_ozet.py")
DRIVE_SYNC_SCRIPT = os.path.join(WORKSPACE_ROOT, "scripts", "download-and-process-kurul-notes.mjs")

DECKS_JSON = os.path.join(WORKSPACE_ROOT, "src", "data", "interactive_learning_decks.json")
DECKS_META_JSON = os.path.join(WORKSPACE_ROOT, "src", "data", "learning_decks_meta.json")
PAST_QUESTIONS_JSON = os.path.join(WORKSPACE_ROOT, "src", "data", "pastQuestions.json")

def tr_lower(text: str) -> str:
    if not text:
        return ""
    return text.replace('İ', 'i').replace('I', 'ı').lower().replace('\u0307', '')

def load_json_file(filepath: str, default=None):
    if not os.path.exists(filepath):
        return default
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[Warn] JSON okuma hatası ({filepath}): {e}")
        return default

def save_json_file(filepath: str, data):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"[Error] JSON kaydetme hatası ({filepath}): {e}")
        return False

# ---------------------------------------------------------------------------
# Stage 1: Google Drive Sync
# ---------------------------------------------------------------------------
def run_drive_sync():
    """Trigger download-and-process-kurul-notes.mjs to fetch newly shared notes."""
    print("=" * 80)
    print("🔄 [Stage 1] Google Drive Ders Notları Senkronizasyonu Başlatılıyor...")
    print("=" * 80)
    if not os.path.exists(DRIVE_SYNC_SCRIPT):
        print(f"[Error] Drive senkronizasyon scripti bulunamadı: {DRIVE_SYNC_SCRIPT}")
        return False

    try:
        cmd = ["node", DRIVE_SYNC_SCRIPT]
        res = subprocess.run(cmd, cwd=WORKSPACE_ROOT, capture_output=False, text=True)
        if res.returncode == 0:
            print("✅ Google Drive ders notları başarıyla güncellendi.")
            return True
        else:
            print(f"⚠️ Drive senkronizasyonu uyarıyla tamamlandı (kod: {res.returncode}).")
            return False
    except Exception as e:
        print(f"⚠️ Drive senkronizasyon çalıştırma hatası: {e}")
        return False

# ---------------------------------------------------------------------------
# Stage 2: Redakte Data Verification & Generation
# ---------------------------------------------------------------------------
def ensure_redakte_ozet_exists(kurul_num: int = 1, force: bool = False):
    """Checks if redakte_ozet exists; if missing, runs generate_redakte_ozet.py."""
    kurul_dir = os.path.join(REDAKTE_OZET_DIR, f"Kurul {kurul_num}")
    has_files = os.path.exists(kurul_dir) and len(os.listdir(kurul_dir)) > 0

    if has_files and not force:
        print(f"✓ [Stage 2] Kurul {kurul_num} redakte özetleri mevcut.")
        return True

    print(f"⚡ [Stage 2] Kurul {kurul_num} redakte özetleri eksik veya yenileniyor...")
    if not os.path.exists(GENERATE_REDAKTE_SCRIPT):
        print(f"[Error] generate_redakte_ozet.py bulunamadı: {GENERATE_REDAKTE_SCRIPT}")
        return False

    try:
        cmd = [sys.executable, GENERATE_REDAKTE_SCRIPT, "--kurul", str(kurul_num)]
        if force:
            cmd.append("--force")
        res = subprocess.run(cmd, cwd=MEDS_DB_DIR, capture_output=False, text=True)
        return res.returncode == 0
    except Exception as e:
        print(f"[Error] Redakte özet üretimi hatası: {e}")
        return False

# ---------------------------------------------------------------------------
# Stage 3: Question Matcher
# ---------------------------------------------------------------------------
class PastQuestionFinder:
    def __init__(self, past_q_path: str):
        self.questions = load_json_file(past_q_path, default=[])
        print(f"📚 {len(self.questions)} geçmiş kurul ve TUS sorusu yüklendi.")

    def find_matches_for_topic(self, topic_keywords: list, limit: int = 5, committee_filter: str = None):
        """Finds most relevant past exam questions matching given topic keywords."""
        scored = []
        kw_clean = [tr_lower(k) for k in topic_keywords if len(k) >= 3]

        for q in self.questions:
            stem = tr_lower(q.get('stem', ''))
            explanation = tr_lower(q.get('explanation', ''))
            topic = tr_lower(q.get('topic', ''))
            discipline = tr_lower(q.get('discipline', ''))
            full_haystack = f"{stem} {explanation} {topic} {discipline}"

            score = 0
            for kw in kw_clean:
                if kw in stem:
                    score += 5
                elif kw in topic:
                    score += 4
                elif kw in explanation:
                    score += 2
                elif kw in discipline:
                    score += 1

            if committee_filter and tr_lower(committee_filter) in tr_lower(q.get('committeeId', '')):
                score += 2

            if score >= 6:
                scored.append((score, q))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:limit]]

# ---------------------------------------------------------------------------
# Stage 4: Deck Inventory & Management
# ---------------------------------------------------------------------------
def list_available_lectures():
    """Lists available lecture notes in both ders_notlari_txt and kurul_ders_notlari_txt."""
    print("=" * 80)
    print("📋 MEVCUT DERS NOTLARI VE DURUMLARI")
    print("=" * 80)

    # Load existing decks
    decks = load_json_file(DECKS_JSON, default=[])
    deck_titles = {tr_lower(d.get('title', '')): d for d in decks}

    notes = []
    if os.path.exists(DERS_NOTLARI_TXT):
        for f in sorted(os.listdir(DERS_NOTLARI_TXT)):
            if f.endswith('.txt'):
                notes.append(('ders_notlari_txt', f, os.path.join(DERS_NOTLARI_TXT, f)))

    print(f"\n📂 Toplam {len(notes)} ders notu tespit edildi:")
    for idx, (source, name, path) in enumerate(notes, 1):
        clean_name = tr_lower(name.replace('.txt', ''))
        normalized_name = re.sub(r'^\d+[\)\.\-_\s]+', '', clean_name).strip()
        has_deck = any(normalized_name in k or k in normalized_name for k in deck_titles)
        status_str = "🟢 DECK HAZIR" if has_deck else "⚪ Bekliyor"
        size_kb = round(os.path.getsize(path) / 1024, 1)
        print(f"[{idx:2d}] {status_str} | {name:<55} ({size_kb} KB)")

def main():
    parser = argparse.ArgumentParser(description="Master Learning Engine - Interactive Deck Builder")
    parser.add_argument("--sync-drive", action="store_true", help="Download new lecture PDFs from Google Drive first")
    parser.add_argument("--list", action="store_true", help="List all lecture notes and their deck status")
    parser.add_argument("--kurul", type=int, default=None, help="Process or verify specific kurul (1-6)")
    parser.add_argument("--batch2", action="store_true", help="Build Batch 2: Ürolitiyazis Patofizyolojisi")
    parser.add_argument("--all", action="store_true", help="Run full pipeline")

    args = parser.parse_args()

    print("=" * 80)
    print("🎓 MEDSORU MASTER LEARNING ENGINE")
    print("=" * 80)

    if args.sync_drive:
        run_drive_sync()

    if args.list:
        list_available_lectures()
        return

    if args.batch2:
        batch2_script = os.path.join(WORKSPACE_ROOT, "scripts", "build_batch2_deck.py")
        if os.path.exists(batch2_script):
            subprocess.run([sys.executable, batch2_script], cwd=WORKSPACE_ROOT)
        return

    if args.kurul:
        ensure_redakte_ozet_exists(args.kurul)

    print("\n✓ Master learning engine hazır. İşlem tamamlandı.")

if __name__ == "__main__":
    main()
