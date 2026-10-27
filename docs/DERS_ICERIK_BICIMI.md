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
