# Semantik Veri Modeli (Anlamsal Bağdaştırma Motoru)

Bu klasör, MedSoru verilerini **yalnızca veri modelleme ve anlamsal bağdaştırma** amacıyla kullanan
bağımsız bir çekirdektir. Buradaki çıktı **kullanıcıya sunulmaz**; soruları makineye anlamlandırmak,
ders/konu/kazanım ile eşleştirmek ve RAG için sağlam bir bilgi tabanı sağlamak için vardır.

- **GPU kullanılmaz. Tüm işlem ücretsizdir (CPU).** Bulut AI zorunlu değildir.
- **Eski veritabanına dokunulmaz**; tüm girdiler salt okunur. Çıktı yalnızca bu klasörün `data/` altına yazılır.
- Mevcut v2 çıktısı ve sitede kullanılan veriler **değiştirilmeden**, yeni modeli üretmek için kullanılır.

---

## 1. Ne yapar?

Soru metnini alır → **normalize → NLP → varlık (NER) → niyet → embedding → vektör arama → yeniden
sıralama → hiyerarşik sınıflandırma** zincirinden geçirir ve şunları üretir:

- **İlgili ders notu parçası (kanıt):** chunk_id, kaynak dosya, sayfa
- **Ders → Kurul → Konu → Kazanım** (hiyerarşik sınıflandırma)
- **Niyet** (tanı, tedavi, mekanizma, patogenez, komplikasyon, sıklık, …)
- **Tıbbi varlıklar** (terimler) ve **ICD-10 / UMLS / QID** kodları
- **Güven skoru** ve alternatif adaylar

---

## 2. Klasör yapısı

```
scripts/semantic/
├── config.py        # yollar, model, eşikler (salt-okunur kaynaklar + data/ çıktı)
├── nlp.py           # normalizasyon, tokenizasyon, stop-words, hafif TR kök bulma, n-gram, BoW, TF-IDF, (spaCy varsa) bağımlılık analizi
├── medical.py       # tıbbi sözlük + ICD-10 (TR/EN) yükleme, tek sözlükte birleştirme
├── ner.py           # sözlük tabanlı varlık çıkarımı (çok-kelimeli), ICD/UMLS/QID döndürür
├── taxonomy.py      # Ders→Kurul→Konu→Kazanım ağacı + konu/kazanım eşleyici (TF-IDF kosinüs)
├── embeddings.py    # multilingual-e5-small (CPU) embedding (passage/query)
├── vectorstore.py   # FAISS indeksi (kosinüs = normalize + inner product)
├── intent.py        # niyet tespiti (kural tabanlı)
├── pipeline.py      # Engine: retrieve + classify (uçtan uca)
├── build.py         # bilgi tabanı + indeksi üretir
├── evaluate.py      # 1000 soruda başarı ölçümü
├── run.py           # CLI (build | eval | classify | info)
└── data/            # ÇIKTI: taxonomy.json, lexicon.json, icd.json, chunks_meta.jsonl, index.faiss, eval_report.json
```

---

## 3. Veri kaynakları (salt okunur)

| Kaynak | Yol | Rol |
|---|---|---|
| Resmî müfredat (kazanım) | `meds/curriculum/kbu_tip_donem3_curriculum.json` | Komite çekirdek konuları = kazanım |
| Ders programı | `meds_database/taxonomy/donem3_ders_programi.json` | Kurul → Ders → Konu |
| Ders notları | `meds_database/derived/clean_notes/*.jsonl` | Atomik bilgi parçaları (metin) |
| ICD-10 (TR/EN) | `meds_database_v2/reference/icd10.tsv` | Kod ↔ ad eşlemesi |
| Kanıtlı sözlük | `meds_database_v2/evidence_thesaurus/kanitli_sozluk.json` | Türkçe/Latin terim + eş anlamlı |
| Kavram kimlikleri | `meds_database_v2/concept_ids/kavramlar.json` | UMLS CUI, QID, DOID |
| CORE parçaları + vektörleri (v2) | `meds_database_core/chunks/`, `vectors/` | İndekslenecek bilgi tabanı |
| Değerlendirme soruları (v2) | `meds_database_core/questions/` | 1000 soruluk test |

