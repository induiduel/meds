# Canlı çizim ve işaretleme kuralları (bütün kurullar, bütün dersler, bütün PDF'ler)

Sesli derste hoca anlatırken PDF üstünde çizilen her şeyin (ok, boyama, panel, etiket, işaretçi) kuralları. Kaynak:
kullanıcı geri bildirimleri (2026-10-24, H40–H49). Üretim `scripts/cizim/cizim_uret.py` (yerleşim betikte), kapı
`scripts/cizim/cizim_dogrula.py`, çizim `src/components/learn/pdf/CizimLayer.tsx` + `pdfDoc.css`, görüntüleyici
`PdfDocView.tsx`. Modelin (Claude) uyduğu kısa liste `scripts/cizim/TALIMAT_CIZIM.md`'dedir; bu belge ayrıntıdır.
Kural ders ya da PDF'e özgü yazılmaz; yeni geri bildirim buraya ve TALIMAT'a genel kural olarak eklenir.

## 1. Ne zaman ne çizilir

| Anlatılan | Çizim | Not |
|---|---|---|
| Resimde bir bölge (herni alanı, lezyon, kanama, yapı) | **kontur** → fosforlu boyama | yarı saydam sarı dolgu + kırmızı hat; şekil görünür kalır |
| Resimdeki bir yapıdan başka bir yapıya etki / yön | **akış oku** | yalnız resim/şema üstünde |
| Resimde zaten çizili bir ok | **odak** | kopya ok çizilmez; mevcut ok çerçevelenip etiketlenir |
| Bir kaynaktan birden çok yere | **dallı ok** | kaynak bir kez çerçevelenir, dallar ortak gövdeden sırayla |
| Grafik/eğri (EKG, kan gazı) | **eğri fazı** | eğrinin üstünde, faz renkleri |
| Yazı ↔ yazı ilişkisi (slayt maddeleri arasında) | **panel** (şema) | iki satır arasına ok çizilmez |

## 2. Panel türleri (ilişki yapısından kendiliğinden)

- **zincir** A → B → C · **grup** birden çok → bir ("}" ayracı) · **dal** bir → birden çok (karar)
- **maske** görünen neden; perde kalkınca altta aranacak · **karşıt** iki kutup yan yana
- Birbirine bağlı olmayan ilişkiler **ayrı satır**; hepsi tek "A → B" ise **hizalı tablo** (kaynak | ok | hedef).
- Kenar türleri: aktive (→), inhibe (⊣, kırmızı, belirgin uç), dönüşür (⇒), maske, karşıt; kenar etiketi ≤5 kelime.

## 2b. Anlam şablonları (dersten bağımsız kütüphane: `scripts/cizim/sablonlar.json`)

Panel, ilişkinin **tıbbi anlamına** göre bir şablona bağlanır; düzen anlamdan gelir, ders ya da PDF'ten değil.
- Yönlü etki yoksa ok yoktur: **durum → bakılacak tetkik** (`tani_tetkik`), **zehirlenme → antidot/tedavi**
  (`zehir_antidot`), **bulgu → düşündürdüğü** (`bulgu_dusundurur`), **lezyon yeri → bulgu** (`lezyon_bulgu`), **skor**
  başlıklı tablodur. ("üremik ensefalopati → istenir → üre" ya da "glukoz ⊣ hipoglisemi" yanlış okunur.)
- Gerçek neden-sonuç: `neden_sonuc` / `mekanizma_adimlari` (zincir); birçok neden → tek sonuç: `cok_neden_tek_sonuc`
  (numaralı kaynaklar + "}"); karar: `karar` (dal); sıralı yapılacaklar: `algoritma` (numaralı); alt türler: `siniflama`
  (madde imli; aynı grubun sıralı öğeleri numaralı); ayırıcı tanı: `karsilastirma`; gizleyen neden: `maskeleyen`.
- **Numara / madde:** aynı grubun sıralı ya da sayılan öğeleri numaralı; birbirinden bağımsız şeyler madde imli.
- **Kesikli ayraç:** bir panelde iki ayrı öğenin satırları ve sütunları kesikli çizgiyle ayrılır (karışmasın).
- **Yeni şablon:** uygun şablon yoksa model `yeni_sablon` önerir (kimlik, ad, genel düzen, başlıklar, ne zaman, örnek);
  kapıdan geçen öneri kütüphaneye eklenir (`eklenme.kaynak` = ders) ve sonraki derslerde kullanılır. Düzenler istemcide
  geneldir (tablo, zincir, grup, dal, karşıt, maske, liste, adımlar); yeni şablon için kod değişmez.
