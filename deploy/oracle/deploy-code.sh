#!/usr/bin/env bash
# deploy-code.sh — cihaz working tree'yi Oracle'a gönderir + doğrular (rsync yolu).
# Neden git değil: data/*.json git'te 350MB+, commitlenmemiş değişiklikler var;
# rsync çalışan ağacı birebir taşır. GitHub yedek/ortak çalışma için durur.
# Kullanım (cihazdan, meds/ içinde): ./deploy/oracle/deploy-code.sh [--build] [--imaj] [--derleme-yok]
set -euo pipefail

# Cihaz kilidi (2026-10-20): iki oturum aynı anda dağıtınca Oracle'da eşzamanlı derleme belleği tüketip
# sunucuyu düşürdü. Tüm çalışma ağaçları (meds, meds-dagitim, ...) aynı kilit dosyasını paylaşır; ikinci
# dağıtım beklemez, hemen durur. Kilit süreç bitince (çökse bile) çekirdek tarafından bırakılır.
if [ -z "${MEDS_DEPLOY_LOCKED:-}" ]; then
  exec 9>"${XDG_RUNTIME_DIR:-/tmp}/medsor-deploy.lock"
  if ! flock -n 9; then
    echo "DURDU: başka bir dağıtım sürüyor (kilit: ${XDG_RUNTIME_DIR:-/tmp}/medsor-deploy.lock). O bitince yeniden çalıştırın." >&2
    exit 75
  fi
  export MEDS_DEPLOY_LOCKED=1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MEDS_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
KEY="${SSH_KEY:-$HOME/.ssh/medsor-oracle.key}"
ORACLE_USER="${ORACLE_USER:-ubuntu}"
ORACLE_HOST="${ORACLE_HOST:-92.5.55.109}"
# Alt betikler (content-overlay-sync.sh, sync-*.sh) aynı hedefi görsün
export ORACLE_HOST ORACLE_USER
ORACLE_DIR="/home/ubuntu/medsor/meds"
# Mod: değişen dosyalara göre kendiliğinden seçilir (2026-10-20, kod imaja gömülmez, ../..:/app bağlı):
#   yalnız dist/ / statik / içerik  → yalnız rsync (saniyeler; sayfa diskten sunulur)
#   sunucu kodu ya da src/data       → docker restart meds-app (~30 sn)
#   package*.json / Dockerfile / compose → imaj yeniden kurulur (nadir)
# --build: en az yeniden başlatma zorlar (eski kullanım) · --imaj: imajı zorla kurar · --derleme-yok: yerel vite build atlanır
FORCE=0; DO_IMAGE=0; SKIP_LOCAL_BUILD=0
for a in "$@"; do case "$a" in
  --build) FORCE=1;; --imaj) DO_IMAGE=1;; --derleme-yok) SKIP_LOCAL_BUILD=1;;
  *) echo "bilinmeyen seçenek: $a"; exit 2;; esac; done
SSH="ssh -i $KEY -o StrictHostKeyChecking=no -o ControlMaster=auto -o ControlPath=$HOME/.ssh/cm-deploy-%r@%h:%p -o ControlPersist=120"
T0=$(date +%s)

echo "==> [0/4] ders işçisi yayınları: Oracle'da yayınlanan dersler önce yerel kaynaklara işlenir"
# Oracle onaylanan dersleri kendisi yayınlar (yayinla.py --sunucu). Eşitlemeden rsync, o dersleri sitede eski
# hâline döndürürdü (Oracle sonraki turda kendini onarır ama arada ders kaybolur).
PY="$MEDS_DIR/.venv-ocr/bin/python"; [[ -x "$PY" ]] || PY=python3
"$PY" "$MEDS_DIR/scripts/ders_isci/yayinla.py" --esitle || { echo "DURDU: yayınlar eşitlenemedi (yukarıdaki çıktıya bakın)"; exit 1; }

echo "==> [0b/4] yönetim paneli değişiklikleri: Oracle data/content/ → yerel src/data (rsync ezmesin)"
"$SCRIPT_DIR/content-overlay-sync.sh" || { echo "DURDU: panel değişiklikleri eşitlenemedi (yukarıdaki çıktıya bakın)"; exit 1; }
if [[ "$SKIP_LOCAL_BUILD" == "0" ]]; then
  echo "==> [0c/4] yerel derleme (dist/ cihazda üretilir; Oracle ARM'de derleme yok)"
  (cd "$MEDS_DIR" && npm run build --silent >/dev/null) || { echo "DURDU: yerel derleme başarısız"; exit 1; }
fi
[[ -f "$MEDS_DIR/dist/index.html" ]] || { echo "DURDU: dist/index.html yok"; exit 1; }

