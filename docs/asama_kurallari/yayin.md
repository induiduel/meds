# Aşama kuralları — yayin

> ÜRETİLMİŞ DOSYA: elle yazma. Kaynak `docs/KURUL2_YAPILMAYACAK_HATALAR.md`, üreteç `scripts/hat/tam_hat/kural_secici.py`. 45 madde. Tek satırlı maddeleri betik denetler (tam metin: `kural_secici.py --tam <H no|aşama>`).

### H6 — Birleştirici ders/dosya siliyor
- **Kural:** birleştirici yalnız ekler/günceller; reddedilen ders eski hâliyle kalır.
- **Kapı — EKLENDİ:** `ders_zinciri.korumali`: ders sayısı düşerse ya da öğe sayısı %10'dan fazla azalırsa yedek geri konur (kod 11). Silen, küçülten ve ekleyen durumlar sınandı.


- H14 — Sunucu kodu Oracle'da ama çalışan sunucu eski kodla (yeni uç sitenin ana sayfasını döndürüyor) — betik denetler: `deploy-code.sh`
### H29 — "Burası önemli" kuralları birbiriyle çelişiyordu; OCR'lı sayıda sıfır kayıp yanlış alarmı (2026-10-23)


### H37 — Oracle'da yayın/işaret yazamıyordu: sahiplik (2026-10-24)


### H56 — Yeni yayınlanan dersin PDF'i uygulamada açılmıyordu (2026-10-24, kullanıcı, k2-07)


### H63 — Sesli Derslerde Arşiv PDF'lerinin Çok Geç Yüklenmesi veya Hiç Yüklenmemesi (AutoFetch, SW Range ve Linearization Hatası) (2026-10-26, kullanıcı)
- **Çözüm & Kural:**
  1. `PdfDocView.tsx`: `disableAutoFetch: true` ve `rangeChunkSize: 256 * 1024` sabitlendi. PDF.js artık asla tüm dosyayı arka planda otomatik çekmez; yalnızca o an görüntülenen sayfanın 256 KB'lık dilimini çeker ve ilk sayfa 1 saniyenin altında ekrana gelir.
  2. `public/sw.js`: `/api/lecture-pdf/` akışları Service Worker tamponlama ve cache mekanizmasından tamamen muaf tutularak (`return;`) doğrudan tarayıcının yerel yüksek hızlı ağ motoruna bırakıldı (`SW v16`).
  3. `pikepdf` motoru ile tüm arşiv PDF'leri linearize edildi (Fast Web View); ilk sayfa ve xref tablosu dosyanın ilk kilobaytlarına taşındı.
  4. `server.ts`: `/api/lecture-pdf/deck/:deckId/:index` için `Accept-Ranges: bytes` ve `public, max-age=604800, stale-while-revalidate=86400` başlıkları eklendi.





### H73 — `terim/` klasörü dağıtım betiğinin veri listesinde yoktu; terim dosyaları canlıya ulaşamıyordu (2026-10-26)
- **Çözüm / kural:** Listeye `terim` eklendi. `data/sesli_anlatim` altına yeni bir veri türü ekleyen her oturum, `deploy-code.sh` [1b] listesini de günceller; dağıtımdan sonra canlı API yanıtında alanın varlığı `curl` ile doğrulanır.


### H88 — Drive klasör adı değişince yayın PDF'in kaynak kimliğini bulamadı (2026-10-27, k2-03)
- **Çözüm / kural:** sunucu ve deneme kipi `kaynak_kimligi_esnek` kullanır; esnek eşleme klasör farkını yok sayıp `Kurul N/<branş>/`
  sonrası yol manifestte tekse onu kabul eder. Yayın denetim hatasında taslağın `yayin.json`'u silinip yeniden onaylanır.


### H94 — Çıkmış listesinde birleştirilmiş gizli kopya: çip 404 verdi (2026-10-27, k2-03)
- **Kural:** `cikmis_konum` yalnız sunulan soru kimliklerini içerir; canlı doğrulamada her kimlik `/tek` 200 vermeden ders tamam sayılmaz.


