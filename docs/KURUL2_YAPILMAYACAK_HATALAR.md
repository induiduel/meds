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
