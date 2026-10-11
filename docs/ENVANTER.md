# ENVANTER — T0 Tam Envanter (salt-okunur)

> Tarih: 2026-10-11 (gece) · Kapsam: `/home/indu/medsor/` kökü, `meds/` 2. seviye, veri klasörleri, `meds/data`, `meds/src/data`, `meds/scripts`, cihaz servisleri.
> Yöntem: `du -sh`, `find` (dosya sayısı + en yeni mtime), kod referansı için grep (`meds/server.ts`, `meds/src/`, `meds/scripts/` [archive hariç], `meds/deploy/`, `meds/dashboard_server.py`, `vite.config.ts`, `package.json` scripts), systemd user üniteleri, docker compose dosyaları, `.env` yol değişkenleri (yalnız İSİM). Hiçbir dosya değiştirilmedi.
> Öneri sözlüğü: **KALIR** (canlı) · **TAŞI** (repo/proje dışı yedeğe: `/home/indu/medsor-yedek/<tarih>/`) · **ARŞİVLE** (`meds/scripts/archive/<tarih>/` veya yedek; yeniden üretim/iz için saklanır) · **SİL-ADAYI** (kanıtla gereksiz; önce yedeğe taşı → 7 gün → onayla sil). **(?)** = belirsiz, kullanıcı kararı gerekir.
> Not: Paralel oturum `meds/` altında çalışıyor; 2026-10-10/11 tarihli değişiklikler o oturumun ürünü olabilir.

---

## 0. Önce bilinmesi gereken ölçülen gerçekler (yol haritasındaki varsayımları düzeltenler)

| # | Bulgu | Kanıt | Etki |
|---|---|---|---|
| E1 | **Makinede GPU VAR** (RTX 4060 Laptop). §12 B6'daki "GPU'suz makine" ifadesi yanlış; doğrusu: GPU var ama `.env` ile kapatılmış (`MEDS_DISABLE_GPU`, `CUDA_VISIBLE_DEVICES`, `OLLAMA_NUM_GPU`). Yerel Ollama **Docker'da değil, native** (`/usr/lib/ollama/llama-server`, 1 GB VRAM kullanıyor; bge-m3 14 saat önce çekilmiş). | `nvidia-smi` | `meds-gpuguard`/`meds-phases` GPU koruma mantığı çalışabilir durumda; `docker-compose*.yml`'deki `meds-ollama` konteyneri kullanılmıyor |
| E2 | `:8094` (bge-m3 sorgu gömme, `.env` `MEDS_EMBED_URL` bunu gösteriyor) **systemd ünitesi olmayan, elle başlatılmış** bir süreç: `.venv-ocr/bin/python scripts/agents/embed_server.py` (pid 702110, ~7.5 saattir açık). `meds-embed.service` ise :8091 (e5-small). | `ss -ltnp`, `ps` | Yeniden başlatmada :8094 kaybolur → `meds-web` vektör araması düşer. T5'te ünite haline getirilmeli |
| E3 | `meds/dist/assets`: 9420 dosya / 1185 MB; mevcut `index.html` + `sw.js` import grafiğinden **erişilebilen 280 dosya / 100 MB**; **bayat 9140 dosya / 1085 MB**. Bayatların **hiçbiri 7 günden eski değil** (en eski 2026-10-09). | BFS betiği (scratchpad) | T3'teki "son 2 manifest dışı + 7 günden eski" kuralı bugün **hiçbir şey silmez**; kural "son N derleme" bazlı olmalı |
| E4 | Kök `packages/` (13 deste, k1-30…k1-42) **meds'teki kopya DEĞİL**: `meds/src/data/decks/packages/` yalnız 30 klasör (k1-01…k1-29) içeriyor. Kök paketler 2026-10-10 01:00 tarihli, `items/` sürümleri 2026-10-11 01:36 tarihli ve md5'leri FARKLI (kök = eski anlık görüntü). Desteler `interactive_learning_decks.json` içinde mevcut (114 deste). | `diff`, md5 | Kök paketler bayat; ama `meds/.../packages` içinde k1-30+ paketi hiç yok → AGENTS.md kural 5 ("paket dosyaları senkron") için paket üretimi eksik |
| E5 | `meds/data/pastQuestions.json` ≡ `meds/src/data/pastQuestions.json` (md5 `e317f94f…`, 5713 kayıt, aynı saniyede yazılmış). `server.ts:1791` her kayıtta ikisini birden yazıyor. İstemci kodu `src/data/pastQuestions.json`'u **import etmiyor** (yalnız sunucu servisleri yolunu biliyor). | md5 + grep | src kopyası gereksiz ikinci yazım; Oracle'a rsync ile 72 MB fazladan gidiyor |
| E6 | `meds_database/meds_sorular` (327 MB, 99 dosya): **98 dosya `meds_downloads` içindekilerle bayt-bayt aynı (324 MB)**. Sunucu bu klasörü okuyor. | md5 karşılaştırma | T4'te hardlink/symlink ile ~324 MB kazanılabilir (silme değil) |
| E7 | Oracle konteyneri `meds_database`, `_v2`, `_core`, `meds_temp`, `meds_downloads` klasörlerini **ro** bağlıyor; `meds_database_v3_export` ve `meds_export` **bağlanmıyor**. `geminiV3DataService.ts` varsayılanı sabit `/home/indu/medsor/meds_database_v3_export`; `server.ts:5493` `../meds_export/notebooklm`. | `docker-compose.oracle.yml` | Oracle'da Gemini v3 verisi ve NotebookLM indirme ucu (404) çalışmıyor olabilir — doğrulanmalı |
| E8 | `deploy-code.sh` rsync'i yalnız `/.env`'i hariç tutuyor → `meds/.env.cloud.bak` (sır içerebilir), `src/data/pastQuestions.json.bak_manual_import` (61 MB), `get-pip.py`, `.agents/.claude/.github` skill kopyaları (3×20 MB), `scripts/semantic/data` (108 MB) Oracle'a gidiyor. (`.dockerignore` `*.bak*`/`.env*`'i imajdan dışlıyor ama diskte duruyor.) | `deploy-code.sh:18-26` | Rsync şişkinliği + sır dosyası Oracle diskinde |
| E9 | `data/local_rag_chunks.json` artık git'te **takipli değil** (gitignore'lı, `git ls-files` boş) — §3'teki "`git rm --cached` gerekli" notu güncel değil. `data/lecture_notes.legacy_backup.json` (53 MB) ise hâlâ takipli. | `git ls-files` | §3 tablosu güncellenmeli |

---

## 1. Kök (`/home/indu/medsor/`)

