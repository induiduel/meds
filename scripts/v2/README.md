# MedSoru Core v2 (`scripts/v2`)

Bağımsız veri **denetim + ingest** çekirdeği. Eski `scripts/agents`, `scripts/advanced_ai` ve
`scripts/pipeline` hattından ayrı çalışır; onları kaldırmaz ve onların verisini ezmez.

- **Okur:** `meds_database/`, `meds/data/`, `meds_database_v2/` (denetim için, salt okunur).
- **Yazar:** yalnız `MEDS_CORE_DIR` (varsayılan `meds_database_core/`).
- **Şema:** `meds_database/schema/{question,chunk,source}.schema.json` (değişmez sözleşme).
- **Donanım:** GPU kullanan yerel AI YOK. CPU-only (Tesseract/rules/BM25/CPU embedding) + ücretsiz bulut LLM.

## Çalıştırma ortamı

Python bağımlılıkları hazır olan ortam: `meds/.venv-ocr/bin/python` (jsonschema, requests, numpy).
Testler stdlib `unittest` ile yazıldı (pytest gerekmez; varsa pytest de çalıştırır).

```bash
cd /home/indu/medsor/meds/scripts
/home/indu/medsor/meds/.venv-ocr/bin/python -m unittest discover -s v2/tests -v
```

## Kullanım (CLI)

```bash
cd /home/indu/medsor/meds/scripts
PY=/home/indu/medsor/meds/.venv-ocr/bin/python

$PY -m v2 status                                   # yollar/yapılandırma
$PY -m v2 audit                                    # mevcut veriyi denetle (salt okunur)
$PY -m v2 ingest <dosya-veya-klasör>               # oku→normalize→doğrula→tekilleştir→yayınla
$PY -m v2 ingest <klasör> --match --ders "Tıbbi Patoloji"   # mevcut parçalarla eşleştir
$PY -m v2 ingest <dosya> --no-publish              # yalnız işle (yazmaz)
$PY -m v2 ingest-all <köklar...> --limit N         # toplu işle (checkpoint ile kaldığı yerden)
$PY -m v2 cycle                                    # tek tur; --watch --post ile sürekli (systemd)
$PY -m v2 curriculum                               # ders → konu → kazanım eşleme + metadata + terimler
$PY -m v2 answers --limit 30                       # eksik cevaplı soruları tamamla (Faz 14'ü atlar)
$PY -m v2 answers --limit 30 --include-faz14       # Faz 14'ün incelediklerini de işle
$PY -m v2 embed                                    # CORE parçalarını CPU e5 ile vektörleştir
$PY -m v2 notes                                    # ders notları + özetleri düzeltip CORE'a al
$PY -m v2 link                                     # soruları ders notu parçalarına bağla (sayfa + alıntı)
$PY -m v2 verify                                   # cevaplı soruların tıbbi doğruluğunu denetle (kanıt desteği)
$PY -m v2 graph                                    # kavram grafı üret (ders/konu/kazanım/terim)
$PY -m v2 cluster                                  # toplu soru tamamlama: parçaları kümele/birleştir
$PY -m v2 cleanup                                  # kök/şık metinlerini temizle (mojibake, '!'→'i')
$PY -m v2 purge                                    # gerçek soru kökü olmayan kayıtları ELE
$PY -m v2 revalidate                               # issues/status'u tazele (site filtreleri)
$PY -m v2 export-site                              # v2 çıktısını site hub'ına bağla (ortak/veri)
$PY -m v2 study prepare                            # sözlük/kart/soru kartı denetim paketleri → meds_temp/study/
$PY -m v2 study build [--export]                   # editör kararlarını birleştir; --export site verisini yedekleyip yazar
```

Açık uçlu sorular `acik_uclu: true` anahtarıyla işaretlenir (şıksız oldukları için engelleyici
sayılmaz); sınıflandırma ve filtreleme bu anahtar üzerinden yapılır. Site: `/veri` (Veri Merkezi).

**Soru kökü kapısı (`core/quality.py`):** bir kayıt yalnızca gerçek soru bağlamı taşıyorsa kabul
edilir (soru işareti veya `hangisi/nedir/nasıl/...` kalıbı). Başlıklar ("KOMPLİKASYONLAR"), şık
satırları ("Bradikardi"), ders içeriği cümleleri ve birleşmiş sınav blokları (`✅`, çok satır, çoklu
soru kalıbı) **elenir**. `purge` bunu mevcut veriye de uygular.

