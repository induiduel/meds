#!/usr/bin/env bash
# sync-data.sh — meds/data/*.json çift yönlü eşitleme (cihaz <-> Oracle).
# Supabase auth/realtime tabloları bu scriptin dışındadır (doğrudan Supabase'e yazar).
# Kullanım (CİHAZDAN):
#   ./sync-data.sh --to-oracle [--dry-run]    # cihaz -> Oracle
#   ./sync-data.sh --from-oracle [--dry-run]  # Oracle -> cihaz
set -euo pipefail

MODE=""
DRY_RUN=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --to-oracle) MODE="to" ;;
    --from-oracle) MODE="from" ;;
    --dry-run) DRY_RUN="--dry-run" ;;
    *) echo "Bilinmeyen argüman: $1"; exit 1 ;;
  esac
  shift
done

if [[ -z "$MODE" ]]; then
  echo "Kullanım: $0 --to-oracle|--from-oracle [--dry-run]"
  exit 1
fi

ORACLE_USER="${ORACLE_USER:-ubuntu}"
ORACLE_HOST="${ORACLE_HOST:?ORACLE_HOST tanımlı değil (örn: export ORACLE_HOST=150.136.x.x)}"
ORACLE_SSH_KEY="${ORACLE_SSH_KEY:-$HOME/.ssh/id_ed25519}"
ORACLE_REPO="${ORACLE_REPO:-~/meds}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOCAL_DATA="$SCRIPT_DIR/../../data/"
REMOTE_DATA="$ORACLE_REPO/meds/data/"
BACKUP_BASE="$HOME/meds-data-backup/$(date +%Y%m%d_%H%M%S)"

SSH="ssh -i $ORACLE_SSH_KEY -o StrictHostKeyChecking=accept-new"

echo "==> Yedek alınıyor: $BACKUP_BASE"
mkdir -p "$BACKUP_BASE"
if [[ "$MODE" == "to" ]]; then
  cp -a "$LOCAL_DATA" "$BACKUP_BASE/local-data-before-push" 2>/dev/null || true
else
  cp -a "$LOCAL_DATA" "$BACKUP_BASE/local-data-before-pull" 2>/dev/null || true
fi

EXCLUDES=(
  --exclude='node_modules'
  --exclude='dist'
  --exclude='*.log'
  --exclude='*.legacy_backup.json'
  --exclude='active_tunnel.txt'
)

if [[ "$MODE" == "to" ]]; then
  # data/lectureSummariesCatalog.json Oracle'daki ders işçisi yayınlarını da içerir: önce yerel kaynaklara işle
  PY="$SCRIPT_DIR/../../.venv-ocr/bin/python"; [[ -x "$PY" ]] || PY=python3
  "$PY" "$SCRIPT_DIR/../../scripts/ders_isci/yayinla.py" --esitle || { echo "DURDU: ders yayınları eşitlenemedi"; exit 1; }
fi

echo "==> Eşitleme yönü: $MODE (dry-run: ${DRY_RUN:-yok})"
if [[ "$MODE" == "to" ]]; then
  # shellcheck disable=SC2086
  rsync -avz --backup --suffix=.sync-bak $DRY_RUN "${EXCLUDES[@]}" \
    -e "$SSH -i $ORACLE_SSH_KEY" \
    "$LOCAL_DATA" "$ORACLE_USER@$ORACLE_HOST:$REMOTE_DATA"
  if [[ -z "$DRY_RUN" ]]; then
    # shellcheck disable=SC2029
    $SSH -i "$ORACLE_SSH_KEY" "$ORACLE_USER@$ORACLE_HOST" \
      "cd $ORACLE_REPO/meds && pm2 restart meds-server --update-env || true"
  fi
else
  # shellcheck disable=SC2086
  rsync -avz --backup --suffix=.sync-bak $DRY_RUN "${EXCLUDES[@]}" \
    -e "$SSH -i $ORACLE_SSH_KEY" \
    "$ORACLE_USER@$ORACLE_HOST:$REMOTE_DATA" "$LOCAL_DATA"
fi

echo "Bitti. Yedek: $BACKUP_BASE"
echo "Not: iki tarafta aynı anda yazma yapma — önce çek, sonra yaz."
