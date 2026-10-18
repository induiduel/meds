# Şık Açıklama Standardı — "Yardım al", yanlış şık ve çözüm açıklamaları (ZORUNLU)

> Kullanıcı kararı, 2026-10-18. Kurul 2'den itibaren Drive'a gelen her yeni PDF'ten **tam otomatik** üretilecek içeriğin
> (interaktif ders, sesli spot / sınav asistanı, sesli soru çözücü — EMA seslendirmesiyle) şık açıklamaları bu standarda uyar.
> Otomatik hatta insan denetimi olmayacağı için kalite kapısı doğrulayıcıdadır: standardı karşılamayan çıktı **yayına giremez**.

## Neden

Sınav asistanında (Patoloji 08, IL-17 sorusu) "Yardım al" şu metinleri gösterdi:

- "IL-13 nötrofil toplayıcı olarak geçmez."
- "IL-10 nötrofil alımı yapmaz."
- "IL-2 bu sorunun cevabı değil."

Bunlar öğrenciye hiçbir şey öğretmez: IL-13'ün, IL-10'un, IL-2'nin **ne olduğunu, ne işe yaradığını** söylemez; yalnız
"bu değil" der. Kullanıcının ifadesiyle: *"kısa geçiştirici ifadeler ile kimseye fayda sağlamaz."*

Kök neden: talimatlarda "TEK kısa cümle, 5–20 kelime" kuralı ve "kavram PDF'te yoksa 'bu sorunun cevabı değil' de" kaçış
yolu; doğrulayıcı da yalnız uzunluk üst sınırını ölçüyordu.

## Kural: her şık için üç bilgi

"Yardım al" **her şıkkı (doğru dahil)** şu üç soruya cevap vererek açıklar:

1. **Ne?** — Şıktaki kavramın kimliği: nereden/hangi hücreden çıkar, hangi gruba/sınıfa girer, nasıl bir yapıdır.
2. **Ne işe yarar / ne yapar?** — Temel işlevi, etkisi, tipik bulgusu ya da klinikte nerede karşımıza çıktığı.
3. **Bu soruyla bağı** — Sorunun sorduğu özelliğe neden uyuyor (doğru şık) ya da neden uymuyor; öğrencinin onu neyle
   karıştırabileceği.

Örnek (aynı soru, kabul edilen biçim):

- **IL-13:** Th2 hücrelerinden salınan bir sitokindir; alerjik yanıtta ve alternatif makrofaj aktivasyonunda rol oynar.
  Nötrofil toplamaz, Th2 tipi (alerjik/onarım) yanıtın sitokinidir; pürülan iltihapla ilgisi yoktur.
- **IL-17:** Th17 hücrelerinden salınır; nötrofil ve monositleri iltihap bölgesine toplar. Akut iltihabın nötrofilden zengin,
  pürülan yanıtını bu yüzden IL-17 yürütür — doğru cevap.

> [!IMPORTANT]
> "Bu sorunun cevabı değil", "cevap değil", "… olarak geçmez", "… arasında yer almaz", "… yapmaz." gibi **yalnız olumsuzlayan**
> cümleler tek başına açıklama sayılmaz. Olumsuz cümle ancak 1. ve 2. madde (ne olduğu + ne yaptığı) verildikten sonra gelebilir.

## Biçim

- `yardim[harf]`: **2–3 cümle, 20–55 kelime** (metin). Ses biçimi aynı anlam, aynı kurallar (kısaltma harf adıyla, rakam yazıyla).
- `yanlis[harf]` / `siklar[harf]`: aynı üç bilgi + "Doğrusu: …"; 2–4 cümle, 20–65 kelime.
- En az bir cümle olumlu kimlik/işlev cümlesi olmalı (olumsuzlama içermeyen).
- Her şıkkın açıklaması o şıkka özgüdür; şıklar arası kalıp tekrar yok.
- Harf anılmaz ("A şıkkı" yok); iç süreç dili ("PDF'te", "kaynakta", "aday", "talimat") yok.

## Kaynak sırası (bilgi nereden alınır)

1. Aynı dersin PDF'i / slayt metni.
2. Aynı kurulun diğer ders PDF'leri ve ders notları (`meds_database_v2/ders_notlari_k*/`), çıkmış soru açıklamaları.
3. Kavram müfredatta hiç yoksa: **örnek soru üretiliyorsa o şık çeldirici olarak kullanılmaz** (müfredattaki komşu kavramla
   değiştirilir). Çıkmış soruda (şık değiştirilemez) ise kavramın standart ders kitabı düzeyindeki kimliği ve işlevi tek cümleyle
   verilir; bağımsız denetçi geçişi bu cümleyi doğrular.
   *(Açık karar: 3. adımdaki ders kitabı düzeyi açıklama kullanıcı tarafından onaylanmayı bekliyor — bkz. DEGISIKLIK_KAYDI 2026-10-18.)*

## Kalite kapısı

- Asistan doğrulayıcıları (`meds/scripts/spot_cozucu/asistan_dogrula.py`, `meds/scripts/patoloji_onem/asistan_dogrula.py`)
  `yardim` için alt sınır, boş kalıp yasağı ve olumlu cümle şartını **HATA** olarak denetler.
- Çözücü doğrulayıcıları (`cozucu_dogrula*.py`) `siklar` / `yanlis` için aynı kalıp yasağını denetler.
- Yazar + bağımsız denetçi iki geçişi korunur; denetçi her şıkta "Ne? / Ne işe yarar? / Bu soruyla bağı" üçlüsünü tek tek arar.
- Otomatik hatta (Kurul 2 Drive → içerik) doğrulayıcı 0 HATA vermeden seslendirmeye (EMA) ve yayına geçilmez.

## Mevcut veri borcu (2026-10-18 ölçümü)

`meds/src/data/*_asistan` "Yardım al" girdilerinin ~%98'i 18 kelimeden kısa (≈8.700 / 8.900); boş kalıp içeren şık
açıklaması: asistan `yardim` 259, asistan `yanlis` ~710, çözücü `siklar/yanlis` ~840 (en çok Patoloji ve Enfeksiyon).
Bu içerik yeniden üretilip yeniden seslendirilene kadar yeni doğrulayıcı eski çıktılarda HATA verir — bu beklenen durumdur.
