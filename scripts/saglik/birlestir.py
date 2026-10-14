#!/usr/bin/env python3
"""
Sağlık Bakanlığı sekmesi — resmî veri araştırma çıktısını uygulamaya taşır ve denetler (yerel, modelsiz).

Girdi (varsayılan: --kaynak klasörü): asi.json, anne_yenidogan.json, karabuk.json, turkiye.json — her biri
`kaynaklar` listesi + bölüm verisi (şema: docs/SAGLIK_BAKANLIGI_PLANI.md, bileşen türleri: src/components/saglik/saglikVeri.ts).

Yapılanlar:
  1. Kaynak URL'si devlet alan adında mı (.gov.tr, .edu.tr, .bel.tr, .tsk.tr) — değilse kaynak ve ona dayanan ögeler atılır.
  2. Aynı kimlik farklı dosyalarda farklı URL'yle geçiyorsa dosya önekiyle yeniden adlandırılır, başvurular güncellenir.
  3. `kaynak` alanı kaynak listesinde olmayan liste ögeleri atılır (kaynaksız sayı gösterilmez).
  4. src/data/saglik/kaynaklar.json (birleşik) + bölüm dosyaları yazılır; rapor stdout'a.

Kullanım: python3 scripts/saglik/birlestir.py --kaynak <araştırma klasörü> [--deneme]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

MEDS = Path(__file__).resolve().parents[2]
OUT = MEDS / "src" / "data" / "saglik"
DOSYALAR = {"asi": "asi.json", "anne_yenidogan": "anne_yenidogan.json", "karabuk": "karabuk.json", "turkiye": "turkiye.json",
            "kavramlar": "kavramlar.json", "mevzuat_teskilat": "mevzuat_teskilat.json", "havuz": "havuz.json"}
# 2. tur araştırması (--kaynak2): kavramlar/mevzuat düz dosya, bilgi havuzu havuz/*.json (birleştirilir), Karabük geçmişi ayrı
DEVLET = re.compile(r"(\.gov\.tr|\.edu\.tr|\.bel\.tr|\.tsk\.tr|\.pol\.tr|\.k12\.tr)$", re.I)


def ders_mi(k: dict) -> bool:
    return k.get("tur") == "ders"


def devlet_mi(url: str) -> bool:
    try:
        h = urlparse(url).hostname or ""
    except ValueError:
        return False
    return bool(DEVLET.search(h))


def yeniden_adlandir(x, harita: dict[str, str]):
    if isinstance(x, dict):
        return {k: (harita.get(v, v) if k == "kaynak" and isinstance(v, str) else yeniden_adlandir(v, harita)) for k, v in x.items()}
    if isinstance(x, list):
        return [yeniden_adlandir(v, harita) for v in x]
    return x


def kaynak_ayir(x, gecerli: set[str]):
    """'a; b, c' gibi birleşik kaynak alanını ilk geçerli kimlik + ek_kaynaklar'a ayırır; kimlik olmayan sözcükler düşer."""
    if isinstance(x, list):
        return [kaynak_ayir(v, gecerli) for v in x]
    if not isinstance(x, dict):
        return x
    d = {k: kaynak_ayir(v, gecerli) for k, v in x.items()}
    k = d.get("kaynak")
    if isinstance(k, str) and k not in gecerli and re.search(r"[;,]", k):
        parcalar = [t.strip() for t in re.split(r"[;,]", k) if t.strip() in gecerli]
        if parcalar:
            d["kaynak"] = parcalar[0]
            ek = [e for e in (d.get("ek_kaynaklar") or []) if e in gecerli]
            d["ek_kaynaklar"] = list(dict.fromkeys(parcalar[1:] + ek))
            if not d["ek_kaynaklar"]:
                del d["ek_kaynaklar"]
    return d


