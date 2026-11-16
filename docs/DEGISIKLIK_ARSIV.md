# Değişiklik kaydı — arşiv

> Eski bölümler buraya taşındı (oturum açılış token tasarrufu, 2026-11-16). Güncel kayıt `DEGISIKLIK_KAYDI.md`.

## 2026-11-15 — Soru dışa aktarıcı PDF: sayfa kutusu kâğıttan kısa basıldı, alt bilgi üstüne binmesi yapısal olarak kapatıldı (H576, onem 722, kullanıcı bildirdi)
- **İstek:** "Alt bilgi satırında sayfa sayısı bilgisi yazsa bile bir katman oluşturup diğer metnin üstünü kaplayarak sorun teşkil ediyor." (Çıktı türü: PDF dosyası.)
- **Kök neden:** `.pg`/`.yp` kutusu `@page` ölçüsüne eşit kuruluyordu. HTML'de alt bilgi akış içinde olduğundan üstüne binemez; ama Chrome baskı dizgisi kutuyu yarım piksel büyütürse kutuyu parçalayıp taşanı SONRAKİ basılı sayfanın içeriğinin üstüne basar (sayfa sayısı değişmez). Alt bilgi en altta olduğundan en sık o taşar.
- **Çözüm:** `belge.ts`: `.pg` ve `.yp` yüksekliği `${ölçü − 0,25 mm}`. Kutu her zaman kâğıda sığar; baskı parçalaması olanaksızlaşır. `npm run lint` 0 hata, `npx vite build` ✓.
- **Kural:** Sabit sayfa kutusu kâğıda eşit ölçülmez; "eşit" yuvarlamada "büyük" demektir. Ayrıntı: `docs/KURUL2_YAPILMAYACAK_HATALAR.md` H576.
- **Dosya:** `src/components/v15/soruAktar/belge.ts` (yalnız).

## 2026-11-15 — Soru dışa aktarıcı PDF: sıfır boşluklu gövdeye baskı toleransı (H575, onem 721, kullanıcı bildirdi)
- **İstek:** "Soru dışa aktarıcıda PDF oluştururken sayfanın alt kısmında soruların veya şıkların metinlerinin kesik kalması veya görüntülenmemesi sorunu devam etmekte." (H572 düzeltmelerinden sonra tekrar bildirdi.)
- **Kanıt:** Canlı sitede gerçek "PDF indir" akışı dört kipte birebir yinelendi (varsayılan akış 2.345 sayfa, 4'lü ızgara 2.953, kitapçık 1.174, sayfaAlti 672): DOM taşması 0, pdftotext boşluksuz karşılaştırmada önizlemedeki 60 sorunun kök+şık metinlerinin tamamı PDF'te, sayfa alt 30 pt'sine giren sözcük 0. Yayın bu kiplerde metin kaybetmiyor; kalan risk: Chrome baskı dizgisi ölçümden 1–2 px farklı dizebilir, sıfır boşluk + `overflow:hidden` ile son satır sessizce kırpılır.
- **Çözüm:** `ayar.ts`: `BASKI_PAY_MM = 1.2`; `govde()` gövde yüksekliğinden bu payı düşer. Önizleme/PDF/DOCX/PPTX aynı fonksiyonu kullandığından üç çıktı birlikte kayar. `npm run lint` 0 hata, `npx vite build` ✓.
- **Kural:** "Tam dolu sayfa + `overflow:hidden`" kırpma demektir; sabit ölçülü gövde baskı toleransı taşır. Sınama yöntemi (ihracat HTML'i yakala → bağımsız Chrome'da bas → pdftotext boşluksuz karşılaştır + `-bbox` alt kenar taraması) H575'te kayıtlı.
- **Dosya:** `src/components/v15/soruAktar/ayar.ts` (yalnız). Ayrıntı: `docs/KURUL2_YAPILMAYACAK_HATALAR.md` H575.

## 2026-11-14 — Soru dışa aktarıcı: çökme + PDF'te kesilen/üst üste binen metin; "sayfayı yenile" döngüsü (H572–H574, onem 720, kullanıcı bildirdi)
- **İstek:** "Soru dışa aktarıcıda bazen kullanıcılara hatalar geliyor ve sayfayı yenilemesi isteniyor, kaynak sorunu bul ve çöz. Ayrıca PDF içeriğinde sayfanın altında içerik kesik kesik yazılabiliyor, tam verilemiyor ve kayboluyor… alt bilgilendirme yeri ile üst üste biniyor. Bu tarz hataları da çöz ve dağıt."
- **Kök neden (çökme):** Canlı `data/istemci_hatalari.jsonl`'de `/sorular/disa-aktar` için `undefined is not an object (evaluating 'xt[t.palet].renk')` (yığın `chunk-belge` → `useMemo` → `chunk-SoruAktarV15`). `renkHaritasi` paleti doğrudan `PALETLER[a.palet].renk` ile okuyordu; localStorage/şablondan gelen tanınmayan palet değeri tüm ekranı düşürüp "sayfayı yenile" ekranını çıkarıyordu.
- **Kök neden (üst üste binme / kesilme):** `govde()` ve CSS başlık bandını sabit 16 mm, alt bilgiyi sabit 7 mm varsayıyordu. 24 mm logo başlıktan 9 px taşıp gövdeyle çakışıyordu; uzun alt bilgi `nowrap` ile tek satırda kesiliyordu (üç bölgenin üçü de); uzun başlık 438 px taşıyordu; ızgarada hücreye sığmayan soru `overflow:hidden` ile sessizce kırpılıyordu (8'li düzende 371 px).
- **Çözüm:** Palet erişimi `paletRenkleri`/`paletNormal`e alındı (tanınmayan → Canlı, boş palette `a.vurgu`). `baslikYukMm()`/`altYukMm()` gerçek yüksekliği verir; HTML, DOCX ve PPTX aynı fonksiyonu kullanır. Alt bilgi iki, başlık iki satıra kadar sarar; kapak taşması `overflow:auto`, çerçevesiz kapağa 8 mm iç boşluk. Izgarada sığmayan soru kırpılmaz: belgenin sonunda tam genişlik "Sığmayan sorular" akışına alınır (`zorunluAkis`), tamamen boş ızgara sayfası üretilmez, uyarı "ayrı sayfaya alındı" der.
- **"Sayfayı yenile" döngüsü (H573):** Hata sınırı ve `vite:preloadError` yalnız `location.reload()` diyordu; service worker eski kabuğu geri verince aynı ekran kalıyordu. Yeni `kabukOnbelleginiTazele()`: bekleyen SW'yi etkinleştirir, çevrimdışı ders/PDF paketleri korunarak kabuk ve sürümsüz kopyaları önbellekten siler; yenileme ondan sonra yapılır. `preloadError` artık `preventDefault()` eder (Vite'ın kendi reload'uyla yarışmaz).
- **Oyun masası çökmesi (H574):** `/sorular/oyunlar` için 13 kayıt: `MasaUstCubuk` içinde `oyuncular.filter` (`oyuncular` dizisi yok) ve `o.cezalar.map`. `Array.isArray` korumaları eklendi; `MasaSonuc`, `okey/Rakipler`, `okey/OkeyMasa` da aynı korumaya alındı.
- **Sınama:** `npm run lint` 0 hata, `npx vite build` ✓. Tarayıcıda beş senaryo (varsayılan, 24 mm logo + uzun alt bilgi, uzun başlık, 40 mm not alanı + şerit, sade kapak) render + ölçüm → `hatalar: []`. Logo senaryosunda yerleşim: başlık 0–98, gövde 98–977, alt bilgi 977–1009 (çakışma yok). Bozuk palet (`'yokolan-palet'`, elle `'BOZUK'`) çökmeden Canlı'ya düşüyor. 200 gerçek soruda sayfa sayıları değişmedi (akış 42, 2'li 120, 4'lü 70, 8'li 45), boş sayfa 0.
- **Kural:** `PALETLER[...]` doğrudan indekslenmez; kullanıcı ayarına bağlı yükseklikler `baslikYukMm`/`altYukMm`den gelir ve üç çıktı aynı fonksiyonu çağırır; soru kutusunda `overflow:hidden` kırpma demektir — sığmayan blok taşınır, kırpılmaz. Ayrıntı ve önleme: `docs/KURUL2_YAPILMAYACAK_HATALAR.md` H572–H574.

## 2026-11-13 — Claude aboneliği yerine OpenDesign modelleri: ajan hattı, site AI'sı, eklentiler ve yerel artifact stüdyosu (H560/H561, onem 716, kullanıcı istedi)
- **İstek:** "Artık Claude yerine OpenDesign'a ait DeepSeek ve diğer modeller kullanılacak; kodları buna göre düzelt ve geliştir. Gerekli plugin, eklenti, script, skill indirilsin kurulsun; tüm eski işlevler çalışsın; kodlama/tasarım hatasına karşı eklentiler eklensin; artifact design özelliği Claude'a eklensin."
- **Kapsam (kullanıcı seçimi):** (1) ajan hattı + sitenin AI sağlayıcısı OpenDesign'a taşınır, (2) claude.ai Artifact 3P geçit kipinde çalışmadığı için eşdeğeri **yerel artifact stüdyosu** olarak kurulur.
- **Model yönlendirme (tek kaynak `scripts/opendesign/rotalar.json`):** masaüstü uygulaması ve terminal `claude` Anthropic rotası adlarını gönderir (`claude-sonnet-5`, `claude-opus-4-8`…); yerel köprü (`opendesign-kopru.service`, 127.0.0.1:8787, stdlib) bunları geçit kimliklerine çevirir (`deepseek-v4.1-flash`, `deepseek-v4-pro`, `glm-5.3-flashx`, `kimi-k2.7-code`, `claude-haiku-5.5`, `gpt-6-luna`, `minimax-m3.1-flash`, `mimo-v2.6-*`, `hy4-preview`). 14 görünen rota + 18 eski ad (alias) — depodaki `--model claude-opus-5-5` çağrıları çalışmaya devam eder. Kurulum/denetim: `bash scripts/opendesign/kur.sh` / `--kontrol` (`kopru.py --doctor` eşleme tablosunu `rotalar.json` ile karşılaştırır).
- **Ajan hattı:** `otomasyon/llm/model_sec.py` (yeni) model kimliğini tek yerden verir (`MEDS_AJAN_MODEL` > `butce.json` → `claude.model` > masaüstü `settings.json` → Opus > `claude-opus-5-5`; denetçi/hızlı için ayrı alanlar). Koda gömülü `claude-opus-5-5` çağrıları `ders_zinciri`, `son_prova_zinciri`, `hastalik_zinciri`, `checkup_zinciri`, `kamp_zinciri`, `olasi_soru/gece.sh`, `cizim_uret`, `paralel_arsiv_isci`, `ders_isci/ayarlar.py` içinde buradan beslenir. `otomasyon/llm/opendesign.py` (yeni) CLI'sız doğrudan `/v1/messages` gönderir (köprü ayaktaysa köprü, değilse genel geçit); `yonlendir.py` A katmanı `opendesign` ajanı, `cloud_llm.py` ve `v2/core/llm.py` aynı istemciyi kullanır. `butce.json`: `opendesign` (deepseek) + `opendesign_glm` (glm/gpt, yazar ≠ denetçi kuralı için) ajanları, günlük tavan 2000.
- **Kilit değişmedi:** bütün bu yollar `llm_kilit.py` arkasında; kendiliğinden çalışan iş/zamanlayıcı yok (kural 20). Köprü yalnız gelen isteği iletir, iş başlatmaz.
- **Site AI'sı (`src/services/aiProvider.ts`):** `callOpenDesign` + `openDesignApiKey/openDesignBaseUrls`; `generateResilientMedicalAi` sırası Yerel GPU → **OpenDesign geçidi** → Groq → Muse Spark → Gemini. Anahtar yalnız sunucuda (`MEDS_OPENDESIGN_KEY`, `.env.example`'a üç satır eklendi); istemci paketine gitmez; uçların kendi zaman aşımı/iptali var.
- **Eklentiler (`scripts/claude_eklenti/kur.sh`, yeni):** resmî pazardan 10 eklenti — `typescript-lsp`, `pyright-lsp`, `frontend-design`, `code-review`, `code-simplifier`, `feature-dev`, `claude-security`, `security-guidance`, `pr-review-toolkit`, `plugin-dev` — + global `typescript-language-server`, `pyright`. Böylece tip/hata denetimi modelin dikkatine bırakılmaz; `npm run lint` (tsc) 0 hata korunur.
- **Artifact stüdyosu (`scripts/artifact_studio/`, yeni):** `studyo.py` JSON reçeteyi tek dosyalık, çevrimdışı HTML'e çevirir (satır içi CSS/JS, dış istek yok, bento ızgara, açık/koyu tema, yazdırma). Kutu türleri: metrik, metin, grafik (`cizgi`/`sutun`, çift eksen), tablo, not, alıntı, kod. Eksenler "yuvarlak" adımlarla (1·2·2,5·5×10ⁿ), sütunlar sıfır tabanlı. `SKILL.md` Claude skill'i (`artifact-studyo`), `kur.sh` skill'i `.claude/skills/`e ve önizleme sunucusunu **oturum kökünün** `.claude/launch.json`'una yazar (port 5199). Çıktı `cikti/` (git dışı).
- **Sınama:** `py_compile` (kopru/model_sec/opendesign/studyo), `bash -n` (üç kur.sh), JSON çözümleme (rotalar/butce/ornek), `npm run lint` 0 hata, `npx vite build` ✓; köprü canlı geçitle `POST /v1/messages` → 200 (masaüstü seçici `claude-od-01…14`); artifact sayfası önizleme bölmesinde açık/koyu temada görsel olarak doğrulandı; örnek reçete çift eksenli grafikle üretildi.
- **Dağıtım (kullanıcı onayıyla, aynı gün):** commit `f2d68621` `origin/main`e gönderildi, `bash deploy/oracle/dagit.sh` ile canlıya alındı — canlı `surum 20261112232020`, `onem 716`. Oracle `.env`'ine `MEDS_OPENDESIGN_KEY` eklendi (önce `.env.once.<zaman>` yedeği alındı; değer ekrana/depoya yazılmadı); `MEDS_OPENDESIGN_URL` boş bırakıldı (köprü yok → istemci genel geçide gider).
- **Canlı doğrulama:** Oracle'dan geçide doğrudan `POST /v1/messages` (`deepseek-v4.1-flash`) → **200**; konteynerde `/app/.env` anahtarı görüyor (`grep -c` = 1, GEMINI ile aynı yol); canlı sunucuda `POST /api/ai/generate` → `{"success":true,"providerUsed":"OpenDesign (deepseek-v4.1-flash)"}`. Yani site yapay zekâsı canlıda OpenDesign'ı gerçekten kullanıyor.
- **Dağıtım tuzağı (ilk deneme):** `[1/4] rsync` adımı `kex_exchange_identification: Connection reset by peer` ile düştü — Oracle SSH'ı art arda açılan bağlantıları (MaxStartups/fail2ban) kısa süre kesiyor. 20 sn bekleyip `ssh` sınandı (`SSH_OK`), `dagit.sh` yeniden koşuldu → 56 sn'de bitti. Dağıtım yarıda kalırsa önce SSH sağlığı denenir, kilit/commit durumu `dagit.sh` çıktısından okunur.
- **Denetim notu:** `kur.sh --kontrol` Claude'un kum kabuğunda (bubblewrap) `systemctl --user` ve ağa erişemediği için köprüyü "yok/kapalı" gösterip canlı sınamayı düşürür — gerçek durum Terminal panelinden bakılır (`systemctl --user is-active opendesign-kopru` → `active`, `curl 127.0.0.1:8787/health` → `{"ok":true,…}`).
- **Bilinen ortam tuzağı:** oturum sırasında `meds/.claude/launch.json` bir süre `/dev/null` üzerine salt-okunur bind-mount ile maskelendi (masaüstü uygulaması kendi launch yapılandırmasını korumak için yapıyor); maske kalkınca dosya `git checkout -- .claude/launch.json` ile geri yüklendi, çalışma ağacı temiz.

