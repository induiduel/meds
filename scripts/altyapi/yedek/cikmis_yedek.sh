#!/usr/bin/env bash
# cikmis_yedek.sh — çıkmış soru bankasının günlük yedeği (dosya git'te tutulmuyor, 100 MiB GitHub sınırı).
# Canlı (Oracle data/) + yerel (meds/data/) pastQuestions.json ve çöp kutusu listesi gzip'lenir;
# ~/medsor-yedek/cikmis/<tarih>/ altına yazılır, 30 günden eski klasörler silinir.
# systemd: ~/.config/systemd/user/meds-cikmis-yedek.{service,timer} (her gün 04:30)
set -euo pipefail
HEDEF="$HOME/medsor-yedek/cikmis/$(date +%Y%m%d)"
YEREL=/home/indu/medsor/meds/data
mkdir -p "$HEDEF"

for f in pastQuestions.json deleted_past_questions.json; do
  gzip -c "$YEREL/$f" > "$HEDEF/yerel_$f.gz"
done

# Canlı (oylar, yorumlar, bildirimler yalnız orada birikir); bağlantı yoksa yerel yedek yine de kalır
if ssh -o ConnectTimeout=15 -o BatchMode=yes medsor-oracle true 2>/dev/null; then
  for f in pastQuestions.json deleted_past_questions.json; do
    ssh -o BatchMode=yes medsor-oracle "gzip -c ~/medsor/meds/data/$f" > "$HEDEF/canli_$f.gz.tmp"
    gzip -t "$HEDEF/canli_$f.gz.tmp" && mv "$HEDEF/canli_$f.gz.tmp" "$HEDEF/canli_$f.gz"
  done
else
  echo "UYARI: Oracle'a bağlanılamadı, yalnız yerel yedek alındı" >&2
fi

find "$HOME/medsor-yedek/cikmis" -mindepth 1 -maxdepth 1 -type d -mtime +30 -exec rm -rf {} +
ls -la "$HEDEF"
