# Hastalık önerisi → şema 2 profil (Claude, otomatik hat)

Girdi: `meds_database_v2/ders_isci/hastalik_onerileri/<ders_id>.json` — ders işçisinin bir ders PDF'inden çıkardığı profil
önerileri (`profiller[]`, düz metin dizileri; `mevcut: true` = sitede bu kimlikle kayıt var). Çıktı: her profil için
`meds_database_v2/ders_isci/hastalik_onerileri/sema2/<profil id>.json` (tek profil, şema 2).

Önce oku: `meds/docs/HASTALIK_MODELI.md` (model), `meds/src/types/disease.ts` (tipler), `src/data/diseases.json`'dan
`schemaVersion: 2` olan 2–3 örnek kayıt (biçim örneği), `scripts/diseases/varlik_esanlamlari.json` (kanonik varlık adları).

## Kurallar
- **Mevcut kayıt (`mevcut: true`):** sitedeki kaydı temel al; yalnız bu dersin getirdiği YENİ bilgiyi ilgili bölüme madde
  olarak ekle, aynı bilgiyi tekrar etme, var olan maddeyi silme ya da anlamını değiştirme. `lecture` bölümüne bu dersin
  maddelerini `source: "<ders_id>"` ile ekle; `relatedLectures`'a ders kimliğini ekle. Kimlik, ad, `aliases` değişmez.
- **Yeni kayıt:** öneriden şema 2 profil kur; kimlik önerideki `id` (slug, değiştirme).
- **Madde:** tek bilgi, doğal Türkçe (`docs/TURKCE_USLUP_STANDARDI.md`); `==terim==` vurgu, sınavda sorulan kritik bilgi
  `key: true`; `entities` yalnız tanımlı türlerden ve kanonik adla. Şablon cümle ("standart protokol…") YASAK.
- **Kaynak sadakati:** yalnız önerideki (ders PDF'inden gelen) bilgi; ekleme/tahmin yok. `references` yalnız öneride ya da
  mevcut kayıtta olanlar.
- `schemaVersion: 2`, `curation: {"yontem": "ders işçisi önerisi → şema 2 (otomatik)", "zaman": "<ISO>"}`.

## Kapı
Bitince: `python3 meds/scripts/diseases/hastalik_profilleri.py denetle` HATA sayısı başlangıçtakinden fazla olmamalı
(birleştirici `yayinla.py --hastaliklar` bunu yine denetler, artarsa geri alır). Yalnız `sema2/` altına yaz; başka dosyaya dokunma.
