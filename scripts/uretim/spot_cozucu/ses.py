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
    env CUDA_VISIBLE_DEVICES= EMA_IS_PARCACIGI=3 ~/.local/share/meds-ema/venv/bin/python meds/scripts/uretim/spot_cozucu/ses.py \
    --brans enfeksiyon [--ses ema] [kod ...]       (ya da: meds/scripts/uretim/spot_cozucu/ses_kuyruk.sh enfeksiyon e01 e02)
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

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

if os.environ.get("EMA_CIHAZ") != "cuda":  # GPU istisnası: ema_isci.py başındaki koşullar
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
MEDS = _kok.MEDS
W = MEDS.parent / "meds_temp/spot_cozucu"
sys.path.insert(0, str(MEDS / "scripts/uretim/sesli_anlatim"))
sys.path.insert(0, str(MEDS / "scripts/uretim/patoloji_cozucu"))
sys.path.insert(0, str(MEDS / "scripts/uretim/ses_ortak"))
import ses_klip as SK  # noqa: E402  (seslendir/klasor/cumlele/nokta tek kaynak, 2026-11-16)
import ses_metin  # noqa: E402

CUMLE_SN, KISA_SN, UZUN_SN, ON_SN = 0.45, 0.3, 0.7, 0.12
HARF_AD = {"A": "A", "B": "Be", "C": "Ce", "D": "De", "E": "E"}
ORTAK = {"yanlis": ["Yanlış."], "dene": ["Bir daha dene."],
         # Otomatik çöz ara cümleleri (SoruCozucu.tsx OC ile aynı)
         "oc-bas": ["Bu soruyu birlikte çözelim.", "Önce soruyu dikkatlice okuyalım."],
         "oc-yol": ["Soruyu çözmek için şu yoldan gideceğiz."],
         "oc-ele": ["Şimdi seçenekleri tek tek değerlendirip yanlış olanları eleyelim."],
         "oc-elendi": ["Bu yüzden bu seçeneği eliyoruz."],
         "oc-kalan": ["Geriye tek bir seçenek kaldı.", "Şimdi bunun neden doğru olduğuna bakalım."],
         "oc-son": ["Benzer bir soruyla karşılaşınca da aynı yolu izleyebilirsin."]}


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

    def __init__(self, kbps: int = 48):
        import ema_isci as E
        import kisaltma_ses as KS
        # Klip metni: KS.uzat ("dee nee aa", karmaya dahil). Motor metni: ses_metin uzun yolu (terim + yazım kısaltması +
        # fonetik/sayı). Eskiden E.okunus.duzelt / E.KBPS genel olarak eziliyordu (2026-11-16 kalktı).
        self.E, self.KS, self.SR, self.tts, self.kbps = E, KS, E.SR, None, kbps
        self.surum = f"{self.surum}|{E.HIZ}"
        self.okunus = ses_metin.okuyucu(yol="uzun")

    def hazirla(self):
        if self.tts is None:
            self.tts = self.E.model_yukle()

    def paragraf(self, metin):
        """metin: zaten okunuş metni (ses_klip.seslendir okunus() uygular)."""
        self.hazirla()
        return self.E.paragraf_seslendir(self.tts, metin, hazir=True)

    def ses_metni(self, cumle, ek_kisaltma):
        return self.KS.uzat(cumle, ek_kisaltma)

    def mp3(self, pcm16):
        return self.E.mp3_kodla(pcm16, kbps=self.kbps)

    def log(self, s):
        self.E.log(s)


SESLER: dict[str, dict] = {
    "ema": {"sinif": Ema, "ad": "EMA", "varsayilan": True, "kbps": 48},
}


def ses_klasoru(brans: str, ses: str) -> Path:
    return MEDS / "data" / f"{brans}_cozucu" / ("ses" if SESLER[ses].get("varsayilan") else f"ses_{ses}")


cumlele, nokta = SK.cumlele, SK.nokta


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
        if q.get("anlatim"):  # ders içi ara soru (scripts/uretim/hoca_ara_soru): çözümü önceki slaytlardan anlatan klip
            k[f"a-{n}"] = cumlele(q["anlatim"]["ses"])
        for ad in list(k)[k0:]:
            k[ad] = [S.ses_metni(c, ekk) for c in k[ad]]
    return k


def seslendir(S: Saglayici, cumleler: list[str], kbps: int):
    return SK.seslendir(None, cumleler, okunus=S.okunus, kbps=kbps, E=S.E, paragraf=S.paragraf)


def _koru(klip: str) -> bool:
    # n-<no> kısa not ve no ≥ 1001 ek modül klipleri: Çıkmış çözücü (scripts/uretim/cikmis_paket/not_ses.py) bu klasörde yaşar, silinmez
    return klip.startswith("n-") or bool(re.match(r"[a-z]-\d{4}", klip))


def klasor(S: Saglayici, kok: Path, ad: str, K: dict[str, list[str]], kbps: int, silinsin: bool = True) -> None:
    S.okunus = ses_metin.okuyucu(yol="uzun", modul=kok.parent.name)
    SK.klasor(kok / ad, K, surum=S.surum, uret=lambda c: seslendir(S, c, kbps), silinsin=silinsin, koru=_koru)


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
