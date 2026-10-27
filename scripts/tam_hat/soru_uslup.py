#!/usr/bin/env python3
"""Örnek soru üslup kapısı (H119; kullanıcı kararı 2026-10-28). LLM yok.

  python3 scripts/tam_hat/soru_uslup.py <ornek_sorular.json> [--uslup <soru_uslubu.json>]

Soru başına HATA (yalnız o soru yeniden yazılır — kısmi düzeltme):
  - kökte/şıkta ders çağrıştıran ifade (derste, slayt, sunum, hoca, bu bölümde, metne göre, sayfa N, yukarıda …)
  - şık sayısı 5 değil, boş/tekrarlı şık, doğru anahtar şıklarda yok
  - kök 4 kelimeden kısa ya da aynı kök iki kez
  - kazanım bağı yok (`kazanim` alanı) — her soru bir kazanıma hizmet eder
  - doğru şık (≥6 kelime) en uzun şık ve ötekilerin ortalamasının 1,8 katından uzun (klasik ipucu)
Set düzeyi (soru_uslubu.json verilirse; tolerans ±%10 = 10 puan, kullanıcı kuralı):
  - olumsuz kök / vaka / öncüllü kalıp payı çıkmış payından 10 puandan fazla saparsa HATA; rapor kaç sorunun hangi kalıba
    çevrileceğini söyler (bütün set değil, yalnız o kadar soru yeniden yazılır). n < 20 ise UYARI.
  - ortalama kök uzunluğu çıkmış ortalamasının ±%10'u dışında → UYARI (kalite kararı denetçide).
Çıkış 0 = HATA yok.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from soru_uslup_ornek import kalip  # noqa: E402

YASAK = re.compile(r"\b(derste|dersin|bu ders|slayt|sunum|hocan|hoca\b|bu bölüm|dersin bölüm|metne göre|metinde|"
                   r"yukarıda|kaynakta|notlarda|sayfa\s*\d+|anlatılan)", re.I)
TOLERANS = 0.10


def norm(s: str) -> str:
    return re.sub(r"\W+", " ", s.lower()).strip()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dosya", type=Path)
    ap.add_argument("--uslup", type=Path)
    a = ap.parse_args()
    veri = json.loads(a.dosya.read_text())
    if isinstance(veri, dict) and "kazanimlar" in veri:  # yayın biçimi: kazanım → sorular
        sorular = [q for k in veri["kazanimlar"] for q in k.get("sorular", [])]
    else:
        sorular = veri["sorular"] if isinstance(veri, dict) else veri
    hata: list[str] = []
    uyari: list[str] = []
    gorulen: set[str] = set()
    for q in sorular:
        qid = q.get("id", "?")
        kok = str(q.get("soru", "")).strip()
        sec = q.get("secenekler") or {}
        degerler = [str(v).strip() for v in (sec.values() if isinstance(sec, dict) else sec)]
        for m in {m.group(0) for m in YASAK.finditer(" ".join([kok, *degerler]))}:
            hata.append(f"{qid}: ders çağrıştıran ifade «{m}» (kök bağımsız, çıkmış kalıbında olmalı)")
        if len(degerler) != 5 or any(not d for d in degerler):
            hata.append(f"{qid}: 5 dolu şık gerekli ({len(degerler)})")
        if len({norm(d) for d in degerler}) != len(degerler):
            hata.append(f"{qid}: tekrarlı şık")
        if isinstance(sec, dict) and q.get("dogru") not in sec:
            hata.append(f"{qid}: doğru anahtar şıklarda yok")
        if len(kok.split()) < 4:
            hata.append(f"{qid}: kök çok kısa")
        if norm(kok) in gorulen:
            hata.append(f"{qid}: aynı kök tekrar")
        gorulen.add(norm(kok))
        if q.get("kazanim") in (None, "", []):
            hata.append(f"{qid}: kazanım bağı yok")
        if isinstance(sec, dict) and q.get("dogru") in sec and len(degerler) == 5:
            d = len(str(sec[q["dogru"]]))
            obur = [len(str(v)) for k, v in sec.items() if k != q["dogru"]]
            # Yalnız tanımlayıcı doğru şık (≥6 kelime): tek terimlik ad şıklarında uzunluk ipucu sayılmaz (k2-08: SEDC, mavi sklera)
            if len(str(sec[q["dogru"]]).split()) >= 6 and d == max(d, *obur) and d > 1.8 * (sum(obur) / len(obur)):
                hata.append(f"{qid}: doğru şık belirgin biçimde en uzun (ipucu)")
    if a.uslup and sorular:
        u = json.loads(a.uslup.read_text())
        n = len(sorular)
        say = {k: 0 for k in ("olumsuz", "vaka", "onculu", "dogrudan")}
        for q in sorular:
            say[kalip(str(q.get("soru", "")))] += 1
        for k in ("olumsuz", "vaka", "onculu"):
            hedef, bizde = u["kalip_payi"].get(k, 0), say[k] / n
            if abs(bizde - hedef) > TOLERANS:
                fark = round((hedef - bizde) * n)
                yon = f"{fark} soru bu kalıba çevrilmeli" if fark > 0 else f"{-fark} soru başka kalıba çevrilmeli"
                (hata if n >= 20 else uyari).append(f"set: {k} payı %{bizde * 100:.0f}, çıkmış %{hedef * 100:.0f} → {yon}")
        ort = sum(len(str(q.get("soru", "")).split()) for q in sorular) / n
        if abs(ort - u["kok_kelime_ort"]) > TOLERANS * u["kok_kelime_ort"]:
            uyari.append(f"set: kök ort. {ort:.1f} kelime, çıkmış {u['kok_kelime_ort']}")
    for h in hata:
        print("HATA", h)
    for w in uyari:
        print("UYARI", w)
    print(f"{len(sorular)} soru · {len(hata)} HATA · {len(uyari)} UYARI")
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main())
