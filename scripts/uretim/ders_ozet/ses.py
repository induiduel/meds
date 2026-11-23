#!/usr/bin/env python3
"""Ders Özeti — EMA seslendirme (klip başına bir bölüm). GPU ZORUNLU (AGENTS kural 10): yalnız başlatıcıyla çağrılır:

  bash scripts/uretim/patoloji_cozucu/cozucu_ses_gpu.sh meds/scripts/uretim/ders_ozet/ses.py k2-15 [k2-xx ...]

Girdi : meds_temp/ders_ozet/<k>/ozet.json (dogrula.py 0 HATA)
Çıktı : data/k<N>ozet_cozucu/ses/<kod>/{g,b-1..b-n,a}.mp3 + kayit.json (ses_klip.klasor: değişmeyen klip yeniden üretilmez)
        g = giriş · b-i = i. bölüm (başlık + maddeler) · a = "Akılda kalması gerekenler"
Sunucu adresi (değişiklik gerekmez): /api/cozucu-ses/k<N>ozet/ema/<kod>/<klip>.mp3
Cümle → madde eşlemesi `klip_cumleleri()` ile yapılır; yayinla.py aynı işlevi kullanır (tek kaynak).
"""
from __future__ import annotations

import sys
from pathlib import Path as _P

_s = _P(__file__).resolve()
while not (_s / "kok.py").exists() and _s != _s.parent:
    _s = _s.parent
sys.path.insert(0, str(_s))
from kok import MEDS, PROJE, SCRIPTS  # noqa: E402

import json  # noqa: E402
import re  # noqa: E402

KOK = PROJE / "meds_temp" / "ders_ozet"


def sade(m: str) -> str:
    return re.sub(r"\*\*(.+?)\*\*", r"\1", m or "").strip()


def cumleler(m: str) -> list[str]:
    """Ekranda bir madde → okunacak cümleler (ses_klip.cumlele ile aynı bölme)."""
    sys.path.insert(0, str(SCRIPTS / "uretim/ses_ortak"))
    import ses_klip as SK
    return SK.cumlele(sade(m))


def klip_cumleleri(o: dict) -> dict[str, list[tuple[str, list[str]]]]:
    """klip → [(öğe kimliği, cümleler)]; öğe: 'baslik', madde id, 'akilda-i', 'giris'."""
    K: dict[str, list[tuple[str, list[str]]]] = {"g": [("giris", cumleler(o["giris"]))]}
    for i, b in enumerate(o["bolumler"], 1):
        K[f"b-{i}"] = [("baslik", [sade(b["baslik"]).rstrip(".") + "."])] + [(m["id"], cumleler(m["metin"])) for m in b["maddeler"]]
    K["a"] = [("baslik", ["Akılda kalması gerekenler."])] + [(f"akilda-{j}", cumleler(a["metin"])) for j, a in enumerate(o["akilda"], 1)]
    return K


def klasor_adi(o: dict, g: dict) -> tuple[str, str]:
    return f"k{g['kurul']}ozet", g["kod"]


def main() -> None:
    ks = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not ks:
        raise SystemExit(__doc__)
    import os
    if os.environ.get("EMA_CIHAZ") != "cuda":
        print("EMA sesi DAİMA GPU: cozucu_ses_gpu.sh ile çalıştır (kural 10)")
        sys.exit(75)
    import importlib.util as IU  # spot_cozucu/ses.py: Ema sağlayıcısı + klasor() (ad çakışması: bu dosya da ses.py)
    sp = IU.spec_from_file_location("spot_ses", SCRIPTS / "uretim/spot_cozucu/ses.py")
    SP = IU.module_from_spec(sp)
    sp.loader.exec_module(SP)
    import subprocess
    S = SP.Ema(kbps=48)
    for k in ks:
        r = subprocess.run([sys.executable, str(SCRIPTS / "uretim/ders_ozet/dogrula.py"), k], capture_output=True, text=True)
        if r.returncode:
            print(r.stdout[-2000:])
            raise SystemExit(f"{k}: kapı 0 HATA değil — ses üretilmedi")
        o = json.loads((KOK / k / "ozet.json").read_text(encoding="utf-8"))
        g = json.loads((KOK / k / "girdi.json").read_text(encoding="utf-8"))
        brans, kod = klasor_adi(o, g)
        K = {}
        for klip, ogeler in klip_cumleleri(o).items():
            hepsi = [c for _, cc in ogeler for c in cc]
            ekk = SP.kisaltmalar(*hepsi)
            K[klip] = [S.ses_metni(c, ekk) for c in hepsi]
        SP.klasor(S, MEDS / "data" / f"{brans}_cozucu" / "ses", kod, K, 48)


if __name__ == "__main__":
    main()
