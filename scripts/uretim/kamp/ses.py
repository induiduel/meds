#!/usr/bin/env python3
"""Kurul kampı EMA sesi: anlatım maddeleri + deneme (kök + şıklar, her şıkkın açıklaması). Kurul 2+ uzun kısaltma okunuşu.
Klipler data/kamp/ses/k<N>/<brans>/<id>.mp3 (+ <id>-<harf>.mp3); kamp JSON'una "ses": {anahtar: "dosya?v=karma"} yazılır.
Metni değişmeyen klip yeniden üretilmez. Çalıştırma: EMA venv, makine korumalı kapsam (CPU):
  systemd-run --user --scope -p CPUQuota=300% -p MemoryMax=2200M ~/.local/share/meds-ema/venv/bin/python ses.py <kamp.json>
"""
# Konum-bağımsız kök (2026-11-16): sabit parents[N] yerine scripts/kok.py (dosya taşınsa da doğru).
import sys as _sys
from pathlib import Path as _Path
_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402
import hashlib, json, sys
from pathlib import Path

MEDS = _kok.MEDS
sys.path.insert(0, str(MEDS / "scripts/uretim/sesli_anlatim")); sys.path.insert(0, str(MEDS / "scripts/uretim/ses_ortak"))
import ema_isci as E  # noqa: E402
import ses_klip as SK  # noqa: E402  (2026-11-16: E.uzun_kisaltma_ayarla genel durumu yerine ortak klip + okunuş)
import ses_metin  # noqa: E402

KBPS = 48  # eski ogren_ses_uret.KBPS (dosya biçimi aynı kalır)


def main():
    yol = Path(sys.argv[1]); k = json.loads(yol.read_text())
    okunus = ses_metin.okuyucu(ders=f"k{k['kurul']}-kamp")  # yol veriden: k<N>-kamp → kurul N
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
        try:
            mp3, _, _, _ = SK.seslendir(tts, cumleler, okunus=okunus, kbps=KBPS, E=E)
        except SK.BozukKlip as e:
            SK.bozuk_kaydet(klasor=str(hedef), klip=anahtar, hata=str(e), karakter=sum(map(len, cumleler)))
            print(f"HATA {anahtar}: {e} — klip yazılmadı"); continue
        SK.atomik_yaz(dosya, mp3); ses[anahtar] = f"{anahtar}.mp3?v={h}"; n += 1
    k["ses"] = ses
    yol.write_text(json.dumps(k, ensure_ascii=False, indent=1))
    print(f"kamp sesi: {n} yeni klip · toplam {len(ses)}")


if __name__ == "__main__":
    main()
