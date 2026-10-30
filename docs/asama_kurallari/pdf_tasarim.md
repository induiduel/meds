# Aşama kuralları — pdf_tasarim

> ÜRETİLMİŞ DOSYA: elle yazma. Kaynak `docs/KURUL2_YAPILMAYACAK_HATALAR.md`, üreteç `scripts/tam_hat/kural_secici.py`. 43 madde. Ayrıntı gerekirse madde başlığıyla defterde aç.

### Sesli ders PDF/DOCX dışa aktarımı (2026-10-20)
- **Yazıyla sayı:** konuşma metni okunuş için "iki virgül bir", "yüzde kırkına" yazar; öğrenciye verilen dosyada bunlar
  "2,1", "%40'ına" olmalı. Kural tek yerde: `src/services/sayiYazim.ts` (`sayilariYaz`), dışa aktarım
  (`components/canliDers/canliDersDisaAktar.ts`) ve ekran (`canliDersStore.ts` → `sayilariDuzelt`, vurgu konumları `sayilariYazEslemeli` ile taşınır) her derste uygular. Saklanan metin değiştirilmez (ses ve cümle zamanı ona bağlı).
- **Düz madde yığını yok:** paragraf tek madde olarak basılmaz; ilk cümle ana madde, sonrakiler alt madde, "Yani/Örneğin…"
  ve "2 ölçütü ayırın" gibi duyurulardan sonra gelenler ikinci düzey; kısa noktasız satır alt başlık olur.

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

### H46 — Telefonda panel yazısı okunmayacak kadar küçüktü; panel kelime kenarına biniyordu; ek alan şişiyordu (2026-10-24)
- Kullanıcının telefon görüntüleri eski önbellekli sürümdendi (ek alan yok, sabit px yazı). Güncel sürümde telefonda panel
  yazısı 5 px kalıyordu → %2,2 cqw. Boşluk eşiği %3 mürekkep bir kelimenin kenarını kaçırıyordu → %1 + 0,012 pay.
  Bir sayfanın ek panelleri üst üste diziliyordu (ek alan sayfanın 1,24 katı) → aynı yeri paylaşır, tam genişlik.
  Grup/dal tahmini uzun düğüm kırılmasını saymıyordu → `panel_boyu` sütun genişliği + satır sayısı.
- Sınama: 35 panel 366 / 567 / 1100 px sayfada ölçüldü (taşma 0); gerçek uygulamada 420 px telefon görünümünde s.11.

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

### H56 — Yeni yayınlanan dersin PDF'i uygulamada açılmıyordu (2026-10-24, kullanıcı, k2-07)
- Deste → PDF eşlemesi (`build_deck_pdf_sources.py` → `meds_downloads/_deck_pdf_sources.json`) yalnız işçinin Drive
  taramasında (50 dk) yenileniyordu; k2-07 21:47'de yayınlandı, eşleme 21:14'tendi → ders PDF'siz. PDF sunucu diskinden
  verilir (`/api/lecture-pdf/deck/<deste>/<n>`); Drive yalnız sunucusuz yedek yoldur.
- Düzeltme: `yayinla.py` yeni ders yayınlayınca `_pdf_eslesme_yenile()` → işçi kapsayıcısında `izle.pdf_eslesme_guncelle()`
  (günlükte "PDF eşleşmesi: yenilendi"). Kapı: yayından sonra `/api/lecture-pdf/deck/<deste>/0` 200 dönmeli.
- `.medspak` öğrenci paketi PDF taşımaz (tasarım: `ek` yalnız `--ekler` yönetici dışa aktarımında); uygulama PDF'i paketten değil sunucudan açar.

### H61 — Üst Üste Çakışan ve İç İçe Geçen Çizgi/Kontur Hatası (2026-10-25/26, kullanıcı)
- **Çözüm & Kural:**
  1. Cümle bazlı çizim izolasyonu ile C0 bittiğinde "dekortike postür" kalkar, C1 başladığında "kollar fleksiyonda" gelir; asla aynı anda görünmezler.
  2. Tek bir cümlede veya aynı görsel üzerinde eşzamanlı çakışan/iç içe geçen koordinatlar YASAKTIR. Çizim kapısı (`cizim_kapisi.py`) çakışan konturları denetler.


