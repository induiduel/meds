#!/usr/bin/env python3
"""
Supabase Cloud -> meds_database & meds/data indirme ve akıllı birleştirme betiği.
- 4069 çıkmış soru, 885 ders notu, 24 komite ve 605 chunk'ı indirir.
- Mevcut yerel verileri ezmeden akıllı tekilleştirme (deduplication) yapar.
- Şema uyumlu hale getirip ilgili .jsonl ve .json dosyalarına birleştirir.
"""

import os
import re
import json
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://kgutsltgmqbnlxcnzrtl.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_SECRET_KEY", os.environ.get("SUPABASE_KEY", ""))

PROJECT_ROOT = Path("/home/indu/Masaüstü/MedSoru Project")
MEDS_DATABASE_DIR = PROJECT_ROOT / "meds_database"
DATA_DIR = PROJECT_ROOT / "meds" / "data"
EXPORT_DIR = MEDS_DATABASE_DIR / "backups" / "supabase_export"


def fetch_all_from_supabase(table_name: str, batch_size: int = 500):
    """Supabase REST API üzerinden sayfalamayla (pagination) tüm satırları çeker."""
    print(f"\n📡 '{table_name}' tablosu Supabase'den indiriliyor...")
    records = []
    offset = 0

    while True:
        end = offset + batch_size - 1
        url = f"{SUPABASE_URL}/rest/v1/{table_name}?select=*"
        req = urllib.request.Request(url, headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Range-Unit": "items",
            "Range": f"{offset}-{end}",
            "Prefer": "count=exact"
        })

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if not data:
                    break
                records.extend(data)
                content_range = resp.headers.get("Content-Range", "")
                print(f"  ✓ Çekildi: {len(records)} kayıt (Aralık: {offset}-{end} / Header: {content_range})")
                if len(data) < batch_size:
                    break
                offset += batch_size
        except Exception as e:
            print(f"  ❌ Hata ({table_name} @ {offset}): {e}")
            break

    print(f"  ✅ Toplam {len(records)} kayıt indirildi.")
    return records


def normalize_stem(stem: str) -> str:
    """Tekilleştirme için soru kökünü temizler ve normalize eder."""
    if not stem:
        return ""
    text = stem.strip().lower()
    text = re.sub(r'[\W_]+', '', text, flags=re.UNICODE)
    return text[:160]


def parse_donem_kurul(committee_id: str, raw_donem=None, raw_kurul=None):
    """committee_id veya ham veriden dönem ve kurul int/str değerlerini çıkarır."""
    donem = None
    kurul = None

    if raw_donem:
        d_m = re.search(r'(\d+)', str(raw_donem))
        if d_m:
            donem = int(d_m.group(1))

    if raw_kurul:
        k_m = re.search(r'(\d+)', str(raw_kurul))
        if k_m:
            kurul = int(k_m.group(1))
        else:
            kurul = str(raw_kurul).strip().lower()

    if committee_id and (donem is None or kurul is None):
        c_lower = str(committee_id).lower()
        if "donem1" in c_lower:
            donem = donem or 1
        elif "donem2" in c_lower:
            donem = donem or 2
        elif "donem3" in c_lower:
            donem = donem or 3

        if "kurul1" in c_lower or "k1" in c_lower:
            kurul = kurul or 1
        elif "kurul2" in c_lower or "k2" in c_lower:
            kurul = kurul or 2
        elif "kurul3" in c_lower or "k3" in c_lower:
            kurul = kurul or 3
        elif "kurul4" in c_lower or "k4" in c_lower:
            kurul = kurul or 4
        elif "kurul5" in c_lower or "k5" in c_lower:
            kurul = kurul or 5
        elif "kurul6" in c_lower or "k6" in c_lower:
            kurul = kurul or 6
        elif "final" in c_lower:
            kurul = kurul or "final"
        elif "but" in c_lower:
            kurul = kurul or "but"

    return donem or 3, kurul or "genel"


def format_options(options_obj):
    """Seçenekleri {'A': '...', 'B': '...'} formatına dönüştürür."""
    if isinstance(options_obj, dict):
        return options_obj
    if isinstance(options_obj, list):
        res = {}
        for item in options_obj:
            if isinstance(item, dict):
                k = item.get("key") or item.get("label") or item.get("option")
                v = item.get("text") or item.get("value") or ""
                if k:
                    res[str(k).upper().strip()] = str(v).strip()
            elif isinstance(item, str):
                m = re.match(r'^([A-Ea-e])[\.\)\:\s]+(.*)', item)
                if m:
                    res[m.group(1).upper()] = m.group(2).strip()
        return res
    return {}


