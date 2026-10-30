# Yargıç yönergesi: öğrenci notu bu çıkmış sorunun bilgisini içeriyor mu?

Bağlam: Dönem 3 Kurul 2 için bir öğrenci 2025-26 ders slaytlarından önemli yerleri kesip not yapmış (el yazısı + vurgu).
Bu notların gerçek çıkmış soruları ne kadar yakaladığını ölçüyoruz. Her soru için tarafsız karar ver; nota iyi davranmaya çalışma.

Girdi: `parti_NN.json` → her kayıt: `kok`, `siklar`, `dogru`, `aday_birimler` (notun o soruya en yakın 4 birimi: başlık | basılı
slayt metni | el yazısı), `arsiv_sayfalari` (2025-26 ders PDF'inde soruya en yakın 2 sayfanın metni).
Notun o derse ait bütün birimleri: `/home/indu/medsor/meds/src/data/ogrenci_onem/<ders>.json` → `birimler[]` (`metin`, `el_yazisi[].metin`).
"yok" demeden önce doğru şıkkın anahtar terimini (ör. "Nöronopati", "SCA8", "Turner") bu dosyada `grep -i` ile ara.

Karar:
- **tam**: sorunun ölçtüğü belirleyici bilgi (doğru şıkkı seçtiren bilgi) notta açıkça var — yalnız bu notu çalışan öğrenci doğru cevabı bulabilir.
- **kismi**: konu notta var ama belirleyici bilgi eksik ya da yalnız bir parçası var (ör. hastalık geçiyor, sorulan özelliği yok).
- **yok**: notta yok.
- **slaytta**: sorunun bilgisi 2025-26 ders slaytında var mı? `arsiv_sayfalari` metnine bak; metin boşsa ve konu dersin konusuysa `true`
  say. Soru açıkça başka dersin içeriğiyse (ör. Nörolojik Muayene etiketli Brodmann alanı / serebellar çekirdek anatomisi) `false`.
- `birim`: bilgiyi taşıyan birim kimliği (tam/kismi'de), yoksa null.

Çıktı: aynı klasöre `yargi_NN.json` (parti numarasıyla aynı), JSON liste:
`[{"id": "...", "karar": "tam|kismi|yok", "slaytta": true, "birim": "psk-s04-b03" | null, "gerekce": "≤20 kelime"}]`
Her soruya tam bir kayıt. Proje dosyalarına yazma.
