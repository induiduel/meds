#!/usr/bin/env bash
# ses_dusuk_esitle.sh — yeni/onarılmış sesli ders sesinin düşük bit hızlı kopyası (H709/H714, 2026-11-27).
#
# dagit.sh her dağıtımın sonunda kendiliğinden çağırır (atlamak: MEDS_DAGIT_DUSUK=0). LLM yok, GPU yok (ffmpeg, nice 19).
# 1) Oracle data/sesli_anlatim/ses (ve arşiv) → yerel: boyutu farklı dosya gelir (--size-only), yerelde DAHA YENİ dosya
#    ezilmez (--update), hiçbir şey silinmez. sesli_cek.sh --ignore-existing kullandığı için onarılan ses (aynı ad) gelmiyordu.
# 2) scripts/uretim/sesli_anlatim/dusuk_bit.py: yalnız eksik ya da kaynak boyutu değişmiş kopyalar üretilir.
# 3) ses_dusuk/ → Oracle (yalnız .mp3/.json; yarım dosya .yarim uzantılıdır, gönderilmez).
# Sunucu kopyayı yalnız {kaynakBayt} Oracle'daki asıl sesle tutarsa verir; tutmayan ders asıl sesle çalar (güvenli düşüş).
set -euo pipefail
ANA="$(cd "$(dirname "$0")/../.." && pwd)"
KEY="${SSH_KEY:-$HOME/.ssh/medsor-oracle.key}"
HOST="ubuntu@${ORACLE_HOST:-92.5.55.109}"
SSHC="ssh -i $KEY -o StrictHostKeyChecking=accept-new -o ConnectTimeout=15"
UZAK=/home/ubuntu/medsor/meds
cd "$ANA"

echo "==> düşük bit hızlı ses kopyaları"
for kok in data/sesli_anlatim data/arsiv_25_26/sesli_anlatim; do
  $SSHC "$HOST" "test -d $UZAK/$kok/ses" || continue
  mkdir -p "$kok/ses"
  n="$(rsync -a --size-only --update --itemize-changes -e "$SSHC" --include='*/' --include='*.mp3' --exclude='*' \
    "$HOST:$UZAK/$kok/ses/" "$kok/ses/" | grep -c '^>f' || true)"
  echo "    $kok/ses: Oracle'dan $n ses"
done

python3 scripts/uretim/sesli_anlatim/dusuk_bit.py --is "${MEDS_DUSUK_IS:-3}"

for kok in data/sesli_anlatim/ses_dusuk data/arsiv_25_26/sesli_anlatim/ses_dusuk; do
  [[ -d "$kok" ]] || continue
  n="$(rsync -a --update --itemize-changes --chown=ubuntu:ubuntu --rsync-path="sudo mkdir -p $UZAK/$kok && sudo rsync" \
    --include='*/' --include='*.mp3' --include='*.json' --exclude='*' -e "$SSHC" "$kok/" "$HOST:$UZAK/$kok/" | grep -c '^<f' || true)"
  echo "    $kok → Oracle: $n dosya"
done

# Doğrulama: canlıdaki varyantların kaçında geçerli kopya var (bilgi; eksik varsa uyarır, dağıtımı durdurmaz)
GIZ="$(grep -E '^MEDS_PANEL_SECRET=' "$ANA/.env" 2>/dev/null | cut -d= -f2- | tr -d '"' || true)"
curl -s -m 20 -H "x-panel-secret: $GIZ" https://nofrostlife.com.tr/api/canli-ders | python3 -c '
import json,sys
try:
    d=json.load(sys.stdin)["dersler"]
except Exception:
    print("    UYARI: canlı liste okunamadı"); sys.exit(0)
v=[x for r in d for x in r.get("varyantlar",[])]
k=sum(1 for x in v if x.get("dusuk"))
print(f"    canlı: {k}/{len(v)} ses varyantında düşük kopya" + ("" if k==len(v) else "  (UYARI: eksik)"))' || true
