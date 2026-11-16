#!/usr/bin/env python3
"""Patoloji alternatif soru çözücü — EMA Lightning ile seslendirme.

Girdi : meds/data/patoloji_cozucu_alt/metin/<kod>.json  (uret.py)
Çıktı : meds/data/patoloji_cozucu_alt/ses/<kod>/<no>.mp3 + kayit.json {no: {h, sure, cumle}}

Kullanım (GPU, kullanıcı izni 2026-10-19; meds-gpuguard etkin + saat kilidi):
  meds/scripts/uretim/patoloji_cozucu/cozucu_ses_gpu.sh meds/scripts/uretim/patoloji_cozucu_alt/seslendir.py 01
  ... seslendir.py            # bütün dersler
"""
from __future__ import annotations
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
import sys
import time
from pathlib import Path

MEDS = _kok.MEDS
sys.path.insert(0, str(MEDS / "scripts/uretim/patoloji_cozucu"))
sys.path.insert(0, str(MEDS / "scripts/uretim/sesli_anlatim"))

import cozucu_ses as C  # noqa: E402  (EMA, mp3 kodlama, cümle bölme)
import ema_isci as E  # noqa: E402

sys.path.insert(0, str(MEDS / "scripts/uretim/ses_ortak"))
import ses_klip as SK  # noqa: E402  (2026-11-16: karma/seslendir/atomik yazım ortak; okunuş ses_metin uzun yolu)
import ses_metin  # noqa: E402

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
    okunus = ses_metin.okuyucu(yol="uzun", modul="patoloji_cozucu_alt")  # eski C.seslendir ile aynı yol
    t0 = time.time()
    for q in sorular:
        ad = str(q["no"])
        cumleler = cumlelere(q["ses"])
        h = SK.klip_karmasi(f"{SURUM}|{E.HIZ}", cumleler)  # eski formülle birebir (sahte motor sınaması 2026-11-16)
        if kayit.get(ad, {}).get("h") == h and (d / f"{ad}.mp3").exists():
            continue
        try:
            mp3, zaman, sure, notlar = SK.seslendir(tts, cumleler, okunus=okunus, kbps=C.KBPS, E=E)
        except SK.BozukKlip as e:
            SK.bozuk_kaydet(klasor=str(d), klip=ad, hata=str(e), karakter=sum(map(len, cumleler)))
            E.log(f"  HATA {kod}/{ad}: {e} — klip yazılmadı")
            continue
        SK.atomik_yaz(d / f"{ad}.mp3", mp3)
        kayit[ad] = {"h": h, "sure": sure, "cumle": len(cumleler), **({"not": notlar} if notlar else {}),
                     "okunus_surum": ses_metin.SOZLUK_SURUM}
        yeni += 1
        toplam += sure
        if yeni % 5 == 0:
            SK.atomik_yaz(kp, json.dumps(kayit, ensure_ascii=False))
            E.log(f"{kod}: {yeni} klip ({toplam:.0f} sn ses)")
    SK.atomik_yaz(kp, json.dumps(kayit, ensure_ascii=False))
    E.log(f"{kod}: {len(sorular)} soru, {yeni} yeni ({toplam:.0f} sn ses, {time.time() - t0:.0f} sn'de)")


def main(kodlar: list[str]) -> None:
    tts = C.Model()()
    for kod in kodlar:
        ders(tts, kod)


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a or sorted(x.stem for x in GIRDI.glob("*.json")))
