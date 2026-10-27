#!/usr/bin/env bash
# Olası soru gece işi: yeni kanıt varsa Claude sentezi + kapı. Hat kayıt defterinden (otomasyon/hat.json) çağrılır.
# Kullanım: gece.sh [kurul]   (kurul verilmezse takvimden sınavı geçmiş en son kurul)
[ "${MEDS_LLM_ELLE:-}" = 1 ] && [ -z "${INVOCATION_ID:-}" ] || { echo "[llm_kilit] olasi_soru gece.sh elle komut gerektirir" >&2; exit 75; }
set -euo pipefail
KOK="$(cd "$(dirname "$0")/../../.." && pwd)"; cd "$KOK/meds"
# Akşam (meds-olasi-soru.timer) ve gece (meds-hat-gece) çalıştırmaları üst üste binmesin
exec 8>"${XDG_RUNTIME_DIR:-/tmp}/medsor-olasi-soru.lock"; flock -n 8 || { echo "olası soru işi zaten çalışıyor"; exit 0; }
K="${1:-$(python3 scripts/takvim/aktif_kurul.py --son-sinav)}"
# Sınav günü kontrol listesi (bir kez): sınav günü ilk çalıştırma (20:00) ve ertesi gün — yöneticiye bildirim
python3 - <<'PYEOF' || true
import json, sys, datetime as dt
from pathlib import Path
sys.path.insert(0, "scripts/takvim"); sys.path.insert(0, "otomasyon")
from aktif_kurul import durum
from bildir import bildir
bugun = dt.date.today(); d = durum(bugun.isoformat())
isaret = Path("../meds_temp/olasi_soru/sinav_gunu_bildirimleri.json")
gonderilen = json.loads(isaret.read_text()) if isaret.exists() else []
kurul, sinav = d["aktif"], d["aktif_sinav"]
if d["sinava_gun"] == 0 and f"k{kurul}-gun" not in gonderilen:
    bildir(f"Bugün Kurul {kurul} sınavı — olası soru kontrol listesi",
           "1) Öğrenciler sınavdan çıkınca Soru ekle'de 'Kaçıncı soruydu?' alanıyla soruları girsin (numara yuvalamayı çok iyileştirir).\n"
           "2) 20:00 ve 23:30'da olası sorular kurulur; 02:30 gece hattı yeniden dener.\n"
           f"3) Yarın sabah /olasi-sorular?kurul={kurul} — güven rozetleri ve kanıt sayısına bakın; öğrenciler 'Buydu / Bu değildi' ile düzeltir.\n"
           "4) Ham soru defteri ve havuz Oracle'da birikir; motor her çalıştırmada güncel kopyayı çeker.", hedef="sinav-gunu")
    gonderilen.append(f"k{kurul}-gun")
son = d.get("son_sinav")
if son and (bugun - dt.date.fromisoformat(next(k["sinav"] for k in json.load(open("src/data/kurul_takvimi_ozet.json"))["kurullar"] if k["kurul"] == son))).days == 1 \
        and f"k{son}-ertesi" not in gonderilen:
    p = Path(f"data/olasi_sorular/k{son}.json")
    n = len(json.loads(p.read_text()).get("sorular", [])) if p.exists() else 0
    bildir(f"Kurul {son} olası soruları: {n} soru" if n else f"Kurul {son}: henüz olası soru seti yok",
           (f"/olasi-sorular?kurul={son} yayında. Yeni kayıt geldikçe her akşam 20:00/23:30 ve gece güncellenir." if n else
            "Sınav sonrası kayıt gelmedi ya da sentez kapıdan geçmedi — Yönetim › Hat ve meds_temp/olasi_soru/ günlüğüne bakın."),
           hedef="sinav-gunu")
    gonderilen.append(f"k{son}-ertesi")
