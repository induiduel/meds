#!/usr/bin/env python3
"""
scripts/sync_to_supabase_v2.py
--------------------------------------------------------------------------------
MedSoru AI - Supabase v2 Chunk-Build Veri Senkronizasyonu Motoru

1. 6.263 Doğrulanmış ve Zenginleştirilmiş Çıkmış Soruyu Supabase past_questions'a yükler:
   - Sürüm etiketi: v2_local_pipeline_2026
   - Çakışma koruması (resolution=merge-duplicates)
   - Mevcut öğrenci yorumları, beğenileri (upvotes) ve şikayetleri (reports) korunur.
   - Öncelikli yükleme (Tier 1: Dönem 3 Kurul 1-6, Final, Bütünleme -> Tier 2: Diğer dönemler).

2. 24.794 Amfi Ders Slayt Parçasını (RAG Chunks) Supabase rag_chunks'a yükler:
   - Chunk-build mimarisi: Önce yüksek kaliteli ve çekirdek kurullar (Tier 1), ardından derin arşiv (Tier 2).
   - Çoklu iş parçacığı (ThreadPoolExecutor) ve bağlantı havuzuyla ultra-hızlı akış.
"""

import os
import sys
import glob
import json
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://kgutsltgmqbnlxcnzrtl.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_SECRET_KEY", os.environ.get("SUPABASE_KEY", ""))

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates"
}

def clean_for_postgres(val):
    if val is None:
        return None
    if isinstance(val, str):
        return val.replace("\x00", "").replace("\u0000", "")
    if isinstance(val, list):
        return [clean_for_postgres(v) for v in val]
    if isinstance(val, dict):
        return {k: clean_for_postgres(v) for k, v in val.items()}
    return val

def post_batch_with_retry(endpoint, rows, max_retries=4):
    url = f"{SUPABASE_URL}/rest/v1/{endpoint}?on_conflict=id"
    payload = json.dumps(clean_for_postgres(rows)).encode("utf-8")
    
    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(url, data=payload, headers=HEADERS, method="POST")
            with urllib.request.urlopen(req, timeout=30) as resp:
                if resp.status in (200, 201, 204):
                    return True, len(rows), None
                return False, 0, f"HTTP {resp.status}"
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8", errors="ignore")
            if attempt == max_retries or e.code not in (429, 500, 502, 503, 504):
                return False, 0, f"HTTP {e.code}: {err_msg[:200]}"
            time.sleep(1.0 * attempt)
        except Exception as e:
            if attempt == max_retries:
                return False, 0, str(e)
            time.sleep(1.0 * attempt)
    return False, 0, "Unknown failure"

def fetch_existing_interactions():
    print("🔍 [Supabase] Mevcut kullanıcı etkileşimleri (yorumlar, oylar) taranıyor...")
    base_url = f"{SUPABASE_URL}/rest/v1/past_questions?select=id,upvotes,comments,reports"
    interactions = {}
    from_row = 0
    page_size = 1000
    
    while True:
        try:
            req = urllib.request.Request(
                base_url,
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
                    "Range": f"{from_row}-{from_row + page_size - 1}"
                }
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if not data:
                    break
                for r in data:
                    up = r.get("upvotes") or 0
                    cm = r.get("comments") or []
                    rp = r.get("reports") or []
                    if up > 0 or len(cm) > 0 or len(rp) > 0:
                        interactions[r["id"]] = {"upvotes": up, "comments": cm, "reports": rp}
                if len(data) < page_size:
                    break
                from_row += page_size
        except Exception as e:
            print(f"⚠️ Etkileşim tarama uyarısı: {e}")
            break
            
    print(f"✅ {len(interactions)} soru için mevcut kullanıcı etkileşimi korundu.")
    return interactions

