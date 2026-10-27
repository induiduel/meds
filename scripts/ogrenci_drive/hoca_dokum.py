"""Hoca ses kaydını CPU'da metne döker (faster-whisper, LLM yok). Çıktı: <klasör>/hoca_dokum.json (segment + kelime zamanı).

  CUDA_VISIBLE_DEVICES="" meds/.venv-hizala/bin/python hoca_dokum.py <ses> <çıktı.json> [--model <ad>]
"""
import json
import os
import sys
import time

os.environ["CUDA_VISIBLE_DEVICES"] = ""
import subprocess  # noqa: E402

import numpy as np  # noqa: E402
from faster_whisper import WhisperModel  # noqa: E402

ses, cikti = sys.argv[1], sys.argv[2]
model_ad = sys.argv[sys.argv.index("--model") + 1] if "--model" in sys.argv else "mobiuslabsgmbh/faster-whisper-large-v3-turbo"
t0 = time.time()
m = WhisperModel(model_ad, device="cpu", compute_type="int8", cpu_threads=8)
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
    segs, _ = m.transcribe(p, language="tr", beam_size=5, condition_on_previous_text=False, word_timestamps=True,
                           vad_filter=False)  # amfi kaydında VAD konuşmayı eliyor, istem sanrı tekrarına yol açıyor
    for s in segs:
        a, b = ofs + s.start, ofs + s.end
        t = s.text.strip()
        if b <= son_bitis + 0.2 or not t or any(k in t.lower() for k in SANRI):
            continue
        out.append({"bas": round(a, 2), "son": round(b, 2), "metin": t,
                    "kelimeler": [[round(ofs + w.start, 2), round(ofs + w.end, 2), w.word.strip()] for w in (s.words or [])]})
        son_bitis = b
    json.dump({"parca": bas, "segmentler": out}, open(YARIM, "w"), ensure_ascii=False)
    print(f"{min(bas + PARCA, sure) / 60:.1f} / {sure / 60:.1f} dk, {len(out)} segment", flush=True)
json.dump({"model": model_ad, "sure": sure, "islem_sn": round(time.time() - t0), "segmentler": out},
          open(cikti, "w"), ensure_ascii=False, indent=1)
print("bitti", len(out), "segment", round(time.time() - t0), "sn")
os.remove(YARIM)
