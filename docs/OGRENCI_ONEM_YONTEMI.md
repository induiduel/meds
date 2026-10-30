# Geçmiş yıl öğrenci önem notları — yöntem, isabet ve işçi kuralları (2026-10-30)

> Kullanıcı kararı 2026-10-30: öğrencilerin en önemli bulduğu, hocanın vurguladığı, çıkmışta sorulan ya da sorulması muhtemel
> yerleri derleyen notlar **hem oluşturulmuş hem oluşturulacak** 2026-27 dersleri için tam içerik işçisinin zorunlu malzemesidir.
> Kural: AGENTS.md madde 28. Veri: `src/data/ogrenci_onem/`. Ders belgeleri: `docs/OGRENCI_ONEM/<ders>.md`. Betikler: `scripts/ogrenci_onem/`.

## 1. Kaynak

| PDF | Branş | Sayfa (A3) | Ders | Yapıştırılmış çıkmış |
|---|---|---|---|---|
| psk3.2 | Psikiyatri | 19 | 19 ders (k2-11 … k2-56) | 66 |
| nöro3.2 | Nöroloji | 13 | 10 ders (k2-01, 02, 05, 10, 17, 18, 24, 31, 32, 62) | 30 |
| tbg3.2 | Tıbbi Genetik | 5 | 5 ders (k2-08, 26, 52, 53, 59) | 9 |
| ftr3.2 | FTR | 2 | 2 ders (k2-16, 28) | 8 |

Notlar 2025-26 slaytlarından kesilmiş parçalar, iPad el yazısı, renkli vurgu ve pembe zeminli yapıştırılmış çıkmış sorulardan
oluşur. İşaret dili sayfadan sayfaya değişir (s10'da sarı alt çizgi, s11'de mavi, bazı sayfalarda pembe genel vurgu); her
sayfada okuyucu ayrıca doğruladı. Ham okuma `data/ogrenci_onem/ham/<pdf>_sNN.json` (blok = slayt parçası / çıkmış / el notu /
öğrenci özeti; `basili_metin`, `el_yazisi[{metin, hedef, guven}]`, `isaretler`, `cikmis`, `y25` sayfası, `duzeltme`).

## 2. Okuma (iki geçiş + bağımsız kontrol)

1. Sayfa 200 dpi'da 3×2 parçaya bölündü (örtüşmeli), basılı yazı için Tesseract yardımcı; **asıl kaynak görüntü**. El yazısı
   kelime kelime, tıbbi bağlamla okundu; emin olunmayan kırpılıp büyütüldü; okunamayan uydurulmadı (`guven: dusuk`).
2. Her blok 2025-26 arşiv slaytına (`meds_database_25_26/pdf/kurul2`) sayfa düzeyinde eşlendi; el yazısı oku/konumuyla bağlı
   olduğu slayt satırına (`hedef`) bağlandı. 2026-27 PDF'i olan derslerde (`k2-01/02/05/08`) bu yılın sayfası da yazıldı.
3. Yapıştırılmış her çıkmış tam yazıldı (kök + şıklar + öğrencinin işareti) ve bankada (`pastQuestions.json`) arandı.
4. İkinci geçiş: sayfa genel görünümü ve parçalar yeniden okunup atlanan blok/işaret/okuma düzeltildi. Koordinatör ayrıca
   rastgele parçaları görüntüyle karşılaştırdı (noro s11, psk s04: birebir).
5. Tıbbi tutarsızlıklar `duzeltme` alanında (ör. "santral nörojenik hipoventilasyon" → hiperventilasyon; MR nedeni olmayan
   soruda öğrencinin "Angelman" cevabı yanlış, bankada Turner; KLP sorusunda "Rancho Los Amigos" üstünü çizip "Glasgow" yazmış,
   banka cevabı "Hepsi"). Bunlar **kullanılmaz**; ders belgesinde §9 tablosundadır.

## 3. Birim, sinyal, öncelik (`scripts/ogrenci_onem/birlestir.py`)

- Birim = slayt / öğrenci özeti / el notu bloğu. Yapıştırılmış çıkmış, aynı dersin en yakın birimine bağlanır (bge-m3 ≥ 0,50).
- Bankadaki Kurul 2 çıkmışları (Psikiyatri, Nöroloji, Tıbbi Genetik, FTR; karantina dışı; OCR varyantları kosinüs ≥ 0,95 ile tekilleştirildi)
  konu adından derse, soru kökü + doğru şık birimlere eşlenir (≥ 0,60).
- Puan: çıkmış 40, bankadaki çıkmış 30 (+5/ek soru), el notu "çıkmış/sorarım" 20, yıldız 15, ünlem/tekrar 10, sarı/yeşil/pembe
  vurgu 10, el notu 8, daire/alt çizgi/kutu 5 (`ortak.AGIRLIK`).
