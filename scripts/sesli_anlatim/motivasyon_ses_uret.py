#!/usr/bin/env python3
"""Sesli ders motivasyon klipleri: src/data/sesli_motivasyon/havuz.json → public/ses/motivasyon/<id>.mp3 (EMA, yalnız CPU).

Ders seslerine dokunmaz; klipler ayrı dosyadır, oynatıcı (canliDersMotivasyon.ts) dersin başında/ortasında/sonunda ve
molada ayrı bir ses öğesiyle çalar. Metni değişen ya da sesi olmayan satır yeniden üretilir (metin karması sidecar'da).
Kullanım: ~/.local/share/meds-ema/venv/bin/python scripts/sesli_anlatim/motivasyon_ses_uret.py [--hepsi]
"""
from __future__ import annotations
import hashlib, json, os, sys
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ.setdefault("EMA_IS_PARCACIGI", "2")
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ema_isci as E  # noqa: E402

KOK = Path(__file__).resolve().parents[2]
HAVUZ = KOK / "src/data/sesli_motivasyon/havuz.json"
CIKTI = KOK / "public/ses/motivasyon"


def main() -> None:
    hepsi = "--hepsi" in sys.argv
    CIKTI.mkdir(parents=True, exist_ok=True)
    satirlar = json.loads(HAVUZ.read_text())["satirlar"]
    karma_yol = CIKTI / "karma.json"
    karma = json.loads(karma_yol.read_text()) if karma_yol.exists() else {}
    is_ = [s for s in satirlar if hepsi or karma.get(s["id"]) != hashlib.sha1(s["metin"].encode()).hexdigest()[:12]
           or not (CIKTI / f"{s['id']}.mp3").exists()]
    sureler = {}
    if is_:
        tts = E.model_yukle()
        for s in is_:
            mp3, _z, sure, notlar = E.parca_uret(tts, {"paragraflar": [s["metin"]], "bolumBasi": False}, True)
            (CIKTI / f"{s['id']}.mp3").write_bytes(mp3)
            karma[s["id"]] = hashlib.sha1(s["metin"].encode()).hexdigest()[:12]
            sureler[s["id"]] = round(sure, 2)
            E.log(f"{s['id']}: {sure:.1f} sn {notlar or ''}")
    # artık havuzda olmayan klipler silinir
    ids = {s["id"] for s in satirlar}
    for f in CIKTI.glob("*.mp3"):
        if f.stem not in ids:
            f.unlink()
    karma = {k: v for k, v in karma.items() if k in ids}
    karma_yol.write_text(json.dumps(karma, ensure_ascii=False, indent=0))
    E.log(f"tamam: {len(is_)} üretildi, {len(satirlar)} satır")


if __name__ == "__main__":
    main()
