# Kopya çift incelemesi — talimat

Her parti dosyası (`inceleme/parti/pNNN.json`) iki çıkmış soruluk çiftler içerir (`A`, `B`). Her çift için
**bu iki kayıt aynı soru mu?** sorusunu tıbbi içeriğe bakarak tek tek yanıtla. Metinler OCR'dan geldiği için yazım,
Türkçe karakter, büyük/küçük harf, soru numarası, başa yapışmış ders/başlık adı, şık sırası ve şık harfi farkları
**önemsizdir**. `site_kok`/`site_siklar` sitede gösterilen (yeniden yazılmış) sürümdür; karar özgün `kok`/`siklar` üzerinden verilir,
özgün metin bozuk/eksikse site sürümü yardımcı olur.

## Kararlar

- `AYNI` — aynı soru: aynı bilgiyi soruyor, şık kümesi aynı ya da büyük ölçüde aynı (sırası değişmiş, biri eksik/kesik,
  OCR bozuk olabilir), doğru cevabın **içeriği** aynı olmalı. Bir kayıt diğerinin kesik/eksik hâli ise de `AYNI`.
- `VARYANT` — aynı kalıp/konu ama farklı soru: farklı sayı/değer (ör. "1-2 mm" ↔ "3-5 mm"), "doğrudur" ↔ "yanlıştır",
  farklı hastalık/ilaç/yapı, şık kümesi belirgin farklı ve doğru cevap farklı bir kavram.
- `FARKLI` — konu ya da soru tamamen farklı.

Ek alanlar:
- `cevap_celiskisi`: `AYNI` iken iki kaydın işaretli cevabının **içeriği** farklıysa `true` (harf farkı tek başına çelişki değildir:
  şık sırası değişmiş olabilir — doğru şıkkın metnine bak). Hangisinin doğru olduğunu biliyorsan `dogru_olan`: "A" | "B" | "?".
- `guven`: "yuksek" | "orta" | "dusuk".
- `not`: kısa gerekçe (özellikle VARYANT/FARKLI ve çelişkilerde; ≤ 25 kelime, Türkçe).

`kural_karari` ve `sinav` alanları yalnız bilgi içindir; kararını etkilemesin (yıl/kurul ayrımını biz yapıyoruz).

## Çıktı

`inceleme/sonuc/pNNN.json` — partideki **her** çift için bir satır, şu biçimde bir JSON dizisi:

```json
[{"cift": 0, "a": "<A.id>", "b": "<B.id>", "karar": "AYNI", "cevap_celiskisi": false, "dogru_olan": null, "guven": "yuksek", "not": ""}]
```

Eksik çift bırakma; `cift` numaraları partidekiyle aynı olmalı. Dosyayı yazdıktan sonra
`python3 inceleme/dogrula.py pNNN` çalıştır; 0 HATA vermeli.
