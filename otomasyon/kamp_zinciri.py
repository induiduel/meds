#!/usr/bin/env python3
"""Kurul kampı zinciri (gece): ONAYLI hoca tüyoları + ders bilgi deposu → Claude (scripts/kamp/TALIMAT_KAMP.md) → kapı
(scripts/kamp/dogrula.py) → EMA (scripts/kamp/ses.py) → src/data/kamp/k<N>/<brans>.json + Oracle data/kamp/ses/.
PDF açılmaz: dersler meds_database_v2/ders_bilgi/<ders>/ozet.md'den (scripts/dersler/bilgi_deposu.py).
Bir branşta kamp: en az 1 onaylı tüyo + en az 1 deposu hazır ders. Tüyolar ya da ders özetleri değişmediyse yeniden
üretilmez (karma). Kapı geçmezse yayımlanan kamp değişmez (önceki sürüm kalır) ve yöneticiye bildirim gider.
  kamp_zinciri.py [--kurul N] [--brans farmakoloji] [--kuru]
"""
import argparse, datetime as dt, hashlib, json, shutil, subprocess, sys, urllib.request
from pathlib import Path

MEDS = Path(__file__).resolve().parents[1]; KOK = MEDS.parent
sys.path.insert(0, str(MEDS / "scripts/dersler")); sys.path.insert(0, str(MEDS / "otomasyon"))
import bilgi_deposu as BD  # noqa: E402
IZIN = "Read,Write,Edit,Glob,Grep,Bash(python3 *)"
import os
API = os.environ.get("MEDS_KAMP_API", "https://api.nofrostlife.com.tr")  # prova: yerel 3000
EMA_PY = Path.home() / ".local/share/meds-ema/venv/bin/python"


