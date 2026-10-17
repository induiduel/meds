# Soru çözücü 3. tur — bağımsız denetim (ikinci göz)

Çalışma klasörü: `/home/indu/medsor/meds_temp/patoloji_ornek26/cozucu/`. Önce `TALIMAT.md`, `TALIMAT2.md` (Kısaltma okunuşu),
`TALIMAT3.md` ve `DENETIM.md`'yi oku. `cikti3/<kod>.json`'u başka bir yazar canlı ders metninden üretti, biçim doğrulayıcısından geçti.
Öğrenci bunları sesli dinleyip sınava girecek; tek yanlış bilgi kabul edilmez.

PDF metnini (`/home/indu/medsor/meds_temp/patoloji_onem/pdf_metin/<kod>.md`) ve `girdi3/<kod>.json` → `canli_metin` dosyasını oku.
Her soruda:
- Anahtar PDF'e göre tartışmasız tek doğru mu? Başka şık savunulabilir mi, eşanlamlı şık var mı, kök belirsiz mi?
- Bilgi PDF'te açıkça var mı (canlı metindeki benzetme/genelleme ya da kitap bilgisi değil)? Sayılar PDF'le birebir mi?
- Tablo/şekil ya da klinik bulguya mı dayanıyor (yasak)? Konunun özünü mü soruyor, yoksa önemsiz ezber mi? Zorluk etiketi doğru mu?
- `girdi3` → `mevcut` sorulardan biriyle aynı bilgiyi (tersini/eşanlamlısını) mı soruyor? Yeni sorular birbirini tekrar ediyor mu?
- Açıklamalar: her önerme PDF'te mi; ipucu cevabı eşanlamlı/tanımla sızdırıyor mu; doğru şık açıklaması gerçek gerekçe mi; `ses` ile
  `metin` aynı bilgi mi; kısaltmalar seste harf harf mi (`python3 /home/indu/medsor/meds/scripts/patoloji_cozucu/okunus_denet.py cikti3/<kod>.json`).
Sorunlu soruyu düzelt ya da aynı bölümden yeni, doğru bir soruyla değiştir; zayıf soru varsa güçlüsüyle değiştir.

Bitiş: `python3 dogrula3.py cikti3/<kod>.json` → 0 HATA. JSON'u Python ile oku/yaz (`ensure_ascii=False`, `indent=1`). Yalnız kendi
derslerinin `cikti3/<kod>.json` dosyasını değiştir; geçici dosyalar `/tmp/claude-1000/denetim3_<grup>/`. Yerel GPU/LLM yok. Son mesajında
ders başına: değiştirdiğin öğeler (kısa gerekçe + PDF sayfası), düzelttiğin okunuş sayısı. Kısa yaz.
