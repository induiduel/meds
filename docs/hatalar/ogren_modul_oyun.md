# Hata defteri — ogren_modul_oyun (Öğren destesi, ek modüller, KMB filmleri, oyunlar)

> Tam metin (kelimesi kelimesine taşındı, 2026-11-16). Dizin: `docs/KURUL2_YAPILMAYACAK_HATALAR.md`.
> Yeni madde bu dosyanın SONUNA `## H<n> — …` başlığıyla eklenir + dizinin sonuna tek satır.

## H67 — H64 tekrarı: harita adımları checkpoint'siz sayıldı + deste `bolum` alt başlık numarası (2026-10-26, k2-26 nörolojik hastalıklar genetiği)
- **Belirti:** `denetle.py` 112 HATA: "pdfSayfalari [n] ama harita [m] diyor", başlık aralıkları içerik adımı değil, "bolum '1.1' basliklar'da yok", ana başlıklar 54/60 adımı kapsıyor.
- **Kök neden:** (1) `sayfa_haritasi.json` `adimlar` (sayfa ve başlık) içerik sırası (1..60) ile yazıldı, `slideNumber` (checkpoint dahil 1..68) ile değil — H64'ün aynısı. (2) 1. parçanın slaytlarına `basliklar`da olmayan alt numara (`1.1`–`1.8`) yazıldı. (3) Fakomatoz (s.61–71) ve işitme (s.90–102) sayfalarında harita bir adım kaymış; adım 1'e s.3 (içindekiler) dahil edilmiş.
- **Çözüm / kural:** Harita `adimlar` daima deste `slideNumber`'ıdır; `bolum` yalnız `basliklar[].no` değerlerinden biri olur (alt başlık yoksa ana no). Kayma görülürse hangi tarafın doğru olduğu sayfa `ne_anlatiliyor` ile slayt başlığı karşılaştırılarak seçilir; içindekiler/kapak sayfası hiçbir adımın `pdfSayfalari` aralığına girmez.

### H89 — Canlı yarışma odası sorusuz kuruluyor, oyun hiç başlamıyordu (2026-10-27)
- **Belirti:** `/api/quiz/ws` odasına katılan herkes "Hazırım" dese de oyun başlamıyordu.
- **Kök neden:** `handleJoinRoom` olmayan odayı `createOrJoinRoom(..., [])` ile **boş soru listesiyle** kuruyordu; `handleSetReady` `questions.length > 0` şartıyla geri sayımı hiç başlatmıyordu. Ayrıca yeniden bağlanan oyuncu yeni kayıtla puanını kaybediyor, istemci `disconnect()` sonrası `onclose` içinde kendiliğinden yeniden bağlanıyordu.
- **Çözüm:** oda yalnız `kaynak` (branş/ders/n) ile kurulur, sorular `oyunSoruKaynagi.ts`'ten; kaynaksız katılımda oda yoksa `room_error`. Yeniden bağlanan aynı kimlik puanını korur; istemci `disconnect` oda kimliğini siler.
- **Kural:** realtime odası veri olmadan kurulamaz; sunucu her başarısız katılımı açık hata mesajıyla döner.

## H113 · KMB video oynatıcısı takılıyor, yazılar üst üste biniyor (2026-10-27)
- **Belirti:** KMB adım/ders videoları cümle geçişlerinde takıla takıla ilerliyor, adımdan adıma geçişte duraksıyor; altyazı,
  denetim çubuğu, "Adım n" başlık kartı ve sahne etiketleri üst üste biniyor; mobilde denetimler iki satıra kırılıyor, ±10 sn yazıları
  görüntüyü sürekli kapatıyordu.
- **Kök neden:** (1) Adım videosu tek sürekli EMA klibine bağlı ama cümleler arasına görüntüde bekleme payı konmuş; oynatıcı her bekleme
  sonunda sesi duraklatıp `currentTime` ile ağdan (HTTP aralık isteği) yeniden konumluyordu → her cümlede tamponlama duraksaması.
  Ayrıca saat her karede ses saatine sert eşleniyordu (ses zamanı kaba güncellendiğinde görüntü ileri-geri zıplıyordu). (2) Ders videosunda
  adım geçişinde 0,9 sn bekleme + 1,8 sn başlık kartı + yeni sesin ilk kez inmesi. (3) `kmb.css` v1→v6 altı katman birbirini
  ezen kurallarla büyümüştü (altyazı bir katmanda akışta, ötekinde mutlak; denetim çubuğu tam ekranda yüzerken altyazı da aynı yere).
- **Kalıcı çözüm:** Klip bütünüyle blob olarak önceden indirilir (`sesOnYukle`, sonraki adımınki de); bekleme sonrası yakın konumdaysa ses
  konumlanmadan sürer, yalnız 0,6 sn üstü sapmada (bellekten, anında) konumlanır; küçük sapma yumuşak düzeltilir, ses tamponlanırken görüntü
  bekler. Başlık kartı kaldırıldı, geçiş 250 ms. `kmb.css` tek katman olarak yeniden yazıldı: normal kipte denetimler sahnenin ALTINDA tek
  satır, altyazı sahne içinde tek kutu; tam ekranda denetim yüzer, altyazı onun üstüne çıkar; aynı anda görünen etiketler birbirinden itilir.
- **Kural:** Sesle eşlenen animasyonda ses ağdan parça parça konumlanmaz (blob/önbellek); saat sert değil yumuşak eşlenir. Stil dosyasına
  "vN: önceki kuralları ez" katmanı eklenmez — kural yerinde değiştirilir; üst üste binen öge eklerken mutlak konumlu her katmanın yeri tek yerde tanımlanır.

## H121 · Sınama (test) Öğren dersi gerçek Kurul 2 dersleriyle aynı listede görünüyordu (2026-10-27, k2-07 Genel Anestezik İlaçlar)
- **Belirti:** Sınama olarak eklenen `k2p-k2-07-genel-anestezik-ilaclar` Öğren kitaplığında Tıbbi Farmakoloji grubunda gerçek derslerle karışık duruyordu (yalnız küçük "Sınama" rozeti vardı); gerçek ders işlenince karışma riski.
- **Kök neden:** `data/sinama.json` ayrımı yalnız Canlı ders servisinde (`canliDers.ts`) uygulanıyordu; Öğren kitaplığı (`LearnLibraryV12`) `deck.sinama` alanını yalnız rozet olarak gösterip dal (branş) ile grupluyordu.
- **Kalıcı çözüm:** kitaplıkta `sinama` işaretli desteler ayrı "Sınama — test verisi" bölümünde, en sonda gösterilir. Önleme: yeni listeleyen her ekran `sinama` alanını bölüm ayrımı için kullanır; gerçek PDF gelince `yayinla.py` aynı kimliği günceller ve `sinama` alanını bırakır (H97/H99 sırası).

## H459 — KMB (Üretral kateter): küçük video, tekrar eden altyazı, iptal edilemeyen otomatik geçiş, metin hataları, hata takibi yok (2026-10-31)

