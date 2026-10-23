#!/usr/bin/env python3
"""Kroki zinciri (R1 + R2) — gece hattı aşaması `kroki` (ICERIK_MOTORU_V3.md §2, §12, §15, §16).

Ders başına, yalnız girdisi değişen adım çalışır:
  1. L0 (`l0.py`)            — PDF karması / şema sürümü değişmediyse atlanır; aynı sayfaların OCR'ı taşınır.
  2. ok + SoM (`ok.py`, `som.py`) — L0 yeniden üretildiyse ya da alanlar yoksa (L0 `r1b` damgası).
  3. çıkmış dizini (`dizin.py`)   — kurul başına bir kez; kaynak değişmediyse önbellekten hızlı.
  4. tarama planı (`plan.py`)     — TEK DERS kuralı tüm dersleri birlikte görür: bir kez, toplu; dizin, ders kümesi ya da
                                    bir PDF değişince yeniden.
  5. kanıt bölgeleri (`kanit.py`) — plan ya da L0 değişince.
Hata veren ders diğerlerini durdurmaz; sonunda hata sayısı kadar çıkış kodu ≠ 0 (sessiz başarısızlık yok).

Kullanım (.venv-ocr): zincir.py [--kurul N | --ders kN-NN] [--zorla]
   varsayılan: bilgi deposundaki TÜM dersler (Kurul 1 dahil — yalnız okur ve kendi l0/l1 klasörüne yazar; K1 içerik
   dosyalarına dokunmaz).
"""
from __future__ import annotations

import argparse
import sys
import time
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "cikmis_dizin"))
import pymupdf  # noqa: E402

import dizin as D  # noqa: E402
import kanit as K  # noqa: E402
import l0 as L0  # noqa: E402
import l0kayit  # noqa: E402
import ok as OK  # noqa: E402
import plan as P  # noqa: E402
import som as SOM  # noqa: E402
from ortak import DEPO, dersler, oku, pdf_bul  # noqa: E402

R1B_SURUM = {"ok": 2, "som": 1}


def r1b(ders: str, zorla: bool) -> str:
    l0 = l0kayit.yukle(ders)
    damga = l0.get("r1b") or {}
    if not zorla and damga == {**R1B_SURUM, "pdf_sha": l0["pdf_sha"]}:
        return "güncel"
    belge = pymupdf.open(pdf_bul(ders))
    alanlar: dict[int, dict] = {}
    n_ok = n_roi = 0
    for s in l0["sayfalar"]:
        sayfa = belge[s["sayfa"] - 1]
        o = OK.bagla(sayfa, s)
        roi, _ = SOM.sayfa_som(belge, s, ders)
        alanlar[s["sayfa"]] = {"ok": o, "roi": roi}
        n_ok += len(o); n_roi += len(roi)
    l0kayit.yaz_toplu(ders, alanlar)
    d = l0kayit.yukle(ders)
    d["r1b"] = {**R1B_SURUM, "pdf_sha": d["pdf_sha"]}
    from ortak import yaz
    yaz(l0kayit.yol(ders), d)
    return f"{n_ok} ok, {n_roi} bölge"


def calistir(liste: list[str], zorla: bool) -> int:
    hata = 0
    eksik: dict[str, str] = {}
    t0 = time.time()
    for ders in liste:
        try:
            L0.uret(ders, zorla=zorla, log=lambda m: print("  " + m))
            print(f"  {ders}: ok/SoM {r1b(ders, zorla)}")
        except SystemExit as e:
            if "PDF bulunamadı" in str(e):
                # bilinen veri eksiği (Drive'da yok / depo metni başka yılın PDF'i): hata değil, eksik kaynak raporu
                eksik[ders] = str(e)
                print(f"  {ders}: eksik kaynak — {e}")
            else:
                print(f"  {ders}: L0 HATA {e}"); hata += 1
        except Exception:  # noqa: BLE001
            print(f"  {ders}: L0 HATA\n{traceback.format_exc()[-600:]}"); hata += 1
    try:
        D.kur(log=lambda m: print("  " + m))
        dz = D.yukle()
    except Exception as e:  # noqa: BLE001
        print(f"  çıkmış dizini HATA: {e}")
        return hata + 1
    try:
        planlar = P.kur_hepsi([x for x in liste if (DEPO / x / "l0" / "sayfalar.json").exists()], zorla=zorla, dz=dz,
                              log=lambda m: print("  " + m))
    except Exception:  # noqa: BLE001
        print(f"  tarama planı HATA\n{traceback.format_exc()[-600:]}")
        return hata + 1
    for ders, pl in planlar.items():
        try:
            kn = oku(DEPO / ders / "l1" / "kanit.json") or {}
            if zorla or kn.get("pdf_sha") != pl["pdf_sha"] or kn.get("dizin_sha") != pl["dizin_sha"] \
                    or kn.get("kume_sha") != pl.get("kume_sha") or kn.get("surum") != K.SURUM:
                K.kur(ders, dz=dz, log=lambda m: print("  " + m))
        except SystemExit as e:
            print(f"  {ders}: kanıt {e}")
            hata += 1
        except Exception:  # noqa: BLE001
            print(f"  {ders}: kanıt HATA\n{traceback.format_exc()[-600:]}"); hata += 1
    from ortak import TEMP, yaz
    yaz(TEMP / "kroki" / "eksik_kaynak.json", {"zaman": time.strftime("%Y-%m-%dT%H:%M:%S"), "dersler": eksik}, 1)
    print(f"kroki zinciri: {len(liste)} ders, {hata} hata, {len(eksik)} eksik kaynak "
          f"(meds_temp/kroki/eksik_kaynak.json), {time.time() - t0:.0f} sn")
    return 1 if hata else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kurul", type=int); ap.add_argument("--ders"); ap.add_argument("--zorla", action="store_true")
    a = ap.parse_args()
    liste = [a.ders] if a.ders else dersler(a.kurul)
    return calistir(liste, a.zorla)


if __name__ == "__main__":
    sys.exit(main())
