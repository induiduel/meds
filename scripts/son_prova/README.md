# Son Prova hattı (her kurul için)

Kurul sınavından önce her dersin sınav odaklı **sesli özet partları** + aşama soruları + part check-up + genel check-up +
sınav dağılımıyla 3 deneme. Ön yüz `/son-prova` (`src/components/sonProva/`), veri `src/data/son_prova/k<N>/`.
Çalışma klasörü `meds_temp/son_prova/` (betiklerin asılları buradaki kopyalarla aynıdır; KOK yolu çalıştırıldığı klasördür).

## Akış (Kurul N)
1. **Plan** — `plan.py`: `SINAV` (fakülte duyurusundaki branş soru sayıları), `PARTLAR` (part anahtarı `kN-8x-son-prova-<branş>[-<no>]`,
   ders kodları PDF sırasıyla, kelime hedefi; part ≤ 88 dk ≈ 9.800 kelime), yazar grupları. Kaynaklar: `pdf_metin` (slayt metni),
   sesli anlatım, ders notu, önem listesi, soru çözücü havuzu (`src/data/<branş>_cozucu`). Çıktı `plan.json` + `havuz/<kod>.md`.
   ⚠ PDF sürümünü doğrula: slayt metni bu yılın hocasının Drive PDF'iyle aynı olmalı (Kurul 1'de e11 eski yıldandı → yeniden yazıldı);
   PDF'i paylaşılmamış derste `pdf_yok: true` (özet PDF'te slayt metni sayfası), Drive adı farklıysa `drive_ad`.
2. **Yazar ajanlar** — `TALIMAT.md` (aşama dosyaları `parca/<part>/aNN.json`; cümle başına slayt atfı, aşama sonu 3–6 soru, check-up 2–6).
3. **Bağımsız denetçi** — `DENETIM.md` (bilgi/atıf/soru/okunuş). Kapı: `dogrula.py --part <part>` → PART 0 HATA.
4. **Derle** — `derle.py` → `cikti/<part>/` (konuşma metni, hizalama + `sayfaKaynak`, vurgu, `kirp.json`, `asamalar.json`).
5. **Özet PDF** — `node scripts/son_prova/pdf_kirp.mjs cikti/<part>/kirp.json` → `data/son_prova/pdf/<part>.pdf` (git dışı;
   deploy-code.sh [1b] gönderir). Sayfa üstü şerit: "Branş N) Ders · slayt S".
6. **Sorular** — `soru_dagit.py` → `src/data/son_prova/kN/{index.json, sorular/<branş>.json}` (aşama/check-up yazardan;
   genel check-up aşama başına 2–3; 3 deneme sınav dağılımıyla, kolay–orta, ayrık).
7. **Ses** — cikti dosyalarını `data/sesli_anlatim/{metin,hizalama,vurgu}/<part>`'a kopyala; Oracle `POST /api/sesli-anlatim/ders-ekle`
   `{key, metin, yalnizEma:true}` (x-panel-secret + X-API-Password). EMA okunuşu `scripts/sesli_anlatim/modul_okunus.py`
   (`-son-prova-` anahtarları modül yazımıyla; Roma rakamı → sayı). Oracle `meds-ema` konteyneri eski kodla iş almasın: kod
   dağıtılmadan önce durdurulur (Kurul 1'de patoloji-2 parçaları silinip yeniden üretildi).
   Kelime/cümle zamanlaması ve PDF işaretleri mevcut zamanlayıcılarla kendiliğinden gelir.
8. **Dağıtım** — commit + `bash deploy/oracle/dagit.sh` (onem +1).

## Soru denetimi ve düzeltme (2026-10-21)
- Denemeler ve kusurlu havuz soruları bağımsız denetlenir (`meds_temp/son_prova/deneme_denetim/`, kanıtlı ikinci tur `SIKI.md`).
- Kurtarılabilen soru yeniden yazılır (`duzelt/TALIMAT.md`, kapı `duzelt/denetle.py`) → `duzelt_uygula.py`: Son Prova'ya özel kimlik
  `<brans>/t0N#n`, sesler `data/<brans>_cozucu/ses/t0N/` (soru çözücü havuzu değişmez). Denemede yalnız değiştirme: `deneme_degistir.py`.
- ⚠ `soru_dagit.py` yeniden çalışırsa bu düzeltmeler ezilir: ardından `duzelt_uygula.py --sessiz` ve `deneme_degistir.py` çalıştır.
- ⚠ e11 (2026) PDF'inin bazı sayfaları görüntüdür: metin çıkarımında yok diye "kaynakta yok" deme, sayfayı görüntü olarak oku.