- **Belirti:** PC'de Öğren ekranı üç sütundu (adım listesi · video · metin), video ~430 px'e sıkışıyordu; etiketler
  ("Üretral kateter: meatustan mesaney…") kesik görünüyordu; v15'te becerinin adı hiçbir yerde görünmüyordu (h1 gizli,
  üst çubukta "KMB dersleri"); video bitince 1,2 sn'lik `setTimeout` sonraki adıma geçiyordu ve "Yeniden izle"ye basılsa
  bile geçiş iptal olmuyordu; mobilde videonun kenarına tek dokunuş 10 sn atlatıyordu; hız değişince görüntü zıplıyordu;
  altyazı/hız tercihi her videoda sıfırlanıyordu. Sınavda yanlışlar hiçbir yerde tutulmuyor, öğrenci hangi basamağı
  unuttuğunu göremiyordu. Hocanın kaydıyla çelişen cümleler vardı (ağrı "takıldıktan sonra" değil "çıkarıldıktan sonra";
  idrar miktarı "en önemli gösterge"; yatağa bağımlılık göreceli endikasyon; kadında 3–4 cm yeterli; doğum yapmış kadında
  vajinaya girmek "kolay ayrım" değil "hata ama sorun yaratmaz"; tek jel lidokainli; izotonik "yıkama" değil yer sınaması)
  ve kadın OSCE akışında "idrar gelince birkaç cm daha ilerlet" basamağı yoktu; 8 şık açıklaması kural 14 alt sınırının altındaydı.
- **Kök neden:** düzen sabit sütun genişlikleriyle (220/1fr/340) viewport'a göre kuruluyordu, kenar çubuğu açıkken içerik
  dar kalıyordu; otomatik geçiş oynatıcının dışında, iptal yolu olmayan zamanlayıcıydı; oynatıcı saati hız değişiminde
  yeniden tabanlanmıyordu; etiketler `white-space: nowrap; max-width: 46cqi` ile kesiliyordu. Ses dökümü cümleye
  çevrilirken hocanın vurgusu özetlenip yumuşatılmış, akış basamakları anlatım cümlelerinden ayrı yazıldığı için
  "birkaç cm daha ilerlet" yalnız açıklama içinde kalmıştı; KMB doğrulayıcısı şık açıklama kapısını çağırmıyordu.
- **Çözüm:** Öğren yeniden kuruldu (`KmbAsistan.tsx::Ogret`): üstte adım başlığı + önceki/sonraki + 18 parçalı adım şeridi
  (izlenen yeşil, sınavda eksik kırmızı), tüm adımlar açılır panelde; video + eşzamanlı metin `@container kmb` ile dar
  alanda alt alta, ≥860 px içerikte yan yana (video yapışkan); cümleye dokununca video o cümleden oynar
  (`LottieVideo` `ref.bolumeGit`). Oynatıcı: tek dokunuş oynat/duraklat, kenarda çift dokunuş ±10 sn, önceki/sonraki cümle
  düğmesi ve ↑/↓, hız değişiminde saat yeniden tabanlanır, altyazı/hız `medsoru_kmb_oynatici_v1`'de, bitişte geri sayımlı
  `otoSonraki` (Yeniden izle / Burada kal / konumlama iptal eder), etiketler iki satıra iner. Hata istatistiği
  `kmbHata.ts` + "Eksikler" sekmesi (`Eksikler.tsx`): her deneme kavram anahtarına (OSCE basamağı, vaka, yapı, hedef)
  yazılır, iki kez üst üste doğru yapılana dek zayıf sayılır; öğretim adımına göre gruplanır ("Adımı yeniden çalış"),
  hedefli tekrar (unutulan basamak için "bundan sonra ne yaparsın?", vaka, sahnede bul, hedefi anlat + öz değerlendirme).
  Sınav ögelerine `adim` alanı eklendi (dogrula.py denetler). `medsoru_kmb_*` hesapla eşitlenir (userKvSync).
  İçerik: kayda dayanan 11 cümle/açıklama düzeltmesi, kadın akışına `ilerlet2`, 11 şık açıklaması genişletildi.
- **Önleme:** KMB'de yeni ekran düzeni viewport değil `@container kmb` ile seçilir; otomatik geçiş yalnız oynatıcının
  iptal edilebilir `otoSonraki`'si ile yapılır. Hocanın sözü cümleye çevrilirken derecelendirme ("en önemli", "göreceli",
  "hata ama sorun değil") korunur; anlatımda vurgulanan her uygulama eylemi OSCE akışında ayrı basamaktır. Her yeni sınav
  ögesi `adim` taşır (yoksa dogrula.py HATA). Şık açıklamaları `sik_aciklama.denetle` ile 0 HATA.

## H460 — KMB Lottie videoları: kesik/taşan etiketler, kayan kamera, yanlış durumdan başlayan sahneler, sonsuz sayaç (2026-10-31)

