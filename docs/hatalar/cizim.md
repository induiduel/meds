# Hata defteri — cizim (canlı çizim, çapa, lazer, panel, PDF işareti)

> Tam metin (kelimesi kelimesine taşındı, 2026-11-16). Dizin: `docs/KURUL2_YAPILMAYACAK_HATALAR.md`.
> Yeni madde bu dosyanın SONUNA `## H<n> — …` başlığıyla eklenir + dizinin sonuna tek satır.

## Canlı ders PDF işareti (2026-10-20)

- **Tahminle vurgu yok:** Kurul 1'de konuşma metni slayttan yeniden yazıldığı için okunan cümlenin slayttaki karşılığı
  kelime örtüşmesiyle tahmin ediliyordu; komşu madde yanıyor ya da hiçbir şey yanmıyordu. Kurul 2'de her `konusma_v2`
  cümlesi `slayt: {sayfa, satir[], sekil}` çapası taşır: `satir` `kaynak.md`'den **birebir** kopya (kapı: `konusma_v2.py
  --dogrula` her satırı o sayfanın metninde arar; çapasız cümle en çok %25). `ses` cümlesi maddenin terimlerini aynı
  sırayla kullanır. Akış: `--turet` → `konusma_capalari.json` → `yayinla.py` (`capalar`) → `data/sesli_anlatim/capa/<key>.json`
  → `pdf_isaret.py` (madde + kelime kutuları) → `isaret/<key>.json` → canlı ders.
- **Kurallar (kullanıcı):** slayt maddesi ancak içeriğinin ≥%80'i okunan cümlede geçiyorsa zeminle işaretlenir; konuşulan
  her kelime hem metinde hem PDF'te anlık işaretlenir (PDF'te yalnız karşılığı olan kelime); lazer imleci yalnız metni
  olmayan yerde (resim/şema, `sekil`). Kelime anı sesten ölçülen konuşma parçaları (`cumle_zaman.py` surum 2, `k`) ve hece
  sayısıyla bulunur; sessizlik kelimelere paylaştırılmaz, işaret animasyonsuz.

---

### H15 — Sesli ders + slayt ekranında slayt okunan bilgiye gitmiyor, kelime vurgusu yok (TBG kampı, 2026-10-20)
- **Kök 1:** PDF görüntüleyici (`PdfDocView`, `.pdv { flex: 1; overflow: auto }`) esnek sütun olmayan bir kaba konmuştu;
  görüntüleyici içeriği kadar uzadı, kendi içinde kaydırılamadı, başlık "slayt 14" derken ekranda 1. sayfa kaldı.
- **Kök 2:** kelime zamanları dosyası (`src/data/genetik_kamp/kelime.json`) boş yayına girmişti; kelime vurgusu hiç çıkmadı.
- **Kural:** `PdfDocView`'u saran kap `display: flex; flex-direction: column` ve yüksekliği sınırlı olur. Sesli metin + slayt
  ekranı yayına girmeden kelime dosyasının her cümlede kelime sayısı ekran bölmesiyle (`/\S+/g`, `**` silinmiş) birebir
  tuttuğu denetlenir (0 eksik); yeniden üretim: `meds_temp/spot_cozucu/genetik/g07_yeni/kelime_esle.py`.
- **Ekran tam ekranı:** uygulama kabuğunun altında kalan sabit (`position: fixed`) katman çubukların altında kalır; tam
  ekranda bileşen `body`'ye taşınır (portal), yerel tam ekran `document.documentElement` için istenir.

## H40 — Canlı çizim çizgileri görünmüyor, amaçları anlaşılmıyordu (2026-10-24, kullanıcı ekran görüntüsü s.14 herniasyon)
- İnce (1,5 px) yarı saydam mavi çizgi resim/renkli zeminde kayboluyordu; okların çoğunda etiket yoktu (k2-02'de 34 okun 15'i),
  öğrenci okun neyi anlattığını çıkaramıyordu; resimdeki mevcut okları kopyalayan anlamsız dirsekler çiziliyordu.
- Düzeltme: her çizginin altında beyaz hale (5,5 px), çizgi 2,4 px tam opak, hedef çerçevesi 2 px; **etiketsiz ok reddedilir**
  (`cizim_uret`: "etiketsiz ok"); etikete boş yer yoksa yolun ortasına koyu hap olarak konur (gizlenmez).
- Birden çok terim aynı sonuca gidiyorsa tek ok değil, alt alta dizilip "}" ile toplanır (şema grubu, `CizimLayer.Sema`).

## H41 — Yazı satırları arasına çizilen oklar kötüydü; tek tip panel yetmiyordu (2026-10-24, kullanıcı s.18)
- "Koma nedeni alkol ?" ile "SAK – SUBDURAL" arasına 1 % boyunda ok çizilmişti: görünmüyor, ilişki anlaşılmıyordu.
- Düzeltme (`cizim_uret.oku_panele`, `panel_tipi`; `CizimLayer.Sema`): iki ucu da yazı satırı olan ok, sayfanın boşluğunda
  ilişkiyi canlandıran panele çevrilir. Panel türleri yapıdan seçilir: **zincir** (A→B→C, çizgi uzayarak), **grup** (çok →
  bir, "}"), **dal** (bir → çok, karar), **maske** (görünen neden; perde kalkınca altta aranacak), **karşıt** (iki kutup).
  Akış şeması kutularındaki 1–2 kelimelik parçalar düğüm olmaz; PDF simge madde imleri ve parantezli ara söz atılır.
- Resimde şeklin kendi okunu kopyalayan kısa ok çizilmez; şekildeki ok **çerçevelenip etiketlenir** (`odak`).
- Bir kaynaktan birden çok yere giden ilişki **dallı ok** olur (`dallar` ya da aynı kaynak kutusu): kaynak kesik çizgili
  turuncu çerçeveyle bir kez gösterilir, dallar konuşma boyunca sırayla çizilir.

## H42 — Okun başlangıcı belirsizdi; resimdeki bölge vurgulanmıyordu (2026-10-24, genel kural)
- Kullanıcı: "okların başlangıç noktası belirsiz", "resimlerde marker ile boyama yapılıp hatlar belirginleştirilebilir";
  "bu derse özgü değil, genel kural". Düzeltme: her okun kaynağı çerçevelenir (kutu yoksa halkalı turuncu nokta); `kontur`
  yarı saydam sarı fosforlu dolgu + kırmızı hatla çizilir. Genel kurallar listesi: `scripts/uretim/cizim/TALIMAT_CIZIM.md`.

## H43 — Panelde bağımsız iki ilişki tek zincir gibi okunuyordu (2026-10-24, s.43)
- "uzamış kanama zamanı → intrakraniyal kanama" ve "trombositopeni → kanama, sepsis" aynı satırda bitişik dizilince
  intrakraniyal kanama ile trombositopeni bağlıymış gibi anlaşıldı. Düzeltme: `CizimLayer.Sema` bağlı bileşenlere böler,
  her bileşen ayrı satırda kendi türüyle; araya kesik ayraç. Ek kurallar: dallı ok sayfada ortak gövdeden çıkar; çizgiler
  yumuşak ve sürekli uzar. Kurallar `TALIMAT_CIZIM.md` "Genel çizim kuralları" 1–13 (bütün dersler).

## H44 — Sayfaya sığmayan panel gizleniyordu (2026-10-24, kullanıcı kararı)
- Dolu slaytlarda panel "yer yok" diye hiç gösterilmiyordu (k2-02'de 3 panel). Düzeltme: `cizim_uret` panel için
  `ek_alt` + `ek_renk` yazar; `PdfDocView` (`ekAlt`) o sayfanın altına slaytın alt kenar rengiyle alan ekler (`.pdv-page-ek`),
  panel oraya oturur. Sayfa kutusu ve işaret koordinatları aynı kalır (y > 1 yalnız panel için), "şu an anlatılan" çerçevesi
  ve sayfa numarası ek alanı da kapsar, gece kipinde ek alan sayfayla birlikte tersine çevrilir. Ek alan ders boyunca
  sabittir (anlatılan cümleye göre değişip sayfaları kaydırmaz).

## H45 — Dar bölmede panel slayta göre büyüyor, yazının üstüne biniyor, kelimeler harf harf kırılıyordu (2026-10-24)
- Gerçek görüntüleyicide (Metin + Slayt, ~570 px sayfa) panel yazısı sabit px idi: panel slayta göre iki kat büyüyor,
  ayrılan boşluktan taşıp yazının üstüne biniyor, dar düğümde kelime harf harf kırılıyordu; panel yüksekliği tahmini de
  gerçeğin ~1,5 katı kısaydı. Düzeltme: panel/etiket boyu `cqw` (sayfa genişliğine oranlı), etiketler SVG'den HTML'e alındı
  (oransız ölçekte bozuluyordu), betikte `panel_boyu` (istemci diziliminin em kopyası). Sınama: 35 panelin hepsi 567 px ve
  1100 px sayfada ayrılan alana ve sayfa/ek alan sınırına sığıyor (sınama sayfası tarayıcı ölçümü).

## H46 — Telefonda panel yazısı okunmayacak kadar küçüktü; panel kelime kenarına biniyordu; ek alan şişiyordu (2026-10-24)
- Kullanıcının telefon görüntüleri eski önbellekli sürümdendi (ek alan yok, sabit px yazı). Güncel sürümde telefonda panel
  yazısı 5 px kalıyordu → %2,2 cqw. Boşluk eşiği %3 mürekkep bir kelimenin kenarını kaçırıyordu → %1 + 0,012 pay.
  Bir sayfanın ek panelleri üst üste diziliyordu (ek alan sayfanın 1,24 katı) → aynı yeri paylaşır, tam genişlik.
  Grup/dal tahmini uzun düğüm kırılmasını saymıyordu → `panel_boyu` sütun genişliği + satır sayısı.
- Sınama: 35 panel 366 / 567 / 1100 px sayfada ölçüldü (taşma 0); gerçek uygulamada 420 px telefon görünümünde s.11.

## H47 — Kelime takipçisi küçük yazıyı okunmaz yapıyordu; ek alan gereğinden sık ve uzundu (2026-10-24)
- Telefon görüntüsü (s.54): konuşulan kelimenin iç gölgesi (3 px) ve koyu zemini "serebral" kelimesinin harflerini kapattı.
  Düzeltme: zemin .13, çizgi harflerin altında (2 px, dışarıda).
- Ek alan her sığmayan panelde baştan açılıyor ve panelin tamamı kadar oluyordu. Düzeltme: panel slaytın alt boşluğundan
  başlar, sayfa yalnız taşan kısım kadar uzar (en büyük ek 0,58 → 0,39 sayfa boyu; s.11'de ek alan hiç gerekmedi).
  Zincirde okun etiketi yanındaki düğümün altına girip kesiliyordu → etiket okun üstünde akış içinde, ok büzülmez.

## H49 — Kırılan zincirde ok yana bakıyordu; panel yazısı büyüktü; takip 8–16 sn duruyordu (2026-10-24)
- "beyin omurilik sıvısı incelemesi → santral sinir sistemi enfeksiyonu" satıra kırılınca ok yana bakıyordu → panel sürümleri
  (yatay/dikey × normal/kompakt), kırılan yatay zincir geçersiz → dikey (oklar aşağı). Panel yazısı %2,2 → %1,75 cqw.
- Canlı tarama (masaüstü, 2×): anlatılan satır 8–16 sn oynatıcı altında kalıyordu. Kök: satırı görünür alana alan program
  kaydırması kullanıcı gezinmesi sayılıp takibi 8 sn durduruyordu → program kaydırması bildirilmez.
- Bütün kurallar tek belgede: `docs/CIZIM_KURALLARI.md` (her kurul, her ders, her PDF).

## H50 — Panel tıbben yanlış okunuyordu; takip kaydırması sessizce boşa gidiyordu; ekran kalabalıktı (2026-10-24)
- "üremik ensefalopati → istenir → üre, kreatinin", "glukoz —hızla geri döndürür⊣ hipoglisemi": ok yönü/işareti anlamı
  bozuyordu. Düzeltme: anlam şablonu kütüphanesi (`scripts/uretim/cizim/sablonlar.json`, `sablon.py`), yönsüz eşleşmeler başlıklı
  tablo; yeni şablon önerisi kütüphaneye eklenir; bağımsız tıbbi anlam denetimi (tamam/düzelt/sil). Numaralı/madde imli
  liste, kesikli satır/sütun ayracı.
- Takip: tarayıcının `scroll-behavior: smooth` kaydırması PDF kapsayıcısında ilerlemiyordu; hesap sayfa geometrisinden
  yapılıp ölçek katmanında ekranla uyuşmuyordu; program kaydırması kullanıcı gezinmesi sayılıp takibi durduruyordu →
  kare kare kaydırma + süre dolunca doğrudan, ekrandaki gerçek konumdan ölçüm, program kaydırması bildirilmez. Ölçüm:
  2× hızda 7 dk'da örtme 8–16 sn → 0,6 sn.
- Ekran: izleme düzeni (anlatılmayan paragraflar soluk, özet kutuları kapalı; slayt %60).
- (2026-10-24) Şablonlu tablo, eski hizalı ilişki düzeninin `is-tablo` sınıfını paylaşıp ızgara düzenine giriyor, sabit düzenli
  tablo Chrome'da 1.000.000 px genişliğe çıkıp ikinci sütun panelin dışında kalıyordu (panel kutusu ölçümü bunu görmüyordu).
  Düzeltme: eski kural `:not(.pdv-sb)`, panel blok düzen, tablo/karşıta ayrılan genişlik doğrudan; sınamaya iç taşma (hücre
  sağ kenarı) eklendi. Telefonda kompakt sürüm 7,5 px sınırı yüzünden küçülemediği için boy tam ölçekle tahmin edilir (%32 pay).

## H51 — Resim slaytında anlatım görselin yerine panelde; yatay zincirde kutular kırılıyordu; testler bunları görmüyordu (2026-10-24)
- Herniasyon şeması anlatılırken altta 5 öğeli yatay zincir paneli; kutular 3–4 satıra kırılıp panel sayfadan 333–692 px
  taşıyordu. Maske paneli "Görünen: Alkol" anlamsızdı. Grup panelinde numaralar basılmıyor, ok sözü kesiliyordu.
- Kök: sınama yalnız panel kutusunun taşmasını ölçüyordu (iç taşma, satır kırılması, kesik söz yoktu) ve elle yapılıyordu.
- Düzeltme: `resim_sayfasi` kapısı (görsel slaytta panel yok; 7 sayfa Claude ile görselin üstünde yeniden çizildi), yatay zincir
  tek satır yoksa dikey, maske "İlk izlenim / ⚠ maskeleyebilir / Atlanmaması gereken", liste numaraları, grup ızgarası.
  Kalıcı otomatik kapı `scripts/uretim/cizim/panel_sinama.mjs` (366/567/1100 px, 8 hata türü) ders zincirinde; düşen çizim yayına gitmez.

## H52 — Etiket çizimden kopuk; PDF'in kendi oku yeniden çiziliyordu (2026-10-24, s.14 ve s.27 görsel denetimi)
- s.14 "santral herniasyon" etiketi 3 numaralı okun yanında, "tonsiller" etiketi 6'dan uzakta; s.27'de slaytın kırmızı okları
  mavi okla kopyalanıyordu. Düzeltme: etiket önce hedef kutusunun (odak çerçevesi / boyalı bölge / ok ucu) hemen yanında
  aranır, uzaksa kesikli bağlantı çizgisi (`etiket_hedef`); uçları PDF aday okuna ya da a→b boyunca çizili hatta (kenar ≥%80)
  denk gelen ok yeni çizilmez, o ok çerçevelenir (`pdf_oku` → odak). k2-02: 9 ok çerçeveye çevrildi, 19/41 etiket bağlantılı.

## H53 — Resim üstündeki çizim asıl yapının önünü kapatıyordu (2026-10-24)
- Kullanıcı: "o bölgeye zoom yapılsın, çizilsin, geri dönülsün". Düzeltme: `cizim_uret.yakinlasma` → komutta `yakin`;
  `CizimLayer.yakinUygula` sayfa katmanlarını yumuşakça büyütür/geri döndürür (cümle başına tek birleşik hedef; ilk denemede
  iki çizim arasında gidip geliyordu). k2-02: 25 çizimde (10 sayfa) yakınlaşma; yerelde gerçek ekranda ölçüldü.

## H59 — Arşiv derslerinde lazer resim ve tabloları göstermiyordu (2026-10-25, kullanıcı, 2025-26 Kurul 2)

- **Belirti:** 33 arşiv dersinde 6.023 cümlenin yalnız 169'u resme, 17'si tabloya işaret ediyordu; şekil anlatılırken
  lazer yazı satırında duruyordu.
- **Kök:** (1) `uygula_lazer_takip.py` "%98–100 kapsama" için her cümleye en yakın maddeyi (bulamazsa M0) ve görselli
  sayfada `resim: 0` basıyordu; (2) `pdf_isaret.capali_ic` maddeyi şekil çapasından önce işliyor, tek ortak kelimelik
  metin eşleşmesi de şekli eziyordu; (3) çapa şemasında tablo alanı, dökümde T# kutusu yoktu; (4) yinelenen R kutuları
  (aynı yere iki görsel) R0 = R1 karışıklığı yaratıyordu.
- **Kural:** şekil/tablo çapası maddeye üstündür; `madde`/`resim` dizini toplu betikle uydurulmaz; kapsama oranı
  çapayı düzelterek yükseltilir. Döküm (capa_dok, cizim dok) yalnız tekil R# ve yeşil T# kutularını gösterir.
- **Kapı:** `pdf_isaret.sekil_isareti` (şekil önceliği), `capa_dogrula.py` T# denetimi; `uygula_lazer_takip.py` çapa yazmaz.
- **Ek (2026-10-25, çizim):** şekil cümlelerinin yalnız 59/853'ü görsel üstünde çiziliyordu; çizimler lazerden başka
  sayfaya (paragraf sayfası) düşüyor, resim anlatılırken panel kuruluyor, yazı slaytının arkasındaki şablon/kart görseli
  "resim" sayılıp bütün slayt çerçeveleniyordu. **Kural:** her ders `scripts/uretim/cizim/cizim_kapisi.py` (K1–K9) 0 HATA olmadan
  yayına girmez; model talimatı `TALIMAT_CIZIM.md` 21–26; kapı gevşetilmez.

## H60 — Slayt Çizimlerinin Toplu Gösterilmesi ve Erken/Tekrarlı Çizim Hatası (`sayfaCizimleri` Yasağı) (2026-10-25/26, kullanıcı)

- **Belirti:** Kullanıcı ekranında aynı anda 3 farklı çizim birden gösteriliyordu (ör. Slayt 14'te falks, tentoryum ve transkalvaryal herniasyon aynı anda aktif). Ayrıca animasyon her yeni cümleye geçildiğinde baştan tekrar tekrar çiziliyordu ("Bir kere gösterilen animasyon tekrar tekrar gösteriliyor. Uygun cümle anlatılırken uygun konum işaretlenmeli, aynı anda 3 konumu işaretlemek ve tekrar tekrar işaretlemek hatalı").
- **Kök Neden:** `CanliDersDers.tsx` içinde `sayfaCizimleri` adında bir toplayıcı yazılmış ve o sayfadaki tüm cümlelerin `z` komutları tek bir dizide birleştirilip `cizim` olarak iletilmişti. Karakter ilerleme sayacı `c` her yeni cümlede `0`'dan başladığı için, sayfadaki tüm çizimler her yeni cümlede kaybolup `c >= k[0]` olduğunda baştan oynuyordu. Ayrıca henüz sırası gelmemiş ileriki cümlelerin çizimleri de ekranda erkenden görünüyordu.
- **Çözüm & Kural:**
  1. `sayfaCizimleri` kökten kaldırıldı. `marks.cizim` KESİNLİKLE VE YALNIZCA o an konuşulan cümlenin `(isr as any).z` verisidir.
  2. Bir slaytta birden fazla cümlenin çizimleri asla tek bir dizide toplanamaz. Yalnızca o an okunan cümlenin işaret ettiği tekil anatomi/bölge gösterilir.
  3. `CizimLayer.tsx` içinde `tamamlananRef` eklendi: Bir çizim `t >= 1` seviyesine ulaştığında cümle bitene kadar sabit kalır (`t = 1`), zaman dalgalanması veya re-render'larda tekrar baştan oynamaz. Komutlara stabil anahtar atanarak unmount/remount döngüsü engellendi.

## H61 — Üst Üste Çakışan ve İç İçe Geçen Çizgi/Kontur Hatası (2026-10-25/26, kullanıcı)

- **Belirti:** Slayt 26'da hasta figürü üzerinde hem "dekortike postür" hem de "kollar fleksiyonda" konturları aynı anda çizilerek iç içe geçmiş iki kırmızı halka oluşturdu ("Aynı anda iki çizginin iç içe geçmesi de hatadır, hem önceki çizimin yeri belirsizleşiyor hem de kullanıcı hangisinin ne olduğunu anlamakta zorlanır").
- **Kök Neden:** (1) `sayfaCizimleri`nin slayttaki ardışık iki cümlenin (C0 ve C1) çizimlerini aynı anda ekrana basması; (2) Aynı görsel üzerinde eşzamanlı çakışan veya iç içe geçen kontur koordinatlarının bulunması.
- **Çözüm & Kural:**
  1. Cümle bazlı çizim izolasyonu ile C0 bittiğinde "dekortike postür" kalkar, C1 başladığında "kollar fleksiyonda" gelir; asla aynı anda görünmezler.
  2. Tek bir cümlede veya aynı görsel üzerinde eşzamanlı çakışan/iç içe geçen koordinatlar YASAKTIR. Çizim kapısı (`cizim_kapisi.py`) çakışan konturları denetler.

## H65 — Tablo sayfasında tabloyu anlatmayan cümleye şekil/tablo çapası (2026-10-26, k2-23 cinsel kimlik)
- **Belirti:** `arsiv_yayinla.py` 4/6'da `cizim_kapisi.py` 1 HATA: `K1 P19.C3: şekil çapası var ama lazer sayfa (s.21)`.
- **Kök neden:** s.21 (organik/psikojenik karşılaştırma tablosu) paragrafındaki son cümle ("Çıkmışta da sorulduğu gibi… tıbbi durum ve kullandığı ilaçlar değerlendirilir") tablonun hiçbir satırını anlatmıyor (`satir: []`), ama yazar paragrafın tüm cümlelerine aynı `sekil`/`tablo: true` çapasını kopyalamıştı. Eşleşecek tablo satırı olmadığından lazer tabloya değil sayfaya düştü.
- **Çözüm / kural:** Şekil/tablo çapası yalnız görseli/satırı gerçekten anlatan cümleye yazılır; paragrafın sonraki cümlelerine kopyalanmaz. Tablo çapalı cümlede `satir` boşsa çapa yazılmaz. Düzeltme: o cümlenin `sekil`'i `null` yapıldı, `tablo` kaldırıldı (capa + v2 + taslak kopyaları, `sekil_cizim.py sus` ile aynı yöntem); kapı gevşetilmedi, yayın 0 HATA ile tamamlandı.

## H85 — Çizim önemli bölgeyi örtüyor, zoom yanlış/fazla, kelime ↔ kelime oku okumayı bozuyor (2026-10-27, kullanıcı bildirdi)
- **Belirti:** "İşaretlenen bölgeler tam anlaşılmıyor; çizimin boyutu ve yerleşimi önemli bölgelerin üstünü kapatıyor, zoom
  farklı yerlere yanlış ve fazla yapılıyor." Kelime ↔ kelime çizgisi istenmiyor; tabloda çizim/zoom istenmiyor.
- **Kök neden:** `CizimLayer` konturu 3,2 px sabit kalın + 6,8 px beyaz hale + %45 sarı dolgu + %22 dış karartma ile çiziyordu
  (yapı örtülüyordu); kontur noktaları yapının üstünden geçtiğinde kenar kesiliyordu. Zoom 2,4×'e kadar ve sayfanın %40'ına
  kadar bölgelerde, yazı kutusu içindeki çizimlerde de yapılıyordu; bir cümledeki birden çok çizimin birleşik kutusuna
  gidiyordu. Akış oku yazı satırları arasında da çiziliyordu. Tablo cümlesinde panel "kapsama" sayılıyordu (K3).
- **Çözüm:** kontur %8 dışa açılır, hale yok, dolgu %13 bulanık, karartma %10, kalınlık bölgeye göre 1–2,4 px; akış yalnız
  resim çiziminde (`yakin`); zoom ≤1,6×, ≥1,25× gerekmezse yok, bölge ≤%20; tabloda çizim yok (yalnız marker). Üretici
  (`cizim_uret.yakinlasma`) yalnız resimde ve ≤%20; kapı K10–K12; standart `KURUL2_DERS_STANDARDI.md` §4; metin takipçisi
  kapısı `takip_kapisi.py` (T1–T6).
- **Önleme kuralı:** okumayı bozan hiçbir çizim/zoom yayına girmez; yeni ders kapıları K10–K12 + `takip_kapisi.py` 0 HATA.
  Yayındaki eski derslerin verisi kapıda 36 ihlal gösteriyor; görüntüleyici aynı kuralları uygular, yeniden üretimde düzelir.

## H87 — Çizim doğrulayıcısının komut satırı Kurul 2 cümle kimliklerini ve resim kutularını tanımıyor; sarmalayıcı yanıltıcı 0 HATA verdi (2026-10-27, k2-02)
- **Belirti:** çizim parti ajanları `cizim_dogrula.py` CLI'sini çalıştıramayıp kendi sarmalayıcılarıyla "0 HATA" bildirdi; gerçek
  yerleşimde (`cizim_uret.py`) 69 adaydan 9'u reddedildi (8 kontur çizgi üstünde değil, 1 resim sayfasında panel).
- **Kök neden:** CLI `denetle()`'ye resim kutularını boş veriyor, `konusma_v2` cümle kimliklerini (`k2-02-c####`) parti biçimine
  (`P#.C#`) çevirmiyor. Ajanlar eksik bağlamla kendi kapılarını kurdu.
