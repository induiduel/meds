# Proje Taşıma ve Yeniden Düzenleme Yol Haritası

Durum: **taslak, onay bekliyor.** Bu belgedeki hiçbir adım uygulanmadı.
Hazırlanma: 2026-10-07. Kaynak: canlı sistemin taranması (servisler, yollar, klasör boyutları, kod referansları).

## 0. Karar bekleyen sorular

1. **Hedef yol:** Proje nereye taşınacak? Bu belgede `$YENI` olarak geçer. Öneri: boşluk ve Türkçe karakter içermeyen bir yol, ör. `/home/indu/medsoru`.
   Bugünkü yolda boşluk (`MedSoru Project`) ve `ü` (`Masaüstü`) var: birçok betikte ve systemd'de tırnaklama hatası, `.env` okuma sorunu ve Claude bellek klasörü adının bozulması (`Masa-st-`) buradan geliyor.
2. **Silinecekler:** Bölüm 4'teki "silinebilir" listesi onaylanınca silinir; önce yedek diske kopyalanır.
3. **Git geçmişi:** `data/users.json` (8 öğrencinin e-posta ve öğrenci numarası) 11 commit'te herkese açık repoda. Geçmişten temizlemek (git filter-repo + zorla push) geri alınamaz; ayrı onay gerekir.

## 1. Bugünkü durum (ölçülen)

