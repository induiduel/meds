# Kurul 2 — Yapılmayacak Hatalar Defteri (ZORUNLU OKUMA)

> Kurul 2'de sistem tam otomatik çalışacak: Drive'a gelen her yeni PDF'ten interaktif ders (Öğren), sesli spot / sınav asistanı
> ve sesli soru çözücü içeriği insan müdahalesi olmadan üretilip EMA ile seslendirilecek. Bu defter, Kurul 1 içeriğinde kullanıcının
> gördüğü ve **Kurul 2'de bir daha yapılmaması gereken** hataları toplar. Kurul 2 hattını kuran ya da çalıştıran her ajan önce
> bu dosyayı okur. Yeni bir hata bildirildiğinde buraya yeni madde eklenir (eskiler silinmez).
>
> Kurul 1'deki mevcut içerik bu defter yüzünden toplu olarak yeniden üretilmez; amaç gelecekteki üretimdir.

## H1 — Geçiştirici şık açıklaması (2026-10-18)

- **Görülen:** Sınav asistanı → Yardım al (Patoloji 08, IL-17 sorusu): "IL-2 bu sorunun cevabı değil.", "IL-10 nötrofil alımı
  yapmaz.", "IL-13 nötrofil toplayıcı olarak geçmez."
- **Neden hata:** Şıkkın ne olduğunu ve ne işe yaradığını söylemiyor; öğrenciye hiçbir şey öğretmiyor.
- **Kurul 2'de doğrusu:** Her şık (doğru dahil) için kavramın ne olduğu + ne işe yaradığı + bu soruda neden doğru/yanlış olduğu,
  2–3 cümle. Ayrıntı: `meds/docs/SIK_ACIKLAMA_STANDARDI.md`.
- **Kapı:** `meds/scripts/sik_aciklama.py`.

## H2 — Türkçeye uymayan ifade ve iç etiketler (2026-10-18)

- **Görülen:** Sınav asistanı (Patoloji 08, "IL-6: karaciğerde akut faz yanıtı"): "IL-6 … salınır; **imzası** karaciğerde akut
  faz yanıtını uyarmaktır." ve "**Ayrım cümlesi:** ateşte IL-1 daha belirgin, akut fazda IL-6, nötrofil alımında IL-17."
- **Neden hata:** "imzası" İngilizceden çeviri mecaz; "Ayrım cümlesi:" yazarın iç etiketi, öğrenci anlamıyor. Metin EMA ile okunduğu
  için doğal olmayan cümle dinlerken daha da kötü duyulur.
- **Kurul 2'de doğrusu:** Doğal, eksiksiz, anlaşılır Türkçe; çeviri mecaz ve iç etiket yok; tam cümle.
  Ayrıntı: `meds/docs/TURKCE_USLUP_STANDARDI.md`.
- **Kapı:** `meds/scripts/turkce_uslup.py` (liste her kalıbı yakalamaz; denetçi metni sesli okunuyormuş gibi okur).

## Kurul 2 hattı için genel kural

- Her içerik türünde yazar + bağımsız denetçi geçişi; doğrulayıcı 0 HATA vermeden EMA seslendirmesine ve yayına geçilmez.
- Bu defterdeki her maddenin kapısı Kurul 2 hattının doğrulayıcılarına bağlıdır (2026-10-18):
  - Sınav asistanı, sesli çözücü, spot önem listesi doğrulayıcıları: her zaman HATA.
  - Öğren: `validate_learning_decks.py deck.json --oyun-zorunlu --kurul2`; sınav spotları: `sinav_spotlari/dogrula.py --kurul2`.
  - **Kurul 2 başlarken ders işçisinin denetimine (`meds/scripts/ders_isci/denetle.py`, Öğren çağrısı) `--kurul2` eklenmeli** ve
    işçi talimatına bu defter okutulmalı. Kurul 1 işçisi bayraksız çalıştığı için şimdilik etkilenmez.

## Sesli ders PDF/DOCX dışa aktarımı (2026-10-20)

- **Yazıyla sayı:** konuşma metni okunuş için "iki virgül bir", "yüzde kırkına" yazar; öğrenciye verilen dosyada bunlar
  "2,1", "%40'ına" olmalı. Kural tek yerde: `src/services/sayiYazim.ts` (`sayilariYaz`), dışa aktarım
  (`components/canliDers/canliDersDisaAktar.ts`) ve ekran (`canliDersStore.ts` → `sayilariDuzelt`, vurgu konumları `sayilariYazEslemeli` ile taşınır) her derste uygular. Saklanan metin değiştirilmez (ses ve cümle zamanı ona bağlı).
- **Düz madde yığını yok:** paragraf tek madde olarak basılmaz; ilk cümle ana madde, sonrakiler alt madde, "Yani/Örneğin…"
  ve "2 ölçütü ayırın" gibi duyurulardan sonra gelenler ikinci düzey; kısa noktasız satır alt başlık olur.

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

