# Ders içerik paketi biçimi (Terimler · Hastalıklar · Bilgiler · Tablolar · Sorular · Kartlar)

Ekran: `src/components/v15/DersIcerikV15.tsx` + `src/styles/v15/dersIcerik.css`. Veri: `src/data/ders_icerik/<key>.json`
(`scripts/ders_icerik_uret.py`). Yeni dersin içerik işçisi veriyi bu ekranın okunaklı gösterebileceği biçimde ayıklar
(kullanıcı kararı 2026-10-27). Düz paragraf yığını YASAK.

## Maddeler (hastalık bölümleri `m`, önemli nokta `alt`, bilgiler)
- Her madde tek fikir; 1–2 cümle. Uzun paragraf maddelere bölünür.
- Başlıklı madde: `Etiket: açıklama` → ekranda kalın etiket. (ör. `Babinski: başparmak dorsifleksiyonu`)
- Alt maddeler: aynı maddede `;` ile 3+ parça → iç içe madde olarak gösterilir. (ör. `Bulgular: hipotoni; hiporefleksi; atrofi`)
- Vurgulanacak terim `**kalın**`.
- Hastalık bölüm adları sabit sözlükten: Etiyoloji, Patogenez, Klinik bulgular, Tanı, Tedavi (renk/ikon bunlara bağlı).

## Tablolar (`h` başlık, `r` satırlar, `k` karşılaştırma)
- Sıralı süreç → ilk sütun `Sıra`/`Adım`/`Aşama` ve 1,2,3… kesintisiz (numara atlanmaz) → adım şeridi.
- İki sütunlu eşleşme (terim → anlamı/yeri) → eşleşme kartları; sol değer kısa tutulur.
- 3+ sütun karşılaştırma → `k: true`, ilk sütun ölçüt, diğerleri kıyaslanan kutuplar; hücreler kısa
  (`Var`/`Yok`/`+`/`−`/`artar`/`azalır` rozet olur). Hücreye cümle yazılmaz.
- Tablolar asla metin içinde düz yazı olarak verilmez.

## Önemli noktalar / spotlar
- `b` başlık ≤ 8 kelime, `m` 1–2 cümlelik özet, `alt` 2–5 kısa madde, `n` "neden önemli" tek cümle, `p` 0–100 puan.

## Terimler / kartlar
- Tanım 1–2 cümle; eş anlamlar `e` dizisinde ayrı ögeler; kısaltma kendi listesinde.

## Zorunlu kapsam ve kaynak kuralı (kullanıcı kararı 2026-10-27)
- Yeni eklenen HER slayt/ders için paket üretilir; eksik paketle ders "tamamlandı" sayılmaz. Üretim: `python3 scripts/ders_icerik_uret.py <key>`;
  kapı: `python3 scripts/ders_icerik_dogrula.py <key>` 0 HATA. Çıkarılacaklar: terim, kavram, kısaltma, hastalık (etiyoloji, patogenez, klinik bulgu,
  tanı, tedavi, ayırt edici/karakteristik özellik), spot, önemli nokta, tablo, karşılaştırma, sıralama/liste, tanım, kart, örnek soru, mini soru.
- **Kaynak dışı veri YASAK:** her kayıt slayt/sayfaya (`s`, `n`) bağlıdır; ders notu, slayt ve yayındaki deste/havuz dışında bilgi yazılmaz.
- **Sıra türü kayıtlıdır** (`listeler[].sira`): `numara` (1,2,3), `alfa` (a,b,c), `azalan` (büyükten küçüğe), `madde` (sırasız); ekran buna göre <ol>/<ul> kurar.
- **Karşılaştırma** `tablolar[].k` ile işaretlenir; ekranda terazi simgesi + renkli sütunlar. Karşılaştırma düz yazıyla verilmez.
- İç içe: başlık › alt başlık › madde › alt madde (`Etiket: a; b; c`). Hastalık/kavram bölümleri gruplanmış bilgidir; kaynağı slayttır.
- Yeni sayfa türü gerekirse `DI_BOLUMLER` + `DersIcerikV15` + `DersDetayV15` satırı + bu belge BİRLİKTE güncellenir (tasarım–kod uyumu).

- **Sesli örnek soru çözücü** da paketin parçasıdır: her şık için kaynak (slayt/sayfa) gösteren ayrıntılı açıklama + EMA sesi; çözücü yoksa kapı HATA verir.
