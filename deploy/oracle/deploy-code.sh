#!/usr/bin/env bash
# deploy-code.sh — cihaz working tree'yi Oracle'a gönderir + doğrular (rsync yolu).
# Neden git değil: data/*.json git'te 350MB+, commitlenmemiş değişiklikler var;
# rsync çalışan ağacı birebir taşır. GitHub yedek/ortak çalışma için durur.
# Kullanım (cihazdan, meds/ içinde): ./deploy/oracle/deploy-code.sh [--build] [--imaj] [--derleme-yok]
set -euo pipefail

# Cihaz kilidi (2026-10-20): iki oturum aynı anda dağıtınca Oracle'da eşzamanlı derleme belleği tüketip
# sunucuyu düşürdü. Tüm çalışma ağaçları (meds, meds-dagitim, ...) aynı kilit dosyasını paylaşır; ikinci
# dağıtım beklemez, hemen durur. Kilit süreç bitince (çökse bile) çekirdek tarafından bırakılır.
if [ -z "${MEDS_DEPLOY_LOCKED:-}" ]; then
  exec 9>"${XDG_RUNTIME_DIR:-/tmp}/medsor-deploy.lock"
  if ! flock -n 9; then
    echo "DURDU: başka bir dağıtım sürüyor (kilit: ${XDG_RUNTIME_DIR:-/tmp}/medsor-deploy.lock). O bitince yeniden çalıştırın." >&2
    exit 75
  fi
  export MEDS_DEPLOY_LOCKED=1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MEDS_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
KEY="${SSH_KEY:-$HOME/.ssh/medsor-oracle.key}"
ORACLE_USER="${ORACLE_USER:-ubuntu}"
ORACLE_HOST="${ORACLE_HOST:-92.5.55.109}"
# Alt betikler (content-overlay-sync.sh, sync-*.sh) aynı hedefi görsün
export ORACLE_HOST ORACLE_USER
ORACLE_DIR="/home/ubuntu/medsor/meds"
SSH_BASIT="ssh -i $KEY -o StrictHostKeyChecking=no -o ConnectTimeout=15"
# Mod: değişen dosyalara göre kendiliğinden seçilir (2026-10-20, kod imaja gömülmez, ../..:/app bağlı):
#   yalnız dist/ / statik / içerik  → yalnız rsync (saniyeler; sayfa diskten sunulur)
#   sunucu kodu ya da src/data       → docker restart meds-app (~30 sn)
#   package*.json / Dockerfile / compose → imaj yeniden kurulur (nadir)
# --build: en az yeniden başlatma zorlar (eski kullanım) · --imaj: imajı zorla kurar · --derleme-yok: yerel vite build atlanır
FORCE=0; DO_IMAGE=0; SKIP_LOCAL_BUILD=0; KIRLI_IZIN=0
for a in "$@"; do case "$a" in
  --build) FORCE=1;; --imaj) DO_IMAGE=1;; --derleme-yok) SKIP_LOCAL_BUILD=1;; --kirli-izin) KIRLI_IZIN=1;;
  *) echo "bilinmeyen seçenek: $a"; exit 2;; esac; done

# Dağıtım düzeni (2026-10-20, kullanıcı kararı): kod yalnız commit'lenmiş + gönderilmiş hâlden, temiz worktree'den çıkar.
# Resmî yol: deploy/oracle/dagit.sh (origin/main → meds-dagitim → bu betik). Çalışma ağacından kirli dağıtım başka
# oturumların yarım işini canlıya taşıyor, canlıdaki daha yeni bir commit'i geri alıyordu.
if [[ "$KIRLI_IZIN" == "0" && -z "${MEDS_DAGIT_ONAYLI:-}" ]]; then
  KIRLI="$(cd "$MEDS_DIR" && git status --porcelain -- src ':!src/data' server.ts index.html vite.config.ts public package.json scripts/vite 2>/dev/null | head -5)"
  if [[ -n "$KIRLI" ]]; then
    echo "DURDU: çalışma ağacında commit'lenmemiş kod var — kirli dağıtım yapılmaz:" >&2
    echo "$KIRLI" | sed 's/^/    /' >&2
    echo "  Doğru yol: commit + push, sonra  bash deploy/oracle/dagit.sh   (acil durumda: --kirli-izin)" >&2
    exit 76
  fi
