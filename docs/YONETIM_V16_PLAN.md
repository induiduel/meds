# Yönetim v16 Planı: baştan kurulum

> Durum: plan (2026-10-28). Kod değişmedi. Kaynak: `src/components/manage/*`, `src/components/v14/**`, `server.ts`,
> `src/services/*` içinde `/api/admin/*` uçları, `data/`, `src/data/`, `deploy/pg/sql/*.sql`, AGENTS.md kural 12/16/20.
> Tarayıcıyla canlı sınama yapılmadı. Değerlendirme koddan yapıldı; "çalışıyor mu" sütunu bu yüzden **kod okumasına dayalı** bir tahmin.

## 0. Özet

| | |
|---|---|
| Mevcut bölüm | 29 bölüm (`ManageConsole.SECTIONS`) + Genel bakış, 4 grupta (Genel, İçerik, Topluluk, Sistem) |
| Mevcut yönetim kodu | ~23.300 satır (`manage/` + `v14/`); en büyükleri DraftStudio 1876, ManageDataSection 1388, NotebookLM 1341, ManageConsole 1167 |
| Mevcut uç | 133 `/api/admin/*` yol+yöntem çifti (+ `/api/notebooklm/manage`, `/api/sesli-anlatim/yerel`, `/api/canli-ders/video-is`, `/api/system/services`) |
| Önerilen | **8 grup, 52 sayfa** (P0: 17, P1: 22, P2: 13) |
| Yeni uç | ~24 uç grubu (§5) |
| Kaldırılacak/birleşecek | 9 bölüm (§6) |

## 1. Mevcut durum envanteri

### 1.1 Kabuk ve iskelet

- **Giriş:** `App.tsx` → `ManageConsole` tek `React.lazy`. Konsolun içinde **29 bölüm statik import** ediliyor (yalnız 1 `lazy`).
  /manage açılınca bütün bölümlerin kodu iniyor. Hızlı açılmayı engelleyen birinci neden bu.
- **Kabuklar:** v12 (`ManageV12`), v14 (`ManageShellV14`, varsayılan) ve klasik `ms-*` (`manage-v9.css`), üçü birlikte duruyor.
  v14 yalnız düzen ve gezinmeden sorumlu, veri ve durum `ManageConsole`'da kalıyor (state çok büyük, her bölüm geçişinde yeniden çiziliyor).
- **Veri girişi:** `ManageConsole` `questions: QuestionItem[]` prop'u alıyor. Uygulama havuzu ve yorumlar/taslaklar/raporları istemcide
  bütünüyle tutuyor. Genel bakış sayaçları bu dizilerden hesaplanıyor.
- **Ortak bileşenler:** `consoleUi.tsx` (Drawer, ConsolePage…), `v14/pageKit.tsx` (Tabs14…), `v14/manageKit.tsx` (BulkBar, JsonView).
  Yeniden kullanılabilir durumdalar.
- **Adres:** `/manage/<slug>`; derin bağlantı yalnız `kisiler/<kişi>` için var.
- **Moderatör:** `MODERATOR_SECTIONS` + `moderatorAccess.ts` ile kısıtlı bölüm listesi.

### 1.2 Bölüm bölüm değerlendirme