- **Belirti:** 18 adım videosunun (89 cümle) kare denetiminde: 47 etiket telefonda "…" ile kesiliyor ("Üretral kateter:
  meatustan mesaney…"), ~100 etiket kadraj dışına ya da altyazı bölgesine (alt %24) düşüp oynatıcı tarafından sahnenin
  üstüne sıkıştırılıyordu; erkek temizlikte kadın/erkek karşılaştırma cümlesinde kamera cümle boyunca kendiliğinden
  kayıyordu; sistit cümlesinde ("mesanede yalnız 15–20 mL") mesane şişip küçülüyordu; travmada "yalnız kırık" cümlesinde
  darbe + kırık baştan oynuyordu; idrar gelmezse ve sabitlemede "40 mL / 10 mL" sayacı sonraki sahnelerde (form, hasta
  konuşması) ekranda kalıyordu; malzemede yardımcının steril olmayan eli steril alanın içindeydi; kadın vulva sahnelerinde
  uyluklar arası beyaz boşluk; alt raf, torba, meatustaki kan altyazının altında; erkek yerleştirmede anatomi etiketleri ve
  "Penis dik ve gergin" iki kez.
- **Kök neden:** (1) Etiketler sahne koordinatıyla elle yazılıyor, oynatıcının kameraya göre sıkıştırma/itme/kesme
  kuralı (LottieVideo.tsx Katman + kmb.css 46cqi) üretimde hiç hesaplanmıyordu; kapı yoktu. (2) `kamera_ekle` geçişin
  başlangıç anahtarını ekleme anındaki son anahtardan kopyalıyordu: araya sonradan eklenen hareket (zemin_kat sıfırlaması)
  sonraki geçişin başlangıcını güncellemiyordu. (3) `Ic` (alt kompozisyon) eşlenmeyen (None) bölümü video sonrasına
  atıyordu; önceki bölümün anahtarları geleceğe gidince Lottie anahtarları zamanca yeniden sıralanıyor, eşlenen bölüm
  yanlış durumdan başlıyordu. (4) Oynatıcı sayacı `t >= bas` ile videonun sonuna dek gösterir (bitişi yok).
- **Kalıcı çözüm:** `lottie_dsl.py`: kamera artık hareket listesi, `kamera_coz` zaman sırasıyla çözer;
  `etiket_yerlestir` her etiketi kamera geçişi bitince belirtir, ömrü boyunca (0,25 sn örnekle) kadrajda ve altyazının
  üstünde tutar, eşzamanlı etiketleri oynatıcının itme eşiğinin (%26/%8) dışına ayırır; `Ic` eşlenmeyen önceki bölümleri
  (ve `'once'`) görünmeden önceki sessiz paya sıkıştırır ("olmuş bitmiş"), sonrakileri atar; sahneye ait sayaç sahne
  kaybolunca biten adım etiketlerine çevrilir. 45 etiket ≤30 harfe kısaltıldı; sahne düzeltmeleri `adim_lottie.py` ve
  `lottie_uret.py`'de. Kapı: `dogrula.py` → `lottie_dsl.etiket_denetle` (≤30 harf, kadraj, altyazı bölgesi, çakışma) HATA.
- **Önleme:** Video değişikliğinden sonra `node meds/scripts/uretim/kmb/kare_onizle.mjs [ad…]` ile temas sayfası üretilir ve her
  cümle karesi metinle karşılaştırılır (rapor.json otomatik bulgu 0 olmalı). Etiket ≤30 harf; önemli öge (torba, meatus,
  kan) sahnenin alt %24'üne konmaz; alt kompozisyonda "son durum" gerekiyorsa `'once'` kullanılır, None değil.

- **Arayüz: dense ızgarada boşluk (2026-10-31, profil):** farklı yükseklikteki kartlar `grid-auto-flow: dense` ile iki sütuna dizilince uzun kartın yanında büyük boşluk kalır. Kolonları açık kur (`.apr15-ikili > .apr15-kol`), uzun listeyi kısa açıp "Tümünü göster" ekle; düzeni gerçek veri büyüklüğüyle (40+ öğe) sına.

## H461 — KMB video oynatıcı: tek dokunuş oynatmayı durduruyor ya da 10 sn sarıyordu (tam ekran dahil) (2026-10-31)

- **Belirti:** Videoya (tam ekran ders videosunda da) tek dokunuş ya duraklatıyor ya da kenarlarda 10 sn ileri/geri sarıyordu;
  öğrenci yalnız alttaki çubuğu gizlemek istediğinde bunu yapamıyordu. Sonraki sınamada iki ek kusur çıktı: (1) orta
  düğme sırasındaki ±10 düğmeleri kenar bölgelerine taşıyor, kenara tek dokunuş yine görünür bir sarma düğmesine denk
  geliyordu; (2) sağa seri sarmanın hemen ardından sola dokunmak tek başına geri sarıyordu. Ayrıca tam ekran açılamayınca
  (iOS) ders videosu katmanı alttan 24 px kısa kalıyor, altında sitenin menüsü görünüyordu; zaman çubuğunda sarmak
  otomatik geçişi kalıcı iptal ediyordu.
- **Kök neden:** sahnede üç görünmez düğme (sol %25 / orta / sağ %25) vardı ve her biri tek tıkta eylem yapıyordu; dokunma
  ile fare aynı kurala bağlıydı, dokunma sayısı ve hareket (basılı tutma, kaydırma) hiç ayırt edilmiyordu. Seri sarma
  penceresi tarafı denetlemiyordu. v11.css'teki genel `[role=dialog] { max-height: vvh − 24px }` tam ekran katmanını da kısaltıyordu.
- **Çözüm:** tek jest katmanı (`LottieVideo.tsx` `jestBas/jestKay/jestBit`, pointer olayları): DOKUNMATİK tek dokunuş
  yalnız denetimleri gösterir/gizler (280 ms çift dokunuş beklenir), kenarda çift dokunuş ±10 sn ve 700 ms içinde aynı
  kenara her dokunuş +10 (toplam rozetle), ortada çift dokunuş oynat/duraklat, basılı tutma 2×, yatay kaydırma sarar
  (hedef süre + cümle balonu; dikey kaydırma sayfaya kalır, `touch-action: pan-y`). FARE tık oynat/duraklat, çift tık
  tam ekran. Denetimler her kipte görüntünün üstünde yüzer, oynarken 3 sn sonra gizlenir (ince ilerleme çizgisi kalır);
  ders videosunun üst şeridi aynı duruma bağlı (`onGoster`). Orta sıra: önceki cümle · oynat · sonraki cümle (±10 yok).
  Cümle listesi menüsü, hız menüsü (0,75–2×), cümle parçalı zaman çubuğu + üzerinde süre/cümle önizlemesi, 0–9 tuşları,
  dokunmatikte ilk oynatmada bir kez jest ipucu. Adım videosu bitince altında o adıma bağlı tek soru (`HizliKontrol`);
  yanıtlanana dek geri sayım bekler, cevap Eksikler istatistiğine "Video sonu soruları" olarak yazılır. Sarma otomatik
  geçişi iptal etmez (yalnız "Burada kal"). `.kmb-dv[role=dialog] { max-height: none }`.
- **Önleme:** oynatıcıda görünmez tıklama bölgesi tek dokunuşta oynatma durumunu ya da konumu değiştirmez; konum/oynatma
  değiştiren tek dokunuş yalnız görünür düğmededir ve görünür düğme çift dokunuş bölgesine (kenar %35) taşmaz. Jest
  kuralları başsız Chrome dokunma olaylarıyla sınanır (26 senaryo: tek/çift/üçlü dokunuş, basılı tutma, kaydırma,
  tam ekran, fare). Tam ekran/sabit katmanlar `[role=dialog]` taşıyorsa genel max-height'ı kapatır (H461, hucrem.css örneği).

## H462 — KMB Hedefler filmi: yakınlaştırma ayrıntıyı kesiyordu; 3B deneme (Pixar/organik) kalite eşiğini geçemedi → ARŞİV (2026-11-01)

- **Belirti:** Filmde kamera odak ögesine 1,5–1,8× yaklaşınca komşu ayrıntılar ve etiketler kadrajdan taşıyor, yakınlaşma
  olmasa da sahne 8:5 kadrajı "çok yakın çekim" gibi dolduruyordu. Ardından denenen three.js 3B küme (14 sahne; ilkel
  kapsül/küre sonra marching-cubes organik yüzeyler) kullanıcı denetiminde reddedildi: iç içe geçen parçalar, kesik kadraj,
  boncuk gibi zincir yüzeyler, "sakız gibi" katı antiseptik halkaları (ıslak film olmalıydı), insana benzemeyen anatomi,
  ölçek uyumsuz eller; `organik()` nesnesine dışarıdan verilen ölçek iç ölçeğini ezdiği için eller minicik/kopuk çıktı (H464).
- **Kök neden:** (1) yakınlaştırma odak kutusunun büyüklüğüne bakmadan sabit katsayıyla yapılıyordu; (2) 3B'de prosedürel
  ilkel geometri ile insan dokusu kurmak ek yeri ve iç içe geçme üretir, metaball ile kaynaştırma da düşük çözünürlükte
  boncuklanır; sıvı/katı ayrımı (ıslak alan) malzemeyle değil geometriyle verilmişti; önizleme "tüm ögeler açık" yapay
  durumuyla alındığından birbirini dışlayan ögeler (sönük/şişmiş balon) üst üste görünüp hata gibi okundu.
- **Çözüm:** yakınlaştırma tavanı 1,35 ve odak kutusu + etiket payı kadrajın en çok %70'i (`HedefFilmi` kamera; veri zoom
  1–1,4 kapısı `dogrula.py`). 3B küme (`components/kmb/sahne3b/`, `SahneGoster`) **arşivde**: varsayılan KAPALI
  (`localStorage.medsoru_kmb_3b='1'` ile yalnız geliştirici açar), "3B" düğmesi kaldırıldı, canlıya gönderilmedi.
  Ön yüz 2B (SVG + Lottie) hattında sürer; hedef stil: düz vektör çizgi film (referans: Foley kateter illüstrasyonu —
  pürüzsüz dolgular, temiz kontur, sınırlı palet).
- **Önleme (2B yeniden çizim için KESİN kurallar):** ① hiçbir parça diğerinin içine girmez (katmanlar kesişmez, önde olan
  arkadakini düzgün örter); ② ölçekler anatomiye uyar (16 Fr ≈ 5 mm; üretra ~1 cm; balon 10 mL ≈ 2,7 cm); ③ sıvılar
  (idrar, izotonik, jel, antiseptik) yarı saydam/parlak ve yüzeye yapışık gösterilir, katı halka/boncuk olmaz; ④ bakış
  açısı anatomiye göre seçilir (sagittal kesit yandan, vulva önden litotomi, mesane içi üstten) ve kadraj hiçbir anlatılan
  ögeyi kesmez; ⑤ her öge adıyla ayırt edilir (neyin ne olduğu belirsizse çizim yeniden yapılır); ⑥ önizleme
  gerçek vuruş durumuyla alınır (`sahne3b_onizle.mjs --film`, SVG için de çalışır), "tüm ögeler açık" karesi yalnız
  kimlik denetimi içindir; ⑦ her sahne yayından önce kare temas sayfasıyla göz denetiminden geçer.

