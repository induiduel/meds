#!/usr/bin/env python3
"""Sürekli çalışan orkestratör: stage2 -> stage3 -> stage4, hata toleranslı."""
import json, subprocess, sys, time, os
from pathlib import Path
import lib

HERE = Path(__file__).parent
PY = sys.executable
log = lib.get_logger("runner")
STATUS = Path(lib.STATE_DIR) / "status.json"
IDLE = int(os.environ.get("MEDS_IDLE_SEC", "90"))
LOCK_FILE = Path(lib.STATE_DIR) / "pipeline_runner.lock"

def acquire_lock():
    import fcntl
    LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        f = open(LOCK_FILE, "w")
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return f
    except (IOError, BlockingIOError):
        log.warning("Başka bir pipeline_runner süreci zaten çalışıyor. Çıkılıyor.")
        sys.exit(0)


def ollama_up():
    try:
        import requests
        requests.get(os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434") + "/api/tags", timeout=10).raise_for_status()
        return True
    except Exception as e:
        log.warning("Ollama API geçici olarak yanıt vermedi (%s), bekleniyor...", e)
        time.sleep(3)
        return False


def run(stage, args=None):
    t = time.time()
    env = dict(os.environ)
    jemalloc_path = Path("/usr/lib/x86_64-linux-gnu/libjemalloc.so.2")
    if jemalloc_path.exists():
        env["LD_PRELOAD"] = str(jemalloc_path)
    r = subprocess.run([PY, str(HERE / stage), *(args or [])], capture_output=True, text=True, cwd=HERE, env=env)
    return {"stage": stage, "rc": r.returncode, "sec": round(time.time() - t),
            "tail": (r.stdout + r.stderr)[-400:]}


def main():
    delay = IDLE
    while True:
        res = []
        try:
            ollama_up()
            stages = [
                ("stage2_clean.py", "Aşama 2 (Faz 2): Türkçe Onarım & Soru Ayrıştırma"),
                ("stage3_merge.py", "Aşama 3 (Faz 3): RAG Eşleştirme & Zenginleştirme"),
                ("stage4_database.py", "Aşama 4 (Faz 4): Doğrulanmış Veritabanı Aktarımı"),
                ("../advanced_ai/orchestrator.py", "Aşama 5: GraphRAG & Hibrit Arama & MemGPT"),
                # Faz 5 → 6 → 6.5 → 7 → 7.5 → 8 → Aşama 1 yenileme artık ayrı orkestratörde (scripts/agents/phase_cycle.py,
                # meds-phases servisi): sırayla, zaman aşımlı, GPU soğuması beklenerek. Burada çalıştırılınca bir fazın
                # takılması yeni dosyaların aşama 2-4'ten geçmesini saatlerce durduruyordu.
            ]
            state = lib.State()
            for s_idx, stage_info in enumerate(stages, 1):
                s, s_desc, *stage_args = stage_info
                state.set_progress("pipeline", s_idx, len(stages), f"{s_desc} (Çalışıyor...)")
                out = run(s, stage_args[0] if stage_args else [])
                res.append(out)
                log.error(f"{s} rc={out['rc']}: {out['tail']}") if out["rc"] else None

                # Aşama geçişlerinde RAM ve VRAM önbelleğini tazele
                try:
                    import requests, gc
                    requests.post("http://127.0.0.1:11434/api/generate", json={"model": "gemma3:4b", "keep_alive": 0}, timeout=2)
                    requests.post("http://127.0.0.1:11434/api/generate", json={"model": "bge-m3:latest", "keep_alive": 0}, timeout=2)
                    gc.collect()
                except Exception:
                    pass
                if out["rc"]:
                    break
            # Eğer hata rc=-9 (dışarıdan kod tazeleme) ise hemen 2 saniyede başla
            had_kill = any(o.get("rc") == -9 for o in res)
            delay = 2 if had_kill else (IDLE if not any(o["rc"] for o in res) else min(delay * 2, 300))
        except Exception as e:
            delay = min(delay * 2, 300)
            res.append({"error": str(e)})
        STATUS.parent.mkdir(parents=True, exist_ok=True)
        STATUS.write_text(json.dumps({"time": time.strftime("%F %T"), "runs": res}, ensure_ascii=False, indent=1))
        lib.State().set_progress("pipeline", len(stages), len(stages), f"Döngü Tamamlandı ✓ (Yeni dosyalar için {delay} sn bekleniyor...)")
        time.sleep(delay)


if __name__ == "__main__":
    _lock = acquire_lock()
    main()
