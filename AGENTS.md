# MedSoru AI: Sistem Mimarisi, Boru Hattı ve Yapay Zeka Talimatnamesi (AGENTS.md)
> **Hedef Kitle:** Yapay Zeka Asistanları (Antigravity, Cursor, Claude, GPT, Ollama yerel modelleri) ve Geliştiriciler.  
> **Temel İlke:** Bu proje tamamen **yerel donanım (Zero-Cost Local GPU)** ve **kanıtlanabilir tıp verisi (Zero-Hallucination Medical RAG)** prensibiyle çalışır.

---

## 1. Proje Özeti ve Amaç
MedSoru, Tıp Fakültesi Dönem 3 kurul ders slaytları, amfi notları ve geçmiş çıkmış sınav sorularını otomatik işleyen, temizleyen, zenginleştiren ve anlamsal olarak birbirine bağlayan uçtan uca otonom bir yapay zeka tıp ekosistemidir.

### Temel Çıktılar:
1. **Doğrulanmış Soru Bankası:** 5 şıklı, amfi ders notundan kanıtlı, açıklamalı ve detaylandırılmış tıp soruları.
2. **GraphRAG & Hibrit Arama:** Hastalık-ilaç-semptom ilişkilerini içeren bilgi grafı (`DiGraph`) ve `BM25 + BGE-M3` hibrit arama motoru.
3. **MemGPT Hiyerarşik Bellek:** Öğrencinin dönem, hedef puan ve zayıf konularını takip eden LLM OS bellek katmanı.
4. **Web Arayüzü:** `localhost:3000` (`nofrostlife.com.tr`) ve Canlı Analiz Kokpiti (`localhost:8085`).

---

## 2. Dizin Yapısı ve Dosya Haritası

```
MedSoru Project/
├── meds/                                   # Ana Git Deposu (induiduel/meds)
│   ├── scripts/
│   │   ├── agents/                         # Otonom Boru Hattı ve Ajan Kodları
│   │   │   ├── pipeline_runner.py          # Aşamaları sırayla çalıştıran orkestratör
│   │   │   ├── stage1_extract.py           # Aşama 1: PDF/PPTX -> Ham Metin & OCR
│   │   │   ├── stage2_clean.py             # Aşama 2: Türkçe Onarım & A-E Soru Ayrıştırma
│   │   │   ├── stage3_merge.py             # Aşama 3: RAG Chunking, Vektörleme & Zenginleştirme
│   │   │   ├── stage4_database.py          # Aşama 4: Doğrulanmış veriyi meds_database'e aktarma
│   │   │   ├── watchdog.py                 # Otonom Donanım, Docker ve Süreç Denetleyicisi
│   │   │   └── lib.py                      # Ortak ML, GPU, Ollama, Metin ve State Kütüphanesi
│   │   ├── advanced_ai/                    # İleri Düzey AI Katmanı (Aşama 5)
│   │   │   ├── orchestrator.py             # Aşama 5 Orkestratörü
│   │   │   ├── graph_rag.py                # NetworkX DiGraph Tıbbi Bilgi Grafı
│   │   │   ├── hybrid_search.py            # BM25 + Dense BGE-M3 Hibrit Arama Motoru
│   │   │   ├── memory_os.py                # MemGPT Core/Recall Bellek Sistemi
│   │   │   └── react_guardrails.py         # ReAct Döngüsü & Halüsinasyon Engelleyici
│   │   └── training/                       # Yerel Tıp Modeli Eğitimi (Fine-Tuning)
│   │       ├── prepare_dataset.py          # Alpaca formatında eğitim çifti üretici
│   │       └── train_lora.py               # 4-bit QLoRA RTX 4060 eğitim betiği
│   ├── supabase/
│   │   └── migrations/                     # PostgreSQL, pgvector & GraphRAG Şemaları
│   │       ├── 20261001_initial_schema.sql
│   │       ├── 20261004_rag_vector_schema.sql
│   │       └── 20261005_advanced_ai_graph_hybrid.sql
│   ├── docker-compose.ollama.yml           # Optimize edilmiş Ollama GPU konteyneri
│   └── AGENTS.md                           # Bu dosya (AI & Sistem Talimatnamesi)
├── meds_temp/                              # NVMe SSD Geçici Çalışma Alanı (Git dışı)
│   ├── temp1/                              # Ham OCR / metin çıktıları
│   ├── temp2/                              # Düzeltilmiş metin ve ayrıştırılmış ham sorular
│   ├── temp3/                              # Chunk'lar, BGE-M3 vektörleri (.npy), metadata
│   │   └── advanced_ai/                    # Bilgi grafı JSON ve bellek veritabanı
│   └── state/                              # Diskcache SQLite önbelleği ve ilerleme logları
├── meds_database/                          # Doğrulanmış Nihai Tıp Veritabanı
│   ├── questions/                          # Sadece verified / fixed sorular
│   └── chunks/                             # Kanıtlanmış ders slayt parçaları
└── dashboard_server.py                     # Port 8085 Canlı Telemetri & DiGraph Kokpiti
```

