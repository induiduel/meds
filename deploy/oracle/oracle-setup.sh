#!/usr/bin/env bash
# oracle-setup.sh — Oracle Always Free (Ubuntu 22.04/24.04) ilk kurulumu.
# İdempotent: tekrar çalıştırılabilir. Repo ~/meds altında varsayılır.
set -euo pipefail

REPO_DIR="${REPO_DIR:-$HOME/meds}"
APP_DIR="$REPO_DIR/meds"
NODE_MAJOR="${NODE_MAJOR:-20}"

echo "==> [1/6] Sistem paketleri"
sudo apt-get update -y
sudo apt-get install -y curl git build-essential rsync ufw fail2ban

echo "==> [2/6] Node.js $NODE_MAJOR"
if ! command -v node >/dev/null 2>&1; then
  curl -fsSL https://deb.nodesource.com/setup_${NODE_MAJOR}.x | sudo -E bash -
  sudo apt-get install -y nodejs
fi
node --version
npm --version

echo "==> [3/6] PM2"
if ! command -v pm2 >/dev/null 2>&1; then
  sudo npm install -g pm2
fi

echo "==> [4/6] cloudflared"
if ! command -v cloudflared >/dev/null 2>&1; then
  ARCH="$(dpkg --print-architecture)"
  case "$ARCH" in
    arm64)  DEB="cloudflared-linux-arm64.deb" ;;
    amd64)  DEB="cloudflared-linux-amd64.deb" ;;
    *) echo "Desteklenmeyen mimari: $ARCH"; exit 1 ;;
  esac
  curl -fsSL -o /tmp/$DEB "https://github.com/cloudflare/cloudflared/releases/latest/download/$DEB"
  sudo dpkg -i /tmp/$DEB || sudo apt-get install -f -y
fi
cloudflared --version || true

echo "==> [5/6] Uygulama kurulumu ($APP_DIR)"
cd "$APP_DIR"
npm ci --no-audit --no-fund || npm install --no-audit --no-fund
npm run build

echo "==> [6/6] PM2 ile başlatma"
pm2 start ecosystem.config.cjs --only meds-server 2>/dev/null || \
  pm2 --cwd "$APP_DIR/deploy/oracle" start ecosystem.config.cjs --only meds-server || \
  pm2 start "$APP_DIR/deploy/oracle/ecosystem.config.cjs" --only meds-server
pm2 save || true

echo "--- UFW (22/80/443 açık, 3000 kapalı: erişim tunnel üzerinden) ---"
sudo ufw allow 22/tcp || true
sudo ufw allow 80/tcp || true
sudo ufw allow 443/tcp || true
sudo ufw --force enable || true

echo "--- PM2 açılışta başlasın ---"
pm2 startup systemd -u "$USER" --hp "$HOME" || true
echo "Yukarıdaki 'sudo env ... pm2 startup' satırını bir kez çalıştır, sonra: pm2 save"

echo ""
echo "Kurulum bitti. Sıradakiler:"
echo "  1) $APP_DIR/.env dosyasını deploy/oracle/.env.oracle.example dosyasına bakarak doldur, sonra: pm2 restart meds-server"
echo "  2) /etc/cloudflared/config.yml dosyasını cloudflared-config.example.yml dosyasına bakarak yaz, DNS route ekle, systemctl enable --now cloudflared"
echo "  3) curl -s http://127.0.0.1:3000/api/health"
