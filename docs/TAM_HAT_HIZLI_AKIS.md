# Tam içerik hattı — hızlı ve hatasız akış (kullanıcı kararı 2026-10-28)

> Kural 21/22 katmanları ve kapıları DEĞİŞMEZ; bu belge onların **sırasını, paralelliğini, okumasını ve düzeltme biçimini**
> belirler. Ölçüt: kalite ve hız birlikte; kaliteden ödün verilmez. Kök neden kaydı: `KURUL2_YAPILMAYACAK_HATALAR.md` H123.

## 0.0 Tek hat + read-once bağlam (kullanıcı kararı 2026-11-16, ZORUNLU)

Sıra artık kafada/4 ayrı dosyada değil, **tek kaynakta**: `scripts/hat/tam_hat/mod.py` (katmanlar + kip). Koşucu runbook basar ve
hazırlık adımlarını çalıştırır:
```
python3 scripts/hat/tam_hat/kosucu.py <klasör> --ders <key> --mod <tam|tasarruf> [--calistir]
```
**Aynı kaynağı defalarca okuma YASAK (token israfı).** E1 paketi üretildikten sonra bir kez bağlam üretilir:
```
python3 scripts/hat/tam_hat/baglam.py <klasör> --ders <key> --mod <mod>   # <klasör>/baglam/kaynak.md + sema.md
```
- `baglam/kaynak_atom.md` (slayt dizini + bilgi paketleri + **atomlar**), `kaynak_hoca.md` (hoca vurguları + öğrenci önem notları),
  `kaynak_cikmis.md` (doğrulanmış çıkmış), `kaynak_uslup.md` (soru üslubu). Her aşama YALNIZ kendi dilimini okur (`baglam.py`
  `DILIM_ASAMA`): önem = atom+hoca+çıkmış, çıkmış analizi = çıkmış (+atom), örnek soru = atom+çıkmış+üslup. `kaynak.md` geriye
  uyum için dilimlerin birleşimidir; bütün okunmaz.
- `baglam/sema.md` = aşama çıktı şemaları + kapı komutları (33k şablon dosyası + kapı-kaynağı yerine ~0,2k kelime).
- **Gerçek ölçüm (k2-28, kelime, 2026-11-16):** kaynak.md 8.529 (hedeflenen ~2k DEĞİL) = atom 5.908 + hoca 2.148 + çıkmış 521 +
  üslup 63 (her dilimde ~45 kelime ortak başlık). Üç aşamada bütün okuma 25,6k → dilimle ~15,6k.
- **Kural girdisi (`kural_secici.py --oku`, dosyaların toplamı, kelime):** kaynak 12.575→7.690 · anlatım 14.598→6.967 ·
  ses 7.502→1.303 · çapa/çizim 11.625→5.563 · ders içerik 8.966→1.944 · Öğren 13.621→7.295 · örnek soru 15.217→5.815 ·
  PDF 8.588→2.310 · yayın 15.464→8.777. Aşama özetleri toplamı 67,3k→13,4k; kalan ağırlık standart belgelerdir
  (EL_KITABI 6,3k, OGREN_ETKILESIM 5,1k, DERS_STANDARDI 2,5k). İstem başına `kural_secici.py --ozet <aşama>` (≤300 kelime).

- **C6/C7 + ölçüm (2026-11-16):** E0 sonunda `hoca_kirp.py` → `hoca_dokum_kirpik.md` (değerlendirme HAM `hoca_dokum.json` okumaz;
  tek slaytın hamı `hoca_kirp.py <klasör> --ham <s>`) ve `iskelet.py uret` → `baglam/iskelet_<anlatim|ornek_soru|cikmis_analiz>.json`
  (kimlik/sayfa dolu; cümle/soru kimliği `iskelet.py numarala`; `<DOLDUR>` kalırsa anlatım/örnek soru kapısı HATA). Koşucu her
  aşamaya `manifest.py uret --kapi-sonucu` satırı, yayından önce `manifest.py goster --eksik` ve bağımlılık gruplarını
  (`mod.py BAGIMLILIK`) basar. `kosucu.py … --olc`: aşama girdisi tablosu → `meds_temp/hat_olcum/<key>.json`;
  k2-28 toplam ≈80,2k kelime (≈128k token; önceki 175k kelime ölçümü ham döküm + bütün kaynak.md + eski kural setini sayıyordu).

