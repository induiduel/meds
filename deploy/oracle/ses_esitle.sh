#!/usr/bin/env bash
# ses_esitle.sh — yerelde (GPU, EMA) üretilen ve git'e GİRMEYEN ses kliplerini Oracle'a taşır (H623, 2026-11-18).
#
# Kök neden: çözücü/asistan/ara soru/ek modül ses kökleri .gitignore'da (H592); dagit.sh temiz worktree'den (git) dağıtır,
# bu yüzden yeni dersin sesleri canlıya hiç gitmiyordu (k2-40/41/42: data/<brans>_cozucu/ses/<kod>/ Oracle'da yoktu).
#
# Kapsam: data/*_cozucu*/ses*/, data/*_asistan*/ses*/, data/ek_moduller/ses/ (kaynak: ana çalışma ağacı, worktree değil).
#   data/sesli_anlatim/ses/ DIŞARIDA: o sesler Oracle'da üretilir/yönetilir.
# Güvenlik: yalnız ekler/günceller, ASLA silmez (--delete yok); --update: Oracle'daki daha yeni dosya ezilmez;
#   yalnız .mp3/.json/.wav/.ogg/.m4a/.mp4 (KMB videoları data/kmb_cozucu/ses_video/); sahiplik ubuntu:ubuntu.
# Doğrulama: her kökte Oracle dosya sayısı ≥ yerel olmalı; eksik varsa çıkış 73.
#
# Kullanım: bash deploy/oracle/ses_esitle.sh [--kuru]      (dagit.sh deploy-code.sh'tan sonra kendiliğinden çağırır;
#           atlamak için MEDS_DAGIT_SES=0)
set -euo pipefail
ANA="$(cd "$(dirname "$0")/../.." && pwd)"
KURU=""; [[ "${1:-}" == "--kuru" ]] && KURU="-n"
KEY="${SSH_KEY:-$HOME/.ssh/medsor-oracle.key}"
HOST="ubuntu@${ORACLE_HOST:-92.5.55.109}"
SSHC="ssh -i $KEY -o StrictHostKeyChecking=accept-new -o ConnectTimeout=15"
UZAK=/home/ubuntu/medsor/meds

cd "$ANA"
mapfile -t KOKLER < <(ls -d data/*_cozucu*/ses*/ data/*_asistan*/ses*/ data/ek_moduller/ses/ 2>/dev/null | sed 's:/$::' | sort -u)
[[ ${#KOKLER[@]} -gt 0 ]] || { echo "    ses kökü yok"; exit 0; }
echo "==> ses klasörleri Oracle'a (${#KOKLER[@]} kök${KURU:+, KURU})"

AKTARILAN=0
for k in "${KOKLER[@]}"; do
  OUT="$(rsync -a $KURU --update --itemize-changes --chown=ubuntu:ubuntu --rsync-path="sudo mkdir -p $UZAK/$k && sudo rsync" \
    --include='*/' --include='*.mp3' --include='*.json' --include='*.wav' --include='*.ogg' --include='*.m4a' --include='*.mp4' --exclude='*' \
    -e "$SSHC" "$k/" "$HOST:$UZAK/$k/")"
  n="$(grep -c '^[<>c]f' <<<"$OUT" || true)"
  if [[ "$n" != "0" ]]; then echo "    $k: $n dosya"; AKTARILAN=$((AKTARILAN + n)); fi
done
echo "    toplam aktarılan: $AKTARILAN dosya"
[[ -n "$KURU" ]] && exit 0

# Doğrulama: kök başına Oracle sayısı ≥ yerel sayı
YEREL="$(for k in "${KOKLER[@]}"; do echo "$k $(find "$k" -type f \( -name '*.mp3' -o -name '*.json' -o -name '*.wav' -o -name '*.ogg' -o -name '*.m4a' -o -name '*.mp4' \) | wc -l)"; done)"
UZAKS="$($SSHC "$HOST" "cd $UZAK && for k in ${KOKLER[*]}; do echo \"\$k \$(find \"\$k\" -type f \\( -name '*.mp3' -o -name '*.json' -o -name '*.wav' -o -name '*.ogg' -o -name '*.m4a' -o -name '*.mp4' \\) 2>/dev/null | wc -l)\"; done")"
EKSIK="$(join <(sort <<<"$YEREL") <(sort <<<"$UZAKS") | awk '$3 < $2 {print "    EKSİK " $1 ": yerel " $2 ", Oracle " $3}')"
if [[ -n "$EKSIK" ]]; then echo "$EKSIK"; echo "DURDU: Oracle'da eksik ses dosyası var (H623)"; exit 73; fi
echo "    doğrulandı: her kökte Oracle ≥ yerel"
