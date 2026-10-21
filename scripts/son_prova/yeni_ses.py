#!/usr/bin/env python3
"""Son Prova yeni örnek sorularının EMA klipleri (soru çözücüyle aynı biçim: q/i/s/c/d).

Girdi : meds_temp/son_prova/parca/<part>/aNN.json → "yeni_sorular" (YENI_SORU.md)
Çıktı : meds/data/<brans>_cozucu/ses/s<NN>/<klip>.mp3 + kayit.json   (NN = part anahtarındaki numara, ör. k1-81-… → s81)
Soru no = aşama no × 10 + sıra (ör. aşama 3'ün 2. sorusu → 32). Sunucu ucu: /api/cozucu-ses/<brans>/ema/s81/q-32.mp3
Kullanım (CPU, makine korunarak):
  systemd-run --user --scope -p CPUQuota=300% -p MemoryMax=2200M --nice=10 env CUDA_VISIBLE_DEVICES= EMA_IS_PARCACIGI=3 \
    ~/.local/share/meds-ema/venv/bin/python meds/scripts/son_prova/yeni_ses.py [part-key ...]
"""
import json
import os
import re
import sys
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
KOK = Path(os.environ.get("SON_PROVA_KOK") or MEDS.parent / "meds_temp/son_prova")  # Kurul 2+: meds_temp/son_prova_k<N>
sys.path.insert(0, str(MEDS / "scripts/spot_cozucu"))
import ses as SC  # noqa: E402


def sorular(part: dict) -> list[dict]:
    out = []
    for n, f in enumerate(sorted((KOK / "parca" / part["key"]).glob("a*.json")), 1):
        a = json.loads(f.read_text(encoding="utf-8"))
        for i, q in enumerate(a.get("yeni_sorular") or [], 1):
            t = lambda x: {"metin": x, "ses": x}  # noqa: E731
            out.append({"no": n * 10 + i, "soru": q["soru"], "kok_ses": q["soru"], "secenekler": q["secenekler"],
                        "secenek_ses": q["secenekler"], "dogru": q["dogru"], "ipucu": t(q["ipucu"]), "cozum": t(q["cozum"]),
                        "siklar": {h: t(v) for h, v in q["siklar"].items()}})
    return out


def main():
    plan = json.loads((KOK / "plan.json").read_text(encoding="utf-8"))
    istek = sys.argv[1:]
    S = SC.Ema()
    for p in plan["partlar"]:
        if istek and p["key"] not in istek:
            continue
        qs = sorular(p)
        if not qs:
            print(f"{p['key']}: yeni soru yok", flush=True)
            continue
        kl = "s" + re.match(r"k\d+-(\d+)-", p["key"]).group(1)
        SC.klasor(S, SC.ses_klasoru(p["brans"], "ema"), kl, SC.klipler({"sorular": qs}, S), SC.SESLER["ema"]["kbps"])


if __name__ == "__main__":
    main()
