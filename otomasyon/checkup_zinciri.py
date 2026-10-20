#!/usr/bin/env python3
"""Patoloji Hızlı Check Up — Kurul 2+ (gece). Branşta ≥3 bağımsız denetimden geçmiş ders olunca ve onaylı ders kümesi /
PDF'leri değişince Claude TALIMAT_CHECKUP.md ile k<N> bölümlerini kurar/günceller → dogrula.py --kurul N 0 HATA değilse
önceki sürüm geri konur. Çıktı src/data/patoloji_checkup/k<N>/ → gece içerik dağıtımıyla sitede (/patoloji-check-up?kurul=N).
  checkup_zinciri.py [--kurul N] [--kuru]
"""
import argparse, datetime as dt, hashlib, json, shutil, subprocess, sys, tempfile
from pathlib import Path

MEDS = Path(__file__).resolve().parents[1]; KOK = MEDS.parent
DURUM = KOK / "meds_temp/hat/checkup.json"
IZIN = "Read,Write,Edit,Glob,Grep,Bash(python3 *)"
EN_AZ = 3


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--kurul", type=int); ap.add_argument("--kuru", action="store_true")
    a = ap.parse_args()
    if a.kurul:
        kurullar = [a.kurul]
    else:
        sys.path.insert(0, str(MEDS / "scripts/takvim")); from aktif_kurul import durum
        kurullar = list(range(2, durum(dt.date.today().isoformat())["aktif"] + 1))
    durum_ = json.loads(DURUM.read_text()) if DURUM.exists() else {}
    hata = 0
    for k in kurullar:
        W = KOK / f"meds_temp/spot_cozucu/k{k}patoloji"
        onayli = sorted(json.loads((W / "onayli.json").read_text())) if (W / "onayli.json").exists() else []
        if len(onayli) < EN_AZ:
            print(f"Kurul {k}: {len(onayli)} onaylı patoloji dersi (en az {EN_AZ}) — Check Up bekliyor"); continue
        h = hashlib.sha256()
        for kod in onayli:
            h.update(kod.encode()); h.update((W / "pdf_metin" / f"{kod}.md").read_bytes())
        iz = h.hexdigest()[:16]
        if durum_.get(str(k)) == iz:
            print(f"Kurul {k}: değişiklik yok"); continue
        print(f"▶ Kurul {k}: {len(onayli)} ders → Check Up")
        if a.kuru:
            continue
        hedef = MEDS / f"src/data/patoloji_checkup/k{k}"
        yedek = Path(tempfile.mkdtemp(prefix="medsor-checkup-"))
        if hedef.exists():
            shutil.copytree(hedef, yedek / "eski")
        istem = (f"{MEDS}/scripts/patoloji_checkup/TALIMAT_CHECKUP.md talimatını uygula. Kurul {k}. Girdi klasörü {W}, "
                 f"çıktı klasörü {hedef}. Proje kökü {KOK}.")
        try:
            with open(KOK / "meds_temp/hat/checkup_claude.log", "a") as log:
                subprocess.run(["claude", "-p", istem, "--model", "claude-opus-5-5", "--allowedTools", IZIN, "--add-dir", str(KOK)],
                               cwd=KOK, stdout=log, stderr=subprocess.STDOUT, timeout=3 * 3600)
        except subprocess.TimeoutExpired:
            print("   claude zaman aşımı")
        r = subprocess.run([sys.executable, str(MEDS / "scripts/patoloji_checkup/dogrula.py"), "--kurul", str(k)],
                           capture_output=True, text=True)
        print("  ", (r.stdout.strip().splitlines() or ["?"])[-1])
        if r.returncode:  # kapı geçmedi: önceki sürüm geri (yarım/hatalı tablo yayına girmesin)
            shutil.rmtree(hedef, ignore_errors=True)
            if (yedek / "eski").exists():
                shutil.copytree(yedek / "eski", hedef)
            print(f"   HATA: Kurul {k} Check Up kapıdan geçmedi — önceki sürüm geri konuldu"); hata += 1
        else:
            durum_[str(k)] = iz; DURUM.parent.mkdir(parents=True, exist_ok=True); DURUM.write_text(json.dumps(durum_))
        shutil.rmtree(yedek, ignore_errors=True)
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main())
