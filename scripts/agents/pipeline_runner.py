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


def ollama_up():
    try:
        import requests
        requests.get(os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434") + "/api/tags", timeout=5).raise_for_status()
        return True
    except Exception:
        log.warning("Ollama veya GPU yanıt vermiyor, otomatik GPU & ses uyandırma çalıştırılıyor...")
        subprocess.run(["/usr/local/bin/meds-gpu-recovery"], capture_output=True)
        subprocess.run(["sudo", "-n", "docker", "restart", "meds-ollama"], capture_output=True)
        time.sleep(10)
        return False


def run(stage):
    t = time.time()
    r = subprocess.run([PY, str(HERE / stage)], capture_output=True, text=True, cwd=HERE)
    return {"stage": stage, "rc": r.returncode, "sec": round(time.time() - t),
            "tail": (r.stdout + r.stderr)[-400:]}


def main():
    delay = IDLE
    while True:
        res = []
        try:
            ollama_up()
            for s in ("stage2_clean.py", "stage3_merge.py", "stage4_database.py", "../advanced_ai/orchestrator.py"):
                out = run(s)
                res.append(out)
                log.error(f"{s} rc={out['rc']}: {out['tail']}") if out["rc"] else None
                if out["rc"]:
                    break
            delay = IDLE if not any(o["rc"] for o in res) else min(delay * 2, 1800)
        except Exception as e:
            delay = min(delay * 2, 1800)
            res.append({"error": str(e)})
        STATUS.parent.mkdir(parents=True, exist_ok=True)
        STATUS.write_text(json.dumps({"time": time.strftime("%F %T"), "runs": res}, ensure_ascii=False, indent=1))
        time.sleep(delay)


if __name__ == "__main__":
    main()
