# Spot bilgiler (Sınav için en önemliler, 100 puan) + ders soru havuzu — 1. adım (yazar ajan talimatı)

> ⚠️ **Türkçe üslup standardı (ZORUNLU, 2026-10-18):** metin doğal, eksiksiz ve anlaşılır Türkçe olur; çeviri mecaz ("imzası",
> "motoru", "freni") ve iç etiket ("Ayrım cümlesi:", "Akılda tut:", "Mantığı şudur:") YASAK. Ayrıntı: `meds/docs/TURKCE_USLUP_STANDARDI.md`.

Çalışma klasörü: `/home/indu/medsor/meds_temp/spot_cozucu/<brans>/` (`enfeksiyon` = Kurul 1 Enfeksiyon Hastalıkları, `uroloji` = Kurul 1 Üroloji).
Bu iş patolojide yapılan "Sınav için en önemliler" listesinin ve sesli soru çözücünün aynısını bu derslere kurar. Bu adımda:
(1) dersin önem listesi (spot bilgiler), (2) dersin **örnek soruları**, (3) çıkmış soruların ders PDF'ine göre seçimi yazılır.
Sesli çözücünün açıklamaları ikinci adımdadır (`TALIMAT_COZUCU.md`).

## Kullanıcının kuralları (KESİN)
- **Tek kaynak ders PDF'i** (`pdf_metin/<kod>.md`, `=== SAYFA n ===` ayraçlı; 2026-27 Drive Kurul 1 ders slaytı). **PDF'te olmayan hiçbir bilgi
  yazılmaz** — kendi tıp bilgini, kitap bilgisini, başka ders notunu EKLEME. PDF'teki ifadeyi sadeleştirebilir, Türkçesini düzeltebilir,
  kısaltabilirsin; yeni olgu/sayı/oran/ilaç/doz/terim ekleyemezsin. Müfredat = bu PDF.
- **Sınava yönelik:** sınavda sorulabilecek bilgi (tanım, en sık, karakteristik bulgu, ayırıcı özellik, sayı/eşik/doz/süre, etken–hastalık
  eşleşmesi, sınıflama, mekanizma, tanı yöntemi, tedavi seçimi/ilk seçenek, klasik tuzak). Tarihçe, genel giriş cümlesi, teşekkür vb. YOK.
