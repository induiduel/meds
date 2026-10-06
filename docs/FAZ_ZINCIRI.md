# Faz zinciri (meds-phases) — 2026-10-06

Orkestratör: `scripts/agents/phase_cycle.py` (systemd kullanıcı servisi `meds-phases`). Adımlar sırayla çalışır, aynı anda
yalnızca biri. Servis yeniden başlarsa **aynı turda kalınan adımdan** devam eder (`meds_temp/state/phase_cycle_state.json`
→ `tur_tamamlanan`). Kayıt: `meds_temp/logs/phase_cycle.log` ve adım başına `phase_cycle_<adım>.log`.
İzleme: `python3 scripts/monitor.py` (faz tablosu: durum, süre, çıktı, hız; GPU koruyucu; son hata kayıtları).

| Adım | Betik | Çıktı | Güvenilirlik / not |
|---|---|---|---|
| faz5 | `advanced_ai/multi_ai_consensus_phase5.py` | `meds_database_v2/questions` | Ders/slayt ipuçları kullanılır |
| faz6 | `advanced_ai/deep_metadata_generator_phase6.py --cycles 40` | `meds_database_v2/deep_metadata` | AI üretimi; ICD istenmez; GPU yoksa tur atlanır |
| faz6_dogrulama | `advanced_ai/validate_phase6_metadata.py` | `deep_metadata_validated/` | Modelsiz: ayırıcı tanı materyalde kanıtlı mı; ICD resmî liste (Wikidata P494) ile kod–ad uyumu |
| faz6_5 | `thesaurus_anchor_phase6_5.py` | `medical_thesaurus/` | Sözlük AI üretimi; çok sayıda yanlış eş anlamlı — doğrudan kullanılmaz |
| faz7_5 | `reconstruct_slides_phase7_5.py` | `slide_reconstructed/` | |
| faz8 | `phase8_curriculum_graph.py` | `meds_temp/phase8/` | **Yalnızca `guven=yuksek` güvenilir** (20/20 doğru/kısmen) |
| sozluk | `build_evidence_thesaurus.py` | `meds_database_v2/evidence_thesaurus/` | Kanıtlı: kısaltma ~%96, yazım varyantı ~%93; parantez çiftleri yalnız inceleme |
| faz9 | `phase9_thesaurus_graph.py` | `meds_temp/phase9/` | Faz 8 + sözlük kavramları; Faz 8 yüksek öncelikli |
| faz10 | `phase10_concept_ids.py` | `meds_database_v2/concept_ids/`, `meds_temp/phase10/` | Wikidata → UMLS CUI/MeSH/ICD/DO kimlikleri; Stanza kök varyantı; bge-m3 adayları hakeme |
| faz11 | `phase11_question_slide.py` | `meds_temp/phase11/` | Soru↔slayt: BM25+kavram + e5-small + Faz5/8/6.5 → RRF → mMiniLM cross-encoder. Tam üretim (2.735 soru) katmanlı denetim: yüksek 9,5/10, orta 8,5/10, düşük 6,5/10 → genel ~%82; yayınlanan (yüksek+orta) ~%89 |
| yayin | `export_phase_insights.py` | `meds_database/derived/phase_insights/insights.json` | Site yalnız güvenilir katmanları okur |
| asama1 | `agents/stage1_refresh.py` | indirme + hatalı OCR yenileme | GPU yoksa `--vision` kullanılmaz |
| hakem | `referee_queue.py --max 80` | `meds_temp/hakem/kararlar.jsonl` | Groq gpt-oss-120b; alıntı doğrulanmayan karar kabul edilmez; ana veriyi değiştirmez |

Faz 7 (eski hikâye üretimi) karantinada; Faz 7 v2 (`phase7_question_metadata_v2.py`) elle çalıştırılır, zincirde yok.

## Ortak kurallar
- Sınav/soru dökümleri hiçbir fazda kanıt sayılmaz: `phase8_curriculum_graph.is_exam_dump` (ad: "Kurul … Sınavı",
  "Cevap Anahtarı" dahil; 20 kaynak).
- Yeni bir fazın çıktısı siteye ancak ~30 örneklik elle denetimden sonra alınır.
- Boş sonuç mevcut çıktının üzerine yazılmaz; yazımlar atomiktir.

## GPU güvenliği
`scripts/agents/gpu_guard.py` (servis `meds-gpuguard`): ≥ 89 °C → GPU istemci betikleri SIGSTOP (≤ 86 °C'de SIGCONT);
30 sn ortalama kullanım ≥ %92 → 8 sn görev döngüsü; ≥ 95 °C acil. Kullanıcı sınırı: < 90 °C, < %92, asla > 95 °C.
2026-10-06'da GPU "fallen off the bus" (Xid 79) oldu — yeniden başlatma gerekir; o sürede Faz 6 tur atlar, diğerleri CPU'da sürer.
