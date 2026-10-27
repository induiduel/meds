# v15 ekran denetimi

Tarih: 2026-10-27. Kaynak: v15 tasarım sistemi `components/bundle.js` (`MeDSor.screens.*`) ve ekran README'leri; site: `src/router.ts`, `src/App.tsx`, `src/components/v15/*`, `src/styles/v15/*`, `docs/V15_PLAN.md`.

Yöntem: her ekranın bundle.js çizimindeki metin ve öğeler, sitedeki bileşenin JSX metinleriyle karşılaştırıldı (grep + okuma). Ekran görüntüsüyle görsel karşılaştırma yapılmadı. Bir öğe kodda bulunamadıysa ve emin olunamadıysa **DOĞRULANMADI** yazıldı.

Durumlar: **VAR** = yapı tasarıma uyuyor · **KISMİ** = sayfa var, yapı/öğe farklı ya da eksik ("CSS katmanı" = eski bileşen + v15 stil dosyası, yapı değişmedi) · **YOK** = sitede yok · **BİLİNÇLİ YOK** = kullanıcı reddetti · **DOĞRULANMADI** = karşılık belirlenemedi.

## Özet
Toplam 280 ekran.

| Durum | Sayı |
|---|---|
| VAR | 55 |
| KISMİ | 111 |
| YOK | 50 |
| BİLİNÇLİ YOK | 14 |
| DOĞRULANMADI | 50 |

Not: YOK sayısının 6'sı tasarım belgesi ekranıdır (A09, K08, P01, W03, X09, Z01: bileşen, ikon, yazı örneği, ekran haritası); kod karşılığı gerekmez.

## Öncelik önerisi (öğrencinin en çok kullandığı ekranlar önce)
1. **Sesli ders (S):** S18 bölüm sonu, S08 okuma ayarları (satır/yazı tipi/zemin), S10 seçim araç çubuğu, S21 çıkmış belirdi şeridi, S28 oynatıcı ⋯ v15 sayfası, S26 ders seçeneklerinin eksik satırları, S20 terim kartına Sözlükte aç / Karta ekle, S16 kilit ekranı (mediaSession), S09 Vurgular/Notlar sekmeleri. Sonra S06 sesli kitap + uyku zamanlayıcı, S07 PC üç bölme.
2. **Soru (C):** C01 Karma test + kip seçici, C03 doğru cevap sonrası ders bağlantısı/takip/puan, C04 "48 saat sonra" + önerilen ders bölümü, C09 Yanlışlarım sekmeli ekranı, C07 çıkmışlar yapısı (CSS katmanından gerçek v15 yapıya), C06 çözücü ekranı.
3. **Öğren B05–B07:** kullanıcı onayladı; B06/B07 yalnız CSS katmanı, yapı değişikliği gerekmiyorsa dokunma.
4. **Bugün A02:** alt şeride Hücre + Kronometre, hızlı satıra Oyna, kurul hâkimiyeti halkası.
5. **Kabuk:** A06 bildirim merkezi, A03 menüde Oyunlar bölümü, A05 aramada "sesli derste geçen yerler", A08 ortak boş/hata durum bileşeni.
6. Ardından B04 süzgeçleri, B08 spot kartı (çıkma sayısı, sesli bağlantı), B11 not damgaları, D02–D05 kamp iç sayfaları (CSS katmanından yapıya), J01/J02 grafikler, Y01–Y05 süzgeç.


## A · Kabuk

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| A01 | giris | AuthV12 (v15 dalı), styles/v15/giris.css | KISMİ | Tasarım tek form (e-posta+şifre, Google, "Sınıf koduyla kayıt ol"); sitede Giriş/Kayıt sekmesi, sınıf kodu girişi yok |
| A02 | ana (Bugün) | today → today/TodayView.tsx (v15 dalı), today.css | KISMİ | Plan+akış+hızlı satır var; alt şeritte Hücre ve Kronometre yok (Seri/Bugün/Bu hafta), hızlı satırda "Oyna" yerine "Tekrar", kurul hâkimiyeti halkası yok |
| A03 | menu | ShellV15 › TabBarV15 Menü | KISMİ | Tasarımda dört iş + Oyunlar bölüm satırları (alt açıklamalı); sitede Başvuru · Ben · Araçlar gruplaması, Oyunlar ayrı bölüm değil |
| A04 | kurul | Merkezlerdeki "Kurul seç" (DerslerMerkezV15 vb.) | KISMİ | Tasarım: Kurul 1–6 listesi Bitti/Aktif/Kapalı + "Takvimi aç"; sitede açılır seçici, durum etiketleri DOĞRULANMADI |
| A05 | arama | search → SearchView (⌘K) | DOĞRULANMADI | Tasarımdaki tür çipleri ve "Sesli derste geçen yerler" (zaman damgalı) bölümü bulunamadı |
| A06 | bildirim | — | YOK | Sekmeli bildirim merkezi (Tümü/Ders/Soru/Sistem, düello daveti) sitede yok; ShellV15'te yalnız "Bildirimler" girişi |
| A07 | guncelle | UpdatePrompt + shell.css hap bildirim | VAR |  |
| A08 | durumlar | v15-skel, sayfa içi boş/hata metinleri | KISMİ | Ortak boş/çevrimdışı/hata durum kartı (simge+başlık+eylem) yok; her sayfa kendi düz metnini yazıyor |
| A09 | bilesenler | — (tasarım belgesi) | YOK | Kod karşılığı gerekmez; ortak sınıflar V15_PLAN tablosunda |

