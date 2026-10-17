# Spot bilgiler + sesli soru çözücü — branş geneli hat (Enfeksiyon, Üroloji; yeni branşlar)

Patolojideki "Sınav için en önemliler" + "Sesli soru çözücü"nün aynısını başka Kurul 1 branşlarına kurar. Ekranda: Sınav spotları ›
En önemliler / Soru çözücü › branş seçici (`?brans=enfeksiyon|uroloji`). Patoloji kendi hattında kalır (`scripts/patoloji_onem`,
`scripts/patoloji_cozucu`).

Kullanıcı kuralları (2026-10-17): yalnız ders PDF'i (PDF'te olmayan bilgi yok, müfredat = PDF); spot bilgi sayfası çıkmış ve örnek
sorularla güçlenir ve maddeler o soruları çözdürecek kadar detaylı; çözücü setleri 20–40 soru, çıkmış + örnek karışık; örnekler
çıkmışların üslubunda, ağırlıklı orta (kolay/zor da var), tekrar soru yok; ses yalnız EMA (başka sesler için altyapı hazır).

## Akış
1. PDF → sayfa metni: `meds_temp/spot_cozucu/<brans>/pdf_metin/<kod>.md` (`scripts/ders_isci/cikar.py`, OCR yedekli) + `pdf_liste.json`.
   Kodlar branşlar arasında tekil: `e01`… (Enfeksiyon), `u01`… (Üroloji); ilerleme/öğrendim kayıtları koda bağlı.
2. `aday_hazirla.py` → `cikmis/<kod>.json` (sitede görünen çıkmışlar; check-solve müfredat konusu → ders; aynı bilgiyi soran farklı yıl
   tekrarları `tekrar` grubunda) + `girdi/<kod>.json` (örnek soru hedefi). Konu → ders eşlemesi betiğin başındaki `BRANS` sözlüğü.
3. Yazar ajan: `TALIMAT_ONEM.md` → `onem/<kod>.json` (`onem_dogrula.py` 0 HATA), sonra `TALIMAT_COZUCU.md` → `cozucu/<kod>.json`
   (`cozucu_dogrula.py` 0 HATA; okunuş `../patoloji_cozucu/okunus_denet.py`).
4. Bağımsız denetçi ajan: `DENETIM.md` (PDF'e karşı her önerme; görsel sayfalar PDF'ten görüntüyle; çözülebilirlik; tekrar; ipucu sızıntısı).
5. `birlestir.py <brans>` → `src/data/<brans>_onem/`, `src/data/<brans>_cozucu/` (40'tan çok sorulu ders ardışık setlere: `u04-1`,
   `u04-2`; ses klasörü `klasor` = ders kodu), `cikti_tam/` (ses girdisi), `numara.json` (kalıcı soru no; yalnız eklenir).
6. Ses: `ses_kuyruk.sh <brans> [kod…]` → `ses.py` (EMA, CPU, flock'lu tek süreç) → `data/<brans>_cozucu/ses/<kod>/` → yeniden `birlestir.py`.
   Başka ses: `ses.py`'de `Saglayici` alt sınıfı + `SESLER` kaydı, `birlestir.py` `SES_AD`; klipler `ses_<id>/`, ön yüz `klipSes`/`sesler`
   ile ses seçiciyi kendiliğinden gösterir. Sunucu ucu `/api/cozucu-ses/<brans>/<ses>/<kod>/<klip>.mp3` (`src/services/cozucuSes.ts`).
7. `npx vite build`. Canlıya: kod dağıtımı + `data/<brans>_cozucu/ses/` Oracle'a rsync (git dışı).

Ön yüz: `components/spots/brans.ts` (branş tanımları: asistan/sınav kuralı yalnız patoloji), `OnemListesi.tsx`, `onem/*`,
`cozucu/*` (hepsi `brans` alır). Örnek sorular önem verisinde `ornek26` alanında (`zorluk`'lu).