## Diğer oturumlarda düzeltilen hatalardan çıkarılan dersler (tarama 2026-10-20)

Her maddede: belirti · kök neden · Kurul 2 kuralı · kapı durumu. Kanıtlar commit/kayıt olarak `GELECEK_PLANLAMASI.md` §13–14'te.

### H3 — Kısaltma kelime gibi okunuyor ("DNA" → "deneye")
- **Kök:** `okunus.duzelt` harf adlarını bitişik yazıyordu ("denea"); EMA bunu kelime gibi okur.
- **Kural:** EMA'ya giden her Kurul 2+ metni uzun harf okunuşuyla ("dee nee aa", `patoloji_cozucu/kisaltma_ses.uzat`).
- **Kapı — EKLENDİ:** `ema_isci.uzun_kisaltma_ayarla` (anahtar `k[2-6]…` → uzun okunuş), Öğren sesi `ema-2`. Kurul 1 eski yolda (toplu yeniden üretim yok).

### H4 — Öğrenci metninde iç süreç dili ("PDF'te yok", "aday soru", "bağlanan çıkmış")
- **Kök:** yazar ajan kendi notunu öğrenci metnine bırakıyor.
- **Kapı — EKLENDİ:** `turkce_uslup.py` kalıpları (Kurul 2+ HATA). **"Doğrusu: …" yasak DEĞİL**: şık açıklaması standardının parçası. "ajan" tıbbi terimdir.

### H5 — Kapının kendisi bozuk (her metin "999 HATA")
- **Kök:** doğrulayıcı Python sürümünde çöktü, çöküş "içerik reddi" sayıldı.
- **Kapı — EKLENDİ:** `otomasyon/saglik.py kapi_oz_sinama`: üslup, şık ve v2 kapıları iyi/kötü örnekle her gece; arıza panoda `kapi_ariza`.

### H6 — Birleştirici ders/dosya siliyor
- **Kök:** toptan yeniden yazım; reddedilen ders siliniyordu (patoloji asistanı, s13/s15/s16).
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
- **Kök:** yeniden başlatma kararı "bu dağıtımda değişen dosyalar"a bakıyordu; dosya Oracle'a başka yoldan (tek dosya rsync,
  başka oturum) yeniden başlatmasız gelmişti, rsync saat damgasını da koruyor (2026-10-20: kamp uçları yüklenmemişti).
- **Kapı — EKLENDİ:** `deploy-code.sh` Oracle'daki sunucu kodunun içerik karmasını, son yeniden başlatmada yazılan
  `.sunucu_kod_karma` ile karşılaştırır; farklıysa yeniden başlatır. Yeni uç ekleyen iş, dağıtımdan sonra ucu canlıda dener.

### H15 — Sesli ders + slayt ekranında slayt okunan bilgiye gitmiyor, kelime vurgusu yok (TBG kampı, 2026-10-20)
- **Kök 1:** PDF görüntüleyici (`PdfDocView`, `.pdv { flex: 1; overflow: auto }`) esnek sütun olmayan bir kaba konmuştu;
  görüntüleyici içeriği kadar uzadı, kendi içinde kaydırılamadı, başlık "slayt 14" derken ekranda 1. sayfa kaldı.
- **Kök 2:** kelime zamanları dosyası (`src/data/genetik_kamp/kelime.json`) boş yayına girmişti; kelime vurgusu hiç çıkmadı.
- **Kural:** `PdfDocView`'u saran kap `display: flex; flex-direction: column` ve yüksekliği sınırlı olur. Sesli metin + slayt
  ekranı yayına girmeden kelime dosyasının her cümlede kelime sayısı ekran bölmesiyle (`/\S+/g`, `**` silinmiş) birebir
  tuttuğu denetlenir (0 eksik); yeniden üretim: `meds_temp/spot_cozucu/genetik/g07_yeni/kelime_esle.py`.
- **Ekran tam ekranı:** uygulama kabuğunun altında kalan sabit (`position: fixed`) katman çubukların altında kalır; tam
  ekranda bileşen `body`'ye taşınır (portal), yerel tam ekran `document.documentElement` için istenir.

### H16 — Sesli ders listesinde iki ders aynı branş numarasını aldı (Meme Kanseri / Memenin Benign "33", 2026-10-20)
- **Kök:** branş içi numara Drive dosya adındaki `NN)` önekinden okunuyordu; Drive'da iki PDF aynı numarayla gelmişti,
  elle düzeltme tablosu (`BRANS_DUZELT`) gerekti.
- **Kurul 2 kuralı:** K2+ derslerinde branş ve numara YALNIZ ders kayıt defterinden (`src/data/dersler/kN.json`, kod
  `2n07` → 7) alınır; Drive adı numara kaynağı değildir. Elle tablo K1'e özgüdür, K2'ye satır eklenmez.
