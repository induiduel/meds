# Faz 8 — Düzeltme ve Geliştirme Talimatları

> Durum: **hazırlık alanında, ana veritabanına alınmadı.** Çıktılar `meds_temp/phase8/` altında.
> Bu dosya, Faz 8'i ana veritabanına güvenle almak için yapılması gerekenleri ve kabul ölçütlerini anlatır.
> Betik: `scripts/advanced_ai/phase8_curriculum_graph.py` · Hazırlanma: 2026-10-05

## 1. Ne yapıyor?

Hiyerarşi: **Müfredat → Kurul → Ders → Konu → Kazanım → Kaynak (slayt/özet, sayfa + metin) → Soru**

| Kural | Uygulama |
|---|---|
| Her kurulda farklı dersler | Yapı resmi ders programından (`meds_database/taxonomy/donem3_ders_programi.json`): 6 kurul, 55 ders |
| Her dersin birden fazla konusu | Ders programındaki ders satırları → 362 tekil konu (tarih, hoca, saat) |
| PDF/özet bir dersin belli konusuna bağlı | 413 ders PDF'i + 347 özet konuya bağlanır (Kurul 1'de programdaki PDF adayı birebir; diğerlerinde ad + içerik benzerliği). Soru/sınav dökümleri kaynak sayılmaz |
| Her kazanım bir konuya ait | Kazanım = konunun kendi kaynağındaki öğrenme noktası: slayt başlığı (sayfa + metin) ya da özetin ana maddesi. **Uydurulmaz.** Kaynağı olmayan konu için "konu geneli" kazanımı (işaretli) |
| Her soru bir kazanım içerir | İki aşamalı eşleştirme: önce konu, sonra konu içinde kazanım; kazanımı içeren slayt sayfası kanıt olarak yazılır. Emin değilse birden fazla aday |

Sinyaller: soru kökü + şıklar + açıklama, Faz 5 metaverisi (doğrulanmış ders, pedagojik amaç, tıbbi varlıklar, ders slaytı eşleşmeleri — sınav dökümü eşleşmeleri atılır), soru metaverisi (ne sormuş / alt konu / terimler), kayıtlı kurul (zayıf öncelik; etiketler güvenilmez).

## 2. Ölçülen doğruluk (2026-10-05)

Rastgele 40 sorunun elle değerlendirmesi (ipuçları açık, `--sample 40`):

| Güven | Soru | Doğru | Kısmen | Yanlış | Karar |
|---|---|---|---|---|---|
| **yüksek** | 20 | 17 | 3 | 0 | **Kesin bağlantı olarak alınabilir** |
| orta | 5 | 1 | 0 | 4 | Alınmaz — inceleme kuyruğu |
| düşük | 15 | 4 | 2 | 9 | Alınmaz — inceleme kuyruğu |

Tüm üretimde: yüksek güven **1.444 / 2.735 (%53)**, orta 671, düşük 620.
Faz 5 ders etiketiyle uyum %52,5 — ancak bu ölçüt yanıltıcıdır: Faz 5 klinik branş adı veriyor
("Gastroenteroloji", "Anesteziyoloji"); ders programında aynı konuyu Tıbbi Patoloji / Genetik / Farmakoloji anlatıyor.
Elle kontrolde uyuşmazlıkların çoğunda Faz 8 doğru çıktı.

## 3. Bilinen hatalar ve düzeltme adımları

### 3.1 Orta/düşük güvende yanlış konu (öncelik: yüksek)
Örnekler: TB ilaç mekanizması → *Antifungal İlaçlar* (doğru: Antimikobakteriyel), hemokromatoz → *Akut Pankreatit*,
diüretik emilimi → *Antiaritmik İlaçlar*, şizofreni pozitif belirtileri → *Bipolar Bozukluk*.
- [ ] Konu belgelerinde başlık sayısı çok olan PDF'lerin baskınlığını azalt: konu belgesine kazanım başlıklarını en
      fazla 40 tekil başlıkla sınırla ya da BM25 `b` değerini 0,5 → 0,75 dene; `--no-hints` ile karşılaştır.
- [ ] Ders programında aynı adla geçen kardeş konular (ör. "Antimikobakteriyel" ↔ "Antifungal") için konu adına
      ağırlık 4 → 6; ilaç sınıfı son eklerini (-mikobakteriyel, -fungal, -viral) ayrı terim olarak say.
