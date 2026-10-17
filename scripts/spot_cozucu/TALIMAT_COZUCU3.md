# Branş soru çözücü — 3. tur: canlı ders konularından yeni örnek sorular (yazar ajan talimatı)

Çalışma klasörü: `/home/indu/medsor/meds_temp/spot_cozucu/<brans>/`. Önce şunları baştan sona oku ve aynen uygula:
- `/home/indu/medsor/meds/scripts/spot_cozucu/TALIMAT_COZUCU.md` — alanlar (`kok_ses`, `secenek_ses`, `ipucu`, `siklar`, `cozum`, `sayfa`),
  çift biçim (`metin`/`ses`), öğrenciye dönük dil, uzunluklar, okunuş.
- `/home/indu/medsor/meds_temp/patoloji_ornek26/cozucu/TALIMAT2.md` yalnız "Kısaltma okunuşu" bölümü (harf harf, Türkçe harf adları:
  L "le", R "re", S "se", F "fe", W "çift ve"; seste kesme işaretli ek yok: "ce de dördün").
- `/home/indu/medsor/meds_temp/patoloji_ornek26/cozucu/TALIMAT3.md` — 3. turun kalite kuralları (bu belge yalnız yol farklarını söyler).

## Girdi — `girdi3/<kod>.json`
- `canli_metin`: dersin canlı ders konuşma metni (`@@ Başlık` bölümleri) — soruların KONUSU buradan (vurgulanan, ayırt edici, en sık…).
- `pdf_metin` (= `pdf_metin/<kod>.md`): **bilgi doğruluğunun tek ölçütü**; her bilgi PDF'te açıkça geçmeli. Canlı metinde olup PDF'te
  olmayan bilgiyle soru YAZMA. `sayfa` PDF sayfasıdır.
- `mevcut`: dersin şu anki tüm soruları (örnek + çıkmış). Aynı bilgiyi (tersini/eşanlamlısını) tekrar sorma.
- `onem`: önem maddeleri (öncelik için; `onem_id` istersen yaz).
- `yeni_soru_sayisi`: hedef; 5–30 içinde, kaliteli konu kalmadıysa ±3 sapabilirsin (gerekçe yaz). Zayıf soruyla doldurma.

## Ek kesin kurallar (hocaların sınav kuralı)
- **Tablo, şekil, resim ya da şekil altyazısında YALNIZCA geçen bilgiyle soru YOK** (anahtar ve çeldirici gerekçesi metin gövdesinde
  geçmeli). Klinik bulgu (semptom/muayene) sorusu yok; tanı/tedavi/korunma/epidemiyoloji/mekanizma sorulabilir (PDF'te açıksa).
- Çeldiriciler derste/PDF'te geçen komşu kavramlardan; PDF'te hiç geçmeyen kavramı çeldirici yapma.
- Bir bölümden en çok 3 soru; önemli bölümlerin her birinden en az 1. Kolay en çok %20, "hangisi yanlıştır" en çok %30.

## Çıktı — `cozucu3/<kod>.json`
```json
{"kod": "e02", "yeni": [{"canli_bolum": "<@@ başlığı birebir>", "onem_id": "e02-07", "zorluk": "orta",
  "soru": "…", "secenekler": {"A": "…", …}, "dogru": "B", "kok_ses": "…", "secenek_ses": {…},
  "ipucu": {…}, "siklar": {…}, "cozum": {…}, "sayfa": [n]}]}
```
Bitiş: `python3 /home/indu/medsor/meds/scripts/spot_cozucu/cozucu_dogrula3.py cozucu3/<kod>.json` → 0 HATA (UYARI'ları incele). Okunuş:
`python3 /home/indu/medsor/meds/scripts/patoloji_cozucu/okunus_denet.py cozucu3/<kod>.json`. Yalnız `cozucu3/<kod>.json` yaz; geçici
dosyalar `/tmp/claude-1000/cozucu3_<brans>_<grup>/`. Yerel GPU/LLM yok. Son mesaj kısa: ders başına sayı (kolay/orta/zor), sapma gerekçesi,
emin olmadığın okunuşlar.
