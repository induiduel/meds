#!/usr/bin/env bash
# sync-vectors.sh — cihazdaki meds-pg'nin rag_chunks tablosunu Oracle meds-pg'ye taşır.
# Ne zaman: cihazda vektör backfill/cron çalıştıktan sonra (yeni chunk + gömme biriktiğinde).
# Yöntem: pg_dump -t (yalnız rag_chunks) → restore --clean. Diğer tablolara dokunmaz.
# Kullanım (cihazdan): ./deploy/oracle/sync-vectors.sh          (fark)
#                       ./deploy/oracle/sync-vectors.sh --tam    (tam döküm, ORACLE_HOST gerekir)
set -euo pipefail
# 2026-10-13: varsayılan artık FARK eşitlemesi (yalnız değişen satırlar, gzip'li, birkaç yüz KB–birkaç MB):
#   scripts/advanced_ai/rag_vektor_hatti.py --sadece-oracle
# Tam döküm + --clean geri yükleme yalnız --tam ile (DİKKAT: geri yüklemeden sonra indeksleri yeniden kur:
#   deploy/pg/sql/rag_chunks_indexes.sql — 2026-10-13'te Oracle'da indekssiz kalmıştı).
if [[ "${1:-}" != "--tam" ]]; then
  cd "$(dirname "$0")/../.."
  exec .venv-ocr/bin/python scripts/advanced_ai/rag_vektor_hatti.py --sadece-oracle "$@"
fi
KEY="${SSH_KEY:-$HOME/.ssh/medsor-oracle.key}"
ORACLE_USER="${ORACLE_USER:-ubuntu}"
ORACLE_HOST="${ORACLE_HOST:-92.5.55.109}"
SSH="ssh -i $KEY -o StrictHostKeyChecking=no"
DUMP=/home/indu/medsor/meds_temp/rag_chunks_sync.dump

echo "==> [1/4] cihazdan rag_chunks dökümü"
docker exec meds-pg pg_dump -U meds -Fc -d meds -t public.rag_chunks -f /tmp/rag_sync.dump
docker cp meds-pg:/tmp/rag_sync.dump "$DUMP"
docker exec meds-pg rm /tmp/rag_sync.dump
ls -la "$DUMP"

echo "==> [2/4] Oracle'a taşıma"
rsync -avz -e "$SSH" "$DUMP" "$ORACLE_USER@$ORACLE_HOST:/home/ubuntu/rag_chunks_sync.dump" | tail -1

echo "==> [3/4] Oracle'da restore (HNSW yeniden kurulur, birkaç dakika)"
$SSH "$ORACLE_USER@$ORACLE_HOST" "docker cp /home/ubuntu/rag_chunks_sync.dump meds-pg:/tmp/rag_sync.dump && docker exec meds-pg pg_restore -U meds -d meds --no-owner --clean --if-exists -t rag_chunks /tmp/rag_sync.dump 2>&1 | tail -2; docker exec meds-pg rm /tmp/rag_sync.dump; rm -f /home/ubuntu/rag_chunks_sync.dump"

echo "==> [3b] indeksler (geri yükleme düşürebiliyor)"
$SSH "$ORACLE_USER@$ORACLE_HOST" "docker exec -i meds-pg psql -U meds -d meds -q" < deploy/pg/sql/rag_chunks_indexes.sql
$SSH "$ORACLE_USER@$ORACLE_HOST" "docker exec -i meds-pg psql -U meds -d meds -q" < deploy/pg/sql/rag_vektor_islevleri.sql

echo "==> [4/4] doğrulama"
$SSH "$ORACLE_USER@$ORACLE_HOST" "docker exec meds-pg psql -U meds -d meds -tAc \"select count(*), count(embedding_bge_m3), count(embedding_e5) from rag_chunks;\""
echo "BİTTİ."