### H95 — Yayın düzeltmesinde olmayan alan; PDF eşleyici durdurulan işçi kapsayıcısında (2026-10-27, k2-03/k2-04)
- **Önleme kuralı:** yayın betiği değişikliği Oracle'a gitmeden önce yerel taslakla `kaynak_kimligi_esnek` ve `--deneme` akışı
  çalıştırılır; yayından sonra `/api/lecture-pdf/deck/<deck>/0` 200 kontrolü zorunlu.


### H97 — Dağıtım, yeni sesli ders metnini git'teki eski sürümle geri aldı; ses eski metinle üretildi (2026-10-27, k2-03/k2-04)
- **Kural:** yeni metin + v2 + vurgu + hizalama önce commit/push, sonra ders-ekle; ses tamamlanınca eski metne ait varyantlar silinir (`DELETE /api/sesli-anlatim/ses/<key>/<vid>`); `kayit.json` süre/özet ve `takip_kapisi --api` ile doğrulanır.


### H99 — Dağıtım sunucu servis değişikliğini "yalnız ön yüz" sandı; yeni data dosyası Oracle'a gitmedi (2026-10-27, sınama)
- **Kural:** sunucu kodu değişen dağıtımdan sonra `curl` ile yeni davranış doğrulanır; gerekirse `docker restart meds-app` ve sağlık kontrolü. Yeni `data/*.json` dosyası Oracle'a elle (`scp` + `sudo cp`) kopyalanıp canlıda okunduğu doğrulanır.


### H116 · Birleştiriciler yeni ders eklerken branştaki eski dersin dosyalarını da yeniden yazıyor (2026-10-27, k2-05 Nörolojik Muayene)
- **Kural:** elle zincirde her birleştirmeden sonra `git diff --stat`; yalnız yeni dersin dosyaları ve indeksteki yeni ders satırı sahnelenir;
  eski dersin dosyaları `git checkout` ile geri alınır, indekste eski ders satırı HEAD'den korunur (bilerek yapılan toplu yenileme hariç).


### H129 — "Salt okunur" SQL konsolu süper kullanıcıyla çalışıyordu (2026-10-28, Yönetim v16)
- **Önleme:** "salt okunur" iddia eden her uç bağlantı rolünün yetkisiyle sınanır (COPY TO PROGRAM, pg_read_file, pg_authid, CTE içinde DELETE); tehlikeli uçlar istemci onayına ek olarak sunucuda onay sözcüğü ister.


### H130 — Canlı içerik katmanı tam kopyaydı, kaynaktaki yeni kayıtları gölgeliyordu (2026-10-28)
- **Önleme:** `python3 scripts/icerik_katman.py denetle` 0 HATA (tam kopya = HATA, birleşimde kaynak kaydı eksik = HATA). Katmana bütün dosya kopyalayan yeni yazıcı yazılmaz; başlangıç kopyası gerekiyorsa `resolveContent(file)` (birleşik) kopyalanır, ham kaynak değil.


### H138 — Sekmede açılan görsel/JSON yanıtı site kabuğu diye önbelleğe yazılıyordu (2026-10-28, sayfa denetimi)
- **Çözüm/kural:** Yalnız `Content-Type: text/html` yanıt kabuğa yazılır; `CACHE_VERSION` v19 kirlenmiş eski kabuğu siler. Kabuk önbelleğine yazan her yol içerik türünü denetler.


### H390–H392 — Veri tutarlılığı: yıldız işaretleri, soru haritası sayımı, deste kurul adları, yinelenen kazanım konuları (2026-10-28, kullanıcı onayıyla)
- **H390 Belirti:** Deneme ekranında soru/şık metninde `**değildir**`, `**Soru:**` ham görünüyordu. **Kök neden:** veri doğru (kasıtlı vurgu; çıkmışta 49 soru, Öğren klinik karar vakalarında 414 öge), `PracticeV15` metni işlemeden yazıyordu. **Çözüm:** `**…**` kalın yazıya çevrilir; veri değişmedi.

