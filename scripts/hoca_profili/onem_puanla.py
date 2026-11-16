#!/usr/bin/env python3
"""Ders metninde "soruya müsait yerler" + önerilen soru dönüşümü (LLM yok).

  python3 scripts/hoca_profili/onem_puanla.py <ders_metni.md|sayfa_metni.txt> --ders "Tıbbi Farmakoloji" [--ilk 25]

Her satıra iki şey verir: (a) önem ipucu puanı (satır modeli: bileşik sıra = biçim+işaret ve ders içi tekrar), (b) hangi soru
kalıbı/dönüşümüyle sorulabileceği (hocanın üç dönüşümü + bilgi türü). ÖNEMLİ — güven sınırı (docs/HOCA_USLUBU_YONTEMI.md §6):
satır modeli aynı biçimli geçmiş özetlerde AUC≈0,66–0,73 (rastgele 0,5), AMA 2026-27 Kurul 1 yeni ders notlarında rastgele
düzeyinde ölçüldü. Bu nedenle çıktı yalnız ADAY LİSTESİDİR: kanıt (kalın, tekrar, hoca sesi, çıkmış eşlemesi) ve tıbbi gerekçe
olmadan tek başına "önemli" kararı verilmez. Çıktı hangi işaretin neden tetiklendiğini yazar.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from satir_model import ISARET_RX, ILAC_EK, skorla_dosya  # noqa: E402
from ortak import norm  # noqa: E402

ONERI = {
    "tanim": ("tanim_kavram", "ters_ad: olgu/ölçüt verilir, terim sorulur"),
    "siniflama": ("siniflama_ad", "birleştirme: iki ardışık madde tek şıkta; komşu tip/evre çeldirici"),
    "karsit": ("ayirici", "kopya+çevirme ya da olumsuz kök (istisna/ancak cümlesi mutlaklaştırılır)"),
    "kontrendike": ("ilac_yan_etki", "ilaçtan yan etkiye ve ters yön; çeldirici aynı sınıfın üyesi"),
    "ilk_secim": ("ilac_endikasyon", "durumdan ilaca; çeldirici ikinci basamak ilaç"),
    "tani_koydurucu": ("tanimlayici_bulgu", "ters_yon: bulgudan hastalığa ve hastalıktan bulguya"),
    "neden_sonuc": ("mekanizma", "mekanizma halkası sorulur; çeldirici komşu halka (sıra/zincir)"),
    "karsilastirma": ("tani_ayirici", "eşleştirme/ayırt edici tek bulgu; çeldirici benzer hastalık"),
    "en_sik": ("etiyoloji_risk", "'en sık/en tipik' kökü; çeldirici daha seyrek nedenler"),
    "tablo_satiri": ("eslestirme", "tablo hücresi → çapraz eşleme; çeldirici yer değiştirmiş hücre"),
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("dosya", type=Path)
    ap.add_argument("--ders", required=True)
    ap.add_argument("--ilk", type=int, default=25)
    a = ap.parse_args()
    sat, sk, b, t, fe = skorla_dosya(a.dosya)
    sira = sorted(range(len(sat)), key=lambda i: -sk[i])[: a.ilk]
    print(f"# {a.dosya.name} — {len(sat)} satır; ilk {len(sira)} aday (GÜVEN: düşük-orta; kanıtsız önem kararı verme)")
    for r_, i in enumerate(sira, 1):
        s = sat[i]
        tl = norm(s["t"])
        tetik = [k for k, rx in ISARET_RX.items() if (s["tablo"] if k == "tablo_satiri" else rx.search(tl))]
        if re.search(r"\d", s["t"]) and re.search(r"%|yüzde|oran|\bsıklık", tl):
            tetik.append("sayi_oran")
        if ILAC_EK.search(tl):
            tetik.append("ilac")
        oneri = [ONERI[k][1] for k in tetik if k in ONERI][:2] or ["doğrudan kavram sorusu; komşu kavramlı çeldirici"]
        print(f"{r_:>2}. [{sk[i]:.2f}] {s['t'][:130]}\n    işaret: {', '.join(tetik) or '—'} · öneri: {' | '.join(oneri)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
