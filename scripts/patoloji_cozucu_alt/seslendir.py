#!/usr/bin/env python3
"""Patoloji alternatif soru çözücü — EMA Lightning ile seslendirme.

Girdi : meds/data/patoloji_cozucu_alt/metin/<kod>.json  (uret.py)
Çıktı : meds/data/patoloji_cozucu_alt/ses/<kod>/<no>.mp3 + kayit.json {no: {h, sure, cumle}}

Kullanım (GPU, kullanıcı izni 2026-10-19; meds-gpuguard etkin + saat kilidi):
  meds/scripts/patoloji_cozucu/cozucu_ses_gpu.sh meds/scripts/patoloji_cozucu_alt/seslendir.py 01
  ... seslendir.py            # bütün dersler
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MEDS / "scripts/patoloji_cozucu"))
sys.path.insert(0, str(MEDS / "scripts/sesli_anlatim"))

import cozucu_ses as C  # noqa: E402  (EMA, mp3 kodlama, cümle bölme)
import ema_isci as E  # noqa: E402

GIRDI = MEDS / "data/patoloji_cozucu_alt/metin"
CIKTI = MEDS / "data/patoloji_cozucu_alt/ses"
SURUM = "alt-1"


def cumlelere(ses: str) -> list[str]:
    """Cümlelere böl; yalnız noktalama kalan parçaları (M.Ö. gibi kısaltma artıkları) at."""
    return [
        c for satir in ses.splitlines() for c in C.cumlele(satir)
        if any(ch.isalpha() for ch in c)
    ]


def ders(tts, kod: str) -> None:
    d = CIKTI / kod
    d.mkdir(parents=True, exist_ok=True)
    kp = d / "kayit.json"
    kayit = json.loads(kp.read_text(encoding="utf-8")) if kp.exists() else {}
    sorular = json.loads((GIRDI / f"{kod}.json").read_text(encoding="utf-8"))["sorular"]
    yeni = toplam = 0
    t0 = time.time()
    for q in sorular:
        ad = str(q["no"])
        cumleler = cumlelere(q["ses"])
        h = hashlib.sha1((SURUM + f"|{E.HIZ}|" + "\n".join(cumleler)).encode()).hexdigest()[:12]
        if kayit.get(ad, {}).get("h") == h and (d / f"{ad}.mp3").exists():
            continue
        mp3, zaman, sure, notlar = C.seslendir(tts, cumleler)
        (d / f"{ad}.mp3").write_bytes(mp3)
        kayit[ad] = {"h": h, "sure": sure, "cumle": len(cumleler), **({"not": notlar} if notlar else {})}
        yeni += 1
        toplam += sure
        if yeni % 5 == 0:
            kp.write_text(json.dumps(kayit, ensure_ascii=False), encoding="utf-8")
            E.log(f"{kod}: {yeni} klip ({toplam:.0f} sn ses)")
    kp.write_text(json.dumps(kayit, ensure_ascii=False), encoding="utf-8")
    E.log(f"{kod}: {len(sorular)} soru, {yeni} yeni ({toplam:.0f} sn ses, {time.time() - t0:.0f} sn'de)")


def main(kodlar: list[str]) -> None:
    tts = C.Model()()
    for kod in kodlar:
        ders(tts, kod)


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a or sorted(x.stem for x in GIRDI.glob("*.json")))
