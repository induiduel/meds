#!/usr/bin/env python3
"""Quiz Motoru Pipeline Entegrasyon ve Köprü Modülü.

Sesli ders ile Quiz motoru arasındaki sıralı (sequential) iş akışını yönetir.
Çakışma, mükerrer analiz ve yarış durumlarını (race condition) engeller.
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from kapsam import quiz_etkin_mi, sesli_ders_tamamlandi_mi
from envanter_genislet import envanter_derle


def pipeline_kos(taslak_klasor: Path, ders_id: str = None, brans: str = None, kuru: bool = False) -> int:
    """Tek bir ders taslağı için sıralı Quiz hattını çalıştırır."""
    if not taslak_klasor.exists():
        print(f"HATA: Taslak klasörü bulunamadı: {taslak_klasor}")
        return 1

    # Bilgileri oku
    baglam_dosya = taslak_klasor / "baglam.json"
    ders_paketi_dosya = taslak_klasor / "ders_paketi.json"
    
    dp = json.loads(ders_paketi_dosya.read_text()) if ders_paketi_dosya.exists() else {}
    baglam = json.loads(baglam_dosya.read_text()) if baglam_dosya.exists() else {}

    ders_id = ders_id or dp.get("id") or baglam.get("ders_id") or taslak_klasor.name
    brans = brans or dp.get("ders") or baglam.get("program", {}).get("ders") or "Tıbbi Farmakoloji"

    print(f"\n--- [QUIZ MOTORU PİPELİNE] Başlatılıyor: {ders_id} ({brans}) ---")

    # Faz 1: Kapsam Kilidi Kontrolü (Scope Lock)
    if not quiz_etkin_mi(brans):
        print(f"ℹ Faz 1 Kapsam Kilidi: '{brans}' dersi için Quiz üretimi şu an aktif değil (yalnızca Farmakoloji). Atlanıyor.")
        return 0

    print("✔ Faz 1: Kapsam Kilidi Doğrulandı (Farmakoloji aktif).")

    # Faz 3: Öncelik Kilidi (Sesli Ders Tamamlanma Kontrolü)
    if not sesli_ders_tamamlandi_mi(ders_id, taslak_klasor):
        print(f"⛔ Faz 3 Öncelik Kilidi: {ders_id} için Sesli Ders (Audio Lesson) henüz COMPLETED durumunda değil! Quiz üretimi kilitlendi.")
        return 75  # Hata / Bekletme kodu

    print("✔ Faz 3: Sesli Ders Tamamlanma Kilidi Doğrulandı (COMPLETED).")

    # Faz 2: Birleştirilmiş Derin Analiz (Atomik Bilgi Envanteri)
    envanter_dosya = taslak_klasor / "atomik_bilgi_envanteri.json"
    if not envanter_dosya.exists():
        print("▶ Faz 2: Atomik Bilgi Envanteri derleniyor (Single Source of Truth)...")
        if not kuru:
            try:
                envanter_derle(taslak_klasor)
                print("✔ Faz 2: Atomik Bilgi Envanteri hazırlandı.")
            except Exception as e:
                print(f"HATA (Faz 2 Envanter): {e}")
                return 2
    else:
        print("✔ Faz 2: Atomik Bilgi Envanteri zaten mevcut (Mükerrer analiz önlendi).")

    # Faz 4: Otomatik Quiz Havuzu Üretimi (Batch Processing)
    quiz_dosya = taslak_klasor / "quiz_havuzu.json"
    talimat_dosya = Path(__file__).resolve().parent / "TALIMAT_QUIZ.md"
    dogrula_betik = Path(__file__).resolve().parent / "quiz_dogrula.py"

    if quiz_dosya.exists():
        print("▶ Mevcut Quiz Havuzu doğrulanıyor...")
        r = subprocess.run([sys.executable, str(dogrula_betik), str(quiz_dosya), str(taslak_klasor)])
        if r.returncode == 0:
            print("✔ Quiz Havuzu mevcut ve 0 HATA ile doğrulandı.")
            return 0
        else:
            print("⚠ Mevcut Quiz Havuzu hatalı, yeniden üretilecek.")

    print(f"▶ Faz 4: Quiz Üretim Ajanı tetiklenebilir (Talimat: {talimat_dosya.name})")
    print(f"   (Ajan atomik_bilgi_envanteri.json üzerinden N -> 2N batch processing ile quiz_havuzu.json üretecek)")

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Quiz Motoru Pipeline Köprüsü")
    parser.add_argument("taslak", type=Path, help="Ders taslak klasörü yolu")
    parser.add_argument("--ders", type=str, help="Ders kimliği")
    parser.add_argument("--brans", type=str, help="Branş adı")
    parser.add_argument("--kuru", action="store_true", help="Kuru çalıştırma")

    args = parser.parse_args()
    sys.exit(pipeline_kos(args.taslak, args.ders, args.brans, args.kuru))
