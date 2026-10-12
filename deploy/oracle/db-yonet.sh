#!/usr/bin/env bash
# db-yonet.sh — Oracle veritabanını yönetmek için güvenli SSH tüneli (portlar internete AÇILMAZ).
#
#   ./deploy/oracle/db-yonet.sh            tüneli açar (Ctrl+C ile kapanır)
#   ./deploy/oracle/db-yonet.sh --arka     tüneli arka planda açar
#   ./deploy/oracle/db-yonet.sh --kapat    arka plandaki tüneli kapatır
#   ./deploy/oracle/db-yonet.sh --durum    tünel açık mı
#
# Açılan (yalnız bu bilgisayarda):
#   localhost:54331          meds-pg PostgreSQL (DBeaver / pgAdmin / psql). Kullanıcı: meds, veritabanı: meds,
#                            parola: Oracle ~/medsor/meds/.env → MEDS_PG_PASSWORD
#   Örnek: psql "postgres://meds@localhost:54331/meds"
# (Supabase Studio 2026-10-12'de kaldırıldı; tablo düzenleme için DBeaver/pgAdmin kullanılır.)
# Parola bu betikte ve çıktısında YOK; görmek için:  ssh medsor-oracle 'grep ^MEDS_PG_PASSWORD ~/medsor/meds/.env'
# Önkoşul: ~/.ssh/config içinde "Host medsor-oracle" (anahtar ~/.ssh/medsor-oracle.key).
set -euo pipefail

HOST="${ORACLE_SSH_HOST:-medsor-oracle}"
# Cihazdaki yerel meds-pg 54330'u kullanır; çakışmasın diye Oracle tüneli 54331.
PG_PORT="${PG_PORT:-54331}"
SOCK="$HOME/.ssh/medsor-db-tunel.sock"
FWD=(-L "127.0.0.1:${PG_PORT}:127.0.0.1:54330")

acik_mi() { ssh -S "$SOCK" -O check "$HOST" >/dev/null 2>&1; }

case "${1:-}" in
  --kapat)
    if acik_mi; then ssh -S "$SOCK" -O exit "$HOST" >/dev/null 2>&1; echo "Tünel kapatıldı."; else echo "Açık tünel yok."; fi
    exit 0 ;;
  --durum)
    if acik_mi; then echo "Tünel AÇIK: Postgres localhost:${PG_PORT} (kullanıcı/veritabanı: meds)"; else echo "Tünel kapalı."; fi
    exit 0 ;;
  --arka)
    acik_mi && { echo "Tünel zaten açık."; exit 0; }
    ssh -f -N -M -S "$SOCK" -o ExitOnForwardFailure=yes -o ServerAliveInterval=30 "${FWD[@]}" "$HOST"
    echo "Tünel açık (arka plan): Postgres localhost:${PG_PORT} (kullanıcı/veritabanı: meds)"
    echo "Kapatmak için: $0 --kapat"
    exit 0 ;;
esac

echo "Oracle tüneli açılıyor… Postgres: localhost:${PG_PORT} (kullanıcı/veritabanı: meds)  (Ctrl+C kapatır)"
exec ssh -N -o ExitOnForwardFailure=yes -o ServerAliveInterval=30 "${FWD[@]}" "$HOST"