## H465 — KMB 2B Erkek sahnesi: sırtüstü gövdede iç organlar "ayakta" dizilimindeydi (mantık hatası) (2026-11-01)

- **Belirti:** Kullanıcı onaylı 2B stil örneğinde (Erkek kesit) "mantıksal hatalar" gördü: mesane göbek deliğinin tam altında,
  prostat mesanenin altında, penis yatay ve ~19 cm, üretra skrotumun altından dolanıyor, simfiz işlevsiz, gövde bacaksız
  bitiyor, mesane dopdolu dururken küvet boş, meatus etiketi örtünün üstünde.
- **Kök neden:** Gövde sırtüstü (ön yüz yukarı, ayaklar sağda) çizilirken iç anatomi ayakta duran insanın sagital
  şemasından (mesane üstte → prostat altta → penis öne/sağa) kopyalandı; yani iç organlar gövdeye göre 90° dönüktü.
  Tek tek parçalar doğru görünse de yön sistemi (superior/inferior, anterior/posterior) gövdeyle çakışmıyordu.
- **Çözüm:** Sahne tek yön sistemiyle yeniden kuruldu: inferior = sağ, anterior = yukarı; simfiz derinin hemen altında,
  mesane simfizin arka-üstünde, prostat arkasında, bulbar üretra perinede öne kıvrılır, penis eldivenli elle DİK tutulur
  (işlem standardı; avuç şaftın arkasında, başparmak/parmak uçları kenarlarda → üretra kanalı görünür), skrotum penis
  kökünün arka-altında, uyluklar sağda örtü altında, küvet örtü üstünde; idrar yalnız `e-balon-dogru` durumunda lümen →
  damla → küvet filmi. Ölçek 1 cm ≈ 12 px.
- **Önleme:** Her kesit sahnesinde önce yön sistemi yazılır (kod yorumunda: "inferior = …, anterior = …"), her organ
  bu sisteme göre yerleştirilir; "ayakta şema" başka duruşa KOPYALANMAZ. Tutulması gereken şey tutulur (el çizilir),
  gövde kadrajda kesilmez (uyluk/örtü ile tamamlanır), sıvı davranışı duruma bağlıdır (kateter yerleşmeden idrar akmaz).
  Kural `docs/KMB_2B_STIL.md` §2-3/§2-6; önizleme `sahne3b_onizle.mjs --film` ile gerçek vuruş durumunda bakılır.

### H497 — KMB Lottie: çarpı "Z" çiziyordu; çok alt yollu SVG tek şekle birleşiyordu (2026-11-05)
- **Belirti:** KMB videolarında kırmızı çarpı (ortak2b.carpi) iki kol yerine Z biçiminde; kesik çizgi/akış yollarında alt yollar arası fazladan çizgi.
- **Kök neden:** `lottie_dsl.yol` her yolu tek Lottie `sh` alt yolu sayıyordu; `M… L… M… L…` dizisinde ikinci M bir önceki noktadan çizgiyle bağlandı.
- **Çözüm/önleme:** `yol` çok-M yolu alt yol başına ayrı `sh` listesi döndürür, `G` listeleri düzleştirir; `carpi` iki ayrı kol çizer. 02 (eski + 2B) videoları yeniden üretildi.

### H498 — KMB: ata grupta transform olan sahnede kutular (bbox) 60 px kaydı (2026-11-05)
- **Belirti:** ng-kesit sahnesinde video halkaları/etiketleri ve Hedefler filmi kamerası farinks bölgesinde 50–80 px kayık hedefliyordu.
- **Kök neden:** `getBBox` ögenin kendi koordinatını verir; sahne çizimi `translate(60 0)` grubunun içindeydi. `svg_disa.mjs` ve `HedefFilmi.tsx` dönüşümü hesaba katmıyordu.
- **Çözüm/önleme:** ikisi de kutuyu `svg.getCTM()⁻¹ · el.getCTM()` ile sahne köküne çevirir. Sahnede grup kaydırması serbest; kutular hep kök koordinatında.

### H499 — KMB: clipPath'li sıvı Lottie'de dikdörtgen olarak organ dışına taştı (2026-11-05)
- **Belirti:** ng-mide videolarında mide içeriği mide dışına taşan dikdörtgen.
- **Kök neden:** `svg_lottie.py` süzgeç/desen/kırpma taşımaz; sahnede sıvı `clipPath` ile kırpılmış dikdörtgendi.
- **Çözüm/önleme:** sıvı organ biçiminde açık yol olarak çizildi. Kural: Lottie'ye gidecek KMB sahnelerinde `clipPath`/`mask`/`filter` kullanılmaz; biçim yolla verilir.

### H500 — KMB: altyazı bandı (alt %24) kesitteki ana yapıları örtüyordu (2026-11-05)
- **Belirti:** Nazogastrik kesitte larinks/trakea/özofagus girişi ve aspirasyon oku altyazı açıkken görünmüyordu.
- **Kök neden:** sahne anatomisi tüm 500 px yüksekliğe yayılmıştı; kamera kadraj kenarını aşamadığı için yakınlaşma da kurtarmadı.
- **Çözüm/önleme:** anatomi 70 px yukarı taşındı, alt yapılar kadraj altına uzatıldı. Yeni KMB sahnesinde anlatılacak yapılar y ≤ 380 içinde çizilir.

### H523 — Taş Masası: "Oyunu başlat / masa kur" bazen hiçbir şey yapmıyor, hata da görünmüyordu (2026-11-10)
- **Belirti:** Oyunlar'da masa kurmaya ya da "Oyunu başlat"a basınca ekran olduğu gibi kalıyor, hiçbir bildirim çıkmıyordu; oyun başlasa da hamlelerde takılma varmış gibi bekleniyordu.
- **Kök neden:** iki sessiz düşme. (1) İstemci soket `OPEN` olur olmaz mesajı yolluyordu, ama sunucu kimlik doğrulanana (`gir` → `girdi`) dek `gir`/`ping` dışındaki her mesajı **yanıtsız** atıyordu; `onopen` içinde `auth.getIdToken()` beklenirken basılan kur/başlat kayboluyordu. (2) Bağlantı koparken basılan "başlat/sonraki el" istemcide yalnız kur/katıl kuyruğa alındığı için **hiç gönderilmiyordu**. Hiçbir yanıt gelmediğinden ne hata ne bekleme göstergesi vardı (merkezdeki düğmeler 5 sn sonra sessizce yeniden açılıyordu).
- **Çözüm/önleme:** `istemci.ts`: `gir`/`ping` dışındaki mesaj yalnız `baglanti === 'hazir'` iken gider; hazır değilse kur/katıl/başlat/sonraki el kuyruğa girer, `girdi` gelince (gerekirse önce masaya geri oturularak) gönderilir; hamle gönderilemezse hata bildirilir. Yanıt beklenen her istek `bekliyor` durumuna yazılır → `MasaBekleme` (kurma/katılma/dağıtım tam ekran, hamle küçük hap) ve 15 sn yanıtsızlıkta hata + soket yenileme. `sunucu.ts`: kimliksiz mesaja `kimlik-bekle` hatası döner. Kural: istemci–sunucu sözleşmesinde **hiçbir istek yanıtsız düşmez**; sunucu ya durum ya hata döner, istemci her bekleyen isteği görünür kılar ve zaman aşımına bağlar.

