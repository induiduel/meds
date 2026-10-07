# MedSoru AI Studio Master Prompt & Architectural Specification
> **Hedef:** Google AI Studio (Gemini 1.5 Pro / Flash) ortamına tek seferde yapıştırılacak; projenin tüm bağlamını, veri şemalarını, mimari hedeflerini anlatan ve istenen 3 devasa üretim scriptini eksiksiz ürettirecek ana talimatnamedir.

---

```markdown
# MISSION BRIEFING: MEDSORU MEDICAL AI & HIGH-PERFORMANCE DATA LAKE ENGINE

Sen dünya çapında kıdemli bir Yapay Zeka Sistem Mimarı, Tıbbi NLP Uzmanı ve Dağıtık Büyük Veri Mühendisisin.
Bu görevde senden, **MedSoru** (Tıp Fakültesi Dönem 3 Akıllı Soru Bankası & RAG Ekosistemi) için sıfır veri kaybı, milisaniyelik gecikme (<50ms) ve sıfır tıp halüsinasyonu sağlayan 3 devasa üretim sınıfı (production-grade) Python modülünü eksiksiz olarak kodlaman istenmektedir.

---

## 1. PROJE BAĞLAMI VE MEVCUT DURUM

### Projenin Amacı:
MedSoru; Tıp Fakültesi amfi ders slaytlarını (PDF/PPTX), hoca ses kayıtlarını ve geçmiş yılların çıkmış kurul sınav sorularını işleyen, bunları anlamsal olarak birbirine bağlayan, öğrencilere web üzerinden anlık soru çözümü ve klinik açıklama sunan bir tıp yapay zekasıdır.

### Mevcut Mimari ve Yaşanan Büyük Darboğazlar:
1. **Veri Saklama Darboğazı:**
   - Veriler şu an yerel NVMe SSD üzerinde binlerce küçük JSON, JSONL ve SQLite diskcache (`temp1`, `temp2`, `temp3`, `meds_database`) formatında dağınık durmaktadır.
   - Bu durum disk I/O patlamasına, bellek şişmesine ve uzaktaki öğrenci sorgulama yaptığında kabul edilemez gecikmelere (5-15 saniye) neden olmaktadır.
2. **Yerel Model Kalite Yetersizliği:**
   - Yerelde çalışan NVIDIA RTX 4060 (8 GB VRAM) üzerindeki küçük modeller (`gemma3:4b`, `qwen3:1.7b`), tıp gibi ağır terminoloji içeren metinlerde soru şıklarını (A-E) birbirine karıştırmakta, OCR hatalarını düzeltirken halüsinasyon görmekte ve ders notlarındaki kritik tıbbi ayrıntıları budamaktadır.
3. **Milisaniyelik Uzak Erişim İhtiyacı:**
   - Uzaktaki öğrenci `localhost:3000` veya internet üzerinden soru çözmek veya konu aramak istediğinde, sistemin tüm veri tabanını taramak yerine **bölümlenmiş (partitioned), sütun bazlı (Parquet) ve bellek-içi (DuckDB SIMD)** çalışarak 50 milisaniyenin altında kanıt getirmesi zorunludur.

---

## 2. YENİ MİMARİ VE TASARIM PRENSİPLERİ

Sistem 3 temel omurga üzerine kurulacaktır:
1. **Medical Data Lakehouse (DuckDB + Parquet + Metadata Pruning):**
   - Hiyerarşik Bölümleme: `donem={donem}/komite={komite}/ders={ders}/`
   - Parquet Sıkıştırma: Snappy / ZSTD ile ultra hafif disk boyutu.
   - Vektörlerin Entegrasyonu: Parquet sütununda `FLOAT[1024]` (BGE-M3) veya `FLOAT[768]` saklama.
   - DuckDB Vektörel Sorgu: SQL üzerinden `array_cosine_similarity` ve metadata filtreleme ile <20ms arama.
2. **AI Studio Deep Medical Curator & Shadow Judge (Gemini Teacher-Student):**
   - Google AI Studio (Gemini 1.5 Pro / Flash) API'si kullanılarak, yerel modellerin berbat ettiği bozuk sorular, OCR gürültüleri ve slayt eşleştirmeleri %100 tıbbi doğruluk ve Structured JSON Schema ile onarılır.
   - Her soru amfi slaytındaki kanıtıyla çapraz denetlenir. Kanıtı slaytta bulunamayan hiçbir soru veritabanına onaylanmaz (`support_ratio >= 0.85` kuralı).
3. **Low-Latency Hybrid Serving API (FastAPI + DuckDB In-Memory + Reranker):**
   - Uzaktaki istemciler için milisaniyelik REST/WebSocket uç noktası.
   - BM25 (Sparse) + Cosine Similarity (Dense) -> Reciprocal Rank Fusion (RRF) sıralaması.
   - Ego-Graph (Hastalık-İlaç-Semptom ilişkisi) entegrasyonu.

---

## 3. ÜRETİLMESİ GEREKEN 3 DEVASA SCRIPT VE TEKNİK ŞARTNAME

Aşağıdaki 3 scripti hiçbir fonksiyonu eksik bırakmadan, `TODO` veya `pass` gibi geçiştirmeler yapmadan, prodüksiyona hazır, tip tanımlamaları (typing) tam, hata toleranslı ve detaylı docstring'lerle tek seferde yazmalısın.

---

### SCRIPT 1: `scripts/lakehouse_migrator.py` (Medical Lakehouse Builder)
**Görevi:** Dağınık ve yavaş JSON/JSONL/SQLite verilerini okuyarak modern, bölümlenmiş Parquet gölüne dönüştürür.
**Gereksinimler:**
1. `pyarrow`, `parquet`, `duckdb` ve `numpy` kullanarak `meds_temp/temp3`, `meds_database` ve `meds_temp/state` altındaki verileri tarar.
2. **Hedef Şema 1: `meds_lake/chunks/`**
   - Slayt Paragraf Verileri (Chunk'lar):
     - `chunk_id` (STRING, PK): `{source_id}:p{page}:c{chunk_index}`
     - `donem` (INT16, Partition Key): Tıp dönemi (örn. 3)
     - `komite` (INT16, Partition Key): Kurul no (örn. 1, 2, 3...)
     - `ders` (STRING, Partition Key): Patoloji, Farmakoloji, Mikrobiyoloji vb.
     - `source_file` (STRING): Orijinal slayt dosya adı
     - `page_num` (INT32): Slayt sayfa numarası
     - `heading_path` (LIST[STRING]): Hiyerarşik başlıklar `["Kardiyoloji", "Kalp Yetmezliği"]`
     - `content` (STRING): 900 karakterlik temiz metin
     - `medical_entities` (LIST[STRING]): Metinde geçen hastalık, ilaç, semptomlar
     - `embedding` (LIST[FLOAT]): 1024 boyutlu BGE-M3 veya 768 boyutlu vektör
     - `token_count` (INT32): Token uzunluğu
     - `created_at` (TIMESTAMP)
3. **Hedef Şema 2: `meds_lake/questions/`**
   - Çıkmış Sınav Soruları:
     - `question_id` (STRING, PK)
     - `donem` (INT16, Partition Key)
     - `komite` (INT16, Partition Key)
     - `ders` (STRING, Partition Key)
     - `academic_year` (STRING): örn. "2023-2024"
     - `exam_type` (STRING): "Komite Sonu", "Bütünleme" vb.
     - `stem` (STRING): Soru kökü
     - `options` (MAP[STRING, STRING]): `{"A": "...", "B": "...", "C": "...", "D": "...", "E": "..."}`
     - `correct_answer` (STRING): "A", "B", "C", "D", "E" veya null
     - `explanation` (STRING): Klinik ve slayt kanıtlı çözüm
     - `evidence_chunk_ids` (LIST[STRING]): Bu sorunun kanıtlandığı chunk ID'leri
     - `support_ratio` (FLOAT): 0.0 - 1.0 arası kanıt güven skoru
     - `status` (STRING): "verified", "fixed", "needs_fix", "rejected"
     - `difficulty` (STRING): "Kolay", "Orta", "Zor", "Vaka"
     - `clinical_tags` (LIST[STRING])
4. **Partition Pruning ve Optimizasyon:**
   - PyArrow `write_to_dataset` kullanarak `partition_cols=['donem', 'komite', 'ders']` yapısında yazar.
   - ZSTD sıkıştırması uygular.
   - DuckDB üzerinde anında bir view oluşturarak otomatik doğrulama sorgusu çalıştırır (Toplam kayıt, null kontrolü, indeksleme doğrulaması).

---

### SCRIPT 2: `scripts/ai_studio_deep_curator.py` (Gemini Shadow Judge & Data Repair)
**Görevi:** Yerel modellerin ürettiği bozuk, eksik veya şıkları birbirine girmiş tıp sorularını Google AI Studio (Gemini 1.5 Pro/Flash) API'si ile derinlemesine denetler, onarır ve doğrular.
**Gereksinimler:**
1. `google-genai` veya `google-generativeai` SDK'sını kullanır (`GEMINI_API_KEY` ortam değişkeniyle).
2. **Kuyruk Taraması:**
   - Durumu `needs_fix` olan, `support_ratio < 0.85` olan veya şıkları A-E eksik olan soruları tespit eder.
   - İlgili sorunun geçtiği komitedeki en alakalı amfi slayt chunk'larını (Parquet gölünden DuckDB ile) çeker.
3. **Structured Outputs (Katı Pydantic / JSON Şeması):**
   - Modele slayt metinleri ve ham bozuk soru verilir.
   - Modele katı bir sistem talimatı verilir:
     *"Sen Tıp Fakültesi Sınav Değerlendirme Kurul Başkanısın. Sana verilen amfi ders slaytlarını tek hakikat kabul edeceksin. Dışarıdan tıbbi bilgi uydurmayacaksın (Sıfır Halüsinasyon). Soru kökünü, A-B-C-D-E şıklarını ayrıştıracak, doğru cevabı slayt referansıyla gerekçelendireceksin."*
   - JSON Çıktı Şeması:
     ```json
     {
       "is_valid_medical_question": true,
       "cleaned_stem": "Soru metni...",
       "options": {
         "A": "Metin...",
         "B": "Metin...",
         "C": "Metin...",
         "D": "Metin...",
         "E": "Metin..."
       },
       "correct_answer": "C",
       "slide_evidence_exact_quote": "Slayttan harfi harfine alıntı...",
       "clinical_reasoning": "Adım adım neden C şıkkı doğru, diğerleri neden yanlış...",
       "support_ratio": 0.95,
       "status": "fixed",
       "detected_entities": {
         "diseases": ["..."],
         "drugs": ["..."],
         "symptoms": ["..."]
       }
     }
     ```
4. **Geri Yazma & Tekilleştirme:**
   - Düzeltilen soruları doğrudan `meds_lake/questions/` Parquet veri tabanına günceller.
   - Düzeltilemeyen (gerçekten geçersiz veya slaytta hiç olmayan) soruları `rejected` olarak işaretler.
   - Kota aşımı (RateLimit / 429) durumlarında Exponential Backoff (üstel geri çekilme) ve token optimizasyonu yapar.

---

### SCRIPT 3: `scripts/fast_hybrid_server.py` (Milisaniyelik DuckDB API Motoru)
**Görevi:** Uzaktaki kullanıcı veya yerel web arayüzü (`localhost:3000`) için milisaniyelik hibrit arama, filtreleme ve soru getirme API'si sunar.
**Gereksinimler:**
1. **FastAPI + DuckDB In-Memory Engine:**
   - Sunucu ayağa kalktığında DuckDB bağlantısını açar ve `meds_lake/**/*.parquet` dosyalarını sıfır kopyalama (zero-copy) ile bağlar.
   - Gerekirse bellek içi DuckDB VSS veya HNSW indekslerini önbelleğe alır.
2. **Hibrit Arama (Dense Cosine + Sparse BM25 / ILIKE):**
   - Endpoint: `POST /api/search/hybrid`
   - Girdiler: `query`, `donem` (opsiyonel), `komite` (opsiyonel), `ders` (opsiyonel), `top_k` (varsayılan 5).
   - İşleyiş:
     - SQL seviyesinde Partition Pruning: Filtre varsa sorgu doğrudan `WHERE donem = ? AND komite = ?` çalışır; Parquet okuyucu gereksiz dosyaları anında eler (0ms disk atlama).
     - Dense Similarity: Sorgu vektörü ile chunk embedding'leri arasında kosinüs benzerliği.
     - Sparse Text: DuckDB full-text / n-gram eşleşmesi.
     - Reciprocal Rank Fusion (RRF) ile en iyi 5 kanıt chunk'ı seçilir.
     - **Tüm arama süresi < 50 milisaniye olmalıdır.**
3. **Akıllı Soru Getirici:**
   - Endpoint: `GET /api/questions/quiz`
   - Öğrencinin seçtiği komiteye ve derslere göre doğrulanmış (`status IN ('verified', 'fixed')`) rastgele veya zorluk derecesine göre soruları <10ms içinde döner.
4. **LLM Çözüm Akışı (SSE - Server-Sent Events Streaming):**
   - Endpoint: `POST /api/solve/stream`
   - Kullanıcı soruyu çözemediğinde veya açıklama istediğinde, sorunun kanıt chunk'larını DuckDB'den çeker ve hafif model veya Gemini ile canlı kelime kelime (token-by-token) açıklama üretir.
5. **CORS, Telemetri ve Loglama:**
   - Tüm istekler sorgu süresi (latency_ms) ve taranan partition sayısı ile birlikte loglanır.

---

## 4. KODLAMA STANDARTLARI VE KATI KURALLAR
1. **Eksiksiz Kod:** Her script kendi başına çalışabilir olmalı, `from ... import ...` kısımları standart kütüphaneler ve yaygın paketlerle (`duckdb`, `pyarrow`, `fastapi`, `uvicorn`, `pydantic`, `google-genai` veya `google-generativeai`) uyumlu olmalıdır.
2. **Tıp Etiği & Güvenlik:** Soru ve şıklarda eksik veya uydurma veri üretilmesine karşı `support_ratio` validasyonunu kodda asla atlama.
3. **Performans:** Bellek sızıntılarını önlemek için DuckDB bağlantılarını `contextmanager` veya singleton ile yönet. Parquet okuma ve yazma işlemlerinde chunked streaming kullan.

Şimdi bu 3 scripti sırasıyla ve eksiksiz olarak üret.
```
