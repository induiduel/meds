#!/usr/bin/env python3
"""meds-pg şema göç koşucusu (GELECEK_PLANLAMASI §6). Yerel ve Oracle'da aynı sırayla, bir kez.

Göçler: deploy/pg/sql/goc/NNNN_ad.sql — numaralı, idempotent (CREATE ... IF NOT EXISTS, ADD COLUMN IF NOT EXISTS).
Kural: göç yalnız EKLER (tablo/kolon/indeks/işlev). Kolon silme ya da anlam değiştirme yok; ad değişikliği = yeni kolon +
geçiş dönemi. Böylece eski site sürümü yeni şemayla, yeni sürüm eski veriyle çalışır.
Kayıt: schema_migrations(no, ad, sha, uygulandi). Uygulanmış bir göçün dosyası sonradan değişirse UYARI (yeniden çalıştırılmaz;
düzeltme yeni numaralı göçle yapılır).

Kök SQL dosyaları (deploy/pg/sql/*.sql: realtime, user_data, …) sunucu açılışında ya da elle uygulanmaya devam eder; goc/0001
bunları taban olarak kaydeder (içerik yeniden çalıştırılmaz, yalnız idempotent oldukları için güvenle --uygula da edilebilir).

  goc.py --durum [--oracle]
  goc.py --uygula [--oracle] [--kuru]
"""
import argparse, hashlib, re, subprocess, sys
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
GOC = MEDS / "deploy/pg/sql/goc"
PSQL = ["docker", "exec", "-i", "meds-pg", "psql", "-U", "meds", "-d", "meds", "-v", "ON_ERROR_STOP=1", "-q"]
TABLO = """CREATE TABLE IF NOT EXISTS schema_migrations (
  no integer PRIMARY KEY, ad text NOT NULL, sha text NOT NULL, uygulandi timestamptz NOT NULL DEFAULT now());"""


def psql(sql, oracle, tA=False):
    kom = PSQL + (["-tA"] if tA else []) + ["-c", sql] if not sql.startswith("@") else PSQL
    if oracle:
        kom = ["ssh", "-o", "ConnectTimeout=15", "medsor-oracle", " ".join(_tirnak(k) for k in kom)]
    girdi = Path(sql[1:]).read_text() if sql.startswith("@") else None
    r = subprocess.run(kom, input=girdi, capture_output=True, text=True, timeout=600)
    if r.returncode:
        raise SystemExit(f"psql hatası ({'oracle' if oracle else 'yerel'}): {r.stderr.strip()[:500]}")
    return r.stdout


def _tirnak(s):
    return "'" + s.replace("'", "'\\''") + "'" if re.search(r"[^\w./=:-]", s) else s


def gocler():
    out = []
    for p in sorted(GOC.glob("*.sql")):
        m = re.match(r"(\d{4})_([\w-]+)\.sql$", p.name)
        if not m:
            raise SystemExit(f"HATA göç adı NNNN_ad.sql olmalı: {p.name}")
        out.append((int(m.group(1)), m.group(2), hashlib.sha256(p.read_bytes()).hexdigest()[:16], p))
    nos = [g[0] for g in out]
    if len(set(nos)) != len(nos):
        raise SystemExit("HATA aynı numaralı iki göç var")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--durum", action="store_true"); ap.add_argument("--uygula", action="store_true")
    ap.add_argument("--oracle", action="store_true"); ap.add_argument("--kuru", action="store_true")
    a = ap.parse_args()
    hedef = "Oracle" if a.oracle else "yerel"
    psql(TABLO, a.oracle)
    yapilan = {int(no): (ad, sha) for no, ad, sha in
               (ln.split("|") for ln in psql("SELECT no, ad, sha FROM schema_migrations ORDER BY no", a.oracle, True).split("\n") if ln)}
    bekleyen = []
    for no, ad, sha, p in gocler():
        if no in yapilan:
            if yapilan[no][1] != sha:
                print(f"UYARI {no:04d}_{ad}: uygulandıktan sonra dosya değişmiş (yeniden çalıştırılmaz; yeni göç yazın)")
            elif a.durum:
                print(f"  ✓ {no:04d}_{ad}")
        else:
            bekleyen.append((no, ad, sha, p))
    for no, ad, _, _ in bekleyen:
        print(f"  … {no:04d}_{ad} bekliyor ({hedef})")
    if a.uygula:
        for no, ad, sha, p in bekleyen:
            print(f"▶ {no:04d}_{ad} → {hedef}")
            if a.kuru:
                continue
            psql("@" + str(p), a.oracle)
            psql(f"INSERT INTO schema_migrations(no, ad, sha) VALUES ({no}, '{ad}', '{sha}') ON CONFLICT (no) DO NOTHING", a.oracle)
    print(f"{hedef}: {len(yapilan)} uygulanmış · {len(bekleyen)} bekleyen" + (" (uygulandı)" if a.uygula and not a.kuru else ""))


if __name__ == "__main__":
    main()