### H437 — Çevrimdışı indirme "sırada" takılıyor, her açılışta uygulama dosyası iniyor (2026-10-29)
- **Önleme:** arka plan indirmesinde dosya başına bekleme süresi toplam süreyi paket boyuyla çarpar — bekleme paket başına değil dosya başınaysa üst sınır saniyeler düzeyinde tutulur; sürüm değişimi her dağıtımda olan bir paket kuyruğun önüne zorla alınmaz.


### H441 — Sesli ders listesi (`/api/canli-ders`) canlıda her açılışta 1,2 sn (2026-10-29)
- **Önleme:** İstek başına döngü içinde dosya okuyup ayrıştırma yapılmaz; değişmeyen kayıt defteri bir kez okunur, imza (boyut+mtime) değişince tazelenir. Önbellekten dönen nesne değiştirilmez (yazan kod taze `oku` kullanır). Yeni liste ucu eklerken Oracle içinden `curl -w %{time_total}` ile ölçülür (hedef < 50 ms).


### H457 — Sesli ders "İndir" düğmesi indirmeyi hiç başlatmıyordu (çevrimdışı, 2026-10-31)
- **Önleme:** tarayıcıya devredilen bir indirme/iş, ilerleme gelmezse zaman aşımıyla sayfa içi yola düşmeden kullanılmaz;
  çevrimdışı içerik kullanıcının dosya sistemine değil uygulama önbelleğine yazılır.


### H466 — Google/Firebase projesi askıya alındı: kimse giriş yapamadı, site fiilen kapandı (2026-11-02)
- **Önleme:** Kimlik, veri, yedek ve canlı yayın yalnız Oracle'da (meds-pg + sunucu). Yeni özellik dış bir hesaba bağlı
  **zorunlu** bir yol (giriş, veri yazımı, yedek) açamaz; dış servis yalnız kesilince sitenin çalışmaya devam ettiği
  isteğe bağlı ek olabilir (yazı tipi, LLM gibi). Jeton doğrulaması ağ çağrısı yapmaz. Kimlik e-postası (kod) SMTP'ye
  bağlıdır; SMTP gitmezse yönetici Kullanıcılar › Erişim › "Şifre kodu üret" ile 24 saatlik kod verir.


### H467 — Taşınan hesaplar için e-postaya bağlı şifre belirleme tek yoldu; Drive'da ölü servis hesabı yedeği (2026-11-02)
- **Önleme:** Hesap kurtarmanın en az bir yolu hiçbir dış hesaba bağlı olmamalı (yönetici onayı). Bir dış servisin yedeği
  çalışmıyorsa sessiz geçilmez, günlüğe bir kez yazılır. İçerik alımı herkese açık Drive yoluyla çalışır; kimlikli yedek
  için kullanıcı askıda olmayan bir hesapta yeni servis hesabı ya da `rclone config reconnect meds:` kurmalıdır.


### H471 — Yeni Kurul 2 derslerinde PDF açılmadı, PDF işareti atlandı (2026-11-02)
- **Önleme:** Elle hatta yayın sırası: PDF → manifest + iki drive_root → `yayinla.py --yerel` → `build_deck_pdf_sources.py`
  (bütün desteler yayınlandıktan sonra) → commit/dağıtım → `ders-ekle`. Dağıtımdan sonra `/api/lecture-pdf/deck/<deste>/0` 200
  denetlenir.


### H474 — Bu yılın PDF'inden üretilen Farmakoloji dersi öğrenciye görünmedi (2026-11-02)
- **Önleme:** Sınama yalnız anahtar listesiyle verilir (branş kuralı yok). Yeni ders yayınında §6 doğrulaması güncel listede
  (`/api/canli-ders`, `donem` yok) dersin anahtarını arar; yoksa yayın bitmiş sayılmaz. `data/*.json` değişikliği Oracle'a
  `scp + sudo cp + chown ubuntu` ile ayrıca konur ve canlı uçtan okunarak doğrulanır.


