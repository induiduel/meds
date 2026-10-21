#!/bin/bash
# Şık açıklaması uygulama + seslendirme: çözücü sesleriyle ortak kilit, CPU tavanlı.
cd /home/indu/medsor || exit 1
exec 9>/tmp/claude-1000/cozucu_ses.lock
flock 9
systemd-run --user --scope -q -p CPUQuota=300% -p MemoryMax=2200M --nice=10 env CUDA_VISIBLE_DEVICES= EMA_IS_PARCACIGI=3 \
  /home/indu/.local/share/meds-ema/venv/bin/python meds/scripts/cikmis_paket/sik_uygula.py "$@" > meds_temp/cikmis_paket/sik_uygula.log 2>&1
