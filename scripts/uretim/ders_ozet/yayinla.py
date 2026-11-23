#!/usr/bin/env python3
"""Ders Özeti — site verisine yayın. Kapı (dogrula.py) 0 HATA + bağımsız denetçi GEÇER + ses tam olmadan yazmaz.

Girdi : meds_temp/ders_ozet/<k>/{ozet.json, girdi.json, denetim.json}, data/k<N>ozet_cozucu/ses/<kod>/kayit.json
Çıktı : src/data/ders_ozet/k<N>/<k>.json  (ekran + ses zamanları) ve src/data/ders_ozet/k<N>/index.json (ders listesi)
  ders dosyası: {ders, key, kod, kurul, brans, baslik, ogretim_uyesi, giris, bolumler[{id,baslik,maddeler[{id,tur,metin,s,cikmis}]}],
                 akilda[{metin,s,cikmis}], cikmis[{id,kok,cevap,yil,s}], cozucu{brans,kod,soru,cikmis}|null,
                 ses{brans,kod,klipler{klip:{v,sure,oge{oge_id:[bas,son]}}}}, sure, kelime}
denetim.json: {"karar": "GEÇER", "denetci": "...", "tarih": "...", "bulgular": [...]} (bağımsız denetçi alt ajan yazar)
Kullanım: python3 scripts/uretim/ders_ozet/yayinla.py k2-15 [--sessiz-izin]  (--sessiz-izin: ses yoksa da yaz — yalnız sınama)
"""
from __future__ import annotations

import sys
from pathlib import Path as _P

_s = _P(__file__).resolve()
while not (_s / "kok.py").exists() and _s != _s.parent:
    _s = _s.parent
sys.path.insert(0, str(_s))
from kok import MEDS, PROJE, SCRIPTS  # noqa: E402

import json  # noqa: E402
import subprocess  # noqa: E402

sys.path.insert(0, str(SCRIPTS / "uretim/ders_ozet"))
from ses import klip_cumleleri, klasor_adi  # noqa: E402

KOK = PROJE / "meds_temp" / "ders_ozet"


def yayinla(k: str, sessiz_izin: bool) -> None:
    r = subprocess.run([sys.executable, str(SCRIPTS / "uretim/ders_ozet/dogrula.py"), k], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stdout[-1500:] + f"\n{k}: kapı 0 HATA değil — yayın yok")
    d = KOK / k
    den = json.loads((d / "denetim.json").read_text(encoding="utf-8")) if (d / "denetim.json").exists() else {}
    if den.get("karar") != "GEÇER":
        raise SystemExit(f"{k}: bağımsız denetçi GEÇER yok (denetim.json) — yayın yok")
    o = json.loads((d / "ozet.json").read_text(encoding="utf-8"))
    g = json.loads((d / "girdi.json").read_text(encoding="utf-8"))
    brans, kod = klasor_adi(o, g)
    kp = MEDS / "data" / f"{brans}_cozucu" / "ses" / kod / "kayit.json"
    kayit = json.loads(kp.read_text(encoding="utf-8")) if kp.exists() else {}
    klipler = {}
    eksik = []
    for klip, ogeler in klip_cumleleri(o).items():
        x = kayit.get(klip)
        if not x:
            eksik.append(klip)
            continue
        z = x.get("zaman") or []
        oge, i = {}, 0
        for oid, cc in ogeler:
            n = len(cc)
            if z[i:i + n]:
                oge[oid] = [round(z[i][0], 2), round(z[min(i + n, len(z)) - 1][1], 2)]
            i += n
        if i != len(z):
            eksik.append(f"{klip}(cümle sayısı {len(z)}≠{i})")
        klipler[klip] = {"v": x["h"], "sure": round(x["sure"], 2), "oge": oge}
    if eksik and not sessiz_izin:
        raise SystemExit(f"{k}: ses eksik/uyumsuz {eksik} — önce ses.py (GPU)")
    coz = g.get("cozucu")
    sorular = g.get("sorular") or []
    cikti = {
        "ders": k, "key": g["key"], "kod": g["kod"], "kurul": g["kurul"], "brans": g.get("brans"), "baslik": o["baslik"],
        "ogretim_uyesi": g.get("ogretim_uyesi"), "giris": o["giris"],
        "bolumler": [{"id": b["id"], "baslik": b["baslik"],
                      "maddeler": [{k2: m[k2] for k2 in ("id", "tur", "metin", "s", "cikmis") if k2 in m} for m in b["maddeler"]]}
                     for b in o["bolumler"]],
        "akilda": [{k2: a[k2] for k2 in ("metin", "s", "cikmis") if k2 in a} for a in o["akilda"]],
        "cikmis": [{k2: c.get(k2) for k2 in ("id", "kok", "cevap", "yil", "s")} for c in g["cikmis"]],
        "cozucu": {**coz, "soru": len(sorular), "cikmis": sum(q.get("tur") == "cikmis" for q in sorular)} if coz else None,
        "ses": {"brans": brans, "kod": kod, "klipler": klipler} if klipler else None,
        "sure": round(sum(x["sure"] for x in klipler.values())),
        "kelime": None,
    }
    import dogrula as D
    cikti["kelime"] = D.dogrula(k)[2].get("kelime")
    od = MEDS / "src/data/ders_ozet" / f"k{g['kurul']}"
    od.mkdir(parents=True, exist_ok=True)
    (od / f"{k}.json").write_text(json.dumps(cikti, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    ix_p = od / "index.json"
    ix = json.loads(ix_p.read_text(encoding="utf-8")) if ix_p.exists() else {"kurul": g["kurul"], "dersler": []}
    ix["dersler"] = [x for x in ix["dersler"] if x["ders"] != k] + [{
        "ders": k, "key": g["key"], "kod": g["kod"], "brans": g.get("brans"), "baslik": o["baslik"],
        "madde": sum(len(b["maddeler"]) for b in o["bolumler"]), "cikmis": len(g["cikmis"]), "sure": cikti["sure"],
        "ses": bool(klipler), "soru": cikti["cozucu"]["soru"] if coz else 0}]
    ix["dersler"].sort(key=lambda x: x["ders"])
    ix_p.write_text(json.dumps(ix, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{k}: yayın yazıldı → {od / (k + '.json')} ({len(klipler)} klip, {cikti['sure']} sn)")


def main() -> None:
    ks = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not ks:
        raise SystemExit(__doc__)
    for k in ks:
        yayinla(k, "--sessiz-izin" in sys.argv)


if __name__ == "__main__":
    main()