| Yer | Boyut | Ne | Kod kullanıyor mu |
|---|---|---|---|
| `meds/` (git repo) | 14 GB | site, sunucu, betikler | — |
| ├ `.venv-ocr/` | 6,7 GB | asıl Python ortamı (servisler bunu kullanır) | evet |
| ├ `.venv_train/` | 5,4 GB | LoRA eğitimi ortamı | 1 betik |
| ├ `.venv/` | 60 MB | eski ortam | 1 referans |
| ├ `models/` | 322 MB | eğitilmiş LoRA (medsoru-d3-qlora) | 10 dosya |
| ├ `node_modules/`, `dist/` | 620 MB | yeniden üretilebilir | — |
| ├ `data/` | 290 MB | site JSON veritabanı (git'te) | evet |
| ├ `supabase-server/` | 70 MB | yerel Supabase araçları | 12 dosya |
| ├ `meds/meds_temp/` | 0,8 MB | **yanlış yerde** (asıl `../meds_temp`) | hayır |
| ├ `scripts/` | 231 betik | çoğu tek seferlik deste/özet üreticileri | karışık |
| `meds_database/` | 391 MB | temiz veritabanı + `derived/` faz çıktıları | evet (`MEDS_DATABASE_DIR`) |
| `meds_database_v2/` | 27 MB | faz 6–14 çıktıları, sözlük, ICD | 31 dosya (göreli yol) |
| `meds_temp/` | 586 MB | ara veri, günlükler, durum dosyaları | evet (`MEDS_TEMP_DIR`) |
| `meds_downloads/` | 2,0 GB | Drive ham indirmeleri | evet |
| `med_data/` | 238 MB | eski bir proje kopyası (README, server.ts, src…) | **hayır** |
| `meds_database_backup_20261005/` | 124 MB | yedek | hayır |
| `meds_database_v2_backups/` | 3,8 MB | yedek | 1 referans |
| `meds_database_v3_export/` | 18 MB | dışa aktarım | 5 dosya |
| `meds_save_backup1.zip` | 407 MB | yedek | hayır |
| `yedekler/` | 265 MB | 2026-10-06 yedeği (`.env` içerir) | hayır |
| `dashboard_server.py` (kök) | — | `meds/dashboard_server.py` ile birebir aynı kopya | servis artık repo kopyasını çalıştırıyor |
| `watch_pipeline.py` (kök) | — | eski izleyici | 1 referans |

**Yola bağlı parçalar (taşımada kırılacaklar):**

- 8 systemd kullanıcı servisi (`~/.config/systemd/user/meds-*.service`): `ExecStart`, `WorkingDirectory`, `EnvironmentFile` mutlak yol içerir.
- 45 kaynak dosyada mutlak yol (`/home/indu/...`): `server.ts`, `dashboard_server.py`, `watchdog.py`, ~35 tek seferlik betik, `CLAUDE.md`, `AGENTS.md`.
- `.env`: `MEDS_DATABASE_DIR`, `MEDS_TEMP_DIR`, `MEDS_DOWNLOADS_DIR`, `MEDS_DEEPSEEK_DIR`, `MEDS_TRANSCRIPTIONS_DIR`, `GOOGLE_SERVICE_ACCOUNT_FILE`.
- **Python sanal ortamları taşınamaz:** `bin/*` betiklerinin ilk satırı mutlak yol içerir (`exec ".../meds/.venv-ocr/bin/python3"`). Taşımadan sonra yeniden kurulmalı.
- Göreli varsayılanlar: birçok faz betiği `PROJECT/meds_database_v2`, `PROJECT/meds_temp` kullanır (repo klasörünün bir üstü). Kardeş klasör düzeni korunursa bunlar kendiliğinden çalışır.
- Claude Code proje belleği klasör adı yoldan türetilir (`~/.claude/projects/-home-indu-Masa-st--MedSoru-Project-meds/`). Yeni yolda yeni klasöre kopyalanmalı.

**Yoldan bağımsız olanlar:** Cloudflare tüneli (sistem servisi, token ile, porta yönlendirir), GitHub remote, Ollama, nvm/Node, Hugging Face önbelleği (`~/.cache`).

## 2. Hedef hiyerarşi

```
$YENI/                         (ör. /home/indu/medsoru)
├── app/                       git repo (bugünkü meds/) — yalnız kod ve küçük yapılandırma
│   ├── server.ts, src/, public/, index.html, vite.config.ts
│   ├── scripts/
│   │   ├── pipeline/          Drive → downloads → temp → database
│   │   ├── agents/            servis süreçleri (phase_cycle, watchdog, gpu_guard, lib)
│   │   ├── phases/            faz 5–14 (bugünkü advanced_ai/)
│   │   ├── eval/              retrieval-eval vb.
│   │   └── archive/           tek seferlik betikler (deste/özet üreticileri) — çalıştırılmaz
│   ├── tools/dashboard/       dashboard_server.py (tek kopya)
│   ├── data/                  site JSON (users.json git dışı)
│   ├── docs/
│   └── deploy/systemd/        servis dosyalarının şablonları (yol değişkenli)
├── veri/
│   ├── database/              bugünkü meds_database/
│   ├── database_v2/           bugünkü meds_database_v2/ (faz çıktıları)
│   ├── downloads/             bugünkü meds_downloads/
│   └── temp/                  bugünkü meds_temp/ (logs/, state/ içinde)
├── ortam/                     Python sanal ortamları (yeniden kurulur, git dışı)
│   ├── ocr/  train/
├── modeller/                  LoRA ve yerel model dosyaları
└── yedek/                     tüm yedekler, zip'ler, eski dışa aktarımlar (salt okunur)
```

İlke: **kod (app) ↔ veri (veri) ↔ çalışma ortamı (ortam) ↔ yedek** ayrı. Kod veriye yalnız `.env` ile ulaşır; göreli `../meds_*` varsayılanları tek bir yol modülünde toplanır.

## 3. Uygulama planı (aşamalı, her aşama sonunda doğrulama)

Her aşama tek başına geri alınabilir. Bir aşamanın doğrulaması geçmeden sonrakine geçilmez.

### Aşama A — Hazırlık (taşıma yok)

1. Tam yedek: `rsync -aHAX "MedSoru Project/" /yedek-disk/medsoru-ONCE/` (venv'ler hariç, ~3,5 GB). `.env` dahil; repoya girmez.
2. Bağımlılık kilitleri: `.venv-ocr/bin/pip freeze > app/deploy/requirements-ocr.lock`, aynısı `train` için. Node sürümü `.nvmrc`.
3. **Yol modülü:** `scripts/agents/paths.py` ve `src/services/paths.ts` — `MEDS_ROOT`, `MEDS_DATABASE_DIR`, `MEDS_TEMP_DIR`, `MEDS_V2_DIR`, `MEDS_DOWNLOADS_DIR`, `MEDS_MODELS_DIR` değerlerini `.env`'den okur, yoksa bugünkü kardeş düzeni varsayar. 45 mutlak yollu dosya bu modüle geçirilir (tek seferlik arşiv betikleri için yalnız uyarı yorumu).
4. Servis şablonları: `deploy/systemd/*.service.in` (`@ROOT@` yer tutucu) + `deploy/install-services.sh`.
5. Doğrulama: mevcut yerde her şey çalışır (aşağıdaki **Kontrol listesi**). Bu aşama yalnız kod değişikliğidir; git'e girer.

### Aşama B — Durdur ve taşı

1. Faz zincirinin turu bitince (ya da `aktif` boşken) servisleri durdur: `systemctl --user stop meds-phases meds-pipeline meds-downloads-watcher meds-watchdog meds-gpuguard meds-dashboard meds-web`.
2. `rsync -aHAX` ile yeni hiyerarşiye kopyala (taşıma değil; eski yer geri dönüş için kalır):
   `meds/` → `app/` (venv, node_modules, dist hariç), `meds_database/` → `veri/database/`, `meds_database_v2/` → `veri/database_v2/`, `meds_temp/` → `veri/temp/`, `meds_downloads/` → `veri/downloads/`, `meds/models/` → `modeller/`, yedekler → `yedek/`.
3. `.env` yollarını güncelle (`MEDS_ROOT=$YENI`, diğerleri `$YENI/veri/...`).
4. Ortamları yeniden kur: `python3 -m venv ortam/ocr && ortam/ocr/bin/pip install -r app/deploy/requirements-ocr.lock`; `npm ci` (app içinde); `npx vite build`.
5. Kopya sayımı doğrulaması: her klasör için dosya sayısı ve toplam boyut eski/yeni karşılaştırılır (`find | wc -l`, `du -sb`).

### Aşama C — Servisleri yeni yere bağla

1. `deploy/install-services.sh $YENI` → `~/.config/systemd/user/` altına yazar, `daemon-reload`.
2. Sırayla başlat ve her birinin durumunu kontrol et: gpuguard → web → dashboard → watchdog → pipeline → downloads-watcher → phases.
3. Claude belleğini yeni proje klasörüne kopyala.

### Aşama D — Doğrulama (kontrol listesi)

| Kontrol | Komut / yöntem | Beklenen |
|---|---|---|
| Tip denetimi | `npm run lint` | yalnız bilinen 2 hata (aiProvider) ya da 0 |
| Ön yüz derleme | `npx vite build` | başarılı |
| Site | `curl localhost:3000/api/past-exams` | 4551 soru (bugünkü sayı) |
| Faz verisi | `/api/questions/00a07e4dda4a/insights` | kurul 3, Mide Tümörleri, varlıklar |
| Öğren bağlantıları | `/api/learn-links` | 300 bağlantı |
| RAG | `npx tsx scripts/eval/retrieval-eval.mts` (+`STRIP=1`) | 93 / 89 / 40 (±1) |
| Ders notu temiz katmanı | `/api/lecture-notes/:id` | temiz metin, `?raw=1` özgün |
| Panel | `localhost:8085` | fazlar, kuyruk, GPU |
| Faz zinciri | `meds-phases` günlüğü | kaldığı adımdan sürer, `rc=0` |
| İndirme izleyici | yeni PDF bırak | OCR'dan geçer |
| Tünel | `https://nofrostlife.com.tr/test/cikmis` | açılır |
| GPU koruyucu | `meds_temp/state/gpu_guard.json` (yeni yerde) | güncel zaman |
| Mutlak eski yol | `grep -r "Masaüstü/MedSoru Project"` (app, .env, servisler) | 0 sonuç |

### Aşama E — Temizlik (yalnız D tamamen geçince, ayrı onayla)

1. Eski klasör 7 gün salt okunur bekletilir (`chmod -R a-w`), sonra yedek diske arşivlenip silinir.
2. Bölüm 4'teki silinecekler silinir.
3. Repo içi düzen (scripts/phases, scripts/archive, tools/dashboard) **ayrı commit'lerde** yapılır; her commit sonrası kontrol listesi.

### Geri dönüş

B/C aşamasında bir şey bozulursa: yeni servisleri durdur → eski servis dosyalarını geri yükle (`~/.config/systemd/user/*.bak`) → eski klasörde başlat. Eski yer, E aşamasına kadar dokunulmadan kalır.

## 4. Gürültü ve kirlilik: silinecek / arşivlenecekler (öneri)

**Silinebilir (yeniden üretilebilir ya da kopya):** `node_modules/`, `dist/`, `__pycache__/` (her yerde), `meds/meds_temp/` (yanlış yerde), kökteki `dashboard_server.py` (repo kopyası asıl), `.impeccable/hook.cache.json`, `test_shadow.pptx`, `test_table.pptx`, `.venv/` (`.venv-ocr` asıl ortam; tek referans güncellenir).

**Yedeğe taşınacak (kod kullanmıyor):** `med_data/` (eski proje kopyası), `meds_database_backup_20261005/`, `meds_save_backup1.zip`, `yedekler/`, `meds_database_v2_backups/`.

**Arşiv klasörüne (scripts/archive) taşınacak tek seferlik betikler:** `build_*_deck.py` (~25), `generate_*_deck.py`, `generate_kurul*_redakte_sorular.mjs`, `generate_kurul*_amfi_ozetleri.mjs`, `expand_*_terms.py`, `enrich_*` — her biri için "bir servis, zincir adımı, package.json betiği ya da AdminScriptsTab tarafından çağrılıyor mu" kontrol edilir; çağrılan taşınmaz.

**Kullanılmayan faz çıktıları:** Faz 7 hikâyeleri (`phase7_stories`), eski tıbbi sözlük (`medical_thesaurus`) — güvenilmez bulunmuştu; yedeğe.

**Veri hijyeni kuralları (kalıcı):**
- `data/users.json`, `.env`, `.claude/settings.local.json`, `.codex/` git dışı (`.gitignore`).
- Faz çıktıları yalnız `veri/database/derived/` ve `veri/database_v2/` altına; repo içine veri yazılmaz.
- Günlükler `veri/temp/logs/` altında, 30 günden eskiler sıkıştırılır.
- Yedekler yalnız `yedek/` altında, tarih adlı.

## 5. Riskler

| Risk | Önlem |
|---|---|
| Venv kopyalanıp çalışır sanılması | Kopyalanmaz; kilit dosyasından yeniden kurulur |
| Faz zinciri yarı adımda durması | Aşama B, zincir `aktif: null` iken başlar; zincir zaten kaldığı adımdan sürer |
| Göreli `../meds_*` varsayılanı yeni düzende yanlış klasörü göstermesi | Aşama A'daki yol modülü + `.env`; doğrulamada `grep` |
| Eski yolun gizli bir yerde kalması (cron, masaüstü kısayolu, IDE) | `grep -r` + `crontab -l` (bugün boş) + `~/.local/share/applications` |
| Disk alanı (kopya sırasında iki kat) | Gerekli boş alan: ~4 GB veri + ~13 GB yeniden kurulan ortam |
| Herkese açık repoya kişisel veri | `users.json` git dışı; geçmiş temizliği ayrı onayla |
