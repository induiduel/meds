#!/usr/bin/env python3
"""Gece çalışması: ağır fazları tek GPU kuyruğunda sırayla yürütür."""
import fcntl, json, os, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT.parent / 'meds_temp' / 'state'
LOG_DIR = ROOT.parent / 'meds_temp' / 'logs'
LOCK_PATH = STATE_DIR / 'overnight_pipeline.lock'
STATUS_PATH = STATE_DIR / 'overnight_pipeline.json'
PYTHON = ROOT / '.venv-ocr' / 'bin' / 'python'
if not PYTHON.exists(): PYTHON = Path(sys.executable)

STAGES = [
    ('phase5', ROOT / 'scripts/advanced_ai/multi_ai_consensus_phase5.py', []),
    ('phase6', ROOT / 'scripts/advanced_ai/deep_metadata_generator_phase6.py', ['--once']),
    ('phase6_5', ROOT / 'scripts/advanced_ai/thesaurus_anchor_phase6_5.py', []),
    ('phase7', ROOT / 'scripts/advanced_ai/microagent_storyteller_phase7.py', []),
    ('phase7_5', ROOT / 'scripts/advanced_ai/reconstruct_slides_phase7_5.py', []),
]

def write_status(stage, state, detail=''):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATUS_PATH.write_text(json.dumps({'stage': stage, 'state': state, 'detail': detail, 'updated_at': time.strftime('%Y-%m-%dT%H:%M:%S%z')}, ensure_ascii=False, indent=2))

def main():
    STATE_DIR.mkdir(parents=True, exist_ok=True); LOG_DIR.mkdir(parents=True, exist_ok=True)
    lock = LOCK_PATH.open('w')
    try: fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError: return
    for name, script, args in STAGES:
        if not script.exists():
            write_status(name, 'blocked', f'Bulunamadı: {script}'); return
        log_path = LOG_DIR / f'overnight_{name}.log'
        write_status(name, 'running')
        with log_path.open('a', encoding='utf-8') as log:
            log.write(f'\n=== {time.ctime()} BAŞLADI ===\n'); log.flush()
            result = subprocess.run([str(PYTHON), str(script), *args], cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, env=os.environ.copy())
        if result.returncode != 0:
            write_status(name, 'failed', f'Çıkış kodu: {result.returncode}'); return
        write_status(name, 'completed')
    write_status('all', 'completed', 'Gece faz kuyruğu tamamlandı.')

if __name__ == '__main__': main()
