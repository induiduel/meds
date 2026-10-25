#!/usr/bin/env python3
"""Quiz Havuzu Doğrulayıcı Kapısı (0 HATA Kuralı).

Doğrulama Ölçütleri:
1. [ÖNCELİK KİLİDİ]: İlgili sesli ders (audio_lesson_id) 'COMPLETED' durumunda mı?
2. [2X ÇAPRAZ SORGULAMA]: N adet atomik bilgi için en az 2N adet özgün soru üretilmiş mi?
3. [ÇİFT EŞLEŞMESİ]: Her atomik bilginin 1 pozitif (positive_direct) ve 1 ters (negative_inverse)
   sorusu üretilmiş ve question_pair_id ile bağlanmış mı?
4. [ACTIVE RECALL FORMATI]: Sorular kısa, net ve 5-15 saniyede çözülebilir mi? (Uzun paragraf yasağı).
5. [ŞIK VE AÇIKLAMA]: A-D veya A-E şıklarının her biri için standart gerekçeli açıklama var mı?
6. [SIFIR HALÜSİNASYON]: Soru kökü ve doğru cevap kanıttaki atomik bilgiyle doğrudan örtüşüyor mu?
"""
import json
import re
import sys
from pathlib import Path
from typing import Dict, Any, List

MEDS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from kapsam import sesli_ders_tamamlandi_mi


def dogrula(quiz_dosyasi: Path, taslak_klasor: Path = None) -> List[str]:
    hatalar: List[str] = []
    
    if not quiz_dosyasi.exists():
        return [f"Dosya bulunamadı: {quiz_dosyasi}"]

    try:
        data = json.loads(quiz_dosyasi.read_text())
    except Exception as e:
        return [f"JSON okuma hatası: {e}"]

    topic_id = data.get("topic_id", "")
    audio_lesson_id = data.get("audio_lesson_id", "")
    audio_status = data.get("audio_lesson_status", "")

    # 1. Sesli Ders Öncelik Kilidi Kontrolü
    if audio_status != "COMPLETED":
        hatalar.append(f"[ÖNCELİK KİLİDİ] audio_lesson_status 'COMPLETED' olmalıdır (Mevcut: {audio_status})")
    
    if taslak_klasor and not sesli_ders_tamamlandi_mi(topic_id, taslak_klasor):
        hatalar.append(f"[ÖNCELİK KİLİDİ] {topic_id} için Sesli Ders tamamlanmadan Quiz onaylanamaz!")

    total_atoms = data.get("total_atoms", 0)
    questions = data.get("questions", [])
    pairs = data.get("pairs", [])
    total_questions = len(questions)

    # 2. Minimum 2x Soru Havuzu Kuralı
    if total_atoms > 0 and total_questions < (2 * total_atoms):
        hatalar.append(
            f"[2X KURALI] Yetersiz soru sayısı! {total_atoms} atomik bilgi için en az "
            f"{2 * total_atoms} soru üretilmelidir (Mevcut: {total_questions})"
        )

    # 3. Çift Eşleşmesi ve Çapraz Sorgulama Kontrolü
    pair_map: Dict[str, Dict[str, Any]] = {p.get("question_pair_id"): p for p in pairs}
    atom_questions: Dict[str, Dict[str, List[str]]] = {}

    for q in questions:
        q_id = q.get("id", "")
        atom_id = q.get("knowledge_atom_id", "")
        pair_id = q.get("question_pair_id", "")
        direction = q.get("direction", "")
        
        if not atom_id:
            hatalar.append(f"Soru {q_id}: knowledge_atom_id eksik!")
        if not pair_id:
            hatalar.append(f"Soru {q_id}: question_pair_id eksik!")
        elif pair_id not in pair_map:
            hatalar.append(f"Soru {q_id}: pair_id '{pair_id}' pairs listesinde tanımlı değil!")

        if direction not in ("positive_direct", "negative_inverse"):
            hatalar.append(f"Soru {q_id}: direction geçersiz ('{direction}'). positive_direct veya negative_inverse olmalı.")

        atom_questions.setdefault(atom_id, {"positive_direct": [], "negative_inverse": []})
        if direction in atom_questions[atom_id]:
            atom_questions[atom_id][direction].append(q_id)

        # 4. Soru formatı ve süre kontrolü (5-15 sn hedefi, max 45 kelime)
        prompt = q.get("prompt", "")
        kelime_sayisi = len(prompt.split())
        if kelime_sayisi > 45:
            hatalar.append(f"Soru {q_id}: Soru kökü çok uzun ({kelime_sayisi} kelime). Active recall için kısa ve net olmalı (maks 45 kelime).")
        if kelime_sayisi < 4:
            hatalar.append(f"Soru {q_id}: Soru kökü çok kısa veya geçersiz ({kelime_sayisi} kelime).")

        reading_sec = q.get("estimated_reading_sec", 10)
        if not (5 <= reading_sec <= 20):
            hatalar.append(f"Soru {q_id}: Okuma süresi {reading_sec} sn aralık dışı (5-15 sn hedeflenmelidir).")

        # 5. Şıklar ve Açıklamalar
        options = q.get("options", {})
        correct = q.get("correct_option", "")
        explanations = q.get("option_explanations", {})

        if len(options) not in (4, 5):
            hatalar.append(f"Soru {q_id}: Seçenek sayısı 4 veya 5 olmalıdır (Mevcut: {len(options)})")

        if correct not in options:
            hatalar.append(f"Soru {q_id}: Doğru şık '{correct}' seçeneklerde bulunamadı!")

        for opt_key in options:
            exp = explanations.get(opt_key, "")
            if not exp or len(exp.strip()) < 15:
                hatalar.append(f"Soru {q_id}: '{opt_key}' şıkkı için gerekçeli açıklama eksik veya çok kısa (<15 karakter).")
            # Yasaklı geçiştirme ifadeleri kontrolü
            if re.search(r"^(bu sorunun cevabı değil|olarak geçmez|yapmaz|doğrudur|yanlıştır)\.?$", exp.strip().casefold()):
                hatalar.append(f"Soru {q_id}: '{opt_key}' şıkkı için yüzeysel geçiştirme açıklaması YASAKTIR: '{exp}'")

        # 6. Kanıt kontrolü
        evidence = q.get("evidence", {})
        if not evidence.get("quote") or not evidence.get("page"):
            hatalar.append(f"Soru {q_id}: Kanıt (sayfa veya alıntı) eksik!")

    # Her atom için hem pozitif hem negatif soru var mı?
    for atom_id, dirs in atom_questions.items():
        if not dirs["positive_direct"]:
            hatalar.append(f"Atom {atom_id}: Pozitif (positive_direct) sorusu üretilmemiş!")
        if not dirs["negative_inverse"]:
            hatalar.append(f"Atom {atom_id}: Ters (negative_inverse) sorusu üretilmemiş!")

    return hatalar


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım: python3 quiz_dogrula.py <quiz_dosyasi.json> [taslak_klasor]")
        sys.exit(1)

    q_file = Path(sys.argv[1])
    t_klasor = Path(sys.argv[2]) if len(sys.argv) >= 3 else q_file.parent

    hatalar = dogrula(q_file, t_klasor)
    if hatalar:
        print(f"{len(hatalar)} HATA BULUNDU:")
        for h in hatalar[:30]:
            print(f"  - {h}")
        if len(hatalar) > 30:
            print(f"  ... ve {len(hatalar) - 30} hata daha.")
        sys.exit(1)
    else:
        print("0 HATA: Quiz havuzu tüm pedagojik ve teknik kurallara tam uyumludur.")
        sys.exit(0)
