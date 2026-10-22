# Blok özet ekleri (TALIMAT.md'nin ÜSTÜNDE geçerli; çelişirse bu dosya kazanır)

Bu kez Son Prova değil, **Patoloji blok özet sesli dersi** yazıyorsun (kullanıcı isteği, 2026-10-22):
birkaç dersi tek sesli derste, **çok özet olmadan**, çıkmış odaklı anlatmak. Part süresi **en az 62, en çok 115 dakika**
(112 kelime/dk). Görevdeki ders kelime hedeflerine ±%15 uy.

- **Çıkmış odaklı:** her çıkmış sorunun sınadığı bilgi metinde, anlaşılır biçimde açıklanmış olsun (neden öyle olduğunu bir
  cümleyle söyle: mekanizma, ayırt ettiren bulgu). Sık sorulan yerlerde "Burası önemli" ya da "çıkmış sorularda" kullan.
- **En önemli yerleri açıkla, anlaşılır kıl:** kuru liste değil; kavramı tanımla, mekanizmayı tane tane anlat, karıştırılan
  çiftleri ayır. Ama dolgu, tekrar, "hoca vurguladı" gibi meta cümleler YASAK.
- **Tablolara ve resimlere takılma:** tabloyu satır satır okuma; yalnız sınav değeri olan satırları cümleye çevir. Mikroskop
  resmi, makroskopi fotoğrafı, şema betimlemesi yapma (yalnız tanı koydurucu tek bulgu adı geçebilir: "Psammom cisimleri" gibi).
- **Soru seçme YOK:** `sorular` ve `checkup` alanlarını boş liste `[]` yaz. `karsilanan_cikmis` / `atlanan_cikmis` ZORUNLU.
- Kapı: `python3 meds_temp/blok_ozet/dogrula.py --part <part>` → PART 0 HATA (yazar grubu olarak yalnız kendi dosyalarını
  `dogrula.py <dosya>` ile 0 HATA'ya getir; part süresi denetimini son denetçi yapar).
