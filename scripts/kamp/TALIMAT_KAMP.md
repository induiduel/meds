# Kurul kampı — hoca tüyoları + ders bilgi deposundan sınav kampı (Claude, otomatik hat)

Örnek: Kurul 1 "TBG Sınav Kampı" (`src/data/genetik_kamp/kalip.json` + `src/data/genetik_asistan/g07.json`; önce oku). Bu
talimat aynı fikri **her kurul ve branş** için genelleştirir: hocanın derste verdiği tüyolar (ONAYLI) + o branşın yayımlanmış
derslerinin bilgi deposu → hızlı tekrar kampı. **PDF'i açma:** her dersin `ozet.md`'si (bilgi paketi, önem puanları, tablolar,
hoca vurgusu, çıkmışlar — her satırda `kod:sayfa`) yeterlidir; çok gerekirse depodaki `kaynak.md`'ye bak.

## Girdiler (çalışma dizininde `girdi.json`)
`{kurul, brans, brans_ad, dersler: [{ders_id, kod, konu, ozet: "<ozet.md yolu>", kaynak: "<kaynak.md yolu>"}], tuyolar: [{id, metin, ders_id?, kaynak}], onceki: "<varsa önceki kamp JSON yolu>"}`

## Çıktı: `kamp.json`
```json
{"surum": 1, "kurul": 2, "brans": "farmakoloji", "baslik": "Farmakoloji Sınav Kampı", "kisa": "1 cümle: hangi tüyolara ve derslere dayanıyor",
 "tuyolar": [{"id": "t-…", "metin": "…"}],
 "anlatim": [{"id": "a01", "baslik": "…", "metin": "doktorun öğrenciye anlatımı, 60–180 kelime, doğal Türkçe",
              "k": ["2f01:12"], "puan": 0-100, "tuyo": "t-…" | null}],
 "kalipler": [{"id": "ilac-etki", "baslik": "İlaç → etki", "soru": "“… ilacının etki mekanizması hangisidir?”",
               "sutun": ["İlaç", "Etki"], "satir": [{"s": "…", "t": "…", "k": "2f01:12", "h": 1}]}],
 "deneme": [{"id": "d01", "kok": "…", "secenekler": {"A": "…", "B": "…", "C": "…", "D": "…", "E": "…"}, "dogru": "C",
             "aciklama": {"A": "…", "B": "…", "C": "…", "D": "…", "E": "…"}, "k": ["2f01:14"], "tuyo": "t-…" | null}]}
```
## Kurallar
1. **Her onaylı tüyo en az bir kez işlenir** (anlatım/kalıp/deneme `tuyo` alanıyla). Tüyonun söylediğini derste karşılığı olan
   bilgiyle doldur; tüyoda olup derste olmayan bilgi EKLENMEZ (tüyo "neyin önemli olduğunu" söyler, bilgiyi ders verir).
2. **Kaynak zorunlu:** her anlatım, kalıp satırı ve deneme sorusu `kod:sayfa` taşır; kod bu kampın derslerinden, sayfa ders
   metninde var.
3. **Anlatım** puan sırasıyla; tüyoya bağlı ve çıkmışta sorulmuş bilgiler ≥90. 8–25 madde.
4. **Kalıplar:** hocanın soru kalıpları (tüyolardan) + çıkmışlarda tekrar eden kalıplar; 3–8 tablo, satır başına 1 bilgi; `h: 1` =
   çıkmışta ya da tüyoda geçen.
5. **Deneme:** 10–20 soru, çıkmışların üslubunda, orta-zor; tekrar soru yok; çıkmışı aynen kopyalama. Şık açıklaması standardı
   (`meds/docs/SIK_ACIKLAMA_STANDARDI.md`, her şık 2–3 cümle, "Doğrusu: …" yanlış şıklarda).
6. Türkçe üslup standardı; iç süreç dili yok ("aday", "PDF'te yok", "tüyo listesinde" gibi ifadeler öğrenci metninde geçmez —
   öğrenci metninde "Hocanız derste … vurguladı" denebilir).
7. Önceki kamp varsa kimlikleri koru (a01, d03 …), yalnız değişeni güncelle.
Bitince `python3 /home/indu/medsor/meds/scripts/kamp/dogrula.py kamp.json --girdi girdi.json` 0 HATA olana kadar düzelt.
