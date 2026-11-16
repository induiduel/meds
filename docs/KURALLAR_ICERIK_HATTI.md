# İçerik Hattı Kuralları — İşletim Ayrıntısı (AGENTS.md'den taşındı, 2026-11-16)

> Bu kurallar **bağlayıcıdır**. AGENTS.md'de her kuralın bağlayıcı çekirdeği + işaretçisi kalır; komut satırları, yollar,
> eşikler ve adım listeleri burada **kelimesi kelimesine** durur. Numaralar korunur (başka belgelerdeki "kural 21", "kural 26"
> atıfları hem AGENTS.md çekirdeğine hem buraya işaret eder). Amaç: her oturumda okunan AGENTS.md'yi inceltmek.

14. **Kurul 2 Tam Otomatik İçerik Hattı ve Şık Açıklama Standardı (ZORUNLU, kullanıcı kararı 2026-10-18):**
   - Kurul 2 hattına başlamadan önce **`meds/docs/KURUL2_YAPILMAYACAK_HATALAR.md`** okunur: kullanıcının Kurul 1'de gördüğü ve Kurul 2'de tekrarlanmaması gereken hatalar defteri. Kullanıcı yeni bir hata gösterdiğinde oraya madde eklenir.
   - ⛔ **2026-10-27 kararıyla otomatik başlatma KALDIRILDI (bkz. kural 20).** Aşağıdaki üretim zinciri yalnız kullanıcının bu PC'den ya da yönetim panelinden verdiği komutla çalışır.
   - Kurul 2'den itibaren Drive'a gelen her yeni PDF'ten (kullanıcı komutuyla) interaktif ders (Öğren), sesli spot / sınav asistanı ve sesli soru çözücü içeriği üretilir ve **EMA** ile seslendirilir. Hat eksiksiz ve hatasız olmalı: her adımın doğrulayıcısı 0 HATA vermeden seslendirmeye ve yayına geçilmez; yazar + bağımsız denetçi iki geçişi korunur.
   - **Sesli ders dolgu yasağı (2026-10-22):** kelime/dakika hedefi yok; "hoca vurguladı" gibi asılsız meta cümle, tekrar ve geçiş dolgusu yasak; vurgu yalnız çıkmış/öğrenci notu dayanaklı. Kapı `metin_denetle.py` (H22).
   - **Şık açıklamaları** ("Yardım al", yanlış şık, çözücü `siklar`) her şık için kavramın **ne olduğunu**, **ne işe yaradığını** ve **bu soruda neden doğru/yanlış olduğunu** anlatır (2–3 cümle). "Bu sorunun cevabı değil", "… olarak geçmez", "… yapmaz." gibi kısa geçiştirme cümleleri YASAK. Standart: `meds/docs/SIK_ACIKLAMA_STANDARDI.md`; kapı: `meds/scripts/sik_aciklama.py` (asistan ve çözücü doğrulayıcılarına bağlı).
   - **Türkçe üslup:** öğrenciye okunan/gösterilen her metin doğal, eksiksiz ve anlaşılır Türkçe olur; çeviri mecaz ("imzası", "motoru", "freni", "çapası") ve iç yazım etiketi ("Ayrım cümlesi:", "Kısa formül:", "Akılda tut:", "Mantığı şudur:") YASAK. Standart: `meds/docs/TURKCE_USLUP_STANDARDI.md`; kapı: `meds/scripts/turkce_uslup.py`.
   - Kapılar bağlı (2026-10-18): asistan, çözücü ve spot önem doğrulayıcıları her zaman HATA; Öğren `validate_learning_decks.py deck.json --oyun-zorunlu --kurul2`, sınav spotları `sinav_spotlari/dogrula.py --kurul2`. Kurul 2 başlarken ders işçisinin `denetle.py` Öğren çağrısına `--kurul2` eklenir.

