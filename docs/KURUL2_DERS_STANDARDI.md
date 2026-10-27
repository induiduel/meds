# Kurul 2+ ders standardı — her ders için yapılacakların tamamı (tek kaynak)

> Kullanıcı kararı 2026-10-27: "Bundan sonra ekstra bir şey yazmama gerek kalmadan yapılacaklar belli olsun. Hata istemiyorum."
> Kullanıcı yalnız **hangi dosyanın hangi ders olduğunu** söyler; aşağıdaki her şey sormadan, eksiksiz ve kapılardan
> 0 HATA ile geçerek yapılır ve canlıya alınır. Ayrıntılı kurallar bağlantılı belgelerdedir; çelişkide bu belge + AGENTS.md esastır.
> İşletim adımları (komutlar): `KURUL_OTOMASYON_EL_KITABI.md` §19. Hata defteri: `KURUL2_YAPILMAYACAK_HATALAR.md` (H1–H95).

## 0. Değişmez ilkeler
1. **LLM/API otomasyonu yok** (AGENTS kural 20): işçi, zamanlayıcı, `claude -p` yok. Ders, kullanıcı komutuyla bu oturumda
   (gerekirse alt ajanlarla) üretilir. `otomasyon/llm_kilit.py` gevşetilmez.
2. **Arşiv arşivde kalır:** `y25-*` (2025-26) içeriği yeni derse kopyalanmaz; yeni ders bu yılın PDF'inden sıfırdan.
3. **Uydurma yok:** her bilgi slayt, öğrenci notu ya da doğrulanmış çıkmışa dayanır. Çıkmış = ham sınav belgesinde yeri
   gösterilen soru (H83/H84); banka etiketi kanıt değildir.
4. **Okumayı bozan hiçbir şey yapılmaz:** çizim, zoom, panel, işaret öğrencinin okuduğu yazıyı ve anlatılan bölgeyi örtmez.
5. **Sade, güvenilir, kusursuz:** kapısı olmayan katman yayına girmez; kapı eşiği gevşetilmez; hata bulunursa kök neden
   hata defterine + önleme kuralı (AGENTS başı).

## 1. Girdiler (her ders)
| Girdi | Nereden | Eşleme |
|---|---|---|
| Bu yılın orijinal ders PDF'i | Okul Drive'ı (`1ozu5KiLZjFd4YKNMZ0bSRvLVV6b7lv0W`, `Kurul N/<Branş>/`) | ders kayıt defteri `src/data/dersler/kN.json` |
| Öğrenci notu (işaret, çizim, el yazısı PDF) | Öğrenci Drive'ı (`17K7doMGg0xupQekTD5_Vz9xMXc5gd7BA`) | **sayfa başlıklarıyla** (dosya adı farklı olabilir) |
| Hoca ses kaydı | Öğrenci Drive'ı | kullanıcının söylediği ders; döküm slaytlarla hizalanır |
| Çıkmışlar | Banka → ham belge doğrulaması | §3 |

Kullanıcı eşlemeyi söylediyse o esastır; yine de sayfa başlıkları içerikle doğrulanır, uyuşmazsa sorulur.

## 2. Aşamalar (sırayla; her biri kapısıyla)
| # | Aşama | Çıktı | Kapı (0 HATA) |
|---|---|---|---|
| 1 | Kaynakları indir, içerikle eşle | `meds_temp/ogrenci_ders/<ders>/` | başlık eşlemesi |
| 2 | Öğrenci notu: işaret + el yazısı **her sayfa görüntüsü okunarak** | paket `ogrenci_notlari` | `degerlendirme_dogrula.py` |
| 3 | Hoca kaydı dökümü (CPU) + slayt hizası | paket `hoca_vurgulari` (yalnız anlaşılan yerler) | anlaşılmayan döküm vurgu dayanağı olmaz (H22, H81) |
| 4 | Çıkmış eşleme (ham belgede yer + slayt kanıtı) | `cikmis_konum` (`s`,`kanit`,`kaynak`,`seviye`,`dogrulandi`) | `degerlendirme_dogrula.py` |
| 5 | Değerlendirme paketi: bilgi paketleri, atomik bilgi (ilaç/hastalık/belirti…) | `meds_database_v2/ders_bilgi/<ders>/degerlendirme/paket.json` | `degerlendirme_dogrula.py` |
| 6 | Ders paketi (ders işçisi TALIMAT.md biçimi): deste (Öğren), ders notu, **örnek sorular**, sözlük, hastalıklar, bilgi havuzu, çıkmış bağları | `ders_paketi.json`, `deck.json`, `ornek_sorular.json` … | `denetle.py`, `validate_learning_decks.py --oyun-zorunlu --kurul2`, `sik_aciklama`, `turkce_uslup` |
| 7 | Sesli ders metni (+ `konusma_v2`) | `metin/<key>.md` | `metin_denetle.py`, `konusma_v2.py --dogrula`, `turkce_uslup`, **bağımsız denetçi GEÇER** |
| 8 | Yayın: ders-ekle + Öğren destesi + PDF bağı | canlı ders | canlı API |
| 9 | EMA ses → cümle/kelime zamanı → PDF işareti | `ses/`, `cumle_zaman/`, `kelime_zaman/`, `isaret/` | **metin takipçisi kapısı §5** |
| 10 | Terim + kısaltma katmanı (kısaltma listesi slaytla okunur; branşa göre anlamı değişen için `kisaltma_elle/<key>.json`, H92) | `terim/`, `kisaltma/` | `terim_sozlugu.py dogrula`, `kisaltma_sozlugu.py` |
| 11 | Anlamsal çapa → Oracle'a yükle → `pdf_isaret.py --key <key> --zorla` (H93) | `capa/`, `isaret/` | `capa_dogrula.py` (≥%70, hedef %100) |
| 12 | Çizim (tasarım kataloğunun tamamı, §4) + bağımsız anlam denetimi | `cizim/` | `cizim_kapisi.py`, `panel_sinama.mjs` (3 genişlik) |
| 13 | Spot / önem, sınav asistanı, soru çözücü (branşta varsa) | `src/data/k2<brans>_*` | `onem/asistan/cozucu_dogrula.py`, `sik_aciklama.py` |
| 14 | Quiz envanteri (her ders); quiz soruları yalnız Farmakoloji (kural 19) | `atomik_bilgi_envanteri.json` (+ `quiz_havuzu.json`) | `quiz_dogrula.py` |
| 15 | Hastalık birleştirme, RAG vektörü (elle komut) | `diseases`, `rag_chunks` | ilgili denetleyici |
| 16 | Kayıt + `guncelleme_notu.json` onem+1 + commit + `dagit.sh` | canlı | canlıda §6 doğrulaması |

