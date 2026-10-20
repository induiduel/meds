#!/usr/bin/env python3
"""Kurul kampı EMA sesi: anlatım maddeleri + deneme (kök + şıklar, her şıkkın açıklaması). Kurul 2+ uzun kısaltma okunuşu.
Klipler data/kamp/ses/k<N>/<brans>/<id>.mp3 (+ <id>-<harf>.mp3); kamp JSON'una "ses": {anahtar: "dosya?v=karma"} yazılır.
Metni değişmeyen klip yeniden üretilmez. Çalıştırma: EMA venv, makine korumalı kapsam (CPU):
  systemd-run --user --scope -p CPUQuota=300% -p MemoryMax=2200M ~/.local/share/meds-ema/venv/bin/python ses.py <kamp.json>
"""
import hashlib, json, sys
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MEDS / "scripts/sesli_anlatim")); sys.path.insert(0, str(MEDS / "scripts/ogren_ses"))
import ema_isci as E  # noqa: E402
import ogren_ses_uret as O  # noqa: E402


def main():
    yol = Path(sys.argv[1]); k = json.loads(yol.read_text())
    E.uzun_kisaltma_ayarla(f"k{k['kurul']}-kamp")
    kok = Path(sys.argv[sys.argv.index("--ses-kok") + 1]) if "--ses-kok" in sys.argv else MEDS / "data/kamp/ses"
    hedef = kok / f"k{k['kurul']}" / k["brans"]; hedef.mkdir(parents=True, exist_ok=True)
    isler = [(a["id"], [a["baslik"] + ".", a["metin"]]) for a in k["anlatim"]]
    for q in k["deneme"]:
        isler.append((q["id"], [q["kok"]] + [f"{h} şıkkı: {m}" for h, m in q["secenekler"].items()]))
        isler += [(f"{q['id']}-{h.lower()}", [a]) for h, a in q["aciklama"].items()]
    tts, ses, n = None, dict(k.get("ses") or {}), 0
    for anahtar, cumleler in isler:
        h = hashlib.sha1(("kamp-ema-2|" + "\n".join(cumleler)).encode()).hexdigest()[:12]
        dosya = hedef / f"{anahtar}.mp3"
        if ses.get(anahtar, "").endswith(h) and dosya.exists():
            continue
        tts = tts or E.model_yukle()
        mp3, _, _, _ = O.seslendir(tts, cumleler)
        dosya.write_bytes(mp3); ses[anahtar] = f"{anahtar}.mp3?v={h}"; n += 1
    k["ses"] = ses
    yol.write_text(json.dumps(k, ensure_ascii=False, indent=1))
    print(f"kamp sesi: {n} yeni klip · toplam {len(ses)}")


if __name__ == "__main__":
    main()
