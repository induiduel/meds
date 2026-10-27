## 2026-10-27 — Quiz her ders için açık + örnek soru kapsamı (k2-05, k2-08)
- Farmakoloji kapsam kilidi kalktı (`quiz_motoru/kapsam.py`, AGENTS kural 19); `quiz_dogrula.py` artık `sik_aciklama` standardını da denetler; elle üretilen ders yayınlı sesli dersle "tamamlandı" sayılır.
- `quiz_havuzu.json` (meds_database_v2/ders_isci/yayinlanan/elle-k2-05|k2-08/): k2-05 116 atom/232 soru, k2-08 205 atom/410 soru, 0 HATA. Kaynakta çelişkili/görsele bağlı/kanıtı eşleşmeyen atomlar havuza alınmadı (k2-05: 12, 33, 36; k2-08: 056, 057, 068, 083, 093, 131, 188, 198, 211). Quiz havuzu henüz sitede bir ekrana bağlı değil.
- Örnek soru kuralı (önem tamamı + ayrıntı ~%40, 50<n≤100; `KURUL2_DERS_STANDARDI.md` §10.8, bundan sonra her ders): k2-05 34→69, k2-08 43→95, canlıda (onem 484). `s16` kazanım tavanı `100-3*(kaz-1)`. k2-05'te monoparezi/stupor vb. tanımlar slaytta yalnız terim; açıklamalar genel tıp bilgisinden.

## 2026-10-27 — k2-05 Nörolojik Muayene Faz C: çizim, önem/çözücü/asistan
- Çizim 63 (52 kontur + 11 şablonlu panel; `data/sesli_anlatim/cizim/k2-05-norolojik-muayene.json`), kapılar 0 HATA; önem 42 madde, çözücü 20 soru, asistan 33 nokta (`src/data/k2noroloji_*/2n03.json`), EMA sesi (çözücü 181, asistan 183 klip); quiz envanteri 119 atom.
- Hata H116: birleştiriciler branştaki eski dersin dosyalarını da yeniden yazıyor; elle zincirde yalnız yeni ders dosyaları sahnelenir.