- **Spot bilgi sayfası çıkmış ve örnek sorularla güçlendirilir; o sorular maddedeki bilgiyle ÇÖZÜLEBİLMELİ:** bir maddeye bağlanan her çıkmış
  ve örnek sorunun doğru cevabını bulmak ve çeldiricileri elemek için gereken PDF bilgisi o maddenin `bilgi` + `alt` + `detay` alanlarında
  yazılı olmalı (ör. "hangisi risk faktörü değildir" sorusu bağlandıysa detay PDF'teki risk faktörü listesini içerir). Yetmiyorsa detayı
  PDF'ten genişlet; PDF'te çözülebilecek bilgi yoksa soru o maddeye (ve çözücüye) alınmaz.
- **Tekrarlayan soru yok:** aynı bilgiyi soran iki soru olmaz (örnek–örnek, örnek–çıkmış, çıkmış–çıkmış).

## Girdi
- `girdi/<kod>.json`: `{kod, no, ad (PDF adı), sayfa, brans, cikmis_tekil, ornek_hedef}`.
- `cikmis/<kod>.json`: bu derse eşlenmiş, sitede görünen çıkmış sorular — tekrarlar zaten gruplanmış: her öge bir **temsilci**
  `{id, yil, sinav, kok, secenekler{A..E}, dogru, tekrar:[{id, sinav}] (aynı soru başka yıllarda), yillar:[…], dikkat?}`.
  Eşleme makinedir: bazıları başka derse/konuya ait ya da PDF kapsamı dışında olabilir. `dikkat: true` = kayıt şüpheli.
- `pdf_metin/<kod>.md`: **baştan sona oku.**

## Çıktı — `onem/<kod>.json`
```json
{
  "kod": "e07", "baslik": "Sifiliz", "pdf": "7)Sifiliz .pdf",
  "ozet": "Dersin 2–3 cümlelik özeti (PDF'ten).",
  "neden_onemli": "Sınav açısından önemi: kaç çıkmış soru, hangi konular tekrar tekrar soruluyor (1–3 cümle).",
  "maddeler": [
    {
      "id": "e07-01", "puan": 96,
      "baslik": "Sifilizin etkeni",
      "bilgi": "Sifiliz etkeni **Treponema pallidum**dur …",
      "alt": [],
      "tur": "eslesme",
      "alinti": [{"sayfa": 3, "metin": "PDF'ten BİREBİR 4–30 kelime"}],
      "neden": "Neden önemli — 1 cümle (ör. '2020-21 ve 2023-24'te soruldu', 'klasik çeldirici: …').",
      "detay": "- **Başlık:** açıklama\n- **…:** … (60–250 kelime, yalnız PDF içeriği, maddeli; bağlı soruları çözdürecek bilgi)",
      "cikmis": ["c1b740ecd59e"],
      "ornek": [
        {"kok": "…?", "secenekler": {"A": "…", "B": "…", "C": "…", "D": "…", "E": "…"}, "dogru": "C", "zorluk": "orta",
         "aciklama": "1–3 cümle: neden doğru + en güçlü çeldirici neden yanlış (PDF'e dayalı)", "sayfa": [3, 4]}
      ]
    }
  ],
  "elenen_cikmis": [{"id": "…", "neden": "pdf_disi | anahtar_celiskili | gorsel | tekrar:<id> | belirsiz", "not": "kısa gerekçe, PDF s. n"}]
}
```

### Maddeler
- `tur`: `tanim` | `en_sik` | `karakteristik` | `sayi` | `eslesme` | `mekanizma` | `siniflama` | `tuzak` | `tani_tedavi`.
- Madde sayısı PDF yoğunluğuyla orantılı: **20–45** (20 sayfalık ders ~20–25, 50+ sayfa ~35–45). Aynı bilgi iki maddede yazılmaz.
- **100 puan ölçeği** (sınavda sorulma olasılığı × önem), bantlar 10'ar puan: 90–100 bandında 4–8 madde ("olmazsa olmaz"); 80–89, 70–79,
  60–69, 50–59 bantlarının her birinde en az 2 madde. Puan ipuçları: çıkmışta sorulmuş → yüksek (birden çok yılda sorulmuş → 90+);
  slaytta "en sık / en önemli / ilk seçenek / tanı koydurucu / dikkat / önemli" vurgusu, büyük harf, tekrar → yüksek; ayrıntı/istisna → düşük.
- `bilgi`: tek cümle, 4–30 kelime; anahtar terim `**kalın**`. `alt`: en çok 4 kısa alt madde (her biri ≤20 kelime). `bilgi`/`alt`'taki her
  sayı (yüzde, yaş, süre, doz, oran) PDF metninde birebir geçmeli.
- `alinti`: 1–3 öge; `metin` ilgili sayfadan BİREBİR (büyük/küçük harf, satır sonu, madde işareti farkı önemsiz); `sayfa` doğru (±1).
- `detay`: 60–250 kelime, maddeli (`- **Başlık:** açıklama`), yalnız PDF bilgisi; bağlı tüm soruları çözdürecek kadar ayrıntılı.
- `neden`: çıkmışta sorulduysa yıllarını yaz (`yillar` alanından; "2020-21" biçimi); sorulmadıysa slayttaki vurguyu ya da klasik tuzağı.
- Öğrenciye dönük metinlerde iç süreç dili YOK ("aday", "bağlandı", "eşlendi", "PDF'te yok", "talimat", "ajan").

### Çıkmış soru seçimi
- `cikmis/<kod>.json`'daki **her temsilci** için karar ver: ya en az bir maddenin `cikmis` listesinde (kullanılan) ya da `elenen_cikmis`te.
- Kullanılacak soru: konusu bu ders PDF'inde işleniyor ve anahtarı PDF'e göre doğru, tek doğru. Kök/şık/anahtar **değiştirilmez**.
- Ele: `pdf_disi` (sorunun bilgisi bu PDF'te yok/başka dersin konusu), `anahtar_celiskili` (PDF başka şıkkı destekliyor ya da iki şık doğru —
  `not`'ta PDF sayfasıyla açıkla; anahtarı kendin değiştirme), `gorsel` (şekil/resim gerekiyor), `tekrar:<id>` (başka bir temsilciyle aynı
  bilgiyi soruyor — yenisini/daha iyisini tut), `belirsiz` (kök bozuk/eksik, anlaşılmıyor).
- Bir çıkmış soru, onu çözdürecek bilgiyi taşıyan maddeye bağlanır (en çok 2 madde). O maddenin puanı yüksek olmalı (çoğu 80+).

### Örnek sorular (`ornek`)
- **Soru üslubu ve tıbbi kapsam (ZORUNLU, kullanıcı uyarısı 2026-10-27):**
  - Soru kökünde dersi/slaytı/bölümü çağrıştıran, öznel ya da kaynağa gönderen ifade YASAK: "dersin bölümüne göre", "bu derste anlatıldığına göre",
    "slaytta belirtildiği gibi", "notlara göre", "yukarıdaki bilgiye göre", "hocaya göre". Soru kendi başına, ders okunmamış bir sınav sorusu gibi tam ve bağımsız olur.
  - Üslup çıkmış sorulara benzer olmalı; yalnız genel kabul görmüş kalıplar kullanılır: klinik vaka kökü (yaş, cinsiyet, yakınma, bulgu → "Bu hastada en olası tanı/
    tanıyı doğrulayan/en olası mekanizma/ilk yapılacak/tedavi hangisidir?"), "Aşağıdakilerden hangisi …dir?", "… ile ilgili aşağıdakilerden hangisi YANLIŞTIR/ doğrudur?",
    "Hangisi … özelliğidir?". Garip, oyunsu, meta ("bu bilgi hangi başlıkta") veya tanımsız kalıp kurulmaz.
  - Her soru müfredat → kazanım → konu zincirinde yer alan, tıbbi olarak anlamlı ve sınavda sorulabilir bir bilgiyi ölçer. Slayttaki rastgele bir ayrıntıyı
    (başlık sırası, görsel düzen, anekdot, sayfa notu, tıbbi olmayan öge) sormak YASAK; soru önce hangi kazanıma hizmet ettiğiyle gerekçelendirilebilmelidir.
- Toplam örnek soru sayısı: **`max(ornek_hedef, 20 − kullanılan çıkmış sayısı)`** ile **`ornek_hedef + 6`** arası. Ders çözücüsü = örnek +
  kullanılan çıkmış (karışık, 20–40'lık setler).
- **Çıkmışlara uygun:** bu dersin çıkmış sorularının biçim ve üslubunda yaz — "Aşağıdakilerden hangisi … değildir/yanlıştır?", "en sık …",
  öncüllü (I, II, III, IV + "I ve III" gibi şıklar), 1–2 cümlelik kısa vaka ("… yaşında hasta … ; en olası tanı / ilk seçilecek tedavi
  hangisidir?"), eşleştirme. 5 şık A–E, **tek doğru**, kök "?" ile biter; şıklar kısa ve aynı kategoriden (hepsi ilaç / hepsi etken / hepsi
  test …), eşanlamlı iki şık yok. Doğru cevap ve çeldiriciler PDF'teki kavramlardan; çeldiriciler derste öğretilen komşu kavramlar.
- **Zorluk:** ağırlıklı **orta**; kolay ve zor da bulunur. Dağılım (sayıyla): kolay %15–25, orta %50–65, zor %15–25.
  - kolay: tek bir temel bilgi (tanım, etken, en sık).
  - orta: iki kavramı ayırma, sayı/eşik, tedavi seçimi, "hangisi değildir" listesi.
  - zor: öncüllü çoklu bilgi, vaka + karar, mekanizma zinciri, istisna/tuzak.
- **Tekrar yasağı:** hiçbir örnek soru bir çıkmış soruyla (temsilciler ve tekrarları) ya da başka bir örnek soruyla aynı bilgiyi sormaz;
  çıkmış sorunun kelimelerini değiştirip yeniden yazmak YASAK. Çıkmışın sormadığı ama sınav potansiyeli yüksek bilgileri sor. Örnek sorular
  dersin tüm önemli bölümlerine yayılsın (puanı ≥60 olan maddeler öncelikli; bir maddede en çok 2 örnek).
- Doğru cevap harflerini dengeli dağıt (hiçbir harf %35'i geçmesin). "Hangisi yanlıştır/değildir" kökünde yalnız bir şık yanlış olmalı.
- `aciklama`: 1–3 cümle; neden doğru + en güçlü çeldiricinin neden yanlış olduğu (PDF'e dayalı). `sayfa`: bilginin geçtiği PDF sayfaları.

## Bitiş
`python3 /home/indu/medsor/meds/scripts/spot_cozucu/onem_dogrula.py onem/<kod>.json` → **0 HATA**; UYARI'ları tek tek incele (benzerlik
uyarısı = olası tekrar soru). JSON'u Python ile yaz (`ensure_ascii=False`, `indent=1`). Yerel GPU/LLM yok. Yalnız kendi derslerinin
`onem/<kod>.json` dosyasını yaz; geçici dosyalar `/tmp/claude-1000/spot_<kod>/`.
