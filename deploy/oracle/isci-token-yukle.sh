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
export LC_ALL=C   # Türkçe yerel ayarda [A-Za-z] aralıkları farklı yorumlanabiliyor
HOST="${ORACLE_SSH_HOST:-medsor-oracle}"
ENVF="/home/ubuntu/medsor/meds/.env"

TOKEN=""
# 1) Önce panodan dene (yapıştırma gerekmez): anahtarı terminalden kopyalaman yeterli.
# Anahtar terminalde birkaç satıra bölünebilir; açıklama metninden BOŞ satırla ayrılır → yalnız anahtarın paragrafını birleştir.
PANO="$( (wl-paste --no-newline 2>/dev/null || xclip -o -selection clipboard 2>/dev/null) | python3 -c '
import re, sys
t = sys.stdin.read()
for par in re.split(r"\n\s*\n", t):
    j = re.sub(r"\s+", "", par)
    m = re.search(r"sk-ant-[A-Za-z0-9_-]{40,}", j)
    if m:
        print(m.group(0)); break
' 2>/dev/null || true)"
if [[ "$PANO" =~ (sk-ant-[A-Za-z0-9_-]{40,}) ]]; then
  ADAY="${BASH_REMATCH[1]}"
  read -r -p "Panoda ${#ADAY} karakterlik bir Claude anahtarı bulundu (${ADAY:0:13}…). Kullanılsın mı? [E/h] " CEVAP
  if [[ ! "$CEVAP" =~ ^[hHnN] ]]; then TOKEN="$ADAY"; fi
fi
unset PANO ADAY
# 2) Panoda yoksa: anahtarı BURADA üret ve çıktıyı yalnız sana açık geçici dosyadan oku (kopyala-yapıştır gerekmez;
#    Claude terminal bölmesi anahtarın bir kısmını maskeli gösterdiği için kopyalanamıyor).
if [[ -z "$TOKEN" ]]; then
  CLAUDE_BIN="$(command -v claude || ls -d "$HOME"/.config/Claude/claude-code/*/claude 2>/dev/null | sort -V | tail -1)"
  [[ -x "$CLAUDE_BIN" ]] || { echo "claude komutu bulunamadı."; exit 1; }
  echo "Panoda anahtar yok. Şimdi 'claude setup-token' çalışacak: tarayıcıda Claude hesabınla onay ver."
  echo "Anahtar ekrana basılsa da kopyalaman GEREKMEZ; betik kendisi alacak."
  read -r -p "Devam edilsin mi? [E/h] " CEVAP
  [[ "$CEVAP" =~ ^[hHnN] ]] && exit 1
  GECICI="$(umask 077; mktemp -d "${XDG_RUNTIME_DIR:-/tmp}/claude-anahtar.XXXXXX")"
  script -q -f -c "\"$CLAUDE_BIN\" setup-token" "$GECICI/cikti" || true
  TOKEN="$(python3 - "$GECICI/cikti" <<'PYX'
import re, sys
t = open(sys.argv[1], encoding="utf-8", errors="ignore").read()
# İmleç/renk kaçışlarını satır sonuna çevir (Ink boş satırları imleç hareketiyle çiziyor), \r'yi at
t = re.sub(r"\x1b\[[0-9;?]*[ABEFGHJKSTf]", "\n", t)
t = re.sub(r"\x1b\[[0-9;?]*[ -/]*[@-~]|\x1b\][^\x07]*\x07|\x1b[=>]|\r", "", t)
satirlar = [x.strip() for x in t.split("\n")]
SAF = re.compile(r"^[A-Za-z0-9_-]+$")
aday = []
for i, x in enumerate(satirlar):
    m = re.search(r"(sk-ant-[A-Za-z0-9_-]+)$", x)
    if not m:
        continue
    tok = m.group(1)
    for y in satirlar[i + 1:]:          # yalnız tamamı anahtar karakterinden oluşan devam satırları (boşları atla)
        if not y:
            continue
        if SAF.match(y):
            tok += y
        else:
            break
    if len(tok) >= 60:
        aday.append(tok)
if aday:
    print(max(set(aday), key=aday.count))   # ekran yeniden çizilse de en sık görülen tam aday
PYX
)"
  [[ -n "$TOKEN" ]] && echo "Anahtar çıktıdan alındı (${#TOKEN} karakter)."
fi
TOKEN="${TOKEN//[[:space:]]/}"
if ! [[ "$TOKEN" =~ ^sk-ant-[A-Za-z0-9_-]{60,}$ ]]; then
  echo "Anahtar biçimi tanınmadı (${#TOKEN} karakter)."
  [[ -n "${GECICI:-}" ]] && echo "Çıktı yalnız sana açık geçici bellekte saklandı: $GECICI (yeniden üretmeden düzeltebilmem için). Yeniden başlatınca silinir."
  exit 1
fi
# Oracle'a göndermeden önce anahtarı bu bilgisayarda gerçekten dene (geçersiz anahtar yüklenmesin)
echo "Anahtar bu bilgisayarda deneniyor…"
YB="$(command -v claude || ls -d "$HOME"/.config/Claude/claude-code/*/claude 2>/dev/null | sort -V | tail -1)"
if ! CLAUDE_CODE_OAUTH_TOKEN="$TOKEN" timeout 90 "$YB" -p "Yalnızca TAMAM yaz." --output-format text 2>&1 | grep -q "TAMAM"; then
  echo "Anahtar Claude'a bağlanamadı (${#TOKEN} karakter); Oracle'a YÜKLENMEDİ."
  [[ -n "${GECICI:-}" ]] && echo "Çıktı yalnız sana açık geçici bellekte saklandı: $GECICI"
  exit 1
fi
echo "Anahtar geçerli."
[[ -n "${GECICI:-}" ]] && { shred -u "$GECICI"/* 2>/dev/null; rm -rf "$GECICI"; }
echo "Anahtar alındı (${#TOKEN} karakter)."

# Anahtar ssh komut satırında değil stdin'den gider (süreç listesinde görünmez)
printf '%s' "$TOKEN" | ssh "$HOST" "set -e; umask 077; T=\$(cat); \
  touch $ENVF; chmod 600 $ENVF; \
  grep -v '^CLAUDE_CODE_OAUTH_TOKEN=' $ENVF > $ENVF.yeni || true; \
  printf 'CLAUDE_CODE_OAUTH_TOKEN=%s\n' \"\$T\" >> $ENVF.yeni; mv $ENVF.yeni $ENVF; chmod 600 $ENVF"
unset TOKEN
(wl-copy --clear 2>/dev/null || true)   # anahtar panoda kalmasın
echo "Anahtar Oracle'a yazıldı. Ders işçisi yeniden başlatılıyor…"
ssh "$HOST" "cd ~/medsor/meds && docker compose --env-file ~/medsor/meds/.env -f deploy/oracle/docker-compose.oracle.yml up -d meds-ders-isci >/dev/null 2>&1; \
  sleep 5; docker exec meds-ders-isci sh -c 'claude -p \"Yalnızca TAMAM yaz.\" --output-format text 2>&1 | head -c 200'"
echo
echo "Yukarıda 'TAMAM' görüyorsan işçi aboneliğine bağlandı."
