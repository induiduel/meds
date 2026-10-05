#!/usr/bin/env bash
# manage-service.ps1'in Linux karşılığı.
# Kullanım: manage-service.sh <install-and-start|status|stop|sync-now|notify> [başlık] [mesaj]
# Servis, systemd --user altında "meds-local-sync.service" olarak çalışır.
set -u

ACTION="${1:-install-and-start}"
TITLE="${2:-MedSoru Otomasyon Servisi}"
MESSAGE="${3:-Servis arka planda çalışıyor.}"

MEDS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UNIT_NAME="meds-local-sync.service"
UNIT_DIR="$HOME/.config/systemd/user"
UNIT_PATH="$UNIT_DIR/$UNIT_NAME"
NODE_BIN="$(command -v node || echo /usr/bin/node)"

notify() {
  command -v notify-send >/dev/null 2>&1 && notify-send "$1" "$2" 2>/dev/null || true
}

is_running() { systemctl --user is-active --quiet "$UNIT_NAME" 2>/dev/null; }
is_installed() { [ -f "$UNIT_PATH" ]; }
is_enabled() { systemctl --user is-enabled --quiet "$UNIT_NAME" 2>/dev/null; }

case "$ACTION" in
  notify)
    notify "$TITLE" "$MESSAGE"
    echo "Notification sent."
    ;;

  status)
    PIDS="[]"
    if is_running; then
      PID="$(systemctl --user show -p MainPID --value "$UNIT_NAME" 2>/dev/null)"
      [ -n "$PID" ] && [ "$PID" != "0" ] && PIDS="[$PID]"
    fi
    printf '{"isInstalledOnDesktop":%s,"isRegisteredInStartup":%s,"isRunning":%s,"pids":%s,"desktopShortcutPath":"%s","startupShortcutPath":"%s"}\n' \
      "$(is_installed && echo true || echo false)" \
      "$(is_enabled && echo true || echo false)" \
      "$(is_running && echo true || echo false)" \
      "$PIDS" "$UNIT_PATH" "$UNIT_PATH"
    ;;

  stop)
    systemctl --user stop "$UNIT_NAME" 2>/dev/null
    notify "MedSoru Otomasyon Servisi" "Arka plan işleyici durduruldu."
    echo "Stopped."
    ;;

  sync-now)
    echo "Triggering immediate sync..."
    notify "MedSoru: Senkronizasyon Başlatıldı" "Google Drive ve yerel klasör taranıyor..."
    (cd "$MEDS_DIR" && nohup "$NODE_BIN" scripts/meds-local-sync.mjs --sync-now >/dev/null 2>&1 &)
    ;;

  install-and-start)
    mkdir -p "$UNIT_DIR"
    cat > "$UNIT_PATH" <<EOF
[Unit]
Description=MedSoru yerel senkronizasyon servisi

[Service]
WorkingDirectory=$MEDS_DIR
ExecStart=$NODE_BIN scripts/meds-local-sync.mjs
Restart=on-failure

[Install]
WantedBy=default.target
EOF
    systemctl --user daemon-reload
    systemctl --user enable --now "$UNIT_NAME"
    notify "MedSoru Otomasyon Servisi" "Oturum açılışına eklendi, servis arka planda çalışıyor."
    echo "SUCCESS: systemd user service installed and started."
    ;;

  *)
    echo "Bilinmeyen eylem: $ACTION" >&2
    exit 2
    ;;
esac
