# v15 ekran denetimi

Tarih: 2026-10-27. Kaynak: v15 tasarım sistemi `components/bundle.js` (`MeDSor.screens.*`) ve ekran README'leri; site: `src/router.ts`, `src/App.tsx`, `src/components/v15/*`, `src/styles/v15/*`, `docs/V15_PLAN.md`.

Yöntem: her ekranın bundle.js çizimindeki metin ve öğeler, sitedeki bileşenin JSX metinleriyle karşılaştırıldı (grep + okuma). Ekran görüntüsüyle görsel karşılaştırma yapılmadı. Bir öğe kodda bulunamadıysa ve emin olunamadıysa **DOĞRULANMADI** yazıldı.

Durumlar: **VAR** = yapı tasarıma uyuyor · **KISMİ** = sayfa var, yapı/öğe farklı ya da eksik ("CSS katmanı" = eski bileşen + v15 stil dosyası, yapı değişmedi) · **YOK** = sitede yok · **BİLİNÇLİ YOK** = kullanıcı reddetti · **DOĞRULANMADI** = karşılık belirlenemedi.

## Özet
Toplam 280 ekran.

| Durum | Sayı |
|---|---|
| VAR | 131 |
| KURULDU | 64 |
| KISMİ | 12 |
| YOK | 51 |
| BİLİNÇLİ YOK | 16 |
| DOĞRULANMADI | 6 |

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
| A01 | giris | AuthV12 (v15 dalı), styles/v15/giris.css | KURULDU | Hesabına gir tek ekran (I05) |
| A02 | ana (Bugün) | today → today/TodayView.tsx (v15 dalı), today.css | KURULDU | Seri·Hücre·Kronometre şeridi, Oyna |
| A03 | menu | ShellV15 › TabBarV15 Menü | KURULDU | Oyunlar bölümü + bölüm açıklamaları |
| A04 | kurul | Merkezlerdeki "Kurul seç" (DerslerMerkezV15 vb.) | KURULDU | KurulSecV15: Bitti/Aktif/tarih + Takvimi aç (4 merkez) |
| A05 | arama | search → SearchView (⌘K) | KISMİ | SearchPalette (⌘K) komut paleti + SearchView; "Sesli derste geçen yerler" (zaman damgalı) bölümü bulunamadı |
| A06 | bildirim | — | VAR | v15/BildirimlerV15.tsx (/bildirimler): Tümü/Ders/Soru/Sistem sekmeleri; düello daveti türü yok |
| A07 | guncelle | UpdatePrompt + shell.css hap bildirim | VAR |  |
| A08 | durumlar | v15-skel, sayfa içi boş/hata metinleri | KURULDU | .b15-bos ortak durum kartı (simge + metin, hata + Yeniden dene) |
| A09 | bilesenler | — (tasarım belgesi) | YOK | Kod karşılığı gerekmez; ortak sınıflar V15_PLAN tablosunda |

## B · Ders çalış

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| B01 | dersler | hub_dersler → v15/DerslerMerkezV15.tsx | VAR | Onaylı; 4 araç kartı + Devam et + Diğer araçlar çekmecesi |
| B02 | brans | canli_ders (kurul/branş) → v15/BransV15.tsx | VAR | Seçici Dersler/Önem/Çıkmışlar; satırdaki "hoca · dk" DOĞRULANMADI |
| B03 | ders | ders_detay → v15/DersDetayV15.tsx | VAR |  |
| B04 | sesliListe | canli_ders (kurul) → v15/SesliListeV15.tsx | KURULDU | Yeni/İndirilen + sıralama |
| B05 | ogrenListe | learn → v15/OgrenKutuphaneV15.tsx | VAR |  |
| B06 | ogrenSlayt | learn › LessonPlayer + styles/v15/ogren.css | VAR | Onaylı; yapı eski oynatıcı, v15 yalnız CSS katmanı |
| B07 | ogrenEtk | LessonPlayer etkileşimleri + ogren.css | VAR | Onaylı (CSS katmanı) |
| B08 | spotlar | spots → v15/SpotsV15.tsx | KURULDU | Yıldızlı + Derste dinle (çıkmış sayısı verisi yok) |
| B09 | onem | en_onemliler → OnemListesi + onem.css | VAR | Arama, Sesli asistan, her maddede puan + PDF alıntı (tasarımdakinden zengin; tablo yerine kart satır) |
| B10 | sozluk | glossary → GlossaryV12 + sozluk.css | KURULDU | bilgi kartında Derste dinle (ders adı eşleşmesi + ?ara=) + n soru çipi |
| B11 | notlar | notlarim → v15/NotlarimV15.tsx | KURULDU | Yıldızlı/Ses damgalı + damga |
| B12 | bitirdiklerim | bitirdiklerim → BitirdiklerimView + bitir.css | VAR | üst istatistik şeridi (Ders/Soru/Doğru oranı/Süre) + "baraj %60" alt başlığı |
| B13 | b2ozet | summaries → v15/OzetlerV15.tsx | VAR |  |
| B14 | b2ozetOku | summaries okuyucu (LectureSummariesView) | VAR | SummaryReader: içindekiler, ilerleme çizgisi, Aa, ara |
| B15 | b2hastalik | diseases → DiseasesV12 + sozluk.css | VAR | Liste/Anatomi seçici, DiseaseAnatomy: sistem noktaları (category + ad kökünden), bulgu süzgeci; 199/474 "Diğer" |
| B16 | b2hastalikDetay | DiseasesV12 ayrıntı | VAR | tanım listesi (Klinik/Tanı/Tedavi…), çıkmış sayısı, dersler; sekme yerine bölüm |
| B17 | b2kazanim | kazanimlar (PageToolbar) | KURULDU | kapsam halkası + Tam kapsam/Çıkmışta/Kapsamsız |
| B18 | b2ornek | ornek_sorular | VAR | KazanimSorulariView: Toplam/Çözdüğün/Bugün özet kartları (ks15) |
| B19 | b2oncelik | oncelikli_dersler | VAR | OncelikliDerslerView: B19 panosu (kalan ders, süre, beklenen soru, branş puan/emek çubukları) |
| B20 | b2harita | soru_haritasi → v15/SoruHaritasiV15.tsx | VAR |  |
| B21 | b2masa | study (Çalışma masam) | VAR | v15/MasaGunV15.tsx: hafta şeridi, günün akışı, bugünkü süre + seri |
| B22 | b2muzik | music | VAR | v15/MuzikV15.tsx: çalar kartı, süre çipleri (25/45 dk/ders bitene kadar), liste |

