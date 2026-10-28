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

## [2026-10-21] Çıkmış soruda iç uyarı metni ve kalıp şık açıklaması (h06/19 Refik Saydam)

- **Hata:** Çözücüdeki çıkmış sorunun kökünde "[Dikkat — olası hatalı kayıt …]" iç notu kalmıştı; öğrenciye gösterildi ve EMA ile
  okundu. Aynı sorunun şık açıklamaları "bu soruda aranan özellik değildir ve elenir" kalıbıydı, ipucu konu dışıydı.
- **Karar (kullanıcı):** cevap anahtarı çelişkisinde tıbben/tarihen doğru olan esas alınır (224 sayılı Kanun 1961; Refik Saydam
  1942'de öldü → E). Not kökten çıkarıldı, şıklar ne/ne işe yarar/neden standardıyla yeniden yazılıp seslendirildi.
- **Kurul 2 kuralı:** soru kökü, şık ve seçeneklerde köşeli parantezli iç not ("Dikkat", "olası hatalı", "öğrenci notundan")
  yayına giremez; kaynak çelişkisi denetçi tarafından tıbbi doğruya göre çözülür ve gerekçesi kayda yazılır.

### H — Okunuş ekrana, rakam sese sızıyordu (kullanıcı, 2026-10-22)
- **Belirti:** ekranda “yirminci ile yirmi dördüncü hafta”, “beta ha ce ge”; seste “14. … hafta” (rakam + nokta duraklamalı).
- **Kural:** ses okunuşla (“on dördüncü”, “doku plazminojen aktivatörü”), ekran yazımla (“14.”, “(t-PA)”, “β-hCG”, “12+6 hafta”).
- **Kapı — EKLENDİ:** ekran `ekranYazim.ts`, ses `okunus.SAYI_TTS`; yeni kısaltma/açılım `yazim_sozlugu.py` ile sözlüğe girer.

### H22 — Sesli derste dolgu ve asılsız "hoca vurguladı" cümleleri (kullanıcı kuralı, 2026-10-22, KALICI)
- **Belirti:** K1 sesli derslerinde "hoca bunu ayrıca vurgulamıştır", "hocanın altını çizdiği nokta şudur" gibi dayanaksız,
  sürekli tekrar eden meta cümleler; kelime/dakika sınırına ulaşmak için eklenen, dersi uzatıp bağlamdan koparan dolgu.
- **Kural:** Amaç bilgiyi en kısa yoldan, doğru, açıklayıcı ve eksiksiz iletmek. Kelime alt sınırı ve süre hedef DEĞİLDİR;
  kısa ama eksiksiz metin doğrudur. Önem vurgusu yalnız dayanağı varsa (çıkmış soru, öğrenci notu, slayttaki işaret) ve
  kritik noktada yapılır; dayanağı yazılmadan "hoca vurguladı/işaretledi/altını çizdi" denmez. Tekrar, geçiş ve özet
  dolgusu ("şimdi gelelim", "bir kez daha hatırlatalım", "daha önce de söylediğimiz gibi") yasak.
- **Kapı — EKLENDİ:** `scripts/sesli_anlatim/metin_denetle.py` → `DOLGU` kalıpları HATA; "Burası önemli/çok önemli/sınavda
  sık" bölüm sayısının yarısını (en az 3) aşarsa HATA; kelime alt sınırı artık yalnız uyarı. K1 metinlerine toplu müdahale yok.

### H23 — Öğrenci işaretli slayt yanlış yorumlandı + okunuşla yazılmış metin (İmmünofarmakoloji V2, kullanıcı, 2026-10-22)
- **Belirti:** İşaretli PDF'te sarı vurguların hepsi "işlendi" sayıldı, çapraz sarı şeritler kaçırıldı; metin "ce de iki" gibi
  okunuşla yazıldı; anlatım kopuk ve hızlıydı.
- **Kural (kullanıcı tanımı):** sarı ya da mavi ÇAPRAZ şerit/çizgi = hoca okumadı (anlatılmaz); metin üzerindeki YATAY
  çizgi/vurgu = okundu; yıldız, daire, "önemli", "bil", ünlem, altı çizili = önemli. Öğrenci notlu PDF önce sayfa sayfa
  işaret dökümüne (okundu/okunmadı/önemli/el yazısı) çevrilir, metin dökümden yazılır.
- **Yazım:** konuşma metni kısaltmaları yazımla tutar (CD2, IL-2); okunuşu EMA katmanı yapar (`modul_okunus.py`
  MODUL_ANAHTARLAR / Kurul 2+ uzun kısaltma yolu). Sayı, Yunan harfi ve simge yazıyla.
- **Anlatım:** akıcı, bağlantılı (ne → nasıl → nerede → yan etki); kısa kopuk cümle dizisi yasak.

### H24 — Kısa özet derste önemli yerler atlandı, slaytla ilişkisiz/kopuk anlatım (Patoloji V2, kullanıcı, 2026-10-23)
- **Belirti:** "%50 kısa" hedefli V2'lerde önem maddeleri ve çıkmış bilgileri atlandı; paragraflarda çıkmıştan koparılmış tek
  cümleler ("çıkmış soruda doğru önerme…", "… değildir" diye şık sayma), konu ortasında başka konudan bilgi; bir slayttan tek
  satır okunup başlığı bile açıklanmadan başka konuya geçildi.
- **Kural:** kısa sürüm slayt sırasını izler; önem listesinin (`src/data/<branş>_onem/`) TAMAMI ve her çıkmış konu içinde
  anlatılır; konu ne → neden/nasıl → sınav ayrıntısı sırasıyla kapanmadan geçilmez; soru dili ve şık yankısı yasak; uzunluk
  V1'in %45–65'i ("çok kısalt" diye madde atma). Yazar + bağımsız denetçi (kapsama dökümü + kaynak karşılaştırması) zorunlu.
- **Uygulama:** `meds_temp/sesli_anlatim/v3_pat/{TALIMAT,DENETIM}.md`, blok için `meds_temp/blok_ozet_v2/EK_V2.md`.
- **Ek tuzaklar:** ders–PDF eşlemesi içerikle doğrulanır (k1-65 Meme Kanseri Öğren destesi 33) Benign PDF'ine bağlıydı →
  sesli V2/V3 sanal deste `k1p-k1-65-…-sesli-v2`); kitte slayt metni yoksa (k1-66) PDF metni ayrıca verilir.

### H25 — Claude CLI yolu değişti, gece hattının bütün Claude aşamaları sessizce düştü (2026-10-23)
- **Belirti:** masaüstü uygulaması 02:18'de güncellenip Claude Code'u `~/.config/Claude/claude-code/<sürüm>/<karma>/claude`
  altına taşıdı; `~/.local/bin/claude` sarmalayıcısı yalnız `<sürüm>/claude`'a baktığı için "Claude Code bulunamadı" ile
  çıktı. `claude -p` kullanan her aşama (ders zinciri, olası soru — o akşam Kurul 1 sınav günüydü —, hastalık, kamp, Son Prova)
  çalışmazdı; hata yalnız aşamanın kendi `claude.log`'unda kalırdı.
- **Düzeltme:** sarmalayıcı iki düzeni de arar, en yüksek sürümü seçer (yedek: oturum karalama klasörü). **Kapı:**
  `otomasyon/saglik.py` → `claude_cli` (`claude --version`); başarısızsa sabah özetinde sorun.

### H26 — Ücretsiz modelde sessiz boş yanıt ve yarım JSON (Gemini düşünme payı, 2026-10-23)
- **Belirti:** Gemini düşünme belirteçleri `maxOutputTokens`'tan düşüyor → uzun JSON yarıda (`finishReason=MAX_TOKENS`),
  `parts` yok → `KeyError` ağ hatası sanılıp aynı model yeniden deneniyor; hiçbir şey günlüğe yazılmıyordu (86 sn bekleyip `None`).
- **Düzeltme:** `cloud_llm.chat(dusunme=N)` düşünme payını ayrı verir, çıktı sınırını o kadar büyütür; boş yanıt `BosYanit` →
  doğrudan sıradaki model; her istisna ve ayrıştırılamayan yanıt `log`'a. Görev yönlendiricisi Gemini'ye varsayılan 2048 pay verir
  (`gorevler.json` → `gemini_dusunme`), uyarılar `meds_temp/gorev/gunluk.jsonl`'de (`model_uyari`).

### H27 — Ücretsiz model zinciri sağlam modeli bütün gün kapatıyordu (cloud_llm, 2026-10-23)
- **Belirti:** bir anahtar `400` (yanıta özgü JSON hatası), ikinci anahtar `401` (geçersiz) verince anahtar döngüsü "tüm
  anahtarların günlük kotası doldu" dalına düşüyor, `groq:openai/gpt-oss-120b` `meds_temp/state/cloud_llm.json`'a "kota dolu"
  yazılıyor → o gün BÜTÜN süreçlerde (Faz 14 kuyruğu, görev yönlendiricisi) en güçlü Groq modeli kullanılmıyordu. Ayrıca tek
  anahtarın `401`'i modeli tüm anahtarlarıyla süreç boyunca atlatıyordu.
- **Düzeltme:** model yalnız TÜM geçerli anahtarlar günlük kota (429 günlük) dediyse kapanır; `401/403` yalnız o anahtarı,
  `404` modeli atlatır. Yanlış kayıt temizlendi. **Açık (kullanıcı):** `.env` `GROQ_API_KEY_2` geçersiz (401; değer anahtar
  adına benziyor) — düzeltilmeli ya da silinmeli.

### H28 — Doğrulayıcı tıbbi "kaynaklı"yı süreç dili sanıyordu; önem ↔ çözücü şık uzunluğu uyumsuzdu (2026-10-23)
- `patoloji_cozucu/cozucu_dogrula2.py` `IC_DIL` `kaynak\w*` kalıbı "plazma kaynaklı", "endotelden kaynaklanır", "enfeksiyon
  kaynağı" ifadelerini HATA sayıyordu (çözücü ve asistan şık açıklamaları). Kalıp yalnız süreç biçimlerine daraltıldı
  (kaynakta, kaynağa göre, kaynakça, kaynak metin).
- Önem listesi talimatı örnek şıklara ≤14 kelime (uyarı) izin verirken çözücü kapısı örnek şıkta ≤6 kelime istiyor → önem
  aşamasından geçen soru çözücüde kalıyordu. Görev kuralı 6 kelimeye indirildi (`kurallar/ornek_soru_spot.md`).
- Not: Kurul 1 Claude çözücüleri (ör. e07) bugünkü kapıdan geçmez (486 HATA, 2026-10-18 şık standardından önce üretildi);
  K1 çıktısı kalite kıyasında referans alınırken bu bilinmeli.