- **Çözüm / kural:** çizim için geçerli kapılar YALNIZ `cizim_uret.py` (yerleşim + doğrulama, gerçek kutu ve görüntüyle) →
  `cizim_kapisi.py` → `panel_sinama.mjs`. Parti ajanının kendi sarmalayıcı sonucu kanıt sayılmaz; reddedilen çizim
  yayına girmez (emin olunmayan yer çizilmez). CLI düzeltmesi açık iş.

## H91 — Çizim PDF'i önbellekte olmayınca bütün konturlar sessizce reddedildi (2026-10-27, k2-03/k2-04)
- **Belirti:** `cizim_uret.py` 14 konturun tamamını "sayfa görüntüsü yok" diye attı; panel_sinama `hazirla.py` IndexError ile çöktü.
- **Kök neden:** `capa_dok.py` ders PDF'ini indirme klasöründen (`meds_downloads/drive_root/<path>`) okur, `cizim_uret.py` ve
  `sinama/hazirla.py` ise yalnız `data/sesli_anlatim/.pdf_onbellek/<deck>_0_*.pdf` arıyordu. İşçisiz (elle) yayında önbellek
  dolmaz → belge `None` → raster yok → kontur doğrulanamaz ve sessizce elenir.
- **Çözüm:** ikisine de aynı yedek yol (indirme klasörü → `pdf_isaret.pdf_indir`); `cizim_uret` PDF hiç bulunamazsa durur.
- **Önleme kuralı:** bir hattaki bütün betikler kaynak dosyayı aynı yardımcıyla bulur; ret sayacında tek bir nedenin tüm komutları
  ataması (ör. "görüntü yok" = kontur sayısı) kapı hatası sayılır, yayına geçilmez.