### H479 — Yönetim › Quiz havuzu Oracle'da boştu (Docker'da rootDir/.. yanlış kök) (2026-11-03)
- **Önleme:** Sunucu kodunda kardeş veri klasörleri `rootDir/..`'dan değil ortam değişkeninden (MEDS_DATABASE_DIR, MEDS_TEMP_DIR, MEDS_DOWNLOADS_DIR) türetilir;
  yeni uç canlıda (Oracle) bir kez çağrılarak boş olmadığı doğrulanır.


### H480 — Canlı damgası yeni commit'i gösterirken sunucu kodu eski kaldı (2026-11-03)
- **Önleme:** dağıtım "bitti" ancak canlının diskindeki kod hedef commit'le eşleşince sayılır; damga doğrulamadan önce yazılmaz.


### H481
- **Önleme:** bir isteği SW'den "ağa bırakan" her kısa devre, o adresi yazan TÜM önbellekleri (paket, sesli ders, eski PDF) önce denetlemelidir;
  çevrimdışı düzeltmesi internetsiz gerçek sınamayla doğrulanmadan bitmiş sayılmaz.


### H482
- **Önleme:** yeni bir çevrimdışı önbellek adı eklenince `ARAMA_SIRASI` ve lecture-pdf kısa devresi birlikte güncellenir.


### H483
- **Önleme:** çevrimdışı indirmeye yeni bir parça eklenince denetim (`paketiDenetle`) ve `eksikGider` aynı commit'te güncellenir; `ONARIM_SURUM` artırılır.


### H503 — "Güncelle"ye basınca eski sürüm açılıyor, sürekli güncelleme varmış gibi görünüyordu (2026-11-06)
- **Çözüm/önleme:** `UpdatePrompt.tsx`: güncellemede çevrimdışı ders/paket önbellekleri dışındaki tüm önbelleklerden HTML/rota kabuğu kayıtları silinir; sürüm kayıtları yalnız ileri yazılır. Kural: cihaz sürüm kaydı asla geriye yazılmaz; kabuk silme, SW'nin aradığı bütün önbellekleri kapsar.


### H505 — Polinöropati ve Bazal Ganglionlar sesli derslerinde PDF açılmıyor, yalnız "Drive'da aç" çıkıyordu (2026-11-06)
- **Çözüm/önleme:** iki kayıt eklendi, sunucu yeniden başlatıldı, dağıtıldı. Yeni kapı `python3 scripts/kapilar/ders_pdf_kapisi.py [--sunucu …]`: her `data/sesli_anlatim/hizalama/k2-*.json` deckId'si sunucu kataloğunda açılabilir PDF'le bulunmalı (0 HATA). Kural: `ders-ekle`/hizalama sonrası SANAL_DESTELER kaydı + `meds-web` restart + bu kapı (yerel ve Oracle) — kapı geçmeden ders yayında sayılmaz.