### H524 — Taş Masası: Taş Domino masası açılır açılmaz "Cannot read properties of undefined (reading 'length')" ile çöküyordu (2026-11-10)
- **Belirti:** Taş Domino oyunu başlayınca masa yerine hata ekranı (`chunk-MasaView`, `Array.filter` içinde `.length`).
- **Kök neden:** `MasaUstCubuk` "bu elin cezaları" listesini oyun Uno değilse (`oda.tur !== 'uno'`; işlenmemiş çalışmada `tasMi`) `oda.oyun`'u `OkeyGorunum` sayıp `oyuncular.filter((o) => o.cezalar.length)` ile kuruyordu. Bu koşul 3. turda eklenen Taş Domino'yu (ve `tasMi` hâliyle de domino'yu) kapsar; `DominoOyuncuGorunum`'da `cezalar` alanı yoktur. `as OkeyGorunum` dökümü tip denetimini susturduğu için derleme yakalamadı.
- **Çözüm/önleme:** erişim `o.cezalar?.length` yapıldı (cezası olmayan oyun = boş liste). Kural: yeni oyun türü eklenirken `tasMi`/`as OkeyGorunum` geçen her yer gözden geçirilir; ortak kabuk bileşenleri oyuna özgü görünüm alanlarını (`cezalar`, `atiklar`, `acti`) yalnız isteğe bağlı erişimle okur, `as` dökümüyle alan varsayılmaz.

### H525 — Taş Masası: başlamış masaya gelen arkadaş geri çevriliyor, kopmalar görünmüyordu (2026-11-10)
- **Belirti:** Oyun başladıktan sonra bağlantıyla gelen arkadaş yalnız "Bu masada oyun başlamış." görüp merkeze düşüyordu; bağlantıyla gelip önce giriş yapan kişi girişten sonra masaya dönmüyordu; rakip koptuğunda ya da kendi bağlantın koptuğunda masada yalnız küçük bir "Yeniden bağlanılıyor…" şeridi vardı, kimin beklendiği ve ne kadar süredir bilinmiyordu.
- **Kök neden:** sunucuda masada "koltuk = bağlantı kimliği" eşlemesi tekti; koltuksuz bağlantı kavramı (izleyici) ve kimliği farklı birinin bot koltuğunu alması yoktu. `?masa=` parametresi açılışta silinip giriş yapılmamışken `kimlik` hatasıyla kayboluyordu. İstemci kopma anını ve deneme sayısını tutmuyor, sunucu kopan koltuğun zamanını yayınlamıyordu.
- **Çözüm/önleme:** `sunucu.ts`: oyun sürerken gelen bağlantı izleyici olur (`izleyici` haritası, `gorunum(…, null)` ile gizli bilgi açılmaz), `koltukIste`/`koltukVer`/`koltukRed`; koltuk devri `oda.devir` (bağlantı kimliği → koltuk kimliği, motor durumu değişmez, her kimlik okuması `sid()` üzerinden); kopan koltuğun anı `kopZ` → görünümde `kopSn`; yanlış yazılan kod (O/0→D, I/1→L/J/T) var olan odaya eşlenir. İstemci: davet kodu `sessionStorage`'da girişe dek saklanır; `deneme`/`sonrakiDeneme` → `MasaBaglanti.tsx` katmanları. Kural: masaya gelen hiçbir kişi açıklamasız geri çevrilmez; bekleyen her durum (kim, ne kadar, ne yapılabilir) ekranda yazılır. Sınama kancası `window.__masaTest` yalnız `?masatest` kipinde.

### H526 — Taş Masası: Remi/Kastet düzenlemede elden taslağa konan taş geri alınamıyordu (2026-11-10)
- **Belirti:** Masayı düzenle kipinde ıstakadan pere konan taş yanlışsa tek tek geri alınamıyor, yalnız "Vazgeç" ile tüm düzenleme siliniyordu.
- **Kök neden:** taslaktaki taşa dokunma yalnız seçimi açıp kapatıyordu; taşın elden mi masadan mı geldiği ayrımı dokunma işleyicisinde kullanılmıyordu.
- **Çözüm/önleme:** `OkeyMasa.tsx` `duzen.onTas`: el taşına (`elMap`) dokununca gruplardan çıkar → ıstakaya döner; masa taşı seçilir. Taslak araçlarında her eklemenin tek tek geri alma yolu olmalı.

### H527 — Taş Masası: dar ekranda eylem düğmeleri 3–4 satıra yığılıyor, durum yazısı "Sıra…" diye kesiliyordu (2026-11-10)
- **Belirti:** 375 px'te Yedili/Takım/Remi eylem çubuğu ekranın üçte birini kaplıyordu; masaüstünde düğme çoğalınca "Sıra sende: taş çek" yazısı "Sıra…"ya kısalıyordu; oyun sırasında sitenin "Bir sorun bulundu" hapı üst çubuğu örtüyordu.
- **Kök neden:** `.om-eylem-dugmeler` dar kipte `flex-wrap: wrap` + `min-height: 93px`, durum yazısı `white-space: nowrap; text-overflow: ellipsis` ve düğmeler `flex: none` olduğundan tüm daralma yazıya düşüyordu; `NetworkBanner` sabit konumda masanın kabuğunun üstündeydi.
- **Çözüm/önleme:** dar kipte tek satır, simge üstte kısa yazılı, yatay kaydırılan düğmeler; durum yazısı sarar ve en az 150 px; oyun sırasında `html.mk-oyunda .nb-wrap` gizli (bağlantıyı masa gösterir). Yeni eylem eklerken 375×740'ta sayfa_tarama/senaryo ile bakılır.

### H528 — Taş Masası: lobide mod seçenekleri "NormalZorlu", "KlasikYığma7-0AtlamaHızlıÇek-çek" diye bitişik yazı olarak görünüyordu (2026-11-10)
- **Belirti:** Lobideki "Oyun modu", "Uno modu" ve "Kişi başı taş" seçenekleri düğme gibi değil, aralıksız tek satır metin olarak çıkıyordu; hangisinin seçili olduğu anlaşılmıyordu. "Kısaca" adımlarında numara yoktu, kural metinlerinde madde imi/numara görünmüyordu. Merkezde Taş Domino çiziminde taşlar üst üste biniyor, iki kişilik oyunlar "2–2 oyuncu" yazıyordu. Bota karşı oyunda Uno modu ve Zorlu mod hiç seçilemiyordu (lobi atlanıyor).
- **Kök neden:** `MasaLobi.tsx` `mk-secenek` sınıfını kullanıyordu ama bu sınıfın hiçbir stil dosyasında kuralı yoktu (2. turda bileşen yazıldı, CSS eklenmedi); site sıfırlaması `button`'ı çıplak bıraktığından metinler bitişti. Liste imleri de aynı sıfırlamayla (`list-style: none`) siliniyordu, `.mk-kural ol/ul` bunu geri açmıyordu. Domino çiziminde 34 px'lik taşlar 28 px arayla ve 90° döndürülerek konmuştu. Mod ayarları yalnız lobide olduğundan lobisiz başlayan bot oyununa ulaşmıyordu.
- **Çözüm/önleme:** ortak `ModSecici.tsx` (`OyunModu`, `UnoModu`: başlık + kısa tanıtım kartları, seçili işaret) hem lobide hem kurulum yaprağında; bot kurulumu `asistan`/`unoMod`/`tasSayisi` gönderir. `lobi.css` + `kurallar-gorsel.css` (liste imleri açık, numaralı `mk-adimlar`). Kategoriler ve sıra tek kaynakta: `oyunKatalog.ts` (merkez kartları, kural sekmeleri, kısayollar). Kural: TSX'e yeni `mk-*` sınıfı yazınca aynı işte CSS'i de yazılır; `grep -rn "<sınıf>" src/styles` boşsa iş bitmemiştir. Yeni ayar lobiye eklenirken bota karşı kurulum yaprağına da eklenir.

### H529 — Taş Masası: tüm oyunlarda hamleler gecikmeli görünüyordu (2026-11-10)
- **Belirti:** Kullanıcı "tüm oyun modlarında internet gecikmesi var" dedi; taş/kart/işaret dokunduktan sonra geç yerine oturuyor, masa o arada donuk kalıyordu.
- **Kök neden:** Sunucu hızlı (Oracle içinde ping ≤18 ms, durum paketi ~1,3 KB), ama istemci her hamlede ekranı yalnız sunucunun `durum` yanıtıyla çiziyor ve yanıt gelene dek masayı kilitliyordu (`is-gonderiliyor`). Yanıt Cloudflare tüneli (`--protocol http2`) üstünden geliyor: ölçüm medyan 94 ms, p99 673 ms, en kötü 2,4 sn (TCP yeniden gönderim / tünel takılması). Her hamle bu gidiş-dönüşü bekliyordu.
- **Çözüm:** `src/services/masa/tahmin.ts` iyimser tahmin: oyuncunun kendi hamlesinin istemcide kesin bilinen sonucu (XOX/Go işareti + Go esir alma, Uno/Pişti kartı, Domino taşı, Çizgi adımı, 101 taş atma) anında ekrana yazılır; gizli bilgi tahmin edilmez (sıra bilinmiyorsa `''` → ikinci hamle kilitli). `istemci.ts`: `onayli` son sunucu görünümü; `durum` tahmini ezer, `hata` ya da 15 sn yanıtsızlıkta onaylıya dönülür. Sınama: 7 motorda bot oyunlarıyla 11.700 tahmin sunucu sonucuyla karşılaştırıldı (tahta/el birebir; yalnız Pişti yeni dağıtımı ve Çizgi tur sonu `kalan` farkı, sunucu düzeltir); tarayıcıda 1,6 sn yapay gecikmede işaret anında çizildi.
- **Önleme:** Yeni oyun/hamle eklenince `tahmin.ts`'e kesin bilinen kısmı eklenir ve aynı karşılaştırma koşulur; ekran hiçbir zaman ağ yanıtına kilitlenmez. Okey per açma/işleme/çekme hâlâ sunucuyu bekler (ıstaka düzeni + gizli taş). Ağ tarafındaki sıçramalar için kalıcı çözüm ancak WS'yi tünelden ayırmaktır (ayrı alt alan, Cloudflare/Oracle erişimi kullanıcıda).

### H533 — Taş Masası: dar ıstakada grup toplamı yanlış; Go/XOX botu hiç hata yapmıyordu (2026-11-10)
- **Belirti:** Istaka daralınca (telefon, döndürme) bitişik duran taşların per toplamı (101 açılış balonu, Remi 30) yanlış görünüyordu. Go ve XOX'ta bot "hep en mantıklı yolu seçip" kazanıyordu. Takım Yedili/Yedili Zorlu modda masa dizilimi ve ıstaka sıralaması kapalıydı; çekilen taş ıstakaya rastgele ilk boşa giriyordu.
- **Kök neden:** (1) `yuva.ts uzlas` boyut değişince taşları konumla taşıyordu: yeni sütun sayısını aşan taşlar `ilkBos` ile ilk boşluğa düşüp komşu gruba yapışıyordu; `diz` boşluk sığmayınca `dene(0)` ile tüm grupları bitişik diziyordu → `gruplar()` iki peri tek grup sayıp toplamı bozuyordu. Sütun sayısı `n+4` payıyla grup boşluklarını taşımıyordu. (2) XOX 3×3 tam minimax, Go botu gürültüsüz en iyi puan; zorluk seçeneği yoktu. (3) Zorlu mod "elle dizme yok" kararı sıralama/masayı dizi de kapatıyordu.
- **Çözüm:** `uzlas` boyut değişince `diz(yeni, gruplar(eski))` ile grupları taşır; `diz` önce boşluklu, sonra satır sonunda bölerek (yapıştırmadan) dener; `OkeyMasa` sütun payı `max(4, %35·n) + kat`. `OdaAyar.botZorluk` (kolay/orta/zor, varsayılan orta): XOX hata olasılıkları (rastgele kare / kazancı / engeli kaçırma), Go gürültü + ara sıra tahmini hamle + tehlikeyi görmeme; zor = eski bot. Bota karşı Go/XOX'ta "Geri al" (insan hamlesi + bot yanıtı; süreli Go'da yok). Sırala + Masayı diz iki modda; "Istakayı otomatik sırala" tercihi (varsayılan açık): ele yeni taş girince son dizme biçimine göre dizilir.
- **Önleme:** Istaka düzeni değiştiren her işlev grupları korumalı; grup toplamını gösteren her ekran dar boyutta (`yuva_t` sınaması: 21 taş 6 grup, sütun 16/14) denenir. Bot ekleyen her oyuna zorluk seçeneği verilir; "kusursuz bot" yalnız Zor'da. Sınama `tahta.sinama.ts` (kolay bot 40 elde ≥5 kayıp).

