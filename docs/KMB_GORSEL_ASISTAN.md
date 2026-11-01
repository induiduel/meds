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
| A8b | **Hedefler filmi** `HedefFilmi.tsx` (2026-10-31): hedef kartları (`hedefCalisma`) tam ekranda art arda; SVG sahneler gerçek zamanlı, cümle başına `film[i]` vuruşu (`sahne?`, `eylem[]`, `odak`, `zoom` 1–2), kamera odak kutusuna yaklaşır + spot, evreler Ne/Nasıl/Neden/Sık hata/Hoca sorar (`h-N`, `h-N-s`), bitiş özeti; kapı `dogrula.py` film denetimi | ✅ 02 |
| A8c | 3B deneme (three.js, `components/kmb/sahne3b/`): 14 sahne, organik yüzeyler — 2026-11-01 kullanıcı kararıyla ARŞİV (varsayılan kapalı, `localStorage.medsoru_kmb_3b='1'`); ön yüz 2B (SVG+Lottie) hattında, hedef stil düz vektör çizgi film (H462 kuralları) | 🗄 arşiv |
| A8d | **2B düz çizgi film geçişi** (2026-11-01, kullanıcı onaylı stil, `docs/KMB_2B_STIL.md`): tüm SVG sahneler yeniden çizildi (`sahneler.tsx` Erkek; `sahneler_2b_a/b/c.tsx` kalan 13; ortak sözleşme `sahneOrtak.tsx`, `kmb-2b-*` palet), Lottie paleti aynı tonlara alındı (`lottie_uret.py`/`adim_lottie.py`/`lottie_dsl.py`), H465 (yön sistemi). Canlıya gönderilmedi | ✅ yerel |
| A8e | **Lottie 2B hattı + Hikâye filmi** (2026-11-01): `scripts/kmb/lottie2b/` (svg_disa → svg_lottie → Sahne2B/ortak2b → uret2b/adim2b), çıktı `src/data/kmb/lottie2b/`, eski hat korunur (`medsoru_kmb_lottie_eski`); `HikayeFilmi.tsx` tam ekran tek akış (kazanım + bulgu kartları) | ✅ yerel |
| A9 | Kalan beceriler: NG sonda, atel, burun kanaması, hava yolu, enjeksiyon — **ses kaydı geldikçe** A2–A6 tekrar | ⏳ kaynak bekleniyor |
| A10 | Bağımsız denetçi geçişi (yazar + denetçi), yayın (`dagit.sh`) | ⏳ |

## 3. Veri şeması (`src/data/kmb/<kod>.json`)

```
{ kod, ad, belgeKodu, amac, kaynaklar[], hedefler[{no, metin, adimlar[]}],
  adimlar[{ id, baslik, sahne, ek[], cumleler[{ metin, eylem[] }], puf[], dikkat[] }],
  sinav: { akislar[{ id, ad, yonerge, basamaklar[{ id, metin, aciklama, adim, dal?{ soru, yollar[{ id, etiket, basamaklar[] }] } }] }], senaryolar[{ id, baslik, sahne, adim, eylem[], soru, secenekler[{metin, dogru, aciklama}], puf }],
           bul[{ id, sahne, yonerge, hedef, aciklama, adim }] } }
```

`adim` (zorunlu, dogrula.py): sınav ögesinin ilgili öğretim adımı. Hata istatistiği (Eksikler) yanlışı bu adıma bağlar
ve "Adımı yeniden çalış" ile Öğren'i o adımda açar.

Eylem türleri: `vurgula` (nabız ışığı), `ciz` (çizgi aşama aşama çizilir), `renk` (yesil/kirmizi/mavi/sari), `goster`, `gizle`,
`etiket`. Bir adımdaki eylemler cümle ilerledikçe birikir; ses cümle zamanlamasıyla eşzamanlıdır.

## 4. Komutlar

```
python3 meds/scripts/kmb/lottie_uret.py                 # Lottie videoları (ses varsa ses zamanlı); ses.py'den sonra yeniden çalıştır
python3 meds/scripts/kmb/dogrula.py                     # 0 HATA olmadan ses ve yayın yok (Lottie etiket kapısı dahil)
node meds/scripts/kmb/kare_onizle.mjs [ad… | konu]     # kare temas sayfası: her cümlenin karesi metinle göz denetimi (OUT=klasör)
bash meds/scripts/patoloji_cozucu/cozucu_ses_gpu.sh meds/scripts/kmb/ses.py 02   # EMA, GPU
```

## 5. Yeni ders ekleme sırası

1. Kaynağı `meds_temp/kmb/kaynak/` altına koy, ses kaydını yazıya dök.
2. `index.json`'da becerinin `durum`unu `hazirlaniyor` yap; `<kod>.json`'u hedeflerden başlat.
3. Gerekirse `sahneler.tsx`'e yeni sahne (her öge `id`'li, etiketi `lbl-<id>`).
4. `dogrula.py` 0 HATA → `ses.py <kod>` (GPU) → `npx vite build` → durum `hazir`.

## 6. Ekran ve hata istatistiği (2026-10-31, H459)

- Öğrenme yolu: İzle → Öğren → Hedefler → Sınav + **Eksikler** (`/dersler/kmb/<beceri>/eksik`).
- Öğren: adım başlığı + önceki/sonraki + adım şeridi (yeşil izlendi, kırmızı sınavda eksik), tüm adımlar açılır panelde;
  video + eşzamanlı metin (cümleye dokun → video o cümleden), düzen `@container kmb` (dar: alt alta, ≥860 px: yan yana).
- Oynatıcı (`LottieVideo.tsx`, H461): denetimler görüntünün üstünde, oynarken 3 sn sonra gizlenir. Dokunmatik: tek dokunuş
  denetimleri aç/kapat (oynatmaya/konuma dokunmaz), kenarda çift dokunuş ±10 sn (seri: her dokunuş +10), ortada çift
  dokunuş oynat/duraklat, basılı tut 2×, yana kaydır sar. Fare: tık oynat/duraklat, çift tık tam ekran. Orta sıra önceki
  cümle · oynat · sonraki cümle; cümle listesi ve hız menüsü; zaman çubuğu cümle parçalı + önizleme; hız/altyazı tercihi
  hatırlanır; bitişte geri sayım (`otoSonraki`, "Burada kal" iptal eder; `bekle` soruyu bekler).
- Öğren'de adım videosu bitince o adıma bağlı tek soru (`Eksikler.tsx::HizliKontrol`), cevap istatistiğe "video" kaynağıyla.
- Hata istatistiği (`kmbHata.ts`, `medsoru_kmb_hata_<kod>`, hesapla eşitlenir): vaka, OSCE sırası (basamak başına),
  kontrol listesi ("Atladım" = unutulan basamak), sahnede bul (görev başına ilk dokunuş), etiketleme (yapı başına ilk
  deneme), hedef anlatımı (öz değerlendirme). Kavram iki kez üst üste doğru yapılınca eksik listesinden düşer.
  `Eksikler.tsx`: özet, bölüm başına doğruluk, 14 gün, adıma göre eksikler, hedefli tekrar oturumu (en fazla 10 soru).
