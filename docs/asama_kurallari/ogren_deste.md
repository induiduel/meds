# Aşama kuralları — ogren_deste

> ÜRETİLMİŞ DOSYA: elle yazma. Kaynak `docs/KURUL2_YAPILMAYACAK_HATALAR.md`, üreteç `scripts/hat/tam_hat/kural_secici.py`. 32 madde. Tek satırlı maddeleri betik denetler (tam metin: `kural_secici.py --tam <H no|aşama>`).

### H64 — Sayfa haritası adım numaraları tekrar sayfalarını saymıyordu; kısa/eksik kanıt (2026-10-26, k2-22 psikosomatik)
- **Çözüm / kural:** Harita `adimlar`ı daima son destenin içerik slaytlarının `pdfSayfalari`ndan türetilir (checkpoint/oyun hariç); başlık `adimlar` = kapsadığı sayfaların ilk/son içerik adımı. Metinsiz görsel sayfada `kanit: {sayfa, gorsel: "≥4 kelime görülen"}` kullanılır; alıntı kaynak.md'de birebir geçen ≥4 kelime olur.


### H67 — H64 tekrarı: harita adımları checkpoint'siz sayıldı + deste `bolum` alt başlık numarası (2026-10-26, k2-26 nörolojik hastalıklar genetiği)
- **Çözüm / kural:** Harita `adimlar` daima deste `slideNumber`'ıdır; `bolum` yalnız `basliklar[].no` değerlerinden biri olur (alt başlık yoksa ana no). Kayma görülürse hangi tarafın doğru olduğu sayfa `ne_anlatiliyor` ile slayt başlığı karşılaştırılarak seçilir; içindekiler/kapak sayfası hiçbir adımın `pdfSayfalari` aralığına girmez.


### H89 — Canlı yarışma odası sorusuz kuruluyor, oyun hiç başlamıyordu (2026-10-27)
- **Kural:** realtime odası veri olmadan kurulamaz; sunucu her başarısız katılımı açık hata mesajıyla döner.


### H105 · Harita `adimlar` = deste `slideNumber` (checkpoint dahil); iskelet ajanı içerik adımlarını 1..N saydı (2026-10-27, k2-08)
- **Kural:** Harita deste birleşmeden planlı sayıyla yazılır; birleştirmeden sonra slideNumber'a çevrilir ve `denetle.py` yeniden çalıştırılır (TALIMAT §1b'ye not eklendi).


### H113 · KMB video oynatıcısı takılıyor, yazılar üst üste biniyor (2026-10-27)
- **Kural:** Sesle eşlenen animasyonda ses ağdan parça parça konumlanmaz (blob/önbellek); saat sert değil yumuşak eşlenir. Stil dosyasına
  "vN: önceki kuralları ez" katmanı eklenmez — kural yerinde değiştirilir; üst üste binen öge eklerken mutlak konumlu her katmanın yeri tek yerde tanımlanır.


### H121 · Sınama (test) Öğren dersi gerçek Kurul 2 dersleriyle aynı listede görünüyordu (2026-10-27, k2-07 Genel Anestezik İlaçlar)
- **Kalıcı çözüm:** kitaplıkta `sinama` işaretli desteler ayrı "Sınama — test verisi" bölümünde, en sonda gösterilir. Önleme: yeni listeleyen her ekran `sinama` alanını bölüm ayrımı için kullanır; gerçek PDF gelince `yayinla.py` aynı kimliği günceller ve `sinama` alanını bırakır (H97/H99 sırası).


### H459 — KMB (Üretral kateter): küçük video, tekrar eden altyazı, iptal edilemeyen otomatik geçiş, metin hataları, hata takibi yok (2026-10-31)
- **Önleme:** KMB'de yeni ekran düzeni viewport değil `@container kmb` ile seçilir; otomatik geçiş yalnız oynatıcının
  iptal edilebilir `otoSonraki`'si ile yapılır. Hocanın sözü cümleye çevrilirken derecelendirme ("en önemli", "göreceli",
  "hata ama sorun değil") korunur; anlatımda vurgulanan her uygulama eylemi OSCE akışında ayrı basamaktır. Her yeni sınav
  ögesi `adim` taşır (yoksa dogrula.py HATA). Şık açıklamaları `sik_aciklama.denetle` ile 0 HATA.