### H80 — Öğrenci Drive betiği uzantısız PDF'i not saymadı; kısaltma bulucu "HT+DM" yazımını kaçırdı (2026-10-27)
- **Çözüm / kural:** Tür MIME'den de belirlenir; bölme deseni `[/\-–+]`; EP `kisaltma_bilinen.json`'a eklendi.
  `degerlendirme_dogrula.py` slayttaki her kısaltmanın sözlükte olmasını HATA ile ister.


### H86 — Sınav planı Kurul 2'de boş sayfa (2026-10-27)
- **Çözüm:** boş durum iletisi ("Kurul N için sınav dağılımı henüz girilmedi"). Kurul 2 dağılımı girilince plan kendiliğinden kurulur.
- **Önleme kuralı:** kurula bağlı veriyle çizilen her ekran, veri yokken `null` değil nedenini söyleyen boş durum gösterir;
  yeni kurul açılırken `sinav_dagilimi.json`'a o kurulun dağılımı eklenir.


### H88 — Drive klasör adı değişince yayın PDF'in kaynak kimliğini bulamadı (2026-10-27, k2-03)
- **Çözüm / kural:** sunucu ve deneme kipi `kaynak_kimligi_esnek` kullanır; esnek eşleme klasör farkını yok sayıp `Kurul N/<branş>/`
  sonrası yol manifestte tekse onu kabul eder. Yayın denetim hatasında taslağın `yayin.json`'u silinip yeniden onaylanır.


### H87 — v15 katmanlarında tanımsız renk/yazı değişkenleri: saydam kartlar, varsayılan yazı tipi (2026-10-27)
- **Çözüm:** `styles/v15/tokens.css`'e takma adlar (gerçek jetonlara bağlı).
- **Önleme kuralı:** yeni CSS'te renk/yazı değişkeni yazmadan önce `getComputedStyle(document.documentElement)` ile ya da
  palettes.ts/tokens.css'te var olduğu doğrulanır; yeni ad uydurulmaz.


### H91 — Çizim PDF'i önbellekte olmayınca bütün konturlar sessizce reddedildi (2026-10-27, k2-03/k2-04)
- **Çözüm:** ikisine de aynı yedek yol (indirme klasörü → `pdf_isaret.pdf_indir`); `cizim_uret` PDF hiç bulunamazsa durur.
- **Önleme kuralı:** bir hattaki bütün betikler kaynak dosyayı aynı yardımcıyla bulur; ret sayacında tek bir nedenin tüm komutları
  ataması (ör. "görüntü yok" = kontur sayısı) kapı hatası sayılır, yayına geçilmez.


### H92 — Bilinen kısaltma sözlüğü bağlamsız: MSS "Muskuloskeletal sistem" diye açıldı (2026-10-27, k2-03/k2-04)
- **Çözüm:** derse özel `data/sesli_anlatim/kisaltma_elle/<key>.json` (`MSS: Merkezi sinir sistemi`), elle eşleme bilinenden önce gelir.
- **Önleme kuralı:** her derste kısaltma listesi (kısaltma = açılım) yazdırılıp slayt metniyle okunur; branşa göre anlamı değişen
  kısaltma (MSS, KB, BOS …) için derse özel eşleme yazılır, genel sözlüğe yeni anlam eklenmez.


### H95 — Yayın düzeltmesinde olmayan alan; PDF eşleyici durdurulan işçi kapsayıcısında (2026-10-27, k2-03/k2-04)
- **Çözüm:** `y.b.get("ders_id")`; PDF eşleme tek seferlik `docker run --rm -u 1001:1001 --entrypoint python3 medsoru-isci:latest`
  (aynı bağlar, LLM anahtarı yok) ile; deste PDF'i 200 doğrulandı.
- **Önleme kuralı:** yayın betiği değişikliği Oracle'a gitmeden önce yerel taslakla `kaynak_kimligi_esnek` ve `--deneme` akışı
  çalıştırılır; yayından sonra `/api/lecture-pdf/deck/<deck>/0` 200 kontrolü zorunlu.


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


