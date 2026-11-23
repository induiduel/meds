#!/usr/bin/env python3
"""Ders Özeti (Kurul 2+) — read-once girdi paketi.

Bir dersin mevcut, doğrulanmış katmanlarını TEK dosyada toplar; yazar alt ajan yalnız bunu okur (ham slaytı/katmanları
tekrar tekrar taramaz). Yeni bilgi üretmez, yalnız derler.

Girdi (hepsi varsa):
  meds_temp/ogrenci_ders/<k>/sayfalar.json            slayt metni (sayfa → metin)  — BİRİNCİL kaynak
  data/sesli_anlatim/cikmis_konum/<key>.json          doğrulanmış çıkmışlar (dogrulandi:true, s = slayt sayfası)
  src/data/ders_analizi/<k>.json                      çıkmış analizi / önemli / odak
  src/data/k<N>*_onem/<kod>.json                      "Sınav için en önemliler" (puanlı)
  src/data/k<N>*_cozucu/<kod>.json                    sesli çözücü soruları (örnek + çıkmış)
  src/data/hoca_vurgu/<k>.json                        hoca sözlü vurgusu (ses dökümünden)
  src/data/ogrenci_onem/<k>.json                      geçmiş yıl öğrenci önem birimleri (A/B/C)
  ../meds_temp/ogrenci_sentez/ders/<k>.json           öğrenci+YZ derlemesi (yalnız slaytta karşılığı varsa)
Çıktı: meds_temp/ders_ozet/<k>/girdi.json
Kullanım: python3 scripts/uretim/ders_ozet/topla.py k2-15 [k2-xx ...]
"""
from __future__ import annotations

import sys
from pathlib import Path as _P

_s = _P(__file__).resolve()
while not (_s / "kok.py").exists() and _s != _s.parent:
    _s = _s.parent
sys.path.insert(0, str(_s))
from kok import MEDS, PROJE  # noqa: E402

import json  # noqa: E402
import re  # noqa: E402
from pathlib import Path  # noqa: E402

CIKTI = PROJE / "meds_temp" / "ders_ozet"


def oku(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def ders_kaydi(k: str) -> dict:
    kurul = k.split("-")[0][1:]
    d = oku(MEDS / "src/data/dersler" / f"k{kurul}.json") or {}
    for x in d.get("dersler", []):
        if x.get("id") == k:
            return x
    raise SystemExit(f"{k}: ders kayıt defterinde yok")


def tam_key(k: str) -> str:
    for p in sorted((MEDS / "data/sesli_anlatim/cikmis_konum").glob(f"{k}-*.json")):
        if not re.search(r"-v\d+\.json$", p.name):
            return p.stem
    for p in sorted((MEDS / "src/data/ders_icerik").glob(f"{k}-*.json")):
        return p.stem
    raise SystemExit(f"{k}: tam anahtar bulunamadı")


def cozucu_bul(kurul: str, kod: str) -> tuple:
    """Dersin sesli çözücüsü; bölünmüşse parçalar (2f03-1, 2f03-2 …) → (brans, [kod…], [soru…])."""
    for d in sorted((MEDS / "src/data").glob(f"k{kurul}*_cozucu")):
        brans = d.name[: -len("_cozucu")]
        if brans.endswith("hoca") or brans.endswith("hocaara") or not kod:
            continue
        parcalar = [d / f"{kod}.json"] if (d / f"{kod}.json").exists() else sorted(
            d.glob(f"{kod}-*.json"), key=lambda p: int(re.sub(r"\D", "", p.stem.rsplit("-", 1)[1]) or 0))
        if parcalar:
            sorular = [q for p in parcalar for q in (oku(p) or {}).get("sorular", [])]
            return brans, [p.stem for p in parcalar], sorular
    return None, [], []


def pdf_sayfalari(key: str) -> dict | None:
    """Yedek: sesli dersin hizalamasındaki kaynak PDF (meds_downloads/drive_root/<path>) → pdftotext sayfa sayfa."""
    import subprocess
    h = oku(MEDS / "data/sesli_anlatim/hizalama" / f"{key}.json") or {}
    for f in h.get("dosyalar", [])[:1]:
        for kok in (PROJE / "meds_downloads/drive_root", MEDS / "meds_downloads/drive_root"):
            pdf = kok / f["path"]
            if pdf.exists():
                t = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True).stdout
                sayfa = t.split("\f")
                if sayfa and not sayfa[-1].strip():
                    sayfa.pop()
                return {str(i): m for i, m in enumerate(sayfa, 1)}  # metinsiz (görsel) sayfa da kalır: önem/çıkmış dayanağı
    return None


