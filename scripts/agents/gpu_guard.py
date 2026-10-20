#!/usr/bin/env python3
"""
GPU koruyucu (meds-gpuguard) — dizüstü RTX 4060'ı ısı ve aşırı yükten korur; XTTS işçisinden BAĞIMSIZ dış fren.

Geçmiş: 2026-10-11'de GPU yasağıyla yedeğe kaldırılmıştı. 2026-10-16 02:06'da XTTS sentezi sırasında kart 87–88 °C
sıçramalarından sonra düştü (NVRM GSP rpcSendMessage hatası, nvidia-smi kartı görmedi, yeniden başlatma gerekti).
İşçinin kendi ısı denetimi cümle arasında ölçtüğü için sıçramayı yakalayamadı. Bu servis saniyede bir ölçer ve GPU
istemcisi süreçleri SIGSTOP ile dondurur (o an çalışan CUDA çekirdeği biter, yenisi gönderilmez → kart soğur), güvenli
aralığa dönünce SIGCONT ile sürdürür.

Sınırlar (kullanıcı: GPU en fazla %60, ısınmada katı protokol):
  * sıcaklık ≥ 76 °C              → duraklat; ≤ 66 °C olunca sürdür
  * sıcaklık ≥ 82 °C (acil)       → duraklat, uyarı; ≤ 62 °C olmadan sürdürme
  * 20 sn ortalama kullanım ≥ %60  → 6 sn duraklat (görev döngüsü)
  * 1 sn'de ≥ 8 °C yükselme ve ≥ 72 °C → 3 sn önleyici duraklatma (tehlike bölgesine yaklaşan sıçrama; 55→61 gibi
    soğuk bölgedeki normal yük artışı frenlenmez — 2026-10-16'da her cümlede frenleyip hızı 3,5 kat düşürüyordu)
  * nvidia-smi kartı görmüyor      → istemcileri duraklat (CUDA çağrısı askıda/hatalı), durumu "gpu_yok" yaz
  * saat kilidi yok: istemci çalışırken SM saati 2 ölçüm üst üste > 1600 MHz → meds_temp/state/gpu_kilit_yok
    (açılış kimliğiyle) yazılır, istemciler SIGTERM ile kapatılır; XTTS işçisi bu açılışta yalnız CPU kullanır.
    Kullanıcı `sudo nvidia-smi -lgc 300,1500` koyar (2026-10-16: kilitle tepe 65 °C, kilitsiz 79–89 °C); kilit yeniden
    başlatmada sıfırlandığı için işaret açılış kimliğine bağlıdır — her açılışta ilk GPU işinde yeniden sınanır.
Servis kapanırken (SIGTERM, atexit) ve açılışta duraklatılmış tüm istemciler sürdürülür (takılı kalmaz).
Ortam: MEDS_GPU_MAX_TEMP (76), MEDS_GPU_RESUME_TEMP (66), MEDS_GPU_EMERGENCY (82), MEDS_GPU_EMERGENCY_RESUME (62),
       MEDS_GPU_MAX_UTIL (60)
Kayıt: meds_temp/logs/gpu_guard.log   Durum: meds_temp/state/gpu_guard.json
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
MAX_TEMP = int(os.environ.get("MEDS_GPU_MAX_TEMP", "76"))
RESUME_TEMP = int(os.environ.get("MEDS_GPU_RESUME_TEMP", "66"))
EMERGENCY = int(os.environ.get("MEDS_GPU_EMERGENCY", "82"))
EMERGENCY_RESUME = int(os.environ.get("MEDS_GPU_EMERGENCY_RESUME", "62"))
MAX_UTIL = int(os.environ.get("MEDS_GPU_MAX_UTIL", "60"))
CLOCK_LIMIT = int(os.environ.get("MEDS_GPU_CLOCK_LIMIT", "1600"))  # MHz; üstü = saat kilidi yok
KILIT_YOK = TEMP / "state" / "gpu_kilit_yok"


def boot_id() -> str:
    try:
        return Path("/proc/sys/kernel/random/boot_id").read_text().strip()
    except Exception:
        return ""
RISE = 8          # °C / ölçüm: sıçrama başlangıcı
RISE_FROM = 72    # sıçrama freni yalnız bu sıcaklık ve üstünde (kart her hesaplama patlamasında 65→72 zıplar; normal)
POLL = 1.0
WINDOW = 20       # sn, kullanım ortalaması penceresi
# GPU'ya iş gönderen istemciler: yalnız ağır sentez süreçleri (bekleme döngüsü `xtts_isci.py bekle` dondurulmaz)
CLIENTS = ("xtts_isci.py sentezle", "xtts_isci.py dene", "xtts_ornekler.py",
           "video_uret.py uret")  # ders videosu: çizim süreci dondurulunca boru durur, NVENC boşa düşer

paused: set[int] = set()


def log(m: str):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [gpu_guard] {m}"
    print(line, flush=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def gpu():
    try:
        r = subprocess.run(["nvidia-smi", "--query-gpu=temperature.gpu,utilization.gpu,clocks.sm", "--format=csv,noheader,nounits"],
                           capture_output=True, text=True, timeout=5)
        t, u, c = r.stdout.strip().splitlines()[0].split(",")
        return int(t), int(u), int(c)
    except Exception:
        return None, None, None


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
    """Açılış/kapanış: istemcilerden durdurulmuş (T) kalan varsa sürdür."""
    for p in client_pids():
        try:
            st = (Path("/proc") / str(p) / "stat").read_text().split(")")[-1].split()[0]
            if st == "T":
                os.kill(p, signal.SIGCONT)
                log(f"takılı kalmış süreç sürdürüldü: {p}")
        except Exception:
            pass


def save_state(t, u, avg, mode, tmax):
    try:
        STATE.parent.mkdir(parents=True, exist_ok=True)
        STATE.write_text(json.dumps({"zaman": time.strftime("%Y-%m-%dT%H:%M:%S"), "sicaklik": t, "kullanim": u,
                                     "ort_kullanim": avg, "durum": mode, "duraklatilan": len(paused), "son_tepe": tmax,
                                     "sinirlar": {"sicaklik": MAX_TEMP, "surdur": RESUME_TEMP, "acil": EMERGENCY,
                                                  "acil_surdur": EMERGENCY_RESUME, "kullanim": MAX_UTIL}},
                                    ensure_ascii=False))
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
    log(f"başladı: duraklat ≥ {MAX_TEMP} °C (sürdür ≤ {RESUME_TEMP}), acil ≥ {EMERGENCY} (sürdür ≤ {EMERGENCY_RESUME}), "
        f"kullanım < %{MAX_UTIL}, sıçrama ≥ {RISE} °C/sn (≥ {RISE_FROM} °C)")
    utils = collections.deque(maxlen=int(WINDOW / POLL))
    mode = "normal"            # normal | isi | acil | kullanim | sicrama | gpu_yok
    until = 0.0
    last_save = 0.0
    prev_t = None
    tmax = 0
    yuksek_saat = 0
    while True:
        t, u, clk = gpu()
        now = time.time()
        if t is None:
            if mode != "gpu_yok":
                log("GPU görünmüyor (nvidia-smi): istemciler duraklatılıyor — kart düşmüş olabilir (yeniden başlatma gerekebilir)")
                mode = "gpu_yok"
            pause("gpu yok")
            if now - last_save > 5:
                save_state(None, None, None, mode, tmax)
                last_save = now
            time.sleep(POLL * 5)
            continue
        if mode == "gpu_yok":
            mode = "isi"           # kart geri geldi: soğuma eşiği altında sürdürülür
            log(f"GPU yeniden görünüyor ({t} °C)")
        tmax = max(tmax, t)
        # saat kilidi denetimi: istemci GPU'yu kullanırken saat sınırı aşılıyorsa kilit yok
        if clk is not None and clk > CLOCK_LIMIT and u > 20 and client_pids():
            yuksek_saat += 1
            if yuksek_saat >= 2:
                if not (KILIT_YOK.exists() and KILIT_YOK.read_text().strip() == boot_id()):
                    KILIT_YOK.parent.mkdir(parents=True, exist_ok=True)
                    KILIT_YOK.write_text(boot_id())
                    log(f"SAAT KİLİDİ YOK: SM {clk} MHz > {CLOCK_LIMIT} → istemciler kapatılıyor, bu açılışta XTTS yalnız CPU "
                        f"(kilit: sudo nvidia-smi -lgc 300,1500; sonra {KILIT_YOK} silinir)")
                resume("kilit yok, kapatılıyor")
                for p in client_pids():
                    try:
                        os.kill(p, signal.SIGTERM)
                    except ProcessLookupError:
                        pass
                yuksek_saat = 0
        else:
            yuksek_saat = 0
        if mode == "normal":
            utils.append(u)
        avg = round(sum(utils) / len(utils), 1) if utils else 0
        if t >= EMERGENCY:
            if mode != "acil":
                log(f"ACİL: GPU {t} °C ≥ {EMERGENCY} °C")
            mode = "acil"
            pause(f"acil {t} °C")
        elif t >= MAX_TEMP and mode in ("normal", "kullanim", "sicrama"):
            mode = "isi"
            pause(f"{t} °C ≥ {MAX_TEMP} °C")
        elif mode == "isi" and t <= RESUME_TEMP:
            mode = "normal"
            utils.clear()
            resume(f"{t} °C")
        elif mode == "acil" and t <= EMERGENCY_RESUME:
            mode = "normal"
            utils.clear()
            resume(f"acil sonrası {t} °C")
        elif mode == "normal" and prev_t is not None and t - prev_t >= RISE and t >= RISE_FROM:
            mode, until = "sicrama", now + 3
            pause(f"sıçrama {prev_t}→{t} °C")
        elif mode == "normal" and len(utils) == utils.maxlen and avg >= MAX_UTIL:
            mode, until = "kullanim", now + 6
            pause(f"{WINDOW} sn ort. kullanım %{avg} ≥ %{MAX_UTIL}")
        elif mode in ("kullanim", "sicrama") and now >= until:
            mode = "normal"
            for _ in range(utils.maxlen // 3):       # duraklatma ortalamaya yansısın
                utils.append(0)
            resume("görev döngüsü bitti")
        if mode in ("isi", "acil", "kullanim", "sicrama"):
            pause("yeni istemci")
        prev_t = t
        if now - last_save > 5:
            save_state(t, u, avg, mode, tmax)
            last_save = now
            tmax = t
        time.sleep(POLL)


if __name__ == "__main__":
    main()
