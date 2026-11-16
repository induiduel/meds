#!/usr/bin/env python3
"""Örnek soru setinin hoca profiline uygunluğu (LLM yok). soru_uslup.py'ye EK kapı.

  python3 scripts/hoca_profili/profil_kapisi.py <ornek_sorular.json> --ders "Tıbbi Farmakoloji"

Kural: ders profili güveni yüksek + set ≥20 soru → sapma HATA; orta → UYARI; düşük → UYARI. Tolerans ±10 puan (kalıp, düzey) ve
şık ölçüleri için makul bantlar. Soru başına: hepsi/hiçbiri HATA (guven bağımsız), doğru şık tek başına en uzun ise UYARI.
Çıkış 0 = HATA yok. Rapor "kaç soru hangi kalıba/düzeye çevrilmeli" der (kısmi düzeltme).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ortak import bilgi_turu, bilissel_duzey, kok_kalibi, norm, sik_ozellik  # noqa: E402
from profil_oku import profil_yukle  # noqa: E402

TOL = 0.10


def duz(q: dict) -> dict:
    """İki yayın biçimi: {soru, secenekler{A:..}, dogru} ve {kok, siklar[...], cevap 'A'} → birincisi."""
    if "kok" in q and "siklar" in q:
        return dict(id=q.get("id") or q.get("onem_id", "?"), soru=q["kok"], secenekler={"ABCDE"[i]: t for i, t in enumerate(q["siklar"])}, dogru=q.get("cevap"))
    return q


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("dosya", type=Path)
    ap.add_argument("--ders", required=True)
    a = ap.parse_args()
    veri = json.loads(a.dosya.read_text())
    if isinstance(veri, dict) and "kazanimlar" in veri:
        sorular = [q for k in veri["kazanimlar"] for q in k.get("sorular", [])]
    else:
        sorular = (veri.get("sorular") or veri.get("sorular_listesi") or []) if isinstance(veri, dict) else veri
    sorular = [duz(q) for q in sorular]
    u, _ = profil_yukle(a.ders)
    hata, uyari = [], []
    n = len(sorular)
    say_k, say_d, say_t = {}, {}, {}
    sf_dogru_uzun = bilesik = 0
    for q in sorular:
        qid = q.get("id", "?")
        sec = q.get("secenekler") or {}
        anahtarlar = list(sec) if isinstance(sec, dict) else list(range(len(sec)))
        degerler = [str(sec[k]) for k in anahtarlar]
        if q.get("dogru") not in anahtarlar or len(degerler) < 4:
            continue
        di = anahtarlar.index(q["dogru"])
        kok = str(q.get("soru", ""))
        f = sik_ozellik(degerler, di)
        kal = kok_kalibi(kok)
        tur = bilgi_turu(kok, degerler[di])
        du = bilissel_duzey(kal, tur, kok)
        for d_, x in ((say_k, kal), (say_d, du), (say_t, tur)):
            d_[x] = d_.get(x, 0) + 1
        if f["hepsi_hicbiri"]:
            hata.append(f"{qid}: 'hepsi/hiçbiri' şıkkı (profil: %{round(u['sik']['hepsi_hicbiri_orani']*100)})")
        if f["dogru_en_uzun"]:
            sf_dogru_uzun += 1
        bilesik += f["bilesik"]
    if n >= 8:
        sev = hata if (u["guven"] == "yuksek" and n >= 20) else uyari
        for ad, say, hedef in (("kök kalıbı", say_k, u["kok_kalibi"]), ("bilişsel düzey", say_d, u["bilissel_duzey"])):
            for k in set(hedef) | set(say):
                h, b = hedef.get(k, 0), say.get(k, 0) / n
                if abs(b - h) > TOL + (0.05 if n < 30 else 0):
                    fark = round((h - b) * n)
                    sev.append(f"set/{ad}: {k} %{b*100:.0f}, profil %{h*100:.0f} → {fark:+d} soru ({'bu türe çevrilmeli' if fark > 0 else 'başka türe çevrilmeli'})")
        if sf_dogru_uzun / n > max(0.25, u["sik"]["dogru_en_uzun_orani"] + TOL):
            uyari.append(f"set: doğru şık tek başına en uzun %{sf_dogru_uzun/n*100:.0f} (profil %{u['sik']['dogru_en_uzun_orani']*100:.0f}) — ipucu riski")
        if abs(bilesik / n - u["sik"]["bilesik_sik_orani"]) > 0.25:
            uyari.append(f"set: bileşik şık oranı %{bilesik/n*100:.0f}, profil %{u['sik']['bilesik_sik_orani']*100:.0f}")
        # bilgi türü çeşitliliği: tek türe yığılma
        if say_t and max(say_t.values()) / n > 0.6:
            uyari.append(f"set: sorular tek bilgi türüne yığılmış ({max(say_t, key=say_t.get)} %{max(say_t.values())/n*100:.0f}); profil: {list(u['bilgi_turu'].items())[:3]}")
    for h in hata:
        print("HATA", h)
    for w in uyari:
        print("UYARI", w)
    print(f"{n} soru · profil güveni {u['guven']} · {len(hata)} HATA · {len(uyari)} UYARI")
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main())
