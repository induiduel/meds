# Soru çözücü — 2. tur: yeni benzer sorular + çıkmış sorular (alt ajan talimatı)

Çalışma klasörü: `/home/indu/medsor/meds_temp/patoloji_ornek26/cozucu/`. Önce `TALIMAT.md`'yi baştan sona oku: açıklama alanları
(`kok_ses`, `secenek_ses`, `ipucu`, `siklar`, `cozum`, `sayfa`), çift biçim (`metin`/`ses`), öğrenciye dönük dil ve uzunluk kuralları
AYNEN geçerli. Bu belge yalnız farkları ve yeni işi anlatır. **Ses yazımında aşağıdaki "Kısaltma okunuşu" bölümü TALIMAT.md'deki
eski örneklerin (ör. "her iki", "anka") yerine geçer.**

Girdi: `girdi2/<kod>.json` →
- `mevcut`: dersin hâlihazırdaki örnek soruları (kök + doğru cevap). Yeni sorular bunlardan FARKLI olmalı (aynı bilgiyi başka kelimeyle sorma).
- `yeni_soru_sayisi`: yazacağın yeni soru sayısı (TAM bu kadar).
- `onem`: dersin sınav potansiyeli en yüksek maddeleri (puan, sınav adayı sırası `aday`, bilgi, PDF sayfaları). Yeni soruları önce
  `aday` dolu ve puanı 90+ maddelerden, sonra 80+, sonra 70+ maddelerden kur; bir maddeden en çok 2 soru; mevcut soruların zaten
  sorduğu bilgiyi tekrar sorma.
- `cikmis_adaylari`: konuyla eşleşmiş geçmiş sınav soruları (id, sinav, kok, secenekler, dogru).
- PDF metni: `/home/indu/medsor/meds_temp/patoloji_onem/pdf_metin/<kod>.md` — tek kaynak. Baştan sona oku.

## A) Yeni benzer sorular (`yeni`)
- Hocanın 2026-27 örnek sorularıyla AYNI üslup ve biçim: kısa tek cümlelik kök (en çok 1–2 cümlelik kısa senaryo olabilir), 5 şık A–E,
  şıklar KISA (1–6 kelime), tek doğru cevap, çeldiriciler aynı kategoriden ve makul.
- **Zorluk orta-zor:** ezber tanıma değil; ayırıcı nokta, mekanizma, "en sık / en erken / en önemli", "hangisi beklenmez / yanlıştır",
  iki yakın kavramı ayırma, sebep–sonuç. Her soruda en az 2 güçlü çeldirici (derste öğretilen komşu kavramlar).
- Sınav kuralı: tablo/şekil okumaya dayalı soru YOK; klinik bulgu (semptom/muayene) sorusu YOK; prognoz ve tedavi sorulabilir.
- Her bilgi PDF'te açıkça geçmeli; doğru cevap PDF'e göre tartışmasız tek doğru olmalı. Eşanlamlı iki şık olmamalı (ör. "Tip IV" ve
  "Gecikmiş tip" aynı soruda olmaz). "Hangisi yanlıştır/değildir" kökünde yanlış olan tek şık olmalı.
