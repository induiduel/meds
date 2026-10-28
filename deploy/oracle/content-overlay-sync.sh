#!/usr/bin/env bash
# content-overlay-sync.sh — Oracle'da yönetim panelinden değiştirilen paket verisini (data/content/, bkz.
# src/services/contentOverlay.ts) dağıtımdan ÖNCE yerel src/data'ya geri çeker. deploy-code.sh [0/4] çağırır.
#
# Katman 2026-10-28'den beri KAYIT DÜZEYİNDE FARK'tır (data/content/<rel>.fark.json; tam kopya kaynağı gölgeliyordu).
# Her fark için (scripts/icerik_katman.py uygula):
#   yerel farkı zaten içeriyor → fark silinir (imaj bu dağıtımla aynısını taşır)
#   değilse                    → fark yerel src/data'ya (ve ana çalışma ağacına) kayıt kayıt uygulanır; fark Oracle'da
#                                kalır (yeni imaj üstünde etkisizdir), bir sonraki dağıtımda "zaten güncel" olarak silinir
#   kayıt iki tarafta değişmiş → DURUR (taban sha'sı tutmaz; elle birleştirilmeli; hiçbir şey ezilmez)
# Oracle'da çevrilmemiş TAM KOPYA varsa DURUR (sunucu açılışta çevirir; ya da icerik_katman.py goc).
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MEDS_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
KEY="${SSH_KEY:-$HOME/.ssh/medsor-oracle.key}"
ORACLE_USER="${ORACLE_USER:-ubuntu}"
ORACLE_HOST="${ORACLE_HOST:-92.5.55.109}"
ORACLE_DIR="/home/ubuntu/medsor/meds"
SSH="ssh -i $KEY -o StrictHostKeyChecking=no $ORACLE_USER@$ORACLE_HOST"
# Worktree'den dağıtılıyorsa çekilen dosya ana çalışma ağacına da yazılır (orada commit'lenmeli)
MAIN_DIR="$(git -C "$MEDS_DIR" worktree list --porcelain 2>/dev/null | awk '/^worktree /{print $2; exit}')"
MAIN_DIR="${MAIN_DIR:-$MEDS_DIR}"

TAM=$($SSH "cd $ORACLE_DIR/data/content 2>/dev/null && find . -type f -name '*.json' ! -name '*.fark.json' ! -name '*.tmp' ! -path './_*' | sed 's|^\./||'" || true)
if [[ -n "$TAM" ]]; then
  echo "DURDU: Oracle data/content altında farka çevrilmemiş tam kopya var: $TAM"
  echo "  Oracle'da: python3 $ORACLE_DIR/scripts/icerik_katman.py goc --veri $ORACLE_DIR/data --kaynak <imaj src/data>"
  exit 1
fi
mapfile -t FILES < <($SSH "cd $ORACLE_DIR/data/content 2>/dev/null && find . -type f -name '*.fark.json' ! -path './_birlesik/*' | sed 's|^\./||; s|\.fark\.json$||'" || true)
if [[ ${#FILES[@]} -eq 0 ]]; then echo "  panel değişikliği yok"; exit 0; fi

TMPD="$(mktemp -d)"; trap 'rm -rf "$TMPD"' EXIT
pulled=()
for rel in "${FILES[@]}"; do
  fk="$TMPD/$(echo "$rel" | tr '/' '_').fark.json"
  scp -q -i "$KEY" -o StrictHostKeyChecking=no "$ORACLE_USER@$ORACLE_HOST:$ORACLE_DIR/data/content/$rel.fark.json" "$fk"
  for dir in "$MEDS_DIR" "$MAIN_DIR"; do
    out=$(python3 "$MEDS_DIR/scripts/icerik_katman.py" uygula "$fk" "$dir/src/data/$rel") || {
      echo "$out"; echo "DURDU: src/data/$rel kaydı hem Oracle panelinde hem yerelde değişmiş ($dir)."
      echo "  Oracle farkı: $ORACLE_DIR/data/content/$rel.fark.json — elle birleştirip yeniden dağıtın."; exit 1; }
    echo "  $rel ($dir):$out"
    [[ "$dir" == "$MEDS_DIR" && "$out" == *"zaten güncel"* ]] && guncel=1 || { [[ "$dir" == "$MEDS_DIR" ]] && guncel=0; }
    [[ "$MAIN_DIR" == "$MEDS_DIR" ]] && break
  done
  if [[ "${guncel:-0}" == 1 ]]; then
    $SSH "rm -f '$ORACLE_DIR/data/content/$rel.fark.json'; rm -f '$ORACLE_DIR/data/content/_birlesik/$rel'"
    echo "  güncel: $rel (fark kaldırıldı)"
  else
    pulled+=("src/data/$rel")
  fi
done
if [[ ${#pulled[@]} -gt 0 ]]; then
  echo "  NOT: çekilen dosyaları commit'leyin ($MAIN_DIR): ${pulled[*]}"
fi