## B · Ders çalış

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| B01 | dersler | hub_dersler → v15/DerslerMerkezV15.tsx | VAR | Onaylı; 4 araç kartı + Devam et + Diğer araçlar çekmecesi |
| B02 | brans | canli_ders (kurul/branş) → v15/BransV15.tsx | VAR | Seçici Dersler/Önem/Çıkmışlar; satırdaki "hoca · dk" DOĞRULANMADI |
| B03 | ders | ders_detay → v15/DersDetayV15.tsx | VAR |  |
| B04 | sesliListe | canli_ders (kurul) → v15/SesliListeV15.tsx | KISMİ | Çipler Tümü/Yarım kalan/Bitti; tasarımdaki "Yeni" ve "İndirilen" süzgeçleri ve sıralama düğmesi yok |
| B05 | ogrenListe | learn → v15/OgrenKutuphaneV15.tsx | VAR |  |
| B06 | ogrenSlayt | learn › LessonPlayer + styles/v15/ogren.css | VAR | Onaylı; yapı eski oynatıcı, v15 yalnız CSS katmanı |
| B07 | ogrenEtk | LessonPlayer etkileşimleri + ogren.css | VAR | Onaylı (CSS katmanı) |
| B08 | spotlar | spots → v15/SpotsV15.tsx | KISMİ | "n kez çıktı" sayısı, "Yıldızlı" süzgeci ve kartta sesli ders zaman bağlantısı (04:18) yok |
| B09 | onem | en_onemliler → OnemListesi + onem.css | KISMİ | Yalnız CSS katmanı; tablo yapısı (Madde/Kaynak/Önem) ve "Sesli" düğmesi DOĞRULANMADI |
| B10 | sozluk | glossary → GlossaryV12 + sozluk.css | KISMİ | Liste + bilgi kartı var; kartta "Derste dinle" ve "n soru" bağlantıları DOĞRULANMADI |
| B11 | notlar | notlarim → v15/NotlarimV15.tsx | KISMİ | Tümü/Yıldızlı/Ses damgalı süzgeci, ders·zaman·sayfa damgası yok |
| B12 | bitirdiklerim | bitirdiklerim → BitirdiklerimView + bitir.css | KISMİ | Tasarımdaki 4'lü stat (Ders/Soru/Doğru/Süre) DOĞRULANMADI; tanıtım kaldırıldı, yapı eski |
| B13 | b2ozet | summaries → v15/OzetlerV15.tsx | VAR |  |
| B14 | b2ozetOku | summaries okuyucu (LectureSummariesView) | KISMİ | Okuyucu v15'e geçirilmedi (plan: "okuyucu aynı") |
| B15 | b2hastalik | diseases → DiseasesV12 + sozluk.css | KISMİ | "Anatomiden gez" yapısı yok, yalnız CSS katmanı |
| B16 | b2hastalikDetay | DiseasesV12 ayrıntı | KISMİ | CSS katmanı; tasarım yapısı DOĞRULANMADI |
| B17 | b2kazanim | kazanimlar (PageToolbar) | KISMİ | Yalnız başlık üst bara taşındı |
| B18 | b2ornek | ornek_sorular | DOĞRULANMADI | v15 dalı/stili bulunamadı |
| B19 | b2oncelik | oncelikli_dersler | DOĞRULANMADI | v15 dalı/stili bulunamadı |
| B20 | b2harita | soru_haritasi → v15/SoruHaritasiV15.tsx | VAR |  |
| B21 | b2masa | study (Çalışma masam) | DOĞRULANMADI | Notlar sekmesine notlar.css; masa ekranının kendisi DOĞRULANMADI |
| B22 | b2muzik | music | DOĞRULANMADI | v15 dalı bulunamadı |

