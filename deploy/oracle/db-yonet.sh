#!/usr/bin/env bash
# db-yonet.sh — Oracle veritabanını yönetmek için güvenli SSH tüneli (portlar internete AÇILMAZ).
#
#   ./deploy/oracle/db-yonet.sh            tüneli açar, Studio'yu tarayıcıda açar (Ctrl+C ile kapanır)
#   ./deploy/oracle/db-yonet.sh --arka     tüneli arka planda açar
#   ./deploy/oracle/db-yonet.sh --kapat    arka plandaki tüneli kapatır
#   ./deploy/oracle/db-yonet.sh --durum    tünel açık mı
#
# Açılanlar (yalnız bu bilgisayarda):
#   http://localhost:54323   Supabase Studio (tablo düzenleyici, SQL editörü). Giriş: Oracle'daki
#                            ~/medsor/meds/supabase-server/.env → DASHBOARD_USERNAME / DASHBOARD_PASSWORD
#   localhost:54322          PostgreSQL (DBeaver / pgAdmin / psql). Kullanıcı: postgres.<POOLER_TENANT_ID>
#                            (pooler) ya da postgres; parola: aynı .env → POSTGRES_PASSWORD
# Parolalar bu betikte ve çıktısında YOK; görmek için:  ssh medsor-oracle 'grep -E "^(DASHBOARD_|POSTGRES_PASSWORD|POOLER_TENANT_ID)" ~/medsor/meds/supabase-server/.env'
# Önkoşul: ~/.ssh/config içinde "Host medsor-oracle" (anahtar ~/.ssh/medsor-oracle.key).
set -euo pipefail

HOST="${ORACLE_SSH_HOST:-medsor-oracle}"
STUDIO_PORT="${STUDIO_PORT:-54323}"
PG_PORT="${PG_PORT:-54322}"
SOCK="$HOME/.ssh/medsor-db-tunel.sock"
FWD=(-L "127.0.0.1:${STUDIO_PORT}:127.0.0.1:8000" -L "127.0.0.1:${PG_PORT}:127.0.0.1:5432")

acik_mi() { ssh -S "$SOCK" -O check "$HOST" >/dev/null 2>&1; }

case "${1:-}" in
  --kapat)
    if acik_mi; then ssh -S "$SOCK" -O exit "$HOST" >/dev/null 2>&1; echo "Tünel kapatıldı."; else echo "Açık tünel yok."; fi
    exit 0 ;;
  --durum)
    if acik_mi; then echo "Tünel AÇIK: Studio http://localhost:${STUDIO_PORT} · Postgres localhost:${PG_PORT}"; else echo "Tünel kapalı."; fi
    exit 0 ;;
  --arka)
    acik_mi && { echo "Tünel zaten açık."; exit 0; }
    ssh -f -N -M -S "$SOCK" -o ExitOnForwardFailure=yes -o ServerAliveInterval=30 "${FWD[@]}" "$HOST"
    echo "Tünel açık (arka plan): Studio http://localhost:${STUDIO_PORT} · Postgres localhost:${PG_PORT}"
    echo "Kapatmak için: $0 --kapat"
    exit 0 ;;
esac

echo "Oracle tüneli açılıyor… Studio: http://localhost:${STUDIO_PORT}  ·  Postgres: localhost:${PG_PORT}  (Ctrl+C kapatır)"
( sleep 3; command -v xdg-open >/dev/null && xdg-open "http://localhost:${STUDIO_PORT}" >/dev/null 2>&1 || true ) &
exec ssh -N -o ExitOnForwardFailure=yes -o ServerAliveInterval=30 "${FWD[@]}" "$HOST"