---

## 2.1. Veritabanı ve Veri Şeması (Database Architecture)

Proje, hem yerel NVMe SSD önbelleğinde (SQLite/JSONL) hem de PostgreSQL / Supabase üzerinde iki katmanlı ilişkisel ve vektörel bir şema kullanır:

```mermaid
erDiagram
    COMMITTEES ||--o{ LECTURE_SLIDES : "içerir"
    COMMITTEES ||--o{ PAST_QUESTIONS : "içerir"
    LECTURE_SLIDES ||--o{ RAG_CHUNKS : "bölünür"
    RAG_CHUNKS ||--o{ MEDICAL_GRAPH_NODES : "varlık_çıkarır"
    MEDICAL_GRAPH_NODES ||--o{ MEDICAL_GRAPH_EDGES : "bağlanır"
    PAST_QUESTIONS ||--o{ RAG_CHUNKS : "kanıt_gösterir"
    STUDENT_AI_MEMORY ||--o{ PAST_QUESTIONS : "çözer"
```

### PostgreSQL / Supabase Tablo Şeması:
1. **`committees`:** Tıp kurulu/komite tanımları (`id`, `name`, `academic_year`, `target_questions`).
2. **`lecture_slides` & `rag_chunks`:** Slayt sayfaları ve 900 karakterlik semantik paragraflar.
   - `id`: Benzersiz chunk ID (`{source_id}:p{page}:c{chunk_index}`)
   - `content`: Metin içeriği
   - `heading_path`: Dizin hiyerarşisi (`["Ders Adı", "Slayt Başlığı"]`)
   - `embedding`: BGE-M3 (1024d) veya Gemini kompakt vektör (`vector(768)`)
   - **İndeksler:** IVFFlat (`vector_cosine_ops`), GIN (`to_tsvector('simple', content)`)
3. **`past_questions`:** Çıkmış sınav soruları (`question_id`, `stem`, `options`, `answer`, `explanation`, `status`).
4. **`medical_graph_nodes` & `medical_graph_edges`:** GraphRAG tıbbi bilgi grafı.
   - `nodes`: `node_type` (`Ders`, `Konu`, `Hastalik`, `Belirti`, `Ilac`, `Gen`, `Soru`)
   - `edges`: `relation` (`NEDEN_OLUR`, `TEDAVİ_EDER`, `SEMPTOMUDUR`, `SORGULAR`, `İÇERİR`)
5. **`student_ai_memory`:** MemGPT öğrenci profili, dönem, hedef ve zayıf kalınan kurullar (`JSONB`).

## 3. Donanım ve Model Kuralları (ZORUNLU)

1. **GPU Offloading Kuralı:**  
   - Cihazda **NVIDIA GeForce RTX 4060 Laptop GPU (8 GB VRAM)** ve Intel UHD grafik kartı bulunmaktadır.
   - Tüm LLM ve Embedding çağrılarında **RTX 4060 kullanılmalıdır**.
   - Model çağrılarında katmanların CPU'ya düşmesini engellemek için her zaman **`-ngl 99`** (`options["num_gpu"] = 99`) kuralı uygulanır.
2. **Bellek / SSD Önbellek Kuralı:**  
   - Vektör ve ara işlemler için Python RAM belleğinde `dict` veya `pickle` biriktirilmez.
   - Doğrudan NVMe SSD üzerinde çalışan **`diskcache.Cache` (SQLite tabanlı)** kullanılır.
3. **Konteyner ve Süreç İzolasyonu:**  
   - `meds-ollama` konteyneri `OLLAMA_NUM_PARALLEL: 2`, `OLLAMA_FLASH_ATTENTION: 0`, `OLLAMA_KV_CACHE_TYPE: f16` ile çalışır.
   - Boşta kalan modeller `keep_alive: 24h` ile bellekte tutulur, `max_loaded_models: 1` ile izole edilir.
