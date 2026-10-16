# Patoloji önem listesi — "sınavda çıkabilecek" ayrımı — alt ajan talimatı

Çalışma klasörü: `/home/indu/medsor/meds_temp/patoloji_onem/sinav/` (PDF metinleri `../pdf_metin/<kod>.md`, `=== SAYFA n ===`).

Kullanıcının sınav bilgisi (hocadan, KESİN):
1. **Resim ve tablolardan soru sorulmayacak.**
2. **Klinik bulgu sorulmayacak.**
3. **Her ders slaytından (her PDF) 1 soru**; yalnız **"Genetik, Pediatrik ve Çevresel Patoloji" (kod 15) slaytından 2 soru**.

`partiler/<P>.json`: her ders için mevcut maddeler (`id, puan, tur, baslik, bilgi, alt, alinti[{sayfa, metin}], cikmis_sayisi, ipucu`).
`ipucu` otomatik: alıntının geldiği sayfada "Tablo"/"Şekil/FIG" geçiyor mu, sayfa tablo/şema gibi mi. İpucudur, kesin değil — **PDF sayfasını
kendin aç ve bak**: bilgi sayfadaki düz anlatım metninde (madde işaretli slayt metni) de geçiyorsa `metin` say; YALNIZ tablo hücresinde,
şekil/resim altyazısında, şema etiketinde geçiyorsa `tablo` / `sekil`.

## Her madde için
- `kaynak`: `metin` | `tablo` | `sekil` (bilginin slaytta asıl geçtiği yer; hem metinde hem tabloda varsa `metin`).
- `klinik`: `true` = maddenin sorduğu şey klinik bulgu/belirti/semptom/muayene bulgusu/klinik tablo (ör. "hematüri ile başvurur", "ağrısız kitle",
  "çocukta ödem", "ateş ve kilo kaybı"). Morfoloji/histopatoloji, mekanizma, tanım, sınıflama, etken, gen, epidemiyoloji (en sık) klinik DEĞİLDİR.
  Hem klinik hem patolojik bilgi içeriyorsa sorulabilecek kısmı patolojikse `false`.
- `sinava_uygun` = `kaynak == "metin"` ve `klinik == false`.

## Her ders için aday sıralaması
- `adaylar`: sınava uygun maddeler arasından bu slayttan sorulma olasılığı en yüksek **3–5 madde** (kod 15 için **5–7**), olasılık sırasıyla.
  Ölçüt: slaytta vurgu (en sık / en önemli / karakteristik / tanım / büyük harf / tekrar), çıkmış soru sayısı (`cikmis_sayisi`), puan,
  soru yazılabilirliği (tek doğru cevaplı net bilgi). Tablo/şekil/klinik madde aday OLAMAZ.
- `sira` 1 = en olası soru (kod 15'te sira 1 ve 2 = iki soru). Her adaya 1 cümlelik `gerekce` (öğrenciye dönük; "aday", "ipucu" gibi iç
  terim kullanma; ör. "Slaytta 'en sık' diye vurgulanıyor ve 2021-22, 2024-25'te soruldu.").

## Çıktı — `cikti/<kod>.json` (her ders ayrı)
```json
{"kod": "07",
 "maddeler": {"07-01": {"kaynak": "metin", "klinik": false}, "07-02": {"kaynak": "tablo", "klinik": false, "not": "yalnız Tablo 2.3'te"}},
 "adaylar": [{"id": "07-01", "sira": 1, "gerekce": "…"}, {"id": "07-05", "sira": 2, "gerekce": "…"}]}
```
Her maddeye bir kayıt (eksik yok). Bitiş: `python3 dogrula.py cikti/<kod>.json` → 0 HATA. Yalnız `cikti/` altına yaz; geçici betikler
`/tmp/claude-1000/sinav_<P>/` altında. Son mesajında ders başına: tablo/şekil/klinik sayısı, 1. sıradaki aday (kısa).
