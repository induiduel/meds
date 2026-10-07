# MeDSor — Sistem Dokümanı

> Projenin ne yaptığını, verinin nereden gelip nereye gittiğini, yapay zekâ katmanlarını,
> sunucu uçlarını, ön yüz ekranlarını ve tüm betikleri tek yerde anlatır.
> Hazırlanma: 2026-10-05. Kaynak: kodun kendisi (servis ve betik başlık açıklamaları, `server.ts` rotaları,
> `package.json`, `PROJE_TANITIMI.md`, `CLAUDE.md`). Kodla çelişen bir yer görürsen kod doğrudur; bu dosyayı güncelle.

---

## 1. Proje ne yapar?

MeDSor (eski adıyla MedSoru), Karabük Üniversitesi Tıp Fakültesi **Dönem 3** öğrencileri için ortak bir
**kurul sınavı soru havuzu ve çalışma uygulamasıdır**.

1. **Hatırlanan soruyu toplamak.** Sınavdan çıkan öğrenciler aklında kalan parçaları (soru kökü, şık, ipucu,
   cevap) yazar. Aynı soruya ait parçalar otomatik eşleştirilip tek bir taslakta birleşir.
2. **Soruyu yeniden kurmak.** Taslak; ders slaytları, ders özetleri, ses kaydı dökümleri ve geçmiş yılların
   çıkmış sorularından **kaynak bulunarak (RAG)** yapay zekâyla tam soruya dönüştürülür. Kaynağa dayanmayan
   bilgi üretilmez; kullanılan kaynaklar soruyla birlikte saklanır.
3. **Çalışmak.** Çıkmış soru arşivi, soru çözme ve deneme sınavı, ezber kartları (aralıklı tekrar),
   interaktif ders anlatımları (slayt slayt), tıbbi sözlük/ansiklopedi, ders özetleri ve bir yapay zekâ asistanı.
4. **Yönetmek.** Yönetici konsolu: şikâyet edilen sorular, taslak stüdyosu, kullanıcılar, betik ve otomasyon
   çalıştırma, sistem sağlığı.

Arayüz dili Türkçedir. Uygulama telefonda, tablette ve bilgisayarda aynı kod tabanıyla çalışır
(GitHub Pages + tünel ya da yerel sunucu üzerinden).

---

## 2. Mimari (kuşbakışı)

```
 Google Drive (ders PDF/PPTX, çıkmış soru dosyaları, ders programı)
        │  scripts/pipeline/01-inventory → 02-download
        ▼
 meds_downloads/  (ham)  ──scripts/agents/read_document──▶ meds_temp/temp1
        │                                   stage2_clean ──▶ temp2
        │                                   stage3_merge ──▶ temp3
        │                                   stage4_database ▶ meds_database/  (yalnızca doğrulanmış, chunk'lı)
        ▼
 data/*.json  (uygulamanın yerel JSON veritabanı)     Supabase (bulut / yerel) · Firebase (kimlik)
        │
        ▼
 server.ts  (Express, 130 /api ucu)  ── localRagEngine (BM25 indeksi, ~60 bin chunk) ── aiProvider (yerel GPU → Groq → Muse Spark → Gemini)
        │
        ▼
 React ön yüz (Vite)  ──  src/App.tsx + src/components/*  ──  safeJsonFetch('/api/...')
```

- **Sunucu:** `server.ts` tek Express uygulaması; geliştirmede Vite ara katmanıyla, `dist/` varsa derlenmiş
  ön yüzü sunar. Port 3000 sabittir.
- **Ön yüz:** React 19 + Tailwind v4, Vite ile derlenir. Tüm sunucu çağrıları `src/services/api.ts` içindeki
  `safeJsonFetch` üzerinden gider (GitHub Pages + tünel kurulumunda adresin başına kullanıcı ayarındaki API
  adresini ekler).
- **Veri katmanları:**
  - `data/` — sunucunun yerel JSON veritabanı (soru havuzu `questions.json`, çıkmış sorular
    `pastQuestions.json`, ders notları, kullanıcılar, AI etkileşimleri, RAG indeksi `local_rag_chunks.json`).
  - Supabase (PostgreSQL) — bulut ya da yerel (Docker, `supabase-server/`). Çıkmış sorular, şikâyetler, havuz
    aynası. `multiDbManager` ve `supabaseDb` üzerinden.
  - Firebase — kimlik doğrulama; Firestore `dbFlags.ts` ile kapatılabilir (varsayılan: Supabase + yerel).
  - Tarayıcı — kişisel çalışma verisi (`studyStore.ts`: ilerleme, tekrar listesi, favoriler, notlar;
    `pastQuestionsCache.ts`: IndexedDB soru önbelleği).
- **Makineye özel klasörler** `.env` ile verilir: `MEDS_DATABASE_DIR`, `MEDS_TEMP_DIR`,
  `MEDS_DOWNLOADS_DIR`, `MEDS_DEEPSEEK_DIR`, `MEDS_TRANSCRIPTIONS_DIR`.

---

## 3. Veri boru hattı (Drive → veritabanı)

Kural kitabı `../PROJE_TANITIMI.md`'dir. Aşamalar sırayla çalışır; bir öncekinin çıktısı doğrulanmadan
sonrakine geçilmez. Okuma, temizleme ve eşleştirme **yerel araçlarla** yapılır (Tesseract `tur`, PyMuPDF,
python-pptx, Ollama); bulut AI yalnızca gerektiğinde kullanılır.

| Aşama | Betik | Ne yapar |
|---|---|---|
| 0 | `scripts/pipeline/00-init.mjs` | `meds_downloads` / `meds_temp` / `meds_database` iskeletini kurar. |
| 1 | `scripts/pipeline/01-inventory.mjs` | Drive köklerinin envanterini çıkarır → `meds_downloads/_manifest.json` (dosya indirmez). |
| 2 | `scripts/pipeline/02-download.mjs` | Dosyaları artımlı indirir (`_downloads.json` durum). |
| 3 | `scripts/agents/read_document.py` (+ `watch_downloads.py`) | PDF/PPTX → `temp1` (metin + OCR; isteğe bağlı görsel model). |
| 4 | `scripts/agents/stage2_clean.py` | `temp1` → `temp2`: biçim temizliği, Türkçe karakter onarımı, ham kaynakla teyit. |
| 5 | `scripts/agents/stage3_merge.py` | `temp2` → `temp3`: müfredat eşleşmesi, metadata, tekilleştirme, soru ↔ kaynak ilişkisi. |
| 6 | `scripts/agents/stage4_database.py` | `temp3` → `meds_database`: yalnızca doğrulanmış/kanıtlı kayıtlar, chunk'lı JSON. |
| — | `scripts/agents/pipeline_runner.py` | 4–6'yı sürekli ve hata toleranslı çalıştıran orkestratör. |
| — | `scripts/agents/parse_ders_programi.py` | Ders programı PDF'ini ayrıştırır → `meds_database/taxonomy/donem3_ders_programi.json` (kurul → ders → konu → tarih/hoca → PDF adayı). |
| — | `scripts/pipeline/10-enrich-summaries.mjs` | Ders özetlerini programdaki gerçek ders adı/hocasıyla ve kaynak PDF'in tarihiyle eşleştirir → `src/data/summaries_enrichment.json`, `curriculum_disciplines.json`. |

Destek ajanları: `watchdog.py` (GPU/VRAM ve asılı süreç denetimi), `question_quality_inspector.py`
(tekrar eden ve bağlamı bozuk soruları arka planda işaretler), `post_lora_auto_refiner.py` (model eğitimi
sonrası veri iyileştirme), `run.sh` (doğru Python ortamıyla çalıştırma). Mevcut Supabase verisi yeni hat
hazır olana kadar kullanılmaya devam eder.

---

## 4. Yapay zekâ sistemleri

### 4.1 Sağlayıcı katmanı — `src/services/aiProvider.ts` (yalnız sunucu)

Tüm model çağrıları buradan geçer; anahtarlar yalnızca sunucu `.env` dosyasından okunur, istemciye gönderilmez.
`generateResilientMedicalAi()` sırayla dener:

1. **Yerel GPU (Ollama, `OLLAMA_HOST`)** — `gemma3:4b`, `medgemma1.5:4b`, `qwen3:1.7b`, `deepseek-r1:8b`,
   özel eğitilmiş `medsoru-d3` (QLoRA, `models/medsoru-d3-qlora`).
2. **Groq** — `openai/gpt-oss-120b` ve benzerleri (`GROQ_API_KEY`, yedek `GROQ_API_KEY_2`).
3. **Muse Spark / OpenRouter** — ücretsiz katman (`MUSE_SPARK_API_KEY`).
4. **Google Gemini Flash** — anahtar havuzu (`GEMINI_API_KEY`, `GEMINI_BILLED_KEY`), son seçenek.

Her model için ayrı zaman aşımı vardır (`MODEL_TIMEOUTS_MS`). Hatalar `data/ai_error_logs.json`'a yazılır,
yönetici konsolunda ve Asistan sayfasında (yalnız yöneticiye) görünür.

> Not: `CLAUDE.md` sırayı "Gemini → Groq" olarak anlatıyor; güncel kod yukarıdaki dört basamaklı sırayı
> kullanıyor.

### 4.2 Bilgi getirme (RAG)

- **`localRagEngine.ts`** — bellek içi **BM25** indeksi (~60 bin chunk: çıkmış sorular, havuz soruları, ders
  slaytları, özetler, ses dökümleri, öğrenci katkıları, DeepSeek katkıları, AI kayıtları). Türkçe karakter
  katlama, tam kelime + 5 harf kök, yazım hatası toleransı (Damerau–Levenshtein), terim koordinasyonu ve tür
  bonusları. İndeks açılışta `data/local_rag_chunks.json`'dan yeniden kurulur.
  - Ek olarak: `findChunksById` (kimlikle arama), `suggestSpelling` ("Bunu mu kastettiniz?" — derlem
    sözlüğünden düzeltme ve Türkçe karakter geri kazanımı).
- **`ragService.ts`** — üst katman:
  - `searchRagChunks` / `findSourcesForQuestion` / `formatSourcesForPrompt` / `toSourceRef`: soru yazan ya da
    düzelten her özellik kaynakları buradan alır, isteme koyar, modelden `usedSources` ister.
  - **Kural:** getirme yalnızca `GROUNDING_DOC_TYPES` (past_question, lecture_slide, summary, transcript) ile
    yapılır; AI üretimi kayıtlar kaynak sayılmaz. Soru yığını olan "ders notları" (`getExamDumpNoteIds`)
    slayt sonucu olarak dönmez.
  - `searchEverything`: uygulama içi genel arama — BM25 sonrası kapsama + başlık eşleşmesine göre yeniden
    sıralama, tekilleştirme, eşleşmenin çevresinden kesit, türe göre sayım. AI kayıtları gösterilmez.
  - `findSimilarPastQuestions`: yazılan metne benzeyen çıkmış sorular (şıklar ve cevapla).