15. **Tam Otomatik Hat ve Kurul Geçişi (ZORUNLU, kullanıcı kararları 2026-10-20):**
   - Aşamalar `meds/otomasyon/hat.json` defterindedir; yeni üretim adımı = deftere aşama (baştan kurma yok). İşletim talimatı
     `meds/docs/KURUL_OTOMASYON_EL_KITABI.md`; her değişiklikte güncellenir.
   - ⛔ 2026-10-27: `meds-hat-gece` ve `meds-olasi-soru` birimleri **maskelendi**, Oracle `meds-ders-isci` durduruldu (kural 20).
   - LLM gerektiren işler **yalnız elle komutla** ve Claude (`claude -p`, dar izin listesi) ile çalışır; eski gece hattı `meds-hat-gece.timer`
     (02:30, kaçırılan açılışta), olası soru `meds-olasi-soru.timer` (20:00, 23:30).
   - Aktif kurul yalnız takvimden (`src/services/kurulTakvimi.ts`, `scripts/hat/takvim/aktif_kurul.py`); ders kimliği/kodu yalnız
     ders kayıt defterinden (`src/data/dersler/kN.json`, branşlar `branslar.json`). Kimlikler kalıcıdır (`k2-07`, `k2-07-c0142`).
   - Kurul 2+ içeriği: kapılar 0 HATA (`--kurul2` dahil) + bağımsız denetçi geçmeden yayına girmez; Kurul 1 verisine otomatik
     toplu müdahale yapılmaz.
   - **Kod dağıtımının tek yolu: `bash meds/deploy/oracle/dagit.sh`** (önce commit + `git push origin main`). Betik kilidi
     bekler, origin/main'i temiz worktree'ye (`meds-dagitim`) alır, canlı kirliyse ya da canlı commit hedefte yoksa durur,
     `guncelleme_notu.json` `onem` artmamışsa durur (küçük düzeltme: `--sessiz`), eşitleme commit'ini main'e gönderir.
     `deploy-code.sh`'ı doğrudan çalıştırmak kirli ağaçta ve canlıyı geri alacak durumda reddedilir (acil durum: `--kirli-izin`).
     Gece içerik dağıtımı canlı commit'i `dist/dagitim.json`'dan yeniden derler.
   - Kullanıcının bildirdiği / düzelttiği her içerik hatası `KURUL2_YAPILMAYACAK_HATALAR.md`'ye madde (+ mümkünse otomatik kapı) olarak işlenir.

21. **Ders Değerlendirme: Orijinal PDF + Öğrenci Notu + Hoca Sesi (ZORUNLU, kullanıcı kararı 2026-10-27):**
   - İki Drive: okul (orijinal ders PDF'leri) ve öğrenci (`17K7doMGg0xupQekTD5_Vz9xMXc5gd7BA`: öğrencinin not/işaret/çizim PDF'i + hocanın ses kaydı).
     Dosya adları farklı olabilir; eşleştirme **içerikteki başlıklarla** yapılır, hangi dosyanın hangi ders olduğunu kullanıcı işlem sırasında söyler.
   - Her derste: hoca vurguları (zaman damgalı alıntı), öğrenci işaretleri, **çıkmış soru eşlemeleri** (slayt sağ üstünde yanıp sönen chip →
     ses durur, soru çözülür, kapanınca ders kaldığı yerden sürer), terimler + kısaltmalar sözlüğü (1–2 cümle), bilgi paketleri / önemli yerler.
   - "Çıkmışta soruldu" vurgusu yalnız doğrulanmış eşlemeye dayanır; eşleme teyit edilmeden vurgu yapılmaz.
   - Farmakoloji: dersteki ilaçlar, hastalıklar ve ilişkileri quiz envanterine (`atomik_bilgi_envanteri.json`) kayıt edilir (kural 19).
   - **Yeni ders üretim standardı (2026-10-27, bundan sonraki HER ders; adım adım: `meds/docs/KURUL_OTOMASYON_EL_KITABI.md` §19):**
     arşiv dersi arşivde kalır, yeni ders bu yılın PDF'inden sıfırdan üretilir; işçi/`claude -p` gerekmez, kullanıcı komutuyla
     oturumda yazılır. Zorunlu katmanlar: değerlendirme paketi (`degerlendirme_dogrula.py` 0 HATA) → anlatım metni
     (`metin_denetle.py` + `turkce_uslup` 0 HATA + bağımsız denetçi GEÇER) → `ders-ekle` → EMA ses → cümle/kelime zamanı +
     PDF işareti → doğrulanmış çıkmış chip'i → terim + kısaltma katmanı → **anlamsal çapa + çizim** (kural 17; tasarım
     kataloğunun TAMAMI amaca göre kullanılır, `TALIMAT_CIZIM.md` 27–30, `cizim_kapisi.py` 0 HATA) → atomik bilgi envanteri.
     Eksik katmanla ders "tamamlandı" sayılmaz.

