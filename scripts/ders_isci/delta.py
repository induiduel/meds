"""Delta motoru (R5, ICERIK_MOTORU_V3.md §… "yalnız etkilenen sayfa ve parçalar yeniden üretilir"; 2026-10-24).

Aynı dersin önceki taslağı varsa (hoca PDF'i güncelledi ya da yönetici sonradan not/ses ekledi) her şey baştan
üretilmez. Yeni PDF'in sayfaları önceki taslağın sayfa izleriyle (`sayfa_izleri.json`, scripts/kroki/iz.py: SimHash +
pHash) eşlenir:
  · PDF aynı (bütün sayfalar "ayni")       → önceki taslak kopyalanır; yalnız sesli metin + vurgu yeniden (yeni ekler)
  · az değişiklik (≤%20 sayfa "degismis",   → önceki taslak kopyalanır; değişen sayfaları kapsayan ANA başlıkların deste
    sayfa sayısı ve sırası aynı)             parçaları, ders notu ve sesli metin silinir → paralel.py yalnız eksikleri yazar
  · yapı değişti (sayfa eklendi/çıktı/kaydı → tam üretim (önceki taslağa dokunulmaz)
    ya da >%20 değişti) ya da iz yok
Kaynak metin (kaynak.md) ve sayfa varlıkları her zaman YENİ PDF'ten; iskelet (ders_paketi + sayfa_haritasi), sorular,
sözlük kısmi kipte korunur. Karar delta.json'a yazılır (rapor + panel).
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

from ayarlar import APP, TASLAK, log, oku, yaz

sys.path.insert(0, str(APP / "scripts" / "kroki"))

KORUNAN = ["ders_paketi.json", "sayfa_haritasi.json", "deck_ust.json", "ornek_sorular.json", "cikmis_baglantilari.json",
           "sozluk.json", "hastaliklar.json", "bilgi_havuzu.jsonl"]
SESLI = ["konusma_v2.json", "konusma_metni.md", "konusma_sayfalari.json", "konusma_capalari.json", "oturum_sesli.json"]


def sayfa_izleri(pdf: Path) -> list[dict]:
    import pymupdf
    import iz
    out = []
    with pymupdf.open(pdf) as doc:
        for i, s in enumerate(doc, 1):
            out.append({"sayfa": i, "iz": {"metin": iz.simhash(s.get_text()), "gorsel": iz.phash(iz.sayfa_gri32(s))}})
    return out


def onceki_taslak(d: Path, ders_id: str) -> Path | None:
    """Aynı dersin en son üretilmiş (deste parçaları ya da deck.json olan) başka taslağı."""
    aday = []
    for b in TASLAK.glob("*/baglam.json"):
        t = b.parent
        if t == d or (oku(b, {}) or {}).get("ders_id") != ders_id:
            continue
        if (t / "sayfa_izleri.json").exists() and ((t / "deck_parca").is_dir() or (t / "deck.json").exists()):
            aday.append((t.stat().st_mtime, t))
    return max(aday)[1] if aday else None


def hazirla(j: dict, d: Path, b: dict) -> dict:
    """Yeni taslak d için delta kararı + dosya hazırlığı. Her durumda d/sayfa_izleri.json yazılır."""
    if (d / "delta.json").exists():
        return oku(d / "delta.json", {})
    izler = sayfa_izleri(Path(j["tam"]))
    yaz(d / "sayfa_izleri.json", izler)
    bastan = bool(j.get("duzeltme_notu") or j.get("bastan"))   # yönetici düzeltmesi / "Baştan üret": tam üretim
    on = None if bastan else onceki_taslak(d, b.get("ders_id") or "")
    karar = {"kip": "tam", "onceki": None, **({"neden": "yönetici baştan üretim istedi"} if bastan else {})}
    if on:
        import iz
        eski = oku(on / "sayfa_izleri.json", [])
        es = iz.eslestir(eski, izler)
        # aynı konumda büyük değişiklik: eşleşmeyen yeni sayfa, eski PDF'te eşleşmesiz kalan aynı numaralı sayfanın yerinde
        bos_eski = {e["sayfa"] for e in eski} - {x["eski"] for x in es.values() if x["eski"]}
        for n, x in es.items():
            if x["tur"] == "yeni" and n in bos_eski:
                x.update(eski=n, tur="degismis")
        turler = [x["tur"] for x in es.values()]
        ayni_sira = all(x["eski"] == n for n, x in es.items())
        degisen = [n for n, x in es.items() if x["tur"] != "ayni"]
        karar.update(onceki=on.name, sayfa=len(izler), degisen=degisen)
        if not ayni_sira or "yeni" in turler or len(es) != len(oku(on / "sayfa_izleri.json", [])):
            karar["neden"] = "yapı değişti (sayfa eklendi/çıktı/kaydı)"
        elif len(degisen) > 0.2 * len(izler):
            karar["neden"] = f"{len(degisen)} sayfa değişti (>%20)"
        else:
            karar["kip"] = "ekler" if not degisen else "kismi"
            for f in KORUNAN:
                if (on / f).exists() and not (d / f).exists():
                    shutil.copy2(on / f, d / f)
            silinen = []
            if (on / "deck_parca").is_dir():
                h = oku(d / "sayfa_haritasi.json", {}) or {}
                etkilenen = set()
                for bs in h.get("basliklar", []):
                    if bs.get("ust"):
                        continue
                    a, z = (bs.get("sayfalar") or [0, 0])[:2]
                    if any(a <= n <= z for n in degisen):
                        etkilenen.add(str(bs["no"]))
                (d / "deck_parca").mkdir(exist_ok=True)
                for f in (on / "deck_parca").glob("*.json"):
                    if f.stem in etkilenen:
                        silinen.append(f"deste {f.stem}")
                    else:
                        shutil.copy2(f, d / "deck_parca" / f.name)
            if degisen and (on / "ders_notu.md").exists():
                silinen.append("ders notu")                      # bölümleri değişen sayfalara bağlı → yeniden
            elif (on / "ders_notu.md").exists():
                shutil.copy2(on / "ders_notu.md", d / "ders_notu.md")
            silinen.append("sesli metin")                        # yeni not/ses ya da değişen sayfa → yeniden (paralel)
            karar["yeniden"] = silinen
    yaz(d / "delta.json", karar)
    log(f"delta: {karar['kip']}" + (f" · önceki {karar['onceki']}" if karar.get("onceki") else "")
        + (f" · değişen sayfa {karar.get('degisen')}" if karar.get("degisen") else "")
        + (f" · yeniden {karar.get('yeniden')}" if karar.get("yeniden") else "") + (f" · {karar.get('neden')}" if karar.get("neden") else ""))
    return karar
