#!/usr/bin/env python3
"""İşe başlamadan anlama sınavı (dış ajan protokolü §12-5). LLM yok. %100 değilse iş başlamaz.

  python3 scripts/tam_hat/dis_ajan/anlama_sinavi.py sorular  <W>   # W/sinav_sorulari.json üretir (cevapsız)
  python3 scripts/tam_hat/dis_ajan/anlama_sinavi.py puanla   <W> --ajan <etiket> --ders <k2-07>
        # W/sinav_cevaplari.json = {"q01": 1, "q02": 2, …} (seçenek sırası 0'dan)
Yanlış cevapta ilgili KURAL yazdırılır; ajan kuralı okuyup sınavı yeniden yapar. Geçince W/sinav_gecti.json yazılır.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

BANKA = Path(__file__).with_name("sinav_bankasi.json")


def surum() -> str:
    """Soru bankası + TALIMAT özeti: yönerge ya da sınav değişince eski geçiş kaydı geçersiz olur (yeniden sınav)."""
    h = hashlib.sha256()
    for f in (BANKA, Path(__file__).with_name("TALIMAT_DIS_AJAN.md")):
        h.update(f.read_bytes())
    return h.hexdigest()[:16]


def imza(ajan: str, ders: str, tarih: str) -> str:
    return hashlib.sha256(f"{ajan}|{ders}|{tarih}|{surum()}|sinav-gecti".encode()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mod", choices=["sorular", "puanla"])
    ap.add_argument("W", type=Path)
    ap.add_argument("--ajan")
    ap.add_argument("--ders")
    a = ap.parse_args()
    banka = json.loads(BANKA.read_text("utf8"))
    if a.mod == "sorular":
        a.W.mkdir(parents=True, exist_ok=True)
        (a.W / "sinav_sorulari.json").write_text(json.dumps(
            [{k: q[k] for k in ("id", "soru", "secenekler")} for q in banka], ensure_ascii=False, indent=1), "utf8")
        print(f"{len(banka)} soru yazıldı: {a.W/'sinav_sorulari.json'}\nCevapları {a.W/'sinav_cevaplari.json'} dosyasına "
              f'{{"q01": <seçenek sırası>, …}} olarak yaz, sonra "puanla" çalıştır.')
        return 0
    if not (a.ajan and a.ders):
        print("HATA --ajan ve --ders gerekli")
        return 2
    try:
        cev = json.loads((a.W / "sinav_cevaplari.json").read_text("utf8"))
    except Exception as e:  # noqa: BLE001
        print(f"HATA sinav_cevaplari.json okunamadı: {e}")
        return 2
    yanlis = []
    for q in banka:
        v = cev.get(q["id"])
        if not isinstance(v, int) or hashlib.sha256(f"{q['id']}:{v}".encode()).hexdigest() != q["dogru_hash"]:
            yanlis.append(q)
    for q in yanlis:
        print(f"YANLIŞ/EKSİK {q['id']}: {q['soru']}\n   KURAL: {q['aciklama']}")
    puan = len(banka) - len(yanlis)
    print(f"Puan: {puan}/{len(banka)}")
    if yanlis:
        print("GEÇEMEDİN: yukarıdaki kuralları oku, cevapları düzelt ve yeniden puanla. İşe başlama.")
        return 1
    t = date.today().isoformat()
    (a.W / "sinav_gecti.json").write_text(json.dumps(
        {"ajan": a.ajan, "ders": a.ders, "tarih": t, "puan": puan, "toplam": len(banka), "surum": surum(), "imza": imza(a.ajan, a.ders, t)}, indent=1), "utf8")
    print("GEÇTİN: sinav_gecti.json yazıldı.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
