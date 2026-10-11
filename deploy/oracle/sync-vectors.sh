#!/usr/bin/env bash
# sync-vectors.sh — cihaz local Supabase'teki rag_chunks tablosunu Oracle local'e taşır.
# Ne zaman: cihazda vektör backfill/cron çalıştıktan sonra (yeni chunk + gömme biriktiğinde).
# Yöntem: pg_dump -t (yalnız rag_chunks) → restore --clean. Diğer tablolara dokunmaz.
# Kullanım (cihazdan): ./deploy/oracle/sync-vectors.sh
set -euo pipefail
KEY="${SSH_KEY:-$HOME/.ssh/medsor-oracle.key}"
ORACLE_USER="${ORACLE_USER:-ubuntu}"
ORACLE_HOST="${ORACLE_HOST:?ORACLE_HOST tanımlı değil (export ORACLE_HOST=92.5.55.109)}"
SSH="ssh -i $KEY -o StrictHostKeyChecking=no"
DUMP=/home/indu/medsor/meds_temp/rag_chunks_sync.dump

echo "==> [1/4] cihazdan rag_chunks dökümü"
docker exec supabase-db pg_dump -U postgres -Fc -d postgres -t public.rag_chunks -f /tmp/rag_sync.dump
docker cp supabase-db:/tmp/rag_sync.dump "$DUMP"
docker exec supabase-db rm /tmp/rag_sync.dump
ls -la "$DUMP"

echo "==> [2/4] Oracle'a taşıma"
rsync -avz -e "$SSH" "$DUMP" "$ORACLE_USER@$ORACLE_HOST:/home/ubuntu/rag_chunks_sync.dump" | tail -1

echo "==> [3/4] Oracle'da restore (HNSW yeniden kurulur, birkaç dakika)"
$SSH "$ORACLE_USER@$ORACLE_HOST" "docker cp /home/ubuntu/rag_chunks_sync.dump supabase-db:/tmp/rag_sync.dump && docker exec supabase-db pg_restore -U postgres -d postgres --clean --if-exists -t rag_chunks /tmp/rag_sync.dump 2>&1 | tail -2; docker exec supabase-db rm /tmp/rag_sync.dump; rm -f /home/ubuntu/rag_chunks_sync.dump"

echo "==> [4/4] doğrulama"
$SSH "$ORACLE_USER@$ORACLE_HOST" "docker exec supabase-db psql -U postgres -d postgres -tAc \"select count(*), count(embedding_bge_m3), count(embedding_e5) from rag_chunks;\""
echo "BİTTİ."
