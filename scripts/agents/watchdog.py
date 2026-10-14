#!/usr/bin/env python3
"""
MeDSor Watchdog: pipeline_runner, dashboard (8085) ve web sunucusunun (3000) canlılığını, ajan kodu değişince
bayat süreçleri ve sistem belleğini denetler. Yerel GPU/Ollama denetimi yok (2026-10-11: yerel GPU yasak).
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
# Günlük veri klasöründeki meds_temp/logs altına (repo içine değil)
LOG_FILE = Path(os.environ.get("MEDS_TEMP_DIR") or ROOT.parent / "meds_temp") / "logs" / "watchdog.log"
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

def systemd_user_active(unit: str) -> bool:
    """systemd --user servisi etkin/çalışıyor mu (servis varsa yeniden başlatmayı systemd'ye bırak)."""
    try:
        r = subprocess.run(["systemctl", "--user", "is-active", unit], capture_output=True, text=True, timeout=3)
        state = r.stdout.strip()
        if state in ("active", "activating", "reloading"):
            return True
        r = subprocess.run(["systemctl", "--user", "is-enabled", unit], capture_output=True, text=True, timeout=3)
        return r.stdout.strip() == "enabled"
    except Exception:
        return False


def port_in_use(port: int) -> bool:
    import socket
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=1):
            return True
    except OSError:
        return False


_web_failures = 0
# Çıkış yapan faz betikleri hemen yeniden doğmasın: betik adı -> son başlatma zamanı
_last_phase_launch: dict = {}
PHASE_RELAUNCH_COOLDOWN_SEC = 600

def check_pipeline_runner_alive():
    """Eğer pipeline_runner tamamen kapandıysa otonom olarak tekrar ayağa kaldırır"""
    # meds-pipeline systemd servisi varsa yeniden başlatma onun işi (Restart=always). İkinci bir
    # kopya kilidi tutup servisin kendi örneğini her 30 sn'de çıkışa zorluyordu.
    if systemd_user_active("meds-pipeline.service"):
        return
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

def check_supabase_health():
    """Veritabanı (meds-pg) ve eski betikler için REST uyumluluk kapısının (127.0.0.1:8000) canlılığı.
    Supabase 2026-10-12'de kaldırıldı; ad geriye uyumluluk için korunuyor."""
    try:
        res = subprocess.run(["docker", "exec", "meds-pg", "pg_isready", "-U", "meds", "-d", "meds"], capture_output=True, text=True, timeout=10)
        if res.returncode != 0:
            log("UYARI: meds-pg veritabanı yanıt vermiyor (docker compose -f deploy/pg/docker-compose.yml --profile cihaz up -d).")
    except Exception:
        pass
    try:
        requests.get("http://127.0.0.1:8000/rest/v1/", timeout=3)
    except Exception:
        log("BİLGİ: REST uyumluluk kapısı (meds-rest, :8000) kapalı; eski betikler veritabanına yazamaz.")

def check_dashboard_alive():
    """Dashboard izleme sunucusunun (8085) çökmesini veya asılı kalmasını engeller"""
    dash_alive = False
    try:
        r = requests.get("http://127.0.0.1:8085", timeout=3)
        if r.status_code in [200, 301, 302, 404]:
            dash_alive = True
    except Exception:
        dash_alive = False

    if not dash_alive:
        # Asılı kalmış süreç varsa temizle
        res = subprocess.run(["pgrep", "-f", "dashboard_server.py"], capture_output=True, text=True)
        if res.stdout.strip():
            log("UYARI: dashboard_server.py (Port 8085) yanıt vermiyor/kilitlenmiş! Sonlandırılıyor...")
            for pid in res.stdout.strip().split():
                try:
                    os.kill(int(pid), 9)
                except Exception:
                    pass
            time.sleep(1)

        log("UYARI: dashboard_server.py (Port 8085) başlatılıyor...")
        venv_py = ROOT / ".venv-ocr" / "bin" / "python"
        py_bin = str(venv_py) if venv_py.exists() else sys.executable
        dash_script = ROOT / "dashboard_server.py"
        if not dash_script.exists():
            dash_script = ROOT.parent / "dashboard_server.py"
        cmd = [py_bin, str(dash_script)]
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        log("dashboard_server.py yeniden başlatıldı ✓")


def check_web_server_alive():
    """Web sunucusunun (server.ts / Port 3000) canlı kalmasını sağlar.

    Sunucu açılırken RAG indeksini kurduğu için ~1 dk yanıt vermeyebilir. Eskiden 3 sn'lik tek
    hatada yeni kopya başlatılıyor, port dolu olduğundan bu kopyalar bellekte birikiyordu. Artık:
    meds-web servisi varsa ona bırakılır; port doluysa ya da server.ts süreci varsa dokunulmaz;
    yalnızca art arda 3 başarısız denetimden sonra başlatılır.
    """
    global _web_failures
    try:
        r = requests.get("http://127.0.0.1:3000/api/health", timeout=10)
        if r.ok:
            _web_failures = 0
            return
    except Exception:
        pass
    if systemd_user_active("meds-web.service") or port_in_use(3000):
        return
    if subprocess.run(["pgrep", "-f", "tsx.*server\\.ts"], capture_output=True, text=True).stdout.strip():
        return
    _web_failures += 1
    if _web_failures < 3:
        return
    _web_failures = 0
    log("UYARI: Web sunucusu (Port 3000) art arda 3 denetimde kapalı! Otomatik olarak başlatılıyor...")
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


