# Hata defteri — içerik katmanı ve depo güvenliği (dagitim_sunucu.md'den bölündü, 2026-11-16)

Sunucunun src/data'ya katmansız yazımı ve git/depo güvenliği maddeleri.

## H580 — "Otomatik onarım / NotebookLM ile düzelen deste dağıtımda geri dönüyor" (2026-11-16)
- **Belirti:** Otomatik hata onarımı ya da NotebookLM aktarımıyla değişen Öğren destesi Oracle'da bir sonraki dağıtımda eski hâline dönüyor; `decks/items/<id>.json` parçası kaynakla sapıyor; slayt ucu değişikliği hiç göstermiyor.
- **Kök neden:** `autoErrorRepairEngine.ts` ve `notebooklmBridgeService.ts` içerik katmanını atlayıp imaj içi (geçici) `src/data/interactive_learning_decks.json` ve türetilmiş `items/` parçasına doğrudan yazıyordu; `/api/decks/:id/slides/:n` ucu katmana bakmadan önce `items/`'tan okuyordu.
- **Kalıcı çözüm:** İki servis `resolveContent()` ile okur, `writableContent()` + `markContentChanged('decks',[id])` ile yazar (fark `data/content`'te kalır); `items/` yazımı kaldırıldı; slayt ucu `/api/decks/:id` ile aynı katman denetimini yapar.
- **Önleme kuralı:** Sunucu tarafında `src/data` altına yazan her kod `writableContent()` ile yazar, `resolveContent()` ile okur; türetilmiş dosyalara (`decks/items`, paketler) elle yazılmaz.

## H581 — "Panelden/NotebookLM'den düzeltilen sözlük, kart, özet, örnek soru dağıtımda geri dönüyor" (2026-11-16)
- **Belirti:** NotebookLM aktarımı ve katkı geri alma ile yapılan sözlük, bilgi kartı, ders özeti, örnek soru ve ansiklopedi değişiklikleri Oracle'da bir sonraki dağıtımda kayboluyordu; ayrıca 100 MB'lık `src/data/pastQuestions.json` gereksiz yere yeniden yazılıyordu.
- **Kök neden:** H580 ile aynı sınıf — `notebooklmBridgeService.ts`, `notebooklmManageService.ts` ve `autoErrorRepairEngine.ts` içerik katmanını atlayıp imaj içi (geçici) `src/data`'ya yazıyordu. İlk yapı kapısı (D5) dosya düzeyinde sezgiseldi: 10 dosyayı işaretledi, 7'si yanlış alarmdı (src/data'yı yalnız okuyorlardı), asıl hedefi göremiyordu.
- **Kalıcı çözüm:** Üç servis CONTENT_FILES için `resolveContent`/`writableContent` + `markContentChanged` kullanıyor; src/data kopya yazımları kaldırıldı (asıl kayıt `data/`). D5 artık yazma çağrısının İLK argümanını değişken zinciri boyunca izliyor; gövdesinde `writableContent` olan sarmalayıcılar güvenli, okunan veri değişkenleri yol sayılmıyor. İzin listesi satır düzeyinde (1 kalem: server.ts srcPast).
- **Önleme kuralı:** Yeni bir koruma sezgisi kurulurken yanlış alarm oranı ölçülür; dosya düzeyinde muafiyet verilmez, muafiyet satır parçasıyla ve gerekçeyle yazılır. Açık: ansiklopediyi okuyanlar (`src/data/glossary.ts` derleme, queryIntel/diseaseGraph derleme betikleri) katmanı görmüyor.

## H583 — "`git add -A` gizli anahtarı ve 600 MB çalışma verisini herkese açık depoya gönderdi" (2026-11-16)
- **Belirti:** "Her şeyi commitle" isteğinde `git add -A` ile atılan commit 7.282 dosya ekledi: `data/.kimlik_anahtari` (giriş imza anahtarı), yönetici denetim ve istemci hata kayıtları, 10 çözücünün ses klipleri, `meds_temp/`, `meds_downloads/` PDF'leri (597 MB) — depo PUBLIC.
- **Kök neden:** `.gitignore` yalnız iki çözücü ses klasörünü ve birkaç dosyayı kapsıyordu; git dışı olması gereken çalışma verisi (AGENTS: "klipler git dışı") kuralla değil alışkanlıkla dışarıda tutuluyordu. `git add -A` kör toplu ekleme yaptı; pre-commit kapısı boyut/gizli dosya denetlemiyordu.
- **Kalıcı çözüm:** Commit geri alınıp yalnız amaçlanan 24 dosyayla yeniden atıldı (force-with-lease, yalnız o commit); `.gitignore` kalıpları eklendi (anahtar, `data/*_cozucu/ses/`, `_yedek`, `ders_kilit`, istemci/denetim kayıtları, `ses/`, `cikis/`, `meds_temp/`, `meds_downloads/`); yapı kapısına D9 (gizli/büyük dosya sahnelenmesi HATA) eklendi. Anahtar döndürüldü.
- **Önleme kuralı:** Toplu commit'te `git add -A` yerine yol listesi; "her şeyi commitle" = izlenen + bilinçli yeni kod/belge, çalışma verisi değil. Sahnelenen yeni dosyalarda ≥5 MB ya da gizli adlı (`anahtar`, `.env`, `key`, `token`, `secret`) dosya kapı tarafından durdurulur.

## H585 — "Otomatik onarım / özel redaksiyon / soru yükseltme çıkmış soru dosyasını sunucu önbelleğini atlayarak yazıyordu" (2026-11-16)
- **Belirti:** Görünür hata bildirilmedi; analizde bulundu. Onarım motoru bir soruyu düzeltirken aynı anda öğrenci oyu/düzenlemesi gelirse biri diğerinin yazımını ezebilirdi; her çağrıda 97 MB dosya baştan ayrıştırılıyordu (bellek tepe 2,2 GB'ın bir kalemi).
- **Kök neden:** `autoErrorRepairEngine.ts`, `questionUpgradeService.ts`, `notebooklmManageService.ts` ve `server.ts` özel redaksiyon ucu `data/pastQuestions.json`'u kendileri okuyup `writeFile` ile geri yazıyordu; sunucunun `cachedPastQuestionsDb` önbelleği, toplu atomik yazımı, boşla ezme freni ve DB aynası (`savePastQuestionsDb`) devre dışı kalıyordu. Ayrıca her kayıtta dosya `src/data/` altına 97 MB kopyalanıyordu.
- **Kalıcı çözüm:** `src/services/cikmisErisim.ts` — sunucu açılışta kendi okuma/kaydetme işlevlerini enjekte eder (`registerCikmisErisimi`); servisler yalnız `cikmisOku()` / `cikmisKaydet()` kullanır. Enjeksiyon yoksa (betik) okuma salt okunur, yazma reddedilir ve günlüğe yazılır. `src/data` aynası kaldırıldı (`MEDS_PAST_SRC_AYNA=1` değilse), okuyucu betikler `scripts/kok.py::CIKMIS`.
- **Önleme kuralı:** `data/pastQuestions.json`'a sunucu kodunda `savePastQuestionsDb` dışında yazılmaz; yeni servis dosyayı açmaz, `cikmisErisim` kullanır. Tek seferde >%10 kayıt düşüren yazım reddedilir (`MEDS_PAST_TOPLU_SIL=1` kaçışı, yalnız kullanıcı komutu). Model: `docs/VERI_MODELI.md` §4.

## H592 — `.gitignore`'daki ses dizinlerinde 2.809 MP3 hâlâ izleniyordu (2026-11-17)
- **Belirti:** depo 1,7 GB; `.gitignore`'a alınmış `data/k2*_cozucu/ses/` dizinlerinde ~200 MB MP3 her klonda/dağıtım worktree'sinde taşınıyor.
- **Kök neden:** `.gitignore` yalnız izlenmeyen dosyayı durdurur; kural eklenmeden önce işlenmiş dosyalar dizinde kalır. Kural eklenirken `git rm --cached` yapılmamıştı.
- **Çözüm:** `git ls-files -ci --exclude-standard | grep '\.mp3$'` → `git rm --cached` (dosyalar diskte duruyor). Önce doğrulandı: kod rsync'i `/data`'yı zaten dışlar, Oracle'da her kökte en az izlenen kadar MP3 var. `kayit.json` kayıtları izlenmeye devam ediyor.
- **Kural:** `.gitignore`'a dizin ekleyen aynı commit'te `git ls-files -ci --exclude-standard` boş mu diye bakar. Geçmişteki nesneler `.git`'te kalır; küçültmek geçmiş yeniden yazımı ister (kullanıcı kararı).
