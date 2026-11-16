# ⚠️ TÜM AJANLARIN DİKKATİNE (KESİNLİKLE ZORUNLU KURAL):
> **HER HATA ÇÖZÜMÜNDE HATANIN KÖK NEDENİ VE ÇÖZÜMÜ MUTLAKA BELGELENMELİ VE TÜM AJANLAR TARAFINDAN DİKKATLE İNCELENMELİDİR!**
> Karşılaşılan ve çözülen her hata için:
> 1. Belirti (Kullanıcının gördüğü problem)
> 2. Kök neden (Teknik ve mantıksal kaynak problem)
> 3. Çözüm ve geleceğe yönelik katı önleme kuralı
> eksiksiz olarak bu deftere işlenmeli; hiçbir ajan kök nedeni anlamadan yüzeysel geçici yamalar yapmamalı ve bu defteri okumadan geliştirme yapmamalıdır!

# Kurul 2 — Yapılmayacak Hatalar Defteri (ZORUNLU OKUMA)

> Kurul 2'de sistem tam otomatik çalışacak: Drive'a gelen her yeni PDF'ten interaktif ders (Öğren), sesli spot / sınav asistanı
> ve sesli soru çözücü içeriği insan müdahalesi olmadan üretilip EMA ile seslendirilecek. Bu defter, Kurul 1 içeriğinde kullanıcının
> gördüğü ve **Kurul 2'de bir daha yapılmaması gereken** hataları toplar. Kurul 2 hattını kuran ya da çalıştıran her ajan önce
> bu dosyayı okur. Yeni bir hata bildirildiğinde buraya yeni madde eklenir (eskiler silinmez).
>
> Kurul 1'deki mevcut içerik bu defter yüzünden toplu olarak yeniden üretilmez; amaç gelecekteki üretimdir.

## Bu dosya artık DİZİNDİR (2026-11-16, token tasarrufu)

> Madde metinleri konu dosyalarına **kelimesi kelimesine** taşındı (`docs/hatalar/<konu>.md`); bu dosya yalnız dizindir.
> İşe başlamadan önce bu dizini oku, yalnız işine giren konu dosyasını (ya da madde numarasıyla ilgili maddeyi) aç — hepsini değil.
> Aşama özetleri `scripts/hat/tam_hat/kural_secici.py` ile konu dosyalarından üretilir (`docs/asama_kurallari/`).

| Konu dosyası | Kapsam | Madde |
|---|---|---|
| `hatalar/ses.md` | EMA sesi, okunuş, hoca dökümü, cümle/kelime zamanı | 23 |
| `hatalar/cizim.md` | canlı çizim, çapa, lazer, panel, PDF işareti | 32 |
| `hatalar/soru_cozucu.md` | örnek soru, şık açıklaması, sesli çözücü, önem listesi | 18 |
| `hatalar/ders_metni_anlatim.md` | anlatım metni, slayt sadakati, öğrenci denetçisi | 21 |
| `hatalar/ders_metni_terim_kisaltma.md` | terim ve kısaltma katmanı, PDF metin ayrıştırma, cümle sayacı | 19 |
| `hatalar/ders_metni_degerlendirme.md` | değerlendirme kapısı, sayfa haritası, ders içerik paketi, ders analizi | 16 |
| `hatalar/veri_cikmis.md` | çıkmış soru verisi, eşleme, yıl/kurul etiketi | 29 |
| `hatalar/dagitim_sunucu.md` | dağıtım, Oracle, sunucu, önbellek/SW, çevrimdışı, kimlik | 35 |
| `hatalar/on_yuz_disa_aktarim.md` | soru dışa aktarıcı, PDF/DOCX dışa aktarım, baskı geometrisi | 11 |
| `hatalar/on_yuz_oynatici_ders.md` | sesli ders oynatıcısı, ders ekranı, ders hattı ön yüz kayıtları | 26 |
| `hatalar/on_yuz_tasarim_tema.md` | tasarım, tema, kabuk, düzen, cihaz güvenli alanı | 21 |
| `hatalar/on_yuz_sayfa_denetimi.md` | sayfa denetimi bulguları, öğrenci sayfaları, veri/eşitleme ekranları | 39 |
| `hatalar/yonetim_basarim.md` | yönetim paneli ve ön yüz başarımı | 21 |
| `hatalar/betik_altyapi.md` | betik, LLM zinciri/kilidi, GPU/CPU, kapı altyapısı | 20 |
| `hatalar/ogren_modul_oyun.md` | Öğren destesi, ek modüller, KMB filmleri, oyunlar | 28 |
| `hatalar/diger.md` | genel kurallar ve kayıt maddeleri | 5 |

### Yeni madde nasıl eklenir

1. Tam metni (Belirti · Kök neden · Kalıcı çözüm · Önleme kuralı/Kapı) ilgili `docs/hatalar/<konu>.md` dosyasının **SONUNA**
   `## H<n> — <başlık> (<tarih>)` başlığıyla ekle (konu dosyasında `##`/`###` başlıkları madde sınırıdır).
2. Bu dizinin **SONUNA** tek satır ekle: `- **H<n>** · <tek cümle kural/özet> → hatalar/<konu>.md`.
   Satır sırası = madde sırası: bir konu dosyasındaki k'ıncı madde, dizinde o dosyayı gösteren k'ıncı satırdır.
3. `python3 scripts/hat/tam_hat/kural_secici.py` çalıştır (dizin ↔ konu dosyası tutarlılığını da denetler; uyuşmazlıkta HATA).

### Maddeler (kronolojik)

