#!/usr/bin/env bash
# Supabase (supabase-db) public şemasını meds-pg'ye taşır. Önce tam yedek alır.
# Kullanım: deploy/pg/migrate-from-supabase.sh   (cihazda ya da Oracle'da, konteynerlerin olduğu makinede)
# Hedefte tablo varsa durur (üzerine yazmaz); yeniden denemek için: MEDS_PG_FORCE=1
set -euo pipefail
cd "$(dirname "$0")"
STAMP=$(date +%Y%m%d_%H%M%S)
YEDEK="${MEDS_PG_BACKUP_DIR:-$HOME/yedek}/supabase_public_$STAMP.dump"
mkdir -p "$(dirname "$YEDEK")"

docker ps --format '{{.Names}}' | grep -qx supabase-db || { echo "supabase-db çalışmıyor"; exit 1; }
docker ps --format '{{.Names}}' | grep -qx meds-pg || { echo "meds-pg çalışmıyor"; exit 1; }

n=$(docker exec meds-pg psql -U meds -d meds -tAc "select count(*) from pg_tables where schemaname='public'")
if [ "$n" != "0" ] && [ "${MEDS_PG_FORCE:-0}" != "1" ]; then
  echo "meds-pg'de zaten $n tablo var; üzerine yazılmadı (MEDS_PG_FORCE=1 ile yeniden yükle)."; exit 1
fi

echo "==> [1/5] Supabase public şeması yedekleniyor: $YEDEK"
docker exec supabase-db pg_dump -U postgres -d postgres -Fc --schema=public --no-owner --no-privileges -f /tmp/mig.dump
docker cp supabase-db:/tmp/mig.dump "$YEDEK"
docker exec supabase-db rm -f /tmp/mig.dump
sha256sum "$YEDEK"

echo "==> [2/5] meds-pg'ye yükleniyor (HNSW/GIN indeksleri yeniden kurulur, birkaç dakika)"
docker cp "$YEDEK" meds-pg:/tmp/mig.dump
if [ "${MEDS_PG_FORCE:-0}" = "1" ]; then CLEAN="--clean --if-exists"; else CLEAN=""; fi
docker exec meds-pg pg_restore -U meds -d meds --no-owner --no-privileges $CLEAN -j 2 /tmp/mig.dump 2>&1 \
  | grep -vE 'schema "public" already exists|extension "vector"|already exists' || true
docker exec meds-pg rm -f /tmp/mig.dump

echo "==> [3/5] Canlı yayın tetikleyicileri, indeksler, yetkiler"
docker exec -i meds-pg psql -v ON_ERROR_STOP=1 -U meds -d meds < sql/realtime.sql

echo "==> [4/5] İstatistik"
docker exec meds-pg psql -U meds -d meds -c "analyze" >/dev/null

echo "==> [5/5] Satır sayısı karşılaştırması (kaynak | hedef)"
fail=0
for t in $(docker exec supabase-db psql -U postgres -d postgres -tAc "select tablename from pg_tables where schemaname='public' order by 1"); do
  a=$(docker exec supabase-db psql -U postgres -d postgres -tAc "select count(*) from public.\"$t\"")
  b=$(docker exec meds-pg psql -U meds -d meds -tAc "select count(*) from public.\"$t\"" 2>/dev/null || echo YOK)
  flag=""; [ "$a" = "$b" ] || { flag="  <-- FARK"; fail=1; }
  printf "%-28s %8s | %8s%s\n" "$t" "$a" "$b" "$flag"
done
[ $fail = 0 ] && echo "TAMAM: tüm tablolar eşit." || { echo "UYARI: fark var, uygulamayı geçirmeden önce incele."; exit 2; }
