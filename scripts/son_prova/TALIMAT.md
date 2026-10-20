# Son Prova — Sesli Özet Ders Yazım Talimatı (yazar alt ajanlar için)

Kurul 1 sınavı yaklaşıyor (100 teorik soru: Patoloji 34, Enfeksiyon 22, Genetik 12, Üroloji 12, Halk Sağlığı 10,
Kadın Doğum 6, Farmakoloji 4). "Son Prova" her dersi 1–4 parta bölünmüş **sesli özet derslerle** tekrar ettirir.
Amaç: öğrenci yalnız bu modülle sınavın **en az yarısını** yapabilsin. Bu yüzden içerik **özet ama eksiksiz**:
çıkmış soruların sınadığı her bilgi, sınavda sorulmaya müsait her hap bilgi (tanım, sınıflama, sıralama, en sık/en önemli,
tanı ölçütü, bulgu ve belirti, tedavi ve ilaç, sayı/oran/süre), karıştırılan kavram çiftleri. Dolgu, tekrar, giriş/kapanış yok.

Metin EMA sesiyle **olduğu gibi** okunur; öğrenci aynı anda metni ve kırpılmış ders slaytını görür (her cümle kendi
slaytına bağlanır, okunan kelime işaretlenir). Her aşamanın sonunda öğrenci senin seçtiğin soruları sesli asistanla çözer;
partın sonunda check-up testi gelir.

## Kaynaklar (yalnız bunlardaki bilgiyi kullan)
Görevde sana partın `plan.json` girdisi verilir; her ders için:
- `pdf_metin` — **BİRİNCİL kaynak**, slayt metni, `=== SAYFA N ===` ile sayfa numaralı. Her cümlenin bilgisi burada olmalı.
  OCR'ı bozuk ya da görsel ağırlıklı sayfalar varsa ve bilgi oradaysa PDF'in kendisine bakabilirsin:
  `meds_downloads/drive_root/Kurul 1/<Branş klasörü>/<pdf_ad>` (Read aracı PDF sayfalarını görüntü olarak okur, `pages` ile).