### H534 — Taş Masası: masadaki taş eldeki taşlarla yeni pere katılamıyordu (2026-11-10)
- **Belirti:** Yedili Okey'de masada dörtlü 10 grubu, elde sarı 9 ve 11 varken sarı 10'u gruptan alıp 9-10-11 serisi kurmak mümkün değildi; 101 Okey'de masayı düzenleme hiç yoktu. Kullanıcı: "kurallara aykırı bir şey yapmam; okey, 101 ve yedili için geçerli".
- **Kök neden:** `motor/yedili.ts` `duzenle` hamlesi yalnız masadaki taşları kabul ediyordu (`Masayı düzenlerken elden taş eklenemez` reddi); arayüz düzenleme kipinde ıstaka seçimini siliyor, elden taşı yalnız Kastet/Remi (`acik`) için taslağa alıyordu. `motor/yuzbir.ts`'te `duzenle` dalı yoktu. Yeni per yalnız `ac` (tamamı elden) ya da `isle` (uca/bölerek tek taş) ile kurulabildiğinden masadan taş ödünç alan birleşim iki hamleye bölünemiyordu.
- **Çözüm:** `duzenle` üç motorda da masadaki taşların tamamı + elden taş alır; her per geçerli olmalı, masadan ele taş dönmez. Elden taş katıldıysa hamle sayılır (`hamleYapti`, yedilide el biterse kazanır, takımda elden taşla 4'lenen grup hediye verdirir; 101'de atacak taş kalmalı, çiftlere dokunulmaz, çiftle açan elden katamaz, masadaki okey `perCoz` ile yeniden değer alır). `OkeyMasa.tsx`: düzenleme kipinde ıstaka taşı seçilip/sürüklenip taslağa girer, 101'e "Masayı düzenle" düğmesi. Düz Okey'de masaya per açılmadığı için uygulanmaz.
- **Önleme:** Masaya taş koyan her oyunda "masadan taş + elden taş = yeni per" senaryosu motor sınamasında bulunur (`yedili.sinama.ts`, `yuzbir.sinama.ts` düzenle bölümleri). Bir hamle türü bir oyuna eklenince aynı masa modelini paylaşan öteki oyunlar (yedili/takım/101/kastet/remi) birlikte gözden geçirilir.
- **Ek (aynı gün, kullanıcı isteği):** düzenleme için düğme şart değil. `motor/odunc.ts oduncBul` seçili el taşlarına masadan 1–2 taş ödünç alan çözümü bulur (her renk; veren per geçerli kalmalı); `OkeyMasa` Per aç / yeni per alanı / masadaki taşa dokunma bunu `duzenle` olarak yollar, çözüm yoksa taşa dokunmak taslağı o taş seçili başlatır. Sırala yedilide de `per` kipine sahip; Masayı diz renk → sayı → açılış sırası döner. Sınama: `yedili.sinama.ts` / `yuzbir.sinama.ts` oduncBul bölümleri.

