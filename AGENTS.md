# meds/ — Ajan Talimatı

> ⚠️ **TÜM AJANLARIN DİKKATİNE (KESİNLİKLE ZORUNLU KURAL):**
> **HER HATA ÇÖZÜMÜNDE HATANIN KÖK NEDENİ VE ÇÖZÜMÜ TÜM AJANLAR TARAFINDAN DİKKATLE İNCELENMELİDİR!**
> Çözülen her sorunda:
> 1. Belirti (kullanıcının gördüğü hata),
> 2. Kök neden (kod/veri seviyesinde hatayı doğuran asıl mekanizma),
> 3. Kalıcı çözüm ve geleceğe yönelik önleme kuralı
> mutlaka `docs/KURUL2_YAPILMAYACAK_HATALAR.md` ve `../DEGISIKLIK_KAYDI.md` dosyalarına işlenmelidir. Hiçbir ajan kök nedeni anlamadan yüzeysel geçici yama yapamaz, hatayı geçiştiremez!

Bu klasör MeDSor uygulamasının kodudur. Kurallar tek yerde tutulur:

- **`../AGENTS.md`** — içerik, deste, etkileşim ve GPU kuralları (esas belge; çelişkide bu geçerlidir).
- **`../PROJE_TANITIMI.md`** — amaç, klasör yapısı, veri hattı (downloads → temp → database).
- **`../DEGISIKLIK_KAYDI.md`** — oturum günlüğü; işe başlamadan oku.
- **`CLAUDE.md`** — kod düzeni, komutlar, RAG/grounding kuralları.
- **`docs/OGREN_ETKILESIM_REHBERI.md`** — Öğren destesi şeması ve gönderim adımları.
- **İçerik üretimi (tek hat):** `python3 scripts/tam_hat/kosucu.py <klasör> --ders <key> --mod <tam|tasarruf>` sırayı tek
  kaynaktan (`scripts/tam_hat/mod.py`) verir; aşamalar bir kez üretilen **read-once `baglam/`** (`scripts/tam_hat/baglam.py`)
  okur, ham slaytı/şablonu tekrar tekrar değil. Ders kilidi `scripts/tam_hat/ders_kilit.py` (oturum çakışması). Akış: `docs/TAM_HAT_HIZLI_AKIS.md` §0.0.
- **GPU istisnaları + ısı/saat protokolleri:** `docs/GPU_KULLANIM.md` (ana AGENTS kural 10'un ayrıntısı).
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