| Yol | Boyut | Son değişim | Kanıt (kim kullanıyor) | Öneri | Not |
|---|---|---|---|---|---|
| `meds/` | 19 G | 2026-10-11 | Uygulama kodu; tüm servisler | KALIR | 12.0 G'si `.venv-ocr`+`.venv_train`, 2.2 G `supabase-server`, 1.3 G `node_modules`, 1.2 G `dist` (§2) |
| `meds_database/` | 1.2 G | 2026-10-11 | `.env MEDS_DATABASE_DIR`; server, servisler, Oracle ro mount | KALIR | Ayrıntı §4 |
| `meds_database_v2/` | 195 M | 2026-10-11 | server (`PHASE14_DIR`), faz betikleri, Oracle ro mount | KALIR | Ayrıntı §4 |
| `meds_database_core/` | 126 M | 2026-10-11 | `MEDS_CORE_DIR` (meds-core/revize/v2search/v2semantic üniteleri), server | KALIR | Ayrıntı §4 |
| `meds_database_v3_export/` | 19 M | 2026-10-05 | `src/services/geminiV3DataService.ts` (server import), `advanced_ai/extract_gemini_v3_metadata.py` | KALIR | Sabit yol; Oracle'da bağlı değil (E7) |
| `meds_export/` | 106 M | 2026-10-10 | `server.ts:5493` NotebookLM indirme ucu | KALIR | `notebooklm/` 13 dosya; Oracle'da bağlı değil (E7) |
| `meds_temp/` | 947 M | 2026-10-11 | `.env MEDS_TEMP_DIR`; tüm boru hattı | KALIR (içinde TAŞI/ARŞİVLE kalemleri var) | Ayrıntı §4 |
| `meds_downloads/` | 683 M | 2026-10-08 | `.env MEDS_DOWNLOADS_DIR`; `meds-core --roots`, `meds-downloads-watcher` | KALIR | Ham kaynak, salt-ekle |
| `yedek/` | 1.2 G | 2026-10-10 | Kod referansı yok | **TAŞI** → `/home/indu/medsor-yedek/` | `meds_save_backup1.zip` 407M, `20261006_1522` 266M, `med_data_eski_proje_kopyasi` 245M, `meds_database_backup_20261005` 128M, `meds-src-oncesi-v7…tgz` 60M, `study` 46M, `desteler` 32M, `reviews_*.jsonl` ~8M … (T1) |
| `scripts/` (kök) | 40 M (1326 dosya) | 2026-10-10 | Canlı kodda referans yok. Göreli yolla `src/data/decks/items` ve `meds_database_v2/faz14_kurtarilan_sorular` yazıyorlar | **ARŞİVLE** (kısmen SİL-ADAYI) | 157 .py + 51 `k1_NN_deck_data/`. **53 .py + 29 deck_data klasörü (~19 MB) `meds/scripts/k1_decks` ile birebir aynı → SİL-ADAYI**; 103 .py benzersiz (`build_full_lesson_30..66`, `apply_web_grounded_party1..22`, `create_k*`, `enrich_k*`, `phase15_parti*_auditor`, `export_notebooklm*` …) + `k1_31..66_deck_data` → ARŞİVLE (deste yeniden üretimi için iz). `__pycache__` 1.3M SİL-ADAYI |
| `packages/` (kök) | 9.0 M (13 klasör) | 2026-10-10 | Referans yok | **ARŞİVLE** | E4: `items/` sürümlerinden eski; meds'te k1-30+ paketi olmadığından silmeden önce paket yeniden üretimi kararı (?) |
| `src/` (kök) | 820 K (1 dosya) | 2026-10-10 | Referans yok | **ARŞİVLE** | `src/data/decks/items/k1p-k1-48-….json` — kök betiklerin göreli yazımı; meds'teki sürümden farklı (eski). |
| `patch_*.py` (10), `fix_deck.py`, `fix_hints.py`, `apply_fixed.py`, `update_builder.py` | 14 × ≤4K | 2026-10-10 | Referans yok. Hepsi mutlak yolla `meds/scripts/deck_generators/builder_helper.py` veya `items/k1p-k1-50-sifilis.json` yamalıyor (uygulanmış tek seferlik yamalar) | **ARŞİVLE** | `items/` derlemede üretildiği için `items`'a yazan yamalar zaten kalıcı değil |
| `rag-project/` | 25 M | 2026-10-11 05:50 | Referans yok; yalnız boş bir `venv/` (py3.11), kod yok | **SİL-ADAYI (?)** | Bugün oluşturulmuş; hangi oturumun açtığı sorulmalı |
| `splash_box.png`, `splash_box_1024.png` | 12K+28K | 2026-10-10 | Referans yok; `meds/public` içinde eşi yok | **ARŞİVLE (?)** | Tasarım taslağı olabilir |
| `ssh-key1.key`, `ssh-key1.pub` | 4K+4K | 2026-10-11 | `deploy-code.sh` varsayılan `KEY`, `SISTEM_MIMARISI.md` | **TAŞI** → `~/.ssh/` | T1: `deploy-code.sh`/`sync-*.sh` yol güncellemesiyle aynı adımda |
| `AGENTS.md` | 8 K | 2026-10-10 | Ajan talimatı (canlı) | KALIR | |
| `PROJE_TANITIMI.md` | 12 K | 2026-10-10 | Ajan talimatı (canlı) | KALIR | §6'daki "Ollama Docker'da" ifadesi güncel değil (E1) |
| `DEGISIKLIK_KAYDI.md` | 220 K | 2026-10-11 | Oturum günlüğü (canlı) | KALIR | T8: eski girdiler arşive |
| `GEMINI.md` | 8 K | 2026-10-10 | `INTERAKTIF_OGRENME_REHBERI.md`, `meds/docs/OGREN_ETKILESIM_REHBERI.md`, `YENILIKLER_2026-10-09.md` atıf veriyor | **ARŞİVLE (T8 birleştir)** | AGENTS.md'nin 9 kuralının tamamı + başlıkta farklı "Medical Evaluation & Reasoning" protokolü (soru çözüm/şık analizi). Benzersiz kısım AGENTS.md'ye taşınmalı |
| `INTERAKTIF_OGRENME_REHBERI.md` | 12 K | 2026-10-09 | Yalnız yol haritası atıf veriyor | **ARŞİVLE (T8 birleştir)** | **Çelişki:** "her ders 100–400 adım", "adım 30–250 kelime", "etkileşim yalnız dönüm noktalarında" ↔ AGENTS.md "≥60 kelime", "her slaytta 4–6 öge". Asıl rehber `meds/docs/OGREN_ETKILESIM_REHBERI.md` (355 satır) |
| `NOTEBOOKLM_TALIMAT_REHBERI.md` | 12 K | 2026-10-10 | Hiçbir yerden atıf yok; içerik `meds_export/notebooklm` + server ingest ucunu anlatıyor | **TAŞI** → `meds/docs/` | Canlı özelliğin belgesi |
| `FAZ15_TANITIMI.md` | 8 K | 2026-10-08 | `PROJE_TANITIMI.md` §3.7 atıf veriyor | **TAŞI** → `meds/docs/` | Atıf yolu birlikte güncellenmeli |
| `.claude/` | 8 K | 2026-10-10 | `launch.json` (önizleme sunucuları 5175/5176; hafıza notu 5176 konsol) | KALIR | |
| `.commandcode/` | 52 K | 2026-10-09 | Harici araç (Command Code "taste") yapılandırması; kod referansı yok | **SİL-ADAYI (?)** | Kullanıcı aracı kullanıyorsa KALIR |

---

## 2. `meds/` ikinci seviye

### 2.1 Kod, yapılandırma, belgeler