## S · Sesli ders

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| S01 | sdA (PDF üstte, metin altta) | canli_ders › CanliDersDers + CdV15 + sesli.css | VAR |  |
| S02 | sdB (yan yana) | CdV15Gorunum › Bölme yönü "Yan yana" | VAR |  |
| S03 | sdC (yalnız metin) | Görünüm "Metin" | VAR |  |
| S04 | sdD (PDF + altyazı şeridi) | — | DOĞRULANMADI | "Altyazı" kipi kodda bulunamadı; büyük olasılıkla YOK |
| S05 | sdE (odak modu) | ShellV15 odakEkrani + Tam ekran | KISMİ | Kabuk gizleniyor; "yalnız metin + üç düğme, dokununca denetimler" kipi yok |
| S06 | sdF (sesli kitap kipi) | — | YOK | Kapak + dalga + uyku zamanlayıcı kipi yok |
| S07 | sdG (üç bölmeli masa) | — | YOK | PC'de bölümler + PDF + metin üç bölme yok; "Vurgularım" yok |
| S08 | sdH (okuma ayarları) | CdV15Gorunum › Yazı boyutu | KISMİ | Yalnız yazı boyutu; satır aralığı, yazı tipi (serif/sans/disleksi), zemin rengi, "etkin cümleyi ortala" yok |
| S09 | sdI (bölümler ve işaretler) | CanliDersDers bölüm/aşama listesi | KISMİ | Bölümler var; Vurgular ve Notlar sekmeleri yok |
| S10 | sdJ (seçim araç çubuğu) | — | YOK | Cümle seçince Spot yap/Not/Kart/Açıkla/Soru üret çubuğu yok |
| S11 | sdK (mini oynatıcı + çevrimdışı) | CanliDersDock + CanliDersCevrimdisi | KISMİ | Mini oynatıcı ve çevrimdışı var; v15 biçimi DOĞRULANMADI |
| S12 | sdL (ders içi ara soru) | CdCikmisChip (çıkmış soru) | KISMİ | Çıkmış chip'iyle soru var; "bölüm sonunda ses durur, tek soru" akışı yok |
| S13 | sdM (yükleniyor) | CanliDersDers "hazırlanıyor" | KISMİ | Ses iniş halkası ve "metni oku" seçeneği DOĞRULANMADI |
| S14 | sdN (PDF eşleşmesi yok) | CanliDersDers "bulunamadı" | KISMİ | PDF soluklaşma + "Eşleşme hatası bildir" DOĞRULANMADI |
| S15 | sdO (yatay telefon) | — | DOĞRULANMADI | Yatay telefon tek satır oynatıcı kipi kodda görülmedi |
| S16 | sdP (kilit ekranı) | — | YOK | Sesli derste navigator.mediaSession yok (yalnız asistan/çözücü/müzikte); kilit ekranı altyazı satırı yok |
| S17 | sdQ (bağlantı koptu) | — | DOĞRULANMADI | Arabellek uyarısı/"Tekrar dene"/indir kartı bulunamadı |
| S18 | sdR (bölüm sonu) | — | YOK | "Bölüm bitti · 3 soruyla pekiştir · Devam (5 sn)" kutusu ve "bölüm sonlarında dur" ayarı yok |
| S19 | sdS (ana ekran v2) | CdV15Bas + PDF şeridi | VAR |  |
| S20 | sdT (terim bilgi kartı) | CdTerimKatman | KISMİ | Terim/kısaltma kartı ve "Karıştırılan" var; "Sözlükte aç" ve "Karta ekle" düğmeleri yok |
| S21 | sdU0 (çıkmış belirdi) | CdCikmisChip | KISMİ | Çip var; oynatıcı şeridi ("Bu slayttaki bilgi n kez soruldu · Çöz") yok (plan: yapılmadı) |
| S22 | sdU (kompakt çıkmış kartı) | CikmisKart (v15) | VAR |  |
| S23 | sdV (çıkmış cevaplandı) | CikmisKart | VAR | "PDF'te göster" ve "2. soru hazır" DOĞRULANMADI |
| S24 | sdW (Görünüm › PDF katmanları) | CdV15Gorunum | VAR |  |
| S25 | sdW2 (Görünüm › Düzen) | CdV15Gorunum (Bölme yönü, Oran, Bölmelerin yeri, Tam ekran) | VAR |  |
| S26 | sdX (ders seçenekleri) | CdV15Menu (gruplar CanliDersDers'ten) | KISMİ | "Bu dersi bitirdim", "Yıldızlı paragraflar", "Listeme ekle", "Metni aktar" kodda bulunamadı; Video/Motivasyon var |
| S27 | sdY (kalem araç kutusu) | CdV15KalemDugme/KalemKutusu | VAR |  |
| S28 | sdOy (oynatıcı seçenekleri) | eski açılır menü (Hız, Kaç kez) | KISMİ | Plan: "⋯ sheet'inin v15 biçimi yapılmadı"; eski menü duruyor |
| S29 | sdZ (çizim panelleri) | canlı çizim katmanı | KISMİ | 8 panelden "değer kartı" türü yalnız tasarımda (plan) |
| S30 | sdZ2 (PDF üstü işaretler) | canlı çizim (kontur, ok, lazer) | VAR | DOĞRULANMADI: tüm işaret türleri tek tek sınanmadı |

## C · Soru çöz

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| C01 | soruMerkez | hub_sorular → v15/SorularMerkezV15.tsx | KISMİ | Test oluştur, Tekrar zamanı, Yıla göre var; "Karma test başlat" kartı ve kip seçici (Öğrenme/Sınav/Sesli çözücü) yok, soru sayısı seçenekleri farklı |
| C02 | soru | practice → v15/PracticeV15.tsx | VAR |  |
| C03 | soruDogru | PracticeV15 | KISMİ | "Derste 04:18" bağlantısı, "Takip sorusu", "+puan · seri" satırı yok |
| C04 | soruYanlis | PracticeV15 (yanlış çekmecesi) | KISMİ | "Birlikte toparlayalım" + her şık açıklaması var; "48 saat sonra yeniden soracağım" ve önerilen sesli ders bölümü yok |
| C05 | yardim | PracticeV15 Yardım al | KISMİ | Şık açıklamaları var; "Neden yanlış yaptın?" ve takip sorusu alanı yok |
| C06 | cozucu | soru_cozucu → SoruCozucuSayfa + cozucu.css | KISMİ | Başlangıç v15; çözücü ekranı yalnız CSS katmanı |
| C07 | cikmis | past_exams → CikmisV12 + cikmis.css | KISMİ | Yıla/Konuya/Hocaya göre seçici ve yıl kartı (soru sayısı + ilerleme) DOĞRULANMADI; yalnız CSS katmanı |
| C08 | sonuc | PracticeV15 Test sonucu | VAR | Halka + stat var; konu dağılımı çubukları DOĞRULANMADI |
| C09 | hatalar (Yanlışlarım) | Hata defteri (Öğren kitaplığı bağlantısı) | DOĞRULANMADI | Tekrar zamanı/Bekleyen/Öğrenildi sekmeli v15 ekranı bulunamadı |
| C10 | soruEkle | quick_add → PoolV12 + havuz.css | KISMİ | Yalnız CSS katmanı; 4 adımlı çekmece eski |

## D · Sınava hazırlan

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| D01 | kamplar | hub_kamplar → v15/KamplarMerkezV15.tsx | VAR | Onaylı |
| D02 | kampAsama | kamp → KampView + kamp.css | KISMİ | Yalnız CSS katmanı; aşama listesi (Şimdi/Tamamlandı/Kilitli) + kamp skoru kartı DOĞRULANMADI |
| D03 | checkup | patoloji_checkup → PatolojiCheckUp + kamp.css | KISMİ | CSS katmanı |
| D04 | sonProva | son_prova → SonProvaView + kamp.css | KISMİ | CSS katmanı; 1·2·3 adım kartları DOĞRULANMADI |
| D05 | plan60 | sinav_plani → SinavPlaniView + kamp.css | KISMİ | Tahmini puan / bu hafta / soru payı çubukları DOĞRULANMADI |
| D06 | takvim | sinav_takvimi → v15/SinavTakvimiV15.tsx | KISMİ | T‑5/3/1 var; "Sınav öncesi pratik soruları gönder" anahtarı ve sınav ekleme (+) yok |
| D07 | olasi | olasi_sorular | KISMİ | Yalnız başlık/simge üst barda |

## E · KMB

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| E01 | kmbListe | kmb_asistan → kmb/KmbAsistan.tsx | KISMİ | v15 stili yok (yalnız başlık üst barda); kategori çipleri DOĞRULANMADI |
| E02 | kmbOgret | KmbAsistan öğret adımı | KISMİ | v15 stili yok |
| E03 | kmbVaka | KmbAsistan vaka sınavı | KISMİ | v15 stili yok |
| E04 | kmbCizim | — | DOĞRULANMADI | Sürükle-bırak canlı çizim bulunamadı |
| E05 | kmbKontrol | — | DOĞRULANMADI | Kontrol listesi değerlendirme ekranı bulunamadı |

## F · Oyunlar

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| F01 | oyunMerkez | oyunlar → v15/OyunlarV15.tsx | KISMİ | Haftalık lig kartı ve "Hızlı düello bul" yok; tür listesi farklı (Canlı, Hayatta kal, Blitz, Terimi bul, Eşleştir) |
| F02 | bosluk | v15/OyunBoslukV15.tsx | VAR |  |
| F03 | eslestir | v15/OyunEslestirV15.tsx | VAR |  |
| F04 | kartlar | flashcards → FlashcardsV12 + kartlar.css | KISMİ | CSS katmanı; Tekrar/Zor/İyi/Kolay dörtlüsü DOĞRULANMADI |
| F05 | sirala | — | YOK |  |
| F06 | blitz | OyunSoloV15 (Blitz) | KISMİ | Doğru/Yanlış önerme + çarpan biçimi yerine çoktan seçmeli 60 sn |
| F07 | izgara | — | YOK |  |
| F08 | duelloLobi | OyunlarV15 Oda kur/Koda katıl | KISMİ | Rastgele rakip, çevrimiçi arkadaşlar, ayar seçicisi yok |
| F09 | duello | OyunlarV15 canlı oyun | VAR |  |
| F10 | duelloSonuc | OyunlarV15 Oyun bitti | KISMİ | Lig puanı, Rövanş, Yanlışları gör yok |
| F11 | sinifYarisma | OyunlarV15 oda (çok oyunculu) | KISMİ | Ayrı "sınıf yarışması" görünümü (katılımcı sayısı, canlı sıralama paneli) DOĞRULANMADI |

## G · Başvuru ve profil

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| G01 | kaynaklar | hub_kaynaklar → v15/KaynaklarMerkezV15.tsx | KISMİ | Onay bekliyor; arama + önerilen var, satırlar merkezModel'den (Ders PDF'leri/Kurul takvimi/Sınav dağılımı/Asistan) DOĞRULANMADI |
| G02 | saglik | health_ministry → SaglikView + saglik.css | KISMİ | CSS katmanı; Rehberler/Aşı/Bildirimi zorunlu/İstatistik seçicisi DOĞRULANMADI |
| G03 | asistan | ai_chat | DOĞRULANMADI | v15 dalı yok |
| G04 | profil | settings → ProfileV12 (v15 dalı) + profil.css | KISMİ | Profil kartı + gruplu satırlar; 4'lü stat ve haftalık etkinlik grafiği DOĞRULANMADI |
| G05 | basarim | basarimlar | KISMİ | Yalnız başlık üst barda |
| G06 | ayarlar | ProfileV12 #hash bölümleri | KISMİ | Paneller v12'den |
| G07 | cevrimdisi | cevrimdisi | DOĞRULANMADI | v15 dalı yok |
| G08 | yonetim | /manage (v14 kabuğu) | KISMİ | Yönetim ayrı v14 konsolu; v15'e geçirilmesi planlanmamış |

