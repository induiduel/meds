#!/usr/bin/env bash
# content-overlay-sync.sh — Oracle'da yönetim panelinden değiştirilen paket verisini (data/content/, bkz.
# src/services/contentOverlay.ts) dağıtımdan ÖNCE yerel src/data'ya geri çeker. deploy-code.sh [0/4] çağırır.
#
# Her katman dosyası için:
#   yerel == katman         → yerel zaten güncel; katman dosyası silinir (imaj bu dağıtımla aynısını taşır)
#   yerel == çalışan imaj   → yerel son dağıtımdan beri değişmedi; katman yerele (ve ana çalışma ağacına) çekilir
#   ikisi de değil          → iki tarafta da değişmiş: DURUR (elle birleştirilmeli; hiçbir şey ezilmez)
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MEDS_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
KEY="${SSH_KEY:-$HOME/.ssh/medsor-oracle.key}"
ORACLE_USER="${ORACLE_USER:-ubuntu}"
ORACLE_HOST="${ORACLE_HOST:?ORACLE_HOST tanımlı değil}"
ORACLE_DIR="/home/ubuntu/medsor/meds"
SSH="ssh -i $KEY -o StrictHostKeyChecking=no $ORACLE_USER@$ORACLE_HOST"
# Worktree'den dağıtılıyorsa çekilen dosya ana çalışma ağacına da yazılır (orada commit'lenmeli)
MAIN_DIR="$(git -C "$MEDS_DIR" worktree list --porcelain 2>/dev/null | awk '/^worktree /{print $2; exit}')"
MAIN_DIR="${MAIN_DIR:-$MEDS_DIR}"

mapfile -t FILES < <($SSH "cd $ORACLE_DIR/data/content 2>/dev/null && find . -type f -name '*.json' ! -name '_ids.json' | sed 's|^\./||'" || true)
if [[ ${#FILES[@]} -eq 0 ]]; then echo "  panel değişikliği yok"; exit 0; fi

pulled=()
for rel in "${FILES[@]}"; do
  overlay=$($SSH "md5sum '$ORACLE_DIR/data/content/$rel'" | cut -d' ' -f1)
  image=$($SSH "docker exec meds-app md5sum '/app/src/data/$rel' 2>/dev/null" | cut -d' ' -f1 || true)
  localf="$MEDS_DIR/src/data/$rel"
  loc=$([[ -f "$localf" ]] && md5sum "$localf" | cut -d' ' -f1 || echo yok)
  if [[ "$loc" == "$overlay" ]]; then
    $SSH "rm -f '$ORACLE_DIR/data/content/$rel'"
    echo "  güncel: $rel (katman kaldırıldı)"
  elif [[ -n "$image" && "$loc" == "$image" ]]; then
    for dir in "$MEDS_DIR" "$MAIN_DIR"; do
      mkdir -p "$(dirname "$dir/src/data/$rel")"
      scp -q -i "$KEY" -o StrictHostKeyChecking=no "$ORACLE_USER@$ORACLE_HOST:$ORACLE_DIR/data/content/$rel" "$dir/src/data/$rel"
    done
    pulled+=("src/data/$rel")
    echo "  çekildi: $rel (panel değişikliği yerele işlendi)"
  else
    echo "DURDU: src/data/$rel hem Oracle panelinde hem yerelde değişmiş."
    echo "  Oracle kopyası: $ORACLE_DIR/data/content/$rel — yerelle elle birleştirip yeniden dağıtın."
    exit 1
  fi
done
if [[ ${#pulled[@]} -gt 0 ]]; then
  echo "  NOT: çekilen dosyaları commit'leyin ($MAIN_DIR): ${pulled[*]}"
fi
