> **Not (yeniden kullanım):** bu yönerge 2026-10-30 okumasında kullanılan haliyle saklanır; aşağıdaki `/tmp/...scratchpad` yolları o oturumun
> çalışma klasörüdür. Yeni notta: `parcala.py <not.pdf> <ad> <klasör>/hr/<ad>`, arşiv/2026-27 sayfa metinleri `<klasör>/y25txt/<anahtar>/sNN.txt`
> ve `<klasör>/y26txt/<k2-xx>/sNN.txt` (pdftotext -f N -l N), arama `OGRENCI_ONEM_CALISMA=<klasör> python3 -I scripts/ogrenci_onem/ara.py …`;
> çıktı `data/ogrenci_onem/ham/<pdf>_sNN.json`. Paralel okuyucular kırpmaları yalnız kendi alt klasörüne yazar (ortak `z.png` çakışması yaşandı).

# Öğrenci önem notu PDF'lerini okuma yönergesi (Kurul 2, 2026-10-30)

## Kaynak nedir
Dört PDF (psk3.2 = Psikiyatri, nöro3.2 = Nöroloji, tbg3.2 = Tıbbi Genetik, ftr3.2 = FTR) Dönem 3 Kurul 2'nin öğrenci
derleme notlarıdır. Bir öğrenci 2025-26 ders slaytlarından **en önemli yerleri kesip A3 sayfaya yapıştırmış**, üstüne
iPad'de el yazısı not, renkli vurgu ve çıkmış soru eklemiş. İçerik: hocanın üstünde durduğu / "buraya çalışın" / "sorarım"
dediği yerler, çıkmışlarda sorulan yerler, sorulması muhtemel yerler.

Görülen işaret dili (her sayfada kendin doğrula, farklıysa not et):
- **Yapıştırılmış slayt parçası** (basılı yazı). Üstünde **sarı/yeşil fosforlu vurgu** = önemli satır.
- **Pembe fosforlu blok içindeki küçük basılı soru** = yapıştırılmış **çıkmış soru**; şıklardan biri kırmızı daire/işaretle
  cevap olarak işaretli. Bazen yalnız "Soru? - cevap" biçiminde pembe satırdır.
