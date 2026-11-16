# Patoloji Sesli Soru Çözücü — soru denetimi + açıklama + ses metni (alt ajan talimatı)

> ⚠️ **Şık açıklama standardı (ZORUNLU, 2026-10-18):** her şık açıklaması kavramın ne olduğunu, ne işe yaradığını ve bu soruyla
> bağını anlatır; "bu sorunun cevabı değil / … olarak geçmez" gibi geçiştirme HATA'dır. Ayrıntı ve kaynak sırası: `meds/docs/SIK_ACIKLAMA_STANDARDI.md`.
> ⚠️ **Türkçe üslup standardı (ZORUNLU, 2026-10-18):** metin doğal, eksiksiz ve anlaşılır Türkçe olur; çeviri mecaz ("imzası",
> "motoru", "freni") ve iç etiket ("Ayrım cümlesi:", "Akılda tut:", "Mantığı şudur:") YASAK. Ayrıntı: `meds/docs/TURKCE_USLUP_STANDARDI.md`.

Çalışma klasörü: `/home/indu/medsor/meds_temp/patoloji_ornek26/cozucu/`

Öğrenci tam ekran bir "soru çözücü" ile 2026-27 patoloji örnek sorularını çözer. Anlatım YOK, yalnız soru. Asistan (EMA, Türkçe kadın
sesi; metin harfi harfine okunur) soruyu ve şıkları okur. Öğrenci şık seçer ya da yardım düğmelerine basar:
- **İpucu** → `ipucu` okunur (cevabı söylemeden düşündürür).
- **Bir yanlışı ele** → rastgele bir yanlış şık vurgulanır, `siklar[harf]` okunur, şık elenir.
- **Çözümü dinle** → şıklar A'dan E'ye tek tek vurgulanıp `siklar[harf]` okunur, sonra "Doğru cevap X, <şık>." + `cozum` okunur.
- Yanlış şık seçerse "Yanlış." + o şıkkın `siklar` açıklaması; doğruyu seçerse "Doğru!" + `cozum`.
Bu yüzden her `siklar` açıklaması **tek başına** anlaşılır olmalı (önce/sonra ne çalınacağını varsaymaz).

Girdi: `../cikti/<kod>.json` (soru listesi: no, konu, soru, secenekler A–E, dogru, aciklama, sayfa) ve ders PDF metni
`/home/indu/medsor/meds_temp/patoloji_onem/pdf_metin/<kod>.md` (`=== SAYFA n ===` ayraçlı). Sorulardaki `aciklama`/`sayfa` yol
göstericidir ama yanlış olabilir — her şeyi PDF metninden doğrula.

## Kesin kurallar
1. **Tek kaynak ders PDF'i.** Açıklamalardaki her tıbbi bilgi PDF metninde geçmeli (aynı ya da açıkça eşdeğer ifade). Kitap/genel bilgi
   ekleme, sayı uydurma. Bir çeldirici kavram PDF'te hiç yoksa bilgi UYDURMA; aynı kurulun diğer dersleri/ders notlarından kavramın ne olduğunu ver (`meds/docs/SIK_ACIKLAMA_STANDARDI.md`), ayrıca
   PDF'teki doğru bilgiyi öğret (sorunun sorduğu özelliğin gerçekte neye ait olduğunu söyle).
2. **Önce soruyu denetle (hatasızlık).** Her soru için PDF'te:
   - Doğru cevap gerçekten doğru mu, PDF'te açıkça destekleniyor mu?
   - Başka bir şık da PDF'e göre doğru sayılabilir mi (iki doğru)? Kök belirsiz ya da yanıltıcı mı? Şıkta yazım/terim hatası var mı?
   - Sorun yoksa `kontrol: {"durum": "tamam"}` ve `soru`/`secenekler`/`dogru` alanlarını kaynaktaki gibi BİREBİR kopyala.
   - Sorun varsa en küçük düzeltmeyi yap (kökü netleştir, hatalı şıkkı aynı kategoriden başka bir makul çeldiriciyle değiştir ya da
     anahtarı düzelt) ve `kontrol: {"durum": "duzeltildi", "not": "neyi neden değiştirdin, PDF s. n"}` yaz. Sorunun konusunu değiştirme.
