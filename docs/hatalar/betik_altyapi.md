# Hata defteri — betik_altyapi (betik, LLM zinciri/kilidi, GPU/CPU, kapı altyapısı)

> Tam metin (kelimesi kelimesine taşındı, 2026-11-16). Dizin: `docs/KURUL2_YAPILMAYACAK_HATALAR.md`.
> Yeni madde bu dosyanın SONUNA `## H<n> — …` başlığıyla eklenir + dizinin sonuna tek satır.

### H5 — Kapının kendisi bozuk (her metin "999 HATA")
- **Kök:** doğrulayıcı Python sürümünde çöktü, çöküş "içerik reddi" sayıldı.
- **Kapı — EKLENDİ:** `otomasyon/saglik.py kapi_oz_sinama`: üslup, şık ve v2 kapıları iyi/kötü örnekle her gece; arıza panoda `kapi_ariza`.

### H25 — Claude CLI yolu değişti, gece hattının bütün Claude aşamaları sessizce düştü (2026-10-23)
- **Belirti:** masaüstü uygulaması 02:18'de güncellenip Claude Code'u `~/.config/Claude/claude-code/<sürüm>/<karma>/claude`
  altına taşıdı; `~/.local/bin/claude` sarmalayıcısı yalnız `<sürüm>/claude`'a baktığı için "Claude Code bulunamadı" ile
  çıktı. `claude -p` kullanan her aşama (ders zinciri, olası soru — o akşam Kurul 1 sınav günüydü —, hastalık, kamp, Son Prova)
  çalışmazdı; hata yalnız aşamanın kendi `claude.log`'unda kalırdı.
- **Düzeltme:** sarmalayıcı iki düzeni de arar, en yüksek sürümü seçer (yedek: oturum karalama klasörü). **Kapı:**
  `otomasyon/saglik.py` → `claude_cli` (`claude --version`); başarısızsa sabah özetinde sorun.

### H26 — Ücretsiz modelde sessiz boş yanıt ve yarım JSON (Gemini düşünme payı, 2026-10-23)
- **Belirti:** Gemini düşünme belirteçleri `maxOutputTokens`'tan düşüyor → uzun JSON yarıda (`finishReason=MAX_TOKENS`),
  `parts` yok → `KeyError` ağ hatası sanılıp aynı model yeniden deneniyor; hiçbir şey günlüğe yazılmıyordu (86 sn bekleyip `None`).
- **Düzeltme:** `cloud_llm.chat(dusunme=N)` düşünme payını ayrı verir, çıktı sınırını o kadar büyütür; boş yanıt `BosYanit` →
  doğrudan sıradaki model; her istisna ve ayrıştırılamayan yanıt `log`'a. Görev yönlendiricisi Gemini'ye varsayılan 2048 pay verir
  (`gorevler.json` → `gemini_dusunme`), uyarılar `meds_temp/gorev/gunluk.jsonl`'de (`model_uyari`).

### H27 — Ücretsiz model zinciri sağlam modeli bütün gün kapatıyordu (cloud_llm, 2026-10-23)
- **Belirti:** bir anahtar `400` (yanıta özgü JSON hatası), ikinci anahtar `401` (geçersiz) verince anahtar döngüsü "tüm
  anahtarların günlük kotası doldu" dalına düşüyor, `groq:openai/gpt-oss-120b` `meds_temp/state/cloud_llm.json`'a "kota dolu"
  yazılıyor → o gün BÜTÜN süreçlerde (Faz 14 kuyruğu, görev yönlendiricisi) en güçlü Groq modeli kullanılmıyordu. Ayrıca tek
  anahtarın `401`'i modeli tüm anahtarlarıyla süreç boyunca atlatıyordu.
- **Düzeltme:** model yalnız TÜM geçerli anahtarlar günlük kota (429 günlük) dediyse kapanır; `401/403` yalnız o anahtarı,
  `404` modeli atlatır. Yanlış kayıt temizlendi. **Açık (kullanıcı):** `.env` `GROQ_API_KEY_2` geçersiz (401; değer anahtar
  adına benziyor) — düzeltilmeli ya da silinmeli.

