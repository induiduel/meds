# Hocanın soracağı yerleri tahmin rehberi (sürüm v6; her test turunda genel kurallarla iyileştirilir)

> Kullanım: tam içerik işçisi ve kör test ajanları. Girdi: `not.md` (ders metni) + `profil.md` + `adaylar.md`. Çıktı: ders başına `profil.md` başında yazan **K tahmin** (10–18; ders uzunluğuyla orantılı).
> Yalnız GENEL kurallar içerir. Ölçüm: tek çalışmada ders başına 8 tahmin soruların ~%45'ini, 24 tahmin ~%70'ini yakalıyor → **kapsama** (geniş, çeşitli liste) ana hedeftir.

## 1. Hoca bir bilgiyi neden sorar
(a) ayırt edici özellik · (b) mekanizma halkası · (c) tanımlayıcı/tanı koydurucu bulgu · (d) tanım-sınıflama-ad · (e) **ilaç imzası** (ilaç → ayırt edici yan etki / endikasyon / izlem organı / gebelikte durum) · (f) sayı-oran-eşik-süre-doz · (g) klinik/halk sağlığı kararı (ilk basamak, ne zaman başlanır/eklenir/YAPILMAZ) · (h) **liste üyeliği**.

## 2. Olumsuz kökün gizli hedefi: LİSTE ve SINIF
"… değildir / yanlıştır / risk faktörü değildir / örneği değildir" köklerinde cevap listenin DIŞINDAKİ elemandır. Çözmek için listenin TÜM üyeleri bilinmeli. Bu yüzden:
- Her sınıflama/liste/gruplama bloğu (≥4 madde: örnekler, risk faktörleri, türler, yöntemler, hastalık grupları, koruyucu/zararlı etkenler) için bir tahmin yaz: olgu = "sınıf adı: üyeler" (en çok 8 üye; fazlaysa komşu listeyle karışabilenleri seç) ve gerekirse "X bu listeye girmez/başka listeye aittir".
- Her **koruyucu/zararlı etken listesinde** hem olumlu hem olumsuz üyeleri ayrı yaz (örn. "risk artıran" ve "azaltan").
- Liste tahmini sayısı: en çok K/3 (10–18 tahminde 3–6). Aynı tablo hem liste hem eşleştirme olabilir; **tek tahmin say**, kalıbı bilgi doğasına göre seç.

## 3. İlaç imzası, yöntem sınıfı, kural/eşik
- İlaç: tabloda her ilaç satırı için tek imza ("ilaç → imza"). Gebelikte yasak olan, izlem gerektiren, ayırt edici yan etkisi olan ilaçlar öncelikli.
- Yöntem/test listeleri: hangisi kesin tanı / invaziv / biyofizik / tarama gibi **sınıf ayrımı**.
- Kural-eşik: ne zaman başlanır/eklenir/yapılmaz; süre, doz, eşik, "her hastaya … verilmez" gibi **yanlış uygulama** cümleleri. Sayı olgunun parçasıdır. Birleşik şema (tedavi şeması) tek tahmin sayılır.

