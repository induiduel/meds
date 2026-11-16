#!/usr/bin/env python3
"""Tam içerik işçisinin okuyacağı kısa hoca-profili özeti (LLM yok).

  python3 scripts/hoca_profili/profil_oku.py --ders "Tıbbi Patoloji" [--konu "Tiroid ve Paratiroid"] [--json]

Verilen ders+konu için: üslup hedefleri (kalıp/bilgi türü/düzey/şık), konunun kazanım haritası girdisi (neden-nasıl-hangi bilgi-zorluk-
çeldirici-kaynak bağımlılığı, tekrar eden çekirdek kavramlar), güven düzeyi ve GÜVEN KURALI. Konu eşleşmezse ders geneli verilir.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ortak import CIKTI, jetonlar, slug  # noqa: E402

GUVEN_KURALI = {
    "yuksek": "Profil hedefleri bağlayıcıdır (kapı: profil_kapisi.py ±10 puan).",
    "orta": "Profil hedefleri yol göstericidir; kapı UYARI verir, HATA vermez.",
    "dusuk": "Veri az (n<40): ders profili değil `_genel` profil ve konu başlığı bazlı yazım esas; kapı yalnız UYARI.",
}


def profil_yukle(ders: str) -> tuple[dict, list[dict]]:
    d = CIKTI / slug(ders)
    if not (d / "uslup.json").exists():
        g = json.loads((CIKTI / "_genel/uslup.json").read_text())
        g["guven"] = "dusuk"
        g["not"] = f"'{ders}' için çıkmış yok → genel profil"
        return g, []
    return json.loads((d / "uslup.json").read_text()), json.loads((d / "kazanim_haritasi.json").read_text())["konular"]


def konu_bul(harita: list[dict], konu: str) -> dict | None:
    kj = set(jetonlar(konu))
    en, ens = None, 0.0
    for h in harita:
        hj = set(jetonlar(h["konu"]))
        if not kj or not hj:
            continue
        s = len(kj & hj) / len(kj | hj)
        if s > ens:
            en, ens = h, s
    return en if ens >= 0.34 else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ders", required=True)
    ap.add_argument("--konu")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    u, harita = profil_yukle(a.ders)
    h = konu_bul(harita, a.konu) if a.konu else None
    if a.json:
        print(json.dumps(dict(uslup=u, konu=h), ensure_ascii=False, indent=1))
        return 0
    top = lambda d, k=5: ", ".join(f"{x} %{round(v*100)}" for x, v in list(d.items())[:k])
    print(f"## {a.ders} — {u['n_soru']} tekil çıkmış, güven {u['guven']}. {GUVEN_KURALI[u['guven']]}")
    print(f"- Kök kalıbı: {top(u['kok_kalibi'])}")
    print(f"- Bilgi türü (neden sorulur): {top(u['bilgi_turu'])}")
    print(f"- Bilişsel düzey: {top(u['bilissel_duzey'])}")
    k, s = u["kok_kelime"], u["sik"]
    print(f"- Kök {k['p25']}–{k['p75']} kelime (ort {k['ort']}); şık ort {s['kelime_ort']} kelime; bileşik şık %{round(s['bilesik_sik_orani']*100)}; "
          f"doğru en uzun %{round(s['dogru_en_uzun_orani']*100)}; hepsi/hiçbiri %{round(s['hepsi_hicbiri_orani']*100)}")
    print(f"- Çeldirici stratejisi: {top(u['celdirici_stratejisi'], 4)}")
    if u["donem_kaymasi_2023_sonrasi"]:
        print(f"- Dönem kayması (2023+): {u['donem_kaymasi_2023_sonrasi']}")
    if a.konu and not h:
        print(f"- Konu '{a.konu}' haritada yok (çıkmışı yok/az) → yalnız ders profili; konuyu ders geneli bilgi türü payına göre kurgula.")
    if h:
        print(f"### Konu: {h['konu']} — {h['n_soru']} soru, yıllar {h['yillar']}, güven {h['guven']}")
        for n in h["neden_sorulur"]:
            print(f"- NEDEN: {n['bilgi_turu']} %{round(n['pay']*100)} — {n['gerekce']}")
        print(f"- NASIL: {h['nasil_sorulur']['kurulus']} Kalıp: {top(h['nasil_sorulur']['kok_kalibi'], 4)}; düzey: {top(h['nasil_sorulur']['bilissel_duzey'], 3)}")
        print(f"- ÇELDİRİCİ: {top(h['hangi_bilgilerle']['celdirici'], 3)} · ZORLUK: {h['zorluk']} · KAYNAK BAĞIMLILIĞI: özet kanıtlı %{round(h['kaynaga_bagimlilik']['ozet_kanitli_oran']*100)}")
        for c in h["cekirdek_kavramlar"][:6]:
            print(f"- TEKRAR EDEN ÇEKİRDEK: {c['kavram']} ({c['kez']}×, yıllar {c['yillar']}, kalıplar {c['kaliplar']}) örnek kök: {c['ornek_kok'][:110]}")
        for kk in h["tipik_kok_ornekleri"]:
            print(f"- TİPİK KÖK: {kk}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
