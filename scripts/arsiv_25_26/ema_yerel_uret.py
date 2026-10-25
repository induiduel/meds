#!/usr/bin/env python3
"""2025-2026 arşiv sesli dersleri için doğrudan GPU'da EMA Lightning sentezleyici.
cozucu_ses_gpu.sh aracılığıyla çalıştırılır (meds-gpuguard etkin + EMA_CIHAZ=cuda).

Kullanım:
  bash scripts/patoloji_cozucu/cozucu_ses_gpu.sh scripts/arsiv_25_26/ema_yerel_uret.py \
      --key y25-k2-01-norolojik-hastaya-yaklasim \
      --metin data/arsiv_25_26/sesli_anlatim/metin/y25-k2-01-norolojik-hastaya-yaklasim.md \
      --kok data/arsiv_25_26/sesli_anlatim
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

for _y in filter(None, os.environ.get("MEDS_EK_SITE", "").split(os.pathsep)):
    if _y not in sys.path:
        sys.path.append(_y)

GPU = os.environ.get("EMA_CIHAZ") == "cuda" and os.system("systemctl --user is-active --quiet meds-gpuguard") == 0
if not GPU:
    print("HATA: EMA sesleri yalnız GPU'da (meds-gpuguard etkin + cozucu_ses_gpu.sh ile) üretilebilir!", file=sys.stderr)
    sys.exit(75)

MEDS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MEDS / "scripts" / "sesli_anlatim"))
import ema_isci as EI  # noqa: E402


def fnv(s: str) -> str:
    h = 2166136261
    b = s.encode("utf-16-le")
    for i in range(0, len(b), 2):
        h = ((h ^ (b[i] | b[i + 1] << 8)) * 16777619) & 0xFFFFFFFF
    return format(h, "x")


def metin_paragraflari(md: str) -> list[dict]:
    """sesliAnlatim.ts::metinParagraflari ile birebir."""
    out = []
    tampon: list[str] = []
    bolum_baslik = ""
    bolum_basi = False

    def bitir():
        nonlocal tampon, bolum_basi
        t = re.sub(r"\s+", " ", " ".join(tampon)).strip()
        if t:
            out.append({"t": t, "bolumBasi": bolum_basi, "bolumBaslik": bolum_baslik})
            bolum_basi = False
        tampon = []

    for s in re.split(r"\r?\n", md):
        if s.startswith("# "):
            continue
        if s.startswith("@@"):
            bitir()
            bolum_baslik = s.replace("@@", "", 1).strip()
            bolum_basi = True
            continue
        if not s.strip():
            bitir()
        else:
            tampon.append(s.strip())
    bitir()
    return out


def metni_parcala(md: str, sinir: int = 3200) -> list[dict]:
    paragraflar = metin_paragraflari(md)
    out = []
    cur = None

    def it(c):
        out.append({
            "paragraflar": c["t"],
            "bolumBasi": c["bolumBasi"],
            "ilkParagraf": c["ilk"],
        })

    for idx, p in enumerate(paragraflar):
        uzun = (len("\n".join(cur["t"])) + len(p["t"])) if cur else 0
        if not cur or p["bolumBasi"] or uzun > sinir:
            if cur:
                it(cur)
            cur = {"t": [p["t"]], "bolumBasi": p["bolumBasi"], "ilk": idx}
        else:
            cur["t"].append(p["t"])
    if cur:
        it(cur)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", required=True)
    ap.add_argument("--metin", required=True)
    ap.add_argument("--kok", required=True)
    ap.add_argument("--zorla", action="store_true")
    a = ap.parse_args()

    kok = Path(a.kok)
    md_yol = Path(a.metin)
    md = md_yol.read_text(encoding="utf-8")
    mh = fnv(md)
    vid = "ema-yerel-ema"
    ses_yol = kok / "ses" / a.key / f"{vid}.mp3"
    kayit_yol = kok / "kayit.json"
    kayit = json.loads(kayit_yol.read_text(encoding="utf-8")) if kayit_yol.exists() else {}

    mevcut = next((v for v in (kayit.get(a.key) or []) if v.get("id") == vid), None)
    if not a.zorla and mevcut and mevcut.get("metinHash") == mh and ses_yol.exists() and ses_yol.stat().st_size == mevcut.get("bayt"):
        print(f"[{a.key}] EMA sesi güncel ({mevcut.get('sureSn')} sn, {mevcut.get('bayt')} bayt)")
        return 0

    # Kurul 2+ uzun kısaltma kuralını zorunlu aç (H3: "dee nee aa" vb.)
    EI.UZUN_KISALTMA = True
    EI.MODUL_OKUNUS = False
    tts = EI.model_yukle()
    parcalar = metni_parcala(md)

    tum_mp3 = bytearray()
    tum_zaman: list[list[float]] = []
    ofset = 0.0
    t0 = time.time()

    for i, p in enumerate(parcalar):
        pt = time.time()
        mp3, zaman, sure, notlar = EI.parca_uret(tts, p, i == 0)
        for bas, son in zaman:
            tum_zaman.append([round(ofset + bas, 3), round(ofset + son, 3)])
        tum_mp3.extend(mp3)
        ofset += sure
        print(f"  [{a.key}] parça {i + 1}/{len(parcalar)}: {sure:.1f} sn ses ({time.time() - pt:.1f} sn'de)", flush=True)

    ses_yol.parent.mkdir(parents=True, exist_ok=True)
    tmp_ses = ses_yol.with_suffix(".mp3.tmp")
    tmp_ses.write_bytes(bytes(tum_mp3))
    tmp_ses.replace(ses_yol)

    toplam_sure = round(len(tum_mp3) * 8 / (EI.KBPS * 1000), 2)
    varyant = {
        "id": vid,
        "saglayici": "ema-yerel",
        "ses": "Ema",
        "etiket": "Ema · EMA Lightning",
        "sureSn": round(toplam_sure),
        "bayt": len(tum_mp3),
        "metinHash": mh,
        "uretildi": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "zamanlama": tum_zaman,
    }
    import fcntl
    kayit_yol.parent.mkdir(parents=True, exist_ok=True)
    lock_yol = Path("/tmp/meds_arsiv_kayit.json.lock")
    with open(lock_yol, "w", encoding="utf-8") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        try:
            guncel_kayit = json.loads(kayit_yol.read_text(encoding="utf-8")) if kayit_yol.exists() else {}
        except Exception:
            guncel_kayit = {}
        liste = [v for v in (guncel_kayit.get(a.key) or []) if v.get("id") != vid]
        liste.insert(0, varyant)
        guncel_kayit[a.key] = liste
        tmp_k = kayit_yol.with_suffix(f".{os.getpid()}.json.tmp")
        tmp_k.write_text(json.dumps(guncel_kayit, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp_k.replace(kayit_yol)

    print(f"[{a.key}] EMA GPU ses tamamlandı: {toplam_sure:.1f} sn ({toplam_sure/60:.1f} dk), {len(tum_mp3)} bayt, {len(tum_zaman)} paragraf ({time.time() - t0:.1f} sn)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
