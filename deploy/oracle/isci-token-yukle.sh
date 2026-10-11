#!/usr/bin/env bash
# isci-token-yukle.sh — Ders işçisinin Claude aboneliğini kullanması için uzun ömürlü anahtarı Oracle'a yükler.
#
# 1) Bu bilgisayarda bir kez:   claude setup-token
#    (tarayıcıda Claude hesabınla onay verirsin; terminalde "sk-ant-oat01-…" ile başlayan bir anahtar basılır)
# 2) Sonra:                     ./deploy/oracle/isci-token-yukle.sh
#    Anahtarı yapıştır (ekranda görünmez). Oracle'daki ~/medsor/meds/.env dosyasına CLAUDE_CODE_OAUTH_TOKEN olarak
#    yazılır (izin 600), ders işçisi yeniden başlatılır ve bağlantı denenir.
# Anahtar ne bu betikte ne git'te ne de sohbette tutulur. İptal: claude.ai → Ayarlar → Claude Code anahtarları.
set -euo pipefail
HOST="${ORACLE_SSH_HOST:-medsor-oracle}"
ENVF="/home/ubuntu/medsor/meds/.env"

read -r -s -p "Claude anahtarını yapıştır (sk-ant-oat01-…): " TOKEN; echo
[[ "$TOKEN" =~ ^sk-ant-[A-Za-z0-9_-]{20,}$ ]] || { echo "Anahtar biçimi tanınmadı; 'claude setup-token' çıktısını yapıştır."; exit 1; }

# Anahtar ssh komut satırında değil stdin'den gider (süreç listesinde görünmez)
printf '%s' "$TOKEN" | ssh "$HOST" "set -e; umask 077; T=\$(cat); \
  touch $ENVF; chmod 600 $ENVF; \
  grep -v '^CLAUDE_CODE_OAUTH_TOKEN=' $ENVF > $ENVF.yeni || true; \
  printf 'CLAUDE_CODE_OAUTH_TOKEN=%s\n' \"\$T\" >> $ENVF.yeni; mv $ENVF.yeni $ENVF; chmod 600 $ENVF"
unset TOKEN
echo "Anahtar Oracle'a yazıldı. Ders işçisi yeniden başlatılıyor…"
ssh "$HOST" "cd ~/medsor/meds && docker compose --env-file ~/medsor/meds/.env -f deploy/oracle/docker-compose.oracle.yml up -d meds-ders-isci >/dev/null 2>&1; \
  sleep 5; docker exec meds-ders-isci sh -c 'claude -p \"Yalnızca TAMAM yaz.\" --output-format text 2>&1 | head -c 200'"
echo
echo "Yukarıda 'TAMAM' görüyorsan işçi aboneliğine bağlandı."