## 2026-10-27 — Kurul 2 k2-08 Beyin ve İskelet Sistemi Gelişimi Genetiği (Tıbbi Genetik 1) — Faz B (aşama 7–11) tamam
- Anlatım: 16 bölüm · 86 paragraf · 422 cümle · 5.611 kelime (≈50 dk); `metin_denetle` 0 HATA, `konusma_v2 --dogrula` 0 HATA, bağımsız öğrenci denetçi tur 1 KALIR → düzeltme → tur 2 GEÇER (H112).
- Hocanın sınav özeti (32:36–36:50): HOX/OTX/MSX/PAX6 (s10,12,13,15), holoprozensefali oluşum+hasar, trizomi 13/18, üç tip (s23–25), lizensefali (s26), somit/kraniyofasiyal hastalık adları (s31,34,35,37,39), kraniyosinostoz 3 tip (s41), displazi tip adları/FGFR3 (s50,51) ilgili paragrafta + son bölümde özetlendi; 1–44. slayt için "hoca anlattı" yok (kayıt s.45'ten başlıyor). Çıkmış `dogrudan`: HPE siklops (s24), DMD en sık MD (s80); chip 8 soru (6 ilişkili).
- Yayın: Öğren destesi (87 slayt, `--oyun-zorunlu --kurul2` 0 HATA), ders notu, 43 örnek soru, 160 sözlük terimi (`yayinla.py --yerel`), Oracle `ders-ekle` + EMA (21 parça, 2369 sn), cümle/kelime zamanı, anlamsal çapa 422 cümle %98 (0 HATA), PDF işareti kapsama %98, terim 242, kısaltma 75 (H110), `takip_kapisi` 0 HATA. Çizim, önem/çözücü/asistan, quiz, dağıtım Faz C'de.
- Yeni hatalar: H110 (kısaltma elle sözlüğü), H111 (alt ajan çapa indeks kayması), H112 (anlatım denetçi bulguları).

## 2026-10-27 — Yeni PDF standart akışı
- `docs/KURUL2_DERS_STANDARDI.md` §9: yeni PDF geldiğinde karşılama/sınıflandırma (sınama kuralı), üretim, yayın sırası (H97/H99), kayıt. AGENTS.md başına işaret eklendi (AGENTS.md git dışında).

## 2026-10-27 — Sesli ders: çizimsiz resimde zoom takılı kalıyordu
- Belirti: resimde çizim yokken sayfa yakınlaşmış (is-yakin) halde kalıyordu.
- Kök neden: `CizimLayer` kaldırılırken temizlik `kokRef.current` üzerinden sayfayı buluyordu; React ref'i o an boşalttığı için (null) yakınlaşma sınıfı/`--yakin-t` hiç silinmiyordu.
- Çözüm: sayfa öğesi bağlanırken yakalanır, kaldırmada doğrudan sınıf ve değişken silinir. Önleme: unmount temizliğinde `ref.current` okunmaz, öğe önceden yakalanır.

## 2026-10-27 — k2-08 Beyin ve İskelet Sistemi Gelişimi Genetiği Faz C (aşama 12–16)
- Çizim 37 (14 kontur, 1 odak oku, 22 şablonlu panel; yeni şablon `tip_ozellik`); anlam denetimi iki bağımsız geçiş (23 panel tamam, düzeltmeler uygulandı), `cizim_kapisi` 0 HATA, `panel_sinama` 366/567/1100 px 0 hata. Resim sayfaları 24, 27, 68, 73, 78, 81, 82; s.15 fotoğrafları (aniridi) emin olunamadığı için çizilmedi. P81.C2 çapası `madde`den `resim`e çevrildi (Gowers fotoğrafı), işaret yenilendi.
- Önem 44 madde (hoca sınav yerleri + çıkmış `dogrudan` HPE siklops/DMD en üst bant), çözücü 28 soru, asistan 38 nokta; üç doğrulayıcı 0 HATA, 2 bağımsız denetçi GEÇER; ses EMA GPU (çözücü 252, asistan 244 klip). Quiz envanteri 227 atom (slayt iç çelişkili 13 atom `quiz_kullanimi: yasak`); quiz sorusu yok (yalnız Farmakoloji).
- Yeni hatalar: H114, H115.

## 2026-10-27 · Ders içerik sayfaları (k2-05 ilk ders) — yerel; commit/dağıtım yok
- **Belirti:** Ders ayrıntısında yalnız sesli ders/Öğren/çıkmış/yorum vardı; dersin terim, hastalık, spot, tablo, soru, kart içeriği ayrı sayfalarda yoktu.
- **Kök neden:** Ders paketi (taslak) üretilmişti ama ders sayfasına bağlanan ders-bazlı içerik katmanı yoktu.
- **Çözüm:** `scripts/ders_icerik_uret.py <kod> <key> <önem kodu> <önem dizini>` → `src/data/ders_icerik/<key>.json`; `DersIcerikV15.tsx` + `dersIcerik.ts` (`?b=terimler|hastaliklar|bilgiler|tablolar|sorular|kartlar`), `DersDetayV15` satırları paket varsa görünür. Yeni derse: betiği çalıştır, başka kod gerekmez.
- **Açık:** hasta/hastalık alanları yalnız taslakta dolu olanları gösterir; commit/dağıtım için `onem`+1 gerekir.

## 2026-10-27 · Ders içerik paketi 6 Kurul 2 dersine + sesli soru çözücü erişimi
- 6 dersin (k2-01,02,03,04,07,08) paketi `scripts/ders_icerik_uret.py` ile yayındaki deste/havuz/terim katmanından üretildi; kapı `ders_icerik_dogrula.py` (çözücü yoksa HATA). **k2-01'in Öğren destesi, havuzu ve çözücüsü yok → paketi yalnız terim/kısaltma; kapı HATA verir, tam içerik işçisi üretmeli.**
- Yeni sayfalar: Sıralamalar ve listeler (sıra türü numara/alfa/azalan/madde), Mini sorular; karşılaştırma tablosunda terazi simgesi.
- Sesli soru çözücü erişimi: ders ayrıntısı satırı, oynatıcıda "Önce soru çözücüyle dene" (başlamadan), ders bitince "Ders bitti" kartı (`cd:bitti` olayı, `dersCozucu.ts` başlık eşlemesi).
- Talimatlar: AGENTS kural 23, el kitabı §19 11a/11b, `docs/DERS_ICERIK_BICIMI.md`.
- Önleme: yeni dersin çözücüsü `src/data/k*_cozucu/index.json`'a, başlığı ders başlığıyla birebir, eklenmeden erişim satırı görünmez.

## 2026-10-27 · k2-01 Nörolojik Hastaya Yaklaşım — tam hat (AGENTS kural 22), yayında
- Katmanlar: Öğren destesi (14 slayt + oyun sayfası), 51 örnek soru (kaynak 9 slayt: standart 50–100'e giriyor), sözlük, hastalıklar, bilgi havuzu, ders içerik paketi (`ders_icerik_dogrula` 0 HATA), önem listesi 2n01 (24 madde), sesli çözücü 2n01 (23 soru, 207 EMA klibi GPU), sınav asistanı 2n01 (23 soru, 190 klip). Sesli ders/çıkmış/terim/kısaltma/çizim önceden vardı. Quiz envanteri: Farmakoloji dışı (kural 19) — atomik envanter paket.json'da.
- Denetim: yazar + 2 bağımsız denetçi; ikincisi slayt 1 klinik kararda **ters bayrak** buldu (H120) → düzeltildi, `validate_learning_decks.py` `klinik-karar-bayrak` kapısı eklendi.
- `birlestir.py`/`asistan_birlestir.py` 2n02'yi değiştiriyordu (kaynak çıkmışlar yok) → 2n02/2n03 dosyaları korundu, yalnız 2n01 + index girdileri alındı. Önleme: tek ders eklerken birleştiriciyi tüm dizinde çalıştırıp farkı kontrol et, değişen eski dersi geri yükle.
- Açık/küçük (denetçi GEÇER-dışı notlar): örnek soru Q14 A şıkkı (epilepsi) ayırt ediciliği, Q25 D/kuyruk cümleleri, asistan 2n01-01 cümle 2 ("lokalizasyon ve nedeni" öykü unsuru gibi okunuyor), paket `medicalTerms` slayt 7 piramidal/serebellar. Slayt dışı çeldirici (Guillain-Barré, Alzheimer, ALS) açıklamaları ders kitabı düzeyinde tek cümle.
- Saat kilidi (`nvidia-smi -lgc`) bu oturumda uygulanamadı (sudo); koruyucu etkindi.