### H113 · KMB video oynatıcısı takılıyor, yazılar üst üste biniyor (2026-10-27)
- **Kalıcı çözüm:** Klip bütünüyle blob olarak önceden indirilir (`sesOnYukle`, sonraki adımınki de); bekleme sonrası yakın konumdaysa ses
  konumlanmadan sürer, yalnız 0,6 sn üstü sapmada (bellekten, anında) konumlanır; küçük sapma yumuşak düzeltilir, ses tamponlanırken görüntü
  bekler. Başlık kartı kaldırıldı, geçiş 250 ms. `kmb.css` tek katman olarak yeniden yazıldı: normal kipte denetimler sahnenin ALTINDA tek
  satır, altyazı sahne içinde tek kutu; tam ekranda denetim yüzer, altyazı onun üstüne çıkar; aynı anda görünen etiketler birbirinden itilir.
- **Kural:** Sesle eşlenen animasyonda ses ağdan parça parça konumlanmaz (blob/önbellek); saat sert değil yumuşak eşlenir. Stil dosyasına
  "vN: önceki kuralları ez" katmanı eklenmez — kural yerinde değiştirilir; üst üste binen öge eklerken mutlak konumlu her katmanın yeri tek yerde tanımlanır.


### H118 · Anlamsız karşılaştırma tabloları (Öge / Sınıf / Gerekçe) (2026-10-27)
- **Çözüm:** swipe_matching tablo dışı bırakıldı; venn/feature_bidding yalnız ≥3 satır, her gerekçe ≥7 kelime ve benzersizse alınır.
- **Kural:** Karşılaştırma yalnız iki GERÇEK tıbbi kavramı (hastalık, yapı, ilaç, mekanizma) ayırt eder; "X mi Y başlığı mı" gibi meta sınıflama, tek cümlelik özdeş gerekçe, bozuk Türkçe yasak. Yazar parçalarında da yazılmaz; yazar/denetçi bunu kontrol eder.
- PDF/yazdırma: belge yalıtılmış iframe'de yazdırılır; uygulama DOM'unda yazdırma ve sayfa yüksekliğine eşit sabit yükseklik YASAK (boş sayfa/renk karışması).


### H108 · Tablo rozetleri harf harf dikey; Ders seçenekleri kartları uzayıp taşıyordu (2026-10-28)
- **Çözüm:** eski kural `svg.di15-ik` ile kapsandı, rozete `white-space: nowrap; flex: none`. Menüde alt liste/düzen `grid-column: 1 / -1`, ızgara `align-items: start`.
- **Kural:** Yeni CSS sınıfı eklemeden önce aynı adın kullanılmadığını grep'le; kısa ortak adlara (`-ik`, `-ad`) element/üst seçici kapsamı ver. `display: contents` ile çözülen sarmalayıcının açılır alt parçaları tam satır olmalı.


### H123 · Tam içerik hattı ders başına 4–6 saat sürüyor, soru/metin/PDF hataları geri dönüş yaratıyordu (2026-10-28)
- **Kural:** `docs/TAM_HAT_HIZLI_AKIS.md` — E0 `hazirlik.py` (döküm GPU ≤2500 MHz, AGENTS §10 altıncı istisna); alt ajana yalnız
  `kural_secici.py --oku <aşama>`; yalnız hatalı parça yeniden yazılır (sayısal hedefte ±%10, kalite hatasında tolerans yok);
  ders başına tek denetçi.
- **Kapı — EKLENDİ:** `scripts/tam_hat/soru_uslup.py` (ders çağrıştıran kök, ipuçlu uzun doğru şık, kazanım bağı, kalıp payı),
  `kaynak_kapisi.py` (kayıt içeriği `s` sayfasında mı), `pdf_tarama.py` (boş sayfa, taşma, üst üste, harf harf kırılma).


### H124 · Soru çözücüde Kurul 2 seçili görünürken Kurul 1 dersleri listeleniyordu (2026-10-28)
- **Çözüm:** çözücü ve En önemliler başlangıcı `useSeciliKurul()` kullanır (vurgulanan kurul = listelenen kurul), "Tümü" kaldırıldı, ad önekindeki "Kurul N" atılır, başlanmış dersler önde sıralanır. Olası sorular şeridi `.ks.kseridi` olarak kapsamlandı.
- **Kural:** seçili durum gösteren bir bileşen ile içeriği süzen kod AYNI kaynaktan (aynı kanca) okur; görsel vurgu için ayrı varsayılan hesaplanmaz. Ortak bileşenlerin sınıf önekleri (`.ks`, `.kh`) başka sayfa CSS'inde kapsamsız kullanılmaz.


