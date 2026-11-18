#!/usr/bin/env bash
# sesli_cek.sh — Oracle'da yayınlanan sesli dersleri YEREL sunucuya (3000) çeker (2026-11-18).
#
# Kök neden: sesli dersler Oracle'da yayınlanır (ders_ekle / sesli_yayinla.py → Oracle API; yayinla.py --sunucu) ve
# kod dağıtımı /data'yı taşımaz. Yerel data/sesli_anlatim/dersler.json Oracle'ın 61 ders gerisindeydi, MP3'ler (kayit.json +
# ses/) yerelde yoktu → yerel /api/canli-ders/<key> "ders yok" (404) diyordu; MEDS_API varsayılanı yerel olan betikler
# (pdf_isaret, terim, kısaltma …) yeni derste çalışamıyordu.
#
# Yön: YALNIZ Oracle → yerel. Kayıt defterleri anahtar bazında birleştirilir (sesli_cek_birlestir.py): Oracle'daki kayıt
# kazanır, yalnız yerelde olan kayıt korunur (başka oturumun yayınlanmamış işi silinmez). Dosyalar --ignore-existing ile:
# YALNIZ yerelde olmayan dosya gelir (yeni ders, yeni ses varyantı). Yerelde var olan dosya ezilmez — git'te izlenen metin/çapa
# gibi dosyalarda yerel ağaç (ve başka oturumların commit'lenmemiş işi) esastır; ilk ölçümde 1.573 dosya bu yüzden dışarıda.
# Hiçbir şey silinmez. Çalışma/kilit dosyaları (kuyruk, bütçe, ayar, gpu.lock, gunluk/) çekilmez.
#
# Kullanım: bash deploy/oracle/sesli_cek.sh [--kuru]     (dagit.sh dağıtımın sonunda çağırır; atlamak için MEDS_DAGIT_CEK=0)
# Sonra yerel sunucu yeniden başlatılmaz: canliDers.ts kayıt defterlerini boyut+mtime önbelleğiyle okur.
set -euo pipefail
ANA="$(cd "$(dirname "$0")/../.." && pwd)"
KURU=""; [[ "${1:-}" == "--kuru" ]] && KURU="-n"
KEY="${SSH_KEY:-$HOME/.ssh/medsor-oracle.key}"
HOST="ubuntu@${ORACLE_HOST:-92.5.55.109}"
SSHC="ssh -i $KEY -o StrictHostKeyChecking=accept-new -o ConnectTimeout=15"
UZAK=/home/ubuntu/medsor/meds
GECICI="$(mktemp -d)"; trap 'rm -rf "$GECICI"' EXIT

echo "==> sesli dersler Oracle → yerel${KURU:+ (KURU)}"
for kok in data/sesli_anlatim data/arsiv_25_26/sesli_anlatim; do
  $SSHC "$HOST" "test -d $UZAK/$kok" || continue
  mkdir -p "$ANA/$kok"
  # 1) kayıt defterleri: geçiciye indir, anahtar bazında birleştir
  for f in dersler.json kayit.json; do
    if rsync -a -e "$SSHC" "$HOST:$UZAK/$kok/$f" "$GECICI/${kok//\//_}_$f" 2>/dev/null; then
      python3 "$ANA/deploy/oracle/sesli_cek_birlestir.py" "$f" "$ANA/$kok/$f" "$GECICI/${kok//\//_}_$f" ${KURU:+--kuru}
    fi
  done
  # 2) içerik ve ses dosyaları: yalnız eksik/eski olanlar
  OUT="$(rsync -a $KURU --ignore-existing --itemize-changes -e "$SSHC" \
    --exclude='/dersler.json' --exclude='/kayit.json' --exclude='/kuyruk.json' --exclude='/butce.json' --exclude='/ayar.json' \
    --exclude='/yerel_plan.json' --exclude='*.lock' --exclude='*.tmp' --exclude='/gunluk/' --exclude='/_arsiv*/' --exclude='*.bak*' --exclude='*.yedek*' \
    "$HOST:$UZAK/$kok/" "$ANA/$kok/")"
  echo "    $kok: $(grep -c '^[>c]f' <<<"$OUT" || true) dosya"
done