## S · Sesli ders

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| S01 | sdA (PDF üstte, metin altta) | canli_ders › CanliDersDers + CdV15 + sesli.css | VAR |  |
| S02 | sdB (yan yana) | CdV15Gorunum › Bölme yönü "Yan yana" | VAR |  |
| S03 | sdC (yalnız metin) | Görünüm "Metin" | VAR |  |
| S04 | sdD (PDF + altyazı şeridi) | — | VAR | CanliDersDers: "Slayt + altyazı" görünümü (altyazi) |
| S05 | sdE (odak modu) | ShellV15 odakEkrani + Tam ekran | KURULDU | Odak modu (menü › Diğer): yalnız metin, 3 düğme, dokununca denetimler, Esc/Çık |
| S06 | sdF (sesli kitap kipi) | — | VAR | CdSesliEk sesli kitap kipi |
| S07 | sdG (üç bölmeli masa) | — | VAR | CdSesliEk üç bölmeli masa (≥1200px) + Vurgularım |
| S08 | sdH (okuma ayarları) | CdV15Gorunum › Yazı boyutu | KURULDU | okuma ayarları (satır, yazı tipi, zemin, ortala) |
| S09 | sdI (bölümler ve işaretler) | CanliDersDers bölüm/aşama listesi | KURULDU | Bölümler + Yıldızlılarım |
| S10 | sdJ (seçim araç çubuğu) | — | VAR | seçim çubuğu: Spot yap/Not/Kart/Açıkla (Soru üret kaynaksız olduğu için yok) |
| S11 | sdK (mini oynatıcı + çevrimdışı) | CanliDersDock + CanliDersCevrimdisi | KURULDU | mini oynatıcı simge karosu + çevrimdışı/bağlantı kartı (S17) |
| S12 | sdL (ders içi ara soru) | CdCikmisChip (çıkmış soru) | VAR | "Bölüm sonunda dur" + Pekiştir (S18) ses durur, soru çözülür |
| S13 | sdM (yükleniyor) | CanliDersDers "hazırlanıyor" | KURULDU | Ders hazırlanıyor iskeleti; ses iniş yüzdesi yok |
| S14 | sdN (PDF eşleşmesi yok) | CanliDersDers "bulunamadı" | KURULDU | PDF eşleşmesi yok notu: son eşleşen sayfa, orada kal, elle gez (bildir yok) |
| S15 | sdO (yatay telefon) | — | VAR | CanliDersDers GENIS_SORGU + sesli.css yatay telefon kuralı (tek satır oynatıcı) |
| S16 | sdP (kilit ekranı) | — | VAR | canliDersStore mediaSession |
| S17 | sdQ (bağlantı koptu) | — | VAR | CanliDersDock: Bağlantı koptu kartı, "Ses mm:ss'de durdu", Tekrar dene; indirilmiş derste çıkmaz |
| S18 | sdR (bölüm sonu) | — | VAR | bölüm sonu kutusu + Bölüm sonlarında dur |
| S19 | sdS (ana ekran v2) | CdV15Bas + PDF şeridi | VAR |  |
| S20 | sdT (terim bilgi kartı) | CdTerimKatman | KURULDU | Sözlükte aç + Karta ekle |
| S21 | sdU0 (çıkmış belirdi) | CdCikmisChip | KURULDU | oynatıcı çıkmış şeridi |
| S22 | sdU (kompakt çıkmış kartı) | CikmisKart (v15) | VAR |  |
| S23 | sdV (çıkmış cevaplandı) | CikmisKart | VAR | "PDF'te göster" ve "2. soru hazır" DOĞRULANMADI |
| S24 | sdW (Görünüm › PDF katmanları) | CdV15Gorunum | VAR |  |
| S25 | sdW2 (Görünüm › Düzen) | CdV15Gorunum (Bölme yönü, Oran, Bölmelerin yeri, Tam ekran) | VAR |  |
| S26 | sdX (ders seçenekleri) | CdV15Menu (gruplar CanliDersDers'ten) | KURULDU | menü gruplu kutucuklar |
| S27 | sdY (kalem araç kutusu) | CdV15KalemDugme/KalemKutusu | VAR |  |
| S28 | sdOy (oynatıcı seçenekleri) | eski açılır menü (Hız, Kaç kez) | KURULDU | oynatıcı ⋯ sheet v15 |
| S29 | sdZ (çizim panelleri) | canlı çizim katmanı | VAR | değer kartı (`deger_karti`) CizimLayer + şablon + kapı K13; 8 türün tamamı destekli |
| S30 | sdZ2 (PDF üstü işaretler) | canlı çizim (kontur, ok, lazer) | VAR | DOĞRULANMADI: tüm işaret türleri tek tek sınanmadı |

## C · Soru çöz

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| C01 | soruMerkez | hub_sorular → v15/SorularMerkezV15.tsx | KURULDU | Karma test + kip seçici |
| C02 | soru | practice → v15/PracticeV15.tsx | VAR |  |
| C03 | soruDogru | PracticeV15 | KURULDU | "Derste mm:ss" çipi: GET /api/canli-ders/cikmis-dizin (cikmis_konum + cumle_zaman, metinHash kontrollü; 655 soru, 467'si zamanlı); takip sorusu LLM (kural 20) |
| C04 | soruYanlis | PracticeV15 (yanlış çekmecesi) | KURULDU | 48 saat + Yanlışlarım |
| C05 | yardim | PracticeV15 Yardım al | KURULDU | yanlış çekmecesinde "Neden yanlış yaptın?" seçimi → Yanlışlarım kaydı; takip sorusu LLM (kural 20) |
| C06 | cozucu | soru_cozucu → SoruCozucuSayfa + cozucu.css | VAR | SoruCozucu: soru + şıklar + sesli açıklama vurgusu + oynatıcı |
| C07 | cikmis | past_exams → CikmisV12 + cikmis.css | KURULDU | Yıla/Konuya göre kartlar |
| C08 | sonuc | PracticeV15 Test sonucu | VAR | Halka + stat var; konu dağılımı çubukları DOĞRULANMADI |
| C09 | hatalar (Yanlışlarım) | Hata defteri (Öğren kitaplığı bağlantısı) | VAR | v15/YanlislarimV15.tsx: Tekrar zamanı/Bekleyen/Öğrenildi sekmeleri |
| C10 | soruEkle | quick_add → PoolV12 + havuz.css | VAR | soru ekle: kök/şıklar + yazım yardımcısı (composer) |

## D · Sınava hazırlan

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| D01 | kamplar | hub_kamplar → v15/KamplarMerkezV15.tsx | VAR | Onaylı |
| D02 | kampAsama | kamp → KampView + kamp.css | VAR | sesli ders kamp kipinde aşama çubuğu (KampAsamaCubugu); kamp skoru kartı yok |
| D03 | checkup | patoloji_checkup → PatolojiCheckUp + kamp.css | VAR | Check Up tabloları boşluk doldurma + seçenek çipleri |
| D04 | sonProva | son_prova → SonProvaView + kamp.css | VAR | Son Prova: sesli özet partları, aşama soruları, deneme kartları |
| D05 | plan60 | sinav_plani → SinavPlaniView + kamp.css | VAR | tahmini puan + baraj rozeti + sınav dağılımı kartı (sinav_dagilimi) |
| D06 | takvim | sinav_takvimi → v15/SinavTakvimiV15.tsx | KURULDU | pratik hatırlatma anahtarı (Bildirimler T‑5/3/1) + Sınavlarım (+ ile kişisel sınav, çizelgede "Senin") |
| D07 | olasi | olasi_sorular | VAR | olası soru kartı: güven rozeti, çöz, benzer çıkmış, geri bildirim |

## E · KMB

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| E01 | kmbListe | kmb_asistan → kmb/KmbAsistan.tsx | VAR | kmb.css 2026-10-27 token tabanlı yeniden yazıldı (başka oturum); kart ızgarası + durum |
| E02 | kmbOgret | KmbAsistan öğret adımı | VAR | aynı stil katmanı; öğret adımı sahne + ses |
| E03 | kmbVaka | KmbAsistan vaka sınavı | VAR | aynı; vaka sınavı + yeni Etiketleri yerleştir/Değerlendirme |
| E04 | kmbCizim | — | KISMİ | KmbAsistan Yerlestir: etiket seçip sahnede yerine dokunma; sürükle-bırak yok |
| E05 | kmbKontrol | — | VAR | KmbAsistan: kontrol listesi Yaptım/Atladım, n/N ve %80 Geçti/Tekrar çalış |

## F · Oyunlar

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| F01 | oyunMerkez | oyunlar → v15/OyunlarV15.tsx | KURULDU | önce 6 mod kartı, sonra ayarlar; haftalık lig verisi yok |
| F02 | bosluk | v15/OyunBoslukV15.tsx | VAR |  |
| F03 | eslestir | v15/OyunEslestirV15.tsx | VAR |  |
| F04 | kartlar | flashcards → FlashcardsV12 + kartlar.css | KURULDU | Tekrar/Zor/İyi/Kolay dörtlüsü (Kolay: kutu +2, kısayol 4) |
| F05 | sirala | — | VAR | OyunDersV15 Sırala |
| F06 | blitz | OyunSoloV15 (Blitz) | KURULDU | Blitz: önerme Doğru/Yanlış + seri çarpanı (×1, ×2…), puan rekoru |
| F07 | izgara | — | VAR | OyunDersV15 Izgara (terim–tanım) |
| F08 | duelloLobi | OyunlarV15 Oda kur/Koda katıl | VAR | Oda kur + Koda katıl; rastgele rakip/çevrimiçi arkadaşlar eşleştirme sunucusu gerektirir |
| F09 | duello | OyunlarV15 canlı oyun | VAR |  |
| F10 | duelloSonuc | OyunlarV15 Oyun bitti | KURULDU | puan özeti, Yanlışları gör, Rövanş (kurucu, aynı ayar), Yeni oyun |
| F11 | sinifYarisma | OyunlarV15 oda (çok oyunculu) | VAR | çok oyunculu oda: katılımcılar + canlı skor tablosu |

## G · Başvuru ve profil

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| G01 | kaynaklar | hub_kaynaklar → v15/KaynaklarMerkezV15.tsx | VAR | KaynaklarMerkezV15 arama + önerilen + satırlar |
| G02 | saglik | health_ministry → SaglikView + saglik.css | VAR | bölüm seçici (aşı, tarama, yenidoğan, Karabük…) + ders bağları |
| G03 | asistan | ai_chat → LocalAiChatView | KISMİ | Sohbet sayfası var (v15 dışı); eksik: v15 kabuğu, "Kaynaklı yanıt · ders notlarından" alt başlığı, yanıt altında kaynak chip'i (ders · dakika · PDF sayfası); sayfa hâlâ "Yerel GPU (RTX 4060)/gemma3" sağlayıcısı gösteriyor (kural 10/20) |
| G04 | profil | settings → ProfileV12 (v15 dalı) + profil.css | KURULDU | Seri/Soru/Biten konu/Rozet + haftalık etkinlik çubukları (ProfilOzetV15) |
| G05 | basarim | basarimlar | VAR | BasarimView: hedefler, rozet seviyeleri, ATP, rozet ayrıntısı (M11) |
| G06 | ayarlar | ProfileV12 #hash bölümleri | VAR | Profil bölümleri ayrı ekran; paneller v15 renkleriyle (v12 yapısı) |
| G07 | cevrimdisi | cevrimdisi → cevrimdisi/CevrimdisiView.tsx | VAR | Alan bilgisi, paket listesi + indirme kuyruğu, Yalnız Wi-Fi'de indir; tarayıcıda doğrulandı |
| G08 | yonetim | /manage (v14 kabuğu) | BİLİNÇLİ YOK | yönetim ayrı v14 konsolu; v15 geçişi planlanmadı |

## H · Diyalog, çekmece, tost

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| H01 | dlgOnay | shell.css › Katmanlar | VAR | CSS katmanı (ortalı uyarı, tam genişlik düğmeler) |
| H02 | dlgSil | shell.css › Katmanlar | VAR |  |
| H03 | dlgBilgi | shell.css › Katmanlar | VAR |  |
| H04 | dlgForm | shell.css › Katmanlar | VAR | DOĞRULANMADI: form alanları |
| H05 | tur1 | canliDers/CanliDersTur.tsx, onboarding/LearnTour.tsx | KISMİ | Koç kartı mekaniği var (n/toplam, kapat, önceki/sonraki) ama yalnız sesli derste/Öğren'de; eksik: Bugün ekranında halkayı anlatan tur (Tur 1/4, Atla, Sonraki) |
| H06 | tur2 | canliDers/CanliDersTur.tsx | KISMİ | Eksik: "cümleye uzun bas → spot/not/kart yap, PDF yeri işaretlenir" turu ve arkasındaki uzun basma eylemi (kodda yok) |
| H07 | acilir | shell.css | VAR |  |
| H08 | cekmece | shell.css (bulanık perde, 22–24 px köşe) | VAR |  |
| H09 | altCekmece | shell.css | VAR |  |
| H10 | toastlar | shell.css hap bildirim | VAR |  |
| H11 | yukleme | .v15-skel | VAR |  |

## I · Açılış ve kayıt

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| I01 | splash | index.html #app-splash | VAR | Açılış ekranı (kalp + EKG), temaya göre zemin |
| I02 | intro1 | OnboardingV12 (v15 ilerleme çubuğu) | KURULDU | tam sayfa tanıtım |
| I03 | intro2 | OnboardingV12 | KURULDU | tam sayfa tanıtım |
| I04 | intro3 | OnboardingV12 | KURULDU | tam sayfa tanıtım |
| I05 | girisSecenek | AuthV12 Giriş/Kayıt sekmesi | KURULDU | Hesabına gir |
| I06 | otp | — | VAR | e-posta bağlantısıyla şifresiz giriş (EpostaBaglantiGiris); Firebase Email link açık, canlıda denendi 2026-10-27 |
| I07 | kayitUni | OnboardingV12? | VAR | v15/ProfilKurulumV15.tsx (üniversite adımı) |
| I08 | kayitSinif | OnboardingV12? | VAR | v15/ProfilKurulumV15.tsx (sınıf adımı) |
| I09 | kayitKurul | OnboardingV12? | VAR | v15/ProfilKurulumV15.tsx (kurul adımı, kurulKaydet) |
| I10 | kayitHedef | OnboardingV12? | VAR | v15/ProfilKurulumV15.tsx (hedef adımı) |
| I11 | kayitBitti | OnboardingV12 Bitir | KURULDU | Hücren doğdu (ProfilKurulumV15) |

## J · Grafik ve şemalar

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| J01 | grafikler | stats → StatsView + v15/CalismaGrafikleriV15.tsx | KURULDU | doğru oranı çizgisi (baraj %60) + çalışma takvimi; sınıf ortalaması verisi yok |
| J02 | grafikDetay | — | VAR | IstatistikV15 Konular: performans + unutma eğrisi |
| J03 | zihin | zihin_haritasi (bağlantısız) | BİLİNÇLİ YOK | Kullanıcı reddetti (2026-10-27) |
| J04 | yolHaritasi | — | BİLİNÇLİ YOK | J03–J06 grubu reddedildi (plan) |
| J05 | akis | — | BİLİNÇLİ YOK |  |
| J06 | zamanCizelgesi | v15/SinavTakvimiV15.tsx (yılın sınavları) | VAR | Sınav takvimi yılın sınavları zaman çizelgesi |

## K · Not ve kalem

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| K01 | renklendir | NotlarimV15 fosforlu | KURULDU | seçili metne 5 renk + temizle; renk aralıkları (Not.boya) metin kutusunun arkasındaki katmanda, yazdıkça kayar |
| K02 | kalemPdf | CdV15KalemKutusu (sesli ders) | VAR |  |
| K03 | kalemNot | NotlarimV15 kalem | BİLİNÇLİ YOK | el yazısını metne çevirme tanıma modeli gerektirir (yerel GPU/LLM yasağı) |
| K04 | notEditor | NotlarimV15 | KURULDU | madde listesi düğmesi + Enter ile yeni madde; ses damgası (B11) var |
| K05 | notPaylas | — | VAR | NotPaylasV15 + notPaylas.ts |
| K06 | paylasilan | — | VAR | /notlarim?gorunum=paylasilan |
| K07 | yaziAyar | Profil › Görünüm/Erişilebilirlik (v12/ProfileV12.tsx), sesli ders okuma (canliDers/CdV15.tsx) | KISMİ | Okuma yazısı, arayüz ölçeği, geniş satır/harf aralığı anahtarı, sesli derste boyut/satır aralığı/zemin var; eksik: canlı önizleme metni, kalınlık (400/500/600), hizalama (Sola/İki yana), harf aralığı kaydırıcısı, vurgu (işaretleyici) rengi seçimi tek ekranda |
| K08 | yaziOrnek | — (tasarım belgesi) | YOK | Kod karşılığı gerekmez |

## L · Topluluk ve listeler

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| L01 | sohbetListe | topluluk → v15/ToplulukV15.tsx | VAR | sohbet listesi + oda + davet kodu (toplulukSohbet.ts, topluluk_sohbet.sql) |
| L02 | sohbet | ToplulukV15 kanal | VAR |  |
| L03 | yorumlar | ToplulukV15 ders yorumları | VAR | yorumlar: En faydalı/En yeni, beğeni toggle (yorum_begeni), yanıt |
| L04 | soruListe | quick_add/PoolView | VAR | PoolV12: kişisel süzgeç çipleri (Hepsi/Yanlışlarım/Kaydettiklerim/Yorumlu) |
| L05 | kurulListe | "Kurul seç" | KURULDU | KurulSecV15 tema adları + durum |
| L06 | seneSec | SesliListeV15 "2025-26 arşivi" | KURULDU | dönem seçici 2026–27 / 2025–26 |

## M · Hücrem

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| M01 | hucrem | hucrem → v15/HucremV15.tsx + Hucre3D | VAR |  |
| M02 | evrim | HucremV15 (28 basamak) | VAR |  |
| M03 | evrimDetay | HucremV15 | VAR | HucremV15: basamak ayrıntısı (evrimDetay) |
| M04 | glukoz | HucremV15 glukoz | VAR |  |
| M05 | hucreStres | HucremV15 "Hücren aç kalıyor" | VAR | canlılık çubuğu + "Hücren aç kalıyor/uykuda" durumu |
| M06 | seviyeAtla | — | VAR | HucremV15: seviye atlama kutlaması (Paylaş + Harika) |
| M07 | siralama | leaderboard + Hucrem "Hücre sırası" | VAR | SiralamaV15: Sınıfım/Üniversite/Türkiye/Arkadaşlar; üniversite süzgeci sunucuda; arkadaş sistemi yok (boş durum) |
| M08 | profil2 | ProfileV12 v15 | KURULDU | profil kartında okul/sınıf/kurul |
| M09 | profilDuzenle | v15/ProfilKurulumV15.tsx + Hesap paneli + v15/GizlilikAnahtari.tsx | VAR | Okul, sınıf, öğrenci no, eğitim yılı, kurul, hedef; ad/fotoğraf Hesap'ta; "herkese açık" anahtarı. Ayrı "Hücremi herkese göster" anahtarı yok |
| M10 | basarim2 | basarimlar | VAR | BasarimView + rozet ayrıntısı |
| M11 | rozetDetay | — | VAR | BasarimView: rozet ayrıntısı (baklava rozet, seviye, tarih, Paylaş) |
| M12 | evrimYol | HucremV15 basamak yolu | VAR | HucremV15: evrim yolculuğu, önceki/sonraki, zaman çizgisi |
| M13 | cag1 | — | VAR | HucremV15: çağ sekmesi + basamak kartları |
| M14 | cag2 | — | VAR | HucremV15: çağ sekmesi + basamak kartları |
| M15 | cag3 | — | VAR | HucremV15: çağ sekmesi + basamak kartları |
| M16 | cag4 | — | VAR | HucremV15: çağ sekmesi + basamak kartları |
| M17 | hucreKarsilastir | — | VAR | Hücrem Karşılaştır |

## N · Quiz kipleri

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| N01 | quizModSec | OyunlarV15 tür seçimi | KURULDU | Oyunlar mod kartları |
| N02 | quizGorsel | — | KISMİ | kod hazır; havuzda görselli soru yok, kart gizli |
| N03 | quizCumle | OyunBoslukV15 | VAR | Terimi bul (OyunBoslukV15) |
| N04 | quizCan | OyunSoloV15 "Hayatta kal" | VAR |  |
| N05 | quizZaman | OyunSoloV15 Blitz | VAR |  |
| N06 | quizTakim | — | VAR | takım modu (quizRealtimeServer) |
| N07 | quizKaydir | — | VAR | OyunDersV15 Kaydır |
| N08 | quizSonuc2 | OyunSoloV15 sonuç | VAR | solo sonuç: puan/doğru + rekor + yeniden oyna |

## O · Video, PDF, tam ekran

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| O01 | video | — | KISMİ | VideoDersV15; hazır video yok, giriş gizli |
| O02 | videoTam | — | KISMİ | VideoDersV15 tam ekran |
| O03 | videoPip | — | KISMİ | VideoDersV15 PiP |
| O04 | pdfOkuyucu | Öğren ders PDF'i (PDF.js) | VAR | DeckPdfViewer/PdfDocView: sayfa gezinme, yakınlaştırma, tema, tam ekran |
| O05 | pdfIzgara | — | VAR | DeckPdfViewer: sayfa ızgarası, Tümü/İşaretli, sayfa işaretleme |
| O06 | pdfArama | — | VAR | DeckPdfViewer: arama, eşleşme listesi + parça metin |
| O07 | pdfIkili | — | KISMİ | DeckPdfViewer: aynı PDF'te iki sayfa yan yana; başka dersle karşılaştırma yok |
| O08 | tamEkranOgren | ShellV15 Tam ekran | KURULDU | tam ekran + tam-katman |
| O09 | tamEkranSoru | ShellV15 Tam ekran | KURULDU | tam ekran + tam-katman |
| O10 | tamEkranAyar | — | KISMİ | v15/TamEkranAyarV15.tsx: uygulama tam ekranı, Wake Lock, kısayollar; "kendiliğinden tam ekran" ve "yatayda yan yana" yok |

## P · İkonlar

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| P01 | ikonlar | — (tasarım belgesi) | YOK | Kod karşılığı gerekmez |

## T · Kronometre

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| T01 | kronoSoru | — | VAR | soru ekranında kronometre |
| T02 | kronoAcik | v15/KronometreV15.tsx | VAR |  |
| T03 | kronoSesli | — | YOK | Sesli derste gizli (bilinçli tasarım dışı seçim) |
| T04 | kronoVideo | — | VAR | data-kr-yuva="video" yuvası |
| T05 | kronoBirlesme | — | VAR | mini oynatıcıyla birleşme |
| T06 | kronoDurum | KronometreV15 | KURULDU | zar baloncuğu durumları |
| T07 | kronoAyar | — | VAR | v15/KronometreEkranV15.tsx: kronometre ayarları + geçmiş |
| T08 | kronoGecmis | KronometreV15 (localStorage 50 oturum) | KURULDU | Kronometre geçmişi ekranı |
| T09 | kronoPc | KronometreV15 | KURULDU | PC: aynı baloncuk, sürüklenebilir |
| T10 | kronoFormlar | — | VAR | biçim seçimi |
| T11 | kronoF1 | — | VAR | Nokta |
| T12 | kronoF2 | — | VAR | Hap |
| T13 | kronoF3 | — | VAR | Kenar sekmesi |
| T14 | kronoF4 | — | VAR | Başlık çipi |
| T15 | kronoF5 | — | VAR | İnce çizgi |

## U · Çalışma kapsülü

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| U01 | kapDers | v15/KapsulV15.tsx | KURULDU | kronometre + oynatıcı kaynaşması |
| U02 | kapOgren | KapsulV15 | KURULDU | aynı |
| U03 | kapSpot | KapsulV15 | KURULDU | aynı |
| U04 | kapSozluk | KapsulV15 | KURULDU | aynı |
| U05 | kapNotlar | KapsulV15 | KURULDU | aynı |
| U06 | kapOnem | KapsulV15 | KURULDU | aynı |
| U07 | kapPdf | KapsulV15 | KURULDU | aynı |
| U08 | kapZihin | — | BİLİNÇLİ YOK | Zihin haritası reddedildi |
| U09 | kapSoru | KapsulV15 | KURULDU | aynı |
| U10 | kapAcik | KapsulV15 | VAR |  |
| U11 | kapYanMenu | SideNavV15 Odak girişi | KURULDU | Menü › Odak/Kronometre |
| U12 | kapYanMenuSesli | — | VAR | ShellV15 yan menü oynatıcı kapsülü |

## V · Tema, motif, şema

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| V01 | temaGaleri | Ayarlar › Tasarım/Görünüm (palettes.ts) | VAR | Görünüm: tasarım + tema + palet seçici |
| V02 | temaSec | Ayarlar › Görünüm | VAR | tema seçici |
| V03 | motifler | — | VAR | motifler.css + GorunumEkleri |
| V04 | yaziTipleri | — | VAR | GorunumEkleri yazı tipleri |
| V05 | vucut | — | BİLİNÇLİ YOK |  |
| V06 | kalpSema | — | BİLİNÇLİ YOK |  |
| V07 | labSema | — | BİLİNÇLİ YOK |  |
| V08 | ekgSema | — | BİLİNÇLİ YOK |  |

## W · Palet, kart, zihin biçimleri

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| W01 | paletDuzenle | Ayarlar | VAR | palet düzenle (kontrast kapılı) |
| W02 | paletGaleri | Ayarlar palet | VAR | palet seçici |
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
| X01 | istatGun | StatsView (7/30 gün) | VAR | çubuğa dokununca gün ayrıntısı |
| X02 | istatHafta | StatsView 7 gün | VAR | 7 gün kipi |
| X03 | istatAy | StatsView 30 gün | KURULDU | 30 gün kipi + 15 haftalık çalışma takvimi |
| X04 | istatSoru | StatsView | VAR | IstatistikV15 Genel |
| X05 | istatSoruTek | — | VAR | IstatistikV15 Sorular |
| X06 | istatSoruDetay | — | VAR | soru detayı |
| X07 | istatPuan | — | VAR | puan |
| X08 | istatKonu | — | VAR | IstatistikV15 Konular |
| X09 | grafikTurleri | — (tasarım belgesi) | YOK | Kod karşılığı gerekmez |
| X10 | grafikAyar | — | VAR | grafik ayarı |

## Y · Süzgeç ve PDF oluştur

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| Y01 | filtreTam | SorularMerkezV15 Test oluştur | KURULDU | Test oluştur: ders + kaynak + zorluk + sayı + kip (adres parametreleri) |
| Y02 | filtreHizli | SorularMerkezV15 çipleri | KURULDU | kaynak/zorluk hızlı çipleri |
| Y03 | filtreAktif | — | VAR | SoruSuzgecV15 çipler |
| Y04 | filtrePanel | — | VAR | SoruSuzgecV15 yan panel |
| Y05 | filtreKayitli | — | VAR | kayıtlı süzgeçler |
| Y06 | filtreBos | "Bu süzgeçte … yok" metinleri | VAR |  |
| Y07 | pdf1 | pdf_olustur → v15/PdfSihirbaziV15.tsx | VAR |  |
| Y08 | pdf2 | PdfSihirbaziV15 | VAR |  |
| Y09 | pdf3 | PdfSihirbaziV15 | VAR |  |
| Y10 | pdf4 | PdfSihirbaziV15 → TopluPdf | VAR | PDF sihirbazı dördüncü adım ortak TopluPdf |
| Y11 | pdfHazirlik | TopluPdf | VAR | TopluPdf hazırlık |
| Y12 | pdfHazir | TopluPdf | VAR | TopluPdf hazır |
| Y13 | pdfGecmis | PdfSihirbaziV15 Geçmiş | VAR |  |

## Z · Ekran haritası ve araç listeleri

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| Z01 | ekranHaritasi | — (tasarım belgesi) | YOK | Kod karşılığı gerekmez |
| Z02 | arac_dersler | DerslerMerkezV15 Diğer araçlar çekmecesi | VAR |  |
| Z03 | arac_soruMerkez | SorularMerkezV15 "Araçlar" | KURULDU | Soru çöz araçlar ızgarası |
| Z04 | arac_kamplar | KamplarMerkezV15 | KISMİ | Tasarımdaki "Planlama" listesi: Sınav takvimi ve Sınav planı (yol haritası) var; eksik: Olası sorular satırı (rota var, merkezde yok), Sınav ağırlığı kabarcık haritası (yok) |
| Z05 | arac_kaynaklar | KaynaklarMerkezV15 | KISMİ | Tasarımdaki "Topluluk ve belgeler" listesinin hiçbir satırı merkezde yok: Sohbet (topluluk), Paylaşılan notlar, Oluşturduğum PDF'ler, Kurul takvimi; sayfada yalnız başvuru kartları |
| Z06 | arac_oyunMerkez | OyunlarV15 | KURULDU | Oyunlar mod kartları |
| Z07 | arac_profil2 | v15/TumSayfalarV15.tsx | VAR | Menü (TumSayfalarV15) grupları |

## AA · Ders programı

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| AA01 | dpListe | ders_programi → v15/DersProgramiV15.tsx | VAR |  |
| AA02 | dpHafta | DersProgramiV15 | VAR |  |
| AA03 | dpGun | DersProgramiV15 | VAR |  |
| AA04 | dpAy | DersProgramiV15 (Ay ızgarası) | VAR | Plan "ay yok" diyor; kodda ay görünümü var (plan güncel değil) |
| AA05 | dpDetay | DersProgramiV15 → ders ayrıntısı | VAR | ders programındaki ders → ders ayrıntısı (sesli ders, Öğren, çıkmış sorular) |
| AA06 | dpEkle | — | YOK | Ekle/içe aktar yok |
| AA07 | dpWidget | — | YOK |  |

## AB · Hesap, arka plan, uygulama temelleri

| Kod | Ad | Site karşılığı | Durum | Not |
|---|---|---|---|---|
| AB01 | arkaPlan | — | YOK | Arka plan işleri ekranı yok |
| AB02 | arkaPlanUst | — | YOK |  |
| AB03 | kisisel | ProfileV12 | VAR | Profil › Hesap |
| AB04 | hesapGuvenlik | ProfileV12 hesap | VAR | Profil › Hesap (şifre, oturum) |
| AB05 | veriGizlilik | ProfileV12 verilerim | VAR | Profil › Veriler ve gizlilik |
| AB06 | bildirimTercih | — | YOK | Bildirim türü başına anahtarlar (sınav öncesi pratik, yeni ders, düello/sınıf, hücre, sohbet, yenilikler) ve Sessiz saatler yok |
| AB07 | erisilebilirlik | ProfileV12 Erişilebilirlik | VAR |  |
| AB08 | dilBolge | — | YOK |  |
| AB09 | komutPaleti | ⌘K arama | KURULDU | ⌘K: karma test, yanlışlar, kronometre, odak, yeni not, tam ekran, tema komutları |
| AB10 | kisayollar | v15/TamEkranAyarV15.tsx (Profil › Tam ekran ve kısayollar) | KISMİ | 8 kısayolluk düz liste var; eksik: Genel/Sesli ders/Soru/Kronometre grupları ve ?, G sonra B, [ ] hız, M işaretle, H yardım al, T/L/R kronometre kısayolları |
| AB11 | baslangicGorev | — | YOK |  |
| AB12 | geriAl | NotlarimV15 "Geri al" | KURULDU | geriAlinabilir(): not, yanlış, kişisel sınav silmede 6 sn "Geri al" bildirimi (onay penceresi yerine) |
| AB13 | cevrimdisiBanner | system/NetworkBanner.tsx | VAR | "Çevrimdışısın" + "n sırada" hapı, bağlanınca gönderim; metin tasarımdaki "cevapların bağlanınca eşitlenecek" değil |
| AB14 | yardimMerkezi | — | YOK |  |
| AB15 | yenilikler | guncellemeler | VAR | GuncellemeGunluguView: sürüm kartları (sürüm, gün/saat, başlık, eklenen/değişen/düzeltilen maddeler) |
| AB16 | hata404 | — | YOK | Bilinmeyen adres sessizce ana sayfaya (Soru ekle) düşüyor (router.ts parseLocation → quick_add); eksik: "Bu sayfa bulunamadı" ekranı + Ara + Bugün'e dön |
| AB17 | hataSunucu | main.tsx RootErrorBoundary | KISMİ | Hata ekranı (Geri dön / Sayfayı yenile) var; eksik: tasarım metni ("Bir şeyler ters gitti", "Sorun bize iletildi"), İndirilenler düğmesi; ham hata metnini öğrenciye gösteriyor; v15 görünümü değil |
| AB18 | bakim | — | YOK | Bakım ekranı (dişli, "Kısa bakım", tahmini süre, çalışman kaydedildi) yok; yalnız UpdatePrompt "Site güncellendi" |

- S08: KURULDU (2026-10-27): satır aralığı, yazı tipi (Okuma/Sade/Kolay okunur), zemin, okunan cümleyi ortala
- S09: KURULDU: oynatıcı çekmecesinde Bölümler / Yıldızlılarım sekmeleri
- S10: KURULDU: seçim çubuğu Nota ekle · Yıldızla · Kopyala (Açıkla/Soru üret LLM gerektirir, yok)
- S16: KURULDU: medyaSession zaten vardı; kilit ekranında okunan cümle + ±15 sn eklendi
- S18: KURULDU: Bölüm sonunda dur + Tekrar dinle / Pekiştir / Devam et kutusu
- S20: KURULDU: Sözlükte aç · Karta ekle
- S21: KURULDU: oynatıcıda "n kez çıkmışta soruldu · Çöz" şeridi (yalnız doğrulanmış eşleme)
- S26: VAR (denetim kaçırmıştı): dört gruplu ders seçenekleri
- S28: KURULDU: oynatıcı seçenekleri alt çekmecesi
- S26 ders seçenekleri: v15.4 yeniden düzen (kullanıcı geri bildirimi: uzun/okunaksız) — 3 grup, simgeli kare ızgara
- C01: Tekrar zamanı kartı Yanlışlarım'a bağlandı (karma test/kip seçici henüz yok)
- C03: seri rozeti (Derste 04:18 bağlantısı: soru–ders zaman eşlemesi verisi yok; takip sorusu: LLM, yok)
- C04: '48 saat sonra yeniden soracağım' + Yanlışlarım bağlantısı (services/yanlislarim.ts)
- C09: KURULDU /sorular/yanlislarim (Tekrar zamanı · Bekleyen · Öğrenildi, hazırları çöz)

### KURULDU (2026-10-27, devam)
- A03 menü: Oyunlar ayrı bölüm (Oyunlar · Hücrem · Başarımlar), her bölüm başlığının altında içerik açıklaması.
- B04 sesli liste: Yeni (hiç dinlenmemiş; listede eklenme tarihi yok) ve İndirilen süzgeçleri, sıralama (ders sırası / son dinlenen / kısa olan önce), indirildi işareti.
- B11 notlar: Tümü / Yıldızlı / Ses damgalı süzgeci, kartta yıldız; sesli dersten "Nota ekle" ders · bölüm · zaman damgasıyla gelir, damgaya dokununca derste o yere gider (eski notlarda "Kaynak:" satırından okunur).
- Kronometre ayarları + geçmişi (T › kronoAyar, kronoGecmis).
- A06 bildirim merkezi: /bildirimler (zil buraya), Tümü/Ders/Soru/Sistem sekmeleri + okunmamış sayıları, Tümünü okundu say, Okunmuşları temizle; hesap bildirimleri + gerçek veriden türeyen (yeni sesli ders, sınava ≤14 gün, tekrar zamanı gelen yanlışlar). Düello daveti yok (düello özelliği yok).

## Değerlendirilmemiş ekranların değerlendirmesi (2026-10-27)

Kök neden: ilk denetim "DOĞRULANMADI" (50) ve "KISMİ" satırlarını sıraya koymadı; iş yalnız kullanıcının saydığı öncelik
listesinden yürüdü, I07–I10 kayıt adımları gibi bütün bir akış hiç ele alınmadı. Bundan sonra her tur bu tablodan seçer;
"DOĞRULANMADI" kalmaz.

| Kod | Karar | Not |
|---|---|---|
| I07–I11 kayitUni/Sinif/Kurul/Hedef/Bitti | KURULDU | ProfilKurulumV15: girişten sonra eksik profile bir kez; Profil › Okul ve hedef; hedef Bugün planına bağlı. Hatırlatma saati kaydediliyor, bildirim gönderimi yok |
| M09 profilDuzenle | KISMİ → KURULDU (okul/sınıf/kurul/hedef) | Ad/fotoğraf Hesap panelinde |
| B08 spotlar | KURULDU | Yıldızlı süzgeci, kart altı ders + "Derste dinle" (?ara= ile en yakın paragrafa). "n kez çıktı": spot verisinde çıkmış eşlemesi yok → yazılmadı |
| I01 splash | VAR | index.html açılış ekranı (kalp + EKG) |
| I02–I04 intro1-3 | KURULDU (sonraki turlar) | Onboarding sahneleri eski metinle; tasarım metni (PDF takip, şık açıklaması, hücre) ile değiştirilecek |
| I05 girisSecenek / A01 | KURULDU (sonraki turlar) | Google + e-posta var; Apple ve sınıf kodu altyapısı yok (sınıf kodu: sunucu gerektirir) |
| I06 otp | YAPILDI | Kod yerine Firebase e-posta bağlantısıyla şifresiz giriş (2026-10-27, canlıda doğrulandı) |
| A05 arama | VAR | SearchPalette ⌘K |
| B18 b2ornek, B19 b2oncelik, B21 b2masa, B22 b2muzik | KURULDU (sonraki turlar) | Sayfalar var, v15 yapısı denetlenecek |
| S04 altyazı şeridi, S15 yatay telefon, S17 bağlantı koptu | KURULDU (sonraki turlar) | S17: oynatıcıda çevrimdışı kaydı varken uyarı kartı |
| C09 hatalar | KURULDU | YanlislarimV15 |
| E04 kmbCizim, E05 kmbKontrol | KURULDU (sonraki turlar) | KMB veri yapısına bağlı |
| G03 asistan | BİLİNÇLİ | Yapay zekâ sohbeti LLM gerektirir (kural 20) |
| G07 cevrimdisi | VAR | CevrimdisiView (başka oturum geliştiriyor) |
| H05–H06 tur | VAR | Tanıtım turu |
| K07 yaziAyar | VAR | Erişilebilirlik + sesli ders okuma ayarları |
| L04 soruListe | KURULDU (sonraki turlar) | Havuz listesi v15 yapısı |
| M03, M06, M11–M16 hücre/evrim/rozet/çağlar | KURULDU (sonraki turlar) | HucremV15 3B sahne var; seviye atlama, rozet ayrıntısı, çağ ekranları yok |
| O04–O07, O10 PDF okuyucu/ızgara/arama/ikili/tam ekran | KURULDU (sonraki turlar) | PDF.js görüntüleyici tek sayfa; ızgara, arama, ikili sayfa yok |
| Kronometre T, U | KURULDU | Kaynaşma, ayarlar, geçmiş |
| A06 bildirim | KURULDU | /bildirimler |
- I02–I04 tanıtım: tam sayfa (Atla, resim, noktalar, ortalı başlık, İleri/Başlayalım), tasarım metinleri. I05 giriş: "Hesabına gir", Google + "Öğrenci e-postasıyla kayıt ol" + e-posta/şifre + Şifremi unuttum; Apple ve sınıf kodu altyapı olmadığı için yok (sahte düğme konmadı).
- O04 PDF okuyucu: VAR (DeckPdfViewer: sayfa gezinme, yakınlaştırma, tema, tam ekran). O06 arama: VAR (eşleşme listesi + parça metin; denetim yanlışlıkla DOĞRULANMADI demişti). O05 ızgara: KURULDU (tüm alan ızgara, Tümü/İşaretli, sayfa işaretleme). O07 ikili: KURULDU aynı PDF'te iki sayfa yan yana (başka dersle karşılaştırma yok). O10 tam ekran: KURULDU Profil › Tam ekran ve kısayollar (uygulama tam ekranı, sesli derste ekran kararmasın/Wake Lock, kısayol listesi); "kendiliğinden tam ekran" ve "yatayda yan yana" yok.
- M03/M12 evrim ayrıntısı + yolculuk: KURULDU (basamağa dokun → tam sayfa: 3B/çizim, önceki/sonraki, 28'lik zaman çizgisi, bu basamaktaki bilgi). M13–M16 çağlar: KURULDU (çağ sekmesi + kartlar). M06 seviye atlama: KURULDU (basamak açılınca kutlama + Paylaş). M11 rozet ayrıntısı: KURULDU (Başarımlar kartı › Rozeti gör; tarih defterden). M04 hücre karşılaştır yok.
- S04 altyazı: KURULDU (görünüm "Altyazı": slayt tüm alan + önceki cümle soluk / okunan cümle vurgulu şerit). S15 yatay telefon: KURULDU (alçak yatay ekranda bölmeler yan yana, üst bar sıkışır). S17 bağlantı koptu: KURULDU (çevrimdışı + indirilmemiş derste kart: durduğu an / arabellek süresi, Tekrar dene; bağlantı gelince yeşil).
- B22 müzik: KURULDU (MuzikV15: çalar kartı + 25/45/ders bitene kadar süre + liste + ekle). B21 masa: KURULDU üst bölüm (hafta şeridi, günün akışı etkinlik günlüğünden, bugün süre/hedef, seri); plan yok (uydurma akış yazılmadı). B19 öncelikli: pano eklendi (ders sayısı, dinleme, beklenen soru, branş puan/emek çubukları). B18 örnek: özet (toplam/çözdüğün %/bugün; bugün sayacı bu sürümden itibaren) + kart eylemi. L04 havuz: kişisel süzgeç Hepsi/Yanlışlarım/Kaydettiklerim/Yorumlu (PoolV12).
- E04 kmbCizim: KURULDU "Etiketleri yerleştir" (Sınav sekmesi; sahnenin etiketli yapıları seçilip sahnede yerine dokunulur, yanlış deneme sayılır). E05 kmbKontrol: KURULDU "Değerlendirme" (OSCE akışının ana basamakları Yaptım/Atladım, %80 ile Geçti, son sonuç cihazda).