fi
if [[ "$KIRLI_IZIN" == "0" ]]; then
  CANLI="$($SSH_BASIT "$ORACLE_USER@$ORACLE_HOST" "python3 -c 'import json;print(json.load(open(\"$ORACLE_DIR/dist/dagitim.json\"))[\"commit\"])'" 2>/dev/null || true)"
  if [[ -n "$CANLI" ]] && ! (cd "$MEDS_DIR" && git merge-base --is-ancestor "$CANLI" HEAD 2>/dev/null); then
    echo "DURDU: canlıdaki commit ($CANLI) bu ağacın geçmişinde yok — dağıtım onu geri alırdı. Önce güncel origin/main'i alın" >&2
    echo "  (bash deploy/oracle/dagit.sh bunu kendisi yapar)." >&2
    exit 77
  fi
fi
SSH="ssh -i $KEY -o StrictHostKeyChecking=no -o ControlMaster=auto -o ControlPath=$HOME/.ssh/cm-deploy-%r@%h:%p -o ControlPersist=120"
T0=$(date +%s)

echo "==> [0/4] ders işçisi yayınları: Oracle'da yayınlanan dersler önce yerel kaynaklara işlenir"
# Oracle onaylanan dersleri kendisi yayınlar (yayinla.py --sunucu). Eşitlemeden rsync, o dersleri sitede eski
# hâline döndürürdü (Oracle sonraki turda kendini onarır ama arada ders kaybolur).
PY="$MEDS_DIR/.venv-ocr/bin/python"; [[ -x "$PY" ]] || PY=python3
"$PY" "$MEDS_DIR/scripts/ders_isci/yayinla.py" --esitle || { echo "DURDU: yayınlar eşitlenemedi (yukarıdaki çıktıya bakın)"; exit 1; }

echo "==> [0b/4] yönetim paneli değişiklikleri: Oracle data/content/ → yerel src/data (rsync ezmesin)"
"$SCRIPT_DIR/content-overlay-sync.sh" || { echo "DURDU: panel değişiklikleri eşitlenemedi (yukarıdaki çıktıya bakın)"; exit 1; }
if [[ "$SKIP_LOCAL_BUILD" == "0" ]]; then
  echo "==> [0c/4] yerel derleme (dist/ cihazda üretilir; Oracle ARM'de derleme yok)"
  (cd "$MEDS_DIR" && npm run build --silent >/dev/null) || { echo "DURDU: yerel derleme başarısız"; exit 1; }
fi
[[ -f "$MEDS_DIR/dist/index.html" ]] || { echo "DURDU: dist/index.html yok"; exit 1; }
# Dağıtım damgası (2026-10-20): gece içerik dağıtımı (otomasyon/icerik_dagit.py) canlıdaki kodu birebir yeniden
# derleyebilsin diye commit + commit'lenmemiş kod listesi dist/dagitim.json'a yazılır (src/data hariç: içerik).
( cd "$MEDS_DIR" && python3 - <<'PYEOF'
import json, subprocess, time
g = lambda *a: subprocess.run(["git", *a], capture_output=True, text=True).stdout.strip()
kirli = [l[3:] for l in g("status", "--porcelain", "--", "src", ":!src/data", "server.ts", "index.html", "vite.config.ts",
                         "public", "package.json", "scripts/vite").splitlines() if l.strip()]
json.dump({"commit": g("rev-parse", "HEAD"), "kirli": kirli, "zaman": time.strftime("%Y-%m-%dT%H:%M:%S")},
          open("dist/dagitim.json", "w"), ensure_ascii=False)
PYEOF
) || echo "  UYARI: dağıtım damgası yazılamadı"

echo "==> [1/4] rsync kod + dist (src/data DAHİL, .env HARİÇ; içerik karşılaştırması)"
CHANGED="$(mktemp)"; trap 'rm -f "$CHANGED"' EXIT
# --checksum: değişiklik listesi içeriğe göre (worktree checkout'u tarihleri yeniler; tarihe bakınca package.json
# 'değişti' sayılıp imaj gereksiz kuruluyordu, 2026-10-20). Ölçüm: ~2 sn.
# sudo rsync: konteyner src/data'ya root olarak yazar; tarih/sahip eşitlemesi yetki ister (sahip uid 1000 olur)
rsync -az --checksum --rsync-path='sudo rsync' --out-format='%i %n' \
  --exclude='/node_modules' --exclude='/dist-gh' \
  --exclude='/data' --exclude='/.git' --exclude='/models' \
  --exclude='/training_data' --exclude='/linux' \
  --exclude='.venv*' --exclude='__pycache__' --exclude='*.log' \
  --exclude='/cloudflared.exe' \
  --exclude='/.env' --exclude='/.env.*' --exclude='*.bak' --exclude='*.bak_*' --exclude='*.backup*' \
  --exclude='/get-pip.py' --exclude='/.agents' --exclude='/.claude' --exclude='/.github' \
  --exclude='/scripts/archive' --exclude='/scripts/semantic/data' \
  -e "$SSH" "$MEDS_DIR/" "$ORACLE_USER@$ORACLE_HOST:$ORACLE_DIR/" > "$CHANGED"