4. **Donanım Koruma ve Termal Güvenlik Freni (ZORUNLU):**
   - GPU yükü **%90** veya GPU çekirdek sıcaklığı **80°C** üzerine çıkamaz.
   - `lib.py` (`wait_for_gpu_safety`) ve `watchdog.py` (`enforce_gpu_thermal_and_load_limits`) her model ve embedding çağrısından önce GPU telemetrisini denetler; eşikler aşılırsa sistemi güvenli sıcaklığa inene kadar otomatik uyutur (Thermal Throttling).
5. **Kod Güncelleme Sonrası Yeniden Başlatma:**  
   - `scripts/agents/` dizinindeki bir `.py` dosyası düzenlendiğinde, arka plandaki Python süreci eski kodu çalıştırmaya devam eder.
   - Yeni kod yazıldığında çalışan süreç sonlandırılmalı (`kill -9`) veya `watchdog.py`'ın otomatik tazelemesine bırakılmalıdır.

---

## 4. Boru Hattı Aşamaları (Execution Pipeline)

### Aşama 1: Ham Çıkarım (`read_document.py` / `stage1_extract`)
- `downloads/` altındaki PDF ve PPTX dosyalarını PyMuPDF, EasyOCR/Tesseract ve Qwen3-VL ile tarar. Metinleri `temp1/` altına JSON formatında yazar.
- **İleri Seviye OCR İyileştirme Mimarisi (Faz 3 Sonrası Geri Dönüş Standardı):**
  1. **Görüntü Ön İşleme (Pre-Processing):** Görseller Lanczos algoritmasıyla 2x büyütülür (300 DPI eşdeğeri), gri tonlama ve kontrast adaptasyonu uygulanır.
  2. **Görüntü Dilimleme (Image Tiling / Slicing):** Yoğun ve çok sütunlu slaytlar 2x2 kadrana (quadrants) bölünerek Qwen-VL downsampling kaybı önlenir.
  3. **VLM İçin Katı OCR Promptu:** Modele yorum yapmayan ve tıbbi tabloları Markdown formatında aktaran katı sistem promptu dayatılır.
  4. **Hibrit OCR Hiyerarşisi:** Önce PyMuPDF dijital metin, ardından GPU EasyOCR / Tesseract, yetersiz kalınırsa Qwen3-VL devreye girer.

### Aşama 2: Türkçe Onarım ve Soru Ayrıştırma (`stage2_clean.py`)
- OCR gürültülerini temizler, kırık hece ve Türkçe karakterleri düzeltir.
- **LLM ile Post-OCR Tıbbi Onarım (Gemma 3 / Qwen):** OCR motorunun karıştırdığı harf/rakam hataları (0->O, 1->I) ve tıbbi terimler (`5taf11ococus` -> `Staphylococcus`) tıbbi bağlam bozulmadan onarılır.
- Çıkmış sorulardan `no`, `stem` ve `A-E` seçeneklerini ayıklar (`temp2/`).
- **Destek Oranı:** Soru içeriği amfi metninde en az %80 doğrulanmalıdır (`support_ratio >= 0.80`).

### Aşama 3: RAG Bölümleme, Vektörleme & Zenginleştirme (`stage3_merge.py`)
- Slaytları 900 karakter hedef ve 120 karakter overlap ile doğal paragraf sınırlarından böler (`split_passages`).
- **Öksüz Veri Çözümü (Metadata Injection):** Her 900 karakterlik bloğun en başına `[Komite X | Ders | Başlık: ...]` öneki statik olarak gömülür; BGE-M3 vektörlemesi ve LLM bağlamı hiçbir zaman kaybolmaz.
- Her chunk `bge-m3` ile 1024 boyutlu vektöre dönüştürülüp SSD `diskcache`'e kaydedilir.
- Çıkmış sorular amfi slaytlarıyla kosinüs benzerliği + IDF terim örtüşmesiyle eşleştirilir.
- **Hakem Ajan (Judge Agent) Kuralları:**
  - `support_ratio >= 0.85`: Otomatik onayla (`verified`), zenginleştirmeye al (`fixed`).
  - `0.65 <= support_ratio < 0.85`: Sınır vaka; `referee_queue` kuyruğuna atılarak DeepSeek-R1 Hakem Ajan incelemesine yönlendirilir.
  - `support_ratio < 0.65`: Eksik slayt / inceleme (`needs_fix` / `rejected`).
- **Gemma 3 Düşünce Zinciri (CoT) & XML Yapılandırılmış Prompt:**
  - LLM girdi ve çıktıları `<SLAYT_KANITLARI>`, `<SORU>`, `<ANALİZ>` ve `<YANIT>` XML etiketleriyle sınırlandırılır.
  - Zenginleştirme ve çözümlerde 4 adımlı sıralı klinik akıl yürütme (Chain-of-Thought) zorunlu tutulur.