### H513 — dist/assets hiç budanmıyordu: cihazda 473 derleme (3 GB), Oracle'da 92 bin parça (5,2 GB) + 5,9 GB arşiv (2026-11-09)
- **Önleme:** Hash'li çıktı biriktiren her klasöre (dist, arşiv, ses klipleri) yazan kod, "güncel küme + yaş" kuralıyla budama da yazar; "sonra temizleriz" diye bırakılmaz. Oracle'da imaj yeniden kurulduğunda `docker builder prune` dağıtım sonrası adımıdır (`dagit.sh`'a eklenmedi; elle).


### H516 — Dağıtım yeniden başlatması sırasında açılan sayfa açılış ekranında sessizce takılıyordu (2026-11-09)
- **Çözüm/önleme:** `index.html` H516 bekçisi: 7 sn'de açılmazsa `/api/surum` yoklar, durum yazısı gösterir, sunucu dönünce kendiliğinden yeniler. Kural: öğrencinin bekleyebileceği her "sunucu yok / ağ yok / eski kabuk" durumu ekranda bir yazı + kendiliğinden kurtulma yolu taşır; sessiz bekleme yasak. Dağıtım saatinde gelen "site açılmıyor" bildiriminde önce Oracle `docker events`/uptime'a bakılır (bu kez `uptime: 18 s` ile doğrulandı).


### H539 — EMA tam MP3 yüklemesi Oracle'daki başka bir dağıtımın sunucu yeniden başlatmasına denk gelince iş "hata"ya düştü (2026-11-09, k2-22)
- **Önleme:** dağıtım öncesi `dagit.sh` kuyrukta `calisiyor` EMA işi varsa beklemeli ya da işçi `tam/bitir` adımını 3 kez yinelemeli (yapılacak). İşçi günlüğü: `journalctl --user -o cat | grep <key>` (birim değil, scope).


### H545 — `git add server.ts` başka oturumun commit'lenmemiş iki satırını da commit'e aldı; depoda olmayan dosyayı içe aktaran sunucu kodu origin/main'e gitti (2026-11-10)
- **Önleme:** ortak dosya sahnelenmeden önce `git diff <dosya>` okunur; yabancı satır varsa yalnız kendi parçaların sahnelenir (`git apply --cached` / `git update-index --cacheinfo`). Commit'ten sonra `git show --stat` satır sayıları beklenenle karşılaştırılır. Oracle'da `server.ts`'in kirli sürümle bulunmasının kaynağı saptanamadı (dağıtım temiz worktree'den yapılır); yinelenirse o dakikada Oracle'a yazan öteki süreç aranır.


### H556 — "PDF indir" herkese "X-API-Password başlığı gereklidir" diyordu; canlıda başsız tarayıcı da yoktu (2026-11-13, kullanıcı bildirdi)
- **Önleme:** yeni bir parolasız uç gerektiğinde önce "veri yazıyor mu?" sorusu sorulur: yazmıyorsa `readOnlyPosts`/`STUDENT_WRITE_ROUTES`'a **sınırıyla** eklenir, yazıyorsa parola ister. Kapı: `python3 scripts/kapilar/pdf_basim_kapisi.py` (yerelde ve canlıda) `/api/pdf/status` `available:true` + parolasız 200 ve `%PDF` imzası arar; 401'de "uç beyaz listede değil", tarayıcı yoksa "imaja chromium eklenmeli" der.

### H559 — İçerik katmanı toplu "silinen" yazdı: sözlükte 750 terim, Öğren'de 11 deste sunucuda görünmüyordu (2026-11-13, kullanıcı bildirmedi — tur sırasında bulundu)
- **Önleme:** `data/content/` altına elle, başka araçla ya da eski yedekten **tam kopya bırakılmaz** (yalnız `.fark.json`). Sözlük/deste/soru sayısı beklenenden az görünürse ilk bakılacak yer `data/content/<dosya>.fark.json` → `silinen`dır; `python3 scripts/icerik_katman.py denetle` ile katman düzenli denetlenir. Günlükte "toplu silme sayılmadı, karantinaya alındı" uyarısı görülürse `_karantina_silinen.json` açılır: silme gerçekten yönetici kararıysa kimlikler fark dosyasına elle yazılır; değilse hiçbir şey yapılmaz — kayıtlar görünür kalır. Katmanı mtime'a göre "taze" saymak yetmez: bir kopya yeni damgalı ama içeriği eski olabilir.


### H562 — Canlıda yeni anahtar "yok" göründü: `env_file` yalnız konteyner oluşturulurken okunur, loopback da konteynerde loopback değildir (2026-11-13)
- **Önleme:** `.env`'e yalnız dotenv'in okuyacağı yeni anahtar ekleniyorsa konteyner yeniden başlatma yeterlidir; **compose `environment:` listesine eklenmesi gereken** bir değişken söz konusuysa `docker compose up -d --force-recreate` gerekir (bu tur gerekmedi). "Container env'de yok" tek başına "uygulama görmüyor" demek değildir; kanıt uygulamanın kendi ucundan alınır. Konteyner içinden atılan istek yönetici/loopback muamelesi görmez.


