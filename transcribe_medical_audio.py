#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MedSoru - Tıbbi Amfi Ses Kayıtları Transkripsiyon ve Ders Eşleştirme Motoru
=============================================================================
Karabük Üniversitesi Tıp Fakültesi ve Tıbbi Literatür Uyumlu Gemini Transkript Motoru

Özellikler:
1. Google Drive veya Yerel Klasördeki ses kayıtlarını (.m4a, .mp3, .wav vb.) okur.
2. Gemini 3.8 Flash & 3.5 Flash-Lite multimodal API ve File API ile uzun ders kayıtlarını işler.
3. Tıp müfredatı ve 347 derslik özet kataloğu ile eşleştirme yapar;
   dosya adı ve ses içeriğinden Kurul, Disiplin, Ders Adı ve Öğretim Üyesini tespit eder.
4. Tıbbi terminoloji (Latince anatomik terimler, farmakoloji, patoloji, mikrobiyoloji)
   desteğiyle fonetik hataları (örn. 'üoloji' -> 'üroloji', 'saülığı' -> 'sağlığı') engeller.
5. Kota ve Hız Limiti Yönetimi (Rate Limiting, RPM/TPM koruması, 429 backoff ve model fallback).
6. İlerleme Kaydı (transcription_manifest.json): Yarım kalan işlemler kaldığı yerden devam eder.
7. Hem Yerel (Windows/Linux/Mac) hem de Online (Google Colab / Cloud) çalışabilir.
"""

import os
import sys
import json
import time
import re
import shutil
import tempfile
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional

# --- 1. RESMİ DÖNEM 3 TIP MÜFREDATI & KURUL BİLGİLERİ ---
OFFICIAL_COMMITTEES = [
    {
        "id": "donem3-kurul1",
        "code": "TIP 310",
        "name": "Ürogenital ve Obstetrik Kurulu",
        "disciplines": [
            "Tıbbi Patoloji", "Enfeksiyon Hastalıkları", "Üroloji", 
            "Tıbbi Genetik", "Halk Sağlığı", "Kadın Hastalıkları ve Doğum", "Tıbbi Farmakoloji"
        ],
        "instructors": [
            "Prof. Dr. Hikmet Keleş", "Dr. Öğr. Üyesi Rüveyda Korkmazer", "Uz. Dr. Merve Kaçar",
            "Dr. Öğr. Üyesi F. Şamil Uysal", "Doç. Dr. Özer Baran", "Dr. Öğr. Üyesi Salih Bürlükkara",
            "Dr. Öğr. Üyesi Serap Arslan", "Doç. Dr. Nergiz Sevinç", "Dr. Öğr. Üyesi Erkay Nacar",
            "Dr. Öğr. Üyesi Hilal Ezgi Türkmen", "Prof. Dr. Mehmet Özdemir"
        ]
    },
    {
        "id": "donem3-kurul2",
        "code": "TIP 320",
        "name": "Nöropsikiyatri Kurulu",
        "disciplines": [
            "Tıbbi Farmakoloji", "Psikiyatri", "Nöroloji", "Tıbbi Genetik",
            "Aile Hekimliği", "Beyin ve Sinir Cerrahisi", "Tıbbi Patoloji", "FTR", "Anesteziyoloji ve Reanimasyon"
        ],
        "instructors": [
            "Prof. Dr. Mehmet Özdemir", "Dr. Öğr. Üyesi Namık Bilici", "Doç. Dr. Zuhal Koç Apaydın",
            "Dr. Öğr. Üyesi Nefise Demir", "Dr. Öğr. Üyesi Pınar Durmaz", "Dr. Öğr. Üyesi İrfan Yavaş",
            "Dr. Öğr. Üyesi Serap Arslan", "Doç. Dr. Habibe İnci", "Doç. Dr. Aydın Sinan Apaydın"
        ]
    },
    {
        "id": "donem3-kurul3",
        "code": "TIP 330",
        "name": "Gastrointestinal Sistem Kurulu",
        "disciplines": [
            "Tıbbi Farmakoloji", "İç Hastalıkları", "Tıbbi Patoloji", 
            "Çocuk Sağlığı ve Hastalıkları", "Tıbbi Genetik", "Enfeksiyon Hastalıkları"
        ],
        "instructors": [
            "Prof. Dr. Mehmet Özdemir", "Dr. Öğr. Üyesi Namık Bilici", "Prof. Dr. Fatih Karataş",
            "Prof. Dr. Hikmet Keleş", "Prof. Dr. Eylem Sevinç", "Dr. Öğr. Üyesi Serap Arslan"
        ]
    },
    {
        "id": "donem3-kurul4",
        "code": "TIP 340",
        "name": "Dolaşım, Solunum ve Tümör Kurulu",
        "disciplines": [
            "Kardiyoloji", "Tıbbi Patoloji", "Tıbbi Farmakoloji", "Çocuk Sağlığı ve Hastalıkları",
            "Tıbbi Genetik", "Göğüs Hastalıkları", "Enfeksiyon Hastalıkları", "Kalp ve Damar Cerrahisi"
        ],
        "instructors": [
            "Prof. Dr. Orhan Önalan", "Prof. Dr. Yeşim Akın", "Prof. Dr. Hikmet Keleş",
            "Dr. Öğr. Üyesi Rabia Hande Avcı", "Doç. Dr. Erdem Çetin"
        ]
    },
    {
        "id": "donem3-kurul5",
        "code": "TIP 350",
        "name": "Ortopedi, Travmatoloji ve Hematopoetik Sistem Kurulu",
        "disciplines": [
            "Acil Tıp", "Tıbbi Patoloji", "Ortopedi ve Travmatoloji", "Halk Sağlığı",
            "FTR", "İç Hastalıkları", "Tıbbi Genetik", "Tıbbi Farmakoloji", "Çocuk Sağlığı ve Hastalıkları"
        ],
        "instructors": [
            "Doç. Dr. Bora Çekmen", "Prof. Dr. Uygar Daşar", "Doç. Dr. Yılmaz Ergişi",
            "Doç. Dr. Hatice Gülşah Karataş", "Dr. Öğr. Üyesi Ramazan Gündüz"
        ]
    },
    {
        "id": "donem3-kurul6",
        "code": "TIP 360",
        "name": "Endokrin, Metabolizma ve Yaşlanma Kurulu",
        "disciplines": [
            "İç Hastalıkları", "Halk Sağlığı", "Tıbbi Farmakoloji", "Tıbbi Biyokimya",
            "Tıbbi Genetik", "Tıbbi Patoloji", "Çocuk Sağlığı ve Hastalıkları", "Psikiyatri"
        ],
        "instructors": [
            "Prof. Dr. Fatih Karataş", "Prof. Dr. Tahir Kahraman", "Prof. Dr. Eyüp Altınöz",
            "Prof. Dr. Mehmet Özdemir", "Doç. Dr. Nergis Sevinç"
        ]
    }
]

# Tıbbi Kısaltma ve Yazım Düzeltme Sözlüğü
MEDICAL_ABBREVIATIONS = {
    "tbg": "Tıbbi Biyoloji ve Genetik (Tıbbi Genetik)",
    "hs": "Halk Sağlığı",
    "use": "Üriner Sistem Enfeksiyonları",
    "ftr": "Fiziksel Tıp ve Rehabilitasyon",
    "kvc": "Kalp ve Damar Cerrahisi",
    "k1": "Kurul 1", "k2": "Kurul 2", "k3": "Kurul 3",
    "k4": "Kurul 4", "k5": "Kurul 5", "k6": "Kurul 6",
}

TYPO_CORRECTIONS = {
    "üoloji": "üroloji", "uoloji": "üroloji",
    "saülığı": "sağlığı", "sauiligi": "sağlığı",
    "genetşk": "genetik", "genetsk": "genetik",
    "farmakolji": "farmakoloji", "patolji": "patoloji",
    "enfeksyon": "enfeksiyon",
}

def to_ascii_safe_name(name: str) -> str:
    """Türkçe karakterleri ASCII eşdeğerlerine çevirir (HTTP header güvenliği)."""
    tr_map = {
        "ı": "i", "İ": "I", "ğ": "g", "Ğ": "G",
        "ü": "u", "Ü": "U", "ş": "s", "Ş": "S",
        "ö": "o", "Ö": "O", "ç": "c", "Ç": "C"
    }
    for tr, asc in tr_map.items():
        name = name.replace(tr, asc)
    return re.sub(r"[^a-zA-Z0-9._-]", "_", name)

def clean_and_normalize_name(name: str) -> str:
    """Dosya adındaki yazım hatalarını ve kısaltmaları çözer."""
    base = Path(name).stem.lower()
    for typo, fix in TYPO_CORRECTIONS.items():
        base = re.sub(rf"\b{typo}\b", fix, base)
        base = base.replace(typo, fix)
    for abbr, full in MEDICAL_ABBREVIATIONS.items():
        base = re.sub(rf"\b{abbr}\b", full.lower(), base)
    return base

def find_lecture_candidate(filename: str, summaries_catalog: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Dosya adı üzerinden en olası kurul, disiplin ve ders başlığını bulur."""
    cleaned = clean_and_normalize_name(filename)
    
    # 1. Katalogda doğrudan eşleşme arayışı
    best_item = None
    best_score = 0
    words = [w for w in re.findall(r"\w+", cleaned) if len(w) > 2]

    for item in summaries_catalog:
        target_str = f"{item.get('discipline', '')} {item.get('title', '')} {' '.join(item.get('keyPoints', []))}".lower()
        score = sum(1 for w in words if w in target_str)
        if score > best_score:
            best_score = score
            best_item = item

    # 2. Kurul ve Disiplin Heuristiği
    matched_discipline = "Tıp Fakültesi"
    matched_committee = OFFICIAL_COMMITTEES[0] # Default Kurul 1

    for comm in OFFICIAL_COMMITTEES:
        for disc in comm["disciplines"]:
            if disc.lower() in cleaned:
                matched_discipline = disc
                matched_committee = comm
                break

    if best_item and best_score >= 2:
        return {
            "committeeId": best_item.get("committeeId", matched_committee["id"]),
            "kurul": best_item.get("kurul", 1),
            "discipline": best_item.get("discipline", matched_discipline),
            "suggestedTitle": best_item.get("title", Path(filename).stem),
            "keyPoints": best_item.get("keyPoints", []),
            "confidence": "high" if best_score >= 3 else "medium"
        }

    return {
        "committeeId": matched_committee["id"],
        "kurul": 1,
        "discipline": matched_discipline,
        "suggestedTitle": Path(filename).stem,
        "keyPoints": [],
        "confidence": "heuristic"
    }