def sayfa_metni(k: str, key: str = "") -> dict[str, str]:
    d = (oku(PROJE / "meds_temp/ogrenci_ders" / k / "sayfalar.json") or oku(MEDS / "meds_temp/ogrenci_ders" / k / "sayfalar.json")
         or pdf_sayfalari(key))
    if not d:
        raise SystemExit(f"{k}: sayfalar.json yok (slayt metni BİRİNCİL kaynak)")
    return {str(s): re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n+", "\n", str(m).replace("\f", ""))).strip() for s, m in d.items()}


def topla(k: str) -> dict:
    kayit = ders_kaydi(k)
    kurul = k.split("-")[0][1:]
    key = tam_key(k)
    kod = kayit.get("kod") or ""
    brans, kodlar, coz_sorular = cozucu_bul(kurul, kod)
    onem = next((oku(p) for p in sorted((MEDS / "src/data").glob(f"k{kurul}*_onem/{kod}.json"))), None)
    ck = oku(MEDS / "data/sesli_anlatim/cikmis_konum" / f"{key}.json") or {}
    cikmis = [{"id": q["id"], "kok": q.get("kok"), "cevap": q.get("cevap"), "yil": q.get("yil"), "s": q.get("s"),
               "neden": q.get("neden")} for q in ck.get("q", []) if q.get("dogrulandi")]
    analiz = oku(MEDS / "src/data/ders_analizi" / f"{k}.json") or {}
    hv = oku(MEDS / "src/data/hoca_vurgu" / f"{k}.json") or {}
    oo = oku(MEDS / "src/data/ogrenci_onem" / f"{k}.json") or {}
    sentez = oku(PROJE / "meds_temp/ogrenci_sentez/ders" / f"{k}.json") or {}
    sorular = []
    for q in coz_sorular:
        sorular.append({"no": q["no"], "tur": q.get("tur"), "sinav": q.get("sinav"), "soru": q["soru"],
                        "secenekler": q["secenekler"], "dogru": q["dogru"], "cozum": q.get("cozum"), "sayfa": q.get("sayfa")})
    return {
        "ders": k, "key": key, "kod": kod, "kurul": int(kurul), "baslik": kayit.get("ad") or kayit.get("baslik") or analiz.get("konu"),
        "brans": analiz.get("brans") or kayit.get("brans"), "ogretim_uyesi": analiz.get("ogretim_uyesi"),
        "cozucu": {"brans": brans, "kod": kodlar[0], "kodlar": kodlar} if brans else None,
        "sayfalar": sayfa_metni(k, key),
        "cikmis": cikmis,
        "cikmis_analiz": [x for x in analiz.get("analiz", []) if x.get("id") in ("cikmis", "onemli", "odak", "kazanim")],
        "onem": {"neden_onemli": (onem or {}).get("neden_onemli"),
                 "maddeler": [{"puan": m.get("puan"), "baslik": m.get("baslik"), "bilgi": m.get("bilgi"), "alt": m.get("alt"),
                               "s": sorted({a.get("sayfa") for a in m.get("alinti", []) if a.get("sayfa")})}
                              for m in (onem or {}).get("maddeler", [])]},
        "hoca_vurgu": [{"id": v.get("id"), "kategori": v.get("kategori"), "alinti": v.get("alinti"), "konu": v.get("konu"), "s": v.get("s")}
                       for v in hv.get("vurgular", [])],
        "ogrenci_onem": [{"id": b.get("id"), "sayfa": b.get("sayfa"), "oncelik": b.get("oncelik"), "baslik": b.get("baslik"),
                          "metin": (b.get("metin") or "")[:700]}
                         for b in oo.get("birimler", []) if b.get("oncelik") in ("A", "B")],
        "ogrenci_sentez": [{"sayfa": b.get("sayfa"), "metin": (b.get("metin") or "")[:400]}
                           for s in sentez.get("kaynaklar", []) for b in s.get("birimler", [])][:120],
        "sorular": sorular,
    }


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    for k in sys.argv[1:]:
        try:
            g = topla(k)
        except SystemExit as e:
            print(f"ATLANDI {e}")
            continue
        d = CIKTI / k
        d.mkdir(parents=True, exist_ok=True)
        (d / "girdi.json").write_text(json.dumps(g, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{k}: {len(g['sayfalar'])} sayfa, {len(g['cikmis'])} çıkmış, {len(g['onem']['maddeler'])} önem, "
              f"{len(g['hoca_vurgu'])} hoca, {len(g['ogrenci_onem'])} öğrenci A/B, {len(g['sorular'])} soru, çözücü={g['cozucu']}")


if __name__ == "__main__":
    main()
