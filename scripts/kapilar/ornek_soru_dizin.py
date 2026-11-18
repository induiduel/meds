#!/usr/bin/env python3
"""Örnek soru dosyası adı + dizin kapısı (H623, 2026-11-18).

Belirti: k2-40/k2-41 örnek soruları `k2-40.json` gibi kısa adla yazıldı, `ornek_sorular/k2/index.json`'a girmedi → sitede görünmeyecekti.
Kural: `src/data/ornek_sorular/k<N>/<id>.json` dosyasının adı içindeki `id` ile aynı ve tam ders anahtarıdır (`k2-40-santral-…`);
her dosya o kurulun `index.json`'unda kayıtlıdır; dizindeki her kayıt bir dosyaya karşılık gelir.

Kullanım:
  python3 scripts/kapilar/ornek_soru_dizin.py [--kok <meds kökü>]        → bütün kurullar (dagit.sh statik kapısı)
  python3 scripts/kapilar/ornek_soru_dizin.py --dosya <ornek soru json>   → tek dosya (ornek_soru_kapi.py çağırır)
"""
import sys as _sys
from pathlib import Path as _Path
_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402
import argparse, json, re, sys  # noqa: E402
from pathlib import Path  # noqa: E402

TAM = re.compile(r"^k\d+-\d+-[a-z0-9-]+$")
HARIC = {"index.json", "_dizin.json"}


def dosya_denetle(p: Path) -> list[str]:
    e = []
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception as x:
        return [f"{p.name}: okunamadı ({x})"]
    if not isinstance(d, dict) or "kazanimlar" not in d:
        return []  # ders dosyası değil (ör. k2-cikmis-ornek.json)
    kid = str(d.get("id") or "")
    if kid != p.stem:
        e.append(f"{p.name}: dosya adı içindeki id ({kid!r}) ile aynı değil")
    idx = p.parent / "index.json"
    ids = {x.get("id") for x in json.loads(idx.read_text(encoding="utf-8"))} if idx.exists() else set()
    if p.stem not in ids:  # dizinde kayıtlı özel dosya (ör. k2-cikmis-ornek) ad kuralından muaf
        if not TAM.match(p.stem):
            e.append(f"{p.name}: ad tam ders anahtarı değil (k<N>-<no>-<konu>; kısa ad sitede görünmez)")
        e.append(f"{p.name}: {idx.parent.name}/index.json'da kayıtlı değil")
    return e


def tumu(kok: Path) -> list[str]:
    e = []
    for kd in sorted((kok / "src" / "data" / "ornek_sorular").glob("k*")):
        if not kd.is_dir():
            continue
        for p in sorted(kd.glob("*.json")):
            if p.name not in HARIC:
                e += dosya_denetle(p)
        idx = kd / "index.json"
        if idx.exists():
            for x in json.loads(idx.read_text(encoding="utf-8")):
                if not (kd / f"{x.get('id')}.json").exists():
                    e.append(f"{kd.name}/index.json: {x.get('id')} kaydının dosyası yok")
    return e


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kok", type=Path, default=_kok.MEDS)
    ap.add_argument("--dosya", type=Path)
    a = ap.parse_args()
    hata = dosya_denetle(a.dosya.resolve()) if a.dosya else tumu(a.kok.resolve())
    for x in hata:
        print("HATA", x)
    print(f"örnek soru dizin kapısı: {len(hata)} HATA")
    sys.exit(1 if hata else 0)
