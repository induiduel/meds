#!/usr/bin/env python3
"""Sesli soru çözücü (branş geneli) — klip seslendirme, çok sağlayıcılı (varsayılan EMA Lightning, yalnız CPU, bu bilgisayarda).

Girdi : meds_temp/spot_cozucu/<brans>/cikti_tam/<kod>.json (birlestir.py: örnek + çıkmış; her açıklama {metin, ses})
Çıktı : meds/data/<brans>_cozucu/<ses klasörü>/<kod>/<klip>.mp3 + kayit.json {klip: {h, sure, zaman: [[bas, son] cümle başına]}}
        ses klasörü: varsayılan ses (SESLER'de varsayilan=True, şimdilik EMA) → "ses"; diğerleri → "ses_<id>".
Klipler (soru no = n): q-n kök+şıklar · i-n ipucu · s-n-H şık açıklaması · c-n "Doğru cevap Ce, …" + çözüm · d-n "Doğru!" + çözüm;
ortak/ yanlis · dene. Duraklar: cümle sonu 0,45 sn; " | " 0,3 sn, " || " 0,7 sn. Metni değişmeyen klip yeniden üretilmez (h = özet).

Yeni ses eklemek: Saglayici alt sınıfı yaz (hazirla / paragraf / ses_metni / surum), SESLER'e kaydet, `--ses <id>` ile üret,
sonra birlestir.py dizine ve ders dosyasına o sesin kliplerini ekler; ön yüz (SoruCozucu) sesi kendiliğinden seçilebilir gösterir.

Kullanım (makine korunarak, GPU kapalı):
  systemd-run --user --scope -p CPUQuota=300% -p MemoryMax=2200M --nice=10 \
    env CUDA_VISIBLE_DEVICES= EMA_IS_PARCACIGI=3 ~/.local/share/meds-ema/venv/bin/python meds/scripts/spot_cozucu/ses.py \
    --brans enfeksiyon [--ses ema] [kod ...]       (ya da: meds/scripts/spot_cozucu/ses_kuyruk.sh enfeksiyon e01 e02)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

os.environ["CUDA_VISIBLE_DEVICES"] = ""
MEDS = Path(__file__).resolve().parents[2]
W = MEDS.parent / "meds_temp/spot_cozucu"
sys.path.insert(0, str(MEDS / "scripts/sesli_anlatim"))
sys.path.insert(0, str(MEDS / "scripts/patoloji_cozucu"))

CUMLE_SN, KISA_SN, UZUN_SN, ON_SN = 0.45, 0.3, 0.7, 0.12
HARF_AD = {"A": "A", "B": "Be", "C": "Ce", "D": "De", "E": "E"}
ORTAK = {"yanlis": ["Yanlış."], "dene": ["Bir daha dene."]}


class Saglayici:
    """Ses sağlayıcısı arayüzü. SR örnekleme hızında float32 dizi döndürür."""
    id = ""
    ad = ""
    surum = ""
    SR = 24000

    def hazirla(self) -> None: ...
    def paragraf(self, metin: str):  # → (np.float32 dizi, not | None)
        raise NotImplementedError
    def ses_metni(self, cumle: str, ek_kisaltma: set[str]) -> str:
        """Modele gidecek son biçim (kısaltma okunuşu vb.). Ekrandaki metin ve klip zamanlaması değişmez."""
        return cumle
    def mp3(self, pcm16: bytes) -> bytes:
        raise NotImplementedError


class Ema(Saglayici):
    id, ad, surum = "ema", "EMA", "ema-2"  # ema-2: kısaltmalar uzun ünlülü harf adlarıyla (kisaltma_ses.py)

    def __init__(self):
        import ema_isci as E
        import kisaltma_ses as KS
        # kısaltma okunuşu burada (KS.uzat: "dee nee aa"); okunus.py'nin bitişik yazımı ("denea") kelime gibi okunduğu için kapatılır
        E.okunus.duzelt = lambda metin, kayit=None: metin
        E.KBPS = 48
        self.E, self.KS, self.SR, self.tts = E, KS, E.SR, None
        self.surum = f"{self.surum}|{E.HIZ}"

    def hazirla(self):
        if self.tts is None:
            self.tts = self.E.model_yukle()

    def paragraf(self, metin):
        self.hazirla()
        return self.E.paragraf_seslendir(self.tts, metin)

    def ses_metni(self, cumle, ek_kisaltma):
        return self.KS.uzat(cumle, ek_kisaltma)

    def mp3(self, pcm16):
        return self.E.mp3_kodla(pcm16)

    def log(self, s):
        self.E.log(s)


SESLER: dict[str, dict] = {
    "ema": {"sinif": Ema, "ad": "EMA", "varsayilan": True, "kbps": 48},
}


def ses_klasoru(brans: str, ses: str) -> Path:
    return MEDS / "data" / f"{brans}_cozucu" / ("ses" if SESLER[ses].get("varsayilan") else f"ses_{ses}")


def cumlele(s: str) -> list[str]:
    return [c.strip() for c in re.split(r"(?<=[.!?])\s+", s.strip()) if c.strip()]


def nokta(s: str) -> str:
    s = s.strip()
    return s if s[-1:] in ".!?" else s + "."


def kisaltmalar(*metinler: str) -> set[str]:
    k = set()
    for m in metinler:
        for w in re.findall(r"[A-Za-zÇĞİÖŞÜçğıöşü]+", m or ""):
            if 2 <= len(w) <= 8 and sum(c.isupper() for c in w) >= 2:
                k.add(w.upper().replace("İ", "I"))
    return k


def klipler(o: dict, S: Saglayici) -> dict[str, list[str]]:
    k: dict[str, list[str]] = {}
    for q in o["sorular"]:
        n = q["no"]
        ekk = kisaltmalar(q["soru"], *q["secenekler"].values(), q["ipucu"]["metin"], q["cozum"]["metin"],
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
            k[ad] = [S.ses_metni(c, ekk) for c in k[ad]]
    return k


def seslendir(S: Saglayici, cumleler: list[str], kbps: int):
    import numpy as np

    sessiz = lambda sn: np.zeros(int(round(sn * S.SR)), dtype=np.float32)  # noqa: E731
    parca, zaman, t, notlar = [sessiz(ON_SN)], [], ON_SN, []
    for c in cumleler:
        bas = t
        for par, ayrac in re.findall(r"(.+?)(\|\||\||$)", c.strip()):
            par = par.strip()
            if not par:
                continue
            wav, n = S.paragraf(par)
            if n:
                notlar.append(f"{n}: {par[:50]}")
            parca.append(wav)
            t += len(wav) / S.SR
            if ayrac:
                d = UZUN_SN if ayrac == "||" else KISA_SN
                parca.append(sessiz(d))
                t += d
        zaman.append([bas, t])
        parca.append(sessiz(CUMLE_SN))
        t += CUMLE_SN
    x = np.concatenate(parca)
    mp3 = S.mp3((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())
    gercek = len(mp3) * 8 / (kbps * 1000)
    k = gercek / (len(x) / S.SR)
    return mp3, [[round(a * k, 3), round(b * k, 3)] for a, b in zaman], round(gercek, 3), notlar


def klasor(S: Saglayici, kok: Path, ad: str, K: dict[str, list[str]], kbps: int, silinsin: bool = True) -> None:
    d = kok / ad
    d.mkdir(parents=True, exist_ok=True)
    kp = d / "kayit.json"
    kayit = json.loads(kp.read_text(encoding="utf-8")) if kp.exists() else {}
    yeni = toplam_sn = 0
    t0 = time.time()
    for klip, cumleler in K.items():
        h = hashlib.sha1((S.surum + "|" + "\n".join(cumleler)).encode()).hexdigest()[:12]
        if kayit.get(klip, {}).get("h") == h and (d / f"{klip}.mp3").exists():
            continue
        mp3, zaman, sure, notlar = seslendir(S, cumleler, kbps)
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
    print(f"{time.strftime('%H:%M:%S')} {ad}: {len(K)} klip, {yeni} yeni ({toplam_sn:.0f} sn ses, {time.time() - t0:.0f} sn'de)", flush=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--brans", required=True)
    ap.add_argument("--ses", default="ema", choices=sorted(SESLER))
    ap.add_argument("kodlar", nargs="*")
    a = ap.parse_args()
    girdi = W / a.brans / "cikti_tam"
    tanim = SESLER[a.ses]
    S = tanim["sinif"]()
    kok = ses_klasoru(a.brans, a.ses)
    klasor(S, kok, "ortak", ORTAK, tanim["kbps"])
    for kod in a.kodlar or sorted(x.stem for x in girdi.glob("*.json")):
        p = girdi / f"{kod}.json"
        if not p.exists():
            print(f"{kod}: çıktı yok, atlandı", flush=True)
            continue
        klasor(S, kok, kod, klipler(json.loads(p.read_text(encoding="utf-8")), S), tanim["kbps"])


if __name__ == "__main__":
    main()