## H93 — Çapa değişince PDF işareti yenilenmedi (2026-10-27, k2-04)
- **Belirti:** takip kapısı `T5 P72.C2: işaret s.74 ≠ çapa s.73`.
- **Kök neden:** `meds-cumle-zaman` servisi işareti yalnız ses/metin değişince yeniden üretir; çapa sonradan yüklenince eski
  (v2 sayfa ipucuyla üretilmiş) işaret kalır.
- **Çözüm/kural:** çapa Oracle'a yüklendikten sonra `pdf_isaret.py --key <key> --zorla` çalıştırılır, ardından `takip_kapisi.py --api` 0 HATA.

## H98 — Çizim panelleri dar ekranda taşıyor/sözcük kırıyor (2026-10-27, k2-03/k2-04)
- **Belirti:** `panel_sinama` 366 px'te 10–16 hata (5+ maddeli neden listeleri, dar karşılaştırma sütunlarında "Kafatası", "Korunur" kırılması).
- **Kural:** çizim ajan talimatına panel başına en çok 4 madde ve ≤60 karakter eklendi; taşan panel silinir/kısaltılır, kapı gevşetilmez.

## Sesli ders: çizimsiz resimde zoom takılı kalması
- Belirti: çizim yokken resim yakınlaşmış kalır. Kök neden: React unmount temizliğinde `ref.current` null; `CizimLayer` sayfayı ref'ten bulup sıfırlıyordu. Önleme: temizlikte ref okuma, DOM öğesini önceden yakala.