def main():
    print("=" * 60)
    print("🏥 MedSoru: Supabase Cloud -> Yerel Database Birleştirme")
    print("=" * 60)

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    now_iso = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    # 1. Supabase'den tabloları çek ve ham yedeğe kaydet
    tables_to_sync = ["committees", "lecture_notes", "past_questions", "rag_chunks"]
    raw_data = {}

    for t in tables_to_sync:
        records = fetch_all_from_supabase(t)
        raw_data[t] = records
        export_file = EXPORT_DIR / f"{t}.json"
        export_file.write_text(json.dumps(records, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  💾 Ham yedek kaydedildi: {export_file}")

    # 2. Mevcut yerel soruları yükle ve indeksle
    local_questions_dir = MEDS_DATABASE_DIR / "questions"
    local_questions_dir.mkdir(parents=True, exist_ok=True)

    existing_stems = {}
    existing_ids = set()
    total_local_existing = 0

    local_files = list(local_questions_dir.glob("*.jsonl"))
    print(f"\n📂 Mevcut yerel dosyalar taranıyor ({len(local_files)} dosya)...")

    for f in local_files:
        for line in f.read_text(encoding="utf-8").splitlines():
            line_s = line.strip()
            if not line_s:
                continue
            try:
                q = json.loads(line_s)
                total_local_existing += 1
                qid = q.get("question_id") or q.get("id")
                if qid:
                    existing_ids.add(str(qid))
                stem_norm = normalize_stem(q.get("stem") or "")
                if stem_norm:
                    existing_stems[stem_norm] = str(qid)
            except Exception:
                pass

    print(f"  ✓ Yerelde mevcut soru sayısı: {total_local_existing}")

    # 3. Supabase'den gelen 4069 soruyu işle ve tekilleştir
    print("\n🔄 Supabase soruları dönüştürülüyor ve birleştiriliyor...")
    supabase_questions = raw_data.get("past_questions", [])

    new_questions_by_target = {}
    duplicates_skipped = 0
    added_count = 0

    for row in supabase_questions:
        data = row.get("data") if isinstance(row.get("data"), dict) else {}
        reconstruction = row.get("reconstruction") if isinstance(row.get("reconstruction"), dict) else {}
        raw_q = row.get("raw_question") if isinstance(row.get("raw_question"), dict) else {}

        qid = str(row.get("id") or data.get("id") or "").strip()
        stem = (
            data.get("stem")
            or reconstruction.get("stem")
            or raw_q.get("stem")
            or row.get("stem")
            or ""
        ).strip()

        if not stem:
            continue

        stem_norm = normalize_stem(stem)

        # Tekilleştirme kontrolü (ID veya Soru metni örtüşmesi)
        if (qid and qid in existing_ids) or (stem_norm and stem_norm in existing_stems):
            duplicates_skipped += 1
            continue

        # Dönem ve Kurul ayrıştırma
        donem, kurul = parse_donem_kurul(
            row.get("committee_id") or data.get("committeeId"),
            data.get("donem") or row.get("donem"),
            data.get("kurul") or row.get("kurul")
        )

        # Seçenekler
        options = format_options(
            data.get("options")
            or reconstruction.get("options")
            or raw_q.get("options")
            or row.get("options")
        )

        # Doğru cevap
        answer = (
            data.get("correctAnswer")
            or data.get("claimedAnswer")
            or reconstruction.get("correctAnswer")
            or row.get("claimed_answer")
            or None
        )

        # Açıklama ve Kanıt
        explanation = data.get("explanation") or reconstruction.get("explanation") or None
        evidence_text = data.get("evidenceText") or reconstruction.get("evidenceText")
        evidence = data.get("evidence") or []
        if evidence_text and not evidence:
            evidence = [evidence_text[:500]]

        status = data.get("status") or ("verified" if evidence else "needs_fix")
        tags = sorted(list(set(data.get("tags", []) + ["supabase_sync", f"donem_{donem}", f"kurul_{kurul}"])))

        unified_q = {
            "question_id": qid or f"sb_{donem}_{kurul}_{len(existing_ids) + 1}",
            "source_id": row.get("source_file") or data.get("sourceFile") or None,
            "donem": donem,
            "kurul": kurul,
            "ders": row.get("discipline") or data.get("discipline") or None,
            "konu": row.get("topic") or data.get("topic") or None,
            "stem": stem,
            "options": options,
            "answer": answer,
            "explanation": explanation,
            "status": status,
            "issues": data.get("issues") or [],
            "evidence": evidence,
            "pipeline_generation": "v2_supabase_merged",
            "tags": tags,
            "created_at": data.get("createdAt") or row.get("updated_at") or now_iso
        }

        # Hedef dosya adı belirleme:
        # Dönem 3 için kurul numarası formatı korunur: 1.jsonl, 2.jsonl vb.
        # Dönem 1 ve 2 için donemX_kY.jsonl formatı kullanılır.
        if donem == 3 and isinstance(kurul, int):
            target_filename = f"{kurul}.jsonl"
        elif donem == 3:
            target_filename = f"3_{kurul}.jsonl"
        else:
            target_filename = f"donem{donem}_{kurul}.jsonl"

        new_questions_by_target.setdefault(target_filename, []).append(unified_q)
        existing_ids.add(unified_q["question_id"])
        if stem_norm:
            existing_stems[stem_norm] = unified_q["question_id"]
        added_count += 1

    print(f"  ✓ Tekilleştirme sonucu atlanan (zaten yerelde olan) soru: {duplicates_skipped}")
    print(f"  ✓ Yerel veritabanına eklenecek yeni soru: {added_count}")

    # 4. Dosyalara yazma / ekleme (Append mode)
    print("\n📝 Dosyalar güncelleniyor...")
    for filename, questions in sorted(new_questions_by_target.items()):
        file_path = local_questions_dir / filename
        lines = [json.dumps(q, ensure_ascii=False) for q in questions]
        mode = "a" if file_path.exists() else "w"
        with open(file_path, mode, encoding="utf-8") as fp:
            if mode == "a":
                fp.write("\n")
            fp.write("\n".join(lines) + "\n")
        print(f"  ➕ {filename}: +{len(questions)} yeni soru eklendi (Toplam dosya satırı: {sum(1 for _ in open(file_path))})")

    # 5. meds/data/pastQuestions.json ve lecture_notes.json güncellemesi
    print("\n🌐 Web arayüzü ve yerel servisler için meds/data senkronize ediliyor...")
    past_json_path = DATA_DIR / "pastQuestions.json"
    if past_json_path.exists():
        existing_past = json.loads(past_json_path.read_text(encoding="utf-8"))
        existing_p_ids = {p.get("id") for p in existing_past if p.get("id")}
        new_past_entries = []
        for row in supabase_questions:
            pid = row.get("id")
            if pid not in existing_p_ids:
                item = row.get("data") if isinstance(row.get("data"), dict) else {}
                item["id"] = pid
                item["committeeId"] = row.get("committee_id")
                item["discipline"] = row.get("discipline")
                item["topic"] = row.get("topic")
                item["claimedAnswer"] = row.get("claimed_answer")
                item["examYear"] = row.get("exam_year")
                new_past_entries.append(item)
                existing_p_ids.add(pid)

        all_merged_past = existing_past + new_past_entries
        past_json_path.write_text(json.dumps(all_merged_past, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  ✓ meds/data/pastQuestions.json güncellendi: {len(existing_past)} -> {len(all_merged_past)} soru!")

    # Lecture Notes kopyası
    lecture_notes = raw_data.get("lecture_notes", [])
    if lecture_notes:
        (DATA_DIR / "lecture_notes_supabase.json").write_text(
            json.dumps(lecture_notes, ensure_ascii=False, indent=1), encoding="utf-8"
        )
        print(f"  ✓ meds/data/lecture_notes_supabase.json kaydedildi ({len(lecture_notes)} ders sunumu).")

    print("\n" + "=" * 60)
    print("🎉 BİRLEŞTİRME BAŞARIYLA TAMAMLANDI!")
    print(f"  - Önceki Yerel Soru Sayısı: {total_local_existing}")
    print(f"  - Supabase'den Eklenen Yeni Soru: {added_count}")
    print(f"  - Toplam Soru Sayısı: {total_local_existing + added_count}")
    print(f"  - Ham Yedek Konumu: {EXPORT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
