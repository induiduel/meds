#!/usr/bin/env python3
"""Son Prova: denetimde yeniden yazılan soruları uygular ve seslendirir (soru çözücü havuzuna DOKUNMAZ).

Girdi : meds_temp/son_prova/duzelt/cikti_*.json ({ref, karar, soru, secenekler, dogru, ipucu, siklar, cozum, zorluk, sayfa})
Her düzeltilen soru Son Prova'ya özel yeni kimlik alır: <brans>/t0N#<no>  (t0N = branş klasörü: patoloji t01 … farmakoloji t07),
eşleme duzelt/eslem.json'da kalıcı (aynı eski kimlik hep aynı yeni numarayı alır). index.json'daki tüm listelerde (aşama, check-up,
genel, deneme) eski kimlik yenisiyle değişir; sorular/<brans>.json'a yeni kayıt eklenir. Sesler: data/<brans>_cozucu/ses/t0N/
(soru çözücü EMA motoru, q/i/s/c/d klipleri). Kullanım (CPU, korumalı):
  systemd-run --user --scope -p CPUQuota=300% -p MemoryMax=2200M --nice=10 env CUDA_VISIBLE_DEVICES= EMA_IS_PARCACIGI=3 \
    ~/.local/share/meds-ema/venv/bin/python meds/scripts/son_prova/duzelt_uygula.py [--sessiz]
"""
import glob
import json
import sys
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
DZ = MEDS.parent / "meds_temp/son_prova/duzelt"
OUT = MEDS / "src/data/son_prova/k1"
KLASOR = {"patoloji": "t01", "enfeksiyon": "t02", "genetik": "t03", "uroloji": "t04", "halksagligi": "t05",
          "kadindogum": "t06", "farmakoloji": "t07"}


def main():
    sessiz = "--sessiz" in sys.argv
    cik = {}
    for f in sorted(glob.glob(str(DZ / "cikti_*.json"))):
        for q in json.loads(Path(f).read_text(encoding="utf-8")):
            cik[q["ref"]] = q
    ep = DZ / "eslem.json"
    eslem = json.loads(ep.read_text(encoding="utf-8")) if ep.exists() else {}
    ix = json.loads((OUT / "index.json").read_text(encoding="utf-8"))
    sor = {f.stem: json.loads(f.read_text(encoding="utf-8")) for f in (OUT / "sorular").glob("*.json")}
    sayac = {}
    for yeni in eslem.values():
        b, n = yeni.split("/")[0], int(yeni.split("#")[1])
        sayac[b] = max(sayac.get(b, 0), n)
    for eski, q in cik.items():
        b = eski.split("/")[0]
        if eski not in eslem:
            sayac[b] = sayac.get(b, 0) + 1
            eslem[eski] = f"{b}/{KLASOR[b]}#{sayac[b]}"
    # ses
    klip = {}
    if not sessiz:
        sys.path.insert(0, str(MEDS / "scripts/spot_cozucu"))
        import ses as SC
        S = SC.Ema()
        for b in KLASOR:
            qs = []
            for eski, q in cik.items():
                if eski.split("/")[0] != b:
                    continue
                n = int(eslem[eski].split("#")[1])
                t = lambda x: {"metin": x, "ses": x}  # noqa: E731
                qs.append({"no": n, "soru": q["soru"], "kok_ses": q["soru"], "secenekler": q["secenekler"], "secenek_ses": q["secenekler"],
                           "dogru": q["dogru"], "ipucu": t(q["ipucu"]), "cozum": t(q["cozum"]), "siklar": {h: t(v) for h, v in q["siklar"].items()}})
            if qs:
                SC.klasor(S, SC.ses_klasoru(b, "ema"), KLASOR[b], SC.klipler({"sorular": qs}, S), SC.SESLER["ema"]["kbps"])
    for b, kl in KLASOR.items():
        kp = MEDS / f"data/{b}_cozucu/ses/{kl}/kayit.json"
        if kp.exists():
            klip[b] = json.loads(kp.read_text(encoding="utf-8"))
    # sorular + index
    for eski, q in cik.items():
        b = eski.split("/")[0]
        yeni = eslem[eski]
        n = int(yeni.split("#")[1])
        k = klip.get(b, {})
        kl_v = {t: k[f"{t}-{n}"]["h"] for t in "qicd" if f"{t}-{n}" in k}
        kl_v.update({f"s{h}": k[f"s-{n}-{h}"]["h"] for h in "ABCDE" if f"s-{n}-{h}" in k})
        onceki = sor[b].get(eski) or sor[b].get(yeni)
        if onceki is None:
            print(f"UYARI kayıt yok: {eski}")
            continue
        sor[b][yeni] = {
            "soru": q["soru"], "secenekler": q["secenekler"], "dogru": q["dogru"], "ipucu": q["ipucu"], "siklar": q["siklar"],
            "cozum": q["cozum"], "tur": onceki.get("tur") if q["karar"] == "duzelt" else "yeni",
            **({"sinav": onceki["sinav"]} if q["karar"] == "duzelt" and onceki.get("sinav") else {}),
            "zorluk": q.get("zorluk") or onceki.get("zorluk"),
            "kaynak": {"kod": onceki["kaynak"]["kod"], "s": q.get("sayfa") or onceki["kaynak"]["s"]},
            "asama": onceki["asama"], "kl": KLASOR[b], "klip": kl_v,
        }
        sor[b].pop(eski, None)

    def degis(liste):
        return [eslem.get(r, r) for r in liste]
    for d in ix["dersler"]:
        d["genel"] = degis(d["genel"])
        for p in d["partlar"]:
            for a in p["asamalar"]:
                a["sorular"] = degis(a["sorular"])
                a["checkup"] = degis(a["checkup"])
    for dn in ix["denemeler"]:
        dn["sorular"] = degis(dn["sorular"])
    for b, qs in sor.items():
        (OUT / "sorular" / f"{b}.json").write_text(json.dumps(qs, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    (OUT / "index.json").write_text(json.dumps(ix, ensure_ascii=False, indent=1), encoding="utf-8")
    ep.write_text(json.dumps(eslem, ensure_ascii=False, indent=1), encoding="utf-8")
    eksik = [eslem[e] for e in cik if len(sor[e.split('/')[0]].get(eslem[e], {}).get("klip", {})) < 9]
    print(f"{len(cik)} soru uygulandı; klibi eksik: {len(eksik)} {eksik[:5]}")


if __name__ == "__main__":
    main()
