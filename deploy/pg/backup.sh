#!/usr/bin/env bash
# meds-pg günlük yedeği: pg_dump (özel biçim, sıkıştırılmış) → $MEDS_PG_BACKUP_DIR, son $KEEP gün saklanır.
# Geri yükleme: docker exec -i meds-pg pg_restore -U meds -d meds --clean --if-exists < dosya.dump
# Oracle: systemd zamanlayıcısı deploy/oracle/systemd/meds-pg-yedek.timer (her gece 03:30)
# --yalniz-liste: yedek almadan yalnız panel yedek listesini yeniden üretir.
set -euo pipefail
DIR="${MEDS_PG_BACKUP_DIR:-$HOME/yedek/meds-pg}"
KEEP="${MEDS_PG_BACKUP_KEEP:-7}"
mkdir -p "$DIR"

if [ "${1:-}" != "--yalniz-liste" ]; then
  F="$DIR/meds_$(date +%Y%m%d_%H%M).dump"
  docker exec meds-pg pg_dump -U meds -d meds -Fc -Z 6 > "$F.tmp"
  # Boş/yarım döküm eski yedeğin yerini almasın
  [ "$(stat -c %s "$F.tmp")" -gt 1000000 ] || { echo "$(date -Is) HATA: döküm çok küçük, saklanmadı"; rm -f "$F.tmp"; exit 1; }
  mv "$F.tmp" "$F"
  ls -1t "$DIR"/meds_*.dump | tail -n +$((KEEP + 1)) | xargs -r rm -f
  echo "$(date -Is) tamam: $F ($(du -h "$F" | cut -f1))"
fi

# Panel yedek listesi (Yönetim › Veritabanı ve yedek): konteyner $DIR'i göremez, liste meds_temp'e yazılır.
# Her yedeğin içindekiler pg_restore -l ile denetlenir (yalnız içindekiler okunur).
INDEX="${MEDS_PG_BACKUP_INDEX:-$HOME/medsor/meds_temp/yedek_listesi.json}"
{
  printf '{"guncellendi":"%s","klasor":"%s","saklama_gun":%s,"backups":[' "$(date -Is)" "$DIR" "$KEEP"
  ilk=1
  for f in $(ls -1t "$DIR"/meds_*.dump 2>/dev/null); do
    toc=$(docker exec -i meds-pg pg_restore -l < "$f" 2>/dev/null || true)
    n=$(printf '%s\n' "$toc" | grep -vc '^;' || true)
    tablo=$(printf '%s\n' "$toc" | grep -c ' TABLE DATA ' || true)
    [ "$ilk" = 1 ] || printf ','
    ilk=0
    printf '{"ad":"%s","boyut":%s,"tarih":"%s","ogeler":%s,"tablolar":%s,"dogrulandi":%s}' \
      "$(basename "$f")" "$(stat -c %s "$f")" "$(date -Is -r "$f")" "${n:-0}" "${tablo:-0}" "$([ "${tablo:-0}" -gt 0 ] && echo true || echo false)"
  done
  printf '],"geri_yukleme":"docker exec -i meds-pg pg_restore -U meds -d meds --clean --if-exists < DOSYA"}\n'
} > "$INDEX.tmp" && mv "$INDEX.tmp" "$INDEX" || echo "$(date -Is) uyarı: yedek listesi yazılamadı"