- Doğru cevap harflerini A–E arasında dengeli dağıt (hiçbir harf %35'i geçmesin).
- Ek alanlar: `onem_id` (dayandığı madde id'si), `zorluk` ("orta" | "zor"; en az yarısı "zor").

## B) Çıkmış sorular (`cikmis`)
- `cikmis_adaylari`ndan **en çok 5** soru seç (aday azsa hepsi uygunsa hepsi). Seçilenler birbirinden FARKLI bilgiyi sormalı
  (aynı sorunun farklı yıl tekrarı ya da aynı bilgiyi soran ikinci soru alınmaz) ve mevcut/yeni sorularla aynı bilgiyi sormamaya özen
  göster. Önce sınav potansiyeli en yüksek konudakiler.
- `soru`, `secenekler`, `dogru` adaydaki gibi BİREBİR kopyalanır (yazım hatası bile düzeltilmez; yalnız baş/son boşluk). `id` ve `sinav`
  aynen yazılır.
- Anahtarı PDF'e göre doğrula. PDF anahtarla çelişiyorsa ya da soru PDF'in kapsamı dışındaysa o soruyu ALMA; `elenen_cikmis`
  listesine `{id, neden}` yaz. Görsel/şekil gerektiren soru alma.
- Açıklamalar (ipucu, siklar, cozum) yine yalnız PDF'e dayanır. "Hangisi yanlıştır" sorularında doğru şıkkın açıklaması: ifadenin
  neden yanlış olduğu + "bu yüzden doğru cevaptır"; diğer şıklarda ifadenin neden doğru olduğu (yani cevap olmadığı).
- Şıklar uzun cümle olabilir; `secenek_ses` şıkkın ses biçimidir (aynı içerik).

## Kısaltma okunuşu (ses alanları) — KESİN
Seslendirme motoru birleşik yazılan harf dizisini kelime gibi okuyor; bu YANLIŞ. Kısaltmalar **harf harf**, her harf Türkçe adıyla,
**boşlukla ayrık** yazılır:
- Harf adları: A a, B be, C ce, Ç çe, D de, E e, F fe, G ge, H ha, I ı, İ i, J je, K ka, L le, M me, N ne, O o, Ö ö, P pe, R re,
  S se, Ş şe, T te, U u, Ü ü, V ve, Y ye, Z ze, Q ku, W çift ve, X iks.
- Örnekler: DNA → "de ne a", RNA → "re ne a", HPV → "ha pe ve", ATP → "a te pe", CD4 → "ce de dört", TP53 → "te pe elli üç",
  BRCA1 → "be re ce a bir", IgG → "i ge ge", PSA → "pe se a", ACTH → "a ce te ha", ADH → "a de ha", VHL → "ve ha le",
  MHC → "me ha ce", ANCA → "a ne ce a", GBM → "ge be me", TNF → "te ne fe", IL-1 → "i le bir", PDGF → "pe de ge fe",
  VEGF → "ve e ge fe", ER/PR → "e re ve pe re", CIN → "ce i ne", PAS → "pe a se", HIV → "ha i ve", HIF → "ha i fe".
- Yalnız şu yerleşik okunuşlar kelime gibi kalır: HER2 → "her tu", HELLP → "help", AIDS → "eyds", TORCH → "torç", gen adları
  RAS → "ras", MYC → "mik", KIT → "kit", MET → "met", BRAF → "be raf", PARP → "parp", NOTCH → "noç", WNT → "vint", SMAD → "smad".
  Bunların dışında kısaltmayı birleştirme, kelime gibi okutma ("anka", "denea", "atepe" YASAK).
- Türkçe açılımı yerleşik ve kısaysa açılımı da kullanabilirsin (DCIS → "duktal karsinoma in situ", SLE → "sistemik lupus
  eritematozus"), ama cevabı ele verecekse kullanma.
- Yunan harfi: TNF-α → "te ne fe alfa", IFN-γ → "interferon gama".

## Çıktı — `cikti2/<kod>.json`
```json
{"kod": "02",
 "yeni": [{"onem_id": "02-07", "zorluk": "zor", "soru": "…", "secenekler": {"A": "…", …}, "dogru": "B",
           "kok_ses": "…", "secenek_ses": {…}, "ipucu": {…}, "siklar": {…}, "cozum": {…}, "sayfa": [n]}],
 "cikmis": [{"id": "04efaa244730", "sinav": "2020-2021 · …", "soru": "…", "secenekler": {…}, "dogru": "C",
             "kok_ses": "…", "secenek_ses": {…}, "ipucu": {…}, "siklar": {…}, "cozum": {…}, "sayfa": [n]}],
 "elenen_cikmis": [{"id": "…", "neden": "…"}]}
```
Bitiş: `python3 dogrula2.py cikti2/<kod>.json` → 0 HATA (UYARI'ları da incele). Yalnız `cikti2/<kod>.json` yaz; geçici dosyalar
`/tmp/claude-1000/cozucu2_<grup>/`. Yerel GPU/LLM yok. Son mesajında ders başına: yeni soru sayısı (zor/orta), seçilen çıkmışlar
(id), elenen çıkmışlar ve nedenleri, emin olmadığın okunuşlar.
