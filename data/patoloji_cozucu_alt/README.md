# Patoloji · Alternatif Sesli Soru Çözücü

Mevcut patoloji soru bankasındaki **örnek** ve **çıkmış** sorulardan otomatik üretilmiş, kısa ve nokta atışı
çözümlü metinler ile bunların EMA Lightning seslendirmeleri.

- Metin: `meds/data/patoloji_cozucu_alt/metin/<kod>.json` (soru başına `metin` + `ses`) ve `<kod>.md`
- Ses: `meds/data/patoloji_cozucu_alt/ses/<kod>/<soru no>.mp3` + `kayit.json`
- Dizin: `meds/data/patoloji_cozucu_alt/index.json`
- Uygulama paketi: `meds/src/data/patoloji_cozucu_alt/{index,<kod>}.json`
- Ekran: `/alternatif-cozucu` (menü: Sınava hazırlan › Alternatif çözücü; soru çözücü sayfasında "Alternatif anlatım")
- Ses sunucusu: `GET /api/patoloji-cozucu-alt/ses/<kod>/<no>.mp3` (`meds/src/services/patolojiCozucuAlt.ts`)

## Ekran

Ders listesinden bir konu seçilir. Oynatıcıda soru kökü ve beş seçenek durur; "Çözüm" bölümünde her seçeneğin
gerekçesi, doğru cevap ve özet görünür. Alt çubukta oynat/duraklat, konum, hız ve "Otomatik geç" vardır; ses
bitince sıradaki soruya geçilir. Klavye: boşluk oynat/duraklat, oklar önceki/sonraki soru. İlerleme tarayıcıda
`medsoru_alt_cozucu_v1` anahtarında tutulur.

## Biçim

Her soru şu akışla çözülür:

1. Soru kökü ve beş seçenek okunur.
2. Kısa bir geçiş cümlesiyle seçenekler tek tek değerlendirilir; her seçenekte kavramın ne olduğu ve neden
   doğru ya da yanlış olduğu söylenir.
3. Doğru cevap ve kısa özet verilir.

Metin ortanca 152 kelimedir (en kısa 107, en uzun 317). Seslendirme toplamı ders başına `index.json` içinde.

## Üretim

```bash
python3 meds/scripts/patoloji_cozucu_alt/uret.py          # metinler
bash meds/scripts/patoloji_cozucu/cozucu_ses_gpu.sh \
  meds/scripts/patoloji_cozucu_alt/seslendir.py 01 02    # ses (GPU, gpuguard + saat kilidi)
python3 meds/scripts/patoloji_cozucu_alt/topla.py         # index.json
```

Ses üretimi tekrar çalıştırıldığında metni değişmeyen klipler yeniden üretilmez (`kayit.json` içindeki özet).
