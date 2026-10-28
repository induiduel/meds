#!/usr/bin/env python3
"""Canlı içerik katmanı (data/content) araçları — kayıt düzeyinde fark biçimi (bkz. src/services/contentOverlay.ts).

Kullanım:
  icerik_katman.py denetle [--veri data] [--kaynak src/data]   # 0 HATA olmalı (dağıtım [0b] ve el kitabı)
  icerik_katman.py goc     [--veri data] [--kaynak src/data]   # eski TAM KOPYA katmanları farka çevirir (yedekli)
  icerik_katman.py uygula  <fark.json> <hedef src/data dosyası> # dağıtım geri çekme: farkı yerel kaynağa kayıt kayıt uygular

Kök neden (2026-10-28): katman tam kopyaydı ve kaynağı gölgeliyordu; kopyadan sonra src/data'ya eklenen kayıtlar
(k2p desteleri, 383 sözlük terimi) sunucuda görünmüyordu. Fark biçiminde kaynakta olup farkta olmayan kayıt görünür.
"""
import argparse, hashlib, json, os, shutil, sys, time
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
ANAHTARLAR = ["id", "deckId", "key", "slug"]
VARLIK = {"medical_glossary.json": "glossary", "question_cards.json": "cards", "diseases.json": "diseases",
          "interactive_learning_decks.json": "decks", "lectureSummariesCatalog.json": "summaries"}


def js(v):  # JSON.stringify ile aynı sıkı biçim (sha karşılaştırması için)
    return json.dumps(v, ensure_ascii=False, separators=(",", ":"))


def sha(v):
    return hashlib.sha1(js(v).encode("utf-8")).hexdigest()


def anahtar(*diziler):
    for k in ANAHTARLAR:
        ok = True
        for d in diziler:
            gor = set()
            for x in d:
                v = x.get(k) if isinstance(x, dict) else None
                if v in (None, "") or str(v) in gor:
                    ok = False; break
                gor.add(str(v))
            if not ok: break
        if ok: return k
    return None


def harita(veri, f):
    if f["bicim"] == "dizi":
        return {str(x[f["anahtar"]]): x for x in veri}
    return dict(veri or {})


def uygula_fark(kaynak, f):
    if not f: return kaynak
    if f["bicim"] == "tam": return f["tam"]
    sil, k = set(f.get("silinen") or []), f.get("kayitlar") or {}
    if f["bicim"] == "dizi" and isinstance(kaynak, list):
        a, out, gor = f["anahtar"], [], set()
        for x in kaynak:
            i = str(x.get(a)); gor.add(i)
            if i in sil: continue
            out.append(k.get(i, x))
        out += [x for i, x in k.items() if i not in gor]
        return out
    if f["bicim"] == "nesne" and isinstance(kaynak, dict):
        out = {i: k.get(i, x) for i, x in kaynak.items() if i not in sil}
        for i, x in k.items():
            if i not in out and i not in sil: out[i] = x
        return out
    return kaynak


def tam_kopyalar(icerik: Path):
    for p in sorted(icerik.rglob("*.json")):
        r = p.relative_to(icerik)
        if r.parts[0].startswith("_") or p.name.endswith(".fark.json") or ".tmp" in p.name: continue
        yield str(r)


def farklar(icerik: Path):
    for p in sorted(icerik.rglob("*.fark.json")):
        r = p.relative_to(icerik)
        if r.parts[0] == "_birlesik": continue
        yield str(r)[: -len(".fark.json")]


def oku(p):
    with open(p, encoding="utf-8") as fh: return json.load(fh)


def yaz(p, veri, girinti=1):
    p = Path(p); p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + f".{os.getpid()}.tmp")
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(veri, fh, ensure_ascii=False, indent=girinti)
        if girinti: fh.write("\n")
    os.replace(tmp, p)


def girinti_bul(p):
    try:
        bas = open(p, encoding="utf-8").read(200)
        import re
        m = re.search(r"\n( +)\S", bas)
        return len(m.group(1)) if m else None
    except Exception:
        return 2


def cmd_goc(a):
    veri, kaynak = Path(a.veri), Path(a.kaynak)
    icerik = veri / "content"
    ids = {}
    try: ids = oku(icerik / "_ids.json")
    except Exception: pass
    liste = list(tam_kopyalar(icerik))
    if not liste:
        print("göç: tam kopya yok"); return 0
    yedek = veri / "_yedek" / f"content_goc_{time.strftime('%Y%m%d_%H%M%S')}"
    shutil.copytree(icerik, yedek, ignore=shutil.ignore_patterns("_birlesik"))
    print(f"yedek: {yedek}")
    for rel in liste:
        tam, src = oku(icerik / rel), (oku(kaynak / rel) if (kaynak / rel).exists() else None)
        izli = list((ids.get(VARLIK.get(rel, ""), {}) or {}).keys()) or None
        if src is None:
            f = {"surum": 1, "bicim": "tam", "kayitlar": {}, "silinen": [], "taban": {}, "tam": tam}
        elif isinstance(tam, list) and isinstance(src, list) and anahtar(tam, src):
            f = {"surum": 1, "bicim": "dizi", "anahtar": anahtar(tam, src), "kayitlar": {}, "silinen": [], "taban": {}}
        elif isinstance(tam, dict) and isinstance(src, dict) and all(isinstance(v, dict) for v in list(tam.values()) + list(src.values())):
            f = {"surum": 1, "bicim": "nesne", "kayitlar": {}, "silinen": [], "taban": {}}
        else:
            f = {"surum": 1, "bicim": "tam", "kayitlar": {}, "silinen": [], "taban": {}, "tam": tam}
        if f["bicim"] != "tam":
            tM, kM = harita(tam, f), harita(src, f)
            # Eski kopya kaynaktan bayat: silme kaydedilmez (kaynakta sonra eklenenler), _ids izi varsa yalnız onlar
            for i, x in tM.items():
                if izli and i not in izli: continue
                if i in kM and js(kM[i]) == js(x): continue
                f["kayitlar"][i] = x
                f["taban"][i] = sha(kM[i]) if i in kM else None
        n = len(f["kayitlar"])
        if f["bicim"] != "tam" and not n:
            print(f"  {rel}: kaynakla aynı (iz yok) → katman kaldırıldı")
        else:
            yaz(icerik / (rel + ".fark.json"), f)
            print(f"  {rel}: fark yazıldı ({f['bicim']}, {n} kayıt{', izli' if izli else ''})")
        (icerik / rel).unlink()
    shutil.rmtree(icerik / "_birlesik", ignore_errors=True)
    return 0


