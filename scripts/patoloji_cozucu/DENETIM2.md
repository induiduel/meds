# Soru çözücü 2. tur — bağımsız denetim (ikinci göz) talimatı

> ⚠️ **Şık açıklama standardı (ZORUNLU, 2026-10-18):** her şık açıklaması kavramın ne olduğunu, ne işe yaradığını ve bu soruyla
> bağını anlatır; "bu sorunun cevabı değil / … olarak geçmez" gibi geçiştirme HATA'dır. Ayrıntı ve kaynak sırası: `meds/docs/SIK_ACIKLAMA_STANDARDI.md`.
> ⚠️ **Türkçe üslup standardı (ZORUNLU, 2026-10-18):** metin doğal, eksiksiz ve anlaşılır Türkçe olur; çeviri mecaz ("imzası",
> "motoru", "freni") ve iç etiket ("Ayrım cümlesi:", "Akılda tut:", "Mantığı şudur:") YASAK. Ayrıntı: `meds/docs/TURKCE_USLUP_STANDARDI.md`.

Çalışma klasörü: `/home/indu/medsor/meds_temp/patoloji_ornek26/cozucu/`. Önce `TALIMAT.md`, `TALIMAT2.md` ve `DENETIM.md`'yi oku.
İki iş yapacaksın; ikisi de aynı derste.

## 1) Yeni içerik denetimi — `cikti2/<kod>.json` (`yeni` benzer sorular + `cikmis` çıkmış sorular)
Başka bir yazar üretti, biçim doğrulayıcısından geçti. Öğrenci bunları sesli dinleyip sınava girecek; tek yanlış bilgi kabul edilmez.
PDF metnini (`/home/indu/medsor/meds_temp/patoloji_onem/pdf_metin/<kod>.md`) baştan sona oku, sonra her soruda:
- **Yeni sorular:** anahtar PDF'e göre tartışmasız tek doğru mu? Başka şık da savunulabilir mi, eşanlamlı iki şık var mı, kök belirsiz
  mi? Bilgi PDF'te açıkça var mı (kitap bilgisi yok)? Tablo/şekil okumaya ya da klinik bulguya dayanıyor mu (yasak)? Gerçekten
  orta-zor mu ve sınav için önemli bir bilgiyi mi soruyor? `girdi2/<kod>.json` → `mevcut` sorularla aynı bilgiyi mi soruyor? Sorunluysa
  soruyu düzelt ya da aynı `onem` maddesinden yeni, doğru bir soruyla değiştir (sayı `yeni_soru_sayisi` kalmalı).
- **Çıkmış sorular:** kök/şık/anahtar adaydan birebir mi (değiştirme!)? Anahtar PDF'le çelişiyorsa ya da soru PDF kapsamı dışındaysa
  soruyu çıkar, `elenen_cikmis`e gerekçesiyle ekle ve uygunsa `girdi2`'deki başka bir adayla değiştir (en çok 5, birbirinden farklı).
  Seçilenler aynı bilgiyi soruyorsa birini değiştir.
- **Açıklamalar** (ipucu, siklar, cozum): her önerme PDF'te var mı; sayılar birebir mi; ipucu cevabı (eşanlamlı ya da tanımla) sızdırıyor
  mu; doğru şık açıklaması gerçekten doğru gerekçe mi; `ses` `metin` ile aynı bilgiyi mi taşıyor?

## 2) Okunuş düzeltmesi — `cikti/<kod>.json` (mevcut örnek soruların YALNIZ `ses`, `kok_ses`, `secenek_ses` alanları)
Seslendirme motoru kısaltmayı kelime gibi okuyunca öğrenci yanlış duyuyor ("anka", "sin", "pekam", "nos", "malt"). TALIMAT2'deki
"Kısaltma okunuşu" kuralını hem `cikti2` hem `cikti` ses alanlarına uygula: kısaltma harf harf, Türkçe harf adlarıyla, boşlukla ayrık
(ANCA → "a ne ce a", CIN → "ce i ne", PECAM → "pe e ce a me", eNOS → "e ne o se", MALT → "me a le te"); yerleşik istisnalar yalnız
TALIMAT2'deki listedekiler. Türkçe/Latince tam açılımla okunanlar (FSGS → "fokal segmental glomerüloskleroz") doğrudur, dokunma.
`okunus_aday/<kod>.txt` makinenin bulduğu adayları listeler (yanlış pozitif olabilir); ayrıca tüm ses alanlarını kendin tara.
`cikti/<kod>.json`'da `metin`, `soru`, `secenekler`, `dogru`, `kontrol` ve açıklamaların içeriğine DOKUNMA (yalnız ses yazımı).

Kontrol aracı: `python3 /home/indu/medsor/meds/scripts/patoloji_cozucu/okunus_denet.py cikti/<kod>.json cikti2/<kod>.json` — metinde
geçip seste harf harf yazılmamış kısaltmaları listeler (açılımla okunanlar burada da görünür; onlar doğru).

## Bitiş
`python3 dogrula.py cikti/<kod>.json` ve `python3 dogrula2.py cikti2/<kod>.json` → ikisi de 0 HATA. JSON'u Python ile oku/yaz
(`ensure_ascii=False`, `indent=1`). Yalnız kendi derslerinin `cikti/<kod>.json` ve `cikti2/<kod>.json` dosyalarını değiştir; geçici
dosyalar `/tmp/claude-1000/denetim2_<grup>/`. Yerel GPU/LLM yok. Son mesajında ders başına: değiştirdiğin her öğe (kısa gerekçe + PDF
sayfası), değiştirilen/elenen çıkmışlar, düzelttiğin okunuşların sayısı ve örnekleri.
