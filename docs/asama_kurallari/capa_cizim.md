# Aşama kuralları — capa_cizim

> ÜRETİLMİŞ DOSYA: elle yazma. Kaynak `docs/KURUL2_YAPILMAYACAK_HATALAR.md`, üreteç `scripts/tam_hat/kural_secici.py`. 36 madde. Ayrıntı gerekirse madde başlığıyla defterde aç.

### Canlı ders PDF işareti (2026-10-20)
- **Kurallar (kullanıcı):** slayt maddesi ancak içeriğinin ≥%80'i okunan cümlede geçiyorsa zeminle işaretlenir; konuşulan
  her kelime hem metinde hem PDF'te anlık işaretlenir (PDF'te yalnız karşılığı olan kelime); lazer imleci yalnız metni
  olmayan yerde (resim/şema, `sekil`). Kelime anı sesten ölçülen konuşma parçaları (`cumle_zaman.py` surum 2, `k`) ve hece
  sayısıyla bulunur; sessizlik kelimelere paylaştırılmaz, işaret animasyonsuz.

---


### Diğer oturumlarda düzeltilen hatalardan çıkarılan dersler (tarama 2026-10-20)
- **Kural:** EMA'ya giden her Kurul 2+ metni uzun harf okunuşuyla ("dee nee aa", `patoloji_cozucu/kisaltma_ses.uzat`).
- **Kapı — EKLENDİ:** `ema_isci.uzun_kisaltma_ayarla` (anahtar `k[2-6]…` → uzun okunuş), Öğren sesi `ema-2`. Kurul 1 eski yolda (toplu yeniden üretim yok).

### H4 — Öğrenci metninde iç süreç dili ("PDF'te yok", "aday soru", "bağlanan çıkmış")
- **Kapı — EKLENDİ:** `turkce_uslup.py` kalıpları (Kurul 2+ HATA). **"Doğrusu: …" yasak DEĞİL**: şık açıklaması standardının parçası. "ajan" tıbbi terimdir.

### H5 — Kapının kendisi bozuk (her metin "999 HATA")
- **Kapı — EKLENDİ:** `otomasyon/saglik.py kapi_oz_sinama`: üslup, şık ve v2 kapıları iyi/kötü örnekle her gece; arıza panoda `kapi_ariza`.

### H6 — Birleştirici ders/dosya siliyor
- **Kural:** birleştirici yalnız ekler/günceller; reddedilen ders eski hâliyle kalır.
- **Kapı — EKLENDİ:** `ders_zinciri.korumali`: ders sayısı düşerse ya da öğe sayısı %10'dan fazla azalırsa yedek geri konur (kod 11). Silen, küçülten ve ekleyen durumlar sınandı.

### H7 — Düzeltme tek kopyada kalıyor (çözücüde düzeltilen soru spot/asistan/örnekte eski)
- **Kural:** soru kimliği tek; denetçi düzeltmesi tüm kopyalara yayılır.
- **Kapı — EKLENDİ:** `ders_zinciri.kopya_tutarliligi` (birleştirme sonrası): aynı kökteki soru önem listesi (çıkmış +
  örnek) ile çözücüde farklı doğru şık METNİYLE duramaz (harf farkı serbest: şık sırası değişebilir) → kod 13. K1'in 6
  branşında 0 yanlış pozitif; sahte uyuşmazlık yakalandı.

### H8 — Aynı PDF iki ders / yanlış PDF eşleşmesi
- **Kural:** PDF içerikle tanınır; mevcut dersle yüksek sayfa örtüşmesinde yeni ders açılmaz ("tekrar/kısım").
- **Kapı — EKLENDİ:** `isle.tekrar_denetle`: yeni dersin sayfalarının >%50'si aynı kuruldaki yayımlanmış tek bir derste
  neredeyse aynıysa (kelime kümesi Jaccard ≥0,8) uyarı → otomatik onay kapanır, yönetici karar verir. 19 yayımlanmış derste
  0 yanlış uyarı; aynı PDF'in yeniden gelişi %100 yakalandı.

### H9 — Görsel ya da bozuk OCR'lı sayfa içerikte yok
- **Kural:** metni zayıf sayfa görüntüden okunur; sayfa kapsaması ölçülür.
- **Kapı — EKLENDİ:** işçi denetleyicisi zaten her sayfayı haritada, her içerik sayfasını bir adım + bilgi maddesinde ve
  şekil/tablo sayfasını açıklamalı istiyor (%100 kapsama). Eklenen: görsel ağırlıklı ya da hoca vurgulu (≥3 renkli/kalın)
  sayfa "boş/kapak" diye atlanamaz (s.1–2 kapak muaf) — `denetle.py`, 2026-10-20.

### H10 — Başka dersin sayısı / genel bilgi; çıkmış anahtarı PDF ile çelişiyor
- **Kural:** her ürün yalnız kendi PDF'inin sayısını kullanır; anahtarı PDF ile çelişen çıkmış soru otomatik düzeltilmez, karantinaya alınır ve bildirilir.
- **Kapı — EKLENDİ:** önem yazarı çelişkiyi `elenen_cikmis` → `anahtar_celiskili` ile işaretler (soru o derste kullanılmaz);
  `ders_zinciri.karantina_onerileri` öneriyi `meds_database_v2/ders_isci/cikmis_karantina_onerileri.jsonl`'a yazar ve yöneticiye
  bildirim gönderir. Sitede otomatik gizleme/düzeltme YOK (geçmiş yıl verisi; karar yöneticinin).

### H11 — Ses Oracle'a gitmiyor, tarayıcı sesine düşüyor (404)
- **Kapı — EKLENDİ:** zincirin `oracle` adımı canlıda dersin rastgele 5 çözücü/asistan klibini yokluyor (200/206 değilse kod 12).