### H110 · Çıkmış sorular yıl çipi 21, listede 20 soru (2026-10-28)
- **Çözüm:** çip sayımı aynı `facetPass` + arama ile; yalnız çipin kendi boyutu (yıl çipinde `year`, ders çipinde `discipline`) hariç tutulur (yönlü süzgeç kuralı). Sınama: 12 yıl çipinin toplamı 502 = liste; 2023-2024 çipi 26 → liste 26.
- **Kural:** Süzgeç çipi/rozetindeki sayı, o çip seçilince listenin göstereceği sayıyla aynı yoldan (aynı süzgeç zinciri) hesaplanır; ayrı, eksik bir sayım yazılmaz.


### H111c · Esc uygulama tam ekranından çıkarmıyordu (2026-10-28, ortak kabuk)
- **Çözüm:** `src/utils/fullscreen.ts` › `installEscExit` — tek genel `keydown` (bubble, `defaultPrevented`/yazı alanı/açık pencere-menü/sayfa içi tam ekran katmanı/`tam-katman`/`cd-tam-ekran` varken dokunmaz) sınıfı kaldırır ve `medsor:fullscreenchange` yayar. Tarayıcıda sınandı: aç → Esc → kapandı, düğme "Tam ekran"a döndü.
- **Kural:** Native tam ekranın yedeği olan her CSS kipi kendi Esc çıkışını taşır; Esc önce açık pencereye/katmana aittir.


### H111d · Yönetim betik kataloğu her açılışta ana pakete iniyordu (2026-10-28, başarım)
- **Çözüm:** `getScriptsList` kataloğu `await import('../data/bundledScripts')` ile yalnız çağrıldığında yükler. Ölçüm: index.html'in indirdiği JS+CSS 2.747 KB → 2.719 KB (102 → 91 dosya). (`manualChunks` ile `deckStore`'u ayırma denendi: rolldown ortak bağımlılıkları o parçaya çekip 443 KB'lık yeni bir ilk yük parçası üretti → geri alındı; `manualChunks` ile paylaşılan modül ayırmak YASAK, statik içe aktarmayı kaldır.)
- **Kural:** Ortak istemci/servis dosyaları (api.ts, auth, realtimeEvents) yalnız tek ekranın kullandığı büyük veri/katalog modüllerini statik içe aktarmaz; dinamik `import()` kullanılır.


### H111g · İzleme hızı kaydırıcısı: dokunma hedefleri 10–19 px, boş durumda imleç metinle çelişiyordu (2026-10-28, Sınav planı/Bitirdiklerim)
- **Çözüm:** boş durumda imleç 1×; ray `padding: 9px 0` + `background-clip: content-box` (görünüş aynı, 28 px dokunma), duraklara `::before` ile 40 px dikey alan + `min-width: 40px`. Bugün akışındaki "Tümü" bağlantısı (14 px) negatif kenar boşluklu 40 px alana alındı (`today.css .t15-more`). Takvim, kronometre ve tam ekran ayarlarındaki `kre-tgl` anahtarlarına `aria-label` eklendi (adsız düğme).
- **Kural:** Görünür öğe küçük olabilir ama dokunma alanı ≥40 px (dolgu/`::before`); yer tutucu değer ile açıklama metni aynı varsayımı göstermeli; her `role="switch"` düğmesinin erişilebilir adı olur (label içi olmak yetmez).


### H111h · PC'de açıklama metinleri 120–160 karakter satır uzunluğunda (2026-10-28, okunabilirlik)
- **Çözüm:** `takip.css` `.sp-acikla/.ss-acik` 14 px + 72ch, `.sp-nasil ul` 75ch (özet 40 px), `cevrimdisi.css .cv-not` 14 px + 72ch, `saglik.css` kaynakça 90ch, `topluluk.css .tp15-kural` 75ch.
- **Kural:** Gövde/açıklama metni ≥14 px ve satır ≤ ~75ch; geniş kartın içindeki paragraf `max-width` ile sınırlanır.


