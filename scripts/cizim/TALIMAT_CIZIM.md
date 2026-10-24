# Canlı çizim talimatı (R6, ICERIK_MOTORU_V3.md §4)

Sesli derste hoca konuşurken PDF'in üstünde **anlattığı şeyi çizer**: bir yapının sınırını kalemle dolanır, bir yolağı
okla gösterir, bir eğrinin yükselişini/inişini iz sürer, görseli olmayan slaytta küçük bir şema kurar. Çizim
zenginleştirmedir: yalnız cümle gerçekten o görseli/ilişkiyi anlatıyorsa çiz. Emin değilsen çizme.

## Girdi (çalışma dizini)
- `sayfalar.md`: bu partideki sayfalar; her sayfa için görüntü dosyası (`sNN.png`, üstünde numaralı mavi madde M# ve kırmızı
  resim R# kutuları; R# satırında kutunun sayfa oranı [x0,y0,x1,y1]) ve o sayfayı anlatan cümleler (`P#.C#: metin`, kelimeler
  `[0]kelime [1]kelime …` biçiminde numaralı).
- Her görüntüyü **Read ile aç ve bak**: koordinatları görüntüden okursun (0–1, sol üst = 0,0; x sağa, y aşağı).

## Çıktı: `cizim.json`
```json
{"komutlar": [
  {"cumle": "P12.C3", "bas": 4, "son": 11, "sayfa": 24, "tur": "kontur",
   "nokta": [[0.52,0.31],[0.58,0.29],[0.63,0.35],[0.60,0.44],[0.53,0.42]], "etiket": "dekortike postür"},
  {"cumle": "P5.C1", "bas": 0, "son": 9, "sayfa": 11, "tur": "akis", "a": [0.20,0.40], "b": [0.55,0.40], "iliski": "aktive",
   "etiket": "hipoksi → bilinç kaybı"},
  {"cumle": "P20.C0", "bas": 2, "son": 14, "sayfa": 40, "tur": "egri_faz",
   "nokta": [[0.10,0.70],[0.25,0.40],[0.40,0.42],[0.60,0.75]], "fazlar": [{"aralik": [0,1], "faz": "yukselis"}, {"aralik": [2,3], "faz": "inis"}]},
  {"cumle": "P8.C2", "bas": 0, "son": 12, "sayfa": 18, "tur": "sema",
   "dugum": [{"id": "n1", "metin": "beyin sapı lezyonu"}, {"id": "n2", "metin": "ARAS hasarı"}, {"id": "n3", "metin": "koma"}],
   "kenar": [{"a": "n1", "b": "n2", "tur": "donusur"}, {"a": "n2", "b": "n3", "tur": "aktive"}]}
]}
```
- `cumle`: sayfalar.md'deki kimlik; `bas`/`son`: çizimin başladığı ve bittiği **kelime numarası** (o cümlede, dahil).
  Çizim bu kelimeler söylenirken çizilir; ilgili terimin söylendiği kelimeyi seç.
- **kontur** (resimdeki bir yapının sınırı: anatomik bölge, lezyon, postür, histolojik alan): 5–20 nokta, yapının
  KENARI boyunca sırayla; mutlaka bir R# kutusunun içinde ve görüntüdeki gerçek çizginin/kenarın üstünde.
- **akis** (A, B'ye yol açar / B'yi baskılar / A, B'ye dönüşür): `kaynak_metin` ve `hedef_metin` = slaytta YAZILI olan
  kaynak ve hedef ifadesi (sayfalar.md'deki M# satırlarından, birebir; ör. "Osmolar açık", "Etilen glikol"); `a`/`b`
  yaklaşık noktaları (aynı ifadenin üstünde), `iliski`: `aktive` | `inhibe` | `donusur`. Betik oku o yazıların gerçek
  kutularına oturtur ve rotayı (düz / dirsek / kavis) içeriği kapatmayacak şekilde kendisi seçer; hedef yazı
  çerçevelenir. Hedef bir resim bölgesiyse `hedef_metin` yazma.
- **egri_faz** (grafik/eğri: EKG, kan gazı, skor seyri): `nokta` eğrinin ÜSTÜNDE soldan sağa sıralı 4–30 nokta; `fazlar`
  nokta dizini aralıkları (`yukselis` | `inis` | `plato`).
- **sema** (görseli olmayan ya da metin ağırlıklı slaytta bir mekanizma/sınıflama): en çok 8 düğüm, her düğüm metni o
  cümlede ya da DAHA ÖNCEKİ cümlelerde geçen terim (ileri sızıntı yasak); kenar türü `aktive` | `inhibe` | `donusur`.
  Koordinat yazma (yerleşim istemcide).
- **Aday varsa kullan:** sayfalar.md'de "Aday ok A#" (PDF'in kendi ok çiziminden) ve "Aday eğri E#" (grafikten çıkarılmış
  eğri) satırları kesin koordinattır. Cümle o oku/eğriyi anlatıyorsa komuta `"aday": "A2"` (ya da `"E1"`) yaz;
  koordinat ve faz alanlarını yazma, betik adaydan doldurur. Aday yoksa görüntüden oku.
- Bir cümlede en çok 2 çizim; sayfa başına en çok 8. Etiket en çok 6 kelime, Türkçe.
- Görseli zaten imleçle yeterince gösterilen basit bir cümleyi çizme; çizim anlamı açmalı (sınır, yön, faz, ilişki).

Yalnız `cizim.json`'u yaz; başka dosyaya dokunma. Bitince tek satır: `BİTTİ: <komut sayısı>`.
