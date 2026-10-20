# Canlı Ders Konuşma Metni — Ders İşçisi Talimatı (Claude, Oracle, başsız)

Görevin: Bu taslak klasöründeki **tek bir dersin** canlı ders (sesli anlatım) metnini yazmak. Metin yayından sonra
Türkçe kadın sesleriyle (Microsoft Emel ve EMA Lightning) **olduğu gibi** seslendirilir; öğrenci dersi dinlerken ekranda
metin ve PDF slaytı eşzamanlı ilerler. Kullanıcı "kusursuz ve hatasız" istiyor. Kurallar, mevcut 69 dersin metinleriyle
aynıdır (`meds_temp/sesli_anlatim/TALIMAT.md`'nin ders işçisi uyarlaması).

## Girdiler (çalışma dizini = taslak klasörü; yalnız buraya yaz)
1. `kaynak.md` — güncel amfi PDF'inin metni (`=== SAYFA n ===`). **Birincil kaynak.**
2. `deck.json` — bu derse az önce ürettiğin etkileşimli deste (anlatımlar, sınav spotları, terimler, tablolar).
3. `sayfa_haritasi.json` — başlık yapısı ve sayfa sırası: **anlatım sırası budur** (başlıklar → bölümler).
4. `cikmis_baglantilari.json` + `baglam.json` → `cikmis_adaylari` — `ilgili: true` olan her çıkmış sorunun kökü, şıkları
   ve doğru cevabı (`baglam.json`'daki aynı `soru_id`).
5. Gerekirse `ders_notu.md` ve `ders_paketi.json` (bilgi_paketi). Başka kaynak yok; kendi literatür bilgini ekleme.

## Çıktı: `konusma_metni.md`
```
# <Dersin başlığı>

@@ <Bölüm başlığı 1>
<Paragraf>

<Paragraf>

@@ <Bölüm başlığı 2>
...
```
- `@@` satırları bölüm başlığıdır (seslendirilmez, oynatıcıda bölüm listesi olur). 8–25 bölüm; `sayfa_haritasi.json`
  başlıklarını izle (çok küçük alt başlıkları birleştirebilirsin).
- Bölüm altındaki her şey **aynen okunur**. Paragraflar boş satırla ayrılır; paragraf 40–160 kelime.
- Markdown YOK: `*`, `#`, `|`, `>`, `-` madde imi, `==`, emoji, köşeli parantez, tablo, URL kullanma. Yalnız düz Türkçe
  cümleler ve noktalama.

## İkinci çıktı: `konusma_sayfalari.json` (PDF eşleşmesi — zorunlu)
Canlı derste her paragraf okunurken yanda o paragrafın anlattığı PDF sayfası açılır. Bunun için **her paragraf için bir
sayfa numarası** yaz: metindeki paragraf sırasıyla (bölüm başlıkları `@@` ve `#` satırı sayılmaz; boş satırla ayrılmış her
metin bloğu bir paragraftır), `kaynak.md`'deki `=== SAYFA n ===` numaralarıyla:
```json
[4, 5, 5, 6, 8, 8, 9]
```
- Uzunluk paragraf sayısına **tam eşit** olmalı; her sayı `kaynak.md`'de var olan bir sayfa olmalı.
- Paragraf birden çok sayfayı anlatıyorsa anlattığı ilk içerik sayfasını yaz; tablo/şekil anlatıyorsa o şeklin sayfasını.
- Sıra PDF sırasını izler (anlatım sırası zaten budur); "özetle" paragrafı son anlatılan sayfayı tekrar edebilir.

## Kapsam ve sadakat (en önemli kural)
1. **Eksiksiz:** `kaynak.md`'deki ve `deck.json`'daki her tıbbi bilgi (tanım, sınıflama, mekanizma, örnek, sayı/yüzde,
   gen/ilaç/hastalık adı, ayırıcı tanı, klinik not, şekil/tablo açıklaması) anlatımda yer almalı.
2. **Uydurma yok:** Bu girdilerde olmayan tıbbi bilgi ekleme. Yalnız anlamayı kolaylaştıran kısa bağlayıcı açıklama
   ("yani…", basit benzetme) serbest; yeni olgu, sayı, ilaç, gen, sınıflama ekleme. Deste referansla tamamlanmış bir
   bilgi içeriyorsa (kanıtı `referans`) onu anlatabilirsin.
3. **Tablolar:** neyi karşılaştırdığını söyle, sınavda önemli ve kaynakta vurgulanan satırları cümleye dök; her hücreyi
   okuma ama önemli eşleşmeyi atlama. **Şekiller:** ne gösterdiğini ve kilit noktasını 1–3 cümleyle anlat.
4. OCR/yazım bozukluğu varsa doğru tıbbi biçimle yaz; çelişkide güncel slaytı (`kaynak.md`) esas al.
5. **Bir PDF birden çok konu içeriyorsa** yalnız bu dersin (`baglam.json` → program.konu, deste kapsamı) sayfalarını anlat.

## Giriş ve akış
- **Doğrudan konuya gir.** "Merhaba", ders tanıtımı, hoca adı, telif/uyarı slaytı, "bugün şunları göreceğiz", kaynakça,
  "dinlediğiniz için teşekkürler" YOK. İlk cümle dersin ilk tıbbi kavramıyla başlar.
- Sıra: `sayfa_haritasi.json`'daki sayfa/başlık sırası (PDF eşleşmesi buna dayanır; geri dönüp ileri atlama).
  Her bilgi bir kez anlatılır; sonda en fazla 3–5 cümlelik "özetle" serbest (yeni bilgi yok).
- Üslup: deneyimli, sıcak bir kadın klinik hocası; öğretici, akıcı. "Arkadaşlar" en fazla ~5 kez. Mekanizmaları
  neden-sonuç zinciriyle anlat; karıştırılan kavramları açıkça karşılaştır.

## "Burası önemli" (zorunlu)
- `cikmis_baglantilari.json`'da `ilgili: true` olan **her** çıkmış sorunun ölçtüğü bilgi (doğru şık + kökün test ettiği
  kavram) anlatımda geçmeli ve orada **"Burası önemli"** denmeli ("Burası önemli, bu bilgi çıkmış sorularda soruldu: …").
- Destedeki yüksek önemli sınav spotları için de kullanabilirsin; her paragrafa serpiştirme.
- Soru yılı, soru numarası ya da şık harfi okuma.

## Uzunluk
- Hız ~112 kelime/dk. **En az 1.150, en fazla 6.000 kelime.** İçerikli slayt başına kabaca 60–80 kelime; 40 sayfalık
  ders ≈ 2.500–3.500, 90+ sayfalık yoğun ders ≈ 5.000–6.000. 6.000'i asla aşma: tekrarları kıs, bilgiyi kısma.

## Telaffuz (seslendirme motoru metni harfi harfine okur)
- **Kısaltmalar** okunduğu gibi: "DNA" → "de ne a", "HPV" → "ha pe ve", "CD4" → "ce de dört", "TP53" → "te pe elli üç",
  "BRCA1" → "be er ce a bir", "IgA" → "immünoglobulin A"; açılımı Türkçe biliniyorsa açılımı yaz; kelime gibi okunanları
  okunuşuyla ("Dünya Sağlık Örgütü"). (EMA sesi için heceler ayrıca otomatik birleştirilir; sen ayrık yaz.)
- **Sayılar/simgeler** yazıyla: "%30" → "yüzde otuz", "5 mg/dL" → "beş miligram bölü desilitre", "2018" → "iki bin on
  sekiz", "≥" → "eşit ya da büyük". Rakam ve simge kullanma.
- **Yunan harfleri:** alfa, beta, gama, kappa, lambda. **Yabancı adlar** Türkçe okunuşla ("Helikobakter pilori", "Vilms").
- Parantez kullanma; parantez içini cümleye yedir. Büyük harfli kısaltma bırakma.

## Bitirmeden önce (zorunlu)
1. `kaynak.md` ve `deck.json`'u baştan sona gez; her sayfa/adım için anlatımda karşılık var mı; eksikleri ekle.
2. Her `ilgili` çıkmış soru için bilginin ve "Burası önemli"nin bulunduğunu kontrol et.
3. Uydurma/çelişen sayı var mı kontrol et.
4. `python3 /app/scripts/sesli_anlatim/metin_denetle.py konusma_metni.md` → **0 HATA** olana kadar düzelt.
   Metni her değiştirdiğinde `konusma_sayfalari.json`'u da güncelle (uzunluk = paragraf sayısı).
5. Son mesajın tek satır: `BİTTİ-SESLİ: <kelime> kelime · <bölüm> bölüm · <burası önemli> önemli · <karşılanan>/<toplam> çıkmış`.

Yalnız `konusma_metni.md` ve `konusma_sayfalari.json` yazılır; başka dosyaya dokunma (deck.json ve diğer çıktılar bitti).

## §v2 — Kurul 2 ve sonrası: `konusma_v2.json` (ZORUNLU; kullanıcı kararı 2026-10-20)
Kurul 2+ derslerinde **yalnız `konusma_v2.json` yazılır**; `konusma_metni.md` ve `konusma_sayfalari.json` ondan otomatik
türetilir (`scripts/sesli_anlatim/konusma_v2.py --turet`), elle yazma. Yukarıdaki kapsam, sadakat, sıra ve çıkmış
kuralları aynen geçerlidir. Şema ve kimlik kuralları `konusma_v2.py` başındadır; özet:

- **İki yüz, tek içerik:** her cümlenin
  - `ses` alanı: bir tıp doktorunun karşısındaki tıp öğrencisine anlatır gibi kurduğu, doğal, tam Türkçe cümle (EMA bunu
    okur; markdown/işaret yok, kısaltmalar okunuşa uygun). Mekanizmayı neden-sonuç bağıyla anlat; "şimdi şuna bakalım",
    "bunu sınavda sık sorarlar" gibi hoca dili serbest, ama abartma ve dolgu yok.
  - `ekran` alanı: aynı bilginin ekranda gösterilecek **madde** hâli (en çok 28 kelime; kısa, isim cümlesi olabilir).
    Kilit kavramı `**…**` ile işaretle. `duzey` 0 = ana madde, 1 = alt madde (bir öncekinin ayrıntısı).
- **Vurgu kodu:** `vurgu: [{"metin": "<ekran metninde geçen ifade>", "tur": "terim|sayi|tuzak|cikmis|tanim"}]`.
  `cikmis` = bu ifade bir çıkmış sorunun cevabıdır (`cikmis` alanına o soru kimliklerini de yaz); `tuzak` = klasik
  çeldirici; `sayi` = eşik/oran/doz/süre; `tanim` = tanım cümlesinin çekirdeği. Her cümlede vurgu zorunlu değil.
- **Bağlar:** paragrafın `sayfa`'sı `kaynak.md` sayfası (eski konusma_sayfalari kuralı); cümlenin `slayt_adim`'ı
  deck.json'daki ilgili adımın kimliği (`<ders_id>-d-s<adım no 2 hane>`), varsa `spot` kimliği.
- **Slayt çapası (ZORUNLU, kullanıcı kararı 2026-10-20):** canlı derste konuşulan her kelime PDF'te anlık işaretlenir;
  bunun için her cümleye `slayt: {"sayfa": N, "satir": [...], "sekil": null}` yaz.
  - `satir`: cümlenin anlattığı slayt madde(ler)ini `kaynak.md`'nin o sayfasından **harfi harfine kopyala** (madde imi
    hariç, satır bölünmüşse birleştir). Uydurma/yeniden yazılmış satır kapıdan geçmez.
  - `ses` cümlesini o maddenin kelimeleriyle kur: maddedeki terimler aynı sırayla ve aynı biçimde geçsin (açıklama,
    neden-sonuç ekleri serbest). Maddenin en az %80'i cümlede geçmezse PDF'te madde zemini yanmaz.
  - `sekil`: metni olmayan resim/şema/grafik anlatılıyorsa kısa tarifi (ör. "nekroz tiplerinin mikroskobik görüntüsü");
    canlı derste lazer imleci o resme gider. Tablo hücresi anlatılıyorsa hücre metni `satir`'a yazılır.
  - Yalnız bağlam/geçiş cümlesi `slayt: null` olabilir (en çok %25). Kapı her satırı o sayfanın metninde arar.
- **Kimlik:** `ders_id` = `baglam.json` → `ders_id`'nin ilk iki parçası (ör. `k2-07`). Bölüm `k2-07-b01`, paragraf
  `k2-07-p001`, cümle `k2-07-c0001`; ders içinde tekil. İlk yazımda sırayla ver. Düzeltme turunda var olan cümlenin
  kimliğini **değiştirme** (soru açıklamaları ve deeplinkler buna bağlanır); araya eklenen cümle kullanılmamış bir
  sonraki numarayı alır, silinen cümlenin numarası yeniden kullanılmaz.
- **Kapı:** `python3 /app/scripts/sesli_anlatim/konusma_v2.py --dogrula .` 0 HATA (Türkçe üslup dahil), sonra
  `metin_denetle.py` 0 HATA.