**Nereye baglam, nereye ham slayt (ölçümle, 2026-11-16):**
- **Örnek soru / önem / çözücü:** `baglam/kaynak.md` + `baglam/sema.md` + `docs/asama_kurallari/<aşama>.md` okur; 33k'lık örnek
  şablon dosyasını, kapı kaynağını, standart belgelerin tamamını OKUMAZ (birebir slayt zorunluluğu yok; şablon elenir). Gerçek
  girdi (k2-28 ölçümü): örnek soru ~23,9k kelime (kaynak.md 8,5k + şema 0,2k + kural 15,2k) → ~12,5k (dilim 6,5k + şema + kural 5,8k).
  Eski "~3,9k" rakamı gerçeği yansıtmıyordu.
- **Anlatım:** `sayfalar.json`'ı (TAM slayt) + `baglam/sema.md` + `anlatim.md` okur. `slayt.satir` çapası ve `--dogrula`
  satır-birebir kapısı tam slayt metnini GEREKTİRİR — `baglam/kaynak` yetmez ve kapıyı zayıflatır (`kaynak.md` yoksa satır
  denetimi atlanıyordu). Anlatımda kazanç şablon değil, **kural özeti sıkıştırmasıdır**.

**Önemli — token'ın asıl belirleyeni:** Alt-ajan tokeni girdi boyutundan çok **araç-çağrısı/iterasyon sayısına** bağlıdır
(ölçüm: aynı ders 12 çağrıda 132k, 36 çağrıda 181k). Asıl tasarruf kapı-fail yeniden-yazımını azaltmaktır (ilk-geçiş doğruluğu,
net şema). baglam + sıkıştırılmış özet girdiyi küçültür ama dibi iterasyon belirler. Ders kilidi + hat-başı özet kapısı E0'da otomatiktir.

**Anlatım TEK KAPI (iterasyon + bütünlük, ZORUNLU):** 4 ayrı kapı yerine tek komut —
`python3 scripts/hat/tam_hat/anlatim_kapi.py <v2 dizin> --sayfalar <sayfalar.json> --key <key>` (turet+dogrula+metin_denetle+
turkce_uslup birlikte, TÜM sorunlar bir seferde). Kapı `kaynak.md` yoksa `sayfalar.json`'dan üretir → `slayt.satir` birebir
denetimi ASLA atlanmaz. (Ölçüm: baglam-yalnız anlatım, `kaynak.md` yokken 46 hatalı satırı sessizce geçiriyordu — bu kapı yakalar.)

### 0.0c Sentez okuma kipi — YALNIZ yönetici açarsa (2026-11-17, deneysel)

