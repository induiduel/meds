# Soru çözücü — bağımsız denetim (ikinci göz) talimatı

Çalışma klasörü: `/home/indu/medsor/meds_temp/patoloji_ornek26/cozucu/`. Önce `TALIMAT.md`'yi oku (biçim ve kurallar aynı).
`cikti/<kod>.json` başka bir yazar tarafından üretildi ve biçim doğrulayıcısından geçti. Senin işin **tıbbi doğruluk ve
kaynağa sadakat denetimi**: öğrenci bu açıklamaları sesli dinleyip sınava girecek; tek bir yanlış bilgi kabul edilemez.

Her ders için PDF metnini (`/home/indu/medsor/meds_temp/patoloji_onem/pdf_metin/<kod>.md`) baştan sona oku, sonra her soruda:
1. **Anahtar:** `dogru` şık PDF'e göre gerçekten doğru ve tek doğru mu? Kök PDF'teki ifadeyle çelişiyor mu? (Örn. "en sık", "en erken",
   "hangisi değildir" kalıplarını PDF'teki ifadeyle birebir karşılaştır.) Sorun varsa en küçük düzeltmeyi yap; `kontrol` alanını
   `{"durum": "duzeltildi", "not": "…, PDF s. n"}` yap (önceki yazar zaten düzelttiyse notu güncelle). Kaynak sorudan farklıysa durum
   "duzeltildi" olmak zorunda.
2. **Her `siklar` açıklaması, `ipucu` ve `cozum`:** her önerme PDF'te var mı? Sayı, yüzde, yaş, gen, boya, hücre, organ adları PDF'le
   birebir mi? Kitap bilgisi / PDF'te olmayan ayrıntı / yanlış genelleme varsa düzelt ya da çıkar. Bir şıkkın kavramı PDF'te hiç yoksa
   o kavram hakkında iddia bulunmamalı ("X bu sorunun cevabı değil; …").
3. **Ses biçimi:** `ses` alanı `metin` ile aynı bilgiyi mi taşıyor (eksik/fazla bilgi, yanlış okunuş)? Kısaltma okunuşları doğal mı
   ("de ne a", "ha pe ve"), Latince terimler Türkçe okunuşla mı? `secenek_ses` şıkla aynı mı?
4. **İpucu** cevabı açık etmiyor mu (eşanlamlı ya da tanımla doğrudan söyleme de sızıntıdır)? Gerçekten düşündürüyor mu?
5. Öğrenciye dönük dil, kısalık: TALIMAT'taki sınırlar.

Düzeltmeyi doğrudan `cikti/<kod>.json` üzerinde yap (Python json ile oku/yaz, `ensure_ascii=False`, `indent=1`). Sonra
`python3 dogrula.py cikti/<kod>.json` → 0 HATA. Başka dosyaya dokunma; yerel GPU/LLM yok.

Son mesajında ders başına: incelenen soru sayısı, değiştirdiğin her öğe (`<kod> s<no> <alan>`: eski → yeni, kısa gerekçe + PDF
sayfası). Değişiklik yoksa "değişiklik yok" yaz.