### H535 — Taş Masası: masayı düzenlerken perler boşalan yere kayıyordu (2026-11-10)
- **Belirti:** Masayı düzenlerken bir perden taş alınınca ya da per boşalınca öteki perler hemen boşluğu dolduruyor, satır/sütun değiştiriyordu; kullanıcı taşların yerini gözden kaçırıyordu. Düzenlemeye girerken de perler yeniden sıralanıyordu.
- **Kök neden:** `OkeyMasa.tsx` taslağı `perSirala(masaPerler)` ile (ekrandaki sıradan bağımsız) başlatıyor, her taşımada boş grupları `filter((x) => x.length)` ile atıyordu; per alanı sarmalı flex olduğu için daralan/kaybolan perin ardındakiler sola ve üst satıra akıyordu.
- **Çözüm:** Taslak ekrandaki sırayla başlar (`taslakBasla`), boşalan per yer tutucu olarak kalır (`om-per--bos`, kesikli çerçeve), her per düzenleme başındaki piksel genişliğini en az genişlik olarak korur (`PerAlani enAz`); yeni per sona eklenir, yalnız sondaki sonradan eklenmiş boş perler atılır (`kirp`). Onayda boş perler hamleye girmez.
- **Önleme:** Kullanıcının elle düzenlediği alanda (masa taslağı, ıstaka) öğeler kendiliğinden yer değiştirmez; düzen yalnız kullanıcının açık isteğiyle (Sırala, Masayı diz) değişir. Sınama: düzenlemede taş alıp per boşaltınca komşu perin `getBoundingClientRect().left/top` değeri değişmemeli.

### H542 — Uno'ya 10 yeni mod eklenirken motor sınamasının yakaladığı dört kural hatası (2026-11-10)
- **Belirti (yayından önce, `unoMod.sinama.ts` ile yakalandı):** (1) Extreme'de vuruş gelen oyuncu başka renkten Vur kartı ekleyemiyordu. (2) Hepsini At, 7 takası, 0 devri ya da kart vermeyle tek karta düşen oyuncu UNO demek zorunda kalmıyor, yakalanamıyordu. (3) Takım modunda Takım Oyunu jokerinden sonra ortak "uyan kartını oyna" zorunluluğunda kilitleniyordu. (4) Yalancı modunda kapalı kart karar beklerken deste yenilenince atık boşalıyor, yalan yakalanınca oyun çöküyordu.
- **Kök neden:** (1) `oyna` dalı biriken ceza denetiminden (`yiginUyar`) geçen karta ayrıca renk/değer eşleşmesi (`duzUyar`) uyguluyordu. (2) UNO durumu yalnız "kart oynayıp 2→1" anında işaretleniyordu; el sayısını değiştiren öteki yollar (toplu atma, takas, devir, verme) hesaba katılmıyordu. (3) Zorunluluk bayrağı (`takimOyun`) kurulduktan sonra aynı hamlede "eli biten oyuncuya yarı verme" araya girip ortağın uyan tek kartını elinden alabiliyordu. (4) `al()` desteyi yenilerken atıkta yalnız en üstteki kartı bırakıyordu; karar bekleyen kapalı kart geri alınınca altındaki gerçek üst kart desteye gitmiş oluyordu.
- **Çözüm:** (1) Biriken ceza varken yalnız `yiginUyar` geçerli. (2) `sonIslem` her hamlenin sonunda eli 1'e düşen herkesi (oynarken UNO diyen hariç) `yakalanabilir` yapar. (3) Uyan kart kalmadıysa çekme serbest: jokeri oynayan 2 kart çeker, sıra geçer. (4) `bekle.tur === 'yalan'` iken atıkta iki kart bırakılır.
- **Önleme:** Uno'ya kural/kart ekleyen her değişiklikte `npx tsx src/services/masa/motor/uno.sinama.ts` ve `unoMod.sinama.ts` 0 hata vermeli: her mod için birim senaryolar + bütün oyuncu sayılarında hepsi-bot rastgele eller (kart korunumu, tıkanmama, gizlilik, puan toplamı) + bulanık hamle. Yeni bir "bekleyen karar" ya da el sayısını değiştiren etki eklenince korunum denetimine (`korunum`) ve `sonIslem` UNO taramasına dahil edilir. Arayüz: `meds_temp/uno_ui/uno_ui.mjs` (başsız Chrome, `?masatest`, 12 mod × telefon dikey/yatay, tablet, masaüstü; taşma, dokunma hedefi, konsol hatası). Başsız sınama çıktısı `/tmp/claude-1000` kotasına yazılmaz (EDQUOT ile yarıda kesildi), `meds_temp` altına yazılır.


### H544 — Ek modül içeriği hocanın materyali sorulmadan yazıldı; çalışma soruları gelince 16 konunun tamamı yeniden yazıldı (2026-11-10, Yürüyüş ve Kampçılık)
- **Belirti:** "Yürüyüş ve Kampçılık" seçmeli dersi için kazanım bilinmediğinden doğada beceri ağırlıklı 8 başlık yazıldı (128 soru + 17 görsel). Kullanıcı ardından hocanın 32 sayfalık çalışma sorularını verdi: dersin yarısı ilk taslakta hiç yoktu (dağcılık tarihi ve türleri, kayaç–buzul, dağ ekosistemi, UIAA bildirgeleri, jeolog pusulası) ve taslaktaki bazı bilgiler hocanın cevabıyla çelişiyordu (su kaynağına 60 m ↔ 50 m; "altta hafif ve hacimli" ↔ hocaya göre yanlış; çanta görseli).
- **Kök neden:** müfredat dışı derste tek kaynak hocadır; içerik genel bilgiyle kurulup sonradan hocaya uydurulmaya çalışıldı. Üretime başlamadan önce "hocanın notu, sunumu, çalışma sorusu var mı" diye sorulmadı.
- **Kalıcı çözüm:** içerik `meds_temp/ek_modul/<modül>/hoca_calisma_sorulari.txt` esas alınarak yeniden kuruldu (`GOREV.md`: konu başına hoca soru numaraları + hocanın kendi içinde çeliştiği yerlerde verilen kararlar); ilk taslak `eski/` altında kaynak olarak kaldı. `scripts/uretim/ek_modul/TALIMAT.md`'ye "Hocanın çalışma soruları varsa ESAS KAYNAK odur" bölümü eklendi; iki bağımsız denetçi hoca kapsamını soru soru yeniden eşledi.
- **Önleme:** yeni ek modülde ilk iş hocanın materyalini istemektir (AGENTS kural 30). Hocanın kendi içinde çeliştiği cevaplar (kazık 45°/90°, tuvalet 50/150 m) sessizce "düzeltilmez": en çok yinelenen değer esas alınır, ekrana "ikisini de bil" notu düşülür ve kullanıcıya raporlanır. Hocanın bilimsel olarak tartışmalı ifadesi (baştan %50 ısı kaybı, gnays kristalleri) hocanın dediği gibi kalır; metin ona aykırı yeni iddia eklemez.