| Yol | Boyut | Son değişim | Kanıt | Öneri | Not |
|---|---|---|---|---|---|
| `server.ts` | 396 K | 2026-10-11 | `npm run dev` (meds-web), Oracle imajı | KALIR | |
| `src/` (kod) | 388 M (veri dahil) | 2026-10-11 | Vite derlemesi | KALIR | `src/data` ayrıntısı §3.2 |
| `index.html`, `vite.config.ts`, `tsconfig.json`, `package.json`, `package-lock.json` | — | 10-07…10-11 | Derleme | KALIR | `vite.config.ts:33 emptyOutDir:false` → E3 |
| `public/` | 648 K | 2026-10-11 | `express.static` (server.ts:9590) | KALIR | `CNAME`, `sw.js`, ikonlar |
| `deploy/` | 108 K | 2026-10-11 | Oracle dağıtımı | KALIR | `create-vcn.sh`, `fix-route.sh`, `oracle-setup.sh`, `ecosystem.config.cjs` tek seferlik/kullanılmayan → ARŞİVLE (?) |
| `docs/` | 168 K | 2026-10-10 | Ajan/insan belgeleri | KALIR | `MEDSOR_SISTEM_DOKUMANI.md` eski betikleri (medical_data_*, build_batch*) anlatıyor — güncel değil |
| `supabase/` (migrations) | 52 K | 2026-10-11 | Şema | KALIR | |
| `supabase-server/` | 2.2 G | 2026-10-11 | Çalışan 11 Supabase konteyneri (`com.docker.compose.project.working_dir`=burası) | KALIR | 2.2 G'nin tamamı `volumes/` (canlı DB) |
| `curriculum/` | 40 K | 2026-10-05 | server.ts, `v2/core/curriculum.py`, semantic | KALIR | `*.before_program_sync.json` yedeği ARŞİVLE (?) |
| `dashboard_server.py` | 280 K | 2026-10-07 | `meds-dashboard.service` (:8085) | KALIR | |
| `.github/` | 20 M | 2026-10-11 | `workflows/deploy-oracle.yml`, `deploy.yml` (gh-pages) | KALIR | `skills/impeccable` 20M kopya (bkz. aşağı) |
| `.agents/`, `.claude/` | 20 M + 20 M | 10-07 / 10-08 | Ajan araçları (impeccable skill) | KALIR (?) | Aynı skill 3 kopya (.agents/.claude/.github), içerikleri birbirinden **farklı** sürüm; rsync ile Oracle'a gidiyor. Tekilleştirme kararı (?) |
| `.codex/`, `.impeccable/`, `skills-lock.json` | küçük | 10-04…10-07 | Ajan araçları | KALIR | |
| `AGENTS.md` (meds) | 28 K | 2026-10-10 | Ajan talimatı | KALIR (T8 gözden geçir) | **Çelişki:** "Zero-Cost Local GPU" ilkesi ↔ PROJE_TANITIMI "yerel GPU çalıştırılmaz, ücretsiz bulut" |
| `CLAUDE.md`, `README.md` | 8 K + 8 K | 10-09 / 10-06 | Belgeler | KALIR | `link-exam-questions.mts` gibi eski betiklere atıf |
| `PROJECT_INSTRUCTIONS.md`, `PRODUCT.md` | 12 K + 8 K | 10-09 / 10-05 | Atıf yok | **ARŞİVLE (?)** (T8) | "v2.5 Tamamen Yerel AI" — güncel mimariyle çelişiyor |
| `metadata.json`, `firebase-applet-config.json`, `firebase-blueprint.json`, `firebase.json`, `firestore.rules` | küçük | 2026-10-04 | `firebase-applet-config` → `firestoreDb.ts` + sync betikleri; `metadata.json` (AI Studio uygulama tanımı) adı genel, eşleşmeler başka dosyalara ait; `firebase-blueprint` atıf yok | KALIR (firebase*) / **ARŞİVLE (?)** (`metadata.json`, `firebase-blueprint.json`) | AI Studio kökenli kalıntılar |
| `404.html`, `.nojekyll` | küçük | 2026-10-04 | `deploy-gh-pages.cjs`, `.github/workflows/deploy.yml` | KALIR | GitHub Pages yedeği |
| `Dockerfile`, `docker/entrypoint.sh`, `docker-compose.yml`, `docker-compose.ollama.yml` | küçük | 2026-10-05 | Yalnız birbirine atıf; `meds-ollama` konteyneri çalışmıyor (Ollama native, E1) | **ARŞİVLE (?)** | Oracle `deploy/oracle/Dockerfile.oracle` kullanıyor |
| `start-supabase.sh`, `stop-supabase.sh`, `apply-migrations-to-local.sh` | küçük | 2026-10-04 | PROJE_TANITIMI §6 (elle kullanım) | KALIR | |
| `*.bat` (8), `start-meds-daemon.vbs`, `run-meds-sync.bat`, `switch-env-to-*.bat`, `apply-migrations-to-local.bat` | küçük | 2026-10-04 | Windows dönemi; yalnız `AdminPanelModal.tsx` metinleri / `manage-service.ps1` atıf | **ARŞİVLE** | Linux'ta çalışmaz |
| `linux/common.sh` | 8 K | 2026-10-04 | Yalnız `.gitignore` | **ARŞİVLE (?)** | |
| `transcribe_medical_audio.py` | 28 K | 2026-10-04 | Atıf yok (npm `transcribe:*` başka betik kullanıyor) | **ARŞİVLE** | |
| `test_shadow.pptx`, `test_table.pptx` | 28 K × 2 | 2026-10-04 | Atıf yok | **SİL-ADAYI** | |
| `get-pip.py` | 2.2 M | 2026-08-05 | Atıf yok (git'te takipsiz) | **SİL-ADAYI** | Yol haritası §3 ile uyumlu |
| `assets/` (meds kökü) | 4.1 M (9) | 2026-10-04 | Atıf yok; eski bir derleme çıktısı (`index-B-l1WRHu.js` …) ama **git'te takipli** | **SİL-ADAYI** | `git rm` gerekir |
| `__pycache__/` (meds kökü) | 316 K | 2026-10-07 | — | **SİL-ADAYI** | |
| `bun.lock` | 108 K | 2026-10-04 | npm kullanılıyor (package-lock); atıf yok | **SİL-ADAYI (?)** | |
| `.env` | 8 K | 2026-10-11 | Tüm üniteler `EnvironmentFile` | KALIR | Değişken isimleri §7 |
| `.env.example` | 4 K | 2026-10-08 | Şablon | KALIR | `.env`'in gerisinde (yol haritası §0) |
| `.env.cloud.bak` | 4 K | 2026-10-04 | `scripts/switch-env-to-local.mjs` (Windows dönemi) | **TAŞI** (şifreli yedeğe) | E8: rsync ile Oracle'a gidiyor |
| `.git/` | 304 M | — | — | KALIR | |
| `node_modules/` | 1.3 G | — | Derleme | KALIR | |
| `.venv-ocr/` | 6.6 G | — | Tüm Python üniteleri (`meds-core`, `revize`, `v2search`, `v2semantic`, `embed`, `phases`, `pipeline`, `run.sh`) | KALIR | |
| `.venv/` | 71 M | 2026-10-11 | Grep eşleşmeleri `.venv-ocr`'a ait; doğrudan kullanan bulunamadı (py3.14) | **SİL-ADAYI (?)** | Bugün değişmiş; paralel oturum kullanıyor olabilir |
| `.venv_train/` | 5.4 G | 2026-10-05 | Hiçbir ünite/betik kullanmıyor (`scripts/training/` docker compose kullanıyor) | **SİL-ADAYI (?)** | `requirements-train.txt`'ten yeniden kurulabilir. Eğitim planı var mı? |
| `models/medsoru-d3-qlora/` | 322 M | 2026-10-07 | Yalnız `scripts/training/train_lora.py`; Ollama listesinde yok (servis edilmiyor) | **ARŞİVLE (?)** | 2 checkpoint (127M+127M) + adapter |
| `training_data/` | 16 M | 2026-10-07 | `scripts/training/train_lora.py` | **ARŞİVLE (?)** | Eğitimle birlikte karar |
| `dist/` | 1.2 G (9445) | 2026-10-11 | `express.static` (server.ts:9588) | KALIR + **bayat parçalar SİL-ADAYI** | E3: 280 dosya/100 MB canlı, 9140 dosya/1085 MB bayat. Elle silme yok — T3 prune betiği ile |
| `dist-gh/` | 434 M (1334) | 2026-10-10 | `npm run deploy` (gh-pages, pasif yedek site) | **SİL-ADAYI (?)** | Yeniden üretilebilir; GitHub Pages yedeği gerekiyorsa KALIR |

### 2.2 `meds/data/` (birincil kayıtlar; Oracle'da volume)

| Yol | Boyut | Son değişim | Kanıt | Öneri | Not |
|---|---|---|---|---|---|
| `pastQuestions.json` | 72 M | 10-11 | server.ts:1692 (`PAST_QUESTIONS_FILE`), 4+ servis | KALIR | 5713 kayıt (asıl) |
| `questions.json` | 368 K | 10-11 | server.ts, `api.ts`, dashboard | KALIR | |
| `users.json`, `admin_notifications.json`, `admin_push_subscriptions.json`, `web_push_keys.json`, `processed_notification_ids.json`, `learn_feedback.json`, `music_playlists.json`, `user_answer_polls.json`, `deleted_past_questions.json`, `sent_emails.json`, `smtp_config.json`, `manage_settings.json`, `drive_sync_settings.json`, `ai_error_logs.json`, `ai_interactions.json`, `ornek_soru_bildirimleri.jsonl`, `rag_indexing_manifest.json`, `real_drive_slides.json`, `drive_check_result.json` | toplam ~1 M | 10-07…10-11 | server.ts / ilgili servisler (refs tablosu) | KALIR | Kullanıcı/jurnal verisi |
| `lecture_notes.json` | 2.5 M | 10-08 | `serverLectureNotes.ts:17`, `localRagEngine.ts:581`, `lectureRepairEngine.ts` | KALIR | 55 kayıt (2026-27 güncel) |
| `lectureSummariesCatalog.json` | 11 M | 10-10 | server.ts:7000, localRagEngine, notebooklm servisleri | KALIR | `src/data` kopyasıyla md5 aynı |
| `local_rag_chunks.json` | 104 M | 10-11 | `localRagEngine.ts`, `notebooklmManageService.ts` | KALIR | gitignore'lı + takipsiz (E9); yeniden üretilebilir |
| `deepseek_contributions.json` | 19 M | 10-04 | `deepseekDataService.ts`, `index-rag-knowledge.mjs` | KALIR | |
| `notebooklm_contributions.json` | 5.3 M | 10-10 | `notebooklmManageService.ts` | KALIR | `src/data` kopyasıyla md5 aynı (servis ikisini de yazıyor) |
| `auto_repair/` | 3.6 M | 10-11 | `autoErrorRepairEngine.ts` | KALIR | |
| `interactive_decks_registry.json` | 32 K | 10-04 | `orchestrate_drive_curriculum_ai.mjs` (npm `sync:drive`) | KALIR | Tohum adayı |
| `script_jobs_history.json`, `script_logs/` | 96 K | 10-08 | `automation-runner.mjs` (server spawn) | KALIR | |
| `donem3_curriculum.json`, `user_drive_catalog.json`, `drive_crawler_results.json`, `ai-redactor-status.json`, `self_healing_health_status.json` | ~350 K | 10-04…10-07 | Bundled/npm betikler | KALIR | |
| `deep_slide_matching_report.json`, `eliminated_questions_report.json`, `slide_audit_report.json`, `slide_match_report.json`, `spelling_errors_report.json`, `verification_report.json`, `rag_evaluation_report.json`, `gemini_v3_ingestion_report.json`, `missing_drive_pdfs.json`, `truly_missing_drive_pdfs.json` | ~200 K | 10-04…10-08 | Yalnız onları üreten tek seferlik betikler (bazıları `archive/`) | **ARŞİVLE** | Rapor çıktıları |
| `extracted_lectures/` | 656 K | 10-04 | Yalnız `archive/` betikleri | **ARŞİVLE** | |
| `lecture_notes_2026_2027.json` | 2.5 M | 10-08 | Atıf yok | **ARŞİVLE** | 50 kayıt; `lecture_notes.json` (55) ile farklı md5 — eski ara sürüm |
| `lecture_notes_supabase.json` | 24 M | 10-05 | Yalnız `archive/download_and_merge_supabase.py` | **ARŞİVLE** | 885 kayıt |
| `lecture_notes.legacy_backup.json` | 53 M | 10-08 | Atıf yok; `sync-data.sh` hariç tutuyor; **git'te takipli** | **TAŞI** (yedek) | 881 kayıt |
| `pastQuestions.json.bak_manual_import` | 61 M | 10-10 | Atıf yok | **TAŞI** (yedek) | 4924 kayıt |
| `pastQuestions.backup.json` / `.backup_before_verify.json` / `.backup_before_typo_fix.json` | 8.2 M / 6.8 M / 5.1 M | 10-04 | Yalnız onları yazan tek seferlik betikler (`migrate-separate…`, `verify-question-answers`, `fix-question-typos`) | **TAŞI** (yedek) | 2922 kayıtlık eski hâller |
| `questions.backup.json` | 5.0 M | 10-04 | `migrate-separate-current-and-past.mjs` | **TAŞI** (yedek) | |

**meds/data yedek toplamı:** 6 dosya / ~139 MB (TAŞI).

### 2.3 `meds/src/data/` (derleme girdisi; Oracle'a rsync)

| Yol | Boyut | Son değişim | Kanıt | Öneri | Not |
|---|---|---|---|---|---|
| `interactive_learning_decks.json` | 82 M | 10-11 | Tek kaynak; `splitLearningDecks` (vite), server.ts | KALIR | 114 deste |
| `decks/` (`catalog.json`, `items/` 114, `packages/` 30) | 74 M | 10-11 | `deckStore.ts`, vite eklentisi, server.ts | KALIR | `items/` derlemede üretilir (deploy rsync'te hariç). `packages/` yalnız k1-01…29 (E4) |
| `kazanimlar/` | 13 M | 10-10 | vite manualChunks, `KazanimlarView`, router | KALIR | `k1` parçası 8.2 MB (en büyük canlı chunk) |
| `summaries/`, `summaries_meta.json`, `summaries_enrichment.json` | 11 M + 352 K | 10-08…10-09 | `LectureSummariesView`, server.ts | KALIR | |
| `ornek_sorular/` | 15 M | 10-09 | server.ts, router, `ManageDataSection` | KALIR | |
| `lectureSummariesCatalog.json` | 11 M | 10-10 | `notebooklmManageService.ts` (SRC kopya), server | KALIR (?) | `data/` ile md5 aynı; çift yazım (E5 benzeri) |
| `notebooklm_contributions.json` | 5.3 M | 10-10 | `notebooklmManageService.ts` (SRC kopya) | KALIR (?) | `data/` ile md5 aynı; istemci import etmiyor |
| `pastQuestions.json` | 72 M | 10-11 | server.ts:1791 ikinci kopya yazımı; istemci import etmiyor | **KALIR (?)** → T4/F'de tekilleştir | E5 |
| `pastQuestions.json.bak_manual_import` | 61 M | 10-10 | Atıf yok; `data/` kopyasıyla md5 AYNI | **SİL-ADAYI** | Rsync ile Oracle'a gidiyor (E8) |
| `lecture_notes.json` | 32 M | 10-04 | Yalnız `serverLectureNotes.ts:127/285` — `data/lecture_notes.json` YOKSA yedek yol | **ARŞİVLE (?)** | 864 kayıt (eski müfredat); `data/` her yerde var → fiilen kullanılmıyor. Git'te 32 MB |
| `medical_glossary.json`, `medical_encyclopedia.json`, `medicalConcepts5000.json`, `diseases.json`, `slidePdfMappings.json`, `question_cards.json`, `mufredat_paketi.json`, `musicTracks.json`, `curriculum_disciplines.json`, `pool_question_clusters.json` | ~6 M | 10-04…10-11 | İlgili bileşen/servisler (refs tablosu) | KALIR | |
| `*.ts` (`deckStore`, `curriculumData`, `glossary`, `deckPdfCatalog`, `driveCatalog`, `bundledScripts`) | küçük | 10-04…10-11 | İstemci importları | KALIR | |
| `disease_entities.json`, `medical_fts.db`, `processed_diseases.txt` | 484 K + 656 K + 12 K | 10-11 | Yalnız `scripts/akbc_disease_pipeline.py` (bugün değişmiş) | KALIR (?) | Paralel oturumun yeni işi olabilir |
| `study_questions/` | 2.2 M (15) | 10-04 | Uygulama import etmiyor; yalnız `archive/` betikleri | **ARŞİVLE (?)** | |
| `learning_batch_queue.json`, `learning_decks_meta.json` | 12 K + 4 K | 10-04 | Yalnız `archive/` betikleri | **ARŞİVLE** | |

---

## 3. `meds/scripts/`

### 3.1 Alt klasörler

| Yol | Boyut | Son değişim | Kanıt | Öneri | Not |
|---|---|---|---|---|---|
| `agents/` | 452 K | 10-11 | Üniteler: embed, gpuguard, phases, pipeline, watchdog, downloads-watcher (`run.sh`), faz14 (`faz14_auto.sh`); server.ts:5895 | KALIR | Boru hattı çekirdeği |
| `v2/` | 1.3 M | 10-08 | `meds-core` (`-m v2 cycle`), `meds-revize` (`-m v2.revize`), `meds-v2search` | KALIR | |
| `semantic/` | 108 M | 10-08 | `meds-v2semantic` (`-m semantic.server`, :8093), server.ts `/api/v2/semantic/*` | KALIR | `data/` 108 M (indeks); Oracle'a rsync'leniyor |
| `pipeline/` | 88 K | 10-08 | server `/api/admin/scripts/pipeline/run`, dashboard (`01-inventory`, `02-download`), PROJE_TANITIMI (`11-restore-summary-lines.py`) | KALIR | |
| `advanced_ai/` | 1.2 M | 10-11 | dashboard, `phase_cycle.py`, `faz14_auto.sh`, `phaseInsightsService.ts` | KALIR | İçinde tek seferlik olanlar var (`fix_curb65.py`, `analyze_corrupted_130.py`, `categorize_corruptions.py`, `split_issue_groups.py`) → ARŞİVLE (?) |
| `vite/` | 8 K | 10-11 | `vite.config.ts` (`splitLearningDecks`) | KALIR | |
| `design/` | 16 K | 10-11 | `check-contrast.mjs` (appearance.css açıklaması) | KALIR | |
| `eval/` | 8 K | 10-07 | `semantic/run.py` | KALIR | |
| `deck_generators/` | 7.0 M (166) | 10-10 | Kök `patch_*.py` buraya yazıyor; `build_deck_54/61_full.py` `meds_database_v2/ders_notlari_k1` okuyor | KALIR (?) | Deste 48–66 üretim aracı; aktif üretim bitince ARŞİVLE |
| `k1_decks/` | 22 M (724) | 10-09 | `validate_learning_decks.py`'yi import ediyor; dışarıdan çağıran yok | **ARŞİVLE (?)** | Ders 1–29 deste kurucuları (yeniden üretim izi). Kök `scripts/` ile 53 dosya ortak |
| `build_k1_48_data/`, `build_k1_49_data/` | 1.5 M + 24 K | 10-10 | Yalnız `build_deck_48_full.py` | **ARŞİVLE** | |
| `build_k1_50_data` … `build_k1_53_data`, `curriculum_generators/` | 0 | — | Boş klasörler | **SİL-ADAYI** | |
| `data_decks/`, `ileri_tumor_genetigi/`, `tumor_immuno_builder/` | 80 K + 176 K + 332 K | 10-04…10-10 | Atıf yok | **ARŞİVLE** | Tek deste kurucuları |
| `training/` | 48 K | 10-05 | Atıf yok (elle çalıştırılan LoRA eğitimi) | **ARŞİVLE (?)** | `models/`, `.venv_train` ile birlikte karar |
| `archive/` | 5.5 M (143) | 10-07 | Hedef klasör | KALIR | T2 arşiv hedefi |
| `__pycache__/` | 304 K | 10-10 | — | SİL-ADAYI | |

### 3.2 Üst seviye betikler (166 dosya) — gruplar

| Grup | Dosyalar | Son değişim | Kanıt | Öneri |
|---|---|---|---|---|
| **Kapı/boru hattı (canlı)** | `validate_learning_decks.py`, `build_kazanim_deck_index.py`, `automation-runner.mjs`, `scripts-meta.json`, `meds-local-sync.mjs`, `verify-question-answers.mjs`, `transcribe-drive-audio.mjs`, `sync-drive-updates.mjs`, `deep-ai-redactor.mjs`, `manage-slide-relations.mjs`, `match-and-link-lecture-slides.mjs`, `audit-and-disconnect-faulty-slides.mjs`, `slide-matching-utils.mjs`, `master_controller.py` (+`monitor.py`, `fast_hybrid_server.py`), `manage-service.sh`, `build_curriculum_catalog.py`, `akbc_disease_pipeline.py` | 10-04…10-11 | server.ts spawn/require, dashboard, AGENTS.md/PROJE_TANITIMI, `DEGISIKLIK_KAYDI` | KALIR |
| **npm scripts** | `auto-git-sync.mjs`, `build_learning_decks.py`, `check-online-status.ts`, `detect-database-updates.mjs`, `generate_medical_glossary.py`, `index-rag-knowledge.mjs`, `orchestrate_drive_curriculum_ai.mjs`, `sync_deepseek_data.py` | 10-04…10-07 | `package.json` | KALIR |
| **Yönetim panelinin "Betikler" sekmesi** (`bundledScripts.ts` + `scripts-meta.json`) | `background-ai-redactor.mjs`, `build-database-json.mjs`, `build_full_drive_slides.mjs`, `crawl-all-drive-folders.mjs`, `deploy-gh-pages.cjs`, `detect-faulty-ocr.mjs`, `download-*.mjs`, `enrich-drive-slides.mjs`, `extract-*.py`, `filter-donem3-and-clean-ocr.mjs`, `fix-*.mjs`, `inspect-sources.mjs`, `local-drive-sync-agent.mjs`, `migrate-separate-current-and-past.mjs`, `process-*.mjs`, `rebuild-all-past-questions.mjs`, `sync-all-to-{firebase,firestore,supabase}.mjs`, `sync-database-json-to-cloud.mjs`, `sync-past-questions-to-supabase.mjs`, `start-*-tunnel.mjs`, `test-*.mjs`, `update-drive-catalog.mjs`, `merge-same-exam-duplicates.mjs`, `self-healing-auditor.mjs`, `deep-triple-slide-matcher.mjs`, `show-notification.ps1`, `manage-service.ps1`, `*.bat` | 10-04…10-09 | UI listesi (çalıştırılabilir) | KALIR (?) — çoğu Windows/eski Firebase dönemi; panel listesinden çıkarılıp arşivlenmesi kullanıcı kararı |
| **Yardımcı (başka betikçe import)** | `ds_pipeline.py`, `ds_quote_index.py`, `enrichment_definitions.py`, `sync_to_supabase_v2.py`, `sync_user_drive_folder.mjs`, `switch-env-to-local.mjs` | 10-04…10-10 | ds_batches/ds_assemble, retrofit, post_lora, orchestrate, start-supabase.sh | KALIR (bağlı olduğu betikle birlikte karar) |
| **Deste-49/5-deste üretim kalabalığı (tek seferlik)** | 71 dosya, hepsi 2026-10-10: `apply_deck_48.py`, `apply_generated_deck.py`, `ai_deck_compiler.py`, `auto_build_*`, `auto_curriculum_compiler.py`, `auto_deck_49_*`, `auto_deck_synthesizer.py`, `auto_generator_*`, `batch_*`, `build_deck_48_full.py`, `build_deck_49_*`, `build_deck_50_master.py`, `build_full_deck_49.py`, `build_k1_49_*`, `gen_*` (8), `generate_5_decks_*`, `generate_all_5_decks_*` (11), `generate_all_deck49.py`, `generate_all_five_decks.py`, `generate_clean_deck_49.py`, `generate_complete_5_decks.py`, `generate_deck_49*`, `generate_deck_core/util.py`, `generate_k1_deck_49.py`, `make_deck_*`, `pipeline_build_5_decks.py`, `write_deck_49_s1.py`, `retrofit_all_past_decks.py`, `test_*.py` (7), `test_json_write.json`, `sample_slide.json` | 10-10 | Canlı kodda atıf yok (~133 KB) | **ARŞİVLE** (`test_*`, `sample_slide.json`, `test_json_write.json` → SİL-ADAYI) |
| **Eski tek seferlikler (10-04/10-09)** | `build_batch{1..4}_deck.py`, `build_chunked_study_questions.py`, `medical_data_*.py` (6), `medical_master_expansion.py`, `medical_taxonomy_pharm.py`, `generate_genetics_pediatric_complete.py`, `ds_assemble.py`, `ds_batches.py`, `gpu_recovery.sh`, `link-exam-questions.mts`, `index-practice-questions-rag.mjs`, `sync-all-practice-questions-to-supabase.mjs`, `retrospective_deck_repair.py`, `VERIFY_INSTRUCTIONS.md` | 10-04…10-09 | Yalnız `docs/MEDSOR_SISTEM_DOKUMANI.md`/README/CLAUDE.md anlatımı | **ARŞİVLE (?)** — `sync-all-practice-questions-to-supabase.mjs` ve `index-practice-questions-rag.mjs` elle çalıştırılıyor olabilir |
| `monitor.py.bak` | 1 | 10-05 | — | **SİL-ADAYI** |

---

## 4. Veri klasörleri — alt klasör düzeyi

### 4.1 `meds_database/` (1.2 G)

| Yol | Boyut | Son değişim | Kanıt | Öneri | Not |
|---|---|---|---|---|---|
| `derived/rag_vektor` | 450 M | 10-11 | `rag_vector_build*.py`, `rag_bge_m3_test_backfill.py`, `new_data_pipeline.py`, dashboard | KALIR | Vektör önbelleği (yol haritası: git yok, yedeklenir) |
| `derived/clean_notes` | 32 M | 10-07 | `lectureCleanOverlay.ts`, `phase_cycle.py`, `rag_refresh.py` | KALIR | |
| `derived/curriculum_links` | 8.5 M | 10-07 | `questionQuarantine.ts`, `phase_cycle.py`, `publish_to_database.py` | KALIR | |
| `derived/curriculum_links.prev` | 8.3 M | 10-07 | `publish_to_database.py` otomatik geri dönüş kopyası | KALIR | Her yayında yeniden oluşur |
| `derived/phase8` | 16 M | 10-05 | Kodda `derived/phase8` atfı yok (faz çıktıları `meds_temp/phase8`'de) | **ARŞİVLE (?)** | Eski konum olabilir |
| `derived/{entities, phase_insights, quarantine, resplit, learn_links.json, manual_overrides, ornek_sorular, ai_bilgi}` | ~12 M | 10-07…10-11 | `phaseInsightsService.ts`, `phaseDataExplorer.ts`, server, `localRagEngine.ts`, `PracticeQuestionsView.tsx` | KALIR | |
| `meds_sorular` | 327 M | 10-08 | server.ts, `serverLectureNotes.ts`, `sync-drive-updates.mjs`, `meds-local-sync.mjs` | KALIR | **E6: 98/99 dosya `meds_downloads` ile aynı (324 MB)** → T4'te bağlantıya çevir (?) |
| `meds_sorular_txt` | 20 M | 10-08 | server.ts, sync betikleri | KALIR | |
| `index` | 100 M | 10-07 | `stage4_database.py` (meds-pipeline), `00-init.mjs` | KALIR | `.npy` vektörler |
| `chunks`, `sources` | 24 M + 1.7 M | 10-07 | `stage4_database.py`, server.ts | KALIR | |
| `questions` | 5.6 M | 10-07 | Boru hattı aşama 4 | KALIR | |
| `deepseek_meta_data` | 53 M | 10-07 | `geminiV3DataService.ts` (`METADATA_DIR`), `localRagEngine.ts` | KALIR | |
| `ortak` (`rag` 18M, `veri`, `KATALOG.json`) | 18 M | 10-11 | `meds-core` (`v2_katalog.json` yazıyor), `localRagEngine.ts`, `build_curriculum_catalog.py` | KALIR | |
| `taxonomy`, `schema`, `reports`, `README.md`, `2026_2027_guncel_kaynaklar.json` | <1 M | 10-04…10-08 | `parse_ders_programi.py`, `stage3_merge.py`, `00-init.mjs`, `generate_cloud_study_notes.py` | KALIR | |
| `backups/supabase_export` | 72 M | 10-05 | Atıf yok | **TAŞI** (yedek) | |
| `database_json`, `ders_notlari_pdf`, `ders_notlari_txt`, `kurul_ders_notlari`, `kurul_ders_notlari_txt`, `redakte_sorular` | 0 dosya (boş klasör ağaçları) | — | Eski betikler yol olarak biliyor | KALIR (?) | Boş; zararsız. T4'te temizlenebilir |

### 4.2 `meds_database_v2/` (195 M)

| Yol | Boyut | Son değişim | Kanıt | Öneri | Not |
|---|---|---|---|---|---|
| `phase14_past_question_editor` | 1.4 M | 10-11 | `server.ts:2677` (`PHASE14_DIR`), `phase14Overlay.ts`, dashboard | KALIR | |
| `ders_notlari_k1` | 2.5 M | 10-08 | AGENTS.md kural 4 (soru kaynağı), deste kurucuları | KALIR | |
| `kurul1_ders_paketleri` | 4.1 M | 10-08 | PROJE_TANITIMI adım 6, `s15/s16`, `build_curriculum_catalog.py` | KALIR | |
| `ornek_sorular_k1` + `_revize`, `_v3`, `_v4`, `_v5_muse`, `_v6_muse` | 15+5.4+0.1+3.6+3.0+8.0 M | 10-08…10-09 | `s16_ornek_sorular.py` (v1), `sync-all-practice-questions-to-supabase.mjs` (6 sürümün hepsini yüklüyor) | KALIR | Sürümler Supabase'e ayrı kaynak olarak gidiyor |
| `tibbi_terimler_sozlugu` | 6.1 M | 10-09 | `localRagEngine.ts:1149` | KALIR | |
| `soru_birlestirme` | 84 K | 10-07 | `questionMerge.ts`, `questionCrossAuditService.ts` | KALIR | |
| `reference` (icd10) | 612 K | 10-06 | `semantic/medical.py`, faz betikleri | KALIR | |
| `concept_ids`, `deep_metadata`, `deep_metadata_validated`, `evidence_thesaurus`, `medical_thesaurus`, `blacklist`, `phase7_v2`, `slide_reconstructed`, `questions`, `phase5_consensus_state.json` | ~27 M | 10-05…10-07 | dashboard, `phase_cycle.py`, `new_data_pipeline.py`, `gpu_guard.py`, `monitor.py`, faz 5–10 betikleri | KALIR | Faz zinciri girdileri |
| `faz14_kurtarilan_sorular` | 19 M (3603) | 10-09 | Yazan: kök `scripts/apply_web_grounded_party*.py`; okuyan: yalnız `advanced_ai/fix_curb65.py` | KALIR (?) | Canlı tüketicisi belirsiz — kurtarılan sorular `pastQuestions`'a işlendiyse ARŞİVLE |
| `phase15_quality_audit` | 35 M (8454) | 10-08 | Yalnız `phase15_*_auditor.py` | KALIR (?) | Faz 15 sürüyor mu? Bittiyse ARŞİVLE |
| `phase14_backup` | 68 M | 10-09 | Yalnız tek seferlik denetim betikleri (`analyze_corrupted_130.py` …) | **TAŞI** (yedek) | |
| `soru_uretici_k1.py`, `soru_uretici_k1_v2.py` | 16 K | 10-08 | Atıf yok; veri klasöründe kod | **ARŞİVLE** → `meds/scripts/archive/` | |
| `reports` | 0 | — | boş | KALIR (?) | |

### 4.3 `meds_database_core/` (126 M) — tamamı **KALIR**

`meds-core` (her 600 sn tur; son tur 20:00), `meds-revize`, `meds-v2search` (:8092), `meds-v2semantic` (:8093) `MEDS_CORE_DIR` ile buraya okur/yazar; server.ts:1100 `meds_database_core` varsayılanı. Alt klasörler: `chunks` 27M, `vectors` 50M, `notes` 15M, `questions` 13M, `summaries` 11M, `derived` 7.3M, `sources` 2M, `_state` 1.8M, `reports` 1.2M, `revize_v2` 1.1M, `KATALOG.json`. Son değişim 10-08…10-11.

### 4.4 `meds_temp/` (947 M)

| Yol | Boyut | Son değişim | Kanıt | Öneri | Not |
|---|---|---|---|---|---|
| `temp1`, `temp2`, `temp3` | 27 + 31 + 142 M | 10-07…10-10 | `stage2_clean.py`, `stage3_merge.py`, `new_data_pipeline.py`, `11-restore-summary-lines.py`, dashboard | KALIR | Boru hattı çekirdeği |
| `state` | 229 M | 10-11 | Tüm servisler (lock/pid/ayarlar); `disk_emb_cache` 188M + `embcache.pkl` 41M (`stage3_merge.py` önbelleği) | KALIR | Önbellekler yeniden üretilebilir |
| `logs` | 6 M | 10-11 | server, dashboard, servisler | KALIR | |
| `study` | 20 M (482) | 10-09 | server.ts, PROJE_TANITIMI adım 6 (`study/k1/NN_*.md`) | KALIR | |
| `phase8`, `phase9`, `phase10`, `phase11` | 18+18+18+23 M | 10-07 | `phase_cycle.py`, `publish_to_database.py`, dashboard | KALIR | |
| `phase8.prev`, `phase9.prev`, `phase10.prev` | 18 M × 3 | 10-07 | `phase8_curriculum_graph.py:670` atomik geri dönüş kopyası | KALIR | Bir sonraki üretimde yeniden oluşur |
| `hakem`, `review`, `jobs`, `ocr`, `extract`, `scratch` | <1 M | 10-07 | server.ts, dashboard, `00-init.mjs` | KALIR | Bazıları boş |
| `supabase_local.dump` | 330 M | 10-11 | Atıf yok (Oracle'a pg_restore için üretilmiş) | **TAŞI** (yedek) | `sync-vectors.sh` ayrı dump adı kullanıyor (`rag_chunks_sync.dump`) |
| `ozet_satir_yedek` | 32 M | 10-08 | `11-restore-summary-lines.py` yazım-öncesi yedeği | **TAŞI** (yedek) | |
| `before_phase14_last_fix.json`, `four_options_57.json`, `missing_answers_66.json`, `kazanim_denetim_20261009/`, `soru_kurtarma/` | ~3.7 M | 10-09…10-10 | Atıf yok (tek seferlik çalışma artığı) | **ARŞİVLE** | |

### 4.5 `meds_database_v3_export/`, `meds_export/`, `meds_downloads/`
Yukarıda §1'de: üçü de **KALIR** (E7: ilk ikisi Oracle'da bağlı değil).

### 4.6 `yedek/` (1.2 G) — tamamı **TAŞI** → `/home/indu/medsor-yedek/` (T1). Kodda `yedek/` yoluna atıf yok.

---

## 5. Cihaz servisleri (`~/.config/systemd/user/`)

| Ünite | Durum | Çalıştırdığı | Port | Bellek | GPU? | Öneri |
|---|---|---|---|---|---|---|
| `meds-web` | enabled/active | `npm run dev` (`tsx watch server.ts`), `NODE_ENV=development` | :3000 | 1179 MB | Hayır | KALIR |
| `meds-dashboard` | enabled/active | `python3 dashboard_server.py` | :8085 | 172 MB | Hayır (GPU durumunu gösterir) | KALIR |
| `meds-core` | enabled/active | `.venv-ocr … -m v2 cycle --watch --interval 600 --roots meds_downloads` | — | 928 MB | Hayır ("GPU yok, ücretsiz bulut") | KALIR |
| `meds-revize` | enabled/active | `-m v2.revize run --limit 200 --watch` | — | 21 MB | Hayır | KALIR (son turlar 0 işlem — boşta) |
| `meds-v2search` | enabled/active | `-m v2.search_server` (CPU e5) | :8092 | ~8 MB* | Hayır | T5 birleştirme adayı |
| `meds-v2semantic` | enabled/active | `-m semantic.server` (CPU e5 + FAISS) | :8093 | ~8 MB* | Hayır | T5 birleştirme adayı |
| `meds-embed` | enabled/active | `scripts/agents/embed_server.py` (e5-small, `CUDA_VISIBLE_DEVICES=`) | :8091 | ~8 MB* | Hayır | T5 birleştirme adayı |
| *(ünitesiz)* bge-m3 embed | elle başlatılmış | `scripts/agents/embed_server.py` (pid 702110) | :8094 | — | Hayır | **E2: ünite yazılmalı** (`.env MEDS_EMBED_URL` bunu gösteriyor) |
| `meds-downloads-watcher` | enabled/active | `scripts/agents/run.sh watch` (drop-in `CUDA_VISIBLE_DEVICES=`) | — | 7 MB | Hayır | KALIR |
| `meds-pipeline` | enabled/active | `pipeline_runner.py` (Ollama :11434 sağlığı bekler) | — | 34 MB | Ollama'ya bağlı (Ollama GPU kullanıyor) | KALIR (?) |
| `meds-phases` | enabled/active | `phase_cycle.py` — log: "elle kip, otomatik geçiş kapalı" | — | 2.4 MB | Evet (nvidia-smi sıcaklık, Ollama boşaltma) | KALIR (?) — boşta bekliyor |
| `meds-gpuguard` | enabled/active | `gpu_guard.py` (sıcaklık <89 °C) | — | 10 MB | Evet (nvidia-smi) | KALIR (?) — GPU var (E1) ama `.env` GPU'yu kapatmış |
| `meds-watchdog` | enabled/active | `watchdog.py` (Ollama/Docker `meds-ollama`, `open-webui` denetimi) | — | 45 MB | Evet (nvidia-smi) | KALIR (?) — `meds-ollama` konteyneri yok (Ollama native); denetim listesi eskimiş |
| `meds-local-sync` | **disabled/inactive** | `node scripts/meds-local-sync.mjs` | — | — | Hayır | **ARŞİVLE (?)** (server.ts de bu betiği tetikleyebiliyor) |
| `meds-faz14-ucretsiz.service` + `.timer` | static / **timer disabled** | `scripts/agents/faz14_auto.sh` (11:15, 18:00) | — | — | Hayır | KALIR (?) — devre dışı; Faz 14 bitti mi? |
| `eski_yol_yedek/` (8 eski ünite + drop-in) | yüklenmez | — | — | — | — | **TAŞI** (yedek) |

\* `MemoryCurrent` düşük görünüyor (çoğu swap'ta olabilir). Docker: yalnız `supabase-server` yığını (11 konteyner, healthy) + root docker'da `open-webui` (:8080). `meds/docker-compose*.yml`'deki `meds-ollama` çalışmıyor. PM2 listesi boş.

GPU özeti: `nvidia-smi` mevcut → RTX 4060 Laptop, 1046 MiB kullanımda (yalnız native `ollama llama-server`). GPU'ya dokunan üniteler: `meds-gpuguard`, `meds-phases`, `meds-watchdog` (izleme) ve dolaylı olarak `meds-pipeline` (Ollama). Diğer 8 ünite açıkça CPU/bulut.

---

## 6. `dist/assets` ayrıntısı

| Ölçü | Değer |
|---|---|
| Toplam | 9420 dosya, 1185 MB |
| Canlı (index.html + sw.js'ten import grafiği BFS) | 280 dosya, 100 MB |
| Bayat | 9140 dosya, 1085 MB |
| Bayatların tarih dağılımı | 10-09: 4238 · 10-10: 2289 · 10-11: 2893 (toplam dosya) — **hiçbiri >7 gün değil** |
| En büyük canlı parçalar | `local-data-kazanimlar-k1` 8.2 MB, `summaries-kurul5` 2.4 MB, `k1p-k1-09…` 2.3 MB, `entry-index` 1.8 MB |

Öneri: T3 prune kuralı "son 2–3 derlemenin import grafiği dışında kalan + X saatten eski" olmalı (7 gün değil); eski SW istemcileri için son 2 derleme korunur. `meds/assets/` (kök, 9 dosya) bu sistemle ilgisiz eski derleme → SİL-ADAYI.

---

## 7. `.env` yol/ayar değişkenleri (yalnız isimler)

Cihaz `meds/.env` içinde yol/yerleşim değişkenleri: `MEDS_DATABASE_DIR`, `MEDS_TEMP_DIR`, `MEDS_DOWNLOADS_DIR`, `MEDS_DEEPSEEK_DIR` (boş), `MEDS_TRANSCRIPTIONS_DIR` (boş), `GOOGLE_APPLICATION_CREDENTIALS`, `GOOGLE_SERVICE_ACCOUNT_FILE`, `MEDS_EMBED_URL`; çalışma kipi: `MEDS_DISABLE_GPU`, `CUDA_VISIBLE_DEVICES`, `OLLAMA_NUM_GPU`, `MEDS_OPERATION_MODE`, `MEDS_LLM_BACKEND`, `MEDS_FREE_ONLY`, `MEDS_CMD_MODELS`, `MEDS_CMD_ONLY`, `MEDS_VECTOR_SEARCH`, `MEDS_VECTOR_TIMEOUT_MS`, `MEDS_VECTOR_WEIGHT`.
Ünitelerde ek: `MEDS_CORE_DIR` (4 ünitede `Environment=`).
Kodda env'siz sabit yol: `geminiV3DataService.ts` (`MEDS_DATABASE_V3_EXPORT`, `MEDS_GEMINI_V3_METADATA_DIR` varsayılanları `/home/indu/...`), `server.ts:2677` (`../meds_database_v2/phase14_past_question_editor`), `server.ts:5493` (`../meds_export`), `localRagEngine.ts:1149` (`../meds_database_v2/tibbi_terimler_sozlugu`). Cihaz `.env`'de `LOCAL_SUPABASE_*` adı yok (Oracle `.env`'de var).

---

## 8. Özet — öneri başına geri kazanılabilir alan

| Öneri | Kalemler | Yaklaşık boyut |
|---|---|---|
| **SİL-ADAYI (kanıtı güçlü)** | `dist/assets` bayat parçalar (prune betiğiyle) 1085M · `src/data/pastQuestions.json.bak_manual_import` (data/ kopyasıyla aynı) 61M · kök `scripts/` içindeki meds kopyası 53 .py + 29 klasör 19M · `meds/assets/` 4.1M · `get-pip.py` 2.2M · `scripts/__pycache__` ×2 + `meds/__pycache__` ~1.9M · `test_*.pptx`, `monitor.py.bak`, `scripts/test_*.py`, `sample_slide.json`, `test_json_write.json`, boş `build_k1_50..53_data`/`curriculum_generators` <0.2M | **≈ 1.17 G** |
| **SİL-ADAYI (?) — kullanıcı kararı** | `.venv_train` 5.4G · `dist-gh` 434M · `meds/.venv` 71M · `rag-project` 25M · `bun.lock` · `.commandcode` | **≈ 5.9 G** |
| **TAŞI** (→ `/home/indu/medsor-yedek/`, `~/.ssh/`) | `yedek/` 1.2G · `meds_temp/supabase_local.dump` 330M · `meds/data` yedekleri 139M · `meds_database/backups` 72M · `meds_database_v2/phase14_backup` 68M · `meds_temp/ozet_satir_yedek` 32M · `.env.cloud.bak` · `ssh-key1.*` · systemd `eski_yol_yedek/` · kök `NOTEBOOKLM_TALIMAT_REHBERI.md`/`FAZ15_TANITIMI.md` → `meds/docs/` | **≈ 1.84 G** (proje ağacından çıkar) |
| **ARŞİVLE (kanıtı güçlü)** | kök `scripts/` benzersiz kısmı ~21M · kök `packages/` 9M · kök `src/` 0.8M · kök `patch_/fix_/apply_/update_*.py` · `meds/data` rapor/eskimiş not dosyaları (`lecture_notes_supabase` 24M, `lecture_notes_2026_2027` 2.5M, raporlar, `extracted_lectures`) ~28M · `meds_temp` tek seferlik artıklar 3.7M · `meds/scripts` deste-49 kalabalığı + `build_k1_48/49_data` + `data_decks`/`ileri_tumor_genetigi`/`tumor_immuno_builder` ~2.2M · Windows `.bat/.vbs` · `transcribe_medical_audio.py` · `v2/soru_uretici_k1*.py` · `src/data/learning_*` | **≈ 87 M** |
| **ARŞİVLE (?) — kullanıcı kararı** | `models/` 322M · `src/data/lecture_notes.json` 32M · `meds/scripts/k1_decks` 22M · `training_data` 16M · `meds_database/derived/phase8` 16M · `src/data/study_questions` 2.2M · `docker-compose*.yml`/`Dockerfile`/`docker/` · `PROJECT_INSTRUCTIONS.md`/`PRODUCT.md`/`GEMINI.md`/`INTERAKTIF_OGRENME_REHBERI.md` (T8) · eski 10-04 betikleri | **≈ 410 M** |
| **Tekilleştirme fırsatı (silme değil)** | `meds_database/meds_sorular` ↔ `meds_downloads` 324M (hardlink/symlink) · `src/data/pastQuestions.json` 72M + `lectureSummariesCatalog`/`notebooklm_contributions` src kopyaları 16M (çift yazımı kaldır) | **≈ 412 M** |

Kesin + taşıma toplamı (proje ağacından çıkan): **≈ 3.1 G**; kullanıcı onayıyla **+≈ 6.3 G** daha.

---

## 9. Kullanıcı kararı gereken belirsiz kalemler

1. **`.venv_train` (5.4 G) + `models/medsoru-d3-qlora` (322 M) + `training_data` + `scripts/training`** — LoRA eğitimi tekrar yapılacak mı? Model Ollama'da servis edilmiyor.
2. **`dist-gh` (434 M)** — GitHub Pages yedek sitesi hâlâ isteniyor mu? (Yeniden üretilebilir.)
3. **Kök `packages/` (k1-30…42)** — `meds/src/data/decks/packages/` yalnız k1-01…29 içeriyor; paketler mevcut desteden yeniden üretilsin mi, yoksa kök eski kopyalar arşive mi? (AGENTS.md kural 5 paket senkronunu şart koşuyor.)
4. **Kök `scripts/` benzersiz 103 betik + `meds/scripts/k1_decks`, `deck_generators`** — deste yeniden üretim izi olarak arşivde mi tutulacak; paralel oturum hâlâ `deck_generators` ile üretim yapıyor mu?
5. **`src/data/pastQuestions.json` çift yazımı** (server.ts:1791) ve `src/data/lecture_notes.json` (32 M, yalnız yedek yol) — kaldırılması kod değişikliği ister (F/T4 fazı).
6. **`meds-gpuguard`, `meds-phases`, `meds-watchdog`, `meds-pipeline`** — GPU mevcut ama `.env` kapatmış; `meds-phases` "elle kip"te boşta. Bu dört servis kalsın mı / `Condition` ile mi kısılsın? `meds-watchdog` olmayan `meds-ollama` konteynerini denetliyor.
7. **:8094 bge-m3 embed süreci** ünitesiz — kalıcı ünite yazılsın mı? (Yazmak servis değişikliği → onay.)
8. **`meds-local-sync` (disabled) ve `meds-faz14-ucretsiz.timer` (disabled)** — tamamen kaldırılsın mı?
9. **`meds_database_v2/faz14_kurtarilan_sorular` (19 M) ve `phase15_quality_audit` (35 M)** — Faz 14/15 tamamlandıysa arşive.
10. **Yönetim panelindeki "Betikler" listesi** (Windows/Firebase dönemi ~30 betik) — panelden çıkarılıp arşivlensin mi?
11. **`rag-project/`, `meds/.venv`, `.commandcode/`** — bugün/son günlerde oluşmuş; hangi oturum/araç kullanıyor?
12. **Belge birleştirme (T8)** — `GEMINI.md` ve `INTERAKTIF_OGRENME_REHBERI.md` AGENTS.md ile çelişiyor (adım/kelime/öge yoğunluğu); `meds/AGENTS.md` ve `PROJECT_INSTRUCTIONS.md` "tamamen yerel GPU" diyor, `PROJE_TANITIMI.md` "yerel GPU çalıştırılmaz" diyor. Hangisi esas?
13. **E7** — Oracle'da `meds_database_v3_export` ve `meds_export` bağlı değil; Gemini v3 verisi ve NotebookLM indirme ucu Oracle'da gerekli mi?
14. **`.agents/.claude/.github` içindeki 3 farklı `impeccable` skill sürümü** (her biri 20 M) — tek kopya mı kalsın?
