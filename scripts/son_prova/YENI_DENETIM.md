# Yeni örnek soruların bağımsız denetimi
Önce YENI_SORU.md'yi oku. Sana verilen partların her aşama dosyasındaki `yeni_sorular` alanını denetle ve HATAYI DOSYADA DÜZELT:
1. Doğru cevap aşama metnine (ve kaynak slayta, pdf_metin) göre kesin doğru mu? Başka bir şık da savunulabilir mi (iki doğru)? → düzelt.
2. Soru, doğru şık ve "doğru" diye sunulan her bilgi aşama metninde var mı? Yoksa soruyu metindeki bir bilgiye göre yeniden yaz.
   Şık açıklamalarında metin dışı tıbbi iddia varsa kaynağa uygun hâle getir.
3. Kök/ipucu cevabı sızdırıyor mu; çeldiriciler aynı aşamada öğretilmiş komşu kavramlar mı; çıkmış üslubunda ve kolay–orta mı?
4. Aynı aşamanın `sorular`/`checkup` sorularıyla ya da başka aşamanın yeni sorusuyla aynı bilgiyi aynı kalıpla soruyor mu?
5. Türkçe doğal mı; şık açıklamaları standarda uygun mu (ne/ne işe yarar/neden doğru-yanlış).
Her düzeltmeden sonra `python3 meds_temp/son_prova/dogrula.py --part <part>` → PART 0 HATA. Yalnız `yeni_sorular` alanına dokun.
Ara dosyaların için scratchpad'de KENDİ adını taşıyan alt klasör kullan; `rm -rf` ile klasör silme YASAK.
Son rapor: part başına düzeltilen soru sayısı ve en önemli 3 düzeltme.
