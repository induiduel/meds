#!/usr/bin/env python3
"""Görüntüye bakılarak yazılmış şekil/tablo çapalarını (sekil.json: {"P3.C2": {"sekil", "resim", "tablo"}}) arşiv
dersinin çapa ve v2 dosyalarına işler (H59). Çapa "el": true ile işaretlenir; uygula_lazer_takip.py onu silmez.
Sonra işaret için: uygula_lazer_takip.py <key>.
Kullanım: python3 scripts/arsiv_25_26/sekil_capa_uygula.py <key> <sekil.json>"""
import json
import re
import sys
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
SA_KOK = MEDS / "data" / "arsiv_25_26" / "sesli_anlatim"
TASLAK = MEDS.parent / "meds_database_25_26" / "taslak"


def uygula(key: str, sekiller: dict) -> int:
    capa_yol, v2_yol = SA_KOK / "capa" / f"{key}.json", SA_KOK / "v2" / f"{key}.json"
    capa = json.loads(capa_yol.read_text(encoding="utf-8"))
    v2 = json.loads(v2_yol.read_text(encoding="utf-8"))
    vp = [p for b in v2.get("bolumler", []) for p in b.get("paragraflar", [])]
    n = 0
    for etiket, s in sekiller.items():
        m = re.fullmatch(r"P(\d+)\.C(\d+)", etiket)
        pn, ci = int(m.group(1)), int(m.group(2))
        alan = {"sekil": s["sekil"], "el": True}
        if s.get("resim") is not None:
            alan["resim"] = int(s["resim"])
        if s.get("tablo") not in (None, False):
            alan["tablo"] = s["tablo"]
        c = capa["p"][pn][ci]
        for k in ("madde", "resim", "tablo"):
            c.pop(k, None)
        c.update(alan)
        vc = vp[pn]["cumleler"][ci]
        assert vc["ses"].strip()[:40] == c["ses"][:40], f"{etiket}: v2 cümlesi çapayla eşleşmiyor"
        sl = vc.get("slayt") if isinstance(vc.get("slayt"), dict) else {"sayfa": c.get("sayfa")}
        for k in ("madde", "resim", "tablo"):
            sl.pop(k, None)
        sl.update(alan)
        vc["slayt"] = sl
        n += 1
    capa_yol.write_text(json.dumps(capa, ensure_ascii=False, indent=1), encoding="utf-8")
    v2_yol.write_text(json.dumps(v2, ensure_ascii=False, indent=1), encoding="utf-8")
    t = TASLAK / key
    if (t / "konusma_capalari.json").exists():
        (t / "konusma_capalari.json").write_text(json.dumps(capa["p"], ensure_ascii=False, indent=1), encoding="utf-8")
    if (t / "konusma_v2.json").exists():
        (t / "konusma_v2.json").write_text(json.dumps(v2, ensure_ascii=False, indent=1), encoding="utf-8")
    return n


if __name__ == "__main__":
    print(sys.argv[1], uygula(sys.argv[1], json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))), "çapa yazıldı")
