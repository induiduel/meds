#!/usr/bin/env bash
# dagit.sh — TEK resmî kod dağıtım yolu (kullanıcı kararı 2026-10-20). Her oturum, her zaman bunu kullanır.
#
#   1. Önce kendi işini commit'le ve origin/main'e gönder (bu betik yalnız gönderilmiş commit'i dağıtır).
#   2. bash deploy/oracle/dagit.sh [--sessiz] [deploy-code.sh seçenekleri…]
#
# Ne yapar:
#   · cihaz dağıtım kilidini BEKLER (en çok 30 dk; aynı anda iki dağıtım Oracle'ı düşürmüştü)
#   · origin/main'in en güncel hâlini temiz worktree'ye (/home/indu/medsor/meds-dagitim) alır — çalışma ağacından
#     derlemez, başka oturumların yarım işi canlıya çıkmaz
#   · canlı (dist/dagitim.json) kirli dağıtılmışsa ya da canlı commit hedefte yoksa DURUR (geri alma yok)
#   · server.ts'ten ulaşılan bir import dosyası commit'te yoksa durur (import_denetimi.mjs)
#   · guncelleme_notu.json `onem` canlıdakinden büyük değilse durur (Kural 13; yalnız küçük düzeltme: --sessiz)
#   · deploy-code.sh'ı onaylı modda çalıştırır; eşitlemenin ([0] yayinla --esitle) attığı commit'i origin/main'e gönderir
set -euo pipefail
WT="${MEDS_DAGIT_WT:-/home/indu/medsor/meds-dagitim}"
ANA="$(cd "$(dirname "$0")/../.." && pwd)"
LOCK="${XDG_RUNTIME_DIR:-/tmp}/medsor-deploy.lock"
SESSIZ=0; ARG=()
for a in "$@"; do case "$a" in --sessiz) SESSIZ=1;; *) ARG+=("$a");; esac; done

exec 9>"$LOCK"
echo "==> dağıtım kilidi bekleniyor…"
flock -w 1800 9 || { echo "DURDU: 30 dk içinde kilit alınamadı (başka dağıtım sürüyor)"; exit 75; }
export MEDS_DEPLOY_LOCKED=1

[[ -d "$WT/.git" || -f "$WT/.git" ]] || git -C "$ANA" worktree add -q --detach "$WT" origin/main
[[ -e "$WT/node_modules" ]] || ln -s "$ANA/node_modules" "$WT/node_modules"
git -C "$WT" fetch -q origin
HEDEF="$(git -C "$WT" rev-parse origin/main)"

SSH="ssh -i ${SSH_KEY:-$HOME/.ssh/medsor-oracle.key} -o StrictHostKeyChecking=no -o ConnectTimeout=15 ubuntu@${ORACLE_HOST:-92.5.55.109}"
DAMGA="$($SSH 'cat /home/ubuntu/medsor/meds/dist/dagitim.json 2>/dev/null' || true)"
CANLI="$(python3 -c 'import json,sys;print(json.loads(sys.argv[1] or "{}").get("commit",""))' "$DAMGA")"
KIRLI="$(python3 -c 'import json,sys;print(len(json.loads(sys.argv[1] or "{}").get("kirli",[])))' "$DAMGA")"
echo "    hedef ${HEDEF:0:8} · canlı ${CANLI:0:8} (kirli öge: $KIRLI)"
if [[ "$KIRLI" != "0" ]]; then
  echo "DURDU: canlı sürüm commit'lenmemiş kodla dağıtılmış; bu dağıtım o işi geri alır. O oturum işini commit+push etsin."; exit 78
fi
if [[ -n "$CANLI" ]] && ! git -C "$WT" merge-base --is-ancestor "$CANLI" "$HEDEF"; then
  echo "DURDU: canlı commit ($CANLI) origin/main'de yok — önce o commit main'e gönderilmeli."; exit 77
fi
if [[ "$CANLI" == "$HEDEF" ]]; then echo "Canlı zaten güncel (${HEDEF:0:8})."; exit 0; fi

git -C "$WT" checkout -q -f --detach "$HEDEF"
# commit'lenmemiş dosyaya import → canlı açılış çökmesi (2026-10-21)
node "$WT/deploy/oracle/import_denetimi.mjs" "$WT" server.ts || exit 76
YENI_ONEM="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["onem"])' "$WT/guncelleme_notu.json")"
CANLI_ONEM="$(curl -s -m 15 https://api.nofrostlife.com.tr/api/surum | python3 -c 'import json,sys;print(json.load(sys.stdin).get("onem",0))' 2>/dev/null || echo 0)"
if [[ "$SESSIZ" == "0" && "$YENI_ONEM" -le "$CANLI_ONEM" ]]; then
  echo "DURDU: guncelleme_notu.json onem ($YENI_ONEM) canlıdakinden ($CANLI_ONEM) büyük değil (Kural 13)."
  echo "  onem+1, baslik, maddeler → commit+push → yeniden çalıştır. Yalnız küçük düzeltme ise: --sessiz"; exit 79
fi

(cd "$WT" && MEDS_DAGIT_ONAYLI=1 bash deploy/oracle/deploy-code.sh "${ARG[@]}")

# [0] eşitleme Oracle yayınlarını bu worktree'de commit'lemiş olabilir: main'e gönder (kaybolmasın)
SON="$(git -C "$WT" rev-parse HEAD)"
if [[ "$SON" != "$HEDEF" ]]; then
  if git -C "$WT" push -q origin "HEAD:main"; then echo "==> eşitleme commit'i main'e gönderildi (${SON:0:8})"
  else echo "UYARI: eşitleme commit'i (${SON:0:8}) main'e gönderilemedi (main ilerlemiş) — elle birleştirin"; fi
fi
echo "==> canlı: $(curl -s -m 15 https://api.nofrostlife.com.tr/api/surum | head -c 120)"
