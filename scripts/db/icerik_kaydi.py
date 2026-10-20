#!/usr/bin/env python3
"""İçerik seti kaydı (icerik_setleri, göç 0001): üretici bir ürünü bitirince çağırır. Kaynak karması öncekiyle
aynıysa yeni sürüm açılmaz. Yerel meds-pg'ye yazar; --oracle ile Oracle'a da.
  icerik_kaydi.py --kimlik k2-07 --tur onem --kaynak-sha abc --yol src/data/k2noroloji_onem/2n03.json [--kurul 2] [--ozet '{"madde":40}'] [--oracle]
"""
import argparse, json, subprocess, sys

PSQL = ["docker", "exec", "-i", "meds-pg", "psql", "-U", "meds", "-d", "meds", "-v", "ON_ERROR_STOP=1", "-tAq"]


def lit(s):
    return "NULL" if s is None else "'" + str(s).replace("'", "''") + "'"


def kaydet(kimlik, tur, kaynak_sha, yol, kurul=None, ozet=None, oracle=False):
    sql = f"""INSERT INTO icerik_setleri (kimlik, tur, surum, kurul, kaynak_sha, yol, ozet)
SELECT {lit(kimlik)}, {lit(tur)}, COALESCE(MAX(surum), 0) + 1, {kurul if kurul else 'NULL'}, {lit(kaynak_sha)}, {lit(yol)}, {lit(json.dumps(ozet or {}, ensure_ascii=False))}::jsonb
FROM icerik_setleri WHERE kimlik = {lit(kimlik)} AND tur = {lit(tur)}
HAVING COALESCE((SELECT kaynak_sha FROM icerik_setleri_son WHERE kimlik = {lit(kimlik)} AND tur = {lit(tur)}), '') <> COALESCE({lit(kaynak_sha)}, '')
RETURNING surum;"""
    hedefler = [False] + ([True] if oracle else [])
    out = []
    for o in hedefler:
        kom = PSQL if not o else ["ssh", "-o", "ConnectTimeout=15", "medsor-oracle", " ".join(PSQL)]
        r = subprocess.run(kom, input=sql, capture_output=True, text=True, timeout=60)
        if r.returncode:
            print(f"içerik kaydı yazılamadı ({'oracle' if o else 'yerel'}): {r.stderr.strip()[:200]}", file=sys.stderr)
            return 1
        out.append(r.stdout.strip() or "aynı")
    print(f"{kimlik}/{tur}: sürüm {' · '.join(out)}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    for k in ("--kimlik", "--tur", "--kaynak-sha", "--yol", "--ozet"): ap.add_argument(k)
    ap.add_argument("--kurul", type=int); ap.add_argument("--oracle", action="store_true")
    a = ap.parse_args()
    sys.exit(kaydet(a.kimlik, a.tur, a.kaynak_sha, a.yol, a.kurul, json.loads(a.ozet) if a.ozet else None, a.oracle))
