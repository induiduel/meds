#!/usr/bin/env python3
"""Bütçe kapısı (2026-11-16) — geri kaymayı durdurur: ölçer, butce.json tavanlarıyla karşılaştırır; aşım = HATA (çıkış 1).

  python3 scripts/kapilar/butce.py              ölç + karşılaştır
  python3 scripts/kapilar/butce.py --guncelle   tavanı YALNIZ AŞAĞI çeker (ölçüm × 1,05 < tavan ise)
  python3 scripts/kapilar/butce.py --json

Tavanlar yalnız azalır: --guncelle hiçbir tavanı yükseltmez. Yükseltmek bilinçli karardır → butce.json elle düzenlenir
ve gerekçe `_gerekce` alanına yazılır. Eşiği sessizce gevşetmek YASAK (kapilar/CLAUDE.md). İlk tavanlar = 2026-11-16
ölçümü × 1,05. LLM/GPU yok; yalnız stdlib. Ön yüz kalemleri dist/ derlemesinden okunur (önce `npx vite build`).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

_d = Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
sys.path.insert(0, str(_d))
sys.path.insert(0, str(_d / "altyapi"))
from kok import MEDS, PROJE  # noqa: E402
from saglik_raporu import paket_olc  # noqa: E402

BUTCE = Path(__file__).resolve().parent / "butce.json"
PAY = 1.05


def kelime(p: Path) -> int:
    return len(re.findall(r"\S+", p.read_text(encoding="utf-8", errors="replace"))) if p.exists() else 0


def olc() -> dict[str, float]:
    o: dict[str, float] = {}
    p = paket_olc()
    o["ilk_yuk_js_gzip_kb"] = round(p["js"][1] / 1024, 1)
    o["ilk_yuk_css_gzip_kb"] = round(p["css"][1] / 1024, 1)
    o["ilk_yuk_dosya"] = p["ilk_dosya"]
    o["tembel_parca_en_buyuk_mb"] = round(p["tembel"][0][0] / 1048576, 2) if p["tembel"] else 0
    izli = subprocess.run(["git", "ls-files", "-z", "src/data"], cwd=MEDS, capture_output=True, text=True).stdout.split("\0")
    o["src_data_en_buyuk_mb"] = round(max((MEDS / f).stat().st_size for f in izli if f and (MEDS / f).is_file()) / 1048576, 2)
    o["zorunlu_okuma_kelime"] = sum(kelime(x) for x in (PROJE / "AGENTS.md", MEDS / "CLAUDE.md",
                                                      PROJE / "PROJE_TANITIMI.md", PROJE / "DEGISIKLIK_KAYDI.md"))
    for a in sorted((MEDS / "docs/asama_kurallari").glob("*.md")):
        o[f"asama_kelime:{a.stem}"] = kelime(a)
        if a.stem == "genel":
            continue
        r = subprocess.run([sys.executable, "scripts/hat/tam_hat/kural_secici.py", "--oku", a.stem], cwd=MEDS,
                           capture_output=True, text=True, timeout=60)
        dosya = [s.strip() for s in r.stdout.splitlines() if s.strip().endswith(".md") or s.strip().endswith(".py")]
        if r.returncode == 0 and dosya:
            o[f"oku_kelime:{a.stem}"] = sum(kelime((MEDS / s) if (MEDS / s).exists() else PROJE / s) for s in dosya)
    return o


def main() -> int:
    ap = argparse.ArgumentParser(description="Bütçe kapısı")
    ap.add_argument("--guncelle", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    olcum = olc()
    b = json.loads(BUTCE.read_text(encoding="utf-8")) if BUTCE.exists() else {}
    tavan = b.setdefault("tavan", {})
    hata, yeni, inen = [], [], []
    for k, v in olcum.items():
        t = tavan.get(k)
        hedef = round(v * PAY, 2) if isinstance(v, float) else int(v * PAY + 0.999)
        if t is None:
            tavan[k] = hedef
            yeni.append(k)
        elif v > t:
            hata.append(k)
        elif a.guncelle and hedef < t:
            tavan[k] = hedef
            inen.append(k)
    if a.json:
        print(json.dumps({"olcum": olcum, "tavan": tavan, "hata": hata}, ensure_ascii=False, indent=1))
    else:
        print(f"{'kalem':34} {'ölçüm':>10} {'tavan':>10}  durum")
        for k, v in olcum.items():
            print(f"{k:34} {v:>10} {tavan[k]:>10}  {'HATA' if k in hata else 'yeni' if k in yeni else 'aşağı' if k in inen else 'ok'}")
    if yeni or inen:
        b.setdefault("_aciklama", "Tavanlar yalnız azalır (butce.py --guncelle aşağı çeker). Yükseltmek: elle düzenle + _gerekce yaz.")
        BUTCE.write_text(json.dumps(b, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"bütçe: {len(hata)} HATA" + (f" ({', '.join(hata)})" if hata else "") + (f", {len(yeni)} yeni kalem" if yeni else ""))
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main())
