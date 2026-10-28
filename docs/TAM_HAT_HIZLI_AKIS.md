# Tam içerik hattı — hızlı ve hatasız akış (kullanıcı kararı 2026-10-28)

> Kural 21/22 katmanları ve kapıları DEĞİŞMEZ; bu belge onların **sırasını, paralelliğini, okumasını ve düzeltme biçimini**
> belirler. Ölçüt: kalite ve hız birlikte; kaliteden ödün verilmez. Kök neden kaydı: `KURUL2_YAPILMAYACAK_HATALAR.md` H123.

## 1. Evreler ve paralellik

| Evre | İşler (aynı anda) | Kaynak payı |
|---|---|---|
| **E0 Hazırlık** (LLM yok) | `python3 scripts/tam_hat/hazirlik.py <klasör> --ders <key>`: hoca dökümü (GPU) ∥ sayfa metni ∥ sayfa görüntüleri ∥ öğrenci notu ∥ çıkmış aday | GPU tek iş; CPU en çok 2 iş, her biri `CPUQuota=200%` `MemoryMax=2G` |
| **E1 Kaynak** | değerlendirme paketi ∥ `soru_uslup_ornek.py` | — |
| **E2 Yazım** (alt ajanlar) | anlatım metni ∥ Öğren destesi ∥ örnek sorular + çözücü ∥ atomik envanter | En çok **3 alt ajan** aynı anda (RAM 15 GB, Claude oturumları korunur) |
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
python3 scripts/tam_hat/kural_secici.py --oku <kaynak|anlatim|ses|capa_cizim|ders_icerik|ogren_deste|ornek_soru|pdf_tasarim|yayin>
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

1. `python3 scripts/tam_hat/soru_uslup_ornek.py <klasör>` → `soru_uslubu.json`: konuya en yakın **8** çıkmış (her kalıptan en
   az biri), kalıp payları ve ortalama kök uzunluğu. Yazar yalnız bunu okur.
2. Yazım kuralları: `docs/SORU_USLUBU.md`.
3. Kapı: `python3 scripts/tam_hat/soru_uslup.py ornek_sorular.json --uslup soru_uslubu.json` 0 HATA (ayrıca mevcut
   `sik_aciklama.py`, `cozucu_dogrula.py`).

## 6. PDF tasarım taraması

`npx tsx scripts/ders_pdf.mts <key> <çıktı.pdf>` → `.venv-ocr/bin/python -I scripts/tam_hat/pdf_tarama.py <çıktı.pdf>`:
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
