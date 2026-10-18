# Spot bilgiler + soru çözücü — bağımsız denetim (ikinci göz) talimatı

> ⚠️ **Şık açıklama standardı (ZORUNLU, 2026-10-18):** her şık açıklaması kavramın ne olduğunu, ne işe yaradığını ve bu soruyla
> bağını anlatır; "bu sorunun cevabı değil / … olarak geçmez" gibi geçiştirme HATA'dır. Ayrıntı ve kaynak sırası: `meds/docs/SIK_ACIKLAMA_STANDARDI.md`.
> ⚠️ **Türkçe üslup standardı (ZORUNLU, 2026-10-18):** metin doğal, eksiksiz ve anlaşılır Türkçe olur; çeviri mecaz ("imzası",
> "motoru", "freni") ve iç etiket ("Ayrım cümlesi:", "Akılda tut:", "Mantığı şudur:") YASAK. Ayrıntı: `meds/docs/TURKCE_USLUP_STANDARDI.md`.

Çalışma klasörü: `/home/indu/medsor/meds_temp/spot_cozucu/<brans>/`. Önce `TALIMAT_ONEM.md` ve `TALIMAT_COZUCU.md`'yi
(`/home/indu/medsor/meds/scripts/spot_cozucu/`) baştan sona oku. Başka bir yazar `onem/<kod>.json` ve `cozucu/<kod>.json`'u üretti, biçim
doğrulayıcılarından geçti. Öğrenci bunları okuyup sesli dinleyerek sınava girecek; **tek yanlış bilgi kabul edilmez.** Sen bağımsız
denetçisin: ders PDF metnini (`pdf_metin/<kod>.md`) baştan sona oku, sonra her şeyi PDF'e karşı doğrula ve hataları DÜZELT (yalnız rapor
etme).

## 1) Önem listesi (`onem/<kod>.json`)
- Her maddenin `bilgi`, `alt`, `detay` önermeleri PDF'te açıkça var mı? Kitap/genel bilgiyle eklenmiş cümle, PDF'te olmayan sayı/doz/süre,
  yanlış genelleme ("her zaman", "en sık" PDF'te öyle denmediyse) → düzelt ya da sil.
- Puanlar makul mü (çıkmışta birden çok yıl sorulan bilgi yüksek; ayrıntı düşük)? Sınav açısından önemli bir PDF bilgisi hiç maddeye
  girmemiş mi (özellikle slaytta vurgulanan "en sık / ilk seçenek / tanı" bilgileri)? Eksikse madde ekle (sayı sınırı 20–45).
- **Çözülebilirlik:** maddeye bağlı her çıkmış ve örnek soruyu yalnız o maddenin `bilgi + alt + detay` metniyle çöz. Doğru cevabı bulmak
  ve çeldiricileri elemek için gereken PDF bilgisi orada yoksa detayı PDF'ten genişlet (60–250 kelime) ya da soruyu doğru maddeye taşı.
- Çıkmış bağları: bağlanan soru gerçekten o maddenin bilgisini mi soruyor?

## 2) Çıkmış kararları
- Kullanılan her çıkmış: konusu bu PDF'te mi, anahtar PDF'e göre doğru ve tek mi? Kök/şık/anahtar `cikmis/<kod>.json`'daki temsilciyle
  birebir mi (değiştirilmemeli)?
- `elenen_cikmis`: gerekçe doğru mu? PDF'te çözülebilen ve anahtarı tutarlı bir soru yanlışlıkla elendiyse geri al (maddeye bağla +
  `cozucu`'ya tam açıklamasıyla ekle). Elenen `anahtar_celiskili` soruların `not`'unda PDF sayfasıyla somut gerekçe olmalı.
- Kullanılan iki çıkmış aynı bilgiyi soruyorsa (farklı yıl tekrarı) birini `tekrar:<id>` ile ele.

## 3) Örnek sorular
- Anahtar PDF'e göre tartışmasız tek doğru mu? Başka şık savunulabilir mi, eşanlamlı iki şık var mı, kök belirsiz mi, "hangisi değildir"
  kökünde birden çok yanlış şık var mı? Bilgi PDF'te açıkça var mı?
- Çıkmışların üslubunda mı? Zorluk etiketi gerçekçi mi (kolay = tek temel bilgi; orta = ayırt etme/sayı/tedavi seçimi; zor = öncüllü/vaka/
  mekanizma/istisna)? Dağılım ağırlıklı orta mı?
- **Tekrar yok:** hiçbir örnek bir çıkmışla (temsilci ya da `tekrar` kopyaları) veya başka örnekle aynı bilgiyi sormamalı. Aynıysa örneği
  aynı maddenin sorulmamış başka bir bilgisine (ya da başka maddeye) yeniden yaz.
- Örneği değiştirirsen aynı değişikliği hem `onem` hem `cozucu` dosyasına yaz; çözücüdeki açıklamaları (ipucu, şıklar, çözüm, ses) yeni
  soruya göre yeniden yaz.

## 4) Çözücü açıklamaları (`cozucu/<kod>.json`)
- `ipucu`, `siklar`, `cozum`: her önerme PDF'te var mı; sayılar birebir mi; ipucu cevabı eşanlamlı ya da tanımla sızdırıyor mu; doğru şık
  açıklaması gerçekten doğru gerekçe mi; yanlış şık açıklaması o şıkkın PDF'teki gerçek özelliğini mi söylüyor (uydurma yok)?
- `ses` alanları `metin` ile aynı bilgiyi taşıyor mu; kısaltmalar harf harf ve Türkçe harf adlarıyla mı, Latince adlar Türkçe okunuşla mı,
  sayılar yazıyla mı? `okunus_denet.py` çıktısını incele.

## Bitiş
`python3 /home/indu/medsor/meds/scripts/spot_cozucu/onem_dogrula.py onem/<kod>.json` ve
`python3 /home/indu/medsor/meds/scripts/spot_cozucu/cozucu_dogrula.py cozucu/<kod>.json` → ikisi de **0 HATA**; okunuş:
`python3 /home/indu/medsor/meds/scripts/patoloji_cozucu/okunus_denet.py cozucu/<kod>.json`. JSON'u Python ile oku/yaz
(`ensure_ascii=False`, `indent=1`). Yalnız kendi derslerinin `onem/` ve `cozucu/` dosyalarını değiştir; geçici dosyalar
`/tmp/claude-1000/denetim_<kod>/`. Yerel GPU/LLM yok. Son mesajında ders başına: değiştirdiğin her öğe (kısa gerekçe + PDF sayfası),
geri alınan/elenen çıkmışlar, yeniden yazılan örnekler, genişletilen detaylar, düzelttiğin okunuşların sayısı ve örnekleri.