## 4. Kesin tanımlar
- **`satir`** (kesin): olgunun yazılı olduğu TEK satır. Tabloda o bilginin geçtiği veri satırı (başlık değil; birkaç satırı birleştiren eşleştirmede ilk veri satırı). Liste bloğunda bloğun İLK ÜYE satırı. Aynı bilgi spot ve gövdede ise gövde; ama çıkmış sorunun bilgisi yalnız spot satırında geçiyorsa o spot satırı. Birleşik olguda (fenotip+karyotip, aşı şeması) ilk bilginin geçtiği satır; olgu tek satıra aitse o satır. `adaylar.md`'deki `s<N>` ve `satir` numaraları `not.md` satır numarasıdır.
- **`olgu`**: kaynaktaki bilgiyi (kısaltarak/birleştirerek) tek bilgi cümlesi; liste ise §2. Kaynakta olmayan bilgi ekleme.
- **`bilgi_turu`** (kapalı küme): mekanizma · tani_ayirici · tanimlayici_bulgu · ilac_yan_etki · ilac_endikasyon · etiyoloji_risk · siniflama_ad · epidemiyoloji_sayi · onleme_halk_sagligi · prognoz_komplikasyon · tanim_kavram · diger. Sayısal olgu: `kalip: sayi` + `epidemiyoloji_sayi` (veya konuya uyan tür). Tablo başına en çok bir birleşik tahmin yazılır; alt tip başına ayırt edici özellik ise alt tip başına birer `en_tipik` yazılabilir.
- **`kalip`**: olumsuz/yanlis_bul (liste/istisna/kural) · en_tipik (tek ayırt edici) · dogrudan (tanım/ad/imza) · dogru_ifade (üç-dört ifadeden doğru olan) · sayi · onculu (3–4 parçalı kural) · vaka · eslestirme (tablo). Çatışırsa bilginin doğası belirler, profil payı değil.
- **Profil (tek kural)**: `profil.md`'de iki pay bloğu var: genel ders profili ve "bu konuya en yakın 40 çıkmış" (yerel). Güven YÜKSEK ise ders profilini, ORTA ise kotanın yarısını ders profiline yarısını yerel bloğa ver, DÜŞÜK ise yerel bloğu esas al; iki blok çelişirse konuya özgü olan yerel blok ağır basar; baskın türleri **kotaya çevir** (pay %p → yaklaşık K×p; en az 1; kaynakta yoksa serbest okumaya devret). Yakın çıkmış örnek listesi yalnız güven yüksekse okunur.
- **Çıkmış ters yön**: yalnız `not.md` içindeki "Çıkmış Sorular" bölümü için; bölüm yoksa atla. Ters yön = çıkmış sorunun doğru şıkkının olumlu cümleye çevrilmesi VE yanlış-bul köklerinde her şıkkın (doğru üyeler) ayrı bilgi noktası olarak yazılması; aynı soru tekrarı değil. Çıkmış bölümü olan derste kotanın en çok ~1/4'ü, en az 1 tahmin buraya ayrılır (tek soruluk bölümde 1–2); çıkmış seçenekleri kaynakta yoksa çözüm notundaki bilgi ters yön sayılır. Çıkmış ters yönü liste kotasının (K/3) içinde sayılmaz. Çeldirici şıkların ilaç/sınıf bilgisi ayrı nokta sayılabilir.

## 5. Adım adım
1. `profil.md` (K sayısı + baskın türler; yakın çıkmış listesi yalnız güven yüksekse).
2. `not.md`'yi baştan sona tara; öğrenim hedeflerinin fiillerine bak (ayırt etmek, sıralamak, karşılaştırmak, sınıflamak) → önce bu hedeflere tahmin.
3. `adaylar.md`: A genel, B liste blokları, C ilaç, D kural/eşik. Boş sınıfın kotası serbest okumaya geçer.
4. **Kota önceliği (tek sıra; çatışmada üstteki kazanır)**: (1) ayırt etme/sınıflama hedefleri, (2) liste blokları (en çok min(K/3, 4)), (3) ilaç imzası + kural/eşik, (4) çıkmış ters yönü, (5) profilin baskın türü, (6) bölüm çeşitliliği (kalan boşluğu doldurur).
5. Her tahmin için kendine sor: "Bu bilgiyi bilen ile bilmeyen öğrenciyi 5 şıkta ayıran ne?" Cevap yoksa tahmini at.
6. Yazım: `neden` alanına dayanak (aday sınıfı / hedef fiili / çıkmış ters yön / tablo) yaz.

- Ders tamamen farmakolojiyse kota: mekanizma ~%35, endikasyon ~%25, yan etki ~%15, sınıflama/ad ~%10, sayı/eşik ~%10 (profil bunu ezmez, yalnız dengeler).
- Sayı yoğun derslerde `sayi`+`eslestirme` toplamı K'nin yarısını geçmez.


## 6. Yapma
- Giriş/tanım cümlelerini sırf başta diye seçme; tüm tahmini tek bölümden seçme; aynı bilgiyi iki kez yazma; kanıtsız "önemli" deme.

## 7. Sürüm notları
- v7 denendi ve GERİ ALINDI (tur 10–11: geliştirme %82,4 ama bekletilmiş %65; v6 ortalama %78, v7 %73,7 — gürültü içinde ama yarar kanıtlanmadı).
- v6 (tur 7 ajan geri bildirimi): kapalı bilgi_turu listesi, orta güven kuralı, liste tavanı tekleştirme, spot/gövde ve birleşik olguda satır, tek soruluk çıkmış ters yön, farmakoloji kotası.
- v5 (tur 5, bekletilmiş küme): satır/liste/profil/ters-yön/kota kuralları tekleştirildi.
- v2: liste/ilaç/kural sınıfları. v3: kesin tanımlar, kompakt adaylar, gürültü temizliği. v4 (tur 4): K=10–18 (kapsama), liste kuralı (koruyucu/zararlı üyeler, ≤4), profil→kota dönüşümü, boş sınıf kotası devri, `diger`, `dogru_ifade`, birleşik şema tek tahmin, "5 şıkta ayıran ne?" testi.
