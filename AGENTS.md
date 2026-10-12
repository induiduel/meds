# meds/ — Ajan Talimatı

Bu klasör MedSoru uygulamasının kodudur. Kurallar tek yerde tutulur:

- **`../AGENTS.md`** — içerik, deste, etkileşim ve GPU kuralları (esas belge; çelişkide bu geçerlidir).
- **`../PROJE_TANITIMI.md`** — amaç, klasör yapısı, veri hattı (downloads → temp → database).
- **`../DEGISIKLIK_KAYDI.md`** — oturum günlüğü; işe başlamadan oku.
- **`CLAUDE.md`** — kod düzeni, komutlar, RAG/grounding kuralları.
- **`docs/OGREN_ETKILESIM_REHBERI.md`** — Öğren destesi şeması ve gönderim adımları.
- **`deploy/oracle/SISTEM_MIMARISI.md`** + **`YENI_YAPI_YOL_HARITASI.md`** — Oracle canlı mimarisi ve toparlama planı.

## Donanım ve AI (2026-10-11)

- **Yerel GPU YASAK.** Ollama, llama-server, CUDA'lı PyTorch, GPU'lu konteyner ve LoRA eğitimi kaldırıldı.
- Vektörleme yalnız CPU: `meds-embed-bge` (bge-m3, 127.0.0.1:8094) ve `meds-embed` (e5-small, :8091) systemd birimleri;
  Python'da `scripts/agents/lib.py::embed`. Oracle'da aynı `embed_server.py` `meds-embed` konteynerinde çalışır.
- LLM gereken her iş ücretsiz bulut zincirine gider (`MEDS_LLM_BACKEND=cloud`, `MEDS_FREE_ONLY=1`).
- Makinede 15 GB RAM var: yeni servislerde `MemoryMax`/`CPUQuota`/`OOMScoreAdjust` zorunlu; ağır işleri (vite build, tsc,
  model yükleme) aynı anda çalıştırma.
- **3000 sunucusu (`meds-web`) kendiliğinden yeniden başlamaz** (2026-10-12'den beri `tsx watch` yok). `server.ts` ya da
  başka sunucu kodu değişince `systemctl --user restart meds-web`; yalnız ön yüz değiştiyse `npx vite build` yeter.
  Ayrıntı: `../AGENTS.md` kural 12.

## Kapı (gönderimden önce)

`npx tsc --noEmit -p .` 0 hata · `python3 scripts/validate_learning_decks.py` 0 HATA · `npx vite build` geçer.
Eski ayrıntılı (GPU dönemi) sürümler: `/home/indu/medsor-yedek/arsiv_belgeler_20261011/`.
