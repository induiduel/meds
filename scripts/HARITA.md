# `meds/scripts/` Haritası — hangi iş nerede (2026-11-16 yeniden yapılandırma)

> Modelin doğru betiği **tek okumada** bulması için. Önce bu dosyayı oku; klasörleri gezme.
> Eski yol → yeni yol tam listesi: `deploy/oracle/tasinan_yollar.txt` (eski belge/hafıza notlarındaki yolları buradan çevir).

## Düzen
```
scripts/
├── kok.py          konum-bağımsız kök: SCRIPTS / MEDS / PROJE (yeni betikler parents[N] KULLANMAZ — aşağıya bak)
├── HARITA.md       bu dosya
├── kapilar/        tek kapı girişi: kos.py + matris.json (aşama → kapı komutu)
│                   yapi_koruma.py = yeniden yapılanma koruması (deste deposu, parents[N], taşınan yollar, hata dizini, src/data yazımı, yeni kök dizin; pre-commit `.githooks/pre-commit`)
├── hat/            içerik hattının orkestrasyonu
├── uretim/         içerik üretimi (ders, soru, ses, çizim, önem, çözücü ...)
├── altyapi/        servis, dağıtım, derleme, veri hattı, arama
├── moduller/       site özelliklerinin araçları (soru havuzu, composer, sözlük, hastalık, sağlık, ölçüm)
├── arsiv/          ÖLÜ kod — hiçbir şey çağırmaz; tsc ve Oracle gönderiminden dışlı. Yeni iş BURAYA BAĞLANMAZ.
└── *.py / *.mjs    kök kütüphaneler ve tek dosyalık araçlar (sik_aciklama, turkce_uslup, validate_learning_decks,
                    ders_icerik_*, build_* ...). Çok sayıda betik bunları adıyla import eder.
                    `deste_deposu.py` = Öğren destelerinin TEK okuma/yazma noktası (sunucu eşi src/services/desteDeposu.ts);
                    interactive_learning_decks.json'ı doğrudan açmak YASAK.
```

## hat/ — orkestrasyon (tam hat tek giriş: `hat/tam_hat/kosucu.py`)
- `tam_hat/` — **içerik üretiminin tek hattı** (`mod.py` katmanlar, `baglam.py` read-once, `hazirlik.py`, `ders_kilit.py`, `manifest.py` ders başına katman manifesti → `ders_bilgi/<key>/katman_manifest.json`, `hoca_kirp.py` döküm kırpma, `iskelet.py` çıktı iskeleti). Önce burası.
- `takvim/` (aktif kurul) · `dersler/` (ders kayıt defteri) · `onem/` · `oncelikli_dersler/` · `olasi_soru/` (gece.sh) ·
  `paket/` (.medspak) · `quiz_motoru/` (quiz KAPALI, kural 19)

## uretim/ — içerik üretimi
- Ders: `ders_isci/` (yayinla.py, denetle.py) · `sesli_anlatim/` (EMA/XTTS işçisi, cümle/kelime zamanı, pdf_isaret, terim) ·
  `ders_analizi/` · `ders_icerik/` · `ders_video/` · `ogren_ses/` · `ek_modul/`
- Ses ortak: `ses_ortak/` (`ses_kapisi.py`: ses kalite kapısı + kayıt↔disk↔Oracle boyut denetimi + artık raporu; CPU, salt okunur)
- Görsel: `cizim/` (cizim_kapisi, TALIMAT_CIZIM) · `kroki/` · `ara_resim/` · `lottie/` · `kmb/`
- Soru/çözücü: `spot_cozucu/` (ses.py, onem_dogrula, cozucu_dogrula) · `patoloji_cozucu/` (cozucu_ses_gpu.sh) ·
  `ses_ortak/` (EMA okunuş tek girişi `ses_metin.hazirla` + klip çekirdeği `ses_klip` + `okunus_farki.py` raporu + `sinama_okunus.py` okunuş sınaması, 0 HATA) ·
  `patoloji_cozucu_alt/` · `patoloji_soru_isci/` · `patoloji_onem/` · `patoloji_checkup/` · `sinav_spotlari/` · `cikmis_paket/`
