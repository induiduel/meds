#!/usr/bin/env python3
"""Konuşma metni eksik/hatalı taslakları tamamlar ve canlı derse işler.

  --uret [is_id ...]   (meds-ders-isci konteynerinde) metni olmayan ya da denetimi geçmeyen taslaklar için
                       isle.konusma_metni; onay bekleyen taslağın durum.json özeti güncellenir. -j N paralel.
  --canliya [is_id ...] (Oracle sunucusunda) yayınlanmış taslakların 0 HATA metnini /api/sesli-anlatim/ders-ekle'ye
                       gönderir (yayinla._canli_ders_ekle; metin değiştiyse Emel + EMA sesleri kuyruğa girer).
"""
import argparse
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def taslaklar(kok: Path, secili: list[str]) -> list[Path]:
    return [d for d in sorted(kok.iterdir()) if d.is_dir() and (d / "deck.json").exists() and (not secili or d.name in secili)]


def uret(secili: list[str], paralel: int) -> int:
    import isle
    hedef = [d for d in taslaklar(isle.TASLAK, secili) if isle.metin_denetle(d)["hata"]]
    print(f"{len(hedef)} taslakta konuşma metni eksik/hatalı: {[d.name for d in hedef]}", flush=True)

    def tek(d: Path) -> str:
        if not (d / "ana_bitti.json").exists():
            isle.yaz(d / "ana_bitti.json", isle.oku(d / "denetim.json", {}))
        s = isle.konusma_metni(d)
        du = isle.oku(d / "durum.json", {})
        if du.get("durum") == "onay_bekliyor" and s["durum"] in ("tamam", "hata"):
            du["ozet"] = re.sub(r" · (konuşma metni.*)$", "", du.get("ozet", "")) + " · " + s["ozet"]
            du["canli_ders"] = s["durum"]
            isle.yaz(d / "durum.json", du)
        isle.log(f"konuşma metni tamamlama: {d.name} → {s['ozet']}")
        return f"{d.name}: {s['durum']} · {s['ozet']}"

    with ThreadPoolExecutor(paralel) as ex:
        for r in ex.map(tek, hedef):
            print(r, flush=True)
    kalan = [d.name for d in hedef if isle.metin_denetle(d)["hata"]]
    print("kalan hatalı:", kalan or "yok")
    return 1 if kalan else 0


def canliya(secili: list[str]) -> int:
    import isle
    import yayinla
    kok = Path.home() / "medsor" / "ders_isci" / "taslak"
    kayit = {y["is_id"]: y for y in yayinla.oku(yayinla.DURUM_KAYIT, []) or []}
    hata = 0
    for d in taslaklar(kok, secili):
        if d.name not in kayit:
            continue
        den = isle.metin_denetle(d) if (d / "konusma_metni.md").exists() else {"hata": 999}
        if den["hata"]:
            print(f"{d.name}: metin yok/hatalı, atlandı")
            hata += 1
            continue
        y = type("Y", (), {})()
        y.d, y.kayit = d, kayit[d.name]
        y.ders_id, y.deste_id = y.kayit["ders_id"], y.kayit["deste_id"]
        print(yayinla._canli_ders_ekle(y), flush=True)
        time.sleep(1)
    return 1 if hata else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--uret", action="store_true")
    ap.add_argument("--canliya", action="store_true")
    ap.add_argument("-j", type=int, default=3)
    ap.add_argument("is_id", nargs="*")
    a = ap.parse_args()
    sys.exit(uret(a.is_id, a.j) if a.uret else canliya(a.is_id) if a.canliya else ap.print_help())