### H111q · Sesli ders telefonda: başlık 75 px'e sıkışıyor, Kalem düğmesi eziliyor, bölme hızlı düğmeleri 23×21 px (2026-10-28, Ders çalış)
- **Çözüm:** `styles/v15/sesli.css` telefonda başlık iki satıra sarılır (16 px, line-clamp 2); `.cd15-pb { flex: none; min-width: 32px }`; `@container (max-width: 460px)` dosya adı gizli. `canli-ders.css` `(pointer: coarse)` hızlı düğmeler 36×36.
- **Kural:** Esnek şeritteki simge/düğmeler `flex: none` alır, yalnız metin öğesi küçülür; metin öğesi 40 px altına inecekse gizlenir ya da sarılır.


### H111s · Zihin haritası numaraları koyu temada okunmuyordu (2026-10-28, Ders çalış)
- **Çözüm:** `zihin.css` `:root.theme-dark .zh15-no { color: oklch(0.84 0.09 var(--t)) }`.
- **Kural:** Sabit `oklch()/hex` yazı rengi yalnız token zeminiyle birlikte koyu tema karşılığı yazılarak kullanılır.


### H111t · Ders çalış dokunma hedefleri: "Tüm dersler" 75×14, Öğren "▶ Dinle" 52×20 px (2026-10-28, Ders çalış)
- **Çözüm:** `dersler.css .d15-more` 40 px dolgu + negatif kenar (H111g ile aynı desen); `LessonPlayer.tsx` düğmeye `ls-dinle` sınıfı, `v12/lesson.css` dokunmatikte `::before` ile 40 px alan.
- **Kural:** H111g kuralı: görünür öğe küçük kalabilir, dokunma alanı ≥40 px.


### H111v · Ana CSS 936 KB, tam katman sayaçsız, tam ekranda fazla yükseklik, kısa başlık, küçük yazı, çevrimdışı boş istekler (2026-10-28, kabuk/başarım)
- **Çözüm:** (1) `src/styles/ogren-ders.css` (index.css'in iki `ls-*` bölümü) yalnız ls-* çizen 13 bileşenden içe aktarılır; ana CSS 936,8 → 865,7 KB (151,2 → 139,9 KB gzip); hesaplanmış stil dökümü önce/sonra (375/1440, deste + 3 ders adımı) 0 fark. `html.ui-v3` ls katmanı, health/v12 ezmeleri yüksek özgüllükte olduğundan ana CSS'te kaldı. (2) `src/utils/tamKatman.ts` (`useTamKatman`, referans sayaçlı); beş bileşen ona geçti. (3) v15 tam ekranda (`:not(.cd-ders-acik)`) `--sh-top-h` ve `--sh-top-vis` = 44 px + güvenli alan; `.sh-main` artık tam görünüm yüksekliği. (4) Telefonda `.v15-top-h` iki satıra sarar (17 px, line-clamp 2); sesli derste Tam ekran düğmesi telefonda gizli (Görünüm çekmecesinde var); `v15-crumb::before` ile ≥40 px dokunma alanı. (5) `--v15-t-caption` 13 → 13,5 px; v15 stillerinde 95 font değeri (10–12 px, <.78rem) 12,5 px'e çekildi. (6) `net.ts` `cevrimdisiMi()` + fetch koruyucusunda arka plan uçları (`presence`, `user-data/backup`, `music/playlist`) çevrimdışıyken ağa çıkmadan reddedilir; `presence.ts` ve `UpdatePrompt` `/api/surum` denetimi çevrimdışıyken atlanır (bağlantı yoklaması `baglanti.ts`/probe `/api/surum`'u kullanmaya devam eder).
- **Kural:** Sayfaya özgü büyük stil bloğu `index.css`/`main.tsx`'e eklenmez, kullanan bileşenden içe aktarılır (sıra/özgüllük hesaplanmış stil dökümüyle doğrulanır). Kök sınıfı birden çok bileşen açıyorsa sayaçlı yardımcıdan geçer. Tam ekranda gizlenen çubuğun yerine dolgu konuyorsa ilgili yükseklik değişkeni de o dolguyu yansıtır. v15'te metin ≥12,5 px; istisnalar yalnız rozet/sayaç/kbd/kronometre mini saati/yazdırma belgesi (`dersPdf.css`)/ray etiketi. Arka plan eşitleme ucu ekleyen `net.ts` `BG_RE`'ye ekler.


