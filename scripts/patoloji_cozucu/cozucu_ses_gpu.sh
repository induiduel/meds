#!/bin/bash
# EMA çözücü seslendirmesi GPU'da (kullanıcı istisnası 2026-10-18; AGENTS.md kural 10): yalnız meds-gpuguard etkin ve
# saat kilidi (sudo nvidia-smi -lgc 300,1500) varken. CUDA'lı torch XTTS venv'inden, ema_lightning EMA venv'inden (sona eklenir).
# Kullanım: cozucu_ses_gpu.sh <betik.py> [arg…]   (ör. meds/scripts/patoloji_cozucu/cozucu_ses.py 31 32)
cd /home/indu/medsor || exit 1
# Kullanıcı kararı 2026-10-24: EMA sesleri DAİMA GPU'da (çözücü, asistan, Öğren adımları; ders zinciri ve kuyruklar bu
# başlatıcıyı kullanır). Koruyucu kapalıysa açılır; açılamazsa CPU'ya düşülmez, çıkış 75 (geçici: sonraki turda yeniden).
systemctl --user is-active --quiet meds-gpuguard || systemctl --user start meds-gpuguard 2>/dev/null
sleep 2
systemctl --user is-active --quiet meds-gpuguard || { echo "meds-gpuguard çalışmıyor — GPU yok, ses üretilmedi (CPU'ya düşülmez)"; exit 75; }
SP=$(ls -d /home/indu/.local/share/meds-ema/venv/lib/python3*/site-packages)
betik="$1"; shift
exec systemd-run --user --scope -q -p CPUQuota=200% -p MemoryMax=3000M --nice=10 env EMA_CIHAZ=cuda EMA_IS_PARCACIGI=2 MEDS_EK_SITE="$SP" \
  /home/indu/.local/share/meds-xtts/venv/bin/python -c "import sys,runpy; sys.path.append('$SP'); sys.argv=sys.argv[1:]; runpy.run_path(sys.argv[0], run_name='__main__')" "$betik" "$@"
