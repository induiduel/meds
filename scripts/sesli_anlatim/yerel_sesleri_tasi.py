#!/usr/bin/env python3
"""Bu bilgisayarda (yerel kuyrukta) üretilen yerel sesleri (xtts-yerel, ema-yerel) Oracle'a aktarır.

- MP3'ler `data/sesli_anlatim/ses/<key>/<vid>.mp3` → Oracle aynı yol (sudo rsync, root sahipli).
- Oracle `kayit.json`'a yalnız EKSİK varyantlar eklenir (sona; varsayılan ses değişmez). Var olan kayıtlara dokunulmaz,
  dosya atomik yazılır. MP3'ü Oracle'a ulaşmayan varyant kayda eklenmez.
- `--ornek`: konuşmacı örnekleri `data/sesli_anlatim/ornek/` da kopyalanır.
- `--degistir`: Oracle'da aynı derste AYNI sağlayıcı + konuşmacıyla eski bir yerel ses varsa (ör. okunuş düzeltmesinden
  önceki EMA sesi) yenisi onun YERİNE geçer (aynı sırada); eski MP3 silinir. Yalnız yerel sağlayıcılar etkilenir.

Kullanım: yerel_sesleri_tasi.py [--ornek] [--degistir] [--kuru]
"""
import json
import subprocess
import sys
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
KOK = MEDS / "data/sesli_anlatim"
UZAK = "/home/ubuntu/medsor/meds/data/sesli_anlatim"
YEREL = {"xtts-yerel", "ema-yerel"}
KURU = "--kuru" in sys.argv


def ssh(komut: str, girdi: str | None = None) -> str:
    r = subprocess.run(["ssh", "medsor-oracle", komut], input=girdi, capture_output=True, text=True, timeout=600)
    if r.returncode:
        raise SystemExit(f"ssh hatası: {r.stderr.strip()[:400]}")
    return r.stdout


kayit = json.loads((KOK / "kayit.json").read_text(encoding="utf-8"))
uzak = json.loads(ssh(f"sudo cat {UZAK}/kayit.json"))
aday = {k: [v for v in vs if v.get("saglayici") in YEREL and not any(u.get("id") == v["id"] for u in uzak.get(k, []))] for k, vs in kayit.items()}
aday = {k: vs for k, vs in aday.items() if vs}
dosyalar = [f"ses/{k}/{v['id']}.mp3" for k, vs in aday.items() for v in vs]
eksik = [f for f in dosyalar if not (KOK / f).exists()]
if eksik:
    raise SystemExit(f"yerelde MP3 yok: {eksik[:5]}")
print(f"aktarılacak: {len(dosyalar)} ses, {len(aday)} ders; {sum((KOK / f).stat().st_size for f in dosyalar) / 1e6:.0f} MB")
if KURU:
    sys.exit(0)

liste = "\n".join(dosyalar + (["ornek/"] if "--ornek" in sys.argv else []))
if dosyalar or "--ornek" in sys.argv:
    subprocess.run(["rsync", "-az", "--rsync-path=sudo rsync", "--chown=ubuntu:ubuntu", "--files-from=-", "-r", f"{KOK}/", f"medsor-oracle:{UZAK}/"],
                   input=liste, text=True, check=True, timeout=7200)

# Oracle'da birleştir: MP3'ü gelmiş ve kayıtta olmayan varyantı sona ekle (atomik)
birlestir = r'''
import json, os, sys
kok = sys.argv[1]
degistir = sys.argv[2] == "1"
aday = json.load(sys.stdin)
p = os.path.join(kok, "kayit.json")
k = json.load(open(p))
n = d = 0
for key, vs in aday.items():
    liste = k.setdefault(key, [])
    for v in vs:
        if any(u.get("id") == v["id"] for u in liste) or not os.path.exists(os.path.join(kok, "ses", key, v["id"] + ".mp3")):
            continue
        eski = [i for i, u in enumerate(liste) if degistir and u.get("saglayici") == v["saglayici"] and u.get("ses") == v["ses"]]
        if eski:
            eskiler = [liste[i] for i in eski]
            for i in eski[1:][::-1]:
                liste.pop(i)
            liste[eski[0]] = v
            for u in eskiler:
                try:
                    os.remove(os.path.join(kok, "ses", key, u["id"] + ".mp3"))
                except FileNotFoundError:
                    pass
            d += 1
        else:
            liste.append(v)
        n += 1
tmp = p + ".tmp"
json.dump(k, open(tmp, "w"), ensure_ascii=False, indent=1)
os.replace(tmp, p)
print("aktarıldı", n, "· eskisinin yerine geçen", d)
'''
print(ssh(f"sudo python3 -c '{birlestir}' {UZAK} {1 if '--degistir' in sys.argv else 0} && sudo chown -R root:root {UZAK}", json.dumps(aday, ensure_ascii=False)).strip())
