#!/bin/bash
# ==============================================================================
# MedSoru AI Container Entrypoint
# Docker konteyneri açıldığında hiçbir manuel komuta gerek kalmadan tüm servisleri,
# denetmenleri ve arka plan otonom yapay zeka ajanlarını sıralı olarak başlatır.
# ==============================================================================

set -e

echo "========================================================================"
echo "🚀 MedSoru Otonom AI Sistemi ve Docker Orkestrasyonu Başlatılıyor..."
echo "========================================================================"

export PYTHONUNBUFFERED=1

# Master Orchestrator (Kullanıcı Mod Seçimi & Süreç Yönetimi)
echo "[1/4] Master Supervisor & Süreç Yöneticisi başlatılıyor..."
python3 /app/scripts/master_controller.py &
PID_MASTER=$!
echo "✓ Master Supervisor PID: $PID_MASTER"

# 1. Dashboard Kokpit Sunucusu (Port 8085)
echo "[2/4] Canlı Telemetri ve Analiz Kokpiti (Port 8085) başlatılıyor..."
python3 /app/dashboard_server.py &
PID_DASH=$!
echo "✓ Kokpit PID: $PID_DASH"

# 2. Watchdog (Otonom Donanım, Süreç ve Hata Kurtarma Denetmeni)
echo "[3/4] Otonom Watchdog Denetmeni başlatılıyor..."
python3 /app/scripts/agents/watchdog.py &
PID_WATCHDOG=$!
echo "✓ Watchdog PID: $PID_WATCHDOG"

# 3. Pipeline Koşucusu (Aşama 1 -> 2 -> 3 -> 4 -> 5 Döngüsü)
echo "[4/4] Ana Boru Hattı Koşucusu (Pipeline Runner) başlatılıyor..."
python3 /app/scripts/agents/pipeline_runner.py &
PID_PIPELINE=$!
echo "✓ Pipeline Runner PID: $PID_PIPELINE"

# 4. Web Arayüzü ve API Sunucusu (Port 3000)
if [ -f "/app/server.ts" ]; then
    npx tsx /app/server.ts &
    PID_WEB=$!
    echo "✓ Web Sunucu PID: $PID_WEB"
fi

echo "========================================================================"
echo "✨ Tüm MedSoru AI servisleri ve denetmenleri arka planda başarıyla aktif!"
echo "   - Kokpit:     http://localhost:8085"
echo "   - Web Uygulama: http://localhost:3000"
echo "   - Hibrit REST: http://localhost:8000"
echo "   - Master Süreç Kontrol: GUI & Web Dashboard Aktif"
echo "========================================================================"

# Sinyal Yakalama ve Temiz Kapatma
trap "echo 'Kapatılıyor...'; kill $PID_MASTER $PID_DASH $PID_WATCHDOG $PID_PIPELINE $PID_WEB 2>/dev/null; exit 0" SIGINT SIGTERM

# Konteynerin canlı kalmasını sağla
wait
