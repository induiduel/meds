# deploy/pg/ — meds-pg (Postgres 17 + pgvector)

- `docker-compose.yml` (konteyner), `init/` (ilk kurulum), `sql/` (idempotent şema: realtime, user_activity, kimlik, rag_* …),
  `backup.sh` (yedek), `migrate-from-supabase.sh` + `sql/gecmis_supabase_migrations/` (tarihî göç), `Caddyfile.rest` (eski PostgREST).

## Veritabanı (meds-pg) ve canlı yayın

Supabase 2026-10-12'de kaldırıldı. Tek veritabanı `meds-pg` (Postgres 17 + pgvector, `deploy/pg/`); asıl kaynak hâlâ
`data/*.json`, Postgres sorgulanabilir kopya + RAG vektörleri + canlı yayın kaynağıdır.
- Sunucu: `src/services/pgDb.ts` (`pgDb.from(...)` Supabase zincir biçimi, `pgDb.rpc`, `pgListen`). Bağlantı `DATABASE_URL`.
- Tarayıcı veritabanına bağlanmaz: `getSupabaseClient()` → `dbRemoteClient` → `POST /api/db/query` (beyaz liste,
  yazma yalnız yönetici; `src/services/dbQueryRoute.ts`).
- Canlı yayın: tablo tetikleyicisi `pg_notify('meds_changes')` (`deploy/pg/sql/realtime.sql`) → server.ts hub
  (120 ms toplu paket) → SSE `/api/realtime/events`. İstemciden istemciye: `broadcastLiveEvent` / `onLiveEvent`
  (`POST /api/live/broadcast`, `app:*` olayları). Gidiş-dönüş testi `POST /api/live/ping`.
- SSE güvenilirliği (2026-10-14): her olay `id: <açılış>-<sıra>` taşır, son 10 dk/2.000 olay halkada; istemci
  (`realtimeEvents.ts`) yeniden bağlanırken `?lastEventId=` yollar, aradakiler yeniden gelir; telafi edilemezse `resync`
  → `medsoru:realtime-resync` (havuz, çıkmış, notlar, profil yeniden çekilir). 20 sn'de bir `hb`; istemci 45 sn veri
  almazsa akışı yeniden kurar. Tek havuz sorusu yazan uçlar `saveQuestionLive(q)` kullanır (meds-pg → `question_updated`
  / `db_change`); yalnız `saveDatabase()` canlı yayın yapmaz. Ekranda canlı abonelik: `hooks/useLiveEvent.ts`.
- Kişiler (yönetim › `/manage/kisiler/<anahtar>`): `src/services/peopleInsights.ts` — `POST /api/presence` (cihaz +
  etkin süre, `user_devices`/`user_usage_daily`), öğrenci yazma uçları ara katmanla `user_events`'e; tetikleyici →
  yalnız yöneticilere `people_changed`. Şema açılışta kendiliğinden uygulanır (`deploy/pg/sql/user_activity.sql`).
  `/api/admin/people*` başlık e-postasına GÜVENMEZ: loopback, yöneticinin erişim jetonu ya da `MEDS_PANEL_SECRET`
  (iki makinenin .env'inde aynı). Yerel panel Oracle hedefindeyken istek yerel sunucudan vekille gider.
- Şema değişikliği: `deploy/pg/sql/` altına idempotent .sql, iki makinede `docker exec -i meds-pg psql -U meds -d meds < ...`.
- Cihazdaki eski betikler `127.0.0.1:8000/rest/v1` (PostgREST, `meds-rest`) ile çalışmaya devam eder; Oracle'da yoktur.
- Yedek: Oracle `meds-pg-yedek.timer` her gece 03:30 → `~/yedek/meds-pg/` (7 gün).
