# scripts/altyapi/ — servis, derleme, veri hattı, arama

- `pipeline/` Drive → meds_downloads → meds_temp → meds_database · `advanced_ai/` RAG vektör hattı · `vite/` derleme eklentileri
- `v2/`, `semantic/` paketleri: `cd scripts/altyapi && python -m v2` · `opendesign/` model geçidi · `perf/` ölçüm · `db/`, `yedek/`
- `veri.py` içerik verisi sorgusu (FTS5, `~/.cache/meds/veri.sqlite`): `ders k2-07` manifest · `bul "<sorgu>" --tur cikmis` · `al <tur> <id> --kisa` · `liste` · `say` · `--denetle`. Dev JSON'u açmadan önce bunu kullan.
- `belge_haritasi.py` (`docs/HARITA.md` üretir), `betik_haritasi.py` (scripts/HARITA.md denetimi).

## Kurallar
- Kök `scripts/kok.py` ile; `parents[N]` yasak (D2). Yeni servis: `CUDA_VISIBLE_DEVICES=""` + systemd `MemoryMax`/`CPUQuota` (AGENTS kural 10).
- Vektörleme yalnız CPU servisleriyle (:8094/:8091); LLM betiği `otomasyon/llm_kilit.py` arkasında.
- Belge eklenince `python3 scripts/altyapi/belge_haritasi.py`; kapı `python3 scripts/kapilar/yapi_koruma.py` (D8).
- Ayrıntı: `scripts/HARITA.md`, `docs/hatalar/betik_altyapi.md`.
