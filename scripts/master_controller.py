#!/usr/bin/env python3
"""
MedSoru Master Orchestrator & Supervisor (scripts/master_controller.py)
En Yönetici, En Kapsamlı Sistem & Donanım Yöneticisi.

Özellikler:
1. Başlangıçta Terminal & GUI üzerinden Çalışma Modu Seçimi:
   - 1: Normal (GPU 1-3 GB VRAM, orta seviye sistem yükü, dengeli dinlenme)
   - 2: Güvenli (Zero GPU, No Local AI, Sadece CPU & RAM normal çalışır)
   - 3: Aşırı Güç (Watchdog termal ve yük sınırları dahilinde tam GPU/CPU performansı)
2. Arka Plan Scriptlerini Yönetme (Başlatma, Durdurma, Yeniden Başlatma, Canlı Durum):
   - pipeline_runner.py, watchdog.py, dashboard_server.py, web_server (server.ts),
     thesaurus_anchor, deep_metadata, reconstruct_slides,
     question_quality_inspector, fast_hybrid_server, monitor.py vb.
3. Çalışma Takvimi & Zamanlayıcı (Scheduler):
   - Belirli saatlerde çalışma, çalışma aralıkları (ör. 09:00 - 23:00) veya bekleme periyotları.
4. Donanım & Süreç Metrikleri (CPU, RAM, GPU Util/VRAM/Temp, Disk I/O).
5. Hem Bağımsız Tkinter GUI hem de Web Dashboard Entegrasyonu:
   - python3 scripts/master_controller.py --gui (Doğrudan Masaüstü GUI)
   - python3 scripts/master_controller.py --cli (Terminal İnteraktif Mod)
   - python3 scripts/master_controller.py --daemon (Konteyner/Arka Plan Yönetim Modu)
"""
import sys
import os
import time
import json
import signal
import subprocess
import threading
from pathlib import Path
from typing import Dict, Any, Optional

# Kök dizinler
ROOT_DIR = Path(__file__).resolve().parent.parent
PROJECT_PARENT = ROOT_DIR.parent
TEMP_DIR = PROJECT_PARENT / "meds_temp"
STATE_DIR = TEMP_DIR / "state"
CONFIG_FILE = STATE_DIR / "master_controller_config.json"
STATE_FILE = STATE_DIR / "master_controller_state.json"
LOG_DIR = TEMP_DIR / "logs"

