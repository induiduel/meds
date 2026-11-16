#!/usr/bin/env python3
"""Öğren deste monoliti ↔ deste-başına-dosya dönüştürücü (VERI_MODELI Faz 3 iskelesi).

Biçim tanımı ve serileştirme kuralı TEK yerde: `scripts/deste_deposu.py` (dosya_adi/seri/birlestir_bayt/parcali_yaz).
Bu betik monoliti DEĞİŞTİRMEZ; varsayılan hedef `../meds_temp/deste_parcali/desteler/` (src/data içine yazılmaz).

    python3 scripts/deste_bol.py bol [--hedef DIZIN] [--kaynak MONOLIT]
    python3 scripts/deste_bol.py birlestir --cikti DOSYA [--hedef DIZIN]
    python3 scripts/deste_bol.py dogrula [--hedef DIZIN] [--kaynak MONOLIT]   # 0 fark → çıkış 0
    python3 scripts/deste_bol.py fark <kimlik> [--hedef DIZIN] [--kaynak MONOLIT]
    python3 scripts/deste_bol.py durum        # bayrak açıksa parça dizinini basar, kapalıysa HİÇBİR ŞEY (kabuk betikleri için)

`bol --kalici`: hedef yalnız `src/data/desteler/` olabilir (varsayılanı çevirme adımı; Oracle'a rsync ile taşınır).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path as _P

_s = _P(__file__).resolve()
while not (_s / "kok.py").exists() and _s != _s.parent:
    _s = _s.parent
sys.path.insert(0, str(_s))
from kok import PROJE  # noqa: E402

import deste_deposu as dd  # noqa: E402

VARSAYILAN_HEDEF = PROJE / "meds_temp" / "deste_parcali" / "desteler"


KALICI_HEDEF = dd.YOL.parent / "desteler"


def bol(kaynak: _P, hedef: _P, kalici: bool = False) -> None:
    hedef = hedef.resolve()
    if kalici:
        if hedef != KALICI_HEDEF.resolve():
            sys.exit(f"HATA: --kalici yalnız {KALICI_HEDEF} hedefiyle")
    elif dd.YOL.parent.resolve() in (hedef, *hedef.parents):
        sys.exit("HATA: hedef src/data altında olamaz (--kalici olmadan; çalışma verisi meds_temp'e)")
    desteler = dd.hepsi(kaynak)
    n = dd.parcali_yaz(desteler, hedef)
    print(f"bol: {len(desteler)} deste → {hedef} ({n} dosya yazıldı)")


def birlestir(hedef: _P, cikti: _P) -> None:
    if cikti.resolve() == dd.YOL.resolve():
        sys.exit("HATA: monolitin üstüne yazılmaz (bu görevde monolit değişmez)")
    cikti.parent.mkdir(parents=True, exist_ok=True)
    dd._atomik_bayt(cikti, dd.birlestir_bayt(dd.parca_baytlari(hedef)))
    print(f"birlestir: {cikti}")


def dogrula(kaynak: _P, hedef: _P) -> int:
    mono = kaynak.read_bytes()
    sira = dd.sira_oku(hedef)["desteler"]
    hatalar = []
    parcalar = []
    for g in sira:
        b = (hedef / g["dosya"]).read_bytes()
        if hashlib.sha1(b).hexdigest() != g["sha1"]:
            hatalar.append(f"sha1 uyuşmaz: {g['id']}")
        if dd.kimlik_of(g["dosya"]) != g["id"]:
            hatalar.append(f"dosya adı geri çevrilemiyor: {g['dosya']}")
        parcalar.append(b)
    birlesik = dd.birlestir_bayt(parcalar)
    liste = json.loads(mono)
    m_ids = [d.get("id") for d in liste]
    p_ids = [g["id"] for g in sira]
    yetim = sorted(p.name for p in hedef.glob("*.json") if p.name != dd.SIRA and p.name not in {g["dosya"] for g in sira})
    ha, hb = hashlib.sha256(mono).hexdigest(), hashlib.sha256(birlesik).hexdigest()
    print(f"monolit  : {len(m_ids)} deste, {len(mono):,} bayt, sha256 {ha}")
    print(f"parçalar : {len(p_ids)} deste, {len(birlesik):,} bayt, sha256 {hb}")
    if ha != hb:
        hatalar.append("BAYT FARKI: birleştirilen çıktı monolitle aynı değil")
    if m_ids != p_ids:
        hatalar.append("sıra/kimlik listesi farklı" + (" (küme de farklı)" if set(m_ids) != set(p_ids) else " (yalnız sıra)"))
    if yetim:
        hatalar.append(f"sırada olmayan {len(yetim)} yetim dosya: {yetim[:5]}")
    for h in hatalar:
        print("HATA", h)
    print(f"dogrula: {len(hatalar)} fark")
    return 1 if hatalar else 0


def fark(kimlik: str, kaynak: _P, hedef: _P) -> int:
    m = next((d for d in dd.hepsi(kaynak) if d.get("id") == kimlik), None)
    p = hedef / dd.dosya_adi(kimlik)
    pb = p.read_bytes() if p.exists() else None
    mb = dd.seri(m) if m is not None else None
    if mb == pb:
        print(f"{kimlik}: aynı" if mb is not None else f"{kimlik}: iki tarafta da yok")
        return 0
    if mb is None or pb is None:
        print(f"{kimlik}: yalnız {'parçada' if mb is None else 'monolitte'} var")
        return 1
    pd = json.loads(pb)
    anahtarlar = sorted(set(m) | set(pd))
    for k in anahtarlar:
        if m.get(k) != pd.get(k):
            print(f"  alan farklı: {k}")
    if m == pd:
        print("  içerik eşit, yalnız bayt biçimi farklı (anahtar sırası?)")
    return 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("komut", choices=["bol", "birlestir", "dogrula", "fark", "durum"])
    ap.add_argument("kimlik", nargs="?")
    ap.add_argument("--hedef", type=_P, default=VARSAYILAN_HEDEF, help="parça dizini")
    ap.add_argument("--kaynak", type=_P, default=dd.YOL, help="monolit (varsayılan deste deposunun yolu)")
    ap.add_argument("--cikti", type=_P, help="birlestir çıktısı")
    ap.add_argument("--kalici", action="store_true", help="bol: src/data/desteler/ hedefine izin ver")
    a = ap.parse_args()
    if a.komut == "durum":
        # Parçalı ya da çift yazım bayrağı açıksa dizin; kapalıysa boş çıktı (davranış değişmez)
        if dd._parcali() or dd._cift():
            print(dd.parca_dizini().resolve())
        return 0
    if a.komut == "bol":
        bol(a.kaynak, a.hedef, a.kalici)
    elif a.komut == "birlestir":
        if not a.cikti:
            ap.error("--cikti gerekli")
        birlestir(a.hedef, a.cikti)
    elif a.komut == "dogrula":
        return dogrula(a.kaynak, a.hedef)
    else:
        if not a.kimlik:
            ap.error("fark <kimlik>")
        return fark(a.kimlik, a.kaynak, a.hedef)
    return 0


if __name__ == "__main__":
    sys.exit(main())
