#!/usr/bin/env python3
"""Sesli sınav asistanı (branş geneli) — EMA klipleri (yalnız CPU). Patoloji asistan v2'nin klip düzeni + çözücünün okunuşu (ses.py Ema:
kısaltmalar uzun ünlülü harf adlarıyla, kisaltma_ses.py).

Girdi : meds_temp/spot_cozucu/<brans>/asistan/cikti/<kod>.json (asistan_dogrula.py 0 HATA)
Çıktı : meds/data/<brans>_asistan/ses/<kod>/<klip>.mp3 + kayit.json — giris · b-<n> · a-<id> · q-<s> · d-<s> · y-<s>-<H> · h-<s> · kapanis
Kullanım: asistan_ses_kuyruk.sh <brans> [kod ...]  (EMA venv, systemd-run kapsamı, flock'lu tek süreç)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ses as SC  # noqa: E402


def klipler(o: dict, S) -> dict[str, list[str]]:
    def ekle(ad, cumleler, *metinler):
        ekk = SC.kisaltmalar(*metinler)
        k[ad] = [S.ses_metni(c, ekk) for c in cumleler]

    k: dict[str, list[str]] = {}
    ekle("giris", [c["ses"] for c in o.get("giris") or []], *(c["metin"] for c in o.get("giris") or []))
    for bi, b in enumerate(o["bolumler"], 1):
        ekle(f"b-{bi}", [b["neden"]["ses"]], b["neden"]["metin"])
        for n in b["noktalar"]:
            ekle(f"a-{n['id']}", [c["ses"] for c in n["cumleler"]], *(c["metin"] for c in n["cumleler"]))
            for s in n.get("sorular") or []:
                a = s["anahtar"]
                tum = [s["dogru"]["metin"], *(v["metin"] for v in s["yanlis"].values()), *(v["metin"] for v in s["yardim"].values())]
                ekle(f"q-{a}", [s["kok_ses"]], *tum)
                ekle(f"d-{a}", [s["dogru"]["ses"]], *tum)
                for h, v in s["yanlis"].items():
                    ekle(f"y-{a}-{h}", [v["ses"]], *tum)
                ekle(f"h-{a}", [f"{SC.HARF_AD.get(h, h)} şıkkı. | {v['ses']}" for h, v in sorted(s["yardim"].items())], *tum)
    ekle("kapanis", [c["ses"] for c in o.get("kapanis") or []], *(c["metin"] for c in o.get("kapanis") or []))
    return k


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--brans", required=True)
    ap.add_argument("kodlar", nargs="*")
    a = ap.parse_args()
    girdi = SC.W / a.brans / "asistan" / "cikti"
    S = SC.Ema()
    kok = SC.MEDS / "data" / f"{a.brans}_asistan" / "ses"
    for kod in a.kodlar or sorted(x.stem for x in girdi.glob("*.json")):
        p = girdi / f"{kod}.json"
        if not p.exists():
            print(f"{kod}: çıktı yok, atlandı", flush=True)
            continue
        SC.klasor(S, kok, kod, klipler(json.loads(p.read_text(encoding="utf-8")), S), 48)


if __name__ == "__main__":
    main()
