#!/bin/bash
# Ek modül seslendirmesi GPU'da (EMA istisnası, AGENTS.md kural 10): yalnız meds-gpuguard etkin + saat kilidi varken.
cd /home/indu/medsor || exit 1
exec 9>/tmp/claude-1000/cozucu_ses.lock
flock 9
bash meds/scripts/patoloji_cozucu/cozucu_ses_gpu.sh meds/scripts/cikmis_paket/ek_uygula.py "$@" > meds_temp/cikmis_paket/ek_uygula_gpu.log 2>&1
