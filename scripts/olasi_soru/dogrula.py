#!/usr/bin/env python3
"""olasi_sorular.json kapısı: şema, kimlik kararlılığı, kanıt bağı, şık/cevap tutarlılığı. 0 HATA → yayın."""
import argparse, json, re, sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(KOK / "meds/scripts"))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--kurul", type=int, required=True); a = ap.parse_args()
    d = KOK / f"meds_temp/olasi_soru/k{a.kurul}"
    yv = json.loads((d / "yuvalar.json").read_text())
    os_ = json.loads((d / "olasi_sorular.json").read_text())
    hata, uyari = [], []
    kanitlar = {k for y in yv["yuvalar"].values() for k in y["kanit_idleri"]}
    if os_.get("parmak_izi") != yv.get("parmak_izi"):
        uyari.append("parmak_izi yuvalar.json ile aynı değil (eski sentez)")
    gorulen = set()
    for s in os_.get("sorular", []):
        i = s.get("id", "?")
        if not re.fullmatch(rf"k{a.kurul}-os-(\d{{3}}|s-[\w-]{{6}})", i): hata.append(f"{i}: kimlik biçimi")
        if i in gorulen: hata.append(f"{i}: çift kimlik")
        gorulen.add(i)
        if str(s.get("yuva")) not in yv["yuvalar"]: hata.append(f"{i}: bilinmeyen yuva {s.get('yuva')}")
        if len((s.get("kok") or "").split()) < 4: hata.append(f"{i}: kök çok kısa")
        harfler = [x.get("harf") for x in s.get("siklar", [])]
        if harfler != list("ABCDE")[:len(harfler)] or len(harfler) < 4: hata.append(f"{i}: şıklar A–E sırasında değil")
        if s.get("cevap") not in harfler: hata.append(f"{i}: cevap şıklarda yok")
        if not 0 <= int(s.get("guven", -1)) <= 100: hata.append(f"{i}: guven 0–100 değil")
        if not set(s.get("kanit_idleri", [])) <= kanitlar or not s.get("kanit_idleri"): hata.append(f"{i}: kanıt bağı yok/geçersiz")
        if not (s.get("ders_ref") or {}).get("ders_id"): uyari.append(f"{i}: ders_ref yok")
    try:
        from sik_aciklama import denetle as sik_denetle  # varsa Kurul 2 kapısı
        for s in os_.get("sorular", []):
            for x in s.get("siklar", []):
                hata.extend(sik_denetle(x.get("aciklama", ""), f"{s['id']}/{x.get('harf')}"))
    except ImportError:
        uyari.append("sik_aciklama.denetle bulunamadı; şık üslup kapısı atlandı")
    try:
        from turkce_uslup import denetle_yapi
        hata.extend(denetle_yapi(os_.get("sorular", []), "olasi_sorular"))
    except ImportError:
        uyari.append("turkce_uslup bulunamadı")
    for u in uyari[:20]: print("UYARI", u)
    for h in hata[:60]: print("HATA", h)
    print(f"{len(os_.get('sorular', []))} soru · {len(hata)} HATA · {len(uyari)} uyarı")
    sys.exit(1 if hata else 0)


if __name__ == "__main__":
    main()
