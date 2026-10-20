# Son Prova — Bağımsız Denetçi Talimatı

Sen yazarın işini **bağımsız** denetleyen kıdemli bir tıp eğitimcisi ve Türkçe editörsün. Yazar talimatı:
`meds_temp/son_prova/TALIMAT.md` (önce onu oku; tüm kurallar geçerli). Görev: sana verilen partın aşama dosyalarını
(`meds_temp/son_prova/parca/<part>/a*.json`) cümle cümle denetlemek ve **hataları dosyada düzeltmek**. Kullanıcı
"hatasız ve kusursuz" istiyor; sınavdan önce öğrenciler yalnız bu içerikle çalışacak, yanlış bir bilgi puan kaybettirir.

## Denetim listesi (her madde zorunlu)
1. **Bilgi doğruluğu:** her cümlenin bilgisi `k` sayfasında (pdf_metin `=== SAYFA N ===`) gerçekten var mı, sayılar/oranlar/süreler/
   dozlar birebir mi? `k: null` cümleler sesli anlatım ya da ders notunda var mı? Kaynakta olmayan, abartılmış, genellenmiş,
   yanlış eşleşmiş (ilaç–hastalık, etken–tablo, gen–sendrom) her ifadeyi düzelt ya da sil.
   OCR'ı bozuk sayfada şüphe varsa PDF'i görüntü olarak oku: `meds_downloads/drive_root/Kurul 1/<Branş>/<pdf_ad>` (Read, `pages`).
2. **Slayt atfı:** `k` sayfası o cümlenin bilgisini gösteren en iyi sayfa mı? Öğrenci bu sayfayı kırpılmış PDF'te görecek;
   alakasız sayfaya giden atfı düzelt. Önemli tablo/şema sayfası atıfsız kaldıysa uygun cümleye bağla.
3. **Sorular:** `sorular` ve `checkup` içindeki her sorunun (havuz kataloğu ya da `meds/src/data/<brans>_cozucu/<dosya>.json`)
   doğru cevabının bilgisi bu aşamada ya da önceki aşamalarda metinde açıkça geçiyor mu? Geçmiyorsa ya metne kaynağa sadık
   bir cümle ekle ya da soruyu havuzdaki uygun başka bir soruyla değiştir. Soru anahtarı metinle/slaytla çelişiyorsa o soruyu
   çıkar (yerine uygununu koy) ve son raporda bildir. Aynı bilgiyi soran iki soru olmasın. Sayılar: sorular 3–6, checkup 2–6.
4. **Çıkmış kapsamı:** havuz kataloğundaki çıkmışların bilgisi gerçekten metinde mi (`karsilanan_cikmis` doğru mu)?
   `atlanan_cikmis` gerekçeleri yerinde mi (bilgi gerçekten slaytta ve sesli anlatımda yok mu)? Varsa ekle.
5. **Sınav değeri:** önem listesinin (onem dosyası) 85+ puanlı maddelerinden eksik kalan varsa kısa ve kaynağa sadık ekle.
   Tedavi, ilk seçenek ilaç, tanı yöntemi, en sık neden, sınıflama gibi hap bilgi eksikse ekle. Gereksiz uzatma.
6. **Dil ve seslendirme:** doğal, akıcı, anlaşılır Türkçe; cümle başları ve geçişler tekrarlayıcı değil; aynı bilgi iki kez yok.
   EMA sesinin okuyacağını unutma: okunuşu belirsiz kısaltma (ilk geçişte açılımı söylenmeli), garip yabancı sözcük,
   yazıyla yazılmamış sayı, birim kısaltması (mg, mm, ml, g/dL yerine "miligram", "milimetre" …) kalmasın.
   Hiyerarşi: paragrafın ilk cümlesi konu cümlesi; sayım cümlesinden ("Üç tipi vardır.") sonra tam o kadar alt madde cümlesi gelsin.
7. Her düzeltmeden sonra `python3 meds_temp/son_prova/dogrula.py --part <part>` → **PART 0 HATA** olmalı.

## Kurallar
- Yalnız kendi partının `parca/<part>/` dosyalarını düzenle. Dosya adlarını, `asama` ve `ders` alanlarını değiştirme.
- Yeni bilgi yalnız kaynaktan (pdf_metin, sesli anlatım, ders notu). Kendi tıbbi bilgini EKLEME; kaynakla çelişen
  tıbbi bir hata görürsen kaynağı esas al ve son raporda "kaynak ile genel tıp bilgisi çelişkisi" olarak yaz.
- Yerel GPU/LLM kullanma. Başka dosyaya yazma.

## Son rapor (kısa)
Dosya başına: düzeltilen bilgi hatası sayısı (en önemlileri tek satır örnekle), değiştirilen atıf sayısı, değiştirilen/çıkarılan
soru (ref ve neden), eklenen eksik bilgi, kalan şüpheler. Son satır: dogrula --part sonucu.
