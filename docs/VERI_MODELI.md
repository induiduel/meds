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
| Yedek tavanı | `data/backups/catalog`: ad başına en yeni 3; fazlası arşive |
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

**Faz 4 — RAG parça dosyası JSONL** (4 okuyucu: `localRagEngine` oku/yaz, `rag_vektor_hatti.py`, `queryIntel/build.ts`,
`queryIntel/server.ts`); kararsız parça kimlikleri (`chunk-sum` sıra, `chunk-gloss` içerik özeti) kaynak kimliğine bağlanır.

**Faz 5 — ders manifesti kalıcılaşır:** `veri.py ders` çıktısı hat koşucusunun ve dağıtımın okuduğu
`ders_bilgi/<key>/manifest.json`'a dönüşür (HANTALLIK §4); manifestte olmayan katman "üretildi" sayılmaz.
**Yapıldı (2026-11-16):** `scripts/hat/tam_hat/manifest.py` (uret/goster/denetle/fark) → `ders_bilgi/<key>/katman_manifest.json` (65 K2 dersi üretildi; `veri.py ders` güncel manifesti okur). **Kalan:** koşucu/dağıtım entegrasyonu (`kosucu.py` sonu `uret`, `dagit.sh` öncesi `denetle`), Kurul 1 uyarlaması.

**Faz 6 — kullanıcı kararı isteyen alan kazanımları:** `meds_temp` içindeki referanssız iş artıkları (~3,5 GB),
Supabase öncesi yedek (2,2 GB), varsayılan olmayan ses varyantları (1,9 GB), `dist-android`, üç kopya skill klasörü.