> Bu dosyalar **okunur**, hiçbiri değiştirilmez.

---

## 4. Nasıl çalışır (aşamalar)

**Aşama 1 — Bilgi tabanı (taxonomy + chunk):**
- `taxonomy.build()` müfredat ve ders programından **Ders → Kurul → Konu → Kazanım** ağacını üretir.
- Her ders notu parçası (chunk) metadata ile zenginleştirilir: ders (kaynaktan), konu/kazanım (TF-IDF eşleme).

**Aşama 2 — Tıbbi terim standardizasyonu & NER:**
- `medical.build_lexicon()` ICD + sözlük + kavram kimliklerini tek sözlükte birleştirir (≈9.000 terim).
- `ner.extract()` metinde çok-kelimeli tıbbi ifadeleri bulur; ICD/UMLS/QID kodlarını döndürür.

**Aşama 3 — Embedding (CPU):**
- `intfloat/multilingual-e5-small` (384d) ile hem parçalar (`passage:`) hem sorgular (`query:`) vektörlenir. GPU yok.

**Aşama 4 — Dense retriever + reranker:**
- FAISS `IndexFlatIP` üzerinde **kosinüs benzerliği** ile hızlı tarama (top-100).
- Yeniden sıralama: `0.28*yoğun + 0.52*kapsam + 0.10*kök + 0.10*taksonomi` (deterministik, CPU).

**Aşama 5 — Hiyerarşik sınıflandırma (çıktı):**
- En iyi parçanın metadata'sı (ders/konu/kazanım) ve sorunun kendi taksonomi eşlemesi birleştirilir.

**NLP bileşenleri:** normalizasyon, tokenizasyon, **stop-words temizleme**, hafif Türkçe **kök bulma**,
**n-gram (unigram/bigram)**, **Bag-of-Words**, **TF-IDF**, cümle bölme ve (spaCy modeli varsa) **bağımlılık
analizi** (yoksa kural tabanlı öbek çıkarımı).

---

## 5. Nasıl çalıştırılır

```bash
cd /home/indu/medsor/meds/scripts
PY=/home/indu/medsor/meds/.venv-ocr/bin/python

$PY -m semantic build                 # bilgi tabanı + FAISS indeksini üret (~3 sn)
$PY -m semantic eval --n 1000         # 1000 soruda başarıyı ölç
$PY -m semantic classify "Efor dispnesi ve 2. sağ interkostal aralıkta sistolik ejeksiyon üfürümü olan hastada en olası patoloji hangi kapaktadır?"
$PY -m semantic info                  # indeks hazır mı
```

`build` mevcut e5 vektörlerini kullanır (yoksa üretir). Tekrar çalıştırmak idempotenttir.

---

## 6. Başarı (1000 soru üzerinde)

Metrik (şeffaf): Anlamsal arama, sorunun gerçekten geldiği **ders notu kaynağını** bulabiliyor mu?

| Metrik | Sonuç | Not |
|---|---|---|
| **top-5 kaynak isabeti** | **0.964** | İşletim noktası: doğru materyal ilk 5'te (hedef ≥0.90 ✅) |
| top-1 kaynak isabeti | 0.809 | Sıkı; kopya/yakın ders notları ve gürültülü kökler nedeniyle ~%81'de doyuyor |
| top-1 destek oranı | 0.991 | En iyi parça soruyu neredeyse her zaman destekliyor |
| top-1 ders uyumu | 0.555 | Kaynakların bir kısmında ders etiketi yok (yoldan çıkarılamıyor) |

> Yorum: Soru → doğru ders notu eşleştirmesinde **top-5 %96** (≥%90). Tek en iyi 1. sıra (top-1) ise
> kopya dersler ve OCR gürültüsü yüzünden ~%81'de kalıyor. Cross-encoder (bge/mmarco) denendi; bu
> korpusta top-1'i artırmadı (CPU maliyeti yüksek), bu yüzden varsayılan kapalı.

Rapor: `data/eval_report.json`.

---

## 6.1. Site kullanımı için servis (hazır)