- **Bağımsız tıbbi anlam denetimi:** bütün paneller ve ok etiketleri, öğrencinin okuyacağı biçimde (`sablon.okunus`)
  cümleyle yan yana ikinci bir Claude geçişine verilir: tamam / düzelt (yeni şablon alanları) / sil. Sonuç önbellekte.

## 3. Panel tasarım sürümleri (en uygun olan seçilir)

Betik her panel için sürümleri öncelik sırasıyla dener ve slaytın boşluğuna **ek alan açmadan** sığan ilkini seçer:

1. yatay · normal  2. dikey · normal  3. yatay · kompakt (%85)  4. dikey · kompakt

- **Yatay zincir tek satıra sığmazsa o sürüm geçersizdir** (satıra kırılan zincirde yana bakan ok yanlış okunur) →
  dikey sürüm: düğümler alt alta, oklar **aşağı**.
- Genişlik adayları yatayda 0,5 / 0,42 / 0,6 / 0,34 / 0,3, dikeyde 0,34 / 0,42 / 0,3 / 0,5 (sayfa oranı); 0,3'ten dar yok.
- Hiçbiri sığmazsa ek alan (bölüm 5) için de aynı sürümler denenir; en az ek alan isteyen seçilir.

## 4. Boyut ve okunurluk

- Panel yazısı sayfa genişliğinin **%1,75'i** (`1.75cqw`, en az 7 px), kompakt %85; etiket **%1,9** (en az 7 px).
  Slayt büyüyüp küçüldükçe panel de aynı oranda değişir (telefonda ve masaüstünde slayta göre aynı oran).
- Betik panel yüksekliğini ekrandaki dizilimin em hesabıyla tahmin eder (`panel_boyu`, düğüm satır kırılması dahil,
  %25 pay). Doğrulama: sınama sayfasında 366 / 567 / 1100 px sayfada her panel ayrılan alana ve sayfa sınırına sığmalı.
- Düğüm kelime ortasından kırılmaz; uzun düğüm kendi hücresinde satıra iner. Etiket kırpılmaz, satıra iner.

## 5. Yerleşim: hiçbir şeyin üstü kapanmaz

- Panel/etiket kutusunda resim/yazı mürekkebi < %1 (panel) / %2 (etiket) **ve** PDF yazı satırı kutusuna değmez
  (`yazi_kesisir`, 0,01 / 0,004 pay).
- Panel anlattığı satırların yanına konur (düğüm terimlerinin geçtiği satırların merkezine en yakın boş yer).
- Etiket: önce okun yakınında boş yer → yoksa yakında, yazıya değmeyen ama resmin ≤%25'ini örten yer → yoksa sayfada
  ≤0,35 uzaklıkta boş yer. Yazının üstüne hiç konmaz.
- **Ek alan yalnız gerektiğinde ve gerektiği kadar:** panel önce slaytın kendi boşluğuna (alttaki boş bant dahil) oturur;
  sığmazsa slaytın alt boşluğundan başlar ve sayfa yalnız taşan kısım kadar uzar (`ek_alt`, `ek_renk` = slaytın alt
  kenar rengi). Sayfanın ek panelleri aynı yeri paylaşır (her panel yalnız kendi cümlesinde görünür). Sayfa kutusu ve
  işaret koordinatları değişmez; "Şu an anlatılan" çerçevesi ek alanı da sarar; gece kipinde ek alan da tersine döner.

## 5b. Etiket ve mevcut ok (H52)

- Etiket hedefinin (odak çerçevesi, boyalı bölge, ok ucu) hemen sağına/soluna/üstüne/altına konur; boşluk 0,02'den büyükse
  etiketten hedefe ince kesikli bağlantı çizilir.
- PDF'te zaten çizili ok (vektör aday ya da a→b boyunca çizili hat) yeniden çizilmez; çerçevelenip etiketlenir.

## 6. Görünürlük ve anlam

- Her çizgi beyaz hale üstünde 2,4 px tam opak. Ok etiketsiz çizilmez. Okun başlangıcı (kaynak kutusu ya da halkalı
  nokta) ve hedefi (yazı/kutu çerçevesi) belli. Resim sayfasında hedef, çizili kutunun kendisi.
- Ok rotası sayfanın boşluğuna göre: düz (yatay/dikey), dirsek (dikey→yatay) ya da kavis; içeriğin üstünden en az geçen.

## 7. Zamanlama

- Çizim, çizilen şeyin adı konuşulurken başlar (`bas`/`son` terimin geçtiği kelimeye kaydırılır); konuşmayla yumuşak ve
  sürekli uzar, düğümler sırayla belirir.
