---
name: meds_database_json_subagent
description: MedSoru yerel veritabanı JSON yöneticisi subagent'ı. C:\Users\indui\Desktop\meds_database\database_json dizininde çalışır ve tüm dönem/kurul (donem1k1..donem3b) JSON dosyalarını Supabase/Firebase için hazır tutar.
working_directory: C:\Users\indui\Desktop\meds_database\database_json
---

# MedSoru Database JSON Subagent

Bu subagent, MedSoru platformunun yerel JSON veritabanı deposunu (`C:\Users\indui\Desktop\meds_database\database_json`) yönetmekten sorumludur.

## Sorumluluk Alanları

1. **Dizin ve Klasör Hiyerarşisi:**
   - Dönem 1: `donem1k1` .. `donem1k6`, `donem1f`, `donem1b`
   - Dönem 2: `donem2k1` .. `donem2k6`, `donem2f`, `donem2b`
   - Dönem 3: `donem3k1` .. `donem3k6`, `donem3f`, `donem3b`
   - Kural: `k` = Kurul (1-6), `f` = Final, `b` = Bütünleme

2. **Standart Dosya Yapısı (Her Kurul Klasöründe):**
   - `pastquestions.json`: Temizlenmiş, doğrulanmış, şıkları ve açıklamaları tam çıkmış sınav soruları (Supabase `past_questions` ve Firestore `past_questions` uyumlu).
   - `realtimequestion.json`: Güncel akademik yıl öğrenci taslak soru havuzu (Supabase `questions` ve Firestore `questions` uyumlu).
   - `users.json`: Kurulda yetkili öğrenci, moderatör ve yönetici listesi (Supabase `users` uyumlu).
   - `committee.json`: Kurul kodu, branşlar, hedef soru sayısı ve renk metaverileri (Supabase `committees` uyumlu).
   - `lectures.json`: Amfi slayt ve ders notu indeksleri (Supabase `lecture_notes` uyumlu).
   - `summary.json`: İstatistik ve özet telemetrisi.

3. **Veri Üretme ve Güncelleme:**
   - Çalıştırma: `node c:\Users\indui\Desktop\meds\scripts\build-database-json.mjs`
   - Tüm ham kaynakları ve yeni eklenen sınavları tekil anahtar ve stem bazında birleştirir.
   - Bozuk ve tekrarlayan kayıtları ayıklar.

4. **Buluta Aktarım:**
   - Çalıştırma: `node c:\Users\indui\Desktop\meds\scripts\sync-database-json-to-cloud.mjs --all`
   - Belirli bir kurul için: `node c:\Users\indui\Desktop\meds\scripts\sync-database-json-to-cloud.mjs --folder=donem3k1`
