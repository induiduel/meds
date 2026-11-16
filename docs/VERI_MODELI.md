# Veri Modeli ve Yol Haritası (2026-11-16)

> Amaç: modeller en doğru veriyi en az tokenla bulsun; veri tek yerde dursun, kaybolmasın, hızlı okunup yazılsın;
> site, çevrimdışı paket, RAG parçaları ve arama motorları bozulmasın. Bu belge veri katmanının **tek karar kaynağıdır**.
> Kök neden kanıtları: `docs/HANTALLIK_KOK_NEDENLERI.md` §4, §10.

## 1. Katmanlar — hangi veri nerede yaşar

| Katman | Yer | Asıl kaynak mı | Kural |
|---|---|---|---|
| Sunucu kayıtları (havuz, çıkmış, kullanıcı, yönetim) | `data/*.json` | Evet | Yalnız sunucu yazar (atomik); meds-pg sorgulanabilir kopya |
| Siteye giden içerik | `src/data/` | Evet | Sunucu yalnız içerik katmanıyla yazar (`data/content/` farkları) |
| İkili/ses | `data/*/ses/`, `data/sesli_anlatim/` | Evet | Git dışı, Oracle'a rsync |
| Türetilmiş (yeniden üretilir) | `src/data/decks/`, `data/local_rag_chunks.jsonl`, `data/search/`, `~/.cache/meds/` | Hayır | Elle düzenlenmez, yedeklenmez |
| Çalışma/ara veri | `../meds_temp/<modül>/` | Hayır | `src/data` ve `data/` içine ara dosya yazılmaz |
| Arşiv (sıkıştırılmış, doğrulanmış) | `../_arsiv_veri/<tarih>/` + `MANIFEST.jsonl` | Yedek | `veri_bakim.py geri <yol>` ile geri alınır |
| Kullanıcı/kimlik/topluluk | meds-pg | Evet | `deploy/pg/sql`, göç `scripts/altyapi/db/goc.py` |

## 2. Modeller veriye nasıl erişir (token kuralı)

1. **Önce sorgu aracı:** `python3 scripts/altyapi/veri.py` — dev JSON'u açmak, `jq` ile taramak ya da grep'lemek yerine.
   - `veri.py ders k2-07` → dersin kayıt satırı + bütün katman dosyaları + eksik katmanlar (ders manifesti)
   - `veri.py bul "<sorgu>" [--tur ..] [--ders ..] [--kurul ..]` → kısa, sıralı sonuç
   - `veri.py al <tur> <id> [--alan a,b] [--kisa]` → tek kaydın tam içeriği (asıl kaynaktan)
   - `veri.py liste|say|--denetle`
   Dizin türetilmiştir (`~/.cache/meds/veri.sqlite`, artımlı); silinirse yeniden kurulur.
2. **Yazma yalnız depo/kapı üzerinden:** deste → `scripts/deste_deposu.py` / `src/services/desteDeposu.ts`; site içeriği →
   içerik katmanı; çıkmış → sunucu ucu. Monoliti doğrudan açıp yazan yeni kod YASAK (kapı D1/D5).
3. **Bütün okuma yasağı:** 5 MB üstü JSON hiçbir koşulda bütün okunmaz.

## 3. Değişmezler (bozulursa RAG/arama/çevrimdışı kırılır)

- Kayıt kimlikleri: ders `k<N>-NN`, ders kodu, soru `id`, `note.id`, `deckId`, `slideNumber`, `pageNumber`.
- RAG parça kimliği `chunk-<tür>-<kaynak id>…`; vektör önbelleği parça `hash`'ine (içerik md5) bağlı. Kaynak kayıt `id`'si
  değişmedikçe taşıma/bölme vektörleri bozmaz. Yola bağlı tek tür: `chunk-tr-<dosya adı>`.
- Sabit okunan yollar: `data/pastQuestions.json`, `data/lecture_notes.json`, `data/lectureSummariesCatalog.json`,
  `data/local_rag_chunks.jsonl`, `src/data/ornek_sorular/k<N>/*.json` (düz), `src/data/medical_glossary.json`, `data/search/`.