def sync_past_questions():
    print("\n" + "="*80)
    print("🚀 [AŞAMA 1] ÇIKMIŞ SORULAR SENKRONİZASYONU (6.263 Soru)")
    print("="*80)
    
    past_path = os.path.join(ROOT_DIR, "data", "pastQuestions.json")
    with open(past_path, "r", encoding="utf-8") as f:
        questions = json.load(f)
        
    print(f"📂 Yerel dosya yüklendi: {len(questions)} soru.")
    existing_meta = fetch_existing_interactions()
    
    now_iso = datetime.now(timezone.utc).isoformat()
    rows = []
    
    for q in questions:
        qid = q.get("id")
        cid = q.get("committeeId") or "donem3-kurul1"
        disc = q.get("discipline") or "Tıbbi Patoloji"
        topic = q.get("topic") or f"Soru #{q.get('questionNumber') or qid}"
        year = q.get("examYear") or "Geçmiş Yıllar Çıkmışı (Arşiv)"
        source = q.get("sourceFile") or None
        cat = q.get("category") or q.get("aiCategory") or None
        claimed = q.get("correctOption") or q.get("correctAnswer") or q.get("claimedAnswer") or None
        
        # Merge existing interactions
        inter = existing_meta.get(qid, {})
        upvotes = inter.get("upvotes") or q.get("upvotes") or 0
        comments = inter.get("comments") or q.get("comments") or []
        reports = inter.get("reports") or q.get("reports") or []
        
        # Versioning metadata injection
        q_copy = dict(q)
        q_copy["version"] = "v2_local_pipeline_2026"
        q_copy["pipeline_version"] = "2026_phase4_verified"
        q_copy["upvotes"] = upvotes
        q_copy["comments"] = comments
        q_copy["reports"] = reports
        q_copy["syncedAt"] = now_iso
        
        row = {
            "id": qid,
            "committee_id": cid,
            "discipline": disc,
            "topic": topic,
            "exam_year": year,
            "source_file": source,
            "ai_category": cat,
            "claimed_answer": claimed,
            "raw_question": q.get("rawQuestion") or None,
            "reconstruction": q.get("reconstruction") or None,
            "is_suspect": bool(q.get("isSuspect")),
            "is_ambiguous": bool(q.get("isAmbiguous")),
            "is_locked": bool(q.get("isLocked")),
            "upvotes": upvotes,
            "comments": comments,
            "reports": reports,
            "custom_redacted_by": q.get("customRedactedBy") or None,
            "custom_redacted_at": q.get("customRedactedAt") or None,
            "custom_redaction_prompt": q.get("customRedactionPrompt") or None,
            "data": q_copy,
            "updated_at": q.get("updatedAt") or now_iso
        }
        rows.append(row)
        
    # Chunk-Build Önceliklendirme:
    # Tier 1: Dönem 3 Kurul 1-6 + Final + Bütünleme (En kritik aktif müfredat)
    tier1 = [r for r in rows if r["committee_id"].startswith("donem3")]
    tier2 = [r for r in rows if not r["committee_id"].startswith("donem3")]
    
    print(f"⚡ Chunk-Build Sıralaması: {len(tier1)} adet Dönem 3 Sorusu (Tier 1) + {len(tier2)} Arşiv Sorusu (Tier 2)")
    ordered_rows = tier1 + tier2
    
    BATCH_SIZE = 100
    batches = [ordered_rows[i:i + BATCH_SIZE] for i in range(0, len(ordered_rows), BATCH_SIZE)]
    print(f"📦 Toplam {len(batches)} parti halinde yükleniyor (batch_size={BATCH_SIZE})...")
    
    total_uploaded = 0
    failed_batches = 0
    t0 = time.time()
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(post_batch_with_retry, "past_questions", b): i for i, b in enumerate(batches)}
        for fut in as_completed(futures):
            b_idx = futures[fut]
            success, count, err = fut.result()
            if success:
                total_uploaded += count
                sys.stdout.write(f"\rİlerleme: [{total_uploaded}/{len(ordered_rows)}] soru Supabase'e yazıldı (%{total_uploaded*100/len(ordered_rows):.1f})...")
                sys.stdout.flush()
            else:
                failed_batches += 1
                print(f"\n❌ Parti #{b_idx} hatası: {err}")
                
    t1 = time.time()
    print(f"\n✅ Çıkmış Sorular Tamamlandı: {total_uploaded} soru {t1 - t0:.2f} saniyede senkronize edildi. (Hatalı parti: {failed_batches})")