| Bölüm (slug) | Bileşen | Ne yapar | Uç | Değerlendirme |
|---|---|---|---|---|
| bekleyen-islemler | ManagePendingOperationsSection (651) | auto-repair kuyruğu, geri alma | `/api/admin/auto-repair/*` (10) | Çalışıyor. Gemini onarım işçisi kural 20 gereği duraklatılmış başlıyor. Taşınacak (Sistem › İşler) |
| gelen-kutusu | ManageInboxSection (552) | bildirim/yorum/taslak tek kuyruk | `/api/admin/inbox`, notifications | Çalışıyor. Moderasyonla kesişiyor |
| moderasyon | ManageModerationSection (449) + moderationActions | soru şikâyetleri | `/api/admin/moderation/*`, reports/resolve | Çalışıyor, ancak yalnız soru şikâyetlerini kapsıyor. **Sohbet/topluluk mesajı moderasyonu yok** |
| soru-havuzu | ManagePoolV14 (404) | havuz düzenle/sil/içe aktar | `/api/admin/questions/:id` | Çalışıyor. Bütün havuz istemcide, sunucu sayfalaması yok |
| veri-katalogu | ManageCatalogSection (706) | 11 varlık türü (past, pool, decks, kazanım, örnek, sözlük, kart, hastalık, özet, geri bildirim, müzik, çöp) | `/api/admin/catalog/*` (8) | En sağlam altyapı: sunucuda süzme ve sayfalama, çöp kutusu, ilişkiler. v16'nın içerik sayfalarının omurgası olur |
| tum-veriler | ManageDataSection (1388) | tüm kümeler tek tabloda, CSV | istemci dizileri | Katalogla çakışıyor ve istemcide çalışıyor. **Kaldırılacak** |
| fazlar | ManagePhasesSection (612) | Faz 14/15 soru çıktıları | `/api/admin/phases/*` | Çalışıyor, uzman aracı. P2'de Sistem altına alınacak |
| sesli-anlatim | ManageSesliAnlatimSection (835) | metin, MP3, alternatif ses kuyruğu | `/api/sesli-anlatim/yerel/*` | Çalışıyor. "Yerel" uçları Oracle'da anlamsız olabilir, doğrulanmalı |
| yeni-dersler | ManageDersIsci* (1003+190+228+110) | ders işçisi paketleri, onay | dersIsciProxy, dersIsciEk | **Oracle işçisi 2026-10-27'de durduruldu** (kural 20). Bölüm büyük ölçüde boşta. Salt okunur arşiv + elle tetiklemeye indirilecek |
| kamp-tuyolari | ManageKampSection (267) | tüyo onay/red | `/api/admin/kamp/*` | Çalışıyor. Taşınacak |
| ham-havuz | ManageRawPoolSection (386) | append-only defter | `/api/admin/raw-pool/*` | Çalışıyor. Taşınacak. Silme düğmesi bilinçli olarak yok |
| birlesenler | ManageMergesSection (333) | kopya çıkmış birleştirme | `/api/admin/question-merges` | Çalışıyor. Taşınacak |
| veri-merkezi | ManageDataCoreSection (152) | "Core v2" | — | Sunucuda `/api/core` karşılığı bulunamadı. **Ölü sayılıyor, kaldırılacak** |
| notebooklm | ManageNotebookLMSection (1341) | NotebookLM içe aktarma | `/api/notebooklm/*` | Kullanımı düşük, ağır bir bölüm. P2 "Araçlar"a, lazy |
| serbest-girdiler | ManageIntakeSection (503) | serbest metin ayrıştırma | `/api/admin/question-intake/*` | Ayrıştırma LLM kullanıyor, kural 20 kilidine bağlı. Taşınacak |
| taslaklar / studyo | ManageDraftsSection (926), DraftStudio (1876) | taslak kümeleme ve eşleme | `/api/admin/drafts/merge` | Stüdyo en büyük dosya ve kullanımı belirsiz. Taslaklar kalır, **Stüdyo P2/lazy ya da kaldırılır** |
| puan-atp | ManageBasarim (293) | puan/ATP/kilit | `/api/admin/basarim/*` (6) | Çalışıyor. Taşınacak |
| kisiler | ManagePeopleSection (925) + PersonStudy | 360° kişi, cihaz, etkinlik | `/api/admin/people*` (12) | Çalışıyor, ancak `GET /api/admin/people` listeyi **sayfalamadan** döküyor (`buildList()`). Sayfalama gerekiyor |
| giris-gorev | ManageGorevTakip (152) | seri ve görev | `/api/admin/people/gorev-takip` | Çalışıyor |
| ders-ilerlemesi | ManageStudyProgress (258) | ders × öğrenci matrisi | `/api/admin/people/calisma-matris` | Çalışıyor. Matris büyüdükçe ağırlaşacak |
| kullanicilar | ManageUsersSection (775) + UserAccessControls | hesap, rol, SMTP | `/api/admin/users*`, people-access, smtp | Kişilerle büyük ölçüde örtüşüyor. Rol/askı Kişiler'e taşınacak, SMTP Site › Bildirimler'e |
| betikler | AdminScriptsTab | betik/zincir çalıştırma | `/api/admin/scripts/*` | Çalışıyor. LLM çağıran betikler kural 20 kilidine bağlı |
| sistem | ManageSystemSection (295) + ServiceControl | sağlık, servis, konsol günlüğü | `/api/admin/servis/*`, console-logs | Çalışıyor |
| otomasyon | ManageAutomationSection (328) | zamanlama, anahtarlar, Drive | manage-settings, drive/* | Zamanlayıcıların çoğu maskelendi (kural 20). "Zamanlama" sekmesi yanıltıcı. Salt durum + elle tetiklemeye indirilecek |
| hat | ManageHatSection (437) | hat.json aşamaları | `/api/admin/hat/*` (8) | Çalışıyor. `hat/gece/calistir` elle tetikleme olarak kalır |
| veritabani-gezgini | ManageDatabaseExplorer (506) | pg tablo/satır CRUD + salt okunur SQL | `/api/admin/pg/*` | Çalışıyor, sayfalı. Taşınacak |
| kisayollar | ManageShortcuts (175) | bağlantılar | — | Statik. Sistem › Bağlantılar |
| veritabani | ManageDatabaseV14 (368) | yedek, içe/dışa aktarım, `db/reset` | `/api/admin/db/*`, export-zip, backup-to-cloud | `db/reset` tehlikeli: çift onay ve denetim kaydı şart. "supabase/firebase" anahtar kelimeleri eski kalmış |

### 1.3 Yavaşlık kaynakları

1. Konsolda 29 statik import var. Rota bazlı `lazy` gerekiyor.
2. Havuz, yorumlar, taslaklar ve kullanıcılar istemcide bütünüyle tutuluyor (`questions` prop'u, `ManageDataSection`).
3. `GET /api/admin/people` sayfalamıyor. `calisma-matris` tam matris döndürüyor.
4. Katalog `pastQuestions.json` (96 MB) ve `interactive_learning_decks.json` (86 MB) dosyalarını sunucu belleğinde okuyor. Kabul edilebilir, ama her yazma tam dosya yazımı demek. Yazma kuyruğu ve tek yazıcı gerekiyor.
5. Genel bakış sayaçları istemci dizilerinden hesaplanıyor. Yerine tek bir `GET /api/admin/ozet` ucu konacak.

## 2. Yönetilebilir veri envanteri

Canlı katman notu: Oracle'da `src/data` geçicidir (dağıtımda ezilir). Panelden yazılan içerik **`data/content/`** katmanına
yazılır ve `SSE content_changed` yayınlanır (bugün yalnız `interactive_learning_decks`, `medical_glossary`, `question_cards` var).
v16'da içerik yazan her sayfa bu katmanı kullanır. Yeni varlık eklemek, `data/content/<varlık>.json` + `_ids.json` kaydı +
deploy [0b] geri çekme listesine ekleme demektir.

### 2.1 İçerik (dosya)

| Varlık | Kaynak | Boyut | Bugün yönetilebilir mi | v16 yazma yolu | Sayfalama |
|---|---|---|---|---|---|
| Çıkmış sorular | `data/pastQuestions.json` (+ `src/data` kopyası) | 96 MB | Katalog `past`, birleşenler | katalog ucu + `syncPastMergeSiblings` | sunucu, zorunlu |
| Soru havuzu | `data/questions.json` | küçük | ManagePoolV14 | katalog `pool` | sunucu |
| Örnek sorular | `src/data/ornek_sorular/k*/` | orta | Katalog `ornek` | data/content katmanı (yeni) | sunucu |
| Kazanımlar | `src/data/kazanimlar/k*.json` | orta | Katalog | data/content (yeni) | sunucu |
| Öğren desteleri | `src/data/interactive_learning_decks.json` | 86 MB | Katalog `decks` (data/content var) | var + `validate_learning_decks.py` kapısı | sunucu |
| Ders kayıt defteri | `src/data/dersler/kN.json`, `branslar.json` | küçük | **Yok** | yeni: `data/content/dersler/` | hayır |
| Kurul takvimi | `src/data/kurul_takvimi.json`, `kurulTakvimi.ts`, `scripts/takvim/aktif_kurul.py` | küçük | **Yok** | yeni: `data/content/kurul_takvimi.json` + SSE | hayır |
| Ders içerik paketleri | `src/data/ders_icerik/` | büyük | Yok (salt üretim) | salt okunur + yayın bayrağı | sunucu |
| Sesli ders | `src/data/sesli_anlatim/`, `data/sesli_anlatim/`, `data/ogren_ses` | büyük | ManageSesliAnlatim | mevcut + görünürlük bayrağı | sunucu |
| Önem/asistan/çözücü (branş) | `src/data/*_onem`, `*_asistan`, `*_cozucu`, `data/*_cozucu` | orta | **Yok** | yeni salt okunur + gizle | sunucu |
| Sınav spotları | `src/data/exam_spots_k1*.json` | orta | Yok | katalog bağdaştırıcısı | sunucu |
| Sözlük, kısaltma, terim | `medical_glossary.json` (4 MB), `kisaltma_sozluk.json`, `terim_yardimcisi_sozluk.json` | orta | Katalog `glossary` | var (data/content) | sunucu |
| Hastalıklar | `diseases.json` (6,8 MB), `disease_*.json` | orta | Katalog | data/content (yeni) | sunucu |
| Ders özetleri | `summaries_meta.json`, `summaries/` | orta | Katalog | mevcut | sunucu |
| Kartlar | `question_cards.json` | orta | Katalog | var | sunucu |
| Kamp / check-up / son prova | `data/kamp`, `src/data/genetik_kamp`, `patoloji_checkup`, `son_prova`, `kmb` | orta | Kamp tüyoları | salt okunur + yayın bayrağı | hayır |
| Sınav dağılımı | `src/data/sinav_dagilimi.json` | küçük | Yok | data/content (yeni) | hayır |
| Başarım tanımları | `src/data/basarim/tanim.json` | küçük | `PUT /api/admin/basarim/tanim` | mevcut | hayır |
| Oyun soru kaynakları | `src/services/quiz/oyunSoruKaynagi.ts` (çözücü setleri) | — | Yok | yeni: kaynak aç/kapa bayrağı | hayır |
| Müzik | `data/music_shared.json` | küçük | Katalog | mevcut | hayır |
| Güncelleme notu | `meds/guncelleme_notu.json`, `surum_gunlugu.json` | küçük | Yok (dağıtımla) | salt okunur (dağıtımın parçası, kural 13) | hayır |
| Ham soru defteri | `data/question_ledger` | büyük | ham-havuz | append-only, değişmez | sunucu |
| Havuz dondurma | `data/havuz_dondur.json` | küçük | Yok | yeni: salt okunur + kullanıcı onayıyla işlem | hayır |
| Geri bildirim | `learn_feedback.json`, `ornek_soru_bildirimleri.jsonl` | küçük | Katalog | mevcut | sunucu |

### 2.2 meds-pg tabloları (`deploy/pg/sql`)

| Dosya | Tablolar (özet) | Bugün | v16 sayfası |
|---|---|---|---|
| `user_data.sql` | user_data (kv) | DB gezgini (ham) | Kullanıcılar › Profil verisi (anahtar bazlı, biçimli) |
| `user_activity.sql` | user_events, cihaz/oturum | Kişiler | Kişiler + Etkinlik günlüğü |
| `topluluk.sql`, `topluluk_sohbet.sql` | topluluk_mesajlar, sohbet_odalari, üyeler | **Panel yok**, yalnız ham gezgin | Topluluk › Sohbetler, Mesajlar |
| `arkadaslik.sql` | arkadas_istek, arkadaşlık | Yok | Topluluk › Arkadaşlık |
| `not_paylas.sql` | paylasilan_notlar | Yok | Topluluk › Paylaşılan notlar |
| `learn_social.sql` | Öğren sosyal (beğeni/yorum) | Yok | Topluluk › Öğren yorumları |
| `realtime.sql` | NOTIFY tetikleyicileri | — | Sistem › Canlı olaylar |
| `rag_chunks_*.sql` | rag_chunks, işlevler | Yok | Sistem › RAG indeksi (salt durum) |

### 2.3 Site kabuğu ve ayarlar

| Ayar | Bugün nerede | Değişim yolu | v16 |
|---|---|---|---|
| GIZLI_SAYFALAR / KAPALI_SAYFALAR | `src/components/merkez/merkezModel.ts` (derleme sabiti) | kod + dağıtım | **Çalışma anında**: `data/content/site_ayar.json` → `/api/site-ayar` (genel) + SSE `site_ayar_changed`. Sabitler ilk değer olarak kalır |
| Menü | `shell/navModel.ts`, navV15, `siteHaritasi.ts` | kod | Salt görünüm + sayfa bazında gizle/aç (site_ayar). Menü yapısı kodda kalır (kural 16) |
| Bakım kipi | `bakimHataRoutes.ts`, `MEDS_BAKIM`, `POST /api/admin/bakim` (bellekte) | uç var, panel yok | Site › Bakım. Kalıcılık için bellekteki durum site_ayar'a yazılmalı |
| Özellik bayrakları | dağınık (`manage_settings.json`, env) | `manage-settings` | Site › Özellik bayrakları (tek şema) |
| Duyuru / bildirim | `send-notification`, push, `admin_notifications.json` | uç var | Site › Duyurular + Bildirim gönder |
| SMTP / WhatsApp | `smtp-config`, `/api/whatsapp/*` | Kullanıcılar içinde | Site › Kanallar |
| İçerik görünürlüğü (kurul/ders/soru) | yok (kurul takvimi + `KAPALI_SAYFALAR`) | — | **Yeni** `gorunurluk` haritası: `{kurul, ders, varlık, id} → acik/gizli/yalniz-yonetici` |

### 2.4 LLM kuyrukları (kural 20)

Faz14 kullanıcı kuyruğu (`POST /api/admin/faz14-kuyruk/baslat`), Gemini onarım işçisi (`auto-repair/toggle-worker`),
serbest girdi ayrıştırma, ders işçisi, hat gece. v16'da bunların hepsi tek sayfada (Sistem › LLM işleri) toplanır: **durum + elle başlat/durdur**.
Zamanlama düğmesi olmaz, her başlatmada onay penceresi açılır ve denetim kaydı tutulur. `MEDS_LLM_OTOMATIK` panelden değiştirilemez.

## 3. Yeni bilgi mimarisi (8 grup, 52 sayfa)

Adres şeması `/manage/<grup>/<sayfa>[/<id>]`. Eski slug'lar yönlendirilir (§6).

### 3.1 Genel bakış

| Adres | Amaç | Veri | Eylem | Uç | Sayfa/arama | Öncelik |
|---|---|---|---|---|---|---|
| /manage | Durum panosu | sayaçlar, bekleyen kuyruklar, canlı kişi, son hatalar, dağıtım sürümü | ilgili sayfaya git | **yeni** `GET /api/admin/ozet` | — | P0 |
| /manage/gelen | Tek bekleyen kuyruğu | şikâyet, geri bildirim, tüyo, taslak, ayrıştırma | aç, çöz | mevcut inbox + toplama | sunucu | P0 |

### 3.2 İçerik: Kurullar ve dersler

| Adres | Amaç | Veri | Eylem | Uç | Sayfa | Öncelik |
|---|---|---|---|---|---|---|
| /manage/icerik/kurullar | Kurul takvimi, aktif kurul | kurul_takvimi | tarih düzenle, aktif kurulu gör | **yeni** `GET/PUT /api/admin/kurullar` | — | P0 |
| /manage/icerik/dersler | Ders kayıt defteri (kN.json) | ders, branş, kimlik, katman durumu | ad/branş düzenle, gizle/aç | **yeni** `/api/admin/dersler` | arama | P0 |
| /manage/icerik/dersler/:id | Ders ayrıntısı | katmanlar (sesli, Öğren, önem, çözücü, örnek, quiz), kapı sonuçları | katman bazında gizle/aç | yeni | — | P0 |
| /manage/icerik/branslar | branslar.json | branş listesi | düzenle | yeni | — | P2 |

### 3.3 İçerik: Sorular

| Adres | Amaç | Uç | Öncelik |
|---|---|---|---|
| /manage/sorular/havuz | Havuz soruları | katalog `pool` | P0 |
| /manage/sorular/cikmis | Çıkmış (96 MB, sunucu sayfalı) | katalog `past` | P0 |
| /manage/sorular/birlesen | Kopya grupları | question-merges | P1 |
| /manage/sorular/ornek | Örnek sorular | katalog `ornek` | P1 |
| /manage/sorular/ham | Ham defter (salt ekleme) | raw-pool | P1 |
| /manage/sorular/serbest | Serbest girdiler | question-intake | P2 |
| /manage/sorular/taslak | Taslaklar | drafts | P2 |
| /manage/sorular/dondurma | Havuz dondurma durumu (salt okunur) | **yeni** `GET /api/admin/havuz-dondur` | P2 |
| /manage/sorular/olasi | Olası sorular | olasiSoruRoutes | P2 |

### 3.4 İçerik: Öğrenme

| Adres | Amaç | Uç | Öncelik |
|---|---|---|---|
| /manage/ogrenme/desteler | Öğren desteleri (doğrulayıcı sonucu ile) | katalog `decks` | P1 |
| /manage/ogrenme/sesli | Sesli ders listesi, ses, zaman, çizim kapısı | sesli-anlatim (Oracle uyumlu hale getirilecek) | P1 |
| /manage/ogrenme/onem | Önem listesi, asistan, çözücü (branş) | **yeni** `/api/admin/spot-cozucu` salt okunur + gizle | P1 |
| /manage/ogrenme/spot | Sınav spotları | katalog bağdaştırıcısı (yeni) | P2 |
| /manage/ogrenme/kazanim | Kazanımlar | katalog | P2 |
| /manage/ogrenme/kart | Ezber kartları | katalog | P2 |
| /manage/ogrenme/kamp | Kamp, check-up, son prova, KMB: yayın durumu + tüyolar | kamp + **yeni** yayın bayrağı | P1 |

### 3.5 İçerik: Kaynaklar

| Adres | Uç | Öncelik |
|---|---|---|
| /manage/kaynak/sozluk (sözlük + kısaltma + terim) | katalog `glossary` + yeni bağdaştırıcılar | P1 |
| /manage/kaynak/hastalik | katalog `diseases` | P2 |
| /manage/kaynak/ozet | katalog `summaries` | P2 |
| /manage/kaynak/muzik | katalog `music` | P2 |
| /manage/kaynak/cop | katalog `trash` (geri yükle) | P1 |

### 3.6 Site

| Adres | Amaç | Eylem | Uç | Öncelik |
|---|---|---|---|---|
| /manage/site/gorunurluk | Sayfa + kurul + ders + varlık görünürlüğü (açık / gizli / yalnız yönetici) | anahtar, toplu, geçmiş | **yeni** `GET/PUT /api/admin/site-ayar/gorunurluk` + genel `GET /api/site-ayar` + SSE | P0 |
| /manage/site/menu | Menü önizleme (siteHaritasi), gizle | salt görünüm + gizle | site-ayar | P1 |
| /manage/site/bakim | Bakım kipi + süre metni | aç/kapa (çift onay) | `POST /api/admin/bakim` (kalıcılık eklenmeli) | P0 |
| /manage/site/bayraklar | Özellik bayrakları (tek şema) | aç/kapa | manage-settings → site-ayar | P1 |
| /manage/site/duyurular | Duyuru bandı + push/e-posta bildirimi | oluştur, zamanla değil elle gönder | send-notification, push, **yeni** duyuru ucu | P1 |
| /manage/site/kanallar | SMTP, WhatsApp, push anahtarları | sınama | smtp-*, whatsapp, push | P2 |
| /manage/site/surum | Canlı commit, guncelleme_notu, dağıtım geçmişi (salt okunur) | — | `/api/surum`, `dist/dagitim.json` | P1 |

### 3.7 Kullanıcılar

| Adres | Amaç | Uç | Sayfa | Öncelik |
|---|---|---|---|---|
| /manage/kisi | Kişi listesi (çevrimiçi, rol, son görülme) | `GET /api/admin/people?sayfa=&q=&sirala=` (**sayfalama eklenecek**) | sunucu | P0 |
| /manage/kisi/:key | 360° (sekmeler: özet, cihaz, etkinlik, çalışma, katkı, bildirim) | people/:key | — | P0 |
| /manage/kisi/:key/veri | Profil kv verisi: anahtar bazında gör/düzenle/sil | **yeni** `GET/PUT/DELETE /api/admin/user-data/:uid/:anahtar` + SSE `user_data_changed` | — | P0 |
| /manage/kisi/erisim | Rol, askı, moderatör, hesap birleştirme | people-access, birlestir | — | P0 |
| /manage/kisi/basarim | Puan, ATP, kilit, unvan + tanım | basarim/* | sunucu | P1 |
| /manage/kisi/ilerleme | Ders × öğrenci | calisma-matris (sayfalanacak) | sunucu | P1 |
| /manage/kisi/gorev | Seri ve görevler | gorev-takip | — | P2 |
| /manage/kisi/etkinlik | Etkinlik günlüğü (tüm kullanıcılar) | **yeni** `GET /api/admin/events?tur=&uid=&imlec=` | imleç | P1 |
| /manage/kisi/gizlilik | Veri dışa aktarma ve silme talepleri | **yeni** | — | P2 |

### 3.8 Topluluk

| Adres | Amaç | Uç | Öncelik |
|---|---|---|---|
| /manage/topluluk/sikayet | Soru + mesaj + not şikâyetleri tek liste | moderation + **yeni** mesaj şikâyeti | P0 |
| /manage/topluluk/sohbet | Odalar: üye, kilit, arşiv | **yeni** `/api/admin/topluluk/odalar` | P0 |
| /manage/topluluk/mesaj | Mesaj arama, gizle/sil (yumuşak), kullanıcı sustur | **yeni** `/api/admin/topluluk/mesajlar` | P0 |
| /manage/topluluk/arkadaslik | İstek/ilişki görünümü | **yeni** salt okunur + sil | P2 |
| /manage/topluluk/not | Paylaşılan notlar | **yeni** | P2 |
| /manage/topluluk/geri-bildirim | Öğren geri bildirimi, yorumlar | katalog `feedback` + learn-feedback/resolve | P1 |

### 3.9 Oyunlar

| Adres | Amaç | Uç | Öncelik |
|---|---|---|---|
| /manage/oyun/odalar | Canlı quiz odaları (RAM), oyuncu sayısı, kapat | **yeni** `GET/DELETE /api/admin/quiz/odalar` (quizRealtimeServer) | P1 |
| /manage/oyun/kaynak | Oyun soru kaynaklarını aç/kapa, soru sayısı | **yeni** `/api/admin/quiz/kaynaklar` | P1 |
| /manage/oyun/quiz-havuzu | quiz_havuzu.json + `quiz_dogrula.py` sonucu (salt okunur) | yeni | P2 |

### 3.10 Sistem

| Adres | Amaç | Uç | Öncelik |
|---|---|---|---|
| /manage/sistem/saglik | Servis sağlığı, kaynak, istemci hataları | servis/*, istemci-hata, console-logs | P0 |
| /manage/sistem/llm | LLM işleri: Faz14, onarım, ayrıştırma, hat. Elle başlat/durdur + kilit durumu | faz14-kuyruk/baslat, auto-repair/toggle-worker, **yeni** `GET /api/admin/llm-durum` | P0 |
| /manage/sistem/isler | Betikler ve iş geçmişi | scripts/* | P1 |
| /manage/sistem/hat | Hat panosu | hat/* | P1 |
| /manage/sistem/db | Veritabanı gezgini | pg/* | P0 |
| /manage/sistem/yedek | Yedek, dışa/içe aktarım, reset (çift onay) | db/*, pg/backups | P1 |
| /manage/sistem/denetim | Yönetici denetim kaydı | **yeni** `GET /api/admin/denetim` (+ `admin_auth_log.jsonl`) | P0 |
| /manage/sistem/drive | Drive eşitleme durumu, elle denetim | drive/* | P2 |
| /manage/sistem/rag | RAG indeksi durumu | **yeni** salt okunur | P2 |
| /manage/sistem/fazlar | Faz verisi aracı | phases/* | P2 |
| /manage/sistem/baglanti | Kısayollar | statik | P2 |

**P0 (17):** Genel bakış, Gelen, Kurullar, Dersler, Ders ayrıntısı, Havuz, Çıkmış, Görünürlük, Bakım, Kişi listesi,
Kişi 360°, Profil verisi, Erişim, Şikâyetler, Sohbet odaları, Mesajlar, Sağlık, LLM işleri, DB gezgini, Denetim kaydı.
(Kişi 360° ile Profil verisi ve Kurullar ile Dersler aynı kalıbı paylaştığından uygulamada 17 iş paketi olur.)

## 4. Ortak bileşenler ve performans ilkeleri

### 4.1 Bileşen seti (`src/components/v16/kit/`)

| Bileşen | Kaynağı | Not |
|---|---|---|
| `Liste` | yeni (`@tanstack/react-virtual` ya da elle yazılmış pencereleme) | sunucu sayfalaması/imleci, sütun seçimi, sıralama, satır seçimi, adreste durum (`?q=&s=`) |
| `Suzgec` | katalog facet'leri | arama kutusu 250 ms gecikmeli |
| `Cekmece` | consoleUi Drawer | ayrıntı ve düzenleme, adreste `/:id` |
| `Form` | yeni, şema güdümlü | şema EntityDef `editable` alanlarından gelir |
| `Onay` | yeni | tehlikeli eylemde yazılı onay (ör. "SIFIRLA") |
| `TopluCubuk` | manageKit BulkBar | |
| `JsonGor` | manageKit JsonView | |
| `Gecmis` | yeni | kayıt başına denetim satırları |
| `Durum` | yeni | boş, yükleniyor, hata, yetki yok |
| `Anahtar` | yeni | görünürlük ve bayraklar için üç konum |

### 4.2 Performans ilkeleri

1. **Rota bazlı lazy:** her sayfa ayrı yığın. Kabuk + Genel bakış < 60 KB gz.
2. **Sunucu tarafı sayfalama:** her liste ucu `{ogeler, toplam, imlec}` döner, varsayılan 50 satır. İstemcide tam dizi tutulmaz;
   `questions` prop'u konsola geçmez.
3. **Arama ucu:** katalogun `q` parametresi. Kişi ve mesajda pg `ILIKE`/trigram.
4. **SSE:** mevcut realtime kanalı. `content_changed`, `user_data_changed`, yeni `site_ayar_changed`, `moderasyon_changed`.
   Açık liste yalnız ilgili satırı yeniler.
5. **Yazma:** içerik yazımı tek yazıcı kuyruğundan geçer, `data/content/` katmanına gider ve denetim kaydına işlenir. Büyük JSON'da tam dosya yeniden yazımı arka planda yapılır.
6. **Durum:** konsol genel state'i kaldırılır. Sayfa durumu sayfada ve adreste tutulur, veri önbelleği tek bir sorgu katmanında (basit `useAdminQuery` + SWR).
7. **Tek kabuk:** v16 kabuğu. v12/v9/v14 CSS'i geçiş bitince silinir.

## 5. Yeni gereken uçlar

| Uç | Amaç |
|---|---|
| `GET /api/admin/ozet` | pano sayaçları |
| `GET/PUT /api/admin/kurullar` | kurul takvimi (data/content) |
| `GET/PUT /api/admin/dersler[/:id]` | ders kayıt defteri + katman durumu |
| `GET /api/site-ayar` (genel), `GET/PUT /api/admin/site-ayar[/gorunurluk]` | çalışma anı görünürlük ve bayraklar + SSE |
| bakım durumunun kalıcılığı | `POST /api/admin/bakim` → site_ayar |
| `POST /api/admin/duyuru`, `GET /api/duyuru` | duyuru bandı |
| `GET /api/admin/people` sayfalama/arama | mevcut ucun genişletilmesi |
| `GET/PUT/DELETE /api/admin/user-data/:uid/:anahtar` | profil kv |
| `GET /api/admin/events` | etkinlik günlüğü (imleçli) |
| `GET /api/admin/people/calisma-matris` sayfalama | mevcut ucun genişletilmesi |
| `/api/admin/topluluk/odalar`, `/mesajlar`, `/sikayetler` | sohbet moderasyonu |
| `/api/admin/topluluk/arkadaslik`, `/notlar` | P2 |
| `GET/DELETE /api/admin/quiz/odalar`, `GET/PUT /api/admin/quiz/kaynaklar` | oyunlar |
| `GET /api/admin/llm-durum` | kilit + kuyruk durumu |
| `GET /api/admin/denetim` | yönetici denetim kaydı (tüm `/api/admin` yazmalarına ara katman) |
| `GET /api/admin/spot-cozucu` | önem/asistan/çözücü envanteri |
| `GET /api/admin/havuz-dondur` | salt okunur |
| katalog bağdaştırıcıları: `spot`, `kisaltma`, `terim`, `sinav_dagilimi` | `dataCatalogService.ENTITIES` |

## 6. Taşınacaklar ve kaldırılacaklar

| Mevcut | Karar | Hedef |
|---|---|---|
| ManageCatalogSection + dataCatalogService | **Yeniden kullanılır** (omurga) | İçerik sayfaları katalogun varlık başına görünümleri |
| ManagePeopleSection, PersonStudy, UserAccessControls, HesapBirlestir | taşınır, parçalanır | Kullanıcılar |
| ManageBasarim, GorevTakip, StudyProgress | taşınır | Kullanıcılar |
| ManageModerationSection, moderationActions, Inbox | birleşir | Gelen + Şikâyetler |
| ManageDatabaseExplorer, ManageDatabaseV14 | taşınır | Sistem › DB, Yedek |
| ManageHatSection, AdminScriptsTab, ServiceControl, SystemSection | taşınır | Sistem |
| ManagePendingOperations | taşınır | Sistem › LLM işleri |
| RawPool, Merges, Intake, Drafts, Kamp, SesliAnlatim | taşınır (kendi sayfaları) | İçerik |
| ManagePoolV14 | taşınır, sunucu sayfalamasına geçer | Sorular › Havuz |
| consoleUi, manageKit, pageKit | kite girer | v16/kit |
| **ManageDataSection (Tüm veriler)** | **kaldırılır** | katalogla çakışıyor, istemci tarafında çalışıyor |
| **ManageDataCoreSection (Veri Merkezi v2)** | **kaldırılır** | sunucu karşılığı yok |
| **DraftStudio (Taslak stüdyosu)** | kaldırılır ya da P2 lazy | kullanımı belirsiz, 1876 satır |
| **ManageAutomationSection "Zamanlama"** | kaldırılır | zamanlayıcılar maskeli (kural 20). Drive kısmı Sistem › Drive'a |
| **ManageDersIsci* (4 dosya)** | salt okunur arşive indirilir | Oracle işçisi durdu. Elle üretim §19 oturumda yapılıyor |
| ManageNotebookLMSection | P2 lazy ya da kaldırılır | kullanımı düşük |
| ManageUsersSection "Katkılar" | Kişiler'e katılır | çakışma |
| ManageShortcuts | Sistem › Bağlantılar | |
| ManageShellV12/ManageV12, `manage-v9.css`, `ms-*` | geçiş bitince silinir | tek kabuk |
| FlatfileDataOnboarding (1126) | kullanımı denetlenmeli, büyük olasılıkla ölü | |
| AdminFloatingSwitcher, AdminMobileBridgeModal | korunur | mobil yönetici köprüsü |

Eski adres yönlendirmesi: `bekleyen-islemler→sistem/llm`, `moderasyon→topluluk/sikayet`, `soru-havuzu→sorular/havuz`,
`veri-katalogu→icerik (varlığa göre)`, `kisiler/<k>→kisi/<k>`, `veritabani-gezgini→sistem/db`, `puan-atp→kisi/basarim` …
(`siteHaritasi.ts` mantığıyla tek tablo).

## 7. Riskler

1. **Görünürlüğün çalışma anına taşınması:** `GIZLI_SAYFALAR`/`KAPALI_SAYFALAR` bugün derleme sabiti. Çalışma anı ayarı istemcide geç yüklenirse
   gizli sayfa bir an görünür. Sabitler varsayılan olarak kalmalı, ayar SW önbelleğine alınmamalı.
2. **Oracle src/data geçiciliği:** yeni yazılabilir her varlık `data/content` katmanına ve deploy [0b] listesine eklenmezse panel yazımı ilk dağıtımda kaybolur.
3. **96/86 MB JSON yazımları:** eşzamanlı yazım bozulması (`pastQuestions.json.*.tmp` kalıntısı bunu gösteriyor). Tek yazıcı + atomik rename + yedek zorunlu.
4. **Kural 20:** LLM sayfası zamanlayıcı ya da otomatik tetik içeremez. `toggle-worker` ve `faz14` yalnız onaylı elle başlatma.
5. **Kural 16 çakışması:** menü yapısını panelden değiştirmek site haritası tek kaynağını bozar. Panel yalnız gizle/aç yapar, sıra ve yapı kodda kalır.
6. **Tehlikeli uçlar:** `db/reset`, `db/import`, `pg/sql` (salt okunur olduğu doğrulanmalı), `pg/row DELETE`, `users/:uid DELETE`. Hepsi çift onaylı ve denetim kaydına bağlı olmalı.
7. **Ham defter ve havuz dondurma:** değiştirilemezlik korunmalı. Panelde silme düğmesi olmaz.
8. **Sohbet moderasyonu kişisel veri içerir:** mesaj okuma da denetim kaydına yazılmalı.
9. **Büyük geçiş:** 23 bin satır. Aşamalı yapılmalı: kit + kabuk + P0 → P1 → P2. Her aşama `vite build`, sunucu değişikliğinde `meds-web` yeniden başlatma (kural 12), `dagit.sh` + onem+1 (kural 13/15).
10. **Canlı sınama yapılmadı:** "çalışıyor" değerlendirmeleri koda dayanıyor. P0 başlamadan önce her bölüm canlıda tıklanarak doğrulanmalı.

## 8. Uygulama sırası

1. Kit + v16 kabuğu + rota bazlı lazy + eski adres yönlendirmesi + denetim ara katmanı.
2. P0 uçları (ozet, site-ayar, kurullar, dersler, people sayfalama, user-data, topluluk, llm-durum, denetim).
3. P0 sayfaları. Eski bölümler o sırada eski kabukta erişilebilir kalır.
4. P1, sonra P2. Ardından kaldırılacak bölümlerin ve v9/v12 CSS'in silinmesi.