def main():
    log("MeDSor Gelişmiş Otonom Sistem & Docker Watchdog Başlatıldı.")
    last_known_code_mtime = get_code_mtime()

    while True:
        try:
            current_code_mtime = get_code_mtime()
            if current_code_mtime > last_known_code_mtime:
                log("Ajan kodlarında (scripts/agents/) değişiklik tespit edildi. Tazelik denetimi aktif.")
                inspect_pipeline_freshness(current_code_mtime)
                last_known_code_mtime = current_code_mtime

            # 1–3. GPU/Ollama/Docker (meds-ollama, open-webui) denetimleri KALDIRILDI (2026-10-11): yerel GPU yasak,
            #      Ollama kapatıldı. Bu konteynerleri yeniden başlatmak GPU'yu geri açardı.

            # 4. Pipeline koşucusunun canlılığını sağla
            check_pipeline_runner_alive()

            # 5. Dashboard kokpitinin canlılığını sağla
            check_dashboard_alive()

            # 5b. Web sunucusunun (Port 3000 / server.ts) canlılığını sağla
            check_web_server_alive()

            # 6. Sistem RAM/VRAM kaynak baskısını denetle
            check_system_resources()

            # 7. GPU sıcaklık/kullanım sınırı artık meds-gpuguard servisinde (scripts/agents/gpu_guard.py):
            #    bu eski fren yalnızca watchdog'u uyutuyordu, GPU kullanan süreçlere etkisi yoktu.

            # 8–9. Otomatik faz geçişleri KAPALI (2026-10-07, kullanıcı isteği): watchdog hiçbir fazı/betiği kendiliğinden
            # başlatmaz (eskiden Faz 5 → 6 → 7.5 sırası ve LoRA sonrası iyileştirici). Fazlar yalnız panelden başlatılır.
            if os.environ.get("MEDS_PHASE_AUTO") == "1":
                check_phase5_and_phase6_workers()

        except Exception as e:
            log(f"Watchdog genel döngü hatası: {e}")

        time.sleep(10)


def _phase_cooldown_ok(name: str) -> bool:
    """Aynı faz betiği son 10 dk içinde başlatıldıysa (ve çıktıysa) tekrar başlatma."""
    now = time.time()
    if now - _last_phase_launch.get(name, 0) < PHASE_RELAUNCH_COOLDOWN_SEC:
        return False
    _last_phase_launch[name] = now
    return True


# Faz motorları GPU'yu paylaşır; aynı anda çalışınca laptop GPU'su 89 °C'ye çıkıyordu.
# Artık sırayla çalışırlar: biri bitmeden sıradaki başlamaz (5 → 6 → 7.5 → 5 ...).
PHASE_SEQUENCE = [
    ("multi_ai_consensus_phase5.py", "Faz 5 Çoklu AI Konsensüsü"),
    ("deep_metadata_generator_phase6.py", "Faz 6 Hiper-Metadata Motoru"),
    ("reconstruct_slides_phase7_5.py", "Faz 7.5 Müfredat Slayt Motoru"),
]
_next_phase_index = 0


def check_phase5_and_phase6_workers():
    """Faz 5, 6 ve 7.5 motorlarını SIRAYLA çalıştırır (aynı anda en fazla bir tane).

    meds-phases servisi (scripts/agents/phase_cycle.py) varsa zinciri o yönetir; watchdog karışmaz.
    """
    global _next_phase_index
    if systemd_user_active("meds-phases.service"):
        return
    # pipeline_runner zaten fazları bağımlılık sırasıyla yürütüyorsa ikinci bir
    # scheduler açılmaz; böylece GPU üzerinde aynı faz çift çalışmaz.
    if subprocess.run(["pgrep", "-f", "pipeline_runner.py"], capture_output=True, text=True).stdout.strip():
        return
    running = [
        name for name, _ in PHASE_SEQUENCE
        if subprocess.run(["pgrep", "-f", name], capture_output=True, text=True).stdout.strip()
    ]
    if running:
        # Çalışan fazdan (watchdog ya da boru hattı başlatmış olabilir) sonraki faz sıradadır
        names = [n for n, _ in PHASE_SEQUENCE]
        _next_phase_index = (names.index(running[0]) + 1) % len(PHASE_SEQUENCE)
        return  # bitmesini bekle

    venv_py = ROOT / ".venv-ocr" / "bin" / "python"
    py_bin = str(venv_py) if venv_py.exists() else sys.executable
    for _ in range(len(PHASE_SEQUENCE)):
        name, label = PHASE_SEQUENCE[_next_phase_index]
        _next_phase_index = (_next_phase_index + 1) % len(PHASE_SEQUENCE)
        script = ROOT / "scripts" / "advanced_ai" / name
        if script.exists() and _phase_cooldown_ok(name):
            subprocess.Popen([py_bin, str(script)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
            log(f"{name} ({label}) sırası geldi, başlatıldı ✓")
            return

if __name__ == "__main__":
    main()
