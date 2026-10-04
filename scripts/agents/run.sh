#!/usr/bin/env bash
# Okuma ajanlarını doğru Python ortamıyla çalıştırır.
#   scripts/agents/run.sh read  <dosya|klasör> [--vision] [--force]   # belgeleri temp1'e çevir
#   scripts/agents/run.sh watch [--once] [--vision]                    # meds_downloads'ı izle
#   scripts/agents/run.sh install-service                              # izleyiciyi oturum açılışında otomatik başlat
set -e
AGENTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEDS_DIR="$(cd "$AGENTS_DIR/../.." && pwd)"
PY="$MEDS_DIR/.venv-ocr/bin/python"
export PYTHONWARNINGS=ignore
# .env içindeki MEDS_* / OLLAMA_URL değerlerini yükle
if [ -f "$MEDS_DIR/.env" ]; then
  while IFS= read -r line; do
    case "$line" in MEDS_*=*|OLLAMA_URL=*) eval "export ${line%%#*}";; esac
  done < "$MEDS_DIR/.env"
fi

cmd="${1:-}"; shift || true
case "$cmd" in
  read)  exec "$PY" "$AGENTS_DIR/read_document.py" "$@" ;;
  watch) exec "$PY" "$AGENTS_DIR/watch_downloads.py" "$@" ;;
  install-service)
    UNIT_DIR="$HOME/.config/systemd/user"; mkdir -p "$UNIT_DIR"
    cat > "$UNIT_DIR/meds-downloads-watcher.service" <<EOF
[Unit]
Description=MedSoru downloads -> temp1 okuma ajanı

[Service]
ExecStart="$AGENTS_DIR/run.sh" watch
Restart=on-failure

[Install]
WantedBy=default.target
EOF
    systemctl --user daemon-reload
    systemctl --user enable --now meds-downloads-watcher.service
    echo "Servis kuruldu: systemctl --user status meds-downloads-watcher" ;;
  *) sed -n '2,6p' "${BASH_SOURCE[0]}"; exit 2 ;;
esac
