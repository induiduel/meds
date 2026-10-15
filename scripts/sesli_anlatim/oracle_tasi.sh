#!/usr/bin/env bash
# Sesli anlatım kuyruğunu cihazdan Oracle'a taşır (bir kez): yerel işçiyi durdurur, yarım işler parçalarıyla
# birlikte data/sesli_anlatim'i Oracle'a kopyalar, Oracle işçisini açar. Sonra yerel işçi kapalı kalır.
# Kullanım: scripts/sesli_anlatim/oracle_tasi.sh
set -euo pipefail
MEDS_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
YEREL="http://127.0.0.1:3000"
HDR=(-H 'Content-Type: application/json' -H 'x-admin-email: nofrostlife@gmail.com')

echo "==> [1/4] yerel işçi durduruluyor"
curl -sf -X POST "$YEREL/api/sesli-anlatim/isci" "${HDR[@]}" -d '{"aktif":false}' >/dev/null
for i in $(seq 1 120); do
  n=$(python3 -c "import json;print(sum(1 for x in json.load(open('$MEDS_DIR/data/sesli_anlatim/kuyruk.json')) if x['durum']=='calisiyor'))")
  [[ "$n" == "0" ]] && break
  sleep 5
done
echo "    çalışan iş kalmadı"

echo "==> [2/4] data/sesli_anlatim → Oracle (ayar.json hariç)"
rsync -az --rsync-path="sudo rsync" --exclude='ayar.json' --exclude='*.tmp' \
  "$MEDS_DIR/data/sesli_anlatim/" "medsor-oracle:/home/ubuntu/medsor/meds/data/sesli_anlatim/"

echo "==> [3/4] Oracle'da kuyruk düzeltmesi + işçi açık, ücretli kapalı"
ssh medsor-oracle 'sudo python3 - <<EOF
import json
k="/home/ubuntu/medsor/meds/data/sesli_anlatim"
q=json.load(open(k+"/kuyruk.json"))
for x in q:
    if x["durum"] in ("calisiyor",) or (x["durum"]=="kota-bekliyor" and "durduruldu" in (x.get("hata") or "")):
        x["durum"]="bekliyor"; x.pop("sonrakiDeneme",None); x.pop("hata",None)
json.dump(q,open(k+"/kuyruk.json","w"),ensure_ascii=False,indent=1)
json.dump({"isciAktif":True,"ucretliAktif":False},open(k+"/ayar.json","w"))
print("kuyruk:",len(q),"iş")
EOF
sudo chown -R root:root /home/ubuntu/medsor/meds/data/sesli_anlatim'

echo "==> [4/4] Oracle işçisi uyandırılıyor (yeniden başlatma gerekmez; döngü en geç 60 sn'de dosyayı okur)"
SECRET=$(grep '^MEDS_PANEL_SECRET=' "$MEDS_DIR/.env" | cut -d= -f2-)
curl -sf -X POST "https://api.nofrostlife.com.tr/api/sesli-anlatim/isci" "${HDR[@]}" -H "x-panel-secret: $SECRET" -d '{"aktif":true}' && echo
echo "Taşındı. Yerel işçi kapalı kalır (panel › Sesli anlatım › Başlat ile açılmamalı)."