- Hoca/öğrenci: `hoca_profili/` · `hoca_ara_soru/` · `hoca_vurgu/` · `ogrenci_onem/` · `ogrenci_drive/`
- Kamp/tekrar: `son_prova/` · `blok_ozet/` · `kamp/` · `tekrar_analizi/`
- Çıkmış: `cikmis_dizin/` · `cikmis_2627/` · Arşiv dersleri: `arsiv_25_26/` (adı arşiv ama CANLI üretim)
- Hastalık: `akbc_disease_pipeline.py` (AKBC hastalık profili hattı)
- Konu özel: `ileri_tumor_genetigi/` · `tumor_immuno_builder/` · `arzu/` (özel katman; sürüm notunda anılmaz)

- `asistan/` (kök altında) — sınav asistanı kaynak toplayıcı (`kaynaklar.py`); desteleri `deste_deposu` ile okur.

## altyapi/ — servis, dağıtım, veri
- Servisler (systemd): `agents/` (embed_server, gpu_guard, watchdog, pipeline_runner) · `v2/` + `semantic/` (**paket**:
  `cd scripts/altyapi && python -m v2 …` / `-m semantic.server`; birimlerde `WorkingDirectory=…/scripts/altyapi`) ·
  `opendesign/` (köprü kaynağı; çalışan kopya `~/.local/bin`, kur.sh) · `yedek/`
- Veri/arama: `pipeline/` (Drive → downloads → temp → database) · `advanced_ai/` (rag_vektor_hatti.py …) · `search/` · `db/` · `db_analiz/`
- Derleme/sınama: `vite/` (splitLearningDecks, surumDosyasi — vite.config.ts buradan import eder) · `design/` (kontrast kapısı) ·
  `perf/` · `cevrimdisi_sinama/` · `v15/` · `fixtures/` · `artifact_studio/` · `claude_eklenti/`