- **A** = çıkmış kanıtı (notta yapıştırılmış ya da bankadaki çıkmış eşleşmesi) ya da puan ≥ 55 → en ayrıntılı anlatım, önem
  listesi, ≥ 2 örnek soru. **B** = puan ≥ 18 (vurgu + el notu) ya da yıldız/ünlem/"sorarım" → anlatımda açık + ≥ 1 soru.
  **C** = notta seçilmiş ama az işaretli → kapsamda kalır. Notta hiç olmayan slayt içeriği bunların altındadır.
- Puan bir **yönlendirmedir**, tıbbi kanıt değildir; kanıtsız "önemli" damgası yasağı (AGENTS 26) sürer: rozet ve vurgu
  cümlesi yalnız A/B biriminde ve birimin kanıtı (çıkmış / işaret / el notu) belgede yazılıyken kullanılır.

## 4. İsabet (başarı) ölçümü (`scripts/ogrenci_onem/basari.py`)

Soru: öğrencinin notu gerçekten sorulan yerleri yakalıyor mu? Vektör benzerliği yalnız konuyu yakalar (k2-05'te nöroanatomi
soruları muayene birimlerine 0,5 benzerlikle düşüyor). Bu yüzden bankadaki her Kurul 2 çıkmışı için bağımsız yargıç (alt ajan)
sorunun ölçtüğü belirleyici bilginin notta olup olmadığına karar verdi: **tam / kısmi / yok** ve bilginin 2025-26 slaytında
olup olmadığı. Ölçüler: isabet (tam, geniş = tam + kısmi), yapıştırılmamış sorularda isabet (gerçek öngörü), seçicilik
(notta yer alan slayt sayfası / dersin sayfası), kaldıraç (= yapıştırılmamış tam isabet / seçicilik).

**Sonuçlar (237 tekil Kurul 2 çıkmışı, 8 partide 3 bağımsız yargıç; `src/data/ogrenci_onem/basari.json`):**