### Aşama 4: Doğrulama ve Veritabanı Taşıma (`stage4_database.py` & `scripts/sync_to_supabase_v2.py`)
- Sadece `status == "verified"` veya `status == "fixed"` olan sorular `meds_database/` dizinine ve Supabase tablolarına aktarılır.
- Toplu aktarımda `execute_batch` (batch_size=1000) kullanılır, ardından HNSW ve GIN indeksleri tetiklenir.
- **Supabase v2 Chunk-Build Senkronizasyonu (`scripts/sync_to_supabase_v2.py`):**
  - Tüm 6.263 çıkmış soru `v2_local_pipeline_2026` sürümüyle çakışmasız (`resolution=merge-duplicates`) Supabase `past_questions` tablosuna aktarılır; mevcut öğrenci yorumları ve oyları korunur.
  - 24.794 amfi ders slayt parçası `rag_chunks` tablosuna Tier 1 (kalite >= 0.85) ve Tier 2 kademeli inşa mantığıyla aktarılır.
  - İstemci tarafında PostgREST 1000 satır sınırını aşan sayfalamalı (range pagination) yükleme mimarisi işletilir.

### Aşama 5: Gelişmiş AI Orkestratörü (`scripts/advanced_ai/orchestrator.py`)
- Slayt ve sorular üzerinden **GraphRAG Tıbbi Bilgi Grafı** inşa eder (`medical_knowledge_graph.json`, ego-graph radius=2).
  - **Graph Triples Formatı:** DiGraph ilişkileri LLM'e ham JSON yerine `[Varlık] --> (İlişki) --> [Varlık]` biçiminde metinsel üçlüler halinde beslenir.
- `rank-bm25` indekslerini BGE-M3 matrisleriyle birleştirerek **Hibrit Arama Motorunu** ayağa kaldırır.
  - Sıralama standardı: **Reciprocal Rank Fusion (RRF)**:
    $$RRF\_Score(d) = \frac{1}{60 + rank_{dense}(d)} + \frac{1}{60 + rank_{sparse}(d)}$$
  - Çapraz Dikkat benzetimli hafif **Reranker** ile Top-20 aday Top-5'e indirgenerek LLM prompt yükü hafifletilir.
- **Bağlam Kanamasını (Context Bleeding) Engelleme:** Soru çözerken Ollama mesaj geçmişi her soruda sıfırlanır, MemGPT belleği sadece tekil sistem talimatı olarak enjekte edilir.

---

## 5. Denetleyici ve Otonom Kurtarma (Watchdog)