`kosucu.py … --sentez` verilmezse hiçbir şey değişmez (standart: alt ajan her sayfanın `op/s-NN.png`'sini açar, H111).
Açılınca `scripts/hat/tam_hat/sentez.py <klasör>` → `baglam/sentez.md` (sayfa metni + sayfa başına `GÖRSEL: aç|gerekmez`),
`temas_N.png` (aday sayfaların 3×3 küçük resim ızgarası), `sentez.json`. PDF okuyan aşama önce temas sayfasına bakar, yalnız
tanısal görüntü/şema/resim-tablo sayfasının tam PNG'sini açar, seçimini `sentez_secim.json`'a yazar. Kapılar/denetçi aynen.
- **MarkItDown (microsoft/markitdown 0.1.9, `.venv-markitdown`) PDF'te KULLANILMAZ:** k2-13'te pdftotext 568 kelime ↔ MarkItDown
  779 kelime; fazlası çok sütunlu madde imlerinden uydurulan sahte tablo satırları, sayfa sınırı da yok. Yalnız PDF dışı ek kaynak
  (pptx/docx/xlsx/html) varsa `baglam/ek_<ad>.md`'ye çevirir.
- **Ölçüm (k2-13, 20 sayfa, Haiku, aynı atom çıkarma görevi):** standart 20 PNG açtı; sentez 2 temas + 12 PNG (−%40 görsel).
  Önbellek yazımı 463k → 281k (−%39), önbellek okuma 1,79M → 1,94M, çıktı 65k → 81k; ağırlıklı maliyet (yazım×1,25 + okuma×0,1 +
  çıktı×5) ≈ 1,09M → 0,95M = **−%12**. Kalite eşit (atom 79 → 107, aynı sayfalarda aynı bilgiler; görsel tanımları denk).
  **%50 hedefi tutmadı**: maliyetin çoğu görsel değil, alt ajanın tur başına yeniden okunan bağlamı ve çıktısı. Görsel ağırlıklı
  (patoloji/radyoloji) derste kazanç daha az, saf metin slaytlı derste daha fazla olur. Varsayılan yapılmaz.

## 0. Tasarruf kipi (kullanıcı kararı 2026-11-07)

Kullanıcı "tasarruf modunda" / "tasarruf kipiyle" derse hat `--mod tasarruf` ile yürür: `python3 scripts/hat/tam_hat/hazirlik.py <klasör> --ders <key> --mod tasarruf`
(`<klasör>/mod.json` yazılır; katman tablosu `python3 scripts/hat/tam_hat/mod.py --rapor <klasör>`, tek kaynak `scripts/hat/tam_hat/mod.py`).
- **Yapılır:** sesli ders (anlatım, EMA, cümle/kelime zamanı + PDF metin vurgusu/takip), çıkmış chip + ayrıntılı çıkmış analizi + ders analizi,
  terim/kısaltma, önem listesi, örnek sorular + sesli çözücü + EMA sesi, patoloji hoca soruları kartı + sesli hoca çözücü, ders içerik paketi (betik), kapılar + tek denetçi, yayın.
- **Yapılmaz (atlandı — tasarruf kipi):** çapa + canlı çizim (E4 tümüyle), ara resim katmanı (`src/data/ara_resim`), ara soru sayfası,
  atomik envanter, ders PDF tasarım taraması, Öğren destesi, quiz. Eksiklikleri dersi tamamlanmamış saymaz.
- Kalite düşürülmez: kapılar 0 HATA, tek denetçi, kural 7/14/26/28/29 aynen. Alt ajan en çok 2 aynı anda; yeniden yazım yalnız hatalı parça.

## 1. Evreler ve paralellik

> §0.0 `kosucu.py` bu tabloyu **tek kaynaktan (`mod.py`)** okuyup sıralı runbook olarak basar — aşağıdaki evre/paralellik
> onun yürüttüğü detaydır (çelişki değil). E1 paketinden sonra `baglam.py` çalışır; E2+ aşamalar `baglam/`'ı okur.

| Evre | İşler (aynı anda) | Kaynak payı |
|---|---|---|
| **E0 Hazırlık** (LLM yok) | `python3 scripts/hat/tam_hat/hazirlik.py <klasör> --ders <key>`: hoca dökümü (GPU) ∥ sayfa metni ∥ sayfa görüntüleri ∥ öğrenci notu ∥ çıkmış aday | GPU tek iş; CPU en çok 2 iş, her biri `CPUQuota=200%` `MemoryMax=2G` |
| **E1 Kaynak** | değerlendirme paketi ∥ `soru_uslup_ornek.py` | — |
| **E2 Yazım** (alt ajanlar) | anlatım metni ∥ ~~Öğren destesi~~ (ASKIDA 2026-11-02, kullanıcı aksi demedikçe üretilmez) ∥ örnek sorular + çözücü ∥ atomik envanter | En çok **3 alt ajan** aynı anda (RAM 15 GB, Claude oturumları korunur) |
| **E3 Ses + yerleşim** | EMA sesi (GPU) → cümle/kelime zamanı ∥ çıkmış chip ∥ terim/kısaltma ∥ ders içerik paketi | GPU işleri sırayla (tek kart) |
| **E4 Çapa + çizim** | çapa → çizim partileri (bölüm başına alt ajan, en çok 3) | — |
| **E5 Kapılar + tek denetçi** | bütün betik kapıları ∥ `pdf_tarama.py` → **tek denetçi** | — |
| **E6 Yayın** | commit → `dagit.sh` → canlı doğrulama | — |

- Hoca dökümü E2'yi beklemez: anlatım taslağı slayttan başlar, hoca vurgusu döküm bitince yalnız ilgili paragraflara eklenir.
- GPU işi aynı anda tek olur (döküm, EMA, kelime zamanı sıraya girer); hepsi `meds-gpuguard` altında, çekirdek saati
  **≤2500 MHz** (AGENTS §10 altıncı istisna; kalıcı tavan `sudo nvidia-smi -lgc 300,2500`).
- Ölçüm (2026-10-28, k2-08): 3 dk ses GPU'da 11 sn; E0'ın tamamı (döküm hariç) 118 sn.

## 2. Okuma haritası — büyük dosya her seferinde okunmaz

Her alt ajan istemine yalnız kendi aşamasının listesi konur:

```bash
python3 scripts/hat/tam_hat/kural_secici.py --oku <kaynak|anlatim|ses|capa_cizim|ders_icerik|ogren_deste|ornek_soru|pdf_tasarim|yayin>
```

- Liste = `docs/asama_kurallari/<aşama>.md` (defterin o aşamaya ait maddeleri, kural satırları aynen) + `genel.md` + aşamanın
  standart belgeleri. 115 maddelik defter yerine aşama başına 13–39 madde.
- Hat başında `kural_secici.py --denetle`; defter değiştiyse özet yeniden üretilir (`kural_secici.py`). Özet elle yazılmaz.
- Defterin tamamı yalnız yeni hata maddesi yazılırken ya da özet bir kuralı belirsiz bıraktığında açılır.

## 3. Kısmi düzeltme ve ±%10–20 tolerans

- Kapı ya da denetçi bir **bölüm/kayıt/soru** kimliği verir; yalnız o parça yeniden yazılır, geri kalan dokunulmaz.
  Alt ajana bütün taslak değil, hatalı parça + kapı mesajı + o parçanın kaynak sayfaları verilir.
- **Sayısal hedeflerde** (kelime aralığı, öge sayısı, soru sayısı, kalıp payı, kök uzunluğu, süre) hedeften ±%10 sapma — sesli ders anlatımında kelime/süre/örnek sayısı için ±%20 (kullanıcı, 2026-10-28) —
  kabul edilir; dışındaysa yalnız sapan bölüm düzenlenir (ör. soru kalıp payı: rapor "3 soru olumsuz köke çevrilmeli" der,
  yalnız 3 soru yeniden yazılır).
- **Tolerans yalnız sayısaldır.** Tıbbi yanlış, kaynakta olmayan bilgi, ileri sızıntı, ders çağrıştıran kök, şık
  standardı ve Türkçe üslup ihlalinde tolerans yoktur: kapı 0 HATA olmalıdır.

- **Önce plan:** anlatım yazarı metinden önce `anlatim_plani.md` kurar (`ANLATIM_KURGU_STANDARDI.md` §2); doğru plan
  tek geçişte kabul edilir, LLM yeniden çağrısı ve limit tüketimi azalır.

## 4. Metin ve veri çıkarma

- Sayfa metni `sayfalar.json` (pdftotext, sayfa sayfa) ve görüntüler `op/s-NNN.png` E0'da bir kez çıkarılır; alt ajanlar
  bunları okur, PDF'i yeniden ayrıştırmaz. Şekil/tablo içeren sayfa görüntüden okunur (H111).
- Her kayıt `s` (sayfa) taşır; **`kaynak_kapisi.py <json> sayfalar.json`** içeriğin o sayfada (±1) geçtiğini denetler.
  Şekilden okunan kayıt `gorsel: true` alır ve denetçi gözle doğrular.
- k2-08 sınamasında kapı 552 kayıttan 41'ini işaretledi (ör. genetik dersinde "Taşıyıcı" patojen taşıyıcısı diye
  tanımlanmış) — yazım sırasında çalıştırılırsa geri dönüş baştan önlenir.