22. **Tam Hat Komutu (kullanıcı kararı 2026-10-27):**
   - ⛔ **Öğren destesi ASKIDA (kullanıcı kararı 2026-11-02):** aksi söylenene kadar tam içerik işçisi etkileşimli/interaktif Öğren içeriği (deste, slayt etkileşimleri, ders sonu oyunları, `interactive_learning_decks.json` girdisi, Öğren EMA sesi) ÜRETMEZ; bu katman "atlandı — kullanıcı kararı" diye raporlanır ve eksikliği dersi tamamlanmamış saymaz. Kural 9/9b yalnız kullanıcı Öğren içeriğini açıkça isterse uygulanır.
   - Kullanıcı "… PDF'i driveye eklendi. İçerik işçisini tüm adımları yapmak üzere başlat" (ya da benzeri: "tüm aşamaları yap",
     "içerik işçisini başlat") derse bu, o PDF için kural 21'deki **tüm katmanların** + aşağıdakilerin açık izni sayılır (kural 20 elle komut şartı sağlanır):
     * Öğrenci Drive'ında not/işaret PDF'i varsa okunur, hoca ses kaydı varsa dökülür; yoksa yalnız orijinal PDF'ten devam edilir (eksiklik gerekçe sayılmaz, durdurmaz).
     * Sesli ders (§19 adım 1–11), **En önemlileri** sayfası (önem listesi + her maddenin örnek sorusu/sesli çözücü: `spot_onem`, `soru_cozucu`, `sinav_asistani`),
       müfredat sadık örnek sorular (kural 4), Öğren destesi + ders sonu oyunları (kural 9b; askıda), atomik envanter (quiz havuzu KAPALI — kural 19, 2026-11-07).
     * Tüm kapılar 0 HATA + bağımsız denetçi geçince `dagit.sh` ile canlıya; sonunda katman katman rapor (hangisi yapıldı/atlandı ve neden).
   - Hangi PDF'in hangi ders olduğu belirsizse sayfa başlıklarıyla doğrulanır, doğrulanamazsa yalnız o noktada kullanıcıya sorulur.

