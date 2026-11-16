# CLAUDE.md

> **Kurul 2+ otomatik hat:** `docs/KURUL_OTOMASYON_EL_KITABI.md` (aşamalar, zamanlayıcılar, kapılar, dağıtım kuralları) +
> `docs/KURUL2_YAPILMAYACAK_HATALAR.md`; aşama defteri `otomasyon/hat.json`.

> **İçerik üretimi — tek hat (2026-11-16):** `scripts/hat/tam_hat/kosucu.py` sırayı tek kaynaktan (`scripts/hat/tam_hat/mod.py`)
> verir; aşamalar bir kez üretilen read-once `baglam/` (`scripts/hat/tam_hat/baglam.py`: slayt dizini+atom+hoca vurgusu+çıkmış+şema)
> okur, ham slaytı/şablonu tekrar değil. Ders kilidi `scripts/hat/tam_hat/ders_kilit.py` (atomik). Akış `docs/TAM_HAT_HIZLI_AKIS.md` §0.0.

> **Önce oku:** `../PROJE_TANITIMI.md` — projenin amacı, klasör yapısı (downloads/temp1-2-3/database) ve zorunlu boru hattı. Tüm ajanlar buna uygun davranmalıdır.

MeDSor: shared exam-question pool for Turkish medical school (Dönem 3). Students submit fragments of
questions they remember; the backend retrieves matching course material / past exam questions (RAG)
and an LLM reconstructs the full question grounded on those sources. See README.md for the flow.

UI text, prompts and most comments are Turkish. Keep new user-facing strings Turkish.


**Başlarken:** `python3 scripts/altyapi/nereye.py "<görev>"` okunacak dosyaları, kuralları ve kapıları verir; `python3 scripts/altyapi/bag.py kim|etki <yol>` bağımlılıkları (grep yerine). Klasöre özgü kurallar alt klasörlerin kısa `CLAUDE.md`'lerinde.
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

Starting the server has side effects: it rebuilds `data/local_rag_chunks.jsonl` (JSONL, one chunk per line; old `.json` read only if `.jsonl` is missing — `src/services/ragParcaDeposu.ts`; gitignored, ~130MB)
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
- `scripts/` — grouped by purpose (2026-11-16); **read `scripts/HARITA.md` first** instead of browsing: `hat/` (orchestration;
  content line `hat/tam_hat/kosucu.py`), `uretim/` (content production), `altyapi/` (services, `pipeline/`, `advanced_ai/`,
  `vite/` plugins, `v2`/`semantic` packages run as `cd scripts/altyapi && python -m v2`), `moduller/` (site tools, `eval/`),
  `kapilar/` (gate entry `kos.py` + `matris.json`), `arsiv/` (dead code: excluded from `tsc` and Oracle; never wire to it).
  New scripts resolve roots via `scripts/kok.py` (`_kok.MEDS/SCRIPTS/PROJE`), never `Path(__file__).parents[N]`;
  working data lives in `meds_temp/<module>/`, code only in git. Old→new paths: `deploy/oracle/tasinan_yollar.txt`.
- `data/` — local JSON database (large, committed). `src/data/` — data bundled into the frontend.

## Rules

- **Secrets:** provider keys come only from the server `.env` (see `.env.example`). Never hardcode,
  base64/XOR-obfuscate, or ship keys to the client bundle. The browser calls AI only through the
  backend (`/api/ai/generate` or feature endpoints).
- **Auth (2026-11-02, Firebase/Google removed):** own accounts in meds-pg (`auth_hesaplar`/`auth_oturumlar`/`auth_kodlar`,
  `deploy/pg/sql/kimlik.sql`), routes `/api/kimlik/*` (`src/services/yerelKimlik.ts`), HMAC access token verified locally
  (`src/services/kimlikDogrulama.ts`: `requestUser`, `bearerToken`). Client `src/services/auth.ts` exposes a Firebase-like
  `auth` object (`currentUser.getIdToken()`, `onAuthStateChanged`). uids of migrated accounts are the old Firebase uids.
  Never add a mandatory path (login, data write, backup) that depends on an external account.
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

Ayrıntı (pgDb, SSE, Kişiler, şema, yedek): `src/services/CLAUDE.md`.

## Retrieval

Changing the tokenizer, stopwords or scoring in `localRagEngine.ts` changes ranking for every
feature. Run `npx tsx scripts/moduller/eval/retrieval-eval.mts` (and again with `STRIP=1`) before and after.
It samples 300 past questions (fixed seed) and checks whether a simulated student query finds the
same question in the top 5.