- Çevrimdışı gruplar yol desenine bağlı (`cevrimdisiKatalog.ts`): `summaries/`, `kazanimlar/(questions|lite)/`,
  `sinav_calisma/`, `ornek_sorular/`, `decks/items/<id>.json`.
- Bir kaynak yolu değişecekse önce `python3 scripts/altyapi/bag.py etki <yol>`; dinamik yollar (`k${k}`) bag'de görünmez, elle aranır.

## 4. Kayıp önleme kapıları

| Koruma | Yer |
|---|---|
| Atomik yazım (tmp + rename) | havuz, çıkmış, içerik katmanı, deste deposu, RAG parça dosyası |
| Boşla/küçülterek ezme freni | çıkmış kaydı, RAG budaması (tür %50'den fazla küçülürse silmez), içerik katmanı toplu silme freni (H559) |
| Kaçış kapıları (bilerek toplu silme) | `MEDS_RAG_BUDAMA_ZORLA=1` ve ilgili ortam değişkenleri — yalnız kullanıcı komutuyla |
| Yedek tavanı | `data/backups/catalog`: ad başına en yeni 1 kalır; diğerleri 30 günden eskiyse ya da en yeniyle sha256 aynıysa arşive |
| Arşiv = sıkıştır + sha256 doğrula + sonra sil | `scripts/altyapi/veri_bakim.py arsivle` (varsayılan kuru çalışma) |
| Günlük | sunucu `data/gunluk/veri-YYYY-MM.jsonl`, betikler `data/gunluk/betik-YYYY-MM.jsonl`; `python3 scripts/gunluk.py son|ozet` |
| Kapı | `python3 scripts/kapilar/yapi_koruma.py` (D1–D10), `python3 scripts/altyapi/veri_bakim.py denetle` |

## 5. Yol haritası

**Faz 1 — bu tur (2026-11-16):** sorgu aracı `veri.py`; ortak günlük; RAG atomik yazım + budama freni; katalog yedek tavanı;
`veri_bakim.py` (rapor/arşivle/geri/denetle) + kapı D10; ara monolit `sinav_calisma_k1.json` → `meds_temp`.

**Faz 2 — kopyaları bire indir (her biri ayrı, küçük iş):**
1. `pastQuestions.json` `src/data` aynası kaldırılır (asıl `data/`); iki `.mjs` yazıcı tek yola çevrilir.
2. Özetler: `lectureSummariesCatalog.json` (data + src) ve `summaries/kurul*.json` üçlüsü → tek kaynak + türetme.
3. `src/data/lecture_notes.json` (864 eski not; `data/lecture_notes.json` 2026-10-08'den beri onu gölgeliyor) — kullanıcı kararıyla arşiv.

**Faz 3 — deste monolitini parçalı arka uca geçir** (85 MB kaynak + 85 MB türev → deste başına tek dosya):
yalnız `deste_deposu.py` + `desteDeposu.ts` arka ucu değişir; ama şu noktalar birlikte uyarlanmadan YAPILMAZ:
içerik katmanı `relOf/farkYol` (dosya başına tek fark varsayımı), `icerik_katman.py` `VARLIK` eşlemesi,
`content-overlay-sync.sh` yolu, `splitLearningDecks` mtime denetimi, depo önbelleği/ETag, kapı D1 izin listeleri.
Sıra: çift yazım (monolit + parça) → karşılaştırma kapısı 0 fark → okuma parçaya → monolit arşive.

**Yapıldı — iskele (2026-11-16, varsayılan davranış DEĞİŞMEDİ):**
- Biçim (tek tanım `scripts/deste_deposu.py`): `<dizin>/_sira.json` = `{"bicim":1,"desteler":[{id,dosya,sha1[,deckId]}]}`
  (monolit sırası) + `<dosya>.json` = tek deste, monolitteki bayt biçimiyle (`json.dumps(ensure_ascii=False)`, girintisiz,
  varsayılan ayraçlar, sonda satır sonu yok — mevcut monolit `json.dumps(json.load(...))` ile bayt bayt aynı, kanıtlandı).
  Birleşim `"[" + ", ".join(parçalar) + "]"`. Dosya adı: kimlik `[A-Za-z0-9][A-Za-z0-9._-]*` ise kendisi, değilse `~<utf8 hex>`.
- `scripts/deste_bol.py bol|birlestir|dogrula|fark` (varsayılan hedef `../meds_temp/deste_parcali/desteler/`; `src/data`'ya yazmaz).
- `deste_deposu.py` parçalı arka uç: `MEDS_DESTE_PARCALI=1` + `MEDS_DESTE_PARCA_DIZIN` (yalnız `yol` verilmeyen çağrılar);
  `guncelle/sil` tek dosya + `_sira.json` (sıra en son / silmede önce), kilit aynı. Sınama `scripts/sinama_deste_parcali.py`.
- `desteDeposu.ts` parçalı OKUMA (aynı bayrak; katmanda deste farkı varsa KAPALI); yazım monolitte/katmanda.
- Kapı D1: parça dizini işaretlerini (`MEDS_DESTE_PARCA_DIZIN`, `deste_parcali`, `desteler/_sira.json`) yalnız depo modülleri anar.

**Yapıldı — geçiş zinciri (2026-11-17, varsayılan YİNE DEĞİŞMEDİ; hepsi bayrakla açılır):**
1. ✅ Çift yazım `MEDS_DESTE_CIFT_YAZ=1` (+ `MEDS_DESTE_PARCA_DIZIN`). Python: monolit asılken her `yaz_hepsi/duzenle/guncelle/sil`
   (doğrudan `yaz_hepsi` çağıran üretim betikleri dahil) monolitten SONRA `parcali_yaz` ile aynalanır; `PARCALI=1` + çift
   yazımda parçalar asıl, monolit birleşimden türetilir. Aynalama hatası asıl yazımı geri almaz → `gunluk.py` HATA
   (`deste_bol dogrula` uyarısı). Sunucu src/data'ya yazmaz (H580): `desteleriYaz` katmana yazar, ~3 sn sonra öteki taban +
   fark = yazılan liste denetlenir, ayrışma `veriOlayi('hata','deste-cift-yaz')`. Kanıt `scripts/sinama_deste_parcali.py`.
2. ✅ Katman farkı: **yeni biçim YOK.** Deste farkı zaten kayıt düzeyli (`bicim:'dizi'`, `anahtar:'id'`) → arka uçtan
   bağımsız. `contentOverlay.ts` `kaynakSaglayiciKaydet` ile yalnız TABAN değişir (parçalı kipte parça birleşimi;
   `donustur` + `resolveContent`); `desteDeposu.ts` parçalı kipte sağlayıcıyı kurar, katman farkı varken birleşik dosya
   parçalar + farktan üretilir. Oracle'daki mevcut `interactive_learning_decks.json.fark.json` olduğu gibi okunur; H559 freni
   aynen (prova: 30 eksik deste → karantina, silme sayılmadı). `icerik_katman.py` `uygula/denetle/goc` aynı kural
   (parçalı kipte taban/hedef parçalar, çift yazımda öteki taraf aynalanır).
3. ✅ `splitLearningDecks` `PARCALI=1` iken parçalardan okur, tazelik `_sira.json` mtime'ı. Kanıt: eski (HEAD) eklenti, yeni
   eklenti bayraksız ve bayraklı (parçadan) çıktı → `decks/` 188 dosya karması üçünde ve gerçek `src/data/decks` ile aynı.
4. ✅ `content-overlay-sync.sh` + `dagit.sh`: yalnız `MEDS_DESTE_PARCALI/CIFT_YAZ=1` iken (kapalıyken hiçbir süreç
   çalışmaz) `deste_bol.py durum` → dağıtım öncesi/sonrası (Oracle) `dogrula`; parça dizini `src/data/` altında olmalı
   (rsync zaten taşır). `bash -n` geçti; çalıştırılmadı.
5. ✅ Uçtan uca kuru prova (sunucu başlatılmadan, `meds_temp/deste_parcali/e2e/e2e.mts`): parçalı `desteleriOku` = monolit,
   `desteOku` tek dosya (≈10–40 ms), `desteleriYaz` (1 değişen + 1 yeni + 1 silinen) → fark anahtar=id; parçalar + fark =
   monolit + fark = yazılan liste; `icerik_katman.py uygula` farkı parçalara + türetilmiş monolite uygular, `_sira.json`
   doğru, `deste_bol dogrula` 0 fark.

**Varsayılanı çevirmek için kalan komutlar (KULLANICI ONAYIYLA, sırayla; her adımın kapısı `dogrula` 0 fark):**
```bash
python3 scripts/deste_bol.py bol --kalici --hedef src/data/desteler        # ilk bölme (git'e eklenir, yol listesiyle)
python3 scripts/deste_bol.py dogrula --hedef src/data/desteler              # 0 fark
# yerel .env + Oracle .env (konteyner):  MEDS_DESTE_CIFT_YAZ=1  MEDS_DESTE_PARCA_DIZIN=src/data/desteler
systemctl --user restart meds-web                                            # yerel; sonra bir süre çift yazımla çalış
# commit + push (onem+1) → MEDS_DESTE_CIFT_YAZ=1 MEDS_DESTE_PARCA_DIZIN=src/data/desteler bash deploy/oracle/dagit.sh
ssh medsor-oracle 'cd medsor/meds && python3 scripts/icerik_katman.py denetle'   # 0 HATA
# geçiş: iki .env'e MEDS_DESTE_PARCALI=1 ekle (parçalar asıl, monolit türetilir) → yeniden başlat + dağıt + dogrula
# bir dağıtım süresince sorunsuzsa: MEDS_DESTE_CIFT_YAZ kalkar, monolit `veri_bakim.py arsivle` ile arşive,
# D1 monolit adını anan kodu HATA sayar (adım 6 eski plan); bayrak kodu tek yola indirgenir.
```
**Riskler:** (a) `src/data/desteler/` hiçbir ön yüz `import.meta.glob` kapsamında değil (2026-11-17 denetlendi; yeni glob eklenirse
yeniden bak). Bayraktaki göreli yol sürecin çalışma dizinine göre çözülür (meds-web/konteyner `meds/` kökünde çalışmalı). (b) Çift yazımda girintili `yaz_hepsi(girinti=…)` monolitle bayt eşitliğini
bozar (günlüğe UYARI). (c) Parçalı kipte Oracle'da `_birlesik` her `_sira.json` değişiminde yeniden üretilir (85 MB yazım).
(d) Python ve sunucu aynı parça dizinine aynı anda yazmaz (sunucu yalnız katmana yazar), ama iki Python yazıcısı kilit paylaşır
(`<monolit>.lock`); `DESTE_DOSYASI` farklıysa kilit ayrışır.

**Faz 4 — RAG parça dosyası JSONL** (4 okuyucu: `localRagEngine` oku/yaz, `rag_vektor_hatti.py`, `queryIntel/build.ts`,
`queryIntel/server.ts`); kararsız parça kimlikleri (`chunk-sum` sıra, `chunk-gloss` içerik özeti) kaynak kimliğine bağlanır.

**Faz 5 — ders manifesti kalıcılaşır:** `veri.py ders` çıktısı hat koşucusunun ve dağıtımın okuduğu
`ders_bilgi/<key>/manifest.json`'a dönüşür (HANTALLIK §4); manifestte olmayan katman "üretildi" sayılmaz.
**Yapıldı (2026-11-16):** `scripts/hat/tam_hat/manifest.py` (uret/goster/denetle/fark) → `ders_bilgi/<key>/katman_manifest.json` (65 K2 dersi üretildi; `veri.py ders` güncel manifesti okur). **Kalan:** koşucu/dağıtım entegrasyonu (`kosucu.py` sonu `uret`, `dagit.sh` öncesi `denetle`), Kurul 1 uyarlaması.

**Faz 6 — kullanıcı kararı isteyen alan kazanımları:** `meds_temp` içindeki referanssız iş artıkları (~3,5 GB),
Supabase öncesi yedek (2,2 GB), varsayılan olmayan ses varyantları (1,9 GB), `dist-android`, üç kopya skill klasörü.