## H · Diyalog, çekmece, tost

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| H01 | dlgOnay | shell.css › Katmanlar | VAR | CSS katmanı (ortalı uyarı, tam genişlik düğmeler) |
| H02 | dlgSil | shell.css › Katmanlar | VAR |  |
| H03 | dlgBilgi | shell.css › Katmanlar | VAR |  |
| H04 | dlgForm | shell.css › Katmanlar | VAR | DOĞRULANMADI: form alanları |
| H05 | tur1 | CanliDersTur / tanıtım | DOĞRULANMADI |  |
| H06 | tur2 | CanliDersTur / tanıtım | DOĞRULANMADI |  |
| H07 | acilir | shell.css | VAR |  |
| H08 | cekmece | shell.css (bulanık perde, 22–24 px köşe) | VAR |  |
| H09 | altCekmece | shell.css | VAR |  |
| H10 | toastlar | shell.css hap bildirim | VAR |  |
| H11 | yukleme | .v15-skel | VAR |  |

## I · Açılış ve kayıt

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| I01 | splash | — | DOĞRULANMADI |  |
| I02 | intro1 | OnboardingV12 (v15 ilerleme çubuğu) | KISMİ | "Hoş geldin / İleri / Bitir" adımları; tasarımdaki üç tanıtım ekranının içeriği DOĞRULANMADI |
| I03 | intro2 | OnboardingV12 | KISMİ | aynı |
| I04 | intro3 | OnboardingV12 | KISMİ | aynı |
| I05 | girisSecenek | AuthV12 Giriş/Kayıt sekmesi | KISMİ | Seçenek ekranı ayrı değil, sekme |
| I06 | otp | — | YOK | E-posta/şifre; tek kullanımlık kod ekranı yok |
| I07 | kayitUni | OnboardingV12? | DOĞRULANMADI |  |
| I08 | kayitSinif | OnboardingV12? | DOĞRULANMADI |  |
| I09 | kayitKurul | OnboardingV12? | DOĞRULANMADI |  |
| I10 | kayitHedef | OnboardingV12? | DOĞRULANMADI |  |
| I11 | kayitBitti | OnboardingV12 Bitir | KISMİ |  |