# Yalnız içeriği aktarılan dosyalar (>f); tarih/sahip eşitlemesi (.f..t..) yeniden başlatma sebebi değil
sed -n 's/^>f[^ ]* //p' "$CHANGED" > "$CHANGED.f" || true; mv "$CHANGED.f" "$CHANGED"
echo "  $(wc -l < "$CHANGED") dosya aktarıldı"

echo "==> [1b/4] sesli ders verisi (metin/hizalama/vurgu → Oracle data/sesli_anlatim)"
# data/ yukarıda dışlanır; bu dört klasör metinle birlikte değişmezse canlıda paragraf/cümle zamanlaması ve PDF
# eşlemesi kullanılamaz (2026-10-20: eski metin yüzünden 55 ses kaydı zamanlamasız kaldı). Ses dosyaları ve kayit.json
# Oracle'da üretilip yönetildiği için gönderilmez; cumle_zaman/ de Oracle'da meds-cumle-zaman.timer ile üretilir
# (yereldeki eski kopya onu ezmesin). Commit'lenmemiş değişikliği olan klasör (başka oturumun yarım işi) atlanır.
SA="data/sesli_anlatim"
for k in metin hizalama vurgu capa ogrenci_not; do
  [[ -d "$MEDS_DIR/$SA/$k" ]] || continue
  if [[ -n "$(git -C "$MEDS_DIR" status --porcelain -- "$SA/$k" 2>/dev/null)" ]]; then
    echo "  ATLANDI $k: commit'lenmemiş değişiklik var (önce commit edin)"; continue
  fi
  n=$(rsync -az --checksum --rsync-path='sudo rsync' --out-format='%i %n' -e "$SSH" \
    "$MEDS_DIR/$SA/$k/" "$ORACLE_USER@$ORACLE_HOST:$ORACLE_DIR/$SA/$k/" | grep -c '^>f' || true)
  echo "  $k: $n dosya"
done
# Son Prova kırpılmış özet PDF'leri (git dışı; scripts/son_prova/pdf_kirp.mjs üretir, hizalama sayfa numaraları bunlara bağlı)
if [[ -d "$MEDS_DIR/data/son_prova/pdf" ]]; then
  $SSH "$ORACLE_USER@$ORACLE_HOST" "sudo mkdir -p $ORACLE_DIR/data/son_prova/pdf"
  n=$(rsync -az --checksum --rsync-path='sudo rsync' --out-format='%i %n' -e "$SSH" \
    "$MEDS_DIR/data/son_prova/pdf/" "$ORACLE_USER@$ORACLE_HOST:$ORACLE_DIR/data/son_prova/pdf/" | grep -c '^>f' || true)
  echo "  son_prova/pdf: $n dosya"
fi

if grep -qE '^(package(-lock)?\.json|deploy/oracle/(Dockerfile\.oracle|docker-compose\.oracle\.yml))$' "$CHANGED"; then DO_IMAGE=1; fi
# Sunucunun belleğe aldığı her şey: dist/, public/, ön yüz bileşenleri, belgeler dışındaki her değişiklik
NEED_RESTART=$FORCE
if grep -vE '^(dist/|public/|docs/|src/(components|screens|styles|pages)/|.*\.(tsx|css|md)$|guncelleme_notu\.json$|deploy/)' "$CHANGED" | grep -q .; then NEED_RESTART=1; fi
# Sunucu kodu karması (2026-10-20): değişen dosya listesi yetmez — dosya Oracle'a başka bir yoldan (tek dosya rsync,
# başka oturum) yeniden başlatmasız gelmiş olabilir; rsync saat damgasını da korur. Çalışan sunucunun yüklediği kodun
# karması her yeniden başlatmada .sunucu_kod_karma'ya yazılır; Oracle'daki kodun karması farklıysa yeniden başlat.
# Sunucunun açılışta içe aktardığı kural verisi de karmaya girer (2026-10-21): başarım tanımı, kurul takvimi, ders kayıt
# defteri — yalnız bunlar değişse de meds-app yeniden başlar (önceden elle `docker restart meds-app` gerekiyordu).
KOD_KARMA_KOMUT="cd $ORACLE_DIR && find server.ts src/services src/serverLectureNotes.ts src/config src/types src/data/basarim src/data/dersler src/data/kurul_takvimi_ozet.json -type f \( -name '*.ts' -o -name '*.json' \) 2>/dev/null | LC_ALL=C sort | xargs sha256sum | sha256sum | cut -c1-16"
UZAK_KARMA="$($SSH "$ORACLE_USER@$ORACLE_HOST" "$KOD_KARMA_KOMUT" 2>/dev/null || true)"
YUKLU_KARMA="$($SSH "$ORACLE_USER@$ORACLE_HOST" "cat $ORACLE_DIR/.sunucu_kod_karma 2>/dev/null" || true)"
if [[ -n "$UZAK_KARMA" && "$UZAK_KARMA" != "$YUKLU_KARMA" ]]; then
  echo "  sunucu kodu çalışan sürümden farklı ($YUKLU_KARMA → $UZAK_KARMA) — yeniden başlatılacak"; NEED_RESTART=1
