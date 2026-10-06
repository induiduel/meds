# MedSoru Açık Veri API Kataloğu

MedSoru'nun yayınlanan eğitim verileri, hesap açmadan ve API anahtarı kullanmadan okunabilir.
Sorular, ders notları, özetler, sözlük/terim verileri, soru-müfredat ilişkileri, diğer metadatalar
ve transkriptler bu katalogdaki salt okunur yollarla alınabilir.

## Başlangıç

Sunucu adresini kendi kurulumunuza göre seçin:

- Yerel kurulum: `http://localhost:3000`
- Yayın ortamı: sitenin API sunucusunun adresi

Tüm isteklerde sürümlü yolu kullanın: `GET /v1/...`.
Kök katalog, yayınlanan uç noktaları makinenin okuyabileceği JSON biçiminde döndürür:

```text
GET /v1/
```

Bu kılavuzun çevrimiçi Markdown sürümü için `GET /v1/documentation` kullanın.

Eski ve doğrudan yollar da çalışır: `/api/...`. Örneğin `/v1/questions` ile
`/api/questions` aynı güncel soru havuzunu döndürür.

## Hızlı başlangıç

```bash
curl http://localhost:3000/v1/
curl http://localhost:3000/v1/committees
curl "http://localhost:3000/v1/questions?committeeId=donem3-kurul-1"
curl "http://localhost:3000/v1/past-exams?discipline=Patoloji"
curl "http://localhost:3000/v1/lecture-notes?compact=1"
```

Tarayıcı uygulamalarında CORS açıktır; `fetch` doğrudan kullanılabilir:

```js
const response = await fetch('http://localhost:3000/v1/past-exams');
const questions = await response.json();
```

## Veri uç noktaları

| Veri | Yol | Filtreler / kullanım | Yanıt |
|---|---|---|---|
| Kurullar | `GET /v1/committees` | Yok | `{ committees: [...] }` |
| Güncel soru havuzu | `GET /v1/questions` | `committeeId`, `discipline`, `status`, `search` | `{ questions: [...] }` |
| Tek güncel soru | `GET /v1/questions/:id` | `:id` soru kimliği | `{ question: {...} }` |
| Çıkmış sorular | `GET /v1/past-exams` | `committeeId`, `discipline`, `year`, `query` | `{ questions: [...] }` |
| Çıkmış soru eşitleme | `GET /v1/past-exams/sync` | `since`, `count` | Tam liste veya değişen kayıtlar |
| Faz 14 İnceleme Katmanı | `GET /v1/past-question-reviews` | `status`, `questionId` | `{ totalCount, report, reviews: [...] }` |
| Veri kümesi kataloğu | `GET /v1/data-catalog` | Yok | `{ veri_kumeleri: [...] }` |
| Öğrenme bağlantıları | `GET /v1/learn-links` | Yok | `{ baglantilar: {...} }` |
| Ders notu listesi | `GET /v1/lecture-notes` | `committeeId`, `discipline`, `compact=1` | Ders notu dizisi |
| Tek ders notu | `GET /v1/lecture-notes/:id` | `raw=1` özgün metni döndürür | Ders notu ve sayfaları |
| Ders özetleri | `GET /v1/summaries` | Yok | Özet katalog kaydı |
| Tek ders özeti | `GET /v1/summaries/:id` | `:id` özet kimliği | Tam özet |
| Arama | `GET /v1/search` | `q` veya `query`, `committeeId`, `discipline`, `limit` | `{ success, count, results }` |
| Gemini v3 soru verileri | `GET /v1/gemini-v3/questions` | `q`, `committeeId`, `limit`, `offset` | `{ total, items }` |
| Gemini v3 ders notları | `GET /v1/gemini-v3/lecture-notes` | `q`, `committeeId`, `limit` | `{ total, items }` |
| Tek Gemini v3 ders notu | `GET /v1/gemini-v3/lecture-notes/:sourceId` | `:sourceId` | Not metni ve metadata |
| Tıbbi sözlük ve terimler | `GET /v1/gemini-v3/thesaurus` | `q` | Terim kayıtları |
| Soru-müfredat ilişkileri | `GET /v1/gemini-v3/metadata/relations` | Yok | İlişki metadataları |
| Tıbbi eş anlamlılar | `GET /v1/gemini-v3/metadata/synonyms` | `q` | Eş anlamlı metadata kayıtları |
| RAG durum ve istatistikleri | `GET /v1/rag/status`, `GET /v1/rag/stats` | Yok | İndeks ve kaynak sayıları |
| Transkriptler | `GET /v1/transcriptions` | Yok | Transkript dizisi |
| Tek transkript | `GET /v1/transcriptions/:id` | `:id` | Tam transkript |
| İçe aktarılmış katkılar | `GET /v1/deepseek/contributions` | Yok | Katkılar ve metadatalar |

Türkçe kısa yollar:

| Yol | Karşılığı |
|---|---|
| `GET /v1/sorular` | `GET /v1/questions` |
| `GET /v1/cikmis` | `GET /v1/past-exams` |

## Veri kümelerini çekme

### Güncel soru havuzu

Bu uç yalnızca 2026-2027 güncel havuzunu verir. `search` konusu, anabilim dalını,
soru numarasını ve soru metnini tarar.

```text
GET /v1/questions?committeeId=donem3-kurul-1&discipline=Patoloji&status=verified
GET /v1/questions?search=hiperkalsemi
```

Her kayıtta `id`, `committeeId`, `questionNumber`, `discipline`, `topic`, `status`,
katkı parçaları (`fragments`) ve varsa yeniden kurulmuş soru (`reconstruction`) bulunur.