### H29 — "Burası önemli" kuralları birbiriyle çelişiyordu; OCR'lı sayıda sıfır kayıp yanlış alarmı (2026-10-23)
- `TALIMAT_SESLI.md` her ilgili çıkmışta "Burası önemli" isterken `metin_denetle.py` (H22) toplamı `max(3, bölüm/2)` ile sınırlar
  → çok çıkmışlı derste ikisi birden sağlanamaz. Karar: H22 (daha yeni kullanıcı kuralı) esas; her çıkmış `vurgu tur=cikmis` ile
  işaretlenir, "Burası önemli" sınır içinde en çok sorulanlarda. Talimat güncellendi (Oracle'da sonraki dağıtımla); görev yolunda
  `sesli_bolum` bölüm başına en çok 1, birleştirici ders sınırını betikle uygular (`onem_sinirla`).
- Sesli metin ekranında sayılar yazıyla yazılmıştı ("iki yüz seksen gün") — okunuş ekrana sızması (önceki H "Okunuş ekrana");
  görev kuralı: ekran rakamla, okunuş yalnız `ses`te; sıfır kayıp kapısı bunu yakalar.
- OCR'lı tablo sayfasında bozuk sayılar ("185-249 kg/m" = 18,5–24,9) düzeltilerek anlatılınca sıfır kayıp kapısı yanlış alarm
  veriyordu → `baglam.ocr_sayfalar` sayfaları ve ondalık ayracı düşmüş eşdeğerler muaf.

## H30 — Çıkmış konu eşlemesi birebir olunca ders sessizce çıkmışsız kalıyordu (2026-10-23 K2 provası)
- Ders kayıt defterindeki konu "Gebelik Terminolojisi ve Kavramları", çıkmış bankasındaki müfredat konusu
  "Gebelik Terminolojisi/Kavramları" → `a_hazirla` 0 çıkmış buldu ve hata vermeden devam etti (önem listesi ve çözücü boş kalırdı).
- Düzeltme: `ders_zinciri.konu_eslesen_cikmislar` üç basamak: birebir → yazım farkı ("/", "&", "ve", noktalama) yok sayılarak →
  ≥0,92 benzerlik; hangi yolla eşlendiği günlüğe yazılır. Sınama: Gebelik 27 (yazım farkı), Sifilis 19 (birebir).

## H31 — Hesap sorusu yanlış alarmı + iç etiketin öğrenci metnine sızması (2026-10-23 K2 provası)
- Naegele tarih sorusunun doğru şıkkı ("10.02.2021") maddede yazmaz, kuraldan hesaplanır; önem görevinin çözülebilirlik kapısı
  "çözülemiyor" diyordu → doğru şık yalnız sayı/tarih/birimse kökteki kural terimlerinden ≥2'si maddede olması yeter.
- Ücretsiz model detay alanına "Q3 ve Q4'te verilen tarihler…" yazdı (öğrenci Q3'ü bilmez). Ortak kapı
  `cekirdek.etiket_sizintisi` (yönlendirici + `gorev.py dogrula`): pakette verilmiş kısa etiket öğrenci metninde kalırsa HATA;
  girdide tıbbi anlamda da geçen (S1 kalp sesi, L4 omur) muaf; iç veri görevleri `OGRENCI_METNI = False`. Kural `cikti_disiplini.md`.

## H32 — Zorluk parça içinde yuvarlanınca ders toplamı hedefin altında kalıyordu (2026-10-23 K2 provası)
- 6 parçanın 6'sı ücretsiz katmanda geçti ama birleştirme "zor %9 (hedef %15–25)" ile durdu: 3 soruluk parçada %20 zor → 0.
- Düzeltme: `_spot.zorluk_dagit` zorluğu ders düzeyinde dağıtıp parçalara dilimler; parça kapısı zor soruda plandan eksiği kabul etmez.

## H33 — Türkçe harfsiz metin kabul ediliyordu + kabul edilmiş iş yeni kapıdan geçirilmiyordu (2026-10-23 K2 provası)
- Gemini Flash-Lite bazı çözücü partilerini ve bir sesli bölümü baştan sona harfsiz yazdı ("dogum", "bagli", "oykusu");
  hiçbir kapı yakalamadı, partiler KABUL edildi (önceki e07 çözücü ve k1-64 sesli sınamalarında da vardı; yalnız geçici kopya).
- Ortak kapı `cekirdek.turkce_katlama`: sözlük paketin kendi girdisinden; girdide Türkçe harfle geçen kelimenin katlanmış
  biçimi ≥3 kelimelik bir alanda ≥2 kez varsa HATA (İngilizce alıntı, kimlik/tür alanı, büyük harfli OCR yanlış alarm vermez).
- Kabul edilmiş iş yeniden kullanılırken `yonlendir.kapi` ile güncel kapılardan geçirilir; geçemezse "yeniden" koşar.
- Betik onarımı `cekirdek.ses_onar` (SES_ONAR görevleri): ses alanlarında kısaltma/Roma rakamı `modul_okunus.donustur`
  ile ("MSH" → "mee see haa"); modelin üç turda düzeltemediği "büyük harfli kısaltma" hatası kalktı.
- Öncüllü soruda "kökle uzunluk uyumsuz" hatasına düzeltme ipucu eklendi (kok_ses öncüllerin hepsini okur).

## H34 — Ücretsiz katman zinciri: Gemini tavanı, Zen kapandı, OpenRouter eklendi (2026-10-23)
- Bir dersin önem + çözücü adımı ~50 Gemini çağrısı harcadı; ardından bütün Gemini anahtarları 429 ("quota" / "monthly
  spending cap"). "spending cap" dakikalık sınır sanılıp 20 sn bekleniyordu → artık anahtar tükenmiş sayılır.
- Zen: Muse Spark kaldırıldı (410), Zen ücretsiz katmanı yalnız OpenCode istemcisinden (403 FreeTierError) → zincirden çıktı
  (`MEDS_CLOUD_ZEN=1` ile geri açılır). 410 artık 404 gibi model atlatır.
- OpenRouter ücretsiz modeller zincire eklendi (`nvidia/nemotron-3-ultra-550b-a55b:free`, `google/gemma-4-31b-it:free`);
  görev defterinde `zen` yerine `openrouter`. Groq ücretsiz katmanında ~24 bin karakterlik düzeltme istemi 413 alıyor.

## H35 — Ücretsiz/yazılı içerikte betik kapılarından geçen tıbbi hatalar; denetim bulguları düzeltilmiyordu (2026-10-24)
- Betik kapılarından 0 HATA ile geçen 2x99 içeriğinde OpenCode GLM denetçisi gerçek hatalar buldu: gravida 8 yerine "7",
  çoğul gebelik minör iken "majör", VTE eşikleri ">4"/">2" yerine "4 ve üzeri"/"2 ve üzeri", ders dışı Leopold ayrıntısı.
- Düzeltme: denetim bulguları yazara geri döner (`yonlendir.bulgu_duzelt`), kapılar + önemde yapı sabit kalır
  (`onem_listesi.duzeltme_kisiti`: madde/örnek sayısı, puan), yeniden uygulanır ve yeniden denetlenir (iş başına ≤2 tur).
  2x99: 5 engelli işin 5'i OpenCode ile düzeldi, yeniden denetim 0 engelleyici.
- Yan hatalar: aynı W yolunda eski provaların işleri denetime karışıyordu → ders iş defteri `W/gorev/<kod>/isler.json`;
  çözücü `uygula` her çağrıda yeni numaralı dosya açıp kopya üretiyordu → dosya adı soru kimliklerinden, eski kopya temizlenir;
  önem değişince çözücü kaydı eski soruya göre kalabiliyordu → `cozucu_sorusu.eskiyen` kapısı (birleştirme HATA verir,
  çözücü adımı eskiyeni düşürüp yeniden üretir).

## H36 — Cümle sayacı sıra sayısı noktasını cümle sonu sayıyordu (2026-10-24, oturum kuyruğu sınaması)
- "8-10. haftalarda" iki cümle sayılıp "4 cümle (en çok 3)" yanlış alarmı veriyordu; yazar ifadeyi bozarak geçiyordu.
- `CUMLE_SINIRI` (cozucu_dogrula2.py, cozucu_dogrula.py, spot_cozucu/asistan_dogrula.py): rakamdan sonraki nokta ancak
  ardından büyük harfle başlayan cümle gelirse sınırdır. Sayım yalnız azalabilir; veri değişmedi.

## H37 — Oracle'da yayın/işaret yazamıyordu: sahiplik (2026-10-24)
- 16 Ekim'den beri hiçbir ders yayınlanamıyordu: `src/data` uid 1000 (`opc`, cihazdan `rsync -a` sahipliği), `data/sesli_anlatim`
  `root` (meds-app konteyneri ve `sudo rsync`); yayın ve işaret hizmetleri `ubuntu`. Düzeltme (kullanıcı onayı): `ubuntu` → `opc`
  grubu; sesli ders aktarımlarına `--chown=ubuntu:ubuntu`; `meds-ders-yayin` ve `meds-cumle-zaman` drop-in
  `ExecStartPre=+chown -R ubuntu:ubuntu data/sesli_anlatim` (konteyner root yazmaya devam eder).

## H38 — Sesli ders v2 slayt adımı hiç gösterilmiyordu (2026-10-24)
- `konusma_v2.py` şemasında `slayt_adim` adım KİMLİĞİ (`k2-02-d-s05`); sunucu yalnız sayıyı kabul ediyordu → bütün K2
  cümlelerinde adım bağı boş. `canliDers.ts` ve `.medspak` kimlikten numarayı çözer. Paket kapısı bunu yakaladı.

## H39 — Sesli metin kısaydı: sayfa atlanıyor, şekiller anlatılmıyordu (2026-10-24, kullanıcı "ders süresi az")
- k2-02'de 56 içerik sayfasının 12'si anlatılmamış, 19 sayfa tek cümleyle geçilmişti; "kısa ve öz" + paralel üretimde kapı yoktu.
  Kapı `isle.sesli_kapsam` (sayfa + derinlik). Kelime/dakika hedefi YOK; derinlik bilgi maddesi sayısından.

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
  yarı saydam sarı fosforlu dolgu + kırmızı hatla çizilir. Genel kurallar listesi: `scripts/cizim/TALIMAT_CIZIM.md`.

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

## H48 — Canlı sitede tasarım taraması bulguları (2026-10-24)
- Panel PDF yazı satırının kutusuna yapışıyordu (s.10 "Opioid overdozu ?", s.16 "Hipotermi?"): mürekkep eşiği harf
  gövdesini görür, satır kutusunu görmez → `yazi_kesisir` (panel ve etiket yazı satırı kutusundan 0,01 / 0,004 uzak).
- Dar PDF bölmesinde "Çiz" düğmesi harf harf alt alta kırılıyordu: ölçüt ekran genişliğiydi → bölme genişliği (container query).
- Oynatıcı, anlatılan satırları örtüyordu: görüntüleyici anlatılan satırlar oynatıcının altında kalırsa yetecek kadar kaydırır.
- Telefonda görünüm seçici (Metin / Metin + Slayt / Slayt) ayrı bir satır kaplıyordu → başlık satırında tek döngü düğmesi.
- Canlı tarama (telefon, Slayt, 4×): 46 panel/etiketin 45'i temiz; uzun etiket ("kollar fleksiyonda, bacaklar
  ekstansiyonda") kırpılıp yazıya biniyordu → etiket satıra iner, yerleşim satır sayısıyla. Hızlı dinlemede anlatılan satır
  oynatıcı altında kalıyordu (her cümlede sıfırlanan zamanlayıcı hiç çalışmıyordu) → iptal edilmeyen 600 ms kısıtlayıcı.
- Aynı paneldeki bağımsız "A → B" satırları farklı kırılıyordu (nalokson tek satır, flumazenil iki satır) → hizalı tablo
  (kaynak | ok | hedef sütunları, `is-tablo`); baskılama ucu ⊣ büyütüldü.
- Canlı tarama (telefon, Slayt, 2×, 8:08–16:07): etiket "tabloya uygun yaklaşım" (s.49) yazının üstüne konmuştu (yakında yer
  yokken yolun ortasına) → önce yakında yazısız yer, sonra yakında resmin ≤%25'ini örten ama yazıya değmeyen yer, sonra
  sayfada ≤0,35 uzaklıkta boş yer. Sonuç: 35 etiketin 0'ı yazı satırıyla kesişiyor. Sayfa geçişi kaydırması sürerken atlanan
  satır düzeltmesi kaydırma bitince yeniden denenir (masaüstü 2×'te s.11–19'da 2–13 sn örtme vardı).

## H49 — Kırılan zincirde ok yana bakıyordu; panel yazısı büyüktü; takip 8–16 sn duruyordu (2026-10-24)
- "beyin omurilik sıvısı incelemesi → santral sinir sistemi enfeksiyonu" satıra kırılınca ok yana bakıyordu → panel sürümleri
  (yatay/dikey × normal/kompakt), kırılan yatay zincir geçersiz → dikey (oklar aşağı). Panel yazısı %2,2 → %1,75 cqw.
- Canlı tarama (masaüstü, 2×): anlatılan satır 8–16 sn oynatıcı altında kalıyordu. Kök: satırı görünür alana alan program
  kaydırması kullanıcı gezinmesi sayılıp takibi 8 sn durduruyordu → program kaydırması bildirilmez.
- Bütün kurallar tek belgede: `docs/CIZIM_KURALLARI.md` (her kurul, her ders, her PDF).

## H50 — Panel tıbben yanlış okunuyordu; takip kaydırması sessizce boşa gidiyordu; ekran kalabalıktı (2026-10-24)
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

## H51 — Resim slaytında anlatım görselin yerine panelde; yatay zincirde kutular kırılıyordu; testler bunları görmüyordu (2026-10-24)
- Herniasyon şeması anlatılırken altta 5 öğeli yatay zincir paneli; kutular 3–4 satıra kırılıp panel sayfadan 333–692 px
  taşıyordu. Maske paneli "Görünen: Alkol" anlamsızdı. Grup panelinde numaralar basılmıyor, ok sözü kesiliyordu.
- Kök: sınama yalnız panel kutusunun taşmasını ölçüyordu (iç taşma, satır kırılması, kesik söz yoktu) ve elle yapılıyordu.
- Düzeltme: `resim_sayfasi` kapısı (görsel slaytta panel yok; 7 sayfa Claude ile görselin üstünde yeniden çizildi), yatay zincir
  tek satır yoksa dikey, maske "İlk izlenim / ⚠ maskeleyebilir / Atlanmaması gereken", liste numaraları, grup ızgarası.
  Kalıcı otomatik kapı `scripts/cizim/panel_sinama.mjs` (366/567/1100 px, 8 hata türü) ders zincirinde; düşen çizim yayına gitmez.

## H52 — Etiket çizimden kopuk; PDF'in kendi oku yeniden çiziliyordu (2026-10-24, s.14 ve s.27 görsel denetimi)
- s.14 "santral herniasyon" etiketi 3 numaralı okun yanında, "tonsiller" etiketi 6'dan uzakta; s.27'de slaytın kırmızı okları
  mavi okla kopyalanıyordu. Düzeltme: etiket önce hedef kutusunun (odak çerçevesi / boyalı bölge / ok ucu) hemen yanında
  aranır, uzaksa kesikli bağlantı çizgisi (`etiket_hedef`); uçları PDF aday okuna ya da a→b boyunca çizili hatta (kenar ≥%80)
  denk gelen ok yeni çizilmez, o ok çerçevelenir (`pdf_oku` → odak). k2-02: 9 ok çerçeveye çevrildi, 19/41 etiket bağlantılı.

## H53 — Resim üstündeki çizim asıl yapının önünü kapatıyordu (2026-10-24)
- Kullanıcı: "o bölgeye zoom yapılsın, çizilsin, geri dönülsün". Düzeltme: `cizim_uret.yakinlasma` → komutta `yakin`;
  `CizimLayer.yakinUygula` sayfa katmanlarını yumuşakça büyütür/geri döndürür (cümle başına tek birleşik hedef; ilk denemede
  iki çizim arasında gidip geliyordu). k2-02: 25 çizimde (10 sayfa) yakınlaşma; yerelde gerçek ekranda ölçüldü.

## H54 — Benzer soru araması boş döndü, ders çıkmışsız üretildi (2026-10-24, k2-07 ikinci sınama)
- k2-07 Genel Anestezik İlaçlar: veritabanında bu konunun 19 çıkmışı varken `cikmis_adaylari` 30 sorguda da 200 + boş
  sonuç aldı (dizin o an hazır değildi). Hata sayılmadı: "0 çıkmış bağı", sesli metinde "0 önemli" vurgu.
  Birkaç dakika sonra aynı arama 40 aday verdi.
- Kapı: `isle.cikmis_adaylari` bütün sorgular boş gelirse 60 sn bekleyip bir kez yineler, yine boşsa iş durur (sonra
  yeniden dener). Çıkmışı gerçekten olmayan yeni konu yine üretilir; yalnız *hiçbir sorgu sonuç vermezse* durur.

## H55 — Görsel tablodan yanlış satır okundu; hocanın kendi çelişkisi kesin "sınav spotu" yapıldı (2026-10-24, k2-07)
- Bütün betik kapıları 0 HATA iken bağımsız tıbbi denetim (PDF ile satır satır) buldu:
  - s.63 Tablo 25.3 (görüntü): droperidol premedikasyon/sedasyon/antiemetik dozları **midazolama** yazılmış; kart, soru,
    checkpoint ve sesli metne yayılmış. Aynı tablonun opioid yarısı atlanmış.
  - s.6 "en zayıf desfluran" ↔ s.13 Tablo 25.1 MAK azot protoksit >100: iki zıt cevap öğretiliyordu. Kural: hocanın
    çelişkisi tek cümlede uzlaştırılır (halojenli uçucular içinde desfluran; tüm inhalerler içinde N₂O), kesin spot yapılmaz.
  - Tablodaki 0 değeri "seyrek" diye okunmuş (midazolam bradikardi); "(Katzung)", "standart kaynaklara göre" ekleri sızmış.
- Kural: Kurul 2+ her derste yayından önce PDF'le karşılaştıran bağımsız tıbbi denetim (ayrı oturum, yazar ≠ denetçi)
  zorunlu; görsel tablo satırı ilaç/değer eşlemesi görüntüden tek tek doğrulanır. Bulgular düzeltilip kapılar yeniden koşulur.

## H56 — Yeni yayınlanan dersin PDF'i uygulamada açılmıyordu (2026-10-24, kullanıcı, k2-07)
- Deste → PDF eşlemesi (`build_deck_pdf_sources.py` → `meds_downloads/_deck_pdf_sources.json`) yalnız işçinin Drive
  taramasında (50 dk) yenileniyordu; k2-07 21:47'de yayınlandı, eşleme 21:14'tendi → ders PDF'siz. PDF sunucu diskinden
  verilir (`/api/lecture-pdf/deck/<deste>/<n>`); Drive yalnız sunucusuz yedek yoldur.
- Düzeltme: `yayinla.py` yeni ders yayınlayınca `_pdf_eslesme_yenile()` → işçi kapsayıcısında `izle.pdf_eslesme_guncelle()`
  (günlükte "PDF eşleşmesi: yenilendi"). Kapı: yayından sonra `/api/lecture-pdf/deck/<deste>/0` 200 dönmeli.
- `.medspak` öğrenci paketi PDF taşımaz (tasarım: `ek` yalnız `--ekler` yönetici dışa aktarımında); uygulama PDF'i paketten değil sunucudan açar.

## H57 — Kurul 2 derslerinde çıkmışlar neredeyse hiç duyulmuyordu (2026-10-24, kullanıcı)
- Kurul 1'de derste 11–13 "Burası önemli", 33–40 çıkmış/sınav anışı vardı; k2-07'de 4/0, k2-02'de 1/2. Bilgi anlatılıyor,
  `cikmis` alanına bağlanıyordu ama sesli söylenmiyordu: H22 dolgu yasağı + `max(3, bölüm/2)` "Burası önemli" tavanı
  dayanaklı çıkmış uyarısını da sildi. k2-02'de ayrıca arama tek aday döndürmüştü (H54).
- Kural: çıkmış uyarısı dolgu DEĞİLDİR. Her `ilgili` çıkmışın bilgisi anlatılır ve ilk geçtiği cümlede sesli söylenir
  ("bu bilgi çıkmışta soruldu"); tavan yalnız çıkmış dayanağı olmayan "Burası önemli"ye uygulanır. Dayanaksız çıkmış anışı yasak.
- Kapı: `isle.cikmis_ses_kapsam` (sesli_kapsam'a bağlı, Kurul 2+): ilgili çıkmış anlatılmamış / sesli uyarısız → HATA;
  "çıkmış/sınavda soruldu" geçen cümlede `cikmis` boş → HATA. Arama kurul filtresiyle <10 aday dönerse filtresiz yedek arama.

## H58 — EMA cümle ortasında sesi düşürüp es veriyordu (2026-10-24, kullanıcı)
- Kök: `ema_lightning/chunker.py` ~10 sn'yi (hız 1'de 180 harf) aşan metni son virgülde ya da düz boşlukta kesip parça
  sonuna "." ekliyor, araya 0,12–0,25 sn es koyuyordu → cümle bitmiş gibi kapanış tonu. Virgülde de virgülsüz yerde de oluyordu.
- Düzeltme: `ema_isci.model_yukle()` `chunker.MAX_SECONDS=30`, `MAX_LETTERS=750` (bütün EMA betikleri bu yoldan geçer);
  kesim yalnız gerçek cümle sonunda. Kurul 1 sesleri bilerek yeniden üretilmedi (kullanıcı kararı); K2'de etkilenen tek
  klip (k2farmakoloji 2f01 q-26) yenilendi.
- Kural: bu sınır geri çekilmez; tek cümle 30 sn'yi aşıyorsa metin aşamasında bölünür. Sayım betiği: kütüphanenin
  `chunker.chunk` çıktısında `SENTENCE_PAUSE` dışı kesim = hata.

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
  "resim" sayılıp bütün slayt çerçeveleniyordu. **Kural:** her ders `scripts/cizim/cizim_kapisi.py` (K1–K9) 0 HATA olmadan
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

## H62 — Quiz Üretiminde Öncelik Sırasının İhlali, Çifte Analiz Maliyeti ve Yarış Durumu Hatası (2026-10-26)

- **Belirti (Risk):** Drive'a yeni ders geldiğinde Quiz ajanlarının Sesli Ders süreci tamamlanmadan devreye girmesi, sesli dersin analiziyle quiz analizinin mükerrer yapılması (duplikasyon), dosya ezilmesi (overwrite) veya henüz onaylanmamış sesli ders taslağı üzerinden tutarsız soru havuzu üretilmesi.
- **Kök Neden:** Pipeline adımları arasında katı bir durum bağımlılığı (state dependency) ve tekil analiz deposu (Single Source of Truth) olmaması; modüllerin asenkron veya paralel başlatılması durumunda yarış durumu (race condition) doğması.
- **Çözüm & Kural:**
  1. **Öncelik Kilidi (Priority Lock):** Sesli Ders (Audio Lesson) `COMPLETED` (onaylı `konusma_v2.json` ve 0 HATA denetim) durumuna geçmeden Quiz soru üretim ajanları KESİNLİKLE tetiklenemez.
  2. **Kapsam Kilidi (Scope Lock):** Quiz üretimi şimdilik YALNIZCA `Farmakoloji` (`Tıbbi Farmakoloji`) dersi için aktiftir. Kod altyapısı ders-bağımsız (`course-agnostic`) kurulmuştur.
  3. **Single Source of Truth:** Sesli dersin ilk analiz adımında üretilen `atomik_bilgi_envanteri.json`, hem Sesli Dersi hem de ardından çalışacak Quiz Ajanını besler. İkinci bir LLM analizi yapılmaz; mükerrer araştırma yasaktır.
  4. **2x Çapraz Sorgulama ve Batch Processing:** $N$ atomik bilgi $\rightarrow$ en az $2N$ soru. Token limitine takılmamak için en fazla 25 atom (50 soru) partileri halinde döngüyle işlenir.
- **Kapı:** `meds/scripts/quiz_motoru/quiz_dogrula.py` (Öncelik kilidi, 2x soru kuralı, 5-15 sn okunma süresi, gerekçeli şık açıklamaları, sıfır halüsinasyon). Çıkış kod 0 olmadan yayın yapılamaz.

## H63 — Sesli Derslerde Arşiv PDF'lerinin Çok Geç Yüklenmesi veya Hiç Yüklenmemesi (AutoFetch, SW Range ve Linearization Hatası) (2026-10-26, kullanıcı)

- **Belirti:** Sesli derslerde 2025-2026 arşivi açıldığında slayt PDF'leri ya dakikalarca yüklenmiyor (uzun süre `%...` ilerleme çubuğunda bekliyor) ya da hiç yüklenmiyor (Cloudflare tunnel `context canceled`, zaman aşımı veya boş ekran).
- **Kök Neden:** 
  1. `PdfDocView.tsx` içinde `disableAutoFetch: !(boyut > 0 && boyut <= 15 * 1024 * 1024)` kuralı nedeniyle 15 MB altındaki tüm PDF dosyalarında autoFetch açık kalıyordu. PDF.js, ilk sayfa için range isteği atmak yerine arka planda bütün 5-15 MB'lık dosyanın stream indirmesini başlatıyor ve ilk sayfa çizimi bu dev stream bitene kadar bloke oluyordu.
  2. `public/sw.js` dosyasında ses akışları (`/api/canli-ders/ses/` vb.) Range/206 muafiyetindeyken `/api/lecture-pdf/` akışları bu listeye eklenmemişti. İstemci çevrimdışı paketini indirmediğinde istek SW'nin genel `/api/` Network-First bloğuna düşüyor; Service Worker Range isteklerini `fetch(req)` ile yakalayıp tarayıcının yerel Range motorunu bozuyor ve dönen yanıtları `DATA_CACHE`'e yazmaya çalışarak iş parçacığını kilitliyordu.
  3. Arşivdeki PDF dosyalarının hiçbiri linearize (Fast Web View) formatında değildi (0/65). Linearize olmayan PDF'lerde katalog ve xref tablosu dosyanın sonunda olduğu için autoFetch ile yarışan range istekleri zaman aşımına uğruyordu.
  4. Sunucu `Accept-Ranges: bytes` ve `public, max-age=604800, stale-while-revalidate=86400` başlıklarını eksik döndürdüğünden CDN ve ara katmanlar byte-range parçalarını önbellekleyemiyordu.
- **Çözüm & Kural:**
  1. `PdfDocView.tsx`: `disableAutoFetch: true` ve `rangeChunkSize: 256 * 1024` sabitlendi. PDF.js artık asla tüm dosyayı arka planda otomatik çekmez; yalnızca o an görüntülenen sayfanın 256 KB'lık dilimini çeker ve ilk sayfa 1 saniyenin altında ekrana gelir.
  2. `public/sw.js`: `/api/lecture-pdf/` akışları Service Worker tamponlama ve cache mekanizmasından tamamen muaf tutularak (`return;`) doğrudan tarayıcının yerel yüksek hızlı ağ motoruna bırakıldı (`SW v16`).
  3. `pikepdf` motoru ile tüm arşiv PDF'leri linearize edildi (Fast Web View); ilk sayfa ve xref tablosu dosyanın ilk kilobaytlarına taşındı.
  4. `server.ts`: `/api/lecture-pdf/deck/:deckId/:index` için `Accept-Ranges: bytes` ve `public, max-age=604800, stale-while-revalidate=86400` başlıkları eklendi.




## H64 — Sayfa haritası adım numaraları tekrar sayfalarını saymıyordu; kısa/eksik kanıt (2026-10-26, k2-22 psikosomatik)
- **Belirti:** `denetle.py` 76 HATA: adım 8–31 için "pdfSayfalari [n] ama harita [n+1] diyor", başlık aralıkları içerik adımı değil, bilgi/harita alıntıları 3 kelime ya da yok.
- **Kök neden:** `sayfa_haritasi.json` `adimlar` alanı desteden ayrı, CHECKPOINT slaytları sayılmadan numaralandırılmıştı; her checkpoint'ten sonra kayma büyüdü. Yalnız görsel olan sayfalarda (s.6, s.30: kaynak.md metni yok) `alinti` yazılamadığı için kanıt boş bırakılmıştı; tablo/liste sayfalarında tek satırlık (3 kelime) alıntı seçilmişti.
- **Çözüm / kural:** Harita `adimlar`ı daima son destenin içerik slaytlarının `pdfSayfalari`ndan türetilir (checkpoint/oyun hariç); başlık `adimlar` = kapsadığı sayfaların ilk/son içerik adımı. Metinsiz görsel sayfada `kanit: {sayfa, gorsel: "≥4 kelime görülen"}` kullanılır; alıntı kaynak.md'de birebir geçen ≥4 kelime olur.

## H65 — Tablo sayfasında tabloyu anlatmayan cümleye şekil/tablo çapası (2026-10-26, k2-23 cinsel kimlik)
- **Belirti:** `arsiv_yayinla.py` 4/6'da `cizim_kapisi.py` 1 HATA: `K1 P19.C3: şekil çapası var ama lazer sayfa (s.21)`.
- **Kök neden:** s.21 (organik/psikojenik karşılaştırma tablosu) paragrafındaki son cümle ("Çıkmışta da sorulduğu gibi… tıbbi durum ve kullandığı ilaçlar değerlendirilir") tablonun hiçbir satırını anlatmıyor (`satir: []`), ama yazar paragrafın tüm cümlelerine aynı `sekil`/`tablo: true` çapasını kopyalamıştı. Eşleşecek tablo satırı olmadığından lazer tabloya değil sayfaya düştü.
- **Çözüm / kural:** Şekil/tablo çapası yalnız görseli/satırı gerçekten anlatan cümleye yazılır; paragrafın sonraki cümlelerine kopyalanmaz. Tablo çapalı cümlede `satir` boşsa çapa yazılmaz. Düzeltme: o cümlenin `sekil`'i `null` yapıldı, `tablo` kaldırıldı (capa + v2 + taslak kopyaları, `sekil_cizim.py sus` ile aynı yöntem); kapı gevşetilmedi, yayın 0 HATA ile tamamlandı.

## H66 — İlgili çıkmış sorular sesli derste hiçbir cümleye bağlanmamış (2026-10-26, k2-24 epilepsi)
- **Belirti:** `arsiv_yayinla.py` 1/6'da 8 adet `sesli_kapsam: çıkmış …: bilgisi anlatılmamış (cümlenin cikmis listesine bağla)`.
- **Kök neden:** Bilgiler anlatılmıştı (s.5, 15, 33, 45, 50), ama `cikmis_baglantilari.json`'da `ilgili: true` olan sorular `konusma_v2.json` cümlelerinin `cikmis` listesine yazılmamıştı (tüm cümlelerde `cikmis: []`); sesli çıkmış uyarısı da yoktu.
- **Çözüm / kural:** Yazar, `ilgili: true` her çıkmışı `kanit.sayfa`/`slideNumber` sayfasında bilgiyi taşıyan cümlenin `cikmis` listesine bağlar ve o cümlede sesli uyarı ("Bu bilgi çıkmış sorularda soruldu.") verir. Kapı (`isle.py::cikmis_ses_kapsam`) gevşetilmedi.

## H67 — H64 tekrarı: harita adımları checkpoint'siz sayıldı + deste `bolum` alt başlık numarası (2026-10-26, k2-26 nörolojik hastalıklar genetiği)
- **Belirti:** `denetle.py` 112 HATA: "pdfSayfalari [n] ama harita [m] diyor", başlık aralıkları içerik adımı değil, "bolum '1.1' basliklar'da yok", ana başlıklar 54/60 adımı kapsıyor.
- **Kök neden:** (1) `sayfa_haritasi.json` `adimlar` (sayfa ve başlık) içerik sırası (1..60) ile yazıldı, `slideNumber` (checkpoint dahil 1..68) ile değil — H64'ün aynısı. (2) 1. parçanın slaytlarına `basliklar`da olmayan alt numara (`1.1`–`1.8`) yazıldı. (3) Fakomatoz (s.61–71) ve işitme (s.90–102) sayfalarında harita bir adım kaymış; adım 1'e s.3 (içindekiler) dahil edilmiş.
- **Çözüm / kural:** Harita `adimlar` daima deste `slideNumber`'ıdır; `bolum` yalnız `basliklar[].no` değerlerinden biri olur (alt başlık yoksa ana no). Kayma görülürse hangi tarafın doğru olduğu sayfa `ne_anlatiliyor` ile slayt başlığı karşılaştırılarak seçilir; içindekiler/kapak sayfası hiçbir adımın `pdfSayfalari` aralığına girmez.

## H68 — H66 tekrarı + süs bölüm sayfaları `sekil` türünde (2026-10-26, k2-27 periyodik muayeneler)
- **Belirti:** `arsiv_yayinla.py`'de 15 `sesli_kapsam: çıkmış …: bilgisi anlatılmamış` + 8 "s. n (sekil) anlatılmamış" (bölüm başlık/kapanış süs sayfaları).
- **Kök neden:** (1) H66'nın aynısı: 248 cümlenin hiçbirinde `cikmis` dolu değil, ilgili 15 soru bağlanmamış. (2) `sayfa_haritasi.json`'da yalnız süs görselli bölüm başlık sayfaları (s.18, 26, 39, 51, 52, 107, 130, 135) `tur: sekil` yazılmış; kapı bunları anlatılacak şekil sayar.
- **Çözüm / kural:** Çıkmışlar `kanit.sayfa` cümlelerine bağlandı (c0003, c0037, c0047, c0101, c0112, c0204, c0213, c0218, c0222) ve sesli uyarı eklendi; süs bölüm sayfaları `tur: kapak` yapıldı. Haritacı, bilgi taşımayan bölüm başlık/kapanış sayfalarını `kapak` yazar; sesli yazar H66 adımını atlamaz. Kapı gevşetilmedi.

- **2026-10-26 (k2-29):** `cikmis_baglantilari.json`'da `ilgili: true` olan çıkmışın bilgisi cümlede anlatılsa da cümlenin `cikmis` listesine kimliği yazılmadı ve sesli uyarı yoktu → `sesli_kapsam` yayını durdurdu. Önleme: sesli metin yazarı her ilgili çıkmışı `kanit.sayfa` sayfasındaki cümleye bağlar ve o cümlede "bu bilgi çıkmışta soruldu" der (kapı: `isle.cikmis_ses_kapsam`).

## H69 — `cikmis_baglantilari.json` liste yerine nesne sarmalayıcısıyla yazıldı (2026-10-26, k2-46 sempatomimetikler)
- **Belirti:** `arsiv_yayinla.py` 5/6'da `AttributeError: 'str' object has no attribute 'get'` hatası vererek durdu (`bag_sayisi = len([x for x in json.loads(...) if x.get("ilgili")])`).
- **Kök neden:** `cikmis_baglantilari.json` dosyası doğrudan liste (`list[dict]`) olmak yerine `{"baglantilar": [...]}` şeklinde sözlük olarak yazılmıştı. Sözlük üzerinde iterasyon yapıldığında string anahtarlar dönmüş ve `.get()` patlamıştı.
- **Çözüm / kural:** `cikmis_baglantilari.json` daima kökte bir liste (`[{"soru_id": ..., "soru": ..., "ilgili": bool, "aciklama": ...}]`) olarak yazılır. `denetle.py` ve `arsiv_yayinla.py` doğrudan liste formatı bekler. Dosya düzeltildi, 0 HATA ile Oracle'a dağıtıldı.

## H70 — Mekanik 2 Cümlelik Şablon ve Yüzeysel Anlatım Yasağı (Sıfır Bilgi Kaybı ve Amfi Derinliği Standardı) (2026-10-26, k2-48 lokal anestezikler)
- **Belirti:** Kullanıcı uyarısı: *"Son eklenen dersler hep eksik anlatılmış içeriklerinin neredeyse %60'ı yok"*. 37 sayfalık amfi dersi yalnızca 74 cümle ve 839 kelime (~6.7 dakika) ile geçiştirilmiş; slaytlardaki kimyasal gruplar, spesifik formülasyonlar (Anestol, EMLA, Jetex, Lidestol, Lincaine, LMX-4, Vemcaine), subkutan maksimum doz tablosu (Ultrakain, Citanest, Marcaine, Naropin), potens katsayıları (tetrakain/bupivakain 16 kat), difüzyon ve iyonizasyon eğrileri (pKa 7.9 lidokain vs 8.1 bupivakain), toksisite basamakları, diazepam premedikasyonu ve %20 intravenöz lipid emülsiyon protokolü sesli anlatımda yer almamıştı.
- **Kök neden:** Taslak ve sesli metin üretiminde sayfa başına mekanik olarak tam 2 kısa cümle yazan bir şablon kullanılmış; bu şablon kapıların asgari kelime/sayfa şartlarını yüzeysel olarak karşılasa da gerçek amfi anlatımının %60–75'ini dışarıda bırakmıştı.
- **Çözüm / kural:** Sayfa başına yüzeysel 2 cümlelik kopyala-yapıştır şablonlar KESİNLİKLE YASAKTIR. Her slayt için amfi ders notundaki tüm maddeleri, tabloları, spesifik ilaç isimlerini, maksimum dozları ve patofizyolojik mekanizmaları kapsayan 3 ila 6 zengin cümle yazılmalıdır (35–70 slaytlık dersler için 140–250+ cümle, ~2000–3500 kelime, 15–25 dakika anlatım derinliği). K48 bu standartla baştan üretildi (144 cümle, 2438 kelime, 68 atomik bilgi, 10/10 çizim, 6.23 MB .medspak) ve 0 HATA ile Oracle canlı ortamına alındı.


## H71 — PDF metnindeki ayrışık (decomposed) harfler terim eşleşmesini bozuyordu (2026-10-26, k2-07 genel anestezik ilaçlar)
- **Belirti:** `terim_sozlugu.py dogrula` doğru yazılmış terimler için "bu sayfanın metninde bulunamadı" HATAsı verdi: "retiküler aktive edici sistemde", "Antikonvülzandır", "venöz irritasyon". Slayt metnini `dok` çıktısında da "retiküler" gibi bozuk görünüyordu.
- **Kök neden:** PDF'ten gelen kelimede "ü" tek kod noktası değil, "u" + birleşik inceltme (U+0308) olarak ayrışık yazılmıştı. `TOK` düzeni birleşik işareti kelime karakteri saymadığı için kelime iki parçaya bölünüyor, `katla()` sonrası "antikonvu" + "lzandir" gibi anlamsız parçalar oluşuyordu; terim hiçbir zaman eşleşmiyordu.
- **Çözüm / kural:** `Sayfa` sınıfı PDF kelimelerini okurken `unicodedata.normalize("NFC", w)` uygular; `bul()` de terimi NFC'ye çevirip token'lara ayırır. Kapı gevşetilmedi. Yeni PDF okuyan her betik kelimeleri NFC'ye çevirmeden eşleştirme yapmamalıdır.

## H72 — Çok sözcüklü terimin kısa son sözcüğü ek aldığında eşleşmiyordu (2026-10-26, k2-07 genel anestezik ilaçlar)
- **Belirti:** "Serebral metabolik hız" terimi slaytta "Serebral metabolik hızın azaltılması" olarak geçtiği hâlde "bulunamadı" HATAsı verdi.
- **Kök neden:** `ek_mi()` yanlış eşleşmeyi önlemek için 4 harf ve altındaki sözcüklerde yalnız birebir eşleşmeye izin veriyordu; "hız" 3 harf olduğu için "hızın" reddediliyordu. Oysa terimin önceki sözcükleri ("serebral metabolik") bağlamı zaten daraltıyor.
- **Çözüm / kural:** `ek_mi(..., kisa_izin=True)` yalnız **çok sözcüklü** terimin **son** sözcüğünde ve terim en az 8 karakterken kullanılır; tek sözcüklü kısa terimlerde (kısaltmalar) davranış değişmedi. Eşleşme gevşetilmedi, yalnız Türkçe ek kuralı bağlamla birlikte uygulandı.

## H73 — `terim/` klasörü dağıtım betiğinin veri listesinde yoktu; terim dosyaları canlıya ulaşamıyordu (2026-10-26)
- **Belirti:** Terim yardımcısı yerelde çalışıyor, canlıda `/api/canli-ders/...` yanıtında `terim` alanı hiç gelmiyordu (k2-02, k2-07 dahil tüm dersler).
- **Kök neden:** `deploy-code.sh` ana rsync'i `/data` klasörünü dışlıyor; `data/sesli_anlatim` altındaki klasörler [1b] adımındaki sabit listeden aktarılıyor. Liste `metin hizalama vurgu capa cizim ogrenci_not cikmis_konum` idi ve `terim` eklenmemişti; yeni bir veri türü eklenirken dağıtım listesi güncellenmemişti.
- **Çözüm / kural:** Listeye `terim` eklendi. `data/sesli_anlatim` altına yeni bir veri türü ekleyen her oturum, `deploy-code.sh` [1b] listesini de günceller; dağıtımdan sonra canlı API yanıtında alanın varlığı `curl` ile doğrulanır.

## H74 — Madde imi kelimeye yapışık gelince terim işaretlenemiyordu (2026-10-26, k1-35 prenatal tanı)
- **Belirti:** "CVS", "Fetoskopi", "Koryon villus biyopsisi", "PAPP-A", "İnvaziv yöntemler" terimleri slaytta açıkça yazdığı hâlde kapı "bu sayfanın metninde bulunamadı" HATAsı verdi.
- **Kök neden:** Slaytlarda madde imi Wingdings "o" karakteridir ve PDF metnine kelimeye bitişik geliyor ("oCVS", "oFetoskopi", "oİnvaziv"). `TOK` bu birleşik diziyi tek kelime saydığı için "ocvs" üretiliyor, gerçek terim hiç eşleşmiyordu.
- **Çözüm / kural:** `Sayfa` kelimeyi okurken baştaki "o" yalnız **ardından büyük harf geliyorsa** (madde imi kalıbı) ayrılır; kutu aynı kalır. Madde başındaki terimler de artık işaretlenir. Kapı gevşetilmedi.

## H75 — Gündelik Türkçe sözcükler terim diye işaretlenmişti (2026-10-26, tüm dersler)
- **Belirti:** Öğren ekranında "Büyüme", "Kanama", "Gelişim", "Sarılık", "İyileşme", "Kalp yetmezliği", "Bilinç" gibi gündelik sözcükler terim gibi altı çiziliyor, dokununca sözlük tanımı açılıyordu; okuma bölünüyordu.
- **Kök neden:** Terim dosyalarının bir bölümü, `turkce_kokenli` kapısı eklenmeden önce `otomatik`/sözlük yolundan üretilmişti. Sözlükte bu sözcükler "terim" olarak kayıtlı olduğu için işaretlenmiş, kapı sonradan eklendiğinde dosyalar bir daha denetlenmediğinden canlıda kaldılar (kapı yalnız yeni yazımı denetliyor, var olan dosyayı taramıyordu).
- **Kalıcı çözüm:** `terim_sozlugu.py ayikla [--yaz]` bütün terim dosyalarını (canlı + arşiv) tarayıp kapının reddettiği ögeleri çıkarır; terimi kalmayan sayfa/dosya kaydı silinir (hiçbir dosyada boş `t` dizisi bulunmaz). Bu turda 514 öge ayıklandı, kapı gevşetilmedi.
- **Önleme kuralı:** Terim kapısı kuralı değiştiğinde yalnız yeni dosya değil, **tüm mevcut dosyalar** yeni kuralla yeniden taranır (`ayikla`), sonuç canlıya dağıtılır.

## H76 — Cümle sayısı kapısı kısaltma noktalarını cümle sonu sayıyordu (2026-10-26)
- **Belirti:** "Gebeliğin 20. ile 37. haftaları arasında gerçekleşen doğumdur" ya da "Geniş spektrumlu 3. kuşak sefalosporindir" gibi tek/iki cümlelik açıklamalar "en çok 2 cümle" HATAsı veriyordu; 167 terim bu yüzden canlıda kural dışı görünüyordu.
- **Kök neden:** Denetim `[.!?](\s|$)` kalıbıyla her noktayı cümle sonu sayıyordu. Sıra sayısı ("3."), ölçü ("20.") ve tür kısaltması ("N. gonorrhoeae", "C. trachomatis") noktaları da sayıldığı için cümle sayısı şişiyordu.
- **Kalıcı çözüm:** Cümle sonu ancak noktadan sonra **büyük harf** ya da metin sonu geliyorsa sayılır (`[.!?](?=\s+[A-ZÇĞİÖŞÜ]|\s*$)`). Gerçek üç cümleli açıklama hâlâ HATA alır; kural gevşemedi, yanlış sayım düzeldi. Ayrıca "frenler"/"çapası" gibi çeviri mecazları (8 terim) doğal Türkçeyle yeniden yazıldı.

## H77 — Kısaltma katmanı eklenirken üç ayrı tuzak: büyük harfli Türkçe sözcük, tireyle bitişik yazım, dağıtım listesi (2026-10-26, Kurul 2 · 60 ders)
- **Belirti:** Slayt kısaltmaları (ÜSYE, DD, VUR, DSM-5, MAO-A, 5-HTTLPR …) işaretlenirken (a) "BİLİNÇ", "KOMA", "NÖBET", "CEYLAN" gibi büyük harfli Türkçe sözcükler/başlıklar kısaltma sanıldı, (b) "DSM-5", "MAO-A", "HIV-1", "GABAA-reseptör", "5-HTTLPR", madde imli "o5-HTT" yazımlarında "kutular bulunamadı" HATAsı verdi, (c) kısaltma dosyaları yazıldığı hâlde canlıya hiç ulaşmadı.
- **Kök neden:**
  1. Kısaltma sezgiseli yalnız "büyük harf dizisi" kalıbına bakıyordu; Türkçe sözlük (hunspell) denetimi yoktu.
  2. Kutu araması terim kapısının `bul()` kuralını kullanıyordu; bu kural yalnız **tam kelimeyi** (ya da Türkçe ekini) eşler. Tireyle/rakamla bitişik yazımlarda kısaltma ayrı bir kelime olmadığı için hiç bulunamıyordu. Ayrıca madde imi "o" yalnız ardından **büyük harf** gelirse ayrılıyor; "o5-HTT" gibi rakamla gelen yazımda "o5-" önek olarak kalıyordu.
  3. `deploy-code.sh` [1b] veri listesine `kisaltma` eklenmemişti (H73'ün aynısı).
- **Çözüm / kural:**
  1. `kisaltma_mi()` artık `/usr/share/hunspell/tr_TR.dic` köklerini (ek soyma ile) kullanır: sözlükte bulunan büyük harfli sözcük kısaltma sayılmaz. Bilinen/elle sözlükte (`kisaltma_bilinen.json`, `kisaltma_elle/`) açıkça tanımlı kısaltmalar (SAK, KS gibi Türkçe sözcüğe benzeyenler) bu filtreden muaftır.
  2. `kutular()` eklendi: tam eşleşme yoksa kısaltma, kelime içinde **önek/sonek sınırı** denetlenerek (ör. "o5-httlpr", "t12-l1", "dsm-iii-r", "gabaa-reseptor") karakter oranıyla daraltılmış kutuda işaretlenir. Kapı gevşetilmedi; yalnız doğru konum hesaplandı.
  3. Dağıtım listesine `kisaltma` eklendi; canlı API'de `kisaltma` alanı `curl` ile doğrulandı.
- **Önleme kuralı:** (i) Her yeni veri türü hem `canliDers.ts` yol tanımına hem `deploy-code.sh` [1b] listesine yazılır. (ii) Kısaltma/açılım **yalnız dersin kendi metninden ya da elle/bilinen sözlükten** alınır; metinde açılımı olmayan kısaltmaya tahminle açılım yazılmaz (yanlış açılım, eksik açılımdan kötüdür).

## H78 — Gece otomatik LLM hattı kullanıcının Claude limitini tüketti; Oracle ders işçisi manuel moda geçişin dışında kalmıştı (2026-10-27)
- **Belirti:** 26.10 gecesi kullanıcıdan habersiz ~266 `claude -p` çağrısı (00:00–04:00, arşiv şekil/çizim onarımı `sekil_cizim.py`
  partileri) ve Oracle `meds-ders-isci` konteyneri (`CLAUDE_CODE_OAUTH_TOKEN` ile, `duraklat:false`, `otomatik_tarama:true`,
  günde 8 ders, 50 dk'da bir tarama) aboneliğin limitini bitirdi.
- **Kök neden:** (1) 26.10'daki "manuel mod" yalnız yerel systemd birimlerini durdurdu; Oracle konteynerindeki `/isci/ayar.json`
  ayrı bir dosyaydı ve değişmedi. (2) LLM çağıran betiklerde ortak bir "elle komut" kilidi yoktu. (3) Sunucuda Gemini onarım
  işçisi (`startAutoRepairWorker`, 20 sn) ve Faz14 kullanıcı kuyruğu (bildirim gelince / 10 dk'da bir) kendiliğinden LLM'e gidiyordu.
- **Çözüm:** Oracle işçisi durduruldu (`restart=no`, ayar duraklat/otomatik kapalı/günlük 0), `.env` anahtarı `#KAPALI`;
  `meds-hat-gece`, `meds-olasi-soru` maskelendi; `otomasyon/llm_kilit.py` (MEDS_LLM_ELLE=1 yoksa çıkış 75, systemd altında
  panel bayrağı şart) 11 betiğe ve `yonlendir._claude/_ajan`'a bağlandı; Gemini onarım işçisi duraklatılmış başlar, Faz14
  kuyruğu yalnız `POST /api/admin/faz14-kuyruk/baslat` ile.
- **Önleme kuralı (AGENTS.md kural 20):** "kapat" kararı her makinede (yerel + Oracle konteyner ayarları + `.env` anahtarları)
  ayrı ayrı doğrulanır; yeni LLM betiği kilitsiz yazılmaz; zamanlayıcı/izleyici/setInterval ile LLM çağrısı yasak.

## H79 — Otomatik çıkmış→cümle eşlemesi (vektör) derse ait olmayan soruları "çıkmış" diye bağladı (2026-10-27, y25-k2-01)
- **Belirti:** "Nörolojik Hastaya Yaklaşım" çıkmış listesinde hasta merkezli klinik yöntem, SVO prognozu, konversiyon bozukluğu,
  angular gyrus gibi bu derste geçmeyen 10 soru 0,92 puanla slayt 1'e bağlıydı.
- **Kök neden:** `cikmis_konum.py` her soruyu bge-m3 ile dersin en benzer cümlesine eşleyip eşik üstünü yazıyordu; "soru bu
  slayttaki bilgiyi mi soruyor" denetimi yoktu. Genel giriş cümlesi her nöroloji/psikiyatri sorusuna yüksek benzerlik verdi.
- **Çözüm:** Elle doğrulandı: 7 soru (4 doğrudan, 3 ilişkili), her birine `s` (slayt), birebir `kanit`, `seviye`,
  `dogrulandi:true`. Slayttaki yanıp sönen çıkmış chip'i yalnız `dogrulandi` kayıtları gösterir; `degerlendirme_dogrula.py`
  kanıtın slaytta birebir geçtiğini denetler.
- **Önleme kuralı:** "Çıkmışta soruldu" vurgusu ve chip yalnız doğrulanmış, slayt kanıtlı eşlemeye dayanır; vektör benzerliği
  yalnız aday listesidir. Metindeki "Bu bilgi çıkmış sınavda sorulmuştur" cümleleri de aynı kanıtla teyit edilir.

## H80 — Öğrenci Drive betiği uzantısız PDF'i not saymadı; kısaltma bulucu "HT+DM" yazımını kaçırdı (2026-10-27)
- **Belirti:** Öğrenci notu "Nöroloji 1 - Nörolojik Hastaya Yaklaşım" (uzantısız PDF) envanterde "diger" kaldı; slayttaki HT, DM,
  EP kısaltma sözlüğüne girmedi.
- **Kök neden:** Sınıflama yalnız uzantıya bakıyordu; kısaltma bölme deseni `+` işaretini ayırıcı saymıyordu; "EP" hunspell'de
  Türkçe sözcük sayılıp elendi.
- **Çözüm / kural:** Tür MIME'den de belirlenir; bölme deseni `[/\-–+]`; EP `kisaltma_bilinen.json`'a eklendi.
  `degerlendirme_dogrula.py` slayttaki her kısaltmanın sözlükte olmasını HATA ile ister.

## H81 — Amfi kaydı tek parça + VAD ile verilince Whisper "Altyazı M.K." sanrısıyla erken bitti; eşzamanlı tsc OOM'a yol açtı (2026-10-27)
- **Belirti:** 28 dk hoca kaydından 1 segment ("Altyazı M.K.") ya da istem cümlesi tekrarları çıktı; sonra iş OOM ile öldü.
- **Kök neden:** Kısık/yankılı amfi sesinde VAD konuşmayı eliyor, `initial_prompt` sanrı tekrarına yol açıyor; tüm dosya tek
  çağrıda verilince model ilk sanrıdan sonra susuyor. Aynı anda iki `tsc --noEmit` (5,6 + 3,5 GB) belleği bitirdi.
- **Çözüm / kural:** `hoca_dokum.py`: ham ses, VAD ve istem yok, 60 sn parça + 2 sn bindirme, sanrı süzgeci, her parçadan sonra
  `.yarim` yazılır ve kaldığı yerden sürer; birim `MemoryMax=4G`. Döküm sürerken `tsc --noEmit` çalıştırılmaz.

## H82 — Çıkmış soru penceresi şık seçilince kayboldu, ders sürmedi (2026-10-27, sınamada yakalandı)
- **Belirti:** Slayt 3'teki chip'e basıp şık seçince pencere kapandı, görünüm slayt 1'e döndü, ses sürmedi.
- **Kök neden:** Pencere durumu slayt katmanındaki chip bileşenindeydi. Ses durunca görünüm canlı konuma döndü, PDF
  görüntüleyici ekran dışı slaytı (chip + pencere) kaldırdı; durum ve "çalıyordu" bilgisi kayboldu.
- **Çözüm / kural:** Durum modül düzeyinde (`useSyncExternalStore`), pencere `CdCikmisPencereKok` ile `document.body`'ye
  portal; sanal listede çizilen bileşen kalıcı durum tutmaz. Sınama: çalarken aç → ses durur, kapat → aynı saniyeden sürer.

## H83 — "Çıkmış" diye gösterilen iki soru doğrulanamadı; biri sitede yüklenmedi (2026-10-27, kullanıcı bildirdi)
- **Belirti:** k2-01 slayt 3 chip'inde 2/2. soru "Soru yüklenemedi"; kullanıcı soruların orijinalini veritabanında bulamadı.
- **Kök neden:** (1) `4ba07c308e35`, `4c4eb178b88b`'nin yeniden yazılmış gizli kopyasıydı (sunulan listede yok → `/tek` 404).
  (2) `d3-k2-nor-014`'ün kaynak dosyası (`Noroloji_Kurul2_Cikmis_Sorular.json`) hiçbir ham klasörde yok; banka kaydı
  "doğrulanmış" etiketli olsa da özgün sınav belgesi bulunamadı. Eşlemede banka etiketine güvenildi, ham belge açılmadı.
  (3) Aşil sorusu bankada "2020-2021 / Kurul 1" etiketli; ham metinde 2021-2022 Kurul 5.
- **Çözüm:** Her soru ham belgede arandı (`meds_downloads/donem3/3. Sınıf/Kurul 2/2.Kurul-2021.pdf`, `21 22.txt`,
  `2. kurul .pdf`); kaynağı bulunan 5 soru kaldı, her kayda `kaynak` (belge + sayfa) yazıldı ve pencerede gösteriliyor.
- **Önleme kuralı:** Çıkmış eşlemesi yalnız **ham sınav belgesinde bulunan** soruyla yapılır; banka etiketi ("verified",
  "altin_standart") kanıt değildir. `kaynak` alanı olmayan kayıt `degerlendirme_dogrula.py`'de HATA. Gizli kopya
  (sunulmayan id) eşlenmez; hatırlama listesinden gelen sorunun şıkları "sonradan tamamlandı" diye belirtilir.

## H84 — Kaynağı olmayan 86 Kurul 2 "çıkmış"ı Check-Solve onayıyla görünür kalıyordu (2026-10-27)
- **Belirti:** Ham sınav belgesi taramasında 574 Kurul 2 sorusundan 86'sının özgün kaynağı bulunamadı (91/92 `d3-` önekli);
  76'sı 57 sesli dersin çıkmış listesindeydi. Rapor: `meds_database/derived/quarantine/kurul2_cikmis_kaynak_raporu.{md,csv}`.
- **Kök neden:** (1) `d3-*` kayıtları kaynak dosyası olmayan türetilmiş JSON'lardan (`*_Kurul2_Cikmis_Sorular.json`) geldi;
  "altin_standart/denetleyici_onayi" etiketleri özgünlüğü kanıtlamadı. (2) `applyQuarantine` Check-Solve ve Faz 14 onaylı
  soruları karantinadan muaf tutuyordu; 86'nın 86'sı Check-Solve onaylı olduğundan karantinaya yazmak hiçbirini gizlemezdi.
  (3) Sesli ders `cikmisKonum` listesi karantinayı hiç okumuyordu.
- **Çözüm:** 86 soru `karantina.json`'a `neden: kaynak_bulunamadi` ile yazıldı (silme yok; yedek `meds_temp/karantina_yedek_oracle_20261027.json`).
  `kaynakBulunamadi()` onay muafiyetinden ÖNCE uygulanır; `canliDers.ts` çıkmış listesini aynı kuralla süzer.
- **Önleme kuralı:** Banka/çıkmış eklemeleri ham sınav belgesindeki yerle (belge + sayfa) gelir; kaynak gösterilemeyen soru
  "çıkmış" olarak yayınlanmaz. Bir onay katmanı (Check-Solve, Faz 14) kaynağın yokluğunu gidermez. Geri alma: soruyu
  `karantina.json`'dan çıkarmak.

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

## H86 — Sınav planı Kurul 2'de boş sayfa (2026-10-27)
- **Belirti:** `/kamplar/sinav-plani` yalnız başlık ve açıklamayı gösteriyor, altı bomboş.
- **Kök neden:** aktif kurul takvimden 2; `planVerisiYukle` `kurulDagilimi(2)` bulamayınca (sinav_dagilimi.json'da Kurul 2 yok)
  `null` dönüyor, `SinavPlani` da `if (!plan) return null` ile hiçbir şey çizmiyordu.
- **Çözüm:** boş durum iletisi ("Kurul N için sınav dağılımı henüz girilmedi"). Kurul 2 dağılımı girilince plan kendiliğinden kurulur.
- **Önleme kuralı:** kurula bağlı veriyle çizilen her ekran, veri yokken `null` değil nedenini söyleyen boş durum gösterir;
  yeni kurul açılırken `sinav_dagilimi.json`'a o kurulun dağılımı eklenir.

## H86 — Ders işçisi denetimi örnek soru şık açıklamalarını standart kapıdan geçirmiyordu (2026-10-27, k2-03)
- **Belirti:** k2-03 taslağı `denetle.py` ile 0 HATA verdi, ama örnek soruların şık açıklamalarında `sik_aciklama.py` 98 hata
  buldu (20 kelimenin altında, "ne/ne işe yarar/neden" eksik); q18'de müfredat dışı iki çeldirici (oligoklonal bant, LP basıncı).
- **Kök neden:** `denetle.py` yalnız ≥20 karakter uzunluk denetliyordu; şık açıklama standardı (kural 14) yalnız asistan/çözücü
  doğrulayıcılarına bağlıydı, ders paketinin örnek sorularına bağlı değildi.
- **Çözüm:** `denetle.py` Kurul 2+ dersinde her şık açıklamasını `sik_aciklama.denetle` + `turkce_uslup.denetle` ile HATA verir.
  k2-03'ün 110 şık açıklaması yeniden yazıldı; q18 çeldiricileri dersin kendi kavramlarıyla değiştirildi.
- **Önleme kuralı:** örnek soru çeldiricisi de müfredattan (öğretilmiş komşu kavram) seçilir (AGENTS kural 4, 9).

## H87 — Çizim doğrulayıcısının komut satırı Kurul 2 cümle kimliklerini ve resim kutularını tanımıyor; sarmalayıcı yanıltıcı 0 HATA verdi (2026-10-27, k2-02)
- **Belirti:** çizim parti ajanları `cizim_dogrula.py` CLI'sini çalıştıramayıp kendi sarmalayıcılarıyla "0 HATA" bildirdi; gerçek
  yerleşimde (`cizim_uret.py`) 69 adaydan 9'u reddedildi (8 kontur çizgi üstünde değil, 1 resim sayfasında panel).
- **Kök neden:** CLI `denetle()`'ye resim kutularını boş veriyor, `konusma_v2` cümle kimliklerini (`k2-02-c####`) parti biçimine
  (`P#.C#`) çevirmiyor. Ajanlar eksik bağlamla kendi kapılarını kurdu.
- **Çözüm / kural:** çizim için geçerli kapılar YALNIZ `cizim_uret.py` (yerleşim + doğrulama, gerçek kutu ve görüntüyle) →
  `cizim_kapisi.py` → `panel_sinama.mjs`. Parti ajanının kendi sarmalayıcı sonucu kanıt sayılmaz; reddedilen çizim
  yayına girmez (emin olunmayan yer çizilmez). CLI düzeltmesi açık iş.

## H88 — Drive klasör adı değişince yayın PDF'in kaynak kimliğini bulamadı (2026-10-27, k2-03)
- **Belirti:** onaylanan k2-03 taslağı Oracle yayınında "PDF'in kaynak kimliği (manifest) bulunamadı" ile durdu (hiçbir şey yazılmadı).
- **Kök neden:** okul Drive'ında klasör "Patoloji" → "Tıbbi Patoloji" olarak yeniden adlandırılmış; dosya diskte eski yolda,
  manifest yeni yolda ("…/ Herniasyon .pdf", '/' içeren ad). Sunucu kipi yalnız birebir yol eşleyen `kaynak_kimligi`'ni kullanıyordu.
- **Çözüm / kural:** sunucu ve deneme kipi `kaynak_kimligi_esnek` kullanır; esnek eşleme klasör farkını yok sayıp `Kurul N/<branş>/`
  sonrası yol manifestte tekse onu kabul eder. Yayın denetim hatasında taslağın `yayin.json`'u silinip yeniden onaylanır.

## H89 — Slayttaki yapışık madde imi glifi (U+F06E) kısaltmayı ve kanıt eşlemesini bozdu (2026-10-27, k2-02/k2-03)
- **Belirti:** "KB" (kan basıncı) kısaltması sözlüğe girmedi; değerlendirme kapısı slayt metninde birebir geçen kanıtları "yok" saydı.
- **Kök neden:** PowerPoint madde imi özel kullanım alanı karakteri (``) sözcüğe boşluksuz yapışık geliyor; kısaltma bölme
  deseni ve kapı normalleştirmesi bu karakterleri ayırıcı saymıyordu.
- **Çözüm / kural:** `kisaltma_sozlugu.adaylar` ve `degerlendirme_dogrula.norm` U+F000–F8FF ve madde imi işaretlerini ayırıcı/boşluk
  sayar. Yeni metin işleyen her betik slayt metnini bu karakterlerden arındırarak karşılaştırır.

## H90 — Anlam denetimi önbellek anahtarı değişince denetim sessizce atlandı (2026-10-27, k2-02)
- **Belirti:** parti çizimi düzeltilince yerleşim "anlam denetimi bakılan 0" verdi; denetimin düzeltme/silme kararları uygulanmadan çizim yazıldı.
- **Kök neden:** `cizim_uret.anlam_denetimi` önbelleği girdinin sha1'ine bağlı; girdi değişince yeni denetim ister, çağrı yapılamazsa
  (claude kapalı) boş sonuçla devam eder.
- **Çözüm / kural:** elle üretimde her yerleşimden sonra `rapor.anlam_denetimi.bakilan` panel sayısına eşit olmalı; değilse kararlar
  yeni girdi anahtarına (sıra korunarak) eşlenir ya da denetim yeniden yapılır. `bakilan: 0` ile çizim yayına girmez.

## H87 — v15 katmanlarında tanımsız renk/yazı değişkenleri: saydam kartlar, varsayılan yazı tipi (2026-10-27)
- **Belirti:** Soru haritasında ısı hücreleri renksiz; v15 katmanlı sayfalarda bazı kartların zemini saydam, Newsreader okuma
  yazısı uygulanmıyor.
- **Kök neden:** v15 CSS'inde `--color-surface`, `--color-success(-soft)`, `--color-warning-soft`, `--v15-serif`, `--v15-font`
  kullanıldı; palet kaydında (`utils/palettes.ts`) bu adlar yok (gerçekleri `--color-white`, `--color-ok(-soft)`,
  `--color-warn-soft`, `--font-read`, `--font-sans`). Tanımsız değişken hesaplanınca özellik geçersiz → zemin saydam,
  `color-mix` boş, yazı tipi miras.
- **Çözüm:** `styles/v15/tokens.css`'e takma adlar (gerçek jetonlara bağlı).
- **Önleme kuralı:** yeni CSS'te renk/yazı değişkeni yazmadan önce `getComputedStyle(document.documentElement)` ile ya da
  palettes.ts/tokens.css'te var olduğu doğrulanır; yeni ad uydurulmaz.

## H91 — Çizim PDF'i önbellekte olmayınca bütün konturlar sessizce reddedildi (2026-10-27, k2-03/k2-04)
- **Belirti:** `cizim_uret.py` 14 konturun tamamını "sayfa görüntüsü yok" diye attı; panel_sinama `hazirla.py` IndexError ile çöktü.
- **Kök neden:** `capa_dok.py` ders PDF'ini indirme klasöründen (`meds_downloads/drive_root/<path>`) okur, `cizim_uret.py` ve
  `sinama/hazirla.py` ise yalnız `data/sesli_anlatim/.pdf_onbellek/<deck>_0_*.pdf` arıyordu. İşçisiz (elle) yayında önbellek
  dolmaz → belge `None` → raster yok → kontur doğrulanamaz ve sessizce elenir.
- **Çözüm:** ikisine de aynı yedek yol (indirme klasörü → `pdf_isaret.pdf_indir`); `cizim_uret` PDF hiç bulunamazsa durur.
- **Önleme kuralı:** bir hattaki bütün betikler kaynak dosyayı aynı yardımcıyla bulur; ret sayacında tek bir nedenin tüm komutları
  ataması (ör. "görüntü yok" = kontur sayısı) kapı hatası sayılır, yayına geçilmez.

## H92 — Bilinen kısaltma sözlüğü bağlamsız: MSS "Muskuloskeletal sistem" diye açıldı (2026-10-27, k2-03/k2-04)
- **Belirti:** Nöropatoloji derslerinde MSS kısaltma kartında "Muskuloskeletal sistem"; slayt "MSS-SSS: Merkezi-Santral Sinir Sistemi" diyor.
- **Kök neden:** `kisaltma_bilinen.json` her kısaltmaya dersten bağımsız tek açılım verir ve `otomatik` slaytın kendi tanımına bakmaz.
- **Çözüm:** derse özel `data/sesli_anlatim/kisaltma_elle/<key>.json` (`MSS: Merkezi sinir sistemi`), elle eşleme bilinenden önce gelir.
- **Önleme kuralı:** her derste kısaltma listesi (kısaltma = açılım) yazdırılıp slayt metniyle okunur; branşa göre anlamı değişen
  kısaltma (MSS, KB, BOS …) için derse özel eşleme yazılır, genel sözlüğe yeni anlam eklenmez.

## H93 — Çapa değişince PDF işareti yenilenmedi (2026-10-27, k2-04)
- **Belirti:** takip kapısı `T5 P72.C2: işaret s.74 ≠ çapa s.73`.
- **Kök neden:** `meds-cumle-zaman` servisi işareti yalnız ses/metin değişince yeniden üretir; çapa sonradan yüklenince eski
  (v2 sayfa ipucuyla üretilmiş) işaret kalır.
- **Çözüm/kural:** çapa Oracle'a yüklendikten sonra `pdf_isaret.py --key <key> --zorla` çalıştırılır, ardından `takip_kapisi.py --api` 0 HATA.

## H94 — Çıkmış listesinde birleştirilmiş gizli kopya: çip 404 verdi (2026-10-27, k2-03)
- **Belirti:** `/api/past-exams/tek/ea1ab6a5b61d` 404 (çip açılınca "Soru yüklenemedi").
- **Kök neden:** aynı kökün iki kopyası eşlendi; biri birleştirme katmanında gizli (`applyMergeOverlay`), sunulan listede yok.
- **Kural:** `cikmis_konum` yalnız sunulan soru kimliklerini içerir; canlı doğrulamada her kimlik `/tek` 200 vermeden ders tamam sayılmaz.

## H95 — Yayın düzeltmesinde olmayan alan; PDF eşleyici durdurulan işçi kapsayıcısında (2026-10-27, k2-03/k2-04)
- **Belirti:** `meds-ders-yayin` her 10 dakikada `AttributeError: 'Yayin' object has no attribute 'ders_id'`; yayından sonra
  "PDF eşleşmesi: container … is not running" ve deste PDF'i 404.
- **Kök neden:** H88 düzeltmesindeki lambda `y.ders_id`'yi `denetle()` öncesi okuyordu (alan orada atanır); PDF eşleyici
  `docker exec meds-ders-isci` ile çalışıyor, LLM yasağıyla durdurulan kapsayıcıda koşamıyor.
- **Çözüm:** `y.b.get("ders_id")`; PDF eşleme tek seferlik `docker run --rm -u 1001:1001 --entrypoint python3 medsoru-isci:latest`
  (aynı bağlar, LLM anahtarı yok) ile; deste PDF'i 200 doğrulandı.
- **Önleme kuralı:** yayın betiği değişikliği Oracle'a gitmeden önce yerel taslakla `kaynak_kimligi_esnek` ve `--deneme` akışı
  çalıştırılır; yayından sonra `/api/lecture-pdf/deck/<deck>/0` 200 kontrolü zorunlu.

## H96 — Önem/çözücü zinciri ham belgede olmayan soruyu "çıkmış" diye kullandı (2026-10-27, k2-03)
- **Belirti:** k2patoloji 2p01 önem maddesi ve çözücüde "2020-2021 Final" etiketli `q-2021final_230619_142600-3-r68`; kaynak
  PDF'inde (`meds_sorular/2021final_230619_142600.pdf`) bu soru yok.
- **Kök neden:** `ders_zinciri` `hazirla` adımı çıkmış adaylarını bankadan konu eşlemesiyle seçer; ders için elle doğrulanan
  liste (`cikmis_konum`, kaynak taraması) ile karşılaştırılmaz. Bankadaki türetilmiş (`-rNN`) kayıtlar da aday olur.
- **Çözüm:** soru önemden `elenen_cikmis`e, çözücü ve `cikmis/2p01.json`'dan çıkarıldı (numaralar `numara.json`'da sabit).
- **Önleme kuralı:** zincirden sonra önem/çözücü/asistandaki her çıkmış kimliği ham belge taramasında `bulundu` ve `/tek` 200
  olmalı; değilse yayına girmez. `-rNN` türetilmiş kayıt hiçbir zaman çıkmış sayılmaz.

### H89 — Canlı yarışma odası sorusuz kuruluyor, oyun hiç başlamıyordu (2026-10-27)
- **Belirti:** `/api/quiz/ws` odasına katılan herkes "Hazırım" dese de oyun başlamıyordu.
- **Kök neden:** `handleJoinRoom` olmayan odayı `createOrJoinRoom(..., [])` ile **boş soru listesiyle** kuruyordu; `handleSetReady` `questions.length > 0` şartıyla geri sayımı hiç başlatmıyordu. Ayrıca yeniden bağlanan oyuncu yeni kayıtla puanını kaybediyor, istemci `disconnect()` sonrası `onclose` içinde kendiliğinden yeniden bağlanıyordu.
- **Çözüm:** oda yalnız `kaynak` (branş/ders/n) ile kurulur, sorular `oyunSoruKaynagi.ts`'ten; kaynaksız katılımda oda yoksa `room_error`. Yeniden bağlanan aynı kimlik puanını korur; istemci `disconnect` oda kimliğini siler.
- **Kural:** realtime odası veri olmadan kurulamaz; sunucu her başarısız katılımı açık hata mesajıyla döner.

### H90 — v15'te Toplu PDF penceresinin üstüne üst/alt çubuk biniyordu (2026-10-27)
- **Belirti:** Sesli dersler (ve PDF oluştur) › Toplu PDF açılınca pencerenin başlığı ve "indir" düğmesi v15 üst çubuğunun ve alt sekme çubuğunun altında kalıyordu.
- **Kök neden:** pencere (`.tp-perde`, z-index 120) sayfa kabının içinde çiziliyordu; kap kendi katman bağlamını kurduğu için z-index'i kabın dışına taşmıyor, sabit konumlu v15 çubukları (z 30/40) üstte kalıyordu.
- **Çözüm:** `TopluPdfDugme` pencereyi `createPortal(..., document.body)` ile çizer.
- **Kural:** tam ekran örtü/pencere bileşenleri daima body'ye portal ile çizilir; sayfa içi z-index'e güvenilmez.

## H97 — Dağıtım, yeni sesli ders metnini git'teki eski sürümle geri aldı; ses eski metinle üretildi (2026-10-27, k2-03/k2-04)
- **Belirti:** ders-ekle "metinDegisti" döndü ama Oracle'da metin 08:18'deki eski sürümdü; k2-04'ün yeni EMA varyantı eski metnin süresiyle (1609 sn) çıktı; doğrulayıcı eski 65 paragrafı gördü.
- **Kök neden:** `dagit.sh` git'teki sesli_anlatim verisini Oracle'a eşitler; yeni metin git'e işlenmeden ders-ekle yapılınca (başka oturumun dağıtımı dahil) canlı metin eski commit'e döner. EMA işi metni çalışırken Oracle'dan okur.
- **Kural:** yeni metin + v2 + vurgu + hizalama önce commit/push, sonra ders-ekle; ses tamamlanınca eski metne ait varyantlar silinir (`DELETE /api/sesli-anlatim/ses/<key>/<vid>`); `kayit.json` süre/özet ve `takip_kapisi --api` ile doğrulanır.

## H98 — Çizim panelleri dar ekranda taşıyor/sözcük kırıyor (2026-10-27, k2-03/k2-04)
- **Belirti:** `panel_sinama` 366 px'te 10–16 hata (5+ maddeli neden listeleri, dar karşılaştırma sütunlarında "Kafatası", "Korunur" kırılması).
- **Kural:** çizim ajan talimatına panel başına en çok 4 madde ve ≤60 karakter eklendi; taşan panel silinir/kısaltılır, kapı gevşetilmez.

### H99 — v15'te yeni ve bazı eski sayfalara menüden ulaşılamıyordu (2026-10-27)
- **Belirti:** Topluluk, PDF oluştur, Check Up, sıralama, müzik gibi sayfalar telefonda/tablette/masaüstünde menüde görünmüyordu; tam ekran gibi araçlar dağınıktı.
- **Kök neden:** v15 kabuğunda üç ayrı elle yazılmış liste vardı (telefon menüsü: yalnız Başvuru + MENU_SAYFALARI; kenar çubuğu: yalnız açık bölümün alt sayfaları + sabit 5 kişisel bağlantı; tablet rayı: yalnız 5 bölüm). NAV_TREE'ye eklenen sayfa bu listelere girmiyordu.
- **Çözüm:** `navV15.menuGruplari` tek kaynak; üç görünüm de ondan çizer. Araçlar ayrı kompakt sıra.
- **Kural:** yeni sayfa yalnız NAV_TREE'ye (ve gerekirse KISISEL'e) eklenir; kabukta elle sayfa listesi yazılmaz.

## H99 — Dağıtım sunucu servis değişikliğini "yalnız ön yüz" sandı; yeni data dosyası Oracle'a gitmedi (2026-10-27, sınama)
- **Belirti:** `src/services/canliDers.ts` değişikliği ve `data/sinama.json` dağıtıldıktan sonra canlı API eski davranışı sürdürdü.
- **Kök neden:** `dagit.sh` bu değişiklikte uygulamayı yeniden başlatmadı ("yalnız ön yüz/statik"); `data/` altındaki yeni dosya eşitlenmedi.
- **Kural:** sunucu kodu değişen dağıtımdan sonra `curl` ile yeni davranış doğrulanır; gerekirse `docker restart meds-app` ve sağlık kontrolü. Yeni `data/*.json` dosyası Oracle'a elle (`scp` + `sudo cp`) kopyalanıp canlıda okunduğu doğrulanır.

## H100 — Asklepios kutlama efekti görünmüyordu (2026-10-27)
- **Belirti:** "Asklepios Asası" kutlama efekti çalışmıyor; asa/yılan hiç görünmüyordu.
- **Kök neden:** `KutlamaKatmani.tsx` canvas'ı kartın ARKASINDA ve asayı tam merkeze (`cx`) çiziyordu; opak 380 px kart (`.bs-k-kart`) ortayı tamamen örtüyordu. Işıltılar da merkezden doğup kartın altında kalıyordu.
- **Kural:** ortada çizilen efekt kartın altında kalmaz; kartı örtmeyen konuma (iki yan) çizilir ve canvas kart üstüne (`is-ust-katman`) alınır. Yeni kutlama efektini canlı kartla birlikte gör.

## Tasarımdaki animasyon/3B ögesini "yok" diye atlamak (2026-10-27, Hücrem)
- **Belirti:** Kullanıcının canvas'ta çizdiği evrim animasyonları sayfaya girmedi, düz SVG yapıldı.
- **Kök neden:** Plana "3B yok" yazıp geçmek; tasarım kapsamı onaysız daraltıldı.
- **Kural:** Tasarımda olan animasyon/3B atlanamaz; zor ya da bağımlılık gerektiriyorsa kullanıcıya sorulur, plana "yok" diye yazılmaz.

## v15 tam ekranda yan menü içeriğin üstüne biniyor (2026-10-27)
- **Belirti:** Tam ekran modunda 76 px ray açık kalıyor, "Günler, Dr" başlığı ve akış kartlarının solu menünün altında kesiliyor; çıkış hapı üst barın sağındaki simgelerin üstüne biniyor.
- **Kök neden:** `v12.css` tam ekranda `.sh-app` dolgusunu ve `--sh-side-w`'yi sıfırlıyor, `.sh-side/.sh-top`'u gizliyor; v15 kabuğu `.v15-side/.v15-top` kullandığı için gizlenmedi, dolgu kalktı ama ray `position: fixed` kaldı.
- **Kural:** Yeni kabuk (v13, v15…) eklenince `html.is-app-fullscreen` için o kabuğun yan menü/üst bar sınıfları da gizlenir ve `--sh-side-w` sıfırlanır (`styles/v15/shell.css` sonu).

### H100 — Koyu temada "beyaz" yazılar kayboluyordu; spinner/iskelet renkleri temaya uymuyordu (2026-10-27)
- **Belirti:** Koyu temada renkli düğmelerdeki, koyu başlık şeritlerindeki ve perde üstündeki "beyaz" yazılar okunmuyordu; yükleme iskeleti her temada sabit maviydi; bazı ekranlarda doğru şık/zor etiketi renksizdi.
- **Kök neden:** Tailwind `white` rengi `--color-white` = palet **yüzeyine** bağlı; koyu temada `text-white` koyu lacivert çıkıyordu. `.ms-shimmer` sabit `rgba(30,79,216,…)`; `--color-good`, `--color-danger`, `--color-text(-sub)`, `--color-bg/border/text-dim` hiçbir yerde tanımlı değildi.
- **Çözüm:** `index.css`: `.text-white` → `var(--color-on-solid)` (katmansız kural utilities katmanını ezer), `.bg-ink-surface .text-white` → `--color-canvas`, koyu perde için `.on-perde`; iskelet `color-mix(accent)`; tanımsız değişkenler gerçek tokenlara bağlandı. Tam döküm `docs/V15_TEMA_DENETIMI.md`.
- **Kural:** Yazı rengi için `text-white` değil `text-on-accent`/`text-on-solid`; yeni CSS değişkeni yalnız `palettes.ts` TOKEN_KEYS ya da v15 tokens.css içindekilerden; sabit renk yalnız bilinçli süs (çerçeve, kâğıt üstü çizim) için.

## Sesli ders: çizimsiz resimde zoom takılı kalması
- Belirti: çizim yokken resim yakınlaşmış kalır. Kök neden: React unmount temizliğinde `ref.current` null; `CizimLayer` sayfayı ref'ten bulup sıfırlıyordu. Önleme: temizlikte ref okuma, DOM öğesini önceden yakala.

## H101 · Kronometre sayfa değişince kayboluyor, iki sayaç aynı anda açılıyor (2026-10-27)
- **Belirti:** Yüzen kronometre sesli ders / Öğren ekranına geçince kayboluyordu; "Odak" ayrı bir ikinci baloncuk olarak kronometreyle aynı anda çalışabiliyordu; sesli ders oynatıcısıyla üst üste biniyordu.
- **Kök neden:** `KronometreV15` ve `KapsulV15` `TopBarV15` içinde bağlanmıştı; odak ekranlarında üst bar `null` döndüğünden bileşenler sökülüyordu. Odak oturumu ayrı bileşen + ayrı portal olduğu için iki sayaç bağımsızdı. Oynatıcı konumunu bilen bir mekanizma yoktu.
- **Çözüm:** Kronometre uygulama kökünde (`App.tsx`, `V15Icinde`) tek kez bağlanır; Odak panelin sekmesidir (`KapsulV15 gomulu`), biri başlayınca öteki duraklar (`medsoru:sayac`). Baloncuk `.cd-dock`'u izler: mini oynatıcının sağ ucuna kaynaşır, tam oynatıcının sağ üstüne oturur.
- **Kural:** Sayfalar arası kalıcı olması gereken yüzen öğe (sayaç, oynatıcı) asla sayfaya/üst bara bağlı bileşenin içine konmaz; uygulama kökünde tek örnek olarak bağlanır. Aynı işlevin ikinci yüzen örneği eklenmez.

## H102 · Sınav planı Kurul 2'de yanlış puan/plan veriyor (2026-10-27)
- **Belirti:** Kurul 2 aktifken Bitirdiklerim › Sınav planı çok düşük beklenen puan ve gerçek dışı plan gösteriyordu; sesli dersler hiç hesaba girmiyordu.
- **Kök neden:** (1) `sinavPlani.ts` sesli dersi `CD_SPOT_BRANS` ile eşliyordu; bu tablo yalnız Kurul 1 branşlarını bilir, K2 dersleri (`k2noroloji` …) `!b` diye atlanıyordu. (2) İçeriği henüz olmayan branşta (psikiyatri, aile, ftr…) ders listesi boş olduğundan `bransP` = 0 çıkıyor, tüm sorular yanlış sayılıp baraj cezası (−n/2) yazılıyordu.
- **Çözüm:** K2+ için branş `k<kurul><slug>` olarak türetilir ve ders kurulu eşleşmelidir; içeriksiz branşın olasılığı çalışılmamış taban (0,30) alınır.
- **Kural:** Kurul 1 sabit tablolarına dayanan eşleme Kurul 2+ için kurul önekli türetilmeli; içeriği olmayan branş 0 olasılıkla değil taban olasılıkla modellenmeli.

## H103 · Çıkmış adayı farklı dönem/ders sınavından geliyor; ham anahtar bankadaki cevapla çelişiyor; bankada olmayan çıkmışlar (2026-10-27, k2-05 Nörolojik Muayene)
- **Belirti:** Bankada "Nörolojik Muayene / Kraniyal Sinir Muayenesi" konulu 32 kayıt vardı; ham belgelerde yeri açıldığında: laterale bakış (abdusens) sorusu Dönem 2 Anatomi sınavından (`tüm sorular.pdf` s.544), Broca/Brodmann 44 sorusunun ham anahtarı "İdeomotor apraksi" (banka "Broca"), dil sapması sorusunun üç varyantında anahtarlar çelişkili. Buna karşılık dersin slayt bilgisini birebir ölçen sorular (kornea refleksi V–VII, Babinski patolojik, kas gücü 3/5 profili; `2.Kurul-2021.pdf` s.18, s.22) bankada hiç yoktu.
- **Kök neden:** Banka konu etiketi başka kaynaktan (Dönem 2 anatomi kitapçığı, FTR bölümü, türetilmiş `-rNN` kayıt) gelen soruyu bu derse atamış; etiket ham belgenin dönemini/dersini/anahtarını doğrulamıyor. Öte yandan banka, ham Kurul 2 sınavındaki tüm soruları taşımıyor.
- **Kural:** Çıkmış eşlemesi yalnız (a) ham belgenin DÖNEMİ ve DERSİ bu ders olan, (b) basılı anahtarı banka cevabıyla uyuşan, (c) slayt kanıtı birebir olan sorularla yapılır. Ham belgede olup bankada olmayan soru eşlenmez, `cikmis_taslak.json › bankada_yok_ham_belgede_var` listesine yazılıp bankaya ekleme kararı ana oturuma bırakılır. `-rNN` kayıt ham belgede doğrulansa bile karar ana oturumundur.

## H102 · Tasarımdaki kayıt adımları (üniversite, sınıf, kurul, hedef) koda geçirilmemişti (2026-10-27)
- **Belirti:** Kullanıcının v15 tasarımında çizdiği giriş sonrası bilgi toplama akışı sitede yoktu.
- **Kök neden:** Ekran denetimi I07–I10'u "DOĞRULANMADI" diye bıraktı; iş yalnız kullanıcının sıraladığı öncelik listesinden yürüdü, denetim tablosundaki DOĞRULANMADI/KISMİ satırları hiçbir zaman iş listesine dönüştürülmedi.
- **Çözüm:** ProfilKurulumV15 (I07–I11) + Profil › Okul ve hedef; denetim belgesine "Değerlendirilmemiş ekranların değerlendirmesi" tablosu (her satıra karar).
- **Kural:** Tasarım geçişinde "DOĞRULANMADI" durumu iş sonu kabul edilmez; her ekran KURULDU / SIRADA / VAR / BİLİNÇLİ / altyapı yok kararından birini alır ve tur sonunda tablo güncellenir.


## H104 · Hoca ses kaydı: tek model dökümü sınav vurgularını bozuyordu; kayıt dersin ortasından başlıyordu (2026-10-27, k2-08)
- **Belirti:** large-v3-turbo dökümünde hocanın dersin sonunda saydığı sınav yerleri gen adlarını bozuyordu (HOX "koks/COX", PAX6 "faksa altı", holoprozensefali tipleri "Dövar, övar, sevdövar"); kayıt 45. slayt civarından başlıyor, 1–44. slaytlar dökümde yoktu; "Altyazı M.K." sanrıları arada segment kapatıyordu.
- **Kök neden:** Kısık amfi sesi + tek model; sınav özeti hızlı konuşulduğu için en çok bozulan bölüm tam da en önemli bölüm.
- **Çözüm:** Son 7 dk Systran medium ile 30 sn parçalarla ikinci kez döküldü (CPU, systemd-run MemoryMax=4G); iki dökümün ortak anlaşılan kısmı alındı; her vurguya `kaynak_dokum`, `not` ve (öğrenci notuyla örtüşme) yazıldı; anlaşılmayan/slayta ters (Becker kardiyak tutulum) kayıtlar `hoca_vurgulari_dusuk_guven.md`'ye ayrıldı, pakete alınmadı.
- **Kural:** Sınav vurgusu tek dökümden çıkarılmaz; alıntı birebir döküm, anlaşılmayan sözcük "düzeltilerek" yazılmaz (düzeltme `not`ta); gen adı/sayı yalnız slayt ve/veya öğrenci notu ile örtüşünce vurgu olur; kaydın hangi slayttan başladığı rapora yazılır.

## H105 · Harita `adimlar` = deste `slideNumber` (checkpoint dahil); iskelet ajanı içerik adımlarını 1..N saydı (2026-10-27, k2-08)
- **Belirti:** Deste birleşince `denetle.py` 138 HATA (adım X: pdfSayfalari … ama harita … diyor).
- **Kök neden:** TALIMAT §1b "içerik adımı" diyor; denetleyici `adimlar`'ı destedeki slideNumber olarak okuyor, araya giren checkpoint slaytları numaraları kaydırıyor.
- **Çözüm:** Deste birleştirildikten sonra haritadaki k. içerik adımı → k. içerik slaytının slideNumber'ına çevrildi (sayfa kayıtları ve ana başlık aralıkları).
- **Kural:** Harita deste birleşmeden planlı sayıyla yazılır; birleştirmeden sonra slideNumber'a çevrilir ve `denetle.py` yeniden çalıştırılır (TALIMAT §1b'ye not eklendi).

## H106 · `baglam.kazanimlar` kapak metninden türetilmiş çöp şablon cümleler içeriyor (2026-10-27, k2-08)
- **Belirti:** "BEYİN VE İSKELET sİSTEMİ GELİŞİMİ gENETİĞİ dr. Öğr. Üyesi Serap ARSLAN … mekanizmasını ve klinik önemini analiz eder." gibi kazanımlar.
- **Kök neden:** `isle.kazanimlar` kayıtlı kazanımı olmayan derste konu adından şablon kurup PDF kapak satırlarını da içine alıyor; TALIMAT "varsa baglam.kazanimlar'ı aynen kullan" dediği için işçi bunları ders paketine kopyalar.
- **Çözüm:** k2-08 kazanımları dersten elle yazıldı (8 ölçülebilir kazanım).
- **Kural:** Genel şablon ("temel kavramlarını … analiz eder") ya da kapak metni içeren kazanım kullanılmaz. Açık iş: `isle.kazanimlar` kayıt yoksa boş dönmeli (kod düzeltmesi bu turda yapılmadı).

## H107 · Çıkmış eşlemesi: banka yıl etiketi ham belgeyle çelişiyor, yeniden yazılmış kökler, basılı anahtar yok (2026-10-27, k2-08)
- **Belirti:** `past-1790877040110-917236` etiketi 2020-2021, ham belge `22 23.pdf` = 2022-2023 Kurul 5; `past-q-18-85` etiketi 2018-2019 Kurul 1, ham belge `2016GKurul 5 soruları…pdf`; `d3-b-053` (Marfan) ham eşlemesi güvenilmez ve doğru şık (pektus karinatum) slayttaki pektus excavatum ile çelişiyor; `e07675f936c7`, `dea0348ff630` kökleri ham belgeden farklı yazılmış; `d3-k2-pat-008`/`d3-k2-tbg-008`/`d3-k5-pat-023` ham belgede yok. `22 23.pdf`, `İSKENDERUN…pdf`, `KURUL 2 ÇIKMIŞ 3.pdf` basılı anahtar taşımıyor.
- **Kök neden:** H83/H103 ile aynı: banka etiketi (yıl, kurul, "doğrulanmış") ham belgenin yılını/anahtarını kanıtlamıyor.
- **Kural:** `kaynak` ham belge adı + sayfa/soru no; çelişen yıl `yil_notu`na; basılı anahtar yoksa `anahtar_notu` ("tıbbi tutarlılık kontrol edildi"); kökü yeniden yazılmış sürüm ya da slayta ters doğru şık eşlenmez.

## H108 · Kısaltma kapısı slayttaki gen sembollerini ve slayt yazım hatalarını (LMXIB, WTI) Faz A'da HATA sayıyor (2026-10-27, k2-08)
- **Belirti:** `degerlendirme_dogrula.py` 19 HATA: OTX, MSX, SRY, TWIST, MITF, HOXA, HOXD, DCX, LFNG, FND, FGFR, MD, HMG, HD, TGF, LMXIB, WTI "sözlükte yok".
- **Kök neden:** Kapı `src/data/kisaltma_sozluk.json`'a bakıyor; kısaltma katmanı (aşama 10) daha sonra çalışıyor, arşivdeki y25 sözlüğü yalnız bazı genleri taşıyor; slayt yazım hatası (LMXIB, WTI) ayrı anahtar sayılıyor.
- **Çözüm:** 17 anahtar yalnız bu ders için eklendi (açılım standart, slayttaki yazım hatası belirtilerek).
- **Kural:** Genetik derslerde Faz A'da slayttaki gen sembolleri + kısaltmalar sözlüğe önce eklenir; yazım hatalı sembol (LMXIB/WTI) aynen ayrı anahtar olur ve açılımında doğru gen belirtilir.

## H109 · v2 cümlesinin `ses` alanında iç cümle sonu: sunucu cümle sayısı v2 ile tutmuyor (2026-10-27, k2-05 Nörolojik Muayene)
- **Belirti:** `konusma_v2.py --dogrula` 0 HATA verirken 4 cümlenin `ses` alanı ("Optik disk … çukurdur. Makula ise …") iki cümle içeriyordu; sunucu ve istemci bunu iki cümle sayar, v2/çapa/cümle zamanı/işaret/çıkmış konumu (`p`, `c`) tek cümle varsayar → çapa ve işaret bir cümle kayardı (`capa_baslangic` cümle sayısı tutmayan paragrafta v2 sayfasını kullanmaz).
- **Kök neden:** v2 doğrulayıcı `ses` içeriğini yalnız işaretleme/uzunluk bakımından denetliyordu; cümle sınırı kuralı (`pdf_hizala.cumle_sinirlari` = `canliDersStore.ts::cumleSinirlari`) v2 şemasında zorunlu değildi.
- **Çözüm:** `konusma_v2.dogrula` her `ses`'in tek cümle olmasını HATA sayar (`_cumle_sayisi`, sunucu kuralıyla aynı); yazar iki cümleyi iki v2 cümlesine böler. k2-01…k2-05 veride ihlal yok.
- **Kural:** her v2 `ses` tam bir cümledir; yazım betiğinde ayrıca kendi sınır kontrolü (cümle sayısı = 1, ≤25 kelime) çalıştırılır.

## H110 · Kısaltma kapısı `kisaltma_elle`deki OD/OR/ID/SED'i "kısaltma biçiminde değil" diye reddetti (2026-10-27, k2-08 Tıbbi Genetik)
- **Belirti:** `kisaltma_sozlugu.py denetle` 12 HATA: OD, OR, ID, SED "kısaltma biçiminde değil"; `otomatik` aynı kısaltmaları (slaytta onlarca kez geçen "OD kalıtım") hiç aday saymadı.
- **Kök neden:** `kisaltma_mi()` büyük harfli sözcüğü Türkçe sözlükte (hunspell) bulursa eler (od, or, id, sed); istisna yalnız genel `kisaltma_bilinen.json` içindi, dersin kendi `kisaltma_elle/<key>.json` anahtarları dikkate alınmıyordu (H92'nin önerdiği branşa özgü elle sözlük bu yüzden OD/OR için işe yaramıyordu).
- **Çözüm:** `ELLE_AKTIF` (işlenen dersin elle anahtarları) `kisaltma_mi`de kabul edilir; `k_adaylar/k_otomatik/k_dogrula` başında doldurulur. Çok anlamlı kısaltma (CVS: kardiyovasküler sistem s.49 / koryonik villus örneklemesi s.70) genel sözlüğe konmaz, sayfa bazlı yazar dosyasıyla verilir.
- **Kural:** branşa özgü, Türkçe sözcüğe benzeyen kısaltma (OD, OR, ID, SED) dersin `kisaltma_elle` dosyasına yazılır; genel `kisaltma_bilinen.json`a eklenmez.

## H111 · Alt ajan çapası: görüntüyü açmadan betikle eşleme, indeks kayması; kapı yalnız sınır denetliyor (2026-10-27, k2-08)
- **Belirti:** `capa_dogrula.py` 1 HATA (P82.C3 "madde M[6, 7] sayfada yok"); elle bakınca s.75 (2 cümle) ve s.83 (4 cümle) yanlış kutuya bağlıydı. Ajan raporları "kutu numaralarını txt'den eşledim, PNG'yi açmadım" diyordu.
- **Kök neden:** `sNN.txt` madde kutuları bir madde imi içinde birleşik (M1 = üç bullet) ya da bölünmüş (M3/M4) olabilir; ajan satır sırasından numara türetti. `capa_dogrula.py` sınır dışı indeksi yakalar ama yanlış ama geçerli kutuyu yakalamaz.
- **Çözüm:** ana oturum çıktıyı cümle×kutu kelime örtüşmesiyle taradı (şüpheli 81), kritik sayfaları tek tek okudu, 6 cümle düzeltildi; 422 cümle %98 anlamsal, 0 HATA.
- **Kural:** alt ajan çapası kapıdan geçmeden kabul edilmez ve ana oturum her sayfa için "cümle ↔ atanan kutu metni" dökümünü (`goster.py` benzeri) okur; birleşik maddeli (bullet'ları tek kutuda toplayan) sayfalarda kutu numarası satır sayısından türetilmez.

## H112 · İlk anlatım taslağı öğrenci denetçide KALDI: aynı sözcük iki anlamda, kilit kavram tanımsız, gen sembolü okunuşu çözülemedi (2026-10-27, k2-08)
- **Belirti:** bağımsız denetçi tur 1 KALIR: "tip bir kollajen" ile "osteogenezis imperfekta tip bir" aynı sesle okunup karışıyor; distrofinin işlevi ve "okuma çerçevesi" anlatılmadan ekzon rakamları verilmiş; sklerotom/dermatom/miyotom türevsiz; kraniyoraşizis tanımı anensefaliyle çakışıyor; WT1 "çifte ve te bir" çözülemedi; "Hoca da ... söyledi" onaylama cümleleri bilgi taşımayıp dolgu hissi veriyor.
- **Kök neden:** slayt satırı sırasıyla yazılırken ses dinleyicisinin görmediği ayrım (tip/tür) ve kilit kavramın önceden tanımı atlandı; Hoca atfı "her yerde ekleyelim" refleksiyle kuruldu.
- **Çözüm:** kollajen için "birinci/üçüncü tür", hastalık için "birinci tip" kullanıldı; okuma çerçevesi ve distrofin işlevi kısaca tanımlandı; somit türevleri, kraniyoraşizis tanımı düzeltildi; W harfi "duble ve" okunur; yalnız yeni bilgi (ayırt edici vurgu, klinik örnek, tedavi) taşıyan hoca atıfları kaldı. Tur 2 GEÇER (%90 yanıtlanabilirlik).
- **Kural:** sesle okunan metinde aynı sözcük iki ayrı kavramı gösteriyorsa yazım ayrıştırılır; sayısal/ekzon gibi kavram ancak tanımından sonra kullanılır; "hoca da ... söyledi" yalnız slaytın vermediği ek bilgi ya da sınav vurgusu içerdiğinde yazılır.

## H116 · Birleştiriciler yeni ders eklerken branştaki eski dersin dosyalarını da yeniden yazıyor (2026-10-27, k2-05 Nörolojik Muayene)
- **Belirti:** `birlestir.py k2noroloji --taslak` ve `asistan_birlestir.py k2noroloji` sonrası `git status`ta k2-02'nin (2n02) önem/çözücü/asistan
  dosyaları ve indeks satırları değişmişti (önem `cikmis`, çözücü/asistan `klip` alanı, asistan indeksinde `ses`/`sure`); k2-02'ye dokunulmamıştı.
- **Kök neden:** birleştiriciler branştaki TÜM dersleri çalışma klasöründen ve yerel ses dosyalarının o anki durumundan yeniden üretir.
  `korumali` yalnız içerik küçülmesini (%10) yakalar, başka dersin içerik farkını değil.
- **Kural:** elle zincirde her birleştirmeden sonra `git diff --stat`; yalnız yeni dersin dosyaları ve indeksteki yeni ders satırı sahnelenir;
  eski dersin dosyaları `git checkout` ile geri alınır, indekste eski ders satırı HEAD'den korunur (bilerek yapılan toplu yenileme hariç).

## Sesli derste geri oku "Ders çalış"a atıyordu (2026-10-27)
- **Belirti:** Sesli ders listesinden bir ders açılıp geri oka basılınca liste yerine "Ders çalış" sayfası açılıyordu.
- **Kök neden:** Ders içindeki geri oku her zaman ders ayrıntı sayfasına (`ders_detay`) gidiyordu; o sayfanın geri bağlantısı da kurul/branş merkezine çıkıyordu. Liste doğrudan derse açıldığı için ayrıntı sayfası hiç görülmeden araya girip yolu bozuyordu.
- **Çözüm / kural:** Uygulama içinden gelindiyse (`navigateTo` `__icGezinti` bayrağını koyar) ok `history.back()` yapar; doğrudan bağlantıyla açıldıysa ayrıntı sayfasına gider. Geri düğmeleri sabit hedefe değil, geldiği yere dönmelidir.

## Sesli derste canlı konum bazen çalışmıyor / bozuk çalışıyordu (2026-10-27)
- **Belirti:** Okunan cümle bazen izlenmiyor, bazen metin yanlış yere atlıyor, "Canlı konuma dön" kendiliğinden çıkıyordu.
- **Kök neden:** (1) Paragraf henüz çizilmemişken kaydırma tek denemeyle vazgeçiyordu. (2) Gizli (display:none) bölmede ölçüm sıfır çıkıp yanlış konuma kaydırıyordu. (3) Yerleşim kaynaklı küçük scroll olayları elle gezinme sayılıp takibi 8 sn durduruyordu.
- **Çözüm / kural:** Eksik öğede kısa aralıkla yeniden dene; sıfır boyutta kaydırma yapma; 3 px altı scroll farkını kullanıcı eylemi sayma. Yeni takip/kaydırma kodu bu üç durumu karşılamalı.

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

## H114 · Çizim ileri-sızıntı denetimi yalnız ses metnine bakıyordu: gen sembolleri (HOX, PAX6, FGFR3) panelde reddedildi (2026-10-27, k2-08)
- **Belirti:** Genetik dersinde şablonlu panelde "PAX6", "FGFR3" gibi sembol içeren hücreler "henüz anlatılmamış terim" diye elendi.
- **Kök neden:** `cizim_uret` `onceki` metni `cumleler.md` (ses metni, "paks altı", "fe ge fe re üç") idi; öğrencinin okuduğu `ekran` metni (PAX6) denetime girmiyordu.
- **Çözüm:** `cizim_uret.py` v2 `ekran` metnini de `onceki`ye katar (cümle sayısı tutuyorsa). Eşik değişmedi.
- **Kural:** ileri-sızıntı, öğrencinin gördüğü (ekran) ve duyduğu (ses) metnin birleşimine göre denetlenir.

## H115 · Elle çizimde koordinat tahmini kenar kapısından geçmiyor; `cizim_kapisi` K3 elle çapada boş geçiyor (2026-10-27, k2-08)
- **Belirti:** gözle yazılan kontur noktaları `kenar_orani` < %70 ile düştü (s.82 fotoğraf: %26); `cizim_kapisi` "şekil 0/0 çizimli" verdi.
- **Kök neden:** kontur noktaları Canny kenarına ±5 px içinde olmalı; tahmin yetmez. K3 çapadaki `sekil` alanını sayar, elle yazılan çapa `resim: 0` kullandığı için (k2-04 dahil) K3 boş (0/0) geçer.
- **Çözüm/kural:** noktalar görüntüden kenara oturtulur (eşik/snap, ham kenar haritası bakılır, bindirme görüntüsü okunur); K3 yerine elle ölçü: lazeri resim olan cümlelerin ≥%40'ı çizimli (k2-08: 8/14). Açık iş: K3 `resim` alanını da şekil beyanı saymalı (diğer derslerin sonucunu değiştireceği için bu turda dokunulmadı).

## H117 · Tam ekranda ayar düğmesi araç şeridini göstermiyordu (2026-10-27)
- **Belirti:** Sesli ders tam ekranda sağ üstteki ayar düğmesine basınca şerit açılmıyor, kenarda ince "s." şeridi kalıyordu.
- **Kök neden:** `.cd-pdf-bar` `container-type: inline-size` taşıyor; tam ekranda mutlak konumlanınca genişliği 0'a çöküyordu. Ayrıca `:is(> svg, …)` geçersiz seçiciydi, kural tümden atılıyordu.
- **Çözüm/kural:** tam ekran şeridinde `container-type: normal; width: max-content`; seçici düzeltildi. Mutlak konumlu öğeye `container-type: inline-size` verilirse genişlik açıkça verilir; `:is()` içinde başa combinator yazılmaz.

- **Geri düğmesi gelinen listeye dönmeli (2026-10-27):** Sayfa başlığındaki sabit `geri` hedefi her zaman push yapıp gezinme yığınını bozuyordu (liste→ders→Geri ≠ liste). Geri hedefi için `geriHedefe` kullanılır; sabit hedefe doğrudan `navigateTo` yok.

## H104 · Soru çöz sayfasında Araçlar görünmüyordu (2026-10-27)
- **Belirti:** Masaüstünde Araçlar listesi ekranın altında kesik kalıyor, üç satırdan fazlası görünmüyordu.
- **Kök neden:** `.d15.s15` ekran yüksekliğine sabitlenmişti (`height: calc(100dvh - …)`) ve araç listesi kalan alanda kendi içinde kayıyordu; Test oluştur kutusu büyüdükçe (yeni süzgeç satırları) listeye kalan alan birkaç piksele indi.
- **Çözüm:** Sabit yükseklik kaldırıldı (sayfa normal kayar); özet kartları tek satır, test kutusu sıkı, araçlar ızgara.
- **Kural:** İçerik sayfalarında ekrana sabit yükseklik + iç kaydırma kurma; büyüyebilen içerik (süzgeç, liste) başka bölümü görünmez kılar.

## H105 · Sıralı tabloda adım atlanıyordu (k2-05, 2026-10-27)
- **Belirti:** "Muayene başlıklarının sırası" tablosu 1, 2, 4, 5 diye gidiyordu; Motor sistem yoktu (Öğren tablosu + ders içerik sekmesi).
- **Kök neden:** Yazar parçası (`uret/parca_A.json`) interactive_table'ı yazarken 3. satırı atlamış; slayt metni beş başlığı doğru sayıyordu, tabloyla metin kıyaslanmadı. `ders_icerik_uret.py` tabloyu aynen kopyaladığı için hata iki yüzeye taşındı.
- **Çözüm:** 3. satır (Motor sistem) parça, taslak deste ve `interactive_learning_decks.json`'a eklendi; ders içerik paketi yeniden yazıldı.
- **Kural:** Sıra/Adım sütunlu tablolarda numaralar 1'den kesintisiz olmalı ve slayt metnindeki sayımla eşleşmeli (`docs/DERS_ICERIK_BICIMI.md`). Kapı: `scripts/ders_icerik/sira_kapisi.py`.

## H118 · Anlamsız karşılaştırma tabloları (Öge / Sınıf / Gerekçe) (2026-10-27)
- **Belirti:** "Anatomik basamak mı, muayene başlığı mı?" gibi karşılaştırma kartı/tablosu: Türkçesi bozuk, tıbbi olarak anlamsız ve öğretmiyor.
- **Kök neden:** `ders_icerik_uret.py` tüm karşılaştırma tipli Öğren ögelerini (swipe_matching, venn_grid, feature_bidding) koşulsuz tabloya çeviriyordu; yazar, öğretilmiş iki tıbbi kavram yerine "üst kategori etiketi" (basamak/başlık) ile sınıflama kurmuştu.
- **Çözüm:** swipe_matching tablo dışı bırakıldı; venn/feature_bidding yalnız ≥3 satır, her gerekçe ≥7 kelime ve benzersizse alınır.
- **Kural:** Karşılaştırma yalnız iki GERÇEK tıbbi kavramı (hastalık, yapı, ilaç, mekanizma) ayırt eder; "X mi Y başlığı mı" gibi meta sınıflama, tek cümlelik özdeş gerekçe, bozuk Türkçe yasak. Yazar parçalarında da yazılmaz; yazar/denetçi bunu kontrol eder.
- PDF/yazdırma: belge yalıtılmış iframe'de yazdırılır; uygulama DOM'unda yazdırma ve sayfa yüksekliğine eşit sabit yükseklik YASAK (boş sayfa/renk karışması).

## H119 · Örnek sorularda öznel/ders çağrıştıran kök ve rastgele slayt sorusu (2026-10-27)
- **Belirti:** Soru kökleri "dersin bölümüne göre…" gibi ifadeler içeriyor, çıkmış soru kalıplarına uymuyor, bazı sorular müfredat/kazanım dışı rastgele ayrıntı soruyordu.
- **Kök neden:** Talimat kaynak sadakatini ve şık standardını söylüyordu ama soru kökü üslubunu ve "her soru bir kazanıma hizmet etmeli" şartını söylemiyordu; yazar slayttan çıkan her bilgiyi soruya çevirdi.
- **Kural:** Kök bağımsız ve çıkmış-benzeri kalıpta; ders/slayt/bölüm göndermesi yok; her soru kazanım–konu bağlı, tıbbi ve sınav değerli. Kaynak: `TALIMAT.md` §4, `TALIMAT_ONEM.md`, `KURUL2_DERS_STANDARDI.md` §10.9.


## H106 · Çalışma takvimi (ısı haritası) hücreleri dev görünüyordu (2026-10-27)
- **Belirti:** İstatistiklerim › Çalışma takvimi geniş ekranda ~80 px'lik kutularla sayfayı kaplıyordu.
- **Kök neden:** `.gf15-isi` sütunları `minmax(0, 1fr)` (kart genişliğini paylaşır) + hücre `aspect-ratio: 1` → hücre yüksekliği kart genişliğiyle büyüyor.
- **Çözüm:** Sütun `minmax(0, 16px)` + `justify-content: start`; hücre en çok 16 px.
- **Kural:** Kare hücreli ızgaralarda (ısı haritası, takvim) sütun genişliğine üst sınır koy; `1fr` + `aspect-ratio` birlikte kullanılmaz.

## H107 · "Günlük çözülen soru" çubukları çok genişti; ajan sınama verisi tarayıcıda kalmıştı (2026-10-27)
- **Belirti:** İstatistiklerim › Ayrıntılar'da 14 günlük çubuklar ~82 px genişliğinde; ayrıca 19–27 Ekim arası günde tam 4–5 soru (40 çözüm, 2 deneme) görünüyordu.
- **Kök neden (çubuk):** `.st-col` `flex: 1`, içindeki `.ok/.bad` çubuk sütunun tüm genişliğini alıyor. **Kök neden (veri):** istatistik alt ajanı boş ekranı sınamak için `medsoru_study_progress_v1` / `medsoru_selftest_history_v1`'e sahte kayıt yazdı, "geri aldım" dedi ama kayıtlar tarayıcıda kaldı (sunucuya ulaşmadı: yerel + Oracle `user_data`'da yok).
- **Çözüm:** çubuk `max-width: 24px; align-self: center`. Sahte kayıtlar (hepsi `20:11:00.929Z` damgalı) silindi, eşitleme sarmalayıcısıyla temiz hal yazıldı.
- **Kural:** Alt ajan/ajan, eşitlenen profil anahtarlarına (userKvSync izin listesi) sınama verisi YAZMAZ; sınama gerekiyorsa ayrı anahtar ya da `?demo` bayrağı kullanılır. Ajan raporunda "geri aldım" deniyorsa tarayıcıda doğrulanır.

## H120 · Dallanmalı soruda doğru/yanlış bayrağı ters işaretliydi (2026-10-27, k2-01)
- **Belirti:** Öğren destesi slayt 1 klinik karar sorusunda, Merritt'e uyan şık `isCorrect:false` ama geri bildirimi "Doğru…", ters şık `isCorrect:true` ama "Yanlış…". Öğrenci doğruyu yanlış öğrenirdi.
- **Kök neden:** Yazar ajan şıkları ve bayrakları ayrı yazdı; `validate_learning_decks.py` yalnız "tek isCorrect var mı" bakıyordu, bayrak ↔ geri bildirim yönünü karşılaştırmıyordu. İlk bağımsız denetçi bunu yakalamadı; ikincisi betikle taradı.
- **Kalıcı çözüm:** doğrulayıcıya `klinik-karar-bayrak` HATA kapısı (geri bildirim "Doğru/Yanlış" ile başlıyor ve bayrakla çelişiyorsa). Önleme: bayrak ve geri bildirim tek yerden üretilir; denetçi kapı dışı tutarlılık taraması yapar; doğru şık hep ilk sırada olmaz.

## H121 · Sınama (test) Öğren dersi gerçek Kurul 2 dersleriyle aynı listede görünüyordu (2026-10-27, k2-07 Genel Anestezik İlaçlar)
- **Belirti:** Sınama olarak eklenen `k2p-k2-07-genel-anestezik-ilaclar` Öğren kitaplığında Tıbbi Farmakoloji grubunda gerçek derslerle karışık duruyordu (yalnız küçük "Sınama" rozeti vardı); gerçek ders işlenince karışma riski.
- **Kök neden:** `data/sinama.json` ayrımı yalnız Canlı ders servisinde (`canliDers.ts`) uygulanıyordu; Öğren kitaplığı (`LearnLibraryV12`) `deck.sinama` alanını yalnız rozet olarak gösterip dal (branş) ile grupluyordu.
- **Kalıcı çözüm:** kitaplıkta `sinama` işaretli desteler ayrı "Sınama — test verisi" bölümünde, en sonda gösterilir. Önleme: yeni listeleyen her ekran `sinama` alanını bölüm ayrımı için kullanır; gerçek PDF gelince `yayinla.py` aynı kimliği günceller ve `sinama` alanını bırakır (H97/H99 sırası).

## H108 · Tablo rozetleri harf harf dikey; Ders seçenekleri kartları uzayıp taşıyordu (2026-10-28)
- **Belirti:** Ders içerik tablolarında "Kayboldu/Azalır" gibi rozetli hücreler harf harf alt alta yazılıyordu. Sesli ders › Ders seçenekleri'nde "Metni dışa aktar" açılınca Cihazda/MP3 kartları dev boyuta uzayıp seçenekler sağa taşıyordu.
- **Kök neden (rozet):** başka bir oturum `dersIcerik.css`'e bir simge için aynı sınıf adıyla `.di15-ik{width:16px;height:16px}` ekledi; rozet `span.di15-ik` 16 px'e sıkıştı. **Kök neden (menü):** `.cd15-mliste > :not(.cd-btn) { display: contents }` sarmalayıcıyı çözünce dışa aktar alt listesi ve PDF düzeni ızgara hücresi oldu; satır `align-items: stretch` ile tüm kartları uzattı.
- **Çözüm:** eski kural `svg.di15-ik` ile kapsandı, rozete `white-space: nowrap; flex: none`. Menüde alt liste/düzen `grid-column: 1 / -1`, ızgara `align-items: start`.
- **Kural:** Yeni CSS sınıfı eklemeden önce aynı adın kullanılmadığını grep'le; kısa ortak adlara (`-ik`, `-ad`) element/üst seçici kapsamı ver. `display: contents` ile çözülen sarmalayıcının açılır alt parçaları tam satır olmalı.

## H109 · Ders içerik kayıtlarında "Slayt s.N" kaynağı eksik (2026-10-28)
- **Belirti:** k2-05 Terimler ekranında bazı terimlerde slayt/sayfa rozeti yoktu; k2-01..08 paketlerinde 650'den fazla terim `s` taşımıyordu; "Checkpoint" gibi slayt iskeleti ve slaytta olmayan "Afferent / efferent" terim olarak yazılmıştı.
- **Kök neden:** `ders_icerik_adim.py` terime `adim` yazıyor ama PDF sayfası `s`'yi yazmıyordu; doğrulayıcı yalnız `adim` eksikliğine bakıyordu, ekranın gösterdiği `s` denetlenmiyordu.
- **Çözüm:** `scripts/ders_icerik_kaynak.py` (adim→slayt→pdfSayfalari[0]) tüm paketlere uygulandı; kaynaksız iki terim silindi; `ders_icerik_dogrula.py` `s` eksikse ve iskelet terimde HATA verir.
- **Kural:** Ekranda gösterilen her kaynak alanı doğrulayıcıda zorunlu olur; sayfa uydurulmaz, bulunamayan kayıt silinir (el kitabı §19 11a).

## H122 · Paylaşılan çıkmış soruda süzgeç/kategori alanları öne çıkıyordu (2026-10-28)
- **Belirti:** Özel sohbette paylaşılan çıkmış soru `/cikmis/<id>` ile açılınca liste tek soruya iniyor ama araç çubuğu, yıl/konu giriş kartları ve v12 süzgeç sütunu da görünüyordu.
- **Kök neden:** `sharedId` yalnız soru listesini süzüyordu (`paginatedQuestions`); süzgeç alanları `sharedId`'ye bakmadan çiziliyordu.
- **Çözüm:** `PastExamsView.tsx`'te `sharedId` varken PageToolbar, v15 giriş kartları ve V12Frame gizlenir; "Tüm sorular" düğmesi paylaşım bandında kalır.
- **Kural:** Tek öğeye indirgenen (paylaşım/derin bağlantı) görünümde yeni süzgeç/giriş bileşeni eklenirse `sharedId` ile koşullanır.

## H109 · Aynı cihazda iki sekme açıkken profil eşitleme fırtınası (2026-10-28)
- **Belirti:** İkinci sekme açılınca iki sekme ~25–30 sn boyunca saniyede birden fazla `/api/user-data/backup` + `/api/notes` isteği attı (ölçüm: 25 sn'de 55 istek, her sekmede 17–19 yedek); sunucu 429 döndü, bekleyen gerçek değişikliğin gönderimi reddedilebiliyordu.
- **Kök neden:** (1) `userDataSyncService` yayın kaynağı `ORIGIN` sekme başına üretiliyordu; aynı cihazın öteki sekmesinin gönderimi `user_data_changed` ile "başka cihaz" sayılıp `pullFromServer` başlatıyordu. (2) `lastBackedUpFingerprint` sekme belleğindeydi ama `localStorage` sekmeler arasında ortak: öteki sekmenin yazdıkları bu sekmenin parmak izini değiştirdiği için `pullFromServer` çekmek yerine yeniden yedek gönderiyor, bu da öteki sekmeyi tetikliyordu (ping-pong).
- **Çözüm:** `ORIGIN` cihaz düzeyinde (`medsoru_sync_origin_v1`), son gönderilen parmak izi `localStorage`'da (`medsoru_sync_fp_v1`); ikisi de eşitleme izin listesinde değil. Sınama: iki yeni kodlu sekmede ikinci sekme açılınca ilk sekme 25 sn'de 1 not çekme + 1 yedek (önce 55 istek).
- **Kural:** Sekmeler arası ortak olan duruma (localStorage) bağlı karar verilerini sekme belleğinde tutma; yayın kaynağı kimliği cihaz düzeyinde olmalı. Sınamada eski kodlu açık sekmeleri kapat (yeni/eski sürüm karışımı ölçümü bozar).

## H123 · Tam içerik hattı ders başına 4–6 saat sürüyor, soru/metin/PDF hataları geri dönüş yaratıyordu (2026-10-28)
- **Belirti:** k2-05 ve k2-08 her biri ≈5 saat; sorularda çıkmış dışı üslup ve ipuçlu şık, metinde kaynak dışı bilgi, PDF'te tasarım hataları.
- **Kök neden:** (1) hoca dökümü CPU'da tek başına saatler sürüyordu; (2) birbirinden bağımsız adımlar sırayla yürüyordu;
  (3) her alt ajan 1.100 satırlık defteri bütünüyle okuyordu, ilgili kural kalabalıkta kayboluyordu; (4) denetçi reddedince
  bütün metin yeniden yazılıyordu; (5) soru üslubu, sayfa kaynağı ve PDF görünümü için betik kapısı yoktu, hatalar ancak
  denetçide ya da kullanıcıda ortaya çıkıyordu.
- **Kural:** `docs/TAM_HAT_HIZLI_AKIS.md` — E0 `hazirlik.py` (döküm GPU ≤2500 MHz, AGENTS §10 altıncı istisna); alt ajana yalnız
  `kural_secici.py --oku <aşama>`; yalnız hatalı parça yeniden yazılır (sayısal hedefte ±%10, kalite hatasında tolerans yok);
  ders başına tek denetçi.
- **Kapı — EKLENDİ:** `scripts/tam_hat/soru_uslup.py` (ders çağrıştıran kök, ipuçlu uzun doğru şık, kazanım bağı, kalıp payı),
  `kaynak_kapisi.py` (kayıt içeriği `s` sayfasında mı), `pdf_tarama.py` (boş sayfa, taşma, üst üste, harf harf kırılma).

## H124 · Soru çözücüde Kurul 2 seçili görünürken Kurul 1 dersleri listeleniyordu (2026-10-28)
- **Belirti:** `/sorular/soru-cozucu` açılınca kurul şeridinde "Kurul 2 · şimdi" vurgulu, ama liste 11 dersi (Kurul 1 + "Kurul 2 …" önekli) birlikte gösteriyordu; şeridin etrafında da boş, geniş bir kutu vardı.
- **Kök neden:** `KurulSecici` adreste kurul yokken vurguyu `varsayilanKurul()`'dan alıyor, `BransBaslangic` ise süzgeci `useKurulParam()`'dan (adres → null = süzgeçsiz) alıyordu; vurgu ve liste iki ayrı kaynaktan besleniyordu. Kutu: `olasi-sorular.css` içindeki kapsamsız `.ks` kuralı aynı sınıf adını taşıyan kurul seçicisine kenarlık/zemin/860 px veriyordu.
- **Çözüm:** çözücü ve En önemliler başlangıcı `useSeciliKurul()` kullanır (vurgulanan kurul = listelenen kurul), "Tümü" kaldırıldı, ad önekindeki "Kurul N" atılır, başlanmış dersler önde sıralanır. Olası sorular şeridi `.ks.kseridi` olarak kapsamlandı.
- **Kural:** seçili durum gösteren bir bileşen ile içeriği süzen kod AYNI kaynaktan (aynı kanca) okur; görsel vurgu için ayrı varsayılan hesaplanmaz. Ortak bileşenlerin sınıf önekleri (`.ks`, `.kh`) başka sayfa CSS'inde kapsamsız kullanılmaz.

## H125 · Ders içerik terimlerinde genel sözlükten bağlam dışı tanım, kopya terim, ipuçlu soru şıkkı (2026-10-28, k2-08)
- **Belirti:** Genetik dersinde "Taşıyıcı" patojen taşıyıcısı, "Frajilite" serviks muayene bulgusu, "Kollajen" skar dokusu/C vitamini,
  "Biyopsi" cerrahi biyopsi türleri, "Nematod" parazit listesi, "Polihidramniyoz" konjenital kızamık bağlamıyla tanımlanmıştı;
  mikrosefali/makrosefalide kaynaksız "±3 SD" eşiği vardı. 306 terimin 33'ü kopyaydı (Drosophila ×2, Zebra balığı/Zebra fish,
  Nörülasyon/Nörulasyon, "G380R" ile "G380R mutasyonu", Preaurikuler çukur ×3). 15 örnek soruda doğru şık ötekilerden belirgin uzundu.
- **Kök neden:** (1) Terim tanımları dersin sayfasından değil sitenin genel sözlüğünden alındı; sözlükteki ilk anlam (başka branş)
  dersin bağlamına bakılmadan kopyalandı. (2) İki ayrı terim geçişinin çıktısı birleştirilirken ad normalleştirmesi yapılmadı.
  (3) Soru yazarı doğru şıkkı eksiksiz tanımla yazıp çeldiricileri kısa bıraktı; uzunluk denetimi yoktu. (4) pdftotext slayt madde
  imini "o" harfi olarak kelimeye yapıştırıyor ("oOsteogenezis"); kelime eşlemeli her denetim bu yüzden yanlış sonuç veriyordu.
- **Kural:** Terim tanımı dersin sayfasındaki bağlamla yazılır (genel sözlük yalnız yardımcıdır, ilk anlamı kopyalanmaz); kaynakta
  olmayan sayı/eşik yazılmaz. Terim eklemeden önce ad + `e` eşanlamları normalleştirilip kopya aranır; slayttaki yazım farkı
  (Gl13, FLBN, speksifikasyon) `e`'ye girer. Şekilden okunan kayıt `gorsel: true`. Doğru şık çeldiricilerle benzer uzunlukta yazılır.
- **Kapı — EKLENDİ:** `scripts/tam_hat/kaynak_kapisi.py` (terim adı sayfada mı → HATA; tanım az örtüşüyorsa UYARI, denetçi bağlamı okur),
  `soru_uslup.py` (≥6 kelimelik doğru şık en uzun ve 1,8× → HATA), `hazirlik.py` madde imi temizliği.

## H126 · Sesli ders ekranında gen sembolleri okunuşla görünüyordu: "hoks, o te iks, me se iks, paks 6" (2026-10-28, k2-08)
- **Belirti:** Beyin ve İskelet Sistemi Gelişimi Genetiği sesli dersinde ana metin "hoks, o te iks ve me se iks genleri ile göz geni paks 6" yazıyordu; doğrusu HOX, OTX, MSX, PAX6.
- **Kök neden:** Ders metni iki katmanlıdır: `ses` (EMA'nın okuduğu) ve `ekran` (v2 `cumleler[].ekran`, doğru yazımla). Ana paragraf ise `ses` metninden `ekranYazim.ts` ile geri çevrilerek gösterilir; bu geri çeviri sözlüğü (`yazim_sozlugu.json`) yalnız kaynak md'den türetiliyordu ve harf harf okunmayan / kelime gibi okunan gen sembollerini (hoks, paks, soks) hiç tanımıyordu. Sayı geçişi "altı"yı "6" yaptığı için "paks 6" gibi karma yazım çıktı. Sözlük ayrıca uzun süre yeniden üretilmediği için yeni derslerin kısaltmaları hiç girmemişti.
- **Çözüm:** `yazim_sozlugu.py` artık her v2 dersinin `ses` ↔ `ekran` cümle çiftlerini hizalayıp okunuş → yazım eşlemesini kendisi çıkarır ("hoks" → HOX, "paks altı" → PAX6, "ce o le bir a bir" → COL1A1); Türkçe sözcük, Roma rakamı ve rakamsız okunuşa rakamlı yazım eşlemeleri elenir.
- **Kural:** Kullanıcıya gösterilen metin daima yazımla (HOX, OTX, PAX6), EMA'ya giden metin okunuşla olur. Tam içerik hattında her yeni v2 metni yazılınca `python3 scripts/sesli_anlatim/yazim_sozlugu.py` yeniden çalıştırılır ve ekran metni okunuş artığı için gözle denetlenir; `ekran` alanı her cümlede doldurulur (sembol içeren cümlede boş bırakılmaz).

## H110 · Çıkmış sorular yıl çipi 21, listede 20 soru (2026-10-28)
- **Belirti:** 2025–2026 çipi "21" gösteriyor, çipe basınca liste 20 soru veriyordu.
- **Kök neden:** `PastExamsView.girisGruplari` (yıl/ders çipleri) yalnız kurul süzgecini uyguluyordu; liste ise `facetPass` zincirinin tamamından geçiyor (varsayılan `quarantineFilter='standard'` karantina, Dönem 3 dışı ve gizli soruları eler; arama ve diğer süzgeçler de). Çip, listenin hiç göstermeyeceği soruyu sayıyordu.
- **Çözüm:** çip sayımı aynı `facetPass` + arama ile; yalnız çipin kendi boyutu (yıl çipinde `year`, ders çipinde `discipline`) hariç tutulur (yönlü süzgeç kuralı). Sınama: 12 yıl çipinin toplamı 502 = liste; 2023-2024 çipi 26 → liste 26.
- **Kural:** Süzgeç çipi/rozetindeki sayı, o çip seçilince listenin göstereceği sayıyla aynı yoldan (aynı süzgeç zinciri) hesaplanır; ayrı, eksik bir sayım yazılmaz.

## H127 — Yıldızlı paragraflar: Bugün'de yok, silinen geri geliyor, sesli derste tüm dersler listeleniyor (2026-10-28)
- **Belirti:** Öğrenci yıldızladığı paragrafları Bugün sayfasında göremedi ("internete kaydedilmiyor" sandı); sesli ders içindeki panel 108 kaydın tamamını (başka kurul/derslerin asistan kayıtları dahil) gösterdi.
- **Kök neden:** (1) Bugün sayfası (`FavorilerBugun`) yalnız `favoriStore`'u okuyordu; `medsoru_yildizli_paragraflar_v1` hiç bağlanmamıştı — kayıt eşitleniyordu ama erişim yolu yoktu. (2) `userKvSync` birleştirmesi iki cihazın listesini birleşim (union) ile kuruyordu; silme iz bırakmadığı için çıkarılan yıldız öbür cihazdan geri diriliyordu. (3) `CanliDersDers` paneli ders süzgeci olmadan açılıyordu.
- **Çözüm/kural:** Bugün'e kurul→ders→konu gruplu yıldızlı paragraflar bölümü eklendi; silme artık `silindi` mezar taşıyla yazılır ve birleştirmede aynı kimlikte en yeni `tarih` kazanır; sesli ders paneli `dersKey` ile varsayılan "Bu ders" kapsamında açılır ("Tüm dersler" seçilebilir). Yeni bir kişisel liste deposu eklenirken: (a) Bugün/Listeler erişimi, (b) silme mezar taşı + en yeni kazanır birleştirmesi, (c) bağlam içinden açılan panelde bağlam süzgeci zorunludur.

## H128 · EMA yabancı terimleri yanlış okuyor; anlatım konu geçişini söylemiyor; panel geç, zoom kısa anlatımda, çizim tek renk (2026-10-28)

- **Belirti:** EMA "Wernicke", "Staphylococcus", "locked-in", "Xanax" gibi yazımları Türkçe harf kuralıyla okuyordu. Başlıksız
  slaytta yeni konuya geçilince anlatım söylemediği için öğrenci önceki konuyla ilişkili sanıyordu. Liste/sıralama paneli
  anlatım başladıktan sonra açılıyordu; kısa değinmede zoom bitmeden slayt değişiyordu; resimden resme hızlı geçişte işaretler
  karışıyor, çizimler hep kırmızı ve hat tam izlenemiyordu.
- **Kök neden:** (1) EMA yolunda yalnız kısaltma katmanı vardı (okunus/kisaltma_ses); eponim/Latince/İngilizce terim
  sözlüğü yoktu. (2) Sesli ders talimatında kurgu (amaç, hiyerarşi, bölüm geçişinin ilişki türü, örnek) kuralı ve ön plan adımı
  yoktu. (3) Panel ilerlemesi `k0` = terimin söylendiği kelimeden başlıyordu. (4) Zoom yalnız bölge boyutuna bakıyordu,
  anlatım süresine bakmıyordu. (5) Kontur rengi CSS'te sabit kırmızıydı, boyama yalnız %13 sarı ışıltıydı, çizim hangi
  resim kutusuna ait olduğunu taşımıyordu.
- **Kalıcı çözüm:** `scripts/sesli_anlatim/terim_okunus.py` + `data/sesli_anlatim/okunus/terim_okunus.json` (eponim, Latince,
  İngilizce, ticari ad + Latince kural motoru) EMA'ya giden Kurul 2+/modül metnine uygulanır (`ema_isci.paragraf_seslendir`);
  `ses_temizle` (DC, RMS eşitleme, yumuşak tepe sınırı, 12 ms geçiş). `docs/ANLATIM_KURGU_STANDARDI.md` (plan → metin,
  ±%20 sayısal tolerans). `CizimLayer.tsx` panel cümle başından, zoom ≥55 karakter; `cizim_uret.py` ZOOM_EN_AZ=70, `renk_ata`,
  `renk/boya/resim` alanları; `cizim_dogrula.py` renk/resim kutusu denetimi.
- **Kural:** yeni ders seslendirmesinden önce `terim_okunus.py --denetle <anahtar>`; yanlış `KURAL` satırı sözlüğe eklenir.
  Anlatım yazarı önce `anlatim_plani.md` kurar; başlıksız konu geçişinde "burada konu değişiyor" cümlesi zorunlu.
  Çizimde birden çok resim varsa `resim: "R#"`, ayrı yapılar ayrı renk, hattı belirsiz bölge `boya: true`.

## H111c · Esc uygulama tam ekranından çıkarmıyordu (2026-10-28, ortak kabuk)
- **Belirti:** Kabuktaki "Tam ekran" düğmesine basılınca üst çubuk gizleniyor; native tam ekranın açılmadığı durumlarda (dokunmatik/klavyeli cihaz — iPad + klavye, dokunmatik dizüstü — ya da tarayıcı isteği reddettiğinde) Esc'e basmak hiçbir şey yapmıyordu, kullanıcı çıkışı yalnız küçük "Tam ekrandan çık" hapında arıyordu.
- **Kök neden:** Uygulama tam ekranı = `html.is-app-fullscreen`. Kaldırılması yalnız düğmeye ya da native `fullscreenchange` olayına bağlıydı; native katman yoksa Esc'i dinleyen hiçbir kod yoktu.
- **Çözüm:** `src/utils/fullscreen.ts` › `installEscExit` — tek genel `keydown` (bubble, `defaultPrevented`/yazı alanı/açık pencere-menü/sayfa içi tam ekran katmanı/`tam-katman`/`cd-tam-ekran` varken dokunmaz) sınıfı kaldırır ve `medsor:fullscreenchange` yayar. Tarayıcıda sınandı: aç → Esc → kapandı, düğme "Tam ekran"a döndü.
- **Kural:** Native tam ekranın yedeği olan her CSS kipi kendi Esc çıkışını taşır; Esc önce açık pencereye/katmana aittir.

## H111d · Yönetim betik kataloğu her açılışta ana pakete iniyordu (2026-10-28, başarım)
- **Belirti:** İlk açılışta inen ortak parça (`chunk-contentLive`) ~210 KB; içinde yalnız yönetim "Betikler" sekmesinin kullandığı yedek betik kataloğu (`bundledScripts.ts`, ~20 KB kaynak) vardı.
- **Kök neden:** `services/api.ts` (her ekranın kullandığı istemci) kataloğu statik içe aktarıyordu; rolldown onu api ile aynı ilk yükleme parçasına koydu.
- **Çözüm:** `getScriptsList` kataloğu `await import('../data/bundledScripts')` ile yalnız çağrıldığında yükler. Ölçüm: index.html'in indirdiği JS+CSS 2.747 KB → 2.719 KB (102 → 91 dosya). (`manualChunks` ile `deckStore`'u ayırma denendi: rolldown ortak bağımlılıkları o parçaya çekip 443 KB'lık yeni bir ilk yük parçası üretti → geri alındı; `manualChunks` ile paylaşılan modül ayırmak YASAK, statik içe aktarmayı kaldır.)
- **Kural:** Ortak istemci/servis dosyaları (api.ts, auth, realtimeEvents) yalnız tek ekranın kullandığı büyük veri/katalog modüllerini statik içe aktarmaz; dinamik `import()` kullanılır.

## H111e · Profil verisi dinleyicileri render sırasında setState yapıyordu (2026-10-28, Bugün/Arka plan)
- **Belirti:** Her sayfa açılışında konsolda React uyarısı: "Cannot update a component (`ArkaPlanGosterge` / `EsitlemeKarti`) while rendering a different component (`MusicPlayerProvider`)".
- **Kök neden:** `userKvSync.onWrite` profil anahtarı yazılınca `onProfileDataChange` dinleyicilerini **eşzamanlı** çağırıyordu. `MusicPlayerProvider`'ın `useState` başlatıcısı (`getVoterId` → `getDeviceToken`) ilk açılışta localStorage'a yazıyor; bu yazım render içinde olduğundan dinleyicideki `setKv`/`setBekleyen` başka bileşenin render'ında setState oldu.
- **Çözüm:** `userKvSync.ts` `bildir()` dinleyicileri `queueMicrotask` ile çağırır (tüm dinleyiciler zaten zamanlayıcı/setState yapıyor; eşzamanlılık gerekmiyordu). Sınama: sayfa_tarama /bugun, /arka-plan konsol hatası 1 → 0.
- **Kural:** localStorage/depo yazımına bağlı olay yayıcıları dinleyicileri eşzamanlı çağırmaz (mikro görev); render içinde (useState başlatıcısı, useMemo) yan etkili yazım yapılmaz.

## H111f · Deste kataloğu (~600 KB) her sayfada yalnız sayı için iniyordu (2026-10-28, başarım)
- **Belirti:** /kaynaklar, /topluluk, /saglik, /sozluk, /basarimlar gibi desteyle ilgisi olmayan sayfalarda `decks/catalog.json` (dev 3,4 MB, prod ~600 KB) indirilip ayrıştırılıyordu.
- **Kök neden:** (1) `offlineDatabaseService.loadStats` IndexedDB'de deste yoksa `decksCount` için `loadDeckCatalog()` çağırıyordu (açılışta her sayfada çalışır). (2) `deckStore.patchCatalog` açılıştaki içerik yeniden eşitlemesinde (değişen deste kimliği varsa) önce tüm kataloğu yüklüyordu.
- **Çözüm:** `loadStats` katalog yüklüyse uzunluğunu, değilse son kayıtlı istatistiği kullanır (`isDeckCatalogLoaded`); `patchCatalog` kataloğu yüklemez, değişen girdileri ekler — `loadDeckCatalog` sonradan bunları korur (mevcut "early" birleştirmesi). /kamplar, /istatistik ölçümde katalog artık inmiyor.
- **Kural:** Yalnız sayı/özet için büyük veri modülü tembel yüklenmez; özet meta veride tutulur. Canlı yama işlevleri ana veriyi zorla yüklemez, yüklemeyi bekleyen birleştirmeye bırakır.

## H111g · İzleme hızı kaydırıcısı: dokunma hedefleri 10–19 px, boş durumda imleç metinle çelişiyordu (2026-10-28, Sınav planı/Bitirdiklerim)
- **Belirti:** Telefonda hız durakları (1×…2,5×) 19 px, kaydırıcı rayı 10 px yüksekti; seçim yokken metin "kalan süre 1× gösteriliyor" derken imleç 1,5×'te duruyordu.
- **Kök neden:** `IzlemeHizi.tsx` boş değer için `?? 1.5` kullanıyordu; `takip.css` rayın ve durakların görünür boyutu dokunma alanı olarak bırakılmıştı.
- **Çözüm:** boş durumda imleç 1×; ray `padding: 9px 0` + `background-clip: content-box` (görünüş aynı, 28 px dokunma), duraklara `::before` ile 40 px dikey alan + `min-width: 40px`. Bugün akışındaki "Tümü" bağlantısı (14 px) negatif kenar boşluklu 40 px alana alındı (`today.css .t15-more`). Takvim, kronometre ve tam ekran ayarlarındaki `kre-tgl` anahtarlarına `aria-label` eklendi (adsız düğme).
- **Kural:** Görünür öğe küçük olabilir ama dokunma alanı ≥40 px (dolgu/`::before`); yer tutucu değer ile açıklama metni aynı varsayımı göstermeli; her `role="switch"` düğmesinin erişilebilir adı olur (label içi olmak yetmez).

## H111h · PC'de açıklama metinleri 120–160 karakter satır uzunluğunda (2026-10-28, okunabilirlik)
- **Belirti:** 1440 px'te Sınav planı açıklamaları (`sp-acikla`, `ss-acik`, "Bu sayılar nasıl hesaplanıyor?" listesi) ~130, Sağlık kaynakçası ~160, Topluluk kuralı ~116, Arka plan notu ~108 karakter satır.
- **Kök neden:** metin blokları kart genişliğini dolduruyor, ölçü (`max-width: ..ch`) yoktu; bir kısmı 12,5–13,5 px idi.
- **Çözüm:** `takip.css` `.sp-acikla/.ss-acik` 14 px + 72ch, `.sp-nasil ul` 75ch (özet 40 px), `cevrimdisi.css .cv-not` 14 px + 72ch, `saglik.css` kaynakça 90ch, `topluluk.css .tp15-kural` 75ch.
- **Kural:** Gövde/açıklama metni ≥14 px ve satır ≤ ~75ch; geniş kartın içindeki paragraf `max-width` ile sınırlanır.

## H111p · Sesli derste hatalı adreste sunucu hata kodu ham gösteriliyordu (2026-10-28, Ders çalış)
- **Belirti:** `/dersler/canliders/kurul1/<eski/hatalı anahtar>` açılınca ekranın ortasında yalnız küçük harfle "geçersiz ders" yazıyordu.
- **Kök neden:** `CanliDersDers.tsx` hata durumunda `fetch` hatasının `message` alanını (sunucunun iç kodu `{error:'geçersiz ders'}`) olduğu gibi basıyordu.
- **Çözüm:** "geçersiz ders / bulunamadı / 400 / 404" öğrenciye "Bu adreste bir sesli ders yok. Bağlantı eski ya da hatalı olabilir; listeden dersi seçebilirsin." olarak çevrilir; liste düğmesi kalır.
- **Kural:** Sunucu hata kodu (`error` alanı) öğrenci metni değildir; ekranda bilinen hatalar Türkçe açıklamaya çevrilir, bilinmeyen hata için genel cümle kullanılır.

## H111q · Sesli ders telefonda: başlık 75 px'e sıkışıyor, Kalem düğmesi eziliyor, bölme hızlı düğmeleri 23×21 px (2026-10-28, Ders çalış)
- **Belirti:** 375 px'te üst bar başlığı "Tümör …" (75 px), PDF şeridinde Kalem düğmesi 25 px'e ezilip boş daire görünüyor, dosya adı 18 px'e inip "1…" kalıyordu; Metin/PDF ayracının hızlı düğmeleri (35/50/65, yön, sıfırla) dokunmatikte 23×21 px.
- **Kök neden:** `.cd15-ad` tek satır `nowrap` + yanında 4–5 sabit simge düğmesi; `.cd15-pb` `flex: none` almadığı için `flex-shrink` ile küçülüyordu; `.cd-pdf-ad` dar kapta gizlenmiyordu; `.cd-ayrac-hizli button` için dokunmatik boyutu yoktu.
- **Çözüm:** `styles/v15/sesli.css` telefonda başlık iki satıra sarılır (16 px, line-clamp 2); `.cd15-pb { flex: none; min-width: 32px }`; `@container (max-width: 460px)` dosya adı gizli. `canli-ders.css` `(pointer: coarse)` hızlı düğmeler 36×36.
- **Kural:** Esnek şeritteki simge/düğmeler `flex: none` alır, yalnız metin öğesi küçülür; metin öğesi 40 px altına inecekse gizlenir ya da sarılır.

## H111r · Soru haritası hücrelerinde yazı kontrastı 2.6–4.0 (2026-10-28, Soru çöz)
- **Belirti:** `/sorular/soru-haritasi` ısı tablosunda orta yoğunluktaki hücrelerin sayıları zor okunuyordu (WCAG AA altında, açık ve koyu temada).
- **Kök neden:** renk yoğunluğu %12–90 arası sürekli ölçekti; %40–85 aralığında zemin orta mavi olduğundan ne koyu (`ink`) ne açık (`on-accent`, eşik %55) yazı 4.5'i geçebiliyordu.
- **Çözüm:** `SoruHaritasiV15.tsx` ölçeği iki banda ayırır: açık bant %10–40 (koyu yazı), koyu bant %90–100 (açık yazı); ara ton kullanılmaz. DOM kontrast ölçümü: 7 ihlal → 0.
- **Kural:** Yoğunluğa göre boyanan hücrede yazı rengi tek eşikle seçiliyorsa, eşiğin iki yanındaki zemin tonları her iki yazı rengiyle de 4.5'i geçmelidir; geçmiyorsa ara tonlar atlanır.

## H111s · Zihin haritası numaraları koyu temada okunmuyordu (2026-10-28, Ders çalış)
- **Belirti:** Koyu temada `/dersler/zihin-haritasi` liste numaraları (1, 2, 3…) koyu zemin üstünde 1.7–2.0 kontrastla neredeyse görünmüyordu.
- **Kök neden:** `.zh15-no` yazı rengi tema bağımsız sabit `oklch(0.45 …)`; zemin `--color-white` ile karıştığı için koyu temada koyulaşıyor, yazı koyu kalıyordu.
- **Çözüm:** `zihin.css` `:root.theme-dark .zh15-no { color: oklch(0.84 0.09 var(--t)) }`.
- **Kural:** Sabit `oklch()/hex` yazı rengi yalnız token zeminiyle birlikte koyu tema karşılığı yazılarak kullanılır.

## H111t · Ders çalış dokunma hedefleri: "Tüm dersler" 75×14, Öğren "▶ Dinle" 52×20 px (2026-10-28, Ders çalış)
- **Belirti:** Dersler merkezinde "Tüm dersler" bağlantısı ve Öğren adımındaki "▶ Dinle" düğmesi telefonda parmakla zor seçiliyordu.
- **Kök neden:** `.d15-more` yalnız metin yüksekliğindeydi (line-height 1); `.ls-tag` 20 px rozet stili düğmeye de uygulanıyordu.
- **Çözüm:** `dersler.css .d15-more` 40 px dolgu + negatif kenar (H111g ile aynı desen); `LessonPlayer.tsx` düğmeye `ls-dinle` sınıfı, `v12/lesson.css` dokunmatikte `::before` ile 40 px alan.
- **Kural:** H111g kuralı: görünür öğe küçük kalabilir, dokunma alanı ≥40 px.

## H111u · Çıkmış sorular kart görünümü sınırsız büyüyor, Odak ızgarası 4.372 düğme çiziyordu (2026-10-28, Soru çöz, başarım)
- **Belirti:** `/sorular/cikmis` Kart görünümünde aşağı kaydırdıkça DOM 2.700 → 34.000 düğüme (300 kart) çıkıyor, uzun oturumda sayfa ağırlaşıyordu; Odak modunda sağdaki numara ızgarası süzgeç sonucunun tamamını (4.372 düğme) çiziyor, her Önceki/Sonraki'de hepsi yeniden render oluyordu.
- **Kök neden:** `PastExamsView` `filteredQuestions.slice(0, richLimit)` ile her "daha fazla"da baştan sona tüm kartları tutuyordu; `CikmisModGorunum.Odak` `sorular.map` ile tüm numaraları çiziyordu.
- **Çözüm:** Kart görünümü kayan pencere: yalnız son 60 kart (`RICH_WINDOW`) çizilir, üstte düşenler tarayıcının kaydırma çapasıyla görünen kartı oynatmaz, üstte "Önceki soruları göster (n)" düğmesi; sayaçlar `richLimit` ile gösterilir. Odak ızgarası geçerli sorunun 100'lük bloğunu çizer, ‹ › ile blok değişir. Ölçüm: 8 kaydırmada DOM 34.226 → ~7.100 (sabit); Odak açılışı ~650 düğüm.
- **Kural:** Kaydırdıkça yüklenen listeler sınırsız büyümez (pencere ya da sanal liste); yüzlerce öğelik gezinme ızgarası bloklara bölünür.

## H111v · Ana CSS 936 KB, tam katman sayaçsız, tam ekranda fazla yükseklik, kısa başlık, küçük yazı, çevrimdışı boş istekler (2026-10-28, kabuk/başarım)
- **Belirti:** (1) her açılışta 936 KB (151 KB gzip) ana CSS iniyordu; (2) iki tam katman (ör. Başarımlar rozet ayrıntısı + kronometre) üst üste açılıp biri kapanınca alttaki açıkken alt sekme çubuğu geri geliyordu; (3) uygulama tam ekranında `.sh-main` 20–28 px uzun, boş sayfada bile kaydırma; (4) telefonda ders ayrıntısı/sesli ders başlığı "Tümör Biyoloji…" diye kesiliyor, `v15-crumb` dokunma alanı 61×16 px; (5) v15'te 13 px açıklama ve 10–12 px metinler; (6) çevrimdışıyken `/api/presence`, `/api/user-data/backup`, `/api/surum`, `/api/music/playlist` boşuna atılıyordu.
- **Kök neden:** (1) Öğren ders ekranı `ls-*` stilleri (~800 satır) `index.css` içindeydi, `main.tsx` onu ilk yükte veriyordu; (2) beş bileşen `tam-katman` kök sınıfını doğrudan `classList.add/remove` ediyordu — ilk kapanan sınıfı siler; (3) v12 tam ekranda `--sh-top-h`/`--sh-top-vis`'i 0 yapıp `.sh-main`'e 48 px üst dolgu veriyor, v15 "ekrana sığan" sayfa yükseklikleri (`100dvh - --sh-top-h - --sh-tabs-h - 48px`) bu dolguyu bilmiyordu; (4) telefonda geri + 4–5 simge düğmesi başlığa ~120/75 px bırakıyor, başlık tek satır `nowrap`; (5) eski sayfalar 11–12 px ile yazılmış, alt sınır yoktu; (6) bu uçlar `getNetState()`/`navigator.onLine` denetlemiyordu (yalnız `userDataSyncService` denetliyordu; fetch koruyucusu bilmediği için hepsi ağa gidip SW 503/zaman aşımı üretiyordu).
- **Çözüm:** (1) `src/styles/ogren-ders.css` (index.css'in iki `ls-*` bölümü) yalnız ls-* çizen 13 bileşenden içe aktarılır; ana CSS 936,8 → 865,7 KB (151,2 → 139,9 KB gzip); hesaplanmış stil dökümü önce/sonra (375/1440, deste + 3 ders adımı) 0 fark. `html.ui-v3` ls katmanı, health/v12 ezmeleri yüksek özgüllükte olduğundan ana CSS'te kaldı. (2) `src/utils/tamKatman.ts` (`useTamKatman`, referans sayaçlı); beş bileşen ona geçti. (3) v15 tam ekranda (`:not(.cd-ders-acik)`) `--sh-top-h` ve `--sh-top-vis` = 44 px + güvenli alan; `.sh-main` artık tam görünüm yüksekliği. (4) Telefonda `.v15-top-h` iki satıra sarar (17 px, line-clamp 2); sesli derste Tam ekran düğmesi telefonda gizli (Görünüm çekmecesinde var); `v15-crumb::before` ile ≥40 px dokunma alanı. (5) `--v15-t-caption` 13 → 13,5 px; v15 stillerinde 95 font değeri (10–12 px, <.78rem) 12,5 px'e çekildi. (6) `net.ts` `cevrimdisiMi()` + fetch koruyucusunda arka plan uçları (`presence`, `user-data/backup`, `music/playlist`) çevrimdışıyken ağa çıkmadan reddedilir; `presence.ts` ve `UpdatePrompt` `/api/surum` denetimi çevrimdışıyken atlanır (bağlantı yoklaması `baglanti.ts`/probe `/api/surum`'u kullanmaya devam eder).
- **Kural:** Sayfaya özgü büyük stil bloğu `index.css`/`main.tsx`'e eklenmez, kullanan bileşenden içe aktarılır (sıra/özgüllük hesaplanmış stil dökümüyle doğrulanır). Kök sınıfı birden çok bileşen açıyorsa sayaçlı yardımcıdan geçer. Tam ekranda gizlenen çubuğun yerine dolgu konuyorsa ilgili yükseklik değişkeni de o dolguyu yansıtır. v15'te metin ≥12,5 px; istisnalar yalnız rozet/sayaç/kbd/kronometre mini saati/yazdırma belgesi (`dersPdf.css`)/ray etiketi. Arka plan eşitleme ucu ekleyen `net.ts` `BG_RE`'ye ekler.

## H127 · Slayttaki şekil/deney anlatılmadı, "ders yorumuna girmez" diye geçildi (2026-10-28, k2-05 Nörolojik Muayene, sayfa 32–33)
- **Belirti:** VIII. sinir slaytında Rinne/Weber diyapazon çizimleri (mastoid → kulak önü; verteks + normal / iletim tipi / sensörinöral üç panel) vardı. Anlatım "Bu çizimde testlerin nasıl uygulandığı gösterilir" deyip geçti; testin neden yapıldığı, hangi panelin hangi sonucu gösterdiği söylenmedi. Önceki paragraf "ders bunların nasıl yorumlandığına girmez, yalnız adlarını verir" dedi.
- **Kök neden:** yazar "kaynak dışı bilgi yasak" kuralını yalnız slayt YAZISINA uyguladı; şekil, çizim, fotoğraf ve tablodaki bilgiyi kaynak saymadı. Yazıda yorum olmayınca çizimdeki normal/patolojik ayrımı da "kaynakta yok" diye atladı ve boşluğu meta cümleyle kapattı. Kapılar (metin_denetle, turkce_uslup, denetçi) bu kaçamak cümleyi yakalamıyordu; denetçi slayta bakmadan okuduğu için şeklin anlatılmadığını göremedi.
- **Kalıcı çözüm ve kural (Şekil ve deney anlatım kuralı, `KURUL2_DERS_STANDARDI.md` §8.12):**
  1. **Şekil kaynaktır.** Slayttaki çizim, fotoğraf, şema, grafik, tablo, mikroskopi ve görüntüleme; içindeki oklar, etiketler, işaretler (X, kesik/kalın çizgi, renk), panel karşılaştırmaları ders içeriğidir ve anlatılır. "Slaytta yazmıyor" şekli atlama gerekçesi değildir.
  2. **Deney/test/muayene görseli** her zaman beş soruyla anlatılır: (a) ne sınanır ve neden yapılır, (b) nasıl uygulanır (görselde ne görülüyorsa adım adım), (c) normal sonuç, (d) her patolojik panel/sonuç ne demektir ve hangi lezyonu gösterir, (e) sonuçlar birbirinden nasıl ayrılır (sınavda karıştırılan çift).
  3. **Çok panelli şekil:** her panel ayrı ayrı adlandırılır ve karşılaştırılır ("soldaki normal…, ortadaki…, sağdaki…"); işaretlerin anlamı (X = hasarlı yapı, kalın ok = sesin daha güçlü duyulduğu taraf) açıklanır.
  4. **Yalnız adı geçen kavram/test:** ilk geçtiği yerde 1–2 cümleyle ne olduğu ve ne ölçtüğü söylenir (Terim kuralı §8.5). Ayrıntı slaytta/şekilde ya da hoca dökümünde varsa o kadar açılır; yoksa uydurma yorum eklenmez ama ADI DA BOŞ BIRAKILMAZ.
  5. **Kaçamak meta cümle YASAK:** "ders bunun yorumuna girmez", "yalnız adını verir", "ölçütünü vermez", "şekilde ayrıntı yok", "nasıl uygulandığı gösterilir" gibi öğrenciye bir şey öğretmeyen cümleler yazılmaz. Gerçekten kaynakta bilgi yoksa cümle hiç yazılmaz; konu olduğu kadar anlatılır.
  6. **Şekil paragrafı betimlemeyle bitmez:** yalnız "…gösterilir / görülür / yer alır" cümlelerinden oluşan şekil paragrafı eksik sayılır; şeklin öğrettiği bilgi (mekanizma, sonuç, ayırıcı nokta) eklenir.
  7. **Çizim katmanı anlatımı izler:** her panel/sonuç anlatılırken lazer ve kontur o panele gider (kural 17/18; bir cümle = bir panel).
  8. **Denetçi şekle bakar:** bağımsız denetçi metni okuduktan sonra şekilli/tablolu her sayfanın görüntüsüne bakıp "şekildeki her panel/işaret anlatıldı mı" listesini işaretler; eksik varsa GEÇMEZ.
- **Otomatik kapı:** `metin_denetle.py` kaçamak meta cümleyi HATA sayar (`KACAMAK` kalıpları); yalnız betimleme cümlelerinden oluşan kısa şekil paragrafını UYARI olarak gösterir.
- **Uygulama:** k2-05 v1 korunur; `k2-05-norolojik-muayene-v2` klipli ses + taşınan katmanlarla yeniden kuruldu, 31–32. paragraflar bu kurala göre yeniden yazıldı.

## H129 — "Salt okunur" SQL konsolu süper kullanıcıyla çalışıyordu (2026-10-28, Yönetim v16)
- **Belirti:** Yönetim › Veritabanı gezgini SQL konsolu "salt okunur" diye sunuluyordu; READ ONLY işlem içinde `COPY … TO PROGRAM`, `pg_read_file`, `pg_authid` (parola özetleri) okunabilir durumdaydı.
- **Kök neden:** `DATABASE_URL` kullanıcısı `meds` süper kullanıcı; `begin read only` yalnız tablo yazımını engeller, COPY TO / dosya ve süreç işlevleri READ ONLY işlemde serbesttir.
- **Kalıcı çözüm:** `pgAdminRoutes.ts` `/api/admin/pg/sql`: ilk sözcük izin listesi (SELECT/WITH/EXPLAIN/VALUES/TABLE/SHOW), tehlikeli işlev/katalog yasak listesi, işlem içinde `set local role meds_salt_okur` (NOLOGIN, yalnız `pg_read_all_data`). Rol kurulamazsa konsol kapalı (503). `DELETE /api/admin/pg/row` ve `POST /api/admin/db/import` sunucuda onay sözcüğü ister.
- **Önleme:** "salt okunur" iddia eden her uç bağlantı rolünün yetkisiyle sınanır (COPY TO PROGRAM, pg_read_file, pg_authid, CTE içinde DELETE); tehlikeli uçlar istemci onayına ek olarak sunucuda onay sözcüğü ister.

## H130 — Canlı içerik katmanı tam kopyaydı, kaynaktaki yeni kayıtları gölgeliyordu (2026-10-28)
- **Belirti:** Kaynakta (`src/data/interactive_learning_decks.json`) duran yeni k2p desteleri (7 deste) yerel sunucunun kataloğunda/ders ayrıntısında görünmüyordu; sözlükte kaynağa sonradan eklenen 383 terim de sunucudan gelmiyordu.
- **Kök neden:** `contentOverlay.ts` panel yazımında dosyanın TAMAMINI `data/content/<rel>`'e kopyalıyor, `resolveContent` katman dosyası varsa kaynağa hiç bakmıyordu. 20.10'daki tek alanlık panel düzenlemeleri (yalnız `updatedAt`) 81 MB'lık deste kopyası bıraktı; sonraki tüm kaynak güncellemeleri (yeni desteler, sözlük terimleri, 44 güncellenen terim) gölgede kaldı. Dağıtım eşitlemesi de tam kopya varsayıyordu.
- **Kalıcı çözüm:** Katman kayıt düzeyinde farktır: `data/content/<rel>.fark.json` (`kayitlar`, `silinen`, kaynaktaki kaydın sha'sı `taban`). Okuma = kaynak + fark (`_birlesik/<rel>` önbelleği). Yazıcılar tam dosyayı yine `writableContent` yoluna yazar; kilit bırakılınca birleşik tabana göre farka çevrilir. Eski kopyalar `scripts/icerik_katman.py goc` ile `_ids.json` izine göre farka çevrildi (yedek `data/_yedek/content_goc_*`). `content-overlay-sync.sh` farkı kayıt kayıt uygular, `taban` tutmazsa durur, tam kopya görürse durur.
- **Önleme:** `python3 scripts/icerik_katman.py denetle` 0 HATA (tam kopya = HATA, birleşimde kaynak kaydı eksik = HATA). Katmana bütün dosya kopyalayan yeni yazıcı yazılmaz; başlangıç kopyası gerekiyorsa `resolveContent(file)` (birleşik) kopyalanır, ham kaynak değil.

## H131 — Yönetim öğrenci uygulamasının ortak girişiyle açılıyordu; ayrı giriş + SW önbellek zehirlenmesi riski (2026-10-28, Yönetim v16)
- **Belirti:** /manage ilk yükü 544 KB gzip JS + 152 KB gzip CSS (öğrenci App.tsx girişi, Tailwind index.css, splash, tüm kabuk yardımcıları); yönetim yavaş açılıyordu.
- **Kök neden:** v16 kabuğu `App.tsx` içinde `React.lazy` ile açılıyordu; yönetim için ayrı Vite girişi yoktu, bu yüzden öğrenci girişinin statik içe aktardığı her şey önce iniyordu.
- **Kalıcı çözüm:** `manage.html` + `src/manage-main.tsx` (yalnız adminFetchAuth, Firebase kimlik, palettes.ts tokenları, `styles/yonetim-temel.css`, kit, kabuk). `vite.config.ts` çoklu giriş; `server.ts` SPA geri dönüşü `/manage*` için `dist/manage.html`; geliştirmede `scripts/vite/yonetimGirisi.ts`. Yönetici değilse (moderatör) ya da `?kabuk=v14` ise `manage-main` tam uygulamayı (`import('./main')`) yükler. Uygulama içinden /manage'e geçiş (`App.tsx yonetimGirisineGec`) tam sayfa gezinmesi yapar (10 sn döngü koruması). Ölçüm: /manage 544+152 KB → 179+5 KB gzip; tarayıcıda 191 KB aktarım, FCP 164 ms.
- **SW kuralı:** `public/sw.js` gezinme yanıtını `/` ve `/index.html` olarak da önbelleğe yazar; /manage artık farklı HTML döndürdüğünden yönetim gezinmesi SW'de atlanır (ağdan gelir) ve `CACHE_VERSION` v18'e çıktı (eski SW'nin bir kez zehirleyebileceği önbellek etkinleşmede silinir). **Önleme:** Sunucu bir yol için farklı HTML kabuğu döndürmeye başlarsa sw.js gezinme önbelleğinden o yol çıkarılır ve sürüm artırılır.

## H131a — `/react-dom/` eşleşmesi react-dom/server'ı her sayfanın açılış parçasına sokuyordu (2026-10-28)
- **Belirti:** `vendor-react` parçası 137 KB gzip (react + react-dom istemci ~60 KB olmalı); öğrenci ve yönetim açılışı gereksiz 70 KB taşıyordu.
- **Kök neden:** `manualChunks` `includes('/react-dom/')` ile eşleşiyordu: yalnız PDF dışa aktarımında (`v15/dersPdfHtml.ts`) dinamik kullanılan `react-dom/server` ve `@floating-ui/react-dom` aynı açılış parçasına zorlanıyordu.
- **Çözüm/kural:** Paket kökü düzenli ifadesi (`/node_modules/(react|react-dom|scheduler)/`) ve `react-dom/server|static` hariç. `vendor-react` 65,9 KB gzip; öğrenci açılışı 544 → 475 KB gzip. Elle parça gruplarken paket adı alt dize ile değil kök yolla eşlenir.

## H131b — Kişiler listesi arka tazelemesi 2,5 sn olay döngüsünü kilitliyordu (2026-10-28)
- **Belirti:** Panelde sayfa geçişlerinde ilgisiz istekler (people-access, basarim/kisiler, calisma-matris) aynı anda ~2 sn bekliyordu; tek başına çağrıldıklarında 5 ms.
- **Kök neden:** `peopleInsights.buildList` kişi başına `contributions(p)` çağırıyordu: her kişi için bütün çıkmış/havuz soruları taranıyor ve `learn_feedback.json` + `ornek_soru_bildirimleri.jsonl` yeniden okunuyordu (≈900 kişi × 6.000 soru). SWR liste her istekte arka planda yeniden hesaplandığından eşzamanlı her yönetim isteği bekliyordu.
- **Çözüm:** `contributionCountsAll(ps)` tek geçişte kimlik/ad dizinleriyle sayar (eşleşme kuralları birebir; 895 kişide sayılar önce/sonra aynı). `/api/admin/people` 2,5 sn → 0,05–0,15 sn. **Kural:** kişi × veri kümesi döngüsü yazılmaz; ters dizin bir kez kurulur.

## H131c — v16 kabuğu her alt yol değişiminde sayfayı yeniden kuruyordu (2026-10-28)
- **Belirti:** Satır çekmecesi açıp kapatınca liste baştan çekiliyor, kaydırma/sayfa kayboluyor, odak satıra değil `<main>`'e dönüyordu.
- **Kök neden:** `ManageV16.git()` her çağrıda `gezinti` sayacını artırıyordu; sayfa `key`'i buna bağlı olduğundan alt yol (`/sorular/cikmis/<id>`) değişimi de yeniden bağlama demekti; ardından `<main>` odaklanıyordu.
- **Çözüm/kural:** Aynı sayfa içinde yalnız alt yol değişirse sayfa yeniden kurulmaz, odak/kaydırma korunur (aynı adrese yeniden tıklama sıfırlar). Çekmece açma 1 istek (önce liste + ayrıntı).

## H131d — Dar ekranda süzgeç çipleri tabloyu ekran dışına itiyordu; kesik süre hücreleri (2026-10-28)
- **Belirti:** 375 px'te Çıkmış sayfasında süzgeçler (Ders ~40, Yıl ~20 seçenek) 1,5 ekran kaplıyordu; 1440 px'te Kişiler "7 gün/Çalışma" hücreleri "3 sa 14 …" diye kesiliyordu; dokunmatikte düğme/çip 22–30 px, iOS'ta 13,5 px girdiler odakta yakınlaştırıyordu.
- **Kök neden:** `.m16-cip-grup` `flex-wrap: wrap`; sabit 80–96 px sütunlar "N sa M dk" biçimine dar; kit dokunmatik ölçüsü tanımlamıyordu.
- **Çözüm/kural:** Her süzgeç grubu tek satır yatay kaydırılır (etiket sabit); süre sütunları ≥100 px, kesilen düz metin hücresi `title` taşır; `@media (pointer: coarse)` düğme/ara/girdi 40 px, çip 32 px, alan yazısı 16 px. Kısa değer (≤14 karakter) hücrede kesilmez — tarama betiği bunu denetler.

## H131 — Kurul 2 çıkmışlarında başka kurul soruları ve yanlış konu etiketleri (2026-10-28, kullanıcı bildirdi)
- **Belirti:** Kurul 2 çıkmışları arasında Kurul 1/3/5 konusu sorular (genel farmakoloji, tetanoz, Negri, halk sağlığı, pediatrik kabızlık, C8 kökü) ve komşu derse etiketlenmiş Kurul 2 soruları vardı.
- **Kök neden:** Soru kurulu sınav belgesinin kurul etiketinden geldi, ders/konu etiketi ise içerikle doğrulanmadı; Check-Solve/Faz 14 onayı da konu uygunluğunu kanıtlamaz.
- **Çözüm:** 574 soru ders programı + kazanım + 25-26 ders metni ile tarandı (`meds_temp/kurul2_soru_tespit/`, rapor `meds_database/derived/quarantine/kurul2_konu_tespit.csv`). 19 soru `karantina.json`'a `neden: kurul2_disi` ile yazıldı (`kaynakBulunamadi` bu nedeni de onay muafiyetinden önce uygular); 52 soruda konu/ders etiketi düzeltildi (`eskiKonu`/`eskiDers` saklı). 9 Primer Myelin önerisi 2026 programında ders olmadığı için uygulanmadı. Yedekler aynı klasörde.
- **Önleme kuralı:** Yeni çıkmış eşlemesinde konu etiketi içerik ile doğrulanır; geri alma: karantina kaydını silmek / eskiKonu'yu geri yazmak. Açık: 86 "elle bakılmalı" soru.

## H132 — Karantina listesi eskimişti; OCR ikizleri ve parça kayıtlar karantinada duruyordu (2026-10-28)
- **Belirti:** Karantinada 513 (eski `karantina.json`) + 47 `status=quarantined` + 86 `kaynak_bulunamadi` kayıt görünüyordu; çoğu aslında düzelmişti.
- **Kök neden:** (1) `karantina.json` 2026-10-07'den kalmaydı; 314+109 kayıt sonradan Check-Solve/Faz 14 ile onaylanmıştı, 43'ü Faz 17'de çöpe alınmıştı, 29'u kayıttan düşmüştü. (2) 53 karantina kaydı temiz bir ikizi olan OCR/site-kalıntısı kopyaydı (örn. `past-q-22_final_…-117` ↔ `q-22_final_…-117`; `ff640ee5472c` CYBE sorusunun parçası) — yanlış kümeleme/OCR bunları "bozuk soru" yaptı; bazılarında cevap bile yanlıştı (PBS sorusunda A işaretli, temiz ikizde D). (3) 84 `d3-k2-*`/türev kayıt çıkmış değil, ders notundan üretilmiş geçerli sorular; "Çıkmış Sınav / 2021-2026" etiketi yanlıştı.
- **Çözüm:** 53 kopya `birlestirmeler.json` grubuna (tekrar arşivi) alındı, `tekrarArsivi{asil,eslesen,onceki}` ile geri alınabilir; `karantina` etiketi ve `karantina.json` girdisi kaldırıldı. Yedek: `yedek/karantina_20261028/`.
- **Önleme:** Karantinaya almadan önce aynı soru/şık kümesine sahip sağlam kayıt aranır (stem+şık Jaccard); varsa karantina değil tekrar arşivi. Üretilmiş soru "çıkmış" etiketi taşımaz.

## H133 — Kaynağı doğrulanamayan sorular gizlenerek kaybedilmişti; "Çıkmış–Örnek" sınıfı (2026-10-28)
- **Belirti:** 104 soru (85 `kaynak_bulunamadi` + 19 `kurul2_disi`) karantinada duruyordu; çoğu tıbben doğru, müfredata uygun veya gerçek sınav sorusuydu.
- **Kök neden:** "Özgün belgede bulunamadı" ile "yanlış/bozuk" aynı kovaya konmuştu; gerçek çıkmış olma ihtimali olan sorular da gizlendi. Kurul 2 dışı tespiti Santral Sinir Sistemi Enfeksiyonları gibi Kurul 2 derslerini kaçırdı.
- **Çözüm:** 4 bağımsız denetçi 104 soruyu müfredat + ders notu + tekrar taramasıyla değerlendirdi: 72 `cikmis_ornek` (hem Çıkmışlar'da hem `k2-cikmis-ornek` Örnek sorular dersinde, öğrenciye "çıkmış olduğu doğrulanmadı" rozetiyle; sesli ders çıkmış chip'inden hariç), 15 serbest çıkmış, 9 tekrar arşivi, 7 karantinada (`siniflama` alanıyla gerekçeli). 5 soru ders notuna göre düzeltildi (`duzeltmeOnceki` saklı).
- **Önleme:** Kaynağı doğrulanamayan ama doğru soru gizlenmez, `kaynakSinifi=cikmis_ornek` ile etiketlenip öğrenciye belirtilir; çıkmış vurgusu yalnız doğrulanmış kaynağa dayanır.

## H138 — Sekmede açılan görsel/JSON yanıtı site kabuğu diye önbelleğe yazılıyordu (2026-10-28, sayfa denetimi)
- **Belirti:** Önizleme tarayıcısında `/` ve `/bugun` site yerine yalnız favicon gösterdi; bir dosya adresini doğrudan açan öğrencide yavaş ağda sonraki açılışlar site yerine o dosyayı verir.
- **Kök neden:** `sw.js` gezinme işleyicisi 200 dönen her `navigate` yanıtını içerik türüne bakmadan `/` ve `/index.html` olarak yazıyordu; 0,4 sn içinde ağ yanıtı gelmezse kabuk diye o kayıt veriliyordu.
- **Çözüm/kural:** Yalnız `Content-Type: text/html` yanıt kabuğa yazılır; `CACHE_VERSION` v19 kirlenmiş eski kabuğu siler. Kabuk önbelleğine yazan her yol içerik türünü denetler.

## H139 — Gizlenen sayfaya giden bağlantı öğrenciyi açıklamasız Bugün'e atıyordu (2026-10-28, sayfa denetimi)
- **Belirti:** /kamplar'daki "Kamplar" sekmesi, takvimdeki T-5 adımı, Bugün'deki "Günün spotu", `/olasi-sorular` tıklanınca Bugün açılıyordu; öğrenci neden olduğunu anlamıyordu.
- **Kök neden:** Merkez kartları `menudeGorunur` ile süzülüyordu ama sekmeler, takvim adımları ve Bugün bağlantıları süzülmüyordu; App.tsx gizli sayfayı sessizce `setActiveTab('today')` ile değiştiriyordu.
- **Çözüm/kural:** Sekmeler (`gorunenSekmeler`), takvim hazırlık adımları ve Günün spotu bağlantısı `menudeGorunur` ile süzülür; adresle girilen gizli sayfa "Bu sayfa şu an kapalı" ekranı + Ne yapmak istiyorsun kartlarını gösterir. Bir sayfaya bağlantı veren her yer `menudeGorunur(route)` denetler.

## H140 — Bazı sayfalar aktif kurul yerine Kurul 1 ya da "Tümü" ile açılıyordu (2026-10-28, sayfa denetimi)
- **Belirti:** Aktif kurul 2 iken Kazanımlar Kurul 1, Örnek sorular tüm kurulları karışık (sayaçlar yalnız k1-), Test oluştur "Tümü" ile açılıyordu; Öncelikli dersler Kurul 1 olduğunu söylemiyordu.
- **Kök neden:** Sayfalar varsayılanı sabit `1`/`'all'` yazmıştı; `varsayilanKurul()` (son seçim → takvim) kullanılmıyordu.
- **Çözüm/kural:** Kazanımlar, Örnek sorular (kurul seçici + kurul önekli sayaçlar), Test oluştur (kayıtlı ölçüt yoksa) `varsayilanKurul()` ile açılır; yalnız Kurul 1 verisi olan Öncelikli dersler bunu başlıkta yazar. Yeni kurul bağımlı sayfa varsayılanını `varsayilanKurul()`dan alır.

## H141 — Yönetimde görünürlük tek tıkla, onaysız ve geri alınamaz yazıyordu (2026-10-28, sayfa denetimi)
- **Belirti:** Site › Görünürlük ve ders/deste/önem görünürlük çiplerinde yanlış tık sayfayı/dersi tüm öğrencilere anında kapatıyordu; hangi sunucuya yazıldığı da yazmıyordu.
- **Kök neden:** Çip `onClick` doğrudan `siteAyarYaz`/PUT çağırıyordu; kit bildiriminde eylem yoktu.
- **Çözüm/kural:** Öğrenciden kaldıran değişiklik (gizli/kapalı/yalnız yönetici, menüden kaldırma) hedef sunucuyu (`yazimHedefi()`: canlı site / yerel sunucu) yazan onay ister; her yazım 8 sn "Geri al" bildirimi verir (`bildir(metin, ton, {etiket, yap})`).

## H142 — Mesaj/şikâyet yazarından kişiye geçilemiyordu (2026-10-28, sayfa denetimi)
- **Belirti:** Topluluk mesaj çekmecesi yazarı yalnız uid kodu olarak gösteriyordu; kişinin diğer mesajlarını görmenin yolu yoktu.
- **Çözüm/kural:** `MesajTablosu` `git` alır; Yazan sütunu ve çekmece Kişi 360'a, "Tüm mesajları" `topluluk/mesaj?s.uid=` süzgecine bağlanır; Kişi 360'ta "Mesajları" düğmesi. Kişiye ait her kayıt panelde kişiye bağlantı verir.

## H143 — Yönetim tablolarında uzun içerikli satırın sütunları kayıyordu (2026-10-28)
- **Belirti:** Mesajlar'da oda mesajı satırlarında Mesaj/Kanal/Şikâyet sütunları başlıktan sağa kaymış, Durum ekran dışındaydı.
- **Kök neden:** Her satır ayrı ızgara ve `.m16-satir { min-width: max-content }`: uzun içerikli satır kendi genişliğine büyüyüp fr sütunlarını başlıktan farklı dağıtıyordu.
- **Çözüm/kural:** VeriTablosu sütun px alt sınırlarının toplamını `--m16-tablo-en` olarak verir; tüm satırlar aynı en küçük genişliği paylaşır (telefonda yatay kaydırma korunur). Satır ızgarası içeriğe göre genişlemez.

## H144 — Deneme ekranında soru numarası çubuğuna dokunulamıyordu; telefonda süre gizliydi (2026-10-28, sayfa denetimi)
- **Belirti:** 20 soruluk denemede soru düğmeleri 6 px yüksekliğindeydi (telefonda 7×6 px); 420 px altında süre göstergesi tamamen kayboluyordu.
- **Kök neden:** Görünen çizgi ile dokunma alanı aynı öğeydi (`button { height: 6px }`); dar ekranda yer açmak için süre gizlenmişti.
- **Çözüm/kural:** Düğme 24 px dokunma alanı, görünen çizgi `::before`; telefonda süre kalır, doğru/yanlış sayaçları kalkar (soru numarası çubukta). İnce göstergelerde dokunma alanı görsel çizgiden ayrı tutulur.

## H145 — Örnek sorularda "Başla" düğmesi harf harf dikey yazılıyordu (2026-10-28, sayfa denetimi)
- **Belirti:** Masaüstü ders listesinde her satırda B-a-ş-l-a alt alta, satır ~160 px uzuyordu.
- **Kök neden:** v15 kart eylemi (`.ks15-eylem`) v12 satır ızgarasında alan (`grid-area`) almadığı için kendiliğinden 30 px'lik numara sütununa yerleşiyordu.
- **Çözüm/kural:** Izgaraya `ey` alanı eklendi (masaüstü sağ sütun, telefonda ayrı satır). Izgara satırına yeni öğe ekleyen her katman ona alan tanımlar.

## H146 — Yönetim tabloları telefonda okunmuyordu (2026-10-28, sayfa denetimi)
- **Belirti:** 375 px'te tablolar yatay kayıyor, ilk ekranda 2-3 sütun görünüyor, durum/görünürlük/eylem sütunları ekran dışında kalıyordu.
- **Çözüm/kural:** VeriTablosu ≤640 px'te kart görünümüne geçer: başlık satırı gizli, ilk hücre kart başlığı, diğerleri "Sütun adı · değer" (`data-baslik`), seçim kutusu sağ üstte; kart yüksekliği değiştiği için sanal kaydırma kapanır. Yeni tablo sütunlarına düz metin `baslik` verilir (kart etiketi buradan gelir).

## H147 — Öğrenci menüsünde hesap ve ders sayfaları yanlış gruplardaydı (2026-10-28, sayfa denetimi)
- **Belirti:** Başarımlar Oyunlar'da, Güncelleme günlüğü Başvuru'da aranıyordu; Öncelikli dersler ve Geçmiş kurullar Başvuru'daydı ve telefonda alt sekmede "Menü" yanıyordu.
- **Çözüm/kural:** Öncelikli dersler + Geçmiş kurullar → Ders çalış (merkez, menü, alt sekme "Ders"); Başarımlar + Güncelleme günlüğü → Kişisel. Grup değişikliği `merkezModel.MERKEZ_HAM`, `navModel.NAV_TREE_HAM` ve `navV15` (OYUNLAR/KISISEL) birlikte yapılır; adresler değişmez.

## H148 — Ders çalış merkezinde "hepsini bitirdin ya da henüz ders yok" ikili mesajı (2026-10-28, sayfa denetimi)
- **Belirti:** Kurul 2'de hiç sesli ders yokken öğrenciye "hepsini bitirdin ya da henüz ders yok" deniyordu; yapılacak bir şey önerilmiyordu.
- **Çözüm/kural:** Kurulda ders var ve hepsi bitti → "hepsini bitirdin" + tüm dersler bağlantısı; ders yok → "henüz eklenmedi" + önceki kurula geçiş. Boş durum metni iki ayrı durumu tek cümlede birleştirmez, bir eylem verir.

## H149 — Aramada "Sesli derste geçen yerler" stilsiz görünüyordu (2026-10-28, sayfa denetimi)
- **Belirti:** Ders adı ile cümle parçası bitişik ("Patolojiye GirişFormalin…"), zaman damgası metne yapışık.
- **Kök neden:** `SesliYerler.tsx`'te `import '../../styles/sesli-yer.css'` satırı dosya başındaki `/** … */` yorum bloğunun içine düşmüştü; stil dosyası hiç yüklenmiyordu (derleme hata vermez).
- **Çözüm/kural:** İçe aktarma yorumun dışına alındı; depoda aynı kalıp tarandı (başka yok). Belge yorumunun içine kod satırı eklenmez; stil "kural var ama uygulanmıyor" görünüyorsa önce içe aktarmanın gerçekten çalıştığına bakılır.

## H150 — Güncelleme günlüğünde öğrenciye dosya yolları görünüyordu (2026-10-28, sayfa denetimi)
- **Belirti:** "Geliştirme notları" kapalıyken bile öğrenci maddelerinde `meds/scripts/...`, `*.json` gibi yollar vardı.
- **Kök neden:** Öğrenci maddeleri (`ogrenci`) sürüm notlarından üretilirken teknik ayrıntı temizlenmiyordu; ekran olduğu gibi basıyordu.
- **Çözüm/kural:** Ekran öğrenci maddelerinden kod parçasını, dosya yolunu ve yollu parantezi siler; 3 kelimeden kısa kalan maddeyi göstermez. `guncelleme_notu.json` maddeleri öğrenci diliyle yazılır, dosya yolu içermez.

## H151 — Sağlık Bakanlığı uzun bölümlerinde başa dönüş yoktu; geçmiş düğmesi küçüktü (2026-10-28, sayfa denetimi)
- **Belirti:** Aşı bölümü telefonda ~17.000 px; yukarı dönmenin tek yolu kaydırmaktı. "N yılın geçmişini göster" düğmesi 49×18 px.
- **Çözüm/kural:** 1200 px aşağıda "Başa dön" düğmesi (kaydırılan kabı olaydan bulur); geçmiş düğmesine `::after` ile ~57×34 dokunma alanı. Not: "Kaynak N" bağlantıları zaten `::after` ile büyütülmüştü, tarama aracı bunu göremez (yanlış bulgu).

## H152 — Yönetimde ders ayrıntısından o dersin sorularına geçiş yoktu (2026-10-28, sayfa denetimi)
- **Çözüm/kural:** Sorular kartında örnek sorular, çıkmış sorular ve havuz için ders konusuyla süzülmüş (`?q=<konu>`) bağlantılar. Sayı gösteren her özet, o kayıtların listesine bağlanır.

## H153 — Yönetimde Yerel kipte hangi veriye bakıldığı belli değildi; birleştirmede asıl soru görünmüyordu (2026-10-28, sayfa denetimi)
- **Belirti:** Yalnız Canlı kipte bant vardı; Yerel'de hiçbir işaret yoktu. Havuz birleştirmede asıl soru görünmeyen seçim sırasına bağlıydı. Ders ayrıntısında görünürlük seçicisi kartın dışına taşıyordu.
- **Çözüm/kural:** Yerel bandı + sekme adında `[Canlı]`/`[Yerel]`; birleştirme onayında asıl soru açılır listeden seçilir; `.m16-liste` satırı sarar, seçici alt satıra iner.

## H154–H169 — Sayfa denetimi dördüncü tur, öğrenci sitesi orta bulguları (2026-10-28)
- **H154/H155 Kutlama:** kuyruk hangi ekranda olursa olsun hemen açılıyordu → deneme, çıkmış testi, soru çözücü ve sesli ders ayrıntısında ertelenir. Rozetteki "3" ödül seviyesiydi, "Hepsini geç" sayısı bu ödülü saymıyordu → "3. seviye" ipucu, sayaç tüm kuyruk.
- **H156 Bugün:** halka öğrencinin çalışmasını, alt kart okul programını gösteriyordu (farklı veri, aynı dil) → "bugün çalışma yok" / "Okuldaki bugünkü 2 ders sona erdi".
- **H157 Deste sayısı:** merkez yayında olmayan desteleri de sayıyordu → kitaplıkla aynı ölçüt (`isPublished`, `kurulOf`).
- **H158 Sesli ders süzgeci:** "2026–27/2025–26" etiketleri telefonda satırı taşırıyordu → "Bu yıl/Arşiv"; boş listede "Geçen yılın derslerini aç".
- **H159/H160 Soru çöz kartları, Yanlışlarım:** uzun etiket/kırılan düğme → kısa ad, tek satır; boş Yanlışlarım'da "Soru çözmeye başla".
- **H161 Boş Check Up:** düz metin → başka kurulun check-up'ı ve hazırlık araçlarına düğme.
- **H162 Kazanım "8/2":** veri doğruydu ("0/2"); sabit genişlikli yazı tipinin çizgili sıfırı 8 okunuyordu → normal yazı tipi + tabular rakam. Sayaçta mono yazı tipi kullanılmaz.
- **H163 Sınav planı hız çipleri:** 40×19 px → ≥32 px.
- **H164 /profil:** /ayarlar ile aynı ekran → adres /ayarlar'a döner (eski bağlantı çalışır).
- **H165–H167 Boş durumlar:** İstatistik (çalışmaya başla), Sıralama (Üniversiteni seç), Arkadaşlar (Giriş yap: App.tsx `medsoru:giris-ac` olayı).
- **H168 Bildirimler:** eylem satırı kırılmıyordu ("Ok" kesik); silinemeyen okunmuşlar "temizle"yi etkin tutuyordu → satır sarar, düğme yalnız silinebilir varken etkin.
- **H169 Telefonda kurul:** üst çubukta kurul yolu yoktu → kompakt "K2" çipi.
- Masaüstü 24 px alt şerit uygulamada yeniden üretilemedi (tarama aracının boyut geçişi kalıntısı); değiştirilmedi.

## H170–H185 — Sayfa denetimi dördüncü tur, yönetim paneli orta bulguları (2026-10-28)
- **H170 Kurul çipi "1 66":** etiket yalın rakam + aynı boyutta sayı → "Kurul N" + soluk sayı rozeti.
- **H171 Yüklenirken "0 kayıt":** sayaç yükleme durumuna bakmıyordu → "Yükleniyor…", seçeneksiz süzgeç satırı gizli.
- **H172 Açıklamalarda dosya yolu/jargon:** yönetici diline çevrildi; yol küçük ikincil etiket.
- **H173 Son yönetici işlemleri:** okuma kayıtlarıyla doluyordu → yalnız yazma (`sonDenetimler(8, true)` + istemci süzgeci).
- **H174 Bellek "1462 / 234 MB":** RSS ve yığın etiketsiz yan yanaydı → ayrı satırlar, `yiginToplamMb` eklendi.
- **H175 Gelen kartları:** sıfır kartlar gizli, hepsi sıfırsa "Bekleyen iş yok".
- **H176** Çıkmış "Cevap" başlığı 56→72 px. **H177** Birleşenler "Ayır" yazılı onay + Geri al. **H178** Taslaklar kendi çekmecesini açar, dönüşte süzgeç korunur.
- **H179 Askı gerekçesi `window.prompt`:** kit onay penceresine gerekçe alanı (`gerekceIste`, ≥3 karakter); Kişi 360, Erişim, Kişiler.
- **H180** Oyun odası "Kapat" satır çekmecesinde. **H181** Erişim, DB satır yazımı, duyuru onaylarında hedef sunucu (`yazimHedefi()`); duyuru yayınlama artık onaylı.
- **H182 Betik tehlikesi:** ad regex'i yerine izin listesi: yalnız bilinen salt okunur betikler onaysız, gerisi yazılı onay.
- **H183 Yedek içe aktarma:** ezmeden önce `/api/admin/db/export` ile mevcut havuz indirilir, başarısızsa iptal (kalıcı çözüm: sunucu import ucu kendi yedeğini almalı — açık).
- **H184 Çöp kutusu:** tek seçenekli "Tür" süzgeci gizleniyordu → gösterilir; Silinme süzgeci (bugün/7/30 gün/eski).
- **H185 Site › Menü:** erişimi kapalı sayfada anahtar kilitli + açıklamalı; menüden gizleme onaylı, her yazım Geri al.

## H200–H212 — Sayfa denetimi beşinci tur, öğrenci sitesi kalan bulgular (2026-10-28)
- **H200/H201/H205/H210 Sınava hazırlan:** boş "Planlama" başlığı yalnız içerik varken; sınav ağırlığı kartı nereye gittiğini söylüyor; olası sorular kartı ATP kilidini önceden yazıyor; telefonda sekme şeridi kenarda solar.
- **H202/H203 Soru haritası:** yılı belirsiz "?" sütunu renk ölçeğine katılıp en koyu hücreleri alıyordu → "Yılsız", sona alındı, ölçek dışı; telefonda yana kaydırma ipucu. Kural: belirsiz/eksik kategori renk ölçeğini belirlemez.
- **H204** Çıkmış arama yer tutucusu telefonda kesikti → anahtar sözcük önde.
- **H206/H207 Sesli ders:** küçült düğmesi `::after` ile ~44 px; bölme hap düğmeleri ≥28 px + aria-label.
- **H208** Hastalık dipnotları `::after` dokunma alanı.
- **H209 Çift başlık:** v15'te sayfa adı hem üst çubukta hem `PageHeader` h1'de görünüyordu → v15'te PageHeader başlığı görsel olarak gizli (ekran okuyucu için h1 kalır). Site geneli kural; yeni sayfa başlığı v15'te üst çubuktan gelir.
- **H211/H212 Sağlık:** açıklamasız sayı rozetleri dipnot biçiminde ("[14]"); "15 yıl" → "15 yıllık geçmiş".

## H250–H268 — Sayfa denetimi beşinci tur, yönetim paneli kalan bulgular (2026-10-28)
- Genel bakış kart adları ve hedefleri (topluluk şikâyeti, istemci hatası → Gelen süzgeci), yük renk eşiği, sürüm etiketi (H250–H253).
- Bağlantılar: Ctrl/orta tık yeni sekme (H254), `manageAdres` (H255), Çıkmış ve Birleşenler içi bağlantılar panel içi gezinme (H256, H266), Branşlar → derslere (H265).
- Metin/ad netliği: Ham defter dışa aktarım (H257), Faz 14 → "Çıkmış inceleme (Faz 14)" (H259), Kamplar → "Kamp tüyoları" (H260), benzer menü adları ayrıştırıldı (H261), Sözlük silinemez sekme açıklaması (H267), katalog form alanlarına Türkçe etiket (H268).
- Onaylarda hedef sunucu: bakım ve LLM işleri (H262, H263; kural 20 davranışı değişmedi). Faz 14'te kimliksiz satır bildirimi (H258).
- **H264 Boş tablo:** yalnız "Kayıt yok" diyordu → süzgeç mi kaynak mı boş söylenir, yerelde Canlı önerisi.
- Kapsam dışı bırakılan öneriler: menünün baştan düzenlenmesi, görünürlüğün tek yerde toplanması, Çıkmış/şikâyet toplu işlemleri, kirli kurul etiketlerinin veri temizliği, üç "bugün" sayfasının birleşmesi, oynatıcı araç çubuğu yeniden tasarımı, çıkmış listesinde sayfalama.

## H220 — Üç sayfa aynı "bugün ne yapayım" işini bölüyordu (2026-10-28, sayfa denetimi; kullanıcı isteği)
- **Belirti:** Bugün (plan halkası, akış, hafta çubukları), Çalışma masam (hafta şeridi, günün etkinlik akışı, bugünkü süre, seri + soru çalışma alanı) ve Ders çalış merkezi (devam et) aynı soruya üç ayrı yerden cevap veriyordu; iki ayrı hafta görünümü vardı.
- **Kök neden:** Çalışma masamın v15 üst bölümü (`MasaGunV15`) Bugün'den bağımsız tasarlanmış, sonra Bugün'e hafta çubukları eklenmişti; sayfaların görev sınırı tanımlı değildi.
- **Çözüm/kural (görev sınırı):**
  - **Bugün** = günün tek sayfası: plan halkası → Kaldığın yerler (araçlar arası devam) → hafta şeridi + Bugün yaptıkların (`MasaGunV15 gomulu`; yan kartlar gizli, süre/seri halkada ve şeritte). Hafta çubukları kaldırıldı.
  - **Listelerim ve notlar** (eski Çalışma masam, `/calis` aynı) = yalnız kişisel soru çalışma alanı (Soru çöz, Test, Listelerim, Notlar).
  - **Ders çalış merkezi** = ders araçları merkezi; "Devam et" yalnız sesli ders içindir.
  - Yeni "günlük özet" öğesi yalnız Bugün'e eklenir; diğer sayfalar kendi aracının durumunu gösterir.

## H239–H241 — Ders programı: import.meta.glob anahtarı + numara eşleşmesi (2026-10-28)
- **Belirti:** /dersler/program'da Kurul çipleri hiç yoktu; Kurul 1 açılınca "Invalid Date" başlığı.
- **Kök neden:** `import.meta.glob` anahtarları globu çağıran dosyaya göredir (`services/programVeri.ts` → `../data/…`); bileşen `../../data/…` arıyordu. Sesli ders eşlemesi arşiv önekini atıp yalnız `kN-NN` numarasına bakıyordu (yıllar arası numara kesin değil). Tarihi boş kayıt `tarihYaz('')`'a gidiyordu.
- **Kural:** glob kaydını başka dosyadan sorgulama, kaynağın yardımcısını (`programVar`) kullan; ders↔sesli bağlantısı yalnız `ders_id_tam` birebir başlangıcıyla; boş tarih ayrı etiketle.

## H242 — Çıkmış listesinde konum yoktu; geri dönünce liste baştan açılıyordu (2026-10-28, kullanıcı isteği)
- **Belirti:** Varsayılan Kart görünümü sonsuz kaydırmaydı (20'şer yükleme, en çok 60 kart penceresi); kaçıncı soruda olunduğu görünmüyor, bir soruya ya da başka sayfaya gidip dönünce liste ilk 20 soruyla açılıyordu. Kompakt görünümde yalnız "3 / 26" vardı.
- **Kök neden:** Konum yalnız bileşen durumunda (richLimit/currentPage) tutuluyordu; bileşen kalkınca kayboluyordu. Kaydırmayla ilerleyen pencere sayfa kavramı taşımıyordu.
- **Çözüm/kural:** Liste/Panel yerleşiminde iki görünüm de sayfalı (Kart 20, Kompakt 25): üstte "41–60 / 571 soru · sayfa 3/29", altta Önceki · sayfa seçici · Sonraki (`cikmis/CikmisSayfa.tsx`). Konum (süzgeç imzası + sayfa + sayfadaki sıra) `sessionStorage cikmis_konum`'a yazılır; dönüşte aynı sayfa açılır ve aynı soru yapışkan üst çubuğun altına yerleşir. Tuzaklar: rotadan çıkarken yapılan "başa kaydır" kaydı bozar (kayıt yalnız çıkmış adresindeyken), `scrollIntoView` yapışkan çubuğun altına gizler (ölçüm ve yerleştirme `.v15-top` alt çizgisine göre), geri yükleme birkaç kez yerleştirilir ve bitene dek kaydedilmez. Uzun liste ekranlarında konum sayfa + sıra olarak saklanır.

## H290–H295 — Yönetimde iş akışı uzundu: Gelen yalnız yönlendiriyordu, toplu işlem yoktu (2026-10-28, sayfa denetimi)
- **Belirti:** Gelen'deki her iş için başka sayfaya gidip dönmek gerekiyordu (soru şikâyeti en az 4 tıklama); soru şikâyetleri ve çıkmışlarda toplu işlem yoktu; gizlenen topluluk mesajı Gelen'de kalıyordu; istemci hatası için hiç işlem yoktu.
- **Kök neden:** Satır yalnız `git(hedef)` çağırıyordu; Gelen 15 sn önbelleği işlem uçlarınca temizlenmiyordu; Gelen sorgusu `silindi`'ye bakmıyordu.
- **Çözüm/kural:** Gelen'de satır ve çekmece işlemleri (Çözüldü / Yok say / Mesajı gizle / Kapat + iç not / Görüldü), aynı türde toplu işlem; `gelenOnbellekSil()` işlem uçlarında; yeni uç `POST /api/admin/gelen/hata/goruldu` (işaret `data/istemci_hata_goruldu.json`, hata yinelenirse geri düşer); VeriTablosu `dusur(t)` ile işlenen satır süzgeç/sayfa korunarak düşer. Soru şikâyetlerinde çekmeceden Çözüldü + toplu; çıkmışlarda toplu Gizle/Göster (onay + hedef + 8 sn Geri al). Not: "Yok say" şikâyeti `resolved` yapar (ayrı red durumu yok).

## H296 — Gelen'de tek satır işlemleri onaysız ve geri alınamazdı (2026-10-28, ajan sınaması)
- **Belirti:** Gelen'de "Çözüldü"/"Yok say"/"Mesajı gizle"/"Kapat" tek tıkla canlıya yazılıyor, yanlış tık geri alınamıyordu; Soru şikâyetlerinde tek çözme de geri alınamıyordu.
- **Kök neden:** H290'da onay yalnız toplu işleme konmuştu; işlemlerin tersi tanımlanmamıştı.
- **Çözüm/kural:** Tersi olan işlemler (soru şikâyeti → yeniden aç, mesaj gizle → göster, geri bildirim kapat → aç) 8 sn "Geri al" verir, geri alınan satır listeye döner; tersi olmayan (topluluk şikâyetini yok say: şikâyet kayıtları silinir) tek işlem de "geri alınamaz" diyen onay ister. Yerelde tıklanarak sınandı (Çözüldü → Geri al, çıkmış toplu Gizle → Geri al; veri eski hâline döndü).
- **Sınama notu:** Sınama betiği satır düğmesini sayfa genelinde ararsa yanlış satıra basar; düğme her zaman ilgili satırın/çekmecenin içinde aranır.

## H300–H311 (öğrenci) — Çevrimdışı ve Arka plan işleri aynı işi iki sayfada yapıyordu (2026-10-28, sayfa denetimi)
- **Belirti:** "Yalnız Wi-Fi" iki sayfada iki farklı denetimle (anahtar / onay kutusu), eşitleme kartı ve indirilenler iki kez; Arka plan işlerinin menüde belirsiz karşılığı.
- **Çözüm/kural:** Tek sayfa "Çevrimdışı ve indirmeler" (`/cevrimdisi`): durum → indirme kuyruğu ve arka plan işleri (`#isler`, ArkaPlanV15 gömülü) → toplu indir → indirilenler ve depolama → ayarlar ve eşitleme (tek Wi-Fi denetimi, aynı `ayar.wifi` anahtarı). `/arka-plan`, `/arka-plan-isleri` → `/cevrimdisi#isler`. Bir ayar sitede tek yerde düzenlenir.

## H310–H314 (yönetim) — 69 sayfalık menüde bulunabilirlik (2026-10-28, sayfa denetimi)
- **Çözüm:** Sabitlenenler (`m16_sabit`), Son kullanılanlar (`m16_son`, 5), ilk açılışta yalnız Genel + etkin grup açık (`m16_kapali_grup` yoksa), menüde ara (etiket + `anahtar`, Türkçe harf duyarsız, Esc temizler), telefonda ≥32 px hedefler. Menü yapısı ve adresler değişmedi.

## H320–H329 — Görünürlük beş ayrı yerden düzenleniyordu (2026-10-28, sayfa denetimi; kullanıcı isteği)
- **Belirti:** Site › Görünürlük, Site › Menü, Kurullar, Dersler ayrıntısı, Sesli dersler, Önem ve çözücü, İçerik paketleri ve Desteler aynı `site_ayar.gorunurluk`/`sayfalar`/`menu` verisini satır içi seçicilerle yazıyordu; hangisinin geçerli olduğu ve nereden değiştiği belirsizdi.
- **Kök neden:** Paylaşılan `GorunurlukSecici` her sayfaya düzenleme yetkisiyle gömülmüştü; tek doğruluk yeri tanımlı değildi.
- **Çözüm/kural:** Görünürlük YALNIZ Site › Görünürlük'te yazılır: "Sayfalar" (öğrenci sayfaları + menü) ve "İçerik" (kurul, ders, sesli, deste, paket, önem/asistan/çözücü; yeni uç `GET /api/admin/gorunurluk/icerik`, sayfalı, süzgeçli, katalogda olmayan ayar `sahipsiz`). Diğer sayfalarda `GorunurlukBaglantisi` (rozet + "Değiştir" → `site/gorunurluk?sekme=icerik&q=<anahtar>`). `site/menu` → Görünürlük. Gizleme onay + hedef, her yazım 8 sn Geri al, toplu değiştirme. Yerelde tıklanarak sınandı (tek + toplu, geri al sonrası ayar boş).

## H330–H334 — Sesli ders araç çubukları kalabalıktı (2026-10-28, sayfa denetimi; kullanıcı isteği)
- **Belirti:** Masaüstünde üst çubukta 11 düğme (görünüm, A−/A+, yıldız, bilgi, tam ekran, ayar, ⋯), PDF çubuğunda Çıkmış/Kalem/tema/zoom; telefonda üstte 4 simge.
- **Çözüm/kural:** Görünür kalanlar ders boyunca sık dokunulanlar: görünüm kipi, tam ekran (masaüstü), Çıkmış, Kalem, yakınlaştırma (masaüstü). Seyrekler `CdTasmaMenu` ⋯ menüsünde: yazı boyutu (menü açık kalır, değer yazar), yıldızlı paragraflar, terim yardımcısı (✓; açıkken çubukta etkin göstergesi), görünüm ayarları, tüm ders seçenekleri, tam ekran; PDF ⋯: sayfa teması, yakınlaştır/uzaklaştır/sığdır. Menü erişilebilir (aria-haspopup, ↑/↓/Home/End, Esc/dışarı/Tab kapatır, odak düğmeye döner), kısayollar değişmedi, tanıtım turu yeni hedeflere bağlandı (9/8 durak). Çizim/zamanlama mantığına dokunulmadı (kural 17/18). Açık: TV kipinde menü ok tuşları TV katmanına takılabilir; telefonda Kalem 33 px, küçült düğmesi 36×22 px.
- **Kural:** Sesli ders ekranına yeni düğme eklenirken önce sık/seyrek kararı verilir; seyrekse ⋯ menüsüne girer, durum taşıyorsa menüde ✓ ve çubukta etkin göstergesi olur.

## H335–H337 — TV kipinde ⋯ menüsü ve ders ekranında TV kumandası (2026-10-28)
- **H335 Belirti:** TV kipinde ⋯ menüsü açıkken Esc menüyü kapatmıyor, odak menüden düşüyordu; Geri tuşu (GoBack/461/10009) menüyü hiç kapatmıyordu.
- **Kök neden:** TV kumanda dinleyicisi pencere düzeyinde yakalama aşamasında (capture) Esc/Geri'yi alıp odağı bırakıyordu (menünün belge düzeyi dinleyicisinden önce çalışır); menü yalnız `Escape`'i tanıyordu.
- **Çözüm/kural:** Odak `[role="menu"]` içindeyse TV katmanı tuşu menüye bırakır; menü Geri tuş kodlarını da kapatma sayar. Düzeltmeli/düzeltmesiz karşılaştırmayla doğrulandı. Kural: pencere düzeyinde capture dinleyici yazan her katman açık menü/diyalog içindeki tuşları bırakır.
- **H337 Belirti:** Ders ekranında TV kumanda gezinmesi ve kumanda tanıtımı hiç çalışmıyordu.
- **Kök neden:** `cbff0844`'te başlık yeniden yazılırken `<CdTvKumanda />` kaldırılmış, `import` kalmıştı (derleme uyarı vermez).
- **Çözüm/kural:** Bileşen ders ekranına geri bağlandı (TV dışında hiçbir şey çizmez), Kumanda düğmesi köşeye sabit. Kullanılmayan içe aktarma, kaybolmuş bir özellik işareti olabilir; büyük başlık yeniden yazımlarında eski bileşenlerin hâlâ çizildiği kontrol edilir.
- **H336:** PDF şeridindeki Kalem ve Çıkmış düğmeleri dokunmatikte `::after` ile ~44 px dokunma yüksekliği (görünüm aynı). "Oynatıcıyı küçült" zaten H206 ile 44 px'ti; tarama `::after`'ı göremediği için küçük ölçüyordu.

## H340–H347, H360–H374 — Sayfa denetimi düşük önemli bulgular (2026-10-28)
- **Öğrenci (H340–H347):** boş Notlarım'da arama kutusu gizli; bildirim yokken toplu eylemler gizli; müzik ilerleme çubuğu 28 px; Bugün şerit etiketi tek satır; arama sıralama seçici 36 px; sınav planında gereksiz "· K2" eki; topluluk ders yorumları boş durumuna "Derslere git"; İlk adımlar ilerleme çubuğu belirgin.
- **Yönetim (H360–H374):** serbest girdiden soruya, olası sorudan ayrıntıya, ses işinden sesli derse, desteden derse, oyuncudan kişiye bağlantı; Gelen kırıntısı "Yönetim › Gelen"; ders sekmesi (`?sekme=`), kurul ve kamp çekmecesi (`?ac=`) adreste; kurul takvimi bildirimi "dağıtımda yansır"; çöp kalıcı silme onayında hedef; görünürlükte "bayrağa git"; Puan/ATP tehlikeli işlemler açık listeyle (`ozel_kaldir` artık uyarılı); şikâyet sayfasında "Gizlenen mesajlar" kartı; Gelen "Ek" sütunu varsayılan gizli.
- **Kural:** Tehlikeli işlem ad kalıbıyla değil açık listeyle belirlenir (H182, H372). Açık çekmece/sekme adreste tutulur ki yenileme ve paylaşım aynı görünümü açsın.
- Açık öneriler (yapı): menü/başlık ad eşleşmeleri, `kurul_2` adres biçimi, yinelenen girişler (KMB, Sözlük/Hastalıklar, takvim), havuz dondurmanın Bayraklar'a taşınması, ses kuyruğunun sesli ders sekmesi olması, sürüm notu + dağıtım bilgisinin birleşmesi. Veri: kazanımlarda yinelenen konu 31, soru haritası 498 / çıkmış 502 farkı.