fi

echo "==> [2/4] bütünlük: kritik dosya md5 karşılaştırma"
KRITIK="deploy/oracle/docker-compose.oracle.yml deploy/oracle/Dockerfile.oracle server.ts package.json dist/index.html"
yerel=$(cd "$MEDS_DIR" && md5sum $KRITIK)
uzak=$($SSH "$ORACLE_USER@$ORACLE_HOST" "cd $ORACLE_DIR && md5sum $KRITIK")
if [[ "$yerel" == "$uzak" ]]; then echo "  OK ($(echo $KRITIK | wc -w) dosya)"; else echo "  HATA uyuşmuyor:"; diff <(echo "$yerel") <(echo "$uzak"); exit 1; fi

C="docker compose --env-file $ORACLE_DIR/.env -f deploy/oracle/docker-compose.oracle.yml"
if [[ "$DO_IMAGE" == "1" ]]; then
  echo "==> [3/4] imaj (yalnız bağımlılıklar) + başlat (kapı yeniden başlatma süresince istekleri bekletir)"
  $SSH "$ORACLE_USER@$ORACLE_HOST" "cd $ORACLE_DIR && [ ! -e node_modules ] || echo '  UYARI: sunucuda meds/node_modules var, /node_modules gölgelenir'; flock /tmp/meds-deploy.lock sh -c '
    $C build -q meds-app && $C up -d --no-deps meds-app && $C up -d --no-deps meds-server'"
elif [[ "$NEED_RESTART" == "1" ]]; then
  echo "==> [3/4] sunucu kodu/veri değişti → meds-app yeniden başlatılıyor"
  $SSH "$ORACLE_USER@$ORACLE_HOST" "flock /tmp/meds-deploy.lock docker restart -t 20 meds-app >/dev/null"
else
  echo "==> [3/4] yalnız ön yüz/statik → yeniden başlatma yok (dist/ diskten anında sunulur)"
fi

if [[ "$NEED_RESTART" == "1" || "$DO_IMAGE" == "1" ]]; then  # yüklenen kodun karması (bir sonraki dağıtım karşılaştırır)
  $SSH "$ORACLE_USER@$ORACLE_HOST" "$KOD_KARMA_KOMUT > /tmp/.sunucu_kod_karma.tmp && cat /tmp/.sunucu_kod_karma.tmp > $ORACLE_DIR/.sunucu_kod_karma && rm -f /tmp/.sunucu_kod_karma.tmp" || true
fi
echo "==> [4/4] sağlık kontrolü (kapı üzerinden, en çok 120 sn)"
$SSH "$ORACLE_USER@$ORACLE_HOST" 'for i in $(seq 1 60); do curl -sf -m 5 http://127.0.0.1:3000/api/health && exit 0; sleep 2; done; echo "sağlık kontrolü geçmedi"; docker logs meds-app --tail 40; exit 1' | head -c 2000
echo
if [[ "$NEED_RESTART" == "1" || "$DO_IMAGE" == "1" ]]; then
  echo "==> [5/5] arama paketi + hastalık grafiği (AYRI konteynerde, arka planda; imza aynıysa ~1 sn)"
  # Yalnız son komut arka plana atılır (önceki 'a && b && nohup … &' tüm zinciri atıp SSH'ı açık tutuyordu, 2026-10-18)
  # meds-app 3 GB tavanında derlemez (bellek koruması); derleme 2 GB sınırlı tek seferlik konteynerde
  $SSH "$ORACLE_USER@$ORACLE_HOST" "cd $ORACLE_DIR; mkdir -p deploy/oracle/logs; setsid nohup ./deploy/oracle/build-search.sh </dev/null > deploy/oracle/logs/build-search.log 2>&1 &"
fi
echo "BİTTİ. ($(( $(date +%s) - T0 )) sn)"