# --- 2. GEMINI API ENTEGRASYONU ---
def get_gemini_client(api_key: Optional[str] = None):
    """Google GenAI istemcisini başlatır."""
    key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        # Check .env if exists
        for env_file in [".env", "../.env", str(Path.home() / ".env")]:
            if os.path.exists(env_file):
                with open(env_file, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("GEMINI_API_KEY="):
                            key = line.split("=", 1)[1].strip().strip('"').strip("'")
                            break
            if key:
                break

    if not key:
        print("\n❌ [Hata] GEMINI_API_KEY bulunamadı!")
        print("Lütfen şu komutla ortam değişkenini tanımlayın veya parametre olarak verin:")
        print("  Windows PowerShell: $env:GEMINI_API_KEY=\"AIzaSy...\"")
        print("  Linux/Mac/Colab:    export GEMINI_API_KEY=\"AIzaSy...\"")
        print("  Veya scripti çalıştırırken: python transcribe_medical_audio.py --gemini-key=\"AIzaSy...\"\n")
        sys.exit(1)

    try:
        from google import genai
        return genai.Client(api_key=key)
    except ImportError:
        print("\n❌ [Hata] 'google-genai' kütüphanesi yüklü değil!")
        print("Lütfen şu komutla en güncel resmi Gemini SDK'sını yükleyin:")
        print("  pip install -U google-genai\n")
        sys.exit(1)

def build_transcription_prompt(candidate: Dict[str, Any], filename: str) -> str:
    """Tıbbi literatür ve ders notlarıyla zenginleştirilmiş sistem istemi."""
    key_points_str = "\n".join([f"- {kp}" for kp in candidate.get("keyPoints", [])]) if candidate.get("keyPoints") else "Mevcut değil"
    
    return f"""Sen Tıp Fakültesi Dönem 3 amfi derslerini kaydeden ve tıbbi literatüre %100 sadık kalarak çözümleyen Kıdemli Tıp Fakültesi Öğretim Üyesi ve Klinik Transkripsiyon Uzmanısın.

SES KAYDI BİLGİLERİ:
- Dosya Adı: {filename}
- Ön Eşleştirme (Aday Ders): {candidate.get('suggestedTitle')}
- Ön Eşleştirme Disiplin: {candidate.get('discipline')}
- Ön Eşleştirme Kurul: Kurul {candidate.get('kurul')} ({candidate.get('committeeId')})
- Bilinen Tıbbi Alt Başlıklar:
{key_points_str}

GÖREVLERİN:
1. 【DERSİN GERÇEK KİMLİĞİNİ TESPİT ET】:
   Ses kaydının girişindeki selamlama, hocanın hitabı ve anlatılan patofizyolojik konulardan yola çıkarak;
   bu kaydın GERÇEKTE hangi Dönem 3 Kuruluna (Kurul 1-6), hangi Tıp Disiplinine (örn. Tıbbi Patoloji, Tıbbi Farmakoloji, Tıbbi Genetik, Üroloji, Halk Sağlığı vb.), hangi Ders Başlığına ve (mümkünse) hangi Öğretim Üyesine ait olduğunu KESİN olarak belirle.

2. 【TIBBİ LİTERATÜR VE TERMİNOLOJİYE %100 UYUM】:
   - Amfi derslerinde hocaların kullandığı Latince anatomik yapıları, fizyolojik/patolojik süreçleri, mikrobiyolojik etkenleri (cins ve tür adları eğik/tam yazım), sendrom adlarını ve farmakolojik etken maddeleri eksiksiz ve doğru tıp imlasıyla yaz.
   - Fonetik bozulmaları (örn. 'üroloji' yerine 'üoloji', 'karyotip' yerine 'karyotop', 'aminoglikozit' yerine 'aminoglikoz') düzelt.
   - Amfi gürültülerini, mikrofon cızırtılarını veya alakasız konuşmaları temizle, dersin akademik özünü koru.

3. 【YAPILANDIRILMIŞ VE EKSİKSİZ TRANSKRİPT】:
   - Başlıklar ve alt başlıklarla kronolojik olarak dersi çözümle.
   - Hocanın "Sınavda sorarım", "TUS'ta çıkar", "Burası çok önemli", "Yıldızlı bilgi" dediği klinik incileri (High-Yield Pearls) özel vurgulu kutu olarak öne çıkar.

ÇIKTI FORMATI (Markdown formatında olmalı, aşağıdaki yapıyı birebir koru):

# 🩺 [Tespit Edilen Resmi Ders Adı]

> **Kurul:** Kurul X - [Kurul Adı] (TIP XXX)  
> **Disiplin:** [Örn. Tıbbi Genetik / Üroloji / Tıbbi Patoloji]  
> **Öğretim Üyesi:** [Hocanın Adı veya 'Belirtilmedi']  
> **Kaynak Ses Kaydı:** `{filename}`  
> **Tespit Güveni:** [%95 - Doğrulandı]  

---

## 📌 Dersin Özeti ve Anahtar Kavramlar
[Dersin ana hatları ve işlenen temel kavramlar]

## ⭐ Amfi & Sınav Hap Bilgileri (High-Yield Pearls)
- **[Kavram 1]:** [Hocanın özellikle sınav için vurguladığı kritik nokta]
- **[Kavram 2]:** [Klinik/TUS ipucu]

---

## 📝 Ayrıntılı Ders Transkripti

### 1. [Bölüm / Konu Başlığı]
[Bu bölümde anlatılanların akıcı, tıbbi literatüre uygun, terimleri doğru yazılmış tam transkripti...]

### 2. [İkinci Konu Başlığı]
[...]

---
*Transkripsiyon MedSoru Gemini 3.8 Tıbbi Dil Motoru tarafından üretilmiştir.*
"""

def transcribe_audio_file(
    client, 
    audio_path: Path, 
    candidate: Dict[str, Any], 
    primary_model: str = "gemini-3.8-flash",
    delay_seconds: int = 8
) -> tuple[str, str]:
    """Tek bir ses dosyasını Gemini File API ile yükler ve transkribe eder."""
    print(f"\n🎙️  Ses Dosyası Yükleniyor: {audio_path.name} ({audio_path.stat().st_size / (1024*1024):.1f} MB)...")
    
    # ASCII güvenli geçici kopya oluştur
    ext = audio_path.suffix.lower()
    safe_stem = to_ascii_safe_name(audio_path.stem)
    temp_dir = tempfile.gettempdir()
    tmp_path = Path(temp_dir) / f"meds_py_{int(time.time())}_{safe_stem}{ext}"
    shutil.copyfile(str(audio_path), str(tmp_path))

    uploaded_file = None
    try:
        # 1. Dosyayı File API'ye yükle
        mime_type = "audio/mp4" if ext == ".m4a" else "audio/mpeg"
        uploaded_file = client.files.upload(
            file=str(tmp_path),
            config={"display_name": f"{safe_stem}{ext}", "mime_type": mime_type}
        )
        print(f"   ☁️  File API URI: {uploaded_file.uri} | Durum: {uploaded_file.state}")

        # 2. İşlenme durumunu kontrol et
        retries = 0
        while uploaded_file.state == "PROCESSING" and retries < 60:
            time.sleep(4)
            uploaded_file = client.files.get(name=uploaded_file.name)
            retries += 1
            sys.stdout.write(".")
            sys.stdout.flush()

        if uploaded_file.state != "ACTIVE":
            raise Exception(f"Ses dosyası hazır hale gelemedi. Durum: {uploaded_file.state}")

        print("\n   🧠 Gemini Tıbbi Akıl Yürütme ve Transkripsiyon Başlatılıyor...")
        prompt = build_transcription_prompt(candidate, audio_path.name)

        # 3. Model çağrısı (Quota 429 durumunda 3.5-flash-lite fallback)
        models_to_try = [primary_model]
        if primary_model != "gemini-3.5-flash-lite":
            models_to_try.append("gemini-3.5-flash-lite")

        transcript_text = ""
        used_model = primary_model

        for model_candidate in models_to_try:
            model_success = False
            for attempt in range(1, 3):
                try:
                    from google.genai import types
                    print(f"   ⚡ Model Çağrılıyor: {model_candidate} (Deneme {attempt})...")
                    response = client.models.generate_content(
                        model=model_candidate,
                        contents=[uploaded_file, prompt],
                        config=types.GenerateContentConfig(
                            temperature=0.2,
                            max_output_tokens=8192
                        )
                    )
                    transcript_text = response.text or ""
                    used_model = model_candidate
                    model_success = True
                    break
                except Exception as e:
                    err_msg = str(e)
                    is_quota = "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg
                    if is_quota:
                        print(f"   ⚠️ {model_candidate} kotası dolu (429)!")
                        if model_candidate != models_to_try[-1]:
                            print(f"   🔄 Yüksek kotalı alternatif modele geçiliyor: {models_to_try[1]}...")
                            break
                        wait_time = 35 * attempt
                        print(f"   ⏳ {wait_time} saniye bekleniyor...")
                        time.sleep(wait_time)
                    else:
                        raise e
            if model_success:
                break

        if not transcript_text:
            raise Exception("Model yanıtı boş döndü.")

        # 4. İki istek arası güvenlik beklemesi (RPM kotasını korumak için)
        print(f"   ⏱️  Kota güvenliği için {delay_seconds} saniye bekleniyor...")
        time.sleep(delay_seconds)

        return transcript_text, used_model

    finally:
        # Geçici dosyayı temizle
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except Exception:
                pass
        # Gemini Storage'dan sil (Kota temizliği)
        if uploaded_file:
            try:
                client.files.delete(name=uploaded_file.name)
                print("   🧹 Geçici dosya File API deposundan temizlendi.")
            except Exception:
                pass

def parse_markdown_metadata(md_text: str) -> Dict[str, Any]:
    """Üretilen markdown başlığından ders, kurul ve hoca bilgilerini parse eder."""
    meta = {
        "lecture_title": "",
        "committee": "",
        "discipline": "",
        "instructor": "",
        "confidence": ""
    }
    
    title_match = re.search(r"^#\s*🩺\s*(.+)$", md_text, re.MULTILINE)
    if title_match:
        meta["lecture_title"] = title_match.group(1).strip()

    kurul_match = re.search(r"\*\*Kurul:\*\*\s*(.+)", md_text)
    if kurul_match:
        meta["committee"] = kurul_match.group(1).strip()

    disc_match = re.search(r"\*\*Disiplin:\*\*\s*(.+)", md_text)
    if disc_match:
        meta["discipline"] = disc_match.group(1).strip()

    inst_match = re.search(r"\*\*Öğretim Üyesi:\*\*\s*(.+)", md_text)
    if inst_match:
        meta["instructor"] = inst_match.group(1).strip()

    conf_match = re.search(r"\*\*Tespit Güveni:\*\*\s*(.+)", md_text)
    if conf_match:
        meta["confidence"] = conf_match.group(1).strip()

    return meta

# --- 3. ANA ÇALIŞMA DÖNGÜSÜ ---
def main():
    parser = argparse.ArgumentParser(description="MedSoru Tıp Amfi Ses Kayıtları Transkripsiyon Motoru")
    parser.add_argument("--audio-dir", type=str, default="", help="Ses kayıtlarının bulunduğu yerel klasör")
    parser.add_argument("--output-dir", type=str, default="", help="Transkriptlerin kaydedileceği klasör")
    parser.add_argument("--gemini-key", type=str, default="", help="Google Gemini API Anahtarı")
    parser.add_argument("--model", type=str, default="gemini-3.8-flash", help="Kullanılacak Gemini modeli (Varsayılan: gemini-3.8-flash)")
    parser.add_argument("--delay", type=int, default=8, help="İstekler arası bekleme süresi (saniye)")
    parser.add_argument("--force", action="store_true", help="Daha önce transkribe edilmiş dosyaları yeniden işle")
    parser.add_argument("--limit", type=int, default=0, help="İşlenecek maksimum ses dosyası sayısı (0 = hepsi)")
    args = parser.parse_args()

    print("=================================================================")
    print("🩺 MedSoru - Tıbbi Amfi Ses Kayıtları Transkripsiyon Sistemi")
    print(f"🤖 Tercih Edilen Model: {args.model} (1M Token Çok Modlu)")
    print("=================================================================")

    # 1. Ses Klasörünü Belirle
    audio_dir_path = None
    if args.audio_dir and os.path.exists(args.audio_dir):
        audio_dir_path = Path(args.audio_dir)
    else:
        # Otomatik arama yolları
        candidates = [
            Path(r"C:\Users\indui\Desktop\Quick"),
            Path("./audio"),
            Path("../audio"),
            Path(r"C:\Users\indui\Desktop\meds_database\ses_kayitlari"),
            Path("/content/drive/MyDrive/Quick"),
            Path("/content/drive/MyDrive")
        ]
        for c in candidates:
            if c.exists() and any(c.glob("*.m4a")):
                audio_dir_path = c
                break

    if not audio_dir_path or not audio_dir_path.exists():
        print("❌ [Hata] Ses kayıtları klasörü bulunamadı!")
        print("Lütfen --audio-dir parametresiyle geçerli bir klasör belirtin:")
        print(r'  python transcribe_medical_audio.py --audio-dir="C:\Users\indui\Desktop\Quick"')
        sys.exit(1)

    print(f"📂 Ses Klasörü: {audio_dir_path}")

    # 2. Çıktı Klasörünü Belirle
    if args.output_dir:
        output_dir_path = Path(args.output_dir)
    else:
        output_dir_path = Path(r"C:\Users\indui\Desktop\meds_database\transcriptions")
        if not output_dir_path.parent.exists():
            output_dir_path = Path("./transcriptions")
    
    output_dir_path.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir_path / "transcription_manifest.json"
    print(f"💾 Çıktı Klasörü: {output_dir_path}")

    # 3. Ders Özetleri Kataloğunu Yükle
    summaries_catalog = []
    catalog_paths = [
        Path(r"C:\Users\indui\Desktop\meds\src\data\summaries_meta.json"),
        Path(r"C:\Users\indui\Desktop\meds_database\redakte_ozet_manifest.json"),
        Path("./summaries_meta.json")
    ]
    for cp in catalog_paths:
        if cp.exists():
            try:
                with open(cp, "r", encoding="utf-8") as f:
                    summaries_catalog = json.load(f)
                    print(f"📚 {len(summaries_catalog)} Tıp Dersi Özeti Kataloğu Yüklendi.")
                    break
            except Exception:
                pass

    # 4. Manifest / Önceki İşlem Kontrolü
    manifest = {}
    if manifest_path.exists() and not args.force:
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = json.load(f)
        except Exception:
            manifest = {}

    # 5. Ses Dosyalarını Listele
    supported_extensions = {".m4a", ".mp3", ".wav", ".aac", ".ogg", ".flac", ".mp4"}
    audio_files = [f for f in audio_dir_path.iterdir() if f.is_file() and f.suffix.lower() in supported_extensions]

    if not audio_files:
        print(f"⚠️  {audio_dir_path} içinde desteklenen formatta ses dosyası bulunamadı.")
        sys.exit(0)

    print(f"🎯 Bulunan Ses Kaydı Sayısı: {len(audio_files)}")

    # 6. Gemini Client Başlat
    client = get_gemini_client(args.gemini_key)

    processed_count = 0
    total_to_process = len(audio_files)

    for idx, audio_file in enumerate(audio_files, 1):
        if args.limit > 0 and processed_count >= args.limit:
            print(f"\n🛑 Limit sınırına ({args.limit}) ulaşıldı, işlem tamamlandı.")
            break

        file_id = audio_file.stem
        # Daha önce başarıyla tamamlanmış mı?
        if not args.force and file_id in manifest and manifest[file_id].get("status") == "completed":
            print(f"\n⏩ [{idx}/{total_to_process}] Zaten Transkribe Edilmiş (Atlanıyor): {audio_file.name}")
            continue

        print(f"\n=======================================================")
        print(f"▶️  [{idx}/{total_to_process}] İşleniyor: {audio_file.name}")
        print("=======================================================")

        # Aday ders eşleştirmesi
        candidate = find_lecture_candidate(audio_file.name, summaries_catalog)
        print(f"🔍 Ön Tespit: Kurul {candidate.get('kurul')} | {candidate.get('discipline')} | {candidate.get('suggestedTitle')}")

        try:
            # Transkripsiyon motorunu çağır
            transcript_md, used_model = transcribe_audio_file(
                client=client,
                audio_path=audio_file,
                candidate=candidate,
                primary_model=args.model,
                delay_seconds=args.delay
            )

            # Metadata parse et
            meta = parse_markdown_metadata(transcript_md)

            # Markdown dosyasını kaydet
            safe_title = to_ascii_safe_name(meta.get("lecture_title") or audio_file.stem)
            out_md_path = output_dir_path / f"{safe_title}_Transkript.md"
            with open(out_md_path, "w", encoding="utf-8") as f:
                f.write(transcript_md)

            print(f"✅ Transkript Kaydedildi: {out_md_path.name}")
            print(f"   🎓 Tespit Edilen Ders: {meta.get('lecture_title')} ({meta.get('discipline')})")
            print(f"   👨‍🏫 Öğretim Üyesi: {meta.get('instructor')} | Model: {used_model}")

            # Manifesti güncelle
            manifest[file_id] = {
                "audio_filename": audio_file.name,
                "file_size_mb": round(audio_file.stat().st_size / (1024 * 1024), 2),
                "markdown_file": out_md_path.name,
                "lecture_title": meta.get("lecture_title") or candidate.get("suggestedTitle"),
                "committee": meta.get("committee") or f"Kurul {candidate.get('kurul')}",
                "discipline": meta.get("discipline") or candidate.get("discipline"),
                "instructor": meta.get("instructor") or "Belirtilmedi",
                "confidence": meta.get("confidence") or candidate.get("confidence"),
                "model_used": used_model,
                "status": "completed",
                "processed_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }

            with open(manifest_path, "w", encoding="utf-8") as f:
                json.dump(manifest, f, ensure_ascii=False, indent=2)

            processed_count += 1

        except Exception as e:
            print(f"❌ Hata oluştu ({audio_file.name}): {e}")
            manifest[file_id] = {
                "audio_filename": audio_file.name,
                "status": "error",
                "error_message": str(e),
                "attempted_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            with open(manifest_path, "w", encoding="utf-8") as f:
                json.dump(manifest, f, ensure_ascii=False, indent=2)

    print("\n=======================================================")
    print(f"🎉 İşlem Tamamlandı! Toplam {processed_count} yeni ses kaydı transkribe edildi.")
    print(f"📁 Transkriptler: {output_dir_path}")
    print(f"📋 Manifest: {manifest_path}")
    print("=======================================================")

if __name__ == "__main__":
    main()
