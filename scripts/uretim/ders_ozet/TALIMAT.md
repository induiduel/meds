# Ders Özeti — yazar talimatı (Kurul 2+, alt ajan)

Amaç: öğrenci yalnız bu özete çalışarak dersin **bütün çıkmış sorularını ve örnek sorularını** çözebilsin; yine de
**özet** kalsın (dersin tam anlatımı değil). Hızlı okunur, sesli dinlenir (EMA, metin harfi harfine okunur), akılda kalır.

## Tek girdi
`meds_temp/ders_ozet/<k>/girdi.json` (topla.py). Başka dosya okuma. Alanlar:
- `sayfalar` — slayt metni (sayfa no → metin). **BİRİNCİL kaynak.** Her madde en az bir sayfaya (`s`) dayanır.
- `cikmis` — doğrulanmış çıkmışlar (`id`, kök, cevap, `s`). **Her biri** özetteki bir maddeyle cevaplanır.
- `onem.maddeler` — "Sınav için en önemliler" (puanlı). Puanı **85+** olan her madde özette geçer.
- `hoca_vurgu` — hocanın derste "önemli/dikkat" dediği yerler; `ogrenci_onem` — geçmiş yıl öğrenci A/B önem birimleri;
  `ogrenci_sentez` — öğrenci derlemesi (yalnız slaytta karşılığı varsa kullanılır, kendi başına kanıt değildir).
- `sorular` — dersin örnek + çıkmış soruları (çözücüde sesli çözülür). Doğru cevaplarının bilgisi özette bulunmalı.

Kaynakta olmayan bilgi, kendi literatür bilgin, uydurma sayı **YASAK**. Çıkmış anahtarı slaytla çelişirse slaytı yaz,
çıkmışı `atlanan_cikmis`e gerekçesiyle koy.

## Çıktı: `meds_temp/ders_ozet/<k>/ozet.json`
```json
{
  "ders": "k2-15",
  "baslik": "Şizofreni ve Diğer Psikotik Bozukluklar",
  "giris": "1–2 cümle: ders ne anlatır, sınavda en çok neresi sorulur.",
  "bolumler": [
    {"id": "b1", "baslik": "Kısa konu başlığı",
     "maddeler": [
       {"id": "b1-1", "tur": "bilgi", "metin": "Tek cümlelik ya da iki cümlelik bilgi.", "s": [2], "cikmis": []}
     ]}
  ],
  "akilda": [ {"metin": "Akılda kalması gereken tek cümle.", "s": [18], "cikmis": ["c116fba1f3d0"]} ],
  "cikmis_kapsam": {"<çıkmış id>": "b3-2"},
  "onem_kapsam": {"<önem baslik>": "b2-1"},
  "atlanan_cikmis": [ {"id": "…", "gerekce": "…"} ]
}
```
- `tur`: `bilgi` (temel bilgi) · `spot` (sayı/oran/süre/en sık/ilk seçenek gibi hap bilgi) · `ayirici` (karıştırılan iki
  kavramı ayıran bilgi: "X ile Y karıştırılır; X'te …, Y'de …") · `klinik` (tıbben önemli: tedavi, acil, kontrendikasyon, prognoz).
- `cikmis`: bu maddenin cevapladığı çıkmış id'leri (ekranda "Çıkmış" rozeti). `cikmis_kapsam` her doğrulanmış çıkmışı
  bir madde id'sine bağlar; o maddenin `cikmis` listesinde de aynı id olmalı.
- `onem_kapsam`: puanı 85+ olan her önem maddesinin `baslik`ı → onu karşılayan madde id'si.
- `akilda`: dersin sonundaki "Akılda kalması gerekenler" — **8–15** madde, en çok sorulan ve en ayırt edici bilgiler;
  bölümlerdeki cümlelerin kopyası değil, daha sıkı yeniden söylenişi.

## Ölçüler
- Bölüm 4–12; bölüm başına 3–12 madde; madde 6–45 kelime. Toplam (giriş + maddeler + akılda) **500–2500 kelime**;
  ders kısaysa alt sınıra yakın kal. Dolgu, giriş/kapanış cümlesi, "bu bölümde" geçişi yok.
- Bölümler slayt sırasını izler; dersin hiçbir ana konusu atlanmaz (önemsiz yer bir maddeyle geçilir).
- Her madde **ileriye yeni** bilgi taşır; aynı bilgi iki bölümde yazılmaz.

## Üslup ve seslendirme
- Doğal Türkçe, kısa cümle. `**kalın**` yalnız madde başına en çok bir anahtar kavram için. Başka markdown yok.
- Sayılar rakamla yazılabilir (%1, 6 ay, 25 yaş); okunuş betiği yazıya çevirir. Ok, ≥, ±, / gibi işaret YOK ("en az",
  "artmış" yaz). Kısaltmanın ilk geçişinde açılımı.
- Çeviri mecaz ("imzası", "motoru", "çapası"), iç etiket ("Akılda tut:", "Ayrım:"), iç süreç dili ("slaytta", "PDF",
  "çıkmış soruda soruldu ki", "aday", "havuz", soru yılı/şık harfi) YASAK. Kapı: `turkce_uslup.py`.
- "Hoca vurguladı" yalnız `hoca_vurgu`da karşılığı olan yerde ve dersin tamamında en çok 3 kez.

## Soru kapsamı (önce kapı, sonra bu)
- Her doğrulanmış çıkmış: zorunlu (kapı denetler). Çıkmışı olmayan derste `cikmis_kapsam` boş `{}` kalır.
- `sorular` (çözücü): doğru cevabın bilgisi özette olmalı. Soru çoksa (60+) aynı bilgiyi soran soruları tek maddeyle karşıla;
  kelime sınırını aşmadan cevaplanamayan soru kalırsa raporunda listele (uydurma ekleme yapma).
- Girdi PDF'ten okunduysa sayfa metninde düzen bozukluğu olabilir; anlamı çözülemeyen sayfaya dayanma.

## Bitince
`python3 scripts/uretim/ders_ozet/dogrula.py <k>` **0 HATA** verene kadar düzelt.