### H12 — Türev veri (cümle/kelime zamanı, işaret, vurgu) metnin başka sürümünden üretilmiş
- **Kural:** türev veri yayındaki metinden ve aynı makinede üretilir; hash uyuşmazlığı sessizce boş gelmez.
- **Kapı — EKLENDİ:** `saglik.py turev_eksikleri`: canlıda sesi olan her derste cümle zamanı + PDF işareti var mı (sunucu
  karma tutmayanı göndermez → sessiz kayıp görünür olur). Kurul 2+ eksik = sorun, Kurul 1 = rapor. İlk ölçüm (2026-10-20):
  15 Kurul 1 dersinde cümle zamanı yok (metin aynı gün değişmiş; Oracle zamanlama işi yetişmeli).

### H13 — Sesli ders bütünlüğü (yönerge okunması, kapanış patlaması, paragraf/süre uyuşmazlığı)
- **Kural:** EMA için de aynı: modele yalnız okunacak metin gider; eşleşme kapısı korunur.
- **Kapı — VAR:** `metin_denetle` + eşleşme kapısı + v2 kapısı.

### Kurul 2 içeriğinin karşılaması gereken sonradan eklenen özellikler
| Özellik | Durum |
|---|---|
| Konuşma v2, cümle zamanı, PDF işareti | hatta |
| Kelime zamanlaması | yalnız cihazda (`meds-kelime-zaman-hat`, GPU; Oracle ARM'de çalışmaz). **İZLENİYOR**: `saglik.py` Kurul 2+ derste kelime zamanı yoksa sorun → sabah bildirimi |
| Önemli cümle vurgusu | **EKLENDİ**: Kurul 2+'da yayın, `konusma_v2.vurgu_turet` ile `data/sesli_anlatim/vurgu/<anahtar>.json` yazar (çıkmışa bağlı cümle 3, tuzak/sayı/tanım 2, terimler). `vurgu_uret.py` Kurul 1'e bağlı kalır |
| "Öğren'de bu bilgi" (`ogren_esle.py`) | **EKLENDİ**: zincirin birleştirme adımında |
| Deste `versionGroup` / Bitirdiklerim konu kimliği | gerekmez: konu kimliği `versionGroup || id` (id her zaman var), K2 kimlikleri defterden |
| Patoloji Hızlı Check Up | **EKLENDİ** (Kurul 2+): `otomasyon/checkup_zinciri.py` (≥3 denetlenmiş ders, Claude `TALIMAT_CHECKUP.md`, `dogrula.py --kurul N`, geçmezse önceki sürüm) → `/patoloji-check-up?kurul=N` |
| Genetik TBG sınav kampı | Kurul 1'e özgü elle hazırlanmış içerik; K2 genetik dersleri spot/çözücü/asistan alır. Kamp eşdeğeri istenirse Check Up kalıbıyla eklenir |
| Test bankası | **EKLENDİ**: örnek/deste kaynakları öge kimliğinden kurula süzülür (Kurul 2+ içerik gelince kendiliğinden) |
| Örnek sorular K1–6, hastalıklar, sözlük, olası soru | hatta |

### H14 — Sunucu kodu Oracle'da ama çalışan sunucu eski kodla (yeni uç sitenin ana sayfasını döndürüyor)
- **Kapı — EKLENDİ:** `deploy-code.sh` Oracle'daki sunucu kodunun içerik karmasını, son yeniden başlatmada yazılan
  `.sunucu_kod_karma` ile karşılaştırır; farklıysa yeniden başlatır. Yeni uç ekleyen iş, dağıtımdan sonra ucu canlıda dener.

### H15 — Sesli ders + slayt ekranında slayt okunan bilgiye gitmiyor, kelime vurgusu yok (TBG kampı, 2026-10-20)
- **Kural:** `PdfDocView`'u saran kap `display: flex; flex-direction: column` ve yüksekliği sınırlı olur. Sesli metin + slayt
  ekranı yayına girmeden kelime dosyasının her cümlede kelime sayısı ekran bölmesiyle (`/\S+/g`, `**` silinmiş) birebir
  tuttuğu denetlenir (0 eksik); yeniden üretim: `meds_temp/spot_cozucu/genetik/g07_yeni/kelime_esle.py`.
- **Kapı — EKLENDİ:** `canliDers.ts bransBilgisi` K2+ için kayıt defterini kullanır; `otomasyon/saglik.py
  kayit_defteri_sorunlari` her kurulda kimlik/kod/branş numarası çiftini sorun sayar (gece sağlık → bildirim).

### H17 — EMA okunuş ayarı alt süreçte uygulanmıyordu (TBG kampı, 2026-10-20)
- **Kural:** sesi etkileyen her ayar iş dosyasından (`is.key`) sentez sürecinin İÇİNDE kurulur; genel değişkene üst süreçten
  güvenilmez. Kamp sesi (`scripts/kamp/ses.py`) süreç içi çalışır, anahtarı `kN-kamp` (K2+ uzun kısaltma yolu).
- **Kapı — EKLENDİ:** `sentezle` başta `uzun_kisaltma_ayarla(is.key)` çağırır; `saglik.py ema_alt_surec_okunusu` bu
  çağrı kalkarsa kapı arızası verir. Modül dersleri (birden çok dersin özeti) `modul_okunus.py MODUL_ANAHTARLAR`'a eklenir.

### H19 — Çıkmış cevap anahtarı tıbben hatalı / iki kaynakta çelişik (2026-10-21, TBG kampı)
- **Kural:** cevap anahtarını körü körüne kopyalama; her çıkmışın anahtarı ders kaynağına (slayt) karşı denetlenir, kaynakta yoksa
  tıbbi bilgiye göre. Anahtar değiştirilirse eski anahtar ve gerekçe **sorunun kendisinde** yazılır (açıklama + "Dikkat: sınavın cevap
  dosyasında X işaretli, tıbben hatalı"), çıkmış kaydında `anahtarDuzeltme {eski, yeni, tarih, gerekce}`, sesli anlatımda da söylenir.
  Aynı bilgiyi soran tekrar çiftleri şık METNİYLE karşılaştırılıp tek karara bağlanır (harf farkı şık sırasından olabilir).
- Kararlar: higroma → Turner şıkta varsa Turner, yoksa Down (g05 s30); over → FOXL2/RSPO1/WNT4 varsa o (g03 s30), yoksa WNT4+DAX1;
  nükleotid indel → C. Denetim raporları `meds_temp/spot_cozucu/genetik/celiski/`.
- K2–K6 taraması (2026-10-21): 51 anahtar düzeltildi; alt ajan denetiminde **soru başına kaynak araması + alıntı kaydı zorunlu** (`kanit_NN.jsonl`) — ilk turda ajanlar 76 soruyu ~6 aramayla "uygun" saydı. Araçlar `meds_temp/cikmis_celiski/`.

### H18 — Diğer oturumların 2026-10-20 düzeltmelerinden Kurul 2'ye taşınanlar (kayıt)
- Sesli ders alt madde kuralları (`CanliDersDers.tsx`: "şunlardır/ikiye ayrılır", "Birincisi/Diğeri", "Çünkü/Örneğin")
  istemcide ve tüm derslere (K2 dahil) uygulanır; v2 `duzey` alanı henüz istemcide okunmuyor. K2 yazarı alt maddeleri bu
  kalıplarla açar (liste açan cümle → sıralayan/açıklayan cümleler) ki madde düzeni doğru çıksın.
- Baştan üretme: `POST /kuyruk/<is>/yeniden-uret` (aynı gün ikinci kez 409, yeni is_id) — elle PDF yeniden işletme
  bundan başka yolla yapılmaz (el kitabı §hat panosu).
- PDF görüntüleyici kabı esnek sütun + sınırlı yükseklik (H15); tam ekran katmanı `body`'ye portal.

### H20 — Kurul 1'de elle kurulan Son Prova ve anlamsal çapa Kurul 2'de unutulmasın / K1'e sabit kalmasın (2026-10-21)
- **Kural:** kurul başına elle yapılan her yeni ürün, ertesi gün hat.json'a aşama olarak girer; betik kurul/branş/kod
  biçimini plandan ya da kayıt defterinden alır, talimatları depoda (`meds/scripts/...`) tutulur.
- **Kapı — EKLENDİ:** `son_prova` aşaması (plan_kurul.py + son_prova_zinciri.py), `ders_zinciri` `capa` adımı
  (capa_dogrula.py). Son Prova sınav dağılımı duyurusu yoksa bildirim gider.

### H21 — Soru çözücü sonradan genişleyince Son Prova soru kimlikleri kaydı (Kadın Doğum, 2026-10-21)

### H40 — Canlı çizim çizgileri görünmüyor, amaçları anlaşılmıyordu (2026-10-24, kullanıcı ekran görüntüsü s.14 herniasyon)
- İnce (1,5 px) yarı saydam mavi çizgi resim/renkli zeminde kayboluyordu; okların çoğunda etiket yoktu (k2-02'de 34 okun 15'i),
  öğrenci okun neyi anlattığını çıkaramıyordu; resimdeki mevcut okları kopyalayan anlamsız dirsekler çiziliyordu.
- Düzeltme: her çizginin altında beyaz hale (5,5 px), çizgi 2,4 px tam opak, hedef çerçevesi 2 px; **etiketsiz ok reddedilir**
  (`cizim_uret`: "etiketsiz ok"); etikete boş yer yoksa yolun ortasına koyu hap olarak konur (gizlenmez).
- Birden çok terim aynı sonuca gidiyorsa tek ok değil, alt alta dizilip "}" ile toplanır (şema grubu, `CizimLayer.Sema`).

### H41 — Yazı satırları arasına çizilen oklar kötüydü; tek tip panel yetmiyordu (2026-10-24, kullanıcı s.18)
- "Koma nedeni alkol ?" ile "SAK – SUBDURAL" arasına 1 % boyunda ok çizilmişti: görünmüyor, ilişki anlaşılmıyordu.
- Düzeltme (`cizim_uret.oku_panele`, `panel_tipi`; `CizimLayer.Sema`): iki ucu da yazı satırı olan ok, sayfanın boşluğunda
  ilişkiyi canlandıran panele çevrilir. Panel türleri yapıdan seçilir: **zincir** (A→B→C, çizgi uzayarak), **grup** (çok →
  bir, "}"), **dal** (bir → çok, karar), **maske** (görünen neden; perde kalkınca altta aranacak), **karşıt** (iki kutup).
  Akış şeması kutularındaki 1–2 kelimelik parçalar düğüm olmaz; PDF simge madde imleri ve parantezli ara söz atılır.
- Resimde şeklin kendi okunu kopyalayan kısa ok çizilmez; şekildeki ok **çerçevelenip etiketlenir** (`odak`).
- Bir kaynaktan birden çok yere giden ilişki **dallı ok** olur (`dallar` ya da aynı kaynak kutusu): kaynak kesik çizgili
  turuncu çerçeveyle bir kez gösterilir, dallar konuşma boyunca sırayla çizilir.

### H42 — Okun başlangıcı belirsizdi; resimdeki bölge vurgulanmıyordu (2026-10-24, genel kural)
- Kullanıcı: "okların başlangıç noktası belirsiz", "resimlerde marker ile boyama yapılıp hatlar belirginleştirilebilir";
  "bu derse özgü değil, genel kural". Düzeltme: her okun kaynağı çerçevelenir (kutu yoksa halkalı turuncu nokta); `kontur`
  yarı saydam sarı fosforlu dolgu + kırmızı hatla çizilir. Genel kurallar listesi: `scripts/cizim/TALIMAT_CIZIM.md`.

### H43 — Panelde bağımsız iki ilişki tek zincir gibi okunuyordu (2026-10-24, s.43)
- "uzamış kanama zamanı → intrakraniyal kanama" ve "trombositopeni → kanama, sepsis" aynı satırda bitişik dizilince
  intrakraniyal kanama ile trombositopeni bağlıymış gibi anlaşıldı. Düzeltme: `CizimLayer.Sema` bağlı bileşenlere böler,
  her bileşen ayrı satırda kendi türüyle; araya kesik ayraç. Ek kurallar: dallı ok sayfada ortak gövdeden çıkar; çizgiler
  yumuşak ve sürekli uzar. Kurallar `TALIMAT_CIZIM.md` "Genel çizim kuralları" 1–13 (bütün dersler).

### H44 — Sayfaya sığmayan panel gizleniyordu (2026-10-24, kullanıcı kararı)
- Dolu slaytlarda panel "yer yok" diye hiç gösterilmiyordu (k2-02'de 3 panel). Düzeltme: `cizim_uret` panel için
  `ek_alt` + `ek_renk` yazar; `PdfDocView` (`ekAlt`) o sayfanın altına slaytın alt kenar rengiyle alan ekler (`.pdv-page-ek`),
  panel oraya oturur. Sayfa kutusu ve işaret koordinatları aynı kalır (y > 1 yalnız panel için), "şu an anlatılan" çerçevesi
  ve sayfa numarası ek alanı da kapsar, gece kipinde ek alan sayfayla birlikte tersine çevrilir. Ek alan ders boyunca
  sabittir (anlatılan cümleye göre değişip sayfaları kaydırmaz).

### H49 — Kırılan zincirde ok yana bakıyordu; panel yazısı büyüktü; takip 8–16 sn duruyordu (2026-10-24)
- "beyin omurilik sıvısı incelemesi → santral sinir sistemi enfeksiyonu" satıra kırılınca ok yana bakıyordu → panel sürümleri
  (yatay/dikey × normal/kompakt), kırılan yatay zincir geçersiz → dikey (oklar aşağı). Panel yazısı %2,2 → %1,75 cqw.
- Canlı tarama (masaüstü, 2×): anlatılan satır 8–16 sn oynatıcı altında kalıyordu. Kök: satırı görünür alana alan program
  kaydırması kullanıcı gezinmesi sayılıp takibi 8 sn durduruyordu → program kaydırması bildirilmez.
- Bütün kurallar tek belgede: `docs/CIZIM_KURALLARI.md` (her kurul, her ders, her PDF).

### H50 — Panel tıbben yanlış okunuyordu; takip kaydırması sessizce boşa gidiyordu; ekran kalabalıktı (2026-10-24)
- "üremik ensefalopati → istenir → üre, kreatinin", "glukoz —hızla geri döndürür⊣ hipoglisemi": ok yönü/işareti anlamı
  bozuyordu. Düzeltme: anlam şablonu kütüphanesi (`scripts/cizim/sablonlar.json`, `sablon.py`), yönsüz eşleşmeler başlıklı
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

### H51 — Resim slaytında anlatım görselin yerine panelde; yatay zincirde kutular kırılıyordu; testler bunları görmüyordu (2026-10-24)
- Herniasyon şeması anlatılırken altta 5 öğeli yatay zincir paneli; kutular 3–4 satıra kırılıp panel sayfadan 333–692 px
  taşıyordu. Maske paneli "Görünen: Alkol" anlamsızdı. Grup panelinde numaralar basılmıyor, ok sözü kesiliyordu.
- Kök: sınama yalnız panel kutusunun taşmasını ölçüyordu (iç taşma, satır kırılması, kesik söz yoktu) ve elle yapılıyordu.
- Düzeltme: `resim_sayfasi` kapısı (görsel slaytta panel yok; 7 sayfa Claude ile görselin üstünde yeniden çizildi), yatay zincir
  tek satır yoksa dikey, maske "İlk izlenim / ⚠ maskeleyebilir / Atlanmaması gereken", liste numaraları, grup ızgarası.
  Kalıcı otomatik kapı `scripts/cizim/panel_sinama.mjs` (366/567/1100 px, 8 hata türü) ders zincirinde; düşen çizim yayına gitmez.

### H52 — Etiket çizimden kopuk; PDF'in kendi oku yeniden çiziliyordu (2026-10-24, s.14 ve s.27 görsel denetimi)
- s.14 "santral herniasyon" etiketi 3 numaralı okun yanında, "tonsiller" etiketi 6'dan uzakta; s.27'de slaytın kırmızı okları
  mavi okla kopyalanıyordu. Düzeltme: etiket önce hedef kutusunun (odak çerçevesi / boyalı bölge / ok ucu) hemen yanında
  aranır, uzaksa kesikli bağlantı çizgisi (`etiket_hedef`); uçları PDF aday okuna ya da a→b boyunca çizili hatta (kenar ≥%80)
  denk gelen ok yeni çizilmez, o ok çerçevelenir (`pdf_oku` → odak). k2-02: 9 ok çerçeveye çevrildi, 19/41 etiket bağlantılı.

### H53 — Resim üstündeki çizim asıl yapının önünü kapatıyordu (2026-10-24)
- Kullanıcı: "o bölgeye zoom yapılsın, çizilsin, geri dönülsün". Düzeltme: `cizim_uret.yakinlasma` → komutta `yakin`;
  `CizimLayer.yakinUygula` sayfa katmanlarını yumuşakça büyütür/geri döndürür (cümle başına tek birleşik hedef; ilk denemede
  iki çizim arasında gidip geliyordu). k2-02: 25 çizimde (10 sayfa) yakınlaşma; yerelde gerçek ekranda ölçüldü.

### H59 — Arşiv derslerinde lazer resim ve tabloları göstermiyordu (2026-10-25, kullanıcı, 2025-26 Kurul 2)
- **Kural:** şekil/tablo çapası maddeye üstündür; `madde`/`resim` dizini toplu betikle uydurulmaz; kapsama oranı
  çapayı düzelterek yükseltilir. Döküm (capa_dok, cizim dok) yalnız tekil R# ve yeşil T# kutularını gösterir.
- **Kapı:** `pdf_isaret.sekil_isareti` (şekil önceliği), `capa_dogrula.py` T# denetimi; `uygula_lazer_takip.py` çapa yazmaz.

### H60 — Slayt Çizimlerinin Toplu Gösterilmesi ve Erken/Tekrarlı Çizim Hatası (`sayfaCizimleri` Yasağı) (2026-10-25/26, kullanıcı)
- **Çözüm & Kural:**
  1. `sayfaCizimleri` kökten kaldırıldı. `marks.cizim` KESİNLİKLE VE YALNIZCA o an konuşulan cümlenin `(isr as any).z` verisidir.
  2. Bir slaytta birden fazla cümlenin çizimleri asla tek bir dizide toplanamaz. Yalnızca o an okunan cümlenin işaret ettiği tekil anatomi/bölge gösterilir.
  3. `CizimLayer.tsx` içinde `tamamlananRef` eklendi: Bir çizim `t >= 1` seviyesine ulaştığında cümle bitene kadar sabit kalır (`t = 1`), zaman dalgalanması veya re-render'larda tekrar baştan oynamaz. Komutlara stabil anahtar atanarak unmount/remount döngüsü engellendi.


### H61 — Üst Üste Çakışan ve İç İçe Geçen Çizgi/Kontur Hatası (2026-10-25/26, kullanıcı)
- **Çözüm & Kural:**
  1. Cümle bazlı çizim izolasyonu ile C0 bittiğinde "dekortike postür" kalkar, C1 başladığında "kollar fleksiyonda" gelir; asla aynı anda görünmezler.
  2. Tek bir cümlede veya aynı görsel üzerinde eşzamanlı çakışan/iç içe geçen koordinatlar YASAKTIR. Çizim kapısı (`cizim_kapisi.py`) çakışan konturları denetler.


### H65 — Tablo sayfasında tabloyu anlatmayan cümleye şekil/tablo çapası (2026-10-26, k2-23 cinsel kimlik)
- **Çözüm / kural:** Şekil/tablo çapası yalnız görseli/satırı gerçekten anlatan cümleye yazılır; paragrafın sonraki cümlelerine kopyalanmaz. Tablo çapalı cümlede `satir` boşsa çapa yazılmaz. Düzeltme: o cümlenin `sekil`'i `null` yapıldı, `tablo` kaldırıldı (capa + v2 + taslak kopyaları, `sekil_cizim.py sus` ile aynı yöntem); kapı gevşetilmedi, yayın 0 HATA ile tamamlandı.


### H70 — Mekanik 2 Cümlelik Şablon ve Yüzeysel Anlatım Yasağı (Sıfır Bilgi Kaybı ve Amfi Derinliği Standardı) (2026-10-26, k2-48 lokal anestezikler)
- **Çözüm / kural:** Sayfa başına yüzeysel 2 cümlelik kopyala-yapıştır şablonlar KESİNLİKLE YASAKTIR. Her slayt için amfi ders notundaki tüm maddeleri, tabloları, spesifik ilaç isimlerini, maksimum dozları ve patofizyolojik mekanizmaları kapsayan 3 ila 6 zengin cümle yazılmalıdır (35–70 slaytlık dersler için 140–250+ cümle, ~2000–3500 kelime, 15–25 dakika anlatım derinliği). K48 bu standartla baştan üretildi (144 cümle, 2438 kelime, 68 atomik bilgi, 10/10 çizim, 6.23 MB .medspak) ve 0 HATA ile Oracle canlı ortamına alındı.



### H76 — Cümle sayısı kapısı kısaltma noktalarını cümle sonu sayıyordu (2026-10-26)
- **Kalıcı çözüm:** Cümle sonu ancak noktadan sonra **büyük harf** ya da metin sonu geliyorsa sayılır (`[.!?](?=\s+[A-ZÇĞİÖŞÜ]|\s*$)`). Gerçek üç cümleli açıklama hâlâ HATA alır; kural gevşemedi, yanlış sayım düzeldi. Ayrıca "frenler"/"çapası" gibi çeviri mecazları (8 terim) doğal Türkçeyle yeniden yazıldı.


### H85 — Çizim önemli bölgeyi örtüyor, zoom yanlış/fazla, kelime ↔ kelime oku okumayı bozuyor (2026-10-27, kullanıcı bildirdi)
- **Çözüm:** kontur %8 dışa açılır, hale yok, dolgu %13 bulanık, karartma %10, kalınlık bölgeye göre 1–2,4 px; akış yalnız
  resim çiziminde (`yakin`); zoom ≤1,6×, ≥1,25× gerekmezse yok, bölge ≤%20; tabloda çizim yok (yalnız marker). Üretici
  (`cizim_uret.yakinlasma`) yalnız resimde ve ≤%20; kapı K10–K12; standart `KURUL2_DERS_STANDARDI.md` §4; metin takipçisi
  kapısı `takip_kapisi.py` (T1–T6).
- **Önleme kuralı:** okumayı bozan hiçbir çizim/zoom yayına girmez; yeni ders kapıları K10–K12 + `takip_kapisi.py` 0 HATA.
  Yayındaki eski derslerin verisi kapıda 36 ihlal gösteriyor; görüntüleyici aynı kuralları uygular, yeniden üretimde düzelir.


### H87 — Çizim doğrulayıcısının komut satırı Kurul 2 cümle kimliklerini ve resim kutularını tanımıyor; sarmalayıcı yanıltıcı 0 HATA verdi (2026-10-27, k2-02)
- **Çözüm / kural:** çizim için geçerli kapılar YALNIZ `cizim_uret.py` (yerleşim + doğrulama, gerçek kutu ve görüntüyle) →
  `cizim_kapisi.py` → `panel_sinama.mjs`. Parti ajanının kendi sarmalayıcı sonucu kanıt sayılmaz; reddedilen çizim
  yayına girmez (emin olunmayan yer çizilmez). CLI düzeltmesi açık iş.


### H90 — Anlam denetimi önbellek anahtarı değişince denetim sessizce atlandı (2026-10-27, k2-02)
- **Çözüm / kural:** elle üretimde her yerleşimden sonra `rapor.anlam_denetimi.bakilan` panel sayısına eşit olmalı; değilse kararlar
  yeni girdi anahtarına (sıra korunarak) eşlenir ya da denetim yeniden yapılır. `bakilan: 0` ile çizim yayına girmez.


### H91 — Çizim PDF'i önbellekte olmayınca bütün konturlar sessizce reddedildi (2026-10-27, k2-03/k2-04)
- **Çözüm:** ikisine de aynı yedek yol (indirme klasörü → `pdf_isaret.pdf_indir`); `cizim_uret` PDF hiç bulunamazsa durur.
- **Önleme kuralı:** bir hattaki bütün betikler kaynak dosyayı aynı yardımcıyla bulur; ret sayacında tek bir nedenin tüm komutları
  ataması (ör. "görüntü yok" = kontur sayısı) kapı hatası sayılır, yayına geçilmez.


### H93 — Çapa değişince PDF işareti yenilenmedi (2026-10-27, k2-04)
- **Çözüm/kural:** çapa Oracle'a yüklendikten sonra `pdf_isaret.py --key <key> --zorla` çalıştırılır, ardından `takip_kapisi.py --api` 0 HATA.


### H98 — Çizim panelleri dar ekranda taşıyor/sözcük kırıyor (2026-10-27, k2-03/k2-04)
- **Kural:** çizim ajan talimatına panel başına en çok 4 madde ve ≤60 karakter eklendi; taşan panel silinir/kısaltılır, kapı gevşetilmez.

### H99 — v15'te yeni ve bazı eski sayfalara menüden ulaşılamıyordu (2026-10-27)
- **Çözüm:** `navV15.menuGruplari` tek kaynak; üç görünüm de ondan çizer. Araçlar ayrı kompakt sıra.
- **Kural:** yeni sayfa yalnız NAV_TREE'ye (ve gerekirse KISISEL'e) eklenir; kabukta elle sayfa listesi yazılmaz.


### v15 tam ekranda yan menü içeriğin üstüne biniyor (2026-10-27)
- **Kural:** Yeni kabuk (v13, v15…) eklenince `html.is-app-fullscreen` için o kabuğun yan menü/üst bar sınıfları da gizlenir ve `--sh-side-w` sıfırlanır (`styles/v15/shell.css` sonu).

### H100 — Koyu temada "beyaz" yazılar kayboluyordu; spinner/iskelet renkleri temaya uymuyordu (2026-10-27)
- **Çözüm:** `index.css`: `.text-white` → `var(--color-on-solid)` (katmansız kural utilities katmanını ezer), `.bg-ink-surface .text-white` → `--color-canvas`, koyu perde için `.on-perde`; iskelet `color-mix(accent)`; tanımsız değişkenler gerçek tokenlara bağlandı. Tam döküm `docs/V15_TEMA_DENETIMI.md`.
- **Kural:** Yazı rengi için `text-white` değil `text-on-accent`/`text-on-solid`; yeni CSS değişkeni yalnız `palettes.ts` TOKEN_KEYS ya da v15 tokens.css içindekilerden; sabit renk yalnız bilinçli süs (çerçeve, kâğıt üstü çizim) için.


### Sesli ders: çizimsiz resimde zoom takılı kalması
- Belirti: çizim yokken resim yakınlaşmış kalır. Kök neden: React unmount temizliğinde `ref.current` null; `CizimLayer` sayfayı ref'ten bulup sıfırlıyordu. Önleme: temizlikte ref okuma, DOM öğesini önceden yakala.

### H111 · Alt ajan çapası: görüntüyü açmadan betikle eşleme, indeks kayması; kapı yalnız sınır denetliyor (2026-10-27, k2-08)
- **Çözüm:** ana oturum çıktıyı cümle×kutu kelime örtüşmesiyle taradı (şüpheli 81), kritik sayfaları tek tek okudu, 6 cümle düzeltildi; 422 cümle %98 anlamsal, 0 HATA.
- **Kural:** alt ajan çapası kapıdan geçmeden kabul edilmez ve ana oturum her sayfa için "cümle ↔ atanan kutu metni" dökümünü (`goster.py` benzeri) okur; birleşik maddeli (bullet'ları tek kutuda toplayan) sayfalarda kutu numarası satır sayısından türetilmez.


### H114 · Çizim ileri-sızıntı denetimi yalnız ses metnine bakıyordu: gen sembolleri (HOX, PAX6, FGFR3) panelde reddedildi (2026-10-27, k2-08)
- **Çözüm:** `cizim_uret.py` v2 `ekran` metnini de `onceki`ye katar (cümle sayısı tutuyorsa). Eşik değişmedi.
- **Kural:** ileri-sızıntı, öğrencinin gördüğü (ekran) ve duyduğu (ses) metnin birleşimine göre denetlenir.


### H115 · Elle çizimde koordinat tahmini kenar kapısından geçmiyor; `cizim_kapisi` K3 elle çapada boş geçiyor (2026-10-27, k2-08)
- **Çözüm/kural:** noktalar görüntüden kenara oturtulur (eşik/snap, ham kenar haritası bakılır, bindirme görüntüsü okunur); K3 yerine elle ölçü: lazeri resim olan cümlelerin ≥%40'ı çizimli (k2-08: 8/14). Açık iş: K3 `resim` alanını da şekil beyanı saymalı (diğer derslerin sonucunu değiştireceği için bu turda dokunulmadı).


### H128 · EMA yabancı terimleri yanlış okuyor; anlatım konu geçişini söylemiyor; panel geç, zoom kısa anlatımda, çizim tek renk (2026-10-28)
- **Kalıcı çözüm:** `scripts/sesli_anlatim/terim_okunus.py` + `data/sesli_anlatim/okunus/terim_okunus.json` (eponim, Latince,
  İngilizce, ticari ad + Latince kural motoru) EMA'ya giden Kurul 2+/modül metnine uygulanır (`ema_isci.paragraf_seslendir`);
  `ses_temizle` (DC, RMS eşitleme, yumuşak tepe sınırı, 12 ms geçiş). `docs/ANLATIM_KURGU_STANDARDI.md` (plan → metin,
  ±%20 sayısal tolerans). `CizimLayer.tsx` panel cümle başından, zoom ≥55 karakter; `cizim_uret.py` ZOOM_EN_AZ=70, `renk_ata`,
  `renk/boya/resim` alanları; `cizim_dogrula.py` renk/resim kutusu denetimi.
- **Kural:** yeni ders seslendirmesinden önce `terim_okunus.py --denetle <anahtar>`; yanlış `KURAL` satırı sözlüğe eklenir.
  Anlatım yazarı önce `anlatim_plani.md` kurar; başlıksız konu geçişinde "burada konu değişiyor" cümlesi zorunlu.
  Çizimde birden çok resim varsa `resim: "R#"`, ayrı yapılar ayrı renk, hattı belirsiz bölge `boya: true`.


### H111g · İzleme hızı kaydırıcısı: dokunma hedefleri 10–19 px, boş durumda imleç metinle çelişiyordu (2026-10-28, Sınav planı/Bitirdiklerim)
- **Çözüm:** boş durumda imleç 1×; ray `padding: 9px 0` + `background-clip: content-box` (görünüş aynı, 28 px dokunma), duraklara `::before` ile 40 px dikey alan + `min-width: 40px`. Bugün akışındaki "Tümü" bağlantısı (14 px) negatif kenar boşluklu 40 px alana alındı (`today.css .t15-more`). Takvim, kronometre ve tam ekran ayarlarındaki `kre-tgl` anahtarlarına `aria-label` eklendi (adsız düğme).
- **Kural:** Görünür öğe küçük olabilir ama dokunma alanı ≥40 px (dolgu/`::before`); yer tutucu değer ile açıklama metni aynı varsayımı göstermeli; her `role="switch"` düğmesinin erişilebilir adı olur (label içi olmak yetmez).


### H111u · Çıkmış sorular kart görünümü sınırsız büyüyor, Odak ızgarası 4.372 düğme çiziyordu (2026-10-28, Soru çöz, başarım)
- **Çözüm:** Kart görünümü kayan pencere: yalnız son 60 kart (`RICH_WINDOW`) çizilir, üstte düşenler tarayıcının kaydırma çapasıyla görünen kartı oynatmaz, üstte "Önceki soruları göster (n)" düğmesi; sayaçlar `richLimit` ile gösterilir. Odak ızgarası geçerli sorunun 100'lük bloğunu çizer, ‹ › ile blok değişir. Ölçüm: 8 kaydırmada DOM 34.226 → ~7.100 (sabit); Odak açılışı ~650 düğüm.
- **Kural:** Kaydırdıkça yüklenen listeler sınırsız büyümez (pencere ya da sanal liste); yüzlerce öğelik gezinme ızgarası bloklara bölünür.


### H127 · Slayttaki şekil/deney anlatılmadı, "ders yorumuna girmez" diye geçildi (2026-10-28, k2-05 Nörolojik Muayene, sayfa 32–33)
- **Kalıcı çözüm ve kural (Şekil ve deney anlatım kuralı, `KURUL2_DERS_STANDARDI.md` §8.12):**
  1. **Şekil kaynaktır.** Slayttaki çizim, fotoğraf, şema, grafik, tablo, mikroskopi ve görüntüleme; içindeki oklar, etiketler, işaretler (X, kesik/kalın çizgi, renk), panel karşılaştırmaları ders içeriğidir ve anlatılır. "Slaytta yazmıyor" şekli atlama gerekçesi değildir.
  2. **Deney/test/muayene görseli** her zaman beş soruyla anlatılır: (a) ne sınanır ve neden yapılır, (b) nasıl uygulanır (görselde ne görülüyorsa adım adım), (c) normal sonuç, (d) her patolojik panel/sonuç ne demektir ve hangi lezyonu gösterir, (e) sonuçlar birbirinden nasıl ayrılır (sınavda karıştırılan çift).
  3. **Çok panelli şekil:** her panel ayrı ayrı adlandırılır ve karşılaştırılır ("soldaki normal…, ortadaki…, sağdaki…"); işaretlerin anlamı (X = hasarlı yapı, kalın ok = sesin daha güçlü duyulduğu taraf) açıklanır.
  4. **Yalnız adı geçen kavram/test:** ilk geçtiği yerde 1–2 cümleyle ne olduğu ve ne ölçtüğü söylenir (Terim kuralı §8.5). Ayrıntı slaytta/şekilde ya da hoca dökümünde varsa o kadar açılır; yoksa uydurma yorum eklenmez ama ADI DA BOŞ BIRAKILMAZ.
  5. **Kaçamak meta cümle YASAK:** "ders bunun yorumuna girmez", "yalnız adını verir", "ölçütünü vermez", "şekilde ayrıntı yok", "nasıl uygulandığı gösterilir" gibi öğrenciye bir şey öğretmeyen cümleler yazılmaz. Gerçekten kaynakta bilgi yoksa cümle hiç yazılmaz; konu olduğu kadar anlatılır.
  6. **Şekil paragrafı betimlemeyle bitmez:** yalnız "…gösterilir / görülür / yer alır" cümlelerinden oluşan şekil paragrafı eksik sayılır; şeklin öğrettiği bilgi (mekanizma, sonuç, ayırıcı nokta) eklenir.
  7. **Çizim katmanı anlatımı izler:** her panel/sonuç anlatılırken lazer ve kontur o panele gider (kural 17/18; bir cümle = bir panel).
  8. **Denetçi şekle bakar:** bağımsız denetçi metni okuduktan sonra şekilli/tablolu her sayfanın görüntüsüne bakıp "şekildeki her panel/işaret anlatıldı mı" listesini işaretler; eksik varsa GEÇMEZ.

### H330–H334 — Sesli ders araç çubukları kalabalıktı (2026-10-28, sayfa denetimi; kullanıcı isteği)
- **Çözüm/kural:** Görünür kalanlar ders boyunca sık dokunulanlar: görünüm kipi, tam ekran (masaüstü), Çıkmış, Kalem, yakınlaştırma (masaüstü). Seyrekler `CdTasmaMenu` ⋯ menüsünde: yazı boyutu (menü açık kalır, değer yazar), yıldızlı paragraflar, terim yardımcısı (✓; açıkken çubukta etkin göstergesi), görünüm ayarları, tüm ders seçenekleri, tam ekran; PDF ⋯: sayfa teması, yakınlaştır/uzaklaştır/sığdır. Menü erişilebilir (aria-haspopup, ↑/↓/Home/End, Esc/dışarı/Tab kapatır, odak düğmeye döner), kısayollar değişmedi, tanıtım turu yeni hedeflere bağlandı (9/8 durak). Çizim/zamanlama mantığına dokunulmadı (kural 17/18). Açık: TV kipinde menü ok tuşları TV katmanına takılabilir; telefonda Kalem 33 px, küçült düğmesi 36×22 px.
- **Kural:** Sesli ders ekranına yeni düğme eklenirken önce sık/seyrek kararı verilir; seyrekse ⋯ menüsüne girer, durum taşıyorsa menüde ✓ ve çubukta etkin göstergesi olur.


### H447 — Metni değişen paragrafların v2 cümleleri boş kaldı, ders ekranı ve çapası o paragraflarda eksik yayında (2026-10-30)
- **Çözüm:** 9 paragraf metin değişmeden dolduruldu (eski v2'de birebir aynı kalan 17 cümle kimliğiyle geri alındı, kalanlar yeni
  kimlikle yazıldı; paragraf kimlikleri `k2-05-pNNN` biçimine döndü); `konusma_v2.py --dogrula` 0 HATA.
- **Önleme:** `klip_tasi.py` "v2: N paragraf boş" raporu verdiyse o ders, boş paragraflar `konusma_v2` biçiminde yazılıp
  `konusma_v2.py --dogrula <dizin>` (kaynak.md ile) 0 HATA verene dek dağıtılmaz; açık iş olarak not düşmek yerine aynı oturumda kapatılır.


### H448 — `klip_tasi.py` metinle birlikte düzenlenmiş v2'yi eski metne göre yeniden kurup değişen paragrafları boşaltıyordu; `ders-ekle` elle iyileştirilmiş çapayı ezdi (2026-10-30)
- **Çözüm:** `klip_tasi` cümle seslerinin birleşimi yeni paragraf metniyle aynıysa v2'ye dokunmaz. Çapa: yereldeki taşınmış çapa esas alındı,
  değişen paragraflarda değişmeyen cümleler eski çapayı (git HEAD) geri aldı, yeni cümleler satırdan `pdf_isaret.capa_maddeleri` ile madde
  dizinine çevrildi; `capa_dogrula` %98, 0 HATA; çapa Oracle'a yeniden yazıldı.
- **Önleme:** yayımlanmış dersin metni düzeltildiğinde `sesli_yayinla.py`'den SONRA yerel çapa (klip_tasi ile taşınmış + değişen paragraflar
  yazılmış) Oracle'a geri kopyalanır ve `pdf_isaret.py --key <key> --zorla` çalıştırılır (H93); `ders-ekle`'nin yazdığı kaba çapaya güvenilmez.
