#!/usr/bin/env bash
# MedSoru tam yedek (YENI_YAPI_YOL_HARITASI F0/T1). Yalnız yeni dosya yazar; kaynakta hiçbir şeyi değiştirmez.
# Kullanım: deploy/backup.sh            → $MEDS_BACKUP_DIR/<YYYYMMDD_HHMM>/
#   MEDS_BACKUP_DIR   yedek kökü (varsayılan: <proje>/../medsor-yedek, cihazda /home/indu/medsor-yedek)
#   MEDS_DB_CONTAINER pg konteyneri (varsayılan: meds-pg)
#   MEDS_BACKUP_GPG_PASS_FILE  verilirse .env dosyaları gpg ile şifreli eklenir; verilmezse secret ATLANIR (K4 kararı bekliyor)
set -euo pipefail

APP="$(cd "$(dirname "$0")/.." && pwd)"          # meds/
ROOT="$(dirname "$APP")"                          # medsor/
DEST_ROOT="${MEDS_BACKUP_DIR:-$(dirname "$ROOT")/medsor-yedek}"
DEST="$DEST_ROOT/$(date +%Y%m%d_%H%M)"
DB="${MEDS_DB_CONTAINER:-meds-pg}"
mkdir -p "$DEST"
echo "[yedek] hedef: $DEST"

# 1) Veritabanı (özel biçim, pg_restore ile açılır)
if docker inspect "$DB" >/dev/null 2>&1; then
  echo "[yedek] pg_dump ($DB)…"
  docker exec "$DB" pg_dump -U meds -Fc meds > "$DEST/db.dump"
else
  echo "[yedek] UYARI: $DB konteyneri yok, DB atlandı"
fi

# 2) JSON çalışma verisi (local_rag_chunks.json yeniden üretilir → hariç)
echo "[yedek] data + src/data…"
tar -C "$APP" -czf "$DEST/data.tar.gz" --exclude='data/local_rag_chunks.json' data
tar -C "$APP" -czf "$DEST/src_data.tar.gz" --exclude='src/data/decks/items' src/data

# 3) Secret'lar yalnız şifreli
if [[ -n "${MEDS_BACKUP_GPG_PASS_FILE:-}" && -r "${MEDS_BACKUP_GPG_PASS_FILE}" ]]; then
  for f in "$APP/.env" "$APP/deploy/oracle/.env.oracle"; do
    [[ -f "$f" ]] || continue
    name="$(realpath --relative-to="$ROOT" "$f" | tr '/' '_')"
    gpg --batch --yes --pinentry-mode loopback --passphrase-file "$MEDS_BACKUP_GPG_PASS_FILE" \
        --symmetric --cipher-algo AES256 -o "$DEST/$name.gpg" "$f"
  done
else
  echo "[yedek] secret atlandı (MEDS_BACKUP_GPG_PASS_FILE yok)"
fi

# 4) Sayaç manifestosu + SHA256
python3 - "$APP" "$DB" > "$DEST/SAYAC.json" <<'PY'
import json, subprocess, sys
app, db = sys.argv[1], sys.argv[2]
def n(p):
    d = json.load(open(f"{app}/{p}"))
    return len(d) if isinstance(d, list) else len(d.get("questions", d.get("decks", d)))
def q(sql):
    try:
        return subprocess.run(["docker", "exec", db, "psql", "-U", "postgres", "-At", "-c", sql],
                              capture_output=True, text=True, timeout=60).stdout.strip()
    except Exception as e:
        return f"HATA: {e}"
out = {
    "pastQuestions_data": n("data/pastQuestions.json"),
    "pastQuestions_src": n("src/data/pastQuestions.json"),
    "questions_pool": n("data/questions.json"),
    "decks": n("src/data/interactive_learning_decks.json"),
    "db_rag_chunks": q("select count(*) from rag_chunks"),
    "db_rag_chunks_bge": q("select count(embedding_bge_m3) from rag_chunks"),
    "db_past_questions": q("select count(*) from past_questions"),
}
print(json.dumps(out, ensure_ascii=False, indent=2))
PY
(cd "$DEST" && sha256sum -- * > SHA256SUMS)
du -sh "$DEST"
cat "$DEST/SAYAC.json"
echo "[yedek] tamam: $DEST"
