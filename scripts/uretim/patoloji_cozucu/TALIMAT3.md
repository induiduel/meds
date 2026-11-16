# Soru çözücü — 3. tur: canlı ders konularından yeni sorular (alt ajan talimatı)

> ⚠️ **Şık açıklama standardı (ZORUNLU, 2026-10-18):** her şık açıklaması kavramın ne olduğunu, ne işe yaradığını ve bu soruyla
> bağını anlatır; "bu sorunun cevabı değil / … olarak geçmez" gibi geçiştirme HATA'dır. Ayrıntı ve kaynak sırası: `meds/docs/SIK_ACIKLAMA_STANDARDI.md`.
> ⚠️ **Türkçe üslup standardı (ZORUNLU, 2026-10-18):** metin doğal, eksiksiz ve anlaşılır Türkçe olur; çeviri mecaz ("imzası",
> "motoru", "freni") ve iç etiket ("Ayrım cümlesi:", "Akılda tut:", "Mantığı şudur:") YASAK. Ayrıntı: `meds/docs/TURKCE_USLUP_STANDARDI.md`.

Çalışma klasörü: `/home/indu/medsor/meds_temp/patoloji_ornek26/cozucu/`. Önce `TALIMAT.md` ve `TALIMAT2.md`'yi baştan sona oku:
açıklama alanları (`kok_ses`, `secenek_ses`, `ipucu`, `siklar`, `cozum`, `sayfa`), çift biçim (`metin`/`ses`), öğrenciye dönük dil,
uzunluklar ve **TALIMAT2'deki "Kısaltma okunuşu"** AYNEN geçerli. Bu belge yalnız yeni işi anlatır.

## Girdi — `girdi3/<kod>.json`
- `canli_metin`: dersin "Canlı ders" konuşma metni (öğrencinin sesli dinlediği anlatım; `@@ Başlık` bölümleri). Baştan sona oku.
  Soruların KONUSU buradan seçilir: canlı derste anlatılan, vurgulanan ("aklınızda tutun", "sınavda", "ayırt edici", "en sık",
  "karıştırmayın") konular.
- PDF metni `/home/indu/medsor/meds_temp/patoloji_onem/pdf_metin/<kod>.md` — **bilgi doğruluğunun tek ölçütü**. Soruya giren her bilgi
  (anahtar, çeldirici gerekçesi, sayı) PDF'te de açıkça geçmeli. Canlı metinde olup PDF'te olmayan (anlatım için eklenmiş benzetme,
  genelleme) bilgiyle soru YAZMA. `sayfa` PDF sayfasıdır.
- `mevcut`: dersin şu anki tüm soruları (örnek + benzer + çıkmış; kök + doğru cevap). Yeni sorular bunların sorduğu bilgiyi TEKRAR
  SORMAMALI (tersini sorma, eşanlamlısıyla sorma). Mevcutların kapsamadığı konulara/ayrıntılara git.
- `onem`: sınav önem maddeleri (puan, aday). Önceliklendirmede kullan; `onem_id` istersen yaz (zorunlu değil).
- `yeni_soru_sayisi`: hedef. 5–30 arası olmak koşuluyla, mevcutla çakışmayan kaliteli konu kalmadıysa ±3 sapabilirsin (son mesajda
  gerekçe yaz). Sayıyı doldurmak için zayıf/önemsiz soru yazma.

## Ne tür soru — kalite
- Konunun ÖZÜ, kazanıma uygun: önemli, karakteristik, ayırt edici, dikkat çekici bilgi (patognomonik bulgu, tanımlayıcı morfoloji,
  mekanizma–sonuç, en sık/en önemli/ilk, iki komşu kavramın ayırıcı noktası, sınıflama ölçütü, prognoz belirleyicisi).
- Canlı dersin bölümlerine YAYIL: aynı bölümden en çok 3 soru; her önemli bölümden en az 1.
- Hocanın 2026-27 örnek soruları üslubu: kısa kök (en çok 1–2 cümle), 5 kısa şık (1–6 kelime), tek doğru, çeldiriciler aynı kategoriden,
  derste öğretilmiş komşu kavramlar (en az 2 güçlü çeldirici). "Hangisi yanlıştır/değildir/beklenmez" kökleri en çok %30.
- Zorluk: ağırlıkla orta ve zor; en çok %20 kolay (`zorluk`: "kolay" | "orta" | "zor").
- YASAK: tablo/şekil okumaya dayalı soru; klinik bulgu (semptom/muayene) sorusu; eşanlamlı iki şık; PDF'e göre ikinci savunulabilir şık;
  tarih/kişi adı gibi önemsiz ezber (konunun özü değilse).
- Doğru harfleri A–E dengeli (hiçbiri %35'i geçmez).

## Çıktı — `cikti3/<kod>.json`
```json
{"kod": "02", "yeni": [{"canli_bolum": "<canlı metindeki @@ başlığı, birebir>", "onem_id": "02-07", "zorluk": "zor",
  "soru": "…", "secenekler": {"A": "…", …}, "dogru": "B", "kok_ses": "…", "secenek_ses": {…},
  "ipucu": {…}, "siklar": {…}, "cozum": {…}, "sayfa": [n]}]}
```
Bitiş: `python3 dogrula3.py cikti3/<kod>.json` → 0 HATA (UYARI'ları incele; PDF'te olmayan sayı = büyük olasılıkla hata). Yalnız
`cikti3/<kod>.json` yaz; geçici dosyalar `/tmp/claude-1000/cozucu3_<grup>/`. Yerel GPU/LLM yok. Son mesajında ders başına: soru sayısı
(kolay/orta/zor), kapsanan bölümler, hedeften sapma gerekçesi, emin olmadığın okunuşlar. Kısa yaz.
