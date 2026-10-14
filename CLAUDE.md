# CLAUDE.md

> **Önce oku:** `../PROJE_TANITIMI.md` — projenin amacı, klasör yapısı (downloads/temp1-2-3/database) ve zorunlu boru hattı. Tüm ajanlar buna uygun davranmalıdır.

MeDSor: shared exam-question pool for Turkish medical school (Dönem 3). Students submit fragments of
questions they remember; the backend retrieves matching course material / past exam questions (RAG)
and an LLM reconstructs the full question grounded on those sources. See README.md for the flow.

UI text, prompts and most comments are Turkish. Keep new user-facing strings Turkish.

## Commands

- `npm run dev` — backend + Vite middleware on http://localhost:3000 (`PORT` is hardcoded in `server.ts`)
- **Port 3000 = systemd user service `meds-web`, NOT watched** (since 2026-10-12 it runs `tsx server.ts`, see
  `~/.config/systemd/user/meds-web.service.d/10-performans.conf`). After changing `server.ts` or any server-side code:
  `systemctl --user restart meds-web` (ready when `/api/health` returns 200, ~20-30 s). Frontend-only changes need just
  `npx vite build` (3000 serves `dist/`). Do not add `MemoryMax` (Node crashes at startup) or bring `tsx watch` back.
- `npm run lint` — `tsc --noEmit` (must stay at 0 errors)
- `npx vite build` — frontend build check
- No test suite. Verify retrieval changes with a small `tsx` script against `searchRagChunks`
  (see "Retrieval" below) and AI routes by starting the server and curling the endpoint.

Starting the server has side effects: it rebuilds `data/local_rag_chunks.json` (gitignored, ~100MB)
and may write to `data/*.json`. Check `git status` afterwards and revert unintended data changes.

## Layout

- `server.ts` — Express app, all `/api/*` routes (large; prefer adding logic to `src/services/*`).
- `src/services/aiProvider.ts` — the only place that talks to Gemini/Groq. Use
  `generateResilientMedicalAi()` (Gemini key pool → Groq fallback). Server-only.
- `src/services/ragService.ts` — retrieval + grounding helpers: `searchRagChunks`,
  `findSourcesForQuestion`, `formatSourcesForPrompt`, `toSourceRef`, `findSimilarPastQuestions`,
  `executeRagQuery`. Server-only.
- `src/services/localRagEngine.ts` — chunking + in-memory BM25 index (Turkish folding + 5-char stems).
- `src/services/api.ts` — frontend API client (`ApiService`, `safeJsonFetch`). Always use
  `safeJsonFetch('/api/...')`; it prepends the user-configured API URL (live site → Oracle API, or a custom tunnel).
  Raw `fetch('/api/...')` ignores that setting.
- `src/serverLectureNotes.ts` — lecture note storage. `findBestMatchingLectureSlides` is legacy
  (substring matcher, poor ranking); only `scripts/verify-question-answers.mjs` still uses it.
- `scripts/link-exam-questions.mts` — parses exam PDFs/DOCX and links each question to the pool and to
  course material (retrieval only). Run it on a folder to check parser changes.
- `scripts/` — data pipelines (`pipeline/`, `agents/`, `advanced_ai/` phases, `eval/`). `scripts/archive/` holds one-off
  scripts nothing calls (deck/summary builders, Windows launchers); excluded from `tsc`, do not wire new code to them.
- `data/` — local JSON database (large, committed). `src/data/` — data bundled into the frontend.

## Rules

- **Secrets:** provider keys come only from the server `.env` (see `.env.example`). Never hardcode,
  base64/XOR-obfuscate, or ship keys to the client bundle. The browser calls AI only through the
  backend (`/api/ai/generate` or feature endpoints). Firebase web `apiKey` is public by design.
- **Grounding:** any feature that writes or fixes a question must retrieve sources with
  `findSourcesForQuestion` and put them in the prompt via `formatSourcesForPrompt`, ask the model for
  `usedSources`, and return them with `toSourceRef`.
- **Exam dumps are not course material:** notes whose pages are mostly questions are excluded from
  `lecture_slide` results (`getExamDumpNoteIds`). Use `MATERIAL_DOC_TYPES` when you need slides/summaries only.
- **AI output is not evidence:** retrieval is restricted to `GROUNDING_DOC_TYPES`
  (past_question, lecture_slide, summary, transcript). Do not add `ai_qa`, `ai_refinement` or
  `deepseek_contribution` to it.