## J · Grafik ve şemalar

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| J01 | grafikler | stats → StatsView + v15/CalismaGrafikleriV15.tsx | KISMİ | Özet + günlük çubuk + modül dağılımı var; doğru oranı çizgi grafiği (sınıf ort.), çalışma ısı takvimi yok |
| J02 | grafikDetay | — | YOK | Konu performansı + unutma eğrisi yok |
| J03 | zihin | zihin_haritasi (bağlantısız) | BİLİNÇLİ YOK | Kullanıcı reddetti (2026-10-27) |
| J04 | yolHaritasi | — | BİLİNÇLİ YOK | J03–J06 grubu reddedildi (plan) |
| J05 | akis | — | BİLİNÇLİ YOK |  |
| J06 | zamanCizelgesi | v15/SinavTakvimiV15.tsx (yılın sınavları) | KISMİ | Plan reddedilen gruba koyuyor ama takvimde zaman çizelgesi olarak kullanıldı; renkli durum noktaları DOĞRULANMADI |

## K · Not ve kalem

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| K01 | renklendir | NotlarimV15 fosforlu | KISMİ | Metni renklendir (seçili kelimeye renk) yok; yalnız fosforlu çizim |
| K02 | kalemPdf | CdV15KalemKutusu (sesli ders) | VAR |  |
| K03 | kalemNot | NotlarimV15 kalem | KISMİ | El yazısı var; "otomatik metne çevir" yok |
| K04 | notEditor | NotlarimV15 | KISMİ | Ses damgası, PDF kesiti ekleme, liste biçimi yok |
| K05 | notPaylas | — | YOK | Kişi/grup paylaşımı yok (paylaş = metni gönder) |
| K06 | paylasilan | — | YOK |  |
| K07 | yaziAyar | Ayarlar › Görünüm | DOĞRULANMADI |  |
| K08 | yaziOrnek | — (tasarım belgesi) | YOK | Kod karşılığı gerekmez |

