#!/usr/bin/env python3
"""Hat sağlık denetimi: canlı site, Oracle SSH, yerel 3000, vektör servisleri, EMA işçisi, disk.
Sorun varsa çıkış 1 + meds_temp/hat/saglik.json; hat.py bunu durum.json'a yazar (yönetim › Hat panosunda kırmızı).
Bağımlı aşamalar (Oracle'a yükleyenler) sağlık kötüyken boşuna denemesin diye `oracle_ok` alanı okunur.
  saglik.py [--sessiz]
"""
import json, shutil, subprocess, sys, time, urllib.request
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
CIKTI = KOK / "meds_temp/hat/saglik.json"


def http(url, t=15):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "MeDSor-saglik/1 (+hat)"})
        with urllib.request.urlopen(req, timeout=t) as r:
            return r.status
    except Exception as e:  # noqa: BLE001
        return getattr(e, "code", None) or str(e)[:80]


def ssh_ok():
    try:
        return subprocess.run(["ssh", "-o", "ConnectTimeout=12", "-o", "BatchMode=yes", "medsor-oracle", "true"],
                              capture_output=True, timeout=30).returncode == 0
    except subprocess.TimeoutExpired:
        return False


def birim(ad):
    return subprocess.run(["systemctl", "--user", "is-active", ad], capture_output=True, text=True).stdout.strip()


def main():
    s = {
        "zaman": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "canli_api": http("https://api.nofrostlife.com.tr/api/health"),
        "oracle_ssh": ssh_ok(),
        "yerel_3000": http("http://127.0.0.1:3000/api/health"),
        "embed_bge": birim("meds-embed-bge"), "ema_isci": birim("meds-ema"),
        "disk_bos_gb": round(shutil.disk_usage(str(KOK)).free / 1e9, 1),
    }
    s["oracle_ok"] = s["canli_api"] == 200 and s["oracle_ssh"]
    sorun = [k for k, ok in [("canli_api", s["canli_api"] == 200), ("oracle_ssh", s["oracle_ssh"]),
                             ("yerel_3000", s["yerel_3000"] == 200), ("embed_bge", s["embed_bge"] == "active"),
                             ("ema_isci", s["ema_isci"] == "active"), ("disk", s["disk_bos_gb"] >= 10)] if not ok]
    s["sorun"] = sorun
    CIKTI.parent.mkdir(parents=True, exist_ok=True); CIKTI.write_text(json.dumps(s, ensure_ascii=False, indent=1))
    if "--sessiz" not in sys.argv:
        print(json.dumps(s, ensure_ascii=False))
    return 1 if sorun else 0


if __name__ == "__main__":
    sys.exit(main())