def onayli_tuyolar(kurul):
    req = urllib.request.Request(f"{API}/api/kamp/tuyolar?kurul={kurul}", headers={"User-Agent": "MeDSor-hat/1"})
    return json.load(urllib.request.urlopen(req, timeout=30)).get("tuyolar") or []


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--kurul", type=int); ap.add_argument("--brans"); ap.add_argument("--kuru", action="store_true")
    ap.add_argument("--prova", action="store_true", help="çıktı + ses meds_temp/prova/kamp/'a; src/data ve Oracle'a dokunmaz")
    a = ap.parse_args()
    if a.kurul:
        kurullar = [a.kurul]
    else:
        sys.path.insert(0, str(MEDS / "scripts/takvim")); from aktif_kurul import durum
        kurullar = list(range(2, durum(dt.date.today().isoformat())["aktif"] + 1))
    slug_ad = {b["slug"]: b["ad"] for b in json.loads((MEDS / "src/data/dersler/branslar.json").read_text())["branslar"]}
    ad_slug = {v: k for k, v in slug_ad.items()}
    hata = 0
    for k in kurullar:
        try:
            tuyolar = onayli_tuyolar(k)
        except Exception as e:  # noqa: BLE001
            print(f"HATA: Kurul {k} tüyoları okunamadı: {e}"); hata += 1; continue
        depolar = [BD.manifest(p.parent.name) for p in sorted(BD.DEPO.glob(f"k{k}-*/manifest.json"))]
        for brans in sorted({t["brans"] for t in tuyolar}):
            if a.brans and brans != a.brans:
                continue
            ts = [t for t in tuyolar if t["brans"] == brans]
            dersler = [m for m in depolar if m and ad_slug.get(m["brans"]) == brans]
            if not dersler:
                print(f"Kurul {k} {brans}: {len(ts)} tüyo var, deposu hazır ders yok — bekliyor"); continue
            girdi = {"kurul": k, "brans": brans, "brans_ad": slug_ad.get(brans, brans), "tuyolar": ts,
                     "dersler": [{"ders_id": m["ders_id"], "kod": m["kod"], "konu": m["konu"],
                                  "ozet": str(BD.DEPO / m["ders_id"] / "ozet.md"),
                                  "kaynak": str(Path(m["kaynak_dizin"]) / "kaynak.md")} for m in dersler]}
            iz = hashlib.sha256(json.dumps([[t["id"], t["metin"]] for t in ts] + [m["ozet_sha"] for m in dersler]).encode()).hexdigest()[:16]
            W = KOK / f"meds_temp/kamp/k{k}/{brans}"; W.mkdir(parents=True, exist_ok=True)
            yayin = (KOK / f"meds_temp/prova/kamp/k{k}/{brans}.json") if a.prova else MEDS / f"src/data/kamp/k{k}/{brans}.json"
            if (W / "iz.txt").exists() and (W / "iz.txt").read_text() == iz and yayin.exists():
                print(f"Kurul {k} {brans}: değişiklik yok"); continue
            if yayin.exists():
                girdi["onceki"] = str(yayin)
            (W / "girdi.json").write_text(json.dumps(girdi, ensure_ascii=False, indent=1))
            print(f"▶ Kurul {k} {brans}: {len(ts)} tüyo · {len(dersler)} ders")
            if a.kuru:
                continue
            if yayin.exists() and not (W / "kamp.json").exists():
                shutil.copy(yayin, W / "kamp.json")  # kimlikler korunsun diye önceki sürümden başla
            kapi = [sys.executable, str(MEDS / "scripts/kamp/dogrula.py"), str(W / "kamp.json"), "--girdi", str(W / "girdi.json")]
            istem = (f"{MEDS}/scripts/kamp/TALIMAT_KAMP.md talimatını uygula. Çalışma klasörü {W} (girdi.json orada; çıktı kamp.json). "
                     f"Bitince şu kapıyı 0 HATA olana kadar çalıştır: {' '.join(kapi)}")
            r = 1
            for tur in range(3):
                try:
                    with open(W / "claude.log", "a") as log:
                        subprocess.run(["claude", "-p", istem, "--model", "claude-opus-5-5", "--allowedTools", IZIN, "--add-dir", str(KOK)],
                                       cwd=W, stdout=log, stderr=subprocess.STDOUT, timeout=3 * 3600)
                except subprocess.TimeoutExpired:
                    print("   claude zaman aşımı")
                r = subprocess.run(kapi, capture_output=True, text=True)
                print("  ", (r.stdout.strip().splitlines() or ["?"])[-1])
                if r.returncode == 0:
                    break
                istem = f"Kapı HATA verdi: `{' '.join(kapi)}`. Çalıştır, hataların hepsini kamp.json'da düzelt, 0 HATA olunca bitir."
            if r.returncode:
                hata += 1
                from bildir import bildir
                bildir(f"Kurul {k} {brans} kampı kapıdan geçmedi", (r.stdout or "")[-1500:] + "\nYayımlanan kamp değişmedi.", hedef="kamp")
                continue
            s = subprocess.run(["systemd-run", "--user", "--scope", "-q", "-p", "CPUQuota=300%", "-p", "MemoryMax=2200M", "--nice=10",
                                "env", "CUDA_VISIBLE_DEVICES=", str(EMA_PY), str(MEDS / "scripts/kamp/ses.py"), str(W / "kamp.json")]
                               + (["--ses-kok", str(KOK / "meds_temp/prova/kamp/ses")] if a.prova else []))
            if s.returncode:
                print("   HATA: kamp sesi üretilemedi"); hata += 1; continue
            yayin.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(W / "kamp.json", yayin)
            if a.prova:
                print(f"   PROVA tamam: {yayin} (Oracle'a gönderilmedi)"); (W / "iz.txt").write_text(iz); continue
            sk = MEDS / "data/kamp/ses" / f"k{k}" / brans
            o = subprocess.run(["rsync", "-az", "--mkpath", "--rsync-path=flock /tmp/meds-deploy.lock sudo rsync", f"{sk}/",
                                f"medsor-oracle:/home/ubuntu/medsor/meds/data/kamp/ses/k{k}/{brans}/"], timeout=900)
            if o.returncode:
                print("   HATA: kamp sesi Oracle'a gönderilemedi"); hata += 1; continue
            (W / "iz.txt").write_text(iz)
            print(f"   yayına hazır: {yayin.relative_to(MEDS)} (gece içerik dağıtımı sitede yayınlar)")
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main())
