#!/usr/bin/env bash
# Olası soru gece işi: yeni kanıt varsa Claude sentezi + kapı. Hat kayıt defterinden (otomasyon/hat.json) çağrılır.
# Kullanım: gece.sh [kurul]   (kurul verilmezse takvimden sınavı geçmiş en son kurul)
set -euo pipefail
KOK="$(cd "$(dirname "$0")/../../.." && pwd)"; cd "$KOK/meds"
K="${1:-$(python3 scripts/takvim/aktif_kurul.py --son-sinav)}"
[ "$K" = 0 ] && { echo "Henüz sınavı yapılmış kurul yok; olası soru işi bekliyor"; exit 0; }
set +e; python3 scripts/olasi_soru/topla.py --kurul "$K"; rc=$?; set -e
[ "$rc" = 3 ] && { echo "Kurul $K: yeni kanıt yok, sentez atlandı"; exit 0; }
[ "$rc" != 0 ] && exit "$rc"
D="$KOK/meds_temp/olasi_soru/k$K"
[ "$(python3 -c "import json;print(json.load(open('$D/yuvalar.json'))['kanit'])")" = 0 ] && { echo "kanıt yok"; exit 0; }
cd "$D"
# Yayın: kapı 0 HATA → data/olasi_sorular/k<N>.json (yerel 3000) → Oracle aynı yol. Oracle'a ulaşılamazsa hata (sessiz geçme yok).
yayinla() {
  mkdir -p "$KOK/meds/data/olasi_sorular"
  cp "$D/olasi_sorular.json" "$KOK/meds/data/olasi_sorular/k$K.json.tmp" && mv "$KOK/meds/data/olasi_sorular/k$K.json.tmp" "$KOK/meds/data/olasi_sorular/k$K.json"
  ssh medsor-oracle "mkdir -p /home/ubuntu/medsor/meds/data/olasi_sorular" 2>/dev/null || sudo_yok=1
  rsync -az --rsync-path="sudo rsync" "$KOK/meds/data/olasi_sorular/k$K.json" "medsor-oracle:/home/ubuntu/medsor/meds/data/olasi_sorular/k$K.json" \
    && echo "yayınlandı: k$K.json (yerel + Oracle)" || { echo "HATA: Oracle'a gönderilemedi"; exit 4; }
}
# Claude (başsız). Dar izin listesi: yalnız dosya okuma/yazma + doğrulayıcı + yerel API okuma.
IZIN='Read,Write,Edit,Glob,Grep,Bash(python3 *),Bash(curl -s http://127.0.0.1:3000/*)'
cl() { claude -p "$1" --model claude-opus-5-5 --allowedTools "$IZIN" --add-dir "$KOK" >> "$D/claude.log" 2>&1; }
echo "=== $(date -Is) kurul $K sentez ===" >> "$D/claude.log"
cl "meds/scripts/olasi_soru/TALIMAT.md talimatını uygula (kurul $K). Çalışma dizini: $D. Proje kökü: $KOK. Bitince 'python3 $KOK/meds/scripts/olasi_soru/dogrula.py --kurul $K' çalıştır ve 0 HATA olana kadar düzelt."
for tur in 1 2; do
  python3 "$KOK/meds/scripts/olasi_soru/dogrula.py" --kurul "$K" > "$D/dogrula.txt" && { tail -1 "$D/dogrula.txt"; yayinla; exit 0; }
  cl "dogrula.py HATA verdi ($D/dogrula.txt). Yalnız olasi_sorular.json'u düzelt, sonra dogrula.py'yi yeniden çalıştır."
done
python3 "$KOK/meds/scripts/olasi_soru/dogrula.py" --kurul "$K"
