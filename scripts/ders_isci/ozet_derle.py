#!/usr/bin/env python3
"""Ders özeti derleyici (yapay zekâsız, maliyetsiz): python3 ozet_derle.py <taslak_klasörü>

`ders_paketi.json` → `ders_ozeti` (giriş) + `sayfa_haritasi.json` → başlıkların `ozet` maddeleri ve sayfa aralıkları
→ `<klasör>/ders_ozeti.md`. Görsel anlatımları (`sekiller`) başlığın altında listelenir.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def derle(d: Path) -> Path | None:
    paket_p, harita_p = d / "ders_paketi.json", d / "sayfa_haritasi.json"
    if not paket_p.exists() or not harita_p.exists():
        return None
    paket = json.loads(paket_p.read_text(encoding="utf-8"))
    harita = json.loads(harita_p.read_text(encoding="utf-8"))
    oz = paket.get("ders_ozeti") or {}
    satir = [f"# {oz.get('baslik') or paket.get('konu') or 'Ders özeti'}", ""]
    kunye = " · ".join(str(x) for x in (paket.get("ders"), paket.get("ogretim_uyesi"), paket.get("tarih")) if x)
    if kunye:
        satir += [f"*{kunye}*", ""]
    if oz.get("ozet"):
        satir += [oz["ozet"].strip(), ""]
    sekil = {}
    for s in harita.get("sayfalar") or []:
        for g in s.get("sekiller") or []:
            if "süs görseli" not in str(g).lower():
                sekil.setdefault(str(s.get("baslik")), []).append((s.get("sayfa"), g))
    for b in harita.get("basliklar") or []:
        no = str(b.get("no"))
        ust = "###" if b.get("ust") else "##"
        sp = b.get("sayfalar") or []
        aralik = f" <sub>s. {sp[0]}–{sp[-1]}</sub>" if len(sp) == 2 and sp[0] != sp[1] else (f" <sub>s. {sp[0]}</sub>" if sp else "")
        satir += [f"{ust} {no}. {b.get('baslik', '')}{aralik}", ""]
        satir += [f"- {m}" for m in b.get("ozet") or []]
        for sayfa, g in sekil.get(no, []):
            satir.append(f"- 🖼 *Şekil (s. {sayfa}):* {g}")
        satir.append("")
    out = d / "ders_ozeti.md"
    out.write_text("\n".join(satir).rstrip() + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    p = derle(Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve())
    print(f"yazıldı: {p}" if p else "ders_paketi.json ya da sayfa_haritasi.json yok")
