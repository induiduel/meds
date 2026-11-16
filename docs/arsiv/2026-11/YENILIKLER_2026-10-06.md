# Yenilikler — 2026-10-06

Bu belge 5–6 Ekim 2026'da yapılan veri hattı, veri kalitesi ve site değişikliklerini özetler.
Ayrıntılı faz tablosu: [FAZ_ZINCIRI.md](FAZ_ZINCIRI.md).

## Veri doğruluğu (site)

| Sorun | Neden | Çözüm |
|---|---|---|
| Bir soruda 3–5 farklı soru kökü/şık | Eski `meds-local-sync` servisi açılışta PDF'leri kaba bölüp 278 soruyu "verified" ekliyordu; sınav sistemi çıktısı (`combinepdf (28)`) dil modeliyle bölünürken sınırlar kaçmıştı | Servis kapatıldı; `quarantine_questions.py` birleşik/bozuk soruları karantinaya alır (okuma sırasında, kaynak dosyalar değişmez); `resplit_exam_printout.py` sınav çıktısını tablo yapısına göre kuralla yeniden böler |
| Yanlış cevap anahtarı | Sınav çıktısındaki "cevap" sütunu öğrencinin işaretlediği şıktı (başka kaynakla 62 eşleşmenin 49'u farklı) | Bu sorular "Cevap anahtarı doğrulanmadı" gösterilir; hakem `anahtar` görevi soruyu kayıtlı cevabı görmeden slayt kanıtıyla yanıtlar (ilk 5/5 doğru) |
| Yanlış kurul/ders filtresi | Sınav çıktısının hepsi toplu "Kurul 1" etiketliydi; Faz 8 bazen dersi yanlış seçiyordu | `curriculum_resolve.py`: sorunun sınav başlığındaki ders+konu → resmî program konusu (> Faz 8 yüksek güven). Sunucu kurul/ders/konuyu okuma sırasında düzeltir, kurulu bulunamayan toplu etiketli sorular "belirsiz" sayılır |
| "Öğren" yanlış slayta gidiyordu | Anahtar kelime tahmini genel kelimesi bol giriş/özet slaytlarını seçiyordu | `learn_links.py` (BM25 + e5 + cross-encoder, eşikli) + `/api/learn-links`; tahmin kaldırıldı, eşik altında Öğren gösterilmez |
| Ders notlarında OCR/glif hataları | PowerPoint sembol glifleri, OCR çöp satırları, üst/alt bilgi | Faz 12 (`phase12_clean_notes.py`) kural tabanlı temizlik; site temiz katmanı gösterir (`?raw=1` özgün) |

## Yeni fazlar

- **Faz 8–11**: müfredat ağacı, kanıtlı sözlük, Wikidata/UMLS kavram kimlikleri, soru↔slayt eşleştirme (elle denetim ~%82, yayınlanan ~%89).
- **Faz 12**: ders notu temizleme. **Faz 13**: GLiNER (çok dilli, sıfır atış) + spaCy PhraseMatcher terminoloji eşleme (Wikidata/UMLS, WHO ICD-10, kanıtlı sözlük). Türkçe biyomedikal BERT/BIO NER kontrol noktası bulunmadığı için GLiNER kullanılır.
- **Hakem kuyruğu**: Groq gpt-oss-120b → qwen3.8 → Gemini; alıntısı doğrulanmayan karar kabul edilmez; "emin" kararlar uygulanır.

## Ortak veri deposu ve RAG

- `meds_database/ortak/KATALOG.json`: 21 veri kümesi (yol, kayıt, açıklama, güvenilirlik, üretici betik). `ortak/veri/` tüm kümelere tek yerden bağlantı. Site: `GET /api/data-catalog`.
- `ortak/rag/ders_materyali.jsonl`: yeni hattın 22.676 ders parçası (Faz 12 temiz metin, sınav dökümleri hariç, kurul/ders/konu ve kavram kimlikli). Site arama motoru (localRagEngine) bunu "lecture_slide" olarak okur; eski ders notlarına da temiz katman uygulanır.

## Altyapı ve güvenlik

- **Firebase veritabanı kapalı**: tüm Firestore yazma/okumaları `src/services/dbFlags.ts` anahtarının arkasında (Firebase Auth girişi değişmedi).
- **GPU koruyucu** (`meds-gpuguard`): 89 °C'de GPU istemcilerini duraklatır, %92 kullanım, 95 °C acil. Bu dizüstü GPU'da PyTorch CUDA işi (tek başına bile) "GPU fallen off the bus" verdiği için tüm PyTorch adımları CPU'da; GPU yalnız Ollama'ya ayrılmıştır.
- **Faz zinciri** kaldığı adımdan sürer, kodu değişince kendini yeniden yükler; Faz 6 süre bütçeli.
- **Yeni servisler**: `meds-watchdog`, `meds-gpuguard` (açılışta başlar). `meds-local-sync` devre dışı.
- **Panel (localhost:8085)** "Faz Zinciri" sekmesi: faz tablosu (durum, süre, çıktı, hız), canlı günlükler, hakem, veritabanı, servisler, güncel hatalar.
- **Yedek**: `MedSoru Project/yedekler/20261006_1522/` (veri + servisler; `.env` içerir, repoya eklenmez).
