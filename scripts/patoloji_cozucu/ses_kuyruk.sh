#!/bin/bash
# Soru çözücü seslendirme kuyruğu: aynı anda tek EMA süreci (flock + çalışan süreci bekleme). Kullanım: ses_kuyruk.sh 05 06 07 08
cd /home/indu/medsor || exit 1
exec 9>/tmp/claude-1000/cozucu_ses.lock
flock 9
while pgrep -f "^/home/indu/.local/share/meds-ema/venv/bin/python meds/scripts/patoloji_cozucu/cozucu_ses.py" >/dev/null; do sleep 5; done
log="meds_temp/patoloji_ornek26/cozucu/log/ses_$(IFS=-; echo "$*").log"
systemd-run --user --scope -q -p CPUQuota=300% -p MemoryMax=2200M --nice=10 env CUDA_VISIBLE_DEVICES= EMA_IS_PARCACIGI=3 \
  /home/indu/.local/share/meds-ema/venv/bin/python meds/scripts/patoloji_cozucu/cozucu_ses.py "$@" > "$log" 2>&1