## L · Topluluk ve listeler

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| L01 | sohbetListe | topluluk → v15/ToplulukV15.tsx | KISMİ | Kanallar (Genel, Kurul 1–6) var; kişi/grup sohbetleri ve arama yok |
| L02 | sohbet | ToplulukV15 kanal | VAR |  |
| L03 | yorumlar | ToplulukV15 ders yorumları | KISMİ | Soru yorumları, beğeni, "En faydalı/En yeni" sıralaması yok |
| L04 | soruListe | quick_add/PoolView | DOĞRULANMADI | Süzgeç çipli soru listesi v15'te bulunamadı |
| L05 | kurulListe | "Kurul seç" | KISMİ | Tema adları + durum etiketli kurul listesi yok |
| L06 | seneSec | SesliListeV15 "2025-26 arşivi" | KISMİ | Yıl/dönem seçici yok; yalnız arşiv düğmesi |

## M · Hücrem

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| M01 | hucrem | hucrem → v15/HucremV15.tsx + Hucre3D | VAR |  |
| M02 | evrim | HucremV15 (28 basamak) | VAR |  |
| M03 | evrimDetay | HucremV15 | DOĞRULANMADI |  |
| M04 | glukoz | HucremV15 glukoz | VAR |  |
| M05 | hucreStres | HucremV15 "Hücren aç kalıyor" | KISMİ | Stres durumu metni var; ayrı ekran DOĞRULANMADI |
| M06 | seviyeAtla | — | DOĞRULANMADI |  |
| M07 | siralama | leaderboard + Hucrem "Hücre sırası" | KISMİ | v15 dalı yok (leaderboard) |
| M08 | profil2 | ProfileV12 v15 | KISMİ | Hücre/hesap kartı DOĞRULANMADI |
| M09 | profilDuzenle | — | DOĞRULANMADI |  |
| M10 | basarim2 | basarimlar | KISMİ | Yalnız başlık |
| M11 | rozetDetay | — | DOĞRULANMADI |  |
| M12 | evrimYol | HucremV15 basamak yolu | DOĞRULANMADI |  |
| M13 | cag1 | — | DOĞRULANMADI |  |
| M14 | cag2 | — | DOĞRULANMADI |  |
| M15 | cag3 | — | DOĞRULANMADI |  |
| M16 | cag4 | — | DOĞRULANMADI |  |
| M17 | hucreKarsilastir | — | YOK |  |

## N · Quiz kipleri

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| N01 | quizModSec | OyunlarV15 tür seçimi | KISMİ | Tür listesi farklı |
| N02 | quizGorsel | — | YOK |  |
| N03 | quizCumle | OyunBoslukV15 | KISMİ |  |
| N04 | quizCan | OyunSoloV15 "Hayatta kal" | VAR |  |
| N05 | quizZaman | OyunSoloV15 Blitz | VAR |  |
| N06 | quizTakim | — | YOK |  |
| N07 | quizKaydir | — | YOK |  |
| N08 | quizSonuc2 | OyunSoloV15 sonuç | KISMİ |  |

## O · Video, PDF, tam ekran

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| O01 | video | — | YOK | Video oynatıcı ekranı yok (yalnız dışa aktarım) |
| O02 | videoTam | — | YOK |  |
| O03 | videoPip | — | YOK |  |
| O04 | pdfOkuyucu | Öğren ders PDF'i (PDF.js) | DOĞRULANMADI |  |
| O05 | pdfIzgara | — | DOĞRULANMADI |  |
| O06 | pdfArama | — | DOĞRULANMADI |  |
| O07 | pdfIkili | — | DOĞRULANMADI |  |
| O08 | tamEkranOgren | ShellV15 Tam ekran | KISMİ |  |
| O09 | tamEkranSoru | ShellV15 Tam ekran | KISMİ |  |
| O10 | tamEkranAyar | — | DOĞRULANMADI |  |

## P · İkonlar

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| P01 | ikonlar | — (tasarım belgesi) | YOK | Kod karşılığı gerekmez |

