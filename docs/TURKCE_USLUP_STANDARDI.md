# Türkçe Üslup Standardı — öğrenciye okunan ve gösterilen tüm metinler (ZORUNLU)

> Kullanıcı kararı, 2026-10-18: "Cümleler Türkçeye uygun olsun; üslup Türkçe açısından eksiksiz ve anlaşılır olmalıdır."
> Kapsam: sınav asistanı anlatımı ve soruları, sesli soru çözücü, spot (önem listesi), Öğren desteleri, ders özetleri —
> ve Kurul 2'den itibaren tam otomatik üretilecek her içerik. Metin EMA ile harfi harfine okunduğu için kulağa doğal gelmeyen
> her ifade iki kez kötüdür: hem okunurken hem dinlenirken.

## Neden

Sınav asistanı, Patoloji 08 · "IL-6: karaciğerde akut faz yanıtı":

- "IL-6 makrofaj ve diğer hücrelerden salınır; **imzası** karaciğerde akut faz yanıtını uyarmaktır." — "imza" İngilizce
  *signature* çevirisi; Türkçede tıbbi anlatımda bu anlamda kullanılmaz.
- "**Ayrım cümlesi:** ateşte IL-1 daha belirgin, akut fazda IL-6, nötrofil alımında IL-17." — yazarın iç etiketi öğrenciye
  sızmış; ne anlama geldiği anlaşılmıyor.

Doğal karşılıkları:

- "IL-6 makrofajlardan ve diğer hücrelerden salınır; en önemli etkisi karaciğerde akut faz yanıtını başlatmaktır."
- "Bu üç sitokini şöyle ayırabilirsiniz: ateşte IL-1, akut faz yanıtında IL-6, nötrofillerin bölgeye toplanmasında IL-17 öne çıkar."

## Kurallar

1. **Çeviri mecaz yok.** "imzası", "motoru", "freni", "çapası", "gaz pedalı", "anahtar oyuncu", "oyun değiştirici" yerine
   "en belirgin özelliği / tipik bulgusu", "temel nedeni", "baskılayıcısı", "bağlandığı yapı", "uyarıcısı", "temel rol oynayan".
2. **İç etiket yok.** "Ayrım cümlesi:", "Kısa formül:", "Akılda tut:", "Mekanizma şudur:", "Mantığı şudur:", "Ayırt et:",
   "Ayrım:" gibi yazarın kendine koyduğu başlıklar metne girmez. Bilgi doğrudan, tam cümleyle verilir
   ("… şöyle ayrılır: …", "Özetle, …", "Unutmayın, …"). Arayüzün kendi kutu başlıkları ("Akılda kalsın") bu kurala girmez.
3. **Tam ve kurallı cümle.** Özne–yüklem eksiksiz; yüklemsiz liste cümlesi ("ateşte IL-1, akut fazda IL-6") ancak bir giriş
   cümlesinin devamında ve iki noktadan sonra gelir. Noktalı virgülle üç ayrı yargı tek cümleye sıkıştırılmaz.
4. **Doğal söz dizimi ve ekler.** Kısaltmadan sonra gelen ek okunuşa uyar ("IL-6'nın", "CRP'nin"); edilgen-etken karışmaz;
   "ve diğer hücrelerden" gibi eksik eşlemeler tamamlanır ("makrofajlardan ve diğer hücrelerden").
5. **Tıp Türkçesi.** Türkçe karşılığı yerleşik terim Türkçe yazılır (yangı/enflamasyon derste nasıl geçiyorsa); yerleşik
   olmayan İngilizce kelime metne karışmaz.
6. **Seslendirmeye uygunluk.** Cümle yüksek sesle okunduğunda tek seferde anlaşılmalı; 25 kelimeyi aşan ses cümlesi bölünür.

## Kalite kapısı

- `meds/scripts/turkce_uslup.py` — yasak mecaz ve etiket listesi; asistan (`spot_cozucu/asistan_dogrula.py`,
  `patoloji_onem/asistan_dogrula.py`, `asistan2/dogrula.py`) ve çözücü (`patoloji_cozucu/cozucu_dogrula*.py`,
  `spot_cozucu/cozucu_dogrula.py`) doğrulayıcılarında her metin alanına uygulanır, ihlal HATA'dır. Listeyi yeni bir kalıp
  görüldüğünde genişlet (önerilen karşılığıyla birlikte).
- Liste her kalıbı yakalayamaz: bağımsız denetçi geçişi her metni **sesli okunuyormuş gibi** okur ve doğal olmayan, eksik
  ya da anlaşılmayan cümleyi yeniden yazar.

## Mevcut veri borcu (2026-10-18 ölçümü)

Yasak kalıp sayısı ≈290: patoloji asistan 171, patoloji önem 45, patoloji çözücü 39, enfeksiyon 23, üroloji 12, genetik 3.
En sık: "fren…" 110, "imza…" 75, "Ayrım:" 43, "Akılda tut:" 16, "Ayırt et:" 15, "Mekanizma/Mantığı şudur:" 14.