STATE_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Yönetilen Scriptler Envanteri & Metadata
MANAGED_SCRIPTS = {
    "dashboard_server": {
        "name": "Canlı Telemetri & Analiz Kokpiti (Port 8085)",
        "script": "dashboard_server.py",
        "cwd": ROOT_DIR,
        "category": "core",
        "desc": "Port 8085 üzerinden canlı donanım, DiGraph, işlem kuyruğu ve kontrol arayüzü sunar.",
        "default_enabled": True,
        "supports_gpu": False
    },
    "watchdog": {
        "name": "Otonom Donanım & Süreç Bekçisi (Watchdog)",
        "script": "scripts/agents/watchdog.py",
        "cwd": ROOT_DIR,
        "category": "core",
        "desc": "Termal fren (%90 GPU, 80°C), çökme kurtarma, -ngl 3 taşma önleme ve otomatik süreç canlandırma.",
        "default_enabled": True,
        "supports_gpu": True
    },
    "pipeline_runner": {
        "name": "Ana Boru Hattı Koşucusu (Pipeline Runner)",
        "script": "scripts/agents/pipeline_runner.py",
        "cwd": ROOT_DIR,
        "category": "pipeline",
        "desc": "Aşama 2'den Aşama 10'a kadar tüm döngüyü sırayla ve güvenle yürüten ana motor.",
        "default_enabled": True,
        "supports_gpu": True
    },
    "web_server": {
        "name": "MedSoru Web Uygulaması (Port 3000)",
        "cmd": ["npx", "tsx", "server.ts"],
        "cwd": ROOT_DIR,
        "category": "frontend",
        "desc": "Next.js / Node.js tabanlı ana tıp soru portalı ve soru çözme arayüzü.",
        "default_enabled": True,
        "supports_gpu": False
    },
    "fast_hybrid_server": {
        "name": "BM25 + BGE-M3 Hibrit Arama Servisi (Port 8000)",
        "script": "scripts/fast_hybrid_server.py",
        "cwd": ROOT_DIR,
        "category": "search",
        "desc": "Soru ve slaytlar arasında anlık milisaniyelik anlamsal ve anahtar kelime araması yapar.",
        "default_enabled": False,
        "supports_gpu": True
    },
    "question_quality_inspector": {
        "name": "Soru Kalite & Mükerrerlik Denetmeni",
        "script": "scripts/agents/question_quality_inspector.py",
        "cwd": ROOT_DIR,
        "category": "audit",
        "desc": "Arka planda düşük CPU/GPU ile 6.263 soruyu tarar; hatalı ve mükerrer soruları raporlar.",
        "default_enabled": False,
        "supports_gpu": True
    },
    "thesaurus_anchor": {
        "name": "Faz 6.5: Tıbbi Sözlük (Thesaurus) & Kanıt Motoru",
        "script": "scripts/advanced_ai/thesaurus_anchor_phase6_5.py",
        "cwd": ROOT_DIR,
        "category": "advanced_ai",
        "desc": "Sorular ile amfi slaytlarını Latince/Türkçe tıp terminolojisi üzerinden kesin kancalar.",
        "default_enabled": False,
        "supports_gpu": True
    },
    "deep_metadata": {
        "name": "Faz 6: Derin Hiper-Metadata Motoru",
        "script": "scripts/advanced_ai/deep_metadata_generator_phase6.py",
        "cwd": ROOT_DIR,
        "category": "advanced_ai",
        "desc": "ICD-10, ayırıcı tanı, multidisipliner ilişkiler ve hiper-arama etiketleri üretir.",
        "default_enabled": False,
        "supports_gpu": True
    },
    "reconstruct_slides": {
        "name": "Faz 7.5: Amfi Ders Slaytı Müfredat Düzenleyici",
        "script": "scripts/advanced_ai/reconstruct_slides_phase7_5.py",
        "cwd": ROOT_DIR,
        "category": "advanced_ai",
        "desc": "KBÜ Dönem 3 resmi müfredat hedeflerine göre amfi slaytlarını zenginleştirir.",
        "default_enabled": False,
        "supports_gpu": True
    },
    "phase14_cloud": {
        "name": "Faz 14: Çıkmış Soru İyileştirme (Gemini Flash Bulut)",
        "script": "scripts/advanced_ai/phase14_cloud_question_editor.py",
        "cwd": ROOT_DIR,
        "category": "advanced_ai",
        "desc": "Gemini 3.8 Flash bulut modeliyle Robbins/Guyton tıp literatürüne dayalı kök/şık onarımı ve YZV üretimi.",
        "default_enabled": False,
        "supports_gpu": False
    },
    "phase14_local": {
        "name": "Faz 14: Çıkmış Soru Redaksiyonu (Gemma 3:4b Yerel GPU)",
        "script": "scripts/advanced_ai/phase14_past_question_editor.py",
        "cwd": ROOT_DIR,
        "category": "advanced_ai",
        "desc": "Yerel RTX 4060 GPU Gemma 3 modeliyle OCR/imla ve müfredat redaksiyonu üretimi.",
        "default_enabled": False,
        "supports_gpu": True
    },
    "terminal_monitor": {
        "name": "Terminal Curses Monitörü (monitor.py)",
        "script": "scripts/monitor.py",
        "cwd": ROOT_DIR,
        "category": "monitor",
        "desc": "Terminal içi canlı telemetri ve ilerleme tablosu.",
        "default_enabled": False,
        "supports_gpu": False
    }
}

MODES = {
    "1": {
        "key": "normal",
        "name": "Normal Mod",
        "desc": "Dengeli Performans: GPU 1-3 GB VRAM sınırı, orta seviye sistem tüketimi, otomatik dinlenme.",
        "gpu_limit_gb": 3,
        "gpu_enabled": True,
        "throttle_sleep_sec": 4.0,
        "ollama_keep_alive": "10m",
        "max_gpu_util": 75,
        "max_gpu_temp": 72
    },
    "2": {
        "key": "safe",
        "name": "Güvenli Mod",
        "desc": "Sıfır GPU & Sıfır Local AI: Yalnızca CPU ve RAM kullanılır, ekran kartı tamamen boşta kalır.",
        "gpu_limit_gb": 0,
        "gpu_enabled": False,
        "throttle_sleep_sec": 8.0,
        "ollama_keep_alive": "0m",
        "max_gpu_util": 0,
        "max_gpu_temp": 60
    },
    "3": {
        "key": "extreme",
        "name": "Aşırı Güç Modu",
        "desc": "Tam Performans: Watchdog güvenlik sınırları dahilinde maksimum GPU ve CPU gücü.",
        "gpu_limit_gb": 8,
        "gpu_enabled": True,
        "throttle_sleep_sec": 0.5,
        "ollama_keep_alive": "24h",
        "max_gpu_util": 90,
        "max_gpu_temp": 90
    }
}

