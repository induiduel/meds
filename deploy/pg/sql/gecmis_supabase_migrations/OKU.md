# Geçmiş Supabase migration'ları (yalnız başvuru)

Supabase 2026-10-12'de kaldırıldı. Bu dosyalar şemanın nasıl oluştuğunu gösterir; **yeniden çalıştırılmaz**.
Güncel şema meds-pg'ye `deploy/pg/migrate-from-supabase.sh` ile döküm olarak taşındı; canlı yayın
tetikleyicileri ve ek indeksler `deploy/pg/sql/realtime.sql` içindedir. Yeni şema değişikliği
`deploy/pg/sql/` altına idempotent bir .sql dosyası olarak eklenir ve iki makinede de uygulanır:
`docker exec -i meds-pg psql -U meds -d meds < deploy/pg/sql/<dosya>.sql`
