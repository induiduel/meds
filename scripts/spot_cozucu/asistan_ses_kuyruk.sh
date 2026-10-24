#!/bin/bash
# Sesli sınav asistanı seslendirme kuyruğu (branş geneli): çözücülerle ortak kilit, aynı anda tek EMA süreci.
# Kullanım: asistan_ses_kuyruk.sh <brans> [kod ...]
cd /home/indu/medsor || exit 1
brans="$1"; shift
mkdir -p /tmp/claude-1000 "meds_temp/spot_cozucu/$brans/log"
exec 9>/tmp/claude-1000/cozucu_ses.lock
flock 9
while pgrep -f "python.* meds/scripts/(patoloji_cozucu/cozucu_ses|spot_cozucu/ses|spot_cozucu/asistan_ses).py" >/dev/null; do sleep 5; done
log="meds_temp/spot_cozucu/$brans/log/asistan_ses_$(date +%m%d-%H%M%S).log"
# EMA daima GPU (2026-10-24): XTTS venv CUDA torch + EMA site-packages, koruyucu/ısı protokolü (cozucu_ses_gpu.sh)
bash meds/scripts/patoloji_cozucu/cozucu_ses_gpu.sh meds/scripts/spot_cozucu/asistan_ses.py --brans "$brans" "$@" > "$log" 2>&1
