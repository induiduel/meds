#!/usr/bin/env python3
"""nereye.py — serbest görev metninden okunacak dosyaları bulur (stdlib, LLM yok).

  python3 scripts/altyapi/nereye.py "k2-30 pdf geldi tam hat"
  python3 scripts/altyapi/nereye.py --liste | --json "<metin>" | --denetle
Katalog: docs/yonlendirme.json (yollar meds/ köküne göre).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_d = Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
sys.path.insert(0, str(_d))
import kok as _kok  # noqa: E402

MEDS = _kok.MEDS
KATALOG = MEDS / "docs" / "yonlendirme.json"
AGENTS = _kok.PROJE / "AGENTS.md"
TR = str.maketrans("ıİşŞğĞüÜöÖçÇâÂîÎûÛ", "iissgguuoocCaaiiuu")


def katla(s: str) -> str:
    s = s.translate(TR).lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def yukle() -> list[dict]:
    return json.loads(KATALOG.read_text(encoding="utf-8"))["gorevler"]


def puanla(metin: str, g: dict) -> float:
    m = katla(metin)
    kel = set(m.split())
    p = 0.0
    for a in g["anahtarlar"] + [g["ad"]]:
        a = katla(a)
        if not a:
            continue
        if " " in a:
            if re.search(rf"\b{re.escape(a)}\b", m):
                p += 3 + len(a.split())
        elif a in kel:
            p += 3
        elif len(a) >= 4 and any(k.startswith(a) or (len(k) >= 4 and a.startswith(k)) for k in kel):
            p += 1.5  # Türkçe ek: "dağıt" ~ "dağıtım", "sözlükte" ~ "sözlük"
    return p


def bas(g: dict) -> str:
    s = [f"## {g['ad']}  [{g['id']}]", "Oku:"]
    s += [f"  {i}. {o['yol']} — {o['neden']}" for i, o in enumerate(g["oku"], 1)]
    if g["kurallar"]:
        s.append("Kurallar (AGENTS.md): " + ", ".join(g["kurallar"]))
    if g["kapilar"]:
        s.append("Kapılar:")
        s += [f"  $ {k}" for k in g["kapilar"]]
    if g["hatalar"]:
        s.append("Hatalar: " + ", ".join(g["hatalar"]))
    if g.get("asama"):
        s.append(f"Aşama özeti: python3 scripts/hat/tam_hat/kural_secici.py --oku {g['asama']}")
    return "\n".join(s)


def denetle(gorevler: list[dict]) -> int:
    hata = []
    metin = AGENTS.read_text(encoding="utf-8") if AGENTS.exists() else ""
    kurallar = set(re.findall(r"^(\d+[a-z]?)\. ", metin, re.M))
    if not metin:
        hata.append(f"AGENTS.md yok: {AGENTS}")
    idler = set()
    for g in gorevler:
        if g["id"] in idler:
            hata.append(f"{g['id']}: yinelenen id")
        idler.add(g["id"])
        if len(g["oku"]) > 6:
            hata.append(f"{g['id']}: oku > 6")
        for y in [o["yol"] for o in g["oku"]] + g["hatalar"]:
            if not (MEDS / y).exists():
                hata.append(f"{g['id']}: yol yok {y}")
        for k in g["kurallar"]:
            if k not in kurallar:
                hata.append(f"{g['id']}: kural {k} AGENTS.md'de yok")
        if g.get("asama") == "genel" or g.get("asama") and not (MEDS / "docs/asama_kurallari" / f"{g['asama']}.md").exists():
            hata.append(f"{g['id']}: aşama {g['asama']} yok")
    for h in hata:
        print("HATA", h)
    print(f"{len(gorevler)} görev, {len(hata)} HATA")
    return 1 if hata else 0


def main(argv: list[str]) -> int:
    gorevler = yukle()
    if "--denetle" in argv:
        return denetle(gorevler)
    if "--liste" in argv:
        for g in gorevler:
            print(f"{g['id']:<18} {g['ad']}")
        return 0
    js = "--json" in argv
    metin = " ".join(a for a in argv if not a.startswith("--"))
    if not metin:
        print(__doc__)
        return 2
    sirali = sorted(((puanla(metin, g), g) for g in gorevler), key=lambda x: -x[0])
    en = sirali[0][0]
    secilen = [g for p, g in sirali[:2] if p > 0 and p >= en * 0.6]
    if js:
        print(json.dumps({"sorgu": metin, "gorevler": secilen,
                          "oneri": [g["id"] for _, g in sirali[:3]] if not secilen else []},
                         ensure_ascii=False, indent=1))
        return 0
    if not secilen:
        print("Eşleşme yok. En yakın görevler: " + ", ".join(g["id"] for _, g in sirali[:3]))
        print("Haritalar: scripts/HARITA.md (betikler), docs/HARITA.md (belgeler), "
              "docs/KURUL2_YAPILMAYACAK_HATALAR.md (hatalar); tüm liste: --liste")
        return 0
    print("\n\n".join(bas(g) for g in secilen))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