### H460 — KMB Lottie videoları: kesik/taşan etiketler, kayan kamera, yanlış durumdan başlayan sahneler, sonsuz sayaç (2026-10-31)
- **Önleme:** Video değişikliğinden sonra `node meds/scripts/uretim/kmb/kare_onizle.mjs [ad…]` ile temas sayfası üretilir ve her
  cümle karesi metinle karşılaştırılır (rapor.json otomatik bulgu 0 olmalı). Etiket ≤30 harf; önemli öge (torba, meatus,
  kan) sahnenin alt %24'üne konmaz; alt kompozisyonda "son durum" gerekiyorsa `'once'` kullanılır, None değil.


### H461 — KMB video oynatıcı: tek dokunuş oynatmayı durduruyor ya da 10 sn sarıyordu (tam ekran dahil) (2026-10-31)
- **Önleme:** oynatıcıda görünmez tıklama bölgesi tek dokunuşta oynatma durumunu ya da konumu değiştirmez; konum/oynatma
  değiştiren tek dokunuş yalnız görünür düğmededir ve görünür düğme çift dokunuş bölgesine (kenar %35) taşmaz. Jest
  kuralları başsız Chrome dokunma olaylarıyla sınanır (26 senaryo: tek/çift/üçlü dokunuş, basılı tutma, kaydırma,
  tam ekran, fare). Tam ekran/sabit katmanlar `[role=dialog]` taşıyorsa genel max-height'ı kapatır (H461, hucrem.css örneği).


### H462 — KMB Hedefler filmi: yakınlaştırma ayrıntıyı kesiyordu; 3B deneme (Pixar/organik) kalite eşiğini geçemedi → ARŞİV (2026-11-01)
- **Önleme (2B yeniden çizim için KESİN kurallar):** ① hiçbir parça diğerinin içine girmez (katmanlar kesişmez, önde olan
  arkadakini düzgün örter); ② ölçekler anatomiye uyar (16 Fr ≈ 5 mm; üretra ~1 cm; balon 10 mL ≈ 2,7 cm); ③ sıvılar
  (idrar, izotonik, jel, antiseptik) yarı saydam/parlak ve yüzeye yapışık gösterilir, katı halka/boncuk olmaz; ④ bakış
  açısı anatomiye göre seçilir (sagittal kesit yandan, vulva önden litotomi, mesane içi üstten) ve kadraj hiçbir anlatılan
  ögeyi kesmez; ⑤ her öge adıyla ayırt edilir (neyin ne olduğu belirsizse çizim yeniden yapılır); ⑥ önizleme
  gerçek vuruş durumuyla alınır (`sahne3b_onizle.mjs --film`, SVG için de çalışır), "tüm ögeler açık" karesi yalnız
  kimlik denetimi içindir; ⑦ her sahne yayından önce kare temas sayfasıyla göz denetiminden geçer.


### H465 — KMB 2B Erkek sahnesi: sırtüstü gövdede iç organlar "ayakta" dizilimindeydi (mantık hatası) (2026-11-01)
- **Önleme:** Her kesit sahnesinde önce yön sistemi yazılır (kod yorumunda: "inferior = …, anterior = …"), her organ
  bu sisteme göre yerleştirilir; "ayakta şema" başka duruşa KOPYALANMAZ. Tutulması gereken şey tutulur (el çizilir),
  gövde kadrajda kesilmez (uyluk/örtü ile tamamlanır), sıvı davranışı duruma bağlıdır (kateter yerleşmeden idrar akmaz).
  Kural `docs/KMB_2B_STIL.md` §2-3/§2-6; önizleme `sahne3b_onizle.mjs --film` ile gerçek vuruş durumunda bakılır.


### H497 — KMB Lottie: çarpı "Z" çiziyordu; çok alt yollu SVG tek şekle birleşiyordu (2026-11-05)
- **Çözüm/önleme:** `yol` çok-M yolu alt yol başına ayrı `sh` listesi döndürür, `G` listeleri düzleştirir; `carpi` iki ayrı kol çizer. 02 (eski + 2B) videoları yeniden üretildi.