def temizle(x, gecerli: set[str], atilan: list[str], yol: str = ""):
    """Listelerde kaynağı geçersiz olan sözlük ögelerini atar; tekil sözlükte geçersiz kaynağı siler."""
    if isinstance(x, list):
        out = []
        for i, v in enumerate(x):
            if isinstance(v, dict) and isinstance(v.get("kaynak"), str) and v["kaynak"] not in gecerli:
                # Bilgi havuzu: soru kimliğiyle bağlı bilgi (kaynağı sorunun kendisi) ya da yukarıdaki maddelerden
                # derlenen tablo korunur; yalnız geçersiz kaynak alanı silinir
                if v.get("sorular") or v.get("sutunlar"):
                    v = {k: x for k, x in v.items() if k != "kaynak"}
                    out.append(temizle(v, gecerli, atilan, f"{yol}[{i}]"))
                    continue
                atilan.append(f"{yol}[{i}] kaynak={v['kaynak']}")
                continue
            out.append(temizle(v, gecerli, atilan, f"{yol}[{i}]"))
        return out
    if isinstance(x, dict):
        d = {}
        for k, v in x.items():
            if k == "kaynak" and isinstance(v, str) and v not in gecerli:
                atilan.append(f"{yol}.kaynak={v} (alan silindi)")
                continue
            d[k] = temizle(v, gecerli, atilan, f"{yol}.{k}")
        return d
    return x


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kaynak", required=True, type=Path)
    ap.add_argument("--kaynak2", type=Path, help="2. tur klasörü (kavramlar.json, mevzuat_teskilat.json, havuz/*.json, karabuk_tarihsel.json)")
    ap.add_argument("--deneme", action="store_true", help="yazmadan rapor ver")
    a = ap.parse_args()

    tum_kaynak: dict[str, dict] = {}
    veriler: dict[str, dict] = {}
    def oku(ad: str, dosya: str):
        if ad == "havuz":
            if not a.kaynak2 or not (a.kaynak2 / "havuz").exists():
                return None
            # Yalnız ajanların son çıktıları (ara dosyalar _ ile başlar ya da sözlük değildir)
            parcalar = sorted(x for x in (a.kaynak2 / "havuz").glob("*.json") if not x.name.startswith("_"))
            if not parcalar:
                return None
            d = {"kaynaklar": [], "konular": [], "anahtar_suphesi": [], "dogrulanamayan": []}
            for pp in parcalar:
                x = json.loads(pp.read_text(encoding="utf-8"))
                if not isinstance(x, dict) or "konular" not in x:
                    continue
                for alan in d:
                    d[alan].extend(x.get(alan, []))
            return d
        for kok in [a.kaynak2, a.kaynak]:
            if kok and (kok / dosya).exists():
                return json.loads((kok / dosya).read_text(encoding="utf-8"))
        return None

    for ad, dosya in DOSYALAR.items():
        d = oku(ad, dosya)
        if d is None:
            print(f"[yok] {dosya} — boş yazılacak")
            veriler[ad] = {}
            continue
        harita: dict[str, str] = {}
        for k in d.get("kaynaklar", []):
            kid = k.get("id")
            if not kid:
                continue
            if ders_mi(k):
                # Ders kaynağı: uygulama içi bağlantı (Öğren destesi); yerel dosya yolları yayımlanmaz
                k = {x: v for x, v in k.items() if x not in ("dosya", "ozet")}
                k["url"] = f"/ogren/{k['deste']}" if k.get("deste") else ""
            elif not k.get("url"):
                continue
            # Aynı belge (aynı URL) başka dosyada başka kimlikle varsa o kimliğe bağlanır
            ayni = None if ders_mi(k) else next((x for x in tum_kaynak.values() if x.get("url") == k.get("url") and x["id"] != kid), None)
            if ayni:
                harita[kid] = ayni["id"]
                continue
            if kid in tum_kaynak and tum_kaynak[kid].get("url") != k.get("url"):
                yeni = f"{ad}-{kid}"
                harita[kid] = yeni
                k = {**k, "id": yeni}
            tum_kaynak[k["id"]] = k
        d = yeniden_adlandir(d, harita)
        d.pop("kaynaklar", None)
        veriler[ad] = d

    gecersiz = {kid for kid, k in tum_kaynak.items() if not ders_mi(k) and not devlet_mi(k["url"])}
    for kid in sorted(gecersiz):
        print(f"[devlet dışı kaynak atıldı] {kid}: {tum_kaynak[kid]['url']}")
        del tum_kaynak[kid]
    gecerli = set(tum_kaynak)

    # Karabük geçmiş yıl serileri (karabuk_tarihsel.json) → karabuk.json ögelerine `seri` / `turkiye_seri`
    if a.kaynak2 and (a.kaynak2 / "karabuk_tarihsel.json").exists() and veriler.get("karabuk"):
        t = json.loads((a.kaynak2 / "karabuk_tarihsel.json").read_text(encoding="utf-8"))
        for k in t.get("kaynaklar", []):
            if k.get("id") and k.get("url") and devlet_mi(k["url"]) and k["id"] not in tum_kaynak:
                tum_kaynak[k["id"]] = k
        gecerli = set(tum_kaynak)
        kb = veriler["karabuk"]
        temiz_seri = lambda xs: sorted([{kk: vv for kk, vv in x.items() if kk in ("yil", "deger", "kaynak", "konum", "not")} for x in (xs or []) if isinstance(x.get("deger"), (int, float)) and (not x.get("kaynak") or x["kaynak"] in gecerli)], key=lambda x: str(x["yil"]))
        n = t.get("nufus", {})
        if kb.get("nufus"):
            if n.get("toplam"): kb["nufus"]["seri"] = temiz_seri(n["toplam"])
            for il in kb["nufus"].get("ilceler", []):
                if il["ad"] in n.get("ilceler", {}): il["seri"] = temiz_seri(n["ilceler"][il["ad"]])
            if n.get("yas_65_ustu_orani") and kb["nufus"].get("yas_65_ustu_orani"): kb["nufus"]["yas_65_ustu_orani"]["seri"] = temiz_seri(n["yas_65_ustu_orani"])
        for g in kb.get("gostergeler", []):
            ts = t.get("gostergeler", {}).get(g.get("kod"))
            if ts:
                if ts.get("il"): g["seri"] = temiz_seri(ts["il"])
                if ts.get("turkiye"): g["turkiye_seri"] = temiz_seri(ts["turkiye"])
        for k in kb.get("kurum_sayilari", []):
            if k["tur"] in t.get("kurumlar", {}): k["seri"] = temiz_seri(t["kurumlar"][k["tur"]])
        for c in kb.get("cevre", []):
            for anahtar, seri in t.get("cevre", {}).items():
                bas, _, ist = anahtar.partition("|")
                if bas.strip() == c.get("baslik") and ist.strip() and ist.strip().lower() in (c.get("istasyon") or "").lower():
                    c["seri"] = temiz_seri(seri)
        for c in kb.get("is_sagligi", []):
            if c["ad"] in t.get("is_sagligi", {}): c["seri"] = temiz_seri(t["is_sagligi"][c["ad"]])
        kb.setdefault("dogrulanamayan", []).extend(t.get("dogrulanamayan", []))
        print("[karabük geçmişi] eklendi")

    kullanilan: set[str] = set()

    def topla(x):
        if isinstance(x, dict):
            if isinstance(x.get("kaynak"), str):
                kullanilan.add(x["kaynak"])
            for v in x.values():
                topla(v)
        elif isinstance(x, list):
            for v in x:
                topla(v)

    for ad, d in veriler.items():
        atilan: list[str] = []
        dogrulanamayan = d.pop("dogrulanamayan", [])
        d = kaynak_ayir(d, gecerli)
        d = temizle(d, gecerli, atilan, ad)
        if dogrulanamayan:
            d["dogrulanamayan"] = dogrulanamayan
        veriler[ad] = d
        topla(d)
        for x in atilan:
            print(f"[kaynaksız öge atıldı] {x}")

    kullanilmayan = sorted(gecerli - kullanilan)
    if kullanilmayan:
        print(f"[bilgi] başvurulmayan {len(kullanilmayan)} kaynak: {', '.join(kullanilmayan[:12])}{'…' if len(kullanilmayan) > 12 else ''}")

    print(f"kaynak: {len(tum_kaynak)} · " + " · ".join(f"{k}: {len(json.dumps(v))//1024} KB" for k, v in veriler.items()))
    if a.deneme:
        return 0
    OUT.mkdir(parents=True, exist_ok=True)
    kaynaklar = sorted(tum_kaynak.values(), key=lambda k: k["id"])
    (OUT / "kaynaklar.json").write_text(json.dumps({"guncelleme": date.today().isoformat(), "kaynaklar": kaynaklar}, ensure_ascii=False, indent=1), encoding="utf-8")
    for ad, dosya in DOSYALAR.items():
        (OUT / dosya).write_text(json.dumps(veriler[ad], ensure_ascii=False, indent=1), encoding="utf-8")
    print("yazıldı:", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