## H111 · Alt ajan çapası: görüntüyü açmadan betikle eşleme, indeks kayması; kapı yalnız sınır denetliyor (2026-10-27, k2-08)
- **Belirti:** `capa_dogrula.py` 1 HATA (P82.C3 "madde M[6, 7] sayfada yok"); elle bakınca s.75 (2 cümle) ve s.83 (4 cümle) yanlış kutuya bağlıydı. Ajan raporları "kutu numaralarını txt'den eşledim, PNG'yi açmadım" diyordu.
- **Kök neden:** `sNN.txt` madde kutuları bir madde imi içinde birleşik (M1 = üç bullet) ya da bölünmüş (M3/M4) olabilir; ajan satır sırasından numara türetti. `capa_dogrula.py` sınır dışı indeksi yakalar ama yanlış ama geçerli kutuyu yakalamaz.
- **Çözüm:** ana oturum çıktıyı cümle×kutu kelime örtüşmesiyle taradı (şüpheli 81), kritik sayfaları tek tek okudu, 6 cümle düzeltildi; 422 cümle %98 anlamsal, 0 HATA.
- **Kural:** alt ajan çapası kapıdan geçmeden kabul edilmez ve ana oturum her sayfa için "cümle ↔ atanan kutu metni" dökümünü (`goster.py` benzeri) okur; birleşik maddeli (bullet'ları tek kutuda toplayan) sayfalarda kutu numarası satır sayısından türetilmez.

## H114 · Çizim ileri-sızıntı denetimi yalnız ses metnine bakıyordu: gen sembolleri (HOX, PAX6, FGFR3) panelde reddedildi (2026-10-27, k2-08)
- **Belirti:** Genetik dersinde şablonlu panelde "PAX6", "FGFR3" gibi sembol içeren hücreler "henüz anlatılmamış terim" diye elendi.
- **Kök neden:** `cizim_uret` `onceki` metni `cumleler.md` (ses metni, "paks altı", "fe ge fe re üç") idi; öğrencinin okuduğu `ekran` metni (PAX6) denetime girmiyordu.
- **Çözüm:** `cizim_uret.py` v2 `ekran` metnini de `onceki`ye katar (cümle sayısı tutuyorsa). Eşik değişmedi.
- **Kural:** ileri-sızıntı, öğrencinin gördüğü (ekran) ve duyduğu (ses) metnin birleşimine göre denetlenir.

## H115 · Elle çizimde koordinat tahmini kenar kapısından geçmiyor; `cizim_kapisi` K3 elle çapada boş geçiyor (2026-10-27, k2-08)
- **Belirti:** gözle yazılan kontur noktaları `kenar_orani` < %70 ile düştü (s.82 fotoğraf: %26); `cizim_kapisi` "şekil 0/0 çizimli" verdi.
- **Kök neden:** kontur noktaları Canny kenarına ±5 px içinde olmalı; tahmin yetmez. K3 çapadaki `sekil` alanını sayar, elle yazılan çapa `resim: 0` kullandığı için (k2-04 dahil) K3 boş (0/0) geçer.
- **Çözüm/kural:** noktalar görüntüden kenara oturtulur (eşik/snap, ham kenar haritası bakılır, bindirme görüntüsü okunur); K3 yerine elle ölçü: lazeri resim olan cümlelerin ≥%40'ı çizimli (k2-08: 8/14). Açık iş: K3 `resim` alanını da şekil beyanı saymalı (diğer derslerin sonucunu değiştireceği için bu turda dokunulmadı).

## H470 — Çizim kapısı R0 resim etiketini reddediyordu (2026-11-02)

- **Belirti:** k2-11 s.38 fotoğraf konturu "resim kimliği geçersiz (R0)" ile atıldı.
- **Kök neden:** `capa_dok`/`cizim_uret` görüntüye `pdf_isaret.Sayfa.resimler`'in kalıcı (0 tabanlı, atlamalı) dizinini R etiketi
  olarak basıyor; `cizim_dogrula.denetle` ise `kutular` listesindeki 1 tabanlı SIRAYI bekliyor (dış ajan sınamasında 2026-10-29
  görülmüş, düzeltilmemişti).
- **Çözüm:** `cizim_uret.py` doğrulamadan önce etiketi sıraya çevirir (`resim_etiketleri`).
- **Önleme:** Görüntüde gösterilen kimlik ile kapının beklediği kimlik aynı dönüşümden geçer; kapı yazarın gördüğü etiketi kabul eder.

### H506 — Ara resimler kısa kelime öbekli kutu şemasıydı, öğretmiyordu (2026-11-06)
- **Belirti:** Kullanıcı: ara resimler "kısa kelime cümle öbekleri ile anlaşılmaz", ucuz ve ihmalkâr; akademik doğru, ayrıntılı, vektörel/Lottie/illüstrasyon istendi.
- **Kök neden:** `ARA_RESIM_KURALLARI.md` resim içi metni "en çok ~40 kelime" ile sınırlıyordu, kapı 40'ı aşanı UYARI/60'ı HATA sayıyordu; çizim zenginliği hiç ölçülmüyordu. Yazar bu yüzden 2–3 renkli kutu + 3 kelimelik etiket üretti. Ayrıca kural "slayt resmi" çağrışımıyla dar yorumlandı.
- **Kalıcı çözüm:** Üst sınır kaldırıldı; standart "Ayrıntı ve akademik çizim" bölümü (yapı çizimi, paneller, kılavuzlu etiket, slayt kaynaklı doğruluk, isteğe bağlı Lottie `lottie` alanı). Slaytta resim olmasa da mekanizma/sıralı aşama/görselleştirilebilir konu resimlenir; slayttaki mevcut resmi yeniden çizmek yasak. Kapı (`dogrula.py`): <45 kelime, <12 etiket, <15 çizim ögesi, <2 eğrili yol → HATA. Ekran `CdAraResim` Lottie oynatır (SVG yedek).
- **Önleme:** Yeni ara resim kapıdan 0 HATA geçmeden yayına girmez; ölçü örneği k2-07 r01.

### H550 — Canlı çizimde kontur doğru, etiketi yanlış figüre düşüyor ya da slayt yazısını kapatıyordu (2026-11-10, k2-28)
- **Belirti:** bağımsız anlam denetçisi 80 konturun 11'ini etiket yüzünden geri çevirdi: s.39'da "hemipleji" etiketi dipleji figürünün üstünde, "dipleji" etiketi hemipleji figürünün yanında; s.14/s.21/s.33'te yazı parçasını boyayan konturun etiketi komşu yazıyı kapatıyor; s.25'te konus ve kauda konturları kesişiyor (H61). Betik kapıları (`panel_sinama`, `cizim_kapisi`) 0 HATA veriyordu.
- **Kök neden:** `cizim_uret.py` etiketi boş bulduğu yere koyar, konumu elle verilemez; kalabalık şekil sayfasında boş yer başka figürün yanıdır. Yazar konturlara bindirmede baktı ama etiketleri çizmeden baktı; kapılar etiketin hangi figüre yakın düştüğünü ölçmüyor.
- **Çözüm:** yanlış yere düşen ve yazı kapatan etiketler kaldırıldı (etiketli kontur 72 → 20), konus/kauda konturları ayrıldı, eksik okkulta konturu eklendi; denetçi kararları `denetim_<hash>.json` ile uygulandı.
- **Önleme:** (1) yazı parçasını boyayan konturda etiket yazılmaz (boyanan yazı zaten etikettir); (2) kendi yazısını taşıyan figür/kutu konturunda etiket yalnız slaytta olmayan bilgiyi ekliyorsa yazılır; (3) yazar yayından önce bindirmeyi ETİKETLERİYLE üretip bakar (`etiket_konum` + `pdfDoc.css` yazı boyutu; k2-28 `cizim/bindir2.py`); (4) yanlış yerde etiket, etiketsizlikten kötüdür — güvenle oturmayan etiket kaldırılır.

### H572 — Etiketleri görselin içinde olan slayt şeması "resim" sayılmıyordu: lazer sayfaya düşüyor, üstüne çizim yapılamıyordu (2026-11-15, k2-65 s.40)
- **Belirti:** Kanamalı inme dersinde "Şemada bu beş yerleşim başın kesitinde ayrı ayrı kutu ile işaretlenmiştir" cümlesi
  şemayı anlatırken lazer **sayfaya** düşüyordu; `cizim_kapisi` K1 "şekil çapası var ama lazer sayfa" hatası veriyor,
  şemanın üstüne kontur çizilemiyordu. Dökümde/de `R#` kutusu hiç yoktu.
- **Kök neden:** `pdf_isaret.Sayfa`, görsel kutusunun içinde ≥8 metin kelimesi varsa onu "yazının arkasındaki şablon/kart
  zemini" sayıp `tekil_resim` listesinden çıkarıyordu (H59 düzeltmesi). Bu ölçüt, **kendi etiketlerini taşıyan slayt
  şemasını** da eliyor: 16 etiketli kelime kutunun içinde, dışarıda 1 kelime (başlık) var → kutu elenir. Sonuç:
  `resim_kutusu()` None, `sekil_isareti()` sayfa döndürür.
- **Kalıcı çözüm:** `sekil_isareti`, zemin yedeği de yoksa ve sayfa yazısının neredeyse **tümü** en büyük görsel kutusunun
  içindeyse (dışarıda ≤3 kelime, sayfa ≤24 kelime) o kutuyu şekil kabul eder. `cizim_uret.dok_uret` de `tekil_resim`
  boşken sayfadaki görsel kutularını döküme çizer (R# numarası doğrulayıcının beklediği sıra).
- **Önleme kuralı:** "İçinde çok yazı var" tek başına zemin göstergesi DEĞİL; ayırt edici ölçüt yazının **nerede** olduğudur
  (kutunun dışında kalan kelime sayısı). Yeni bir görsel/görsel-içi-etiket slaytı eklendiğinde: `sekil_isareti` çıktısı
  `t: resim` olmalı, dökümde `R#` satırı bulunmalı; bulunmuyorsa şablon zemin değil şema kabul edilir. Kapı gevşetilmez.


### H713 — Çizim kapısı şekil kapsamasını "0/0" gösterdi, gerçekte 6/6 (2026-11-27, k2-63)
- **Belirti:** `cizim_kapisi.py k2-63` "0 HATA (şekil 0/0 çizimli)" dedi; s3 sinaps şemasını anlatan 6 cümlenin hepsi çizimliydi.
- **Kök neden:** Kapı kapsamayı çapa dosyasındaki `sekil` alanından sayar; elle kurulan çapada s3 cümlelerinde bu alan boş (`None`) kaldı. Kapı boş kapsamayı HATA saymıyor, şekilsiz ders gibi geçiriyor.
- **Çözüm:** Kapsama elle doğrulandı: 8 kontur, 6 cümle. Kapıya dokunulmadı.
- **Kural:** Metinsiz (görüntü) sayfası olan derste çapa `sekil` alanı doldurulur. Kapı "0/0" verirken sayfalarda görüntü varsa bu sonuç kanıt sayılmaz, çizim elle sayılır. Kapı düzeltmesi önerisi: görüntü sayfası olup `sekil` alanı boşsa UYARI.
