#!/usr/bin/env python3
"""Patoloji sesli soru çözücü — EMA Lightning ile klip seslendirme (yalnız CPU, bu bilgisayarda).

Girdi : meds_temp/patoloji_ornek26/cozucu/cikti_tam/<kod>.json (cozucu_birlestir.py: örnek + benzer + çıkmış; her açıklama {metin, ses})
Çıktı : meds/data/patoloji_cozucu/ses/<kod>/<klip>.mp3 + kayit.json {klip: {h, sure, zaman: [[bas, son] cümle başına]}}
Klipler (soru no = n):
  q-n      soru kökü + şıklar ("A, …", "Be, …"; ekranda okunan şık vurgulanır)
  i-n      ipucu
  s-n-H    H şıkkının açıklaması (yanlış seçimde, "Bir yanlışı ele"de ve "Çözümü dinle"de çalınır)
  c-n      "Doğru cevap Ce, …" + çözüm
  d-n      "Doğru!" + çözüm (öğrenci doğruyu seçince)
  ortak/   yanlis ("Yanlış.") · dene ("Bir daha dene.")

Duraklar: cümle sonu 0,45 sn; " | " 0,3 sn, " || " 0,7 sn. Metni değişmeyen klip yeniden üretilmez (h = metin özeti). MP3 24 kHz mono 48 kbps.

Kullanım (EMA ortamıyla, GPU kapalı, makine korunarak):
  systemd-run --user --scope -p CPUQuota=300% -p MemoryMax=2200M --nice=10 \
    env CUDA_VISIBLE_DEVICES= EMA_IS_PARCACIGI=3 ~/.local/share/meds-ema/venv/bin/python meds/scripts/patoloji_cozucu/cozucu_ses.py [kod ...]
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
sys.path.insert(0, str(MEDS / "scripts/patoloji_cozucu"))
import kisaltma_ses as KS  # noqa: E402

# Kısaltma okunuşu burada (KS.uzat: "dee nee aa"); okunus.py'nin bitişik yazımı ("denea") kelime gibi okunduğu için kapatılır
E.okunus.duzelt = lambda metin, kayit=None: metin

E.KBPS = 48
GIRDI = MEDS.parent / "meds_temp/patoloji_ornek26/cozucu/cikti_tam"  # cozucu_birlestir.py üretir
CIKTI = MEDS / "data/patoloji_cozucu/ses"
CUMLE_SN, KISA_SN, UZUN_SN, ON_SN = 0.45, 0.3, 0.7, 0.12
SURUM = "ema-2"  # ema-2: kısaltmalar uzun ünlülü harf adlarıyla (kisaltma_ses.py)
HARF_AD = {"A": "A", "B": "Be", "C": "Ce", "D": "De", "E": "E"}
ORTAK = {"yanlis": ["Yanlış."], "dene": ["Bir daha dene."]}


def cumlele(s: str) -> list[str]:
    """Ses metnini cümlelere böl (ekranda cümle vurgusu + doğal durak)."""
    return [c.strip() for c in re.split(r"(?<=[.!?])\s+", s.strip()) if c.strip()]


def nokta(s: str) -> str:
    s = s.strip()
    return s if s[-1:] in ".!?" else s + "."


def klipler(o: dict) -> dict[str, list[str]]:
    k: dict[str, list[str]] = {}
    for q in o["sorular"]:
        n = q["no"]
        ekk = KS.metin_kisaltmalari(q["soru"], *q["secenekler"].values(), q["ipucu"]["metin"], q["cozum"]["metin"],
                                    *(v["metin"] for v in q["siklar"].values()))
        k0 = len(k)
        k[f"q-{n}"] = [nokta(q["kok_ses"])] + [f"{HARF_AD[h]}, {nokta(q['secenek_ses'][h])}" for h in "ABCDE"]
        k[f"i-{n}"] = cumlele(q["ipucu"]["ses"])
        for h in "ABCDE":
            k[f"s-{n}-{h}"] = cumlele(q["siklar"][h]["ses"])
        cz = cumlele(q["cozum"]["ses"])
        d = q["dogru"]
        k[f"c-{n}"] = [f"Doğru cevap {HARF_AD[d]}, {nokta(q['secenek_ses'][d])}"] + cz
        k[f"d-{n}"] = ["Doğru!"] + cz
        for ad in list(k)[k0:]:
            k[ad] = [KS.uzat(c, ekk) for c in k[ad]]
    return k


def seslendir(tts, cumleler: list[str]):
    import numpy as np

    sessiz = lambda sn: np.zeros(int(round(sn * E.SR)), dtype=np.float32)  # noqa: E731
    parca, zaman, t, notlar = [sessiz(ON_SN)], [], ON_SN, []
    for c in cumleler:
        bas = t
        for par, ayrac in re.findall(r"(.+?)(\|\||\||$)", c.strip()):
            par = par.strip()
            if not par:
                continue
            wav, n = E.paragraf_seslendir(tts, par)
            if n:
                notlar.append(f"{n}: {par[:50]}")
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


class Model:
    tts = None

    def __call__(self):
        if self.tts is None:
            self.tts = E.model_yukle()
        return self.tts


def klasor(m: Model, ad: str, K: dict[str, list[str]], silinsin: bool = True) -> None:
    d = CIKTI / ad
    d.mkdir(parents=True, exist_ok=True)
    kp = d / "kayit.json"
    kayit = json.loads(kp.read_text(encoding="utf-8")) if kp.exists() else {}
    yeni = toplam_sn = 0
    t0 = time.time()
    for klip, cumleler in K.items():
        h = hashlib.sha1((SURUM + f"|{E.HIZ}|" + "\n".join(cumleler)).encode()).hexdigest()[:12]
        if kayit.get(klip, {}).get("h") == h and (d / f"{klip}.mp3").exists():
            continue
        mp3, zaman, sure, notlar = seslendir(m(), cumleler)
        (d / f"{klip}.mp3").write_bytes(mp3)
        kayit[klip] = {"h": h, "sure": sure, "zaman": zaman, **({"not": notlar} if notlar else {})}
        yeni += 1
        toplam_sn += sure
        if yeni % 10 == 0:
            kp.write_text(json.dumps(kayit, ensure_ascii=False), encoding="utf-8")
    if silinsin:
        for klip in [a for a in kayit if a not in K]:
            kayit.pop(klip)
            (d / f"{klip}.mp3").unlink(missing_ok=True)
    kp.write_text(json.dumps(kayit, ensure_ascii=False), encoding="utf-8")
    E.log(f"{ad}: {len(K)} klip, {yeni} yeni ({toplam_sn:.0f} sn ses, {time.time() - t0:.0f} sn'de)")


def main(kodlar: list[str]) -> None:
    m = Model()
    klasor(m, "ortak", ORTAK)
    for kod in kodlar:
        p = GIRDI / f"{kod}.json"
        if not p.exists():
            E.log(f"{kod}: çıktı yok, atlandı")
            continue
        klasor(m, kod, klipler(json.loads(p.read_text(encoding="utf-8"))))


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a or sorted(x.stem for x in GIRDI.glob("*.json")))
