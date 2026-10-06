#!/usr/bin/env python3
"""
GPU koruyucu (meds-gpuguard servisi) — sıcaklık ve kullanım sınırlarını GERÇEKTEN uygular.

Eski watchdog "freni" yalnızca watchdog'un kendisini uyutuyordu; GPU'yu kullanan süreçlere etkisi yoktu.
Bu servis GPU istemcisi faz süreçlerini SIGSTOP ile duraklatır, güvenli aralığa dönünce SIGCONT ile sürdürür.
(Ollama'daki o an çalışan tek istek biter, yenisi gelmez → GPU boşa düşer ve soğur.)

Sınırlar (kullanıcı: güvenli aralık < 90 °C ve < %92 kullanım, asla 95 °C üstü):
  * sıcaklık ≥ 89 °C           → duraklat; ≤ 86 °C olunca sürdür
  * 30 sn ortalama kullanım ≥ %92 → 8 sn duraklat (görev döngüsü; ortalamayı sınırın altına çeker)
  * sıcaklık ≥ 95 °C (acil)     → duraklat, uyarı yaz; ≤ 85 °C olmadan sürdürme
Servis durursa/çökerse (SIGTERM, atexit) ve açılışta: duraklatılmış tüm süreçler sürdürülür (takılı kalmaz).
Ortam: MEDS_GPU_MAX_TEMP (89), MEDS_GPU_RESUME_TEMP (86), MEDS_GPU_MAX_UTIL (92), MEDS_GPU_EMERGENCY (95)
Kayıt: meds_temp/logs/gpu_guard.log  Durum: meds_temp/state/gpu_guard.json
"""
from __future__ import annotations

import atexit
import collections
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

TEMP = Path(os.environ.get("MEDS_TEMP_DIR") or Path(__file__).resolve().parents[3] / "meds_temp")
LOG = TEMP / "logs" / "gpu_guard.log"
STATE = TEMP / "state" / "gpu_guard.json"
MAX_TEMP = int(os.environ.get("MEDS_GPU_MAX_TEMP", "89"))
RESUME_TEMP = int(os.environ.get("MEDS_GPU_RESUME_TEMP", "86"))
MAX_UTIL = int(os.environ.get("MEDS_GPU_MAX_UTIL", "92"))
EMERGENCY = int(os.environ.get("MEDS_GPU_EMERGENCY", "95"))
POLL = 2.0
# GPU'ya iş gönderen (Ollama / CUDA) istemci betikleri
CLIENTS = ("deep_metadata_generator_phase6.py", "multi_ai_consensus_phase5.py", "phase10_concept_ids.py", "phase11_question_slide.py", "learn_links.py", "phase13_entities.py", "phase14_past_question_editor.py", "phase7_question_metadata_v2.py", "read_document.py", "thesaurus_anchor_phase6_5.py",
           "reconstruct_slides_phase7_5.py", "stage3_merge.py", "stage5_advanced_ai.py", "train_lora.py")

paused: set[int] = set()