### H498 — KMB: ata grupta transform olan sahnede kutular (bbox) 60 px kaydı (2026-11-05)
- **Çözüm/önleme:** ikisi de kutuyu `svg.getCTM()⁻¹ · el.getCTM()` ile sahne köküne çevirir. Sahnede grup kaydırması serbest; kutular hep kök koordinatında.


### H499 — KMB: clipPath'li sıvı Lottie'de dikdörtgen olarak organ dışına taştı (2026-11-05)
- **Çözüm/önleme:** sıvı organ biçiminde açık yol olarak çizildi. Kural: Lottie'ye gidecek KMB sahnelerinde `clipPath`/`mask`/`filter` kullanılmaz; biçim yolla verilir.


### H500 — KMB: altyazı bandı (alt %24) kesitteki ana yapıları örtüyordu (2026-11-05)
- **Çözüm/önleme:** anatomi 70 px yukarı taşındı, alt yapılar kadraj altına uzatıldı. Yeni KMB sahnesinde anlatılacak yapılar y ≤ 380 içinde çizilir.


### H523 — Taş Masası: "Oyunu başlat / masa kur" bazen hiçbir şey yapmıyor, hata da görünmüyordu (2026-11-10)
- **Çözüm/önleme:** `istemci.ts`: `gir`/`ping` dışındaki mesaj yalnız `baglanti === 'hazir'` iken gider; hazır değilse kur/katıl/başlat/sonraki el kuyruğa girer, `girdi` gelince (gerekirse önce masaya geri oturularak) gönderilir; hamle gönderilemezse hata bildirilir. Yanıt beklenen her istek `bekliyor` durumuna yazılır → `MasaBekleme` (kurma/katılma/dağıtım tam ekran, hamle küçük hap) ve 15 sn yanıtsızlıkta hata + soket yenileme. `sunucu.ts`: kimliksiz mesaja `kimlik-bekle` hatası döner. Kural: istemci–sunucu sözleşmesinde **hiçbir istek yanıtsız düşmez**; sunucu ya durum ya hata döner, istemci her bekleyen isteği görünür kılar ve zaman aşımına bağlar.


### H524 — Taş Masası: Taş Domino masası açılır açılmaz "Cannot read properties of undefined (reading 'length')" ile çöküyordu (2026-11-10)
- **Çözüm/önleme:** erişim `o.cezalar?.length` yapıldı (cezası olmayan oyun = boş liste). Kural: yeni oyun türü eklenirken `tasMi`/`as OkeyGorunum` geçen her yer gözden geçirilir; ortak kabuk bileşenleri oyuna özgü görünüm alanlarını (`cezalar`, `atiklar`, `acti`) yalnız isteğe bağlı erişimle okur, `as` dökümüyle alan varsayılmaz.


### H525 — Taş Masası: başlamış masaya gelen arkadaş geri çevriliyor, kopmalar görünmüyordu (2026-11-10)
- **Çözüm/önleme:** `sunucu.ts`: oyun sürerken gelen bağlantı izleyici olur (`izleyici` haritası, `gorunum(…, null)` ile gizli bilgi açılmaz), `koltukIste`/`koltukVer`/`koltukRed`; koltuk devri `oda.devir` (bağlantı kimliği → koltuk kimliği, motor durumu değişmez, her kimlik okuması `sid()` üzerinden); kopan koltuğun anı `kopZ` → görünümde `kopSn`; yanlış yazılan kod (O/0→D, I/1→L/J/T) var olan odaya eşlenir. İstemci: davet kodu `sessionStorage`'da girişe dek saklanır; `deneme`/`sonrakiDeneme` → `MasaBaglanti.tsx` katmanları. Kural: masaya gelen hiçbir kişi açıklamasız geri çevrilmez; bekleyen her durum (kim, ne kadar, ne yapılabilir) ekranda yazılır. Sınama kancası `window.__masaTest` yalnız `?masatest` kipinde.


