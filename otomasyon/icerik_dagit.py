#!/usr/bin/env python3
"""Gece içerik dağıtımı: Oracle'da yayımlanan dersler + yerel zincir çıktıları → temiz derleme → yalnız dist Oracle'a.

Neden: Oracle'da ön yüz derlenmez (dist cihazda üretilir, 2026-10-20). Ders işçisinin Oracle'da yayımladığı deste/örnek
soru/sözlük ve ders zincirinin yerelde ürettiği k<N><brans>_onem|_cozucu|_asistan verisi ön yüz paketine gömülüdür;
derlenip dist gönderilmeden sitede görünmez.

Güvenlik: çalışma ağacından DERLENMEZ (başka oturumların yarım ön yüz işi pakete girerdi). Akış:
  1. origin/main'in son commit'inden geçici git worktree (node_modules ana ağaçtan bağlanır)
  2. Oracle src/data → worktree src/data (yayımlanan içeriğin asıl yeri Oracle'dır; salt-okunur çekilir)
  3. yerel zincir çıktıları (src/data/k[2-6]*_onem|_cozucu|_asistan, cozucu_ogren) → worktree + Oracle src/data
  4. vite build (worktree) → dist rsync (silmeden; eski parçalar açık sekmeler için kalır) → sağlık + sürüm denetimi
Değişiklik yoksa (girdi karması aynı) hiçbir şey yapılmaz. Cihaz dağıtım kilidini paylaşır (deploy-code.sh ile çakışmaz).
Kod commit'i ya da guncelleme_notu artırımı YAPMAZ: yalnız içerik; "Siteyi güncelle" diyaloğu çıkmaz, yeni içerik
sonraki açılışta sessizce yüklenir (guncelleme_notu.json _aciklama kuralı).
  icerik_dagit.py [--kuru] [--zorla]
"""
import argparse, fcntl, hashlib, json, os, shutil, subprocess, sys, tempfile, time
from pathlib import Path

MEDS = Path(__file__).resolve().parents[1]; KOK = MEDS.parent
DURUM = KOK / "meds_temp/hat/icerik_dagit.json"
UZAK = "medsor-oracle:/home/ubuntu/medsor/meds"
KILIT = Path(os.environ.get("XDG_RUNTIME_DIR", "/tmp")) / "medsor-deploy.lock"


def sh(kom, **k):
    print("   $", kom if isinstance(kom, str) else " ".join(map(str, kom)))
    return subprocess.run(kom, shell=isinstance(kom, str), **k)


def zincir_klasorleri():
    d = MEDS / "src/data"
    return sorted([p for p in d.glob("k[2-6]*_onem")] + [p for p in d.glob("k[2-6]*_cozucu")] +
                  [p for p in d.glob("k[2-6]*_asistan")] + ([d / "cozucu_ogren"] if (d / "cozucu_ogren").exists() else []))


def karma(dizinler):
    h = hashlib.sha256()
    for k in dizinler:
        for p in sorted(Path(k).rglob("*")) if Path(k).is_dir() else [Path(k)]:
            if p.is_file():
                h.update(str(p.relative_to(k)).encode()); h.update(p.read_bytes())
    return h.hexdigest()[:20]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--kuru", action="store_true"); ap.add_argument("--zorla", action="store_true")
    a = ap.parse_args()
    kilit = open(KILIT, "w")
    try:
        fcntl.flock(kilit, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("başka dağıtım sürüyor; sonraki gece"); return 0
    # Başka bir oturum çalışma ağacından (commit'lenmemiş ön yüz koduyla) dağıttıysa, temiz commit'ten derlemek onun
    # canlıdaki işini geri alır: ön yüz/sunucu kodunda commit'lenmemiş değişiklik varken içerik dağıtımı yapılmaz.
    kirli = subprocess.run(["git", "-C", str(MEDS), "status", "--porcelain", "--", "src", ":!src/data", "server.ts",
                            "index.html", "vite.config.ts", "public"], capture_output=True, text=True).stdout.strip()
    ileri = subprocess.run(["git", "-C", str(MEDS), "rev-list", "--count", "origin/main..HEAD"], capture_output=True, text=True).stdout.strip()
    if (kirli or ileri not in ("", "0")) and not a.zorla:
        print("ATLANDI: çalışma ağacında commit'lenmemiş/gönderilmemiş kod var; canlı sürüm ondan dağıtılmış olabilir:")
        print("  " + "\n  ".join((kirli.splitlines() + ([f"{ileri} commit gönderilmemiş"] if ileri not in ("", "0") else []))[:10]))
        return 3
    tmp = Path(tempfile.mkdtemp(prefix="medsor-icerik-"))
    wt = tmp / "wt"
    try:
        sh(["git", "-C", str(MEDS), "fetch", "-q", "origin", "main"], check=True)
        sh(["git", "-C", str(MEDS), "worktree", "add", "-q", "--detach", str(wt), "origin/main"], check=True)
        # meds/ deponun kökü değilse worktree içinde meds alt klasörü olur
        wm = wt / "meds" if (wt / "meds" / "package.json").exists() else wt
        (wm / "node_modules").symlink_to(MEDS / "node_modules")
        r = sh(["rsync", "-az", "--exclude=decks/items", f"{UZAK}/src/data/", f"{wm}/src/data/"], timeout=900)
        if r.returncode:
            print("HATA: Oracle src/data çekilemedi"); return 1
        for k in zincir_klasorleri():
            sh(["rsync", "-a", f"{k}/", f"{wm}/src/data/{k.name}/"], check=True)
        oz = karma([wm / "src/data"]) + sh(["git", "-C", str(wt), "rev-parse", "--short", "HEAD"],
                                            capture_output=True, text=True).stdout.strip()
        onceki = json.loads(DURUM.read_text()).get("karma") if DURUM.exists() else None
        if oz == onceki and not a.zorla:
            print("içerik ve kod değişmedi; dağıtım yok"); return 0
        if a.kuru:
            print("kuru: derleme ve gönderim atlandı"); return 0
        r = sh("nice -n 10 npx vite build", cwd=wm, shell=True, capture_output=True, text=True, timeout=1800,
               env={**os.environ, "CUDA_VISIBLE_DEVICES": ""})
        if r.returncode or not (wm / "dist/index.html").exists():
            print("HATA: derleme:", (r.stderr or r.stdout)[-1500:]); return 1
        for k in zincir_klasorleri():  # Oracle src/data da güncel kalsın (sonraki tam dağıtım/eşitleme için)
            sh(["rsync", "-az", "--rsync-path=sudo rsync", f"{k}/", f"{UZAK}/src/data/{k.name}/"], check=True)
        r = sh(["rsync", "-az", "--rsync-path=sudo rsync", f"{wm}/dist/", f"{UZAK}/dist/"], timeout=900)
        if r.returncode:
            print("HATA: dist gönderilemedi"); return 1
        time.sleep(3)
        s = subprocess.run(["curl", "-s", "-m", "20", "https://api.nofrostlife.com.tr/api/surum"], capture_output=True, text=True).stdout
        ok = '"surum"' in s
        DURUM.parent.mkdir(parents=True, exist_ok=True)
        DURUM.write_text(json.dumps({"karma": oz, "zaman": time.strftime("%Y-%m-%dT%H:%M:%S"), "surum": s[:200]}, ensure_ascii=False))
        print("dağıtıldı:", s[:120] if ok else "sürüm okunamadı!")
        return 0 if ok else 1
    finally:
        subprocess.run(["git", "-C", str(MEDS), "worktree", "remove", "--force", str(wt)], capture_output=True)
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
