# CLAUDE.md

> **Önce oku:** `../PROJE_TANITIMI.md` — projenin amacı, klasör yapısı (downloads/temp1-2-3/database) ve zorunlu boru hattı. Tüm ajanlar buna uygun davranmalıdır.

MedSoru: shared exam-question pool for Turkish medical school (Dönem 3). Students submit fragments of
questions they remember; the backend retrieves matching course material / past exam questions (RAG)
and an LLM reconstructs the full question grounded on those sources. See README.md for the flow.

UI text, prompts and most comments are Turkish. Keep new user-facing strings Turkish.

## Commands

- `npm run dev` — backend + Vite middleware on http://localhost:3000 (`PORT` is hardcoded in `server.ts`)
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
  `safeJsonFetch('/api/...')`; it prepends the user-configured API URL (GitHub Pages + tunnel setup).
  Raw `fetch('/api/...')` breaks on GitHub Pages.
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
  backend (`/api/ai/generate` or feature endpoints). Firebase web `apiKey` and Supabase publishable
  key are public by design.
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

## Retrieval

Changing the tokenizer, stopwords or scoring in `localRagEngine.ts` changes ranking for every
feature. Run `npx tsx scripts/eval/retrieval-eval.mts` (and again with `STRIP=1`) before and after.
It samples 300 past questions (fixed seed) and checks whether a simulated student query finds the
same question in the top 5.

Current tokenizer: Turkish case/character folding + full word + 5-char stem. Last results (hit@5):
partial stem words 95%, suffix-changed words 91%, topic only 58% (98% same-topic; topics are shared
by many questions, so exact match is not expected). Stem-only and word-only were both worse.

Hybrid BM25 + e5 vectors (`src/services/vectorSearch.ts`, local Supabase `match_rag_chunks_e5`, embed service
`meds-embed` on 127.0.0.1:8091) is OFF by default (`MEDS_VECTOR_SEARCH=1` to enable): `HYBRID=1` eval gave
94/93/41 (weight 0.8) and 95/93/43 (0.3) vs BM25 96/92/44. Vectors are local-only; cloud Supabase is full
(`rag_vector_build.py` defaults to `--hedef yerel`).

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
Mevcut Supabase verisi yeni hat hazır olana kadar kullanılır, sonra silinmez: "eski" olarak saklanır.
