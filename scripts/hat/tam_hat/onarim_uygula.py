#!/usr/bin/env python3
"""Onarım yanıtını soru dosyasına işler (onarim_paketi.py'nin eşi; LLM yok).

Yanıt biçimi (alt ajan yazar): {"<soru id>": {"<şık harfi>": "yeni şık açıklaması", ...}, ...}
Güvenlik:
  · yalnız paketin işaretlediği alanlar (meds_temp/onarim/<dosya>.json) değişir; başka alan → HATA, hiçbiri yazılmaz
  · ham dosyada eski metnin JSON kaçışlı hâli birebir ve TEK kez bulunmalı → yalnız o dize değişir (biçim/girinti korunur)
  · yeni metin 20–55 kelime, "(s. N)" kaynak etiketi taşır

  python3 scripts/hat/tam_hat/onarim_uygula.py <soru dosyası> <yanıt.json> [--kuru]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

_d = Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
sys.path.append(str(_d))
import kok as _kok  # noqa: E402

KOK = _kok.MEDS
ONARIM = KOK.parent / "meds_temp" / "onarim"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dosya", type=Path)
    ap.add_argument("yanit", type=Path)
    ap.add_argument("--kuru", action="store_true")
    a = ap.parse_args()
    dosya = a.dosya if a.dosya.is_absolute() else KOK / a.dosya
    ham = dosya.read_text(encoding="utf-8")
    veri = json.loads(ham)
    Q = {q["id"]: q for k in veri.get("kazanimlar", []) for q in k.get("sorular", [])}
    izin = json.loads((ONARIM / f"{dosya.stem}.json").read_text(encoding="utf-8"))
    yanit = json.loads(a.yanit.read_text(encoding="utf-8"))
    hata, degis = [], []
    for qid, siklar in yanit.items():
        if qid not in Q:
            hata.append(f"{qid}: soru yok")
            continue
        for h, yeni in siklar.items():
            if h not in izin.get(qid, []) and not (izin.get(qid) == [""]):
                hata.append(f"{qid}.{h}: pakette işaretli değil (dokunma)")
                continue
            eski = (Q[qid].get("sik_aciklamalari") or {}).get(h)
            yeni = re.sub(r"\s+", " ", yeni).strip()
            n = len(yeni.split())
            if not eski:
                hata.append(f"{qid}.{h}: eski açıklama yok")
            elif not 20 <= n <= 55:
                hata.append(f"{qid}.{h}: {n} kelime (20–55)")
            elif not re.search(r"\(s\.\s*\d", yeni):
                hata.append(f"{qid}.{h}: kaynak etiketi (s. N) yok")
            else:
                ek, yk = json.dumps(eski, ensure_ascii=False)[1:-1], json.dumps(yeni, ensure_ascii=False)[1:-1]
                # konuma göre: sorunun kimliğinden sonraki "sik_aciklamalari" içinde "<harf>": "<eski>" (aynı metin
                # aciklama alanında da geçebilir; ham metin araması o yüzden yetmiyordu — H619)
                bas = ham.find(f'"id": "{qid}"') if f'"id": "{qid}"' in ham else ham.find(f'"id":"{qid}"')
                son = ham.find('"id":', bas + 5)
                son = len(ham) if son < 0 else son
                sa = ham.find("sik_aciklamalari", bas, son)
                anahtar = next((x for x in (f'"{h}": "{ek}"', f'"{h}":"{ek}"') if sa >= 0 and ham.find(x, sa, son) >= 0), None)
                if bas < 0 or anahtar is None:
                    hata.append(f"{qid}.{h}: şık açıklaması dosyada konumuyla bulunamadı")
                else:
                    konum = ham.find(anahtar, sa, son)
                    degis.append((konum, anahtar, anahtar.replace(ek, yk, 1)))
    for x in hata:
        print("HATA", x)
    if hata:
        print(f"{len(hata)} HATA — hiçbir değişiklik yazılmadı")
        return 1
    for konum, eski_k, yeni_k in sorted(degis, reverse=True):  # sondan başa: önceki konumlar kaymaz
        ham = ham[:konum] + yeni_k + ham[konum + len(eski_k):]
    json.loads(ham)  # geçerli JSON kalmalı
    if not a.kuru:
        dosya.write_text(ham, encoding="utf-8")
    print(f"{len(degis)} şık açıklaması {'(kuru) ' if a.kuru else ''}güncellendi → {dosya.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
