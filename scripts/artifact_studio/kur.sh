#!/usr/bin/env bash
# Artifact stüdyosu kurulumu (2026-11-13).
#
#   bash meds/scripts/artifact_studio/kur.sh            # skill + launch.json kur, örneği üret
#   bash meds/scripts/artifact_studio/kur.sh --kontrol  # yalnız durum
#   bash meds/scripts/artifact_studio/kur.sh --kaldir   # skill ve launch girdisini kaldır
#
# Ne kurar:
#   * $MEDS/.claude/skills/artifact-studyo/SKILL.md  → Claude'a "artifact istendiğinde bu yolu kullan" talimatı
#   * $MEDS/.claude/launch.json → "artifact-studyo" (python3 -m http.server, çıktı klasörü)
#   * örnek sayfa: scripts/artifact_studio/cikti/kurul-2-icerik-hatti-durumu.html
#
# Not: .claude/skills yazımı kabuk korumalı olduğu için bu betik kullanıcı terminalinden çalıştırılır.
# Elle çalışır; kendiliğinden iş başlatmaz (AGENTS kural 20).
set -uo pipefail

MEDS="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
KAYNAK="$MEDS/scripts/artifact_studio"
CIKTI="$KAYNAK/cikti"
SKILL_HEDEF="$MEDS/.claude/skills/artifact-studyo"
# Masaüstü uygulaması launch.json'ı OTURUM KÖKÜNDEN okur (bu makinede /home/indu/medsor),
# yani deponun bir üstü. ARTIFACT_LAUNCH ile başka yol verilebilir.
LAUNCH="${ARTIFACT_LAUNCH:-$(dirname "$MEDS")/.claude/launch.json}"
# 5199 başka önizleme girdilerinde (kmb-pafta, tasarim-onizleme) de kullanılıyor: çakışmasın.
PORT="${ARTIFACT_PORT:-5198}"

say() { printf '%s\n' "$*"; }
uyar() { printf 'uyarı: %s\n' "$*" >&2; }

launch_yaz() {  # $1 = kur | kaldir
  python3 - "$LAUNCH" "$PORT" "$CIKTI" "$1" <<'PY'
import json, os, sys
yol, port, dizin, kip = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
d = {"version": "0.0.1", "configurations": []}
if os.path.exists(yol):
    try:
        d = json.load(open(yol, encoding="utf-8"))
    except Exception:
        os.replace(yol, yol + ".yedek")
        d = {"version": "0.0.1", "configurations": []}
if not isinstance(d, dict):
    d = {"version": "0.0.1", "configurations": []}
cfg = [c for c in (d.get("configurations") or []) if c.get("name") != "artifact-studyo"]
if kip == "kur":
    cfg.append({"name": "artifact-studyo", "runtimeExecutable": "python3",
                "runtimeArgs": ["-m", "http.server", str(port), "--bind", "127.0.0.1",
                                "--directory", dizin],
                "port": port})
d["configurations"] = cfg
os.makedirs(os.path.dirname(yol), exist_ok=True)
with open(yol, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(yol)
PY
}

durum() {
  say "── artifact stüdyosu ──"
  if [ -f "$SKILL_HEDEF/SKILL.md" ]; then say "  ✓ skill  $SKILL_HEDEF"; else say "  ✗ skill eksik"; fi
  if [ -f "$LAUNCH" ] && grep -q '"artifact-studyo"' "$LAUNCH" 2>/dev/null; then
    say "  ✓ launch $LAUNCH (port $PORT)"
  else
    say "  ✗ launch girdisi yok"
  fi
  if [ -f "$KAYNAK/studyo.py" ]; then
    say "  ✓ betik  $KAYNAK/studyo.py ($(python3 "$KAYNAK/studyo.py" --surum 2>/dev/null || echo '?'))"
  fi
  n="$(ls -1 "$CIKTI"/*.html 2>/dev/null | wc -l)"
  say "  · üretilmiş sayfa: $n  ($CIKTI)"
}

kur() {
  mkdir -p "$SKILL_HEDEF" "$CIKTI"
  cp "$KAYNAK/SKILL.md" "$SKILL_HEDEF/SKILL.md"
  say "skill  : $SKILL_HEDEF/SKILL.md"
  say "launch : $(launch_yaz kur)"
  chmod +x "$KAYNAK/studyo.py" 2>/dev/null || true
  if ! ls -1 "$CIKTI"/*.html >/dev/null 2>&1; then
    python3 "$KAYNAK/studyo.py" --ornek >/dev/null && say "örnek  : $CIKTI/… (üretildi)"
  fi
  # port başka bir süreçte mi
  if command -v ss >/dev/null && ss -ltn 2>/dev/null | grep -q ":$PORT "; then
    uyar "port $PORT şu an dolu — ARTIFACT_PORT=<boş port> ile yeniden kur"
  fi
  durum
}

kaldir() {
  rm -rf "$SKILL_HEDEF"
  launch_yaz kaldir >/dev/null
  say "kaldırıldı: skill ve launch girdisi (üretilmiş sayfalar duruyor)"
}

case "${1:-}" in
  "" ) kur ;;
  --kontrol|--doctor|kontrol ) durum ;;
  --kaldir ) kaldir ;;
  -h|--help ) sed -n '2,16p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//' ;;
  * ) uyar "bilinmeyen seçenek: $1"; exit 2 ;;
esac