- [ ] Orta/düşük güvendeki kayıtlar için LLM hakemliği: modele yalnızca soru + ilk 3 aday konu + her konudan 2 kanıt
      chunk'ı ver; **kanıt satırı alıntılamayan cevap reddedilir** (`GEMINI_MODEL_SELECTION.md` kuralı). Karar
      `soru_kazanim.jsonl` içinde `hakem` alanına yazılır, otomatik kabul yalnızca alıntı doğrulanırsa.

### 3.2 Kaynağı olmayan konular (%34)
`kural_dogrulama.kaynagi_olan_konu_orani = 0.657`. Kurul 2–6 için ders programında PDF adayı yok; yalnızca ad/içerik
benzerliğiyle bağlanıyor.
- [ ] `scripts/agents/parse_ders_programi.py` ile Kurul 2–6 için de `pdf_adaylari` üret (Kurul 1'deki yöntem).
- [ ] Geçen yılın (`gecen_yil_d3`) PDF'leri bu yılın konusuyla eşleşirse `kaynak.yil` alanıyla işaretle; hoca/konu
      değişmiş olabilir.

### 3.3 Kazanım metni kalitesi
Bazı kazanımlar slayt başlığından geliyor ve kısa/genel ("KOMPLİKASYONLAR", "Kaslar=", "✓Etki Mekanizması").
- [ ] Tek kelimelik veya genel başlıkları üst başlıkla birleştir (`heading_path` içindeki bir önceki düzey).
- [ ] "✓", madde imleri ve numaralandırmayı temizle (`clean_heading`).

### 3.4 Kurul etiketleri
Soruların kayıtlı kurulu güvenilmez (1.916 soru toplu "D3K1" dosyasından "kurul 1"). Faz 8 kurulu içerikten
çıkarır. Doğru kurul bulunduğunda kaynak sorulardaki etiket **değiştirilmez**; yalnızca Faz 8 çıktısında yazılır.

## 4. Ana veritabanına alma (yalnızca kabul ölçütleri sağlanınca)

Kabul ölçütleri:
1. Rastgele 50 **yüksek güven** kaydının elle denetiminde ≥ %95 doğru (konu düzeyinde).
2. `kural_dogrulama`: her kazanım bir konuya ait = true; her derste konu ve kazanım oranı = 1.0.
3. Hiçbir kazanım "uydurma" değil: her `kaynaktan` kazanımın en az bir kanıtı (kaynak + sayfa/madde + metin) var.

Alma yöntemi (geri dönüşlü):
1. `meds_database/derived/phase8_<tarih>/` klasörüne kopyala (ana kayıtların üzerine **yazma**).
2. Uygulama yalnızca `guven = "yuksek"` bağlantıları okusun; diğerleri inceleme ekranında aday olarak görünsün.
3. Geri alma: klasörü silmek yeterli; kaynak sorular ve chunk'lar hiç değişmedi.

## 5. Çalıştırma

```bash
# Tam üretim (meds_temp/phase8 içine; önceki üretim meds_temp/phase8.prev olarak saklanır)
python3 scripts/advanced_ai/phase8_curriculum_graph.py --sample 40

# Bağımsız ölçüm (Faz 5 ipuçları kapalı, dosya yazmaz)
python3 scripts/advanced_ai/phase8_curriculum_graph.py --no-hints --dry-run
```

Otomasyon: `meds-phases` servisi (`scripts/agents/phase_cycle.py`) her turda Faz 5 → 6 → 6.5 → 7 → 7.5 → 8 →
Aşama 1 yenileme sırasıyla çalıştırır. Kayıt: `meds_temp/logs/phase_cycle.log`, durum: `meds_temp/state/phase_cycle_state.json`.

## 6. Bu turda yapılan ilgili düzeltmeler

- `curriculum/kbu_tip_donem3_curriculum.json` resmi ders programından yeniden üretildi (eski dosyada kurul kodları
  programla çelişiyordu: TIP310 "Gastrointestinal" yazıyordu; Faz 6.5 / 7.5 ve Gemini v3 hataları buradan geliyordu).
  Yedek: `curriculum/kbu_tip_donem3_curriculum.before_program_sync.json`. Eski Faz 6.5 / 7.5 çıktıları:
  `meds_database_v2_backups/*.before_program_sync_20261005`.
- `pipeline_runner.py` artık yalnızca aşama 2–5'i çalıştırır; fazlar `phase_cycle.py`'ye taşındı.
