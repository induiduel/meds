#!/usr/bin/env bash
# apply-migrations-to-local.bat'in Linux karşılığı.
# supabase/migrations altındaki tüm .sql dosyalarını sırayla yükler.
set -e
source "$(dirname "${BASH_SOURCE[0]}")/linux/common.sh"
require_docker

if ! $DOCKER ps --format '{{.Names}}' | grep -q '^supabase-db$'; then
  echo "[HATA] supabase-db konteyneri çalışmıyor. Önce ./start-supabase.sh çalıştırın." >&2
  exit 1
fi

for f in "$ROOT_DIR"/supabase/migrations/*.sql; do
  echo ">> $(basename "$f")"
  $DOCKER exec -i supabase-db psql -v ON_ERROR_STOP=0 -U postgres -d postgres < "$f"
done
echo "Tüm migration'lar yüklendi."