### Çıkmış sorular ve verimli eşitleme

İlk indirmede tüm arşivi çekin:

```text
GET /v1/past-exams
```

Sonraki eşitlemelerde son alınan `lastModified` değerini ve yereldeki kayıt sayısını gönderin:

```text
GET /v1/past-exams/sync?since=2026-10-06T08%3A00%3A00.000Z&count=250
```

Yanıt `upToDate: true` ise yerel önbellek günceldir. Değişiklik varsa
`updatedQuestions` yalnızca değişen kayıtları taşır. Sayı değiştiğinde gelen `allIds`,
silinen veya karantinaya alınan yerel kayıtların temizlenmesi için kullanılabilir.

Çıkmış soru listesini daraltmak için:

```text
GET /v1/past-exams?committeeId=donem3-kurul-1
GET /v1/past-exams?discipline=Farmakoloji&year=2025
GET /v1/past-exams?query=antibiyotik
```

Filtre kullanılmayan arşiv yanıtları kısa süreli HTTP önbellekleme desteği sağlar;
istemci `If-Modified-Since` başlığıyla yeniden indirmeyi önleyebilir.

### Faz 14: Çıkmış soru redaksiyon inceleme katmanı (Test edilen veriler)

Yerel model tarafından üretilen kanıta dayalı redaksiyon önerileri, canlı soru havuzuna
doğrudan yazılmaz. Ayrı bir inceleme katmanı olarak salt okunur yayınlanır:

```text
GET /v1/past-question-reviews
GET /v1/past-question-reviews?status=review_required
GET /v1/past-question-reviews?questionId=0d5ceef7f165
```

Her kayıt, kaynak soruyu (`source`), modelin önerisini (`proposal`), token örtüşme
desteğini (`support_ratio`) ve onay/inceleme durumunu (`status`) taşır. İnceleme web
arayüzünden [`/test/cikmis`](/test/cikmis) adresinde test edilip görüntülenebilir.

### Ders notları

Önce hafif listeyi alın, ardından kullanıcı seçtiğinde tek notu indirin:

```text
GET /v1/lecture-notes?compact=1
GET /v1/lecture-notes?committeeId=donem3-kurul-1&discipline=Patoloji&compact=1
GET /v1/lecture-notes/<note-id>
```

`compact=1`, sayfa metinlerini çıkarır ve listeleme için küçük bir yanıt döndürür.
Tam ders notu sayfaları tek kayıt yolundan gelir. Varsayılan yanıt temizlenmiş metindir;
orijinal kaynak metni için `?raw=1` eklenebilir.

### Ders özetleri ve öğrenme ilişkileri

```text
GET /v1/summaries
GET /v1/summaries/<summary-id>
GET /v1/learn-links
GET /v1/data-catalog
```

`learn-links`, soru kimlikleri ile ilgili öğrenme destesi/slayt ilişkilerini verir.
`data-catalog`, sunucuda yayınlanan veri kümelerinin adlarını ve metadatasını verir;
yerel disk yolları yanıta dahil edilmez.

### Sözlük, terimler ve zengin metadatalar

```text
GET /v1/gemini-v3/thesaurus
GET /v1/gemini-v3/thesaurus?q=hiperkalsemi
GET /v1/gemini-v3/metadata/synonyms?q=antibiyotik
GET /v1/gemini-v3/metadata/relations
GET /v1/gemini-v3/questions?committeeId=3&limit=100&offset=0
GET /v1/gemini-v3/lecture-notes?committeeId=3
GET /v1/transcriptions
GET /v1/deepseek/contributions
```

Küratörlü soru kayıtları `limit` ve `offset` ile sayfalanır. Sözlük, eş anlamlı ve ilişki
uçları kaynak etiketiyle birlikte tıbbi terimleri ve soru-müfredat bağlarını döndürür.

### Arama

```text
GET /v1/search?q=nefrotik+sendrom&limit=10
GET /v1/search?query=beta+laktam&committeeId=donem3-kurul-2&discipline=Farmakoloji
```

`q` ve `query` aynı amaçla kullanılabilir. `limit` 1 ile 50 arasında sınırlandırılır.
Boş arama sorgusu boş sonuç döndürür.

## Hata ve kullanım kuralları

- Başarılı veri istekleri `200` döndürür.
- Kayıt bulunamazsa tek kayıt uçları `404` döndürür.
- `/v1` yalnızca `GET` ve `HEAD` kabul eder; diğer yöntemler `405` döndürür.
- Katalogda yer almayan `/v1` yolları `404` döndürür.
- Veri oluşturma, değiştirme veya silme için `/api/...` yolunda `X-API-Password` başlığı gereklidir.

```bash
curl -X POST http://localhost:3000/api/questions \
  -H 'Content-Type: application/json' \
  -H 'X-API-Password: <yazma-parolası>' \
  --data '{"committeeId":"donem3-kurul-1"}'
```

Parola yalnızca sunucunun `.env` dosyasında `MEDSORU_API_PASSWORD` olarak tutulur. Tarayıcı
arayüzü ilk yazma denemesinde parolayı ister ve tarayıcı oturumu boyunca saklar. Yönetim,
kullanıcı hesapları, e-posta ve otomasyon uçları ayrıca kendi yetki kurallarına da tabidir.

Web kullanıcıları soru havuzunu [`/sorular`](/sorular) sayfasından kullanabilir. Yazılım
entegrasyonları için sürümlü `/v1` yolları tercih edilmelidir.