def cmd_denetle(a):
    icerik, kaynak = Path(a.veri) / "content", Path(a.kaynak)
    hata = uyari = 0
    for rel in tam_kopyalar(icerik):
        print(f"HATA: {rel} TAM KOPYA olarak duruyor (kaynağı gölgeler) → icerik_katman.py goc"); hata += 1
    for rel in farklar(icerik):
        try: f = oku(icerik / (rel + ".fark.json"))
        except Exception as e:
            print(f"HATA: {rel}.fark.json okunamadı: {e}"); hata += 1; continue
        if f.get("bicim") == "tam":
            print(f"UYARI: {rel} bütün dosya olarak tutuluyor (kayıt kimliği yok)"); uyari += 1; continue
        src = oku(kaynak / rel) if (kaynak / rel).exists() else None
        if src is None:
            print(f"HATA: {rel} kaynakta yok"); hata += 1; continue
        kM = harita(src, f)
        degismis = [i for i, t in (f.get("taban") or {}).items() if t and i in kM and sha(kM[i]) != t and i in (f.get("kayitlar") or {})]
        ayni = [i for i, x in (f.get("kayitlar") or {}).items() if i in kM and js(kM[i]) == js(x)]
        sil_yok = [i for i in f.get("silinen") or [] if i not in kM]
        print(f"  {rel}: {len(f.get('kayitlar') or {})} düzenli, {len(f.get('silinen') or [])} silinmiş kayıt")
        if degismis: print(f"UYARI: {rel}: kaynakta da değişmiş kayıtlar (katman kazanır): {degismis[:8]}"); uyari += 1
        if ayni: print(f"UYARI: {rel}: kaynakla artık aynı kayıtlar (dağıtımda temizlenir): {len(ayni)}"); uyari += 1
        if sil_yok: print(f"UYARI: {rel}: silinmiş sayılan ama kaynakta zaten olmayan: {sil_yok[:8]}"); uyari += 1
        birlesik = uygula_fark(src, f)
        eksik = [i for i in kM if i not in harita(birlesik, f) and i not in set(f.get("silinen") or [])]
        if eksik: print(f"HATA: {rel}: kaynak kayıtları birleşimde yok: {eksik[:8]}"); hata += 1
    print(f"{hata} HATA, {uyari} UYARI")
    return 1 if hata else 0


def cmd_uygula(a):
    """Dağıtım geri çekme: farkı yerel src/data dosyasına uygular. Çıkış 0 uygulandı/zaten güncel, 3 çakışma."""
    f, hedef = oku(a.fark), Path(a.hedef)
    if f["bicim"] == "tam":
        yeni = f["tam"]
        mevcut = oku(hedef) if hedef.exists() else None
        if js(mevcut) == js(yeni): print("  zaten güncel"); return 0
        yaz(hedef, yeni, girinti_bul(hedef) if hedef.exists() else 2); print("  bütün dosya yazıldı"); return 0
    src = oku(hedef)
    kM = harita(src, f)
    cakisma = []
    for i, x in (f.get("kayitlar") or {}).items():
        t = (f.get("taban") or {}).get(i)
        if i in kM and js(kM[i]) != js(x) and t and sha(kM[i]) != t: cakisma.append(i)
    for i in f.get("silinen") or []:
        t = (f.get("taban") or {}).get(i)
        if i in kM and t and sha(kM[i]) != t: cakisma.append(i)
    if cakisma:
        print(f"ÇAKIŞMA: hem panelde hem yerelde değişmiş kayıtlar: {cakisma[:10]}"); return 3
    yeni = uygula_fark(src, f)
    if js(yeni) == js(src): print("  zaten güncel"); return 0
    yaz(hedef, yeni, girinti_bul(hedef))
    print(f"  uygulandı: {len(f.get('kayitlar') or {})} kayıt, {len(f.get('silinen') or [])} silme")
    return 0


def main():
    ap = argparse.ArgumentParser()
    alt = ap.add_subparsers(dest="k", required=True)
    for ad in ("denetle", "goc"):
        p = alt.add_parser(ad)
        p.add_argument("--veri", default=str(KOK / "data"))
        p.add_argument("--kaynak", default=str(KOK / "src" / "data"))
    p = alt.add_parser("uygula"); p.add_argument("fark"); p.add_argument("hedef")
    a = ap.parse_args()
    sys.exit({"denetle": cmd_denetle, "goc": cmd_goc, "uygula": cmd_uygula}[a.k](a))


if __name__ == "__main__":
    main()
