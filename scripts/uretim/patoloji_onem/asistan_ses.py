#!/usr/bin/env python3
"""Patoloji sesli sınav asistanı — EMA Lightning ile klip seslendirme (yalnız CPU, bu bilgisayarda).

Girdi : meds_temp/patoloji_onem/asistan/cikti/<kod>.json  (dogrula.py 0 HATA; her cümle {metin, ses})
Çıktı : meds/data/patoloji_asistan/ses/<kod>/<klip>.mp3 + kayit.json {klip: {h, sure, zaman: [[bas, son] cümle başına]}}
Klipler (v2): giris · b-<n> (bölümün "neden önemli" girişi) · a-<id> (nokta anlatımı) · q-<s> (soru kökü) · d-<s> (doğru) ·
y-<s>-<harf> (yanlış şık açıklaması) · h-<s> ("Yardım al": her şık harfiyle, tek cümle) · kapanis

Duraklar: cümle sonu 0,45 sn; ses metnindeki " | " 0,3 sn, " || " 0,7 sn (nefes/vurgu öncesi). Her parça ayrı sentezlenir
(ema_isci.paragraf_seslendir: okunus.duzelt kısaltma okunuşu + süre denetimli 3 deneme). Metni değişmeyen klip yeniden üretilmez
(h = metin özeti). MP3 24 kHz mono 48 kbps.

Kullanım (EMA ortamıyla, GPU kapalı, makine korunarak):
  systemd-run --user --scope -p CPUQuota=300% -p MemoryMax=2200M --nice=10 \
    env CUDA_VISIBLE_DEVICES= EMA_IS_PARCACIGI=3 ~/.local/share/meds-ema/venv/bin/python meds/scripts/uretim/patoloji_onem/asistan_ses.py [kod ...]
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
import os
import re
import sys
from pathlib import Path

os.environ["CUDA_VISIBLE_DEVICES"] = ""
MEDS = _kok.MEDS
sys.path.insert(0, str(MEDS / "scripts/uretim/sesli_anlatim"))
import ema_isci as E  # noqa: E402
sys.path.insert(0, str(_kok.SCRIPTS / "uretim/ses_ortak"))
import ses_klip as SK  # noqa: E402  (seslendir/klasor tek kaynak, 2026-11-16; E.KBPS ezmesi kalktı)
import ses_metin  # noqa: E402

KBPS = 48
GIRDI = MEDS.parent / "meds_temp/patoloji_onem/asistan2/cikti"
CIKTI = MEDS / "data/patoloji_asistan/ses"
CUMLE_SN, KISA_SN, UZUN_SN, ON_SN = 0.45, 0.3, 0.7, 0.12
SURUM = "ema-1"


HARF_AD = {"A": "A", "B": "Be", "C": "Ce", "D": "De", "E": "E"}


def klipler(o: dict) -> dict[str, list[str]]:
    k: dict[str, list[str]] = {"giris": [c["ses"] for c in o.get("giris") or []], "kapanis": [c["ses"] for c in o.get("kapanis") or []]}
    for bi, b in enumerate(o["bolumler"], 1):
        k[f"b-{bi}"] = [b["neden"]["ses"]]
        for n in b["noktalar"]:
            k[f"a-{n['id']}"] = [c["ses"] for c in n["cumleler"]]
            for s in n.get("sorular") or []:
                a = s["anahtar"]
                k[f"q-{a}"] = [s["kok_ses"]]
                k[f"d-{a}"] = [s["dogru"]["ses"]]
                for h, v in s["yanlis"].items():
                    k[f"y-{a}-{h}"] = [v["ses"]]
                # yardım: şık sırasıyla, her biri harf adıyla başlayan bir cümle (ekranda o şık vurgulanır)
                k[f"h-{a}"] = [f"{HARF_AD.get(h, h)} şıkkı. | {v['ses']}" for h, v in sorted(s["yardim"].items())]
    return k


def seslendir(tts, cumleler: list[str]):
    # Motor metni: ses_metin, yol veriden (patoloji_asistan → Kurul 1 → bitişik; eskiden okunus.duzelt doğrudan)
    return SK.seslendir(tts, cumleler, okunus=ses_metin.okuyucu(modul=CIKTI.parent.name), kbps=KBPS, E=E)


class _Model:
    tts = None

    def __call__(self):
        if self.tts is None:
            self.tts = E.model_yukle()
        return self.tts


def main(kodlar: list[str]) -> None:
    m = _Model()
    ok = ses_metin.okuyucu(modul=CIKTI.parent.name)
    for kod in kodlar:
        p = GIRDI / f"{kod}.json"
        if not p.exists():
            E.log(f"{kod}: çıktı yok, atlandı")
            continue
        K = klipler(json.loads(p.read_text(encoding="utf-8")))
        SK.klasor(CIKTI / kod, K, surum=f"{SURUM}|{E.HIZ}", uret=lambda c: SK.seslendir(m(), c, okunus=ok, kbps=KBPS, E=E),
                  ara_yaz=1, log=E.log)


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a or sorted(x.stem for x in GIRDI.glob("*.json")))
