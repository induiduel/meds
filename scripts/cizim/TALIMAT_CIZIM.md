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
- **Resim/şema slaytında panel YOK (H51):** slaytın asıl içeriği bir görselse (şema, anatomik çizim, akış şeması görüntüsü,
  taranmış slayt) ilişkiyi görselin ÜSTÜNDE anlat: `kontur` (bölgeyi boya), `akis` (yapıdan yapıya ok; görseldeki mevcut
  ok için kısa ok → betik odak çerçevesine çevirir), dallı ok. Örn. herniasyon şemasında "kanama unkusu aşağı iter" →
  kanamadan unkusa ok + unkus konturu. Böyle sayfada `sema` yazma; betik reddeder.
- **Panel = şablon (ZORUNLU, 2026-10-24):** yazıdan yazıya ilişki paneli `"tur": "sema"` + `"sablon": "<kimlik>"` ile yazılır;
  şablonlar çalışma dizinindeki `sablonlar.json`'dadır (dersten bağımsız). Önce ANLAMI belirle, sonra şablonu seç:
  - durum/şüphe → bakılacak tetkik: `tani_tetkik` (tablo; ok DEĞİL — test hastalığa yol açmaz)
  - zehirlenme/durum → antidot/tedavi: `zehir_antidot` (tablo; "glukoz ⊣ hipoglisemi" gibi baskılama oku YANLIŞ)
  - bulgu → düşündürdüğü: `bulgu_dusundurur` · lezyon yeri → bulgu: `lezyon_bulgu` · skor: `skor`
  - gerçek neden → sonuç: `neden_sonuc` / `mekanizma_adimlari` (zincir) · birçok neden → tek sonuç: `cok_neden_tek_sonuc`
  - karar: `karar` (dal) · sıralı yapılacaklar: `algoritma` (numaralı) · alt türler: `siniflama` (madde imli;
    aynı grubun SIRALI öğeleriyse `"numarali": true`) · iki durumu ayırma: `karsilastirma` · gizleyen neden: `maskeleyen`
  - tek sayı (eşik, kesim noktası, doz, oran, süre) anlatılıyorsa: `deger_karti` (değer kartı). Cümlede sayının
    kendisi geçmeli; birden çok sayı karşılaştırılıyorsa tablo kullan. `cikmis` (kaç kez soruldu) YALNIZ doğrulanmış
    çıkmış eşlemesi varsa yazılır (kural 21), tahminle yazılmaz.
  Alanlar düzene göre: tablo `satirlar` [[hücre, hücre]] · zincir/adimlar `ogeler` · liste `baslik`+`ogeler` ·
  grup `kaynaklar`+`sonuc` · dal `soru`+`dallar` [[koşul, sonuç]] · maske `gorunen`+`altta` · karşıt `kutuplar`+`satirlar`
  [[özellik, A, B]] · değer `deger` (sayı içerir, ≤12 karakter) + `aciklama` + isteğe bağlı `birim`, `cikmis` (tam sayı). Hücre ≤60 karakter, yalnız cümlede/önceki cümlelerde geçen bilgi.
  **Uygun şablon yoksa** komuta `"yeni_sablon": {"id": "kisa_ad", "ad": "...", "duzen": "tablo|zincir|grup|dal|karsit|maske|liste|adimlar|deger",
  "basliklar": [...], "ne_zaman": "hangi tıbbi ilişki", "ornek": "..."}` ekle ve aynı kimliği `sablon`'a yaz; betik kütüphaneye
  ekler, sonraki derslerde de kullanılır. Bağımsız bir denetçi her paneli cümleyle karşılaştırıp tıbben yanlış ya da yanlış
  anlaşılır olanı düzeltir ya da siler.
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
19. **Resim slaytında panel yok:** görsel slaytta anlatım görselin üstünde (kontur/akış/odak); panel yalnız yazı slaytında.
20. **Yatay zincir tek satır:** kutular tek satıra sığmıyorsa dikey çizilir (betik seçer); sınama `panel_sinama.mjs` 0 hata.

## Şekil cümlesi kuralları (H59, 2026-10-25 — ihlal eden ders yayına GİRMEZ, `cizim_kapisi.py`)
21. **Şekil cümlesi çizilir:** sayfalar.md'de ★ ile işaretli (lazeri resim/tablo olan) her cümle için görselin üstünde
    cümlenin ANLATTIĞI PARÇAYI gösteren çizim yaz: lezyon/yapı/bölge `kontur`, yapıdan yapıya `akis`, tablo satırı/hücre
    grubu `kontur`. Seçilemiyorsa atla ve `atlanan` listesine nedenini yaz; uydurma yok. Ders başına ★ cümlelerin
    en az %40'ı çizimli olmalı (sınama dersleri k2-02/k2-07 düzeyi).
22. **Bütün resmi çevreleme:** kontur resim kutusunun %85'inden fazlasını kaplayamaz; "bu resim" demek için çizim
    yapılmaz (lazer zaten resmi gösterir). Anlatılan parçayı dola.
23. **Kontur çizginin üstünde:** noktaların en az %70'i görüntüdeki gerçek kenar/çizgi üstünde olmalı (görüntüyü yakından
    incele). Sınırı çizgi olmayan bölge (yumuşak doku, yazı bloğu) için kontur değil kısa `akis` (boş yerden yapıya) yaz.