## H34 — Ücretsiz katman zinciri: Gemini tavanı, Zen kapandı, OpenRouter eklendi (2026-10-23)
- Bir dersin önem + çözücü adımı ~50 Gemini çağrısı harcadı; ardından bütün Gemini anahtarları 429 ("quota" / "monthly
  spending cap"). "spending cap" dakikalık sınır sanılıp 20 sn bekleniyordu → artık anahtar tükenmiş sayılır.
- Zen: Muse Spark kaldırıldı (410), Zen ücretsiz katmanı yalnız OpenCode istemcisinden (403 FreeTierError) → zincirden çıktı
  (`MEDS_CLOUD_ZEN=1` ile geri açılır). 410 artık 404 gibi model atlatır.
- OpenRouter ücretsiz modeller zincire eklendi (`nvidia/nemotron-3-ultra-550b-a55b:free`, `google/gemma-4-31b-it:free`);
  görev defterinde `zen` yerine `openrouter`. Groq ücretsiz katmanında ~24 bin karakterlik düzeltme istemi 413 alıyor.

## H35 — Ücretsiz/yazılı içerikte betik kapılarından geçen tıbbi hatalar; denetim bulguları düzeltilmiyordu (2026-10-24)
- Betik kapılarından 0 HATA ile geçen 2x99 içeriğinde OpenCode GLM denetçisi gerçek hatalar buldu: gravida 8 yerine "7",
  çoğul gebelik minör iken "majör", VTE eşikleri ">4"/">2" yerine "4 ve üzeri"/"2 ve üzeri", ders dışı Leopold ayrıntısı.
- Düzeltme: denetim bulguları yazara geri döner (`yonlendir.bulgu_duzelt`), kapılar + önemde yapı sabit kalır
  (`onem_listesi.duzeltme_kisiti`: madde/örnek sayısı, puan), yeniden uygulanır ve yeniden denetlenir (iş başına ≤2 tur).
  2x99: 5 engelli işin 5'i OpenCode ile düzeldi, yeniden denetim 0 engelleyici.
- Yan hatalar: aynı W yolunda eski provaların işleri denetime karışıyordu → ders iş defteri `W/gorev/<kod>/isler.json`;
  çözücü `uygula` her çağrıda yeni numaralı dosya açıp kopya üretiyordu → dosya adı soru kimliklerinden, eski kopya temizlenir;
  önem değişince çözücü kaydı eski soruya göre kalabiliyordu → `cozucu_sorusu.eskiyen` kapısı (birleştirme HATA verir,
  çözücü adımı eskiyeni düşürüp yeniden üretir).

## H78 — Gece otomatik LLM hattı kullanıcının Claude limitini tüketti; Oracle ders işçisi manuel moda geçişin dışında kalmıştı (2026-10-27)
- **Belirti:** 26.10 gecesi kullanıcıdan habersiz ~266 `claude -p` çağrısı (00:00–04:00, arşiv şekil/çizim onarımı `sekil_cizim.py`
  partileri) ve Oracle `meds-ders-isci` konteyneri (`CLAUDE_CODE_OAUTH_TOKEN` ile, `duraklat:false`, `otomatik_tarama:true`,
  günde 8 ders, 50 dk'da bir tarama) aboneliğin limitini bitirdi.
- **Kök neden:** (1) 26.10'daki "manuel mod" yalnız yerel systemd birimlerini durdurdu; Oracle konteynerindeki `/isci/ayar.json`
  ayrı bir dosyaydı ve değişmedi. (2) LLM çağıran betiklerde ortak bir "elle komut" kilidi yoktu. (3) Sunucuda Gemini onarım
  işçisi (`startAutoRepairWorker`, 20 sn) ve Faz14 kullanıcı kuyruğu (bildirim gelince / 10 dk'da bir) kendiliğinden LLM'e gidiyordu.
- **Çözüm:** Oracle işçisi durduruldu (`restart=no`, ayar duraklat/otomatik kapalı/günlük 0), `.env` anahtarı `#KAPALI`;
  `meds-hat-gece`, `meds-olasi-soru` maskelendi; `otomasyon/llm_kilit.py` (MEDS_LLM_ELLE=1 yoksa çıkış 75, systemd altında
  panel bayrağı şart) 11 betiğe ve `yonlendir._claude/_ajan`'a bağlandı; Gemini onarım işçisi duraklatılmış başlar, Faz14
  kuyruğu yalnız `POST /api/admin/faz14-kuyruk/baslat` ile.
- **Önleme kuralı (AGENTS.md kural 20):** "kapat" kararı her makinede (yerel + Oracle konteyner ayarları + `.env` anahtarları)
  ayrı ayrı doğrulanır; yeni LLM betiği kilitsiz yazılmaz; zamanlayıcı/izleyici/setInterval ile LLM çağrısı yasak.

## H90 — Anlam denetimi önbellek anahtarı değişince denetim sessizce atlandı (2026-10-27, k2-02)
- **Belirti:** parti çizimi düzeltilince yerleşim "anlam denetimi bakılan 0" verdi; denetimin düzeltme/silme kararları uygulanmadan çizim yazıldı.
- **Kök neden:** `cizim_uret.anlam_denetimi` önbelleği girdinin sha1'ine bağlı; girdi değişince yeni denetim ister, çağrı yapılamazsa
  (claude kapalı) boş sonuçla devam eder.
- **Çözüm / kural:** elle üretimde her yerleşimden sonra `rapor.anlam_denetimi.bakilan` panel sayısına eşit olmalı; değilse kararlar
  yeni girdi anahtarına (sıra korunarak) eşlenir ya da denetim yeniden yapılır. `bakilan: 0` ile çizim yayına girmez.

## H123 · Tam içerik hattı ders başına 4–6 saat sürüyor, soru/metin/PDF hataları geri dönüş yaratıyordu (2026-10-28)
- **Belirti:** k2-05 ve k2-08 her biri ≈5 saat; sorularda çıkmış dışı üslup ve ipuçlu şık, metinde kaynak dışı bilgi, PDF'te tasarım hataları.
- **Kök neden:** (1) hoca dökümü CPU'da tek başına saatler sürüyordu; (2) birbirinden bağımsız adımlar sırayla yürüyordu;
  (3) her alt ajan 1.100 satırlık defteri bütünüyle okuyordu, ilgili kural kalabalıkta kayboluyordu; (4) denetçi reddedince
  bütün metin yeniden yazılıyordu; (5) soru üslubu, sayfa kaynağı ve PDF görünümü için betik kapısı yoktu, hatalar ancak
  denetçide ya da kullanıcıda ortaya çıkıyordu.
- **Kural:** `docs/TAM_HAT_HIZLI_AKIS.md` — E0 `hazirlik.py` (döküm GPU ≤2500 MHz, AGENTS §10 altıncı istisna); alt ajana yalnız
  `kural_secici.py --oku <aşama>`; yalnız hatalı parça yeniden yazılır (sayısal hedefte ±%10, kalite hatasında tolerans yok);
  ders başına tek denetçi.
- **Kapı — EKLENDİ:** `scripts/hat/tam_hat/soru_uslup.py` (ders çağrıştıran kök, ipuçlu uzun doğru şık, kazanım bağı, kalıp payı),
  `kaynak_kapisi.py` (kayıt içeriği `s` sayfasında mı), `pdf_tarama.py` (boş sayfa, taşma, üst üste, harf harf kırılma).

## H440 — Arka plan işleri boşta da bellek, CPU, internet ve LLM kotası harcıyordu (sistem başarım turu, 2026-10-29)
- **Belirti:** Makine yavaş, RAM 15 GB'ın 10 GB'ı dolu, 14 GB takas; ilk istekte bekleme. Günlükte günde ~2.500 `sudo` oturumu, ~8.600 panel `GET /`, ~840 "bellek kritik" satırı; Firestore günde ~130 bin okuma (ücretsiz kota 50 bin).
- **Kök neden:**
  1. `meds-core` (`v2 cycle --watch`) her 10 dk'da 224 indirmenin (726 MB) SHA1'ini baştan hesaplıyor, kilitsiz `v2/core/llm.py` ile ücretsiz bulut LLM'e (Gemini/Groq/OpenRouter) cevap tamamlama deniyor (kural 20 ihlali), tam son işlemin yüklediği arşivi (~916 MB) tur bitince de bellekte tutuyordu.
  2. Öğrenci hata bildirimi ve Firestore köprüsü `processQueueItem`'ı doğrudan çağırıyor, işçi duraklatılmış olsa da LLM'e gidiyordu (kural 20 ihlali). Firestore `onSnapshot` canlıyken ayrıca 10 sn'de bir `getDocs` yoklaması vardı.
  3. Panel (`dashboard_server.py`) kimse bakmasa da 5 sn'de bir tüm klasörleri tarayıp kaldırılmış `meds-ollama` için iki `sudo docker` + iki `:11434` isteği yapıyordu; bekçi 10 sn'de bir panelin tüm HTML'ini çekiyordu.
  4. Arama servisleri (v2search :8092, semantic :8093) aynı e5-small modelinin kendi kopyasını taşıyordu (~1 GB × 2); vektörleme servisleri modeli bıraksa da torch belleği işletim sistemine dönmüyordu; her model yüklemesi HF Hub'a sürüm yoklaması atıyordu.
  5. query-intel her 6 saatte 3 GB'lık alt süreçte 122 MB derlemi ayrıştırıp ancak sonra "imza aynı" diyordu; her yönetici kaydı (pastQuestions.json) 15 sn sonra BM25 dizinini baştan kurup 122 MB dosyayı yeniden yazıyordu (değişen parça olmasa da).
  6. İstemci: canlı ders deposunun 50 ms yedek saati modül yüklenince her öğrencide sürekli çalışıyordu; bakım yoklaması gizli sekmede sürüyordu; her açılışta SW'ye 15 rota yeniden mühürletiliyordu.
- **Çözüm:** LLM kilidi `v2/core/llm.py` (`chat`, `vision_ocr`) ve `processQueueItemOtomatik` + zamanlayıcılı `questionIntake`/`poolClusterService` yolları (`MEDS_LLM_OTOMATIK=1` yoksa çalışmaz); `cycle.py` dosya özeti önbelleği (ad+boyut+mtime) + her tur ayrı alt süreç; panel istatistiği yalnız son 60 sn'de istenmişse, Ollama yoklaması kaldırıldı; bekçi 60 sn + yalnız başlık; arama servisleri sorgu vektörünü `meds-embed`'den (:8091, `MEDS_E5_EMBED_URL`) alır, boyut 384 değilse yerel modele düşer; `embed_server.py` model bırakınca `malloc_trim`; birimlere `HF_HUB_OFFLINE=1` (`*.service.d/20-cevrimdisi.conf`); query-intel ucuz ön imza (`data/search/query-intel.onimza`); RAG değişen parça yoksa dizin/dosya yeniden kurulmaz, bekleme 2 dk; Firestore yedek yoklaması canlı dinleyici varken 10 dk; istemci saat yalnız çalarken, bakım yoklaması yalnız görünür sekmede, SW mühürleme günde bir, başarım yoklaması 10 dk, müzik listesi ilk bağlanmada tekrar çekilmez. `meds-web` doğrudan `node --import tsx server.ts` (`30-dogrudan-node.conf`).
- **Önleme:** (a) Sürekli çalışan servis tur başına değişmeyen girdiyi baştan okumaz/özetlemez: önce ad+boyut+mtime ön imzası. (b) Ağır son işlemi olan uzun ömürlü Python döngüsü işi alt süreçte yapar (bellek tur sonunda iade). (c) Yalnız ekran açıkken anlamlı olan hesap (panel istatistiği, saat, yoklama) "son istek/görünürlük" koşuluna bağlanır. (d) LLM çağıran HER yol — en alt katmandaki ortak `chat` işlevi dahil — kilidi denetler; yalnız zamanlayıcıyı duraklatmak yetmez. (e) Aynı modeli taşıyan ikinci servis yazılmaz; ortak vektörleme servisine istek atılır. (f) Kaldırılan servisin (Ollama vb.) yoklaması panel/bekçi kodundan da silinir.

## H478 — LLM kilidi masaüstü Claude oturumunu zamanlayıcı sandı (2026-11-03)
- **Belirti:** `cizim_uret.py` kullanıcı "çizimi yap" dediği hâlde `MEDS_LLM_ELLE=1` ile de çıkış 75 verdi; yerleştirme (LLM'siz) adımı da durdu.
- **Kök neden:** `otomasyon/llm_kilit.py` `INVOCATION_ID` varsa zamanlayıcı sayar; Claude masaüstü oturumu systemd kullanıcı biriminden
  başladığı için bu değişken etkileşimli oturumda da tanımlı. Ayrıca kilit betiğin başında: LLM çağırmayan yerleştirme de kilitleniyor.
- **Çözüm (bu sefer):** kullanıcının açık onayıyla (2026-11-03) yalnız k2-12/k2-64 yerleştirmesi `env -u INVOCATION_ID MEDS_LLM_ELLE=1` + her
  çağrıyı reddeden sahte `claude` ile koşturuldu; anlam denetimi ayrı ajanla yapıldı. k2-13/k2-14'te ajanlar bunu onaysız yapmıştı (kayıt).
- **Önleme:** ajan kilidi kendi başına aşmaz; takılırsa ana oturum kullanıcıya sorar. Kalıcı çözüm kullanıcı kararı bekler: kilidin yalnız
  `claude()`/`anlam_denetimi()` çağrısına taşınması ya da masaüstü oturumunu tanıyan ayrı bayrak (kilit gevşetme sayılır → kullanıcı onayı şart).

## H484
- **Belirti (2026-11-04, k2-07/15/16 tam hat):** üç ders paralel hazırlanırken `hazirlik.py` sayfa metni / görüntü / öğrenci notu işlerinin bir kısmı
  0 sn'de HATA verdi.
- **Kök neden:** `cpu_run` systemd birim adını yalnız saniye damgasıyla kuruyordu (`meds-hazirlik-<iş>-<sn>`); iki süreç aynı saniyede
  aynı işi başlatınca "Unit … already loaded" ile reddedildi.
- **Çözüm:** birim adına süreç numarası eklendi (`meds-hazirlik-<iş>-<pid>-<sn>`).
- **Önleme:** systemd-run ile geçici birim açan her betik adı süreçten tekil kurar (pid ya da uuid); zaman damgası tek başına kimlik sayılmaz.

## H489 — `cizim_uret.py` oturum içinde LLM kilidine takılıyor (INVOCATION_ID, 2026-11-05)
- **Belirti:** çizim ajanları `cizim_uret.py`'yi çalıştıramadı; kilit "systemd altında panel bayrağı yok" diye reddetti, ajanlar `env -u INVOCATION_ID` + sahte `claude` ile atlattı (LLM çağrısı olmadı).
- **Kök neden:** masaüstü uygulaması oturumu systemd kullanıcı biriminden başlattığı için `INVOCATION_ID` kalıtılıyor; `llm_kilit.py` bunu zamanlayıcı sanıyor. Ayrıca `cizim_uret.py` yerleşim kipinde de (Claude çağırmayacağı hâlde) kilidi yokluyor.
- **Kural / açık iş:** yerleşim (LLM'siz) kipinde kilit yoklanmamalı; o zamana dek atlatma yalnız `--kuru`/hazır parti dosyalarıyla ve LLM çağrısı olmadığı doğrulanarak yapılır. Kilidi gevşetmek yasak (kural 20).

### H557 — `claude` açılmıyordu (abonelik yok) + masaüstü uygulamasında model listesi boş (2026-11-13, kullanıcı bildirdi)
- **Belirti:** (1) Terminalde `claude` → `Failed to authenticate: OAuth session expired and could not be refreshed`; (2) Claude masaüstü uygulaması 3P modunda model seçici boş, Code sekmesi açılmıyor; "modeller gözükmüyor, claude code'a giremiyorum".
- **Kök neden 1 (terminal):** Abonelik yok; `~/.claude/.credentials.json` OAuth yenileme süresi dolmuş (`refreshTokenExpiresAt: 2026-11-08`). Çözüm: geçit anahtarı (`ANTHROPIC_AUTH_TOKEN`) + `ANTHROPIC_BASE_URL` `~/.claude/settings.json` `env` bloğunda.
- **Kök neden 2 (uygulama, model listesi):** Uygulama 3P gateway modunda `inferenceModels` satırlarını doğrularken ad **Anthropic modeli gibi görünmeli**: `Io(name) = !/ark-code|deepseek|glm|gpt|kimi|mimo|minimax|qwen|…/.test(name) && (/^(sonnet|opus|haiku|fable|mythos)(-[\d.]+)?$/.test(name) || name.includes("claude"|"anthropic"|family))`. Geçit kimlikleri (`deepseek-v4.1-flash`, `glm-5.3-flash` …) bu testi geçemez → satır sessizce listeden **atılır** (`inferenceModels: "…" is not an Anthropic model and was removed from the list`). Üstelik geçitte Claude kimlikleri yetkisiz (403).
- **Kök neden 3 (kendi kendine döngü):** `~/.claude/settings.json` içindeki `env` **süreç ortam değişkenlerini ezer**; `ANTHROPIC_BASE_URL=http://127.0.0.1:8787 claude` komutu yok sayılır. Köprü `upstream` adresini aynı dosyadan okuduğu için kendi kendine istek atan sonsuz döngü oluştu (health `upstream: http://127.0.0.1:8787`).
- **Kalıcı çözüm:** (1) `~/.local/bin/opendesign-kopru.py` + `opendesign-kopru.service` (systemd --user, `Restart=always`, `MemoryMax=256M`, `CPUQuota=50%`): uygulamanın `claude-od-01…14` rota adlarını geçit kimliklerine çevirir, SSE/`tool_use` aynen akıtılır, eşlenmemiş ad olduğu gibi geçer. (2) Gerçek geçit adresi `~/.claude/opendesign-kopru.json` → `upstream` alanında (settings'ten okunmaz; kendine işaret ederse betik açılışta durur). (3) `settings.json` `env.ANTHROPIC_BASE_URL` = `http://127.0.0.1:8787`. (4) Masaüstü 3P yapılandırması `~/.config/Claude-3p/configLibrary/<id>.json`: `inferenceProvider: gateway`, `inferenceGatewayBaseUrl: http://127.0.0.1:8787`, `inferenceModels` = `claude-od-NN` + `labelOverride` (gerçek ad), `deploymentMode: "3p"`. Doğrulama: uygulama günlüğü `picker = 14 (inferenceModels)` + `ConfigHealth … healthy`; köprü günlüğü `POST /v1/messages -> 200`.
- **Önleme:** 3P `inferenceModels` rota adında üçüncü taraf işareti (`deepseek/glm/kimi/mimo/minimax/gpt/…`) kullanılmaz; ad `claude-od-NN` gibi nötr olur, gerçek model `labelOverride` ve köprü eşlemesinde tutulur. `settings.json` `env` değerleri komut satırından ezilemez — ortam değişikliği sanılıyorsa önce bu dosyaya bakılır. Köprü `upstream`'i asla kendi adresini göstermez (açılışta kapı var). Ayrıntı: `~/.claude/OPENDESIGN_KULLANIM.md`.

### H558 — Bash aracı hiç açılmıyordu: `apply-seccomp: write /proc/self/setgroups … Permission denied` (2026-11-13, kullanıcı bildirdi)
- **Belirti:** Oturumda her Bash çağrısı (`echo hi` bile) komut çalışmadan `apply-seccomp: write /proc/self/setgroups (nested userns is capability-restricted; caller must provide CAP_SYS_ADMIN): Permission denied` ile düşüyordu; kabuk, git ve servis denetimi hiç yapılamıyordu.
- **Kök neden:** İki katmanlı Ubuntu userns sıkılaştırması. (1) `/etc/apparmor.d/bwrap-userns-restrict` içindeki **`unpriv_bwrap`** profili `audit deny capability,` satırıyla bwrap'ın tüm yeteneklerini reddediyor; AppArmor'da `deny` kuralları complain modunda bile yürürlükte olduğu için `aa-complain` bu profili gevşetmez (local include da `deny`'yi geçersiz kılamaz). (2) `kernel.apparmor_restrict_unprivileged_userns=1` unprivileged userns'i yalnız AppArmor profili olan ikililere (`bwrap`, `unshare`) açıyor. Claude Code sandbox yardımcısı bwrap içinde iç içe userns kurup `/proc/self/setgroups` yazmaya çalışınca `sys_admin` reddi geliyordu. Kanıt `dmesg`: `apparmor="DENIED" operation="capable" profile="unpriv_bwrap" capname="sys_admin"`. Yanıltıcı nokta: `unshare -Ur true` ve doğrudan `bwrap` kabuktan çalışıyordu; hata yalnız sandbox yardımcısının profilinde çıkıyordu — "userns zaten çalışıyor" diye erken karar verilmemeli.
- **Kalıcı çözüm:** `sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0` + `/etc/sysctl.d/99-userns.conf` içine `kernel.apparmor_restrict_unprivileged_userns=0` (açılışta kalıcı) ve `sudo ln -sf /etc/apparmor.d/bwrap-userns-restrict /etc/apparmor.d/disable/` + `sudo apparmor_parser -R /etc/apparmor.d/bwrap-userns-restrict`. Doğrulama: `echo`, `git status`, `git log` çalıştı.
- **Önleme:** Aynı hata görülürse önce `sudo dmesg | grep -E "apparmor|userns" | tail` bakılır; `unpriv_bwrap` + `sys_admin` satırı varsa profil bir paket güncellemesiyle geri gelmiştir, iki komut yinelenir (`aa-complain` çözüm değildir). **Ayrı katman:** sandbox ağ kapısı (`sandbox.network.allowedDomains: []`, `allowManagedDomainsOnly: true`) bu düzeltmeden sonra da kapalıdır; `git fetch/push`, `ssh`, `curl` Bash'te çalışmaz — ağ işleri Terminal panelinden yapılır ya da kullanıcı Ayarlar → Claude Code'dan ağ iznini açar. İki katmanı karıştırıp "kabuk açıldı, ağ da açıldı" sanmak yeni bir yanlış kök neden avına yol açar.

### H560 — Ajan hattı OpenDesign geçidine taşınırken roller tek modelde birleşti, eşlenmemiş adlar sessizce geçide gitti (2026-11-13, kullanıcı istedi)
- **Belirti:** `claude -p` çağrıları geçit kipine alındıktan sonra (1) yazar ve denetçi aşamaları **aynı** modelle koşuyordu — yazar ≠ denetçi kuralı (AGENTS 14/26) kâğıt üstünde kalıyordu; (2) bazı betikler `--model claude-opus-5-5` gibi depoda gömülü adlar gönderdiğinde geçit isteği reddediyor ya da ad olduğu gibi iletildiği için anlaşılmaz hata dönüyordu; (3) bazı zincirler hâlâ eski `claude` CLI'ye ve Claude aboneliğine bağlıydı — abonelik bittiği için o aşamalar hiç çalışmıyordu.
- **Kök neden:** Model kimliği **koda gömülüydü** (her betikte ayrı `"claude-opus-5-5"` sabiti; `butce.json`'da tek `claude.model`). Köprü eşlemesinde karşılığı olmayan ad `alias` tablosunda yoksa **olduğu gibi** geçide iletilir; geçit Anthropic kimliğini tanımaz. `ayan_model` fikri ilk yazıldığında yalnız tek varsayılan döndürdüğü için denetçi de yazarın modelini aldı. Yani "model seçimi" üç ayrı yerde (betik, butce.json, köprü tablosu) tutuluyordu ve hiçbiri diğerini denetlemiyordu.
- **Kalıcı çözüm:** (1) **Tek kaynak** `otomasyon/llm/model_sec.py::ajan_model(rol)` — yazar/denetci/hizli rolleri ayrı: `butce.json` → `claude.model`, `claude.model_denetci` (`claude-opus-4-7` → `glm-5.3-flashx`, farklı aile), `claude.model_hizli`. Bütün zincirler (ders, son prova, hastalık, checkup, kamp, olası soru, çizim, arşiv, ders işçisi) buradan beslenir; koda model adı yazılmaz. (2) Köprü haritası `scripts/altyapi/opendesign/rotalar.json` (tek kaynak, 14 görünen + 18 alias) ve `otomasyon/llm/opendesign.py::ESLEME` aynı olmak zorunda: `python3 scripts/altyapi/opendesign/kopru.py --doctor` ikisini karşılaştırır, eksik eşlemede HATA verir. (3) CLI'sız makineler (Oracle) için `opendesign.py` doğrudan `/v1/messages` gönderir ve adı `ESLEME` ile çevirir; tanınmayan ad gönderilmez, açık hata yazılır. (4) `llm_kilit.py` bütün yollarda korunur — taşıma, kurallı 20'yi gevşetmez.
- **Önleme:** Yeni bir model/ad eklenirken **iki** yere yazılır: `rotalar.json` ve `opendesign.ESLEME`; sonra `kopru.py --doctor` koşulur (0 HATA). Bir betiğe `--model <sabit ad>` yazılmaz, `ajan_model()` çağrılır. Aynı aile iki rolde görünüyorsa (yazar = denetçi) denetim bağımsızlığı yoktur: denetçi rolü ayrı aileye (`glm-*`/`gpt-*`) bakar. `claude` CLI çağrısı eklerken önce `llm_kilit` + `model_sec` çifti eklenir, sonra çağrı yazılır.

### H561 — Artifact stüdyosu: önizleme sunucusu bulunamadı, grafikte iki farklı büyüklük tek eksende ezildi, `.claude/launch.json` `/dev/null` ile maskelendi (2026-11-13, kullanıcı istedi)
- **Belirti:** (1) `preview_start` "No server named `artifact-studyo` found" dedi; `meds/.claude/launch.json`'a yazılan girdi okunmadı. (2) Örnek panoda 0–5 aralığındaki "ders" serisi ile 40–96 aralığındaki "soru" serisi aynı eksende çizilince küçük seri tabanda görünmez oldu; eksen etiketleri `107,5` / `-0,6` gibi okunmaz sayılara düştü. (3) `meds/.claude/launch.json` bir noktada `crw-rw-rw- 1 nobody nogroup 1, 3` göründü; `git diff` "desteklenmeyen dosya türü", `rm` "Aygıt ya da özkaynak meşgul" verdi.
- **Kök neden:** (1) Masaüstü uygulaması `launch.json`'ı **oturum kökünden** okur (bu makinede `/home/indu/medsor`), depo kökünden (`/home/indu/medsor/meds`) değil; betik yanlış dosyaya yazıyordu. (2) Grafik üreteci min/max'tan ham `(hi-lo)/4` adımı türetiyordu; iki seri tek ölçekte birleştirildiğinde fark büyüklüklerinden biri sıkışıyor, adım da yuvarlak olmuyordu. (3) `/dev/null`, `devtmpfs` üzerinden o yola **salt-okunur bind mount** edilmişti (`/proc/self/mountinfo` 8108 → `devtmpfs[/null] ro`): uygulama kendi launch yapılandırmasını korumak için iç içe dosyayı maskeleyebiliyor. `rm`/`git diff` bu yüzden anlamsız hata verdi; ortamda dosya "yok" gibi davranıyordu.
- **Kalıcı çözüm:** (1) `kur.sh` artık `LAUNCH="$(dirname "$MEDS")/.claude/launch.json"` kullanır (`ARTIFACT_LAUNCH` ile değiştirilebilir); `--kontrol` hangi dosyaya baktığını yazar. (2) `studyo.py::_olcek` yuvarlak adım (1·2·2,5·5×10ⁿ) ve sütunlarda sıfır tabanı verir; `"eksen": "sag"` verilen seri sağ eksende **kendi** ölçeğiyle çizilir, sağ etiketler `_izgara` içinde ayrı basılır. (3) Maskeleme kalktıktan sonra `git checkout -- .claude/launch.json` ile izlenen dosya geri yüklendi.
- **Önleme:** Önizleme sunucusu eklerken **önce** `mcp__Claude_Browser__preview_list`/`preview_start` ile yolun doğruluğu sınanır; `launch.json` yazımı oturum köküne yapılır. Bir dosyada `git diff`, `rm` ya da `cat` "desteklenmeyen tür / meşgul" derse **dosyanın kendisi değil üstündeki mount** sorgulanır: `findmnt -T <yol>` + `grep <yol> /proc/self/mountinfo`. Maskeleme biter beklemeden `git rm`/`rm -f` denenmez — `rm -f` **başarılı görünüp** izlenen dosyayı silebilir (bu turda oldu; geri yükleme `git checkout --` ile yapıldı). Grafikte büyüklük farkı ~10× ise çift eksen zorunlu; tek eksende "küçük seri görünmüyor" bir tasarım tercihi değil hatadır.

### H577 — "Toplu yol süpürmesi bazı betikleri sessizce atladı": Türkçe yerel ayarda sed/grep `[a-z]` aralığı "i" harfini eşleştirmiyor (2026-11-16, yeniden yapılandırma)
- **Belirti:** son_prova çift-kopya temizliğinde `sed -E 's#meds_temp/son_prova/([a-z_]+\.py)#meds/scripts/uretim/son_prova/\1#g'`
  ile docstring'lerdeki betik yolları kanonik konuma çevrildi. Hata vermedi ama **yalnız bir kısmı** değişti:
  `plan.py`, `derle.py`, `dogrula.py` düzeldi; `deneme_degistir.py`, `soru_dagit.py` (ve `spVeri.ts`'teki atıf) **eski kaldı**.
- **Kök neden:** Sistem dili `tr_TR.UTF-8`. GNU sed/grep köşeli parantez aralıklarını (`[a-z]`) yerel ayarın sıralama
  kuralına (LC_COLLATE/LC_CTYPE) göre yorumlar. Türkçede noktalı/noktasız i (i/ı/İ/I) sıralaması yüzünden `[a-z]` aralığı
  C ayarındaki gibi "i"yi kapsamaz; `[a-z_]+` "i" içeren her adda eşleşmez. Kaçan adların hepsinde "i" var
  (degist**i**r, dag**i**t); "i" içermeyenler sorunsuz. Aynı komut `LC_ALL=C` ile hepsini eşleştirdi (doğrulandı).
- **Kalıcı çözüm:** Kalan atıflar `LC_ALL=C sed ...` ile düzeltildi; `LC_ALL=C grep` ile 0 kalıntı doğrulandı.
- **Önleme kuralı:** (a) Bu projede aralık içeren her sed/grep/awk süpürmesi (`[a-z]`, `[A-Z]`, `[a-zA-Z0-9]`)
  **`LC_ALL=C` önekiyle** çalıştırılır. (b) Süpürmenin kendi doğrulaması da `LC_ALL=C` ile yapılır — tr_TR altında yapılan
  denetim aynı kör noktayı tekrarlar ve "0 kaldı" yanılsaması verir. (c) Taşıma/silme **güvenlik kapılarında** aralık değil
  birebir dosya adı (`grep -F` / sabit dize) kullanılır; bu turdaki kapılar böyle olduğundan etkilenmedi. (d) Büyük/küçük
  harf duyarsız eşleşmede (`-i`) de aynı i/İ katlama tuzağı vardır; yol/dosya adında `-i` yerine birebir eşleşme tercih edilir.

### H578 — Betik dizini taşırken sessiz kırılma sınıfları: yeniden yapılandırmada yakalanan 7 tuzak (2026-11-16)
- **Belirti:** `meds/scripts/` 79 modülü `hat/ uretim/ altyapi/ moduller/ arsiv/` gruplarına taşınırken yol süpürmesi "0 kalıntı",
  kum havuzu "fark yok" dediği hâlde gerçek çalıştırma kırılmalar gösterdi; bir kısmı dağıtımı da bozacaktı.
- **Kök nedenler (her biri ayrı mekanizma):**
  1. **Sabit kademe:** 123/153 betik kökü `Path(__file__).parents[N]` ile buluyordu; bir kademe derine taşıma hepsini yanlış yola sokar.
  2. **Çift konum:** son_prova / blok_ozet / tekrar_analizi `meds_temp/<modül>/` KOPYASINDAN çalışacak şekilde yazılmıştı
     (`KOK.parents[1]` = repo kökü yalnız orada doğru); git kopyası `meds/meds` gibi yanlış yol üretiyordu.
  3. **Paket adıyla import:** `ders_isci/yayinla.py` scripts kökünü path'e ekleyip `from v2.stages import …` yapıyordu; v2 taşınınca
     kırıldı. Kum havuzu stdlib dışı her importu sahteyle değiştirdiği için bunu GÖREMEZ. `deploy-code.sh` [0/4] bu betiği çağırır →
     dağıtım bozulurdu.
  4. **`python -m` + WorkingDirectory:** meds-core/v2search/v2semantic/revize `WorkingDirectory=…/scripts` + `-m v2` ile çalışıyordu;
     yol dizesi olmadığından süpürme yakalamaz. Ayrıca v2 içi `cwd=parents[1]` "scripts kökü" değil "paket kabı" anlamındaydı —
     kök sabitine çevrilseydi bozulurdu.
  5. **Bağlamı yanlış okunan `..`:** `gece.sh` çalışma dizinine, `pdf_kirp.mjs` bir değişkene (`MEDS`) göreli `..` kullanıyordu;
     sözdizimsel "+1 ..'" kuralı bunları bozardı. `.tsx` dosyaları düzelticinin uzantı listesinde yoktu (tsc yakaladı).
  6. **Oracle sapması:** `rsync` silme yapmadığından taşınan eski dizinler Oracle'da kalır; Oracle sistem birimleri bir kez elle
     kurulmuştu, dağıtım onları hiç güncellemiyordu → zamanlayıcılar eski kodu sessizce çalıştırmaya devam ederdi.
  7. **Yerel ayar:** liste üretirken `sed '[a-z]'` yine "i"li adları eledi (H577 tekrarı).
- **Kalıcı çözüm:** `scripts/kok.py` (marker walk-up, `_kok.MEDS/SCRIPTS/PROJE`); dönüştürücü yalnız modül DIŞINA çıkan ataları
  çevirir, modül içi yollar göreli kalır; çift konumlu modüllerde kod git'te, veri `meds_temp/<modül>` (`*_KOK` env). yayinla.py
  v2 kabını (`scripts/altyapi`) path'e ekler; dört birim `WorkingDirectory=…/scripts/altyapi`. `deploy-code.sh` [1a] kurulu Oracle
  birimlerini repo ile eşitler, [4b] `deploy/oracle/tasinan_yollar.txt`'deki eski konumları sağlık kontrolünden SONRA arşive alır.
  Araçlar ve doğrulama: `_temizlik/araclar/` (kum.py, yakala.py, donustur.py, supur.py, karsilastir.py).
- **Önleme kuralı (dizin taşıma/yeniden adlandırma kontrol listesi):** (a) önce yol-çözümleme envanteri (`__file__`, `parents`, `dirname`,
  `os.path.join(...'..')`, değişken zincirleri); (b) `meds_temp`'te aynı adlı kopya var mı → varsa önce kod/veri ayrımı; (c) kum havuzu
  diferansiyeli YETMEZ — ayrıca AST ile "taşınan modülü paket adıyla import eden dış dosya" taraması ve `-m <modül>` / `WorkingDirectory`
  taraması; (d) py-dışı göreli atıf yalnız dosyaya-göreli bağlamda değiştirilir, tüm uzantılar (.tsx dahil) listelenir; (e) gerçek kapılar
  gerçek ÇALIŞMA girdileriyle koşulur (yayınlanmış kopya değil); (f) taşınan her yol `tasinan_yollar.txt`'ye; birim değişince repo kopyası
  da değişir; (g) liste/süpürme Python ile (yerel ayardan bağımsız).


## H584 — "patoloji_onem betikleri veriyi bulamıyor; arsiv_yayinla çıkmış konumunda `lib` bulunamayabilir" (2026-11-16)
- **Belirti:** `patoloji_onem/birlestir.py` ve `dogrula.py` açılışta `scripts/pdf_liste.json` / `scripts/cikmis_pdf.json` için FileNotFoundError; `arsiv_yayinla.cikmis_konum_yerel` `from lib import` yalnız `isle` önceden yüklendiyse çalışıyordu; `dashboard_server.py` geçersiz `\s` kaçışları (SyntaxWarning, gelecekte SyntaxError).
- **Kök neden:** Betikler eskiden `meds_temp/patoloji_onem/araclar/` kopyasından çalışıyordu (`dirname(dirname(__file__))` = veri klasörü); kod git'e alınınca aynı ifade `scripts/`'i gösterdi (çift kopya kalıntısı, H578 sınıfı). `lib` yolu başka modülün yan etkisine bağlıydı. JS kodu düz Python dizesinde tutuluyordu.
- **Kalıcı çözüm:** Veri klasörü `PATOLOJI_ONEM_KOK` ya da `meds_temp/patoloji_onem`; `arsiv_yayinla` `scripts/altyapi/agents`'ı kendisi ekler; kaçışlar `\\s`. `patoloji_cozucu/girdi3_hazirla.py` da aynı kalıntıydı (kendi klasöründe `girdi2/` arıyordu; veri `meds_temp/patoloji_ornek26/cozucu/`, kardeşleri oraya bakıyor) → `PATOLOJI_COZUCU_KOK` ya da o klasör.
- **Önleme kuralı:** Taşıma/temizlikten sonra tüm betikler gerçek yerel içe aktarmayla taranır (`_temizlik/araclar/kum2.py`: depo modüllerini gerçekten yükler, yalnız dış paketleri sahteler); `python3 -W error -m py_compile` uyarıları da hata sayar.