- **Değerlendirme:** `scripts/eval/retrieval-eval.mts` (300 soruluk sabit örnek, hit@5). Sıralamayı etkileyen
  her değişiklikten önce ve sonra çalıştırılır.

### 4.3 Uygulama içindeki AI özellikleri

| Özellik | Nerede | Ne yapar |
|---|---|---|
| Soru yeniden kurma | `POST /api/questions/:id/ai-reconstruct` | Taslak parçalarını kaynaklara dayanarak tam soruya çevirir. |
| AI ile düzelt / iyileştir | `AiQuestionOptimizerModal`, `/api/ai/optimize-question` | Var olan soruyu kaynaklı biçimde düzeltir. |
| Gelişmiş soruya dönüştür | `questionUpgradeService.ts`, `/api/ai/upgrade-advanced-question` | Basit soruyu vaka temelli soruya yükseltir. |
| Benzer soru üret | `/api/ai/generate-similar-question` | Çıkmış sorudan pratik sorusu türetir. |
| Soru sohbeti | `QuestionAiChatDrawer`, `/api/ai/question-chat` | Belirli bir soru hakkında kaynaklı sohbet. |
| Asistan | `LocalAiChatView`, `/api/ai/general-chat` | Soru dedektifi, anahtar kelimeden soru türetme, mekanizma açıklama. |
| Taslak stüdyosu | `studioAiService.ts`, `/api/studio/*` | Dağınık parçalardan soru adayı oluşturur. |
| Ders notu onarımı | `lectureRepairEngine.ts` | OCR'ı bozuk notları özetlerle onarır. |
| Ses dökümü | `transcriptionService.ts`, `transcribe_medical_audio.py` | Amfi ses kayıtlarını metne çevirir. |
| Çıkmış soru ayrıştırma | `/api/ai/parse-past-questions`, `/api/ai/extract-document` | Sınav belgelerinden soru çıkarır. |

### 4.4 İstemci tarafı akıllı eşleştirme (model yok, anlık)

- **`draftClusteringService.ts`** — yazılan parçayı havuzdaki taslaklarla karşılaştırır (kök benzerliği, şık
  kümesi, ortak tıbbi varlık), %35 üstü adayları önerir, birleştirme kararı verir. 5.000 kavramlık
  `medicalConcepts5000.json` sözlüğü **boşta yüklenir**; bulanık arama uzunluk + ilk harf gruplu ve önbellekli.
- **`medicalPredictorService.ts`** — metinden kurul/ders tahmini, çapraz kurul uyarısı.
- **`learnMatcher.ts`** — çıkmış soruyu ilgili ders slaytına bağlar (desteler arka planda parça parça yüklenir).

### 4.5 Deneysel / ileri AI betikleri (`scripts/advanced_ai/`)

Faz 5–7 çalışmaları: çoklu model uzlaşısı (`multi_ai_consensus_phase5.py`), derin metadata
(`deep_metadata_generator_phase6.py`), tıbbi eş-anlamlı sözlük ve birlikte görünme grafiği
(`thesaurus_anchor_phase6_5.py`), GraphRAG bilgi grafı (`graph_rag.py`), BM25 + bge-m3 hibrit arama
(`hybrid_search.py`), hiyerarşik bellek (`memory_os.py`), ReAct + guardrail (`react_guardrails.py`), mikro-ajan
anlatım modellemesi ve 100 altın örnek (`microagent_storyteller_phase7.py`, `generate_perfect_100_stories.py`,
`build_phase7_gold_100.py`), slayt yeniden düzenleme (`reconstruct_slides_phase7_5.py`), RAG ölçümü
(`rag_evaluator.py`), hepsini zincirleyen `orchestrator.py`. Eğitim verisi `training_data/`, model çıktısı
`models/` altındadır.

---

## 5. Sunucu uçları (`server.ts`)

130 `/api` ucu. Gruplar:

| Grup | Uç sayısı | Amaç |
|---|---|---|
| `/api/admin/*` | 31 | Yönetim: kullanıcılar, SMTP, Drive ayarları, şikâyet çözme, betik/pipeline çalıştırma, DB dışa/içe aktarma, yedek. `requireAdmin` korumalı. |
| `/api/ai/*` | 17 | Model çağrıları (bkz. 4.3), anahtar sağlığı, hata kayıtları, AI etkileşim geçmişi. |
| `/api/questions/*` | 14 | Soru havuzu: ekleme, parça/şık/oy, iddia edilen cevap, AI kurma, toplu içe aktarma. |
| `/api/past-exams/*` | 13 | Çıkmış sorular: liste (kimlikle arama dahil), yorum, şikâyet, oy, güncelleme (gizleme), **silme**, doğrulama. |
| `/api/automation/*` | 12 | Yerel senkron, Drive durum, masaüstü klasör tarama, Windows servisi, slayt görüntüsü. |
| `/api/search/*` | 3 | `/api/search` (eski), `/api/search/all` (genel arama, sayfalı), `/api/search/spell` (yazım önerisi). |
| `/api/rag/*` | 4 | İndeks durumu, istatistik, yeniden indeksleme. |
| `/api/lecture-notes/*`, `/api/slides/*`, `/api/summaries/*`, `/api/transcriptions/*` | 12 | Ders içerikleri. |
| `/api/deepseek/*`, `/api/studio/*`, `/api/audit/*`, `/api/worker/*` | 9 | DeepSeek katkı verisi, taslak stüdyosu, denetim, arka plan işçisi. |
| Diğer | — | `/api/committees`, `/api/users`, `/api/health`, `/api/system/*`, e-posta, NotebookLM, Drive, Gemini. |

Açılışta: RAG indeksi kurulur, yazım sözlüğü boşta ısıtılır, DeepSeek klasör izleyicisi başlar, Supabase komut
yoklayıcısı çalışır. **Yan etki:** `data/local_rag_chunks.json` yeniden üretilir; başlatmadan sonra
`git status` ile istenmeyen `data/` değişikliklerine bakılmalıdır.

> **Bilinen açık:** `requireAdmin`, `x-admin-email` başlığına ve loopback IP'ye güvenir (tünel trafiği
> loopback görünür); AI uçlarında kimlik doğrulama ve hız sınırı yoktur.

---

## 6. Ön yüz

### 6.1 Kabuk
- `main.tsx`: tema, klavye/görsel alan takibi (`--vvh`, `kb-open`), hata sınırı.
- `App.tsx`: yönlendirme (`router.ts`, yol tabanlı: `/`, `/ogren`, `/sozluk`, `/kartlar`, `/sorular`, `/cikmis`,
  `/calis`, `/test`, `/siralama`, `/ozetler`, `/asistan`, `/ara/<sorgu>`, `/manage` …), splash + 5 adımlı
  tanıtım/kayıt (`onboarding/`), yeni soru eklenince ona kaydırma.
- Gezinme: masaüstünde daraltılabilir sol menü (`AppRail`), tablette simge rayı, telefonda alt sekme çubuğu.
- Ortak arayüz: `ui/Toast`, `ui/TooltipHost` (uygulama geneli Material ipucu), `ui/Collapsible`,
  `search/SearchPalette` (Ctrl+K / `/`).

### 6.2 Ekranlar
| Ekran | Bileşen | Öz |
|---|---|---|
| Soru ekle | `QuickAddHero` | Tek kutu; ders/numara akıllı etiketleri, yazım önerisi, benzer çıkmış sorular, taslak eşleşmeleri. |
| Soru havuzu | `QuestionCard`, `MetricsBar` | Kurul havuzu, parça/şık oylama, AI kurma. |
| Çıkmış sorular | `PastExamsView` | Arama, Sırala, filtre popup'ı (kurul, ders, yıl, cevap, açıklama, doğrulama…), yorum, şikâyet. |
| Öğren | `learn/InteractiveDeckView` | Slayt slayt ders; desteler `deckStore` ile parça parça yüklenir. |
| Kartlar | `flashcards/FlashcardsView` | Leitner aralıklı tekrar, süzgeçler, favoriler, ileri/geri. |
| Çalış | `study/StudyHub` | Soru çöz, test (hızlı test tüm bankadan), Listelerim (tekrar + favoriler), notlar. |
| Sözlük | `encyclopedia/MedicalEncyclopediaView` | Kategori, kurul, ders, harf, doğrulanmış, kaydedilenler, sıralama. |
| Ders özetleri | `LectureSummariesView` | Resmi ders adı/hocası, kaynak PDF yılı, kurula göre ders süzgeci. |
| Asistan | `LocalAiChatView` | Tek ekrana sığan sohbet; teknik ayarlar yalnız yöneticiye. |
| Arama | `search/SearchView` | Tüm veri setleri, tür süzgeci, kaynağa git. |
| Yönetim | `manage/ManageConsole` | Gelen kutusu, moderasyon (şikâyet: düzelt / AI / taslağa çevir / gizle / sil), veriler, taslak stüdyosu, kullanıcılar, betikler, sistem, otomasyon. |

