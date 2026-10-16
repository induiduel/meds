#!/usr/bin/env python3
"""Patoloji sesli sınav asistanı — EMA Lightning ile klip seslendirme (yalnız CPU, bu bilgisayarda).

Girdi : meds_temp/patoloji_onem/asistan/cikti/<kod>.json  (dogrula.py 0 HATA; her cümle {metin, ses})
Çıktı : meds/data/patoloji_asistan/ses/<kod>/<klip>.mp3 + kayit.json {klip: {h, sure, zaman: [[bas, son] cümle başına]}}
Klipler: giris · a-<id> (adım anlatımı) · q-<id> (soru kökü) · d-<id> (doğru geri bildirimi) · y-<id>-<harf> (yanlış şık) · kapanis

Duraklar: cümle sonu 0,45 sn; ses metnindeki " | " 0,3 sn, " || " 0,7 sn (nefes/vurgu öncesi). Her parça ayrı sentezlenir
(ema_isci.paragraf_seslendir: okunus.duzelt kısaltma okunuşu + süre denetimli 3 deneme). Metni değişmeyen klip yeniden üretilmez
(h = metin özeti). MP3 24 kHz mono 48 kbps.

Kullanım (EMA ortamıyla, GPU kapalı, makine korunarak):
  systemd-run --user --scope -p CPUQuota=300% -p MemoryMax=2200M --nice=10 \
    env CUDA_VISIBLE_DEVICES= EMA_IS_PARCACIGI=3 ~/.local/share/meds-ema/venv/bin/python meds/scripts/patoloji_onem/asistan_ses.py [kod ...]
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

os.environ["CUDA_VISIBLE_DEVICES"] = ""
MEDS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MEDS / "scripts/sesli_anlatim"))
import ema_isci as E  # noqa: E402

E.KBPS = 48
GIRDI = MEDS.parent / "meds_temp/patoloji_onem/asistan/cikti"
CIKTI = MEDS / "data/patoloji_asistan/ses"
CUMLE_SN, KISA_SN, UZUN_SN, ON_SN = 0.45, 0.3, 0.7, 0.12
SURUM = "ema-1"


def klipler(o: dict) -> dict[str, list[str]]:
    k: dict[str, list[str]] = {"giris": [c["ses"] for c in o.get("giris") or []], "kapanis": [c["ses"] for c in o.get("kapanis") or []]}
    for a in o["adimlar"]:
        k[f"a-{a['id']}"] = [c["ses"] for c in a["cumleler"]]
        s = a.get("soru")
        if s:
            k[f"q-{a['id']}"] = [s["kok_ses"]]
            k[f"d-{a['id']}"] = [s["dogru"]["ses"]]
            for h, v in s["yanlis"].items():
                k[f"y-{a['id']}-{h}"] = [v["ses"]]
    return k


def seslendir(tts, cumleler: list[str]):
    import numpy as np

    sessiz = lambda sn: np.zeros(int(round(sn * E.SR)), dtype=np.float32)  # noqa: E731
    parca, zaman, t, notlar = [sessiz(ON_SN)], [], ON_SN, []
    for c in cumleler:
        bas = t
        # " || " uzun, " | " kısa durak; parçalar ayrı sentezlenir
        for i, (par, ayrac) in enumerate(re.findall(r"(.+?)(\|\||\||$)", c.strip())):
            par = par.strip()
            if not par:
                continue
            wav, n = E.paragraf_seslendir(tts, par)
            if n:
                notlar.append(n)
            parca.append(wav)
            t += len(wav) / E.SR
            if ayrac:
                d = UZUN_SN if ayrac == "||" else KISA_SN
                parca.append(sessiz(d))
                t += d
        zaman.append([bas, t])
        parca.append(sessiz(CUMLE_SN))
        t += CUMLE_SN
    x = np.concatenate(parca)
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2").tobytes()
    mp3 = E.mp3_kodla(pcm)
    gercek = len(mp3) * 8 / (E.KBPS * 1000)
    k = gercek / (len(x) / E.SR)
    return mp3, [[round(a * k, 3), round(b * k, 3)] for a, b in zaman], round(gercek, 3), notlar


def main(kodlar: list[str]) -> None:
    tts = None
    for kod in kodlar:
        p = GIRDI / f"{kod}.json"
        if not p.exists():
            E.log(f"{kod}: çıktı yok, atlandı")
            continue
        o = json.loads(p.read_text(encoding="utf-8"))
        d = CIKTI / kod
        d.mkdir(parents=True, exist_ok=True)
        kp = d / "kayit.json"
        kayit = json.loads(kp.read_text(encoding="utf-8")) if kp.exists() else {}
        K = klipler(o)
        yeni = toplam_sn = 0
        t0 = time.time()
        for ad, cumleler in K.items():
            h = hashlib.sha1((SURUM + f"|{E.HIZ}|" + "\n".join(cumleler)).encode()).hexdigest()[:12]
            if kayit.get(ad, {}).get("h") == h and (d / f"{ad}.mp3").exists():
                continue
            if tts is None:
                tts = E.model_yukle()
            mp3, zaman, sure, notlar = seslendir(tts, cumleler)
            (d / f"{ad}.mp3").write_bytes(mp3)
            kayit[ad] = {"h": h, "sure": sure, "zaman": zaman, **({"not": notlar} if notlar else {})}
            yeni += 1
            toplam_sn += sure
            kp.write_text(json.dumps(kayit, ensure_ascii=False), encoding="utf-8")
        for ad in [a for a in kayit if a not in K]:  # artık olmayan klipler
            kayit.pop(ad)
            (d / f"{ad}.mp3").unlink(missing_ok=True)
        kp.write_text(json.dumps(kayit, ensure_ascii=False), encoding="utf-8")
        gecen = time.time() - t0
        E.log(f"{kod}: {len(K)} klip, {yeni} yeni ({toplam_sn:.0f} sn ses, {gecen:.0f} sn'de)")


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a or sorted(x.stem for x in GIRDI.glob("*.json")))
