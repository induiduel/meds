#!/usr/bin/env bash
# stop-supabase.bat'in Linux karşılığı.
set -e
source "$(dirname "${BASH_SOURCE[0]}")/linux/common.sh"
require_docker
cd "$ROOT_DIR/supabase-server"
$DOCKER compose down