### H131 — Yönetim öğrenci uygulamasının ortak girişiyle açılıyordu; ayrı giriş + SW önbellek zehirlenmesi riski (2026-10-28, Yönetim v16)
- **Kalıcı çözüm:** `manage.html` + `src/manage-main.tsx` (yalnız adminFetchAuth, Firebase kimlik, palettes.ts tokenları, `styles/yonetim-temel.css`, kit, kabuk). `vite.config.ts` çoklu giriş; `server.ts` SPA geri dönüşü `/manage*` için `dist/manage.html`; geliştirmede `scripts/vite/yonetimGirisi.ts`. Yönetici değilse (moderatör) ya da `?kabuk=v14` ise `manage-main` tam uygulamayı (`import('./main')`) yükler. Uygulama içinden /manage'e geçiş (`App.tsx yonetimGirisineGec`) tam sayfa gezinmesi yapar (10 sn döngü koruması). Ölçüm: /manage 544+152 KB → 179+5 KB gzip; tarayıcıda 191 KB aktarım, FCP 164 ms.

### H133 — Kaynağı doğrulanamayan sorular gizlenerek kaybedilmişti; "Çıkmış–Örnek" sınıfı (2026-10-28)
- **Çözüm:** 4 bağımsız denetçi 104 soruyu müfredat + ders notu + tekrar taramasıyla değerlendirdi: 72 `cikmis_ornek` (hem Çıkmışlar'da hem `k2-cikmis-ornek` Örnek sorular dersinde, öğrenciye "çıkmış olduğu doğrulanmadı" rozetiyle; sesli ders çıkmış chip'inden hariç), 15 serbest çıkmış, 9 tekrar arşivi, 7 karantinada (`siniflama` alanıyla gerekçeli). 5 soru ders notuna göre düzeltildi (`duzeltmeOnceki` saklı).
- **Önleme:** Kaynağı doğrulanamayan ama doğru soru gizlenmez, `kaynakSinifi=cikmis_ornek` ile etiketlenip öğrenciye belirtilir; çıkmış vurgusu yalnız doğrulanmış kaynağa dayanır.


### H154–H169 — Sayfa denetimi dördüncü tur, öğrenci sitesi orta bulguları (2026-10-28)
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

### H170–H185 — Sayfa denetimi dördüncü tur, yönetim paneli orta bulguları (2026-10-28)
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

### H200–H212 — Sayfa denetimi beşinci tur, öğrenci sitesi kalan bulgular (2026-10-28)
- **H200/H201/H205/H210 Sınava hazırlan:** boş "Planlama" başlığı yalnız içerik varken; sınav ağırlığı kartı nereye gittiğini söylüyor; olası sorular kartı ATP kilidini önceden yazıyor; telefonda sekme şeridi kenarda solar.
- **H202/H203 Soru haritası:** yılı belirsiz "?" sütunu renk ölçeğine katılıp en koyu hücreleri alıyordu → "Yılsız", sona alındı, ölçek dışı; telefonda yana kaydırma ipucu. Kural: belirsiz/eksik kategori renk ölçeğini belirlemez.
- **H204** Çıkmış arama yer tutucusu telefonda kesikti → anahtar sözcük önde.
- **H206/H207 Sesli ders:** küçült düğmesi `::after` ile ~44 px; bölme hap düğmeleri ≥28 px + aria-label.
- **H208** Hastalık dipnotları `::after` dokunma alanı.
- **H209 Çift başlık:** v15'te sayfa adı hem üst çubukta hem `PageHeader` h1'de görünüyordu → v15'te PageHeader başlığı görsel olarak gizli (ekran okuyucu için h1 kalır). Site geneli kural; yeni sayfa başlığı v15'te üst çubuktan gelir.
- **H211/H212 Sağlık:** açıklamasız sayı rozetleri dipnot biçiminde ("[14]"); "15 yıl" → "15 yıllık geçmiş".

### H320–H329 — Görünürlük beş ayrı yerden düzenleniyordu (2026-10-28, sayfa denetimi; kullanıcı isteği)
- **Çözüm/kural:** Görünürlük YALNIZ Site › Görünürlük'te yazılır: "Sayfalar" (öğrenci sayfaları + menü) ve "İçerik" (kurul, ders, sesli, deste, paket, önem/asistan/çözücü; yeni uç `GET /api/admin/gorunurluk/icerik`, sayfalı, süzgeçli, katalogda olmayan ayar `sahipsiz`). Diğer sayfalarda `GorunurlukBaglantisi` (rozet + "Değiştir" → `site/gorunurluk?sekme=icerik&q=<anahtar>`). `site/menu` → Görünürlük. Gizleme onay + hedef, her yazım 8 sn Geri al, toplu değiştirme. Yerelde tıklanarak sınandı (tek + toplu, geri al sonrası ayar boş).