### H546 — Ek modülde sesli ders PDF'le birlikte ilerlemiyordu; eşleme kurulurken iki ölçüm tuzağı (2026-11-10, Yürüyüş ve Kampçılık)
- **Belirti:** kullanıcı: "ek modüllerde sesli ders oluşturdum fakat PDF ile birlikte aynı anda işlenmiyor". Ek modül sesli dersi yalnız bölüm kartlarını sırayla yakıyordu; klasik sesli dersteki gibi PDF sayfası, anlatılan satır ve cümle takibi yoktu.
- **Kök neden:** ek modül hattı (kural 30) kurul hattından ayrı kuruldu ve klasik dersin iki katmanı hiç üretilmedi: cümle zamanı (`ses.py` EMA'nın döndürdüğü zamanlamayı atıyor, klip başına yalnız süre yazıyordu) ve PDF konumu (kitapçık `pdf.py` ile basılıyor ama hangi bölümün hangi sayfada/kutuda olduğu kaydedilmiyordu).
- **Kalıcı çözüm:** `scripts/uretim/ek_modul/pdf_esle.py` → `src/data/ek_moduller/<modül>/pdf_esle.json` (klip başına sayfa, bölüm kutusu, satır kutuları, cümle zamanı, cümle → not maddesi); ekranda "PDF ile" kipi (`EkPdfDers.tsx`, `PdfDocView` işaret katmanı). LLM ve GPU yok; ses yeniden üretilmedi.
- **Tuzak 1 (PDF metin sırası):** PyMuPDF blokları okuma sırasıyla vermez; madde listeleri bloğun sonuna düşer, başlıktan sonraki satır bir sonraki bölümün başlığı olur. Satırlar sayfa içinde konuma (y, x) göre sıralanmadan başlık/madde aranmaz.
- **Tuzak 2 (duraklama eşiği):** `cumle_zaman.py` eşiği (konuşma düzeyinin %2,5'i) EMA kliplerinde paragraf içi cümle sonlarını (0,2–0,3 sn, taban tam sessiz değil) görmüyor; sınırların %20'si tahminde kalıyor, klip sonundaki nefes payı son sınırı kapıyordu (son cümle 0,3 sn). Eşik %6'ya çıkarıldı, baş/son sessizlik aday dışı, tahmin konuşulan süre üzerinden, bütün sınırlar birlikte (sıra korunarak) yerleştirildi: 631/667 sınır duraklamada; üç klipte Whisper kelime zamanıyla ortalama sapma 0,06 sn, en çok 0,56 sn.
- **Önleme:** ek modülde ses ya da ders kitapçığı yeniden üretilince `pdf_esle.py` yeniden çalıştırılır; `dogrula.py --modul` eşleme eskimişse (klip özeti ya da PDF boyutu tutmuyorsa) HATA verir, ekran da özeti tutmayan klibin eşlemesini kullanmaz. Karşılığı bulunamayan cümleye madde uydurulmaz (yalnız bölüm çerçevesi; kural 17'deki "çapa uydurma" yasağıyla aynı ilke).

### H552 — Sesli çalışma sorularında boşluk doldurma "boşluk" diye okunuyordu (2026-11-10, ek modül)
- **Belirti:** hocanın boşluk doldurma sorularında EMA "Uyku tulumu, vücudun boşluk kaybını önlemek için kullanılır" gibi anlamsız cümleler okuyordu; çok boşluklu sorularda "boşluk, boşluk, boşluk".
- **Kök neden:** `ek_modul/ses.py` ekran metnini (`metin`) doğrudan okunuşa çeviriyor, `____`'yi " boşluk " sözcüğüne değiştiriyordu; ekranda anlamlı olan biçim seste soru değildir (ekran ≠ ses ilkesi, kural 30, bu sorularda uygulanmamıştı).
- **Çözüm:** 100 boşluk sorusunun her birine soru biçimli `okunus` alanı yazıldı ("Uyku tulumu, vücudun ne kaybını önlemek için kullanılır?"); ses yalnız onu okur, ekran ve kitapçık `metin`'i göstermeye devam eder. Sesler GPU'da yeniden üretildi, `pdf_esle_hoca.py` ile takipçi yeni seslere eşlendi (okunuş sorunun kitapçıktaki satırlarını yakar).
- **Önleme:** `dogrula.py --modul` boşluklu (`__`) her hoca sorusunda `okunus` yoksa ya da soru işaretiyle bitmiyorsa HATA verir. Yeni boşluklu soru eklenirken (her modülde) okunuş elle, doğal soru cümlesi olarak yazılır; mekanik "boşluk/ne" değişimi yapılmaz.

### H574 — Oyun masasında 13 kez çökme: `oyuncu.cezalar` olmayan eski oyun durumu (2026-11-14, kullanıcı "bu tarz hataları da çöz" dedi)
- **Belirti:** Canlı günlükte `/sorular/oyunlar` için 13 çökme: `Cannot read properties of undefined (reading 'length')`, yığın `chunk-MasaView…` → `Array.filter` → `MasaUstCubuk`.
- **Kök neden:** `MasaUstCubuk` içinde `(oda.oyun as OkeyGorunum).oyuncular.filter((o) => o.cezalar?.length)`. `?.` yalnız `cezalar` alanını korur; `oyuncular` **dizisi** yoksa `.filter` düşer (oda oyunu açılırken/bitmiş oyundan dönerken eski biçimli durum). Sonraki `.map` da `o.cezalar.map` ile aynı riski taşıyordu.
- **Kalıcı çözüm:** `Array.isArray(oyuncular)` önce sınanır, `cezalar` alanı `Array.isArray` ile doğrulanır; `MasaSonuc` (`satirlar`, `s.cezalar`), `okey/Rakipler` ve `okey/OkeyMasa` aynı korumaya alındı.
- **Önleme:** `?.` **alan** korur, **dizi metotlarını** korumaz: `X.filter(...)` öncesi `Array.isArray(X)` sınanır. Sunucudan gelen oyun durumu eski biçimli olabileceği için istemci her dizi alanını varsaymak yerine doğrular.


### H640 — Taş oyunlarında "Masayı düzenliyorsun" yüzen ögeleri masayı örtüyordu (2026-11-20)
- **Belirti:** Masa düzenleme kipinde ekranın ortasında/altında yüzen kutular perleri kapatıyor, düzenleme yapılamıyordu.
- **Kök neden:** İki katman üst üste: (1) `.om-duzenserit` `position:absolute; bottom:8px` ile masanın (om-masa, %100 yükseklik) alt perlerinin ÜSTÜNE biniyordu; dar ekranda düğmeler sütun kipine geçip şeridi büyütüyordu. (2) `duzenleBasla`/`masaTasDokun` 2–3 satırlık uzun 'bilgi' baloncuğunu (`.om-bildirim`, ıstakanın üstünde mutlak) 4,6 sn boyunca masanın üstüne basıyordu.
- **Kalıcı çözüm:** Şerit akışa alındı (sahne `:has(.om-duzenserit)` iken sütun flex; masa kalan yüksekliği alır), yönerge kısa metin olarak şeridin içinde; uzun düzenleme baloncukları kaldırıldı.
- **Önleme:** Oyun sırasında etkileşim gerektiren alanın (masa, ıstaka) üstüne mutlak konumlu kalıcı/uzun öge konmaz; kip göstergesi akışta yer kaplar, yönerge tek satır.