**Baseline 2026-11-16 (hit@5, pool = questions the site actually shows; merged copies and quarantined records are excluded
like in the index, H589): partial stem words 87%, suffix-changed words 60%, topic only 34% (100% same-topic).** Compare against
these, not the 2026-10-03 figures below (measured before question merging and before the pool grew to 6.6k near-duplicates).

Current tokenizer: Turkish case/character folding + full word + 5-char stem. Last results (hit@5):
partial stem words 95%, suffix-changed words 91%, topic only 58% (98% same-topic; topics are shared
by many questions, so exact match is not expected). Stem-only and word-only were both worse.

Hybrid BM25 + vectors (`src/services/vectorSearch.ts`): query → embed service (`MEDS_EMBED_URL`, bge-m3 :8094 on
both machines) → meds-pg `match_rag_chunks_bge_m3` (HNSW) → RRF with BM25. Enabled when `MEDS_EMBED_URL` is set
(`MEDS_VECTOR_SEARCH=0` disables). Older `HYBRID=1` eval (e5): 94/93/41 (w 0.8) vs BM25 96/92/44.

Vector pipeline (`rag_vektor_hatti.py`, indeks SQL, `/api/rag/related`): `scripts/altyapi/advanced_ai/CLAUDE.md`.

The in-memory BM25 index stores postings as typed arrays (`Int32Array` doc numbers + `Uint16Array` tf); chunks added
after a rebuild go to a small pending map. The old nested `Map<term, Map<chunkId, tf>>` (~1 GB) made `meds-web` hit the
2 GB heap limit during re-chunking.

## Known gaps

- Admin auth (2026-10-20, `src/services/adminAuth.ts`): `isRequestAdmin`/`requireAdmin` accept only a verified
  caller — `x-panel-secret` = `MEDS_PANEL_SECRET`, genuine loopback (no `cf-connecting-ip`/`x-forwarded-for`/`x-real-ip`),
  or `Authorization: Bearer <MeDSor access token>` of the admin email (browser adds it via `src/services/adminFetchAuth.ts`).
  Switch `MEDS_ADMIN_AUTH`: `log` (default) still accepts the legacy `x-admin-email`/`adminEmail`/`requestedBy` claim but
  writes it to `data/admin_auth_log.jsonl`; `strict` rejects it. Go strict only after the log stays empty of legitimate
  traffic. Scripts calling Oracle must send `x-panel-secret`. Local panel → Oracle goes same-origin with
  `x-panel-proxy: oracle` (`?panelProxy=oracle` for EventSource); the local server forwards genuine-loopback requests
  with the secret. AI endpoints have no auth or rate limit.
- Lecture data contains duplicate decks, chat exports with personal data, and empty OCR pages.

## Öğren destesi (src/data/interactive_learning_decks.json)

- Read `docs/OGREN_ETKILESIM_REHBERI.md` before adding decks, slides or interactive elements, or changing `src/components/learn/lesson/`.
- Write decks only to `src/data/interactive_learning_decks.json`. `src/data/decks/items/` is generated by `scripts/altyapi/vite/splitLearningDecks.ts`, gitignored, and overwritten whenever the source changes.
- Gate: `python3 scripts/validate_learning_decks.py` must report 0 HATA (`--duzelt` repairs truncated chain steps and answer-leaking hints). Then `npx vite build` and `python3 scripts/build_kazanim_deck_index.py`.
- Student error reports: `/api/learn/feedback*` → `src/services/learnFeedbackService.ts` → `data/learn_feedback.json`.

## Büyük veri dosyaları (2026-11-16)

Ayrıntı (dev JSON'lar, `jq`, deste deposu): `src/data/CLAUDE.md`.

## Paths

- Proje kodu: `/home/indu/medsor/meds`
- Veritabanı klasörü (PDF'ler, `database_json/`, redakte sorular): `/home/indu/medsor/meds_database`
  — `.env` içindeki `MEDS_DATABASE_DIR` bunu gösterir; script/server varsayılanı da aynıdır. Yeni kodda bu yolu
  hardcode etme, `process.env.MEDS_DATABASE_DIR` kullan.

## Yeni veri hattı (scripts/altyapi/pipeline/)

Ayrıntı: `scripts/altyapi/pipeline/CLAUDE.md`.

## Faz 14 kullanıcı kuyruğu

Ayrıntı: `src/services/CLAUDE.md`.