isaret.parent.mkdir(parents=True, exist_ok=True); isaret.write_text(json.dumps(gonderilen))
PYEOF
[ "$K" = 0 ] && { echo "Henüz sınavı yapılmış kurul yok; olası soru işi bekliyor"; exit 0; }
# Havuz dondurulduysa (data/havuz_dondur.json, src/services/havuzDondur.ts) öğrenci kayıtlarına dokunulmaz: yerel ya da
# Oracle kopyasında dondur:true varsa çık. Oracle'a ulaşılamazsa da güvenli tarafta kal (çık).
dondu() { python3 -c "import json,sys;sys.exit(0 if json.load(sys.stdin).get('dondur') is True else 1)" 2>/dev/null; }
if dondu < "$KOK/meds/data/havuz_dondur.json" \
   || ssh -o ConnectTimeout=15 medsor-oracle "cat /home/ubuntu/medsor/meds/data/havuz_dondur.json 2>/dev/null || echo '{}'" | dondu \
   || ! ssh -o ConnectTimeout=15 medsor-oracle true 2>/dev/null; then
  echo "Havuz donduruldu (ya da Oracle'a ulaşılamadı): olası soru işi atlandı, kayıtlara dokunulmadı"; exit 0
fi
# Öğrenci kayıtları canlıda (Oracle) birikir: güncel kopyayı salt-okunur çek (çekilemezse DUR, eski veriyle sentez yok)
V="$KOK/meds_temp/olasi_soru/oracle_veri"; mkdir -p "$V/question_ledger" "$V/olasi_sorular"
U=medsor-oracle:/home/ubuntu/medsor/meds/data
rsync -az "$U/questions.json" "$V/questions.json" && rsync -az --delete "$U/question_ledger/" "$V/question_ledger/" \
  && { rsync -az "$U/olasi_sorular/geri_bildirim_k$K.jsonl" "$V/olasi_sorular/" 2>/dev/null || true; } \
  || { echo "HATA: Oracle'dan öğrenci kayıtları çekilemedi"; exit 5; }
set +e; python3 scripts/olasi_soru/topla.py --kurul "$K" --veri "$V"; rc=$?; set -e
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
  python3 "$KOK/meds/scripts/db/icerik_kaydi.py" --kimlik "k$K" --tur olasi_soru --kurul "$K" --oracle \
    --kaynak-sha "$(python3 -c "import json;print(json.load(open('$D/yuvalar.json'))['parmak_izi'][:16])")" --yol "data/olasi_sorular/k$K.json" || true
}
# Claude (başsız). Dar izin listesi: yalnız dosya okuma/yazma + doğrulayıcı + yerel API okuma.
IZIN='Read,Write,Edit,Glob,Grep,Bash(python3 *),Bash(curl -s http://127.0.0.1:3000/*)'
cl() { timeout 3h claude -p "$1" --model claude-opus-5-5 --allowedTools "$IZIN" --add-dir "$KOK" >> "$D/claude.log" 2>&1 || echo "claude çıkış $? (devam: kapı karar verir)" >> "$D/claude.log"; }
echo "=== $(date -Is) kurul $K sentez ===" >> "$D/claude.log"
cl "meds/scripts/olasi_soru/TALIMAT.md talimatını uygula (kurul $K). Çalışma dizini: $D. Proje kökü: $KOK. Bitince 'python3 $KOK/meds/scripts/olasi_soru/dogrula.py --kurul $K' çalıştır ve 0 HATA olana kadar düzelt."
for tur in 1 2; do
  python3 "$KOK/meds/scripts/olasi_soru/dogrula.py" --kurul "$K" > "$D/dogrula.txt" && { tail -1 "$D/dogrula.txt"; yayinla
    python3 -c "import json;print(json.load(open('$D/yuvalar.json'))['parmak_izi'])" > "$D/yayinlanan_iz.txt"; exit 0; }
  cl "dogrula.py HATA verdi ($D/dogrula.txt). Yalnız olasi_sorular.json'u düzelt, sonra dogrula.py'yi yeniden çalıştır."
done
python3 "$KOK/meds/scripts/olasi_soru/dogrula.py" --kurul "$K"
