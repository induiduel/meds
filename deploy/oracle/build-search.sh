#!/usr/bin/env bash
# build-search.sh — sorgu zekâsı paketi + hastalık grafiğini AYRI konteynerde derler (Oracle host'unda çalışır).
# Neden: derleyici ~1,2 GB tepe yapar; meds-app 3 GB tavanında 1,5+ GB kullanır → aynı konteynerde OOM riski.
# Çıktı bind-mount edilen data/ klasörüne yazılır (data/search, data/knowledge); meds-app dosya değişince
# kendiliğinden yeniden yükler (30 sn içinde). İmza aynıysa ~1 sn'de çıkar → cron ile güvenle çağrılabilir.
# Kullanım (Oracle'da, meds/ içinde): ./deploy/oracle/build-search.sh [--force]
# Zamanlama: ./deploy/oracle/build-search.sh --cron-kur → systemd zamanlayıcısı 12:00/16:00/22:00 (TR) kurar (tekrar çalıştırmak güvenli;
# ders-işçi 01-08 penceresi dışında). Ayrıca deploy-code.sh --build her dağıtımın sonunda arka planda çağırır.
set -euo pipefail
APP_DIR="${MEDS_APP_DIR:-/home/ubuntu/medsor/meds}"
if [[ "${1:-}" == "--cron-kur" ]]; then
  # Oracle UTC: UTC 09/13/19 = TR 12/16/22 (ders-işçi penceresi 01-08 TR ya da UTC olsun, çakışmaz).
  # Host'ta crontab yok → systemd zamanlayıcısı (meds-arama-paketi.timer); tekrar çalıştırmak güvenli.
  mkdir -p "$APP_DIR/deploy/oracle/logs"
  sudo tee /etc/systemd/system/meds-arama-paketi.service >/dev/null <<UNIT
[Unit]
Description=MedSoru arama paketi + hastalık grafiği (ayrı konteyner, imza aynıysa ~1 sn)
After=docker.service
[Service]
Type=oneshot
User=$(id -un)
WorkingDirectory=$APP_DIR
ExecStart=/bin/sh -c '$APP_DIR/deploy/oracle/build-search.sh >> $APP_DIR/deploy/oracle/logs/build-search.log 2>&1'
Nice=15
UNIT
  sudo tee /etc/systemd/system/meds-arama-paketi.timer >/dev/null <<UNIT
[Unit]
Description=MedSoru arama paketi zamanlaması (UTC 09/13/19)
[Timer]
OnCalendar=*-*-* 09,13,19:00:00 UTC
Persistent=true
[Install]
WantedBy=timers.target
UNIT
  sudo systemctl daemon-reload
  sudo systemctl enable --now meds-arama-paketi.timer
  systemctl list-timers meds-arama-paketi.timer --no-pager | head -3
  exit 0
fi
V2_DIR="${MEDS_V2_DIR:-/home/ubuntu/medsor/meds_database_v2}"
IMAGE="${MEDS_IMAGE:-medsoru-server:oracle}"
exec flock -n /tmp/meds-search-build.lock docker run --rm --name meds-search-build \
  --memory 2g --cpus 1 \
  -e CUDA_VISIBLE_DEVICES= -e MEDS_DATABASE_V2_DIR=/v2 \
  -v "$APP_DIR/data:/app/data" -v "$V2_DIR:/v2:ro" \
  "$IMAGE" nice -n 15 node --max-old-space-size=1800 node_modules/.bin/tsx scripts/search/build-query-intel.mts "$@"
