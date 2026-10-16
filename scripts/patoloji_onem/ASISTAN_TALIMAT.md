# Patoloji Sesli Sınav Asistanı — anlatım ve geri bildirim metni (alt ajan talimatı)

Çalışma klasörü: `/home/indu/medsor/meds_temp/patoloji_onem/asistan/`

Öğrenci tam ekran bir asistanla çalışacak: asistan her dersin sınavdaki en önemli noktalarını **kısaca** anlatır (EMA Lightning
Türkçe kadın sesiyle, metin harfi harfine okunur), önemli yerlerde soru sorar; öğrenci yanlış şıkkı seçerse **neden yanlış
olduğunu, neyi karıştırdığını ve doğrusunu** öğretir, doğru seçerse "Doğru" deyip kısa bir pekiştirmeyle sonraki noktaya geçer.

## Kesin kurallar
1. **Tek kaynak ders PDF'i.** `../pdf_metin/<kod>.md` (Kurul 1 Tıbbi Patoloji ders PDF'inin sayfa metni) ve plandaki madde alanları
   (`bilgi`, `alt`, `detay`, `neden` — zaten PDF'ten üretildi). PDF'te olmayan tıbbi bilgi YAZMA; kendi tıp bilgini, kitap bilgisini ekleme.
   Yanlış şık açıklamasında şıktaki kavram PDF'te geçmiyorsa uydurma: "Bu şık bu sorunun cevabı değil" deyip PDF'teki doğru bilgiyi öğret.
2. **Sınava odaklı, kısa, anlaşılır.** Her adım 2–5 cümle, toplam 25–90 kelime. Giriş cümlesi tekrarı, "bu derste", "şimdi göreceğiz",
   ders/hoca tanıtımı YOK. Doğrudan bilginin özüne gir: ne soruluyor, ayırt edici nokta, karıştırılan kavram.
3. **Vurgu:** sınavda en kritik terim ekranda `**kalın**`. Aday adımlarında (plan `aday` dolu) bir kez "Burası çok önemli" ya da
   "Sınavda en olası soru buradan" de (yalnız bu adımlarda, sınav adayı sırası 1 ise "en olası soru"). Diğer adımlarda en fazla
   ders başına 3 kez "Dikkat" ile karıştırılan kavramı vurgula.
4. **Öğrenciye dönük dil:** "aday", "plan", "talimat", "PDF'te", "kaynakta", "madde", "ipucu" sözcükleri metinde geçmez. Soru yılı,
   sınav adı, soru numarası okunmaz.

## Çift biçim: `metin` (ekranda) ve `ses` (EMA okur)
Her cümle `{"metin": "...", "ses": "..."}` çiftidir; ikisi **aynı içerik**, yalnız yazım farklı. Ekranda o an okunan cümle vurgulanır.
- `metin`: normal Türkçe yazım; kısaltma, sayı, simge serbest (`HPV`, `%30`, `≥`, `CD4`). `**kalın**` serbest. Parantez kullanma.
- `ses`: seslendirme metni (harfi harfine okunur):
  - **Kısaltmalar harf adlarıyla ayrık:** "HPV" → "ha pe ve", "CD4" → "ce de dört", "TP53" → "te pe elli üç", "BRCA1" → "be er ce a bir",
    "PSA" → "pe se a", "ER/PR" → "e er ve pe er", "HER2" → "her iki" (yerleşik okunuşu), "DCIS" → "duktal karsinoma in situ" (açılımı
    Türkçe biliniyorsa açılımı yaz). Kelime gibi okunanlar okunuşuyla: "RAS" → "ras".
  - **Sayılar ve simgeler yazıyla:** "%30" → "yüzde otuz", "1/300" → "üç yüzde bir", "≥" → "eşit ya da büyük", "5 yıl" → "beş yıl",
    "↑" → "artmış". Rakam (0–9), %, /, →, ±, ≈, <, >, =, +, parantez, köşeli parantez, `*`, `#`, `|` (aşağıdaki durak işareti hariç) YASAK.
  - **Yunan harfleri:** α alfa, β beta, γ gama, κ kappa, λ lambda.
  - **Latince/İngilizce terimler Türkçe okunuşla:** "Helicobacter pylori" → "Helikobakter pilori", "in situ" → "in situ",
    "Chlamydia trachomatis" → "Klamidya trakomatis", "Wilms" → "Vilms", "seminoma" → "seminom", "Gleason" → "Glison",
    "Paget" → "Peycet", "peau d'orange" → "po doranj". Yerleşik Türkçe tıp yazımı ("adenokarsinom", "glomerülonefrit").
  - **Nefes ve duraklar:** cümle sonu nokta ile biter (otomatik ~0,45 sn durak). Cümle içinde vurgudan önce kısa durak için ` | `
    (~0,3 sn), çok önemli bilgiden önce uzun durak için ` || ` (~0,7 sn) kullan — ölçülü: cümle başına en çok bir işaret.
    Virgülü doğal nefes yerlerine koy; 25 kelimeden uzun cümleyi ikiye böl.
  - Vurgu için ses tarafında terimi gerekirse yinele ya da "yani" ile açıkla; büyük harf ya da `**` kullanma.

## Girdi — `plan/<kod>.json`
`{kod, no, baslik, pdf, pdf_metin, ozet, adimlar: [{id, puan, aday, baslik, bilgi, alt, detay, neden, sayfalar, kategori, soru}]}`
`soru` doluysa: `{anahtar, tur: "cikmis"|"ornek", kok, secenekler, dogru, aciklama?}`. Adım sırası ve sorular SABİT (değiştirme).
Her adımı yazmadan önce `sayfalar`daki PDF sayfalarını oku; anlatım plandaki maddeden taşmasın ama PDF'teki bağlamla anlaşılır olsun.

## Çıktı — `cikti/<kod>.json`
```json
{"kod": "21",
 "giris": [{"metin": "…", "ses": "…"}],
 "adimlar": [
  {"id": "21-03", "baslik": "Ekranda kısa başlık (en çok 8 kelime)",
   "cumleler": [{"metin": "…", "ses": "…"}],
   "soru": {
     "kok_ses": "Soru kökünün ses biçimi (kökü aynen; şıkları okuma)",
     "dogru": {"metin": "Doğru! …", "ses": "Doğru! …"},
     "yanlis": {"A": {"metin": "…", "ses": "…"}, "B": {…}}
   }}
 ],
 "kapanis": [{"metin": "…", "ses": "…"}]
}
```
- `giris`: 1–2 cümle; dersin sınavdaki ağırlığı ve en çok sorulan 1–2 konu (yalnız plan/PDF'e dayanarak). "Hoş geldin" yok.
- `adimlar`: plandaki HER adım, aynı sırada, aynı `id`.
- `soru` yalnız planda soru olan adımda. `yanlis`: doğru şık DIŞINDAKİ her şık için bir kayıt (harfler planla aynı).
  - Yanlış açıklaması 2–4 cümle, en çok 70 kelime: (1) bu şıkkın neden yanlış olduğu, (2) öğrencinin neyi karıştırmış olabileceği
    (komşu kavram), (3) "Doğrusu: …" ile doğru cevap ve gerekçesi. İlk cümle "Bu şık yanlış." gibi kuru başlamasın; doğrudan şıktaki
    kavramla başla (ör. "Seminom radyoterapiye çok duyarlıdır, bu yüzden kötü prognozlu değildir.").
  - `dogru`: "Doğru!" ile başlar + 1 pekiştirme cümlesi (en çok 30 kelime).
  - "Hayır / bir daha düşün" gibi tekrar kalıpları kullanma; her açıklama o şıkka özgü olsun.
- `kapanis`: 2–3 cümle; dersin sınav için akılda tutulacak 2–3 noktası (yeni bilgi yok).

## Bitiş
Her ders için `python3 dogrula.py cikti/<kod>.json` → **0 HATA** (uyarıları da gözden geçir). Yalnız `cikti/` altına yaz; geçici betikler
`/tmp/claude-1000/asistan_<ajan>/` altında. Yerel GPU/LLM yok. Son mesajında ders başına: adım/soru sayısı ve emin olmadığın telaffuzlar.

## Pilot dersten notlar (örnek: `cikti/05.json`, `cikti/21.json` — üslup ve uzunluk için oku)
- Ses biçiminde kısaltmaya çekim eki gerekirse ("FSGS'de") harf okunuşuna kesme koyma; açılımı yaz ("fokal segmental glomerülosklerozda").
- Karışık harfli kısaltmalar da harfle: "IgG" → "ig ge", "C1q" → "ce bir ku", "PLA2R" → "pe le a iki er", "mRNA" → "em er en a".
- Özel adlar okunuşla: "Tey Saks" (Tay-Sachs), "Niman Pik", "Rasel" (Russell), "Malori Denk", "Peycet" (Paget), "Kimelştil Vilson".
- İngilizce terim gerekiyorsa okunuşla yaz ve hemen Türkçesini ver: "spayk end dom, yani çıkıntı ve kubbe".
- Şıktaki kavram PDF'te yoksa: "Bu, bu sorunun cevabı değil" de, şıkkı tanımlamaya kalkma; PDF'teki doğru bilgiyi öğret.
