#!/bin/sh
# Hoca dökümü sınırlı GPU kipinde (AGENTS.md §10 altıncı istisna): systemd-run kaynak tavanı + CUDA kitaplıkları.
#   sh hoca_dokum_gpu.sh <ses> <çıktı.json>
set -e
# systemd-run çalışma dizini farklıdır: göreli yol ffmpeg'de "dosya yok" (254) verir → mutlak yola çevir (2026-11-05)
SES=$(realpath "$1"); CIK=$(realpath -m "$2"); shift 2  # kalan argümanlar (--model …) aktarılır; eskiden yutuluyordu (2026-11-06)
K=/home/indu/medsor/meds
# Saat kilidi kalkmışsa (H493: nvidia-clocks 3000'e açıyor) döküm CPU'ya düşer ve uydurma cümleli döküm çıkar →
# kullanıcının kilit servisini (300–1500 MHz) önce yeniden uygula; şifresiz sudo yoksa sessizce geç.
sudo -n systemctl restart nvidia-clock-lock.service 2>/dev/null || echo "uyarı: saat kilidi yeniden uygulanamadı" >&2
S=$K/.venv-hizala/lib/python3.14/site-packages/nvidia
exec systemd-run --user --wait --collect --quiet --pipe -p MemoryMax=4G -p CPUQuota=400% -p OOMScoreAdjust=500 \
  -E LD_LIBRARY_PATH=$S/cublas/lib:$S/cuda_nvrtc/lib:$S/cudnn/lib -E HD_THREADS=4 \
  $K/.venv-hizala/bin/python -I $K/scripts/ogrenci_drive/hoca_dokum.py "$SES" "$CIK" --gpu "$@"