class MasterController:
    def __init__(self):
        self.running = True
        self.lock = threading.Lock()
        self.processes: Dict[str, subprocess.Popen] = {}
        self.start_times: Dict[str, float] = {}
        self.config = self.load_config()
        self.current_mode = self.config.get("mode", "normal")
        self.schedule_config = self.config.get("schedule", {
            "enabled": False,
            "start_hour": 8,
            "end_hour": 23,
            "pause_on_battery": True
        })
        self.active_scripts_config = self.config.get("scripts_enabled", {
            k: v["default_enabled"] for k, v in MANAGED_SCRIPTS.items()
        })
        self.apply_mode_environment()

    def load_config(self) -> Dict[str, Any]:
        if CONFIG_FILE.exists():
            try:
                return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {
            "mode": "normal",
            "schedule": {"enabled": False, "start_hour": 8, "end_hour": 23},
            "scripts_enabled": {k: v["default_enabled"] for k, v in MANAGED_SCRIPTS.items()}
        }

    def save_config(self):
        with self.lock:
            self.config["mode"] = self.current_mode
            self.config["schedule"] = self.schedule_config
            self.config["scripts_enabled"] = self.active_scripts_config
            try:
                CONFIG_FILE.write_text(json.dumps(self.config, ensure_ascii=False, indent=2), encoding="utf-8")
            except Exception as e:
                print(f"[Master] Config kaydetme hatası: {e}")

    def apply_mode_environment(self):
        """Çalışma moduna göre çevre değişkenlerini ve limitleri uygular."""
        mode_data = next((v for v in MODES.values() if v["key"] == self.current_mode), MODES["1"])
        os.environ["MEDS_OPERATION_MODE"] = mode_data["key"]
        os.environ["MEDS_MAX_GPU_UTIL"] = str(mode_data["max_gpu_util"])
        os.environ["MEDS_MAX_GPU_TEMP"] = str(mode_data["max_gpu_temp"])
        os.environ["MEDS_THROTTLE_SLEEP"] = str(mode_data["throttle_sleep_sec"])

        if not mode_data["gpu_enabled"]:
            # Güvenli Mod: CUDA/GPU tamamen devredışı bırakılır
            os.environ["CUDA_VISIBLE_DEVICES"] = ""
            os.environ["OLLAMA_NUM_GPU"] = "0"
            os.environ["MEDS_DISABLE_GPU"] = "1"
        else:
            if "CUDA_VISIBLE_DEVICES" in os.environ and os.environ["CUDA_VISIBLE_DEVICES"] == "":
                del os.environ["CUDA_VISIBLE_DEVICES"]
            os.environ["OLLAMA_NUM_GPU"] = "99" if mode_data["key"] == "extreme" else "30"
            os.environ["MEDS_DISABLE_GPU"] = "0"

    def set_mode(self, mode_key: str):
        if mode_key not in ["normal", "safe", "extreme"]:
            return
        self.current_mode = mode_key
        self.apply_mode_environment()
        self.save_config()
        print(f"[Master] Çalışma modu '{mode_key}' olarak güncellendi.")

    def is_within_schedule(self) -> bool:
        if not self.schedule_config.get("enabled", False):
            return True
        now = time.localtime()
        sh = self.schedule_config.get("start_hour", 8)
        eh = self.schedule_config.get("end_hour", 23)
        if sh <= eh:
            return sh <= now.tm_hour < eh
        else: # Gece vardiyası (ör. 22:00 - 06:00)
            return now.tm_hour >= sh or now.tm_hour < eh

    def start_script(self, key: str):
        with self.lock:
            if key not in MANAGED_SCRIPTS:
                return False
            # Güvenli modda sadece CPU destekleyenler veya GPU kapatılmışlar çalışır
            meta = MANAGED_SCRIPTS[key]
            
            # Zaten çalışıyor mu kontrol et
            if self.is_script_running(key):
                return True

            log_path = LOG_DIR / f"{key}.log"
            out_file = open(log_path, "a", encoding="utf-8")

            env = os.environ.copy()
            py_bin = sys.executable

            cmd = meta.get("cmd")
            if not cmd:
                cmd = [py_bin, str(ROOT_DIR / meta["script"])]

            try:
                proc = subprocess.Popen(
                    cmd,
                    cwd=str(meta.get("cwd", ROOT_DIR)),
                    stdout=out_file,
                    stderr=subprocess.STDOUT,
                    env=env,
                    start_new_session=True
                )
                self.processes[key] = proc
                self.start_times[key] = time.time()
                self.active_scripts_config[key] = True
                self.save_config()
                print(f"[Master] {meta['name']} başlatıldı (PID: {proc.pid}).")
                return True
            except Exception as e:
                print(f"[Master] {key} başlatılırken hata: {e}")
                return False

    def stop_script(self, key: str):
        with self.lock:
            meta = MANAGED_SCRIPTS.get(key)
            if not meta:
                return False
            
            self.active_scripts_config[key] = False
            self.save_config()

            # Process tablosunda var mı?
            proc = self.processes.get(key)
            if proc and proc.poll() is None:
                try:
                    proc.terminate()
                    proc.wait(timeout=3)
                except Exception:
                    try:
                        proc.kill()
                    except Exception:
                        pass
                del self.processes[key]

            # pgrep ile isimden süreci de garanti temizle
            script_pattern = meta.get("script") or (meta.get("cmd")[-1] if meta.get("cmd") else None)
            if script_pattern:
                try:
                    subprocess.run(["pkill", "-9", "-f", Path(script_pattern).name], capture_output=True)
                except Exception:
                    pass

            self.start_times.pop(key, None)
            print(f"[Master] {key} durduruldu.")
            return True

    def is_script_running(self, key: str) -> bool:
        meta = MANAGED_SCRIPTS.get(key)
        if not meta:
            return False
        
        proc = self.processes.get(key)
        if proc and proc.poll() is None:
            return True

        # Dışarıdan pgrep ile kontrol et (başka oturumda başlatılmış olabilir)
        script_pattern = meta.get("script") or (meta.get("cmd")[-1] if meta.get("cmd") else None)
        if script_pattern:
            pname = Path(script_pattern).name
            res = subprocess.run(["pgrep", "-f", pname], capture_output=True, text=True)
            pids = res.stdout.strip().split()
            # Kendi PID'imizi hariç tut
            pids = [p for p in pids if p != str(os.getpid())]
            return len(pids) > 0

        return False

    def get_system_telemetry(self) -> Dict[str, Any]:
        telemetry = {
            "cpu_percent": 0.0,
            "cpu_count": os.cpu_count() or 4,
            "ram_used_gb": 0.0,
            "ram_total_gb": 0.0,
            "ram_percent": 0.0,
            "gpu_name": "N/A",
            "gpu_vram_used": 0,
            "gpu_vram_total": 8188,
            "gpu_util": 0,
            "gpu_temp": 0
        }
        try:
            import psutil
            mem = psutil.virtual_memory()
            telemetry["cpu_percent"] = psutil.cpu_percent(interval=None)
            telemetry["ram_used_gb"] = round((mem.total - mem.available) / (1024**3), 1)
            telemetry["ram_total_gb"] = round(mem.total / (1024**3), 1)
            telemetry["ram_percent"] = mem.percent
        except Exception:
            pass

        try:
            cmd = ["nvidia-smi", "--query-gpu=name,memory.used,memory.total,utilization.gpu,temperature.gpu", "--format=csv,noheader,nounits"]
            out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True).strip()
            if out:
                parts = [p.strip() for p in out.split(",")]
                telemetry["gpu_name"] = parts[0]
                telemetry["gpu_vram_used"] = int(parts[1])
                telemetry["gpu_vram_total"] = int(parts[2])
                telemetry["gpu_util"] = int(parts[3])
                telemetry["gpu_temp"] = int(parts[4])
        except Exception:
            pass

        return telemetry

    def get_all_status(self) -> Dict[str, Any]:
        """Tüm scriptlerin canlı süre, durum, görev ve hedef metriklerini toplar."""
        scripts_info = {}
        now = time.time()

        for k, meta in MANAGED_SCRIPTS.items():
            is_run = self.is_script_running(k)
            uptime_sec = round(now - self.start_times.get(k, now)) if is_run and k in self.start_times else 0
            scripts_info[k] = {
                "name": meta["name"],
                "category": meta["category"],
                "desc": meta["desc"],
                "running": is_run,
                "enabled_in_config": self.active_scripts_config.get(k, False),
                "uptime_sec": uptime_sec,
                "uptime_formatted": self.format_uptime(uptime_sec) if is_run else "Durduruldu"
            }

        # Boru hattı ve aşama hedefleri
        pipeline_metrics = self.get_pipeline_progress()

        return {
            "mode": self.current_mode,
            "mode_info": next((v for v in MODES.values() if v["key"] == self.current_mode), MODES["1"]),
            "schedule": self.schedule_config,
            "within_schedule": self.is_within_schedule(),
            "telemetry": self.get_system_telemetry(),
            "scripts": scripts_info,
            "pipeline": pipeline_metrics,
            "links": [
                {"name": "MedSoru Web Portalı", "url": "http://localhost:3000", "port": 3000, "icon": "graduation-cap"},
                {"name": "Hibrit Arama & Supabase REST", "url": "http://localhost:8000", "port": 8000, "icon": "bolt"},
                {"name": "Canlı Analiz Kokpiti", "url": "http://localhost:8085", "port": 8085, "icon": "gauge-high"}
            ]
        }

    def format_uptime(self, sec: int) -> str:
        if sec < 60:
            return f"{sec} sn"
        elif sec < 3600:
            return f"{sec // 60} dk {sec % 60} sn"
        else:
            return f"{sec // 3600} sa {(sec % 3600) // 60} dk"

    def get_pipeline_progress(self) -> Dict[str, Any]:
        status_file = STATE_DIR / "status.json"
        state_file = STATE_DIR / "pipeline_state.json"
        pipe_info = {
            "active_stage": "Boşta / Beklemede",
            "current_step": 0,
            "total_steps": 10,
            "completed_items": 0,
            "target_items": 413,
            "percent": 0.0,
            "details": ""
        }
        if status_file.exists():
            try:
                data = json.loads(status_file.read_text(encoding="utf-8"))
                runs = data.get("runs", [])
                if runs:
                    last_run = runs[-1]
                    pipe_info["active_stage"] = last_run.get("stage", "Tamamlandı")
            except Exception:
                pass

        if state_file.exists():
            try:
                st = json.loads(state_file.read_text(encoding="utf-8"))
                prog = st.get("progress", {}).get("pipeline", {})
                if prog:
                    pipe_info["current_step"] = prog.get("current", 0)
                    pipe_info["total_steps"] = prog.get("total", 10)
                    pipe_info["details"] = prog.get("msg", "")
                    if prog.get("total", 0) > 0:
                        pipe_info["percent"] = round((prog.get("current", 0) / prog.get("total", 1)) * 100, 1)
            except Exception:
                pass

        # Tamamlanan soru ve slayt sayısı
        t3 = TEMP_DIR / "temp3"
        q_file = t3 / "questions.jsonl"
        if q_file.exists():
            try:
                with open(q_file, "rb") as f:
                    pipe_info["completed_items"] = sum(1 for _ in f)
            except Exception:
                pass

        return pipe_info

    def write_state_file(self):
        try:
            status_data = self.get_all_status()
            STATE_FILE.write_text(json.dumps(status_data, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass

    def supervisor_loop(self):
        """Arka planda periyodik denetleme, zamanlayıcı kontrolü ve durum güncellemesi yapar."""
        while self.running:
            try:
                in_sched = self.is_within_schedule()
                
                # Eğer zamanlama dışındaysak ve durdurulması gerekiyorsa
                if not in_sched:
                    # Zaman dışı: Çalışan opsiyonel pipeline scriptlerini askıya al
                    for k in ["pipeline_runner", "thesaurus_anchor", "deep_metadata"]:
                        if self.is_script_running(k):
                            print(f"[Master Scheduler] Zamanlama dışı saat ({time.strftime('%H:%M')}). {k} bekletmeye alınıyor...")
                            self.stop_script(k)
                else:
                    # Zamanlama içinde: Konfigürasyonda 'açık' olanları çalışır durumda tut
                    for k, enabled in self.active_scripts_config.items():
                        if enabled and not self.is_script_running(k):
                            # Güvenli modda supports_gpu olan ağır AI işlerini başlatma
                            if self.current_mode == "safe" and MANAGED_SCRIPTS[k]["supports_gpu"] and k != "watchdog":
                                continue
                            print(f"[Master Supervisor] {k} durmuş, otomatik yeniden başlatılıyor...")
                            self.start_script(k)

                self.write_state_file()
            except Exception as e:
                print(f"[Master Supervisor Hata]: {e}")
            time.sleep(3)


# ==============================================================================
# Terminal İnteraktif Başlangıç Modu (Docker / CLI)
# ==============================================================================
def prompt_user_for_mode() -> str:
    print("\n" + "=" * 65)
    print("  🏥  MEDSORU AI MASTER YÖNETİCİ & SÜREÇ ORKESTRATÖRÜ")
    print("=" * 65)
    print("Sistemin çalışma ve güç modunu seçiniz:")
    print("  [1] Normal Mod    -> GPU'da 1-3 GB VRAM, orta seviye sistem yükü")
    print("  [2] Güvenli Mod   -> Sıfır GPU, No Local AI, Sadece CPU/RAM")
    print("  [3] Aşırı Güç     -> Tam Performans (Watchdog termal limitlerinde)")
    print("-" * 65)
    
    # Konteynerde veya non-interactive shell'de otomatik timeout ile varsayılanı seç
    if not sys.stdin.isatty():
        print("Etkileşimsiz ortam tespit edildi. Varsayılan [1] Normal Mod seçildi.")
        return "normal"

    try:
        choice = input("Lütfen seçim yapınız (1/2/3) [Varsayılan: 1]: ").strip()
        if choice == "2":
            return "safe"
        elif choice == "3":
            return "extreme"
        return "normal"
    except (EOFError, KeyboardInterrupt):
        return "normal"


# ==============================================================================
# Bağımsız Masaüstü GUI Penceresi (Tkinter GUI Dashboard)
# ==============================================================================
def run_desktop_gui(controller: MasterController):
    import tkinter as tk
    from tkinter import ttk, messagebox

    root = tk.Tk()
    root.title("MedSoru AI - Master Yönetim & Denetim Kokpiti")
    root.geometry("1100x750")
    root.minsize(950, 650)
    root.configure(bg="#0f172a")

    # Stil Ayarları
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#0f172a")
    style.configure("Card.TFrame", background="#1e293b", relief="flat")
    style.configure("TLabel", background="#0f172a", foreground="#f8fafc", font=("Helvetica", 10))
    style.configure("Title.TLabel", font=("Helvetica", 14, "bold"), foreground="#38bdf8")
    style.configure("Sub.TLabel", font=("Helvetica", 9), foreground="#94a3b8")
    style.configure("MetricVal.TLabel", font=("Helvetica", 18, "bold"), foreground="#ffffff")
    style.configure("TButton", font=("Helvetica", 9, "bold"), padding=5)

    # Üst Başlık & Mod Seçici
    header_frame = tk.Frame(root, bg="#1e293b", padx=15, pady=12, relief="groove", bd=1)
    header_frame.pack(fill="x", padx=10, pady=8)

    title_box = tk.Frame(header_frame, bg="#1e293b")
    title_box.pack(side="left")
    tk.Label(title_box, text="⚡ MedSoru AI Master Supervisor", font=("Helvetica", 15, "bold"), fg="#38bdf8", bg="#1e293b").pack(anchor="w")
    tk.Label(title_box, text="Tüm Yerel Scriptler, Donanım Koruyucusu ve Otomasyon Kontrol Masası", font=("Helvetica", 9), fg="#94a3b8", bg="#1e293b").pack(anchor="w")

    # Mod Butonları
    mode_box = tk.Frame(header_frame, bg="#1e293b")
    mode_box.pack(side="right")
    tk.Label(mode_box, text="Çalışma Modu:", font=("Helvetica", 9, "bold"), fg="#e2e8f0", bg="#1e293b").pack(side="left", padx=5)

    mode_var = tk.StringVar(value=controller.current_mode)

    def on_mode_change(new_mode):
        controller.set_mode(new_mode)
        mode_var.set(new_mode)
        update_mode_buttons()

    btn_normal = tk.Button(mode_box, text="1. Normal (1-3GB GPU)", command=lambda: on_mode_change("normal"), relief="flat", padx=8, pady=4, cursor="hand2")
    btn_normal.pack(side="left", padx=3)

    btn_safe = tk.Button(mode_box, text="2. Güvenli (Zero GPU)", command=lambda: on_mode_change("safe"), relief="flat", padx=8, pady=4, cursor="hand2")
    btn_safe.pack(side="left", padx=3)

    btn_extreme = tk.Button(mode_box, text="3. Aşırı Güç (Max GPU)", command=lambda: on_mode_change("extreme"), relief="flat", padx=8, pady=4, cursor="hand2")
    btn_extreme.pack(side="left", padx=3)

    def update_mode_buttons():
        m = controller.current_mode
        btn_normal.configure(bg="#3b82f6" if m == "normal" else "#334155", fg="white")
        btn_safe.configure(bg="#10b981" if m == "safe" else "#334155", fg="white")
        btn_extreme.configure(bg="#ef4444" if m == "extreme" else "#334155", fg="white")

    update_mode_buttons()

    # Donanım Metrikleri Çubuğu
    metric_frame = tk.Frame(root, bg="#0f172a", padx=10, pady=5)
    metric_frame.pack(fill="x")

    def create_card(parent, title, val_id, sub_id):
        card = tk.Frame(parent, bg="#1e293b", padx=12, pady=10, relief="solid", bd=1)
        card.pack(side="left", fill="both", expand=True, padx=4)
        tk.Label(card, text=title, font=("Helvetica", 9, "bold"), fg="#94a3b8", bg="#1e293b").pack(anchor="w")
        val_lbl = tk.Label(card, text="-", font=("Helvetica", 14, "bold"), fg="#ffffff", bg="#1e293b")
        val_lbl.pack(anchor="w", pady=2)
        sub_lbl = tk.Label(card, text="-", font=("Helvetica", 8), fg="#64748b", bg="#1e293b")
        sub_lbl.pack(anchor="w")
        return val_lbl, sub_lbl

    cpu_val, cpu_sub = create_card(metric_frame, "İŞLEMCİ (CPU)", "cpu", "cpu_sub")
    ram_val, ram_sub = create_card(metric_frame, "BELLEK (RAM)", "ram", "ram_sub")
    gpu_val, gpu_sub = create_card(metric_frame, "EKRAN KARTI (RTX 4060)", "gpu", "gpu_sub")
    pipe_val, pipe_sub = create_card(metric_frame, "BORU HATTI (FAZ 1-10)", "pipe", "pipe_sub")

    # Hızlı Linkler Çubuğu (Port 3000, 8000, 8085)
    link_bar = tk.Frame(root, bg="#1e293b", padx=15, pady=8)
    link_bar.pack(fill="x", padx=10, pady=4)

    tk.Label(link_bar, text="🌐 Servis Bağlantıları:", font=("Helvetica", 9, "bold"), fg="#cbd5e1", bg="#1e293b").pack(side="left", padx=5)

    def open_url(url):
        import webbrowser
        webbrowser.open(url)

    tk.Button(link_bar, text="🔗 Web Arayüzü (Port 3000)", bg="#065f46", fg="#ecfdf5", relief="flat", padx=8, pady=3, cursor="hand2", command=lambda: open_url("http://localhost:3000")).pack(side="left", padx=4)
    tk.Button(link_bar, text="🔗 Hibrit Arama & REST (Port 8000)", bg="#1e3a8a", fg="#eff6ff", relief="flat", padx=8, pady=3, cursor="hand2", command=lambda: open_url("http://localhost:8000")).pack(side="left", padx=4)
    tk.Button(link_bar, text="🔗 Canlı Kokpit & DiGraph (Port 8085)", bg="#581c87", fg="#faf5ff", relief="flat", padx=8, pady=3, cursor="hand2", command=lambda: open_url("http://localhost:8085")).pack(side="left", padx=4)

    # Orta Bölüm: Script Kontrol Tablosu
    table_frame = tk.Frame(root, bg="#1e293b", padx=10, pady=10)
    table_frame.pack(fill="both", expand=True, padx=10, pady=6)

    tk.Label(table_frame, text="📋 Yönetilen Scriptler, Görevleri ve Canlı Kontroller", font=("Helvetica", 11, "bold"), fg="#f8fafc", bg="#1e293b").pack(anchor="w", pady=(0, 6))

    # Canvas & Scrollbar for script cards
    canvas = tk.Canvas(table_frame, bg="#1e293b", highlightthickness=0)
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=canvas.yview)
    scroll_content = tk.Frame(canvas, bg="#1e293b")

    scroll_content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_content, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    script_rows = {}

    for k, meta in MANAGED_SCRIPTS.items():
        row_card = tk.Frame(scroll_content, bg="#0f172a", padx=10, pady=8, relief="solid", bd=1)
        row_card.pack(fill="x", expand=True, pady=3, padx=2)

        left_col = tk.Frame(row_card, bg="#0f172a")
        left_col.pack(side="left", fill="x", expand=True)

        name_lbl = tk.Label(left_col, text=meta["name"], font=("Helvetica", 10, "bold"), fg="#e2e8f0", bg="#0f172a")
        name_lbl.pack(anchor="w")

        desc_lbl = tk.Label(left_col, text=meta["desc"], font=("Helvetica", 8), fg="#94a3b8", bg="#0f172a")
        desc_lbl.pack(anchor="w")

        right_col = tk.Frame(row_card, bg="#0f172a")
        right_col.pack(side="right")

        status_lbl = tk.Label(right_col, text="Durduruldu", font=("Helvetica", 9, "bold"), fg="#ef4444", bg="#0f172a", width=12)
        status_lbl.pack(side="left", padx=5)

        uptime_lbl = tk.Label(right_col, text="-", font=("Helvetica", 8), fg="#64748b", bg="#0f172a", width=10)
        uptime_lbl.pack(side="left", padx=5)

        def make_toggle(s_key):
            return lambda: toggle_script(s_key)

        toggle_btn = tk.Button(right_col, text="Başlat", bg="#10b981", fg="white", relief="flat", padx=10, pady=2, cursor="hand2")
        toggle_btn.configure(command=make_toggle(k))
        toggle_btn.pack(side="left", padx=4)

        script_rows[k] = {
            "status_lbl": status_lbl,
            "uptime_lbl": uptime_lbl,
            "toggle_btn": toggle_btn
        }

    def toggle_script(s_key):
        if controller.is_script_running(s_key):
            controller.stop_script(s_key)
        else:
            controller.start_script(s_key)
        refresh_ui()

    # Otomatik Yenileme Döngüsü
    def refresh_ui():
        st = controller.get_all_status()
        telem = st["telemetry"]
        pipe = st["pipeline"]

        # Metrikleri güncelle
        cpu_val.config(text=f"%{telem['cpu_percent']}")
        cpu_sub.config(text=f"{telem['cpu_count']} Çekirdek Aktif")

        ram_val.config(text=f"{telem['ram_used_gb']} / {telem['ram_total_gb']} GB")
        ram_sub.config(text=f"%{telem['ram_percent']} Dolu")

        gpu_val.config(text=f"{telem['gpu_vram_used']} / {telem['gpu_vram_total']} MB")
        gpu_sub.config(text=f"{telem['gpu_name']} | Yük: %{telem['gpu_util']} | {telem['gpu_temp']}°C")

        pipe_val.config(text=f"%{pipe['percent']} ({pipe['completed_items']} Soru)")
        pipe_sub.config(text=f"{pipe['active_stage'][:30]}")

        # Script satırlarını güncelle
        scripts_data = st["scripts"]
        for k, widgets in script_rows.items():
            s_info = scripts_data.get(k, {})
            is_run = s_info.get("running", False)
            if is_run:
                widgets["status_lbl"].config(text="● Çalışıyor", fg="#10b981")
                widgets["uptime_lbl"].config(text=s_info.get("uptime_formatted", "-"), fg="#38bdf8")
                widgets["toggle_btn"].config(text="Durdur", bg="#ef4444")
            else:
                widgets["status_lbl"].config(text="○ Durduruldu", fg="#94a3b8")
                widgets["uptime_lbl"].config(text="-", fg="#64748b")
                widgets["toggle_btn"].config(text="Başlat", bg="#10b981")

        root.after(2000, refresh_ui)

    root.after(500, refresh_ui)

    def on_closing():
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


# ==============================================================================
# Ana Giriş Noktası
# ==============================================================================
def main():
    import argparse
    parser = argparse.ArgumentParser(description="MedSoru AI Master Supervisor")
    parser.add_argument("--mode", choices=["normal", "safe", "extreme"], help="Başlangıç çalışma modu")
    parser.add_argument("--gui", action="store_true", help="Masaüstü GUI penceresini aç")
    parser.add_argument("--cli", action="store_true", help="Terminal etkileşimli mod")
    parser.add_argument("--daemon", action="store_true", help="Arka plan / Konteyner orkestratör modu")
    args = parser.parse_args()

    controller = MasterController()

    # Mod belirleme
    if args.mode:
        selected_mode = args.mode
    elif not args.daemon and not os.environ.get("MEDS_DAEMON"):
        selected_mode = prompt_user_for_mode()
    else:
        selected_mode = controller.current_mode

    controller.set_mode(selected_mode)

    # Supervisor izleme thread'ini başlat
    supervisor_thread = threading.Thread(target=controller.supervisor_loop, daemon=True)
    supervisor_thread.start()

    print(f"\n[✓] MedSoru Master Supervisor Başlatıldı. Mod: {controller.current_mode.upper()}")
    print("    - Web Dashboard:     http://localhost:8085")
    print("    - MedSoru Web App:   http://localhost:3000")
    print("    - Hibrit REST Servis: http://localhost:8000\n")

    # Eğer GUI istenmişse veya ekran ortamı müsaitse Tkinter GUI aç
    if args.gui or (not args.daemon and os.environ.get("DISPLAY") and not args.cli):
        try:
            run_desktop_gui(controller)
        except Exception as e:
            print(f"[Master] GUI başlatılamadı ({e}), CLI modunda devam ediliyor...")
            while True:
                time.sleep(2)
    else:
        # Daemon / CLI bekleme döngüsü
        def sig_handler(sig, frame):
            print("\n[Master] Kapatılıyor, tüm alt süreçler güvenle sonlandırılıyor...")
            controller.running = False
            for k in list(controller.processes.keys()):
                controller.stop_script(k)
            sys.exit(0)

        signal.signal(signal.SIGINT, sig_handler)
        signal.signal(signal.SIGTERM, sig_handler)

        while controller.running:
            time.sleep(2)

if __name__ == "__main__":
    main()