## 2026-11-13 — "PDF indir" herkese 401 veriyordu; canlı imajda başsız tarayıcı da yoktu (H556, onem 713, kullanıcı bildirdi)
- **Belirti:** soru çıktısı, soru dışa aktarımı ve ek modül föyünde PDF indirme `X-API-Password başlığı gereklidir` hatasıyla duruyordu; öğrenciye parola verilmediği için hiçbir öğrenci indiremiyordu.
- **Kök neden:** `/api/pdf/render` yalnız HTML'i PDF'e basar (veri yazmaz) ama `requireWritePassword` ara katmanının parolasız listelerinde (`readOnlyPosts`, `STUDENT_WRITE_ROUTES`) yoktu. İkinci engel: canlı Oracle imajında (`Dockerfile.oracle`) Chrome/Chromium yoktu, canlıda `pdf/status` `available:false` dönüyordu. Yerelde Chrome kurulu ve istekler loopback (yönetici) olduğu için hata geliştirmede görünmüyordu.
- **Çözüm:** uç `STUDENT_WRITE_ROUTES`'a `belge` sınıfıyla eklendi (IP başına 20/dk, 300/saat; Chrome kuyruğu zaten sınırlı 2 koşut + 8 kuyruk). `Dockerfile.oracle`'a `chromium` + `fonts-dejavu-core` eklendi (ARM'de uçtan uca sınandı: `%PDF-1.4`, 13.595 bayt). `API_KATALOG.md`'ye parolasız uçlar bölümü yazıldı. Yeni kapı `scripts/kapilar/pdf_basim_kapisi.py` (yerel 0 HATA).
- **Sınama:** yerel 3000'de dış istemci benzetimi (`cf-connecting-ip`) ile `POST /api/pdf/render` → 200, 11.816 bayt `PDF 1.4`; `/api/questions`, `/api/ai/extract-document` hâlâ 401 (yazma koruması bozulmadı); `tsc` 0 hata.
- **Dağıtım notu:** imaj değişti (`Dockerfile.oracle`) → `deploy-code.sh` kendiliğinden `--imaj` yolunu seçer; canlı Chrome kurulumu için dağıtım biraz uzun sürer.
- **Canlı doğrulama (dagit.sh sonrası):** `pdf/status` `available:true`; canlıda `POST /api/pdf/render` parolasız 200, 7.218 bayt `%PDF-1.4`; `/api/questions` hâlâ parola/doğrulama istiyor (yazma koruması bozulmadı); canlı kapı `0 HATA`. Tuzak: kapı canlıda elle `cf-connecting-ip` basınca Cloudflare `403 error code: 1000` verdi — kapı artık hedefe göre başlık seçer (yerelde `cf-connecting-ip`, canlıda tarayıcı User-Agent'ı) (commit 943cebc1).
- **Durum:** canlıda — onem 713, sürüm 20261112213630.

## 2026-11-10 — Sesli çalışma soruları: boşluk doldurma doğal soru olarak okunuyor (H552, onem 711)
- **Belirti/kök:** `ek_modul/ses.py` `____`'yi " boşluk " diye okuyordu (ekran metni sese gidiyordu).
- **Çözüm:** `hoca_sorulari.json` bosluk setinin 100 sorusuna soru biçimli `okunus` alanı; `ses.py` onu okur (ekran/kitapçık `metin` aynen). h-bosluk-* sesleri GPU'da yeniden üretildi, `pdf_esle_hoca.py` yeniden koşuldu (1262/1262). `dogrula.py --modul` okunuşsuz boşluklu soruda HATA verir. Diğer setlerde (doğru–yanlış, çoktan seçmeli) boşluk yok.

## 2026-11-10 — Ek modül hoca soruları: "PDF ile" eş zamanlı sesli çözüm + sesli ders tarzı oynatıcı (onem 708)
- **Eşleme (`scripts/ek_modul/pdf_esle_hoca.py`, yeni):** çözümlü kitapçıkta her soru bloğu (sol kenarda "N.", çözüm kutusu zemini #EEF3EE) bulunur; h-/hc- klibinin cümleleri satırlara bağlanır (kök, şık şık; çözümde doğru şık + kutu satırları karakter oranıyla), cümle zamanı `pdf_esle.py::cumle_zamanlari`. Yuruyus-kampcilik: 480 soru, 960 klip, 1220/1220 cümle sınırı duraklamaya oturdu → `src/data/ek_moduller/<modül>/hoca_pdf_esle.json`. Tuzak: "100." numarası metinle aynı satıra birleşiyordu (yalnız `^\d+\.` başı aranır).
- **Ekran:** `EkPdfHoca.tsx` (soru bloğu kırpılır, okunan satır yanar), `EkHoca.tsx` "PDF ile / Yalnız soru" kipi, `EkSesliOynatici.tsx` (canlı ders v15 alt oynatıcı düzeni: soru parçalı çubuk + sürükle/atla, ±10, önceki/sonraki soru, hız hapı, ⋯). `useSira` `konum(i, t)` ve `cal(n, bas)` kazandı.
- **Kapı:** `dogrula.py --modul` artık `hoca_pdf_esle.json` eskimişse HATA verir. TALIMAT.md'ye adım eklendi.
- **Yeniden eşleme (onem 710):** öteki oturumun hata notlu kitapçığı (e1b3d6e0) ve yeni hc- sesleriyle eşleme yeniden üretildi; hata kutusu zemini #FBEFE3 de çözüm kutusu sayılır (1262/1262 sınır). Ders: kitapçık ya da hoca sesi değişen her commit'ten sonra `pdf_esle_hoca.py` koşulur, `dogrula.py --modul` bunu yakalar.
- **Sınama:** yerel 3000, 1400 px ve 375 px: oynat → kök/şık A yanıyor, çözüm klibinde çözüm satırları; çubukta 13:42'ye atlama → Soru 36, PDF s. 36. Gerçek telefonda denenmedi.

## 2026-11-10 — Profil ve arkadaşlık istekleri görünmüyordu (H551, kullanıcı bildirdi)
- **Belirti:** giriş yapılmış olmasına rağmen kendi profil/arkadaş listesi ve istekler boş.
- **Kök neden:** `src/services/adminFetchAuth.ts::ogrenciJetonu` GET'te jetonu yalnız basarim/olasi-sorular/topluluk yollarına ekliyordu; `/api/arkadas` ve `/api/kisi/*` jetonsuz → sunucu kişiyi tanımıyordu.
- **Çözüm:** listeye `kisi/` + `arkadas` eklendi; öğrenci jetonu gereken istek açılışta oturum hazır olana dek (≤4 sn) bekler. Ayrıntı H551.

## 2026-11-10 — Ek modüller sesli ders: arka planda çalma, konular arası otomatik geçiş, oynatıcı ayarı, PDF bölüm görünümü
- **Oynatıcı (`ekOrtak.tsx::useSira`):** tek ortak `Audio` öğesi (konu değişince yeni öğe açılmaz → kilit ekranında/arka planda geçişte oynatma izni kaybolmaz), Media Session (başlık, oynat/duraklat, sonraki/önceki bölüm, ±10 sn; müzik susar). Çubuk: 10 sn geri/ileri, sonraki bölüm, klip anı, ayar paneli (hız 0,75–2×, "konu bitince sonraki konuya geç" `medsoru_ek_modul_oto_gecis`, başa dön).
- **Otomatik geçiş (`EkModullerV15.tsx::Ders`):** konu bitince ayar açıksa `sessionStorage medsoru_ek_modul_oto_basla` + sonraki konuya gidilir, ses ilk bölümden sürer.
- **PDF bölüm görünümü (`EkPdfBolum.tsx`, yeni):** kitapçık sayfası `pdf_esle.json` bölüm kutusuna (+%2 pay) kırpılıp kaba sığdırılır, okunan satır yanar; varsayılan kip, üst çubuktaki düğmeyle tam sayfa (eski PdfDocView, içerik değişmedi). Dar ekranda kap içeriğe göre uzar.
- **Sınama:** yerel 3000'de 1a: bölüm kırpma masaüstü + 375 px, son bölümden sonra 1b'ye geçip çalmayı sürdürdü, `mediaSession` başlık/`playing`. Gerçek telefonda kilit ekranı denenmedi.
- **Durum:** canlıda — başka oturumun f45d1c82 commit'i (onem 704, "ek modül PDF bölüm düzenlemeleri") bu değişiklikleri de aldı ve dağıttı; canlı `dagitim.json` aynı commit.

## 2026-11-10 — Çizgi Yarışı: Eğlenceli mod (onem 699, kullanıcı kararı)
- **Kural (kullanıcı onayı 2026-11-10):** `OdaAyar.cizgiMod` 'klasik' (aynen) | 'eglence'. Eğlencelide pistte ayna simetrik özel kareler (`ozelKur`, ≈uzunluk/10 çift, kale ve ilk satırlar dışında): ileri +3 adım, yan +1 yan hakkı, zar (tur bitince yeniden zar, `tekrar`), tuzak (2 hücre geri, kale kalır, tur biter). Kapışmada basılan kare etkisiz; kare basılınca tükenir.
- **Ekran:** kurulum/lobide "Mod" seçici, pistte kare simgeleri, kare etkisi kutlama yazısı; kurallar sayfası güncellendi. Düzeltme: "Yol kapalı, tur yandı" yazısı zar atılır atılmaz yanlışlıkla çıkıyordu, artık yalnız tur bitince.
- **Sınama:** `tahta.sinama.ts` 63 (simetri, üç etki, 6 bot-bot eğlence oyunu). Tarayıcıda elle oynanmadı.

## 2026-11-10 — Çizgi Yarışı: hızlı oyun, otomatik ilerle, yarış çubuğu (onem 697)
- **Belirti:** kullanıcı "işlevler, oyun hızı kötü" dedi: her adım ayrı dokunuş + ayrı sunucu gidiş-dönüşü; bot her adımda 0,75–1,4 sn bekliyordu (6 atınca ~8 sn).
- **Çözüm (kural değişmedi):** motor `{t:'kos'}` düz yol açık oldukça adımları tek hamlede harcar (bot da kullanır: tur ≈ 2 tik); `tahmin.ts` koşu tahmini. Ekran: "Otomatik ilerle" (varsayılan açık, yan seçimi gerekince durur), "Hepsi" tek hamle, önü kapalıyken yön uyarısı, yarış çubuğu, kapışma/altı/sıkışma kutlama yazısı.
- **Sınama:** `tahta.sinama.ts` 55 (koş). Tarayıcıda elle oynanmadı.

## 2026-11-10 — Uno: 10 yeni mod, yeniden çizilen kartlar, Sevimli Dostlar teması, mod kataloğu (H542)
- **Modlar (16):** kutu oyunları Klasik, Deluxe, Express, Flip, Hepsi Joker (All Wild), No Mercy, Extreme, Flex, Takım (Teams), Yalancı (Liar's); ev kuralları Yığma, 7-0 (artık hedef seçilir), Atlama, Hızlı, Çek-çek; MeDSor özel **Sevimli Dostlar** (Kedicik hediye, Yarasa siper, Yaramaz Tavşan şaka, Gökkuşağı Tayı). Tanımlar tek kaynak `tipler.ts UNO_MODLAR` (grup, deste, kişi başı kart, oyuncu sınırı, puan hedefi); desteler ve puanlar `motor/unoKartlar.ts`.
- **Motor:** `motor/uno.ts` baştan yazıldı: `bekle` (renk / itiraz / rulet / yalan / meydan), `ver` (kart verme), `yigin` (biriken ceza, Extreme'de basış), Flip `arka` yüzü + `cevir`, No Mercy elenme (25 kart), Extreme fırlatıcı (`gerilim`), Flex `guc`, Takım (karşılıklı ortak, yarı verme), Yalancı (kapalı kart `by`, Meydan Okuma). `sunucu.ts`: mod oyuncu sınırı (`unoOyuncuUygun`), puan hedefinde maç sonu. `tahmin.ts`: iyimser tahmin yalnız sonucu kesin kartlarda.
- **Arayüz:** `uno/Kart.tsx` (46 kart değeri + bayraklar), `figurler.tsx`, `temalar.ts` (`dostlar`, koyu yüz paleti), `Secimler.tsx` (hedef, flex, beyan, karar pencereleri), `UnoMasa.tsx` (seçim taslağı, görev bandı, kart tanıtım balonu), `Orta.tsx` (fırlatıcı, renksiz, Flip deste üstü), `Rakipler.tsx` (öbür yüzler, ortak / güç / elenme rozetleri), `canlandir.tsx` (yeni olaylar), `styles/masa/uno-mod.css`. Lobi/merkez: gruplu mod kataloğu (`ModSecici.tsx UnoModu`), kural sayfası `kurallar/UnoKurallar.tsx` + `uno/kartRehber.ts` (her modun her kartı: resim, adet, etki, puan).
- **Kurallarda uygulama kararları (kural sayfasında yazılı):** No Mercy renkli döküm (0–9×2, Atlat 3, Yön 3, Hepsini At 3, Herkesi Atlat 2, +2×3, +4×2), elenen −250; Flex dağılımı ve 4/8 çevirme simgesi; Extreme fırlatıcı olasılık modeli; Flip'te ilk kart Flip/Joker +2 yenilenir; Takım'da kartlar tek tek seçilerek verilir; Yalancı'da düz kart arayüzde hep açık oynanır.
- **Sınama:** `uno.sinama.ts` (klasik aile) + yeni `unoMod.sinama.ts` (31 birim + 11 mod rastgele oyun + bulanık) 0 hata; `tsc` 0 hata; başsız Chrome `meds_temp/uno_ui/uno_ui.mjs` 12 mod × 4 ekran: taşma 0, küçük dokunma hedefi 0, konsol hatası 0. Takım modunda eller uzundur (4 oyuncuda ortanca ~180 hamle; kural gereği iki ortak da bitirmeli).
- **Açık:** gerçek telefon/tablette elle oynanmadı (başsız dokunma benzetimi); iki insanlı Yalancı/Takım akışı yalnız motor düzeyinde sınandı; kural sayfasındaki kartlar hep klasik temayla çizilir.

## 2026-11-10 — Taş Masası: düzenlemede perler yerinde kalır (H535, onem 694)
- `OkeyMasa.tsx` (`taslakBasla`, `kirp`, boş grup yer tutucu), `PerAlani.tsx` (`enAz` px, `om-per--bos`), `okey.css`. H534 eki (düğmesiz düzenleme, per sıralaması) onem 693 ile canlıda.
- **Sınama:** yerel tarayıcıda Yedili: taş alınca ve per boşalınca komşu perin konumu aynı (229,112), Vazgeç eski hâle döndürüyor. Çok satırlı kalabalık masada ve telefonda denenmedi; taslak büyüyüp taş boyu küçülürse tüm masa birlikte ölçeklenir.

## 2026-11-10 — Taş Masası: düğmesiz masa düzenleme, per sıralaması, masa dizme kipleri (H534 eki)
- **Düğmesiz:** `motor/odunc.ts` (yeni, saf) + `OkeyMasa.tsx`: seçili el taşları + Per aç ya da masadaki taşa dokunma → masadan 1–2 taş ödünç alınıp `duzenle` yollanır (Yedili/Takım/101, her renk). `PerAlani.tsx` `onTas`.
- **Sıralama:** Sırala yedilide Per → Renk → Sayı; Masayı diz Renk → Sayı → Açılış sırası. Kural metni güncellendi.
- **Sınama:** oduncBul motor sınamaları geçti; yerel tarayıcıda Yedili: Sırala (per), Masayı diz, taşa dokununca taslak açılıyor. Ödünç alma ekranda gerçek elde denenmedi (uygun el gelmedi). Sunucu kodu değişmedi.
- **Durum:** yerelde; commit ve dağıtım yapılmadı.

## 2026-11-10 — Taş Masası: masadan taş alıp eldekilerle yeni per (H534)
- **Kural:** Yedili / Takım / 101 Okey'de `duzenle` hamlesi elden taş da alır (masadaki sarı 10 + eldeki sarı 9 ve 11 → seri). `motor/yedili.ts`, `motor/yuzbir.ts` (yeni dal), `tipler.ts` açıklaması, `OkeyMasa.tsx` (taslağa ıstaka taşı, sürükleme, 101 düğmesi), `MasaKurallar.tsx`.
- **Sınama:** `yedili.sinama.ts` ve `yuzbir.sinama.ts` düzenle bölümleri geçti, `tsc` 0 hata. Arayüz tarayıcıda elle oynanarak sınanmadı. Bot ve ipucu bu hamleyi önermez; zorunluluk/ceza hesabı değişmedi.
- **Durum:** yerelde; commit ve dağıtım yapılmadı.

## 2026-11-10 — Taş Masası: bot zorluğu, geri al, otomatik ıstaka sıralama, dar ıstaka toplamı (H533, onem 689)
- **Go/XOX:** `OdaAyar.botZorluk` kolay/orta/zor (varsayılan orta; zor = eski kusursuz bot), merkez + lobide "Bot gücü"; bota karşı "Geri al" (insan hamlesi + bot yanıtı, süreli Go hariç; `sunucu.ts hamle`).
- **Okey:** "Istakayı otomatik sırala" (`MasaTercih.otoSira`, menüde), Sırala ve Masayı diz Zorlu modda da; dar ıstakada gruplar korunur (`yuva.ts uzlas/diz`, sütun payı). Ayrıntı H533.
- **Sınama:** `tahta.sinama.ts` 54, yedili/duzOkey/acikMasa/yuzbir geçti, ıstaka dar boyut betiği. Gerçek telefonda elle oynanmadı.

## 2026-11-10 — Taş Masası: hamleler anında görünür, ağ gecikmesi gizlendi (H529, onem 688)
- **Belirti:** tüm oyun modlarında hamle gecikmesi.
- **Kök neden:** istemci her hamlede tünel üstünden sunucu yanıtını bekleyip masayı kilitliyordu (medyan 94 ms, p99 673 ms, en kötü 2,4 sn); sunucu içi ≤18 ms.
- **Çözüm:** `src/services/masa/tahmin.ts` (iyimser tahmin) + `istemci.ts` (`onayli`, geri dönüş, 15 sn güvenlik). Ayrıntı H529.
- **Açık:** Okey çek/aç/işle tahmin edilmiyor; ağ sıçramalarının kökü (tünel) için WS'ye ayrı alt alan kullanıcı erişimi ister.

## 2026-11-10 — Taş Masası: Go, Çizgi Yarışı, XOX arayüzü + Go eksikleri (onem 685)
- **Açıldı:** `sunucu.ts` `TURLER` += go/cizgi/xox; merkezde "Tahta oyunları" kategorisi; ekranlar `components/masa/{go,cizgi,xox}/`, ortak `tahta/ortak.tsx` (`TahtaAyar` merkez + lobi ayar seçicisi, `OyuncuSerit`), kurallar `kurallar/TahtaKurallar.tsx`, stil `styles/masa/tahta.css`. Bota karşı kurulumda tahta ayarları `kur(tur, bot, ayar)` ile gider (MasaView `kur` artık `Partial<OdaAyar>` alır).
- **Go motoru:** konumsal süperko (`gecmis` tahta özetleri), handikap 0–9 (`handikapNoktalari`, beyaz başlar, komi 0,5), süre `goSure` (`GO_SURELER`, ana + byo-yomi; sunucu hamleye `z` basar, `Motor.sureSonu` + `surePlanla` zamanlayıcısı `sureBitti`, durakta `saatKaydir`), bot sayımda kendi diri grubunun (`diriMi`) ölü işaretini geri alır. Sınama 49 → 53.
- **Varsayım düzeltmeleri:** `kabukOrtak.tasMi` artık "okey taşıyla oynanan" (uno/pişti/tahta değil); `MasaUstCubuk`/`MasaLobi` `okey = tur !== 'uno'` yerine `tasMi`; tahta oyunlarında tema/renk seçimi yok, asistan yalnız Go'da; el sonu metni tahta oyunlarına uygun.
- **Not:** ortak dosyalarda başka oturumun işlenmemiş izleyici/davet satırları vardı; bu commit'e yalnız HEAD + tahta oyunu satırları sahnelendi (dizin kopyasında tsc 0 hata doğrulandı).

## 2026-11-10 — Taş Masası 3. tur: Remi, Kastet, Düz Okey, Pişti, Taş Domino (onem 683)
- **Motorlar:** `motor/acikMasa.ts` (Kastet + Remi tek motor: genel `duzenle` = masadaki taşların tamamı + elden taşlar, Kastet 26 seri alanı + kilitli çift alanı, 22 taş sınırı, açan çekemez/çeken açamaz, bitene +50; Remi elden ≥30 ilk açılış, 2 sahte okey joker), `motor/duzOkey.ts` (çek-at, `bitir` perler/7 çift, okey/çift çarpanı, `goster`), `motor/pisti.ts` (52 kart, 2/4 eşli, pişti 10/Vale piştisi 20, puan tablosu), `motor/domino.ts` (rengi ya da sayısı tutan taş, uyan gelene dek çek, "Ek hamle": ardışık ya da iki uç eş sayı). Her birinin `*.sinama.ts` sınaması + bot benzetimi.
- **Domino tasarım kararı:** ilk kural (aynı renk ±1 / aynı sayı) bot ellerinin %94'ünü kilitle bitiriyordu; uyma kuralı genişletildi (kilit %0, el 14–19 tur), strateji ek hamle kuralında.
- **Arayüz:** `okey/OkeyMasa.tsx` kastet/remi/duz bayrakları (elden taslağa taş, Pas, Bitir, Gösterge, Kastet seri sayacı ve çift alanı, Remi 30 rozeti); `pisti/`, `domino/` yeni masalar; kurallar `components/masa/kurallar/*Kurallar.tsx`. Merkez kategorileri: Okey modları, Akıl oyunları, Kart oyunları.
- **Not:** aynı anda başka oturum go/cizgi/xox tahta oyunlarını ortak dosyalarda işlemeden tutuyordu; bu commit ortak dosyalara yalnız HEAD + bu turun eklemeleri olarak girdi (çalışma ağacında iki oturumun satırları birlikte duruyor).
- **Sınama:** 5 oyun başsız Chrome'da 1280×800 ve 375×740'ta açıldı (taşma ve konsol hatası yok); motor sınamaları geçti. Elle tam oyun oynanmadı.

## 2026-11-10 — Taş Masası 2. tur: başlatma hatası, Eğlence bölümü, Takım taş sayısı, masayı düzenle, geri al, Zorlu mod, Uno modları (H523, onem 682)
- **Belirti:** "Oyun başlatılamıyor, hata da görünmüyor"; oyun içinde takılma hissi.
- **Kök neden:** kimlik doğrulanmadan (`girdi` öncesi) gönderilen kur/başlat sunucuda yanıtsız atılıyordu; kopukken basılan başlat/sonraki el istemcide hiç gönderilmiyordu (ayrıntı H523).
- **Çözüm:** `istemci.ts` kuyruk + `bekliyor` durumu + 15 sn zaman aşımı, `MasaView.tsx` `MasaBekleme`; sunucu `kimlik-bekle` hatası.
- **Takım Yedili:** 5–6 oyuncu 4 taş, 2–4 oyuncu kurucu seçimi 7/14 (`OdaAyar.tasSayisi`, `takimElTas`; `Motor.elBaslat` artık `ayar` alır).
- **Yedili/Takım:** `duzenle` hamlesi (masadaki taşların tamamı yeniden perlere dizilir; ele taş dönmez, elden eklenmez; kullanıcı kararı 2026-11-10), `geriAl` (sunucu tur içi yığın: per açma/işleme/düzenleme; çekme, devretme, hediye taş, el sonu sıfırlar; ıstaka hareketleri istemcide). Oyun modu Normal / Zorlu (`asistan:false`: yardımcı ve elle dizme yok, masa el bitince dizilir).
- **Uno:** dengeli dağıtım (elde ≤2 joker/+4, ≤1 +4, ≤3 aksiyon; çekişte 4. joker verilmez), resmî kurallar (ilk kart etkisi, ilk joker → `renk`, +4 `kabul`/`itiraz`, botlar +4'ü dürüst oynar), `UNO_MODLAR`: Klasik, Yığma, 7-0, Çek-çek, Atlama, Hızlı. Kurallar sayfası yeniden yazıldı.
- **Menü:** `navV15` yeni `eglence` bölümü (ray + Menü; oyunlar Soru çöz'den çıktı); merkezde "Okey modları / Kart oyunları".
- **Sınama:** `yedili.sinama.ts` (40+2), `uno.sinama.ts` (16), 6 Uno modu × 300 el ve 14 taşlı takım × 45 el bot benzetimi, soket uçtan uca (14 taş, geri al, kimlik öncesi), başsız Chrome ekran görüntüleri. Gerçek telefon sınanmadı.

## 2026-11-09 — Açılış ekranı sunucu kapalıyken kendiliğinden yeniden deniyor (H516, onem 674)
- **Belirti:** Kullanıcı "site açılmıyor, splash ekranından geçmiyor" dedi (22:05). Aynı dakikada başka oturumun Oracle dağıtımı (onem 672) `meds-app`'i yeniden başlatmıştı; sunucu RAG indeksini yüklerken 1-2 dk yanıt vermiyor.
- **Kök neden:** Dağıtım kesintisinde service worker kabuğu (index.html) verdiği için sayfa açılıyor ama uygulama hiçbir API yanıtı alamıyor; splash React hazır olunca kalktığından sonsuza dek kalıyor. `__medsoruTazeYukle` yalnız `/api/surum` 200 ise yenilediğinden kesinti sırasında hiçbir şey olmuyor, kullanıcı elle yenilemeden kurtulamıyordu. Kod hatası değil, "sunucu yok" durumunun ekranda karşılığı yoktu.
- **Çözüm:** `index.html` H516 betiği + `#sp-durum` durum satırı: uygulama 7 sn'de açılmazsa `/api/surum` yoklanır; yanıt yoksa "Sunucu başlatılıyor, yeniden deneniyor…" (3. denemeden sonra "Sunucu güncelleniyor; 1-2 dakika içinde kendiliğinden açılır" + Yenile düğmesi), 4 sn'de bir yeniden; sunucu dönünce sayfa kendiliğinden yenilenir. Ağ yoksa yalnız bilgi verilir (çevrimdışı önbelleklere dokunulmaz). Sunucu sağlıklıyken uygulama yine açılmadıysa 4. yoklamada `__medsoruTazeYukle` (eski kabuk) denenir.
- **Sınama:** Chrome'da yeni kabuk normal açılışta durum yazısı göstermiyor; sahte splash + `/api/surum` reddi ile yazı ve düğme çıktı, yanıt geri gelince "Sunucu hazır, sayfa yenileniyor…" ve yenileme gerçekleşti.
- **Not:** Yerel `guncelleme_notu.json`'daki dağıtılmamış H515 notu (onem 673, sesli ders çevrimdışı) bu notla değiştirildi; yedeği oturum karalama klasöründe, H515 dağıtılırken yeniden yazılmalı (onem 675+).

## 2026-11-09 — Sesli ders çevrimdışı: ek katmanlar da cihaza iner, paket çevrimiçi açılışta kendini tazeler (H515, onem 673)
- **Belirti:** İndirilmiş sesli ders internetsizken ses + PDF + metinle açılıyordu ama 2026-10-21'den sonra eklenen katmanlar çalışmıyordu: hocanın sorabileceği ara soru sayfası sessiz (klipler `/api/cozucu-ses/k2hocaara/…` hiç inmemişti, SW sessiz klip veriyordu), ders analizi sesleri yok, çıkmış soru chip'i "Soru yüklenemedi" (`/api/past-exams/tek/<id>` 503), terim sesi düğmesi kayboluyor, Lottie ara resimleri SVG'ye düşüyor; ayrıca indirmeden sonra sunucuda eklenen katmanlar (çizim, çıkmış chip'i, terim sözlüğü, v2 cümleler) cihazdaki eski ayrıntı kopyasında yoktu.
- **Kök neden:** `canliDersCevrimdisi.ts` yalnız ses/PDF/ayrıntı/ara resim SVG indiriyordu; sw.js `PAKET_SES_RE` kliplerini yalnız `medsor-paket-v1`'de arıyor, `/api/terim-ses` ve genel API dalı ağ yokken sesli ders önbelleğine hiç bakmıyordu. Ayrıntı kopyası yalnız indirme anında yazılıyordu. Ayrıca `detayAdresi` kopyası TÜM varyantları taşıyordu: Wi-Fi var/internet yok durumunda oynatıcı inmemiş sesi seçebiliyordu.
- **Çözüm:** yeni `canliDersCevrimdisiEk.ts` — dersin ek dosya listesi (ara soru + ortak klipler, ders analizi/özeti klipleri, çıkmış soru verisi, gömülü değilse örnek soru API kopyası, terim/kısaltma sesleri, günlük, Lottie) `medsoru-canli-ders-offline`'a yazılır (ses: sorgusuz yol + `X-Cd-Surum`; JSON: tam adres); kayıt defterinde `ekler`/`ekEksik`, silmede başka dersin kullandığı ortak klip korunur. İlerleme: ana dosyalar %0–90, ekler %90–99. sw.js: `cdEkYaniti()` (klip paketlerde yoksa sesli ders önbelleği, sürüm farkında önce ağ, Range/206), `/api/terim-ses` ve `/ara_resim/*.json` dalları, genel API dalında ağ hatasında 503'ten önce `onbellekte()`. Store: ayrıntı ağdan gelince `cdYerelDetayTazele` kopyayı tazeler ve eksik ekleri arka planda indirir (oturumda ders başına bir kez). Her iki ayrıntı kopyası yalnız cihazdaki seslerle.
- **Sınama:** `scripts/cevrimdisi_sinama/sesli_ek.mjs` (vekil + başsız Chrome: indir → ağı kes → ders sayfası, ses Range/206, ara soru klibi, analiz klibi, çıkmış verisi, Lottie). Yerelde Kurul 2 dersi olmadığından k2-07 (farmakoloji) Oracle'dan geçici çekildi; `dersler.json` değişikliği sınama sonrası geri alındı.
- **Önleme:** sesli derse yeni bir katman (yeni API ucu / klip ailesi) eklenince `cdEkDosyalar()`'a satır + sw.js'de o yolun cihaz kopyasına bakan dal + `sesli_ek.mjs` denemesi birlikte eklenir (yol haritası `docs/CEVRIMDISI_YOL_HARITASI.md` §5).
- **Dağıtım:** yapılmadı — aynı anda başka oturumların yarım dosyaları (`CanliDersAktarPencere.tsx`) tsc'yi kırıyor; commit/dağıtım kullanıcı kararıyla.

## 2026-11-09 — Soru dışa aktarıcı: renk temaları, öge renkleri, yazı stilleri (H510, onem 672)
- `/sorular/disa-aktar` (`v15/soruAktar/ayar.ts`): 15 renk teması (`TEMALAR`/`temaUygula`), 24 öge rengi `renkler` + `ogeRenk(a,k)` (boş → vurgu/metinden türetilir), palet 15 + `paletOzel`; 44 yazı tipi (`YAZI`, Google Fonts bağlantısı önizleme/ölçüm/sunucu PDF/panelde), ayrı başlık yazısı, kalınlık, harf aralığı, başlık oranı, kök/şık stili, büyük harf, numara ve şık harfi biçimi, şık girintisi.
- `belge.ts`/`docx.ts`/`pptx.ts` tüm renkleri `ogeRenk` ile alır; DOCX sayfa zemini (`w:background`), başlık fontu, caps/altı çizili run; PPTX slayt zemini + `BAS_FONT`.
- Site: `appearance.ts` FONT_LIST arayüz 20 / okuma 19, `OkumaAyar.kalinlik` 300–700; `YaziAyarV15` arayüz yazı tipi seçici.
- Doğrulama: tsc + vite build temiz; Sepya + Lora/Montserrat ile DOCX/PPTX (LibreOffice açtı) ve sunucu PDF (fontlar gömülü) üretildi. Eski kayıtlı ayarlar `ayarNormal` ile uyumlu.

## 2026-11-09 — Tablet düzen taraması: örnek soru satırında rozet/yazar üst üste binmesi (H514, dağıtılmadı)
- 14 rota × 6 boyut (700/768/820 dikey, 1024/1180 yatay, 1024×1366) `sayfa_tarama.mjs` ile tarandı: yatay taşma yok.
  Tek gerçek kusur `/sorular/ornek` ders listesinde "Hoca üslubu · N yeni soru" rozetinin yazar adına binmesiydi (iki span aynı `grid-area: who`).
- `KazanimSorulariView.tsx`: tek `.ks-lesson-who` (yazar · rozet); `v12/secondary.css`: alan sarar. `vite build` yapıldı; commit/dağıtım yok (onem artırılmadı).
- Bilinen ve kabul edilmiş: 1180 px yatayda Bugün sağ sütununda "KRONOME…" kısaltması (H343 kararı).

## 2026-11-06 (7) — Sesli ders yakınlık sınırı %80–%140 (onem 658)
- `CanliDersDers.tsx` `Z_MIN/Z_MAX` (0,8/1,4): düğmeler ±0,1, kayıtlı değer sınır dışıysa 1; `PdfDocView` `zoomMin/zoomMax` (kıstırma + tekerlek; varsayılan 0,5–4 öteki ekranlarda).

## 2026-11-06 (6) — Kıstırma yumuşatıldı (onem 657)
- `PdfDocView.tsx`: önizleme her sayfa yerine tek `.pdv-track` dönüşümü (parmak ortası çapa, iki parmak kaydırma, kare başına bir çizim);
  bırakınca çapa sayfa + sayfa içi oranla geri kurulur (sayfa araları ölçeklenmediği için düz y·k kayıyordu). Belirti: büyütürken sıçrama, bırakınca başka yere atlama.

## 2026-11-06 (5) — Ara resim kullanıcı tercihi (onem 656)
- `CdTerimKatman.tsx` PDF_GORUNUM'a `araResim` katmanı (`cd-pdf-araResim`, varsayılan açık); `CdV15` Görünüm › PDF katmanları satırı; `CdAraResim` kapalıyken kart açılmaz (galeri düğmesi kalır).

## 2026-11-06 (4) — PDF iki parmak kıstırma + kalıcı yakınlık (onem 655)
- `PdfDocView.tsx`: dokunmatik iki parmak kıstırma (hareket sırasında CSS ölçek önizlemesi, parmak kalkınca tek `onZoom`), iOS `gesture*` engeli; `pdfDoc.css` `.pdv { touch-action: pan-x pan-y }`.
- `CanliDersDers.tsx` `CdPdfBolme`: yakınlık `medsoru_cd_pdf_zoom_{genislik|sayfa}` anahtarında kalıcı.

## 2026-11-06 (3) — Sesli ders altyazı modu + ara soru otomatik çöz düğmesi (onem 654)
- `CanliDersDers.tsx`: Slayt + altyazı modunda `CdPdfBolme sigdir` → `PdfDocView fit="page"` (genişliğe sığınca slaytın altı kesiliyordu); altyazı şeridi en çok 22vh.
- `CdHocaAra.tsx`: "Otomatik çöz" onay kutusu (`medsoru_hoca_ara_coz_v1`, varsayılan açık); kapalıyken okuma sonrası geri sayım durur, öğrenci şık seçer ya da "Çözümü göster"e basar; düşünme sırasında açılırsa hemen çözer.

## 2026-11-06 (2) — iPad pencere kipinde geri dönüş (H502, onem 653)
- `components/shell/ipadPencere.tsx`: iPad pencere/bölünmüş ekran algısı (`:root[data-pencere='dar']`, üst çubuk 84 px sağa), alt yüzen geri hapı,
  sol kenar kaydırması + Esc/⌘[/Alt+←, yedek yollar 2 kez kullanılırsa hap cihazda kalıcı (`medsoru_ipad_geri_hap`). `ShellV15`: başlık = geri düğmesi.
- Arzu katmanı: bir kerelik "sürprizler açık kalsın mı" sorusu (`arzu/ArzuSoru.tsx`, `medsoru_arzu_soru_v1`, yöneticide sorulmaz). Sürüm notunda anılmaz.

## 2026-11-06 (1) — KMB 01 hoca kaydına göre tam denetim (H501)
- Kayıt large-v3 ile yeniden döküldü (`meds_temp/kmb/kaynak/nazogastrik_metin_l3.txt`); tüm anlatım, notlar, akış, vakalar, hedef kartları satır satır kıyaslandı (cümle sayıları korunarak): "kostik" terimi, sınav biçimi (malzeme seçtirme + basamaklar, 34:03), ölçüm son noktası "epigastrium (ksifoid hizası)", ölçümde "en sık hata" iddiası kaldırıldı (32:49), septum deviasyonu yaşlılarda, yutkunmada yarımşar mL su, idrar torbası, kayıtta olmayan iddialar çıkarıldı. Vazelin kullanıcı kararıyla "zor durumda az" (sarı, çarpı yok). 27 klip yeniden seslendirildi, 19 video yeniden üretildi, kapılar 0 HATA.
- `hoca_dokum_gpu.sh` ek argümanları aktarır (H501).

## 2026-11-05 (2) — KMB 01 Nazogastrik sonda dersi (H497–H500)
- Kaynak: hoca ses kaydı (Drive, 37 dk; GPU dökümü `meds_temp/kmb/kaynak/nazogastrik_dokum.json`) + TIS301.43.1 föyü. İçerik `src/data/kmb/01.json` (kurucu `meds_temp/kmb/ng/ders_kur.py`): 19 adım / 99 cümle, 14 föy hedefi kartı (6 vuruşlu film), 2 OSCE akışı (takma + dal "ses var/yok", çıkarma), 11 vaka (6'sı kime takılır/takılmaz), 5 "sahnede bul". Hoca sınav vurguları: kontrendikasyonlar (yüz/kafa tabanı kırığı, koroziv, bilinci kapalı + hava yolu korunmamış, özofagus varisi), ölçüm burun–kulak memesi–ksifoid, aniden hava + epigastrium dinleme. Bağımsız denetçi DÜZELTİLMELİ → 16 düzeltme uygulandı.
- 6 yeni 2B sahne (`sahneler_ng_a/b/c.tsx`: ng-kesit, ng-burun, ng-govde, ng-mide, ng-malzeme, ng-pozisyon; sözleşme `meds_temp/kmb/ng/SAHNE_SOZLESMESI.md`), 19 adım videosu (`scripts/kmb/lottie2b/adim2b_ng1/2/3.py`, öneki `ng-`), EMA 123 klip GPU'da (`data/kmb_cozucu/ses/01`, git dışı → Oracle rsync).
- Hat çok derse açıldı: `adim2b.py --kod=`, `ses.py`/`dogrula.py` 01 için `lottie2b` + `ng-` öneki, `uret2b.py` ses_01, `LottieVideo.LOTTILER` yalnız-2B videoları da alır, `svg_lottie.ON_EK` ng sahneleri.
- Kök neden düzeltmeleri: H497 `lottie_dsl.yol` çok alt yol (çarpı "Z" çiziyordu; 02 videoları yeniden üretildi), H498 bbox ata transform (`svg_disa.mjs`, `HedefFilmi.tsx`), H499 clipPath'li sıvı, H500 altyazı bandı (kesit 70 px yukarı).
- Kapı `dogrula.py 01` ve `02` 0 HATA; 19 videoda `kare_onizle` 0 otomatik bulgu + kare kare göz denetimi.

## 2026-11-05 (1) — Arayüz denetimi aşama 2–3: kaydırma kilidi, klavye, kesme noktası, Esc (H494–H496, dağıtılmadı)
- H494: 16 bileşen doğrudan `body.style.overflow` yazıyordu → sayaçlı `lockScroll/unlockScroll` (DraftDeduplicationModal, QuickAddHero, ContributeModal, AdminPanelModal, TopluPdf, PdfStudio, kmb/DersVideo, HedefFilmi, HikayeFilmi, KazanimSorulariView, SearchPalette, CanliDersView, LearnReview, AnnotationWorkspace, LessonPlayer, SpotsSureDiyalog).
- H495: çekmece/pencere eşiği 640 → 768 (`shell.css` + `Sheet.tsx`); klavyede `.pa.is-tam`, `.kr15e-arka`, `.teg-perde`, `.pt-pop`, `.sh-pop` görünür alana uyar (`katman-duzeni.css`); `.ms-chat-shell` 768+ zoom bölmesi; UpdatePrompt Esc belge düzeyinde.
- H496: sözlük bağlantısının dokunma alanı.
- Bilinçli bırakılan: `.teg` (tam ekran adası) tam ekran katmanların üstünde kalmalı; spot süre/istatistik modalları içinden diyalog açılmıyor.
- Hız ölçümü (4× CPU): `/sozluk` 0,66 sn; `/cikmis` sıcak 1,8 sn, soğuk 5,8 sn (ilk kez ~40 MB indirme, işçide; cihaz başına bir kez). Ayrı iş adayı: ince liste kaydı + ayrıntının tembel yüklenmesi.
- KMB (onem 647): `.kmb-serit` adım şeridinin `::before` dokunma alanı (−10 px) `overflow-x:auto` kabında kırpılıyordu (gerçek hedef ~16 px); dolgu 10 px + `margin-block:-6px`, görünüm aynı.
- Doğrulama: `tsc` bu dosyalarda temiz, `vite build` temiz, 10 sayfa × 4 görünüm taramasında taşma/hata yok. Klavye ve çekmece davranışı gerçek cihazda sınanmadı. Commit/dağıtım yok.

## 2026-11-04 (6) — Arayüz denetimi aşama 1: katman, klavye, dokunma (H491–H493, dağıtılmadı)
- Tarama: 20 sayfa × 7 görünüm (`sayfa_tarama.mjs`, başarım penceresi kapatılarak) + stil kodu katman/klavye denetimi. Bulgular ve sıradaki aşamalar: canvas https://claude.ai/artifact/VVyP72D9Bf6AwqbcQKLVnv
- Düzeltildi: başarım penceresi kesilmesi (H491), katman sırası + klavyede alt öğeler + dokunmatikte gizli denetimler + mini oynatıcı değişken adı (H492, yeni `src/styles/katman-duzeni.css`), Soru çöz özet kartı kesilmesi (H493).
- Açık (aşama 2–3): `.teg` katman çakışması, spot katmanları, Esc eksikleri, kaydırma kilidi sıfırlama, `100dvh` katmanlar, 640/768 kesme noktası farkı, `/cikmis` ve `/sozluk` açılış hızı.
- `npx vite build` temiz; commit/dağıtım yapılmadı.

## 2026-11-04 (5) — Sesli ders yerel ilerlemesini sıfırlama / temizleme (onem 643)
- Kullanıcı isteği: öğrenci sesli derslerde cihazındaki ilerlemeyi dilediği gibi sıfırlayıp yeniden çalışabilsin. Yalnız yerel kayıtlar: "kaldığın yer" (`medsoru_canli_ders_konum_v1`) ve çalışma takibi (`medsoru_calisma_takip_v1`: süre, bitti işareti, tekrar turu). Ses dosyaları, indirilenler, listem ve ayarlara dokunulmaz.
- Yeni `src/components/canliDers/CdIlerlemeTemizle.tsx`: `SifirlaDugme` (tek ders, iki adımlı onay, 6 sn'de kendiliğinden vazgeçer) ve `TemizleDiyalog` (görünen listenin dersleri için toplu; "kaldığın yer" ve "bitti + süre" ayrı onay kutuları, sayılarıyla; sonuç satırı). Yerler: v15 sesli ders listesi altı ("İlerlemeyi temizle"), v15 ders ayrıntısı kaldığın yer kartı ("İlerlemeyi sıfırla", kayıt yoksa gizli), klasik liste kenar çubuğu "Temizlik" + satır seçenekleri.
- Servis: `calismaTakip.ts` `konuSifirla(m, konu)` + `modulSifirla(m, konular?)`; `canliDersStore.ts` `cdKonumSil(key)` + `cdKonumlariTemizle(keys?)` (yüklü ders sıfırlanırsa ses durur ve başa alınır ki konum yeniden yazılmasın) + `CD_KONUM_OLAY` ('cd:konum'). `useCdKonumSurum()` ile `useIlerleme` (dersVeri.ts), `DersDetayV15` ve `CanliDersView` konum haritasını olayla yeniler (eskiden tek seferlik `useState` idi: silince ekran güncellenmiyordu).
- Sınama: localhost tarayıcı (masaüstü + 375 px): toplu temizlik 2 konum + 2 takip kaydını sildi, "1/35 bitti" → "0/35", ders ayrıntısı "Kaldığın yer 10:00" → "Henüz başlamadın" / "Sesli dersi başlat"; konsol hatası yok. Telefonda diyalog eylem satırı sekme çubuğunun altında kalıyordu → `--sh-tabs-h` kadar alt boşluk. Commit + dagit.sh ile dağıtıldı (onem 643).

## 2026-11-04 (5) — Diyalog açılırken titreme / ileri-geri zıplama (H490, onem 642)
- Belirti (kullanıcı): diyalog açılırken diyalog ya da arkadaki ekran "flashback gibi" git-gel yapıyor. Başsız Chrome'da (masaüstü + telefon, 7 senaryo: arama, kurul çipi, hesap menüsü, bildirim, kronometre, kart menüsü → Hakkında penceresi, ayarlar) kare kare kayıt (`scratchpad/film.mjs` + PIL kare farkı) ve kare başına yerleşim ölçümü (`titre.mjs`) ile **yeniden üretilemedi**; sayfa kayması, scroll sıçraması ya da geri dönüş deseni yok.
- Kök neden adayı (kod incelemesi, en güçlü): `main.tsx` görsel alan izleyicisi `--vvh/--vvt`'yi klavye kapalıyken de her karede yazıyordu; iOS/Android'de adres çubuğu açılıp kapanırken, sıçramalı kaydırmada ve yakınlaştırmada görsel alan sürekli değişir. Pencere (`.ms-overlay`), alt sayfa (`.sh-sheet`), arama, ders ve çözücü katmanlarının yüksekliği/konumu bu değişkenlere bağlı olduğundan diyalog açılır açılmaz (kilit → belge yüksekliği değişir → çubuk hareket eder) katman birkaç kez yukarı-aşağı zıplıyordu. Değişkenler artık yalnız bir yazı alanı odaktayken (klavye olasılığı) yazılır; odak yokken kaldırılır → katmanlar `100dvh`/`0px` yerleşim alanını kullanır (tarayıcı araç çubuğunu kendisi hesaba katar).
- Ek sertleştirme: `Dialog.tsx` kaydırma kilidi `useLayoutEffect`'e (Sheet ile aynı; masaüstünde kaydırma çubuğu bir kare sonra kalkınca sayfa kayıyordu), odak `preventScroll`; `ConfirmDialog` odak `preventScroll`; `QuickAddHero` tembel `AiQuestionOptimizerModal` kendi `React.Suspense` sınırına alındı (sayfa düzeyi Suspense'e düşünce tüm sayfa iskelete dönüp geri geliyordu — "flashback" deseni; diğer tembel pencereler zaten sarılıydı).
- Kullanıcıdan beklenen: hangi cihaz/tarayıcı ve hangi diyalogda sürdüğü; sürerse kayıt aracı o senaryoyla koşulur.

## 2026-11-04 (4) — Açılış ve geçiş hızı + tasarım hataları (H484–H489, onem 640)
- Ölçüm (4× CPU yavaşlatma, `scripts/perf/yukleme_olcum.mjs` artık `AI_COOKIE` ile zorunlu girişi geçer; soğuk açılış `acilis.mjs` ve splash ölçümü oturum geçici klasöründe): soğuk açılış 99 betik / 524 KB gz, hazır 2,4 sn; sıcak 1,5 sn (betik isteği yok, süre ayrıştırma/çalıştırma). Geçişler: /cikmis 8,6 sn (IndexedDB getAll 1,5 sn + arama alanı katlama 0,7 sn + GC), /sozluk 2,1 sn (3,4 MB ansiklopedi parçası ayrıştırma), diğer merkez sayfaları 0,6–1,6 sn.
- **H484 (kök neden: splash her yeni sekmede ≥5 sn zorunlu bekliyordu, `sessionStorage`):** `App.tsx` — gösteri yalnız günün ilk açılışında ve en çok 1,8 sn (`localStorage medsoru_splash_gun`), sonraki açılışlarda uygulama hazır olunca hemen kalkar; Klasik (v10) eski davranışı korur. Ölçüm: ilk açılış 2,9 sn (önce ≥5), sonrakiler 1,65 sn (uygulamanın hazır olma süresi).
- **H485:** kök adres `/` öğrenciye gizli "Soru ekle"ye düşüyor, açılış "Bu sayfa şu an kapalı" ekranıyla başlıyordu → kapalıysa Bugün'e geçer (`replaceState`, geçmişe kayıt yok); adresle girilen diğer gizli sayfalar H139 gereği ekranda kalır.
- **H486:** v15 jetonları `'Plus Jakarta Sans'` / `'Newsreader'` istiyordu, hiçbir yerde yüklenmiyordu (index.html yalnız Geist/Bricolage/Literata/JetBrains Mono indirir); tarayıcı sessizce Geist/Literata'ya düşüyordu → jetonlar yüklenen yazı tiplerini adlandırır (görünüm değişmedi, tasarım–kod uyumsuzluğu kalktı).
- **H487:** küçük dokunma hedefleri (tarama `sayfa_tarama.mjs`): "Kurul 1 derslerine geç" 150×19, üst çubuk kırıntısı "Soru çöz" 67×16, İstatistik "Tümünü aç" 86×19 → satır içi dolgu / telafili dolgu, görünüm aynı, tarama 0 küçük hedef.
- **H488:** 600–959 px kapsayıcıda (tablet 820, yarım ekran) Soru çöz özet kartları tek satır düzeninde taşıyordu (sayı kesik, "Karma test · 20 soru" kart dışına) → bu aralıkta kısa düğme adı (`.s15-kisa`) + dar dolgu (`dersler.css`).
- **H489:** telefonda üst başlık `overflow-wrap: break-word` ile tek kelimeyi hece ortasından bölüyordu ("İstatistikleri|m") → `normal` + kırpma (`shell.css`).
- Yapılmayan / aday: `/cikmis` açılışında 4.700 zengin kaydın IndexedDB'den okunması ana iş parçacığında ~1,5 sn (4×); liste için ince kayıt + ayrıntıyı açınca yükleme ayrı iş. `/sozluk` 3,4 MB veri parçası yerine JSON getirme ayrı iş. Rolldown `codeSplitting.minSize` ile parça birleştirme denenmedi (sıcak açılış istek değil ayrıştırma ağırlıklı).

## 2026-11-04 (3) — Çevrimdışı eksik giderici (H483)
- Yeni `src/services/cevrimdisi/eksikGider.ts` (açılışta + 'Eksikleri tamamla' düğmesi), `paketiDenetle` sesli derste PDF/eşleme sayar. Uçtan uca sınandı; dağıtıldı.

## 2026-11-04 (2) — İnternetsiz sesli derste PDF/slayt/çizim (H482)
- `sw.js` `ARAMA_SIRASI`: sesli ders ve eski PDF önbellekleri eklendi (toplu indirmenin pdf.js yardımcıları bulunamıyordu). Uçtan uca internetsiz sınama geçti; dağıtıldı.

## 2026-11-04 — Çevrimdışı ders PDF'leri internetsiz açılmıyordu (H481, dağıtıldı onem 637)
- `public/sw.js`: H63'ün `/api/lecture-pdf/` kısa devresi sesli ders (`medsoru-canli-ders-offline`) ve eski PDF indirme (`medsoru-pdf-offline`) önbelleklerini atlıyordu. Artık bu adresler kümede (`cihazPdfYukle`/`cihazPdfYaniti`) tutulup cihazdan (Range → 206) veriliyor; olmayan ağa bırakılır.
- `canliDersCevrimdisi.ts` ve `deviceStorage.ts::savePdfOffline` kayıttan sonra SW'ye `PAKET_CHANGED` gönderir. Sınama: headless Chrome internetsiz → 200 + 206. Commit/dağıtım yapılmadı.

## 2026-11-03 (3) — Arzu katmanı yöneticiye de açık (onem 635)
- `arzuKimlik.ts` izin listesine `ADMIN_EMAIL` eklendi: yönetici hesabı da karşılama/yaratık/kalp katmanını görür (kullanıcı kararı). Sürüm notu değişmedi.

## 2026-11-03 (2) — Arzu katmanı: yeni easter egg'ler, tek yaratık kuralı, tavşan (onem 632; sürüm notunda ANILMAZ)
- Yeni: `KucukDokunuslar.tsx` (boş yere çift dokunma → kalp; uzun sayfa sonunda "Buraya kadar okudun"; 11:11/22:22 notu; 40 dk aralıksız → mola tilkisi + not; sekme gizlenince başlık "Tilki seni bekliyor"), `Yoldas.tsx` (gece 23–05 uyuyan tilki "z z z", dokununca uyanır; koşan tilkiye ikinci dokunuş → 5 dk yanında kalan tilki), `ozelGunler.ts` (14 Şubat + doldurulacak doğum günü/yıl dönümü satırları → karşılamada özel cümle + kalp yağmuru), tilki patileri (`.ar-pati`).
- Kullanıcı kararı: yaratıklar aynı anda görünmez → `GezinenTilki.tsx` tek yaratık kuyruğu (geçit sırayla), yoldaş açıkken bekler (`arzu:yoldas-durum`); "selam" kipi: kenardan hızla gelir, pati sallar ("Selam!"), kaçar; tavşan eklendi (`TavsanZiplayan`, zıplama/kulak/arka ayak animasyonu, durup burun oynatma), klavye "tavsan".
- Çizim denetimi: `scripts/arzu/cizim_onizle.tsx` (çizimleri büyük boyutta statik HTML'e basar). Tilkinin yakın ön bacağı DOM'da başın önüne alındı (selamda pati yüzü kapatmasın). Kullanıcı `mesajlar.ts`'teki dört cümleyi kendi sözleriyle değiştirdi (korundu).

## 2026-11-03 — Arzu'ya özel katman: karşılama, gezinen tilki, kalpler, Kitty & Batman (onem 630; sürüm notunda ANILMAZ)
- Kullanıcı isteği: Arzu hesabına (arzuturk361@gmail.com / drarzuturk@gmail.com, uid'ler `arzuKimlik.ts`) özel, tilkili-kalpli sürpriz katmanı; güncelleme notunda yazılmaz (sürpriz). Başka hiçbir kullanıcı için parça yüklenmez (`App.tsx` → `arzuMu(currentUser)` + tembel `ArzuKatmani`).
- `src/components/arzu/`: `cizimler.tsx` (elle SVG: yürüyen tilki 4 eklemli bacak, oturan kalpli tilki, Kitty & Batman çifti, asılı kalp, sekme simgesi), `ArzuKarsilama.tsx` (günde bir kez, girişten 35 sn sonra; başka diyalog açıksa bekler; `medsoru_arzu_karsilama_v1`), `GezinenTilki.tsx` (WAAPI koşu, koklama durağı, dokununca kalp + balon; `arzu:tilki` geçidi), `KalpAskisi.tsx` (sarkaç; dokun → patlama + not; 3 dokunuş/uzun basış → karşılama), `CiftGizli.tsx` (sağ alttan bakan çift), `Fisiltilar.tsx` (sayfa/saate göre sade notlar, `mesajlar.ts`), `KalpAvi.tsx` (saklı kalp, sayaç `medsoru_arzu_kalpler`, 1/5/10/25/50/100 notu), `sallama.ts` (telefonu sallayınca geçit, iOS izni ilk dokunuşta), `kalpPatlamasi.ts` (WAAPI parçacık + halka). Klavye: metin alanı dışında "arzu"/"tilki"/"kalp".
- Stil `src/styles/arzu.css` (katman sırası, koyu tema, `prefers-reduced-motion` → durağan, `hover` yalnız fareli cihazda, güvenli alan). Marka simgesine kalp rozeti (`:root[data-arzu]`).
- Tuzaklar: (1) SVG `transform` özniteliği olan gruba CSS animasyonu uygulanınca öznitelik ezilir (baş sol üste kaydı) → dış `translate` grubu + iç animasyon grubu, `transform-box: fill-box`. (2) v11 genel `[role=dialog]` `max-height` kuralı (özgüllük 0,3,0) tam ekran karşılamayı kısıp alt çubuğu gösterdi → `.ar-kars.ar-kars.ar-kars { max-height:none }`.
- Kullanıcı düzeltmeleri: klişe/abartılı sözler sadeleştirildi, imza ve "tıpkı bizim gibi" kaldırıldı. Sınama: 5175 önizleme, yapay zekâ test oturumu + `medsoru_arzu_onizleme=1`; masaüstü/telefon/koyu tema ekran görüntüleriyle.

## 2026-11-02 (2) — Yönetici onaylı şifre, öğrenci numarasıyla giriş, Drive ve SMTP sağlamlaştırma (H467, onem 618)
- Şifre talebi: `deploy/pg/sql/kimlik.sql` (`auth_sifre_talepleri`, `auth_hesaplar.ogrenci_no`), `yerelKimlik.ts` (`POST /api/kimlik/sifre-talebi`, `.../durum`; yönetici `GET /api/admin/kimlik/sifre-talepleri`, `POST .../karar`), istemci `SifreTalebi.tsx` + `auth.ts` (`sifreTalebiGonder/Durumu`, `medsoru_sifre_talebi_v1`), yönetim `manage16/sayfalar/SifreTalepleri.tsx` (menü Kullanıcılar › Şifre talepleri, SSE `sifre_talebi`, yöneticiye web push). Eski hesapla giriş/kayıt denemesi talep formunu açar; onaylanınca talep eden cihaz kendiliğinden girer (durum 20 sn'de bir sorulur).
- Giriş alanı "E-posta ya da öğrenci no" (öğrenci, eski kart, yönetim girişi). Kayıtta aynı öğrenci no ikinci hesaba verilmez.
- Drive (alt ajan denetimi): okul + öğrenci Drive'ı herkese açık yolla yerelde ve Oracle'da çalışıyor; servis hesabı askıdaki projede (`invalid_grant`), Oracle'da hiç bağlı değildi. `02-download.mjs`: `free_uc` ikinci yol, uuid onay sayfası, servis hesabı hatası bir kez günlükte. `DriveSaveModal` yalnız PDF indirme; App otomatik Drive yedeği kalktı, `medsoru_drive_token` silinir. `ogrenciDriveRoutes /indir` hedef yolu izinli köklerle sınırlı.
- SMTP (Site › Bildirim kanalları): servis seçimi kalktı (sunucu adı belirler), port değişince `secure` porttan, `POST /api/admin/smtp-test {yalnizBaglanti}` göndermeden sınar, Google dışı hazır sağlayıcılar (Brevo, Resend, Mailjet, Zoho) + Gmail uyarısı; Google'a özgü hata metinleri genelleştirildi.
- Eski konsol metinleri: tanılama penceresi, eski yönetim paneli, alt ajan izleyici, çıkmış içe aktarıcı, v12/v14 sağlık satırlarından Firebase kartı/kip/aktarma bölümleri kaldırıldı; `multiDbManager` 'firebase' kipini kabul etmez; sağlık izleyici yalnız meds-pg'ye bakar.
- Sınama (yerel): curl ile talep → yanlış takip → onay öncesi giriş reddi → dışarıdan onay 403 → onay → ikinci onay 409 → cihaza tek seferlik oturum → e-posta ve öğrenci no ile giriş; tarayıcıda form → bekleme kartı → yönetici onayı → kendiliğinden giriş. tsc 0, vite build.
- Kullanıcıya kalan: Drive kimlikli yedeği (yeni GCP projesi + servis hesabı ya da `rclone config reconnect meds:`); `~/.config/rclone/rclone.conf` `client_id` alanında düz metin API anahtarı duruyor; iki `.env`'deki `GOOGLE_SERVICE_ACCOUNT_FILE` artık ölü.

## 2026-11-02 — Google/Firebase tamamen kaldırıldı: kendi kimlik sistemi (Oracle meds-pg) (H466, onem 617)
- Belirti: Google/Firebase projesi askıya alındı (`Consumer 'projects/990828780858' has been suspended`); giriş tamamen durdu, zorunlu giriş kapısı yüzünden site kullanılamadı. Veri zaten meds-pg'deydi; tek bağımlılık kimlikti (+ sunucuda Firestore dinleyen köprü).
- Sunucu: `src/services/yerelKimlik.ts` (`/api/kimlik/{kayit,giris,yenile,cikis,kod-gonder,kod-dogrula,sifre,profil,ben}`, yönetici `/api/admin/kimlik/{hesaplar,sifirlama-kodu,oturumlari-kapat}`), şema `deploy/pg/sql/kimlik.sql` (açılışta uygulanır; `auth_hesaplar`/`auth_oturumlar`/`auth_kodlar`), `src/services/kimlikDogrulama.ts` (eski `firebaseIdentity.ts` yerine; HMAC-SHA256 erişim jetonu 1 sa, ağsız doğrulama; anahtar `MEDS_AUTH_SECRET` ya da `data/.kimlik_anahtari`). Yenileme jetonu 180 gün, özetiyle saklanır; "oturumları sonlandır" yenilemeyi de reddeder. scrypt şifre özeti; kod 6 hane/15 dk/5 deneme; hız sınırları.
- Göç: `users` + doğrulanmış `user_data` e-postaları **aynı uid** ile `auth_hesaplar`'a (`kaynak='firebase-gocu'`, şifresiz). Giriş/kayıt denemesi `kod: 'sifre-belirle'` döner, istemci kod akışını açar; kod doğrulanınca şifre kaydedilir, uid değişmediği için tüm veri (user_data, notlar, yedekler, başarım) yerinde. Tarayıcıdaki eski yerel veri `userScope` stash'iyle aynı uid'ye geri gelir.
- Kimlik e-postası: `epostaGonder` genel `smtp_config.enabled` kapalı olsa da kayıtlı SMTP bilgisiyle gönderir (Oracle'da genel e-posta 8 Ekim'den beri kapalı; o ayar değiştirilmedi). SMTP gitmezse yönetici Kullanıcılar › Erişim › "Şifre kodu üret" (24 sa) — yeni "Şifre" sütunu belirlenmiş/bekliyor gösterir.
- İstemci: `src/services/auth.ts` yeniden yazıldı (Firebase benzeri `auth` nesnesi; `onAuthStateChanged` dışa açık, `firebase/auth` içe aktarmaları kalktı). Giriş kartı (`UserAuthModal`, `AuthV12`): Google düğmeleri kalktı; `EpostaBaglantiGiris.tsx` artık e-posta kodu akışı (Şifremi unuttum / Şifre belirle, şifresiz kodla giriş). Yönetim girişi (`manage-main.tsx`) e-posta+şifre + kod. Profil şifre metni güncellendi. `AuthErrorModal` + `AuthErrorV12` (Firebase alan adı uyarısı) silindi. `adminFetchAuth` `/api/kimlik/*`'ye jeton eklemez (yenileme kendini beklerdi).
- Kaldırılan: `firebase` paketi, `firebase*.json`, `firestore.rules`, `cloudNotificationBridge.ts` (Firestore dinleyicisi), vite `firebase/firestore` takma adı ve `vendor-firebase` parçası, Google Drive'a otomatik yedek. Firebase'e yazan eski betikler `scripts/archive/`'e (sync-all-to-*, start-*-tunnel, process-scanned-ocr, download-and-process-kurul-notes, background-ai-redactor, build_full_drive_slides, check-online-status; `check:*` npm komutları silindi). `firestoreDb.ts`/`api.ts`/`driveAutomation.ts` eski çağrıları `firestoreKapali.ts` boş modülüne bağlı (bayrakla zaten kapalı).
- Sınama (yerel): curl ile kayıt/giriş/yanlış şifre/yenile/çıkış/sahte jeton/göç hesabı/kod (yanlış, doğru, tekrar)/yönetici ucu dışarıdan 403; tarayıcıda kayıt → giriş → yenileme sonrası oturum kalıcı, yedek/not/başarım/varlık uçları 200. `tsc` 0, `vite build` tamam. Firestore günlük satırı yeniden başlatmadan sonra 0.
- Kalan (Google'a bağlı ama zorunlu olmayan): Google Fonts yazı tipleri (hesapsız CDN), Drive içerik hattı (`drive.ts`, öğrenci Drive, `drive_yeni_pdf`) ve Gemini anahtarları (kural 20 kilidi) yerinde; Gmail SMTP (nofrostlife@gmail.com) kimlik kodları için kullanılıyor — Google dışı bir SMTP'ye geçmek yalnız `data/smtp_config.json` ayarıdır.

## 2026-11-01 — KMB: Lottie 2B hattı (30 video) + Hikâye filmi (eski hat korunur; canlıya gönderilmedi)
- Kullanıcı kararı: Lottie videoları da tam 2B çizgi film diline geçsin, ESKİSİ KORUNSUN; tüm videolar kazanım ve öğretici bulgularla tek hikâye gibi tam ekran oynasın.
- Yeni hat `scripts/kmb/lottie2b/`: `svg_disa.mjs` (2B SVG sahneleri + öge kutuları, başsız Chrome) → `svg_lottie.py` (SVG → Lottie katmanları: tüm yol komutları, dönüşümler, objectBoundingBox degradeler, gs degrade çizgi, evenodd, ok ucu, pathLength dasharray) → `sahne2b.py` (`Sahne2B`) + `ortak2b.py` (koreografi yardımcıları, `ic_ekle2b`, `adim`) → `uret2b.py`/`uret2b_a.py`/`uret2b_b.py` (12 konu videosu) ve `adim2b.py`/`adim2b_a/b/c.py` (18 adım videosu) → `src/data/kmb/lottie2b/` (index.json, adimlar.json). Anatomi/el/araç 2B sahnelerden gelir (tek kaynak); üreticiler yalnız koreografi. Bölüm metinleri eskiyle birebir (ses klipleri değişmedi). `lottie_dsl.ic_ekle(modul=…)`, `kare_onizle.mjs LOT=…`, `lottie2b/kare.mjs` tek kare aracı.
- Üretim 1 referans (erkek-ilerleyis) + 5 paralel alt ajan; her video `kare_onizle` 360 px'te 0 otomatik bulgu + göz denetimi (30/30), `dogrula.py` 0 HATA. Düzeltilen tuzaklar: degrade çizgi `gs` olmadan ön kol koyu çıkıyordu; `uret2b_a._son` alt kompozisyonda (Ic) bölüm listesi olmadığı için çöküyordu → harita uzunluğu.
- Oynatıcı `LottieVideo.tsx`: aynı ad için `lottie2b/` varsa 2B, yoksa eski; `localStorage.medsoru_kmb_lottie_eski='1'` eski hattı zorlar. Eski üreticiler/çıktılar silinmedi.
- Yeni `HikayeFilmi.tsx` (+ `kmb.css .kmb-hk-*`, Öğret ve Videolar sekmelerinde "Hikâye filmi" düğmesi, `?hikaye=1`): açılış kartı (amaç + içindekiler) → her bölüm için kazanım kartı (hedef ilk geçtiği bölümde) → 2B adım videosu (EMA sesi) → öğretici bulgular (puf, dikkat, hedef kartının sık hatası) → bitişte 15 kazanım onay listesi; kartlar 6–14 sn geri sayım, video bitince otomatik geçiş, bölüm şeridi/klavye. Başsız Chrome'da masaüstü + 390 px sınandı, konsol hatasız.
- Belge: `docs/KMB_2B_STIL.md §4`, `KMB_GORSEL_ASISTAN.md` A8e. Commit edildi; kullanıcı onayıyla **canlıya dağıtıldı** (`dagit.sh`, sürüm 20261101021248, onem 616; yalnız ön yüz).

## 2026-11-01 — KMB: 2B düz çizgi film geçişi tamamlandı (14 SVG sahne + Lottie paleti; H465; canlıya gönderilmedi)
- Kullanıcı 2B stili onayladı, örnek karedeki mantık hatalarını bildirdi → **H465**: sırtüstü gövdede iç organlar "ayakta" dizilimindeydi. Erkek sahnesi tek yön sistemiyle (inferior = sağ, anterior = yukarı) yeniden kuruldu: simfiz derinin altında, mesane arka-üstte, prostat arkada, bulbar üretra perinede, penis eldivenli elle dik, skrotum kök arkasında, uyluk + örtü + küvet; idrar yalnız balon yerleşince akar.
- Kalan 13 sahne üç paralel alt ajanla sıfırdan çizildi: `sahneler_2b_a.tsx` (foley, foley-kesit, malzeme, maket), `sahneler_2b_b.tsx` (mesane, yakin-mesane, yakin-uretra, travma), `sahneler_2b_c.tsx` (kadin, yakin-kadin, yakin-erkek-jel, yakin-el, pozisyon). Ortak sözleşme `sahneOrtak.tsx` (tipler, `Ortak` degradeler + `kmb-2b-*` palet, `Boru`); `sahneler.tsx` yalnız Erkek + kayıt (eski gerçekçi çizimler kaldırıldı, 1269 → 233 satır). Öge kimlikleri/`gizli` semantiği değişmedi; `dogrula.py` MALZEMELER'i 2B dosyalarından da okur → 0 HATA.
- Stil ve doğruluk sözleşmesi: `docs/KMB_2B_STIL.md` (palet, kontur, 1 cm ≈ 12 px, H462 ①–⑦ + yön sistemi, kare denetimi komutları). Göz denetimi: her sahne `--goster --etiket` + gerçek vuruş kareleri (`sahne3b_onizle.mjs --film`, 90 kare temas sayfası `meds_temp/kmb/stil/film_sheet.png`); etiket çakışmaları, iç içe geçmeler ve örtülen ögeler düzeltildi (ilaç oku üretradan, levator/rektum sırası, travma kırık etiketi, meatus/jel etiketleri).
- Lottie (30 video): geometri doğru olduğundan korundu, palet 2B tonlarına alındı (`lottie_uret.py`, `adim_lottie.py`, `lottie_dsl.py`: deri, mesane, idrar, kemik, eldiven) ve videolar yeniden üretildi; `kare_onizle.mjs` 0 yeni bulgu (balon-sisme'deki 2 "10 mL altyazı bölgesi" bulgusu eskiden beri var).
- Commit edildi; kullanıcı onayıyla **canlıya dağıtıldı** (`dagit.sh`, sürüm 20261101011450, onem 615; yalnız ön yüz, sunucu yeniden başlatılmadı).

## 2026-11-01 — KMB: film yakınlaştırma düzeltmesi + 3B deneme ARŞİVE (H462–H464; canlıya gönderilmedi)
- `HedefFilmi`: yakınlaştırma ≤1,35 ve odak kutusu kadrajın en çok %70'i; veri zoom tavanı 1,35 (`dogrula.py` 1–1,4), vuruşlara isteğe bağlı `aci` (kamera açısı) alanı.
- 3B deneme (`components/kmb/sahne3b/`: `Sahne3B.tsx` motor, `yardimci.ts` malzeme/geometri/organik marching-cubes, `sahneler3b*.ts` 14 sahne; `SahneGoster` seçici; `scripts/kmb/sahne3b_onizle.mjs` başsız Chrome kare alıcı; `KmbAsistan` `?sahne=` önizleme rotası; `dogrula.py` 3B öge kapısı). Kullanıcı denetiminde kalite yetersiz bulundu (iç içe geçme, kesik kadraj, boncuklu yüzey, katı "antiseptik", insana benzemeyen anatomi) → **arşiv**: varsayılan kapalı, düğme yok, öğrenciye görünmez. Ders: H462 (2B yeniden çizim kuralları ①–⑦).
- Karar: ön yüz 2B'de sürer; hedef stil düz vektör çizgi film (referans Foley illüstrasyonu). Sonraki iş: SVG sahne kitaplığı + Lottie adım videoları bu stilde yeniden çizilir.
- Commit yapıldı, dağıtım YAPILMADI (kullanıcı kararı).
- **2B stil örneği:** `sahneler.tsx` Erkek sahnesi düz vektör çizgi film diliyle yeniden çizildi (sırtüstü hasta, alt karın kesit penceresi, mesane/prostat/sfinkter/üretra, penis yatay, kateter meatus→mesane, balon, Y bağlantı → böbrek küvet + enjektör; ölçek 1 cm ≈ 12 px). Önizleme `scripts/kmb/sahne3b_onizle.mjs` artık varsayılan SVG (`--uc` ile 3B), kare `meds_temp/kmb/stil/erkek_2b_ornek.png`. Kullanıcı stil onayı bekleniyor; onayla kalan 13 sahne + Lottie videoları aynı dille çizilecek.

## 2026-10-31 — KMB Hedefler filmi: öğrenim hedefleri tam ekran animasyon (H461)
- Yeni `components/kmb/HedefFilmi.tsx`: Hedefler sekmesindeki 15 KMB öğrenim hedefi ayrı bir tam ekran filmde art arda oynar. Lottie değil; SVG sahne kitaplığı gerçek zamanlı sürülür: her cümle bir vuruş (`hedefCalisma[].film[i]`: sahne değişimi, biriken eylem, `odak` + `zoom`), kamera odak ögesinin gerçek kutusuna (getBBox) CSS geçişiyle yaklaşır, odak dışı alan spotla loşlaşır, etiketler yakınlaşmada aynı boyda kalır (`SahneCiz olcek`). Evreler: başlık kartı (hedef no + belge metni) → Ne / Nasıl / Neden → Sık hata (kırmızı çerçeve + sarsıntı) → Hoca sorar (`h-N-s` sesi, 5 sn düşünme halkası, "Cevabı göster") → sonraki hedef; bitişte 15 hedefin onay listesi + Sınava geç. Ses `h-N` klipleri (cümle zamanlı), ses yoksa sessiz kip. Denetimler 3,2 sn'de gizlenir; hız, "Sorular" anahtarı, klavye (boşluk, ←/→ cümle, PgUp/PgDn/J/L hedef, f, Esc). İzlenen hedefler `medsoru_kmb_hedeffilm_02`.
- `02.json`: 15 kartın tümüne `film` koreografisi (6 vuruş; hedef 5/9/10/11/15'te sahne geçişleri: kadın↔erkek, yakın plan mesane↔üretra, malzeme↔kesit). `dogrula.py` film kapısı (vuruş sayısı = cümle, sahne/öge/odak kimliği, zoom 1–2) → 0 HATA. `kmbVeri.ts` `FilmVurus`.
- `kmb.css` `.kmb-hf-*`; Hedefler yan şeridinde `.kmb-hf-ac` düğmesi (yatay şeritte dar kart — width:100% tüm şeridi 950 px'e uzatıyordu, düzeltildi).
- Tuzaklar: klip gerçek süresi `ses_02.json sure`den birkaç ms kısa → `audio.ended` bölüm sonu sayılır (ilerleme %98'de asılı kalıyordu); hızlı hedef geçişinde eski klibin kesilen `play()` sözü AbortError verir → yalnız NotAllowedError duraklatır; dikeyde denetim satırı sığmayınca grid sütunu genişleyip sahneyi kesiyordu → `minmax(0,1fr)` + sarma.
- Yerel 3000'de sınandı (1280×800 ve 375×812): başlık kartı, cümle akışı, kamera/spot, sık hata, soru + düşünme, hedef geçişi, bitiş ekranı. Commit/dağıtım yapılmadı.

## 2026-10-31 — KMB Lottie videoları kare denetimi ve onarımı (H460)
- Yeni araç `scripts/kmb/kare_onizle.mjs`: başsız Chrome + lottie-web canvas ile her bölümün başı/ortası/sonundan kare,
  oynatıcının etiket katmanını taklit eder, cümle metniyle temas sayfası + `rapor.json` (kesik/taşan/çakışan etiket, boş kare).
- `lottie_dsl.py`: kamera hareket listesi + `kamera_coz` (kayan kamera hatası), `etiket_yerlestir`/`etiket_denetle`
  (kadraj, altyazı bölgesi, çakışma, ≤30 harf), `Ic` eşlenmeyen bölüm "olmuş bitmiş" (`'once'`), sahne sayacı → etiket.
- `adim_lottie.py`/`lottie_uret.py`: 45 etiket kısaltıldı; sistit küçük iltihaplı mesane, travma neden/kırık/yalnız kırık
  ayrımı + penis/kan yukarı, malzeme alt raf ve steril alan sınırı, kateter boyları, torba kamerası, vulva perine zemini,
  erkek temizlikte eldiven değişimi paneli, idrar gelmezse iki neden yan yana, yeni cümle metinlerine uyan etiketler.
- `dogrula.py` etiket kapısını çağırır (0 HATA). 02.json ve ses dosyalarına dokunulmadı; commit/dağıtım yapılmadı.

## 2026-10-31 — Soru dışa aktarıcı: çok katmanlı gruplama, ders renkleri, sayfaya sığdır, etiket görünümü, yalnız doğru şık (H456)
- `v15/soruAktar/ayar.ts`: `gruplar: Alan[]` (yıl/kurul/ders/konu/kaynak/tür/zorluk/etiket, en çok 4 iç içe katman; eski `grupla` kaydı katmana çevrilir), `grupSirasi` (olağan / soru sayısı), `grupStil` (alt çizgi, bant, kutu, sade), `grupSayi`; 12 sıralama kipi (`SIRALAMALAR`: yıl eski önce, zordan, kaynak numarası, kısa/uzun, A→Z …); `dersRenkleri` + `DERS_RENK`/`dersRengi` (sitedeki `health.css` ders renkleri; eşleşmeyen ders ad karmasıyla ek listeden); `sigdir` (kapalı / yalnız küçült / doldur) + `sigdirHedef`; etiket görünümü (`etiketBoyut`, `etiketDizilim`, `etiketSekil` hap/kutu/köşeli/çerçeve/düz, `etiketRenk` gri/türüne göre/dersin rengi/özel, `etiketZemin/Metin`, `etiketKalin`); `cozumIcerik.yalnizDogru`.
- `kaynak.ts`: `AQ.etiketler` (çıkmış `tags` + rozetler; süreç etiketleri `_`, `donem3-…`, yıl, dosya adı, ders/yıl kopyası ve Faz 14 rozeti ayıklanır), süzgeç `etiketler`, `secenekler('etiketler')`.
- `belge.ts`: `katmanla` (kararlı çok katmanlı kümeleme, katman sırası yıl yeni önce/metin yıllar sona, kurul no, zorluk, kaynak sırası, etiket sıklığı), `HS.gruplar/grupRenk/dersRenk`, başlık rengi mirası (ders başlığı dersin rengi, alt katman üstünden), `katmanBasliklari` → akışta başlık blokları (`.gb.s0–s3`), ızgarada yalnız en üst katman sayfa bandı + hücre içi `basliklar` (H456); `sayfala` → `sigdirarak` (seyrek bölüm sonu ölçütü `Sayfa.dolu/yeniBolum`, ikili arama 0,6–1,35, `Belge.olcek/sigdirNot`), `Olcer.sigdir(k0)` + `enBuyuk`; etiket rengi `etiketler().renk` (HTML/DOCX/PPTX ortak), `cozumIcerik` yalnız doğru şık (doğru seçeneğin gerekçesi, çeldirici satırı yok).
- `docx.ts`/`pptx.ts`: katman başlıkları (seviye puntosu, girinti, bant/kutu/çizgi), hücre içi alt başlıklar, etiket biçimleri (dolgu/`w:bdr` çerçeve/düz ayraçlı; PPTX vurgu dolgusu), akışta ölçek tabanı `belge.olcek` ile.
- `SoruAktarV15.tsx`: Sıralama/Gruplama (katman ekle-kaldır, hazır dizilimler, grup sırası, başlık biçimi), "Sayfaya sığdır" bölümü (hedef sayfa, ölçek bilgisi), Renk sekmesi (zorluk/etiket alanı, "Her dersin kendi rengi", etiket görünümü bölümü), Çözüm "Yalnız doğru şıkkı açıkla", süzgeçte Etiket; CSS `sx15-katman`.
- Sınama (yerel 3000, 40 çıkmış soru, yıl › kurul › ders › konu): önizleme 22 sayfa = sunucu PDF 22; DOCX LibreOffice 21 sayfa (çözüm akışı Word'de kendi sütun akışı), PPTX 26 slayt (16:9 geometri), tüm XML parçaları ayrıştı; hedef 10 sayfa → ölçek %77 ile 10 içerik sayfası; yalnız doğru şık 30 → 16 sayfa. Commit/dağıtım yapılmadı.

## 2026-10-29 — v15 üst çubuk arka plan göstergesi stilsizdi (H439)
- `ap15g` kuralları tembel yüklenen `kisisel.css`'ten kabuğun `shell.css`'ine taşındı; kart çerçeve/zemin ve etiket stili kendine yeterli. Yerel tarayıcı ekran görüntüsü alınamadı (yerel sekme açılışta takıldı); derlenmiş ana CSS'te kuralların varlığı doğrulandı.

## 2026-10-29 — Kurul 2 (2026-27) ara soruları üretildi: 7 ders, 77 soru (kural 27)
- k2-01 (5), k2-02 (9), k2-03 (13), k2-04 (12), k2-05-v2 (12), k2-07 (12), k2-08 (14); k2-06'nın sesli dersi yok. Branş `k2hocaara`, kodlar 2a01…2a08; veri `src/data/k2hocaara_cozucu/`, ses `data/k2hocaara_cozucu/ses/` (EMA, GPU).
- Tıbbi kaynak yalnız PDF sayfa metni (pymupdf); ders akış metni yalnız slayt eşlemesi için (Whisper hatası riski). Yazar alt ajan + bağımsız denetçi; 6 derste denetçi düzeltmesi, düzeltilen 21 soru ikinci denetimden GEÇER (H436). `kur.py dogrula --ses` 7/7 0 HATA.
- k2-05 için yalnız `k2-05-norolojik-muayene-v2` anahtarına bağlandı (eski anahtarda ara sayfa çıkmaz).

## 2026-10-29 — Sesli derste "Hocanın sorabileceği soru" ara sayfası + ünlem modu (AGENTS kural 27)
- Ön yüz: `canliDers/CdHocaAra.tsx` (slaytın son paragrafı bitince ders durur → yapay soru sayfası; EMA oku → 5 sn düşün → çöz `c/d` → slayttan anlat `a-N` → derse dön; PDF çubuğunda ünlem = tümü ardışık), `styles/v15/hoca_ara.css`; ders sayfasında "Hocanın sorabileceği sorular" kartı (`dersAraCozucu`), çözücü branşı `k<N>hocaara` (`brans.ts`), `CSoru.ara/anlatim`, `DersSoruTur 'hoca'`.
- Hat: `scripts/hoca_ara_soru/kur.py` (iskele/dogrula/birlestir; kapılar: ileriye sızıntı, dayanak, slayt atfı, şık/üslup, profil, `--ses` klip eksiksizliği), `TALIMAT.md`; `spot_cozucu/ses.py` `anlatim` → `a-N` klibi; `hat.json` `hoca_ara_soru`, el kitabı §19 11d, standart §2 13b.
- Yerelde deneme verisiyle sınandı (ünlem modu, ders içi otomatik açılış + sürdürme, ders dışı çözücü); deneme verisi silindi. Henüz hiçbir derste ara soru verisi yok (yeni derslerle üretilecek).

## 2026-10-28 — Sesli ders: adsız gönderme yasağı (H434)
- `metin_denetle.py` BAGLAMSIZ kapısı (paragraf başında "bu hastalıkta/durumda…", "burada", "bunlarda" → HATA); kural KURUL2_DERS_STANDARDI §8.13, ANLATIM_KURGU_STANDARDI, hata defteri H434. Mevcut dersler toplu değiştirilmedi. Commit/dağıtım yapılmadı.

## 2026-10-28 — Öğrenci yerleşim bulguları (H230–H241)
- H230 `dersler.css` d15-tools 4 sabit sütun → auto-fit (3 araçta sağ boşluk). H231 `v12/cards.css` kartlar başlığı telefonda tek satır + deste satırı soluk kenar.
- H232 `rebuild.css` ≤420 px soru kartı başlığı: araç 30 px, ders hapı içerik kadar. H233/H234 `test-builder.css` "Testi oluştur" yapışkan alt bilgi, ders hapı kaydırma ipucu.
- H235 `v15/soru.css` PC'de eylem çubuğu soru içeriğinin hemen altında. H236/H237 `baslangic.css` 4 ders kartı 4 sütun, "Nasıl çalışır?" hapı satırda.
- H238 `cevrimdisi15.css` ≥600 px kurul çipleri sarar, toplu indir çipleri sıkı. H239–H241 `DersProgramiV15.tsx`: sesli ders bağlantısı yalnız bu yılın anahtarı + `ders_id_tam` birebir; glob anahtarı yanlış olduğu için Kurul çipleri hiç çizilmiyordu (programVar); tarihsiz dersler "Invalid Date" yerine "Tarihi belirsiz".
- Commit/dağıtım yapılmadı.

## 2026-10-28 — Terim / kısaltma / bilgi paketi hazır sesleri (EMA GPU)
- `scripts/sesli_anlatim/terim_ses_uret.py` (başlatıcı `patoloji_cozucu/cozucu_ses_gpu.sh`, kural 10 ikinci istisna yolu): PDF terim yardımcısı (`sesli_anlatim/terim|kisaltma`), `ders_icerik` (terim/kısaltma/bilgi) ve iki genel sözlükten **5.615 benzersiz** "başlık + 1-2 cümle" klibi → `data/terim_ses/<h2>/<h>.mp3` (226 MB, ~10,3 sa, 0 hata) + `kayit.json`. Anahtar `h = sha1("terim-1|"+başlık+"|"+tanım)[:12]` (ekrandaki metinle; `anahtar()`); yeniden çalıştırma yalnız eksik/değişeni üretir.
- Kök neden/ders: Unicode simgeler (α, β, ⁺, ₂, ≥, µ, ²) EMA'da "unikod U artı 207A" diye okunuyordu; `konus()` okunuşu Türkçeleştirir (alfa, artı, büyük eşit, mikro, kare, yüzde, bölü, CYP 2 D 6). Başlık tek başına sentezlenince süre denetimi şaşıyordu → başlık+tanım tek paragraf. Yeni terim/bilgi kaynağı eklenirse simge içeriyorsa `konus()`'a kural eklenir.
- Henüz arayüze bağlanmadı ve Oracle'a taşınmadı (rsync + `anahtar()` ile arama gerekir). Commit/dağıtım yapılmadı.

## 2026-10-28 — Soru çözücü / En önemliler başlangıcı: kurul süzgeci hatası + sade tasarım (H124)
- `spots/BransBaslangic.tsx`: liste seçili kurula göre (`useSeciliKurul`), "Tümü" yok, "Kurul N" öneki atılır, başlanmışlar önde; başlık "Kurul N dersleri".
- `ui/Baslangic.tsx` v15 dalı + `styles/baslangic.css`: kurul şeridi ile özet tek satır, vurgulu devam kartı, halka yerine alt ilerleme çubuğu + yüzde, üzerine gelince yükselen kart/kayan ok/"Başla", basınca küçülme; alt bağlantılar ayraçlı tek satır.
- `olasi-sorular.css` `.ks` → `.ks.kseridi` (kurul seçicisine kutu çiziyordu). Canlıya gönderilmedi.

## 2026-10-28 — Kaynak sayfa kapısı (H109) + Favoriler (★/↻, Bugün, PDF)
- `scripts/ders_icerik_kaynak.py` (adim→slayt→PDF sayfası `s`) k2-01..08 paketlerine uygulandı (650+ terim); kaynaksız 2 terim silindi; `ders_icerik_dogrula.py` `s` eksik/iskelet terimde HATA; el kitabı §19 11a + H109.
- Favoriler: `services/favoriStore.ts` (`medsoru_favoriler_v1`, userKvSync'te), `v15/FavDugme.tsx` (ders içerik kartlarında), `v15/FavorilerBugun.tsx` (Bugün, kaynağa gider, ders/slayt/sayfa bilgili maddeli PDF = iframe yazdır). Canlıya gönderilmedi (dagit.sh bekliyor).

## 2026-10-27 — Quiz her ders için açık + örnek soru kapsamı (k2-05, k2-08)
- Farmakoloji kapsam kilidi kalktı (`quiz_motoru/kapsam.py`, AGENTS kural 19); `quiz_dogrula.py` artık `sik_aciklama` standardını da denetler; elle üretilen ders yayınlı sesli dersle "tamamlandı" sayılır.
- `quiz_havuzu.json` (meds_database_v2/ders_isci/yayinlanan/elle-k2-05|k2-08/): k2-05 116 atom/232 soru, k2-08 205 atom/410 soru, 0 HATA. Kaynakta çelişkili/görsele bağlı/kanıtı eşleşmeyen atomlar havuza alınmadı (k2-05: 12, 33, 36; k2-08: 056, 057, 068, 083, 093, 131, 188, 198, 211). Quiz havuzu henüz sitede bir ekrana bağlı değil.
- Örnek soru kuralı (önem tamamı + ayrıntı ~%40, 50<n≤100; `KURUL2_DERS_STANDARDI.md` §10.8, bundan sonra her ders): k2-05 34→69, k2-08 43→95, canlıda (onem 484). `s16` kazanım tavanı `100-3*(kaz-1)`. k2-05'te monoparezi/stupor vb. tanımlar slaytta yalnız terim; açıklamalar genel tıp bilgisinden.

## 2026-10-27 — k2-05 Nörolojik Muayene Faz C: çizim, önem/çözücü/asistan
- Çizim 63 (52 kontur + 11 şablonlu panel; `data/sesli_anlatim/cizim/k2-05-norolojik-muayene.json`), kapılar 0 HATA; önem 42 madde, çözücü 20 soru, asistan 33 nokta (`src/data/k2noroloji_*/2n03.json`), EMA sesi (çözücü 181, asistan 183 klip); quiz envanteri 119 atom.
- Hata H116: birleştiriciler branştaki eski dersin dosyalarını da yeniden yazıyor; elle zincirde yalnız yeni ders dosyaları sahnelenir.



## 2026-10-27 — Kurul 2 k2-08 Beyin ve İskelet Sistemi Gelişimi Genetiği (Tıbbi Genetik 1) — Faz B (aşama 7–11) tamam
- Anlatım: 16 bölüm · 86 paragraf · 422 cümle · 5.611 kelime (≈50 dk); `metin_denetle` 0 HATA, `konusma_v2 --dogrula` 0 HATA, bağımsız öğrenci denetçi tur 1 KALIR → düzeltme → tur 2 GEÇER (H112).
- Hocanın sınav özeti (32:36–36:50): HOX/OTX/MSX/PAX6 (s10,12,13,15), holoprozensefali oluşum+hasar, trizomi 13/18, üç tip (s23–25), lizensefali (s26), somit/kraniyofasiyal hastalık adları (s31,34,35,37,39), kraniyosinostoz 3 tip (s41), displazi tip adları/FGFR3 (s50,51) ilgili paragrafta + son bölümde özetlendi; 1–44. slayt için "hoca anlattı" yok (kayıt s.45'ten başlıyor). Çıkmış `dogrudan`: HPE siklops (s24), DMD en sık MD (s80); chip 8 soru (6 ilişkili).
- Yayın: Öğren destesi (87 slayt, `--oyun-zorunlu --kurul2` 0 HATA), ders notu, 43 örnek soru, 160 sözlük terimi (`yayinla.py --yerel`), Oracle `ders-ekle` + EMA (21 parça, 2369 sn), cümle/kelime zamanı, anlamsal çapa 422 cümle %98 (0 HATA), PDF işareti kapsama %98, terim 242, kısaltma 75 (H110), `takip_kapisi` 0 HATA. Çizim, önem/çözücü/asistan, quiz, dağıtım Faz C'de.
- Yeni hatalar: H110 (kısaltma elle sözlüğü), H111 (alt ajan çapa indeks kayması), H112 (anlatım denetçi bulguları).

## 2026-10-27 — Yeni PDF standart akışı
- `docs/KURUL2_DERS_STANDARDI.md` §9: yeni PDF geldiğinde karşılama/sınıflandırma (sınama kuralı), üretim, yayın sırası (H97/H99), kayıt. AGENTS.md başına işaret eklendi (AGENTS.md git dışında).

## 2026-10-27 — Sesli ders: çizimsiz resimde zoom takılı kalıyordu
- Belirti: resimde çizim yokken sayfa yakınlaşmış (is-yakin) halde kalıyordu.
- Kök neden: `CizimLayer` kaldırılırken temizlik `kokRef.current` üzerinden sayfayı buluyordu; React ref'i o an boşalttığı için (null) yakınlaşma sınıfı/`--yakin-t` hiç silinmiyordu.
- Çözüm: sayfa öğesi bağlanırken yakalanır, kaldırmada doğrudan sınıf ve değişken silinir. Önleme: unmount temizliğinde `ref.current` okunmaz, öğe önceden yakalanır.