Hibrit arama (CPU e5) varsayılan kapalı: `MEDS_V2_VECTOR=1` ile açılır (GPU yok, model CPU'da).

`ingest` idempotenttir: aynı dosya ikinci kez işlenince yeni kayıt üretmez (aynı `question_id`
güncellenir). Çıktı yalnızca `MEDS_CORE_DIR` altına yazılır.

### systemd (bağımsız servisler)

```bash
scripts/v2/deploy/install-meds-core.sh          # unit'leri ~/.config/systemd/user'a kurar (başlatmaz)
systemctl --user enable --now meds-core meds-v2search
```

- `meds-core`: tam veri hattı (her 10 dk tur).
- `meds-v2search`: CPU e5 anlamsal arama servisi (127.0.0.1:8092); site `/api/v2/search` bunu kullanır,
  kapalıysa BM25 yedeğine düşer.

## Modüller

| Modül | Görev |
|---|---|
| `config.py` | Yollar/env; `.env` yükleme; `MEDS_CORE_DIR`; CORE sınırı |
| `core/schema.py` | question/chunk/source JSON-Schema doğrulaması (jsonschema + yedek) |
| `core/ids.py` | İçerik-adresli deterministik kimlikler (source/chunk/question) |
| `core/store.py` | Atomik yazım, JSONL, kilit, checkpoint, "boş sonuçla ezme" guard'ı, KATALOG |
| `core/textnorm.py` | NFC, mojibake onarımı, ligatür, kontrol karakteri, tire-birleştirme, TR katlama |
| `core/llm.py` | GPU'suz LLM: yalnız ücretsiz bulut (groq→zen→gemini→openrouter) + görsel OCR |
| `core/segment.py` | Soru/şık ayrıştırma (satır içi/ayrı satır), negatif soru tespiti |
| `core/validate.py` | Kayıt bazlı `issues[]` + severity (blocking/review) |
| `core/dedupe.py` | İçerik-adresli tam tekrar + yakın-kopya gruplama |
| `core/evidence.py` | provenance ve `support_ratio` (kanıt kapısı) |
| `core/match.py` | BM25 (CPU) + kalibre güven katmanları (yuksek/orta/dusuk) |
| `core/vector.py` | Opsiyonel CPU e5 hibrit arama (RRF); varsayılan kapalı |
| `core/curriculum.py` | Ders → Konu → Kazanım eşleme + tıbbi terim çıkarımı |
| `core/faz14.py` | Faz 14 inceleme entegrasyonu (içerik anahtarıyla çakışma önleme) |
| `core/embed.py` | CPU e5 vektörleştirme (site RAG için `vectors/`) |
| `core/cluster.py` | Toplu soru tamamlama: benzerlik + union-find + birleştirme (AI yok) |
| `core/graph.py` | Kavram grafı: ders/konu/kazanım/terim co-occurrence (AI yok) |
| `stages/s1..s12` | extract → normalize → validate → dedupe → match → enrich → publish → curriculum → answer → notes → link → verify |
| `pipeline.py` / `cli.py` | Orkestrasyon (tek dosya, toplu `ingest-all`) ve komut satırı |
| `cycle.py` | Bağımsız orkestratör (kilit/checkpoint/log; `--watch`) |
| `audit.py` | Mevcut veri denetçisi (rapor + inceleme kuyruğu) |
| `export_site.py` | Site hub bağları (`ortak/veri`) + kırık symlink onarımı |
| `core/lectures.py` | Ders notu korpusu (yalnız lecture_slide) + ters indeks, terim geçişi, kök tabanlı kanıt desteği |
| `stages/s13_study.py` | Sözlük, ansiklopedi, deste kartları ve çıkmış soru kartları: denetim → editör kararı → kanıt kapısı → dışa aktarma |
| `deploy/` | `meds-core.service` + kurulum betiği |

## Sözlük ve kartlar (`study`)

`prepare` mevcut sözlüğü (`src/data/medical_glossary.json`), deste kartlarını
(`interactive_learning_decks.json`) ve cevap anahtarlı çıkmış soruları ders notlarıyla ölçer; yeni terim
adaylarını (`meds_database_v2/concept_ids`) alıntılarıyla `meds_temp/study/` altına yazar. Tanımları ve
düzeltmeleri **editör** (yerel/bulut model değil) `editor_*.jsonl` dosyalarına yazar. `build` her tanımın
kök tabanlı desteğini yeniden ölçer: `support >= 0.6` → `kaynakli`, editörün tıbbi doğruluğunu teyit ettiği
→ `editor_onay`, diğerleri inceleme kuyruğu (`meds_database_core/reports/study_review.jsonl`).
`--export` öncesi orijinaller `yedek/study/<zaman>/` altına kopyalanır; deste parçaları
(`src/data/decks/`) Vite açılışında yeniden üretilir.

## Faz 14 entegrasyonu

Eski sistemin bulut AI incelemesi (`meds_database_v2/phase14_past_question_editor/reviews.jsonl`)
okunur; v2 **aynı soruyu tekrar incelemez** (içerik anahtarıyla eşleştirir). Varsayılan olarak
cevap tamamlama Faz 14'ün incelediği soruları atlar; birincil hedef onun denetlemediği soruları
tamamlamaktır. `--include-faz14` ile istenirse onlar da işlenir.

## Yol haritası

M0 ✅ çekirdek · M1 ✅ denetçi · M2 ✅ ingest · M3 ✅ güven katmanları + hibrit arama + `ingest-all` ·
M4 ✅ `cycle.py` + systemd `meds-core` · M5 ✅ site entegrasyonu (`/api/v2/*`, ortak/veri bağları) ·
M6 ✅ müfredat/kazanım eşleme + Faz 14 uyumlu cevap tamamlama + CPU e5 vektörleştirme (tam zincir) ·
M7 ✅ açık uçlu anahtarı + ders notu/özet düzeltme + kaynak ilişkilendirme + tıbbi doğrulama +
kavram grafı + toplu soru tamamlama + site arayüzü (`/veri`) ·
M8 ✅ soru kökü kapısı + OCR onarımı + GH Pages base düzeltmesi + CPU e5 anlamsal arama servisi (`meds-v2search`).
