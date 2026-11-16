#!/usr/bin/env python3
"""Bu bilgisayarda (yerel kuyrukta) üretilen yerel sesleri (xtts-yerel, ema-yerel) Oracle'a aktarır.

- MP3'ler `data/sesli_anlatim/ses/<key>/<vid>.mp3` → Oracle aynı yol (sudo rsync, root sahipli).
- Oracle `kayit.json`'a yalnız EKSİK varyantlar eklenir (sona; varsayılan ses değişmez). Var olan kayıtlara dokunulmaz,
  dosya atomik yazılır. MP3'ü Oracle'a ulaşmayan varyant kayda eklenmez.
- `--ornek`: konuşmacı örnekleri `data/sesli_anlatim/ornek/` da kopyalanır.
- `--degistir`: Oracle'da aynı derste AYNI sağlayıcı + konuşmacıyla eski bir yerel ses varsa (ör. okunuş düzeltmesinden
  önceki EMA sesi) yenisi onun YERİNE geçer (aynı sırada); eski MP3 silinir. Yalnız yerel sağlayıcılar etkilenir.

- `--dogrula` (2026-11-16): yalnız doğrulama — yerel kayıttaki yerel sağlayıcı seslerinin (MP3'ü yerelde olan) Oracle'da
  var olup BOYUTUNUN aynı olduğunu `ssh medsor-oracle find -printf` ile karşılaştırır; hiçbir şey göndermez/silmez.
  Eksik/boyutu farklı varsa çıkış 1. Normal aktarım sonunda da aynı doğrulama çalışır ve sonuç `scripts/gunluk.py`
  (kaynak `ses_aktar`) ile kaydedilir (rsync karşı tarafta boyut/karma doğrulamıyordu; H11/H539 sınıfı sessiz eksik).
  Çözücü/asistan kökleri için eşdeğer: `scripts/uretim/ses_ortak/ses_kapisi.py oracle <kök|--hepsi>`.

Kullanım: yerel_sesleri_tasi.py [--ornek] [--degistir] [--kuru] [--dogrula]
"""
# Konum-bağımsız kök (2026-11-16): sabit parents[N] yerine scripts/kok.py (dosya taşınsa da doğru).
import sys as _sys
from pathlib import Path as _Path
_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402
import json
import subprocess
import sys
from pathlib import Path

MEDS = _kok.MEDS
KOK = MEDS / "data/sesli_anlatim"
UZAK = "/home/ubuntu/medsor/meds/data/sesli_anlatim"
YEREL = {"xtts-yerel", "ema-yerel"}
KURU = "--kuru" in sys.argv
DOGRULA = "--dogrula" in sys.argv


def ssh(komut: str, girdi: str | None = None) -> str:
    r = subprocess.run(["ssh", "medsor-oracle", komut], input=girdi, capture_output=True, text=True, timeout=600)
    if r.returncode:
        raise SystemExit(f"ssh hatası: {r.stderr.strip()[:400]}")
    return r.stdout


def dogrula() -> int:
    """Yerel ↔ Oracle: yerel kayıttaki yerel sağlayıcı MP3'leri karşıda var mı, boyut aynı mı (salt okunur)."""
    kayit_ = json.loads((KOK / "kayit.json").read_text(encoding="utf-8"))
    yerel = {f"{k}/{v['id']}.mp3": (KOK / "ses" / k / f"{v['id']}.mp3") for k, vs in kayit_.items() for v in vs
             if v.get("saglayici") in YEREL and (KOK / "ses" / k / f"{v['id']}.mp3").exists()}
    uz = {}
    for satir in ssh(f"sudo find {UZAK}/ses -type f -name '*.mp3' -not -path '*/.parca/*' -printf '%P\\t%s\\n'").splitlines():
        if "\t" in satir:
            yol, n = satir.rsplit("\t", 1)
            uz[yol] = int(n)
    eksik = sorted(g for g in yerel if g not in uz)
    fark = sorted(f"{g} yerel {p.stat().st_size} ≠ Oracle {uz[g]}" for g, p in yerel.items() if g in uz and uz[g] != p.stat().st_size)
    for g in eksik[:40]:
        print(f"HATA  Oracle'da yok: ses/{g}")
    for g in fark[:40]:
        print(f"HATA  boyut farklı: ses/{g}")
    print(f"== doğrulama: yerel {len(yerel)} yerel-sağlayıcı ses · Oracle {len(uz)} ses dosyası · eksik {len(eksik)} · boyut farkı {len(fark)}")
    try:
        sys.path.append(str(_kok.SCRIPTS))
        import gunluk  # noqa: E402
        gunluk.olay("ses_aktar", "hata" if eksik or fark else "bilgi", "sesli ders Oracle doğrulaması",
                    yerel=len(yerel), oracle=len(uz), eksik=len(eksik), boyut_farki=len(fark), ornek=(eksik + fark)[:5])
    except Exception:  # noqa: BLE001 — günlük asla aktarımı düşürmez
        pass
    return 1 if eksik or fark else 0


if DOGRULA:
    sys.exit(dogrula())

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
# Aktarım sonrası doğrulama (2026-11-16): rsync'in karşıya ulaştırdığını boyutla teyit et, sonucu günlüğe yaz.
sys.exit(dogrula())