## 5. Örnek soru üslubu

1. `python3 scripts/hat/tam_hat/soru_uslup_ornek.py <klasör>` → `soru_uslubu.json`: konuya en yakın **8** çıkmış (her kalıptan en
   az biri), kalıp payları ve ortalama kök uzunluğu. Yazar yalnız bunu okur.
2. Yazım kuralları: `docs/SORU_USLUBU.md`.
3. Kapı: `python3 scripts/hat/tam_hat/soru_uslup.py ornek_sorular.json --uslup soru_uslubu.json` 0 HATA (ayrıca mevcut
   `sik_aciklama.py`, `cozucu_dogrula.py`).

## 6. PDF tasarım taraması

`npx tsx scripts/ders_pdf.mts <key> <çıktı.pdf>` → `.venv-ocr/bin/python -I scripts/hat/tam_hat/pdf_tarama.py <çıktı.pdf>`:
boş sayfa, kenar taşması, üst üste binen yazı, harf harf kırılma HATA; seyrek sayfa UYARI. Rapor sayfa numarası verir;
yalnız o sayfanın kartı/tablosu düzeltilir.

## 7. Tek denetçi

Katman başına ayrı denetçi yerine ders başına **tek bağımsız denetçi** alt ajanı, betik kapıları 0 HATA olduktan sonra
bir kez çalışır. Girdisi: bütün katmanların dosya yolları, `sayfalar.json` + `op/`, `kural_secici.py --oku` listelerinin
birleşimi. Bakacakları, bu sırayla:

1. Tıbbi doğruluk ve kaynak sadakati (kapının atladığı `gorsel` kayıtlar dahil).
2. Öğrenci rolünde anlaşılırlık: ilk geçişte tanımsız terim, aynı sözcüğün iki anlamı (H112).
3. Soru: kazanım değeri, çeldirici gücü, çıkmış üslubu.
4. Türkçe üslup ve dolgu.

Çıktı: `denetim.json` → `{"karar": "GEÇER|KALIR", "bulgular": [{"katman", "kimlik", "sorun", "oneri"}]}`. KALIR ise yalnız
bulgulardaki kimlikler §3'e göre düzeltilir, denetçi yalnız o kimlikleri yeniden denetler (bütün ders değil).

## 6. Hoca profili adımı (2026-10-29)
E1'e `profil_oku.py --ders <ders> --konu <konu>` eklenir (LLM yok, <1 sn); çıktı yalnız yazım ve önem alt ajanlarının istemine konur (≤30 satır).
E2 örnek soru çıkışı `soru_uslup.py` + **`profil_kapisi.py`** kapılarından geçer; kısmi düzeltme kuralı aynen (kapı "N soru şu türe çevrilmeli" der).
Önem listesinde profilden önerilen madde `kanit: profil` etiketi taşır. Ayrıntı: `HOCA_USLUBU_YONTEMI.md` §4.1.


## Hoca tahmin adımı (2026-10-29)
E2 önem listesi öncesi: `scripts/uretim/hoca_profili/tahmin_girdisi.py` (profil + aday satırlar + K) → yazar `docs/HOCA_TAHMIN_REHBERI.md` v6 ile K tahmin; kör sınama %75–80 (docs/HOCA_USLUBU/TEST_TURLARI.md). Tahmin satırları önem listesine `kanit: profil` ve gerekçeyle girer.
E2 ara sorular (kural 27): tahmin satırlarından seçilen slaytlar için `scripts/uretim/hoca_ara_soru/TALIMAT.md` (iskele → yazım → `kur.py dogrula` → denetçi); E3'te EMA GPU + `dogrula --ses`.

## Öğrenci önem notu adımı (2026-10-30, AGENTS 28)
E0 `hazirlik.py` → `ogrenci_onem.json` (geçmiş yıl öğrenci derlemesinin A/B birimleri bu yılın sayfalarına eşlenmiş). E2 yazarlarının
istemine `oku.py --ders <k2-xx>` özeti (≤45 satır) + `docs/OGRENCI_ONEM/<ders>.md` bağlantısı girer; önem listesi, anlatım, örnek soru ve ara
soru bu belgedeki öncelik haritasına ve soru payına uyar. E5'te `scripts/uretim/ogrenci_onem/kapi.py <ders>` 0 HATA (eksik bilgi listesi §3 kısmi
düzeltmeyle yalnız o bilgilere uygulanır). Yöntem: `docs/OGRENCI_ONEM_YONTEMI.md`.
