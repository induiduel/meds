#!/usr/bin/env python3
"""Ders içerik eki — değerlendirme paketinden ve PDF tablolarından (LLM yok, kullanıcı kararı 2026-11-17).

Destesiz derste ders_icerik_uret.py tablo/liste/spot/kart ve bilgi havuzunu taslak/ders_icerik_ek.json + bilgi_havuzu.jsonl'den
alır; bu dosyaları yazan betik yoktu (önceki derslerde elle yazıldı). Bu betik yalnız KAPIDAN GEÇMİŞ, sayfa kaynaklı veriden
derler, yeni bilgi yazmaz:
  · bilgi paketleri (degerlendirme/paket.json: baslik, s, onem, maddeler)  → spotlar (onem ≥ 2), listeler (≥ 3 madde), kartlar
  · atomik bilgi envanteri (kategori, baslik, ifade, s)                       → bilgi havuzu (bilgiler + kavram kartları)
  · orijinal PDF'teki METİN tabloları (pymupdf find_tables)                   → tablolar (görüntü tablo okunmaz; tahmin yok)
  · taslak/tablolar_gorsel.json (varsa): görüntü tablonun slayttan birebir aktarımı, sayfa (s) zorunlu
Mevcut ek dosyası varsa ÜZERİNE YAZILMAZ (--zorla ile yazılır).

  .venv-ocr/bin/python scripts/uretim/ders_icerik/paketten_ek.py k2-50 [k2-49 …] [--zorla]
  sonra: python3 scripts/ders_icerik_uret.py <tam key> && python3 scripts/ders_icerik_adim.py <tam key> && python3 scripts/ders_icerik_dogrula.py <tam key>
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

MEDS = _kok.MEDS
PROJE = MEDS.parent
BILGI = PROJE / "meds_database_v2" / "ders_bilgi"
KAT_TUR = {"disease": "klinik", "drug": "ilac", "clinical_note": "spot", "mechanism": "mekanizma", "diagnosis": "tani",
           "treatment": "tedavi", "epidemiology": "epidemiyoloji"}


def pdf_yolu(kaynak: dict, kisa: str) -> Path | None:
    adaylar = [kaynak.get("orijinal_pdf") or "", str(PROJE / "meds_temp/ogrenci_ders" / kisa / "orijinal.pdf"),
               str(MEDS / "meds_temp/ogrenci_ders" / kisa / "orijinal.pdf")]
    return next((Path(a) for a in adaylar if a and Path(a).exists()), None)


def temiz(c) -> str:
    return re.sub(r"\s+", " ", str(c or "")).strip()


def pdf_tablolari(pdf: Path) -> list[dict]:
    """Yalnız metin katmanlı, ≥2 satır × ≥2 sütun ve boş olmayan hücreleri ≥ %60 tablolar. Başlık: tablonun sol üst
    hücresi boşsa sayfadaki ilk satır (slayt başlığı)."""
    import pymupdf  # noqa: PLC0415 — yalnız .venv-ocr'da var
    out = []
    with pymupdf.open(pdf) as d:
        # şablon satırları (ders adı, hoca, dönem): sayfaların ≥ %30'unda geçen satır başlık sayılmaz
        say: dict[str, int] = {}
        for p in d:
            for ln in {temiz(x) for x in p.get_text().splitlines()}:
                say[ln] = say.get(ln, 0) + 1
        sablon = {ln for ln, n in say.items() if n >= max(2, 0.3 * len(d))}
        for i, p in enumerate(d):
            for t in p.find_tables().tables:
                r = [[temiz(c) for c in row] for row in t.extract()]
                r = [row for row in r if any(row)]
                if len(r) < 2 or len(r[0]) < 2:
                    continue
                dolu = sum(1 for row in r for c in row if c) / (len(r) * len(r[0]))
                if dolu < 0.6:
                    continue
                h, govde = r[0], r[1:]
                if not h[0]:
                    h[0] = "Özellik"
                hucre = {c for row in r for c in row}
                baslik = next((temiz(x) for x in p.get_text().splitlines()
                               if len(temiz(x)) > 3 and temiz(x) not in sablon and temiz(x) not in hucre), f"Tablo s.{i + 1}")
                out.append({"t": baslik[:90], "h": h, "r": govde, "n": i + 1, "s": i + 1, "kaynak": "pdf_tablo"})
    return out


def ek_uret(kisa: str) -> tuple[dict, list[dict]]:
    pk = json.loads((BILGI / kisa / "degerlendirme" / "paket.json").read_text(encoding="utf-8"))
    bp = pk.get("bilgi_paketleri", [])
    atom = (pk.get("atomik_bilgi_envanteri") or {}).get("atomlar", [])
    spot, lis, kart = [], [], []
    # spot eşiği: önem ≥ 2; derste hiç yoksa dersin en yüksek önem düzeyi
    esik = 2 if any((b.get("onem") or 0) >= 2 for b in bp) else max([b.get("onem") or 0 for b in bp] or [0])
    for b in bp:
        s = (b.get("s") or [None])[0]
        m = [temiz(x) for x in b.get("maddeler", []) if temiz(x)]
        if not s or not m:
            continue
        if (b.get("onem") or 0) >= esik and esik > 0:
            spot += [{"m": x, "n": s, "s": s, "bolum": b["baslik"]} for x in m]
        if len(m) >= 3:
            lis.append({"t": b["baslik"], "sira": "madde", "m": [{"m": x} for x in m], "n": s, "s": s})
        # bilgi kartı ÜRETİLMEZ (kullanıcı kararı 2026-11-18)
    # varlık = atomun sayfasını kapsayan bilgi paketinin başlığı (aynı konudaki atomlar tek kavram kartında toplanır)
    def varlik(a: dict) -> str:
        return next((b["baslik"] for b in bp if a.get("s") in (b.get("s") or [])), a.get("baslik", ""))
    havuz = [{"varlik": varlik(a), "bilgi": temiz(a.get("ifade")), "tur": KAT_TUR.get(a.get("kategori"), "spot"),
              "kanit": {"sayfa": a.get("s"), "alinti": a.get("kanit", "")}} for a in atom if a.get("s") and temiz(a.get("ifade"))]
    pdf = pdf_yolu(pk.get("kaynaklar") or {}, kisa)
    tab = pdf_tablolari(pdf) if pdf else []
    # görüntü tablolar betikle okunmaz: oturumda slayttan birebir aktarılanlar (kaynak sayfasıyla) taslak/tablolar_gorsel.json'da
    gp = PROJE / "meds_temp" / "ogrenci_ders" / kisa / "taslak" / "tablolar_gorsel.json"
    gerekce = ""
    if gp.exists():
        g = json.loads(gp.read_text(encoding="utf-8"))
        liste = g if isinstance(g, list) else g.get("tablolar", [])
        tab += [x for x in liste if x.get("s") and x.get("h") and x.get("r")]
        gerekce = "" if isinstance(g, list) else (g.get("tablo_yok_gerekce") or "").strip()
    return {"baslik": pk.get("konu", ""), "ozet": "", "spotlar": spot, "tablolar": tab, "listeler": lis, "kartlar": kart,
            "_kaynak": "scripts/uretim/ders_icerik/paketten_ek.py (değerlendirme paketi + PDF metin tabloları; LLM yok)",
            "_tablo_notu": "" if tab else "PDF'te metin katmanlı tablo bulunamadı (tablo yoksa ya da görüntüyse)",
            **({"tablolarYok": gerekce} if gerekce and not tab else {})}, havuz


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dersler", nargs="+")
    ap.add_argument("--zorla", action="store_true")
    a = ap.parse_args()
    for k in a.dersler:
        m = re.match(r"k\d-\d{2}", k)
        if not m:
            print(f"HATA: ders kimliği değil: {k}")
            continue
        kisa = m.group(0)
        T = PROJE / "meds_temp" / "ogrenci_ders" / kisa / "taslak"
        T.mkdir(parents=True, exist_ok=True)
        ekp, hp = T / "ders_icerik_ek.json", T / "bilgi_havuzu.jsonl"
        if ekp.exists() and not a.zorla:
            print(f"{kisa}: ek zaten var, dokunulmadı (--zorla)")
            continue
        ek, havuz = ek_uret(kisa)
        # kısaltmaların sayfası (ders_icerik_adim.py destesiz yol) taslak/sayfalar.json'dan bulunur: yoksa PDF metninden yazılır
        sp = T / "sayfalar.json"
        pk = json.loads((BILGI / kisa / "degerlendirme" / "paket.json").read_text(encoding="utf-8"))
        pdf = pdf_yolu(pk.get("kaynaklar") or {}, kisa)
        if pdf and not sp.exists():
            import pymupdf  # noqa: PLC0415
            with pymupdf.open(pdf) as d:
                sp.write_text(json.dumps({str(i + 1): pg.get_text() for i, pg in enumerate(d)}, ensure_ascii=False), encoding="utf-8")
        ekp.write_text(json.dumps(ek, ensure_ascii=False, indent=1), encoding="utf-8")
        if havuz and (not hp.exists() or a.zorla):
            hp.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in havuz), encoding="utf-8")
        print(f"{kisa}: spot {len(ek['spotlar'])} · tablo {len(ek['tablolar'])} · liste {len(ek['listeler'])} · kart {len(ek['kartlar'])} · havuz {len(havuz)}"
              + (f"  ({ek['_tablo_notu']})" if ek["_tablo_notu"] else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
