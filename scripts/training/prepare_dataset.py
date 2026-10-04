#!/usr/bin/env python3
"""
MedSoru Özel Tıp Yapay Zekası İçin İnce Ayar (Fine-Tuning) Veri Seti Hazırlayıcı.
Kaynak: meds_database/questions (v2_local_pipeline_2026 etiketli doğrulanmış veriler)
Çıktı : meds/training_data/medsoru_train.jsonl (Alpaca / ChatML formatında)
"""
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DB_QUESTIONS = ROOT / "meds_database" / "questions"
OUT_DIR = ROOT / "meds" / "training_data"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT_DIR / "medsoru_train.jsonl"

SYSTEM_PROMPT = (
    "Sen tıp fakültesi Dönem 3 kurulları ve sınavları konusunda uzmanlaşmış akademik bir tıp asistanısın. "
    "Ders notları ve amfi slaytları doğrultusunda soruları analiz eder, doğru cevabı açıklar ve tıp öğrencisine klinik/patolojik mantığını öğretirsin."
)

def format_options(opts: dict) -> str:
    return "\n".join(f"{k}) {v}" for k, v in sorted(opts.items()))

def main():
    if not DB_QUESTIONS.exists():
        print("meds_database/questions henüz hazır değil.")
        return

    records = []
    for qf in DB_QUESTIONS.glob("*.jsonl"):
        for line in qf.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                q = json.loads(line)
            except Exception:
                continue

            # Yalnızca yeni boru hattının doğruladığı veya kanıtlı soruları al
            if q.get("status") in ["verified", "fixed"] and q.get("evidence"):
                stem = q.get("stem_detailed") or q.get("stem", "").strip()
                opts_str = format_options(q.get("options", {}))
                ans = q.get("answer", "")
                exp = q.get("explanation") or "Ders notu ve kurul slaytları doğrultusunda bu seçenek teyit edilmiştir."
                tax = q.get("taxonomy_metadata", {})
                
                # Format 1: Sınav Sorusu Çözme & Gerekçelendirme
                user_input = f"{stem}\n\nŞıklar:\n{opts_str}"
                assistant_response = f"Doğru Cevap: {ans}\n\nAçıklama ve Slayt Kanıtı:\n{exp}"
                if tax.get("ne_sormus"):
                    assistant_response += f"\n\nSoru Analizi: Bu soru temel olarak {tax['ne_sormus']} konusunu ölçmektedir."

                records.append({
                    "instruction": SYSTEM_PROMPT,
                    "input": user_input,
                    "output": assistant_response
                })

                # Format 2: Hoca Tarzı Sentez & Konu Anlatımı
                if tax.get("alt_konu") and tax.get("ne_sormus"):
                    teach_input = f"Bana Dönem 3 {q.get('ders', 'Tıp')} dersindeki '{tax['alt_konu']}' konusunu ve sınavda çıkabilecek önemli noktaları açıkla."
                    teach_response = f"### {tax['alt_konu']} - Sınav Odaklı Özet\n\nBu konunun amfi slaytlarındaki kritik odağı: {tax['ne_sormus']}.\n\nÖnemli Klinik Bilgi:\n{exp}"
                    records.append({
                        "instruction": SYSTEM_PROMPT,
                        "input": teach_input,
                        "output": teach_response
                    })

    if records:
        with open(OUT_FILE, "w", encoding="utf-8") as f:
            for r in records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"Başarıyla {len(records)} adet eğitim örneği üretildi: {OUT_FILE}")
    else:
        print("Eğitim için henüz yeterli doğrulanmış soru birikmedi, boru hattı bekleniyor...")

if __name__ == "__main__":
    main()
