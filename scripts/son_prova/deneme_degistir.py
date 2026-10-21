#!/usr/bin/env python3
"""Deneme denetiminde işaretlenen soruları değiştirir; denemelerin öteki soruları AYNEN kalır.

Girdi: deneme_denetim/sonuc_*.json ({ref, deneme, sorun, agirlik}); deneme_denetim/haric.json (önceki turlarda reddedilenler, birikir)
Her reddedilen soru, aynı dersin (kaynak kodu) Son Prova'da hiç kullanılmamış, reddedilmemiş, kökü tekrar etmeyen bir sorusuyla
değişir (zorluk: orta > kolay > çıkmış; zor yok). Değişenler deneme_denetim/yeni_tur.json'a yazılır (yeniden denetim için).
Kullanım: python3 meds_temp/son_prova/deneme_degistir.py
"""
import glob
import json
import random
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent
sys.path.insert(0, str(KOK))
from soru_dagit import havuz_yukle, kok_anahtar, slayt_kodu  # noqa: E402

MEDS = KOK.parents[1] / "meds"
OUT = MEDS / "src/data/son_prova/k1"
DD = KOK / "deneme_denetim"


def main():
    ix = json.loads((OUT / "index.json").read_text(encoding="utf-8"))
    sor = {}
    for f in sorted((OUT / "sorular").glob("*.json")):
        sor[f.stem] = json.loads(f.read_text(encoding="utf-8"))
    haric = set(json.loads((DD / "haric.json").read_text(encoding="utf-8"))) if (DD / "haric.json").exists() else set()
    ret = {}
    for f in glob.glob(str(DD / "sonuc_*.json")):
        for x in json.loads(Path(f).read_text(encoding="utf-8")):
            ret[x["ref"]] = x
    haric |= set(ret)
    kullanilan = {r for b in sor.values() for r in b}
    koks = {kok_anahtar(q["soru"]) for b in sor.values() for q in b.values()}
    rnd = random.Random(7)
    puan = {"orta": 0, None: 1, "kolay": 1, "zor": 9}
    yeni_tur, degisen = [], 0
    for dn in ix["denemeler"]:
        for i, r in enumerate(dn["sorular"]):
            if r not in haric:
                continue
            b = r.split("/")[0]
            eski = sor[b][r]
            havuz = havuz_yukle(b)
            aday = [k for k, q in havuz.items() if slayt_kodu(b, q["_kod"]) == eski["kaynak"]["kod"] and k not in kullanilan
                    and k not in haric and kok_anahtar(q["soru"]) not in koks and q.get("dogru") in (q.get("secenekler") or {})
                    and q.get("zorluk") != "zor"]
            if not aday:  # aynı ders yoksa branşın kalanı
                aday = [k for k, q in havuz.items() if k not in kullanilan and k not in haric and kok_anahtar(q["soru"]) not in koks
                        and q.get("zorluk") != "zor"]
            rnd.shuffle(aday)
            aday.sort(key=lambda k: puan.get(havuz[k].get("zorluk"), 1) + (0.5 if havuz[k].get("tur") == "cikmis" else 0))
            if not aday:
                print(f"HATA yerine soru yok: {r}")
                continue
            y = aday[0]
            q = havuz[y]
            sor[b][y] = {
                "soru": q["soru"], "secenekler": q["secenekler"], "dogru": q["dogru"], "ipucu": q.get("ipucu", ""),
                "siklar": q.get("siklar", {}), "cozum": q.get("cozum", ""), "tur": q.get("tur"),
                **({"sinav": q["sinav"]} if q.get("sinav") else {}), **({"zorluk": q["zorluk"]} if q.get("zorluk") else {}),
                "kaynak": {"kod": slayt_kodu(b, q["_kod"]), "s": q.get("sayfa") or []},
                "asama": eski["asama"], "kl": q["_kl"], "klip": q["_klip"],
            }
            sor[b].pop(r, None)
            dn["sorular"][i] = y
            kullanilan.add(y)
            koks.add(kok_anahtar(q["soru"]))
            degisen += 1
            yeni_tur.append({"deneme": dn["no"], "ref": y, "yerine": r, "sorun_eski": ret.get(r, {}).get("sorun", "önceki tur")})
    for b, qs in sor.items():
        (OUT / "sorular" / f"{b}.json").write_text(json.dumps(qs, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    (OUT / "index.json").write_text(json.dumps(ix, ensure_ascii=False, indent=1), encoding="utf-8")
    (DD / "haric.json").write_text(json.dumps(sorted(haric), ensure_ascii=False, indent=1), encoding="utf-8")
    (DD / "yeni_tur.json").write_text(json.dumps(yeni_tur, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{degisen} soru değişti; yeniden denetim için deneme_denetim/yeni_tur.json")


if __name__ == "__main__":
    main()