## T · Kronometre

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| T01 | kronoSoru | — | YOK | Soru ekranı içi kronometre yok |
| T02 | kronoAcik | v15/KronometreV15.tsx | VAR |  |
| T03 | kronoSesli | — | YOK | Sesli derste gizli (bilinçli tasarım dışı seçim) |
| T04 | kronoVideo | — | YOK |  |
| T05 | kronoBirlesme | — | YOK | Ses oynatıcıyla birleşme yapılmadı (plan) |
| T06 | kronoDurum | KronometreV15 | KISMİ |  |
| T07 | kronoAyar | — | YOK |  |
| T08 | kronoGecmis | KronometreV15 (localStorage 50 oturum) | KISMİ | Profil › Kronometre geçmişi ekranı yok |
| T09 | kronoPc | KronometreV15 | KISMİ | DOĞRULANMADI: PC biçimi |
| T10 | kronoFormlar | — | YOK | Tek biçim |
| T11 | kronoF1 | — | YOK |  |
| T12 | kronoF2 | — | YOK |  |
| T13 | kronoF3 | — | YOK |  |
| T14 | kronoF4 | — | YOK |  |
| T15 | kronoF5 | — | YOK |  |

## U · Çalışma kapsülü

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| U01 | kapDers | v15/KapsulV15.tsx | KISMİ | Tek genel panel; sayfaya göre (ders) bağlam yok |
| U02 | kapOgren | KapsulV15 | KISMİ | aynı |
| U03 | kapSpot | KapsulV15 | KISMİ | aynı |
| U04 | kapSozluk | KapsulV15 | KISMİ | aynı |
| U05 | kapNotlar | KapsulV15 | KISMİ | aynı |
| U06 | kapOnem | KapsulV15 | KISMİ | aynı |
| U07 | kapPdf | KapsulV15 | KISMİ | aynı |
| U08 | kapZihin | — | BİLİNÇLİ YOK | Zihin haritası reddedildi |
| U09 | kapSoru | KapsulV15 | KISMİ | aynı |
| U10 | kapAcik | KapsulV15 | VAR |  |
| U11 | kapYanMenu | SideNavV15 Odak girişi | KISMİ |  |
| U12 | kapYanMenuSesli | — | YOK | Sesli derste yan menü kapsülü yok |

## V · Tema, motif, şema

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| V01 | temaGaleri | Ayarlar › Tasarım/Görünüm (palettes.ts) | KISMİ | Galeri görünümü DOĞRULANMADI |
| V02 | temaSec | Ayarlar › Görünüm | KISMİ |  |
| V03 | motifler | — | YOK | Tıbbi motifler yok |
| V04 | yaziTipleri | — | DOĞRULANMADI |  |
| V05 | vucut | — | BİLİNÇLİ YOK |  |
| V06 | kalpSema | — | BİLİNÇLİ YOK |  |
| V07 | labSema | — | BİLİNÇLİ YOK |  |
| V08 | ekgSema | — | BİLİNÇLİ YOK |  |

## W · Palet, kart, zihin biçimleri

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| W01 | paletDuzenle | Ayarlar | DOĞRULANMADI |  |
| W02 | paletGaleri | Ayarlar palet | KISMİ |  |
| W03 | kartlar (kart çeşitleri) | — (tasarım belgesi) | YOK | Kod karşılığı gerekmez |
| W04 | tostlar2 | shell.css hap bildirim | VAR |  |
| W05 | zihinListe | — | BİLİNÇLİ YOK |  |
| W06 | zihinAgac | — | BİLİNÇLİ YOK |  |
| W07 | zihinBalik | — | BİLİNÇLİ YOK |  |
| W08 | zihinKabarcik | — | BİLİNÇLİ YOK |  |
| W09 | zihinKavram | — | BİLİNÇLİ YOK |  |
| W10 | zihinDongu | — | BİLİNÇLİ YOK |  |

## X · İstatistik

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| X01 | istatGun | StatsView (7/30 gün) | KISMİ | Gün ayrıntısı dokununca; ayrı gün ekranı yok |
| X02 | istatHafta | StatsView 7 gün | KISMİ |  |
| X03 | istatAy | StatsView 30 gün | KISMİ |  |
| X04 | istatSoru | StatsView | DOĞRULANMADI |  |
| X05 | istatSoruTek | — | DOĞRULANMADI |  |
| X06 | istatSoruDetay | — | DOĞRULANMADI |  |
| X07 | istatPuan | — | DOĞRULANMADI |  |
| X08 | istatKonu | — | YOK |  |
| X09 | grafikTurleri | — (tasarım belgesi) | YOK | Kod karşılığı gerekmez |
| X10 | grafikAyar | — | YOK |  |

