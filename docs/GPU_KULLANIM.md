# Yerel GPU kullanımı — tam istisna listesi ve ısı/saat protokolleri

> AGENTS.md kural 10'un tam ayrıntısı buraya taşındı (2026-11-16, oturum-açılış token tasarrufu). Bağlayıcı çekirdek
> AGENTS.md'de; işletim ayrıntısı (hangi iş, hangi sıcaklık/saat eşiği) burada. GPU gereken bir iş yazıyorsan BURAYI oku.

Yerel GPU (RTX 4060) hiçbir iş için serbest değildir: Ollama/llama-server, CUDA'lı PyTorch, GPU'lu Docker konteyneri,
LoRA eğitimi YOK. `meds-ollama` ve eğitim ortamı 2026-10-11'de kaldırıldı. Vektörleme yalnız CPU servisleriyle:
`meds-embed-bge` (bge-m3, 127.0.0.1:8094) ve `meds-embed` (e5-small, :8091); Python'da `scripts/altyapi/agents/lib.py::embed`.
LLM gereken her iş ücretsiz bulut zincirine gider (`MEDS_LLM_BACKEND=cloud`).

GPU ancak **dış koruyucu `meds-gpuguard`** (`scripts/altyapi/agents/gpu_guard.py`) etkinken ve aşağıdaki sayılı istisnalarda açılır.
Koruyucu (saniyede bir): ≥76 °C dondur / ≤66 sürdür, acil ≥82 / ≤62, 20 sn ort. ≥%60 görev döngüsü, ≥6 °C/sn sıçrama
freni, kart görünmezse dondur. Yeni servis/betikte `CUDA_VISIBLE_DEVICES=""` ve systemd biriminde
`MemoryMax`/`CPUQuota`/`OOMScoreAdjust` ZORUNLU (makine 15 GB RAM; Claude oturumları korunur).

## İstisnalar

1. **Coqui XTTS v2 yerel ses işçisi** (kullanıcı izni 2026-10-16): `meds-xtts`, `scripts/uretim/sesli_anlatim/xtts_isci.py`. GPU ≤%60;
   YALNIZ `meds-gpuguard` çalışırken (birim `BindsTo`). VRAM payı 0.6, iş/bekleme ≈%60, 72 °C üstü yavaş, 64 °C tam hız,
   78 °C'de durur, GPU ancak ≤62 °C iken açılır, CUDA hatasında iş sıraya döner ve o oturum yalnız CPU. (2026-10-16 02:06'da
   %70 + 87–88 °C sıçramalarda kart düştü.) Başka iş bu istisnadan yararlanamaz.
2. **EMA Lightning çözücü/asistan seslendirmesi** (2026-10-18): `EMA_CIHAZ=cuda` + `meds-gpuguard` + saat kilidi
   (`sudo nvidia-smi -lgc 300,1500`); başlatıcı `scripts/uretim/patoloji_cozucu/cozucu_ses_gpu.sh` (XTTS venv CUDA torch + EMA
   site-packages), VRAM payı 0,6, %60/ısı protokolü. Ölçüm ~5× hızlı, 59–65 °C. **Kullanıcı kararı 2026-10-24: EMA sesleri
   (çözücü, asistan, Öğren adımları) DAİMA bu yoldan GPU'da** (`ses_kuyruk.sh`, `asistan_ses_kuyruk.sh`, ders zinciri ses adımı
   → `cozucu_ses_gpu.sh`; koruyucu kapalıysa açılır, açılamazsa CPU'ya düşülmez, çıkış 75). *(2026-11-16 tek seferlik sapma:
   GPU erişilemediğinde kullanıcı izniyle EMA sesleri CPU'da üretilebildi — bkz. memory `kurul2-tasarruf-5-ders-cpu-ses`.)*
3. **Sesli ders vurgu üretimi** (2026-10-19): `scripts/uretim/sesli_anlatim/vurgu_uret.py --gpu`, bge-m3 fp16; `meds-gpuguard` + saat
   kilidi (kapalıysa durur), XTTS venv python'u, VRAM payı 0,6. Ölçüm: 26 ders birkaç dakikada, ≤62 °C.
4. **Sesli ders kelime zamanlaması** (2026-10-20): `scripts/uretim/sesli_anlatim/kelime_zaman.py --gpu`, faster-whisper medium
   int8_float16; `meds-gpuguard` + saat kilidi (kapalıysa CPU'ya döner); görev döngüsü ≈%60, 72 °C üstü yavaş, 78 °C'de ≤64'e
   dek durur, CUDA hatasında o oturum CPU. Ortam `meds/.venv-hizala` (CUDA kitaplıkları pip `nvidia-*`, `LD_LIBRARY_PATH`);
   birim `meds-kelime-zaman-hat.timer` (30 dk, `--oracle`: eksikleri çözer, Oracle'a rsync). ~3,5× hızlı.
5. **Sesli ders video dışa aktarımı** (2026-10-20): YALNIZ yetkili yönetici isteğiyle yerel GPU (NVENC); öğrenciler videoyu
   kendi cihazında üretir (`cdVideo.ts`). Kuyruk Oracle'da (`src/services/dersVideoIs.ts`), işçi `meds-ders-video`
   (`scripts/uretim/ders_video/video_uret.py bekle`): iş yalnız `meds-gpuguard` + bu açılışta saat kilidi sorunu yokken alınır (yoksa
   beklenir, CPU'ya düşülmez); kart yalnız ffmpeg sürecine açılır (çizim ve birim `CUDA_VISIBLE_DEVICES=""`), koruyucu
   `video_uret.py uret`'i dondurur (%60/ısı).
6. **Hoca ses kaydı dökümü** (2026-10-28): `scripts/uretim/ogrenci_drive/hoca_dokum.py --gpu`, başlatıcı `hoca_dokum_gpu.sh`
   (`MemoryMax=4G`, `CPUQuota=400%`); yalnız `meds-gpuguard` etkinken; görev döngüsü ≈%60, kart ≤62 °C iken açılır, 72 °C üstü
   yavaş, 78 °C'de ≤64'e dek durur. **Çekirdek saati ≤2500 MHz** (saniyede iki ölçüm, aşılırsa o oturum CPU; kalıcı tavan
   `sudo nvidia-smi -lgc 300,2500`). CUDA hatasında kalan parçalar CPU'da. Ölçüm: 3 dk ses 11 sn.
7. **Tıp Asistanı belge vektörleme** (2026-10-29): `scripts/asistan/vektorle.py --gpu`, XTTS venv python'u, bge-m3 fp16; yalnız
   `meds-gpuguard` etkinken, kart ≤62 °C iken açılır, VRAM payı 0,6, görev döngüsü ≈%60, 72 °C üstü yavaş, 78 °C'de ≤64'e dek
   durur. **Saat kilidi `sudo nvidia-smi -lgc 300,3000`** (3000 MHz aşılırsa o oturum CPU servisine döner; bu iş için tavan
   3000, diğer istisnaların tavanı için ayrı karar yok). Ölçüm: 34.313 belge 954 sn, ≤73 °C.