### H579 — "Oracle'da kok'u import eden her betik çöküyor": kök markerı yalnız geliştirme makinesinde vardı (2026-11-16, dağıtım sonrası canlı sınama)
- **Önleme kuralı:** Kök çözümü yalnız REPO İÇİNDE izlenen dosyalara dayanır (git'te olmayan, makineye özgü dosya marker olamaz).
  Yol/altyapı değişikliği dağıtıldıktan sonra Oracle'da en az bir zamanlayıcı birimi GERÇEKTEN çalıştırılıp günlüğü okunur; sağlık uç
  noktası ve birim "success" durumu yeterli kanıt değildir (boru hattı çıkış kodunu yutabilir).


### H580 — "Otomatik onarım / NotebookLM ile düzelen deste dağıtımda geri dönüyor" (2026-11-16)
- **Önleme kuralı:** Sunucu tarafında `src/data` altına yazan her kod `writableContent()` ile yazar, `resolveContent()` ile okur; türetilmiş dosyalara (`decks/items`, paketler) elle yazılmaz.


### H581 — "Panelden/NotebookLM'den düzeltilen sözlük, kart, özet, örnek soru dağıtımda geri dönüyor" (2026-11-16)
- **Önleme kuralı:** Yeni bir koruma sezgisi kurulurken yanlış alarm oranı ölçülür; dosya düzeyinde muafiyet verilmez, muafiyet satır parçasıyla ve gerekçeyle yazılır. Açık: ansiklopediyi okuyanlar (`src/data/glossary.ts` derleme, queryIntel/diseaseGraph derleme betikleri) katmanı görmüyor.


### H582 — "Ansiklopedi düzeltmesi Oracle'da dağıtımı durdurabilir / ekrana gelmez" (2026-11-16)
- **Önleme kuralı:** Kimlik üreten her slug çakışmayı sonekle çözer ve kimlik tekilliği doğrulanır. Panelden/hattan yazılan her src/data dosyası CONTENT_FILES'ta tür olarak kayıtlıdır ve ekran onu ortak yükleyiciden okur.


### H583 — "`git add -A` gizli anahtarı ve 600 MB çalışma verisini herkese açık depoya gönderdi" (2026-11-16)
- **Önleme kuralı:** Toplu commit'te `git add -A` yerine yol listesi; "her şeyi commitle" = izlenen + bilinçli yeni kod/belge, çalışma verisi değil. Sahnelenen yeni dosyalarda ≥5 MB ya da gizli adlı (`anahtar`, `.env`, `key`, `token`, `secret`) dosya kapı tarafından durdurulur.


### H585 — "Otomatik onarım / özel redaksiyon / soru yükseltme çıkmış soru dosyasını sunucu önbelleğini atlayarak yazıyordu" (2026-11-16)
- **Önleme kuralı:** `data/pastQuestions.json`'a sunucu kodunda `savePastQuestionsDb` dışında yazılmaz; yeni servis dosyayı açmaz, `cikmisErisim` kullanır. Tek seferde >%10 kayıt düşüren yazım reddedilir (`MEDS_PAST_TOPLU_SIL=1` kaçışı, yalnız kullanıcı komutu). Model: `docs/VERI_MODELI.md` §4.


### H592 — `.gitignore`'daki ses dizinlerinde 2.809 MP3 hâlâ izleniyordu (2026-11-17)
- **Kural:** `.gitignore`'a dizin ekleyen aynı commit'te `git ls-files -ci --exclude-standard` boş mu diye bakar. Geçmişteki nesneler `.git`'te kalır; küçültmek geçmiş yeniden yazımı ister (kullanıcı kararı).