22c. **Tasarruf kipi (kullanıcı kararı 2026-11-07):** kullanıcı "tasarruf modunda" derse tam hat `hazirlik.py --mod tasarruf` ile yürür
   (tek kaynak `meds/scripts/hat/tam_hat/mod.py`, ayrıntı `TAM_HAT_HIZLI_AKIS.md` §0): sesli ders, metin vurgusu/takip, çıkmış analizi, örnek soru +
   sesli çözücü + patoloji hoca soruları kartı üretilir; çizim/çapa, ara resim, ara soru, atomik envanter, PDF taraması, Öğren, quiz ÜRETİLMEZ ve
   "atlandı — tasarruf kipi" diye raporlanır (kural 17/21/27'nin o katmanları bu kipte dersi eksik saymaz). Kapılar ve denetçi aynen.

22b. **Hızlı ve hatasız akış (kullanıcı kararı 2026-10-28):** tam hat `meds/docs/TAM_HAT_HIZLI_AKIS.md`'ye göre yürür:
   E0 hazırlık betiği (paralel, kaynak tavanlı), alt ajanlara yalnız `kural_secici.py --oku <aşama>` listesi, yalnız hatalı
   parçanın yeniden yazımı (sayısal hedeflerde ±%10 tolerans; tıbbi/kaynak/üslup hatasında tolerans yok), çıkmış üslup
   örnekleri + `soru_uslup.py`, `kaynak_kapisi.py`, `pdf_tarama.py` ve ders başına tek denetçi.

23. **Ders İçerik Paketi — her yeni ders için ZORUNLU (kullanıcı kararı 2026-10-27):**
   - Yeni eklenen her slayt/ders için ders sayfasındaki içerik sayfaları (terimler, kısaltmalar, hastalık/kavram kartları, bilgi spotları, önemli noktalar, tablolar, karşılaştırmalar, sıralamalar/listeler, kartlar, örnek ve mini sorular) üretilir: `python3 meds/scripts/ders_icerik_uret.py <key>` + `ders_icerik_dogrula.py <key>` 0 HATA. Eksik paketle ders tamamlandı sayılmaz (el kitabı §19 adım 11a).
   - Slayttan çıkarılabilen HER bilgi paketi çıkarılır; kaynak dışı veri yazmak YASAK, her kayıt slayt/sayfa kaynaklıdır. Sıra türü (numara/alfa/azalan/madde) kayıtlıdır, karşılaştırma `k` işaretli tabloyla ve terazi simgesiyle gösterilir, iç içe madde yapısı korunur. Yeni sayfa türü: veri + ekran + `DersDetayV15` + `meds/docs/DERS_ICERIK_BICIMI.md` birlikte (tasarım–kod uyumu).

   - **Sesli örnek soru çözücü her ders için ZORUNLUDUR (2026-10-27):** dersin örnek soruları için her şıkkı kaynak göstererek (slayt/sayfa) ayrıntılı açıklayan sesli çözücü (`src/data/k2*_cozucu/<kod>.json`, `scripts/uretim/spot_cozucu/TALIMAT_COZUCU.md`, EMA sesi, `cozucu_dogrula.py` 0 HATA + bağımsız denetçi, şık açıklama standardı kural 14) üretilir ve çalışır olmalıdır. `ders_icerik_dogrula.py` çözücü yoksa HATA verir; tam içerik işçisi bunu da yapmadan ders tamamlanmaz.

24. **Dış Ajan Tam İçerik İşçisi: Etiketli, Karantinalı, Yönetici Onaylı (ZORUNLU, kullanıcı kararı 2026-10-29):**
   - Claude dışındaki her ajan (Gemini, GPT, DeepSeek, Antigravity…) tam içerik hattını çalıştırırsa çıktısı `<ders>-ag-<etiket>` anahtarıyla ayrı yaşar (örn. `k2-07-ag-gemini`); mevcut dersin üstüne yazılmaz, v2/v3 artırımı yapılmaz, Claude'un ve sitedeki verilerle karışmaz.
   - `ders-ekle` yalnız `ajan` alanlı çağrıda ajan anahtarını kabul eder (aynı anahtar varsa 409) ve `sesli:/deste:/paket:` görünürlüğünü kendiliğinden `yalniz-yonetici` yapar; yönetici panelden (Site › Görünürlük) onaylamadan öğrenciye görünmez. Ajan kendi içeriğini açamaz.
   - Yol haritası ve hata önleme: `meds/docs/DIS_AJAN_YOL_HARITASI.md` (ZORUNLU okuma); izolasyon kapısı `scripts/hat/tam_hat/dis_ajan_kapisi.py`. Ajana verilecek görev yönergesi `meds/scripts/hat/tam_hat/dis_ajan/TALIMAT_DIS_AJAN.md` (kanıt-önce yazım, `bolum_kontrol.py`, `anlama_sinavi.py`, `hedef.py`); kural 20/22 elle komut şartı aynen geçerlidir.

25. **Patoloji Soruları Hoca Üslubuna Bağlıdır (ZORUNLU, kullanıcı kararı 2026-10-29):**
   - Tıbbi Patoloji dersi için yazılan her örnek soru, önem/vurgu listesi ve "çıkabilecek soru" katmanı (mevcut Kurul 2 dersleri ve bundan sonra eklenecek her patoloji dersi)
     `meds/docs/PATOLOJI_HOCA_SORU_MANTIGI.md` (v2) + `meds/docs/PATOLOJI_SORU_ESLEME_TABLOSU.md` ve işçi `meds/scripts/uretim/patoloji_soru_isci/` (TALIMAT.md) kurallarına göre üretilir.
   - Her önem noktasına en az 2 soru (farklı dönüşüm: birleştirme/kopya+çevirme/ters yön/ad); çıkmış varsa ters yön zorunlu; çeldirici yalnız aynı dersin komşu kavramı; doğru şık en uzun olmaz.
   - Kapı: `python3 meds/scripts/uretim/patoloji_soru_isci/dogrula.py sorular.json paket.json` → 0 HATA (+ şık açıklama ve Türkçe üslup kapıları). Yeni patoloji PDF'i eklendiğinde bu akış çalıştırılmadan ders tamamlanmış sayılmaz.
   - Bu analiz küçük örnekleme (30 soru) dayanır; ilk Kurul 2 patoloji çıkmışı gelince profil yeniden hesaplanır. Kurul 1 verisine toplu müdahale yok; LLM adımları kural 20/22 elle komut şartına tabidir.

26. **Hoca Üslubu Profili ve Kazanım Haritası (ZORUNLU, kullanıcı kararı 2026-10-29):**
   - Tam içerik işçisi (ve dış ajanlar) bir ders/konu hazırlarken önce **`meds/docs/HOCA_USLUBU_YONTEMI.md`** okunur; ders üslubu `python3 meds/scripts/uretim/hoca_profili/profil_oku.py --ders "<ders>" --konu "<konu>"` ile alınır (veri `meds/src/data/hoca_profilleri/`, insan okuması `meds/docs/HOCA_USLUBU/<ders>.md`).
   - Profil: kök kalıbı, **bilgi türü (neden sorulur)**, bilişsel düzey, şık/çeldirici stratejisi, zorluk, kaynağa bağımlılık, tekrar eden çekirdek kavramlar. Önem listesi çıkmış eşlemesiyle BİTMEZ: profilin ilk bilgi türlerine uyan, çıkmışla eşleşmemiş yerler `onem_puanla.py` adaylarından **yazılı gerekçeyle ve `kanit: profil` etiketiyle** eklenir. Anlatım ve örnek sorular konunun ilk 2 bilgi türünü ve tekrar eden çekirdek kavramları kapsar.
   - Örnek soru kapısı: `python3 meds/scripts/uretim/hoca_profili/profil_kapisi.py <ornek_sorular.json> --ders "<ders>"` (soru_uslup.py'ye EK): güven yüksek + ≥20 soru → sapma HATA, aksi UYARI; "hepsi/hiçbiri" her zaman HATA.
   - **Dürüstlük kuralı:** satır önem puanı kanıtlanmış bir belirleyici DEĞİLDİR (2026-27 holdout'ta rastgele düzeyi); kanıtsız satıra "önemli" damgası yasak. Ders-düzeyi üslup profili ölçülmüştür (5/5 derste genel profilden iyi). Yeni sınav/çıkmış gelince `python3 meds/scripts/uretim/hoca_profili/uslup_analiz.py` ile profil yeniden üretilir ve `HOCA_USLUBU_YONTEMI.md` §3 sınaması güncellenir.
   - **Ayrı kart + sesli çözücü (kullanıcı kararı 2026-10-29, ZORUNLU):** hoca üslubu sorular dersin "Bu dersin içerikleri › Soru çöz" bölümünde **"Örnek sorular"a karışmaz**, ayrı kartlarla sunulur: **"Hoca soruları"** (`?b=hoca`, şık şık açıklama) ve **"Sesli hoca çözücü"** (branş `k2patolojihoca`, ders kodu `<kurul>h<sıra>`: 2h01, 2h02 …). Her yeni patoloji dersinde ikisi de üretilir; çözücü içeriği `scripts/uretim/spot_cozucu/TALIMAT_COZUCU.md` biçiminde yazılır, kapı `python3 meds/scripts/uretim/patoloji_soru_isci/cozucu_kur.py dogrula <ders-id>` 0 HATA, birleştirme `cozucu_kur.py birlestir`.
   - **EMA sesi DAİMA GPU'da (kural 10, 2. istisna):** `bash meds/scripts/uretim/patoloji_cozucu/cozucu_ses_gpu.sh meds/scripts/uretim/spot_cozucu/ses.py --brans k2patolojihoca <kod…>` (meds-gpuguard etkin; kapalıysa açılır, açılamazsa CPU'ya düşülmez, çıkış 75). Sesli klip yoksa ders "tamamlandı" sayılmaz; klipler `data/k2patolojihoca_cozucu/ses/` (git dışı, Oracle'a rsync).
   - **Hoca-tahmin hattı (2026-10-29, aynı kural):** önem/çıkabilecek yer listesi ve örnek soru için `python3 meds/scripts/uretim/hoca_profili/tahmin_girdisi.py <ders.md> --ders ... --konu ... --cikti <klasör>` (meds/.venv-ocr/bin/python) → yazar `meds/docs/HOCA_TAHMIN_REHBERI.md` (v5) ile K=10–18 tahmin yazar. 2026-27 ile kör sınamada %62,5 (bekletilmiş) – %69 yakalama; sınırlar `meds/docs/HOCA_USLUBU/TEST_TURLARI.md`. Tahmin satırları önem listesine `kanit: profil` etiketiyle ve gerekçeyle girer; kanıtsız önem damgası yasağı sürer. Ders adı çıkmış bankasındaki adla verilir (Tıbbi Patoloji, Tıbbi Farmakoloji…). Yeni sınav gelince `uslup_analiz.py` + test düzeneği yeniden koşulur.

27. **Sesli Derste "Hocanın Sorabileceği Soru" Ara Sayfası (ZORUNLU, kullanıcı kararı 2026-10-29; bundan sonra eklenen HER ders):**
   - Hoca üslubuna göre soru çıkabilecek slaytın (çıkmış eşlemesi `kanit: cikmis` ya da profil/tahmin `kanit: profil` + yazılı gerekçe; kural 26) anlatımı bitince ders sesi durur, yapay soru sayfası açılır: EMA soruyu okur, çözer ve çözümü **önceki slaytlara numarasıyla dayanarak** anlatır (`a-N` klibi); sayfa kapanınca ders bir sonraki slayttan sürer. PDF üst çubuğundaki ünlem tüm ara soruları ardışık okur/çözer/anlatır. Öğrenci atlayabilir, kendiliğinden açılmayı kapatabilir.
   - Aynı sorular ders dışında çözülür (ders sayfası › "Hocanın sorabileceği sorular", branş `k<N>hocaara`, kod `<N>a<sıra>`); tek kaynak `src/data/k<N>hocaara_cozucu/`. Ders sesi ve ara ses tek seferde tek oynatıcıdan çalar.
   - Soru yalnız o slayt ve öncekilerin bilgisiyle kurulur (kural 7); çeldiriciler öğretilmiş komşu kavramlar; şık açıklama (kural 14) ve Türkçe üslup kapıları; tıbbi doğruluk bağımsız denetçiyle.
   - Akış ve yazım: `meds/scripts/uretim/hoca_ara_soru/TALIMAT.md`; kapı `python3 meds/scripts/uretim/hoca_ara_soru/kur.py dogrula <key> --ses` 0 HATA. EMA sesi DAİMA GPU (`cozucu_ses_gpu.sh … ses.py --brans k<N>hocaara <kod>`, kural 10). Sesi eksik ders tamamlanmış sayılmaz. LLM adımları kural 20/22 elle komut şartına tabidir.

28. **Geçmiş Yıl Öğrenci Önem Notları (ZORUNLU, kullanıcı kararı 2026-10-30):**
   - 2025-26 öğrencilerinin Kurul 2 derleme notları (psk3.2, nöro3.2, tbg3.2, ftr3.2: slayttan kesilmiş en önemli yerler + el yazısı +
     vurgu + yapıştırılmış çıkmışlar) okunup ders başına önem birimlerine çevrildi: veri `meds/src/data/ogrenci_onem/<k2-xx>.json`,
     ders belgeleri `meds/docs/OGRENCI_ONEM/<k2-xx>.md`, yöntem ve isabet ölçümü `meds/docs/OGRENCI_ONEM_YONTEMI.md` (ZORUNLU okuma).
   - Tam içerik işçisi (ve dış ajanlar) **oluşturulmuş ve oluşturulacak her 2026-27 dersinde** bunu kullanır: E0'da `hazirlik.py`
     `ogrenci_onem.json` üretir (elle: `python3 meds/scripts/uretim/ogrenci_onem/oku.py --ders <k2-xx> --sayfalar sayfalar.json`).
     A birimi (çıkmış kanıtlı) → anlatımda ayrıntılı + önem listesinde `ogrenci: {oncelik: "A"}` + ≥2 örnek soru + ara soru adayı;
     B birimi (vurgu + el notu) → anlatımda açık + ≥1 soru. Örnek soru dağılımı ders belgesindeki soru payına ±10 puan.
   - Ekranda "Öğrenciler buraya çalıştı" rozeti: sesli ders v2 cümlesinde `ogrenci: {oncelik, birim}`, önem maddesinde `ogrenci`.
     Rozet ve "geçen yılın öğrencileri…" vurgu cümlesi yalnız kanıtlı A/B biriminde (kanıtsız önem damgası yasağı sürer, kural 26).
   - 2026-27 slaytında karşılığı olmayan birim anlatıma girmez; notun yanlışları (belge §9) kullanılmaz; güveni düşük el notu tek
     başına dayanak olmaz. Kapı: `python3 meds/scripts/uretim/ogrenci_onem/kapi.py <k2-xx>` → 0 HATA (eksik bilgileri listeler, yalnız onlar eklenir).
   - Yeni öğrenci notu gelirse aynı akış: `scripts/uretim/ogrenci_onem/OKUMA_YONERGESI.md` → `birlestir.py` → `basari.py` (yargıç) → `ANALIZ_YONERGESI.md` → `belge.py`.

29. **Ayrıntılı Çıkmış Analizi ve Öğrenci Notu Olmayan Ders (ZORUNLU, kullanıcı kararı 2026-11-06):**
   - Ders analizindeki "Çıkmış sorularda ne soruldu" bölümü soru + cevaptan ibaret OLAMAZ. Her doğrulanmış çıkmış için
     `meds_database_v2/ders_bilgi/<key>/degerlendirme/cikmis_analiz.json` (`{"giris", "sorular": {"<çıkmış id>": {"aciklama": [..], "ornek", "tuzak"}}}`) yazılır:
     **aciklama ≥3 cümle** (sorunun hangi kavramı ölçtüğü, doğru cevabın mekanizması/tanımı slayta dayanarak, en güçlü çeldiricinin neden yanlış olduğu),
     **ornek** (hocanın derste verdiği örnek ya da slayttaki vaka ile pekiştirme), **tuzak** (sınavda karıştırılan komşu kavram). `giris`
     çıkmışların genel eğilimini (hangi alt başlıklar tekrar soruluyor, hangi kök kalıbı) anlatır. Kaynak dışı bilgi yasak.
     Kapı: `python3 scripts/uretim/ders_analizi/uret.py --dogrula <key>` (dosya varsa eksik madde HATA). Ses `ders_analizi/ses.py` ile yeniden üretilir.
   - **Öğrenci notu PDF'i yoksa** çıkmış eşlemesi ve hoca sesi tek önem kaynağıdır: çıkmış taraması (konu + anahtar terim + hoca adı, tüm yıllar)
     iki geçişte yapılır; hoca dökümündeki vurgu ("sorarım", "çıkmıştı", "önemli", "dikkat") ve hocanın örnekleri/vakaları anlatıma, önem listesine
     ve hoca vurgu katmanına eksiksiz girer. Bir derse ait birden çok ses kaydı varsa (ör. TSSB 1 + 2) hepsi dökülür, sırayla birleştirilir.
   - Örnek sorular ve hocanın sorabileceği sorular hoca üslubunda (kural 25/26), çıkmışlara kalıp/kök düzeyinde benzer, önem listesinden ve
     yalnız o slayta kadar işlenmiş bilgiden (kural 7) kurulur.

30. **Ek Modüller: Seçmeli / Geçici Ders İçeriği (kullanıcı kararı 2026-11-10, H544):**
   - Kurul müfredatı dışındaki dersler (ör. seçmeli "Yürüyüş ve Kampçılık") `Ders çalış › Ek modüller` sayfasında yaşar (`/dersler/ek-moduller/kurul<N>/<modül>`);
     kurul hattına, ders kayıt defterine ve Öğren destelerine karışmaz. Veri `meds/src/data/ek_moduller/` (`index.json` + `<modül>/b<N>.json`, `sinav_oncesi.json`,
     `genel_sorular.json`, `hoca_sorulari.json`, `klip.json`), görseller ve PDF'ler `meds/public/ek_moduller/<modül>/`, ekran `src/components/v15/ekModul/`.
   - **Önce hocanın materyali istenir** (not, sunum, çalışma sorusu). Varsa esas kaynak odur: her hoca sorusunun bilgisi anlatımda geçer, hocayla çelişen bilgi yazılmaz,
     sorular hoca üslubunda dönüştürülerek kurulur; hocanın kendi içinde çeliştiği yerde en çok yinelenen değer + ekranda not. Yazım kuralları `meds/scripts/uretim/ek_modul/TALIMAT.md`.
   - Her modülde: sesli ders + spot anlatıcı + sınav öncesi anlatıcı (EMA, DAİMA GPU: `cozucu_ses_gpu.sh meds/scripts/uretim/ek_modul/ses.py --modul <modül>`), konu soruları (yalnız o konuya
     kadar öğretilen bilgi) + genel tekrar soruları + sınav denemesi (sesli çözümlü), küçük etkinlikler, PDF kitapçıkları (`scripts/uretim/ek_modul/pdf.py`). **Ekran metni ile okuma
     metni ayrıdır**: ekranda not (`ekran`), seste konuşma metni (`ses`); okuma metni ekranda gösterilmez.
   - **Sesli ders PDF ile birlikte ilerler (2026-11-10, H546):** ses ve ders kitapçığı üretildikten sonra `meds/.venv-ocr/bin/python meds/scripts/uretim/ek_modul/pdf_esle.py --modul <modül>`
     (`pdf_esle.json`: sayfa, bölüm kutusu, cümle zamanı, cümle → not maddesi; CPU, LLM yok). Ekranda "PDF ile" kipi (`EkPdfDers.tsx`). Ses ya da kitapçık değişince yeniden çalıştırılır; eşleşmeyen cümleye madde uydurulmaz.
   - Kapı: `python3 meds/scripts/uretim/ek_modul/dogrula.py --modul <modül>` 0 HATA + bağımsız denetçi GEÇER olmadan ses ve yayın yok. Klipler `meds/data/ek_moduller/ses/<modül>/`
     (git dışı, Oracle'a rsync); sunucu ucu `/api/ek-modul/ses/:modul/:klip.mp3` (`src/services/ekModulSes.ts`).

31. **Model Sağlayıcısı: OpenDesign Geçidi (ZORUNLU, kullanıcı kararı 2026-11-13):**
   - Claude aboneliği yok; masaüstü uygulaması, terminal `claude` ve ajan hattı **OpenDesign geçidi** üzerinden
     DeepSeek/GLM/GPT/Kimi/MiniMax/MiMo/HY4 modelleriyle çalışır. Yerel köprü `opendesign-kopru.service`
     (127.0.0.1:8787, stdlib python) Anthropic rota adlarını geçit kimliklerine çevirir; tek kaynak
     `meds/scripts/altyapi/opendesign/rotalar.json`, kurulum/denetim `bash meds/scripts/altyapi/opendesign/kur.sh` / `--kontrol`
     (`kopru.py --doctor` eşleme tablosunu `otomasyon/llm/opendesign.py::ESLEME` ile karşılaştırır, 0 HATA şart).
   - Model kimliği koda yazılmaz: `otomasyon/llm/model_sec.py::ajan_model(rol)` (yazar/denetci/hizli) kullanılır;
     yeni betikte `--model <sabit ad>` YASAK. Yazar ≠ denetçi kuralı için denetçi ayrı aileye bakar (glm/gpt).
   - CLI'sız ortamda (Oracle) `otomasyon/llm/opendesign.py` doğrudan `POST /v1/messages` gönderir; anahtar yalnız
     sunucu `.env`'inde (`MEDS_OPENDESIGN_KEY`, `MEDS_OPENDESIGN_URL`) durur, istemciye/repoya yazılmaz. Site AI'sı
     (`src/services/aiProvider.ts`) sırayla Yerel GPU → OpenDesign → Groq → Muse Spark → Gemini dener.
   - **Kural 20 aynen geçerli:** taşıma hiçbir işi kendiliğinden başlatmaz; bütün LLM çağrıları `llm_kilit.py`
     arkasında ve `MEDS_LLM_ELLE=1` (ya da panel bayrağı) ister. Köprü yalnız gelen isteği iletir.
   - Kodlama/tasarım kalitesi için resmî eklentiler `bash meds/scripts/altyapi/claude_eklenti/kur.sh` ile kurulur/denetlenir
     (typescript-lsp, pyright-lsp, frontend-design, code-review, code-simplifier, feature-dev, claude-security,
     security-guidance, pr-review-toolkit, plugin-dev + global LSP paketleri); kapılar `npm run lint` 0 hata ve
     `npx vite build`.
   - **Artifact tasarımı:** claude.ai Artifact 3P geçit kipinde çalışmadığı için eşdeğeri yereldir —
     `meds/scripts/altyapi/artifact_studio/studyo.py <reçete.json>` tek dosyalık çevrimdışı HTML üretir, `kur.sh` skill'i
     (`.claude/skills/artifact-studyo`) ve önizleme sunucusunu **oturum kökünün** `.claude/launch.json`'una yazar.
     Veri uydurulmaz; kaynak alanı yazılır; büyüklükleri ~10× farklı seriler çift eksende (`"eksen": "sag"`) çizilir.
