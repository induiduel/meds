#!/usr/bin/env bash
# deploy-code.sh — cihaz working tree'yi Oracle'a gönderir + doğrular (rsync yolu).
# Neden git değil: data/*.json git'te 350MB+, commitlenmemiş değişiklikler var;
# rsync çalışan ağacı birebir taşır. GitHub yedek/ortak çalışma için durur.
# Kullanım (cihazdan, meds/ içinde): ./deploy/oracle/deploy-code.sh [--build]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MEDS_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
KEY="${SSH_KEY:-$HOME/.ssh/medsor-oracle.key}"
ORACLE_USER="${ORACLE_USER:-ubuntu}"
ORACLE_HOST="${ORACLE_HOST:?ORACLE_HOST tanımlı değil (export ORACLE_HOST=92.5.55.109)}"
ORACLE_DIR="/home/ubuntu/medsor/meds"
DO_BUILD=0
[[ "${1:-}" == "--build" ]] && DO_BUILD=1
SSH="ssh -i $KEY -o StrictHostKeyChecking=no"

echo "==> [0/4] ders işçisi yayınları: Oracle'da yayınlanan dersler önce yerel kaynaklara işlenir"
# Oracle onaylanan dersleri kendisi yayınlar (yayinla.py --sunucu). Eşitlemeden rsync, o dersleri sitede eski
# hâline döndürürdü (Oracle sonraki turda kendini onarır ama arada ders kaybolur).
PY="$MEDS_DIR/.venv-ocr/bin/python"; [[ -x "$PY" ]] || PY=python3
"$PY" "$MEDS_DIR/scripts/ders_isci/yayinla.py" --esitle || { echo "DURDU: yayınlar eşitlenemedi (yukarıdaki çıktıya bakın)"; exit 1; }

echo "==> [1/4] rsync kod (src/data DAHİL, .env HARİÇ)"
rsync -avz --checksum \
  --exclude='/node_modules' --exclude='/dist' --exclude='/dist-gh' \
  --exclude='/data' --exclude='/.git' --exclude='/models' \
  --exclude='/training_data' --exclude='/linux' \
  --exclude='.venv*' --exclude='__pycache__' --exclude='*.log' \
  --exclude='/cloudflared.exe' --exclude='src/data/decks/items' \
  --exclude='/.env' --exclude='/.env.*' --exclude='*.bak' --exclude='*.bak_*' --exclude='*.backup*' \
  --exclude='/get-pip.py' --exclude='/.agents' --exclude='/.claude' --exclude='/.github' \
  --exclude='/scripts/archive' --exclude='/scripts/semantic/data' \
  -e "$SSH" "$MEDS_DIR/" "$ORACLE_USER@$ORACLE_HOST:$ORACLE_DIR/" 2>&1 | tail -2

echo "==> [2/4] bütünlük: kritik dosya md5 karşılaştırma"
for f in deploy/oracle/docker-compose.oracle.yml deploy/oracle/Dockerfile.oracle server.ts package.json; do
  a=$(md5sum "$MEDS_DIR/$f" | cut -d' ' -f1)
  b=$($SSH "$ORACLE_USER@$ORACLE_HOST" "md5sum $ORACLE_DIR/$f" | cut -d' ' -f1)
  if [[ "$a" == "$b" ]]; then echo "  OK $f"; else echo "  HATA $f uyuşmuyor!"; exit 1; fi
done

if [[ "$DO_BUILD" == "1" ]]; then
  echo "==> [3/4] Oracle'da derle + başlat (kesintisiz: imaj önce derlenir, kapı yeniden başlatma süresince istekleri bekletir)"
  # Kapı (meds-server, Caddy) yalnız yoksa/tanımı değiştiyse yeniden kurulur; Caddyfile değişirse: docker restart meds-server
  $SSH "$ORACLE_USER@$ORACLE_HOST" "cd $ORACLE_DIR && flock /tmp/meds-deploy.lock sh -c '
    C=\"docker compose --env-file $ORACLE_DIR/.env -f deploy/oracle/docker-compose.oracle.yml\"
    \$C build -q meds-app &&
    \$C up -d --no-deps meds-app &&
    \$C up -d --no-deps meds-server
  '"
fi

echo "==> [4/4] sağlık kontrolü (kapı üzerinden, en çok 120 sn)"
$SSH "$ORACLE_USER@$ORACLE_HOST" 'for i in $(seq 1 60); do curl -sf -m 5 http://127.0.0.1:3000/api/health && exit 0; sleep 2; done; echo "sağlık kontrolü geçmedi"; docker logs meds-app --tail 40; exit 1' | head -c 2000
echo
if [[ "$DO_BUILD" == "1" ]]; then
  echo "==> [5/5] arama paketi + hastalık grafiği (AYRI konteynerde, arka planda; imza aynıysa ~1 sn)"
  # meds-app 3 GB tavanında derlemez (bellek koruması); derleme 2 GB sınırlı tek seferlik konteynerde
  $SSH "$ORACLE_USER@$ORACLE_HOST" "cd $ORACLE_DIR && mkdir -p deploy/oracle/logs && nohup ./deploy/oracle/build-search.sh </dev/null > deploy/oracle/logs/build-search.log 2>&1 &"
fi
echo "BİTTİ."
