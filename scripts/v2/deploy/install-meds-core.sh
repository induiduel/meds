#!/usr/bin/env bash
# MedSoru Core v2 systemd kullanıcı servislerini kurar (başlatmaz).
# Kullanım:  scripts/v2/deploy/install-meds-core.sh
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
DEST_DIR="$HOME/.config/systemd/user"

command -v systemctl >/dev/null || { echo "systemctl yok; systemd olmayan ortam."; exit 1; }

mkdir -p "$DEST_DIR"
for UNIT in meds-core.service meds-v2search.service; do
  install -m 644 "$HERE/$UNIT" "$DEST_DIR/$UNIT"
done
# Semantik servis (scripts/semantic/deploy)
SEM="$HERE/../../semantic/deploy"
if [ -f "$SEM/meds-v2semantic.service" ]; then
  install -m 644 "$SEM/meds-v2semantic.service" "$DEST_DIR/meds-v2semantic.service"
fi
# Revize v2 servisi (scripts/v2/revize/deploy)
REV="$HERE/../revize/deploy"
if [ -f "$REV/meds-revize.service" ]; then
  install -m 644 "$REV/meds-revize.service" "$DEST_DIR/meds-revize.service"
fi
systemctl --user daemon-reload

echo "kuruldu : $DEST_DIR/meds-core.service"
echo "kuruldu : $DEST_DIR/meds-v2search.service"
echo "başlat  : systemctl --user enable --now meds-core meds-v2search"
echo "durum   : systemctl --user status meds-core meds-v2search"
echo "durdur  : systemctl --user disable --now meds-core meds-v2search"
