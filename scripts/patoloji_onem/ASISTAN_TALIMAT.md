# Patoloji Sesli Sınav Asistanı v2 — derin, hiyerarşik anlatım + tüm sorular + "Yardım al" (alt ajan talimatı)

Çalışma klasörü: `/home/indu/medsor/meds_temp/patoloji_onem/asistan2/`

Öğrenci tam ekran bir asistanla çalışır. Asistan her dersi **bölüm bölüm**, slayttaki mantıksal akışla anlatır (EMA Lightning
Türkçe kadın sesi, metin harfi harfine okunur); her noktadan sonra o noktayla ilgili soruları sorar; yanlışta o şıkkın neden yanlış
olduğunu, neyi karıştırdığını ve doğrusunu öğretir; doğruda "Doğru" deyip ilerler. Öğrenci "Yardım al"a basarsa asistan **her şıkkı**
tek tek, kısa ve akılda kalıcı biçimde açıklar.

Kullanıcı geri bildirimi (v1 yetersiz bulundu): "Sığ metin olarak anlatınca neyi neden anlattığı anlaşılmıyor; belli bir hiyerarşiye
göre gitsin; neden anlatıldığı, ne işimize yaradığı, neden böyle bir şey olduğu anlaşılır olsun." Bu v2'nin ana hedefi budur.

