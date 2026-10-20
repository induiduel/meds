#!/usr/bin/env python3
"""Hastalık zinciri: ders işçisi önerileri (Oracle) → Claude şema 2 → diseases.json birleştirme (kapılı) → canlı katman.

  1. Oracle'dan meds_database_v2/ders_isci/hastalik_onerileri/*.json salt-okunur çekilir (silme yok).
  2. Şema 2'ye çevrilmemiş (ya da önerisi değişmiş) her ders için Claude: scripts/diseases/TALIMAT_SEMA2.md → sema2/<id>.json
  3. yayinla.hastaliklari_uygula(): diseases.json'a upsert; başka oturum diseases.json'u değiştiriyorsa BEKLER; denetim
     hatası artarsa geri alır (yedek meds_temp/…).
  4. Değişen diseases.json → Oracle data/content/diseases.json (canlı katman) + POST /api/admin/icerik/diseases/degisti
     (Oracle loopback, yönetici) → SSE content_changed. Bir sonraki dağıtım katmanı src/data'ya zaten geri çeker.
Durum: meds_temp/hat/hastalik_zinciri.json {ders_id: öneri sha}. LLM yalnız Claude (kullanıcı kararı 2026-10-20).
  hastalik_zinciri.py [--kuru] [--en-cok 4]
"""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path

MEDS = Path(__file__).resolve().parents[1]; KOK = MEDS.parent
ONERI = KOK / "meds_database_v2/ders_isci/hastalik_onerileri"
DURUM = KOK / "meds_temp/hat/hastalik_zinciri.json"
DIS = MEDS / "src/data/diseases.json"
IZIN = "Read,Write,Edit,Glob,Grep,Bash(python3 *)"


def sha(p):
    return hashlib.sha1(p.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--kuru", action="store_true"); ap.add_argument("--en-cok", type=int, default=4)
    a = ap.parse_args()
    ONERI.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["rsync", "-az", "--include=*.json", "--exclude=*/", "--exclude=sema2",
                        "medsor-oracle:/home/ubuntu/medsor/meds_database_v2/ders_isci/hastalik_onerileri/", f"{ONERI}/"],
                       capture_output=True, text=True, timeout=300)
    if r.returncode:
        print("HATA: öneriler Oracle'dan çekilemedi:", r.stderr.strip()[:300]); return 1
    durum = json.loads(DURUM.read_text()) if DURUM.exists() else {}
    bekleyen = [p for p in sorted(ONERI.glob("k*.json")) if durum.get(p.stem) != sha(p)][: a.en_cok]
    print(f"{len(bekleyen)} ders önerisi şema 2 bekliyor")
    for p in bekleyen:
        istem = (f"{MEDS}/scripts/diseases/TALIMAT_SEMA2.md talimatını uygula. Girdi: {p}. Çıktı klasörü: {ONERI}/sema2/. "
                 f"Proje kökü {KOK}.")
        print("▶", p.stem)
        if a.kuru:
            continue
        (ONERI / "sema2").mkdir(exist_ok=True)
        with open(KOK / "meds_temp/hat/hastalik_claude.log", "a") as log:
            k = subprocess.run(["claude", "-p", istem, "--model", "claude-opus-5-5", "--allowedTools", IZIN, "--add-dir", str(KOK)],
                               cwd=KOK, stdout=log, stderr=subprocess.STDOUT, timeout=3 * 3600).returncode
        if k == 0:
            durum[p.stem] = sha(p); DURUM.parent.mkdir(parents=True, exist_ok=True)
            DURUM.write_text(json.dumps(durum, ensure_ascii=False, indent=1))
    if a.kuru:
        return 0
    once = sha(DIS); onceki = {d["id"]: json.dumps(d, sort_keys=True) for d in json.loads(DIS.read_text())}
    sys.path.insert(0, str(MEDS / "scripts/ders_isci")); import yayinla
    yayinla.hastaliklari_uygula()
    if sha(DIS) == once:
        print("diseases.json değişmedi"); return 0
    ids = [d["id"] for d in json.loads(DIS.read_text()) if onceki.get(d["id"]) != json.dumps(d, sort_keys=True)]
    r = subprocess.run(["rsync", "-az", "--rsync-path=sudo rsync", str(DIS),
                        "medsor-oracle:/home/ubuntu/medsor/meds/data/content/diseases.json"], timeout=120)
    if r.returncode:
        print("HATA: canlı katmana gönderilemedi"); return 1
    govde = json.dumps({"ids": ids})
    # Oracle'da /api yazmaları loopback'ten de parola ister: parola ve panel sırrı sunucunun .env'inden okunur
    uzak = ("cd /home/ubuntu/medsor/meds && PW=$(grep -m1 '^MEDSORU_API_PASSWORD=' .env | cut -d= -f2-) && "
            "PS=$(grep -m1 '^MEDS_PANEL_SECRET=' .env | cut -d= -f2-) && "
            "curl -s -X POST -H 'Content-Type: application/json' -H \"X-API-Password: $PW\" -H \"x-panel-secret: $PS\" "
            f"--data '{govde}' http://127.0.0.1:3000/api/admin/icerik/diseases/degisti")
    r = subprocess.run(["ssh", "medsor-oracle", uzak],
                       capture_output=True, text=True, timeout=60)
    print(f"canlı: {len(ids)} hastalık kaydı → {r.stdout.strip()[:160]}")
    return 0 if '"success":true' in r.stdout else 1


if __name__ == "__main__":
    sys.exit(main())
