#!/usr/bin/env bash
# Claude Code eklentileri: kodlama ve tasarımda hata yakalayan resmî eklentiler + dil sunucuları (2026-11-13).
#
#   bash meds/scripts/claude_eklenti/kur.sh            # eksikleri kur, sonra durumu yaz
#   bash meds/scripts/claude_eklenti/kur.sh --kontrol  # yalnız durum (hiçbir şey kurmaz)
#
# Neden: modeller OpenDesign geçidine geçti; kod kalitesini modelin dikkatine bırakmamak için
#   * typescript-lsp / pyright-lsp → düzenlenen dosyada gerçek tip/hata bilgisi (tsc ve py_compile'ın ötesi),
#   * code-review / pr-review-toolkit → değişikliği bağımsız gözle denetler,
#   * code-simplifier, feature-dev      → sadeleştirme ve özellik akışı,
#   * frontend-design                   → tasarım kalitesi (mevcut v15 kabuğuyla birlikte),
#   * claude-security, security-guidance→ sır sızıntısı ve güvenlik deseni uyarısı,
#   * plugin-dev                        → yeni skill/eklenti yazımı.
# Elle çalıştırılır; kendiliğinden iş başlatmaz (AGENTS kural 20).
set -uo pipefail

PAZAR="claude-plugins-official"
EKLENTILER="typescript-lsp pyright-lsp frontend-design code-review code-simplifier feature-dev claude-security security-guidance pr-review-toolkit plugin-dev"
NPM_PAKETLER="typescript-language-server pyright"

say() { printf '%s\n' "$*"; }
uyar() { printf 'uyarı: %s\n' "$*" >&2; }

kurulu_liste() {  # satır satır eklenti adları
  claude plugin list --json 2>/dev/null | python3 -c '
import json,sys
try: d=json.load(sys.stdin)
except Exception: d=[]
for p in d if isinstance(d,list) else d.get("plugins",[]):
    n=p.get("name") or p.get("id") or ""
    if n: print(n.split("@")[0])
'
}

npm_var() {  # $1 = paket
  npm ls -g --depth=0 "$1" >/dev/null 2>&1
}

durum() {
  say "── eklentiler ($PAZAR) ──"
  var="$(kurulu_liste)"
  for e in $EKLENTILER; do
    if printf '%s\n' "$var" | grep -qx "$e"; then say "  ✓ $e"; else say "  ✗ $e (eksik)"; fi
  done
  say "── dil sunucuları ──"
  for p in $NPM_PAKETLER; do
    if npm_var "$p"; then say "  ✓ $p ($(npm ls -g --depth=0 "$p" 2>/dev/null | awk -F@ '/@/{print $NF}' | head -1))"
    else say "  ✗ $p (eksik: npm i -g $p)"
    fi
  done
  # tsc projede yerel; pyright global aranır
  say "── proje kapıları ──"
  MEDS="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
  [ -f "$MEDS/package.json" ] && say "  ✓ npm run lint = tsc --noEmit ($MEDS)"
  if command -v python3 >/dev/null; then say "  ✓ python3 $(python3 -V 2>&1 | cut -d' ' -f2)"; fi
}

kur() {
  command -v claude >/dev/null || { uyar "claude CLI yok"; return 1; }
  command -v node >/dev/null || { uyar "node/npm yok — LSP paketleri kurulamaz"; }

  var="$(kurulu_liste)"
  for e in $EKLENTILER; do
    if printf '%s\n' "$var" | grep -qx "$e"; then say "var   : $e"; continue; fi
    say "kuruluyor: $e"
    if ! claude plugin install "$e@$PAZAR" -y >${TMPDIR:-/tmp}/claude-eklenti-$e.log 2>&1; then
      # bayrak sırası sürüme göre değişebilir: ikinci deneme
      claude plugin install "$e" -y --marketplace "$PAZAR" >>${TMPDIR:-/tmp}/claude-eklenti-$e.log 2>&1 \
        || uyar "$e kurulamadı (günlük: ${TMPDIR:-/tmp}/claude-eklenti-$e.log)"
    fi
  done

  if command -v npm >/dev/null; then
    eksik=""
    for p in $NPM_PAKETLER; do npm_var "$p" || eksik="$eksik $p"; done
    if [ -n "$eksik" ]; then
      say "npm ile kuruluyor:$eksik"
      # typescript-language-server TypeScript'i de ister (projede yerel sürüm var ama global sunucu kendi arar)
      npm install -g --no-fund --no-audit $eksik typescript >${TMPDIR:-/tmp}/claude-lsp-npm.log 2>&1 \
        || uyar "npm kurulumu başarısız (günlük: ${TMPDIR:-/tmp}/claude-lsp-npm.log)"
    fi
  fi
  durum
}

case "${1:-}" in
  "" ) kur ;;
  --kontrol|--doctor|kontrol ) durum ;;
  -h|--help ) sed -n '2,16p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//' ;;
  * ) uyar "bilinmeyen seçenek: $1"; exit 2 ;;
esac
