#!/usr/bin/env bash
# meds-pg günlük yedeği: pg_dump (özel biçim, sıkıştırılmış) → $MEDS_PG_BACKUP_DIR, son $KEEP gün saklanır.
# Geri yükleme: docker exec -i meds-pg pg_restore -U meds -d meds --clean --if-exists < dosya.dump
# Oracle: systemd zamanlayıcısı deploy/oracle/systemd/meds-pg-yedek.timer (her gece 03:30)
set -euo pipefail
DIR="${MEDS_PG_BACKUP_DIR:-$HOME/yedek/meds-pg}"
KEEP="${MEDS_PG_BACKUP_KEEP:-7}"
mkdir -p "$DIR"
F="$DIR/meds_$(date +%Y%m%d_%H%M).dump"
docker exec meds-pg pg_dump -U meds -d meds -Fc -Z 6 > "$F.tmp"
# Boş/yarım döküm eski yedeğin yerini almasın
[ "$(stat -c %s "$F.tmp")" -gt 1000000 ] || { echo "$(date -Is) HATA: döküm çok küçük, saklanmadı"; rm -f "$F.tmp"; exit 1; }
mv "$F.tmp" "$F"
ls -1t "$DIR"/meds_*.dump | tail -n +$((KEEP + 1)) | xargs -r rm -f
echo "$(date -Is) tamam: $F ($(du -h "$F" | cut -f1))"
