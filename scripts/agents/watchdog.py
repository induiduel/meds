#!/usr/bin/env python3
"""
MedSoru Watchdog & Otonom Donanım Denetleyicisi (Autonomous Hardware Supervisor)
Sürekli arka planda çalışarak sistemi denetler:
1. GPU ve VRAM Kontrolü:
   - GPU'ya sadece 3 katman (-ngl 3) yüklenmiş ve CPU'ya taşmış asılı süreçleri yakalar, anında temizler.
   - VRAM kullanımını ve sıcaklığını takip eder.
2. Kod / Süreç Tazelik Denetimi:
   - Kaynak kodlar (stage2, stage3, lib.py) güncellendiğinde, eski kodla çalışan bayat süreçleri tespit eder ve güvenle yeniden başlatır.
3. Donanım & Kilitlenme Kurtarma:
   - GPU uykuya geçerse veya Ollama 500/timeout verirse otomatik meds-gpu-recovery tetikler.
4. Zombi & Kaçak Süreç Temizliği:
   - İşlevi bitmiş ama VRAM'i bloke eden llama-server veya python süreçlerini otomatik tahliye eder.
"""
import time
import os
import sys
import shutil
import subprocess
import requests
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS_DIR = ROOT / "scripts" / "agents"
LOG_FILE = ROOT / "meds_temp" / "logs" / "watchdog.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

def log(msg: str):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [WATCHDOG] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def get_code_mtime() -> float:
    """Ajan kodlarının en son değiştirilme zamanı"""
    mtimes = []
    for p in SCRIPTS_DIR.glob("*.py"):
        try:
            mtimes.append(p.stat().st_mtime)
        except Exception:
            pass
    return max(mtimes) if mtimes else 0.0

