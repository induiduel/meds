# Son Prova — Yeni Örnek Soru Yazım Talimatı

Her aşama dosyasına (`meds_temp/son_prova/parca/<part>/aNN.json`) **2 yeni örnek soru** eklenir: alan `"yeni_sorular"`.
Öğrenci bu soruları aşama biter bitmez sesli asistanla çözer. Sorular **çıkmışların üslubunda, benzer uzunluk ve zorlukta**
olmalı (örnekler: `meds_temp/son_prova/havuz/<kod>.md` çıkmış bölümü).

## Kurallar
- **Bilgi yalnız bu aşamanın metninden** (`bolumler` içindeki cümleler) — anlatılmayan bilgi sorulmaz, ileri aşamaya sızma yok.
  Metindeki bilgi kaynağa (slayt) sadıktır; metinde olmayan hiçbir tıbbi bilgi şıklara bile doğru gibi konmaz.
- Mevcut `sorular`/`checkup` sorularıyla ve havuzdaki çıkmışlarla **aynı bilgiyi aynı kalıpla sormaz**: farklı bir sınav noktası
  seç (aşamada çıkmışta sorulmamış ama sorulmaya müsait hap bilgi: tanım, en sık, sınıflama, tedavi/ilaç, bulgu, sayı).
- Kalıplar çıkmışlardaki gibi: "Aşağıdakilerden hangisi … değildir/doğrudur?", "… en sık …", eşleştirme "I, II, III", kısa vaka kökü.
- Zorluk: kolay–orta, ortaya yakın (iki sorudan biri orta, diğeri kolay ya da orta). 5 şık (A–E), tek doğru, doğru şık harfleri
  dağınık olsun. Çeldiriciler aynı aşamada geçen komşu kavramlar.
- **İpucu** (`ipucu`): düşündüren tek cümle; doğru cevabın kelimesini/kökünü içermez.
- **Şık açıklamaları** (`siklar`, her şık için 2–3 cümle, 20–55 kelime): kavramın ne olduğu, ne işe yaradığı ve bu soruda neden
  doğru/yanlış olduğu (`meds/docs/SIK_ACIKLAMA_STANDARDI.md`). "Bu sorunun cevabı değil" gibi geçiştirme YASAK.
- **Çözüm** (`cozum`): 2–3 cümle, doğru cevabın gerekçesi.
- Türkçe doğal (`meds/docs/TURKCE_USLUP_STANDARDI.md`). Soru ekranda gösterilir ve EMA ile okunur: rakam serbest (ekranda),
  kısaltmalar standart yazımla.
- `sayfa`: bilginin slayt sayfa(lar)ı (aşamanın `k` atıflarından, sayı listesi, ör. [23]).

## Biçim
```json
"yeni_sorular": [
  {"soru": "…?", "secenekler": {"A": "…", "B": "…", "C": "…", "D": "…", "E": "…"}, "dogru": "C",
   "ipucu": "…", "siklar": {"A": "…", "B": "…", "C": "…", "D": "…", "E": "…"}, "cozum": "…", "zorluk": "orta", "sayfa": [23]}
]
```
Dosyanın başka alanına dokunma. Her dosyadan sonra `python3 meds_temp/son_prova/dogrula.py <dosya>` → 0 HATA.
Son mesaj: dosya başına eklenen soru sayısı ve kısa not.
