# Anlamsal Slayt Çapası — Yazım Talimatı (Kurul 2+ ders zinciri `capa` adımı)

Sesli derste okunan her cümle, ekrandaki ders slaytında **gerçekten anlattığı yeri** işaretler (madde kutusu, resim kutusu,
hareketli imleç). Kelime eşlemesi tahmin yürütür ve yanlış satıra sıçrar; sen yeri **görüntüye bakarak** seçersin.

## Girdiler (görevde verilen çalışma klasöründe)
- `dok/cumleler.md` — dersin paragrafları ve cümleleri (`P<i>.C<j>: …`, istemcinin bölmesiyle birebir) + eski sayfa tahmini.
- `dok/sNN.png` (çok dosyalıda `dNN_sNN.png`) — slayt görüntüsü: mavi **M#** = madde kutusu, kırmızı **R#** = resim kutusu.
  `dok/sNN.txt` — aynı sayfanın M# metinleri ve R# kutuları. Görüntüyü Read aracıyla aç.
- `capa.json` — başlangıç: yazarın v2 çapası (`ses`, `sayfa`, varsa `satir`/`sekil`). Sayfa çoğu zaman doğrudur; madde yoktur.

## Çıktı: `capa.json` (aynı dosyanın üzerine)
```json
{"mdSha1": "<değiştirme>", "p": [[{"ses": "<cümlenin ilk 60 harfi>", "sayfa": 12, "dosya": 0,
   "madde": [3, 4] | "resim": 1 | "kutu": [x0, y0, x1, y1],
   "yol": [{"k": "cümlede geçen ifade", "x": 0.42, "y": 0.61}]}, …], …]}
```
- **Paragraf başına bir liste, cümle başına bir öge, sırayla.** Paragraf ve cümle sayısı `cumleler.md` ile birebir.
- `ses`: cümlenin başı, harfi harfine (`cumleler.md`'den kopyala).
- `sayfa`: cümlenin bilgisinin geçtiği sayfa. Eski tahmin yanlışsa düzelt; bağlayıcı cümlede önceki cümlenin sayfası.
- `madde`: cümlenin anlattığı **M#** kutuları (yalnız o sayfanın numaraları). Cümle bir maddeyi okuyorsa o madde; birkaç maddeyi
  özetliyorsa hepsi. Başlık cümlesi başlık maddesine.
- `resim`: cümle bir şekli/tabloyu/görseli anlatıyorsa (M# yoksa ya da şekil daha doğruysa) **R#**.
- `kutu`: madde/resim kutusu yeri karşılamıyorsa (ör. resmin bir parçası, tablonun bir sütunu) sayfa oranı 0–1 elle kutu.
- `yol` (isteğe bağlı, resim anlatımında): cümlede adı geçen yapıların resim üzerindeki yerleri, cümledeki sırayla — imleç o
  kelime okunurken oraya gider. `k` cümlede birebir geçmeli.
- En az **%70** cümle `madde`, `resim` ya da `kutu` taşımalı (yalnız sayfa vurgusu az kalsın). Slaytta karşılığı olmayan cümle
  (geçiş, toparlama) yalnız `sayfa` ile kalabilir.

## Kurallar
- Uydurma yer verme: kutu gerçekten o bilgiyi göstermeli. Emin değilsen görüntüyü yeniden aç.
- Metne, sesli ders dosyalarına, başka hiçbir dosyaya dokunma; yalnız `capa.json`.
- Bitince kapı: görevde verilen `capa_dogrula.py` komutu **0 HATA**.