- **Kapı — EKLENDİ:** `canliDers.ts bransBilgisi` K2+ için kayıt defterini kullanır; `otomasyon/saglik.py
  kayit_defteri_sorunlari` her kurulda kimlik/kod/branş numarası çiftini sorun sayar (gece sağlık → bildirim).

### H17 — EMA okunuş ayarı alt süreçte uygulanmıyordu (TBG kampı, 2026-10-20)
- **Kök:** `ema_isci.sentezle` ayrı süreçte çalışır; üst süreçte `uzun_kisaltma_ayarla` ile kurulan genel ayar (H3 uzun
  kısaltma, modül okunuşu) oraya taşınmıyordu → kısaltmalar eski yolla okundu.
- **Kural:** sesi etkileyen her ayar iş dosyasından (`is.key`) sentez sürecinin İÇİNDE kurulur; genel değişkene üst süreçten
  güvenilmez. Kamp sesi (`scripts/kamp/ses.py`) süreç içi çalışır, anahtarı `kN-kamp` (K2+ uzun kısaltma yolu).
- **Kapı — EKLENDİ:** `sentezle` başta `uzun_kisaltma_ayarla(is.key)` çağırır; `saglik.py ema_alt_surec_okunusu` bu
  çağrı kalkarsa kapı arızası verir. Modül dersleri (birden çok dersin özeti) `modul_okunus.py MODUL_ANAHTARLAR`'a eklenir.

### H19 — Çıkmış cevap anahtarı tıbben hatalı / iki kaynakta çelişik (2026-10-21, TBG kampı)
- **Görülen:** (1) 2018-2019 K1 `past-q-18-84` "nükleotid delesyon ve insersiyonları hangi yöntemlerle?" — cevap dosyası E
  (Southern blot + PCR + prometafaz bantlaması + dizi analizi); tıbben C (PCR ve dizi analizi): bantlama megabaz, Southern kilobaz
  düzeyindedir. Site açıklaması da "boyut yelpazesi" yorumuyla E'yi savunuyordu. (2) Kistik higroma + ASD/VSD aynı soru iki kaynakta
  Down / Edwards / Turner. (3) Over yönü genleri iki sürümde aynı üçlü bir yerde doğru, bir yerde yanlış.
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
- **Görülen:** Son Prova betikleri `Kurul 1` yolu, sabit branş tabloları (`BRANS_KLASOR`), `KURUL = 1`, yalnız `meds_temp`'te
  duran talimatlar (YENI_SORU.md, YENI_DENETIM.md) ve `[a-z]?\d{2}` slayt kodu kalıbıyla yazılmıştı; anlamsal çapa 83 derste
  ajanlarla elle yazıldı, hatta adımı yoktu.
- **Kural:** kurul başına elle yapılan her yeni ürün, ertesi gün hat.json'a aşama olarak girer; betik kurul/branş/kod
  biçimini plandan ya da kayıt defterinden alır, talimatları depoda (`meds/scripts/...`) tutulur.
- **Kapı — EKLENDİ:** `son_prova` aşaması (plan_kurul.py + son_prova_zinciri.py), `ders_zinciri` `capa` adımı
  (capa_dogrula.py). Son Prova sınav dağılımı duyurusu yoksa bildirim gider.

### H21 — Soru çözücü sonradan genişleyince Son Prova soru kimlikleri kaydı (Kadın Doğum, 2026-10-21)
- **Görülen:** `k1-93-son-prova-kadin-dogum` doğrulaması 16 HATA "soru ref havuzda yok". Part 02:12'de yazıldı; 04:01–04:21'de
  Kadın Doğum çözücüsüne 15 soru eklendi, setler (`k02-1`/`k02-2`) yeniden numaralandı. Sitedeki Son Prova bozulmadı (sorular
  yayın dosyasında kendi kopyasıyla, denetimde yeniden yazılanlar `t06#…` kimliğiyle duruyordu).
- **Düzeltme:** `dogrula.py` denetimde yeniden yazılmış soruyu (`duzelt/eslem.json` → yayındaki `t0N#…`) geçerli sayar; yalnız
  numarası kayan `k01-2#32` → `k01-1#32`. 14 part 0 HATA, yayındaki tüm kimlikler karşılıklı.
- **Kurul 2 kuralı:** Son Prova yazıldıktan sonra çözücü değişirse part yeniden yazılır — `son_prova_zinciri.part_izi` ders
  başına havuz soru sayısını içerir, değişince part `_eski/`'ye alınıp baştan yazılır. Kurul 1'de `soru_dagit.py` elle yeniden
  çalıştırılmamalı (kayan 15 eski kimlik havuzda yok); gerekirse önce parça referansları güncellenir.