### H526 — Taş Masası: Remi/Kastet düzenlemede elden taslağa konan taş geri alınamıyordu (2026-11-10)
- **Çözüm/önleme:** `OkeyMasa.tsx` `duzen.onTas`: el taşına (`elMap`) dokununca gruplardan çıkar → ıstakaya döner; masa taşı seçilir. Taslak araçlarında her eklemenin tek tek geri alma yolu olmalı.


### H527 — Taş Masası: dar ekranda eylem düğmeleri 3–4 satıra yığılıyor, durum yazısı "Sıra…" diye kesiliyordu (2026-11-10)
- **Çözüm/önleme:** dar kipte tek satır, simge üstte kısa yazılı, yatay kaydırılan düğmeler; durum yazısı sarar ve en az 150 px; oyun sırasında `html.mk-oyunda .nb-wrap` gizli (bağlantıyı masa gösterir). Yeni eylem eklerken 375×740'ta sayfa_tarama/senaryo ile bakılır.


### H528 — Taş Masası: lobide mod seçenekleri "NormalZorlu", "KlasikYığma7-0AtlamaHızlıÇek-çek" diye bitişik yazı olarak görünüyordu (2026-11-10)
- **Çözüm/önleme:** ortak `ModSecici.tsx` (`OyunModu`, `UnoModu`: başlık + kısa tanıtım kartları, seçili işaret) hem lobide hem kurulum yaprağında; bot kurulumu `asistan`/`unoMod`/`tasSayisi` gönderir. `lobi.css` + `kurallar-gorsel.css` (liste imleri açık, numaralı `mk-adimlar`). Kategoriler ve sıra tek kaynakta: `oyunKatalog.ts` (merkez kartları, kural sekmeleri, kısayollar). Kural: TSX'e yeni `mk-*` sınıfı yazınca aynı işte CSS'i de yazılır; `grep -rn "<sınıf>" src/styles` boşsa iş bitmemiştir. Yeni ayar lobiye eklenirken bota karşı kurulum yaprağına da eklenir.


### H529 — Taş Masası: tüm oyunlarda hamleler gecikmeli görünüyordu (2026-11-10)
- **Önleme:** Yeni oyun/hamle eklenince `tahmin.ts`'e kesin bilinen kısmı eklenir ve aynı karşılaştırma koşulur; ekran hiçbir zaman ağ yanıtına kilitlenmez. Okey per açma/işleme/çekme hâlâ sunucuyu bekler (ıstaka düzeni + gizli taş). Ağ tarafındaki sıçramalar için kalıcı çözüm ancak WS'yi tünelden ayırmaktır (ayrı alt alan, Cloudflare/Oracle erişimi kullanıcıda).


### H533 — Taş Masası: dar ıstakada grup toplamı yanlış; Go/XOX botu hiç hata yapmıyordu (2026-11-10)
- **Önleme:** Istaka düzeni değiştiren her işlev grupları korumalı; grup toplamını gösteren her ekran dar boyutta (`yuva_t` sınaması: 21 taş 6 grup, sütun 16/14) denenir. Bot ekleyen her oyuna zorluk seçeneği verilir; "kusursuz bot" yalnız Zor'da. Sınama `tahta.sinama.ts` (kolay bot 40 elde ≥5 kayıp).


### H534 — Taş Masası: masadaki taş eldeki taşlarla yeni pere katılamıyordu (2026-11-10)
- **Önleme:** Masaya taş koyan her oyunda "masadan taş + elden taş = yeni per" senaryosu motor sınamasında bulunur (`yedili.sinama.ts`, `yuzbir.sinama.ts` düzenle bölümleri). Bir hamle türü bir oyuna eklenince aynı masa modelini paylaşan öteki oyunlar (yedili/takım/101/kastet/remi) birlikte gözden geçirilir.

### H535 — Taş Masası: masayı düzenlerken perler boşalan yere kayıyordu (2026-11-10)
- **Önleme:** Kullanıcının elle düzenlediği alanda (masa taslağı, ıstaka) öğeler kendiliğinden yer değiştirmez; düzen yalnız kullanıcının açık isteğiyle (Sırala, Masayı diz) değişir. Sınama: düzenlemede taş alıp per boşaltınca komşu perin `getBoundingClientRect().left/top` değeri değişmemeli.