Bir aşama ders için uygulanamıyorsa (ör. branşta çözücü yok) nedeni değişiklik kaydına yazılır; sessizce atlanmaz.

## 3. Çıkmış soru kuralları
- Yalnız **ham sınav belgesinde bulunan** soru (belge + sayfa `kaynak` alanında). Gizli kopya, kaynağı bulunamayan,
  karantinadaki (`kaynak_bulunamadi`) soru eşlenmez. Hatırlama listesinden gelen sorunun şıkları "sonradan tamamlandı" diye belirtilir.
- Anlatımda "Bu bilgi çıkmış sınavda sorulmuştur" yalnız `seviye: dogrudan` eşlemede; "ilgili" eşleme vurgulanmaz.
- Slayt sağ üstünde yanıp sönen **Çıkmış** chip'i: dokununca ses durur, soru normal/tam ekran çözülür, kaynak satırı ve
  **"Çıkmış sorularda aç"** düğmesi görünür; kapatınca ders aynı saniyeden sürer.

## 4. PDF üstü işaret, çizim ve zoom (H85 — kullanıcı kararı 2026-10-27)
**Okumayı bozmamak her şeyin önündedir.**
- **Resim üstünde çizim mutlaka doğru yeri gösterir.** Kontur anlatılan yapının sınırını **tam kapsar**, biraz geniş
  çizilir (yapının dışına ~%6 pay; yapı kesilmez). Hatlar **keskin değil, yumuşak** (yumuşatılmış eğri + hafif yayılma);
  dolgu yapının üstünü **örtmez** (çok hafif ton, ≤%15), beyaz kalın hale yok.
- **Çizgi kalınlığı dinamiktir:** bölge küçüldükçe incelir (küçük yapıda ~1 px, büyük bölgede en çok ~2,4 px).
- **Kelime ↔ kelime ilişkisi için çizgi/ok çizilmez.** Yazı ilişkisi gerekiyorsa yalnız şablonlu panel (boş alanda).
  Ok yalnız resmin/şemanın içinde, iki görsel yapı arasında.
- **Okunabilir metinli tablolarda çizim ve zoom yok;** en çok satır/hücre **marker** (işaret katmanı) ile vurgulanır.
- **Zoom ölçülü ve doğru yere:** yalnız resim üstündeki tek, küçük bölgede (sayfanın ≤%20'si); en çok 1,6×; hedef çizimin
  kendi bölgesi (birleşik kutu sayfanın %20'sini aşıyorsa zoom yok); yazı slaytında, tabloda, panelde zoom yok.
- Panel ve etiket yazının/anlatılan bölgenin üstüne gelmez (CIZIM_KURALLARI §5); yalnız o an konuşulan cümlenin çizimi
  görünür (kural 18).
- Tasarım kataloğunun tamamı amaca göre kullanılır (`TALIMAT_CIZIM.md` 27–30).

## 5. Metin takipçisi (kelime/cümle takibi) güvencesi
Her derste yayından önce `scripts/sesli_anlatim/takip_kapisi.py <key>` **0 HATA**:
- kelime zamanlaması eşleşmesi ≥ %95; cümle başlangıçları artan, boşluksuz/çakışmasız; son cümle ses süresinin içinde,
- her cümlenin PDF işareti (`isaret`) var ve doğru sayfada (çapa ile aynı), kapsama ≥ %95,
- PDF sayfası ders PDF'inin kendisi (deste/hizalama aynı dosya, sayfa sayısı tutar).

## 6. Canlı doğrulama (dağıtımdan sonra)
`/api/canli-ders/<key>`: bölüm/paragraf, ses varyantı + süre, `isaret`, çizimli cümle sayısı, `cikmisKonum` (hepsi
`/api/past-exams/tek/<id>` 200 — gizli/birleştirilmiş kopya listeye girmez, H94), `terim`, `kisaltma`; `/api/lecture-pdf/deck/<deck>/0` 200; Öğren destesi açılıyor.

## 7. İçerik kuralları (özet; ayrıntı bağlı belgelerde)
AGENTS 1–9b (madde yapısı, sıfır tekrar, 60–250 kelime, müfredat sadakati, kronoloji/sıfır ileri sızıntı, 4–6 öge,
ders sonu oyunları), kural 14 (dolgu yasağı, şık açıklama standardı `SIK_ACIKLAMA_STANDARDI.md`, Türkçe üslup
`TURKCE_USLUP_STANDARDI.md`), Öğren rehberi `OGREN_ETKILESIM_REHBERI.md`, çizim `CIZIM_KURALLARI.md`.
