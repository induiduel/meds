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
