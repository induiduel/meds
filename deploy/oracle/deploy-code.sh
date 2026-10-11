#!/usr/bin/env bash
# deploy-code.sh — cihaz working tree'yi Oracle'a gönderir + doğrular (rsync yolu).
# Neden git değil: data/*.json git'te 350MB+, commitlenmemiş değişiklikler var;
# rsync çalışan ağacı birebir taşır. GitHub yedek/ortak çalışma için durur.
# Kullanım (cihazdan, meds/ içinde): ./deploy/oracle/deploy-code.sh [--build]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MEDS_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
KEY="${SSH_KEY:-/home/indu/medsor/ssh-key1.key}"
ORACLE_USER="${ORACLE_USER:-ubuntu}"
ORACLE_HOST="${ORACLE_HOST:?ORACLE_HOST tanımlı değil (export ORACLE_HOST=92.5.55.109)}"
ORACLE_DIR="/home/ubuntu/medsor/meds"
DO_BUILD=0
[[ "${1:-}" == "--build" ]] && DO_BUILD=1
SSH="ssh -i $KEY -o StrictHostKeyChecking=no"

echo "==> [1/4] rsync kod (src/data DAHİL, .env HARİÇ)"
rsync -avz --checksum \
  --exclude='/node_modules' --exclude='/dist' --exclude='/dist-gh' \
  --exclude='/data' --exclude='/.git' --exclude='/models' \
  --exclude='/training_data' --exclude='/linux' \
  --exclude='.venv*' --exclude='__pycache__' --exclude='*.log' \
  --exclude='/supabase-server/volumes' --exclude='/supabase-server/backups' \
  --exclude='/cloudflared.exe' --exclude='src/data/decks/items' \
  --exclude='/.env' \
  -e "$SSH" "$MEDS_DIR/" "$ORACLE_USER@$ORACLE_HOST:$ORACLE_DIR/" 2>&1 | tail -2

echo "==> [2/4] bütünlük: kritik dosya md5 karşılaştırma"
for f in deploy/oracle/docker-compose.oracle.yml deploy/oracle/Dockerfile.oracle server.ts package.json; do
  a=$(md5sum "$MEDS_DIR/$f" | cut -d' ' -f1)
  b=$($SSH "$ORACLE_USER@$ORACLE_HOST" "md5sum $ORACLE_DIR/$f" | cut -d' ' -f1)
  if [[ "$a" == "$b" ]]; then echo "  OK $f"; else echo "  HATA $f uyuşmuyor!"; exit 1; fi
done

if [[ "$DO_BUILD" == "1" ]]; then
  echo "==> [3/4] Oracle'da derle + başlat"
  $SSH "$ORACLE_USER@$ORACLE_HOST" "cd $ORACLE_DIR && flock /tmp/meds-deploy.lock docker compose --env-file $ORACLE_DIR/.env -f deploy/oracle/docker-compose.oracle.yml up -d --build meds-server 2>&1 | tail -2"
  sleep 25
fi

echo "==> [4/4] sağlık kontrolü"
$SSH "$ORACLE_USER@$ORACLE_HOST" "curl -sf http://127.0.0.1:3000/api/health" | head -c 200
echo
echo "BİTTİ."