CPU e5 + FAISS tabanlı servis: **`meds-v2semantic`** (127.0.0.1:8093). Site uçları:
`GET /api/v2/semantic/classify?q=...` ve `GET /api/v2/semantic/search?q=...&limit=...`
(`/v1/v2/semantic/*` takma adıyla). Servis kapalıysa 503 döner; site etkilenmez.

```bash
scripts/v2/deploy/install-meds-core.sh          # unit'leri kurar
systemctl --user enable --now meds-v2semantic    # başlat
```

**Aktif kullanılabileceği alanlar (site):**
1. **Soru → müfredat etiketleme:** Her soru için ders/konu/kazanım önerisi (moderasyon/düzenleme ekranında otomatik etiket).
2. **RAG zeminleme:** Yeni soru/rekonstrüksiyon akışında en iyi ders notu parçalarını (kaynak+sayfa) getirme.
3. **Benzer soru / çıkmış eşleştirme:** Mevcut sorularla anlamsal benzerlik.
4. **Niyet & varlık (NER):** Soru tipini (tanı/tedavi/mekanizma) ve tıbbi terimleri + ICD kodu çıkarma.
5. **Kalite denetimi:** Ders uyumu düşük veya kanıtsız soruları işaretleme.
6. **Eğitim denetimi:** Eşleşen (soru, kanıt, etiket) üçlülerinden reranker/embedding için denetimli veri üretimi.

Kısıt: bu çıktı **kullanıcıya doğrudan sunulmaz**; veri modelleme ve arka plan etiketleme içindir.


---

## 7. Nerede / nasıl kullanılır

- **Soru eşleştirme servisi:** `pipeline.Engine.classify()` doğrudan çağrılır; sonuç JSON'dur. İstenirse
  küçük bir HTTP servisine sarılıp (ör. `meds-v2search` gibi) site/panel tarafına salt-okunur sunulabilir.
- **RAG omurgası:** `Engine.retrieve()` + vektör deposu, soru → kanıt parçaları eşleştirmesini sağlar;
  cevap/rekonstrüksiyon akışlarına temel olur.
- **Toplu etiketleme:** Mevcut tüm sorular için ders/konu/kazanım tahmini üretip veri modelleme/analiz
  için kullanılabilir (kullanıcıya sunulmaz).
- **NER/ICD:** Terim ve ICD normalizasyonu gereken her yerde (`ner.extract`) kullanılabilir.
- **Eğitim verisi üretimi:** Eşleşen (soru, kanıt parça, ders/konu/kazanım) üçlüleri, ileride bir
  reranker/embedding modelini **kontrastif ince ayar** (MultipleNegativesRankingLoss) için denetimli
  veri olarak kullanılabilir — bu çekirdek o verinin üretimini ve doğrulanmasını sağlar.

---

## 8. Teknoloji ve kısıtlar

- **Diller/çatı:** Python; `sentence-transformers`, `faiss`, `scikit-learn`, `spaCy` (opsiyonel), `numpy`.
- **Vektör DB:** FAISS (CPU). Kod tarafı model-bağımsız; ileride Qdrant/Chroma'ya taşınabilir.
- **GPU yok, ücretsiz.** Ağır model indirmesi yok (e5 yerel önbellekte; NER sözlük tabanlı).
- **Eski veri korunur.** Tüm girdiler salt-okunur; çıktı `data/` altında.

---

## 9. Geliştirme notları

- **Reranker:** İstenirse `bge-reranker` (cross-encoder, CPU) eklenerek top-1 daha da artırılabilir; şu an
  deterministik kapsam/kök/taksonomi karışımı kullanılıyor (indirme gerektirmez).
- **Taxonomy kalitesi:** Konu/kazanım eşleme eşiği (`min_score`) veriye göre ayarlanabilir.
- **Kod bütünlüğü:** Soru kökleri gürültülü olduğunda eşleme düşer; soru ön-işleme (OCR onarımı) beslenebilir.
- **Ölçek:** 31.680 parça, 384d; tümü CPU'da. Daha büyük koleksiyonda FAISS IVF/HNSW indeksine geçilebilir.
