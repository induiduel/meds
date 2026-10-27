#!/usr/bin/env python3
"""Yeni anlatım metnini (md) konusma_v2.json'a çevirmenin birleştirme + doğrulama adımı (LLM yok).

Ajanlar bölüm parçalarını kimliksiz yazar: {"baslik": "...", "paragraflar": [{"sayfa": N, "cumleler": [{ses, ekran, duzey,
vurgu, slayt_adim, cikmis, spot, slayt}]}]}. Bu betik kimlikleri verir (b01/p001/c0001), metni doğrulanmış md ile BİREBİR
karşılaştırır (her paragrafın cümleleri birleşince md paragrafı olur), konusma_v2.dogrula + turet çalıştırır.
  .venv-ocr/bin/python scripts/ogrenci_drive/v2_birlestir.py --ders k2-04 --baslik "…" --md metin.md --kaynak kaynak.md \\
      --cikis DIZIN parca1.json [parca2.json …]
  --kontrol: yalnız bu parçaların kendi paragraflarını md'de arar ve doğrular (ajan ön kontrolü; kimlikler geçici)
"""
import argparse, json, re, sys
from pathlib import Path
MEDS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MEDS / "scripts" / "sesli_anlatim"))
import konusma_v2 as KV  # noqa: E402
sys.path.insert(0, str(MEDS / "scripts" / "arsiv_25_26"))
from pdf_isaret import cumle_sonlari  # noqa: E402


def md_paragraflar(yol):
    out, bolum = [], None
    for blok in re.split(r"\n\s*\n", Path(yol).read_text(encoding="utf-8")):
        b = blok.strip()
        if not b or b.startswith("# "):
            continue
        if b.startswith("@@"):
            ilk, _, kalan = b.partition("\n")
            bolum = ilk[2:].strip()
            b = kalan.strip()
            if not b:
                continue
        out.append((bolum, " ".join(b.split())))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ders", required=True); ap.add_argument("--baslik", default="")
    ap.add_argument("--md", required=True); ap.add_argument("--kaynak", required=True)
    ap.add_argument("--cikis"); ap.add_argument("--kontrol", action="store_true")
    ap.add_argument("parcalar", nargs="+")
    a = ap.parse_args()
    md = md_paragraflar(a.md)
    havuz = {t: b for b, t in md}
    bolumler, bi, pi, ci, hata = [], 0, 0, 0, []
    for yol in a.parcalar:
        part = json.loads(Path(yol).read_text(encoding="utf-8"))
        for b in (part if isinstance(part, list) else part.get("bolumler", [part])):
            bi += 1
            nb = {"id": f"{a.ders}-b{bi:02d}", "baslik": b["baslik"], "paragraflar": []}
            for p in b["paragraflar"]:
                pi += 1
                ps = {"id": f"{a.ders}-p{pi:03d}", "sayfa": p["sayfa"], "cumleler": []}
                for c in p["cumleler"]:
                    ci += 1
                    ps["cumleler"].append({**c, "id": f"{a.ders}-c{ci:04d}"})
                metin = " ".join(" ".join(c["ses"].split()) for c in ps["cumleler"])
                if metin not in havuz:
                    hata.append(f"{ps['id']}: paragraf md'de birebir yok: {metin[:70]!r}")
                elif len(cumle_sonlari(metin)) != len(ps["cumleler"]):
                    hata.append(f"{ps['id']}: cümle bölünmesi cumle_sonlari ile uyuşmuyor ({len(ps['cumleler'])} ≠ {len(cumle_sonlari(metin))}): {metin[:60]!r}")
                elif havuz[metin] != b["baslik"]:
                    hata.append(f"{ps['id']}: bölüm {b['baslik']!r} ≠ md bölümü {havuz[metin]!r}")
                nb["paragraflar"].append(ps)
            bolumler.append(nb)
    d = {"surum": 2, "ders_id": a.ders, "baslik": a.baslik, "bolumler": bolumler}
    kd = Path(a.kaynak).parent  # kaynak.md bu dizinde olmalı
    hata += KV.dogrula(d, KV.kaynak_sayfa(kd), KV.kaynak_metin(kd))
    if not a.kontrol:
        sirali = [t for _, t in md]
        yazilan = [" ".join(" ".join(c["ses"].split()) for c in p["cumleler"]) for b in bolumler for p in b["paragraflar"]]
        if sirali != yazilan:
            hata.append(f"paragraf sırası/sayısı md ile uyuşmuyor ({len(yazilan)} ≠ {len(sirali)})")
    for h in hata[:60]:
        print("HATA", h)
    print(f"{a.ders}: {len(bolumler)} bölüm · {pi} paragraf · {ci} cümle · {len(hata)} HATA")
    if hata:
        return 1
    if a.cikis and not a.kontrol:
        o = Path(a.cikis); o.mkdir(parents=True, exist_ok=True)
        (o / "konusma_v2.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        (o / "kaynak.md").write_text(Path(a.kaynak).read_text(encoding="utf-8"), encoding="utf-8")
        metin, sayfalar = KV.turet(d)
        (o / "konusma_metni.md").write_text(metin, encoding="utf-8")
        (o / "konusma_sayfalari.json").write_text(json.dumps(sayfalar), encoding="utf-8")
        print("yazıldı:", o)
    return 0


if __name__ == "__main__":
    sys.exit(main())