[`scripts/agents/watchdog.py`](file:///home/indu/Masaüstü/MedSoru%20Project/meds/scripts/agents/watchdog.py) sistemi sürekli izler:
- `llama-server` süreçlerinde `-ngl 3` (CPU taşması) görürse süreci temizler ve tam GPU ile yeniden başlatır.
- Ajan kodları güncellendiğinde bayat Python süreçlerini otomatik tazeler.
- `meds-ollama` konteyneri durursa anında `docker start` yapar.
- `dashboard_server.py` kapanırsa anında yeniden çalıştırır.
- `server.ts` (Web Sunucusu - Port 3000) kapanır veya yanıt vermezse anında otonom olarak yeniden başlatır.
- Sistem RAM'i %92'nin üzerine çıkarsa acil bellek ve VRAM tahliyesi yapar.

---

## 6. Yeni Geliştirici ve AI Asistanı İçin Talimatlar

1. **Kod Yazarken:**
   - Herhangi bir model çağrısı yapacaksanız [`scripts/agents/lib.py`](file:///home/indu/Masaüstü/MedSoru%20Project/meds/scripts/agents/lib.py) içindeki `lib.chat()` ve `lib.embed()` fonksiyonlarını kullanın. Asla doğrudan kontrolsüz `requests.post` yazmayın.
   - Dışarıdan bilgi uydurmayı engelleyen koruma mekanizmalarını (`support_ratio`) bozmayın.
2. **Sistem Durumunu İzlerken:**
   - `http://localhost:8085` kokpit arayüzünü kontrol edin.
   - Terminalde `nvidia-smi` çıktısında GPU kullanımının aktif ve VRAM'in 3.5 - 4.5 GB bandında olduğunu doğrulayın.
3. **Yeni Bir Algoritma veya Script Eklendiğinde:**
   - Bu `AGENTS.md` ve `PROJECT_INSTRUCTIONS.md` dosyalarını güncelleyin.
   - Yeni scripti `pipeline_runner.py` veya `watchdog.py` izleme listesine ekleyin.
   - Değişiklikleri Git `main` dalına commit ve push yapın.

---

## 7. Yerel QLoRA Fine-Tuned Model & Web Entegrasyonu (nofrostlife.com.tr)
- **Model Adaptörü Konumu:** `meds/models/medsoru-d3-qlora`
- **HuggingFace Yetkilendirmeleri:**
  - `meds2` (Inference / Hub Okuma): `HF_TOKEN_MEDS2` (`.env`)
  - `meds3` (Write Access / Model Yükleme): `HF_TOKEN_MEDS3_WRITE` (`.env`)
- **Web Sohbet Ajanı Hedefi:** QLoRA eğitimi tamamlandığında Ollama'ya `medsoru-d3` adıyla entegre edilir ve `nofrostlife.com.tr` (localhost:3000) web arayüzünde Dönem 3 tıp soru-cevap asistanı olarak devreye alınır.

---

## 8. Arka Plan Soru Kalite Denetçisi ve Çoklu AI Sohbet Mimarisi

### 8.1. Otonom Soru Kalite Denetçisi (`question_quality_inspector.py`)
- **İşleyiş:** Arka planda donanımı (RTX 4060 GPU / CPU) yormadan yavaşça (throttled micro-sleep) 6.263 çıkmış soruyu tarar.
- **Denetim Parametreleri:**
  1. **Mükerrer & Tekrarlanan Soru:** Token Jaccard / Levenshtein benzerliği >= 0.88 olan mükerrer kopyaları tespit eder (`duplicates`).
  2. **Bozuk Karakter & OCR Hataları:** Mojibake (UTF-8 çift kodlama), rakam-harf karışımı gürültüler (0->O, 1->I) ve tipografik ligatürleri bulup onarım önerir.
  3. **Şık & Kök Bütünlüğü:** 4 veya 5 şıkkı olmayan, içeriği boş kalan şıkları ve 15 karakterden kısa anlamsız taslak kökleri belirler.
  4. **Tıbbi Anabilim Dalı Uyuşmazlığı:** Soru metnindeki yoğun kavramları analiz ederek hatalı branş etiketlerini (`discipline mismatch`) tespit eder.
- **Raporlama:** Çıktılar `meds_temp/state/quality_audit_suggestions.json` içine yapılandırılmış olarak yazılır ve `/api/audit/status` endpoint'i üzerinden web kokpitine sunulur.

### 8.2. Web AI Tıp Asistanı & Soru Dedektifi (`/asistan` - `LocalAiChatView.tsx`)
- **Yerel GPU (RTX 4060):** Ollama üzerinden `gemma3:4b`, `deepseek-r1:8b`, `qwen3:1.7b` ve eğitilen `qLoRA` modellerini sıfır maliyetle çalıştırır.
- **İnternet & Bulut Modelleri:** Kota tükenmelerine karşı Google Gemini Flash, Groq Cloud (GPT-OSS 120B) ve sınırsız Muse Spark 1.3 Free katmanlarını otomatik devreye sokar.
- **Özel Klinik Modlar:**
  - **Soru Dedektifi (`find_question`):** Öğrencinin "50 yaş hasta, hiperkalsemi ve lityum vardı" gibi eksik hatırladığı soruları BM25 + BGE-M3 RAG ile veritabanından bulup şıkları ve açıklamasıyla getirir.
  - **Soru Türetici (`generate_from_keywords`):** Verilen anahtar kelimelerden doğru kurul, ders ve konuyu saptayarak 5 şıklı orijinal kurul soruları yazar.
  - **Klinik Mekanizma:** Tıbbi patofizyolojik ve farmakolojik derin açıklamalar sunar.

### 8.3. Soru Yaşı ve Değerlendirme Sistemi
- **Yeni Soru vs Arşiv:** 2026-2027 kurul soruları ile geçmiş yılların çıkmışları yeşil (`Yeni Soru`) ve gri (`Geçmiş Yıl`) rozetlerle ayrıştırılır; filtreleme paneline `new_only` ve `archived_only` seçenekleri eklenmiştir.
- **Çift Yönlü Like / Dislike:** Her çıkmış soru için hem `upvotes` hem de `downvotes` sayaçları çalışır; oylar yerel veritabanı ile Supabase `past_questions` tablosunda anlık senkronize edilir.

