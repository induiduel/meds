#!/usr/bin/env python3
"""Örnek soru kaynak kapısı (kullanıcı kararı 2026-10-29, H-ÖS1). LLM yok.

  python3 scripts/tam_hat/ornek_soru_kaynak.py <ornek_sorular.json> <orijinal.pdf | sayfalar.json> [--esik 0.5]
  python3 scripts/tam_hat/ornek_soru_kaynak.py --hepsi        # src/data/ornek_sorular/k2 + KAYNAKLAR eşlemesi

Neden: kaynak_kapisi.py yalnız `s` alanlı kayda bakar; örnek sorular sayfayı `kanit.sayfa`da taşır ve `sik_aciklamalari`
hiçbir kapıdan geçmiyordu → şık açıklamasına slaytta olmayan bilgi ("yaklaşık 12 saat sonra", k2-03 q02) sızdı.

Denetim (her soru):
  1. kanit.alinti, kanit.sayfa (±1) metninde harfi harfine (katlanmış, boşluk normalize) geçmeli → HATA.
  2. soru / secenekler / aciklama / sik_aciklamalari içindeki her sayı (s. N atıfları hariç) ders PDF'inde geçmeli → HATA.
  3. aciklama içindeki her "(s. N)" atfı: atfın bulunduğu cümlenin içerik kökleri N±1 sayfada en az %esik → HATA.
  4. Her şık açıklaması ve aciklama: içerik köklerinin ders metninde bulunmayanları ≥2 ise HATA (kaynak dışı ekleme),
     1 ise UYARI. Genel anlatım sözcükleri GENEL kümesinde.
Çıkış 0 = HATA yok.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]
KATLA = str.maketrans("çğıöşüâîûÇĞIİÖŞÜ", "cgiosuaiucgiiosu")
# Ders adı → orijinal PDF (bu yılın dersi; arşiv değil)
KAYNAKLAR = {
    "k2-01": "meds_temp/ogrenci_ders/k2-01/orijinal.pdf",
    "k2-02": "meds_temp/ogrenci_ders/k2-02/orijinal.pdf",
    "k2-03": "meds_temp/ogrenci_ders/pato/p1_orijinal.pdf",
    "k2-04": "meds_temp/ogrenci_ders/pato/p2_orijinal.pdf",
    "k2-05": "meds_temp/ogrenci_ders/k2-05/orijinal.pdf",
    "k2-07": "meds_temp/gercek_pdf/k2-07.pdf",
    "k2-08": "meds_temp/ogrenci_ders/k2-08/orijinal.pdf",
}
# Şık açıklamasında kaynakta olmasa da serbest olan anlatım sözcükleri (5 harf kök)
GENEL = {k[:5] for k in """
olarak oldugu olmasi sonucu nedeniyle ancak ayrica ozellikle arasinda seklinde hangisi asagidakilerden dogrudur
yanlistir derste sayfa sayilir verilir belirtilir soruda sorunun secenek cevap cevaptir dogru yanlis beklenen
beklenmeyen bulgu bulgusu bulgudur ozellik ozelligi ifade ifadesi aranan istisna elenir olamaz gorulur gorulen
tipik temel birlikte nedenle yaklasik oldugundan oldugu icin degil degildir boyle burada bunun buna kadar sonra
once daha fazla dolayi tanimi tanimlar anlami adini veren tanir taninir sayilan ilkdir sayilir yerine gosterir
gostermez anlatilir aittir ait karistirilir karistirma tuzak celdirici diger baska ayni benzer farkli
""".split()}


def katla(m: str) -> str:
    return re.sub(r"\s+", " ", m.translate(KATLA).lower()).strip()


def kokler(m: str) -> set[str]:
    return {w[:5] for w in re.findall(r"[a-z]+", katla(m)) if len(w) >= 5}


def sayfalar_oku(yol: Path) -> dict[int, str]:
    if yol.suffix == ".json":
        d = json.loads(yol.read_text())
        if isinstance(d, list):
            return {i + 1: (x if isinstance(x, str) else x.get("metin", "")) for i, x in enumerate(d)}
        return {int(k): v for k, v in d.items()}
    ham = subprocess.run(["pdftotext", "-layout", str(yol), "-"], capture_output=True, text=True, check=True).stdout
    return {i + 1: s for i, s in enumerate(ham.split("\f"))}


def sayilar(m: str) -> set[str]:
    m = re.sub(r"\(?\b(?:s\.|sayfa|slayt)\s*\d+(\s*(?:[-–,]|ve)\s*\d+)*\)?", " ", m, flags=re.I)  # sayfa atıfları
    return set(re.findall(r"\d+(?:[.,]\d+)?", m))


def sorular(d) -> list[dict]:
    out = []
    for k in d.get("kazanimlar", []):
        out += k.get("sorular", [])
    out += d.get("sorular", [])
    return out


def denetle(dosya: Path, kaynak: Path, esik: float) -> tuple[list, list, int]:
    sf = sayfalar_oku(kaynak)
    tum = katla(" ".join(sf.values()))
    tum_kok = kokler(tum)
    tum_say = set(re.findall(r"\d+(?:[.,]\d+)?", tum))
    hata, uyari = [], []
    qs = sorular(json.loads(dosya.read_text()))
    for q in qs:
        qid = q.get("id", "?")
        kn = q.get("kanit") or {}
        s = kn.get("sayfa")
        al = katla(kn.get("alinti", ""))
        if not al or not isinstance(s, int):
            hata.append(f"{qid}: kanit.sayfa/alinti eksik")
        else:
            komsu = katla(" ".join(sf.get(p, "") for p in (s - 1, s, s + 1)))
            parca = [p for p in re.split(r"\s*[–\-…]\s*|\.\.\.", al) if len(p) > 6]
            eksik = [p for p in parca if re.sub(r"[^a-z0-9 ]", "", p) not in re.sub(r"[^a-z0-9 ]", "", komsu)]
            if eksik:
                hata.append(f"{qid}: alıntı s.{s} sayfasında yok → {eksik[0][:60]!r}")
        metinler = {"soru": q.get("soru", ""), "aciklama": q.get("aciklama", "")}
        metinler.update({f"secenek {h}": v for h, v in (q.get("secenekler") or {}).items()})
        metinler.update({f"şık {h}": v for h, v in (q.get("sik_aciklamalari") or {}).items()})
        for ad, m in metinler.items():
            yok = sorted(n for n in sayilar(m) if n not in tum_say)
            if yok:
                hata.append(f"{qid} [{ad}]: kaynakta olmayan sayı {yok} → {m[:90]!r}")
            if ad.startswith("şık") or ad == "aciklama":
                ick = {k for k in kokler(m) if k not in GENEL}
                disari = sorted(ick - tum_kok)
                if len(disari) >= 4 and len(disari) / max(1, len(ick)) > 0.5:
                    hata.append(f"{qid} [{ad}]: kaynakta olmayan kavram {disari} → {m[:90]!r}")
                elif disari:
                    uyari.append(f"{qid} [{ad}]: kaynakta olmayan sözcük {disari}")
        for cumle in re.split(r"(?<=[.)])\s+", " ".join([q.get("aciklama", "")] + list((q.get("sik_aciklamalari") or {}).values()))):
            for ref in re.findall(r"(?:s\.|sayfa)\s*(\d+)", cumle, flags=re.I):
                n = int(ref)
                hedef = kokler(" ".join(sf.get(p, "") for p in (n - 1, n, n + 1)))
                ck = {k for k in kokler(cumle) if k not in GENEL}
                if ck and len(ck & hedef) / len(ck) < esik:
                    hata.append(f"{qid}: 's. {n}' atfı tutmuyor (%{100*len(ck & hedef)//len(ck)}) → {cumle[:80]!r}")
    return hata, uyari, len(qs)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dosya", nargs="?", type=Path)
    ap.add_argument("kaynak", nargs="?", type=Path)
    ap.add_argument("--esik", type=float, default=0.3)
    ap.add_argument("--hepsi", action="store_true")
    ap.add_argument("--uyari", action="store_true", help="uyarıları da yaz")
    a = ap.parse_args()
    isler = []
    if a.hepsi:
        for f in sorted((KOK / "meds/src/data/ornek_sorular/k2").glob("k2-0*.json")):
            k = f.name[:5]
            if k in KAYNAKLAR:
                isler.append((f, KOK / KAYNAKLAR[k]))
            else:
                print(f"HATA {f.name}: KAYNAKLAR eşlemesi yok")
                return 1
    else:
        isler.append((a.dosya, a.kaynak))
    toplam = 0
    for f, k in isler:
        h, u, n = denetle(f, k, a.esik)
        toplam += len(h)
        print(f"{f.name}: {n} soru, {len(h)} HATA, {len(u)} UYARI")
        for x in h:
            print("  HATA", x)
        if a.uyari:
            for x in u:
                print("  UYARI", x)
    return 1 if toplam else 0


if __name__ == "__main__":
    sys.exit(main())