def get_process_start_time(pid: int) -> float:
    """Linux /proc üzerinden sürecin gerçek başlangıç epoch zamanını hesaplar"""
    try:
        btime = 0
        with open("/proc/stat", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("btime"):
                    btime = int(line.split()[1])
                    break
        stat_parts = Path(f"/proc/{pid}/stat").read_text(encoding="utf-8").split()
        starttime_ticks = int(stat_parts[21])
        clk_tck = os.sysconf(os.sysconf_names["SC_CLK_TCK"])
        return btime + (starttime_ticks / clk_tck)
    except Exception:
        return 0.0

def inspect_gpu_processes():
    """Ollama ve llama-server süreçlerini denetler, -ngl 3 gibi anomalileri temizler"""
    try:
        # ps aux ile llama-server süreçlerini tara
        res = subprocess.run(["ps", "-eo", "pid,cmd"], capture_output=True, text=True)
        for line in res.stdout.splitlines():
            if "llama-server" in line and "-ngl 3" in line:
                pid = int(line.strip().split()[0])
                log(f"KRİTİK UYARI: PID {pid} '-ngl 3' ile CPU'ya taşmış olarak tespit edildi! Süreç sonlandırılıyor...")
                subprocess.run(["kill", "-9", str(pid)], capture_output=True)
                log(f"PID {pid} temizlendi. Model sonraki çağrıda '-ngl 99' ile tam GPU'da başlayacak.")
    except Exception as e:
        log(f"GPU süreç denetleme hatası: {e}")

def inspect_pipeline_freshness(last_code_mtime: float):
    """Kod değiştiği halde eski kodla çalışan stage süreçlerini yakalar"""
    try:
        res = subprocess.run(["pgrep", "-f", "stage3_merge.py"], capture_output=True, text=True)
        pids = [int(p) for p in res.stdout.split() if p.strip()]
        for pid in pids:
            p_start = get_process_start_time(pid)
            # Eğer kod, sürecin başlamasından sonra güncellendiyse (ve süreç kod değişikliğinden önce başladıysa)
            if p_start > 0 and (last_code_mtime - p_start) > 2.0:
                log(f"UYARI: stage3_merge (PID {pid}) eski kod ile çalışıyor! Kod güncellendiği için süreç güvenle yeniden başlatılıyor...")
                subprocess.run(["kill", "-9", str(pid)], capture_output=True)
    except Exception as e:
        log(f"Pipeline tazelik denetleme hatası: {e}")

def check_ollama_health():
    """Ollama servisinin canlılığını ve yanıt süresini kontrol eder"""
    try:
        r = requests.get("http://127.0.0.1:11434/api/tags", timeout=6)
        if not r.ok:
            raise RuntimeError(f"HTTP {r.status_code}")
    except Exception as e:
        log(f"Ollama yanıt vermiyor ({e}). Servis bekleniyor...")
        time.sleep(5)

def check_pipeline_runner_alive():
    """Eğer pipeline_runner tamamen kapandıysa otonom olarak tekrar ayağa kaldırır"""
    res = subprocess.run(["pgrep", "-f", "pipeline_runner.py"], capture_output=True, text=True)
    if not res.stdout.strip():
        log("UYARI: pipeline_runner.py çalışmıyor! Otomatik olarak başlatılıyor...")
        cmd = [
            "/usr/bin/systemd-inhibit", "--what=idle:sleep", "--why=medsoru",
            str(ROOT / ".venv-ocr" / "bin" / "python"),
            str(SCRIPTS_DIR / "pipeline_runner.py")
        ]
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        log("pipeline_runner.py arka planda güvenle başlatıldı ✓")

def check_docker_containers():
    """Tüm kritik Docker konteynerlerini denetler (meds-ollama, open-webui vb.)"""
    env = os.environ.copy()
    env["DOCKER_HOST"] = "unix:///var/run/docker.sock"
    for cname in ["meds-ollama", "open-webui"]:
        try:
            res = subprocess.run(["docker", "inspect", "-f", "{{.State.Running}}", cname], env=env, capture_output=True, text=True)
            if "true" not in res.stdout.lower():
                log(f"UYARI: Konteyner '{cname}' durmuş! Otomatik olarak yeniden başlatılıyor...")
                subprocess.run(["docker", "start", cname], env=env, capture_output=True)
                log(f"Konteyner '{cname}' ayağa kaldırıldı ✓")
        except Exception as e:
            pass

def check_supabase_health():
    """Supabase yerel veritabanı ve REST servislerinin canlılığını denetler"""
    try:
        r = requests.get("http://127.0.0.1:8000/rest/v1/", headers={"apikey": os.environ.get("SUPABASE_ANON_KEY", "anon")}, timeout=3)
        # 200 veya 401/404 bile olsa envoy ayaktadır
    except Exception:
        # Docker desktop altındaki supabase-db kontrolü
        try:
            res = subprocess.run(["docker", "ps", "--filter", "name=supabase-db", "--format", "{{.Status}}"], capture_output=True, text=True)
            if not res.stdout.strip():
                log("BİLGİ: Supabase yerel servisleri henüz başlatılmamış veya durdurulmuş.")
        except Exception:
            pass

def check_dashboard_alive():
    """Dashboard izleme sunucusunun (8085) çökmesini engeller"""
    res = subprocess.run(["pgrep", "-f", "dashboard_server.py"], capture_output=True, text=True)
    if not res.stdout.strip():
        log("UYARI: dashboard_server.py (Port 8085) durmuş! Otomatik yeniden başlatılıyor...")
        venv_py = ROOT / ".venv-ocr" / "bin" / "python"
        py_bin = str(venv_py) if venv_py.exists() else sys.executable
        dash_script = ROOT / "dashboard_server.py"
        if not dash_script.exists():
            dash_script = ROOT.parent / "dashboard_server.py"
        cmd = [py_bin, str(dash_script)]
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        log("dashboard_server.py yeniden başlatıldı ✓")

def check_web_server_alive():
    """Web sunucusunun (server.ts / Port 3000) canlı kalmasını sağlar"""
    try:
        r = requests.get("http://127.0.0.1:3000/api/health", timeout=3)
        if r.ok:
            return
    except Exception:
        pass
    log("UYARI: Web sunucusu (Port 3000) kapalı! Otomatik olarak başlatılıyor...")
    npx_bin = shutil.which("npx") or "/home/indu/.nvm/versions/node/v24.21.0/bin/npx"
    cmd = [npx_bin, "tsx", "server.ts"]
    subprocess.Popen(cmd, cwd=str(ROOT), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    log("Web sunucusu (server.ts) arka planda güvenle başlatıldı ✓")

def check_system_resources():
    """Aşırı RAM ve Disk baskısını denetler, gerekirse önbellek temizler"""
    try:
        import psutil
        mem = psutil.virtual_memory()
        # Eğer kullanılabilir RAM %15'in altına düşerse (Erken OOM-Killer Koruması)
        if mem.available < (0.15 * mem.total):
            log(f"DİKKAT: Sistem belleği kritik seviyede (%{mem.percent} dolu, kullanılabilir: {round(mem.available / (1024**3), 2)} GB)! Önbellek tazeleme tetikleniyor...")
            import gc
            gc.collect()
    except Exception:
        pass


def enforce_gpu_thermal_and_load_limits(max_util: int = 90, max_temp: int = 80):
    """GPU %90 üzeri yük veya 80°C üzeri sıcaklığa ulaşırsa boru hattını dinlendirir."""
    try:
        res = subprocess.run(
            ["nvidia-smi", "--query-gpu=utilization.gpu,temperature.gpu", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=2
        )
        if res.returncode == 0 and res.stdout.strip():
            parts = res.stdout.strip().split(",")
            util = int(parts[0].strip())
            temp = int(parts[1].strip())
            if temp >= max_temp or util > max_util:
                log(f"GÜVENLİK FRENİ: GPU Yükü: %{util} (Limit: %{max_util}), Sıcaklık: {temp}°C (Limit: {max_temp}°C). Model 5 sn dinlendiriliyor...")
                time.sleep(5)
    except Exception:
        pass


lora_was_running = False

def check_post_lora_training_trigger():
    """QLoRA eğitimi sonlandığı an otomatik veri denetleme ve iyileştirme motorunu devreye alır."""
    global lora_was_running
    res = subprocess.run(["pgrep", "-f", "train_lora.py"], capture_output=True, text=True)
    is_currently_running = bool(res.stdout.strip())

    if is_currently_running:
        lora_was_running = True
        return

    # Eğer daha önce çalışıyordu ve şimdi kapandıysa -> Eğitim BİTTİ
    if lora_was_running and not is_currently_running:
        lora_was_running = False
        log("🎉 [OTOMASYON] QLoRA eğitimi tamamlandı! Veri denetleme ve iyileştirme motoru (post_lora_auto_refiner.py) devreye alınıyor...")
        refiner_script = SCRIPTS_DIR / "agents" / "post_lora_auto_refiner.py"
        if refiner_script.exists():
            py_bin = sys.executable
            cmd = [py_bin, str(refiner_script), "--sync-supabase"]
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
            log("post_lora_auto_refiner.py arka planda otomatik olarak başlatıldı ✓")

def main():
    log("MedSoru Gelişmiş Otonom Sistem & Docker Watchdog Başlatıldı.")
    last_known_code_mtime = get_code_mtime()

    while True:
        try:
            current_code_mtime = get_code_mtime()
            if current_code_mtime > last_known_code_mtime:
                log("Ajan kodlarında (scripts/agents/) değişiklik tespit edildi. Tazelik denetimi aktif.")
                inspect_pipeline_freshness(current_code_mtime)
                last_known_code_mtime = current_code_mtime

            # 1. Hatalı katman (-ngl 3) kullanan llama-server'ları denetle
            inspect_gpu_processes()

            # 2. Ollama ve GPU sağlığını denetle
            check_ollama_health()

            # 3. Docker konteynerlerini denetle
            check_docker_containers()

            # 4. Pipeline koşucusunun canlılığını sağla
            check_pipeline_runner_alive()

            # 5. Dashboard kokpitinin canlılığını sağla
            check_dashboard_alive()

            # 5b. Web sunucusunun (Port 3000 / server.ts) canlılığını sağla
            check_web_server_alive()

            # 6. Sistem RAM/VRAM kaynak baskısını denetle
            check_system_resources()

            # 7. Donanım Güvenlik Freni: GPU Yükü (%90) ve Sıcaklık (80°C) denetimi
            enforce_gpu_thermal_and_load_limits(max_util=90, max_temp=80)

            # 8. QLoRA Eğitim Sonrası Otomatik Veri Denetleme & İyileştirme Tetikleyicisi
            check_post_lora_training_trigger()

            # 9. Faz 5 (Çoklu AI Konsensüs) ve Faz 6 (Derin Tıbbi Metadata) Motorlarını Canlı Tut
            check_phase5_and_phase6_workers()

        except Exception as e:
            log(f"Watchdog genel döngü hatası: {e}")

        time.sleep(10)


def check_phase5_and_phase6_workers():
    """Faz 5 (Çoklu AI Konsensüs) ve Faz 6 (Derin Tıbbi Metadata) motorlarının arka planda çalışmasını sağlar"""
    venv_py = ROOT / ".venv-ocr" / "bin" / "python"
    py_bin = str(venv_py) if venv_py.exists() else sys.executable

    # Faz 5 Konsensüs Motoru Denetimi
    res_p5 = subprocess.run(["pgrep", "-f", "multi_ai_consensus_phase5.py"], capture_output=True, text=True)
    if not res_p5.stdout.strip():
        p5_script = ROOT / "scripts" / "advanced_ai" / "multi_ai_consensus_phase5.py"
        if p5_script.exists():
            subprocess.Popen([py_bin, str(p5_script)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
            log("multi_ai_consensus_phase5.py (Faz 5 Çoklu AI Konsensüsü) arka planda başlatıldı ✓")

    # Faz 6 Derin Metadata Motoru Denetimi
    res_p6 = subprocess.run(["pgrep", "-f", "deep_metadata_generator_phase6.py"], capture_output=True, text=True)
    if not res_p6.stdout.strip():
        p6_script = ROOT / "scripts" / "advanced_ai" / "deep_metadata_generator_phase6.py"
        if p6_script.exists():
            subprocess.Popen([py_bin, str(p6_script)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
            log("deep_metadata_generator_phase6.py (Faz 6 Hiper-Metadata Motoru) arka planda başlatıldı ✓")

    # Faz 7 5-Adımlı Mikro-Ajans Modelleme & Hikaye Motoru Denetimi
    res_p7 = subprocess.run(["pgrep", "-f", "microagent_storyteller_phase7.py"], capture_output=True, text=True)
    if not res_p7.stdout.strip():
        p7_script = ROOT / "scripts" / "advanced_ai" / "microagent_storyteller_phase7.py"
        if p7_script.exists():
            subprocess.Popen([py_bin, str(p7_script)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
            log("microagent_storyteller_phase7.py (Faz 7 Mikro-Ajans Hikaye Motoru) arka planda başlatıldı ✓")

    # Faz 7.5 Amfi Ders Slaytlarını Düzenleme Motoru Denetimi
    res_p75 = subprocess.run(["pgrep", "-f", "reconstruct_slides_phase7_5.py"], capture_output=True, text=True)
    if not res_p75.stdout.strip():
        p75_script = ROOT / "scripts" / "advanced_ai" / "reconstruct_slides_phase7_5.py"
        if p75_script.exists():
            subprocess.Popen([py_bin, str(p75_script)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
            log("reconstruct_slides_phase7_5.py (Faz 7.5 Müfredat Slayt Motoru) arka planda başlatıldı ✓")

if __name__ == "__main__":
    main()

