# Patoloji hocasının soru mantığı — Kurul 1 2026-27 derin analiz (v2, 2026-10-29)

> Amaç: Kurul 2+ patoloji vurgu, örnek soru ve "çıkabilecek soru" üretimini hocanın gerçek seçim mantığına bağlamak.
> Bu not **kanıt düzeyini açıkça** yazar; zayıf kanıtlı kalıbı kesin kural gibi uygulamak YASAK.
> Soru-soru eşleme: `docs/PATOLOJI_SORU_ESLEME_TABLOSU.md`. İşçi: `scripts/patoloji_soru_isci/` (TALIMAT.md).
> v1'den farklar: slayt biçimi yeniden yorumlandı (sarı = yapı etiketi), "ters yön" ve "birleştirme/kopya" dönüşümleri bulundu,
> 30 sorunun her biri için kaynak slayt bulundu (4 ajan, biçim işaretli döküm).

## 0. Veri ve sınırlar
- Sınav: `data/cikmis_2627/kurul1_2627.json`, Patoloji soru 35–68. **58, 62, 65, 66 hiç toplanmadı**; 9 sorunun şıkları öğrenci
  hafızasından kısmen tamamlanmış (`siklar_uretildi`: yalnız kök + doğru şık güvenilir). 21 soru `tam`. Örneklem küçüktür (n=30).
