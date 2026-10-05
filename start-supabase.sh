#!/usr/bin/env bash
# start-supabase.bat'in Linux karşılığı: yerel Supabase'i (docker compose) başlatır.
# İlk çalıştırmada supabase-server/.env ve local-supabase-keys.json otomatik üretilir.
set -e
source "$(dirname "${BASH_SOURCE[0]}")/linux/common.sh"

echo "== MEDS - Yerel Supabase başlatılıyor =="
require_docker

cd "$ROOT_DIR/supabase-server"
if [ ! -f .env ]; then
  echo "[1/3] İlk kurulum: gizli anahtarlar üretiliyor..."
  node setup-local-env.mjs
else
  echo "[1/3] supabase-server/.env zaten var."
fi

echo "[2/3] Servisler ayağa kaldırılıyor (docker compose up -d)..."
$DOCKER compose up -d

echo "[3/3] Hazır!"
echo "- Supabase Studio / API: http://localhost:8000"
echo "- PostgreSQL:            localhost:5432"
echo "- Anahtarlar:            supabase-server/local-supabase-keys.json"
echo
echo "Sonraki adımlar:"
echo "  ./apply-migrations-to-local.sh     # şemayı yükle"
echo "  node scripts/switch-env-to-local.mjs  # .env'yi yerel Supabase'e yönlendir"