- Sağlık/bütçe: `saglik_raporu.py [--canli] [--json] | egilim` tek sağlık raporu · bütçe kapısı `kapilar/butce.py` (+ `butce.json`, tavan yalnız azalır)
- Tek dosyalık: `gpu_recovery.sh` (GPU kurtarma) · `rag-yeniden-parcala.mts` (RAG yeniden parçalama)
- Belgeler: `belge_haritasi.py` → `docs/HARITA.md` (belge eklenince yeniden çalıştır) · `betik_haritasi.py` → bu dosyanın kök bölümü
- **Yönlendirme:** `nereye.py "<görev>"` (katalog `docs/yonlendirme.json`, `--denetle` D8'de) · `bag.py kim|ne|etki|yetim <yol>`
  (içe aktarma + veri + çağrı bağları; önbellek `~/.cache/meds/bag.json`, artımlı)
- **Veri sorgusu:** `veri.py ders|bul|al|liste|say|kur|--denetle` (çıkmış/deste/örnek/sözlük/ansiklopedi/hastalık/özet/not/anlatım; FTS5 önbelleği `~/.cache/meds/veri.sqlite`, artımlı)
- **Veri bakımı:** `veri_bakim.py rapor|arsivle [--uygula]|geri <yol>|denetle` (yedek kalıntısı → `_arsiv_veri/` zstd, sha256 doğrulamalı; D10) · günlük `scripts/gunluk.py son|ozet`

## moduller/ — site özellik araçları
`recall/` (soru havuzu motoru) · `composer/` · `sozluk_v2/` · `diseases/` · `saglik/` · `eval/` (`npm run eval:*`)

<!-- kok-dosyalar:bas -->
## Kök dosyalar (81) — otomatik: `python3 scripts/altyapi/betik_haritasi.py`

**Kapılar / doğrulayıcılar** (10)
- `audit-and-disconnect-faulty-slides.mjs` — MeDSor Slayt İlişkisi Denetim ve Hatalı İlişkileri Kesme Scripti (Script 1)
- `ders_icerik_dogrula.py` — Ders içerik paketi kapısı: python3 scripts/ders_icerik_dogrula.py <key> ... → 0 HATA ol…
- `detect-faulty-ocr.mjs` — data/pastQuestions.json'da bozuk OCR'lı soruları listeler
- `run-verify-answers.bat` — Windows: soru/cevap doğrulama motorunu çalıştırır (eski)
- `self-healing-auditor.mjs` — MeDSor Otonom Kendi Kendini Denetleyen ve İyileştiren Sistem (Self-Healing Auditor)
- `sik_aciklama.py` — Şık açıklama kalite kapısı — meds/docs/SIK_ACIKLAMA_STANDARDI.md (kullanıcı kararı 2026…
- `start-answer-verifier-daemon.bat` — Windows: soru izleyici + doğrulama servisini başlatır (eski)
- `turkce_uslup.py` — Türkçe üslup kapısı — meds/docs/TURKCE_USLUP_STANDARDI.md (kullanıcı kararı 2026-10-18).
- `validate_learning_decks.py` — Öğren destelerini docs/OGREN_ETKILESIM_REHBERI.md kurallarına göre denetler.
- `verify-question-answers.mjs` — MeDSor Çıkmış Soru ve Cevap Doğrulama Motoru (scripts/verify-question-answers.mjs)

**Deste / ders içeriği** (16)
- `build_deck_packages.py` — Öğren destelerinin dışa aktarım paketlerini TEK kaynaktan üretir.
- `build_deck_pdf_sources.py` — Öğren desteleri → Drive'daki ders PDF'leri ve slayt → (PDF, sayfa) eşlemesi; İÇERİKLE D…
- `build_deck_schedule.py` — Ders programı sırası → src/data/deckSchedule.json (Öğren kitaplığı "Ders programı" sıra…
- `build_kazanim_deck_index.py` — Öğren desteleri için deste → kazanımlar dizini üretir (src/data/kazanimlar/byDeck.json).
- `build_learning_decks.py` — *- coding: utf-8 -*
- `ders_icerik_adim.py` — Ders içerik paketindeki her kayda `adim` (ait olduğu Öğren slayt numarası) anahtarını y…
- `ders_icerik_kaynak.py` — Ders içerik paketinde PDF sayfası (`s`) olmayan terim/kısaltma/bilgi kayıtlarına kaynak…
- `ders_icerik_uret.py` — Ders içerik paketi üretici: yayındaki kaynaklardan (deste, bilgi havuzu, terim/kısaltma…
- `ders_pdf.mts` — Ders PDF'i (yapay zekasız, limitsiz): python scripts/ders_icerik_adim.py ile `adim` yaz…
- `deste_bol.py` — Öğren deste monoliti ↔ deste-başına-dosya dönüştürücü (VERI_MODELI Faz 3 iskelesi).
- `deste_deposu.py` — Öğren desteleri için TEK okuma/yazma noktası (Python tarafı).
- `extract_curriculum.py` — müfredat PDF'inden Dönem 3 müfredat listesini çıkarır (eski, Windows yolu)
- `generate_medical_glossary.py` — *- coding: utf-8 -*
- `icerik_katman.py` — Canlı içerik katmanı (data/content) araçları — kayıt düzeyinde fark biçimi (bkz. src/se…
- `sinav_calisma_bol.py` — Sınav Çalışması verisini sayfanın yükleyebileceği küçük parçalara böler.
- `sinav_calisma_olustur.py` — Sınav Çalışma Veri Katmanı ve Kazanım Eşleştirici v2

**Derleme / dağıtım** (6)
- `build-database-json.mjs` — MeDSor Veritabanı JSON Üretim ve Senkronizasyon Motoru
- `build_android_apk.sh` — Android APK derlemesi (Capacitor, Android SDK)
- `prepare-android-dist.mjs` — dist/ içindeki yalnızca GÜNCEL derlemeye ait (reachable) JS/CSS parçalarını ve temel st…
- `prune-dist.mjs` — dist/assets birikimini temizler (vite emptyOutDir:false → her derleme yeni hash'li parç…
- `surum_gunlugu.py` — Güncelleme ve geliştirme günlüğü üretici → src/data/surum_gunlugu.json (/guncellemeler …
- `surum_gunlugu_turler.json` — sürüm günlüğü değişiklik türleri (surum_gunlugu.py girdisi)

**Senkron / Drive / bulut** (17)
- `auto-git-sync.mjs` — proje değişikliklerini otomatik git commit/push ile eşitler (eski)
- `crawl-all-drive-folders.mjs` — Drive çıkmış/dönem klasörlerini tarayıp dosya listesini çıkarır
- `download-all-slides.mjs` — Drive'daki ders slaytlarını toplu indirir
- `enrich-drive-slides.mjs` — driveAutomation.ts slayt kataloğuna şablon sayfa içeriği ekler (eski)
- `local-drive-sync-agent.mjs` — MeDSor Yerel Bilgisayar Arka Plan Otomasyon İşleyicisi (Local Sync Worker)
- `meds-local-sync.mjs` — MeDSor Yerel Otomasyon ve Senkronizasyon Motoru (meds-local-sync.mjs)
- `orchestrate_drive_curriculum_ai.mjs` — MeDSor AI Drive Curriculum Orchestrator & Interactive Deck Generator
- `sync-all-to-supabase.mjs` — Veritabanı senkronizasyon motoru
- `sync-database-json-to-cloud.mjs` — C:\Users\indui\Desktop\meds_database\database_json altındaki yapılandırılmış JSON dosya…
- `sync-drive-updates.mjs` — MeDSor Google Drive Değişiklik Tespit ve Manuel Senkronizasyon Motoru
- `sync-past-questions-to-supabase.mjs` — pastQuestions.json dosyasındaki 2922 adet çıkmış soruyu
- `sync_deepseek_data.py` — *- coding: utf-8 -*
- `sync_to_supabase_v2.py` — MeDSor AI - Supabase v2 Chunk-Build Veri Senkronizasyonu Motoru
- `sync_user_drive_folder.mjs` — öğrenci Drive klasörünü özyineli tarar
- `test-drive-folders.mjs` — Drive klasör kimliklerine erişimi sınar
- `transcribe-drive-audio.mjs` — MeDSor Tıbbi Amfi Ses Kayıtları Transkripsiyon, Ders Eşleştirme ve İzleme Motoru
- `update-drive-catalog.mjs` — data/real_drive_slides.json'dan Drive slayt kataloğunu üretir

**Veri düzeltme / eşleme** (17)
- `deep-ai-redactor.mjs` — MeDSor Derin Tıbbi Yapay Zeka Redaksiyon Motoru (scripts/deep-ai-redactor.mjs)
- `deep-triple-slide-matcher.mjs` — MeDSor Derinlemesine 3 Aşamalı Slayt ve Soru Eşleştirme Motoru
- `detect-database-updates.mjs` — Veritabanında Soru Bazında Güncelleme Tespit ve Ekonomik Artımlı Senkronizasyon Scripti
- `extract-scanned-images.py` — MeDSor Scanned PDF Image Extractor
- `filter-donem3-and-clean-ocr.mjs` — 1. Dönem 3 müfredatına (Tıbbi Patoloji, Farmakoloji, Dahiliye, Kardiyoloji, Pediatri,
- `fix-nested-and-embedded-questions.mjs` — MeDSor İç İçe Geçmiş Şıklar, Soru Kökünde Kalan Şıklar ve
- `fix-question-typos.mjs` — MeDSor Soru Yazım Hatalarını ve Bozuk OCR İfadelerini Tespit ve Düzeltme Motoru
- `index-rag-knowledge.mjs` — MeDSor RAG Knowledge Indexer & Embedder
- `inspect-sources.mjs` — çıkmış sorularını kaynak dosyaya göre sayar (inceleme)
- `link-exam-questions.mts` — Link past-exam files to the existing question pool and course material (retrieval only,…
- `manage-slide-relations.mjs` — MeDSor Çıkmış Soru & Amfi Slayt İlişki Yönetim Motoru (Master Runner)
- `match-and-link-lecture-slides.mjs` — MeDSor Slayt Eşleştirme, Bağlama ve Vurgulama Scripti (Script 2)
- `merge-same-exam-duplicates.mjs` — Eşleşen sorular birbirini tekrar eden sorular veya birbirine aşırı benzeyen
- `migrate-separate-current-and-past.mjs` — Veritabanı Ayrıştırma ve Düzenleme Motoru
- `process-local-sorular.mjs` — C:\Users\indui\Desktop\meds_database\local_sorular klasöründeki
- `rebuild-all-past-questions.mjs` — meds_sorular_txt'ten tüm çıkmış soru verisini yeniden kurar
- `slide-matching-utils.mjs` — MeDSor Slayt Eşleştirme ve Denetim Yardımcı Modülü

**Diğer** (15)
- `automation-runner.mjs` — MeDSor Central Script & Automation Runner Engine
- `deck_pdf_slide_duzeltme.json` — deste ↔ PDF slayt eşleme düzeltmeleri (build_deck_pdf_sources girdisi)
- `fast_hybrid_server.py` — MeDSor Low-Latency Hybrid Serving API — FastAPI + DuckDB (cursor-per-request).
- `gunluk.py` — Ortak betik günlüğü (yalnız stdlib; asla istisna fırlatmaz).
- `kok.py` — konum-bağımsız kök yolları: SCRIPTS / MEDS / PROJE
- `manage-service.ps1` — Windows: otomasyon servisini kur/başlat/durdur/durum (eski)
- `manage-service.sh` — manage-service.ps1'in Linux karşılığı.
- `master_controller.py` — MeDSor Master Orchestrator & Supervisor (scripts/master_controller.py)
- `monitor.py` — MeDSor Canlı Terminal Kokpiti ve Boru Hattı İzleyici (Terminal Dashboard v2)
- `rag_parca_deposu.py` — RAG parça deposu okuyucusu (Python eşi: src/services/ragParcaDeposu.ts).
- `scripts-meta.json` — betik üstverisi (eski otomasyon panelinin listesi)
- `show-notification.ps1` — Windows: masaüstü bildirimi gösterir (eski)
- `sinama_deste_parcali.py` — Deste deposu parçalı arka uç sınaması (VERI_MODELI Faz 3). Monolite DOKUNMAZ: geçici ko…
- `test-filter-donem3.mjs` — Dönem 3 müfredat süzgecini çıkmış sorularda sınar
- `test-sample-pdfs.mjs` — örnek Drive PDF'lerini indirip okumayı sınar

<!-- kok-dosyalar:son -->

## Çalışma verisi kod değildir
Bir betiğin üretim/ara verisi `meds_temp/<modül>/` altında yaşar (ör. `meds_temp/son_prova/`, `meds_temp/blok_ozet/`,
`meds_temp/tekrar_analizi/`); kod yalnız burada (git). Veri klasörünü ortam değişkeniyle değiştirilebilir yap
(`SON_PROVA_KOK`, `BLOK_OZET_KOK`, `TEKRAR_KOK`). Kodu meds_temp'e kopyalayıp oradan çalıştırma (çift kopya yasak).

## Yeni betik eklerken (ZORUNLU)
1. Doğru grubu seç (yukarıdaki tablo); tek seferlik deneme/göç ise doğrudan `arsiv/`'e değil, işi bitince arsiv'e taşı.
2. Kök yolu **asla** `Path(__file__).parents[N]` ile hesaplama; `kok.py` kullan:
   ```python
   import sys as _sys
   from pathlib import Path as _Path
   _d = _Path(__file__).resolve().parent
   while not (_d / "kok.py").exists() and _d != _d.parent:
       _d = _d.parent
   if str(_d) not in _sys.path:
       _sys.path.append(str(_d))
   import kok as _kok  # _kok.MEDS, _kok.SCRIPTS, _kok.PROJE
   ```
3. Kardeş modüle yol: `_kok.SCRIPTS / "uretim" / "kroki"` (grup segmenti dahil). Modülün kendi dosyaları: `Path(__file__).parent`.
4. Bu haritaya bir satır ekle. Taşıdığın/yeniden adlandırdığın her yolu `deploy/oracle/tasinan_yollar.txt`'ye yaz
   (Oracle'daki eski kopya dağıtımda arşive alınır).
5. Yol süpürmesi yapacaksan sed `[a-z]` aralığı Türkçe yerelde "i"yi atlar (H577) → Python ya da `LC_ALL=C`.