- `sesli_anlatim` — bu dersin 69 ders hattındaki tam sesli anlatımı (güvenilir, aynı slaytlardan; yapı ve vurgu için).
- `ders_notu` — amfi ders notu (varsa).
- `onem` — "Sınav için en önemliler" listesi (`maddeler`: puan, bilgi, alt, alinti sayfası, neden). Puanı 85+ olan her madde metinde geçmeli.
- `havuz_katalog` — `meds_temp/son_prova/havuz/<slayt_kod>.md`: bu dersin **çıkmış soruları** ve **soru havuzu** (ref'li).

Kaynakta olmayan bilgi, kendi literatür bilgin, uydurma sayı **YASAK**. Kaynaklar çelişirse güncel slaytı (pdf_metin) esas al.
Çıkmış sorunun anahtarı slaytla çelişiyorsa slaytı yaz ve `atlanan_cikmis`e gerekçesini yaz.

## Kapsam önceliği
1. **Her çıkmış sorunun** sınadığı bilgi (doğru şıkkın bilgisi + kökün sınadığı kavram + çeldiricilerin doğru yeri) metinde geçer.
   O cümle "Burası önemli, …" ile başlar ya da "çıkmış sorularda … soruldu" bilgisini içerir (her çıkmışta değil; aşama başına 2–6 kez,
   gerçekten sık sorulan yerde). Soru yılı, numarası, şık harfi okunmaz.
2. Önem listesinin 85+ puanlı maddeleri ve slayttaki sınav spotu sayıları/oranları.
3. Hap bilgi: tedavi/ilaç (ilk seçenek, alternatif, kontrendikasyon), bulgu/belirti, tanı yöntemi, en sık neden, sınıflamalar, sıralamalar.
4. Kalan konular bir iki cümleyle geçilir ama **dersin hiçbir ana konusu atlanmaz**: ders baştan sona slayt sırasıyla ilerler.

## Öğretici, özgün ve hızlı anlatım
- Özet ders: her cümle bir bilgi taşır. Uzun hikâye, tekrar, "şimdi şuna bakalım" geçişleri yok.
- Her alt başlık 1 cümlelik net tanım/konu cümlesiyle başlar, sonra maddeler gelir.
- Karıştırılan çiftleri açıkça ayır ("… ile … karıştırılır; ayıran bulgu …").
- Sıcak ama hızlı bir hoca üslubu. "Arkadaşlar" en fazla aşamada bir kez. Selam, kapanış, "bu derste" girişleri yok.
- Aynı bilgi iki kez anlatılmaz (başka aşamada anlatılan bilgiye yalnız kısa atıf).

## Hiyerarşi (ekranda başlık/madde/alt madde olarak görünür)
- **Aşama** = bir ders (ya da büyük dersin bir konu bloğu). `baslik`: ekranda aşama adı.
- **Alt başlık** (`bolumler[].baslik`): konu başlığı; okunmaz, ekranda görünür. Kısa, Türkçe; rakam serbest (ör. "Tip 1 ve tip 2 diyabet").
- **Paragraf**: ekranda bir blok. **İlk cümle giriş** (konu cümlesi), sonraki cümleler **madde** olarak gösterilir.
- **Alt madde**: bir cümle sayım bildiriyorsa ("Üç evresi vardır.", "Dört temel bulgusu şunlardır.") ya da liste açıyorsa
  ("… şunlardır.", "… üçe ayrılır.") sonraki cümleler o maddenin **alt maddeleri** olur. Sayım sayısı kadar cümle yaz;
  "Birincisi …", "İkincisi …", "Son olarak …" sıralamaları alt madde olarak dizilir. Tablo varsa her satırı bir cümle yap
  ("Nefrotik sendromda proteinüri günde üç buçuk gramın üzerindedir.").

## Türkçe üslup (kapı: meds/scripts/turkce_uslup.py)
Doğal, eksiksiz Türkçe. Çeviri mecaz ("imzası", "motoru", "freni", "çapası", "anahtar oyuncu", "kilit taşı") ve iç etiket
("Ayrım cümlesi:", "Kısa formül:", "Akılda tut:", "Mantığı şudur:", "Sınavda en olası soru buradan:") YASAK.
İç süreç dili YASAK: "PDF'te", "slaytta yok", "aday", "havuz", "katalog", "ders notunda".

## Seslendirme kuralları (metin harfi harfine okunur; ekranda sayılar otomatik rakama döner)
- **Sayılar yazıyla:** "yüzde otuz", "on birinci hafta", "üç buçuk gram", "yüz kırk milimetre cıva", "on iki ile yirmi dört saat".
  Rakam, %, /, +, ×, →, ≥, ±, ↑, ↓ YOK ("artmış", "azalmış", "en az", "en çok" yaz).
- **Kısaltma ve gen adları** standart yazımıyla (ekranda doğru görünsün): DNA, IL-1, TNF, CD31, ICAM-1, HPV, HIV, ÜSE, CYBE, IgE, MHC,
  BRCA1, PSA, AFP, hCG, TMP-SMX. Rakam yalnız böyle adların içinde serbesttir. Yunan harfi yazıyla: "TNF alfa", "beta laktam", "TGF beta".
  İlk geçişte açılımı söyle ("cinsel yolla bulaşan enfeksiyonlar, yani CYBE").
- **Parantez, tırnak, köşeli parantez, yıldız, noktalı virgül, tire ile madde imi YOK.** Kısa çizgi yalnız birleşik adlarda (IL-1, Birt-Hogg-Dubé).
- **Cümle sınırı (ZORUNLU):** her cümle `.` `?` ya da `!` ile biter. Cümle İÇİNDE nokta + boşluk + büyük harf geçemez
  ("vs.", "örn.", "Dr.", "St." YASAK). İki nokta üst üste ile cümle bitirme. Üç nokta yok. Cümle küçük harfle başlamaz.
- Latince/İngilizce terimler yerleşik Türkçe yazımıyla (nekroz, apoptoz, Treponema pallidum, Chlamydia trachomatis, Escherichia coli).
- Cümle 8–32 kelime (en çok 40). Uzun sıralamaları iki cümleye böl.

## Yapı ve uzunluk
- Her aşama 3–8 alt başlık; her alt başlık 1–3 paragraf; her paragraf 3–8 cümle, 40–150 kelime.
- Kelime hedefi görevde verilir (ders başına). Özet olsun ama çıkmış ve 85+ önem maddesinin hiçbiri eksik kalmasın;
  hedefi %25'ten fazla aşma. Partın toplam süresi en fazla 88 dakika (112 kelime/dk).

## Slayt bağlantısı (her cümle için ZORUNLU)
Her cümleye bilgisinin geçtiği **slayt sayfası**: `"k": "p07:23"` (`slayt_kod:sayfa`, sayfa = `=== SAYFA N ===`).
En açık anlatıldığı tek sayfayı seç. Slaytta karşılığı olmayan bağlayıcı cümlede `"k": null` (önceki slayt açık kalır; oran %20'yi geçmesin).
Paragrafın ilk cümlesine mutlaka sayfa ver. Sayfa numarasını pdf_metin'de arayarak bul; uydurma sayfa verme. Slaytlar sırayla ilerlemeli
(geri dönüş yalnız gerekiyorsa). Bu sayfalarla öğrenciye **kırpılmış özet PDF** üretilecek: atıf yapılmayan sayfa öğrenciye gösterilmez,
o yüzden önemli tablo/şema sayfalarına da atıf yap.

## Sorular (her aşama)
`havuz_katalog`'daki soru havuzundan ref ile seç (yeni soru yazma):
- `sorular`: **3–5 soru** (aşama sonu, ses eşliğinde çözülür). Yalnız **bu aşamada ve önceki aşamalarda anlatılan** bilgiyle çözülebilmeli
  (sızıntı yok: anlatmadığın bir bilgiyi soran soruyu seçme — seçtiğin sorunun bilgisini metne ekle). En az biri çıkmış (varsa);
  zorluk kolay–orta ağırlıklı, en çok biri zor. Aynı bilgiyi soran iki soru seçme.
- `checkup`: **2–4 soru** (part sonu check-up adayı), `sorular`dan farklı, yine bu aşamada anlatılanla çözülebilen; çıkmış ve orta ağırlıklı.
- Kalan havuz soruları genel check-up ve deneme sınavlarına ayrılır; o yüzden bir dersin havuzunun yarısından fazlasını kullanma.

## Çıktı (yalnız bu dosyalara yaz)
`meds_temp/son_prova/parca/<part-key>/aNN.json` — her aşama ayrı dosya, NN görevde verilen numaradan başlar (iki haneli: a01, a02 …):
```json
{
  "asama": 3,
  "ders": "p07",
  "baslik": "Akut enflamasyon",
  "giris": "Aşamanın konusunu ve sınavla bağını söyleyen tek cümle (okunur).",
  "giris_k": "p07:2",
  "bolumler": [
    {"baslik": "Damarsal olaylar", "paragraflar": [
      [ {"t": "Akut enflamasyonun ilk olayı damar çapında ve geçirgenliğinde değişikliktir.", "k": "p07:8"},
        {"t": "…", "k": "p07:9"} ]
    ]}
  ],
  "sorular": ["patoloji/07#12", "patoloji/07#3", "patoloji/07#30"],
  "checkup": ["patoloji/07#41", "patoloji/07#7"],
  "karsilanan_cikmis": ["2c53ae28a450", "…"],
  "atlanan_cikmis": {"kimlik": "neden atlandığının gerekçesi (anahtar slaytla çelişiyor vb.)"}
}
```

## Bitirmeden önce (ZORUNLU)
1. Her dosya için `python3 meds_temp/son_prova/dogrula.py meds_temp/son_prova/parca/<part>/aNN.json` → **0 HATA** (uyarıları da mümkünse düzelt).
2. Çıkmış listesindeki her soruyu tek tek kontrol et; bilgisini metne koy ve kimliğini `karsilanan_cikmis`e yaz. Aynı soru farklı
   kimlikle birkaç kez listelenmişse hepsini yaz.
3. Her sayı/oran/süre kaynağa birebir uyuyor mu kontrol et; her `k` sayfasında o bilgi gerçekten var mı kontrol et.
4. Seçtiğin her sorunun doğru cevabının bilgisi metinde (bu ya da önceki aşamada) açıkça var mı kontrol et.
5. Son mesajında yalnız: dosyalar, kelime, alt başlık, soru/check-up sayısı, karşılanan çıkmış / toplam, atlanan ve nedeni.

Başka hiçbir dosyaya yazma; site verisine dokunma. Yerel GPU/LLM kullanma.
