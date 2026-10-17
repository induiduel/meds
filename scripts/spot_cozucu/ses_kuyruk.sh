#!/bin/bash
# Soru çözücü seslendirme kuyruğu (branş geneli): aynı anda tek EMA süreci (patoloji çözücüsüyle ortak kilit).
# Kullanım: ses_kuyruk.sh <brans> [--ses ema] [kod ...]
cd /home/indu/medsor || exit 1
brans="$1"; shift
mkdir -p /tmp/claude-1000 "meds_temp/spot_cozucu/$brans/log"
exec 9>/tmp/claude-1000/cozucu_ses.lock
flock 9
while pgrep -f "^/home/indu/.local/share/meds-ema/venv/bin/python meds/scripts/(patoloji_cozucu/cozucu_ses|spot_cozucu/ses).py" >/dev/null; do sleep 5; done
log="meds_temp/spot_cozucu/$brans/log/ses_$(date +%m%d-%H%M%S).log"
systemd-run --user --scope -q -p CPUQuota=300% -p MemoryMax=2200M --nice=10 env CUDA_VISIBLE_DEVICES= EMA_IS_PARCACIGI=3 \
  /home/indu/.local/share/meds-ema/venv/bin/python meds/scripts/spot_cozucu/ses.py --brans "$brans" "$@" > "$log" 2>&1
