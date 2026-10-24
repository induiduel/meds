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
  **Dallı ok:** bir kaynak resimde birden çok yere yol açıyorsa tek komutta `"dallar": [{"b": [x,y], "hedef_metin": "…",
  "etiket": "…"}, …]` (2–4 dal) yaz; kaynak bir kez çerçevelenir, dallar konuşma boyunca sırayla çizilir. Her dalın etiketi zorunlu.
- **egri_faz** (grafik/eğri: EKG, kan gazı, skor seyri): `nokta` eğrinin ÜSTÜNDE soldan sağa sıralı 4–30 nokta; `fazlar`
  nokta dizini aralıkları (`yukselis` | `inis` | `plato`).
- **sema** (görseli olmayan ya da metin ağırlıklı slaytta bir mekanizma/sınıflama): en çok 8 düğüm, her düğüm metni o
  cümlede ya da DAHA ÖNCEKİ cümlelerde geçen terim (ileri sızıntı yasak); kenar türü `aktive` | `inhibe` | `donusur` |
  `maske` (A görünür neden, B altta yatan / gözden kaçan: "alkol → SAK, subdural") | `karsit` (A ile B iki kutup:
  "dekortike ↔ deserebre"); kenara en çok 5 kelimelik `etiket` yazılabilir. Panel türü yapıdan kendiliğinden seçilir:
  zincir (A→B→C), grup (birden çok → bir, "}"), dal (bir → birden çok, karar), maske (perde kalkar), karşıt (yan yana).
  Koordinat yazma (yerleşim betikte).
- **Yazı slaytında iki satırı okla bağlama**: ok okunmuyor ve amacı anlaşılmıyor (H40). İki ucu da yazı olan ilişkiyi
  `sema` olarak yaz; betik iki ucu yazıya düşen okları da panele çevirir. `akis` yalnız resim/şema üstünde.
- **Aday varsa kullan:** sayfalar.md'de "Aday ok A#" (PDF'in kendi ok çiziminden) ve "Aday eğri E#" (grafikten çıkarılmış
  eğri) satırları kesin koordinattır. Cümle o oku/eğriyi anlatıyorsa komuta `"aday": "A2"` (ya da `"E1"`) yaz;
  koordinat ve faz alanlarını yazma, betik adaydan doldurur. Aday yoksa görüntüden oku.
- Bir cümlede en çok 2 çizim; sayfa başına en çok 8. Etiket en çok 6 kelime, Türkçe.
- Görseli zaten imleçle yeterince gösterilen basit bir cümleyi çizme; çizim anlamı açmalı (sınır, yön, faz, ilişki).

## Genel çizim kuralları (her ders için; kullanıcı geri bildirimi 2026-10-24, H40–H42)
1. **Görünürlük:** her çizgi beyaz hale üstünde 2,4 px tam opak; ince/saydam çizgi yok.
2. **Amaç:** her okun etiketi zorunlu (≤6 kelime); etiketsiz ok reddedilir.
3. **Başlangıç ve hedef belli:** okun çıktığı yer çerçevelenir (kutu yoksa halkalı nokta), hedef yazı/kutu çerçevelenir.
4. **Resimde bölge:** bir alan anlatılıyorsa (herni alanı, lezyon, kanama) `kontur` ile çiz; fosforlu kalemle boyanır.
5. **Resimdeki mevcut ok:** kopyası çizilmez; şekildeki ok çerçevelenip etiketlenir (betik kendisi yapar).
6. **Yazı ↔ yazı ilişkisi:** ok değil `sema` paneli (zincir / grup / dal / maske / karşıt).
7. **Bir → çok:** dallı ok (`dallar`), kaynak bir kez gösterilir.
8. **Kapatma yok:** etiket ve panel boş alana; panelin yeri yoksa sayfa altına ek alan açılır (kural 14).
9. **Eş zamanlı:** `bas`–`son`, çizilen şeyin ADI konuşulurken olmalı (terim cümlede geçtiği kelimede başlar; betik kaymayı
   düzeltir). Çizim, tarif edilen bölgenin kendisine oturur; yakınına ya da benzer bir yere değil.
10. **Ayrı ilişkiler ayrı:** birbirine bağlı olmayan iki ilişki aynı panelde yan yana dizilmez; her biri ayrı satırda
    kendi türüyle (betik/istemci bağlı bileşenlere böler). Panelde bağsız iki düğüm yan yana durmaz.
11. **Dallanma sayfada da:** resimde bir kaynaktan birden çok yere giden ilişki dallı oktur; dallar ortak gövdeden çıkar.
12. **Akıcı animasyon:** çizgiler konuşmayla yumuşak ve sürekli uzar (sıçrama yok); düğümler sırayla süzülür.
13. Bu kurallar bütün dersler içindir; kullanıcının her yeni çizim geri bildirimi buraya kural olarak eklenir.
14. **Panel sığmıyorsa sayfa uzar:** sayfada boş yer yoksa panel gizlenmez; betik `ek_alt` (sayfa oranı) ve `ek_renk`
    (slaytın alt kenar rengi) yazar, görüntüleyici o sayfanın altına aynı renkte alan ekler ve paneli oraya koyar (y > 1).
    Sayfanın kendi kutusu, işaret/vurgu/imleç koordinatları değişmez; ek alan ders boyunca sabittir (sayfalar kaymaz).
15. **Panel sayfayla orantılı ve okunur:** panel yazısı sayfa genişliğinin %2,2'si, etiket %2,3'ü (cqw; telefonda ~8 px,
    masaüstünde ~20 px, slayt yazısına yakın). Betik panel yüksekliğini istemcideki dizilimle aynı em hesabıyla tahmin eder
    (`panel_boyu`, düğüm satır kırılması dahil, %25 pay); 0,30'dan dar panel kullanılmaz. Slayt üstündeki panel kutusunda
    yazı/resim mürekkebi %1'i geçemez (kelimenin kenarına bile binmez); sığmazsa ek alana gider. Ek alanda panel tam
    genişlikte durur ve sayfanın ek panelleri aynı yeri paylaşır (her panel yalnız kendi cümlesinde görünür).

Yalnız `cizim.json`'u yaz; başka dosyaya dokunma. Bitince tek satır: `BİTTİ: <komut sayısı>`.
16. **Sayfa yalnız gerektiğinde ve gerektiği kadar uzar:** panel önce slaytın kendi boşluğuna (alttaki boş bant dahil)
    oturur; sığmazsa slaytın alt boşluğundan başlar ve sayfa yalnız taşan kısım kadar uzatılır (en az ek alan seçilir).
17. **Kelime takipçisi yazıyı kapatmaz:** konuşulan kelime hafif zemin + harflerin altında ince çizgiyle gösterilir; harflerin
    üstüne dolgu ya da kalın iç çizgi konmaz (küçük slayt yazısında okunmaz hale getiriyordu).
18. **Panel sürümleri ve boyut:** panel yazısı sayfa genişliğinin %1,75'i; betik yatay/dikey × normal/kompakt sürümlerinden
    slayta sığanı seçer. Satıra kırılan yatay zincir kullanılmaz → dikey (oklar aşağı). Ayrıntı: `docs/CIZIM_KURALLARI.md`.
