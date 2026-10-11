#!/usr/bin/env bash
# build-search.sh — sorgu zekâsı paketi + hastalık grafiğini AYRI konteynerde derler (Oracle host'unda çalışır).
# Neden: derleyici ~1,2 GB tepe yapar; meds-app 3 GB tavanında 1,5+ GB kullanır → aynı konteynerde OOM riski.
# Çıktı bind-mount edilen data/ klasörüne yazılır (data/search, data/knowledge); meds-app dosya değişince
# kendiliğinden yeniden yükler (30 sn içinde). İmza aynıysa ~1 sn'de çıkar → cron ile güvenle çağrılabilir.
# Kullanım (Oracle'da, meds/ içinde): ./deploy/oracle/build-search.sh [--force]
set -euo pipefail
APP_DIR="${MEDS_APP_DIR:-/home/ubuntu/medsor/meds}"
V2_DIR="${MEDS_V2_DIR:-/home/ubuntu/medsor/meds_database_v2}"
IMAGE="${MEDS_IMAGE:-medsoru-server:oracle}"
exec flock -n /tmp/meds-search-build.lock docker run --rm --name meds-search-build \
  --memory 2g --cpus 1 \
  -e CUDA_VISIBLE_DEVICES= -e MEDS_DATABASE_V2_DIR=/v2 \
  -v "$APP_DIR/data:/app/data" -v "$V2_DIR:/v2:ro" \
  "$IMAGE" nice -n 15 node --max-old-space-size=1800 node_modules/.bin/tsx scripts/search/build-query-intel.mts "$@"
