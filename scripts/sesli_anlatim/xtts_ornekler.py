#!/usr/bin/env python3
"""XTTS v2 hazır konuşmacılarının dinleme örneklerini üretir (panelde "Dinle").

Çıktı: data/sesli_anlatim/ornek/xtts-yerel-<ses-slug>.mp3 (var olan atlanır) + ornek/xtts_konusmacilar.json (tam liste).
GPU/ısı sınırları xtts_isci.py ile aynı (en fazla %70, 80/70 °C). Kullanım: xtts_ornekler.py [--hepsi-yeniden]
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
sp = importlib.util.spec_from_file_location("xtts_isci", MEDS / "scripts/sesli_anlatim/xtts_isci.py")
x = importlib.util.module_from_spec(sp)
sp.loader.exec_module(x)

METIN = ("Tümör biyolojisinde ilk kavram neoplazidir. Neoplazi, hücrelerin kontrolsüz ve amaçsız çoğalmasıdır; "
         "uyaran ortadan kalksa bile büyüme sürer. Burası önemli: benign tümörler kapsüllüdür ve metastaz yapmaz.")
OUT = MEDS / "data/sesli_anlatim/ornek"
OUT.mkdir(parents=True, exist_ok=True)
slug = lambda s: re.sub(r"^-|-$", "", re.sub(r"[^a-z0-9]+", "-", s.lower()))  # noqa: E731 — sesliAnlatim.ts::sesSlug

tts = x.model_yukle()
sesler = sorted(tts.speakers)
(OUT / "xtts_konusmacilar.json").write_text(json.dumps(sesler, ensure_ascii=False, indent=1), encoding="utf-8")
for ses in sesler:
    f = OUT / f"xtts-yerel-{slug(ses)}.mp3"
    if f.exists() and "--hepsi-yeniden" not in sys.argv:
        continue
    mp3, _, sure, notlar = x.parca_uret(tts, {"paragraflar": [METIN], "bolumBasi": False}, True, ses)
    f.write_bytes(mp3)
    x.log(f"{ses}: {sure:.1f} sn {notlar or ''}")
x.log(f"{len(sesler)} konuşmacı")
