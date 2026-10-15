#!/usr/bin/env bash
# Sesli anlatım kuyruğunu cihazdan Oracle'a taşır (bir kez): yerel işçiyi durdurur, yarım işler parçalarıyla
# birlikte data/sesli_anlatim'i Oracle'a kopyalar, Oracle işçisini açar. Ücretli üretim ayarı yereldekiyle aynı kalır.
# Sonra yerel işçi kapalı kalır (iki makine aynı işi yapmasın).
# Kullanım: scripts/sesli_anlatim/oracle_tasi.sh
set -euo pipefail
MEDS_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
YEREL="http://127.0.0.1:3000"
HDR=(-H 'Content-Type: application/json' -H 'x-admin-email: nofrostlife@gmail.com')
KOK=/home/ubuntu/medsor/meds/data/sesli_anlatim

echo "==> [1/5] yerel işçi durduruluyor (üzerindeki parça bitene kadar beklenir; ücretli parça yarıda kesilmez)"
curl -sf -X POST "$YEREL/api/sesli-anlatim/isci" "${HDR[@]}" -d '{"aktif":false}' >/dev/null
for i in $(seq 1 180); do
  n=$(python3 -c "import json;print(sum(1 for x in json.load(open('$MEDS_DIR/data/sesli_anlatim/kuyruk.json')) if x['durum']=='calisiyor'))")
  [[ "$n" == "0" ]] && break
  sleep 5
done
[[ "$n" == "0" ]] || { echo "DURDU: 15 dk içinde çalışan iş bitmedi"; exit 1; }
echo "    çalışan iş kalmadı"

UCRETLI=$(python3 -c "import json;print(1 if json.load(open('$MEDS_DIR/data/sesli_anlatim/ayar.json')).get('ucretliAktif') else 0)" 2>/dev/null || echo 0)

echo "==> [2/5] data/sesli_anlatim → Oracle (ayar.json hariç)"
rsync -az --rsync-path="sudo rsync" --exclude='ayar.json' --exclude='*.tmp' \
  "$MEDS_DIR/data/sesli_anlatim/" "medsor-oracle:$KOK/"

echo "==> [3/5] Oracle: durdurma nedeniyle bekleyen işler sıraya, işçi açık, ücretli üretim=$UCRETLI"
ssh medsor-oracle "sudo python3 - $KOK $UCRETLI" <<'PY'
import json, sys
k, ucretli = sys.argv[1], sys.argv[2] == '1'
q = json.load(open(k + '/kuyruk.json'))
for x in q:
    if x['durum'] == 'calisiyor' or (x['durum'] == 'kota-bekliyor' and 'durduruldu' in (x.get('hata') or '')):
        x['durum'] = 'bekliyor'; x.pop('sonrakiDeneme', None); x.pop('hata', None)
json.dump(q, open(k + '/kuyruk.json', 'w'), ensure_ascii=False, indent=1)
json.dump({'isciAktif': True, 'ucretliAktif': ucretli}, open(k + '/ayar.json', 'w'))
print('kuyruk:', len(q), 'iş; ücretli:', ucretli)
PY
ssh medsor-oracle "sudo chown -R root:root $KOK"

echo "==> [4/5] Oracle işçisi uyandırılıyor"
SECRET=$(grep '^MEDS_PANEL_SECRET=' "$MEDS_DIR/.env" | cut -d= -f2-)
curl -sf -X POST "https://api.nofrostlife.com.tr/api/sesli-anlatim/isci" "${HDR[@]}" -H "x-panel-secret: $SECRET" -d '{"aktif":true}' && echo

echo "==> [5/5] doğrulama"
curl -sf "https://api.nofrostlife.com.tr/api/sesli-anlatim" -H 'x-admin-email: nofrostlife@gmail.com' | python3 -c "
import sys, json
d = json.load(sys.stdin)
ses = sum(1 for x in d['dersler'] if x['varyantlar'])
print('Oracle: ders', len(d['dersler']), '· sesli', ses, '· kuyruk', len(d['kuyruk']), '· harcanan', d['butce']['harcananTL'], 'TL · ücretli', d['ucretliAktif'], '· işçi', d['isci'])"
echo "Taşındı. Yerel işçi kapalı kalır."