| Kapsam | Soru | Tam isabet | Geniş (tam+kısmi) | Notta yapıştırılmamışta tam | Seçicilik | Kaldıraç |
|---|---|---|---|---|---|---|
| Bilgisi 2025-26 slayt metninde olan sorular | 156 | **%74** | **%94** | %64 (102 soru) | %31 | **×2,1** |
| Tüm sorular (slayt dışı / başka ders etiketli dahil) | 237 | %49 | %70 | %37 | %31 | ×1,2 |
| En yeni sınav 2025-26 (17 soru, yalnız 1'i notta yapıştırılmış → yaklaşık kör sınama) | 17 | **%71** | **%100** | %69 | %30 | ×2,3 |
| Psikiyatri (slaytta olan) | 83 | %74 | %94 | %62 | %29 | ×2,1 |
| Nöroloji (slaytta olan) | 46 | %76 | %100 | %69 | %38 | ×1,8 |
| Tıbbi Genetik (slaytta olan) | 14 | %79 | %93 | %78 | %14 | ×5,6 |
| FTR (slaytta olan) | 13 | %62 | %69 | %44 | %31 | ×1,4 |

Yorum:
- Not, slayt sayfalarının ancak üçte birini içermesine rağmen slayttan sorulan bilginin dörtte üçünü birebir, neredeyse tamamını
  kısmen yakalıyor; rastgele sayfa seçimine göre ×2 isabet. 2025-26 sınavında (notta neredeyse hiç yapıştırılmamış) sonuç aynı düzeyde
  → not geleceği öngörmede güvenilir bir yönlendiricidir.
- Tüm sorularda isabet düşer, çünkü bankanın bir kısmı slaytta olmayan bilgi (hocanın sözü, başka kaynak) ya da yanlış ders etiketidir
  (k2-05 etiketli Brodmann/serebellar çekirdek soruları, k2-26/k2-28'de slaytta olmayan kas distrofisi/SMA/inme prognozu soruları).
  Bu kısım için öğrenci notu yetmez; işçi ders belgesi §7 "notta olmayan ama sorulmuş" listesini de anlatır ve soruya çevirir.
- Notun zayıf olduğu dersler (tam isabet ≤ %35): k2-05 Nörolojik Muayene (%7; çoğu soru başka ders içeriği), k2-62 Kraniyal Sinir Muayenesi
  (%0 tam, %67 kısmi), k2-20 Psikiyatrik Tedaviler (%17), k2-26 Nörolojik Hastalıklar Genetiği (%27), k2-28 Nörolojik Hastalıklar ve
  Rehabilitasyon (%33). Bu derslerde öğrenci notu öncelik haritasının yalnız bir girdisidir; çıkmış + hoca profili ağırlığı artırılır.
- Bankada yargıçların bulduğu anahtar sorunları (düzeltilmedi, çıkmış cevap doğrulama işine eklenecek): `74bf290256d5` (Brodmann 44 → doğru
  şık "Wernicke afazisi" yazıyor; alan 44 Broca'dır), `88612c9f5ce5` ve `1ab3d959d0ec` (dil sapması: iki kaydın doğru şıkları birbiriyle çelişiyor).


## 5. Tam içerik işçisi kuralları (AGENTS 28)

1. **E0 hazırlık:** `scripts/tam_hat/hazirlik.py` → `ogrenci_onem.json` (A/B birimleri bu yılın sayfasına eşlenmiş; eşleşmeyen
   "bu yıl slaytta yok?" işaretli). Elle: `python3 scripts/ogrenci_onem/oku.py --ders <k2-xx> [--sayfalar sayfalar.json]`.
   Her yazar alt ajanın istemine bu özet + `docs/OGRENCI_ONEM/<ders>.md` bağlantısı konur.
2. **Önem listesi:** A birimleri (bu yıl slaytta varsa) önem listesinde madde olur, madde `ogrenci: {"oncelik": "A", "not": "<kanıt>"}`
   taşır (ekranda "Öğrenciler buraya çalıştı" rozeti); B birimi madde ise `oncelik: "B"`. Puan sıralamasında çıkmış kanıtlı
   madde > öğrenci A > profil önerisi.
3. **Anlatım:** A birimi ayrıntılı: tanım → ayırt edici nokta → sayı/ölçüt → karıştırılan komşu kavram; el notundaki
   açıklama ve örnek (düzeltilmiş) anlatıma girer. Süre sınırı yok (kullanıcı: ders 5–10 dk uzayabilir), dolgu yasağı sürer.
   Vurgu cümlesi: "çıkmış sınavda soruldu" yalnız doğrulanmış çıkmışta; "geçen yılın öğrencileri bu bilgiyi en önemli yerler
   arasına aldı" türü cümle derste en çok 2 kez, yalnız A biriminde. v2 cümlesi `ogrenci: {"oncelik": "A|B", "birim": "<id>"}`
   alır (ekranda rozet).
4. **Örnek soru:** A ≥ 2 (farklı kalıp), B ≥ 1; dağılım ders belgesi §2 soru payına ±10 puan; §7 "notta olmayan ama sorulmuş"
   çıkmışların bilgisi de soruya çevrilir. Notta yapıştırılmış çıkmış birebir kopyalanmaz (çıkmış ayrı katmandır), aynı bilgi
   ters yön / farklı kalıpla sorulur.
5. **Ara soru (kural 27):** ders belgesindeki "ara soru adayları" ilk adaylardır.
6. **Kaynak sadakati:** 2026-27 slaytında karşılığı olmayan birim anlatıma girmez; çıkmış kanıtlıysa önem listesine "geçen yıl
   sorulmuştu" notuyla ve örnek soruya girebilir. §9 yanlışları kullanılmaz; güveni düşük el notu tek başına dayanak olmaz.
7. **Kapı:** `python3 scripts/ogrenci_onem/kapi.py <ders> [--sayfalar …]` 0 HATA. Bilgi düzeyinde çalışır: birimin her el notu,
   vurgulu satırı ve çıkmış önermesi anlatım/önem cümlelerinde aranır (bge-m3 ≥ 0,80, ya da ≥ 0,62 + kelime kökü örtüşmesi ≥ %50;
   yalnız vektör yanıltır: "spastisite ve rijidite tonus artışıdır" cümlesi rijiditenin tanımını soran bilgiye 0,69 verir).
   A: anlatım kapsamı ≥ %60, çıkmış bilgisi anlatımda, önem listesinde ≥ 1 bilgi, ≥ 2 soru (eksik = HATA; bu yıl slaytta yoksa UYARI).
   B: anlatım ≥ %40, ≥ 1 soru (UYARI). Kapı eksik bilgileri listeler; yalnız o bilgiler eklenir (TAM_HAT_HIZLI_AKIS §3).
8. **Yeni öğrenci notu gelirse:** `data/ogrenci_onem/ham/` biçiminde okunur (yönerge: `scripts/ogrenci_onem/OKUMA_YONERGESI.md`)
   → `birlestir.py` → yargı (`basari.py --hazirla`, yargıç, `--hesapla`) → analiz (`ANALIZ_YONERGESI.md`) → `belge.py`.

## 6. Sınırlar (gizleme yok)

- Not tek öğrencinin (ya da küçük grubun) seçimidir; hocanın 2026-27 slaytı değişmiş olabilir. Bu yüzden kural 6 (bu yıl
  slaytta yoksa anlatıma girmez) ve isabet ölçümü birlikte okunur.
- Yapıştırılmış çıkmışlar notun isabetini doğal olarak yükseltir; gerçek öngörü gücü "yapıştırılmamış" sütunudur.
- Bankanın konu etiketi bazen yanlıştır (k2-05 etiketli nöroanatomi soruları; Kurul 6 yaşlılık soruları k2-34 sayfasına
  yapıştırılmış); yargıç `slaytta: false` diye ayırır, isabet paydasına girmez.
- Puan ağırlıkları elle konmuştur (kanıt sırası: çıkmış > hoca/öğrenci yıldızı > vurgu); 2026-27 Kurul 2 sınavı gelince
  `basari.py` aynı yargıyla yeniden koşulup ağırlıklar sınanır.