## Kesin kurallar
1. **Tek kaynak ders PDF'i.** `../pdf_metin/<kod>.md` + plandaki madde alanları (`bilgi`, `alt`, `detay`, `neden` — PDF'ten üretildi) +
   2026-27 örnek sorularının `aciklama`sı (PDF'e dayalı). PDF'te olmayan tıbbi bilgi YAZMA. Şıktaki kavram PDF'te yoksa uydurma:
   "Bu, bu sorunun cevabı değil" de ve PDF'teki doğru bilgiyi öğret.
2. **Öğrenciye dönük dil:** "aday", "plan", "talimat", "PDF'te", "kaynakta", "ipucu" sözcükleri geçmez. Soru yılı/sınav adı/numarası okunmaz.
3. **Kronoloji:** bir soru, sorduğu bilgi anlatılmadan önce sorulmaz. Soru planda bağlı olduğu noktada kalır; bilgi daha sonraki bir
   noktada anlatılıyorsa soruyu o noktaya taşı (her soru tam bir kez yer alır).

## Hiyerarşi ve derinlik
- **Bölümler (3–8):** dersin slayt akışındaki ana başlıklar (ör. "Nefrotik sendrom nedir", "Çocukta: minimal değişiklik", "Erişkinde:
  FSGS ve membranöz", "Ayırıcı tanı"). Her bölümün `neden`i 1–2 cümle: bu bölüm neden önemli, sınavda/pratikte ne işe yarar, önceki
  bölümle bağı ne ("Tanımı bildik; şimdi hangi hastalık hangi yaşta, onu ayıralım, çünkü sorular buradan geliyor.").
- **Noktalar:** her bölüm 2–9 nokta, mantıksal sırayla (genelden özele, tanım → mekanizma → morfoloji → ayırıcı nokta → prognoz/tedavi).
  `zorunlu: true` noktaların HEPSİ yer alır. `zorunlu: false` (70–79 puan) noktalardan anlatıma değer katanları (bağlam kuran, ayırıcı
  tanıyı tamamlayan, sorunun anlaşılması için gerekli) seç; gereksizleri atla. Toplam nokta sayısı plandaki zorunlu sayısı + seçtiklerin.
- **Nokta anlatımı (`cumleler`, 3–7 cümle, 45–140 kelime):** sığ liste değil, anlam kuran anlatım:
  1. **Ne:** bilginin özü (en kritik terim `**kalın**`).
  2. **Neden / nasıl:** mekanizma, sebep–sonuç, "bu yüzden…" (PDF'te varsa).
  3. **Ne işe yarar / sınavda nasıl karşımıza çıkar:** ayırt edici nokta, karıştırılan komşu kavram ("Dikkat: … ile karıştırılır"),
     neden önemli olduğu.
  Aday noktalarda (plan `aday` dolu) bir kez "Burası çok önemli" ya da sıra 1 ise "Sınavda en olası soru buradan". "Dikkat" ders başına en çok 5.

## Çift biçim: `metin` (ekranda) ve `ses` (EMA okur)
Her cümle `{"metin": "...", "ses": "..."}`; aynı içerik, farklı yazım. `metin` normal yazım (kısaltma, sayı, simge serbest, `**kalın**`
serbest, parantez yok). `ses`:
- Kısaltmalar harf adlarıyla: "HPV" → "ha pe ve", "CD4" → "ce de dört", "TP53" → "te pe elli üç", "IgG" → "ig ge", "C1q" → "ce bir ku",
  "PSA" → "pe se a"; Türkçe açılımı yerleşikse açılım ("DCIS" → "duktal karsinoma in situ"). Kısaltmaya çekim eki gerekiyorsa açılımı yaz.
- Sayı/simge yazıyla: "%30" → "yüzde otuz", "1–7 yaş" → "bir ile yedi yaş", "≥" → "eşit ya da büyük". Rakam, %, /, →, ±, ≈, <, >, =, +,
  parantez, `*`, `#` YASAK. Yunan harfleri: alfa, beta, gama, kappa, lambda.
- Latince/İngilizce/özel adlar Türkçe okunuşla: "Helikobakter pilori", "Vilms", "Peycet", "Glison", "Tey Saks", "Kimelştil Vilson",
  "spayk end dom, yani çıkıntı ve kubbe".
- Nefes/durak: cümle sonu nokta (~0,45 sn). Vurgudan önce ` | ` (~0,3 sn), çok önemli bilgiden önce ` || ` (~0,7 sn); cümle başına en çok
  bir işaret. 25 kelimeden uzun ses cümlesini böl.

## Sorular (planda her noktanın `sorular` listesi: `anahtar`, `tur` cikmis | ornek26 | ornek, `kok`, `secenekler`, `dogru`, `aciklama?`)
Her soru için:
- `kok_ses`: kökün ses biçimi (şıkları okuma).
- `dogru`: `{"metin": "Doğru! …", "ses": "Doğru! …"}` — 1 pekiştirme cümlesi, en çok 30 kelime; neden doğru olduğunu söyler.
- `yanlis`: doğru şık DIŞINDAKİ her şık için `{metin, ses}`, 2–4 cümle, 15–60 kelime: şıktaki kavramla başla, neden yanlış, öğrenci neyi
  karıştırmış olabilir, "Doğrusu: …". Her açıklama o şıkka özgü.
- `yardim`: **TÜM şıklar** için (doğru dahil) `{metin, ses}`, her biri TEK kısa cümle, 5–20 kelime, akılda kalıcı hap bilgi.
  Yanlış şıkta neden yanlış ("Seminom radyoterapiye çok duyarlı, kötü prognoz değil."); doğru şıkta neden doğru ("Minimal değişiklik:
  çocukta bir numara, yüzde altmış beş."). Harfi okuma ("A şıkkı" deme); asistan harfleri kendisi söyler.

## Çıktı — `cikti/<kod>.json`
```json
{"kod": "21",
 "giris": [{"metin": "…", "ses": "…"}],
 "bolumler": [
  {"baslik": "Nefrotik sendrom nedir", "neden": {"metin": "…", "ses": "…"},
   "noktalar": [
    {"id": "21-07", "baslik": "Ekranda kısa başlık (en çok 8 kelime)",
     "cumleler": [{"metin": "…", "ses": "…"}],
     "sorular": [{"anahtar": "s3", "kok_ses": "…", "dogru": {…}, "yanlis": {"A": {…}}, "yardim": {"A": {…}, "B": {…}, …}}]}
   ]}
 ],
 "kapanis": [{"metin": "…", "ses": "…"}]}
```
- `giris` 1–2 cümle: dersin sınavdaki ağırlığı ve en çok sorulan 2–3 konu (yeni bilgi yok, "hoş geldin" yok).
- `kapanis` 2–4 cümle: akılda tutulacak 3–4 nokta.
- v1 çıktısı varsa (`../asistan/cikti/<kod>.json`) üslup için bakabilirsin; ama v2 daha derin ve hiyerarşik olmalı, soruların çoğu yeni.

## Bitiş
Her ders için `python3 dogrula.py cikti/<kod>.json` → **0 HATA** (uyarıları da gözden geçir). Yalnız `cikti/` altına yaz; geçici betikler
`/tmp/claude-1000/asistan2_<grup>/` altında (kendi alt klasörün). Yerel GPU/LLM yok. Son mesajında ders başına: bölüm/nokta/soru sayısı,
atladığın seçmeli noktalar (kısa gerekçe), emin olmadığın telaffuzlar.

## Pilot dersten notlar (örnek: `cikti/21.json` — derinlik, bölüm girişleri, yardım cümleleri için mutlaka incele)
- Ses biçiminde tek harfler de harf adıyla: "hepatit B" → "hepatit be", "T hücre" → "te hücre", "Faktör H" → "faktör ha";
  Romen rakamı: "Faktör I" → "faktör bir", "tip II" → "tip iki", "sınıf V" → "sınıf beş".
- Harfle okunan kısaltmadan sonra ek gerekiyorsa ünlü uyumuna dikkat et ya da açılımı yaz ("glomerülosklerozda", "fe se ge se'de" değil).
- Bir sorunun şıkları daha sonraki bir noktada anlatılan kavramlara dayanıyorsa soruyu o noktaya taşı (kronoloji).
- Seçmeli noktaları bağlam/ayırıcı tanı için kullan; noktayı bölümün mantığına göre yerleştir (slayt sırasından hafif sapma serbest).
- `yardim` her şık için TEK cümle: yanlışsa "neden değil", doğruysa "neden doğru" — sayı/anahtar kelimeyle akılda kalıcı.
