# Kurul 2 — Yapılmayacak Hatalar Defteri (ZORUNLU OKUMA)

> Kurul 2'de sistem tam otomatik çalışacak: Drive'a gelen her yeni PDF'ten interaktif ders (Öğren), sesli spot / sınav asistanı
> ve sesli soru çözücü içeriği insan müdahalesi olmadan üretilip EMA ile seslendirilecek. Bu defter, Kurul 1 içeriğinde kullanıcının
> gördüğü ve **Kurul 2'de bir daha yapılmaması gereken** hataları toplar. Kurul 2 hattını kuran ya da çalıştıran her ajan önce
> bu dosyayı okur. Yeni bir hata bildirildiğinde buraya yeni madde eklenir (eskiler silinmez).
>
> Kurul 1'deki mevcut içerik bu defter yüzünden toplu olarak yeniden üretilmez; amaç gelecekteki üretimdir.

## H1 — Geçiştirici şık açıklaması (2026-10-18)

- **Görülen:** Sınav asistanı → Yardım al (Patoloji 08, IL-17 sorusu): "IL-2 bu sorunun cevabı değil.", "IL-10 nötrofil alımı
  yapmaz.", "IL-13 nötrofil toplayıcı olarak geçmez."
- **Neden hata:** Şıkkın ne olduğunu ve ne işe yaradığını söylemiyor; öğrenciye hiçbir şey öğretmiyor.
- **Kurul 2'de doğrusu:** Her şık (doğru dahil) için kavramın ne olduğu + ne işe yaradığı + bu soruda neden doğru/yanlış olduğu,
  2–3 cümle. Ayrıntı: `meds/docs/SIK_ACIKLAMA_STANDARDI.md`.
- **Kapı:** `meds/scripts/sik_aciklama.py`.

## H2 — Türkçeye uymayan ifade ve iç etiketler (2026-10-18)

- **Görülen:** Sınav asistanı (Patoloji 08, "IL-6: karaciğerde akut faz yanıtı"): "IL-6 … salınır; **imzası** karaciğerde akut
  faz yanıtını uyarmaktır." ve "**Ayrım cümlesi:** ateşte IL-1 daha belirgin, akut fazda IL-6, nötrofil alımında IL-17."
- **Neden hata:** "imzası" İngilizceden çeviri mecaz; "Ayrım cümlesi:" yazarın iç etiketi, öğrenci anlamıyor. Metin EMA ile okunduğu
  için doğal olmayan cümle dinlerken daha da kötü duyulur.
- **Kurul 2'de doğrusu:** Doğal, eksiksiz, anlaşılır Türkçe; çeviri mecaz ve iç etiket yok; tam cümle.
  Ayrıntı: `meds/docs/TURKCE_USLUP_STANDARDI.md`.
- **Kapı:** `meds/scripts/turkce_uslup.py` (liste her kalıbı yakalamaz; denetçi metni sesli okunuyormuş gibi okur).

## Kurul 2 hattı için genel kural

- Her içerik türünde yazar + bağımsız denetçi geçişi; doğrulayıcı 0 HATA vermeden EMA seslendirmesine ve yayına geçilmez.
- Bu defterdeki her maddenin kapısı Kurul 2 hattının doğrulayıcılarına bağlıdır (2026-10-18):
  - Sınav asistanı, sesli çözücü, spot önem listesi doğrulayıcıları: her zaman HATA.
  - Öğren: `validate_learning_decks.py deck.json --oyun-zorunlu --kurul2`; sınav spotları: `sinav_spotlari/dogrula.py --kurul2`.
  - **Kurul 2 başlarken ders işçisinin denetimine (`meds/scripts/ders_isci/denetle.py`, Öğren çağrısı) `--kurul2` eklenmeli** ve
    işçi talimatına bu defter okutulmalı. Kurul 1 işçisi bayraksız çalıştığı için şimdilik etkilenmez.

## Sesli ders PDF/DOCX dışa aktarımı (2026-10-20)

- **Yazıyla sayı:** konuşma metni okunuş için "iki virgül bir", "yüzde kırkına" yazar; öğrenciye verilen dosyada bunlar
  "2,1", "%40'ına" olmalı. Kural tek yerde: `src/services/sayiYazim.ts` (`sayilariYaz`), dışa aktarım
  (`components/canliDers/canliDersDisaAktar.ts`) ve ekran (`canliDersStore.ts` → `sayilariDuzelt`, vurgu konumları `sayilariYazEslemeli` ile taşınır) her derste uygular. Saklanan metin değiştirilmez (ses ve cümle zamanı ona bağlı).
- **Düz madde yığını yok:** paragraf tek madde olarak basılmaz; ilk cümle ana madde, sonrakiler alt madde, "Yani/Örneğin…"
  ve "2 ölçütü ayırın" gibi duyurulardan sonra gelenler ikinci düzey; kısa noktasız satır alt başlık olur.

## Canlı ders PDF işareti (2026-10-20)

- **Tahminle vurgu yok:** Kurul 1'de konuşma metni slayttan yeniden yazıldığı için okunan cümlenin slayttaki karşılığı
  kelime örtüşmesiyle tahmin ediliyordu; komşu madde yanıyor ya da hiçbir şey yanmıyordu. Kurul 2'de her `konusma_v2`
  cümlesi `slayt: {sayfa, satir[], sekil}` çapası taşır: `satir` `kaynak.md`'den **birebir** kopya (kapı: `konusma_v2.py
  --dogrula` her satırı o sayfanın metninde arar; çapasız cümle en çok %25). `ses` cümlesi maddenin terimlerini aynı
  sırayla kullanır. Akış: `--turet` → `konusma_capalari.json` → `yayinla.py` (`capalar`) → `data/sesli_anlatim/capa/<key>.json`
  → `pdf_isaret.py` (madde + kelime kutuları) → `isaret/<key>.json` → canlı ders.
- **Kurallar (kullanıcı):** slayt maddesi ancak içeriğinin ≥%80'i okunan cümlede geçiyorsa zeminle işaretlenir; konuşulan
  her kelime hem metinde hem PDF'te anlık işaretlenir (PDF'te yalnız karşılığı olan kelime); lazer imleci yalnız metni
  olmayan yerde (resim/şema, `sekil`). Kelime anı sesten ölçülen konuşma parçaları (`cumle_zaman.py` surum 2, `k`) ve hece
  sayısıyla bulunur; sessizlik kelimelere paylaştırılmaz, işaret animasyonsuz.