- Anlatılan satır oynatıcının altında kalmaz: görüntüleyici gerekirse yetecek kadar kaydırır (sayfa geçişi bitince
  yeniden dener; bu kaydırma kullanıcı gezinmesi sayılmaz, takip durmaz). Kelime takipçisi harfleri kapatmaz (hafif zemin +
  harflerin altında ince çizgi).

## 7b. Pekiştiren animasyonlar (eğitsel; süs değil)

- **Odak merceği:** resimde bölge (kontur) anlatılırken slaytın geri kalanı hafifçe kararır (%22), bölge açık ve boyalı kalır.
- **Şu an anlatılan:** tablo satırı, liste öğesi ve zincir düğümü belirdiği anda sarı zeminle öne çıkar; panel tamamlanınca
  vurgu kalkar (öncekiler sakin).
- **Neden-sonuç akışı:** zincir/grup oklarında küçük parçacık nedenden sonuca akar (yönü sezdirir); tablo eşleşmelerinde
  (yönsüz ilişki) parçacık yoktur.
- Hareket azaltma tercihinde (prefers-reduced-motion) hepsi kapanır.
- Sıradaki fikirler: karşıtlık tablosunda farklı hücre vurgusu, skor toplamında sayaç, ders sonunda panelleri "hatırla" kartı.

## 7c. Yakınlaşma (H53)

- Resim üstündeki çizimde (resim sayfası ya da resim kutusu içinde; bölge sayfanın %40'ından küçük) betik yakınlaşma
  bölgesi yazar (`yakin`: çizim + etiket sınırı, %6 pay). Görüntüleyici cümlenin ilk resim çizimi başlarken tuval/metin/işaret
  katmanlarını o bölgeye yumuşakça büyütür (bölge ortaya gelir, ≤2,4×, sayfa kenarı açığa çıkmaz), çizimler büyütülmüş
  görünümde akar, sonuncusu bitince 1,6 sn sonra geri döner. Bir cümlede birden çok çizim varsa birleşik bölge tek hedeftir
  (gidip gelmez). Sayfa kutusu, kaydırma ve sayfa takibi değişmez; hareket azaltma tercihinde kapalı.

## 8. Ekran

- **İzleme düzeni:** ders oynarken metinde yalnız anlatılan paragraf ve onun ekran maddeleri tam görünür, diğerleri
  soluk ve madde kutuları kapalı; "Metin + Slayt"ta slayt varsayılan %60.
- Görüntüleyici kaydırması kare kare yapılır (tarayıcının yumuşak kaydırması bu kapsayıcıda durabiliyordu); kare
  çizilmeyen ortamda süre dolunca hedefe doğrudan gider. Anlatılan satırın görünürlüğü ekrandaki gerçek konumundan ölçülür.

- Dar PDF bölmesinde araç çubuğu düğmeleri kırılmaz (ölçüt bölme genişliği, container query).
- Telefonda görünüm seçici (Metin / Metin + Slayt / Slayt) başlık satırında tek döngü düğmesidir.

## 8b. Resim slaytı ve yatay zincir (H51)

- Slaytın asıl içeriği görselse (≥%35 resim kutusu ya da metin katmanı olmayan dolu taranmış sayfa) panel kurulmaz; ilişki
  görselin üstünde çizilir (boyama, ok, odak). Kapı (`resim_sayfasi`) paneli reddeder.
- Yatay zincirde her kutu tek satırdır; sığmıyorsa sürüm geçersizdir ve dikey (oklar aşağı) çizilir.
- Maske şablonu: "İlk izlenim" → ⚠ maskeleyebilir ↓ → "Atlanmaması gereken" (bulanıktan netleşir).

## 9. Sınama (her yeni ders ya da yerleşim değişikliğinde)

**Otomatik kapı:** `node scripts/cizim/panel_sinama.mjs <ders>` — gerçek bileşen + stil, başsız Chrome, 366/567/1100 px;
taşma, iç taşma, ayrılan yükseklik aşımı, yatay zincirde kırılma, kelime ortasından kırılma, kesik yazı, panel içi üst üste
binme, 7 px altı yazı. Ders zinciri (`cizim` adımı) çalıştırır; düşerse `CIZIM_PAY=1.4` ile bir kez yeniden yerleştirir,
yine düşerse çizim yayına gönderilmez (çıkış 14).


1. `cizim_uret.py` → kapı 0 HATA. 2. Sınama sayfası (gerçek `CizimLayer` + `pdfDoc.css`): bütün paneller 366 / 567 /
   1100 px'te — ayrılan alan aşımı, sayfa/ek alan taşması, kırık yatay zincir, kesik etiket = 0. 3. Canlıda denetleyici
   (2× hız, telefon + masaüstü): panel/etiketin yazı kutusuyla kesişmesi, anlatılan satırın oynatıcı altında ≥1 sn kalması.
