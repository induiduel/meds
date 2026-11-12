#!/usr/bin/env bash
# OpenDesign köprüsünü kurar/tazeler ve denetler (2026-11-13).
#
#   bash meds/scripts/opendesign/kur.sh            # kur + yeniden başlat + doktor
#   bash meds/scripts/opendesign/kur.sh --kontrol  # yalnız denetle (hiçbir şey yazma)
#   bash meds/scripts/opendesign/kur.sh --kaldir   # servisi durdur, kurulu dosyaları sil
#
# Neden: `claude` (masaüstü + terminal) 3P geçit kipinde Anthropic model adları gönderir; köprü bunları
# OpenDesign kimliklerine çevirir. Köprü kapalıyken CLI yerinde olsa bile her LLM aşaması 401'de düşer —
# bu yüzden kurulum tek komuttur ve `--kontrol` tek bakışta durumu söyler.
# Elle çalıştırılır; kendiliğinden iş başlatmaz (AGENTS kural 20).
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"          # meds/scripts/opendesign
BIN="$HOME/.local/bin/opendesign-kopru.py"
MAP="$HOME/.claude/opendesign-kopru.json"
BIRIM="$HOME/.config/systemd/user/opendesign-kopru.service"
ENV_DOSYA="$HOME/.config/opendesign-kopru.env"

say() { printf '%s\n' "$*"; }
die() { printf 'HATA: %s\n' "$*" >&2; exit 1; }

sistemctl() {
  command -v systemctl >/dev/null || die "systemctl yok"
  systemctl --user "$@" 2>/dev/null || return 0
}

durum() {
  # 1) kurulu dosyalar
  [ -f "$BIN" ] && say "betik    : $BIN ($(python3 "$BIN" --surum 2>/dev/null || echo '?') sürüm)" \
                || say "betik    : YOK ($BIN)"
  [ -f "$MAP" ] && say "eşleme   : $MAP" || say "eşleme   : YOK ($MAP)"
  [ -f "$BIRIM" ] && say "birim    : $BIRIM" || say "birim    : YOK ($BIRIM)"
  # 2) ayarlar (köprü adresi + anahtar)
  python3 - "$HOME/.claude/settings.json" <<'PY'
import json, os, sys
p = sys.argv[1]
try:
    env = (json.load(open(p)).get("env") or {})
except Exception as e:  # noqa: BLE001
    print(f"ayarlar  : okunamadı ({e})"); raise SystemExit
print(f"ayarlar  : ANTHROPIC_BASE_URL={env.get('ANTHROPIC_BASE_URL', 'YOK')} · "
      f"ANAHTAR={'…' + env['ANTHROPIC_AUTH_TOKEN'][-4:] if env.get('ANTHROPIC_AUTH_TOKEN') else 'YOK'}")
for k in ("ANTHROPIC_DEFAULT_OPUS_MODEL", "ANTHROPIC_DEFAULT_SONNET_MODEL", "ANTHROPIC_DEFAULT_HAIKU_MODEL"):
    print(f"           {k}={env.get(k, 'YOK')}")
PY
  # 3) servis + doktor
  if command -v systemctl >/dev/null; then
    say "servis   : $(systemctl --user is-active opendesign-kopru 2>/dev/null || echo 'yok') / $(systemctl --user is-enabled opendesign-kopru 2>/dev/null || echo 'kapalı')"
  fi
  [ -f "$BIN" ] && { python3 "$BIN" --doctor || true; }
}

kur() {
  command -v python3 >/dev/null || die "python3 yok"
  mkdir -p "$(dirname "$BIN")" "$(dirname "$MAP")" "$(dirname "$BIRIM")"

  # 1) köprü betiği
  install -m 0755 "$SRC/kopru.py" "$BIN"

  # 2) eşleme: rotalar depodan, port/upstream kullanıcıda özelleşmişse korunur; eski dosya yedeklenir
  if [ -f "$MAP" ]; then cp -a "$MAP" "$MAP.yedek-$(date +%Y%m%d-%H%M%S)"; fi
  python3 - "$SRC/rotalar.json" "$MAP" <<'PY'
import json, sys
kaynak, hedef = sys.argv[1], sys.argv[2]
yeni = json.load(open(kaynak, encoding="utf-8"))
try:
    eski = json.load(open(hedef, encoding="utf-8"))
except Exception:  # noqa: BLE001
    eski = {}
for anahtar in ("port", "upstream"):           # kullanıcı özelleştirmesi ezilmesin
    if eski.get(anahtar):
        yeni[anahtar] = eski[anahtar]
with open(hedef, "w", encoding="utf-8") as f:
    json.dump(yeni, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(f"eşleme yazıldı: {len(yeni['routes'])} satır → {hedef}")
PY

  # 3) systemd birimi (yalnız içerik değiştiyse yaz)
  yeni_birim="$(mktemp)"; trap 'rm -f "$yeni_birim"' EXIT
  cat > "$yeni_birim" <<'UNIT'
[Unit]
Description=OpenDesign koprusu (Claude 3P + Claude Code icin model adi cevirici)
Documentation=file://%h/medsor/meds/scripts/opendesign/kopru.py
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
EnvironmentFile=-%h/.config/opendesign-kopru.env
Environment=PYTHONUNBUFFERED=1
ExecStart=/usr/bin/python3 %h/.local/bin/opendesign-kopru.py
Restart=always
RestartSec=2
MemoryMax=256M
CPUQuota=50%
OOMScoreAdjust=200
NoNewPrivileges=yes
PrivateTmp=yes

[Install]
WantedBy=default.target
UNIT
  if ! cmp -s "$yeni_birim" "$BIRIM"; then install -m 0644 "$yeni_birim" "$BIRIM"; say "birim yazıldı: $BIRIM"; fi

  # 4) başlat/yeniden başlat + sağlık bekle
  if command -v systemctl >/dev/null && systemctl --user show-environment >/dev/null 2>&1; then
    systemctl --user daemon-reload
    systemctl --user enable opendesign-kopru >/dev/null 2>&1 || true
    systemctl --user restart opendesign-kopru
    for _ in $(seq 1 20); do
      if curl -fsS -m 1 http://127.0.0.1:8787/health >/dev/null 2>&1; then
        say "köprü hazır: http://127.0.0.1:8787"
        break
      fi
      sleep 0.5
    done
  else
    say "uyarı: systemctl --user erişilemedi — elle: python3 $BIN &"
    say "       (bu oturum sandbox içindeyse terminalden çalıştırın)"
  fi
  durum
}

kaldir() {
  command -v systemctl >/dev/null && { systemctl --user disable --now opendesign-kopru 2>/dev/null || true; }
  rm -f "$BIN" "$MAP" "$BIRIM" "$MAP".yedek-* 2>/dev/null || true
  command -v systemctl >/dev/null && systemctl --user daemon-reload 2>/dev/null || true
  say "kaldırıldı. (Claude ayarları ~/.claude/settings.json içinde ANTHROPIC_BASE_URL'i hâlâ köprüyü gösteriyorsa"
  say " düzeltin: ya köprüyü yeniden kurun ya da ANTHROPIC_BASE_URL=https://amr-link.open-design.ai yapın.)"
}

case "${1:-}" in
  "" ) kur ;;
  --kontrol|--doctor|kontrol ) durum ;;
  --kaldir|kaldir ) kaldir ;;
  -h|--help) sed -n '2,12p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//' ;;
  *) die "bilinmeyen seçenek: $1 (--kontrol | --kaldir)" ;;
esac
