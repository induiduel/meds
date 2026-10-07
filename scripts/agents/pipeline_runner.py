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


STAGE_LOCK = Path(os.environ.get("MEDS_TEMP_DIR") or Path(__file__).resolve().parents[3] / "meds_temp") / "state" / "asama_kilidi.lock"


def run(stage, args=None):
    """Aşama betiğini çalıştır; yeni veri hattıyla aynı anda aynı aşama işlenmesin diye ortak kilit."""
    import fcntl
    STAGE_LOCK.parent.mkdir(parents=True, exist_ok=True)
    with open(STAGE_LOCK, "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        return _run(stage, args)


def _run(stage, args=None):
    t = time.time()
    env = dict(os.environ)
    jemalloc_path = Path("/usr/lib/x86_64-linux-gnu/libjemalloc.so.2")
    if jemalloc_path.exists():
        env["LD_PRELOAD"] = str(jemalloc_path)
    r = subprocess.run([PY, str(HERE / stage), *(args or [])], capture_output=True, text=True, cwd=HERE, env=env)
    return {"stage": stage, "rc": r.returncode, "sec": round(time.time() - t),
            "tail": (r.stdout + r.stderr)[-400:]}


AUTO_NEXT = os.environ.get("MEDS_PIPELINE_AUTO_NEXT") == "1"
RUN_NEXT_ONCE = "--sonraki" in sys.argv


def main():
    delay = IDLE
    while True:
        res = []
        try:
            stages = [
                ("stage2_clean.py", "Aşama 2 (Faz 2): Türkçe Onarım & Soru Ayrıştırma"),
                ("stage3_merge.py", "Aşama 3 (Faz 3): RAG Eşleştirme & Zenginleştirme"),
                ("stage4_database.py", "Aşama 4 (Faz 4): Doğrulanmış Veritabanı Aktarımı"),
                ("../advanced_ai/orchestrator.py", "Aşama 5: GraphRAG & Hibrit Arama & MemGPT"),
                # Faz 5 → 6 → 6.5 → 7 → 7.5 → 8 → Aşama 1 yenileme artık ayrı orkestratörde (scripts/agents/phase_cycle.py,
                # meds-phases servisi): sırayla, zaman aşımlı, GPU soğuması beklenerek. Burada çalıştırılınca bir fazın
                # takılması yeni dosyaların aşama 2-4'ten geçmesini saatlerce durduruyordu.
            ]
            # Otomatik ilerleme yalnız Aşama 2'ye kadar (yerel: Tesseract + kural tabanlı ayrıştırma). Aşama 3 ve sonrası
            # (bulut/LLM içerir) kendiliğinden başlamaz: tek sefer için "pipeline_runner.py --sonraki", kalıcı için
            # .env MEDS_PIPELINE_AUTO_NEXT=1.
            if not (AUTO_NEXT or RUN_NEXT_ONCE):
                stages = stages[:1]
            state = lib.State()
            for s_idx, stage_info in enumerate(stages, 1):
                s, s_desc, *stage_args = stage_info
                state.set_progress("pipeline", s_idx, len(stages), f"{s_desc} (Çalışıyor...)")
                out = run(s, stage_args[0] if stage_args else [])
                res.append(out)
                log.error(f"{s} rc={out['rc']}: {out['tail']}") if out["rc"] else None

                import gc
                gc.collect()
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
        if RUN_NEXT_ONCE:
            return
        time.sleep(delay)


if __name__ == "__main__":
    _lock = acquire_lock()
    main()
