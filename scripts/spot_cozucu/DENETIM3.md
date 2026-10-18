# Branş soru çözücü 3. tur — bağımsız denetim

> ⚠️ **Şık açıklama standardı (ZORUNLU, 2026-10-18):** her şık açıklaması kavramın ne olduğunu, ne işe yaradığını ve bu soruyla
> bağını anlatır; "bu sorunun cevabı değil / … olarak geçmez" gibi geçiştirme HATA'dır. Ayrıntı ve kaynak sırası: `meds/docs/SIK_ACIKLAMA_STANDARDI.md`.
> ⚠️ **Türkçe üslup standardı (ZORUNLU, 2026-10-18):** metin doğal, eksiksiz ve anlaşılır Türkçe olur; çeviri mecaz ("imzası",
> "motoru", "freni") ve iç etiket ("Ayrım cümlesi:", "Akılda tut:", "Mantığı şudur:") YASAK. Ayrıntı: `meds/docs/TURKCE_USLUP_STANDARDI.md`.

Çalışma klasörü: `/home/indu/medsor/meds_temp/spot_cozucu/<brans>/`. Önce `TALIMAT_COZUCU3.md` (ve onun andığı belgeler) ile
`/home/indu/medsor/meds/scripts/spot_cozucu/DENETIM.md`'yi oku. `cozucu3/<kod>.json`'u başka bir yazar canlı ders metninden üretti.
Öğrenci bunları sesli dinleyip sınava girecek; tek yanlış bilgi kabul edilmez. `pdf_metin/<kod>.md` ve `girdi3/<kod>.json` → `canli_metin`'i oku.
Her soruda: anahtar PDF'e göre tartışmasız tek doğru mu; eşanlamlı/ikinci savunulabilir şık; bilgi PDF metin gövdesinde açık mı (YALNIZ
tablo/şekil/altyazıda geçen bilgi YASAK — kesin); klinik bulgu sorusu mu (yasak); konunun özü mü yoksa önemsiz ezber mi; zorluk etiketi;
`mevcut` ile ya da diğer yeni sorularla aynı bilgi (tersi/eşanlamlısı) mi; çeldirici PDF'te geçen kavram mı; açıklamalarda PDF dışı önerme,
sayı uyuşmazlığı, ipucu sızıntısı (eşanlamlı/tanım/ad benzerliği), ses–metin eşitliği, kısaltma okunuşu (harf harf; kesme işaretli ek yok).
Sorunluyu düzelt ya da aynı dersten güçlü bir soruyla değiştir; zayıfı sil (5–30, hedef ±3).
Bitiş: `python3 /home/indu/medsor/meds/scripts/spot_cozucu/cozucu_dogrula3.py cozucu3/<kod>.json` → 0 HATA. JSON'u Python ile yaz
(`ensure_ascii=False`, `indent=1`). Yalnız kendi derslerinin `cozucu3/<kod>.json`'unu değiştir; geçici dosyalar
`/tmp/claude-1000/denetim3_<brans>_<grup>/`. Son mesaj kısa: ders başına değişiklikler (gerekçe + PDF sayfası), okunuş düzeltme sayısı.
