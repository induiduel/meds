# Aşama kuralları — genel

> ÜRETİLMİŞ DOSYA: elle yazma. Kaynak `docs/KURUL2_YAPILMAYACAK_HATALAR.md`, üreteç `scripts/tam_hat/kural_secici.py`. 12 madde. Ayrıntı gerekirse madde başlığıyla defterde aç.

### H39 — Sesli metin kısaydı: sayfa atlanıyor, şekiller anlatılmıyordu (2026-10-24, kullanıcı "ders süresi az")
- k2-02'de 56 içerik sayfasının 12'si anlatılmamış, 19 sayfa tek cümleyle geçilmişti; "kısa ve öz" + paralel üretimde kapı yoktu.
  Kapı `isle.sesli_kapsam` (sayfa + derinlik). Kelime/dakika hedefi YOK; derinlik bilgi maddesi sayısından.

### H45 — Dar bölmede panel slayta göre büyüyor, yazının üstüne biniyor, kelimeler harf harf kırılıyordu (2026-10-24)
- Gerçek görüntüleyicide (Metin + Slayt, ~570 px sayfa) panel yazısı sabit px idi: panel slayta göre iki kat büyüyor,
  ayrılan boşluktan taşıp yazının üstüne biniyor, dar düğümde kelime harf harf kırılıyordu; panel yüksekliği tahmini de
  gerçeğin ~1,5 katı kısaydı. Düzeltme: panel/etiket boyu `cqw` (sayfa genişliğine oranlı), etiketler SVG'den HTML'e alındı
  (oransız ölçekte bozuluyordu), betikte `panel_boyu` (istemci diziliminin em kopyası). Sınama: 35 panelin hepsi 567 px ve
  1100 px sayfada ayrılan alana ve sayfa/ek alan sınırına sığıyor (sınama sayfası tarayıcı ölçümü).

### H47 — Kelime takipçisi küçük yazıyı okunmaz yapıyordu; ek alan gereğinden sık ve uzundu (2026-10-24)
- Telefon görüntüsü (s.54): konuşulan kelimenin iç gölgesi (3 px) ve koyu zemini "serebral" kelimesinin harflerini kapattı.
  Düzeltme: zemin .13, çizgi harflerin altında (2 px, dışarıda).
- Ek alan her sığmayan panelde baştan açılıyor ve panelin tamamı kadar oluyordu. Düzeltme: panel slaytın alt boşluğundan
  başlar, sayfa yalnız taşan kısım kadar uzar (en büyük ek 0,58 → 0,39 sayfa boyu; s.11'de ek alan hiç gerekmedi).
  Zincirde okun etiketi yanındaki düğümün altına girip kesiliyordu → etiket okun üstünde akış içinde, ok büzülmez.

### H68 — H66 tekrarı + süs bölüm sayfaları `sekil` türünde (2026-10-26, k2-27 periyodik muayeneler)
- **Çözüm / kural:** Çıkmışlar `kanit.sayfa` cümlelerine bağlandı (c0003, c0037, c0047, c0101, c0112, c0204, c0213, c0218, c0222) ve sesli uyarı eklendi; süs bölüm sayfaları `tur: kapak` yapıldı. Haritacı, bilgi taşımayan bölüm başlık/kapanış sayfalarını `kapak` yazar; sesli yazar H66 adımını atlamaz. Kapı gevşetilmedi.


### H100 — Asklepios kutlama efekti görünmüyordu (2026-10-27)
- **Kural:** ortada çizilen efekt kartın altında kalmaz; kartı örtmeyen konuma (iki yan) çizilir ve canvas kart üstüne (`is-ust-katman`) alınır. Yeni kutlama efektini canlı kartla birlikte gör.


### H106 · `baglam.kazanimlar` kapak metninden türetilmiş çöp şablon cümleler içeriyor (2026-10-27, k2-08)
- **Çözüm:** k2-08 kazanımları dersten elle yazıldı (8 ölçülebilir kazanım).
- **Kural:** Genel şablon ("temel kavramlarını … analiz eder") ya da kapak metni içeren kazanım kullanılmaz. Açık iş: `isle.kazanimlar` kayıt yoksa boş dönmeli (kod düzeltmesi bu turda yapılmadı).


### H109 · v2 cümlesinin `ses` alanında iç cümle sonu: sunucu cümle sayısı v2 ile tutmuyor (2026-10-27, k2-05 Nörolojik Muayene)
- **Çözüm:** `konusma_v2.dogrula` her `ses`'in tek cümle olmasını HATA sayar (`_cumle_sayisi`, sunucu kuralıyla aynı); yazar iki cümleyi iki v2 cümlesine böler. k2-01…k2-05 veride ihlal yok.
- **Kural:** her v2 `ses` tam bir cümledir; yazım betiğinde ayrıca kendi sınır kontrolü (cümle sayısı = 1, ≤25 kelime) çalıştırılır.


### Sesli derste geri oku "Ders çalış"a atıyordu (2026-10-27)
- **Çözüm / kural:** Uygulama içinden gelindiyse (`navigateTo` `__icGezinti` bayrağını koyar) ok `history.back()` yapar; doğrudan bağlantıyla açıldıysa ayrıntı sayfasına gider. Geri düğmeleri sabit hedefe değil, geldiği yere dönmelidir.


### Sesli derste canlı konum bazen çalışmıyor / bozuk çalışıyordu (2026-10-27)
- **Çözüm / kural:** Eksik öğede kısa aralıkla yeniden dene; sıfır boyutta kaydırma yapma; 3 px altı scroll farkını kullanıcı eylemi sayma. Yeni takip/kaydırma kodu bu üç durumu karşılamalı.


### H117 · Tam ekranda ayar düğmesi araç şeridini göstermiyordu (2026-10-27)
- **Çözüm/kural:** tam ekran şeridinde `container-type: normal; width: max-content`; seçici düzeltildi. Mutlak konumlu öğeye `container-type: inline-size` verilirse genişlik açıkça verilir; `:is()` içinde başa combinator yazılmaz.


### H106 · Çalışma takvimi (ısı haritası) hücreleri dev görünüyordu (2026-10-27)
- **Çözüm:** Sütun `minmax(0, 16px)` + `justify-content: start`; hücre en çok 16 px.
- **Kural:** Kare hücreli ızgaralarda (ısı haritası, takvim) sütun genişliğine üst sınır koy; `1fr` + `aspect-ratio` birlikte kullanılmaz.


### H111e · Profil verisi dinleyicileri render sırasında setState yapıyordu (2026-10-28, Bugün/Arka plan)
- **Çözüm:** `userKvSync.ts` `bildir()` dinleyicileri `queueMicrotask` ile çağırır (tüm dinleyiciler zaten zamanlayıcı/setState yapıyor; eşzamanlılık gerekmiyordu). Sınama: sayfa_tarama /bugun, /arka-plan konsol hatası 1 → 0.
- **Kural:** localStorage/depo yazımına bağlı olay yayıcıları dinleyicileri eşzamanlı çağırmaz (mikro görev); render içinde (useState başlatıcısı, useMemo) yan etkili yazım yapılmaz.

