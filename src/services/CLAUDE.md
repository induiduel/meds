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
- Servis değişince etki: `python3 scripts/altyapi/bag.py etki <dosya>` (kim kullanıyor).
- Kapı: `npm run lint` 0 hata. Ayrıntı: `docs/hatalar/dagitim_sunucu.md` (H580/H581), `meds/CLAUDE.md` Rules/Retrieval.

- Veritabanı (meds-pg) ve canlı yayın: `deploy/pg/CLAUDE.md`.

## Faz 14 kullanıcı kuyruğu

Students can send a past question to Faz 14 review; error reports join the same queue. The server owns
`meds_database_v2/phase14_past_question_editor/kullanici_kuyrugu.json` (`src/services/phase14UserQueue.ts`); the script
`phase14_cloud_question_editor.py --kullanici-kuyrugu` (free keys only, its own lock) appends results to `kullanici_sonuclari.jsonl`.
The server applies results with `applyPhase14Review` (same path as admin approval) and e-mails non-admin reporters the old/new
question (`src/services/phase14Mail.ts`). Reporter e-mails live only in the local queue file — never in question records or the cloud.