- **Never overwrite data with an empty result** (see the guard in `deepseekDataService.ts`).
  Machine-specific folders (`MEDS_DATABASE_DIR`, `MEDS_DEEPSEEK_DIR`) come from env.

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
  `/api/admin/people*` başlık e-postasına GÜVENMEZ: loopback, Firebase yönetici jetonu ya da `MEDS_PANEL_SECRET`
  (iki makinenin .env'inde aynı). Yerel panel Oracle hedefindeyken istek yerel sunucudan vekille gider.
- Şema değişikliği: `deploy/pg/sql/` altına idempotent .sql, iki makinede `docker exec -i meds-pg psql -U meds -d meds < ...`.
- Cihazdaki eski betikler `127.0.0.1:8000/rest/v1` (PostgREST, `meds-rest`) ile çalışmaya devam eder; Oracle'da yoktur.
- Yedek: Oracle `meds-pg-yedek.timer` her gece 03:30 → `~/yedek/meds-pg/` (7 gün).

## Retrieval

Changing the tokenizer, stopwords or scoring in `localRagEngine.ts` changes ranking for every
feature. Run `npx tsx scripts/eval/retrieval-eval.mts` (and again with `STRIP=1`) before and after.
It samples 300 past questions (fixed seed) and checks whether a simulated student query finds the
same question in the top 5.

Current tokenizer: Turkish case/character folding + full word + 5-char stem. Last results (hit@5):
partial stem words 95%, suffix-changed words 91%, topic only 58% (98% same-topic; topics are shared
by many questions, so exact match is not expected). Stem-only and word-only were both worse.

Hybrid BM25 + vectors (`src/services/vectorSearch.ts`): query → embed service (`MEDS_EMBED_URL`, bge-m3 :8094 on
both machines) → meds-pg `match_rag_chunks_bge_m3` (HNSW) → RRF with BM25. Enabled when `MEDS_EMBED_URL` is set
(`MEDS_VECTOR_SEARCH=0` disables). Older `HYBRID=1` eval (e5): 94/93/41 (w 0.8) vs BM25 96/92/44.

Vector pipeline (2026-10-13): `scripts/advanced_ai/rag_vektor_hatti.py` is the only writer of `rag_chunks`
(`rag_vector_build.py` is a compat wrapper). It reads `data/local_rag_chunks.json`, embeds only new/changed chunks
through the CPU services (no in-process model), writes meds-pg with COPY, deletes rows no longer in the source, and
with `--oracle` sends only the diff (id + hashes + vector fingerprint) to Oracle over ssh (gzip). `--denetle` finds and
repairs bge vectors stored under the wrong chunk. Cron every 3 h on the device. Never restore `rag_chunks` with a full
dump without re-running `deploy/pg/sql/rag_chunks_indexes.sql` (Oracle lost every index that way → 1.7 s queries).
SQL functions live in `deploy/pg/sql/rag_vektor_islevleri.sql` (dynamic plpgsql so HNSW is used with/without filters).
`GET /api/rag/related` (`src/services/ragRelatedRoutes.ts`) uses stored vectors (no embed call): `mod=ilgili` lecture
material, `benzer` similar questions, `kopya` near-duplicates; `GET /api/rag/vectors/health` shows coverage.

The in-memory BM25 index stores postings as typed arrays (`Int32Array` doc numbers + `Uint16Array` tf); chunks added
after a rebuild go to a small pending map. The old nested `Map<term, Map<chunkId, tf>>` (~1 GB) made `meds-web` hit the
2 GB heap limit during re-chunking.

## Known gaps

- `requireAdmin` trusts the `x-admin-email` header and loopback IPs (tunnel traffic is loopback):
  effectively unauthenticated. AI endpoints have no auth or rate limit.
- Lecture data contains duplicate decks, chat exports with personal data, and empty OCR pages.

## Öğren destesi (src/data/interactive_learning_decks.json)

- Read `docs/OGREN_ETKILESIM_REHBERI.md` before adding decks, slides or interactive elements, or changing `src/components/learn/lesson/`.
- Write decks only to `src/data/interactive_learning_decks.json`. `src/data/decks/items/` is generated by `scripts/vite/splitLearningDecks.ts`, gitignored, and overwritten whenever the source changes.
- Gate: `python3 scripts/validate_learning_decks.py` must report 0 HATA (`--duzelt` repairs truncated chain steps and answer-leaking hints). Then `npx vite build` and `python3 scripts/build_kazanim_deck_index.py`.
- Student error reports: `/api/learn/feedback*` → `src/services/learnFeedbackService.ts` → `data/learn_feedback.json`.

## Paths

- Proje kodu: `/home/indu/medsor/meds`
- Veritabanı klasörü (PDF'ler, `database_json/`, redakte sorular): `/home/indu/medsor/meds_database`
  — `.env` içindeki `MEDS_DATABASE_DIR` bunu gösterir; script/server varsayılanı da aynıdır. Yeni kodda bu yolu
  hardcode etme, `process.env.MEDS_DATABASE_DIR` kullan.

## Yeni veri hattı (scripts/pipeline/)

Akış: Drive → `meds_downloads` (ham) → `meds_temp` (ara) → `meds_database` (temiz). Kapsam: Dönem 3.
`00-init` iskelet, `01-inventory` envanter (`_manifest.json`), `02-download` artımlı indirme
(`_downloads.json` durum; ücretsiz herkese açık indirme, olmazsa `GOOGLE_SERVICE_ACCOUNT_FILE`).
Eski Supabase verisinin tam dökümleri `meds_temp/yedek/supabase_oncesi_20261012/` altında saklanır (silinmez).

## Faz 14 kullanıcı kuyruğu

Students can send a past question to Faz 14 review; error reports join the same queue. The server owns
`meds_database_v2/phase14_past_question_editor/kullanici_kuyrugu.json` (`src/services/phase14UserQueue.ts`); the script
`phase14_cloud_question_editor.py --kullanici-kuyrugu` (free keys only, its own lock) appends results to `kullanici_sonuclari.jsonl`.
The server applies results with `applyPhase14Review` (same path as admin approval) and e-mails non-admin reporters the old/new
question (`src/services/phase14Mail.ts`). Reporter e-mails live only in the local queue file — never in question records or the cloud.
