# KMB Görsel Sesli Asistan — Yol Haritası ve İşletim

Klinik Mesleki Beceri (KMB, Dönem 3 · TIS301/TIS302) dersleri için **önce öğreten, sonra sınava sokan** etkileşimli,
görsel ve EMA sesli asistan. Amaç: pratik sınavda hocanın kazanımları sorgulayan her vaka sorusuna cevap verebilmek,
uygulamada her aşamada nelere dikkat edileceğini ve anormal durumlara yaklaşımı öğretmek.

## 1. Kaynak önceliği (değişmez)

1. **Hocanın ses kaydı** (`meds_temp/kmb/kaynak/*.m4a` → yazı `meds_temp/kmb/yazi/<beceri>.{txt,json}`) — ana kaynak.
2. **KMB belgesi** (ders bilgi paketi: amaç, öğrenim hedefleri — TIS301/302 Ek-4/Ek-5) — kazanım iskeleti.
   Her öğrenim hedefi en az bir öğretim adımına ve en az bir sınav ögesine bağlanır (`hedefler[].adimlar`).
3. Ders kaynakları (KMB Rehberi, Roberts & Hedges) — yalnız teorik boşluğu doldurmak için; kayıtla çelişirse kayıt geçerli.
4. YouTube / internet videoları ve maket resimleri — **yalnız** işlemi anlamak ve doğru görsel kurmak için; içerik kaynağı değildir.

Kayıttan net duyulamayan sayı/süre (`dogrulanacak: true`) öğrenciye kesin bilgi gibi sunulmaz; kaynakla doğrulanınca açılır.

## 2. Aşamalar (yol)

| Aşama | İş | Durum |
|---|---|---|
| A0 | Kaynak alımı: PDF + ses → `meds_temp/kmb/kaynak`, yazıya dökme (faster-whisper, GPU koruyuculu) | ✅ ilk paket (2026-10-24) |
| A1 | Kazanım haritası: belge hedefleri → beceri kayıt defteri `src/data/kmb/index.json` | ✅ 6 beceri |
| A2 | Ders senaryosu: ses yazısı + hedeflerden öğretim adımları (cümle cümle, her cümleye görsel eylem) | ✅ 02 Üretral kateter |
| A3 | Görsel sahneler: SVG sahne kitaplığı (`src/components/kmb/sahneler.tsx`), her öge kimlikli → vurgula/çiz/renklendir/etiket; v2 degrade/anatomik katman; adım başına ana sahne + `ek` yakın plan panelleri (2–3 görsel); malzemeler ürün fotoğraflarına, maket sahnesi eğitim maketine göre | ✅ 14 sahne |
| A4 | Sınav: dallanan OSCE akışı (`akislar`: karar noktası → yollar, numaralı yuvalar, akış haritası, basamak başına açılır ayrıntılı açıklama + ses) + vaka senaryoları (çoklu) + sahnede bul (hotspot); her şıkta ne/neden açıklaması | ✅ 02 |
| A5 | EMA sesi (GPU, `cozucu_ses_gpu.sh`) → `data/kmb_cozucu/ses/<kod>/`, zamanlama `src/data/kmb/ses_<kod>.json` | ✅ 02 |
| A6 | Doğrulama kapısı `scripts/kmb/dogrula.py` (hedef kapsamı, sahne/öge kimlikleri, şık açıklaması, Türkçe üslup) | ✅ |
| A7 | Ekran: `/dersler/kmb[/<beceri>[/ogren|hedef|video|sinav]] (eski /kamplar/kmb yönlenir)` (iç `/kmb`) | ✅ |
| A8 | Lottie videoları: `scripts/kmb/lottie_dsl.py` (bölüm zaman çizelgesi, SVG yolu→Lottie, yol boyunca hareket, kırpma, degrade) + `lottie_uret.py` (12 video, 18–41 sn, EMA `l-<ad>` sesine kare kare oturur) → `src/data/kmb/lottie/`; oynatıcı `LottieVideo.tsx` (zaman çubuğu, bölümler, hız, altyazı, tam ekran); tam ekran ders videosu `DersVideo.tsx` (adım başına 2–3 görsel yatayda, altta altyazı) | ✅ 02 |
| A9 | Kalan beceriler: NG sonda, atel, burun kanaması, hava yolu, enjeksiyon — **ses kaydı geldikçe** A2–A6 tekrar | ⏳ kaynak bekleniyor |
| A10 | Bağımsız denetçi geçişi (yazar + denetçi), yayın (`dagit.sh`) | ⏳ |

## 3. Veri şeması (`src/data/kmb/<kod>.json`)

```
{ kod, ad, belgeKodu, amac, kaynaklar[], hedefler[{no, metin, adimlar[]}],
  adimlar[{ id, baslik, sahne, ek[], cumleler[{ metin, eylem[] }], puf[], dikkat[] }],
  sinav: { akislar[{ id, ad, yonerge, basamaklar[{ id, metin, aciklama, dal?{ soru, yollar[{ id, etiket, basamaklar[] }] } }] }], senaryolar[{ id, baslik, sahne, eylem[], soru, secenekler[{metin, dogru, aciklama}], puf }],
           bul[{ id, sahne, yonerge, hedef, aciklama }] } }
```

Eylem türleri: `vurgula` (nabız ışığı), `ciz` (çizgi aşama aşama çizilir), `renk` (yesil/kirmizi/mavi/sari), `goster`, `gizle`,
`etiket`. Bir adımdaki eylemler cümle ilerledikçe birikir; ses cümle zamanlamasıyla eşzamanlıdır.

## 4. Komutlar

```
python3 meds/scripts/kmb/lottie_uret.py                 # Lottie videoları (ses varsa ses zamanlı); ses.py'den sonra yeniden çalıştır
python3 meds/scripts/kmb/dogrula.py                     # 0 HATA olmadan ses ve yayın yok
bash meds/scripts/patoloji_cozucu/cozucu_ses_gpu.sh meds/scripts/kmb/ses.py 02   # EMA, GPU
```

## 5. Yeni ders ekleme sırası

1. Kaynağı `meds_temp/kmb/kaynak/` altına koy, ses kaydını yazıya dök.
2. `index.json`'da becerinin `durum`unu `hazirlaniyor` yap; `<kod>.json`'u hedeflerden başlat.
3. Gerekirse `sahneler.tsx`'e yeni sahne (her öge `id`'li, etiketi `lbl-<id>`).
4. `dogrula.py` 0 HATA → `ses.py <kod>` (GPU) → `npx vite build` → durum `hazir`.
