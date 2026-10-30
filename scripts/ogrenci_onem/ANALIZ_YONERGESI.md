# Ders analizi yönergesi (öğrenci önem notu → tam içerik işçisi malzemesi)

Amaç: tam içerik işçisi bir Kurul 2 dersini yazarken **neyi ne kadar vurgulayacağını, nerede ayrıntıya gireceğini ve
örnek soruları hangi konulara yığacağını** bilsin. Kaynak: 2025-26 öğrencilerinin derleme notu (slayttan kesilmiş en önemli
yerler, el yazısı, vurgu, yapıştırılmış çıkmışlar) + çıkmış bankasıyla eşleşme. Analiz bu veriden çıkar; **uydurma yok**.

## Girdi
- `src/data/ogrenci_onem/<ders>.json`: `birimler[]` (A/B/C öncelik, `puan`, `sinyal`, `metin` = slayt yazısı, `el_yazisi[]`,
  `vurgulu[]`, `ogrenci_sorulari`, `banka_cikmis`, `duzeltme[]`, `y25`/`y26` sayfa), `ogrenci_sorulari[]` (notta yapıştırılmış
  çıkmışlar: kök, şıklar, öğrenci cevabı, banka id, `tutarli`), `banka[]` (bankadaki Kurul 2 çıkmışları, `kapsandi`, `yillar`).
- Ders kaydı: `src/data/dersler/k2.json`. Hoca üslubu (varsa): `python3 scripts/hoca_profili/profil_oku.py --ders "<branş>" --konu "<konu>"`.
- Yalnız gerekirse: ham sayfa okuması `data/ogrenci_onem/ham/<pdf>_sNN.json`.

## Çıktı: `data/ogrenci_onem/analiz/<ders>.json`
```json
{"ders": "k2-19",
 "ozet": "2–4 cümle: sınavda bu dersin çekirdeği; öğrenciler neye yığılmış; çıkmışlar hangi konuya düşmüş.",
 "temalar": [
  {"tema": "Bipolar I / II / siklotimi ayrımı", "oncelik": "A", "birimler": ["psk-s01-b02"],
   "kanit": "notta 2 çıkmış (2020-21, 2025-26) + yıldız + el notu: 'Bipolar I için tek mani atağı yeter'",
   "anlatim": "Ne kadar ve nasıl anlatılmalı (1–2 cümle): hangi ayrıntı, hangi karşılaştırma, hangi sayı.",
   "soru_payi": 20,
   "soru_tipleri": ["ayırıcı: hipomani 4 gün / mani 1 hafta", "yanlış bul: siklotimide süre"]}],
 "hoca_kaliplari": ["'… hangisi yanlıştır' (5 sorunun 3'ü)", "öncüllü (I–IV)"],
 "tuzaklar": [{"tuzak": "Siklotimide süre en az 2 yıl", "neden": "çeldiricide 1 yıl ya da 6 ay verilir"}],
 "sayilar": ["Bipolar yaygınlık %1–5", "Başlangıç 15–24 yaş"],
 "duzeltmeler": [{"yanlis": "…", "dogru": "…", "kaynak": "slayt s.8 / bankadaki doğru şık / genel tıbbi bilgi"}],
 "ara_soru_adaylari": [{"birim": "psk-s01-b05", "fikir": "mani epizodu için süre + işlev kaybı ölçütü"}],
 "kurul2627_notu": "2026-27 slaytı gelince bakılacak: … (konu çıkarılmış/eklenmiş olabilir)"}
```
Kurallar:
1. `temalar` dersin TÜM A ve B birimlerini kapsar; C birimleri tek bir "diğer seçilen yerler" temasında toplanabilir. Soru payları
   toplamı 100. Pay, kanıt gücüne göre: çıkmış (özellikle birden çok yıl/yakın yıl) > yıldız/el notu > yalnız vurgu.
2. Bankada notta OLMAYAN ama sorulmuş çıkmışlar (`banka[]` içinde `kapsandi: false`) ayrı tema olur: "Notta yok, sorulmuş".
   Öğrencinin kaçırdığı yer de işçi için önemlidir.
3. `duzeltmeler`: birimlerdeki `duzeltme` ve `tutarli: false` çıkmışlardan **tıbbi anlamı olanlar** (yazım hataları değil).
   Öğrenci notu ile slayt çelişiyorsa slayt; slayt ile bankadaki doğru şık çelişiyorsa ikisini de yaz, gerekçeyle.
4. `kanit` alanı somut: kaç çıkmış, hangi yıl, hangi işaret, hangi el notu (kısa alıntı).
5. Türkçe üslup: doğal, açık Türkçe; çeviri mecaz ("imzası", "motoru", "çapası") ve iç etiket ("Akılda tut:") yok.
6. Tıbbi bilgi yalnız girdideki slayt metni, el notu (düzeltilmiş), çıkmış soru ve doğru şıktan gelir.