### H330–H334 — Sesli ders araç çubukları kalabalıktı (2026-10-28, sayfa denetimi; kullanıcı isteği)
- **Çözüm/kural:** Görünür kalanlar ders boyunca sık dokunulanlar: görünüm kipi, tam ekran (masaüstü), Çıkmış, Kalem, yakınlaştırma (masaüstü). Seyrekler `CdTasmaMenu` ⋯ menüsünde: yazı boyutu (menü açık kalır, değer yazar), yıldızlı paragraflar, terim yardımcısı (✓; açıkken çubukta etkin göstergesi), görünüm ayarları, tüm ders seçenekleri, tam ekran; PDF ⋯: sayfa teması, yakınlaştır/uzaklaştır/sığdır. Menü erişilebilir (aria-haspopup, ↑/↓/Home/End, Esc/dışarı/Tab kapatır, odak düğmeye döner), kısayollar değişmedi, tanıtım turu yeni hedeflere bağlandı (9/8 durak). Çizim/zamanlama mantığına dokunulmadı (kural 17/18). Açık: TV kipinde menü ok tuşları TV katmanına takılabilir; telefonda Kalem 33 px, küçült düğmesi 36×22 px.
- **Kural:** Sesli ders ekranına yeni düğme eklenirken önce sık/seyrek kararı verilir; seyrekse ⋯ menüsüne girer, durum taşıyorsa menüde ✓ ve çubukta etkin göstergesi olur.


### H388/H389 — Sınıf adı çakışması: Ders çalış çip şeridi ortaya/sağa kayıyordu (2026-10-28, kullanıcı bildirdi)
- **Çözüm:** `kisi.css` öneki `apr15`, Bitirdiklerim öneki `btr15`. Canlıda Arkadaşlar → Ders çalış geçişiyle önce/sonra ölçüldü (seçici sol boşluğu 427 px → 0).
- **Kural:** Her v15 ekranının kök sınıf öneki sitede tektir; yeni önek seçmeden önce `grep -rn "\.<önek>\b" src/styles` ile denetlenir (bu oturumda yazılan tarama: aynı kök sınıfı iki dosyada tanımlayan stil yok olmalı). Stil "yalnız bazı gezinme sıralarından sonra" bozuluyorsa önce sınıf çakışması aranır.


### H432 — Ders PDF ekranı kaydırırken "parçalanıp geri geliyordu" (2026-10-28, kullanıcı bildirdi)
- **Çözüm/kural:** Çerçeve ekran boyunda, belge içinde kayar; dar ekranda belge çerçeve genişliğine `zoom` ile sığar, yazdırmadan önce ölçek kalkar (afterprint ile geri gelir). Ölçüm: telefonda çerçeve 358×642, ölçek 0,358, yatay taşma 0; masaüstünde 1010×694. Önizleme/gömülü belge iframe'i içerik boyuna büyütülmez.


### H439 — Üst çubuk arka plan göstergesi stilsiz çiziliyordu (v15, 2026-10-29)
- **Çözüm/önleme:** `ap15g` kuralları (+ kendi `@keyframes ap15g-don`, kart çerçevesi/zemini, `v15-label`) kabukla birlikte yüklenen `styles/v15/shell.css`'e taşındı. Kural: kabukta (ShellV15) her sayfada çizilen bileşenin stili sayfa CSS'ine değil `shell.css`/`tokens.css`'e yazılır; bir bileşenin sınıfları yalnız onu içe aktaran (ya da kabuğun) CSS dosyasında yaşar.


### H442 — Yeni sayfanın CSS öneki başka bileşenle çakıştı; sekmeler dev daire, düzen tek sütun (soru dışa aktarıcı, 2026-10-30)
- **Çözüm:** önek `sx15` yapıldı (CSS + bileşen).
- **Önleme:** yeni v15 sayfası/bileşeni için önek seçmeden önce `grep -rn "\.<önek>[ {.:-]" src/styles src/components` ile boş olduğu doğrulanır; kısa (3–4 harf) önekler çakışmaya en açık olanlardır.

