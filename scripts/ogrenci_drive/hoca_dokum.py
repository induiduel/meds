"""Hoca ses kaydını metne döker (faster-whisper, LLM yok). Çıktı: <klasör>/hoca_dokum.json (segment + kelime zamanı).

  meds/.venv-hizala/bin/python hoca_dokum.py <ses> <çıktı.json> [--model <ad>] [--gpu]

--gpu (kullanıcı izni 2026-10-28, AGENTS.md §10 altıncı istisna): YALNIZ meds-gpuguard etkinken; VRAM payı 0,6,
  görev döngüsü ≈%60, kart ≤62 °C iken açılır, 72 °C üstü yavaş, 78 °C'de ≤64'e dek durur. Çekirdek saati 2500 MHz'i
  geçerse (saniyede iki ölçüm) o oturum CPU'ya döner — kalıcı tavan için: sudo nvidia-smi -lgc 300,2500.
  CUDA hatasında kalan parçalar CPU'da sürer. Koruyucu ayrıca dondurabilir.
"""
import json
import os
import sys
import time

GPU = "--gpu" in sys.argv
if not GPU:
    os.environ["CUDA_VISIBLE_DEVICES"] = ""  # GPU yasak (AGENTS.md kural 10); --gpu yalnız koruyucuyla
import subprocess  # noqa: E402
import threading  # noqa: E402

import numpy as np  # noqa: E402
from faster_whisper import WhisperModel  # noqa: E402

ses, cikti = sys.argv[1], sys.argv[2]
model_ad = sys.argv[sys.argv.index("--model") + 1] if "--model" in sys.argv else "mobiuslabsgmbh/faster-whisper-large-v3-turbo"
SAAT_TAVAN = 2500  # MHz, kullanıcı sınırı


def gpu_oku(alan: str) -> int:
    try:
        r = subprocess.run(["nvidia-smi", f"--query-gpu={alan}", "--format=csv,noheader,nounits"],
                           capture_output=True, text=True, timeout=5)
        return int(float(r.stdout.strip().splitlines()[0]))
    except Exception:
        return 99999  # okunamıyorsa güvenli taraf: kart görünmüyor → dur/CPU


def cpu_model():
    return WhisperModel(model_ad, device="cpu", compute_type="int8", cpu_threads=int(os.environ.get("HD_THREADS", "8")))


cihaz, saat_asildi = "cpu", threading.Event()
if GPU and subprocess.run(["systemctl", "--user", "is-active", "--quiet", "meds-gpuguard"]).returncode != 0:
    print("meds-gpuguard etkin değil: GPU kullanılmaz, CPU (AGENTS.md §10)", file=sys.stderr, flush=True)
    GPU = False
t0 = time.time()
m = None
if GPU:
    while gpu_oku("temperature.gpu") > 62:  # kart ancak ≤62 °C iken açılır
        time.sleep(10)
    try:
        m = WhisperModel(model_ad, device="cuda", compute_type="int8_float16", num_workers=1)
        cihaz = "cuda"
    except Exception as e:
        print(f"CUDA açılamadı ({e}); CPU", file=sys.stderr, flush=True)
if m is None:
    m = cpu_model()


def saat_bekcisi():
    while cihaz == "cuda":
        if gpu_oku("clocks.gr") > SAAT_TAVAN:
            saat_asildi.set()
        time.sleep(0.5)


if cihaz == "cuda":
    threading.Thread(target=saat_bekcisi, daemon=True).start()


def gpu_nefes(hesap_sn: float):
    """%60 görev döngüsü + ısı protokolü (yalnız cuda)."""
    time.sleep(hesap_sn * 2 / 3)
    t = gpu_oku("temperature.gpu")
    if t >= 78:
        while gpu_oku("temperature.gpu") > 64:
            time.sleep(5)
    elif t > 72:
        time.sleep(hesap_sn * 1.5)
# Ham ses en iyi sonucu veriyor (süzgeç/normalleştirme denendi, 2026-10-27). PyAV sürüm uyumsuzluğu (metadata_errors) yüzünden ses ffmpeg ile 16 kHz mono float'a çözülür
ham = subprocess.run(["ffmpeg", "-v", "error", "-i", ses, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
# Tüm dosya tek seferde verilince model "Altyazı M.K." sanrısıyla erken bitiyor → 60 sn parçalar (2 sn bindirme)
ses_d = np.frombuffer(ham, dtype=np.float32)
SR, PARCA, BIN = 16000, 60, 2
sure = len(ses_d) / SR
# Yarım kalan iş (OOM, kesinti) kaldığı parçadan sürer: her parçadan sonra <çıktı>.yarim yazılır
YARIM = cikti + ".yarim"
yarim = json.load(open(YARIM)) if os.path.exists(YARIM) else {"parca": -1, "segmentler": []}
out = yarim["segmentler"]
son_bitis = out[-1]["son"] if out else 0.0
SANRI = ("altyazı m.k", "izlediğiniz için", "abone ol")
for bas in range(0, int(sure) + 1, PARCA):
    if bas <= yarim["parca"]:
        continue
    p = ses_d[max(0, (bas - BIN) * SR):(bas + PARCA) * SR]
    ofs = max(0, bas - BIN)
    tp = time.time()
    try:
        segs, _ = m.transcribe(p, language="tr", beam_size=5, condition_on_previous_text=False, word_timestamps=True,
                               vad_filter=False)  # amfi kaydında VAD konuşmayı eliyor, istem sanrı tekrarına yol açıyor
        segs = list(segs)
    except Exception as e:
        if cihaz != "cuda":
            raise
        print(f"CUDA hatası ({e}); bu oturum CPU", file=sys.stderr, flush=True)
        cihaz, m = "cpu", cpu_model()
        segs, _ = m.transcribe(p, language="tr", beam_size=5, condition_on_previous_text=False, word_timestamps=True,
                               vad_filter=False)
        segs = list(segs)
    for s in segs:
        a, b = ofs + s.start, ofs + s.end
        t = s.text.strip()
        if b <= son_bitis + 0.2 or not t or any(k in t.lower() for k in SANRI):
            continue
        out.append({"bas": round(a, 2), "son": round(b, 2), "metin": t,
                    "kelimeler": [[round(ofs + w.start, 2), round(ofs + w.end, 2), w.word.strip()] for w in (s.words or [])]})
        son_bitis = b
    json.dump({"parca": bas, "segmentler": out}, open(YARIM, "w"), ensure_ascii=False)
    print(f"{min(bas + PARCA, sure) / 60:.1f} / {sure / 60:.1f} dk, {len(out)} segment [{cihaz}]", flush=True)
    if cihaz == "cuda":
        if saat_asildi.is_set():
            print(f"GPU saati {SAAT_TAVAN} MHz'i aştı; bu oturum CPU (tavan: sudo nvidia-smi -lgc 300,{SAAT_TAVAN})",
                  file=sys.stderr, flush=True)
            cihaz, m = "cpu", cpu_model()
        else:
            gpu_nefes(time.time() - tp)
json.dump({"model": model_ad, "cihaz": cihaz, "sure": sure, "islem_sn": round(time.time() - t0), "segmentler": out},
          open(cikti, "w"), ensure_ascii=False, indent=1)
print("bitti", len(out), "segment", round(time.time() - t0), "sn")
os.remove(YARIM)
