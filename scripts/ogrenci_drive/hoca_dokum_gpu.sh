#!/bin/sh
# Hoca dökümü sınırlı GPU kipinde (AGENTS.md §10 altıncı istisna): systemd-run kaynak tavanı + CUDA kitaplıkları.
#   sh hoca_dokum_gpu.sh <ses> <çıktı.json>
set -e
K=/home/indu/medsor/meds
S=$K/.venv-hizala/lib/python3.14/site-packages/nvidia
exec systemd-run --user --wait --collect --quiet --pipe -p MemoryMax=4G -p CPUQuota=400% -p OOMScoreAdjust=500 \
  -E LD_LIBRARY_PATH=$S/cublas/lib:$S/cuda_nvrtc/lib:$S/cudnn/lib -E HD_THREADS=4 \
  $K/.venv-hizala/bin/python -I $K/scripts/ogrenci_drive/hoca_dokum.py "$1" "$2" --gpu
