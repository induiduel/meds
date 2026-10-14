# Cevap ↔ ders özeti anlamsal denetimi — talimat

Her parti (`parti/aNNN.json`) çıkmış sorular içerir: kök (`kok`), doğru cevap (`dogru_cevap`), kökün olumsuz olup olmadığı
(`olumsuz_kok`: "hangisi değildir/yanlıştır" türü) ve ders özetinden sözcüksel olarak en benzer 1–2 pasaj (`pasajlar`; her biri
özet kimliği, satır no ve ±1 satır bağlamlı metin).

Her soru için şunu yargıla: **Bu pasaj, sorunun doğru cevabını anlamca eksiksiz veriyor mu?** Yani yalnız bu pasajı okuyan bir
öğrenci sorunun doğru cevabını kesin olarak bulabilir mi?

- `anlamsal` (0–100): pasajın doğru cevabı **anlamsal bütünlükle** karşılama derecesi.
  - 90–100: pasaj cevabı açıkça ve tam veriyor (aynı bilgi; farklı kelimeler/eş anlamlı ifade olabilir). Olumsuz kökte: pasaj,
    doğru şıkkın neden "değil/yanlış" olduğunu açıkça gösteriyor (ör. doğru listeyi verip bu şıkkı dışarıda bırakıyor ya da tersini söylüyor).
  - 60–89: ilgili ve kısmen destekliyor ama bir parçası eksik/örtük ya da ek çıkarım gerekiyor.
  - 0–59: aynı konu ama cevabı vermiyor, ya da yalnız kelime benzerliği var, ya da çelişiyor.
- `celisiyor`: pasaj işaretli doğru cevapla **çelişiyorsa** true (cevap anahtarı şüpheli olabilir) — `not`a kısa gerekçe.
- `pasaj`: en iyi pasajın sırası (0 ya da 1); hiçbiri uygun değilse yine en yakını.
- `not`: ≤ 20 kelime, yalnız 60–89 aralığında ya da çelişkide.

Kelime benzerliğine kanma: pasaj soruda geçen terimleri içerip cevabı vermiyorsa puan düşük olmalı. Tıbbi bilgini kullanarak
pasajın gerçekten aynı şeyi söyleyip söylemediğine bak; pasajda olmayan bir bilgiyi "biliyorum" diye puanlama.

Çıktı: `sonuc/aNNN.json` — partideki her soru için:
`[{"id": "<soru id>", "pasaj": 0, "anlamsal": 95, "celisiyor": false, "not": ""}]`
Eksik soru bırakma. Yazdıktan sonra `python3 dogrula.py aNNN` → 0 HATA.
