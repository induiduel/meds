# src/services/ — sunucu ve istemci servisleri

- Sunucu tarafı: `aiProvider.ts` (tek LLM noktası), `ragService.ts` + `localRagEngine.ts` + `vectorSearch.ts` (arama),
  `pgDb.ts` (meds-pg), `contentOverlay.ts` (içerik katmanı), `desteDeposu.ts` (Öğren desteleri), `adminAuth.ts`, `yerelKimlik.ts`, `yonetim16/` (panel).
- İstemci tarafı: `api.ts` (`safeJsonFetch`), `auth.ts`, `realtimeEvents.ts`.

## Kurallar
- **src/data'ya yazım yalnız katmandan (H580/H581):** okuma `resolveContent()`, yazma `writableContent()` + `markContentChanged(entity, ids)`
  (`contentOverlay.ts`); türetilmiş dosyalara (`src/data/decks/items`, paketler) elle yazma. Kapı D5: `python3 scripts/kapilar/yapi_koruma.py`.
- Desteleri yalnız `desteDeposu.ts` (`desteleriOku/desteOku/desteleriYaz`) okur/yazar (D1).
- Sunucu kodu değişince `systemctl --user restart meds-web` (`curl localhost:3000/api/health` 200 olunca hazır); `MemoryMax`/`tsx watch` yok.
- Anahtar yalnız sunucu `.env`'inde; istemciye gitmez. Kaynaklı soru yazımı `findSourcesForQuestion` + `formatSourcesForPrompt` + `toSourceRef`.
- Kapı: `npm run lint` 0 hata. Ayrıntı: `docs/hatalar/dagitim_sunucu.md` (H580/H581), `meds/CLAUDE.md` Rules/Retrieval.

## Taşınan ayrıntı (meds/CLAUDE.md'den)

### Veritabanı (meds-pg) ve canlı yayın

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

### Faz 14 kullanıcı kuyruğu

Students can send a past question to Faz 14 review; error reports join the same queue. The server owns
`meds_database_v2/phase14_past_question_editor/kullanici_kuyrugu.json` (`src/services/phase14UserQueue.ts`); the script
`phase14_cloud_question_editor.py --kullanici-kuyrugu` (free keys only, its own lock) appends results to `kullanici_sonuclari.jsonl`.
The server applies results with `applyPhase14Review` (same path as admin approval) and e-mails non-admin reporters the old/new
question (`src/services/phase14Mail.ts`). Reporter e-mails live only in the local queue file — never in question records or the cloud.