### H542 — Uno'ya 10 yeni mod eklenirken motor sınamasının yakaladığı dört kural hatası (2026-11-10)
- **Önleme:** Uno'ya kural/kart ekleyen her değişiklikte `npx tsx src/services/masa/motor/uno.sinama.ts` ve `unoMod.sinama.ts` 0 hata vermeli: her mod için birim senaryolar + bütün oyuncu sayılarında hepsi-bot rastgele eller (kart korunumu, tıkanmama, gizlilik, puan toplamı) + bulanık hamle. Yeni bir "bekleyen karar" ya da el sayısını değiştiren etki eklenince korunum denetimine (`korunum`) ve `sonIslem` UNO taramasına dahil edilir. Arayüz: `meds_temp/uno_ui/uno_ui.mjs` (başsız Chrome, `?masatest`, 12 mod × telefon dikey/yatay, tablet, masaüstü; taşma, dokunma hedefi, konsol hatası). Başsız sınama çıktısı `/tmp/claude-1000` kotasına yazılmaz (EDQUOT ile yarıda kesildi), `meds_temp` altına yazılır.



### H544 — Ek modül içeriği hocanın materyali sorulmadan yazıldı; çalışma soruları gelince 16 konunun tamamı yeniden yazıldı (2026-11-10, Yürüyüş ve Kampçılık)
- **Önleme:** yeni ek modülde ilk iş hocanın materyalini istemektir (AGENTS kural 30). Hocanın kendi içinde çeliştiği cevaplar (kazık 45°/90°, tuvalet 50/150 m) sessizce "düzeltilmez": en çok yinelenen değer esas alınır, ekrana "ikisini de bil" notu düşülür ve kullanıcıya raporlanır. Hocanın bilimsel olarak tartışmalı ifadesi (baştan %50 ısı kaybı, gnays kristalleri) hocanın dediği gibi kalır; metin ona aykırı yeni iddia eklemez.


### H546 — Ek modülde sesli ders PDF'le birlikte ilerlemiyordu; eşleme kurulurken iki ölçüm tuzağı (2026-11-10, Yürüyüş ve Kampçılık)
- **Önleme:** ek modülde ses ya da ders kitapçığı yeniden üretilince `pdf_esle.py` yeniden çalıştırılır; `dogrula.py --modul` eşleme eskimişse (klip özeti ya da PDF boyutu tutmuyorsa) HATA verir, ekran da özeti tutmayan klibin eşlemesini kullanmaz. Karşılığı bulunamayan cümleye madde uydurulmaz (yalnız bölüm çerçevesi; kural 17'deki "çapa uydurma" yasağıyla aynı ilke).


### H552 — Sesli çalışma sorularında boşluk doldurma "boşluk" diye okunuyordu (2026-11-10, ek modül)
- **Önleme:** `dogrula.py --modul` boşluklu (`__`) her hoca sorusunda `okunus` yoksa ya da soru işaretiyle bitmiyorsa HATA verir. Yeni boşluklu soru eklenirken (her modülde) okunuş elle, doğal soru cümlesi olarak yazılır; mekanik "boşluk/ne" değişimi yapılmaz.


### H574 — Oyun masasında 13 kez çökme: `oyuncu.cezalar` olmayan eski oyun durumu (2026-11-14, kullanıcı "bu tarz hataları da çöz" dedi)
- **Önleme:** `?.` **alan** korur, **dizi metotlarını** korumaz: `X.filter(...)` öncesi `Array.isArray(X)` sınanır. Sunucudan gelen oyun durumu eski biçimli olabileceği için istemci her dizi alanını varsaymak yerine doğrular.



- H587 — Öğren destesinde 16 klip 14–22 dakika sürüyordu; ses için kalite kapısı yoktu (2026-11-16) — betik denetler: `ses_kapisi.py`
### H640 — Taş oyunlarında "Masayı düzenliyorsun" yüzen ögeleri masayı örtüyordu (2026-11-20)
- **Önleme:** Oyun sırasında etkileşim gerektiren alanın (masa, ıstaka) üstüne mutlak konumlu kalıcı/uzun öge konmaz; kip göstergesi akışta yer kaplar, yönerge tek satır.

