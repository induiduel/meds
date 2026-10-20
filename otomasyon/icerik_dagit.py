#!/usr/bin/env python3
"""Gece içerik dağıtımı: Oracle'da yayımlanan dersler + yerel zincir çıktıları → temiz derleme → yalnız dist Oracle'a.

Neden: Oracle'da ön yüz derlenmez (dist cihazda üretilir, 2026-10-20). Ders işçisinin Oracle'da yayımladığı deste/örnek
soru/sözlük ve ders zincirinin yerelde ürettiği k<N><brans>_onem|_cozucu|_asistan verisi ön yüz paketine gömülüdür;
derlenip dist gönderilmeden sitede görünmez.

Güvenlik: çalışma ağacından DERLENMEZ; canlıdaki kod birebir yeniden üretilir. Akış:
  1. Oracle dist/dagitim.json (deploy-code.sh yazar): dağıtılan commit + o anki commit'lenmemiş kod. Kirliyse ATLA (3).
  2. O commit'ten geçici git worktree; Oracle src/data birebir + panel katmanı (data/content) üstüne
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
    ek = [d / "cozucu_ogren", d / "kamp"] + sorted((d / "patoloji_checkup").glob("k[2-6]"))  # Öğren eşlemesi, kamp, Check Up K2+
    return sorted([p for p in d.glob("k[2-6]*_onem")] + [p for p in d.glob("k[2-6]*_cozucu")] +
                  [p for p in d.glob("k[2-6]*_asistan")] + [p for p in ek if p.exists()])


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
    # Canlıdaki kodu birebir yeniden üret: deploy-code.sh dist/dagitim.json'a dağıtılan commit'i ve o anki
    # commit'lenmemiş kod listesini yazar. Kirli dağıtılmışsa canlı kod yeniden üretilemez → ATLA (yanlış kodu dağıtma).
    r = subprocess.run(["ssh", "-o", "ConnectTimeout=15", "medsor-oracle", "cat /home/ubuntu/medsor/meds/dist/dagitim.json"],
                       capture_output=True, text=True, timeout=60)
    try:
        damga = json.loads(r.stdout)
    except ValueError:
        print("ATLANDI: Oracle'da dağıtım damgası (dist/dagitim.json) yok — önce bir kod dağıtımı (deploy-code.sh) gerekir")
        return 3
    if damga.get("kirli") and not a.zorla:
        print(f"ATLANDI: canlı kod {damga['commit'][:8]} + commit'lenmemiş değişiklikle dağıtılmış "
              f"({', '.join(damga['kirli'][:5])}); birebir yeniden derlenemez. Sonraki temiz kod dağıtımından sonra çalışır.")
        return 3
    tmp = Path(tempfile.mkdtemp(prefix="medsor-icerik-"))
    wt = tmp / "wt"
    # Oracle'daki uzak rsync sunucunun yayın kilidini (yayinla.py / deploy-code.sh: /tmp/meds-deploy.lock) tutarak çalışır
    UZ_RSYNC = "--rsync-path=flock /tmp/meds-deploy.lock sudo rsync"  # kilit ubuntu olarak (protected_regular), rsync root
    try:
        sh(["git", "-C", str(MEDS), "fetch", "-q", "origin"], check=True)
        sh(["git", "-C", str(MEDS), "worktree", "add", "-q", "--detach", str(wt), damga["commit"]], check=True)
        wm = wt / "meds" if (wt / "meds" / "package.json").exists() else wt
        (wm / "node_modules").symlink_to(MEDS / "node_modules")
        # Oracle src/data birebir (yayımlanan içeriğin asıl yeri), üstüne panel katmanı (deploy-code.sh [0b] gibi)
        r = sh(["rsync", "-az", "--delete", "--exclude=decks/items", UZ_RSYNC, f"{UZAK}/src/data/", f"{wm}/src/data/"], timeout=900)
        r2 = sh(["rsync", "-az", "--exclude=_ids.json", UZ_RSYNC, f"{UZAK}/data/content/", f"{wm}/src/data/"], timeout=300)
        if r.returncode or r2.returncode:
            print("HATA: Oracle src/data ya da panel katmanı çekilemedi"); return 1
        for k in zincir_klasorleri():
            rel = k.relative_to(MEDS / "src/data")  # patoloji_checkup/k2 gibi alt klasörler yerinde kalsın
            sh(["rsync", "-a", "--mkpath", "--delete", f"{k}/", f"{wm}/src/data/{rel}/"], check=True)
        oz = karma([wm / "src/data"]) + damga["commit"][:12]
        onceki = json.loads(DURUM.read_text()).get("karma") if DURUM.exists() else None
        if oz == onceki and not a.zorla:
            print("içerik ve kod değişmedi; dağıtım yok"); return 0
        if a.kuru:
            print(f"kuru: {damga['commit'][:8]} + Oracle içeriği hazır; derleme ve gönderim atlandı"); return 0
        r = sh("nice -n 10 npm run build --silent", cwd=wm, shell=True, capture_output=True, text=True, timeout=1800,
               env={**os.environ, "CUDA_VISIBLE_DEVICES": ""})
        if r.returncode or not (wm / "dist/index.html").exists():
            print("HATA: derleme:", (r.stderr or r.stdout)[-1500:]); return 1
        (wm / "dist/dagitim.json").write_text(json.dumps({**damga, "icerik_dagit": time.strftime("%Y-%m-%dT%H:%M:%S")},
                                                         ensure_ascii=False))
        for k in zincir_klasorleri():  # Oracle src/data da güncel kalsın (sonraki tam dağıtım/eşitleme için)
            rel = k.relative_to(MEDS / "src/data")
            sh(["rsync", "-az", "--mkpath", UZ_RSYNC, f"{k}/", f"{UZAK}/src/data/{rel}/"], check=True)
        r = sh(["rsync", "-az", UZ_RSYNC, f"{wm}/dist/", f"{UZAK}/dist/"], timeout=900)
        if r.returncode:
            print("HATA: dist gönderilemedi"); return 1
        time.sleep(3)
        s = subprocess.run(["curl", "-s", "-m", "20", "https://api.nofrostlife.com.tr/api/surum"], capture_output=True, text=True).stdout
        ok = '"surum"' in s
        DURUM.parent.mkdir(parents=True, exist_ok=True)
        DURUM.write_text(json.dumps({"karma": oz, "commit": damga["commit"], "zaman": time.strftime("%Y-%m-%dT%H:%M:%S"),
                                     "surum": s[:200]}, ensure_ascii=False))
        print("dağıtıldı:", s[:120] if ok else "sürüm okunamadı!")
        return 0 if ok else 1
    finally:
        subprocess.run(["git", "-C", str(MEDS), "worktree", "remove", "--force", str(wt)], capture_output=True)
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
