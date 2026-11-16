"""Ders analizi + ders özeti EMA seslendirmesi (her bölüm bir klip).

  bash meds/scripts/uretim/patoloji_cozucu/cozucu_ses_gpu.sh meds/scripts/uretim/ders_analizi/ses.py k2-01 [k2-02 …]   # boşsa: hepsi

EMA sesi DAİMA GPU başlatıcısıyla (AGENTS.md kural 10, 2. istisna; koruyucu kapalıysa çıkış 75, CPU'ya düşülmez).
Girdi : src/data/ders_analizi/<key>.json (scripts/uretim/ders_analizi/uret.py)
Çıktı : data/k<N>dersanaliz_cozucu/ses/<kod>/{a-*,o-*}.mp3 + kayit.json — /api/cozucu-ses/k<N>dersanaliz/ema/<kod>/<klip>.mp3
        (git dışı; Oracle'a rsync). Değişmeyen klip yeniden üretilmez (metin özeti).
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
from pathlib import Path

sys.path.insert(0, str(_kok.SCRIPTS / "uretim" / "spot_cozucu"))
from ses import MEDS, SESLER, kisaltmalar, klasor  # noqa: E402

GIRDI = MEDS / "src/data/ders_analizi"


def main() -> None:
    keyler = sys.argv[1:] or sorted(p.stem for p in GIRDI.glob("k*.json"))
    tanim = SESLER["ema"]
    S = tanim["sinif"]()
    for key in keyler:
        o = json.loads((GIRDI / f"{key}.json").read_text(encoding="utf-8"))
        K = {}
        for b in [*o["analiz"], *(o.get("ozet") or [])]:
            ekk = kisaltmalar(*b["ses"])
            K[b["klip"]] = [S.ses_metni(c, ekk) for c in b["ses"]]
        kok = MEDS / "data" / f"{o['sesKlasor']['brans']}_cozucu" / "ses"
        klasor(S, kok, o["sesKlasor"]["kod"], K, tanim["kbps"])


if __name__ == "__main__":
    main()