def log(m: str):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [gpu_guard] {m}"
    print(line, flush=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def gpu():
    try:
        r = subprocess.run(["nvidia-smi", "--query-gpu=temperature.gpu,utilization.gpu", "--format=csv,noheader,nounits"],
                           capture_output=True, text=True, timeout=5)
        t, u = r.stdout.strip().splitlines()[0].split(",")
        return int(t), int(u)
    except Exception:
        return None, None


def client_pids() -> list[int]:
    me = os.getpid()
    out = []
    for d in Path("/proc").iterdir():
        if not d.name.isdigit() or int(d.name) == me:
            continue
        try:
            cmd = (d / "cmdline").read_bytes().replace(b"\0", b" ").decode("utf-8", "replace")
        except Exception:
            continue
        if "python" in cmd and any(c in cmd for c in CLIENTS):
            out.append(int(d.name))
    return out


def pause(reason: str):
    pids = [p for p in client_pids() if p not in paused]
    for p in pids:
        try:
            os.kill(p, signal.SIGSTOP)
            paused.add(p)
        except ProcessLookupError:
            pass
    if pids:
        log(f"DURAKLAT ({reason}): {len(pids)} süreç")


def resume(reason: str):
    n = 0
    for p in list(paused):
        try:
            os.kill(p, signal.SIGCONT)
            n += 1
        except ProcessLookupError:
            pass
        paused.discard(p)
    if n:
        log(f"SÜRDÜR ({reason}): {n} süreç")


def resume_all_stopped():
    """Açılış/kapanış: istemci betiklerinden durdurulmuş (T) kalan varsa sürdür."""
    for p in client_pids():
        try:
            st = (Path("/proc") / str(p) / "stat").read_text().split(")")[-1].split()[0]
            if st == "T":
                os.kill(p, signal.SIGCONT)
                log(f"takılı kalmış süreç sürdürüldü: {p}")
        except Exception:
            pass


def save_state(t, u, avg, mode):
    try:
        STATE.parent.mkdir(parents=True, exist_ok=True)
        STATE.write_text(json.dumps({"zaman": time.strftime("%Y-%m-%dT%H:%M:%S"), "sicaklik": t, "kullanim": u,
                                     "ort_kullanim_30sn": avg, "durum": mode, "duraklatilan": len(paused),
                                     "sinirlar": {"sicaklik": MAX_TEMP, "surdur": RESUME_TEMP, "kullanim": MAX_UTIL,
                                                  "acil": EMERGENCY}}, ensure_ascii=False))
    except Exception:
        pass


def main():
    def bye(*_):
        resume("koruyucu kapanıyor")
        sys.exit(0)

    atexit.register(lambda: resume("koruyucu kapanıyor"))
    signal.signal(signal.SIGTERM, bye)
    signal.signal(signal.SIGINT, bye)
    resume_all_stopped()
    log(f"başladı: sıcaklık < {MAX_TEMP} °C (sürdür ≤ {RESUME_TEMP}), kullanım < %{MAX_UTIL}, acil {EMERGENCY} °C")
    utils = collections.deque(maxlen=int(30 / POLL))
    mode = "normal"            # normal | isi | acil | kullanim
    duty_until = 0.0
    last_save = 0.0
    while True:
        t, u = gpu()
        now = time.time()
        if t is None:                       # nvidia-smi kartı görmüyor (ör. Xid 79: yeniden başlatma gerekli)
            if now - last_save > 5:
                save_state(None, None, None, "gpu_yok")
                last_save = now
            time.sleep(POLL * 5)
            continue
        if mode not in ("isi", "acil", "kullanim"):
            utils.append(u)
        avg = round(sum(utils) / len(utils), 1) if utils else 0
        if t >= EMERGENCY:
            if mode != "acil":
                log(f"ACİL: GPU {t} °C ≥ {EMERGENCY} °C")
            mode = "acil"
            pause(f"acil {t} °C")
        elif t >= MAX_TEMP and mode in ("normal", "kullanim"):
            mode = "isi"
            pause(f"{t} °C ≥ {MAX_TEMP} °C")
        elif mode == "isi" and t <= RESUME_TEMP:
            mode = "normal"
            utils.clear()
            resume(f"{t} °C")
        elif mode == "acil" and t <= 85:
            mode = "normal"
            utils.clear()
            resume(f"acil sonrası {t} °C")
        elif mode == "normal" and len(utils) == utils.maxlen and avg >= MAX_UTIL:
            mode = "kullanim"
            duty_until = now + 8
            pause(f"30 sn ort. kullanım %{avg} ≥ %{MAX_UTIL}")
        elif mode == "kullanim" and now >= duty_until:
            mode = "normal"
            for _ in range(utils.maxlen // 3):       # pencereyi kısmen boşalt: duraklatma ortalamaya yansısın
                utils.append(0)
            resume("görev döngüsü bitti")
        # duraklatma sırasında yeni başlayan istemciler de duraklatılır
        if mode in ("isi", "acil", "kullanim"):
            pause("yeni istemci")
        if now - last_save > 5:
            save_state(t, u, avg, mode)
            last_save = now
        time.sleep(POLL)


if __name__ == "__main__":
    main()