- **H1** · Geçiştirici şık açıklaması → hatalar/soru_cozucu.md
- **H2** · Türkçeye uymayan ifade ve iç etiketler → hatalar/ders_metni_anlatim.md
- **—** · Kurul 2 hattı için genel kural → hatalar/diger.md
- **—** · Sesli ders PDF/DOCX dışa aktarımı → hatalar/on_yuz_disa_aktarim.md
- **—** · Canlı ders PDF işareti → hatalar/cizim.md
- **—** · Diğer oturumlarda düzeltilen hatalardan çıkarılan dersler → hatalar/diger.md
- **H3** · Kısaltma kelime gibi okunuyor ("DNA" → "deneye") → hatalar/ses.md
- **H4** · Öğrenci metninde iç süreç dili ("PDF'te yok", "aday soru", "bağlanan çıkmış") → hatalar/ders_metni_anlatim.md
- **H5** · Kapının kendisi bozuk (her metin "999 HATA") → hatalar/betik_altyapi.md
- **H6** · Birleştirici ders/dosya siliyor → hatalar/dagitim_sunucu.md
- **H7** · Düzeltme tek kopyada kalıyor (çözücüde düzeltilen soru spot/asistan/örnekte eski) → hatalar/soru_cozucu.md
- **H8** · Aynı PDF iki ders / yanlış PDF eşleşmesi → hatalar/veri_cikmis.md
- **H9** · Görsel ya da bozuk OCR'lı sayfa içerikte yok → hatalar/ders_metni_anlatim.md
- **H10** · Başka dersin sayısı / genel bilgi; çıkmış anahtarı PDF ile çelişiyor → hatalar/veri_cikmis.md
- **H11** · Ses Oracle'a gitmiyor, tarayıcı sesine düşüyor (404) → hatalar/ses.md
- **H12** · Türev veri (cümle/kelime zamanı, işaret, vurgu) metnin başka sürümünden üretilmiş → hatalar/ses.md
- **H13** · Sesli ders bütünlüğü (yönerge okunması, kapanış patlaması, paragraf/süre uyuşmazlığı) → hatalar/ses.md
- **—** · Kurul 2 içeriğinin karşılaması gereken sonradan eklenen özellikler → hatalar/diger.md
- **H14** · Sunucu kodu Oracle'da ama çalışan sunucu eski kodla (yeni uç sitenin ana … → hatalar/dagitim_sunucu.md
- **H15** · Sesli ders + slayt ekranında slayt okunan bilgiye gitmiyor, kelime vurgusu yok → hatalar/cizim.md
- **H16** · Sesli ders listesinde iki ders aynı branş numarasını aldı → hatalar/veri_cikmis.md
- **H17** · EMA okunuş ayarı alt süreçte uygulanmıyordu → hatalar/ses.md
- **H19** · Çıkmış cevap anahtarı tıbben hatalı / iki kaynakta çelişik → hatalar/veri_cikmis.md
- **H18** · Diğer oturumların 2026-10-20 düzeltmelerinden Kurul 2'ye taşınanlar (kayıt) → hatalar/diger.md
- **H20** · Kurul 1'de elle kurulan Son Prova ve anlamsal çapa Kurul 2'de unutulmasın … → hatalar/diger.md
- **H21** · Soru çözücü sonradan genişleyince Son Prova soru kimlikleri kaydı → hatalar/soru_cozucu.md
- **—** · [2026-10-21] Çıkmış soruda iç uyarı metni ve kalıp şık açıklaması (h06/19 Refik … → hatalar/veri_cikmis.md
- **H** · Okunuş ekrana, rakam sese sızıyordu → hatalar/ses.md
- **H22** · Sesli derste dolgu ve asılsız "hoca vurguladı" cümleleri → hatalar/ders_metni_anlatim.md
- **H23** · Öğrenci işaretli slayt yanlış yorumlandı + okunuşla yazılmış metin → hatalar/ders_metni_anlatim.md
- **H24** · Kısa özet derste önemli yerler atlandı, slaytla ilişkisiz/kopuk anlatım → hatalar/ders_metni_anlatim.md
- **H25** · Claude CLI yolu değişti, gece hattının bütün Claude aşamaları sessizce düştü → hatalar/betik_altyapi.md
- **H26** · Ücretsiz modelde sessiz boş yanıt ve yarım JSON → hatalar/betik_altyapi.md
- **H27** · Ücretsiz model zinciri sağlam modeli bütün gün kapatıyordu → hatalar/betik_altyapi.md
- **H28** · Doğrulayıcı tıbbi "kaynaklı"yı süreç dili sanıyordu; önem ↔ çözücü şık uzunluğu uyumsuzdu → hatalar/soru_cozucu.md
- **H29** · "Burası önemli" kuralları birbiriyle çelişiyordu; OCR'lı sayıda sıfır kayıp yanlış alarmı → hatalar/soru_cozucu.md
- **H30** · Çıkmış konu eşlemesi birebir olunca ders sessizce çıkmışsız kalıyordu → hatalar/veri_cikmis.md
- **H31** · Hesap sorusu yanlış alarmı + iç etiketin öğrenci metnine sızması → hatalar/soru_cozucu.md
- **H32** · Zorluk parça içinde yuvarlanınca ders toplamı hedefin altında kalıyordu → hatalar/soru_cozucu.md
- **H33** · Türkçe harfsiz metin kabul ediliyordu + kabul edilmiş iş yeni kapıdan geçirilmiyordu → hatalar/ders_metni_anlatim.md
- **H34** · Ücretsiz katman zinciri: Gemini tavanı, Zen kapandı, OpenRouter eklendi → hatalar/betik_altyapi.md
- **H35** · Ücretsiz/yazılı içerikte betik kapılarından geçen tıbbi hatalar; denetim bulguları düzeltilmiyordu → hatalar/betik_altyapi.md
- **H36** · Cümle sayacı sıra sayısı noktasını cümle sonu sayıyordu → hatalar/ders_metni_terim_kisaltma.md
- **H37** · Oracle'da yayın/işaret yazamıyordu: sahiplik → hatalar/dagitim_sunucu.md
- **H38** · Sesli ders v2 slayt adımı hiç gösterilmiyordu → hatalar/ders_metni_degerlendirme.md
- **H39** · Sesli metin kısaydı: sayfa atlanıyor, şekiller anlatılmıyordu → hatalar/ders_metni_anlatim.md
- **H40** · Canlı çizim çizgileri görünmüyor, amaçları anlaşılmıyordu → hatalar/cizim.md
- **H41** · Yazı satırları arasına çizilen oklar kötüydü; tek tip panel yetmiyordu → hatalar/cizim.md
- **H42** · Okun başlangıcı belirsizdi; resimdeki bölge vurgulanmıyordu → hatalar/cizim.md
- **H43** · Panelde bağımsız iki ilişki tek zincir gibi okunuyordu → hatalar/cizim.md
- **H44** · Sayfaya sığmayan panel gizleniyordu → hatalar/cizim.md
- **H45** · Dar bölmede panel slayta göre büyüyor, yazının üstüne biniyor, kelimeler harf harf … → hatalar/cizim.md
- **H46** · Telefonda panel yazısı okunmayacak kadar küçüktü; panel kelime kenarına biniyordu; ek alan … → hatalar/cizim.md
- **H47** · Kelime takipçisi küçük yazıyı okunmaz yapıyordu; ek alan gereğinden sık ve uzundu → hatalar/cizim.md
- **H48** · Canlı sitede tasarım taraması bulguları → hatalar/on_yuz_tasarim_tema.md
- **H49** · Kırılan zincirde ok yana bakıyordu; panel yazısı büyüktü; takip 8–16 sn duruyordu → hatalar/cizim.md
- **H50** · Panel tıbben yanlış okunuyordu; takip kaydırması sessizce boşa gidiyordu; ekran kalabalıktı → hatalar/cizim.md
- **H51** · Resim slaytında anlatım görselin yerine panelde; yatay zincirde kutular kırılıyordu; testler bunları … → hatalar/cizim.md
- **H52** · Etiket çizimden kopuk; PDF'in kendi oku yeniden çiziliyordu → hatalar/cizim.md
- **H53** · Resim üstündeki çizim asıl yapının önünü kapatıyordu → hatalar/cizim.md
- **H54** · Benzer soru araması boş döndü, ders çıkmışsız üretildi → hatalar/veri_cikmis.md
- **H55** · Görsel tablodan yanlış satır okundu; hocanın kendi çelişkisi kesin "sınav spotu" yapıldı → hatalar/ders_metni_anlatim.md
- **H56** · Yeni yayınlanan dersin PDF'i uygulamada açılmıyordu → hatalar/dagitim_sunucu.md
- **H57** · Kurul 2 derslerinde çıkmışlar neredeyse hiç duyulmuyordu → hatalar/veri_cikmis.md
- **H58** · EMA cümle ortasında sesi düşürüp es veriyordu → hatalar/ses.md
- **H59** · Arşiv derslerinde lazer resim ve tabloları göstermiyordu → hatalar/cizim.md
- **H60** · Slayt Çizimlerinin Toplu Gösterilmesi ve Erken/Tekrarlı Çizim Hatası (`sayfaCizimleri` Yasağı) → hatalar/cizim.md
- **H61** · Üst Üste Çakışan ve İç İçe Geçen Çizgi/Kontur Hatası → hatalar/cizim.md
- **H62** · Quiz Üretiminde Öncelik Sırasının İhlali, Çifte Analiz Maliyeti ve Yarış Durumu Hatası → hatalar/soru_cozucu.md
- **H63** · Sesli Derslerde Arşiv PDF'lerinin Çok Geç Yüklenmesi veya Hiç Yüklenmemesi (AutoFetch, SW … → hatalar/dagitim_sunucu.md
- **H64** · Sayfa haritası adım numaraları tekrar sayfalarını saymıyordu; kısa/eksik kanıt → hatalar/ders_metni_degerlendirme.md
- **H65** · Tablo sayfasında tabloyu anlatmayan cümleye şekil/tablo çapası → hatalar/cizim.md
- **H66** · İlgili çıkmış sorular sesli derste hiçbir cümleye bağlanmamış → hatalar/veri_cikmis.md
- **H67** · H64 tekrarı: harita adımları checkpoint'siz sayıldı + deste `bolum` alt başlık numarası → hatalar/ogren_modul_oyun.md
- **H68** · H66 tekrarı + süs bölüm sayfaları `sekil` türünde → hatalar/ders_metni_degerlendirme.md
- **H69** · `cikmis_baglantilari.json` liste yerine nesne sarmalayıcısıyla yazıldı → hatalar/veri_cikmis.md
- **H70** · Mekanik 2 Cümlelik Şablon ve Yüzeysel Anlatım Yasağı (Sıfır Bilgi Kaybı ve … → hatalar/ders_metni_anlatim.md
- **H71** · PDF metnindeki ayrışık (decomposed) harfler terim eşleşmesini bozuyordu → hatalar/ders_metni_terim_kisaltma.md
- **H72** · Çok sözcüklü terimin kısa son sözcüğü ek aldığında eşleşmiyordu → hatalar/ders_metni_terim_kisaltma.md
- **H73** · `terim/` klasörü dağıtım betiğinin veri listesinde yoktu; terim dosyaları canlıya ulaşamıyordu → hatalar/dagitim_sunucu.md
- **H74** · Madde imi kelimeye yapışık gelince terim işaretlenemiyordu → hatalar/ders_metni_terim_kisaltma.md
- **H75** · Gündelik Türkçe sözcükler terim diye işaretlenmişti → hatalar/ders_metni_terim_kisaltma.md
- **H76** · Cümle sayısı kapısı kısaltma noktalarını cümle sonu sayıyordu → hatalar/ders_metni_terim_kisaltma.md
- **H77** · Kısaltma katmanı eklenirken üç ayrı tuzak: büyük harfli Türkçe sözcük, tireyle bitişik … → hatalar/ders_metni_terim_kisaltma.md
- **H78** · Gece otomatik LLM hattı kullanıcının Claude limitini tüketti; Oracle ders işçisi manuel … → hatalar/betik_altyapi.md
- **H79** · Otomatik çıkmış→cümle eşlemesi (vektör) derse ait olmayan soruları "çıkmış" diye bağladı → hatalar/veri_cikmis.md
- **H80** · Öğrenci Drive betiği uzantısız PDF'i not saymadı; kısaltma bulucu "HT+DM" yazımını kaçırdı → hatalar/ders_metni_terim_kisaltma.md
- **H81** · Amfi kaydı tek parça + VAD ile verilince Whisper "Altyazı M.K." sanrısıyla … → hatalar/ses.md
- **H82** · Çıkmış soru penceresi şık seçilince kayboldu, ders sürmedi → hatalar/on_yuz_oynatici_ders.md
- **H83** · "Çıkmış" diye gösterilen iki soru doğrulanamadı; biri sitede yüklenmedi → hatalar/veri_cikmis.md
- **H84** · Kaynağı olmayan 86 Kurul 2 "çıkmış"ı Check-Solve onayıyla görünür kalıyordu → hatalar/veri_cikmis.md
- **H85** · Çizim önemli bölgeyi örtüyor, zoom yanlış/fazla, kelime ↔ kelime oku okumayı bozuyor → hatalar/cizim.md
- **H86** · Sınav planı Kurul 2'de boş sayfa → hatalar/on_yuz_sayfa_denetimi.md
- **H86** · Ders işçisi denetimi örnek soru şık açıklamalarını standart kapıdan geçirmiyordu → hatalar/soru_cozucu.md
- **H87** · Çizim doğrulayıcısının komut satırı Kurul 2 cümle kimliklerini ve resim kutularını tanımıyor; … → hatalar/cizim.md
- **H88** · Drive klasör adı değişince yayın PDF'in kaynak kimliğini bulamadı → hatalar/dagitim_sunucu.md
- **H89** · Slayttaki yapışık madde imi glifi (U+F06E) kısaltmayı ve kanıt eşlemesini bozdu → hatalar/ders_metni_terim_kisaltma.md
- **H90** · Anlam denetimi önbellek anahtarı değişince denetim sessizce atlandı → hatalar/betik_altyapi.md
- **H87** · v15 katmanlarında tanımsız renk/yazı değişkenleri: saydam kartlar, varsayılan yazı tipi → hatalar/on_yuz_tasarim_tema.md
- **H91** · Çizim PDF'i önbellekte olmayınca bütün konturlar sessizce reddedildi → hatalar/cizim.md
- **H92** · Bilinen kısaltma sözlüğü bağlamsız: MSS "Muskuloskeletal sistem" diye açıldı → hatalar/ders_metni_terim_kisaltma.md
- **H93** · Çapa değişince PDF işareti yenilenmedi → hatalar/cizim.md
- **H94** · Çıkmış listesinde birleştirilmiş gizli kopya: çip 404 verdi → hatalar/veri_cikmis.md
- **H95** · Yayın düzeltmesinde olmayan alan; PDF eşleyici durdurulan işçi kapsayıcısında → hatalar/dagitim_sunucu.md
- **H96** · Önem/çözücü zinciri ham belgede olmayan soruyu "çıkmış" diye kullandı → hatalar/veri_cikmis.md
- **H89** · Canlı yarışma odası sorusuz kuruluyor, oyun hiç başlamıyordu → hatalar/ogren_modul_oyun.md
- **H90** · v15'te Toplu PDF penceresinin üstüne üst/alt çubuk biniyordu → hatalar/on_yuz_tasarim_tema.md
- **H97** · Dağıtım, yeni sesli ders metnini git'teki eski sürümle geri aldı; ses eski … → hatalar/dagitim_sunucu.md
- **H98** · Çizim panelleri dar ekranda taşıyor/sözcük kırıyor → hatalar/cizim.md
- **H99** · v15'te yeni ve bazı eski sayfalara menüden ulaşılamıyordu → hatalar/on_yuz_tasarim_tema.md
- **H99** · Dağıtım sunucu servis değişikliğini "yalnız ön yüz" sandı; yeni data dosyası Oracle'a … → hatalar/dagitim_sunucu.md
- **H100** · Asklepios kutlama efekti görünmüyordu → hatalar/on_yuz_tasarim_tema.md
- **—** · Tasarımdaki animasyon/3B ögesini "yok" diye atlamak → hatalar/on_yuz_tasarim_tema.md
- **—** · v15 tam ekranda yan menü içeriğin üstüne biniyor → hatalar/on_yuz_tasarim_tema.md
- **H100** · Koyu temada "beyaz" yazılar kayboluyordu; spinner/iskelet renkleri temaya uymuyordu → hatalar/on_yuz_tasarim_tema.md
- **—** · Sesli ders: çizimsiz resimde zoom takılı kalması → hatalar/cizim.md
- **H101** · Kronometre sayfa değişince kayboluyor, iki sayaç aynı anda açılıyor → hatalar/on_yuz_sayfa_denetimi.md
- **H102** · Sınav planı Kurul 2'de yanlış puan/plan veriyor → hatalar/on_yuz_sayfa_denetimi.md
- **H103** · Çıkmış adayı farklı dönem/ders sınavından geliyor; ham anahtar bankadaki cevapla çelişiyor; bankada … → hatalar/veri_cikmis.md
- **H102** · Tasarımdaki kayıt adımları (üniversite, sınıf, kurul, hedef) koda geçirilmemişti → hatalar/on_yuz_sayfa_denetimi.md
- **H104** · Hoca ses kaydı: tek model dökümü sınav vurgularını bozuyordu; kayıt dersin ortasından … → hatalar/ses.md
- **H105** · Harita `adimlar` = deste `slideNumber` (checkpoint dahil); iskelet ajanı içerik adımlarını 1..N … → hatalar/ders_metni_degerlendirme.md
- **H106** · `baglam.kazanimlar` kapak metninden türetilmiş çöp şablon cümleler içeriyor → hatalar/ders_metni_degerlendirme.md
- **H107** · Çıkmış eşlemesi: banka yıl etiketi ham belgeyle çelişiyor, yeniden yazılmış kökler, basılı … → hatalar/veri_cikmis.md
- **H108** · Kısaltma kapısı slayttaki gen sembollerini ve slayt yazım hatalarını (LMXIB, WTI) Faz … → hatalar/ders_metni_terim_kisaltma.md
- **H109** · v2 cümlesinin `ses` alanında iç cümle sonu: sunucu cümle sayısı v2 ile … → hatalar/ses.md
- **H110** · Kısaltma kapısı `kisaltma_elle`deki OD/OR/ID/SED'i "kısaltma biçiminde değil" diye reddetti → hatalar/ders_metni_terim_kisaltma.md
- **H111** · Alt ajan çapası: görüntüyü açmadan betikle eşleme, indeks kayması; kapı yalnız sınır … → hatalar/cizim.md
- **H112** · İlk anlatım taslağı öğrenci denetçide KALDI: aynı sözcük iki anlamda, kilit kavram … → hatalar/ders_metni_anlatim.md
- **H116** · Birleştiriciler yeni ders eklerken branştaki eski dersin dosyalarını da yeniden yazıyor → hatalar/dagitim_sunucu.md
- **—** · Sesli derste geri oku "Ders çalış"a atıyordu → hatalar/on_yuz_oynatici_ders.md
- **—** · Sesli derste canlı konum bazen çalışmıyor / bozuk çalışıyordu → hatalar/on_yuz_oynatici_ders.md
- **H113** · KMB video oynatıcısı takılıyor, yazılar üst üste biniyor → hatalar/ogren_modul_oyun.md
- **H114** · Çizim ileri-sızıntı denetimi yalnız ses metnine bakıyordu: gen sembolleri (HOX, PAX6, FGFR3) … → hatalar/cizim.md
- **H115** · Elle çizimde koordinat tahmini kenar kapısından geçmiyor; `cizim_kapisi` K3 elle çapada boş … → hatalar/cizim.md
- **H117** · Tam ekranda ayar düğmesi araç şeridini göstermiyordu → hatalar/on_yuz_oynatici_ders.md
- **H104** · Soru çöz sayfasında Araçlar görünmüyordu → hatalar/on_yuz_sayfa_denetimi.md
- **H105** · Sıralı tabloda adım atlanıyordu → hatalar/ders_metni_degerlendirme.md
- **H118** · Anlamsız karşılaştırma tabloları (Öge / Sınıf / Gerekçe) → hatalar/ders_metni_degerlendirme.md
- **H119** · Örnek sorularda öznel/ders çağrıştıran kök ve rastgele slayt sorusu → hatalar/soru_cozucu.md
- **H106** · Çalışma takvimi (ısı haritası) hücreleri dev görünüyordu → hatalar/on_yuz_sayfa_denetimi.md
- **H107** · "Günlük çözülen soru" çubukları çok genişti; ajan sınama verisi tarayıcıda kalmıştı → hatalar/on_yuz_sayfa_denetimi.md
- **H120** · Dallanmalı soruda doğru/yanlış bayrağı ters işaretliydi → hatalar/soru_cozucu.md
- **H121** · Sınama (test) Öğren dersi gerçek Kurul 2 dersleriyle aynı listede görünüyordu → hatalar/ogren_modul_oyun.md
- **H108** · Tablo rozetleri harf harf dikey; Ders seçenekleri kartları uzayıp taşıyordu → hatalar/on_yuz_sayfa_denetimi.md
- **H109** · Ders içerik kayıtlarında "Slayt s.N" kaynağı eksik → hatalar/ders_metni_degerlendirme.md
- **H122** · Paylaşılan çıkmış soruda süzgeç/kategori alanları öne çıkıyordu → hatalar/on_yuz_sayfa_denetimi.md
- **H109** · Aynı cihazda iki sekme açıkken profil eşitleme fırtınası → hatalar/on_yuz_sayfa_denetimi.md
- **H123** · Tam içerik hattı ders başına 4–6 saat sürüyor, soru/metin/PDF hataları geri dönüş … → hatalar/betik_altyapi.md
- **H124** · Soru çözücüde Kurul 2 seçili görünürken Kurul 1 dersleri listeleniyordu → hatalar/on_yuz_sayfa_denetimi.md
- **H125** · Ders içerik terimlerinde genel sözlükten bağlam dışı tanım, kopya terim, ipuçlu soru … → hatalar/ders_metni_terim_kisaltma.md
- **H126** · Sesli ders ekranında gen sembolleri okunuşla görünüyordu: "hoks, o te iks, me … → hatalar/ses.md
- **H110** · Çıkmış sorular yıl çipi 21, listede 20 soru → hatalar/on_yuz_sayfa_denetimi.md
- **H127** · Yıldızlı paragraflar: Bugün'de yok, silinen geri geliyor, sesli derste tüm dersler listeleniyor → hatalar/on_yuz_sayfa_denetimi.md
- **H128** · EMA yabancı terimleri yanlış okuyor; anlatım konu geçişini söylemiyor; panel geç, zoom … → hatalar/ses.md
- **H111c** · Esc uygulama tam ekranından çıkarmıyordu → hatalar/on_yuz_tasarim_tema.md
- **H111d** · Yönetim betik kataloğu her açılışta ana pakete iniyordu → hatalar/yonetim_basarim.md
- **H111e** · Profil verisi dinleyicileri render sırasında setState yapıyordu → hatalar/yonetim_basarim.md
- **H111f** · Deste kataloğu (~600 KB) her sayfada yalnız sayı için iniyordu → hatalar/yonetim_basarim.md
- **H111g** · İzleme hızı kaydırıcısı: dokunma hedefleri 10–19 px, boş durumda imleç metinle çelişiyordu → hatalar/on_yuz_oynatici_ders.md
- **H111h** · PC'de açıklama metinleri 120–160 karakter satır uzunluğunda → hatalar/on_yuz_tasarim_tema.md
- **H111p** · Sesli derste hatalı adreste sunucu hata kodu ham gösteriliyordu → hatalar/on_yuz_oynatici_ders.md
- **H111q** · Sesli ders telefonda: başlık 75 px'e sıkışıyor, Kalem düğmesi eziliyor, bölme hızlı … → hatalar/on_yuz_oynatici_ders.md
- **H111r** · Soru haritası hücrelerinde yazı kontrastı 2.6–4.0 → hatalar/on_yuz_sayfa_denetimi.md
- **H111s** · Zihin haritası numaraları koyu temada okunmuyordu → hatalar/on_yuz_tasarim_tema.md
- **H111t** · Ders çalış dokunma hedefleri: "Tüm dersler" 75×14, Öğren "▶ Dinle" 52×20 px → hatalar/on_yuz_sayfa_denetimi.md
- **H111u** · Çıkmış sorular kart görünümü sınırsız büyüyor, Odak ızgarası 4.372 düğme çiziyordu → hatalar/yonetim_basarim.md
- **H111v** · Ana CSS 936 KB, tam katman sayaçsız, tam ekranda fazla yükseklik, kısa … → hatalar/yonetim_basarim.md
- **H127** · Slayttaki şekil/deney anlatılmadı, "ders yorumuna girmez" diye geçildi → hatalar/ders_metni_anlatim.md
- **H129** · "Salt okunur" SQL konsolu süper kullanıcıyla çalışıyordu → hatalar/dagitim_sunucu.md
- **H130** · Canlı içerik katmanı tam kopyaydı, kaynaktaki yeni kayıtları gölgeliyordu → hatalar/dagitim_sunucu.md
- **H131** · Yönetim öğrenci uygulamasının ortak girişiyle açılıyordu; ayrı giriş + SW önbellek zehirlenmesi … → hatalar/yonetim_basarim.md
- **H131a** · `/react-dom/` eşleşmesi react-dom/server'ı her sayfanın açılış parçasına sokuyordu → hatalar/yonetim_basarim.md
- **H131b** · Kişiler listesi arka tazelemesi 2,5 sn olay döngüsünü kilitliyordu → hatalar/yonetim_basarim.md
- **H131c** · v16 kabuğu her alt yol değişiminde sayfayı yeniden kuruyordu → hatalar/on_yuz_tasarim_tema.md
- **H131d** · Dar ekranda süzgeç çipleri tabloyu ekran dışına itiyordu; kesik süre hücreleri → hatalar/on_yuz_sayfa_denetimi.md
- **H131** · Kurul 2 çıkmışlarında başka kurul soruları ve yanlış konu etiketleri → hatalar/veri_cikmis.md
- **H132** · Karantina listesi eskimişti; OCR ikizleri ve parça kayıtlar karantinada duruyordu → hatalar/veri_cikmis.md
- **H133** · Kaynağı doğrulanamayan sorular gizlenerek kaybedilmişti; "Çıkmış–Örnek" sınıfı → hatalar/veri_cikmis.md
- **H138** · Sekmede açılan görsel/JSON yanıtı site kabuğu diye önbelleğe yazılıyordu → hatalar/dagitim_sunucu.md
- **H139** · Gizlenen sayfaya giden bağlantı öğrenciyi açıklamasız Bugün'e atıyordu → hatalar/on_yuz_sayfa_denetimi.md
- **H140** · Bazı sayfalar aktif kurul yerine Kurul 1 ya da "Tümü" ile açılıyordu → hatalar/on_yuz_sayfa_denetimi.md
- **H141** · Yönetimde görünürlük tek tıkla, onaysız ve geri alınamaz yazıyordu → hatalar/yonetim_basarim.md
- **H142** · Mesaj/şikâyet yazarından kişiye geçilemiyordu → hatalar/yonetim_basarim.md
- **H143** · Yönetim tablolarında uzun içerikli satırın sütunları kayıyordu → hatalar/yonetim_basarim.md
- **H144** · Deneme ekranında soru numarası çubuğuna dokunulamıyordu; telefonda süre gizliydi → hatalar/on_yuz_sayfa_denetimi.md
- **H145** · Örnek sorularda "Başla" düğmesi harf harf dikey yazılıyordu → hatalar/on_yuz_sayfa_denetimi.md
- **H146** · Yönetim tabloları telefonda okunmuyordu → hatalar/yonetim_basarim.md
- **H147** · Öğrenci menüsünde hesap ve ders sayfaları yanlış gruplardaydı → hatalar/on_yuz_sayfa_denetimi.md
- **H148** · Ders çalış merkezinde "hepsini bitirdin ya da henüz ders yok" ikili mesajı → hatalar/on_yuz_sayfa_denetimi.md
- **H149** · Aramada "Sesli derste geçen yerler" stilsiz görünüyordu → hatalar/on_yuz_sayfa_denetimi.md
- **H150** · Güncelleme günlüğünde öğrenciye dosya yolları görünüyordu → hatalar/on_yuz_sayfa_denetimi.md
- **H151** · Sağlık Bakanlığı uzun bölümlerinde başa dönüş yoktu; geçmiş düğmesi küçüktü → hatalar/on_yuz_sayfa_denetimi.md
- **H152** · Yönetimde ders ayrıntısından o dersin sorularına geçiş yoktu → hatalar/yonetim_basarim.md
- **H153** · Yönetimde Yerel kipte hangi veriye bakıldığı belli değildi; birleştirmede asıl soru görünmüyordu → hatalar/yonetim_basarim.md
- **H154–H169** · Sayfa denetimi dördüncü tur, öğrenci sitesi orta bulguları → hatalar/on_yuz_sayfa_denetimi.md
- **H170–H185** · Sayfa denetimi dördüncü tur, yönetim paneli orta bulguları → hatalar/yonetim_basarim.md
- **H200–H212** · Sayfa denetimi beşinci tur, öğrenci sitesi kalan bulgular → hatalar/on_yuz_sayfa_denetimi.md
- **H250–H268** · Sayfa denetimi beşinci tur, yönetim paneli kalan bulgular → hatalar/yonetim_basarim.md
- **H220** · Üç sayfa aynı "bugün ne yapayım" işini bölüyordu → hatalar/on_yuz_sayfa_denetimi.md
- **H239–H241** · Ders programı: import.meta.glob anahtarı + numara eşleşmesi → hatalar/on_yuz_sayfa_denetimi.md
- **H242** · Çıkmış listesinde konum yoktu; geri dönünce liste baştan açılıyordu → hatalar/on_yuz_sayfa_denetimi.md
- **H290–H295** · Yönetimde iş akışı uzundu: Gelen yalnız yönlendiriyordu, toplu işlem yoktu → hatalar/yonetim_basarim.md
- **H296** · Gelen'de tek satır işlemleri onaysız ve geri alınamazdı → hatalar/yonetim_basarim.md
- **H300–H311** · Çevrimdışı ve Arka plan işleri aynı işi iki sayfada yapıyordu → hatalar/on_yuz_sayfa_denetimi.md
- **H310–H314** · 69 sayfalık menüde bulunabilirlik → hatalar/yonetim_basarim.md
- **H320–H329** · Görünürlük beş ayrı yerden düzenleniyordu → hatalar/yonetim_basarim.md
- **H330–H334** · Sesli ders araç çubukları kalabalıktı → hatalar/on_yuz_oynatici_ders.md
- **H335–H337** · TV kipinde ⋯ menüsü ve ders ekranında TV kumandası → hatalar/on_yuz_oynatici_ders.md
- **H340–H347, H360–H374** · Sayfa denetimi düşük önemli bulgular → hatalar/on_yuz_sayfa_denetimi.md
- **H388/H389** · Sınıf adı çakışması: Ders çalış çip şeridi ortaya/sağa kayıyordu → hatalar/on_yuz_tasarim_tema.md
- **H380–H387** · Kalan küçük öğrenci bulguları → hatalar/on_yuz_sayfa_denetimi.md
- **H390–H392** · Veri tutarlılığı: yıldız işaretleri, soru haritası sayımı, deste kurul adları, yinelenen kazanım … → hatalar/veri_cikmis.md
- **H393** · Canlı çıkmışlarda kazanım birleştirmesinden kalan eski konu adları / kimlikler → hatalar/veri_cikmis.md
- **H400–H406, H420–H424** · Yapı sadeleştirme: yinelenen sayfa ve girişler → hatalar/on_yuz_sayfa_denetimi.md
- **H430** · Video oluştur penceresi Ders seçenekleri panelinin altında kalıyordu → hatalar/on_yuz_disa_aktarim.md
- **H431** · Kişi 360° › Etkinlik sekmesi hep "Olay yok" gösteriyordu → hatalar/yonetim_basarim.md
- **H431** · Odak ekranlarında durum çubuğu ve ana ekran çizgisi payı yoktu → hatalar/on_yuz_tasarim_tema.md
- **H432** · Ders PDF ekranı kaydırırken "parçalanıp geri geliyordu" → hatalar/on_yuz_oynatici_ders.md
- **H433** · iPhone: panel başlıkları ve durum çubuğu çakışması → hatalar/on_yuz_tasarim_tema.md
- **H434** · Sesli derste "bu hastalıkta" gibi adsız göndermeler hangi hastalığın kastedildiğini karıştırıyordu → hatalar/ders_metni_anlatim.md
- **H435** · Örnek sorular hocanın yeni sınav kalıbını yansıtmıyordu → hatalar/soru_cozucu.md
- **H435** · Sıralama: ölçü değişince eski veri yanlış birimle görünüyor, tepki geç → hatalar/on_yuz_sayfa_denetimi.md
- **H436** · Ara soru şık açıklamalarında ileriye sızıntı ve kaynakta olmayan iddia → hatalar/soru_cozucu.md
- **H436** · Hata defteri tekrar ekranı yan rayın altında → hatalar/on_yuz_sayfa_denetimi.md
- **H437** · Çevrimdışı indirme "sırada" takılıyor, her açılışta uygulama dosyası iniyor → hatalar/dagitim_sunucu.md
- **H438** · Anlatım slaytın söylediğini tersine çevirdi → hatalar/ders_metni_anlatim.md
- **H439** · Üst çubuk arka plan göstergesi stilsiz çiziliyordu → hatalar/on_yuz_tasarim_tema.md
- **H440** · Arka plan işleri boşta da bellek, CPU, internet ve LLM kotası harcıyordu → hatalar/betik_altyapi.md
- **H441** · Sesli ders listesi (`/api/canli-ders`) canlıda her açılışta 1,2 sn → hatalar/dagitim_sunucu.md
- **H442** · Yeni sayfanın CSS öneki başka bileşenle çakıştı; sekmeler dev daire, düzen tek … → hatalar/on_yuz_disa_aktarim.md
- **H443** · Önizleme iframe'i genel `max-width: 100%` kuralıyla daraldı, sayfanın sağı kesildi → hatalar/on_yuz_disa_aktarim.md
- **H444** · DOCX ızgara sayfaları LibreOffice/Word'de ikiye bölündü; 26 sayfa 52 oldu → hatalar/on_yuz_disa_aktarim.md
- **H445** · Veride boolean `false` metin olarak "false" yazdı → hatalar/on_yuz_disa_aktarim.md
- **H446** · Öğrencinin en çok çalıştığı ve çıkmışta sorulan bilgi anlatımda "ders yalnız adıyla … → hatalar/ders_metni_anlatim.md
- **H447** · Metni değişen paragrafların v2 cümleleri boş kaldı, ders ekranı ve çapası o … → hatalar/ses.md
- **H448** · `klip_tasi.py` metinle birlikte düzenlenmiş v2'yi eski metne göre yeniden kurup değişen paragrafları … → hatalar/ses.md
- **H449** · Ders/ses sürümleri (V1/V2/V3) sitede görünmüyordu; Nörolojik Muayene V2'ye branş listesinden ulaşılamıyordu → hatalar/on_yuz_oynatici_ders.md
- **H450** · Çıkmış kayıtlarında uydurma ya da sınavdan sapmış şık/kök → hatalar/veri_cikmis.md
- **H451** · Aynı sınavın derleme kopyaları ayrı görünen sorular olarak kalmış, bazılarının cevabı yanlış → hatalar/veri_cikmis.md
- **H452** · Sınav yılı/kurul etiketi belge kanıtı olmadan tahmin edilmişti → hatalar/veri_cikmis.md
- **H453** · Çıkmış PDF ayıklama tuzakları → hatalar/veri_cikmis.md
- **H454** · Aynı soru iki yılın hatırlamasında farklı ifadeyle geçince bağlanmadı; aynı sınavın iki … → hatalar/veri_cikmis.md
- **H455** · Çıkmış kayıtlarında sınav yılı çok yıllı aralık ("2021-2026") ya da yılsız etiket … → hatalar/veri_cikmis.md
- **H456** · Izgara düzeninde her alt grup değişiminde sayfa kırılıyor, sayfada tek soru kalıyordu; … → hatalar/on_yuz_disa_aktarim.md
- **H457** · Sesli ders "İndir" düğmesi indirmeyi hiç başlatmıyordu → hatalar/dagitim_sunucu.md
- **H458** · sunucunun reddettiği (4xx) ya da 8 denemede gidemeyen yorum/beğeni/bildirim, kısa bir "kuyruktan … → hatalar/on_yuz_sayfa_denetimi.md
- **H459** · KMB (Üretral kateter): küçük video, tekrar eden altyazı, iptal edilemeyen otomatik geçiş, … → hatalar/ogren_modul_oyun.md
- **H460** · KMB Lottie videoları: kesik/taşan etiketler, kayan kamera, yanlış durumdan başlayan sahneler, sonsuz … → hatalar/ogren_modul_oyun.md
- **H461** · KMB video oynatıcı: tek dokunuş oynatmayı durduruyor ya da 10 sn sarıyordu … → hatalar/ogren_modul_oyun.md
- **H462** · KMB Hedefler filmi: yakınlaştırma ayrıntıyı kesiyordu; 3B deneme (Pixar/organik) kalite eşiğini geçemedi … → hatalar/ogren_modul_oyun.md
- **H465** · KMB 2B Erkek sahnesi: sırtüstü gövdede iç organlar "ayakta" dizilimindeydi (mantık hatası) → hatalar/ogren_modul_oyun.md
- **H466** · Google/Firebase projesi askıya alındı: kimse giriş yapamadı, site fiilen kapandı → hatalar/dagitim_sunucu.md
- **H467** · Taşınan hesaplar için e-postaya bağlı şifre belirleme tek yoldu; Drive'da ölü servis … → hatalar/dagitim_sunucu.md
- **H468** · Hoca dökümü sessizce CPU'ya düştü; turbo dökümü konuşmanın üçte birini kaçırdı → hatalar/ses.md
- **H469** · Kurul 2 EMA yolu büyük harfli kısaltmayı okumuyordu (NMDA, GABA, IP3) → hatalar/ses.md
- **H470** · Çizim kapısı R0 resim etiketini reddediyordu → hatalar/cizim.md
- **H471** · Yeni Kurul 2 derslerinde PDF açılmadı, PDF işareti atlandı → hatalar/dagitim_sunucu.md
- **H472** · Hoca vurgusu `konu` alanı özetti, değerlendirme kapısı slayttan birebir istiyor → hatalar/ders_metni_degerlendirme.md
- **H473** · Ders notu sadakati eşiğin altında: "Ek bilgi" etiketleri ve meta cümleler → hatalar/ders_metni_anlatim.md
- **H474** · Bu yılın PDF'inden üretilen Farmakoloji dersi öğrenciye görünmedi → hatalar/dagitim_sunucu.md
- **H475** · Yeni sürüm penceresi kartsız (düz madde) göründü → hatalar/on_yuz_tasarim_tema.md
- **H476** · Ders analizi özeti "çözücü yok" diyerek düştü (setlere bölünmüş çözücü) → hatalar/ders_metni_degerlendirme.md
- **H477** · Asıl hoca derse girmediğinde sınav kaynağı → hatalar/ders_metni_anlatim.md
- **H478** · LLM kilidi masaüstü Claude oturumunu zamanlayıcı sandı → hatalar/betik_altyapi.md
- **H479** · Yönetim › Quiz havuzu Oracle'da boştu (Docker'da rootDir/.. yanlış kök) → hatalar/dagitim_sunucu.md
- **H480** · Canlı damgası yeni commit'i gösterirken sunucu kodu eski kaldı → hatalar/dagitim_sunucu.md
- **H481** · çevrimdışına indirilen ders PDF'leri internetsiz açılmıyor; → hatalar/dagitim_sunucu.md
- **H482** · Kurul 2 toplu indirmeden sonra internetsiz sesli derste PDF görünmüyor, slayt/çizim takibi … → hatalar/dagitim_sunucu.md
- **H483** · H481/H482 öncesinde indirilmiş derslerde PDF ya da eşleme eksik kalmış olabilir; → hatalar/dagitim_sunucu.md
- **H484** · üç ders paralel hazırlanırken `hazirlik.py` sayfa metni / görüntü / öğrenci notu … → hatalar/betik_altyapi.md
- **H485** · destesiz taslakta `denetle.py` sayfa haritası denetiminde çöktü; → hatalar/ders_metni_degerlendirme.md
- **H486** · k2-07 (genel anestezik) anlatımı ve örnek soruları bağımsız denetimde KALIR: remifentanil "plazma … → hatalar/ders_metni_anlatim.md
- **H491** · "Hedef tamamlandı" başarım penceresi yatay telefonda / yarım ekranda (yükseklik ≤420) madalyası … → hatalar/on_yuz_oynatici_ders.md
- **H492** · asistan düğmesi çekmece/diyalog/aramanın üstünde; → hatalar/on_yuz_oynatici_ders.md
- **H493** · Soru çöz özet kartlarında yatay telefonda ve yarım ekranda açıklama "He…", "Yanlı…", … → hatalar/on_yuz_oynatici_ders.md
- **H487** · `kisaltma_sozlugu.py sozluk_disa` elle eklenmiş kısaltmaları siliyor → hatalar/ders_metni_terim_kisaltma.md
- **H488** · Slayt fotoğrafı ters yorumlandı: hipotonik bebek "tonus artışı" diye anlatıldı → hatalar/ders_metni_anlatim.md
- **H489** · `cizim_uret.py` oturum içinde LLM kilidine takılıyor → hatalar/betik_altyapi.md
- **H494** · bir pencere kapandıktan sonra sayfa kaydırılamaz kalabiliyor ya da diyalog açıkken arka … → hatalar/on_yuz_oynatici_ders.md
- **H495** · 640–767 px'te (büyük telefon yatay, yarım ekran) alt sekme çubuğu görünürken çekmece … → hatalar/on_yuz_oynatici_ders.md
- **H496** · sözlükte "Hastalıklar'a git" bağlantısı telefonda 17 px yükseklikte, dokunması zor. → hatalar/on_yuz_oynatici_ders.md
- **H490** · Öğrenci önem kapısı geçilemez yanlış HATA veriyordu → hatalar/soru_cozucu.md
- **H491** · Ara soru kodu başka dersin numarasını aldı → hatalar/on_yuz_oynatici_ders.md
- **H492** · Hoca vurgu alıntısı bozuk CPU dökümünden kuruldu → hatalar/on_yuz_oynatici_ders.md
- **H493** · Saat kilidi kalktı, hoca dökümü sessizce CPU'da yapıldı → hatalar/on_yuz_oynatici_ders.md
- **H494** · Boş çapa satırı ("‖") çapasız cümleyi çapalı gösterdi → hatalar/on_yuz_oynatici_ders.md
- **H495** · Ok glifi (↓ ⟸ ←) ve "Gpi/ SNr" boşluğu kanıt eşleşmesini bozdu → hatalar/on_yuz_oynatici_ders.md
- **H496** · Kısa şık açıklaması betikle kalıp ekle uzatıldı → hatalar/on_yuz_oynatici_ders.md
- **H497** · KMB Lottie: çarpı "Z" çiziyordu; çok alt yollu SVG tek şekle birleşiyordu → hatalar/ogren_modul_oyun.md
- **H498** · KMB: ata grupta transform olan sahnede kutular (bbox) 60 px kaydı → hatalar/ogren_modul_oyun.md
- **H499** · KMB: clipPath'li sıvı Lottie'de dikdörtgen olarak organ dışına taştı → hatalar/ogren_modul_oyun.md
- **H500** · KMB: altyazı bandı (alt %24) kesitteki ana yapıları örtüyordu → hatalar/ogren_modul_oyun.md
- **H501** · Hoca dökümü sarmalayıcısı model seçimini yutuyordu; turbo dökümüyle hocanın sözü yanlış okundu → hatalar/ses.md
- **H502** · iPad pencere kipinde sistem düğmeleri geri tuşunu kapatıyordu; kullanıcı geri çıkamıyordu → hatalar/on_yuz_tasarim_tema.md
- **H503** · "Güncelle"ye basınca eski sürüm açılıyor, sürekli güncelleme varmış gibi görünüyordu → hatalar/dagitim_sunucu.md
- **H504** · Ayarlarda "Küçük sürprizler" satırı görünmüyordu → hatalar/on_yuz_tasarim_tema.md
- **H505** · Polinöropati ve Bazal Ganglionlar sesli derslerinde PDF açılmıyor, yalnız "Drive'da aç" çıkıyordu → hatalar/dagitim_sunucu.md
- **H506** · Ara resimler kısa kelime öbekli kutu şemasıydı, öğretmiyordu → hatalar/cizim.md
- **H507** · iPad'de sesli dersten geri çıkılamıyordu; "başlığa bas = geri" çalışmıyordu → hatalar/on_yuz_oynatici_ders.md
- **H508** · Drive'daki ses dosyasının adı başka dersi gösteriyordu: "TSSB Psikaytr 2" aslında EKT … → hatalar/ses.md
- **H509** · Destesiz derste ders içerik paketinin kısaltmaları "Ek"e düşüyordu (adim 0), kapı %5 … → hatalar/ders_metni_terim_kisaltma.md
- **H510** · Değerlendirme kapısı kaynakça sayfasındaki yazar baş harflerini "sözlükte yok kısaltma" sayıyordu → hatalar/ders_metni_terim_kisaltma.md
- **H511** · Şık açıklamalarına betikle yeni geçiştirme kalıpları eklendi, kapı yakalamadı → hatalar/soru_cozucu.md
- **H512** · Anlatım parçalara bölünerek yazdırılınca ara resim adımı düştü (k2-21) → hatalar/ders_metni_anlatim.md
- **H513** · dist/assets hiç budanmıyordu: cihazda 473 derleme (3 GB), Oracle'da 92 bin parça … → hatalar/dagitim_sunucu.md
- **H514** · Örnek sorular ders listesinde "Hoca üslubu · N yeni soru" rozeti öğretim … → hatalar/on_yuz_sayfa_denetimi.md
- **H516** · Dağıtım yeniden başlatması sırasında açılan sayfa açılış ekranında sessizce takılıyordu → hatalar/dagitim_sunucu.md
- **H517** · Üst bar başlığı bölünmüş ekranda ve yan ray açıkken kırpılıyordu ("Sesli dersler" … → hatalar/on_yuz_tasarim_tema.md
- **H518** · Ayarlar: gruplar karışık, alt sayfalar iki ayrı anahtar görünümü kullanıyor, geniş ekranda … → hatalar/on_yuz_tasarim_tema.md
- **H519** · Sesli ders › Oynatıcı çekmecesinde "Hız" başlığı ve hız hapları içeriden/ortadan başlıyordu → hatalar/on_yuz_oynatici_ders.md
- **H520** · Sesli ders listesinde süzgeç hapları sıralama düğmesinin altına giriyordu (telefonda "Arşiv" üstüne … → hatalar/on_yuz_oynatici_ders.md
- **H523** · Taş Masası: "Oyunu başlat / masa kur" bazen hiçbir şey yapmıyor, hata … → hatalar/ogren_modul_oyun.md
- **H524** · Taş Masası: Taş Domino masası açılır açılmaz "Cannot read properties of undefined … → hatalar/ogren_modul_oyun.md
- **H525** · Taş Masası: başlamış masaya gelen arkadaş geri çevriliyor, kopmalar görünmüyordu → hatalar/ogren_modul_oyun.md
- **H526** · Taş Masası: Remi/Kastet düzenlemede elden taslağa konan taş geri alınamıyordu → hatalar/ogren_modul_oyun.md
- **H527** · Taş Masası: dar ekranda eylem düğmeleri 3–4 satıra yığılıyor, durum yazısı "Sıra…" … → hatalar/ogren_modul_oyun.md
- **H528** · Taş Masası: lobide mod seçenekleri "NormalZorlu", "KlasikYığma7-0AtlamaHızlıÇek-çek" diye bitişik yazı olarak görünüyordu → hatalar/ogren_modul_oyun.md
- **H529** · Taş Masası: tüm oyunlarda hamleler gecikmeli görünüyordu → hatalar/ogren_modul_oyun.md
- **H530** · Kısık amfi kaydında hoca dökümü uydurma cümlelerle doluyordu → hatalar/ses.md
- **H531** · Hoca sesi sonradan gelen yayımlanmış derste anlatım baştan yazılmaz; kısmi revizyon ve … → hatalar/ders_metni_anlatim.md
- **H532** · CPU'lu `meds-ema` birimi açıkken ders EMA işi GPU yerine CPU'ya düşebiliyordu → hatalar/ses.md
- **H533** · Taş Masası: dar ıstakada grup toplamı yanlış; Go/XOX botu hiç hata yapmıyordu → hatalar/ogren_modul_oyun.md
- **H534** · Taş Masası: masadaki taş eldeki taşlarla yeni pere katılamıyordu → hatalar/ogren_modul_oyun.md
- **H535** · Taş Masası: masayı düzenlerken perler boşalan yere kayıyordu → hatalar/ogren_modul_oyun.md
- **H542** · Uno'ya 10 yeni mod eklenirken motor sınamasının yakaladığı dört kural hatası → hatalar/ogren_modul_oyun.md
- **H536** · Değerlendirme kapısı tasarım PDF'inin harf aralıklı başlıklarını ("Y A N I TL … → hatalar/ders_metni_terim_kisaltma.md
- **H537** · A1a/A2 "kanıt" alanları birden çok satırı birleştiren özetler olduğundan değerlendirme kapısından geçmiyordu → hatalar/ders_metni_degerlendirme.md
- **H538** · 5. parti derslerinin anahtarları `MODUL_ANAHTARLAR`'da yoktu: yazımla tutulan kısaltmalar (DSM, EEG, SSRI) … → hatalar/ses.md
- **H539** · EMA tam MP3 yüklemesi Oracle'daki başka bir dağıtımın sunucu yeniden başlatmasına denk … → hatalar/ses.md
- **H540** · `kelime_zaman.py --gpu` elle çağrıda `libcublas.so.12` bulamayıp sessizce CPU'ya düştü → hatalar/ses.md
- **H541** · Destesiz derslerin örnek soruları k2-12'den beri siteye yayınlanmıyordu → hatalar/soru_cozucu.md
- **H543** · İçi boş madde imi pymupdf metninde "o" harfi olarak geldi; değerlendirme kapısı … → hatalar/ders_metni_degerlendirme.md
- **H544** · Ek modül içeriği hocanın materyali sorulmadan yazıldı; çalışma soruları gelince 16 konunun … → hatalar/ogren_modul_oyun.md
- **H545** · `git add server.ts` başka oturumun commit'lenmemiş iki satırını da commit'e aldı; depoda … → hatalar/dagitim_sunucu.md
- **H546** · Ek modülde sesli ders PDF'le birlikte ilerlemiyordu; eşleme kurulurken iki ölçüm tuzağı → hatalar/ogren_modul_oyun.md
- **H547** · Gövdesi yalnız resim olan slayda dayanan doğrudan çıkmış, değerlendirme kapısından geçemiyordu → hatalar/veri_cikmis.md
- **H548** · Slayt altındaki kaynak satırının dergi adı "sözlükte olmayan kısaltma" sayıldı → hatalar/ders_metni_terim_kisaltma.md
- **H549** · Önem maddesinin alıntısı olarak slayttaki kaynak künyesi yazıldı → hatalar/soru_cozucu.md
- **H550** · Canlı çizimde kontur doğru, etiketi yanlış figüre düşüyor ya da slayt yazısını … → hatalar/cizim.md
- **H551** · Giriş yapmış öğrenci kendi profilini ve arkadaşlık isteklerini göremiyordu → hatalar/on_yuz_sayfa_denetimi.md
- **H552** · Sesli çalışma sorularında boşluk doldurma "boşluk" diye okunuyordu → hatalar/ogren_modul_oyun.md
- **H553** · Değerlendirme kapısı OCR'lı metinden alınan çok satırlı kanıtları PDF'te bulamadı → hatalar/ders_metni_degerlendirme.md
- **H554** · Ders içerik paketinde "bilgiler boş": bilgi havuzu `tur` alanı içerik tipiyle dolduruldu → hatalar/ders_metni_degerlendirme.md
- **H555** · Şık açıklamasında uzunluk dolgusu: aynı "ana bilgi" cümlesi birden çok şıka eklendi → hatalar/soru_cozucu.md
- **H556** · "PDF indir" herkese "X-API-Password başlığı gereklidir" diyordu; canlıda başsız tarayıcı da yoktu → hatalar/dagitim_sunucu.md
- **H557** · `claude` açılmıyordu (abonelik yok) + masaüstü uygulamasında model listesi boş → hatalar/betik_altyapi.md
- **H558** · Bash aracı hiç açılmıyordu: `apply-seccomp: write /proc/self/setgroups … Permission denied` → hatalar/betik_altyapi.md
- **H559** · İçerik katmanı toplu "silinen" yazdı: sözlükte 750 terim, Öğren'de 11 deste sunucuda … → hatalar/dagitim_sunucu.md
- **H560** · Ajan hattı OpenDesign geçidine taşınırken roller tek modelde birleşti, eşlenmemiş adlar sessizce … → hatalar/betik_altyapi.md
- **H561** · Artifact stüdyosu: önizleme sunucusu bulunamadı, grafikte iki farklı büyüklük tek eksende ezildi, … → hatalar/betik_altyapi.md
- **H562** · Canlıda yeni anahtar "yok" göründü: `env_file` yalnız konteyner oluşturulurken okunur, loopback da … → hatalar/dagitim_sunucu.md
- **H570** · Ders analizi betiği tam ders anahtarını "kayıt defterinde yok" sandı → hatalar/ders_metni_degerlendirme.md
- **H571** · Ders içerik paketinde kısaltmaların hepsi `adim: 0` kaldı: `sayfalar.json` yedeği hiç çalışmadı → hatalar/ders_metni_terim_kisaltma.md
- **H572** · Soru dışa aktarıcı çöküyordu ("sayfayı yenile"); PDF'te logo alt bilgiyle üst üste … → hatalar/on_yuz_disa_aktarim.md
- **H573** · "Sayfayı yenile" ekranı yenilemeyi öneriyor ama kurtarmıyordu: eski kabuk + eksik parça … → hatalar/on_yuz_disa_aktarim.md
- **H574** · Oyun masasında 13 kez çökme: `oyuncu.cezalar` olmayan eski oyun durumu → hatalar/ogren_modul_oyun.md
- **H575** · "PDF'te alt kısımda soru/şık metni kesik kalıyor" bildirimi H572 sonrası da geldi: … → hatalar/on_yuz_disa_aktarim.md
- **H576** · "PDF'te alt bilgi (sayfa numaralı satır) diğer metnin üstünü kapatıyor": sayfa kutusu … → hatalar/on_yuz_disa_aktarim.md
- **H572** · Etiketleri görselin içinde olan slayt şeması "resim" sayılmıyordu: lazer sayfaya düşüyor, üstüne … → hatalar/cizim.md
- **H577** · "Toplu yol süpürmesi bazı betikleri sessizce atladı": Türkçe yerel ayarda sed/grep `[a-z]` … → hatalar/betik_altyapi.md
- **H578** · Betik dizini taşırken sessiz kırılma sınıfları: yeniden yapılandırmada yakalanan 7 tuzak → hatalar/betik_altyapi.md
- **H579** · "Oracle'da kok'u import eden her betik çöküyor": kök markerı yalnız geliştirme makinesinde … → hatalar/dagitim_sunucu.md
- **H580** · "Otomatik onarım / NotebookLM ile düzelen deste dağıtımda geri dönüyor": katmanı atlayan yazıcılar → hatalar/dagitim_icerik_katmani.md
- **H581** · "Panelden/NotebookLM'den düzeltilen sözlük, kart, özet, örnek soru dağıtımda geri dönüyor": katmansız yazım + sezgisel D5 → hatalar/dagitim_icerik_katmani.md
- **H582** · "Ansiklopedi düzeltmesi Oracle'da dağıtımı durdurabilir / ekrana gelmez": slug çakışması + katman kaydı yok → hatalar/veri_cikmis.md
- **H583** · "`git add -A` gizli anahtarı ve 600 MB çalışma verisini herkese açık depoya gönderdi": eksik .gitignore + kör toplu ekleme → hatalar/dagitim_icerik_katmani.md
- **H584** · "patoloji_onem betikleri veriyi bulamıyor; arsiv_yayinla çıkmış konumunda `lib` bulunamayabilir": çift kopya kalıntısı yol + yan etkiye bağlı sys.path → hatalar/betik_altyapi.md
- **H585** · "Onarım/redaksiyon servisleri çıkmış soru dosyasını önbelleği atlayarak yazıyordu (yazma yarışı)": doğrudan dosya yazımı → tek erişim `cikmisErisim` → hatalar/dagitim_icerik_katmani.md
- **H586** · "Çözücü/asistan/Öğren seslerinde terim ve kısaltma okunuşu uygulanmıyor; 'engel' → 'Engıl'": okunuş 9 yerde + elle anahtar listesi → `ses_ortak/ses_metin` → hatalar/ses.md
- **H587** · "16 Öğren klibi 14–22 dk sürüyor; bozuk ses yayına çıkabiliyor": ses kalite kapısı yoktu → `ses_ortak/ses_kapisi.py` → hatalar/ses.md
- **H588** · "Dağıtımdan sonra tembel ekran 'e._result.default' / React #306 ile çöküyor": preloadError preventDefault → import boş çözülüyor → `guvenliLazy` → hatalar/on_yuz_sayfa_denetimi.md
- **H589** · "Arama ölçümü %95'ten %75'e düştü sanıldı": değerlendirme örneklemi dizinde olmayan gizli kopyaları içeriyordu → hatalar/veri_cikmis.md
- **H590** · "İndirilmemiş sesli ders bağlantı gelince 'Ağ bağlantısı yok' kartında kalıyor": yükleme etkisi yalnız ders kimliğine bağlı, yeniden deneme yok → yoklama + düğme → hatalar/on_yuz_sayfa_denetimi.md
- **H591** · "Yönetim girişinde 'Şifremi unuttum' stilsiz": `au-*` yalnız ana sitenin `rebuild.css`'inde → `giris-au.css` iki girişten → hatalar/on_yuz_sayfa_denetimi.md
- **H592** · "`.gitignore`'daki ses dizinlerinde 2.809 MP3 hâlâ izleniyor": kural sonradan eklendi, `git rm --cached` yapılmadı → hatalar/dagitim_icerik_katmani.md
- **H593** · "Yedek arşivi hep 0 iş; ses kapısı yol verilince yön göstermiyor; nereye var olmayan yolu önerebilir": saklama kuralı 2 sabit, ad-yalnız eşleme, süzgeçsiz öneri → hatalar/betik_altyapi.md
- **H594** · Aşama girdisi ders verisinden çok bütün okutulan standart belgeydi; denetçi yayın kurallarını okuyordu → hatalar/betik_altyapi.md
- **H585** · "Commit kancası başka oturumun yarım değişikliği yüzünden temiz commit'i durduruyor": kanca çalışma ağacını denetliyordu → hatalar/betik_altyapi.md
- **H598** · "Commit kancası D8, başka oturumun sahnelenmemiş belgeleri yüzünden haritayı bayat sayıyor": üreticiler çalışma ağacını okur → sahne kipinde UYARI → hatalar/betik_altyapi.md
- **H595** · "Öğren sesinde 32/35 adım reddedildi (süre oranı 0.48: 2.)": cumlelere_ayir sıra imini ("2.") tek cümle yapıyordu → hatalar/ses.md
- **H596** · "Kimliksiz istek 100 MB gövde gönderebiliyor; aynı uç iki kez tanımlı, ikincisi yetkisiz": gövde ayrıştırıcı kimlikten önce + mükerrer uç kapısı yok → kademeli tavan, `kos.py uc` → hatalar/dagitim_sunucu.md
- **H597** · "Kapı girdisi yoksa Traceback, ajan içerik hatası sanıyor": çıkış kodu ayrımı yok → `kos.py` girdi denetimi (2) + çökme ayrımı (70) → hatalar/betik_altyapi.md
- **H601** · "Ücretsiz bulut LLM çağrı noktası ve 11 betik kilitsiz (kural 20)": kilit yalnız Claude/ajan CLI yoluna eklenmişti → `cloud_llm` kilitliyken None, betikler çıkış 75, sunucu yönetici yolunda `LLM_PANEL_ENV` → hatalar/betik_altyapi.md
- **H603** · "Olmayan adres 200 dönüyor": SPA geri dönüşü koşulsuz 200 → sunucu ön yüz çözücüsüyle (`parseLocation`) 404 → hatalar/on_yuz_sayfa_denetimi.md
- **H602** · "Sesli ders telefon/tablet: oynatıcı düğmeleri 30–34 px, tablette başlık kesik, PDF parçası geç": minimal çubuk ölçüleri medya sorgusuz dokunmatiğe gidiyordu, PdfDocView veri gelince isteniyordu → hatalar/on_yuz_oynatici_ders.md
- **H604** · "Optimize ettik, build uzadı (77 sn, 30+ uyarı)": esbuild küçültücü + gzip raporu + karesel budama regex'i + önbelleksiz sürüm günlüğü → oxc, rapor kapalı, çapalı regex, HEAD önbelleği (≈38 sn, 0 uyarı) → hatalar/betik_altyapi.md