- Slayt: 35 PDF (`drive_root/Kurul 1/Tıbbi Patoloji`; 27, 29, 36–38 numaralı dersler Patoloji PDF'i olarak yok). Biçim işaretli döküm:
  `scripts/patoloji_soru_isci/dokum.py` (⟦kırmızı⟧ ‹kalın› `Y|` sarı dolgu `#` başlık).
- Karşılaştırma tabanı: 546 eski patoloji çıkmışı (2018–2026). Eski çıkmış taraması **anahtar sözcüklüdür**; "eski yıllarda yok" demek kesin değil.

## 1. Sorular nereden geldi (30/30 kaynak bulundu)
- **25/30 slaytın gövde madde satırı**, 3/30 başlık altı özet/sınıflama listesi, 1 tablo, 1 ad parantezi. **Slayt başlığından hiç soru çıkmadı**; hoca
  başlığın *altındaki* cümleyi sorar.
- **5/30 (35, 37, 39, 50, 61) slayt dışı bir adım içeriyor:** doğru şık slayt bilgisine bir *çıkarım* ekliyor ("ksilol kullanılmadan tespit", "Hayflick
  sınırı", "DNA hasarı → kanser", yanlış şıkta uydurma mutlak ifade "tamamen engellenir"). Yani hoca ~%15–20 oranında slayt cümlesini bir
  mantık basamağı ileri taşır; salt ezber yetmez, **ilişkiyi kurmak** gerekir.
- **Genişlik:** 26 derse ~1'er soru; yalnız Hücresel Yaşlanma, Hücre Hasarı II, Genetik-Pediatrik-Çevresel, Tümör Biyolojisi'nden 2. Eski yıllarda
  yığılan dersler (Aşırı Duyarlılık 50, Prostat 36, Meme Kanseri 27) bu yıl 1'er soru. **Her dersten en az bir soru beklenir.**
- Toplanmayan 4 sorunun muhtemel yerleri: sınav ders sırasını izliyor; soru verisi olmayan dersler: Hücre İçi Birikimler, Karsinojenez, İleri Tümör
  Genetiği, Tümör İmmünolojisi, Evreleme, Vasküler/Kistik Böbrek, Gebelik, Meme Benign, İnvaziv Serviks. **Bunlar kör nokta**: soru olasılığı yüksek.

## 2. Slayt biçimi — yeniden yorumlama (v1'deki "sarı önemli değil" yanlış okumaydı)
Ölçüm (35 PDF, 33.197 satır): **kırmızı satırların %42'si**, **sarı dolgulu satırların %31'i** (11.254), kalın %7.
- **Sarı dolgu içeriği değil yapıyı işaretler:** sarı satırların **%72'si kısa etiket** (≤4 kelime ya da ":" ile biten: "Sonuç:", "Ancak:", "İstisna:",
  "Örnek:", "Not:", "Çözünmezse", konu başlığı). Yani sarı = "bundan sonra bir karşıt dal / sonuç / istisna geliyor" levhası. **Soru çoğu zaman sarı
  etiketin ALTINDAKİ satırdan çıkar** (38 "Ancak:" altı; 40 "Sonuç: Çözünmezse"; 36 "İstisna:"; 37 "Hücresel sonuç:"; 53 "Not:"; 59 "Moleküler sınıflama").
- **Kırmızı** her yerde (%42); tek başına ayırt edici değil. Kırmızısız kaynaklar da çıktı (55: düz satır; 59: kalın+sarı).
- **Kalın** nadir (%7) ve **güçlü ek sinyal**: kaynak satırları arasında kalın içeren pay belirgin yüksek (38 "Neoplazi", 39 "ölümsüz", 56 Kimmelstiel, 57, 59 alt tipler;
  ≈6/30, el sayımı). **Kırmızı+kalın birlikte** ya da **kırmızı+kalın+sarı** aynı satırda = en yüksek öncelik (38: üçü birden).
- **Açık hoca işareti:** `***` ("***Bilateralite önemli ipucu", 64) → soru oldu. Slaytta `***`/"önemli", büyük harf ("YOK", 68), "ipucu" sözcüğü → neredeyse kesin.
- **Tekrar sinyali (güçlü):** aynı bilgi gövdede + şekil altı yazısında / iki slaytta / iki derste geçiyorsa soru oluyor: Cowdry A (60), bazal hücre tabakası (68, üç kez),
  tür/eponim başlık özeti (42: üçlü özet 3 sayfada). **Bir bilgi ≥2 yerde geçiyorsa öncelik ver.**
- Başlık satırı (≥24 pt): hiçbir sorunun kaynağı değil.

## 3. Hocanın üç dönüşüm yöntemi (30 sorunun dağılımı, yaklaşık)
1. **Kopya + küçük çevirme (≈8):** doğru şık slayt cümlesinin neredeyse kelimesi kelimesine kopyası (38, 42, 43, 47, 53, 55, 59, 61-şıklar). Çeldirici =
   aynı cümlenin **mutlaklaştırılmış ya da tek kelimesi ters çevrilmiş** hâli ("her zaman", "hiçbir zaman", "tamamen engellenir", "sadece").
2. **Birleştirme (≈10):** aynı slayttaki 2–3 ardışık madde (44 fibrozis+hemosiderin; 43 granülasyon+skar+kontraksiyon; 55 dört bulgu), ya da **iki ayrı slayt**
   (45 türbülans örneği + Virchow bileşeni; 52 BAX/BAK→geçirgenlik→sitokrom c→kaspaz, iki sayfadan), ya da **kural + istisna** (36 koagülatif ↔ beyin likefaksiyon).
   Çeldirici: karşıt kategorinin maddesi (primer ↔ sekonder yara; çocuk ↔ erişkin kurşun bulgusu; nefrotik ↔ nefritik).
3. **Yön/ad değiştirme (≈9):** eski çıkmışta sorulan bilgi **ters yönde** gelir: "Cowdry A hangi etkende?" → "HSV'de en tipik bulgu" (60); "BPH'de olmayan" →
   "adenokarsinomu ayıran özellik" (68); "atipi hangi özelliği" → "sınıflama atipili/atipisiz" (63); "bilateral olma ihtimali düşük" → "bilateral müsinöz → Krukenberg" (64);
   olgu → eponim (46 Waterhouse–Friderichsen, 56 Kimmelstiel–Wilson). **Hoca yeni bilgi aramıyor, bilinen bilgiyi başka yönden soruyor.**
   - Eski çıkmışla ilişki: 36, 45, 47, 49, 50, 52, 56, 60, 61, 63, 64, 67, 68 aynı bilgiyi/konuyu daha önce sormuş (anahtar sözcük taramasıyla).
     Yani **çıkmış sorular hâlâ en güçlü ipucu**, ama aynı kökle değil, **yönü çevrilmiş** biçimiyle gelir.

## 4. Hangi bilgi türü? (30)
Ayırıcı bulgu 6 · klinik korelasyon 6 · eşleşme (tablo/çapraz) 4 · sonuç 3 · en tipik 3 · mekanizma sırası 2 · tanım 2 · eponim 2 · sınıflama 2. **Sayı/eşik sorusu yok.**
Yapısal kalıplar: "İstisna/Ancak/Sonuç/Not" etiketli dal (36, 38, 40, 53) · "X tipleri/iki ana form/üç alt tip" listesi (59, 63) · sendrom adı → tümör/bulgu
kümesi (51, 55) · akut↔kronik ikili sayfasının kronik tarafı (44) · hastalığın son/ince morfoloji maddesi (54 tübül) · slaytta tek parantezde geçen ad (46).

## 5. Soru kalıbı (v1 tablosu geçerli, n küçük)
Şık uzunluğu 3,9 → 5,8 kelime; bileşik şık %14 → %40; "en tipik/en olası/en doğru" kökü %12 → %45; olumsuz kök %28 → %10 (ama 50 ve 61 "yanlıştır"); kök kısa (12 kelime).
"Doğru şık en uzun" %85 olarak ölçüldü ama hatırlama yanlılığı olabilir; yine de kural: **doğru şıkkı en uzun yazma**.

## 6. Çeldirici mantığı
Yanlış şık rastgele değil: (a) **aynı dersin komşu kategorisinin doğru maddesi** (43 primer, 47 tip I/II/III, 49 çocuk bulgusu, 55 nefrotik, 54 kresent/lineer IgG);
(b) **doğru cümlenin mutlaklaştırılmış tersi** (53, 61); (c) **komşu dersin sınıflaması** (63: LSIL/HSIL, seröz/berrak hücreli); (d) **önceki yılın doğru önermesi**
(50: apoptoz "yanlış olan"da eski doğru ifadeler çeldirici); (e) bileşenlerin yer değiştirmesi (36, 41, 45, 52). Dışarıdan uydurma çeldirici yok.

## 7. İşçiye bağlanan kurallar
1. **Önem puanı:** kırmızı+kalın+sarı üstü üste (+), `***`/"önemli ipucu"/büyük harf (+++), **≥2 yerde tekrar** (++), sarı etiketin ("Ancak/İstisna/Sonuç/Not/Çözünmezse")
   altındaki satır (++), tek geçen ad/eponim (++), "X tipleri/alt tip" listesi (+), tablo satırı eşleşmesi (+). Tek başına kırmızı, tek başına sarı, başlık: puan yok.
2. **Her önem noktasına ≥2 soru, farklı dönüşümde** (`dogrudan`, `bilesik`, `eslesme`, `sira`, `olumsuz`, `ters_ad`, **`ters_yon`** = aynı bilgiyi eski çıkmış yönünün tersinden,
   **`yanlis_bul`**). Mümkünse biri birleştirme, biri ters yön.
3. **Çıkmış soru varsa** o bilgi için ters yönlü soru zorunlu (hocanın yaptığı bu).
4. Ders başına çekirdek 3–5 nokta + **her derse en az 2 soru** (genişlik).
5. Çıkarım adımı: noktaların ~%15–20'sinde slayt cümlesinden bir mantık adımı ileri soru (yine PDF'te dayanağı olmalı; kaynak dışı bilgi yasağı sürer).
6. Çeldirici §6'daki 5 türden; yalnız aynı dersin komşu kavramı; kaynak sayfa yazılır.
7. Doğru şık en uzun olmaz; bileşik şık %30–50; "en tipik/en olası" kökü %30–55; olumsuz kök ≤%15.

## 8. Güncelleme
Kurul 2 patoloji hocası (Prof. Dr. Hikmet Keleş) aynı kişi olmayabilir. İlk Kurul 2 çıkmışı gelince `profil.json` ve bu belge yeniden hesaplanır; ayrışırsa Kurul 2 profili ayrılır.
58/62/65/66 numaralı soruların metni toplanırsa tablo güncellenir.