- **Kırmızı el yazısı** = öğrencinin/hocanın derste söylediği ek bilgi, açıklama, kısaltma.
- **Kırmızı basılı (yazılmış) satırlar** = öğrencinin klavyeyle yazdığı özet notu.
- Kırmızı daire, alt çizgi, yıldız (★/*), ünlem, ok, "çıkmış", "önemli", "sorarım" yazıları = ek önem sinyali.

## Dosyalar
- Sayfa parçaları (200 dpi, 3 sütun × 2 satır, kenarlar 60 px örtüşür): `/tmp/claude-1000/-home-indu--claude-spares-spare-Q84dUq/4fcdf015-158b-4c2d-967c-7fb24262833c/scratchpad/hr/<pdf>/sNN_r<satır>c<sütun>.png`
- Sayfanın küçük genel görünümü (yerleşimi görmek için): `/tmp/claude-1000/-home-indu--claude-spares-spare-Q84dUq/4fcdf015-158b-4c2d-967c-7fb24262833c/scratchpad/hr/<pdf>/sNN_genel.png`
- Parçanın Tesseract OCR'si (yalnız yardımcı; el yazısında sık yanlış, asıl kaynak GÖRÜNTÜDÜR): `sNN_rXcY.ocr.txt`
- 2025-26 arşiv slaytlarının sayfa metni: `/tmp/claude-1000/-home-indu--claude-spares-spare-Q84dUq/4fcdf015-158b-4c2d-967c-7fb24262833c/scratchpad/y25txt/<y25 anahtarı>/sNN.txt`
- 2026-27 orijinal ders PDF'lerinin sayfa metni (yalnız k2-01, k2-02, k2-05, k2-08): `/tmp/claude-1000/-home-indu--claude-spares-spare-Q84dUq/4fcdf015-158b-4c2d-967c-7fb24262833c/scratchpad/y26txt/<k2-xx>/sNN.txt`
- Arama aracı (her zaman `python3 -I` ile):
  - `python3 -I /tmp/claude-1000/-home-indu--claude-spares-spare-Q84dUq/4fcdf015-158b-4c2d-967c-7fb24262833c/scratchpad/tools/ara.py y25 "<slayt metni>" --ders psk|noro|tbg|ftr -n 5` → hangi arşiv dersi/sayfası
  - `python3 -I /tmp/claude-1000/-home-indu--claude-spares-spare-Q84dUq/4fcdf015-158b-4c2d-967c-7fb24262833c/scratchpad/tools/ara.py y26 "<metin>" -n 3` → 2026-27 PDF sayfası (varsa)
  - `python3 -I /tmp/claude-1000/-home-indu--claude-spares-spare-Q84dUq/4fcdf015-158b-4c2d-967c-7fb24262833c/scratchpad/tools/ara.py banka "<soru kökü + şıklar>" --ders Psikiyatri|Nöroloji|"Tıbbi Genetik"|FTR -n 3` → çıkmış bankasındaki karşılığı
- Kurul 2 ders listesi (kimlik ↔ konu): `/home/indu/medsor/meds/src/data/dersler/k2.json`

## Ne yapacaksın (her sayfa için)
1. Genel görünüme bak, sayfadaki blokları (slayt parçası, pembe soru, el yazısı kümesi, özet notu) say ve konumla.
2. 6 parçanın HER birini görüntü olarak oku. Küçük yazıda emin değilsen PIL ile kırpıp büyüt
   (`python3 -I -c "from PIL import Image; im=Image.open('...'); im.crop((x0,y0,x1,y1)).resize((w*2,h*2)).save('<scratchpad>/z.png')"` sonra Read).
   El yazısında **her kelimeyi** okumaya çalış; tıbbi bağlamla doğrula (ör. "hiperkortizolizm", "Cushing"). Okuyamadığını uydurma: `guven: "dusuk"` + alternatif okuma.
3. Her bloğu arşiv slaytına eşle (`ara.py y25`), dersin Kurul 2 kimliğini bul (k2.json konusu). El yazısını **doğru slayt satırına** bağla (hangi satırın yanında/okla gösterilmiş).
4. Her pembe çıkmış soruyu tam yaz (kök + tüm şıklar + öğrencinin işaretlediği cevap), bankada ara; bulursan id, yıl, bankanın doğru cevabı. Öğrencinin cevabı ile banka/tıbbi doğru uyuşmuyorsa `tutarli:false` ve gerekçe.
5. Tıbbi hata ya da OCR/yazım bozukluğu görürsen `duzeltme` alanına ham → düzeltilmiş + gerekçe (slayt metni dayanak).
6. **İkinci geçiş (zorunlu):** sayfa JSON'unu yazdıktan sonra genel görünüme ve parçalara yeniden bak: atlanmış blok, pembe soru, el yazısı, yıldız var mı; el yazısı okumaların bağlamla tutarlı mı? Düzelt, sonra dosyayı son haliyle yaz.

## Çıktı
Her sayfa için `/home/indu/medsor/meds_temp/ogrenci_onem_k2/ham/<pdf>_sNN.json` (pdf: psk, noro, tbg, ftr):
```json
{"pdf":"psk","sayfa":1,"sayfa_ozeti":"Bipolar bozukluk: alt tipler, tanı kriterleri, prognoz, tedavi",
 "bloklar":[
  {"id":"psk-s01-b01","bolge":"r1c1","tur":"slayt|cikmis_soru|ogrenci_ozet|el_yazisi",
   "baslik":"Bipolar Bozukluğun Alt Tipleri",
   "ders":"k2-19","y25":{"key":"y25-k2-19-bipolar-bozukluk","sayfa":8},
   "basili_metin":"Slayttaki yazı, satır satır, düzeltilmiş",
   "isaretler":[{"tur":"sari|yesil|pembe|kirmizi_cizgi|daire|yildiz|unlem|ok|kutu|karalama","hedef":"işaretlenen ifade"}],
   "el_yazisi":[{"metin":"okunan el yazısı","hedef":"bağlandığı slayt ifadesi","guven":"yuksek|orta|dusuk","alternatif":"varsa"}],
   "cikmis":{"kok":"","siklar":["A) ...","B) ..."],"ogrenci_cevap":"E","banka_id":"","banka_yil":"","banka_dogru":"","tutarli":true,"not":""},
   "onem":["cikmis","sari","yildiz","el_onemli","el_cikmis","el_sorarim","tekrar"],
   "duzeltme":[{"ham":"","dogru":"","gerekce":""}]}
 ]}
```
`cikmis` yalnız çıkmış soru bloklarında; `y25` bulunamazsa null. Kimlik/konu belirsizse `ders`: "?" ve nedenini `sayfa_ozeti`'ne yaz.
Son olarak kısa rapor: sayfa başına blok/çıkmış/el yazısı sayısı, düşük güvenli okumalar, bulunamayan eşlemeler, gördüğün tıbbi hatalar.
Proje dosyalarına (meds/ altı) YAZMA; yalnız yukarıdaki çıktı klasörüne.