3. **Öğrenciye dönük dil:** "PDF", "kaynak", "slayt", "ders notu", "talimat", "ipucu", "çeldirici", "şık" ("şık" yalnız ses dışı metinde
   değil — hiç kullanma; asistan harfleri kendisi söyler), "A şıkkı" gibi harf anma YASAK. Soru numarası okunmaz. "Hoca", "sınavda
   şu yıl" yok. Kısa, net, öğretici; sohbet dolgu sözcüğü yok ("Harika", "Hadi bakalım" yok).
4. **Öğretici:** `siklar` 2–3 cümle (20–55 kelime): şıktaki kavram ne, ne işe yarar, bu soruda neden doğru/yanlış — `meds/docs/SIK_ACIKLAMA_STANDARDI.md`; `ipucu`/`cozum` kısa kalır.

## Alanlar (soru başına)
- `no`: kaynak no (aynı sıra, hepsi).
- `kontrol`, `soru`, `secenekler`, `dogru`: yukarıdaki kural 2.
- `kok_ses`: `soru` kökünün ses biçimi (anlam birebir aynı; şıkları içermez).
- `secenek_ses`: {A..E}: her şıkkın ses biçimi (yalnız şık metni; harf yok). Şık zaten okunabilir Türkçeyse aynen.
- `ipucu`: {metin, ses} — TEK cümle, 6–24 kelime. Cevabı söylemez, cevabın kelimesini/kökünü/sayısını içermez (doğru şık metnindeki
  4+ harfli hiçbir sözcüğün ilk 5 harfi ipucunda geçmesin). Düşündürür: hangi mekanizmayı/ayırt edici özelliği hatırlamalı, hangi
  kavram çiftini ayırmalı ("Geri dönüşümlü hasarda zarın sağlam kaldığını ve en erken değişikliğin su ile ilgili olduğunu düşün.").