echo "==> [1/4] rsync kod + dist (src/data DAHİL, .env HARİÇ; içerik karşılaştırması)"
CHANGED="$(mktemp)"; trap 'rm -f "$CHANGED"' EXIT
# --checksum: değişiklik listesi içeriğe göre (worktree checkout'u tarihleri yeniler; tarihe bakınca package.json
# 'değişti' sayılıp imaj gereksiz kuruluyordu, 2026-10-20). Ölçüm: ~2 sn.
rsync -az --checksum --out-format='%n' \
  --exclude='/node_modules' --exclude='/dist-gh' \
  --exclude='/data' --exclude='/.git' --exclude='/models' \
  --exclude='/training_data' --exclude='/linux' \
  --exclude='.venv*' --exclude='__pycache__' --exclude='*.log' \
  --exclude='/cloudflared.exe' \
  --exclude='/.env' --exclude='/.env.*' --exclude='*.bak' --exclude='*.bak_*' --exclude='*.backup*' \
  --exclude='/get-pip.py' --exclude='/.agents' --exclude='/.claude' --exclude='/.github' \
  --exclude='/scripts/archive' --exclude='/scripts/semantic/data' \
  -e "$SSH" "$MEDS_DIR/" "$ORACLE_USER@$ORACLE_HOST:$ORACLE_DIR/" > "$CHANGED"
grep -v '/$' "$CHANGED" > "$CHANGED.f" || true; mv "$CHANGED.f" "$CHANGED"
echo "  $(wc -l < "$CHANGED") dosya aktarıldı"

if grep -qE '^(package(-lock)?\.json|deploy/oracle/(Dockerfile\.oracle|docker-compose\.oracle\.yml))$' "$CHANGED"; then DO_IMAGE=1; fi
# Sunucunun belleğe aldığı her şey: dist/, public/, ön yüz bileşenleri, belgeler dışındaki her değişiklik
NEED_RESTART=$FORCE
if grep -vE '^(dist/|public/|docs/|src/(components|screens|styles|pages)/|.*\.(tsx|css|md)$|guncelleme_notu\.json$|deploy/)' "$CHANGED" | grep -q .; then NEED_RESTART=1; fi

echo "==> [2/4] bütünlük: kritik dosya md5 karşılaştırma"
KRITIK="deploy/oracle/docker-compose.oracle.yml deploy/oracle/Dockerfile.oracle server.ts package.json dist/index.html"
yerel=$(cd "$MEDS_DIR" && md5sum $KRITIK)
uzak=$($SSH "$ORACLE_USER@$ORACLE_HOST" "cd $ORACLE_DIR && md5sum $KRITIK")
if [[ "$yerel" == "$uzak" ]]; then echo "  OK ($(echo $KRITIK | wc -w) dosya)"; else echo "  HATA uyuşmuyor:"; diff <(echo "$yerel") <(echo "$uzak"); exit 1; fi

C="docker compose --env-file $ORACLE_DIR/.env -f deploy/oracle/docker-compose.oracle.yml"
if [[ "$DO_IMAGE" == "1" ]]; then
  echo "==> [3/4] imaj (yalnız bağımlılıklar) + başlat (kapı yeniden başlatma süresince istekleri bekletir)"
  $SSH "$ORACLE_USER@$ORACLE_HOST" "cd $ORACLE_DIR && [ ! -e node_modules ] || echo '  UYARI: sunucuda meds/node_modules var, /node_modules gölgelenir'; flock /tmp/meds-deploy.lock sh -c '
    $C build -q meds-app && $C up -d --no-deps meds-app && $C up -d --no-deps meds-server'"
elif [[ "$NEED_RESTART" == "1" ]]; then
  echo "==> [3/4] sunucu kodu/veri değişti → meds-app yeniden başlatılıyor"
  $SSH "$ORACLE_USER@$ORACLE_HOST" "flock /tmp/meds-deploy.lock docker restart -t 20 meds-app >/dev/null"
else
  echo "==> [3/4] yalnız ön yüz/statik → yeniden başlatma yok (dist/ diskten anında sunulur)"
fi

echo "==> [4/4] sağlık kontrolü (kapı üzerinden, en çok 120 sn)"
$SSH "$ORACLE_USER@$ORACLE_HOST" 'for i in $(seq 1 60); do curl -sf -m 5 http://127.0.0.1:3000/api/health && exit 0; sleep 2; done; echo "sağlık kontrolü geçmedi"; docker logs meds-app --tail 40; exit 1' | head -c 2000
echo
if [[ "$NEED_RESTART" == "1" || "$DO_IMAGE" == "1" ]]; then
  echo "==> [5/5] arama paketi + hastalık grafiği (AYRI konteynerde, arka planda; imza aynıysa ~1 sn)"
  # Yalnız son komut arka plana atılır (önceki 'a && b && nohup … &' tüm zinciri atıp SSH'ı açık tutuyordu, 2026-10-18)
  # meds-app 3 GB tavanında derlemez (bellek koruması); derleme 2 GB sınırlı tek seferlik konteynerde
  $SSH "$ORACLE_USER@$ORACLE_HOST" "cd $ORACLE_DIR; mkdir -p deploy/oracle/logs; setsid nohup ./deploy/oracle/build-search.sh </dev/null > deploy/oracle/logs/build-search.log 2>&1 &"
fi
echo "BİTTİ. ($(( $(date +%s) - T0 )) sn)"