24. **Doğru sayfa:** komutun `sayfa`'sı cümlenin listelendiği sayfadır (lazerin gösterdiği sayfa); başka sayfaya çizim
    reddedilir.
25. **Resim anlatılırken panel yok:** lazeri resim olan cümleye `sema` yazılmaz (sayfa yazı ağırlıklı olsa bile).
26. **Arka plan/süs resim değildir:** slayt şablonu, logo, kenar süsü, kapak deseni, yazının arkasındaki kart görseli
    için çizim yapılmaz; bunlar ★ olsa da atlanır.

## Tasarım kataloğunun tamamı kullanılır (kullanıcı kararı 2026-10-27 — bundan sonraki HER ders)
27. **Önce katalog:** her sayfa için `sablonlar.json`'daki **bütün** şablonlar (43+; zaman/seyir, bulgu→düşündürdüğü,
    lezyon→bulgu, refleks→düzey, muayene, tetkik, karar, algoritma, sınıflama, karşılaştırma, ilaç etkisi, skor, yaş/tarama,
    gen/kromozom …) gözden geçirilir; anlatılan ilişkinin **amacına en uygun** tasarım seçilir. Hep aynı 2–3 şablona
    (ör. yalnız `neden_sonuc`/`siniflama`) yığılmak HATA sayılır; uygun şablon varken düz kontur/ok yetinmek de eksiktir.
28. **Gerekli yerde mutlaka:** başlangıç şekli/seyir → `klinik_seyir` ya da `zaman_gorunum`; bulgu kümesi → `bulgu_dusundurur`;
    lokalizasyon → `lezyon_bulgu` / `refleks_duzey`; ayırıcı tanı ya da sık karıştırılan iki kavram → `karsilastirma`;
    tetkik seçimi → `tani_tetkik`; acil yaklaşım → `durum_yaklasim` / `algoritma`. Metin ağırlıklı slayt da bu panellerden
    yararlanır (kural 25: resim anlatılırken panel yok).
29. **Çıkmış ve öğrenci notu önceliği:** doğrulanmış çıkmış (`cikmis_konum` `dogrulandi`) ve öğrenci notunda işaretli
    satırlar çizimde öncelik alır; panel ya da kontur bu satırları gösterir.
30. Uygun şablon gerçekten yoksa `yeni_sablon` önerilir (CIZIM_KURALLARI §2b); kapı ve `panel_sinama.mjs` 0 hata zorunlu.

## Okumayı bozmama (H85 — kullanıcı kararı 2026-10-27; ihlal eden ders yayına GİRMEZ)
31. **Doğru yer, tam kapsama:** resim üstündeki kontur anlatılan yapının sınırının hafif dışından geçer, yapıyı tam içine alır
    (görüntüyü yakından aç; noktaları yapının çevresine koy, içinden değil). Emin değilsen çizme.
32. **Kelime ↔ kelime oku yok:** `akis` yalnız resim/şema içindeki iki görsel yapı arasında. Yazı maddeleri arası ilişki →
    şablonlu panel (boş alanda) ya da hiçbir şey.
33. **Okunabilir metinli tablo:** `kontur`, `akis`, `sema` yazılmaz; tablo yalnız işaret katmanıyla (marker) vurgulanır.
34. **Zoom'u betik belirler** (yalnız küçük resim bölgesi); geniş ya da çok parçalı bölgeyi tek cümlede çizme — anlatılan
    tek yapıyı çiz.
35. Okumayı bozacak hiçbir şey (yazının üstüne panel, büyük dolgu, gereksiz hareket) yapılmaz.

36. **Çok renk + marker boyama (2026-10-28, H128):** çizim yalnız kırmızı değildir. Aynı sayfada ayrı yapılara ayrı `renk`
    (`kirmizi|mavi|yesil|turuncu|mor|camgobegi|pembe|sari`; verilmezse betik `renk_ata` ile sayfa içinde sırayla atar).
    Hattı net izlenemeyen bölge (ödem/kanama/enfarkt alanı, doku zemini, lezyon yüzeyi) konturla değil `boya: true` ile
    fosforlu marker gibi boyanır (kenar şartı %40).
37. **Hangi resim (2026-10-28, H128):** birden çok resimli sayfada her çizime `resim: "R#"` yazılır; noktalar o kutunun
    dışındaysa doğrulayıcı reddeder. İki resim karşılaştırılıyorsa her resme ayrı renk ayrı çizim; resimden resme hızlı
    geçişte her cümle yalnız kendi resmini işaretler (önceki resmin çizimi taşınmaz, kural 18 / H60).
38. **Kısa anlatımda zoom yok (2026-10-28, H128):** çizimin başından cümle sonuna 70 karakterden (~4 sn) az kalıyorsa betik
    `yakin` yazmaz; ön yüz de 55 karakterden kısa çizim aralığına yakınlaşmaz.
39. **Panel anlatım başında açılır (2026-10-28, H128):** `sema` paneli (liste/sıralama/şema) cümle başında kurulmaya başlar,
    `son` kelimesinde tamamlanır; `son`'u listenin son maddesinin söylendiği kelimeye koy.