- `siklar`: {A..E} her şık için {metin, ses} — 1–2 cümle, 6–34 kelime:
  - Yanlış şık: şıktaki kavramla başla, bu kavramın PDF'teki gerçek özelliğini söyle ve neden bu sorunun cevabı olmadığını göster
    ("Karyoreksis, piknotik çekirdeğin parçalanmasıdır; geri dönüşümsüz hasarın, yani nekrozun bulgusudur.").
  - Doğru şık: şıktaki kavramla başla, "doğru" sözcüğünü içersin, neden doğru olduğunu söylesin ("Hücresel şişme doğru: ATP azalınca
    sodyum pompası bozulur, hücreye su girer; bu en erken geri dönüşümlü bulgudur.").
  - Her açıklama o şıkka özgü; beş açıklama birbirini tekrar etmez. Sayılar PDF'teki gibi.
- `cozum`: {metin, ses} — 1–2 cümle, 10–40 kelime: sorunun öğrettiği ana bilgi + ayırt edici nokta. "Doğru cevap …" diye BAŞLAMA (asistan
  bunu kendisi söyler); doğrudan bilgiyle başla ("Hidropik değişim, yani hücresel şişme, geri dönüşümlü hasarın en erken bulgusudur;
  karyoreksis ve karyolizis ise nekrozda görülür.").
- `sayfa`: bu sorunun bilgilerinin geçtiği PDF sayfaları listesi (`[26, 33]`), en az 1.

## Çift biçim: `metin` (ekranda) ve `ses` (EMA okur)
İkisi aynı içerik, yalnız yazım farklı.
- `metin`: normal Türkçe yazım; kısaltma, sayı, simge serbest (`HPV`, `%30`, `≥`, `Na⁺/K⁺`). `**kalın**` ile en kritik 1 terimi
  vurgulayabilirsin. Parantez kullanma.
- `ses` (ve `kok_ses`, `secenek_ses`):
  - **Kısaltmalar harf adlarıyla ayrık:** "HPV" → "ha pe ve", "CD4" → "ce de dört", "TP53" → "te pe elli üç", "BRCA1" → "be er ce a bir",
    "PSA" → "pe se a", "ER/PR" → "e er ve pe er", "HER2" → "her iki", "IgA" → "i ge a", "ATP" → "a te pe", "DNA" → "de ne a",
    "C3" → "ce üç". Türkçe açılımı yerleşikse açılım ("DCIS" → "duktal karsinoma in situ"). Kelime gibi okunanlar okunuşuyla:
    "RAS" → "ras", "AIDS" → "eyds". Kısaltmaya ek gerekirse açılımı yaz.
  - **Sayılar ve simgeler yazıyla:** "%10" → "yüzde on", "1–2" → "bir ile iki", "20–30 dakika" → "yirmi ile otuz dakika",
    "~700" → "yaklaşık yedi yüz", "≥" → "eşit ya da büyük", "Na⁺/K⁺ ATPaz" → "sodyum potasyum a te pe az", "Ca²⁺" → "kalsiyum".
    Rakam (0–9), %, /, →, ±, ≈, ~, <, >, =, +, ⁺, parantez, köşeli parantez, `*`, `#`, `:`, `;`, tırnak, `|` (durak hariç) YASAK.
    `:` ve `;` yerine virgül ya da nokta.
  - **Yunan harfleri:** α alfa, β beta, γ gama, κ kappa, λ lambda.
  - **Latince/İngilizce/özel adlar Türkçe okunuşla:** "Helicobacter pylori" → "Helikobakter pilori", "Wilms" → "Vilms",
    "Gleason" → "Glison", "Paget" → "Peycet", "Virchow" → "Virkov", "Omnis cellula e cellula" → "omnis sellula e sellula",
    "functio laesa" → "funksiyo leza", "Oil Red O" → "oyl red o", "Masson trichrome" → "Mason trikrom", "Carnoy" → "Karnoy",
    "Bouin" → "Buen", "Zenker" → "Zenker", "frozen" → "frozın". Yerleşik Türkçe tıp yazımı ("adenokarsinom", "glomerülonefrit").
  - **Duraklar:** cümle sonu nokta. Vurgudan önce kısa durak ` | ` — cümle başına en çok bir; çoğu cümlede hiç gerekmez.
  - 25 kelimeden uzun ses cümlesini ikiye böl. Büyük harfli kısaltma, `**` ya da karışık harf (IgG, mRNA) seste YASAK.

## Çıktı — `cikti/<kod>.json`
```json
{"kod": "02", "sorular": [
 {"no": 1, "kontrol": {"durum": "tamam"},
  "soru": "…", "secenekler": {"A": "…", "B": "…", "C": "…", "D": "…", "E": "…"}, "dogru": "C",
  "kok_ses": "…", "secenek_ses": {"A": "…", "B": "…", "C": "…", "D": "…", "E": "…"},
  "ipucu": {"metin": "…", "ses": "…"},
  "siklar": {"A": {"metin": "…", "ses": "…"}, "B": {…}, "C": {…}, "D": {…}, "E": {…}},
  "cozum": {"metin": "…", "ses": "…"},
  "sayfa": [26]}
]}
```

## Bitiş
Her ders için `python3 dogrula.py cikti/<kod>.json` → **0 HATA**; UYARI'ları tek tek kontrol et (PDF'te olmayan sayı = büyük olasılıkla
hata). Yalnız `cikti/<kod>.json` yaz (başka dosyaya dokunma; geçici dosya gerekiyorsa `/tmp/claude-1000/cozucu_<grup>/`). Yerel GPU/LLM
kullanma. Son mesajında ders başına: soru sayısı, düzelttiğin sorular (no + kısa gerekçe), emin olmadığın telaffuzlar.