## Y · Süzgeç ve PDF oluştur

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| Y01 | filtreTam | SorularMerkezV15 Test oluştur | KISMİ | Yalnız ders + soru sayısı; tam süzgeç sayfası yok |
| Y02 | filtreHizli | SorularMerkezV15 çipleri | KISMİ |  |
| Y03 | filtreAktif | — | YOK |  |
| Y04 | filtrePanel | — | YOK | PC yan süzgeç paneli yok |
| Y05 | filtreKayitli | — | YOK |  |
| Y06 | filtreBos | "Bu süzgeçte … yok" metinleri | VAR |  |
| Y07 | pdf1 | pdf_olustur → v15/PdfSihirbaziV15.tsx | VAR |  |
| Y08 | pdf2 | PdfSihirbaziV15 | VAR |  |
| Y09 | pdf3 | PdfSihirbaziV15 | VAR |  |
| Y10 | pdf4 | PdfSihirbaziV15 → TopluPdf | KISMİ | Dördüncü adım ortak TopluPdf penceresi |
| Y11 | pdfHazirlik | TopluPdf | KISMİ |  |
| Y12 | pdfHazir | TopluPdf | KISMİ |  |
| Y13 | pdfGecmis | PdfSihirbaziV15 Geçmiş | VAR |  |

## Z · Ekran haritası ve araç listeleri

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| Z01 | ekranHaritasi | — (tasarım belgesi) | YOK | Kod karşılığı gerekmez |
| Z02 | arac_dersler | DerslerMerkezV15 Diğer araçlar çekmecesi | VAR |  |
| Z03 | arac_soruMerkez | SorularMerkezV15 "Araçlar" | KISMİ | "Tüm araçlar" tek satır girişi DOĞRULANMADI |
| Z04 | arac_kamplar | KamplarMerkezV15 | DOĞRULANMADI |  |
| Z05 | arac_kaynaklar | KaynaklarMerkezV15 | DOĞRULANMADI |  |
| Z06 | arac_oyunMerkez | OyunlarV15 | KISMİ |  |
| Z07 | arac_profil2 | v15/TumSayfalarV15.tsx | KISMİ |  |

## AA · Ders programı

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| AA01 | dpListe | ders_programi → v15/DersProgramiV15.tsx | VAR |  |
| AA02 | dpHafta | DersProgramiV15 | VAR |  |
| AA03 | dpGun | DersProgramiV15 | VAR |  |
| AA04 | dpAy | DersProgramiV15 (Ay ızgarası) | VAR | Plan "ay yok" diyor; kodda ay görünümü var (plan güncel değil) |
| AA05 | dpDetay | DersProgramiV15 → ders ayrıntısı | KISMİ | Ayrı ders programı ayrıntı kartı yok |
| AA06 | dpEkle | — | YOK | Ekle/içe aktar yok |
| AA07 | dpWidget | — | YOK |  |

## AB · Hesap, arka plan, uygulama temelleri

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| AB01 | arkaPlan | — | YOK | Arka plan işleri ekranı yok |
| AB02 | arkaPlanUst | — | YOK |  |
| AB03 | kisisel | ProfileV12 | KISMİ |  |
| AB04 | hesapGuvenlik | ProfileV12 hesap | KISMİ |  |
| AB05 | veriGizlilik | ProfileV12 verilerim | KISMİ |  |
| AB06 | bildirimTercih | — | DOĞRULANMADI |  |
| AB07 | erisilebilirlik | ProfileV12 Erişilebilirlik | VAR |  |
| AB08 | dilBolge | — | YOK |  |
| AB09 | komutPaleti | ⌘K arama | KISMİ | Arama var; komut (eylem) listesi yok |
| AB10 | kisayollar | — | DOĞRULANMADI |  |
| AB11 | baslangicGorev | — | YOK |  |
| AB12 | geriAl | NotlarimV15 "Geri al" | KISMİ | Genel geri al tostu yok |
| AB13 | cevrimdisiBanner | — | DOĞRULANMADI |  |
| AB14 | yardimMerkezi | — | YOK |  |
| AB15 | yenilikler | guncellemeler | KISMİ | Yalnız başlık üst barda |
| AB16 | hata404 | — | DOĞRULANMADI |  |
| AB17 | hataSunucu | — | DOĞRULANMADI |  |
| AB18 | bakim | — | DOĞRULANMADI |  |

- S08: KURULDU (2026-10-27): satır aralığı, yazı tipi (Okuma/Sade/Kolay okunur), zemin, okunan cümleyi ortala
- S09: KURULDU: oynatıcı çekmecesinde Bölümler / Yıldızlılarım sekmeleri
- S10: KURULDU: seçim çubuğu Nota ekle · Yıldızla · Kopyala (Açıkla/Soru üret LLM gerektirir, yok)
- S16: KURULDU: medyaSession zaten vardı; kilit ekranında okunan cümle + ±15 sn eklendi
- S18: KURULDU: Bölüm sonunda dur + Tekrar dinle / Pekiştir / Devam et kutusu
- S20: KURULDU: Sözlükte aç · Karta ekle
- S21: KURULDU: oynatıcıda "n kez çıkmışta soruldu · Çöz" şeridi (yalnız doğrulanmış eşleme)
- S26: VAR (denetim kaçırmıştı): dört gruplu ders seçenekleri
- S28: KURULDU: oynatıcı seçenekleri alt çekmecesi