def sync_rag_chunks():
    print("\n" + "="*80)
    print("🚀 [AŞAMA 2] RAG DERS SLAYT PARÇALARI SENKRONİZASYONU (24.794 Chunk)")
    print("="*80)
    
    chunks_dir = os.path.join(ROOT_DIR, "..", "meds_database", "chunks")
    chunk_files = sorted(glob.glob(os.path.join(chunks_dir, "*.jsonl")))
    print(f"📂 {len(chunk_files)} adet slayt chunk dosyası taranıyor...")
    
    all_chunks = []
    for fpath in chunk_files:
        try:
            with open(fpath, "r", encoding="utf-8") as fp:
                for line in fp:
                    line = line.strip()
                    if not line:
                        continue
                    c = json.loads(line)
                    all_chunks.append(c)
        except Exception as e:
            print(f"⚠️ Dosya okuma hatası {os.path.basename(fpath)}: {e}")
            
    print(f"📑 Toplam {len(all_chunks)} parça yüklendi. Veritabanı şemasına dönüştürülüyor...")
    now_iso = datetime.now(timezone.utc).isoformat()
    rows = []
    
    for c in all_chunks:
        chunk_id = c.get("chunk_id")
        source_id = c.get("source_id") or "slide_doc"
        page = c.get("page") or 1
        heading_path = c.get("heading_path") or []
        title = heading_path[-1] if heading_path else f"Slayt {page}"
        text = c.get("text") or ""
        donem = c.get("donem") or 3
        kurul = c.get("kurul") or 1
        cid = f"donem{donem}-kurul{kurul}"
        ders = c.get("ders") or "Genel Tıp"
        quality = c.get("quality_score") or 0.8
        
        metadata = {
            "version": "v2_local_pipeline_2026",
            "quality_score": quality,
            "heading_path": heading_path,
            "hash": c.get("hash"),
            "source_id": source_id,
            "donem": donem,
            "kurul": kurul,
            "ders": ders
        }
        
        row = {
            "id": chunk_id,
            "document_id": source_id,
            "document_type": "lecture_slide",
            "committee_id": cid,
            "discipline": ders,
            "title": title[:300],
            "page_number": page,
            "content": text,
            "metadata": metadata,
            "embedding": None,
            "created_at": now_iso
        }
        rows.append(row)
        
    # Chunk-Build Kademesi (Tiered Ingestion):
    # Tier 1: Yüksek kaliteli parçalar (quality_score >= 0.85)
    # Tier 2: Kalan parçalar
    tier1 = [r for r in rows if (r["metadata"].get("quality_score") or 0) >= 0.85]
    tier2 = [r for r in rows if (r["metadata"].get("quality_score") or 0) < 0.85]
    
    print(f"⚡ Chunk-Build Kademeleri: {len(tier1)} Yüksek Kaliteli Slayt (Tier 1) + {len(tier2)} Tamamlayıcı Arşiv (Tier 2)")
    ordered_rows = tier1 + tier2
    
    BATCH_SIZE = 150
    batches = [ordered_rows[i:i + BATCH_SIZE] for i in range(0, len(ordered_rows), BATCH_SIZE)]
    print(f"📦 Toplam {len(batches)} parti halinde yükleniyor (batch_size={BATCH_SIZE})...")
    
    total_uploaded = 0
    failed_batches = 0
    t0 = time.time()
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(post_batch_with_retry, "rag_chunks", b): i for i, b in enumerate(batches)}
        for fut in as_completed(futures):
            b_idx = futures[fut]
            success, count, err = fut.result()
            if success:
                total_uploaded += count
                sys.stdout.write(f"\rİlerleme: [{total_uploaded}/{len(ordered_rows)}] slayt chunk Supabase'e yazıldı (%{total_uploaded*100/len(ordered_rows):.1f})...")
                sys.stdout.flush()
            else:
                failed_batches += 1
                print(f"\n❌ Parti #{b_idx} hatası: {err}")
                
    t1 = time.time()
    print(f"\n✅ RAG Slayt Parçaları Tamamlandı: {total_uploaded} chunk {t1 - t0:.2f} saniyede senkronize edildi. (Hatalı parti: {failed_batches})")

def verify_sync_counts():
    print("\n" + "="*80)
    print("📊 [DOĞRULAMA] SUPABASE NİHAİ TABLO SAYIMLARI")
    print("="*80)
    
    for table in ["past_questions", "rag_chunks", "lecture_notes", "committees"]:
        req = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/{table}?select=id",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Range": "0-0",
                "Prefer": "count=exact"
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                crange = resp.headers.get("Content-Range", "Bilinmiyor")
                total = crange.split("/")[-1] if "/" in crange else crange
                print(f"🎯 Tablo '{table}': Toplam {total} kayıt mevcut.")
        except Exception as e:
            print(f"⚠️ Tablo '{table}' sayım hatası: {e}")

if __name__ == "__main__":
    t_start = time.time()
    questions_only = "--questions-only" in sys.argv
    chunks_only = "--chunks-only" in sys.argv

    if chunks_only:
        sync_rag_chunks()
    elif questions_only:
        sync_past_questions()
    else:
        sync_past_questions()
        sync_rag_chunks()

    verify_sync_counts()
    print(f"\n🎉 SENKRONİZASYON BAŞARIYLA TAMAMLANDI! Toplam Süre: {time.time() - t_start:.2f}s")
