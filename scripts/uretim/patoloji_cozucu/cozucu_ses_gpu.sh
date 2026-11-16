#!/bin/bash
# EMA çözücü seslendirmesi GPU'da (kullanıcı istisnası 2026-10-18; AGENTS.md kural 10): yalnız meds-gpuguard etkin ve
# saat kilidi (sudo nvidia-smi -lgc 300,1500) varken. CUDA'lı torch XTTS venv'inden, ema_lightning EMA venv'inden (sona eklenir).
# Kullanım: cozucu_ses_gpu.sh <betik.py> [arg…]   (ör. meds/scripts/uretim/patoloji_cozucu/cozucu_ses.py 31 32)
# Kilit (2026-11-16): aynı anda TEK GPU EMA ses işi. Kuyruk betikleriyle (patoloji_cozucu/ses_kuyruk.sh,
# spot_cozucu/ses_kuyruk.sh, asistan_ses_kuyruk.sh) AYNI kilit dosyası /tmp/claude-1000/cozucu_ses.lock → birbirini dışlar.
# Davranış değişikliği: ikinci çağrı artık kilidi BEKLER (önceden iki oturum GPU'ya aynı anda girebiliyordu);
# MEDS_SES_KILIT_BEKLE=0 verilirse beklemez, açık mesajla çıkış 75. Kilidi zaten tutan kuyruk betiğinden çağrıda (fd 9 aynı
# dosyaya açık) yeniden kilitlenmez (yoksa kendini kilitlerdi). Kilit exec ile sürece devredilir, iş bitince bırakılır.
# İstisna: sürekli bekleyen işçi kipi (`… ema_isci.py bekle`, meds-ema.service drop-in'i bu başlatıcıyı kullanıyor) kilit
# ALMAZ — alsaydı kilidi süresiz tutup bütün kuyrukları kilitlerdi; onunla çakışma H532 yordamıyla (birimi durdur) önlenir.
cd /home/indu/medsor || exit 1
KILIT=/tmp/claude-1000/cozucu_ses.lock
mkdir -p /tmp/claude-1000
if [ "${@: -1}" != "bekle" ] && [ "$(readlink /proc/$$/fd/9 2>/dev/null)" != "$KILIT" ]; then
  exec 9>"$KILIT"
  if [ "${MEDS_SES_KILIT_BEKLE:-1}" = "0" ]; then
    flock -n 9 || { echo "başka bir EMA ses işi kilidi tutuyor ($KILIT) — çıkılıyor (MEDS_SES_KILIT_BEKLE=0)"; exit 75; }
  elif ! flock -n 9; then
    echo "başka bir EMA ses işi sürüyor ($KILIT) — bitmesi bekleniyor…"
    flock 9
  fi
fi
# Kullanıcı kararı 2026-10-24: EMA sesleri DAİMA GPU'da (çözücü, asistan, Öğren adımları; ders zinciri ve kuyruklar bu
# başlatıcıyı kullanır). Koruyucu kapalıysa açılır; açılamazsa CPU'ya düşülmez, çıkış 75 (geçici: sonraki turda yeniden).
systemctl --user is-active --quiet meds-gpuguard || systemctl --user start meds-gpuguard 2>/dev/null
sleep 2
systemctl --user is-active --quiet meds-gpuguard || { echo "meds-gpuguard çalışmıyor — GPU yok, ses üretilmedi (CPU'ya düşülmez)"; exit 75; }
SP=$(ls -d /home/indu/.local/share/meds-ema/venv/lib/python3*/site-packages)
betik="$1"; shift
exec systemd-run --user --scope -q -p CPUQuota=200% -p MemoryMax=3000M --nice=10 env EMA_CIHAZ=cuda EMA_IS_PARCACIGI=2 MEDS_EK_SITE="$SP" \
  /home/indu/.local/share/meds-xtts/venv/bin/python -c "import sys,runpy; sys.path.append('$SP'); sys.argv=sys.argv[1:]; runpy.run_path(sys.argv[0], run_name='__main__')" "$betik" "$@"
