#!/bin/bash
# Kısa not seslendirmesi: çözücü sesleriyle ortak kilit (aynı anda tek EMA süreci), CPU tavanlı.
cd /home/indu/medsor || exit 1
mkdir -p /tmp/claude-1000 meds_temp/cikmis_paket
exec 9>/tmp/claude-1000/cozucu_ses.lock
flock 9
systemd-run --user --scope -q -p CPUQuota=300% -p MemoryMax=2200M --nice=10 env CUDA_VISIBLE_DEVICES= EMA_IS_PARCACIGI=3 \
  /home/indu/.local/share/meds-ema/venv/bin/python meds/scripts/cikmis_paket/not_ses.py > meds_temp/cikmis_paket/not_ses.log 2>&1