### 6.3 Derleme
- `npm run dev` — sunucu + Vite (http://localhost:3000). `npm run lint` — `tsc --noEmit`. `npx vite build`.
- `vite.config.ts` içindeki `splitLearningDecks` eklentisi öğrenme destelerini derlemede
  `src/data/decks/` altına böler (git'e girmez).

---

## 7. Betik kataloğu

`package.json` kısayolları:

| Komut | Betik |
|---|---|
| `verify:answers` / `verify:watch` / `verify:all` | `scripts/verify-question-answers.mjs` — cevap doğrulama. |
| `slides:audit` / `slides:match` / `slides:sync` / `slides:stats` | Slayt ↔ soru ilişkisi denetimi ve eşleştirme. |
| `check:updates` / `sync:updates` | `detect-database-updates.mjs` — veri değişikliği tespiti. |
| `transcribe:audio` / `transcribe:watch` | Drive ses kayıtlarının dökümü. |
| `rag:index` / `rag:index:all` | RAG bilgi indeksleme. |
| `decks:build` | `build_learning_decks.py` — öğrenme destesi üretimi. |
| `sync:deepseek` | DeepSeek verisini içe alma. |
| `sync:drive` / `sync:drive:dry` | Drive müfredat orkestrasyonu. |
| `glossary:build` | Tıbbi sözlük üretimi. |
| `git:sync` / `git:watch` | Otomatik git senkronu. |

Betikler yönetim konsolundaki **Scriptler** bölümünden de çalıştırılabilir (`automation-runner.mjs`,
`/api/admin/scripts/*`). Aşağıdaki tam döküm, her dosyanın kendi başlık açıklamasından derlenmiştir; başlığı
olmayan dosyalar adına göre gruplanmıştır.


### AI redaksiyon (4)

| Dosya | Açıklama |
|---|---|
| `scripts/archive/ai_studio_deep_curator.py` | MedSoru Gemini Shadow Judge — bozuk tıp sorularını AI Studio ile onarır. |
| `scripts/background-ai-redactor.mjs` | MedSoru Arkaplan Yapay Zeka Redaksiyon & İyileştirme Motoru (scripts/background-ai-redactor.mjs) Bu subagent/daemon script: 1. meds_sorular_txt klasöründeki tüm sınav dosyalarını en ince ayrıntısına kadar ayrıştırır (sor |
| `scripts/archive/curriculum_daily_pipeline.py` | scripts/archive/curriculum_daily_pipeline.py ======================================================================================== DÖNEM 3 GÜNLÜK MÜFREDAT VE ETKİLEŞİMLİ ÖĞRENME OTOMASYONU (MASTER CURRICULUM PIPELINE) ======= |
| `scripts/deep-ai-redactor.mjs` | MedSoru Derin Tıbbi Yapay Zeka Redaksiyon Motoru (scripts/deep-ai-redactor.mjs) Kurallar: 1. Her soru için en az 20 saniye süre ayrılır (derin analiz ve oran sınırlaması). 2. Asla kalıp / laf kalabalığı cümleler ("Bu sor |

### DeepSeek veri hattı (8)

| Dosya | Açıklama |
|---|---|
| `scripts/ds_assemble.py` | Adım 4: Batch çıktılarını birleştir, doğrula, onar ve tek JSONL dosyası üret. |
| `scripts/ds_batches.py` | Adım 2 (v2): Soru -> ders notu aday eşleştirmesi + AI doğrulama iş birimleri. - Final/Bütünleme sınavları kümülatif olduğundan TÜM kurul ders notlarına bakar. - Her aday için en ilgili bölüm (heading) ve kanıt pasajı çık |
| `scripts/archive/ds_deliver.py` | Adım 5: Doğrulanmış JSONL'i hedef klasöre yaz ve bütünlüğünü doğrula. Hedef: C:\\Users\\indui\\Desktop\\meds_database\\deepseek_data |
| `scripts/ds_pipeline.py` | Dönem 3 - Çıkmış soru + ders notu eşleştirme ve düzeltme hattı. Adım 1: Deterministik normalizasyon + ders notu kataloğu + iş birimi (batch) üretimi. |
| `scripts/ds_quote_index.py` | Tüm ders notları için global doğrulama indeksi + alıntı doğrulama. |
| `scripts/archive/ds_report.py` | Teslim edilen dosyanın kaynak 1279 soruya karşı kapsama ve kalite raporu. |
| `scripts/archive/ds_retry.py` | Eksik/kalitesiz kalan sorular için tamamlayıcı (retry) batch üretir. |
| `scripts/archive/ds_schema.py` | _başlık açıklaması yok_ |

### Denetim ve doğrulama (16)

| Dosya | Açıklama |
|---|---|
| `scripts/audit-and-disconnect-faulty-slides.mjs` | MedSoru Slayt İlişkisi Denetim ve Hatalı İlişkileri Kesme Scripti (Script 1) (scripts/audit-and-disconnect-faulty-slides.mjs) Amaç: 1. Çıkmış sorular ile ilişkilendirilen her bir ders slaytını ve sayfasını kontrol eder.  |
| `scripts/archive/audit_and_fix_flashcards.py` | scripts/archive/audit_and_fix_flashcards.py Audits all flashcards across all interactive learning decks. Guarantees that every flashcard has BOTH: - front AND question (front = front or question) - back AND answer (back = back o |
| `scripts/archive/audit_donem3_master.mjs` | _başlık açıklaması yok_ |
| `scripts/archive/audit_drive_pdf_decks.py` | _başlık açıklaması yok_ |
| `scripts/check-online-status.ts` | MedSoru - Online Veritabanı ve Yapay Zeka Limit Denetleme Scripti (check-online-status.ts) Bu script: 1. Online Firebase Firestore bağlantısını ve günlük Spark 50K okuma kotasını denetler. 2. Online Supabase PostgreSQL b |
| `scripts/archive/check_missing_drive_pdfs.py` | _başlık açıklaması yok_ |
| `scripts/detect-database-updates.mjs` | scripts/detect-database-updates.mjs Veritabanında Soru Bazında Güncelleme Tespit ve Ekonomik Artımlı Senkronizasyon Scripti Kullanım: node scripts/detect-database-updates.mjs             -> Güncellemeleri tespit eder ve  |
| `scripts/detect-faulty-ocr.mjs` | _başlık açıklaması yok_ |
| `scripts/archive/ds_check_quotes.py` | _başlık açıklaması yok_ |
| `scripts/archive/ds_validate.py` | _başlık açıklaması yok_ |
| `scripts/archive/find_truly_missing_pdfs.py` | _başlık açıklaması yok_ |
| `scripts/archive/inspect_check_result_files.py` | _başlık açıklaması yok_ |
| `scripts/self-healing-auditor.mjs` | MedSoru Otonom Kendi Kendini Denetleyen ve İyileştiren Sistem (Self-Healing Auditor) (scripts/self-healing-auditor.mjs) Görevleri: 1. Veritabanındaki tüm soruları ve ders notlarını periyodik veya tetiklemeli denetler. 2. |
| `scripts/verify-question-answers.mjs` | MedSoru Çıkmış Soru ve Cevap Doğrulama Motoru (scripts/verify-question-answers.mjs) Amaç: Çıkmış soruların cevaplarını; hem amfi ders notları/slaytları hem de güncel tıp literatürü ve internet bilgisi ile çapraz kontrole |
| `scripts/archive/verify_clustering_tuning.ts` | _başlık açıklaması yok_ |
| `scripts/archive/verify_integrity.py` | _başlık açıklaması yok_ |

### Deste / içerik üretimi (68)

| Dosya | Açıklama |
|---|---|
| `scripts/archive/auto_scheduled_batch_builder.py` | scripts/archive/auto_scheduled_batch_builder.py Manages the structured batch queue for all Kurul 1 lectures. Processes each lecture into deep %500 interactive decks on a planned schedule. |
| `scripts/build-database-json.mjs` | scripts/build-database-json.mjs MedSoru Veritabanı JSON Üretim ve Senkronizasyon Motoru Hedef Klasör: meds_database\database_json Bu script: 1. Tüm dönem ve kurullar için klasör hiyerarşisini kurar |
| `scripts/archive/build_all_curriculum_decks.py` | scripts/archive/build_all_curriculum_decks.py Generates the remaining 6 authentic, faculty-grounded 24-slide learning decks: 1. learn-ileri-tumor-genetigi-metabolizmasi 2. learn-tumor-immunolojisi-metastaz 3. learn-tumor-evrelem |
| `scripts/build_batch1_deck.py` | _başlık açıklaması yok_ |
| `scripts/build_batch2_deck.py` | _başlık açıklaması yok_ |
| `scripts/build_batch3_deck.py` | _başlık açıklaması yok_ |
| `scripts/build_batch4_deck.py` | Master Learning Deck Generator - Batch 4: Akut Enflamasyon: Vasküler Değişiklikler ve Hücresel Olaylar Prof. Dr. Hikmet Keleş - Tıbbi Patoloji (Dönem 3 Kurul 1) |
| `scripts/archive/build_batch_drive_decks.py` | scripts/archive/build_batch_drive_decks.py Generates the next batch of Google Drive lectures for Dönem 3 Kurul 1: 1. Tromboz Patofizyolojisi, Virchow Triadı ve Trombofili (Prof. Dr. Hikmet Keleş) 2. Emboli Tipleri, Enfarktüs ve  |
| `scripts/archive/build_bebek_beslenmesi_deck.py` | Bebek Beslenmesi, Anne Sütü İmmünolojisi, Tamamlayıcı Beslenme ve Malnütrisyon Güvertesi Sosyal Pediatri ve Çocuk Sağlığı Anabilim Dalı 24 Kapsamlı Slayt ve Pediatri Uzmanlık/Komite Sınavı Düzeyinde Sorular |
| `scripts/archive/build_chemical_mediators_deck.py` | scripts/archive/build_chemical_mediators_deck.py Generates the comprehensive 22-slide interactive learning deck for: 'Enflamasyonun Kimyasal Mediyatörleri: Vazoaktif Aminler, Araşidonik Asit Metabolitleri, Sitokinler ve Komplema |
| `scripts/build_chunked_study_questions.py` | scripts/build_chunked_study_questions.py Generates original, high-yield practice study questions for each lecture derived directly from the authentic lecture content (synthesis narrative, coreContent, spotPearls, profess |
| `scripts/build_full_drive_slides.mjs` | _başlık açıklaması yok_ |
| `scripts/archive/build_halk_sagligi_deck.py` | Builder script for 24 high-yield academic slides: Halk Sagligi Tarihcesi, Felsefesi ve Koruyucu Hekimlik Ilkeleri |
| `scripts/archive/build_hypersensitivity_deck.py` | build_hypersensitivity_deck.py Generates the comprehensive 500% depth interactive learning deck for: 'learn-asiri-duyarlilik-ve-otoimmunite' (Prof. Dr. Hikmet Keleş / Robbins 11. Baskı) Includes: - 24 rich slides with sy |
| `scripts/archive/build_karsinojenez_molekuler_deck.py` | scripts/archive/build_karsinojenez_molekuler_deck.py Generates full 24-slide high-yield interactive learning deck for: Prof. Dr. Hikmet Keleş - Karsinojenezin Moleküler Temeli Extracted from: 17)Karsinojenezin Moleküler Temeli.p |
| `scripts/archive/build_kronik_enflamasyon_deck.py` | scripts/archive/build_kronik_enflamasyon_deck.py Generates full 24-slide high-yield interactive learning deck for: Prof. Dr. Hikmet Keleş - Kronik ve Granülomatöz Enflamasyon Adheres strictly to all curriculum and database const |
| `scripts/archive/build_kronik_part1.py` | Part 1: Slides 1 to 12 for Kronik ve Granülomatöz Enflamasyon Deck. |
| `scripts/archive/build_kronik_part2.py` | Part 2: Slides 13 to 24 for Kronik ve Granülomatöz Enflamasyon Deck. |
| `scripts/build_learning_decks.py` | build_learning_decks.py (5x Ayrıntı, Akıl Kartları & Akıcı Sentez Versiyonu) ============================================================================= Bu script: 1. c:\\Users\\indui\\Desktop\\meds_database\\transcrip |
| `scripts/archive/build_medical_concepts_5000.py` | Master 5,000 Medical Concepts Knowledge Base Generator Gathers, synthesizes, enriches and standardizes 5,000+ medical concepts for MedSoru. |
| `scripts/archive/build_medical_encyclopedia.py` | Medical Encyclopedia & Dictionary Generator Grounded strictly in authentic lecture notes from Kurul 1, 2, 3 faculty text files: - 26)Böbrek Tümörleri.txt (Prof. Dr. Hikmet Keleş) - 26)Mesane Hastalıkları ve Tümörleri.txt |
| `scripts/archive/build_mega_medical_encyclopedia.py` | Mega Medical Encyclopedia & Comprehensive Dictionary Generator Scales the medical dictionary to 500+ verified medical diseases, drugs, pathology findings, pathogens, and genetic syndromes strictly grounded in the Dönem 3 |
| `scripts/archive/build_remaining_drive_decks.py` | _başlık açıklaması yok_ |
| `scripts/archive/build_tumor_biyolojisi_deck.py` | scripts/archive/build_tumor_biyolojisi_deck.py Generates full 24-slide high-yield interactive learning deck for: Prof. Dr. Hikmet Keleş - Tümör Biyolojisi ve Terminolojisi Replaces the old 4-slide stub with an authentic, deep, % |
| `scripts/archive/build_uriner_epidemiyoloji_deck.py` | Build High-Quality Academic Deck: 'learn-uriner-sistem-enfeksiyonlari-epidemiyoloji' (24 Slayt) Kaynak: Üriner Sistem Enfeksiyonlarının Epidemiyoloji, Etyoloji ve Semptomatolojisi Uzman Tıbbi Mikrobiyoloji ve Enfeksiyon  |
| `scripts/archive/complete_genetics_pediatric_deck.py` | complete_genetics_pediatric_deck.py Completes slides 13 to 24 for 'learn-genetik-pediatrik-cevresel-patoloji', adds encyclopedia and glossary terms, and handles chunked study questions. |
| `scripts/archive/complete_missing_batches.py` | complete_missing_batches.py (Hızlı ve Optimize) Eksik kalan 28 batch için doğrulama ve redaksiyon çıktılarını (.meds_ds/out/<batchId>.json) üretir. Ders notu kanıtları hızlı taranır ve açıklama/şık kalitesi standartlara  |
| `scripts/archive/generate_cell_injury_deck.py` | scripts/archive/generate_cell_injury_deck.py Generates the deep (%500 detail) 24-slide learning deck for: "Hücre Hasarı, Hücre Ölümü ve Nekroz" (Tıbbi Patoloji - Prof. Dr. Hikmet Keleş) Incorporating 24 slides, 48 3D flashcards, |
| `scripts/archive/generate_cellular_adaptation_deck.py` | scripts/archive/generate_cellular_adaptation_deck.py Generates the deep (%500 detail) 24-slide learning deck for: "Hücresel Adaptasyonlar: Atrofi, Hipertrofi, Hiperplazi, Metaplazi ve Otofaji" (Tıbbi Patoloji - Prof. Dr. Hikmet  |
| `scripts/archive/generate_chromosomal_diseases_deck.py` | scripts/archive/generate_chromosomal_diseases_deck.py Generates the comprehensive %500 detail 22-slide learning deck for: "Kromozomal Hastalıklar ve Genetik Danışma" (Tıbbi Genetik - Dr. Öğr. Üyesi Serap Arslan) Incorporating 22 |
| `scripts/archive/generate_chronic_inflammation_deck.py` | scripts/archive/generate_chronic_inflammation_deck.py Generates the deep (%500 detail) 22-slide learning deck for: "Kronik Enflamasyon, Granülomlar ve Doku Onarımı" (Tıbbi Patoloji - Prof. Dr. Hikmet Keleş) Incorporating 22 slid |
| `scripts/archive/generate_dismorphology_deck.py` | scripts/archive/generate_dismorphology_deck.py Generates the deep (%500 detail) 20-slide learning deck for: "Dismorfolojide Genetik Terminoloji ve Malformasyonlar" (Tıbbi Genetik - Dr. Öğr. Üyesi Serap Arslan) Incorporating 20 s |
| `scripts/archive/generate_donem3_butunleme_redakte_sorular.mjs` | generate_donem3_butunleme_redakte_sorular.mjs Karabük Üniversitesi Tıp Fakültesi Dönem 3 Bütünleme Sınavı (donem3b) Çıkmış Sorularını %100 Doğrulanmış Tıbbi Şemaya Göre Redakte ve Senkronize Eden Master Script. Kapsam: - |
| `scripts/archive/generate_donem3_final_redakte_sorular.mjs` | generate_donem3_final_redakte_sorular.mjs Karabük Üniversitesi Tıp Fakültesi Dönem 3 Final Sınavı (donem3f) Çıkmış Sorularını %100 Doğrulanmış Tıbbi Şemaya Göre Redakte ve Senkronize Eden Master Script. Tüm 261 Final Sor |
| `scripts/archive/generate_epidemic_control_deck.py` | scripts/archive/generate_epidemic_control_deck.py Generates the comprehensive %500 detail 18-slide learning deck for: "Salgın Hastalıklarda Kontrol, Sürveyans ve Korunma" (Halk Sağlığı - Uzm. Dr. Erkay Nacar) Incorporating 18 sl |
| `scripts/generate_genetics_pediatric_complete.py` | generate_genetics_pediatric_complete.py Master builder for 'learn-genetik-pediatrik-cevresel-patoloji' (Kurul 1). Prof. Dr. Hikmet Keleş & Robbins 11th edition. Constructs: 1. 24 high-yield slides with structured spot pe |
| `scripts/archive/generate_hemodynamics_deck.py` | scripts/archive/generate_hemodynamics_deck.py Generates the deep (%500 detail) 22-slide learning deck for: "Hemodinamik Bozukluklar: Ödem, Hiperemi, Konjesyon, Tromboz ve Kanama" (Tıbbi Patoloji - Prof. Dr. Hikmet Keleş) Incorpo |
| `scripts/archive/generate_hypersensitivity_complete.py` | generate_hypersensitivity_complete.py Master builder for 'learn-asiri-duyarlilik-ve-otoimmunite'. Constructs: 1. 24 high-yield slides with structured spot pearls, flashcards, core content, practice questions 2. 32 compre |
| `scripts/archive/generate_infection_isolation_deck.py` | scripts/archive/generate_infection_isolation_deck.py Generates the comprehensive %500 detail 20-slide learning deck for: "Hastane Enfeksiyonları ve İzolasyon Önlemleri" (Enfeksiyon Hastalıkları & Klinik Mikrobiyoloji - Dr. Rüvey |
| `scripts/archive/generate_intracellular_accumulations_deck.py` | scripts/archive/generate_intracellular_accumulations_deck.py Generates the deep (%500 detail) 24-slide learning deck for: "İntraselüler Birikimler ve Patolojik Kalsifikasyonlar" (Tıbbi Patoloji - Prof. Dr. Hikmet Keleş) Incorpor |
| `scripts/archive/generate_ischemia_infarct_shock.py` | generate_ischemia_infarct_shock.py Prof. Dr. Hikmet Keleş - Ders 12: Emboli, Enfarktüs ve Şok Patolojisi (Kurul 1 / Dönem 2) 24 slaytlık %500 derinlikli öğrenme güvertesi, 24 özgün çalışma sorusu, chunk_8 ve index.json e |
| `scripts/archive/generate_kurul2_redakte_sorular.mjs` | generate_kurul2_redakte_sorular.mjs Dönem 3 Kurul 2 (TIP 320 - NÖROPSİKİYATRİ KURULU) çıkmış sorularını: 1. Nöroloji 2. Psikiyatri 3. Tıbbi Farmakoloji (Nörofarmakoloji & Psikofarmakoloji) 4. Beyin ve Sinir Cerrahisi (Nö |
| `scripts/archive/generate_kurul3_redakte_sorular.mjs` | generate_kurul3_redakte_sorular.mjs Dönem 3 Kurul 3 (TIP 330 - GASTROİNTESTİNAL SİSTEM KURULU) çıkmış sorularını: 1. Tıbbi Patoloji (GİS, KC, Safra Yolları, Pankreas Patolojisi) - 45 Soru 2. Tıbbi Farmakoloji (GİS İlaçla |
| `scripts/archive/generate_kurul4_amfi_ozetleri.mjs` | generate_kurul4_amfi_ozetleri.mjs meds_database\kurul_ders_notlari_txt\Kurul 4 altındaki 46 adet amfi ders notunu okur; her bir ders notunun klinik, farmakolojik ve patolojik özetini çıkararak C:\U |
| `scripts/archive/generate_kurul4_redakte_sorular.mjs` | generate_kurul4_redakte_sorular.mjs Dönem 3 Kurul 4 (TIP 340 - DOLAŞIM, SOLUNUM VE TÜMÖR KURULU) çıkmış sorularını: 1. Kardiyoloji ve Kalp Damar Cerrahisi (KVS) - 35 Soru 2. Göğüs Hastalıkları ve Göğüs Cerrahisi (Solunum |
| `scripts/archive/generate_kurul5_amfi_ozetleri.mjs` | generate_kurul5_amfi_ozetleri.mjs meds_database\kurul_ders_notlari_txt\Kurul 5 altındaki 75 adet amfi ders notunu okur; her bir ders notunun klinik, farmakolojik ve patolojik özetini çıkararak C:\U |
| `scripts/archive/generate_kurul5_redakte_sorular.mjs` | generate_kurul5_redakte_sorular.mjs Karabük Üniversitesi Tıp Fakültesi Dönem 3 Kurul 5 (TIP 350 - Ortopedi, Travmatoloji ve Hematopoetik Sistem) Çıkmış Sorularını %100 Doğrulanmış Tıbbi Şemaya Göre Redakte ve Senkronize  |
| `scripts/archive/generate_kurul6_amfi_ozetleri.mjs` | generate_kurul6_amfi_ozetleri.mjs meds_database\kurul_ders_notlari_txt\Kurul 6 altındaki 53 adet amfi ders notunu okur; her bir ders notunun klinik, farmakolojik ve patolojik özetini çıkararak C:\U |
| `scripts/archive/generate_kurul6_redakte_sorular.mjs` | generate_kurul6_redakte_sorular.mjs Karabük Üniversitesi Tıp Fakültesi Dönem 3 Kurul 6 (TIP 360 - Endokrin, Metabolizma ve Yaşlanma) Çıkmış Sorularını %100 Doğrulanmış Tıbbi Şemaya Göre Redakte ve Senkronize Eden Master  |
| `scripts/generate_medical_glossary.py` | scripts/generate_medical_glossary.py Medical glossary generator and synchronizer for Dönem 3 Kurul 1. Ensures medical_glossary.json remains valid, properly formatted, and sorted. |
| `scripts/archive/generate_redakte_sorular.mjs` | generate_redakte_sorular.mjs Dönem 3 Kurul 1 çıkmış sorularını: 1. Enfeksiyon Hastalıkları (62 soru) 2. Tıbbi Patoloji (71 soru) 3. Halk Sağlığı (33 soru) 4. Tıbbi Biyoloji ve Genetik - TBG (15 soru) 5. Üroloji (16 soru) |
| `scripts/archive/generate_slide_pdf_mappings.py` | _başlık açıklaması yok_ |
| `scripts/archive/generate_thrombosis_complete.py` | generate_thrombosis_complete.py Ders: Prof. Dr. Hikmet Keleş - Tromboz Patofizyolojisi (Kurul 1 / Dönem 2) Tüm 24 slayt, spotlar, flashcardlar, 24 özgün çalışma sorusu, chunk_8 ve sözlük/ansiklopedi entegrasyonu. |
| `scripts/medical_data_builder.py` | Medical Data Builder Module Generates comprehensive clinical, pharmacological, microbiological, pathological, and basic science concept entries. |
| `scripts/rebuild-all-past-questions.mjs` | _başlık açıklaması yok_ |
| `scripts/archive/rebuild_aging_and_repair_decks.py` | Rebuild Cellular Aging & Tissue Repair Decks with High-Quality Medical Standards 1. learn-hucresel-yaslanma-ve-hucr (24 Slayt) 2. learn-doku-onarimi-yara-iyilesmesi (24 Slayt) Prof. Dr. Hikmet Keleş & Robbins Pathology |
| `scripts/archive/rebuild_all_14_clean_decks.py` | Rebuilds the 14 decks with 100% authentic, high-yield Turkish medical lecture data matching Prof. Dr. Hikmet Keleş and faculty syllabi from Kurul 1 text files. Completely eliminates all generic placeholder text: - "Müfre |
| `scripts/archive/rebuild_bobrek_tumorleri_deck.py` | Rebuild Kidney Tumors Deck with High-Quality Medical Standards learn-bobrek-tumorleri (24 Slayt) Prof. Dr. Hikmet Keleş & Robbins Pathology |
| `scripts/archive/rebuild_cybh_high_quality.py` | Rebuilds learn-cinsel-yolla-bulasan-enfe with rich, fully-articulated medical narrative, completely removing all robotic templates, broken characters, and meaningless headings. |
| `scripts/archive/rebuild_genital_and_anacocuk_decks.py` | Rebuild Genital Infections & Maternal-Child Health Decks with High-Quality Medical Standards 1. learn-genital-enfeksiyonlar (24 Slayt) 2. learn-ana-cocuk-sagligi (24 Slayt) Enfeksiyon Hastalıkları & Halk Sağlığı Anabilim |
| `scripts/archive/rebuild_genital_anomalies_and_prenatal.py` | Rebuild Congenital Genital Anomalies & Prenatal Diagnosis Decks with Highest Medical Quality Standards 1. learn-dogumsal-genital-anomaliler (24 Slides - Tıbbi Genetik / Embriyoloji) 2. learn-prenatal-tani (24 Slides - Tı |
| `scripts/archive/rebuild_group1_nephrology.py` | Rebuild Nephrology Glomerular & Tubulointerstitial Decks with High-Quality Medical Standards 1. learn-glomeruler-hastaliklar-nefrotik (24 Slayt) 2. learn-glomeruler-hastaliklar-nefritik (24 Slayt) 3. learn-tubulointersti |
| `scripts/archive/rebuild_mesane_deck.py` | Rebuild Bladder Diseases and Tumors Deck with High-Quality Medical Standards learn-mesane-hastaliklari-tumorleri (24 Slayt) Prof. Dr. Hikmet Keleş & Robbins Pathology |
| `scripts/archive/rebuild_nefritik_deck.py` | Rebuild Nefritik Sendrom Deck with High-Quality Medical Standards learn-glomeruler-hastaliklar-nefritik (24 Slayt) Prof. Dr. Hikmet Keleş & Robbins Pathology |
| `scripts/archive/rebuild_patoloji_giris.py` | Rebuilds Part 1 decks (Patolojiye Giriş, Hücresel Yaşlanma, Doku Onarımı) with complete grammatical sentences, deep medical narratives, and red/blue spot pearls. |
| `scripts/archive/rebuild_tubulointerstisyel_deck.py` | Rebuild Tubulointerstitial Diseases Deck with High-Quality Medical Standards learn-tubulointerstisyel-hastaliklar (24 Slayt) Prof. Dr. Hikmet Keleş & Robbins Pathology |
| `scripts/archive/rebuild_vaskuler_kistik_deck.py` | Rebuild Vascular & Cystic Kidney Diseases Deck with High-Quality Medical Standards learn-vaskuler-kistik-bobrek-hastaliklari (24 Slayt) Prof. Dr. Hikmet Keleş & Robbins Pathology |
| `scripts/archive/sync_drive_curriculum_and_build_decks.py` | _başlık açıklaması yok_ |

### Değerlendirme (1)

| Dosya | Açıklama |
|---|---|
| `scripts/archive/eval-rag-system.ts` | _başlık açıklaması yok_ |

### Diğer (50)

| Dosya | Açıklama |
|---|---|
| `scripts/automation-runner.mjs` | MedSoru Central Script & Automation Runner Engine ---------------------------------------------------- Bu script; mevcut ve gelecekte oluşturulacak TÜM scriptlerin dinamik taranmasını, manuel veya zincirleme (pipeline) o |
| `scripts/archive/bulletize_all_decks.py` | scripts/archive/bulletize_all_decks.py Converts all slides across all 17 interactive learning decks into structured, hierarchical markdown with clear bullet points, spot callouts, and curriculum synthesis. |
| `scripts/archive/compile-summaries-catalog.mjs` | MedSoru Ders Özetleri ve Spot Bilgi Kataloğu Derleyicisi (scripts/archive/compile-summaries-catalog.mjs) meds_database\redakte_ozet altındaki 347 adet Markdown ders özetini okur, ayrıştırır ve web uygulama |
| `scripts/deploy-gh-pages.cjs` | _başlık açıklaması yok_ |
| `scripts/archive/diagnose_down_drafts.ts` | _başlık açıklaması yok_ |
| `scripts/fast_hybrid_server.py` | MedSoru Low-Latency Hybrid Serving API — FastAPI + DuckDB (cursor-per-request). |
| `scripts/gpu_recovery.sh` | MedSoru GPU & Audio Otomatik Uyandırma ve Kurtarma Scripti |
| `scripts/inspect-sources.mjs` | _başlık açıklaması yok_ |
| `scripts/archive/inspect_genetics_pediatric.py` | _başlık açıklaması yok_ |
| `scripts/archive/inspect_hypersensitivity.py` | _başlık açıklaması yok_ |
| `scripts/archive/integrate_batch1_decks.py` | Integrate Batch 1 Rebuilt Decks into src/data/interactive_learning_decks.json Decks: 1. learn-uriner-sistem-enfeksiyonlari-epidemiyoloji 2. learn-uriner-sistemin-spesifik-enfeksiyonlari 3. learn-enfeksiyon-epidemiyoloji  |
| `scripts/archive/integrate_batch2_decks.py` | Integrate Batch 2 Rebuilt Decks into src/data/interactive_learning_decks.json Decks: 1. learn-enflamasyon-kimyasal-mediyatorleri 2. learn-enfeksiyon-temel-kavramlar 3. learn-sistemik-hastaliklar-bobrek-hasari 4. learn-ur |
| `scripts/archive/integrate_batch3_decks.py` | _başlık açıklaması yok_ |
| `scripts/archive/integrate_batch4_decks.py` | _başlık açıklaması yok_ |
| `scripts/archive/integrate_batch5_decks.py` | _başlık açıklaması yok_ |
| `scripts/archive/integrate_deepseek_jsonl.py` | scripts/archive/integrate_deepseek_jsonl.py ----------------------------------- Entegrates DeepSeek-verified Dönem 3 questions (meds_donem3_sorulari_duzeltilmis.jsonl) directly into: 1. src/data/pastQuestions.json 2. data/pastQu |
| `scripts/archive/integrate_new_batch1.py` | _başlık açıklaması yok_ |
| `scripts/archive/integrate_new_batch2.py` | _başlık açıklaması yok_ |
| `scripts/archive/integrate_new_batch3.py` | _başlık açıklaması yok_ |
| `scripts/archive/integrate_new_batch4.py` | _başlık açıklaması yok_ |
| `scripts/archive/integrate_new_batch5.py` | _başlık açıklaması yok_ |
| `scripts/archive/lakehouse_migrator.py` | MedSoru Medical Lakehouse Builder — JSON/JSONL/SQLite → Parquet gölü. |
| `scripts/manage-service.sh` | manage-service.ps1'in Linux karşılığı. Kullanım: manage-service.sh <install-and-start/status/stop/sync-now/notify> [başlık] [mesaj] Servis, systemd --user altında "meds-local-sync.service" olarak çalışır. |
| `scripts/manage-slide-relations.mjs` | MedSoru Çıkmış Soru & Amfi Slayt İlişki Yönetim Motoru (Master Runner) (scripts/manage-slide-relations.mjs) Bu betik iki ana scripti entegre olarak yönetir: 1. Script 1 (Denetim & Kesme): Çıkmış sorularla ilişkilendirile |
| `scripts/master_controller.py` | MedSoru Master Orchestrator & Supervisor (scripts/master_controller.py) En Yönetici, En Kapsamlı Sistem & Donanım Yöneticisi. Özellikler: 1. Başlangıçta Terminal & GUI üzerinden Çalışma Modu Seçimi: - 1: Normal (GPU 1-3  |
| `scripts/archive/master_learning_engine.py` | MASTER LEARNING ENGINE (Eğitim Metodolojisi & Otomasyon Motoru) ============================================================== Tüm dersler için uçtan uca öğrenim sunumlarını (%500 derinlik, akıl kartları, sentez ders not |
| `scripts/medical_data_clinical.py` | Clinical Medicine Master Concepts Database (Cardiology, Pulmonology, GI, Nephrology, Endocrine, Heme, Rheum, Neuro, Peds, OB/GYN, Surgery) |
| `scripts/medical_data_genetics.py` | Genetics, Chromosomal Anomalies, Dysmorphology & Metabolic Inborn Errors Data |
| `scripts/medical_data_master_taxonomy.py` | Medical Master Taxonomy Generator Generates comprehensive clinical entities across all major organ systems and basic sciences. |
| `scripts/medical_data_micro.py` | Microbiology & Infectious Diseases Concepts Database |
| `scripts/medical_data_patho.py` | Pathology & Histology Master Concepts Database |
| `scripts/medical_master_expansion.py` | Medical Master Expansion Database Provides 1,500+ distinct clinical, anatomical, biochemical, physiological, microbiological, pathological, and pharmacological concepts. |
| `scripts/medical_taxonomy_pharm.py` | Pharmacology Master Taxonomy (1,000+ Drugs, Receptors, Mechanisms, Antidotes) |
| `scripts/merge-same-exam-duplicates.mjs` | ============================================================================= merge-same-exam-duplicates.mjs ----------------------------------------------------------------------------- Eşleşen sorular birbirini tekrar  |
| `scripts/archive/merge_same_exam_duplicates.py` | ============================================================================= merge_same_exam_duplicates.py ----------------------------------------------------------------------------- Bu script; 1. Birbiriyle eşleşen,  |
| `scripts/migrate-separate-current-and-past.mjs` | scripts/migrate-separate-current-and-past.mjs Veritabanı Ayrıştırma ve Düzenleme Motoru: 1. 2026-2027 dönemine ait kurullarda henüz sınava girilmediği için tüm mevcut soru ve taslakları güncel havuzdan ('questions') çıka |
| `scripts/monitor.py` | MedSoru Canlı Terminal Kokpiti ve Boru Hattı İzleyici (Terminal Dashboard v2) Tüm aşamaları (Faz 1 - Faz 6) hedefleri ve canlı ilerlemeleriyle gösterir: - Faz 1 (Ham Metin & OCR) - Faz 2 (Türkçe Onarım & Soru Ayrıştırma) |
| `scripts/archive/parse_butunleme.py` | _başlık açıklaması yok_ |
| `scripts/process-local-sorular.mjs` | scripts/process-local-sorular.mjs meds_database\local_sorular klasöründeki PPTX ve PDF dosyalarını işler: 1. PPTX slaytlarını JSZip ile XML'den sayfa sayfa okur. 2. PDF dosyalarını pdf-parse ile ok |
| `scripts/archive/rechunk_all_study_questions.py` | _başlık açıklaması yok_ |
| `scripts/archive/reconcile-curriculum-summaries.mjs` | scripts/archive/reconcile-curriculum-summaries.mjs MedSoru Ders Programı (Curriculum) Tabanlı Özet, Hoca, Konu ve Kurul Senkronizasyon Motoru Bu script: 1. Karabük Üniversitesi Tıp Fakültesi Dönem 3 Resmi Müfredatını (curriculum |
| `scripts/archive/sanitize_questions_and_decks.py` | scripts/archive/sanitize_questions_and_decks.py 1. Audits and sanitizes pastQuestions.json by removing or repairing corrupted, bloated, or unreadable OCR dumps (>1000 chars, multiple '?' marks, garbled characters). 2. Cleans int |
| `scripts/start-cloudflare-tunnel.mjs` | scripts/start-cloudflare-tunnel.mjs MedSoru Sunucusunu (port 3000) ve Cloudflare Quick Tunnel'ı eşzamanlı olarak başlatır. Domain gerektirmeden anında güvenli bir https://*.trycloudflare.com adresi üretir. |
| `scripts/start-hybrid-tunnel.mjs` | scripts/start-hybrid-tunnel.mjs Yerel bilgisayarınızdaki MedSoru sunucusunu (port 3000) GitHub Pages (HTTPS) üzerinden güvenle erişilebilir kılmak için ücretsiz bir tünel açar ve adresi doğrudan Firebase Firestore'a kayd |
| `scripts/archive/switch-env-to-cloud.mjs` | _başlık açıklaması yok_ |
| `scripts/switch-env-to-local.mjs` | _başlık açıklaması yok_ |
| `scripts/test-sample-pdfs.mjs` | _başlık açıklaması yok_ |
| `scripts/archive/test_norm.ts` | _başlık açıklaması yok_ |
| `scripts/archive/tumor_evreleme_slides_part1.py` | Part 1 of the Tumor Staging and Laboratory Diagnosis Deck (Slides 1 to 12) |
| `scripts/archive/tumor_evreleme_slides_part2.py` | Part 2 of the Tumor Staging and Laboratory Diagnosis Deck (Slides 13 to 24) |

### Drive indirme ve tarama (13)

| Dosya | Açıklama |
|---|---|
| `scripts/crawl-all-drive-folders.mjs` | _başlık açıklaması yok_ |
| `scripts/download-all-slides.mjs` | _başlık açıklaması yok_ |
| `scripts/download-and-process-kurul-notes.mjs` | scripts/download-and-process-kurul-notes.mjs Google Drive'daki Kurul 1 - Kurul 6 tüm amfi ders notlarını: 1. meds_database\kurul_ders_notlari\Kurul 1 .. 6 klasörlerine indirir. 2. PDF, PPTX ve DOCX |
| `scripts/archive/download_and_merge_supabase.py` | Supabase Cloud -> meds_database & meds/data indirme ve akıllı birleştirme betiği. - 4069 çıkmış soru, 885 ders notu, 24 komite ve 605 chunk'ı indirir. - Mevcut yerel verileri ezmeden akıllı tekilleştirme (deduplication)  |
| `scripts/archive/download_missing_drive_file.mjs` | _başlık açıklaması yok_ |
| `scripts/archive/extract_missing_drive_materials.py` | extract_missing_drive_materials.py Extracts text from all pending PDF, PPTX, and DOCX files in meds_database/meds_sorular and saves them to meds_database/meds_sorular_txt. |
| `scripts/archive/extract_remaining_drive_lectures.py` | _başlık açıklaması yok_ |
| `scripts/archive/inspect_drive_pdfs_deep.py` | _başlık açıklaması yok_ |
| `scripts/orchestrate_drive_curriculum_ai.mjs` | ============================================================================== MedSoru AI Drive Curriculum Orchestrator & Interactive Deck Generator ======================================================================= |
| `scripts/archive/test-drive-audio-scan.mjs` | _başlık açıklaması yok_ |
| `scripts/test-drive-folders.mjs` | _başlık açıklaması yok_ |
| `scripts/transcribe-drive-audio.mjs` | scripts/transcribe-drive-audio.mjs MedSoru Tıbbi Amfi Ses Kayıtları Transkripsiyon, Ders Eşleştirme ve İzleme Motoru --------------------------------------------------------------------------------- 1. Google Drive ('G:\ |
| `scripts/update-drive-catalog.mjs` | _başlık açıklaması yok_ |

### Eşleştirme (7)

| Dosya | Açıklama |
|---|---|
| `scripts/deep-triple-slide-matcher.mjs` | MedSoru Derinlemesine 3 Aşamalı Slayt ve Soru Eşleştirme Motoru (scripts/deep-triple-slide-matcher.mjs) Özellikler: 1. Çıkmış soru dosyalarını ders notlarından kesin olarak ayıklar (778 gerçek amfi slaytı). 2. Soruların  |
| `scripts/link-exam-questions.mts` | Link past-exam files to the existing question pool and course material (retrieval only, no AI). npx tsx scripts/link-exam-questions.mts <file-or-folder> [--out report.json] For every question found in a PDF/DOCX it repor |
| `scripts/match-and-link-lecture-slides.mjs` | MedSoru Slayt Eşleştirme, Bağlama ve Vurgulama Scripti (Script 2) (scripts/match-and-link-lecture-slides.mjs) Amaç: 1. Henüz ders ilişkisi olmayan ya da hatalı ders ilişkisine sahip olduğu tespit edilen (Script 1 ile ili |
| `scripts/slide-matching-utils.mjs` | MedSoru Slayt Eşleştirme ve Denetim Yardımcı Modülü (scripts/slide-matching-utils.mjs) |
| `scripts/archive/test_concept_matcher.ts` | _başlık açıklaması yok_ |
| `scripts/archive/test_glossary_match.js` | _başlık açıklaması yok_ |
| `scripts/archive/test_glossary_match.mjs` | _başlık açıklaması yok_ |

### Onarım ve temizlik (4)

| Dosya | Açıklama |
|---|---|
| `scripts/archive/clean_fake_slide_matches.cjs` | _başlık açıklaması yok_ |
| `scripts/fix-nested-and-embedded-questions.mjs` | scripts/fix-nested-and-embedded-questions.mjs MedSoru İç İçe Geçmiş Şıklar, Soru Kökünde Kalan Şıklar ve Birbirine Yapışmış Soruları Ayrıştırma ve Düzeltme Motoru Çözülen Sorunlar: 1. Şık İçinde Şık (Nested Options): Örn |
| `scripts/fix-question-typos.mjs` | scripts/fix-question-typos.mjs MedSoru Soru Yazım Hatalarını ve Bozuk OCR İfadelerini Tespit ve Düzeltme Motoru Özellikler: 1. Tire Bölünmelerini Düzeltir: - "Send- romu" -> "Sendromu" - "mev- cuttur" -> "mevcuttur" - "b |
| `scripts/test-filter-donem3.mjs` | _başlık açıklaması yok_ |

### RAG (3)

| Dosya | Açıklama |
|---|---|
| `scripts/index-rag-knowledge.mjs` | ============================================================================== MedSoru RAG Knowledge Indexer & Embedder ============================================================================== Bu betik: 1. data/pas |
| `scripts/archive/reorganize_curriculum_and_rag.py` | scripts/archive/reorganize_curriculum_and_rag.py Tüm soruların Karabük Üniversitesi Tıp Fakültesi resmi ders programlarına (Dönem 1, 2, 3) göre yeniden sınıflandırılması, Dönem 2 / Dönem 3 ayrımının yapılması, #111 vb. hatalı so |
| `scripts/archive/test-rag.ts` | _başlık açıklaması yok_ |

### Senkronizasyon ve yedek (16)

| Dosya | Açıklama |
|---|---|
| `scripts/auto-git-sync.mjs` | _başlık açıklaması yok_ |
| `scripts/archive/backup-local-to-cloud.mjs` | scripts/archive/backup-local-to-cloud.mjs Yerel Supabase (Docker) veritabanındaki verileri Cloud Supabase (https://kgutsltgmqbnlxcnzrtl.supabase.co) üzerine yedekler. |
| `scripts/local-drive-sync-agent.mjs` | MedSoru Yerel Bilgisayar Arka Plan Otomasyon İşleyicisi (Local Sync Worker) Bu betik kendi bilgisayarınızda arkaplanda çalışarak: 1. Google Drive klasöründeki (Kurul 1 ve Dönem 3) yeni PDF/DOCX slaytlarını otomatik takip |
| `scripts/meds-local-sync.mjs` | MedSoru Yerel Otomasyon ve Senkronizasyon Motoru (meds-local-sync.mjs) Bu betik: 1. Google Drive çıkmış soru ve ders notları klasörlerini tarar. 2. Yeni/eksik PDF'leri doğrudan meds_database klasör |
| `scripts/sync-all-to-firebase.mjs` | scripts/sync-all-to-firebase.mjs Yerel olarak işlenen tüm verileri doğrudan Firebase Firestore'a eşitler: 1. 184 adet Amfi Ders Slayt Notu -> 'lecture_notes' koleksiyonuna yüklenir. 2. 1.600+ Geçmiş Kurul & Yapay Zeka So |
| `scripts/sync-all-to-firestore.mjs` | MedSoru Firestore Full Database Sync Script Bu betik: 1. INITIAL_COMMITTEES listesini Firestore 'committees' koleksiyonuna eşitler. 2. data/lecture_notes.json içindeki tüm ders notlarını Firestore 'lecture_notes' koleksi |
| `scripts/sync-all-to-supabase.mjs` | scripts/sync-all-to-supabase.mjs Veritabanı senkronizasyon motoru: 1. Kurulları (Committees) 2. Çıkmış Soruları (Past Questions - 2314 adet) 3. Amfi Ders Notlarını (Lecture Notes) Supabase PostgreSQL veritabanına aktarır |
| `scripts/sync-database-json-to-cloud.mjs` | scripts/sync-database-json-to-cloud.mjs meds_database\database_json altındaki yapılandırılmış JSON dosyalarını doğrudan Supabase (PostgreSQL) ve Firebase (Firestore) veritabanlarına yükler. Kullanı |
| `scripts/archive/sync-deepseek-contributions.ts` | _başlık açıklaması yok_ |
| `scripts/sync-drive-updates.mjs` | scripts/sync-drive-updates.mjs MedSoru Google Drive Değişiklik Tespit ve Manuel Senkronizasyon Motoru --------------------------------------------------------------------- Bu script; Google Drive klasörlerinde (Ders Notl |
| `scripts/sync-past-questions-to-supabase.mjs` | scripts/sync-past-questions-to-supabase.mjs pastQuestions.json dosyasındaki 2922 adet çıkmış soruyu güvenli 25'lik partiler halinde ve otomatik tekrar (retry) mekanizmasıyla Supabase 'past_questions' tablosuna aktarır. |
| `scripts/archive/sync-rag-sorular-to-site-and-supabase.mjs` | scripts/archive/sync-rag-sorular-to-site-and-supabase.mjs Bu script: 1. meds_database/rag_sorular klasöründeki 1.082 adet doğrulanmış ve amfi ders notlarıyla zeminlenmiş (grounded) soruyu okur. 2. meds/data/pastQuestions.json do |
| `scripts/sync_deepseek_data.py` | scripts/sync_deepseek_data.py Robust DeepSeek Data Synchronizer and Sanitizer for MedSoru: - Scans `meds_database/deepseek_data/` and local `deepseek_data/`. - Enforces strict anti-corruption filters: * Rejects bloated q |
| `scripts/archive/sync_drive_curriculum_folder.mjs` | scripts/archive/sync_drive_curriculum_folder.mjs Google Drive klasöründeki (1ozu5KiLZjFd4YKNMZ0bSRvLVV6b7lv0W) tüm ders notlarını: 1. meds_database\ders_notlari_pdf ve kurul_ders_notlari\Kurul 1'e indirir. |
| `scripts/sync_to_supabase_v2.py` | scripts/sync_to_supabase_v2.py -------------------------------------------------------------------------------- MedSoru AI - Supabase v2 Chunk-Build Veri Senkronizasyonu Motoru 1. 6.263 Doğrulanmış ve Zenginleştirilmiş Ç |
| `scripts/sync_user_drive_folder.mjs` | _başlık açıklaması yok_ |

### Sözlük ve terim zenginleştirme (10)

| Dosya | Açıklama |
|---|---|
| `scripts/enrich-drive-slides.mjs` | _başlık açıklaması yok_ |
| `scripts/archive/enrich_apoptosis_terms.py` | Enrich Medical Glossary and Encyclopedia with detailed Apoptosis & Bcl-2 Family entries (Bax, Bak, Intrinsic Pathway, Extrinsic Pathway, Apoptosome, Smac/DIABLO, etc.) |
| `scripts/archive/enrich_high_yield_terms.py` | _başlık açıklaması yok_ |
| `scripts/archive/enrich_medical_encyclopedia_and_glossary.py` | scripts/archive/enrich_medical_encyclopedia_and_glossary.py Enriches medical_glossary.json and medical_encyclopedia.json with faculty-aligned, deeply structured medical entries for pathology, genetics, oncology, immunology, and  |
| `scripts/archive/enrich_new_drive_terms.py` | _başlık açıklaması yok_ |
| `scripts/archive/enrich_past_questions.py` | enrich_past_questions.py DeepSeek tarafından doğrulanmış ve zenginleştirilmiş soruları (meds_donem3_sorulari_duzeltilmis.jsonl) mevcut pastQuestions.json veri tabanına entegre eder. Tüm kök, şık, gerekçe, kanıt metni, de |
| `scripts/archive/enrich_spot_pearls_structure.py` | scripts/archive/enrich_spot_pearls_structure.py Upgrades all spotPearls in 'learn-enflamasyon-kimyasal-mediyatorleri' to multi-tier structured format: - Üst madde & alt madde (indented sub-bullets) - 🔴 Kırmızı (Önemli / Kritik / |
| `scripts/archive/expand_apoptosis_terms.py` | scripts/archive/expand_apoptosis_terms.py Enriches medical_encyclopedia.json and medical_glossary.json with granular entries: 1. Bax Proteini (Bcl-2 Associated X Protein) 2. Bak Proteini (Bcl-2 Antagonist/Killer) 3. İntrensek Ap |
| `scripts/archive/expand_genetics_pediatric_terms.py` | expand_genetics_pediatric_terms.py Enriches medical_encyclopedia.json and medical_glossary.json with comprehensive, granular terms for Genetics, Pediatric, Environmental, Nutritional Pathology, and Molecular Diagnostics  |
| `scripts/archive/expand_hypersensitivity_terms.py` | expand_hypersensitivity_terms.py Enriches medical_encyclopedia.json and medical_glossary.json with comprehensive, granular terms for Hypersensitivity, Autoimmunity, Immunogenetics, Rejection, Immunodeficiencies, and Amyl |

### advanced_ai/ (13)

| Dosya | Açıklama |
|---|---|
| `scripts/advanced_ai/build_phase7_gold_100.py` | Faz 7: 100 Altın Standart Tıp Eğitmen Modellemesi Üretici --------------------------------------------------------- Hekimlik nosyonu, patofizyoloji, farmakoloji ve klinik kurallarla 100 sorunun 5 adımlı mikro-ajan modell |
| `scripts/advanced_ai/deep_metadata_generator_phase6.py` | Faz 6: Derin Tıbbi Hiper-Metadata Motoru (Çoklu AI & Dinamik Zamanlama) ---------------------------------------------------------------------- Görevler: 1. Faz 5 doğrulanmış soruları ve amfi ders notlarını (slide chunks) |
| `scripts/advanced_ai/generate_perfect_100_stories.py` | Faz 7: 100 Altın Tıp Sorusunu Gerçek Tıbbi Ontoloji ve Hekimlik Nosyonu ile 5 Adımlı Mikro-Ajans Kurallarına Birebir Uygun Olarak Üreten Motor. |
| `scripts/advanced_ai/graph_rag.py` | GraphRAG & Tıbbi Bilgi Grafı (Medical Knowledge Graph) - Düğümler (Nodes): Hastalık, Belirti, İlaç, Gen, Kurul, Ders, Konu, Soru ID - Kenarlar (Edges): NEDEN_OLUR, TEDAVİ_EDER, İLİŞKİLİDİR, BULUNUR, SORULMUŞTUR |
| `scripts/advanced_ai/hybrid_search.py` | BM25 + Dense Retrieval (bge-m3) Hibrit Arama & Reranker Motoru |
| `scripts/advanced_ai/memory_os.py` | MemGPT / Hiyerarşik Bellek Katmanı (MedSoru) - Core Memory: Kullanıcı/Öğrenci profili, hedefler, zayıf kalınan tıbbi kurullar/dersler - Recall Memory: Son etkileşimler, çözülen sorular, oturum bağlamı - Archival Memory:  |
| `scripts/advanced_ai/microagent_storyteller_phase7.py` | Faz 7: 5 Adımlı Mikro-Ajans (Micro-Agent) Tıbbi Modelleme & Hikayeleştirme Motoru --------------------------------------------------------------------------------- Altın Kural: 'Böl ve Yönet' (Divide & Conquer) Kısıtlı p |
| `scripts/advanced_ai/multi_ai_consensus_phase5.py` | Faz 5 Çoklu AI Konsensüs & Soru Derin Analiz Motoru -------------------------------------------------- Görevler: 1. Mevcut veritabanındaki (meds_database/questions) soruları ve amfi ders notlarını okur. 2. Her bir soru i |
| `scripts/advanced_ai/orchestrator.py` | Gelişmiş AI Orkestratörü & Boru Hattı Entegrasyonu (Aşama 5) Aşama 3 ve 4 tamamlandığında otomatik tetiklenir: 1. Slaytlar ve Sorular üzerinden Tıbbi Knowledge Graph (GraphRAG) inşa eder. 2. BM25 indekslerini hesaplar ve |
| `scripts/advanced_ai/rag_evaluator.py` | MedSoru RAG Değerlendirme (Evaluation) Test Scripti Metrikler: Hit Rate@1, Hit Rate@3, Hit Rate@5, MRR (Mean Reciprocal Rank) Ground Truth: Sorunun 'evidence.chunk_id' veya 'doc_source_id' / 'kaynak.source_id' bilgisi. |
| `scripts/advanced_ai/react_guardrails.py` | ReAct (Reasoning + Acting) & Function Calling & Guardrails Motoru - Düşünce (Thought) -> Eylem (Action) -> Gözlem (Observation) döngüsü - Guardrails: Tıbbi uydurma (hallucination) engelleme, kaynak doğrulaması - Function |
| `scripts/advanced_ai/reconstruct_slides_phase7_5.py` | Faz 7.5: Amfi Ders Slaytlarını Resmi Müfredat Standartlarında Düzenleme Motoru ----------------------------------------------------------------------------- Görevler: 1. KBÜ Tıp Fakültesi resmi müfredat hedeflerini (TIP3 |
| `scripts/advanced_ai/thesaurus_anchor_phase6_5.py` | Faz 6.5: Tıbbi Terimler Sözlüğü (Thesaurus) & Soru-Slayt Birlikte Görünme (Co-occurrence) Graf Motoru ------------------------------------------------------------------------------------------------------ Görevler: 1. Tü |

### agents/ (12)

| Dosya | Açıklama |
|---|---|
| `scripts/agents/lib.py` | MedSoru otomatik boru hattı — ortak kütüphane (tamamen yerel; bulut AI kullanmaz). Süreç: PROJE_TANITIMI.md (downloads -> temp1 -> temp2 -> temp3 -> database) |
| `scripts/agents/parse_ders_programi.py` | Ders programı ayrıştırıcı (tamamen yerel, token harcamaz). Girdi : "2026-27 D3 ders programı.pdf" (Kurul başlık sayfaları + haftalık tablolar) Çıktı : kurul -> dersler (saat, öğretim üyeleri) -> işlenen konular (tarih, s |
| `scripts/agents/pipeline_runner.py` | Sürekli çalışan orkestratör: stage2 -> stage3 -> stage4, hata toleranslı. |
| `scripts/agents/post_lora_auto_refiner.py` | scripts/agents/post_lora_auto_refiner.py -------------------------------------------------------------------------------- MedSoru Otonom Veri Düzeltme & İyileştirme Motoru (Post-Training Autonomous Dataset Refiner) Amaç: |
| `scripts/agents/question_quality_inspector.py` | scripts/agents/question_quality_inspector.py Otonom Soru Kalite ve Bağlam Denetçisi (Autonomous Medical Question Quality & Audit Inspector) Arka planda donanımı yormadan (düşük öncelikli, throttled) çalışır: 1. Tekrar ed |
| `scripts/agents/read_document.py` | PDF / PPTX okuma ajanı (downloads -> temp1). PROJE_TANITIMI.md'deki 1. aşama: ham kaynaktan ilk veriyi çıkarır. Tamamen yerel çalışır (PyMuPDF, python-pptx, Tesseract[tur]; isteğe bağlı Ollama görsel model) ve token harc |
| `scripts/agents/run.sh` | Okuma ajanlarını doğru Python ortamıyla çalıştırır. scripts/agents/run.sh read  <dosya/klasör> [--vision] [--force]   # belgeleri temp1'e çevir scripts/agents/run.sh watch [--once] [--vision]                    # meds_do |
| `scripts/agents/stage2_clean.py` | 2. aşama: temp1 -> temp2 (düzeltme / anlamlandırma). Yerel, token harcamaz. Her belge için: 1. Biçim temizliği (boşluk, kesik satırlar, sayfa numaraları, kontrol karakterleri, tekrarlayan üst/alt bilgi) 2. Deterministik  |
| `scripts/agents/stage3_merge.py` | 3. aşama: temp2 -> temp3 (birleştirme, ilişkilendirme, metadata, tekilleştirme). Yerel, token harcamaz. Kaynak notları (lecture_slide): - müfredat eşleşmesi (kurul/ders yoldan; konu: ders programı taslağıyla bulanık eşle |
| `scripts/agents/stage4_database.py` | Aşama 4: temp3 -> meds_database. Yalnızca verified/fixed + kanıtlı sorular yazılır. |
| `scripts/agents/watch_downloads.py` | meds_downloads izleyicisi: yeni/değişen PDF ve PPTX dosyalarını fark eder ve read_document.py ile temp1'e çevirir (PROJE_TANITIMI.md, 1. aşama). 20 çekirdekli CPU için concurrent.futures.ThreadPoolExecutor(max_workers=8) |
| `scripts/agents/watchdog.py` | MedSoru Watchdog & Otonom Donanım Denetleyicisi (Autonomous Hardware Supervisor) Sürekli arka planda çalışarak sistemi denetler: 1. GPU ve VRAM Kontrolü: - GPU'ya sadece 3 katman (-ngl 3) yüklenmiş ve CPU'ya taşmış asılı |

### vite/ (1)

| Dosya | Açıklama |
|---|---|
| `scripts/vite/splitLearningDecks.ts` | src/data/interactive_learning_decks.json (≈14 MB) tek parça olarak tarayıcıya gönderilince öğrenme sayfası açılırken donuyordu. Bu eklenti derleme/geliştirme başlarken veriyi böler: src/data/decks/catalog.json      → lis |

### eval/ (1)

| Dosya | Açıklama |
|---|---|
| `scripts/eval/retrieval-eval.mts` | Retrieval eval: 300 seeded past questions -> simulated student queries -> is the same question in top 5? Run from repo root: npx tsx scripts/eval/retrieval-eval.mts   (STRIP=1 to drop Turkish characters) |

### ileri_tumor_genetigi/ (4)

| Dosya | Açıklama |
|---|---|
| `scripts/ileri_tumor_genetigi/part1_slides.py` | scripts/ileri_tumor_genetigi/part1_slides.py Slides 1 to 6 for 'learn-ileri-tumor-genetigi-metabolizmasi' |
| `scripts/ileri_tumor_genetigi/part2_slides.py` | scripts/ileri_tumor_genetigi/part2_slides.py Slides 7 to 12 for 'learn-ileri-tumor-genetigi-metabolizmasi' |
| `scripts/ileri_tumor_genetigi/part3_slides.py` | scripts/ileri_tumor_genetigi/part3_slides.py Slides 13 to 18 for 'learn-ileri-tumor-genetigi-metabolizmasi' |
| `scripts/ileri_tumor_genetigi/part4_slides.py` | scripts/ileri_tumor_genetigi/part4_slides.py Slides 19 to 24 for 'learn-ileri-tumor-genetigi-metabolizmasi' |

### pipeline/ (5)

| Dosya | Açıklama |
|---|---|
| `scripts/pipeline/00-init.mjs` | Aşama 1: meds_downloads / meds_temp / meds_database iskeletini kurar (idempotent). |
| `scripts/pipeline/01-inventory.mjs` | Aşama 2: Drive envanteri (yalnızca metadata, dosya indirmez). Çıktı: meds_downloads/_manifest.json |
| `scripts/pipeline/02-download.mjs` | Aşama 3: Drive dosyalarını meds_downloads altına indirir (artımlı, devam edilebilir, sıralı). Önce ücretsiz herkese açık indirme; başarısız olursa GOOGLE_SERVICE_ACCOUNT_FILE varsa Drive API (servis hesabı). Kullanım: no |
| `scripts/pipeline/10-enrich-summaries.mjs` | Ders özetlerini resmi ders programıyla ve kaynak PDF'leriyle eşleştirir. Girdi:  src/data/summaries_meta.json $MEDS_DATABASE_DIR/taxonomy/donem3_ders_programi.json (dersler, konular, PDF adayları) $MEDS_DOWNLOADS_DIR/_ma |
| `scripts/pipeline/config.mjs` | MedSoru pipeline: ortak yollar. Akış: Drive -> downloads -> temp -> database |

### training/ (3)

| Dosya | Açıklama |
|---|---|
| `scripts/training/monitor_train.sh` | MedSoru Canlı Eğitim Terminal Monitörü |
| `scripts/training/prepare_dataset.py` | MedSoru Özel Tıp Yapay Zekası İçin İnce Ayar (Fine-Tuning) Veri Seti Hazırlayıcı. Kaynak : meds_database/questions (2.194 doğrulanmış soru) & meds_database/chunks (amfi slayt kanıtları) Çıktı : meds/training_data/medsoru |
| `scripts/training/train_lora.py` | MedSoru 4-Bit QLoRA Fine-Tuning Eğitici (RTX 4060 8GB VRAM Optimize) Kaynak : meds/training_data/medsoru_train.jsonl & medsoru_val.jsonl Hedef : Tıp Fakültesi Dönem 3'e özel yerel tıp uzmanı modeli (LoRA Adaptörü) Özelli |

### tumor_immuno_builder/ (5)

| Dosya | Açıklama |
|---|---|
| `scripts/tumor_immuno_builder/part1_antigens.py` | Part 1: Tümör İmmünolojisine Giriş ve Tümör Antijenleri (Slayt 1 - 6) Robbins & Kumar Basic Pathology 11. Baskı ve Prof. Dr. Hikmet Keleş Ders Notu temelinde. |
| `scripts/tumor_immuno_builder/part2_effectors.py` | Part 2: Efektör İmmün Yanıt ve Hücreler (Slayt 7 - 10) Robbins & Kumar Basic Pathology 11. Baskı ve Prof. Dr. Hikmet Keleş Ders Notu temelinde. |
| `scripts/tumor_immuno_builder/part3_escape.py` | Part 3: Tümörün İmmün Kaçış Mekanizmaları ve İmmünoterapi (Slayt 11 - 15) Robbins & Kumar Basic Pathology 11. Baskı ve Prof. Dr. Hikmet Keleş Ders Notu temelinde. |
| `scripts/tumor_immuno_builder/part4_metastasis1.py` | Part 4: Metastaz Kaskadı I (Slayt 16 - 20) Robbins & Kumar Basic Pathology 11. Baskı ve Prof. Dr. Hikmet Keleş Ders Notu temelinde. |
| `scripts/tumor_immuno_builder/part5_metastasis2.py` | Part 5: Metastaz Kaskadı II (Slayt 21 - 24) Robbins & Kumar Basic Pathology 11. Baskı ve Prof. Dr. Hikmet Keleş Ders Notu temelinde. |

### Çıkarma ve OCR (6)

| Dosya | Açıklama |
|---|---|
| `scripts/extract-scanned-images.py` | MedSoru Scanned PDF Image Extractor Extracts images from scanned PDFs in meds_database\meds_sorular and saves them to meds_database\meds_sorular_images\[pdf_name]\ |
| `scripts/archive/extract_batch_pending_lectures.py` | _başlık açıklaması yok_ |
| `scripts/extract_curriculum.py` | _başlık açıklaması yok_ |
| `scripts/filter-donem3-and-clean-ocr.mjs` | scripts/filter-donem3-and-clean-ocr.mjs 1. Dönem 3 müfredatına (Tıbbi Patoloji, Farmakoloji, Dahiliye, Kardiyoloji, Pediatri, Üroloji, Kadın Doğum, Enfeksiyon, Ortopedi, Acil Tıp, Nöroloji, Psikiyatri, FTR, Genetik vb.)  |
| `scripts/archive/outline_extracted_lectures.py` | _başlık açıklaması yok_ |
| `scripts/process-scanned-ocr.mjs` | MedSoru Scanned PDF OCR & Question Extraction Engine Bu betik: 1. meds_sorular_images içindeki taranmış sınav fotoğraflarını OCR ile okur. 2. 180° ters çekilmiş fotoğrafları otomatik tespit edip döndürür. 3. Orijinal ham |

---

## 8. Kurallar ve bilinen açıklar (özet)

- **Gizli anahtarlar** yalnız sunucu `.env`'de; istemci paketine ya da koda gömülmez. Firebase web anahtarı ve
  Supabase publishable anahtarı tasarım gereği herkese açıktır.
- **Kaynağa dayanma:** soru yazan/düzelten her özellik `findSourcesForQuestion` + `formatSourcesForPrompt` +
  `usedSources` + `toSourceRef` zincirini kullanır.
- **AI çıktısı kanıt değildir:** `ai_qa`, `ai_refinement`, `deepseek_contribution` getirme türlerine eklenmez.
- **Boş sonuçla veri ezilmez** (`deepseekDataService.ts` korumasına bakın).
- **Açıklar:** yönetici doğrulaması zayıf (başlık + loopback), AI uçlarında hız sınırı yok; ders verisinde
  yinelenen desteler, kişisel veri içeren sohbet dökümleri ve boş OCR sayfaları var; bazı çıkmış soru kayıtları
  OCR ile tam sayfa (sınav sonuç ekranı gibi) almış durumda — moderasyon ekranından gizlenebilir/silinebilir.
